from __future__ import annotations

import pytest

from context_aggregator import ContextSubjectScope, InvalidContextTypeError


def test_same_scope_yields_same_subject_id() -> None:
    a = ContextSubjectScope(
        instrument_id="BTC-USD", venue_id="binance", timeframe="1h", context_definition_version="ctxdef-v1"
    )
    b = ContextSubjectScope(
        instrument_id="BTC-USD", venue_id="binance", timeframe="1h", context_definition_version="ctxdef-v1"
    )
    assert a.context_subject_id == b.context_subject_id


@pytest.mark.parametrize(
    "field,value",
    [
        ("instrument_id", "ETH-USD"),
        ("venue_id", "coinbase"),
        ("timeframe", "4h"),
        ("context_definition_version", "ctxdef-v2"),
    ],
)
def test_different_scope_field_yields_different_subject_id(field: str, value: str) -> None:
    base: dict[str, str] = dict(
        instrument_id="BTC-USD", venue_id="binance", timeframe="1h", context_definition_version="ctxdef-v1"
    )
    a = ContextSubjectScope(**base)
    changed = dict(base)
    changed[field] = value
    b = ContextSubjectScope(**changed)
    assert a.context_subject_id != b.context_subject_id


def test_subject_id_is_opaque_string_not_reversible_shape() -> None:
    scope = ContextSubjectScope(
        instrument_id="BTC-USD", venue_id="binance", timeframe="1h", context_definition_version="ctxdef-v1"
    )
    subject_id = scope.context_subject_id
    assert isinstance(subject_id, str)
    assert "BTC-USD" not in subject_id


def test_invalid_context_type_rejected() -> None:
    with pytest.raises(InvalidContextTypeError):
        ContextSubjectScope(
            instrument_id="BTC-USD",
            venue_id="binance",
            timeframe="1h",
            context_definition_version="ctxdef-v1",
            context_type="strategy_context",
        )
