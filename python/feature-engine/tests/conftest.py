from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from feature_engine import (
    CANDLE_CLOSED_CONTRACT_ID,
    CANDLE_CORRECTED_CONTRACT_ID,
    CORRECTION_POLICY,
    CURRENT_VIEW_SELECTION_POLICY,
    EFFECTIVE_WINDOW_POLICY,
    ELIGIBLE_SWING_EFFECTIVE_CUTOFF_POLICY,
    ELIGIBLE_SWING_SELECTION_POLICY,
    INPUT_NORMALIZATION_POLICY,
    MISSING_INPUT_POLICY,
    OHLCV,
    REGIME_CLASSIFIED_CONTRACT_ID,
    REGIME_FACT_INVALIDATED_CONTRACT_ID,
    SWING_CONFIRMED_CONTRACT_ID,
    SWING_INVALIDATED_CONTRACT_ID,
    WARM_UP_POLICY,
    CandleFact,
    CandleScope,
    DecimalPrecisionPolicy,
    EventContractRef,
    FeatureCurrentView,
    FeatureDefinition,
    FeatureEvent,
    FeatureScope,
    FeatureViewResult,
    RegimeClassifiedFact,
    RegimeFactInvalidatedFact,
    SequenceAllocator,
    SwingConfirmedFact,
    SwingInvalidatedFact,
)
from feature_engine.contracts import FeatureComputed, FeatureFactInvalidated

INSTRUMENT = "BTC-USDT"
VENUE = "binance-spot"
TIMEFRAME = "1m"
BASE = datetime(2026, 1, 1, tzinfo=UTC)

# Test-fixture-pinned upstream contract_version — a FeatureDefinition's own
# choice of which immutable contract snapshot it authorizes; distinct from
# feature_engine's internal FEATURE_EVENT_CONTRACT_VERSION output stand-in.
CONTRACT_VERSION = "v1"


@pytest.fixture
def allocator() -> SequenceAllocator:
    return SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="test-run")


@dataclass
class FixedDeltaTimeSource:
    """TEST-ONLY `RecordedTimeSource` — returns `strict_floor + delta`.
    Never production knowledge-time authority.
    """

    delta: timedelta = field(default_factory=lambda: timedelta(microseconds=1))

    def next_after(self, strict_floor: datetime) -> datetime:
        return strict_floor + self.delta


class NonCausalTimeSource:
    """TEST-ONLY deliberately-broken `RecordedTimeSource` — returns the
    floor unchanged, violating the causal-floor contract.
    """

    def next_after(self, strict_floor: datetime) -> datetime:
        return strict_floor


@pytest.fixture
def time_source() -> FixedDeltaTimeSource:
    return FixedDeltaTimeSource()


def candle_at(
    allocator: SequenceAllocator,
    index: int,
    *,
    high: str,
    low: str,
    close: str | None = None,
    open_: str | None = None,
    volume: str = "1",
    is_correction: bool = False,
    recorded_offset_seconds: int = 0,
    instrument_id: str = INSTRUMENT,
    venue_id: str = VENUE,
    timeframe: str = TIMEFRAME,
    event_contract_ref: EventContractRef | None = None,
) -> CandleFact:
    window_start = BASE + timedelta(minutes=index)
    window_end = window_start + timedelta(minutes=1)
    scope = CandleScope(instrument_id, venue_id, timeframe, window_start, window_end)
    close_v = close if close is not None else high
    open_v = open_ if open_ is not None else close_v
    ohlcv = OHLCV(Decimal(open_v), Decimal(high), Decimal(low), Decimal(close_v), Decimal(volume))
    recorded_time = window_end + timedelta(seconds=recorded_offset_seconds)
    ref = allocator.next_ref("candle")
    if event_contract_ref is None:
        contract_id = CANDLE_CORRECTED_CONTRACT_ID if is_correction else CANDLE_CLOSED_CONTRACT_ID
        event_contract_ref = EventContractRef(contract_id, CONTRACT_VERSION)
    return CandleFact(scope, ohlcv, recorded_time, ref, event_contract_ref, is_correction=is_correction)


