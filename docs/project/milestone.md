---
id: ride-project-milestone-register-001
title: "Ride Quant Platform — Product Owner Milestone Register"
version: "1.0"
status: Active
owner: Product Owner
maintainer: "WP executors under Lean Ride Operating Model v1.1"
visual_companion: docs/project/milestone-dashboard.html
state_verified_against_head: dd05c963397bbb8c9b8bd30f6a88c913baf3f153
state_verified_against_at: "2026-09-24"
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
| Condition 1 | `PASS — REVIEW A VALIDATED` — gated by the ACTIVATED recalibrated threshold-v3: Condition 1A (raw score ≥ `84.899201217193%`, MEASURED `85.393685812096%`, PASS) AND Condition 1B (18 pinned current-material identities individually resolved, MEASURED `18/18 KILLED`, PASS) — evidence-006, formally validated by distinct-principal ChatGPT Review A, recorded via `FE-EVID03-COND1-FORMAL-006-DTR-001` (Delegated Technical Resolution, NOT a Product Owner approval). Condition 1 is no longer the primary blocker. |
| Condition 1 — unstable cases (current, evidence-006) | `0` — historical Evidence-005 figure of `9` is superseded at the current measurement boundary, not reopened |
| Condition 1 — current survivor count (evidence-006) | `384` — historical Evidence-005 figure of `406` is superseded at the current measurement boundary |
| Condition 1 — current-material companion gate | `18/18 formally resolved — PASS — REVIEW A VALIDATED` — `docs/governance/mutation-baseline-evidence/feature-engine-condition1-current-material-gap-set-003.json` (APPROVED — EFFECTIVE, sole current Condition-1B authority; all 18 measured KILLED by exact identity in `feature-engine-mutation-step9-formal-evidence-006.json`; old 42-ID set-001/24-ID set-002 and their 18+6 delegated-reclassifications are historical, `feature-engine-condition1-material-gap-dtr-001.json` + `feature-engine-condition1-wave6-classification-dtr-001.json`) |
| Condition 2 | `169/170` — also independently blocking (1 `TOOL_IDENTITY_DRIFT` row unresolved: `contracts.x__seal_verified_authority__mutmut_33`). A candidate resolution mechanism has been authored — `feature-engine-condition2-tool-identity-continuity-proposal-001.md`, `CANDIDATE — NOT EFFECTIVE / AWAITING REVIEW A` — but grants no credit; count remains `169/170` until a separate, governed Review A + per-identity decision. |
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

**Note (added by `FE-EVID03-COND1-THRESHOLD-RECAL-001-ACTIVATION-001`,
this document's own later activation transaction; the paragraph above is
preserved unchanged as the correct historical record at its own
boundary):** the `87.001959503592%` threshold cited above has since been
recalibrated and activated — the controlling Condition-1 gate is now
Condition 1A (raw score ≥ `85.812095853937%`) AND Condition 1B (42 pinned
current-material identities individually resolved); see the Primary Work
Package paragraph near the end of this document and
`docs/governance/mutation-baseline-evidence/feature-engine-mutation-
threshold-recalibration-proposal-001.md` for the current, controlling
authority.

**Second note (added by `FE-EVID03-COND1-THRESHOLD-RECAL-V2-001`, this
document's own later activation transaction; both the paragraph above and
the note immediately above are preserved unchanged as the correct
historical record at their own boundary):** proposal-001 and its
`85.812095853937%`/42-ID gate have themselves since been superseded — the
controlling Condition-1 gate is now Condition 1A (raw score ≥
`85.127424876379%`) AND Condition 1B (24 pinned current-material
identities in `feature-engine-condition1-current-material-gap-set-
002.json` individually resolved); see the Primary Work Package paragraph
near the end of this document and
`docs/governance/mutation-baseline-evidence/feature-engine-mutation-
threshold-recalibration-proposal-002.md` for the current, controlling
authority.

**Third note (added by `FE-EVID03-COND1-THRESHOLD-RECAL-V3-001`, this
document's own later activation transaction; the paragraph above and both
notes immediately above are preserved unchanged as the correct historical
record at their own boundary):** proposal-002 and its
`85.127424876379%`/24-ID gate have themselves since been superseded — the
controlling Condition-1 gate is now Condition 1A (raw score ≥
`84.899201217193%`) AND Condition 1B (18 pinned current-material
identities in `feature-engine-condition1-current-material-gap-set-
003.json` individually resolved); see the Primary Work Package paragraph
near the end of this document and
`docs/governance/mutation-baseline-evidence/feature-engine-mutation-
threshold-recalibration-proposal-003.md` for the current, controlling
authority. No fresh formal mutation measurement has been performed since
Wave 5/6 — the current Condition 1 status is `AWAITING FRESH FORMAL
MEASUREMENT`, not a re-assertion of any prior raw score.

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

**Primary Work Package — Delegated Technical Resolution recorded
(`FE-EVID03-COND2-CANDIDATE-005-DTR-001`): COMPLETE — `RESOLVED —
DELEGATED TECHNICAL RESOLUTION`.** ChatGPT's earlier `CLEAN` Review A on
Candidate-005 (boundary `31fc6f5dda1834916f68c55656bd2fa4893bdcb8`) was
pre-activation and, per `X-MIN-02`, did not by itself satisfy `D8`. A
fresh, post-activation Review A (ChatGPT, `AI Technical Architect` —
distinct from Candidate-005's own authoring/executing principal `Claude`,
satisfying `D8`) independently re-verified Candidate-005's exact
subject/evidence at boundary `1e4078c3edba521c7f6f182da09dd8c833b9a734`
and returned `CLEAN — 0 Blocker / 0 Major / 0 Minor`, Risk `R1`, ADR
Scope `ADR_NOT_REQUIRED`. `D1`–`D12` all independently confirmed `PASS`.
Both rows resolved via `DELEGATED TECHNICAL RESOLUTION — CLEAN`
(resolution ID `FE-EVID03-COND2-CANDIDATE-005-DTR-001`) — **this is NOT
a Product Owner approval**; `product_owner_state` on both rows is
explicitly `NOT_REQUIRED_DUE_TO_DELEGATED_TECHNICAL_RESOLUTION`, never
`APPROVED`. Row 1 (`_reevaluate_all_windows__mutmut_32` →
`_prepare_reevaluate_all_windows__mutmut_32`, `killed`) and Row 2
(`on_swing_confirmed__mutmut_35` → `prepare_swing_confirmed__mutmut_35`,
`killed`, message-text-only historical mutation, materiality tag
unchanged) both closed `RECLASSIFIED_4_1_B — LEGITIMATE REFACTOR /
SUCCESSOR VERIFIED`. Both statuses independently re-cross-checked
against `evidence-005.json`'s own `full_current_mutant_mapping` — both
`killed`, zero discrepancy. No mutation execution performed. **Condition
2: `167/170` → `169/170`.** Remaining unresolved: exactly 1 row,
`contracts.x__seal_verified_authority__mutmut_33` —
`TOOL_IDENTITY_DRIFT — NO EXISTING GOVERNED RESOLUTION MECHANISM` — NOT
resolved by this transaction, no identity-continuity mechanism invented.

**Work Package — governance-improvement candidate authoring
(`GOV-DELEGATION-MODEL-ADR-045-AUTHOR-001`): COMPLETE.** Authored
`docs/adr/ADR-045.md` v0.1 (`Draft`), `docs/constitution/00-governance.md`
v1.5 (`Draft` candidate), and `docs/governance/execution-rules.md` v0.7
(`CANDIDATE`) — a bounded **Delegated Technical Resolution** lane. ADR
Scope Rule run fresh: `ADR_REQUIRED`; expected Risk `R2` (not
self-finalized). Verified no genuine contradiction in Chapter 11, Chapter
12, the ADR template, `/docs/team/team.yaml`, or Phase-3 Rules — none
modified.

**Work Package — bounded correction
(`GOV-DELEGATION-MODEL-ADR-045-CORR-001`): COMPLETE.** ChatGPT's fresh
Review A on the v0.1/v1.5/v0.7 bundle returned `REVISION_REQUIRED — 0
Blocker / 2 Major / 1 Minor`, Risk `R2` — `MAJOR-01` (ADR-045 corrected
to `supersedes: [ADR-042]` instead of "extends"), `MAJOR-02` (Chapter 0
§3 corrected to exactly ONE future controlling branching workflow, old
diagram historical-only), `MINOR-01` (`D10` corrected to cover both
governing-artifact reservation and explicit Product Owner call-in) — all
remediated in `ADR-045` v0.2.

