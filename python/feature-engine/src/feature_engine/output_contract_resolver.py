"""Filesystem-backed Feature outbound Event Contract authority resolver
(ADR-039, Approved; ADR-040, Approved).

This module is explicitly OUTSIDE the Feature analytical core —
`contracts.py`/`swing_distance.py`/`regime_passthrough.py`/`candle_window.py`
never import it, and never perform filesystem I/O themselves. It is the
"repository/configuration adapter" a caller/orchestrator uses to actually
resolve `docs/architecture/event-contracts/<contract_id>/<contract_version>.yaml`
into a genuine `VerifiedOutputEventContractAuthority` — exactly the same role
`authority_resolver.py` plays for Feature-scoped Input Contract authority.

Resolution is ADR-039's own deterministic, direct path function — pure
literal substitution of `{contract_id}`/`{contract_version}` into
`docs/architecture/event-contracts/<contract_id>/<contract_version>.yaml` —
never an alias, a git-history search, a registry, or any other lookup
mechanism (ADR-039 §"Canonical path/version grammar"; ADR-040's own
Class G within-horizon commitment: the canonical path is the ONLY resolver,
git history is content-identity/audit evidence only). A resolved artifact's
own `contract_id`/`contract_version`/`status` fields are read back and
cross-checked against the exact identity the path was constructed from —
never assumed merely because the path resolved.

`status: Published` is a hard requirement (ADR-039 §"Immutability and
identifier non-reuse"): a `Draft` (or any other non-Published) artifact is
never a usable `event_contract_ref` target for a real, persisted
authoritative event — resolution fails closed instead.

Deliberately dependency-free (no PyYAML), same minimal line-scanner
discipline as `authority_resolver.py`.

`P3-FEATURE-EVID05B-IMPL-A-MAJ-01` remediation: `feature-computed` and
`feature-fact-invalidated` are independently versioned Event Contract
lineages (ADR-039's own authority is exactly `{contract_id, contract_version}`
per artifact) — this resolver no longer accepts one shared `contract_version`
applied to both; each lineage's exact version is a separate, independently
pinned input.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .contracts import (
    FEATURE_COMPUTED_CONTRACT_ID,
    FEATURE_FACT_INVALIDATED_CONTRACT_ID,
    VerifiedOutputEventContractAuthority,
    _seal_verified_output_authority,
)
from .envelope import EventContractRef
from .errors import (
    OutputEventContractIdentityMismatchError,
    OutputEventContractNotPublishedError,
    OutputEventContractUnresolvableError,
    OutputStreamEligibilityError,
)

_REPO_ROOT_MARKER = "docs"
_EVENT_CONTRACTS_RELDIR = "docs/architecture/event-contracts"
_PUBLISHED_STATUS = "Published"


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / _REPO_ROOT_MARKER).is_dir():
            return candidate
    raise OutputEventContractUnresolvableError(
        f"could not locate repository root (no {_REPO_ROOT_MARKER!r} directory found above {start!r}) — "
        "outbound Event Contract authority cannot be resolved from the filesystem"
    )


def _extract_scalar(lines: list[str], key: str) -> str | None:
    prefix = f"{key}:"
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped[len(prefix) :].strip().strip('"')
    return None


def _extract_allowed_streams(lines: list[str]) -> tuple[str, ...]:
    """Parses the Event Contract artifact's own `allowed_streams: [{-
    stream_id: ...}]` block (Chapter 8 §8.3.1: "eligibility khai báo MỘT
    CHIỀU tại Event Contract") — a bounded block scanner, same dependency-
    free discipline as `authority_resolver.py`'s `_extract_included_streams`
    (no PyYAML). Terminates the block on the first line that is not a
    matching `- stream_id: ...` entry (e.g. a following comment or the next
    top-level key) — mirrors that same scanner's own termination rule.
    """
    prefix = "- stream_id:"
    streams: list[str] = []
    in_block = False
    for line in lines:
        stripped = line.strip()
        if stripped == "allowed_streams:":
            in_block = True
            continue
        if in_block:
            if stripped.startswith(prefix):
                streams.append(stripped[len(prefix) :].strip())
                continue
            break
    return tuple(streams)


def _resolve_one(contract_id: str, contract_version: str, *, root: Path) -> tuple[EventContractRef, tuple[str, ...]]:
    """ADR-039's own deterministic path function — pure literal
    substitution, no alias/normalization/case-folding, no history search.
    Reads the resolved artifact's own `contract_id`/`contract_version`/
    `status` back and fails closed on any missing field, identity mismatch,
    or non-`Published` status. Also returns the artifact's own resolver-
    parsed `allowed_streams` (ADR043-IMPL-A-MAJ-03) — unvalidated here; the
    caller cross-validates against the paired contract's own resolved
    `allowed_streams`.
    """
    path = root / _EVENT_CONTRACTS_RELDIR / contract_id / f"{contract_version}.yaml"
    if not path.is_file():
        raise OutputEventContractUnresolvableError(
            f"Event Contract version-artifact not found at its own canonical path {path!r} "
            f"(contract_id={contract_id!r}, contract_version={contract_version!r}) — no alias/history-search/"
            "registry fallback exists (ADR-039)"
        )
    lines = path.read_bytes().decode("utf-8").splitlines()
    resolved_contract_id = _extract_scalar(lines, "contract_id")
    resolved_contract_version = _extract_scalar(lines, "contract_version")
    resolved_status = _extract_scalar(lines, "status")
    if not resolved_contract_id or not resolved_contract_version or not resolved_status:
        raise OutputEventContractUnresolvableError(
            f"Event Contract version-artifact at {path!r} did not resolve a complete "
            "{contract_id, contract_version, status} identity"
        )
    if resolved_contract_id != contract_id or resolved_contract_version != contract_version:
        raise OutputEventContractIdentityMismatchError(
            f"Event Contract version-artifact at {path!r} declares "
            f"contract_id={resolved_contract_id!r}/contract_version={resolved_contract_version!r}, which does not "
            f"exactly match its own canonical path identity {contract_id!r}/{contract_version!r} — an artifact "
            "must self-identify consistently with its own canonical location"
        )
    if resolved_status != _PUBLISHED_STATUS:
        raise OutputEventContractNotPublishedError(
            f"Event Contract version-artifact at {path!r} has status={resolved_status!r}, not "
            f"{_PUBLISHED_STATUS!r} — a non-Published artifact is never a usable event_contract_ref target "
            "(ADR-039/ADR-040)"
        )
    allowed_streams = _extract_allowed_streams(lines)
    ref = EventContractRef(contract_id=resolved_contract_id, contract_version=resolved_contract_version)
    return ref, allowed_streams


def _resolve_authoritative_stream(
    computed_ref: EventContractRef,
    computed_streams: tuple[str, ...],
    invalidated_ref: EventContractRef,
    invalidated_streams: tuple[str, ...],
) -> str:
    """ADR043-IMPL-A-MAJ-03: the one, resolver-proven, mutually-agreeing
    authoritative Feature output stream identity — never hard-coded, never
    caller-chosen. Fails closed (`OutputStreamEligibilityError`) if either
    contract's own `allowed_streams` is missing/empty, names more than one
    stream (this implementation has no deterministic selection rule for
    that case), or the two contracts disagree.
    """
    if not computed_streams:
        raise OutputStreamEligibilityError(
            f"{computed_ref!r} does not declare a non-empty allowed_streams block — cannot resolve an "
            "authoritative Feature output stream"
        )
    if not invalidated_streams:
        raise OutputStreamEligibilityError(
            f"{invalidated_ref!r} does not declare a non-empty allowed_streams block — cannot resolve an "
            "authoritative Feature output stream"
        )
    if len(computed_streams) > 1:
        raise OutputStreamEligibilityError(
            f"{computed_ref!r} declares {len(computed_streams)} allowed_streams entries {computed_streams!r} — "
            "this implementation cannot deterministically select an authoritative stream among more than one"
        )
    if len(invalidated_streams) > 1:
        raise OutputStreamEligibilityError(
            f"{invalidated_ref!r} declares {len(invalidated_streams)} allowed_streams entries "
            f"{invalidated_streams!r} — this implementation cannot deterministically select an authoritative "
            "stream among more than one"
        )
    if computed_streams[0] != invalidated_streams[0]:
        raise OutputStreamEligibilityError(
            f"{computed_ref!r} allowed_streams={computed_streams!r} disagrees with {invalidated_ref!r} "
            f"allowed_streams={invalidated_streams!r} — both Feature output Event Contracts must resolve the "
            "SAME authoritative stream"
        )
    return computed_streams[0]


def resolve_output_event_contract_authority_from_repository(
    computed_contract_version: str, invalidated_contract_version: str, *, repo_root: Path | None = None
) -> VerifiedOutputEventContractAuthority:
    """Resolves `feature-computed` at `computed_contract_version` and
    `feature-fact-invalidated` at `invalidated_contract_version` —
    INDEPENDENTLY pinned exact `{contract_id, contract_version}` identities
    (ADR-039) — from their own canonical paths. The two lineages are never
    assumed to share a version: ADR-039's own authority is exactly
    `{contract_id, contract_version}` per artifact, and
    `VerifiedOutputEventContractAuthority` already carries
    `computed_contract_ref`/`invalidated_contract_ref` as two separate
    fields. This is the "verified factory"/"repository adapter" the Feature
    analytical core itself never performs; callers/orchestrators (and this
    repository's own test fixtures) use this — or an equivalent resolver —
    to obtain the object they inject into a computation engine.

    Fails closed (`OutputEventContractUnresolvableError`/
    `OutputEventContractIdentityMismatchError`/
    `OutputEventContractNotPublishedError`) if EITHER artifact,
    independently, is missing, malformed, self-identifies inconsistently
    with its own canonical path, or is not `status: Published` — a failure
    on one lineage never substitutes, defers to, or is silently masked by
    the other lineage's own resolution. Never falls back to an invented
    value, an older version, an alias, or any other artifact.
    """
    root = repo_root if repo_root is not None else _find_repo_root(Path(__file__).resolve())
    computed_ref, computed_streams = _resolve_one(FEATURE_COMPUTED_CONTRACT_ID, computed_contract_version, root=root)
    invalidated_ref, invalidated_streams = _resolve_one(
        FEATURE_FACT_INVALIDATED_CONTRACT_ID, invalidated_contract_version, root=root
    )
    authoritative_stream_id = _resolve_authoritative_stream(
        computed_ref, computed_streams, invalidated_ref, invalidated_streams
    )
    return _seal_verified_output_authority(
        computed_contract_ref=computed_ref,
        invalidated_contract_ref=invalidated_ref,
        authoritative_stream_id=authoritative_stream_id,
    )


@dataclass(frozen=True, slots=True)
class FilesystemOutputEventContractAuthorityResolver:
    """The default `OutputEventContractAuthorityProvider` (`contracts.py`)
    — every `.resolve()` call reads the real, `Published` Event Contract
    version-artifacts off disk and resolves fresh, genuinely-verified
    authority for the INDEPENDENTLY pinned `computed_contract_version`/
    `invalidated_contract_version`. Optionally pinned to a fixed
    `repo_root` (used by this repository's own tests to point at a
    temporary fixture tree).
    """

    computed_contract_version: str
    invalidated_contract_version: str
    repo_root: Path | None = None

    def resolve(self) -> VerifiedOutputEventContractAuthority:
        return resolve_output_event_contract_authority_from_repository(
            self.computed_contract_version, self.invalidated_contract_version, repo_root=self.repo_root
        )


@dataclass(frozen=True, slots=True)
class StaticOutputEventContractAuthorityProvider:
    """A trivial `OutputEventContractAuthorityProvider` (`contracts.py`)
    wrapping an ALREADY-resolved `VerifiedOutputEventContractAuthority` —
    useful for a caller (or this repository's own test fixtures) that
    resolved authority once, e.g. via
    `resolve_output_event_contract_authority_from_repository` at process/
    test-module start, and wants to inject a stable provider into multiple
    engine instances without repeating filesystem I/O on every
    construction.
    """

    authority: VerifiedOutputEventContractAuthority

    def resolve(self) -> VerifiedOutputEventContractAuthority:
        return self.authority
