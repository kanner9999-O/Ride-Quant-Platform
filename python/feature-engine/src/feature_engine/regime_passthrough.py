"""`volatility_metric`/`directional_persistence_metric` — `upstream_source:
regime` (feature.md §7.1/§7.2).

Exposes a Raw Regime `RegimeClassified.computed_metric` verbatim (after
Feature's own `decimal_precision_policy` normalization only) — never
reclassifies it, never enriches `directional_persistence_metric` into a
Bullish/Bearish/price-action interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .contracts import (
    FeatureComputed,
    FeatureDefinition,
    FeatureEvent,
    FeatureFactInvalidated,
    FeatureScope,
    RecordedTimeSource,
    normalize_input_facts,
)
from .envelope import EventRecordRef
from .errors import (
    DefinitionVersionMismatchError,
    FeatureLineageError,
    ForeignScopeError,
    NonMonotonicRecordedTimeError,
    RecordedTimeSourceViolationError,
    RegimeDimensionMismatchError,
)
from .publish import SequenceAllocator
from .regime_input import RegimeClassifiedFact, RegimeFactInvalidatedFact

_DIMENSION_BY_FEATURE_TYPE = {
    "volatility_metric": "volatility",
    "directional_persistence_metric": "directional_persistence",
}


@dataclass(slots=True)
class _WindowLineage:
    head_fact: FeatureComputed
    invalidated: bool
    last_evidence_ref: EventRecordRef
    pending_invalidation_ref: EventRecordRef | None = None
    pending_invalidation_recorded_time: datetime | None = None


class RegimePassthroughFeatureEngine:
    """One instance per Feature subject. Consumes exactly
    `RegimeClassifiedFact`/`RegimeFactInvalidatedFact` — never
    `RegimeCurrentView`.
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
        if definition.feature_type not in _DIMENSION_BY_FEATURE_TYPE:
            raise ValueError(f"unsupported feature_type for regime pass-through: {definition.feature_type!r}")
        if definition.upstream_source != "regime":
            raise ValueError("RegimePassthroughFeatureEngine requires upstream_source='regime'")
        if scope.feature_type != definition.feature_type or scope.feature_definition_version != (
            definition.feature_definition_version
        ):
            raise ValueError("scope does not match definition")
        self.scope = scope
        self.definition = definition
        self._expected_dimension = _DIMENSION_BY_FEATURE_TYPE[definition.feature_type]
        self._allocator = allocator
        self._time_source = time_source
        self._stream_id = stream_id
        self._last_input_recorded_time: datetime | None = None
        self._lineage: dict[tuple[datetime, datetime], _WindowLineage] = {}

    def _check_scope(self, fact_instrument: str, fact_venue: str, fact_timeframe: str) -> None:
        if (
            fact_instrument != self.scope.instrument_id
            or fact_venue != self.scope.venue_id
            or fact_timeframe != self.scope.timeframe
        ):
            raise ForeignScopeError("regime fact scope does not match this Feature engine's own scope")

    def _check_recorded_time(self, recorded_time: datetime) -> None:
        if self._last_input_recorded_time is not None and recorded_time < self._last_input_recorded_time:
            raise NonMonotonicRecordedTimeError(
                f"recorded_time {recorded_time!r} precedes last-seen {self._last_input_recorded_time!r}"
            )
        self._last_input_recorded_time = recorded_time

    def _next_recorded_time(self, strict_floor: datetime) -> datetime:
        candidate = self._time_source.next_after(strict_floor)
        if not candidate > strict_floor:
            raise RecordedTimeSourceViolationError(
                f"RecordedTimeSource.next_after({strict_floor!r}) returned {candidate!r}, not strictly later"
            )
        return candidate

    def on_regime_classified(self, fact: RegimeClassifiedFact) -> list[FeatureEvent]:
        self._check_scope(fact.instrument_id, fact.venue_id, fact.timeframe)
        if fact.regime_dimension != self._expected_dimension:
            raise RegimeDimensionMismatchError(
                f"expected regime_dimension={self._expected_dimension!r}, got {fact.regime_dimension!r}"
            )
        if fact.regime_definition_version != self.definition.required_upstream_definition_version:
            raise DefinitionVersionMismatchError(
                f"expected regime_definition_version={self.definition.required_upstream_definition_version!r}, "
                f"got {fact.regime_definition_version!r}"
            )
        self._check_recorded_time(fact.recorded_time)

        key = (fact.window_start, fact.window_end)
        existing = self._lineage.get(key)
        if existing is None:
            return self._emit_original(key, fact)
        if not existing.invalidated:
            if fact.ref == existing.last_evidence_ref:
                return []  # duplicate computation idempotency
            raise FeatureLineageError(
                f"received a new RegimeClassified for window {key!r} whose current lineage head is not "
                "pending correction — a replacement must be preceded by RegimeFactInvalidated"
            )
        return self._emit_replacement(key, fact, existing)

    def on_regime_invalidated(self, invalidation: RegimeFactInvalidatedFact) -> list[FeatureEvent]:
        self._check_recorded_time(invalidation.recorded_time)
        match_key: tuple[datetime, datetime] | None = None
        for key, state in self._lineage.items():
            if not state.invalidated and state.last_evidence_ref == invalidation.invalidated_fact_ref:
                match_key = key
                break
        if match_key is None:
            raise FeatureLineageError(
                f"RegimeFactInvalidated targets {invalidation.invalidated_fact_ref!r}, which is not the current "
                "evidence for any non-invalidated window in this engine"
            )
        return self._emit_invalidation(match_key, invalidation)

    def _emit_original(self, key: tuple[datetime, datetime], fact: RegimeClassifiedFact) -> list[FeatureEvent]:
        normalized_refs = normalize_input_facts(
            [fact], effective_time=lambda f: (f.window_start, f.window_end), ref_of=lambda f: f.ref, expected_count=1
        )
        recorded_time = self._next_recorded_time(fact.recorded_time)
        value = self.definition.decimal_precision_policy.apply(fact.computed_metric)
        feature_fact = FeatureComputed(
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
        )
        self._lineage[key] = _WindowLineage(head_fact=feature_fact, invalidated=False, last_evidence_ref=fact.ref)
        return [feature_fact]

    def _emit_invalidation(
        self, key: tuple[datetime, datetime], invalidation: RegimeFactInvalidatedFact
    ) -> list[FeatureEvent]:
        state = self._lineage[key]
        floor = max(state.head_fact.recorded_time, invalidation.recorded_time)
        recorded_time = self._next_recorded_time(floor)
        ref = self._allocator.next_ref(self._stream_id)
        inv = FeatureFactInvalidated(
            scope=state.head_fact.scope,
            invalidated_fact_ref=state.head_fact.ref,
            invalidation_cause="regime_fact_invalidated",
            window_start=state.head_fact.window_start,
            window_end=state.head_fact.window_end,
            causation_refs=(state.head_fact.ref, invalidation.ref),
            recorded_time=recorded_time,
            ref=ref,
        )
        state.invalidated = True
        state.pending_invalidation_ref = ref
        state.pending_invalidation_recorded_time = recorded_time
        return [inv]

    def _emit_replacement(
        self, key: tuple[datetime, datetime], fact: RegimeClassifiedFact, existing: _WindowLineage
    ) -> list[FeatureEvent]:
        normalized_refs = normalize_input_facts(
            [fact], effective_time=lambda f: (f.window_start, f.window_end), ref_of=lambda f: f.ref, expected_count=1
        )
        assert existing.pending_invalidation_recorded_time is not None
        assert existing.pending_invalidation_ref is not None
        recorded_time = self._next_recorded_time(existing.pending_invalidation_recorded_time)
        value = self.definition.decimal_precision_policy.apply(fact.computed_metric)
        replacement = FeatureComputed(
            scope=self.scope,
            value=value,
            unit=self.definition.unit,
            window_start=key[0],
            window_end=key[1],
            input_fact_refs=normalized_refs,
            supersedes_fact_ref=existing.head_fact.ref,
            causation_refs=(*normalized_refs, existing.pending_invalidation_ref),
            recorded_time=recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
        )
        self._lineage[key] = _WindowLineage(head_fact=replacement, invalidated=False, last_evidence_ref=fact.ref)
        return [replacement]