def swing_confirmed_at(
    allocator: SequenceAllocator,
    *,
    pivot_index: int,
    swing_id: str,
    swing_revision: int = 1,
    direction: str = "HIGH",
    pivot_price: str = "100",
    swing_definition_version: str = "swd-1",
    recorded_offset_minutes: int = 0,
    instrument_id: str = INSTRUMENT,
    venue_id: str = VENUE,
    timeframe: str = TIMEFRAME,
    event_contract_ref: EventContractRef | None = None,
) -> SwingConfirmedFact:
    pivot_start = BASE + timedelta(minutes=pivot_index)
    pivot_end = pivot_start + timedelta(minutes=1)
    recorded_time = pivot_end + timedelta(minutes=recorded_offset_minutes)
    if event_contract_ref is None:
        event_contract_ref = EventContractRef(SWING_CONFIRMED_CONTRACT_ID, CONTRACT_VERSION)
    return SwingConfirmedFact(
        instrument_id=instrument_id,
        venue_id=venue_id,
        timeframe=timeframe,
        swing_definition_version=swing_definition_version,
        direction=direction,  # type: ignore[arg-type]
        swing_id=swing_id,
        swing_revision=swing_revision,
        pivot_price=Decimal(pivot_price),
        pivot_effective_time=(pivot_start, pivot_end),
        recorded_time=recorded_time,
        ref=allocator.next_ref("swing"),
        event_contract_ref=event_contract_ref,
    )


def swing_invalidated_at(
    allocator: SequenceAllocator,
    *,
    swing_id: str,
    swing_revision: int,
    recorded_time: datetime,
    event_contract_ref: EventContractRef | None = None,
) -> SwingInvalidatedFact:
    if event_contract_ref is None:
        event_contract_ref = EventContractRef(SWING_INVALIDATED_CONTRACT_ID, CONTRACT_VERSION)
    return SwingInvalidatedFact(
        swing_id=swing_id,
        swing_revision=swing_revision,
        recorded_time=recorded_time,
        ref=allocator.next_ref("swing"),
        event_contract_ref=event_contract_ref,
    )


def regime_classified_at(
    allocator: SequenceAllocator,
    index: int,
    *,
    computed_metric: str,
    regime_dimension: str = "volatility",
    regime_definition_version: str = "rgd-1",
    recorded_offset_seconds: int = 0,
    instrument_id: str = INSTRUMENT,
    venue_id: str = VENUE,
    timeframe: str = TIMEFRAME,
    event_contract_ref: EventContractRef | None = None,
) -> RegimeClassifiedFact:
    window_start = BASE + timedelta(minutes=index)
    window_end = window_start + timedelta(minutes=1)
    recorded_time = window_end + timedelta(seconds=recorded_offset_seconds)
    if event_contract_ref is None:
        event_contract_ref = EventContractRef(REGIME_CLASSIFIED_CONTRACT_ID, CONTRACT_VERSION)
    return RegimeClassifiedFact(
        instrument_id=instrument_id,
        venue_id=venue_id,
        timeframe=timeframe,
        regime_dimension=regime_dimension,  # type: ignore[arg-type]
        regime_definition_version=regime_definition_version,
        computed_metric=Decimal(computed_metric),
        window_start=window_start,
        window_end=window_end,
        recorded_time=recorded_time,
        ref=allocator.next_ref("regime"),
        event_contract_ref=event_contract_ref,
    )


def regime_invalidated_at(
    allocator: SequenceAllocator,
    *,
    invalidated_fact_ref: object,
    recorded_time: datetime,
    event_contract_ref: EventContractRef | None = None,
) -> RegimeFactInvalidatedFact:
    if event_contract_ref is None:
        event_contract_ref = EventContractRef(REGIME_FACT_INVALIDATED_CONTRACT_ID, CONTRACT_VERSION)
    return RegimeFactInvalidatedFact(
        invalidated_fact_ref=invalidated_fact_ref,  # type: ignore[arg-type]
        recorded_time=recorded_time,
        ref=allocator.next_ref("regime"),
        event_contract_ref=event_contract_ref,
    )


class RangeFormula:
    """TEST-ONLY metric formula — high/low range over the window's evidence.
    Never a production canonical formula.
    """

    formula_id = "test-high-low-range-v1"

    def compute(self, evidence: Sequence[CandleFact]) -> Decimal:
        highs = [candle.ohlcv.high for candle in evidence]
        lows = [candle.ohlcv.low for candle in evidence]
        return max(highs) - min(lows)


def make_decimal_policy(digits: int = 2) -> DecimalPrecisionPolicy:
    return DecimalPrecisionPolicy(digits=digits, rounding="ROUND_HALF_UP")


