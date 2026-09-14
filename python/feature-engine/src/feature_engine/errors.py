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
    """An `OutputEventContractAuthorityProvider.resolve()` call did not
    return a genuine `VerifiedOutputEventContractAuthority` — either the
    wrong type entirely, or (for the injected provider itself) a
    profile/identity that does not match what this engine requires. This
    engine never invents a stand-in outbound `event_contract_ref` (e.g. the
    former `"v0"`/caller-injected-arbitrary-string patterns,
    P3-FEATURE-A-MAJ-02): its own outbound `feature-computed`/
    `feature-fact-invalidated` refs are only ever the genuine, resolved,
    `Published` Event Contract version-artifact identity (ADR-039); if a
    provider does not hand back that exact, genuine authority, this engine
    fails closed here instead.
    """


class OutputEventContractUnresolvableError(FeatureEngineError):
    """A Published Event Contract version-artifact could not be resolved at
    its own canonical, deterministic path (ADR-039:
    `docs/architecture/event-contracts/<contract_id>/<contract_version>.yaml`)
    — the file is missing, or its content does not resolve a complete
    `{contract_id, contract_version, status}` identity. Never falls back to
    git-history search, an alias, a registry, or any other lookup mechanism
    (ADR-039/ADR-040) — a canonical-path miss is always a genuine
    resolution failure.
    """


class OutputEventContractIdentityMismatchError(FeatureEngineError):
    """The Event Contract version-artifact resolved at a canonical path
    declares a `contract_id`/`contract_version` inside its own content that
    does not exactly match the `{contract_id, contract_version}` the path
    itself was constructed from — an artifact must self-identify
    consistently with its own canonical location; a mismatch is a
    resolution failure, never silently accepted or corrected.
    """


class OutputEventContractNotPublishedError(FeatureEngineError):
    """A resolved Event Contract version-artifact's own `status` is not
    exactly `"Published"` (ADR-039 §"Immutability and identifier
    non-reuse") — a `Draft` (or any other non-Published) artifact is never
    a usable `event_contract_ref` target for a real, persisted authoritative
    event (ADR-039/ADR-040's own retention/fail-closed posture); resolution
    fails closed here instead of treating a Draft as if it were final.
    """


class ReplayPreparationArtifactUnresolvableError(FeatureEngineError):
    """Replay preparation (ADR-037; `P3-FEATURE-QG-EVID-05(b)`) could not
    resolve the exact Input Contract/Stream Registry artifact a fact's own
    `computation_cursor` names, at all — the underlying authority-resolution
    failure (missing artifact, incomplete identity, Registry/Contract
    cross-validation failure) is ADR-037 failure class 1. Replay execution
    must never begin for this fact while this condition holds.
    """


class ReplayPreparationEvidenceMalformedError(FeatureEngineError):
    """A fact's own `computation_dependency_content_evidence` is missing or
    does not carry two well-formed (64 lowercase hex character) SHA-256
    content-identity digests — ADR-037 failure class 2. A schema-populated
    but non-well-formed value is never treated as usable evidence; Replay
    execution must never begin for this fact while this condition holds.
    """


class ReplayPreparationCursorReferenceMismatchError(FeatureEngineError):
    """The Input Contract/Stream Registry artifact actually resolved at
    Replay-preparation time does not exactly match the `input_contract_ref`/
    `stream_registry_version` pinned on the fact's own `computation_cursor`
    — ADR-037 failure class 3 (cursor/reference relational mismatch, e.g.
    the artifact has since evolved to a different `contract_version`/
    `registry_version` than the one this fact was originally computed
    against). Never silently rebased onto the currently-resolved identity;
    Replay execution must never begin for this fact while this condition
    holds.
    """


