"""Shared Feature contracts (feature.md): subject identity, Feature
Definition, canonical policy identifiers, authoritative events, recorded-time
causality boundary, and generic evidence normalization.

Split into its own module so all three computation engines
(`regime_passthrough.py`, `candle_window.py`, `swing_distance.py`) and the
`current_view.py` projection share exactly one definition of each of these
concepts — never redefined per engine.
"""

from __future__ import annotations

import decimal
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal, Protocol

from .envelope import EventContractRef, EventRecordRef
from .errors import (
    EvidenceCardinalityError,
    EvidenceReferenceConflictError,
    InvalidFeatureDefinitionError,
    UnresolvedOutputContractAuthorityError,
)
from .identity import deterministic_id

FeatureType = Literal["volatility_metric", "directional_persistence_metric", "distance_to_last_confirmed_swing"]
UpstreamSource = Literal["candle", "regime"]
SwingDirection = Literal["HIGH", "LOW"]
DistanceRepresentation = Literal["signed", "absolute"]

# feature.md §14's exact, closed upstream-contract-ID vocabulary — no contract ID is
# invented beyond what the Domain Contract itself already enumerates. Feature's own
# output contract IDs are feature.md §3/§4's own `id:` fields, verbatim.
CANDLE_CLOSED_CONTRACT_ID = "candle-closed"
CANDLE_CORRECTED_CONTRACT_ID = "candle-corrected"
SWING_CONFIRMED_CONTRACT_ID = "swing-confirmed"
SWING_INVALIDATED_CONTRACT_ID = "swing-invalidated"
REGIME_CLASSIFIED_CONTRACT_ID = "regime-classified"
REGIME_FACT_INVALIDATED_CONTRACT_ID = "regime-fact-invalidated"
FEATURE_COMPUTED_CONTRACT_ID = "feature-computed"
FEATURE_FACT_INVALIDATED_CONTRACT_ID = "feature-fact-invalidated"

_CANDLE_CONTRACT_IDS = frozenset({CANDLE_CLOSED_CONTRACT_ID, CANDLE_CORRECTED_CONTRACT_ID})
_REGIME_CONTRACT_IDS = frozenset({REGIME_CLASSIFIED_CONTRACT_ID, REGIME_FACT_INVALIDATED_CONTRACT_ID})
_SWING_CONTRACT_IDS = frozenset({SWING_CONFIRMED_CONTRACT_ID, SWING_INVALIDATED_CONTRACT_ID})

# P3-FEATURE-A-MAJ-02 remediation: no fabricated stand-in value (e.g. the
# former `FEATURE_EVENT_CONTRACT_VERSION = "v0"`) is invented for Feature's
# own outbound `event_contract_ref.contract_version` anymore. `stream-
# registry.yaml`/a real Event Contract version authority does not exist yet
# in this repository (Phase 1, not yet authored) — each computation engine
# now requires the caller to inject the genuine, non-empty contract version
# it authorizes at construction time (mirroring how `SequenceAllocator`'s
# `module_id`/`implementation_version`/`run_id` are already caller-supplied,
# never invented) and fails closed
# (`UnresolvedOutputContractAuthorityError`) if none is supplied — see
# `candle_window.py`/`swing_distance.py`/`regime_passthrough.py`.

# feature.md §6 "Giá trị canonical mặc định" — the exact canonical policy
# identifier strings pinned by the Domain Contract itself. Validated
# fail-closed by `FeatureDefinition`; no alias, no second canonical spelling.
INPUT_NORMALIZATION_POLICY = (
    "effective_time_window_start_asc_then_window_end_asc_then_stream_id_asc_then_registry_version_asc_"
    "then_sequence_asc_then_event_id_asc"
)
CURRENT_VIEW_SELECTION_POLICY = (
    "effective_window_end_desc_then_window_start_desc_then_recorded_time_asc_then_stream_id_asc_"
    "then_registry_version_asc_then_sequence_asc_then_event_id_asc"
)
ELIGIBLE_SWING_SELECTION_POLICY = (
    "pivot_effective_time_window_start_desc_then_recorded_time_asc_then_stream_id_asc_"
    "then_registry_version_asc_then_sequence_asc_then_swing_revision_desc_then_swing_id_asc_then_event_id_asc"
)
ELIGIBLE_SWING_EFFECTIVE_CUTOFF_POLICY = "REFERENCE_CANDLE_WINDOW_END_EXCLUSIVE"

