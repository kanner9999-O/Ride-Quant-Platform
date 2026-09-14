"""ADR-043 — per-`feature_subject_id` authoritative ownership/coordinator
runtime (Approved `docs/adr/ADR-043.md`, `v0.2`; design mapped onto this
module by `README.md`'s "ADR-043 — Per-subject authoritative ownership
implementation design" section, corrections 001-003).

This module owns exactly the ownership/fencing/commit/catch-up/arbitration
CONCERNS `ADR-043` requires — it never redefines Feature domain semantics
(those stay in `contracts.py`/`regime_passthrough.py`/`swing_distance.py`,
unchanged). The three external boundaries this module defines as `Protocol`s
(`SubjectOwnershipAuthority`, `FencedFeatureCommitter`,
`AuthoritativeLineageHistoryProvider`) are semantic contracts only — this
repository still has no real durable event log, distributed fencing store,
broker, RPC, or production deployment topology, and this module does not
fake one. `tests/` supplies deterministic in-memory fakes, each explicitly
labeled NOT sufficient for production-authoritative cross-process use.

Never exported via `feature_engine.__init__` — module-internal machinery,
consumed directly (`from feature_engine.ownership import ...`) by whichever
caller/orchestrator wires an authoritative runtime together; no current
repository code constructs an `AuthoritativeSubjectOwner` in production.
"""

from __future__ import annotations

import enum
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

from .contracts import (
    EvaluationFrontier,
    FeatureEvent,
    InputMergePolicy,
    PreparedTransition,
)
from .envelope import EventRecordRef
from .errors import (
    CanonicalHistoryMismatchError,
    DualOwnershipError,
    IncompleteCertifiedFrontierError,
    NonMonotonicApplicationOrderError,
    OwnershipAuthorityUnavailableError,
    StaleOwnershipGenerationError,
    UnprovenCatchUpError,
    UnsupportedMergePolicyError,
)

# ADR043-IMPLDESIGN-A-MAJ-04: the only merge_policy shape p_run_sort actually
# implements. ownership.py NEVER treats this as ordering authority by
# itself -- the authority it consumes on every call is always the caller's
# own resolved `VerifiedInputContractAuthority.merge_policy` (contracts.py/
# authority_resolver.py); this constant only bounds what p_run_sort is
# capable of executing, mirroring authority_resolver.py's own validation-
# only capability constants.
_SUPPORTED_MERGE_ALGORITHM = "deterministic-causal-topological-order"
_SUPPORTED_CONCURRENT_TIE_BREAK: tuple[str, ...] = ("stream_id", "sequence")


class SubjectOwnershipState(enum.Enum):
    """ADR-043 §H handoff lifecycle — smallest sufficient state machine, one
    instance per `(feature_subject_id, ownership_generation)`.
    """

    INACTIVE = "INACTIVE"
    CATCHING_UP = "CATCHING_UP"
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"


@dataclass(frozen=True, slots=True)
class OwnerHandle:
    """Immutable local view of one `(feature_subject_id, ownership_
    generation)` pair's own lifecycle state. `ownership_generation` is pure
    execution-control metadata (ADR-043 semantic 6) — never put into
    Feature Event Schema/domain facts.
    """

    feature_subject_id: str
    ownership_generation: int
    state: SubjectOwnershipState


class SubjectOwnershipAuthority(Protocol):
    """External, durable, exclusivity-proving fencing boundary (ADR-043 §B).
    No technology is selected by this design — no production, durable
    implementation is provided here; `tests/` inject a deterministic
    in-memory fake explicitly labeled NOT sufficient for production-
    authoritative cross-process ownership.
    """

    def acquire(self, feature_subject_id: str) -> int:
        """Atomically mints and returns a new, strictly-increasing
        `ownership_generation` for `feature_subject_id`, fencing/revoking
        any previously active generation FIRST (revoke-before-successor;
        no dual-active generations ever exist). Raises
        `DualOwnershipError`/`OwnershipAuthorityUnavailableError` on
        failure — never returns a generation without genuine, proven
        exclusivity.
        """
        ...

    def is_current(self, feature_subject_id: str, ownership_generation: int) -> bool:
        """A fast, EARLY-FAILURE check only — never the sole gate before a
        commit. The real, indivisible verify-at-commit-time gate is
        `FencedFeatureCommitter.commit` itself (ADR043-IMPLDESIGN-A-MAJ-01);
        a caller must never treat a `True` result here as sufficient proof
        that a subsequent, separate write is still safe.
        """
        ...

    def revoke(self, feature_subject_id: str, ownership_generation: int) -> None:
        """Explicitly fences `ownership_generation` for an orderly handoff
        — the same fencing `acquire` already performs internally before
        minting a successor, exposed directly for `AuthoritativeSubjectOwner.
        revoke`.
        """
        ...


