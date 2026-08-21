"""Shared, explicit technical failure modes.

Per Error Handling Convention §7's resolution order: these represent genuine
input/ordering/configuration violations that have no existing domain/business
representation — bounded technical sentinel errors, not new domain
semantics. The first five mirror structure-engine's own `errors.py`
(duplicated, not imported — see `identity.py`'s module docstring);
`FormulaMismatchError` and `RegimeLineageError` are new, specific to Raw
Regime's own formula-injection boundary (regime.md's "no canonical formula"
constraint) and per-window correction-lineage invariants (regime.md §10).
"""

from __future__ import annotations


class RawRegimeEngineError(Exception):
    """Base class for all raw-regime-engine technical errors."""


class OutOfOrderCorrectionError(RawRegimeEngineError):
    """A correction was submitted for a subject never previously ingested.

    Chapter 8 §8.3.4 causal precedence: a CandleCorrected must not be
    processed before the fact it corrects has been applied.
    """


class NonMonotonicRecordedTimeError(RawRegimeEngineError):
    """A fact was submitted with recorded_time earlier than the last-seen one.

    Cursor-bounded visibility (Chapter 5) requires facts to be ingested in
    non-decreasing recorded_time order — the engine never looks ahead.
    """


class DuplicateCandleConflictError(RawRegimeEngineError):
    """A non-correction fact was submitted for an already-seen subject with
    different content — an ambiguous input the engine refuses to guess about.
    """


class OutOfOrderCandleError(RawRegimeEngineError):
    """A candle was submitted with window_start earlier than the last-seen
    candle for the same (instrument, venue, timeframe) scope.
    """


class ForeignScopeError(RawRegimeEngineError):
    """A fact was submitted whose scope does not match this engine's/view's
    own scope. Raw Regime fails closed rather than silently ingesting a
    foreign-scope fact (regime.md §13 — Regime scope is not global state).
    """


class FormulaMismatchError(RawRegimeEngineError):
    """The `MetricFormula` supplied to the engine does not identify itself
    (`formula_id`) as the one pinned by the `RegimeDimensionDefinition`'s
    `metric_formula_id`. regime.md deliberately does not select a concrete
    canonical formula (no global formula registry exists to resolve this
    automatically) — a caller must supply one explicitly, and the engine
    fails closed on any mismatch rather than silently substituting or
    guessing.
    """


class RegimeLineageError(RawRegimeEngineError):
    """A `RegimeClassified`/`RegimeFactInvalidated` event was submitted (to
    `RegimeCurrentView`) that violates regime.md §10's mandatory correction
    lineage invariants for its (window_start, window_end) — e.g. it does not
    target the current lineage head, a fact was invalidated more than once,
    or a replacement arrived before its own invalidation became visible.
    """
