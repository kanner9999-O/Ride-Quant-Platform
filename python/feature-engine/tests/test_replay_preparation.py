"""ADR-037 Replay preparation (`P3-FEATURE-QG-EVID-05(b)`) — fail-closed
BEFORE Replay execution begins, for each of ADR-037's four failure classes.
Preserves `EVID-05(a)`: `prepare_replay_evidence` itself performs filesystem
I/O (it IS the Replay-preparation phase) — `test_replay_isolation.py`
separately proves Replay EXECUTION never calls it or any other
filesystem-touching function.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest
from conftest import (
    OUTPUT_EVENT_CONTRACT_AUTHORITY,
    REGIME_INPUT_CONTRACT,
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
    ReplayPreparationCursorReferenceMismatchError,
    ReplayPreparationEvidenceMalformedError,
)


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


# --- Failure class 3: cursor/reference relational mismatch ------------------


def test_cursor_input_contract_ref_mismatch_fails_closed() -> None:
    """The fact's own `computation_cursor.input_contract_ref` no longer
    matches what is currently resolvable at the real repository — e.g. the
    artifact evolved to a different `contract_version` since this fact was
    computed.
    """
    computed = _real_regime_fact()
    corrupted_cursor = dataclasses.replace(
        computed.computation_cursor,
        input_contract_ref=InputContractRef(
            contract_id=computed.computation_cursor.input_contract_ref.contract_id,
            contract_version="not-the-real-version",
        ),
    )
    corrupted = dataclasses.replace(computed, computation_cursor=corrupted_cursor)
    with pytest.raises(ReplayPreparationCursorReferenceMismatchError):
        prepare_replay_evidence(corrupted)


def test_cursor_stream_registry_version_mismatch_fails_closed() -> None:
    computed = _real_regime_fact()
    corrupted_cursor = dataclasses.replace(
        computed.computation_cursor, stream_registry_version="not-the-real-registry-version"
    )
    corrupted = dataclasses.replace(computed, computation_cursor=corrupted_cursor)
    with pytest.raises(ReplayPreparationCursorReferenceMismatchError):
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
