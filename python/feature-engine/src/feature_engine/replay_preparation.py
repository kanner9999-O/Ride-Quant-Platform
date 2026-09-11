"""Replay preparation (ADR-037, Approved; `P3-FEATURE-QG-EVID-05(b)`).

I-5 requires two strictly separated phases: *Replay preparation* (external
resolution — reading Input Contract/Stream Registry authority off the
repository filesystem — is allowed here) and *Replay execution* (must depend
only on already-materialized, persisted/cached state; never touches an
external source again, `EVID-05(a)`, `test_replay_isolation.py`).

This module is explicitly OUTSIDE the Feature analytical core — the same
role `authority_resolver.py`/`output_contract_resolver.py` already play —
and is called exactly ONCE per fact, BEFORE Replay execution begins for that
fact, never during. It never mutates, recomputes, or "repairs" a fact; a
failure here means Replay must abort for that fact, not proceed with
degraded/assumed evidence.

`P3-FEATURE-EVID05B-IMPL-A-MAJ-02` remediation: this module resolves the
EXACT historical Input Contract + Stream Registry identity a fact's own
`computation_cursor` pins — via
`authority_resolver.resolve_historical_input_contract_authority_from_repository`,
which reads ONLY the immutable ADR-041 canonical version-snapshot artifacts
(`docs/architecture/input-contract-versions/<contract_id>/<contract_version>.yaml`,
`docs/architecture/stream-registry-versions/<registry_version>.yaml`) —
NEVER `resolve_input_contract_authority_from_repository`, which reads the
current/active mutable files and is reserved for fresh (non-replay)
computation resolution. There is no fallback from one to the other.

Fails closed for each of ADR-037's four failure classes:

1. missing/unresolvable Input Contract or Stream Registry version-snapshot,
   a malformed cursor version token, or a Registry <-> Contract
   relational/self-identity inconsistency WITHIN the pinned snapshot pair
   (all detected during resolution itself, since resolution now happens BY
   the cursor's own exact identity rather than by re-deriving and comparing
   against a separately-resolved current artifact) —
   `ReplayPreparationArtifactUnresolvableError`;
2. malformed/missing `computation_dependency_content_evidence` —
   `ReplayPreparationEvidenceMalformedError`;
3. (historical note) under the prior, superseded current-path design, this
   class was "the currently-resolved artifact's own identity does not match
   the fact's own cursor" — `ReplayPreparationCursorReferenceMismatchError`.
   That comparison is structurally obsolete now that resolution is BY the
   cursor's own identity (a successful resolution's own identity always
   equals the cursor's, by construction); the underlying risk it guarded
   against is now covered by class 1's own relational/self-identity checks
   inside the historical resolver. This class is retained in `errors.py`
   for historical continuity but is no longer raised by this function;
4. the pinned snapshot's own recomputed content-identity digest does not
   match the fact's own persisted evidence (content-ID mismatch) —
   `ReplayPreparationContentIdentityMismatchError`.
"""

from __future__ import annotations

import re
from pathlib import Path

from .authority_resolver import resolve_historical_input_contract_authority_from_repository
from .contracts import FeatureComputationProfile, FeatureComputed, FeatureFactInvalidated
from .errors import (
    ReplayPreparationArtifactUnresolvableError,
    ReplayPreparationContentIdentityMismatchError,
    ReplayPreparationEvidenceMalformedError,
    UnresolvedComputationCursorAuthorityError,
)

FeatureReplayFact = FeatureComputed | FeatureFactInvalidated

# feature.md §7.1/§7.2/§7.3 — the closed, three-member feature_type enum, each
# mapped to the exact `FeatureComputationProfile` its own owning engine binds
# at construction (`regime_passthrough.py`/`swing_distance.py`'s own
# `_REQUIRED_INPUT_CONTRACT_PROFILE` constants) — mechanically transcribed
# here, not redefined or re-decided; `candle_window.py`'s `upstream_source:
# candle` path is permanently unavailable (`UnsupportedFeatureFormulaError`,
# construction always fails), so no real repository fact of feature_type
# volatility_metric/directional_persistence_metric can exist under any
# profile other than "regime" today.
_PROFILE_BY_FEATURE_TYPE: dict[str, FeatureComputationProfile] = {
    "volatility_metric": "regime",
    "directional_persistence_metric": "regime",
    "distance_to_last_confirmed_swing": "distance_to_last_confirmed_swing",
}

