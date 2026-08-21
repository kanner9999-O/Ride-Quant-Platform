"""Raw Regime — authoritative regime classification (`docs/domain/regime.md`).

Implements the engine GENERICALLY over an explicit, immutable
`RegimeDefinition`: this module invents no canonical ATR/ADX/efficiency-ratio/
realized-volatility/trend-score/moving-average formula and no production
threshold values (regime.md deliberately does not select one — see §19). A
caller supplies both a `RegimeDefinition` (thresholds/policies) and a
`MetricFormula` implementation whose own `formula_id` must match the
definition's pinned `metric_formula_id`; the engine fails closed
(`FormulaMismatchError`) if they disagree, and there is no global formula
registry to fall back on.

Two dimensions only, per regime.md's own closed scope: `volatility`
(`LOW|NORMAL|HIGH|EXTREME`) and `directional_persistence`
(`NON_DIRECTIONAL|DIRECTIONAL|TRANSITIONAL`). No Activity/Liquidity/
Structure-aware regime — those responsibilities are explicitly deferred
elsewhere (module-registry.yaml's own "DEFERRED COVERAGE" note on this
module, blocked on Domain Context/Capability registration, out of this
module's scope).

Never imports Structure/Swing/Feature/Context/Strategy/Account/Risk —
ADR-014's independence from Structure is structural: this package simply
never references `structure_engine`, by construction.

`RegimeClassified`/`RegimeFactInvalidated`'s own `recorded_time` is never
copied from Candle `recorded_time` — regime.md §3/§4 require it to be
strictly later than specific causal floors (max evidence recorded_time for
an original fact; the invalidated fact's and the causing CandleCorrected's
recorded_time for an invalidation; the invalidation's recorded_time for a
replacement). The engine asks an injected `RecordedTimeSource` for each
knowledge time and validates the causal-floor invariant itself — production
wall-clock/runtime time generation lives outside this analytical core.
"""

from __future__ import annotations

import decimal
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from types import MappingProxyType
from typing import Protocol

from .candle import CandleFact
from .envelope import EventRecordRef
from .errors import (
    DuplicateCandleConflictError,
    EvidenceCardinalityError,
    EvidenceReferenceConflictError,
    ForeignScopeError,
    FormulaMismatchError,
    NonMonotonicRecordedTimeError,
    OutOfOrderCandleError,
    OutOfOrderCorrectionError,
    RecordedTimeSourceViolationError,
    RegimeLineageError,
)
from .identity import deterministic_id
from .publish import SequenceAllocator

# regime.md §6 — the exact two canonical policy-identifier strings pinned by
# the Domain Contract itself (not this module's invention — copied verbatim
# from regime.md §6's `regime_definition` schema block). `RegimeDefinition`
# validates a candidate value against these fail-closed; there is no second
# canonical spelling and no alias.
CANDLE_EVIDENCE_NORMALIZATION_POLICY = (
    "window_start_asc_then_window_end_asc_then_stream_id_asc_then_registry_version_asc_"
    "then_sequence_asc_then_event_id_asc"
)
CURRENT_VIEW_SELECTION_POLICY = (
    "analysis_window_end_desc_then_window_start_desc_then_recorded_time_asc_then_stream_id_asc_"
    "then_registry_version_asc_then_sequence_asc_then_event_id_asc"
)

# Bounded stand-in for the stream-registry.yaml infrastructure that does not
# exist yet (Phase 1) — same role/value as structure-engine's own constant of
# this kind. Not real infrastructure; every Candle evidence ref is treated as
# belonging to this one pinned registry_version for normalization purposes.
_REGISTRY_VERSION = "v0"

# regime.md §2/§9 — the closed label vocabulary per dimension. A domain fact
# (this module does not invent these), not implementation choice.
_ALLOWED_LABELS: dict[str, frozenset[str]] = {
    "volatility": frozenset({"LOW", "NORMAL", "HIGH", "EXTREME"}),
    "directional_persistence": frozenset({"NON_DIRECTIONAL", "DIRECTIONAL", "TRANSITIONAL"}),
}

