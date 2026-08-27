"""Shared Feature contracts (feature.md): subject identity, Feature
Definition, canonical policy identifiers, authoritative events, recorded-time
causality boundary, and generic evidence normalization.

Split into its own module so all three computation engines
(`regime_passthrough.py`, `candle_window.py`, `swing_distance.py`) and the
`current_view.py` projection share exactly one definition of each of these
concepts — never redefined per engine.
"""

from __future__ import annotations

import decimal
import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from types import MappingProxyType
from typing import Literal, Protocol

from .envelope import EventContractRef, EventRecordRef
from .errors import (
    CursorRelationalInvariantViolationError,
    EvidenceCardinalityError,
    EvidenceReferenceConflictError,
    InvalidFeatureDefinitionError,
    RegistryContractMismatchError,
    StreamPositionsUniverseMismatchError,
    UnresolvedComputationCursorAuthorityError,
    UnresolvedOutputContractAuthorityError,
)
from .identity import deterministic_id

FeatureType = Literal["volatility_metric", "directional_persistence_metric", "distance_to_last_confirmed_swing"]
UpstreamSource = Literal["candle", "regime"]
SwingDirection = Literal["HIGH", "LOW"]
DistanceRepresentation = Literal["signed", "absolute"]

# feature.md §14's exact, closed upstream-contract-ID vocabulary — no contract ID is
# invented beyond what the Domain Contract itself already enumerates. Feature's own
# output contract IDs are feature.md §3/§4's own `id:` fields, verbatim.
CANDLE_CLOSED_CONTRACT_ID = "candle-closed"
CANDLE_CORRECTED_CONTRACT_ID = "candle-corrected"
SWING_CONFIRMED_CONTRACT_ID = "swing-confirmed"
SWING_INVALIDATED_CONTRACT_ID = "swing-invalidated"
REGIME_CLASSIFIED_CONTRACT_ID = "regime-classified"
REGIME_FACT_INVALIDATED_CONTRACT_ID = "regime-fact-invalidated"
FEATURE_COMPUTED_CONTRACT_ID = "feature-computed"
FEATURE_FACT_INVALIDATED_CONTRACT_ID = "feature-fact-invalidated"

_CANDLE_CONTRACT_IDS = frozenset({CANDLE_CLOSED_CONTRACT_ID, CANDLE_CORRECTED_CONTRACT_ID})
_REGIME_CONTRACT_IDS = frozenset({REGIME_CLASSIFIED_CONTRACT_ID, REGIME_FACT_INVALIDATED_CONTRACT_ID})
_SWING_CONTRACT_IDS = frozenset({SWING_CONFIRMED_CONTRACT_ID, SWING_INVALIDATED_CONTRACT_ID})

# P3-FEATURE-A-MAJ-02 remediation: no fabricated stand-in value (e.g. the
# former `FEATURE_EVENT_CONTRACT_VERSION = "v0"`) is invented for Feature's
# own outbound `event_contract_ref.contract_version` anymore. `stream-
# registry.yaml`/a real Event Contract version authority does not exist yet
# in this repository (Phase 1, not yet authored) — each computation engine
# now requires the caller to inject the genuine, non-empty contract version
# it authorizes at construction time (mirroring how `SequenceAllocator`'s
# `module_id`/`implementation_version`/`run_id` are already caller-supplied,
# never invented) and fails closed
# (`UnresolvedOutputContractAuthorityError`) if none is supplied — see
# `candle_window.py`/`swing_distance.py`/`regime_passthrough.py`.

# feature.md §6 "Giá trị canonical mặc định" — the exact canonical policy
# identifier strings pinned by the Domain Contract itself. Validated
# fail-closed by `FeatureDefinition`; no alias, no second canonical spelling.
INPUT_NORMALIZATION_POLICY = (
    "effective_time_window_start_asc_then_window_end_asc_then_stream_id_asc_then_registry_version_asc_"
    "then_sequence_asc_then_event_id_asc"
)
CURRENT_VIEW_SELECTION_POLICY = (
    "effective_window_end_desc_then_window_start_desc_then_recorded_time_asc_then_stream_id_asc_"
    "then_registry_version_asc_then_sequence_asc_then_event_id_asc"
)
ELIGIBLE_SWING_SELECTION_POLICY = (
    "pivot_effective_time_window_start_desc_then_recorded_time_asc_then_stream_id_asc_"
    "then_registry_version_asc_then_sequence_asc_then_swing_revision_desc_then_swing_id_asc_then_event_id_asc"
)
ELIGIBLE_SWING_EFFECTIVE_CUTOFF_POLICY = "REFERENCE_CANDLE_WINDOW_END_EXCLUSIVE"

# feature.md §6 declares warm_up_policy/missing_input_policy/
# effective_window_policy as free-form strings with NO canonical value
# pinned by the contract (unlike the four policies above) — this module pins
# ONE bounded, documented implementation value for each (module-local
# mechanism choice, not a governance decision), fail-closed on any other.
WARM_UP_POLICY = "require_full_evidence"
MISSING_INPUT_POLICY = "defer_until_resolved"
EFFECTIVE_WINDOW_POLICY = "derive_from_input_evidence"
CORRECTION_POLICY = "always_invalidate_and_replace_no_shortcut"  # feature.md §6 fixed `value:`, not a choice

_REGISTRY_VERSION = "v0"  # bounded stand-in for stream-registry.yaml (Phase 1, does not exist yet)
_OHLC_FIELDS = frozenset({"open", "high", "low", "close"})


