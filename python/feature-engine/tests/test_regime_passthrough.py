from __future__ import annotations

import dataclasses
from datetime import timedelta
from decimal import Decimal

import pytest
from conftest import (
    BASE,
    FEATURE_OUTPUT_CONTRACT_VERSION,
    FixedDeltaTimeSource,
    feature_scope,
    make_regime_definition,
    only_computed,
    only_invalidated,
    regime_classified_at,
    regime_invalidated_at,
)

from feature_engine import EventContractRef, RegimePassthroughFeatureEngine, SequenceAllocator
from feature_engine.errors import (
    DefinitionVersionMismatchError,
    EvidenceReferenceConflictError,
    FeatureLineageError,
    RegimeDimensionMismatchError,
    UnauthorizedUpstreamContractError,
    UnresolvedOutputContractAuthorityError,
)


def _engine(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource, feature_type: str = "volatility_metric"
) -> RegimePassthroughFeatureEngine:
    definition = make_regime_definition(feature_type=feature_type, regime_dimension_version="rgd-1")
    scope = feature_scope(feature_type, version=definition.feature_definition_version)
    return RegimePassthroughFeatureEngine(
        scope, definition, allocator, time_source, feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION
    )


# --- P3-FEATURE-A-MAJ-02 remediation: output contract-version authority ------


def test_output_contract_version_must_be_genuine_non_empty(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    definition = make_regime_definition(regime_dimension_version="rgd-1")
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    with pytest.raises(UnresolvedOutputContractAuthorityError):
        RegimePassthroughFeatureEngine(scope, definition, allocator, time_source, feature_event_contract_version="")


# --- 3. Regime volatility pass-through ---------------------------------------


def test_regime_volatility_correct_dimension_and_version_accepted(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    computed = only_computed(engine.on_regime_classified(fact)[0])
    assert computed.value == Decimal("1.50")
    assert computed.input_fact_refs == (fact.ref,)


def test_regime_volatility_wrong_dimension_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator,
        0,
        computed_metric="1.5",
        regime_dimension="directional_persistence",
        regime_definition_version="rgd-1",
    )
    with pytest.raises(RegimeDimensionMismatchError):
        engine.on_regime_classified(fact)


def test_regime_volatility_wrong_definition_version_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-2"
    )
    with pytest.raises(DefinitionVersionMismatchError):
        engine.on_regime_classified(fact)


# --- P3-FEATURE-A-MAJ-02 remediation: contract qualification -----------------


def test_unauthorized_regime_contract_id_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    bad = dataclasses.replace(fact, event_contract_ref=EventContractRef("regime-current-view", "v1"))
    with pytest.raises(UnauthorizedUpstreamContractError):
        engine.on_regime_classified(bad)


# --- P3-FEATURE-A-MAJ-05 remediation: same-ref-different-content fails closed


def test_regime_same_ref_different_content_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    engine.on_regime_classified(fact)
    conflicting = dataclasses.replace(fact, computed_metric=Decimal("9.9"))
    with pytest.raises(EvidenceReferenceConflictError):
        engine.on_regime_classified(conflicting)


# --- 4. Directional persistence pass-through --------------------------------


def test_directional_persistence_continuous_value_no_reinterpretation(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source, feature_type="directional_persistence_metric")
    fact = regime_classified_at(
        allocator,
        0,
        computed_metric="0.42",
        regime_dimension="directional_persistence",
        regime_definition_version="rgd-1",
    )
    computed = only_computed(engine.on_regime_classified(fact)[0])
    assert computed.value == Decimal("0.42")
    field_names = {f.name for f in dataclasses.fields(computed)}
    assert not field_names & {"direction", "label", "orientation", "class_label"}


# --- 13. Dedup ---------------------------------------------------------------