# feature.md §6 declares warm_up_policy/missing_input_policy/
# effective_window_policy as free-form strings with NO canonical value
# pinned by the contract (unlike the four policies above) — this module pins
# ONE bounded, documented implementation value for each (module-local
# mechanism choice, not a governance decision), fail-closed on any other.
WARM_UP_POLICY = "require_full_evidence"
MISSING_INPUT_POLICY = "defer_until_resolved"
EFFECTIVE_WINDOW_POLICY = "derive_from_input_evidence"
CORRECTION_POLICY = "always_invalidate_and_replace_no_shortcut"  # feature.md §6 fixed `value:`, not a choice

_REGISTRY_VERSION = "v0"  # bounded stand-in for stream-registry.yaml (Phase 1, does not exist yet)
_OHLC_FIELDS = frozenset({"open", "high", "low", "close"})


def resolve_output_contract_refs(feature_event_contract_version: str) -> tuple[EventContractRef, EventContractRef]:
    """P3-FEATURE-A-MAJ-02 remediation — the single place every computation
    engine resolves its own outbound `(FeatureComputed, FeatureFactInvalidated)`
    `event_contract_ref`s. `feature_event_contract_version` is the exact,
    genuine, immutable contract-version identity the CALLER authorizes for
    this engine's own output (never invented here) — fails closed
    (`UnresolvedOutputContractAuthorityError`) if empty, rather than
    defaulting to a fabricated stand-in.
    """
    if not feature_event_contract_version:
        raise UnresolvedOutputContractAuthorityError(
            "feature_event_contract_version must be a genuine, non-empty contract-version identity — "
            "no stand-in value is invented for Feature's own outbound event_contract_ref (P3-FEATURE-A-MAJ-02)"
        )
    return (
        EventContractRef(FEATURE_COMPUTED_CONTRACT_ID, feature_event_contract_version),
        EventContractRef(FEATURE_FACT_INVALIDATED_CONTRACT_ID, feature_event_contract_version),
    )


@dataclass(frozen=True, slots=True)
class FeatureScope:
    """feature.md's five-field Feature Subject identity. `effective_window`
    is explicitly NOT part of identity — one continuous subject exists per
    this five-field scope.
    """

    instrument_id: str
    venue_id: str
    timeframe: str
    feature_type: FeatureType
    feature_definition_version: str

    @property
    def feature_subject_id(self) -> str:
        return deterministic_id(
            "feature",
            self.instrument_id,
            self.venue_id,
            self.timeframe,
            self.feature_type,
            self.feature_definition_version,
        )


_VALID_ROUNDINGS = frozenset(
    {
        decimal.ROUND_HALF_UP,
        decimal.ROUND_HALF_EVEN,
        decimal.ROUND_HALF_DOWN,
        decimal.ROUND_UP,
        decimal.ROUND_DOWN,
        decimal.ROUND_CEILING,
        decimal.ROUND_FLOOR,
        decimal.ROUND_05UP,
    }
)


@dataclass(frozen=True, slots=True)
class DecimalPrecisionPolicy:
    """feature.md §6 `decimal_precision_policy` — digits + a stdlib
    `decimal` rounding mode (never a hand-invented rounding scheme).
    """

    digits: int
    rounding: str

    def __post_init__(self) -> None:
        if self.digits < 0:
            raise InvalidFeatureDefinitionError(f"digits must be >= 0, got {self.digits!r}")
        if self.rounding not in _VALID_ROUNDINGS:
            raise InvalidFeatureDefinitionError(f"unsupported rounding mode: {self.rounding!r}")

    def apply(self, value: Decimal) -> Decimal:
        quantum = Decimal(1).scaleb(-self.digits)
        return value.quantize(quantum, rounding=self.rounding)


