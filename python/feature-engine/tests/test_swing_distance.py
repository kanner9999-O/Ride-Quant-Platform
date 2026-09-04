from __future__ import annotations

import dataclasses
import inspect
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

import pytest
from conftest import (
    BASE,
    CANDLE_STREAM_ID,
    CONTRACT_VERSION,
    FEATURE_OUTPUT_CONTRACT_VERSION,
    SWING_DISTANCE_INPUT_CONTRACT,
    SWING_STREAM_ID,
    FixedDeltaTimeSource,
    NonCausalTimeSource,
    authorized_candle_contract_refs,
    authorized_swing_contract_refs,
    candle_at,
    feature_scope,
    frontier_at,
    make_candle_definition,
    make_distance_definition,
    only_computed,
    only_invalidated,
    swing_confirmed_at,
    swing_invalidated_at,
)

from feature_engine import (
    CANDLE_CORRECTED_CONTRACT_ID,
    FEATURE_COMPUTED_CONTRACT_ID,
    FEATURE_FACT_INVALIDATED_CONTRACT_ID,
    ComputationCursor,
    EvaluationFrontier,
    EventContractRef,
    InputContractAuthorityProvider,
    InputContractRef,
    LifecycleFrontier,
    LifecycleFrontierProof,
    LifecyclePosition,
    RecordedTimeSource,
    SequenceAllocator,
    StaticInputContractAuthorityProvider,
    StreamPositionProof,
    SwingDistanceFeatureEngine,
)
from feature_engine.contracts import ResolvedInputContract, VerifiedInputContractAuthority, _seal_verified_authority
from feature_engine.errors import (
    CursorRelationalInvariantViolationError,
    DuplicateCandleConflictError,
    EligibleSwingComputationDefectError,
    EvidenceReferenceConflictError,
    ForeignScopeError,
    InputContractIdentityMismatchError,
    InvalidFeatureDefinitionError,
    InvalidSwingEligibilityInputError,
    NonMonotonicRecordedTimeError,
    OutOfOrderCandleError,
    OutOfOrderCorrectionError,
    RecordedTimeSourceViolationError,
    RegistryContractMismatchError,
    StreamPositionsUniverseMismatchError,
    UnauthorizedUpstreamContractError,
    UnresolvedComputationCursorAuthorityError,
    UnsupportedDistanceRepresentationError,
)


@dataclasses.dataclass(frozen=True)
class _FixedAuthorityProvider:
    """TEST-ONLY `InputContractAuthorityProvider` that returns WHATEVER
    object it was constructed with, verbatim, regardless of type — used to
    prove that a genuine computation engine independently rejects a
    provider that hands back unresolved/plain data instead of a real
    `VerifiedInputContractAuthority` (Review-A round-4).
    """

    authority: object

    def resolve(self, profile: object) -> Any:
        return self.authority


def _engine(
    allocator: SequenceAllocator,
    time_source: RecordedTimeSource,
    *,
    input_contract_authority_provider: InputContractAuthorityProvider | None = None,
    **definition_kwargs: Any,
) -> SwingDistanceFeatureEngine:
    definition = make_distance_definition(**definition_kwargs)
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
        feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
        authorized_candle_contract_refs=authorized_candle_contract_refs(),
        authorized_swing_contract_refs=authorized_swing_contract_refs(),
        input_contract_authority_provider=provider,
    )


def _invalid_frontier(recorded_time: datetime) -> EvaluationFrontier:
    """A deliberately malformed `EvaluationFrontier` (wrong `stream_registry_
    version`, mismatched against this engine's own bound authority) — used
    throughout the Review-A round-2 residual 2 failure-atomicity tests to
    prove that rejecting a frontier never mutates engine state. Built by
    mutating a VALID frontier's own plain `stream_registry_version` field
    directly — never by mutating `SWING_DISTANCE_INPUT_CONTRACT` itself,
    which (as a `VerifiedInputContractAuthority`) has no public constructor
    at all, so `dataclasses.replace` on it always raises `TypeError`
    (Review-A round-5).
    """
    return dataclasses.replace(frontier_at(recorded_time), stream_registry_version="not-the-real-registry-version")


# --- 7. Swing effective cutoff ------------------------------------------------


def test_pivot_before_window_end_eligible(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    engine.on_swing_confirmed(
        swing_confirmed_at(allocator, pivot_index=8, swing_id="s1", pivot_price="100"),
        cursor=frontier_at(BASE + timedelta(days=1)),
    )
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    events = engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))
    assert len(events) == 1
    assert only_computed(events[0]).value == Decimal("5.00")  # 105 - 100


def test_pivot_exactly_equal_window_end_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=11, swing_id="s1")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    assert engine.on_candle(reference, cursor=frontier_at(reference.recorded_time)) == []


def test_pivot_after_window_end_rejected(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=12, swing_id="s1")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    assert engine.on_candle(reference, cursor=frontier_at(reference.recorded_time)) == []


# --- 8. Recorded-time / effective-time independence --------------------------


