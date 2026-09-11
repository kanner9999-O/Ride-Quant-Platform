"""ADR-037 Replay preparation (`P3-FEATURE-QG-EVID-05(b)`) — fail-closed
BEFORE Replay execution begins, for each of ADR-037's four failure classes.
Preserves `EVID-05(a)`: `prepare_replay_evidence` itself performs filesystem
I/O (it IS the Replay-preparation phase) — `test_replay_isolation.py`
separately proves Replay EXECUTION never calls it or any other
filesystem-touching function.
"""

from __future__ import annotations

import dataclasses
import shutil
from pathlib import Path

import pytest
from conftest import (
    OUTPUT_EVENT_CONTRACT_AUTHORITY,
    REGIME_INPUT_CONTRACT,
    SWING_DISTANCE_INPUT_CONTRACT,
    feature_scope,
    frontier_at,
    make_regime_definition,
    only_computed,
    regime_classified_at,
)

from feature_engine import (
    RegimePassthroughFeatureEngine,
    SequenceAllocator,
    StaticInputContractAuthorityProvider,
    StaticOutputEventContractAuthorityProvider,
    prepare_replay_evidence,
)
from feature_engine.contracts import ComputationDependencyContentEvidence, FeatureComputed, InputContractRef
from feature_engine.errors import (
    ReplayPreparationArtifactUnresolvableError,
    ReplayPreparationContentIdentityMismatchError,
    ReplayPreparationEvidenceMalformedError,
)

# tests/ -> feature-engine -> python -> repository root.
_REPO_ROOT = Path(__file__).resolve().parents[3]


def _real_regime_fact() -> FeatureComputed:
    allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="replay-prep-test")
    from conftest import FixedDeltaTimeSource

    definition = make_regime_definition(regime_dimension_version="rgd-1")
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    engine = RegimePassthroughFeatureEngine(
        scope,
        definition,
        allocator,
        FixedDeltaTimeSource(),
        output_event_contract_authority_provider=StaticOutputEventContractAuthorityProvider(
            OUTPUT_EVENT_CONTRACT_AUTHORITY
        ),
        input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
    )
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    events = engine.on_regime_classified(
        fact, cursor=frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    )
    return only_computed(events[0])


# --- Success path: real artifacts, real fact --------------------------------


def test_prepare_replay_evidence_succeeds_for_genuine_fact() -> None:
    computed = _real_regime_fact()
    prepare_replay_evidence(computed)  # succeeds silently (no exception) — no return value to assert on


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _copy_real_snapshot_only_repo(tmp_path: Path) -> Path:
    """A temp repo containing ONLY the real, already-Published ADR-041
    canonical `v1.0` snapshots for the "regime" profile — copied byte-for-
    byte from this actual repository — and deliberately no current/active
    mutable Input Contract/Stream Registry file at all, proving Replay
    preparation resolves the pinned snapshot alone and never needs (or
    consults) the current/active path.
    """
    _write(tmp_path / "docs" / "MARKER.md", "marker")
    src_contract = _REPO_ROOT / "docs/architecture/input-contract-versions/feature-regime-input/v1.0.yaml"
    src_registry = _REPO_ROOT / "docs/architecture/stream-registry-versions/v1.0.yaml"
    dst_contract = tmp_path / "docs/architecture/input-contract-versions/feature-regime-input/v1.0.yaml"
    dst_registry = tmp_path / "docs/architecture/stream-registry-versions/v1.0.yaml"
    dst_contract.parent.mkdir(parents=True, exist_ok=True)
    dst_registry.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src_contract, dst_contract)
    shutil.copyfile(src_registry, dst_registry)
    return tmp_path


# --- Failure class 1: missing/unresolvable artifact -------------------------


def test_missing_artifact_fails_closed(tmp_path: Path) -> None:
    """`repo_root` points at a tree with no Input Contract/Stream Registry
    artifacts at all — the fact itself is genuine, but the artifact its own
    cursor names cannot be resolved there.
    """
    computed = _real_regime_fact()
    (tmp_path / "docs").mkdir()
    with pytest.raises(ReplayPreparationArtifactUnresolvableError):
        prepare_replay_evidence(computed, repo_root=tmp_path)


def test_malformed_snapshot_fails_closed(tmp_path: Path) -> None:
    """The exact snapshot file exists at its own canonical cursor-pinned
    path but its content no longer resolves a complete identity — fails
    closed, never silently accepted.
    """
    computed = _real_regime_fact()
    repo = _copy_real_snapshot_only_repo(tmp_path)
    contract_path = repo / "docs/architecture/input-contract-versions/feature-regime-input/v1.0.yaml"
    contract_path.write_text(contract_path.read_text().replace("contract_id: feature-regime-input", ""))
    with pytest.raises(ReplayPreparationArtifactUnresolvableError):
        prepare_replay_evidence(computed, repo_root=repo)


# --- MAJ-02 required regression proof: snapshot-pinned, not current-path ----


