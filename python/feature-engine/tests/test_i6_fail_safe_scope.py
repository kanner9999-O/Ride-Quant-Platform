"""Feature Engine EVID-06 — I-6 "Fail-Safe by Scope" Feature-LOCAL formal
fault-injection evidence (`docs/governance/quality-gate/feature-engine-
chapter13-remediation-plan-001.md` §9, bounded correction 001, Review A
CLEAN).

Proves the Feature-local half of I-6's own Verification clause only:

    fault injection + blast-radius correctness + no invalid authoritative
    Feature transition/commit + committed-history preservation + correct
    bounded recovery

Every qualifying test below asserts BOTH sides: the affected scope fails
safely AND an unrelated control scope (a different `feature_subject_id`,
sharing the SAME infrastructure where applicable) remains fully
operational. This module does NOT, and must never be read to, assert the
platform-level "risk not increased according to authoritative risk
metric/policy" half of I-6's Verification clause — that remains
`BLOCKED_BY_EXTERNAL_DEPENDENCY` (no Risk Gateway/Decision Pipeline exists
anywhere in this repository).

Six rows, matching §9.6's corrected evidence-matrix design exactly (the
SUBJECT tier is the floor — no WINDOW tier, per §9.3's own correction):

  Row 1 (SUBJECT) — stale ownership generation
  Row 2 (SUBJECT) — terminal owner + fresh-owner recovery
  Row 3 (SUBJECT) — unproven catch-up + fresh-owner recovery
  Row 4 (SUBJECT) — canonical history mismatch + fresh-owner recovery
  Row 5 (SUBJECT) — runtime frontier/cursor mismatch against an
                     already-cached authority, NOT a provider outage
  Row 6 (SHARED UPSTREAM AUTHORITY) — construction-time Input Contract
                     resolver failure, isolated from already-cached
                     engines and from an unrelated profile/provider

All test doubles are deterministic fakes at real Protocol boundaries
(`SubjectOwnershipAuthority`/`FencedFeatureCommitter`/
`AuthoritativeLineageHistoryProvider`/`InputContractAuthorityProvider`),
reusing the SAME in-memory fakes already defined in `test_ownership.py`
— never a distinct/competing implementation, never a monkeypatch of
engine/resolver internals. Real production Feature Engine logic
(`RegimePassthroughFeatureEngine`, `SwingDistanceFeatureEngine`,
`AuthoritativeSubjectOwner`) is exercised throughout.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal

import pytest
from conftest import (
    BASE,
    OUTPUT_EVENT_CONTRACT_AUTHORITY,
    REGIME_INPUT_CONTRACT,
    SWING_DISTANCE_INPUT_CONTRACT,
    FixedDeltaTimeSource,
    candle_at,
    feature_scope,
    frontier_at,
    make_regime_definition,
    only_computed,
    regime_classified_at,
    swing_confirmed_at,
)
from test_ownership import (
    InMemoryFencedFeatureCommitter,
    InMemoryLineageHistoryProvider,
    InMemorySubjectOwnershipAuthority,
    _regime_engine,
    _regime_envelope,
    _swing_engine,
    _swing_envelope,
)

from feature_engine import (
    FeatureComputationProfile,
    RegimePassthroughFeatureEngine,
    SequenceAllocator,
    StaticInputContractAuthorityProvider,
    StaticOutputEventContractAuthorityProvider,
)
from feature_engine.contracts import VerifiedInputContractAuthority
from feature_engine.errors import (
    CanonicalHistoryMismatchError,
    InputContractIdentityMismatchError,
    OwnershipAuthorityUnavailableError,
    RegistryContractMismatchError,
    StaleOwnershipGenerationError,
    UnprovenCatchUpError,
)
from feature_engine.ownership import AuthoritativeSubjectOwner, SubjectOwnershipState

# =============================================================================
# ROW 6's toggleable Input Contract resolver double
# =============================================================================


@dataclass
class _ToggleableInputContractAuthorityProvider:
    """TEST-ONLY `InputContractAuthorityProvider` (Row 6): wraps a real,
    already-resolved `VerifiedInputContractAuthority` for exactly one
    `feature_computation_profile`. `.broken` toggles whether
    `.resolve(profile)` raises — simulating the SHARED resolver/artifact
    becoming unavailable for that profile — or delegates to the real,
    healthy, cached authority. A genuine Protocol-boundary double,
    structurally identical to `StaticInputContractAuthorityProvider`
    (`authority_resolver.py`) with one added toggle; never a monkeypatch
    of engine/resolver internals.
    """

    authority: VerifiedInputContractAuthority
    broken: bool = False

    def resolve(self, profile: FeatureComputationProfile) -> VerifiedInputContractAuthority:
        if self.broken:
            raise RuntimeError(
                "TEST-ONLY forced Input Contract resolver failure -- simulates the shared "
                "artifact/resolver becoming unavailable for this profile"
            )
        if self.authority.feature_computation_profile != profile:
            raise InputContractIdentityMismatchError(
                f"this TEST-ONLY provider's own wrapped authority has feature_computation_profile="
                f"{self.authority.feature_computation_profile!r}, which does not match the requested "
                f"profile {profile!r}"
            )
        return self.authority


# =============================================================================
# ROW 1 (SUBJECT) — stale ownership generation
# =============================================================================


def test_row1_stale_ownership_generation_isolates_to_subject_a(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Subject A's stale-generation commit attempt fails closed with zero
    effect; subject B, sharing the SAME authority/allocator/committer/
    provider infrastructure, continues normal authoritative processing.
    """
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()

    engine_a = _regime_engine(allocator, time_source)
    subject_a = engine_a.scope.feature_subject_id
    stream_id = engine_a.resolved_output_event_contract_authority.authoritative_stream_id
    stale_generation = authority.acquire(subject_a)
    authority.acquire(subject_a)  # mints a successor, fencing stale_generation

    fact_a = regime_classified_at(allocator, 0, computed_metric="1.50")
    frontier_a = frontier_at(fact_a.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    prepared_a = engine_a.prepare_regime_classified(fact_a, cursor=frontier_a)
    assert prepared_a is not None

    with pytest.raises(StaleOwnershipGenerationError):
        committer.commit(
            feature_subject_id=subject_a,
            ownership_generation=stale_generation,
            stream_id=stream_id,
            prepared=prepared_a,
        )
    # Affected scope fails safely: zero effect from the rejected attempt.
    assert committer.log.get(subject_a, []) == []  # no canonical append
    assert allocator._sequences.get(stream_id) is None  # noqa: SLF001 -- no sequence consumed
    assert engine_a._lineage == {}  # noqa: SLF001 -- no authoritative lineage advance

    # Unaffected control: subject B, SAME shared authority/allocator/
    # committer/provider infrastructure, processes normally end-to-end.
    engine_b = _swing_engine(allocator, time_source)
    subject_b = engine_b.scope.feature_subject_id
    provider.register_known_empty(subject_b)
    owner_b = AuthoritativeSubjectOwner(
        engine=engine_b, authority=authority, committer=committer, history_provider=provider
    )
    owner_b.acquire_and_activate(catch_up_frontier=frontier_at(BASE))

    swing = swing_confirmed_at(allocator, pivot_index=0, swing_id="row1-swing")
    frontier_swing = frontier_at(swing.recorded_time)
    provider.enqueue_pending(subject_b, [_swing_envelope(swing, kind="swing_confirmed", frontier=frontier_swing)])
    owner_b.process_certified_frontier(frontier_swing)

    candle = candle_at(allocator, 10, high="110", low="90")
    frontier_candle = frontier_at(candle.recorded_time)
    provider.enqueue_pending(subject_b, [_swing_envelope(candle, kind="candle", frontier=frontier_candle)])
    committed_b = owner_b.process_certified_frontier(frontier_candle)

    assert len(committed_b) == 1
    assert len(committer.log[subject_b]) == 1
    assert owner_b.state is SubjectOwnershipState.ACTIVE
    # Proves blast radius = subject A's stale generation only, never the
    # shared allocator/committer infrastructure itself.
    assert subject_a != subject_b


# =============================================================================
# ROW 2 (SUBJECT) — terminal owner + fresh-owner recovery
# =============================================================================


def test_row2_terminal_owner_never_reacquires_and_recovery_via_fresh_owner_does_not_affect_subject_b(
    time_source: FixedDeltaTimeSource,
) -> None:
    allocator_a1 = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="row2-a1")
    engine_a1 = _regime_engine(allocator_a1, time_source)
    subject_a = engine_a1.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer_a1 = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_a1, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_a)
    owner_a1 = AuthoritativeSubjectOwner(
        engine=engine_a1, authority=authority, committer=committer_a1, history_provider=provider
    )
    empty_frontier = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
    owner_a1.acquire_and_activate(catch_up_frontier=empty_frontier)

    fact_1 = regime_classified_at(allocator_a1, 0, computed_metric="1.50")
    frontier_1 = frontier_at(fact_1.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    provider.enqueue_pending(subject_a, [_regime_envelope(fact_1, kind="regime_classified", frontier=frontier_1)])
    committed_events = owner_a1.process_certified_frontier(frontier_1)
    committed_computed = only_computed(committed_events[0])

    # Unaffected control B, constructed alongside, SAME shared authority/provider.
    allocator_b = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="row2-b")
    engine_b = _swing_engine(allocator_b, time_source)
    subject_b = engine_b.scope.feature_subject_id
    committer_b = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_b, time_source=time_source)
    provider.register_known_empty(subject_b)
    owner_b = AuthoritativeSubjectOwner(
        engine=engine_b, authority=authority, committer=committer_b, history_provider=provider
    )
    owner_b.acquire_and_activate(catch_up_frontier=frontier_at(BASE))
    swing = swing_confirmed_at(allocator_b, pivot_index=0, swing_id="row2-swing")
    frontier_swing = frontier_at(swing.recorded_time)
    provider.enqueue_pending(subject_b, [_swing_envelope(swing, kind="swing_confirmed", frontier=frontier_swing)])
    owner_b.process_certified_frontier(frontier_swing)
    candle = candle_at(allocator_b, 10, high="110", low="90")
    frontier_candle = frontier_at(candle.recorded_time)
    provider.enqueue_pending(subject_b, [_swing_envelope(candle, kind="candle", frontier=frontier_candle)])
    committed_b_before = owner_b.process_certified_frontier(frontier_candle)
    assert len(committed_b_before) == 1
    assert len(committer_b.log[subject_b]) == 1

    # Fault: an external successor acquisition fences owner_a1's generation.
    authority.acquire(subject_a)
    fact_2 = regime_classified_at(allocator_a1, 1, computed_metric="1.75")  # a DIFFERENT window -- legal original
    frontier_2 = frontier_at(fact_2.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    provider.enqueue_pending(subject_a, [_regime_envelope(fact_2, kind="regime_classified", frontier=frontier_2)])

    with pytest.raises(StaleOwnershipGenerationError):
        owner_a1.process_certified_frontier(frontier_2)
    assert owner_a1.state is SubjectOwnershipState.REVOKED
    assert owner_a1.is_terminal is True

    with pytest.raises(OwnershipAuthorityUnavailableError):
        owner_a1.process_certified_frontier(frontier_2)
    with pytest.raises(OwnershipAuthorityUnavailableError):
        owner_a1.acquire_and_activate(catch_up_frontier=empty_frontier)  # never reacquire the SAME owner

    # B remains fully unaffected by A's failure.
    assert owner_b.state is SubjectOwnershipState.ACTIVE
    assert len(committer_b.log[subject_b]) == 1

    # Recovery: fresh analytical engine + fresh owner + fresh generation +
    # canonical catch-up -- never the retired owner_a1/engine_a1 pair.
    provider.register_upstream(subject_a, [_regime_envelope(fact_1, kind="regime_classified", frontier=frontier_1)])
    provider.register_canonical(subject_a, list(committer_a1.log[subject_a]))
    allocator_a2 = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="row2-a2")
    engine_a2 = _regime_engine(allocator_a2, time_source)
    committer_a2 = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_a2, time_source=time_source)
    owner_a2 = AuthoritativeSubjectOwner(
        engine=engine_a2, authority=authority, committer=committer_a2, history_provider=provider
    )
    reconciled = owner_a2.acquire_and_activate(catch_up_frontier=frontier_1)

    assert reconciled == (committed_computed,)
    assert owner_a2.state is SubjectOwnershipState.ACTIVE
    key = (fact_1.window_start, fact_1.window_end)
    assert engine_a2._lineage[key].head_fact.ref == committed_computed.ref  # noqa: SLF001

    # B remains unaffected by A's whole failure+recovery sequence too.
    assert owner_b.state is SubjectOwnershipState.ACTIVE
    assert len(committer_b.log[subject_b]) == 1