def test_late_recorded_old_effective_swing_still_eligible(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    # pivot at index 2 (well before cutoff), but recorded very late relative to its own effective time
    # (still comfortably before the reference candle's own recorded_time / computation cursor).
    late_recorded = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", recorded_offset_minutes=100)
    engine.on_swing_confirmed(late_recorded, cursor=frontier_at(late_recorded.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105", recorded_offset_seconds=5700)
    events = engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))
    assert len(events) == 1


# --- P3-FEATURE-A-MAJ-06 remediation: explicit machine-enforced cursor -------


def test_swing_recorded_after_computation_cursor_excluded(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Effective-time eligible (pivot well before window_end), but the Swing's own
    recorded_time is AFTER the explicit computation cursor `R` supplied to
    `on_candle` — must be excluded, never selected just because it happens to
    already be sitting in the engine's in-memory state.
    """
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    not_yet_visible = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", recorded_offset_minutes=10_000)
    assert not_yet_visible.recorded_time > reference.recorded_time
    engine.on_swing_confirmed(not_yet_visible, cursor=frontier_at(not_yet_visible.recorded_time))
    assert engine.on_candle(reference, cursor=frontier_at(reference.recorded_time)) == []


def test_early_visible_future_effective_swing_remains_ineligible(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    # pivot AFTER the reference candle's own window_end (future-effective), even though it is
    # "visible" (ingested) before the candle is processed.
    future_effective = swing_confirmed_at(allocator, pivot_index=15, swing_id="s1")
    engine.on_swing_confirmed(future_effective, cursor=frontier_at(future_effective.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    assert engine.on_candle(reference, cursor=frontier_at(reference.recorded_time)) == []


def test_explicit_cursor_independent_of_candle_and_swing_recorded_time() -> None:
    """The exact scenario P3-FEATURE-A-MAJ-06 requires: a reference Candle
    recorded at R10, a Swing recorded at R20, evaluated as-of an explicit R —
    proving the engine never implicitly substitutes `R = candle.recorded_time`
    or `R = triggering_event.recorded_time`. Two engine instances ingest
    byte-for-byte identical facts (same Candle recorded_time R10, same Swing
    recorded_time R20) — the ONLY thing that differs between them is the
    explicit `cursor` passed to `on_candle`, and that alone flips the result.
    """
    r10 = BASE + timedelta(minutes=20)
    r20 = BASE + timedelta(minutes=30)
    r100 = BASE + timedelta(minutes=200)

    def _build() -> tuple[SwingDistanceFeatureEngine, SequenceAllocator]:
        alloc = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="cursor-run")
        return _engine(alloc, FixedDeltaTimeSource()), alloc

    engine_before, alloc_before = _build()
    engine_after, alloc_after = _build()

    swing_before = dataclasses.replace(
        swing_confirmed_at(alloc_before, pivot_index=2, swing_id="s1", pivot_price="100"), recorded_time=r20
    )
    swing_after = dataclasses.replace(
        swing_confirmed_at(alloc_after, pivot_index=2, swing_id="s1", pivot_price="100"), recorded_time=r20
    )
    engine_before.on_swing_confirmed(swing_before, cursor=frontier_at(r20))
    engine_after.on_swing_confirmed(swing_after, cursor=frontier_at(r20))

    reference_before = dataclasses.replace(
        candle_at(alloc_before, 10, high="110", low="90", close="105"), recorded_time=r10
    )
    reference_after = dataclasses.replace(
        candle_at(alloc_after, 10, high="110", low="90", close="105"), recorded_time=r10
    )

    # SAME Candle recorded_time (R10) on both engines — only the explicit cursor differs.
    excluded = engine_before.on_candle(reference_before, cursor=frontier_at(r10))
    assert excluded == []  # cursor R10 < Swing's recorded_time R20 -> excluded

    included = engine_after.on_candle(reference_after, cursor=frontier_at(r100))
    assert len(included) == 1  # cursor R100 >= Swing's recorded_time R20 -> eligible
    assert only_computed(included[0]).value == Decimal("5.00")


# --- 9. Eligible Swing revision -----------------------------------------------


def test_latest_valid_revision_selected(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    s1 = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=1, pivot_price="100")
    engine.on_swing_confirmed(s1, cursor=frontier_at(s1.recorded_time))
    inv = swing_invalidated_at(allocator, swing_id="s1", swing_revision=1, recorded_time=BASE + timedelta(minutes=4))
    engine.on_swing_invalidated(inv, cursor=frontier_at(inv.recorded_time))
    s2 = swing_confirmed_at(
        allocator, pivot_index=2, swing_id="s1", swing_revision=2, pivot_price="102", recorded_offset_minutes=5
    )
    engine.on_swing_confirmed(s2, cursor=frontier_at(s2.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    computed = only_computed(engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])
    assert computed.value == Decimal("3.00")  # 105 - 102 (revision 2's price), not 105-100


def test_invalidated_revision_excluded(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    invalidated_at = BASE + timedelta(minutes=3)
    inv = swing_invalidated_at(allocator, swing_id="s1", swing_revision=1, recorded_time=invalidated_at)
    engine.on_swing_invalidated(inv, cursor=frontier_at(invalidated_at))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    assert engine.on_candle(reference, cursor=frontier_at(reference.recorded_time)) == []


# --- 10. Total-order deterministic tie-break ----------------------------------


def test_total_order_prefers_latest_pivot_window_start(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    old = swing_confirmed_at(allocator, pivot_index=2, swing_id="s_old", pivot_price="90")
    engine.on_swing_confirmed(old, cursor=frontier_at(old.recorded_time))
    new = swing_confirmed_at(allocator, pivot_index=5, swing_id="s_new", pivot_price="95")
    engine.on_swing_confirmed(new, cursor=frontier_at(new.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    computed = only_computed(engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])
    # criterion 1 (pivot_effective_time.window_start DESC) picks s_new (index 5 > index 2).
    assert computed.value == Decimal("10.00")  # 105 - 95


# --- 11. Distance arithmetic ---------------------------------------------------


# --- P3-FEATURE-A-MAJ-01 remediation: signed fails closed, absolute unaffected


def test_signed_distance_representation_fails_closed_at_construction(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    with pytest.raises(UnsupportedDistanceRepresentationError):
        _engine(allocator, time_source, distance_representation="signed")


def test_absolute_distance_computed_with_evidence_refs(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    # P3-PY-MUT-STEP9-A field-completeness remediation (EVID-03,
    # constructed_object_field_not_independently_asserted): every
    # constructor-set field of `_emit_original`'s returned `FeatureComputed`
    # is now independently asserted against its authoritative expected
    # value, not just `.value`/`.input_fact_refs` as before.
    absolute_engine = _engine(allocator, time_source, distance_representation="absolute")
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="110")
    absolute_engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    computed = only_computed(absolute_engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])
    assert computed.value == Decimal("5.00")  # |105 - 110|
    assert set(computed.input_fact_refs) == {reference.ref, swing.ref}
    assert computed.scope == absolute_engine.scope
    assert computed.unit == absolute_engine.definition.unit
    assert computed.causation_refs == computed.input_fact_refs
    assert computed.ref.stream_id == "feature"
    assert computed.event_contract_ref == EventContractRef(
        FEATURE_COMPUTED_CONTRACT_ID, FEATURE_OUTPUT_CONTRACT_VERSION
    )


def test_no_eligible_swing_is_valid_absence(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    assert engine.on_candle(reference, cursor=frontier_at(reference.recorded_time)) == []


# --- P3-FEATURE-A-MAJ-04 remediation: revision N+1 requires explicit invalidation of N


def test_revision_two_before_invalidation_of_revision_one_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    s1 = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=1)
    engine.on_swing_confirmed(s1, cursor=frontier_at(s1.recorded_time))
    s2 = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=2, recorded_offset_minutes=5)
    with pytest.raises(InvalidSwingEligibilityInputError):
        engine.on_swing_confirmed(s2, cursor=frontier_at(s2.recorded_time))


def test_revision_skip_after_invalidation_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    s1 = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=1)
    engine.on_swing_confirmed(s1, cursor=frontier_at(s1.recorded_time))
    inv = swing_invalidated_at(allocator, swing_id="s1", swing_revision=1, recorded_time=BASE + timedelta(minutes=4))
    engine.on_swing_invalidated(inv, cursor=frontier_at(inv.recorded_time))
    s3 = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=3, recorded_offset_minutes=5)
    with pytest.raises(InvalidSwingEligibilityInputError):
        engine.on_swing_confirmed(s3, cursor=frontier_at(s3.recorded_time))


def test_first_seen_revision_must_be_one(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    bad = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=2)
    with pytest.raises(InvalidSwingEligibilityInputError):
        engine.on_swing_confirmed(bad, cursor=frontier_at(bad.recorded_time))


def test_pending_window_resolved_by_newly_visible_replacement_revision(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """A window left PENDING_CORRECTION (no eligible Swing existed right after
    invalidation) must be re-evaluated and resolved once a replacement revision
    later becomes visible via `on_swing_confirmed` — not only via
    `on_swing_invalidated`'s own immediate reattempt.
    """
    engine = _engine(allocator, time_source)
    s1 = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=1, pivot_price="100")
    engine.on_swing_confirmed(s1, cursor=frontier_at(s1.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    original = only_computed(engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])
    assert original.value == Decimal("5.00")

    inv = swing_invalidated_at(allocator, swing_id="s1", swing_revision=1, recorded_time=BASE + timedelta(minutes=20))
    invalidation_events = engine.on_swing_invalidated(inv, cursor=frontier_at(inv.recorded_time))
    assert len(invalidation_events) == 1  # invalidation only — no other eligible Swing exists yet

    s2 = swing_confirmed_at(
        allocator, pivot_index=2, swing_id="s1", swing_revision=2, pivot_price="102", recorded_offset_minutes=25
    )
    replacement_events = engine.on_swing_confirmed(s2, cursor=frontier_at(s2.recorded_time))
    assert len(replacement_events) == 1
    replacement = only_computed(replacement_events[0])
    assert replacement.value == Decimal("3.00")  # 105 - 102
    assert replacement.supersedes_fact_ref == original.ref
    assert replacement.window_start == original.window_start
    assert replacement.window_end == original.window_end


def test_settled_valid_window_preempted_by_higher_priority_corrected_revision(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """The exact A -> invalidate -> B(temporary) -> A(N+1)-wins regression
    P3-FEATURE-A-MAJ-04 requires: swing A (pivot index 8) is used first, gets
    invalidated, a lower-priority alternate swing B (pivot index 2) becomes
    the temporary winner and the window settles VALID using B — then A's
    corrected revision 2 (SAME pivot_effective_time as revision 1, since
    swing.md invariance holds across revisions) becomes visible and, because
    it wins the total order over B (later pivot_effective_time.window_start),
    the window must be invalidated AGAIN and replaced with A(rev2) — even
    though it was already VALID (not PENDING_CORRECTION) using B.
    """
    engine = _engine(allocator, time_source)

    swing_a1 = swing_confirmed_at(allocator, pivot_index=8, swing_id="A", swing_revision=1, pivot_price="100")
    engine.on_swing_confirmed(swing_a1, cursor=frontier_at(swing_a1.recorded_time))
    # recorded_offset_minutes=10 keeps swing-stream recorded_time monotonic (>= A's 9min) while
    # staying invisible (recorded_time=13min > 11min) at the cursor used for the ORIGINAL
    # computation below — B only needs to become visible once A is invalidated (cursor=20min).
    swing_b = swing_confirmed_at(
        allocator, pivot_index=2, swing_id="B", swing_revision=1, pivot_price="80", recorded_offset_minutes=10
    )
    engine.on_swing_confirmed(swing_b, cursor=frontier_at(swing_b.recorded_time))

    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    original = only_computed(engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])
    assert original.value == Decimal("5.00")  # 105 - 100 (A wins: later pivot index than B)

    # Invalidate A(rev1) — B (still eligible, lower priority) becomes the temporary winner.
    inv_a1 = swing_invalidated_at(allocator, swing_id="A", swing_revision=1, recorded_time=BASE + timedelta(minutes=20))
    temp_events = engine.on_swing_invalidated(inv_a1, cursor=frontier_at(inv_a1.recorded_time))
    assert len(temp_events) == 2  # invalidation of A-based fact + B-based replacement
    only_invalidated(temp_events[0])
    temporary = only_computed(temp_events[1])
    assert temporary.value == Decimal("25.00")  # 105 - 80 (now using B)
    assert temporary.supersedes_fact_ref == original.ref

    # A's corrected revision 2 arrives (same pivot_effective_time, invariant across revisions,
    # swing.md §1) — it wins the total order over B again, and must preempt the settled B-based
    # VALID window even though that window was never PENDING_CORRECTION at this point.
    swing_a2 = swing_confirmed_at(
        allocator, pivot_index=8, swing_id="A", swing_revision=2, pivot_price="103", recorded_offset_minutes=30
    )
    preempt_events = engine.on_swing_confirmed(swing_a2, cursor=frontier_at(swing_a2.recorded_time))
    assert len(preempt_events) == 2  # invalidation of B-based fact + A(rev2)-based replacement
    invalidation = only_invalidated(preempt_events[0])
    assert invalidation.invalidated_fact_ref == temporary.ref
    # P3-FEATURE-A-MAJ-04/ADR-034: B itself was never invalidated — the B-based FEATURE fact is
    # invalidated because A(rev2) newly-visibly supersedes B in the deterministic total order, not
    # because a SwingInvalidated targeting B was ever received.
    assert invalidation.invalidation_cause == "eligible_swing_selection_superseded"
    assert invalidation.causation_refs == (temporary.ref, swing_a2.ref)
    # P3-PY-MUT-STEP9-A field-completeness remediation (EVID-03,
    # constructed_object_field_not_independently_asserted): remaining
    # constructor-set fields of `_preempt_settled_window`'s returned
    # `FeatureFactInvalidated`, not previously asserted anywhere.
    assert invalidation.scope == temporary.scope
    assert invalidation.window_start == temporary.window_start
    assert invalidation.window_end == temporary.window_end
    assert invalidation.recorded_time >= swing_a2.recorded_time
    assert invalidation.ref.stream_id == "feature"
    assert invalidation.event_contract_ref == EventContractRef(
        FEATURE_FACT_INVALIDATED_CONTRACT_ID, FEATURE_OUTPUT_CONTRACT_VERSION
    )
    # ADR-035: R_later (this invalidation's own cursor) differs from R_original (temporary's own
    # cursor, captured independently at ITS OWN evaluation) — never inherited/copied.
    assert invalidation.computation_cursor != temporary.computation_cursor
    assert invalidation.computation_cursor.recorded_time == swing_a2.recorded_time
    final = only_computed(preempt_events[1])
    assert final.supersedes_fact_ref == temporary.ref
    assert final.value == Decimal("2.00")  # 105 - 103 (A revision 2's corrected price)
    assert final.window_start == original.window_start
    assert final.window_end == original.window_end


# --- P3-FEATURE-A-MAJ-02 remediation: contract qualification -----------------


def test_unauthorized_candle_contract_id_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    bad = dataclasses.replace(reference, event_contract_ref=EventContractRef("candle-observed", CONTRACT_VERSION))
    with pytest.raises(UnauthorizedUpstreamContractError):
        engine.on_candle(bad, cursor=frontier_at(bad.recorded_time))


def test_unauthorized_candle_contract_version_fails_closed_even_when_id_matches(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """P3-FEATURE-A-MAJ-02: a matching contract_id is NOT sufficient — an
    arbitrary, unauthorized contract_version must still fail closed.
    """
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    bad = dataclasses.replace(
        reference, event_contract_ref=EventContractRef(reference.event_contract_ref.contract_id, "not-authorized-v9")
    )
    with pytest.raises(UnauthorizedUpstreamContractError):
        engine.on_candle(bad, cursor=frontier_at(bad.recorded_time))


def test_unauthorized_swing_contract_id_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1")
    bad = dataclasses.replace(swing, event_contract_ref=EventContractRef("swing-candidate-detected", CONTRACT_VERSION))
    with pytest.raises(UnauthorizedUpstreamContractError):
        engine.on_swing_confirmed(bad, cursor=frontier_at(bad.recorded_time))


def test_unauthorized_swing_contract_version_fails_closed_even_when_id_matches(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1")
    bad = dataclasses.replace(
        swing, event_contract_ref=EventContractRef(swing.event_contract_ref.contract_id, "not-authorized-v9")
    )
    with pytest.raises(UnauthorizedUpstreamContractError):
        engine.on_swing_confirmed(bad, cursor=frontier_at(bad.recorded_time))


def test_output_contract_version_must_be_genuine_non_empty(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    from feature_engine.errors import UnresolvedOutputContractAuthorityError

    definition = make_distance_definition()
    scope = feature_scope("distance_to_last_confirmed_swing", version=definition.feature_definition_version)
    with pytest.raises(UnresolvedOutputContractAuthorityError):
        SwingDistanceFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version="",
            authorized_candle_contract_refs=authorized_candle_contract_refs(),
            authorized_swing_contract_refs=authorized_swing_contract_refs(),
            input_contract_authority_provider=StaticInputContractAuthorityProvider(SWING_DISTANCE_INPUT_CONTRACT),
        )


# --- Constructor validation guards (P3-FEATURE-QG-COV-01 remediation) -------
#
# Every existing constructor test above supplies a fully self-consistent,
# valid Definition/scope/authorized-contract-ref combination (via `_engine`
# or by hand) — none of them exercise the six independent construction-time
# rejection guards below, each raising BEFORE the Input Contract authority
# is even resolved.


def test_wrong_feature_type_for_swing_engine_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    definition = make_candle_definition()
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    with pytest.raises(ValueError, match="unsupported feature_type"):
        SwingDistanceFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
            authorized_candle_contract_refs=authorized_candle_contract_refs(),
            authorized_swing_contract_refs=authorized_swing_contract_refs(),
            input_contract_authority_provider=StaticInputContractAuthorityProvider(SWING_DISTANCE_INPUT_CONTRACT),
        )


def test_scope_definition_mismatch_for_swing_engine_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    definition = make_distance_definition()
    scope = feature_scope("distance_to_last_confirmed_swing", version="a-different-version-than-the-definition")
    with pytest.raises(ValueError, match="scope does not match definition"):
        SwingDistanceFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
            authorized_candle_contract_refs=authorized_candle_contract_refs(),
            authorized_swing_contract_refs=authorized_swing_contract_refs(),
            input_contract_authority_provider=StaticInputContractAuthorityProvider(SWING_DISTANCE_INPUT_CONTRACT),
        )


def test_empty_authorized_candle_contract_refs_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    definition = make_distance_definition()
    scope = feature_scope("distance_to_last_confirmed_swing", version=definition.feature_definition_version)
    with pytest.raises(InvalidFeatureDefinitionError, match="authorized_candle_contract_refs must be non-empty"):
        SwingDistanceFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
            authorized_candle_contract_refs=frozenset(),
            authorized_swing_contract_refs=authorized_swing_contract_refs(),
            input_contract_authority_provider=StaticInputContractAuthorityProvider(SWING_DISTANCE_INPUT_CONTRACT),
        )


def test_unsupported_candle_contract_id_in_authorized_set_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    definition = make_distance_definition()
    scope = feature_scope("distance_to_last_confirmed_swing", version=definition.feature_definition_version)
    with pytest.raises(InvalidFeatureDefinitionError, match="unsupported contract_id"):
        SwingDistanceFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
            authorized_candle_contract_refs=frozenset({EventContractRef("candle-observed", CONTRACT_VERSION)}),
            authorized_swing_contract_refs=authorized_swing_contract_refs(),
            input_contract_authority_provider=StaticInputContractAuthorityProvider(SWING_DISTANCE_INPUT_CONTRACT),
        )


def test_empty_authorized_swing_contract_refs_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    definition = make_distance_definition()
    scope = feature_scope("distance_to_last_confirmed_swing", version=definition.feature_definition_version)
    with pytest.raises(InvalidFeatureDefinitionError, match="authorized_swing_contract_refs must be non-empty"):
        SwingDistanceFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
            authorized_candle_contract_refs=authorized_candle_contract_refs(),
            authorized_swing_contract_refs=frozenset(),
            input_contract_authority_provider=StaticInputContractAuthorityProvider(SWING_DISTANCE_INPUT_CONTRACT),
        )


def test_unsupported_swing_contract_id_in_authorized_set_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    definition = make_distance_definition()
    scope = feature_scope("distance_to_last_confirmed_swing", version=definition.feature_definition_version)
    with pytest.raises(InvalidFeatureDefinitionError, match="unsupported contract_id"):
        SwingDistanceFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
            authorized_candle_contract_refs=authorized_candle_contract_refs(),
            authorized_swing_contract_refs=frozenset({EventContractRef("swing-candidate-detected", CONTRACT_VERSION)}),
            input_contract_authority_provider=StaticInputContractAuthorityProvider(SWING_DISTANCE_INPUT_CONTRACT),
        )


def test_engine_own_profile_check_rejects_mismatched_authority(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """`StaticInputContractAuthorityProvider.resolve()` already pre-validates
    its own wrapped authority's profile (see
    `test_input_contract_profile_mismatch_fails_closed_at_construction`
    above, which exercises THAT check) — so it never reaches this engine's
    OWN internal `feature_computation_profile` guard (line 297-298). Using
    `_FixedAuthorityProvider`, which returns whatever it is given
    regardless of the requested profile, isolates and exercises the
    engine's own independent check instead.
    """
    from conftest import REGIME_INPUT_CONTRACT

    with pytest.raises(InputContractIdentityMismatchError):
        _engine(
            allocator, time_source, input_contract_authority_provider=_FixedAuthorityProvider(REGIME_INPUT_CONTRACT)
        )


# --- Scope/causal-ordering rejection guards (P3-FEATURE-QG-COV-01 remediation)
#
# `NonMonotonicRecordedTimeError`/`OutOfOrderCandleError`/
# `OutOfOrderCorrectionError` are the exact three error paths named by
# `P3-FEATURE-QG-MIN-01` — recorded here as a factual overlap; these tests
# alone are supporting evidence only, not a claim that MIN-01 is closed.
# `ForeignScopeError` (candle side) is one of the four raise sites cited by
# `P3-FEATURE-QG-EVID-06` — same factual-overlap caveat, not a claim of
# EVID-06 closure.


def test_foreign_scope_candle_rejected(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    foreign_scope = dataclasses.replace(reference.scope, instrument_id="ETH-USDT")
    foreign = dataclasses.replace(reference, scope=foreign_scope)
    with pytest.raises(ForeignScopeError):
        engine.on_candle(foreign, cursor=frontier_at(foreign.recorded_time))


def test_foreign_scope_swing_confirmed_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    foreign = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", instrument_id="ETH-USDT")
    with pytest.raises(ForeignScopeError):
        engine.on_swing_confirmed(foreign, cursor=frontier_at(foreign.recorded_time))


def test_wrong_swing_definition_version_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact = swing_confirmed_at(
        allocator, pivot_index=2, swing_id="s1", swing_definition_version="not-the-pinned-version"
    )
    with pytest.raises(InvalidSwingEligibilityInputError, match="expected swing_definition_version"):
        engine.on_swing_confirmed(fact, cursor=frontier_at(fact.recorded_time))


def test_wrong_swing_direction_rejected(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)  # default swing_direction="HIGH"
    fact = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", direction="LOW")
    with pytest.raises(InvalidSwingEligibilityInputError, match="expected swing_direction"):
        engine.on_swing_confirmed(fact, cursor=frontier_at(fact.recorded_time))


def test_invalid_swing_invalidation_target_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Invalidating a swing_id/revision this engine never confirmed must be
    rejected — never silently accepted as a no-op.
    """
    engine = _engine(allocator, time_source)
    inv = swing_invalidated_at(allocator, swing_id="never-confirmed", swing_revision=1, recorded_time=BASE)
    with pytest.raises(InvalidSwingEligibilityInputError, match="not the current non-invalidated revision"):
        engine.on_swing_invalidated(inv, cursor=frontier_at(inv.recorded_time))


def test_non_monotonic_candle_recorded_time_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    first = candle_at(allocator, 10, high="110", low="90", close="105")
    engine.on_candle(first, cursor=frontier_at(first.recorded_time))
    earlier = candle_at(allocator, 20, high="120", low="95", close="110", recorded_offset_seconds=-3600)
    assert earlier.recorded_time < first.recorded_time
    with pytest.raises(NonMonotonicRecordedTimeError):
        engine.on_candle(earlier, cursor=frontier_at(earlier.recorded_time))


def test_non_monotonic_swing_recorded_time_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    first = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", recorded_offset_minutes=100)
    engine.on_swing_confirmed(first, cursor=frontier_at(first.recorded_time))
    earlier = swing_confirmed_at(allocator, pivot_index=3, swing_id="s2", recorded_offset_minutes=-100)
    assert earlier.recorded_time < first.recorded_time
    with pytest.raises(NonMonotonicRecordedTimeError):
        engine.on_swing_confirmed(earlier, cursor=frontier_at(earlier.recorded_time))


def test_non_causal_time_source_rejected(allocator: SequenceAllocator) -> None:
    engine = _engine(allocator, NonCausalTimeSource())
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    with pytest.raises(RecordedTimeSourceViolationError):
        engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))


