"""structure-engine — authoritative Swing / Structure analytical core.

Owns Swing candidate/confirmed/invalidated facts, BOS/CHoCH structure facts,
StructureFactInvalidated, and StructureRecomputed (structure.md, swing.md).
Consumes candle-closed/candle-corrected only. Independent from Raw Regime
(ADR-003/ADR-014) — this package never imports a raw-regime-engine module.
"""

from .candle import OHLCV, CandleFact, CandleScope
from .envelope import EventRecordRef, ProducerRef, StreamRef
from .publish import SequenceAllocator
from .structure import (
    BreakOfStructureDetected,
    BrokenSwingRef,
    ChangeOfCharacterDetected,
    StructureDefinition,
    StructureEngine,
    StructureEvent,
    StructureFactInvalidated,
    StructureRecomputed,
    StructureScope,
)
from .swing import (
    SwingCandidateDetected,
    SwingConfirmed,
    SwingDefinition,
    SwingEngine,
    SwingEvent,
    SwingInvalidated,
    SwingScope,
)

__all__ = [
    "OHLCV",
    "CandleFact",
    "CandleScope",
    "EventRecordRef",
    "ProducerRef",
    "StreamRef",
    "SequenceAllocator",
    "SwingDefinition",
    "SwingScope",
    "SwingEngine",
    "SwingEvent",
    "SwingCandidateDetected",
    "SwingConfirmed",
    "SwingInvalidated",
    "StructureDefinition",
    "StructureScope",
    "StructureEngine",
    "StructureEvent",
    "BrokenSwingRef",
    "BreakOfStructureDetected",
    "ChangeOfCharacterDetected",
    "StructureFactInvalidated",
    "StructureRecomputed",
]
