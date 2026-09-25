from __future__ import annotations

import dataclasses
import random
from decimal import Decimal

import pytest
from conftest import full_valid_kwargs, make_candle, make_feature, make_regime, make_structure

from context_aggregator import (
    ContextAggregationCandidate,
    ContextDefinition,
    ContextSubjectScope,
    DirectionalPersistenceRegimeClass,
    DuplicateFactReferenceError,
    FeatureType,
    RegimeClassTypeMismatchError,
    RegimeDimension,
    ScopeDefinitionMismatchError,
    StructureOrientation,
    VolatilityRegimeClass,
    aggregate_context_candidate,
)


@pytest.mark.parametrize(
    "role_key",
    [
        "candle_candidates",
        "structure_candidates",
        "volatility_regime_candidates",
        "directional_persistence_regime_candidates",
        "volatility_metric_candidates",
        "directional_persistence_metric_candidates",
        "distance_to_last_confirmed_swing_candidates",
    ],
)
def test_each_of_the_seven_roles_missing_yields_no_candidate(
    scope: ContextSubjectScope, definition: ContextDefinition, role_key: str
) -> None:
    kwargs = full_valid_kwargs(scope, definition)
    kwargs[role_key] = []
    assert aggregate_context_candidate(**kwargs) is None  # type: ignore[arg-type]


def test_scope_definition_mismatch_raises(scope: ContextSubjectScope, definition: ContextDefinition) -> None:
    wrong_definition = dataclasses.replace(definition, context_definition_version="ctxdef-v2")
    kwargs = full_valid_kwargs(scope, wrong_definition)
    with pytest.raises(ScopeDefinitionMismatchError):
        aggregate_context_candidate(**kwargs)  # type: ignore[arg-type]


def test_cross_role_duplicate_winner_ref_fails_closed(
    scope: ContextSubjectScope, definition: ContextDefinition
) -> None:
    kwargs = full_valid_kwargs(scope, definition)
    structure_candidates = kwargs["structure_candidates"]
    assert isinstance(structure_candidates, list)
    shared_ref = structure_candidates[0].ref
    volatility_regime_candidates = kwargs["volatility_regime_candidates"]
    assert isinstance(volatility_regime_candidates, list)
    kwargs["volatility_regime_candidates"] = [dataclasses.replace(volatility_regime_candidates[0], ref=shared_ref)]
    with pytest.raises(DuplicateFactReferenceError):
        aggregate_context_candidate(**kwargs)  # type: ignore[arg-type]


def test_regime_class_type_mismatch_fails_closed(scope: ContextSubjectScope, definition: ContextDefinition) -> None:
    kwargs = full_valid_kwargs(scope, definition)
    volatility_regime_candidates = kwargs["volatility_regime_candidates"]
    assert isinstance(volatility_regime_candidates, list)
    kwargs["volatility_regime_candidates"] = [
        dataclasses.replace(volatility_regime_candidates[0], regime_class=DirectionalPersistenceRegimeClass.DIRECTIONAL)
    ]
    with pytest.raises(RegimeClassTypeMismatchError):
        aggregate_context_candidate(**kwargs)  # type: ignore[arg-type]


def test_full_valid_evidence_produces_a_candidate(scope: ContextSubjectScope, definition: ContextDefinition) -> None:
    result = aggregate_context_candidate(**full_valid_kwargs(scope, definition))  # type: ignore[arg-type]
    assert result is not None
    assert isinstance(result, ContextAggregationCandidate)


def test_exact_seven_role_cardinality(scope: ContextSubjectScope, definition: ContextDefinition) -> None:
    result = aggregate_context_candidate(**full_valid_kwargs(scope, definition))  # type: ignore[arg-type]
    assert result is not None
    assert len(result.normalized_input_fact_refs) == 7
    assert len(set(result.normalized_input_fact_refs)) == 7


def test_missing_one_role_yields_no_candidate(scope: ContextSubjectScope, definition: ContextDefinition) -> None:
    kwargs = full_valid_kwargs(scope, definition)
    kwargs["distance_to_last_confirmed_swing_candidates"] = []
    result = aggregate_context_candidate(**kwargs)  # type: ignore[arg-type]
    assert result is None


def test_invalidated_required_role_yields_no_candidate(
    scope: ContextSubjectScope, definition: ContextDefinition
) -> None:
    kwargs = full_valid_kwargs(scope, definition)
    structure_candidates = kwargs["structure_candidates"]
    assert isinstance(structure_candidates, list)
    kwargs["structure_invalidated_refs"] = frozenset({structure_candidates[0].ref})
    result = aggregate_context_candidate(**kwargs)  # type: ignore[arg-type]
    assert result is None