def test_swing_state_as_of_unknown_swing_id_returns_none(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """`_swing_state_as_of`'s own `if not records: return None` guard is
    unreachable via the public API: `_select_eligible_swing` only ever
    queries `swing_id`s already present as keys in `_swing_confirmations`
    (populated together with a non-empty record list, in the same
    `setdefault(...).append(...)` statement, in `on_swing_confirmed`) — so
    a key with an empty/absent record list can never occur through any
    public method sequence. This directly, minimally exercises the private
    method's own documented "no confirmation ever recorded for this
    swing_id" contract with a swing_id that is valid input but genuinely
    never confirmed — not a fabricated internal-state hack.
    """
    engine = _engine(allocator, time_source)
    assert engine._swing_state_as_of("never-confirmed-swing-id", frontier_at(BASE)) is None


def test_evidence_reference_conflict_when_candle_and_swing_refs_collide(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """`_normalize_evidence`'s own ref-collision guard: a genuine (if
    contrived) case where the Swing's own `EventRecordRef` happens to
    collide with the reference Candle's `EventRecordRef` — evidence refs
    must always be exactly two distinct events.
    """
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    colliding_swing = dataclasses.replace(
        swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100"), ref=reference.ref
    )
    engine.on_swing_confirmed(colliding_swing, cursor=frontier_at(colliding_swing.recorded_time))
    with pytest.raises(EvidenceReferenceConflictError):
        engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))


