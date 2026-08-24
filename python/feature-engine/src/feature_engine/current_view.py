"""`FeatureCurrentView` — non-authoritative projection (feature.md §5/§11).

Fed `FeatureComputed`/`FeatureFactInvalidated` one at a time by an external
caller — never wired automatically inside any of the three computation
engines, and never used as authoritative input anywhere. Before the first
fact: no row (`current()` returns `None`). After: exactly `VALID` or
`PENDING_CORRECTION` — never a third state, never `UNAVAILABLE`.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .contracts import FeatureComputed, FeatureFactInvalidated, FeatureScope
from .envelope import EventRecordRef
from .errors import FeatureLineageError, ForeignScopeError

_REGISTRY_VERSION = "v0"


@dataclass(frozen=True, slots=True)
class EffectiveWindow:
    window_start: datetime
    window_end: datetime


@dataclass(slots=True)
class _ViewWindowState:
    window_start: datetime
    window_end: datetime
    head_fact: FeatureComputed
    invalidated: bool
    last_recorded_time: datetime


@dataclass(frozen=True, slots=True)
class FeatureViewResult:
    """feature.md §5/§11 — a materialized `FeatureCurrentView` row.

    `VALID`: `value`/`unit`/`effective_window`/`lineage_head_fact_ref` all
    present. `PENDING_CORRECTION`: all four are `None` — the contract does
    not expose them for a pending row. `last_recorded_time` always present.
    """

    feature_subject_id: str
    scope: FeatureScope
    view_state: str
    value: Decimal | None
    unit: str | None
    effective_window: EffectiveWindow | None
    lineage_head_fact_ref: EventRecordRef | None
    last_recorded_time: datetime


def _view_ordering_key(
    window_end: datetime, window_start: datetime, fact: FeatureComputed
) -> tuple[float, float, datetime, str, str, int, str]:
    """feature.md §11's complete 7-criterion deterministic total order,
    applied to every window candidate's current lineage head — evaluated
    BEFORE excluding anything invalidated (Step 1's anti-regression rule).
    DESC criteria are encoded as negated epoch-seconds so the overall winner
    is the lexicographic MINIMUM of this key.
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


class FeatureCurrentView:
    def __init__(self, scope: FeatureScope) -> None:
        self.scope = scope
        self._windows: dict[tuple[datetime, datetime], _ViewWindowState] = {}

    def _check_scope(self, event_scope: FeatureScope) -> None:
        if event_scope != self.scope:
            raise ForeignScopeError(f"event scope {event_scope!r} does not match view scope {self.scope!r}")

    def on_feature_computed(self, event: FeatureComputed) -> None:
        self._check_scope(event.scope)
        key = (event.window_start, event.window_end)
        state = self._windows.get(key)
        if event.supersedes_fact_ref is None:
            if state is not None:
                raise FeatureLineageError(f"original FeatureComputed for already-computed window {key!r}")
            self._windows[key] = _ViewWindowState(
                window_start=key[0],
                window_end=key[1],
                head_fact=event,
                invalidated=False,
                last_recorded_time=event.recorded_time,
            )
            return
        if state is None or state.head_fact.ref != event.supersedes_fact_ref:
            raise FeatureLineageError(
                f"replacement supersedes_fact_ref={event.supersedes_fact_ref!r} does not match the current "
                f"lineage head for window {key!r}"
            )
        if not state.invalidated:
            raise FeatureLineageError(f"replacement for window {key!r} arrived before its invalidation")
        state.head_fact = event
        state.invalidated = False
        state.last_recorded_time = event.recorded_time

    def on_feature_invalidated(self, event: FeatureFactInvalidated) -> None:
        self._check_scope(event.scope)
        key = (event.window_start, event.window_end)
        state = self._windows.get(key)
        if state is None or state.head_fact.ref != event.invalidated_fact_ref:
            raise FeatureLineageError(
                f"invalidation target {event.invalidated_fact_ref!r} does not match the current lineage head "
                f"for window {key!r}"
            )
        if state.invalidated:
            raise FeatureLineageError(f"fact already invalidated for window {key!r}")
        state.invalidated = True
        state.last_recorded_time = event.recorded_time

    def current(self) -> FeatureViewResult | None:
        if not self._windows:
            return None
        target_key = min(
            self._windows.keys(),
            key=lambda k: _view_ordering_key(k[1], k[0], self._windows[k].head_fact),
        )
        state = self._windows[target_key]
        feature_subject_id = self.scope.feature_subject_id
        if not state.invalidated:
            fact = state.head_fact
            return FeatureViewResult(
                feature_subject_id=feature_subject_id,
                scope=self.scope,
                view_state="VALID",
                value=fact.value,
                unit=fact.unit,
                effective_window=EffectiveWindow(fact.window_start, fact.window_end),
                lineage_head_fact_ref=fact.ref,
                last_recorded_time=state.last_recorded_time,
            )
        return FeatureViewResult(
            feature_subject_id=feature_subject_id,
            scope=self.scope,
            view_state="PENDING_CORRECTION",
            value=None,
            unit=None,
            effective_window=None,
            lineage_head_fact_ref=None,
            last_recorded_time=state.last_recorded_time,
        )
