"""ADR-043 implementation candidate tests (`ownership.py`) — deterministic,
ordinary implementation tests using in-memory test doubles for
`SubjectOwnershipAuthority`/`FencedFeatureCommitter`/
`AuthoritativeLineageHistoryProvider`. These are NOT the formal EVID-07
property-based/Hypothesis evidence transaction (still OPEN/FAIL), and no
fake here is claimed production-authoritative — every one is explicitly
labeled TEST-ONLY, single-process, non-durable.
"""

from __future__ import annotations

import dataclasses
import inspect
from dataclasses import dataclass, field
from datetime import datetime, timedelta

import pytest
from conftest import (
    BASE,
    OUTPUT_EVENT_CONTRACT_AUTHORITY,
    REGIME_INPUT_CONTRACT,
    SWING_DISTANCE_INPUT_CONTRACT,
    FixedDeltaTimeSource,
    authorized_candle_contract_refs,
    authorized_swing_contract_refs,
    candle_at,
    feature_scope,
    frontier_at,
    make_distance_definition,
    make_regime_definition,
    only_computed,
    only_invalidated,
    regime_classified_at,
    regime_invalidated_at,
    swing_confirmed_at,
    swing_invalidated_at,
)

from feature_engine import (
    EvaluationFrontier,
    EventRecordRef,
    FeatureEvent,
    InputContractAuthorityProvider,
    RecordedTimeSource,
    RegimePassthroughFeatureEngine,
    SequenceAllocator,
    StaticInputContractAuthorityProvider,
    StaticOutputEventContractAuthorityProvider,
    SwingDistanceFeatureEngine,
)
from feature_engine.contracts import InputMergePolicy, PreparedTransition
from feature_engine.errors import (
    CanonicalHistoryMismatchError,
    ConflictingUpstreamEnvelopeError,
    DualOwnershipError,
    EngineNotPristineForCatchUpError,
    FeatureLineageError,
    NonMonotonicApplicationOrderError,
    OwnershipAuthorityUnavailableError,
    ProviderFrontierMismatchError,
    RegistryContractMismatchError,
    StaleOwnershipGenerationError,
    StreamPositionsUniverseMismatchError,
    UnprovenCatchUpError,
    UnsupportedMergePolicyError,
)
from feature_engine.ownership import (
    AuthoritativeSubjectOwner,
    CanonicalOutputHistoryResult,
    SubjectOwnershipState,
    UpstreamEnvelope,
    UpstreamHistoryResult,
    p_run_sort,
)

# --- TEST-ONLY in-memory fakes ----------------------------------------------
#
# None of these is a production-authoritative implementation of the
# corresponding ADR-043 Protocol (`SubjectOwnershipAuthority`/
# `FencedFeatureCommitter`/`AuthoritativeLineageHistoryProvider`) — every one
# is single-process, non-durable, and exists only to exercise
# `AuthoritativeSubjectOwner`'s own coordination logic deterministically.


@dataclass
class InMemorySubjectOwnershipAuthority:
    """TEST-ONLY `SubjectOwnershipAuthority` fake — NOT sufficient for
    production-authoritative cross-process ownership (single-process,
    non-durable, no crash/restart survival). Tracks the current generation
    per subject; `acquire` fences (overwrites) any prior generation before
    returning the new one, matching the real Protocol's revoke-before-
    successor contract.
    """

    _current_generation: dict[str, int] = field(default_factory=dict)
    _last_minted: dict[str, int] = field(default_factory=dict)

    def acquire(self, feature_subject_id: str) -> int:
        generation = self._last_minted.get(feature_subject_id, 0) + 1
        self._last_minted[feature_subject_id] = generation
        self._current_generation[feature_subject_id] = generation
        return generation

    def is_current(self, feature_subject_id: str, ownership_generation: int) -> bool:
        return self._current_generation.get(feature_subject_id) == ownership_generation

    def revoke(self, feature_subject_id: str, ownership_generation: int) -> None:
        if self._current_generation.get(feature_subject_id) == ownership_generation:
            del self._current_generation[feature_subject_id]


@dataclass
class InMemoryFencedFeatureCommitter:
    """TEST-ONLY `FencedFeatureCommitter` fake — NOT a durable/production
    commit boundary. Verifies the generation against the SAME
    `InMemorySubjectOwnershipAuthority` fake, allocates refs via the SAME
    `SequenceAllocator` the wrapped engine holds, and appends to a shared
    in-memory log, all within one synchronous Python call. `fail_next`, when
    set, makes the NEXT `commit()` call raise BEFORE any ref is allocated or
    anything is appended — used to prove a failed commit has zero effect.
    """

    authority: InMemorySubjectOwnershipAuthority
    allocator: SequenceAllocator
    time_source: RecordedTimeSource
    log: dict[str, list[FeatureEvent]] = field(default_factory=dict)
    fail_next: bool = False

    def commit(
        self,
        *,
        feature_subject_id: str,
        ownership_generation: int,
        stream_id: str,
        prepared: PreparedTransition,
    ) -> tuple[FeatureEvent, ...]:
        if not self.authority.is_current(feature_subject_id, ownership_generation):
            raise StaleOwnershipGenerationError(
                f"generation {ownership_generation!r} for {feature_subject_id!r} is no longer current"
            )
        if self.fail_next:
            self.fail_next = False
            raise RuntimeError("TEST-ONLY forced commit failure — simulates an uncertain/aborted authoritative append")
        refs = tuple(self.allocator.next_ref(stream_id) for _ in prepared.prepared_events)
        finalized = prepared.finalize_live(refs, time_source=self.time_source)
        self.log.setdefault(feature_subject_id, []).extend(finalized)
        return finalized


@dataclass(frozen=True)
class RaisingRecordedTimeSource:
    """TEST-ONLY `RecordedTimeSource` that always raises — used to prove
    historical catch-up/reconcile (ADR043-IMPL-A-MAJ-06) never calls
    `RecordedTimeSource.next_after` at all.
    """

    def next_after(self, strict_floor: datetime) -> datetime:
        raise AssertionError(
            "RecordedTimeSource.next_after must never be called during historical catch-up/reconcile "
            "(ADR043-IMPL-A-MAJ-06)"
        )


