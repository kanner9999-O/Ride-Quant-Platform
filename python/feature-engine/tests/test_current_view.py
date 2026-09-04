from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from conftest import (
    BASE,
    CONTRACT_VERSION,
    SWING_DISTANCE_INPUT_CONTRACT,
    feature_scope,
)

from feature_engine import (
    FEATURE_COMPUTED_CONTRACT_ID,
    FEATURE_FACT_INVALIDATED_CONTRACT_ID,
    ComputationCursor,
    EffectiveWindow,
    EventContractRef,
    FeatureCurrentView,
    FeatureScope,
    LifecycleFrontier,
    LifecyclePosition,
    SequenceAllocator,
)
from feature_engine.contracts import FeatureComputed, FeatureFactInvalidated
from feature_engine.errors import FeatureLineageError, ForeignScopeError

_COMPUTED_CONTRACT_REF = EventContractRef(FEATURE_COMPUTED_CONTRACT_ID, CONTRACT_VERSION)
_INVALIDATED_CONTRACT_REF = EventContractRef(FEATURE_FACT_INVALIDATED_CONTRACT_ID, CONTRACT_VERSION)

# `FeatureCurrentView` is a pure projection over `.scope`/window/lineage fields
# only — it never reads `computation_cursor` — so a single fixed test-fixture
# value here is sufficient for every fact constructed in this file.
_CURSOR = ComputationCursor(
    recorded_time=BASE,
    input_contract_ref=SWING_DISTANCE_INPUT_CONTRACT.input_contract_ref,
    stream_registry_version=SWING_DISTANCE_INPUT_CONTRACT.stream_registry_version,
    lifecycle_frontier=LifecycleFrontier(
        stream_id="platform-lifecycle", position=LifecyclePosition(kind="genesis", sequence=0)
    ),
    stream_positions=dict.fromkeys(SWING_DISTANCE_INPUT_CONTRACT.included_streams, 10**9),
)


def _window(index: int) -> tuple[datetime, datetime]:
    start = BASE + timedelta(minutes=index)
    return start, start + timedelta(minutes=1)


def _computed(
    allocator: SequenceAllocator,
    scope: FeatureScope,
    index: int,
    *,
    value: str = "1.00",
    supersedes: object = None,
    recorded_offset_minutes: int = 0,
) -> FeatureComputed:
    start, end = _window(index)
    input_ref = allocator.next_ref("candle")
    return FeatureComputed(
        scope=scope,
        value=Decimal(value),
        unit="price",
        window_start=start,
        window_end=end,
        input_fact_refs=(input_ref,),
        supersedes_fact_ref=supersedes,  # type: ignore[arg-type]
        causation_refs=(input_ref,),
        recorded_time=end + timedelta(minutes=recorded_offset_minutes),
        ref=allocator.next_ref("feature"),
        event_contract_ref=_COMPUTED_CONTRACT_REF,
        computation_cursor=_CURSOR,
    )


def _invalidated(
    allocator: SequenceAllocator,
    scope: FeatureScope,
    target: FeatureComputed,
    *,
    recorded_offset_minutes: int = 1,
) -> FeatureFactInvalidated:
    return FeatureFactInvalidated(
        scope=scope,
        invalidated_fact_ref=target.ref,
        invalidation_cause="candle_corrected",
        window_start=target.window_start,
        window_end=target.window_end,
        causation_refs=(target.ref,),
        recorded_time=target.recorded_time + timedelta(minutes=recorded_offset_minutes),
        ref=allocator.next_ref("feature"),
        event_contract_ref=_INVALIDATED_CONTRACT_REF,
        computation_cursor=_CURSOR,
    )


# --- 19. FeatureCurrentView ----------------------------------------------------


def test_no_row_before_first_computation(allocator: SequenceAllocator) -> None:
    scope = feature_scope("volatility_metric", version="fd-1")
    view = FeatureCurrentView(scope)
    assert view.current() is None


def test_valid_after_first_computation(allocator: SequenceAllocator) -> None:
    # P3-PY-MUT-STEP9-A field-completeness remediation (EVID-03,
    # constructed_object_field_not_independently_asserted): every field of
    # the returned `FeatureViewResult` is independently asserted against its
    # authoritative expected value, not merely `view_state`/`value` as
    # before -- `feature_subject_id`/`scope` are the view's own construction
    # identity, `unit`/`effective_window` are carried verbatim from the head
    # fact, and `last_recorded_time` is the head fact's own recorded_time.
    scope = feature_scope("volatility_metric", version="fd-1")
    view = FeatureCurrentView(scope)
    fact = _computed(allocator, scope, 0)
    view.on_feature_computed(fact)
    result = view.current()
    assert result is not None
    assert result.view_state == "VALID"
    assert result.feature_subject_id == scope.feature_subject_id
    assert result.scope == scope
    assert result.value == Decimal("1.00")
    assert result.unit == fact.unit
    assert result.effective_window == EffectiveWindow(fact.window_start, fact.window_end)
    assert result.lineage_head_fact_ref == fact.ref
    assert result.last_recorded_time == fact.recorded_time


def test_pending_correction_never_falls_back_to_older_window(allocator: SequenceAllocator) -> None:
    scope = feature_scope("volatility_metric", version="fd-1")
    view = FeatureCurrentView(scope)

    older = _computed(allocator, scope, 0)
    view.on_feature_computed(older)

    newest = _computed(allocator, scope, 1, recorded_offset_minutes=1)
    view.on_feature_computed(newest)

    invalidation = _invalidated(allocator, scope, newest)
    view.on_feature_invalidated(invalidation)

    # P3-PY-MUT-STEP9-A field-completeness remediation (EVID-03): the
    # PENDING_CORRECTION branch's own feature_subject_id/scope/
    # last_recorded_time fields, previously unasserted, are exactly as
    # authoritative as the VALID branch's -- last_recorded_time in
    # particular must reflect the INVALIDATION's own recorded_time
    # (`on_feature_invalidated`'s state mutation), not the superseded
    # computation's.
    result = view.current()
    assert result is not None
    assert result.view_state == "PENDING_CORRECTION"
    assert result.feature_subject_id == scope.feature_subject_id
    assert result.scope == scope
    assert result.value is None
    assert result.effective_window is None
    assert result.lineage_head_fact_ref is None
    assert result.last_recorded_time == invalidation.recorded_time