@dataclass(frozen=True, slots=True)
class FeatureDefinition:
    """feature.md §6 — Referenced Authoritative Artifact. One immutable
    definition per `feature_definition_version`, pinning exactly one
    feature_type and its own type-specific fields; contradictory or
    incomplete combinations fail closed at construction.

    Concrete formula/threshold/window-count VALUES are never invented by
    this module — they always come from whichever definition instance the
    caller constructs (feature.md §6's own "không hardcode một trường phái"
    principle, mirrored from swing_definition/structure_definition/
    regime_definition).
    """

    feature_definition_id: str
    feature_definition_version: str
    feature_type: FeatureType
    unit: str
    decimal_precision_policy: DecimalPrecisionPolicy
    warm_up_policy: str
    missing_input_policy: str
    correction_policy: str
    effective_window_policy: str
    current_view_selection_policy: str
    input_normalization_policy: str
    # volatility_metric / directional_persistence_metric only:
    upstream_source: UpstreamSource | None = None
    upstream_contract_refs: tuple[EventContractRef, ...] | None = None
    required_upstream_definition_version: str | None = None
    window_candle_count: int | None = None
    formula_id: str | None = None
    # distance_to_last_confirmed_swing only:
    swing_direction: SwingDirection | None = None
    distance_representation: DistanceRepresentation | None = None
    reference_price_field: str | None = None
    eligible_swing_selection_policy: str | None = None
    eligible_swing_effective_cutoff_policy: str | None = None
    required_swing_definition_version: str | None = None
    normalization_policy: str | None = None

    def __post_init__(self) -> None:
        if not self.feature_definition_id:
            raise InvalidFeatureDefinitionError("feature_definition_id must be non-empty")
        if not self.feature_definition_version:
            raise InvalidFeatureDefinitionError("feature_definition_version must be non-empty")
        if not self.unit:
            raise InvalidFeatureDefinitionError("unit must be non-empty")
        if self.correction_policy != CORRECTION_POLICY:
            raise InvalidFeatureDefinitionError(f"unsupported correction_policy: {self.correction_policy!r}")
        if self.input_normalization_policy != INPUT_NORMALIZATION_POLICY:
            raise InvalidFeatureDefinitionError(
                f"unsupported input_normalization_policy: {self.input_normalization_policy!r}"
            )
        if self.current_view_selection_policy != CURRENT_VIEW_SELECTION_POLICY:
            raise InvalidFeatureDefinitionError(
                f"unsupported current_view_selection_policy: {self.current_view_selection_policy!r}"
            )
        if self.warm_up_policy != WARM_UP_POLICY:
            raise InvalidFeatureDefinitionError(f"unsupported warm_up_policy: {self.warm_up_policy!r}")
        if self.missing_input_policy != MISSING_INPUT_POLICY:
            raise InvalidFeatureDefinitionError(f"unsupported missing_input_policy: {self.missing_input_policy!r}")
        if self.effective_window_policy != EFFECTIVE_WINDOW_POLICY:
            raise InvalidFeatureDefinitionError(
                f"unsupported effective_window_policy: {self.effective_window_policy!r}"
            )

        distance_only_fields = (
            self.swing_direction,
            self.distance_representation,
            self.reference_price_field,
            self.eligible_swing_selection_policy,
            self.eligible_swing_effective_cutoff_policy,
            self.required_swing_definition_version,
        )
        metric_only_fields = (
            self.upstream_source,
            self.upstream_contract_refs,
            self.required_upstream_definition_version,
        )

        if self.feature_type in ("volatility_metric", "directional_persistence_metric"):
            if any(field is not None for field in distance_only_fields) or self.normalization_policy is not None:
                raise InvalidFeatureDefinitionError(
                    f"{self.feature_type} must not set distance_to_last_confirmed_swing-only fields"
                )
            if self.upstream_source is None:
                raise InvalidFeatureDefinitionError("upstream_source is required for this feature_type")
            if not self.upstream_contract_refs:
                raise InvalidFeatureDefinitionError(
                    "upstream_contract_refs is required (non-empty) for volatility_metric/"
                    "directional_persistence_metric (feature.md §6)"
                )
            allowed_contract_ids = _CANDLE_CONTRACT_IDS if self.upstream_source == "candle" else _REGIME_CONTRACT_IDS
            for contract_ref in self.upstream_contract_refs:
                if contract_ref.contract_id not in allowed_contract_ids:
                    raise InvalidFeatureDefinitionError(
                        f"upstream_contract_refs contains contract_id={contract_ref.contract_id!r}, not valid for "
                        f"upstream_source={self.upstream_source!r} (must be one of {sorted(allowed_contract_ids)!r} "
                        "— feature.md §6: 'PHẢI khớp đúng upstream_source đã chọn, không được trộn')"
                    )
            if self.upstream_source == "candle":
                if self.required_upstream_definition_version is not None:
                    raise InvalidFeatureDefinitionError(
                        "required_upstream_definition_version must be None when upstream_source=candle "
                        "(dual upstream source)"
                    )
                if self.window_candle_count is None or self.window_candle_count < 1:
                    raise InvalidFeatureDefinitionError(
                        "window_candle_count (>=1) is required for upstream_source=candle"
                    )
                if not self.formula_id:
                    raise InvalidFeatureDefinitionError("formula_id is required for upstream_source=candle")
            elif self.upstream_source == "regime":
                if self.window_candle_count is not None or self.formula_id is not None:
                    raise InvalidFeatureDefinitionError(
                        "window_candle_count/formula_id must be None when upstream_source=regime (dual upstream source)"
                    )
                if not self.required_upstream_definition_version:
                    raise InvalidFeatureDefinitionError(
                        "required_upstream_definition_version is required for upstream_source=regime"
                    )
            else:
                raise InvalidFeatureDefinitionError(f"unsupported upstream_source: {self.upstream_source!r}")
        elif self.feature_type == "distance_to_last_confirmed_swing":
            if (
                any(field is not None for field in metric_only_fields)
                or self.window_candle_count is not None
                or (self.formula_id is not None)
            ):
                raise InvalidFeatureDefinitionError(
                    "distance_to_last_confirmed_swing must not set volatility/directional_persistence-only fields"
                )
            if self.swing_direction not in ("HIGH", "LOW"):
                raise InvalidFeatureDefinitionError(f"invalid swing_direction: {self.swing_direction!r}")
            if self.distance_representation not in ("signed", "absolute"):
                raise InvalidFeatureDefinitionError(
                    f"invalid distance_representation: {self.distance_representation!r}"
                )
            if self.reference_price_field not in _OHLC_FIELDS:
                raise InvalidFeatureDefinitionError(f"invalid reference_price_field: {self.reference_price_field!r}")
            if self.eligible_swing_selection_policy != ELIGIBLE_SWING_SELECTION_POLICY:
                raise InvalidFeatureDefinitionError(
                    f"unsupported eligible_swing_selection_policy: {self.eligible_swing_selection_policy!r}"
                )
            if self.eligible_swing_effective_cutoff_policy != ELIGIBLE_SWING_EFFECTIVE_CUTOFF_POLICY:
                raise InvalidFeatureDefinitionError(
                    "unsupported eligible_swing_effective_cutoff_policy: "
                    f"{self.eligible_swing_effective_cutoff_policy!r}"
                )
            if not self.required_swing_definition_version:
                raise InvalidFeatureDefinitionError("required_swing_definition_version is required")
        else:
            raise InvalidFeatureDefinitionError(f"unsupported feature_type: {self.feature_type!r}")


