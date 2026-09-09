from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from feature_engine import (
    DecimalPrecisionPolicy,
    EventRecordRef,
    InvalidFeatureDefinitionError,
)
from feature_engine.contracts import is_visible_at_cursor

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
