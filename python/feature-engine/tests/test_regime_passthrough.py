from __future__ import annotations

import dataclasses
import inspect
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

import pytest
from conftest import (
    BASE,
    FEATURE_OUTPUT_CONTRACT_VERSION,
    REGIME_INPUT_CONTRACT,
    SWING_DISTANCE_INPUT_CONTRACT,
    FixedDeltaTimeSource,
    NonCausalTimeSource,
    feature_scope,
    frontier_at,
    make_candle_definition,
    make_distance_definition,
    make_regime_definition,
    only_computed,
    only_invalidated,
    regime_classified_at,
    regime_invalidated_at,
)

from feature_engine import (
    FEATURE_COMPUTED_CONTRACT_ID,
    FEATURE_FACT_INVALIDATED_CONTRACT_ID,
    EvaluationFrontier,
    EventContractRef,
    RecordedTimeSource,
    RegimePassthroughFeatureEngine,
    SequenceAllocator,
    StaticInputContractAuthorityProvider,
)
from feature_engine.contracts import ResolvedInputContract, VerifiedInputContractAuthority, _seal_verified_authority
from feature_engine.errors import (
    DefinitionVersionMismatchError,
    EvidenceReferenceConflictError,
    FeatureLineageError,
    ForeignScopeError,
    InputContractIdentityMismatchError,
    NonMonotonicRecordedTimeError,
    RecordedTimeSourceViolationError,
    RegimeDimensionMismatchError,
    RegistryContractMismatchError,
    UnauthorizedUpstreamContractError,
    UnresolvedComputationCursorAuthorityError,
    UnresolvedOutputContractAuthorityError,
)


@dataclasses.dataclass(frozen=True)
class _FixedAuthorityProvider:
    """TEST-ONLY `InputContractAuthorityProvider` that returns WHATEVER
    object it was constructed with, verbatim, regardless of type — used to
    prove that a genuine computation engine independently rejects a
    provider that hands back unresolved/plain data instead of a real
    `VerifiedInputContractAuthority` (Review-A round-4).
    """

    authority: object

    def resolve(self, profile: object) -> Any:
        return self.authority


def _engine(
    allocator: SequenceAllocator, time_source: RecordedTimeSource, feature_type: str = "volatility_metric"
) -> RegimePassthroughFeatureEngine:
    definition = make_regime_definition(feature_type=feature_type, regime_dimension_version="rgd-1")
    scope = feature_scope(feature_type, version=definition.feature_definition_version)
    return RegimePassthroughFeatureEngine(
        scope,
        definition,
        allocator,
        time_source,
        feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
        input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
    )


def _frontier_at(recorded_time: datetime) -> EvaluationFrontier:
    return frontier_at(recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT)


def _invalid_frontier(recorded_time: datetime) -> EvaluationFrontier:
    """A deliberately malformed `EvaluationFrontier` (wrong `stream_registry_
    version`) used to prove Review-A round-2 residual 2's failure-atomicity
    requirement for this engine too. Built by mutating a VALID frontier's
    own plain field directly — never by mutating `REGIME_INPUT_CONTRACT`
    itself, which (as a `VerifiedInputContractAuthority`) has no public
    constructor at all, so `dataclasses.replace` on it always raises
    `TypeError` (Review-A round-5).
    """
    return dataclasses.replace(_frontier_at(recorded_time), stream_registry_version="not-the-real-registry-version")


# --- P3-FEATURE-A-MAJ-02 remediation: output contract-version authority ------


def test_output_contract_version_must_be_genuine_non_empty(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    definition = make_regime_definition(regime_dimension_version="rgd-1")
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    with pytest.raises(UnresolvedOutputContractAuthorityError):
        RegimePassthroughFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version="",
            input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
        )


# --- 3. Regime volatility pass-through ---------------------------------------


