"""BOS/CHoCH structure orientation (structure.md).

Structure has exactly ONE continuous subject per (instrument, venue,
timeframe, structure_definition_version) scope (structure.md §1) — this
engine therefore maintains one linear, append-only fact chain per subject,
which is also exactly the data structure needed to implement §10's
dependency-forward correction cascade: everything after the directly
invalidated fact, in original emission order, is its dependent.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal

from .candle import CandleFact, PriceBasis
from .envelope import EventRecordRef
from .errors import DuplicateCandleConflictError, OutOfOrderCorrectionError
from .identity import deterministic_id
from .publish import SequenceAllocator
from .swing import Direction, SwingConfirmed, SwingInvalidated

Orientation = Literal["UNDETERMINED", "NEUTRAL", "BULLISH", "BEARISH"]
ComparisonPolicy = Literal["strict", "inclusive"]
StructureInvalidationCause = Literal["swing_invalidated", "breaking_candle_corrected", "chained_invalidation"]

#: structure.md §6a — the single canonical policy identifier for this
#: implementation's total order. Any future definition version choosing a
#: different order would need its own identifier — out of scope here.
RELEVANT_SWING_SELECTION_POLICY = (
    "pivot_effective_time_window_start_desc_then_recorded_time_asc_then_stream_id_asc_"
    "then_registry_version_asc_then_sequence_asc_then_swing_revision_desc_then_"
    "swing_id_asc_then_event_id_asc"
)

#: stream-registry.yaml (Phase 1) does not exist yet — real stream-registry-
#: version tracking is explicitly out of scope for this module-local build.
#: A single constant registry-version marker keeps criterion 4 of §6a's
#: total order well-defined (a legitimate, always-equal tie under the one
#: registry state that currently exists) without inventing that
#: infrastructure.
_REGISTRY_VERSION = "v0"


@dataclass(frozen=True, slots=True)
class StructureDefinition:
    """structure.md §9 policy — pinned, not hardcoded to one trading philosophy."""

    structure_definition_version: str
    depends_on_swing_definition_version: str
    break_price_basis: PriceBasis
    comparison_policy: ComparisonPolicy

    def __post_init__(self) -> None:
        if not self.depends_on_swing_definition_version:
            raise ValueError("depends_on_swing_definition_version must be set")


@dataclass(frozen=True, slots=True)
class StructureScope:
    """The four-field qualifying scope of the Logical Structure Subject (structure.md §1)."""

    instrument_id: str
    venue_id: str
    timeframe: str
    structure_definition_version: str

    @property
    def structure_subject_id(self) -> str:
        return deterministic_id(
            "structure",
            self.instrument_id,
            self.venue_id,
            self.timeframe,
            self.structure_definition_version,
        )


@dataclass(frozen=True, slots=True)
class BrokenSwingRef:
    """structure.md §6a canonical, revision-qualified reference."""

    swing_id: str
    swing_revision: int
    swing_confirmed_event_ref: EventRecordRef
    direction: Direction


@dataclass(frozen=True, slots=True)
class BreakOfStructureDetected:
    scope: StructureScope
    prior_orientation: Orientation
    new_orientation: Literal["BULLISH", "BEARISH"]
    broken_swing_ref: BrokenSwingRef
    breaking_candle_refs: tuple[EventRecordRef, ...]
    causation_refs: tuple[EventRecordRef, ...]
    recorded_time: datetime
    ref: EventRecordRef


@dataclass(frozen=True, slots=True)
class ChangeOfCharacterDetected:
    scope: StructureScope
    prior_orientation: Literal["BULLISH", "BEARISH"]
    new_orientation: Literal["BULLISH", "BEARISH"]
    broken_swing_ref: BrokenSwingRef
    breaking_candle_refs: tuple[EventRecordRef, ...]
    causation_refs: tuple[EventRecordRef, ...]
    recorded_time: datetime
    ref: EventRecordRef


OrientationFact = BreakOfStructureDetected | ChangeOfCharacterDetected


@dataclass(frozen=True, slots=True)
class StructureFactInvalidated:
    scope: StructureScope
    invalidated_fact_ref: EventRecordRef
    invalidation_cause: StructureInvalidationCause
    causation_refs: tuple[EventRecordRef, ...]
    recorded_time: datetime
    ref: EventRecordRef


@dataclass(frozen=True, slots=True)
class StructureRecomputed:
    scope: StructureScope
    resulting_orientation: Orientation
    justifying_fact_ref: EventRecordRef | None
    input_cursor_ref: str
    causation_refs: tuple[EventRecordRef, ...]
    recorded_time: datetime
    ref: EventRecordRef


StructureEvent = BreakOfStructureDetected | ChangeOfCharacterDetected | StructureFactInvalidated | StructureRecomputed


@dataclass(slots=True)
class _EligibleSwing:
    """One currently-Eligible (swing_id, swing_revision) — structure.md §6a."""

    swing_id: str
    swing_revision: int
    direction: Direction
    pivot_price: Decimal
    pivot_effective_time: tuple[datetime, datetime]
    swing_confirmed_event_ref: EventRecordRef
    swing_confirmed_recorded_time: datetime


@dataclass(slots=True)
class _ChainEntry:
    """One still-tracked fact in the subject's linear orientation chain."""

    fact: OrientationFact
    invalidated: bool = False


