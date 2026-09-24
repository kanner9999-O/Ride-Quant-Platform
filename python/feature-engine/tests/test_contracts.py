from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from conftest import (
    FEATURE_OUTPUT_CONTRACT_VERSION,
    SWING_DISTANCE_EVIDENCE,
    SWING_DISTANCE_INPUT_CONTRACT,
    FixedDeltaTimeSource,
    feature_scope,
    frontier_at,
)

from feature_engine import (
    FEATURE_COMPUTED_CONTRACT_ID,
    DecimalPrecisionPolicy,
    EventContractRef,
    EventRecordRef,
    InvalidFeatureDefinitionError,
    resolve_computation_cursor,
)
from feature_engine.contracts import (
    InputMergePolicy,
    PreparedFeatureComputed,
    _finalize_prepared_batch,
    _validate_canonical_recorded_time,
    is_visible_at_cursor,
)
from feature_engine.errors import CanonicalHistoryMismatchError, UnsupportedMergePolicyError

# Direct unit tests of `resolve_output_event_contract_authority_from_repository`
# (ADR-039/ADR-040 remediation, supersedes the earlier `resolve_output_contract_refs`
# caller-injected-string mechanism) live in `test_output_contract_resolver.py`,
# mirroring where `resolve_input_contract_authority_from_repository`'s own
# direct tests live (`test_authority_resolver.py`).


# P3-PY-MUT-STEP9-B remediation (EVID-03, actionable_test_gap_candidate):
# `is_visible_at_cursor` is feature.md §12(a)'s complete three-branch cursor
# visibility predicate, applied identically everywhere Feature checks whether
# an upstream event is visible -- but every existing test/fixture only ever
# constructs refs whose stream_id IS one of the engine's own included_streams
# (real topology, per conftest's own stream-id constants), so branch 1's
# "stream-universe membership" `return False` for a FOREIGN stream_id was
# never directly exercised. Direct unit test of the pure function itself.


def test_is_visible_at_cursor_rejects_stream_not_in_included_streams() -> None:
    ref = EventRecordRef(stream_id="not-a-real-stream", sequence=1, event_id="x")
    recorded_time = datetime(2026, 1, 1, tzinfo=UTC)
    far_future_cursor = datetime(2030, 1, 1, tzinfo=UTC)
    assert (
        is_visible_at_cursor(
            ref,
            recorded_time,
            included_streams=frozenset({"market-data-ingestion-candle"}),
            stream_positions={"market-data-ingestion-candle": 10**9},
            cursor_recorded_time=far_future_cursor,
        )
        is False
    )


def test_is_visible_at_cursor_accepts_stream_that_is_in_included_streams() -> None:
    """Sanity control for the test above: the SAME ref shape, with a
    stream_id that genuinely IS in `included_streams`, is visible."""
    ref = EventRecordRef(stream_id="market-data-ingestion-candle", sequence=1, event_id="x")
    recorded_time = datetime(2026, 1, 1, tzinfo=UTC)
    far_future_cursor = datetime(2030, 1, 1, tzinfo=UTC)
    assert (
        is_visible_at_cursor(
            ref,
            recorded_time,
            included_streams=frozenset({"market-data-ingestion-candle"}),
            stream_positions={"market-data-ingestion-candle": 10**9},
            cursor_recorded_time=far_future_cursor,
        )
        is True
    )


# --- Condition-3 mutation-surface-completeness design candidate 001,
# DecimalPrecisionPolicy (FI-DECIMAL-APPLY-02, FI-DECIMAL-POSTINIT-01/02) --
#
# `DecimalPrecisionPolicy` is only ever constructed via `conftest.
# make_decimal_policy(digits=2)` elsewhere in this suite -- always a
# non-zero `digits` and always the valid `"ROUND_HALF_UP"` rounding mode,
# always applied to "clean" decimal fixture values that never land on an
# exact rounding half-boundary. These direct, isolated tests exercise the
# construction-time boundary/membership guards and the rounding-mode-
# sensitive branch of `.apply()` that the rest of the suite never reaches.


