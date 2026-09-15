"""Formal I-13 (State Transition Integrity) property-based evidence —
Testing Convention v0.17 (Approved 2026-09-15), mechanism: Hypothesis.

This module is the EVID-07 qualifying formal evidence suite
(`docs/governance/quality-gate/feature-engine-evid07-property-based-
mechanism-candidate-001.md`). It exercises the REAL production
implementations directly — `RegimePassthroughFeatureEngine`,
`SwingDistanceFeatureEngine`, `FeatureCurrentView`, `AuthoritativeSubjectOwner`,
`p_run_sort`, real `PreparedTransition` reconciliation, and real Feature
lineage error types — never a shadow re-implementation of Feature semantics
tested against itself.

Test doubles are used ONLY for the three external runtime boundaries that
deliberately have no production adapter yet (`SubjectOwnershipAuthority`,
`FencedFeatureCommitter`, `AuthoritativeLineageHistoryProvider`) — reusing
the SAME deterministic, explicitly TEST-ONLY fakes already defined in
`test_ownership.py` (`InMemorySubjectOwnershipAuthority`,
`InMemoryFencedFeatureCommitter`, `InMemoryLineageHistoryProvider`,
`RaisingRecordedTimeSource`), never a distinct/competing implementation.
These fakes prove Feature Engine's own governed ownership/fencing CONTRACT
(ADR-043) — they do NOT prove that any concrete production-durable
distributed-storage adapter exists. LIVE remains unauthorized; no such
adapter is implemented anywhere in this repository.

Hypothesis execution profiles (formal-evidence discipline):
  `ci`  — derandomize=True, print_blob=True, database=None, max_examples=200.
          Formal evidence commands MUST explicitly select this profile via
          `HYPOTHESIS_PROFILE=ci`. Never uses the local example database as
          evidence; a genuine minimized counterexample (or
          `@reproduce_failure(...)` payload) is the record of a failure —
          never a bare `@seed(...)` for an ordinary failure.
  `dev` — normal local Hypothesis behavior (its own local example database,
          default `max_examples`), for iterative local development only.
Neither profile is ever applied implicitly; `HYPOTHESIS_PROFILE` selects
between them (default `dev` when unset). `.hypothesis/` is never committed
(see `.gitignore`).
"""

from __future__ import annotations

import os
from datetime import timedelta
from decimal import Decimal

import pytest
from conftest import (
    BASE,
    OUTPUT_EVENT_CONTRACT_AUTHORITY,
    REGIME_INPUT_CONTRACT,
    FixedDeltaTimeSource,
    candle_at,
    feature_scope,
    frontier_at,
    make_regime_definition,
    only_computed,
    only_invalidated,
    regime_classified_at,
    regime_invalidated_at,
    swing_confirmed_at,
    swing_invalidated_at,
)
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, precondition, rule
from test_ownership import (
    _SUPPORTED_MERGE_POLICY,
    InMemoryFencedFeatureCommitter,
    InMemoryLineageHistoryProvider,
    InMemorySubjectOwnershipAuthority,
    RaisingRecordedTimeSource,
    _mk_envelope,
    _mk_ref,
    _regime_engine,
    _regime_envelope,
    _swing_engine,
    _swing_envelope,
)

from feature_engine import (
    EvaluationFrontier,
    EventRecordRef,
    FeatureComputed,
    FeatureCurrentView,
    FeatureFactInvalidated,
    RegimeClassifiedFact,
    RegimePassthroughFeatureEngine,
    SequenceAllocator,
    StaticInputContractAuthorityProvider,
    StaticOutputEventContractAuthorityProvider,
)
from feature_engine.errors import (
    ConflictingUpstreamEnvelopeError,
    FeatureLineageError,
    ForeignScopeError,
    InvalidSwingEligibilityInputError,
    NonMonotonicApplicationOrderError,
    StaleOwnershipGenerationError,
)
from feature_engine.ownership import AuthoritativeSubjectOwner, UpstreamEnvelope, p_run_sort

# --- Hypothesis execution profiles (Testing Convention v0.17, Part 4) ------

settings.register_profile(
    "ci",
    derandomize=True,
    print_blob=True,
    database=None,
    max_examples=200,
    suppress_health_check=[HealthCheck.too_slow],
)
settings.register_profile("dev")
settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "dev"))


def test_dev_profile_uses_hypothesis_library_default_max_examples() -> None:
    """Testing Convention v0.17 Part 4: the `dev` profile must use
    Hypothesis's own unmodified library-default `max_examples` (not a
    locally-tuned value) -- verified programmatically here, not merely
    by omitting an override above.
    """
    dev_profile = settings.get_profile("dev")
    library_default_profile = settings.get_profile("default")
    assert dev_profile.max_examples == library_default_profile.max_examples

# Bounded metric strategy shared across properties -- a genuine, non-trivial
# numeric domain (never a single fixed example) without pathological
# Decimal edge cases (NaN/Infinity are explicitly excluded; feature.md's
# own decimal_precision_policy rounds regardless).
_metric_strategy = st.decimals(
    min_value=Decimal("0.01"), max_value=Decimal("1000.00"), places=2, allow_nan=False, allow_infinity=False
)


# =============================================================================
# CATEGORY A/C — legal transition graph + correction/terminal semantics
# =============================================================================


