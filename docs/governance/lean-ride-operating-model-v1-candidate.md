---
id: lean-ride-operating-model-v1
title: "Lean Ride Operating Model v1 — Candidate"
version: "1.0"
status: Draft
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-09-22"
depends_on: ["00-governance", "11-adr-process", "12-approval-gates", "13-quality-gates", "14-roadmap"]
---

# Lean Ride Operating Model v1 — CANDIDATE (NOT ACTIVE)

**Status: Draft/Candidate.** This document is non-binding until Review A + Risk
Classification + an explicit Product Owner adoption decision complete (see
§8). It changes **zero** Governance/Approval semantics on its own — it is an
**operational efficiency layer sitting strictly inside** the space the
existing rules already treat as low-ceremony (R0/R1 default no-cross-check,
`G-REV` Semantic Sufficiency, `P3-TXN-001` fold-by-default, `P3-MODULE-
BATCH-001` batch containment). No Constitution chapter, ADR, Global Execution
Rule, or Phase rule is edited by this document.

## 0. What is preserved, verbatim

- Governance core: `PLAN → EXECUTE → VERIFY → REVIEW → DECIDE`, mapped onto
  the existing Decision Workflow (`00-governance.md` §3: Requirement → Review
  A → Risk Classification R0/R1/R2 → Product Owner Decision → ADR
  Accepted/Locked).
- Product Owner sole decision authority (`00-governance.md` §2/§12.2).
- Review A mandatory + Risk Classification mandatory (ADR-042 model).
- ADR Scope Rule (Chapter 0 §4b) — unchanged trigger list.
- All existing approved decisions/evidence — nothing here invalidates any
  prior artifact.
- Global Execution Rules `G-AUTH/G-VERIFY/G-ADR/G-TXN/G-REV/G-BUDGET/G-ID/
  G-QG/G-PHASE/G-ORCH` — unchanged, fully in force.

## 1. Lean workflow v1

The lean layer adds structure **on top of** PLAN→EXECUTE→VERIFY→REVIEW→DECIDE
without changing what each stage means:

| Stage | Today (unchanged) | Lean addition |
|---|---|---|
| PLAN | Task/transaction spec | Batched into a **Work Package (WP)** inside a **Milestone** — the new atomic planning unit, sized to a critical-path deliverable, not a single row/finding/mutant |
| EXECUTE | Executor performs bounded work | Internal commits/iterations inside ONE WP need no per-commit review cycle (`P3-MODULE-BATCH-001`, made explicit) |
| VERIFY | Fresh ground-truth check (`G-VERIFY-001`) | Performed **once** at WP completion, covering the WP's full delta |
| REVIEW | Review A + Risk Classification | **Batched**: one Review A per WP, sized to real aggregate risk — never per-row/per-mutant/per-artifact |
| DECIDE | Product Owner decision | Routed by Risk Classification: R0/R1 → no PO step unless Milestone-boundary or escalation; R2 / ADR-triggered / Milestone-complete → PO decision, delivered via the Dashboard (§5) or a direct escalation (§3) |

**New operating constraints:**

- **Work Package (WP)** — replaces micro-task routing. One WP = one coherent
  deliverable against one Quality Gate condition or one module artifact.
- **WIP limit = 1 in-flight WP per critical-path track** per executor/module.
  Prevents the parallel half-finished chains `P3-CORRECTION-CHAIN-001` exists
  to catch after the fact — this prevents most of them from starting.
- **Critical-path prioritization** — WPs ordered against the Roadmap
  dependency graph (Chapter 14 §14.2) and, within a module, against the
  module's own blocking Quality Gate condition first.
- **Batched Review A** — sized to the WP's aggregate semantic delta, per
  `G-REV-001`/Semantic Sufficiency, now a structural default rather than
  case-by-case judgment.
- **Milestone-level PO reporting** — PO sees one Dashboard update per
  Milestone checkpoint, not one report per transaction, plus real
  escalations only (§3).

## 2. Old → New mapping

| Old pattern | New pattern |
|---|---|
| Standalone bookkeeping recording transaction | Folded into the owning WP's own VERIFY/REVIEW (`P3-TXN-001`'s fold-by-default, now the norm) |
| Per-artifact/per-candidate Review A round | One Review A per WP |
| Full narrative PO report per transaction | 1-page Milestone Dashboard + targeted escalations only |
| Micro-task routing (one prompt per row/finding/mutant) | WP batches related items, subject to WIP=1 |
| Correction chains handled ad hoc until 3 rounds | WIP limit + batched Review A prevent most chains from starting; `P3-CORRECTION-CHAIN-001` remains the unchanged fail-safe |
| Identity-by-identity candidate authoring (candidate-002→003→004→005…) | Residual-closure Milestone with WP-sized batches (already the direction this exact EVID-03 track converged on: 69 → 53 → 3 rows) |
| Review A, Risk Classification, ADR Scope Rule, PO authority | **Unchanged**, preserved verbatim |

## 3. Roles and escalation rules

Roles are exactly `team.yaml`'s existing set — no new Constitution role is
created. Two **operational labels**, living only in this document:

