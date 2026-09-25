"""Context subject scope and opaque subject identity (context.md §1)."""

from __future__ import annotations

from dataclasses import dataclass

from context_aggregator.errors import InvalidContextTypeError
from context_aggregator.identity import deterministic_id

MARKET_CONTEXT = "market_context"
"""The single closed `context_type` enum value at this Domain Contract
version (context.md §1 v0.1)."""


@dataclass(frozen=True, slots=True)
class ContextSubjectScope:
    """Five-field qualifying scope (context.md §1) — the exact and only
    fields that determine `context_subject_id`. Immutable after first
    observation; changing any field identifies a DIFFERENT subject, never a
    mutation of this one (§1 invariants)."""

    instrument_id: str
    venue_id: str
    timeframe: str
    context_definition_version: str
    context_type: str = MARKET_CONTEXT

    def __post_init__(self) -> None:
        if self.context_type != MARKET_CONTEXT:
            raise InvalidContextTypeError(self.context_type)

    @property
    def context_subject_id(self) -> str:
        """Deterministic opaque id from exactly the five scope fields
        (context.md §1 invariant) — never parsed by domain logic (Chapter 6
        §6.8)."""
        return deterministic_id(
            self.instrument_id,
            self.venue_id,
            self.timeframe,
            self.context_type,
            self.context_definition_version,
        )