# regime.md §1 invariants — "regime_dimension là enum đóng ở v0.1"; a
# configured RegimeDefinition must realize BOTH, exactly (B2 scope) — no
# missing, no extra/unknown dimension.
_REQUIRED_DIMENSIONS = frozenset(_ALLOWED_LABELS.keys())

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
class RegimeScope:
    """regime.md's five-field Regime Subject identity.

    `analysis_window` is explicitly NOT part of identity — one continuous
    subject exists per this five-field scope, and every completed window of
    that subject produces facts against the SAME `regime_subject_id`.
    """

    instrument_id: str
    venue_id: str
    timeframe: str
    regime_dimension: str
    regime_definition_version: str

    @property
    def regime_subject_id(self) -> str:
        return deterministic_id(
            "regime",
            self.instrument_id,
            self.venue_id,
            self.timeframe,
            self.regime_dimension,
            self.regime_definition_version,
        )


class MetricFormula(Protocol):
    """A bounded, injected metric computation — never resolved from a global
    registry. `formula_id` must match the `RegimeDimensionDefinition`'s own
    `metric_formula_id` for the engine to accept it (`FormulaMismatchError`
    otherwise). Test-only implementations must use a `formula_id` that is
    obviously not a production identifier (e.g. a `test-` prefix) and must
    never be documented as a production canonical formula.
    """

    formula_id: str

    def compute(self, evidence: Sequence[CandleFact]) -> Decimal:
        """Compute the raw (pre-precision-policy) metric over one window's
        evidence, supplied in regime.md §8a canonical normalized order.
        """
        ...


class RecordedTimeSource(Protocol):
    """A bounded, injected knowledge-time provider for Regime events.

    regime.md §3/§4 pin strict recorded_time causality (an original fact's
    recorded_time must be later than its evidence's; an invalidation's must
    be later than both the fact it targets and the causing CandleCorrected;
    a replacement's must be later than its own invalidation) — but never
    specifies a concrete clock/allocation mechanism (Chapter 5 §5.4 defers
    that to the owning module). This engine never fabricates a knowledge
    time itself (e.g. by adding an arbitrary delta to Candle time inside
    production core) — it asks the injected provider and validates the
    result itself, failing closed if the provider violates the causal floor.

    Production wall-clock/runtime implementations of this Protocol live
    outside this analytical core (the same "analytical core only" boundary
    already stated for broker/RPC/deployment concerns). Test-only
    implementations must not be documented as production time authority.
    """

    def next_after(self, strict_floor: datetime) -> datetime:
        """Return a knowledge time strictly later than `strict_floor`.

        The caller (this engine) independently validates `result >
        strict_floor` and raises `RecordedTimeSourceViolationError` if the
        provider fails to honor that contract — the provider's own
        correctness is never trusted blindly.
        """
        ...


@dataclass(frozen=True, slots=True)
class ThresholdBand:
    """One ascending classification band. `upper_bound=None` marks the
    single, mandatory open-ended top band (must be last).
    """

    upper_bound: Decimal | None
    label: str


@dataclass(frozen=True, slots=True)
class DecimalPrecisionPolicy:
    """`regime.md` §6 `decimal_precision_policy` — digits + a stdlib
    `decimal` rounding mode (never a hand-invented rounding scheme).
    """

    digits: int
    rounding: str

    def __post_init__(self) -> None:
        if self.digits < 0:
            raise ValueError(f"digits must be >= 0, got {self.digits!r}")
        if self.rounding not in _VALID_ROUNDINGS:
            raise ValueError(f"unsupported rounding mode: {self.rounding!r}")

    def apply(self, value: Decimal) -> Decimal:
        quantum = Decimal(1).scaleb(-self.digits)
        return value.quantize(quantum, rounding=self.rounding)


@dataclass(frozen=True, slots=True)
class RegimeDimensionDefinition:
    """Per-dimension fields of `regime.md` §6's `regime_definition` schema.

    Threshold *values* are never invented here — they come from whichever
    immutable definition instance the caller constructs; this module only
    pins the generic, bounded classification MECHANISM (ascending band scan,
    strict/inclusive comparison), analogous to how structure-engine pins one
    bounded tie-break mechanism for a domain contract that leaves the
    concrete algorithm unspecified.
    """

    window_candle_count: int
    metric_formula_id: str
    class_thresholds: tuple[ThresholdBand, ...]
    threshold_comparison_policy: str
    warm_up_policy: str
    gap_policy: str
    decimal_precision_policy: DecimalPrecisionPolicy

    def __post_init__(self) -> None:
        if self.window_candle_count < 1:
            raise ValueError(f"window_candle_count must be >= 1, got {self.window_candle_count!r}")
        if not self.class_thresholds:
            raise ValueError("class_thresholds must be non-empty")
        *bounded_bands, last_band = self.class_thresholds
        if last_band.upper_bound is not None:
            raise ValueError("the last threshold band must be open-ended (upper_bound=None)")
        bounds: list[Decimal] = []
        for band in bounded_bands:
            if band.upper_bound is None:
                raise ValueError("only the last threshold band may have upper_bound=None")
            bounds.append(band.upper_bound)
        if bounds != sorted(bounds) or len(set(bounds)) != len(bounds):
            raise ValueError("class_thresholds must be strictly ascending by upper_bound")
        if self.threshold_comparison_policy not in ("strict", "inclusive"):
            raise ValueError(f"unsupported threshold_comparison_policy: {self.threshold_comparison_policy!r}")
        # The only warm-up/gap behaviors regime.md §7 describes — validated
        # fail-closed rather than silently accepted as an unrecognized value.
        if self.warm_up_policy != "require_full_window":
            raise ValueError(f"unsupported warm_up_policy: {self.warm_up_policy!r}")
        if self.gap_policy != "defer_until_resolved":
            raise ValueError(f"unsupported gap_policy: {self.gap_policy!r}")