**Primary Work Package — consolidated bounded correction
(`GOV-DELEGATION-MODEL-ADR-045-CORR-002`): COMPLETE.** ChatGPT's fresh
Review A on the v0.2 bundle (boundary
`bced025c6df3ca36f46313862fddac2c5c3dc8c1`, blob `033c2a95...`) returned
`CLEAN — 0 Blocker / 0 Major / 1 Minor`, Risk `R2`. The Product Owner
selected the optional independent cross-check, which returned `DEFECT
FOUND — 0 Blocker / 2 Major / 5 Minor`; ChatGPT independently
re-verified and accepted all 7 (effective input `0 Blocker / 2 Major / 5
Minor`; the prior round's Review-A-provenance Minor absorbed into
`X-MAJ-02`). **`X-MAJ-01`** — DTR lacked distinct-principal
independence: `D8` strengthened to require, for DTR only, BOTH an
independent CLEAN Review A verdict AND a principal distinct from every
author/executor of the underlying work — narrow safeguard, no mandatory
Review B restored, exactly one Review A. **`X-MAJ-02`** — R0/R1/R2
authority migration was incomplete: `ADR-045` now self-contains the FULL
R0/R1/R2 definitions, unchanged in substance, becoming the current
definition authority once activated; Chapter 0 v1.5, a new Chapter 11
v2.4 successor candidate, the ADR template, and Execution Rules v0.7 all
redirect their future definition-source pointer to `ADR-045`.
**`X-MIN-01`** — added document `Accepted`/`EFFECTIVE` and package/
artifact `Consolidated Stable` to the PO-reserved/non-delegable lists.
**`X-MIN-02`** — a pre-activation Review A verdict is historical input
only and does NOT by itself satisfy `D8` for a post-activation delegated
closure — `Candidate-005`'s existing `CLEAN` review does not, by itself,
satisfy a future `D8`. **`X-MIN-03`** — fresh-verified and mechanically
reconciled two pre-existing MANIFEST bookkeeping defects: Execution
Rules row (stale `0.5`/`EFFECTIVE`, actual `0.6`/`EFFECTIVE` + `v0.7`
`CANDIDATE` preview) and Phase-3 Rules row (stale `0.2`/`CANDIDATE`,
actual `0.3`/`EFFECTIVE`) — `phase-3-rules.md` itself byte-unchanged.
**`X-MIN-04`** — `ADR-045`'s Review-A table corrected to record both
review rounds accurately. **`X-MIN-05`** — defined a generic delegated-
closure recording rule (`resolution_authority`/`delegated_resolution_
state` fields) and a legacy-schema mapping rule (never write `APPROVED`;
map to an explicit non-PO value; `D12` fails if the schema cannot
represent the result unambiguously) — `Candidate-005`'s own artifact
NOT edited. `ADR-045` `v0.2 → v0.3`, still `Draft`. Chapter 0 stays
`v1.5`/`Draft`; Chapter 11 `v2.4` successor candidate authored (`v2.3`
remains controlling); Execution Rules stays `v0.7`/`CANDIDATE`; ADR
template aligned with a before/after-activation bridge reference. This
correction did **not** activate the new model, did **not** request
Product Owner approval, and did **not** resolve Candidate-005.

**Primary Work Package — atomic activation
(`GOV-DELEGATION-MODEL-ADR-045-ACTIVATION-001`): COMPLETE — `DONE /
ACTIVATED`.** Final Review A (ChatGPT) on the v0.3 bundle (boundary
`e54159aa8355cfd1d3d309d43969007b645246ed`) returned `CLEAN — 0 Blocker
/ 0 Major / 1 Minor`, Risk `R2` — the residual Minor was non-semantic
provenance wording only, folded into this activation as deterministic
cleanup per explicit Product Owner authorization; no additional
cross-check required. Product Owner decision (verbatim): "APPROVE
ADR-045 v0.3 and its atomic activation. Accept Review A CLEAN — 0
Blocker / 0 Major / 1 Minor, Risk R2. Fold the non-semantic
provenance-wording cleanup into activation. No additional cross-check
required." (`2026-09-23T14:02+07:00`). Atomically, in one commit:
`ADR-045` `Draft → Approved` (v0.3 unchanged, `supersedes: [ADR-042]`
unchanged, now immutable); `ADR-042` current lifecycle `Approved →
Superseded` (by `ADR-045`, reverse relation recorded, `ADR-042.md`
byte-immutable/unmodified); Chapter 0 `v1.5` `Draft → Locked` (now
controlling, `v1.4` historical predecessor); Chapter 11 `v2.4` `Draft →
Locked` (now controlling, `v2.3` historical predecessor); Global
Execution Rules `v0.7` `CANDIDATE → EFFECTIVE` (`G-DELEGATE-001`/
`G-DELEGATE-002` now effective, `v0.6` historical predecessor). The
**Delegated Technical Resolution model is now binding governance
authority**: an R0/R1 decision satisfying the closed `D1`–`D12`
predicate (including the `D8` distinct-principal safeguard) closes as
`DELEGATED TECHNICAL RESOLUTION` without a Product Owner Decision step;
R2, `ADR_REQUIRED`, and every other Product-Owner-reserved class
continue to route to Product Owner Decision exactly as before. This
activation does **not** resolve Candidate-005, approve Feature Engine,
or authorize LIVE — Candidate-005's pre-activation `CLEAN` Review A does
not, by itself, satisfy `D8`; a separate, subsequent, bounded
transaction is required for its own fresh post-activation `D1`–`D12`
determination.

**Deferred / blocked item:** `contracts.x__seal_verified_authority__mutmut_33`
— `TOOL_IDENTITY_DRIFT — NO EXISTING GOVERNED RESOLUTION MECHANISM`.

**Primary Work Package — Condition-1 post-Evidence-005 survivor
assessment (EVIDENCE/DIAGNOSTIC only): COMPLETE.** Fresh-verified
starting HEAD `2ca64a46a91a907c8976e7fe4ad6acaf151ac628` ==
`origin/main`, no drift; Evidence-005 blob
`f7a6ab715155ad166808e0e9d9a7474196d9b69d` unchanged. Built the exact
current 406-survivor set from `full_current_mutant_mapping.
survivor_mutant_ids` (exact match, no inference); extracted every
survivor's precise diff via a zero-test, offline reproduction of
mutmut's own static CST mutation generator (no pytest, no coverage, no
test execution — self-verified as an exact 2629/2629 match against
Evidence-005's own mutant universe). Classified all 406 survivors:
`GENUINE_TEST_GAP=40`, `LOW_MATERIALITY_MESSAGE_TEXT=344`,
`PROVABLY_EQUIVALENT=16`, `STRUCTURALLY_UNREACHABLE=4`, `UNCLEAR=2`.
Fresh-reassessed the named deferred candidates (`ownership.
_catch_up__mutmut_7`/`_18`, `_select_eligible_swing`'s two swing_id
tie-break mutants, `_total_order_key`'s revision-sign mutant) — all
four `GENUINE_TEST_GAP`. Fresh-assessed the known
`identity.x_deterministic_id__mutmut_3` killed→survived regression:
**GENUINE MISSING TEST**, not tooling/selection instability. Threshold
math: even crediting all 40 genuine + 2 unclear + all 9 unstable
mutants as killed, the resulting numerator (`2265`) remains `23` short
of the required `2288`. **Feasibility result: Case C — `CURRENT
TEST-ONLY PATH APPEARS INSUFFICIENT`** — does not change the approved
threshold. Full record, 8 ranked high-yield clusters:
`docs/governance/mutation-baseline-evidence/feature-engine-condition1-post-e005-survivor-assessment-001.json`.
This diagnostic did **not** change Condition 1's formal result, did
**not** touch Condition 2, did **not** implement any test, and did
**not** resolve the `TOOL_IDENTITY_DRIFT` row.

**Deferred / blocked item:** `contracts.x__seal_verified_authority__mutmut_33`
— `TOOL_IDENTITY_DRIFT — NO EXISTING GOVERNED RESOLUTION MECHANISM`.

**Primary Work Package — Condition-1 threshold recalibration proposal
(candidate authoring only): COMPLETE.** Fresh-verified starting HEAD
`c77af110d7c273c7731001eaa218774c7fd7db95` == `origin/main`, no drift.
Independently re-derived the calibration-drift arithmetic: even
crediting every non-message-text survivor (40 genuine + 2 unclear + 16
equivalent + 4 unreachable + 9 unstable = 71) as killed, the numerator
(`2285`) remains `3` short of the required `2288` — **
`CALIBRATION_DRIFT_CONFIRMED`** against the original Candidate-3 intent
(explicitly NOT requiring message-text closure). Fresh-resolved the 2
`UNCLEAR` survivors in place: `ownership.acquire_and_activate
__mutmut_21`/`_23`, both **`PROVABLY_EQUIVALENT`** (the intermediate
`CATCHING_UP` handle is unconditionally overwritten on every path
before any code observes it) — settled `GENUINE_TEST_GAP=40`,
`PROVABLY_EQUIVALENT=18`, `UNCLEAR=0`. Evaluated three models: **Model
A** (numeric re-baseline, conservative candidate `85.736021300875%`,
derived as `(2214+40)/2629`) — **recommended**; **Model B**
(denominator/exclusion semantics change) — NOT recommended, high
anti-gaming risk; **Model C** (materiality-aware primary gate) — NOT
activated, new classification-drift risk. Both Model A figures remain
above the current actual raw score — not chosen merely to pass today.
Proposed (not activated) a fourth recalibration trigger —
`MATERIALITY / MUTATION-POPULATION COMPOSITION DRIFT`. ADR Scope Rule
freshly re-run against Model A: `ADR_OPTIONAL`. Risk candidate: `R1`.
New artifact: `docs/governance/mutation-baseline-evidence/feature-engine-mutation-threshold-recalibration-proposal-001.md`,
status `CANDIDATE — NOT EFFECTIVE / AWAITING REVIEW A`. This
transaction did **not** activate any threshold, did **not** request a
Product Owner decision, and did **not** touch Condition 2 or 3.

**Deferred / blocked item:** `contracts.x__seal_verified_authority__mutmut_33`
— `TOOL_IDENTITY_DRIFT — NO EXISTING GOVERNED RESOLUTION MECHANISM`.

**Primary Work Package — bounded correction of the Condition-1
recalibration proposal: COMPLETE.** Fresh-verified starting HEAD
`0c9f4ef8eb8d7ad45afb604b3a8e7cfd1883fde9` == `origin/main`, no drift.
Review A returned `REVISION_REQUIRED — 0 Blocker / 2 Major / 2 Minor`,
Risk `R1`, ADR Scope `ADR_OPTIONAL` (R1 default: no independent
cross-check). `MAJOR-01`: Model A corrected to an explicit two-part
gate — Condition 1A (raw score >= recalibrated threshold) **AND**
Condition 1B (all 42 pinned current-material identities individually
resolved, reusing the §4.1 pattern; unrelated kills can never
substitute) — a NEW obligation, explicitly separate from Condition 2's
historical 170-identity obligation. `MAJOR-02`: reclassified
`ownership.acquire_and_activate__mutmut_21`/`_23` from
`PROVABLY_EQUIVALENT` to **`GENUINE_TEST_GAP`** — `owner.handle`/
`owner.state` are public properties observable by a concurrent reader
while `acquire_and_activate` is blocked mid-flight, and the prior
single-thread-only observability assumption was false. Settled:
`GENUINE_TEST_GAP=42`, `LOW_MATERIALITY_MESSAGE_TEXT=344`,
`PROVABLY_EQUIVALENT=16`, `STRUCTURALLY_UNREACHABLE=4`, `UNCLEAR=0`.
`CALIBRATION_DRIFT_CONFIRMED` preserved (robustness numerator `2285`
still `3` short of `2288`, cardinality unchanged by the
reclassification). New pinned identity artifact:
`docs/governance/mutation-baseline-evidence/feature-engine-condition1-current-material-gap-set-001.json`
(42 IDs, 0 duplicates). Corrected Model A candidate: `85.812095853937%`
(= (2214+42)/2629, required numerator `2256`), superseding
`85.736021300875%`. `MINOR-01`: review authority corrected to current
ADR-045/Chapter 11 v2.4 (R1 = Review A only, no Independent Review B);
the numeric-threshold decision itself remains explicitly
Product-Owner-reserved (ADR-045 D10(a)) — DTR is NOT eligible for it.
`MINOR-02`: defined one exact future SSOT transition (old threshold
document → historical/superseded; new document → sole current
authority if/when activated) — future semantics only, not performed
now. ADR Scope Rule freshly re-run against the corrected model:
`ADR_OPTIONAL`. Risk candidate: `R1`. No ADR authored.

**Deferred / blocked item:** `contracts.x__seal_verified_authority__mutmut_33`
— `TOOL_IDENTITY_DRIFT — NO EXISTING GOVERNED RESOLUTION MECHANISM`.

**Primary Work Package — ATOMIC PRODUCT OWNER ACTIVATION of the
Condition-1 threshold recalibration: `DONE / ACTIVATED`.** Fresh-verified
starting HEAD `b16f57e06be265125123cc3c7eb0b2d2bdc75c17` == `origin/main`,
no drift. Final Review A (ChatGPT) on the corrected proposal returned
`CLEAN — 0 Blocker / 0 Major / 1 Minor`, Risk `R1`, ADR Scope
`ADR_OPTIONAL` — R1 default no cross-check, none performed. Product Owner
decision (verbatim): "APPROVE the Feature Engine Condition-1 threshold
recalibration at boundary b16f57e06be265125123cc3c7eb0b2d2bdc75c17.
Replace the current 87.001959503592% Condition-1 threshold with Model A:
Condition 1A: raw mutation-effectiveness >= 85.812095853937%
(2256/2629 at the reviewed calibration boundary); AND Condition 1B: all
42 exact current-material-gap identities in
feature-engine-condition1-current-material-gap-set-001.json must be
individually resolved under the governed per-identity mechanism.
Preserve Condition 2 and Condition 3 as independent requirements. Accept
Review A CLEAN — 0 Blocker / 0 Major / 1 Minor, Risk R1, ADR_OPTIONAL.
Fold the non-semantic two-row provenance-source correction into the
atomic activation. No independent cross-check required."
(`2026-09-23T20:01+07:00`). Authorized non-semantic provenance cleanup
folded in: the 42-ID artifact's two `acquire_and_activate
__mutmut_21`/`_23` `source` fields corrected from inaccurate
`"post-E005 assessment (GENUINE_TEST_GAP)"` to `"Review-A MAJOR-02
correction: post-E005 assessment UNCLEAR -> GENUINE_TEST_GAP"` — 42-ID
set/count/duplicates/order/hash all verified unchanged; blob
`6360c8c1...` → `49c30b439e...`. `feature-engine-mutation-threshold-
recalibration-proposal-001.md` `CANDIDATE → APPROVED — EFFECTIVE`
(resulting blob `12040044578d57d15e699a327a5a8ae39c1e9ea3`) and is now
the **sole current Feature Engine Condition-1 threshold authority**:
Condition 1A (raw score >= `85.812095853937%`) AND Condition 1B (all 42
current-material identities individually resolved).
`feature-engine-mutation-threshold-proposal-001.md` (old
`87.001959503592%`) becomes historical/superseded, byte-unchanged.
MANIFEST now carries one canonical current-threshold pointer.

**Deferred / blocked item:** `contracts.x__seal_verified_authority__mutmut_33`
— `TOOL_IDENTITY_DRIFT — NO EXISTING GOVERNED RESOLUTION MECHANISM`.

**Primary Work Package — Wave-5 test remediation (25 low-complexity/
high-yield Condition-1B current-material gaps): COMPLETE.**
Fresh-verified starting HEAD `a9f75be3ffa5df6d4b6f8b361ff15f28d6e0370a`
== `origin/main`, no drift; governing authority (activated
recalibration proposal, 42-ID artifact + hash) fresh-verified exact.
Fresh-re-extracted all 25 target IDs' exact diffs before designing
tests. Wrote 20 new real, behavior-oriented tests across 7 files (1
new: `test_identity.py`) — full ordinary suite **434/434 passed** (was
414); `ruff`/`mypy` clean. Bounded targeted mutation verification
(`python -m tooling run <id> ...`, real execution scoped to exactly
the 25 named IDs): **12/25 targeted kills verified** (Cluster A
wrong-type-validation 0/9; Cluster B malformed-field 4/5; Cluster C
`zip(strict=True)` 3/6; Cluster D quote-parsing 4/4; Cluster E
deterministic-ID 1/1). Honest analysis of the 13 survivors: Cluster
A's 9 are message-text-only (`type(X)` → `type(None)`, corrects an
inherited assumption — no crash, same exception type either way);
`resolve_historical...mutmut_23` and `_finalize_prepared_batch`'s
`mutmut_8`/`_11`/`_12` (4 more) are STRUCTURALLY_UNREACHABLE given an
earlier unconditional guard in the same function — none gamed.
**Implementation evidence only — formal Condition 1B credit NOT
claimed.** New artifact:
`feature-engine-condition1-wave5-test-remediation-001.json`, exact
17-ID Wave-6 complement persisted. `ADR_NOT_REQUIRED`; Risk `R1`. No
`src/`/`tooling/` change.