def resolve_output_contract_refs(feature_event_contract_version: str) -> tuple[EventContractRef, EventContractRef]:
    """P3-FEATURE-A-MAJ-02 remediation — the single place every computation
    engine resolves its own outbound `(FeatureComputed, FeatureFactInvalidated)`
    `event_contract_ref`s. `feature_event_contract_version` is the exact,
    genuine, immutable contract-version identity the CALLER authorizes for
    this engine's own output (never invented here) — fails closed
    (`UnresolvedOutputContractAuthorityError`) if empty, rather than
    defaulting to a fabricated stand-in.
    """
    if not feature_event_contract_version:
        raise UnresolvedOutputContractAuthorityError(
            "feature_event_contract_version must be a genuine, non-empty contract-version identity — "
            "no stand-in value is invented for Feature's own outbound event_contract_ref (P3-FEATURE-A-MAJ-02)"
        )
    return (
        EventContractRef(FEATURE_COMPUTED_CONTRACT_ID, feature_event_contract_version),
        EventContractRef(FEATURE_FACT_INVALIDATED_CONTRACT_ID, feature_event_contract_version),
    )


@dataclass(frozen=True, slots=True)
class InputContractRef:
    """Chapter 8 §8.3.4 Input Contract identity — `{contract_id, contract_version}`.
    Distinct from `EventContractRef` (Chapter 8 §8.2.5 Event Contract identity):
    Chapter 8 §8.3.1 keeps Stream Registry/Input Contract authority and Event
    Contract authority strictly separate (I-12) — never conflated here.
    """

    contract_id: str
    contract_version: str


@dataclass(frozen=True, slots=True)
class LifecyclePosition:
    """Chapter 8 §8.5 replay-cursor `lifecycle_frontier.position` — `kind` is
    `"genesis"` (no lifecycle event visible yet, Chapter 8 §8.3.5's Genesis
    Registry exception) or `"event"` (resolves to a committed lifecycle event).
    """

    kind: Literal["genesis", "event"]
    sequence: int


@dataclass(frozen=True, slots=True)
class LifecycleFrontier:
    """Chapter 8 §8.5's Dedicated Lifecycle Frontier — `{stream_id, position}`
    on the canonical Lifecycle Stream. Never part of `included_streams` (§8.5's
    own rationale for choosing Dedicated Lifecycle Frontier over folding the
    control stream into every Input Contract) — this module does not redefine
    that design, only carries the value through.
    """

    stream_id: str
    position: LifecyclePosition


def _stream_position(stream_positions: Mapping[str, int], stream_id: str) -> int | None:
    return stream_positions.get(stream_id)


def is_visible_at_cursor(
    ref: EventRecordRef,
    recorded_time: datetime,
    *,
    included_streams: frozenset[str],
    stream_positions: Mapping[str, int],
    cursor_recorded_time: datetime,
) -> bool:
    """feature.md §12(a) — the complete three-branch cursor visibility
    predicate (ADR-035, Approved), applied identically everywhere Feature
    checks whether an upstream event is visible at a computation cursor.
    NEVER a scalar `recorded_time`-only test (the v0.1-v0.3 shortcut §12
    explicitly supersedes). All three branches must hold:

    1. stream-universe membership — `ref.stream_id` is one of the Input
       Contract's own `included_streams` (retirement/Retained-in-Universe
       tracking is out of scope here: current authoritative topology has
       zero retired streams, Genesis-only — Feature does not and must not
       consume `platform-lifecycle` events itself, feature.md §14's closed
       consumption list, so it cannot track retirement independently).
    2. in-stream sequence position — `ref.sequence <= stream_positions[ref.stream_id]`,
       compared ONLY within the same stream (Chapter 8 §8.3.3 — never a
       cross-stream sequence comparison).
    3. recorded-time boundary — `recorded_time <= cursor_recorded_time`
       (Chapter 5 §5.3).
    """
    if ref.stream_id not in included_streams:
        return False
    position = _stream_position(stream_positions, ref.stream_id)
    if position is None or ref.sequence > position:
        return False
    return recorded_time <= cursor_recorded_time


@dataclass(frozen=True, slots=True)
class ComputationCursor:
    """feature.md §12 / ADR-035 (Approved) — the canonical Chapter 8 §8.5
    Replay Cursor NGUYÊN VẸN (applied, never redefined, §18's authority
    boundary): `recorded_time`, `input_contract_ref`, `stream_registry_version`,
    `lifecycle_frontier`, `stream_positions`. Every `FeatureComputed`/
    `FeatureFactInvalidated` pins exactly one of these, captured independently
    at its own evaluation — never inherited/copied from the fact it supersedes
    or the invalidation it replaces (feature.md §3/§4).

    `stream_positions` is captured as an immutable `MappingProxyType` snapshot
    at construction (`resolve_computation_cursor`, below) — a caller mutating
    the source mapping it originally supplied must never retroactively alter
    an already-emitted fact's own durable cursor evidence.
    """

    recorded_time: datetime
    input_contract_ref: InputContractRef
    stream_registry_version: str
    lifecycle_frontier: LifecycleFrontier
    stream_positions: Mapping[str, int]