def test_regime_volatility_correct_dimension_and_version_accepted(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    computed = only_computed(
        engine.on_regime_classified(
            fact, cursor=_frontier_at(fact.recorded_time)
        )[0]
    )
    assert computed.value == Decimal("1.50")
    assert computed.input_fact_refs == (fact.ref,)


def test_regime_volatility_wrong_dimension_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator,
        0,
        computed_metric="1.5",
        regime_dimension="directional_persistence",
        regime_definition_version="rgd-1",
    )
    with pytest.raises(RegimeDimensionMismatchError):
        engine.on_regime_classified(fact, cursor=_frontier_at(fact.recorded_time))


def test_regime_volatility_wrong_definition_version_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-2"
    )
    with pytest.raises(DefinitionVersionMismatchError):
        engine.on_regime_classified(fact, cursor=_frontier_at(fact.recorded_time))


# --- P3-FEATURE-A-MAJ-02 remediation: contract qualification -----------------


def test_unauthorized_regime_contract_id_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    bad = dataclasses.replace(fact, event_contract_ref=EventContractRef("regime-current-view", "v1"))
    with pytest.raises(UnauthorizedUpstreamContractError):
        engine.on_regime_classified(bad, cursor=_frontier_at(bad.recorded_time))


# --- P3-FEATURE-A-MAJ-05 remediation: same-ref-different-content fails closed