**Deferred / blocked item:** `contracts.x__seal_verified_authority__mutmut_33`
— `TOOL_IDENTITY_DRIFT — NO EXISTING GOVERNED RESOLUTION MECHANISM`.

**PO action required now:** No. Wave-5 is COMPLETE. Condition 1 remains
`FAIL — criteria` — no fresh formal mutation measurement was performed,
and formal Condition 1B credit is NOT claimed for any of the 12
targeted-killed identities (implementation evidence only, pending a
later, separately-governed formal measurement transaction). Condition
2 (`169/170`) and Condition 3 (`SATISFIED`) preserved as independent
requirements, not merged with Condition 1B. Candidate-005 remains
recorded `RESOLVED — DELEGATED TECHNICAL RESOLUTION` (`FE-EVID03-
COND2-CANDIDATE-005-DTR-001`) — a governed technical resolution under
`ADR-045` v0.3, **not** a Product Owner approval. EVID-03 remains OPEN
independently on both grounds; Feature Engine remains NOT APPROVED;
Phase-3 module approval remains NOT GRANTED; LIVE remains
NOT_AUTHORIZED. The sole remaining Condition-2 item,
`contracts.x__seal_verified_authority__mutmut_33`
(`TOOL_IDENTITY_DRIFT — NO EXISTING GOVERNED RESOLUTION MECHANISM`),
remains unresolved; no identity-continuity mechanism was invented. Next
governed step: a separate, subsequent, bounded Work Package for Wave-6
(the remaining 17 current-material identities), and, independently, a
future formal measurement transaction to determine actual Condition-1B
credit — neither initiated here.

## 5. Work Package lanes