@dataclass(frozen=True, slots=True)
class StreamPositionProof:
    """The resolved position for one stream PLUS the resolved evidence needed
    to validate Chapter 8 §8.5.2's Position -> Cursor relational invariant
    (`position_event.recorded_time <= cursor.recorded_time`) without this
    engine performing any log read of its own (Review-A residual 4). The
    certifying caller/orchestrator — the one that actually performed
    `feature-context-architecture.md` §4.6's direct-log-read certification —
    supplies both fields; this engine only validates the relation.

    `event_recorded_time` is `None` ONLY when `sequence` denotes that this
    stream has genuinely produced no event yet (i.e. `sequence` equals the
    stream's own Genesis `genesis_position`) — a real, resolved absence, never
    an omitted/forgotten proof for a position that does reference an event.
    """

    sequence: int
    event_recorded_time: datetime | None


@dataclass(frozen=True, slots=True)
class LifecycleFrontierProof:
    """Caller-certified lifecycle frontier PLUS the resolved evidence needed
    to validate Chapter 8 §8.5.2's Lifecycle -> Cursor relational invariant
    (Review-A residual 4). `event_recorded_time` is required and validated
    when `position.kind == "event"`; it MUST be `None` for `kind == "genesis"`
    (Chapter 8 §8.3.5's Genesis carve-out — no lifecycle event exists yet, so
    none may be fabricated as evidence).
    """

    stream_id: str
    position: LifecyclePosition
    event_recorded_time: datetime | None


# Chapter 8 §8.3.5 — the canonical Lifecycle Stream's own stable identity,
# mechanically transcribed from the approved Genesis Stream Registry
# (`docs/architecture/stream-registry.yaml`, `registry_version: v1`,
# `stream_id: platform-lifecycle`, `protected: true`) — never invented.
LIFECYCLE_STREAM_ID = "platform-lifecycle"


@dataclass(frozen=True, slots=True)
class EvaluationFrontier:
    """Caller-certified, PROOF-CARRYING per-trigger computation frontier
    (P3-FEATURE-A-MAJ-06, Review-A residual 4/6).

    Mirrors this module's existing `RecordedTimeSource`/explicit-`cursor`
    doctrine, extended to the complete cursor: this engine NEVER constructs
    `stream_positions`/`lifecycle_frontier` itself (no direct log-read
    capability of its own) — a caller/orchestrator that has actually
    performed `feature-context-architecture.md` §4.6's lifecycle-bracketed,
    registry-pinned direct-log-read certification protocol supplies this
    whole, exactly as it already does for `recorded_time` alone. No silent
    fallback to `trigger_event.recorded_time`/an invented registry
    value/an incomplete Feature-local surrogate exists anywhere this type
    is consumed.

    Unlike the plain-integer `ComputationCursor.stream_positions` a
    `FeatureComputed`/`FeatureFactInvalidated` ultimately persists, THIS
    caller-supplied structure additionally carries the resolved-event-
    recorded-time PROOF needed to validate Chapter 8 §8.5.2's Position/
    Lifecycle -> Cursor relational invariants before authoritative emission
    — a caller-provided integer map alone is not proof. That extra proof is
    implementation-level only; it is deliberately never copied onto the
    persisted `ComputationCursor` schema, which Chapter 8 §8.5.1 already
    closes.
    """

    recorded_time: datetime
    stream_registry_version: str
    lifecycle_frontier: LifecycleFrontierProof
    stream_positions: Mapping[str, StreamPositionProof]

    def plain_stream_positions(self) -> dict[str, int]:
        """The plain `stream_id -> sequence` view used for `is_visible_at_cursor`
        eligibility checks — proof fields are irrelevant to that predicate.
        """
        return {stream_id: proof.sequence for stream_id, proof in self.stream_positions.items()}


FeatureComputationProfile = Literal["distance_to_last_confirmed_swing", "regime"]


@dataclass(frozen=True, slots=True)
class ResolvedInputContract:
    """A caller-supplied CANDIDATE authority unit binding `input_contract_ref`,
    its own claimed `stream_registry_version`, `included_streams`, the exact
    Feature computation profile it applies to, AND claimed content-identity
    proof for both source artifacts — never itself sufficient authority, and
    never itself accepted by any computation engine (Review-A round-4). This
    type exists purely so `authority_resolver.py`'s own internal resolution
    logic has somewhere to hold field values transiently while it works; it
    is not part of any engine's public constructor signature.
    """

    feature_computation_profile: FeatureComputationProfile
    input_contract_ref: InputContractRef
    stream_registry_version: str
    included_streams: frozenset[str]
    input_contract_content_id: str
    stream_registry_content_id: str


# Chapter 8 §8.1.1's "verifiable by content identity" clause: this module's
# own SHA-256-hex-digest identity scheme (`authority_resolver.py` computes
# `hashlib.sha256(artifact_bytes).hexdigest()`) — exactly 64 lowercase hex
# characters. A `VerifiedInputContractAuthority`'s content-identity fields
# must match this shape; this does not, by itself, prove a digest matches
# any SPECIFIC file's bytes (no in-core filesystem access, Review-A round-2
# residual 1's own framing) — it is a secondary sanity check only. The
# actual boundary (Review-A round-5) is that `VerifiedInputContractAuthority`
# has no public constructor at all — see the class docstring below.
_CONTENT_ID_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def _is_well_formed_content_id(value: str) -> bool:
    return bool(_CONTENT_ID_PATTERN.fullmatch(value))


