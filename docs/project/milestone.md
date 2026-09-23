---
id: ride-project-milestone-register-001
title: "Ride Quant Platform — Product Owner Milestone Register"
version: "1.0"
status: Active
owner: Product Owner
maintainer: "WP executors under Lean Ride Operating Model v1.1"
visual_companion: docs/project/milestone-dashboard.html
state_verified_against_head: 31fc6f5dda1834916f68c55656bd2fa4893bdcb8
state_verified_against_at: "2026-09-23"
---

# Ride Quant Platform — Milestone Register

**This document is the single authoritative source of truth for Product
Owner milestone tracking.** `docs/project/milestone-dashboard.html` is a
derived visual view only — if the dashboard ever disagrees with this
document, **this document controls**.

## 1. Purpose / authority

This is a **project visibility layer**, not a governance framework. It does
not create, change, or reinterpret any Governance/Approval semantics,
Quality Gate meaning, Constitution chapter, or ADR. It operates under Lean
Ride Operating Model v1.1 (`docs/governance/lean-ride-operating-model-v1-
candidate.md`, `status: Active — ADOPTED`, adopted 2026-09-22T15:12:00+07:00)
as a Milestone Dashboard instantiation of that model's §5 template, scoped
to whole-project milestone tracking rather than a single module.

All underlying facts (Quality Gate results, Condition states, evidence
counts) are sourced from `docs/governance/quality-gate/feature-engine-
chapter13-remediation-plan-001.md`, `docs/MANIFEST.md`, and the cited
evidence artifacts — this register summarizes them for PO consumption, it
does not restate or supersede them.

## 2. Milestone state model

| State | Meaning |
|---|---|
| `DONE` | Acceptance condition has been reached and recorded. |
| `ACTIVE` | Current milestone on the primary critical path. |
| `QUEUED` | Known future milestone, expected to be required, not active yet. |
| `PROVISIONAL` | Likely future milestone whose exact scope/necessity may change based on earlier milestone outcomes. |
| `BLOCKED` | Milestone cannot progress due to an unresolved dependency. |

**Operational rule:** milestones are identified ahead where reasonably
possible. Work Packages may be created, split, merged, reprioritized, or
replaced inside a milestone without creating a new milestone, unless the
project-level acceptance boundary genuinely changes.

## 3. Milestone register table

| ID | Name | State | Depends on | PO action required now |
|---|---|---|---|---|
| M0 | Lean Ride Operating Model v1.1 Adoption | `DONE` | — | No |
| M1 | Feature Engine — P3-FEATURE-QG-EVID-03 Closure | `ACTIVE` | M0 | No |
| M2 | Feature Engine — Remaining Quality-Gate Closure | `QUEUED` | M1 | No |
| M3 | Feature Engine — Module Approval | `QUEUED` | M2 | No |
| M4 | Feature Engine → Downstream Phase-3 Unlock / Integration | `PROVISIONAL` | M3 | No |

### M0 — Lean Ride Operating Model v1.1 Adoption

- **State:** `DONE`
- **Acceptance condition:** Lean Ride Operating Model v1.1 mechanically
  recorded `Active — ADOPTED`.
- **Closing boundary:** `063bc0771f25b59858df2e3906e00c7a238e0d31`
- **PO action required:** No.

### M1 — Feature Engine — P3-FEATURE-QG-EVID-03 Closure

See §4 for full detail.

### M2 — Feature Engine — Remaining Quality-Gate Closure

- **State:** `QUEUED`
- **Depends on:** M1
- **Acceptance condition:** not yet detailed — exact scope must be
  fresh-derived against repository authority (Chapter 13 Quality Gates,
  current remediation-plan-001.md state) once M1 reaches its own checkpoint.
  Not invented ahead of that evidence.
- **PO action required:** No.

### M3 — Feature Engine — Module Approval

