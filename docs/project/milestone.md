---
id: ride-project-milestone-register-001
title: "Ride Quant Platform — Product Owner Milestone Register"
version: "1.0"
status: Active
owner: Product Owner
maintainer: "WP executors under Lean Ride Operating Model v1.1"
visual_companion: docs/project/milestone-dashboard.html
last_verified_head: 063bc0771f25b59858df2e3906e00c7a238e0d31
last_verified_at: "2026-09-22"
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

**Primary Work Package:** `FE-EVID03-COND1-STOP-001` — investigate the 9
unstable timeout-triage cases and determine whether resolution exists under
the existing locked protocol, or requires a separately governed protocol
decision.

**Secondary queue:** `Candidate-005` — govern the 2 historically
reconstructed Condition-2 identities, when doing so does not disrupt the
primary critical path.

**Deferred / blocked item:** `contracts.x__seal_verified_authority__mutmut_33`
— `TOOL_IDENTITY_DRIFT — NO EXISTING GOVERNED RESOLUTION MECHANISM`.

**PO action required now:** No.

## 5. Work Package lanes

| Lane | Item | Status |
|---|---|---|
| Primary | `FE-EVID03-COND1-STOP-001` | Planned, not yet executed |
| Secondary | `Candidate-005` (2 Condition-2 identities) | Queued, non-blocking |
| Deferred | `contracts.x__seal_verified_authority__mutmut_33` (TOOL_IDENTITY_DRIFT) | Deferred — no existing governed mechanism |
| Completed | `RIDE-PROJECT-MILESTONE-DASHBOARD-001` (this WP) | Tracking infrastructure only |

## 6. PO dashboard snapshot

```text
Current milestone:        M1 — Feature Engine EVID-03 Closure (ACTIVE)
Primary blocker:          Condition 1 — STOPPED / UNRESOLVED
                           (9 UNSTABLE_TIMEOUT_TRIAGE mutants)
Current primary WP:       FE-EVID03-COND1-STOP-001 (not yet executed)
PO decision required now: NO
```

## 7. Update rules

- This register is updated whenever a milestone's state changes, a Work
  Package completes/changes lane, or a Condition/Quality-Gate state changes
  for the ACTIVE milestone.
- `last_verified_head` / `last_verified_at` in the frontmatter must be
  refreshed at each update, verified fresh against the live repository
  (`git rev-parse HEAD`), not carried forward from memory.
- Updates to this register are project-visibility bookkeeping — they do not
  themselves constitute a Governance/Approval decision, Quality Gate
  re-evaluation, or ADR-scope event. If an update would require restating a
  Condition/Quality-Gate verdict, that verdict must be re-verified against
  its own authoritative source (`remediation-plan-001.md`, MANIFEST, cited
  evidence artifacts), never asserted from this file's own prior text.
- `docs/project/milestone-dashboard.html` must be regenerated/edited in the
  same transaction as any change here, so the two never drift — if they
  ever do, this Markdown file controls.
