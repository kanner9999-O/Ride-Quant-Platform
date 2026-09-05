# Feature Engine — Material-Gap Mutant Reclassification Candidate 001

```yaml
status: CANDIDATE / NOT EFFECTIVE / PENDING REVIEW
artifact_id: feature-engine-mutant-reclassification-candidate-001
created_for: >
  Proposing individual disposition of the 10 still-surviving material-gap
  mutant identities after EVID-03 test-remediation Batches 1+2, per
  feature-engine-mutation-post-remediation-diagnostic-001.json.
transaction_kind: PLANNING / DECISION-CANDIDATE ONLY
production_changed: false
tests_changed: false
tooling_changed: false
raw_denominator_changed: false
raw_score_changed: false
formal_step9_qg_evaluation_performed: false
repository_head_at_authoring: 0d69b7750ff319423f4aa4afdebc6c25a662c06d
```

This document is a **candidate**. Nothing in it is effective until a separately
recorded review decision (Review A of this candidate, per this task's own
required next governed action) accepts, rejects, or amends each disposition
below. No `P3-FEATURE-QG-EVID-03` identity is closed by this document. No
raw score, denominator, or ten-status count is touched. No production, test,
or tooling file is modified by this transaction.

## 0. Authority resolved for this candidate

- **Testing Convention v0.16, `docs/engineering/testing.md` item 8** (Approved)
  — the equivalent-mutant adjustment rule this candidate applies: "equivalent
  mutants REMAIN IN THE RAW DENOMINATOR by default... Any removal of a
  specific mutant from the denominator on an 'equivalent' basis requires ALL
  of: a deterministic, reproducible, exactly-pinned mutant identity...; an
  individually-recorded semantic justification...; and a governed adjustment
  mechanism (a reviewed, recorded decision...)." This candidate supplies the
  first two of these three for all 10 identities; it does **not** itself
  constitute the third (the "reviewed, recorded decision" is Review A, not
  yet performed) — hence `NOT EFFECTIVE`.
- **Approved Feature Engine mutation threshold proposal §4.1** (material-gap
  identity-resolution condition) — defines the 170-ID population this
  candidate's 10 identities are drawn from, and confirms (per the proposal's
  own §4.1 wording, corroborated directly in the approved proposal document)
  that a governed reclassification is one of the two legitimate ways an
  individual identity may be marked resolved (the other being killed/
  confirmed_timeout in a fresh measurement) — reclassification does not
  touch condition 1's raw score.
- **`feature-engine-mutation-baseline-001-analysis.md`** §1.6 (per-mutant
  Step-4 analysis) — source of each identity's original category/materiality
  classification and the exact token-level mutation diff.