def make_regime_definition(
    *,
    feature_type: str = "volatility_metric",
    version: str = "fd-regime-1",
    regime_dimension_version: str = "rgd-1",
    digits: int = 2,
) -> FeatureDefinition:
    return FeatureDefinition(
        feature_definition_id="fd-regime",
        feature_definition_version=version,
        feature_type=feature_type,  # type: ignore[arg-type]
        upstream_source="regime",
        upstream_contract_refs=(
            EventContractRef(REGIME_CLASSIFIED_CONTRACT_ID, CONTRACT_VERSION),
            EventContractRef(REGIME_FACT_INVALIDATED_CONTRACT_ID, CONTRACT_VERSION),
        ),
        required_upstream_definition_version=regime_dimension_version,
        unit="ratio",
        decimal_precision_policy=make_decimal_policy(digits),
        warm_up_policy=WARM_UP_POLICY,
        missing_input_policy=MISSING_INPUT_POLICY,
        correction_policy=CORRECTION_POLICY,
        effective_window_policy=EFFECTIVE_WINDOW_POLICY,
        current_view_selection_policy=CURRENT_VIEW_SELECTION_POLICY,
        input_normalization_policy=INPUT_NORMALIZATION_POLICY,
    )


def make_candle_definition(
    *,
    feature_type: str = "volatility_metric",
    version: str = "fd-candle-1",
    window_candle_count: int = 3,
    formula_id: str = RangeFormula.formula_id,
    digits: int = 2,
) -> FeatureDefinition:
    return FeatureDefinition(
        feature_definition_id="fd-candle",
        feature_definition_version=version,
        feature_type=feature_type,  # type: ignore[arg-type]
        upstream_source="candle",
        upstream_contract_refs=(
            EventContractRef(CANDLE_CLOSED_CONTRACT_ID, CONTRACT_VERSION),
            EventContractRef(CANDLE_CORRECTED_CONTRACT_ID, CONTRACT_VERSION),
        ),
        window_candle_count=window_candle_count,
        formula_id=formula_id,
        unit="price",
        decimal_precision_policy=make_decimal_policy(digits),
        warm_up_policy=WARM_UP_POLICY,
        missing_input_policy=MISSING_INPUT_POLICY,
        correction_policy=CORRECTION_POLICY,
        effective_window_policy=EFFECTIVE_WINDOW_POLICY,
        current_view_selection_policy=CURRENT_VIEW_SELECTION_POLICY,
        input_normalization_policy=INPUT_NORMALIZATION_POLICY,
    )


def make_distance_definition(
    *,
    version: str = "fd-distance-1",
    swing_direction: str = "HIGH",
    distance_representation: str = "absolute",
    reference_price_field: str = "close",
    swing_definition_version: str = "swd-1",
    digits: int = 2,
) -> FeatureDefinition:
    return FeatureDefinition(
        feature_definition_id="fd-distance",
        feature_definition_version=version,
        feature_type="distance_to_last_confirmed_swing",
        swing_direction=swing_direction,  # type: ignore[arg-type]
        distance_representation=distance_representation,  # type: ignore[arg-type]
        reference_price_field=reference_price_field,
        eligible_swing_selection_policy=ELIGIBLE_SWING_SELECTION_POLICY,
        eligible_swing_effective_cutoff_policy=ELIGIBLE_SWING_EFFECTIVE_CUTOFF_POLICY,
        required_swing_definition_version=swing_definition_version,
        unit="price",
        decimal_precision_policy=make_decimal_policy(digits),
        warm_up_policy=WARM_UP_POLICY,
        missing_input_policy=MISSING_INPUT_POLICY,
        correction_policy=CORRECTION_POLICY,
        effective_window_policy=EFFECTIVE_WINDOW_POLICY,
        current_view_selection_policy=CURRENT_VIEW_SELECTION_POLICY,
        input_normalization_policy=INPUT_NORMALIZATION_POLICY,
    )


def feature_scope(
    feature_type: str,
    *,
    version: str,
    instrument_id: str = INSTRUMENT,
    venue_id: str = VENUE,
    timeframe: str = TIMEFRAME,
) -> FeatureScope:
    return FeatureScope(
        instrument_id=instrument_id,
        venue_id=venue_id,
        timeframe=timeframe,
        feature_type=feature_type,  # type: ignore[arg-type]
        feature_definition_version=version,
    )


def only_computed(event: FeatureEvent) -> FeatureComputed:
    assert isinstance(event, FeatureComputed)
    return event


def only_invalidated(event: FeatureEvent) -> FeatureFactInvalidated:
    assert isinstance(event, FeatureFactInvalidated)
    return event


def current_result(view: FeatureCurrentView) -> FeatureViewResult:
    result = view.current()
    assert result is not None
    return result
