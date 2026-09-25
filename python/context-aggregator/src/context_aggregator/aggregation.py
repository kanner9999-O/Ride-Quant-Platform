"""The Context Aggregator public entrypoint (context.md §8/§9/§10/§17).

`aggregate_context_candidate` is the ONLY function this package's public
surface expects downstream orchestration to call. It selects, from an
already cursor-visible candidate set, the Eligible Upstream Fact for each of
the seven required roles (§8), enforces exact seven-role cardinality with a
fail-closed `None` result on any gap (§9), and assembles an eligible
cursor-bounded `ContextAggregationCandidate` by copying upstream values
verbatim (§17) — never recomputing Structure/Regime/Feature semantics.

**Explicit computation-point binding (CONTEXT-CORE-A-MAJ-01):** the caller
MUST pass `target_computation_point_ref`, naming the exact visible Candle
fact this aggregation attempt is for. This core resolves the Candle role
ONLY for that fact's own window — an unrelated, merely-newer Candle window
never wins instead (see `select_candle`'s docstring).

See `selection.py`'s module docstring for the explicit cursor-visibility
boundary this core respects (recorded-time visibility is the caller's
responsibility; every other Context-owned predicate is enforced here).
"""

from __future__ import annotations

from collections.abc import Sequence, Set

from context_aggregator.definition import ContextDefinition
from context_aggregator.errors import (
    DuplicateFactReferenceError,
    RegimeClassTypeMismatchError,
    ScopeDefinitionMismatchError,
)
from context_aggregator.evidence import (
    CandleFact,
    DirectionalPersistenceRegimeClass,
    FeatureFact,
    FeatureType,
    RegimeDimension,
    RegimeFact,
    StructureFact,
    VolatilityRegimeClass,
)
from context_aggregator.refs import EventRecordRef
from context_aggregator.scope import ContextSubjectScope
from context_aggregator.selection import (
    normalize_input_fact_refs,
    select_candle,
    select_feature,
    select_regime,
    select_structure,
)
from context_aggregator.values import ContextAggregationCandidate, ContextValues