@dataclass
class InMemoryLineageHistoryProvider:
    """TEST-ONLY `AuthoritativeLineageHistoryProvider` fake — NOT a
    persistent production adapter. Tests explicitly `register_*` a subject's
    complete certified upstream/canonical history ahead of a catch-up call,
    and `enqueue_pending` upstream events ahead of an ongoing
    `process_certified_frontier` call. A subject that was never registered
    at all cannot prove emptiness (`proven_empty=False`) — this is what
    "absent provider" fails closed against.
    """

    _known_subjects: set[str] = field(default_factory=set)
    _upstream: dict[str, list[UpstreamEnvelope]] = field(default_factory=dict)
    _canonical: dict[str, list[FeatureEvent]] = field(default_factory=dict)
    _pending: dict[str, list[UpstreamEnvelope]] = field(default_factory=dict)

    def register_upstream(self, feature_subject_id: str, envelopes: list[UpstreamEnvelope]) -> None:
        self._known_subjects.add(feature_subject_id)
        self._upstream.setdefault(feature_subject_id, []).extend(envelopes)

    def register_canonical(self, feature_subject_id: str, events: list[FeatureEvent]) -> None:
        self._known_subjects.add(feature_subject_id)
        self._canonical.setdefault(feature_subject_id, []).extend(events)

    def register_known_empty(self, feature_subject_id: str) -> None:
        self._known_subjects.add(feature_subject_id)

    def enqueue_pending(self, feature_subject_id: str, envelopes: list[UpstreamEnvelope]) -> None:
        self._known_subjects.add(feature_subject_id)
        self._pending.setdefault(feature_subject_id, []).extend(envelopes)

    def upstream_history(self, feature_subject_id: str, *, up_to: EvaluationFrontier) -> UpstreamHistoryResult:
        events = tuple(self._upstream.get(feature_subject_id, ()))
        return UpstreamHistoryResult(events=events, proven_empty=feature_subject_id in self._known_subjects)

    def canonical_output_history(
        self, feature_subject_id: str, *, up_to: EvaluationFrontier
    ) -> CanonicalOutputHistoryResult:
        events = tuple(self._canonical.get(feature_subject_id, ()))
        return CanonicalOutputHistoryResult(events=events, proven_empty=feature_subject_id in self._known_subjects)

    def not_yet_applied_apply_set(
        self,
        feature_subject_id: str,
        *,
        frontier: EvaluationFrontier,
        applied_frontier: EvaluationFrontier | None,
    ) -> UpstreamHistoryResult:
        events = tuple(self._pending.pop(feature_subject_id, []))
        return UpstreamHistoryResult(events=events, proven_empty=feature_subject_id in self._known_subjects)


# --- Local engine/envelope construction helpers -----------------------------


def _regime_engine(allocator: SequenceAllocator, time_source: RecordedTimeSource) -> RegimePassthroughFeatureEngine:
    definition = make_regime_definition(regime_dimension_version="rgd-1")
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    return RegimePassthroughFeatureEngine(
        scope,
        definition,
        allocator,
        time_source,
        output_event_contract_authority_provider=StaticOutputEventContractAuthorityProvider(
            OUTPUT_EVENT_CONTRACT_AUTHORITY
        ),
        input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
    )


def _swing_engine(
    allocator: SequenceAllocator,
    time_source: RecordedTimeSource,
    *,
    input_contract_authority_provider: InputContractAuthorityProvider | None = None,
) -> SwingDistanceFeatureEngine:
    definition = make_distance_definition()
    scope = feature_scope("distance_to_last_confirmed_swing", version=definition.feature_definition_version)
    provider = (
        input_contract_authority_provider
        if input_contract_authority_provider is not None
        else StaticInputContractAuthorityProvider(SWING_DISTANCE_INPUT_CONTRACT)
    )
    return SwingDistanceFeatureEngine(
        scope,
        definition,
        allocator,
        time_source,
        output_event_contract_authority_provider=StaticOutputEventContractAuthorityProvider(
            OUTPUT_EVENT_CONTRACT_AUTHORITY
        ),
        authorized_candle_contract_refs=authorized_candle_contract_refs(),
        authorized_swing_contract_refs=authorized_swing_contract_refs(),
        input_contract_authority_provider=provider,
    )


def _regime_envelope(fact: object, *, kind: str, frontier: EvaluationFrontier) -> UpstreamEnvelope:
    causation_refs: tuple[EventRecordRef, ...] = ()
    if kind == "regime_invalidated":
        causation_refs = (fact.invalidated_fact_ref,)  # type: ignore[attr-defined]
    return UpstreamEnvelope(
        ref=fact.ref,  # type: ignore[attr-defined]
        recorded_time=fact.recorded_time,  # type: ignore[attr-defined]
        causation_refs=causation_refs,
        kind=kind,
        fact=fact,
        frontier=frontier,
    )


def _swing_envelope(
    fact: object, *, kind: str, frontier: EvaluationFrontier, causation_refs: tuple[EventRecordRef, ...] = ()
) -> UpstreamEnvelope:
    return UpstreamEnvelope(
        ref=fact.ref,  # type: ignore[attr-defined]
        recorded_time=fact.recorded_time,  # type: ignore[attr-defined]
        causation_refs=causation_refs,
        kind=kind,
        fact=fact,
        frontier=frontier,
    )


def _mk_ref(stream_id: str, sequence: int) -> EventRecordRef:
    return EventRecordRef(stream_id=stream_id, sequence=sequence, event_id=f"{stream_id}-{sequence}")


_DUMMY_FRONTIER = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
_SUPPORTED_MERGE_POLICY = InputMergePolicy(
    algorithm="deterministic-causal-topological-order", concurrent_tie_break=("stream_id", "sequence")
)


def _mk_envelope(
    ref: EventRecordRef, *, causation_refs: tuple[EventRecordRef, ...] = (), recorded_time: object = BASE
) -> UpstreamEnvelope:
    return UpstreamEnvelope(
        ref=ref,
        recorded_time=recorded_time,  # type: ignore[arg-type]
        causation_refs=causation_refs,
        kind="test",
        fact=None,
        frontier=_DUMMY_FRONTIER,
    )


# --- Deterministic P_run construction (§D/§D2) ------------------------------


def test_p_run_sort_orders_by_causation_regardless_of_arrival_order() -> None:
    ref_a = _mk_ref("stream-a", 1)
    ref_b = _mk_ref("stream-b", 1)
    envelope_a = _mk_envelope(ref_a)
    envelope_b = _mk_envelope(ref_b, causation_refs=(ref_a,))
    ordered = p_run_sort([envelope_b, envelope_a], merge_policy=_SUPPORTED_MERGE_POLICY)
    assert [e.ref for e in ordered] == [ref_a, ref_b]


