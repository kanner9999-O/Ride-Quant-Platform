"""`volatility_metric`/`directional_persistence_metric` — `upstream_source:
candle` (feature.md §7.1/§7.2).

P3-FEATURE-A-MAJ-03 remediation: feature.md leaves the concrete Candle-derived
formula (ATR/stdev/realized-volatility/etc.) fully unresolved, and no current
repository authority pins an immutable executable identity + parameters for
any `formula_id`. A caller-supplied callable matched only by a `formula_id`
string equality check is not authorization — it is unconditional trust in
whatever code the caller happens to construct this engine with, regardless of
what that code actually computes. That prior design has been removed
entirely, including the `FeatureFormula` injection Protocol.

Because current authority does not pin an immutable executable identity +
parameters, Candle-derived `volatility_metric`/`directional_persistence_metric`
computation is not executable from this engine: construction always fails
closed (`UnsupportedFeatureFormulaError`). No formula registry, expression
language, plugin mechanism, or concrete indicator is introduced as a
substitute — until a governed decision pins genuine executable formula
identity (a Domain Contract / ADR concern, out of this bounded correction's
scope), Candle-path Feature computation is unavailable by design, not merely
undocumented.

The `upstream_source: regime` path (`regime_passthrough.py`) is unaffected —
it never executes a formula, it exposes an upstream `RegimeClassified.
computed_metric` verbatim.
"""

from __future__ import annotations

from .contracts import FeatureDefinition, FeatureScope
from .errors import UnsupportedFeatureFormulaError


class CandleWindowFeatureEngine:
    """Permanently fail-closed for `upstream_source: candle` — see module
    docstring (P3-FEATURE-A-MAJ-03). No instance of this class is ever able
    to compute or emit a `FeatureComputed`/`FeatureFactInvalidated` event;
    construction itself always raises. `scope` is accepted (and validated)
    only to keep this engine's constructor shape consistent with the other
    two computation engines — it is never stored or used beyond validation.
    """

    def __init__(self, scope: FeatureScope, definition: FeatureDefinition) -> None:
        if definition.feature_type not in ("volatility_metric", "directional_persistence_metric"):
            raise ValueError(f"unsupported feature_type for candle-window engine: {definition.feature_type!r}")
        if definition.upstream_source != "candle":
            raise ValueError("CandleWindowFeatureEngine requires upstream_source='candle'")
        if scope.feature_type != definition.feature_type or scope.feature_definition_version != (
            definition.feature_definition_version
        ):
            raise ValueError("scope does not match definition")
        raise UnsupportedFeatureFormulaError(
            "Candle-derived formula computation is not authorized: no current repository authority pins an "
            f"immutable executable identity + parameters for formula_id={definition.formula_id!r} "
            "(feature.md §6/§7.1/§7.2) — this engine never executes a caller-supplied formula matched only by a "
            "formula_id string. Fails closed per P3-FEATURE-A-MAJ-03."
        )
