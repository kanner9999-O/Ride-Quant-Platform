from __future__ import annotations

import pytest
from conftest import feature_scope, make_candle_definition

from feature_engine import CandleWindowFeatureEngine
from feature_engine.errors import UnsupportedFeatureFormulaError

# --- P3-FEATURE-A-MAJ-03 remediation: Candle-derived formula computation is
# permanently fail-closed — no caller-supplied executable formula is ever
# authorized merely by a matching formula_id string, and no formula
# registry/expression language/plugin mechanism/concrete indicator exists as
# a substitute. Every construction attempt for the candle path fails closed.


def test_candle_path_always_fails_closed_at_construction() -> None:
    definition = make_candle_definition()
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    with pytest.raises(UnsupportedFeatureFormulaError):
        CandleWindowFeatureEngine(scope, definition)


def test_candle_path_fails_closed_regardless_of_formula_id() -> None:
    definition = make_candle_definition(formula_id="anything-at-all")
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    with pytest.raises(UnsupportedFeatureFormulaError):
        CandleWindowFeatureEngine(scope, definition)


def test_candle_path_fails_closed_for_directional_persistence_too() -> None:
    definition = make_candle_definition(feature_type="directional_persistence_metric")
    scope = feature_scope("directional_persistence_metric", version=definition.feature_definition_version)
    with pytest.raises(UnsupportedFeatureFormulaError):
        CandleWindowFeatureEngine(scope, definition)