# =============================================================================
# ROW 3 (SUBJECT) — unproven catch-up + fresh-owner recovery
# =============================================================================


def test_row3_unproven_catch_up_terminalizes_owner_and_recovery_via_fresh_owner_does_not_affect_subject_b(
    time_source: FixedDeltaTimeSource,
) -> None:
    allocator_a1 = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="row3-a1")
    engine_a1 = _regime_engine(allocator_a1, time_source)
    subject_a = engine_a1.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer_a1 = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_a1, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()  # subject_a never registered -- ambiguous/unproven
    owner_a1 = AuthoritativeSubjectOwner(
        engine=engine_a1, authority=authority, committer=committer_a1, history_provider=provider
    )
    frontier_a = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)

    with pytest.raises(UnprovenCatchUpError):
        owner_a1.acquire_and_activate(catch_up_frontier=frontier_a)
    assert owner_a1.state is not SubjectOwnershipState.ACTIVE
    assert owner_a1.is_terminal is True  # a generation was already acquired before catch-up failed
    assert committer_a1.log.get(subject_a, []) == []  # A emits/commits nothing

    with pytest.raises(OwnershipAuthorityUnavailableError):
        owner_a1.acquire_and_activate(catch_up_frontier=frontier_a)  # never retry the SAME owner

    # Unaffected control B, independently resolving through the SAME provider.
    allocator_b = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="row3-b")
    engine_b = _swing_engine(allocator_b, time_source)
    subject_b = engine_b.scope.feature_subject_id
    committer_b = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_b, time_source=time_source)
    provider.register_known_empty(subject_b)  # B's own proof IS registered
    owner_b = AuthoritativeSubjectOwner(
        engine=engine_b, authority=authority, committer=committer_b, history_provider=provider
    )
    reconciled_b = owner_b.acquire_and_activate(catch_up_frontier=frontier_at(BASE))
    assert reconciled_b == ()
    assert owner_b.state is SubjectOwnershipState.ACTIVE

    # Recovery for A: corrected provider registration + FRESH engine + FRESH
    # owner + fresh generation -- never retry the terminal owner_a1.
    provider.register_known_empty(subject_a)
    allocator_a2 = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="row3-a2")
    engine_a2 = _regime_engine(allocator_a2, time_source)
    committer_a2 = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_a2, time_source=time_source)
    owner_a2 = AuthoritativeSubjectOwner(
        engine=engine_a2, authority=authority, committer=committer_a2, history_provider=provider
    )
    reconciled_a2 = owner_a2.acquire_and_activate(catch_up_frontier=frontier_a)
    assert reconciled_a2 == ()
    assert owner_a2.state is SubjectOwnershipState.ACTIVE

    # B remains unaffected by A's whole failure+recovery sequence.
    assert owner_b.state is SubjectOwnershipState.ACTIVE


