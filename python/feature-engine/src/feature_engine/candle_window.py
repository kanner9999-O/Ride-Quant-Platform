"""`volatility_metric`/`directional_persistence_metric` — `upstream_source:
candle` (feature.md §7.1/§7.2).

feature.md leaves the concrete Candle-derived formula (ATR/stdev/realized-
volatility/etc.) fully unresolved — this engine is generic over an injected
`FeatureFormula`, identified by `formula_id`, matched fail-closed against the
`FeatureDefinition`'s own pinned `formula_id`. No canonical formula is
chosen or guessed here; if no matching formula is supplied, construction
fails closed (`UnsupportedFeatureFormulaError`) and no computation is ever
possible — a documented, honest, authority-limited implementation boundary,
not a fabricated formula decision.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Protocol

from .candle import CandleFact
from .contracts import (
    FEATURE_COMPUTED_CONTRACT_ID,
    FEATURE_EVENT_CONTRACT_VERSION,
    FEATURE_FACT_INVALIDATED_CONTRACT_ID,
    FeatureComputed,
    FeatureDefinition,
    FeatureEvent,
    FeatureFactInvalidated,
    FeatureScope,
    RecordedTimeSource,
    normalize_input_facts,
)
from .envelope import EventContractRef, EventRecordRef
from .errors import (
    DuplicateCandleConflictError,
    EvidenceReferenceConflictError,
    ForeignScopeError,
    NonMonotonicRecordedTimeError,
    OutOfOrderCandleError,
    OutOfOrderCorrectionError,
    RecordedTimeSourceViolationError,
    UnauthorizedUpstreamContractError,
    UnsupportedFeatureFormulaError,
)
from .publish import SequenceAllocator

_OUTPUT_CONTRACT_REF = EventContractRef(FEATURE_COMPUTED_CONTRACT_ID, FEATURE_EVENT_CONTRACT_VERSION)
_INVALIDATION_CONTRACT_REF = EventContractRef(FEATURE_FACT_INVALIDATED_CONTRACT_ID, FEATURE_EVENT_CONTRACT_VERSION)


class FeatureFormula(Protocol):
    """A bounded, injected metric computation — never resolved from a global
    registry. `formula_id` must match the `FeatureDefinition`'s own
    `formula_id` for the engine to accept it. Test-only implementations must
    use an obviously non-production `formula_id` (e.g. a `test-` prefix) and
    must never be documented as a production canonical formula.
    """

    formula_id: str

    def compute(self, evidence: Sequence[CandleFact]) -> Decimal:
        """Compute the raw (pre-precision-policy) value over one window's
        evidence, supplied in feature.md §8a canonical normalized order.
        """
        ...


@dataclass(slots=True)
class _WindowLineage:
    head_fact: FeatureComputed


class CandleWindowFeatureEngine:
    """One instance per Feature subject. Rolling window over
    `window_candle_count` consecutive, contiguous authoritative Candle
    facts — every completed window emits exactly one `FeatureComputed`, even
    when `value` repeats the previous window's (feature.md §3). Same
    algorithm for streaming and historical/backtest ingestion — no mode
    split.
    """

    def __init__(
        self,
        scope: FeatureScope,
        definition: FeatureDefinition,
        formula: FeatureFormula,
        allocator: SequenceAllocator,
        time_source: RecordedTimeSource,
        *,
        stream_id: str = "feature",
    ) -> None:
        if definition.feature_type not in ("volatility_metric", "directional_persistence_metric"):
            raise ValueError(f"unsupported feature_type for candle-window engine: {definition.feature_type!r}")
        if definition.upstream_source != "candle":
            raise ValueError("CandleWindowFeatureEngine requires upstream_source='candle'")
        if scope.feature_type != definition.feature_type or scope.feature_definition_version != (
            definition.feature_definition_version
        ):
            raise ValueError("scope does not match definition")
        if formula.formula_id != definition.formula_id:
            raise UnsupportedFeatureFormulaError(
                f"formula.formula_id={formula.formula_id!r} does not match "
                f"definition.formula_id={definition.formula_id!r}"
            )
        assert definition.window_candle_count is not None
        self.scope = scope
        self.definition = definition
        self._window_candle_count = definition.window_candle_count
        self._formula = formula
        self._allocator = allocator
        self._time_source = time_source
        self._stream_id = stream_id
        self._candles: list[CandleFact] = []
        self._candle_index: dict[str, int] = {}
        self._last_recorded_time: datetime | None = None
        self._lineage: dict[tuple[datetime, datetime], _WindowLineage] = {}

    def _check_scope(self, candle: CandleFact) -> None:
        if (
            candle.scope.instrument_id != self.scope.instrument_id
            or candle.scope.venue_id != self.scope.venue_id
            or candle.scope.timeframe != self.scope.timeframe
        ):
            raise ForeignScopeError(f"candle scope {candle.scope!r} does not match engine scope {self.scope!r}")

    def _check_contract(self, candle: CandleFact) -> None:
        assert self.definition.upstream_contract_refs is not None
        if candle.event_contract_ref not in self.definition.upstream_contract_refs:
            raise UnauthorizedUpstreamContractError(
                f"candle event_contract_ref={candle.event_contract_ref!r} is not one of "
                f"definition.upstream_contract_refs={self.definition.upstream_contract_refs!r}"
            )

    def _check_recorded_time(self, recorded_time: datetime) -> None:
        if self._last_recorded_time is not None and recorded_time < self._last_recorded_time:
            raise NonMonotonicRecordedTimeError(
                f"recorded_time {recorded_time!r} precedes last-seen {self._last_recorded_time!r}"
            )
        self._last_recorded_time = recorded_time

    def _next_recorded_time(self, strict_floor: datetime) -> datetime:
        candidate = self._time_source.next_after(strict_floor)
        if not candidate > strict_floor:
            raise RecordedTimeSourceViolationError(
                f"RecordedTimeSource.next_after({strict_floor!r}) returned {candidate!r}, not strictly later"
            )
        return candidate

    def on_candle(self, fact: CandleFact) -> list[FeatureEvent]:
        self._check_scope(fact)
        self._check_contract(fact)
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
            self._check_recorded_time(fact.recorded_time)
            self._candles[existing_index] = fact
            return self._reevaluate_windows_covering(existing_index, fact.ref, fact.recorded_time)

        if fact.is_correction:
            raise OutOfOrderCorrectionError(f"correction submitted for never-seen candle {subject_id!r}")
        if self._candles and fact.scope.window_start < self._candles[-1].scope.window_start:
            raise OutOfOrderCandleError(
                f"candle window_start {fact.scope.window_start!r} precedes last-seen "
                f"{self._candles[-1].scope.window_start!r}"
            )
        self._check_recorded_time(fact.recorded_time)
        self._candles.append(fact)
        new_index = len(self._candles) - 1
        self._candle_index[subject_id] = new_index
        return self._try_classify_window_ending_at(new_index)

    @staticmethod
    def _window_is_contiguous(window: Sequence[CandleFact]) -> bool:
        return all(window[i].scope.window_start == window[i - 1].scope.window_end for i in range(1, len(window)))

    def _try_classify_window_ending_at(self, end_index: int) -> list[FeatureEvent]:
        n = self._window_candle_count
        if end_index + 1 < n:
            return []  # warm-up not yet satisfied — valid absence, not an error
        window = self._candles[end_index - n + 1 : end_index + 1]
        if not self._window_is_contiguous(window):
            return []  # gap — valid absence until it resolves
        key = (window[0].scope.window_start, window[-1].scope.window_end)
        return self._emit_original_fact(key, window)

    def _reevaluate_windows_covering(
        self, corrected_index: int, correction_ref: EventRecordRef, correction_recorded_time: datetime
    ) -> list[FeatureEvent]:
        n = self._window_candle_count
        lowest_end = max(n - 1, corrected_index)
        highest_end = min(len(self._candles) - 1, corrected_index + n - 1)
        events: list[FeatureEvent] = []
        for end_index in range(lowest_end, highest_end + 1):
            window = self._candles[end_index - n + 1 : end_index + 1]
            if not self._window_is_contiguous(window):
                continue
            key = (window[0].scope.window_start, window[-1].scope.window_end)
            existing = self._lineage.get(key)
            if existing is None:
                events.extend(self._emit_original_fact(key, window))
            else:
                events.extend(
                    self._emit_correction_pair(key, window, correction_ref, correction_recorded_time, existing)
                )
        return events

    def _emit_original_fact(self, key: tuple[datetime, datetime], window: Sequence[CandleFact]) -> list[FeatureEvent]:
        normalized_refs = normalize_input_facts(
            window,
            effective_time=lambda c: (c.scope.window_start, c.scope.window_end),
            ref_of=lambda c: c.ref,
            expected_count=self._window_candle_count,
        )
        floor = max(candle.recorded_time for candle in window)
        recorded_time = self._next_recorded_time(floor)
        raw_value = self._formula.compute(tuple(window))
        value = self.definition.decimal_precision_policy.apply(raw_value)
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
        self._lineage[key] = _WindowLineage(head_fact=fact)
        return [fact]

    def _emit_correction_pair(
        self,
        key: tuple[datetime, datetime],
        window: Sequence[CandleFact],
        correction_ref: EventRecordRef,
        correction_recorded_time: datetime,
        existing: _WindowLineage,
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

        normalized_refs = normalize_input_facts(
            window,
            effective_time=lambda c: (c.scope.window_start, c.scope.window_end),
            ref_of=lambda c: c.ref,
            expected_count=self._window_candle_count,
        )
        raw_value = self._formula.compute(tuple(window))
        value = self.definition.decimal_precision_policy.apply(raw_value)
        replacement_recorded_time = self._next_recorded_time(invalidation_recorded_time)
        replacement = FeatureComputed(
            scope=self.scope,
            value=value,
            unit=self.definition.unit,
            window_start=key[0],
            window_end=key[1],
            input_fact_refs=normalized_refs,
            supersedes_fact_ref=existing.head_fact.ref,
            causation_refs=(*normalized_refs, invalidation.ref),
            recorded_time=replacement_recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
            event_contract_ref=_OUTPUT_CONTRACT_REF,
        )
        self._lineage[key] = _WindowLineage(head_fact=replacement)
        return [invalidation, replacement]
