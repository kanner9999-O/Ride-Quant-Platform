from __future__ import annotations

import dataclasses
from datetime import timedelta
from decimal import Decimal
from typing import Any

import pytest
from conftest import FixedDeltaTimeSource, RangeFormula, candle_at, feature_scope, make_candle_definition, only_computed

from feature_engine import CandleWindowFeatureEngine, FeatureEvent, SequenceAllocator
from feature_engine.errors import EvidenceReferenceConflictError, UnsupportedFeatureFormulaError


def _engine(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource, **definition_kwargs: Any
) -> CandleWindowFeatureEngine:
    definition = make_candle_definition(**definition_kwargs)
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    return CandleWindowFeatureEngine(scope, definition, RangeFormula(), allocator, time_source)


# --- 5. Candle path -----------------------------------------------------------


def test_candle_path_exact_window_cardinality_and_value(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source, window_candle_count=3)
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    for c in candles[:-1]:
        assert engine.on_candle(c) == []
    computed = only_computed(engine.on_candle(candles[-1])[0])
    assert len(computed.input_fact_refs) == 3
    assert computed.value == Decimal("1.00")


def test_candle_path_deterministic_normalized_evidence_order(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source, window_candle_count=3)
    candles = [candle_at(allocator, i, high="10", low="9") for i in range(3)]
    for c in candles[:-1]:
        engine.on_candle(c)
    computed = only_computed(engine.on_candle(candles[-1])[0])
    assert computed.input_fact_refs == tuple(c.ref for c in candles)


def test_candle_path_unsupported_formula_fails_closed_no_computation(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    definition = make_candle_definition(formula_id="test-not-authorized-formula")
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    with pytest.raises(UnsupportedFeatureFormulaError):
        CandleWindowFeatureEngine(scope, definition, RangeFormula(), allocator, time_source)


def test_candle_path_warm_up_valid_absence(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source, window_candle_count=3)
    assert engine.on_candle(candle_at(allocator, 0, high="10", low="9")) == []
    assert engine.on_candle(candle_at(allocator, 1, high="10", low="9")) == []


def test_candle_path_correction_no_shortcut(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source, window_candle_count=3)
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    original = only_computed(events[0])
    correction = candle_at(
        allocator, 1, high="10", low="9", volume="2", is_correction=True, recorded_offset_seconds=120
    )
    events = engine.on_candle(correction)
    assert len(events) == 2
    replacement = only_computed(events[1])
    assert replacement.value == original.value
    assert replacement.supersedes_fact_ref == original.ref


# --- P3-FEATURE-A-MAJ-05 remediation: dedup is ref-identity-only, never value-equality


def test_candle_path_distinct_correction_ref_enters_lineage_even_when_value_unchanged(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source, window_candle_count=3)
    events: list[FeatureEvent] = []
    for i in range(3):
        events = engine.on_candle(candle_at(allocator, i, high="10", low="9"))
    original = only_computed(events[0])
    original_candle = candle_at(allocator, 1, high="10", low="9")
    # A genuinely new correction ref, but IDENTICAL OHLCV content to the original —
    # must still invalidate+replace (feature.md §3 "no shortcut"), never silently
    # dropped as if it were a duplicate delivery of the same ref.
    correction = dataclasses.replace(
        original_candle,
        ref=allocator.next_ref("candle"),
        recorded_time=original_candle.recorded_time + timedelta(seconds=120),
        is_correction=True,
    )
    events = engine.on_candle(correction)
    assert len(events) == 2
    replacement = only_computed(events[1])
    assert replacement.value == original.value
    assert replacement.supersedes_fact_ref == original.ref
    assert replacement.ref != original.ref


def test_candle_path_same_ref_different_content_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source, window_candle_count=3)
    first = candle_at(allocator, 0, high="10", low="9")
    engine.on_candle(first)
    conflicting = dataclasses.replace(first, ohlcv=dataclasses.replace(first.ohlcv, high=Decimal("999")))
    with pytest.raises(EvidenceReferenceConflictError):
        engine.on_candle(conflicting)


def test_candle_path_same_ref_identical_redelivery_is_idempotent(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source, window_candle_count=3)
    first = candle_at(allocator, 0, high="10", low="9")
    engine.on_candle(first)
    assert engine.on_candle(first) == []