def test_candle_identical_redelivery_is_idempotent(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Mirrors `test_swing_same_ref_identical_redelivery_is_idempotent` for
    the Candle side: byte-for-byte identical redelivery of the same
    `EventRecordRef` (not a correction, not conflicting content) is a
    silent no-op — never re-enters lineage/dedup logic.
    """
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    events = engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))
    assert events == []  # no eligible Swing yet — valid absence
    replay = engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))
    assert replay == []


def test_candle_resubmitted_different_ref_without_correction_flag_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))
    resubmitted = dataclasses.replace(candle_at(allocator, 10, high="111", low="90", close="106"), is_correction=False)
    with pytest.raises(DuplicateCandleConflictError):
        engine.on_candle(resubmitted, cursor=frontier_at(resubmitted.recorded_time))


def test_first_seen_candle_marked_as_correction_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    correction = candle_at(allocator, 10, high="110", low="90", close="105", is_correction=True)
    with pytest.raises(OutOfOrderCorrectionError):
        engine.on_candle(correction, cursor=frontier_at(correction.recorded_time))


def test_out_of_order_candle_window_start_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    later = candle_at(allocator, 10, high="110", low="90", close="105")
    engine.on_candle(later, cursor=frontier_at(later.recorded_time))
    earlier_window = candle_at(allocator, 5, high="108", low="92", close="100", recorded_offset_seconds=3600)
    with pytest.raises(OutOfOrderCandleError):
        engine.on_candle(earlier_window, cursor=frontier_at(earlier_window.recorded_time))


def test_lineage_reevaluation_skips_window_not_using_the_invalidated_swing(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """`on_swing_invalidated` re-attempts every lineage window using the
    invalidated Swing's ref — a SEPARATE window that settled on a
    DIFFERENT Swing must be skipped (`continue`), not touched.
    """
    engine = _engine(allocator, time_source)
    swing_a = swing_confirmed_at(allocator, pivot_index=2, swing_id="A", pivot_price="100")
    engine.on_swing_confirmed(swing_a, cursor=frontier_at(swing_a.recorded_time))
    window_one = candle_at(allocator, 10, high="110", low="90", close="105")
    engine.on_candle(window_one, cursor=frontier_at(window_one.recorded_time))

    swing_b = swing_confirmed_at(allocator, pivot_index=20, swing_id="B", pivot_price="200")
    engine.on_swing_confirmed(swing_b, cursor=frontier_at(swing_b.recorded_time))
    window_two = candle_at(allocator, 30, high="210", low="190", close="205")
    engine.on_candle(window_two, cursor=frontier_at(window_two.recorded_time))

    inv_a = swing_invalidated_at(allocator, swing_id="A", swing_revision=1, recorded_time=BASE + timedelta(hours=1))
    events = engine.on_swing_invalidated(inv_a, cursor=frontier_at(inv_a.recorded_time))
    # Only window_one (which used A) is invalidated -- window_two (which used B) is
    # skipped entirely, never re-touched, never re-emitted.
    assert len(events) == 1
    assert only_invalidated(events[0]).window_start == window_one.scope.window_start


# --- P3-FEATURE-A-MAJ-05 remediation: dedup is ref-identity-only -------------


def test_candle_distinct_correction_ref_enters_lineage_even_when_value_unchanged(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    # P3-PY-MUT-STEP9-A field-completeness remediation (EVID-03,
    # constructed_object_field_not_independently_asserted): this scenario
    # exercises BOTH `_invalidate_and_replace` (the invalidation) and
    # `_emit_replacement_only` (the replacement) in one disciplined
    # candle-correction sequence -- every constructor-set field of both
    # emitted events is now independently asserted, not just
    # `.value`/`.supersedes_fact_ref`/`.ref` as before.
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    original = only_computed(engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])

    correction = dataclasses.replace(
        reference,
        ref=allocator.next_ref(CANDLE_STREAM_ID),
        recorded_time=reference.recorded_time + timedelta(seconds=120),
        is_correction=True,
        event_contract_ref=EventContractRef(CANDLE_CORRECTED_CONTRACT_ID, CONTRACT_VERSION),
    )
    events = engine.on_candle(correction, cursor=frontier_at(correction.recorded_time))
    assert len(events) == 2
    invalidation = only_invalidated(events[0])
    assert invalidation.scope == original.scope
    assert invalidation.invalidated_fact_ref == original.ref
    assert invalidation.invalidation_cause == "candle_corrected"
    assert invalidation.window_start == original.window_start
    assert invalidation.window_end == original.window_end
    assert invalidation.causation_refs == (original.ref, correction.ref)
    assert invalidation.recorded_time >= correction.recorded_time
    assert invalidation.ref.stream_id == "feature"
    assert invalidation.event_contract_ref == EventContractRef(
        FEATURE_FACT_INVALIDATED_CONTRACT_ID, FEATURE_OUTPUT_CONTRACT_VERSION
    )

    replacement = only_computed(events[1])
    assert replacement.value == original.value
    assert replacement.supersedes_fact_ref == original.ref
    assert replacement.ref != original.ref
    assert replacement.scope == original.scope
    assert replacement.unit == original.unit
    assert set(replacement.input_fact_refs) == {correction.ref, swing.ref}
    assert replacement.causation_refs == (*replacement.input_fact_refs, invalidation.ref)
    assert replacement.ref.stream_id == "feature"
    assert replacement.event_contract_ref == EventContractRef(
        FEATURE_COMPUTED_CONTRACT_ID, FEATURE_OUTPUT_CONTRACT_VERSION
    )


def test_candle_same_ref_different_content_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))
    conflicting = dataclasses.replace(reference, ohlcv=dataclasses.replace(reference.ohlcv, high=Decimal("999")))
    with pytest.raises(EvidenceReferenceConflictError):
        engine.on_candle(conflicting, cursor=frontier_at(conflicting.recorded_time))


def test_candle_same_ref_different_recorded_time_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """P3-FEATURE-A-MAJ-05: content equality alone is insufficient — same ref
    with the SAME OHLCV but a DIFFERENT recorded_time must still fail closed.
    """
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))
    conflicting = dataclasses.replace(reference, recorded_time=reference.recorded_time + timedelta(seconds=1))
    with pytest.raises(EvidenceReferenceConflictError):
        engine.on_candle(conflicting, cursor=frontier_at(conflicting.recorded_time))


def test_swing_same_ref_different_content_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """P3-FEATURE-A-MAJ-05: the engine's own Swing ingestion dedup path
    (distinct from `normalize_input_facts`'s generic evidence-normalization
    check) must independently fail closed on same-ref-different-content.
    """
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    conflicting = dataclasses.replace(swing, pivot_price=Decimal("999"))
    with pytest.raises(EvidenceReferenceConflictError):
        engine.on_swing_confirmed(conflicting, cursor=frontier_at(conflicting.recorded_time))


def test_swing_same_ref_identical_redelivery_is_idempotent(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    assert engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time)) == []


# --- Review-A residual 1: history-preserving as-of Swing state --------------
#
# `_swing_state_as_of` is this engine's own internal, append-only-history-backed
# reconstruction of Eligible-Swing state at an arbitrary cursor (ADR-035
# "Implementation consequence") — exercised directly here because no public
# projection API exists for querying a HISTORICAL cursor (only the CURRENT
# triggering cursor is exposed through `on_candle`/`on_swing_confirmed`/
# `on_swing_invalidated`). This mirrors testing any other internal invariant
# of a state machine that has no dedicated public query surface.


def test_historical_invalidation_visibility_does_not_leak_backward(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """A LATER invalidation of a Swing revision must never retroactively
    change what an EARLIER cursor query answers — engine-internal state must
    be cursor-aware and history-preserving, never destructively overwritten.
    """
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))

    r1 = swing.recorded_time + timedelta(minutes=5)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    computed = only_computed(engine.on_candle(reference, cursor=frontier_at(r1))[0])
    assert computed.value == Decimal("5.00")

    r2 = r1 + timedelta(minutes=10)
    inv = swing_invalidated_at(allocator, swing_id="s1", swing_revision=1, recorded_time=r2)
    engine.on_swing_invalidated(inv, cursor=frontier_at(r2))

    # Query AS OF r1 — strictly BEFORE the invalidation's own recorded_time.
    state_at_r1 = engine._swing_state_as_of("s1", frontier_at(r1))
    assert state_at_r1 is not None
    assert state_at_r1.revision == 1
    assert state_at_r1.ref == swing.ref


def test_historical_revision_overwrite_does_not_erase_earlier_revision(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """After A1 -> invalidated -> A2 confirmed, a cursor query BEFORE A1's own
    invalidation must still reconstruct revision 1 as the as-of state —
    revision 2 must be invisible there, never having silently overwritten
    revision 1's own historical record.
    """
    engine = _engine(allocator, time_source)
    s1 = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=1, pivot_price="100")
    engine.on_swing_confirmed(s1, cursor=frontier_at(s1.recorded_time))

    inv = swing_invalidated_at(
        allocator, swing_id="s1", swing_revision=1, recorded_time=s1.recorded_time + timedelta(minutes=10)
    )
    engine.on_swing_invalidated(inv, cursor=frontier_at(inv.recorded_time))

    s2 = swing_confirmed_at(
        allocator, pivot_index=2, swing_id="s1", swing_revision=2, pivot_price="102", recorded_offset_minutes=20
    )
    engine.on_swing_confirmed(s2, cursor=frontier_at(s2.recorded_time))

    r_before_invalidation = s1.recorded_time + timedelta(minutes=5)
    state = engine._swing_state_as_of("s1", frontier_at(r_before_invalidation))
    assert state is not None
    assert state.revision == 1
    assert state.pivot_price == Decimal("100")


def test_cursor_between_invalidation_and_next_revision_neither_eligible(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """At a cursor where A1's invalidation IS visible but A2's confirmation is
    NOT yet visible, swing_id `s1` must be eligible under NEITHER revision —
    A1 invalid, A2 not yet confirmed as of this cursor.
    """
    engine = _engine(allocator, time_source)
    s1 = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", swing_revision=1, pivot_price="100")
    engine.on_swing_confirmed(s1, cursor=frontier_at(s1.recorded_time))

    inv = swing_invalidated_at(
        allocator, swing_id="s1", swing_revision=1, recorded_time=s1.recorded_time + timedelta(minutes=10)
    )
    engine.on_swing_invalidated(inv, cursor=frontier_at(inv.recorded_time))

    s2 = swing_confirmed_at(
        allocator, pivot_index=2, swing_id="s1", swing_revision=2, pivot_price="102", recorded_offset_minutes=20
    )
    engine.on_swing_confirmed(s2, cursor=frontier_at(s2.recorded_time))

    between = inv.recorded_time + timedelta(minutes=1)
    assert between < s2.recorded_time
    state = engine._swing_state_as_of("s1", frontier_at(between))
    assert state is None


def test_restart_rebuild_parity_same_cursor_answer_regardless_of_later_ingested_events(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Querying eligibility as-of cursor R must give the SAME answer whether
    the engine has ALSO already ingested later events (a "live" engine that
    kept running) or has ingested ONLY events up to R (a freshly "restarted"
    engine reconstructing purely from durable history up to that boundary) —
    the reconstruction depends only on the durable evidence visible at R,
    never on how much MORE the process happens to already know. No
    process-local-only shortcut.
    """
    # Same run_id on both allocators — the point is comparing byte-for-byte identical
    # `EventRecordRef`s, isolating the assertion to the historical-reconstruction
    # question rather than an incidental run-identity difference.
    live_allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="shared-run")
    live_engine = _engine(live_allocator, FixedDeltaTimeSource())

    restarted_allocator = SequenceAllocator(
        module_id="feature-engine", implementation_version="0.1.0", run_id="shared-run"
    )
    restarted_engine = _engine(restarted_allocator, FixedDeltaTimeSource())

    s1_live = swing_confirmed_at(live_allocator, pivot_index=2, swing_id="s1", swing_revision=1, pivot_price="100")
    s1_restarted = swing_confirmed_at(
        restarted_allocator, pivot_index=2, swing_id="s1", swing_revision=1, pivot_price="100"
    )
    live_engine.on_swing_confirmed(s1_live, cursor=frontier_at(s1_live.recorded_time))
    restarted_engine.on_swing_confirmed(s1_restarted, cursor=frontier_at(s1_restarted.recorded_time))

    r = s1_live.recorded_time + timedelta(minutes=5)

    # The LIVE engine keeps going: ingest a later invalidation + replacement revision
    # AFTER `r` — this must not change what a query AT `r` answers.
    inv_live = swing_invalidated_at(
        live_allocator, swing_id="s1", swing_revision=1, recorded_time=r + timedelta(minutes=10)
    )
    live_engine.on_swing_invalidated(inv_live, cursor=frontier_at(inv_live.recorded_time))
    s2_live = swing_confirmed_at(
        live_allocator, pivot_index=2, swing_id="s1", swing_revision=2, pivot_price="102", recorded_offset_minutes=20
    )
    live_engine.on_swing_confirmed(s2_live, cursor=frontier_at(s2_live.recorded_time))

    # The RESTARTED engine never ingested anything past `r` at all.
    live_state = live_engine._swing_state_as_of("s1", frontier_at(r))
    restarted_state = restarted_engine._swing_state_as_of("s1", frontier_at(r))
    assert live_state is not None
    assert restarted_state is not None
    assert live_state.revision == restarted_state.revision == 1
    assert live_state.ref == restarted_state.ref
    assert live_state.pivot_price == restarted_state.pivot_price == Decimal("100")


# --- 18. Deterministic replay --------------------------------------------------


def test_deterministic_replay_same_input_different_engine_instances() -> None:
    def _build() -> tuple[SwingDistanceFeatureEngine, SequenceAllocator]:
        allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="replay-run")
        return _engine(allocator, FixedDeltaTimeSource()), allocator

    engine_a, allocator_a = _build()
    engine_b, allocator_b = _build()

    swing_a = swing_confirmed_at(allocator_a, pivot_index=2, swing_id="s1", pivot_price="100")
    swing_b = swing_confirmed_at(allocator_b, pivot_index=2, swing_id="s1", pivot_price="100")
    reference_a = candle_at(allocator_a, 10, high="110", low="90", close="105")
    reference_b = candle_at(allocator_b, 10, high="110", low="90", close="105")

    engine_a.on_swing_confirmed(swing_a, cursor=frontier_at(swing_a.recorded_time))
    engine_b.on_swing_confirmed(swing_b, cursor=frontier_at(swing_b.recorded_time))
    events_a = engine_a.on_candle(reference_a, cursor=frontier_at(reference_a.recorded_time))
    events_b = engine_b.on_candle(reference_b, cursor=frontier_at(reference_b.recorded_time))
    assert events_a == events_b
    assert len(events_a) == 1
    # Full struct equality (frozen dataclasses) recursively compares computation_cursor too —
    # same durable evidence replayed independently produces byte-for-byte identical cursors.
    assert only_computed(events_a[0]).computation_cursor == only_computed(events_b[0]).computation_cursor


