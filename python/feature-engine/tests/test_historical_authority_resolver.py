"""`P3-FEATURE-EVID05B-IMPL-A-MAJ-02` remediation —
`resolve_historical_input_contract_authority_from_repository` (the
cursor-pinned, immutable ADR-041 version-snapshot resolver used exclusively
by Replay preparation, `replay_preparation.py`) — kept entirely separate
from `test_authority_resolver.py`, which covers the current/active-path
resolver (`resolve_input_contract_authority_from_repository`) that this
function is never a substitute for.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from conftest import REGIME_INPUT_CONTRACT

from feature_engine import InputContractRef, resolve_historical_input_contract_authority_from_repository
from feature_engine.contracts import VerifiedInputContractAuthority
from feature_engine.errors import UnresolvedComputationCursorAuthorityError

_DEFAULT_INCLUDED_STREAMS = ("raw-regime-engine-regime",)
_DEFAULT_REGISTRY_STREAM_IDS = (
    "raw-regime-engine-regime",
    "market-data-ingestion-candle",
    "platform-lifecycle",
)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _write_fake_snapshot_repo(
    tmp_path: Path,
    *,
    contract_id: str = "feature-regime-input",
    contract_version: str = "v1.0",
    contract_registry_ref: str = "v1.0",
    included_streams: tuple[str, ...] = _DEFAULT_INCLUDED_STREAMS,
    registry_version: str = "v1.0",
    registry_stream_ids: tuple[str, ...] = _DEFAULT_REGISTRY_STREAM_IDS,
    write_contract: bool = True,
    write_registry: bool = True,
) -> Path:
    """A minimal, TEMPORARY, fabricated repository tree mirroring just
    enough of the real ADR-041 canonical version-snapshot YAML shape for
    the historical resolver's line scanner to parse — never touches the
    actual authoritative docs.
    """
    _write(tmp_path / "docs" / "MARKER.md", "marker file, only used to anchor repo-root discovery")
    if write_contract:
        included_block = "\n".join(f"  - {s}" for s in included_streams)
        _write(
            tmp_path / f"docs/architecture/input-contract-versions/{contract_id}/{contract_version}.yaml",
            f"""# TEST FIXTURE ONLY -- not a real Input Contract version-snapshot.
schema_version: 1
version: "0.5"
status: Draft

input_contract_ref:
  contract_id: {contract_id}
  contract_version: {contract_version}

stream_registry_version: {contract_registry_ref}

included_streams:
{included_block}
""",
        )
    if write_registry:
        streams_block = "\n".join(f"  - stream_id: {s}\n    status: active" for s in registry_stream_ids)
        _write(
            tmp_path / f"docs/architecture/stream-registry-versions/{registry_version}.yaml",
            f"""# TEST FIXTURE ONLY -- not the real Genesis Stream Registry version-snapshot.
schema_version: 1
registry_id: genesis-stream-registry
version: "0.2"
status: Approved

registry_version: {registry_version}