@dataclass(frozen=True, slots=True)
class VerifiedInputContractAuthority:
    """The ONLY type a computation engine actually trusts as its own bound
    Input Contract authority.

    Review-A round-5 residual: an earlier version of this type accepted a
    caller-supplied `_field_binding` field — a deterministic, UNKEYED
    SHA-256 digest over the object's own substantive fields, re-verified in
    `__post_init__` on every construction. That mechanism only ever proved
    internal field-CONSISTENCY, never resolver PROVENANCE: since the hash
    algorithm has no secret and lives in this module's own importable
    source, a normal caller could compute that exact same digest themselves
    and hand it back in as a plain constructor argument, producing an
    instance whose internal check passed despite no actual artifact
    resolution ever having occurred (FIELD-BINDING CHECKSUM != RESOLVER
    PROVENANCE — the same shape-vs-provenance defect one level deeper).
    That field and its check are deleted entirely here rather than replaced
    with a different caller-computable token/hash, which would only move
    the identical defect deeper again.

    Instead, this type's own public constructor is disabled structurally:
    calling `VerifiedInputContractAuthority(...)` — with ANY arguments,
    including a fully genuine-looking field set — always raises `TypeError`
    (`__init__`, below), before any field is ever inspected. This type is
    also never exported through `feature_engine.__init__` — it is not part
    of this package's public surface. The only place an instance is ever
    actually built is `_construct_verified_authority` (module-private,
    below), called exclusively by `_seal_verified_authority` (also
    module-private), which is itself called exclusively by
    `authority_resolver.py`'s filesystem-backed resolver AFTER it has
    genuinely read and cross-validated the real Input Contract/Stream
    Registry artifacts and computed real content-identity digests from
    their actual bytes.

    Every computation engine requests its own bound authority through an
    injected `InputContractAuthorityProvider` (below), never by accepting an
    already-resolved value as a constructor argument — there is no normal,
    supported path by which a caller can invent field values (however
    plausible or well-formed) and obtain an instance any engine will
    accept. `dataclasses.replace()` on a genuine instance is, for the same
    structural reason, also always rejected: `replace()` itself calls this
    type's own (disabled) constructor.

    This is an API/semantic encapsulation boundary, not a defense against
    hostile code with reflection/memory access (Review-A round-5 explicitly
    does not require the latter) — module-private construction is
    sufficient.
    """

    feature_computation_profile: FeatureComputationProfile
    input_contract_ref: InputContractRef
    stream_registry_version: str
    included_streams: frozenset[str]
    input_contract_content_id: str
    stream_registry_content_id: str

    def __init__(self, *_args: object, **_kwargs: object) -> None:
        raise TypeError(
            "VerifiedInputContractAuthority has no public constructor — genuine verified authority is only ever "
            "produced internally by authority_resolver.py, after actual Input Contract/Stream Registry artifact "
            "resolution (Review-A round-5). Obtain authority through an InputContractAuthorityProvider, e.g. "
            "FilesystemInputContractAuthorityResolver().resolve(profile), instead of constructing this type "
            "directly — and note that dataclasses.replace(...) on an existing instance is rejected for the same "
            "reason, since it too calls this constructor."
        )


def _construct_verified_authority(
    *,
    feature_computation_profile: FeatureComputationProfile,
    input_contract_ref: InputContractRef,
    stream_registry_version: str,
    included_streams: frozenset[str],
    input_contract_content_id: str,
    stream_registry_content_id: str,
) -> VerifiedInputContractAuthority:
    """The ONLY place a `VerifiedInputContractAuthority` instance is ever
    actually built (Review-A round-5). Bypasses the type's own disabled
    public `__init__` the same way a frozen dataclass's OWN generated
    `__init__` always does internally (`object.__new__` + `object.
    __setattr__` per field, since frozen instances reject ordinary attribute
    assignment) — this is a standard, well-understood pattern, not a hack.
    Module-private; called exclusively by `_seal_verified_authority`
    immediately below, which performs all actual field validation first.
    """
    instance = object.__new__(VerifiedInputContractAuthority)
    object.__setattr__(instance, "feature_computation_profile", feature_computation_profile)
    object.__setattr__(instance, "input_contract_ref", input_contract_ref)
    object.__setattr__(instance, "stream_registry_version", stream_registry_version)
    object.__setattr__(instance, "included_streams", included_streams)
    object.__setattr__(instance, "input_contract_content_id", input_contract_content_id)
    object.__setattr__(instance, "stream_registry_content_id", stream_registry_content_id)
    return instance


class InputContractAuthorityProvider(Protocol):
    """Every computation engine requests its own bound Input Contract
    authority through this Protocol at construction time — rather than
    accepting an already-resolved value directly, which would let a caller
    "promote" arbitrary, unresolved data into trusted authority merely by
    matching field shape. A provider's `.resolve(profile)` is trusted to
    have ACTUALLY performed genuine artifact resolution for that exact
    profile — the same class of trust this module already places in an
    injected `RecordedTimeSource`/`SequenceAllocator`. The default,
    filesystem-backed implementation (`FilesystemInputContractAuthorityResolver`)
    lives in `authority_resolver.py`, explicitly outside this analytical core.
    """

    def resolve(self, profile: FeatureComputationProfile) -> VerifiedInputContractAuthority: ...


# Chapter 8 §8.5.3 — a `StreamPositionProof.sequence` equal to this value
# denotes "no event committed to this stream yet" (every stream's own
# `genesis_position`, per the Genesis Stream Registry's own topology), the
# only case where `event_recorded_time` proof may legitimately be absent.
# This is a structural Chapter-8 constant, not a copy of any artifact's own
# content — unlike the removed `_KNOWN_STREAM_REGISTRIES`/`_KNOWN_INPUT_
# CONTRACTS` tables, it does not encode any resolvable-artifact-specific
# value and therefore is not itself a duplicated authority surface.
_GENESIS_POSITION = 0


