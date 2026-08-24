"""Feature's own consumer-side view of the Raw Regime contract (regime.md).

feature-engine consumes exactly `RegimeClassified`/`RegimeFactInvalidated` —
never `RegimeCurrentView` (feature.md §14). This module defines
feature-engine's own shape for the payload fields §7.1/§7.2's regime
pass-through path needs — it does not import
`raw_regime_engine.RegimeClassified` (see `identity.py`'s module docstring).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal

from .envelope import EventRecordRef

RegimeDimension = Literal["volatility", "directional_persistence"]


@dataclass(frozen=True, slots=True)
class RegimeClassifiedFact:
    """feature-engine's own view of one authoritative `RegimeClassified`
    fact (regime.md §3) — Feature exposes `computed_metric` verbatim, never
    reclassifies it (feature.md §7.1/§7.2).
    """

    instrument_id: str
    venue_id: str
    timeframe: str
    regime_dimension: RegimeDimension
    regime_definition_version: str
    computed_metric: Decimal
    window_start: datetime
    window_end: datetime
    recorded_time: datetime
    ref: EventRecordRef


@dataclass(frozen=True, slots=True)
class RegimeFactInvalidatedFact:
    """feature-engine's own view of one authoritative `RegimeFactInvalidated`
    fact (regime.md §4) — identifies exactly which prior `RegimeClassified`
    ref is no longer authoritative.
    """

    invalidated_fact_ref: EventRecordRef
    recorded_time: datetime
    ref: EventRecordRef