class ReplayPreparationContentIdentityMismatchError(FeatureEngineError):
    """The content-identity digest recomputed from the actual, current
    Input Contract/Stream Registry artifact bytes does not match the
    corresponding value persisted in the fact's own
    `computation_dependency_content_evidence` — ADR-037 failure class 4
    (content-ID mismatch: the artifact's own bytes changed since this fact
    was computed, even though its `{contract_id, contract_version}`/
    `registry_version` identity did not). Replay execution must never begin
    for this fact while this condition holds.
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


class InputContractIdentityMismatchError(FeatureEngineError):
    """A caller-supplied `ResolvedInputContract` does not match the
    currently-approved Input Contract identity (`contract_id`/
    `contract_version`/`stream_registry_version`/`included_streams`) known
    for the engine's own required Feature computation profile (Review-A
    residual 2 on `P3-FEATURE-A-MAJ-06`). Being merely internally
    self-consistent — three mutually-agreeing but invented strings — is
    explicitly NOT sufficient; this engine fails closed instead of accepting
    an unrecognized authority triple.
    """


class StreamPositionsUniverseMismatchError(FeatureEngineError):
    """A caller-supplied `EvaluationFrontier.stream_positions` key set is not
    EXACTLY the bound Input Contract's own `included_streams` — a missing
    stream, an extra stream, or an "all streams seen" fallback all fail
    closed here (ADR-035's own cardinality clause, Review-A residual 5).
    """


class CursorRelationalInvariantViolationError(FeatureEngineError):
    """A caller-supplied `EvaluationFrontier` violates one of Chapter 8
    §8.5.2's relational invariants (Position -> Cursor, Lifecycle -> Cursor,
    or the canonical Lifecycle Stream identity check), or supplies a
    genesis lifecycle frontier together with a fabricated lifecycle-event
    recorded_time proof (Review-A residual 4 on `P3-FEATURE-A-MAJ-06`). This
    engine fails closed rather than emitting a `computation_cursor` whose
    own fields are not mutually consistent.
    """


class UnsupportedMergePolicyError(FeatureEngineError):
    """An Input Contract's own `merge_policy` (ADR043-IMPLDESIGN-A-MAJ-04)
    is missing, malformed, structurally incomplete, or not one of the
    `algorithm`/`concurrent_tie_break` combinations this Feature
    implementation actually supports — for either the current-path or the
    exact pinned historical-snapshot resolver. Never silently normalized
    into the one supported combination; authority resolution fails closed
    here instead.
    """


class StaleOwnershipGenerationError(FeatureEngineError):
    """A `FencedFeatureCommitter` (ADR-043) rejected a commit attempt
    because the calling owner's `ownership_generation` is no longer the
    current, authoritative generation for its `feature_subject_id` — raised
    as part of the SAME indivisible verify+allocate+append operation, never
    by a separate prior check that could itself go stale before the write
    (ADR043-IMPLDESIGN-A-MAJ-01). The whole attempted batch has zero effect:
    no sequence consumed, no event appended, no local `_lineage` mutated.
    """


class DualOwnershipError(FeatureEngineError):
    """A `SubjectOwnershipAuthority` (ADR-043) was asked to activate a
    subject that already has another live, non-fenced owner generation —
    structurally prevented by genuine atomic-acquisition semantics; raised
    here only if that invariant is ever violated regardless. Never resolved
    by picking a runtime "winner" between the two.
    """


class OwnershipAuthorityUnavailableError(FeatureEngineError):
    """`SubjectOwnershipAuthority`/`FencedFeatureCommitter` (ADR-043) could
    not be reached, or an `AuthoritativeSubjectOwner` was asked to perform
    authoritative work while not genuinely `ACTIVE` (never acquired, still
    `CATCHING_UP`, `REVOKED`, or fenced unusable after a prior uncertain
    commit outcome), or `acquire_and_activate` was called again on an owner
    instance that has already gone TERMINAL after any prior failure
    (ADR043-IMPL-A-MAJ-05) — recovery always requires a fresh analytical
    engine instance, a fresh `AuthoritativeSubjectOwner`, a fresh ownership
    generation, and canonical catch-up, never reactivating the same owner.
    Never silently falls back to local-registry-only fencing or proceeds
    without a currently-recognized owner generation.
    """


class UnprovenCatchUpError(FeatureEngineError):
    """An `AuthoritativeLineageHistoryProvider` (ADR-043 §C) could not
    positively prove either a complete catch-up reconstruction or a
    genuinely empty subject — an absent, unreachable, or incomplete
    provider result is never treated as evidence of emptiness. A
    `CATCHING_UP -> ACTIVE` transition fails closed here instead.
    """


class CanonicalHistoryMismatchError(FeatureEngineError):
    """A recomputed historical candidate transition (ADR-043 §C reconciliation,
    `PreparedTransition.reconcile`) does not match the corresponding
    canonical, already-committed Feature output history supplied by an
    `AuthoritativeLineageHistoryProvider` — including a batch-length
    mismatch. Catch-up fails closed rather than silently preferring either
    the freshly recomputed candidate or the canonical record.
    """


class NonMonotonicApplicationOrderError(FeatureEngineError):
    """A certified apply set (ADR-043 §D `P_run`) could not be
    deterministically topologically sorted under `P_stream ∪ P_causation`
    plus the resolved Input Contract `merge_policy.concurrent_tie_break` —
    a genuine cycle/contradictory ordering, or an event whose relative
    order cannot be derived at all. The batch is rejected, never guessed.
    """


class IncompleteCertifiedFrontierError(FeatureEngineError):
    """An `AuthoritativeLineageHistoryProvider` (ADR-043 §D) returned an
    ambiguous, incomplete not-yet-applied apply-set result for a certified
    `EvaluationFrontier` — neither a genuine event list nor a positive
    proof of "nothing new to apply." Processing fails closed rather than
    guessing the apply set is empty.
    """


class OutputStreamEligibilityError(FeatureEngineError):
    """A Published Feature outbound Event Contract's own `allowed_streams`
    (ADR043-IMPL-A-MAJ-03) is missing, malformed, empty, names more than one
    stream this implementation cannot deterministically select among, or —
    between `feature-computed` and `feature-fact-invalidated` — the two
    contracts' own resolved `allowed_streams` disagree on which stream is
    authoritative. The genuine authoritative Feature output stream identity
    is never hard-coded; resolution fails closed here instead.
    """


class EngineNotPristineForCatchUpError(FeatureEngineError):
    """`AuthoritativeSubjectOwner.acquire_and_activate` (ADR043-IMPL-A-MAJ-05)
    was called against an analytical engine instance that already carries
    non-empty mutable analytical state — a newly acquired owner may only
    perform catch-up reconstruction into a genuinely pristine engine
    instance; an engine that has already processed ANY direct call (or a
    prior, now-abandoned authoritative attempt) is never reused for catch-up.
    """


class ProviderFrontierMismatchError(FeatureEngineError):
    """An `AuthoritativeLineageHistoryProvider` (ADR043-IMPL-A-MAJ-04)
    returned an ongoing-processing `UpstreamEnvelope` whose own `frontier`
    does not exactly equal the certified `EvaluationFrontier` the caller
    passed to `process_certified_frontier` — a provider may never evaluate
    events against one cursor while the owner advances its own committed
    checkpoint to a different, caller-supplied frontier. Processing fails
    closed before any such envelope is prepared or committed.
    """


class ConflictingUpstreamEnvelopeError(FeatureEngineError):
    """A certified apply set supplied to `p_run_sort` (ADR043-IMPL-A-MAJ-07)
    contains the same `EventRecordRef` more than once with materially
    different `UpstreamEnvelope` content — never resolved by input order
    (last-writer-wins); only a byte-for-byte identical redelivery of the
    same ref deterministically deduplicates to one. Fails closed instead of
    silently picking either candidate.
    """
