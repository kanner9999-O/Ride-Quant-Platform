"""`distance_to_last_confirmed_swing` (feature.md §7.3/§9a).

Exactly one reference Candle + exactly one Eligible Swing, selected via the
mandatory 5-step ordered filter pipeline (identity/scope match,
recorded-time visibility, effective-time cutoff STRICT `<`, latest valid
revision, not invalidated) followed by an 8-criterion deterministic total
order — never the reverse: the total order NEVER runs on a candidate that
failed the filter pipeline, and never "resurrects" an effective-time
ineligible Swing. Never consumes Structure `BreakOfStructureDetected`/
`ChangeOfCharacterDetected`/`StructureFactInvalidated`/`StructureRecomputed`
— only re-uses `structure.md` §6a's total-order *methodology*, as
feature.md §9a itself requires.

`distance_representation="signed"`: feature.md §6/§7.3 leaves the sign
orientation of `signed` genuinely unpinned — no authoritative convention
exists anywhere in the Domain Contract for which direction is positive.
This engine does NOT invent one; it fails closed
(`UnsupportedDistanceRepresentationError`) at construction time for
`signed`, and only computes `distance_representation="absolute"` (an
unambiguous, orientation-independent magnitude).

Contract qualification (P3-FEATURE-A-MAJ-02): the caller injects the exact
authorized `EventContractRef` set (contract_id AND contract_version) for
both the Candle and the Swing side at construction — `contract_id` matching
alone is never sufficient authorization for an arbitrary contract_version.
For the Swing side, `required_swing_definition_version` (validated in
`on_swing_confirmed`) additionally pins the confirmation-policy identity
ADR-014 requires ("required contract version HOẶC definition version được
pin"); for the Candle side, feature.md §6 has no per-definition version pin
for this feature_type, so the caller-injected authorized contract-ref set is
the only available exact-identity authority — this engine never accepts a
Candle contract_version the caller did not explicitly authorize.

Input Contract authority (P3-FEATURE-A-MAJ-06, Review-A round-2 residual 1):
`resolved_input_contract` is a REQUIRED constructor argument — a genuine,
already-resolved `ResolvedInputContract` (`contracts.py`) binding
`input_contract_ref`/`stream_registry_version`/`included_streams`/the exact
Feature computation profile/verifiable content-identity proof for BOTH the
Input Contract and Stream Registry artifacts it was resolved from. This
engine performs no filesystem/GitHub I/O itself and keeps no duplicate copy
of Input Contract/Stream Registry semantics — genuine resolution against the
real, current artifacts is the caller's own responsibility (dependency
injection; see `authority_resolver.py`'s
`resolve_input_contract_authority_from_repository` for the default,
filesystem-backed resolver this repository's own tests use).
`resolve_input_contract_authority` (called at construction) validates only
that the supplied object is structurally complete and matches this engine's
own required profile — never accepted merely because its semantic literals
happen to look right without accompanying content-identity evidence.

Computation cursor (P3-FEATURE-A-MAJ-06, ADR-035 Approved): `on_candle`/
`on_swing_confirmed`/`on_swing_invalidated` all take an explicit, required
`cursor: EvaluationFrontier` keyword argument — the caller-certified,
PROOF-CARRYING computation frontier (`recorded_time`, `stream_registry_
version`, `lifecycle_frontier`, `stream_positions`, each stream position and
the lifecycle frontier additionally carrying resolved-event-recorded-time
evidence) used for Swing eligibility (feature.md §9a step 2, full
three-branch predicate, §12) AND captured, together with this engine's own
bound Input Contract authority, into every emitted fact's
`computation_cursor` — after `resolve_computation_cursor` has verified every
Chapter 8 §8.5.2 relational invariant (Registry -> Contract, stream-
positions universe cardinality, Position -> Cursor, Lifecycle -> Cursor,
canonical Lifecycle Stream identity). This engine never substitutes
`R = candle.recorded_time`, a process-local datetime, an invented registry
value, or an incomplete Feature-local surrogate; callers/orchestrators that
have actually performed `feature-context-architecture.md` §4.6's
lifecycle-bracketed, registry-pinned direct-log-read certification supply
the full, proof-carrying frontier explicitly. Every emitted fact's own
`recorded_time` floor additionally includes `cursor.recorded_time` — Chapter
8 §8.5.2's Cursor -> Fact invariant (`computation_cursor.recorded_time <=
FeatureComputed/FeatureFactInvalidated.recorded_time`) is therefore
structurally guaranteed, never merely hoped for.

History-preserving Swing state (ADR-035 Approved, "Implementation
consequence"; Review-A residual 1): Swing confirmation/invalidation
evidence is stored append-only (`_swing_confirmations`/`_swing_invalidations`
— a new revision or invalidation is NEVER destructively overwritten in
place) so that Eligible-Swing state can be correctly reconstructed AS OF ANY
valid `computation_cursor`, not only the latest process-local view. Ingesting
a later Swing revision or invalidation never retroactively changes what an
earlier-cursor query would answer.

Correction propagation (P3-FEATURE-A-MAJ-04): a corrected Swing revision
becoming visible re-resolves EVERY window it could affect — not only windows
currently `PENDING_CORRECTION`, but also windows that already settled on an
alternate, lower-priority eligible Swing while the preferred Swing was
invalidated. If the deterministic total-order winner changes, the settled
window is invalidated and replaced again (feature.md §3 "no shortcut") with
`invalidation_cause="eligible_swing_selection_superseded"` (ADR-034,
Approved) — never a fabricated `swing_invalidated`, since the previously-used
Swing itself was never invalidated. A winner that was ALREADY visible at the
original fact's own `computation_cursor` but not selected then is never
representable via this cause — this engine fails closed
(`EligibleSwingComputationDefectError`) instead, per ADR-034's own explicit
prohibition on "laundering" a computation defect through this invalidation
cause.

Immutable-ref integrity (P3-FEATURE-A-MAJ-05): both Candle and Swing
ingestion validate, before any dedup/routing/lineage logic runs, that a
redelivered `EventRecordRef` resolves to byte-for-byte identical consumer-
side fact content (recorded_time, contract qualification, revision/
correction fields, payload) — any difference fails closed
(`EvidenceReferenceConflictError`); a genuinely distinct ref always enters
lineage even when the recomputed value is unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .candle import CandleFact
from .contracts import (
    CANDLE_CLOSED_CONTRACT_ID,
    CANDLE_CORRECTED_CONTRACT_ID,
    SWING_CONFIRMED_CONTRACT_ID,
    SWING_INVALIDATED_CONTRACT_ID,
    ComputationCursor,
    EvaluationFrontier,
    FeatureComputationProfile,
    FeatureComputed,
    FeatureDefinition,
    FeatureEvent,
    FeatureFactInvalidated,
    FeatureScope,
    RecordedTimeSource,
    ResolvedInputContract,
    is_visible_at_cursor,
    resolve_computation_cursor,
    resolve_input_contract_authority,
    resolve_output_contract_refs,
)
from .envelope import EventContractRef, EventRecordRef
from .errors import (
    DuplicateCandleConflictError,
    EligibleSwingComputationDefectError,
    EvidenceCardinalityError,
    EvidenceReferenceConflictError,
    ForeignScopeError,
    InvalidFeatureDefinitionError,
    InvalidSwingEligibilityInputError,
    NonMonotonicRecordedTimeError,
    OutOfOrderCandleError,
    OutOfOrderCorrectionError,
    RecordedTimeSourceViolationError,
    UnauthorizedUpstreamContractError,
    UnsupportedDistanceRepresentationError,
)
from .publish import SequenceAllocator
from .swing_input import SwingConfirmedFact, SwingInvalidatedFact

# NOTE: this is a deterministic tie-break KEY component only (feature.md §6's
# own named policies, e.g. ELIGIBLE_SWING_SELECTION_POLICY's
# "...then_registry_version_asc..." clause) — it is never exposed as, or used
# for, computation_cursor.stream_registry_version (P3-FEATURE-A-MAJ-06), which
# is exclusively resolved from this engine's own bound `ResolvedInputContract`
# (`self._resolved_input_contract`, below). Any fixed string is equally valid
# here as long as it is applied consistently across all evidence being
# ordered, which it is.
_TIEBREAK_REGISTRY_VERSION = "v0"
_ALLOWED_CANDLE_CONTRACT_IDS = frozenset({CANDLE_CLOSED_CONTRACT_ID, CANDLE_CORRECTED_CONTRACT_ID})
_ALLOWED_SWING_CONTRACT_IDS = frozenset({SWING_CONFIRMED_CONTRACT_ID, SWING_INVALIDATED_CONTRACT_ID})
_REQUIRED_INPUT_CONTRACT_PROFILE: FeatureComputationProfile = "distance_to_last_confirmed_swing"


@dataclass(frozen=True, slots=True)
class _SwingConfirmationRecord:
    """One immutable, append-only `SwingConfirmed` ingestion record (ADR-035
    "Implementation consequence" / Review-A residual 1). Never mutated or
    overwritten after append — a later revision's own record is a new list
    entry, never a replacement of this one.
    """

    revision: int
    pivot_price: Decimal
    pivot_effective_time: tuple[datetime, datetime]
    recorded_time: datetime
    ref: EventRecordRef
    source_fact: SwingConfirmedFact


@dataclass(frozen=True, slots=True)
class _SwingInvalidationRecord:
    """One immutable, append-only `SwingInvalidated` ingestion record for a
    specific `(swing_id, revision)` pair — at most one ever exists per pair
    (swing.md §1a: a revision is invalidated at most once).
    """

    revision: int
    recorded_time: datetime
    ref: EventRecordRef


@dataclass(slots=True)
class _SwingState:
    """A MATERIALIZED view of a swing_id's eligibility state as of one
    specific computation cursor (`_swing_state_as_of`, below) — never itself
    a piece of durable storage. Returned only when that swing_id is, as of
    that cursor, confirmed and not (yet) invalidated.
    """

    revision: int
    pivot_price: Decimal
    pivot_effective_time: tuple[datetime, datetime]
    recorded_time: datetime
    ref: EventRecordRef
    source_fact: SwingConfirmedFact


@dataclass(slots=True)
class _WindowLineage:
    head_fact: FeatureComputed
    invalidated: bool
    used_swing_id: str
    used_swing_ref: EventRecordRef
    pending_invalidation_ref: EventRecordRef | None = None
    pending_invalidation_recorded_time: datetime | None = None


def _total_order_key(swing_id: str, state: _SwingState) -> tuple[float, datetime, str, str, int, int, str, str]:
    """feature.md §9a's 8-criterion deterministic total order, applied ONLY
    to candidates that already passed the 5-step filter pipeline. DESC
    criteria (pivot window_start, swing_revision) are encoded as negated
    values so the overall winner is the lexicographic MINIMUM of this key.
    """
    return (
        -state.pivot_effective_time[0].timestamp(),
        state.recorded_time,
        state.ref.stream_id,
        _TIEBREAK_REGISTRY_VERSION,
        state.ref.sequence,
        -state.revision,
        swing_id,
        state.ref.event_id,
    )


class SwingDistanceFeatureEngine:
    """One instance per Feature subject. Each authoritative reference Candle
    produces at most one `FeatureComputed`, independently — no window
    aggregation across multiple candles.
    """

    def __init__(
        self,
        scope: FeatureScope,
        definition: FeatureDefinition,
        allocator: SequenceAllocator,
        time_source: RecordedTimeSource,
        *,
        feature_event_contract_version: str,
        authorized_candle_contract_refs: frozenset[EventContractRef],
        authorized_swing_contract_refs: frozenset[EventContractRef],
        resolved_input_contract: ResolvedInputContract,
        stream_id: str = "feature",
    ) -> None:
        if definition.feature_type != "distance_to_last_confirmed_swing":
            raise ValueError(f"unsupported feature_type: {definition.feature_type!r}")
        if scope.feature_type != definition.feature_type or scope.feature_definition_version != (
            definition.feature_definition_version
        ):
            raise ValueError("scope does not match definition")
        if definition.distance_representation == "signed":
            raise UnsupportedDistanceRepresentationError(
                "distance_representation='signed' has no authoritative sign-orientation convention pinned "
                "anywhere in feature.md §6/§7.3 — this engine does not invent one; only "
                "distance_representation='absolute' is currently computable"
            )
        if not authorized_candle_contract_refs:
            raise InvalidFeatureDefinitionError("authorized_candle_contract_refs must be non-empty")
        for candle_ref in authorized_candle_contract_refs:
            if candle_ref.contract_id not in _ALLOWED_CANDLE_CONTRACT_IDS:
                raise InvalidFeatureDefinitionError(
                    f"authorized_candle_contract_refs contains unsupported contract_id "
                    f"{candle_ref.contract_id!r} (must be one of {sorted(_ALLOWED_CANDLE_CONTRACT_IDS)!r})"
                )
        if not authorized_swing_contract_refs:
            raise InvalidFeatureDefinitionError("authorized_swing_contract_refs must be non-empty")
        for swing_ref in authorized_swing_contract_refs:
            if swing_ref.contract_id not in _ALLOWED_SWING_CONTRACT_IDS:
                raise InvalidFeatureDefinitionError(
                    f"authorized_swing_contract_refs contains unsupported contract_id "
                    f"{swing_ref.contract_id!r} (must be one of {sorted(_ALLOWED_SWING_CONTRACT_IDS)!r})"
                )
        self._output_contract_ref, self._invalidation_contract_ref = resolve_output_contract_refs(
            feature_event_contract_version
        )
        self._resolved_input_contract = resolve_input_contract_authority(
            resolved_input_contract, required_profile=_REQUIRED_INPUT_CONTRACT_PROFILE
        )
        self._authorized_candle_contract_refs = authorized_candle_contract_refs
        self._authorized_swing_contract_refs = authorized_swing_contract_refs
        self.scope = scope
        self.definition = definition
        self._allocator = allocator
        self._time_source = time_source
        self._stream_id = stream_id
        self._candles: list[CandleFact] = []
        self._candle_index: dict[str, int] = {}
        self._candle_by_window: dict[tuple[datetime, datetime], CandleFact] = {}
        # Candle and Swing are independent upstream streams (Chapter 8 §8.3.3 — no
        # invented global cross-stream order); a Swing confirmation can be recorded
        # much later than its own pivot (right-side evidence accumulation), with no
        # required interleaving relationship to Candle recorded_time at all. Each
        # stream's own monotonicity is tracked and enforced independently.
        self._last_candle_recorded_time: datetime | None = None
        self._last_swing_recorded_time: datetime | None = None
        # ADR-035 "Implementation consequence" / Review-A residual 1: append-only
        # historical evidence, NEVER a single-current-revision mutable dict — see
        # `_swing_state_as_of` for how eligibility as-of an arbitrary cursor is
        # reconstructed from this history.
        self._swing_confirmations: dict[str, list[_SwingConfirmationRecord]] = {}
        self._swing_invalidations: dict[tuple[str, int], _SwingInvalidationRecord] = {}
        self._lineage: dict[tuple[datetime, datetime], _WindowLineage] = {}

    # -- shared ordering / recorded-time causality -----------------------

    def _check_candle_scope(self, candle: CandleFact) -> None:
        if (
            candle.scope.instrument_id != self.scope.instrument_id
            or candle.scope.venue_id != self.scope.venue_id
            or candle.scope.timeframe != self.scope.timeframe
        ):
            raise ForeignScopeError(f"candle scope {candle.scope!r} does not match engine scope {self.scope!r}")

    def _check_candle_contract(self, candle: CandleFact) -> None:
        if candle.event_contract_ref not in self._authorized_candle_contract_refs:
            raise UnauthorizedUpstreamContractError(
                f"candle event_contract_ref={candle.event_contract_ref!r} is not one of the authorized candle "
                f"contract refs {sorted(self._authorized_candle_contract_refs, key=str)!r} — contract_id alone "
                "matching is insufficient (P3-FEATURE-A-MAJ-02)"
            )

    def _check_swing_contract(self, contract_ref: EventContractRef) -> None:
        if contract_ref not in self._authorized_swing_contract_refs:
            raise UnauthorizedUpstreamContractError(
                f"swing event_contract_ref={contract_ref!r} is not one of the authorized swing contract refs "
                f"{sorted(self._authorized_swing_contract_refs, key=str)!r} — contract_id alone matching is "
                "insufficient (P3-FEATURE-A-MAJ-02)"
            )

    def _check_candle_recorded_time(self, recorded_time: datetime) -> None:
        if self._last_candle_recorded_time is not None and recorded_time < self._last_candle_recorded_time:
            raise NonMonotonicRecordedTimeError(
                f"candle recorded_time {recorded_time!r} precedes last-seen {self._last_candle_recorded_time!r}"
            )
        self._last_candle_recorded_time = recorded_time

    def _check_swing_recorded_time(self, recorded_time: datetime) -> None:
        if self._last_swing_recorded_time is not None and recorded_time < self._last_swing_recorded_time:
            raise NonMonotonicRecordedTimeError(
                f"swing recorded_time {recorded_time!r} precedes last-seen {self._last_swing_recorded_time!r}"
            )
        self._last_swing_recorded_time = recorded_time

    def _next_recorded_time(self, strict_floor: datetime) -> datetime:
        candidate = self._time_source.next_after(strict_floor)
        if not candidate > strict_floor:
            raise RecordedTimeSourceViolationError(
                f"RecordedTimeSource.next_after({strict_floor!r}) returned {candidate!r}, not strictly later"
            )
        return candidate

    def _resolve_cursor(self, frontier: EvaluationFrontier) -> ComputationCursor:
        """P3-FEATURE-A-MAJ-06: the single place this engine assembles its own
        outbound `computation_cursor` from a caller-supplied `EvaluationFrontier`
        — fails closed if any Chapter 8 §8.5.2 relational invariant does not
        hold against this engine's own bound Input Contract authority.
        """
        return resolve_computation_cursor(frontier, resolved_input_contract=self._resolved_input_contract)

    # -- Swing ingestion (append-only historical evidence) ------------------

    def _latest_confirmation(self, swing_id: str) -> _SwingConfirmationRecord | None:
        records = self._swing_confirmations.get(swing_id)
        return records[-1] if records else None

    def _swing_state_as_of(self, swing_id: str, cursor: EvaluationFrontier) -> _SwingState | None:
        """Reconstructs swing_id's eligibility state AS OF `cursor`, purely
        from the append-only confirmation/invalidation history — never from
        any single-current-revision mutable field (ADR-035, Review-A
        residual 1). The highest-revision confirmation that is full-cursor-
        visible at `cursor` (feature.md §12(a)) is the candidate; if its own
        matching invalidation record is ALSO visible at `cursor`, swing_id is
        not eligible as of this cursor (no later revision is visible yet).
        """
        records = self._swing_confirmations.get(swing_id)
        if not records:
            return None
        positions = cursor.plain_stream_positions()
        visible = [
            record
            for record in records
            if is_visible_at_cursor(
                record.ref,
                record.recorded_time,
                included_streams=self._resolved_input_contract.included_streams,
                stream_positions=positions,
                cursor_recorded_time=cursor.recorded_time,
            )
        ]
        if not visible:
            return None
        latest = max(visible, key=lambda record: record.revision)
        invalidation = self._swing_invalidations.get((swing_id, latest.revision))
        if invalidation is not None and is_visible_at_cursor(
            invalidation.ref,
            invalidation.recorded_time,
            included_streams=self._resolved_input_contract.included_streams,
            stream_positions=positions,
            cursor_recorded_time=cursor.recorded_time,
        ):
            return None  # invalidated as of this cursor; no later revision visible here yet
        return _SwingState(
            revision=latest.revision,
            pivot_price=latest.pivot_price,
            pivot_effective_time=latest.pivot_effective_time,
            recorded_time=latest.recorded_time,
            ref=latest.ref,
            source_fact=latest.source_fact,
        )

    def on_swing_confirmed(self, fact: SwingConfirmedFact, *, cursor: EvaluationFrontier) -> list[FeatureEvent]:
        """`cursor` is the explicit, caller-certified `EvaluationFrontier`
        (P3-FEATURE-A-MAJ-06) used to re-evaluate Swing eligibility for
        every window once this fact becomes visible — never implicitly
        derived from `fact.recorded_time`.

        Review-A round-2 residual 2: `cursor` is fully certified against this
        engine's own bound authority BEFORE any state mutation below — a
        rejected frontier leaves `_swing_confirmations`/`_swing_invalidations`/
        `_last_swing_recorded_time` untouched, so the exact same authoritative
        event retried later with a valid frontier is processed exactly as if
        the rejected attempt had never happened (no sequence/ref allocation,
        no dedup/lineage state, is committed by a rejected transaction).
        """
        self._resolve_cursor(cursor)
        if (
            fact.instrument_id != self.scope.instrument_id
            or fact.venue_id != self.scope.venue_id
            or fact.timeframe != self.scope.timeframe
        ):
            raise ForeignScopeError("SwingConfirmed scope does not match this Feature engine's own scope")
        self._check_swing_contract(fact.event_contract_ref)

        # P3-FEATURE-A-MAJ-05: immutable-ref consistency check BEFORE any
        # dedup/routing/lineage logic below. Same EventRecordRef with ANY
        # difference in the complete consumer-side fact representation
        # (recorded_time, contract qualification, revision, pivot fields,
        # ...) fails closed; only byte-for-byte identical redelivery is an
        # idempotent no-op.
        existing = self._latest_confirmation(fact.swing_id)
        if existing is not None and existing.ref == fact.ref:
            if existing.source_fact != fact:
                raise EvidenceReferenceConflictError(
                    f"swing ref {fact.ref!r} resolves to conflicting SwingConfirmed content "
                    f"({existing.source_fact!r} vs {fact!r})"
                )
            return []  # duplicate delivery of the identical authoritative event

        if fact.swing_definition_version != self.definition.required_swing_definition_version:
            raise InvalidSwingEligibilityInputError(
                f"expected swing_definition_version={self.definition.required_swing_definition_version!r}, "
                f"got {fact.swing_definition_version!r}"
            )
        if fact.direction != self.definition.swing_direction:
            raise InvalidSwingEligibilityInputError(
                f"expected swing_direction={self.definition.swing_direction!r}, got {fact.direction!r}"
            )
        self._check_swing_recorded_time(fact.recorded_time)

        # swing.md §1a: swing_revision starts at 1 and a revision N+1 is only valid
        # once revision N has been EXPLICITLY invalidated in this engine's own
        # tracked history — Feature independently enforces this ordering, never
        # trusting that the producer's own causation chain alone is sufficient.
        if existing is None:
            if fact.swing_revision != 1:
                raise InvalidSwingEligibilityInputError(
                    f"swing_id {fact.swing_id!r} first-seen revision must be 1, got {fact.swing_revision!r}"
                )
        else:
            if (fact.swing_id, existing.revision) not in self._swing_invalidations:
                raise InvalidSwingEligibilityInputError(
                    f"swing_id {fact.swing_id!r} revision {fact.swing_revision!r} received before revision "
                    f"{existing.revision!r} was explicitly invalidated"
                )
            if fact.swing_revision != existing.revision + 1:
                raise InvalidSwingEligibilityInputError(
                    f"swing_id {fact.swing_id!r} revision must advance by exactly one: expected "
                    f"{existing.revision + 1!r}, got {fact.swing_revision!r}"
                )

        self._swing_confirmations.setdefault(fact.swing_id, []).append(
            _SwingConfirmationRecord(
                revision=fact.swing_revision,
                pivot_price=fact.pivot_price,
                pivot_effective_time=fact.pivot_effective_time,
                recorded_time=fact.recorded_time,
                ref=fact.ref,
                source_fact=fact,
            )
        )
        # P3-FEATURE-A-MAJ-04: a newly-visible Swing revision may resolve a Feature
        # window that was left PENDING_CORRECTION because no eligible Swing existed
        # at the time it was invalidated, AND may preempt a window that already
        # settled on a lower-priority alternate Swing — re-evaluate every window
        # with a lineage entry now that this revision is visible.
        return self._reevaluate_all_windows(cursor)

    def on_swing_invalidated(
        self, invalidation: SwingInvalidatedFact, *, cursor: EvaluationFrontier
    ) -> list[FeatureEvent]:
        """`cursor` is the explicit, caller-certified `EvaluationFrontier`
        (P3-FEATURE-A-MAJ-06) used to immediately reattempt the
        just-invalidated window — never implicitly derived from
        `invalidation.recorded_time`.

        Review-A round-2 residual 2: `cursor` is fully certified against this
        engine's own bound authority BEFORE `_swing_invalidations` is
        mutated — a rejected frontier leaves the targeted revision's
        non-invalidated state untouched, so a valid retry of the exact same
        invalidation is processed normally.
        """
        self._resolve_cursor(cursor)
        existing = self._latest_confirmation(invalidation.swing_id)
        already_invalidated = existing is not None and (
            invalidation.swing_id,
            existing.revision,
        ) in self._swing_invalidations
        if existing is None or existing.revision != invalidation.swing_revision or already_invalidated:
            raise InvalidSwingEligibilityInputError(
                f"SwingInvalidated targets ({invalidation.swing_id!r}, {invalidation.swing_revision!r}), which is "
                "not the current non-invalidated revision tracked by this engine"
            )
        self._check_swing_contract(invalidation.event_contract_ref)
        self._check_swing_recorded_time(invalidation.recorded_time)
        invalidated_ref = existing.ref
        self._swing_invalidations[(invalidation.swing_id, invalidation.swing_revision)] = _SwingInvalidationRecord(
            revision=invalidation.swing_revision, recorded_time=invalidation.recorded_time, ref=invalidation.ref
        )

        events: list[FeatureEvent] = []
        for key, lineage in list(self._lineage.items()):
            if lineage.invalidated or lineage.used_swing_ref != invalidated_ref:
                continue
            events.extend(
                self._invalidate_and_reattempt(key, lineage, invalidation.ref, invalidation.recorded_time, cursor)
            )
        return events

    # -- Candle ingestion ---------------------------------------------------

    def on_candle(self, fact: CandleFact, *, cursor: EvaluationFrontier) -> list[FeatureEvent]:
        """`cursor` is the explicit, caller-certified `EvaluationFrontier`
        (feature.md §9a step 2, §12; P3-FEATURE-A-MAJ-06) used for Swing
        eligibility when computing this Candle's window — never implicitly
        substituted with `fact.recorded_time`. A live/real-time caller MAY
        choose to set `cursor.recorded_time = fact.recorded_time` explicitly,
        but that is a caller decision, never an engine default.

        Review-A round-2 residual 2: `cursor` is fully certified against this
        engine's own bound authority BEFORE `_candles`/`_candle_index`/
        `_candle_by_window`/`_last_candle_recorded_time` are mutated — a
        rejected frontier leaves Candle dedup/routing state untouched, so a
        valid retry of the exact same Candle ref (original or correction) is
        processed exactly as a first attempt would be. Validated even when
        this specific call will end up producing no Feature output at all
        (e.g. no eligible Swing) — the frontier is the certified computation
        frontier for THIS operation regardless of what it ultimately yields.
        """
        self._resolve_cursor(cursor)
        self._check_candle_scope(fact)
        self._check_candle_contract(fact)
        subject_id = fact.scope.subject_id
        existing_index = self._candle_index.get(subject_id)

        if existing_index is not None:
            existing = self._candles[existing_index]
            if existing.ref == fact.ref:
                # P3-FEATURE-A-MAJ-05: full consumer-side fact equality, not just
                # OHLCV — recorded_time/contract qualification/is_correction must
                # also match for a redelivery of the same ref to be idempotent.
                if existing != fact:
                    raise EvidenceReferenceConflictError(
                        f"candle ref {fact.ref!r} resolves to conflicting content ({existing!r} vs {fact!r})"
                    )
                return []  # duplicate delivery of the identical authoritative event
            if not fact.is_correction:
                raise DuplicateCandleConflictError(
                    f"candle {subject_id!r} resubmitted with a different ref but is_correction=False"
                )
            # A distinct correction ref MUST enter lineage even when the recomputed
            # value/payload is unchanged (feature.md §3 "no shortcut") — dedup is
            # keyed on ref identity only, never on value/content equality.
            self._check_candle_recorded_time(fact.recorded_time)
            self._candles[existing_index] = fact
            self._candle_by_window[(fact.scope.window_start, fact.scope.window_end)] = fact
            return self._recompute(
                fact, correction_ref=fact.ref, correction_recorded_time=fact.recorded_time, cursor=cursor
            )

        if fact.is_correction:
            raise OutOfOrderCorrectionError(f"correction submitted for never-seen candle {subject_id!r}")
        if self._candles and fact.scope.window_start < self._candles[-1].scope.window_start:
            raise OutOfOrderCandleError(
                f"candle window_start {fact.scope.window_start!r} precedes last-seen "
                f"{self._candles[-1].scope.window_start!r}"
            )
        self._check_candle_recorded_time(fact.recorded_time)
        self._candles.append(fact)
        self._candle_index[subject_id] = len(self._candles) - 1
        self._candle_by_window[(fact.scope.window_start, fact.scope.window_end)] = fact
        return self._recompute(fact, correction_ref=None, correction_recorded_time=None, cursor=cursor)

    # -- eligible-swing selection (feature.md §9a) --------------------------

    def _select_eligible_swing(
        self, reference_cutoff: datetime, cursor: EvaluationFrontier
    ) -> tuple[str, _SwingState] | None:
        """`cursor` is the explicit, caller-certified `EvaluationFrontier`
        (feature.md §9a step 2) — supplied by the caller of `on_candle`/
        `on_swing_confirmed`/`on_swing_invalidated`, never derived here. A
        Swing is a candidate only if it is BOTH full-cursor-visible at `R`
        (feature.md §12(a), the complete three-branch predicate — NEVER a
        scalar `recorded_time`-only test) AND effective-time eligible; never
        one condition alone (feature.md §12 "hai điều kiện ĐỘC LẬP"). Both
        conditions are evaluated via `_swing_state_as_of`'s append-only
        historical reconstruction (ADR-035, Review-A residual 1) — never a
        destructive single-current-revision lookup.
        """
        candidates: list[tuple[str, _SwingState]] = []
        for swing_id in self._swing_confirmations:
            state = self._swing_state_as_of(swing_id, cursor)
            if state is not None and state.pivot_effective_time[0] < reference_cutoff:
                candidates.append((swing_id, state))
        if not candidates:
            return None
        return min(candidates, key=lambda item: _total_order_key(item[0], item[1]))

    # -- evidence normalization (candle + swing, heterogeneous pair) --------

    @staticmethod
    def _normalize_evidence(
        candle: CandleFact, swing_ref: EventRecordRef, swing_effective: tuple[datetime, datetime]
    ) -> tuple[EventRecordRef, ...]:
        if candle.ref == swing_ref:
            raise EvidenceReferenceConflictError(f"candle ref and swing ref collide: {candle.ref!r}")
        items = [
            (candle.scope.window_start, candle.scope.window_end, candle.ref),
            (swing_effective[0], swing_effective[1], swing_ref),
        ]

        def _sort_key(item: tuple[datetime, datetime, EventRecordRef]) -> tuple[datetime, datetime, str, str, int, str]:
            start, end, ref = item
            return (start, end, ref.stream_id, _TIEBREAK_REGISTRY_VERSION, ref.sequence, ref.event_id)

        items.sort(key=_sort_key)
        refs = tuple(item[2] for item in items)
        if len(set(refs)) != 2:
            raise EvidenceCardinalityError(f"expected exactly 2 unique evidence refs, got {len(set(refs))}")
        return refs

    def _compute_distance(self, candle: CandleFact, state: _SwingState) -> Decimal:
        assert self.definition.reference_price_field is not None
        assert self.definition.distance_representation == "absolute"
        reference_price = candle.ohlcv.field(self.definition.reference_price_field)
        raw = abs(reference_price - state.pivot_price)
        return self.definition.decimal_precision_policy.apply(raw)

    # -- computation orchestration -------------------------------------------

    def _recompute(
        self,
        candle: CandleFact,
        *,
        correction_ref: EventRecordRef | None,
        correction_recorded_time: datetime | None,
        cursor: EvaluationFrontier,
    ) -> list[FeatureEvent]:
        key = (candle.scope.window_start, candle.scope.window_end)
        winner = self._select_eligible_swing(candle.scope.window_end, cursor)
        existing = self._lineage.get(key)

        if winner is None:
            return []  # valid absence — no eligible Swing

        swing_id, state = winner

        if existing is None:
            return self._emit_original(key, candle, swing_id, state, cursor)

        if not existing.invalidated:
            # Reaching here means an unchanged lineage already exists for this exact window and this
            # call is a genuine candle correction (feature.md §3: no shortcut, even if value is unchanged).
            assert correction_ref is not None and correction_recorded_time is not None
            return self._invalidate_and_replace(
                key,
                candle,
                swing_id,
                state,
                existing,
                correction_ref=correction_ref,
                correction_recorded_time=correction_recorded_time,
                cursor=cursor,
            )

        # existing.invalidated: a pending window (from a prior Swing invalidation) is being retried
        # because the reference Candle itself is also being corrected right now.
        assert existing.pending_invalidation_ref is not None
        assert existing.pending_invalidation_recorded_time is not None
        return self._emit_replacement_only(
            key,
            candle,
            swing_id,
            state,
            existing.pending_invalidation_ref,
            existing.pending_invalidation_recorded_time,
            cursor,
        )

    def _emit_original(
        self,
        key: tuple[datetime, datetime],
        candle: CandleFact,
        swing_id: str,
        state: _SwingState,
        cursor: EvaluationFrontier,
    ) -> list[FeatureEvent]:
        normalized_refs = self._normalize_evidence(candle, state.ref, state.pivot_effective_time)
        # Chapter 8 §8.5.2 Cursor -> Fact: the emitted recorded_time floor includes
        # cursor.recorded_time, structurally guaranteeing computation_cursor.recorded_time
        # <= FeatureComputed.recorded_time (Review-A residual 4) — never merely evidence-derived.
        floor = max(candle.recorded_time, state.recorded_time, cursor.recorded_time)
        recorded_time = self._next_recorded_time(floor)
        value = self._compute_distance(candle, state)
        fact = FeatureComputed(
            scope=self.scope,
            value=value,
            unit=self.definition.unit,
            window_start=key[0],
            window_end=key[1],
            input_fact_refs=normalized_refs,
            supersedes_fact_ref=None,
            causation_refs=normalized_refs,
            recorded_time=recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
            event_contract_ref=self._output_contract_ref,
            computation_cursor=self._resolve_cursor(cursor),
        )
        self._lineage[key] = _WindowLineage(
            head_fact=fact, invalidated=False, used_swing_id=swing_id, used_swing_ref=state.ref
        )
        return [fact]

    def _invalidate_and_replace(
        self,
        key: tuple[datetime, datetime],
        candle: CandleFact,
        swing_id: str,
        state: _SwingState,
        existing: _WindowLineage,
        *,
        correction_ref: EventRecordRef,
        correction_recorded_time: datetime,
        cursor: EvaluationFrontier,
    ) -> list[FeatureEvent]:
        invalidation_floor = max(existing.head_fact.recorded_time, correction_recorded_time, cursor.recorded_time)
        invalidation_recorded_time = self._next_recorded_time(invalidation_floor)
        invalidation = FeatureFactInvalidated(
            scope=existing.head_fact.scope,
            invalidated_fact_ref=existing.head_fact.ref,
            invalidation_cause="candle_corrected",
            window_start=existing.head_fact.window_start,
            window_end=existing.head_fact.window_end,
            causation_refs=(existing.head_fact.ref, correction_ref),
            recorded_time=invalidation_recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
            event_contract_ref=self._invalidation_contract_ref,
            computation_cursor=self._resolve_cursor(cursor),
        )
        events: list[FeatureEvent] = [invalidation]
        events.extend(
            self._emit_replacement_only(
                key, candle, swing_id, state, invalidation.ref, invalidation_recorded_time, cursor
            )
        )
        return events

    def _emit_replacement_only(
        self,
        key: tuple[datetime, datetime],
        candle: CandleFact,
        swing_id: str,
        state: _SwingState,
        invalidation_ref: EventRecordRef,
        invalidation_recorded_time: datetime,
        cursor: EvaluationFrontier,
    ) -> list[FeatureEvent]:
        existing = self._lineage[key]
        normalized_refs = self._normalize_evidence(candle, state.ref, state.pivot_effective_time)
        # Floor on ALL of: the invalidation this replaces, both pieces of its own
        # evidence's recorded_time, AND cursor.recorded_time (Chapter 8 §8.5.2
        # Cursor -> Fact, Review-A residual 4) — a replacement triggered by a
        # newly-visible Swing revision (§9a reattempt) must not be recorded_time-
        # earlier than that Swing's own recorded_time or this cursor's own boundary.
        floor = max(invalidation_recorded_time, candle.recorded_time, state.recorded_time, cursor.recorded_time)
        recorded_time = self._next_recorded_time(floor)
        value = self._compute_distance(candle, state)
        replacement = FeatureComputed(
            scope=self.scope,
            value=value,
            unit=self.definition.unit,
            window_start=key[0],
            window_end=key[1],
            input_fact_refs=normalized_refs,
            supersedes_fact_ref=existing.head_fact.ref,
            causation_refs=(*normalized_refs, invalidation_ref),
            recorded_time=recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
            event_contract_ref=self._output_contract_ref,
            computation_cursor=self._resolve_cursor(cursor),
        )
        self._lineage[key] = _WindowLineage(
            head_fact=replacement, invalidated=False, used_swing_id=swing_id, used_swing_ref=state.ref
        )
        return [replacement]

    def _invalidate_and_reattempt(
        self,
        key: tuple[datetime, datetime],
        lineage: _WindowLineage,
        correction_ref: EventRecordRef,
        correction_recorded_time: datetime,
        cursor: EvaluationFrontier,
    ) -> list[FeatureEvent]:
        invalidation_floor = max(lineage.head_fact.recorded_time, correction_recorded_time, cursor.recorded_time)
        invalidation_recorded_time = self._next_recorded_time(invalidation_floor)
        invalidation = FeatureFactInvalidated(
            scope=lineage.head_fact.scope,
            invalidated_fact_ref=lineage.head_fact.ref,
            invalidation_cause="swing_invalidated",
            window_start=lineage.head_fact.window_start,
            window_end=lineage.head_fact.window_end,
            causation_refs=(lineage.head_fact.ref, correction_ref),
            recorded_time=invalidation_recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
            event_contract_ref=self._invalidation_contract_ref,
            computation_cursor=self._resolve_cursor(cursor),
        )
        lineage.invalidated = True
        lineage.pending_invalidation_ref = invalidation.ref
        lineage.pending_invalidation_recorded_time = invalidation_recorded_time
        events: list[FeatureEvent] = [invalidation]

        candle = self._candle_by_window[key]
        winner = self._select_eligible_swing(candle.scope.window_end, cursor)
        if winner is not None:
            swing_id, state = winner
            events.extend(
                self._emit_replacement_only(
                    key, candle, swing_id, state, invalidation.ref, invalidation_recorded_time, cursor
                )
            )
        return events

    def _reevaluate_all_windows(self, cursor: EvaluationFrontier) -> list[FeatureEvent]:
        """P3-FEATURE-A-MAJ-04: re-evaluate EVERY window with a lineage
        entry — both `PENDING_CORRECTION` windows AND windows that already
        settled `VALID` on an alternate (lower-priority) eligible Swing —
        now that a new Swing revision (`cursor`) is visible. Bounded scope:
        only windows that already have a lineage entry (an existing prior
        computation); never a retroactive scan of Candle windows that never
        had any lineage at all.
        """
        events: list[FeatureEvent] = []
        for key, lineage in list(self._lineage.items()):
            candle = self._candle_by_window.get(key)
            if candle is None:
                continue
            winner = self._select_eligible_swing(candle.scope.window_end, cursor)

            if lineage.invalidated:
                if winner is None:
                    continue  # still PENDING_CORRECTION — no eligible Swing yet
                assert lineage.pending_invalidation_ref is not None
                assert lineage.pending_invalidation_recorded_time is not None
                swing_id, state = winner
                events.extend(
                    self._emit_replacement_only(
                        key,
                        candle,
                        swing_id,
                        state,
                        lineage.pending_invalidation_ref,
                        lineage.pending_invalidation_recorded_time,
                        cursor,
                    )
                )
                continue

            if winner is None or winner[1].ref == lineage.used_swing_ref:
                continue  # still the best available (or nothing better) — no repaint
            swing_id, state = winner
            events.extend(self._preempt_settled_window(key, candle, swing_id, state, lineage, cursor))
        return events

    def _preempt_settled_window(
        self,
        key: tuple[datetime, datetime],
        candle: CandleFact,
        swing_id: str,
        state: _SwingState,
        existing: _WindowLineage,
        cursor: EvaluationFrontier,
    ) -> list[FeatureEvent]:
        """A window already `VALID` using a lower-priority alternate Swing
        (the classic A -> invalidate -> B(temporary) sequence) is preempted
        once a corrected/higher-priority Swing revision (`state`) now wins
        the deterministic total order — invalidate-and-replace, never a
        silent in-place swap (feature.md §3 "no shortcut").

        Reaching this function at all already proves ADR-034 condition (d)
        (the Swing fact `existing` actually used remains valid and non-
        invalidated at `R_later`): `_reevaluate_all_windows` only calls this
        function when `lineage.invalidated is False`, and that flag is set
        exactly once, precisely when the used Swing IS invalidated (routing
        instead through `_invalidate_and_reattempt`) — the two paths are
        mutually exclusive by construction.

        P3-FEATURE-A-MAJ-04/ADR-034 (Approved): the winning Swing was never
        itself invalidated (`swing_invalidated` would misrepresent this), so
        the invalidation of the existing, still-VALID Feature fact is caused
        by the *newly-visible-and-winning* SwingConfirmed superseding the
        Swing the existing fact was selected under —
        `eligible_swing_selection_superseded`, and ONLY when ADR-034's own
        visibility relation is provable from durable computation_cursor
        evidence: the new winner must NOT have been full-cursor-visible
        (feature.md §12(a)) at the existing fact's own R_original — read
        directly off that fact's own persisted `computation_cursor`, never
        from process-local state. If it WAS already visible then, the
        original computation itself was wrong — an integrity/computation
        defect, never laundered through this cause (P3-FEATURE-A-MAJ-06
        `EligibleSwingComputationDefectError`).
        """
        original_cursor = existing.head_fact.computation_cursor
        if is_visible_at_cursor(
            state.ref,
            state.recorded_time,
            included_streams=self._resolved_input_contract.included_streams,
            stream_positions=original_cursor.stream_positions,
            cursor_recorded_time=original_cursor.recorded_time,
        ):
            raise EligibleSwingComputationDefectError(
                f"candidate swing {state.ref!r} was already full-cursor-visible at the existing fact's own "
                f"R_original ({original_cursor!r}) but was not selected by the original computation for "
                f"window {key!r} — this is a computation/integrity defect, never representable as "
                "eligible_swing_selection_superseded"
            )
        invalidation_floor = max(existing.head_fact.recorded_time, state.recorded_time, cursor.recorded_time)
        invalidation_recorded_time = self._next_recorded_time(invalidation_floor)
        invalidation = FeatureFactInvalidated(
            scope=existing.head_fact.scope,
            invalidated_fact_ref=existing.head_fact.ref,
            invalidation_cause="eligible_swing_selection_superseded",
            window_start=existing.head_fact.window_start,
            window_end=existing.head_fact.window_end,
            causation_refs=(existing.head_fact.ref, state.ref),
            recorded_time=invalidation_recorded_time,
            ref=self._allocator.next_ref(self._stream_id),
            event_contract_ref=self._invalidation_contract_ref,
            computation_cursor=self._resolve_cursor(cursor),
        )
        events: list[FeatureEvent] = [invalidation]
        events.extend(
            self._emit_replacement_only(
                key, candle, swing_id, state, invalidation.ref, invalidation_recorded_time, cursor
            )
        )
        return events