@dataclass(slots=True)
class SubjectOwnershipRegistry:
    """Process-local coordinator cache/state-machine view ONLY (ADR-043
    §A/§B) — reflects what THIS process believes `SubjectOwnershipAuthority`
    most recently granted. NEVER itself authoritative exclusivity proof;
    every genuine fencing decision goes through `SubjectOwnershipAuthority`/
    `FencedFeatureCommitter` instead. Purely local bookkeeping — this type
    performs no I/O of any kind.
    """

    _handles: dict[str, OwnerHandle] = field(default_factory=dict)

    def get(self, feature_subject_id: str) -> OwnerHandle | None:
        return self._handles.get(feature_subject_id)

    def set(self, handle: OwnerHandle) -> None:
        self._handles[handle.feature_subject_id] = handle


class FencedFeatureCommitter(Protocol):
    """ADR-043's single indivisible authoritative-commit boundary
    (ADR043-IMPLDESIGN-A-MAJ-01): verify `ownership_generation` is still
    current for `feature_subject_id` + allocate `stream_id` sequence(s) +
    append/commit event(s), as ONE operation — never a separate `validate()`
    then `append()` with a gap between them. Batch-capable: a whole prepared
    batch (e.g. invalidate-then-replace) either fully commits or has zero
    effect. No production, durable implementation is provided by this
    design; `tests/` inject a deterministic in-memory fake.
    """

    def commit(
        self,
        *,
        feature_subject_id: str,
        ownership_generation: int,
        stream_id: str,
        prepared: PreparedTransition,
    ) -> tuple[FeatureEvent, ...]:
        """Raises `StaleOwnershipGenerationError` if `ownership_generation`
        is no longer current for `feature_subject_id` — the WHOLE prepared
        batch has zero effect (no sequence consumed, no event appended, no
        sequence gap). Never mutates the caller's own engine `_lineage`;
        the caller applies that separately via `PreparedTransition.
        apply_to_lineage`, and only after this call returns successfully.
        """
        ...


@dataclass(frozen=True, slots=True)
class UpstreamEnvelope:
    """One certified upstream input event to apply in `P_run` order
    (ADR-043 §D) — during catch-up (§C) or ongoing processing. `fact` is
    the concrete, engine-specific upstream fact object (e.g. a `CandleFact`/
    `SwingConfirmedFact`/`SwingInvalidatedFact`/`RegimeClassifiedFact`/
    `RegimeFactInvalidatedFact`) — `AuthoritativeSubjectOwner` never
    inspects its content, only ever passes it to the wrapped engine's own
    `prepare_upstream_event`, dispatched by `kind`.

    `frontier` is the certified `EvaluationFrontier` valid for evaluating
    THIS event: for ongoing processing every envelope in one apply-set
    batch typically shares the SAME certified frontier the coordinator just
    obtained (§D step 1); for catch-up replay, each envelope carries its
    own point-in-time frontier so reconstruction re-derives the SAME
    eligibility decisions history actually made — never all pinned at the
    final catch-up frontier, which could pick a different winner than
    history did.
    """

    ref: EventRecordRef
    recorded_time: datetime
    causation_refs: tuple[EventRecordRef, ...]
    kind: str
    fact: object
    frontier: EvaluationFrontier