def _canonical_field(value: object) -> str:
    if isinstance(value, Decimal):
        return f"Decimal({value!s})"
    return str(value)


def _dimension_content_repr(dimension: RegimeDimensionDefinition) -> str:
    bands = ";".join(f"{_canonical_field(band.upper_bound)}:{band.label}" for band in dimension.class_thresholds)
    return "|".join(
        [
            f"window_candle_count={dimension.window_candle_count}",
            f"metric_formula_id={dimension.metric_formula_id}",
            f"class_thresholds=[{bands}]",
            f"threshold_comparison_policy={dimension.threshold_comparison_policy}",
            f"warm_up_policy={dimension.warm_up_policy}",
            f"gap_policy={dimension.gap_policy}",
            "decimal_precision_policy="
            f"{dimension.decimal_precision_policy.digits}:{dimension.decimal_precision_policy.rounding}",
        ]
    )


@dataclass(frozen=True, slots=True)
class RegimeDefinition:
    """`regime.md` §6's full `regime_definition` — module-level policies plus
    exactly one `RegimeDimensionDefinition` per required dimension.

    A genuinely immutable in-memory snapshot: the caller-supplied
    `dimensions` mapping is defensively copied at construction and exposed
    only through a read-only `MappingProxyType` view — neither mutating the
    caller's original mapping after construction, nor attempting to mutate
    the exposed view, can alter this instance. Nested components
    (`RegimeDimensionDefinition`/`ThresholdBand`/`DecimalPrecisionPolicy`)
    are already frozen dataclasses with tuple-typed fields, so immutability
    is deep, not just shallow.

    `content_identity()` provides a deterministic SHA-256 fingerprint over
    the full canonical content (including `regime_definition_version`) for
    external run-manifest evidence — it is verification evidence, NOT a
    replacement for `regime_definition_version`, which remains the opaque
    semantic version pinned by the contract (§1). This module invents no
    definition registry/storage/lifecycle authority — that remains deferred
    by regime.md §19/§20.
    """

    regime_definition_version: str
    dimensions: Mapping[str, RegimeDimensionDefinition]
    current_view_selection_policy: str
    candle_evidence_normalization_policy: str

    def __post_init__(self) -> None:
        if self.candle_evidence_normalization_policy != CANDLE_EVIDENCE_NORMALIZATION_POLICY:
            raise ValueError(
                f"unsupported candle_evidence_normalization_policy: {self.candle_evidence_normalization_policy!r}"
            )
        if self.current_view_selection_policy != CURRENT_VIEW_SELECTION_POLICY:
            raise ValueError(f"unsupported current_view_selection_policy: {self.current_view_selection_policy!r}")

        # Defensive copy — the caller's own mapping object is never retained;
        # later mutation of it (or attempted mutation of the exposed
        # MappingProxyType view below) cannot alter this instance.
        dimensions_copy = dict(self.dimensions)
        if set(dimensions_copy.keys()) != _REQUIRED_DIMENSIONS:
            raise ValueError(
                f"dimensions must contain exactly {sorted(_REQUIRED_DIMENSIONS)!r}, "
                f"got {sorted(dimensions_copy.keys())!r}"
            )
        for dimension_name, dimension_definition in dimensions_copy.items():
            allowed = _ALLOWED_LABELS[dimension_name]
            labels_used = [band.label for band in dimension_definition.class_thresholds]
            if set(labels_used) != allowed or len(labels_used) != len(allowed):
                raise ValueError(
                    f"dimension {dimension_name!r} class_thresholds must contain exactly the "
                    f"labels {sorted(allowed)!r} each exactly once, got {labels_used!r}"
                )
        object.__setattr__(self, "dimensions", MappingProxyType(dimensions_copy))

    def content_identity(self) -> str:
        """Deterministic content fingerprint — same canonical content always
        produces the same identity; any field change produces a different
        one. Suitable as external run-manifest evidence of exactly which
        immutable definition snapshot a run used.
        """
        dimension_parts = tuple(
            f"{name}={_dimension_content_repr(dimension)}" for name, dimension in sorted(self.dimensions.items())
        )
        return deterministic_id(
            "regime-definition",
            self.regime_definition_version,
            self.current_view_selection_policy,
            self.candle_evidence_normalization_policy,
            *dimension_parts,
        )

    def __hash__(self) -> int:
        return hash(self.content_identity())