# =============================================================================
# ROW 4 (SUBJECT) — canonical history mismatch + fresh-owner recovery
# =============================================================================


def test_row4_canonical_history_mismatch_terminalizes_owner_and_recovery_via_fresh_owner_does_not_affect_subject_b(
    time_source: FixedDeltaTimeSource,
) -> None:
    reference_allocator = SequenceAllocator(
        module_id="feature-engine", implementation_version="0.1.0", run_id="row4-ref"
    )
    reference_engine = _regime_engine(reference_allocator, time_source)
    subject_a = reference_engine.scope.feature_subject_id

    fact_1 = regime_classified_at(reference_allocator, 0, computed_metric="1.50")
    frontier_1 = frontier_at(fact_1.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    computed_1 = only_computed(reference_engine.on_regime_classified(fact_1, cursor=frontier_1)[0])

    tampered = dataclasses.replace(computed_1, value=computed_1.value + 1)  # genuine canonical/upstream mismatch

    authority = InMemorySubjectOwnershipAuthority()
    provider = InMemoryLineageHistoryProvider()
    provider.register_upstream(subject_a, [_regime_envelope(fact_1, kind="regime_classified", frontier=frontier_1)])
    provider.register_canonical(subject_a, [tampered])

    allocator_a1 = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="row4-a1")
    engine_a1 = _regime_engine(allocator_a1, time_source)
    committer_a1 = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_a1, time_source=time_source)
    owner_a1 = AuthoritativeSubjectOwner(
        engine=engine_a1, authority=authority, committer=committer_a1, history_provider=provider
    )

    with pytest.raises(CanonicalHistoryMismatchError):
        owner_a1.acquire_and_activate(catch_up_frontier=frontier_1)
    assert owner_a1.state is not SubjectOwnershipState.ACTIVE
    assert owner_a1.is_terminal is True
    assert allocator_a1._sequences == {}  # noqa: SLF001 -- zero new ref allocation during catch-up
    with pytest.raises(OwnershipAuthorityUnavailableError):
        owner_a1.acquire_and_activate(catch_up_frontier=frontier_1)  # never retry the SAME owner

    # Unaffected control B.
    allocator_b = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="row4-b")
    engine_b = _swing_engine(allocator_b, time_source)
    subject_b = engine_b.scope.feature_subject_id
    committer_b = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_b, time_source=time_source)
    provider.register_known_empty(subject_b)
    owner_b = AuthoritativeSubjectOwner(
        engine=engine_b, authority=authority, committer=committer_b, history_provider=provider
    )
    owner_b.acquire_and_activate(catch_up_frontier=frontier_at(BASE))
    assert owner_b.state is SubjectOwnershipState.ACTIVE

    # Recovery for A: corrected canonical history + FRESH engine + FRESH owner.
    provider._canonical[subject_a] = [computed_1]  # noqa: SLF001 -- correcting the canonical record
    allocator_a2 = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="row4-a2")
    engine_a2 = _regime_engine(allocator_a2, time_source)
    committer_a2 = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_a2, time_source=time_source)
    owner_a2 = AuthoritativeSubjectOwner(
        engine=engine_a2, authority=authority, committer=committer_a2, history_provider=provider
    )
    reconciled = owner_a2.acquire_and_activate(catch_up_frontier=frontier_1)
    assert reconciled == (computed_1,)
    assert owner_a2.state is SubjectOwnershipState.ACTIVE
    assert allocator_a2._sequences == {}  # noqa: SLF001

    assert owner_b.state is SubjectOwnershipState.ACTIVE  # unaffected throughout