- **State:** `QUEUED`
- **Depends on:** M2
- **Acceptance condition:** Feature Engine reaches its existing governed
  module-approval boundary (Chapter 12 §12.2) after all required
  Quality-Gate obligations are satisfied/dispositioned. This register does
  **not** grant, imply, or pre-authorize that approval.
- **PO action required:** No.

### M4 — Feature Engine → Downstream Phase-3 Unlock / Integration

- **State:** `PROVISIONAL`
- **Depends on:** M3
- **Acceptance condition:** not yet detailed — no speculative downstream
  implementation work is hard-coded here. Scope must be fresh-derived from
  the authoritative Phase-3 roadmap/dependency graph (Chapter 14 §14.2)
  after Feature Engine approval (M3).
- **PO action required:** No.

## 4. Current active milestone detail — M1

**Feature Engine — `P3-FEATURE-QG-EVID-03` Closure** (`ACTIVE`, depends on M0)

| Item | Current state |
|---|---|
| Overall | `AT RISK` |
| Condition 1 | `FAIL — criteria` — **PRIMARY BLOCKER** (formally governed result, Chapter 13 §13.8.1 Case A) |
| Condition 1 — unstable cases | 9 `UNSTABLE_TIMEOUT_TRIAGE` mutants (remain individually unresolved) |
| Condition 1 — current survivor count | 406 |
| Condition 2 | `167/170` — also independently blocking |
| Condition 3 | `SATISFIED — REVIEW A VALIDATED` (**DONE — not reopened by this WP**) |
| `P3-FEATURE-QG-EVID-03` | `OPEN` |
| Feature Engine approval | `NOT APPROVED` |
| LIVE | `NOT AUTHORIZED` |

**Condition 1 — now a formal governed result.** As of
`FE-EVID03-COND1-APPLY-001` (this transaction), Chapter 13 v1.8 §13.8.1
is controlling authority and has been formally applied to the existing,
byte-unchanged `evidence-005.json`/`evidence-005-correction-001.json`
measurement: bounds **84.21453023963484%–84.55686572841384%**, both below
the required **87.001959503592%** threshold → Case A → **`FAIL —
criteria`**. This supersedes the prior formal `STOPPED / UNRESOLVED`
verdict *prospectively* (the prior evaluation remains correct, immutable
historical evidence at its own boundary — Chapter 13 v1.7, without
§13.8.1, offered no governed rule to interpret unresolved timeout-triage
mutants). The 9 `UNSTABLE_TIMEOUT_TRIAGE` mutants remain individually
unresolved — this result concerns only the gate-level bounded measurement,
never any individual mutant's own classification. Full record:
`docs/governance/mutation-baseline-evidence/feature-engine-condition1-
bounded-reevaluation-001.json`.

**Primary Work Package — `FE-EVID03-COND1-STOP-001`: COMPLETE.** Bounded
investigation of the 9 unstable timeout-triage mutants. Result: all 9
classified `REQUIRES_GOVERNED_PROTOCOL_DECISION` — the locked protocol's
disagreement clause is a designed terminal state with no built-in
resolution step; no third run/majority vote/tie-break/reinterpretation was
introduced. Verified finding: 100% of the 9 are confined to 3
`authority_resolver.py` functions performing or reached exclusively through
real filesystem I/O; zero instability elsewhere despite objectively slower
tests being unaffected. Open interpretive question flagged for ChatGPT
architecture/governance review (not resolved by this WP): whether
Constitution Chapter 13 §13.10's flaky-test quarantine policy already
covers this phenomenon, or a new governed decision is required. Condition 1
remains `STOPPED / UNRESOLVED` — unchanged. Full record:
`docs/governance/mutation-baseline-evidence/feature-engine-condition1-
unstable-timeout-investigation-001.json`.

**Primary Work Package — `FE-EVID03-COND1-PROTOCOL-DECISION-001`: Draft
candidate authored (`ADR-044.md` v0.1), then Review A returned
`REVISION_REQUIRED — 0 Blocker / 2 Major / 1 Minor`, Risk `R2`.**

