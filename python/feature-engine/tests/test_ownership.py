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
from dataclasses import dataclass, field

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
    DualOwnershipError,
    NonMonotonicApplicationOrderError,
    OwnershipAuthorityUnavailableError,
    StaleOwnershipGenerationError,
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
        finalized = prepared.finalize_live(refs)
        self.log.setdefault(feature_subject_id, []).extend(finalized)
        return finalized


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


def test_p_run_sort_does_not_wait_for_a_hypothetical_future_event_outside_the_apply_set() -> None:
    """ADR043-IMPLDESIGN-A-MAJ-02 Case 2: a causation_ref pointing OUTSIDE
    this bounded apply set is treated as already-satisfied/committed — the
    event is processed now, never blocked waiting for a hypothetical future
    member of a different apply set.
    """
    ref_b = _mk_ref("stream-b", 1)
    envelope_b = _mk_envelope(ref_b, causation_refs=(_mk_ref("stream-a", 1),))
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
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator)
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
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        feature_subject_id=subject_id,
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
        merge_policy=REGIME_INPUT_CONTRACT.merge_policy,
    )
    empty_frontier = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
    owner.acquire_and_activate(catch_up_frontier=empty_frontier)
    with pytest.raises(DualOwnershipError):
        owner.acquire_and_activate(catch_up_frontier=empty_frontier)


def test_process_certified_frontier_fails_closed_when_never_activated(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _regime_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator)
    provider = InMemoryLineageHistoryProvider()
    owner = AuthoritativeSubjectOwner(
        feature_subject_id=subject_id,
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
        merge_policy=REGIME_INPUT_CONTRACT.merge_policy,
    )
    frontier = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
    with pytest.raises(OwnershipAuthorityUnavailableError):
        owner.process_certified_frontier(frontier)


def test_owner_fences_unusable_after_stale_generation_detected_and_requires_reacquire(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _regime_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        feature_subject_id=subject_id,
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
        merge_policy=REGIME_INPUT_CONTRACT.merge_policy,
    )
    empty_frontier = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
    owner.acquire_and_activate(catch_up_frontier=empty_frontier)
    state_after_activate: SubjectOwnershipState = owner.state
    assert state_after_activate is SubjectOwnershipState.ACTIVE

    authority.acquire(subject_id)  # external successor acquisition fences this owner's generation

    fact = regime_classified_at(allocator, 0, computed_metric="1.5")
    frontier = frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    provider.enqueue_pending(subject_id, [_regime_envelope(fact, kind="regime_classified", frontier=frontier)])

    with pytest.raises(StaleOwnershipGenerationError):
        owner.process_certified_frontier(frontier)
    state_after_stale_commit: SubjectOwnershipState = owner.state
    assert state_after_stale_commit is SubjectOwnershipState.REVOKED

    with pytest.raises(OwnershipAuthorityUnavailableError):
        owner.process_certified_frontier(frontier)

    owner.acquire_and_activate(catch_up_frontier=empty_frontier)
    state_after_reactivate: SubjectOwnershipState = owner.state
    assert state_after_reactivate is SubjectOwnershipState.ACTIVE


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
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        feature_subject_id=subject_id,
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
        merge_policy=REGIME_INPUT_CONTRACT.merge_policy,
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


# --- Atomic batch commit (§B "Atomicity and emission") ----------------------


def test_batch_commit_invalidate_and_replace_commits_atomically(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _swing_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        feature_subject_id=subject_id,
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
        merge_policy=SWING_DISTANCE_INPUT_CONTRACT.merge_policy,
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
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        feature_subject_id=subject_id,
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
        merge_policy=SWING_DISTANCE_INPUT_CONTRACT.merge_policy,
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
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_id)
    owner = AuthoritativeSubjectOwner(
        feature_subject_id=subject_id,
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
        merge_policy=REGIME_INPUT_CONTRACT.merge_policy,
    )
    empty_frontier = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
    reconciled = owner.acquire_and_activate(catch_up_frontier=empty_frontier)
    assert reconciled == ()
    assert owner.state is SubjectOwnershipState.ACTIVE


def test_absent_provider_history_cannot_activate(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _regime_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator)
    provider = InMemoryLineageHistoryProvider()  # subject never registered at all
    owner = AuthoritativeSubjectOwner(
        feature_subject_id=subject_id,
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
        merge_policy=REGIME_INPUT_CONTRACT.merge_policy,
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
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=fresh_allocator)
    owner = AuthoritativeSubjectOwner(
        feature_subject_id=subject_id,
        engine=fresh_engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
        merge_policy=REGIME_INPUT_CONTRACT.merge_policy,
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
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=fresh_allocator)
    owner = AuthoritativeSubjectOwner(
        feature_subject_id=subject_id,
        engine=fresh_engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
        merge_policy=REGIME_INPUT_CONTRACT.merge_policy,
    )
    with pytest.raises(CanonicalHistoryMismatchError):
        owner.acquire_and_activate(catch_up_frontier=frontier_1)
    assert owner.state is not SubjectOwnershipState.ACTIVE


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
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=fresh_allocator)
    owner = AuthoritativeSubjectOwner(
        feature_subject_id=subject_id,
        engine=fresh_engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
        merge_policy=REGIME_INPUT_CONTRACT.merge_policy,
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
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=fresh_allocator)
    owner = AuthoritativeSubjectOwner(
        feature_subject_id=subject_id,
        engine=fresh_engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
        merge_policy=SWING_DISTANCE_INPUT_CONTRACT.merge_policy,
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