# =============================================================================
# ROW 5 (SUBJECT) — runtime frontier/cursor mismatch, NOT a provider outage
# =============================================================================


def test_row5_runtime_frontier_mismatch_fails_closed_then_correct_frontier_succeeds_without_affecting_subject_b(
    time_source: FixedDeltaTimeSource,
) -> None:
    allocator_a = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="row5-a")
    engine_a = _regime_engine(allocator_a, time_source)
    subject_a = engine_a.scope.feature_subject_id
    authority = InMemorySubjectOwnershipAuthority()
    committer_a = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_a, time_source=time_source)
    provider = InMemoryLineageHistoryProvider()
    provider.register_known_empty(subject_a)
    owner_a = AuthoritativeSubjectOwner(
        engine=engine_a, authority=authority, committer=committer_a, history_provider=provider
    )
    empty_frontier = frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)
    owner_a.acquire_and_activate(catch_up_frontier=empty_frontier)
    cached_authority_before = engine_a.resolved_input_contract_authority

    # Unaffected control B, constructed alongside.
    allocator_b = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="row5-b")
    engine_b = _swing_engine(allocator_b, time_source)
    subject_b = engine_b.scope.feature_subject_id
    committer_b = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_b, time_source=time_source)
    provider.register_known_empty(subject_b)
    owner_b = AuthoritativeSubjectOwner(
        engine=engine_b, authority=authority, committer=committer_b, history_provider=provider
    )
    owner_b.acquire_and_activate(catch_up_frontier=frontier_at(BASE))

    # Inject ONE malformed caller-supplied EvaluationFrontier (wrong
    # stream_registry_version) against engine_a's ALREADY-cached, healthy
    # VerifiedInputContractAuthority -- explicitly NOT a provider outage;
    # the provider is never re-resolved to manufacture this fault.
    malformed_frontier = dataclasses.replace(
        frontier_at(BASE + timedelta(minutes=1), resolved_input_contract=REGIME_INPUT_CONTRACT),
        stream_registry_version="not-the-real-version",
    )
    with pytest.raises(RegistryContractMismatchError):
        owner_a.process_certified_frontier(malformed_frontier)
    assert owner_a._committed_frontier == empty_frontier  # noqa: SLF001 -- no checkpoint advance
    assert engine_a._lineage == {}  # noqa: SLF001 -- no authoritative lineage change
    assert committer_a.log.get(subject_a, []) == []  # no canonical append
    assert engine_a.resolved_input_contract_authority is cached_authority_before  # cached authority untouched
    assert owner_a.is_terminal is False  # pure frontier-validation failure -- owner survives

    # On the SAME still-valid subject/engine: a correct frontier now succeeds.
    fact = regime_classified_at(allocator_a, 0, computed_metric="1.50")
    good_frontier = frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    provider.enqueue_pending(subject_a, [_regime_envelope(fact, kind="regime_classified", frontier=good_frontier)])
    committed = owner_a.process_certified_frontier(good_frontier)
    assert len(committed) == 1
    assert owner_a.state is SubjectOwnershipState.ACTIVE

    # B's own independent processing succeeded throughout, unaffected by A's
    # transient bad-frontier rejection.
    swing = swing_confirmed_at(allocator_b, pivot_index=0, swing_id="row5-swing")
    frontier_swing = frontier_at(swing.recorded_time)
    provider.enqueue_pending(subject_b, [_swing_envelope(swing, kind="swing_confirmed", frontier=frontier_swing)])
    owner_b.process_certified_frontier(frontier_swing)
    candle = candle_at(allocator_b, 10, high="110", low="90")
    frontier_candle = frontier_at(candle.recorded_time)
    provider.enqueue_pending(subject_b, [_swing_envelope(candle, kind="candle", frontier=frontier_candle)])
    committed_b = owner_b.process_certified_frontier(frontier_candle)
    assert len(committed_b) == 1
    assert owner_b.state is SubjectOwnershipState.ACTIVE


