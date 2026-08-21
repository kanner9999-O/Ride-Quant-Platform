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
"""

from __future__ import annotations

import decimal
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Protocol

from .candle import CandleFact
from .envelope import EventRecordRef
from .errors import (
    DuplicateCandleConflictError,
    ForeignScopeError,
    FormulaMismatchError,
    NonMonotonicRecordedTimeError,
    OutOfOrderCandleError,
    OutOfOrderCorrectionError,
    RegimeLineageError,
)
from .identity import deterministic_id
from .publish import SequenceAllocator

# regime.md §6 — two pinned canonical policy-identifier strings. Opaque,
# module-local conventions (regime.md defers the concrete identifier scheme,
# same status as swing.md/structure.md's own selection-policy strings) —
# validated fail-closed at `RegimeDefinition` construction so a definition
# built against a different, incompatible convention is rejected rather than
# silently misinterpreted.
CANDLE_EVIDENCE_NORMALIZATION_POLICY = "regime.md-8a-window-stream-registryversion-sequence-eventid-lexicographic-v1"
CURRENT_VIEW_SELECTION_POLICY = "regime.md-11-max-window-end-then-window-start-v1"

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


@dataclass(frozen=True, slots=True)
class RegimeDefinition:
    """`regime.md` §6's full `regime_definition` — module-level policies plus
    one `RegimeDimensionDefinition` per dimension actually configured.
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
        for dimension_name, dimension_definition in self.dimensions.items():
            allowed = _ALLOWED_LABELS.get(dimension_name)
            if allowed is None:
                raise ValueError(f"unsupported regime_dimension: {dimension_name!r}")
            for band in dimension_definition.class_thresholds:
                if band.label not in allowed:
                    raise ValueError(f"label {band.label!r} not allowed for dimension {dimension_name!r}")


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


