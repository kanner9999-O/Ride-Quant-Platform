"""The exact two-phase Eligible Upstream Fact selection pipeline (context.md
§8), implemented once per role family.

**Explicit visibility boundary (context.md §8 Phase 1 step 2, §14(a)):**
recorded-time cursor visibility is NOT re-implemented here. This core's
public entrypoint (`aggregation.py`) requires callers to supply, per role,
only candidate facts that are already cursor-visible/boundary-qualified —
cursor-visibility qualification is an external prerequisite to this core,
established by a future orchestration/frontier layer, not by this module.
Re-deriving it here would require inventing stream-position/frontier
semantics this module does not own (`feature-context-architecture.md` §13,
still an open gap) and would reduce Chapter 8 cursor visibility to a scalar
`recorded_time` test, which context.md §14 explicitly treats as only ONE of
two independent required conditions.

Every other locally-resolvable Context-owned predicate — identity/scope
match, required definition-version match, effective-time cutoff (step 3),
role-specific validity-at-cursor via the supplied invalidation/lineage
evidence (step 4), role-specific current selection (Phase 2), and the
shared total-order tie-break — IS enforced here, exactly as context.md §8
specifies.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence, Set
from datetime import datetime
from functools import cmp_to_key
from typing import Protocol, TypeVar

from context_aggregator.errors import DuplicateFactReferenceError
from context_aggregator.evidence import (
    CandleFact,
    FeatureFact,
    FeatureType,
    RegimeDimension,
    RegimeFact,
    StructureFact,
    StructureFactKind,
)
from context_aggregator.refs import EventRecordRef


class _Referenced(Protocol):
    """Structural requirement satisfied by every `@dataclass(frozen=True)`
    evidence type below — declared via read-only `@property` (not a plain
    attribute) because a frozen dataclass field is read-only, and a plain
    Protocol attribute requires read-write conformance."""

    @property
    def ref(self) -> EventRecordRef: ...


_R = TypeVar("_R", bound=_Referenced)


def _reject_conflicting_duplicates(candidates: Sequence[_R]) -> None:  # noqa: UP047
    """context.md §10's 'no duplicate' evidence-set requirement, enforced at
    intake — the SAME ref supplied twice with materially different content
    is never silently resolved by last-write-wins (fails closed)."""
    seen: dict[EventRecordRef, _R] = {}
    for candidate in candidates:
        prior = seen.get(candidate.ref)
        if prior is None:
            seen[candidate.ref] = candidate
        elif prior != candidate:
            raise DuplicateFactReferenceError(candidate.ref)


class _RankedFact(Protocol):
    """Same read-only-property rationale as `_Referenced`."""

    @property
    def recorded_time(self) -> datetime: ...

    @property
    def ref(self) -> EventRecordRef: ...


_F = TypeVar("_F", bound=_RankedFact)


def _compare_total_order(  # noqa: UP047
    a: _F,
    b: _F,
    boundary_end: Callable[[_F], datetime],
    boundary_start: Callable[[_F], datetime],
) -> int:
    """context.md §8 Phase 2 total-order tie-break, criteria 1-7, compared
    strictly in order — the first difference decides, later criteria are
    never evaluated. `sequence` (criterion 6) is only ever reached once
    `stream_id`/`registry_version` (criteria 4/5) have both already tied,
    so cross-stream `sequence` comparison never happens here."""
    ae, be = boundary_end(a), boundary_end(b)
    if ae != be:
        return -1 if ae > be else 1
    a_start, b_start = boundary_start(a), boundary_start(b)
    if a_start != b_start:
        return -1 if a_start > b_start else 1
    if a.recorded_time != b.recorded_time:
        return -1 if a.recorded_time < b.recorded_time else 1
    if a.ref.stream_id != b.ref.stream_id:
        return -1 if a.ref.stream_id < b.ref.stream_id else 1
    if a.ref.registry_version != b.ref.registry_version:
        return -1 if a.ref.registry_version < b.ref.registry_version else 1
    if a.ref.sequence != b.ref.sequence:
        return -1 if a.ref.sequence < b.ref.sequence else 1
    if a.ref.event_id != b.ref.event_id:
        return -1 if a.ref.event_id < b.ref.event_id else 1
    return 0


def select_candle(
    candidates: Sequence[CandleFact],
    *,
    instrument_id: str,
    venue_id: str,
    timeframe: str,
) -> CandleFact | None:
    """Candle cutoff/cadence source role (context.md §7.0/§8). Phase 1 step
    4 (lineage resolution) is performed inline: only a survivor not
    superseded by another survivor's `supersedes_ref` proceeds to Phase 2.
    There is no external `context_cutoff` filter for this role — the
    winning Candle fact's own `effective_window.window_end` DEFINES
    `context_cutoff` for every other role (context.md §6/§11)."""
    _reject_conflicting_duplicates(candidates)
    scope_matched = [
        c
        for c in candidates
        if c.instrument_id == instrument_id and c.venue_id == venue_id and c.timeframe == timeframe
    ]
    superseded = {c.supersedes_ref for c in scope_matched if c.supersedes_ref is not None}
    survivors = [c for c in scope_matched if c.ref not in superseded]
    if not survivors:
        return None

    def _cmp(a: CandleFact, b: CandleFact) -> int:
        return _compare_total_order(
            a, b, lambda x: x.effective_window.window_end, lambda x: x.effective_window.window_start
        )

    ordered = sorted(survivors, key=cmp_to_key(_cmp))
    return ordered[0]


def select_structure(
    candidates: Sequence[StructureFact],
    *,
    instrument_id: str,
    venue_id: str,
    timeframe: str,
    context_cutoff: datetime,
    required_definition_version: str,
    invalidated_refs: Set[EventRecordRef] = frozenset(),
) -> StructureFact | None:
    """Structure role (context.md §7.1/§8). Phase 2 winner = survivor with
    MAX `recorded_time` (each BOS/CHoCH/StructureRecomputed sets the ENTIRE
    orientation, never accumulates); the shared total-order tie-break only
    applies among survivors tied on that maximum."""
    _reject_conflicting_duplicates(candidates)
    survivors = []
    for c in candidates:
        if c.instrument_id != instrument_id or c.venue_id != venue_id or c.timeframe != timeframe:
            continue
        if c.definition_version != required_definition_version:
            continue
        if c.effective_time > context_cutoff:
            continue
        if c.kind != StructureFactKind.STRUCTURE_RECOMPUTED and c.ref in invalidated_refs:
            continue
        survivors.append(c)
    if not survivors:
        return None
    max_recorded = max(c.recorded_time for c in survivors)
    tied = [c for c in survivors if c.recorded_time == max_recorded]

    def _cmp(a: StructureFact, b: StructureFact) -> int:
        return _compare_total_order(a, b, lambda x: x.effective_time, lambda x: x.effective_time)

    ordered = sorted(tied, key=cmp_to_key(_cmp))
    return ordered[0]


def select_regime(
    candidates: Sequence[RegimeFact],
    *,
    instrument_id: str,
    venue_id: str,
    timeframe: str,
    context_cutoff: datetime,
    dimension: RegimeDimension,
    required_definition_version: str,
    invalidated_refs: Set[EventRecordRef] = frozenset(),
) -> RegimeFact | None:
    """One Regime dimension role (context.md §7.2/§8). Phase 2 winner = the
    current lineage head: the survivor no OTHER survivor's `supersedes_ref`
    points to — never a fallback to an already-superseded survivor."""
    _reject_conflicting_duplicates(candidates)
    survivors = []
    for c in candidates:
        if c.instrument_id != instrument_id or c.venue_id != venue_id or c.timeframe != timeframe:
            continue
        if c.regime_dimension != dimension:
            continue
        if c.definition_version != required_definition_version:
            continue
        if c.analysis_window.window_end > context_cutoff:
            continue
        if c.ref in invalidated_refs:
            continue
        survivors.append(c)
    if not survivors:
        return None
    superseded = {c.supersedes_ref for c in survivors if c.supersedes_ref is not None}
    lineage_heads = [c for c in survivors if c.ref not in superseded]
    if not lineage_heads:
        return None

    def _cmp(a: RegimeFact, b: RegimeFact) -> int:
        return _compare_total_order(
            a, b, lambda x: x.analysis_window.window_end, lambda x: x.analysis_window.window_start
        )

    ordered = sorted(lineage_heads, key=cmp_to_key(_cmp))
    return ordered[0]


def select_feature(
    candidates: Sequence[FeatureFact],
    *,
    instrument_id: str,
    venue_id: str,
    timeframe: str,
    context_cutoff: datetime,
    feature_type: FeatureType,
    required_definition_version: str,
    invalidated_refs: Set[EventRecordRef] = frozenset(),
) -> FeatureFact | None:
    """One founding Feature-type role (context.md §7.3/§8). Phase 2 winner =
    the current lineage head, symmetric to `select_regime`."""
    _reject_conflicting_duplicates(candidates)
    survivors = []
    for c in candidates:
        if c.instrument_id != instrument_id or c.venue_id != venue_id or c.timeframe != timeframe:
            continue
        if c.feature_type != feature_type:
            continue
        if c.definition_version != required_definition_version:
            continue
        if c.effective_window.window_end > context_cutoff:
            continue
        if c.ref in invalidated_refs:
            continue
        survivors.append(c)
    if not survivors:
        return None
    superseded = {c.supersedes_ref for c in survivors if c.supersedes_ref is not None}
    lineage_heads = [c for c in survivors if c.ref not in superseded]
    if not lineage_heads:
        return None

    def _cmp(a: FeatureFact, b: FeatureFact) -> int:
        return _compare_total_order(
            a, b, lambda x: x.effective_window.window_end, lambda x: x.effective_window.window_start
        )

    ordered = sorted(lineage_heads, key=cmp_to_key(_cmp))
    return ordered[0]


def normalize_input_fact_refs(
    bounded: Sequence[tuple[datetime, datetime, EventRecordRef]],
) -> tuple[EventRecordRef, ...]:
    """context.md §10 canonical input normalization: `window_start` ASC,
    `window_end` ASC, `stream_id` ASC, `registry_version` ASC, `sequence`
    ASC (only once stream identity has already tied), `event_id` ASC. The
    normalized list is a mathematical evidence SET — the same facts in a
    different incoming order always normalize to the same output."""

    def compare(
        a: tuple[datetime, datetime, EventRecordRef],
        b: tuple[datetime, datetime, EventRecordRef],
    ) -> int:
        a_start, a_end, a_ref = a
        b_start, b_end, b_ref = b
        if a_start != b_start:
            return -1 if a_start < b_start else 1
        if a_end != b_end:
            return -1 if a_end < b_end else 1
        if a_ref.stream_id != b_ref.stream_id:
            return -1 if a_ref.stream_id < b_ref.stream_id else 1
        if a_ref.registry_version != b_ref.registry_version:
            return -1 if a_ref.registry_version < b_ref.registry_version else 1
        if a_ref.sequence != b_ref.sequence:
            return -1 if a_ref.sequence < b_ref.sequence else 1
        if a_ref.event_id != b_ref.event_id:
            return -1 if a_ref.event_id < b_ref.event_id else 1
        return 0

    ordered = sorted(bounded, key=cmp_to_key(compare))
    return tuple(item[2] for item in ordered)
