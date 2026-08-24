"""`distance_to_last_confirmed_swing` (feature.md §7.3/§9a).

Exactly one reference Candle + exactly one Eligible Swing, selected via the
mandatory 5-step ordered filter pipeline (identity/scope match,
recorded-time visibility, effective-time cutoff STRICT `<`, latest valid
revision, not invalidated) followed by an 8-criterion deterministic total
order — never the reverse: the total order NEVER runs on a candidate that
failed the filter pipeline, and never "resurrects" an effective-time
ineligible Swing. Never consumes Structure `BreakOfStructureDetected`/
`ChangeOfCharacterDetected`/`StructureFactInvalidated`/`StructureRecomputed`
— only re-uses `structure.md` §6a's total-order *methodology*, as
feature.md §9a itself requires.

`distance_representation="signed"`: feature.md §6/§7.3 leaves the sign
orientation of `signed` genuinely unpinned — no authoritative convention
exists anywhere in the Domain Contract for which direction is positive.
This engine does NOT invent one; it fails closed
(`UnsupportedDistanceRepresentationError`) at construction time for
`signed`, and only computes `distance_representation="absolute"` (an
unambiguous, orientation-independent magnitude).

Contract qualification: feature.md §14 pins the closed set of upstream
contract IDs Feature may consume for this path (`candle-closed`/
`candle-corrected` for the reference Candle, `swing-confirmed`/
`swing-invalidated` for the Swing side) — every ingested fact's
`event_contract_ref.contract_id` is validated against this fixed set,
fail-closed otherwise. (feature.md §6 scopes the definition-level
`upstream_contract_refs` field to the two metric feature types only — this
path has no per-definition contract-version pin to validate against, so
only the fixed §14 contract-ID set is enforced here, not a specific
version.)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .candle import CandleFact
from .contracts import (
    CANDLE_CLOSED_CONTRACT_ID,
    CANDLE_CORRECTED_CONTRACT_ID,
    FEATURE_COMPUTED_CONTRACT_ID,
    FEATURE_EVENT_CONTRACT_VERSION,
    FEATURE_FACT_INVALIDATED_CONTRACT_ID,
    SWING_CONFIRMED_CONTRACT_ID,
    SWING_INVALIDATED_CONTRACT_ID,
    FeatureComputed,
    FeatureDefinition,
    FeatureEvent,
    FeatureFactInvalidated,
    FeatureScope,
    RecordedTimeSource,
)
from .envelope import EventContractRef, EventRecordRef
from .errors import (
    DuplicateCandleConflictError,
    EvidenceCardinalityError,
    EvidenceReferenceConflictError,
    ForeignScopeError,
    InvalidSwingEligibilityInputError,
    NonMonotonicRecordedTimeError,
    OutOfOrderCandleError,
    OutOfOrderCorrectionError,
    RecordedTimeSourceViolationError,
    UnauthorizedUpstreamContractError,
    UnsupportedDistanceRepresentationError,
)
from .publish import SequenceAllocator
from .swing_input import SwingConfirmedFact, SwingInvalidatedFact

_REGISTRY_VERSION = "v0"
_OUTPUT_CONTRACT_REF = EventContractRef(FEATURE_COMPUTED_CONTRACT_ID, FEATURE_EVENT_CONTRACT_VERSION)
_INVALIDATION_CONTRACT_REF = EventContractRef(FEATURE_FACT_INVALIDATED_CONTRACT_ID, FEATURE_EVENT_CONTRACT_VERSION)
_ALLOWED_CANDLE_CONTRACT_IDS = frozenset({CANDLE_CLOSED_CONTRACT_ID, CANDLE_CORRECTED_CONTRACT_ID})
_ALLOWED_SWING_CONTRACT_IDS = frozenset({SWING_CONFIRMED_CONTRACT_ID, SWING_INVALIDATED_CONTRACT_ID})


@dataclass(slots=True)
class _SwingState:
    revision: int
    invalidated: bool
    pivot_price: Decimal
    pivot_effective_time: tuple[datetime, datetime]
    recorded_time: datetime
    ref: EventRecordRef


@dataclass(slots=True)
class _WindowLineage:
    head_fact: FeatureComputed
    invalidated: bool
    used_swing_id: str
    pending_invalidation_ref: EventRecordRef | None = None
    pending_invalidation_recorded_time: datetime | None = None


def _total_order_key(swing_id: str, state: _SwingState) -> tuple[float, datetime, str, str, int, int, str, str]:
    """feature.md §9a's 8-criterion deterministic total order, applied ONLY
    to candidates that already passed the 5-step filter pipeline. DESC
    criteria (pivot window_start, swing_revision) are encoded as negated
    values so the overall winner is the lexicographic MINIMUM of this key.
    """
    return (
        -state.pivot_effective_time[0].timestamp(),
        state.recorded_time,
        state.ref.stream_id,
        _REGISTRY_VERSION,
        state.ref.sequence,
        -state.revision,
        swing_id,
        state.ref.event_id,
    )


class SwingDistanceFeatureEngine:
    """One instance per Feature subject. Each authoritative reference Candle
    produces at most one `FeatureComputed`, independently — no window
    aggregation across multiple candles.
    """

    def __init__(
        self,
        scope: FeatureScope,
        definition: FeatureDefinition,
        allocator: SequenceAllocator,
        time_source: RecordedTimeSource,
        *,
        stream_id: str = "feature",
    ) -> None:
        if definition.feature_type != "distance_to_last_confirmed_swing":
            raise ValueError(f"unsupported feature_type: {definition.feature_type!r}")
        if scope.feature_type != definition.feature_type or scope.feature_definition_version != (
            definition.feature_definition_version
        ):
            raise ValueError("scope does not match definition")
        if definition.distance_representation == "signed":
            raise UnsupportedDistanceRepresentationError(
                "distance_representation='signed' has no authoritative sign-orientation convention pinned "
                "anywhere in feature.md §6/§7.3 — this engine does not invent one; only "
                "distance_representation='absolute' is currently computable"
            )
        self.scope = scope
        self.definition = definition
        self._allocator = allocator
        self._time_source = time_source
        self._stream_id = stream_id
        self._candles: list[CandleFact] = []
        self._candle_index: dict[str, int] = {}
        self._candle_by_window: dict[tuple[datetime, datetime], CandleFact] = {}
        # Candle and Swing are independent upstream streams (Chapter 8 §8.3.3 — no
        # invented global cross-stream order); a Swing confirmation can be recorded
        # much later than its own pivot (right-side evidence accumulation), with no
        # required interleaving relationship to Candle recorded_time at all. Each
        # stream's own monotonicity is tracked and enforced independently.
        self._last_candle_recorded_time: datetime | None = None
        self._last_swing_recorded_time: datetime | None = None
        self._swings: dict[str, _SwingState] = {}
        self._lineage: dict[tuple[datetime, datetime], _WindowLineage] = {}

    # -- shared ordering / recorded-time causality -----------------------

    def _check_candle_scope(self, candle: CandleFact) -> None:
        if (
            candle.scope.instrument_id != self.scope.instrument_id
            or candle.scope.venue_id != self.scope.venue_id
            or candle.scope.timeframe != self.scope.timeframe
        ):
            raise ForeignScopeError(f"candle scope {candle.scope!r} does not match engine scope {self.scope!r}")

    @staticmethod
    def _check_candle_contract(candle: CandleFact) -> None:
        if candle.event_contract_ref.contract_id not in _ALLOWED_CANDLE_CONTRACT_IDS:
            raise UnauthorizedUpstreamContractError(
                f"candle event_contract_ref.contract_id={candle.event_contract_ref.contract_id!r} is not one of "
                f"{sorted(_ALLOWED_CANDLE_CONTRACT_IDS)!r} (feature.md §14)"
            )

    @staticmethod
    def _check_swing_contract(contract_ref: EventContractRef) -> None:
        if contract_ref.contract_id not in _ALLOWED_SWING_CONTRACT_IDS:
            raise UnauthorizedUpstreamContractError(
                f"swing event_contract_ref.contract_id={contract_ref.contract_id!r} is not one of "
                f"{sorted(_ALLOWED_SWING_CONTRACT_IDS)!r} (feature.md §14)"
            )

    def _check_candle_recorded_time(self, recorded_time: datetime) -> None:
        if self._last_candle_recorded_time is not None and recorded_time < self._last_candle_recorded_time:
            raise NonMonotonicRecordedTimeError(
                f"candle recorded_time {recorded_time!r} precedes last-seen {self._last_candle_recorded_time!r}"
            )
        self._last_candle_recorded_time = recorded_time

    def _check_swing_recorded_time(self, recorded_time: datetime) -> None:
        if self._last_swing_recorded_time is not None and recorded_time < self._last_swing_recorded_time:
            raise NonMonotonicRecordedTimeError(
                f"swing recorded_time {recorded_time!r} precedes last-seen {self._last_swing_recorded_time!r}"
            )
        self._last_swing_recorded_time = recorded_time

    def _next_recorded_time(self, strict_floor: datetime) -> datetime:
        candidate = self._time_source.next_after(strict_floor)
        if not candidate > strict_floor:
            raise RecordedTimeSourceViolationError(
                f"RecordedTimeSource.next_after({strict_floor!r}) returned {candidate!r}, not strictly later"
            )
        return candidate

    # -- Swing ingestion ---------------------------------------------------

    def on_swing_confirmed(self, fact: SwingConfirmedFact) -> list[FeatureEvent]:
        if (
            fact.instrument_id != self.scope.instrument_id
            or fact.venue_id != self.scope.venue_id
            or fact.timeframe != self.scope.timeframe
        ):
            raise ForeignScopeError("SwingConfirmed scope does not match this Feature engine's own scope")
        if fact.swing_definition_version != self.definition.required_swing_definition_version:
            raise InvalidSwingEligibilityInputError(
                f"expected swing_definition_version={self.definition.required_swing_definition_version!r}, "
                f"got {fact.swing_definition_version!r}"
            )
        if fact.direction != self.definition.swing_direction:
            raise InvalidSwingEligibilityInputError(
                f"expected swing_direction={self.definition.swing_direction!r}, got {fact.direction!r}"
            )
        self._check_swing_contract(fact.event_contract_ref)
        self._check_swing_recorded_time(fact.recorded_time)

        existing = self._swings.get(fact.swing_id)
        if existing is not None and existing.ref == fact.ref:
            return []  # duplicate delivery of the identical authoritative event

        # swing.md §1a: swing_revision starts at 1 and a revision N+1 is only valid
        # once revision N has been EXPLICITLY invalidated in this engine's own
        # tracked state — Feature independently enforces this ordering, never
        # trusting that the producer's own causation chain alone is sufficient.
        if existing is None:
            if fact.swing_revision != 1:
                raise InvalidSwingEligibilityInputError(
                    f"swing_id {fact.swing_id!r} first-seen revision must be 1, got {fact.swing_revision!r}"
                )
        else:
            if not existing.invalidated:
                raise InvalidSwingEligibilityInputError(
                    f"swing_id {fact.swing_id!r} revision {fact.swing_revision!r} received before revision "
                    f"{existing.revision!r} was explicitly invalidated"
                )
            if fact.swing_revision != existing.revision + 1:
                raise InvalidSwingEligibilityInputError(
                    f"swing_id {fact.swing_id!r} revision must advance by exactly one: expected "
                    f"{existing.revision + 1!r}, got {fact.swing_revision!r}"
                )

        self._swings[fact.swing_id] = _SwingState(
            revision=fact.swing_revision,
            invalidated=False,
            pivot_price=fact.pivot_price,
            pivot_effective_time=fact.pivot_effective_time,
            recorded_time=fact.recorded_time,
            ref=fact.ref,
        )
        # feature.md §9a: a newly-visible Swing revision may resolve a Feature
        # window that was left PENDING_CORRECTION because no eligible Swing existed
        # at the time it was invalidated — re-evaluate every currently-pending
        # window now that this revision is visible.
        return self._reattempt_pending_windows(fact.recorded_time)

    def on_swing_invalidated(self, invalidation: SwingInvalidatedFact) -> list[FeatureEvent]:
        state = self._swings.get(invalidation.swing_id)
        if state is None or state.revision != invalidation.swing_revision or state.invalidated:
            raise InvalidSwingEligibilityInputError(
                f"SwingInvalidated targets ({invalidation.swing_id!r}, {invalidation.swing_revision!r}), which is "
                "not the current non-invalidated revision tracked by this engine"
            )
        self._check_swing_contract(invalidation.event_contract_ref)
        self._check_swing_recorded_time(invalidation.recorded_time)
        state.invalidated = True

        events: list[FeatureEvent] = []
        for key, lineage in list(self._lineage.items()):
            if lineage.invalidated or lineage.used_swing_id != invalidation.swing_id:
                continue
            events.extend(self._invalidate_and_reattempt(key, lineage, invalidation.ref, invalidation.recorded_time))
        return events

    # -- Candle ingestion ---------------------------------------------------

    def on_candle(self, fact: CandleFact) -> list[FeatureEvent]:
        self._check_candle_scope(fact)
        self._check_candle_contract(fact)
        subject_id = fact.scope.subject_id
        existing_index = self._candle_index.get(subject_id)

        if existing_index is not None:
            existing = self._candles[existing_index]
            if existing.ref == fact.ref:
                if existing.ohlcv != fact.ohlcv:
                    raise EvidenceReferenceConflictError(
                        f"candle ref {fact.ref!r} resolves to conflicting OHLCV content ({existing.ohlcv!r} vs "
                        f"{fact.ohlcv!r})"
                    )
                return []  # duplicate delivery of the identical authoritative event
            if not fact.is_correction:
                raise DuplicateCandleConflictError(
                    f"candle {subject_id!r} resubmitted with a different ref but is_correction=False"
                )
            # A distinct correction ref MUST enter lineage even when the recomputed
            # value/payload is unchanged (feature.md §3 "no shortcut") — dedup is
            # keyed on ref identity only, never on value/content equality.
            self._check_candle_recorded_time(fact.recorded_time)
            self._candles[existing_index] = fact
            self._candle_by_window[(fact.scope.window_start, fact.scope.window_end)] = fact
            return self._recompute(fact, correction_ref=fact.ref, correction_recorded_time=fact.recorded_time)

        if fact.is_correction:
            raise OutOfOrderCorrectionError(f"correction submitted for never-seen candle {subject_id!r}")
        if self._candles and fact.scope.window_start < self._candles[-1].scope.window_start:
            raise OutOfOrderCandleError(
                f"candle window_start {fact.scope.window_start!r} precedes last-seen "
                f"{self._candles[-1].scope.window_start!r}"
            )
        self._check_candle_recorded_time(fact.recorded_time)
        self._candles.append(fact)
        self._candle_index[subject_id] = len(self._candles) - 1
        self._candle_by_window[(fact.scope.window_start, fact.scope.window_end)] = fact
        return self._recompute(fact, correction_ref=None, correction_recorded_time=None)

    # -- eligible-swing selection (feature.md §9a) --------------------------

    def _select_eligible_swing(self, reference_cutoff: datetime, cursor: datetime) -> tuple[str, _SwingState] | None:
        """`cursor` is the explicit, machine-enforced computation cursor `R`
        (feature.md §9a step 2) — the recorded_time of whichever event is
        triggering THIS evaluation. A Swing is a candidate only if it is
        BOTH recorded-time visible at `R` AND effective-time eligible; never
        one condition alone (feature.md §12 "hai điều kiện ĐỘC LẬP").
        """
        candidates = [
            (swing_id, state)
            for swing_id, state in self._swings.items()
            if not state.invalidated
            and state.recorded_time <= cursor
            and state.pivot_effective_time[0] < reference_cutoff
        ]
        if not candidates:
            return None
        return min(candidates, key=lambda item: _total_order_key(item[0], item[1]))

    # -- evidence normalization (candle + swing, heterogeneous pair) --------

    @staticmethod
    def _normalize_evidence(
        candle: CandleFact, swing_ref: EventRecordRef, swing_effective: tuple[datetime, datetime]
    ) -> tuple[EventRecordRef, ...]:
        if candle.ref == swing_ref:
            raise EvidenceReferenceConflictError(f"candle ref and swing ref collide: {candle.ref!r}")
        items = [
            (candle.scope.window_start, candle.scope.window_end, candle.ref),
            (swing_effective[0], swing_effective[1], swing_ref),
        ]

        def _sort_key(item: tuple[datetime, datetime, EventRecordRef]) -> tuple[datetime, datetime, str, str, int, str]:
            start, end, ref = item
            return (start, end, ref.stream_id, _REGISTRY_VERSION, ref.sequence, ref.event_id)

        items.sort(key=_sort_key)
        refs = tuple(item[2] for item in items)
        if len(set(refs)) != 2:
            raise EvidenceCardinalityError(f"expected exactly 2 unique evidence refs, got {len(set(refs))}")
        return refs

    def _compute_distance(self, candle: CandleFact, state: _SwingState) -> Decimal:
        assert self.definition.reference_price_field is not None
        assert self.definition.distance_representation == "absolute"
        reference_price = candle.ohlcv.field(self.definition.reference_price_field)
        raw = abs(reference_price - state.pivot_price)
        return self.definition.decimal_precision_policy.apply(raw)

    # -- computation orchestration -------------------------------------------

    def _recompute(
        self,
        candle: CandleFact,
        *,
        correction_ref: EventRecordRef | None,
        correction_recorded_time: datetime | None,
    ) -> list[FeatureEvent]:
        key = (candle.scope.window_start, candle.scope.window_end)
        winner = self._select_eligible_swing(candle.scope.window_end, candle.recorded_time)
        existing = self._lineage.get(key)

        if winner is None:
            return []  # valid absence — no eligible Swing

        swing_id, state = winner

        if existing is None:
            return self._emit_original(key, candle, swing_id, state)

        if not existing.invalidated:
            # Reaching here means an unchanged lineage already exists for this exact window and this
            # call is a genuine candle correction (feature.md §3: no shortcut, even if value is unchanged).
            assert correction_ref is not None and correction_recorded_time is not None
            return self._invalidate_and_replace(
                key,
                candle,
                swing_id,
                state,
                existing,
                correction_ref=correction_ref,
                correction_recorded_time=correction_recorded_time,
            )

        # existing.invalidated: a pending window (from a prior Swing invalidation) is being retried
        # because the reference Candle itself is also being corrected right now.
        assert existing.pending_invalidation_ref is not None
        assert existing.pending_invalidation_recorded_time is not None
        return self._emit_replacement_only(
            key, candle, swing_id, state, existing.pending_invalidation_ref, existing.pending_invalidation_recorded_time
        )

    def _emit_original(
        self, key: tuple[datetime, datetime], candle: CandleFact, swing_id: str, state: _SwingState
    ) -> list[FeatureEvent]:
        normalized_refs = self._normalize_evidence(candle, state.ref, state.pivot_effective_time)
        floor = max(candle.recorded_time, state.recorded_time)
        recorded_time = self._next_recorded_time(floor)
        value = self._compute_distance(candle, state)
        fact = FeatureComputed(
            scope=self.scope,
            value=value,
            unit=self.definition.unit,
            window_start=key[0],
            window_end=key[1],
            input_fact_refs=normalized_refs,
            supersedes_fact_ref=None,
            causation_refs=normalized_refs,
            recorded_time=recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
            event_contract_ref=_OUTPUT_CONTRACT_REF,
        )
        self._lineage[key] = _WindowLineage(head_fact=fact, invalidated=False, used_swing_id=swing_id)
        return [fact]

    def _invalidate_and_replace(
        self,
        key: tuple[datetime, datetime],
        candle: CandleFact,
        swing_id: str,
        state: _SwingState,
        existing: _WindowLineage,
        *,
        correction_ref: EventRecordRef,
        correction_recorded_time: datetime,
    ) -> list[FeatureEvent]:
        invalidation_floor = max(existing.head_fact.recorded_time, correction_recorded_time)
        invalidation_recorded_time = self._next_recorded_time(invalidation_floor)
        invalidation = FeatureFactInvalidated(
            scope=existing.head_fact.scope,
            invalidated_fact_ref=existing.head_fact.ref,
            invalidation_cause="candle_corrected",
            window_start=existing.head_fact.window_start,
            window_end=existing.head_fact.window_end,
            causation_refs=(existing.head_fact.ref, correction_ref),
            recorded_time=invalidation_recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
            event_contract_ref=_INVALIDATION_CONTRACT_REF,
        )
        events: list[FeatureEvent] = [invalidation]
        events.extend(
            self._emit_replacement_only(key, candle, swing_id, state, invalidation.ref, invalidation_recorded_time)
        )
        return events

    def _emit_replacement_only(
        self,
        key: tuple[datetime, datetime],
        candle: CandleFact,
        swing_id: str,
        state: _SwingState,
        invalidation_ref: EventRecordRef,
        invalidation_recorded_time: datetime,
    ) -> list[FeatureEvent]:
        existing = self._lineage[key]
        normalized_refs = self._normalize_evidence(candle, state.ref, state.pivot_effective_time)
        # Floor on ALL of: the invalidation this replaces, AND both pieces of its own
        # evidence's recorded_time — a replacement triggered by a newly-visible Swing
        # revision (§9a reattempt) must not be recorded_time-earlier than that Swing's
        # own recorded_time, even if it happens to exceed the older invalidation floor.
        floor = max(invalidation_recorded_time, candle.recorded_time, state.recorded_time)
        recorded_time = self._next_recorded_time(floor)
        value = self._compute_distance(candle, state)
        replacement = FeatureComputed(
            scope=self.scope,
            value=value,
            unit=self.definition.unit,
            window_start=key[0],
            window_end=key[1],
            input_fact_refs=normalized_refs,
            supersedes_fact_ref=existing.head_fact.ref,
            causation_refs=(*normalized_refs, invalidation_ref),
            recorded_time=recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
            event_contract_ref=_OUTPUT_CONTRACT_REF,
        )
        self._lineage[key] = _WindowLineage(head_fact=replacement, invalidated=False, used_swing_id=swing_id)
        return [replacement]

    def _invalidate_and_reattempt(
        self,
        key: tuple[datetime, datetime],
        lineage: _WindowLineage,
        correction_ref: EventRecordRef,
        correction_recorded_time: datetime,
    ) -> list[FeatureEvent]:
        invalidation_floor = max(lineage.head_fact.recorded_time, correction_recorded_time)
        invalidation_recorded_time = self._next_recorded_time(invalidation_floor)
        invalidation = FeatureFactInvalidated(
            scope=lineage.head_fact.scope,
            invalidated_fact_ref=lineage.head_fact.ref,
            invalidation_cause="swing_invalidated",
            window_start=lineage.head_fact.window_start,
            window_end=lineage.head_fact.window_end,
            causation_refs=(lineage.head_fact.ref, correction_ref),
            recorded_time=invalidation_recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
            event_contract_ref=_INVALIDATION_CONTRACT_REF,
        )
        lineage.invalidated = True
        lineage.pending_invalidation_ref = invalidation.ref
        lineage.pending_invalidation_recorded_time = invalidation_recorded_time
        events: list[FeatureEvent] = [invalidation]

        candle = self._candle_by_window[key]
        winner = self._select_eligible_swing(candle.scope.window_end, invalidation_recorded_time)
        if winner is not None:
            swing_id, state = winner
            events.extend(
                self._emit_replacement_only(key, candle, swing_id, state, invalidation.ref, invalidation_recorded_time)
            )
        return events

    def _reattempt_pending_windows(self, cursor: datetime) -> list[FeatureEvent]:
        """feature.md §9a: re-evaluate every window still PENDING_CORRECTION
        (invalidated, no replacement yet emitted) now that `cursor` — the
        recorded_time of the Swing confirmation that just became visible —
        may make a previously-unavailable eligible Swing selectable. Bounded
        scope: only reattempts windows that ALREADY have a lineage entry
        (an existing prior computation later invalidated); never a
        retroactive scan of Candle windows that never had any lineage at
        all (same deliberate scope boundary as `_invalidate_and_reattempt`).
        """
        events: list[FeatureEvent] = []
        for key, lineage in list(self._lineage.items()):
            if not lineage.invalidated:
                continue
            candle = self._candle_by_window.get(key)
            if candle is None:
                continue
            winner = self._select_eligible_swing(candle.scope.window_end, cursor)
            if winner is None:
                continue
            assert lineage.pending_invalidation_ref is not None
            assert lineage.pending_invalidation_recorded_time is not None
            swing_id, state = winner
            events.extend(
                self._emit_replacement_only(
                    key,
                    candle,
                    swing_id,
                    state,
                    lineage.pending_invalidation_ref,
                    lineage.pending_invalidation_recorded_time,
                )
            )
        return events