@dataclass(frozen=True, slots=True)
class RegimeClassified:
    """regime.md §3 — one completed window's classification. Emitted for
    EVERY completed valid window (§9), even when `class_label` repeats the
    previous window's — there is no "no-op if unchanged" shortcut for Raw
    Regime, unlike Swing/Structure.
    """

    scope: RegimeScope
    class_label: str
    computed_metric: Decimal
    window_start: datetime
    window_end: datetime
    candle_evidence_refs: tuple[EventRecordRef, ...]
    supersedes_fact_ref: EventRecordRef | None
    causation_refs: tuple[EventRecordRef, ...]
    recorded_time: datetime
    ref: EventRecordRef


@dataclass(frozen=True, slots=True)
class RegimeFactInvalidated:
    """regime.md §4 — `scope`/`window_start`/`window_end` are inherited
    byte-for-byte from the invalidated fact, never independently declared.
    """

    scope: RegimeScope
    invalidated_fact_ref: EventRecordRef
    window_start: datetime
    window_end: datetime
    causation_refs: tuple[EventRecordRef, ...]
    recorded_time: datetime
    ref: EventRecordRef


RegimeEvent = RegimeClassified | RegimeFactInvalidated


def _evidence_sort_key(candle: CandleFact) -> tuple[datetime, datetime, str, str, int, str]:
    return (
        candle.scope.window_start,
        candle.scope.window_end,
        candle.ref.stream_id,
        _REGISTRY_VERSION,
        candle.ref.sequence,
        candle.ref.event_id,
    )


def normalize_evidence(candles: Sequence[CandleFact], *, expected_count: int) -> tuple[EventRecordRef, ...]:
    """regime.md §8a canonical Candle evidence normalization.

    Strict lexicographic order — window_start ASC, window_end ASC, stream_id
    ASC, registry_version ASC, sequence ASC (only meaningful when 3/4 tie,
    i.e. within the same stream), event_id ASC — with dedup by event-record
    ref (two references resolving the same Candle fact keep exactly one).
    Independent of input order: the same underlying evidence set always
    normalizes to the same output tuple (regime.md §8b identity).

    Fails closed (`EvidenceReferenceConflictError`) if the same ref is
    supplied more than once with a `CandleFact` that differs in ANY
    semantic/event-record field (`scope`, `ohlcv`, `recorded_time`,
    `is_correction` — `ref` is already equal by construction of this check)
    — one `EventRecordRef` must resolve exactly one authoritative
    `CandleFact` representation; a mismatch on any single field is never
    silently resolved via last-write-wins, and this is never narrowed to an
    OHLCV-only comparison. `CandleFact` is a frozen dataclass, so full
    structural equality (`!=`) already compares every field at once. Fails
    closed (`EvidenceCardinalityError`) if, after dedup, the normalized
    evidence does not contain exactly `expected_count` unique refs — the
    caller must never publish `candle_evidence_refs` with a cardinality that
    silently differs from what was actually computed over.
    """
    deduped: dict[EventRecordRef, CandleFact] = {}
    for candle in candles:
        existing = deduped.get(candle.ref)
        if existing is not None and existing != candle:
            raise EvidenceReferenceConflictError(
                f"ref {candle.ref!r} resolves to conflicting Candle content ({existing!r} vs {candle!r})"
            )
        deduped[candle.ref] = candle
    ordered = sorted(deduped.values(), key=_evidence_sort_key)
    if len(ordered) != expected_count:
        raise EvidenceCardinalityError(
            f"normalized evidence has {len(ordered)} unique ref(s), expected exactly {expected_count}"
        )
    return tuple(candle.ref for candle in ordered)


