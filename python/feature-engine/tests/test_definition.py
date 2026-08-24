from __future__ import annotations

from typing import Any

import pytest
from conftest import RangeFormula, feature_scope, make_candle_definition, make_decimal_policy, make_distance_definition

from feature_engine import (
    CORRECTION_POLICY,
    CURRENT_VIEW_SELECTION_POLICY,
    EFFECTIVE_WINDOW_POLICY,
    ELIGIBLE_SWING_EFFECTIVE_CUTOFF_POLICY,
    ELIGIBLE_SWING_SELECTION_POLICY,
    INPUT_NORMALIZATION_POLICY,
    MISSING_INPUT_POLICY,
    WARM_UP_POLICY,
    FeatureDefinition,
    InvalidFeatureDefinitionError,
)

# --- 1. Feature subject identity --------------------------------------------


def test_subject_id_same_five_fields_same_id() -> None:
    a = feature_scope("volatility_metric", version="fd-1")
    b = feature_scope("volatility_metric", version="fd-1")
    assert a.feature_subject_id == b.feature_subject_id


@pytest.mark.parametrize(
    "kwargs",
    [
        {"instrument_id": "ETH-USDT"},
        {"venue_id": "other-venue"},
        {"timeframe": "5m"},
        {"version": "fd-2"},
    ],
)
def test_subject_id_any_field_difference_different_id(kwargs: dict[str, str]) -> None:
    base = feature_scope("volatility_metric", version="fd-1")
    version = kwargs.pop("version", "fd-1")
    other = feature_scope("volatility_metric", version=version, **kwargs)
    assert base.feature_subject_id != other.feature_subject_id


def test_subject_id_different_feature_type_different_id() -> None:
    a = feature_scope("volatility_metric", version="fd-1")
    b = feature_scope("directional_persistence_metric", version="fd-1")
    assert a.feature_subject_id != b.feature_subject_id


# --- 2. Definition validation ------------------------------------------------


def _base_kwargs() -> dict[str, Any]:
    return {
        "feature_definition_id": "fd",
        "feature_definition_version": "fd-1",
        "unit": "ratio",
        "decimal_precision_policy": make_decimal_policy(),
        "warm_up_policy": WARM_UP_POLICY,
        "missing_input_policy": MISSING_INPUT_POLICY,
        "correction_policy": CORRECTION_POLICY,
        "effective_window_policy": EFFECTIVE_WINDOW_POLICY,
        "current_view_selection_policy": CURRENT_VIEW_SELECTION_POLICY,
        "input_normalization_policy": INPUT_NORMALIZATION_POLICY,
    }


def test_dual_upstream_source_rejected() -> None:
    with pytest.raises(InvalidFeatureDefinitionError):
        FeatureDefinition(
            **_base_kwargs(),
            feature_type="volatility_metric",
            upstream_source="candle",
            window_candle_count=3,
            formula_id=RangeFormula.formula_id,
            required_upstream_definition_version="rgd-1",  # regime-only field set alongside candle path
        )


def test_missing_required_field_rejected_upstream_source_absent() -> None:
    with pytest.raises(InvalidFeatureDefinitionError):
        FeatureDefinition(**_base_kwargs(), feature_type="volatility_metric")


def test_missing_required_field_rejected_window_candle_count_absent() -> None:
    with pytest.raises(InvalidFeatureDefinitionError):
        FeatureDefinition(
            **_base_kwargs(),
            feature_type="volatility_metric",
            upstream_source="candle",
            formula_id=RangeFormula.formula_id,
        )


def test_missing_required_field_rejected_regime_definition_version_absent() -> None:
    with pytest.raises(InvalidFeatureDefinitionError):
        FeatureDefinition(**_base_kwargs(), feature_type="volatility_metric", upstream_source="regime")


def test_contradictory_type_specific_fields_rejected_distance_field_on_metric() -> None:
    with pytest.raises(InvalidFeatureDefinitionError):
        FeatureDefinition(
            **_base_kwargs(),
            feature_type="volatility_metric",
            upstream_source="regime",
            required_upstream_definition_version="rgd-1",
            swing_direction="HIGH",  # distance-only field
        )


def test_contradictory_type_specific_fields_rejected_metric_field_on_distance() -> None:
    with pytest.raises(InvalidFeatureDefinitionError):
        FeatureDefinition(
            **_base_kwargs(),
            feature_type="distance_to_last_confirmed_swing",
            swing_direction="HIGH",
            distance_representation="signed",
            reference_price_field="close",
            eligible_swing_selection_policy=ELIGIBLE_SWING_SELECTION_POLICY,
            eligible_swing_effective_cutoff_policy=ELIGIBLE_SWING_EFFECTIVE_CUTOFF_POLICY,
            required_swing_definition_version="swd-1",
            upstream_source="candle",  # metric-only field
        )


def test_invalid_reference_price_field_rejected() -> None:
    with pytest.raises(InvalidFeatureDefinitionError):
        FeatureDefinition(
            **_base_kwargs(),
            feature_type="distance_to_last_confirmed_swing",
            swing_direction="HIGH",
            distance_representation="signed",
            reference_price_field="typical_price",  # not open/high/low/close
            eligible_swing_selection_policy=ELIGIBLE_SWING_SELECTION_POLICY,
            eligible_swing_effective_cutoff_policy=ELIGIBLE_SWING_EFFECTIVE_CUTOFF_POLICY,
            required_swing_definition_version="swd-1",
        )


def test_non_canonical_policy_identifier_rejected() -> None:
    with pytest.raises(InvalidFeatureDefinitionError):
        FeatureDefinition(
            feature_definition_id="fd",
            feature_definition_version="fd-1",
            feature_type="volatility_metric",
            upstream_source="regime",
            required_upstream_definition_version="rgd-1",
            unit="ratio",
            decimal_precision_policy=make_decimal_policy(),
            warm_up_policy=WARM_UP_POLICY,
            missing_input_policy=MISSING_INPUT_POLICY,
            correction_policy=CORRECTION_POLICY,
            effective_window_policy=EFFECTIVE_WINDOW_POLICY,
            current_view_selection_policy="not-the-canonical-string",
            input_normalization_policy=INPUT_NORMALIZATION_POLICY,
        )


def test_valid_definitions_accepted() -> None:
    make_candle_definition()
    make_distance_definition()
