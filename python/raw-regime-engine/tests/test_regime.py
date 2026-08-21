from __future__ import annotations

import dataclasses
import pathlib
import re
from datetime import timedelta
from decimal import Decimal

import pytest
from conftest import (
    FixedDeltaTimeSource,
    NonCausalTimeSource,
    RangeFormula,
    SumCloseFormula,
    candle_at,
    current_result,
    directional_persistence_definition,
    make_definition,
    only_classified,
    only_invalidated,
    regime_scope,
    volatility_definition,
)

import raw_regime_engine
from raw_regime_engine import (
    CANDLE_EVIDENCE_NORMALIZATION_POLICY,
    CURRENT_VIEW_SELECTION_POLICY,
    OHLCV,
    AnalysisWindow,
    CandleFact,
    CandleScope,
    DecimalPrecisionPolicy,
    RegimeClassified,
    RegimeCurrentView,
    RegimeDefinition,
    RegimeDimensionDefinition,
    RegimeEngine,
    RegimeEvent,
    RegimeFactInvalidated,
    SequenceAllocator,
    ThresholdBand,
    normalize_evidence,
)
from raw_regime_engine.errors import (
    EvidenceCardinalityError,
    EvidenceReferenceConflictError,
    ForeignScopeError,
    FormulaMismatchError,
    NonMonotonicRecordedTimeError,
    RecordedTimeSourceViolationError,
    RegimeLineageError,
)

# --- warm-up / every-completed-window emission -----------------------------


def test_warm_up_is_valid_absence_not_error(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)

    c0 = candle_at(allocator, 0, high="10", low="9")
    c1 = candle_at(allocator, 1, high="10", low="9")
    assert engine.on_candle(c0) == []
    assert engine.on_candle(c1) == []


def test_every_completed_window_emits_including_identical_class(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)

    c0 = candle_at(allocator, 0, high="10", low="9")
    c1 = candle_at(allocator, 1, high="10", low="9")
    c2 = candle_at(allocator, 2, high="10", low="9")
    c3 = candle_at(allocator, 3, high="10", low="9")

    engine.on_candle(c0)
    engine.on_candle(c1)
    events_2 = engine.on_candle(c2)
    events_3 = engine.on_candle(c3)

    assert len(events_2) == 1
    assert len(events_3) == 1
    fact_2, fact_3 = only_classified(events_2[0]), only_classified(events_3[0])
    assert fact_2.class_label == "LOW"
    assert fact_3.class_label == "LOW"
    assert fact_2.computed_metric == Decimal("1.00") == fact_3.computed_metric
    assert fact_2.supersedes_fact_ref is None
    assert fact_3.supersedes_fact_ref is None
    assert (fact_2.window_start, fact_2.window_end) != (fact_3.window_start, fact_3.window_end)
    assert fact_2.ref != fact_3.ref