def _classify(metric: Decimal, bands: tuple[ThresholdBand, ...], comparison: str) -> str:
    for band in bands:
        if band.upper_bound is None:
            return band.label
        if comparison == "strict":
            if metric < band.upper_bound:
                return band.label
        elif metric <= band.upper_bound:
            return band.label
    raise AssertionError("unreachable: RegimeDimensionDefinition guarantees an open-ended last band")


@dataclass(slots=True)
class _WindowLineage:
    head_fact: RegimeClassified


class RegimeEngine:
    """Pure, deterministic, in-process Raw Regime engine for exactly one
    (instrument_id, venue_id, timeframe, regime_dimension,
    regime_definition_version) subject.

    Same authoritative code path for Replay/Backtest/Paper/Live (Chapter 3
    §3.1): regime.md §9 requires EVERY completed window to emit exactly one
    `RegimeClassified` regardless of mode, so — unlike Swing, which has a
    provisional Candidate stage to suppress in historical mode — there is
    only one algorithm here, not a historical/streaming split. A caller
    drives this engine by calling `on_candle` in cursor order (no
    look-ahead: no Candle beyond the position being processed is ever
    consulted).

    One instance per subject — evidence/lineage bookkeeping is scoped to
    this single (instrument, venue, timeframe) from construction (unlike
    Swing's own multi-scope multiplexing), so ordering discipline and
    foreign-scope rejection are per-instance by construction, not a
    retrofitted dict-keyed mechanism.

    Every emitted event's own `recorded_time` is obtained from an injected
    `RecordedTimeSource`, never copied from Candle `recorded_time` — see
    that Protocol's docstring and `_next_recorded_time` below for the exact
    causal-floor validation performed for each of the three cases (original,
    invalidation, replacement).
    """

    def __init__(
        self,
        scope: RegimeScope,
        definition: RegimeDefinition,
        formula: MetricFormula,
        allocator: SequenceAllocator,
        time_source: RecordedTimeSource,
        *,
        stream_id: str = "regime",
    ) -> None:
        if scope.regime_dimension not in _ALLOWED_LABELS:
            raise ValueError(f"unsupported regime_dimension: {scope.regime_dimension!r}")
        if scope.regime_definition_version != definition.regime_definition_version:
            raise ValueError("scope.regime_definition_version must match definition.regime_definition_version")
        dimension_definition = definition.dimensions.get(scope.regime_dimension)
        if dimension_definition is None:
            raise ValueError(f"definition has no configuration for dimension {scope.regime_dimension!r}")
        if formula.formula_id != dimension_definition.metric_formula_id:
            raise FormulaMismatchError(
                f"formula.formula_id={formula.formula_id!r} does not match "
                f"definition.metric_formula_id={dimension_definition.metric_formula_id!r}"
            )
        self.scope = scope
        self.definition = definition
        self._dimension_definition = dimension_definition
        self._formula = formula
        self._allocator = allocator
        self._time_source = time_source
        self._stream_id = stream_id
        self._candles: list[CandleFact] = []
        self._candle_index: dict[str, int] = {}
        self._last_recorded_time: datetime | None = None
        self._window_lineage: dict[tuple[datetime, datetime], _WindowLineage] = {}

    def _check_scope(self, candle: CandleFact) -> None:
        if (
            candle.scope.instrument_id != self.scope.instrument_id
            or candle.scope.venue_id != self.scope.venue_id
            or candle.scope.timeframe != self.scope.timeframe
        ):
            raise ForeignScopeError(f"candle scope {candle.scope!r} does not match engine scope {self.scope!r}")

    def _check_recorded_time(self, recorded_time: datetime) -> None:
        """Per-scope, per-engine INPUT (Candle) ordering discipline — a
        separate concern from this engine's OWN emitted-event recorded_time
        causality (`_next_recorded_time` below).
        """
        if self._last_recorded_time is not None and recorded_time < self._last_recorded_time:
            raise NonMonotonicRecordedTimeError(
                f"recorded_time {recorded_time!r} precedes last-seen {self._last_recorded_time!r}"
            )
        self._last_recorded_time = recorded_time

    def _next_recorded_time(self, strict_floor: datetime) -> datetime:
        candidate = self._time_source.next_after(strict_floor)
        if not candidate > strict_floor:
            raise RecordedTimeSourceViolationError(
                f"RecordedTimeSource.next_after({strict_floor!r}) returned {candidate!r}, "
                "which is not strictly later than the required causal floor"
            )
        return candidate

    def on_candle(self, fact: CandleFact) -> list[RegimeEvent]:
        self._check_scope(fact)
        subject_id = fact.scope.subject_id
        existing_index = self._candle_index.get(subject_id)

        if existing_index is not None:
            existing = self._candles[existing_index]
            if existing.ohlcv == fact.ohlcv:
                return []  # duplicate computation idempotency
            if not fact.is_correction:
                raise DuplicateCandleConflictError(
                    f"candle {subject_id!r} resubmitted with different content but is_correction=False"
                )
            self._check_recorded_time(fact.recorded_time)
            self._candles[existing_index] = fact
            return self._reevaluate_windows_covering(existing_index, fact.ref, fact.recorded_time)

        if fact.is_correction:
            raise OutOfOrderCorrectionError(f"correction submitted for never-seen candle {subject_id!r}")
        if self._candles and fact.scope.window_start < self._candles[-1].scope.window_start:
            raise OutOfOrderCandleError(
                f"candle window_start {fact.scope.window_start!r} precedes last-seen "
                f"{self._candles[-1].scope.window_start!r}"
            )
        self._check_recorded_time(fact.recorded_time)
        self._candles.append(fact)
        new_index = len(self._candles) - 1
        self._candle_index[subject_id] = new_index
        return self._try_classify_window_ending_at(new_index)

    @staticmethod
    def _window_is_contiguous(window: Sequence[CandleFact]) -> bool:
        return all(window[i].scope.window_start == window[i - 1].scope.window_end for i in range(1, len(window)))

    def _try_classify_window_ending_at(self, end_index: int) -> list[RegimeEvent]:
        window_candle_count = self._dimension_definition.window_candle_count
        if end_index + 1 < window_candle_count:
            return []  # warm_up_policy=require_full_window — valid absence, not an error
        window = self._candles[end_index - window_candle_count + 1 : end_index + 1]
        if not self._window_is_contiguous(window):
            return []  # gap_policy=defer_until_resolved — valid absence until the gap resolves
        key = (window[0].scope.window_start, window[-1].scope.window_end)
        return self._emit_original_fact(key, window)

    def _reevaluate_windows_covering(
        self, corrected_index: int, correction_ref: EventRecordRef, correction_recorded_time: datetime
    ) -> list[RegimeEvent]:
        window_candle_count = self._dimension_definition.window_candle_count
        lowest_end = max(window_candle_count - 1, corrected_index)
        highest_end = min(len(self._candles) - 1, corrected_index + window_candle_count - 1)
        events: list[RegimeEvent] = []
        for end_index in range(lowest_end, highest_end + 1):
            window = self._candles[end_index - window_candle_count + 1 : end_index + 1]
            if not self._window_is_contiguous(window):
                continue
            key = (window[0].scope.window_start, window[-1].scope.window_end)
            existing = self._window_lineage.get(key)
            if existing is None:
                events.extend(self._emit_original_fact(key, window))
            else:
                events.extend(
                    self._emit_correction_pair(key, window, correction_ref, correction_recorded_time, existing)
                )
        return events

    def _emit_original_fact(self, key: tuple[datetime, datetime], window: Sequence[CandleFact]) -> list[RegimeEvent]:
        window_candle_count = self._dimension_definition.window_candle_count
        normalized_refs = normalize_evidence(window, expected_count=window_candle_count)

        # regime.md §3: "recorded_time PHẢI muộn hơn recorded_time của Candle
        # fact mới nhất trong candle_evidence_refs" — the causal floor for an
        # original computation is the latest evidence recorded_time.
        floor = max(candle.recorded_time for candle in window)
        recorded_time = self._next_recorded_time(floor)

        raw_metric = self._formula.compute(tuple(window))
        computed_metric = self._dimension_definition.decimal_precision_policy.apply(raw_metric)
        class_label = _classify(
            computed_metric,
            self._dimension_definition.class_thresholds,
            self._dimension_definition.threshold_comparison_policy,
        )

        fact = RegimeClassified(
            scope=self.scope,
            class_label=class_label,
            computed_metric=computed_metric,
            window_start=key[0],
            window_end=key[1],
            candle_evidence_refs=normalized_refs,
            supersedes_fact_ref=None,
            causation_refs=normalized_refs,
            recorded_time=recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
        )
        self._window_lineage[key] = _WindowLineage(head_fact=fact)
        return [fact]

    def _emit_correction_pair(
        self,
        key: tuple[datetime, datetime],
        window: Sequence[CandleFact],
        correction_ref: EventRecordRef,
        correction_recorded_time: datetime,
        existing: _WindowLineage,
    ) -> list[RegimeEvent]:
        # regime.md §10: no shortcut even if class/computed_metric turn out
        # identical — the evidence lineage changed (a new authoritative
        # CandleCorrected ref replaces a now-stale one), so a replacement is
        # mandatory regardless of the recomputed outcome.

        # regime.md §4: invalidation.recorded_time > max(invalidated fact's
        # recorded_time, causing CandleCorrected's recorded_time).
        invalidation_floor = max(existing.head_fact.recorded_time, correction_recorded_time)
        invalidation_recorded_time = self._next_recorded_time(invalidation_floor)
        invalidation = RegimeFactInvalidated(
            scope=existing.head_fact.scope,
            invalidated_fact_ref=existing.head_fact.ref,
            window_start=existing.head_fact.window_start,
            window_end=existing.head_fact.window_end,
            causation_refs=(existing.head_fact.ref, correction_ref),
            recorded_time=invalidation_recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
        )

        window_candle_count = self._dimension_definition.window_candle_count
        normalized_refs = normalize_evidence(window, expected_count=window_candle_count)
        raw_metric = self._formula.compute(tuple(window))
        computed_metric = self._dimension_definition.decimal_precision_policy.apply(raw_metric)
        class_label = _classify(
            computed_metric,
            self._dimension_definition.class_thresholds,
            self._dimension_definition.threshold_comparison_policy,
        )

        # regime.md §3: replacement.recorded_time > invalidation.recorded_time.
        replacement_recorded_time = self._next_recorded_time(invalidation_recorded_time)
        replacement = RegimeClassified(
            scope=self.scope,
            class_label=class_label,
            computed_metric=computed_metric,
            window_start=key[0],
            window_end=key[1],
            candle_evidence_refs=normalized_refs,
            supersedes_fact_ref=existing.head_fact.ref,
            causation_refs=(*normalized_refs, invalidation.ref),
            recorded_time=replacement_recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
        )
        self._window_lineage[key] = _WindowLineage(head_fact=replacement)
        return [invalidation, replacement]


