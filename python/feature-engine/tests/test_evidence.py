from __future__ import annotations

import dataclasses
from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from conftest import (
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
)

from feature_engine import (
    OHLCV,
    CandleFact,
    RegimePassthroughFeatureEngine,
    SequenceAllocator,
    StaticInputContractAuthorityProvider,
    StaticOutputEventContractAuthorityProvider,
    SwingDistanceFeatureEngine,
    normalize_input_facts,
)
from feature_engine.errors import EvidenceCardinalityError, EvidenceReferenceConflictError


def _candle_key(c: CandleFact) -> tuple[datetime, datetime]:
    return (c.scope.window_start, c.scope.window_end)


# --- 6. Input evidence normalization (feature.md §8a) -----------------------


def test_normalize_input_facts_order_independent(allocator: SequenceAllocator) -> None:
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    ordered = normalize_input_facts(candles, effective_time=_candle_key, ref_of=lambda c: c.ref, expected_count=3)
    shuffled = [candles[2], candles[0], candles[1]]
    assert (
        normalize_input_facts(shuffled, effective_time=_candle_key, ref_of=lambda c: c.ref, expected_count=3) == ordered
    )
    assert ordered == tuple(c.ref for c in candles)


def test_normalize_input_facts_duplicate_identical_collapses(allocator: SequenceAllocator) -> None:
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    duplicate = CandleFact(
        candles[0].scope, candles[0].ohlcv, candles[0].recorded_time, candles[0].ref, candles[0].event_contract_ref
    )
    refs = normalize_input_facts(
        [*candles, duplicate], effective_time=_candle_key, ref_of=lambda c: c.ref, expected_count=3
    )
    assert len(refs) == 3
    assert refs == tuple(c.ref for c in candles)


def test_normalize_input_facts_cardinality_fail_closed(allocator: SequenceAllocator) -> None:
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(2)]
    with pytest.raises(EvidenceCardinalityError):
        normalize_input_facts(candles, effective_time=_candle_key, ref_of=lambda c: c.ref, expected_count=3)


# --- 17. Evidence conflict ----------------------------------------------------


def test_evidence_conflict_same_ref_different_candle_payload_rejected(allocator: SequenceAllocator) -> None:
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    conflicting = CandleFact(
        candles[0].scope,
        OHLCV(Decimal("999"), Decimal("999"), Decimal("999"), Decimal("999"), Decimal("1")),
        candles[0].recorded_time,
        candles[0].ref,
        candles[0].event_contract_ref,
    )
    with pytest.raises(EvidenceReferenceConflictError):
        normalize_input_facts(
            [*candles, conflicting], effective_time=_candle_key, ref_of=lambda c: c.ref, expected_count=3
        )


def test_evidence_conflict_same_ref_different_swing_payload_rejected(allocator: SequenceAllocator) -> None:
    swing = swing_confirmed_at(allocator, pivot_index=0, swing_id="s1")
    conflicting = swing_confirmed_at(allocator, pivot_index=5, swing_id="s1")
    conflicting = dataclasses.replace(conflicting, ref=swing.ref)
    with pytest.raises(EvidenceReferenceConflictError):
        normalize_input_facts(
            [swing, conflicting],
            effective_time=lambda s: s.pivot_effective_time,
            ref_of=lambda s: s.ref,
            expected_count=1,
        )


def test_evidence_conflict_same_ref_different_regime_payload_rejected(allocator: SequenceAllocator) -> None:
    regime_fact = regime_classified_at(allocator, 0, computed_metric="1.0")
    conflicting = regime_classified_at(allocator, 0, computed_metric="2.0")
    conflicting = dataclasses.replace(conflicting, ref=regime_fact.ref)
    with pytest.raises(EvidenceReferenceConflictError):
        normalize_input_facts(
            [regime_fact, conflicting],
            effective_time=lambda r: (r.window_start, r.window_end),
            ref_of=lambda r: r.ref,
            expected_count=1,
        )


# --- ADR-037 computation_dependency_content_evidence ------------------------
#
# Values MUST be copied verbatim from the SAME cached VerifiedInputContractAuthority
# used for that fact's own computation, and each fact — original, replacement,
# invalidation — persists its own independent evidence.


def _regime_engine(
    allocator: SequenceAllocator, feature_type: str = "volatility_metric"
) -> RegimePassthroughFeatureEngine:
    definition = make_regime_definition(feature_type=feature_type, regime_dimension_version="rgd-1")
    scope = feature_scope(feature_type, version=definition.feature_definition_version)
    return RegimePassthroughFeatureEngine(
        scope,
        definition,
        allocator,
        FixedDeltaTimeSource(),
        output_event_contract_authority_provider=StaticOutputEventContractAuthorityProvider(
            OUTPUT_EVENT_CONTRACT_AUTHORITY
        ),
        input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
    )