@dataclass(frozen=True, slots=True)
class UpstreamHistoryResult:
    """Result of an `AuthoritativeLineageHistoryProvider` upstream-history
    query. `proven_empty=True` is the ONLY way an empty `events` tuple is
    ever legitimate — a provider that cannot positively prove "no
    applicable upstream history exists" must raise instead of returning an
    ambiguous empty result (README §C: absence of provider != empty
    history; unavailable provider != empty history).
    """

    events: tuple[UpstreamEnvelope, ...]
    proven_empty: bool


@dataclass(frozen=True, slots=True)
class CanonicalOutputHistoryResult:
    """Result of an `AuthoritativeLineageHistoryProvider` canonical-Feature-
    output-history query — same `proven_empty` discipline as
    `UpstreamHistoryResult`.
    """

    events: tuple[FeatureEvent, ...]
    proven_empty: bool


class AuthoritativeLineageHistoryProvider(Protocol):
    """External read/reconstruction boundary onto already-authoritative
    histories (README §C/§D2) — NEVER an alternate source of truth; it
    reconstructs from what is already authoritative, it does not decide
    what is authoritative. No concrete, persistent production adapter is
    provided by this design; `tests/` inject a deterministic in-memory
    fake.
    """

    def upstream_history(self, feature_subject_id: str, *, up_to: EvaluationFrontier) -> UpstreamHistoryResult:
        """Certified upstream input history for `feature_subject_id`, up to
        `up_to`, in arrival order (NOT yet `P_run`-sorted —
        `AuthoritativeSubjectOwner` performs that itself, §D). Used for
        catch-up replay (§C).
        """
        ...

    def canonical_output_history(
        self, feature_subject_id: str, *, up_to: EvaluationFrontier
    ) -> CanonicalOutputHistoryResult:
        """Canonical, already-committed `FeatureComputed`/
        `FeatureFactInvalidated` history for `feature_subject_id`, up to
        `up_to`, in commit order. Used to reconcile catch-up's recomputed
        candidates (§C) — never used to invent new authoritative output.
        """
        ...

    def not_yet_applied_apply_set(
        self,
        feature_subject_id: str,
        *,
        frontier: EvaluationFrontier,
        applied_frontier: EvaluationFrontier | None,
    ) -> UpstreamHistoryResult:
        """The certified, not-yet-applied upstream apply-set for
        `feature_subject_id` visible within `frontier` (ongoing operation,
        §D) — everything already applied up to `applied_frontier` (`None`
        for a freshly activated owner) excluded.
        """
        ...


class OwnedFeatureEngine(Protocol):
    """The minimal surface `AuthoritativeSubjectOwner` needs from a wrapped
    analytical engine — satisfied by both `RegimePassthroughFeatureEngine`
    and `SwingDistanceFeatureEngine` via their own `prepare_upstream_event`.
    """

    def prepare_upstream_event(
        self, envelope: UpstreamEnvelope, *, cursor: EvaluationFrontier
    ) -> list[PreparedTransition]:
        """Dispatches `envelope` (by `envelope.kind`) to this engine's own
        specific `prepare_*` validation/candidate-construction method,
        returning zero, one, or several independent `PreparedTransition`
        batches (one engine call may fan out across several windows, e.g. a
        Swing revision resolving/preempting more than one window) — never
        allocating a Feature ref or mutating `_lineage` itself.
        """
        ...


def _tie_break_key(envelope: UpstreamEnvelope, fields: tuple[str, ...]) -> tuple[str | int, ...]:
    key: list[str | int] = []
    for field_name in fields:
        if field_name == "stream_id":
            key.append(envelope.ref.stream_id)
        elif field_name == "sequence":
            key.append(envelope.ref.sequence)
        else:
            raise UnsupportedMergePolicyError(f"p_run_sort does not implement tie-break field {field_name!r}")
    key.append(envelope.ref.event_id)
    return tuple(key)


