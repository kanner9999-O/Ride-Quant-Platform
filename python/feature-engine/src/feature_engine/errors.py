"""Shared, explicit technical failure modes (Error Handling Convention §7/§11).

Exception-based technical sentinels for genuine input/ordering/configuration
violations that have no domain/business representation — never used as
normal control flow for a valid domain outcome (§11's own governing
principle).
"""

from __future__ import annotations


class FeatureEngineError(Exception):
    """Base class for all feature-engine technical errors."""


class InvalidFeatureDefinitionError(FeatureEngineError):
    """A `FeatureDefinition` is internally invalid — missing a required
    field, declaring a contradictory combination of type-specific fields
    (e.g. both a candle and a regime upstream path), or using a
    non-canonical policy identifier.
    """


class UnsupportedFeatureFormulaError(FeatureEngineError):
    """The `FeatureFormula` supplied to a candle-path engine does not match
    the `FeatureDefinition`'s own pinned `formula_id` — feature.md leaves
    concrete Candle-derived formulas unresolved (no canonical ATR/stdev/
    realized-volatility/etc.), so this engine never guesses; it fails closed
    instead of silently substituting or inventing one.
    """


class EvidenceCardinalityError(FeatureEngineError):
    """After feature.md §8a canonical normalization/dedup, `input_fact_refs`
    did not contain exactly the role cardinality the `FeatureDefinition`
    pins for this `feature_type`.
    """


class EvidenceReferenceConflictError(FeatureEngineError):
    """The same authoritative `EventRecordRef` was supplied as evidence more
    than once with materially different fact content — never silently
    resolved via last-write-wins.
    """


class ForeignScopeError(FeatureEngineError):
    """A fact was submitted whose scope does not match this engine's/view's
    own scope — Feature scope is not global state (feature.md §16).
    """


class DefinitionVersionMismatchError(FeatureEngineError):
    """An upstream fact's own definition-version pin (e.g. a Regime fact's
    `regime_definition_version`, or a Swing fact's `swing_definition_version`)
    does not match the exact version the `FeatureDefinition` requires.
    """


class RegimeDimensionMismatchError(FeatureEngineError):
    """A `RegimeClassifiedFact` was submitted whose `regime_dimension` does
    not match the dimension this Feature Definition requires (`volatility`
    vs `directional_persistence`).
    """


class DuplicateCandleConflictError(FeatureEngineError):
    """A non-correction fact was submitted for an already-seen subject with
    different content — an ambiguous input the engine refuses to guess about.
    """


class OutOfOrderCorrectionError(FeatureEngineError):
    """A correction was submitted for a subject never previously ingested
    (Chapter 8 §8.3.4 causal precedence).
    """


class OutOfOrderCandleError(FeatureEngineError):
    """A candle was submitted with window_start earlier than the last-seen
    candle for the same (instrument, venue, timeframe) scope.
    """


class NonMonotonicRecordedTimeError(FeatureEngineError):
    """A fact was submitted with recorded_time earlier than the last-seen
    one for its own applicable scope — cursor-bounded visibility requires
    non-decreasing recorded_time order.
    """


class RecordedTimeSourceViolationError(FeatureEngineError):
    """The injected `RecordedTimeSource` returned a knowledge time that is
    not strictly later than the required causal floor.
    """


class FeatureLineageError(FeatureEngineError):
    """A `FeatureComputed`/`FeatureFactInvalidated` event violates
    feature.md §9's mandatory correction-lineage invariants for its
    (feature_subject_id, effective_window) — e.g. it does not target the
    current lineage head, a fact was invalidated more than once, or a
    replacement arrived before its own invalidation became visible.
    """


class ProhibitedInputError(FeatureEngineError):
    """An input was rejected because it is explicitly prohibited for this
    feature_type (e.g. a Structure BOS/CHoCH event, `SwingCandidateDetected`,
    or any `*-current-view` projection) — feature.md §14.
    """


class InvalidSwingEligibilityInputError(FeatureEngineError):
    """A Swing fact was submitted that cannot be evaluated for eligibility
    under feature.md §9a — e.g. it does not match this engine's configured
    scope/`swing_definition_version`/`swing_direction`, or its
    `swing_revision` does not advance exactly by one after an explicit
    invalidation of the prior revision (swing.md §1a).
    """


class UnsupportedDistanceRepresentationError(FeatureEngineError):
    """`distance_representation="signed"` was requested, but no
    authoritative sign-orientation convention exists in feature.md §6/§7.3
    (the contract leaves it an open enum value with no pinned semantics) —
    this engine never invents one; only `distance_representation="absolute"`
    (unambiguous magnitude, no orientation dependency) is computable.
    """


class UnauthorizedUpstreamContractError(FeatureEngineError):
    """An upstream fact's `event_contract_ref` (Chapter 8 §8.2.5) does not
    match any entry in the `FeatureDefinition`'s own pinned
    `upstream_contract_refs` (feature.md §6) — an input's contract
    qualification is never inferred/assumed, only exact-matched against
    definition-pinned authority.
    """
