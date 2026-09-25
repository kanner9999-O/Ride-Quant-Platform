"""Context values (context.md §3 `context_values`) and the internal
aggregation result type.

`ContextAggregationCandidate` is deliberately NOT named / described as a
published `MarketContextSnapshot` event. Per
`feature-context-architecture.md` §5.2/§13's terminology correction, this
module calls its own result an **eligible cursor-bounded Context aggregation
candidate** — record-integrity properties (immutable, cursor-bounded,
lineage-preserving, eligible per §8) are what this core can and does
guarantee; it does NOT claim to be the authoritative
`MarketContextSnapshot` event Chapter 8 §8.2's envelope would require
(genuine `event_id`/`event_contract_ref`/`stream_ref`/`producer_ref`/
`sequence`/`causation_refs`), because context-aggregator owns no such
publishing authority yet (`owns_authoritative_state: false`,
module-registry.yaml). Publishing/envelope binding is a later, separate,
governed slice.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from context_aggregator.evidence import DirectionalPersistenceRegimeClass, StructureOrientation, VolatilityRegimeClass
from context_aggregator.refs import EffectiveWindow, EventRecordRef
from context_aggregator.scope import ContextSubjectScope


@dataclass(frozen=True, slots=True)
class ContextValues:
    """context.md §3 `context_values` — direct copies of upstream
    authoritative fields, never recomputed (§17). Decimal fields are
    preserved exactly as supplied by the upstream Feature fact — never
    round-tripped through `float`."""

    structure_orientation: StructureOrientation
    volatility_regime_class: VolatilityRegimeClass
    directional_persistence_regime_class: DirectionalPersistenceRegimeClass
    volatility_metric: Decimal
    directional_persistence_metric: Decimal
    distance_to_last_confirmed_swing: Decimal


@dataclass(frozen=True, slots=True)
class ContextAggregationCandidate:
    """An implementation-internal, immutable eligible cursor-bounded Context
    aggregation candidate — NOT a published `MarketContextSnapshot` event
    (see module docstring). Contains context subject identity/scope, the
    computation point's effective window, the seven normalized input fact
    refs, the assembled `ContextValues`, and the `context_definition_version`
    pin — nothing else. No `event_id`, `event_contract_ref`, `stream_ref`,
    `producer_ref`, authoritative `sequence`, or `causation_refs` is present
    or fabricated here."""

    context_subject_id: str
    scope: ContextSubjectScope
    effective_window: EffectiveWindow
    context_cutoff_source_ref: EventRecordRef
    structure_fact_ref: EventRecordRef
    volatility_regime_fact_ref: EventRecordRef
    directional_persistence_regime_fact_ref: EventRecordRef
    volatility_metric_fact_ref: EventRecordRef
    directional_persistence_metric_fact_ref: EventRecordRef
    distance_to_last_confirmed_swing_fact_ref: EventRecordRef
    normalized_input_fact_refs: tuple[EventRecordRef, ...]
    context_values: ContextValues
    context_definition_version: str
