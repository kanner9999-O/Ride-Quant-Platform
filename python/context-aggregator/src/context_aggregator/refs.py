"""Canonical event-record locator fields Context needs for role-selection
ordering (context.md §8 Phase 2 tie-break; §10 normalization).

A module-local, independently-defined equivalent — not an import of any
producer module's own envelope types. Chapter 8 §8.2/§8.3.1 owns the real
authoritative event envelope; binding a Context aggregation result to that
real envelope (assigning a genuine `stream_ref`/`producer_ref`/`sequence`/
`event_contract_ref` for a published `MarketContextSnapshot`) is a later,
governed publishing slice this module does not perform (see the package
README's "What this slice does not implement").
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class EventRecordRef:
    """Locates one upstream authoritative fact for role-selection/tie-break
    purposes.

    Fields are exactly the four values context.md's own tie-break/
    normalization text references by name (`stream_ref.stream_id`,
    `stream_ref.registry_version`, `sequence`, `event_id`) — flattened here
    rather than nested under a separate `StreamRef` type, since this module
    does not own event envelope construction.
    """

    stream_id: str
    registry_version: str
    sequence: int
    event_id: str


@dataclass(frozen=True, slots=True)
class EffectiveWindow:
    """`[window_start, window_end)` interval (context.md §3/§14)."""

    window_start: datetime
    window_end: datetime