def test_p_run_sort_orders_same_stream_by_ascending_sequence_regardless_of_arrival_order() -> None:
    ref_1 = _mk_ref("stream-a", 1)
    ref_2 = _mk_ref("stream-a", 2)
    ordered = p_run_sort([_mk_envelope(ref_2), _mk_envelope(ref_1)], merge_policy=_SUPPORTED_MERGE_POLICY)
    assert [e.ref for e in ordered] == [ref_1, ref_2]


def test_p_run_sort_tie_breaks_incomparable_events_by_stream_id_then_sequence() -> None:
    ref_a = _mk_ref("stream-a", 5)
    ref_b = _mk_ref("stream-b", 1)
    ordered = p_run_sort([_mk_envelope(ref_b), _mk_envelope(ref_a)], merge_policy=_SUPPORTED_MERGE_POLICY)
    assert [e.ref for e in ordered] == [ref_a, ref_b]


def test_p_run_sort_case_2_processes_event_whose_out_of_set_cause_is_already_resolved() -> None:
    """ADR043-IMPLDESIGN-A-MAJ-02 Case 2, corrected framing
    (ADR043-IMPL-A-MAJ-07): B is in the current certified apply set; some
    OTHER event A is NOT a member of this apply set and has no `P_stream`/
    `P_causation` relationship to B within it. B's own `causation_refs` may
    legitimately cite a ref outside this bounded set — but ONLY as an
    already-resolved/already-applied cause supplied by the certified
    history boundary (i.e. some upstream/prior event that is already
    authoritative and visible), NEVER as a claim about a hypothetical
    FUTURE independent event. `p_run_sort` treats any such out-of-set
    `causation_ref` as trivially already-satisfied and processes B now —
    it never waits for anything outside its own bounded apply set.
    """
    ref_b = _mk_ref("stream-b", 1)
    already_resolved_cause_ref = _mk_ref("stream-a", 1)
    envelope_b = _mk_envelope(ref_b, causation_refs=(already_resolved_cause_ref,))
    ordered = p_run_sort([envelope_b], merge_policy=_SUPPORTED_MERGE_POLICY)
    assert [e.ref for e in ordered] == [ref_b]


def test_p_run_sort_rejects_cycle() -> None:
    ref_a = _mk_ref("stream-a", 1)
    ref_b = _mk_ref("stream-b", 1)
    envelope_a = _mk_envelope(ref_a, causation_refs=(ref_b,))
    envelope_b = _mk_envelope(ref_b, causation_refs=(ref_a,))
    with pytest.raises(NonMonotonicApplicationOrderError):
        p_run_sort([envelope_a, envelope_b], merge_policy=_SUPPORTED_MERGE_POLICY)


def test_p_run_sort_rejects_unsupported_algorithm() -> None:
    bad_policy = InputMergePolicy(algorithm="some-other-algorithm", concurrent_tie_break=("stream_id", "sequence"))
    with pytest.raises(UnsupportedMergePolicyError):
        p_run_sort([_mk_envelope(_mk_ref("stream-a", 1))], merge_policy=bad_policy)


def test_p_run_sort_rejects_unsupported_tie_break() -> None:
    bad_policy = InputMergePolicy(
        algorithm="deterministic-causal-topological-order", concurrent_tie_break=("recorded_time", "event_id")
    )
    with pytest.raises(UnsupportedMergePolicyError):
        p_run_sort([_mk_envelope(_mk_ref("stream-a", 1))], merge_policy=bad_policy)


# --- ADR043-IMPL-A-MAJ-07: duplicate EventRecordRef must not be last-writer-wins ---


def test_p_run_sort_deduplicates_byte_for_byte_identical_redelivery() -> None:
    ref_a = _mk_ref("stream-a", 1)
    first = _mk_envelope(ref_a, recorded_time=BASE)
    identical_redelivery = _mk_envelope(ref_a, recorded_time=BASE)
    ordered = p_run_sort([first, identical_redelivery], merge_policy=_SUPPORTED_MERGE_POLICY)
    assert [e.ref for e in ordered] == [ref_a]


def test_p_run_sort_rejects_conflicting_duplicate_ref_arrival_order_one() -> None:
    ref_a = _mk_ref("stream-a", 1)
    original = _mk_envelope(ref_a, recorded_time=BASE)
    conflicting = _mk_envelope(ref_a, recorded_time=BASE + timedelta(minutes=1))
    with pytest.raises(ConflictingUpstreamEnvelopeError):
        p_run_sort([original, conflicting], merge_policy=_SUPPORTED_MERGE_POLICY)


def test_p_run_sort_rejects_conflicting_duplicate_ref_arrival_order_two() -> None:
    """Same conflicting pair as above, supplied in the OPPOSITE input order
    — input order must never decide which envelope survives.
    """
    ref_a = _mk_ref("stream-a", 1)
    original = _mk_envelope(ref_a, recorded_time=BASE)
    conflicting = _mk_envelope(ref_a, recorded_time=BASE + timedelta(minutes=1))
    with pytest.raises(ConflictingUpstreamEnvelopeError):
        p_run_sort([conflicting, original], merge_policy=_SUPPORTED_MERGE_POLICY)


# --- ADR043-IMPL-A-MAJ-01/-02/-03: authority/subject/stream derived from engine ---


def test_authoritative_subject_owner_constructor_accepts_no_merge_policy_override() -> None:
    """ADR043-IMPL-A-MAJ-01: an arbitrary caller-constructed `InputMergePolicy`
    can no longer be injected into an owner at all — the constructor
    signature itself carries no such parameter.
    """
    signature = inspect.signature(AuthoritativeSubjectOwner.__init__)
    assert "merge_policy" not in signature.parameters


def test_authoritative_subject_owner_constructor_accepts_no_subject_id_override() -> None:
    """ADR043-IMPL-A-MAJ-02: the constructor signature carries no
    `feature_subject_id` parameter either — subject identity is derived
    exclusively from `engine.scope.feature_subject_id`.
    """
    signature = inspect.signature(AuthoritativeSubjectOwner.__init__)
    assert "feature_subject_id" not in signature.parameters


def test_authoritative_subject_owner_constructor_accepts_no_stream_id_override() -> None:
    """ADR043-IMPL-A-MAJ-03: the constructor signature carries no
    `stream_id` parameter either — the commit stream is derived exclusively
    from `engine.resolved_output_event_contract_authority.
    authoritative_stream_id`.
    """
    signature = inspect.signature(AuthoritativeSubjectOwner.__init__)
    assert "stream_id" not in signature.parameters


