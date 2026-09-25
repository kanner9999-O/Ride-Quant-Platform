"""context-aggregator — Context deterministic aggregation core.

Selects already cursor-visible upstream Structure/Regime/Feature/Candle
facts and assembles an eligible cursor-bounded Context aggregation candidate
(context.md; `module_id: context-aggregator`, Type-2 Projection,
`owns_authoritative_state: false`, module-registry.yaml). See this package's
`README.md` for the exact implemented boundary and the exact gaps
deliberately left open (Input Contract, Event Contract, stream-registry
frontier capture, publishing/envelope binding).

Independent from structure-engine/raw-regime-engine/feature-engine's own
Python packages — this package never imports any of them (see
`identity.py`'s module docstring); it defines its own consumer-side
`evidence.py` views of their contracts.
"""

from .aggregation import aggregate_context_candidate
from .definition import ContextDefinition
from .errors import (
    ContextAggregatorError,
    DuplicateFactReferenceError,
    InvalidContextTypeError,
    MalformedLineageError,
    RegimeClassTypeMismatchError,
    ScopeDefinitionMismatchError,
)
from .evidence import (
    CandleFact,
    DirectionalPersistenceRegimeClass,
    FeatureFact,
    FeatureType,
    RegimeDimension,
    RegimeFact,
    StructureFact,
    StructureFactKind,
    StructureOrientation,
    VolatilityRegimeClass,
)
from .refs import EffectiveWindow, EventRecordRef
from .scope import MARKET_CONTEXT, ContextSubjectScope
from .values import ContextAggregationCandidate, ContextValues

__all__ = [
    "MARKET_CONTEXT",
    "CandleFact",
    "ContextAggregationCandidate",
    "ContextAggregatorError",
    "ContextDefinition",
    "ContextSubjectScope",
    "ContextValues",
    "DirectionalPersistenceRegimeClass",
    "DuplicateFactReferenceError",
    "EffectiveWindow",
    "EventRecordRef",
    "FeatureFact",
    "FeatureType",
    "InvalidContextTypeError",
    "MalformedLineageError",
    "RegimeClassTypeMismatchError",
    "RegimeDimension",
    "RegimeFact",
    "ScopeDefinitionMismatchError",
    "StructureFact",
    "StructureFactKind",
    "StructureOrientation",
    "VolatilityRegimeClass",
    "aggregate_context_candidate",
]