def _seal_verified_authority(
    *,
    feature_computation_profile: FeatureComputationProfile,
    input_contract_ref: InputContractRef,
    stream_registry_version: str,
    included_streams: frozenset[str],
    input_contract_content_id: str,
    stream_registry_content_id: str,
) -> VerifiedInputContractAuthority:
    """The ONLY factory that produces a genuine `VerifiedInputContractAuthority`
    (Review-A round-5) — used exclusively by `authority_resolver.py`'s
    filesystem-backed resolver, immediately after it has read the real
    artifacts, cross-validated Registry <-> Contract semantics, and computed
    genuine content-identity digests from the actual bytes. Deliberately
    private (not exported via `__init__.py`) — no other module constructs
    verified authority.
    """
    if not feature_computation_profile:
        raise UnresolvedComputationCursorAuthorityError("feature_computation_profile must be genuine and non-empty")
    if not input_contract_ref.contract_id or not input_contract_ref.contract_version:
        raise UnresolvedComputationCursorAuthorityError(
            "input_contract_ref must be a genuine, non-empty {contract_id, contract_version} identity"
        )
    if not stream_registry_version:
        raise UnresolvedComputationCursorAuthorityError(
            "stream_registry_version must be a genuine, non-empty registry version identity"
        )
    if not included_streams:
        raise UnresolvedComputationCursorAuthorityError("included_streams must be a genuine, non-empty set")
    if not _is_well_formed_content_id(input_contract_content_id):
        raise UnresolvedComputationCursorAuthorityError(
            f"input_contract_content_id={input_contract_content_id!r} is not a well-formed content-identity "
            "digest (64 lowercase hex characters) — a non-empty but fabricated/arbitrary string is never "
            "sufficient content-identity proof"
        )
    if not _is_well_formed_content_id(stream_registry_content_id):
        raise UnresolvedComputationCursorAuthorityError(
            f"stream_registry_content_id={stream_registry_content_id!r} is not a well-formed content-identity "
            "digest (64 lowercase hex characters) — a non-empty but fabricated/arbitrary string is never "
            "sufficient content-identity proof"
        )
    return _construct_verified_authority(
        feature_computation_profile=feature_computation_profile,
        input_contract_ref=input_contract_ref,
        stream_registry_version=stream_registry_version,
        included_streams=included_streams,
        input_contract_content_id=input_contract_content_id,
        stream_registry_content_id=stream_registry_content_id,
    )


def resolve_computation_cursor(
    frontier: EvaluationFrontier,
    *,
    resolved_input_contract: VerifiedInputContractAuthority,
) -> ComputationCursor:
    """The single place every computation engine assembles its own outbound
    `computation_cursor` from a caller-supplied, proof-carrying
    `EvaluationFrontier` plus this engine's own bound `ResolvedInputContract`
    (P3-FEATURE-A-MAJ-06). Enforces, fail-closed, every Chapter 8 §8.5.2
    relational invariant ADR-035 inherits verbatim — never merely a
    syntactic non-empty check (Review-A residuals 2/4/5/6):

    - **Registry -> Contract**: `frontier.stream_registry_version` must
      exactly equal `resolved_input_contract.stream_registry_version`
      (`RegistryContractMismatchError` otherwise — never silently rebased).
    - **stream_positions universe** (ADR-035's own cardinality clause): the
      supplied `stream_positions` keys must be EXACTLY
      `resolved_input_contract.included_streams` — no missing key, no extra
      key (`StreamPositionsUniverseMismatchError` otherwise).
    - **Position -> Cursor**: every proven `event_recorded_time` in
      `stream_positions` must be `<= frontier.recorded_time`
      (`CursorRelationalInvariantViolationError` otherwise).
    - **Lifecycle -> Cursor** + lifecycle stream identity: `lifecycle_frontier
      .stream_id` must equal the canonical `LIFECYCLE_STREAM_ID`; for
      `kind == "event"`, its proven `event_recorded_time` must be present and
      `<= frontier.recorded_time`; for `kind == "genesis"`, no
      `event_recorded_time` may be supplied at all — Chapter 8 §8.3.5's
      Genesis carve-out is never satisfied by a fabricated lifecycle event
      (`CursorRelationalInvariantViolationError` otherwise).

    `stream_positions` is captured as an immutable snapshot
    (`MappingProxyType`) at this exact point — mutating the caller's own
    source mapping afterward can never retroactively alter the resulting
    `ComputationCursor` (Review-A residual 6).
    """
    if frontier.stream_registry_version != resolved_input_contract.stream_registry_version:
        raise RegistryContractMismatchError(
            f"frontier.stream_registry_version={frontier.stream_registry_version!r} does not match this engine's "
            f"bound Input Contract stream_registry_version={resolved_input_contract.stream_registry_version!r} — "
            "this Input Contract instance is not applicable at the caller's certified frontier (Chapter 8 §8.5 "
            "exact-pin); fails closed rather than silently rebasing the cursor onto a different registry"
        )
    if frozenset(frontier.stream_positions.keys()) != resolved_input_contract.included_streams:
        raise StreamPositionsUniverseMismatchError(
            f"frontier.stream_positions keys {sorted(frontier.stream_positions.keys())!r} do not exactly equal "
            f"the bound Input Contract's own included_streams {sorted(resolved_input_contract.included_streams)!r} "
            "(ADR-035's cardinality clause: no missing stream, no extra stream, never an \"all streams seen\" "
            "fallback)"
        )
    for stream_id, proof in frontier.stream_positions.items():
        if proof.sequence != _GENESIS_POSITION and proof.event_recorded_time is None:
            raise CursorRelationalInvariantViolationError(
                f"stream_positions[{stream_id!r}] references sequence {proof.sequence!r} (not that stream's own "
                f"genesis_position {_GENESIS_POSITION!r}) but supplies no resolved event_recorded_time proof — a "
                "caller-provided integer position alone is not proof (Review-A residual 4)"
            )
        if proof.event_recorded_time is not None and proof.event_recorded_time > frontier.recorded_time:
            raise CursorRelationalInvariantViolationError(
                f"stream_positions[{stream_id!r}] resolves to an event recorded at "
                f"{proof.event_recorded_time!r}, which is AFTER cursor.recorded_time {frontier.recorded_time!r} — "
                "Chapter 8 §8.5.2 Position -> Cursor invariant violated (anti-look-ahead)"
            )
    if frontier.lifecycle_frontier.stream_id != LIFECYCLE_STREAM_ID:
        raise CursorRelationalInvariantViolationError(
            f"lifecycle_frontier.stream_id={frontier.lifecycle_frontier.stream_id!r} is not the canonical "
            f"Lifecycle Stream {LIFECYCLE_STREAM_ID!r} (Chapter 8 §8.3.5)"
        )
    if frontier.lifecycle_frontier.position.kind == "event":
        proof_time = frontier.lifecycle_frontier.event_recorded_time
        if proof_time is None:
            raise CursorRelationalInvariantViolationError(
                "lifecycle_frontier.position.kind == 'event' requires a resolved event_recorded_time proof — "
                "none was supplied"
            )
        if proof_time > frontier.recorded_time:
            raise CursorRelationalInvariantViolationError(
                f"lifecycle_frontier's resolved event recorded_time {proof_time!r} is AFTER "
                f"cursor.recorded_time {frontier.recorded_time!r} — Chapter 8 §8.5.2 Lifecycle -> Cursor "
                "invariant violated"
            )
    elif frontier.lifecycle_frontier.event_recorded_time is not None:
        raise CursorRelationalInvariantViolationError(
            "lifecycle_frontier.position.kind == 'genesis' must not carry a fabricated event_recorded_time — "
            "Chapter 8 §8.3.5's Genesis carve-out means no lifecycle event exists yet to prove"
        )
    stream_positions = MappingProxyType(frontier.plain_stream_positions())
    return ComputationCursor(
        recorded_time=frontier.recorded_time,
        input_contract_ref=resolved_input_contract.input_contract_ref,
        stream_registry_version=frontier.stream_registry_version,
        lifecycle_frontier=LifecycleFrontier(
            stream_id=frontier.lifecycle_frontier.stream_id, position=frontier.lifecycle_frontier.position
        ),
        stream_positions=stream_positions,
    )


