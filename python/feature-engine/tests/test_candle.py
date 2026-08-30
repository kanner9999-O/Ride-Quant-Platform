from __future__ import annotations

from decimal import Decimal

import pytest

from feature_engine import OHLCV

# `OHLCV.field()` is the sole reader of the Definition-pinned
# `reference_price_field` (candle.py) — production code
# (swing_distance.py's `_compute_distance`) only ever exercises it with
# `reference_price_field="close"` (the only value used by any fixture
# Definition in this suite), so the other three supported fields and the
# rejection path were never directly exercised. These are meaningful,
# direct behavior tests of a small, bounded, public dataclass method — each
# assertion would fail if the targeted field lookup returned the wrong
# value or failed to reject an unsupported name.

_OHLCV = OHLCV(
    open=Decimal("100"),
    high=Decimal("110"),
    low=Decimal("90"),
    close=Decimal("105"),
    volume=Decimal("1"),
)


def test_field_open_returns_open() -> None:
    assert _OHLCV.field("open") == Decimal("100")


def test_field_high_returns_high() -> None:
    assert _OHLCV.field("high") == Decimal("110")


def test_field_low_returns_low() -> None:
    assert _OHLCV.field("low") == Decimal("90")


def test_field_close_returns_close() -> None:
    assert _OHLCV.field("close") == Decimal("105")


def test_field_unsupported_name_rejected() -> None:
    with pytest.raises(ValueError, match="unsupported reference_price_field"):
        _OHLCV.field("volume")