class RegimeLegalTransitionMachine(RuleBasedStateMachine):
    """Property Category A (legal transition graph) + Category C (correction/
    terminal semantics over N generated corrections) — a single generated
    Feature subject/window driven through
    `ORIGINAL -> (INVALIDATE -> REPLACEMENT)*` using the REAL
    `RegimePassthroughFeatureEngine` and the REAL `FeatureCurrentView`,
    never a shadow re-implementation.
    """

    def __init__(self) -> None:
        super().__init__()
        self.allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="prop-a")
        self.time_source = FixedDeltaTimeSource()
        self.definition = make_regime_definition(regime_dimension_version="rgd-1")
        self.scope = feature_scope("volatility_metric", version=self.definition.feature_definition_version)
        self.engine = RegimePassthroughFeatureEngine(
            self.scope,
            self.definition,
            self.allocator,
            self.time_source,
            output_event_contract_authority_provider=StaticOutputEventContractAuthorityProvider(
                OUTPUT_EVENT_CONTRACT_AUTHORITY
            ),
            input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
        )
        self.view = FeatureCurrentView(self.scope)
        self.window_key = (BASE, BASE + timedelta(minutes=1))
        self.has_original = False
        self.invalidated = False
        self.last_evidence_ref: EventRecordRef | None = None
        self.current_head: FeatureComputed | None = None
        self.generation_count = 0
        self.history: list[FeatureComputed | FeatureFactInvalidated] = []

    def _window_frontier(self, recorded_time: object) -> EvaluationFrontier:
        return frontier_at(recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)  # type: ignore[arg-type]

    @precondition(lambda self: not self.has_original)
    @rule(metric=_metric_strategy)
    def submit_original(self, metric: Decimal) -> None:
        fact = regime_classified_at(self.allocator, 0, computed_metric=str(metric))
        cursor = self._window_frontier(fact.recorded_time)
        events = self.engine.on_regime_classified(fact, cursor=cursor)
        assert len(events) == 1
        computed = only_computed(events[0])
        assert computed.supersedes_fact_ref is None
        self.view.on_feature_computed(computed)
        self.history.append(computed)
        self.has_original = True
        self.invalidated = False
        self.last_evidence_ref = fact.ref
        self.current_head = computed
        self._assert_consistency()

    @precondition(lambda self: self.has_original and not self.invalidated and self.generation_count < 6)
    @rule()
    def invalidate_current(self) -> None:
        assert self.current_head is not None
        assert self.last_evidence_ref is not None
        invalidation_fact = regime_invalidated_at(
            self.allocator, invalidated_fact_ref=self.last_evidence_ref, recorded_time=self.current_head.recorded_time
        )
        cursor = self._window_frontier(invalidation_fact.recorded_time)
        events = self.engine.on_regime_invalidated(invalidation_fact, cursor=cursor)
        assert len(events) == 1
        invalidated_event = only_invalidated(events[0])
        assert invalidated_event.invalidated_fact_ref == self.current_head.ref
        self.view.on_feature_invalidated(invalidated_event)
        self.history.append(invalidated_event)
        self.invalidated = True
        self._assert_consistency()

    @precondition(lambda self: self.has_original and self.invalidated)
    @rule(metric=_metric_strategy)
    def submit_replacement(self, metric: Decimal) -> None:
        assert self.current_head is not None
        offset = 10 * (self.generation_count + 1)
        fact = regime_classified_at(self.allocator, 0, computed_metric=str(metric), recorded_offset_seconds=offset)
        cursor = self._window_frontier(fact.recorded_time)
        events = self.engine.on_regime_classified(fact, cursor=cursor)
        assert len(events) == 1
        replacement = only_computed(events[0])
        assert replacement.supersedes_fact_ref == self.current_head.ref
        self.view.on_feature_computed(replacement)
        self.history.append(replacement)
        self.invalidated = False
        self.last_evidence_ref = fact.ref
        self.current_head = replacement
        self.generation_count += 1
        self._assert_consistency()

    def _assert_consistency(self) -> None:
        # Category A property 1/2/6: engine current lineage head correct, no fork,
        # no third view state.
        lineage = self.engine._lineage.get(self.window_key)  # noqa: SLF001
        assert lineage is not None
        assert self.current_head is not None
        result = self.view.current()
        assert result is not None
        assert result.view_state in ("VALID", "PENDING_CORRECTION")
        if self.invalidated:
            # Category A property 4: invalidated head becomes PENDING_CORRECTION.
            assert lineage.invalidated is True
            assert result.view_state == "PENDING_CORRECTION"
            assert result.value is None
            assert result.lineage_head_fact_ref is None
        else:
            # Category A property 5: replacement returns it to VALID.
            assert lineage.invalidated is False
            assert lineage.head_fact.ref == self.current_head.ref
            assert result.view_state == "VALID"
            assert result.value == self.current_head.value
            assert result.lineage_head_fact_ref == self.current_head.ref
        # Category C: unique current head, correct supersession chain, no head
        # superseded twice, no intermediate member skipped, recorded-time strictly
        # ordered, each member carries its OWN correct cursor/dependency evidence.
        computed_history = [event for event in self.history if isinstance(event, FeatureComputed)]
        for earlier, later in zip(computed_history, computed_history[1:], strict=False):
            assert later.supersedes_fact_ref == earlier.ref
        seen_superseded: set[EventRecordRef] = set()
        for event in computed_history:
            if event.supersedes_fact_ref is not None:
                assert event.supersedes_fact_ref not in seen_superseded
                seen_superseded.add(event.supersedes_fact_ref)
        for earlier_event, later_event in zip(self.history, self.history[1:], strict=False):
            assert later_event.recorded_time > earlier_event.recorded_time
        for history_event in self.history:
            # Chapter 8 §8.5.2 Cursor -> Fact: each member's OWN cursor, never
            # inherited/stale from a prior member.
            assert history_event.computation_cursor.recorded_time <= history_event.recorded_time
            assert (
                history_event.computation_dependency_content_evidence.input_contract_content_id
                == REGIME_INPUT_CONTRACT.input_contract_content_id
            )


TestRegimeLegalTransitionMachine = RegimeLegalTransitionMachine.TestCase
TestRegimeLegalTransitionMachine.settings = settings(
    max_examples=settings().max_examples, stateful_step_count=12, suppress_health_check=[HealthCheck.too_slow]
)


# =============================================================================
# CATEGORY B — illegal transitions fail closed with the real error types
# =============================================================================


def _fresh_regime_engine() -> RegimePassthroughFeatureEngine:
    allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="prop-b")
    return _regime_engine(allocator, FixedDeltaTimeSource())


def _original_regime(
    engine: RegimePassthroughFeatureEngine, metric: Decimal
) -> tuple[RegimeClassifiedFact, FeatureComputed]:
    allocator = engine._allocator  # noqa: SLF001
    fact = regime_classified_at(allocator, 0, computed_metric=str(metric))
    cursor = frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    computed = only_computed(engine.on_regime_classified(fact, cursor=cursor)[0])
    return fact, computed


