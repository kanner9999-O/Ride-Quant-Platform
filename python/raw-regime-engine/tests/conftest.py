from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from raw_regime_engine import (
    CANDLE_EVIDENCE_NORMALIZATION_POLICY,
    CURRENT_VIEW_SELECTION_POLICY,
    OHLCV,
    CandleFact,
    CandleScope,
    DecimalPrecisionPolicy,
    RegimeClassified,
    RegimeCurrentView,
    RegimeDefinition,
    RegimeDimensionDefinition,
    RegimeEvent,
    RegimeFactInvalidated,
    RegimeScope,
    RegimeViewResult,
    SequenceAllocator,
    ThresholdBand,
)

INSTRUMENT = "BTC-USDT"
VENUE = "binance-spot"
TIMEFRAME = "1m"


@pytest.fixture
def allocator() -> SequenceAllocator:
    return SequenceAllocator(module_id="raw-regime-engine", implementation_version="0.1.0", run_id="test-run")


@dataclass
class FixedDeltaTimeSource:
    """TEST-ONLY `RecordedTimeSource` — returns `strict_floor + delta`.

    Never production knowledge-time authority: a real implementation of this
    Protocol (wall-clock/runtime allocation) lives outside this analytical
    core (regime.md's own "analytical core only" boundary).
    """

    delta: timedelta = field(default_factory=lambda: timedelta(microseconds=1))

    def next_after(self, strict_floor: datetime) -> datetime:
        return strict_floor + self.delta


class NonCausalTimeSource:
    """TEST-ONLY deliberately-broken `RecordedTimeSource` — returns the
    floor unchanged, violating the required `result > strict_floor`
    invariant, to exercise the engine's own fail-closed validation
    (`RecordedTimeSourceViolationError`). Never production time authority.
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
) -> CandleFact:
    """Builds one authoritative candle-closed/candle-corrected fact at a
    deterministic one-minute window, indexed by `index`. Defaults to the
    module's single (instrument, venue, timeframe) scope; pass overrides to
    build a fact belonging to a different/independent scope."""
    window_start = datetime(2026, 1, 1, tzinfo=UTC) + timedelta(minutes=index)
    window_end = window_start + timedelta(minutes=1)
    scope = CandleScope(instrument_id, venue_id, timeframe, window_start, window_end)
    close_v = close if close is not None else high
    open_v = open_ if open_ is not None else close_v
    ohlcv = OHLCV(Decimal(open_v), Decimal(high), Decimal(low), Decimal(close_v), Decimal(volume))
    recorded_time = window_end + timedelta(seconds=recorded_offset_seconds)
    ref = allocator.next_ref("candle")
    return CandleFact(scope, ohlcv, recorded_time, ref, is_correction=is_correction)


class RangeFormula:
    """TEST-ONLY metric formula — high/low range over the window's evidence.

    Never a production canonical formula: regime.md deliberately does not
    select one (ATR/ADX/efficiency-ratio/etc. are all out of scope here).
    """

    formula_id = "test-high-low-range-v1"

    def compute(self, evidence: Sequence[CandleFact]) -> Decimal:
        highs = [candle.ohlcv.high for candle in evidence]
        lows = [candle.ohlcv.low for candle in evidence]
        return max(highs) - min(lows)


class SumCloseFormula:
    """TEST-ONLY metric formula — sum of closes over the window's evidence.

    Never a production canonical formula.
    """

    formula_id = "test-sum-close-v1"

    def compute(self, evidence: Sequence[CandleFact]) -> Decimal:
        total = Decimal(0)
        for candle in evidence:
            total += candle.ohlcv.close
        return total


def volatility_definition(
    *,
    window_candle_count: int = 3,
    comparison: str = "strict",
    digits: int = 2,
) -> RegimeDimensionDefinition:
    return RegimeDimensionDefinition(
        window_candle_count=window_candle_count,
        metric_formula_id=RangeFormula.formula_id,
        class_thresholds=(
            ThresholdBand(upper_bound=Decimal("5"), label="LOW"),
            ThresholdBand(upper_bound=Decimal("10"), label="NORMAL"),
            ThresholdBand(upper_bound=Decimal("20"), label="HIGH"),
            ThresholdBand(upper_bound=None, label="EXTREME"),
        ),
        threshold_comparison_policy=comparison,
        warm_up_policy="require_full_window",
        gap_policy="defer_until_resolved",
        decimal_precision_policy=DecimalPrecisionPolicy(digits=digits, rounding="ROUND_HALF_UP"),
    )


def directional_persistence_definition(
    *,
    window_candle_count: int = 3,
    comparison: str = "inclusive",
    digits: int = 2,
) -> RegimeDimensionDefinition:
    return RegimeDimensionDefinition(
        window_candle_count=window_candle_count,
        metric_formula_id=SumCloseFormula.formula_id,
        class_thresholds=(
            ThresholdBand(upper_bound=Decimal("30"), label="NON_DIRECTIONAL"),
            ThresholdBand(upper_bound=Decimal("60"), label="TRANSITIONAL"),
            ThresholdBand(upper_bound=None, label="DIRECTIONAL"),
        ),
        threshold_comparison_policy=comparison,
        warm_up_policy="require_full_window",
        gap_policy="defer_until_resolved",
        decimal_precision_policy=DecimalPrecisionPolicy(digits=digits, rounding="ROUND_HALF_UP"),
    )


def make_definition(
    *,
    version: str = "rgd-1",
    volatility: RegimeDimensionDefinition | None = None,
    directional_persistence: RegimeDimensionDefinition | None = None,
) -> RegimeDefinition:
    """`RegimeDefinition` requires BOTH dimensions (P3-RGE-DEF-A-MAJ-03) —
    this helper always supplies a default for whichever one the caller does
    not explicitly override, so existing single-dimension-focused test
    scenarios keep working unchanged."""
    dimensions: dict[str, RegimeDimensionDefinition] = {
        "volatility": volatility if volatility is not None else volatility_definition(),
        "directional_persistence": (
            directional_persistence if directional_persistence is not None else directional_persistence_definition()
        ),
    }
    return RegimeDefinition(
        regime_definition_version=version,
        dimensions=dimensions,
        current_view_selection_policy=CURRENT_VIEW_SELECTION_POLICY,
        candle_evidence_normalization_policy=CANDLE_EVIDENCE_NORMALIZATION_POLICY,
    )


def only_classified(event: RegimeEvent) -> RegimeClassified:
    assert isinstance(event, RegimeClassified)
    return event


def only_invalidated(event: RegimeEvent) -> RegimeFactInvalidated:
    assert isinstance(event, RegimeFactInvalidated)
    return event


def current_result(view: RegimeCurrentView) -> RegimeViewResult:
    result = view.current()
    assert result is not None
    return result


def regime_scope(
    dimension: str,
    *,
    version: str = "rgd-1",
    instrument_id: str = INSTRUMENT,
    venue_id: str = VENUE,
    timeframe: str = TIMEFRAME,
) -> RegimeScope:
    return RegimeScope(
        instrument_id=instrument_id,
        venue_id=venue_id,
        timeframe=timeframe,
        regime_dimension=dimension,
        regime_definition_version=version,
    )
