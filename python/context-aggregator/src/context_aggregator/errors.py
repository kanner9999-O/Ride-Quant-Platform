"""Shared, explicit technical failure modes.

Exception-based technical sentinels for genuine input/wiring violations that
have no domain/business representation — never used as normal control flow
for a valid domain outcome. A required role being absent/invalid/pending is
NOT one of these: context.md §9's `missing_input_policy` makes "no candidate"
a normal, valid outcome (represented by returning `None`, not raising),
never an exception.
"""

from __future__ import annotations


class ContextAggregatorError(Exception):
    """Base class for all context-aggregator technical errors."""


class InvalidContextTypeError(ContextAggregatorError):
    """A `context_type` value other than the single closed enum value
    `market_context` (context.md §1 v0.1) was supplied — `context_type` has
    exactly one valid value at this Domain Contract version; adding another
    is an explicit Domain Contract revision (§21), never an implicit one."""


class ScopeDefinitionMismatchError(ContextAggregatorError):
    """The `ContextSubjectScope.context_definition_version` supplied to the
    aggregation entrypoint does not exactly match the `ContextDefinition`
    supplied alongside it — a caller/wiring error (the two must pin the same
    Context Definition, context.md §1/§6), never silently reconciled."""


class RegimeClassTypeMismatchError(ContextAggregatorError):
    """A selected `RegimeFact.regime_class` value's own enum type does not
    match the dimension the role selection was performed for (e.g. a
    `DirectionalPersistenceRegimeClass` value returned for the `volatility`
    role) — a caller/wiring defect in the supplied evidence, never silently
    coerced or reinterpreted."""


class DuplicateFactReferenceError(ContextAggregatorError):
    """Either (a) the same `EventRecordRef` was supplied more than once as a
    candidate for the same role with materially different content, or (b)
    two of the seven selected role winners resolved to the identical
    `EventRecordRef` — context.md §10 requires `normalized_input_fact_refs`
    to contain exactly seven distinct elements; neither case is ever
    resolved by last-write-wins or silently deduplicated."""


class MalformedLineageError(ContextAggregatorError):
    """A role's supplied candidate set contains a correction-lineage shape
    this core can positively detect as invalid: self-supersession (a fact's
    `supersedes_ref` equals its own `ref`), or a fork (two distinct facts
    both claim `supersedes_ref` on the same target — at most one direct
    replacement per invalidated fact, context.md §12 rule 6). Fails closed
    rather than guessing which candidate is the genuine lineage edge."""
