from __future__ import annotations

import pytest
from conftest import INSTRUMENT, TIMEFRAME, VENUE, candle_at

from structure_engine import (
    BreakOfStructureDetected,
    ChangeOfCharacterDetected,
    SequenceAllocator,
    StructureDefinition,
    StructureEngine,
    StructureFactInvalidated,
    StructureRecomputed,
    StructureScope,
    SwingConfirmed,
    SwingDefinition,
    SwingEngine,
    SwingInvalidated,
    SwingScope,
)
from structure_engine.errors import DuplicateCandleConflictError, OutOfOrderCorrectionError
from structure_engine.structure import Orientation


def build_pair(
    allocator: SequenceAllocator, *, comparison_policy: str = "strict"
) -> tuple[SwingEngine, StructureEngine]:
    swing_def = SwingDefinition(
        swing_definition_version="swd-1",
        left_count=2,
        right_count=2,
        price_basis="wick",
        equal_level_policy="first_occurrence",
    )
    swing_engine = SwingEngine(swing_def, allocator, historical=True)
    structure_def = StructureDefinition(
        structure_definition_version="strd-1",
        depends_on_swing_definition_version="swd-1",
        break_price_basis="wick",
        comparison_policy=comparison_policy,  # type: ignore[arg-type]
    )
    scope = StructureScope(INSTRUMENT, VENUE, TIMEFRAME, "strd-1")
    structure_engine = StructureEngine(structure_def, scope, allocator)
    return swing_engine, structure_engine


def drive(
    swing_engine: SwingEngine,
    structure_engine: StructureEngine,
    allocator: SequenceAllocator,
    series: list[tuple[str, str]],
    *,
    corrections: dict[int, tuple[str, str]] | None = None,
) -> list[object]:
    """Feeds a candle series through Swing then Structure, in emission order,
    exactly as a real orchestrator would wire the two engines together."""
    all_events: list[object] = []
    for i, (high, low) in enumerate(series):
        fact = candle_at(allocator, i, high=high, low=low)
        swing_events = swing_engine.ingest_candle(fact)
        for e in swing_events:
            if isinstance(e, SwingConfirmed):
                structure_engine.on_swing_confirmed(e)
            elif isinstance(e, SwingInvalidated):
                all_events.extend(structure_engine.on_swing_invalidated(e))
        all_events.extend(structure_engine.on_candle(fact))
    if corrections:
        for idx, (high, low) in corrections.items():
            fact = candle_at(allocator, idx, high=high, low=low, is_correction=True, recorded_offset_seconds=600)
            swing_events = swing_engine.ingest_candle(fact)
            for e in swing_events:
                if isinstance(e, SwingConfirmed):
                    structure_engine.on_swing_confirmed(e)
                elif isinstance(e, SwingInvalidated):
                    all_events.extend(structure_engine.on_swing_invalidated(e))
            all_events.extend(structure_engine.on_candle(fact))
    return all_events


class TestBOSAndCHoCH:
    def test_bos_establishes_first_orientation(self, allocator: SequenceAllocator) -> None:
        swing_engine, structure_engine = build_pair(allocator)
        # HIGH swing pivot at index2 (110), confirmed by index3,4; breaks at index5 (115).
        series = [
            ("100", "90"),
            ("105", "95"),
            ("110", "100"),
            ("105", "95"),
            ("100", "90"),
            ("116", "106"),
        ]
        events = drive(swing_engine, structure_engine, allocator, series)
        bos = [e for e in events if isinstance(e, BreakOfStructureDetected)]
        assert len(bos) == 1
        assert bos[0].prior_orientation == "UNDETERMINED"
        assert bos[0].new_orientation == "BULLISH"
        assert structure_engine.current_orientation == "BULLISH"

    def test_bos_continuation_same_direction(self, allocator: SequenceAllocator) -> None:
        swing_engine, structure_engine = build_pair(allocator)
        series = [
            ("100", "90"),
            ("105", "95"),
            ("110", "100"),
            ("105", "95"),
            ("100", "90"),  # HIGH swing @110
            ("116", "106"),  # BOS -> BULLISH
            ("115", "105"),
            ("120", "110"),
            ("125", "115"),
            ("120", "110"),
            ("115", "105"),  # HIGH swing @125
            ("131", "121"),  # continuation BOS -> still BULLISH
        ]
        events = drive(swing_engine, structure_engine, allocator, series)
        bos = [e for e in events if isinstance(e, BreakOfStructureDetected)]
        assert len(bos) == 2
        assert bos[1].prior_orientation == "BULLISH"
        assert bos[1].new_orientation == "BULLISH"
        assert structure_engine.current_orientation == "BULLISH"

    def test_choch_reverses_orientation(self, allocator: SequenceAllocator) -> None:
        swing_engine, structure_engine = build_pair(allocator)
        series = [
            ("100", "90"),
            ("105", "95"),
            ("110", "100"),
            ("105", "95"),
            ("100", "90"),  # HIGH swing @110
            ("116", "106"),  # BOS -> BULLISH
            ("115", "105"),
            ("110", "100"),
            ("105", "95"),
            ("110", "100"),
            ("115", "105"),  # LOW swing @95
            ("112", "94"),  # breaks LOW 95 -> CHoCH -> BEARISH
        ]
        events = drive(swing_engine, structure_engine, allocator, series)
        choch = [e for e in events if isinstance(e, ChangeOfCharacterDetected)]
        assert len(choch) == 1
        assert choch[0].prior_orientation == "BULLISH"
        assert choch[0].new_orientation == "BEARISH"
        assert structure_engine.current_orientation == "BEARISH"


