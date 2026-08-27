"""Filesystem-backed Feature-scoped Input Contract authority resolver.

This module is explicitly OUTSIDE the Feature analytical core —
`contracts.py`/`swing_distance.py`/`regime_passthrough.py`/`candle_window.py`/
`current_view.py` never import it, and never perform filesystem I/O
themselves (Review-A round-2 residual 1's own "the analytical engine itself
does NOT need filesystem/GitHub access" framing). It is the "repository/
configuration adapter" a caller/orchestrator uses to actually resolve
`docs/architecture/input-contracts/feature-*.yaml` +
`docs/architecture/stream-registry.yaml` into a genuine, content-identity-
bearing, CROSS-ARTIFACT-VALIDATED `VerifiedInputContractAuthority` that a
computation engine then accepts via dependency injection
(`resolve_input_contract_authority`, `contracts.py`, re-validates STRUCTURE/
content-identity FORMAT only — it never re-reads or duplicates these
artifacts).

Deliberately dependency-free (no PyYAML) — this package pins zero runtime
dependencies (`pyproject.toml`). A minimal, explicit line scanner extracts
exactly the fields Chapter 8 §8.3.4/§8.3.1 require:
- from the Input Contract: `input_contract_ref.contract_id`/`contract_version`,
  `stream_registry_version`, `included_streams`;
- from the Stream Registry: `registry_version`, the full set of declared
  `stream_id` entries.

A SHA-256 of each artifact's own complete file bytes serves as that
artifact's verifiable content identity (Chapter 8 §8.1.1's "verifiable by
content identity" clause). Review-A round-3 residual A: this resolver does
NOT merely hash the Stream Registry's bytes and stop there — it additionally
proves, fail-closed, that the Input Contract's own claimed
`stream_registry_version` EXACTLY equals the resolved Registry's own
`registry_version` (never silently rebased onto a different registry
version), and that every one of the Input Contract's `included_streams` is
genuinely declared by that exact resolved Registry artifact (never a stream
the Input Contract merely assumes exists).

Artifact-state discipline: the Input Contract YAML files themselves remain
`status: Draft` (not Approved/Locked) even though the Feature Input
Contract/Frontier *package* is `Consolidated Stable` — package lifecycle and
artifact-level approval are distinct dimensions (Chapter 0 §7.1). This
resolver reads whatever content currently exists at these paths; it does not
assert, upgrade, or rely on any particular artifact-level status.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from .contracts import (
    FeatureComputationProfile,
    InputContractRef,
    VerifiedInputContractAuthority,
    resolve_input_contract_authority,
)
from .contracts import ResolvedInputContract as _ResolvedInputContractCandidate
from .errors import UnresolvedComputationCursorAuthorityError

_REPO_ROOT_MARKER = "docs"

_INPUT_CONTRACT_RELPATHS: dict[FeatureComputationProfile, str] = {
    "distance_to_last_confirmed_swing": "docs/architecture/input-contracts/feature-swing-distance-input.yaml",
    "regime": "docs/architecture/input-contracts/feature-regime-input.yaml",
}
_STREAM_REGISTRY_RELPATH = "docs/architecture/stream-registry.yaml"


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / _REPO_ROOT_MARKER).is_dir():
            return candidate
    raise UnresolvedComputationCursorAuthorityError(
        f"could not locate repository root (no {_REPO_ROOT_MARKER!r} directory found above {start!r}) — "
        "Input Contract/Stream Registry authority cannot be resolved from the filesystem"
    )


def _extract_scalar(lines: list[str], key: str) -> str | None:
    prefix = f"{key}:"
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped[len(prefix) :].strip().strip('"')
    return None


def _extract_included_streams(lines: list[str]) -> frozenset[str]:
    streams: list[str] = []
    in_block = False
    for line in lines:
        stripped = line.strip()
        if stripped == "included_streams:":
            in_block = True
            continue
        if in_block:
            if stripped.startswith("- "):
                streams.append(stripped[2:].strip())
                continue
            break
    return frozenset(streams)


def _extract_registry_stream_ids(lines: list[str]) -> frozenset[str]:
    """Every `stream_id:` declared as a `streams:` list entry in the Genesis
    Stream Registry — the exact set of logical streams that registry
    artifact actually declares (Review-A round-3 residual A).
    """
    prefix = "- stream_id:"
    stream_ids: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(prefix):
            stream_ids.append(stripped[len(prefix) :].strip())
    return frozenset(stream_ids)


def resolve_input_contract_authority_from_repository(
    profile: FeatureComputationProfile, *, repo_root: Path | None = None
) -> VerifiedInputContractAuthority:
    """Reads the actual, current Feature-scoped Input Contract YAML and the
    actual, current Stream Registry YAML off disk, resolves the SEMANTIC
    relationship between them (Review-A round-3 residual A — not merely
    their bytes), and returns a `VerifiedInputContractAuthority` carrying
    genuine, verifiable content-identity proof for both artifacts. This is
    the "verified factory"/"repository adapter" the Feature analytical core
    itself never performs; callers/orchestrators (and this repository's own
    test fixtures) use this — or an equivalent resolver — to obtain the
    object they inject into a computation engine.

    Fails closed (`UnresolvedComputationCursorAuthorityError`) if:
    - either artifact cannot be found;
    - the Input Contract does not resolve a complete `{contract_id,
      contract_version, stream_registry_version, included_streams}` identity;
    - the Stream Registry does not resolve a complete `{registry_version,
      stream_id set}` identity;
    - the Input Contract's own `stream_registry_version` does NOT exactly
      equal the resolved Registry's own `registry_version` — never silently
      rebased onto a different registry version, never resolved by picking
      a different registry to make the Input Contract fit;
    - any of the Input Contract's `included_streams` is NOT genuinely
      declared by that exact resolved Registry artifact.

    Never falls back to an invented value for any field.
    """
    root = repo_root if repo_root is not None else _find_repo_root(Path(__file__).resolve())
    contract_relpath = _INPUT_CONTRACT_RELPATHS[profile]
    contract_path = root / contract_relpath
    registry_path = root / _STREAM_REGISTRY_RELPATH
    if not contract_path.is_file():
        raise UnresolvedComputationCursorAuthorityError(
            f"Feature-scoped Input Contract artifact not found at {contract_path!r} — cannot resolve authority "
            f"for profile {profile!r}"
        )
    if not registry_path.is_file():
        raise UnresolvedComputationCursorAuthorityError(
            f"Stream Registry artifact not found at {registry_path!r} — cannot resolve authority"
        )
    contract_bytes = contract_path.read_bytes()
    registry_bytes = registry_path.read_bytes()
    contract_lines = contract_bytes.decode("utf-8").splitlines()
    registry_lines = registry_bytes.decode("utf-8").splitlines()

    contract_id = _extract_scalar(contract_lines, "contract_id")
    contract_version = _extract_scalar(contract_lines, "contract_version")
    stream_registry_version = _extract_scalar(contract_lines, "stream_registry_version")
    included_streams = _extract_included_streams(contract_lines)
    if not contract_id or not contract_version or not stream_registry_version or not included_streams:
        raise UnresolvedComputationCursorAuthorityError(
            f"Input Contract artifact at {contract_path!r} did not resolve a complete "
            "{contract_id, contract_version, stream_registry_version, included_streams} identity"
        )

    registry_version = _extract_scalar(registry_lines, "registry_version")
    registry_stream_ids = _extract_registry_stream_ids(registry_lines)
    if not registry_version or not registry_stream_ids:
        raise UnresolvedComputationCursorAuthorityError(
            f"Stream Registry artifact at {registry_path!r} did not resolve a complete "
            "{registry_version, stream_id set} identity"
        )

    # Registry <-> Contract semantic cross-validation (Review-A round-3 residual A) —
    # a hash of the Registry's own bytes alone does not prove the Input Contract
    # actually refers to THAT registry version or that its selected streams exist
    # there; this is a genuine authority-resolution failure, never silently
    # rewritten/rebased onto another registry version.
    if stream_registry_version != registry_version:
        raise UnresolvedComputationCursorAuthorityError(
            f"Input Contract at {contract_path!r} declares stream_registry_version={stream_registry_version!r}, "
            f"but the resolved Stream Registry at {registry_path!r} declares registry_version="
            f"{registry_version!r} — these must match exactly (Chapter 8 §8.5 Registry -> Contract exact-pin "
            "rule); authority-resolution failure, never resolved by selecting a different registry version"
        )
    unresolvable_streams = included_streams - registry_stream_ids
    if unresolvable_streams:
        raise UnresolvedComputationCursorAuthorityError(
            f"Input Contract at {contract_path!r} declares included_streams containing "
            f"{sorted(unresolvable_streams)!r}, which the resolved Stream Registry at {registry_path!r} "
            f"(registry_version={registry_version!r}) does not declare — an Input Contract may only reference "
            "streams that genuinely exist in its own pinned registry"
        )

    candidate = _ResolvedInputContractCandidate(
        feature_computation_profile=profile,
        input_contract_ref=InputContractRef(contract_id=contract_id, contract_version=contract_version),
        stream_registry_version=stream_registry_version,
        included_streams=included_streams,
        input_contract_content_id=hashlib.sha256(contract_bytes).hexdigest(),
        stream_registry_content_id=hashlib.sha256(registry_bytes).hexdigest(),
    )
    return resolve_input_contract_authority(candidate, required_profile=profile)
