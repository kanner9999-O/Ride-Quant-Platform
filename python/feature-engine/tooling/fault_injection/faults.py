"""The exact, approved fault population for Condition-3 evidence.

Ten faults across the five high-materiality methods named in `feature-
engine-mutation-surface-completeness-design-001.md` §3 (APPROVED design).
Every `old_string`/`new_string` pair below is copied verbatim from that
approved design's own "Deterministic reproduction contract" for the
corresponding fault ID — this module does not improvise substitute faults.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FaultSpec:
    """One approved, individually-identified fault-injection specification.

    `source_file` is relative to the `python/feature-engine/` directory
    (e.g. `"src/feature_engine/candle.py"`). `old_string` must match
    exactly once in the pinned file's exact content — the harness fails
    closed (`INJECTION_FAILED`) otherwise.
    """

    fault_id: str
    method: str
    source_file: str
    fault_class: str
    old_string: str
    new_string: str


APPROVED_FAULTS: tuple[FaultSpec, ...] = (
    FaultSpec(
        fault_id="FI-STATIC-PROVIDER-01",
        method="authority_resolver.StaticInputContractAuthorityProvider.resolve",
        source_file="src/feature_engine/authority_resolver.py",
        fault_class="inverted_guard",
        old_string="if self.authority.feature_computation_profile != profile:",
        new_string="if self.authority.feature_computation_profile == profile:",
    ),
    FaultSpec(
        fault_id="FI-OHLCV-FIELD-01",
        method="candle.OHLCV.field",
        source_file="src/feature_engine/candle.py",
        fault_class="branch_swap",
        old_string="            return self.high",
        new_string="            return self.low",
    ),
    FaultSpec(
        fault_id="FI-OHLCV-FIELD-02",
        method="candle.OHLCV.field",
        source_file="src/feature_engine/candle.py",
        fault_class="fail_closed_bypass",
        old_string='        raise ValueError(f"unsupported reference_price_field: {name!r}")',
        new_string="        return self.close",
    ),
    FaultSpec(
        fault_id="FI-DECIMAL-APPLY-01",
        method="contracts.DecimalPrecisionPolicy.apply",
        source_file="src/feature_engine/contracts.py",
        fault_class="sign_flip",
        old_string="quantum = Decimal(1).scaleb(-self.digits)",
        new_string="quantum = Decimal(1).scaleb(self.digits)",
    ),
    FaultSpec(
        fault_id="FI-DECIMAL-APPLY-02",
        method="contracts.DecimalPrecisionPolicy.apply",
        source_file="src/feature_engine/contracts.py",
        fault_class="dropped_rounding_kwarg",
        old_string="return value.quantize(quantum, rounding=self.rounding)",
        new_string="return value.quantize(quantum)",
    ),
    FaultSpec(
        fault_id="FI-DECIMAL-POSTINIT-01",
        method="contracts.DecimalPrecisionPolicy.__post_init__",
        source_file="src/feature_engine/contracts.py",
        fault_class="boundary_flip",
        old_string="if self.digits < 0:",
        new_string="if self.digits <= 0:",
    ),
    FaultSpec(
        fault_id="FI-DECIMAL-POSTINIT-02",
        method="contracts.DecimalPrecisionPolicy.__post_init__",
        source_file="src/feature_engine/contracts.py",
        fault_class="inverted_membership",
        old_string="if self.rounding not in _VALID_ROUNDINGS:",
        new_string="if self.rounding in _VALID_ROUNDINGS:",
    ),
    FaultSpec(
        fault_id="FI-FEATUREDEF-01",
        method="contracts.FeatureDefinition.__post_init__",
        source_file="src/feature_engine/contracts.py",
        fault_class="policy_equality_guard_inversion",
        old_string="if self.correction_policy != CORRECTION_POLICY:",
        new_string="if self.correction_policy == CORRECTION_POLICY:",
    ),
    FaultSpec(
        fault_id="FI-FEATUREDEF-02",
        method="contracts.FeatureDefinition.__post_init__",
        source_file="src/feature_engine/contracts.py",
        fault_class="cross_field_or_and_inversion",
        old_string=(
            "if any(field is not None for field in distance_only_fields) or self.normalization_policy is not None:"
        ),
        new_string=(
            "if any(field is not None for field in distance_only_fields) and self.normalization_policy is not None:"
        ),
    ),
    FaultSpec(
        fault_id="FI-FEATUREDEF-03",
        method="contracts.FeatureDefinition.__post_init__",
        source_file="src/feature_engine/contracts.py",
        fault_class="boundary_flip",
        old_string="if self.window_candle_count is None or self.window_candle_count < 1:",
        new_string="if self.window_candle_count is None or self.window_candle_count <= 1:",
    ),
)
