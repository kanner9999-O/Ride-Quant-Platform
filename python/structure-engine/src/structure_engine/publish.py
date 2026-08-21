"""In-process, per-stream contiguous sequence allocation (ADR-009).

`stream-registry.yaml` (Phase 1) does not exist yet. This is a bounded,
module-local stand-in — the same role market-data-ingestion's Go
`publish.Memory` plays there: it assigns a contiguous, 1-based sequence per
`stream_id` and stamps a `ProducerRef`, but it is NOT a real event log or
broker, and it invents no stream-registry infrastructure.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

from .envelope import EventRecordRef, ProducerRef


@dataclass(slots=True)
class SequenceAllocator:
    """Assigns deterministic, per-stream contiguous sequence numbers.

    module_id/implementation_version/run_id identify the producing
    implementation (Chapter 8 §8.2.4) — module-local values, not resolved
    from module-registry.yaml (which carries no producer-identity fields).
    """

    module_id: str
    implementation_version: str
    run_id: str
    _sequences: dict[str, itertools.count[int]] = field(default_factory=dict, repr=False)
    _event_ordinal: itertools.count[int] = field(default_factory=lambda: itertools.count(1), repr=False)

    def next_ref(self, stream_id: str) -> EventRecordRef:
        counter = self._sequences.setdefault(stream_id, itertools.count(1))
        sequence = next(counter)
        event_id = f"{self.run_id}-{next(self._event_ordinal)}"
        return EventRecordRef(stream_id=stream_id, sequence=sequence, event_id=event_id)

    def producer_ref(self) -> ProducerRef:
        return ProducerRef(self.module_id, self.implementation_version, self.run_id)