class TestComparisonPolicy:
    def test_strict_touch_is_not_a_break(self, allocator: SequenceAllocator) -> None:
        swing_engine, structure_engine = build_pair(allocator, comparison_policy="strict")
        series = [
            ("100", "90"),
            ("105", "95"),
            ("110", "100"),
            ("105", "95"),
            ("100", "90"),
            ("110", "100"),  # exact touch, strict -> not a break
        ]
        events = drive(swing_engine, structure_engine, allocator, series)
        assert not any(isinstance(e, BreakOfStructureDetected) for e in events)
        assert structure_engine.current_orientation == "UNDETERMINED"

    def test_inclusive_touch_is_a_break(self, allocator: SequenceAllocator) -> None:
        swing_engine, structure_engine = build_pair(allocator, comparison_policy="inclusive")
        series = [
            ("100", "90"),
            ("105", "95"),
            ("110", "100"),
            ("105", "95"),
            ("100", "90"),
            ("110", "100"),  # exact touch, inclusive -> IS a break
        ]
        events = drive(swing_engine, structure_engine, allocator, series)
        assert any(isinstance(e, BreakOfStructureDetected) for e in events)
        assert structure_engine.current_orientation == "BULLISH"


class TestTotalOrderTieBreak:
    def test_most_recent_pivot_wins_when_both_broken_same_candle(self, allocator: SequenceAllocator) -> None:
        swing_engine, structure_engine = build_pair(allocator, comparison_policy="inclusive")
        # Two HIGH pivots, both confirmed and both still unbroken/eligible at
        # the same time: pivot1=105 (index2, older), pivot2=104 (index6, more
        # recent — kept BELOW pivot1 so its own arrival never breaks pivot1
        # prematurely). A single later candle (110) breaks both simultaneously.
        # Criterion 1 of §6a (pivot window_start DESC) must pick the MORE
        # RECENT pivot (104, index6) as the winner, even though it is the
        # numerically smaller level.
        series = [
            ("100", "90"),
            ("100", "90"),
            ("105", "95"),
            ("100", "90"),
            ("100", "90"),
            ("102", "93"),
            ("104", "98"),
            ("102", "93"),
            ("102", "93"),
            ("110", "100"),  # breaks both eligible HIGH swings (105 and 104) at once
        ]
        events = drive(swing_engine, structure_engine, allocator, series)
        bos = [e for e in events if isinstance(e, BreakOfStructureDetected)]
        assert len(bos) == 1
        assert bos[0].broken_swing_ref.swing_confirmed_event_ref in bos[0].causation_refs

        pivot2_subject_id = candle_at(allocator, 6, high="0", low="0").scope.subject_id
        pivot1_subject_id = candle_at(allocator, 2, high="0", low="0").scope.subject_id
        expected_winner = SwingScope(
            INSTRUMENT,
            VENUE,
            TIMEFRAME,
            "HIGH",
            pivot2_subject_id,
            "swd-1",
        ).swing_id
        rejected_loser = SwingScope(
            INSTRUMENT,
            VENUE,
            TIMEFRAME,
            "HIGH",
            pivot1_subject_id,
            "swd-1",
        ).swing_id
        assert bos[0].broken_swing_ref.swing_id == expected_winner
        assert bos[0].broken_swing_ref.swing_id != rejected_loser


