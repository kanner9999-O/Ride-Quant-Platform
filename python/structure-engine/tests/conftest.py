from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from structure_engine import OHLCV, CandleFact, CandleScope, SequenceAllocator

INSTRUMENT = "BTC-USDT"
VENUE = "binance-spot"
TIMEFRAME = "1m"


@pytest.fixture
def allocator() -> SequenceAllocator:
    return SequenceAllocator(module_id="structure-engine", implementation_version="0.1.0", run_id="test-run")


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
) -> CandleFact:
    """Builds one authoritative candle-closed/candle-corrected fact at a
    deterministic one-minute window, indexed by `index`."""
    window_start = datetime(2026, 1, 1, tzinfo=UTC) + timedelta(minutes=index)
    window_end = window_start + timedelta(minutes=1)
    scope = CandleScope(INSTRUMENT, VENUE, TIMEFRAME, window_start, window_end)
    close_v = close if close is not None else high
    open_v = open_ if open_ is not None else close_v
    ohlcv = OHLCV(Decimal(open_v), Decimal(high), Decimal(low), Decimal(close_v), Decimal(volume))
    recorded_time = window_end + timedelta(seconds=recorded_offset_seconds)
    ref = allocator.next_ref("candle")
    return CandleFact(scope, ohlcv, recorded_time, ref, is_correction=is_correction)
