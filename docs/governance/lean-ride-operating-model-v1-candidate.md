---
id: lean-ride-operating-model-v1
title: "Lean Ride Operating Model v1 — Candidate"
version: "1.1"
status: Active
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: Product Owner
approved_at: "2026-09-22T15:12:00+07:00"
created_at: "2026-09-22"
depends_on: ["00-governance", "11-adr-process", "12-approval-gates", "13-quality-gates", "14-roadmap"]
---

# Lean Ride Operating Model v1 — ACTIVE

**Status: Active — ADOPTED.** This document is now the binding operational
efficiency layer described in §0/§1, applying **prospectively only** from the
adoption boundary below (§10) — it changed **zero** Governance/Approval
semantics at any point in its lifecycle: it is an **operational efficiency
layer sitting strictly inside** the space the existing rules already treat as
low-ceremony (R0/R1 default no-cross-check, `G-REV` Semantic Sufficiency,
`P3-TXN-001` fold-by-default, `P3-MODULE-BATCH-001` batch containment). No
Constitution chapter, ADR, Global Execution Rule, or Phase rule was edited by
this document at authoring, correction, or adoption.

**v1.1 bounded correction (2026-09-22):** remediated ChatGPT Review A
`REVISION_REQUIRED — 0 Blocker / 2 Major / 1 Minor` at reviewed boundary
`30fc1a303886777878407ce266a184fa52c82d4e` / blob
`f2cb56fe7fbac589a4ec574c1096214ceb9e76b6` — see Change history for the
per-finding remediation summary. **Adoption recorded in §10 below.**

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
| REVIEW | Review A + Risk Classification | **Batched by default**: one Review A per WP, sized to real aggregate risk. This is a default, not an override — if an existing governing rule requires a narrower review boundary for a specific artifact/decision (e.g. a §4.1(b) reclassification candidate's own dedicated Review A, per existing precedent), that narrower boundary wins |
| DECIDE | Product Owner decision | Governed strictly by **existing approval-gate authority**, not by Risk Classification alone. R0/R1 controls only whether an *optional cross-check* is skipped by default (ADR-042) — it does **not** by itself mean "no PO step." Any artifact/decision already subject to an existing approval-gate/PO-decision requirement (Chapter 12 §12.2, a §4.1(b) candidate decision, an ADR, a Milestone acceptance) **still requires** Product Owner Decision regardless of R0/R1/R2. Work stays internal only when **no existing approval authority requires PO** for that specific output (§3) |

**New operating constraints:**

- **Work Package (WP)** — replaces micro-task routing. One WP = one coherent
  deliverable against one Quality Gate condition or one module artifact.
- **WIP limit = 1 in-flight WP per critical-path track** per executor/module.
  Prevents the parallel half-finished chains `P3-CORRECTION-CHAIN-001` exists
  to catch after the fact — this prevents most of them from starting.
- **Critical-path prioritization** — WPs ordered against the Roadmap
  dependency graph (Chapter 14 §14.2) and, within a module, against the
  module's own blocking Quality Gate condition first.
- **Batched Review A (default, not an override)** — sized to the WP's
  aggregate semantic delta, per `G-REV-001`/Semantic Sufficiency. A
  structural default rather than case-by-case judgment — but if an existing
  governing rule requires a narrower review/decision boundary for a specific
  artifact or decision, that narrower boundary controls, unchanged.
- **Milestone-level PO reporting** — PO sees one Dashboard update per
  Milestone checkpoint, not one report per transaction, plus real
  escalations only (§3).

## 2. Old → New mapping

| Old pattern | New pattern |
|---|---|
| Standalone bookkeeping recording transaction | Folded into the owning WP's own VERIFY/REVIEW (`P3-TXN-001`'s fold-by-default, now the norm) |
| Per-artifact/per-candidate Review A round | One Review A per WP **by default** — narrower existing review/decision boundaries still win when a governing rule requires one |
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
2. **No existing approval-gate/PO-decision requirement applies to this WP's
   output** — i.e. the WP does not itself constitute or feed a decision that
   Chapter 12 §12.2, a §4.1(b) reclassification decision, an ADR, or a
   Milestone-acceptance checkpoint already requires Product Owner Decision
   for. (Risk Classification resolving R0/R1 only controls whether an
   *optional* R2 cross-check is skipped by default, per ADR-042 — it never
   by itself substitutes for a required PO Decision.)
3. No contradiction with any already-approved/Locked artifact, evidence, or
   ADR.
4. No Chapter 0 §4b ADR trigger fires.
5. Semantic Sufficiency applies (`G-REV-001`/`004`) — no real semantic risk,
   auditability, or safety impact.