class TestRevisionQualifiedConsumption:
    def test_same_swing_id_different_revision_independently_eligible(self, allocator: SequenceAllocator) -> None:
        swing_engine, structure_engine = build_pair(allocator)
        series = [
            ("100", "90"),
            ("105", "95"),
            ("110", "100"),
            ("105", "95"),
            ("100", "90"),  # HIGH swing rev1 @110
            ("116", "106"),  # BOS consumes rev1
        ]
        events = drive(swing_engine, structure_engine, allocator, series)
        bos1 = next(e for e in events if isinstance(e, BreakOfStructureDetected))
        assert bos1.broken_swing_ref.swing_revision == 1

        # correct the pivot candle (index2) so a NEW revision (2) of the SAME
        # swing_id is produced -- must be independently eligible, not blocked
        # by revision 1 already being consumed.
        corrected = candle_at(allocator, 2, high="112", low="100", is_correction=True, recorded_offset_seconds=600)
        swing_events = swing_engine.ingest_candle(corrected)
        cascade_events: list[object] = []
        for e in swing_events:
            if isinstance(e, SwingConfirmed):
                structure_engine.on_swing_confirmed(e)
            elif isinstance(e, SwingInvalidated):
                cascade_events += structure_engine.on_swing_invalidated(e)
        assert bos1.broken_swing_ref.swing_id in {e.scope.swing_id for e in swing_events if hasattr(e, "scope")}
        # a fresh HIGH break must now be able to consume revision 2 independently.
        follow_up = candle_at(allocator, 6, high="120", low="110", recorded_offset_seconds=700)
        follow_events = structure_engine.on_candle(follow_up)
        bos2 = [e for e in follow_events if isinstance(e, BreakOfStructureDetected)]
        assert len(bos2) == 1
        assert bos2[0].broken_swing_ref.swing_revision == 2
        assert bos2[0].broken_swing_ref.swing_id == bos1.broken_swing_ref.swing_id


class TestCorrectionCascade:
    def test_swing_invalidated_cascades_dependency_forward(self, allocator: SequenceAllocator) -> None:
        swing_engine, structure_engine = build_pair(allocator)
        series = [
            ("100", "90"),
            ("105", "95"),
            ("110", "100"),
            ("105", "95"),
            ("100", "90"),  # HIGH swing @110 (E1 pivot)
            ("116", "106"),  # E1: BOS -> BULLISH
            ("115", "105"),
            ("110", "100"),
            ("105", "95"),
            ("110", "100"),
            ("115", "105"),  # LOW swing @95
            ("112", "94"),  # E2: CHoCH -> BEARISH
        ]
        drive(swing_engine, structure_engine, allocator, series)
        assert structure_engine.current_orientation == "BEARISH"

        # correction disqualifies the FIRST swing (pivot@index2, 110) entirely
        # -> cascades forward through both E1 and E2.
        corrected = candle_at(allocator, 2, high="103", low="100", is_correction=True, recorded_offset_seconds=600)
        swing_events = swing_engine.ingest_candle(corrected)
        cascade: list[object] = []
        for e in swing_events:
            if isinstance(e, SwingInvalidated):
                cascade += structure_engine.on_swing_invalidated(e)

        invalidations = [e for e in cascade if isinstance(e, StructureFactInvalidated)]
        recomputed = [e for e in cascade if isinstance(e, StructureRecomputed)]
        assert len(invalidations) == 2  # E1 direct, E2 chained
        assert invalidations[0].invalidation_cause == "swing_invalidated"
        assert invalidations[1].invalidation_cause == "chained_invalidation"
        assert len(recomputed) == 1
        assert recomputed[0].resulting_orientation == "NEUTRAL"
        assert recomputed[0].justifying_fact_ref is None
        final_orientation: Orientation = structure_engine.current_orientation
        assert final_orientation == "NEUTRAL"

    def test_breaking_candle_corrected_invalidates_without_swing_involvement(
        self, allocator: SequenceAllocator
    ) -> None:
        swing_engine, structure_engine = build_pair(allocator, comparison_policy="strict")
        series = [
            ("100", "90"),
            ("105", "95"),
            ("110", "100"),
            ("105", "95"),
            ("100", "90"),
            ("116", "106"),  # breaking candle for BOS
        ]
        events = drive(swing_engine, structure_engine, allocator, series)
        bos = next(e for e in events if isinstance(e, BreakOfStructureDetected))
        assert structure_engine.current_orientation == "BULLISH"

        # correct the BREAKING candle (index5) so it no longer clears 110.
        corrected = candle_at(allocator, 5, high="108", low="98", is_correction=True, recorded_offset_seconds=600)
        cascade_events = structure_engine.on_candle(corrected)
        invalidations = [e for e in cascade_events if isinstance(e, StructureFactInvalidated)]
        recomputed = [e for e in cascade_events if isinstance(e, StructureRecomputed)]
        assert len(invalidations) == 1
        assert invalidations[0].invalidation_cause == "breaking_candle_corrected"
        assert invalidations[0].invalidated_fact_ref == bos.ref
        assert len(recomputed) == 1
        assert recomputed[0].resulting_orientation == "NEUTRAL"
        final_orientation: Orientation = structure_engine.current_orientation
        assert final_orientation == "NEUTRAL"


