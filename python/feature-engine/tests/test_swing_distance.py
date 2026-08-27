from __future__ import annotations

import dataclasses
from datetime import timedelta
from decimal import Decimal
from typing import Any

import pytest
from conftest import (
    BASE,
    CONTRACT_VERSION,
    FEATURE_OUTPUT_CONTRACT_VERSION,
    INCLUDED_STREAMS,
    INPUT_CONTRACT_REF,
    STREAM_REGISTRY_VERSION,
    FixedDeltaTimeSource,
    authorized_candle_contract_refs,
    authorized_swing_contract_refs,
    candle_at,
    feature_scope,
    frontier_at,
    make_distance_definition,
    only_computed,
    only_invalidated,
    swing_confirmed_at,
    swing_invalidated_at,
)

from feature_engine import (
    CANDLE_CORRECTED_CONTRACT_ID,
    ComputationCursor,
    EventContractRef,
    InputContractRef,
    LifecycleFrontier,
    LifecyclePosition,
    SequenceAllocator,
    SwingDistanceFeatureEngine,
)
from feature_engine.errors import (
    EligibleSwingComputationDefectError,
    EvidenceReferenceConflictError,
    InvalidSwingEligibilityInputError,
    RegistryContractMismatchError,
    UnauthorizedUpstreamContractError,
    UnresolvedComputationCursorAuthorityError,
    UnsupportedDistanceRepresentationError,
)


def _engine(
    allocator: SequenceAllocator,
    time_source: FixedDeltaTimeSource,
    *,
    input_contract_ref: InputContractRef = INPUT_CONTRACT_REF,
    stream_registry_version: str = STREAM_REGISTRY_VERSION,
    included_streams: frozenset[str] = INCLUDED_STREAMS,
    **definition_kwargs: Any,
) -> SwingDistanceFeatureEngine:
    definition = make_distance_definition(**definition_kwargs)
    scope = feature_scope("distance_to_last_confirmed_swing", version=definition.feature_definition_version)
    return SwingDistanceFeatureEngine(
        scope,
        definition,
        allocator,
        time_source,
        feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
        authorized_candle_contract_refs=authorized_candle_contract_refs(),
        authorized_swing_contract_refs=authorized_swing_contract_refs(),
        input_contract_ref=input_contract_ref,
        stream_registry_version=stream_registry_version,
        included_streams=included_streams,
    )


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
    absolute_engine = _engine(allocator, time_source, distance_representation="absolute")
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="110")
    absolute_engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    computed = only_computed(absolute_engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])
    assert computed.value == Decimal("5.00")  # |105 - 110|
    assert set(computed.input_fact_refs) == {reference.ref, swing.ref}


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
            input_contract_ref=INPUT_CONTRACT_REF,
            stream_registry_version=STREAM_REGISTRY_VERSION,
            included_streams=INCLUDED_STREAMS,
        )


# --- P3-FEATURE-A-MAJ-05 remediation: dedup is ref-identity-only -------------


def test_candle_distinct_correction_ref_enters_lineage_even_when_value_unchanged(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    original = only_computed(engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))[0])

    correction = dataclasses.replace(
        reference,
        ref=allocator.next_ref("candle"),
        recorded_time=reference.recorded_time + timedelta(seconds=120),
        is_correction=True,
        event_contract_ref=EventContractRef(CANDLE_CORRECTED_CONTRACT_ID, CONTRACT_VERSION),
    )
    events = engine.on_candle(correction, cursor=frontier_at(correction.recorded_time))
    assert len(events) == 2
    replacement = only_computed(events[1])
    assert replacement.value == original.value
    assert replacement.supersedes_fact_ref == original.ref
    assert replacement.ref != original.ref


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
    assert cursor.input_contract_ref == INPUT_CONTRACT_REF
    assert cursor.stream_registry_version == STREAM_REGISTRY_VERSION
    assert cursor.lifecycle_frontier == LifecycleFrontier(
        stream_id="platform-lifecycle", position=LifecyclePosition(kind="genesis", sequence=0)
    )
    assert dict(cursor.stream_positions) == dict.fromkeys(INCLUDED_STREAMS, 10**9)

    correction = dataclasses.replace(
        reference,
        ref=allocator.next_ref("candle"),
        recorded_time=r + timedelta(seconds=120),
        is_correction=True,
        event_contract_ref=EventContractRef(CANDLE_CORRECTED_CONTRACT_ID, CONTRACT_VERSION),
    )
    invalidation = only_invalidated(engine.on_candle(correction, cursor=frontier_at(correction.recorded_time))[0])
    inv_cursor = invalidation.computation_cursor
    assert inv_cursor.recorded_time == correction.recorded_time
    assert inv_cursor.input_contract_ref == INPUT_CONTRACT_REF
    assert inv_cursor.stream_registry_version == STREAM_REGISTRY_VERSION


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
        ref=allocator.next_ref("candle"),
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
        stream_positions={"candle": 10**9, "swing": swing.ref.sequence - 1, "regime": 10**9},
    )
    assert below_engine.on_candle(reference, cursor=below_ceiling) == []

    at_engine = _engine(allocator, time_source)
    at_engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    at_ceiling = frontier_at(
        reference.recorded_time,
        stream_positions={"candle": 10**9, "swing": swing.ref.sequence, "regime": 10**9},
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

    distinctive = LifecycleFrontier(
        stream_id="platform-lifecycle", position=LifecyclePosition(kind="event", sequence=42)
    )
    computed = only_computed(
        engine.on_candle(reference, cursor=frontier_at(reference.recorded_time, lifecycle_frontier=distinctive))[0]
    )
    assert computed.computation_cursor.lifecycle_frontier == distinctive


def test_registry_mismatch_fails_closed_before_emission(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source, stream_registry_version=STREAM_REGISTRY_VERSION)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    mismatched = frontier_at(reference.recorded_time, stream_registry_version="a-different-registry-version")
    with pytest.raises(RegistryContractMismatchError):
        engine.on_candle(reference, cursor=mismatched)


def test_missing_input_contract_ref_fails_closed_at_construction(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        _engine(allocator, time_source, input_contract_ref=InputContractRef("", ""))


def test_missing_stream_registry_version_fails_closed_at_construction(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        _engine(allocator, time_source, stream_registry_version="")


def test_missing_included_streams_fails_closed_at_construction(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        _engine(allocator, time_source, included_streams=frozenset())


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
    engine = _engine(allocator, time_source, stream_registry_version=STREAM_REGISTRY_VERSION)

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
    mismatched = frontier_at(swing_a2.recorded_time, stream_registry_version="a-different-registry-version")
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
    engine = _engine(allocator, time_source)
    swing = swing_confirmed_at(allocator, pivot_index=2, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference = candle_at(allocator, 10, high="110", low="90", close="105")
    engine.on_candle(reference, cursor=frontier_at(reference.recorded_time))

    inv = swing_invalidated_at(allocator, swing_id="s1", swing_revision=1, recorded_time=BASE + timedelta(minutes=20))
    events = engine.on_swing_invalidated(inv, cursor=frontier_at(inv.recorded_time))
    assert len(events) == 1  # invalidation only — no other eligible Swing exists
    invalidation = only_invalidated(events[0])
    assert invalidation.invalidation_cause == "swing_invalidated"
