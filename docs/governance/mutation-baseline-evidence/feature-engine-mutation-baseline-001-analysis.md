# Feature Engine Mutation Baseline 001 — Step-4 Calibration Analysis

**Status: ANALYSIS ONLY — NON-GATING — NO THRESHOLD PROPOSED**

This document is the governed Step-4 analysis of the completed, durably-recorded
Feature Engine mutation baseline. It analyzes the baseline already recorded at
[`feature-engine-mutation-baseline-001.json`](./feature-engine-mutation-baseline-001.json)
(blob `978ebf92f89e5bd93ba112c1b8e4622835ea71ba`). It does **not** modify that
artifact, does not change the raw score, does not remove any mutant (survivor or
otherwise) from the denominator, and does not propose or select a numeric
mutation-effectiveness threshold. That is explicitly deferred to a future,
separately-governed Step-5 transaction.

## 0. Baseline authority (resolved, not restated from memory)

Resolved directly from Testing Convention v0.16 and the durable evidence
artifact at analysis time:

| Field | Value |
|---|---|
| Total mutants | 1531 |
| Killed | 1162 |
| Survived | 369 |
| All other statuses (no_tests, not_checked, skipped, suspicious, timeout, caught_by_type_check, segfault, check_was_interrupted_by_user) | 0 |
| Raw mutation-effectiveness metric (NON-GATING) | 75.898105813194% |
| Sorted mutant-id→result mapping SHA-256 | `d69f0c1902d1c275bdb1db464eacbda35d6b2727fd4c5f5889c5c780add5e244` |

Independently re-verified against the committed evidence JSON at analysis time —
`total_mutants`, `ten_status_counts`, `mutation_score`, `survivor_count`, and the
mapping SHA-256 all match this table exactly. No premise mismatch found.

---

## 1. Survivors — full population analysis (369/369)

### 1.1 Methodology

Every survivor's exact per-mutant source diff was reconstructed **without any
rerun**, from the full mutated source trees (`_mutmut_orig` vs. the specific
`_mutmut_N` variant for each of the 369 `survivor_mutant_ids` recorded in
baseline-001) preserved from the original mutation run. This is possible because
mutmut's own mutated-source copy inlines every mutant variant as a distinct
function body in the same file; no mutation testing was re-executed to produce
this section.

Classification proceeded in two passes:

1. **Structural category** (9 categories) — a token-level diff
   (`difflib.SequenceMatcher` over `\w+|\s+|.` tokens, not raw characters, to
   avoid coincidental single-character alignment artifacts) isolates the exact
   changed span between `_mutmut_orig` and the survivor variant, then classifies
   the span shape (value→`None`, call-argument removal, operator swap, string
   case/marker mutation, control-flow swap, etc.).
2. **Materiality tag** (5 tags) — AST-based, using the real `ast.Raise` /
   capitalized-constructor `ast.Call` / direct attribute-assignment line ranges
   of the **original, unmutated** function body, to determine whether the
   mutated line falls inside an exception message argument (low materiality),
   inside object construction / a stored field (a named, real test-gap
   pattern), is a likely-equivalent codec-case mutation, is an unambiguous
   logic/boundary mutation, or requires individual review.

All 369 survivors were resolved; there is no unclassified remainder in either
pass.

**Important scope note (Testing Convention v0.16 compliance):** none of the
following classifications remove any survivor from the raw denominator. The
`very_likely_equivalent_codec_case_insensitive` tag (3 mutants) is a *candidate*
observation only — per v0.16, an equivalent classification does not have effect
until it satisfies v0.16's individually-pinned justification requirement in a
separate, dedicated review. All 369 remain counted as survivors in the raw
75.898105813194% score.

### 1.2 Structural category counts (369 total)

| Category | Count |
|---|---|
| `value_replaced_with_none` | 183 |
| `string_case_mutation` | 70 |
| `string_literal_marker_mutation` | 59 |
| `call_argument_removed` | 25 |
| `comparison_or_logical_operator_mutation` | 12 |
| `numeric_literal_mutation` | 10 |
| `control_flow_statement_mutation` | 5 |
| `arithmetic_operator_mutation` | 3 |
| `boolean_none_swap` | 2 |

### 1.3 Materiality counts (369 total)

| Materiality tag | Count | Meaning |
|---|---|---|
| `low_materiality_message_text` | 173 | Mutated content falls inside a `raise SomeError(...)` message-text argument. The exception **type** and control-flow effect are unchanged; only textual message content differs. In principle distinguishable by a test asserting on the exact message — so these are real (if low-priority) test gaps, **not** equivalent mutants. |
| `constructed_object_field_not_independently_asserted` | 83 | Mutated content falls inside a capitalized-name constructor call (e.g. building a dataclass/event object) or is a direct `self.x = ...` / `state.x = ...` attribute assignment. The surviving test exercises the code path but never independently asserts the specific field's value. This is the single largest **named, actionable** test-gap pattern found. |
| `needs_review_data_context` | 55 | Not resolved by either AST heuristic (e.g. a local variable mutated in one statement, consumed by a separate statement later — full dataflow tracing was not performed). Requires individual/manual review; not resolved by this automated pass. |
| `actionable_test_gap_candidate` | 55 | Unambiguous logic/boundary mutations: call-argument removal (25), comparison/logical-operator swap (12), numeric-literal change (10), control-flow statement swap (5), arithmetic-operator swap (3). |
| `very_likely_equivalent_codec_case_insensitive` | 3 | Case-only mutation of a string literal used as a codec name in `.decode(...)`/`.encode(...)` (e.g. `"utf-8"` → `"UTF-8"`). Python's standard codec lookup is case-insensitive, so these are very likely — but, per v0.16, only *candidate* — equivalents. **Not removed from the denominator.** |

Cross-tabulation (category × materiality), the 5 largest cells:

| Category | Materiality | Count |
|---|---|---|
| `value_replaced_with_none` | `constructed_object_field_not_independently_asserted` | 79 |
| `string_case_mutation` | `low_materiality_message_text` | 63 |
| `value_replaced_with_none` | `low_materiality_message_text` | 57 |
| `string_literal_marker_mutation` | `low_materiality_message_text` | 53 |
| `value_replaced_with_none` | `needs_review_data_context` | 47 |

### 1.4 Rollup against the task's illustrative 4-bucket scheme

The task's requested categories ("concrete actionable test gap; candidate-equivalent;
duplicated/semantically-related survivor pattern; requires deeper investigation")
are illustrative, not a rigid partition — "duplicated/semantically-related
pattern" is a cross-cutting *function-level* lens, not mutually exclusive with
the others. Mapped onto the finer-grained materiality tags above:

| Bucket | Composition | Count |
|---|---|---|
| Concrete actionable test gap (material) | `constructed_object_field_not_independently_asserted` + `actionable_test_gap_candidate` | 138 |
| Concrete actionable test gap (low-priority, message-text only) | `low_materiality_message_text` | 173 |
| Candidate-equivalent (pending v0.16 individual pinned justification; **0 removed from denominator**) | `very_likely_equivalent_codec_case_insensitive` | 3 |
| Requires deeper investigation | `needs_review_data_context` | 55 |
| **Total** | | **369** |

So: **138 material actionable-test-gap mutants**, **173 low-priority
message-text-only gaps**, **3 candidate-equivalents (unresolved, not removed)**,
**55 requiring individual review**.

### 1.5 Duplicated / semantically-related survivor pattern (function-level)

369 survivors are **not** 369 independent test gaps. Grouping by base function
(module + mutated function/method), **30 functions account for 345 of the 369
survivors (93.5%)** — meaning most of the raw survivor count is concentrated,
repeated exposure of a small number of underlying gaps (typically: a
constructor/builder function whose individual output fields are not
independently asserted by any test that exercises it), not 345 independent
missing-coverage findings.

Top 15 by survivor count:

| Function | Survivors |
|---|---|
| `contracts.x_resolve_computation_cursor` | 35 |
| `contracts.x__seal_verified_authority` | 24 |
| `swing_distance.SwingDistanceFeatureEngine.__init__` | 23 |
| `swing_distance.SwingDistanceFeatureEngine._recompute` | 20 |
| `swing_distance.SwingDistanceFeatureEngine._invalidate_and_replace` | 17 |
| `regime_passthrough.RegimePassthroughFeatureEngine.__init__` | 16 |
| `regime_passthrough.RegimePassthroughFeatureEngine._emit_replacement` | 16 |
| `authority_resolver.x_resolve_input_contract_authority_from_repository` | 15 |
| `swing_distance.SwingDistanceFeatureEngine._preempt_settled_window` | 15 |
| `swing_distance.SwingDistanceFeatureEngine._emit_replacement_only` | 14 |
| `regime_passthrough.RegimePassthroughFeatureEngine._emit_invalidation` | 13 |
| `candle_window.CandleWindowFeatureEngine.__init__` | 12 |
| `current_view.FeatureCurrentView.current` | 12 |
| `swing_distance.SwingDistanceFeatureEngine._invalidate_and_reattempt` | 12 |
| `swing_distance.SwingDistanceFeatureEngine.on_swing_confirmed` | 11 |

The remaining 15 of the 30 functions with ≥3 survivors range from 3–10
survivors each (full list is derivable from the per-mutant table in §1.6 by
grouping on the module/function prefix of the mutant ID).

This pattern is consistent with §1.3's dominant materiality tag: `__init__`
methods and cursor/authority "sealing" functions are exactly where many
individual constructor-field/attribute-assignment mutations concentrate, and
where a single missing "assert every field of the constructed object" test
produces many survivors from one underlying gap.

### 1.6 Per-mutant analysis (repository-resolvable, all 369)

Sorted by materiality, then category, then mutant ID. `Change` is the minimal
token-level diff span (old → new); full unified diffs for every survivor are
reproducible from the durable evidence artifact's `survivor_mutant_ids` plus the
committed source tree — no separate raw-diff artifact is created here (not
inventing a second framework beyond the one JSON + this one markdown).

