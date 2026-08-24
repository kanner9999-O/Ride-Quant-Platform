from __future__ import annotations

import dataclasses
from datetime import datetime
from decimal import Decimal

import pytest
from conftest import candle_at, regime_classified_at, swing_confirmed_at

from feature_engine import OHLCV, CandleFact, SequenceAllocator, normalize_input_facts
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
