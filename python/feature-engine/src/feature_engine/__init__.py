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

`authority_resolver.py` is the one exception to "no filesystem I/O": it is a
repository/configuration ADAPTER, explicitly outside the analytical core
proper (`contracts.py`/`swing_distance.py`/`regime_passthrough.py`/
`candle_window.py`/`current_view.py` never import it) — computation engines
request their own bound authority through an injected
`InputContractAuthorityProvider` (`contracts.py`), and
`FilesystemInputContractAuthorityResolver`/`StaticInputContractAuthorityProvider`
(`authority_resolver.py`) are the supported implementations of that
Protocol; no engine accepts an already-resolved authority VALUE directly
(Review-A round-4).
"""

from .authority_resolver import (
    FilesystemInputContractAuthorityResolver,
    StaticInputContractAuthorityProvider,
    resolve_input_contract_authority_from_repository,
)
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
    LIFECYCLE_STREAM_ID,
    MISSING_INPUT_POLICY,
    REGIME_CLASSIFIED_CONTRACT_ID,
    REGIME_FACT_INVALIDATED_CONTRACT_ID,
    SWING_CONFIRMED_CONTRACT_ID,
    SWING_INVALIDATED_CONTRACT_ID,
    WARM_UP_POLICY,
    ComputationCursor,
    DecimalPrecisionPolicy,
    EvaluationFrontier,
    FeatureComputationProfile,
    FeatureComputed,
    FeatureDefinition,
    FeatureEvent,
    FeatureFactInvalidated,
    FeatureScope,
    InputContractAuthorityProvider,
    InputContractRef,
    LifecycleFrontier,
    LifecycleFrontierProof,
    LifecyclePosition,
    RecordedTimeSource,
    ResolvedInputContract,
    StreamPositionProof,
    VerifiedInputContractAuthority,
    is_visible_at_cursor,
    normalize_input_facts,
    resolve_computation_cursor,
    resolve_output_contract_refs,
)
from .current_view import EffectiveWindow, FeatureCurrentView, FeatureViewResult
from .envelope import EventContractRef, EventRecordRef, ProducerRef, StreamRef
from .errors import (
    CursorRelationalInvariantViolationError,
    DefinitionVersionMismatchError,
    DuplicateCandleConflictError,
    EligibleSwingComputationDefectError,
    EvidenceCardinalityError,
    EvidenceReferenceConflictError,
    FeatureEngineError,
    FeatureLineageError,
    ForeignScopeError,
    InputContractIdentityMismatchError,
    InvalidFeatureDefinitionError,
    InvalidSwingEligibilityInputError,
    NonMonotonicRecordedTimeError,
    OutOfOrderCandleError,
    OutOfOrderCorrectionError,
    ProhibitedInputError,
    RecordedTimeSourceViolationError,
    RegimeDimensionMismatchError,
    RegistryContractMismatchError,
    StreamPositionsUniverseMismatchError,
    UnauthorizedUpstreamContractError,
    UnresolvedComputationCursorAuthorityError,
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
    "LIFECYCLE_STREAM_ID",
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
    "ComputationCursor",
    "CursorRelationalInvariantViolationError",
    "DecimalPrecisionPolicy",
    "DefinitionVersionMismatchError",
    "DuplicateCandleConflictError",
    "EffectiveWindow",
    "EligibleSwingComputationDefectError",
    "EvaluationFrontier",
    "EventContractRef",
    "EventRecordRef",
    "EvidenceCardinalityError",
    "EvidenceReferenceConflictError",
    "FeatureComputationProfile",
    "FeatureComputed",
    "FeatureCurrentView",
    "FeatureDefinition",
    "FeatureEngineError",
    "FeatureEvent",
    "FeatureFactInvalidated",
    "FeatureLineageError",
    "FeatureScope",
    "FeatureViewResult",
    "FilesystemInputContractAuthorityResolver",
    "ForeignScopeError",
    "InputContractAuthorityProvider",
    "InputContractIdentityMismatchError",
    "InputContractRef",
    "InvalidFeatureDefinitionError",
    "InvalidSwingEligibilityInputError",
    "LifecycleFrontier",
    "LifecycleFrontierProof",
    "LifecyclePosition",
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
    "RegistryContractMismatchError",
    "ResolvedInputContract",
    "SequenceAllocator",
    "StaticInputContractAuthorityProvider",
    "StreamPositionProof",
    "StreamPositionsUniverseMismatchError",
    "StreamRef",
    "SwingConfirmedFact",
    "SwingDistanceFeatureEngine",
    "SwingInvalidatedFact",
    "UnauthorizedUpstreamContractError",
    "UnresolvedComputationCursorAuthorityError",
    "UnresolvedOutputContractAuthorityError",
    "UnsupportedDistanceRepresentationError",
    "UnsupportedFeatureFormulaError",
    "VerifiedInputContractAuthority",
    "is_visible_at_cursor",
    "normalize_input_facts",
    "resolve_computation_cursor",
    "resolve_input_contract_authority_from_repository",
    "resolve_output_contract_refs",
]