def test_decimal_precision_policy_apply_rounds_half_up_at_exact_boundary() -> None:
    policy = DecimalPrecisionPolicy(digits=2, rounding="ROUND_HALF_UP")
    assert policy.apply(Decimal("1.005")) == Decimal("1.01")


def test_decimal_precision_policy_digits_zero_is_valid_boundary() -> None:
    policy = DecimalPrecisionPolicy(digits=0, rounding="ROUND_HALF_UP")
    assert policy.digits == 0


def test_decimal_precision_policy_invalid_rounding_mode_rejected() -> None:
    with pytest.raises(InvalidFeatureDefinitionError):
        DecimalPrecisionPolicy(digits=2, rounding="NOT_A_REAL_MODE")


# --- ADR043-IMPLDESIGN-A-MAJ-04: InputMergePolicy structural validation -----


def test_input_merge_policy_rejects_empty_algorithm() -> None:
    with pytest.raises(UnsupportedMergePolicyError):
        InputMergePolicy(algorithm="", concurrent_tie_break=("stream_id", "sequence"))


def test_input_merge_policy_rejects_empty_concurrent_tie_break() -> None:
    with pytest.raises(UnsupportedMergePolicyError):
        InputMergePolicy(algorithm="deterministic-causal-topological-order", concurrent_tie_break=())


def test_input_merge_policy_accepts_well_formed_value() -> None:
    policy = InputMergePolicy(
        algorithm="deterministic-causal-topological-order", concurrent_tie_break=("stream_id", "sequence")
    )
    assert policy.algorithm == "deterministic-causal-topological-order"
    assert policy.concurrent_tie_break == ("stream_id", "sequence")


# --- ADR043-IMPL-A-MAJ-06: catch-up reconciliation batch-length safety net -


def test_validate_canonical_recorded_time_rejects_mismatched_batch_lengths() -> None:
    """Wave-5 (Condition-1B): `_validate_canonical_recorded_time`'s own
    `zip(..., strict=True)` is an independent, direct safety net against a
    caller supplying mismatched-length `prepared_events`/`canonical_events`
    sequences — it must fail rather than silently pairing/truncating to
    the shorter sequence. (The one current caller, `PreparedBatch.
    reconcile`, already has its own equal-length pre-check before calling
    this function; this test exercises the function's own independent
    contract directly — the same "verify a private helper's own defensive
    contract in isolation" discipline already established for
    `_seal_verified_authority` elsewhere in this test suite.)
    """
    with pytest.raises(ValueError):
        _validate_canonical_recorded_time((), (object(),))  # type: ignore[arg-type]


# --- Wave-6 (Condition-1B): _finalize_prepared_batch / _validate_canonical_
# recorded_time sentinel-default (`None` -> `""`) guards ----------------------
#
# Both `_finalize_prepared_batch` and `_validate_canonical_recorded_time`
# track a same-batch preceding invalidation's own real `ref`/`recorded_time`
# via a module-local `None`-sentinel local, threaded through to a same-batch
# `PreparedFeatureComputed` whose `preceding_batch_invalidation_causation`/
# `depends_on_preceding_invalidation_timing` is True but which is NOT
# actually preceded by a real invalidation earlier in the same batch (a
# malformed/inconsistent prepared batch) -- these three direct, minimal
# constructions exercise that fail-closed guard without inspecting mutant
# internals or asserting exact message text.