@dataclass(frozen=True, slots=True)
class AnalysisWindow:
    """`regime.md` §3's `analysis_window` interval, as exposed on a `VALID`
    `RegimeCurrentView` row (§5/§11) — absent entirely when
    `PENDING_CORRECTION` (the contract does not expose a window for a
    pending row; the projection tracks it internally only, to resolve
    target-window selection).
    """

    window_start: datetime
    window_end: datetime


@dataclass(slots=True)
class _ViewWindowState:
    window_start: datetime
    window_end: datetime
    head_fact: RegimeClassified
    invalidated: bool
    last_recorded_time: datetime


@dataclass(frozen=True, slots=True)
class RegimeViewResult:
    """regime.md §5/§11 — a materialized `RegimeCurrentView` row.

    `VALID`: `class_label`/`computed_metric`/`analysis_window`/
    `lineage_head_fact_ref` all present; `last_recorded_time` = the visible
    event (original or replacement) that established this state.

    `PENDING_CORRECTION`: all four of those fields are `None` — the contract
    does not expose class/metric/window/lineage-ref for a pending row, only
    that a correction is in flight; `last_recorded_time` = the invalidation
    event's own `recorded_time`.

    Never a third state, never `UNAVAILABLE` (§5's v0.2 correction removed
    it). Before the first `RegimeClassified` for a subject, no row exists at
    all — `RegimeCurrentView.current()` returns `None`, not this type.
    """

    regime_subject_id: str
    scope: RegimeScope
    view_state: str
    class_label: str | None
    computed_metric: Decimal | None
    analysis_window: AnalysisWindow | None
    lineage_head_fact_ref: EventRecordRef | None
    last_recorded_time: datetime


