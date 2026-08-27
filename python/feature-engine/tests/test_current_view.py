from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal

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
    EventContractRef,
    FeatureCurrentView,
    FeatureScope,
    LifecycleFrontier,
    LifecyclePosition,
    SequenceAllocator,
)
from feature_engine.contracts import FeatureComputed, FeatureFactInvalidated

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
    scope = feature_scope("volatility_metric", version="fd-1")
    view = FeatureCurrentView(scope)
    fact = _computed(allocator, scope, 0)
    view.on_feature_computed(fact)
    result = view.current()
    assert result is not None
    assert result.view_state == "VALID"
    assert result.value == Decimal("1.00")
    assert result.lineage_head_fact_ref == fact.ref


def test_pending_correction_never_falls_back_to_older_window(allocator: SequenceAllocator) -> None:
    scope = feature_scope("volatility_metric", version="fd-1")
    view = FeatureCurrentView(scope)

    older = _computed(allocator, scope, 0)
    view.on_feature_computed(older)

    newest = _computed(allocator, scope, 1, recorded_offset_minutes=1)
    view.on_feature_computed(newest)

    invalidation = _invalidated(allocator, scope, newest)
    view.on_feature_invalidated(invalidation)

    result = view.current()
    assert result is not None
    assert result.view_state == "PENDING_CORRECTION"
    assert result.value is None
    assert result.effective_window is None
    assert result.lineage_head_fact_ref is None


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