@dataclass(frozen=True, slots=True)
class FeatureScope:
    """feature.md's five-field Feature Subject identity. `effective_window`
    is explicitly NOT part of identity — one continuous subject exists per
    this five-field scope.
    """

    instrument_id: str
    venue_id: str
    timeframe: str
    feature_type: FeatureType
    feature_definition_version: str

    @property
    def feature_subject_id(self) -> str:
        return deterministic_id(
            "feature",
            self.instrument_id,
            self.venue_id,
            self.timeframe,
            self.feature_type,
            self.feature_definition_version,
        )


_VALID_ROUNDINGS = frozenset(
    {
        decimal.ROUND_HALF_UP,
        decimal.ROUND_HALF_EVEN,
        decimal.ROUND_HALF_DOWN,
        decimal.ROUND_UP,
        decimal.ROUND_DOWN,
        decimal.ROUND_CEILING,
        decimal.ROUND_FLOOR,
        decimal.ROUND_05UP,
    }
)


@dataclass(frozen=True, slots=True)
class DecimalPrecisionPolicy:
    """feature.md §6 `decimal_precision_policy` — digits + a stdlib
    `decimal` rounding mode (never a hand-invented rounding scheme).
    """

    digits: int
    rounding: str

    def __post_init__(self) -> None:
        if self.digits < 0:
            raise InvalidFeatureDefinitionError(f"digits must be >= 0, got {self.digits!r}")
        if self.rounding not in _VALID_ROUNDINGS:
            raise InvalidFeatureDefinitionError(f"unsupported rounding mode: {self.rounding!r}")

    def apply(self, value: Decimal) -> Decimal:
        quantum = Decimal(1).scaleb(-self.digits)
        return value.quantize(quantum, rounding=self.rounding)