- **Milestone Owner** — the assigned Module Owner (or PO if unassigned);
  accountable for the Milestone Dashboard.
- **WP Executor** — whoever performs EXECUTE (unchanged from today).

**Stays internal (no PO involvement) when ALL hold:**
1. WP stays within its pre-declared scope (no creep beyond the WP template's
   declared files/artifacts).
2. Risk Classification resolves R0 or R1.
3. No contradiction with any already-approved/Locked artifact, evidence, or
   ADR.
4. No Chapter 0 §4b ADR trigger fires.
5. Semantic Sufficiency applies (`G-REV-001`/`004`) — no real semantic risk,
   auditability, or safety impact.

**Must escalate to Product Owner when ANY holds:**
1. Risk Classification resolves R2.
2. An ADR Scope Rule trigger fires (Chapter 0 §4b, unchanged).
3. A Milestone reaches its completion/acceptance checkpoint (routine
   decision point, not an "issue").
4. Cited evidence contradicts the assertion being recorded — `P3-REVIEW-001`'s
   existing stop clause, unchanged: never silently "fixed" inline.
5. A WP cannot stay within its declared bounds (scope-creep signal).
6. `P3-CORRECTION-CHAIN-001`'s 3-round-no-stabilize threshold is hit.
7. PO has explicitly pre-flagged the area (LIVE-adjacent, custody/security,
   financial-risk boundary).

## 4. Work-package template

```text
WP-ID:
Milestone:
Module / artifact:
Objective (1 sentence):
Critical-path justification:
Scope — files/artifacts IN:
Scope — explicitly OUT / forbidden:
Governing rule / authority (doc + section):
Acceptance criteria (verifiable bullets):
Starting boundary (HEAD/blob to verify fresh):
Expected Risk Classification (confirmed at REVIEW):
Expected ADR scope (confirmed at REVIEW):
Dependencies:
Owner / Executor:
Status: PLANNED | IN_EXECUTE | VERIFY | REVIEW | DECIDE | DONE | BLOCKED
```

## 5. PO Milestone Dashboard template (one page)

```text
MILESTONE DASHBOARD — <milestone name> — <date>

Overall state: ON TRACK | AT RISK | BLOCKED
Primary blocker (if any): <one line>

Progress:
  WPs done:      X / Y
  WPs in flight (WIP=1/track): <WP-ID — status>
  WPs blocked:   <WP-ID — reason>

Critical path:
  Current blocking condition/gate: <name>
  Next unblock action: <one line>

Escalations this period: <none> OR <WP-ID — reason — decision needed>

Decisions needed from PO: <none> OR <exact decision phrase requested>

Evidence/governance integrity:
  Review A this period: <count>, CLEAN / findings
  Risk distribution: R0=x R1=y R2=z
  ADRs triggered: <none> OR <ADR-xxx, status>
  Historical evidence byte-unchanged confirmed: Y/N

Next checkpoint: <date/condition>
```

## 6. Current Ride / Feature Engine dashboard (filled, real state — verified fresh this transaction)

```text
MILESTONE DASHBOARD — Feature Engine P3-FEATURE-QG-EVID-03 closure — 2026-09-22

Overall state: AT RISK
Primary blocker: Condition 1 (raw mutation score) — FAIL — criteria.
  81.97033092430583% < required 87.001959503592%
  (feature-engine-mutation-step9-formal-evidence-004.json, 2629 mutants)

Progress:
  Condition 1: FAIL — criteria (primary blocker, no WP yet opened)
  Condition 2: 167/170 resolved (98.2%) — 2 identities reconstructed and
    READY for Candidate-005 (pending Review A); 1 identity
    (contracts.x__seal_verified_authority__mutmut_33) TOOL_IDENTITY_DRIFT,
    no existing governed mechanism, deferred
  Condition 3: SATISFIED per current record — flagged stale-risk since
    production source has materially expanded since last direct check;
    needs a freshness re-verify before final gate closure, not before

Critical path:
  Current blocking condition/gate: Condition 1 (raw score) — this alone
    keeps P3-FEATURE-QG-EVID-03 FAIL even if Condition 2 reaches 170/170,
    since the gate is a two-part AND (threshold-proposal-001.md §4)
  Next unblock action: diagnostic WP to prioritize the current 474-survivor
    population by kill-value concentration (see §7)

Escalations this period: none open. Candidate-005 (2 rows) and the
  tool-identity-drift gap are routine/deferred items, not escalations.

Decisions needed from PO: none blocking immediately. Next PO decision point:
  Candidate-005 approval once Review A completes.

Evidence/governance integrity:
  All historical evidence artifacts confirmed byte-unchanged this session.
  Candidate-004 (3 rows): Review A CLEAN, R1, PO APPROVED, 2026-09-22.

Next checkpoint: Candidate-005 Review A completion, OR diagnostic WP
  (§7) completion — whichever lands first.
```

## 7. Immediate next critical-path work package