_CONTENT_ID_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def _is_well_formed_content_id(value: str) -> bool:
    return bool(_CONTENT_ID_PATTERN.fullmatch(value))


def prepare_replay_evidence(fact: FeatureReplayFact, *, repo_root: Path | None = None) -> None:
    """Resolves the EXACT historical Input Contract + Stream Registry
    version-snapshot named by `fact.computation_cursor` — never the
    current/active mutable files — recomputes content identities from the
    actual, immutable snapshot bytes, and compares against
    `fact.computation_dependency_content_evidence` — fails closed BEFORE
    Replay execution begins for each of ADR-037's four failure classes (see
    module docstring). Returns `None` on success; raises otherwise. Never
    called from inside Replay execution itself (`EVID-05(a)`).
    """
    feature_type = fact.scope.feature_type
    profile = _PROFILE_BY_FEATURE_TYPE.get(feature_type)
    if profile is None:
        raise ReplayPreparationArtifactUnresolvableError(
            f"no Feature computation profile is known for feature_type={feature_type!r} — cannot resolve which "
            "Input Contract/Stream Registry artifact this fact's computation_cursor names"
        )

    # Failure class 1: missing/unresolvable snapshot, malformed cursor version
    # token, or Registry <-> Contract relational/self-identity mismatch WITHIN
    # the pinned snapshot pair -- all detected during resolution itself, since
    # resolution happens BY the cursor's own exact identity (P3-FEATURE-
    # EVID05B-IMPL-A-MAJ-02).
    cursor = fact.computation_cursor
    try:
        resolved = resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile=profile,
            input_contract_ref=cursor.input_contract_ref,
            stream_registry_version=cursor.stream_registry_version,
            repo_root=repo_root,
        )
    except UnresolvedComputationCursorAuthorityError as exc:
        raise ReplayPreparationArtifactUnresolvableError(
            f"could not resolve the exact historical Input Contract/Stream Registry version-snapshot for profile "
            f"{profile!r} named by this fact's computation_cursor: {exc}"
        ) from exc

    # Failure class 2: malformed/missing evidence.
    evidence = fact.computation_dependency_content_evidence
    if evidence is None:
        raise ReplayPreparationEvidenceMalformedError(
            "fact.computation_dependency_content_evidence is missing — Replay preparation cannot proceed without it"
        )
    if not _is_well_formed_content_id(evidence.input_contract_content_id):
        raise ReplayPreparationEvidenceMalformedError(
            f"fact.computation_dependency_content_evidence.input_contract_content_id="
            f"{evidence.input_contract_content_id!r} is not a well-formed content-identity digest "
            "(64 lowercase hex characters)"
        )
    if not _is_well_formed_content_id(evidence.stream_registry_content_id):
        raise ReplayPreparationEvidenceMalformedError(
            f"fact.computation_dependency_content_evidence.stream_registry_content_id="
            f"{evidence.stream_registry_content_id!r} is not a well-formed content-identity digest "
            "(64 lowercase hex characters)"
        )

    # Failure class 4: content-ID mismatch.
    if resolved.input_contract_content_id != evidence.input_contract_content_id:
        raise ReplayPreparationContentIdentityMismatchError(
            f"the Input Contract artifact's recomputed content identity {resolved.input_contract_content_id!r} "
            f"does not match this fact's own persisted evidence {evidence.input_contract_content_id!r} — the "
            "artifact's own bytes changed since this fact was computed"
        )
    if resolved.stream_registry_content_id != evidence.stream_registry_content_id:
        raise ReplayPreparationContentIdentityMismatchError(
            f"the Stream Registry artifact's recomputed content identity {resolved.stream_registry_content_id!r} "
            f"does not match this fact's own persisted evidence {evidence.stream_registry_content_id!r} — the "
            "artifact's own bytes changed since this fact was computed"
        )
