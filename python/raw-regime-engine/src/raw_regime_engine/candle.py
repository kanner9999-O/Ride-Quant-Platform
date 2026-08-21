"""Authoritative Candle input — candle-closed / candle-corrected only.

raw-regime-engine never consumes CandleObserved (provisional) or
CandleCurrentView (non-authoritative) — regime.md §13 requires authoritative
closed/corrected facts exclusively. Duplicated (not imported) from
structure-engine's own `candle.py` — see `identity.py`'s module docstring for
why the two packages do not share code. Unlike structure-engine's OHLCV
(which adds pivot/break comparison helpers for Swing/Structure), this
module's OHLCV carries no such helpers — Raw Regime never does wick/close
pivot comparison; a `MetricFormula` reads whatever OHLCV fields it needs
directly.
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


@dataclass(frozen=True, slots=True)
class CandleFact:
    """One authoritative candle-closed or candle-corrected fact."""

    scope: CandleScope
    ohlcv: OHLCV
    recorded_time: datetime
    ref: EventRecordRef
    is_correction: bool = False