# --- P3-FEATURE-A-MAJ-06 remediation: durable computation_cursor -------------


def test_feature_computed_and_invalidated_carry_full_computation_cursor(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    r = reference.recorded_time
    computed = only_computed(engine.on_candle(reference, cursor=frontier_at(r))[0])
    cursor = computed.computation_cursor
    assert cursor.recorded_time == r
    assert cursor.input_contract_ref == SWING_DISTANCE_INPUT_CONTRACT.input_contract_ref
    assert cursor.stream_registry_version == SWING_DISTANCE_INPUT_CONTRACT.stream_registry_version
    assert cursor.lifecycle_frontier == LifecycleFrontier(
        stream_id="platform-lifecycle", position=LifecyclePosition(kind="genesis", sequence=0)
    )
    assert dict(cursor.stream_positions) == dict.fromkeys(SWING_DISTANCE_INPUT_CONTRACT.included_streams, 10**9)

    correction = dataclasses.replace(
        reference,
        ref=allocator.next_ref(CANDLE_STREAM_ID),
        recorded_time=r + timedelta(seconds=120),
        is_correction=True,
        event_contract_ref=EventContractRef(CANDLE_CORRECTED_CONTRACT_ID, CONTRACT_VERSION),
    )
    invalidation = only_invalidated(engine.on_candle(correction, cursor=frontier_at(correction.recorded_time))[0])
    inv_cursor = invalidation.computation_cursor
    assert inv_cursor.recorded_time == correction.recorded_time
    assert inv_cursor.input_contract_ref == SWING_DISTANCE_INPUT_CONTRACT.input_contract_ref
    assert inv_cursor.stream_registry_version == SWING_DISTANCE_INPUT_CONTRACT.stream_registry_version


def test_original_and_replacement_facts_have_distinct_computation_cursor(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    original = only_computed(engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])

    correction = dataclasses.replace(
        reference,
        ref=allocator.next_ref(CANDLE_STREAM_ID),
        recorded_time=reference.recorded_time + timedelta(seconds=120),
        is_correction=True,
        event_contract_ref=EventContractRef(CANDLE_CORRECTED_CONTRACT_ID, CONTRACT_VERSION),
    )
    events = engine.on_candle(correction, cursor=frontier_at(correction.recorded_time))
    replacement = only_computed(events[1])
    # Independently captured at its own evaluation — never inherited/copied from the fact it
    # supersedes, even though both facts used the same eligible Swing.
    assert replacement.computation_cursor != original.computation_cursor
    assert replacement.computation_cursor.recorded_time == correction.recorded_time
    assert original.computation_cursor.recorded_time == reference.recorded_time


def test_computation_cursor_survives_reconstruction_round_trip(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    computed = only_computed(engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])

    original_cursor = computed.computation_cursor
    reconstructed = ComputationCursor(
        recorded_time=original_cursor.recorded_time,
        input_contract_ref=InputContractRef(
            original_cursor.input_contract_ref.contract_id, original_cursor.input_contract_ref.contract_version
        ),
        stream_registry_version=original_cursor.stream_registry_version,
        lifecycle_frontier=LifecycleFrontier(
            stream_id=original_cursor.lifecycle_frontier.stream_id,
            position=LifecyclePosition(
                kind=original_cursor.lifecycle_frontier.position.kind,
                sequence=original_cursor.lifecycle_frontier.position.sequence,
            ),
        ),
        stream_positions=dict(original_cursor.stream_positions),
    )
    assert reconstructed == original_cursor


def test_stream_position_ceiling_excludes_swing_from_eligibility(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """A Swing that is recorded-time visible but whose own `EventRecordRef.sequence`
    exceeds `stream_positions["swing"]` must be excluded (feature.md §12(a) branch 2) —
    a Swing sitting in the engine's in-memory state is never selected on recorded_time
    visibility alone.
    """
    # Two independent engine instances (a fresh Candle ingestion dedups on ref identity
    # regardless of cursor, so the below/at-ceiling cases must not share one engine).
    below_engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    below_engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")

    below_ceiling = frontier_at(
        reference.recorded_time,
        stream_positions={
            CANDLE_STREAM_ID: StreamPositionProof(sequence=10**9, event_recorded_time=reference.recorded_time),
            # sequence - 1 == 0 == that stream's own genesis_position — no event yet, no proof needed.
            SWING_STREAM_ID: StreamPositionProof(sequence=swing.ref.sequence - 1, event_recorded_time=None),
        },
    )
    assert below_engine.on_candle(reference, cursor=below_ceiling) == []

    at_engine = _engine(allocator, time_source)
    at_engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    at_ceiling = frontier_at(
        reference.recorded_time,
        stream_positions={
            CANDLE_STREAM_ID: StreamPositionProof(sequence=10**9, event_recorded_time=reference.recorded_time),
            SWING_STREAM_ID: StreamPositionProof(sequence=swing.ref.sequence, event_recorded_time=swing.recorded_time),
        },
    )
    events = at_engine.on_candle(reference, cursor=at_ceiling)
    assert len(events) == 1


def test_lifecycle_frontier_captured_verbatim_in_computation_cursor(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")

    distinctive_position = LifecyclePosition(kind="event", sequence=42)
    distinctive_proof = LifecycleFrontierProof(
        stream_id="platform-lifecycle",
        position=distinctive_position,
        event_recorded_time=reference.recorded_time,  # <= cursor.recorded_time, satisfies Lifecycle -> Cursor
    )
    computed = only_computed(
        engine.on_candle(
            reference, cursor=frontier_at(reference.recorded_time, lifecycle_frontier=distinctive_proof)
        )[0]
    )
    assert computed.computation_cursor.lifecycle_frontier == LifecycleFrontier(
        stream_id="platform-lifecycle", position=distinctive_position
    )


def test_registry_mismatch_fails_closed_before_emission(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    mismatched = dataclasses.replace(
        frontier_at(reference.recorded_time), stream_registry_version="a-different-registry-version"
    )
    with pytest.raises(RegistryContractMismatchError):
        engine.on_candle(reference, cursor=mismatched)


# --- Review-A residual 2: Input Contract authority is a single verified unit -


def test_input_contract_profile_mismatch_fails_closed_at_construction(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """A `VerifiedInputContractAuthority` resolved for the WRONG Feature
    computation profile (here: the `regime` profile, supplied to a
    swing-distance engine) must fail closed, even though it is itself a
    genuine, currently-approved authority value — just not the one this
    engine requires. (Negative test 5.)
    """
    from conftest import REGIME_INPUT_CONTRACT

    with pytest.raises(InputContractIdentityMismatchError):
        _engine(
            allocator,
            time_source,
            input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
        )


# --- Review-A round-5: resolver-only field validation (moved off the now- ---
# --- fully-disabled VerifiedInputContractAuthority public constructor) ------
#
# `_seal_verified_authority` is the sole legitimate constructor of
# `VerifiedInputContractAuthority` (used exclusively by
# `authority_resolver.py`) — these checks used to be exercised via
# `dataclasses.replace(SWING_DISTANCE_INPUT_CONTRACT, ...)`, which round-5
# now rejects UNCONDITIONALLY for every field (see the mutation tests
# below), so the underlying field-validation coverage is retargeted directly
# at that sole legitimate entrypoint instead.


def test_invented_resolved_input_contract_without_content_identity_fails_closed() -> None:
    """Review-A round-2 residual 1: internally self-consistent semantic
    literals (even ones equal to the real, currently-approved identity) are
    NOT sufficient authorization on their own — genuine content-identity
    proof for BOTH source artifacts is required.
    """
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        _seal_verified_authority(
            feature_computation_profile=SWING_DISTANCE_INPUT_CONTRACT.feature_computation_profile,
            input_contract_ref=SWING_DISTANCE_INPUT_CONTRACT.input_contract_ref,
            stream_registry_version=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_version,
            included_streams=SWING_DISTANCE_INPUT_CONTRACT.included_streams,
            input_contract_content_id="",
            stream_registry_content_id="",
        )


def test_empty_input_contract_content_id_fails_closed() -> None:
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        _seal_verified_authority(
            feature_computation_profile=SWING_DISTANCE_INPUT_CONTRACT.feature_computation_profile,
            input_contract_ref=SWING_DISTANCE_INPUT_CONTRACT.input_contract_ref,
            stream_registry_version=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_version,
            included_streams=SWING_DISTANCE_INPUT_CONTRACT.included_streams,
            input_contract_content_id="",
            stream_registry_content_id=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_content_id,
        )


def test_empty_stream_registry_content_id_fails_closed() -> None:
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        _seal_verified_authority(
            feature_computation_profile=SWING_DISTANCE_INPUT_CONTRACT.feature_computation_profile,
            input_contract_ref=SWING_DISTANCE_INPUT_CONTRACT.input_contract_ref,
            stream_registry_version=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_version,
            included_streams=SWING_DISTANCE_INPUT_CONTRACT.included_streams,
            input_contract_content_id=SWING_DISTANCE_INPUT_CONTRACT.input_contract_content_id,
            stream_registry_content_id="",
        )


def test_fabricated_input_contract_content_id_fails_closed() -> None:
    """A non-empty but fabricated/arbitrary string (never derived from
    hashing any real artifact) must be rejected just as forcefully as an
    empty one — `"fabricated"` is not a well-formed content-identity digest.
    """
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        _seal_verified_authority(
            feature_computation_profile=SWING_DISTANCE_INPUT_CONTRACT.feature_computation_profile,
            input_contract_ref=SWING_DISTANCE_INPUT_CONTRACT.input_contract_ref,
            stream_registry_version=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_version,
            included_streams=SWING_DISTANCE_INPUT_CONTRACT.included_streams,
            input_contract_content_id="fabricated",
            stream_registry_content_id=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_content_id,
        )


def test_wrong_length_hex_content_id_fails_closed() -> None:
    """Even a string composed entirely of valid hex characters must be
    exactly 64 characters (a genuine SHA-256 digest length) — a truncated or
    padded fake is still rejected.
    """
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        _seal_verified_authority(
            feature_computation_profile=SWING_DISTANCE_INPUT_CONTRACT.feature_computation_profile,
            input_contract_ref=SWING_DISTANCE_INPUT_CONTRACT.input_contract_ref,
            stream_registry_version=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_version,
            included_streams=SWING_DISTANCE_INPUT_CONTRACT.included_streams,
            input_contract_content_id="a" * 63,
            stream_registry_content_id=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_content_id,
        )


def test_empty_stream_registry_version_fails_closed() -> None:
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        _seal_verified_authority(
            feature_computation_profile=SWING_DISTANCE_INPUT_CONTRACT.feature_computation_profile,
            input_contract_ref=SWING_DISTANCE_INPUT_CONTRACT.input_contract_ref,
            stream_registry_version="",
            included_streams=SWING_DISTANCE_INPUT_CONTRACT.included_streams,
            input_contract_content_id=SWING_DISTANCE_INPUT_CONTRACT.input_contract_content_id,
            stream_registry_content_id=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_content_id,
        )


def test_empty_included_streams_fails_closed() -> None:
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        _seal_verified_authority(
            feature_computation_profile=SWING_DISTANCE_INPUT_CONTRACT.feature_computation_profile,
            input_contract_ref=SWING_DISTANCE_INPUT_CONTRACT.input_contract_ref,
            stream_registry_version=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_version,
            included_streams=frozenset(),
            input_contract_content_id=SWING_DISTANCE_INPUT_CONTRACT.input_contract_content_id,
            stream_registry_content_id=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_content_id,
        )


# --- Review-A round-5: VerifiedInputContractAuthority has no public API -----
# --- (negative tests 1-4, 6; see also test_input_contract_profile_mismatch- --
# --- fails_closed_at_construction above for negative test 5) ---------------


def test_verified_authority_not_exported_from_public_package() -> None:
    """Negative test 1: neither `VerifiedInputContractAuthority` nor its
    resolver-internal precursor `ResolvedInputContract` is part of
    `feature_engine`'s own public surface — a normal caller who only ever
    imports `feature_engine` (never reaching into `feature_engine.contracts`)
    has no name at all to construct authority with.
    """
    import feature_engine

    assert not hasattr(feature_engine, "VerifiedInputContractAuthority")
    assert not hasattr(feature_engine, "ResolvedInputContract")
    assert "VerifiedInputContractAuthority" not in feature_engine.__all__
    assert "ResolvedInputContract" not in feature_engine.__all__


def test_directly_fabricated_verified_type_cannot_be_supplied_to_swing_engine() -> None:
    """Negative test 2: `VerifiedInputContractAuthority`'s own public
    constructor is disabled STRUCTURALLY — calling it directly, even with a
    fully genuine-looking field set plus Review-A's own literal residual
    example `"a" * 64`/`"b" * 64`, raises `TypeError` before any field is
    ever inspected. There is no normal public construction path at all, so
    there is nothing to wrap in a provider and supply to an engine.
    """
    with pytest.raises(TypeError):
        VerifiedInputContractAuthority(
            feature_computation_profile="distance_to_last_confirmed_swing",
            input_contract_ref=SWING_DISTANCE_INPUT_CONTRACT.input_contract_ref,
            stream_registry_version=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_version,
            included_streams=SWING_DISTANCE_INPUT_CONTRACT.included_streams,
            input_contract_content_id="a" * 64,
            stream_registry_content_id="b" * 64,
        )


def test_static_provider_cannot_launder_fabricated_authority(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Negative test 3: `StaticInputContractAuthorityProvider` remains
    public, but it cannot be used to launder a caller-manufactured
    "authority-shaped" object into something the engine accepts — the
    engine's own `isinstance(..., VerifiedInputContractAuthority)` check
    rejects whatever the provider hands back, regardless of how
    plausible-looking its fields are, because there is no supported way to
    construct a genuine `VerifiedInputContractAuthority` to wrap in the
    first place.
    """
    fabricated = ResolvedInputContract(
        feature_computation_profile="distance_to_last_confirmed_swing",
        input_contract_ref=SWING_DISTANCE_INPUT_CONTRACT.input_contract_ref,
        stream_registry_version=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_version,
        included_streams=SWING_DISTANCE_INPUT_CONTRACT.included_streams,
        input_contract_content_id="a" * 64,
        stream_registry_content_id="b" * 64,
    )
    laundering_provider = StaticInputContractAuthorityProvider(fabricated)  # type: ignore[arg-type]
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        _engine(allocator, time_source, input_contract_authority_provider=laundering_provider)


def test_engine_constructor_requires_provider_not_bare_authority_value() -> None:
    """Negative test 4: `SwingDistanceFeatureEngine`'s own constructor
    signature exposes an `input_contract_authority_provider` parameter typed
    `InputContractAuthorityProvider` — never a `resolved_input_contract`/
    `ResolvedInputContract`/`VerifiedInputContractAuthority` parameter. A
    bare `VerifiedInputContractAuthority` value has no `.resolve()` method of
    its own, so it structurally cannot be passed in place of a provider.
    """
    signature = inspect.signature(SwingDistanceFeatureEngine.__init__)
    assert "input_contract_authority_provider" in signature.parameters
    assert "resolved_input_contract" not in signature.parameters
    assert not hasattr(SWING_DISTANCE_INPUT_CONTRACT, "resolve")


def test_unverified_plain_authority_cannot_be_supplied_to_swing_engine_as_if_verified(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Negative test 6: a hand-built `ResolvedInputContract` — NOT the
    verified type, never produced by any resolver — wrapped in a provider
    that hands it back verbatim, must never be accepted by
    `SwingDistanceFeatureEngine` as though it were genuine, resolver-issued
    authority. The engine itself independently rejects a provider that
    returns anything other than a genuine `VerifiedInputContractAuthority`.
    """
    unverified = ResolvedInputContract(
        feature_computation_profile="distance_to_last_confirmed_swing",
        input_contract_ref=SWING_DISTANCE_INPUT_CONTRACT.input_contract_ref,
        stream_registry_version=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_version,
        included_streams=SWING_DISTANCE_INPUT_CONTRACT.included_streams,
        input_contract_content_id="unverified-hand-built-guess",
        stream_registry_content_id="unverified-hand-built-guess",
    )
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        _engine(allocator, time_source, input_contract_authority_provider=_FixedAuthorityProvider(unverified))


def test_valid_looking_fake_sha_digests_cannot_be_supplied_to_swing_engine_as_if_verified(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Negative test 6 (variant): `"a" * 64`/`"b" * 64` are syntactically
    valid SHA-256 hex, but were never computed from any resolved artifact —
    a plain `ResolvedInputContract` carrying them, with otherwise
    plausible/correct-looking semantic fields, must still be rejected.
    SHA-256 SHAPE != SHA-256 PROVENANCE.
    """
    fake_but_well_formed = ResolvedInputContract(
        feature_computation_profile="distance_to_last_confirmed_swing",
        input_contract_ref=SWING_DISTANCE_INPUT_CONTRACT.input_contract_ref,
        stream_registry_version=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_version,
        included_streams=SWING_DISTANCE_INPUT_CONTRACT.included_streams,
        input_contract_content_id="a" * 64,
        stream_registry_content_id="b" * 64,
    )
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        _engine(
            allocator, time_source, input_contract_authority_provider=_FixedAuthorityProvider(fake_but_well_formed)
        )


def test_mutated_verified_authority_rejected_structurally() -> None:
    """A genuinely resolver-issued authority cannot be turned into a
    different-but-still-accepted authority via `dataclasses.replace` at
    all — `replace()` itself calls `VerifiedInputContractAuthority`'s own
    disabled public constructor, so ANY field change raises `TypeError`
    structurally (Review-A round-5), never silently producing a
    plausible-looking mutated copy that still passes some internal check.
    """
    with pytest.raises(TypeError):
        dataclasses.replace(
            SWING_DISTANCE_INPUT_CONTRACT, input_contract_ref=InputContractRef("invented-contract-id", "v99")
        )
    with pytest.raises(TypeError):
        dataclasses.replace(SWING_DISTANCE_INPUT_CONTRACT, stream_registry_version="v99")
    with pytest.raises(TypeError):
        dataclasses.replace(SWING_DISTANCE_INPUT_CONTRACT, included_streams=frozenset({"an-invented-stream"}))
    with pytest.raises(TypeError):
        dataclasses.replace(SWING_DISTANCE_INPUT_CONTRACT, input_contract_content_id="c" * 64)
    with pytest.raises(TypeError):
        dataclasses.replace(SWING_DISTANCE_INPUT_CONTRACT, stream_registry_content_id="d" * 64)


def test_resolved_authority_carries_genuine_content_identity(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """The default resolved authority actually used by every test engine
    carries genuine, non-empty content-identity proof for both source
    artifacts — real SHA-256 hex digests, not placeholder strings.
    """
    from conftest import REGIME_INPUT_CONTRACT

    for resolved in (SWING_DISTANCE_INPUT_CONTRACT, REGIME_INPUT_CONTRACT):
        assert resolved.input_contract_content_id
        assert resolved.stream_registry_content_id
        assert len(resolved.input_contract_content_id) == 64  # SHA-256 hex digest length
        assert len(resolved.stream_registry_content_id) == 64
    # Both profiles are resolved from the SAME Stream Registry artifact.
    assert SWING_DISTANCE_INPUT_CONTRACT.stream_registry_content_id == REGIME_INPUT_CONTRACT.stream_registry_content_id
    # But from DIFFERENT Input Contract artifacts.
    assert SWING_DISTANCE_INPUT_CONTRACT.input_contract_content_id != REGIME_INPUT_CONTRACT.input_contract_content_id


def test_no_fallback_to_trigger_event_recorded_time(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """The explicit `cursor.recorded_time` is captured verbatim into
    `computation_cursor.recorded_time` — never silently substituted with the
    triggering Candle's or Swing's own `recorded_time`.
    """
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    assert reference.recorded_time != swing.recorded_time

    explicit_r = reference.recorded_time + timedelta(hours=1)
    computed = only_computed(engine.on_candle(reference, cursor=frontier_at(explicit_r))[0])
    assert computed.computation_cursor.recorded_time == explicit_r
    assert computed.computation_cursor.recorded_time != reference.recorded_time
    assert computed.computation_cursor.recorded_time != swing.recorded_time


# --- Review-A residual 4: Chapter 8 §8.5.2 relational invariants ------------


def test_cursor_to_fact_invariant_holds_with_far_future_cursor(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Chapter 8 §8.5.2 Cursor -> Fact: `computation_cursor.recorded_time <=
    FeatureComputed.recorded_time` must hold even when the caller-certified
    cursor's own `recorded_time` is far LATER than every piece of upstream
    evidence — the emitted fact's own recorded_time floor includes
    `cursor.recorded_time` (never merely evidence-derived).
    """
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")

    far_future = reference.recorded_time + timedelta(days=365)
    assert far_future > reference.recorded_time and far_future > swing.recorded_time
    computed = only_computed(engine.on_candle(reference, cursor=frontier_at(far_future))[0])
    assert computed.computation_cursor.recorded_time <= computed.recorded_time
    assert computed.recorded_time > far_future  # strictly later, per the existing RecordedTimeSource doctrine


def test_missing_stream_positions_key_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """ADR-035's cardinality clause: `stream_positions` keys must be EXACTLY
    the bound Input Contract's own `included_streams` — a missing key fails
    closed, never treated as "unbounded"/"not applicable."
    """
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")

    # SWING_STREAM_ID kept sufficient so the Swing is genuinely eligible and a fact
    # would otherwise be emitted — the missing CANDLE_STREAM_ID key (irrelevant to
    # eligibility itself) is what must trip the cardinality check before emission.
    missing_key = frontier_at(
        reference.recorded_time,
        stream_positions={
            SWING_STREAM_ID: StreamPositionProof(sequence=10**9, event_recorded_time=swing.recorded_time)
            # CANDLE_STREAM_ID deliberately omitted.
        },
    )
    with pytest.raises(StreamPositionsUniverseMismatchError):
        engine.on_candle(reference, cursor=missing_key)


def test_extra_stream_positions_key_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """An extra `stream_positions` key beyond `included_streams` — an "all
    streams seen" fallback — must also fail closed, not merely be ignored.
    """
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")

    extra_key = frontier_at(
        reference.recorded_time,
        stream_positions={
            CANDLE_STREAM_ID: StreamPositionProof(sequence=10**9, event_recorded_time=reference.recorded_time),
            SWING_STREAM_ID: StreamPositionProof(sequence=10**9, event_recorded_time=reference.recorded_time),
            "raw-regime-engine-regime": StreamPositionProof(sequence=0, event_recorded_time=None),
        },
    )
    with pytest.raises(StreamPositionsUniverseMismatchError):
        engine.on_candle(reference, cursor=extra_key)


def test_stream_position_event_recorded_after_cursor_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Chapter 8 §8.5.2 Position -> Cursor (anti-look-ahead): a
    `stream_positions` proof whose resolved event `recorded_time` is AFTER
    `cursor.recorded_time` must fail closed — a cursor cannot claim to have
    already observed an event from its own future.
    """
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")

    # The bad proof sits on SWING_STREAM_ID's own position — `sequence` alone (used by
    # eligibility's `is_visible_at_cursor`) is still sufficient for the Swing to be
    # selected, so a fact would otherwise be emitted; the proof's own
    # `event_recorded_time` is what must trip Position -> Cursor before emission.
    from_the_future = frontier_at(
        reference.recorded_time,
        stream_positions={
            CANDLE_STREAM_ID: StreamPositionProof(sequence=10**9, event_recorded_time=reference.recorded_time),
            SWING_STREAM_ID: StreamPositionProof(
                sequence=10**9, event_recorded_time=reference.recorded_time + timedelta(days=1)
            ),
        },
    )
    with pytest.raises(CursorRelationalInvariantViolationError):
        engine.on_candle(reference, cursor=from_the_future)


def test_stream_position_missing_proof_for_non_genesis_sequence_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """A caller-provided integer position alone is not proof (Review-A
    residual 4) — a non-zero `sequence` (not that stream's own
    `genesis_position`) with no `event_recorded_time` proof fails closed.
    """
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")

    # SWING_STREAM_ID carries a non-genesis sequence (10**9, sufficient for eligibility
    # via is_visible_at_cursor) but supplies no event_recorded_time proof at all.
    unproven = frontier_at(
        reference.recorded_time,
        stream_positions={
            CANDLE_STREAM_ID: StreamPositionProof(sequence=10**9, event_recorded_time=reference.recorded_time),
            SWING_STREAM_ID: StreamPositionProof(sequence=10**9, event_recorded_time=None),
        },
    )
    with pytest.raises(CursorRelationalInvariantViolationError):
        engine.on_candle(reference, cursor=unproven)


def test_lifecycle_event_recorded_after_cursor_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Chapter 8 §8.5.2 Lifecycle -> Cursor: a `lifecycle_frontier` whose
    resolved lifecycle event `recorded_time` is AFTER `cursor.recorded_time`
    must fail closed.
    """
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")

    lifecycle_from_the_future = frontier_at(
        reference.recorded_time,
        lifecycle_frontier=LifecycleFrontierProof(
            stream_id="platform-lifecycle",
            position=LifecyclePosition(kind="event", sequence=1),
            event_recorded_time=reference.recorded_time + timedelta(days=1),
        ),
    )
    with pytest.raises(CursorRelationalInvariantViolationError):
        engine.on_candle(reference, cursor=lifecycle_from_the_future)


def test_lifecycle_event_kind_requires_proof_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")

    unproven_event_kind = frontier_at(
        reference.recorded_time,
        lifecycle_frontier=LifecycleFrontierProof(
            stream_id="platform-lifecycle",
            position=LifecyclePosition(kind="event", sequence=1),
            event_recorded_time=None,
        ),
    )
    with pytest.raises(CursorRelationalInvariantViolationError):
        engine.on_candle(reference, cursor=unproven_event_kind)


def test_genesis_lifecycle_frontier_must_not_carry_fabricated_proof_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Chapter 8 §8.3.5's Genesis carve-out: no lifecycle event exists yet for
    `kind: genesis`, so no `event_recorded_time` may be fabricated as if one
    did.
    """
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")

    fabricated_genesis_proof = frontier_at(
        reference.recorded_time,
        lifecycle_frontier=LifecycleFrontierProof(
            stream_id="platform-lifecycle",
            position=LifecyclePosition(kind="genesis", sequence=0),
            event_recorded_time=reference.recorded_time,
        ),
    )
    with pytest.raises(CursorRelationalInvariantViolationError):
        engine.on_candle(reference, cursor=fabricated_genesis_proof)


def test_wrong_lifecycle_stream_id_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")

    wrong_stream = frontier_at(
        reference.recorded_time,
        lifecycle_frontier=LifecycleFrontierProof(
            stream_id="not-the-lifecycle-stream",
            position=LifecyclePosition(kind="genesis", sequence=0),
            event_recorded_time=None,
        ),
    )
    with pytest.raises(CursorRelationalInvariantViolationError):
        engine.on_candle(reference, cursor=wrong_stream)


def test_approved_swing_distance_and_regime_input_contracts_are_accepted(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """The real, currently-approved Input Contract identities for both live
    profiles, resolved via the actual filesystem-backed resolver, are
    accepted — the regime authority is genuinely a DIFFERENT, rejected
    identity for a swing-distance engine (wrong profile).
    """
    from conftest import REGIME_INPUT_CONTRACT

    _engine(
        allocator,
        time_source,
        input_contract_authority_provider=StaticInputContractAuthorityProvider(SWING_DISTANCE_INPUT_CONTRACT),
    )  # must not raise
    with pytest.raises(InputContractIdentityMismatchError):
        _engine(
            allocator,
            time_source,
            input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
        )


# --- Review-A residual 6: immutable cursor snapshot -------------------------


def test_mutating_caller_stream_positions_after_emission_does_not_mutate_cursor(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """A caller mutating the ORIGINAL mutable mapping it passed as
    `stream_positions` after a fact has already been emitted must never
    retroactively alter that fact's own persisted `computation_cursor`
    (Review-A residual 6) — `resolve_computation_cursor` captures an
    immutable snapshot at construction time.
    """
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")

    mutable_positions = {
        CANDLE_STREAM_ID: StreamPositionProof(sequence=10**9, event_recorded_time=reference.recorded_time),
        SWING_STREAM_ID: StreamPositionProof(sequence=10**9, event_recorded_time=reference.recorded_time),
    }
    computed = only_computed(
        engine.on_candle(
            reference, cursor=frontier_at(reference.recorded_time, stream_positions=mutable_positions)
        )[0]
    )
    before = dict(computed.computation_cursor.stream_positions)

    mutable_positions[CANDLE_STREAM_ID] = StreamPositionProof(sequence=1, event_recorded_time=reference.recorded_time)
    mutable_positions["a-newly-injected-stream"] = StreamPositionProof(sequence=1, event_recorded_time=None)

    assert dict(computed.computation_cursor.stream_positions) == before
    with pytest.raises(TypeError):
        computed.computation_cursor.stream_positions["a-newly-injected-stream"] = 1  # type: ignore[index]


# --- P3-FEATURE-A-MAJ-04 remediation: eligible_swing_selection_superseded ----


def test_superseding_swing_already_visible_at_original_raises_computation_defect(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """ADR-034's explicit prohibition: if the higher-priority Swing was ALREADY
    full-cursor-visible at the ORIGINAL fact's own R_original but the original
    computation did not select it, that is a computation/integrity defect —
    never representable as `eligible_swing_selection_superseded`.
    """
    engine = _engine(allocator, time_source)
    swing_a = swing_confirmed_at(allocator, pivot_index=2, swing_id="A", pivot_price="100")
    engine.on_swing_confirmed(swing_a, cursor=frontier_at(swing_a.recorded_time))

    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    r_original = reference.recorded_time + timedelta(minutes=5)
    original = only_computed(engine.on_candle(reference, cursor=frontier_at(r_original))[0])
    assert original.value == Decimal("5.00")  # 105 - 100 (only A eligible so far)

    # B has a HIGHER-priority pivot (later pivot_effective_time.window_start) than A, and its own
    # recorded_time is already <= r_original — i.e. it was already visible when the ORIGINAL
    # computation ran, yet the engine (a stand-in for the original computation) never saw it.
    swing_b = swing_confirmed_at(
        allocator, pivot_index=8, swing_id="B", pivot_price="80", recorded_offset_minutes=0
    )
    assert swing_b.recorded_time <= r_original
    with pytest.raises(EligibleSwingComputationDefectError):
        engine.on_swing_confirmed(swing_b, cursor=frontier_at(r_original + timedelta(minutes=1)))


def test_registry_mismatch_during_supersession_fails_closed_before_emission(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Even once ADR-034's visibility relation is satisfied (superseding Swing
    NOT visible at R_original), the engine still must not emit `eligible_swing_
    selection_superseded` if R_later itself cannot be certified against this
    engine's own bound Input Contract — R_later fails closed exactly like any
    other cursor resolution (P3-FEATURE-A-MAJ-06), never a laundered emission.
    """
    engine = _engine(allocator, time_source)

    swing_a1 = swing_confirmed_at(allocator, pivot_index=8, swing_id="A", swing_revision=1, pivot_price="100")
    engine.on_swing_confirmed(swing_a1, cursor=frontier_at(swing_a1.recorded_time))
    swing_b = swing_confirmed_at(
        allocator, pivot_index=2, swing_id="B", swing_revision=1, pivot_price="80", recorded_offset_minutes=10
    )
    engine.on_swing_confirmed(swing_b, cursor=frontier_at(swing_b.recorded_time))

    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))

    inv_a1 = swing_invalidated_at(allocator, swing_id="A", swing_revision=1, recorded_time=BASE + timedelta(minutes=20))
    engine.on_swing_invalidated(inv_a1, cursor=frontier_at(inv_a1.recorded_time))

    swing_a2 = swing_confirmed_at(
        allocator, pivot_index=8, swing_id="A", swing_revision=2, pivot_price="103", recorded_offset_minutes=30
    )
    mismatched = dataclasses.replace(
        frontier_at(swing_a2.recorded_time), stream_registry_version="a-different-registry-version"
    )
    with pytest.raises(RegistryContractMismatchError):
        engine.on_swing_confirmed(swing_a2, cursor=mismatched)


def test_candidate_that_does_not_win_total_order_causes_no_invalidation(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """A newly-visible Swing that remains eligible but does NOT win the
    deterministic total order over the currently-used Swing must never
    trigger an invalidation/replacement — no repaint on a losing candidate.
    """
    engine = _engine(allocator, time_source)
    swing_a = swing_confirmed_at(allocator, pivot_index=8, swing_id="A", pivot_price="100")
    engine.on_swing_confirmed(swing_a, cursor=frontier_at(swing_a.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    original = only_computed(engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])

    # C has a LOWER-priority pivot (earlier pivot_effective_time.window_start) than A — remains
    # eligible but never wins the total order, so the settled A-based window must not repaint.
    swing_c = swing_confirmed_at(
        allocator, pivot_index=2, swing_id="C", pivot_price="80", recorded_offset_minutes=10
    )
    events = engine.on_swing_confirmed(swing_c, cursor=frontier_at(swing_c.recorded_time + timedelta(minutes=1)))
    assert events == []
    assert original.value == Decimal("5.00")


def test_used_swing_itself_invalidated_uses_swing_invalidated_cause(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """When the CURRENTLY-selected Swing itself is explicitly invalidated (as
    opposed to being out-competed by a newly-visible higher-priority Swing),
    the resulting invalidation must use `swing_invalidated` — never
    `eligible_swing_selection_superseded`, since no supersession occurred.
    """
    # P3-PY-MUT-STEP9-A field-completeness remediation (EVID-03,
    # constructed_object_field_not_independently_asserted): every
    # constructor-set field of `_invalidate_and_reattempt`'s returned
    # `FeatureFactInvalidated` is now independently asserted, not just
    # `.invalidation_cause` as before.
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    original = only_computed(engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])

    inv = swing_invalidated_at(allocator, swing_id="s1", swing_revision=1, recorded_time=BASE + timedelta(minutes=20))
    events = engine.on_swing_invalidated(inv, cursor=frontier_at(inv.recorded_time))
    assert len(events) == 1  # invalidation only — no other eligible Swing exists
    invalidation = only_invalidated(events[0])
    assert invalidation.invalidation_cause == "swing_invalidated"
    assert invalidation.scope == original.scope
    assert invalidation.invalidated_fact_ref == original.ref
    assert invalidation.window_start == original.window_start
    assert invalidation.window_end == original.window_end
    assert invalidation.causation_refs == (original.ref, inv.ref)
    assert invalidation.recorded_time >= inv.recorded_time
    assert invalidation.ref.stream_id == "feature"
    assert invalidation.event_contract_ref == EventContractRef(
        FEATURE_FACT_INVALIDATED_CONTRACT_ID, FEATURE_OUTPUT_CONTRACT_VERSION
    )
    assert invalidation.computation_cursor.recorded_time == inv.recorded_time


# --- Review-A round-2 residual 2: failure atomicity -------------------------
#
# A rejected/invalid `EvaluationFrontier` must never leave the engine in a
# state that changes the outcome of a later valid retry of the exact same
# authoritative event — cursor certification happens at the public-method
# boundary, BEFORE any state mutation (`_resolve_cursor(cursor)` as the
# first statement of every public ingestion method).


def _fresh_clean_engine() -> tuple[SwingDistanceFeatureEngine, SequenceAllocator]:
    """A brand-new engine + allocator using the SAME `run_id`/`module_id`/
    `implementation_version` as the `allocator` fixture — when driven through
    an IDENTICAL sequence of successful operations, its own ref/event_id
    allocation advances in perfect lockstep, making full dataclass equality
    against the "contaminated-then-retried" engine's own output a valid,
    exact proof of equivalence (not just field-by-field spot checks).
    """
    clean_allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="test-run")
    return _engine(clean_allocator, FixedDeltaTimeSource()), clean_allocator


def test_swing_confirmed_supersession_retry_after_invalid_frontier_is_deterministic(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """The exact A1 -> A1 invalidated -> B becomes VALID winner -> A2 first
    attempted with an invalid R_later -> fail with no state contamination ->
    SAME A2 retried at a valid R_later -> eligible_swing_selection_superseded
    -> replacement using A2 sequence (MAJ-04 dependency). The rejected
    attempt allocates NO sequence/ref for Feature output and appends NOTHING
    to Swing history, so the valid retry — and its full resulting output —
    is byte-for-byte identical to a clean engine that only ever saw the
    valid attempt.
    """
    engine = _engine(allocator, time_source)

    swing_a1 = swing_confirmed_at(allocator, pivot_index=8, swing_id="A", swing_revision=1, pivot_price="100")
    engine.on_swing_confirmed(swing_a1, cursor=frontier_at(swing_a1.recorded_time))
    swing_b = swing_confirmed_at(
        allocator, pivot_index=2, swing_id="B", swing_revision=1, pivot_price="80", recorded_offset_minutes=10
    )
    engine.on_swing_confirmed(swing_b, cursor=frontier_at(swing_b.recorded_time))

    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    original = only_computed(engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])
    assert original.value == Decimal("5.00")

    inv_a1 = swing_invalidated_at(allocator, swing_id="A", swing_revision=1, recorded_time=BASE + timedelta(minutes=20))
    temp_events = engine.on_swing_invalidated(inv_a1, cursor=frontier_at(inv_a1.recorded_time))
    temporary = only_computed(temp_events[1])
    assert temporary.value == Decimal("25.00")

    swing_a2 = swing_confirmed_at(
        allocator, pivot_index=8, swing_id="A", swing_revision=2, pivot_price="103", recorded_offset_minutes=30
    )

    # 1. Invalid R_later must fail closed and must NOT contaminate Swing history.
    with pytest.raises(RegistryContractMismatchError):
        engine.on_swing_confirmed(swing_a2, cursor=_invalid_frontier(swing_a2.recorded_time))
    latest_a = engine._latest_confirmation("A")
    assert latest_a is not None
    assert latest_a.revision == 1  # A2 was NOT appended by the rejected attempt

    # 2. The SAME A2 event retried with a valid frontier succeeds normally.
    preempt_events = engine.on_swing_confirmed(swing_a2, cursor=frontier_at(swing_a2.recorded_time))
    assert len(preempt_events) == 2
    invalidation = only_invalidated(preempt_events[0])
    assert invalidation.invalidated_fact_ref == temporary.ref
    assert invalidation.invalidation_cause == "eligible_swing_selection_superseded"
    assert invalidation.causation_refs == (temporary.ref, swing_a2.ref)
    final = only_computed(preempt_events[1])
    assert final.supersedes_fact_ref == temporary.ref
    assert final.value == Decimal("2.00")

    # 3. Full equivalence against a clean engine that only ever saw the valid attempt.
    clean_engine, clean_allocator = _fresh_clean_engine()
    c_swing_a1 = swing_confirmed_at(clean_allocator, pivot_index=8, swing_id="A", swing_revision=1, pivot_price="100")
    clean_engine.on_swing_confirmed(c_swing_a1, cursor=frontier_at(c_swing_a1.recorded_time))
    c_swing_b = swing_confirmed_at(
        clean_allocator, pivot_index=2, swing_id="B", swing_revision=1, pivot_price="80", recorded_offset_minutes=10
    )
    clean_engine.on_swing_confirmed(c_swing_b, cursor=frontier_at(c_swing_b.recorded_time))
    c_reference = candle_at(clean_allocator, 10, high="110", low="90", close="105")
    clean_engine.on_candle(c_reference, cursor=frontier_at(c_reference.recorded_time))
    c_inv_a1 = swing_invalidated_at(
        clean_allocator, swing_id="A", swing_revision=1, recorded_time=BASE + timedelta(minutes=20)
    )
    clean_engine.on_swing_invalidated(c_inv_a1, cursor=frontier_at(c_inv_a1.recorded_time))
    c_swing_a2 = swing_confirmed_at(
        clean_allocator, pivot_index=8, swing_id="A", swing_revision=2, pivot_price="103", recorded_offset_minutes=30
    )
    clean_preempt_events = clean_engine.on_swing_confirmed(c_swing_a2, cursor=frontier_at(c_swing_a2.recorded_time))
    clean_invalidation = only_invalidated(clean_preempt_events[0])
    clean_final = only_computed(clean_preempt_events[1])

    assert invalidation == clean_invalidation
    assert final == clean_final


def test_swing_invalidated_retry_after_invalid_frontier_is_deterministic(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Submitting a SwingInvalidated first with an invalid frontier must fail
    WITHOUT marking the targeted revision as invalidated — the exact same
    invalidation retried afterward with a valid frontier produces normal
    `swing_invalidated` behavior, identical to a clean engine.
    """
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    original = only_computed(engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])

    inv = swing_invalidated_at(allocator, swing_id="s1", swing_revision=1, recorded_time=BASE + timedelta(minutes=20))

    with pytest.raises(RegistryContractMismatchError):
        engine.on_swing_invalidated(inv, cursor=_invalid_frontier(inv.recorded_time))
    assert (inv.swing_id, inv.swing_revision) not in engine._swing_invalidations  # not poisoned by the rejection

    events = engine.on_swing_invalidated(inv, cursor=frontier_at(inv.recorded_time))
    assert len(events) == 1
    invalidation = only_invalidated(events[0])
    assert invalidation.invalidation_cause == "swing_invalidated"
    assert invalidation.invalidated_fact_ref == original.ref

    clean_engine, clean_allocator = _fresh_clean_engine()
    c_swing = swing_confirmed_at(clean_allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    clean_engine.on_swing_confirmed(c_swing, cursor=frontier_at(c_swing.recorded_time))
    c_reference = candle_at(clean_allocator, 10, high="110", low="90", close="105")
    clean_engine.on_candle(c_reference, cursor=frontier_at(c_reference.recorded_time))
    c_inv = swing_invalidated_at(
        clean_allocator, swing_id="s1", swing_revision=1, recorded_time=BASE + timedelta(minutes=20)
    )
    clean_events = clean_engine.on_swing_invalidated(c_inv, cursor=frontier_at(c_inv.recorded_time))
    clean_invalidation = only_invalidated(clean_events[0])

    assert invalidation == clean_invalidation


def test_candle_original_retry_after_invalid_frontier_is_deterministic(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Submitting a brand-new Candle first with an invalid frontier must fail
    WITHOUT entering it into Candle dedup/routing state — the exact same
    Candle ref/content retried with a valid frontier is treated as a genuine
    first-time ingestion, emitting `FeatureComputed` exactly as a clean
    engine would.
    """
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")

    with pytest.raises(RegistryContractMismatchError):
        engine.on_candle(reference, cursor=_invalid_frontier(reference.recorded_time))
    assert engine._candle_index == {}  # rejected attempt did not enter Candle dedup state

    events = engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))
    assert len(events) == 1
    computed = only_computed(events[0])
    assert computed.value == Decimal("5.00")

    clean_engine, clean_allocator = _fresh_clean_engine()
    c_swing = swing_confirmed_at(clean_allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    clean_engine.on_swing_confirmed(c_swing, cursor=frontier_at(c_swing.recorded_time))
    c_reference = candle_at(clean_allocator, 10, high="110", low="90", close="105")
    clean_events = clean_engine.on_candle(c_reference, cursor=frontier_at(c_reference.recorded_time))
    clean_computed = only_computed(clean_events[0])

    assert computed == clean_computed


def test_candle_correction_retry_after_invalid_frontier_is_deterministic(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Submitting a CandleCorrected first with an invalid frontier must fail
    WITHOUT overwriting the cached Candle — the exact same correction ref/
    content retried with a valid frontier invalidates-and-replaces exactly
    once, identical to a clean engine.
    """
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    original = only_computed(engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])

    correction = dataclasses.replace(
        reference,
        ref=allocator.next_ref(CANDLE_STREAM_ID),
        recorded_time=reference.recorded_time + timedelta(seconds=120),
        is_correction=True,
        event_contract_ref=EventContractRef(CANDLE_CORRECTED_CONTRACT_ID, CONTRACT_VERSION),
    )

    with pytest.raises(RegistryContractMismatchError):
        engine.on_candle(correction, cursor=_invalid_frontier(correction.recorded_time))
    # The rejected attempt must not have overwritten the cached Candle with the correction.
    cached = engine._candles[engine._candle_index[reference.scope.subject_id]]
    assert cached.ref == reference.ref

    events = engine.on_candle(correction, cursor=frontier_at(correction.recorded_time))
    assert len(events) == 2
    replacement = only_computed(events[1])
    assert replacement.value == original.value
    assert replacement.supersedes_fact_ref == original.ref

    clean_engine, clean_allocator = _fresh_clean_engine()
    c_swing = swing_confirmed_at(clean_allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    clean_engine.on_swing_confirmed(c_swing, cursor=frontier_at(c_swing.recorded_time))
    c_reference = candle_at(clean_allocator, 10, high="110", low="90", close="105")
    clean_engine.on_candle(c_reference, cursor=frontier_at(c_reference.recorded_time))
    c_correction = dataclasses.replace(
        c_reference,
        ref=clean_allocator.next_ref(CANDLE_STREAM_ID),
        recorded_time=c_reference.recorded_time + timedelta(seconds=120),
        is_correction=True,
        event_contract_ref=EventContractRef(CANDLE_CORRECTED_CONTRACT_ID, CONTRACT_VERSION),
    )
    clean_events = clean_engine.on_candle(c_correction, cursor=frontier_at(c_correction.recorded_time))
    clean_replacement = only_computed(clean_events[1])

    assert replacement == clean_replacement


def test_invalid_frontier_rejected_even_when_no_output_would_result(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Even when NO eligible Swing exists (a valid absence that would
    ordinarily emit nothing), a malformed frontier presented as the
    certified computation frontier for this operation must still be
    rejected at the public boundary — never allowed to slip through merely
    because no lineage exists yet to trigger `_resolve_cursor` deep inside
    emission.
    """
    engine = _engine(allocator, time_source)
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    with pytest.raises(RegistryContractMismatchError):
        engine.on_candle(reference, cursor=_invalid_frontier(reference.recorded_time))
    # Confirm the valid-absence path genuinely would have produced no output.
    assert engine.on_candle(reference, cursor=frontier_at(reference.recorded_time)) == []