def test_regime_same_ref_different_content_fails_closed(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    engine.on_regime_classified(fact, cursor=_frontier_at(fact.recorded_time))
    conflicting = dataclasses.replace(fact, computed_metric=Decimal("9.9"))
    with pytest.raises(EvidenceReferenceConflictError):
        engine.on_regime_classified(conflicting, cursor=_frontier_at(conflicting.recorded_time))


# --- 4. Directional persistence pass-through --------------------------------


def test_directional_persistence_continuous_value_no_reinterpretation(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source, feature_type="directional_persistence_metric")
    fact = regime_classified_at(
        allocator,
        0,
        computed_metric="0.42",
        regime_dimension="directional_persistence",
        regime_definition_version="rgd-1",
    )
    computed = only_computed(
        engine.on_regime_classified(
            fact, cursor=_frontier_at(fact.recorded_time)
        )[0]
    )
    assert computed.value == Decimal("0.42")
    field_names = {f.name for f in dataclasses.fields(computed)}
    assert not field_names & {"direction", "label", "orientation", "class_label"}


# --- 13. Dedup ---------------------------------------------------------------


def test_dedup_identical_computation_identity_emits_once(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    assert len(engine.on_regime_classified(fact, cursor=_frontier_at(fact.recorded_time))) == 1
    assert engine.on_regime_classified(fact, cursor=_frontier_at(fact.recorded_time)) == []


def test_same_value_different_windows_emits_separately(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact0 = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    fact1 = regime_classified_at(
        allocator, 1, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    computed0 = only_computed(
        engine.on_regime_classified(
            fact0, cursor=_frontier_at(fact0.recorded_time)
        )[0]
    )
    computed1 = only_computed(
        engine.on_regime_classified(
            fact1, cursor=_frontier_at(fact1.recorded_time)
        )[0]
    )
    assert computed0.ref != computed1.ref
    assert computed0.window_start != computed1.window_start


# --- 14. Correction: no shortcut ----------------------------------------------


def test_correction_invalidate_and_replace_even_when_value_unchanged(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    # P3-PY-MUT-STEP9-A field-completeness remediation (EVID-03,
    # constructed_object_field_not_independently_asserted): this scenario
    # already exercises _emit_original, _emit_invalidation, and
    # _emit_replacement in one disciplined original -> invalidate ->
    # replace sequence -- every constructor-set field of all three emitted
    # events is now independently asserted against its authoritative
    # expected value below, not just `.value`/`.ref`/`.supersedes_fact_ref`
    # as before.
    engine = _engine(allocator, time_source)
    original_input = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    original = only_computed(
        engine.on_regime_classified(
            original_input, cursor=_frontier_at(original_input.recorded_time)
        )[0]
    )
    assert original.scope == engine.scope
    assert original.unit == engine.definition.unit
    assert original.window_end == original_input.recorded_time
    assert original.causation_refs == original.input_fact_refs
    assert original.ref.stream_id == "feature"
    assert original.event_contract_ref == EventContractRef(
        FEATURE_COMPUTED_CONTRACT_ID, FEATURE_OUTPUT_CONTRACT_VERSION
    )

    invalidation_input = regime_invalidated_at(
        allocator, invalidated_fact_ref=original_input.ref, recorded_time=original.recorded_time + timedelta(minutes=5)
    )
    invalidation = only_invalidated(
        engine.on_regime_invalidated(
            invalidation_input, cursor=_frontier_at(invalidation_input.recorded_time)
        )[0]
    )
    assert invalidation.invalidated_fact_ref == original.ref
    assert invalidation.scope == engine.scope
    assert invalidation.invalidation_cause == "regime_fact_invalidated"
    assert invalidation.window_start == original.window_start
    assert invalidation.window_end == original.window_end
    assert invalidation.causation_refs == (original.ref, invalidation_input.ref)
    assert invalidation.ref.stream_id == "feature"
    assert invalidation.event_contract_ref == EventContractRef(
        FEATURE_FACT_INVALIDATED_CONTRACT_ID, FEATURE_OUTPUT_CONTRACT_VERSION
    )

    replacement_input = regime_classified_at(
        allocator,
        0,
        computed_metric="1.5",
        regime_dimension="volatility",
        regime_definition_version="rgd-1",
        recorded_offset_seconds=600,
    )
    replacement = only_computed(
        engine.on_regime_classified(
            replacement_input, cursor=_frontier_at(replacement_input.recorded_time)
        )[0]
    )
    assert replacement.value == original.value == Decimal("1.50")
    assert replacement.supersedes_fact_ref == original.ref
    assert replacement.ref != original.ref
    assert replacement.scope == engine.scope
    assert replacement.unit == engine.definition.unit
    assert replacement.window_start == original.window_start
    assert replacement.window_end == original.window_end
    assert replacement.input_fact_refs == (replacement_input.ref,)
    assert replacement.causation_refs == (*replacement.input_fact_refs, invalidation.ref)
    assert replacement.ref.stream_id == "feature"
    assert replacement.event_contract_ref == EventContractRef(
        FEATURE_COMPUTED_CONTRACT_ID, FEATURE_OUTPUT_CONTRACT_VERSION
    )
    assert replacement.computation_cursor.recorded_time == replacement_input.recorded_time


def test_causal_chain_original_lt_invalidation_lt_replacement(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    original_input = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    original = only_computed(
        engine.on_regime_classified(
            original_input, cursor=_frontier_at(original_input.recorded_time)
        )[0]
    )
    invalidation_input = regime_invalidated_at(
        allocator, invalidated_fact_ref=original_input.ref, recorded_time=original.recorded_time + timedelta(minutes=5)
    )
    invalidation = only_invalidated(
        engine.on_regime_invalidated(
            invalidation_input, cursor=_frontier_at(invalidation_input.recorded_time)
        )[0]
    )
    replacement_input = regime_classified_at(
        allocator,
        0,
        computed_metric="1.5",
        regime_dimension="volatility",
        regime_definition_version="rgd-1",
        recorded_offset_seconds=600,
    )
    replacement = only_computed(
        engine.on_regime_classified(
            replacement_input, cursor=_frontier_at(replacement_input.recorded_time)
        )[0]
    )
    assert original.recorded_time < invalidation.recorded_time < replacement.recorded_time


# --- 15. Lineage: no fork, no skip -------------------------------------------


def test_lineage_no_skip_replacement_without_invalidation_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    original_input = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    engine.on_regime_classified(original_input, cursor=_frontier_at(original_input.recorded_time))
    different_input = regime_classified_at(
        allocator, 0, computed_metric="2.0", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    with pytest.raises(FeatureLineageError):
        engine.on_regime_classified(different_input, cursor=_frontier_at(different_input.recorded_time))


def test_lineage_no_fork_double_invalidation_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    original_input = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    original = only_computed(
        engine.on_regime_classified(
            original_input, cursor=_frontier_at(original_input.recorded_time)
        )[0]
    )
    invalidation_input = regime_invalidated_at(
        allocator, invalidated_fact_ref=original_input.ref, recorded_time=original.recorded_time + timedelta(minutes=5)
    )
    engine.on_regime_invalidated(invalidation_input, cursor=_frontier_at(invalidation_input.recorded_time))
    replacement_input = regime_classified_at(
        allocator,
        0,
        computed_metric="1.5",
        regime_dimension="volatility",
        regime_definition_version="rgd-1",
        recorded_offset_seconds=600,
    )
    engine.on_regime_classified(replacement_input, cursor=_frontier_at(replacement_input.recorded_time))

    # Targeting the now-superseded original ref again must fail — lineage head has moved on.
    stale_invalidation = regime_invalidated_at(
        allocator, invalidated_fact_ref=original_input.ref, recorded_time=original.recorded_time + timedelta(minutes=10)
    )
    with pytest.raises(FeatureLineageError):
        engine.on_regime_invalidated(stale_invalidation, cursor=_frontier_at(stale_invalidation.recorded_time))


# --- 16. Causal ordering ------------------------------------------------------


def test_invalidation_before_original_rejected(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    bogus_ref = allocator.next_ref("regime")
    invalidation_input = regime_invalidated_at(allocator, invalidated_fact_ref=bogus_ref, recorded_time=BASE)
    with pytest.raises(FeatureLineageError):
        engine.on_regime_invalidated(invalidation_input, cursor=_frontier_at(invalidation_input.recorded_time))


# --- P3-FEATURE-A-MAJ-06 remediation: durable computation_cursor -------------


def test_feature_computed_and_invalidated_carry_full_computation_cursor(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    r = fact.recorded_time + timedelta(hours=1)
    computed = only_computed(engine.on_regime_classified(fact, cursor=_frontier_at(r))[0])
    cursor = computed.computation_cursor
    assert cursor.recorded_time == r
    assert cursor.recorded_time != fact.recorded_time  # never a fallback to the trigger event's own recorded_time
    assert cursor.input_contract_ref == REGIME_INPUT_CONTRACT.input_contract_ref
    assert cursor.stream_registry_version == REGIME_INPUT_CONTRACT.stream_registry_version

    invalidation_input = regime_invalidated_at(
        allocator, invalidated_fact_ref=fact.ref, recorded_time=computed.recorded_time + timedelta(minutes=5)
    )
    r_later = invalidation_input.recorded_time + timedelta(hours=1)
    invalidation = only_invalidated(
        engine.on_regime_invalidated(invalidation_input, cursor=_frontier_at(r_later))[0]
    )
    assert invalidation.computation_cursor.recorded_time == r_later
    assert invalidation.computation_cursor != computed.computation_cursor


# --- Review-A round-2 residual 2: failure atomicity -------------------------


def test_regime_classified_retry_after_invalid_frontier_is_deterministic(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Submitting a RegimeClassified first with an invalid frontier must fail
    WITHOUT entering lineage/dedup state — the exact same fact retried with a
    valid frontier is treated as a genuine first-time ingestion, identical to
    a clean engine that only ever saw the valid attempt.
    """
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )

    with pytest.raises(RegistryContractMismatchError):
        engine.on_regime_classified(fact, cursor=_invalid_frontier(fact.recorded_time))
    assert engine._lineage == {}  # rejected attempt did not enter lineage state

    computed = only_computed(engine.on_regime_classified(fact, cursor=_frontier_at(fact.recorded_time))[0])
    assert computed.value == Decimal("1.50")

    clean_allocator = SequenceAllocator(module_id="feature-engine", implementation_version="0.1.0", run_id="test-run")
    clean_engine = _engine(clean_allocator, FixedDeltaTimeSource())
    c_fact = regime_classified_at(
        clean_allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    clean_computed = only_computed(
        clean_engine.on_regime_classified(c_fact, cursor=_frontier_at(c_fact.recorded_time))[0]
    )

    assert computed == clean_computed


def test_unverified_plain_authority_cannot_be_supplied_to_regime_engine_as_if_verified(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Negative test 6: a hand-built `ResolvedInputContract` — NOT the
    verified type, never produced by any resolver — wrapped in a provider
    that hands it back verbatim, must never be accepted by
    `RegimePassthroughFeatureEngine` as though it were genuine, resolver-
    issued authority. The engine itself independently rejects a provider
    that returns anything other than a genuine `VerifiedInputContractAuthority`.
    """
    unverified = ResolvedInputContract(
        feature_computation_profile="regime",
        input_contract_ref=REGIME_INPUT_CONTRACT.input_contract_ref,
        stream_registry_version=REGIME_INPUT_CONTRACT.stream_registry_version,
        included_streams=REGIME_INPUT_CONTRACT.included_streams,
        input_contract_content_id="unverified-hand-built-guess",
        stream_registry_content_id="unverified-hand-built-guess",
    )
    definition = make_regime_definition(regime_dimension_version="rgd-1")
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        RegimePassthroughFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
            input_contract_authority_provider=_FixedAuthorityProvider(unverified),
        )


def test_valid_looking_fake_sha_digests_cannot_be_supplied_to_regime_engine_as_if_verified(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Negative test 6 (variant): `"a" * 64`/`"b" * 64` are syntactically
    valid SHA-256 hex, but were never computed from any resolved artifact.
    SHA-256 SHAPE != SHA-256 PROVENANCE.
    """
    fake_but_well_formed = ResolvedInputContract(
        feature_computation_profile="regime",
        input_contract_ref=REGIME_INPUT_CONTRACT.input_contract_ref,
        stream_registry_version=REGIME_INPUT_CONTRACT.stream_registry_version,
        included_streams=REGIME_INPUT_CONTRACT.included_streams,
        input_contract_content_id="a" * 64,
        stream_registry_content_id="b" * 64,
    )
    definition = make_regime_definition(regime_dimension_version="rgd-1")
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        RegimePassthroughFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
            input_contract_authority_provider=_FixedAuthorityProvider(fake_but_well_formed),
        )


def test_mutated_verified_regime_authority_rejected_structurally() -> None:
    """A genuinely resolver-issued regime authority cannot be turned into a
    different-but-still-accepted authority via `dataclasses.replace` at
    all — `replace()` itself calls `VerifiedInputContractAuthority`'s own
    disabled public constructor, so ANY field change raises `TypeError`
    structurally (Review-A round-5).
    """
    with pytest.raises(TypeError):
        dataclasses.replace(REGIME_INPUT_CONTRACT, included_streams=frozenset({"an-invented-stream"}))
    with pytest.raises(TypeError):
        dataclasses.replace(REGIME_INPUT_CONTRACT, stream_registry_version="v99")


def test_verified_regime_authority_not_exported_from_public_package() -> None:
    """Negative test 1: neither `VerifiedInputContractAuthority` nor its
    resolver-internal precursor `ResolvedInputContract` is part of
    `feature_engine`'s own public surface.
    """
    import feature_engine

    assert not hasattr(feature_engine, "VerifiedInputContractAuthority")
    assert not hasattr(feature_engine, "ResolvedInputContract")
    assert "VerifiedInputContractAuthority" not in feature_engine.__all__
    assert "ResolvedInputContract" not in feature_engine.__all__


def test_directly_fabricated_verified_type_cannot_be_supplied_to_regime_engine() -> None:
    """Negative test 2: directly constructing `VerifiedInputContractAuthority`
    — even with a fully genuine-looking field set plus Review-A's own
    literal residual example `"a" * 64`/`"b" * 64` — raises `TypeError`
    structurally, before any field is ever inspected.
    """
    with pytest.raises(TypeError):
        VerifiedInputContractAuthority(
            feature_computation_profile="regime",
            input_contract_ref=REGIME_INPUT_CONTRACT.input_contract_ref,
            stream_registry_version=REGIME_INPUT_CONTRACT.stream_registry_version,
            included_streams=REGIME_INPUT_CONTRACT.included_streams,
            input_contract_content_id="a" * 64,
            stream_registry_content_id="b" * 64,
        )


def test_static_provider_cannot_launder_fabricated_regime_authority(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """Negative test 3: `StaticInputContractAuthorityProvider` remains
    public, but wrapping a caller-manufactured "authority-shaped" object in
    it is still rejected by the engine's own `isinstance` check — there is
    no supported way to construct a genuine `VerifiedInputContractAuthority`
    to wrap in the first place.
    """
    fabricated = ResolvedInputContract(
        feature_computation_profile="regime",
        input_contract_ref=REGIME_INPUT_CONTRACT.input_contract_ref,
        stream_registry_version=REGIME_INPUT_CONTRACT.stream_registry_version,
        included_streams=REGIME_INPUT_CONTRACT.included_streams,
        input_contract_content_id="a" * 64,
        stream_registry_content_id="b" * 64,
    )
    laundering_provider = StaticInputContractAuthorityProvider(fabricated)  # type: ignore[arg-type]
    definition = make_regime_definition(regime_dimension_version="rgd-1")
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        RegimePassthroughFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
            input_contract_authority_provider=laundering_provider,
        )


def test_regime_engine_constructor_requires_provider_not_bare_authority_value() -> None:
    """Negative test 4: `RegimePassthroughFeatureEngine`'s own constructor
    signature exposes an `input_contract_authority_provider` parameter typed
    `InputContractAuthorityProvider` — never a `resolved_input_contract`/
    `ResolvedInputContract`/`VerifiedInputContractAuthority` parameter.
    """
    signature = inspect.signature(RegimePassthroughFeatureEngine.__init__)
    assert "input_contract_authority_provider" in signature.parameters
    assert "resolved_input_contract" not in signature.parameters
    assert not hasattr(REGIME_INPUT_CONTRACT, "resolve")


def test_empty_regime_content_id_fails_closed_via_resolver_factory() -> None:
    """Resolver-level field validation (moved off the now fully-disabled
    `VerifiedInputContractAuthority` public constructor, Review-A round-5) —
    retargeted directly at the sole legitimate entrypoint,
    `_seal_verified_authority`, which `authority_resolver.py` alone calls.
    """
    with pytest.raises(UnresolvedComputationCursorAuthorityError):
        _seal_verified_authority(
            feature_computation_profile=REGIME_INPUT_CONTRACT.feature_computation_profile,
            input_contract_ref=REGIME_INPUT_CONTRACT.input_contract_ref,
            stream_registry_version=REGIME_INPUT_CONTRACT.stream_registry_version,
            included_streams=REGIME_INPUT_CONTRACT.included_streams,
            input_contract_content_id="",
            stream_registry_content_id=REGIME_INPUT_CONTRACT.stream_registry_content_id,
        )


# --- Constructor/runtime rejection guards (P3-FEATURE-QG-COV-01 remediation) -
#
# The tests below exercise real, independent rejection paths never reached
# by any existing test: three constructor validation guards (a caller could
# misconfigure feature_type/upstream_source/scope even though every
# existing test always builds a self-consistent regime Definition/scope via
# `_engine`'s own `make_regime_definition`+`feature_scope` pairing), a
# misbehaving-provider identity check, this engine's own `ForeignScopeError`
# scope-isolation guard (P3-FEATURE-QG-EVID-06's own cited raise site,
# regime_passthrough.py:152 — recorded here as a factual overlap; this test
# alone is supporting evidence only, not a claim that EVID-06 is closed),
# and the two causal-ordering guards (`NonMonotonicRecordedTimeError` is one
# of the three error paths named by P3-FEATURE-QG-MIN-01 — recorded here as
# a factual overlap, not a claim that MIN-01 is closed).


def test_wrong_feature_type_for_regime_engine_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    definition = make_distance_definition()
    scope = feature_scope("distance_to_last_confirmed_swing", version=definition.feature_definition_version)
    with pytest.raises(ValueError, match="unsupported feature_type for regime pass-through"):
        RegimePassthroughFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
            input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
        )


def test_wrong_upstream_source_for_regime_engine_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """A definition with a correct `feature_type` ("volatility_metric") but
    `upstream_source="candle"` (a genuinely self-consistent candle-window
    Definition — `FeatureDefinition.__post_init__` itself requires
    `upstream_contract_refs` to match `upstream_source`, so a candle
    Definition is used verbatim rather than mutating a regime one) must be
    rejected by the second guard.
    """
    definition = make_candle_definition(feature_type="volatility_metric")
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    with pytest.raises(ValueError, match="requires upstream_source='regime'"):
        RegimePassthroughFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
            input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
        )


def test_scope_definition_mismatch_for_regime_engine_rejected(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    definition = make_regime_definition(feature_type="volatility_metric")
    scope = feature_scope("volatility_metric", version="a-different-version-than-the-definition")
    with pytest.raises(ValueError, match="scope does not match definition"):
        RegimePassthroughFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
            input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
        )


def test_engine_own_profile_check_rejects_mismatched_authority(
    allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """A provider that returns a genuine `VerifiedInputContractAuthority`,
    but one resolved for the WRONG `feature_computation_profile` (here: the
    swing-distance profile, injected into an engine that requires
    "regime"), must be rejected — a well-formed object alone is not trust.
    `StaticInputContractAuthorityProvider.resolve()` already pre-validates
    its own wrapped authority's profile, so `_FixedAuthorityProvider`
    (defined above, returns whatever it is given regardless of the
    requested profile) is used to isolate and exercise THIS engine's own
    independent `feature_computation_profile` guard instead.
    """
    definition = make_regime_definition(feature_type="volatility_metric")
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    with pytest.raises(InputContractIdentityMismatchError):
        RegimePassthroughFeatureEngine(
            scope,
            definition,
            allocator,
            time_source,
            feature_event_contract_version=FEATURE_OUTPUT_CONTRACT_VERSION,
            input_contract_authority_provider=_FixedAuthorityProvider(SWING_DISTANCE_INPUT_CONTRACT),
        )


def test_foreign_scope_regime_fact_rejected(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    fact = regime_classified_at(
        allocator,
        0,
        computed_metric="1.5",
        regime_dimension="volatility",
        regime_definition_version="rgd-1",
        instrument_id="ETH-USDT",
    )
    with pytest.raises(ForeignScopeError):
        engine.on_regime_classified(fact, cursor=_frontier_at(fact.recorded_time))


def test_non_monotonic_recorded_time_rejected(allocator: SequenceAllocator, time_source: FixedDeltaTimeSource) -> None:
    engine = _engine(allocator, time_source)
    first = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    engine.on_regime_classified(first, cursor=_frontier_at(first.recorded_time))
    earlier = regime_classified_at(
        allocator,
        1,
        computed_metric="1.6",
        regime_dimension="volatility",
        regime_definition_version="rgd-1",
        recorded_offset_seconds=-3600,
    )
    with pytest.raises(NonMonotonicRecordedTimeError):
        engine.on_regime_classified(earlier, cursor=_frontier_at(earlier.recorded_time))


def test_non_causal_time_source_rejected(allocator: SequenceAllocator) -> None:
    engine = _engine(allocator, NonCausalTimeSource())
    fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    with pytest.raises(RecordedTimeSourceViolationError):
        engine.on_regime_classified(fact, cursor=_frontier_at(fact.recorded_time))
