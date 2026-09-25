"""Context's own minimal consumer-side representations for exactly the seven
upstream fact roles context.md §7 defines: the Candle cutoff/cadence source
(§7.0), Structure (§7.1), the two independent Regime dimensions (§7.2), and
the three founding Feature types (§7.3).

These are Context-local views, not imports of any producer module's own
domain types — module-registry.yaml's `depends_on` names a permitted event/
contract relationship (`feature-context-architecture.md` §2), never a
license to import another module's implementation package. This module
never imports `feature_engine`, `structure_engine`, `raw_regime_engine`, or
any Go module code.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum

from context_aggregator.refs import EffectiveWindow, EventRecordRef


class StructureFactKind(Enum):
    """The three authoritative Structure event types context.md §7.1
    permits as the Structure role's candidate type — exactly one of these
    per Eligible Structure fact."""

    BREAK_OF_STRUCTURE_DETECTED = "break_of_structure_detected"
    CHANGE_OF_CHARACTER_DETECTED = "change_of_character_detected"
    STRUCTURE_RECOMPUTED = "structure_recomputed"


class StructureOrientation(Enum):
    """context.md §3 `context_values.structure_orientation` closed enum.
    `UNDETERMINED` never appears here — absence is represented by producing
    no candidate at all (§9), never a value."""

    NEUTRAL = "NEUTRAL"
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"


class RegimeDimension(Enum):
    """The two required, independent Regime dimensions (context.md §7.2)."""

    VOLATILITY = "volatility"
    DIRECTIONAL_PERSISTENCE = "directional_persistence"


class VolatilityRegimeClass(Enum):
    """context.md §3 `context_values.volatility_regime_class` closed enum."""

    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    EXTREME = "EXTREME"


class DirectionalPersistenceRegimeClass(Enum):
    """context.md §3 `context_values.directional_persistence_regime_class`
    closed enum."""

    NON_DIRECTIONAL = "NON_DIRECTIONAL"
    DIRECTIONAL = "DIRECTIONAL"
    TRANSITIONAL = "TRANSITIONAL"


class FeatureType(Enum):
    """The three required founding Feature types (context.md §7.3)."""

    VOLATILITY_METRIC = "volatility_metric"
    DIRECTIONAL_PERSISTENCE_METRIC = "directional_persistence_metric"
    DISTANCE_TO_LAST_CONFIRMED_SWING = "distance_to_last_confirmed_swing"


@dataclass(frozen=True, slots=True)
class CandleFact:
    """Consumer-side view of a `candle-closed`/`candle-corrected`
    authoritative fact (context.md §7.0) — Context's cadence/cutoff driver,
    NOT one of the six `context_values` roles.

    `supersedes_ref` is set exactly when this fact is a `candle-corrected`
    replacing a prior fact for the same window (candle.md §10 correction
    lineage) — used by Phase 1 step 4's lineage-head resolution (§8).
    """

    ref: EventRecordRef
    recorded_time: datetime
    instrument_id: str
    venue_id: str
    timeframe: str
    effective_window: EffectiveWindow
    supersedes_ref: EventRecordRef | None = None


@dataclass(frozen=True, slots=True)
class StructureFact:
    """Consumer-side view of exactly one of `break-of-structure-detected` /
    `change-of-character-detected` / `structure-recomputed` (context.md
    §7.1). `effective_time` is a single point (structure.md §2), not a
    window."""

    ref: EventRecordRef
    recorded_time: datetime
    instrument_id: str
    venue_id: str
    timeframe: str
    effective_time: datetime
    definition_version: str
    kind: StructureFactKind
    orientation: StructureOrientation


@dataclass(frozen=True, slots=True)
class RegimeFact:
    """Consumer-side view of a `regime-classified` fact for one of the two
    required, independent dimensions (context.md §7.2).

    `supersedes_ref` is set exactly when this fact is a correction
    replacement for a prior `RegimeFact` of the same dimension/scope
    (regime.md's own correction lineage, referenced not redefined here) —
    used by Phase 2's lineage-head resolution (§8).
    """

    ref: EventRecordRef
    recorded_time: datetime
    instrument_id: str
    venue_id: str
    timeframe: str
    analysis_window: EffectiveWindow
    definition_version: str
    regime_dimension: RegimeDimension
    regime_class: VolatilityRegimeClass | DirectionalPersistenceRegimeClass
    supersedes_ref: EventRecordRef | None = None


@dataclass(frozen=True, slots=True)
class FeatureFact:
    """Consumer-side view of a `feature-computed` fact for one of the three
    required founding feature types (context.md §7.3).

    `supersedes_ref` is set exactly when this fact is a correction
    replacement for a prior `FeatureFact` of the same feature_type/scope
    (feature.md's own correction lineage, referenced not redefined here) —
    used by Phase 2's lineage-head resolution (§8). `value` is preserved as
    `Decimal` throughout this core — never round-tripped through `float`.
    """

    ref: EventRecordRef
    recorded_time: datetime
    instrument_id: str
    venue_id: str
    timeframe: str
    effective_window: EffectiveWindow
    definition_version: str
    feature_type: FeatureType
    value: Decimal
    supersedes_ref: EventRecordRef | None = None
