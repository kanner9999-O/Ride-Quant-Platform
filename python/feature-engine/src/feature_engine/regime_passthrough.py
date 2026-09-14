"""`volatility_metric`/`directional_persistence_metric` — `upstream_source:
regime` (feature.md §7.1/§7.2).

Exposes a Raw Regime `RegimeClassified.computed_metric` verbatim (after
Feature's own `decimal_precision_policy` normalization only) — never
reclassifies it, never enriches `directional_persistence_metric` into a
Bullish/Bearish/price-action interpretation.

Input Contract authority (P3-FEATURE-A-MAJ-06, Review-A round-4): this engine
does NOT accept an already-resolved authority VALUE at all — a caller could
otherwise "promote" arbitrary, unresolved data into trusted authority merely
by matching field shape. Instead, `input_contract_authority_provider:
InputContractAuthorityProvider` is a REQUIRED constructor argument; at
construction this engine itself calls `input_contract_authority_provider.
resolve(profile)` and trusts whatever `VerifiedInputContractAuthority` comes
back. This engine performs no filesystem/GitHub I/O itself and keeps no
duplicate copy of Input Contract/Stream Registry semantics — see
`authority_resolver.py`'s `FilesystemInputContractAuthorityResolver` for the
default, filesystem-backed implementation this repository's own tests use.

Computation cursor (P3-FEATURE-A-MAJ-06, ADR-035 Approved): `on_regime_
classified`/`on_regime_invalidated` both take an explicit, required
`cursor: EvaluationFrontier` keyword argument — the caller-certified,
proof-carrying computation frontier captured, together with this engine's
own bound Input Contract authority, into every emitted fact's
`computation_cursor`, after every Chapter 8 §8.5.2 relational invariant has
been verified (`resolve_computation_cursor`). This engine never substitutes
a process-local datetime, an invented registry value, or an incomplete
Feature-local surrogate. Every emitted fact's own `recorded_time` floor
additionally includes `cursor.recorded_time`, structurally guaranteeing
Chapter 8 §8.5.2's Cursor -> Fact invariant.

State atomicity (Review-A round-2 residual 2): `cursor` is fully certified
against this engine's own bound authority at the top of `on_regime_
classified`/`on_regime_invalidated`, BEFORE any lineage/dedup state is
mutated — a rejected frontier leaves the engine exactly as it was, so a
valid retry of the exact same authoritative event is processed normally.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .contracts import (
    ComputationCursor,
    ComputationDependencyContentEvidence,
    EvaluationFrontier,
    FeatureComputationProfile,
    FeatureComputed,
    FeatureDefinition,
    FeatureEvent,
    FeatureFactInvalidated,
    FeatureScope,
    InputContractAuthorityProvider,
    OutputEventContractAuthorityProvider,
    PreparedFeatureComputed,
    PreparedFeatureFactInvalidated,
    PreparedTransition,
    RecordedTimeSource,
    VerifiedInputContractAuthority,
    VerifiedOutputEventContractAuthority,
    normalize_input_facts,
    resolve_computation_cursor,
    resolve_computation_dependency_content_evidence,
)
from .envelope import EventContractRef, EventRecordRef
from .errors import (
    DefinitionVersionMismatchError,
    EvidenceReferenceConflictError,
    FeatureLineageError,
    ForeignScopeError,
    InputContractIdentityMismatchError,
    NonMonotonicRecordedTimeError,
    RegimeDimensionMismatchError,
    UnauthorizedUpstreamContractError,
    UnresolvedComputationCursorAuthorityError,
    UnresolvedOutputContractAuthorityError,
)
from .ownership import UpstreamEnvelope
from .publish import SequenceAllocator
from .regime_input import RegimeClassifiedFact, RegimeFactInvalidatedFact

_DIMENSION_BY_FEATURE_TYPE = {
    "volatility_metric": "volatility",
    "directional_persistence_metric": "directional_persistence",
}
_REQUIRED_INPUT_CONTRACT_PROFILE: FeatureComputationProfile = "regime"


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
        output_event_contract_authority_provider: OutputEventContractAuthorityProvider,
        input_contract_authority_provider: InputContractAuthorityProvider,
    ) -> None:
        if definition.feature_type not in _DIMENSION_BY_FEATURE_TYPE:
            raise ValueError(f"unsupported feature_type for regime pass-through: {definition.feature_type!r}")
        if definition.upstream_source != "regime":
            raise ValueError("RegimePassthroughFeatureEngine requires upstream_source='regime'")
        if scope.feature_type != definition.feature_type or scope.feature_definition_version != (
            definition.feature_definition_version
        ):
            raise ValueError("scope does not match definition")
        output_authority = output_event_contract_authority_provider.resolve()
        if not isinstance(output_authority, VerifiedOutputEventContractAuthority):
            raise UnresolvedOutputContractAuthorityError(
                "output_event_contract_authority_provider.resolve() returned "
                f"{type(output_authority).__name__!r}, not a genuine VerifiedOutputEventContractAuthority — a "
                "provider is never trusted merely because it returned an object with plausible-looking fields"
            )
        self._output_authority = output_authority
        self._output_contract_ref = output_authority.computed_contract_ref
        self._invalidation_contract_ref = output_authority.invalidated_contract_ref
        self._resolved_input_contract = input_contract_authority_provider.resolve(_REQUIRED_INPUT_CONTRACT_PROFILE)
        if not isinstance(self._resolved_input_contract, VerifiedInputContractAuthority):
            raise UnresolvedComputationCursorAuthorityError(
                f"input_contract_authority_provider.resolve({_REQUIRED_INPUT_CONTRACT_PROFILE!r}) returned "
                f"{type(self._resolved_input_contract).__name__!r}, not a genuine VerifiedInputContractAuthority "
                "— a provider is never trusted merely because it returned an object with plausible-looking "
                "fields (Review-A round-4); unresolved/plain data is never accepted as if it were verified"
            )
        if self._resolved_input_contract.feature_computation_profile != _REQUIRED_INPUT_CONTRACT_PROFILE:
            raise InputContractIdentityMismatchError(
                f"input_contract_authority_provider.resolve({_REQUIRED_INPUT_CONTRACT_PROFILE!r}) returned "
                f"authority for feature_computation_profile="
                f"{self._resolved_input_contract.feature_computation_profile!r} instead — a misbehaving "
                "provider is never trusted merely because it otherwise returned a well-formed object"
            )
        self.scope = scope
        self.definition = definition
        self._expected_dimension = _DIMENSION_BY_FEATURE_TYPE[definition.feature_type]
        self._allocator = allocator
        self._time_source = time_source
        self._stream_id = output_authority.authoritative_stream_id
        self._last_input_recorded_time: datetime | None = None
        self._lineage: dict[tuple[datetime, datetime], _WindowLineage] = {}

    @property
    def resolved_input_contract_authority(self) -> VerifiedInputContractAuthority:
        """ADR043-IMPL-A-MAJ-01: the exact, cached `VerifiedInputContractAuthority`
        this engine itself resolved and trusts — the ONLY Input Contract
        authority any external coordinator (`ownership.py`) may consume for
        this engine; never independently re-resolved.
        """
        return self._resolved_input_contract

    @property
    def resolved_output_event_contract_authority(self) -> VerifiedOutputEventContractAuthority:
        """ADR043-IMPL-A-MAJ-03: the exact, cached `VerifiedOutputEventContractAuthority`
        this engine itself resolved and trusts — carries the resolver-proven
        `authoritative_stream_id` an external coordinator must use as its
        commit stream, never a caller-chosen/hard-coded value.
        """
        return self._output_authority

    def is_pristine_for_authoritative_catchup(self) -> bool:
        """ADR043-IMPL-A-MAJ-05: True only when this engine instance has
        never processed ANY input (direct or authoritative) — the only
        state a freshly acquired `AuthoritativeSubjectOwner` may perform
        catch-up reconstruction into. An engine that has already mutated
        `_lineage`/`_last_input_recorded_time` (even from a single direct
        call, or from an abandoned prior authoritative attempt) is never
        reused for catch-up.
        """
        return not self._lineage and self._last_input_recorded_time is None

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

    def _resolve_cursor(self, frontier: EvaluationFrontier) -> ComputationCursor:
        """P3-FEATURE-A-MAJ-06: the single place this engine assembles its own
        outbound `computation_cursor` from a caller-supplied `EvaluationFrontier`
        — fails closed if any Chapter 8 §8.5.2 relational invariant does not
        hold against this engine's own bound Input Contract authority.
        """
        return resolve_computation_cursor(frontier, resolved_input_contract=self._resolved_input_contract)

    def _resolve_evidence(self) -> ComputationDependencyContentEvidence:
        """ADR-037: the single place this engine assembles its own outbound
        `computation_dependency_content_evidence` — always from this
        engine's own bound `VerifiedInputContractAuthority`, the SAME
        cached instance `_resolve_cursor` draws `input_contract_ref`/
        `stream_registry_version` from for this exact fact.
        """
        return resolve_computation_dependency_content_evidence(self._resolved_input_contract)

    def on_regime_classified(self, fact: RegimeClassifiedFact, *, cursor: EvaluationFrontier) -> list[FeatureEvent]:
        """`cursor` is the explicit, caller-certified `EvaluationFrontier`
        (P3-FEATURE-A-MAJ-06) captured verbatim into this fact's own
        `computation_cursor` — never implicitly derived from
        `fact.recorded_time`.

        Direct, non-authoritative call: prepares AND immediately live-
        commits with a self-allocated ref (ADR-043 §G) — the same
        behavior/output this method has always had. The authoritative
        (owned) path instead calls `prepare_regime_classified` directly and
        drives commit/reconcile through `ownership.py`'s
        `AuthoritativeSubjectOwner`/`FencedFeatureCommitter`.

        Review-A round-2 residual 2: certified against this engine's own
        bound authority BEFORE any lineage/dedup mutation below.
        """
        prepared = self.prepare_regime_classified(fact, cursor=cursor)
        if prepared is None:
            return []
        return self._commit_live(prepared)

    def on_regime_invalidated(
        self, invalidation: RegimeFactInvalidatedFact, *, cursor: EvaluationFrontier
    ) -> list[FeatureEvent]:
        """`cursor` is the explicit, caller-certified `EvaluationFrontier`
        (P3-FEATURE-A-MAJ-06) captured verbatim into this invalidation's own
        `computation_cursor` — never implicitly derived from
        `invalidation.recorded_time`.

        Direct, non-authoritative call: prepares AND immediately live-
        commits with a self-allocated ref (ADR-043 §G) — see
        `on_regime_classified`'s own docstring.

        Review-A round-2 residual 2: certified against this engine's own
        bound authority BEFORE any lineage mutation below.
        """
        prepared = self.prepare_regime_invalidated(invalidation, cursor=cursor)
        return self._commit_live(prepared)

    def _commit_live(self, prepared: PreparedTransition) -> list[FeatureEvent]:
        """The direct, non-authoritative `on_*` path's own commit: allocate
        real refs immediately (self._allocator, unchanged from before this
        seam existed) and apply the resulting lineage mutation right away —
        never used by the authoritative owner path, which drives
        `FencedFeatureCommitter` instead (ADR-043 §B/"Atomicity and
        emission").
        """
        refs = tuple(self._allocator.next_ref(self._stream_id) for _ in prepared.prepared_events)
        finalized = prepared.finalize_live(refs, time_source=self._time_source)
        prepared.apply_to_lineage(finalized)
        return list(finalized)

    def prepare_regime_classified(
        self, fact: RegimeClassifiedFact, *, cursor: EvaluationFrontier
    ) -> PreparedTransition | None:
        """ADR-043 prepare seam: identical validation/candidate-computation
        logic as `on_regime_classified` used to perform inline, but stops
        BEFORE allocating a Feature `ref` or mutating `_lineage` — returns
        `None` for the idempotent-duplicate-delivery no-op case.
        """
        self._resolve_cursor(cursor)
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
            return self._prepare_original(key, fact, cursor)
        if not existing.invalidated:
            if fact.ref == existing.last_evidence_ref:
                if fact != existing.last_evidence_fact:
                    raise EvidenceReferenceConflictError(
                        f"ref {fact.ref!r} resolves to conflicting RegimeClassified content "
                        f"({existing.last_evidence_fact!r} vs {fact!r})"
                    )
                return None  # duplicate delivery of the identical authoritative event
            raise FeatureLineageError(
                f"received a new RegimeClassified for window {key!r} whose current lineage head is not "
                "pending correction — a replacement must be preceded by RegimeFactInvalidated"
            )
        return self._prepare_replacement(key, fact, existing, cursor)

    def prepare_regime_invalidated(
        self, invalidation: RegimeFactInvalidatedFact, *, cursor: EvaluationFrontier
    ) -> PreparedTransition:
        """ADR-043 prepare seam — see `prepare_regime_classified`'s own
        docstring.
        """
        self._resolve_cursor(cursor)
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
        return self._prepare_invalidation(match_key, invalidation, cursor)

    def prepare_upstream_event(
        self, envelope: UpstreamEnvelope, *, cursor: EvaluationFrontier
    ) -> list[PreparedTransition]:
        """ADR-043 §D/§9: the one dispatch seam `ownership.py`'s
        `AuthoritativeSubjectOwner` uses to prepare a certified upstream
        event through this engine, keyed by `envelope.kind` — never
        allocating a Feature ref or mutating `_lineage` itself.
        """
        if envelope.kind == "regime_classified":
            if not isinstance(envelope.fact, RegimeClassifiedFact):
                raise TypeError(f"envelope.kind='regime_classified' but fact is {type(envelope.fact).__name__!r}")
            prepared = self.prepare_regime_classified(envelope.fact, cursor=cursor)
            return [prepared] if prepared is not None else []
        if envelope.kind == "regime_invalidated":
            if not isinstance(envelope.fact, RegimeFactInvalidatedFact):
                raise TypeError(f"envelope.kind='regime_invalidated' but fact is {type(envelope.fact).__name__!r}")
            return [self.prepare_regime_invalidated(envelope.fact, cursor=cursor)]
        raise ValueError(
            f"RegimePassthroughFeatureEngine.prepare_upstream_event: unsupported envelope.kind {envelope.kind!r}"
        )

    def _prepare_original(
        self, key: tuple[datetime, datetime], fact: RegimeClassifiedFact, cursor: EvaluationFrontier
    ) -> PreparedTransition:
        normalized_refs = normalize_input_facts(
            [fact], effective_time=lambda f: (f.window_start, f.window_end), ref_of=lambda f: f.ref, expected_count=1
        )
        # Chapter 8 §8.5.2 Cursor -> Fact (Review-A residual 4): the floor includes
        # cursor.recorded_time, structurally guaranteeing computation_cursor.recorded_time
        # <= FeatureComputed.recorded_time. ADR043-IMPL-A-MAJ-06: this is only the STRICT
        # FLOOR, never a materialized timestamp -- RecordedTimeSource is never called here.
        floor = max(fact.recorded_time, cursor.recorded_time)
        value = self.definition.decimal_precision_policy.apply(fact.computed_metric)
        prepared_computed = PreparedFeatureComputed(
            scope=self.scope,
            value=value,
            unit=self.definition.unit,
            window_start=key[0],
            window_end=key[1],
            input_fact_refs=normalized_refs,
            supersedes_fact_ref=None,
            causation_refs=normalized_refs,
            preceding_batch_invalidation_causation=False,
            recorded_time_floor=floor,
            depends_on_preceding_invalidation_timing=False,
            event_contract_ref=self._output_contract_ref,
            computation_cursor=self._resolve_cursor(cursor),
            computation_dependency_content_evidence=self._resolve_evidence(),
        )

        def _apply(events: tuple[FeatureEvent, ...]) -> None:
            (feature_fact,) = events
            assert isinstance(feature_fact, FeatureComputed)
            self._lineage[key] = _WindowLineage(
                head_fact=feature_fact, invalidated=False, last_evidence_ref=fact.ref, last_evidence_fact=fact
            )

        return PreparedTransition(prepared_events=(prepared_computed,), apply_lineage=_apply)

    def _prepare_invalidation(
        self,
        key: tuple[datetime, datetime],
        invalidation: RegimeFactInvalidatedFact,
        cursor: EvaluationFrontier,
    ) -> PreparedTransition:
        state = self._lineage[key]
        floor = max(state.head_fact.recorded_time, invalidation.recorded_time, cursor.recorded_time)
        prepared_invalidation = PreparedFeatureFactInvalidated(
            scope=state.head_fact.scope,
            invalidated_fact_ref=state.head_fact.ref,
            invalidation_cause="regime_fact_invalidated",
            window_start=state.head_fact.window_start,
            window_end=state.head_fact.window_end,
            causation_refs=(state.head_fact.ref, invalidation.ref),
            recorded_time_floor=floor,
            event_contract_ref=self._invalidation_contract_ref,
            computation_cursor=self._resolve_cursor(cursor),
            computation_dependency_content_evidence=self._resolve_evidence(),
        )

        def _apply(events: tuple[FeatureEvent, ...]) -> None:
            (inv,) = events
            assert isinstance(inv, FeatureFactInvalidated)
            state.invalidated = True
            state.pending_invalidation_ref = inv.ref
            state.pending_invalidation_recorded_time = inv.recorded_time

        return PreparedTransition(prepared_events=(prepared_invalidation,), apply_lineage=_apply)

    def _prepare_replacement(
        self,
        key: tuple[datetime, datetime],
        fact: RegimeClassifiedFact,
        existing: _WindowLineage,
        cursor: EvaluationFrontier,
    ) -> PreparedTransition:
        normalized_refs = normalize_input_facts(
            [fact], effective_time=lambda f: (f.window_start, f.window_end), ref_of=lambda f: f.ref, expected_count=1
        )
        assert existing.pending_invalidation_recorded_time is not None
        assert existing.pending_invalidation_ref is not None
        floor = max(existing.pending_invalidation_recorded_time, cursor.recorded_time)
        value = self.definition.decimal_precision_policy.apply(fact.computed_metric)
        prepared_replacement = PreparedFeatureComputed(
            scope=self.scope,
            value=value,
            unit=self.definition.unit,
            window_start=key[0],
            window_end=key[1],
            input_fact_refs=normalized_refs,
            supersedes_fact_ref=existing.head_fact.ref,
            causation_refs=(*normalized_refs, existing.pending_invalidation_ref),
            preceding_batch_invalidation_causation=False,
            recorded_time_floor=floor,
            depends_on_preceding_invalidation_timing=False,
            event_contract_ref=self._output_contract_ref,
            computation_cursor=self._resolve_cursor(cursor),
            computation_dependency_content_evidence=self._resolve_evidence(),
        )

        def _apply(events: tuple[FeatureEvent, ...]) -> None:
            (replacement,) = events
            assert isinstance(replacement, FeatureComputed)
            self._lineage[key] = _WindowLineage(
                head_fact=replacement, invalidated=False, last_evidence_ref=fact.ref, last_evidence_fact=fact
            )

        return PreparedTransition(prepared_events=(prepared_replacement,), apply_lineage=_apply)
