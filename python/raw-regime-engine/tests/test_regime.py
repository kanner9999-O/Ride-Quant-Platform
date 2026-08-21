from __future__ import annotations

import dataclasses
import pathlib
import re
from decimal import Decimal

import pytest
from conftest import (
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
    DecimalPrecisionPolicy,
    RegimeClassified,
    RegimeCurrentView,
    RegimeDimensionDefinition,
    RegimeEngine,
    RegimeEvent,
    RegimeFactInvalidated,
    SequenceAllocator,
    ThresholdBand,
    normalize_evidence,
)
from raw_regime_engine.errors import (
    ForeignScopeError,
    FormulaMismatchError,
    NonMonotonicRecordedTimeError,
    RegimeLineageError,
)

# --- warm-up / every-completed-window emission -----------------------------


def test_warm_up_is_valid_absence_not_error(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)

    c0 = candle_at(allocator, 0, high="10", low="9")
    c1 = candle_at(allocator, 1, high="10", low="9")
    assert engine.on_candle(c0) == []
    assert engine.on_candle(c1) == []


def test_every_completed_window_emits_including_identical_class(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)

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
    fact_2, fact_3 = events_2[0], events_3[0]
    assert isinstance(fact_2, RegimeClassified) and isinstance(fact_3, RegimeClassified)
    assert fact_2.class_label == "LOW"
    assert fact_3.class_label == "LOW"
    assert fact_2.computed_metric == Decimal("1.00") == fact_3.computed_metric
    assert fact_2.supersedes_fact_ref is None
    assert fact_3.supersedes_fact_ref is None
    assert (fact_2.window_start, fact_2.window_end) != (fact_3.window_start, fact_3.window_end)
    assert fact_2.ref != fact_3.ref


def test_both_dimensions_classify_independently(allocator: SequenceAllocator) -> None:
    vol_scope = regime_scope("volatility")
    dp_scope = regime_scope("directional_persistence")
    definition = make_definition(
        volatility=volatility_definition(), directional_persistence=directional_persistence_definition()
    )
    vol_engine = RegimeEngine(vol_scope, definition, RangeFormula(), allocator)
    dp_engine = RegimeEngine(dp_scope, definition, SumCloseFormula(), allocator)

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


def test_threshold_boundary_strict_moves_to_next_band(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition(window_candle_count=1, comparison="strict"))
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)
    c0 = candle_at(allocator, 0, high="10", low="5")  # range == 5, exactly the LOW upper bound
    fact = only_classified(engine.on_candle(c0)[0])
    assert fact.computed_metric == Decimal("5.00")
    assert fact.class_label == "NORMAL"  # strict: 5 < 5 is False -> falls through to NORMAL


def test_threshold_boundary_inclusive_stays_in_band(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition(window_candle_count=1, comparison="inclusive"))
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)
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


def test_formula_id_mismatch_fails_closed(allocator: SequenceAllocator) -> None:
    class WrongFormula:
        formula_id = "not-the-configured-formula"

        def compute(self, evidence: object) -> Decimal:
            return Decimal(0)

    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    with pytest.raises(FormulaMismatchError):
        RegimeEngine(scope, definition, WrongFormula(), allocator)


def test_test_only_formula_injection_drives_classification(allocator: SequenceAllocator) -> None:
    scope = regime_scope("directional_persistence")
    definition = make_definition(directional_persistence=directional_persistence_definition())
    formula = SumCloseFormula()
    assert formula.formula_id.startswith("test-"), "test-only formulas must not look like production ids"
    engine = RegimeEngine(scope, definition, formula, allocator)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="10", close="10"))
    fact = only_classified(events[0])
    assert fact.computed_metric == Decimal("30.00")
    assert fact.class_label == "NON_DIRECTIONAL"


def test_regime_definition_rejects_label_outside_dimension_vocabulary() -> None:
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


# --- evidence normalization (§8a) -------------------------------------------


def test_evidence_normalization_is_order_independent(allocator: SequenceAllocator) -> None:
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    ordered = normalize_evidence(candles)
    shuffled = [candles[2], candles[0], candles[1]]
    assert normalize_evidence(shuffled) == ordered
    assert ordered == tuple(c.ref for c in candles)