def aggregate_context_candidate(
    *,
    scope: ContextSubjectScope,
    definition: ContextDefinition,
    target_computation_point_ref: EventRecordRef,
    candle_candidates: Sequence[CandleFact],
    structure_candidates: Sequence[StructureFact],
    volatility_regime_candidates: Sequence[RegimeFact],
    directional_persistence_regime_candidates: Sequence[RegimeFact],
    volatility_metric_candidates: Sequence[FeatureFact],
    directional_persistence_metric_candidates: Sequence[FeatureFact],
    distance_to_last_confirmed_swing_candidates: Sequence[FeatureFact],
    structure_invalidated_refs: Set[EventRecordRef] = frozenset(),
    volatility_regime_invalidated_refs: Set[EventRecordRef] = frozenset(),
    directional_persistence_regime_invalidated_refs: Set[EventRecordRef] = frozenset(),
    volatility_metric_invalidated_refs: Set[EventRecordRef] = frozenset(),
    directional_persistence_metric_invalidated_refs: Set[EventRecordRef] = frozenset(),
    distance_to_last_confirmed_swing_invalidated_refs: Set[EventRecordRef] = frozenset(),
) -> ContextAggregationCandidate | None:
    """Assemble one eligible cursor-bounded Context aggregation candidate,
    or return `None` per context.md §9's `missing_input_policy` if any of
    the seven required roles cannot be resolved.

    `target_computation_point_ref` names the exact visible Candle fact this
    call is computing Context for — required, not inferred (MAJ-01).

    Every `*_candidates` argument must already be cursor-visible (Boundary D
    — this core does not self-certify recorded-time visibility). Every
    `*_invalidated_refs` argument is the set of upstream `*FactInvalidated`
    target refs already visible at the same cursor, used only for §8 Phase 1
    step 4's role-specific validity check.

    Never returns a partial result: either all seven roles resolve to
    exactly one Eligible Upstream Fact each and a full candidate is
    produced, or the function returns `None`.
    """
    if scope.context_definition_version != definition.context_definition_version:
        raise ScopeDefinitionMismatchError(scope.context_definition_version, definition.context_definition_version)

    candle_winner = select_candle(
        candle_candidates,
        instrument_id=scope.instrument_id,
        venue_id=scope.venue_id,
        timeframe=scope.timeframe,
        target_computation_point_ref=target_computation_point_ref,
    )
    if candle_winner is None:
        return None
    context_cutoff = candle_winner.effective_window.window_end

    structure_winner = select_structure(
        structure_candidates,
        instrument_id=scope.instrument_id,
        venue_id=scope.venue_id,
        timeframe=scope.timeframe,
        context_cutoff=context_cutoff,
        required_definition_version=definition.required_structure_definition_version,
        invalidated_refs=structure_invalidated_refs,
    )
    if structure_winner is None:
        return None

    volatility_regime_winner = select_regime(
        volatility_regime_candidates,
        instrument_id=scope.instrument_id,
        venue_id=scope.venue_id,
        timeframe=scope.timeframe,
        context_cutoff=context_cutoff,
        dimension=RegimeDimension.VOLATILITY,
        required_definition_version=definition.required_volatility_regime_definition_version,
        invalidated_refs=volatility_regime_invalidated_refs,
    )
    if volatility_regime_winner is None:
        return None

    directional_persistence_regime_winner = select_regime(
        directional_persistence_regime_candidates,
        instrument_id=scope.instrument_id,
        venue_id=scope.venue_id,
        timeframe=scope.timeframe,
        context_cutoff=context_cutoff,
        dimension=RegimeDimension.DIRECTIONAL_PERSISTENCE,
        required_definition_version=definition.required_directional_persistence_regime_definition_version,
        invalidated_refs=directional_persistence_regime_invalidated_refs,
    )
    if directional_persistence_regime_winner is None:
        return None

    volatility_metric_winner = select_feature(
        volatility_metric_candidates,
        instrument_id=scope.instrument_id,
        venue_id=scope.venue_id,
        timeframe=scope.timeframe,
        context_cutoff=context_cutoff,
        feature_type=FeatureType.VOLATILITY_METRIC,
        required_definition_version=definition.required_volatility_metric_feature_definition_version,
        invalidated_refs=volatility_metric_invalidated_refs,
    )
    if volatility_metric_winner is None:
        return None

    directional_persistence_metric_winner = select_feature(
        directional_persistence_metric_candidates,
        instrument_id=scope.instrument_id,
        venue_id=scope.venue_id,
        timeframe=scope.timeframe,
        context_cutoff=context_cutoff,
        feature_type=FeatureType.DIRECTIONAL_PERSISTENCE_METRIC,
        required_definition_version=definition.required_directional_persistence_metric_feature_definition_version,
        invalidated_refs=directional_persistence_metric_invalidated_refs,
    )
    if directional_persistence_metric_winner is None:
        return None

    distance_to_last_confirmed_swing_winner = select_feature(
        distance_to_last_confirmed_swing_candidates,
        instrument_id=scope.instrument_id,
        venue_id=scope.venue_id,
        timeframe=scope.timeframe,
        context_cutoff=context_cutoff,
        feature_type=FeatureType.DISTANCE_TO_LAST_CONFIRMED_SWING,
        required_definition_version=definition.required_distance_to_last_confirmed_swing_feature_definition_version,
        invalidated_refs=distance_to_last_confirmed_swing_invalidated_refs,
    )
    if distance_to_last_confirmed_swing_winner is None:
        return None

    winner_refs = (
        candle_winner.ref,
        structure_winner.ref,
        volatility_regime_winner.ref,
        directional_persistence_regime_winner.ref,
        volatility_metric_winner.ref,
        directional_persistence_metric_winner.ref,
        distance_to_last_confirmed_swing_winner.ref,
    )
    if len(set(winner_refs)) != 7:
        raise DuplicateFactReferenceError(winner_refs)

    bounded = (
        (candle_winner.effective_window.window_start, candle_winner.effective_window.window_end, candle_winner.ref),
        (
            structure_winner.effective_time.window_start,
            structure_winner.effective_time.window_end,
            structure_winner.ref,
        ),
        (
            volatility_regime_winner.analysis_window.window_start,
            volatility_regime_winner.analysis_window.window_end,
            volatility_regime_winner.ref,
        ),
        (
            directional_persistence_regime_winner.analysis_window.window_start,
            directional_persistence_regime_winner.analysis_window.window_end,
            directional_persistence_regime_winner.ref,
        ),
        (
            volatility_metric_winner.effective_window.window_start,
            volatility_metric_winner.effective_window.window_end,
            volatility_metric_winner.ref,
        ),
        (
            directional_persistence_metric_winner.effective_window.window_start,
            directional_persistence_metric_winner.effective_window.window_end,
            directional_persistence_metric_winner.ref,
        ),
        (
            distance_to_last_confirmed_swing_winner.effective_window.window_start,
            distance_to_last_confirmed_swing_winner.effective_window.window_end,
            distance_to_last_confirmed_swing_winner.ref,
        ),
    )
    normalized_refs = normalize_input_fact_refs(bounded)

    if not isinstance(volatility_regime_winner.regime_class, VolatilityRegimeClass):
        raise RegimeClassTypeMismatchError(volatility_regime_winner.regime_class)
    if not isinstance(directional_persistence_regime_winner.regime_class, DirectionalPersistenceRegimeClass):
        raise RegimeClassTypeMismatchError(directional_persistence_regime_winner.regime_class)

    context_values = ContextValues(
        structure_orientation=structure_winner.orientation,
        volatility_regime_class=volatility_regime_winner.regime_class,
        directional_persistence_regime_class=directional_persistence_regime_winner.regime_class,
        volatility_metric=volatility_metric_winner.value,
        directional_persistence_metric=directional_persistence_metric_winner.value,
        distance_to_last_confirmed_swing=distance_to_last_confirmed_swing_winner.value,
    )

    return ContextAggregationCandidate(
        context_subject_id=scope.context_subject_id,
        scope=scope,
        effective_window=candle_winner.effective_window,
        context_cutoff_source_ref=candle_winner.ref,
        structure_fact_ref=structure_winner.ref,
        volatility_regime_fact_ref=volatility_regime_winner.ref,
        directional_persistence_regime_fact_ref=directional_persistence_regime_winner.ref,
        volatility_metric_fact_ref=volatility_metric_winner.ref,
        directional_persistence_metric_fact_ref=directional_persistence_metric_winner.ref,
        distance_to_last_confirmed_swing_fact_ref=distance_to_last_confirmed_swing_winner.ref,
        normalized_input_fact_refs=normalized_refs,
        context_values=context_values,
        context_definition_version=definition.context_definition_version,
    )
