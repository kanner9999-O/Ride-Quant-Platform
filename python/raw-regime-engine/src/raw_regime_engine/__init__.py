"""raw-regime-engine — authoritative Raw Regime analytical core.

Owns `RegimeClassified`/`RegimeFactInvalidated` facts and the non-authoritative
`RegimeCurrentView` projection for exactly the `volatility` and
`directional_persistence` dimensions (`docs/domain/regime.md`). Consumes
candle-closed/candle-corrected only — never Structure/Swing/Feature/Context/
Strategy/Account/Risk/CandleObserved/CandleCurrentView/its own
RegimeCurrentView. Independent from Structure Engine (ADR-014) — this package
never imports a structure_engine module.
"""

from .candle import OHLCV, CandleFact, CandleScope
from .envelope import EventRecordRef, ProducerRef, StreamRef
from .errors import (
    DuplicateCandleConflictError,
    ForeignScopeError,
    FormulaMismatchError,
    NonMonotonicRecordedTimeError,
    OutOfOrderCandleError,
    OutOfOrderCorrectionError,
    RawRegimeEngineError,
    RegimeLineageError,
)
from .publish import SequenceAllocator
from .regime import (
    CANDLE_EVIDENCE_NORMALIZATION_POLICY,
    CURRENT_VIEW_SELECTION_POLICY,
    DecimalPrecisionPolicy,
    MetricFormula,
    RegimeClassified,
    RegimeCurrentView,
    RegimeDefinition,
    RegimeDimensionDefinition,
    RegimeEngine,
    RegimeEvent,
    RegimeFactInvalidated,
    RegimeScope,
    RegimeViewResult,
    ThresholdBand,
    normalize_evidence,
)

__all__ = [
    "OHLCV",
    "CANDLE_EVIDENCE_NORMALIZATION_POLICY",
    "CURRENT_VIEW_SELECTION_POLICY",
    "CandleFact",
    "CandleScope",
    "DecimalPrecisionPolicy",
    "DuplicateCandleConflictError",
    "EventRecordRef",
    "ForeignScopeError",
    "FormulaMismatchError",
    "MetricFormula",
    "NonMonotonicRecordedTimeError",
    "OutOfOrderCandleError",
    "OutOfOrderCorrectionError",
    "ProducerRef",
    "RawRegimeEngineError",
    "RegimeClassified",
    "RegimeCurrentView",
    "RegimeDefinition",
    "RegimeDimensionDefinition",
    "RegimeEngine",
    "RegimeEvent",
    "RegimeFactInvalidated",
    "RegimeLineageError",
    "RegimeScope",
    "RegimeViewResult",
    "SequenceAllocator",
    "StreamRef",
    "ThresholdBand",
    "normalize_evidence",
]