@dataclass(frozen=True, slots=True)
class FeatureDefinition:
    """feature.md §6 — Referenced Authoritative Artifact. One immutable
    definition per `feature_definition_version`, pinning exactly one
    feature_type and its own type-specific fields; contradictory or
    incomplete combinations fail closed at construction.

    Concrete formula/threshold/window-count VALUES are never invented by
    this module — they always come from whichever definition instance the
    caller constructs (feature.md §6's own "không hardcode một trường phái"
    principle, mirrored from swing_definition/structure_definition/
    regime_definition).
    """

    feature_definition_id: str
    feature_definition_version: str
    feature_type: FeatureType
    unit: str
    decimal_precision_policy: DecimalPrecisionPolicy
    warm_up_policy: str
    missing_input_policy: str
    correction_policy: str
    effective_window_policy: str
    current_view_selection_policy: str
    input_normalization_policy: str
    # volatility_metric / directional_persistence_metric only:
    upstream_source: UpstreamSource | None = None
    upstream_contract_refs: tuple[EventContractRef, ...] | None = None
    required_upstream_definition_version: str | None = None
    window_candle_count: int | None = None
    formula_id: str | None = None
    # distance_to_last_confirmed_swing only:
    swing_direction: SwingDirection | None = None
    distance_representation: DistanceRepresentation | None = None
    reference_price_field: str | None = None
    eligible_swing_selection_policy: str | None = None
    eligible_swing_effective_cutoff_policy: str | None = None
    required_swing_definition_version: str | None = None
    normalization_policy: str | None = None

    def __post_init__(self) -> None:
        if not self.feature_definition_id:
            raise InvalidFeatureDefinitionError("feature_definition_id must be non-empty")
        if not self.feature_definition_version:
            raise InvalidFeatureDefinitionError("feature_definition_version must be non-empty")
        if not self.unit:
            raise InvalidFeatureDefinitionError("unit must be non-empty")
        if self.correction_policy != CORRECTION_POLICY:
            raise InvalidFeatureDefinitionError(f"unsupported correction_policy: {self.correction_policy!r}")
        if self.input_normalization_policy != INPUT_NORMALIZATION_POLICY:
            raise InvalidFeatureDefinitionError(
                f"unsupported input_normalization_policy: {self.input_normalization_policy!r}"
            )
        if self.current_view_selection_policy != CURRENT_VIEW_SELECTION_POLICY:
            raise InvalidFeatureDefinitionError(
                f"unsupported current_view_selection_policy: {self.current_view_selection_policy!r}"
            )
        if self.warm_up_policy != WARM_UP_POLICY:
            raise InvalidFeatureDefinitionError(f"unsupported warm_up_policy: {self.warm_up_policy!r}")
        if self.missing_input_policy != MISSING_INPUT_POLICY:
            raise InvalidFeatureDefinitionError(f"unsupported missing_input_policy: {self.missing_input_policy!r}")
        if self.effective_window_policy != EFFECTIVE_WINDOW_POLICY:
            raise InvalidFeatureDefinitionError(
                f"unsupported effective_window_policy: {self.effective_window_policy!r}"
            )

        distance_only_fields = (
            self.swing_direction,
            self.distance_representation,
            self.reference_price_field,
            self.eligible_swing_selection_policy,
            self.eligible_swing_effective_cutoff_policy,
            self.required_swing_definition_version,
        )
        metric_only_fields = (
            self.upstream_source,
            self.upstream_contract_refs,
            self.required_upstream_definition_version,
        )

        if self.feature_type in ("volatility_metric", "directional_persistence_metric"):
            if any(field is not None for field in distance_only_fields) or self.normalization_policy is not None:
                raise InvalidFeatureDefinitionError(
                    f"{self.feature_type} must not set distance_to_last_confirmed_swing-only fields"
                )
            if self.upstream_source is None:
                raise InvalidFeatureDefinitionError("upstream_source is required for this feature_type")
            if not self.upstream_contract_refs:
                raise InvalidFeatureDefinitionError(
                    "upstream_contract_refs is required (non-empty) for volatility_metric/"
                    "directional_persistence_metric (feature.md §6)"
                )
            allowed_contract_ids = _CANDLE_CONTRACT_IDS if self.upstream_source == "candle" else _REGIME_CONTRACT_IDS
            for contract_ref in self.upstream_contract_refs:
                if contract_ref.contract_id not in allowed_contract_ids:
                    raise InvalidFeatureDefinitionError(
                        f"upstream_contract_refs contains contract_id={contract_ref.contract_id!r}, not valid for "
                        f"upstream_source={self.upstream_source!r} (must be one of {sorted(allowed_contract_ids)!r} "
                        "— feature.md §6: 'PHẢI khớp đúng upstream_source đã chọn, không được trộn')"
                    )
            if self.upstream_source == "candle":
                if self.required_upstream_definition_version is not None:
                    raise InvalidFeatureDefinitionError(
                        "required_upstream_definition_version must be None when upstream_source=candle "
                        "(dual upstream source)"
                    )
                if self.window_candle_count is None or self.window_candle_count < 1:
                    raise InvalidFeatureDefinitionError(
                        "window_candle_count (>=1) is required for upstream_source=candle"
                    )
                if not self.formula_id:
                    raise InvalidFeatureDefinitionError("formula_id is required for upstream_source=candle")
            elif self.upstream_source == "regime":
                if self.window_candle_count is not None or self.formula_id is not None:
                    raise InvalidFeatureDefinitionError(
                        "window_candle_count/formula_id must be None when upstream_source=regime (dual upstream source)"
                    )
                if not self.required_upstream_definition_version:
                    raise InvalidFeatureDefinitionError(
                        "required_upstream_definition_version is required for upstream_source=regime"
                    )
            else:
                raise InvalidFeatureDefinitionError(f"unsupported upstream_source: {self.upstream_source!r}")
        elif self.feature_type == "distance_to_last_confirmed_swing":
            if (
                any(field is not None for field in metric_only_fields)
                or self.window_candle_count is not None
                or (self.formula_id is not None)
            ):
                raise InvalidFeatureDefinitionError(
                    "distance_to_last_confirmed_swing must not set volatility/directional_persistence-only fields"
                )
            if self.swing_direction not in ("HIGH", "LOW"):
                raise InvalidFeatureDefinitionError(f"invalid swing_direction: {self.swing_direction!r}")
            if self.distance_representation not in ("signed", "absolute"):
                raise InvalidFeatureDefinitionError(
                    f"invalid distance_representation: {self.distance_representation!r}"
                )
            if self.reference_price_field not in _OHLC_FIELDS:
                raise InvalidFeatureDefinitionError(f"invalid reference_price_field: {self.reference_price_field!r}")
            if self.eligible_swing_selection_policy != ELIGIBLE_SWING_SELECTION_POLICY:
                raise InvalidFeatureDefinitionError(
                    f"unsupported eligible_swing_selection_policy: {self.eligible_swing_selection_policy!r}"
                )
            if self.eligible_swing_effective_cutoff_policy != ELIGIBLE_SWING_EFFECTIVE_CUTOFF_POLICY:
                raise InvalidFeatureDefinitionError(
                    "unsupported eligible_swing_effective_cutoff_policy: "
                    f"{self.eligible_swing_effective_cutoff_policy!r}"
                )
            if not self.required_swing_definition_version:
                raise InvalidFeatureDefinitionError("required_swing_definition_version is required")
        else:
            raise InvalidFeatureDefinitionError(f"unsupported feature_type: {self.feature_type!r}")


