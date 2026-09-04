from __future__ import annotations

from datetime import UTC, datetime

import pytest

from feature_engine import (
    FEATURE_COMPUTED_CONTRACT_ID,
    FEATURE_FACT_INVALIDATED_CONTRACT_ID,
    EventContractRef,
    EventRecordRef,
    UnresolvedOutputContractAuthorityError,
    resolve_output_contract_refs,
)
from feature_engine.contracts import is_visible_at_cursor

# P3-PY-MUT-STEP9-A field-completeness remediation (EVID-03,
# constructed_object_field_not_independently_asserted): `resolve_output_
# contract_refs` is the single place every computation engine resolves its
# own outbound `(FeatureComputed, FeatureFactInvalidated)` `event_contract_
# ref`s -- every existing test file only ever imports the two contract-ID
# constants to build its OWN expected refs by hand, never calling this
# function directly and asserting its actual return value. This is a direct
# unit test of the function itself.


def test_resolve_output_contract_refs_returns_genuine_pinned_identities() -> None:
    computed_ref, invalidated_ref = resolve_output_contract_refs("fv1")
    assert computed_ref == EventContractRef(FEATURE_COMPUTED_CONTRACT_ID, "fv1")
    assert invalidated_ref == EventContractRef(FEATURE_FACT_INVALIDATED_CONTRACT_ID, "fv1")
    assert computed_ref.contract_id == FEATURE_COMPUTED_CONTRACT_ID
    assert computed_ref.contract_version == "fv1"
    assert invalidated_ref.contract_id == FEATURE_FACT_INVALIDATED_CONTRACT_ID
    assert invalidated_ref.contract_version == "fv1"


def test_resolve_output_contract_refs_different_version_produces_different_refs() -> None:
    computed_v1, invalidated_v1 = resolve_output_contract_refs("fv1")
    computed_v2, invalidated_v2 = resolve_output_contract_refs("fv2")
    assert computed_v1 != computed_v2
    assert invalidated_v1 != invalidated_v2
    assert computed_v1.contract_id == computed_v2.contract_id
    assert invalidated_v1.contract_id == invalidated_v2.contract_id


def test_resolve_output_contract_refs_empty_version_fails_closed() -> None:
    with pytest.raises(UnresolvedOutputContractAuthorityError):
        resolve_output_contract_refs("")


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
