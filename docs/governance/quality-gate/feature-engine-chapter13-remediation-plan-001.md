---
id: feature-engine-chapter13-remediation-plan-001
title: "Feature Engine Chapter 13 Remediation Plan #001 — the six blocking EVID findings"
plan_version: "1.0"
plan_status: PLANNING ONLY — NOT AN IMPLEMENTATION TRANSACTION
performed_at: "2026-09-04"
evaluated_boundary: "2d6ab4040a9f48f59d8dd92b875b32dff159adee"
---

# Feature Engine Chapter 13 Remediation Plan #001

**STATUS: PLANNING ONLY. No test/code/tooling implemented. No mutation testing or
Quality Gate rerun. No threshold semantics changed. No finding closed. Feature
Engine not approved. Phase 3 gate not opened. LIVE not authorized.**

This plan addresses the six currently blocking Feature Engine Chapter 13
findings: `P3-FEATURE-QG-EVID-03` through `P3-FEATURE-QG-EVID-08`. It resolves
each dimension's authority directly from the repository (Chapter 2 invariant
text, Chapter 13, Testing Convention v0.16, the original formal QG evidence
and its later corrections, the Step-4 mutation analysis, the Step-9 evidence
and its correction, and current Feature Engine source/tests) rather than
restating prior transactions' prose uncritically — two factual corrections
made during this planning pass are noted explicitly in §1.

## 0. Preserved lifecycle state (unchanged by this plan)

```text
TEST_EFFECTIVENESS_THRESHOLD: EFFECTIVE (87.001959503592% raw AND 170/170
  material-gap identity resolution, Tier-1/FEATURE-ENGINE-ONLY) — unchanged.
P3-FEATURE-QG-EVID-03 through -08: OPEN / blocking — unchanged, none closed
  by this plan.
Overall Feature Engine Chapter 13 Quality Gate: FAIL — evidence — unchanged.
P3-PY-MUT-THRESH-A-MIN-02: OPEN — MINOR / NON-BLOCKING — unchanged.
Feature Engine approval: NOT APPROVED. Phase 3 Approval Gate: NOT OPENED.
LIVE: NOT_AUTHORIZED.
```

## 1. Six-row blocker matrix

| Finding | Dimension | Classification | Exact gap | Dependency | Closure condition |
|---|---|---|---|---|---|
| `EVID-03` (raw score / 170 IDs) | Test-effectiveness — mutation score & material-gap identities | ~~**ACTIONABLE_NOW** — 0/170 pinned material-gap mutants killed; raw score 75.898105813194% < 87.001959503592%~~ **STALE (this row predates its own `evaluated_boundary` `2d6ab404...`, 2026-09-04; superseded by two later, real events this row was never mechanically reconciled with): `P3-FEATURE-QG-EVID-03` was CLOSED — PASS — REVIEW A VALIDATED at boundary `977c7e87507a382dd4a021673f1e582eaa85ff82`/`c220b62a097aa036413865ff0222c5c136f6f05f` (2026-09-08, raw score 87.655%, 170/170 resolved) — that historical closure remains valid and is NOT disputed. Production source has since materially expanded (ADR-043 implementation, `ownership.py`, EVID-06/EVID-07 suites), so a CURRENT-BOUNDARY re-evaluation was performed at exact Commit `596ad027955445be2d85036e1b52f226c8a42fde`: **`FAIL — criteria`** — raw score against a now-2629-mutant population; historical 170-ID contract only 42/170 directly comparable (128 discontinuous); Condition-3 evidence stale for current boundary. Full record: `docs/governance/mutation-baseline-evidence/feature-engine-mutation-step9-formal-evidence-003.json`. **Timeout-fidelity correction (`P3-PY-MUT-STEP9-003-A-MAJ-01`, Review A `REVISION_REQUIRED`):** the sole raw timeout was not individually reproduced/triaged before evidence-003 marked Condition 1 usable — corrected via deterministic isolation of the qualifying run's raw timeout(s) (2 consecutive isolated re-runs per mutant): `confirmed_timeout=1` (`ownership.x_p_run_sort__mutmut_82`, genuine deterministic timeout); the other raw timeout candidate (`contracts.x__construct_verified_authority__mutmut_47`) did not reproduce and resolved to `killed`. Corrected raw score **81.93229364777483%** — still `< 87.001959503592%`, so Condition 1 remains validly `FAIL — criteria`, now with complete timeout triage. Correction record: `docs/governance/mutation-baseline-evidence/feature-engine-mutation-step9-formal-evidence-003-correction-001.json`, `CLOSED — REVIEW A VALIDATED` (`P3-PY-MUT-STEP9-003-A-MAJ-01`). **Fresh formal current-boundary measurement (`feature-engine-mutation-step9-formal-evidence-004.json`, this same executable boundary, fresh venv, fresh run — not reused from evidence-003):** ten-status reconciled (killed=2154, survived=474, confirmed_timeout=1, all else 0, total=2629); raw score **81.97033092430583%** — still `< 87.001959503592%`, Condition 1 remains `FAIL — criteria` (normal run-to-run variance vs. the prior 81.93229364777483%). **Condition-2 identity resolution — exact semantic-continuity mapping (`P3-FEATURE-EVID03-COND2-RES-A-MAJ-01`/`-MAJ-02` `CLOSED — BOUNDED REVIEW A RE-REVIEW`, folded):** for the first time, a fresh formal run durably persisted the COMPLETE current 2629-mutant mapping and, for each of the 170 historical identities, compared the CURRENT mutation at each exact-string-present ID against its HISTORICAL description (not assuming positional-ID stability) — **14 already governedly resolved** (10 candidate-001 + 4 `resolve_output_contract_refs`, Review-A-validated, ID continuity not required) **+ 28 newly resolved via semantically-continuous fresh kill = 42/170 resolved**; **10 identities found `IDENTITY_COLLISION_OR_SEMANTIC_DISCONTINUITY`** (current mutation at that exact ID is a materially different mutation than historically pinned — including, critically, both of the previously-tracked "still-present survivors," whose current mutation turned out to be an unrelated string-marker change, not the historical `_stream_id=None` gap) — their current status is NOT credited to the historical obligation; **118 remain absent/unresolved**. **Condition 2: `FAIL / PARTIALLY SATISFIED — 42/170 resolved`** — NOT 170/170; no replacement mutant IDs authorized. Full record: `docs/governance/mutation-baseline-evidence/feature-engine-mutation-material-gap-identity-resolution-001.json`, cross-referencing `feature-engine-mutation-step9-formal-evidence-004.json`'s own full mapping + per-ID semantic fingerprint comparison.** **Evidence-004 governance-provenance correction, folded (`P3-FEATURE-EVID03-STEP9-004-A-MAJ-01: CLOSED — BOUNDED REVIEW A RE-REVIEW`):** final bounded Review A re-review of the correction returned `CLEAN — 0 Blocker / 0 Major / 0 Minor`, Risk `R1`. `feature-engine-mutation-step9-formal-evidence-004.json` + `-004-correction-001.json` together are now `REVIEW A VALIDATED` formal current-boundary evidence. **Condition-1 survivor-remediation Wave 1 (this transaction, test-only, `python/feature-engine/tests/test_ownership.py`):** selected one coherent 22-mutant cluster from the fresh 474-survivor population — `AuthoritativeSubjectOwner`'s revoke/terminal `OwnerHandle`-construction lifecycle in `ownership.py` (`revoke()` 11 survivors, `_mark_terminal()` 9 survivors, 2 genuine `acquire_and_activate()` survivors — final-handle `feature_subject_id` corruption and the pre-catch-up `_committed_frontier` reset), all classified `TEST_GAP` (materially undertested public-contract behavior, not message-text). 3 new behaviorally-named tests added (`test_revoke_transitions_active_owner_to_revoked_with_correct_handle_and_fences_authority`, `test_revoke_on_never_acquired_owner_marks_terminal_without_a_handle`, `test_failed_catch_up_marks_terminal_with_correct_revoked_handle_and_fences_authority`); no production/tooling/dependency changes. Targeted mutation reruns (fresh disposable venv, `python -m tooling run <id>`) against the new test boundary: **22/22 selected survivors SURVIVED → killed**, zero residual. Estimated Condition-1 numerator: 2155 + 22 = **2177**; estimated raw score **82.80715...% (2177/2629)** — still `< 87.001959503592%`, Condition 1 remains `FAIL — criteria`; remaining approximate gap to the minimum threshold numerator 2288 narrows from 133 to **111**. Full 2629-mutant formal remeasurement was explicitly NOT run this wave (targeted-only, per scope). Condition 2 is unchanged at `FAIL / PARTIALLY SATISFIED — 42/170 resolved` (no historical identity accounting altered by this wave). Condition 3 unchanged `SATISFIED — REVIEW A VALIDATED`. `P3-FEATURE-QG-EVID-03` remains `OPEN/FAIL`. Feature Engine remains NOT APPROVED; LIVE remains NOT_AUTHORIZED. | ~~None — ordinary test-writing against already-identified, already-cited mutant IDs~~ Superseded — see current-boundary evidence-003 record above; Wave 1 above additionally remediated a 22-mutant `ownership.py` cluster, test-only | ~~A fresh Step-9-style formal measurement shows raw score ≥87.001959503592% **and** all 170 pinned identities individually killed/confirmed_timeout or governedly reclassified (proposal §4.1)~~ Superseded — the next remediation task must be designed from evidence-003's own actual current mutant population, not the stale 170-ID set (out of scope for this correction); further high-yield waves against the remaining current-survivor population are the path to Condition 1 closure |
| `EVID-03` (current-boundary mutation-surface blind spot, 9-method approved fault-injection target population) | Test-effectiveness — mutation-surface completeness | ~~**NEEDS_GOVERNED_DESIGN_OR_MECHANISM** — 5 high-materiality methods structurally outside mutmut 3.7.0's mutation surface; no qualifying supplemental mechanism/fault-injection/risk-acceptance evidence exists~~ **STALE — superseded.** The mechanism (Testing Convention v0.16/v0.17 §5c path (ii)) is Approved (`feature-engine-mutation-surface-completeness-design-001.md`), extended to a current-boundary 9-method/14-fault population by Amendment 001 (`...design-001-amendment-001.md`, `APPROVED — DESIGN AMENDMENT EFFECTIVE`, including Bounded Correction 002 for `FI-INPUTMERGE-POSTINIT-01`). Current-boundary formal fault-injection evidence: `feature-engine-mutation-surface-completeness-evidence-003.json` — **14/14 approved faults DETECTED, 9/9 target methods qualify**. ChatGPT Review A: CLEAN — 0 Blocker / 0 Major / 0 Minor, R1. **Condition 3: `SATISFIED — REVIEW A VALIDATED`.** Historical `evidence-001.json`/`evidence-002.json` (5-method, stale src/tests boundary) remain immutable, unaffected. Condition 3's own satisfaction does **not** close EVID-03 overall — Condition 1 remains `FAIL — criteria` and Condition 2 remains partially unresolved (see row above and the material-gap identity-resolution candidate: `feature-engine-mutation-material-gap-identity-resolution-001.json`). | Condition-2 identity resolution (row above); no further Condition-3 work needed | Condition 3 satisfied; `P3-FEATURE-QG-EVID-03` remains OPEN/FAIL pending Condition 1 and Condition 2 |
| `EVID-04` | I-2 Decision Parity / Tier-1 Parity Test | **BLOCKED_BY_EXTERNAL_DEPENDENCY** | I-2's own Verification (golden event-log test, canonical semantic-decision hash comparison across all 4 execution modes at the **Decision** layer) cannot be performed — no Decision Engine/Strategy Plugin Host exists anywhere in the repository (confirmed: `python/`, `go/` contain only feature-engine, raw-regime-engine, structure-engine, market-data-ingestion, market-reference-service) | Decision Engine + a parity harness (Chapter 14 §14.2 sequence) | Decision Engine exists and a parity harness reproduces the same canonical Decision hash across Replay/Backtest/Paper/Live for a real scenario touching Feature Engine's own output |
| `EVID-05` | I-5 Decision-Time Observable Dependency | **NEEDS_GOVERNED_DESIGN_OR_MECHANISM** (split — see §2) | (a) no self-contained-replay test proves `on_candle`/`on_swing_confirmed`/etc. never re-touch the filesystem after construction-time authority resolution; (b) `ComputationCursor` carries `input_contract_ref`/`stream_registry_version` (identity/version strings) but no content-identity **checksum** referenced from the event, so I-5's "checksum của mọi artifact phải khớp" clause is structurally unverifiable today | (a) none — test-only, exercises already-existing cached-authority design; (b) a schema/design decision — plausibly an Event-Schema-adjacent change requiring a **fresh Chapter 0 §4b run** | (a) a self-contained replay test passes with network/filesystem cut after materialization; (b) either `ComputationCursor` (or an equivalent persisted-evidence mechanism) carries a verifiable content-identity checksum, checked against the resolved authority at replay time |
| `EVID-06` | I-6 Fail-Safe by Scope | **OPEN — PARTIALLY SATISFIED / BLOCKED_BY_EXTERNAL_DEPENDENCY** (§9.9: interpretation Review A CLEAN 0/0/0, all four Major findings CLOSED — REVIEW A VALIDATED; Feature-local fault-injection evidence `SATISFIED — REVIEW A VALIDATED` at exact Commit `2cee6e2cfd9538955c9591663a527b96c80e347d` (Review A CLEAN 0/0/0); platform risk-not-increased assertion remains `BLOCKED_BY_EXTERNAL_DEPENDENCY`, never `CLOSED — PASS`) | I-6's actual Verification is fault injection per scope + blast-radius confirmation + a risk-not-increased assertion "theo risk metric/policy authoritative" — Feature Engine (a pure Compute Engine, no risk/exposure semantics of its own) has no resolved interpretation of how "risk-not-increased" applies to it at all | The interpretation is fully derivable, Feature-Engine-only, from already-EFFECTIVE authority — I-6 itself (Locked) + I-9's own Scope boundary line (Locked) + Approved ADR-043's own ownership/fail-closed semantics (Draft `feature.md` cited only as supporting current-model context, never as the binding source, §9.1) — **`ADR_NOT_REQUIRED`**, not `ADR_REQUIRED`. Feature-local fault-injection evidence is now `SATISFIED — REVIEW A VALIDATED` (§9.9). | Feature-local evidence `SATISFIED — REVIEW A VALIDATED` (§9.9) — the platform risk-not-increased assertion remains a SEPARATE, externally-blocked dependency (no Risk Gateway exists); `EVID-06` may close only once that dependency resolves |
| `EVID-07` | I-13 State Transition Integrity / property-based evidence | **NEEDS_GOVERNED_DESIGN_OR_MECHANISM** | No Python property-based testing framework is approved or installed anywhere in the repository (confirmed: zero "hypothesis" references in `testing.md` or any `pyproject.toml`) — I-13's Verification explicitly requires "Property-based test trên transition graph authoritative" | A full governed mechanism-selection sequence, mirroring Testing Convention v0.16's own already-completed mutmut precedent (candidate authoring → Review A/B → Product Owner decision → install/pin → measurement) | A property-based framework is Approved, installed, pinned, and produces transition-graph/illegal-transition/concurrent-transition/replay-reconstruction evidence for Feature Engine's own state-machine entities (e.g. `_WindowLineage`'s VALID/PENDING_CORRECTION lifecycle, `FeatureCurrentView`'s row lifecycle) |
| `EVID-08` | I-1 Explainability / Decision-Pipeline trace completeness | **BLOCKED_BY_EXTERNAL_DEPENDENCY** | I-1's Verification requires 100% trace-completeness across "Toàn bộ Decision Pipeline (Structure/Regime/Feature → Strategy → Decision → Risk Gateway → Execution)" — Strategy/Decision/Risk Gateway/Execution Engine are all unbuilt | Full Decision/Risk/Execution evidence path (superset of EVID-04's own dependency) | The complete pipeline exists and produces production Decision/Risk Action evidence; Feature-local causation evidence (`causation_refs`, `input_fact_refs`, `computation_cursor`) already exists and is preserved as supporting-only evidence, never sufficient alone |