streams:
{streams_block}
""",
        )
    return tmp_path


# --- Positive resolution: the real, currently-Published v1.0 snapshots -----


def test_real_published_snapshot_resolves_successfully() -> None:
    resolved = resolve_historical_input_contract_authority_from_repository(
        feature_computation_profile="regime",
        input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
        stream_registry_version="v1.0",
    )
    assert isinstance(resolved, VerifiedInputContractAuthority)
    assert resolved.feature_computation_profile == "regime"
    assert resolved.input_contract_ref == InputContractRef("feature-regime-input", "v1.0")
    assert resolved.stream_registry_version == "v1.0"
    assert resolved.included_streams == frozenset({"raw-regime-engine-regime"})
    assert len(resolved.input_contract_content_id) == 64
    assert len(resolved.stream_registry_content_id) == 64


def test_real_published_snapshot_matches_current_active_content_id() -> None:
    """The real v1.0 snapshot pair is byte-identical to the current/active
    artifacts at this exact publication boundary (ADR-041 exact-byte rule)
    — so their content identities also match, proving the historical
    resolver reads genuinely equivalent, real bytes, not a stand-in.
    """
    historical = resolve_historical_input_contract_authority_from_repository(
        feature_computation_profile="regime",
        input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
        stream_registry_version="v1.0",
    )
    assert historical.input_contract_content_id == REGIME_INPUT_CONTRACT.input_contract_content_id
    assert historical.stream_registry_content_id == REGIME_INPUT_CONTRACT.stream_registry_content_id


# --- Canonical path resolution / no fallback (ADR-041) ----------------------


def test_matching_synthetic_snapshot_resolves_successfully(tmp_path: Path) -> None:
    """Sanity control: the SAME fixture-generation path, with no deliberate
    defect, resolves cleanly — proving the failure tests below fail for the
    SPECIFIC reason under test, not fixture malformation.
    """
    repo = _write_fake_snapshot_repo(tmp_path)
    resolved = resolve_historical_input_contract_authority_from_repository(
        feature_computation_profile="regime",
        input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
        stream_registry_version="v1.0",
        repo_root=repo,
    )
    assert resolved.included_streams == frozenset(_DEFAULT_INCLUDED_STREAMS)


def test_missing_input_contract_snapshot_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_snapshot_repo(tmp_path, write_contract=False)
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
            stream_registry_version="v1.0",
            repo_root=repo,
        )


def test_missing_stream_registry_snapshot_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_snapshot_repo(tmp_path, write_registry=False)
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
            stream_registry_version="v1.0",
            repo_root=repo,
        )


def test_no_fallback_to_a_different_existing_version(tmp_path: Path) -> None:
    """Only `v1.0` snapshots exist; requesting `v2.0` must never silently
    resolve the nearest/only existing version instead.
    """
    repo = _write_fake_snapshot_repo(tmp_path)
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef("feature-regime-input", "v2.0"),
            stream_registry_version="v1.0",
            repo_root=repo,
        )


# --- Malformed version-token grammar (never construct an unvalidated path) --


@pytest.mark.parametrize(
    "bad_contract_version",
    ["v1", "1.0", "v1.0.0", "v01.0", "v1.00", "../../../etc/passwd", "v1.0/../../x", ""],
)
def test_malformed_contract_version_token_fails_closed(tmp_path: Path, bad_contract_version: str) -> None:
    repo = _write_fake_snapshot_repo(tmp_path)
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef("feature-regime-input", bad_contract_version),
            stream_registry_version="v1.0",
            repo_root=repo,
        )


@pytest.mark.parametrize("bad_registry_version", ["v1", "1.0", "v1.0.0", "../../../etc/passwd", ""])
def test_malformed_stream_registry_version_token_fails_closed(tmp_path: Path, bad_registry_version: str) -> None:
    repo = _write_fake_snapshot_repo(tmp_path)
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
            stream_registry_version=bad_registry_version,
            repo_root=repo,
        )


@pytest.mark.parametrize("bad_contract_id", ["../etc/passwd", "Feature-Regime-Input", "feature/regime", ""])
def test_malformed_contract_id_fails_closed(tmp_path: Path, bad_contract_id: str) -> None:
    repo = _write_fake_snapshot_repo(tmp_path)
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef(bad_contract_id, "v1.0"),
            stream_registry_version="v1.0",
            repo_root=repo,
        )


# --- Self-identity consistency (snapshot content vs. its own canonical path)


def test_contract_snapshot_wrong_contract_id_inside_content_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_snapshot_repo(tmp_path, contract_id="feature-regime-input", contract_version="v1.0")
    path = repo / "docs/architecture/input-contract-versions/feature-regime-input/v1.0.yaml"
    path.write_text(path.read_text().replace("contract_id: feature-regime-input", "contract_id: feature-candle-input"))
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
            stream_registry_version="v1.0",
            repo_root=repo,
        )


def test_contract_snapshot_wrong_contract_version_inside_content_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_snapshot_repo(tmp_path)
    path = repo / "docs/architecture/input-contract-versions/feature-regime-input/v1.0.yaml"
    path.write_text(path.read_text().replace("contract_version: v1.0", "contract_version: v2.0"))
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
            stream_registry_version="v1.0",
            repo_root=repo,
        )


def test_registry_snapshot_wrong_registry_version_inside_content_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_snapshot_repo(tmp_path)
    path = repo / "docs/architecture/stream-registry-versions/v1.0.yaml"
    path.write_text(path.read_text().replace("registry_version: v1.0", "registry_version: v2.0"))
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
            stream_registry_version="v1.0",
            repo_root=repo,
        )


# --- Input Contract <-> Stream Registry relational mismatch (WITHIN the ----
# --- pinned snapshot pair, distinct from self-identity mismatch above) -----


def test_relational_mismatch_between_pinned_snapshots_fails_closed(tmp_path: Path) -> None:
    """The Input Contract snapshot's OWN claimed `stream_registry_version`
    disagrees with the Stream Registry snapshot actually resolved at the
    cursor's pinned `stream_registry_version` — a genuine cross-artifact
    inconsistency, never resolved by silently pairing with a different
    registry snapshot.
    """
    repo = _write_fake_snapshot_repo(tmp_path, contract_registry_ref="v9.0", registry_version="v1.0")
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
            stream_registry_version="v1.0",
            repo_root=repo,
        )


def test_included_stream_absent_from_pinned_registry_snapshot_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_snapshot_repo(
        tmp_path,
        included_streams=("raw-regime-engine-regime", "not-a-real-stream"),
    )
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
            stream_registry_version="v1.0",
            repo_root=repo,
        )


# --- Malformed snapshot content ----------------------------------------------


def test_missing_contract_id_field_in_snapshot_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_snapshot_repo(tmp_path)
    path = repo / "docs/architecture/input-contract-versions/feature-regime-input/v1.0.yaml"
    path.write_text(path.read_text().replace("  contract_id: feature-regime-input\n", ""))
    with pytest.raises(UnresolvedComputationCursorAuthorityError, match="did not resolve a complete"):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
            stream_registry_version="v1.0",
            repo_root=repo,
        )


# --- P3-FEATURE-EVID05B-IMPL-A-MAJ-03: profile <-> contract-lineage -------
# --- binding must be preserved by historical resolution too ---------------


def test_regime_profile_rejects_swing_distance_contract_lineage() -> None:
    """A `"regime"` profile pinned (via a corrupted/forged cursor) to the
    REAL, genuinely-Published `feature-swing-distance-input` v1.0 snapshot
    must fail closed — even though that snapshot and its paired Registry
    snapshot both genuinely resolve on their own, "regime" is never
    authorized to bind that lineage.
    """
    with pytest.raises(UnresolvedComputationCursorAuthorityError, match="not the Input Contract lineage authorized"):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef("feature-swing-distance-input", "v1.0"),
            stream_registry_version="v1.0",
        )


def test_distance_profile_rejects_regime_contract_lineage() -> None:
    """Converse of the above, for symmetry: `"distance_to_last_confirmed_
    swing"` may not bind the `feature-regime-input` lineage either.
    """
    with pytest.raises(UnresolvedComputationCursorAuthorityError, match="not the Input Contract lineage authorized"):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="distance_to_last_confirmed_swing",
            input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
            stream_registry_version="v1.0",
        )


def test_unknown_profile_fails_closed_even_with_a_genuinely_valid_snapshot() -> None:
    """An arbitrary/unsupported `feature_computation_profile` string must
    never be accepted merely because the paired `input_contract_ref`/
    `stream_registry_version` happen to name a real, valid snapshot.
    """
    with pytest.raises(UnresolvedComputationCursorAuthorityError, match="not a known Feature computation profile"):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="not-a-real-profile",  # type: ignore[arg-type]
            input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
            stream_registry_version="v1.0",
        )


def test_profile_binding_checked_before_any_filesystem_access(tmp_path: Path) -> None:
    """The profile <-> contract-lineage mismatch is rejected even against a
    `repo_root` containing NO snapshots at all — proving the check happens
    before path construction/filesystem access, not as a side effect of a
    failed snapshot lookup.
    """
    (tmp_path / "docs").mkdir()
    with pytest.raises(UnresolvedComputationCursorAuthorityError, match="not the Input Contract lineage authorized"):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef("feature-swing-distance-input", "v1.0"),
            stream_registry_version="v1.0",
            repo_root=tmp_path,
        )


def test_missing_registry_version_field_in_snapshot_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_snapshot_repo(tmp_path)
    path = repo / "docs/architecture/stream-registry-versions/v1.0.yaml"
    path.write_text(path.read_text().replace("registry_version: v1.0\n", ""))
    with pytest.raises(UnresolvedComputationCursorAuthorityError, match="did not resolve a complete"):
        resolve_historical_input_contract_authority_from_repository(
            feature_computation_profile="regime",
            input_contract_ref=InputContractRef("feature-regime-input", "v1.0"),
            stream_registry_version="v1.0",
            repo_root=repo,
        )