Condition 2 progress does not move the gate — the two-part gate is an AND,
and raw score is the binding constraint at ~82% vs. an 87.0% bar. The correct
next WP is therefore **not** Candidate-005 (real, but non-critical-path — it
can run in parallel on its own WIP track) — it is a **bounded diagnostic WP**
for Condition 1, sized to stay inside one WP rather than attempting the full
(likely large) test-remediation effort in one unbounded package:

```text
WP-ID: FE-EVID03-COND1-DIAG-001
Milestone: Feature Engine EVID-03 closure
Module / artifact: feature-engine (Condition 1, raw score)
Objective: Produce a prioritized, bounded test-remediation backlog for the
  CURRENT 474 raw survivors (evidence-004/005 boundary) by root-cause
  concentration, mirroring the original baseline analysis's finding that a
  small function set concentrated the majority of survivors.
Critical-path justification: Condition 1 is the sole remaining blocker on
  the two-part EVID-03 gate; no other WP unblocks the gate without it.
Scope IN: read-only analysis of feature-engine-mutation-step9-formal-
  evidence-004/005.json survivor population; per-function/per-root-cause
  clustering; output backlog artifact only.
Scope OUT: no test authored, no src/** change, no mutation rerun, no
  Candidate-005 work (separate WP/track).
Governing rule: feature-engine-mutation-threshold-proposal-001.md §4/§4.1;
  Chapter 13 Quality Gates.
Acceptance criteria: exact survivor count reconciled against evidence-004/005;
  survivors clustered by (module, function); top clusters ranked by
  survivor-count-closed-per-test-scenario; backlog handed off as the next
  WP series' PLAN input.
Starting boundary: fresh HEAD verify at WP open.
Expected Risk: R0/R1 (analysis only, no code/behavior change).
Expected ADR scope: ADR_NOT_REQUIRED (no architecture/contract change).
Dependencies: none — evidence-004/005 already exist.
Owner / Executor: AI Technical Architect (Claude or ChatGPT).
Status: PLANNED
```

Parallel, independent, lower-priority WIP-track item (does not block or get
blocked by the above): Candidate-005 Review A for the 2 already-reconstructed
Condition-2 identities.

## 8. Minimal rollout / migration steps

1. **This document** is authored as Draft/Candidate only — zero edits to any
   Constitution chapter, ADR, Global Execution Rule, or Phase rule. No
   existing artifact, review, approval, or evidence is touched or
   invalidated.
2. Fresh ADR Scope Rule check (§9 below) is run now, at authoring time.
3. Submit for Review A (architecture-class, since it is a new operational
   document) + Risk Classification.
4. Product Owner decision: `ADOPT` / `ADOPT WITH CHANGES` / `REJECT`.
   Non-binding until this decision — no executor is obligated to follow it
   before adoption.
5. **On adoption only** — documents identified as *possibly* needing a
   future update to formally reference this model (list only, **not edited
   by this transaction**):
   - `docs/governance/phases/phase-3-rules.md` (`P3-MODULE-BATCH-001`,
     `P3-TXN-001` could cross-reference WP/Milestone terms)
   - `docs/governance/execution-rules.md` (`G-BUDGET`, `G-ORCH` could
     cross-reference the batched-Review-A default)
   - a future promoted `docs/governance/operating-model/lean-ride-operating-
     model-001.md`, if adopted as Locked operational doctrine
   - each future `phase-<n>-rules.md` as new phases open
6. **No retroactive reclassification** — every already-completed transaction
   (resolution-001/002, corrections, candidate-002/003/004, etc.) remains
   valid exactly as executed under the prior model. The lean model applies
   **prospectively only**, from the adoption boundary forward.
7. **First pilot**: apply this model live to WP `FE-EVID03-COND1-DIAG-001`
   (§7) and the parallel Candidate-005 track, before any wider rollout
   decision.

## 9. ADR Scope Rule check (self-certification, this candidate)

```text
This document proposes an OPERATIONAL efficiency layer — batching,
  WIP limits, dashboard/escalation format — strictly inside the space
  Review A/Risk-Classification/PO-decision authority already occupies.
  It does not add/remove a Platform Invariant, Event Schema, Module
  Taxonomy edge, or Governance/Approval-process rule; Review A remains
  mandatory, Risk Classification remains mandatory, ADR Scope Rule
  triggers are unchanged, PO remains sole decision authority.
Result at authoring time: ADR_NOT_REQUIRED.
Note: IF adopted content is later found to change eligibility, review
  cardinality, or PO-decision requirements in substance (not merely
  batching cadence), that specific future change would need its own
  fresh Chapter 0 §4b check — not assumed here.
```

## Change history

```text
v1.0  2026-09-22  Candidate authored — vai trò: `Lean Ride Operating Model
      v1 Design Executor`. Grounded fresh against 00-governance.md v1.4,
      execution-rules.md v0.6, phase-3-rules.md v0.3, 12-approval-gates.md
      v1.7, team.yaml, and current Feature Engine EVID-03 state
      (Condition 1 FAIL — 81.97033092430583%, Condition 2 167/170,
      Condition 3 SATISFIED-per-record). No governance/approval semantics
      changed. status: Draft, approved_by: null, approved_at: null.
```