@dataclass(frozen=True, slots=True)
class FeatureComputed:
    """feature.md §3 — one completed valid computation point. Emitted for
    EVERY completed valid computation point, even when `value` repeats the
    previous point's — no "no-op if unchanged" shortcut.
    """

    scope: FeatureScope
    value: Decimal
    unit: str
    window_start: datetime
    window_end: datetime
    input_fact_refs: tuple[EventRecordRef, ...]
    supersedes_fact_ref: EventRecordRef | None
    causation_refs: tuple[EventRecordRef, ...]
    recorded_time: datetime
    ref: EventRecordRef
    event_contract_ref: EventContractRef


InvalidationCause = Literal["candle_corrected", "regime_fact_invalidated", "swing_invalidated"]


@dataclass(frozen=True, slots=True)
class FeatureFactInvalidated:
    """feature.md §4 — `scope`/`window_start`/`window_end` are inherited
    byte-for-byte from the invalidated fact, never independently declared.
    """

    scope: FeatureScope
    invalidated_fact_ref: EventRecordRef
    invalidation_cause: InvalidationCause
    window_start: datetime
    window_end: datetime
    causation_refs: tuple[EventRecordRef, ...]
    recorded_time: datetime
    ref: EventRecordRef
    event_contract_ref: EventContractRef


