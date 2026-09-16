"""The exact, approved fault population for Condition-3 evidence.

Fourteen faults across nine high-materiality methods: the historical ten
faults across the five methods named in `feature-engine-mutation-surface-
completeness-design-001.md` §3 (APPROVED design), plus four faults across
four additional current-boundary methods named in `feature-engine-mutation-
surface-completeness-design-001-amendment-001.md` §3 (APPROVED — DESIGN
AMENDMENT EFFECTIVE). Every `old_string`/`new_string` pair below is copied
verbatim from the corresponding approved document's own "Deterministic
reproduction contract" / fault specification for that exact fault ID — this
module does not improvise substitute faults.
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
        old_string='        if name == "high":\n            return self.high',
        new_string='        if name == "high":\n            return self.low',
    ),
    FaultSpec(
        fault_id="FI-OHLCV-FIELD-02",
        method="candle.OHLCV.field",
        source_file="src/feature_engine/candle.py",
        fault_class="fail_closed_bypass",
        old_string=(
            '        if name == "close":\n'
            "            return self.close\n"
            '        raise ValueError(f"unsupported reference_price_field: {name!r}")'
        ),
        new_string=('        if name == "close":\n            return self.close\n        return self.close'),
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
    # --- Amendment 001 (APPROVED — DESIGN AMENDMENT EFFECTIVE): 4 new
    # current-boundary faults across 4 new target methods, copied verbatim
    # from feature-engine-mutation-surface-completeness-design-001-
    # amendment-001.md §3.1-3.4. ---------------------------------------------
    FaultSpec(
        fault_id="FI-PREPTRANS-RECONCILE-01",
        method="contracts.PreparedTransition.reconcile",
        source_file="src/feature_engine/contracts.py",
        fault_class="guard_inversion",
        old_string="if not _prepared_matches_canonical(prepared, canonical):",
        new_string="if _prepared_matches_canonical(prepared, canonical):",
    ),
    FaultSpec(
        fault_id="FI-PFC-FINALIZE-01",
        method="contracts.PreparedFeatureComputed.finalize",
        source_file="src/feature_engine/contracts.py",
        fault_class="silent_corruption",
        old_string="causation_refs = (*causation_refs, invalidation_ref)",
        new_string="causation_refs = (*causation_refs,)",
    ),
    FaultSpec(
        fault_id="FI-INPUTMERGE-POSTINIT-01",
        method="contracts.InputMergePolicy.__post_init__",
        source_file="src/feature_engine/contracts.py",
        fault_class="guard_inversion",
        old_string="if not self.algorithm:",
        new_string="if self.algorithm:",
    ),
    FaultSpec(
        fault_id="FI-OWNER-STATE-01",
        method="ownership.AuthoritativeSubjectOwner.state",
        source_file="src/feature_engine/ownership.py",
        fault_class="silent_corruption",
        old_string=(
            "return self._handle.state if self._handle is not None else SubjectOwnershipState.INACTIVE"
        ),
        new_string=(
            "return self._handle.state if self._handle is not None else SubjectOwnershipState.ACTIVE"
        ),
    ),
)