@given(metric_1=_metric_strategy, metric_2=_metric_strategy)
def test_second_original_against_non_invalidated_lineage_fails_closed(metric_1: Decimal, metric_2: Decimal) -> None:
    """Illegal: a second ORIGINAL RegimeClassified against an existing
    non-invalidated lineage head.
    """
    engine = _fresh_regime_engine()
    allocator = engine._allocator  # noqa: SLF001
    _, original = _original_regime(engine, metric_1)
    key = (original.window_start, original.window_end)

    second_fact = regime_classified_at(allocator, 0, computed_metric=str(metric_2), recorded_offset_seconds=5)
    cursor = frontier_at(second_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    with pytest.raises(FeatureLineageError):
        engine.on_regime_classified(second_fact, cursor=cursor)

    assert engine._lineage[key].head_fact.ref == original.ref  # noqa: SLF001 -- unchanged
    assert engine._lineage[key].invalidated is False  # noqa: SLF001


@given(metric=_metric_strategy)
def test_double_invalidation_fails_closed(metric: Decimal) -> None:
    """Illegal: invalidating an already-invalidated (PENDING_CORRECTION) head."""
    engine = _fresh_regime_engine()
    allocator = engine._allocator  # noqa: SLF001
    original_fact, original = _original_regime(engine, metric)
    key = (original.window_start, original.window_end)

    inv_fact_1 = regime_invalidated_at(
        allocator, invalidated_fact_ref=original_fact.ref, recorded_time=original.recorded_time
    )
    cursor_1 = frontier_at(inv_fact_1.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    engine.on_regime_invalidated(inv_fact_1, cursor=cursor_1)
    pending_before = engine._lineage[key].pending_invalidation_ref  # noqa: SLF001

    inv_fact_2 = regime_invalidated_at(
        allocator, invalidated_fact_ref=original_fact.ref, recorded_time=inv_fact_1.recorded_time + timedelta(seconds=1)
    )
    cursor_2 = frontier_at(inv_fact_2.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    with pytest.raises(FeatureLineageError):
        engine.on_regime_invalidated(inv_fact_2, cursor=cursor_2)

    assert engine._lineage[key].invalidated is True  # noqa: SLF001 -- unchanged
    assert engine._lineage[key].pending_invalidation_ref == pending_before  # noqa: SLF001


@given(metric=_metric_strategy, bogus_sequence=st.integers(min_value=1000, max_value=999_999))
def test_stale_nonexistent_lineage_successor_invalidation_fails_closed(metric: Decimal, bogus_sequence: int) -> None:
    """Illegal: an invalidation targeting a ref that is not the current,
    non-invalidated evidence for any window ("stale/non-current successor").
    """
    engine = _fresh_regime_engine()
    allocator = engine._allocator  # noqa: SLF001
    original_fact, original = _original_regime(engine, metric)
    key = (original.window_start, original.window_end)

    bogus_ref = EventRecordRef(stream_id="raw-regime-engine-regime", sequence=bogus_sequence, event_id="bogus")
    inv_fact = regime_invalidated_at(allocator, invalidated_fact_ref=bogus_ref, recorded_time=original.recorded_time)
    cursor = frontier_at(inv_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    with pytest.raises(FeatureLineageError):
        engine.on_regime_invalidated(inv_fact, cursor=cursor)

    assert engine._lineage[key].head_fact.ref == original.ref  # noqa: SLF001
    assert engine._lineage[key].invalidated is False  # noqa: SLF001


@given(metric_1=_metric_strategy, metric_2=_metric_strategy, metric_3=_metric_strategy)
def test_fork_attempt_second_successor_of_same_prior_head_fails_closed(
    metric_1: Decimal, metric_2: Decimal, metric_3: Decimal
) -> None:
    """Illegal fork attempt: after ONE legal replacement wins a prior
    invalidated head, a SECOND candidate that also conceptually targets
    that SAME (now-superseded) prior head must never also become
    authoritative — it fails closed exactly like an unsolicited second
    original.
    """
    engine = _fresh_regime_engine()
    allocator = engine._allocator  # noqa: SLF001
    original_fact, original = _original_regime(engine, metric_1)
    key = (original.window_start, original.window_end)

    inv_fact = regime_invalidated_at(
        allocator, invalidated_fact_ref=original_fact.ref, recorded_time=original.recorded_time
    )
    cursor = frontier_at(inv_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    engine.on_regime_invalidated(inv_fact, cursor=cursor)

    winner_fact = regime_classified_at(allocator, 0, computed_metric=str(metric_2), recorded_offset_seconds=10)
    winner_cursor = frontier_at(winner_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    winner = only_computed(engine.on_regime_classified(winner_fact, cursor=winner_cursor)[0])
    assert winner.supersedes_fact_ref == original.ref

    # The "forking" second successor -- prepared independently, arriving after the
    # window has already resolved back to VALID under `winner`.
    loser_fact = regime_classified_at(allocator, 0, computed_metric=str(metric_3), recorded_offset_seconds=20)
    loser_cursor = frontier_at(loser_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    with pytest.raises(FeatureLineageError):
        engine.on_regime_classified(loser_fact, cursor=loser_cursor)

    # Never two canonical successors of the same prior head: the window still
    # resolves to exactly ONE current head (the winner), never the loser.
    assert engine._lineage[key].head_fact.ref == winner.ref  # noqa: SLF001
    assert engine._lineage[key].invalidated is False  # noqa: SLF001


@given(
    swing_definition_version=st.sampled_from(["swd-1", "swd-2"]),
    pivot_index=st.integers(min_value=0, max_value=20),
)
def test_swing_revision_skip_fails_closed(swing_definition_version: str, pivot_index: int) -> None:
    """Illegal transition on the Swing surface: a Swing revision that skips
    ahead (never revision 1 first, or a later revision without the required
    intervening invalidation) fails closed with the real Swing-specific
    error type.
    """
    assume(swing_definition_version == "swd-1")  # required by make_distance_definition's own default
    allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="prop-b-swing")
    engine = _swing_engine(allocator, FixedDeltaTimeSource())
    bad_first_swing = swing_confirmed_at(
        allocator, pivot_index=pivot_index, swing_id="skip-swing", swing_revision=2, swing_definition_version="swd-1"
    )
    cursor = frontier_at(bad_first_swing.recorded_time)
    with pytest.raises(InvalidSwingEligibilityInputError):
        engine.on_swing_confirmed(bad_first_swing, cursor=cursor)
    assert engine._swing_confirmations == {}  # noqa: SLF001 -- rejected attempt never entered state


@given(metric=_metric_strategy)
def test_foreign_scope_fails_closed(metric: Decimal) -> None:
    """Illegal: a fact whose scope does not match the engine's own bound
    scope (Feature scope is not global state, feature.md §16).
    """
    engine = _fresh_regime_engine()
    allocator = engine._allocator  # noqa: SLF001
    foreign_fact = regime_classified_at(
        allocator, 0, computed_metric=str(metric), instrument_id="NOT-THE-REAL-INSTRUMENT"
    )
    cursor = frontier_at(foreign_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    with pytest.raises(ForeignScopeError):
        engine.on_regime_classified(foreign_fact, cursor=cursor)
    assert engine._lineage == {}  # noqa: SLF001


# =============================================================================
# CATEGORY D — deterministic P_run (`p_run_sort`)
# =============================================================================


@st.composite
def _apply_sets(draw: st.DrawFn) -> list[UpstreamEnvelope]:
    num_streams = draw(st.integers(min_value=1, max_value=3))
    streams = [f"prop-stream-{i}" for i in range(num_streams)]
    num_events = draw(st.integers(min_value=1, max_value=8))
    per_stream_seq = dict.fromkeys(streams, 0)
    refs: list[EventRecordRef] = []
    envelopes: list[UpstreamEnvelope] = []
    for i in range(num_events):
        stream = draw(st.sampled_from(streams))
        per_stream_seq[stream] += 1
        ref = EventRecordRef(stream_id=stream, sequence=per_stream_seq[stream], event_id=f"e-{i}")
        causation = tuple(draw(st.lists(st.sampled_from(refs), max_size=2, unique=True))) if refs else ()
        envelopes.append(_mk_envelope(ref, causation_refs=causation, recorded_time=BASE))
        refs.append(ref)
    return envelopes


@st.composite
def _apply_set_with_permutation(draw: st.DrawFn) -> tuple[list[UpstreamEnvelope], list[UpstreamEnvelope]]:
    envelopes = draw(_apply_sets())
    order = draw(st.permutations(range(len(envelopes))))
    permuted = [envelopes[i] for i in order]
    return envelopes, permuted


@given(_apply_set_with_permutation())
def test_p_run_sort_permutation_invariant_preserves_hard_constraints(
    pair: tuple[list[UpstreamEnvelope], list[UpstreamEnvelope]],
) -> None:
    original, permuted = pair
    result_a = p_run_sort(original, merge_policy=_SUPPORTED_MERGE_POLICY)
    result_b = p_run_sort(permuted, merge_policy=_SUPPORTED_MERGE_POLICY)
    assert [e.ref for e in result_a] == [e.ref for e in result_b]

    # P_stream preserved: within each stream, ascending sequence order.
    positions_by_stream: dict[str, list[tuple[int, int]]] = {}
    for idx, envelope in enumerate(result_a):
        positions_by_stream.setdefault(envelope.ref.stream_id, []).append((envelope.ref.sequence, idx))
    for entries in positions_by_stream.values():
        ordered_by_position = [seq for seq, _ in sorted(entries, key=lambda item: item[1])]
        assert ordered_by_position == sorted(ordered_by_position)

    # P_causation preserved: an in-set causation ref always precedes its citer.
    position_of = {envelope.ref: idx for idx, envelope in enumerate(result_a)}
    for envelope in result_a:
        for cause_ref in envelope.causation_refs:
            if cause_ref in position_of:
                assert position_of[cause_ref] < position_of[envelope.ref]


@given(
    stream_a=st.text(alphabet="abcdefg", min_size=1, max_size=4).map(lambda s: f"tie-a-{s}"),
    stream_b=st.text(alphabet="abcdefg", min_size=1, max_size=4).map(lambda s: f"tie-b-{s}"),
    seq_a=st.integers(min_value=1, max_value=50),
    seq_b=st.integers(min_value=1, max_value=50),
)
def test_p_run_sort_tie_break_matches_stream_id_then_sequence_for_unrelated_events(
    stream_a: str, stream_b: str, seq_a: int, seq_b: int
) -> None:
    """The resolved Input Contract tie-break (`stream_id`, `sequence`) is
    used ONLY where events remain unordered by `P_stream`/`P_causation` —
    two single-event, causally-unrelated streams are exactly that case.
    """
    assume(stream_a != stream_b)
    ref_a = EventRecordRef(stream_id=stream_a, sequence=seq_a, event_id="a")
    ref_b = EventRecordRef(stream_id=stream_b, sequence=seq_b, event_id="b")
    envelope_a = _mk_envelope(ref_a)
    envelope_b = _mk_envelope(ref_b)
    # Arrival order deliberately reversed relative to the expected tie-break winner.
    ordered = p_run_sort([envelope_b, envelope_a], merge_policy=_SUPPORTED_MERGE_POLICY)
    expected_first = ref_a if (stream_a, seq_a) < (stream_b, seq_b) else ref_b
    assert ordered[0].ref == expected_first


@given(st.integers(min_value=1, max_value=50), st.data())
def test_p_run_sort_identical_duplicate_ref_dedups_deterministically(seq: int, data: st.DataObject) -> None:
    ref = _mk_ref("dup-stream", seq)
    envelope = _mk_envelope(ref, recorded_time=BASE)
    order = data.draw(st.sampled_from([(envelope, envelope), (envelope, envelope)]))
    ordered = p_run_sort(list(order), merge_policy=_SUPPORTED_MERGE_POLICY)
    assert [e.ref for e in ordered] == [ref]


@given(st.integers(min_value=1, max_value=50), st.booleans())
def test_p_run_sort_conflicting_duplicate_ref_fails_closed_both_orders(seq: int, reverse_order: bool) -> None:
    ref = _mk_ref("conflict-stream", seq)
    original = _mk_envelope(ref, recorded_time=BASE)
    conflicting = _mk_envelope(ref, recorded_time=BASE + timedelta(seconds=1))
    ordered_input = [conflicting, original] if reverse_order else [original, conflicting]
    with pytest.raises(ConflictingUpstreamEnvelopeError):
        p_run_sort(ordered_input, merge_policy=_SUPPORTED_MERGE_POLICY)


@given(st.integers(min_value=2, max_value=4))
def test_p_run_sort_cycle_fails_closed(cycle_length: int) -> None:
    refs = [_mk_ref(f"cycle-stream-{i}", 1) for i in range(cycle_length)]
    envelopes = [
        _mk_envelope(refs[i], causation_refs=(refs[(i - 1) % cycle_length],)) for i in range(cycle_length)
    ]
    with pytest.raises(NonMonotonicApplicationOrderError):
        p_run_sort(envelopes, merge_policy=_SUPPORTED_MERGE_POLICY)


@given(_apply_sets(), st.integers(min_value=1000, max_value=9999))
def test_p_run_sort_never_waits_for_a_future_unrelated_event(
    envelopes: list[UpstreamEnvelope], future_seq: int
) -> None:
    """Formal Case 2 (`-MAJ-07` corrected model): `B` (every envelope in the
    generated apply set) is in the CURRENT certified apply set; a `future`
    event `A` does NOT exist in that set at all, and `A`/`B` have NO
    `P_stream`/`P_causation` relationship whatsoever — `A`'s identity is
    used ONLY as a conceptual comparison value below, never placed into any
    envelope's `causation_refs`. This is deliberately distinct from
    `test_p_run_sort_never_waits_for_an_already_applied_out_of_set_cause`
    below (a genuinely different contract: a cause that DOES exist,
    already resolved, and IS legitimately named in `causation_refs`) — the
    two must never be conflated (`-MAJ-07`'s own root cause was exactly
    that conflation).

    `p_run_sort` must resolve the WHOLE apply set now, never waiting for —
    or even being aware of — this absent, unrelated future event.
    """
    future_unrelated_ref = _mk_ref("future-unrelated-stream", future_seq)
    for envelope in envelopes:
        assert future_unrelated_ref not in envelope.causation_refs
        assert envelope.ref != future_unrelated_ref

    result = p_run_sort(envelopes, merge_policy=_SUPPORTED_MERGE_POLICY)

    # B is resolved now: every member of the apply set appears, nothing is
    # deferred/missing waiting on the (never-referenced) future event.
    assert {e.ref for e in result} == {e.ref for e in envelopes}
    assert future_unrelated_ref not in {e.ref for e in result}
    # Deterministic, not merely "didn't raise": identical resolution on repeat.
    assert [e.ref for e in result] == [
        e.ref for e in p_run_sort(envelopes, merge_policy=_SUPPORTED_MERGE_POLICY)
    ]


def test_p_run_sort_never_waits_for_an_already_applied_out_of_set_cause() -> None:
    """Formal Case 2's distinct counterpart (`-MAJ-07` corrected model): here
    the out-of-set cause `C` genuinely EXISTS and has ALREADY been applied
    — demonstrated via a REAL `AuthoritativeSubjectOwner` commit through a
    real history provider/applied frontier, not merely asserted in a
    comment — and is therefore correctly excluded from the CURRENT,
    not-yet-applied apply set. `B.causation_refs` legitimately names `C` (a
    genuine `P_causation` edge), but because `C` already resolved outside
    this apply set, `p_run_sort` must still resolve `B` now, never waiting
    for `C` to (re)appear inside the bounded set being sorted.
    """
    authority = InMemorySubjectOwnershipAuthority()
    provider = InMemoryLineageHistoryProvider()
    time_source = FixedDeltaTimeSource()
    allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="prop-d-applied")
    engine = _regime_engine(allocator, time_source)
    subject_id = engine.scope.feature_subject_id
    provider.register_known_empty(subject_id)
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator, time_source=time_source)
    owner = AuthoritativeSubjectOwner(
        engine=engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )
    owner.acquire_and_activate(catch_up_frontier=frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT))

    already_applied_fact = regime_classified_at(allocator, 0, computed_metric="1.00")
    already_applied_frontier = frontier_at(
        already_applied_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT
    )
    provider.enqueue_pending(
        subject_id,
        [_regime_envelope(already_applied_fact, kind="regime_classified", frontier=already_applied_frontier)],
    )
    committed = owner.process_certified_frontier(already_applied_frontier)
    # `already_applied_ref` is now genuinely authoritative/applied -- proven by
    # the real commit above, not assumed.
    already_applied_ref = only_computed(committed[0]).ref

    b_ref = _mk_ref("already-applied-dependent-stream", 1)
    b_envelope = _mk_envelope(b_ref, causation_refs=(already_applied_ref,), recorded_time=BASE)

    result = p_run_sort([b_envelope], merge_policy=_SUPPORTED_MERGE_POLICY)
    assert [e.ref for e in result] == [b_ref]


# =============================================================================
# CATEGORY E — ADR-043 competing owners / transitions
# =============================================================================


def _empty_frontier() -> EvaluationFrontier:
    return frontier_at(BASE, resolved_input_contract=REGIME_INPUT_CONTRACT)


@given(original_metric=_metric_strategy)
def test_adr043_successor_generation_fences_stale_predecessor_and_sees_canonical_state(
    original_metric: Decimal,
) -> None:
    authority = InMemorySubjectOwnershipAuthority()
    provider = InMemoryLineageHistoryProvider()
    time_source = FixedDeltaTimeSource()

    allocator_0 = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="prop-e-gen0")
    engine_0 = _regime_engine(allocator_0, time_source)
    subject_id = engine_0.scope.feature_subject_id
    provider.register_known_empty(subject_id)
    committer_0 = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_0, time_source=time_source)
    owner_0 = AuthoritativeSubjectOwner(
        engine=engine_0,
        authority=authority,
        committer=committer_0,
        history_provider=provider,
    )
    owner_0.acquire_and_activate(catch_up_frontier=_empty_frontier())
    assert owner_0._handle is not None  # noqa: SLF001
    gen0_generation = owner_0._handle.ownership_generation  # noqa: SLF001

    # Property 1: exactly one generation is currently authoritative.
    assert authority.is_current(subject_id, gen0_generation) is True

    fact_1 = regime_classified_at(allocator_0, 0, computed_metric=str(original_metric))
    frontier_1 = frontier_at(fact_1.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    provider.enqueue_pending(subject_id, [_regime_envelope(fact_1, kind="regime_classified", frontier=frontier_1)])
    committed_1 = owner_0.process_certified_frontier(frontier_1)
    original_computed = only_computed(committed_1[0])

    # A candidate gen0 would still be entitled to commit while current -- prepared
    # now, attempted AFTER handoff below.
    invalidation_fact = regime_invalidated_at(
        allocator_0, invalidated_fact_ref=fact_1.ref, recorded_time=original_computed.recorded_time
    )
    stale_cursor = frontier_at(invalidation_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    stale_prepared = engine_0.prepare_regime_invalidated(invalidation_fact, cursor=stale_cursor)
    log_length_before = len(committer_0.log.get(subject_id, []))
    sequences_before = dict(allocator_0._sequences)  # noqa: SLF001

    owner_0.revoke()
    assert owner_0.is_terminal is True

    provider.register_upstream(subject_id, [_regime_envelope(fact_1, kind="regime_classified", frontier=frontier_1)])
    provider.register_canonical(subject_id, [original_computed])

    allocator_1 = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="prop-e-gen1")
    engine_1 = _regime_engine(allocator_1, time_source)
    committer_1 = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_1, time_source=time_source)
    owner_1 = AuthoritativeSubjectOwner(
        engine=engine_1,
        authority=authority,
        committer=committer_1,
        history_provider=provider,
    )
    reconciled = owner_1.acquire_and_activate(catch_up_frontier=frontier_1)
    assert owner_1._handle is not None  # noqa: SLF001
    gen1_generation = owner_1._handle.ownership_generation  # noqa: SLF001

    # Successor strictly increases; predecessor no longer current (properties 1/6).
    assert gen1_generation > gen0_generation
    assert authority.is_current(subject_id, gen0_generation) is False
    assert authority.is_current(subject_id, gen1_generation) is True

    # Property 5: successor sees canonical state through catch-up.
    assert reconciled == (original_computed,)
    key = (fact_1.window_start, fact_1.window_end)
    assert engine_1._lineage[key].head_fact.ref == original_computed.ref  # noqa: SLF001

    # Properties 2/3/4: stale generation cannot commit; zero authoritative-append
    # effect; no sequence consumed in the fake commit authority.
    with pytest.raises(StaleOwnershipGenerationError):
        committer_0.commit(
            feature_subject_id=subject_id,
            ownership_generation=gen0_generation,
            stream_id=engine_0.resolved_output_event_contract_authority.authoritative_stream_id,
            prepared=stale_prepared,
        )
    assert len(committer_0.log.get(subject_id, [])) == log_length_before
    assert dict(allocator_0._sequences) == sequences_before  # noqa: SLF001


@given(st.just(None))
def test_adr043_two_racing_successor_acquisitions_only_the_later_one_wins(_: None) -> None:
    """Property 6: two conflicting successor candidates can never both
    become authoritative for the same subject — the authority's own
    revoke-before-successor guarantee fences the earlier one immediately.
    """
    authority = InMemorySubjectOwnershipAuthority()
    provider = InMemoryLineageHistoryProvider()
    time_source = FixedDeltaTimeSource()
    allocator_0 = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="race-gen0")
    engine_0 = _regime_engine(allocator_0, time_source)
    subject_id = engine_0.scope.feature_subject_id
    provider.register_known_empty(subject_id)
    committer_0 = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_0, time_source=time_source)
    owner_0 = AuthoritativeSubjectOwner(
        engine=engine_0,
        authority=authority,
        committer=committer_0,
        history_provider=provider,
    )
    owner_0.acquire_and_activate(catch_up_frontier=_empty_frontier())
    owner_0.revoke()

    generation_a = authority.acquire(subject_id)
    generation_b = authority.acquire(subject_id)
    assert generation_b > generation_a
    assert authority.is_current(subject_id, generation_a) is False
    assert authority.is_current(subject_id, generation_b) is True