def _prepared_computed(
    *,
    recorded_time_floor: datetime,
    preceding_batch_invalidation_causation: bool = False,
    depends_on_preceding_invalidation_timing: bool = False,
) -> PreparedFeatureComputed:
    scope = feature_scope("distance_to_last_confirmed_swing", version="wave6-test")
    input_ref = EventRecordRef(stream_id="market-data-ingestion-candle", sequence=1, event_id="wave6-input-1")
    cursor = resolve_computation_cursor(
        frontier_at(recorded_time_floor), resolved_input_contract=SWING_DISTANCE_INPUT_CONTRACT
    )
    return PreparedFeatureComputed(
        scope=scope,
        value=Decimal("1"),
        unit="price",
        window_start=recorded_time_floor,
        window_end=recorded_time_floor,
        input_fact_refs=(input_ref,),
        supersedes_fact_ref=None,
        causation_refs=(input_ref,),
        preceding_batch_invalidation_causation=preceding_batch_invalidation_causation,
        recorded_time_floor=recorded_time_floor,
        depends_on_preceding_invalidation_timing=depends_on_preceding_invalidation_timing,
        event_contract_ref=EventContractRef(FEATURE_COMPUTED_CONTRACT_ID, FEATURE_OUTPUT_CONTRACT_VERSION),
        computation_cursor=cursor,
        computation_dependency_content_evidence=SWING_DISTANCE_EVIDENCE,
    )


def test_finalize_prepared_batch_fails_closed_when_preceding_invalidation_causation_has_no_real_invalidation() -> (
    None
):
    """`_finalize_prepared_batch`'s `invalidation_ref` local starts `None`
    and is only ever set when an earlier `PreparedFeatureFactInvalidated`
    is finalized in the SAME batch. A `PreparedFeatureComputed` whose own
    `preceding_batch_invalidation_causation=True` but which is the batch's
    only/first item (no such invalidation precedes it) must fail closed --
    `PreparedFeatureComputed.finalize`'s own `invalidation_ref is None`
    guard exists specifically to reject exactly this malformed batch shape,
    never to silently splice a placeholder causation ref.
    """
    floor = datetime(2026, 1, 1, tzinfo=UTC)
    prepared = _prepared_computed(recorded_time_floor=floor, preceding_batch_invalidation_causation=True)
    ref = EventRecordRef(stream_id="feature-engine-distance-output", sequence=1, event_id="wave6-out-1")
    with pytest.raises(ValueError):
        _finalize_prepared_batch((prepared,), (ref,), time_source=FixedDeltaTimeSource())


def test_finalize_prepared_batch_fails_closed_when_depends_on_timing_has_no_real_invalidation() -> None:
    """Sibling sentinel guard: `_finalize_prepared_batch`'s `invalidation_
    recorded_time` local starts `None` and is only set once an earlier same-
    batch invalidation is finalized. A `PreparedFeatureComputed` whose own
    `depends_on_preceding_invalidation_timing=True` but which has no such
    preceding invalidation in the same batch must fail closed with the
    documented `ValueError` -- never silently fall through to comparing a
    real `datetime` floor against a non-`datetime` sentinel.
    """
    floor = datetime(2026, 1, 1, tzinfo=UTC)
    prepared = _prepared_computed(recorded_time_floor=floor, depends_on_preceding_invalidation_timing=True)
    ref = EventRecordRef(stream_id="feature-engine-distance-output", sequence=1, event_id="wave6-out-2")
    with pytest.raises(ValueError):
        _finalize_prepared_batch((prepared,), (ref,), time_source=FixedDeltaTimeSource())


def test_validate_canonical_recorded_time_fails_closed_when_depends_on_timing_has_no_real_invalidation() -> None:
    """`_validate_canonical_recorded_time`'s own analogous `invalidation_
    recorded_time` sentinel guard, in the historical-reconcile validation
    path: a prepared replacement that depends on a preceding same-batch
    invalidation's timing, with no such invalidation reconciled earlier in
    the same call, must fail closed with the documented
    `CanonicalHistoryMismatchError` -- never fall through to a mixed-type
    comparison against a non-`datetime` sentinel.
    """
    floor = datetime(2026, 1, 1, tzinfo=UTC)
    prepared = _prepared_computed(recorded_time_floor=floor, depends_on_preceding_invalidation_timing=True)
    ref = EventRecordRef(stream_id="feature-engine-distance-output", sequence=1, event_id="wave6-out-3")
    canonical = prepared.finalize(ref, floor + timedelta(seconds=1))
    with pytest.raises(CanonicalHistoryMismatchError):
        _validate_canonical_recorded_time((prepared,), (canonical,))