def normalize_evidence(candles: Sequence[CandleFact]) -> tuple[EventRecordRef, ...]:
    """regime.md §8a canonical Candle evidence normalization.

    Strict lexicographic order — window_start ASC, window_end ASC, stream_id
    ASC, registry_version ASC, sequence ASC (only meaningful when 3/4 tie,
    i.e. within the same stream), event_id ASC — with dedup by event-record
    ref (two references resolving the same Candle fact keep exactly one).
    Independent of input order: the same underlying evidence set always
    normalizes to the same output tuple (regime.md §8b identity).
    """
    deduped: dict[EventRecordRef, CandleFact] = {}
    for candle in candles:
        deduped[candle.ref] = candle
    ordered = sorted(deduped.values(), key=_evidence_sort_key)
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
    """

    def __init__(
        self,
        scope: RegimeScope,
        definition: RegimeDefinition,
        formula: MetricFormula,
        allocator: SequenceAllocator,
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
        if self._last_recorded_time is not None and recorded_time < self._last_recorded_time:
            raise NonMonotonicRecordedTimeError(
                f"recorded_time {recorded_time!r} precedes last-seen {self._last_recorded_time!r}"
            )
        self._last_recorded_time = recorded_time

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
        return self._try_classify_window_ending_at(new_index, fact.recorded_time)

    @staticmethod
    def _window_is_contiguous(window: Sequence[CandleFact]) -> bool:
        return all(window[i].scope.window_start == window[i - 1].scope.window_end for i in range(1, len(window)))

    def _try_classify_window_ending_at(self, end_index: int, recorded_time: datetime) -> list[RegimeEvent]:
        window_candle_count = self._dimension_definition.window_candle_count
        if end_index + 1 < window_candle_count:
            return []  # warm_up_policy=require_full_window — valid absence, not an error
        window = self._candles[end_index - window_candle_count + 1 : end_index + 1]
        if not self._window_is_contiguous(window):
            return []  # gap_policy=defer_until_resolved — valid absence until the gap resolves
        key = (window[0].scope.window_start, window[-1].scope.window_end)
        return self._emit_window_fact(key, window, recorded_time, correction_ref=None)

    def _reevaluate_windows_covering(
        self, corrected_index: int, correction_ref: EventRecordRef, recorded_time: datetime
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
            events.extend(self._emit_window_fact(key, window, recorded_time, correction_ref=correction_ref))
        return events

    def _emit_window_fact(
        self,
        key: tuple[datetime, datetime],
        window: Sequence[CandleFact],
        recorded_time: datetime,
        *,
        correction_ref: EventRecordRef | None,
    ) -> list[RegimeEvent]:
        normalized_refs = normalize_evidence(window)
        raw_metric = self._formula.compute(tuple(window))
        computed_metric = self._dimension_definition.decimal_precision_policy.apply(raw_metric)
        class_label = _classify(
            computed_metric,
            self._dimension_definition.class_thresholds,
            self._dimension_definition.threshold_comparison_policy,
        )

        existing = self._window_lineage.get(key)
        events: list[RegimeEvent] = []
        invalidation_ref: EventRecordRef | None = None
        if existing is not None:
            # regime.md §10 — no shortcut even if class/computed_metric turn
            # out identical: the evidence lineage changed (a new authoritative
            # CandleCorrected ref replaces a now-stale one), so a replacement
            # is mandatory regardless of the recomputed outcome.
            assert correction_ref is not None
            invalidation_ref = self._allocator.next_ref(self._stream_id)
            events.append(
                RegimeFactInvalidated(
                    scope=existing.head_fact.scope,
                    invalidated_fact_ref=existing.head_fact.ref,
                    window_start=existing.head_fact.window_start,
                    window_end=existing.head_fact.window_end,
                    causation_refs=(existing.head_fact.ref, correction_ref),
                    recorded_time=recorded_time,
                    ref=invalidation_ref,
                )
            )

        causation_refs = list(normalized_refs)
        if invalidation_ref is not None:
            causation_refs.append(invalidation_ref)

        fact = RegimeClassified(
            scope=self.scope,
            class_label=class_label,
            computed_metric=computed_metric,
            window_start=key[0],
            window_end=key[1],
            candle_evidence_refs=normalized_refs,
            supersedes_fact_ref=existing.head_fact.ref if existing is not None else None,
            causation_refs=tuple(causation_refs),
            recorded_time=recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
        )
        events.append(fact)
        self._window_lineage[key] = _WindowLineage(head_fact=fact)
        return events


@dataclass(slots=True)
class _ViewWindowState:
    window_start: datetime
    window_end: datetime
    head_fact: RegimeClassified
    invalidated: bool


@dataclass(frozen=True, slots=True)
class RegimeViewResult:
    """regime.md §11 — `VALID` or `PENDING_CORRECTION` only (never a third
    state, never `UNAVAILABLE`).
    """

    view_state: str
    class_label: str | None
    computed_metric: Decimal | None
    window_start: datetime
    window_end: datetime
    lineage_head_fact_ref: EventRecordRef | None


class RegimeCurrentView:
    """regime.md §11 — non-authoritative `RegimeCurrentView` projection.

    Fed `RegimeClassified`/`RegimeFactInvalidated` one at a time by an
    external caller (mirroring how `StructureEngine` consumes
    `SwingConfirmed`/`SwingInvalidated` incrementally) — never wired
    automatically inside `RegimeEngine` itself, and never used as
    authoritative input anywhere. Before the first fact: no row (`current()`
    returns `None`). After: exactly `VALID` or `PENDING_CORRECTION`,
    resolved by first determining the target window (max `window_end`, then
    max `window_start`) across ALL windows ever classified — BEFORE
    excluding anything invalidated — so the view never silently falls back
    to an older, still-valid window when the newest one is pending
    correction (regime.md §11 Step 1's anti-regression rule).
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
                window_start=key[0], window_end=key[1], head_fact=event, invalidated=False
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

    def current(self) -> RegimeViewResult | None:
        if not self._windows:
            return None
        target_key = max(self._windows.keys(), key=lambda k: (k[1], k[0]))
        state = self._windows[target_key]
        if not state.invalidated:
            fact = state.head_fact
            return RegimeViewResult(
                view_state="VALID",
                class_label=fact.class_label,
                computed_metric=fact.computed_metric,
                window_start=fact.window_start,
                window_end=fact.window_end,
                lineage_head_fact_ref=fact.ref,
            )
        return RegimeViewResult(
            view_state="PENDING_CORRECTION",
            class_label=None,
            computed_metric=None,
            window_start=state.window_start,
            window_end=state.window_end,
            lineage_head_fact_ref=None,
        )