def p_run_sort(envelopes: Sequence[UpstreamEnvelope], *, merge_policy: InputMergePolicy) -> list[UpstreamEnvelope]:
    """Chapter 8 §8.3.4 `P_run`: deterministically topologically sorts
    `envelopes` — one certified, RUN-LOCAL, bounded apply set — under
    `P_stream` (same-stream sequence order) UNION `P_causation` (`causation_
    refs` edges to OTHER envelopes within this same set; a `causation_ref`
    pointing outside this set is treated as already-authoritative/committed,
    hence trivially already-satisfied), tie-broken ONLY between envelopes
    related by neither, using the resolved `merge_policy.concurrent_tie_
    break` (ADR043-IMPLDESIGN-A-MAJ-02/-04). Never a claim about ordering
    relative to events outside this bounded set — `P_run` is run-local,
    never a cross-stream global order (Chapter 8 §8.3.3).

    Fails closed (`NonMonotonicApplicationOrderError`) on a genuine cycle/
    contradictory ordering. Fails closed (`UnsupportedMergePolicyError`) if
    `merge_policy` is not the one algorithm/tie-break combination this
    function actually implements — the SAME resolved `merge_policy` value
    every caller must obtain from `VerifiedInputContractAuthority.
    merge_policy`, never a value this function or its caller hard-codes.
    """
    if merge_policy.algorithm != _SUPPORTED_MERGE_ALGORITHM:
        raise UnsupportedMergePolicyError(
            f"p_run_sort does not implement merge_policy.algorithm={merge_policy.algorithm!r} (only "
            f"{_SUPPORTED_MERGE_ALGORITHM!r} is implemented)"
        )
    if merge_policy.concurrent_tie_break != _SUPPORTED_CONCURRENT_TIE_BREAK:
        raise UnsupportedMergePolicyError(
            f"p_run_sort does not implement merge_policy.concurrent_tie_break="
            f"{merge_policy.concurrent_tie_break!r} (only {_SUPPORTED_CONCURRENT_TIE_BREAK!r} is implemented)"
        )

    by_ref = {envelope.ref: envelope for envelope in envelopes}
    successors: dict[EventRecordRef, set[EventRecordRef]] = {ref: set() for ref in by_ref}
    indegree: dict[EventRecordRef, int] = dict.fromkeys(by_ref, 0)

    def _add_edge(before: EventRecordRef, after: EventRecordRef) -> None:
        if after not in successors[before]:
            successors[before].add(after)
            indegree[after] += 1

    by_stream: dict[str, list[UpstreamEnvelope]] = {}
    for envelope in envelopes:
        by_stream.setdefault(envelope.ref.stream_id, []).append(envelope)
    for group in by_stream.values():
        ordered_group = sorted(group, key=lambda e: e.ref.sequence)
        for earlier, later in zip(ordered_group, ordered_group[1:], strict=False):
            _add_edge(earlier.ref, later.ref)

    for envelope in envelopes:
        for cause_ref in envelope.causation_refs:
            if cause_ref in by_ref and cause_ref != envelope.ref:
                _add_edge(cause_ref, envelope.ref)

    remaining = set(by_ref)
    remaining_indegree = dict(indegree)
    ordered_refs: list[EventRecordRef] = []
    while remaining:
        ready = [ref for ref in remaining if remaining_indegree[ref] == 0]
        if not ready:
            raise NonMonotonicApplicationOrderError(
                "certified apply set cannot be deterministically ordered: P_stream/P_causation constraints form a "
                f"cycle among {sorted(str(ref) for ref in remaining)!r}"
            )
        ready.sort(key=lambda ref: _tie_break_key(by_ref[ref], merge_policy.concurrent_tie_break))
        chosen = ready[0]
        ordered_refs.append(chosen)
        remaining.discard(chosen)
        for successor in successors[chosen]:
            remaining_indegree[successor] -= 1
    return [by_ref[ref] for ref in ordered_refs]


