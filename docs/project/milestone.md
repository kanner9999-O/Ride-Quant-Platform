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
| M1 | Feature Engine — P3-FEATURE-QG-EVID-03 Closure | `DONE` | M0 | No |
| M2 | Feature Engine — Remaining Quality-Gate Closure (parallel evidence lane, NOT the primary-path blocker) | `BLOCKED` | M1 | No |
| M3 | Context Projection / `context-aggregator` | `ACTIVE` | upstream executable/contract boundary (M0; NOT M2) | No |
| M4 | Strategy → Decision → Risk Gateway → Execution downstream Phase-3 chain | `QUEUED` | M3 | No |

### M0 — Lean Ride Operating Model v1.1 Adoption

- **State:** `DONE`
- **Acceptance condition:** Lean Ride Operating Model v1.1 mechanically
  recorded `Active — ADOPTED`.
- **Closing boundary:** `063bc0771f25b59858df2e3906e00c7a238e0d31`
- **PO action required:** No.

### M1 — Feature Engine — P3-FEATURE-QG-EVID-03 Closure

See §4 for full detail.

### M2 — Feature Engine — Remaining Quality-Gate Closure

- **State:** `BLOCKED` (fresh-derived and reconciled,
  `FE-EVID03-COND2-M2-SCOPE-001`; was `ACTIVE`)
- **Depends on:** M1 (`DONE`)
- **Acceptance condition (derived, not invented):** all remaining
  current Feature Engine Chapter-13 blocking findings closed —
  `EVID-04 = CLOSED — PASS`, `EVID-06 = CLOSED — PASS`,
  `EVID-08 = CLOSED — PASS`. `EVID-03`, `EVID-05`, and `EVID-07` are
  already complete (`CLOSED — PASS` / `CLOSED — PASS — REVIEW A
  VALIDATED`) and are NOT new M2 work.
- **Blocked reason:** `EVID-04`, the remaining (platform) half of
  `EVID-06`, and `EVID-08` each depend on downstream Phase-3
  capabilities (Decision Engine, Risk Gateway, Execution Engine) that
  do not yet exist anywhere in the repository (fresh-verified: no
  implementation directory in `python/`/`go/`; `module-registry.yaml`'s
  corresponding entries all carry `status: candidate`) — per Chapter 14
  §14.2's own build sequence, `Feature Engine → Context Projection →
  Strategy → Decision → Risk Gateway → Execution`, none can be
  honestly closed by any Feature-Engine-local coding/test work today.
  No fake Feature-local substitute is authorized. Full derivation:
  `docs/governance/quality-gate/feature-engine-m2-scope-derivation-001.json`.
- **Relationship to the primary implementation path (critical-path
  correction, `RIDE-CRITICAL-PATH-CORRECTION-001`, this transaction):**
  M2 is a **parallel evidence lane**, no longer treated as the sole
  blocker of the Phase-3 primary implementation path. It is expected to
  become progressively unblockable as downstream capabilities become
  real (`EVID-04` ← Decision path; `EVID-06` remaining half ← Risk
  Gateway path; `EVID-08` ← full Strategy/Decision/Risk/Execution
  path) — each finding still requires its own separate, governed
  evidence evaluation; M2 does NOT auto-close when downstream code
  merely appears. M3/M4 do not depend on M2 reaching `PASS`.
- **PO action required:** No.

### M3 — Context Projection / `context-aggregator`

- **State:** `ACTIVE` (redefined this transaction,
  `RIDE-CRITICAL-PATH-CORRECTION-001`; supersedes the prior
  `Feature Engine — Module Approval` project-tracking entry — see §3.1
  below for why)
- **Depends on:** the existing upstream executable/contract boundary
  (`market-data-ingestion`, `structure-engine`, `raw-regime-engine`,
  `feature-engine` — all already implemented) required by
  Chapter-14/module-registry ordering. **Explicitly NOT dependent on M2
  reaching `PASS`.**
- **Acceptance condition:** NOT invented by this transaction. Scope /
  implementation readiness to be fresh-derived in the next
  separately-scoped WP. See §4a for current derived facts
  (module-registry entry, implementation-existence verification).
- **Implementation status:** `NOT STARTED`. Implementation MUST NOT
  begin in this transaction.
- **PO action required:** No.

### §3.1 — Why M3/M4 were redefined (critical-path correction)

**Prior project-tracking definition (superseded, not a Constitution
defect):** M3 was previously tracked as `Feature Engine — Module
Approval`, citing Chapter 12 §12.2, with M4 depending on it. Fresh
verification (`RIDE-CRITICAL-PATH-CORRECTION-001`, Review A CLEAN —
0/0/0, Risk `R1`, ADR Scope `ADR_NOT_REQUIRED`) found this was a
**project-tracking / orchestration modeling error**, not a defect in
Chapter 12 or Chapter 13 (neither chapter changed; neither is
reinterpreted to weaken Quality-Gate requirements):

- Chapter 12 §12.2 defines only a **Phase Approval Gate** —
  prerequisite aggregation at the Product Owner **phase** decision
  boundary (quality gates are one input item among several, §12.2(5)).
  It does not define a separate, standalone Feature Engine (or any
  other single-module) Approval Gate.
- Chapter 13 §13.1 is explicit: `Quality Gate pass ≠ Product Owner
  approval`; `Quality Gate → sinh eligibility evidence`; `Approval
  Gate → consume evidence đó`. Quality Gate never approves, locks, or
  decides phase transition.
- `docs/governance/phases/phase-3-rules.md` §11's own gate-path model
  confirms: `Phase 3 module/artifact implementation → Quality Gate
  theo Tier cho từng module/artifact → Phase-wide BCC → Phase-level
  Gate review(s) → Product Owner Phase 3 Approval Gate decision` — a
  single phase-level Approval Gate at the end, not a per-module gate
  inserted between each adjacent Chapter-14 node.
- No other controlling authority (Lean Ride Operating Model v1.1,
  module-registry.yaml, ADR-045) defines a separate Feature Engine
  module Approval Gate either. The one generic phrase found —
  `docs/constitution/00-governance.md`'s "Phase/Module Approval Gate
  decisions" (a Product-Owner-reservation category) — reserves such a
  decision to the Product Owner IF a governing authority ever defines
  one; it does not itself define or create one.

**Corrected model:** Feature Engine's remaining Quality-Gate evidence
(M2) may remain `BLOCKED` while bounded Phase-3 development continues
downstream per Chapter 14 §14.2's own dependency order. The false
operational dependency `M2 → Feature Engine Module Approval →
downstream unlock` is removed. M2 is not weakened, closed, waived, or
reinterpreted — its own acceptance boundary (`EVID-04`/`EVID-06`/
`EVID-08` all `CLOSED — PASS`) is unchanged.

### M4 — Strategy → Decision → Risk Gateway → Execution downstream Phase-3 chain

- **State:** `QUEUED`
- **Depends on:** M3
- **Acceptance condition:** not yet detailed — no speculative downstream
  implementation work is hard-coded here. Exact module/WP decomposition
  remains to be fresh-derived as each roadmap boundary (Strategy,
  Decision, Risk Gateway, Execution — Chapter 14 §14.2) is reached. This
  milestone is NOT implemented or fully designed by this transaction.
- **PO action required:** No.

## 4. Feature Engine — `P3-FEATURE-QG-EVID-03` Closure detail (M1, DONE — historical)

**Feature Engine — `P3-FEATURE-QG-EVID-03` Closure** (`DONE`, depends on M0)

| Item | Current state |
|---|---|
| Overall | `DONE` — `P3-FEATURE-QG-EVID-03` closed via Delegated Technical Resolution (`FE-EVID03-CLOSURE-001-DTR-001`), not a Product Owner approval. M2 (Feature Engine — Remaining Quality-Gate Closure) is `BLOCKED` — its scope is derived (`EVID-04`/`EVID-06` remaining half/`EVID-08`, all `BLOCKED_BY_EXTERNAL_DEPENDENCY` on unimplemented downstream Phase-3 modules), not invented; no Feature-Engine-local remediation path exists today. M2 is now a **parallel evidence lane**, not the primary-path blocker (critical-path correction, `RIDE-CRITICAL-PATH-CORRECTION-001`) — see §4a for M3 (Context Projection / `context-aggregator`), the current primary-path milestone. |
| Condition 1 | `PASS — REVIEW A VALIDATED` — gated by the ACTIVATED recalibrated threshold-v3: Condition 1A (raw score ≥ `84.899201217193%`, MEASURED `85.393685812096%`, PASS) AND Condition 1B (18 pinned current-material identities individually resolved, MEASURED `18/18 KILLED`, PASS) — evidence-006, formally validated by distinct-principal ChatGPT Review A, recorded via `FE-EVID03-COND1-FORMAL-006-DTR-001` (Delegated Technical Resolution, NOT a Product Owner approval). Condition 1 is no longer the primary blocker. |
| Condition 1 — unstable cases (current, evidence-006) | `0` — historical Evidence-005 figure of `9` is superseded at the current measurement boundary, not reopened |
| Condition 1 — current survivor count (evidence-006) | `384` — historical Evidence-005 figure of `406` is superseded at the current measurement boundary |
| Condition 1 — current-material companion gate | `18/18 formally resolved — PASS — REVIEW A VALIDATED` — `docs/governance/mutation-baseline-evidence/feature-engine-condition1-current-material-gap-set-003.json` (APPROVED — EFFECTIVE, sole current Condition-1B authority; all 18 measured KILLED by exact identity in `feature-engine-mutation-step9-formal-evidence-006.json`; old 42-ID set-001/24-ID set-002 and their 18+6 delegated-reclassifications are historical, `feature-engine-condition1-material-gap-dtr-001.json` + `feature-engine-condition1-wave6-classification-dtr-001.json`) |
| Condition 2 | `170/170 — SATISFIED`. The final identity, `contracts.x__seal_verified_authority__mutmut_33`, is resolved via branch (c) `VERIFIED_TOOL_IDENTITY_CONTINUITY` (mapped uniquely to current successor `feature_engine.contracts.x__seal_verified_authority__mutmut_36`, KILLED), recorded as `DELEGATED TECHNICAL RESOLUTION — CLEAN` under ADR-045 (`FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001-APPLY-001`, `FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001-APPLY-DTR-001`) — not a Product Owner approval. |
| Condition 3 | `SATISFIED — REVIEW A VALIDATED` (**DONE — not reopened by this WP**) |
| `P3-FEATURE-QG-EVID-03` | `CLOSED — PASS — REVIEW A VALIDATED` — closed via `FE-EVID03-CLOSURE-001` (`DELEGATED TECHNICAL RESOLUTION — CLEAN`, Risk `R1`, ADR Scope `ADR_NOT_REQUIRED`), aggregating the three already-governed Condition 1/2/3 states above. NOT a Product Owner approval; NOT Feature Engine approval; NOT Phase-3 approval; NOT LIVE authorization — each remains a separate, not-yet-performed governed decision. |
| Feature Engine Chapter-13 Quality Gate | not fully `PASS` — M2 remains `BLOCKED` on `EVID-04`/`EVID-06`/`EVID-08` (see M3/M4 correction, §3). There is no separate standalone Feature Engine Module Approval Gate under current Chapter 12/13 authority — this row states Quality-Gate status only, not an approval lifecycle state. |
| Phase-3 Approval Gate | not reached / not granted — a single phase-level decision (Chapter 12 §12.2), reached after Phase-3 module/artifact implementation and Quality Gate evidence accumulate; not a per-module gate. |
| LIVE | `NOT_AUTHORIZED` |

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

## 4a. Current active primary-path milestone detail — M3

**Context Projection / `context-aggregator`** (`ACTIVE`, depends on the
existing upstream executable/contract boundary — NOT on M2 reaching
`PASS`)

This section is new as of the critical-path correction transaction
(`RIDE-CRITICAL-PATH-CORRECTION-001`) that redefined M3/M4 (§3). It
does not grant, imply, or pre-authorize any implementation,
Quality-Gate result, or approval — see §3's `### M3`/`### M4` entries
for the full derivation and explicit non-claims.

