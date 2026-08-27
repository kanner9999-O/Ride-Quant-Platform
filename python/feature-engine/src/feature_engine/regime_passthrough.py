"""`volatility_metric`/`directional_persistence_metric` — `upstream_source:
regime` (feature.md §7.1/§7.2).

Exposes a Raw Regime `RegimeClassified.computed_metric` verbatim (after
Feature's own `decimal_precision_policy` normalization only) — never
reclassifies it, never enriches `directional_persistence_metric` into a
Bullish/Bearish/price-action interpretation.

Computation cursor (P3-FEATURE-A-MAJ-06, ADR-035 Approved): `on_regime_
classified`/`on_regime_invalidated` both take an explicit, required
`cursor: EvaluationFrontier` keyword argument — the caller-certified
computation frontier captured verbatim, together with this engine's own
bound `input_contract_ref`, into every emitted fact's `computation_cursor`.
This engine never substitutes a process-local datetime, an invented
registry value, or an incomplete Feature-local surrogate.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .contracts import (
    ComputationCursor,
    EvaluationFrontier,
    FeatureComputed,
    FeatureDefinition,
    FeatureEvent,
    FeatureFactInvalidated,
    FeatureScope,
    InputContractRef,
    RecordedTimeSource,
    normalize_input_facts,
    resolve_computation_cursor,
    resolve_input_contract_ref,
    resolve_output_contract_refs,
    resolve_stream_registry_version,
)
from .envelope import EventContractRef, EventRecordRef
from .errors import (
    DefinitionVersionMismatchError,
    EvidenceReferenceConflictError,
    FeatureLineageError,
    ForeignScopeError,
    NonMonotonicRecordedTimeError,
    RecordedTimeSourceViolationError,
    RegimeDimensionMismatchError,
    UnauthorizedUpstreamContractError,
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
    last_evidence_fact: RegimeClassifiedFact
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
        feature_event_contract_version: str,
        input_contract_ref: InputContractRef,
        stream_registry_version: str,
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
        self._output_contract_ref, self._invalidation_contract_ref = resolve_output_contract_refs(
            feature_event_contract_version
        )
        self._input_contract_ref = resolve_input_contract_ref(input_contract_ref)
        self._stream_registry_version = resolve_stream_registry_version(stream_registry_version)
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

    def _check_contract(self, event_contract_ref: EventContractRef) -> None:
        assert self.definition.upstream_contract_refs is not None
        if event_contract_ref not in self.definition.upstream_contract_refs:
            raise UnauthorizedUpstreamContractError(
                f"regime fact event_contract_ref={event_contract_ref!r} is not one of "
                f"definition.upstream_contract_refs={self.definition.upstream_contract_refs!r}"
            )

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

    def _resolve_cursor(self, frontier: EvaluationFrontier) -> ComputationCursor:
        """P3-FEATURE-A-MAJ-06: the single place this engine assembles its own
        outbound `computation_cursor` from a caller-supplied `EvaluationFrontier`
        — fails closed (`RegistryContractMismatchError`) if the frontier's
        registry version does not match this engine's bound Input Contract.
        """
        return resolve_computation_cursor(
            frontier,
            input_contract_ref=self._input_contract_ref,
            expected_stream_registry_version=self._stream_registry_version,
        )

    def on_regime_classified(
        self, fact: RegimeClassifiedFact, *, cursor: EvaluationFrontier
    ) -> list[FeatureEvent]:
        """`cursor` is the explicit, caller-certified `EvaluationFrontier`
        (P3-FEATURE-A-MAJ-06) captured verbatim into this fact's own
        `computation_cursor` — never implicitly derived from
        `fact.recorded_time`.
        """
        self._check_scope(fact.instrument_id, fact.venue_id, fact.timeframe)
        self._check_contract(fact.event_contract_ref)
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
            return self._emit_original(key, fact, cursor)
        if not existing.invalidated:
            if fact.ref == existing.last_evidence_ref:
                if fact != existing.last_evidence_fact:
                    raise EvidenceReferenceConflictError(
                        f"ref {fact.ref!r} resolves to conflicting RegimeClassified content "
                        f"({existing.last_evidence_fact!r} vs {fact!r})"
                    )
                return []  # duplicate delivery of the identical authoritative event
            raise FeatureLineageError(
                f"received a new RegimeClassified for window {key!r} whose current lineage head is not "
                "pending correction — a replacement must be preceded by RegimeFactInvalidated"
            )
        return self._emit_replacement(key, fact, existing, cursor)

    def on_regime_invalidated(
        self, invalidation: RegimeFactInvalidatedFact, *, cursor: EvaluationFrontier
    ) -> list[FeatureEvent]:
        """`cursor` is the explicit, caller-certified `EvaluationFrontier`
        (P3-FEATURE-A-MAJ-06) captured verbatim into this invalidation's own
        `computation_cursor` — never implicitly derived from
        `invalidation.recorded_time`.
        """
        self._check_contract(invalidation.event_contract_ref)
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
        return self._emit_invalidation(match_key, invalidation, cursor)

    def _emit_original(
        self, key: tuple[datetime, datetime], fact: RegimeClassifiedFact, cursor: EvaluationFrontier
    ) -> list[FeatureEvent]:
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
            event_contract_ref=self._output_contract_ref,
            computation_cursor=self._resolve_cursor(cursor),
        )
        self._lineage[key] = _WindowLineage(
            head_fact=feature_fact, invalidated=False, last_evidence_ref=fact.ref, last_evidence_fact=fact
        )
        return [feature_fact]

    def _emit_invalidation(
        self,
        key: tuple[datetime, datetime],
        invalidation: RegimeFactInvalidatedFact,
        cursor: EvaluationFrontier,
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
            event_contract_ref=self._invalidation_contract_ref,
            computation_cursor=self._resolve_cursor(cursor),
        )
        state.invalidated = True
        state.pending_invalidation_ref = ref
        state.pending_invalidation_recorded_time = recorded_time
        return [inv]

    def _emit_replacement(
        self,
        key: tuple[datetime, datetime],
        fact: RegimeClassifiedFact,
        existing: _WindowLineage,
        cursor: EvaluationFrontier,
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
            event_contract_ref=self._output_contract_ref,
            computation_cursor=self._resolve_cursor(cursor),
        )
        self._lineage[key] = _WindowLineage(
            head_fact=replacement, invalidated=False, last_evidence_ref=fact.ref, last_evidence_fact=fact
        )
        return [replacement]