class AuthoritativeSubjectOwner:
    """ADR-043's per-subject authoritative coordinator (README "Chosen
    shape"/§9) — owns exactly one `feature_subject_id`, wraps exactly one
    analytical engine instance, and is the ONLY thing authorized to drive
    that engine's authoritative (live-append) path. Different subjects are
    owned by fully independent `AuthoritativeSubjectOwner` instances with no
    shared state (ADR-043 semantic 1).
    """

    def __init__(
        self,
        *,
        feature_subject_id: str,
        engine: OwnedFeatureEngine,
        authority: SubjectOwnershipAuthority,
        committer: FencedFeatureCommitter,
        history_provider: AuthoritativeLineageHistoryProvider,
        merge_policy: InputMergePolicy,
        stream_id: str = "feature",
    ) -> None:
        self._feature_subject_id = feature_subject_id
        self._engine = engine
        self._authority = authority
        self._committer = committer
        self._history_provider = history_provider
        self._merge_policy = merge_policy
        self._stream_id = stream_id
        self._handle: OwnerHandle | None = None
        self._committed_frontier: EvaluationFrontier | None = None
        self._usable = True

    @property
    def handle(self) -> OwnerHandle | None:
        return self._handle

    @property
    def state(self) -> SubjectOwnershipState:
        return self._handle.state if self._handle is not None else SubjectOwnershipState.INACTIVE

    def acquire_and_activate(self, *, catch_up_frontier: EvaluationFrontier) -> tuple[FeatureEvent, ...]:
        """`INACTIVE -> CATCHING_UP -> ACTIVE` (ADR-043 §H) — acquires a
        fenced generation, then requires successful, matched catch-up
        reconciliation (§C) before ever reaching `ACTIVE`. Fails closed
        (stays out of `ACTIVE`, propagates the raised error) on any
        acquisition or reconciliation failure.
        """
        if self._handle is not None and self._handle.state is SubjectOwnershipState.ACTIVE:
            raise DualOwnershipError(
                f"{self._feature_subject_id!r} already has an ACTIVE local owner generation "
                f"{self._handle.ownership_generation!r} — revoke it before acquiring a new one"
            )
        generation = self._authority.acquire(self._feature_subject_id)
        self._handle = OwnerHandle(self._feature_subject_id, generation, SubjectOwnershipState.CATCHING_UP)
        self._usable = True
        self._committed_frontier = None
        reconciled = self._catch_up(catch_up_frontier)
        self._handle = OwnerHandle(self._feature_subject_id, generation, SubjectOwnershipState.ACTIVE)
        self._committed_frontier = catch_up_frontier
        return reconciled

    def revoke(self) -> None:
        """`ACTIVE -> REVOKED` (ADR-043 §H) — always performed before a new
        acquisition for the same subject may begin its own `CATCHING_UP`.
        """
        if self._handle is None:
            return
        self._authority.revoke(self._feature_subject_id, self._handle.ownership_generation)
        self._handle = OwnerHandle(
            self._feature_subject_id, self._handle.ownership_generation, SubjectOwnershipState.REVOKED
        )
        self._usable = False

    def _catch_up(self, frontier: EvaluationFrontier) -> tuple[FeatureEvent, ...]:
        """ADR-043 §C reconciliation model: replay certified upstream
        history in `P_run` order, reconciling each prepared historical
        candidate against canonical Feature output history in the SAME
        order — never calling the live commit path, never allocating a new
        ref, never inventing `recorded_time`.
        """
        upstream = self._history_provider.upstream_history(self._feature_subject_id, up_to=frontier)
        if not upstream.events and not upstream.proven_empty:
            raise UnprovenCatchUpError(
                f"upstream_history for {self._feature_subject_id!r} returned no events without positively "
                "proving emptiness — catch-up cannot proceed"
            )
        canonical = self._history_provider.canonical_output_history(self._feature_subject_id, up_to=frontier)
        if not canonical.events and not canonical.proven_empty:
            raise UnprovenCatchUpError(
                f"canonical_output_history for {self._feature_subject_id!r} returned no events without "
                "positively proving emptiness — catch-up cannot proceed"
            )

        ordered = p_run_sort(upstream.events, merge_policy=self._merge_policy)
        canonical_events = list(canonical.events)
        cursor = 0
        reconciled: list[FeatureEvent] = []
        for envelope in ordered:
            prepared_list = self._engine.prepare_upstream_event(envelope, cursor=envelope.frontier)
            for prepared in prepared_list:
                batch_size = len(prepared.prepared_events)
                batch = tuple(canonical_events[cursor : cursor + batch_size])
                if len(batch) != batch_size:
                    raise CanonicalHistoryMismatchError(
                        f"canonical output history for {self._feature_subject_id!r} is exhausted before a "
                        "prepared historical batch could be reconciled"
                    )
                prepared.reconcile(batch)
                cursor += batch_size
                reconciled.extend(batch)
        if cursor != len(canonical_events):
            raise CanonicalHistoryMismatchError(
                f"canonical output history for {self._feature_subject_id!r} contains "
                f"{len(canonical_events) - cursor} event(s) not explained by certified upstream replay"
            )
        return tuple(reconciled)

    def process_certified_frontier(self, frontier: EvaluationFrontier) -> tuple[FeatureEvent, ...]:
        """ADR-043 §D ongoing operation: obtain the certified, not-yet-
        applied apply set visible at `frontier`, `P_run`-sort it, and
        prepare + fenced-commit each resulting transition in that order.
        """
        self._require_active()
        apply_set = self._history_provider.not_yet_applied_apply_set(
            self._feature_subject_id, frontier=frontier, applied_frontier=self._committed_frontier
        )
        if not apply_set.events and not apply_set.proven_empty:
            raise IncompleteCertifiedFrontierError(
                f"not_yet_applied_apply_set for {self._feature_subject_id!r} returned no events without "
                "positively proving nothing new is applicable at this frontier"
            )
        ordered = p_run_sort(apply_set.events, merge_policy=self._merge_policy)
        committed: list[FeatureEvent] = []
        for envelope in ordered:
            prepared_list = self._engine.prepare_upstream_event(envelope, cursor=envelope.frontier)
            for prepared in prepared_list:
                committed.extend(self._commit(prepared))
        self._committed_frontier = frontier
        return tuple(committed)

    def _commit(self, prepared: PreparedTransition) -> tuple[FeatureEvent, ...]:
        self._require_active()
        assert self._handle is not None
        if not self._authority.is_current(self._feature_subject_id, self._handle.ownership_generation):
            # Early-failure local check only (SubjectOwnershipAuthority.is_current's
            # own contract) -- the real, indivisible gate is inside committer.commit
            # below; this just avoids an unnecessary attempt when staleness is
            # already locally known.
            self._fence_unusable()
            raise StaleOwnershipGenerationError(
                f"{self._feature_subject_id!r} generation {self._handle.ownership_generation!r} is no longer "
                "current (detected by early local check) — owner fenced, requires catch-up before further "
                "authoritative work"
            )
        try:
            finalized = self._committer.commit(
                feature_subject_id=self._feature_subject_id,
                ownership_generation=self._handle.ownership_generation,
                stream_id=self._stream_id,
                prepared=prepared,
            )
        except Exception:
            # ADR-043 §9: commit outcome uncertain (stale generation, or any
            # other failure) -- never retry blindly; fence this owner
            # unusable and require catch-up/reconstruction from committed
            # history before resuming.
            self._fence_unusable()
            raise
        try:
            prepared.apply_to_lineage(finalized)
        except Exception:
            # Commit succeeded but local cache update failed -- authoritative
            # history already won; fence and require catch-up (ADR-043 §9),
            # never retry/append the same transition blindly.
            self._fence_unusable()
            raise
        return finalized

    def _fence_unusable(self) -> None:
        self._usable = False
        if self._handle is not None:
            self._handle = OwnerHandle(
                self._handle.feature_subject_id, self._handle.ownership_generation, SubjectOwnershipState.REVOKED
            )

    def _require_active(self) -> None:
        if not self._usable or self._handle is None or self._handle.state is not SubjectOwnershipState.ACTIVE:
            current_state = self._handle.state if self._handle is not None else SubjectOwnershipState.INACTIVE
            raise OwnershipAuthorityUnavailableError(
                f"{self._feature_subject_id!r} owner is not currently ACTIVE/usable for authoritative work "
                f"(state={current_state!r}, usable={self._usable!r})"
            )


__all__: list[str] = []