def test_replay_preparation_uses_snapshot_when_no_current_file_exists(tmp_path: Path) -> None:
    """Proves Replay preparation resolves the cursor-pinned historical
    snapshot and succeeds even when NO current/active mutable Input
    Contract/Stream Registry file exists anywhere in the given `repo_root`
    — current/active resolution is never consulted, let alone required.
    """
    computed = _real_regime_fact()
    repo = _copy_real_snapshot_only_repo(tmp_path)
    prepare_replay_evidence(computed, repo_root=repo)


def test_replay_preparation_ignores_changed_current_file(tmp_path: Path) -> None:
    """Even when a DIFFERENT/corrupted current/active file is ALSO present
    at its normal mutable path alongside a valid pinned snapshot, Replay
    preparation is completely unaffected by it — proving no fallback to,
    or cross-check against, the current/active path occurs.
    """
    computed = _real_regime_fact()
    repo = _copy_real_snapshot_only_repo(tmp_path)
    _write(
        repo / "docs/architecture/input-contracts/feature-regime-input.yaml",
        "this file must never be read by Replay preparation\nstatus: Approved\ncontract_version: v99.0\n",
    )
    _write(
        repo / "docs/architecture/stream-registry.yaml",
        "this file must never be read by Replay preparation\nregistry_version: v99.0\n",
    )
    prepare_replay_evidence(computed, repo_root=repo)


def test_replay_preparation_unaffected_by_removed_current_file(tmp_path: Path) -> None:
    """A cursor-pinned snapshot that was valid when the fact was computed
    remains resolvable by Replay preparation even after the current/active
    mutable file it once mirrored has since been deleted entirely.
    """
    computed = _real_regime_fact()
    repo = _copy_real_snapshot_only_repo(tmp_path)
    # `_copy_real_snapshot_only_repo` never creates a current/active file in
    # the first place -- this test's own name asserts that absence is fine.
    assert not (repo / "docs/architecture/input-contracts").exists()
    assert not (repo / "docs/architecture/stream-registry.yaml").exists()
    prepare_replay_evidence(computed, repo_root=repo)


# --- P3-FEATURE-EVID05B-IMPL-A-MAJ-03: lost profile <-> contract-lineage ----
# --- invariant must still fail closed during Replay preparation -------------


def test_regime_fact_forged_onto_swing_snapshot_fails_closed() -> None:
    """A genuine `"regime"` fact whose cursor has been changed to point at
    the REAL, genuinely-valid `feature-swing-distance-input` v1.0 snapshot
    — with the persisted `input_contract_content_id` ALSO changed to that
    snapshot's own genuine digest, so a bare content-ID comparison would
    otherwise succeed, and the pinned `stream_registry_version` left at the
    real, compatible `v1.0` Registry snapshot both lineages share — must
    still fail closed. Proves the failure is specifically the lost
    profile <-> contract-lineage invariant (MAJ-03), not a missing snapshot
    (the Swing snapshot genuinely exists and resolves) and not a bare
    content-ID mismatch (the digest genuinely matches the snapshot named).
    """
    computed = _real_regime_fact()
    assert computed.scope.feature_type in ("volatility_metric", "directional_persistence_metric")

    forged_cursor = dataclasses.replace(
        computed.computation_cursor,
        input_contract_ref=InputContractRef(
            contract_id="feature-swing-distance-input",
            contract_version="v1.0",
        ),
        # stream_registry_version left unchanged: v1.0, genuinely shared by
        # both the Regime and Swing Input Contract lineages today.
    )
    forged = dataclasses.replace(
        computed,
        computation_cursor=forged_cursor,
        computation_dependency_content_evidence=ComputationDependencyContentEvidence(
            input_contract_content_id=SWING_DISTANCE_INPUT_CONTRACT.input_contract_content_id,
            stream_registry_content_id=computed.computation_dependency_content_evidence.stream_registry_content_id,
        ),
    )
    # Sanity: this is a genuinely different, real, well-formed digest -- not
    # a malformed/missing-evidence case (failure class 2) in disguise.
    assert (
        forged.computation_dependency_content_evidence.input_contract_content_id
        != computed.computation_dependency_content_evidence.input_contract_content_id
    )
    with pytest.raises(ReplayPreparationArtifactUnresolvableError, match="not the Input Contract lineage authorized"):
        prepare_replay_evidence(forged)


# --- Failure class 2: malformed/missing evidence ----------------------------


def test_malformed_evidence_fails_closed() -> None:
    computed = _real_regime_fact()
    corrupted = dataclasses.replace(
        computed,
        computation_dependency_content_evidence=ComputationDependencyContentEvidence(
            input_contract_content_id="not-a-well-formed-digest",
            stream_registry_content_id=computed.computation_dependency_content_evidence.stream_registry_content_id,
        ),
    )
    with pytest.raises(ReplayPreparationEvidenceMalformedError):
        prepare_replay_evidence(corrupted)