def _assert_evidence_matches_cached_authority(evidence: object) -> None:
    assert evidence.input_contract_content_id == REGIME_INPUT_CONTRACT.input_contract_content_id  # type: ignore[attr-defined]
    assert evidence.stream_registry_content_id == REGIME_INPUT_CONTRACT.stream_registry_content_id  # type: ignore[attr-defined]


def test_regime_original_evidence_copied_from_cached_authority(allocator: SequenceAllocator) -> None:
    engine = _regime_engine(allocator)
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    computed = only_computed(
        engine.on_regime_classified(
            fact, cursor=frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
        )[0]
    )
    _assert_evidence_matches_cached_authority(computed.computation_dependency_content_evidence)


def test_regime_original_invalidation_and_replacement_each_persist_own_evidence(allocator: SequenceAllocator) -> None:
    """Original, invalidation, AND replacement each independently carry a
    correctly-populated `computation_dependency_content_evidence` — never
    left unset on any of the three fact kinds, and always matching this
    engine's own bound authority.
    """
    engine = _regime_engine(allocator)
    original_fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    original = only_computed(
        engine.on_regime_classified(
            original_fact,
            cursor=frontier_at(original_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT),
        )[0]
    )
    _assert_evidence_matches_cached_authority(original.computation_dependency_content_evidence)

    invalidation_fact = regime_invalidated_at(
        allocator, invalidated_fact_ref=original_fact.ref, recorded_time=original.recorded_time + timedelta(minutes=5)
    )
    invalidation = only_invalidated(
        engine.on_regime_invalidated(
            invalidation_fact,
            cursor=frontier_at(invalidation_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT),
        )[0]
    )
    _assert_evidence_matches_cached_authority(invalidation.computation_dependency_content_evidence)

    replacement_fact = regime_classified_at(
        allocator,
        0,
        computed_metric="1.6",
        regime_dimension="volatility",
        regime_definition_version="rgd-1",
        recorded_offset_seconds=600,
    )
    replacement = only_computed(
        engine.on_regime_classified(
            replacement_fact,
            cursor=frontier_at(replacement_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT),
        )[0]
    )
    _assert_evidence_matches_cached_authority(replacement.computation_dependency_content_evidence)

    # Each fact carries its OWN evidence object — never one fact's evidence
    # literally shared by identity with another's (independent capture per
    # fact, feature.md §3/§4's own binding invariant).
    assert original.computation_dependency_content_evidence is not invalidation.computation_dependency_content_evidence
    assert original.computation_dependency_content_evidence is not replacement.computation_dependency_content_evidence


def test_swing_distance_original_evidence_copied_from_cached_authority(allocator: SequenceAllocator) -> None:
    definition = make_distance_definition()
    scope = feature_scope("distance_to_last_confirmed_swing", version=definition.feature_definition_version)
    engine = SwingDistanceFeatureEngine(
        scope,
        definition,
        allocator,
        FixedDeltaTimeSource(),
        output_event_contract_authority_provider=StaticOutputEventContractAuthorityProvider(
            OUTPUT_EVENT_CONTRACT_AUTHORITY
        ),
        authorized_candle_contract_refs=authorized_candle_contract_refs(),
        authorized_swing_contract_refs=authorized_swing_contract_refs(),
        input_contract_authority_provider=StaticInputContractAuthorityProvider(SWING_DISTANCE_INPUT_CONTRACT),
    )
    swing = swing_confirmed_at(allocator, pivot_index=0, swing_id="s1", pivot_price="100")
    engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    candle = candle_at(allocator, 5, high="110", low="90", close="105")
    events = engine.on_candle(candle, cursor=frontier_at(candle.recorded_time))
    computed = only_computed(events[0])
    assert computed.computation_dependency_content_evidence.input_contract_content_id == (
        SWING_DISTANCE_INPUT_CONTRACT.input_contract_content_id
    )
    assert computed.computation_dependency_content_evidence.stream_registry_content_id == (
        SWING_DISTANCE_INPUT_CONTRACT.stream_registry_content_id
    )


# --- Exact outbound event_contract_ref identity (ADR-039 v1.0 Published) ----


def test_regime_engine_emits_exact_published_v1_0_output_refs(allocator: SequenceAllocator) -> None:
    engine = _regime_engine(allocator)
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    computed = only_computed(
        engine.on_regime_classified(
            fact, cursor=frontier_at(fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)
        )[0]
    )
    assert computed.event_contract_ref.contract_id == "feature-computed"
    assert computed.event_contract_ref.contract_version == "v1.0"

    invalidation_fact = regime_invalidated_at(
        allocator, invalidated_fact_ref=fact.ref, recorded_time=computed.recorded_time + timedelta(minutes=5)
    )
    invalidation = only_invalidated(
        engine.on_regime_invalidated(
            invalidation_fact,
            cursor=frontier_at(invalidation_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT),
        )[0]
    )
    assert invalidation.event_contract_ref.contract_id == "feature-fact-invalidated"
    assert invalidation.event_contract_ref.contract_version == "v1.0"