def test_both_dimensions_classify_independently(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    vol_scope = regime_scope("volatility")
    dp_scope = regime_scope("directional_persistence")
    definition = make_definition(
        volatility=volatility_definition(), directional_persistence=directional_persistence_definition()
    )
    vol_engine = RegimeEngine(vol_scope, definition, RangeFormula(), allocator, time_source)
    dp_engine = RegimeEngine(dp_scope, definition, SumCloseFormula(), allocator, time_source)

    candles = [candle_at(allocator, i, high="10", low="9", close="10") for i in range(3)]
    for c in candles[:-1]:
        assert vol_engine.on_candle(c) == []
        assert dp_engine.on_candle(c) == []
    vol_fact = only_classified(vol_engine.on_candle(candles[-1])[0])
    dp_fact = only_classified(dp_engine.on_candle(candles[-1])[0])

    assert vol_fact.class_label == "LOW"  # range=1
    assert dp_fact.class_label == "NON_DIRECTIONAL"  # sum(close)=30
    assert vol_scope.regime_subject_id != dp_scope.regime_subject_id


# --- threshold comparison policy --------------------------------------------


def test_threshold_boundary_strict_moves_to_next_band(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition(window_candle_count=1, comparison="strict"))
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    c0 = candle_at(allocator, 0, high="10", low="5")  # range == 5, exactly the LOW upper bound
    fact = only_classified(engine.on_candle(c0)[0])
    assert fact.computed_metric == Decimal("5.00")
    assert fact.class_label == "NORMAL"  # strict: 5 < 5 is False -> falls through to NORMAL


def test_threshold_boundary_inclusive_stays_in_band(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition(window_candle_count=1, comparison="inclusive"))
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    c0 = candle_at(allocator, 0, high="10", low="5")  # range == 5
    fact = only_classified(engine.on_candle(c0)[0])
    assert fact.class_label == "LOW"  # inclusive: 5 <= 5 is True


# --- decimal precision -------------------------------------------------------


def test_decimal_precision_policy_rounding_modes() -> None:
    half_up = DecimalPrecisionPolicy(digits=2, rounding="ROUND_HALF_UP")
    half_even = DecimalPrecisionPolicy(digits=2, rounding="ROUND_HALF_EVEN")
    assert half_up.apply(Decimal("1.005")) == Decimal("1.01")
    assert half_even.apply(Decimal("1.005")) == Decimal("1.00")


def test_decimal_precision_policy_rejects_unknown_rounding() -> None:
    with pytest.raises(ValueError):
        DecimalPrecisionPolicy(digits=2, rounding="ROUND_TO_TASTE")


# --- formula boundary (no canonical formula invented) -----------------------


def test_formula_id_mismatch_fails_closed(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    class WrongFormula:
        formula_id = "not-the-configured-formula"

        def compute(self, evidence: object) -> Decimal:
            return Decimal(0)

    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    with pytest.raises(FormulaMismatchError):
        RegimeEngine(scope, definition, WrongFormula(), allocator, time_source)


def test_test_only_formula_injection_drives_classification(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("directional_persistence")
    definition = make_definition(directional_persistence=directional_persistence_definition())
    formula = SumCloseFormula()
    assert formula.formula_id.startswith("test-"), "test-only formulas must not look like production ids"
    engine = RegimeEngine(scope, definition, formula, allocator, time_source)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="10", close="10"))
    fact = only_classified(events[0])
    assert fact.computed_metric == Decimal("30.00")
    assert fact.class_label == "NON_DIRECTIONAL"


# --- Finding 1 (P3-RGE-POLICY-A-MAJ-01): canonical policy identifiers -------


def test_canonical_policy_identifiers_exact_values() -> None:
    assert CANDLE_EVIDENCE_NORMALIZATION_POLICY == (
        "window_start_asc_then_window_end_asc_then_stream_id_asc_then_registry_version_asc_"
        "then_sequence_asc_then_event_id_asc"
    )
    assert CURRENT_VIEW_SELECTION_POLICY == (
        "analysis_window_end_desc_then_window_start_desc_then_recorded_time_asc_then_stream_id_asc_"
        "then_registry_version_asc_then_sequence_asc_then_event_id_asc"
    )


def test_definition_accepts_exact_canonical_policy_values() -> None:
    make_definition()  # uses the real exported canonical constants directly — must not raise


def _definition_with_policies(view_policy: str, evidence_policy: str) -> RegimeDefinition:
    return RegimeDefinition(
        regime_definition_version="rgd-1",
        dimensions={
            "volatility": volatility_definition(),
            "directional_persistence": directional_persistence_definition(),
        },
        current_view_selection_policy=view_policy,
        candle_evidence_normalization_policy=evidence_policy,
    )


def test_definition_rejects_previous_implementation_invented_policy_values() -> None:
    with pytest.raises(ValueError):
        _definition_with_policies(
            "regime.md-11-max-window-end-then-window-start-v1", CANDLE_EVIDENCE_NORMALIZATION_POLICY
        )
    with pytest.raises(ValueError):
        _definition_with_policies(
            CURRENT_VIEW_SELECTION_POLICY,
            "regime.md-8a-window-stream-registryversion-sequence-eventid-lexicographic-v1",
        )


def test_definition_rejects_one_character_mismatch_in_policy_values() -> None:
    mutated_view_policy = CURRENT_VIEW_SELECTION_POLICY[:-1] + (
        "x" if CURRENT_VIEW_SELECTION_POLICY[-1] != "x" else "y"
    )
    with pytest.raises(ValueError):
        _definition_with_policies(mutated_view_policy, CANDLE_EVIDENCE_NORMALIZATION_POLICY)

    mutated_evidence_policy = CANDLE_EVIDENCE_NORMALIZATION_POLICY[:-1] + (
        "x" if CANDLE_EVIDENCE_NORMALIZATION_POLICY[-1] != "x" else "y"
    )
    with pytest.raises(ValueError):
        _definition_with_policies(CURRENT_VIEW_SELECTION_POLICY, mutated_evidence_policy)


# --- Finding 2 (P3-RGE-TIME-A-MAJ-02): authoritative recorded_time ----------


def test_original_fact_recorded_time_strictly_after_evidence(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    for c in candles[:-1]:
        engine.on_candle(c)
    fact = only_classified(engine.on_candle(candles[-1])[0])
    assert fact.recorded_time > max(c.recorded_time for c in candles)


def test_correction_chain_strict_causal_ordering(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    original = only_classified(events[0])

    correction = candle_at(allocator, 1, high="20", low="9", is_correction=True, recorded_offset_seconds=120)
    invalidation, replacement = engine.on_candle(correction)
    invalidation = only_invalidated(invalidation)
    replacement = only_classified(replacement)

    assert invalidation.recorded_time > original.recorded_time
    assert invalidation.recorded_time > correction.recorded_time
    assert replacement.recorded_time > invalidation.recorded_time
    # Real cursor interval: original < invalidation < replacement.
    assert original.recorded_time < invalidation.recorded_time < replacement.recorded_time


def test_cursor_between_invalidation_and_replacement_observes_pending(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    original = only_classified(events[0])
    correction = candle_at(allocator, 1, high="20", low="9", is_correction=True, recorded_offset_seconds=120)
    invalidation, replacement = engine.on_candle(correction)
    invalidation = only_invalidated(invalidation)
    replacement = only_classified(replacement)
    assert original.recorded_time < invalidation.recorded_time < replacement.recorded_time

    view = RegimeCurrentView(scope)
    view.on_regime_classified(original)
    view.on_regime_invalidated(invalidation)  # a cursor strictly between invalidation and replacement
    assert current_result(view).view_state == "PENDING_CORRECTION"

    view.on_regime_classified(replacement)
    assert current_result(view).view_state == "VALID"


def test_invalid_time_provider_fails_closed(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, NonCausalTimeSource())
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    engine.on_candle(candles[0])
    engine.on_candle(candles[1])
    with pytest.raises(RecordedTimeSourceViolationError):
        engine.on_candle(candles[2])


def test_overlapping_windows_correction_each_satisfies_own_causal_ordering(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    originals: list[RegimeClassified] = []
    for i in range(5):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
        originals.extend(only_classified(e) for e in events)
    assert len(originals) == 3

    correction = candle_at(allocator, 2, high="30", low="9", is_correction=True, recorded_offset_seconds=180)
    events = engine.on_candle(correction)
    assert len(events) == 6
    for pair_index in range(3):
        invalidation = only_invalidated(events[pair_index * 2])
        replacement = only_classified(events[pair_index * 2 + 1])
        original = originals[pair_index]
        assert original.recorded_time < invalidation.recorded_time < replacement.recorded_time


# --- Finding 3 (P3-RGE-DEF-A-MAJ-03): RegimeDefinition immutable snapshot ---


def test_definition_dimensions_defensive_copy_from_caller_mapping() -> None:
    caller_dict: dict[str, RegimeDimensionDefinition] = {
        "volatility": volatility_definition(),
        "directional_persistence": directional_persistence_definition(),
    }
    definition = RegimeDefinition(
        regime_definition_version="rgd-1",
        dimensions=caller_dict,
        current_view_selection_policy=CURRENT_VIEW_SELECTION_POLICY,
        candle_evidence_normalization_policy=CANDLE_EVIDENCE_NORMALIZATION_POLICY,
    )
    original_volatility = definition.dimensions["volatility"]
    caller_dict["volatility"] = volatility_definition(window_candle_count=99)  # mutate AFTER construction
    caller_dict["extra"] = directional_persistence_definition()

    assert definition.dimensions["volatility"] is original_volatility
    assert "extra" not in definition.dimensions
    assert set(definition.dimensions.keys()) == {"volatility", "directional_persistence"}


def test_definition_dimensions_view_is_read_only() -> None:
    definition = make_definition()
    with pytest.raises(TypeError):
        definition.dimensions["volatility"] = volatility_definition()  # type: ignore[index]


def test_definition_content_identity_matches_for_identical_content() -> None:
    first = make_definition()
    second = make_definition()
    assert first is not second
    assert first.content_identity() == second.content_identity()
    assert hash(first) == hash(second)


def test_definition_content_identity_differs_for_changed_content() -> None:
    baseline = make_definition()
    changed = make_definition(volatility=volatility_definition(window_candle_count=5))
    assert baseline.content_identity() != changed.content_identity()


def test_definition_content_identity_reflects_version_but_does_not_replace_it() -> None:
    v1 = make_definition(version="rgd-1")
    v2 = make_definition(version="rgd-2")
    assert v1.regime_definition_version == "rgd-1"
    assert v2.regime_definition_version == "rgd-2"
    assert v1.content_identity() != v2.content_identity()


def test_definition_requires_both_dimensions_missing_rejected() -> None:
    with pytest.raises(ValueError):
        RegimeDefinition(
            regime_definition_version="rgd-1",
            dimensions={"volatility": volatility_definition()},
            current_view_selection_policy=CURRENT_VIEW_SELECTION_POLICY,
            candle_evidence_normalization_policy=CANDLE_EVIDENCE_NORMALIZATION_POLICY,
        )


def test_definition_requires_both_dimensions_extra_rejected() -> None:
    with pytest.raises(ValueError):
        RegimeDefinition(
            regime_definition_version="rgd-1",
            dimensions={
                "volatility": volatility_definition(),
                "directional_persistence": directional_persistence_definition(),
                "activity": volatility_definition(),
            },
            current_view_selection_policy=CURRENT_VIEW_SELECTION_POLICY,
            candle_evidence_normalization_policy=CANDLE_EVIDENCE_NORMALIZATION_POLICY,
        )


# --- Finding 6 (P3-RGE-THRESH-A-MIN-06): threshold label completeness ------


def test_definition_accepts_complete_exact_label_set_for_both_dimensions() -> None:
    make_definition()  # default definitions already satisfy this exactly


def test_definition_rejects_label_outside_dimension_vocabulary() -> None:
    bad_dimension = RegimeDimensionDefinition(
        window_candle_count=1,
        metric_formula_id="whatever",
        class_thresholds=(ThresholdBand(upper_bound=None, label="BOGUS_LABEL"),),
        threshold_comparison_policy="strict",
        warm_up_policy="require_full_window",
        gap_policy="defer_until_resolved",
        decimal_precision_policy=DecimalPrecisionPolicy(digits=2, rounding="ROUND_HALF_UP"),
    )
    with pytest.raises(ValueError):
        make_definition(volatility=bad_dimension)


def test_definition_rejects_missing_label() -> None:
    incomplete = RegimeDimensionDefinition(
        window_candle_count=3,
        metric_formula_id=RangeFormula.formula_id,
        class_thresholds=(
            ThresholdBand(upper_bound=Decimal("5"), label="LOW"),
            ThresholdBand(upper_bound=Decimal("10"), label="NORMAL"),
            ThresholdBand(upper_bound=None, label="HIGH"),  # EXTREME missing
        ),
        threshold_comparison_policy="strict",
        warm_up_policy="require_full_window",
        gap_policy="defer_until_resolved",
        decimal_precision_policy=DecimalPrecisionPolicy(digits=2, rounding="ROUND_HALF_UP"),
    )
    with pytest.raises(ValueError):
        make_definition(volatility=incomplete)


def test_definition_rejects_duplicate_label() -> None:
    duplicate = RegimeDimensionDefinition(
        window_candle_count=3,
        metric_formula_id=RangeFormula.formula_id,
        class_thresholds=(
            ThresholdBand(upper_bound=Decimal("5"), label="LOW"),
            ThresholdBand(upper_bound=Decimal("10"), label="LOW"),
            ThresholdBand(upper_bound=Decimal("20"), label="HIGH"),
            ThresholdBand(upper_bound=None, label="EXTREME"),
        ),
        threshold_comparison_policy="strict",
        warm_up_policy="require_full_window",
        gap_policy="defer_until_resolved",
        decimal_precision_policy=DecimalPrecisionPolicy(digits=2, rounding="ROUND_HALF_UP"),
    )
    with pytest.raises(ValueError):
        make_definition(volatility=duplicate)


def test_definition_rejects_extra_label() -> None:
    extra = RegimeDimensionDefinition(
        window_candle_count=3,
        metric_formula_id=RangeFormula.formula_id,
        class_thresholds=(
            ThresholdBand(upper_bound=Decimal("5"), label="LOW"),
            ThresholdBand(upper_bound=Decimal("10"), label="NORMAL"),
            ThresholdBand(upper_bound=Decimal("20"), label="HIGH"),
            ThresholdBand(upper_bound=Decimal("30"), label="EXTREME"),
            ThresholdBand(upper_bound=None, label="SUPER_EXTREME"),
        ),
        threshold_comparison_policy="strict",
        warm_up_policy="require_full_window",
        gap_policy="defer_until_resolved",
        decimal_precision_policy=DecimalPrecisionPolicy(digits=2, rounding="ROUND_HALF_UP"),
    )
    with pytest.raises(ValueError):
        make_definition(volatility=extra)


# --- evidence normalization (§8a) -------------------------------------------


def test_evidence_normalization_is_order_independent(allocator: SequenceAllocator) -> None:
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    ordered = normalize_evidence(candles, expected_count=3)
    shuffled = [candles[2], candles[0], candles[1]]
    assert normalize_evidence(shuffled, expected_count=3) == ordered
    assert ordered == tuple(c.ref for c in candles)


def test_classified_fact_evidence_refs_match_canonical_normalization(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    for c in candles[:-1]:
        engine.on_candle(c)
    events = engine.on_candle(candles[-1])
    fact = only_classified(events[0])
    assert len(fact.candle_evidence_refs) == 3
    assert fact.candle_evidence_refs == normalize_evidence(candles, expected_count=3)


# --- Finding 5 (P3-RGE-EVID-A-MIN-05): evidence cardinality/integrity ------
#
# One EventRecordRef must resolve exactly one authoritative CandleFact
# representation: same ref + a CandleFact differing in ANY semantic/
# event-record field (scope, ohlcv, recorded_time, is_correction — ref is
# already equal by construction) fails closed. The comparison is full
# CandleFact structural equality, never narrowed to OHLCV alone.


def test_normalize_evidence_valid_window_produces_exact_cardinality(allocator: SequenceAllocator) -> None:
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    refs = normalize_evidence(candles, expected_count=3)
    assert len(refs) == 3


def test_normalize_evidence_same_ref_fully_identical_candle_dedupes(
    allocator: SequenceAllocator,
) -> None:
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    duplicate_of_first = CandleFact(
        candles[0].scope,
        candles[0].ohlcv,
        candles[0].recorded_time,
        candles[0].ref,
        candles[0].is_correction,
    )
    assert duplicate_of_first == candles[0]  # fully identical representation, not merely same ref
    refs = normalize_evidence([*candles, duplicate_of_first], expected_count=3)
    assert len(refs) == 3
    assert refs == tuple(c.ref for c in candles)


def test_normalize_evidence_insufficient_unique_evidence_fails_closed(allocator: SequenceAllocator) -> None:
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    duplicate_of_first = CandleFact(candles[0].scope, candles[0].ohlcv, candles[0].recorded_time, candles[0].ref)
    # Only 3 unique refs resolve, but 4 were declared expected — a collision-caused shortfall.
    with pytest.raises(EvidenceCardinalityError):
        normalize_evidence([*candles, duplicate_of_first], expected_count=4)


def test_normalize_evidence_same_ref_different_ohlcv_fails_closed(allocator: SequenceAllocator) -> None:
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    conflicting = CandleFact(
        candles[0].scope,
        OHLCV(Decimal("999"), Decimal("999"), Decimal("999"), Decimal("999"), Decimal("1")),
        candles[0].recorded_time,
        candles[0].ref,  # same ref, different OHLCV content
    )
    with pytest.raises(EvidenceReferenceConflictError):
        normalize_evidence([*candles, conflicting], expected_count=3)


def test_normalize_evidence_same_ref_same_ohlcv_different_recorded_time_fails_closed(
    allocator: SequenceAllocator,
) -> None:
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    conflicting = CandleFact(
        candles[0].scope,
        candles[0].ohlcv,
        candles[0].recorded_time + timedelta(seconds=1),  # only recorded_time differs
        candles[0].ref,
    )
    with pytest.raises(EvidenceReferenceConflictError):
        normalize_evidence([*candles, conflicting], expected_count=3)


def test_normalize_evidence_same_ref_same_ohlcv_different_scope_fails_closed(allocator: SequenceAllocator) -> None:
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    conflicting = CandleFact(
        CandleScope(
            "OTHER-INSTRUMENT",
            candles[0].scope.venue_id,
            candles[0].scope.timeframe,
            candles[0].scope.window_start,
            candles[0].scope.window_end,
        ),
        candles[0].ohlcv,
        candles[0].recorded_time,
        candles[0].ref,  # only scope differs
    )
    with pytest.raises(EvidenceReferenceConflictError):
        normalize_evidence([*candles, conflicting], expected_count=3)


def test_normalize_evidence_same_ref_same_ohlcv_different_is_correction_fails_closed(
    allocator: SequenceAllocator,
) -> None:
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    conflicting = CandleFact(
        candles[0].scope,
        candles[0].ohlcv,
        candles[0].recorded_time,
        candles[0].ref,
        not candles[0].is_correction,  # only is_correction differs
    )
    with pytest.raises(EvidenceReferenceConflictError):
        normalize_evidence([*candles, conflicting], expected_count=3)


# --- duplicate computation idempotency --------------------------------------


def test_duplicate_candle_resubmission_is_idempotent(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    for i in range(3):
        engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    duplicate = candle_at(allocator, 2, high="10", low="9")  # same subject_id, same content, fresh ref
    assert engine.on_candle(duplicate) == []


# --- correction lineage (§10) ------------------------------------------------


def test_correction_invalidates_and_replaces(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    original = only_classified(events[0])
    assert original.class_label == "LOW"

    correction = candle_at(allocator, 1, high="20", low="9", is_correction=True, recorded_offset_seconds=120)
    events = engine.on_candle(correction)

    assert len(events) == 2
    invalidation, replacement = events
    assert isinstance(invalidation, RegimeFactInvalidated)
    assert isinstance(replacement, RegimeClassified)
    assert invalidation.invalidated_fact_ref == original.ref
    assert invalidation.scope == original.scope
    assert invalidation.window_start == original.window_start
    assert invalidation.window_end == original.window_end
    assert original.ref in invalidation.causation_refs
    assert correction.ref in invalidation.causation_refs
    assert replacement.supersedes_fact_ref == original.ref
    assert replacement.window_start == original.window_start
    assert replacement.window_end == original.window_end
    assert replacement.class_label == "HIGH"  # range now 20-9=11
    assert replacement.computed_metric == Decimal("11.00")


def test_correction_replaces_even_when_class_and_metric_unchanged(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    original = only_classified(events[0])

    # Correct volume only — RangeFormula never reads volume, so the recomputed
    # metric/class are bit-for-bit identical; regime.md §10 still mandates a
    # replacement because the evidence lineage (Candle event refs) changed.
    correction = candle_at(
        allocator, 1, high="10", low="9", volume="2", is_correction=True, recorded_offset_seconds=120
    )
    events = engine.on_candle(correction)

    assert len(events) == 2
    invalidation, replacement = events
    assert isinstance(invalidation, RegimeFactInvalidated)
    assert isinstance(replacement, RegimeClassified)
    assert replacement.class_label == original.class_label == "LOW"
    assert replacement.computed_metric == original.computed_metric == Decimal("1.00")
    assert replacement.supersedes_fact_ref == original.ref
    assert replacement.ref != original.ref


def test_one_correction_affects_all_overlapping_windows_independently(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    originals: list[RegimeClassified] = []
    for i in range(5):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
        originals.extend(e for e in events if isinstance(e, RegimeClassified))
    assert len(originals) == 3  # windows ending at index 2, 3, 4

    # index 2 is shared by all three windows: [0,1,2], [1,2,3], [2,3,4].
    correction = candle_at(allocator, 2, high="30", low="9", is_correction=True, recorded_offset_seconds=180)
    events = engine.on_candle(correction)

    assert len(events) == 6
    kinds = [type(e).__name__ for e in events]
    assert kinds == [
        "RegimeFactInvalidated",
        "RegimeClassified",
        "RegimeFactInvalidated",
        "RegimeClassified",
        "RegimeFactInvalidated",
        "RegimeClassified",
    ]
    replacements = [e for e in events if isinstance(e, RegimeClassified)]
    assert [r.window_end for r in replacements] == sorted(r.window_end for r in replacements)
    assert {r.supersedes_fact_ref for r in replacements} == {o.ref for o in originals}
    assert all(r.class_label == "EXTREME" for r in replacements)  # range now 30-9=21


# --- RegimeCurrentView (§11): lineage invariants, pending-correction, no fallback ---


def test_view_rejects_duplicate_original_for_same_window(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    fact = only_classified(events[0])

    view = RegimeCurrentView(scope)
    view.on_regime_classified(fact)
    with pytest.raises(RegimeLineageError):
        view.on_regime_classified(fact)


def test_view_rejects_invalidation_targeting_wrong_head(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    fact = only_classified(events[0])

    view = RegimeCurrentView(scope)
    view.on_regime_classified(fact)
    bogus_ref = allocator.next_ref("regime")
    bogus_invalidation = RegimeFactInvalidated(
        scope=fact.scope,
        invalidated_fact_ref=bogus_ref,
        window_start=fact.window_start,
        window_end=fact.window_end,
        causation_refs=(),
        recorded_time=fact.recorded_time,
        ref=allocator.next_ref("regime"),
    )
    with pytest.raises(RegimeLineageError):
        view.on_regime_invalidated(bogus_invalidation)


def test_view_rejects_replacement_before_invalidation_visible(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    original = only_classified(events[0])
    correction = candle_at(allocator, 1, high="20", low="9", is_correction=True, recorded_offset_seconds=120)
    _invalidation, replacement = engine.on_candle(correction)

    view = RegimeCurrentView(scope)
    view.on_regime_classified(original)
    with pytest.raises(RegimeLineageError):
        view.on_regime_classified(only_classified(replacement))  # invalidation not yet fed


def test_view_rejects_double_invalidation(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    original = only_classified(events[0])
    correction = candle_at(allocator, 1, high="20", low="9", is_correction=True, recorded_offset_seconds=120)
    invalidation, _replacement = engine.on_candle(correction)
    invalidation = only_invalidated(invalidation)

    view = RegimeCurrentView(scope)
    view.on_regime_classified(original)
    view.on_regime_invalidated(invalidation)
    with pytest.raises(RegimeLineageError):
        view.on_regime_invalidated(invalidation)


# --- Finding 4 (P3-RGE-VIEW-A-MAJ-04): RegimeCurrentView schema conformance ---


def test_view_result_full_schema_when_valid(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    fact = only_classified(events[0])

    view = RegimeCurrentView(scope)
    view.on_regime_classified(fact)
    result = current_result(view)
    assert result.regime_subject_id == scope.regime_subject_id
    assert result.scope == scope
    assert result.view_state == "VALID"
    assert result.class_label == fact.class_label
    assert result.computed_metric == fact.computed_metric
    assert result.analysis_window == AnalysisWindow(fact.window_start, fact.window_end)
    assert result.lineage_head_fact_ref == fact.ref
    assert result.last_recorded_time == fact.recorded_time


def test_view_result_pending_correction_fields_absent(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    original = only_classified(events[0])
    correction = candle_at(allocator, 1, high="20", low="9", is_correction=True, recorded_offset_seconds=120)
    invalidation, _replacement = engine.on_candle(correction)
    invalidation = only_invalidated(invalidation)

    view = RegimeCurrentView(scope)
    view.on_regime_classified(original)
    view.on_regime_invalidated(invalidation)
    result = current_result(view)
    assert result.view_state == "PENDING_CORRECTION"
    assert result.class_label is None
    assert result.computed_metric is None
    assert result.analysis_window is None
    assert result.lineage_head_fact_ref is None
    assert result.last_recorded_time == invalidation.recorded_time


def test_view_last_recorded_time_transitions(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    original = only_classified(events[0])

    view = RegimeCurrentView(scope)
    view.on_regime_classified(original)
    assert current_result(view).last_recorded_time == original.recorded_time

    correction = candle_at(allocator, 1, high="20", low="9", is_correction=True, recorded_offset_seconds=120)
    invalidation, replacement = engine.on_candle(correction)
    invalidation = only_invalidated(invalidation)
    replacement = only_classified(replacement)

    view.on_regime_invalidated(invalidation)
    assert current_result(view).last_recorded_time == invalidation.recorded_time

    view.on_regime_classified(replacement)
    assert current_result(view).last_recorded_time == replacement.recorded_time


def test_view_pending_correction_then_valid_again(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    original = only_classified(events[0])

    view = RegimeCurrentView(scope)
    view.on_regime_classified(original)
    assert current_result(view).view_state == "VALID"
    assert current_result(view).class_label == "LOW"

    correction = candle_at(allocator, 1, high="20", low="9", is_correction=True, recorded_offset_seconds=120)
    invalidation, replacement = engine.on_candle(correction)

    view.on_regime_invalidated(only_invalidated(invalidation))
    pending = current_result(view)
    assert pending.view_state == "PENDING_CORRECTION"
    assert pending.class_label is None
    assert pending.computed_metric is None
    assert pending.analysis_window is None

    view.on_regime_classified(only_classified(replacement))
    resolved = current_result(view)
    assert resolved.view_state == "VALID"
    assert resolved.class_label == "HIGH"
    assert resolved.computed_metric == Decimal("11.00")


def test_view_never_falls_back_to_older_still_valid_window(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)

    factA_events: list[RegimeEvent] = []
    for i in range(4):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
        factA_events.extend(events)
    fact_a, fact_b = (only_classified(e) for e in factA_events)  # windows [0,1,2] then [1,2,3]
    assert fact_b.window_end > fact_a.window_end

    view = RegimeCurrentView(scope)
    view.on_regime_classified(fact_a)
    view.on_regime_classified(fact_b)

    # Correcting index 3 only affects window B ([1,2,3]); window A stays VALID.
    correction = candle_at(allocator, 3, high="30", low="9", is_correction=True)
    invalidation, _replacement = engine.on_candle(correction)
    view.on_regime_invalidated(only_invalidated(invalidation))

    result = current_result(view)
    # If the view had incorrectly fallen back to window A, this would read
    # VALID (window A never invalidated) instead of PENDING_CORRECTION.
    assert result.view_state == "PENDING_CORRECTION"
    assert result.last_recorded_time == only_invalidated(invalidation).recorded_time


def test_view_reconstruction_from_full_event_replay_matches_incremental(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)

    all_events: list[RegimeEvent] = []
    for i in range(5):
        all_events.extend(engine.on_candle(candle_at(allocator, i, high="10", low="9")))
    correction = candle_at(allocator, 2, high="30", low="9", is_correction=True, recorded_offset_seconds=180)
    all_events.extend(engine.on_candle(correction))
    assert len(all_events) == 9  # 3 originals + (invalidate+replace) x 3

    def _rebuild(events: list[RegimeEvent]) -> RegimeCurrentView:
        view = RegimeCurrentView(scope)
        for event in events:
            if isinstance(event, RegimeClassified):
                view.on_regime_classified(event)
            else:
                view.on_regime_invalidated(event)
        return view

    incremental = _rebuild(all_events)
    rebuilt_from_log = _rebuild(list(all_events))  # a fresh view fed the exact same recorded event log
    assert incremental.current() == rebuilt_from_log.current()


# --- historical/backtest cadence, no look-ahead ------------------------------


def test_historical_batch_emits_every_completed_window_in_cadence(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)

    emitted: list[RegimeClassified] = []
    for i in range(6):
        events = engine.on_candle(candle_at(allocator, i, high=str(10 + i), low="9"))
        if i < 2:
            assert events == []
        else:
            assert len(events) == 1
            fact = only_classified(events[0])
            emitted.append(fact)
            assert len(fact.candle_evidence_refs) == 3  # never more than window_candle_count

    assert len(emitted) == 4  # 6 candles, window=3 -> 4 completed windows
    window_ends = [f.window_end for f in emitted]
    assert window_ends == sorted(window_ends)
    assert len(set(window_ends)) == 4  # sequential cadence, never jumps/repeats


# --- ordering discipline, scope isolation ------------------------------------


def test_recorded_time_ordering_is_per_engine_not_global(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    definition = make_definition(volatility=volatility_definition())
    scope_a = regime_scope("volatility", instrument_id="AAA-USD")
    scope_b = regime_scope("volatility", instrument_id="BBB-USD")
    engine_a = RegimeEngine(scope_a, definition, RangeFormula(), allocator, time_source)
    engine_b = RegimeEngine(scope_b, definition, RangeFormula(), allocator, time_source)

    candle_a0 = candle_at(allocator, 0, high="10", low="9", instrument_id="AAA-USD", recorded_offset_seconds=100)
    engine_a.on_candle(candle_a0)

    # engine_b has never seen a candle — its own ordering state is independent
    # of engine_a's, even though candle_a0's recorded_time is far later.
    candle_b0 = candle_at(allocator, 0, high="10", low="9", instrument_id="BBB-USD", recorded_offset_seconds=0)
    engine_b.on_candle(candle_b0)  # must not raise

    candle_a1 = candle_at(allocator, 1, high="10", low="9", instrument_id="AAA-USD", recorded_offset_seconds=0)
    with pytest.raises(NonMonotonicRecordedTimeError):
        engine_a.on_candle(candle_a1)


def test_foreign_scope_fails_closed(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator, time_source)
    foreign_candle = candle_at(allocator, 0, high="10", low="9", instrument_id="ETH-USDT")
    with pytest.raises(ForeignScopeError):
        engine.on_candle(foreign_candle)

    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    fact = only_classified(events[0])
    foreign_fact = dataclasses.replace(fact, scope=regime_scope("volatility", instrument_id="ETH-USDT"))
    view = RegimeCurrentView(scope)
    with pytest.raises(ForeignScopeError):
        view.on_regime_classified(foreign_fact)


# --- deterministic replay -----------------------------------------------------


def test_deterministic_replay_across_fresh_engines(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    candles = [candle_at(allocator, i, high=str(10 + i), low="9") for i in range(5)]

    engine_a = RegimeEngine(
        scope,
        definition,
        RangeFormula(),
        SequenceAllocator("raw-regime-engine", "0.1.0", "replay-run"),
        time_source,
    )
    engine_b = RegimeEngine(
        scope,
        definition,
        RangeFormula(),
        SequenceAllocator("raw-regime-engine", "0.1.0", "replay-run"),
        time_source,
    )

    events_a = [event for c in candles for event in engine_a.on_candle(c)]
    events_b = [event for c in candles for event in engine_b.on_candle(c)]

    assert events_a == events_b
    assert len(events_a) > 0


# --- structural independence from Structure Engine ---------------------------


def test_no_structure_engine_import() -> None:
    package_dir = pathlib.Path(raw_regime_engine.__file__).parent
    import_pattern = re.compile(r"^\s*(import|from)\s+structure_engine\b", re.MULTILINE)
    for path in package_dir.rglob("*.py"):
        content = path.read_text()
        assert not import_pattern.search(content), f"{path} imports structure_engine"


# --- identity -----------------------------------------------------------------


def test_regime_subject_id_is_deterministic_and_scope_specific() -> None:
    scope_1 = regime_scope("volatility")
    scope_2 = regime_scope("volatility")
    scope_3 = regime_scope("directional_persistence")
    assert scope_1.regime_subject_id == scope_2.regime_subject_id
    assert scope_1.regime_subject_id != scope_3.regime_subject_id
