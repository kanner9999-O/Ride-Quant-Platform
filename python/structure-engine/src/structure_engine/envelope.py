"""Chapter 8 §8.2 event-record identity shapes.

Chapter 8 owns envelope semantics; this module applies them, it does not
redefine them (same relationship market-data-ingestion's Go `internal/envelope`
package has with Chapter 8).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EventRecordRef:
    """Canonical event-record locator + verification field (Chapter 8 §8.2.3)."""

    stream_id: str
    sequence: int
    event_id: str


@dataclass(frozen=True, slots=True)
class StreamRef:
    """Stream definition snapshot applied at append (Chapter 8 §8.3.1)."""

    stream_id: str
    registry_version: str


@dataclass(frozen=True, slots=True)
class ProducerRef:
    """Authoritative implementation that produced the event (Chapter 8 §8.2.4)."""

    module_id: str
    implementation_version: str
    run_id: str
