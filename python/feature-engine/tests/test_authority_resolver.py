from __future__ import annotations

from pathlib import Path

import pytest

from feature_engine import InputContractRef, VerifiedInputContractAuthority
from feature_engine.authority_resolver import resolve_input_contract_authority_from_repository
from feature_engine.errors import UnresolvedComputationCursorAuthorityError

_DEFAULT_SWING_INCLUDED_STREAMS = ("market-data-ingestion-candle", "structure-engine-swing")
_DEFAULT_REGISTRY_STREAM_IDS = (
    "market-data-ingestion-candle",
    "structure-engine-swing",
    "structure-engine-structure",
    "raw-regime-engine-regime",
    "feature-engine-feature",
    "platform-lifecycle",
    "platform-audit",
)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _write_fake_repo(
    tmp_path: Path,
    *,
    contract_version: str = "v1",
    contract_stream_registry_version: str = "v1",
    swing_included_streams: tuple[str, ...] = _DEFAULT_SWING_INCLUDED_STREAMS,
    registry_version: str = "v1",
    registry_stream_ids: tuple[str, ...] = _DEFAULT_REGISTRY_STREAM_IDS,
) -> Path:
    """A minimal, TEMPORARY, fabricated repository tree mirroring just enough
    of the real Input Contract / Stream Registry YAML shape for
    `resolve_input_contract_authority_from_repository`'s line scanner to
    parse — never touches the actual authoritative docs.
    """
    _write(tmp_path / "docs" / "MARKER.md", "marker file, only used to anchor repo-root discovery")

    included_block = "\n".join(f"  - {stream_id}" for stream_id in swing_included_streams)
    contract_yaml = f"""# TEST FIXTURE ONLY -- not a real Input Contract artifact.
schema_version: 1
version: "0.4"
status: Draft
owner: Product Owner

input_contract_ref:
  contract_id: feature-swing-distance-input
  contract_version: {contract_version}

stream_registry_version: {contract_stream_registry_version}

included_streams:
{included_block}

merge_policy:
  algorithm: deterministic-causal-topological-order
"""
    _write(tmp_path / "docs/architecture/input-contracts/feature-swing-distance-input.yaml", contract_yaml)

    streams_block = "\n".join(
        f"  - stream_id: {stream_id}\n    status: active\n    sequence_policy: contiguous\n    genesis_position: 0"
        for stream_id in registry_stream_ids
    )
    registry_yaml = f"""# TEST FIXTURE ONLY -- not the real Genesis Stream Registry artifact.
schema_version: 1
registry_id: genesis-stream-registry
version: "0.1"
status: Approved

registry_version: {registry_version}

streams:
{streams_block}
"""
    _write(tmp_path / "docs/architecture/stream-registry.yaml", registry_yaml)
    return tmp_path


# --- Positive resolution: the real, current repository artifacts -----------


def test_real_swing_distance_authority_resolves_successfully() -> None:
    resolved = resolve_input_contract_authority_from_repository("distance_to_last_confirmed_swing")
    assert isinstance(resolved, VerifiedInputContractAuthority)
    assert resolved.input_contract_ref == InputContractRef("feature-swing-distance-input", "v1")
    assert resolved.stream_registry_version == "v1"
    assert resolved.included_streams == frozenset({"market-data-ingestion-candle", "structure-engine-swing"})
    assert len(resolved.input_contract_content_id) == 64
    assert len(resolved.stream_registry_content_id) == 64


def test_real_regime_authority_resolves_successfully() -> None:
    resolved = resolve_input_contract_authority_from_repository("regime")
    assert isinstance(resolved, VerifiedInputContractAuthority)
    assert resolved.input_contract_ref == InputContractRef("feature-regime-input", "v1")
    assert resolved.stream_registry_version == "v1"
    assert resolved.included_streams == frozenset({"raw-regime-engine-regime"})
    assert len(resolved.input_contract_content_id) == 64
    assert len(resolved.stream_registry_content_id) == 64


def test_both_real_profiles_share_the_same_registry_content_identity() -> None:
    """Both profiles are resolved against the SAME real Genesis Stream
    Registry artifact — their `stream_registry_content_id`s must match even
    though their own `input_contract_content_id`s (different files) differ.
    """
    swing = resolve_input_contract_authority_from_repository("distance_to_last_confirmed_swing")
    regime = resolve_input_contract_authority_from_repository("regime")
    assert swing.stream_registry_content_id == regime.stream_registry_content_id
    assert swing.input_contract_content_id != regime.input_contract_content_id


# --- Residual A: cross-artifact registry_version / included_streams checks -


