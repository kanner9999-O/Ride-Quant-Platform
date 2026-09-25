from __future__ import annotations

import pytest

from context_aggregator import ContextDefinition, InvalidContextTypeError


def test_valid_definition_constructs(definition: ContextDefinition) -> None:
    assert definition.context_definition_version == "ctxdef-v1"
    assert definition.context_type == "market_context"


def test_invalid_context_type_rejected() -> None:
    with pytest.raises(InvalidContextTypeError):
        ContextDefinition(
            context_definition_id="ctxdef",
            context_definition_version="ctxdef-v1",
            required_structure_definition_version="struct-v1",
            required_volatility_regime_definition_version="regime-vol-v1",
            required_directional_persistence_regime_definition_version="regime-dp-v1",
            required_volatility_metric_feature_definition_version="feat-vol-v1",
            required_directional_persistence_metric_feature_definition_version="feat-dp-v1",
            required_distance_to_last_confirmed_swing_feature_definition_version="feat-dist-v1",
            context_type="strategy_context",
        )


def test_missing_required_field_rejected_by_constructor() -> None:
    with pytest.raises(TypeError):
        ContextDefinition(  # type: ignore[call-arg]
            context_definition_id="ctxdef",
            context_definition_version="ctxdef-v1",
        )