| Lane | Item | Status |
|---|---|---|
| Primary | *(none currently assigned)* | `FE-EVID03-COND1-WAVE5-001`, `FE-EVID03-COND1-AUDIT-001`, `FE-EVID03-COND1-MATERIAL-SET-DTR-001`, `FE-EVID03-COND1-THRESHOLD-RECAL-V2-001`, `FE-EVID03-COND1-WAVE6-001`, `FE-EVID03-COND1-WAVE6-CLASSIFICATION-DTR-001`, `FE-EVID03-COND1-THRESHOLD-RECAL-V3-001`, `FE-EVID03-COND1-FORMAL-EVID-006-001`, `FE-EVID03-COND1-FORMAL-006-DTR-001`, `FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001`, and `FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001-CORR-001` (bounded correction remediating Review A round-1 `MAJOR-01` — approval-routing contradiction between §10.1 and §11, corrected; no credit granted) are all COMPLETE. Condition 1: `PASS — REVIEW A VALIDATED`. Condition 2 remains `169/170`. Next primary WP: a bounded ChatGPT Review A re-review of the corrected tool-identity-continuity candidate — awaits a separate scoping decision. |
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
| Completed | `GOV-DELEGATION-MODEL-ADR-045-AUTHOR-001` | `ADR-045` v0.1 `Draft` authored (Delegated Technical Resolution lane); Chapter 0 v1.5 + Execution Rules v0.7 candidates authored; Review A returned `REVISION_REQUIRED — 0 Blocker / 2 Major / 1 Minor`, R2 — remediated by the CORR-001 WP |
| Completed | `GOV-DELEGATION-MODEL-ADR-045-CORR-001` | `ADR-045` v0.2 `Draft` (supersedes ADR-042, single branching workflow, D10 covers PO call-in); Review A `CLEAN — 0/0/1`, R2; optional PO-selected cross-check `DEFECT FOUND — 0/2/5`, accepted — remediated by the CORR-002 WP |
| Completed | `GOV-DELEGATION-MODEL-ADR-045-CORR-002` | `ADR-045` v0.3 `Draft` (D8 distinct-principal, self-contained R0/R1/R2, Chapter 11 v2.4 candidate authored); Review A `CLEAN — 0/0/1`, R2 — approved/activated by the ACTIVATION-001 WP |
| Completed | `GOV-DELEGATION-MODEL-ADR-045-ACTIVATION-001` | `DONE / ACTIVATED` — `ADR-045` `Approved`, `ADR-042` `Superseded`, Chapter 0 v1.5 `Locked`, Chapter 11 v2.4 `Locked`, Execution Rules v0.7 `EFFECTIVE`; Delegated Technical Resolution model now binding |
| Completed | `FE-EVID03-COND2-CANDIDATE-005-DTR-001` | `RESOLVED — DELEGATED TECHNICAL RESOLUTION` (not a Product Owner approval) — fresh post-activation Review A `CLEAN — 0/0/0`, R1, `ADR_NOT_REQUIRED`, D1-D12 all PASS (D8: reviewer ChatGPT distinct from author/executor Claude); both rows `RECLASSIFIED_4_1_B`; Condition 2 `167/170 → 169/170`; remaining item is the deferred `TOOL_IDENTITY_DRIFT` row |
| Completed | `FE-EVID03-COND2-CANDIDATE-005-DTR-DIAG-001` | Condition-1 post-Evidence-005 survivor assessment (EVIDENCE/DIAGNOSTIC only) — all 406 survivors classified (`GENUINE_TEST_GAP=40`, `LOW_MATERIALITY_MESSAGE_TEXT=344`, `PROVABLY_EQUIVALENT=16`, `STRUCTURALLY_UNREACHABLE=4`, `UNCLEAR=2`); named section-7/8 candidates fresh-reassessed; **Case C — `CURRENT TEST-ONLY PATH APPEARS INSUFFICIENT`** (best-case combined numerator `2265`, still `23` short of `2288`); Condition 1/2 formal status unchanged |
| Completed | `FE-EVID03-COND1-THRESHOLD-RECAL-001` | Condition-1 threshold recalibration proposal authored, `CANDIDATE — NOT EFFECTIVE / AWAITING REVIEW A` — **`CALIBRATION_DRIFT_CONFIRMED`** (71-credit robustness check still `3` short of `2288`); 2 `UNCLEAR` survivors fresh-resolved to `PROVABLY_EQUIVALENT`; Model A (`85.736021300875%`) recommended over Models B/C; `ADR_OPTIONAL`; Risk `R1`; currently-effective `87.001959503592%` threshold NOT changed — **superseded by the CORR-001 WP below** |
| Completed | `FE-EVID03-COND1-THRESHOLD-RECAL-001-CORR-001` | Bounded correction remediating Review A `REVISION_REQUIRED — 0/2/2`, R1, `ADR_OPTIONAL` — `MAJOR-01`: Model A corrected to explicit Condition 1A/1B two-part gate (42 pinned current-material identities, reusing §4.1 pattern); `MAJOR-02`: `acquire_and_activate__mutmut_21`/`_23` reclassified `PROVABLY_EQUIVALENT` → `GENUINE_TEST_GAP` (public-property concurrent observability); settled `GENUINE_TEST_GAP=42`/`PROVABLY_EQUIVALENT=16`/`UNCLEAR=0`; corrected candidate `85.812095853937%` (numerator `2256`); `MINOR-01`: review authority corrected to ADR-045/Chapter 11 v2.4 (R1 = Review A only), DTR ineligible for threshold decision (D10(a)); `MINOR-02`: exact future SSOT transition defined; new artifact `feature-engine-condition1-current-material-gap-set-001.json` (42 IDs); `ADR_OPTIONAL`; Risk `R1`; currently-effective `87.001959503592%` threshold NOT changed — **activated by the ACTIVATION-001 WP below** |
| Completed | `FE-EVID03-COND1-THRESHOLD-RECAL-001-ACTIVATION-001` | `DONE / ACTIVATED` — Final Review A `CLEAN — 0/0/1`, R1, `ADR_OPTIONAL`, no cross-check. Product Owner approved the recalibration at boundary `b16f57e06be265125123cc3c7eb0b2d2bdc75c17`, folding the authorized non-semantic 2-row provenance cleanup (42-ID artifact `6360c8c1...` → `49c30b439e...`, set/count/hash unchanged) into the atomic activation. `feature-engine-mutation-threshold-recalibration-proposal-001.md` `CANDIDATE → APPROVED — EFFECTIVE` (resulting blob `12040044578d...`), now sole current Condition-1 threshold authority: Condition 1A (raw score ≥ `85.812095853937%`) AND Condition 1B (42 current-material identities individually resolved). Old `87.001959503592%` threshold now historical/superseded, byte-unchanged. Condition 2/3 preserved independent. Condition 1 remains `FAIL — criteria` (no fresh measurement performed) |
| Completed | `FE-EVID03-COND1-WAVE5-001` | Wave-5 test remediation of 25 low-complexity/high-yield Condition-1B identities — 20 new tests across 7 files (`test_identity.py` new), ordinary suite `434/434 passed` (was 414), `ruff`/`mypy` clean. Bounded targeted mutation verification (25 named IDs only): **`12/25` targeted kills verified** (Cluster A `0/9`, B `4/5`, C `3/6`, D `4/4`, E `1/1`). 13 survivors honestly reported: Cluster A (9) message-text-only (`type(X)`→`type(None)`, no crash, corrects a prior inherited assumption); 4 more `STRUCTURALLY_UNREACHABLE` given an earlier unconditional guard already in the same function — none gamed. **Implementation evidence only — formal Condition 1B credit NOT claimed.** New artifact `feature-engine-condition1-wave5-test-remediation-001.json`; exact 17-ID Wave-6 complement persisted. `ADR_NOT_REQUIRED`; Risk `R1`. No `src/`/`tooling/` change; Condition 1 remains `FAIL — criteria` |
| Completed | `FE-EVID03-COND1-AUDIT-001` | Consolidated root-cause audit of all 42 activated Condition-1B identities, triggered by Wave-5's own 13 honestly-reported false positives. Fresh-re-extracted all 42 diffs (2629/2629 self-verified); independently re-classified every identity from first principles. 17-ID Wave-6 complement analyzed for the first time: 13 `GENUINE_TEST_GAP`, 2 `STRUCTURALLY_UNREACHABLE`, 2 `UNCLEAR/DISPUTED` (`acquire_and_activate__mutmut_21`/`_23` — stricter re-check cannot confirm Task C's MAJOR-02 concurrent-observability argument; deferred to a separate Review A). All 12 Wave-5-killed identities re-audited: 11 confirmed, 1 reclassified (`identity.x_deterministic_id__mutmut_3` tests an implementation detail, not a documented contract). Final: `GENUINE_TEST_GAP 24 / LOW_MATERIALITY_MESSAGE_TEXT 9 / LOW_MATERIALITY_IMPLEMENTATION_DETAIL 1 / STRUCTURALLY_UNREACHABLE 6 / UNCLEAR 2`. Candidate math (informational, same `2214`/`2629` boundary): `M=24` → `85.12742487637885%`; `M=26` (incl. disputed) → `85.20349942944085%` — **neither activated**. Active threshold/42-ID gate remain fully controlling, now noted conservative/over-strict, not permissive. No threshold change, no DTR (deferred to a separate distinct-principal Review A), activated artifacts byte-unchanged. New artifact `feature-engine-condition1-material-gap-root-cause-audit-001.json`. **Wave 6 implementation PAUSED pending material-set audit.** `ADR_NOT_REQUIRED`; Risk `R1`. No `src/`/`test`/`tooling` change; Condition 1 remains `FAIL — criteria` |
| Completed | `FE-EVID03-COND1-MATERIAL-SET-DTR-001` | Delegated Technical Resolution recording the already-issued ChatGPT Review A adjudication of the root-cause audit's 18 non-material/disputed identities. Verdict: `CLEAN — 0 Blocker / 0 Major / 1 Minor`, Risk `R1`, `ADR_NOT_REQUIRED`; D1-D12 all `PASS`; D8 distinct-principal (ChatGPT vs. audit author/executor Claude) satisfied. Minor (non-semantic, corrected here — audit artifact immutable): D10(a) reserves only the numeric threshold decision, not individually-governed exact-ID reclassification. Governed disposition: 9 `LOW_MATERIALITY_MESSAGE_TEXT`, 6 `STRUCTURALLY_UNREACHABLE`, 1 `LOW_MATERIALITY_IMPLEMENTATION_DETAIL`, 2 `NON_MATERIAL_TRANSIENT_IN_FLIGHT_STATE` (`acquire_and_activate__mutmut_21`/`_23` now confirmed non-material — no concurrent-observation contract, no effect on any authoritative outcome) all `RECLASSIFIED`. Final: `GENUINE_TEST_GAP 24 / NON_MATERIAL 18 / UNCLEAR 0`. Condition 1B accounting: `18/42 RESOLVED_BY_DELEGATED_TECHNICAL_RECLASSIFICATION`, `24/42 still require resolution` (11 with Wave-5 targeted-kill evidence, formal credit NOT claimed; 13 unremediated). Candidate math unchanged (`M=24` → `85.12742487637885%`), still NOT activated. No threshold change; no formal kill credit; root-cause audit artifact, 42-ID artifact, recalibration proposal, and Wave-5 evidence all byte-unchanged. New artifact `feature-engine-condition1-material-gap-dtr-001.json`. Wave 6 remains PAUSED. `ADR_NOT_REQUIRED`; Risk `R1`. No `src/`/`test`/`tooling` change; Condition 1 remains `FAIL — criteria` |
| Completed | `FE-EVID03-COND1-THRESHOLD-RECAL-V2-001` | Authored the final, bounded Condition-1 threshold-correction candidate, built directly on the DTR's Review-A-validated final partition (`GENUINE_TEST_GAP=24 / NON_MATERIAL=18 / UNCLEAR=0`). Same `2214`/`2629` calibration boundary as the active proposal: candidate numerator `2214+24=2238` → `85.127424876379%` (full precision `85.12742487637885%`). New `CANDIDATE — NOT EFFECTIVE / AWAITING REVIEW A` documents: `feature-engine-mutation-threshold-recalibration-proposal-002.md` and `feature-engine-condition1-current-material-gap-set-002.json` (exact 24 IDs from the DTR's `remaining_material_24_sorted`, sha256 `6c8181f7665a63494632ef89514ea7efdf9948c544c9a9a8094e87c17c3d2543`). Proposed gate: Condition 1A (`raw score ≥ 85.127424876379%`) AND Condition 1B (24 exact set-002 IDs individually resolved). Explicitly shown NOT pass-fitting: current raw score `84.21%–84.56%` remains below the candidate figure, so Condition 1A would still FAIL today even if activated. Active gate (`85.812095853937%` / 42-ID set-001) NOT activated, touched, or superseded. No Review A performed; no PO decision requested; DTR NOT eligible for this candidate's own activation (ADR-045 `D10(a)`, PO-reserved). `ADR_OPTIONAL`; Risk `R1` (candidate disposition). Wave 6 remains PAUSED pending this candidate's own Review A/decision. No `src/`/`test`/`tooling` change; Condition 1 remains `FAIL — criteria` |
| Completed | `FE-EVID03-COND1-THRESHOLD-RECAL-V2-001` (activation) | Executed the Product-Owner-authorized atomic activation of threshold recalibration proposal-002 at reviewed boundary `f99f75973049e71b7e3f1876ba0683a7d8434d48` (reviewed proposal blob `4ca7354600ccd81331b3fb8a46f25327bdf53371`, reviewed set-002 blob `d4558f37c8c9084bf8f404309c342126733eeebc`). Review A: ChatGPT, **CLEAN — 0 Blocker / 0 Major / 0 Minor**, Risk `R1`, ADR Scope `ADR_OPTIONAL`, no independent cross-check required/performed. `feature-engine-mutation-threshold-recalibration-proposal-002.md` → **`APPROVED — EFFECTIVE`** (resulting blob `ea0b7a79b733622388597c59346c4615bb2726db`), now sole current Condition-1 threshold authority: Condition 1A (raw score ≥ `85.127424876379%`, basis `2238/2629`) AND Condition 1B (24 exact set-002 IDs individually resolved). `feature-engine-condition1-current-material-gap-set-002.json` → **`APPROVED — EFFECTIVE`** (resulting blob `2e6030c5581df51323937de0bd5f646f3e98b5d9`), exact 24-ID membership/count/duplicates/hash all verified unchanged. Old proposal-001 (`85.812095853937%`) and old set-001 (42 IDs) now historical/superseded, both byte-unchanged. Condition 2/3 preserved independent. Current Condition 1: `FAIL — criteria` (1A FAIL: `84.21%–84.56% < 85.127424876379%`; 1B FAIL: formal closure incomplete). Wave 6 changes from `PAUSED` to **`READY FOR BOUNDED IMPLEMENTATION — 13 genuine unremediated identities`** — NOT implemented by this activation. No `src/`/`test`/`tooling` change; Condition 1 remains `FAIL — criteria` |
| Completed | `FE-EVID03-COND1-WAVE6-001` | Implemented tests against the exact 13 unremediated identities in the active 24-ID gate. Baseline targeted verification: all 13 survived. 9 new tests across `test_contracts.py`/`test_ownership.py`/`test_swing_distance.py` — ordinary suite `443/443 passed` (was 434), `ruff`/`mypy` clean. **`7/13` `KILLED_BY_WAVE6`.** **Significant honest finding:** remaining `6/13` `STILL_SURVIVED`, all independently proven `PROVABLY_EQUIVALENT`/`STRUCTURALLY_UNREACHABLE` — 3 recorded-time-floor mutants redundant given the swing-eligibility invariant (`state.recorded_time <= cursor.recorded_time`, same cursor object, source-traced); `_prepare_recompute__mutmut_23`'s assert unreachable via its only 2 legitimate callers; `_prepare_reevaluate_all_windows__mutmut_6`/`_select_eligible_swing__mutmut_22` discovered, via direct real-mutant-body inspection, to be DIFFERENT mutations than the root-cause audit described (an indexing-drift bug in this session's own diff-extraction script for dense-mutation functions) — both independently structurally unreachable. None force-tested; both originally-intended tests retained as valuable general coverage. **Governance implication NOT acted on:** active gate conservative/over-strict for these 6, never permissive — evidence only for a future re-audit, no reclassification performed. Full 24-ID accounting: 11 Wave-5 + 7 Wave-6 engineering kills (formal credit NOT claimed) + 6 pending re-audit = 24. New artifact `feature-engine-condition1-wave6-test-remediation-001.json`. `ADR_NOT_REQUIRED`; Risk `R1`. No `src/`/`tooling` change; active proposal-002/set-002/audit/DTR byte-unchanged; Condition 1 remains `FAIL — criteria` |
| Completed | `FE-EVID03-COND1-WAVE6-CLASSIFICATION-DTR-001` | Recorded the already-issued Wave-6 six-identity semantic reclassification DTR (ChatGPT Review A, distinct from Wave-6 author/executor Claude — CLEAN 0/0/0, Risk `R1`, `ADR_NOT_REQUIRED`, D1-D12 all PASS): all 6 `STILL_SURVIVED` Wave-6 identities RECLASSIFIED (3 `PROVABLY_EQUIVALENT`, 3 `STRUCTURALLY_UNREACHABLE`). Active Condition-1B accounting: `6/24 RESOLVED_BY_DELEGATED_TECHNICAL_RECLASSIFICATION`, `18/24` genuine material, all with engineering-kill evidence, formal credit NOT claimed. Then authored threshold recalibration candidate 003 from the resulting 18-ID population: candidate numerator `2214+18=2232` → `84.899201217193%`. New `CANDIDATE — NOT EFFECTIVE / AWAITING REVIEW A` documents `feature-engine-mutation-threshold-recalibration-proposal-003.md` and `feature-engine-condition1-current-material-gap-set-003.json` (18 IDs, sha256 `e4d21a0f1765f860d48d8a607c5d4e25b5b43c88f76db631cdd8528d83f73872`). Active gate (`85.127424876379%` / 24-ID set-002) NOT activated, touched, or superseded. No Review A performed on candidate-003; no PO decision requested; DTR NOT eligible for candidate-003's own activation. ADR Scope: DTR `ADR_NOT_REQUIRED`; candidate-003 `ADR_OPTIONAL`. Risk `R1` both. No `src/`/`test`/`tooling` change; Condition 1 remains `FAIL — criteria` |
| Completed | `FE-EVID03-COND1-THRESHOLD-RECAL-V3-001` | Executed the Product-Owner-authorized atomic activation of threshold recalibration proposal-003 at reviewed boundary `0ebde2bd9e532ef7c89ff0a847c84e71d107ba48` (reviewed proposal blob `2a263b9c28e02638bd69884ef0e5b12ac2090460`, reviewed set-003 blob `9065930f732b441e2b298e096c9b8f48531f7aee`). Review A: ChatGPT, **CLEAN — 0 Blocker / 0 Major / 0 Minor**, Risk `R1`, ADR Scope `ADR_OPTIONAL`, no independent cross-check required/performed. `feature-engine-mutation-threshold-recalibration-proposal-003.md` → **`APPROVED — EFFECTIVE`** (resulting blob `a3193f73eb9222ca1b87f4db78c68643dba3a266`), now sole current Condition-1 threshold authority: Condition 1A (raw score ≥ `84.899201217193%`, basis `2232/2629`) AND Condition 1B (18 exact set-003 IDs individually resolved). `feature-engine-condition1-current-material-gap-set-003.json` → **`APPROVED — EFFECTIVE`** (resulting blob `ba276a767a57c2e533e7178000b4f129d61a3e9e`), exact 18-ID membership/count/duplicates/hash all verified unchanged. Old proposal-002 (`85.127424876379%`) and old set-002 (24 IDs) now historical/superseded, both byte-unchanged. Condition 2/3 preserved independent. **Current Condition 1: `AWAITING FRESH FORMAL MEASUREMENT`** — no fresh full formal mutation measurement has run since Wave 5/6; the stale pre-remediation Evidence-005 raw score (`84.21%–84.56%`) is explicitly NOT presented as the current score. The 18/18 targeted engineering kills are engineering evidence only, NOT promoted to formal credit. Next primary WP: a full formal Condition-1 mutation measurement against the active proposal-003/set-003 gate — NOT performed by this activation. No `src/`/`test`/`tooling` change; Condition 1 remains `FAIL — criteria / formal closure not yet demonstrated` |
| Completed | `FE-EVID03-COND1-FORMAL-EVID-006-001` | Executed a fresh, full, formal Condition-1 mutation measurement against the active proposal-003/set-003 gate at executable boundary `dd05c963397bbb8c9b8bd30f6a88c913baf3f153`. Fresh disposable venv, all tool versions matched the lock exactly. Ordinary verification: `443 passed`, `5 passed` (tooling), mypy clean, ruff unchanged. Full single-worker run (`python -m tooling run --max-children 1`) reached natural completion: `2629/2629` mutants; raw `killed=2243 / survived=384 / timeout=2`. One anomaly investigated and recorded, not hidden (a first interrupted attempt, confirmed genuine mutation-induced conftest.py collection failures, not an infrastructure defect — restarted cleanly). Strict twice-independent isolated timeout triage: `p_run_sort__mutmut_82` → `CONFIRMED_TIMEOUT`; `resolve_input_contract_authority_from_repository__mutmut_109` → resolved KILLED. Final formal: `killed=2244 / confirmed_timeout=1 / survived=384`. **Formal numerator `2245` (≥ `2232`); formal percentage `85.393685812096%` (≥ `84.899201217193%`) — `Condition 1A: PASS`.** All 18 exact Set-003 identities queried by exact mutmut identity — **`18/18 KILLED`** — **`Condition 1B: PASS`.** **`FORMAL MEASUREMENT RESULT: PASS — PENDING REVIEW A VALIDATION`** (not self-issued). New additive artifact `feature-engine-mutation-step9-formal-evidence-006.json` (does NOT overwrite Evidence-005). No threshold/calibration change; proposal-003/set-003 fresh-verified byte-unchanged. No `src/`/`test`/`tooling` change; Condition 2/3 unchanged; EVID-03 remains OPEN; Feature Engine remains NOT APPROVED; LIVE remains NOT_AUTHORIZED |
| Completed | `FE-EVID03-COND1-FORMAL-006-DTR-001` | Recorded the already-issued distinct-principal ChatGPT Review A validation of evidence-006 (reviewed boundary `bb00e28056679852f2ccc6b1659e6ef026907f0c`, evidence subject blob `460cf678a2c682c26540719da78ff798ce88705d`). Verdict: **`CLEAN — 0 Blocker / 0 Major / 2 Minor`**, Risk `R1`, ADR Scope `ADR_NOT_REQUIRED`, independent cross-check NOT REQUIRED; D1-D12 all `PASS` (D8: reviewer ChatGPT distinct from Evidence-006's author/executor Claude). Disposition: `DELEGATED TECHNICAL RESOLUTION — CLEAN` — bounded application of the existing Approved gate (proposal-003/set-003) to an already-complete, objectively-passing measurement; no new semantics, no product decision, no residual-risk acceptance, no PO reservation/call-in triggered; deterministic outcome. **Governed transition: Condition 1 `FORMAL MEASUREMENT PASS — PENDING REVIEW A VALIDATION` → `PASS — REVIEW A VALIDATED`.** This is NOT Product Owner approval. Both Minors reconciled in the same transaction (deterministic bookkeeping, folded rather than split into a separate WP): (1) current-state tracking in this document and the dashboard corrected wherever it still presented Evidence-005 figures (`406` survivors, `9` unstable-timeout-triage mutants) as current — replaced with evidence-006's own current figures (`384` survivors, `0` unstable); old 42-ID set-001 no longer presented as the current Condition-1B target anywhere current-state; (2) provenance wording corrected — Evidence-006's executable boundary has `src`/`tooling`/`pyproject.toml`/`requirements-dev.lock.txt` trees byte-identical to Evidence-005's own boundary, but the `tests` tree legitimately DIFFERS (Wave-5/6 test remediation) — this document and MANIFEST already recorded this correctly; the correction applies to completion-report wording only. New additive artifact `feature-engine-condition1-formal-measurement-006-review-a-dtr-001.json`. Evidence-006 NOT modified (remains immutable, blob unchanged). No threshold/calibration change; no new measurement performed. Condition 2 (`169/170`, `TOOL_IDENTITY_DRIFT`) and Condition 3 (`SATISFIED`) preserved independent, not reopened; no Condition-2 work performed. `P3-FEATURE-QG-EVID-03` remains `OPEN`; Feature Engine remains `NOT APPROVED`; LIVE remains `NOT_AUTHORIZED`. No `src/`/`test`/`tooling`/dependency change |
| Completed | `FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001` | Authored a candidate Feature Engine Condition-2 identity-continuity resolution mechanism (branch (c) `VERIFIED_TOOL_IDENTITY_CONTINUITY`, companion to — not an edit of — `feature-engine-mutation-threshold-proposal-001.md` §4.1's existing (a)/(b) branches) for the final unresolved row `contracts.x__seal_verified_authority__mutmut_33` (`TOOL_IDENTITY_DRIFT — NO EXISTING GOVERNED RESOLUTION MECHANISM`). Fresh technical reconstruction (isolated disposable worktrees, zero test execution, exact pinned historical boundary `8d6293aca773757bc3b62cc0d3b80cba9e243954` + mutmut `3.7.0`, current boundary `e9873e17170ada23da98be9c7dd3820045d64cde`) independently re-verified all 5 required facts: (1) `_seal_verified_authority`'s semantic code path not refactored (one honest correction of a prior 6-vs-7-kwarg imprecision, substantive conclusion unchanged); (2) historical mutation site and current `mutmut_36` byte-identical; (3) current `mutmut_33` confirmed a different, unrelated mutation (negates the new ADR-043 `merge_policy` guard); (4) historical-33 → current-36 mapping confirmed unique via exhaustive 49-mutant scan; (5) drift explained by additive ordinal growth (44→49 mutants), not a behavior change. Bounded isolated current-boundary verification of `mutmut_36` (fresh workspace, two independent runs via `python -m tooling run --max-children 1`): `killed` + `killed`, no disagreement — no full 2629-mutant rerun performed. Candidate rule requires ALL of C1–C12 (exact reconstruction, unique mapping, no refactor, tool-provenance pinned to mutmut `3.7.0`, per-identity-only credit via a SEPARATE future governed decision, no raw-score denominator/numerator adjustment) — fails closed on any unresolved criterion; explicitly not a bulk table, heuristic, or ordinal-only rule. **No Condition-2 credit granted by this transaction — remains `169/170`.** Fresh Chapter 0 §4b analysis (not inherited): `ADR_SCOPE_DISPOSITION: ADR_OPTIONAL` — reasoned directly on whether the new evidentiary branch constitutes a Governance/Approval-process change (concluded: no new review role/lifecycle stage/approval-gate structure is created; reuses Testing Convention v0.16 item 8's already-established identity-pin + justification + governed-decision shape) versus the prior final-six-assessment's own deferred concern about an in-place Testing Convention edit (this document deliberately avoids that path via the companion-document pattern already used for proposal-002/003). Risk `R2` (new architecture/authority/contract semantics per `P3-REVIEW-001`, not a bounded correction). New artifacts: `feature-engine-condition2-tool-identity-continuity-proposal-001.md` (`CANDIDATE — NOT EFFECTIVE / AWAITING REVIEW A`) and `feature-engine-condition2-tool-identity-continuity-technical-evidence-001.json`. DTR NOT ELIGIBLE for this mechanism's own eventual activation or any future per-identity credit decision (ADR-045 `D10(a)`, PO-reserved). No `src/`/`test`/`tooling`/dependency change; no Condition-1/3 work; Condition 1 remains `PASS — REVIEW A VALIDATED`; Condition 3 remains `SATISFIED — REVIEW A VALIDATED`; EVID-03 remains `OPEN`; Feature Engine remains `NOT APPROVED`; LIVE remains `NOT_AUTHORIZED` |
| Completed | `FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001-CORR-001` | Bounded correction remediating Review A round-1 finding on `feature-engine-condition2-tool-identity-continuity-proposal-001.md` (principal ChatGPT, reviewed blob `14f83e9c0edfdff503df867222d68f19d31b540e`, technical-evidence blob `a4f5ceb646e39a931a532af5fd324775a38c3bc5`): `REVISION_REQUIRED — 0 Blocker / 1 Major / 0 Minor`, Risk `R2`, ADR Scope `ADR_OPTIONAL, conditional on correcting the Major`. **`MAJOR-01` — approval-routing contradiction:** §10.1 correctly found branch (c) introduces no new Governance/Approval-process, but §11 then hard-coded Product Owner approval for every future per-identity application, an undeclared new mandatory routing rule contradicting that finding. **Corrected:** §5 (`C10`) and §11 now distinguish two decisions — mechanism **activation** (remains Product-Owner-reserved; establishes new R2 evidence-policy semantics; ADR-045 R2 is never delegated) from per-identity **application** of an already-effective mechanism (now routed through the existing, unmodified ADR-045 model: Review A → Risk Classification → `R0`/`R1` + `D1`–`D12` all `PASS` → Delegated Technical Resolution eligible; `R2`/`ADR_REQUIRED`/governing-artifact reservation/explicit Product Owner call-in → Product Owner Decision) — no branch-(c)-specific carve-out. `C10`'s semantic safeguard preserved unchanged: credit remains per-historical-identity-only, individually reviewed/recorded, never blanket/heuristic/bulk. Fresh Chapter 0 §4b re-confirmed against the corrected text: `ADR_SCOPE_DISPOSITION: ADR_OPTIONAL` (strengthened, not weakened, by removing the undeclared routing rule); Risk `R2` unchanged for mechanism activation. **Technical reconstruction/evidence NOT altered** — `feature-engine-condition2-tool-identity-continuity-technical-evidence-001.json` fresh-verified byte-unchanged (blob `a4f5ceb646e39a931a532af5fd324775a38c3bc5`); C1–C9/C11/C12 untouched; historical-33 → current-36 mapping, uniqueness, current-33 collision, and both isolated `killed`+`killed` verification runs not re-litigated. **No Condition-2 credit granted.** Resulting proposal blob `799d7f805387f09c846eebfbe87298fded338f75`, status remains `CANDIDATE — NOT EFFECTIVE / AWAITING REVIEW A` (bounded re-review of this correction, not self-approved). No `src/`/`test`/`tooling`/dependency change; no Condition-1/3 work; Condition 1 remains `PASS — REVIEW A VALIDATED`; Condition 3 remains `SATISFIED — REVIEW A VALIDATED`; EVID-03 remains `OPEN`; Feature Engine remains `NOT APPROVED`; LIVE remains `NOT_AUTHORIZED` |

## 6. PO dashboard snapshot

```text
Current milestone:        M1 — Feature Engine EVID-03 Closure (ACTIVE, AT RISK)
Primary blocker:          Condition 2 -- 169/170, the final 1/170
                           TOOL_IDENTITY_DRIFT identity
                           (contracts.x__seal_verified_authority__
                           mutmut_33), no existing governed resolution
                           mechanism. Condition 1 is now `PASS --
                           REVIEW A VALIDATED` (evidence-006 +
                           FE-EVID03-COND1-FORMAL-006-DTR-001) and no
                           longer blocking -- historical figures below
                           (84.21%-84.56% / 42-ID gate) are superseded.
Current primary WP:       (none currently assigned) -- Condition-1
                           formal measurement 006 and its Review A
                           DTR (`FE-EVID03-COND1-FORMAL-EVID-006-001`,
                           `FE-EVID03-COND1-FORMAL-006-DTR-001`)
                           COMPLETE; Condition-2 tool-identity-
                           continuity candidate authored
                           (`FE-EVID03-COND2-TOOL-IDENTITY-
                           CONTINUITY-001`), CANDIDATE -- NOT
                           EFFECTIVE / AWAITING REVIEW A
ADR-045:                   v0.3, Approved / ACTIVE -- Delegated
                           Technical Resolution lane, self-contained
                           R0/R1/R2 definitions (X-MAJ-02), D8
                           distinct-principal safeguard (X-MAJ-01),
                           supersedes ADR-042 (now Superseded)
Chapter 0 / 11 / Exec:     Chapter 0 v1.5 Locked/controlling (v1.4
                           historical); Chapter 11 v2.4 Locked/
                           controlling (v2.3 historical); Global
                           Execution Rules v0.7 EFFECTIVE (v0.6
                           historical) -- all activated
                           2026-09-23T14:02+07:00
Candidate-005 status:      RESOLVED -- DELEGATED TECHNICAL RESOLUTION
                           (`FE-EVID03-COND2-CANDIDATE-005-DTR-001`).
                           NOT a Product Owner approval. Fresh
                           post-activation Review A CLEAN -- 0/0/0, R1,
                           ADR_NOT_REQUIRED, D1-D12 all PASS (D8:
                           reviewer ChatGPT distinct from author/
                           executor Claude). Both rows RECLASSIFIED_4_1_B.
Condition 2 (current):     169/170 -- 2 rows resolved by this DTR
                           (167 + 2 = 169). 1 row remains:
                           contracts.x__seal_verified_authority__mutmut_33
                           (TOOL_IDENTITY_DRIFT -- no existing governed
                           resolution mechanism at the time). A
                           candidate resolution mechanism (branch (c)
                           VERIFIED_TOOL_IDENTITY_CONTINUITY) has since
                           been authored -- see "Condition-2 continuity
                           candidate" below -- but grants no credit;
                           this row remains unresolved, count remains
                           169/170.
Condition-2 continuity     FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001
candidate:                 -- CANDIDATE -- NOT EFFECTIVE / AWAITING
                           REVIEW A (resulting blob
                           799d7f805387f09c846eebfbe87298fded338f75,
                           post-correction). Proposes one new, disjoint
                           Condition-2 resolution branch (c) for the
                           narrow case of tool-generated mutant-ID
                           ordinal drift with the underlying code path
                           unchanged -- companion to, not an edit of,
                           proposal-001's own SS4.1 (a)/(b). Fresh
                           technical reconstruction (isolated
                           worktrees, zero test execution, pinned
                           historical boundary 8d6293aca773757bc3b62cc
                           0d3b80cba9e243954 + mutmut 3.7.0) verified
                           all 5 required facts fresh, not inherited:
                           unrefactored code path (one honest 6-vs-7-
                           kwarg correction to prior evidence noted,
                           substance unchanged), byte-identical
                           historical/current-mutmut_36 mutation,
                           current mutmut_33 confirmed unrelated
                           (different guard, did not exist
                           historically), unique 33->36 mapping
                           (exhaustive 49-mutant scan), and ordinal-
                           drift causation (44->49 mutants). Bounded
                           isolated verification of mutmut_36 (2
                           independent fresh-workspace runs): killed +
                           killed. Mechanism requires ALL of C1-C12
                           (exact reconstruction, unique mapping, no
                           refactor, tool provenance pinned to mutmut
                           3.7.0 only, per-identity-only credit via a
                           SEPARATE future governed decision, no raw-
                           score adjustment) -- fails closed, no bulk
                           table/heuristic/ordinal-only rule. New
                           artifacts: feature-engine-condition2-tool-
                           identity-continuity-proposal-001.md and
                           feature-engine-condition2-tool-identity-
                           continuity-technical-evidence-001.json. NO
                           Condition-2 credit granted -- 169/170
                           unchanged. No src/test/tooling/dependency
                           change.
Continuity candidate       Review A round 1 (ChatGPT, reviewed blob
correction (CORR-001):     14f83e9c0edfdff503df867222d68f19d31b540e):
                           REVISION_REQUIRED -- 0 Blocker / 1 Major / 0
                           Minor, Risk R2, ADR_OPTIONAL conditional on
                           correcting the Major. MAJOR-01 -- approval-
                           routing contradiction: SS10.1 correctly
                           found branch (c) introduces no new
                           Governance/Approval-process, but SS11 then
                           hard-coded Product Owner approval for every
                           future per-identity application -- an
                           undeclared new mandatory routing rule.
                           CORRECTED: SS5 (C10) and SS11 now distinguish
                           mechanism ACTIVATION (remains Product-Owner-
                           reserved; R2 never delegated under ADR-045)
                           from per-identity APPLICATION of an already-
                           effective mechanism (now routed through the
                           existing, unmodified ADR-045 model: Review A
                           -> Risk Classification -> R0/R1 + D1-D12 all
                           PASS -> Delegated Technical Resolution
                           eligible; R2/ADR_REQUIRED/governing-artifact
                           reservation/explicit Product Owner call-in
                           -> Product Owner Decision) -- no branch-(c)-
                           specific carve-out. C10's semantic safeguard
                           unchanged: per-historical-identity-only
                           credit, individually reviewed/recorded,
                           never blanket/heuristic/bulk. Fresh Chapter
                           0 SS4b re-confirmed against the corrected
                           text: ADR_SCOPE_DISPOSITION: ADR_OPTIONAL
                           (strengthened by removing the undeclared
                           routing rule). Risk R2 unchanged for
                           mechanism activation. Technical
                           reconstruction/evidence NOT altered --
                           feature-engine-condition2-tool-identity-
                           continuity-technical-evidence-001.json
                           fresh-verified byte-unchanged (blob
                           a4f5ceb646e39a931a532af5fd324775a38c3bc5).
                           NO Condition-2 credit granted. Status
                           remains CANDIDATE -- NOT EFFECTIVE / AWAITING
                           REVIEW A (bounded re-review of this
                           correction, not self-approved). No src/test/
                           tooling/dependency change.
Last Review A:             CLEAN -- 0 Blocker / 0 Major / 0 Minor, Risk
                           R1 (on Candidate-005, boundary
                           1e4078c3...). Reviewer ChatGPT, AI Technical
                           Architect, distinct from Candidate-005's
                           author/executor principal Claude (D8).
                           Reason deferred (no PO decision here): D1-D12
                           satisfied -> closes as Delegated Technical
                           Resolution, not a Product Owner Decision.
Condition-1 assessment:    Post-Evidence-005 406-survivor classification
                           (EVIDENCE/DIAGNOSTIC only, boundary
                           2ca64a46...): GENUINE_TEST_GAP=40,
                           LOW_MATERIALITY_MESSAGE_TEXT=344,
                           PROVABLY_EQUIVALENT=16,
                           STRUCTURALLY_UNREACHABLE=4, UNCLEAR=2.
                           Feasibility: Case C -- CURRENT TEST-ONLY PATH
                           APPEARS INSUFFICIENT (best-case combined
                           numerator 2265, still 23 short of required
                           2288). Does not change Condition 1's formal
                           result or the approved threshold. Full
                           record: feature-engine-condition1-post-e005-
                           survivor-assessment-001.json.
Condition-1 recalibration: **ACTIVATED (2026-09-23T20:01+07:00).**
                           Final Review A CLEAN -- 0 Blocker / 0 Major /
                           1 Minor, R1, ADR_OPTIONAL; R1 default no
                           cross-check, none performed. Sole Minor:
                           authorized non-semantic provenance cleanup
                           (42-ID artifact's two acquire_and_activate
                           __mutmut_21/_23 source fields corrected from
                           an inaccurate "post-E005 assessment
                           (GENUINE_TEST_GAP)" to "Review-A MAJOR-02
                           correction: post-E005 assessment UNCLEAR ->
                           GENUINE_TEST_GAP" -- set/count(42)/
                           duplicates(0)/order/hash all verified
                           unchanged; artifact blob 6360c8c1... ->
                           49c30b439e...), folded into this atomic
                           activation per the PO decision.
                           feature-engine-mutation-threshold-
                           recalibration-proposal-001.md CANDIDATE ->
                           APPROVED -- EFFECTIVE (resulting blob
                           12040044578d...) and is now the SOLE current
                           Feature Engine Condition-1 threshold
                           authority: Condition 1A (raw score >=
                           85.812095853937%, required numerator
                           2256/2629) AND Condition 1B (all 42 exact
                           current-material identities individually
                           resolved -- unrelated kills never
                           substitute, no blanket reclassification, no
                           score-offset mechanism).
                           feature-engine-mutation-threshold-
                           proposal-001.md (old 87.001959503592%)
                           becomes historical/superseded, byte-
                           unchanged at f4a3ca0c37... MANIFEST carries
                           one canonical current-threshold pointer. No
                           fresh mutation measurement performed by this
                           activation.
Wave-5 test remediation:   COMPLETE. 20 new tests across 7 files
                           (test_identity.py new); ordinary suite
                           434/434 passed (was 414); ruff/mypy clean.
                           Bounded targeted mutation verification (25
                           named IDs only): 12/25 targeted kills
                           verified (Cluster A wrong-type 0/9, B
                           malformed-field 4/5, C zip-strict 3/6, D
                           quote-parsing 4/4, E deterministic-ID 1/1).
                           13 survivors honestly reported: Cluster A
                           (9) message-text-only (type(X)->type(None),
                           no crash, corrects a prior inherited
                           assumption); 4 more STRUCTURALLY_UNREACHABLE
                           given an earlier unconditional guard already
                           in the same function -- none gamed.
                           IMPLEMENTATION EVIDENCE ONLY -- formal
                           Condition 1B credit NOT claimed. New
                           artifact: feature-engine-condition1-wave5-
                           test-remediation-001.json; exact 17-ID
                           Wave-6 complement persisted. ADR_NOT_REQUIRED;
                           Risk R1. No src/tooling change.
Condition-1 material-gap    Consolidated root-cause audit of all 42
audit:                     activated Condition-1B identities
                           (triggered by Wave-5's own 13 honestly-
                           reported false positives). Fresh-re-
                           extracted all 42 diffs; independently re-
                           classified every identity from first
                           principles, never inheriting prior labels.
                           17-ID Wave-6 complement analyzed for the
                           first time (deep reachability/control-flow
                           tracing, no test implementation): 13
                           GENUINE_TEST_GAP, 2 STRUCTURALLY_UNREACHABLE
                           (EventRecordRef uniqueness argument), 2
                           UNCLEAR/DISPUTED (acquire_and_activate
                           mutmut_21/_23 -- this audit's stricter
                           re-check cannot confirm Task C's MAJOR-02
                           concurrent-observability argument; no
                           documented thread-safety contract, no lock;
                           deferred to a separate, distinct-principal
                           Review A, NOT resolved here). All 12 Wave-5-
                           killed identities re-audited for genuine
                           contractual materiality: 11 confirmed, 1
                           reclassified (identity.x_deterministic_id__
                           mutmut_3's golden-digest-pin kill tests an
                           implementation detail, not a documented
                           contract per identity.py's own docstring).
                           Final: GENUINE_TEST_GAP 24, LOW_MATERIALITY
                           _MESSAGE_TEXT 9, LOW_MATERIALITY_
                           IMPLEMENTATION_DETAIL 1, STRUCTURALLY_
                           UNREACHABLE 6, UNCLEAR 2. Candidate math
                           (informational, same 2214/2629 boundary):
                           M=24 -> 85.12742487637885%; M=26 (incl.
                           disputed) -> 85.20349942944085%. NEITHER
                           ACTIVATED -- active threshold
                           85.812095853937% / 42-ID gate remain fully
                           controlling, now noted conservative/over-
                           strict relative to this audit, not
                           permissive. No threshold change, no DTR
                           issued (deferred to a separate distinct-
                           principal Review A), activated artifacts
                           byte-unchanged. New artifact: feature-
                           engine-condition1-material-gap-root-cause-
                           audit-001.json. WAVE 6 IMPLEMENTATION
                           PAUSED PENDING MATERIAL-SET AUDIT.
                           ADR_NOT_REQUIRED; Risk R1.
Condition-1 material-set   FE-EVID03-COND1-MATERIAL-SET-DTR-001 --
DTR:                       DELEGATED TECHNICAL RESOLUTION -- CLEAN.
                           Review A: ChatGPT (distinct principal from
                           audit author/executor Claude, D8 PASS).
                           Verdict: CLEAN -- 0 Blocker / 0 Major / 1
                           Minor, Risk R1, ADR_NOT_REQUIRED. D1-D12 all
                           PASS. Minor (non-semantic wording, corrected
                           here only -- audit artifact immutable, NOT
                           rewritten): D10(a) reserves only the numeric
                           threshold decision to PO, not individually-
                           governed exact-ID semantic reclassification
                           already permitted by the current Condition-
                           1B mechanism. Governed disposition: the
                           audit's 18 non-material/disputed identities
                           RECLASSIFIED (9 LOW_MATERIALITY_MESSAGE_TEXT,
                           6 STRUCTURALLY_UNREACHABLE, 1 LOW_MATERIALITY
                           _IMPLEMENTATION_DETAIL, 2 NON_MATERIAL_
                           TRANSIENT_IN_FLIGHT_STATE --
                           acquire_and_activate mutmut_21/_23 now
                           confirmed non-material: AuthoritativeSubject
                           Owner establishes no concurrent-observation
                           contract for an in-flight owner, neither
                           mutated field affects the eventual ACTIVE/
                           REVOKED handle or any authoritative outcome).
                           Final: GENUINE_TEST_GAP 24, NON_MATERIAL 18,
                           UNCLEAR 0. Condition 1B accounting: 18/42
                           RESOLVED_BY_DELEGATED_TECHNICAL_
                           RECLASSIFICATION, 24/42 still require
                           resolution (11 with Wave-5 targeted-kill
                           evidence, formal credit NOT claimed; 13
                           unremediated). Candidate math unchanged
                           (M=24 -> 85.12742487637885%), still NOT
                           ACTIVATED -- active threshold/42-ID gate
                           remain fully controlling. No threshold
                           change, no formal kill credit, activated
                           artifacts byte-unchanged. New artifact:
                           feature-engine-condition1-material-gap-dtr-
                           001.json. Wave 6 remains PAUSED. ADR_NOT_
                           REQUIRED; Risk R1.
Formal measurement 006:   FE-EVID03-COND1-FORMAL-EVID-006-001 --
                           MEASUREMENT COMPLETE. Fresh full formal
                           measurement against active proposal-003/
                           set-003, executable boundary
                           dd05c963397bbb8c9b8bd30f6a88c913baf3f153
                           (src/tooling/dependency trees byte-
                           identical to Evidence-005; only tests_tree
                           differs, legitimately, due to Wave-5/6 test
                           remediation). Fresh disposable venv, all
                           tool versions match lock exactly. Ordinary
                           verification: 443 passed, 5 passed
                           (tooling), mypy clean, ruff unchanged (2
                           pre-existing findings). Full single-worker
                           run (python -m tooling run --max-children
                           1) reached natural completion: 2629/2629
                           mutants. Raw: killed=2243, survived=384,
                           timeout=2, sum 2629. One anomaly
                           investigated and recorded, not hidden: a
                           first attempt was interrupted on repeated
                           BadTestExecutionCommandsException
                           tracebacks; confirmed genuine mutation-
                           induced conftest.py import-time collection
                           failures (documented shim behavior,
                           P3-PY-MUT-BASELINE-B-MAJ-01), not an
                           infrastructure defect -- workspace cleaned,
                           run restarted cleanly. Strict twice-
                           independent isolated timeout triage:
                           p_run_sort__mutmut_82 -> timeout+timeout ->
                           CONFIRMED_TIMEOUT (consistent with
                           Evidence-005's own prior confirmation);
                           resolve_input_contract_authority_from_
                           repository__mutmut_109 -> killed+killed ->
                           resolved KILLED. Zero unstable. Final
                           formal: killed=2244, confirmed_timeout=1,
                           survived=384, sum 2629. Formal numerator
                           2245 (>= required 2232); formal percentage
                           85.393685812096% (>= required
                           84.899201217193%) -- CONDITION 1A: PASS.
                           All 18 exact Set-003 identities queried by
                           exact mutmut identity from the persisted
                           result store -- 18/18 KILLED -- CONDITION
                           1B: PASS. New additive artifact: feature-
                           engine-mutation-step9-formal-evidence-
                           006.json (does NOT overwrite Evidence-005).
                           No threshold/calibration change; proposal-
                           003/set-003 fresh-verified byte-unchanged.
                           No source/test/tooling change.
Review A / DTR 006:       FE-EVID03-COND1-FORMAL-006-DTR-001 --
                           DELEGATED TECHNICAL RESOLUTION -- CLEAN.
                           Records the already-issued distinct-
                           principal Review A of evidence-006
                           (reviewed boundary
                           bb00e28056679852f2ccc6b1659e6ef026907f0c,
                           evidence blob
                           460cf678a2c682c26540719da78ff798ce88705d).
                           Principal: ChatGPT, AI Technical Architect,
                           distinct from evidence-006's author/
                           executor Claude (D8 PASS). Verdict: CLEAN --
                           0 Blocker / 0 Major / 2 Minor, Risk R1, ADR
                           Scope ADR_NOT_REQUIRED, independent cross-
                           check NOT REQUIRED. D1-D12 all PASS: bounded
                           application of the existing Approved gate
                           (proposal-003/set-003) to an already-
                           complete, objectively-passing measurement;
                           no new semantics; no product decision; no
                           residual-risk acceptance; evidence/boundary
                           fresh-verified; no PO reservation/call-in;
                           deterministic outcome; unambiguous schema/
                           recording. GOVERNED TRANSITION: Condition 1
                           FORMAL MEASUREMENT PASS -- PENDING REVIEW A
                           VALIDATION -> PASS -- REVIEW A VALIDATED.
                           THIS IS NOT PRODUCT OWNER APPROVAL. Both
                           Minors reconciled in this same transaction
                           (deterministic bookkeeping, folded rather
                           than split into a new WP): (1) current-
                           state tracking corrected wherever this
                           document/dashboard still presented
                           Evidence-005 figures (406 survivors, 9
                           unstable-timeout-triage mutants) as current
                           -- replaced with evidence-006's own current
                           figures (384 survivors, 0 unstable); old
                           42-ID set-001 no longer presented as the
                           current Condition-1B target anywhere
                           current-state; (2) provenance wording --
                           tests tree legitimately DIFFERS from
                           Evidence-005 (Wave-5/6), only src/tooling/
                           dependency trees are byte-identical; this
                           document/MANIFEST already recorded this
                           correctly, correction applies to
                           completion-report wording going forward.
                           New additive artifact: feature-engine-
                           condition1-formal-measurement-006-review-a-
                           dtr-001.json. Evidence-006 NOT modified,
                           blob unchanged. No new measurement
                           performed; no threshold/calibration change;
                           no Condition-2 work performed.
Primary blocker (current): Condition 2 -- 169/170, the final 1/170
                           TOOL_IDENTITY_DRIFT identity
                           (contracts.x__seal_verified_authority__
                           mutmut_33, no existing governed resolution
                           mechanism). Condition 1 is fully resolved
                           (PASS -- REVIEW A VALIDATED) and no longer
                           blocking. Condition 3 remains SATISFIED --
                           REVIEW A VALIDATED.
PO decision required now: NO
                           (Condition 1 is now PASS -- REVIEW A
                           VALIDATED via a Delegated Technical
                           Resolution, not a Product Owner approval --
                           D1-D12 satisfied a bounded, deterministic
                           application of the existing Approved gate.
                           Condition 2 (169/170) independently
                           continues to block. A CANDIDATE resolution
                           mechanism for TOOL_IDENTITY_DRIFT has been
                           authored (FE-EVID03-COND2-TOOL-IDENTITY-
                           CONTINUITY-001, ADR_OPTIONAL, Risk R2) but
                           is NOT yet reviewed and grants NO credit --
                           the row remains unresolved, count remains
                           169/170. Condition 3 (SATISFIED) preserved
                           unchanged. EVID-03 remains OPEN; Feature
                           Engine remains NOT APPROVED; Phase-3 module
                           approval remains NOT GRANTED; LIVE remains
                           NOT_AUTHORIZED. Next governed decision
                           point: a bounded, distinct-principal ChatGPT
                           Review A re-review of the corrected tool-
                           identity-continuity candidate (MAJOR-01
                           remediated) -- not initiated here. This
                           executor does not self-issue that Review A,
                           and a separate, subsequent governed decision
                           would still be
                           required to apply the mechanism to
                           contracts.x__seal_verified_authority__
                           mutmut_33 specifically, even after a CLEAN
                           Review A.)
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
