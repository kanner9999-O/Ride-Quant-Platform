"""Swing pivot detection/confirmation/invalidation (swing.md).

Implements the full Swing revision lifecycle (§1/§1a): candidate detection,
confirmation, `market_evolution` and `upstream_correction` invalidation, and
deterministic re-derivation of a new revision after a correction — for both
the streaming CANDIDATE -> CONFIRMED path and the historical/backtest direct
UNSEEN -> CONFIRMED shortcut (§1), controlled by a single `historical` flag so
both paths share exactly one pivot-evaluation algorithm.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from decimal import Decimal
from typing import Literal

from .candle import OHLCV, CandleFact, PriceBasis
from .envelope import EventRecordRef
from .errors import (
    DuplicateCandleConflictError,
    NonMonotonicRecordedTimeError,
    OutOfOrderCandleError,
    OutOfOrderCorrectionError,
)
from .identity import deterministic_id
from .publish import SequenceAllocator

Direction = Literal["HIGH", "LOW"]
_DIRECTIONS: tuple[Direction, Direction] = ("HIGH", "LOW")
EqualLevelPolicy = Literal["first_occurrence", "last_occurrence"]
InvalidationCause = Literal["market_evolution", "upstream_correction"]
_CandleKey = tuple[str, str, str]


@dataclass(frozen=True, slots=True)
class SwingDefinition:
    """swing.md §9 policy — pinned, not hardcoded to one trading philosophy."""

    swing_definition_version: str
    left_count: int
    right_count: int
    price_basis: PriceBasis
    equal_level_policy: EqualLevelPolicy

    def __post_init__(self) -> None:
        if self.left_count < 1:
            raise ValueError("left_count must be >= 1")
        if self.right_count < 1:
            raise ValueError("right_count must be >= 1")


@dataclass(frozen=True, slots=True)
class SwingScope:
    """The six-field qualifying scope of a Logical Swing Subject (swing.md §1)."""

    instrument_id: str
    venue_id: str
    timeframe: str
    direction: Direction
    pivot_candle_subject_id: str
    swing_definition_version: str

    @property
    def swing_id(self) -> str:
        return deterministic_id(
            "swing",
            self.instrument_id,
            self.venue_id,
            self.timeframe,
            self.direction,
            self.pivot_candle_subject_id,
            self.swing_definition_version,
        )


@dataclass(frozen=True, slots=True)
class SwingCandidateDetected:
    scope: SwingScope
    swing_revision: int
    pivot_price: Decimal
    pivot_effective_time: tuple[datetime, datetime]
    left_evidence_refs: tuple[EventRecordRef, ...]
    causation_refs: tuple[EventRecordRef, ...]
    recorded_time: datetime
    ref: EventRecordRef


@dataclass(frozen=True, slots=True)
class SwingConfirmed:
    scope: SwingScope
    swing_revision: int
    pivot_price: Decimal
    pivot_effective_time: tuple[datetime, datetime]
    pivot_candle_ref: EventRecordRef
    left_evidence_refs: tuple[EventRecordRef, ...]
    right_evidence_refs: tuple[EventRecordRef, ...]
    causation_refs: tuple[EventRecordRef, ...]
    recorded_time: datetime
    ref: EventRecordRef


@dataclass(frozen=True, slots=True)
class SwingInvalidated:
    scope: SwingScope
    swing_revision: int
    invalidation_cause: InvalidationCause
    causation_refs: tuple[EventRecordRef, ...]
    recorded_time: datetime
    ref: EventRecordRef


SwingEvent = SwingCandidateDetected | SwingConfirmed | SwingInvalidated


def _cmp_extreme(direction: Direction, basis: PriceBasis, ohlcv: OHLCV, pivot_ohlcv: OHLCV) -> int:
    """-1 strictly less extreme than pivot, 0 tie, 1 strictly more extreme (fails)."""
    if direction == "HIGH":
        value, pivot = ohlcv.extreme(basis), pivot_ohlcv.extreme(basis)
        less_extreme = value < pivot
    else:
        value, pivot = ohlcv.extreme_low(basis), pivot_ohlcv.extreme_low(basis)
        less_extreme = value > pivot
    if value == pivot:
        return 0
    return -1 if less_extreme else 1


def _window_satisfied(
    window: list[CandleFact],
    direction: Direction,
    basis: PriceBasis,
    equal_level_policy: EqualLevelPolicy,
    pivot_ohlcv: OHLCV,
    *,
    side: Literal["left", "right"],
) -> bool:
    """swing.md §9 left/right evidence + equal-level tie handling.

    A tie is resolved by which occurrence is EARLIER under `first_occurrence`
    (so a tie in the left window — the earlier neighbor — disqualifies the
    later candidate; a tie in the right window does not, since the pivot
    itself is earlier than the right neighbor) or LATER under
    `last_occurrence` (symmetric, opposite disqualification side). This
    operational reading of §9's tie rule is a module-local implementation
    detail — the Domain Contract states the policy semantics, not the exact
    per-window algorithm (swing.md §17 explicitly defers the concrete
    mechanism).
    """
    for candle in window:
        cmp = _cmp_extreme(direction, basis, candle.ohlcv, pivot_ohlcv)
        if cmp == 1:
            return False
        if cmp == 0:
            if side == "left" and equal_level_policy == "first_occurrence":
                return False
            if side == "right" and equal_level_policy == "last_occurrence":
                return False
    return True


@dataclass(slots=True)
class _SwingState:
    pivot_index: int
    revision: int
    state: Literal["CANDIDATE", "CONFIRMED", "INVALIDATED"]
    candidate_ref: EventRecordRef | None
    active_ref: EventRecordRef | None
    pivot_price: Decimal


class SwingEngine:
    """Deterministic, in-process Swing detector — one authoritative code path
    for Replay/Backtest/Paper/Live (Chapter 3 §3.1); orchestration supplies
    candles in cursor order, this engine never looks ahead of what it has
    been given (Chapter 5).
    """

    def __init__(
        self,
        definition: SwingDefinition,
        allocator: SequenceAllocator,
        *,
        historical: bool = False,
        stream_id: str = "swing",
    ) -> None:
        self.definition = definition
        self._allocator = allocator
        self._historical = historical
        self._stream_id = stream_id
        self._candles: dict[_CandleKey, list[CandleFact]] = {}
        self._candle_pos: dict[_CandleKey, dict[str, int]] = {}
        self._last_recorded_time: datetime | None = None
        self._swings: dict[str, _SwingState] = {}

    # -- public API ---------------------------------------------------

    def ingest_candle(self, fact: CandleFact) -> list[SwingEvent]:
        """Ingest one authoritative candle-closed or candle-corrected fact."""
        self._check_recorded_time(fact.recorded_time)
        key = (fact.scope.instrument_id, fact.scope.venue_id, fact.scope.timeframe)
        candles = self._candles.setdefault(key, [])
        positions = self._candle_pos.setdefault(key, {})
        subject_id = fact.scope.subject_id

        if subject_id in positions:
            return self._ingest_known_subject(key, positions[subject_id], fact)
        return self._ingest_new_subject(key, candles, positions, fact)

    def swing_state(self, scope: SwingScope) -> str | None:
        """Current lifecycle state of the latest revision, or None if never seen."""
        state = self._swings.get(scope.swing_id)
        return state.state if state is not None else None

    def swing_revision(self, scope: SwingScope) -> int | None:
        state = self._swings.get(scope.swing_id)
        return state.revision if state is not None else None

    # -- ingestion paths ------------------------------------------------

    def _ingest_known_subject(self, key: _CandleKey, idx: int, fact: CandleFact) -> list[SwingEvent]:
        candles = self._candles[key]
        old = candles[idx]
        if old.ohlcv == fact.ohlcv:
            return []  # idempotent — identical resubmission, not a duplicate source
        if not fact.is_correction:
            raise DuplicateCandleConflictError(
                f"candle {fact.scope.subject_id} already ingested with different OHLCV and is_correction=False"
            )
        candles[idx] = fact
        events: list[SwingEvent] = []
        rc, lc = self.definition.right_count, self.definition.left_count
        for direction in _DIRECTIONS:
            for pivot_idx in range(max(0, idx - rc), min(len(candles), idx + lc + 1)):
                events.extend(self._recompute_after_correction(key, pivot_idx, direction, fact.recorded_time))
        return events

    def _ingest_new_subject(
        self,
        key: _CandleKey,
        candles: list[CandleFact],
        positions: dict[str, int],
        fact: CandleFact,
    ) -> list[SwingEvent]:
        if fact.is_correction:
            raise OutOfOrderCorrectionError(f"correction for never-before-seen subject {fact.scope.subject_id}")
        if candles and fact.scope.window_start < candles[-1].scope.window_start:
            raise OutOfOrderCandleError(
                f"candle window_start {fact.scope.window_start} precedes last-seen {candles[-1].scope.window_start}"
            )
        candles.append(fact)
        idx = len(candles) - 1
        positions[fact.scope.subject_id] = idx

        events: list[SwingEvent] = []
        for direction in _DIRECTIONS:
            events.extend(self._check_market_evolution(key, idx, direction, fact.recorded_time))
        rc = self.definition.right_count
        for direction in _DIRECTIONS:
            events.extend(self._advance(key, idx, direction, fact.recorded_time))
            for pivot_idx in range(max(0, idx - rc), idx):
                events.extend(self._advance(key, pivot_idx, direction, fact.recorded_time))
        return events

    # -- evaluation helpers ----------------------------------------------

    def _scope_for(self, key: _CandleKey, direction: Direction, pivot_fact: CandleFact) -> SwingScope:
        instrument_id, venue_id, timeframe = key
        return SwingScope(
            instrument_id,
            venue_id,
            timeframe,
            direction,
            pivot_fact.scope.subject_id,
            self.definition.swing_definition_version,
        )

    def _pivot_price(self, pivot_fact: CandleFact, direction: Direction) -> Decimal:
        basis = self.definition.price_basis
        return pivot_fact.ohlcv.extreme(basis) if direction == "HIGH" else pivot_fact.ohlcv.extreme_low(basis)

    def _left_satisfied(self, candles: list[CandleFact], pivot_idx: int, direction: Direction) -> bool:
        lc = self.definition.left_count
        if pivot_idx < lc:
            return False
        window = candles[pivot_idx - lc : pivot_idx]
        return _window_satisfied(
            window,
            direction,
            self.definition.price_basis,
            self.definition.equal_level_policy,
            candles[pivot_idx].ohlcv,
            side="left",
        )

    def _right_satisfied(self, candles: list[CandleFact], pivot_idx: int, direction: Direction) -> bool:
        rc = self.definition.right_count
        if pivot_idx + 1 + rc > len(candles):
            return False
        window = candles[pivot_idx + 1 : pivot_idx + 1 + rc]
        return _window_satisfied(
            window,
            direction,
            self.definition.price_basis,
            self.definition.equal_level_policy,
            candles[pivot_idx].ohlcv,
            side="right",
        )

    def _check_market_evolution(
        self, key: _CandleKey, idx: int, direction: Direction, recorded_time: datetime
    ) -> list[SwingEvent]:
        """swing.md §5(a): a still-CANDIDATE swing invalidates immediately once a
        candle breaks past its pivot, without waiting for the full right-side
        evidence window to accumulate.
        """
        candles = self._candles[key]
        rc = self.definition.right_count
        events: list[SwingEvent] = []
        for pivot_idx in range(max(0, idx - rc), idx):
            pivot_fact = candles[pivot_idx]
            scope = self._scope_for(key, direction, pivot_fact)
            existing = self._swings.get(scope.swing_id)
            if existing is None or existing.state != "CANDIDATE" or existing.pivot_index != pivot_idx:
                continue
            cmp = _cmp_extreme(direction, self.definition.price_basis, candles[idx].ohlcv, pivot_fact.ohlcv)
            breaks = cmp == 1 or (cmp == 0 and self.definition.equal_level_policy == "last_occurrence")
            if not breaks:
                continue
            if existing.active_ref is not None:
                ref = self._allocator.next_ref(self._stream_id)
                events.append(
                    SwingInvalidated(
                        scope=scope,
                        swing_revision=existing.revision,
                        invalidation_cause="market_evolution",
                        causation_refs=(existing.active_ref, candles[idx].ref),
                        recorded_time=recorded_time,
                        ref=ref,
                    )
                )
            self._swings[scope.swing_id] = replace(existing, state="INVALIDATED", active_ref=None)
        return events

    def _advance(
        self, key: _CandleKey, pivot_idx: int, direction: Direction, recorded_time: datetime
    ) -> list[SwingEvent]:
        """Normal (non-correction) streaming progression as new candles append."""
        candles = self._candles[key]
        if pivot_idx >= len(candles) or not self._left_satisfied(candles, pivot_idx, direction):
            return []
        pivot_fact = candles[pivot_idx]
        scope = self._scope_for(key, direction, pivot_fact)
        existing = self._swings.get(scope.swing_id)
        right_ok = self._right_satisfied(candles, pivot_idx, direction)
        pivot_price = self._pivot_price(pivot_fact, direction)

        if existing is None:
            if right_ok:
                return self._emit_confirmed(
                    scope,
                    pivot_idx,
                    pivot_price,
                    recorded_time,
                    revision=1,
                    candidate_ref=None,
                    prior_invalidation_ref=None,
                )
            return self._emit_candidate(
                scope,
                pivot_idx,
                pivot_price,
                recorded_time,
                revision=1,
                prior_invalidation_ref=None,
            )

        if existing.state == "CANDIDATE" and right_ok:
            return self._emit_confirmed(
                scope,
                pivot_idx,
                pivot_price,
                recorded_time,
                revision=existing.revision,
                candidate_ref=existing.candidate_ref,
                prior_invalidation_ref=None,
            )
        return []

    def _recompute_after_correction(
        self, key: _CandleKey, pivot_idx: int, direction: Direction, recorded_time: datetime
    ) -> list[SwingEvent]:
        candles = self._candles[key]
        if pivot_idx >= len(candles):
            return []
        pivot_fact = candles[pivot_idx]
        scope = self._scope_for(key, direction, pivot_fact)
        existing = self._swings.get(scope.swing_id)

        left_ok = self._left_satisfied(candles, pivot_idx, direction)
        right_ok = left_ok and self._right_satisfied(candles, pivot_idx, direction)
        pivot_price = self._pivot_price(pivot_fact, direction)
        new_status: Literal["NONE", "CANDIDATE", "CONFIRMED"] = (
            "CONFIRMED" if right_ok else ("CANDIDATE" if left_ok else "NONE")
        )

        was_active = existing is not None and existing.state in ("CANDIDATE", "CONFIRMED")
        old_status: Literal["NONE", "CANDIDATE", "CONFIRMED"] = existing.state if was_active and existing else "NONE"  # type: ignore[assignment]
        old_price = existing.pivot_price if was_active and existing else None

        if old_status == "NONE" and new_status == "NONE":
            return []
        if was_active and new_status == old_status and old_price == pivot_price:
            return []

        events: list[SwingEvent] = []
        prior_invalidation_ref: EventRecordRef | None = None
        if was_active and existing is not None:
            causation = (existing.active_ref,) if existing.active_ref is not None else ()
            if existing.active_ref is not None:
                ref = self._allocator.next_ref(self._stream_id)
                events.append(
                    SwingInvalidated(
                        scope=scope,
                        swing_revision=existing.revision,
                        invalidation_cause="upstream_correction",
                        causation_refs=causation,
                        recorded_time=recorded_time,
                        ref=ref,
                    )
                )
                prior_invalidation_ref = ref
            self._swings[scope.swing_id] = replace(existing, state="INVALIDATED", active_ref=None)

        if new_status == "NONE":
            return events

        next_revision = (existing.revision + 1) if existing is not None else 1
        if new_status == "CANDIDATE":
            events.extend(
                self._emit_candidate(
                    scope,
                    pivot_idx,
                    pivot_price,
                    recorded_time,
                    revision=next_revision,
                    prior_invalidation_ref=prior_invalidation_ref,
                )
            )
        else:
            events.extend(
                self._emit_confirmed(
                    scope,
                    pivot_idx,
                    pivot_price,
                    recorded_time,
                    revision=next_revision,
                    candidate_ref=None,
                    prior_invalidation_ref=prior_invalidation_ref,
                )
            )
        return events

    # -- emission ---------------------------------------------------------

    def _emit_candidate(
        self,
        scope: SwingScope,
        pivot_idx: int,
        pivot_price: Decimal,
        recorded_time: datetime,
        *,
        revision: int,
        prior_invalidation_ref: EventRecordRef | None,
    ) -> list[SwingEvent]:
        key = (scope.instrument_id, scope.venue_id, scope.timeframe)
        candles = self._candles[key]
        pivot_fact = candles[pivot_idx]
        left_refs = tuple(c.ref for c in candles[pivot_idx - self.definition.left_count : pivot_idx])

        if self._historical:
            self._swings[scope.swing_id] = _SwingState(
                pivot_index=pivot_idx,
                revision=revision,
                state="CANDIDATE",
                candidate_ref=None,
                active_ref=None,
                pivot_price=pivot_price,
            )
            return []

        ref = self._allocator.next_ref(self._stream_id)
        causation = list(left_refs)
        if prior_invalidation_ref is not None:
            causation.append(prior_invalidation_ref)
        event = SwingCandidateDetected(
            scope=scope,
            swing_revision=revision,
            pivot_price=pivot_price,
            pivot_effective_time=(pivot_fact.scope.window_start, pivot_fact.scope.window_end),
            left_evidence_refs=left_refs,
            causation_refs=tuple(causation),
            recorded_time=recorded_time,
            ref=ref,
        )
        self._swings[scope.swing_id] = _SwingState(
            pivot_index=pivot_idx,
            revision=revision,
            state="CANDIDATE",
            candidate_ref=ref,
            active_ref=ref,
            pivot_price=pivot_price,
        )
        return [event]

    def _emit_confirmed(
        self,
        scope: SwingScope,
        pivot_idx: int,
        pivot_price: Decimal,
        recorded_time: datetime,
        *,
        revision: int,
        candidate_ref: EventRecordRef | None,
        prior_invalidation_ref: EventRecordRef | None,
    ) -> list[SwingEvent]:
        key = (scope.instrument_id, scope.venue_id, scope.timeframe)
        candles = self._candles[key]
        pivot_fact = candles[pivot_idx]
        left_refs = tuple(c.ref for c in candles[pivot_idx - self.definition.left_count : pivot_idx])
        right_refs = tuple(c.ref for c in candles[pivot_idx + 1 : pivot_idx + 1 + self.definition.right_count])

        ref = self._allocator.next_ref(self._stream_id)
        causation: list[EventRecordRef]
        if candidate_ref is not None:
            causation = [candidate_ref]
        else:
            causation = [pivot_fact.ref, *left_refs, *right_refs]
        if prior_invalidation_ref is not None:
            causation.append(prior_invalidation_ref)

        event = SwingConfirmed(
            scope=scope,
            swing_revision=revision,
            pivot_price=pivot_price,
            pivot_effective_time=(pivot_fact.scope.window_start, pivot_fact.scope.window_end),
            pivot_candle_ref=pivot_fact.ref,
            left_evidence_refs=left_refs,
            right_evidence_refs=right_refs,
            causation_refs=tuple(causation),
            recorded_time=recorded_time,
            ref=ref,
        )
        self._swings[scope.swing_id] = _SwingState(
            pivot_index=pivot_idx,
            revision=revision,
            state="CONFIRMED",
            candidate_ref=candidate_ref,
            active_ref=ref,
            pivot_price=pivot_price,
        )
        return [event]

    # -- ordering discipline ------------------------------------------------

    def _check_recorded_time(self, recorded_time: datetime) -> None:
        if self._last_recorded_time is not None and recorded_time < self._last_recorded_time:
            raise NonMonotonicRecordedTimeError(
                f"recorded_time {recorded_time} precedes last-seen {self._last_recorded_time}"
            )
        self._last_recorded_time = recorded_time