## 2. Two evidence-fidelity corrections made during this planning pass

Freshly re-verifying each finding's factual premise against current repository
state (not restated uncritically) surfaced two corrections, neither of which
changes any finding's `FAIL — evidence` disposition:

1. **`EVID-06`'s "zero test coverage" premise is now stale.** Direct
   inspection of `tests/test_current_view.py`, `tests/test_regime_passthrough.py`,
   and `tests/test_swing_distance.py` shows all 4 `ForeignScopeError` raise
   sites now DO have ordinary example-based coverage
   (`test_foreign_scope_event_rejected`, `test_foreign_scope_regime_fact_rejected`,
   `test_foreign_scope_candle_rejected`, `test_foreign_scope_swing_confirmed_rejected`
   — added, per their own code comments, as branch-coverage remediation for
   `P3-FEATURE-QG-COV-01`, explicitly self-documented as "factual overlap
   only, not a claim of EVID-06 closure"). This does not close EVID-06 — per
   the already-recorded I-6 clarification, ordinary exception-raising tests
   are supporting evidence only; the actual fault-injection/blast-radius/
   risk-not-increased Verification remains entirely unaddressed — but the
   blocker-matrix row above states the CURRENT gap precisely (interpretation
   + fault-injection design) rather than repeating the outdated "zero
   coverage" framing.
2. **`EVID-05`'s dependency is confirmed real by direct code reading, not
   assumed.** `ComputationCursor` (current_view.py/contracts.py-adjacent
   structures) was independently checked: it carries `input_contract_ref`
   (an `{contract_id, contract_version}` identity pair) and
   `stream_registry_version` (a version string) — genuinely no
   content-identity checksum field. `VerifiedInputContractAuthority` DOES
   compute `input_contract_content_id`/`stream_registry_content_id`
   checksums at resolution time, but they are not threaded into the
   persisted, replay-relevant cursor. This confirms the finding's own
   "Required follow-up" text and justifies classifying part (b) as a
   genuine schema-adjacent design gap, not merely a missing test.

## 3. Dependency graph / critical path

```text
EVID-03(a) raw score/170 IDs  ──────────────────────────────▶ [independent, ACTIONABLE_NOW]
EVID-03(b) blind-spot path decision ──▶ blind-spot evidence authored ──▶ [independent]
EVID-05(a) self-contained replay test ────────────────────────▶ [independent, ACTIONABLE_NOW]
EVID-05(b) checksum/schema design ──▶ fresh SS4b run ──▶ implementation ──▶ replay-checksum test ──▶ [independent]
EVID-06 risk-model-applicability interpretation (RESOLVED §9, ADR_NOT_REQUIRED) ──▶ fault-injection test design (§9, this transaction) ──▶ tests ──▶ [independent]
EVID-07 property-based mechanism candidate ──▶ Review A/B ──▶ PO decision ──▶ install/pin ──▶ tests ──▶ [independent]

EVID-04 Decision Parity  ◀── BLOCKED ── Decision Engine + Strategy Plugin Host must exist (Chapter 14 SS14.2) ── external, outside Feature Engine's own remediation scope
EVID-08 I-1 trace completeness ◀── BLOCKED ── Decision Engine + Risk Gateway + Execution Engine must ALL exist (superset of EVID-04's dependency) ── external, longest pole
```

**Critical path:** `EVID-08` has the longest, strictly-superset external
dependency (Decision Engine **and** Risk Gateway **and** Execution Engine);
`EVID-04` depends on a subset of that same chain (Decision Engine alone,
plus a parity harness). Neither can be shortened by any action internal to
Feature Engine. The four remaining findings (`EVID-03`, `EVID-05`, `EVID-06`,
`EVID-07`) are **mutually independent** of each other and of `EVID-04`/`EVID-08`
— none blocks or is blocked by any other.

## 4. Ordered remediation sequence

1. **Immediately, in parallel:** `EVID-03(a)` (material-gap test additions)
   and `EVID-05(a)` (self-contained replay test) — both `ACTIONABLE_NOW`,
   zero design prerequisites, zero cross-dependency.
2. **In parallel with step 1, as separate governed transactions:** initiate
   the design/decision work for `EVID-03(b)` (blind-spot path selection),
   `EVID-05(b)` (checksum/schema design — must rerun Chapter 0 §4b fresh
   before any implementation), `EVID-06` (risk-model-applicability
   interpretation — **RESOLVED §9, this transaction: `ADR_NOT_REQUIRED`,
   not the previously-assumed likely `ADR_REQUIRED`** — proceed directly
   to fault-injection test design/authoring, no ADR/Review-B/PO-decision
   step in between), and `EVID-07` (property-based mechanism candidate
   authoring, mirroring the mutmut precedent's own Step 1 candidate stage
   — since resolved: `P3-FEATURE-QG-EVID-07` is now `CLOSED — PASS`).
   These four are independent efforts that can proceed on separate tracks
   without contention.
3. **Once each design/decision from step 2 resolves:** author the
   corresponding tests/implementation for that specific finding, then a
   dedicated formal evidence transaction for that dimension (mirroring the
   Step-9 pattern already established for EVID-03).
4. **`EVID-04`/`EVID-08`:** do not start. Track as externally blocked (see
   §5's stop/unblock conditions). Revisit when Phase 3's Decision Engine
   (and, for EVID-08, Risk Gateway/Execution Engine) build reaches a point
   where a parity harness / trace-completeness evidence transaction becomes
   feasible — this is a Phase-3-sequencing question, not a Feature-Engine
   remediation task.

## 5. Parallelizable work

`EVID-03(a)`, `EVID-03(b)`-design, `EVID-05(a)`, `EVID-05(b)`-design,
`EVID-06`-interpretation, and `EVID-07`-candidate can all be worked
**simultaneously** by separate governed transactions — none reads or writes
state the others depend on. The only sequencing constraint within each
finding is design-before-implementation-before-formal-evidence (steps 2→3
above); there is no cross-finding sequencing constraint among these six.

## 6. Explicit stop/unblock conditions for externally-blocked items

```text
EVID-04 — STOP condition (do not attempt now): no Decision Engine or
  Strategy Plugin Host exists in this repository.
  UNBLOCK condition: Decision Engine reaches a state where it can process a
  real event log end-to-end AND a parity test harness exists comparing
  canonical Decision hashes across Replay/Backtest/Paper/Live.
EVID-08 — STOP condition (do not attempt now): Strategy/Decision/Risk
  Gateway/Execution Engine are all unbuilt.
  UNBLOCK condition: the full Decision/Risk/Execution evidence path exists
  AND produces real production Decision/Risk Action traces that a
  Chapter-2 I-1 100%-trace-completeness verification can be run against.
  This is a STRICT SUPERSET of EVID-04's own unblock condition -- EVID-08
  cannot unblock before EVID-04 does.
```

Neither condition is evaluated as met or attempted-toward by this plan.

## 7. Explicitly NOT recommended

Per this task's own instruction, and consistent with Testing Convention
v0.16's own anti-gaming discipline: this plan does **not** recommend
weakening the approved 87.001959503592% / 170-identity threshold merely
because Feature Engine currently fails it, does not recommend substituting
same-process determinism for `EVID-04`'s genuine cross-execution-mode parity
requirement, and does not recommend closing `EVID-06` via a
`ForeignScopeError` unit test alone (per §2's correction, such tests already
exist and are already, correctly, recorded as insufficient).

## 8. Single best next governed transaction

**Recommended: a bounded, test-only remediation transaction for `EVID-03(a)`**
— closing as many of the 170 pinned material-gap mutant identities as
possible, prioritized by the Step-4 analysis's own duplication data: **22 of
the 30 functions containing material-gap mutants each contain ≥2, together
covering 162 of the 170 (95%)** — independently re-verified during this
planning pass. The top concentrations: `SwingDistanceFeatureEngine._recompute`
(18), `._invalidate_and_replace` (16), `RegimePassthroughFeatureEngine.
_emit_replacement` (15), `._emit_invalidation` (13), `FeatureCurrentView.current`
(12), `SwingDistanceFeatureEngine._emit_replacement_only` (12). A disciplined
test-writing pass targeting these ~20-30 functions (not 170 independent
efforts) is expected to close the large majority of the 170, followed by a
fresh Step-9-style formal measurement to confirm.

This is the recommended next transaction because it is the only blocker that
is (a) fully `ACTIONABLE_NOW` with zero design/mechanism/ADR prerequisite,
(b) already has an exact, repository-pinned target list (the 170 mutant IDs
in `feature-engine-mutation-baseline-001-analysis.md` §1.6), and (c) directly
moves the one dimension with an already-approved, already-EFFECTIVE numeric
gate — no other blocker has a comparably concrete, immediately-startable
scope.

## 9. `EVID-06` applicability / fail-safe design interpretation

> **Current status (R0 bookkeeping, this transaction):** Review A of the Feature-local EVID-06 fault-injection evidence (executable boundary `2cee6e2cfd9538955c9591663a527b96c80e347d`) returned **CLEAN — 0 Blocker / 0 Major / 0 Minor**. Feature-local fail-safe evidence: **`SATISFIED — REVIEW A VALIDATED`**. Full `P3-FEATURE-QG-EVID-06` remains **`OPEN — PARTIALLY SATISFIED / BLOCKED_BY_EXTERNAL_DEPENDENCY`** — the platform risk-not-increased assertion is unaffected, still `BLOCKED_BY_EXTERNAL_DEPENDENCY` (no Risk Gateway/Decision Pipeline exists). No new review performed by this transaction; reasoning not duplicated here (§9.9 below carries the full record, now updated in place).

> **Status (superseded by the entry above — historical, left unedited for the record):** final bounded Review A re-review of correction 001 (below) returned **CLEAN — 0 Blocker / 0 Major / 0 Minor**, Risk `R1`, `ADR_NOT_REQUIRED`. `P3-FEATURE-QG-EVID06-A-MAJ-01` through `-04` are all **CLOSED — REVIEW A VALIDATED**. This transaction additionally produces the Feature-local half of I-6's own formal evidence — fault injection, blast-radius correctness, no invalid authoritative commit, committed-history preservation, bounded recovery — against exact executable boundary `2cee6e2cfd9538955c9591663a527b96c80e347d` (full record: §9.9). `P3-FEATURE-QG-EVID-06` is recorded **`OPEN — PARTIALLY SATISFIED / BLOCKED_BY_EXTERNAL_DEPENDENCY`** — NEVER `CLOSED — PASS` — because the platform-level risk-not-increased assertion remains externally blocked (no Risk Gateway/Decision Pipeline exists). This transaction does not self-validate its own evidence as Review-A-sufficient; that determination is Review A's own, per Chapter 0 §3.

> **Bounded correction 001 (historical, left unedited for the record) — vai trò: `Feature Engine EVID-06 Applicability / Fail-Safe Design Bounded Correction Executor`.** Review A of §9 (as originally authored) returned `REVISION_REQUIRED — 0 Blocker / 4 Major / 0 Minor`, Risk `R1`: `P3-FEATURE-QG-EVID06-A-MAJ-01` (§9.1 cited Draft `feature.md` as if it were Locked/binding authority), `-MAJ-02` (§9.2/§9.3 claimed a WINDOW fail-safe tier and a blanket "every fail-closed check runs before mutation" that current engine code does not actually support — `_check_recorded_time` mutates subject-wide `_last_input_recorded_time` BEFORE the later lineage check that raises `FeatureLineageError`), `-MAJ-03` (§9.3/§9.6's shared-authority matrix row conflated construction-time provider-resolution failure with runtime frontier/cursor validation against an already-cached authority — two distinct fault classes with two distinct injection points and blast radii), `-MAJ-04` (§9.4 did not yet state the exact required EVID-06 closure disposition — local Feature Engine evidence passing must never be written as `P3-FEATURE-QG-EVID-06 = CLOSED — PASS` while the mandatory risk-not-increased assertion remains externally blocked). All four remediated below, in place, re-grounded against fresh direct source reads (`regime_passthrough.py` `prepare_regime_classified`/`_check_recorded_time`, `contracts.py` `resolve_computation_cursor`, `docs/domain/feature.md` frontmatter, `docs/adr/ADR-043.md` semantics 1/5, `docs/architecture/module-registry.yaml` frontmatter) — none self-closed here; closure is Review A's own re-review determination, per Chapter 0 §3. No ADR authored, no Review B, no Product Owner decision, no production/test code touched by this correction.
>
> `P3-FEATURE-QG-EVID06-A-MAJ-01: REMEDIATED — PENDING REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID06-A-MAJ-02: REMEDIATED — PENDING REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID06-A-MAJ-03: REMEDIATED — PENDING REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID06-A-MAJ-04: REMEDIATED — PENDING REVIEW A RE-REVIEW`

**Vai trò: `Feature Engine EVID-06 Applicability / Fail-Safe Design Executor`.** Resolves ONLY the semantic/applicability question needed to make `EVID-06` testable — does NOT write fault-injection tests, does NOT close `EVID-06`, does NOT author an ADR, does NOT modify production code/Constitution/Domain Contract/Risk semantics. Fresh authority read this transaction (superseding this plan's own earlier, unverified ">1 module → likely `ADR_REQUIRED`" guess at the §1 row/§4 step-2 text above, now struck through and corrected in place): `docs/constitution/02-platform-invariants.md` I-6 (§112-126) and I-9 (§158-172, specifically its Scope line); `docs/constitution/13-quality-gates.md` §13.2/§13.4-13.6 (Tier 1, I-6 evidence row, Chaos/fault-injection category trigger); `docs/constitution/07-module-taxonomy.md` §I-6 cross-reference (line 79); `docs/domain/feature.md` (subject/scope identity, existing fail-closed discipline already present at §4/replay-preparation); `docs/architecture/module-registry.yaml` (`feature-engine` entry, `quality_tier: Tier 1`, `depends_on`); `python/feature-engine/README.md`; `python/feature-engine/src/feature_engine/{errors.py, ownership.py, regime_passthrough.py, swing_distance.py, current_view.py, authority_resolver.py}` (full read); `python/feature-engine/tests/{test_ownership.py, test_regime_passthrough.py, test_swing_distance.py, test_current_view.py}` (representative fault-path tests); `docs/adr/ADR-043.md` (no I-6/fail-safe language present — checked, not assumed); grep across every ADR/architecture doc for "I-6"/fail-safe/degraded-mode/risk-boundary authority (no Feature-Engine-specific or Compute-Engine-class-wide fail-safe ADR exists anywhere in the repository).

### 9.1 Key Question 1 — is existing authority sufficient?

**`-MAJ-01` correction notice:** the original §9.1 (below, corrected in place) leaned on `docs/domain/feature.md` as if it were binding, Locked-equivalent authority. Freshly re-verified this transaction: `feature.md` frontmatter reads `version: "0.6"`, `status: Draft`, `approved_by: null`, `approved_at: null` — it is **not** Locked, **not** Approved, and carries no binding authority equivalent to Constitution or an Approved ADR. It is not discarded — it remains cited below, explicitly labeled as **current Draft Domain Contract / current repository domain model**, useful for implementation/domain context, but it is never the authority ROOT that justifies a governed conclusion. Every claim below is re-grounded in text that is actually effective: I-6/I-9 (Constitution, Locked), ADR-043 (Approved, v0.2), and `module-registry.yaml` (cited only for the specific facts Chapter 13 §13.4 already treats it as authoritative for — module classification/tier — not as a Locked document in its own right; its own frontmatter itself reads "status: Draft, NOT Approved/Locked" at the package-lifecycle level, separate from its individually Product-Owner-approved `quality_tier` field pin).

**Yes, existing authority is sufficient.** No new authority is created or required by this interpretation; `no new authority → no ADR` applies. The interpretation is a direct, single-module reading of already-EFFECTIVE authority:

- I-6 itself (Chapter 2, **Locked**) is self-scoping: `Scope: Mọi Compute Engine, Projection, Runtime Service` — Feature Engine (`module_type: compute_engine`, per `module-registry.yaml`'s own entry) is directly, unambiguously in scope. No new invariant text is needed to establish applicability.
- I-9's own Scope line (Chapter 2, **Locked**) already draws the exact boundary this finding needs: *"ranh giới (boundary) giữa Feature Engine (analytical float được phép) và Execution/Ledger (bắt buộc lossless decimal từ đầu đến cuối)"* — i.e. Constitution itself, in already-Locked text, states that Feature Engine's outputs are analytical (pre-financial), not financial/risk values. This single Locked line resolves most of Key Question 3 without inventing anything and without relying on `feature.md` at all.
- ADR-043 (**Approved**, v0.2) is the actual binding runtime/isolation authority for ownership/concurrency, not `feature.md`. Its own semantics, verified fresh this transaction: semantic 1 — *"Per-subject exclusive ownership. For any `feature_subject_id`, at most one runtime owner may hold authority to validate and emit authoritative Feature transitions at any instant. Different subjects may be owned by different owners concurrently — horizontal scale is by subject partitioning/affinity, not by a single global process."*; semantic 5 — *"Fail closed on uncertain ownership, state, or precedence. If the system cannot prove exclusive current ownership, authoritative state catch-up/current-head correctness, or a deterministic precedence between two competing attempts... that subject scope fails closed — no best-effort winner selection, no wall-clock election."* These two Approved-ADR sentences are the actual authority root for §9.3's subject-scope isolation floor and §9.2's fail-closed formulation — not `feature.md`'s own subject-identity prose (which remains true as domain fact/current-model context, feature.md §1, but is Draft, not the binding source). ADR-043's implementation (Review A CLEAN, README) fails closed at the ~30 identified fault points in §9.5, confirmed by direct source read.
- `module-registry.yaml`'s `feature-engine` entry (cited for module classification, per Chapter 13 §13.4's own "khi registry active, mapping resolve từ registry" treatment — the specific authority basis Chapter 13, Locked, grants it) confirms `module_type: compute_engine`, `owns_authoritative_state: true`, `quality_tier: Tier 1` (individually Product-Owner-approved field), and **no** `depends_on` edge toward Risk Gateway/Execution Engine/Decision Authority Service — Feature Engine is strictly upstream of any risk-bearing module, consuming only `market-data-ingestion`/`structure-engine`/`raw-regime-engine`.
- The remediation plan's own `EVID-04`/`EVID-08` findings (unchanged by this transaction) already confirm, as an independently-established repository fact, that **no Decision Engine, Risk Gateway, or Execution Engine exists anywhere in this repository yet** — so there is structurally no "authoritative risk metric/policy" reachable from Feature Engine to consult, today, by construction.
- `feature.md` (Draft, current repository domain model) is retained ONLY as supporting/current-model context for two facts that also independently follow from I-6/I-9/ADR-043 without it: (a) Feature Engine's own domain scope excludes trade signal/action recommendation/entry-exit setup (consistent with, not the source of, I-9's Locked analytical-float boundary); (b) `feature_subject_id`'s five-field identity composition (`instrument_id`, `venue_id`, `timeframe`, `feature_type`, `feature_definition_version`) is the same identity unit ADR-043 semantics 1 (Approved) already binds ownership exclusivity to — ADR-043 is the authority for the OWNERSHIP/isolation consequence; `feature.md` merely describes the identity fields as current implementation/domain fact, not as the binding source of the isolation guarantee.

None of the above required a new decision, a new cross-module contract, or an edit to any Locked/Approved document — every fact was already present in effective authority. The old plan's ">1 module, likely `ADR_REQUIRED`" framing (§1/§4, corrected in a prior transaction) does not survive contact with the source, and neither did the original §9.1's over-reliance on Draft `feature.md`, now corrected. No genuine architecture/authority gap exists — two or more materially different valid behaviors are NOT possible under current EFFECTIVE authority (I-6 + I-9 + ADR-043 + module-registry.yaml's specific authoritative fields); the interpretation below is the unique reading that authority implies.

### 9.2 Key Question 2 — safe-state interpretation for Feature Engine

**`-MAJ-02` correction notice:** the original §9.2 (corrected below) asserted "every fail-closed check runs BEFORE mutation/append." Freshly re-read this transaction, `regime_passthrough.py`'s `prepare_regime_classified` disproves this as a blanket claim: `_resolve_cursor`/`_check_scope`/`_check_contract`/dimension/version checks run first and ARE mutation-free (confirmed: `_check_scope`/`_check_contract`/`resolve_computation_cursor` read `self`/arguments only, never assign to `self`), but immediately after them, `self._check_recorded_time(fact.recorded_time)` (line 300) **unconditionally sets** `self._last_input_recorded_time = recorded_time` — a subject-wide field — BEFORE the subsequent lineage-key lookup (line 302 onward) that may still raise `FeatureLineageError`/`EvidenceReferenceConflictError`. A rejected input for one window CAN therefore durably advance subject-shared `_last_input_recorded_time`, which could cause a LATER, otherwise-legitimate input for a DIFFERENT window of the SAME subject to be spuriously rejected by `_check_recorded_time`'s own monotonicity check. The corrected formulation below distinguishes the two kinds of state precisely instead of claiming a blanket pre-mutation guarantee.

The task's own candidate safe-state formulation is verified against source, not accepted blindly — the AUTHORITATIVE half holds exactly; the "preserve already-committed history" half is corrected to name the real distinction:

```text
When correctness cannot be proven for one Feature scope:
  fail closed for NEW authoritative Feature transitions in that scope
    (never emit a FeatureComputed/FeatureFactInvalidated built on
    unverified/unprovable state)
  do not fabricate/fallback/guess
    (no error class in §9.5 ever substitutes a default/guessed value;
    every one raises instead)
  do not advance authoritative Feature state/frontier
    (StaleOwnershipGenerationError: "no sequence consumed, no event
    appended, no local _lineage mutated"; UnprovenCatchUpError: a
    CATCHING_UP -> ACTIVE transition fails closed instead of advancing;
    CanonicalHistoryMismatchError: catch-up fails closed rather than
    preferring either candidate)
  preserve already-committed history vs. process-local prepare-side
    state -- these are DIFFERENT, verified separately, never conflated:
    AUTHORITATIVE COMMITTED HISTORY (already-appended FeatureComputed/
      FeatureFactInvalidated, already-successful FencedFeatureCommitter
      commits): never rolled back, never modified, by any fail-closed
      path identified in §9.5 -- confirmed by source read.
    PROCESS-LOCAL PREPARE-SIDE ANALYTICAL STATE (e.g.
      _last_input_recorded_time): MAY be mutated by a `prepare_*` call
      that later still raises for an UNRELATED reason (§9.3's own
      concrete example). This is safe, not a defect this transaction
      diagnoses or fixes: the mutation stays SUBJECT-bounded (never
      crosses to a different feature_subject_id's own instance
      attribute), and it can only cause a LATER legitimate input to be
      REJECTED more conservatively than strictly necessary -- it can
      never cause a wrong/uncertain value to be silently ACCEPTED as
      authoritative. The evidence suite (§9.6) must prove exactly this:
      any prepare-side mutation after a failed authoritative attempt
      either (a) remains bounded by the declared fail-safe scope (here:
      subject), or (b) causes that scope/owner to become unusable and
      require the governed recovery path already proven in ownership.py
      (fresh engine + fresh owner + fresh generation + catch-up).
  keep unrelated subjects operational
    (verified structurally, §9.3 -- separate engine/owner/committer
    instances per feature_subject_id; no shared mutable state links
    two DIFFERENT subjects anywhere in the reviewed source)
```

`FeatureCurrentView` is explicitly `"non-authoritative projection... never used as authoritative input anywhere"` (its own module docstring) — I-6's binding obligation for Feature Engine attaches to the **authoritative emission path** (`on_regime_classified`/`on_swing_confirmed`/`on_candle`/`process_certified_frontier` and the ADR-043 ownership/commit layer), consistent with `module-registry.yaml`'s own `owns_authoritative_state: true` classification, and with Chapter 7 §I-6's own text that non-critical projections are explicitly permitted more latitude to degrade — the view utility is not the primary surface this interpretation targets.

### 9.3 Smallest legitimate fault scope(s) and escalation

**`-MAJ-02` correction notice:** the original §9.3 (corrected below) asserted a WINDOW-level tier on the theory that `FeatureLineageError` "touches ONLY the W1 dict entry." Disproven this transaction by direct code read of `prepare_regime_classified` (§9.2's own correction): `_check_recorded_time` mutates the SUBJECT-wide `_last_input_recorded_time` field BEFORE the window-keyed lineage lookup that eventually raises `FeatureLineageError` — so the very fault previously cited as proof of window isolation is not, in fact, window-bounded; it carries a subject-level side effect. Re-derivation per the four required conditions (fail before any subject-shared mutable state changes; leave every other window's future legal transitions unaffected; not terminalize/fence the owner; not alter subject-level cursor/time/cache state): the zero-mutation checks (`_check_scope`, `_check_contract`, `_resolve_cursor`/`resolve_computation_cursor`, dimension/version checks) run BEFORE `_check_recorded_time` and never touch ANY window-keyed structure at all — they are not "window-scoped," they are stateless, per-call rejections that never reach window-level state in the first place. `FeatureLineageError` itself — the one fault that DOES touch a window-keyed dict entry — is reached only AFTER `_check_recorded_time`'s subject-wide mutation, so it does not satisfy condition 1 either. **No currently-implemented fault satisfies all four conditions at window granularity. WINDOW is removed as an EVID-06 fail-safe tier.** `FeatureCurrentView`'s own per-window dict isolation (noted in the prior draft) is a PROJECTION-layer property only — explicitly non-authoritative (§9.2) — and is not a substitute for authoritative-engine fail-safe evidence, per instruction. The authoritative isolation FLOOR is `feature_subject_id`, not window; three tiers remain, in ascending order — **not** the task's example "instrument" tier, which does not exist as a distinct boundary in this architecture (explained below):

```text
1. SUBJECT  (feature_subject_id -- one engine + one owner instance;
   the FLOOR tier -- default authoritative isolation unit)
   Evidence: both engines' own docstring, "One instance per Feature
   subject" (regime_passthrough.py, swing_distance.py); ADR-043
   (Approved) semantic 1 -- "at most one runtime owner may hold
   authority to validate and emit authoritative Feature transitions
   [per feature_subject_id] at any instant. Different subjects may be
   owned by different owners concurrently" -- and semantic 5 -- "that
   subject scope fails closed." AuthoritativeSubjectOwner/
   SubjectOwnershipAuthority/FencedFeatureCommitter are keyed per
   feature_subject_id, not per window; a fenced/terminal owner blocks
   ALL windows for that subject until a fresh engine + fresh owner +
   fresh generation + catch-up (ADR043-IMPL-A-MAJ-05). Within this
   tier, two sub-cases (§9.2's own distinction, not a finer tier):
   (a) faults that never touch subject-shared state at all before
   raising (ForeignScopeError and the other zero-mutation checks --
   the strictest possible instance of this tier, but still SUBJECT
   tier, not a separate WINDOW tier, since no window-keyed structure
   is ever consulted); (b) faults that DO mutate subject-shared
   process-local state (_last_input_recorded_time) before or instead
   of an authoritative append -- bounded to this SAME subject, never
   crossing to a different feature_subject_id.
   Faults: StaleOwnershipGenerationError, OwnershipAuthorityUnavailableError,
   DualOwnershipError, EngineNotPristineForCatchUpError,
   UnprovenCatchUpError, CanonicalHistoryMismatchError,
   NonMonotonicApplicationOrderError, ProviderFrontierMismatchError,
   IncompleteCertifiedFrontierError, ConflictingUpstreamEnvelopeError,
   RecordedTimeSourceViolationError, NonMonotonicRecordedTimeError,
   FeatureLineageError, EligibleSwingComputationDefectError,
   EvidenceCardinalityError, DefinitionVersionMismatchError,
   RegimeDimensionMismatchError, ProhibitedInputError,
   InvalidSwingEligibilityInputError, ForeignScopeError, and (§9's
   own `-MAJ-03` correction below) the RUNTIME half of frontier/cursor
   validation against an already-cached authority
   (RegistryContractMismatchError, StreamPositionsUniverseMismatchError,
   CursorRelationalInvariantViolationError, when raised against a
   caller-supplied EvaluationFrontier at an already-constructed
   engine's normal processing call, not at construction).

2. SHARED UPSTREAM AUTHORITY / DEFINITION  (every subject depending on
   the SAME Input Contract, Output Contract, or FeatureDefinition/
   formula RESOLUTION -- construction-time only, `-MAJ-03` corrected)
   Evidence: `InputContractAuthorityProvider.resolve(...)`/
   `OutputEventContractAuthorityProvider.resolve()` are each called
   EXACTLY ONCE, in `__init__`, for both engines (confirmed by source
   grep -- no other call site exists anywhere in regime_passthrough.py/
   swing_distance.py); the result is cached (`self._resolved_input_
   contract`, `self._output_authority`) and NEVER re-resolved by any
   runtime/processing call. A caller may legitimately share one
   provider instance across many engine constructions of the same
   feature_computation_profile -- so a newly-broken provider/artifact
   fails EVERY NEW construction attempt under that profile, but does
   NOT retroactively affect already-constructed subjects with
   already-cached authority (no rollback of running state; §9.6 rows
   split this precisely from the DIFFERENT runtime fault below).
   Escalates from subject scope only when the root cause is the SHARED
   authority artifact/definition's own RESOLUTION, not one subject's
   already-cached instance state or a malformed runtime argument.
   Faults (construction-time resolution only):
   UnresolvedComputationCursorAuthorityError,
   InputContractIdentityMismatchError, UnsupportedMergePolicyError,
   UnresolvedOutputContractAuthorityError,
   OutputEventContractUnresolvableError,
   OutputEventContractIdentityMismatchError,
   OutputEventContractNotPublishedError, OutputStreamEligibilityError.
   `RegistryContractMismatchError`/`StreamPositionsUniverseMismatchError`/
   `CursorRelationalInvariantViolationError` are REMOVED from this tier
   (`-MAJ-03` correction) -- they are raised inside
   `resolve_computation_cursor` against an ALREADY-cached, already-
   verified `VerifiedInputContractAuthority` and a caller-supplied
   `EvaluationFrontier` at NORMAL RUNTIME processing, never at provider
   resolution; their actual scope is the one subject/call being
   processed (tier 1), never the shared provider/artifact.
   `UnsupportedDistanceRepresentationError` (per-call, not construction)
   remains listed here only as a SUPPORTING fail-closed fact about
   distance-representation semantics, not a qualifying fault-injection
   target (same demotion as the formula case immediately below).
   `UnsupportedFeatureFormulaError` (construction-time, unconditional --
   `-MAJ-03` correction): a PERMANENTLY unsupported Candle formula
   capability is a design-time fail-closed boundary (no formula is
   ever authoritatively pinned for that `formula_id` anywhere in this
   repository), not a genuine injected runtime/resilience fault against
   an otherwise-healthy capability -- it remains supporting fail-closed
   evidence (feeding §9.5's catalog) but does NOT count as one of the
   minimum qualifying I-6 fault-injection rows in §9.6; a toggleable
   resolver/authority/ownership/history failure is preferred there.

3. WHOLE FEATURE ENGINE  (shared, stateless logic defect --
   e.g. a genuine bug in p_run_sort itself, not bad input)
   This is the architecture's actual ceiling, not "toàl platform":
   module-registry.yaml's own depends_on direction confirms Feature
   Engine is strictly DOWNSTREAM of market-data-ingestion/
   structure-engine/raw-regime-engine (consumes them, never the
   reverse) -- a Feature Engine-internal defect cannot structurally
   cascade UPSTREAM to those modules, and Feature Engine's own outputs
   reach only a non-authoritative projection (context-aggregator) and,
   eventually, an as-yet-unbuilt Decision layer -- consistent with I-6's
   own Prohibited-behavior clause against over-broad platform-wide
   stoppage for a non-execution-critical-boundary failure. For a truly
   shared PURE function (p_run_sort has no mutable shared state across
   calls), correctness is already the correct evidence question --
   NOT cross-subject isolation, which is structurally guaranteed for
   free by statelessness (no shared mutable state exists for one
   subject's fault to leak through) and is already covered by EVID-07's
   own property-based evidence, now CLOSED — PASS. No NEW fault-
   injection isolation test is meaningful here; escalation to this
   tier is a correctness question, not a blast-radius question.

NOT a distinct tier: "instrument" (`-MAJ-01` re-grounded: source + ADR-043,
  not feature.md, now the cited authority). `FeatureScope` (contracts.py)
  is a five-field dataclass -- instrument_id, venue_id, timeframe,
  feature_type, feature_definition_version -- and `feature_subject_id`
  is `deterministic_id("feature", ...)` over ALL FIVE fields (source
  read, this transaction): two scopes differing in ANY one field,
  including venue_id/timeframe while sharing instrument_id, produce a
  DIFFERENT feature_subject_id. Combined with ADR-043 (Approved)
  semantic 1's "different subjects may be owned by different owners
  concurrently," this is sufficient, already-effective authority (no
  feature.md reliance needed) to conclude: forcing an "instrument-wide"
  fault boundary distinct from subject/shared-authority scope would
  invent a tier current architecture does not provide, the same
  discipline this task's own instruction applies in the opposite
  direction (do not force per-subject isolation the architecture
  cannot provide).
```

### 9.4 Key Question 3 — "risk-not-increased" clause

**Interpretation A**, chosen because it is the only one existing authority supports (verified, not preselected):

```text
Feature Engine itself only proves: no new uncertain authoritative
  Feature output is emitted for the affected scope.
It does NOT itself assert financial risk, because it has none to
  assert -- I-9's own Scope line ALONE already draws this boundary in
  already-Locked Constitution text (§9.1): Feature Engine outputs
  analytical float, not financial/risk values. (feature.md's own
  out-of-scope declaration is consistent with this Locked boundary,
  supporting/current-model context only, per §9.1's `-MAJ-01`
  correction -- not itself required to reach this conclusion.)
Actual "risk-not-increased" verification (I-6's own "theo risk model
  authoritative" clause) belongs downstream to Risk Gateway/Decision
  Pipeline -- and is NOT locally measurable today, for the exact same
  reason EVID-04/EVID-08 are BLOCKED_BY_EXTERNAL_DEPENDENCY: no
  Decision Engine, Risk Gateway, or Execution Engine exists anywhere
  in this repository to hold or expose an authoritative risk model
  Feature Engine (or a test of it) could consult.
```

Interpretation B (a stronger Compute-Engine-local surrogate already defined by existing architecture) does not hold — no such surrogate risk metric exists anywhere in this repository's architecture docs, ADRs, or Feature Engine's own source; inventing one now would itself be new risk semantics, explicitly prohibited by this task. Interpretation C (current authority genuinely insufficient, cross-module interpretation must be governed first) does not hold either — §9.1 already shows existing authority is sufficient for the LOCAL half of the question; only the DOWNSTREAM half is blocked, and it is blocked by missing IMPLEMENTATION (no Risk Gateway exists), not by missing AUTHORITY (I-6/I-9 already say what would be required if a risk model existed).

**Explicit split, per instruction — the first is never claimed to be proof of the second:**

```text
LOCALLY TESTABLE NOW (Feature Engine's own EVID-06 evidence):
  - blast-radius correctness: a fault in one scope (subject/shared-
    authority, §9.3 -- WINDOW removed, `-MAJ-02`) fails that scope
    closed and leaves unrelated scopes fully operational (§9.6
    evidence matrix).
  - "no new uncertain authoritative Feature output is emitted": every
    identified fault class in §9.5 raises BEFORE any authoritative
    FeatureComputed/FeatureFactInvalidated append and BEFORE any
    successful FencedFeatureCommitter commit -- this narrower,
    ACCURATE claim holds (confirmed by source read); the broader
    "before any mutation whatsoever" claim does NOT hold (`-MAJ-02`,
    §9.2's own correction) and is not repeated here. To be proven by
    fault-injection tests, not merely exception-raising unit tests
    (the pre-existing gap, per §2's own correction above).
  - already-committed AUTHORITATIVE history (already-appended facts,
    already-successful commits) is never modified/rolled back by a
    fail-safe action (structural: no fault path in §9.5 mutates a
    prior authoritative fact) -- distinct from process-local
    prepare-side state, which MAY mutate within the bound scope
    (§9.2's corrected formulation).

EXTERNALLY BLOCKED (platform-level financial risk assertion,
  NOT locally provable, tracked as a NEW EVID-06 sub-dependency
  alongside EVID-04/EVID-08 -- NOT closed, NOT attempted by fault-
  injection tests written against Feature Engine alone):
  - "does this fail-safe action not increase risk per an authoritative
    risk model/policy" -- requires a Risk Gateway/Decision Pipeline
    that does not exist in this repository (same blocker class as
    EVID-04/EVID-08). Feature Engine emitting nothing new for an
    affected scope is a NECESSARY precondition for downstream risk not
    increasing, but is NOT a platform-level risk-not-increased proof
    by itself -- the two must never be conflated in the eventual
    EVID-06 evidence record (§9.4b's closure rule makes this binding).
```

#### 9.4b `-MAJ-04` correction — EVID-06 closure semantics (both halves of I-6 Verification are mandatory)

Locked I-6's own Verification clause requires BOTH: fault-injection/blast-radius evidence AND an assertion that the permitted fail-safe action does not increase risk per an authoritative risk metric/policy. The LOCAL half (above) can be evidenced now; the PLATFORM half is EXTERNALLY BLOCKED (no Risk Gateway exists). Therefore, once local fault-injection evidence (§9.6) passes, the correct disposition is **NOT** `P3-FEATURE-QG-EVID-06 = CLOSED — PASS` — `EVID-06` may close only when ALL mandatory I-6 verification evidence applicable to its gate has been produced. The correct future disposition, reusing this repository's own existing status vocabulary (`BLOCKED_BY_EXTERNAL_DEPENDENCY`, already used for `EVID-04`/`EVID-08` in this same document — no new lifecycle taxonomy invented) is:

```text
P3-FEATURE-QG-EVID-06:
  OPEN — PARTIALLY SATISFIED / BLOCKED_BY_EXTERNAL_DEPENDENCY

local Feature Engine fail-safe evidence (fault injection + blast
  radius + no-new-uncertain-authoritative-output + committed-history
  preservation, §9.6):
  SATISFIED (once the §9.6 evidence transaction, not this one,
  produces it -- NOT yet satisfied by this transaction).

platform risk-not-increased assertion (I-6's own "theo risk model
  authoritative" clause):
  BLOCKED — authoritative Risk Gateway/risk-policy execution path
  absent from this repository (same external-dependency class as
  EVID-04/EVID-08).
```

This split is a conceptual completeness distinction for evidence-recording purposes, not a new governance finding/process — it does not create a separate `EVID-06-LOCAL` finding identifier unless a future formal-evidence transaction's own authoring finds repository convention requires one at that time; this transaction does not decide that question.

### 9.5 Key Question 4 — fault catalog (grouped by scope, §9.3's corrected tiers; source-grounded, no invented types)

```text
SUBJECT scope (the floor -- `-MAJ-02` correction folds the former
  WINDOW-labeled faults in here; `-MAJ-03` correction moves the
  runtime frontier/cursor faults in here from shared-authority):
  ownership/fencing (ADR-043): StaleOwnershipGenerationError,
    OwnershipAuthorityUnavailableError, DualOwnershipError,
    EngineNotPristineForCatchUpError
  history/catch-up: UnprovenCatchUpError, CanonicalHistoryMismatchError,
    ProviderFrontierMismatchError, IncompleteCertifiedFrontierError
  P_run/apply-set (per-subject certified frontier):
    NonMonotonicApplicationOrderError, ConflictingUpstreamEnvelopeError
  recorded-time: RecordedTimeSourceViolationError,
    NonMonotonicRecordedTimeError (the latter's own mutate-before-
    lineage-check behavior is §9.2/§9.3's own corrected example)
  lineage/admissibility (window-keyed WITHIN this subject, but the
    isolation FLOOR that actually matters for I-6 is the subject, not
    the window -- `-MAJ-02`): FeatureLineageError,
    EligibleSwingComputationDefectError, EvidenceCardinalityError,
    DefinitionVersionMismatchError, RegimeDimensionMismatchError,
    ProhibitedInputError, InvalidSwingEligibilityInputError
  runtime frontier/cursor validation against an ALREADY-cached
    authority (`-MAJ-03`: moved here from shared-authority --
    RegistryContractMismatchError, StreamPositionsUniverseMismatchError,
    CursorRelationalInvariantViolationError, raised inside
    resolve_computation_cursor at normal per-call processing, never at
    provider resolution)
  scope admissibility: ForeignScopeError (zero subject-state touched
    at all -- the strictest instance of this tier, not a separate tier)

SHARED UPSTREAM AUTHORITY / DEFINITION scope (construction-time
  resolution only -- `-MAJ-03` correction):
  input-contract resolution: UnresolvedComputationCursorAuthorityError,
    InputContractIdentityMismatchError, UnsupportedMergePolicyError
  output-contract resolution: UnresolvedOutputContractAuthorityError,
    OutputEventContractUnresolvableError,
    OutputEventContractIdentityMismatchError,
    OutputEventContractNotPublishedError, OutputStreamEligibilityError
  formula/representation (supporting fail-closed evidence only, NOT a
    qualifying §9.6 fault-injection row -- `-MAJ-03`):
    UnsupportedFeatureFormulaError (construction-time, unconditional),
    UnsupportedDistanceRepresentationError

WHOLE FEATURE ENGINE scope (correctness, not isolation -- §9.3 tier 3):
  a genuine defect in shared, stateless p_run_sort logic itself --
  already the evidence question EVID-07 (CLOSED — PASS) answers, not a
  new fault-injection target.
```

Every entry above is a class that already exists in `errors.py` and is already raised at an identified, source-confirmed site. No fault type not present in source is included.

### 9.6 Key Question 5 — future fault-injection evidence matrix (design only, NOT implemented)

**`-MAJ-02`/`-MAJ-03` correction notice:** row [1] (WINDOW) is removed — no currently-implemented fault satisfies §9.3's four window-isolation conditions (§9.3's own correction). Row [5] (formerly a single mixed SHARED UPSTREAM AUTHORITY row) is split: the construction/resolution fault stays here as a genuine shared-authority row; the runtime frontier/cursor fault is relocated to a new SUBJECT-scope row [5], since its actual scope is the one subject/call being processed against an already-cached authority, never the shared provider (`-MAJ-03`). Row [6] (`UnsupportedFeatureFormulaError`) is removed as a qualifying row — a permanently-unsupported formula is a design-time boundary, not an injected fault against an otherwise-healthy capability (`-MAJ-03`); it remains catalogued in §9.5 as supporting evidence only. Former row [4] is split into two distinct catch-up fault semantics per instruction (unproven proof vs. canonical mismatch).

Sized deliberately between "one row per exception type" (too narrow -- mechanical, does not prove isolation, just re-proves what `test_ownership.py`/`test_regime_passthrough.py`/`test_swing_distance.py` already prove today) and "one blanket module-down test" (too broad -- would not distinguish which scope tier actually bounds the blast radius). Six toggleable resolver/authority/ownership/history/frontier rows across §9.3's two isolation-relevant tiers (subject; shared-authority) — no manufactured module-wide row (§9.3 tier 3 is a correctness question EVID-07 already answers, not fabricated here to fill a table):

```text
[1] SUBJECT -- StaleOwnershipGenerationError (fenced predecessor
    attempts commit after handoff)
  injected boundary: owner_0 (subject A, generation N) attempts
    FencedFeatureCommitter.commit(...) after owner_1 (generation N+1)
    has already acquired subject A.
  affected scope: subject A, generation N (owner_0) only.
  expected fail-safe: StaleOwnershipGenerationError raised; zero
    effect (already the exact assertion test_committer_rejects_
    stale_generation_with_zero_effect makes for ONE subject -- this
    matrix entry additionally requires a second, independent subject
    B constructed alongside).
  unaffected control: subject B (different feature_subject_id, SAME
    shared authority/provider/committer instances) continues normal
    acquire/process/commit throughout, unaffected by A's fencing.
  must-not-advance: committer_0.log for subject A unchanged; allocator
    sequence count for subject A unchanged; subject A's lineage
    unchanged by the rejected attempt.
  recovery: a fresh owner_1 (already holding generation N+1) continues
    normally -- no separate recovery action needed for A beyond the
    handoff that already occurred.
  proves: subject-level fencing does not leak into a second,
    independent subject sharing the same authority infrastructure.

[2] SUBJECT -- OwnershipAuthorityUnavailableError (owner goes
    permanently terminal after a prior uncertain commit outcome)
  injected boundary: a StaleOwnershipGenerationError (as in [2]) is
    allowed to mark owner_0 REVOKED/terminal for subject A.
  affected scope: subject A's owner_0 instance -- permanently, all
    windows of subject A blocked until a FRESH engine + fresh owner +
    fresh generation + catch-up (ADR043-IMPL-A-MAJ-05).
  expected fail-safe: every subsequent call on owner_0 raises
    OwnershipAuthorityUnavailableError, including re-acquire attempts.
  unaffected control: subject B, constructed independently, is
    entirely unaware of subject A's terminal owner.
  must-not-advance: subject A emits nothing further via owner_0; no
    partial/uncertain commit is ever treated as successful.
  recovery expectation: a genuinely FRESH engine_1 + fresh owner_1 +
    fresh generation for subject A, performing canonical catch-up
    (AuthoritativeLineageHistoryProvider), reconstructs subject A's
    lineage exactly and may resume authoritative work -- already
    proven for ONE subject by test_fresh_owner_and_fresh_engine_
    recover_canonical_state_after_prior_owner_goes_terminal; this
    matrix entry requires proving recovery of A happens without
    touching subject B's own independent, concurrently-running state.
  proves: permanent subject-level failure does not cascade, and
    recovery is subject-scoped, not module-wide.

[3] SUBJECT -- UnprovenCatchUpError (history provider cannot
    positively prove catch-up)
  injected boundary: AuthoritativeLineageHistoryProvider returns an
    incomplete/ambiguous result (neither a genuine event list nor
    positive proof of emptiness) for subject A's catch-up.
  affected scope: subject A's CATCHING_UP -> ACTIVE transition only.
  expected fail-safe: subject A's owner never reaches ACTIVE; no
    authoritative work is performed for A.
  unaffected control: subject B, catching up against its own
    correctly-resolving provider call (even if the SAME provider
    instance, a different subject_id argument), reaches ACTIVE and
    operates normally.
  must-not-advance: zero FeatureComputed/FeatureFactInvalidated
    emitted for A; fresh_allocator sequence count for A stays at zero.
  recovery: a corrected/complete provider response allows a fresh
    catch-up attempt to succeed normally.
  proves: an ambiguous PROOF failure for one subject does not block or
    corrupt a different subject's own, independently-resolving proof.

[4] SUBJECT -- CanonicalHistoryMismatchError (recomputed historical
    candidate diverges from the canonical committed record)
  injected boundary: AuthoritativeLineageHistoryProvider's canonical
    history for subject A does not match what PreparedTransition.
    reconcile recomputes from the SAME certified upstream replay
    (batch-length or content mismatch).
  affected scope: subject A's catch-up reconciliation only.
  expected fail-safe: CanonicalHistoryMismatchError raised; catch-up
    fails closed rather than silently preferring either the freshly
    recomputed candidate or the canonical record.
  unaffected control: subject B's own independent catch-up (correct,
    matching canonical/recomputed history) completes normally.
  must-not-advance: subject A's owner never reaches ACTIVE via this
    catch-up attempt; no authoritative work performed for A.
  recovery: a corrected canonical-history/upstream-replay input allows
    a fresh catch-up attempt for A to succeed normally.
  proves: a genuine catch-up MISMATCH (distinct fault semantics from
    [3]'s ambiguous/incomplete PROOF) is bounded to the one subject
    whose canonical record actually diverges.

[5] SUBJECT -- runtime frontier/cursor mismatch against an
    already-cached authority (`-MAJ-03`: RegistryContractMismatchError
    / StreamPositionsUniverseMismatchError /
    CursorRelationalInvariantViolationError)
  injected boundary: a malformed/incompatible EvaluationFrontier
    (wrong stream_registry_version, wrong stream_positions key set, or
    a relational-invariant violation) is passed to an ALREADY-
    constructed engine's normal processing call for subject A -- the
    engine's own cached VerifiedInputContractAuthority is untouched
    and correct; only the CALLER-SUPPLIED frontier for this one call
    is bad. This is explicitly NOT a provider-outage test (`-MAJ-03`)
    -- the provider/artifact is healthy throughout.
  affected scope: this one processing call for subject A.
  expected fail-safe: resolve_computation_cursor raises the applicable
    error; no ComputationCursor is assembled, no PreparedTransition
    constructed.
  unaffected control: a subsequent, correctly-formed frontier for
    subject A processes normally afterward (the engine's own cached
    authority was never invalidated by the bad call); subject B
    (own, independently-supplied frontier) is fully unaffected
    throughout.
  must-not-advance: no new authoritative output for subject A from the
    malformed-frontier call; engine's cached authority/lineage
    unchanged.
  recovery: none needed beyond supplying a correctly-formed frontier
    on the next call -- the engine itself was never made unusable.
  proves: a bad RUNTIME ARGUMENT for one subject's one call is
    distinct from a bad SHARED PROVIDER/ARTIFACT ([6] below) -- same
    error-type family, structurally different fault/injection point/
    blast radius, must never be tested as if interchangeable.

[6] SHARED UPSTREAM AUTHORITY -- construction-time Input/Output
    Contract resolver failure (`-MAJ-03` corrected: construction-time
    resolution ONLY, never mixed with [5]'s runtime fault)
  injected boundary: InputContractAuthorityProvider.resolve(...) (or
    OutputEventContractAuthorityProvider.resolve()) fails or returns
    an invalid authority for feature_type=X's shared provider instance
    -- simulating a broken/missing artifact at RESOLUTION time, before
    any engine for feature_type=X exists yet.
  affected scope: EVERY NEW engine construction attempt for
    feature_type=X using that provider, from the break onward.
  expected fail-safe: construction itself raises the applicable
    resolution error (UnresolvedComputationCursorAuthorityError /
    InputContractIdentityMismatchError / UnresolvedOutputContract
    AuthorityError / OutputEventContract* family); no new engine for
    feature_type=X becomes usable while the condition holds.
  unaffected control (two distinct controls, both required): (a) an
    engine for feature_type=X constructed and already caching valid
    authority BEFORE the break continues serving its already-resolved
    work normally -- cached, never re-resolved per-call, and (per [5]
    above) not even vulnerable to a runtime frontier fault touching
    this same provider; (b) a subject of feature_type=Y (a DIFFERENT
    Input/Output Contract provider instance) is fully unaffected
    regardless of construction order.
  must-not-advance: no new authoritative output for feature_type=X
    from any NEWLY-affected construction attempt.
  recovery: once the provider/artifact resolves correctly again, a
    fresh engine construction for feature_type=X succeeds normally;
    already-running engines were never affected and need no recovery.
  proves: shared-authority-scope faults are bounded by "which
    provider/artifact resolution is actually broken, and only for NEW
    construction," not "which subject" and not "which already-cached
    engine's ongoing runtime calls" -- the precise distinction [5] vs
    [6] makes structurally explicit (`-MAJ-03`).

Supporting fail-closed evidence, NOT a qualifying row above
  (`-MAJ-03`): `UnsupportedFeatureFormulaError` (construction-time,
  unconditional, CandleWindowFeatureEngine) is a PERMANENT design-time
  boundary -- no formula is ever authoritatively pinned for that
  `formula_id` anywhere in this repository, so there is no "otherwise-
  healthy capability" to toggle a fault into and back out of. It
  remains catalogued (§9.5) as supporting fail-closed evidence, and is
  deliberately excluded from the minimum qualifying fault-injection
  set — rows [1]-[6] above are all genuinely toggleable (a healthy
  capability can be made to fail and, where applicable, recover).

If a fault legitimately affects module-global authority (WHOLE FEATURE
  ENGINE tier, §9.3/§9.5), module-global failure IS correct and no
  per-subject isolation test should be forced onto it -- per
  instruction, and per §9.3's own statelessness argument for
  p_run_sort, already covered by EVID-07 (CLOSED — PASS), not
  re-tested here.
```

### 9.7 ADR Scope Rule (Chapter 0 §4b) — run fresh, not preselected

```text
Platform Invariant addition/edit:            NO -- I-6/I-9 text unchanged;
                                               this reads/applies it.
Event Schema change:                          NO.
Module Taxonomy / dependency-graph change:    NO -- module-registry.yaml
                                               untouched.
Governance/Approval-process change:           NO.
Decision affecting >1 module:                 NO -- explicitly scoped
                                               FEATURE-ENGINE-ONLY (same
                                               scoping discipline already
                                               established for the
                                               Hypothesis/Testing
                                               Convention v0.17 decision
                                               in this exact chain).
                                               Whether structure-engine/
                                               raw-regime-engine reach an
                                               identical conclusion is a
                                               SEPARATE question for
                                               their OWN future findings
                                               to independently derive --
                                               this transaction does not
                                               bind them, canonicalize a
                                               cross-module doctrine, or
                                               edit any shared authority
                                               document.
Hard to reverse:                              NO -- pure documentation/
                                               evidence-design; a future
                                               bounded correction can
                                               amend it, same discipline
                                               already used throughout
                                               this file's own §2.
Edit/supersede a Locked ADR:                  NO -- no ADR touched.
Materially significant module-internal
  decision (Optional criterion):              NO -- no contract change,
                                               no behavior change, no new
                                               test-execution mechanism/
                                               dependency/tool introduced
                                               (unlike the Hypothesis
                                               decision, which DID change
                                               test-execution behavior).
                                               This decision only reads
                                               already-Locked text and
                                               documents evidence design
                                               for FUTURE tests not yet
                                               written -- the same
                                               "evidence design feeding a
                                               future candidate" shape as
                                               this file's own §1-§8 and
                                               EVID-07 QG candidate's own
                                               §2 surface-identification
                                               work, neither of which was
                                               separately ADR-scored.

Result: ADR_NOT_REQUIRED.
```

Per instruction: the design only describes evidence for already-authoritative semantics — I-6/I-9 (Locked), ADR-043 (Approved), and the specific `module-registry.yaml` fields Chapter 13 already treats as authoritative once the registry is active (§9.1's `-MAJ-01` correction: Draft `feature.md` is never cited as the binding source here, only as supporting current-model context) — no ADR is authored by this transaction, none is required.

### 9.8 Not performed by bounded correction 001 (historical — superseded by §9.9 below)

```text
No fault-injection test authored. No production source file touched
  (verified `git diff --quiet -- python/feature-engine/src
  python/feature-engine/tests`, this transaction). No Constitution/
  Domain Contract/Risk-semantics edit. No ADR authored. No Review B,
  Risk Classification, or Product Owner decision performed. This
  transaction only CORRECTS §9's own interpretation/design in place,
  addressing `P3-FEATURE-QG-EVID06-A-MAJ-01`..`-04` (bounded correction
  001 banner, top of §9) — none of the four is self-closed here;
  closure of each is Review A's own re-review determination, per
  Chapter 0 §3.
  `P3-FEATURE-QG-EVID-06` disposition unchanged: still OPEN,
  `NEEDS_GOVERNED_DESIGN_OR_MECHANISM` — its interpretation sub-step is
  now RE-derived on corrected authority (§9.1-§9.6, this bounded
  correction), pending Review A re-review; fault-injection authoring
  and formal evidence remain a SEPARATE future governed transaction,
  and even once local evidence passes, `EVID-06` may NOT be written as
  `CLOSED — PASS` while the platform risk-not-increased assertion
  remains `BLOCKED_BY_EXTERNAL_DEPENDENCY` (§9.4b). Overall Feature
  Engine Chapter 13 Quality Gate: unchanged, FAIL — evidence
  (EVID-04/EVID-06/EVID-08 remain OPEN/blocking). Feature Engine module
  approval: NOT APPROVED (unaffected). LIVE: NOT_AUTHORIZED (unaffected).
```

**Next governed step (not performed by this transaction):** bounded Review A re-review of `P3-FEATURE-QG-EVID06-A-MAJ-01`..`-04`. If CLEAN, a separate Feature-local fault-injection implementation/evidence transaction may proceed to author the §9.6 matrix (and any additional rows Review A requests) against real Feature Engine source, then a formal Chapter 13 §13.9-style evidence transaction records measurement — but it must NOT claim full `P3-FEATURE-QG-EVID-06` closure while the mandatory platform risk-not-increased assertion remains externally blocked; the correct resulting disposition is §9.4b's `OPEN — PARTIALLY SATISFIED / BLOCKED_BY_EXTERNAL_DEPENDENCY`, not `CLOSED — PASS`.

### 9.9 Final Review A + Feature-local formal evidence record (this transaction)

**Final bounded Review A re-review of correction 001:** `CLEAN — 0 Blocker / 0 Major / 0 Minor`, Risk `R1`, ADR Scope `ADR_NOT_REQUIRED`.

```text
P3-FEATURE-QG-EVID06-A-MAJ-01: CLOSED — REVIEW A VALIDATED
P3-FEATURE-QG-EVID06-A-MAJ-02: CLOSED — REVIEW A VALIDATED
P3-FEATURE-QG-EVID06-A-MAJ-03: CLOSED — REVIEW A VALIDATED
P3-FEATURE-QG-EVID06-A-MAJ-04: CLOSED — REVIEW A VALIDATED
```

None self-closed by the correction executor — this is the recorded Review A determination itself, per Chapter 0 §3.

**Feature-local I-6 formal evidence — tested executable boundary:** `2cee6e2cfd9538955c9591663a527b96c80e347d` (Commit A, parent `a8a2794abcfba4786ff53b358187ffdb960e11ff` — the §9 bounded correction 001 docs-only boundary). Verified `main == origin/main == 2cee6e2c...` before AND after the qualifying run.

```text
Feature-local I-6 evidence: SATISFIED — REVIEW A VALIDATED
  (Review A: CLEAN — 0 Blocker / 0 Major / 0 Minor, executable boundary
  2cee6e2cfd9538955c9591663a527b96c80e347d — R0 bookkeeping recorded
  post-review; reasoning not duplicated here, see Review A's own record)

Covered (python/feature-engine/tests/test_i6_fail_safe_scope.py, 6 tests,
  all pass BOTH "affected scope fails safely" AND "unrelated control
  scope remains operational"):
  - subject stale/fencing isolation (Row 1:
    test_row1_stale_ownership_generation_isolates_to_subject_a)
  - terminal-owner isolation/recovery (Row 2:
    test_row2_terminal_owner_never_reacquires_and_recovery_via_fresh_
    owner_does_not_affect_subject_b)
  - unproven catch-up isolation/recovery (Row 3:
    test_row3_unproven_catch_up_terminalizes_owner_and_recovery_via_
    fresh_owner_does_not_affect_subject_b)
  - canonical-history mismatch isolation/recovery (Row 4:
    test_row4_canonical_history_mismatch_terminalizes_owner_and_recovery_
    via_fresh_owner_does_not_affect_subject_b)
  - runtime frontier/cursor mismatch fail-closed/recovery, explicitly NOT
    a provider outage (Row 5:
    test_row5_runtime_frontier_mismatch_fails_closed_then_correct_
    frontier_succeeds_without_affecting_subject_b)
  - shared Input Contract resolver construction-time blast radius (Row 6:
    test_row6_construction_time_input_contract_resolver_failure_isolates_
    to_new_constructions)
```

**Exact commands/results, against exact Commit A `2cee6e2c...`:**

```text
$ pytest -q tests/test_i6_fail_safe_scope.py
6 passed in 0.14s

$ pytest -q
394 passed in 1.41s
  (388 pre-existing + 6 new I-6 Feature-local fault-injection tests --
  zero regressions in any pre-existing test)

$ ruff check src tests
2 findings, BOTH pre-existing and unrelated (E501 line-too-long,
  src/feature_engine/authority_resolver.py:465 and :528 -- unchanged
  from every prior transaction in this chain; NOT introduced, NOT fixed,
  by this transaction). Ruff is therefore NOT claimed "clean" -- it is
  claimed "2 pre-existing, unrelated findings, unchanged."

$ mypy src tests
Success: no issues found in 35 source files.
```

No property test/fault-injection test discovered a production defect. No production source file was modified (verified `git diff --quiet -- python/feature-engine/src`, this transaction). No dependency version change.

**EVID-06 disposition (current, per R0 bookkeeping of the completed Review A result — §9.4b's own rule applied):**

```text
P3-FEATURE-QG-EVID-06:
  OPEN — PARTIALLY SATISFIED / BLOCKED_BY_EXTERNAL_DEPENDENCY

Feature-local fail-safe evidence:
  SATISFIED — REVIEW A VALIDATED
  (executable boundary 2cee6e2cfd9538955c9591663a527b96c80e347d,
  Review A: CLEAN — 0 Blocker / 0 Major / 0 Minor)

platform risk-not-increased assertion:
  BLOCKED_BY_EXTERNAL_DEPENDENCY (no Risk Gateway/Decision Pipeline
  exists anywhere in this repository)

Feature Engine module approval: NOT APPROVED (unaffected).
Phase 3 Approval Gate: NOT opened (unaffected).
LIVE: NOT_AUTHORIZED (unaffected).
```

`P3-FEATURE-QG-EVID-06` is explicitly NOT `CLOSED — PASS` — Review A validated only the Feature-local half; full closure requires the platform risk-not-increased assertion, which remains externally blocked. `EVID-04`/`EVID-08` are unaffected and not opened by this bookkeeping transaction.

**Not performed by this transaction:** no new review; no ADR; no Review B; no Product Owner decision; no Risk Classification transaction; no production source change (verified); no dependency change; no CI workflow; no module approval; no LIVE authorization; no claim of overall Feature Engine Chapter 13 Quality Gate PASS. Do not reopen Feature-local EVID-06 work — the next relevant transaction only becomes appropriate once a downstream authoritative risk path (Risk Gateway/Decision Pipeline) exists and the platform risk-not-increased assertion becomes executable.

**Next governed step (R0 bookkeeping update, this transaction):** bounded Review A of the Feature-local EVID-06 fault-injection evidence at exact Commit `2cee6e2cfd9538955c9591663a527b96c80e347d` completed — **CLEAN — 0 Blocker / 0 Major / 0 Minor**. Feature-local fail-safe evidence is now recorded `SATISFIED — REVIEW A VALIDATED`. Full `P3-FEATURE-QG-EVID-06` remains `OPEN — PARTIALLY SATISFIED / BLOCKED_BY_EXTERNAL_DEPENDENCY` until the platform risk-not-increased assertion becomes locally verifiable (i.e. until a Risk Gateway/Decision Pipeline exists) — no further Feature-local EVID-06 work is expected before then.