class TestNoRepaintAndDedup:
    def test_bos_never_overwritten_only_invalidated(self, allocator: SequenceAllocator) -> None:
        swing_engine, structure_engine = build_pair(allocator)
        series = [
            ("100", "90"),
            ("105", "95"),
            ("110", "100"),
            ("105", "95"),
            ("100", "90"),
            ("116", "106"),
        ]
        events = drive(swing_engine, structure_engine, allocator, series)
        bos = next(e for e in events if isinstance(e, BreakOfStructureDetected))
        # BreakOfStructureDetected is a frozen dataclass -- structurally cannot
        # be mutated in place; only StructureFactInvalidated can supersede it.
        with pytest.raises(AttributeError):
            bos.new_orientation = "BEARISH"  # type: ignore[misc]

    def test_duplicate_candle_conflict_fails_closed(self, allocator: SequenceAllocator) -> None:
        _, structure_engine = build_pair(allocator)
        fact = candle_at(allocator, 0, high="100", low="90")
        structure_engine.on_candle(fact)
        with pytest.raises(DuplicateCandleConflictError):
            structure_engine.on_candle(candle_at(allocator, 0, high="101", low="90"))

    def test_out_of_order_correction_fails_closed(self, allocator: SequenceAllocator) -> None:
        _, structure_engine = build_pair(allocator)
        with pytest.raises(OutOfOrderCorrectionError):
            structure_engine.on_candle(candle_at(allocator, 0, high="100", low="90", is_correction=True))

    def test_idempotent_resubmission_is_a_no_op(self, allocator: SequenceAllocator) -> None:
        _, structure_engine = build_pair(allocator)
        fact = candle_at(allocator, 0, high="100", low="90")
        structure_engine.on_candle(fact)
        again = structure_engine.on_candle(candle_at(allocator, 0, high="100", low="90"))
        assert again == []


class TestNoRawRegimeConsumption:
    def test_structure_engine_module_never_imports_raw_regime(self) -> None:
        import structure_engine

        assert not any("raw_regime" in name for name in structure_engine.__dict__)


class TestValidAbsence:
    def test_no_orientation_change_when_no_eligible_swing_broken(self, allocator: SequenceAllocator) -> None:
        swing_engine, structure_engine = build_pair(allocator)
        series = [("100", "90"), ("101", "91"), ("102", "92"), ("103", "93"), ("104", "94")]
        events = drive(swing_engine, structure_engine, allocator, series)
        assert events == []
        assert structure_engine.current_orientation == "UNDETERMINED"


class TestDecimalEdgeValues:
    def test_lossless_decimal_break_comparison(self, allocator: SequenceAllocator) -> None:
        swing_engine, structure_engine = build_pair(allocator, comparison_policy="inclusive")
        series = [
            ("0.1", "0.05"),
            ("0.2", "0.15"),
            ("0.30000000000000004", "0.25"),
            ("0.2", "0.15"),
            ("0.1", "0.05"),
            ("0.30000000000000004", "0.2"),
        ]
        events = drive(swing_engine, structure_engine, allocator, series)
        bos = [e for e in events if isinstance(e, BreakOfStructureDetected)]
        assert len(bos) == 1  # exact decimal equality under inclusive comparison