def test_dedup_identical_computation_identity_emits_once(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    assert len(engine.on_regime_classified(fact)) == 1
    assert engine.on_regime_classified(fact) == []


def test_same_value_different_windows_emits_separately(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact0 = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    fact1 = regime_classified_at(
        allocator, 1, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    computed0 = only_computed(engine.on_regime_classified(fact0)[0])
    computed1 = only_computed(engine.on_regime_classified(fact1)[0])
    assert computed0.ref != computed1.ref
    assert computed0.window_start != computed1.window_start


# --- 14. Correction: no shortcut ----------------------------------------------


def test_correction_invalidate_and_replace_even_when_value_unchanged(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    original_input = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    original = only_computed(engine.on_regime_classified(original_input)[0])

    invalidation_input = regime_invalidated_at(
        allocator, invalidated_fact_ref=original_input.ref, recorded_time=original.recorded_time + timedelta(minutes=5)
    )
    invalidation = only_invalidated(engine.on_regime_invalidated(invalidation_input)[0])
    assert invalidation.invalidated_fact_ref == original.ref

    replacement_input = regime_classified_at(
        allocator,
        0,
        computed_metric="1.5",
        regime_dimension="volatility",
        regime_definition_version="rgd-1",
        recorded_offset_seconds=600,
    )
    replacement = only_computed(engine.on_regime_classified(replacement_input)[0])
    assert replacement.value == original.value == Decimal("1.50")
    assert replacement.supersedes_fact_ref == original.ref
    assert replacement.ref != original.ref


def test_causal_chain_original_lt_invalidation_lt_replacement(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    original_input = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    original = only_computed(engine.on_regime_classified(original_input)[0])
    invalidation_input = regime_invalidated_at(
        allocator, invalidated_fact_ref=original_input.ref, recorded_time=original.recorded_time + timedelta(minutes=5)
    )
    invalidation = only_invalidated(engine.on_regime_invalidated(invalidation_input)[0])
    replacement_input = regime_classified_at(
        allocator,
        0,
        computed_metric="1.5",
        regime_dimension="volatility",
        regime_definition_version="rgd-1",
        recorded_offset_seconds=600,
    )
    replacement = only_computed(engine.on_regime_classified(replacement_input)[0])
    assert original.recorded_time < invalidation.recorded_time < replacement.recorded_time


# --- 15. Lineage: no fork, no skip -------------------------------------------


def test_lineage_no_skip_replacement_without_invalidation_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    original_input = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    engine.on_regime_classified(original_input)
    different_input = regime_classified_at(
        allocator, 0, computed_metric="2.0", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    with pytest.raises(FeatureLineageError):
        engine.on_regime_classified(different_input)


def test_lineage_no_fork_double_invalidation_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    original_input = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    original = only_computed(engine.on_regime_classified(original_input)[0])
    invalidation_input = regime_invalidated_at(
        allocator, invalidated_fact_ref=original_input.ref, recorded_time=original.recorded_time + timedelta(minutes=5)
    )
    engine.on_regime_invalidated(invalidation_input)
    replacement_input = regime_classified_at(
        allocator,
        0,
        computed_metric="1.5",
        regime_dimension="volatility",
        regime_definition_version="rgd-1",
        recorded_offset_seconds=600,
    )
    engine.on_regime_classified(replacement_input)

    # Targeting the now-superseded original ref again must fail — lineage head has moved on.
    stale_invalidation = regime_invalidated_at(
        allocator, invalidated_fact_ref=original_input.ref, recorded_time=original.recorded_time + timedelta(minutes=10)
    )
    with pytest.raises(FeatureLineageError):
        engine.on_regime_invalidated(stale_invalidation)


# --- 16. Causal ordering ------------------------------------------------------


def test_invalidation_before_original_rejected(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    bogus_ref = allocator.next_ref("regime")
    invalidation_input = regime_invalidated_at(allocator, invalidated_fact_ref=bogus_ref, recorded_time=BASE)
    with pytest.raises(FeatureLineageError):
        engine.on_regime_invalidated(invalidation_input)