def test_missing_evidence_fails_closed() -> None:
    computed = _real_regime_fact()
    corrupted = dataclasses.replace(computed, computation_dependency_content_evidence=None)  # type: ignore[arg-type]
    with pytest.raises(ReplayPreparationEvidenceMalformedError):
        prepare_replay_evidence(corrupted)


# --- Failure class 1 (folded in): cursor pins a version with no snapshot ----
# --- (historical note: under the prior, superseded current-path design this
# --- was "Failure class 3" and raised `ReplayPreparationCursorReferenceMis-
# --- matchError`; under cursor-driven snapshot resolution, a nonexistent
# --- pinned version is simply unresolvable — `errors.py` retains that
# --- exception class for historical continuity, but it is no longer raised
# --- by `prepare_replay_evidence`, see module docstring.)


def test_cursor_input_contract_ref_naming_nonexistent_version_fails_closed() -> None:
    """The fact's own `computation_cursor.input_contract_ref` names a
    `contract_version` for which no version-snapshot artifact exists —
    fails closed as unresolvable, never falls back to any other version.
    """
    computed = _real_regime_fact()
    corrupted_cursor = dataclasses.replace(
        computed.computation_cursor,
        input_contract_ref=InputContractRef(
            contract_id=computed.computation_cursor.input_contract_ref.contract_id,
            contract_version="v99.0",
        ),
    )
    corrupted = dataclasses.replace(computed, computation_cursor=corrupted_cursor)
    with pytest.raises(ReplayPreparationArtifactUnresolvableError):
        prepare_replay_evidence(corrupted)


def test_cursor_stream_registry_version_naming_nonexistent_version_fails_closed() -> None:
    computed = _real_regime_fact()
    corrupted_cursor = dataclasses.replace(computed.computation_cursor, stream_registry_version="v99.0")
    corrupted = dataclasses.replace(computed, computation_cursor=corrupted_cursor)
    with pytest.raises(ReplayPreparationArtifactUnresolvableError):
        prepare_replay_evidence(corrupted)


# --- Failure class 4: content-ID mismatch -----------------------------------


def test_input_contract_content_id_mismatch_fails_closed() -> None:
    """Cursor/reference identity still matches the real, current artifact,
    but the persisted evidence's own content digest does not — the
    artifact's own bytes changed since this fact was computed.
    """
    computed = _real_regime_fact()
    wrong_but_well_formed_digest = "0" * 64
    assert wrong_but_well_formed_digest != computed.computation_dependency_content_evidence.input_contract_content_id
    corrupted = dataclasses.replace(
        computed,
        computation_dependency_content_evidence=ComputationDependencyContentEvidence(
            input_contract_content_id=wrong_but_well_formed_digest,
            stream_registry_content_id=computed.computation_dependency_content_evidence.stream_registry_content_id,
        ),
    )
    with pytest.raises(ReplayPreparationContentIdentityMismatchError):
        prepare_replay_evidence(corrupted)


def test_stream_registry_content_id_mismatch_fails_closed() -> None:
    computed = _real_regime_fact()
    wrong_but_well_formed_digest = "f" * 64
    assert wrong_but_well_formed_digest != computed.computation_dependency_content_evidence.stream_registry_content_id
    corrupted = dataclasses.replace(
        computed,
        computation_dependency_content_evidence=ComputationDependencyContentEvidence(
            input_contract_content_id=computed.computation_dependency_content_evidence.input_contract_content_id,
            stream_registry_content_id=wrong_but_well_formed_digest,
        ),
    )
    with pytest.raises(ReplayPreparationContentIdentityMismatchError):
        prepare_replay_evidence(corrupted)


# --- feature_type -> profile mapping coverage --------------------------------


def test_directional_persistence_metric_maps_to_regime_profile() -> None:
    """`volatility_metric` and `directional_persistence_metric` both map to
    the `"regime"` profile — proven independently for the second type,
    never assumed from the first alone.
    """
    allocator = SequenceAllocator(
        module_id="feature-engine", implementation_version="0.1.0", run_id="replay-prep-test-2"
    )
    from conftest import FixedDeltaTimeSource

    definition = make_regime_definition(feature_type="directional_persistence_metric", regime_dimension_version="rgd-2")
    scope = feature_scope("directional_persistence_metric", version=definition.feature_definition_version)
    engine = RegimePassthroughFeatureEngine(
        scope,
        definition,
        allocator,
        FixedDeltaTimeSource(),
        output_event_contract_authority_provider=StaticOutputEventContractAuthorityProvider(
            OUTPUT_EVENT_CONTRACT_AUTHORITY
        ),
        input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
    )
    fact = regime_classified_at(
        allocator,
        0,
        computed_metric="0.5",
        regime_dimension="directional_persistence",
        regime_definition_version="rgd-2",
    )
    events = engine.on_regime_classified(
        fact, cursor=frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    )
    computed = only_computed(events[0])
    prepare_replay_evidence(computed)  # succeeds silently (no exception) — no return value to assert on