**Primary Work Package — `FE-EVID03-COND1-PROTOCOL-DECISION-001-CORR-001`:
COMPLETE.** Remediated the 3 round-1 Review A findings: `MAJOR-01`
(reconciled Chapter 13 §13.8 fail-closed semantics — per-mutant
reproducibility vs. gate-level bounded-measurement reproducibility, the
latter a new measurement semantic); `MAJOR-02` (corrected authority-
boundary model — ADR-044 is architecture decision/rationale only; the
authoritative measurement rule now lives in a new Chapter 13 successor,
`docs/constitution/13-quality-gates.md` v1.8 candidate, `Draft`, new
§13.8.1; activation model added requiring the ADR AND the Chapter 13
successor AND MANIFEST to activate together); `MINOR-01` (corrected
Alternative 3's straddle-region logic error). `ADR-044.md` v0.1 → v0.2.
ChatGPT's fresh Review A on this v0.2 bundle reconfirmed all 3 findings
`CLOSED — REVIEW A VALIDATED`, but returned a **new** verdict
`REVISION_REQUIRED — 0 Blocker / 1 Major / 1 Minor`, Risk `R2`.

**Primary Work Package — `FE-EVID03-COND1-PROTOCOL-DECISION-001-CORR-002`:
COMPLETE.** Remediated the 2 round-2 findings: `MAJOR-01` — §13.8.1's
Case C reclassified as an evaluation state, not a fourth final result
(Case A/B remain the only final results, `FAIL — criteria`/`PASS`,
unchanged vocabulary); `MINOR-01` — Chapter 13 banner's stale
`ADR-044.md v0.1` reference corrected. `ADR-044.md` v0.2 → v0.3.
ChatGPT's fresh Review A on this v0.3 bundle (boundary
`926feab8b4c1b6b7168f153713c37fe18a04d28c`) reconfirmed both round-2
findings `CLOSED — REVIEW A VALIDATED` and returned `CLEAN — 0 Blocker
/ 0 Major / 0 Minor`, Risk `R2`. The Product Owner then selected the
**optional** R2 independent cross-check (not an approval prerequisite —
Review A itself was already CLEAN). The cross-check returned `DEFECT
FOUND — 0 Blocker / 1 Major / 4 Minor`; ChatGPT independently
re-verified and accepted all 5, upgrading one to Major — effective
accepted correction input **`0 Blocker / 2 Major / 3 Minor`**.

**Primary Work Package — `FE-EVID03-COND1-PROTOCOL-DECISION-001-CORR-003`:
COMPLETE.** Consolidated all 5 accepted cross-check findings into one
internally complete correction (closed applicability predicate,
mixed-population rule, protocol-equivalence tightening, Testing
Convention item 8 precedence, self-sufficient arithmetic, activation-
wording cleanup, `addresses` metadata fix). `ADR-044.md` v0.3 → v0.4.
ChatGPT's fresh Review A on this v0.4 bundle (boundary
`82cba5dda79fe7138b8f76ebf73abdb841321610`) was `CLEAN — 0 Blocker /
0 Major / 0 Minor`. The Product Owner then selected a **second optional**
R2 independent cross-check, which returned `DEFECT FOUND — 0 Blocker /
1 Major / 3 Minor`; ChatGPT independently re-verified and accepted all
four — effective disposition `REVISION_REQUIRED — 0 Blocker / 1 Major /
3 Minor`. The Major was a **regression of a previously Review-A-
validated closure**: the round-3 rewrite of Chapter 13 §13.8.1 had
silently dropped the per-mutant/gate-level reproducibility reconciliation
present at the prior boundary. Per `P3-CORRECTION-CHAIN-001` (three
narrow correction rounds without stable convergence), the **narrow
correction loop STOPPED** — no `CORR-004` was created.

