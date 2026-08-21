"""Authoritative Candle input — candle-closed / candle-corrected only.

structure-engine never consumes CandleObserved (provisional) or
CandleCurrentView (non-authoritative) — swing.md §13, structure.md §12 both
require authoritative closed/corrected facts exclusively.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal

from .envelope import EventRecordRef
from .identity import deterministic_id

PriceBasis = Literal["wick", "close"]


@dataclass(frozen=True, slots=True)
class CandleScope:
    """The five-field qualifying scope of a Logical Candle Subject (candle.md §1)."""

    instrument_id: str
    venue_id: str
    timeframe: str
    window_start: datetime
    window_end: datetime

    @property
    def subject_id(self) -> str:
        return deterministic_id(
            "candle",
            self.instrument_id,
            self.venue_id,
            self.timeframe,
            self.window_start.isoformat(),
            self.window_end.isoformat(),
        )


@dataclass(frozen=True, slots=True)
class OHLCV:
    """Lossless decimal OHLCV (I-9) — never float32/float64."""

    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal

    def extreme(self, basis: PriceBasis) -> Decimal:
        """The single price value relevant for pivot/break comparison, high side."""
        return self.high if basis == "wick" else self.close

    def extreme_low(self, basis: PriceBasis) -> Decimal:
        """The single price value relevant for pivot/break comparison, low side."""
        return self.low if basis == "wick" else self.close


@dataclass(frozen=True, slots=True)
class CandleFact:
    """One authoritative candle-closed or candle-corrected fact."""

    scope: CandleScope
    ohlcv: OHLCV
    recorded_time: datetime
    ref: EventRecordRef
    is_correction: bool = False