def test_owner_derives_subject_id_merge_policy_and_stream_from_engine(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _regime_engine(allocator, time_source)
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    owner = AuthoritativeSubjectOwner(
        engine=engine, authority=authority, committer=committer, history_provider=provider
    )
    assert owner.feature_subject_id == engine.scope.feature_subject_id
    assert owner._merge_policy == engine.resolved_input_contract_authority.merge_policy  # noqa: SLF001
    assert owner._stream_id == engine.resolved_output_event_contract_authority.authoritative_stream_id  # noqa: SLF001
    assert owner._stream_id == "feature-engine-feature"  # noqa: SLF001


def test_regime_engine_exposes_resolved_authorities_and_pristine_check(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _regime_engine(allocator, time_source)
    assert engine.resolved_input_contract_authority is REGIME_INPUT_CONTRACT
    assert engine.resolved_output_event_contract_authority.authoritative_stream_id == "feature-engine-feature"
    assert engine.is_pristine_for_authoritative_catchup() is True
    fact = regime_classified_at(allocator, 0, computed_metric="1.5")
    engine.on_regime_classified(
        fact, cursor=frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    )
    assert engine.is_pristine_for_authoritative_catchup() is False


def test_swing_engine_exposes_resolved_authorities_and_pristine_check(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _swing_engine(allocator, time_source)
    assert engine.resolved_input_contract_authority is SWING_DISTANCE_INPUT_CONTRACT
    assert engine.resolved_output_event_contract_authority.authoritative_stream_id == "feature-engine-feature"
    assert engine.is_pristine_for_authoritative_catchup() is True
    swing = swing_confirmed_at(allocator, pivot_index=0, swing_id="swing-a")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    assert engine.is_pristine_for_authoritative_catchup() is False


# --- Fencing (§B) ------------------------------------------------------------


def test_authority_acquire_generation_is_strictly_increasing_and_fences_predecessor() -> None:
    authority = InMemorySubjectOwnershipAuthority()
    generation_1 = authority.acquire("subject-1")
    assert authority.is_current("subject-1", generation_1) is True
    generation_2 = authority.acquire("subject-1")
    assert generation_2 > generation_1
    assert authority.is_current("subject-1", generation_1) is False
    assert authority.is_current("subject-1", generation_2) is True


def test_authority_generations_are_independent_per_subject() -> None:
    authority = InMemorySubjectOwnershipAuthority()
    generation_x = authority.acquire("subject-x")
    generation_y = authority.acquire("subject-y")
    assert authority.is_current("subject-x", generation_x) is True
    assert authority.is_current("subject-y", generation_y) is True


def test_committer_rejects_stale_generation_with_zero_effect(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _regime_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    stale_generation = authority.acquire(subject_id)
    authority.acquire(subject_id)  # mints a successor, fencing stale_generation

    fact = regime_classified_at(allocator, 0, computed_metric="1.5")
    frontier = frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    prepared = engine.prepare_regime_classified(fact, cursor=frontier)
    assert prepared is not None

    with pytest.raises(StaleOwnershipGenerationError):
        committer.commit(
            feature_subject_id=subject_id, ownership_generation=stale_generation, stream_id="feature", prepared=prepared
        )
    assert committer.log.get(subject_id, []) == []
    assert allocator._sequences.get("feature") is None


def test_acquire_and_activate_rejects_dual_ownership_while_already_active(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _regime_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )
    empty_frontier = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
    owner.acquire_and_activate(catch_up_frontier=empty_frontier)
    with pytest.raises(DualOwnershipError):
        owner.acquire_and_activate(catch_up_frontier=empty_frontier)


def test_acquire_and_activate_rejects_a_non_pristine_engine(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """ADR043-IMPL-A-MAJ-05: an engine that already processed a direct call
    (even one producing no Feature output) may never be wrapped by a fresh
    owner and used for catch-up.
    """
    engine = _regime_engine(allocator, time_source)
    fact = regime_classified_at(allocator, 0, computed_metric="1.5")
    engine.on_regime_classified(
        fact, cursor=frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    )
    assert engine.is_pristine_for_authoritative_catchup() is False

    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        engine=engine, authority=authority, committer=committer, history_provider=provider
    )

    with pytest.raises(EngineNotPristineForCatchUpError):
        owner.acquire_and_activate(catch_up_frontier=frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT))
    assert owner.state is not SubjectOwnershipState.ACTIVE
    assert authority.is_current(subject_id, 1) is False  # no generation was ever minted


def test_process_certified_frontier_fails_closed_when_never_activated(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _regime_engine(allocator, time_source)
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    owner = AuthoritativeSubjectOwner(
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )
    frontier = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
    with pytest.raises(OwnershipAuthorityUnavailableError):
        owner.process_certified_frontier(frontier)


def test_owner_becomes_terminal_after_stale_generation_and_same_owner_cannot_reacquire(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """ADR043-IMPL-A-MAJ-05: a failed authoritative commit permanently
    retires this owner instance — `acquire_and_activate` must never be
    callable again on it, even against an otherwise-valid empty-history
    frontier. Recovery requires a fresh engine + fresh owner (see
    `test_fresh_owner_and_fresh_engine_recover_canonical_state_after_prior_
    owner_goes_terminal`, below).
    """
    engine = _regime_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )
    empty_frontier = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
    owner.acquire_and_activate(catch_up_frontier=empty_frontier)
    state_after_activate: SubjectOwnershipState = owner.state
    assert state_after_activate is SubjectOwnershipState.ACTIVE
    assert owner.is_terminal is False

    authority.acquire(subject_id)  # external successor acquisition fences this owner's generation

    fact = regime_classified_at(allocator, 0, computed_metric="1.5")
    frontier = frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    provider.enqueue_pending(subject_id, [_regime_envelope(fact, kind="regime_classified", frontier=frontier)])

    with pytest.raises(StaleOwnershipGenerationError):
        owner.process_certified_frontier(frontier)
    state_after_stale_commit: SubjectOwnershipState = owner.state
    assert state_after_stale_commit is SubjectOwnershipState.REVOKED
    assert owner.is_terminal is True

    with pytest.raises(OwnershipAuthorityUnavailableError):
        owner.process_certified_frontier(frontier)

    # The SAME owner instance may never reacquire again, even against a
    # trivially-empty, otherwise-valid frontier.
    with pytest.raises(OwnershipAuthorityUnavailableError):
        owner.acquire_and_activate(catch_up_frontier=empty_frontier)


def test_owner_fences_unusable_when_local_lineage_apply_fails_after_successful_commit(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """ADR-043 §9 crash/local-cache recovery model: authoritative commit
    succeeding but the local cache-update step failing must fence the owner
    unusable — never retry/append the same transition blindly.
    """
    engine = _regime_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )
    empty_frontier = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
    owner.acquire_and_activate(catch_up_frontier=empty_frontier)

    def _broken_apply(_events: tuple[FeatureEvent, ...]) -> None:
        raise RuntimeError("TEST-ONLY simulated local cache-update failure")

    fact = regime_classified_at(allocator, 0, computed_metric="1.5")
    frontier = frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    prepared = engine.prepare_regime_classified(fact, cursor=frontier)
    assert prepared is not None
    broken_prepared = dataclasses.replace(prepared, apply_lineage=_broken_apply)

    with pytest.raises(RuntimeError):
        owner._commit(broken_prepared)  # noqa: SLF001 -- exercising the private commit seam directly, by design

    assert owner.state is SubjectOwnershipState.REVOKED
    assert len(committer.log[subject_id]) == 1  # authoritative history already committed despite local failure

    with pytest.raises(OwnershipAuthorityUnavailableError):
        owner.process_certified_frontier(frontier)


# --- Frontier validation (§D2, ADR043-IMPL-A-MAJ-04) ------------------------


def test_acquire_and_activate_fails_closed_on_invalid_frontier_even_with_proven_empty_history(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _regime_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        engine=engine, authority=authority, committer=committer, history_provider=provider
    )
    valid_frontier = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
    invalid_frontier = dataclasses.replace(valid_frontier, stream_registry_version="not-the-real-version")

    with pytest.raises(RegistryContractMismatchError):
        owner.acquire_and_activate(catch_up_frontier=invalid_frontier)
    state_after_failure: SubjectOwnershipState = owner.state
    assert state_after_failure is not SubjectOwnershipState.ACTIVE
    assert owner._committed_frontier is None  # noqa: SLF001
    assert owner.is_terminal is False  # pure input validation, before any generation was ever acquired

    # A corrected, valid frontier still activates this same (never-acquired) owner.
    owner.acquire_and_activate(catch_up_frontier=valid_frontier)
    state_after_recovery: SubjectOwnershipState = owner.state
    assert state_after_recovery is SubjectOwnershipState.ACTIVE


def test_process_certified_frontier_fails_closed_on_invalid_registry_version_even_with_proven_empty_apply_set(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _regime_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        engine=engine, authority=authority, committer=committer, history_provider=provider
    )
    owner.acquire_and_activate(catch_up_frontier=frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT))
    original_committed = owner._committed_frontier  # noqa: SLF001

    valid_frontier = frontier_at(BASE + timedelta(minutes=1), resolved_input_contract=REGIME_INPUT_CONTRACT)
    invalid_frontier = dataclasses.replace(valid_frontier, stream_registry_version="not-the-real-version")
    # provider.register_known_empty already makes the apply-set query PROVEN EMPTY --
    # frontier validation must still fail closed regardless.
    with pytest.raises(RegistryContractMismatchError):
        owner.process_certified_frontier(invalid_frontier)
    assert owner._committed_frontier == original_committed  # noqa: SLF001 -- no checkpoint advance


def test_process_certified_frontier_fails_closed_on_wrong_stream_universe_even_with_proven_empty_apply_set(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _regime_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        engine=engine, authority=authority, committer=committer, history_provider=provider
    )
    owner.acquire_and_activate(catch_up_frontier=frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT))
    original_committed = owner._committed_frontier  # noqa: SLF001

    wrong_universe_frontier = frontier_at(
        BASE + timedelta(minutes=1), resolved_input_contract=REGIME_INPUT_CONTRACT, stream_positions={}
    )
    with pytest.raises(StreamPositionsUniverseMismatchError):
        owner.process_certified_frontier(wrong_universe_frontier)
    assert owner._committed_frontier == original_committed  # noqa: SLF001 -- no checkpoint advance


def test_process_certified_frontier_fails_closed_when_provider_envelope_frontier_mismatches_requested(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """A provider handing back an `UpstreamEnvelope` certified against a
    DIFFERENT cursor than the requested live frontier must never let the
    owner silently advance its checkpoint to the requested frontier anyway.
    """
    engine = _regime_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        engine=engine, authority=authority, committer=committer, history_provider=provider
    )
    owner.acquire_and_activate(catch_up_frontier=frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT))
    original_committed = owner._committed_frontier  # noqa: SLF001

    requested_frontier = frontier_at(BASE + timedelta(minutes=1), resolved_input_contract=REGIME_INPUT_CONTRACT)
    mismatched_frontier = frontier_at(BASE + timedelta(minutes=2), resolved_input_contract=REGIME_INPUT_CONTRACT)
    fact = regime_classified_at(allocator, 0, computed_metric="1.5")
    provider.enqueue_pending(
        subject_id, [_regime_envelope(fact, kind="regime_classified", frontier=mismatched_frontier)]
    )

    with pytest.raises(ProviderFrontierMismatchError):
        owner.process_certified_frontier(requested_frontier)
    assert owner._committed_frontier == original_committed  # noqa: SLF001 -- no checkpoint advance
    assert owner.is_terminal is True


# --- Atomic batch commit (§B "Atomicity and emission") ----------------------


def test_batch_commit_invalidate_and_replace_commits_atomically(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _swing_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )
    owner.acquire_and_activate(catch_up_frontier=frontier_at(BASE))

    swing = swing_confirmed_at(allocator, pivot_index=0, swing_id="swing-a")
    frontier_swing = frontier_at(swing.recorded_time)
    provider.enqueue_pending(subject_id, [_swing_envelope(swing, kind="swing_confirmed", frontier=frontier_swing)])
    owner.process_certified_frontier(frontier_swing)

    candle = candle_at(allocator, 10, high="110", low="90")
    frontier_candle = frontier_at(candle.recorded_time)
    provider.enqueue_pending(subject_id, [_swing_envelope(candle, kind="candle", frontier=frontier_candle)])
    original_events = owner.process_certified_frontier(frontier_candle)
    assert len(original_events) == 1

    correction = candle_at(allocator, 10, high="120", low="90", is_correction=True, recorded_offset_seconds=5)
    frontier_corr = frontier_at(correction.recorded_time)
    provider.enqueue_pending(subject_id, [_swing_envelope(correction, kind="candle", frontier=frontier_corr)])
    batch_events = owner.process_certified_frontier(frontier_corr)

    assert len(batch_events) == 2
    only_invalidated(batch_events[0])
    replacement = only_computed(batch_events[1])
    key = (candle.scope.window_start, candle.scope.window_end)
    assert engine._lineage[key].head_fact is replacement
    assert len(committer.log[subject_id]) == 3  # original + invalidation + replacement, all committed


def test_batch_commit_failure_has_zero_effect_and_fences_owner(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _swing_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )
    owner.acquire_and_activate(catch_up_frontier=frontier_at(BASE))

    swing = swing_confirmed_at(allocator, pivot_index=0, swing_id="swing-a")
    frontier_swing = frontier_at(swing.recorded_time)
    provider.enqueue_pending(subject_id, [_swing_envelope(swing, kind="swing_confirmed", frontier=frontier_swing)])
    owner.process_certified_frontier(frontier_swing)

    candle = candle_at(allocator, 10, high="110", low="90")
    frontier_candle = frontier_at(candle.recorded_time)
    provider.enqueue_pending(subject_id, [_swing_envelope(candle, kind="candle", frontier=frontier_candle)])
    original_events = owner.process_certified_frontier(frontier_candle)
    key = (candle.scope.window_start, candle.scope.window_end)
    original_head = engine._lineage[key].head_fact

    committer.fail_next = True
    correction = candle_at(allocator, 10, high="120", low="90", is_correction=True, recorded_offset_seconds=5)
    frontier_corr = frontier_at(correction.recorded_time)
    provider.enqueue_pending(subject_id, [_swing_envelope(correction, kind="candle", frontier=frontier_corr)])

    with pytest.raises(RuntimeError):
        owner.process_certified_frontier(frontier_corr)

    assert len(committer.log[subject_id]) == 1  # only the original -- the failed batch has zero effect
    assert engine._lineage[key].head_fact is original_head  # unchanged
    assert engine._lineage[key].head_fact == original_events[0]
    assert owner.state is SubjectOwnershipState.REVOKED


# --- Catch-up (§C) -----------------------------------------------------------


def test_positive_empty_history_proof_allows_activation_for_new_subject(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _regime_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )
    empty_frontier = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
    reconciled = owner.acquire_and_activate(catch_up_frontier=empty_frontier)
    assert reconciled == ()
    assert owner.state is SubjectOwnershipState.ACTIVE


def test_absent_provider_history_cannot_activate(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _regime_engine(allocator, time_source)
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()  # subject never registered at all
    owner = AuthoritativeSubjectOwner(
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )
    with pytest.raises(UnprovenCatchUpError):
        owner.acquire_and_activate(catch_up_frontier=frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT))
    assert owner.state is not SubjectOwnershipState.ACTIVE


def test_catch_up_reconstructs_regime_lineage_using_canonical_refs_and_allocates_zero_new_refs(
    time_source: FixedDeltaTimeSource,
) -> None:
    reference_allocator = SequenceAllocator(
        module_id="feature-engine", implementation_version="0.1.0", run_id="reference-run"
    )
    reference_engine = _regime_engine(reference_allocator, time_source)
    subject_id = reference_engine.scope.feature_subject_id

    fact_1 = regime_classified_at(reference_allocator, 0, computed_metric="1.50")
    frontier_1 = frontier_at(fact_1.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    computed_1 = only_computed(reference_engine.on_regime_classified(fact_1, cursor=frontier_1)[0])

    invalidation_fact = regime_invalidated_at(
        reference_allocator, invalidated_fact_ref=fact_1.ref, recorded_time=computed_1.recorded_time
    )
    frontier_2 = frontier_at(computed_1.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    invalidated_1 = only_invalidated(reference_engine.on_regime_invalidated(invalidation_fact, cursor=frontier_2)[0])

    fact_2 = regime_classified_at(reference_allocator, 0, computed_metric="1.75", recorded_offset_seconds=5)
    frontier_3 = frontier_at(fact_2.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    computed_2 = only_computed(reference_engine.on_regime_classified(fact_2, cursor=frontier_3)[0])

    provider = InMemoryLineageHistoryProvider()
    provider.register_upstream(
        subject_id,
        [
            _regime_envelope(fact_1, kind="regime_classified", frontier=frontier_1),
            _regime_envelope(invalidation_fact, kind="regime_invalidated", frontier=frontier_2),
            _regime_envelope(fact_2, kind="regime_classified", frontier=frontier_3),
        ],
    )
    provider.register_canonical(subject_id, [computed_1, invalidated_1, computed_2])

    fresh_allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="fresh-run")
    fresh_engine = _regime_engine(fresh_allocator, time_source)
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=fresh_allocator, time_source=time_source)
    owner = AuthoritativeSubjectOwner(
        engine=fresh_engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )
    reconciled = owner.acquire_and_activate(catch_up_frontier=frontier_3)

    assert reconciled == (computed_1, invalidated_1, computed_2)
    assert owner.state is SubjectOwnershipState.ACTIVE
    assert fresh_allocator._sequences == {}  # zero new refs allocated during catch-up
    key = (fact_2.window_start, fact_2.window_end)
    assert fresh_engine._lineage[key].head_fact.ref == computed_2.ref
    assert fresh_engine._lineage[key].head_fact.ref.event_id.startswith("reference-run")


def test_catch_up_mismatch_fails_closed(time_source: FixedDeltaTimeSource) -> None:
    reference_allocator = SequenceAllocator(
        module_id="feature-engine", implementation_version="0.1.0", run_id="reference-run"
    )
    reference_engine = _regime_engine(reference_allocator, time_source)
    subject_id = reference_engine.scope.feature_subject_id

    fact_1 = regime_classified_at(reference_allocator, 0, computed_metric="1.50")
    frontier_1 = frontier_at(fact_1.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    computed_1 = only_computed(reference_engine.on_regime_classified(fact_1, cursor=frontier_1)[0])

    # deliberately WRONG canonical value -- must never be silently accepted
    tampered = dataclasses.replace(computed_1, value=computed_1.value + 1)

    provider = InMemoryLineageHistoryProvider()
    provider.register_upstream(subject_id, [_regime_envelope(fact_1, kind="regime_classified", frontier=frontier_1)])
    provider.register_canonical(subject_id, [tampered])

    fresh_allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="fresh-run")
    fresh_engine = _regime_engine(fresh_allocator, time_source)
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=fresh_allocator, time_source=time_source)
    owner = AuthoritativeSubjectOwner(
        engine=fresh_engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )
    with pytest.raises(CanonicalHistoryMismatchError):
        owner.acquire_and_activate(catch_up_frontier=frontier_1)
    assert owner.state is not SubjectOwnershipState.ACTIVE
    assert owner.is_terminal is True  # ADR043-IMPL-A-MAJ-05

    # The SAME owner (wrapping the SAME, now possibly-dirty engine instance) can
    # never reacquire again -- even resupplying the correct canonical value would
    # not help, since it is the OWNER instance itself that is permanently retired.
    provider._canonical[subject_id] = [computed_1]  # noqa: SLF001 -- correct the canonical record for illustration
    with pytest.raises(OwnershipAuthorityUnavailableError):
        owner.acquire_and_activate(catch_up_frontier=frontier_1)


def test_catch_up_incomplete_canonical_history_fails_closed(time_source: FixedDeltaTimeSource) -> None:
    reference_allocator = SequenceAllocator(
        module_id="feature-engine", implementation_version="0.1.0", run_id="reference-run"
    )
    reference_engine = _regime_engine(reference_allocator, time_source)
    subject_id = reference_engine.scope.feature_subject_id

    fact_1 = regime_classified_at(reference_allocator, 0, computed_metric="1.50")
    frontier_1 = frontier_at(fact_1.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    reference_engine.on_regime_classified(fact_1, cursor=frontier_1)

    provider = InMemoryLineageHistoryProvider()
    provider.register_upstream(subject_id, [_regime_envelope(fact_1, kind="regime_classified", frontier=frontier_1)])
    provider.register_canonical(subject_id, [])  # missing -- the upstream replay expects one FeatureComputed

    fresh_allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="fresh-run")
    fresh_engine = _regime_engine(fresh_allocator, time_source)
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=fresh_allocator, time_source=time_source)
    owner = AuthoritativeSubjectOwner(
        engine=fresh_engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )
    with pytest.raises(CanonicalHistoryMismatchError):
        owner.acquire_and_activate(catch_up_frontier=frontier_1)


