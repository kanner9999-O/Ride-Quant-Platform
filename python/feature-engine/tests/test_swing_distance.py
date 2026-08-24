from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from typing import Any

from conftest import (
    BASE,
    FixedDeltaTimeSource,
    candle_at,
    feature_scope,
    make_distance_definition,
    only_computed,
    swing_confirmed_at,
    swing_invalidated_at,
)

from feature_engine import SequenceAllocator, SwingDistanceFeatureEngine


def _engine(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource, **definition_kwargs: Any
) -> SwingDistanceFeatureEngine:
    definition = make_distance_definition(**definition_kwargs)
    scope = feature_scope("distance_to_last_confirmed_swing", version=definition.feature_definition_version)
    return SwingDistanceFeatureEngine(scope, definition, allocator, time_source)


# --- 7. Swing effective cutoff ------------------------------------------------


def test_pivot_before_window_end_eligible(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    engine.on_swing_confirmed(swing_confirmed_at(allocator, pivot_index=8, swing_id="s1", pivot_price="100"))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    events = engine.on_candle(reference)
    assert len(events) == 1
    assert only_computed(events[0]).value == Decimal("5.00")  # 105 - 100


def test_pivot_exactly_equal_window_end_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    engine.on_swing_confirmed(swing_confirmed_at(allocator, pivot_index=11, swing_id="s1"))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    assert engine.on_candle(reference) == []


def test_pivot_after_window_end_rejected(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    engine.on_swing_confirmed(swing_confirmed_at(allocator, pivot_index=12, swing_id="s1"))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    assert engine.on_candle(reference) == []


# --- 8. Recorded-time / effective-time independence --------------------------


def test_late_recorded_old_effective_swing_still_eligible(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    # pivot at index 2 (well before cutoff), but recorded very late relative to its own effective time.
    late_recorded = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", recorded_offset_minutes=100)
    engine.on_swing_confirmed(late_recorded)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    events = engine.on_candle(reference)
    assert len(events) == 1


def test_early_visible_future_effective_swing_remains_ineligible(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    # pivot AFTER the reference candle's own window_end (future-effective), even though it is
    # "visible" (ingested) before the candle is processed.
    future_effective = swing_confirmed_at(allocator, pivot_index=15, swing_id="s1")
    engine.on_swing_confirmed(future_effective)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    assert engine.on_candle(reference) == []


# --- 9. Eligible Swing revision -----------------------------------------------


def test_latest_valid_revision_selected(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    engine.on_swing_confirmed(
        swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=1, pivot_price="100")
    )
    engine.on_swing_confirmed(
        swing_confirmed_at(
            allocator, pivot_index=2, swing_id="s1", swing_revision=2, pivot_price="102", recorded_offset_minutes=5
        )
    )
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    computed = only_computed(engine.on_candle(reference)[0])
    assert computed.value == Decimal("3.00")  # 105 - 102 (revision 2's price), not 105-100


def test_invalidated_revision_excluded(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    engine.on_swing_confirmed(swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100"))
    invalidated_at = BASE + timedelta(minutes=3)
    engine.on_swing_invalidated(
        swing_invalidated_at(allocator, swing_id="s1", swing_revision=1, recorded_time=invalidated_at)
    )
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    assert engine.on_candle(reference) == []


# --- 10. Total-order deterministic tie-break ----------------------------------


def test_total_order_prefers_latest_pivot_window_start(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    engine.on_swing_confirmed(swing_confirmed_at(allocator, pivot_index=2, swing_id="s_old", pivot_price="90"))
    engine.on_swing_confirmed(swing_confirmed_at(allocator, pivot_index=5, swing_id="s_new", pivot_price="95"))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    computed = only_computed(engine.on_candle(reference)[0])
    # criterion 1 (pivot_effective_time.window_start DESC) picks s_new (index 5 > index 2).
    assert computed.value == Decimal("10.00")  # 105 - 95


# --- 11. Distance arithmetic ---------------------------------------------------


def test_distance_signed_and_absolute_and_evidence_refs(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    signed_engine = _engine(allocator, time_source, distance_representation="signed")
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="110")
    signed_engine.on_swing_confirmed(swing)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    computed = only_computed(signed_engine.on_candle(reference)[0])
    assert computed.value == Decimal("-5.00")  # 105 - 110, signed negative
    assert set(computed.input_fact_refs) == {reference.ref, swing.ref}

    allocator2 = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="test-run-2")
    absolute_engine = _engine(allocator2, FixedDeltaTimeSource(), distance_representation="absolute")
    swing2 = swing_confirmed_at(allocator2, pivot_index=2, swing_id="s1", pivot_price="110")
    absolute_engine.on_swing_confirmed(swing2)
    reference2 = candle_at(allocator2, 10, high="110", low="90", close="105")
    computed2 = only_computed(absolute_engine.on_candle(reference2)[0])
    assert computed2.value == Decimal("5.00")


def test_no_eligible_swing_is_valid_absence(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    assert engine.on_candle(reference) == []


# --- 18. Deterministic replay --------------------------------------------------


def test_deterministic_replay_same_input_different_engine_instances() -> None:
    def _build() -> tuple[SwingDistanceFeatureEngine, SequenceAllocator]:
        allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="replay-run")
        return _engine(allocator, FixedDeltaTimeSource()), allocator

    engine_a, allocator_a = _build()
    engine_b, allocator_b = _build()

    swing_a = swing_confirmed_at(allocator_a, pivot_index=2, swing_id="s1", pivot_price="100")
    swing_b = swing_confirmed_at(allocator_b, pivot_index=2, swing_id="s1", pivot_price="100")
    reference_a = candle_at(allocator_a, 10, high="110", low="90", close="105")
    reference_b = candle_at(allocator_b, 10, high="110", low="90", close="105")

    engine_a.on_swing_confirmed(swing_a)
    engine_b.on_swing_confirmed(swing_b)
    events_a = engine_a.on_candle(reference_a)
    events_b = engine_b.on_candle(reference_b)
    assert events_a == events_b
    assert len(events_a) == 1
