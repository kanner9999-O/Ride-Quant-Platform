"""Shared, explicit technical failure modes.

Per Error Handling Convention §7's resolution order: these represent genuine
input/ordering violations that have no existing domain/business
representation (they are not Swing/Structure precedence outcomes — those
outcomes govern well-formed fact sequences, not malformed/out-of-order
input) — bounded technical sentinel errors, not new domain semantics.
"""

from __future__ import annotations


class StructureEngineError(Exception):
    """Base class for all structure-engine technical errors."""


class OutOfOrderCorrectionError(StructureEngineError):
    """A correction was submitted for a subject never previously ingested.

    Chapter 8 §8.3.4 causal precedence: a CandleCorrected must not be
    processed before the fact it corrects has been applied.
    """


class NonMonotonicRecordedTimeError(StructureEngineError):
    """A fact was submitted with recorded_time earlier than the last-seen one.

    Cursor-bounded visibility (Chapter 5) requires facts to be ingested in
    non-decreasing recorded_time order — the engine never looks ahead.
    """


class DuplicateCandleConflictError(StructureEngineError):
    """A non-correction fact was submitted for an already-seen subject with
    different content — an ambiguous input the engine refuses to guess about.
    """


class OutOfOrderCandleError(StructureEngineError):
    """A candle was submitted with window_start earlier than the last-seen
    candle for the same (instrument, venue, timeframe) scope.
    """
