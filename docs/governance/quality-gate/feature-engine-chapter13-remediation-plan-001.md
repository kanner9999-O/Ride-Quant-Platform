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
| `EVID-03` (raw score / 170 IDs) | Test-effectiveness — mutation score & material-gap identities | **ACTIONABLE_NOW** | 0/170 pinned material-gap mutants killed; raw score 75.898105813194% < 87.001959503592% | None — ordinary test-writing against already-identified, already-cited mutant IDs | A fresh Step-9-style formal measurement shows raw score ≥87.001959503592% **and** all 170 pinned identities individually killed/confirmed_timeout or governedly reclassified (proposal §4.1) |
| `EVID-03` (12-method blind spot) | Test-effectiveness — mutation-surface completeness | **NEEDS_GOVERNED_DESIGN_OR_MECHANISM** | 5 high-materiality methods structurally outside mutmut 3.7.0's mutation surface; no qualifying supplemental mechanism/fault-injection/risk-acceptance evidence exists | A governed decision on which of three paths to pursue (Testing Convention v0.16 §5c) | One of: (a) an accepted supplemental mutation-testing mechanism reaching decorated classes now exists; (b) governed deterministic fault-injection evidence is authored and pinned per method; (c) Product Owner explicitly records risk-acceptance naming the 5 residuals |
| `EVID-04` | I-2 Decision Parity / Tier-1 Parity Test | **BLOCKED_BY_EXTERNAL_DEPENDENCY** | I-2's own Verification (golden event-log test, canonical semantic-decision hash comparison across all 4 execution modes at the **Decision** layer) cannot be performed — no Decision Engine/Strategy Plugin Host exists anywhere in the repository (confirmed: `python/`, `go/` contain only feature-engine, raw-regime-engine, structure-engine, market-data-ingestion, market-reference-service) | Decision Engine + a parity harness (Chapter 14 §14.2 sequence) | Decision Engine exists and a parity harness reproduces the same canonical Decision hash across Replay/Backtest/Paper/Live for a real scenario touching Feature Engine's own output |
| `EVID-05` | I-5 Decision-Time Observable Dependency | **NEEDS_GOVERNED_DESIGN_OR_MECHANISM** (split — see §2) | (a) no self-contained-replay test proves `on_candle`/`on_swing_confirmed`/etc. never re-touch the filesystem after construction-time authority resolution; (b) `ComputationCursor` carries `input_contract_ref`/`stream_registry_version` (identity/version strings) but no content-identity **checksum** referenced from the event, so I-5's "checksum của mọi artifact phải khớp" clause is structurally unverifiable today | (a) none — test-only, exercises already-existing cached-authority design; (b) a schema/design decision — plausibly an Event-Schema-adjacent change requiring a **fresh Chapter 0 §4b run** | (a) a self-contained replay test passes with network/filesystem cut after materialization; (b) either `ComputationCursor` (or an equivalent persisted-evidence mechanism) carries a verifiable content-identity checksum, checked against the resolved authority at replay time |
| `EVID-06` | I-6 Fail-Safe by Scope | **NEEDS_GOVERNED_DESIGN_OR_MECHANISM** | I-6's actual Verification is fault injection per scope + blast-radius confirmation + a risk-not-increased assertion "theo risk metric/policy authoritative" — Feature Engine (a pure Compute Engine, no risk/exposure semantics of its own) has no resolved interpretation of how "risk-not-increased" applies to it at all | A design/interpretation decision (likely affecting every Compute-Engine-class module identically — structure-engine, raw-regime-engine, feature-engine — so plausibly `ADR_REQUIRED` under Chapter 0 §4b's ">1 module" trigger) | The interpretation decision is recorded, then genuine fault-injection tests (not merely exception-raising unit tests) are authored per applicable scope with blast-radius and risk-not-increased assertions |
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
EVID-06 risk-model-applicability interpretation (possible ADR) ──▶ fault-injection test design ──▶ tests ──▶ [independent]
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
   interpretation — check whether it rises to `ADR_REQUIRED` given likely
   >1-module effect), and `EVID-07` (property-based mechanism candidate
   authoring, mirroring the mutmut precedent's own Step 1 candidate stage).
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