**`FE-EVID03-COND1-PROTOCOL-CONSOLIDATION-001`: COMPLETE (ROOT-CAUSE
CONSOLIDATION, `P3-CORRECTION-CHAIN-001`).**
Root cause: **dual normative authorship / semantic drift** — ADR-044 and
Chapter 13 §13.8.1 carried parallel copies of normative gate semantics
that had already drifted in both directions across the correction chain.
Consolidated: Chapter 13 §13.8.1 became the **sole, self-contained
normative source** (reproducibility reconciliation restored; Testing
Convention item-8 precedence rewritten unambiguously; protocol
provenance made structural since no separately governed named-protocol
authority exists beyond Feature Engine's own formal evidence). `ADR-044`
v0.4 → v0.5 restructured to rationale-only, carrying no second
executable gate specification, plus a new clause-trace table mapping
every guarantee to its exact Chapter 13 clause. ChatGPT's fresh Review A
on v0.5/v1.8 (boundary `704e492f83af1d463117f002c9f319ebcadd8099`)
returned `CLEAN — 0 Blocker / 0 Major / 2 Minor`; an optional
Product-Owner-selected R2 advisory cross-check (Claude) returned `0
Blocker / 0 Major / 5 Minor`, all accepted by ChatGPT as non-blocking.

**Primary Work Package — `FE-EVID03-COND1-PROTOCOL-ACTIVATION-001`:
COMPLETE (ATOMIC PRODUCT OWNER ACTIVATION).** With zero Blocker/Major on
both Review A and the optional cross-check, the Product Owner approved
the reviewed v0.5/v1.8 bundle (`2026-09-23T09:34:00+07:00`), accepting
Risk `R2` and all five cross-check Minors as non-blocking residual
findings, and authorized deterministic non-normative cleanup of
`X3-MIN-01`/`02`/`03` (ADR-044 wording only) folded into the same atomic
transaction — while explicitly declining to touch Chapter 13 §13.8.1's
normative semantics for `X3-MIN-04`/`05` (both remain accepted,
non-blocking, residual findings). **`ADR-044` v0.5 is now `Approved`;
Chapter 13 `v1.8` is now `Locked` and controlling** (`v1.7` is its
historical predecessor). §13.8.1's own reviewed semantic body was
verified byte-identical before and after. The bounded-uncertainty rule
is now effective prospectively for new evaluations. This activation did
not, by itself, apply the rule to EVID-03 or re-evaluate Condition 1.

**`FE-EVID03-COND1-APPLY-001`: COMPLETE (first formally governed
Condition-1 evaluation under controlling §13.8.1).** Applied §13.8.1
mechanically to the existing, byte-unchanged evidence-005.json/
-005-correction-001.json measurement. All 6 Applicability-predicate
conditions independently re-verified satisfied; executable-boundary
compatibility confirmed (all 5 pinned tree/blob hashes byte-identical
to the current boundary — no rerun performed or needed); Mixed-population
rule analyzed and found **not triggered** (Condition 2's residual
`TOOL_IDENTITY_DRIFT`/ambiguity gap is a separate historical-identity
criterion, not a status present in the current raw-run population —
Condition 2 remains independently unresolved, never masked). Arithmetic
independently recomputed, matching evidence-005.json exactly: bounds
**84.21453023963484%–84.55686572841384%**, both `< T` (87.001959503592%)
→ **Case A → `FAIL — criteria`**. **Condition 1: `STOPPED / UNRESOLVED`
→ `FAIL — criteria`**, recorded prospectively — the prior evaluation
remains immutable historical evidence, correct at its own boundary. All
9 `UNSTABLE_TIMEOUT_TRIAGE` mutants remain individually unresolved — none
reclassified. Condition 2 (`167/170`) and Condition 3 (`SATISFIED —
REVIEW A VALIDATED`) unchanged. `P3-FEATURE-QG-EVID-03` remains `OPEN` —
Condition 1 now fails on criteria and Condition 2 independently fails;
EVID-03 is not closed. No mutation execution, no source/test/tooling
change, no Condition-2/Condition-3 work. Full record:
`docs/governance/mutation-baseline-evidence/feature-engine-condition1-
bounded-reevaluation-001.json`.

**Primary Work Package — `FE-EVID03-COND2-CANDIDATE-005-AUTHOR-001`:
COMPLETE (candidate authoring only — no credit granted).** Fresh-verified
`feature-engine-condition2-remaining-ambiguity-historical-reconstruction-
001.json`'s current blob/content: it uniquely resolves exactly 2
previously ambiguous historical identities via direct historical-diff
reconstruction (not ordinal inference). Row 1 —
`_reevaluate_all_windows__mutmut_32` (historical `continue -> break`, the
3rd of 4 continue statements, positionally reconstructed) → current
successor `_prepare_reevaluate_all_windows__mutmut_32`, `killed`. Row 2 —
`on_swing_confirmed__mutmut_35` (historical mutation is **message-text
only** — a numeric literal inside `InvalidSwingEligibilityInputError`'s
f-string, never the validation condition itself) → current successor
`prepare_swing_confirmed__mutmut_35`, `killed`. Both statuses
independently cross-checked against `evidence-005.json`'s own
`full_current_mutant_mapping`; both successors independently
source-verified as the exact ADR-043 prepare-seam family already used
for the 167 previously-approved rows. Authored
`docs/governance/mutation-baseline-evidence/feature-engine-mutation-
material-gap-reclassification-candidate-005.json` (new) with exactly
these 2 rows, `review_a_state: PENDING`/`product_owner_state: PENDING`
for both. Row 2's message-text-only nature assessed explicitly: §4.1(b)
applies because the identity discontinuity is the ADR-043 prepare-seam
function relocation itself, not anything about where inside the
function the historical mutant sat — recorded as materiality context
only, historical materiality tag unchanged, no new identity-continuity
rule introduced. `contracts.x__seal_verified_authority__mutmut_33`
remains explicitly excluded (`TOOL_IDENTITY_DRIFT`), untouched. ADR
Scope Rule run fresh: `ADR_NOT_REQUIRED`. **Condition 2 remains
`167/170` — UNCHANGED.** Non-controlling projection recorded only:
`167 + 2 = 169/170` **NON-CONTROLLING / FUTURE-IF-APPROVED** if both
rows are later Review-A validated and Product-Owner approved.

**Candidate-005 — `PAUSED — awaiting governance delegation-model
resolution`** (not rejected, not approved). ChatGPT's Review A on
Candidate-005 (boundary `31fc6f5dda1834916f68c55656bd2fa4893bdcb8`,
candidate blob `e217bda50f17b71792429e196a81583ae02633e8`) returned
`CLEAN` — but this does **not** grant §4.1(b) credit by itself; a
separate Product Owner Decision (or, if `ADR-045` is later activated, a
qualifying Delegated Technical Resolution) is still required to close it.
Pending resolution is deliberately paused here rather than forced through
either route while `ADR-045`'s governance-delegation candidate (below) is
itself under review — see `ADR-045`'s own "Candidate-005 worked example"
for the non-normative illustration of how this pending candidate MAY
later be eligible under the new model, without retroactively rewriting
its authoring history.

**Primary Work Package — governance-improvement candidate authoring
(`GOV-DELEGATION-MODEL-ADR-045-AUTHOR-001`): COMPLETE.** Authored
`docs/adr/ADR-045.md` v0.1 (`Draft`) — a bounded **Delegated Technical
Resolution** lane that extends (does not supersede) `ADR-042`: an
eligible `AI Technical Architect`'s Review A may close a routine R0/R1
decision applying already-approved authority to a bounded technical case
without a separate Product Owner Decision, only when a closed,
conjunctive eligibility predicate (`D1`–`D12`) is satisfied — R2 and
every Product-Owner-reserved decision class (ADR approval, Approval
Gates, product direction, governance/approval-process change, Platform
Invariant/Event Schema/module-taxonomy change, explicit risk acceptance,
LIVE) are never delegated. Authored `docs/constitution/00-governance.md`
v1.5 (`Draft` candidate, v1.4 remains controlling) adding a Route
A/Route B addendum to §3; authored `docs/governance/execution-rules.md`
v0.7 (`CANDIDATE`, v0.6 remains `EFFECTIVE`) adding `G-DELEGATE-001`/
`G-DELEGATE-002`. ADR Scope Rule run fresh: `ADR_REQUIRED` (governance/
approval-process change); expected Risk `R2` (not self-finalized).
Verified no genuine contradiction in Chapter 11, Chapter 12, the ADR
template, `/docs/team/team.yaml`, or Phase-3 Rules — none modified. This
transaction does **not** activate the new model and does **not** resolve
Candidate-005.

**Deferred / blocked item:** `contracts.x__seal_verified_authority__mutmut_33`
— `TOOL_IDENTITY_DRIFT — NO EXISTING GOVERNED RESOLUTION MECHANISM`.

**PO action required now:** No. Condition 1 and Condition 2 both
independently fail; EVID-03 remains OPEN; Candidate-005 remains PAUSED.
Next governed step: ChatGPT Review A of `ADR-045`.

## 5. Work Package lanes

| Lane | Item | Status |
|---|---|---|
| Primary | `GOV-DELEGATION-MODEL-ADR-045-AUTHOR-001` | COMPLETE — `ADR-045` v0.1 `Draft` authored (Delegated Technical Resolution lane, D1-D12); Chapter 0 v1.5 and Global Execution Rules v0.7 candidates authored; awaiting ChatGPT Review A |
| Secondary | `Candidate-005` — `PAUSED` | Review A `CLEAN` at `31fc6f5d...`, but no credit granted; awaiting governance delegation-model resolution |
| Deferred | `contracts.x__seal_verified_authority__mutmut_33` (TOOL_IDENTITY_DRIFT) | Deferred — no existing governed mechanism |
| Completed | `RIDE-PROJECT-MILESTONE-DASHBOARD-001` | Tracking infrastructure only |
| Completed | `FE-EVID03-COND1-STOP-001` | 9/9 mutants `REQUIRES_GOVERNED_PROTOCOL_DECISION`; §13.10 applicability question flagged for ChatGPT review |
| Completed | `FE-EVID03-COND1-PROTOCOL-DECISION-001` | ADR-044 v0.1 Draft authored; Review A returned `REVISION_REQUIRED — 0 Blocker / 2 Major / 1 Minor`, R2 |
| Completed | `FE-EVID03-COND1-PROTOCOL-DECISION-001-CORR-001` | ADR-044 v0.2 + Chapter 13 v1.8 corrected (round-1 findings CLOSED); Review A returned `REVISION_REQUIRED — 0 Blocker / 1 Major / 1 Minor`, R2 |
| Completed | `FE-EVID03-COND1-PROTOCOL-DECISION-001-CORR-002` | ADR-044 v0.3 + Chapter 13 v1.8 corrected (round-2 findings CLOSED); Review A `CLEAN — 0/0/0`, R2; optional PO-selected cross-check returned `DEFECT FOUND — 0/1/4`, accepted as `0/2/3` |
| Completed | `FE-EVID03-COND1-PROTOCOL-DECISION-001-CORR-003` | ADR-044 v0.4 + Chapter 13 v1.8 corrected (round-3 findings CLOSED); Review A `CLEAN — 0/0/0`, R2; second optional PO-selected cross-check returned `DEFECT FOUND — 0/1/3`, accepted as `REVISION_REQUIRED — 0/1/3` (Major = regression) — `P3-CORRECTION-CHAIN-001` triggered, narrow loop STOPPED |
| Completed | `FE-EVID03-COND1-PROTOCOL-CONSOLIDATION-001` | ROOT-CAUSE CONSOLIDATION — ADR-044 v0.5 + Chapter 13 v1.8 consolidated to a single normative source; Review A `CLEAN — 0/0/2`, R2; optional PO-selected cross-check `0/0/5`, all accepted non-blocking |
| Completed | `FE-EVID03-COND1-PROTOCOL-ACTIVATION-001` | ATOMIC PRODUCT OWNER ACTIVATION — ADR-044 v0.5 `Approved`, Chapter 13 v1.8 `Locked`/controlling, Risk R2, all 5 cross-check Minors accepted non-blocking |
| Completed | `FE-EVID03-COND1-APPLY-001` | First formally governed Condition-1 evaluation under §13.8.1 — Case A, Condition 1 `STOPPED / UNRESOLVED` → `FAIL — criteria`; Condition 2/3 unchanged; EVID-03 remains OPEN |
| Completed | `FE-EVID03-COND2-CANDIDATE-005-AUTHOR-001` | Candidate-005 authored (2 rows); Review A `CLEAN` at `31fc6f5d...`; credit not granted — now `PAUSED`, see Secondary lane |

## 6. PO dashboard snapshot

```text
Current milestone:        M1 — Feature Engine EVID-03 Closure (ACTIVE, AT RISK)
Primary blocker:          Condition 1 — FAIL — criteria (formally
                           governed result under Chapter 13 v1.8
                           Section 13.8.1, Case A; 9 UNSTABLE_TIMEOUT_
                           TRIAGE mutants remain individually
                           unresolved). Condition 2 (167/170)
                           independently also blocks.
Current primary WP:       GOV-DELEGATION-MODEL-ADR-045-AUTHOR-001
                           (candidate authoring only -- does not activate
                           the new model, does not resolve Candidate-005)
ADR-045:                   v0.1, Draft -- Delegated Technical Resolution
                           lane (D1-D12 closed eligibility predicate),
                           extends ADR-042, does not supersede it
Chapter 0:                 v1.5 Draft candidate (v1.4 remains
                           controlling); Global Execution Rules v0.7
                           CANDIDATE (v0.6 remains EFFECTIVE)
Candidate-005 status:      PAUSED -- awaiting governance delegation-model
                           resolution (Review A CLEAN at 31fc6f5d..., no
                           credit granted -- not rejected, not approved)
Condition 2 (current):     167/170 -- UNCHANGED by this transaction
Condition 2 (projection):  167 + 2 = 169/170 -- NON-CONTROLLING /
                           FUTURE-IF-APPROVED (Candidate-005 not yet
                           reviewed or approved)
Last Review A:             CLEAN — 0 Blocker / 0 Major / 2 Minor (on
                           v0.5/v1.8, ADR-044/Chapter-13 activation).
                           ADR-045 itself has NOT yet had its own Review A
                           -- expected Risk R2, not self-finalized.
PO decision required now: NO
                           (ADR-045 is authored but not yet reviewed or
                           approved; Condition 1 and Condition 2 both
                           independently fail; EVID-03 remains OPEN;
                           Candidate-005 remains PAUSED. Next governed
                           step is ChatGPT Review A of ADR-045.)
```

## 7. Update rules

- This register is updated whenever a milestone's state changes, a Work
  Package completes/changes lane, or a Condition/Quality-Gate state changes
  for the ACTIVE milestone.
- `state_verified_against_head` / `state_verified_against_at` in the
  frontmatter record the repository/evidence boundary the milestone state
  below was verified against **before** this update was authored — not this
  artifact's own resulting commit SHA (which does not exist at verification
  time). Refreshed at each update, verified fresh against the live
  repository (`git rev-parse HEAD` at the start of the update transaction),
  not carried forward from memory.
- Updates to this register are project-visibility bookkeeping — they do not
  themselves constitute a Governance/Approval decision, Quality Gate
  re-evaluation, or ADR-scope event. If an update would require restating a
  Condition/Quality-Gate verdict, that verdict must be re-verified against
  its own authoritative source (`remediation-plan-001.md`, MANIFEST, cited
  evidence artifacts), never asserted from this file's own prior text.
- `docs/project/milestone-dashboard.html` must be regenerated/edited in the
  same transaction as any change here, so the two never drift — if they
  ever do, this Markdown file controls.