@given(metric_x=_metric_strategy, metric_y=_metric_strategy)
def test_adr043_different_subjects_remain_fully_independent(metric_x: Decimal, metric_y: Decimal) -> None:
    """Property 7: ownership/commit activity for one `feature_subject_id`
    never affects another, even sharing the SAME authority/provider.
    """
    authority = InMemorySubjectOwnershipAuthority()
    provider = InMemoryLineageHistoryProvider()
    time_source = FixedDeltaTimeSource()

    allocator_x = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="subj-x")
    engine_x = RegimePassthroughFeatureEngine(
        feature_scope("volatility_metric", version="fd-regime-1", instrument_id="SUBJECT-X"),
        make_regime_definition(regime_dimension_version="rgd-1"),
        allocator_x,
        time_source,
        output_event_contract_authority_provider=StaticOutputEventContractAuthorityProvider(OUTPUT_EVENT_CONTRACT_AUTHORITY),
        input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
    )
    allocator_y = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="subj-y")
    engine_y = RegimePassthroughFeatureEngine(
        feature_scope("volatility_metric", version="fd-regime-1", instrument_id="SUBJECT-Y"),
        make_regime_definition(regime_dimension_version="rgd-1"),
        allocator_y,
        time_source,
        output_event_contract_authority_provider=StaticOutputEventContractAuthorityProvider(OUTPUT_EVENT_CONTRACT_AUTHORITY),
        input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
    )
    subject_x = engine_x.scope.feature_subject_id
    subject_y = engine_y.scope.feature_subject_id
    assert subject_x != subject_y

    provider.register_known_empty(subject_x)
    provider.register_known_empty(subject_y)
    committer_x = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_x, time_source=time_source)
    committer_y = InMemoryFencedFeatureCommitter(authority=authority, allocator=allocator_y, time_source=time_source)
    owner_x = AuthoritativeSubjectOwner(
        engine=engine_x,
        authority=authority,
        committer=committer_x,
        history_provider=provider,
    )
    owner_y = AuthoritativeSubjectOwner(
        engine=engine_y,
        authority=authority,
        committer=committer_y,
        history_provider=provider,
    )
    owner_x.acquire_and_activate(catch_up_frontier=_empty_frontier())
    owner_y.acquire_and_activate(catch_up_frontier=_empty_frontier())

    fact_x = regime_classified_at(allocator_x, 0, computed_metric=str(metric_x), instrument_id="SUBJECT-X")
    frontier_x = frontier_at(fact_x.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    provider.enqueue_pending(subject_x, [_regime_envelope(fact_x, kind="regime_classified", frontier=frontier_x)])
    owner_x.process_certified_frontier(frontier_x)

    # subject_y's owner is untouched: never activated by subject_x's own work, and
    # revoking subject_x's owner must not affect subject_y's own generation/state.
    assert owner_y.state.name == "ACTIVE"
    assert committer_y.log.get(subject_y, []) == []
    owner_x.revoke()
    assert owner_y.is_terminal is False
    assert owner_y.state.name == "ACTIVE"

    fact_y = regime_classified_at(allocator_y, 0, computed_metric=str(metric_y), instrument_id="SUBJECT-Y")
    frontier_y = frontier_at(fact_y.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    provider.enqueue_pending(subject_y, [_regime_envelope(fact_y, kind="regime_classified", frontier=frontier_y)])
    committed_y = owner_y.process_certified_frontier(frontier_y)
    assert len(committed_y) == 1
    assert committer_x.log.get(subject_x, [])  # subject_x's own prior commit remains, unaffected


# =============================================================================
# CATEGORY F — Replay/catch-up reconstruction
# =============================================================================


@given(
    metrics=st.lists(_metric_strategy, min_size=1, max_size=4),
    ends_pending=st.booleans(),
)
def test_regime_catch_up_reconstruction_matches_reference_history(metrics: list[Decimal], ends_pending: bool) -> None:
    """`-MAJ-06` corrected oracle: the reference side is a REAL `live`
    `FeatureCurrentView` maintained CONTEMPORANEOUSLY with reference
    generation (updated immediately after each engine emission, exactly
    as a real live consumer would) — never folded from the persisted
    event list after the fact. The replay side is a SEPARATE
    `FeatureCurrentView`, rebuilt AFTERWARD purely from the persisted
    `canonical_events` obtained via catch-up. The two sides are therefore
    structurally independent: `reference_live_view` never sees
    `canonical_events` at all, and `replay_view` never sees live engine
    emissions directly — only the fresh engine's own catch-up-reconciled
    persisted history.
    """
    reference_allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="ref-f")
    reference_time_source = FixedDeltaTimeSource()
    reference_engine = _regime_engine(reference_allocator, reference_time_source)
    subject_id = reference_engine.scope.feature_subject_id
    scope = reference_engine.scope
    reference_live_view = FeatureCurrentView(scope)

    upstream_envelopes: list[UpstreamEnvelope] = []
    canonical_events: list[FeatureComputed | FeatureFactInvalidated] = []

    fact = regime_classified_at(reference_allocator, 0, computed_metric=str(metrics[0]))
    frontier = frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
    computed = only_computed(reference_engine.on_regime_classified(fact, cursor=frontier)[0])
    reference_live_view.on_feature_computed(computed)  # applied immediately, live-side
    upstream_envelopes.append(_regime_envelope(fact, kind="regime_classified", frontier=frontier))
    canonical_events.append(computed)
    last_ref, last_computed, last_frontier = fact.ref, computed, frontier

    for index, metric in enumerate(metrics[1:], start=1):
        inv_fact = regime_invalidated_at(
            reference_allocator, invalidated_fact_ref=last_ref, recorded_time=last_computed.recorded_time
        )
        inv_frontier = frontier_at(inv_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
        invalidated = only_invalidated(reference_engine.on_regime_invalidated(inv_fact, cursor=inv_frontier)[0])
        reference_live_view.on_feature_invalidated(invalidated)  # applied immediately, live-side
        upstream_envelopes.append(_regime_envelope(inv_fact, kind="regime_invalidated", frontier=inv_frontier))
        canonical_events.append(invalidated)
        last_frontier = inv_frontier

        fact = regime_classified_at(
            reference_allocator, 0, computed_metric=str(metric), recorded_offset_seconds=10 * index
        )
        frontier = frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
        computed = only_computed(reference_engine.on_regime_classified(fact, cursor=frontier)[0])
        reference_live_view.on_feature_computed(computed)  # applied immediately, live-side
        upstream_envelopes.append(_regime_envelope(fact, kind="regime_classified", frontier=frontier))
        canonical_events.append(computed)
        last_ref, last_computed, last_frontier = fact.ref, computed, frontier

    if ends_pending:
        inv_fact = regime_invalidated_at(
            reference_allocator, invalidated_fact_ref=last_ref, recorded_time=last_computed.recorded_time
        )
        inv_frontier = frontier_at(inv_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
        invalidated = only_invalidated(reference_engine.on_regime_invalidated(inv_fact, cursor=inv_frontier)[0])
        reference_live_view.on_feature_invalidated(invalidated)  # applied immediately, live-side
        upstream_envelopes.append(_regime_envelope(inv_fact, kind="regime_invalidated", frontier=inv_frontier))
        canonical_events.append(invalidated)
        last_frontier = inv_frontier

    # Captured ONLY after live generation is fully complete -- the live
    # reference side is now frozen and will not be touched again.
    reference_live_result = reference_live_view.current()

    provider = InMemoryLineageHistoryProvider()
    provider.register_upstream(subject_id, upstream_envelopes)
    provider.register_canonical(subject_id, canonical_events)

    fresh_allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="fresh-f")
    raising_time_source = RaisingRecordedTimeSource()
    fresh_engine = _regime_engine(fresh_allocator, raising_time_source)
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(
        authority=authority,
        allocator=fresh_allocator,
        time_source=raising_time_source,
    )
    owner = AuthoritativeSubjectOwner(
        engine=fresh_engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )

    reconciled = owner.acquire_and_activate(catch_up_frontier=last_frontier)

    # Final canonical lineage head ref identical; no new refs; no live clock;
    # canonical historical recorded_time preserved.
    assert reconciled == tuple(canonical_events)
    assert fresh_allocator._sequences == {}  # noqa: SLF001
    key = (fact.window_start, fact.window_end)
    lineage = fresh_engine._lineage[key]  # noqa: SLF001
    if ends_pending:
        assert lineage.invalidated is True
        assert lineage.pending_invalidation_ref == canonical_events[-1].ref
        assert lineage.pending_invalidation_recorded_time == canonical_events[-1].recorded_time
    else:
        assert lineage.invalidated is False
        assert lineage.head_fact.ref == last_computed.ref
        assert lineage.head_fact.recorded_time == last_computed.recorded_time

    # Replay side: rebuilt AFTERWARD, purely from the persisted
    # `canonical_events` list -- structurally independent of the live
    # reference side above, which was updated during/immediately after
    # generation and never touches `canonical_events` at all.
    replay_view = FeatureCurrentView(scope)
    for event in canonical_events:
        if isinstance(event, FeatureComputed):
            replay_view.on_feature_computed(event)
        else:
            replay_view.on_feature_invalidated(event)
    assert replay_view.current() == reference_live_result


@given(
    swing_a_pivot=st.integers(min_value=0, max_value=3),
    swing_b_pivot=st.integers(min_value=5, max_value=8),
)
def test_swing_catch_up_reconstructs_non_selected_swing_evidence(swing_a_pivot: int, swing_b_pivot: int) -> None:
    """Category F, Swing variant: a Swing confirmation that never wins the
    total order for any window leaves no trace in Feature's own canonical
    output, yet catch-up must still reconstruct it from certified upstream
    replay so a LATER live operation that depends on it (falling back to it
    once the winner is invalidated) matches the reference engine.
    """
    assume(swing_a_pivot != swing_b_pivot)
    reference_allocator = SequenceAllocator(
        module_id="feature-engine",
        implementation_version="0.1.0",
        run_id="ref-f-swing",
    )
    time_source = FixedDeltaTimeSource()
    reference_engine = _swing_engine(reference_allocator, time_source)
    subject_id = reference_engine.scope.feature_subject_id

    swing_a = swing_confirmed_at(reference_allocator, pivot_index=swing_a_pivot, swing_id="prop-swing-a")
    frontier_a = frontier_at(swing_a.recorded_time)
    reference_engine.on_swing_confirmed(swing_a, cursor=frontier_a)

    swing_b = swing_confirmed_at(
        reference_allocator, pivot_index=swing_b_pivot, swing_id="prop-swing-b", recorded_offset_minutes=1
    )
    frontier_b = frontier_at(swing_b.recorded_time)
    reference_engine.on_swing_confirmed(swing_b, cursor=frontier_b)

    candle = candle_at(reference_allocator, 10, high="110", low="90")
    frontier_candle = frontier_at(candle.recorded_time)
    computed = only_computed(reference_engine.on_candle(candle, cursor=frontier_candle)[0])
    key = (candle.scope.window_start, candle.scope.window_end)
    winning_swing_id = "prop-swing-b" if swing_b_pivot > swing_a_pivot else "prop-swing-a"
    assert reference_engine._lineage[key].used_swing_id == winning_swing_id  # noqa: SLF001

    invalidate_winner = swing_invalidated_at(
        reference_allocator, swing_id=winning_swing_id, swing_revision=1, recorded_time=computed.recorded_time
    )
    frontier_inv = frontier_at(invalidate_winner.recorded_time)
    reference_events = reference_engine.on_swing_invalidated(invalidate_winner, cursor=frontier_inv)
    losing_swing_id = "prop-swing-a" if winning_swing_id == "prop-swing-b" else "prop-swing-b"
    assert reference_engine._lineage[key].used_swing_id == losing_swing_id  # noqa: SLF001
    reference_replacement = only_computed(reference_events[1])

    provider = InMemoryLineageHistoryProvider()
    provider.register_upstream(
        subject_id,
        [
            _swing_envelope(swing_a, kind="swing_confirmed", frontier=frontier_a),
            _swing_envelope(swing_b, kind="swing_confirmed", frontier=frontier_b),
            _swing_envelope(candle, kind="candle", frontier=frontier_candle, causation_refs=(swing_a.ref, swing_b.ref)),
        ],
    )
    provider.register_canonical(subject_id, [computed])

    fresh_allocator = SequenceAllocator(
        module_id="feature-engine",
        implementation_version="0.1.0",
        run_id="fresh-f-swing",
    )
    fresh_engine = _swing_engine(fresh_allocator, time_source)
    authority = InMemorySubjectOwnershipAuthority()
    committer = InMemoryFencedFeatureCommitter(authority=authority, allocator=fresh_allocator, time_source=time_source)
    owner = AuthoritativeSubjectOwner(
        engine=fresh_engine,
        authority=authority,
        committer=committer,
        history_provider=provider,
    )
    reconciled = owner.acquire_and_activate(catch_up_frontier=frontier_candle)
    assert reconciled == (computed,)
    assert fresh_allocator._sequences == {}  # noqa: SLF001

    invalidation_envelope = _swing_envelope(invalidate_winner, kind="swing_invalidated", frontier=frontier_inv)
    provider.enqueue_pending(subject_id, [invalidation_envelope])
    live_events = owner.process_certified_frontier(frontier_inv)
    assert len(live_events) == 2
    live_replacement = only_computed(live_events[1])
    assert live_replacement.value == reference_replacement.value
    assert fresh_engine._lineage[key].used_swing_id == losing_swing_id  # noqa: SLF001
