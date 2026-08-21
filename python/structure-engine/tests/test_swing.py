from __future__ import annotations

from decimal import Decimal

import pytest
from conftest import candle_at

from structure_engine import (
    SequenceAllocator,
    SwingCandidateDetected,
    SwingConfirmed,
    SwingDefinition,
    SwingEngine,
    SwingEvent,
    SwingInvalidated,
)
from structure_engine.errors import (
    DuplicateCandleConflictError,
    NonMonotonicRecordedTimeError,
    OutOfOrderCandleError,
    OutOfOrderCorrectionError,
)


def wick_definition(**overrides: object) -> SwingDefinition:
    params: dict[str, object] = dict(
        swing_definition_version="swd-1",
        left_count=2,
        right_count=2,
        price_basis="wick",
        equal_level_policy="first_occurrence",
    )
    params.update(overrides)
    return SwingDefinition(**params)  # type: ignore[arg-type]


def feed(engine: SwingEngine, allocator: SequenceAllocator, series: list[tuple[str, str]]) -> list[SwingEvent]:
    events: list[SwingEvent] = []
    for i, (high, low) in enumerate(series):
        events += engine.ingest_candle(candle_at(allocator, i, high=high, low=low))
    return events


class TestCandidateConfirmInvalidate:
    def test_high_pivot_candidate_then_confirmed(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        highs_lows = [("100", "90"), ("105", "95"), ("110", "100"), ("105", "95"), ("100", "90")]
        events = feed(engine, allocator, highs_lows)
        kinds = [type(e).__name__ for e in events]
        assert "SwingCandidateDetected" in kinds
        assert "SwingConfirmed" in kinds
        confirmed = [e for e in events if isinstance(e, SwingConfirmed) and e.scope.direction == "HIGH"]
        assert len(confirmed) == 1
        assert confirmed[0].pivot_price == Decimal("110")
        assert confirmed[0].swing_revision == 1
        candidate = [e for e in events if isinstance(e, SwingCandidateDetected) and e.scope.direction == "HIGH"]
        assert candidate[0].ref in confirmed[0].causation_refs

    def test_candidate_invalidated_by_market_evolution_before_confirm(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(left_count=2, right_count=3), allocator)
        # index2 is HIGH candidate (110) after index0,1 lower highs; then index3 breaks past 110
        # before the 3-candle right window can complete -> immediate market_evolution invalidation.
        series = [("100", "90"), ("105", "95"), ("110", "100"), ("115", "105")]
        events = feed(engine, allocator, series)
        high_events = [e for e in events if getattr(e.scope, "direction", None) == "HIGH"]
        assert any(isinstance(e, SwingCandidateDetected) for e in high_events)
        invalidations = [e for e in high_events if isinstance(e, SwingInvalidated)]
        assert len(invalidations) == 1
        assert invalidations[0].invalidation_cause == "market_evolution"
        assert not any(isinstance(e, SwingConfirmed) for e in high_events)

    def test_confirmed_swing_never_invalidated_by_market_evolution(self, allocator: SequenceAllocator) -> None:
        """swing.md §8: once CONFIRMED, price continuing past the pivot is NOT
        a Swing invalidation (that's Structure's BOS/CHoCH concern)."""
        engine = SwingEngine(wick_definition(), allocator)
        series = [("100", "90"), ("105", "95"), ("110", "100"), ("105", "95"), ("100", "90"), ("120", "115")]
        events = feed(engine, allocator, series)
        high_events = [e for e in events if getattr(e.scope, "direction", None) == "HIGH"]
        assert any(isinstance(e, SwingConfirmed) for e in high_events)
        assert not any(isinstance(e, SwingInvalidated) for e in high_events)


class TestPriceBasisAndEqualLevel:
    def test_close_basis_ignores_wick_excursion(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(price_basis="close"), allocator)
        # High wicks are noisy but closes form a clean pivot at index2 (close=110).
        series = [
            ("108", "90", "100"),
            ("120", "95", "105"),
            ("130", "100", "110"),
            ("120", "95", "105"),
            ("108", "90", "100"),
        ]
        events: list[object] = []
        for i, (high, low, close) in enumerate(series):
            events += engine.ingest_candle(candle_at(allocator, i, high=high, low=low, close=close))
        confirmed = [e for e in events if isinstance(e, SwingConfirmed) and e.scope.direction == "HIGH"]
        assert len(confirmed) == 1
        assert confirmed[0].pivot_price == Decimal("110")

    def test_equal_high_first_occurrence_disqualifies_later_candidate(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(equal_level_policy="first_occurrence"), allocator)
        # index1 and index2 share the SAME high (110) -> under first_occurrence the
        # earlier one (index1) would win, so index2 must NOT become a HIGH candidate.
        series = [("100", "90"), ("110", "100"), ("110", "100"), ("100", "90")]
        events = feed(engine, allocator, series)
        candidates_high = [e for e in events if isinstance(e, SwingCandidateDetected) and e.scope.direction == "HIGH"]
        idx2_subject = candle_at(allocator, 2, high="110", low="100").scope.subject_id
        # index2 (equal to index1, later) must be disqualified as a pivot under first_occurrence:
        assert not any(c.scope.pivot_candle_subject_id == idx2_subject for c in candidates_high)

    def test_equal_low_last_occurrence_disqualifies_earlier_candidate(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(equal_level_policy="last_occurrence"), allocator)
        # index1 and index2 share the SAME low (90) -> under last_occurrence the
        # later one (index2) wins, so index1 must NOT qualify as the LOW pivot
        # once index2 (a right-window tie) is seen.
        series = [("110", "100"), ("100", "90"), ("100", "90"), ("110", "100")]
        events = feed(engine, allocator, series)
        confirmed_low = [e for e in events if isinstance(e, SwingConfirmed) and e.scope.direction == "LOW"]
        idx1_subject = candle_at(allocator, 1, high="100", low="90").scope.subject_id
        assert all(c.scope.pivot_candle_subject_id != idx1_subject for c in confirmed_low)


class TestRevisionAndCorrection:
    def test_correction_to_pivot_creates_new_revision_same_swing_id(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        series = [("100", "90"), ("105", "95"), ("110", "100"), ("105", "95"), ("100", "90")]
        first_events = feed(engine, allocator, series)
        confirmed1 = next(e for e in first_events if isinstance(e, SwingConfirmed) and e.scope.direction == "HIGH")
        assert confirmed1.swing_revision == 1

        corrected = candle_at(allocator, 2, high="112", low="100", is_correction=True, recorded_offset_seconds=600)
        events2 = engine.ingest_candle(corrected)
        invalidated = [e for e in events2 if isinstance(e, SwingInvalidated)]
        confirmed2 = [e for e in events2 if isinstance(e, SwingConfirmed)]
        assert len(invalidated) == 1
        assert invalidated[0].invalidation_cause == "upstream_correction"
        assert invalidated[0].swing_revision == 1
        assert len(confirmed2) == 1
        assert confirmed2[0].swing_revision == 2
        assert confirmed2[0].pivot_price == Decimal("112")
        # same swing_id (same six-field scope, pivot_candle_subject_id unchanged)
        assert confirmed2[0].scope.swing_id == confirmed1.scope.swing_id
        assert invalidated[0].ref in confirmed2[0].causation_refs

    def test_correction_removing_pivot_status_terminates_with_no_successor(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        series = [("100", "90"), ("105", "95"), ("110", "100"), ("105", "95"), ("100", "90")]
        feed(engine, allocator, series)
        # correction makes index2's high no longer the local extreme (index1 now higher)
        corrected = candle_at(allocator, 2, high="103", low="100", is_correction=True, recorded_offset_seconds=600)
        events2 = engine.ingest_candle(corrected)
        invalidated = [e for e in events2 if isinstance(e, SwingInvalidated) and e.scope.direction == "HIGH"]
        confirmed2 = [e for e in events2 if isinstance(e, SwingConfirmed) and e.scope.direction == "HIGH"]
        assert len(invalidated) == 1
        assert invalidated[0].invalidation_cause == "upstream_correction"
        assert confirmed2 == []

    def test_correction_to_evidence_candle_no_op_when_conclusion_unchanged(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        series = [("100", "90"), ("105", "95"), ("110", "100"), ("105", "95"), ("100", "90")]
        feed(engine, allocator, series)
        # correct index0's volume only — extreme values (high/low) unchanged -> pure no-op
        corrected = candle_at(
            allocator,
            0,
            high="100",
            low="90",
            volume="999",
            is_correction=True,
            recorded_offset_seconds=600,
        )
        events2 = engine.ingest_candle(corrected)
        assert events2 == []


class TestDedupIdempotency:
    def test_identical_resubmission_is_idempotent(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        fact = candle_at(allocator, 0, high="100", low="90")
        first = engine.ingest_candle(fact)
        second = engine.ingest_candle(candle_at(allocator, 0, high="100", low="90"))
        assert first == []  # index0 alone never satisfies anything yet
        assert second == []

    def test_non_correction_conflicting_resubmission_fails_closed(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        engine.ingest_candle(candle_at(allocator, 0, high="100", low="90"))
        with pytest.raises(DuplicateCandleConflictError):
            engine.ingest_candle(candle_at(allocator, 0, high="101", low="90"))


class TestOrderingDiscipline:
    def test_out_of_order_correction_fails_closed(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        with pytest.raises(OutOfOrderCorrectionError):
            engine.ingest_candle(candle_at(allocator, 0, high="100", low="90", is_correction=True))

    def test_out_of_order_candle_window_fails_closed(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        engine.ingest_candle(candle_at(allocator, 5, high="100", low="90"))
        with pytest.raises(OutOfOrderCandleError):
            # recorded_time kept monotonic (pushed past index5's) so only the
            # window_start-ordering discipline is exercised here.
            engine.ingest_candle(candle_at(allocator, 2, high="100", low="90", recorded_offset_seconds=600))

    def test_non_monotonic_recorded_time_fails_closed(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        engine.ingest_candle(candle_at(allocator, 0, high="100", low="90", recorded_offset_seconds=100))
        with pytest.raises(NonMonotonicRecordedTimeError):
            engine.ingest_candle(candle_at(allocator, 1, high="100", low="90", recorded_offset_seconds=0))


class TestHistoricalDirectPath:
    def test_historical_mode_skips_candidate_emits_confirmed_directly(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator, historical=True)
        series = [("100", "90"), ("105", "95"), ("110", "100"), ("105", "95"), ("100", "90")]
        events = feed(engine, allocator, series)
        kinds = {type(e).__name__ for e in events}
        assert "SwingCandidateDetected" not in kinds
        confirmed = [e for e in events if isinstance(e, SwingConfirmed) and e.scope.direction == "HIGH"]
        assert len(confirmed) == 1
        assert confirmed[0].swing_revision == 1
        # causation points directly at pivot + evidence, never a fabricated candidate
        assert confirmed[0].pivot_candle_ref in confirmed[0].causation_refs


class TestDeterministicReplay:
    def test_same_input_produces_same_output_across_two_fresh_engines(self, allocator: SequenceAllocator) -> None:
        series = [("100", "90"), ("105", "95"), ("110", "100"), ("105", "95"), ("100", "90")]

        alloc_a = SequenceAllocator("structure-engine", "0.1.0", "run-a")
        engine_a = SwingEngine(wick_definition(), alloc_a)
        events_a = [(type(e).__name__, e.scope.direction, e.swing_revision) for e in feed(engine_a, alloc_a, series)]

        alloc_b = SequenceAllocator("structure-engine", "0.1.0", "run-b")
        engine_b = SwingEngine(wick_definition(), alloc_b)
        events_b = [(type(e).__name__, e.scope.direction, e.swing_revision) for e in feed(engine_b, alloc_b, series)]

        assert events_a == events_b


class TestDecimalEdgeValuesAndAbsence:
    def test_lossless_decimal_no_float_round_trip(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        series = [("0.1", "0.05"), ("0.2", "0.15"), ("0.30000000000000004", "0.25"), ("0.2", "0.15"), ("0.1", "0.05")]
        events = feed(engine, allocator, series)
        confirmed = [e for e in events if isinstance(e, SwingConfirmed) and e.scope.direction == "HIGH"]
        assert confirmed[0].pivot_price == Decimal("0.30000000000000004")

    def test_no_pivot_is_a_valid_absence_not_an_error(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        # monotonically rising highs — a HIGH candidate may still form locally,
        # but it can never accumulate satisfying right-side evidence, so no
        # SwingConfirmed HIGH ever fires (valid absence, not an error).
        series = [("100", "90"), ("101", "91"), ("102", "92"), ("103", "93"), ("104", "94")]
        events = feed(engine, allocator, series)
        assert not any(isinstance(e, SwingConfirmed) and e.scope.direction == "HIGH" for e in events)


class TestCausalLineage:
    """P3-STR-SWG-A-MAJ-01: swing.md §3/§4/§5 causation invariants."""

    def test_candidate_causation_includes_pivot_candle_fact(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        series = [("100", "90"), ("105", "95"), ("110", "100")]
        pivot_ref = None
        events: list[SwingEvent] = []
        for i, (high, low) in enumerate(series):
            fact = candle_at(allocator, i, high=high, low=low)
            if i == 2:
                pivot_ref = fact.ref
            events += engine.ingest_candle(fact)
        candidate = next(e for e in events if isinstance(e, SwingCandidateDetected) and e.scope.direction == "HIGH")
        assert pivot_ref is not None
        assert pivot_ref in candidate.causation_refs

    def test_confirmed_via_candidate_causation_includes_pivot_and_candidate(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        series = [("100", "90"), ("105", "95"), ("110", "100"), ("105", "95"), ("100", "90")]
        pivot_ref = None
        events: list[SwingEvent] = []
        for i, (high, low) in enumerate(series):
            fact = candle_at(allocator, i, high=high, low=low)
            if i == 2:
                pivot_ref = fact.ref
            events += engine.ingest_candle(fact)
        candidate = next(e for e in events if isinstance(e, SwingCandidateDetected) and e.scope.direction == "HIGH")
        confirmed = next(e for e in events if isinstance(e, SwingConfirmed) and e.scope.direction == "HIGH")
        assert pivot_ref is not None
        assert pivot_ref in confirmed.causation_refs
        assert candidate.ref in confirmed.causation_refs

    def test_confirmed_revision_gt_1_causation_includes_prior_invalidation(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        series = [("100", "90"), ("105", "95"), ("110", "100"), ("105", "95"), ("100", "90")]
        feed(engine, allocator, series)
        corrected = candle_at(allocator, 2, high="112", low="100", is_correction=True, recorded_offset_seconds=600)
        events2 = engine.ingest_candle(corrected)
        invalidated = next(e for e in events2 if isinstance(e, SwingInvalidated))
        confirmed2 = next(e for e in events2 if isinstance(e, SwingConfirmed))
        assert confirmed2.swing_revision == 2
        assert invalidated.ref in confirmed2.causation_refs

    def test_invalidated_upstream_correction_causation_includes_both_refs(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        series = [("100", "90"), ("105", "95"), ("110", "100"), ("105", "95"), ("100", "90")]
        events = feed(engine, allocator, series)
        confirmed = next(e for e in events if isinstance(e, SwingConfirmed) and e.scope.direction == "HIGH")
        corrected = candle_at(allocator, 2, high="112", low="100", is_correction=True, recorded_offset_seconds=600)
        events2 = engine.ingest_candle(corrected)
        invalidated = next(e for e in events2 if isinstance(e, SwingInvalidated))
        # causation must carry BOTH the exact fact being invalidated AND the
        # exact CandleCorrected causing it — never only recorded_time.
        assert confirmed.ref in invalidated.causation_refs
        assert corrected.ref in invalidated.causation_refs

    def test_critical_restoration_after_market_evolution_then_correction(self, allocator: SequenceAllocator) -> None:
        """candidate rev1 -> market_evolution SwingInvalidated rev1 ->
        CandleCorrected removes the market-evolution violation -> swing
        becomes valid again as revision 2, causally linked to the rev1
        SwingInvalidated -- no fabricated invalidation in the restoring pass.
        """
        engine = SwingEngine(wick_definition(left_count=2, right_count=3), allocator)
        series = [("100", "90"), ("105", "95"), ("110", "100"), ("115", "105")]
        events = feed(engine, allocator, series)
        invalidated1 = next(e for e in events if isinstance(e, SwingInvalidated) and e.scope.direction == "HIGH")
        assert invalidated1.invalidation_cause == "market_evolution"
        assert invalidated1.swing_revision == 1

        corrected = candle_at(allocator, 3, high="108", low="98", is_correction=True, recorded_offset_seconds=600)
        events2 = engine.ingest_candle(corrected)
        # Narrow to events belonging to the SAME swing_id under test (pivot @
        # index2). The correction may incidentally also affect an unrelated
        # candidate that had briefly formed at index3 itself before its own
        # value changed — that is legitimate, independent behavior, not part
        # of this restoration case.
        same_swing = [
            e
            for e in events2
            if e.scope.direction == "HIGH"
            and e.scope.pivot_candle_subject_id == invalidated1.scope.pivot_candle_subject_id
        ]
        assert len(same_swing) == 1
        restored = same_swing[0]
        assert isinstance(restored, SwingCandidateDetected)
        assert restored.swing_revision == 2
        assert invalidated1.ref in restored.causation_refs


class TestScopedOrdering:
    """P3-STR-ORDER-A-MAJ-04: no invented global ordering across scopes."""

    def test_independent_scopes_do_not_share_recorded_time_ordering(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        # scope A (default instrument) receives a LATER recorded_time first.
        engine.ingest_candle(candle_at(allocator, 5, high="100", low="90", recorded_offset_seconds=100_000))
        # independent scope B (different instrument) then receives an
        # EARLIER recorded_time -- must NOT fail merely because scope A's
        # last-seen recorded_time was later.
        engine.ingest_candle(
            candle_at(allocator, 0, high="100", low="90", recorded_offset_seconds=0, instrument_id="ETH-USDT")
        )

    def test_same_scope_non_monotonic_still_fails_closed(self, allocator: SequenceAllocator) -> None:
        engine = SwingEngine(wick_definition(), allocator)
        engine.ingest_candle(candle_at(allocator, 0, high="100", low="90", recorded_offset_seconds=1000))
        with pytest.raises(NonMonotonicRecordedTimeError):
            engine.ingest_candle(candle_at(allocator, 1, high="100", low="90", recorded_offset_seconds=0))
