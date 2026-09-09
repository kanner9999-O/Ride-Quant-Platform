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

Fails closed for each of ADR-037's four failure classes:

1. missing/unresolvable Input Contract or Stream Registry artifact —
   `ReplayPreparationArtifactUnresolvableError`;
2. malformed/missing `computation_dependency_content_evidence` —
   `ReplayPreparationEvidenceMalformedError`;
3. the currently-resolved artifact's own identity does not match the
   fact's own `computation_cursor.input_contract_ref`/`stream_registry_version`
   (cursor/reference relational mismatch) —
   `ReplayPreparationCursorReferenceMismatchError`;
4. the currently-resolved artifact's own recomputed content-identity digest
   does not match the fact's own persisted evidence (content-ID mismatch) —
   `ReplayPreparationContentIdentityMismatchError`.
"""

from __future__ import annotations

import re
from pathlib import Path

from .authority_resolver import resolve_input_contract_authority_from_repository
from .contracts import FeatureComputationProfile, FeatureComputed, FeatureFactInvalidated
from .errors import (
    ReplayPreparationArtifactUnresolvableError,
    ReplayPreparationContentIdentityMismatchError,
    ReplayPreparationCursorReferenceMismatchError,
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
    """Resolves the exact Input Contract + Stream Registry named by
    `fact.computation_cursor`, recomputes content identities from the
    actual, current artifact bytes, and compares against
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

    # Failure class 1: missing/unresolvable artifact.
    try:
        resolved = resolve_input_contract_authority_from_repository(profile, repo_root=repo_root)
    except UnresolvedComputationCursorAuthorityError as exc:
        raise ReplayPreparationArtifactUnresolvableError(
            f"could not resolve the Input Contract/Stream Registry artifact for profile {profile!r} named by "
            f"this fact's computation_cursor: {exc}"
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

    # Failure class 3: cursor/reference relational mismatch.
    cursor = fact.computation_cursor
    if resolved.input_contract_ref != cursor.input_contract_ref:
        raise ReplayPreparationCursorReferenceMismatchError(
            f"the currently-resolved Input Contract identity {resolved.input_contract_ref!r} does not match this "
            f"fact's own computation_cursor.input_contract_ref {cursor.input_contract_ref!r} — the artifact has "
            "evolved (or this fact's cursor is otherwise stale/incorrect) since this fact was computed"
        )
    if resolved.stream_registry_version != cursor.stream_registry_version:
        raise ReplayPreparationCursorReferenceMismatchError(
            f"the currently-resolved Stream Registry version {resolved.stream_registry_version!r} does not match "
            f"this fact's own computation_cursor.stream_registry_version {cursor.stream_registry_version!r} — the "
            "artifact has evolved (or this fact's cursor is otherwise stale/incorrect) since this fact was computed"
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
