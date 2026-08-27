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
    """Raised unconditionally by `CandleWindowFeatureEngine`'s constructor
    (P3-FEATURE-A-MAJ-03) — feature.md leaves concrete Candle-derived
    formulas unresolved (no canonical ATR/stdev/realized-volatility/etc.),
    and no current repository authority pins an immutable executable
    identity + parameters for any `formula_id`. A caller-supplied callable
    matched only by a `formula_id` string equality check is not real
    authorization, so this engine no longer accepts one at all — it fails
    closed instead of executing arbitrary caller-supplied code.
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
    exact-match (contract_id AND contract_version) any entry in the
    caller-injected authoritative contract set for this engine — an input's
    contract qualification is never inferred/assumed from `contract_id`
    alone, and never accepted merely because `contract_id` matches while
    `contract_version` is arbitrary (P3-FEATURE-A-MAJ-02).
    """


class UnresolvedOutputContractAuthorityError(FeatureEngineError):
    """The caller did not supply a genuine, non-empty
    `event_contract_ref.contract_version` for this engine's own outbound
    `FeatureComputed`/`FeatureFactInvalidated` events. `stream-registry.yaml`/
    a real Event Contract version authority does not exist yet in this
    repository (Phase 1, not yet authored) — this engine never invents a
    stand-in value (e.g. `"v0"`) for its own authoritative emission; if no
    genuine version is injected, it fails closed here instead
    (P3-FEATURE-A-MAJ-02).
    """


class UnresolvedComputationCursorAuthorityError(FeatureEngineError):
    """The caller did not supply a genuine, non-empty `input_contract_ref`,
    `stream_registry_version`, or `included_streams` at construction —
    `computation_cursor` (P3-FEATURE-A-MAJ-06, ADR-035 Approved) is never
    populated from an invented/fabricated identity; this engine fails
    closed instead.
    """


class RegistryContractMismatchError(FeatureEngineError):
    """A caller-supplied `EvaluationFrontier.stream_registry_version` does
    not exactly equal this engine's bound Input Contract's own pinned
    registry version (Chapter 8 §8.5 exact-pin rule; `feature-context-
    architecture.md` §4.6's registry-contract equality gate,
    P3-FEATURE-FRONTIER-A-MAJ-01). The bound Input Contract instance is not
    applicable at the caller's certified frontier — resolution requires a
    separate governed transaction, never a retry with the same arguments,
    and the cursor is never silently rebased onto a different registry.
    """


class EligibleSwingComputationDefectError(FeatureEngineError):
    """A candidate Swing that would otherwise win the deterministic total
    order at `R_later` was ALREADY full-cursor-visible (feature.md §12(a))
    at `R_original` but was not selected by the original computation. Per
    ADR-034 (Approved), this is NEVER representable as
    `eligible_swing_selection_superseded` — it is a computation/integrity
    defect of the ORIGINAL `FeatureComputed` (its own §9a total-order
    evaluation was not applied correctly at `R_original`), a completely
    different problem class from temporal supersession. This engine fails
    closed and loud rather than silently emitting, hiding, or "laundering"
    the defect through the supersession cause.
    """