def _total_order_key(swing: _EligibleSwing) -> tuple[object, ...]:
    """structure.md §6a's 8-criterion lexicographic key, ASC-sortable.

    Criteria 1 and 6 are DESC in the Domain Contract — negated here so the
    whole tuple can be compared ASC uniformly by `sorted()`. Criteria 3-5
    (stream_id, registry_version, sequence) are naturally short-circuited by
    Python tuple comparison: it never inspects a later element once an
    earlier one differs, which is exactly the "stop at the first
    distinguishing criterion" rule the Domain Contract requires — including
    never comparing `sequence` across differing streams.
    """
    return (
        -swing.pivot_effective_time[0].timestamp(),  # 1: window_start DESC
        swing.swing_confirmed_recorded_time,  # 2: recorded_time ASC
        swing.swing_confirmed_event_ref.stream_id,  # 3: stream_id ASC
        _REGISTRY_VERSION,  # 4: registry_version ASC (single value — see module docstring)
        swing.swing_confirmed_event_ref.sequence,  # 5: sequence ASC (meaningful only within same stream)
        -swing.swing_revision,  # 6: swing_revision DESC
        swing.swing_id,  # 7: swing_id ASC
        swing.swing_confirmed_event_ref.event_id,  # 8: event_id ASC
    )