- **`feature-engine-mutation-post-remediation-diagnostic-001.json`** — source
  of current identity evidence: all 10 IDs independently reconfirmed
  `survived` in a fresh, full, NON-GATING 1531-mutant run at repository HEAD
  `a0e537a6b5f883d26b1fdf7e09499dfa82079419` (one commit behind this
  candidate's own boundary; `python/feature-engine/src/**` has not changed
  between that diagnostic and this candidate's own HEAD — reconfirmed below).
- **Current exact source tree** (`python/feature-engine/src/feature_engine/`)
  — read directly and in full for `swing_distance.py`, `current_view.py`,
  `contracts.py`, `envelope.py`, `publish.py` as part of this candidate's own
  analysis; every claim below is grounded in the actual current source, not
  restated from a prior transaction's memory.
- **`docs/constitution/08-event-model.md` §8.3.2** ("Per-stream contiguous
  sequence", Locked) — the authoritative, Constitution-level invariant used
  for the two total-order-tiebreak identities (not this repository's test
  fixture's `SequenceAllocator` alone).

### Fresh source-identity re-verification (before any analysis)

```text
git rev-parse HEAD                                          -> 0d69b7750ff319423f4aa4afdebc6c25a662c06d
git rev-parse HEAD:python/feature-engine/src                -> 256421344a48a6c9d4ef72f81eb82b27dbedfc50
```

`256421344a48a6c9d4ef72f81eb82b27dbedfc50` is byte-identical to the src tree
recorded in `feature-engine-mutation-baseline-001.json`,
`feature-engine-mutation-step9-formal-evidence-001.json`, AND
`feature-engine-mutation-post-remediation-diagnostic-001.json`'s own
`measurement_boundary`. Source has not changed since any of those
measurements — the diagnostic's survivor identities and this candidate's own
fresh source reading are analyzing the exact same code.

## 1. Fresh Chapter 0 §4b ADR Scope Rule check (this decision, not inherited)

Per Constitution §4b, evaluated independently for THIS specific decision
(proposing individual equivalent/unreachable dispositions for 10 named
mutant identities under an already-approved adjustment mechanism) — not
assumed from the Step-6 `ADR_OPTIONAL` classification recorded for the
threshold *proposal* itself (a materially different, larger-scoped decision
that introduced new numeric conditions into the gate formula):

| §4b criterion | Applies here? |
|---|---|
| Adds/changes a Platform Invariant | No — does not touch Chapter 8, Chapter 13, or any Locked invariant. Cites Chapter 8 §8.3.2 as evidence; does not alter it. |
| Changes an Event Schema | No. |
| Changes Module Taxonomy/dependency graph | No. |
| Changes Governance/Approval process | No — applies the ALREADY-approved Testing Convention v0.16 item 8 mechanism to specific identities; does not invent a new review workflow, role, lifecycle stage, or approval-gate structure (identical reasoning already applied, for a materially larger change, in the threshold proposal's own correction record — see `feature-engine-mutation-threshold-proposal-001.md` line ~450). |
| Affects >1 module | No — scoped entirely to `feature-engine`'s own internal test-effectiveness bookkeeping. |
| Hard to reverse | No — this is a document-level classification candidate; even if a future Review A accepts it, a later transaction can reopen any single identity via a new governed decision (Testing Convention item 8 itself is a repeatable, per-identity mechanism, not a one-way ratchet). |
| Modifies/supersedes a Locked ADR | No — no ADR is touched. |

**Disposition: `ADR_NOT_REQUIRED`.** This is a narrower application of an
already-Approved Convention mechanism to specific mutant identities, not a
new rule, and changes no contract/schema/invariant/module boundary. (Contrast
explicitly with `feature-engine-chapter13-remediation-plan-001.md`'s own
Step-6 result of `ADR_OPTIONAL` for the threshold *proposal*: that decision
introduced NEW gate conditions — a materially different kind of change from
applying an existing per-identity adjustment mechanism to ten specific IDs.)

## 2. Per-identity analysis

Each entry: exact source symbol/location (this repository's current source,
line numbers as read directly), exact original→mutated semantic, why
ordinary meaningful tests cannot distinguish it (if true), the authoritative
facts supporting that claim, proposed classification, required assumptions,
and what future change would invalidate the classification.

---

### 2.1 `current_view.xǁFeatureCurrentViewǁon_feature_computed__mutmut_19`

- **Location:** `src/feature_engine/current_view.py:93-99`, inside
  `FeatureCurrentView.on_feature_computed`'s original-computation branch:
  ```python
  self._windows[key] = _ViewWindowState(
      window_start=key[0],   # mutated to key[1]
      window_end=key[1],
      head_fact=event,
      invalidated=False,
      last_recorded_time=event.recorded_time,
  )
  ```
- **Original → mutated semantic:** `_ViewWindowState.window_start` is
  constructed from `key[0]` (the window's own start) in the original;
  mutmut_19 constructs it from `key[1]` (the window's own end) instead —
  `_ViewWindowState.window_start` silently receives the wrong value.
- **Why ordinary tests cannot distinguish it:** `_ViewWindowState.window_start`
  is written in exactly one place (this one) and read **nowhere** in the
  entire repository. Exhaustive check: `grep -rn "\.window_start"
  src/feature_engine/current_view.py` returns exactly 3 hits — line 88
  (`event.window_start`, the incoming event's own field), line 114 (same),
  line 143 (`fact.window_start` where `fact = state.head_fact`, a
  `FeatureComputed`'s own field) — **none** read `_ViewWindowState.window_start`
  itself. A repo-wide `grep -rn "_ViewWindowState"` finds only this file's own
  3 references (class def, dict type annotation, this one constructor call)
  plus an unrelated, differently-scoped class of the same name in
  `raw_regime_engine/regime.py` (a separate module, never imports this one).
  No test, no serialization, no `dataclasses.asdict`/`vars()`/`__dict__`
  introspection anywhere touches this field (verified directly, zero hits).
- **Classification: `PROVABLY_EQUIVALENT`.**
- **Assumptions required:** none beyond "the field is never read" holding —
  this is a closed, repo-wide, exhaustive grep-verified fact about the
  CURRENT source, not merely "no current test happens to read it."
- **What would invalidate this:** any future code (production or test) that
  reads `_ViewWindowState.window_start` (e.g., a new diagnostic, a new
  ordering criterion, a new field-completeness assertion). Until then, no
  input can make this mutation observable.

---

### 2.2 `current_view.xǁFeatureCurrentViewǁon_feature_computed__mutmut_29`

- **Location:** `src/feature_engine/current_view.py:109`, inside the
  replacement-processing branch of `on_feature_computed`:
  ```python
  state.head_fact = event
  state.invalidated = False   # mutated to None
  state.last_recorded_time = event.recorded_time
  ```
- **Original → mutated semantic:** after a replacement is accepted,
  `state.invalidated` is set to `False` in the original; mutmut_29 sets it to
  `None` instead. `_ViewWindowState.invalidated` is type-annotated `bool` but
  Python does not enforce this at runtime.
- **Why ordinary tests cannot distinguish it:** every read of
  `.invalidated` on a `_ViewWindowState` in this module uses pure
  truthiness, never identity/equality against `False`/`True`/`None`.
  Exhaustive enumeration of all 3 read sites in
  `src/feature_engine/current_view.py`:
  - line 106: `if not state.invalidated:` (raise if NOT invalidated)
  - line 121: `if state.invalidated:` (raise if already invalidated)
  - line 135: `if not state.invalidated:` (VALID vs PENDING_CORRECTION branch)
  `None` and `False` are both falsy in Python; `not None == not False == True`
  and `bool(None) == bool(False) == False` — all three sites therefore behave
  IDENTICALLY whether the field holds `False` or `None`. No `is False`,
  `== False`, `is None`, or `type(...) is bool` check exists anywhere against
  this field (verified via `grep -rn "isinstance.*invalidated\|type(.*invalidated"`,
  zero hits).
- **Classification: `PROVABLY_EQUIVALENT`.**
- **Assumptions required:** all current and would-be future *ordinary*
  consumers of this field continue to use truthiness only — this is a
  property of the current 3 call sites, independently re-verified in this
  transaction (not merely restated from Batch 1's own note, though it
  reaches the same conclusion).
- **What would invalidate this:** a future consumer added anywhere in the
  repository that distinguishes `False` from `None` on this field (e.g., an
  `is False`/`is None` check, or a stricter type-narrowing / schema
  validation step applied to `_ViewWindowState`).

---

### 2.3 `swing_distance.x__total_order_key__mutmut_3`

- **Location:** `src/feature_engine/swing_distance.py:221-236`,
  `_total_order_key`'s returned tuple, criterion 6:
  ```python
  return (
      -state.pivot_effective_time[0].timestamp(),   # criterion 1
      state.recorded_time,                          # criterion 2
      state.ref.stream_id,                          # criterion 3
      _TIEBREAK_REGISTRY_VERSION,                    # criterion 4 (constant)
      state.ref.sequence,                            # criterion 5
      -state.revision,                               # criterion 6 -- mutated to +state.revision
      swing_id,                                       # criterion 7
      state.ref.event_id,                            # criterion 8
  )
  ```
- **Original → mutated semantic:** criterion 6 (`swing_revision`, intended
  DESC — higher revision wins) is negated in the original so the overall
  MINIMUM-key winner has the higher revision; mutmut_3 removes the negation,
  inverting the tiebreak direction for this one criterion.
- **Why ordinary tests cannot distinguish it:** Python tuple comparison is
  strictly lexicographic — criterion 6 is only ever inspected if criteria 1-5
  ALL tie between two candidates. Criterion 5 is `state.ref.sequence`. Every
  `_SwingState` reaching this function is sourced from EXACTLY one
  constructor site, `_swing_state_as_of` (`swing_distance.py:427`) — grep-
  confirmed the only `_SwingState(` call in the module — which in turn is
  populated only from `_SwingConfirmationRecord`s appended by
  `on_swing_confirmed` (the only appender, `swing_distance.py:506-515`).
  `on_swing_confirmed`'s own dedup/lineage-integrity guard (lines 465-472)
  REJECTS (`EvidenceReferenceConflictError`) any redelivery of the same
  `EventRecordRef` with different content, and treats an identical-ref
  redelivery as a no-op that never appends a second record — so every
  DISTINCT `_SwingConfirmationRecord` ever stored carries a DISTINCT,
  genuinely-authoritative `EventRecordRef`. `docs/constitution/08-event-
  model.md` §8.3.2 (Locked Platform Invariant, "Per-stream contiguous
  sequence"): *"Trong mỗi stream, `sequence` là số nguyên liên tiếp, tăng
  nghiêm ngặt"* — within any one stream, sequence numbers are strictly
  increasing and never repeat. Two candidates reach criterion 5's comparison
  only after criterion 3 (`ref.stream_id`) has ALREADY tied, i.e. both share
  the same stream — at which point §8.3.2 guarantees their `ref.sequence`
  values differ. Criterion 5 therefore ALWAYS discriminates before criterion
  6 is ever inspected, for any two genuinely-distinct, authoritatively-
  sourced Swing confirmations.
- **Classification: `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_AUTHORITATIVE_STATE_SPACE`**
  (explicitly NOT `PROVABLY_EQUIVALENT` — see assumptions below; this is a
  reachability claim contingent on an external platform invariant plus this
  module's own current, single call-site discipline, not a claim that holds
  for every conceivable `EventRecordRef`).
- **Assumptions required:** (a) every `EventRecordRef` reaching this code was
  genuinely assigned by an authoritative, §8.3.2-conformant producer — a
  test or a future caller COULD fabricate two `SwingConfirmedFact`s with a
  duplicate `(stream_id, sequence)` pair (nothing in `on_swing_confirmed`
  validates producer-side sequence uniqueness itself, since Feature Engine is
  a consumer, not the sequence-assigning authority); if such a fabricated
  pair existed, criterion 6 would be reachable and this mutation WOULD then
  be observable. (b) No future code path constructs a `_SwingState` outside
  `_swing_state_as_of`.
- **What would invalidate this:** (i) Chapter 8 §8.3.2 being revised/
  superseded (would require reopening a Locked chapter via a new ADR); (ii)
  a new `_SwingState` construction site bypassing `_swing_state_as_of`; (iii)
  a test or upstream producer defect that genuinely delivers two
  authoritative-looking `SwingConfirmedFact`s sharing one `(stream_id,
  sequence)` pair (a data-integrity violation Feature Engine does not itself
  currently detect or reject).

---

### 2.4 `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_original__mutmut_13`

- **Location:** `src/feature_engine/swing_distance.py:746`, inside
  `_emit_original`:
  ```python
  floor = max(candle.recorded_time, state.recorded_time, cursor.recorded_time)
  ```
  mutmut_13 removes the `state.recorded_time` argument, leaving
  `max(candle.recorded_time, cursor.recorded_time)`.
- **Original → mutated semantic:** the recorded_time floor for the emitted
  `FeatureComputed` no longer includes the winning Swing's own recorded_time.
- **Why ordinary tests cannot distinguish it:** `_emit_original` is called
  from exactly one site, `_recompute:703`, with `state` and `cursor` both
  taken directly from `winner = self._select_eligible_swing(candle.scope.
  window_end, cursor)` (`_recompute:694`) — the identical `cursor` object is
  then passed unchanged into `_emit_original`. `_select_eligible_swing`
  (`swing_distance.py:630-651`) only returns states obtained from
  `_swing_state_as_of(swing_id, cursor)` (same `cursor`), which only
  includes a confirmation record in its `visible` list if
  `is_visible_at_cursor(record.ref, record.recorded_time, ...,
  cursor_recorded_time=cursor.recorded_time)` returns `True`
  (`swing_distance.py:404-414`). `is_visible_at_cursor`'s current
  implementation (`contracts.py:159-190`) has exactly 3 branches: stream-
  membership (returns `True`/trivially-visible if the stream is outside
  `included_streams` — not applicable here since Swing's stream IS always in
  `included_streams` for this profile), sequence-position, and finally
  `return recorded_time <= cursor_recorded_time`. For the swing stream
  (always inside `included_streams`), reaching `visible=True` REQUIRES this
  third branch to hold, i.e. `record.recorded_time <= cursor.recorded_time`.
  The `_SwingState.recorded_time` field is copied verbatim from that same
  `record.recorded_time` (`swing_distance.py:431`). Therefore, for every
  `state` value that can ever reach `_emit_original`, `state.recorded_time
  <= cursor.recorded_time` holds **by construction**, using the SAME cursor
  object subsequently used in the floor computation — `state.recorded_time`
  can never be the strict maximum of the three-argument `max(...)` once
  `cursor.recorded_time` is also present.
- **Classification: `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_AUTHORITATIVE_STATE_SPACE`.**
- **Assumptions required:** (a) `is_visible_at_cursor`'s current
  recorded-time branch (`contracts.py:190`) is unchanged; (b) no future
  caller of `_emit_original` supplies a `state`/`cursor` pair where `state`
  was NOT freshly obtained from `_select_eligible_swing(..., cursor)` using
  that exact `cursor` — currently the only caller (`_recompute:703`)
  satisfies this by construction.
- **What would invalidate this:** a change to `is_visible_at_cursor`'s
  recorded-time branch (e.g., relaxing it or removing it); a new call site
  to `_emit_original` that decouples `state` from `cursor`.

---

### 2.5 `swing_distance.xǁSwingDistanceFeatureEngineǁ_emit_replacement_only__mutmut_16`

- **Location:** `src/feature_engine/swing_distance.py:819`, inside
  `_emit_replacement_only`:
  ```python
  floor = max(invalidation_recorded_time, candle.recorded_time, state.recorded_time, cursor.recorded_time)
  ```
  mutmut_16 removes `state.recorded_time`.
- **Original → mutated semantic:** same class of change as 2.4, one
  argument removed from a 4-argument floor.
- **Why ordinary tests cannot distinguish it:** `_emit_replacement_only` has
  5 call sites (`swing_distance.py:796, 873, 902, 724, 988`) — inside
  `_invalidate_and_replace`, `_invalidate_and_reattempt`,
  `_reevaluate_all_windows` (pending-window branch), `_recompute`
  (existing.invalidated branch), and `_preempt_settled_window`. In every one
  of these 5 sites, `state`/`cursor` are the SAME pair obtained from a
  `_select_eligible_swing(_, cursor)` call earlier in the SAME call chain
  (`_recompute:694`, `_invalidate_and_reattempt:869`, `_reevaluate_all_
  windows:893`) — never re-fetched with a different cursor, never
  independently constructed. The identical `is_visible_at_cursor` argument
  established in 2.4 applies unchanged: `state.recorded_time <=
  cursor.recorded_time` holds for every reachable call, by the same
  construction.
- **Classification: `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_AUTHORITATIVE_STATE_SPACE`.**
- **Assumptions required / invalidating change:** identical to 2.4, verified
  independently across all 5 call sites rather than assumed from 2.4's
  single-call-site proof.

---

### 2.6 `swing_distance.xǁSwingDistanceFeatureEngineǁ_preempt_settled_window__mutmut_20`

- **Location:** `src/feature_engine/swing_distance.py:972`, inside
  `_preempt_settled_window`:
  ```python
  invalidation_floor = max(existing.head_fact.recorded_time, state.recorded_time, cursor.recorded_time)
  ```
  mutmut_20 removes `state.recorded_time`.
- **Original → mutated semantic:** same class of change as 2.4/2.5.
- **Why ordinary tests cannot distinguish it:** `_preempt_settled_window`
  has exactly one call site, `_reevaluate_all_windows:917`, where `state`
  and `cursor` are the SAME pair from `winner = self._select_eligible_swing
  (candle.scope.window_end, cursor)` at `_reevaluate_all_windows:893` — the
  identical `cursor` is threaded through to `_preempt_settled_window`
  unchanged. The `EligibleSwingComputationDefectError` guard immediately
  preceding the floor computation (lines 958-971) checks `state`'s
  visibility against a DIFFERENT, separate cursor
  (`existing.head_fact.computation_cursor`, the ORIGINAL fact's own
  persisted cursor) — this does not alter the relationship between `state`
  and the CURRENT `cursor` used in the floor immediately below it. The same
  `is_visible_at_cursor` argument from 2.4 applies: `state.recorded_time <=
  cursor.recorded_time` by construction.
- **Classification: `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_AUTHORITATIVE_STATE_SPACE`.**
- **Assumptions required / invalidating change:** identical to 2.4.

---

### 2.7 `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_23`

- **Location:** `src/feature_engine/swing_distance.py:708`, inside
  `_recompute`'s "not existing.invalidated" branch:
  ```python
  assert correction_ref is not None and correction_recorded_time is not None
  ```
  mutmut_23 changes `and` to `or`.
- **Original → mutated semantic:** the assert requires BOTH arguments
  non-None in the original; mutmut_23 requires only AT LEAST ONE non-None —
  a mismatched `(non-None, None)` or `(None, non-None)` pair would pass the
  mutant's assert but fail the original's.
- **Why ordinary tests cannot distinguish it — public authoritative
  reachability, assessed precisely per this task's own instruction:**
  `_recompute` is a private method (`def _recompute(self, candle, *,
  correction_ref, correction_recorded_time, cursor)`). A complete,
  exhaustive grep of the entire module (`grep -n "self\._recompute("
  src/feature_engine/swing_distance.py`) finds EXACTLY two call sites, both
  inside the public `on_candle` method:
  - `on_candle:611-613` (existing-ref-with-is_correction branch):
    `self._recompute(fact, correction_ref=fact.ref, correction_recorded_
    time=fact.recorded_time, cursor=cursor)` — both arguments always
    non-None together (both derived from the same `fact`).
  - `on_candle:626` (brand-new-candle branch): `self._recompute(fact,
    correction_ref=None, correction_recorded_time=None, cursor=cursor)` —
    both arguments always `None` together (both literal `None`).
  There is no third call site, no keyword-only default that could be
  independently overridden, and `_recompute` is never re-exported or called
  from any other module (private, underscore-prefixed, not present in
  `__init__.py`'s public surface). Under the CURRENT source, no execution
  path — public or private — can invoke `_recompute` with a mismatched
  pair.
- **Classification: `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_AUTHORITATIVE_STATE_SPACE`**
  (explicitly not claimed equivalent merely because "current public callers"
  don't reach it — the claim here is stronger: reachability was assessed
  against the COMPLETE, exhaustively-enumerated set of the private method's
  own only two call sites, both intra-module and both hardcoded literal-
  paired invocations; still classified as reachability-contingent, not
  equivalent, because a future edit to `on_candle` — or a hypothetical third
  call site — could break the pairing without touching this assert line
  itself).
- **Assumptions required:** no future call site to `_recompute` (public or
  private) ever supplies a mismatched pair.
- **What would invalidate this:** any new call site to `_recompute`, or an
  edit to either of the two existing `on_candle` call sites, that decouples
  `correction_ref` from `correction_recorded_time`.

---

### 2.8 `swing_distance.xǁSwingDistanceFeatureEngineǁ_recompute__mutmut_46`

- **Location:** `src/feature_engine/swing_distance.py:727`, inside
  `_recompute`'s "existing.invalidated" branch:
  ```python
  return self._emit_replacement_only(
      key,
      candle,
      swing_id,          # mutated to None
      state,
      existing.pending_invalidation_ref,
      existing.pending_invalidation_recorded_time,
      cursor,
  )
  ```
- **Original → mutated semantic:** the `swing_id` argument (flows into
  `_emit_replacement_only`'s `used_swing_id=swing_id` at
  `swing_distance.py:837`, stored on the new `_WindowLineage`) is replaced
  with `None`.
- **Why ordinary tests cannot distinguish it:** `_WindowLineage.used_swing_id`
  is written in exactly 2 places (`swing_distance.py:764` and `:837`, both
  `_WindowLineage(...)` constructor calls) and read **nowhere** — a
  repository-wide `grep -rn "used_swing_id"` (not scoped to this one file)
  returns only these 2 writes plus the field declaration
  (`swing_distance.py:215`); `used_swing_ref` (a DIFFERENT field on the same
  dataclass) IS read, at `_reevaluate_all_windows:914`, but `used_swing_id`
  itself has zero read sites anywhere in the repository.
- **Classification: `PROVABLY_EQUIVALENT`.**
- **Assumptions required:** none beyond the repo-wide dead-store fact
  holding, verified directly (not merely "no current test reads it" — no
  PRODUCTION code reads it either).
- **What would invalidate this:** any future code reading
  `_WindowLineage.used_swing_id` (e.g., a diagnostic, an assertion, or new
  behavior keyed on which swing_id was used).

---

### 2.9 `swing_distance.xǁSwingDistanceFeatureEngineǁ_reevaluate_all_windows__mutmut_6`

- **Location:** `src/feature_engine/swing_distance.py:890-892`, inside
  `_reevaluate_all_windows`:
  ```python
  for key, lineage in list(self._lineage.items()):
      candle = self._candle_by_window.get(key)
      if candle is None:
          continue   # mutated to break
  ```
- **Original → mutated semantic:** a lineage entry whose window has no
  corresponding `_candle_by_window` entry is skipped (`continue`) in the
  original, versus the ENTIRE loop being abandoned (`break`) in the mutant.
- **Why ordinary tests cannot distinguish it — proving `_lineage` key
  without `_candle_by_window` cannot arise, per this task's own explicit
  instruction:** exhaustive enumeration of every mutation site of both
  dicts in the module:
  - `self._candle_by_window[...] = fact` is written unconditionally at
    exactly 2 sites, both inside the PUBLIC `on_candle`: line 610
    (correction branch) and line 625 (new-candle branch) — both execute
    BEFORE `on_candle` calls `_recompute` (lines 611-613, 626) for that
    exact `(window_start, window_end)` key. `_candle_by_window` is NEVER
    deleted from anywhere in the module (no `del`, no `.pop(`, no
    reassignment to a smaller dict — grep-confirmed, only 4 total usage
    sites: declaration, the 2 writes, and 2 reads at lines 868/890).
  - `self._lineage[key] = ...` is written at exactly 2 sites:
    `_emit_original:763` (creates a genuinely NEW key — reached only when
    `existing is None` at `_recompute:702`, itself reached only via
    `_recompute`, itself reached only via `on_candle`'s two branches, both
    of which have JUST written `_candle_by_window[key]` for that identical
    key in the SAME `on_candle` invocation) and `_emit_replacement_only:836`
    (re-assigns an ALREADY-EXISTING key — every one of `_emit_replacement_
    only`'s 5 callers, per 2.5 above, operates on a key it already holds an
    `existing`/`lineage` reference for, meaning that key was already present
    in `_lineage`, hence — by induction — already had a `_candle_by_window`
    entry).
  By induction over this COMPLETE, exhaustively-enumerated set of mutation
  sites (base case: `_emit_original` always follows a same-key
  `_candle_by_window` write in the same `on_candle` call; inductive step: no
  operation ever removes a `_candle_by_window` entry, and no other path adds
  a new `_lineage` key): every key ever present in `self._lineage` is, at
  all times thereafter, also present in `self._candle_by_window`. The
  `candle is None` branch is therefore never taken for any key actually
  produced by this module's own state machine.
- **Classification: `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_AUTHORITATIVE_STATE_SPACE`**
  (not equivalent: this is an invariant of the CURRENT absence of any
  candle-retraction/cleanup code path, not a mathematical impossibility — a
  future feature that removes stale `_candle_by_window` entries while
  leaving `_lineage` intact would make this branch reachable and the
  mutation observable).
- **Assumptions required:** no future code path ever deletes/replaces-with-
  absence a `_candle_by_window` entry whose key still has a `_lineage`
  entry.
- **What would invalidate this:** any future "candle retraction",
  windowed-cache eviction, or memory-bounding feature that clears
  `_candle_by_window` entries without also clearing the corresponding
  `_lineage` entry.

---

### 2.10 `swing_distance.xǁSwingDistanceFeatureEngineǁ_select_eligible_swing__mutmut_22`

- **Location:** `src/feature_engine/swing_distance.py:651`, inside
  `_select_eligible_swing`:
  ```python
  return min(candidates, key=lambda item: _total_order_key(item[0], item[1]))
  ```
  mutmut_22 changes `item[0]` (the `swing_id: str`) to `item[1]` (the
  `_SwingState` object) for BOTH positional arguments:
  `_total_order_key(item[1], item[1])`.
- **Original → mutated semantic:** `_total_order_key`'s first parameter
  (`swing_id: str`, used only at criterion 7 of the returned tuple, per
  2.3's reading of the function body) receives a `_SwingState` object
  instead of a string. Every OTHER criterion (1-6, 8) is computed from
  `state` (the second, correctly-passed argument `item[1]`) and is therefore
  UNAFFECTED by this specific mutation — only criterion 7's stored value is
  corrupted.
- **Why ordinary tests cannot distinguish it:** identical reasoning to 2.3
  (same authoritative Chapter 8 §8.3.2 argument): criterion 7 is only
  inspected by `min()`'s tuple comparison if criteria 1-6 ALL tie between
  two candidates, which requires criterion 5 (`ref.sequence`) to tie —
  impossible for two genuinely-distinct, authoritatively-sourced
  `_SwingState`s sharing the same `ref.stream_id` (criterion 3, which must
  also already have tied to reach criterion 5), per §8.3.2's per-stream
  contiguous-sequence guarantee. The corrupted criterion-7 value (a
  `_SwingState` object, which has no `__lt__` defined and would raise
  `TypeError` if Python's tuple comparison ever attempted `<` against it) is
  therefore never even inspected by the comparison algorithm, for any two
  distinct authoritative candidates — no crash, no behavioral difference.
- **Classification: `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_AUTHORITATIVE_STATE_SPACE`**
  (same authority and same caveats as 2.3 — NOT claimed equivalent, since a
  fabricated/malformed duplicate-sequence pair, or a `min()` call over a
  single-element `candidates` list combined with some future second call
  needing tiebreak comparison, could in principle reach criterion 7).
- **Assumptions required / invalidating change:** identical to 2.3.

## 3. Summary table

| # | Mutant ID (short) | Original mutation | Proposed classification |
|---|---|---|---|
| 1 | `current_view.on_feature_computed__mutmut_19` | `window_start=key[0]` -> `key[1]` | `PROVABLY_EQUIVALENT` |
| 2 | `current_view.on_feature_computed__mutmut_29` | `state.invalidated=False` -> `None` | `PROVABLY_EQUIVALENT` |
| 3 | `swing_distance.x__total_order_key__mutmut_3` | `-state.revision` -> `+state.revision` | `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_AUTHORITATIVE_STATE_SPACE` |
| 4 | `swing_distance._emit_original__mutmut_13` | `state.recorded_time` removed from floor | `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_AUTHORITATIVE_STATE_SPACE` |
| 5 | `swing_distance._emit_replacement_only__mutmut_16` | `state.recorded_time` removed from floor | `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_AUTHORITATIVE_STATE_SPACE` |
| 6 | `swing_distance._preempt_settled_window__mutmut_20` | `state.recorded_time` removed from floor | `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_AUTHORITATIVE_STATE_SPACE` |
| 7 | `swing_distance._recompute__mutmut_23` | assert `and` -> `or` | `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_AUTHORITATIVE_STATE_SPACE` |
| 8 | `swing_distance._recompute__mutmut_46` | `swing_id` arg -> `None` (feeds dead-store field) | `PROVABLY_EQUIVALENT` |
| 9 | `swing_distance._reevaluate_all_windows__mutmut_6` | `continue` -> `break` | `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_AUTHORITATIVE_STATE_SPACE` |
| 10 | `swing_distance._select_eligible_swing__mutmut_22` | `_total_order_key(item[0],item[1])` -> `(item[1],item[1])` | `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_AUTHORITATIVE_STATE_SPACE` |

**Count proposed reclassifiable (either category): 10/10.**
**Count `NOT_JUSTIFIED_FOR_RECLASSIFICATION`: 0/10** — no identity was forced
through; each of the 10 has an independently-verified, source-grounded
argument distinguishing genuine dead/inert-value equivalence from
reachability-contingent unreachability. If Review A finds any single
argument above unpersuasive, that identity alone reverts to
`NOT_JUSTIFIED_FOR_RECLASSIFICATION` without affecting the other 9 — each
disposition is independent per Testing Convention v0.16 item 8's own
per-identity requirement.

**Exact split: 3 `PROVABLY_EQUIVALENT`** (#1, #2, #8 — dead-store or
truthiness-only-consumed field values, never distinguishable by any
observable behavior) **and 7 `STRUCTURALLY_UNREACHABLE_UNDER_CURRENT_
AUTHORITATIVE_STATE_SPACE`** (#3, #4, #5, #6, #7, #9, #10 — differing
inputs/branches that WOULD be observable if reached, but cannot currently
be reached given the present call-graph discipline and/or the Chapter 8
§8.3.2 sequence-uniqueness invariant).

## 4. Explicit invariance statements (required)

- **Diagnostic raw score remains `86.41410842586545%`** — this candidate
  changes nothing about `feature-engine-mutation-post-remediation-
  diagnostic-001.json`'s own recorded ten-status counts, numerator, or
  denominator. No file in that artifact is modified.
- **Reclassification does NOT change numerator/denominator/raw score.** Per
  Testing Convention v0.16 item 8, equivalent/unreachable mutants "REMAIN IN
  THE RAW DENOMINATOR by default" even once governedly reclassified — a
  reclassification decision (once actually made, which this candidate does
  NOT do) affects ONLY the approved threshold proposal's §4.1 material-gap
  identity-resolution condition (condition 2), never condition 1's raw
  score computation, which is derived purely from `killed`/`confirmed_
  timeout`/`total`/`skipped`.
- **Even if all 10 are ultimately approved as individually resolved,
  Condition 1 still needs at least 9 additional qualifying kills** at the
  current 1531 denominator: `ceil(0.87001959503592 * 1531) = 1332`;
  `1332 - 1323 (current killed) = 9`. Reclassification of these 10 IDs would
  fully satisfy condition 2 (170/170 material-gap identities resolved) but
  leaves condition 1 (raw score >= 87.001959503592%) requiring 9 more
  genuine kills achieved through further test remediation — reclassification
  is not a substitute for that work.
- **Mutation-surface completeness / blind-spot condition (condition 3)
  remains unresolved separately** — unaffected by, and out of scope for,
  this candidate. `feature-engine-mutation-baseline-001-analysis.md` §2's 12
  excluded hand-written methods (5 high-materiality) still have no
  qualifying supplemental mutation mechanism, deterministic fault-injection
  evidence, or recorded Product Owner risk-acceptance — this candidate does
  not touch that dimension at all.

## 5. Preserved (unchanged by this candidate)

```text
TEST_EFFECTIVENESS_THRESHOLD:  EFFECTIVE (unchanged).
All 10 IDs above:              still formally UNRESOLVED / still counted as
                                survived in every existing evidence artifact,
                                until a later, separately-recorded Review A
                                decision accepts some/all/none of the
                                classifications proposed here.
P3-FEATURE-QG-EVID-03:         OPEN / blocking (unchanged, not evaluated).
P3-FEATURE-QG-EVID-04..-08:    OPEN / blocking (unchanged, untouched).
Overall Feature Chapter 13 QG: FAIL — evidence (unchanged).
No formal Step-9/QG evaluation performed by this candidate.
Feature module approval:       NOT APPROVED.
Phase 3 Approval Gate:         NOT opened.
LIVE:                           NOT_AUTHORIZED, unreferenced.
```

## 6. Next governed action

**Review A of this candidate** — an independent reviewer must accept,
reject, or amend each of the 10 per-identity classifications above. Only
after that recorded review decision may any of these 10 identities be
marked resolved in a formal Step-9/QG transaction's material-gap condition.
This document does not perform that review itself.