| Item | Current state |
|---|---|
| Purpose | Next legitimate primary-path Phase-3 module boundary after Feature Engine, per Chapter 14 §14.2's canonical dependency sequence (`Data Layer → Structure Engine & Raw Regime Engine → Feature Engine → Context Projection → Strategy → Decision → Risk Gateway → Execution`). |
| module-registry.yaml entry | `context-aggregator` — `module_type: projection`, `depends_on: [market-data-ingestion, structure-engine, raw-regime-engine, feature-engine]`, `status: candidate` (architecture-declared only). |
| Implementation existence | `python/context-aggregator/` now exists (`CONTEXT-AGGREGATOR-CORE-001`) — deterministic aggregation core only (Sections A-K of that WP's spec). |
| Implementation status | `DETERMINISTIC CORE IMPLEMENTED — REVIEW A VALIDATED — CLEAN` (`CONTEXT-CORE-REVIEW-A-DTR-001`, `0 Blocker / 0 Major / 0 Minor`) — no runtime/event-log integration, stream-frontier capture, Input Contract authority resolution, output Event Contract publication, Strategy/Decision integration, or Quality-Gate closure. See `python/context-aggregator/README.md`'s "What this slice does not implement" for the exact preserved gap list. |
| Next architecture prerequisite | `docs/adr/ADR-046.md` (`Context Computation Cursor and Temporal Eligible-Upstream Supersession`) — `v0.3`, `status: Draft`, `NOT APPROVED`, Risk `R2`, ADR Scope `ADR_REQUIRED`. Round-1 Review A on v0.1 returned `REVISION_REQUIRED — 0/4/2` (remediated by `ADR-046-CORR-001`); round-2 Review A on v0.2 returned `REVISION_REQUIRED — 0/3/0` (remediated by `ADR-046-CORR-002`) — all nine findings addressed/remediated, none self-closed, awaiting fresh Review A re-review. Establishes a durable `computation_cursor` (canonical Chapter 8 §8.5 Replay Cursor) for `MarketContextSnapshot`/`MarketContextFactInvalidated`, its `Cursor → Context projection record` anti-look-ahead relation, a bounded temporal eligible-winner-supersession invalidation rule (role-resolution-delta framing, per-role cause-ref set), and explicit invalidation/replacement-cursor Case A/B rules (Case B: fresh non-counterfactual re-evaluation, 9 sub-rules). Runtime/Input Contract/publishing layer work is blocked pending this decision's current-model review chain: fresh Review A → Product Owner decision (Risk fixed `R2`; an optional advisory cross-check may be Product-Owner-selected, never an approval prerequisite). |
| Acceptance criteria | NOT invented by this transaction — the next Context WP must fresh-derive the next legitimate bounded layer after review of this implementation result and of `ADR-046`. |
| Dependency on M2 | **None.** M3 does not depend on M2 reaching `PASS`. Its dependency is the existing upstream executable/contract boundary (`market-data-ingestion`, `structure-engine`, `raw-regime-engine`, `feature-engine` — all already implemented) required by Chapter-14/module-registry ordering, per `phase-3-rules.md` §11's own gate-path model (Quality Gate evidence accumulates per-module/artifact; the Product Owner Approval Gate decision is phase-level, reached once, not a per-module gate between adjacent Chapter-14 nodes). |
| Feature Engine Chapter-13 Quality Gate | not fully `PASS` (M2 `BLOCKED` on `EVID-04`/`EVID-06`/`EVID-08`) — unaffected by, and not a blocker of, M3's primary-path status. |
| Phase-3 Approval Gate | not reached / not granted. |
| Feature Engine approval / module approval | No standalone gate of this kind exists under current Chapter 12/13 authority (§3's `### M3` derivation) — this row is retained only to make explicit that none is claimed, granted, or implied. |
| LIVE | `NOT_AUTHORIZED` |
| PO action required now | No. |

## 5. Work Package lanes

| Lane | Item | Status |
|---|---|---|
| Primary | *(none currently assigned)* | `FE-EVID03-COND1-WAVE5-001`, `FE-EVID03-COND1-AUDIT-001`, `FE-EVID03-COND1-MATERIAL-SET-DTR-001`, `FE-EVID03-COND1-THRESHOLD-RECAL-V2-001`, `FE-EVID03-COND1-WAVE6-001`, `FE-EVID03-COND1-WAVE6-CLASSIFICATION-DTR-001`, `FE-EVID03-COND1-THRESHOLD-RECAL-V3-001`, `FE-EVID03-COND1-FORMAL-EVID-006-001`, `FE-EVID03-COND1-FORMAL-006-DTR-001`, `FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001`, `FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001-CORR-001`, `FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001-ACTIVATION-001`, `FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001-APPLY-001`, `FE-EVID03-CLOSURE-001`, `FE-EVID03-COND2-M2-SCOPE-001`, `RIDE-CRITICAL-PATH-CORRECTION-001` (project-tracking/orchestration correction: no standalone Feature Engine Module Approval Gate exists under current Chapter 12/13 authority; M3 redefined `Context Projection / context-aggregator` (`ACTIVE`), M4 redefined `Strategy → Decision → Risk Gateway → Execution` (`QUEUED`), neither depends on M2 reaching `PASS`; M2 preserved unchanged as a parallel `BLOCKED` evidence lane), `CONTEXT-AGGREGATOR-CORE-001` (first bounded Phase-3 implementation slice: the deterministic Context aggregation core, `python/context-aggregator/` — two-phase Eligible Upstream Fact selection, seven-role cardinality, canonical normalization, verbatim Context-values assembly; explicit visibility boundary preserved; 54 tests/ruff/mypy strict clean; Input Contract/Event Contract/publishing/Strategy work all deliberately not implemented; not self-approved), and `CONTEXT-AGGREGATOR-CORE-001-CORR-001` (bounded correction remediating ChatGPT Review A's 3 Majors — `CONTEXT-CORE-A-MAJ-01` computation-point Candle binding via new required `target_computation_point_ref`; `CONTEXT-CORE-A-MAJ-02` superseded Regime/Feature resurrection prevention via full-lineage-graph resolution before cutoff/invalidation filtering; `CONTEXT-CORE-A-MAJ-03` Structure `effective_time` changed from scalar `datetime` to the real `[window_start, window_end)` interval — 69 tests/ruff/mypy strict clean; not self-closed, awaiting fresh Review A re-review), and `CONTEXT-AGGREGATOR-CORE-001-CORR-002` (narrowly-scoped correction closing the `CONTEXT-CORE-A-MAJ-02` residual only — cross-window `supersedes_ref` edges now fail closed via `MalformedLineageError` when both successor and target are present in the identity-matched candidate set and their windows differ; `CONTEXT-CORE-A-MAJ-01`/`-03` untouched, confirmed byte-unchanged; 76 tests/ruff/mypy strict clean; not self-closed), and `CONTEXT-CORE-REVIEW-A-DTR-001` + `ADR-046-AUTHOR-001` (Part A: persisted the already-issued final ChatGPT Review A closure of the Context deterministic core — `CLEAN — 0/0/0`, R1, `ADR_NOT_REQUIRED`, `DELEGATED TECHNICAL RESOLUTION — CLEAN`; `CONTEXT-CORE-A-MAJ-01`/`-02`/`-03` all `CLOSED`; Context deterministic core = `REVIEW A VALIDATED — CLEAN`. Part B: authored `docs/adr/ADR-046.md` v0.1 `Draft` candidate only — `Context Computation Cursor and Temporal Eligible-Upstream Supersession`, Risk `R2`, ADR Scope `ADR_REQUIRED`, NOT approved, NOT self-reviewed), and `ADR-046-CORR-001` (bounded correction of `ADR-046` against fresh ChatGPT Review A of v0.1 — `REVISION_REQUIRED — 0 Blocker / 4 Major / 2 Minor`, Risk `R2`; core decision direction preserved unchanged; `MAJ-01` false reviewer-provenance corrected (`reviewers: [ChatGPT]` only, `v0.1 → v0.2`); `MAJ-02` authority-neutral framing added (Chapter 7 §7.4 Projection boundary/preserved terminology tension explicitly not resolved, not touched); `MAJ-03` temporal role-resolution reframed around a per-role minimal-complete cause-ref SET (no new schema field); `MAJ-04` invalidation/replacement cursor relation resolved via explicit Case A/Case B; `MIN-01` bitemporal-safe wording; `MIN-02` fabricated Scale numbers removed; Review-A record table added, no finding marked CLOSED, none self-reviewed/self-approved), and `ADR-046-CORR-002` (bounded correction of `ADR-046` against fresh ChatGPT Review A of v0.2 — `REVISION_REQUIRED — 0 Blocker / 3 Major / 0 Minor`, Risk `R2`; all six v0.1 findings confirmed genuinely remediated, none reopened; `MAJ-R2-01` new Decision item `1a` — `Cursor → Context projection record` anti-look-ahead relation, fail-closed on violation; `MAJ-R2-02` Case B reframed as a "fresh subsequent re-evaluation boundary" governed by 9 sub-rules, `R_replacement != R_later` now a consequence not a definition of "later," explicit causation guardrail added; `MAJ-R2-03` retired Mode-A/Review-B governance vocabulary replaced with current Chapter 11 v2.4 shape, review table simplified, both review rounds recorded as historical evidence) are all COMPLETE. **M1 `DONE`. M2 `BLOCKED` (parallel evidence lane). M3 `ACTIVE` (Context Projection / `context-aggregator`, deterministic core remains Review-A-validated `CLEAN`; `ADR-046` v0.3 corrected Draft candidate pending fresh Review A; runtime/Input Contract/publishing layer blocked on the `ADR-046` decision chain). M4 `QUEUED`.** No Quality-Gate finding remediated; no module approved; no Phase-3 approval granted. Feature Engine Chapter-13 Quality Gate is not fully `PASS` (M2 blocked); Phase-3 Approval Gate not reached; LIVE remains `NOT_AUTHORIZED`. Next governed action: fresh ChatGPT Review A re-review of `ADR-046` v0.3 corrected Draft candidate. |
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
| Completed | `FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001-ACTIVATION-001` | Executed the Product-Owner-authorized atomic activation of the Condition-2 tool-identity-continuity mechanism at reviewed boundary `278a8ab5c0916ef9c803d90bb8cf9ca934ca1260` (reviewed proposal blob `799d7f805387f09c846eebfbe87298fded338f75`, reviewed technical-evidence blob `a4f5ceb646e39a931a532af5fd324775a38c3bc5`). Review A: ChatGPT, **CLEAN — 0 Blocker / 0 Major / 0 Minor**, Risk `R2`, ADR Scope `ADR_OPTIONAL`, Product Owner explicitly selected `PROCEED WITHOUT OPTIONAL CROSS-CHECK`. `feature-engine-condition2-tool-identity-continuity-proposal-001.md` → **`APPROVED — EFFECTIVE` (mechanism activation only)** (resulting blob `f045be889d536c345d3f8154c17dd93fef07981c`), now an additional, disjoint Condition-2 resolution branch **(c) `VERIFIED_TOOL_IDENTITY_CONTINUITY`** — companion to, not a replacement of, `feature-engine-mutation-threshold-proposal-001.md` §4.1's existing (a)/(b) (byte-unchanged, untouched). Mechanism substance (`C1`–`C12`) unchanged from the `MAJOR-01`-corrected reviewed text — not redesigned. Application routing (§11.3) unchanged: every future per-identity application still requires its own separate reviewed/recorded governed decision under the existing ADR-045 model (Review A → Risk Classification → `R0`/`R1` + `D1`–`D12` all PASS → Delegated Technical Resolution eligible; `R2`/`ADR_REQUIRED`/governing-artifact reservation/explicit Product Owner call-in → Product Owner Decision). **This activation does NOT apply branch (c) to `contracts.x__seal_verified_authority__mutmut_33` or any other identity, and grants NO Condition-2 credit — Condition 2 remains `169/170`.** `feature-engine-condition2-tool-identity-continuity-technical-evidence-001.json` fresh-verified byte-unchanged (blob `a4f5ceb646e39a931a532af5fd324775a38c3bc5`), not touched. No `src/`/`test`/`tooling`/dependency change; no Condition-1/3 work; Condition 1 remains `PASS — REVIEW A VALIDATED`; Condition 3 remains `SATISFIED — REVIEW A VALIDATED`; EVID-03 remains `OPEN`; Feature Engine remains `NOT APPROVED`; LIVE remains `NOT_AUTHORIZED` |
| Completed | `FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001-APPLY-001` | Applied the already Product-Owner-APPROVED/EFFECTIVE Condition-2 branch (c) `VERIFIED_TOOL_IDENTITY_CONTINUITY` mechanism to exactly one historical identity: `contracts.x__seal_verified_authority__mutmut_33`, mapped uniquely to current successor `feature_engine.contracts.x__seal_verified_authority__mutmut_36` (KILLED — two independent isolated runs, corroborated by Evidence-006's own formal killed status). Fresh-verified before mutation: boundary `aae246532b7eac8c6e0bbdc15a120784b8bb7e99`; effective mechanism blob `f045be889d536c345d3f8154c17dd93fef07981c`; technical-evidence blob `a4f5ceb646e39a931a532af5fd324775a38c3bc5`; `contracts.py` source blob `0d2e39bffb705a2b1f903cd1a54b5f099ae6a686` (identical to the technical-evidence artifact's own current boundary — no source drift). All `C1`–`C12` verified PASS (exact reconstruction both sides, unique 1:1 mapping, no refactor, mutmut `3.7.0` provenance, per-identity-only credit, no raw-score adjustment). Review A: ChatGPT, **CLEAN — 0 Blocker / 0 Major / 0 Minor**, Risk `R1`, ADR Scope `ADR_NOT_REQUIRED`. ADR-045 `D1`–`D12` all `PASS` (D8: ChatGPT distinct from Claude, who authored/executed the underlying technical evidence; D10: no governing-artifact reservation, no Product Owner call-in for this specific application — R2/D10(a) applied only to the mechanism's own one-time activation, already completed). Governed outcome: **`DELEGATED TECHNICAL RESOLUTION — CLEAN`** (`FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001-APPLY-DTR-001`) — NOT a Product Owner approval; no Product Owner decision requested or required. **Condition 2: `169/170` → `170/170 — SATISFIED`.** New additive artifact `feature-engine-condition2-tool-identity-continuity-application-001.json`. `feature-engine-condition2-tool-identity-continuity-proposal-001.md` and `-technical-evidence-001.json` both fresh-verified byte-unchanged, not touched — branch (c)/`C1`–`C12` not redesigned. No `src/`/`test`/`tooling`/dependency change; no Condition-1/3 work; Condition 1 remains `PASS — REVIEW A VALIDATED`; Condition 3 remains `SATISFIED — REVIEW A VALIDATED`. **`P3-FEATURE-QG-EVID-03` NOT closed by this transaction** — remains `OPEN`, closure is a separate, not-yet-performed governed action. Feature Engine remains `NOT APPROVED`; LIVE remains `NOT_AUTHORIZED` |
| Completed | `FE-EVID03-CLOSURE-001` | Recorded the separately-scoped governed closure of `P3-FEATURE-QG-EVID-03`, based exclusively on the three already-governed current Condition states — no new evidence produced, no condition re-evaluated. Fresh-verified before mutation: boundary `2ae0f3969ee3d377ed57d00cfb2b65d7c56c83f1`; `feature-engine-mutation-step9-formal-evidence-006.json` blob `460cf678a2c682c26540719da78ff798ce88705d`; `feature-engine-condition1-formal-measurement-006-review-a-dtr-001.json` blob `af911b9b5ccd18dc10b62afb0cdab4f85352f732`; `feature-engine-condition2-tool-identity-continuity-application-001.json` blob `09dfe07055fa10a1833a8d1fa6ab4a82ee289f1c`; `feature-engine-mutation-surface-completeness-evidence-003.json` blob `b306a9d78a1c7f5f70ffcd6e8b92489bd12df35b` — all matched exactly. Resolved the existing Condition-3 Review A closure record (`docs/MANIFEST.md`'s own `Condition-3 folded to SATISFIED — REVIEW A VALIDATED` section: CLEAN — 0 Blocker / 0 Major / 0 Minor, Risk `R1`, on `evidence-003.json`, 14/14 DETECTED faults, 9/9 target methods) — confirmed consistent, not redesigned, not rerun. Condition 1: `PASS — REVIEW A VALIDATED` (Condition 1A ≥ `84.899201217193%`, measured `85.393685812096%`, PASS; Condition 1B `18/18 KILLED`). Condition 2: `170/170 — SATISFIED`. Condition 3: `SATISFIED — REVIEW A VALIDATED`. Review A: ChatGPT, **CLEAN — 0 Blocker / 0 Major / 0 Minor**, Risk `R1`, ADR Scope `ADR_NOT_REQUIRED`. ADR-045 `D1`–`D12` all `PASS` (D8: ChatGPT distinct from Claude; D10: no governing-artifact reservation, no Product Owner call-in). Governed outcome: **`DELEGATED TECHNICAL RESOLUTION — CLEAN`** (`FE-EVID03-CLOSURE-001-DTR-001`) — NOT a Product Owner approval. **`P3-FEATURE-QG-EVID-03`: `OPEN` → `CLOSED — PASS — REVIEW A VALIDATED`.** **M1 (Feature Engine — `P3-FEATURE-QG-EVID-03` Closure): `ACTIVE` → `DONE`. M2 (Feature Engine — Remaining Quality-Gate Closure): `QUEUED` → `ACTIVE`** — M2's substantive scope NOT invented by this transaction; must be fresh-derived separately against current Chapter-13 authority. New additive artifact `feature-engine-evid03-closure-001.json`. Evidence-006, Condition-1 DTR, Condition-2 application, and Condition-3 evidence artifacts all fresh-verified byte-unchanged, not touched. No `src/`/`test`/`tooling`/dependency change; no Condition-1/2/3 redesign or rerun. **Feature Engine remains `NOT APPROVED`. Phase-3 module approval remains `NOT GRANTED`. LIVE remains `NOT_AUTHORIZED`.** No EVID-04 through EVID-08 closed |
| Completed | `FE-EVID03-COND2-M2-SCOPE-001` | Bounded, repository-grounded scope derivation and tracking reconciliation for M2 (Feature Engine — Remaining Quality-Gate Closure). No Quality-Gate finding remediated. Fresh-verified before mutation: boundary `01b05e73221474caf303b1a37fe886bf7366980d`; all 10 pinned artifact/authority blobs matched exactly (`milestone.md`, `feature-engine-evid03-closure-001.json`, `feature-engine-chapter13-remediation-plan-001.md`, `feature-engine-evid05b-formal-evidence-001.md`, `feature-engine-evid07-property-based-mechanism-candidate-001.md`, Chapter 2/13/14, Phase-3 rules, module registry). **Fresh-verified current-state matrix:** `EVID-03 = CLOSED — PASS — REVIEW A VALIDATED`; `EVID-05 = CLOSED — PASS` (part (a) `SATISFIED`, part (b) `CLOSED — PASS`); `EVID-07 = CLOSED — PASS` (Hypothesis mechanism Approved/installed/pinned); `EVID-04 = BLOCKED_BY_EXTERNAL_DEPENDENCY` (no Decision Engine/Strategy Plugin Host); `EVID-06 = OPEN — PARTIALLY SATISFIED / BLOCKED_BY_EXTERNAL_DEPENDENCY` (Feature-local `SATISFIED — REVIEW A VALIDATED`, NOT reopened; platform risk-not-increased assertion blocked, no Risk Gateway); `EVID-08 = BLOCKED_BY_EXTERNAL_DEPENDENCY` (Strategy/Decision/Risk Gateway/Execution all unbuilt, strict superset of `EVID-04`). Repository implementation-existence verification (directories inspected, not declarations alone): `python/` contains only `feature-engine`/`raw-regime-engine`/`structure-engine`; `go/` contains only `market-data-ingestion`/`market-reference-service`; zero Decision/Strategy/Risk/Execution implementation directories; `module-registry.yaml`'s corresponding entries all carry `status: candidate`. Chapter 14 §14.2 dependency-order finding: `Data Layer → Structure Engine & Raw Regime Engine → Feature Engine → Context Projection → Strategy → Decision → Risk Gateway → Execution` — matches expected sequence exactly; `EVID-04`/`EVID-06`-remaining-half/`EVID-08` each depend on modules strictly downstream of Feature Engine. **M2 acceptance boundary derived:** `EVID-04 = CLOSED — PASS`, `EVID-06 = CLOSED — PASS`, `EVID-08 = CLOSED — PASS`; `EVID-03`/`EVID-05`/`EVID-07` excluded as already complete, NOT reopened; `EVID-01`/`EVID-02` not reopened. Explicit prohibition on fake Feature-local substitutes recorded (no stub/mock Decision/Risk/Execution; "Feature Engine emitted nothing" never substitutes for the platform risk-not-increased assertion). Reconciled two stale rows in `feature-engine-chapter13-remediation-plan-001.md` (`EVID-05`, `EVID-07` — struck through, corrected in place, referencing their own later governing artifacts) and appended an `EVID-03` closure note; new §10 section added. New additive artifact `feature-engine-m2-scope-derivation-001.json`. Review: ChatGPT, AI Technical Architect, **CLEAN — 0 Blocker / 0 Major / 0 Minor**, Risk `R1`, ADR Scope `ADR_NOT_REQUIRED` — no new Quality-Gate semantics/architecture/module dependency/invariant/schema/governance rule created; reconciles tracking against already-existing authority only. No Product Owner decision required. **M2: `ACTIVE` → `BLOCKED`** — reason: remaining closure depends on downstream Phase-3 capabilities not yet implemented; no honest Feature-Engine-local remediation path exists for `EVID-04`, `EVID-06`'s remaining half, or `EVID-08`. **M1 remains `DONE`. M3 remains `QUEUED`. M4 remains `PROVISIONAL`** — neither re-sequenced by this transaction. No `src/`/`test`/`tooling`/dependency change. Feature Engine remains `NOT APPROVED`; Phase-3 module approval remains `NOT GRANTED`; LIVE remains `NOT_AUTHORIZED` |
| Completed | `RIDE-CRITICAL-PATH-CORRECTION-001` | Corrects the Ride project milestone/critical-path model so it matches already-Locked Phase-3 authority and removes the artificial operational dependency `M2 → Feature Engine Module Approval → downstream unlock`. PROJECT TRACKING / ORCHESTRATION CORRECTION ONLY — no Chapter-12/13 semantics changed, no Quality-Gate finding waived, no module implemented, no approval granted. Fresh-verified before mutation: boundary `cb4c514f2b11747ef4483910bce13a3ead628c5d`; all 9 pinned artifact/authority blobs matched exactly. **Authority Finding 1:** Chapter 12 §12.2 defines only a phase-level Phase Approval Gate (quality gates are one input item); Chapter 13 §13.1 is explicit (`Quality Gate pass ≠ Product Owner approval`; Quality Gate never approves/locks/decides phase transition); `phase-3-rules.md` §11's own gate-path model confirms a single phase-level Approval Gate at the end, not a per-module gate between adjacent Chapter-14 nodes; no other controlling authority (Lean Ride Operating Model, module-registry, ADR-045) defines a separate Feature Engine module Approval Gate — the sole generic phrase found (`docs/constitution/00-governance.md`'s "Phase/Module Approval Gate decisions") is a Product-Owner-reservation category, not a process definition. **Authority Finding 2:** Chapter 14 §14.2 sequence fresh-verified: `Data Layer → Structure Engine & Raw Regime Engine → Feature Engine → Context Projection → Strategy → Decision → Risk Gateway → Execution` — matches expected exactly; Phase-3 Rules require implementation to follow this order but introduce no mandatory per-module Product Owner Approval Gate. **Authority Finding 3:** `module-registry.yaml`'s `context-aggregator` entry fresh-verified (`module_type: projection`, `depends_on: [market-data-ingestion, structure-engine, raw-regime-engine, feature-engine]`, `status: candidate`); no `context-aggregator` executable implementation directory exists anywhere in the repository — confirmed via direct directory inspection. **Milestone correction:** M0/M1 preserved (`DONE`/`DONE`). M2 preserved unchanged (`BLOCKED`, acceptance boundary `EVID-04`/`EVID-06`/`EVID-08` all `CLOSED — PASS` required) but reclassified as a **parallel evidence lane**, no longer the primary-path blocker — NOT weakened, closed, waived, or reinterpreted. Prior M3 (`Feature Engine — Module Approval`, citing Chapter 12 §12.2 without supporting authority) superseded as a project-tracking entry — redefined **M3 — Context Projection / `context-aggregator`**, `QUEUED → ACTIVE`, depends on the existing upstream executable/contract boundary (NOT M2 reaching `PASS`); implementation criteria NOT invented, scope to be fresh-derived in the next separately-scoped WP; implementation NOT started. Prior M4 superseded — redefined **M4 — Strategy → Decision → Risk Gateway → Execution downstream Phase-3 chain**, `PROVISIONAL → QUEUED`, depends on M3; exact module/WP decomposition NOT invented. **Current-state terminology corrected:** "Feature Engine NOT APPROVED"/"Phase-3 module approval NOT GRANTED" replaced in current tracking prose (§4 table) with authority-accurate wording ("Feature Engine Chapter-13 Quality Gate is not fully PASS: M2 remains BLOCKED on EVID-04/EVID-06/EVID-08"; "Phase-3 Approval Gate has not been reached / granted") — historical artifacts and historical per-transaction prose left byte-unchanged; no Constitution defect claimed, no Chapter 12/13 change claimed. New additive artifact `docs/project/ride-critical-path-correction-001.json`. Review: ChatGPT, AI Technical Architect, **CLEAN — 0 Blocker / 0 Major / 0 Minor**, Risk `R1`, ADR Scope `ADR_NOT_REQUIRED` — changes no Constitution, ADR, Quality-Gate applicability, dependency graph, module taxonomy, product scope, or Approval authority; corrects an operational project-tracking model only. No Product Owner decision required; this is NOT a milestone acceptance decision. No `src/`/`test`/`tooling`/dependency change; no Constitution/ADR/module-registry modification; `EVID-04`/`EVID-06`/`EVID-08` unaltered; `context-aggregator`/Strategy/Decision/Risk Gateway/Execution NOT implemented; Phase-3 Approval Gate NOT opened; no module approved; Phase 3 NOT approved; LIVE remains `NOT_AUTHORIZED` |
| Completed | `CONTEXT-AGGREGATOR-CORE-001` | First bounded Phase-3 implementation slice for `context-aggregator` — the deterministic Context aggregation CORE ONLY, per `docs/domain/context.md` and `feature-context-architecture.md` §5. Fresh-verified before mutation: boundary `97ace48f5780abc47fae127c7f11659a988b4a72`; all 6 pinned artifact/authority blobs (`ride-critical-path-correction-001.json`, `milestone.md`, `module-registry.yaml`, `feature-context-architecture.md`, `context.md`, `stream-registry.yaml`) matched exactly; upstream `market-data-ingestion`/`structure-engine`/`raw-regime-engine`/`feature-engine` implementation directories confirmed to still exist, no `context-aggregator` directory existed yet. **Language resolution:** Python — unambiguous application of `ADR-008`'s layer-level pin (core analytical/decision-support logic, no venue I/O/risk-control/execution boundary) to this module's `implements_capabilities: [context-aggregation]` entry, per `monorepo.md` §4; `ADR_NOT_REQUIRED`, no new ADR. **New package:** `python/context-aggregator/` (package `context_aggregator`, Python `>=3.13`, zero runtime dependencies) — `scope.py` (`ContextSubjectScope`/`context_subject_id`, context.md §1), `definition.py` (bounded `ContextDefinition`, §6), `evidence.py` (module-local consumer-side views for exactly the seven upstream roles, §7 — no import of `feature_engine`/`structure_engine`/`raw_regime_engine`), `selection.py` (the exact two-phase Eligible Upstream Fact pipeline — Phase 1 four-step per-candidate filtering, Phase 2 role-specific selection, the shared seven-criterion total-order tie-break, §8; canonical input normalization, §10), `aggregation.py` (public entrypoint `aggregate_context_candidate`, §9/§17), `values.py` (`ContextValues`/`ContextAggregationCandidate` — explicitly NOT a published `MarketContextSnapshot`, no fabricated `event_id`/`event_contract_ref`/`stream_ref`/`producer_ref`/`sequence`). **Explicit visibility boundary preserved (Boundary D):** the public entrypoint accepts, per role, only candidate facts the caller already certifies as cursor-visible — recorded-time visibility (§8 Phase 1 step 2) is NOT re-implemented; every other locally-resolvable predicate (scope/definition-version match, effective-time cutoff, role-specific validity-at-cursor, role-specific selection, normalization) IS enforced. **Validation:** 54 tests passed (`pytest`), `ruff check` clean, `mypy --strict` clean, diagnostic coverage 96% (not a formal claim). **Unresolved gaps explicitly preserved, none invented:** no Context-scoped Input Contract; no published Context Event Contract; no `stream_ref`/`producer_ref` resolution; no ADR-009 runtime ordering protocol; no `context_definition_version` registry/storage mechanism; `context-aggregator.quality_tier` remains unresolved; no formal Chapter-13 Quality-Gate PASS claimed. No STOP condition triggered — Context semantic baseline (context.md §1/§6/§7/§8/§9/§10/§14/§17, `feature-context-architecture.md` §5/§13) was uniquely resolvable from existing authority with no invented Input Contract/Event Contract/frontier/architecture semantics. **Result NOT self-approved** — returned for fresh ChatGPT Review A + Risk Classification (expected `R1`/`ADR_NOT_REQUIRED`, not decided here). No `docs/architecture/module-registry.yaml`/`stream-registry.yaml`/Constitution/ADR modification; no upstream module source touched. **M2 unchanged (`BLOCKED`, parallel lane). M3 remains `ACTIVE`** (core implemented; NOT `DONE` — runtime/Input Contract/Event Contract/publishing/Strategy integration still open). **M4 remains `QUEUED`.** Phase-3 Approval Gate not reached; LIVE remains `NOT_AUTHORIZED`. Next governed action: fresh Review A of this implementation result, then bounded derivation of the next legitimate Context layer |
| Completed | `CONTEXT-AGGREGATOR-CORE-001-CORR-001` | Bounded correction of `CONTEXT-AGGREGATOR-CORE-001`, remediating three ChatGPT Review A Majors (`REVISION_REQUIRED — 0 Blocker / 3 Major / 0 Minor`, Risk `R1`, ADR Scope `ADR_NOT_REQUIRED`). Fresh-verified before mutation: boundary `60124a1f77811651f34f34314c983207d0759cc7`; all 8 pinned blobs (`evidence.py`, `selection.py`, `aggregation.py`, `context.md`, `candle.md`, `structure.md`, `regime.md`, `feature.md`) matched exactly. **`CONTEXT-CORE-A-MAJ-01` (computation-point Candle binding):** `aggregate_context_candidate`/`select_candle` now require an explicit `target_computation_point_ref` naming the exact visible Candle fact this call computes Context for (context.md §6/§7.0/§11) — the core resolves the Candle lineage only for that fact's own window; an unrelated later window never wins merely because its effective boundary is newer; a missing/invalid target fails closed (`None`). **`CONTEXT-CORE-A-MAJ-02` (superseded Regime/Feature resurrection):** `select_regime`/`select_feature` now resolve the lineage-superseded set over the FULL identity-matched candidate set, independent of and before the cutoff/not-invalidated filters (mirrors regime.md §11's "target window before exclusion" principle) — a fact once superseded by a visible successor can never resurface merely because that successor later becomes invalidated with no replacement visible (resolves to `None`, role missing/pending, §9). Also fails closed on the two detectable malformed-lineage shapes (self-supersession, fork) via new `MalformedLineageError`. **`CONTEXT-CORE-A-MAJ-03` (Structure effective-time interval):** `StructureFact.effective_time` changed from `datetime` to `EffectiveWindow` (matches structure.md's binding to the breaking Candle's own `[window_start, window_end)` interval, candle.md §1) — Phase-1 cutoff now checks `.window_end`; Phase-2 tie-break and §10 normalization now use the real `.window_start`/`.window_end` pair instead of one scalar collapsed onto both. All three corrections implemented in `python/context-aggregator/src/context_aggregator/{evidence,selection,aggregation}.py`; `errors.py` gained `MalformedLineageError`. **Tests:** conftest.py's `make_structure`/`full_valid_kwargs` updated (interval-based, `target_computation_point_ref` wired); 15 new regression tests across `test_selection.py`/`test_aggregation.py` covering the exact MAJ-01/02/03 mandatory scenarios (W1-correction-not-hijacked-by-W2, normal-W2-computation, Regime/Feature Cases 1/2/3, malformed-lineage fork/self-supersession, Structure interval-start tie-break, cutoff-checks-window-end-not-start-or-recorded-time). **Result:** `pytest` 69/69 passed (was 54); `ruff check` clean; `mypy --strict` clean, 16 source files; diagnostic coverage 97% (not a formal claim). No `docs/domain/*.md`/module-registry/stream-registry/Constitution/ADR file touched; no upstream module source touched; no Input Contract/Event Contract/frontier/publishing/Current-View work added; no Quality Tier assigned. Findings recorded as `CONTEXT-CORE-A-MAJ-01`/`-02`/`-03` — **addressed/remediated by this executor, NOT self-closed**; closure belongs to a fresh ChatGPT Review A re-review. **M2 unchanged (`BLOCKED`, parallel lane). M3 remains `ACTIVE`** (core corrected, still not `DONE`). **M4 remains `QUEUED`.** Phase-3 Approval Gate not reached; LIVE remains `NOT_AUTHORIZED` |
| Completed | `CONTEXT-AGGREGATOR-CORE-001-CORR-002` | Narrowly-scoped correction closing the residual of `CONTEXT-CORE-A-MAJ-02` only (ChatGPT re-review: `REVISION_REQUIRED — 0 Blocker / 1 Major / 0 Minor`, Risk `R1`, ADR Scope `ADR_NOT_REQUIRED`; `CONTEXT-CORE-A-MAJ-01`/`-03` already `CLOSED`, NOT reopened). Fresh-verified before mutation: boundary `4eca6a7a5075da70dbf36036d974515810dad615`; `selection.py`/`evidence.py`/`aggregation.py`/`milestone.md`/`context.md`/`regime.md`/`feature.md` all matched pinned blobs exactly. **Residual defect:** `_lineage_superseded_targets()` validated self-supersession and fork, but NOT the producer-contract invariant that a correction replacement must target the exact SAME computation window as the fact it supersedes (regime.md: same `(regime_subject_id, analysis_window)`; feature.md: same `(feature_subject_id, effective_window)`) — a malformed cross-window `supersedes_ref` edge could cause the superseded target to be wrongly excluded while the malformed successor was later filtered as effective-time-ineligible, permitting an unrelated older/independent window to win as a stale fallback. **Fix:** `_lineage_superseded_targets()` gained an optional `window_of` accessor parameter; when supplied AND the named `supersedes_ref` target is present in the same identity-matched candidate set, the successor's and target's window boundaries (`window_start`/`window_end`) must match exactly, else `MalformedLineageError` is raised immediately — never resurrecting the mis-targeted fact, never silently letting an unrelated window win, never degrading to `None` when doing so could allow another lineage to win instead. `select_regime`/`select_feature` now pass `window_of=lambda c: c.analysis_window`/`lambda c: c.effective_window` respectively; `select_candle` (MAJ-01) is NOT passed this parameter and its target-ref-bound, window-scoped-before-lineage-resolution behavior is unchanged — confirmed via diff (`evidence.py`/`aggregation.py` byte-unchanged this transaction; `select_candle`/`select_structure`/`StructureFact` untouched in `selection.py`). A `supersedes_ref` naming a target NOT present in the supplied candidate set remains unchecked (target-absent case, explicitly out of scope). **Preserved unchanged:** self-supersession/fork detection, the already-fixed "superseded fact never resurrects merely because its successor later becomes invalidated" rule, and legitimate independent windows (a malformed edge only fails its own lineage, never globally suppresses unrelated windows). **New tests (7):** `test_regime_cross_window_supersession_fails_closed` / `test_feature_cross_window_supersession_fails_closed` (mandatory Case A), `test_regime_cross_window_malformed_successor_cannot_induce_stale_fallback` / `test_feature_cross_window_malformed_successor_cannot_induce_stale_fallback` (mandatory Case B — D/A/B fixture, asserts `MalformedLineageError` not `D`), `test_regime_same_window_correction_remains_valid` / `test_feature_same_window_correction_remains_valid` (mandatory Case C), `test_regime_target_absent_supersedes_ref_unchecked` (target-absent boundary). Mandatory Cases D/E (pending-correction regression; valid 3-fact chain) already covered by CORR-001's existing same-window tests — reconfirmed passing unchanged. **Result:** `pytest` 76/76 passed (was 69); `ruff check` clean; `mypy --strict` clean, 16 source files; diagnostic coverage 98% (not a formal claim). No `docs/domain/*.md`/module-registry/stream-registry/Constitution/ADR file touched; no upstream module source touched; no Input Contract/Event Contract/frontier/publishing/Current-View work added; no Quality Tier assigned. `CONTEXT-CORE-A-MAJ-02` residual addressed/remediated by this executor — **NOT self-closed**; closure belongs to a fresh ChatGPT Review A re-review. **M2 unchanged (`BLOCKED`, parallel lane). M3 remains `ACTIVE`** (core corrected, still not `DONE`). **M4 remains `QUEUED`.** Phase-3 Approval Gate not reached; LIVE remains `NOT_AUTHORIZED` |
| Completed | `CONTEXT-CORE-REVIEW-A-DTR-001` + `ADR-046-AUTHOR-001` | Two-part transaction. **Part A** — persisted the already-issued final ChatGPT Review A closure of the Context deterministic core lineage (`CONTEXT-AGGREGATOR-CORE-001`/`-CORR-001`/`-CORR-002`): `CLEAN — 0 Blocker / 0 Major / 0 Minor`, Risk `R1`, ADR Scope `ADR_NOT_REQUIRED`, ADR-045 `D1`–`D12` all `PASS` (D8: ChatGPT distinct from implementation author/executor Claude). Governed outcome: **`DELEGATED TECHNICAL RESOLUTION — CLEAN`** (`CONTEXT-CORE-REVIEW-A-DTR-001`) — NOT a Product Owner approval, NOT a Chapter-13 Quality-Gate PASS, NOT M3 completion, NOT a Phase-3 approval. New additive artifact `docs/governance/context-aggregator-core-review-a-dtr-001.json`. `CONTEXT-CORE-A-MAJ-01`/`-02`/`-03` all now `CLOSED`. **Context deterministic core: `REVIEW A VALIDATED — CLEAN`.** No `python/context-aggregator/**` file touched. **Part B** — authored `docs/adr/ADR-046.md` (`Context Computation Cursor and Temporal Eligible-Upstream Supersession`, `v0.1`, `status: Draft`) as a **candidate only** — NOT approved, NOT self-reviewed. Ground-truth confirmed (fresh-read `context.md`/Chapter 8/`stream-registry.yaml`): `MarketContextSnapshot`/`MarketContextFactInvalidated` have no durable `computation_cursor`; `normalized_input_fact_refs` cannot substitute (proves selected evidence only, not visible-but-unselected candidates/stream universe/frontier); scalar `recorded_time` insufficient per Chapter 8 §8.5's own three-leg visibility predicate; `context.md` §4's causation-mapping invariant is closed/exhaustive and has no provision for a later-visible authoritative fact (never invalidated) becoming the new §8 winner for an old computation point — confirmed via direct quote of the exact invariant text. **Classification:** Risk `R2`, ADR Scope `ADR_REQUIRED` (Event-Schema trigger, same class as `ADR-034`/`ADR-035` for Feature) — NOT DTR-eligible. **Decision candidate (11 parts):** canonical Chapter 8 §8.5 Replay Cursor reused verbatim (no local schema); required `computation_cursor` on every `MarketContextSnapshot`, own boundary, never inherited on replacement; required `computation_cursor` on every `MarketContextFactInvalidated` (the `R_later` boundary); full three-leg visibility predicate (stream universe + same-stream sequence + recorded_time), effective-time cutoff independently applied; bounded temporal eligible-winner-supersession condition for the six non-Candle roles (conditions a–e, generalizing `ADR-034`'s Feature-specific `eligible_swing_selection_superseded` shape) — previously-selected ref need NOT itself be invalidated; existing direct upstream correction flows preserved/integrated, not replaced; `affected_upstream_roles`/`causation_refs` preserved, minimally extended (per-role causation may be a correction/invalidation event OR the later-visible winning fact itself — no new enum field, multi-role invalidation remains representable); re-evaluation never stale-falls-back, no replacement emitted if any role remains missing/pending; Context Input Contract binding established as a REQUIREMENT only (NOT authored — expected 4-stream universe cited: `market-data-ingestion-candle`/`structure-engine-structure`/`raw-regime-engine-regime`/`feature-engine-feature`, no Swing stream); authoritative-use fail-closed until all referenced artifacts (Input Contract, `ADR-041`-governed exact version snapshot, Stream Registry version) genuinely resolve; no global total order introduced, same-stream-only `sequence` comparison preserved. **Alternatives A–E** all explicitly evaluated (canonical-cursor-plus-temporal-rule chosen; snapshot-only cursor rejected — cannot prove `R_later`; envelope-derived cursor rejected — proven insufficient; process-memory/run-manifest cursor rejected — not durable/restart-survivable; Context-local cursor schema rejected — competing authority vs. Chapter 8). **Authority relationship:** `ADR-014` (Context/Feature fan-in boundary) and `ADR-041` (exact Input Contract version resolution) both cited descriptively, confirmed unaffected, NO fabricated `depends_on` edge to either or to `ADR-035`; no Approved ADR modified in place; no Constitution chapter amended. No STOP condition triggered — ground-truth confirmed the gap is real, not already resolved by existing authority, not impossible under upstream semantics (T-vs-T+n discipline makes it structurally possible for all six roles), representable without a materially larger schema redesign, and does not turn Context into an authoritative business-state owner (stays within `context.md` §20's already-owned "Eligible Upstream Fact selection policy" scope). Fresh-verified before mutation: boundary `442df64a3fcd2216c95cfc58129332ffbb42bedf`; `selection.py`/`context.md`/Chapter 8/`stream-registry.yaml`/`module-registry.yaml`/`ADR-041`/`ADR-035`/`milestone.md` all matched pinned blobs exactly. **Confirmed unchanged by this transaction:** `context.md`, `feature-context-architecture.md`, `module-registry.yaml`, `stream-registry.yaml`, any Input/Event Contract, all production source/tests/tooling, every existing Approved ADR. **M2 unchanged (`BLOCKED`, parallel lane). M3 remains `ACTIVE`** — deterministic core now `REVIEW A VALIDATED — CLEAN`; next architecture prerequisite is `ADR-046` candidate review; runtime/Input Contract/publishing layer remains blocked pending that decision. **M4 remains `QUEUED`.** `ADR-046 NOT APPROVED`. `Context Input Contract NOT AUTHORED`. Phase-3 Approval Gate not reached; LIVE remains `NOT_AUTHORIZED`. Next governed action: fresh ChatGPT Review A of the `ADR-046` Draft candidate |
| Completed | `ADR-046-CORR-001` | Bounded correction of `docs/adr/ADR-046.md` against fresh ChatGPT Review A of v0.1 (`REVISION_REQUIRED — 0 Blocker / 4 Major / 2 Minor`, Risk `R2`, ADR Scope `ADR_REQUIRED`, no Product Owner decision yet). Fresh-verified before mutation: boundary `e6eda486549323ed174603aa53fd62abda6060ac`; `ADR-046.md` matched pinned blob `9a16dd82bb0bbde1130d47944564f2b110784724` exactly. **Core decision direction preserved, not replaced** — canonical Chapter-8 Replay Cursor, required durable boundaries on both Context projection-record types, temporal winner/role-state supersession, no global total order, Context Input Contract deferred, fail-closed until referenced artifacts resolve, all unchanged. **`MAJ-01` (false reviewer-provenance metadata):** `reviewers: [ChatGPT, Claude]` falsely asserted review evidence that did not exist (Chapter 11 §11.4: `reviewers` = historical review evidence). Corrected: `version: "0.1" → "0.2"`, `reviewers: [ChatGPT]` only (Claude has not reviewed; no cross-check invented), `last_review` consistent, new bounded-correction banner recording the round-1 verdict/findings as `addressed/remediated pending fresh Review A re-review` — none marked `CLOSED`. **`MAJ-02` (Projection authority framing):** v0.1 wording implied Context's own output becomes authoritative in places, silently leaning on one side of the preserved `context.md`-vs-Chapter-7/module-registry terminology tension. Corrected: new "Authority-neutral framing" section (5 explicit points — does not change `module_type: projection`/`owns_authoritative_state: false`/Chapter 7 §7.4/the preserved tension; `computation_cursor` gives record-integrity, not domain authority; Decision-dependency ≠ authoritative ownership; legacy `context.md` wording question explicitly deferred; follow-on work must preserve this boundary); "Context projection record" terminology adopted throughout in place of "authoritative Context event/fact"; Decision item 10 retitled "Fail-closed until referenced artifacts resolve." `context.md`/`module-registry.yaml`/`feature-context-architecture.md` NOT touched. **`MAJ-03` (incomplete causal proof set):** Decision item 5/7 assumed exactly one cause ref per temporally-superseded role, insufficient for compound transitions (e.g. a later-visible successor `B` that is itself subsequently invalidated, requiring both `{B, I_B}` as proof). Corrected: Decision item 5 reframed as a 6-step role-resolution-delta test; Decision item 7 changed to a per-role minimal-complete cause-ref SET (one or more refs, branches (a) correction/invalidation, (b) later-visible winner, (c) both when compound) — `affected_upstream_roles`/`causation_refs` preserved unchanged, no new schema field; role attribution remains deterministic via event type + role discriminant + target/ref relationship, never list order; multi-role refs unioned/deduplicated into the one flat `causation_refs` array. **`MAJ-04` (invalidation/replacement cursor relation under-specified):** Decision item 8 did not define whether `R_replacement` equals `R_later`, permitting a knowledge gap. Corrected: Decision item 8 now defines Case A (`R_replacement == R_later`, reuse the exact already-established §8 result) and Case B (`R_replacement != R_later`, MUST independently re-run exact §8 selection at `R_replacement`, never reuse the `R_later` winner set) — required even when all seven roles were already complete at `R_later`. **`MIN-01` (historical truth vs. current validity):** over-strong "no longer the correct... result" wording risked reading as rewriting `C`'s own historical correctness. Corrected: `C` remains immutable and historically correct at `R_original`; only current-valid-lineage-head status changes at `R_later`; new "Bitemporal clarification" subsection confirms replay-before/after behavior is unaffected and already correct under existing §13/§14/§15. **`MIN-02` (unsourced Scale numbers):** fabricated `strategy: 50`/`exchange: 20` projection removed; `expected_scale` reset to `0`/`0`/`0` with explicit reasoning that Context computation/event volume and fixed 4-stream Input-Contract universe cardinality — not strategy/exchange count — are the relevant scale dimensions (same retention pattern `ADR-034` already used). **Review-A record added:** a dedicated "Independent reviews / Concerns / Risks noted" table recording the round-1 ChatGPT review as historical evidence (boundary/blob pinned, verdict `REVISION_REQUIRED`, Risk `R2`) — no finding marked `CLOSED`; disposition explicitly `addressed/remediated pending fresh Review A re-review`; no optional cross-check invoked or fabricated. No STOP condition triggered — authority-safe Projection framing required no Chapter 7/module-registry change; deterministic role→cause attribution achieved within the existing `affected_upstream_roles`/flat `causation_refs` structure, no new field; no new Context authority model, module-taxonomy/dependency change, or Constitution amendment required; no materially new architecture option needed — Option A preserved throughout. **Confirmed unchanged by this transaction:** `context.md`, `feature-context-architecture.md`, `module-registry.yaml`, `stream-registry.yaml`, any Input/Event Contract, all production source/tests/tooling, every existing Approved ADR. **M2 unchanged (`BLOCKED`, parallel lane). M3 remains `ACTIVE`** — Context deterministic core remains `REVIEW A VALIDATED — CLEAN`; `ADR-046` v0.2 correction candidate pending fresh Review A; Context runtime/Input Contract/publishing remains blocked on the `ADR-046` decision chain. **M4 remains `QUEUED`.** `ADR-046: Draft — NOT APPROVED`. Phase-3 Approval Gate not reached; LIVE remains `NOT_AUTHORIZED`. Next governed action: fresh ChatGPT Review A re-review of `ADR-046` v0.2 corrected Draft candidate |
| Completed | `ADR-046-CORR-002` | Bounded correction of `docs/adr/ADR-046.md` against fresh ChatGPT Review A of v0.2 (`REVISION_REQUIRED — 0 Blocker / 3 Major / 0 Minor`, Risk `R2`, ADR Scope `ADR_REQUIRED`, no Product Owner decision yet). Fresh-verified before mutation: boundary `e6ce28ad7b5aefd28f49e2c351e586641e6e1250`; `ADR-046.md` matched pinned blob `e02d7777c8ac02dea8488fdc6e24e4b55a0c80bd` exactly. **All six v0.1 findings (`MAJ-01`–`MAJ-04`, `MIN-01`–`MIN-02`) confirmed genuinely remediated by v0.2 — none reopened**, except that `MAJ-04`'s Case B is further tightened by `MAJ-R2-02`. Core decision direction preserved unchanged throughout. **`MAJ-R2-01` (missing Cursor→Record anti-look-ahead relation):** schema reuse of Chapter 8 §8.5's cursor alone did not define the relation between `computation_cursor` and the Context projection record carrying it — a record could theoretically claim a cursor from its own future. Corrected: new Decision item `1a` requires `computation_cursor.recorded_time <= record.envelope.recorded_time` on every `MarketContextSnapshot`/`MarketContextFactInvalidated` (equivalent to Chapter 8 §8.5.2's `Cursor → Decision` relation and `ADR-035`'s identical Feature adaptation), fail-closed on violation (record MUST NOT be published), no timestamp clamping, no field substitution; explicitly restates that the canonical cursor's own internal invariants (Position→Cursor, Lifecycle→Cursor, Registry→Lifecycle, Registry→Contract, stream-universe validity, retained/genesis semantics) remain entirely Chapter 8's, not redefined locally. **`MAJ-R2-02` (Case B insufficiently proves "later"):** v0.2's Case B labeled `R_replacement != R_later` as "LATER," but Ride's no-global-total-order discipline (§8.3/ADR-009) means two Replay Cursors can be later, earlier, or partially incomparable — inequality alone cannot prove the replacement incorporates the knowledge that justified the invalidation. Corrected: Case B reframed as a "fresh subsequent re-evaluation boundary" governed by 9 explicit sub-rules — genuine non-counterfactual cursor capture via the future governed Input-Contract/frontier mechanism; no proof via raw `recorded_time`/`sequence`/cross-stream comparison/wall-clock ordering; full cursor-visibility of the invalidation's own minimal-complete cause set (Decision item 7) required at `R_replacement`; independent `context.md` §8 rerun, never a cached `R_later` result; `MAJ-R2-01`'s relation applied identically; fail-closed/no-publication if required cause/state evidence is not representable under the new cursor's valid universe; a later governed Input Contract/Stream Registry version is permitted with no raw version-equality requirement — `R_replacement != R_later` is now a possible *consequence*, never the *definition*, of "later." Explicit causation guardrail added citing Chapter 6 §6.7/Chapter 8 §8.2.3: rule 4's cause set is exactly Decision item 7's `causation_refs` set, every member remaining a genuine direct causal predecessor/prerequisite, never a transitive/audit-only reference — Case B does not expand `causation_refs` into a generic evidence bag. **`MAJ-R2-03` (retired mandatory-two-review governance vocabulary):** the ADR still carried `Execution ID`/`Independence mode`/`Isolation attestation`/`Mode A (DISTINCT_PRINCIPAL)`/`Independent Review B`/`Review A/B` language, none of which survives under Chapter 11 v2.4/`ADR-045`'s current model (Review A → Risk Classification → routing; `R2` cross-check is advisory, Product-Owner-selected, never a Review-B-equivalent gate). Corrected: review table now uses only current-template columns (Reviewer principal / Role at review boundary / Review boundary / Concern / Risk / Recommendation), recording BOTH round-1 (`e6eda486...`, `REVISION_REQUIRED — 0/4/2`) and round-2 (`e6ce28ad...`, `REVISION_REQUIRED — 0/3/0`) ChatGPT Review A as historical evidence; "Current governance routing" section rewritten to the exact current shape (fresh Review A required; if CLEAN, Risk stays R2, decision passes to Product Owner, optional advisory cross-check never an approval prerequisite); Consequences/Accepted-risks wording corrected to remove "Review A/B pass" language. No Claude/cross-check invoked or fabricated. No STOP condition triggered — Case B fix required no platform-wide Replay-Cursor ordering relation (explicitly avoided per rules 3/9); no Constitution change; no new Context authority model; no new schema field (item 1a is a relational invariant on the existing `computation_cursor` field only); causation remains truthful under Chapter 6 §6.7 (explicit guardrail added); no module-taxonomy/dependency change. **Confirmed unchanged by this transaction:** `context.md`, `feature-context-architecture.md`, `module-registry.yaml`, `stream-registry.yaml`, any Input/Event Contract, all production source/tests/tooling, every existing Approved ADR. **M2 unchanged (`BLOCKED`, parallel lane). M3 remains `ACTIVE`** — Context deterministic core remains `REVIEW A VALIDATED — CLEAN`; `ADR-046` v0.3 corrected Draft candidate pending fresh Review A; Context runtime/Input Contract/publishing remains blocked on the `ADR-046` decision chain. **M4 remains `QUEUED`.** `ADR-046: Draft — NOT APPROVED`. Phase-3 Approval Gate not reached; LIVE remains `NOT_AUTHORIZED`. Next governed action: fresh ChatGPT Review A re-review of `ADR-046` v0.3 corrected Draft candidate |

## 6. PO dashboard snapshot

```text
Current milestone:        M3 — Context Projection / context-aggregator
                           (ACTIVE -- first bounded implementation
                           slice, the deterministic aggregation core,
                           COMPLETE at python/context-aggregator/, then
                           bounded-corrected (CONTEXT-AGGREGATOR-CORE-
                           001-CORR-001) for 3 Review-A Majors --
                           computation-point Candle binding, superseded
                           Regime/Feature resurrection prevention,
                           Structure effective-time interval -- then
                           the CONTEXT-CORE-A-MAJ-02 residual closed
                           (CONTEXT-AGGREGATOR-CORE-001-CORR-002,
                           cross-window supersedes_ref edges now fail
                           closed) -- final Review A persisted CLEAN
                           -- 0/0/0 (CONTEXT-CORE-REVIEW-A-DTR-001;
                           deterministic core = REVIEW A VALIDATED --
                           CLEAN) -- then ADR-046 Draft candidate
                           authored (Context Computation Cursor and
                           Temporal Eligible-Upstream Supersession,
                           v0.1, R2/ADR_REQUIRED, NOT approved, NOT
                           self-reviewed) -- then bounded-corrected to
                           v0.2 against fresh ChatGPT Review A
                           (REVISION_REQUIRED -- 0/4/2; MAJ-01 false
                           reviewer metadata, MAJ-02 authority-neutral
                           Projection framing, MAJ-03 role-resolution-
                           delta/cause-set reframing, MAJ-04 invalidation/
                           replacement cursor Case A/B, MIN-01 bitemporal
                           wording, MIN-02 unsourced Scale numbers -- all
                           addressed/remediated, none self-closed) --
                           then bounded-corrected to v0.3 against fresh
                           ChatGPT Review A of v0.2 (REVISION_REQUIRED
                           -- 0/3/0; MAJ-R2-01 new Cursor -> Context
                           projection record anti-look-ahead relation,
                           MAJ-R2-02 Case B reframed as a fresh
                           non-counterfactual re-evaluation boundary
                           with 9 sub-rules, MAJ-R2-03 retired
                           mandatory-two-review governance vocabulary
                           replaced with current Chapter 11 v2.4 shape
                           -- all six v0.1 findings confirmed genuinely
                           remediated, not reopened) as the next
                           architecture prerequisite, pending fresh
                           Review A re-review; M3 NOT DONE -- runtime/Input
                           Contract/Event Contract/publishing/Strategy
                           integration still deliberately
                           unimplemented, blocked pending ADR-046's
                           current-model review chain: fresh Review A
                           then Product Owner decision). M1
                           (Feature Engine EVID-03 Closure): DONE. M2
                           (Feature Engine Remaining Quality-Gate
                           Closure): BLOCKED, now a PARALLEL evidence
                           lane, no longer the primary-path blocker.
Primary blocker:          None on the primary implementation path --
                           M3 (Context Projection / context-aggregator)
                           is ACTIVE, depending on the existing
                           upstream executable/contract boundary
                           (market-data-ingestion, structure-engine,
                           raw-regime-engine, feature-engine -- all
                           already implemented), NOT on M2 reaching
                           PASS. M2 remains BLOCKED as a parallel
                           evidence lane -- EVID-04, the remaining
                           (platform) half of EVID-06, and EVID-08 are
                           each BLOCKED_BY_EXTERNAL_DEPENDENCY on
                           downstream Phase-3 modules (Decision
                           Engine, Risk Gateway, Execution Engine)
                           that do not yet exist anywhere in the
                           repository -- no honest Feature-Engine-
                           local remediation path exists today; M2 is
                           NOT weakened, closed, or waived. Full
                           derivation:
                           `feature-engine-m2-scope-derivation-
                           001.json` +
                           `ride-critical-path-correction-001.json`.
                           There is no standalone Feature Engine
                           Module Approval Gate under current Chapter
                           12/13 authority (fresh-verified this
                           transaction) -- the prior M3/M4 project-
                           tracking entries encoded a nonexistent
                           dependency, now corrected. Feature Engine
                           Chapter-13 Quality Gate is not fully PASS
                           (M2 BLOCKED on EVID-04/EVID-06/EVID-08);
                           Phase-3 Approval Gate has not been reached;
                           LIVE remains NOT_AUTHORIZED. Historical
                           figures below (84.21%-84.56% / 42-ID gate)
                           are superseded.
Current primary WP:       (none currently assigned) -- context-aggregator
                           deterministic core (Sections A-K, first
                           bounded Phase-3 implementation slice)
                           COMPLETE (`CONTEXT-AGGREGATOR-CORE-001`):
                           python/context-aggregator/ (package
                           context_aggregator, Python >=3.13, zero
                           runtime dependencies) implements the exact
                           context.md §8 two-phase Eligible Upstream
                           Fact selection pipeline, §9 seven-role
                           cardinality with fail-closed None result,
                           §10 canonical input normalization, and §17
                           verbatim (never recomputed) Context-values
                           assembly. Explicit visibility boundary
                           preserved: the core accepts only
                           already-cursor-visible candidates, never
                           self-certifies recorded-time visibility.
                           54 tests / ruff clean / mypy strict clean.
                           No Input Contract, Event Contract, stream-
                           registry frontier capture, publishing,
                           Quality Tier, or Strategy/Decision/Risk/
                           Execution work performed -- all remain
                           deliberately open, documented in the
                           package README. Result not self-approved --
                           returned for fresh ChatGPT Review A / Risk
                           Classification. Then bounded-corrected
                           (`CONTEXT-AGGREGATOR-CORE-001-CORR-001`)
                           for 3 Review-A Majors: `CONTEXT-CORE-A-MAJ-
                           01` (Candle computation-point binding lost
                           -- fixed via new required
                           target_computation_point_ref, window-scoped
                           lineage resolution); `CONTEXT-CORE-A-MAJ-02`
                           (superseded Regime/Feature fact could
                           resurrect if its successor later became
                           invalidated -- fixed by resolving the
                           lineage-superseded set over the full
                           candidate set before cutoff/invalidation
                           filtering, plus new MalformedLineageError
                           fail-closed on fork/self-supersession);
                           `CONTEXT-CORE-A-MAJ-03` (Structure
                           effective_time collapsed interval to scalar
                           datetime -- fixed, now EffectiveWindow).
                           69 tests / ruff clean / mypy strict clean,
                           97% diagnostic coverage. Findings recorded,
                           NOT self-closed -- awaiting fresh ChatGPT
                           Review A re-review. Re-review returned
                           REVISION_REQUIRED -- 0 Blocker / 1 Major /
                           0 Minor on the `CONTEXT-CORE-A-MAJ-02`
                           residual only (`CONTEXT-CORE-A-MAJ-01`/`-03`
                           CLOSED, not reopened): `_lineage_superseded_
                           targets()` did not validate that a
                           correction replacement targets the SAME
                           computation window as the fact it
                           supersedes (regime.md/feature.md invariant)
                           -- a malformed cross-window edge could
                           exclude the wrong fact and let an unrelated
                           independent window win as a stale fallback.
                           Fixed by `CONTEXT-AGGREGATOR-CORE-001-CORR-
                           002`: new optional `window_of` accessor on
                           `_lineage_superseded_targets()`, wired only
                           for `select_regime`/`select_feature` --
                           when the named `supersedes_ref` target is
                           present and its window differs from the
                           successor's, raises MalformedLineageError
                           immediately (never resurrects, never lets
                           an unrelated window win). `select_candle`/
                           `select_structure`/`StructureFact` and
                           `evidence.py`/`aggregation.py` confirmed
                           byte-unchanged this transaction. 7 new
                           tests (mandatory Cases A/B/C + target-absent
                           boundary, both Regime and Feature). 76 tests
                           / ruff clean / mypy strict clean, 98%
                           diagnostic coverage. NOT self-closed --
                           awaiting fresh ChatGPT Review A re-review of
                           the residual. That final Review A has since
                           been issued and persisted this transaction
                           (`CONTEXT-CORE-REVIEW-A-DTR-001`) --
                           CLEAN -- 0 Blocker / 0 Major / 0 Minor, R1,
                           ADR_NOT_REQUIRED, DELEGATED TECHNICAL
                           RESOLUTION -- CLEAN; CONTEXT-CORE-A-MAJ-01/
                           -02/-03 all CLOSED; Context deterministic
                           core = REVIEW A VALIDATED -- CLEAN. This
                           same transaction then authored
                           `docs/adr/ADR-046.md` (Context Computation
                           Cursor and Temporal Eligible-Upstream
                           Supersession, v0.1, status: Draft) as a
                           candidate only -- R2, ADR_REQUIRED, NOT
                           DTR-eligible, NOT approved, NOT
                           self-reviewed -- establishing a durable
                           canonical Chapter 8 Replay Cursor on
                           MarketContextSnapshot/
                           MarketContextFactInvalidated and a bounded
                           temporal eligible-winner-supersession
                           invalidation rule for the six non-Candle
                           roles. Fresh ChatGPT Review A of that v0.1
                           candidate has since returned
                           `REVISION_REQUIRED -- 0 Blocker / 4 Major /
                           2 Minor`, Risk R2 -- remediated this same
                           transaction (`ADR-046-CORR-001`):
                           `MAJ-01` false reviewer-provenance metadata
                           corrected (`reviewers: [ChatGPT, Claude]` ->
                           `[ChatGPT]`, the true historical review
                           evidence per Chapter 11 §11.4; version
                           `0.1 -> 0.2`); `MAJ-02` authority-neutral
                           framing added -- new dedicated section
                           confirming this ADR does not change
                           `module_type: projection`/
                           `owns_authoritative_state: false`/Chapter 7
                           §7.4/the preserved `context.md`-vs-Chapter-7
                           terminology tension, and does not turn
                           Context into an authoritative domain-state
                           owner; "Context projection record"
                           terminology adopted in place of
                           "authoritative Context event/fact"
                           throughout; `MAJ-03` Decision item 5/7
                           reframed around a role-resolution delta and
                           a per-role minimal-complete cause-ref SET
                           (one or more refs, e.g. `{B, I_B}` for
                           compound transitions) rather than assuming
                           exactly one ref per role --
                           `affected_upstream_roles`/`causation_refs`
                           preserved, no new schema field, role
                           attribution remains deterministic via event
                           type + role discriminant + target/ref
                           relationship; `MAJ-04` Decision item 8 now
                           defines Case A (`R_replacement == R_later`,
                           reuse the established result) and Case B
                           (`R_replacement != R_later`, MUST
                           independently re-run exact §8 selection,
                           never reuse a stale winner set); `MIN-01`
                           bitemporal-safe wording (`C` remains
                           immutable/historically correct at
                           `R_original`; only current-valid-lineage-head
                           status changes at `R_later`); `MIN-02`
                           fabricated `strategy: 50`/`exchange: 20`
                           Scale-check numbers removed, reset to 0/0/0
                           with the actual relevant scale dimensions
                           (Context computation/event volume, fixed
                           4-stream Input-Contract universe) explained.
                           A dedicated Review-A record table was added
                           recording the round-1 verdict as historical
                           evidence -- no finding marked CLOSED, all
                           `addressed/remediated pending fresh Review A
                           re-review`. Core decision direction
                           (canonical Chapter-8 cursor, dual durable
                           boundaries, temporal supersession, no global
                           total order, Input Contract deferred,
                           fail-closed) preserved unchanged throughout.
                           `context.md`/`module-registry.yaml`/
                           `feature-context-architecture.md`/any
                           existing ADR NOT touched. Fresh ChatGPT
                           Review A of that v0.2 candidate has since
                           returned `REVISION_REQUIRED -- 0 Blocker /
                           3 Major / 0 Minor`, Risk R2, confirming all
                           six round-1 findings genuinely remediated
                           (none reopened) -- remediated this same
                           transaction (`ADR-046-CORR-002`): `MAJ-R2-01`
                           new Decision item `1a` -- `Cursor -> Context
                           projection record` anti-look-ahead relation
                           (`computation_cursor.recorded_time <=
                           record.envelope.recorded_time`), fail-closed
                           on violation, no timestamp clamping; cursor's
                           own internal invariants (Position/Lifecycle/
                           Registry -> Cursor/Contract, stream-universe
                           validity, retained/genesis semantics) restated
                           as entirely Chapter 8's, not redefined
                           locally; `MAJ-R2-02` Decision item 8 Case B
                           reframed -- `R_replacement != R_later` no
                           longer means "later" (Ride has no global
                           total order across cursors); Case B is now a
                           "fresh subsequent re-evaluation boundary"
                           governed by 9 sub-rules (genuine
                           non-counterfactual cursor capture; no proof
                           via raw recorded_time/sequence/cross-stream
                           comparison/wall-clock ordering; full
                           cursor-visibility of the invalidation's own
                           minimal-complete cause set required at
                           R_replacement; independent §8 rerun, never a
                           cached R_later result; MAJ-R2-01's relation
                           applied; fail-closed if required evidence
                           unrepresentable; later registry/contract
                           version permitted, no raw version-equality
                           requirement); explicit causation guardrail
                           added (Chapter 6 §6.7/Chapter 8 §8.2.3 --
                           causation_refs never a generic evidence bag,
                           every member a genuine direct causal
                           predecessor/prerequisite); `MAJ-R2-03`
                           retired mandatory-two-review vocabulary
                           (Execution ID/Independence mode/Isolation
                           attestation/Mode A/Independent Review B/
                           Review A/B) replaced with current Chapter 11
                           v2.4 shape -- review table now records BOTH
                           review rounds as historical evidence with
                           current-template columns only; routing
                           corrected to: fresh Review A required, if
                           CLEAN then Risk stays R2 and the decision
                           passes to the Product Owner, optional
                           advisory cross-check never an approval
                           prerequisite. No STOP condition triggered.
                           `context.md`/`module-registry.yaml`/
                           `feature-context-architecture.md`/any
                           existing ADR NOT touched. Next governed
                           action: fresh ChatGPT Review A re-review of
                           `ADR-046` v0.3 corrected Draft candidate.
                           Prior Condition-1
                           formal measurement 006 and its Review A
                           DTR (`FE-EVID03-COND1-FORMAL-EVID-006-001`,
                           `FE-EVID03-COND1-FORMAL-006-DTR-001`)
                           COMPLETE; Condition-2 tool-identity-
                           continuity mechanism authored, corrected
                           (MAJOR-01), Product Owner activated, and
                           applied to the final identity
                           (`FE-EVID03-COND2-TOOL-IDENTITY-
                           CONTINUITY-001`, `-CORR-001`,
                           `-ACTIVATION-001`, `-APPLY-001`) COMPLETE;
                           P3-FEATURE-QG-EVID-03 closed
                           (`FE-EVID03-CLOSURE-001`); M2 scope derived
                           and reconciled (`FE-EVID03-COND2-M2-SCOPE-
                           001`); critical-path corrected
                           (`RIDE-CRITICAL-PATH-CORRECTION-001`); then
                           context-aggregator deterministic core
                           implemented (`CONTEXT-AGGREGATOR-CORE-001`),
                           bounded-corrected for 3 Review-A Majors
                           (`CONTEXT-AGGREGATOR-CORE-001-CORR-001`),
                           and the `CONTEXT-CORE-A-MAJ-02` residual
                           closed (`CONTEXT-AGGREGATOR-CORE-001-CORR-
                           002`); then final Review A persisted CLEAN
                           and ADR-046 Draft candidate authored
                           (`CONTEXT-CORE-REVIEW-A-DTR-001` +
                           `ADR-046-AUTHOR-001`); then ADR-046 bounded-
                           corrected to v0.2 against fresh Review A's 4
                           Majors/2 Minors (`ADR-046-CORR-001`); then
                           bounded-corrected to v0.3 against fresh
                           Review A's 3 further Majors (`ADR-046-CORR-
                           002`, this transaction) -- M1 DONE, M2
                           BLOCKED (parallel lane), M3 ACTIVE (Context
                           Projection / context-aggregator, deterministic
                           core Review-A-validated CLEAN, ADR-046 v0.3
                           pending fresh Review A re-review,
                           runtime/publishing/Strategy integration not
                           started), M4 QUEUED
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
mechanism:                 -- APPROVED -- EFFECTIVE (mechanism
                           activation only; resulting blob
                           f045be889d536c345d3f8154c17dd93fef07981c).
                           Proposes one new, disjoint
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
Continuity mechanism       FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001-
activation                 ACTIVATION-001. Product Owner APPROVED
(ACTIVATION-001):          activation at reviewed boundary
                           278a8ab5c0916ef9c803d90bb8cf9ca934ca1260
                           (reviewed proposal blob 799d7f805387f09c846e
                           ebfbe87298fded338f75, reviewed technical-
                           evidence blob a4f5ceb646e39a931a532af5fd3247
                           75a38c3bc5). Review A: ChatGPT, CLEAN -- 0
                           Blocker / 0 Major / 0 Minor, Risk R2, ADR
                           Scope ADR_OPTIONAL; Product Owner explicitly
                           selected PROCEED WITHOUT OPTIONAL CROSS-
                           CHECK. feature-engine-condition2-tool-
                           identity-continuity-proposal-001.md ->
                           APPROVED -- EFFECTIVE (mechanism activation
                           only; resulting blob f045be889d536c345d3f81
                           54c17dd93fef07981c) -- branch (c)
                           VERIFIED_TOOL_IDENTITY_CONTINUITY is now an
                           additional, disjoint Condition-2 resolution
                           branch, companion to proposal-001's own
                           SS4.1 (a)/(b) (byte-unchanged, untouched).
                           C1-C12 unchanged from the MAJOR-01-corrected
                           reviewed text -- not redesigned. Application
                           routing (SS11.3) unchanged: every future
                           per-identity application still requires its
                           own separate reviewed/recorded governed
                           decision under the existing ADR-045 model.
                           THIS ACTIVATION DOES NOT APPLY branch (c) to
                           contracts.x__seal_verified_authority__
                           mutmut_33 or any other identity, and grants
                           NO Condition-2 credit -- Condition 2 remains
                           169/170. Technical-evidence-001.json fresh-
                           verified byte-unchanged (blob a4f5ceb646e39a
                           931a532af5fd324775a38c3bc5), not touched. No
                           src/test/tooling/dependency change. Condition
                           1/3 preserved, unchanged.
Continuity mechanism       FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-001-
application                APPLY-001. Applied branch (c) to exactly one
(APPLY-001):               historical identity:
                           contracts.x__seal_verified_authority__
                           mutmut_33, mapped uniquely to current
                           successor
                           feature_engine.contracts.x__seal_verified_
                           authority__mutmut_36 (KILLED -- two
                           independent isolated runs, corroborated by
                           Evidence-006's own formal killed status).
                           Fresh-verified before mutation: boundary
                           aae246532b7eac8c6e0bbdc15a120784b8bb7e99;
                           effective mechanism blob
                           f045be889d536c345d3f8154c17dd93fef07981c;
                           technical-evidence blob
                           a4f5ceb646e39a931a532af5fd324775a38c3bc5;
                           contracts.py source blob
                           0d2e39bffb705a2b1f903cd1a54b5f099ae6a686
                           (identical to the technical-evidence
                           artifact's own current boundary -- no
                           source drift). All C1-C12 verified PASS.
                           Review A: ChatGPT, CLEAN -- 0 Blocker / 0
                           Major / 0 Minor, Risk R1, ADR Scope
                           ADR_NOT_REQUIRED. ADR-045 D1-D12 all PASS
                           (D8: ChatGPT distinct from Claude; D10: no
                           governing-artifact reservation, no Product
                           Owner call-in for this specific application
                           -- the mechanism's own R2/D10(a) reservation
                           applied only to activation, already
                           completed). Governed outcome: DELEGATED
                           TECHNICAL RESOLUTION -- CLEAN
                           (FE-EVID03-COND2-TOOL-IDENTITY-CONTINUITY-
                           001-APPLY-DTR-001) -- NOT a Product Owner
                           approval; none requested or required.
                           CONDITION 2: 169/170 -> 170/170 --
                           SATISFIED. New artifact: feature-engine-
                           condition2-tool-identity-continuity-
                           application-001.json. Mechanism/evidence
                           documents fresh-verified byte-unchanged, not
                           touched -- branch (c)/C1-C12 not redesigned.
                           No src/test/tooling/dependency change; no
                           Condition-1/3 work. P3-FEATURE-QG-EVID-03
                           NOT closed by this transaction -- remains
                           OPEN, closure is a separate, not-yet-
                           performed governed action. Feature Engine
                           remains NOT APPROVED; LIVE remains
                           NOT_AUTHORIZED.
P3-FEATURE-QG-EVID-03      FE-EVID03-CLOSURE-001. Recorded the
closure                    separately-scoped governed closure of
(CLOSURE-001):             P3-FEATURE-QG-EVID-03, based exclusively
                           on the three already-governed current
                           Condition states -- no new evidence
                           produced, no condition re-evaluated.
                           Fresh-verified before mutation: boundary
                           2ae0f3969ee3d377ed57d00cfb2b65d7c56c83f1;
                           evidence-006 blob
                           460cf678a2c682c26540719da78ff798ce88705d;
                           Condition-1 DTR blob
                           af911b9b5ccd18dc10b62afb0cdab4f85352f732;
                           Condition-2 application blob
                           09dfe07055fa10a1833a8d1fa6ab4a82ee289f1c;
                           Condition-3 evidence-003 blob
                           b306a9d78a1c7f5f70ffcd6e8b92489bd12df35b --
                           all matched exactly. Resolved the existing
                           Condition-3 Review A closure record
                           (docs/MANIFEST.md's own "Condition-3 folded
                           to SATISFIED -- REVIEW A VALIDATED"
                           section: CLEAN -- 0 Blocker / 0 Major / 0
                           Minor, Risk R1, on evidence-003.json, 14/14
                           DETECTED faults, 9/9 target methods) --
                           confirmed consistent, not redesigned, not
                           rerun. Condition 1: PASS -- REVIEW A
                           VALIDATED. Condition 2: 170/170 --
                           SATISFIED. Condition 3: SATISFIED -- REVIEW
                           A VALIDATED. Review A: ChatGPT, CLEAN -- 0
                           Blocker / 0 Major / 0 Minor, Risk R1, ADR
                           Scope ADR_NOT_REQUIRED. ADR-045 D1-D12 all
                           PASS (D8: ChatGPT distinct from Claude;
                           D10: no governing-artifact reservation, no
                           Product Owner call-in). Governed outcome:
                           DELEGATED TECHNICAL RESOLUTION -- CLEAN
                           (FE-EVID03-CLOSURE-001-DTR-001) -- NOT a
                           Product Owner approval. P3-FEATURE-QG-
                           EVID-03: OPEN -> CLOSED -- PASS -- REVIEW A
                           VALIDATED. M1: ACTIVE -> DONE. M2: QUEUED
                           -> ACTIVE -- M2's substantive scope NOT
                           invented by this transaction, must be
                           fresh-derived separately against current
                           Chapter-13 authority. New artifact:
                           feature-engine-evid03-closure-001.json.
                           Evidence-006, Condition-1 DTR, Condition-2
                           application, and Condition-3 evidence
                           artifacts all fresh-verified byte-
                           unchanged, not touched. No src/test/
                           tooling/dependency change; no Condition-
                           1/2/3 redesign or rerun. Feature Engine
                           remains NOT APPROVED. Phase-3 module
                           approval remains NOT GRANTED. LIVE remains
                           NOT_AUTHORIZED. No EVID-04 through EVID-08
                           closed.
M2 scope derivation        FE-EVID03-COND2-M2-SCOPE-001. Bounded,
(M2-SCOPE-001):             repository-grounded scope derivation and
                           tracking reconciliation for M2 -- no
                           Quality-Gate finding remediated. Fresh-
                           verified before mutation: boundary
                           01b05e73221474caf303b1a37fe886bf7366980d;
                           all 10 pinned artifact/authority blobs
                           matched exactly. Current-state matrix:
                           EVID-03 CLOSED -- PASS -- REVIEW A
                           VALIDATED; EVID-05 CLOSED -- PASS (part (a)
                           SATISFIED, part (b) CLOSED -- PASS,
                           evidence-05b blob
                           6f226560418f6d5cd0e845a8e1e4262e33dd874e);
                           EVID-07 CLOSED -- PASS (Hypothesis
                           mechanism Approved/installed/pinned, blob
                           b5421ecde7fc905045d22fd17a290711cfe0f62c);
                           EVID-04 BLOCKED_BY_EXTERNAL_DEPENDENCY (no
                           Decision Engine/Strategy Plugin Host);
                           EVID-06 OPEN -- PARTIALLY SATISFIED /
                           BLOCKED_BY_EXTERNAL_DEPENDENCY (Feature-
                           local SATISFIED -- REVIEW A VALIDATED, NOT
                           reopened; platform risk-not-increased
                           assertion blocked, no Risk Gateway); EVID-08
                           BLOCKED_BY_EXTERNAL_DEPENDENCY (Strategy/
                           Decision/Risk Gateway/Execution all
                           unbuilt, superset of EVID-04). Repository
                           implementation-existence verification
                           (directories inspected, not declarations
                           alone): python/ contains only feature-
                           engine/raw-regime-engine/structure-engine;
                           go/ contains only market-data-ingestion/
                           market-reference-service; zero Decision/
                           Strategy/Risk/Execution implementation
                           directories; module-registry.yaml's
                           corresponding entries all carry status:
                           candidate. Chapter 14 SS14.2 dependency-
                           order finding: Data Layer -> Structure
                           Engine & Raw Regime Engine -> Feature
                           Engine -> Context Projection -> Strategy ->
                           Decision -> Risk Gateway -> Execution --
                           matches expected sequence exactly. M2
                           acceptance boundary derived: EVID-04 =
                           CLOSED -- PASS, EVID-06 = CLOSED -- PASS,
                           EVID-08 = CLOSED -- PASS; EVID-03/EVID-05/
                           EVID-07 excluded as already complete, NOT
                           reopened; EVID-01/EVID-02 not reopened.
                           Explicit prohibition on fake Feature-local
                           substitutes recorded. Reconciled two stale
                           rows (EVID-05, EVID-07) in feature-engine-
                           chapter13-remediation-plan-001.md and
                           appended an EVID-03 closure note; new SS10
                           section added. New artifact: feature-
                           engine-m2-scope-derivation-001.json.
                           Review: ChatGPT, AI Technical Architect,
                           CLEAN -- 0 Blocker / 0 Major / 0 Minor,
                           Risk R1, ADR Scope ADR_NOT_REQUIRED -- no
                           new Quality-Gate semantics/architecture/
                           module dependency/invariant/schema/
                           governance rule created. No Product Owner
                           decision required. M2: ACTIVE -> BLOCKED --
                           reason: remaining closure depends on
                           downstream Phase-3 capabilities not yet
                           implemented; no honest Feature-Engine-local
                           remediation path exists for EVID-04,
                           EVID-06's remaining half, or EVID-08. M1
                           remains DONE. M3 remains QUEUED. M4 remains
                           PROVISIONAL -- neither re-sequenced by this
                           transaction. No src/test/tooling/dependency
                           change. Feature Engine remains NOT
                           APPROVED; Phase-3 module approval remains
                           NOT GRANTED; LIVE remains NOT_AUTHORIZED.
Critical-path correction   RIDE-CRITICAL-PATH-CORRECTION-001. PROJECT
(CORRECTION-001):          TRACKING / ORCHESTRATION CORRECTION ONLY --
                           no Chapter-12/13 semantics changed, no
                           Quality-Gate finding waived, no module
                           implemented, no approval granted. Fresh-
                           verified before mutation: boundary
                           cb4c514f2b11747ef4483910bce13a3ead628c5d;
                           all 9 pinned artifact/authority blobs
                           matched exactly. Authority Finding 1:
                           Chapter 12 SS12.2 defines only a phase-
                           level Phase Approval Gate (quality gates
                           are one input item, not a standalone
                           module gate); Chapter 13 SS13.1 explicit
                           (Quality Gate pass != Product Owner
                           approval; never approves/locks/decides
                           phase transition); phase-3-rules.md SS11's
                           own gate-path model confirms a single
                           phase-level Approval Gate at the end, not a
                           per-module gate between adjacent Chapter-14
                           nodes; no other controlling authority
                           defines a separate Feature Engine module
                           Approval Gate -- the sole generic phrase
                           found (governance.md's "Phase/Module
                           Approval Gate decisions") is a Product-
                           Owner-reservation category, not a process
                           definition. Authority Finding 2: Chapter 14
                           SS14.2 sequence fresh-verified matches
                           expected exactly; Phase-3 Rules require
                           dependency-STATE verification (executable/
                           contract boundary), not upstream Quality-
                           Gate PASS, before authoring a module out of
                           order. Authority Finding 3: module-
                           registry.yaml's context-aggregator entry
                           fresh-verified (module_type: projection,
                           depends_on: market-data-ingestion/
                           structure-engine/raw-regime-engine/
                           feature-engine, status: candidate); no
                           context-aggregator executable implementation
                           directory exists anywhere in the repository.
                           Milestone correction: M0/M1 preserved (DONE/
                           DONE). M2 preserved unchanged (BLOCKED,
                           acceptance boundary EVID-04/EVID-06/EVID-08
                           all CLOSED -- PASS required) but reclassified
                           as a PARALLEL evidence lane, no longer the
                           primary-path blocker -- NOT weakened,
                           closed, waived, or reinterpreted. Prior M3
                           ("Feature Engine -- Module Approval", citing
                           Chapter 12 SS12.2 without supporting
                           authority) superseded as a project-tracking
                           entry -- redefined M3 -- Context Projection /
                           context-aggregator, QUEUED -> ACTIVE,
                           depends on the existing upstream executable/
                           contract boundary (NOT M2 reaching PASS);
                           implementation criteria NOT invented;
                           implementation NOT started. Prior M4
                           superseded -- redefined M4 -- Strategy ->
                           Decision -> Risk Gateway -> Execution
                           downstream Phase-3 chain, PROVISIONAL ->
                           QUEUED, depends on M3; exact module/WP
                           decomposition NOT invented. Current-state
                           terminology corrected in SS4's live tracking
                           table ("Feature Engine NOT APPROVED"/
                           "Phase-3 module approval NOT GRANTED" ->
                           authority-accurate wording); historical
                           artifacts and historical per-transaction
                           prose left byte-unchanged. No Constitution
                           defect claimed; no Chapter 12/13 change
                           claimed. New artifact: ride-critical-path-
                           correction-001.json. Review: ChatGPT, AI
                           Technical Architect, CLEAN -- 0 Blocker / 0
                           Major / 0 Minor, Risk R1, ADR Scope
                           ADR_NOT_REQUIRED. No Product Owner decision
                           required; this is NOT a milestone acceptance
                           decision. No src/test/tooling/dependency
                           change; no Constitution/ADR/module-registry
                           modification; EVID-04/EVID-06/EVID-08
                           unaltered; context-aggregator/Strategy/
                           Decision/Risk Gateway/Execution NOT
                           implemented; Phase-3 Approval Gate NOT
                           opened; no module approved; Phase 3 NOT
                           approved; LIVE remains NOT_AUTHORIZED.
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
                           (This is a PROJECT TRACKING / ORCHESTRATION
                           CORRECTION only -- no Chapter-12/13
                           semantics changed, no Quality-Gate finding
                           waived, no module implemented, no approval
                           granted, ADR Scope ADR_NOT_REQUIRED, Risk
                           R1, ChatGPT Review A CLEAN -- 0/0/0. Fresh-
                           verified: no authoritative standalone
                           Feature Engine Module Approval Gate exists
                           under current Chapter 12/13 (or any other
                           controlling) authority -- the prior M3/M4
                           project-tracking entries encoded a
                           nonexistent module-approval dependency, now
                           corrected. M2 (Feature Engine Remaining
                           Quality-Gate Closure) remains BLOCKED,
                           unweakened, unwaived, acceptance boundary
                           unchanged (EVID-04/EVID-06/EVID-08 all
                           CLOSED -- PASS required) -- reclassified
                           only as a PARALLEL evidence lane, no longer
                           the primary implementation-path blocker.
                           M3 redefined: Context Projection /
                           context-aggregator, QUEUED -> ACTIVE,
                           depends on the existing upstream executable/
                           contract boundary (NOT M2 reaching PASS);
                           implementation criteria NOT invented,
                           implementation NOT started. M4 redefined:
                           Strategy -> Decision -> Risk Gateway ->
                           Execution downstream Phase-3 chain,
                           PROVISIONAL -> QUEUED, depends on M3;
                           decomposition NOT invented. M0/M1 unchanged
                           (DONE/DONE). Current-state terminology
                           corrected (SS4 live tracking table only;
                           historical artifacts/prose untouched):
                           "Feature Engine NOT APPROVED" ->
                           "Feature Engine Chapter-13 Quality Gate is
                           not fully PASS: M2 remains BLOCKED on
                           EVID-04/EVID-06/EVID-08"; "Phase-3 module
                           approval NOT GRANTED" -> "Phase-3 Approval
                           Gate has not been reached / granted". LIVE
                           remains NOT_AUTHORIZED. Next governed
                           decision point: fresh Context Projection /
                           context-aggregator implementation-readiness
                           derivation and first bounded implementation
                           WP -- not initiated here.)
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