class StructureEngine:
    """Deterministic, in-process BOS/CHoCH detector — one authoritative code
    path for Replay/Backtest/Paper/Live (Chapter 3 §3.1). Consumes
    SwingConfirmed/SwingInvalidated (from a SwingEngine of matching
    swing_definition_version) plus the same authoritative candle-closed/
    candle-corrected stream Swing consumes (structure.md §12 — direct Candle
    input is required for breaking-candle detection).
    """

    def __init__(self, definition: StructureDefinition, scope: StructureScope, allocator: SequenceAllocator) -> None:
        self.definition = definition
        self.scope = scope
        self._allocator = allocator
        self._orientation: Orientation = "UNDETERMINED"
        self._eligible: dict[tuple[str, Direction], _EligibleSwing] = {}
        self._consumed: set[tuple[str, int]] = set()
        self._chain: list[_ChainEntry] = []
        self._fact_index: dict[EventRecordRef, int] = {}
        self._fact_pivot_price: dict[EventRecordRef, Decimal] = {}
        self._breaking_candle_subjects: dict[str, list[EventRecordRef]] = {}
        self._candles: dict[str, CandleFact] = {}

    @property
    def current_orientation(self) -> Orientation:
        return self._orientation

    # -- Swing-side ingestion --------------------------------------------

    def on_swing_confirmed(self, event: SwingConfirmed) -> None:
        if event.scope.swing_definition_version != self.definition.depends_on_swing_definition_version:
            return
        if (event.scope.swing_id, event.swing_revision) in self._consumed:
            return
        key = (event.scope.swing_id, event.scope.direction)
        self._eligible[key] = _EligibleSwing(
            swing_id=event.scope.swing_id,
            swing_revision=event.swing_revision,
            direction=event.scope.direction,
            pivot_price=event.pivot_price,
            pivot_effective_time=event.pivot_effective_time,
            swing_confirmed_event_ref=event.ref,
            swing_confirmed_recorded_time=event.recorded_time,
        )

    def on_swing_invalidated(self, event: SwingInvalidated) -> list[StructureEvent]:
        if event.scope.swing_definition_version != self.definition.depends_on_swing_definition_version:
            return []
        key = (event.scope.swing_id, event.scope.direction)
        eligible = self._eligible.get(key)
        if eligible is not None and eligible.swing_revision == event.swing_revision:
            del self._eligible[key]
            return []
        if (event.scope.swing_id, event.swing_revision) in self._consumed:
            for idx, entry in enumerate(self._chain):
                if entry.invalidated:
                    continue
                ref = entry.fact.broken_swing_ref
                if ref.swing_id == event.scope.swing_id and ref.swing_revision == event.swing_revision:
                    return self._cascade(idx, "swing_invalidated", event.ref, event.recorded_time)
        return []

    # -- Candle-side ingestion --------------------------------------------

    def on_candle(self, fact: CandleFact) -> list[StructureEvent]:
        subject_id = fact.scope.subject_id
        if subject_id in self._candles:
            old = self._candles[subject_id]
            if old.ohlcv == fact.ohlcv:
                return []  # idempotent
            if not fact.is_correction:
                raise DuplicateCandleConflictError(
                    f"candle {subject_id} already ingested with different OHLCV and is_correction=False"
                )
            self._candles[subject_id] = fact
            return self._reevaluate_breaking_candle(subject_id, fact.recorded_time)

        if fact.is_correction:
            raise OutOfOrderCorrectionError(f"correction for never-before-seen subject {subject_id}")
        self._candles[subject_id] = fact
        return self._evaluate_break(fact)

    # -- break evaluation ----------------------------------------------

    def _break_criterion(self, candle: CandleFact, pivot_price: Decimal, direction: Direction) -> bool:
        basis = self.definition.break_price_basis
        inclusive = self.definition.comparison_policy == "inclusive"
        if direction == "HIGH":
            value = candle.ohlcv.extreme(basis)
            return value >= pivot_price if inclusive else value > pivot_price
        value = candle.ohlcv.extreme_low(basis)
        return value <= pivot_price if inclusive else value < pivot_price

    def _decision(self, direction: Direction) -> tuple[Literal["BULLISH", "BEARISH"], Literal["BOS", "CHOCH"]]:
        """structure.md §6/§7 decision tables: which (new_orientation, kind)
        breaking this direction's eligible swing produces, given current
        orientation.
        """
        orientation = self._orientation
        if orientation in ("UNDETERMINED", "NEUTRAL"):
            return ("BULLISH", "BOS") if direction == "HIGH" else ("BEARISH", "BOS")
        if orientation == "BULLISH":
            return ("BULLISH", "BOS") if direction == "HIGH" else ("BEARISH", "CHOCH")
        return ("BEARISH", "BOS") if direction == "LOW" else ("BULLISH", "CHOCH")

    def _evaluate_break(self, candle: CandleFact) -> list[StructureEvent]:
        winners: list[tuple[tuple[object, ...], _EligibleSwing, Direction]] = []
        for (_swing_id, direction), swing in list(self._eligible.items()):
            if not self._break_criterion(candle, swing.pivot_price, direction):
                continue
            winners.append((_total_order_key(swing), swing, direction))
        if not winners:
            return []
        winners.sort(key=lambda item: item[0])
        _, swing, direction = winners[0]
        new_orientation, kind = self._decision(direction)
        return self._emit_orientation_fact(swing, direction, new_orientation, kind, candle)

    def _emit_orientation_fact(
        self,
        swing: _EligibleSwing,
        direction: Direction,
        new_orientation: Literal["BULLISH", "BEARISH"],
        kind: Literal["BOS", "CHOCH"],
        breaking_candle: CandleFact,
    ) -> list[StructureEvent]:
        prior = self._orientation
        broken_ref = BrokenSwingRef(
            swing_id=swing.swing_id,
            swing_revision=swing.swing_revision,
            swing_confirmed_event_ref=swing.swing_confirmed_event_ref,
            direction=direction,
        )
        breaking_refs = (breaking_candle.ref,)
        causation = (swing.swing_confirmed_event_ref, breaking_candle.ref)
        ref = self._allocator.next_ref(_structure_stream_id(self))
        fact: OrientationFact
        if kind == "BOS":
            fact = BreakOfStructureDetected(
                scope=self.scope,
                prior_orientation=prior,
                new_orientation=new_orientation,
                broken_swing_ref=broken_ref,
                breaking_candle_refs=breaking_refs,
                causation_refs=causation,
                recorded_time=breaking_candle.recorded_time,
                ref=ref,
            )
        else:
            assert prior in ("BULLISH", "BEARISH")
            fact = ChangeOfCharacterDetected(
                scope=self.scope,
                prior_orientation=prior,
                new_orientation=new_orientation,
                broken_swing_ref=broken_ref,
                breaking_candle_refs=breaking_refs,
                causation_refs=causation,
                recorded_time=breaking_candle.recorded_time,
                ref=ref,
            )
        key = (swing.swing_id, direction)
        del self._eligible[key]
        self._consumed.add((swing.swing_id, swing.swing_revision))
        self._chain.append(_ChainEntry(fact=fact))
        self._fact_index[ref] = len(self._chain) - 1
        self._fact_pivot_price[ref] = swing.pivot_price
        self._breaking_candle_subjects.setdefault(breaking_candle.scope.subject_id, []).append(ref)
        self._orientation = new_orientation
        return [fact]

    # -- correction cascade (structure.md §10) --------------------------

    def _reevaluate_breaking_candle(self, subject_id: str, recorded_time: datetime) -> list[StructureEvent]:
        candle = self._candles[subject_id]
        events: list[StructureEvent] = []
        for fact_ref in list(self._breaking_candle_subjects.get(subject_id, [])):
            idx = self._fact_index.get(fact_ref)
            if idx is None or self._chain[idx].invalidated:
                continue
            fact = self._chain[idx].fact
            pivot_price = self._fact_pivot_price[fact.ref]
            if self._break_criterion(candle, pivot_price, fact.broken_swing_ref.direction):
                continue  # still breaks — no-op
            events.extend(self._cascade(idx, "breaking_candle_corrected", None, recorded_time))
        return events

    def _cascade(
        self,
        direct_idx: int,
        direct_cause: StructureInvalidationCause,
        direct_cause_ref: EventRecordRef | None,
        recorded_time: datetime,
    ) -> list[StructureEvent]:
        events: list[StructureEvent] = []
        prior_ref: EventRecordRef | None = direct_cause_ref
        for i in range(direct_idx, len(self._chain)):
            entry = self._chain[i]
            if entry.invalidated:
                continue
            cause: StructureInvalidationCause = direct_cause if i == direct_idx else "chained_invalidation"
            causation: list[EventRecordRef] = [entry.fact.ref]
            if prior_ref is not None:
                causation.append(prior_ref)
            ref = self._allocator.next_ref(_structure_stream_id(self))
            fact = StructureFactInvalidated(
                scope=self.scope,
                invalidated_fact_ref=entry.fact.ref,
                invalidation_cause=cause,
                causation_refs=tuple(causation),
                recorded_time=recorded_time,
                ref=ref,
            )
            events.append(fact)
            entry.invalidated = True
            prior_ref = ref

        cascade_refs = tuple(e.ref for e in events)
        justifying: OrientationFact | None = None
        for entry in reversed(self._chain):
            if not entry.invalidated:
                justifying = entry.fact
                break
        resulting: Orientation = justifying.new_orientation if justifying is not None else "NEUTRAL"
        self._orientation = resulting
        recompute_ref = self._allocator.next_ref(_structure_stream_id(self))
        recompute = StructureRecomputed(
            scope=self.scope,
            resulting_orientation=resulting,
            justifying_fact_ref=(justifying.ref if justifying is not None else None),
            input_cursor_ref=f"cursor@{recorded_time.isoformat()}",
            causation_refs=cascade_refs,
            recorded_time=recorded_time,
            ref=recompute_ref,
        )
        events.append(recompute)
        return events


def _structure_stream_id(engine: StructureEngine) -> str:
    return f"structure:{engine.scope.structure_subject_id}"
