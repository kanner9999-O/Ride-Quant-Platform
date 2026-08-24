"""Feature's own consumer-side view of the Swing contract (swing.md).

feature-engine consumes exactly `SwingConfirmed`/`SwingInvalidated` — never
`SwingCandidateDetected`, `SwingCurrentView`, or any Structure event
(`BreakOfStructureDetected`/`ChangeOfCharacterDetected`/
`StructureFactInvalidated`/`StructureRecomputed`/`StructureCurrentView`,
feature.md §14/§7.3). This module defines feature-engine's own shape for the
subset of `SwingConfirmed`/`SwingInvalidated` payload fields the Domain
Contract's §9a eligible-Swing selection actually needs — it does not import
`structure_engine.SwingConfirmed` (see `identity.py`'s module docstring: each
Python module is independently built/deployed; being a permitted
`depends_on` in module-registry.yaml is an event-contract relationship, not a
license to import the producing module's Python package).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal

from .envelope import EventRecordRef

SwingDirection = Literal["HIGH", "LOW"]


@dataclass(frozen=True, slots=True)
class SwingConfirmedFact:
    """feature-engine's own view of one authoritative `SwingConfirmed` fact
    (swing.md §4) — only the fields §9a's eligible-Swing filter/total-order
    actually reads.
    """

    instrument_id: str
    venue_id: str
    timeframe: str
    swing_definition_version: str
    direction: SwingDirection
    swing_id: str
    swing_revision: int
    pivot_price: Decimal
    pivot_effective_time: tuple[datetime, datetime]
    recorded_time: datetime
    ref: EventRecordRef


@dataclass(frozen=True, slots=True)
class SwingInvalidatedFact:
    """feature-engine's own view of one authoritative `SwingInvalidated`
    fact (swing.md §5) — identifies exactly which `(swing_id, swing_revision)`
    is no longer eligible.
    """

    swing_id: str
    swing_revision: int
    recorded_time: datetime
    ref: EventRecordRef