def test_catch_up_reconstructs_non_selected_swing_state_matching_reference_after_live_invalidation(
    time_source: FixedDeltaTimeSource,
) -> None:
    """ADR043-IMPLDESIGN-A-MAJ-03: a Swing confirmation that never wins the
    total order for any window leaves no trace in Feature's own output, yet
    catch-up must still reconstruct it (by replaying the certified upstream
    Swing history itself, not only canonical Feature output) so a LATER
    live operation that depends on it (falling back to it after the winner
    is invalidated) produces the same result a continuously-running engine
    would have produced.
    """
    reference_allocator = SequenceAllocator(
        module_id="feature-engine", implementation_version="0.1.0", run_id="reference-run"
    )
    reference_engine = _swing_engine(reference_allocator, time_source)
    subject_id = reference_engine.scope.feature_subject_id

    swing_a = swing_confirmed_at(reference_allocator, pivot_index=0, swing_id="swing-a")
    frontier_a = frontier_at(swing_a.recorded_time)
    assert reference_engine.on_swing_confirmed(swing_a, cursor=frontier_a) == []

    swing_b = swing_confirmed_at(reference_allocator, pivot_index=5, swing_id="swing-b", recorded_offset_minutes=1)
    frontier_b = frontier_at(swing_b.recorded_time)
    assert reference_engine.on_swing_confirmed(swing_b, cursor=frontier_b) == []

    candle = candle_at(reference_allocator, 10, high="110", low="90")
    frontier_c = frontier_at(candle.recorded_time)
    computed = only_computed(reference_engine.on_candle(candle, cursor=frontier_c)[0])
    key = (candle.scope.window_start, candle.scope.window_end)
    assert reference_engine._lineage[key].used_swing_id == "swing-b"

    invalidate_b = swing_invalidated_at(
        reference_allocator, swing_id="swing-b", swing_revision=1, recorded_time=computed.recorded_time
    )
    frontier_d = frontier_at(invalidate_b.recorded_time)
    reference_events = reference_engine.on_swing_invalidated(invalidate_b, cursor=frontier_d)
    reference_replacement = only_computed(reference_events[1])
    assert reference_engine._lineage[key].used_swing_id == "swing-a"

    provider = InMemoryLineageHistoryProvider()
    # The provider is responsible for certifying a correctly SEQUENCED apply
    # set (README §D2/ADR-043 §D) — Candle and Swing are independent Chapter
    # 8 streams with no real causation edge between them, but THIS engine's
    # own eligibility selection depends on having locally ingested a Swing
    # confirmation before the Candle that depends on it is prepared (exactly
    # as an already-running engine driven by direct on_*/on_swing_confirmed
    # calls in the right order always has). This test's fake provider
    # encodes that ordering explicitly via causation_refs, honestly scoped
    # to this test double — a real production provider would need its own
    # genuine solution to this sequencing responsibility.
    provider.register_upstream(
        subject_id,
        [
            _swing_envelope(swing_a, kind="swing_confirmed", frontier=frontier_a),
            _swing_envelope(swing_b, kind="swing_confirmed", frontier=frontier_b),
            _swing_envelope(
                candle, kind="candle", frontier=frontier_c, causation_refs=(swing_a.ref, swing_b.ref)
            ),
        ],
    )
    provider.register_canonical(subject_id, [computed])

    fresh_allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="fresh-run")
    fresh_engine = _swing_engine(fresh_allocator, time_source)
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=fresh_allocator, time_source=time_source)
    owner = AuthoritativeSubjectOwner(
        engine=fresh_engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )
    reconciled = owner.acquire_and_activate(catch_up_frontier=frontier_c)
    assert reconciled == (computed,)
    assert fresh_allocator._sequences == {}
    assert fresh_engine._lineage[key].head_fact.ref == computed.ref

    provider.enqueue_pending(subject_id, [_swing_envelope(invalidate_b, kind="swing_invalidated", frontier=frontier_d)])
    live_events = owner.process_certified_frontier(frontier_d)

    assert len(live_events) == 2
    live_invalidated = only_invalidated(live_events[0])
    live_replacement = only_computed(live_events[1])
    assert live_invalidated.invalidated_fact_ref == computed.ref
    assert live_replacement.value == reference_replacement.value
    assert fresh_engine._lineage[key].used_swing_id == "swing-a"