def _view_ordering_key(
    window_end: datetime, window_start: datetime, fact: RegimeClassified
) -> tuple[float, float, datetime, str, str, int, str]:
    """regime.md §11's complete 7-criterion deterministic total order,
    applied to every window candidate's current lineage head — not merely a
    fallback reachable only in a degenerate case. DESC criteria (1/2) are
    encoded as negated epoch-seconds so the overall winner is the
    lexicographic MINIMUM of this key; ASC criteria (3-7) are left as-is.
    `sequence` (6) is positioned after `stream_id`/`registry_version` (4/5)
    so Python's tuple short-circuit naturally enforces "never compare
    sequence across different stream identities" without a special case.
    """
    return (
        -window_end.timestamp(),
        -window_start.timestamp(),
        fact.recorded_time,
        fact.ref.stream_id,
        _REGISTRY_VERSION,
        fact.ref.sequence,
        fact.ref.event_id,
    )


class RegimeCurrentView:
    """regime.md §11 — non-authoritative `RegimeCurrentView` projection.

    Fed `RegimeClassified`/`RegimeFactInvalidated` one at a time by an
    external caller (mirroring how `StructureEngine` consumes
    `SwingConfirmed`/`SwingInvalidated` incrementally) — never wired
    automatically inside `RegimeEngine` itself, and never used as
    authoritative input anywhere. Before the first fact: no row (`current()`
    returns `None`). After: exactly `VALID` or `PENDING_CORRECTION`,
    resolved by first determining the target window (regime.md §11's full
    deterministic total order, applied across ALL windows ever classified)
    — BEFORE excluding anything invalidated — so the view never silently
    falls back to an older, still-valid window when the newest one is
    pending correction (regime.md §11 Step 1's anti-regression rule).
    """

    def __init__(self, scope: RegimeScope) -> None:
        self.scope = scope
        self._windows: dict[tuple[datetime, datetime], _ViewWindowState] = {}

    def _check_scope(self, event_scope: RegimeScope) -> None:
        if event_scope != self.scope:
            raise ForeignScopeError(f"event scope {event_scope!r} does not match view scope {self.scope!r}")

    def on_regime_classified(self, event: RegimeClassified) -> None:
        self._check_scope(event.scope)
        key = (event.window_start, event.window_end)
        state = self._windows.get(key)
        if event.supersedes_fact_ref is None:
            if state is not None:
                raise RegimeLineageError(f"original RegimeClassified for already-classified window {key!r}")
            self._windows[key] = _ViewWindowState(
                window_start=key[0],
                window_end=key[1],
                head_fact=event,
                invalidated=False,
                last_recorded_time=event.recorded_time,
            )
            return
        if state is None or state.head_fact.ref != event.supersedes_fact_ref:
            raise RegimeLineageError(
                f"replacement supersedes_fact_ref={event.supersedes_fact_ref!r} does not match the "
                f"current lineage head for window {key!r}"
            )
        if not state.invalidated:
            raise RegimeLineageError(f"replacement for window {key!r} arrived before its invalidation")
        state.head_fact = event
        state.invalidated = False
        state.last_recorded_time = event.recorded_time

    def on_regime_invalidated(self, event: RegimeFactInvalidated) -> None:
        self._check_scope(event.scope)
        key = (event.window_start, event.window_end)
        state = self._windows.get(key)
        if state is None or state.head_fact.ref != event.invalidated_fact_ref:
            raise RegimeLineageError(
                f"invalidation target {event.invalidated_fact_ref!r} does not match the current "
                f"lineage head for window {key!r}"
            )
        if state.invalidated:
            raise RegimeLineageError(f"fact already invalidated for window {key!r}")
        state.invalidated = True
        state.last_recorded_time = event.recorded_time

    def current(self) -> RegimeViewResult | None:
        if not self._windows:
            return None
        target_key = min(
            self._windows.keys(),
            key=lambda k: _view_ordering_key(k[1], k[0], self._windows[k].head_fact),
        )
        state = self._windows[target_key]
        regime_subject_id = self.scope.regime_subject_id
        if not state.invalidated:
            fact = state.head_fact
            return RegimeViewResult(
                regime_subject_id=regime_subject_id,
                scope=self.scope,
                view_state="VALID",
                class_label=fact.class_label,
                computed_metric=fact.computed_metric,
                analysis_window=AnalysisWindow(fact.window_start, fact.window_end),
                lineage_head_fact_ref=fact.ref,
                last_recorded_time=state.last_recorded_time,
            )
        return RegimeViewResult(
            regime_subject_id=regime_subject_id,
            scope=self.scope,
            view_state="PENDING_CORRECTION",
            class_label=None,
            computed_metric=None,
            analysis_window=None,
            lineage_head_fact_ref=None,
            last_recorded_time=state.last_recorded_time,
        )