def test_pending_correction_resolves_on_replacement(allocator: SequenceAllocator) -> None:
    scope = feature_scope("volatility_metric", version="fd-1")
    view = FeatureCurrentView(scope)

    original = _computed(allocator, scope, 0)
    view.on_feature_computed(original)
    invalidation = _invalidated(allocator, scope, original)
    view.on_feature_invalidated(invalidation)
    pending = view.current()
    assert pending is not None
    assert pending.view_state == "PENDING_CORRECTION"

    replacement = _computed(allocator, scope, 0, value="1.50", supersedes=original.ref, recorded_offset_minutes=2)
    view.on_feature_computed(replacement)
    result = view.current()
    assert result is not None
    assert result.view_state == "VALID"
    assert result.value == Decimal("1.50")
    assert result.lineage_head_fact_ref == replacement.ref
    # P3-PY-MUT-STEP9-A field-completeness remediation (EVID-03):
    # `on_feature_computed`'s replacement branch must reset
    # `last_recorded_time` to the REPLACEMENT's own recorded_time, not
    # leave the invalidation's (or the original's) stale value in place.
    assert result.last_recorded_time == replacement.recorded_time


# --- Scope/lineage rejection guards (P3-FEATURE-QG-COV-01 remediation) -----
#
# Every test above only ever feeds `FeatureCurrentView` events that
# genuinely belong to its own construction scope, in the exact valid
# lineage order (original -> invalidation -> replacement) — so none of
# `_check_scope`'s `ForeignScopeError` or the four `on_feature_computed`/
# `on_feature_invalidated` lineage-mismatch `FeatureLineageError` guards
# were ever triggered. Each guard below is feature.md §5/§11's own
# UNCOMPUTED -> COMPUTED state-machine integrity check (I-13) — a caller
# violating lineage order/scope must be rejected, never silently accepted.


def test_foreign_scope_event_rejected(allocator: SequenceAllocator) -> None:
    scope = feature_scope("volatility_metric", version="fd-1")
    other_scope = feature_scope("volatility_metric", version="fd-2")
    view = FeatureCurrentView(scope)
    foreign_fact = _computed(allocator, other_scope, 0)
    with pytest.raises(ForeignScopeError):
        view.on_feature_computed(foreign_fact)


def test_duplicate_original_computation_for_same_window_rejected(allocator: SequenceAllocator) -> None:
    scope = feature_scope("volatility_metric", version="fd-1")
    view = FeatureCurrentView(scope)
    first = _computed(allocator, scope, 0)
    view.on_feature_computed(first)
    second_original = _computed(allocator, scope, 0, value="2.00", recorded_offset_minutes=1)
    with pytest.raises(FeatureLineageError, match="original FeatureComputed for already-computed window"):
        view.on_feature_computed(second_original)


def test_replacement_with_wrong_supersedes_ref_rejected(allocator: SequenceAllocator) -> None:
    scope = feature_scope("volatility_metric", version="fd-1")
    view = FeatureCurrentView(scope)
    original = _computed(allocator, scope, 0)
    view.on_feature_computed(original)
    invalidation = _invalidated(allocator, scope, original)
    view.on_feature_invalidated(invalidation)
    bogus_replacement = _computed(allocator, scope, 0, value="1.50", supersedes=object(), recorded_offset_minutes=2)
    with pytest.raises(FeatureLineageError, match="does not match the current"):
        view.on_feature_computed(bogus_replacement)


def test_replacement_before_invalidation_rejected(allocator: SequenceAllocator) -> None:
    scope = feature_scope("volatility_metric", version="fd-1")
    view = FeatureCurrentView(scope)
    original = _computed(allocator, scope, 0)
    view.on_feature_computed(original)
    premature_replacement = _computed(
        allocator, scope, 0, value="1.50", supersedes=original.ref, recorded_offset_minutes=1
    )
    with pytest.raises(FeatureLineageError, match="arrived before its invalidation"):
        view.on_feature_computed(premature_replacement)


def test_invalidation_with_wrong_target_ref_rejected(allocator: SequenceAllocator) -> None:
    scope = feature_scope("volatility_metric", version="fd-1")
    view = FeatureCurrentView(scope)
    original = _computed(allocator, scope, 0)
    view.on_feature_computed(original)
    unrelated = _computed(allocator, scope, 1, recorded_offset_minutes=1)
    bogus_invalidation = _invalidated(allocator, scope, unrelated)
    with pytest.raises(FeatureLineageError, match="does not match the current lineage head"):
        view.on_feature_invalidated(bogus_invalidation)


def test_double_invalidation_rejected(allocator: SequenceAllocator) -> None:
    scope = feature_scope("volatility_metric", version="fd-1")
    view = FeatureCurrentView(scope)
    original = _computed(allocator, scope, 0)
    view.on_feature_computed(original)
    invalidation = _invalidated(allocator, scope, original)
    view.on_feature_invalidated(invalidation)
    second_invalidation = _invalidated(allocator, scope, original, recorded_offset_minutes=2)
    with pytest.raises(FeatureLineageError, match="already invalidated"):
        view.on_feature_invalidated(second_invalidation)