def test_no_partial_result_when_role_missing(scope: ContextSubjectScope, definition: ContextDefinition) -> None:
    """context.md §9: absolutely no partial snapshot — the entrypoint's
    return type is either a full candidate or exactly `None`, never
    anything in between."""
    kwargs = full_valid_kwargs(scope, definition)
    kwargs["volatility_metric_candidates"] = []
    result = aggregate_context_candidate(**kwargs)  # type: ignore[arg-type]
    assert result is None


def test_incoming_order_independence(scope: ContextSubjectScope, definition: ContextDefinition) -> None:
    """Same seven facts, delivered in a different order per role, must
    normalize to the identical computation identity (context.md §10)."""
    kwargs_a = full_valid_kwargs(scope, definition)

    extra_structure = make_structure("structure-extra", effective_minute=5, recorded=6)
    kwargs_b = full_valid_kwargs(scope, definition)
    structure_candidates = kwargs_b["structure_candidates"]
    assert isinstance(structure_candidates, list)
    reordered = [structure_candidates[0], extra_structure]
    random.Random(42).shuffle(reordered)
    kwargs_b["structure_candidates"] = reordered

    result_a = aggregate_context_candidate(**kwargs_a)  # type: ignore[arg-type]
    result_b = aggregate_context_candidate(**kwargs_b)  # type: ignore[arg-type]
    assert result_a is not None
    assert result_b is not None
    assert result_a.normalized_input_fact_refs == result_b.normalized_input_fact_refs
    assert result_a.context_subject_id == result_b.context_subject_id


def test_assembled_context_values_equal_upstream_values_exactly(
    scope: ContextSubjectScope, definition: ContextDefinition
) -> None:
    kwargs = full_valid_kwargs(scope, definition)
    structure = make_structure(orientation=StructureOrientation.BEARISH)
    kwargs["structure_candidates"] = [structure]
    vol_regime = make_regime(
        "regime-vol-1",
        dimension=RegimeDimension.VOLATILITY,
        regime_class=VolatilityRegimeClass.HIGH,
        definition_version="regime-vol-v1",
        stream_id="stream-regime-vol",
    )
    kwargs["volatility_regime_candidates"] = [vol_regime]
    dp_regime = make_regime(
        "regime-dp-1",
        dimension=RegimeDimension.DIRECTIONAL_PERSISTENCE,
        regime_class=DirectionalPersistenceRegimeClass.TRANSITIONAL,
        definition_version="regime-dp-v1",
        stream_id="stream-regime-dp",
    )
    kwargs["directional_persistence_regime_candidates"] = [dp_regime]
    vol_feature = make_feature(
        "feat-vol-1",
        feature_type=FeatureType.VOLATILITY_METRIC,
        value=Decimal("9.87654321"),
        definition_version="feat-vol-v1",
        stream_id="stream-feat-vol",
    )
    kwargs["volatility_metric_candidates"] = [vol_feature]

    result = aggregate_context_candidate(**kwargs)  # type: ignore[arg-type]
    assert result is not None
    assert result.context_values.structure_orientation is StructureOrientation.BEARISH
    assert result.context_values.volatility_regime_class is VolatilityRegimeClass.HIGH
    assert result.context_values.directional_persistence_regime_class is DirectionalPersistenceRegimeClass.TRANSITIONAL
    assert result.context_values.volatility_metric == Decimal("9.87654321")


def test_decimal_value_preserved_without_float_round_trip(
    scope: ContextSubjectScope, definition: ContextDefinition
) -> None:
    precise = Decimal("0.1234567890123456789")
    kwargs = full_valid_kwargs(scope, definition)
    kwargs["distance_to_last_confirmed_swing_candidates"] = [
        make_feature(
            "feat-dist-precise",
            feature_type=FeatureType.DISTANCE_TO_LAST_CONFIRMED_SWING,
            value=precise,
            definition_version="feat-dist-v1",
            stream_id="stream-feat-dist",
        )
    ]
    result = aggregate_context_candidate(**kwargs)  # type: ignore[arg-type]
    assert result is not None
    assert isinstance(result.context_values.distance_to_last_confirmed_swing, Decimal)
    assert result.context_values.distance_to_last_confirmed_swing == precise
    # A float round-trip would have silently lost precision here.
    assert float(precise) != precise or True  # documents intent; equality above is the real assertion
    assert str(result.context_values.distance_to_last_confirmed_swing) == "0.1234567890123456789"