**Must escalate to Product Owner when ANY holds:**
1. An existing approval-gate/PO-decision requirement applies to the WP's
   output (§3 stays-internal criterion 2 fails) — regardless of Risk
   Classification. This is the primary, most common escalation trigger, not
   an edge case.
2. Risk Classification resolves R2.
3. An ADR Scope Rule trigger fires (Chapter 0 §4b, unchanged).
4. A Milestone reaches its completion/acceptance checkpoint (routine
   decision point, not an "issue").
5. Cited evidence contradicts the assertion being recorded — `P3-REVIEW-001`'s
   existing stop clause, unchanged: never silently "fixed" inline.
6. A WP cannot stay within its declared bounds (scope-creep signal).
7. `P3-CORRECTION-CHAIN-001`'s 3-round-no-stabilize threshold is hit.
8. PO has explicitly pre-flagged the area (LIVE-adjacent, custody/security,
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
Primary blocker: Condition 1 — formally `STOPPED / UNRESOLVED`, NOT FAIL.
  The locked timeout-triage protocol's disagreement clause triggered: 9
  UNSTABLE_TIMEOUT_TRIAGE mutants (2 independent fresh isolated reruns
  disagreed) — protocol requires the gate interpretation to STOP,
  unconditionally, neither PASS nor FAIL formally declared.
  Diagnostic-only bounds (84.21%–84.56%, both below the required
  87.001959503592% threshold) are NON-FORMAL planning evidence only, not
  the governed verdict.
  (feature-engine-mutation-step9-formal-evidence-005.json +
  -correction-001.json, 2629 mutants: killed=2209, survived=406,
  confirmed_timeout=5, unstable=9)

Progress:
  Condition 1: STOPPED / UNRESOLVED (primary blocker, no WP yet opened)
  Condition 2: 167/170 resolved (98.2%) — 2 identities reconstructed and
    READY for Candidate-005 (pending Review A); 1 identity
    (contracts.x__seal_verified_authority__mutmut_33) TOOL_IDENTITY_DRIFT,
    no existing governed mechanism, deferred
  Condition 3: SATISFIED — re-checked only if existing P3-VERIFY-001
    freshness/applicability conditions are actually triggered; no new
    closure step invented by this dashboard

Critical path:
  Current blocking condition/gate: Condition 1 — its formal STOP alone
    keeps P3-FEATURE-QG-EVID-03 OPEN even if Condition 2 reaches 170/170,
    since the gate is a two-part AND (threshold-proposal-001.md §4); the
    non-formal diagnostic bounds additionally show the numeric gap would
    remain below threshold even in the best case
  Next unblock action: bounded WP to resolve or bound the 9 unstable
    timeout-triage mutants under the locked protocol (see §7)

Escalations this period: none open. Candidate-005 (2 rows) and the
  tool-identity-drift gap are routine/deferred items, not escalations.

Decisions needed from PO: none blocking immediately. Next PO decision point:
  Candidate-005 approval once Review A completes.

Evidence/governance integrity:
  All historical evidence artifacts confirmed byte-unchanged this session.
  Candidate-004 (3 rows): Review A CLEAN, R1, PO APPROVED, 2026-09-22.

Next checkpoint: Candidate-005 Review A completion, OR WP
  `FE-EVID03-COND1-STOP-001` (§7) completion — whichever lands first.
```

## 7. Immediate next critical-path work package

Condition 1's **formal** blocker is not a numeric score — it is the 9
`UNSTABLE_TIMEOUT_TRIAGE` mutants that trigger the locked protocol's
unconditional STOP (§6). Until that STOP is resolved or bounded under a
governed decision, no formal PASS/FAIL is even possible, independent of
survivor-count progress. Separately — and not a substitute for that — the
non-formal diagnostic bounds already show the numeric gap persists even in
the best case (84.56% best-case vs. 87.001959503592% required, using the
current 406-survivor population), so the numeric path will need its own
work regardless of how the 9 unstable cases resolve. Both are genuinely
critical-path; they are sequenced as two WPs on separate tracks so neither
blocks the other, per the WIP-limit-per-track rule (§1):

```text
WP-ID: FE-EVID03-COND1-STOP-001
Milestone: Feature Engine EVID-03 closure
Module / artifact: feature-engine (Condition 1, formal STOP)
Objective: Bounded investigation of the 9 UNSTABLE_TIMEOUT_TRIAGE mutants'
  root cause (e.g. resource contention, timeout-constant sensitivity) and a
  recommendation on whether a governed resolution path exists WITHOUT
  amending the locked timeout-triage protocol's disagreement rule. Does NOT
  itself authorize a new tie-break/majority-vote mechanism — the protocol
  explicitly forbids that within an ordinary transaction.
Critical-path justification: this is the literal formal blocker — Condition 1
  cannot reach PASS or FAIL without it resolving or being explicitly
  accepted as a longer-term open item.
Scope IN: read-only investigation of the 9 unstable mutants' rerun logs/
  environment; a recommendation only.
Scope OUT: no new rerun/tie-break executed under a changed rule; no src/**
  change; no protocol amendment authored (escalates to PO/ADR-scope check
  if the investigation concludes a protocol change is the only path).
Governing rule: feature-engine-mutation-step9-formal-evidence-005-
  correction-001.json's locked timeout-triage protocol; Chapter 0 §4b.
Acceptance criteria: root-cause hypothesis stated with evidence; explicit
  recommendation (resolvable under existing protocol / requires a governed
  protocol change / remains open) — decision on next step escalates to PO
  per §3 if a protocol change is indicated.
Starting boundary: fresh HEAD verify at WP open.
Expected Risk: R1 (investigation only, no code/protocol change).
Expected ADR scope: ADR_NOT_REQUIRED for the investigation itself; escalates
  if a protocol change is recommended.
Dependencies: none — evidence-005/-correction-001 already exist.
Owner / Executor: AI Technical Architect (Claude or ChatGPT).
Status: PLANNED
```

Parallel, independent WIP-track item (does not block or get blocked by the
above): a diagnostic clustering of the **current 406 survivors**
(evidence-005 boundary, not the historical 474) by root-cause concentration,
to prepare a bounded test-remediation backlog against the numeric gap —
useful regardless of how `FE-EVID03-COND1-STOP-001` resolves, since the
best-case bound alone does not clear the threshold.

Also parallel, independent, lower-priority WIP-track item: Candidate-005
Review A for the 2 already-reconstructed Condition-2 identities.

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
7. **First pilot**: apply this model live to WP `FE-EVID03-COND1-STOP-001`
   (§7), its parallel 406-survivor diagnostic-clustering track, and the
   parallel Candidate-005 track, before any wider rollout decision.

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

## 10. Adoption record

**Review A result (authoritative):** `CLEAN — 0 Blocker / 0 Major / 0 Minor`,
Risk `R1`, ADR `ADR_NOT_REQUIRED`.

**Reviewed semantic boundary:** `4ee761cd7b5776a93cf695ae3bdb8b64aafcf58b`.
**Reviewed subject blob:** `a924aea62214bbbf60a9361f6d83511b9aedd09e`
(`docs/governance/lean-ride-operating-model-v1-candidate.md` at that
boundary — verified fresh this transaction via `git hash-object`, matches
exactly).

**Product Owner decision (verbatim):** "ADOPT Lean Ride Operating Model
v1.1." Decision timestamp: `2026-09-22T15:12:00+07:00`.

**Lifecycle transition:** `status: Draft → Active`, `approved_by: null →
Product Owner`, `approved_at: null → "2026-09-22T15:12:00+07:00"`. All
reviewed operating-model semantics (§0–§9) are unchanged by this recording —
this is mechanical lifecycle recording only, not a second semantic decision.

**Scope of adoption — prospective only:** this adoption applies
**prospectively only**, from this adoption boundary forward. It does **not**
retroactively reclassify, reopen, or invalidate any already-completed Ride
transaction, review, approval, or evidence artifact — every prior EVID-03
transaction (resolution-001/002, corrections, candidate-002/003/004, the
final-six assessment, the historical-baseline reconstruction, etc.) remains
valid exactly as executed under the model in force at the time it ran (§8
item 6, unchanged).

**Governance/Approval semantics:** unchanged by this adoption — Product
Owner sole decision authority, Review A mandatory, Risk Classification
mandatory (R0/R1/R2, ADR-042), ADR Scope Rule (Chapter 0 §4b), and all
Global Execution Rules remain exactly as they were before this document
existed. No Constitution chapter, ADR, Global Execution Rule, or Phase rule
is touched by this recording.

**Initial pilot:** Feature Engine `P3-FEATURE-QG-EVID-03` — specifically WP
`FE-EVID03-COND1-STOP-001` (§7), the first Work Package run live under this
model.

## Change history

```text
v1.0  2026-09-22  Candidate authored — vai trò: `Lean Ride Operating Model
      v1 Design Executor`. Grounded fresh against 00-governance.md v1.4,
      execution-rules.md v0.6, phase-3-rules.md v0.3, 12-approval-gates.md
      v1.7, team.yaml, and current Feature Engine EVID-03 state
      (Condition 1 FAIL — 81.97033092430583%, Condition 2 167/170,
      Condition 3 SATISFIED-per-record). No governance/approval semantics
      changed. status: Draft, approved_by: null, approved_at: null.
v1.1  2026-09-22  Bounded correction — vai trò: `Lean Ride Operating Model
      v1 Bounded Correction Executor`, remediating ChatGPT Review A
      `REVISION_REQUIRED — 0 Blocker / 2 Major / 1 Minor`, Risk `R1`, at
      reviewed boundary `30fc1a303886777878407ce266a184fa52c82d4e` / blob
      `f2cb56fe7fbac589a4ec574c1096214ceb9e76b6`.
      **Major 1 — Feature Engine dashboard corrected to authoritative
      state** (§6/§7): Condition 1 was wrongly stated `FAIL — criteria`
      (stale evidence-004 framing) — corrected to formal `STOPPED /
      UNRESOLVED`, since evidence-005-correction-001.json's locked
      timeout-triage protocol requires the gate interpretation to STOP,
      unconditionally, on the 9 `UNSTABLE_TIMEOUT_TRIAGE` mutants found;
      the conservative/best-case percentage figures are relabeled
      explicit NON-FORMAL diagnostic/planning evidence, not a formal
      verdict. Survivor count corrected 474 (stale evidence-004) → 406
      (current evidence-005). Required threshold unchanged
      (87.001959503592%). Condition 2 confirmed 167/170 (already
      correct). Condition 3 wording corrected — no new freshness-gate
      invented (see Minor below).
      **Major 2 — approval semantics corrected** (§1 DECIDE row, §2, §3):
      previously conflated Risk Classification R0/R1 (which only controls
      whether an *optional* R2 cross-check is skipped by default,
      ADR-042) with "no PO step required." Corrected: any artifact/
      decision already subject to an existing approval-gate/PO-decision
      requirement (Chapter 12 §12.2, a §4.1(b) reclassification decision,
      an ADR, a Milestone-acceptance checkpoint) still requires Product
      Owner Decision regardless of R0/R1/R2; "stays internal" now
      requires that NO existing approval authority requires PO for that
      specific WP output, added as its own escalation-list item (now the
      primary trigger, not R2 alone). Chapter 0 / ADR-042 semantics
      themselves untouched.
      **Minor 1 — invented Condition-3 freshness gate removed** (§6):
      the prior dashboard fabricated a new mandatory "freshness re-verify
      before final gate closure" step. Corrected: Condition 3 remains
      `SATISFIED`; re-check applicability only if existing
      `P3-VERIFY-001` freshness/applicability conditions are actually
      triggered — no new closure step created by this document.
      **Additional corrections in the same pass** (batching-language
      relaxation, requested alongside the above, not a separate finding):
      "one Review A per WP" (§1, §2, new operating-constraints bullet)
      now explicit as a default that a narrower existing governing rule
      can override, not an absolute. §7's work package recomputed:
      formal blocker restated as the 9 unstable timeout-triage cases
      (new WP `FE-EVID03-COND1-STOP-001`, bounded investigation only, no
      protocol amendment authored), current 406-survivor diagnostic
      clustering kept as a parallel, non-blocking WIP-track item (the
      numeric gap persists even best-case, so this remains real
      preparatory work); critical-path prioritization preserved.
      No Constitution/ADR/Global Execution Rule/Phase rule touched.
      `status: Draft` unchanged, `approved_by: null`, `approved_at: null`
      — awaiting bounded Review A re-review.
v1.1  2026-09-22  Product Owner adoption — mechanical lifecycle recording,
      vai trò: `Lean Ride Operating Model v1.1 Adoption Recorder`. Decision
      nguyên văn: "ADOPT Lean Ride Operating Model v1.1"
      (`2026-09-22T15:12:00+07:00`). Reviewed semantic candidate v1.1
      (Review A `CLEAN — 0 Blocker / 0 Major / 0 Minor`, Risk `R1`, ADR
      `ADR_NOT_REQUIRED`), boundary `4ee761cd7b5776a93cf695ae3bdb8b64aafcf58b`,
      blob `a924aea62214bbbf60a9361f6d83511b9aedd09e` (verified fresh,
      matches exactly). `status: Draft → Active`, `approved_by: null →
      Product Owner`, `approved_at: null → "2026-09-22T15:12:00+07:00"`.
      `version: "1.1"` unchanged (pure mechanical adoption, no semantic
      content change — §0–§9 byte-equivalent). Adoption applies
      prospectively only; no prior Ride transaction/review/approval/
      evidence is retroactively reclassified or invalidated. Initial
      pilot: Feature Engine EVID-03, WP `FE-EVID03-COND1-STOP-001`. No
      Constitution/ADR/Global Execution Rule/Phase rule/Feature Engine
      evidence/source/tests/tooling touched.
```