def test_registry_version_mismatch_fails_closed(tmp_path: Path) -> None:
    """Input Contract claims `stream_registry_version: v1` but the resolved
    Stream Registry artifact itself declares `registry_version: v2` — an
    authority-resolution failure, never silently rebased.
    """
    repo = _write_fake_repo(tmp_path, contract_stream_registry_version="v1", registry_version="v2")
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_input_contract_authority_from_repository("distance_to_last_confirmed_swing", repo_root=repo)


def test_included_stream_absent_from_registry_fails_closed(tmp_path: Path) -> None:
    """`included_streams` containing a stream_id the resolved Stream
    Registry does not itself declare must fail closed.
    """
    repo = _write_fake_repo(
        tmp_path,
        swing_included_streams=(
            "market-data-ingestion-candle",
            "structure-engine-swing",
            "not-a-real-stream",
        ),
    )
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_input_contract_authority_from_repository("distance_to_last_confirmed_swing", repo_root=repo)


def test_matching_registry_version_and_streams_resolves_successfully(tmp_path: Path) -> None:
    """Sanity control: the SAME fixture-generation path, with no deliberate
    mismatch, resolves cleanly — proving the two failure tests above fail
    for the SPECIFIC reason under test, not fixture malformation.
    """
    repo = _write_fake_repo(tmp_path)
    resolved = resolve_input_contract_authority_from_repository("distance_to_last_confirmed_swing", repo_root=repo)
    assert resolved.stream_registry_version == "v1"
    assert resolved.included_streams == frozenset(_DEFAULT_SWING_INCLUDED_STREAMS)


# --- contract_id/contract_version resolved from the actual artifact --------


def test_contract_identity_resolved_from_actual_artifact_not_caller_substituted(tmp_path: Path) -> None:
    """`contract_id`/`contract_version` come from whatever the artifact
    itself currently says — changing the artifact's own content changes
    what is resolved; there is no caller-side override path at all.
    """
    repo = _write_fake_repo(tmp_path, contract_version="v1")
    resolved = resolve_input_contract_authority_from_repository("distance_to_last_confirmed_swing", repo_root=repo)
    assert resolved.input_contract_ref.contract_id == "feature-swing-distance-input"
    assert resolved.input_contract_ref.contract_version == "v1"

    contract_path = repo / "docs/architecture/input-contracts/feature-swing-distance-input.yaml"
    contract_path.write_text(contract_path.read_text().replace("contract_version: v1", "contract_version: v2"))

    resolved_after = resolve_input_contract_authority_from_repository(
        "distance_to_last_confirmed_swing", repo_root=repo
    )
    assert resolved_after.input_contract_ref.contract_version == "v2"
    assert resolved_after.input_contract_content_id != resolved.input_contract_content_id


# --- content identity changes when the underlying artifact bytes change ----


def test_content_identity_changes_when_artifact_bytes_change(tmp_path: Path) -> None:
    repo = _write_fake_repo(tmp_path)
    before = resolve_input_contract_authority_from_repository("distance_to_last_confirmed_swing", repo_root=repo)

    registry_path = repo / "docs/architecture/stream-registry.yaml"
    registry_path.write_text(registry_path.read_text() + "\n# a harmless trailing comment, changes the bytes only\n")

    after = resolve_input_contract_authority_from_repository("distance_to_last_confirmed_swing", repo_root=repo)
    assert after.stream_registry_content_id != before.stream_registry_content_id
    # The Input Contract artifact itself was untouched -- its own content identity is stable.
    assert after.input_contract_content_id == before.input_contract_content_id


def test_content_identity_stable_when_artifact_bytes_unchanged(tmp_path: Path) -> None:
    repo = _write_fake_repo(tmp_path)
    first = resolve_input_contract_authority_from_repository("distance_to_last_confirmed_swing", repo_root=repo)
    second = resolve_input_contract_authority_from_repository("distance_to_last_confirmed_swing", repo_root=repo)
    assert first.input_contract_content_id == second.input_contract_content_id
    assert first.stream_registry_content_id == second.stream_registry_content_id


# --- missing artifacts still fail closed (preserved from round 2) ----------


def test_missing_input_contract_artifact_fails_closed(tmp_path: Path) -> None:
    _write(tmp_path / "docs" / "MARKER.md", "marker")
    _write(tmp_path / "docs/architecture/stream-registry.yaml", "registry_version: v1\nstreams:\n")
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_input_contract_authority_from_repository("distance_to_last_confirmed_swing", repo_root=tmp_path)


def test_missing_stream_registry_artifact_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_repo(tmp_path)
    (repo / "docs/architecture/stream-registry.yaml").unlink()
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_input_contract_authority_from_repository("distance_to_last_confirmed_swing", repo_root=repo)