# =============================================================================
# ROW 6 (SHARED UPSTREAM AUTHORITY) — construction-time resolver failure
# =============================================================================


def test_row6_construction_time_input_contract_resolver_failure_isolates_to_new_constructions(
    time_source: FixedDeltaTimeSource,
) -> None:
    """Models the ACTUAL resolver/profile/provider identity
    (`InputContractAuthorityProvider.resolve(profile)`), not a loose
    `feature_type=X` label: the toggleable provider below is keyed by
    `feature_computation_profile` exactly as the real Protocol requires.
    """
    provider_regime = _ToggleableInputContractAuthorityProvider(authority=REGIME_INPUT_CONTRACT)
    # Unrelated profile/provider instance -- healthy and untouched throughout.
    provider_swing = StaticInputContractAuthorityProvider(SWING_DISTANCE_INPUT_CONTRACT)

    definition = make_regime_definition(regime_dimension_version="rgd-1")
    scope_old = feature_scope("volatility_metric", version=definition.feature_definition_version)
    allocator_old = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="row6-old")
    engine_a_old = RegimePassthroughFeatureEngine(
        scope_old,
        definition,
        allocator_old,
        time_source,
        output_event_contract_authority_provider=StaticOutputEventContractAuthorityProvider(
            OUTPUT_EVENT_CONTRACT_AUTHORITY
        ),
        input_contract_authority_provider=provider_regime,
    )
    cached_authority = engine_a_old.resolved_input_contract_authority

    allocator_b = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="row6-b")
    engine_b = _swing_engine(allocator_b, time_source, input_contract_authority_provider=provider_swing)

    # Toggle: the shared "regime"-profile resolver becomes unavailable.
    provider_regime.broken = True

    scope_new = feature_scope(
        "volatility_metric", version=definition.feature_definition_version, instrument_id="ROW6-NEW-INSTRUMENT"
    )
    allocator_new = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="row6-new")
    with pytest.raises(RuntimeError):
        RegimePassthroughFeatureEngine(
            scope_new,
            definition,
            allocator_new,
            time_source,
            output_event_contract_authority_provider=StaticOutputEventContractAuthorityProvider(
                OUTPUT_EVENT_CONTRACT_AUTHORITY
            ),
            input_contract_authority_provider=provider_regime,
        )

    # Already-cached engine_a_old continues using its cached authority --
    # never re-resolved, never affected by the now-broken provider.
    assert engine_a_old.resolved_input_contract_authority is cached_authority
    fact = regime_classified_at(allocator_old, 0, computed_metric="1.50")
    frontier = frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    computed = only_computed(engine_a_old.on_regime_classified(fact, cursor=frontier)[0])
    assert computed.value == Decimal("1.50")

    # Unrelated profile/provider B remains fully operational throughout.
    assert engine_b.resolved_input_contract_authority is SWING_DISTANCE_INPUT_CONTRACT
    swing = swing_confirmed_at(allocator_b, pivot_index=0, swing_id="row6-swing")
    assert engine_b.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time)) == []

    # Restore: a fresh new construction for the "regime" profile succeeds again.
    provider_regime.broken = False
    engine_a_new = RegimePassthroughFeatureEngine(
        scope_new,
        definition,
        allocator_new,
        time_source,
        output_event_contract_authority_provider=StaticOutputEventContractAuthorityProvider(
            OUTPUT_EVENT_CONTRACT_AUTHORITY
        ),
        input_contract_authority_provider=provider_regime,
    )
    assert engine_a_new.resolved_input_contract_authority is REGIME_INPUT_CONTRACT