def test_context_values_has_no_strategy_decision_risk_execution_fields(
    scope: ContextSubjectScope, definition: ContextDefinition
) -> None:
    """context.md §17: `context_values` must never contain signal strength,
    setup quality, bias, buy/sell/hold, entry/stop/target, position size,
    strategy id, or account state — enforced here as a structural
    assertion on the dataclass's own field set."""
    result = aggregate_context_candidate(**full_valid_kwargs(scope, definition))  # type: ignore[arg-type]
    assert result is not None
    field_names = {f.name for f in dataclasses.fields(result.context_values)}
    assert field_names == {
        "structure_orientation",
        "volatility_regime_class",
        "directional_persistence_regime_class",
        "volatility_metric",
        "directional_persistence_metric",
        "distance_to_last_confirmed_swing",
    }
    forbidden_substrings = (
        "signal",
        "strength",
        "quality",
        "bias",
        "buy",
        "sell",
        "hold",
        "entry",
        "stop",
        "target",
        "position",
        "strategy",
        "account",
        "risk",
        "order",
        "execution",
    )
    for name in field_names:
        lowered = name.lower()
        assert not any(bad in lowered for bad in forbidden_substrings), name


def test_result_never_claims_authoritative_publication_identity(
    scope: ContextSubjectScope, definition: ContextDefinition
) -> None:
    """`ContextAggregationCandidate` must never carry a fabricated
    envelope/publication identity — only the fields Section I permits."""
    result = aggregate_context_candidate(**full_valid_kwargs(scope, definition))  # type: ignore[arg-type]
    assert result is not None
    field_names = {f.name for f in dataclasses.fields(result)}
    forbidden = {"event_id", "event_contract_ref", "stream_ref", "producer_ref", "sequence", "causation_refs"}
    assert field_names.isdisjoint(forbidden)


def test_candle_facts_never_appear_as_one_of_the_six_role_refs(
    scope: ContextSubjectScope, definition: ContextDefinition
) -> None:
    result = aggregate_context_candidate(**full_valid_kwargs(scope, definition))  # type: ignore[arg-type]
    assert result is not None
    role_refs = {
        result.structure_fact_ref,
        result.volatility_regime_fact_ref,
        result.directional_persistence_regime_fact_ref,
        result.volatility_metric_fact_ref,
        result.directional_persistence_metric_fact_ref,
        result.distance_to_last_confirmed_swing_fact_ref,
    }
    assert result.context_cutoff_source_ref not in role_refs
    assert len(role_refs) == 6


def test_extra_candidates_from_a_different_window_do_not_corrupt_result(
    scope: ContextSubjectScope, definition: ContextDefinition
) -> None:
    """CONTEXT-CORE-A-MAJ-01: an unrelated Candle window present in the
    supplied candidate set must never hijack the explicitly requested
    computation point (`target_computation_point_ref`, set by
    `full_valid_kwargs` to the intended candle's own ref)."""
    kwargs = full_valid_kwargs(scope, definition)
    unrelated_earlier_candle = make_candle("candle-earlier-window", start=-120, end=-60, recorded=-59)
    candle_candidates = kwargs["candle_candidates"]
    assert isinstance(candle_candidates, list)
    kwargs["candle_candidates"] = [*candle_candidates, unrelated_earlier_candle]
    result = aggregate_context_candidate(**kwargs)  # type: ignore[arg-type]
    assert result is not None
    assert result.context_cutoff_source_ref == candle_candidates[0].ref


def test_later_unrelated_candle_window_never_hijacks_requested_computation_point(
    scope: ContextSubjectScope, definition: ContextDefinition
) -> None:
    """Same MAJ-01 regression, with the unrelated window LATER instead of
    earlier -- total order would have picked it under the old defect."""
    kwargs = full_valid_kwargs(scope, definition)
    candle_candidates = kwargs["candle_candidates"]
    assert isinstance(candle_candidates, list)
    unrelated_later_candle = make_candle("candle-later-window", start=120, end=180, recorded=181)
    kwargs["candle_candidates"] = [*candle_candidates, unrelated_later_candle]
    result = aggregate_context_candidate(**kwargs)  # type: ignore[arg-type]
    assert result is not None
    assert result.context_cutoff_source_ref == candle_candidates[0].ref
    assert result.effective_window == candle_candidates[0].effective_window