| Mutant ID (short) | Category | Materiality | Change |
|---|---|---|---|
| `current_view.x__view_ordering_key__mutmut_2` | arithmetic_operator_mutation | actionable_test_gap_candidate | - -> + |
| `swing_distance.x__total_order_key__mutmut_3` | arithmetic_operator_mutation | actionable_test_gap_candidate | - -> + |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_confirmed__mutmut_34` | arithmetic_operator_mutation | actionable_test_gap_candidate | + -> - |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_invalidation__mutmut_6` | call_argument_removed | actionable_test_gap_candidate | argument 'state.head_fact.recorded_time' removed from call |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_invalidation__mutmut_7` | call_argument_removed | actionable_test_gap_candidate | argument 'invalidation.recorded_time' removed from call |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_invalidation__mutmut_8` | call_argument_removed | actionable_test_gap_candidate | argument 'cursor.recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_original__mutmut_12` | call_argument_removed | actionable_test_gap_candidate | argument 'candle.recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_original__mutmut_13` | call_argument_removed | actionable_test_gap_candidate | argument 'state.recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_14` | call_argument_removed | actionable_test_gap_candidate | argument 'invalidation_recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_15` | call_argument_removed | actionable_test_gap_candidate | argument 'candle.recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_16` | call_argument_removed | actionable_test_gap_candidate | argument 'state.recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_17` | call_argument_removed | actionable_test_gap_candidate | argument 'cursor.recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_reattempt__mutmut_5` | call_argument_removed | actionable_test_gap_candidate | argument 'lineage.head_fact.recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_reattempt__mutmut_6` | call_argument_removed | actionable_test_gap_candidate | argument 'correction_recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_reattempt__mutmut_7` | call_argument_removed | actionable_test_gap_candidate | argument 'cursor.recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_5` | call_argument_removed | actionable_test_gap_candidate | argument 'existing.head_fact.recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_6` | call_argument_removed | actionable_test_gap_candidate | argument 'correction_recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_7` | call_argument_removed | actionable_test_gap_candidate | argument 'cursor.recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_19` | call_argument_removed | actionable_test_gap_candidate | argument 'existing.head_fact.recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_20` | call_argument_removed | actionable_test_gap_candidate | argument 'state.recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_21` | call_argument_removed | actionable_test_gap_candidate | argument 'cursor.recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_51` | call_argument_removed | actionable_test_gap_candidate | argument 'key' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_52` | call_argument_removed | actionable_test_gap_candidate | argument 'candle' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_53` | call_argument_removed | actionable_test_gap_candidate | argument 'swing_id' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_54` | call_argument_removed | actionable_test_gap_candidate | argument 'state' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_55` | call_argument_removed | actionable_test_gap_candidate | argument 'existing.pending_invalidation_ref' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_56` | call_argument_removed | actionable_test_gap_candidate | argument 'existing.pending_invalidation_recorded_time' removed from call |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_57` | call_argument_removed | actionable_test_gap_candidate | argument 'cursor' removed from call |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_48` | comparison_or_logical_operator_mutation | actionable_test_gap_candidate | 'or' -> 'and' |
| `contracts.x__seal_verified_authority__mutmut_5` | comparison_or_logical_operator_mutation | actionable_test_gap_candidate | 'or' -> 'and' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_check_scope__mutmut_1` | comparison_or_logical_operator_mutation | actionable_test_gap_candidate | 'or' -> 'and' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_check_candle_recorded_time__mutmut_3` | comparison_or_logical_operator_mutation | actionable_test_gap_candidate | '<' -> '<=' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_check_candle_scope__mutmut_1` | comparison_or_logical_operator_mutation | actionable_test_gap_candidate | 'or' -> 'and' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_23` | comparison_or_logical_operator_mutation | actionable_test_gap_candidate | 'and' -> 'or' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_42` | comparison_or_logical_operator_mutation | actionable_test_gap_candidate | 'is not' -> 'is' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_43` | comparison_or_logical_operator_mutation | actionable_test_gap_candidate | 'is not' -> 'is' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_select_eligible_swing__mutmut_10` | comparison_or_logical_operator_mutation | actionable_test_gap_candidate | '<' -> '<=' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_candle__mutmut_27` | comparison_or_logical_operator_mutation | actionable_test_gap_candidate | '<' -> '<=' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_confirmed__mutmut_2` | comparison_or_logical_operator_mutation | actionable_test_gap_candidate | 'or' -> 'and' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_invalidated__mutmut_8` | comparison_or_logical_operator_mutation | actionable_test_gap_candidate | 'or' -> 'and' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_reevaluate_all_windows__mutmut_13` | control_flow_statement_mutation | actionable_test_gap_candidate | continue -> break |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_reevaluate_all_windows__mutmut_32` | control_flow_statement_mutation | actionable_test_gap_candidate | continue -> break |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_reevaluate_all_windows__mutmut_37` | control_flow_statement_mutation | actionable_test_gap_candidate | continue -> break |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_reevaluate_all_windows__mutmut_6` | control_flow_statement_mutation | actionable_test_gap_candidate | continue -> break |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_invalidated__mutmut_29` | control_flow_statement_mutation | actionable_test_gap_candidate | continue -> break |
| `current_view.xǁFeatureCurrentViewǁcurrent__mutmut_15` | numeric_literal_mutation | actionable_test_gap_candidate | 0 -> 1 |
| `current_view.xǁFeatureCurrentViewǁon_feature_computed__mutmut_19` | numeric_literal_mutation | actionable_test_gap_candidate | 0 -> 1 |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_original__mutmut_46` | numeric_literal_mutation | actionable_test_gap_candidate | 0 -> 1 |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_49` | numeric_literal_mutation | actionable_test_gap_candidate | 0 -> 1 |
| `swing_distance.x__total_order_key__mutmut_2` | numeric_literal_mutation | actionable_test_gap_candidate | 0 -> 1 |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_normalize_evidence__mutmut_4` | numeric_literal_mutation | actionable_test_gap_candidate | 0 -> 1 |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_select_eligible_swing__mutmut_22` | numeric_literal_mutation | actionable_test_gap_candidate | 0 -> 1 |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_select_eligible_swing__mutmut_9` | numeric_literal_mutation | actionable_test_gap_candidate | 0 -> 1 |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_candle__mutmut_37` | numeric_literal_mutation | actionable_test_gap_candidate | 1 -> 2 |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_confirmed__mutmut_35` | numeric_literal_mutation | actionable_test_gap_candidate | 1 -> 2 |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_invalidation__mutmut_35` | string_case_mutation | constructed_object_field_not_independently_asserted | 'regime_fact_invalidated' -> 'REGIME_FACT_INVALIDATED' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_32` | string_case_mutation | constructed_object_field_not_independently_asserted | 'candle_corrected' -> 'CANDLE_CORRECTED' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_invalidation__mutmut_34` | string_literal_marker_mutation | constructed_object_field_not_independently_asserted | 'regime_fact_invalidated' -> 'XXregime_fact_invalidatedXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_31` | string_literal_marker_mutation | constructed_object_field_not_independently_asserted | 'candle_corrected' -> 'XXcandle_correctedXX' |
| `contracts.x_resolve_output_contract_refs__mutmut_12` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'FEATURE_FACT_INVALIDATED_CONTRACT_ID' -> 'None' |
| `contracts.x_resolve_output_contract_refs__mutmut_13` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'feature_event_contract_version' -> 'None' |
| `contracts.x_resolve_output_contract_refs__mutmut_8` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'FEATURE_COMPUTED_CONTRACT_ID' -> 'None' |
| `contracts.x_resolve_output_contract_refs__mutmut_9` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'feature_event_contract_version' -> 'None' |
| `current_view.xǁFeatureCurrentViewǁcurrent__mutmut_20` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'feature_subject_id=feature_subject_id,' -> 'feature_subject_id=None,' |
| `current_view.xǁFeatureCurrentViewǁcurrent__mutmut_21` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'scope=self.scope,' -> 'scope=None,' |
| `current_view.xǁFeatureCurrentViewǁcurrent__mutmut_24` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'unit=fact.unit,' -> 'unit=None,' |
| `current_view.xǁFeatureCurrentViewǁcurrent__mutmut_25` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'effective_window=EffectiveWindow(fact.window_start, fact.window_end),' -> 'effective_w... |
| `current_view.xǁFeatureCurrentViewǁcurrent__mutmut_27` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'last_recorded_time=state.last_recorded_time,' -> 'last_recorded_time=None,' |
| `current_view.xǁFeatureCurrentViewǁcurrent__mutmut_38` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'fact.window_start' -> 'None' |
| `current_view.xǁFeatureCurrentViewǁcurrent__mutmut_39` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'fact.window_end' -> 'None' |
| `current_view.xǁFeatureCurrentViewǁcurrent__mutmut_42` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'feature_subject_id=feature_subject_id,' -> 'feature_subject_id=None,' |
| `current_view.xǁFeatureCurrentViewǁcurrent__mutmut_43` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'scope=self.scope,' -> 'scope=None,' |
| `current_view.xǁFeatureCurrentViewǁcurrent__mutmut_45` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'last_recorded_time=state.last_recorded_time,' -> 'last_recorded_time=None,' |
| `current_view.xǁFeatureCurrentViewǁon_feature_computed__mutmut_29` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'state.invalidated = False' -> 'state.invalidated = None' |
| `current_view.xǁFeatureCurrentViewǁon_feature_computed__mutmut_31` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'state.last_recorded_time = event.recorded_time' -> 'state.last_recorded_time = None' |
| `current_view.xǁFeatureCurrentViewǁon_feature_invalidated__mutmut_12` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'state.last_recorded_time = event.recorded_time' -> 'state.last_recorded_time = None' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_39` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'self._stream_id = stream_id' -> 'self._stream_id = None' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_invalidation__mutmut_14` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'scope=state.head_fact.scope,' -> 'scope=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_invalidation__mutmut_16` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'invalidation_cause="regime_fact_invalidated",' -> 'invalidation_cause=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_invalidation__mutmut_17` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'window_start=state.head_fact.window_start,' -> 'window_start=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_invalidation__mutmut_18` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'window_end=state.head_fact.window_end,' -> 'window_end=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_invalidation__mutmut_19` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'causation_refs=(state.head_fact.ref, invalidation.ref),' -> 'causation_refs=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_invalidation__mutmut_21` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'ref=ref,' -> 'ref=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_invalidation__mutmut_22` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'event_contract_ref=self._invalidation_contract_ref,' -> 'event_contract_ref=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_original__mutmut_23` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'scope=self.scope,' -> 'scope=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_original__mutmut_25` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'unit=self.definition.unit,' -> 'unit=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_original__mutmut_27` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'window_end=key[1],' -> 'window_end=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_original__mutmut_29` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'causation_refs=normalized_refs,' -> 'causation_refs=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_original__mutmut_32` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'event_contract_ref=self._output_contract_ref,' -> 'event_contract_ref=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_original__mutmut_48` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'self._stream_id' -> 'None' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_25` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'scope=self.scope,' -> 'scope=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_27` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'unit=self.definition.unit,' -> 'unit=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_28` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'window_start=key[0],' -> 'window_start=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_29` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'window_end=key[1],' -> 'window_end=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_30` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'input_fact_refs=normalized_refs,' -> 'input_fact_refs=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_32` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'causation_refs=(*normalized_refs, existing.pending_invalidation_ref),' -> 'causation_r... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_34` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'ref=self._allocator.next_ref(self._stream_id),' -> 'ref=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_35` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'event_contract_ref=self._output_contract_ref,' -> 'event_contract_ref=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_36` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'computation_cursor=self._resolve_cursor(cursor),' -> 'computation_cursor=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_51` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'self._stream_id' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_59` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'self._stream_id = stream_id' -> 'self._stream_id = None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_original__mutmut_23` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'scope=self.scope,' -> 'scope=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_original__mutmut_25` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'unit=self.definition.unit,' -> 'unit=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_original__mutmut_29` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'causation_refs=normalized_refs,' -> 'causation_refs=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_original__mutmut_31` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'ref=self._allocator.next_ref(self._stream_id),' -> 'ref=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_original__mutmut_32` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'event_contract_ref=self._output_contract_ref,' -> 'event_contract_ref=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_original__mutmut_48` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'self._stream_id' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_26` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'scope=self.scope,' -> 'scope=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_28` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'unit=self.definition.unit,' -> 'unit=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_31` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'input_fact_refs=normalized_refs,' -> 'input_fact_refs=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_33` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'causation_refs=(*normalized_refs, invalidation_ref),' -> 'causation_refs=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_35` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'ref=self._allocator.next_ref(self._stream_id),' -> 'ref=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_36` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'event_contract_ref=self._output_contract_ref,' -> 'event_contract_ref=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_52` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'self._stream_id' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_reattempt__mutmut_11` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'scope=lineage.head_fact.scope,' -> 'scope=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_reattempt__mutmut_15` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'window_end=lineage.head_fact.window_end,' -> 'window_end=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_reattempt__mutmut_16` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'causation_refs=(lineage.head_fact.ref, correction_ref),' -> 'causation_refs=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_reattempt__mutmut_17` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'recorded_time=invalidation_recorded_time,' -> 'recorded_time=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_reattempt__mutmut_19` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'event_contract_ref=self._invalidation_contract_ref,' -> 'event_contract_ref=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_reattempt__mutmut_20` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'computation_cursor=self._resolve_cursor(cursor),' -> 'computation_cursor=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_reattempt__mutmut_33` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'self._stream_id' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_11` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'scope=existing.head_fact.scope,' -> 'scope=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_12` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'invalidated_fact_ref=existing.head_fact.ref,' -> 'invalidated_fact_ref=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_13` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'invalidation_cause="candle_corrected",' -> 'invalidation_cause=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_14` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'window_start=existing.head_fact.window_start,' -> 'window_start=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_15` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'window_end=existing.head_fact.window_end,' -> 'window_end=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_16` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'causation_refs=(existing.head_fact.ref, correction_ref),' -> 'causation_refs=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_17` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'recorded_time=invalidation_recorded_time,' -> 'recorded_time=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_18` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'ref=self._allocator.next_ref(self._stream_id),' -> 'ref=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_19` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'event_contract_ref=self._invalidation_contract_ref,' -> 'event_contract_ref=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_33` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'self._stream_id' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_25` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'scope=existing.head_fact.scope,' -> 'scope=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_28` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'window_start=existing.head_fact.window_start,' -> 'window_start=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_29` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'window_end=existing.head_fact.window_end,' -> 'window_end=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_31` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'recorded_time=invalidation_recorded_time,' -> 'recorded_time=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_32` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'ref=self._allocator.next_ref(self._stream_id),' -> 'ref=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_33` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'event_contract_ref=self._invalidation_contract_ref,' -> 'event_contract_ref=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_47` | value_replaced_with_none | constructed_object_field_not_independently_asserted | 'self._stream_id' -> 'None' |
| `authority_resolver.x__find_repo_root__mutmut_4` | string_case_mutation | low_materiality_message_text | 'InputContractStreamRegistry' -> 'inputcontractstreamregistry' |
| `authority_resolver.x__find_repo_root__mutmut_5` | string_case_mutation | low_materiality_message_text | 'InputContractStreamRegistryauthoritycannotberesolvedfromthefilesystem' -> 'INPUTCONTRA... |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_56` | string_case_mutation | low_materiality_message_text | 'contract_idcontract_versionstream_registry_versionincluded_streamsidentity' -> 'CONTRA... |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_71` | string_case_mutation | low_materiality_message_text | 'registry_versionstream_idsetidentity' -> 'REGISTRY_VERSIONSTREAM_IDSETIDENTITY' |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_75` | string_case_mutation | low_materiality_message_text | 'ruleauthorityresolutionfailureneverresolvedbyselectingadifferentregistryversion' -> 'R... |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_81` | string_case_mutation | low_materiality_message_text | 'streamsthatgenuinelyexistinitsownpinnedregistry' -> 'STREAMSTHATGENUINELYEXISTINITSOWN... |
| `candle_window.xǁCandleWindowFeatureEngineǁ__init____mutmut_12` | string_case_mutation | low_materiality_message_text | 'CandleWindowFeatureEngine' -> 'candlewindowfeatureengine' |
| `candle_window.xǁCandleWindowFeatureEngineǁ__init____mutmut_22` | string_case_mutation | low_materiality_message_text | 'Candle' -> 'candle' |
| `candle_window.xǁCandleWindowFeatureEngineǁ__init____mutmut_23` | string_case_mutation | low_materiality_message_text | 'Candlederivedformulacomputationisnotauthorizednocurrentrepositoryauthoritypinsan' -> '... |
| `candle_window.xǁCandleWindowFeatureEngineǁ__init____mutmut_25` | string_case_mutation | low_materiality_message_text | 'featuremdthisengineneverexecutesacallersuppliedformulamatchedonlybya' -> 'FEATUREMDTHI... |
| `candle_window.xǁCandleWindowFeatureEngineǁ__init____mutmut_27` | string_case_mutation | low_materiality_message_text | 'FailsP3FEATUREAMAJ' -> 'failsp3featureamaj' |
| `candle_window.xǁCandleWindowFeatureEngineǁ__init____mutmut_28` | string_case_mutation | low_materiality_message_text | 'formula_idstringFailsclosedper' -> 'FORMULA_IDSTRINGFAILSCLOSEDPER' |
| `contracts.x__seal_verified_authority__mutmut_10` | string_case_mutation | low_materiality_message_text | 'input_contract_refmustbeagenuinenonemptycontract_idcontract_versionidentity' -> 'INPUT... |
| `contracts.x__seal_verified_authority__mutmut_14` | string_case_mutation | low_materiality_message_text | 'stream_registry_versionmustbeagenuinenonemptyregistryversionidentity' -> 'STREAM_REGIS... |
| `contracts.x__seal_verified_authority__mutmut_18` | string_case_mutation | low_materiality_message_text | 'included_streamsmustbeagenuinenonemptyset' -> 'INCLUDED_STREAMSMUSTBEAGENUINENONEMPTYSET' |
| `contracts.x__seal_verified_authority__mutmut_23` | string_case_mutation | low_materiality_message_text | 'digestlowercasehexcharactersanonemptybutfabricatedarbitrarystringisnever' -> 'DIGESTLO... |
| `contracts.x__seal_verified_authority__mutmut_25` | string_case_mutation | low_materiality_message_text | 'sufficientcontentidentityproof' -> 'SUFFICIENTCONTENTIDENTITYPROOF' |
| `contracts.x__seal_verified_authority__mutmut_30` | string_case_mutation | low_materiality_message_text | 'digestlowercasehexcharactersanonemptybutfabricatedarbitrarystringisnever' -> 'DIGESTLO... |
| `contracts.x__seal_verified_authority__mutmut_32` | string_case_mutation | low_materiality_message_text | 'sufficientcontentidentityproof' -> 'SUFFICIENTCONTENTIDENTITYPROOF' |
| `contracts.x__seal_verified_authority__mutmut_4` | string_case_mutation | low_materiality_message_text | 'feature_computation_profilemustbegenuineandnonempty' -> 'FEATURE_COMPUTATION_PROFILEMU... |
| `contracts.x_resolve_computation_cursor__mutmut_14` | string_case_mutation | low_materiality_message_text | 'ADR' -> 'adr' |
| `contracts.x_resolve_computation_cursor__mutmut_15` | string_case_mutation | low_materiality_message_text | 'scardinalityclausenomissingstreamnoextrastreamneveranallstreamsseen' -> 'SCARDINALITYC... |
| `contracts.x_resolve_computation_cursor__mutmut_17` | string_case_mutation | low_materiality_message_text | 'fallback' -> 'FALLBACK' |
| `contracts.x_resolve_computation_cursor__mutmut_23` | string_case_mutation | low_materiality_message_text | 'ReviewA' -> 'reviewa' |
| `contracts.x_resolve_computation_cursor__mutmut_24` | string_case_mutation | low_materiality_message_text | 'callerprovidedintegerpositionaloneisnotproofReviewresidual' -> 'CALLERPROVIDEDINTEGERP... |
| `contracts.x_resolve_computation_cursor__mutmut_30` | string_case_mutation | low_materiality_message_text | 'ChapterPositionCursor' -> 'chapterpositioncursor' |
| `contracts.x_resolve_computation_cursor__mutmut_31` | string_case_mutation | low_materiality_message_text | 'ChapterPositionCursorinvariantviolatedantilookahead' -> 'CHAPTERPOSITIONCURSORINVARIAN... |
| `contracts.x_resolve_computation_cursor__mutmut_4` | string_case_mutation | low_materiality_message_text | 'InputContractChapter' -> 'inputcontractchapter' |
| `contracts.x_resolve_computation_cursor__mutmut_41` | string_case_mutation | low_materiality_message_text | 'lifecycle_frontierpositionkindeventrequiresaresolvedevent_recorded_timeproof' -> 'LIFE... |
| `contracts.x_resolve_computation_cursor__mutmut_43` | string_case_mutation | low_materiality_message_text | 'nonewassupplied' -> 'NONEWASSUPPLIED' |
| `contracts.x_resolve_computation_cursor__mutmut_47` | string_case_mutation | low_materiality_message_text | 'invariantviolated' -> 'INVARIANTVIOLATED' |
| `contracts.x_resolve_computation_cursor__mutmut_5` | string_case_mutation | low_materiality_message_text | 'thisInputContractinstanceisnotapplicableatthecallerscertifiedfrontierChapter' -> 'THIS... |
| `contracts.x_resolve_computation_cursor__mutmut_51` | string_case_mutation | low_materiality_message_text | 'lifecycle_frontierpositionkindgenesismustnotcarryafabricatedevent_recorded_time' -> 'L... |
| `contracts.x_resolve_computation_cursor__mutmut_53` | string_case_mutation | low_materiality_message_text | 'ChapterGenesis' -> 'chaptergenesis' |
| `contracts.x_resolve_computation_cursor__mutmut_54` | string_case_mutation | low_materiality_message_text | 'ChaptersGenesiscarveoutmeansnolifecycleeventexistsyettoprove' -> 'CHAPTERSGENESISCARVE... |
| `contracts.x_resolve_computation_cursor__mutmut_7` | string_case_mutation | low_materiality_message_text | 'exactpinfailsclosedratherthansilentlyrebasingthecursorontoadifferentregistry' -> 'EXAC... |
| `contracts.x_resolve_output_contract_refs__mutmut_4` | string_case_mutation | low_materiality_message_text | 'feature_event_contract_versionmustbeagenuinenonemptycontractversionidentity' -> 'FEATU... |
| `contracts.x_resolve_output_contract_refs__mutmut_6` | string_case_mutation | low_materiality_message_text | 'FeatureP3FEATUREAMAJ' -> 'featurep3featureamaj' |
| `contracts.x_resolve_output_contract_refs__mutmut_7` | string_case_mutation | low_materiality_message_text | 'nostandinvalueisinventedforFeaturesownoutboundevent_contract_ref' -> 'NOSTANDINVALUEIS... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_10` | string_case_mutation | low_materiality_message_text | 'RegimePassthroughFeatureEngine' -> 'regimepassthroughfeatureengine' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_26` | string_case_mutation | low_materiality_message_text | 'aproviderisnevertrustedmerelybecauseitreturnedanobjectwithplausiblelooking' -> 'APROVI... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_28` | string_case_mutation | low_materiality_message_text | 'ReviewA' -> 'reviewa' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_29` | string_case_mutation | low_materiality_message_text | 'fieldsReviewroundunresolvedplaindataisneveracceptedasifitwereverified' -> 'FIELDSREVIE... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_33` | string_case_mutation | low_materiality_message_text | 'providerisnevertrustedmerelybecauseitotherwisereturnedawellformedobject' -> 'PROVIDERI... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_check_scope__mutmut_8` | string_case_mutation | low_materiality_message_text | 'Feature' -> 'feature' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_check_scope__mutmut_9` | string_case_mutation | low_materiality_message_text | 'regimefactscopedoesnotmatchthisFeatureenginesownscope' -> 'REGIMEFACTSCOPEDOESNOTMATCH... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁon_regime_classified__mutmut_30` | string_case_mutation | low_materiality_message_text | 'RegimeFactInvalidated' -> 'regimefactinvalidated' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁon_regime_classified__mutmut_31` | string_case_mutation | low_materiality_message_text | 'pendingcorrectionareplacementmustbeprecededbyRegimeFactInvalidated' -> 'PENDINGCORRECT... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁon_regime_invalidated__mutmut_13` | string_case_mutation | low_materiality_message_text | 'evidenceforanynoninvalidatedwindowinthisengine' -> 'EVIDENCEFORANYNONINVALIDATEDWINDOW... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_18` | string_case_mutation | low_materiality_message_text | 'distance_representationsignedhasnoauthoritativesignorientationconventionpinned' -> 'DI... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_20` | string_case_mutation | low_materiality_message_text | 'anywhereinfeaturemdthisenginedoesnotinventoneonly' -> 'ANYWHEREINFEATUREMDTHISENGINEDO... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_22` | string_case_mutation | low_materiality_message_text | 'distance_representationabsoluteiscurrentlycomputable' -> 'DISTANCE_REPRESENTATIONABSOL... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_45` | string_case_mutation | low_materiality_message_text | 'aproviderisnevertrustedmerelybecauseitreturnedanobjectwithplausiblelooking' -> 'APROVI... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_47` | string_case_mutation | low_materiality_message_text | 'ReviewA' -> 'reviewa' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_48` | string_case_mutation | low_materiality_message_text | 'fieldsReviewroundunresolvedplaindataisneveracceptedasifitwereverified' -> 'FIELDSREVIE... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_52` | string_case_mutation | low_materiality_message_text | 'providerisnevertrustedmerelybecauseitotherwisereturnedawellformedobject' -> 'PROVIDERI... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_check_candle_contract__mutmut_8` | string_case_mutation | low_materiality_message_text | 'P3FEATUREAMAJ' -> 'p3featureamaj' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_check_candle_contract__mutmut_9` | string_case_mutation | low_materiality_message_text | 'matchingisinsufficient' -> 'MATCHINGISINSUFFICIENT' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_check_swing_contract__mutmut_8` | string_case_mutation | low_materiality_message_text | 'P3FEATUREAMAJ' -> 'p3featureamaj' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_check_swing_contract__mutmut_9` | string_case_mutation | low_materiality_message_text | 'insufficient' -> 'INSUFFICIENT' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_14` | string_case_mutation | low_materiality_message_text | 'eligible_swing_selection_superseded' -> 'ELIGIBLE_SWING_SELECTION_SUPERSEDED' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_confirmed__mutmut_10` | string_case_mutation | low_materiality_message_text | 'SwingConfirmedscopedoesnotmatchthisFeatureenginesownscope' -> 'SWINGCONFIRMEDSCOPEDOES... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_confirmed__mutmut_9` | string_case_mutation | low_materiality_message_text | 'SwingConfirmedFeature' -> 'swingconfirmedfeature' |
| `authority_resolver.x__find_repo_root__mutmut_3` | string_literal_marker_mutation | low_materiality_message_text | 'Inputfilesystem' -> 'XXInputfilesystemXX' |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_55` | string_literal_marker_mutation | low_materiality_message_text | 'identity' -> 'XXidentityXX' |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_70` | string_literal_marker_mutation | low_materiality_message_text | 'identity' -> 'XXidentityXX' |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_74` | string_literal_marker_mutation | low_materiality_message_text | 'ruleversion' -> 'XXruleversionXX' |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_80` | string_literal_marker_mutation | low_materiality_message_text | 'streamsregistry' -> 'XXstreamsregistryXX' |
| `candle_window.xǁCandleWindowFeatureEngineǁ__init____mutmut_11` | string_literal_marker_mutation | low_materiality_message_text | 'CandleWindowFeatureEngine' -> 'XXCandleWindowFeatureEngineXX' |
| `candle_window.xǁCandleWindowFeatureEngineǁ__init____mutmut_18` | string_literal_marker_mutation | low_materiality_message_text | 'scopedefinition' -> 'XXscopedefinitionXX' |
| `candle_window.xǁCandleWindowFeatureEngineǁ__init____mutmut_21` | string_literal_marker_mutation | low_materiality_message_text | 'Candle' -> 'XXCandleXX' |
| `candle_window.xǁCandleWindowFeatureEngineǁ__init____mutmut_24` | string_literal_marker_mutation | low_materiality_message_text | '' -> 'XXXX' |
| `candle_window.xǁCandleWindowFeatureEngineǁ__init____mutmut_26` | string_literal_marker_mutation | low_materiality_message_text | 'formula_id' -> 'XXformula_idXX' |
| `contracts.x__seal_verified_authority__mutmut_13` | string_literal_marker_mutation | low_materiality_message_text | 'stream_registry_versionidentity' -> 'XXstream_registry_versionidentityXX' |
| `contracts.x__seal_verified_authority__mutmut_17` | string_literal_marker_mutation | low_materiality_message_text | 'included_streamsset' -> 'XXincluded_streamssetXX' |
| `contracts.x__seal_verified_authority__mutmut_22` | string_literal_marker_mutation | low_materiality_message_text | 'digest' -> 'XXdigestXX' |
| `contracts.x__seal_verified_authority__mutmut_24` | string_literal_marker_mutation | low_materiality_message_text | 'sufficientproof' -> 'XXsufficientproofXX' |
| `contracts.x__seal_verified_authority__mutmut_29` | string_literal_marker_mutation | low_materiality_message_text | 'digest' -> 'XXdigestXX' |
| `contracts.x__seal_verified_authority__mutmut_3` | string_literal_marker_mutation | low_materiality_message_text | 'feature_computation_profileempty' -> 'XXfeature_computation_profileemptyXX' |
| `contracts.x__seal_verified_authority__mutmut_31` | string_literal_marker_mutation | low_materiality_message_text | 'sufficientproof' -> 'XXsufficientproofXX' |
| `contracts.x__seal_verified_authority__mutmut_9` | string_literal_marker_mutation | low_materiality_message_text | 'input_contract_refidentity' -> 'XXinput_contract_refidentityXX' |
| `contracts.x_resolve_computation_cursor__mutmut_13` | string_literal_marker_mutation | low_materiality_message_text | '' -> 'XXXX' |
| `contracts.x_resolve_computation_cursor__mutmut_16` | string_literal_marker_mutation | low_materiality_message_text | 'fallback' -> 'XXfallbackXX' |
| `contracts.x_resolve_computation_cursor__mutmut_22` | string_literal_marker_mutation | low_materiality_message_text | 'caller' -> 'XXcallerXX' |
| `contracts.x_resolve_computation_cursor__mutmut_29` | string_literal_marker_mutation | low_materiality_message_text | 'Chapter' -> 'XXChapterXX' |
| `contracts.x_resolve_computation_cursor__mutmut_3` | string_literal_marker_mutation | low_materiality_message_text | 'this' -> 'XXthisXX' |
| `contracts.x_resolve_computation_cursor__mutmut_40` | string_literal_marker_mutation | low_materiality_message_text | 'lifecycle_frontier' -> 'XXlifecycle_frontierXX' |
| `contracts.x_resolve_computation_cursor__mutmut_42` | string_literal_marker_mutation | low_materiality_message_text | 'nonesupplied' -> 'XXnonesuppliedXX' |
| `contracts.x_resolve_computation_cursor__mutmut_46` | string_literal_marker_mutation | low_materiality_message_text | 'invariantviolated' -> 'XXinvariantviolatedXX' |
| `contracts.x_resolve_computation_cursor__mutmut_50` | string_literal_marker_mutation | low_materiality_message_text | 'lifecycle_frontier' -> 'XXlifecycle_frontierXX' |
| `contracts.x_resolve_computation_cursor__mutmut_52` | string_literal_marker_mutation | low_materiality_message_text | 'Chapterprove' -> 'XXChapterproveXX' |
| `contracts.x_resolve_computation_cursor__mutmut_6` | string_literal_marker_mutation | low_materiality_message_text | 'exactregistry' -> 'XXexactregistryXX' |
| `contracts.x_resolve_output_contract_refs__mutmut_3` | string_literal_marker_mutation | low_materiality_message_text | 'feature_event_contract_version' -> 'XXfeature_event_contract_versionXX' |
| `contracts.x_resolve_output_contract_refs__mutmut_5` | string_literal_marker_mutation | low_materiality_message_text | 'no' -> 'XXnoXX' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_16` | string_literal_marker_mutation | low_materiality_message_text | 'scopedefinition' -> 'XXscopedefinitionXX' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_25` | string_literal_marker_mutation | low_materiality_message_text | '' -> 'XXXX' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_27` | string_literal_marker_mutation | low_materiality_message_text | 'fieldsverified' -> 'XXfieldsverifiedXX' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_32` | string_literal_marker_mutation | low_materiality_message_text | 'providerobject' -> 'XXproviderobjectXX' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_9` | string_literal_marker_mutation | low_materiality_message_text | 'RegimePassthroughFeatureEngine' -> 'XXRegimePassthroughFeatureEngineXX' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_check_scope__mutmut_7` | string_literal_marker_mutation | low_materiality_message_text | 'regimescope' -> 'XXregimescopeXX' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁon_regime_classified__mutmut_29` | string_literal_marker_mutation | low_materiality_message_text | 'pendingRegimeFactInvalidated' -> 'XXpendingRegimeFactInvalidatedXX' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁon_regime_invalidated__mutmut_12` | string_literal_marker_mutation | low_materiality_message_text | 'evidenceengine' -> 'XXevidenceengineXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_11` | string_literal_marker_mutation | low_materiality_message_text | 'scopedefinition' -> 'XXscopedefinitionXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_17` | string_literal_marker_mutation | low_materiality_message_text | 'distance_representation' -> 'XXdistance_representationXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_19` | string_literal_marker_mutation | low_materiality_message_text | 'anywhere' -> 'XXanywhereXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_21` | string_literal_marker_mutation | low_materiality_message_text | 'distance_representationcomputable' -> 'XXdistance_representationcomputableXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_25` | string_literal_marker_mutation | low_materiality_message_text | 'authorized_candle_contract_refsempty' -> 'XXauthorized_candle_contract_refsemptyXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_32` | string_literal_marker_mutation | low_materiality_message_text | 'authorized_swing_contract_refsempty' -> 'XXauthorized_swing_contract_refsemptyXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_44` | string_literal_marker_mutation | low_materiality_message_text | '' -> 'XXXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_46` | string_literal_marker_mutation | low_materiality_message_text | 'fieldsverified' -> 'XXfieldsverifiedXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_51` | string_literal_marker_mutation | low_materiality_message_text | 'providerobject' -> 'XXproviderobjectXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_check_candle_contract__mutmut_7` | string_literal_marker_mutation | low_materiality_message_text | 'matching' -> 'XXmatchingXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_check_swing_contract__mutmut_7` | string_literal_marker_mutation | low_materiality_message_text | 'insufficient' -> 'XXinsufficientXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_13` | string_literal_marker_mutation | low_materiality_message_text | 'eligible_swing_selection_superseded' -> 'XXeligible_swing_selection_supersededXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_confirmed__mutmut_8` | string_literal_marker_mutation | low_materiality_message_text | 'SwingConfirmedscope' -> 'XXSwingConfirmedscopeXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_invalidated__mutmut_13` | string_literal_marker_mutation | low_materiality_message_text | 'notengine' -> 'XXnotengineXX' |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_11` | value_replaced_with_none | low_materiality_message_text | 'f"Feature-scoped Input Contract artifact not found at {contract_path!r} — cannot resol... |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_13` | value_replaced_with_none | low_materiality_message_text | 'f"Stream Registry artifact not found at {registry_path!r} — cannot resolve authority"'... |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_73` | value_replaced_with_none | low_materiality_message_text | 'f"Input Contract at {contract_path!r} declares stream_registry_version={stream_registr... |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_78` | value_replaced_with_none | low_materiality_message_text | 'f"Input Contract at {contract_path!r} declares included_streams containing " f"{sorted... |
| `candle_window.xǁCandleWindowFeatureEngineǁ__init____mutmut_20` | value_replaced_with_none | low_materiality_message_text | '"Candle-derived formula computation is not authorized: no current repository authority... |
| `contracts.x__seal_verified_authority__mutmut_12` | value_replaced_with_none | low_materiality_message_text | '"stream_registry_version must be a genuine, non-empty registry version identity"' -> '... |
| `contracts.x__seal_verified_authority__mutmut_16` | value_replaced_with_none | low_materiality_message_text | 'raise UnresolvedComputationCursorAuthorityError("included_streams must be a genuine, n... |
| `contracts.x__seal_verified_authority__mutmut_2` | value_replaced_with_none | low_materiality_message_text | 'raise UnresolvedComputationCursorAuthorityError("feature_computation_profile must be g... |
| `contracts.x__seal_verified_authority__mutmut_21` | value_replaced_with_none | low_materiality_message_text | 'f"input_contract_content_id={input_contract_content_id!r} is not a well-formed content... |
| `contracts.x__seal_verified_authority__mutmut_28` | value_replaced_with_none | low_materiality_message_text | 'f"stream_registry_content_id={stream_registry_content_id!r} is not a well-formed conte... |
| `contracts.x__seal_verified_authority__mutmut_8` | value_replaced_with_none | low_materiality_message_text | '"input_contract_ref must be a genuine, non-empty {contract_id, contract_version} ident... |
| `contracts.x_normalize_input_facts__mutmut_21` | value_replaced_with_none | low_materiality_message_text | 'f"normalized evidence has {len(ordered)} unique ref(s), expected exactly {expected_cou... |
| `contracts.x_normalize_input_facts__mutmut_9` | value_replaced_with_none | low_materiality_message_text | 'f"ref {ref!r} resolves to conflicting fact content ({existing!r} vs {fact!r})"' -> 'None' |
| `contracts.x_resolve_computation_cursor__mutmut_10` | value_replaced_with_none | low_materiality_message_text | 'f"frontier.stream_positions keys {sorted(frontier.stream_positions.keys())!r} do not e... |
| `contracts.x_resolve_computation_cursor__mutmut_2` | value_replaced_with_none | low_materiality_message_text | 'f"frontier.stream_registry_version={frontier.stream_registry_version!r} does not match... |
| `contracts.x_resolve_computation_cursor__mutmut_21` | value_replaced_with_none | low_materiality_message_text | 'f"stream_positions[{stream_id!r}] references sequence {proof.sequence!r} (not that str... |
| `contracts.x_resolve_computation_cursor__mutmut_28` | value_replaced_with_none | low_materiality_message_text | 'f"stream_positions[{stream_id!r}] resolves to an event recorded at " f"{proof.event_re... |
| `contracts.x_resolve_computation_cursor__mutmut_33` | value_replaced_with_none | low_materiality_message_text | 'f"lifecycle_frontier.stream_id={frontier.lifecycle_frontier.stream_id!r} is not the ca... |
| `contracts.x_resolve_computation_cursor__mutmut_39` | value_replaced_with_none | low_materiality_message_text | '"lifecycle_frontier.position.kind == \'event\' requires a resolved event_recorded_time... |
| `contracts.x_resolve_computation_cursor__mutmut_45` | value_replaced_with_none | low_materiality_message_text | 'f"lifecycle_frontier\'s resolved event recorded_time {proof_time!r} is AFTER " f"curso... |
| `contracts.x_resolve_computation_cursor__mutmut_49` | value_replaced_with_none | low_materiality_message_text | '"lifecycle_frontier.position.kind == \'genesis\' must not carry a fabricated event_rec... |
| `contracts.x_resolve_output_contract_refs__mutmut_2` | value_replaced_with_none | low_materiality_message_text | '"feature_event_contract_version must be a genuine, non-empty contract-version identity... |
| `current_view.xǁFeatureCurrentViewǁ_check_scope__mutmut_2` | value_replaced_with_none | low_materiality_message_text | 'raise ForeignScopeError(f"event scope {event_scope!r} does not match view scope {self.... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_23` | value_replaced_with_none | low_materiality_message_text | 'f"input_contract_authority_provider.resolve({_REQUIRED_INPUT_CONTRACT_PROFILE!r}) retu... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_24` | value_replaced_with_none | low_materiality_message_text | 'self._resolved_input_contract' -> 'None' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_31` | value_replaced_with_none | low_materiality_message_text | 'f"input_contract_authority_provider.resolve({_REQUIRED_INPUT_CONTRACT_PROFILE!r}) retu... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_check_contract__mutmut_3` | value_replaced_with_none | low_materiality_message_text | 'f"regime fact event_contract_ref={event_contract_ref!r} is not one of " f"definition.u... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_check_recorded_time__mutmut_4` | value_replaced_with_none | low_materiality_message_text | 'f"recorded_time {recorded_time!r} precedes last-seen {self._last_input_recorded_time!r... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_check_scope__mutmut_6` | value_replaced_with_none | low_materiality_message_text | 'raise ForeignScopeError("regime fact scope does not match this Feature engine\'s own s... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_next_recorded_time__mutmut_5` | value_replaced_with_none | low_materiality_message_text | 'f"RecordedTimeSource.next_after({strict_floor!r}) returned {candidate!r}, not strictly... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁon_regime_classified__mutmut_10` | value_replaced_with_none | low_materiality_message_text | 'f"expected regime_dimension={self._expected_dimension!r}, got {fact.regime_dimension!r... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁon_regime_classified__mutmut_12` | value_replaced_with_none | low_materiality_message_text | 'f"expected regime_definition_version={self.definition.required_upstream_definition_ver... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁon_regime_classified__mutmut_27` | value_replaced_with_none | low_materiality_message_text | 'f"ref {fact.ref!r} resolves to conflicting RegimeClassified content " f"({existing.las... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁon_regime_classified__mutmut_28` | value_replaced_with_none | low_materiality_message_text | 'f"received a new RegimeClassified for window {key!r} whose current lineage head is not... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁon_regime_invalidated__mutmut_11` | value_replaced_with_none | low_materiality_message_text | 'f"RegimeFactInvalidated targets {invalidation.invalidated_fact_ref!r}, which is not th... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_16` | value_replaced_with_none | low_materiality_message_text | '"distance_representation=\'signed\' has no authoritative sign-orientation convention p... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_42` | value_replaced_with_none | low_materiality_message_text | 'f"input_contract_authority_provider.resolve({_REQUIRED_INPUT_CONTRACT_PROFILE!r}) retu... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_43` | value_replaced_with_none | low_materiality_message_text | 'self._resolved_input_contract' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_50` | value_replaced_with_none | low_materiality_message_text | 'f"input_contract_authority_provider.resolve({_REQUIRED_INPUT_CONTRACT_PROFILE!r}) retu... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_check_candle_contract__mutmut_2` | value_replaced_with_none | low_materiality_message_text | 'f"candle event_contract_ref={candle.event_contract_ref!r} is not one of the authorized... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_check_candle_recorded_time__mutmut_4` | value_replaced_with_none | low_materiality_message_text | 'f"candle recorded_time {recorded_time!r} precedes last-seen {self._last_candle_recorde... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_check_candle_scope__mutmut_6` | value_replaced_with_none | low_materiality_message_text | 'raise ForeignScopeError(f"candle scope {candle.scope!r} does not match engine scope {s... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_check_swing_contract__mutmut_2` | value_replaced_with_none | low_materiality_message_text | 'f"swing event_contract_ref={contract_ref!r} is not one of the authorized swing contrac... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_check_swing_recorded_time__mutmut_4` | value_replaced_with_none | low_materiality_message_text | 'f"swing recorded_time {recorded_time!r} precedes last-seen {self._last_swing_recorded_... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_next_recorded_time__mutmut_5` | value_replaced_with_none | low_materiality_message_text | 'f"RecordedTimeSource.next_after({strict_floor!r}) returned {candidate!r}, not strictly... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_normalize_evidence__mutmut_13` | value_replaced_with_none | low_materiality_message_text | 'raise EvidenceCardinalityError(f"expected exactly 2 unique evidence refs, got {len(set... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_normalize_evidence__mutmut_2` | value_replaced_with_none | low_materiality_message_text | 'raise EvidenceReferenceConflictError(f"candle ref and swing ref collide: {candle.ref!r... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_12` | value_replaced_with_none | low_materiality_message_text | 'f"candidate swing {state.ref!r} was already full-cursor-visible at the existing fact\'... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_candle__mutmut_11` | value_replaced_with_none | low_materiality_message_text | 'f"candle ref {fact.ref!r} resolves to conflicting content ({existing!r} vs {fact!r})"'... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_candle__mutmut_13` | value_replaced_with_none | low_materiality_message_text | 'f"candle {subject_id!r} resubmitted with a different ref but is_correction=False"' -> ... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_candle__mutmut_25` | value_replaced_with_none | low_materiality_message_text | 'raise OutOfOrderCorrectionError(f"correction submitted for never-seen candle {subject_... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_candle__mutmut_30` | value_replaced_with_none | low_materiality_message_text | 'f"candle window_start {fact.scope.window_start!r} precedes last-seen " f"{self._candle... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_confirmed__mutmut_18` | value_replaced_with_none | low_materiality_message_text | 'f"swing ref {fact.ref!r} resolves to conflicting SwingConfirmed content " f"({existing... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_confirmed__mutmut_27` | value_replaced_with_none | low_materiality_message_text | 'f"swing_id {fact.swing_id!r} first-seen revision must be 1, got {fact.swing_revision!r... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_confirmed__mutmut_29` | value_replaced_with_none | low_materiality_message_text | 'f"swing_id {fact.swing_id!r} revision {fact.swing_revision!r} received before revision... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_confirmed__mutmut_33` | value_replaced_with_none | low_materiality_message_text | 'f"swing_id {fact.swing_id!r} revision must advance by exactly one: expected " f"{exist... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_confirmed__mutmut_7` | value_replaced_with_none | low_materiality_message_text | 'raise ForeignScopeError("SwingConfirmed scope does not match this Feature engine\'s ow... |
| `contracts.x_is_visible_at_cursor__mutmut_2` | boolean_none_swap | needs_review_data_context | False -> True |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_62` | boolean_none_swap | needs_review_data_context | False -> True |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_2` | string_case_mutation | needs_review_data_context | 'feature' -> 'FEATURE' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_2` | string_case_mutation | needs_review_data_context | 'feature' -> 'FEATURE' |
| `authority_resolver.x__extract_scalar__mutmut_5` | string_literal_marker_mutation | needs_review_data_context | '' -> 'XXXX' |
| `identity.x_deterministic_id__mutmut_3` | string_literal_marker_mutation | needs_review_data_context | '' -> 'XXXX' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ__init____mutmut_1` | string_literal_marker_mutation | needs_review_data_context | 'feature' -> 'XXfeatureXX' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ__init____mutmut_1` | string_literal_marker_mutation | needs_review_data_context | 'feature' -> 'XXfeatureXX' |
| `authority_resolver.x__extract_included_streams__mutmut_2` | value_replaced_with_none | needs_review_data_context | 'in_block = False' -> 'in_block = None' |
| `authority_resolver.x__extract_scalar__mutmut_4` | value_replaced_with_none | needs_review_data_context | 'return stripped[len(prefix) :].strip().strip(\'"\')' -> 'return stripped[len(prefix) :... |
| `contracts.x__construct_verified_authority__mutmut_5` | value_replaced_with_none | needs_review_data_context | 'object.__setattr__(instance, "feature_computation_profile", feature_computation_profil... |
| `contracts.x__seal_verified_authority__mutmut_33` | value_replaced_with_none | needs_review_data_context | 'feature_computation_profile=feature_computation_profile,' -> 'feature_computation_prof... |
| `current_view.xǁFeatureCurrentViewǁcurrent__mutmut_17` | value_replaced_with_none | needs_review_data_context | 'feature_subject_id = self.scope.feature_subject_id' -> 'feature_subject_id = None' |
| `current_view.xǁFeatureCurrentViewǁon_feature_computed__mutmut_10` | value_replaced_with_none | needs_review_data_context | 'window_end=key[1],' -> 'window_end=None,' |
| `current_view.xǁFeatureCurrentViewǁon_feature_computed__mutmut_12` | value_replaced_with_none | needs_review_data_context | 'invalidated=False,' -> 'invalidated=None,' |
| `current_view.xǁFeatureCurrentViewǁon_feature_computed__mutmut_13` | value_replaced_with_none | needs_review_data_context | 'last_recorded_time=event.recorded_time,' -> 'last_recorded_time=None,' |
| `current_view.xǁFeatureCurrentViewǁon_feature_computed__mutmut_9` | value_replaced_with_none | needs_review_data_context | 'window_start=key[0],' -> 'window_start=None,' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_invalidation__mutmut_12` | value_replaced_with_none | needs_review_data_context | 'ref = self._allocator.next_ref(self._stream_id)' -> 'ref = self._allocator.next_ref(No... |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_original__mutmut_52` | value_replaced_with_none | needs_review_data_context | 'False' -> 'None' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_54` | value_replaced_with_none | needs_review_data_context | 'replacement' -> 'None' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_55` | value_replaced_with_none | needs_review_data_context | 'False' -> 'None' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_56` | value_replaced_with_none | needs_review_data_context | 'fact.ref' -> 'None' |
| `regime_passthrough.xǁRegimePassthroughFeatureEngineǁ_emit_replacement__mutmut_57` | value_replaced_with_none | needs_review_data_context | 'head_fact=replacement, invalidated=False, last_evidence_ref=fact.ref, last_evidence_fa... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_original__mutmut_52` | value_replaced_with_none | needs_review_data_context | 'False' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_original__mutmut_53` | value_replaced_with_none | needs_review_data_context | 'swing_id' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_56` | value_replaced_with_none | needs_review_data_context | 'False' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_57` | value_replaced_with_none | needs_review_data_context | 'swing_id' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_58` | value_replaced_with_none | needs_review_data_context | 'head_fact=replacement, invalidated=False, used_swing_id=swing_id, used_swing_ref=state... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_reattempt__mutmut_51` | value_replaced_with_none | needs_review_data_context | 'swing_id' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_reattempt__mutmut_53` | value_replaced_with_none | needs_review_data_context | 'invalidation.ref' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_39` | value_replaced_with_none | needs_review_data_context | 'swing_id' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_invalidate_and_replace__mutmut_41` | value_replaced_with_none | needs_review_data_context | 'invalidation.ref' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_normalize_evidence__mutmut_7` | value_replaced_with_none | needs_review_data_context | 'items.sort(key=_sort_key)' -> 'items.sort(key=None)' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_53` | value_replaced_with_none | needs_review_data_context | 'swing_id' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_55` | value_replaced_with_none | needs_review_data_context | 'invalidation.ref' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_14` | value_replaced_with_none | needs_review_data_context | 'swing_id' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_28` | value_replaced_with_none | needs_review_data_context | 'swing_id,' -> 'None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_31` | value_replaced_with_none | needs_review_data_context | 'correction_ref=correction_ref,' -> 'correction_ref=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_44` | value_replaced_with_none | needs_review_data_context | 'key,' -> 'None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_45` | value_replaced_with_none | needs_review_data_context | 'candle,' -> 'None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_46` | value_replaced_with_none | needs_review_data_context | 'swing_id,' -> 'None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_47` | value_replaced_with_none | needs_review_data_context | 'state,' -> 'None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_48` | value_replaced_with_none | needs_review_data_context | 'existing.pending_invalidation_ref,' -> 'None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_49` | value_replaced_with_none | needs_review_data_context | 'existing.pending_invalidation_recorded_time,' -> 'None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_50` | value_replaced_with_none | needs_review_data_context | 'cursor,' -> 'None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_reevaluate_all_windows__mutmut_20` | value_replaced_with_none | needs_review_data_context | 'swing_id,' -> 'None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_reevaluate_all_windows__mutmut_22` | value_replaced_with_none | needs_review_data_context | 'lineage.pending_invalidation_ref,' -> 'None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_reevaluate_all_windows__mutmut_42` | value_replaced_with_none | needs_review_data_context | 'swing_id' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_select_eligible_swing__mutmut_18` | value_replaced_with_none | needs_review_data_context | 'item[0]' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁ_swing_state_as_of__mutmut_42` | value_replaced_with_none | needs_review_data_context | 'source_fact=latest.source_fact,' -> 'source_fact=None,' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_candle__mutmut_15` | value_replaced_with_none | needs_review_data_context | 'self._candles[existing_index] = fact' -> 'self._candles[existing_index] = None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_candle__mutmut_16` | value_replaced_with_none | needs_review_data_context | 'self._candle_by_window[(fact.scope.window_start, fact.scope.window_end)] = fact' -> 's... |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_invalidated__mutmut_19` | value_replaced_with_none | needs_review_data_context | 'invalidation.swing_revision' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_invalidated__mutmut_33` | value_replaced_with_none | needs_review_data_context | 'invalidation.ref' -> 'None' |
| `swing_distance.xǁSwingDistanceFeatureEngineǁon_swing_invalidated__mutmut_4` | value_replaced_with_none | needs_review_data_context | 'already_invalidated = existing is not None and ( invalidation.swing_id, existing.revis... |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_19` | string_case_mutation | very_likely_equivalent_codec_case_insensitive | 'utf' -> 'UTF' |
| `authority_resolver.x_resolve_input_contract_authority_from_repository__mutmut_23` | string_case_mutation | very_likely_equivalent_codec_case_insensitive | 'utf' -> 'UTF' |
| `identity.x_deterministic_id__mutmut_8` | string_case_mutation | very_likely_equivalent_codec_case_insensitive | 'utf' -> 'UTF' |


---
## 2. Mutation-surface blind spots — the 12 excluded hand-written methods

mutmut 3.7.0's decorated-class limitation (established in earlier transactions)
skips hand-written methods on `@dataclass(frozen=True, slots=True)`-decorated
classes. 12 such methods across 10 classes generate zero mutants and are
entirely absent from baseline-001's 1531-mutant population. Per the hard rule
carried forward from Testing Convention v0.12 §5c (restated in v0.16): ordinary
passing unit tests for these classes are **not** equivalent mutation-effectiveness
evidence — they prove the happy path works, not that a seeded fault would be
caught. Each method is assessed below purely on the materiality of its own
logic, read directly from current source.

| Method | Materiality | Why |
|---|---|---|
| `authority_resolver.FilesystemInputContractAuthorityResolver.resolve` | Moderate | One-line passthrough to `resolve_input_contract_authority_from_repository(profile, repo_root=self.repo_root)`. Risk is narrow: dropping/misrouting `repo_root` would silently break the test-fixture-pinning use case. The called function itself is heavily mutated (134 mutants) and separately covered. |
| `authority_resolver.StaticInputContractAuthorityProvider.resolve` | **High** | Contains its own fail-closed guard: `if self.authority.feature_computation_profile != profile: raise InputContractIdentityMismatchError(...)`. A `!=`→`==` mutation here would silently *accept* mismatched-profile authority instead of rejecting it — exactly the class of defect mutation testing exists to catch, and it is structurally invisible to today's baseline. |
| `candle.CandleScope.subject_id` | Moderate-High | Property forwarding 5 fixed fields into `deterministic_id("candle", ...)`. An argument-order or field-omission mutation would silently change scope identity (collision risk). `deterministic_id` itself is separately mutation-tested (`identity.py`); this specific call-site wiring is not. |
| `candle.OHLCV.field` | **High** | 4-way branch dispatch (`open`/`high`/`low`/`close`) plus a fail-closed `raise ValueError` for anything else. Swapping which branch returns which field (e.g. `field("high")` returning `self.low`) is a silent-data-corruption class of bug feeding directly into `reference_price_field` lookups, with no mutation coverage today. |
| `contracts.EvaluationFrontier.plain_stream_positions` | Moderate | One-line dict comprehension (`{stream_id: proof.sequence for ...}`) feeding `is_visible_at_cursor` eligibility. A mutation dropping items or swapping the projected field would silently corrupt cursor-visibility decisions. |
| `contracts.VerifiedInputContractAuthority.__init__` | High intent, low mutation surface | Deliberately, unconditionally raises `TypeError` — a hard anti-construction guard. If mutated to a no-op, this would be a critical governance regression (external code could fabricate verified authority), but the method has almost no internal branching for a mutation operator to act on beyond the exception type/message/entirely removing the raise. Existing ordinary tests (`test_*_verified_authority_not_exported_from_public_package`, `test_directly_fabricated_verified_type_cannot_be_supplied_to_*`) target exactly this property today — but, per the hard rule above, that is ordinary-test evidence, not mutation-effectiveness evidence. |
| `contracts.FeatureScope.feature_subject_id` | Moderate-High | Same pattern as `CandleScope.subject_id` — identity/hash computation from 5 fixed fields, no dedicated mutation coverage. |
| `contracts.DecimalPrecisionPolicy.__post_init__` | Moderate-High | Boundary validation (`digits < 0`, `rounding not in _VALID_ROUNDINGS`). An off-by-one on the boundary check (`< 0` → `<= 0`) would silently change which `digits` values are accepted. |
| `contracts.DecimalPrecisionPolicy.apply` | **High** | `value.quantize(Decimal(1).scaleb(-self.digits), rounding=self.rounding)` — this is the actual numeric rounding computation applied to real feature values. A sign flip on `-self.digits` or a dropped `rounding=` kwarg would silently corrupt numeric feature output. This is the single highest-materiality item on this list: core numeric business logic, zero mutation coverage. |
| `contracts.FeatureDefinition.__post_init__` | **High** | The densest of the 12: ~15 independent `if ... != POLICY: raise InvalidFeatureDefinitionError(...)` fail-closed guards plus feature-type-specific field-combination checks. Each guard is an obvious, independent mutation target (`!=`→`==` inverts it). If mutmut's decorated-class limitation were ever lifted, this method alone would likely be the single highest-value target in the entire module. |
| `publish.SequenceAllocator.next_ref` | Moderate-High | Sequence-number and event-id allocation (`next(counter)`, `f"{self.run_id}-{next(self._event_ordinal)}"`). An off-by-one (`count(1)`→`count(0)`) or swapped counter would silently corrupt stream-sequence integrity, a core platform invariant. |
| `publish.SequenceAllocator.producer_ref` | Moderate | One-line `ProducerRef(self.module_id, self.implementation_version, self.run_id)` construction. An argument-order swap would silently corrupt producer identity on every emitted event. |

**Conclusion:** at least 5 of the 12 (`StaticInputContractAuthorityProvider.resolve`,
`OHLCV.field`, `DecimalPrecisionPolicy.apply`, `DecimalPrecisionPolicy.__post_init__`,
`FeatureDefinition.__post_init__`) are high-materiality, non-trivial-branching
methods with **zero** mutation-effectiveness evidence of any kind today. What
would qualify as evidence under v0.16 (none of which exists yet, and none of
which this transaction creates):

1. An upstream mutmut fix/release removing the decorated-class hand-written-method
   limitation, letting these 12 fall naturally into a future baseline; or
2. A manually-authored, individually-pinned fault-injection test suite specific
   to these 12 methods — deliberately seeding faults that mirror mutmut's own
   operators (None-replacement, comparison-operator flip, off-by-one,
   branch-swap) against each method directly, with each seeded fault
   individually justified per v0.16's evidentiary bar; **not** a blanket
   "this class has unit tests" claim; or
3. A separate, clearly-scoped supplemental mutation tool run against just these
   methods, reported and pinned independently — never silently merged into the
   baseline-001 aggregate, since that would conflate two tools' semantics into
   one score.

No such mechanism exists today. This blind spot is recorded as an open gap, not
resolved by this analysis.

---

## 3. Kill-validity cohort — the 165 `BadTestExecutionCommandsException` occurrences

### 3.1 Why exact per-mutant identity was not recoverable from the original log

Direct inspection of the installed mutmut 3.7.0 source (`mutmut/__main__.py`)
confirms the mechanism precisely, rather than by inference:

- Each mutant's test run happens in a forked child process
  (`mutmut/__main__.py` `_run`, `os.fork()` branch): the child calls
  `runner.run_tests(...)` → `execute_pytest(...)`, and calls `os._exit(result)`
  on a normal return.
- Our shim's `_patched_execute_pytest` raises `BadTestExecutionCommandsException`
  (identical to stock mutmut's own behavior for this exit code, per Testing
  Convention v0.16's approved shim design) whenever `pytest.main()` returns exit
  code 4 outside the authenticated forced-fail sanity path.
- When that exception is raised inside the **child**, it is uncaught at the
  point of `os._exit(result)` (never reached) and instead propagates through
  Python's default unhandled-exception handling, which terminates the child
  process with **OS-level exit status 1**.
- The **parent** reads this via `os.waitstatus_to_exitcode(wait_status)` in
  `read_one_child_exit_status()` and records it via
  `mutation_data.register_result(exit_code=1)` — **bitwise identical** to the
  exit code recorded for a genuine, ordinary pytest test-failure kill.

This is why the aggregate `exit_code_by_key` mapping (and hence baseline-001's
`sorted_mutant_id_to_result_mapping`) cannot distinguish the two cases: both are
simply `{"exit_code": 1, "status": "killed"}`. The only way to tell them apart
is to re-run the specific mutant with `debug=true` and inspect the live
traceback — which is what this section does, in a bounded, isolated,
NON-GATING way.

### 3.2 Diagnostic performed

An 18-mutant stratified sample was drawn from the 1162 killed population (not
from survivors — baseline-001's survivor set and counts are untouched) across
all 7 modules that contribute killed mutants: 6 from `authority_resolver.py`
(both of its two conftest-relevant functions), 2 each from `contracts.py`,
`swing_distance.py`, `regime_passthrough.py`, `current_view.py`,
`candle_window.py`, and `identity.py`.

Each was re-run **individually**, by exact mutant name
(`python -m tooling run <mutant_id>`), in a **separate, disposable git worktree**
checked out at the same boundary (`4cecd03110dd7404e39807cfc1c43628d4af2c4a`)
with its own throwaway virtualenv, with `debug=true` set locally in that
worktree's own `pyproject.toml` copy only. This diagnostic:

- Never touched the tracked working tree (`git status`/`HEAD` in the real repo
  confirmed unchanged before and after).
- Did not overwrite, reinterpret, or re-derive any part of baseline-001 — the
  1531/1162/369 pinned counts and the mapping SHA-256 are untouched.
- Did not alter any production/test/tooling semantics.
- Is explicitly NON-GATING: it informs this analysis only.
- The disposable worktree and venv were removed after the diagnostic completed.

### 3.3 Result — mechanism and scope, empirically confirmed

`tests/conftest.py` makes exactly two module-level (import-time) calls, both to
`resolve_input_contract_authority_from_repository` (lines 84 and 87):

```python
SWING_DISTANCE_INPUT_CONTRACT = resolve_input_contract_authority_from_repository(...)
REGIME_INPUT_CONTRACT = resolve_input_contract_authority_from_repository("regime")
```

Because mutant activation is scoped by the `MUTANT_UNDER_TEST` environment
variable at the trampoline level, only mutations to functions actually
**reachable from these two calls** can affect conftest.py's own import — no
other module's mutation can, regardless of file.

The diagnostic confirmed this exactly:

| Sample | Result |
|---|---|
| 6/6 `authority_resolver.py` mutants (both `resolve_input_contract_authority_from_repository` and `_extract_included_streams`) | **All 6** crashed via `BadTestExecutionCommandsException` at `tests/conftest.py:84`, confirmed live in the debug traceback |
| 2/2 `contracts.py` mutants sampled (`_seal_verified_authority`, `_construct_verified_authority` — both in the reachable call graph) | **Both** crashed the same way, traceback passing through `authority_resolver.py` → `_seal_verified_authority`/`_construct_verified_authority` |
| 2/2 `swing_distance.py`, 2/2 `regime_passthrough.py`, 2/2 `current_view.py`, 2/2 `candle_window.py`, 2/2 `identity.py` (10 total, all outside the reachable call graph) | **0/10** hit `BadTestExecutionCommandsException` — all killed via ordinary, genuine pytest assertion failures |

Direct static confirmation of the reachable call graph (read from current
source, not inferred): `resolve_input_contract_authority_from_repository` →
`contracts._seal_verified_authority` → {`contracts._is_well_formed_content_id`
(×2 call sites), `contracts._construct_verified_authority`}, plus
`authority_resolver`'s own internal helpers (`_find_repo_root`,
`_extract_scalar`, `_extract_included_streams`, `_extract_registry_stream_ids`).

### 3.4 Bounded population estimate (upper bound, not exact membership)

Using the already-recorded per-mutant status counts (unchanged, from
baseline-001):

| Function population | Killed | Survived | Total |
|---|---|---|---|
| `authority_resolver.py` (all functions) | 113 | 21 | 134 |
| `contracts._seal_verified_authority` | 20 | 24 | 44 |
| `contracts._construct_verified_authority` | 49 | 1 | 50 |
| `contracts._is_well_formed_content_id` | 2 | 0 | 2 |
| **Reachable-call-graph upper bound** | **184** | — | — |

The corrected cohort size (165) is comfortably below this upper bound (184),
which is internally consistent: not every killed mutant in the reachable call
graph necessarily crashes collection (a mutation may be unreached by the two
specific fixed conftest.py inputs, or may be independently caught by
`test_authority_resolver.py`'s own direct assertions before ever needing the
crash path). Conversely, every mutant confirmed via the diagnostic to crash
**is** within this exact boundary — no crash-cohort member was found (or is
mechanistically possible, per §3.3) outside it.

### 3.5 Can this cohort materially bias calibration?

**Yes, in one specific, now well-understood way, but the bias is bounded and
localized — not codebase-wide.** The "killed" status for mutants in the
`authority_resolver.py` / `contracts.py`-authority-helper call graph does not
uniformly mean "a dedicated, fine-grained test assertion caught this specific
mutation." A material fraction of it means "this mutation broke the two fixed,
real-configuration calls conftest.py makes at collection time, which aborted
collection before any test — including `test_authority_resolver.py`'s own
dedicated assertions — ever ran." Both are genuine evidence of an
observable behavior change, but they are different detection channels: one is a
blunt, all-or-nothing collection abort; the other is a fine-grained, per-case
assertion. A future Step-5 threshold proposal should treat the elevated kill
rate observed within `authority_resolver.py` and this contracts.py helper
subset with that caveat, rather than reading it as evidence of comprehensive
line-level assertion coverage in `test_authority_resolver.py` specifically.

### 3.6 Disposition — fail-closed on exact identity, not on the analysis

Per this task's own explicit instruction, exact per-mutant identification of
**all 165** members (versus the empirically-confirmed 8/18 sampled) is **not**
pursued further in this transaction. Getting the exact, fully-enumerated
165-identity list would require individually re-running up to 184 additional
candidate mutants with `debug=true` — a bounded, mechanically well-defined, but
non-trivial follow-up diagnostic, disproportionate to a Step-4 *analysis*
transaction whose task is explicitly not to propose a threshold yet.

**Recorded, unresolved analysis gap:** the exact 165-member identity list
remains unrecovered. What is resolved, and is not a guess: the crash mechanism
(§3.3, grounded in direct mutmut source inspection plus live reproduction), the
exact scope boundary within which every possible member must fall (§3.3–3.4,
the reachable-call-graph population of at most 184 candidates, all confined to
`authority_resolver.py` and three named `contracts.py` helper functions), and
the direction/nature of the calibration bias this implies (§3.5). If a future
Step-5 threshold proposal needs the exact 165 identities (e.g. to weight or
exclude this cohort specifically), the diagnostic in §3.2 is directly
extensible: re-run all 134 `authority_resolver.py` candidates plus the 71
in-graph `contracts.py` candidates (205 total invocations, bounded and
NON-GATING) and record which of them individually reproduce the crash pathway.
That is deferred, not performed here.

---

## 4. Is empirical calibration sufficient to proceed to a Step-5 threshold proposal?

**Yes, with three named, carried-forward caveats that a Step-5 proposal must
address, not silently inherit:**

1. **138 material, concrete actionable test gaps** (§1.4) are now individually
   identified by exact mutant ID (§1.6) and are ready to inform either targeted
   test additions or an explicit, justified decision to accept them as residual
   risk at whatever threshold is eventually proposed.
2. **12 hand-written methods (§2) remain completely outside mutation-testing
   visibility**, 5 of them high-materiality. A Step-5 proposal must state
   explicitly whether/how this blind spot is accounted for (e.g. excluded from
   scope with a named justification, or gated on one of the three qualifying
   mechanisms in §2) — it cannot be silently ignored.
3. **The `authority_resolver.py`/`contracts.py`-authority-helper kill rate
   carries a known, bounded detection-channel caveat** (§3.5) and should not be
   read as uniformly strong assertion-level evidence for that specific subset
   without that caveat attached.

No blocking, unresolved-in-principle gap was found: the survivor population is
fully classified with concrete evidence, the blind spots are named and bounded
rather than open-ended, and the kill-validity risk is mechanistically
understood and scope-bounded even though its exact membership is not fully
enumerated. `TEST_EFFECTIVENESS_THRESHOLD` remains `UNRESOLVED` — this document
does not propose one.

---

## 5. Review A dispositions folded into this transaction

Per this task's own instruction and the previously-adopted P3-TXN-001
default-fold lesson, the following externally-supplied Review A dispositions
are recorded here (folded into this already-required analysis transaction,
rather than as a separate standalone review-evidence transaction). These are
recorded as **externally-supplied dispositions being folded in**, not as facts
this executor independently re-derived or verified beyond confirming no
contradicting record already existed in the repository at the stated boundary:

- `P3-PY-MUT-BASELINE-A-MAJ-02`: **CLOSED — REVIEW A** (externally-supplied;
  Review A independently validated the durable evidence artifact
  `feature-engine-mutation-baseline-001.json`, blob
  `978ebf92f89e5bd93ba112c1b8e4622835ea71ba`, at boundary
  `4cecd03110dd7404e39807cfc1c43628d4af2c4a`)
- `P3-PY-MUT-BASELINE-B-MAJ-01`: **CLOSED — REVIEW A INDEPENDENT VALIDATION**
  (externally-supplied; same Review A pass)
- Stated Review A result: Blocker 0 / Major 0 / Minor 0 —
  `FINAL BOUNDED REVIEW A RE-VALIDATION: CLEAN` (externally-supplied)

No prior record of these two dispositions existed in `docs/MANIFEST.md` or
`docs/CHANGELOG.md` before this transaction; this is their first recording.

## 6. Current-state preservation (unchanged by this analysis)

This analysis does not change, and this transaction does not authorize any
change to, the following:

- `TEST_EFFECTIVENESS_THRESHOLD`: **UNRESOLVED**
- `P3-FEATURE-QG-EVID-03`: **FAIL — evidence**
- Feature Engine Chapter 13 Quality Gate: **FAIL**
- Feature Engine approval status: **NOT APPROVED**
- Phase 3 gate: **NOT OPENED**
- LIVE authorization: **NOT_AUTHORIZED**
