"""Bounded Context Definition representation (context.md §6).

Pins exactly the fields this deterministic core needs to enforce §8's
Phase 1 definition-version match and §9's role cardinality — NOT a registry:
no storage/versioning/lookup mechanism is implemented here
(`feature-context-architecture.md` §13 — Phase 1 concern, deliberately
deferred, same gap already carried for Swing/Structure/Regime/Feature). The
caller supplies an already-resolved `ContextDefinition` instance for the
exact `context_definition_version` in force; where the field means a caller
should provide it themselves.

`computation_cadence_policy`, `context_cutoff_policy`,
`window_alignment_policy`, and `missing_input_policy` are each a CLOSED enum
with exactly one currently-valid value (context.md §6) — this core
implements that one value directly as fixed behavior rather than storing it
as a configurable field, so it never presents a pluggable surface that no
current Context Definition actually varies.
"""

from __future__ import annotations

from dataclasses import dataclass

from context_aggregator.errors import InvalidContextTypeError
from context_aggregator.scope import MARKET_CONTEXT


@dataclass(frozen=True, slots=True)
class ContextDefinition:
    """Minimum-viable pinned policy this core consumes (context.md §6
    schema, definition-version-pin fields only)."""

    context_definition_id: str
    context_definition_version: str
    required_structure_definition_version: str
    required_volatility_regime_definition_version: str
    required_directional_persistence_regime_definition_version: str
    required_volatility_metric_feature_definition_version: str
    required_directional_persistence_metric_feature_definition_version: str
    required_distance_to_last_confirmed_swing_feature_definition_version: str
    context_type: str = MARKET_CONTEXT

    def __post_init__(self) -> None:
        if self.context_type != MARKET_CONTEXT:
            raise InvalidContextTypeError(self.context_type)