FeatureEvent = FeatureComputed | FeatureFactInvalidated


class RecordedTimeSource(Protocol):
    """A bounded, injected knowledge-time provider for Feature events.

    feature.md §3/§4 pin strict recorded_time causality (an original fact's
    recorded_time must be later than its evidence's; an invalidation's must
    be later than both the fact it targets and the causing upstream event; a
    replacement's must be later than its own invalidation) but never
    specifies a concrete clock/allocation mechanism (Chapter 5 §5.4 defers
    that to the owning module) — this engine never fabricates a knowledge
    time itself; it asks the injected provider and independently validates
    `result > strict_floor`, failing closed
    (`RecordedTimeSourceViolationError`) otherwise. A real wall-clock/
    runtime implementation of this Protocol lives outside this analytical
    core.
    """

    def next_after(self, strict_floor: datetime) -> datetime: ...


def normalize_input_facts[T](
    facts: Sequence[T],
    *,
    effective_time: Callable[[T], tuple[datetime, datetime]],
    ref_of: Callable[[T], EventRecordRef],
    expected_count: int,
) -> tuple[EventRecordRef, ...]:
    """feature.md §8a canonical input evidence normalization, generalized
    over any authoritative fact type (Candle/Swing/Regime) via the two
    caller-supplied extraction functions — the 6-criterion lexicographic
    order and dedup/conflict semantics are implemented exactly once here,
    not duplicated per engine.

    Fails closed (`EvidenceReferenceConflictError`) if the same ref resolves
    to materially different fact content (full structural equality on the
    frozen dataclass, never narrowed to a subset of fields). Fails closed
    (`EvidenceCardinalityError`) if, after dedup, the normalized evidence
    does not contain exactly `expected_count` unique refs.
    """
    deduped: dict[EventRecordRef, T] = {}
    for fact in facts:
        ref = ref_of(fact)
        existing = deduped.get(ref)
        if existing is not None and existing != fact:
            raise EvidenceReferenceConflictError(
                f"ref {ref!r} resolves to conflicting fact content ({existing!r} vs {fact!r})"
            )
        deduped[ref] = fact

    def _sort_key(fact: T) -> tuple[datetime, datetime, str, str, int, str]:
        start, end = effective_time(fact)
        ref = ref_of(fact)
        return (start, end, ref.stream_id, _REGISTRY_VERSION, ref.sequence, ref.event_id)

    ordered = sorted(deduped.values(), key=_sort_key)
    if len(ordered) != expected_count:
        raise EvidenceCardinalityError(
            f"normalized evidence has {len(ordered)} unique ref(s), expected exactly {expected_count}"
        )
    return tuple(ref_of(fact) for fact in ordered)
