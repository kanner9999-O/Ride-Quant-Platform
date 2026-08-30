from __future__ import annotations

import pytest
from conftest import feature_scope, make_candle_definition, make_distance_definition, make_regime_definition

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


# --- Constructor validation guards (P3-FEATURE-QG-COV-01 remediation) -------
#
# The three tests above all reach the permanent fail-closed `raise` at the
# bottom of `__init__` — none of them exercise the three earlier validation
# guards that reject a definition/scope BEFORE that point is ever reached.
# These guards are real, independent rejection paths (a caller could
# misconfigure `feature_type`/`upstream_source`/`scope` even though the
# candle path itself is permanently unavailable) and must raise `ValueError`
# distinctly from `UnsupportedFeatureFormulaError`.


def test_wrong_feature_type_for_candle_engine_rejected() -> None:
    """A definition whose `feature_type` is not one of the two candle-window
    feature types (e.g. a swing-distance Definition) must be rejected by the
    first guard, never reaching the permanent fail-closed raise.
    """
    definition = make_distance_definition()
    scope = feature_scope("distance_to_last_confirmed_swing", version=definition.feature_definition_version)
    with pytest.raises(ValueError, match="unsupported feature_type for candle-window engine"):
        CandleWindowFeatureEngine(scope, definition)


def test_wrong_upstream_source_for_candle_engine_rejected() -> None:
    """A definition with a correct `feature_type` but `upstream_source`
    other than `"candle"` (e.g. the regime pass-through profile) must be
    rejected by the second guard.
    """
    definition = make_regime_definition(feature_type="volatility_metric")
    scope = feature_scope("volatility_metric", version=definition.feature_definition_version)
    with pytest.raises(ValueError, match="requires upstream_source='candle'"):
        CandleWindowFeatureEngine(scope, definition)


def test_scope_definition_mismatch_for_candle_engine_rejected() -> None:
    """A `scope` whose `feature_definition_version` does not match the
    Definition's own version must be rejected by the third guard, before any
    fail-closed-formula raise.
    """
    definition = make_candle_definition()
    scope = feature_scope("volatility_metric", version="a-different-version-than-the-definition")
    with pytest.raises(ValueError, match="scope does not match definition"):
        CandleWindowFeatureEngine(scope, definition)