@dataclass(frozen=True, slots=True)
class FeatureComputed:
    """feature.md §3 — one completed valid computation point. Emitted for
    EVERY completed valid computation point, even when `value` repeats the
    previous point's — no "no-op if unchanged" shortcut.

    `computation_cursor` (P3-FEATURE-A-MAJ-06, ADR-035 Approved) is REQUIRED
    on every instance, gốc lẫn replacement — captured independently at this
    exact computation, never inherited/copied from the fact it supersedes.
    """

    scope: FeatureScope
    value: Decimal
    unit: str
    window_start: datetime
    window_end: datetime
    input_fact_refs: tuple[EventRecordRef, ...]
    supersedes_fact_ref: EventRecordRef | None
    causation_refs: tuple[EventRecordRef, ...]
    recorded_time: datetime
    ref: EventRecordRef
    event_contract_ref: EventContractRef
    computation_cursor: ComputationCursor


InvalidationCause = Literal[
    "candle_corrected",
    "regime_fact_invalidated",
    "swing_invalidated",
    "eligible_swing_selection_superseded",
]


@dataclass(frozen=True, slots=True)
class FeatureFactInvalidated:
    """feature.md §4 — `scope`/`window_start`/`window_end` are inherited
    byte-for-byte from the invalidated fact, never independently declared.

    `computation_cursor` (P3-FEATURE-A-MAJ-06, ADR-035 Approved) pins
    `R_later` for `eligible_swing_selection_superseded` (ADR-034) — captured
    independently at this invalidation's own evaluation, never copied from
    the fact being invalidated.
    """

    scope: FeatureScope
    invalidated_fact_ref: EventRecordRef
    invalidation_cause: InvalidationCause
    window_start: datetime
    window_end: datetime
    causation_refs: tuple[EventRecordRef, ...]
    recorded_time: datetime
    ref: EventRecordRef
    event_contract_ref: EventContractRef
    computation_cursor: ComputationCursor


FeatureEvent = FeatureComputed | FeatureFactInvalidated


class RecordedTimeSource(Protocol):
    """A bounded, injected knowledge-time provider for Feature events.

    feature.md §3/§4 pin strict recorded_time causality (an original fact's
    recorded_time must be later than its evidence's; an invalidation's must
    be later than both the fact it targets and the causing upstream event; a
    replacement's must be later than its own invalidation) but never
    specifies a concrete clock/allocation mechanism (Chapter 5 §5.4 defers
    that to the owning module) — this engine never fabricates a knowledge
    time itself; it asks the injected provider and independently validates
    `result > strict_floor`, failing closed
    (`RecordedTimeSourceViolationError`) otherwise. A real wall-clock/
    runtime implementation of this Protocol lives outside this analytical
    core.
    """

    def next_after(self, strict_floor: datetime) -> datetime: ...


def normalize_input_facts[T](
    facts: Sequence[T],
    *,
    effective_time: Callable[[T], tuple[datetime, datetime]],
    ref_of: Callable[[T], EventRecordRef],
    expected_count: int,
) -> tuple[EventRecordRef, ...]:
    """feature.md §8a canonical input evidence normalization, generalized
    over any authoritative fact type (Candle/Swing/Regime) via the two
    caller-supplied extraction functions — the 6-criterion lexicographic
    order and dedup/conflict semantics are implemented exactly once here,
    not duplicated per engine.

    Fails closed (`EvidenceReferenceConflictError`) if the same ref resolves
    to materially different fact content (full structural equality on the
    frozen dataclass, never narrowed to a subset of fields). Fails closed
    (`EvidenceCardinalityError`) if, after dedup, the normalized evidence
    does not contain exactly `expected_count` unique refs.
    """
    deduped: dict[EventRecordRef, T] = {}
    for fact in facts:
        ref = ref_of(fact)
        existing = deduped.get(ref)
        if existing is not None and existing != fact:
            raise EvidenceReferenceConflictError(
                f"ref {ref!r} resolves to conflicting fact content ({existing!r} vs {fact!r})"
            )
        deduped[ref] = fact

    def _sort_key(fact: T) -> tuple[datetime, datetime, str, str, int, str]:
        start, end = effective_time(fact)
        ref = ref_of(fact)
        return (start, end, ref.stream_id, _REGISTRY_VERSION, ref.sequence, ref.event_id)

    ordered = sorted(deduped.values(), key=_sort_key)
    if len(ordered) != expected_count:
        raise EvidenceCardinalityError(
            f"normalized evidence has {len(ordered)} unique ref(s), expected exactly {expected_count}"
        )
    return tuple(ref_of(fact) for fact in ordered)
