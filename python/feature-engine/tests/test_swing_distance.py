from __future__ import annotations

import dataclasses
from datetime import timedelta
from decimal import Decimal
from typing import Any

import pytest
from conftest import (
    BASE,
    CONTRACT_VERSION,
    FixedDeltaTimeSource,
    candle_at,
    feature_scope,
    make_distance_definition,
    only_computed,
    swing_confirmed_at,
    swing_invalidated_at,
)

from feature_engine import (
    CANDLE_CORRECTED_CONTRACT_ID,
    EventContractRef,
    SequenceAllocator,
    SwingDistanceFeatureEngine,
)
from feature_engine.errors import (
    EvidenceReferenceConflictError,
    InvalidSwingEligibilityInputError,
    UnauthorizedUpstreamContractError,
    UnsupportedDistanceRepresentationError,
)


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
    # pivot at index 2 (well before cutoff), but recorded very late relative to its own effective time
    # (still comfortably before the reference candle's own recorded_time / computation cursor).
    late_recorded = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", recorded_offset_minutes=100)
    engine.on_swing_confirmed(late_recorded)
    reference = candle_at(allocator, 10, high="110", low="90", close="105", recorded_offset_seconds=5700)
    events = engine.on_candle(reference)
    assert len(events) == 1


# --- P3-FEATURE-A-MAJ-06 remediation: explicit machine-enforced cursor -------


def test_swing_recorded_after_computation_cursor_excluded(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Effective-time eligible (pivot well before window_end), but the Swing's own
    recorded_time is AFTER the reference Candle's own recorded_time (the explicit
    computation cursor `R`) — must be excluded, never selected just because it
    happens to already be sitting in the engine's in-memory state.
    """
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    not_yet_visible = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", recorded_offset_minutes=10_000)
    assert not_yet_visible.recorded_time > reference.recorded_time
    engine.on_swing_confirmed(not_yet_visible)
    assert engine.on_candle(reference) == []


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
    engine.on_swing_invalidated(
        swing_invalidated_at(allocator, swing_id="s1", swing_revision=1, recorded_time=BASE + timedelta(minutes=4))
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


# --- P3-FEATURE-A-MAJ-01 remediation: signed fails closed, absolute unaffected


def test_signed_distance_representation_fails_closed_at_construction(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    with pytest.raises(UnsupportedDistanceRepresentationError):
        _engine(allocator, time_source, distance_representation="signed")


def test_absolute_distance_computed_with_evidence_refs(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    absolute_engine = _engine(allocator, time_source, distance_representation="absolute")
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="110")
    absolute_engine.on_swing_confirmed(swing)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    computed = only_computed(absolute_engine.on_candle(reference)[0])
    assert computed.value == Decimal("5.00")  # |105 - 110|
    assert set(computed.input_fact_refs) == {reference.ref, swing.ref}


def test_no_eligible_swing_is_valid_absence(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    assert engine.on_candle(reference) == []


# --- P3-FEATURE-A-MAJ-04 remediation: revision N+1 requires explicit invalidation of N


def test_revision_two_before_invalidation_of_revision_one_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    engine.on_swing_confirmed(swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=1))
    with pytest.raises(InvalidSwingEligibilityInputError):
        engine.on_swing_confirmed(
            swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=2, recorded_offset_minutes=5)
        )


def test_revision_skip_after_invalidation_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    engine.on_swing_confirmed(swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=1))
    engine.on_swing_invalidated(
        swing_invalidated_at(allocator, swing_id="s1", swing_revision=1, recorded_time=BASE + timedelta(minutes=4))
    )
    with pytest.raises(InvalidSwingEligibilityInputError):
        engine.on_swing_confirmed(
            swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=3, recorded_offset_minutes=5)
        )


def test_first_seen_revision_must_be_one(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    with pytest.raises(InvalidSwingEligibilityInputError):
        engine.on_swing_confirmed(swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=2))


def test_pending_window_resolved_by_newly_visible_replacement_revision(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """A window left PENDING_CORRECTION (no eligible Swing existed right after
    invalidation) must be re-evaluated and resolved once a replacement revision
    later becomes visible via `on_swing_confirmed` — not only via
    `on_swing_invalidated`'s own immediate reattempt.
    """
    engine = _engine(allocator, time_source)
    engine.on_swing_confirmed(
        swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=1, pivot_price="100")
    )
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    original = only_computed(engine.on_candle(reference)[0])
    assert original.value == Decimal("5.00")

    invalidation_events = engine.on_swing_invalidated(
        swing_invalidated_at(allocator, swing_id="s1", swing_revision=1, recorded_time=BASE + timedelta(minutes=20))
    )
    assert len(invalidation_events) == 1  # invalidation only — no other eligible Swing exists yet

    replacement_events = engine.on_swing_confirmed(
        swing_confirmed_at(
            allocator, pivot_index=2, swing_id="s1", swing_revision=2, pivot_price="102", recorded_offset_minutes=25
        )
    )
    assert len(replacement_events) == 1
    replacement = only_computed(replacement_events[0])
    assert replacement.value == Decimal("3.00")  # 105 - 102
    assert replacement.supersedes_fact_ref == original.ref
    assert replacement.window_start == original.window_start
    assert replacement.window_end == original.window_end


# --- P3-FEATURE-A-MAJ-02 remediation: contract qualification -----------------


def test_unauthorized_candle_contract_id_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    bad = dataclasses.replace(reference, event_contract_ref=EventContractRef("candle-observed", CONTRACT_VERSION))
    with pytest.raises(UnauthorizedUpstreamContractError):
        engine.on_candle(bad)


def test_unauthorized_swing_contract_id_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1")
    bad = dataclasses.replace(swing, event_contract_ref=EventContractRef("swing-candidate-detected", CONTRACT_VERSION))
    with pytest.raises(UnauthorizedUpstreamContractError):
        engine.on_swing_confirmed(bad)


# --- P3-FEATURE-A-MAJ-05 remediation: dedup is ref-identity-only -------------


def test_candle_distinct_correction_ref_enters_lineage_even_when_value_unchanged(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    engine.on_swing_confirmed(swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100"))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    original = only_computed(engine.on_candle(reference)[0])

    correction = dataclasses.replace(
        reference,
        ref=allocator.next_ref("candle"),
        recorded_time=reference.recorded_time + timedelta(seconds=120),
        is_correction=True,
        event_contract_ref=EventContractRef(CANDLE_CORRECTED_CONTRACT_ID, CONTRACT_VERSION),
    )
    events = engine.on_candle(correction)
    assert len(events) == 2
    replacement = only_computed(events[1])
    assert replacement.value == original.value
    assert replacement.supersedes_fact_ref == original.ref
    assert replacement.ref != original.ref


def test_candle_same_ref_different_content_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    engine.on_candle(reference)
    conflicting = dataclasses.replace(reference, ohlcv=dataclasses.replace(reference.ohlcv, high=Decimal("999")))
    with pytest.raises(EvidenceReferenceConflictError):
        engine.on_candle(conflicting)


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