def test_catch_up_never_calls_recorded_time_source_and_restores_canonical_timestamps() -> None:
    """ADR043-IMPL-A-MAJ-06: a `RecordedTimeSource` that raises on every
    call is wired into BOTH the wrapped engine's own direct-path time
    source AND the committer's live-materialization time source — catch-up
    must still succeed, proving `RecordedTimeSource.next_after` is never
    called anywhere on this path, and the reconciled event carries the
    EXACT canonical historical `recorded_time`, never an invented one.
    """
    reference_allocator = SequenceAllocator(
        module_id="feature-engine", implementation_version="0.1.0", run_id="reference-run"
    )
    reference_engine = _regime_engine(reference_allocator, FixedDeltaTimeSource())
    subject_id = reference_engine.scope.feature_subject_id

    fact_1 = regime_classified_at(reference_allocator, 0, computed_metric="1.50")
    frontier_1 = frontier_at(fact_1.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    computed_1 = only_computed(reference_engine.on_regime_classified(fact_1, cursor=frontier_1)[0])

    provider = InMemoryLineageHistoryProvider()
    provider.register_upstream(subject_id, [_regime_envelope(fact_1, kind="regime_classified", frontier=frontier_1)])
    provider.register_canonical(subject_id, [computed_1])

    fresh_allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="fresh-run")
    raising_time_source = RaisingRecordedTimeSource()
    fresh_engine = _regime_engine(fresh_allocator, raising_time_source)
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(
        authority=authority, allocator=fresh_allocator, time_source=raising_time_source
    )
    owner = AuthoritativeSubjectOwner(
        engine=fresh_engine, authority=authority, committer=committer, history_provider=provider
    )

    reconciled = owner.acquire_and_activate(catch_up_frontier=frontier_1)
    assert reconciled == (computed_1,)
    assert only_computed(reconciled[0]).recorded_time == computed_1.recorded_time
    assert owner.state is SubjectOwnershipState.ACTIVE
    key = (fact_1.window_start, fact_1.window_end)
    assert fresh_engine._lineage[key].head_fact.recorded_time == computed_1.recorded_time