def test_classified_fact_evidence_refs_match_canonical_normalization(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    for c in candles[:-1]:
        engine.on_candle(c)
    events = engine.on_candle(candles[-1])
    fact = only_classified(events[0])
    assert len(fact.candle_evidence_refs) == 3
    assert fact.candle_evidence_refs == normalize_evidence(candles)


# --- duplicate computation idempotency --------------------------------------


def test_duplicate_candle_resubmission_is_idempotent(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)
    for i in range(3):
        engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    duplicate = candle_at(allocator, 2, high="10", low="9")  # same subject_id, same content, fresh ref
    assert engine.on_candle(duplicate) == []


# --- correction lineage (§10) ------------------------------------------------


def test_correction_invalidates_and_replaces(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)
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


def test_correction_replaces_even_when_class_and_metric_unchanged(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)
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


def test_one_correction_affects_all_overlapping_windows_independently(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)
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


def test_view_rejects_duplicate_original_for_same_window(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    fact = only_classified(events[0])

    view = RegimeCurrentView(scope)
    view.on_regime_classified(fact)
    with pytest.raises(RegimeLineageError):
        view.on_regime_classified(fact)


def test_view_rejects_invalidation_targeting_wrong_head(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)
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


def test_view_rejects_replacement_before_invalidation_visible(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    original = only_classified(events[0])
    correction = candle_at(allocator, 1, high="20", low="9", is_correction=True, recorded_offset_seconds=120)
    _invalidation, replacement = engine.on_candle(correction)

    view = RegimeCurrentView(scope)
    view.on_regime_classified(original)
    with pytest.raises(RegimeLineageError):
        view.on_regime_classified(only_classified(replacement))  # invalidation not yet fed


def test_view_rejects_double_invalidation(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)
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


def test_view_pending_correction_then_valid_again(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)
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
    assert pending.window_start == original.window_start
    assert pending.window_end == original.window_end

    view.on_regime_classified(only_classified(replacement))
    resolved = current_result(view)
    assert resolved.view_state == "VALID"
    assert resolved.class_label == "HIGH"
    assert resolved.computed_metric == Decimal("11.00")


def test_view_never_falls_back_to_older_still_valid_window(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)

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
    assert result.view_state == "PENDING_CORRECTION"
    assert result.window_start == fact_b.window_start
    assert result.window_end == fact_b.window_end


# --- historical/backtest cadence, no look-ahead ------------------------------


def test_historical_batch_emits_every_completed_window_in_cadence(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)

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


def test_recorded_time_ordering_is_per_engine_not_global(allocator: SequenceAllocator) -> None:
    definition = make_definition(volatility=volatility_definition())
    scope_a = regime_scope("volatility", instrument_id="AAA-USD")
    scope_b = regime_scope("volatility", instrument_id="BBB-USD")
    engine_a = RegimeEngine(scope_a, definition, RangeFormula(), allocator)
    engine_b = RegimeEngine(scope_b, definition, RangeFormula(), allocator)

    candle_a0 = candle_at(allocator, 0, high="10", low="9", instrument_id="AAA-USD", recorded_offset_seconds=100)
    engine_a.on_candle(candle_a0)

    # engine_b has never seen a candle — its own ordering state is independent
    # of engine_a's, even though candle_a0's recorded_time is far later.
    candle_b0 = candle_at(allocator, 0, high="10", low="9", instrument_id="BBB-USD", recorded_offset_seconds=0)
    engine_b.on_candle(candle_b0)  # must not raise

    candle_a1 = candle_at(allocator, 1, high="10", low="9", instrument_id="AAA-USD", recorded_offset_seconds=0)
    with pytest.raises(NonMonotonicRecordedTimeError):
        engine_a.on_candle(candle_a1)


def test_foreign_scope_fails_closed(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    engine = RegimeEngine(scope, definition, RangeFormula(), allocator)
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


def test_deterministic_replay_across_fresh_engines(allocator: SequenceAllocator) -> None:
    scope = regime_scope("volatility")
    definition = make_definition(volatility=volatility_definition())
    candles = [candle_at(allocator, i, high=str(10 + i), low="9") for i in range(5)]

    engine_a = RegimeEngine(
        scope, definition, RangeFormula(), SequenceAllocator("raw-regime-engine", "0.1.0", "replay-run")
    )
    engine_b = RegimeEngine(
        scope, definition, RangeFormula(), SequenceAllocator("raw-regime-engine", "0.1.0", "replay-run")
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
