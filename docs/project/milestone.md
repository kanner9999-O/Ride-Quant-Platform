---
id: ride-project-milestone-register-001
title: "Ride Quant Platform — Product Owner Milestone Register"
version: "1.0"
status: Active
owner: Product Owner
maintainer: "WP executors under Lean Ride Operating Model v1.1"
visual_companion: docs/project/milestone-dashboard.html
state_verified_against_head: 09bf6c7dd760deff7307fe8fbccb6f57217c4fc5
state_verified_against_at: "2026-09-22"
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
| Condition 1 | `STOPPED / UNRESOLVED` — **PRIMARY BLOCKER** |
| Condition 1 — unstable cases | 9 `UNSTABLE_TIMEOUT_TRIAGE` mutants |
| Condition 1 — current survivor count | 406 |
| Condition 2 | `167/170` |
| Condition 3 | `SATISFIED — REVIEW A VALIDATED` (**DONE — not reopened by this WP**) |
| `P3-FEATURE-QG-EVID-03` | `OPEN` |
| Feature Engine approval | `NOT APPROVED` |
| LIVE | `NOT AUTHORIZED` |

**Condition 1 — formal vs. diagnostic:** the locked timeout-triage
protocol's disagreement clause triggered on the 9 unstable mutants, so
Condition 1's formal verdict is `STOPPED / UNRESOLVED` — neither PASS nor
FAIL. Diagnostic-only bounds of approximately **84.21%–84.56%** exist
(both below the required **87.001959503592%** threshold) — these numeric
bounds are **planning evidence only** and do **not** replace or substitute
for the formal `STOPPED / UNRESOLVED` verdict.

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
IN PROGRESS (second bounded ADR correction).** Remediates the 2 new
round-2 findings: new `MAJOR-01` — §13.8.1's Case C read as a fourth
final Quality-Gate result; corrected in both ADR-044 and §13.8.1 so
Case A/B remain the only final results (`FAIL — criteria`/`PASS`,
unchanged vocabulary) and **Case C is reclassified as an evaluation
state, not a final result** — no PASS/FAIL emitted, eligibility remains
incomplete/fail-closed per §13.1/§13.8's "Missing gate ≠ passed gate,"
a downstream Approval Gate PASS prerequisite is not satisfied, and Case
C's evidence is not relabeled `FAIL — evidence` either. New `MINOR-01` —
Chapter 13 banner's stale `ADR-044.md v0.1` reference corrected to the
resulting v0.3. `ADR-044.md` v0.2 → v0.3; Chapter 13 stays v1.8 (same
Draft candidate corrected in place, no v1.9). `status: Draft` unchanged
on both, NOT marked Review-A CLEAN. Current EVID-03 worked example under
the candidate rule (illustrative, **`NON-CONTROLLING / FUTURE-IF-
ACTIVATED`**): projected `FAIL — criteria` if later activated (upper
bound 84.56% < required 87.001959503592%). **Condition 1 remains
`STOPPED / UNRESOLVED` now — this correction changes nothing until
reviewed and the full activation model completes.** Awaiting ChatGPT
fresh Review A + Risk Classification of the corrected ADR-044 v0.3 +
Chapter 13 v1.8 bundle before any Product Owner decision point.

**Secondary queue:** `Candidate-005` — govern the 2 historically
reconstructed Condition-2 identities, when doing so does not disrupt the
primary critical path.

**Deferred / blocked item:** `contracts.x__seal_verified_authority__mutmut_33`
— `TOOL_IDENTITY_DRIFT — NO EXISTING GOVERNED RESOLUTION MECHANISM`.

**PO action required now:** No.

## 5. Work Package lanes

| Lane | Item | Status |
|---|---|---|
| Primary | `FE-EVID03-COND1-PROTOCOL-DECISION-001-CORR-002` | ADR-044 v0.3 + Chapter 13 v1.8 candidate corrected (Case C reclassified as evaluation state); awaiting ChatGPT fresh Review A + Risk Classification |
| Secondary | `Candidate-005` (2 Condition-2 identities) | Queued, non-blocking |
| Deferred | `contracts.x__seal_verified_authority__mutmut_33` (TOOL_IDENTITY_DRIFT) | Deferred — no existing governed mechanism |
| Completed | `RIDE-PROJECT-MILESTONE-DASHBOARD-001` | Tracking infrastructure only |
| Completed | `FE-EVID03-COND1-STOP-001` | 9/9 mutants `REQUIRES_GOVERNED_PROTOCOL_DECISION`; §13.10 applicability question flagged for ChatGPT review |
| Completed | `FE-EVID03-COND1-PROTOCOL-DECISION-001` | ADR-044 v0.1 Draft authored; Review A returned `REVISION_REQUIRED — 0 Blocker / 2 Major / 1 Minor`, R2 |
| Completed | `FE-EVID03-COND1-PROTOCOL-DECISION-001-CORR-001` | ADR-044 v0.2 + Chapter 13 v1.8 corrected (round-1 findings CLOSED); Review A returned `REVISION_REQUIRED — 0 Blocker / 1 Major / 1 Minor`, R2 |

## 6. PO dashboard snapshot

```text
Current milestone:        M1 — Feature Engine EVID-03 Closure (ACTIVE)
Primary blocker:          Condition 1 — STOPPED / UNRESOLVED
                           (9 UNSTABLE_TIMEOUT_TRIAGE mutants)
Current primary WP:       FE-EVID03-COND1-PROTOCOL-DECISION-001-CORR-002
                           (ADR-044 v0.3 + Chapter 13 v1.8 candidate
                           corrected: Case C reclassified as evaluation
                           state, not a fourth final result; NOT yet
                           re-reviewed)
Last Review A:             REVISION_REQUIRED — 0 Blocker / 1 Major /
                           1 Minor, Risk R2 (on v0.2, remediated above;
                           round-1 findings CLOSED — REVIEW A VALIDATED)
PO decision required now: NO
                           (deferred until the corrected semantic
                           bundle — ADR-044 v0.3 + Chapter 13 v1.8 —
                           receives a CLEAN Review A)
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