def test_partial_frontier_progress_then_later_prepare_failure_marks_owner_terminal(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """ADR043-IMPL-A-MAJ-05: within ONE `process_certified_frontier` call,
    an earlier envelope in the certified apply set may already commit
    successfully (mutating the engine's local `_lineage`) before a LATER
    envelope in the SAME batch fails during `prepare_upstream_event` —
    never left `ACTIVE` with local state partially advanced and
    `_committed_frontier` still stale; this owner must become terminal.
    """
    engine = _regime_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        engine=engine, authority=authority, committer=committer, history_provider=provider
    )
    empty_frontier = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
    owner.acquire_and_activate(catch_up_frontier=empty_frontier)
    original_committed = owner._committed_frontier  # noqa: SLF001

    good_fact = regime_classified_at(allocator, 0, computed_metric="1.5")
    # References a window this engine has never seen -- prepare_regime_invalidated
    # raises FeatureLineageError for it.
    bad_invalidation = regime_invalidated_at(
        allocator,
        invalidated_fact_ref=EventRecordRef(stream_id="raw-regime-engine-regime", sequence=999, event_id="bogus"),
        recorded_time=good_fact.recorded_time + timedelta(seconds=1),
    )
    frontier = frontier_at(bad_invalidation.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    provider.enqueue_pending(
        subject_id,
        [
            _regime_envelope(good_fact, kind="regime_classified", frontier=frontier),
            _regime_envelope(bad_invalidation, kind="regime_invalidated", frontier=frontier),
        ],
    )

    with pytest.raises(FeatureLineageError):
        owner.process_certified_frontier(frontier)

    # The first envelope's transition DID commit and DID mutate local _lineage...
    key = (good_fact.window_start, good_fact.window_end)
    assert key in engine._lineage
    # ...yet the checkpoint never advanced, and the owner is now permanently terminal.
    assert owner._committed_frontier == original_committed  # noqa: SLF001
    assert owner.is_terminal is True
    with pytest.raises(OwnershipAuthorityUnavailableError):
        owner.acquire_and_activate(catch_up_frontier=empty_frontier)


def test_fresh_owner_and_fresh_engine_recover_canonical_state_after_prior_owner_goes_terminal(
    time_source: FixedDeltaTimeSource,
) -> None:
    """ADR043-IMPL-A-MAJ-05's own prescribed recovery path: after an owner
    goes terminal (here, via explicit `revoke()`), a genuinely fresh
    analytical engine instance plus a genuinely fresh
    `AuthoritativeSubjectOwner` — never the retired owner/engine pair —
    performs canonical catch-up and reaches the exact same committed state.
    """
    allocator_1 = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="owner-1-run")
    engine_1 = _regime_engine(allocator_1, time_source)
    subject_id = engine_1.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer_1 = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_1, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner_1 = AuthoritativeSubjectOwner(
        engine=engine_1, authority=authority, committer=committer_1, history_provider=provider
    )
    empty_frontier = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
    owner_1.acquire_and_activate(catch_up_frontier=empty_frontier)

    fact_1 = regime_classified_at(allocator_1, 0, computed_metric="1.50")
    frontier_1 = frontier_at(fact_1.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    provider.enqueue_pending(subject_id, [_regime_envelope(fact_1, kind="regime_classified", frontier=frontier_1)])
    committed_events = owner_1.process_certified_frontier(frontier_1)
    committed_computed = only_computed(committed_events[0])

    # A real provider would now be able to read this back as canonical output
    # history; this fake is fed explicitly from the committer's own log.
    provider.register_upstream(subject_id, [_regime_envelope(fact_1, kind="regime_classified", frontier=frontier_1)])
    provider.register_canonical(subject_id, list(committer_1.log[subject_id]))

    owner_1.revoke()
    assert owner_1.is_terminal is True
    with pytest.raises(OwnershipAuthorityUnavailableError):
        owner_1.acquire_and_activate(catch_up_frontier=empty_frontier)

    allocator_2 = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="owner-2-run")
    engine_2 = _regime_engine(allocator_2, time_source)
    committer_2 = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_2, time_source=time_source)
    owner_2 = AuthoritativeSubjectOwner(
        engine=engine_2, authority=authority, committer=committer_2, history_provider=provider
    )
    reconciled = owner_2.acquire_and_activate(catch_up_frontier=frontier_1)

    assert reconciled == (committed_computed,)
    assert owner_2.state is SubjectOwnershipState.ACTIVE
    key = (fact_1.window_start, fact_1.window_end)
    assert engine_2._lineage[key].head_fact.ref == committed_computed.ref
