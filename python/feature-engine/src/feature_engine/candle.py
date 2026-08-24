"""Authoritative Candle input — candle-closed / candle-corrected only.

feature-engine never consumes CandleObserved (provisional) or
CandleCurrentView (non-authoritative) — feature.md §14 requires authoritative
closed/corrected facts exclusively. Duplicated (not imported) from
structure-engine/raw-regime-engine's own `candle.py` — see `identity.py`'s
module docstring. No pivot/wick-vs-close helpers here (unlike
structure-engine's OHLCV) — Feature reads whichever OHLCV field the
Definition pins (`reference_price_field`) directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .envelope import EventRecordRef
from .identity import deterministic_id


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

    def field(self, name: str) -> Decimal:
        """Read one of the four price fields by name (Definition-pinned
        `reference_price_field`) — bounded to the OHLC fields only, never an
        arbitrary attribute lookup.
        """
        if name == "open":
            return self.open
        if name == "high":
            return self.high
        if name == "low":
            return self.low
        if name == "close":
            return self.close
        raise ValueError(f"unsupported reference_price_field: {name!r}")


@dataclass(frozen=True, slots=True)
class CandleFact:
    """One authoritative candle-closed or candle-corrected fact."""

    scope: CandleScope
    ohlcv: OHLCV
    recorded_time: datetime
    ref: EventRecordRef
    is_correction: bool = False
