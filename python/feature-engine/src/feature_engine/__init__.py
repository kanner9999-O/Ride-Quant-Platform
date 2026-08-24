"""feature-engine — authoritative Feature analytical core.

Owns `FeatureComputed`/`FeatureFactInvalidated` facts and the
non-authoritative `FeatureCurrentView` projection for exactly the three
founding feature types: `volatility_metric`, `directional_persistence_metric`,
`distance_to_last_confirmed_swing` (`docs/domain/feature.md`). Consumes only
`candle-closed`/`candle-corrected`/`swing-confirmed`/`swing-invalidated`/
`regime-classified`/`regime-fact-invalidated` — never `CandleObserved`,
`CandleCurrentView`, `SwingCandidateDetected`, `SwingCurrentView`, any
Structure event, `RegimeCurrentView`, or its own `FeatureCurrentView`.
Independent from structure-engine/raw-regime-engine's own Python packages —
this package never imports either (see `identity.py`'s module docstring).
"""

from .candle import OHLCV, CandleFact, CandleScope
from .candle_window import CandleWindowFeatureEngine
from .contracts import (
    CANDLE_CLOSED_CONTRACT_ID,
    CANDLE_CORRECTED_CONTRACT_ID,
    CORRECTION_POLICY,
    CURRENT_VIEW_SELECTION_POLICY,
    EFFECTIVE_WINDOW_POLICY,
    ELIGIBLE_SWING_EFFECTIVE_CUTOFF_POLICY,
    ELIGIBLE_SWING_SELECTION_POLICY,
    FEATURE_COMPUTED_CONTRACT_ID,
    FEATURE_FACT_INVALIDATED_CONTRACT_ID,
    INPUT_NORMALIZATION_POLICY,
    MISSING_INPUT_POLICY,
    REGIME_CLASSIFIED_CONTRACT_ID,
    REGIME_FACT_INVALIDATED_CONTRACT_ID,
    SWING_CONFIRMED_CONTRACT_ID,
    SWING_INVALIDATED_CONTRACT_ID,
    WARM_UP_POLICY,
    DecimalPrecisionPolicy,
    FeatureComputed,
    FeatureDefinition,
    FeatureEvent,
    FeatureFactInvalidated,
    FeatureScope,
    RecordedTimeSource,
    normalize_input_facts,
    resolve_output_contract_refs,
)
from .current_view import EffectiveWindow, FeatureCurrentView, FeatureViewResult
from .envelope import EventContractRef, EventRecordRef, ProducerRef, StreamRef
from .errors import (
    DefinitionVersionMismatchError,
    DuplicateCandleConflictError,
    EvidenceCardinalityError,
    EvidenceReferenceConflictError,
    FeatureEngineError,
    FeatureLineageError,
    ForeignScopeError,
    InvalidFeatureDefinitionError,
    InvalidSwingEligibilityInputError,
    NonMonotonicRecordedTimeError,
    OutOfOrderCandleError,
    OutOfOrderCorrectionError,
    ProhibitedInputError,
    RecordedTimeSourceViolationError,
    RegimeDimensionMismatchError,
    UnauthorizedUpstreamContractError,
    UnresolvedOutputContractAuthorityError,
    UnsupportedDistanceRepresentationError,
    UnsupportedFeatureFormulaError,
)
from .publish import SequenceAllocator
from .regime_input import RegimeClassifiedFact, RegimeFactInvalidatedFact
from .regime_passthrough import RegimePassthroughFeatureEngine
from .swing_distance import SwingDistanceFeatureEngine
from .swing_input import SwingConfirmedFact, SwingInvalidatedFact

__all__ = [
    "CANDLE_CLOSED_CONTRACT_ID",
    "CANDLE_CORRECTED_CONTRACT_ID",
    "CORRECTION_POLICY",
    "CURRENT_VIEW_SELECTION_POLICY",
    "EFFECTIVE_WINDOW_POLICY",
    "ELIGIBLE_SWING_EFFECTIVE_CUTOFF_POLICY",
    "ELIGIBLE_SWING_SELECTION_POLICY",
    "FEATURE_COMPUTED_CONTRACT_ID",
    "FEATURE_FACT_INVALIDATED_CONTRACT_ID",
    "INPUT_NORMALIZATION_POLICY",
    "MISSING_INPUT_POLICY",
    "OHLCV",
    "REGIME_CLASSIFIED_CONTRACT_ID",
    "REGIME_FACT_INVALIDATED_CONTRACT_ID",
    "SWING_CONFIRMED_CONTRACT_ID",
    "SWING_INVALIDATED_CONTRACT_ID",
    "WARM_UP_POLICY",
    "CandleFact",
    "CandleScope",
    "CandleWindowFeatureEngine",
    "DecimalPrecisionPolicy",
    "DefinitionVersionMismatchError",
    "DuplicateCandleConflictError",
    "EffectiveWindow",
    "EventContractRef",
    "EventRecordRef",
    "EvidenceCardinalityError",
    "EvidenceReferenceConflictError",
    "FeatureComputed",
    "FeatureCurrentView",
    "FeatureDefinition",
    "FeatureEngineError",
    "FeatureEvent",
    "FeatureFactInvalidated",
    "FeatureLineageError",
    "FeatureScope",
    "FeatureViewResult",
    "ForeignScopeError",
    "InvalidFeatureDefinitionError",
    "InvalidSwingEligibilityInputError",
    "NonMonotonicRecordedTimeError",
    "OutOfOrderCandleError",
    "OutOfOrderCorrectionError",
    "ProducerRef",
    "ProhibitedInputError",
    "RecordedTimeSource",
    "RecordedTimeSourceViolationError",
    "RegimeClassifiedFact",
    "RegimeDimensionMismatchError",
    "RegimeFactInvalidatedFact",
    "RegimePassthroughFeatureEngine",
    "SequenceAllocator",
    "StreamRef",
    "SwingConfirmedFact",
    "SwingDistanceFeatureEngine",
    "SwingInvalidatedFact",
    "UnauthorizedUpstreamContractError",
    "UnresolvedOutputContractAuthorityError",
    "UnsupportedDistanceRepresentationError",
    "UnsupportedFeatureFormulaError",
    "normalize_input_facts",
    "resolve_output_contract_refs",
]
