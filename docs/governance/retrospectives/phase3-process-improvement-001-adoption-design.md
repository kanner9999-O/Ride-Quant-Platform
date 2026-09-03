---
id: phase3-process-improvement-001-adoption-design
title: "Phase 3 Process Improvement Proposal #001 — Adoption Design"
document_type: adoption-design-candidate
design_version: "0.1"
design_state: "ADOPTION DESIGN CANDIDATE / NOT EFFECTIVE"
authored_at: "2026-09-03"
reviewed_proposal: "docs/governance/retrospectives/phase3-process-improvement-001.md"
reviewed_proposal_version: "0.3"
reviewed_proposal_boundary: "8696e422fe41b5cf87bc0558444c3b0b2bc27bea"
accepted_for_design_by: "Product Owner"
accepted_for_design_at: "2026-09-03"
adopted_by: null
adopted_at: null
---

# Phase 3 Process Improvement Proposal #001 — Adoption Design

**State: `ADOPTION DESIGN CANDIDATE / NOT EFFECTIVE`.**

**Vai trò của tài liệu này:** đây LÀ a design candidate for the MINIMUM effective delta needed to realize the accepted lessons of proposal v0.3 — KHÔNG the effective rule change itself, KHÔNG an ADR, KHÔNG a review-evidence recorder for the proposal (that already exists, separately, at the reviewed proposal's own boundary). This document does not edit `phase3-process-improvement-001.md`. Activating any item below requires a SEPARATE, future, governed transaction that itself performs whatever review depth its own actual semantic delta warrants.

**Product Owner decision being folded into this same transaction (per the adopted lesson itself — no separate review-evidence/decision recorder), verbatim:** **"ACCEPT Phase 3 Process Improvement Proposal #001 v0.3 at boundary 8696e422fe41b5cf87bc0558444c3b0b2bc27bea FOR ADOPTION DESIGN. Do not activate any governance change yet."** Decision date: `2026-09-03`.

**Reviewed proposal baseline (as supplied for this transaction, recorded here rather than in a standalone recorder):** `docs/governance/retrospectives/phase3-process-improvement-001.md` v0.3, boundary `8696e422fe41b5cf87bc0558444c3b0b2bc27bea`. Review A: `CLEAN`. Independent Review B: `CLEAN`. This design candidate does not itself re-verify or reinterpret either disposition — it takes v0.3, as reviewed and accepted for design purposes, as its starting baseline.

**What this decision does NOT do:** it does not activate any governance rule change, does not amend `execution-rules.md`/`phase-3-rules.md`/any Constitution chapter/any ADR/`team.yaml`/Testing Convention, does not close `P3-PI-A-MAJ-01`/`-MAJ-02`/`-MIN-01` on proposal v0.3 itself (those remain the proposal document's own finding states, untouched here), and does not authorize any future adoption transaction to skip its own required review.

## 1. Method

```text
Independently inspected, this transaction, before drafting any disposition below:
  docs/governance/execution-rules.md (G-AUTH, G-TXN, G-REV, G-BUDGET, G-ID, G-QG,
    G-ORCH sections, full authority hierarchy);
  docs/governance/phases/phase-3-rules.md (P3-REVIEW-001, P3-TXN-001, P3-VERIFY-001,
    P3-IDENTITY-001, P3-BUDGET-001, P3-CORRECTION-CHAIN-001, P3-RETRO-001);
  docs/constitution/00-governance.md §3 (Decision Workflow, Mode A/B) and §4b (ADR
    Scope Rule table);
  docs/constitution/11-adr-process.md §11.5 (Review and acceptance gate) and §11.6
    (Approval transition must be atomic);
  docs/constitution/12-approval-gates.md (Product Owner sole authority);
  docs/adr/ADR-031.md (full text, especially §8 "Role-resolution semantics" and §9
    "Fail-closed behavior");
  docs/team/team.yaml (current member/role/alias assignments, read-only).
No effective file was modified during this inspection.
```

## 2. Adoption question 1 — Standalone Review Evidence

```text
Question: does any effective rule change is actually needed, given P3-TXN-001
  already defaults to atomic folding and Chapter 11 §11.6 already requires atomic
  approval recording?

Findings:
  - Chapter 11 §11.6, verbatim disposition: an ADR approval is ONE documentation
    change — Draft->Approved, approved_by/approved_at, reviewer evidence pinned,
    MANIFEST updated, ALL in the same change. Explicit: "Không được approve ADR
    trước rồi cập nhật MANIFEST/OQ ở change sau" (must not approve first and update
    MANIFEST in a later change).
  - P3-TXN-001, verbatim disposition: when a semantic transaction reaches a valid
    terminal result, the deterministic current-state bookkeeping it causes MUST by
    default be recorded in the SAME transaction when safe and reproducible ("PHẢI
    fold TRỪ KHI có lý do" — must fold unless there is a reason), with narrow named
    exceptions (atomic recording cannot safely happen together; independent evidence
    must exist first; the bookkeeping itself discovers a semantic conflict; a higher
    rule requires separation).
  - Together, these two rules already establish EXACTLY the target behavior:
    Candidate -> Review A -> Independent Review B -> Product Owner Decision -> ONE
    recorder. §11.6 is ADR-specific text but states the identical atomicity
    principle P3-TXN-001 already generalizes to all Phase 3 transactions.

Disposition: KEEP_NO_CHANGE. No effective rule text change is needed — the target
  workflow is already the DEFAULT under existing authority. The gap observed in the
  proposal's own motivating cycle (a standalone evidence-recording transaction
  before the approval-recording transaction) was a self-imposed PROMPT precondition
  in that specific approval-recording task, not a requirement of any cited rule (see
  question 2). No new parallel workflow is proposed or needed.
```

## 3. Adoption question 2 — Prompt-created precondition

```text
Question: does Global G-ORCH need one narrow tightening such as "A prompt-created
  precondition is not governance authority"?

Findings: G-ORCH's own mandatory pre-prompt self-check (execution-rules.md, "Trước
  MỌI governed executor/reviewer prompt") already includes, verbatim, item 6: "Tôi
  có đang tạo một review/micro-transaction KHÔNG CẦN THIẾT không?" (am I creating an
  unnecessary review/micro-transaction?). This is functionally close to the
  proposal's lesson but does not explicitly name the SPECIFIC failure mode observed:
  treating a precondition written into ONE'S OWN prompt/task design as if it were an
  external authority requirement, rather than recognizing it as a self-imposed
  constraint that can be redesigned.

Disposition: TIGHTEN_EXISTING — narrow, single-sentence candidate addition.
  Target file/rule: docs/governance/execution-rules.md, `## G-ORCH` section, as a new
    numbered rule `G-ORCH-005` (the section currently ends at `G-ORCH-004`).
  Exact minimal candidate wording (verbatim, for a future adoption transaction to
    consider — NOT activated here):
    "G-ORCH-005  Một precondition do CHÍNH prompt/task design tạo ra KHÔNG PHẢI
                 governance authority. Nếu một transaction fail closed CHỈ vì
                 precondition tự đặt ra nghiêm hơn authority thực tế yêu cầu, phản
                 ứng mặc định LÀ sửa lại prompt/process design đó — KHÔNG tự động
                 tạo một transaction governed mới chỉ để thỏa mãn precondition tự
                 tạo. Trước khi tạo transaction mới để thỏa một precondition fail
                 closed, tự hỏi: (1) một rule cao hơn có THỰC SỰ yêu cầu tách biệt
                 không? (2) transaction mới có giảm rủi ro semantic thật không?
                 (3) bookkeeping có thể fold an toàn vào một transaction đã required
                 sẵn không (đúng G-TXN-003/P3-TXN-001)? (4) mình có đang biến một
                 chi tiết implementation của chính prompt/recorder thành một project
                 rule không?"
  This is a clarifying elaboration of self-check item 6 already listed under
    G-ORCH, not a new taxonomy — it does not conflict with G-REV-001, G-TXN-003/004,
    P3-TXN-001, P3-REVIEW-001, or P3-VERIFY-001, all of which it explicitly
    cross-references rather than duplicates.
```

## 4. Adoption question 3 — Independent Review B identity

```text
Question: is a minimal clarification needed so that historical "Independent Review
  B" records still resolve to Claude, the role is not interpreted as requiring
  Claude, and Mode B independent GPT execution remains eligible?

Findings (team.yaml NOT modified in this transaction, read-only inspection):
  - ADR-031 §8 "Role-resolution semantics," verbatim disposition: "Eligibility LUÔN
    thuộc về principal, KHÔNG thuộc về execution... Một execution kế thừa role
    eligibility từ principal đã đăng ký của nó — execution TỰ NÓ KHÔNG BAO GIỜ có
    role riêng." This already establishes, at the highest available authority for
    this exact question, that "Independent Review B" is a ROLE/FUNCTION resolved at
    each review boundary via Mode A or Mode B eligibility (Chapter 0 §3, Chapter 11
    §11.5) — never a fixed identity.
  - team.yaml's own current alias_note on member "Claude" already states this alias
    is registered "theo đúng historical label đã dùng tại ADR-012/ADR-013 và các
    Package review transaction" and is explicitly "KHÔNG phải một actor/AI riêng
    biệt" — i.e. the alias is already scoped, in its own text, to historical/
    Mode-A-diversity-pattern resolution, not a claim that all future Independent
    Review B instances must be Claude.
  - Historical records ALREADY correctly resolve via this exact alias mechanism
    (confirmed: ADR-012/ADR-013 and this cycle's own Independent Review B
    dispositions cite "Claude" directly, consistent with the alias).

Disposition: KEEP_NO_CHANGE for the core semantic question (ADR-031 §8 + Chapter 0
  §3 + Chapter 11 §11.5 already fully establish that the role is not bound to any
  fixed identity; no effective rule contradicts or needs to restate this).
  TIGHTEN_EXISTING, DEFERRED (not designed as an immediate follow-up, only flagged
  as a future candidate): team.yaml's own `aliases: ["Independent Review B"]` field
  is a literal string-lookup mechanism that, if ever consulted mechanically by
  future tooling without reading the surrounding alias_note, could be misapplied to
  imply Claude is required. A minimal, future, non-ADR team.yaml clarification
  (living document, not frozen) would add one sentence to the existing alias_note,
  e.g.: "This alias resolves 'Independent Review B' to Claude for historical/Mode-A
  records only; a Mode B independent execution of a different principal (e.g. an
  isolated ChatGPT execution session satisfying ADR-031 §5) fulfills the same
  workflow role without using or requiring this alias, and must instead pin its own
  execution identity directly per ADR-031 §2/§5." NOT designed further and NOT made
  in this transaction, per this task's own explicit instruction not to change
  team.yaml here.
```

## 5. Adoption question 4 — Review purpose / compact metadata

```text
Question: do existing G-REV/G-ID/P3 rules already sufficiently establish review as
  risk-reduction/cross-check, compact metadata, and no long reasoning duplication in
  MANIFEST?

Findings:
  - G-REV-001 already states review effort must be proportional to real semantic
    risk, not transaction count or document polish — already frames review's
    purpose around actual risk reduction.
  - G-REV-003 already requires Independent Review B to verify independently rather
    than accept Review A's own reasoning — already establishes the cross-check
    purpose, not mere procedural sign-off.
  - G-ID-003 already requires MANIFEST to prioritize compact current-state
    resolution, with detailed history living in CHANGELOG/evidence tables — already
    covers "no long reasoning duplication in MANIFEST by default."
  - P3-IDENTITY-001 already specifies the minimum identity/boundary metadata
    required before a review counts toward a governance prerequisite.

Disposition: KEEP_NO_CHANGE. No new rule needed — every element of proposal v0.3's
  §11 (review purpose, compact record fields) is already fully covered by G-REV-001,
  G-REV-003, G-ID-003, and P3-IDENTITY-001 individually. Preferring KEEP_NO_CHANGE
  over inventing a restatement, per this task's own instruction.
```

## 6. Adoption question 5 — Automation

```text
Deterministic-tooling ideas (proposal v0.3 §8: SHA/parent verification, changed-file
  scope, MANIFEST version-transition checking, lifecycle consistency, arithmetic
  consistency, protected-path byte-identity, reviewed-boundary vs. evidence-
  recording-boundary distinction, approval-progression eligibility checks) are
  TOOLING_FOLLOWUP in every case — none of them require a governance TEXT change to
  authorize (the underlying manual requirement each automates already exists per
  P3-VERIFY-001/P3-IDENTITY-001/G-ID-001/002, per proposal v0.3 §3's own mapping).
  Building any such tool is a software-engineering task with its own review (code
  review, not Review A/B governance review), entirely separate from this adoption-
  design track. Not designed further here; explicitly separated from governance
  adoption, and NOT implemented in this transaction.
```

## 7. Summary disposition table

```text
Item                                          | Disposition
Standalone Review Evidence elimination        | KEEP_NO_CHANGE
Prompt-created-precondition (G-ORCH tighten)  | TIGHTEN_EXISTING (G-ORCH-005 candidate wording, §3)
Independent Review B identity (core question) | KEEP_NO_CHANGE
Independent Review B identity (team.yaml note)| TIGHTEN_EXISTING, DEFERRED (not designed further, not made here)
Review purpose / compact metadata             | KEEP_NO_CHANGE
Automated deterministic-check tooling         | TOOLING_FOLLOWUP (all items)
Batch-findings advisory practice (proposal §7)| DEFER — advisory/soft, no rule text candidate identified; left as reviewer-diligence guidance only, not a rule
```

## 8. ADR Scope Rule — run against the actual proposed future effective deltas

```text
Delta 1: add G-ORCH-005 to docs/governance/execution-rules.md (§3 above).
  Target file/rule: execution-rules.md, G-ORCH section (operational governance, NOT
    a Constitution chapter, NOT an ADR).
  Semantic effect: clarifies an existing self-check question (G-ORCH item 6) with
    one explicit named failure mode and a four-question self-check; does not create
    new approval authority, does not change WHO decides anything, does not add a
    new Governance/Approval PROCESS (it tightens an existing pre-prompt discipline
    check), does not touch any Platform Invariant/Event Schema/Module Taxonomy/
    dependency graph, and is narrowly reversible (a single rule ID, removable by a
    future correction if it proves unhelpful).
  Classification: ADR_NOT_REQUIRED. Rationale: per Chapter 0 §4b's own table, this
    falls under "typo/formatting"-adjacent narrow clarification of an ALREADY-
    EXISTING self-check item, not "Governance/Approval process" change (it does not
    alter who approves what, or the approval gate mechanism itself) and does not
    affect >1 module in the architectural sense (it is a repo-wide PROCESS
    discipline note, the same category execution-rules.md's own prior G-ORCH-004
    amendment and multiple other G-* amendments in its own change history were
    recorded under, each accepted directly by Product Owner without a prior ADR).

Delta 2 (deferred, not designed further, listed for completeness only): a future
  one-sentence clarifying addition to team.yaml's existing Claude alias_note (§4
  above).
  Target file/rule: docs/team/team.yaml (living document, explicitly not frozen,
    per its own header and its own established reverse-lookup-note precedent).
  Semantic effect: clarifies, in prose, that the existing alias does not imply
    Claude is mandatory for future Mode B Independent Review B instances — does not
    change any role, eligibility rule, or approval mechanism; ADR-031 §8 already
    controls the actual semantics being clarified.
  Classification: ADR_NOT_REQUIRED. Rationale: team.yaml's own established amendment
    pattern (its own file header: "living document, KHÔNG frozen") and its own
    documented precedent (the F-04 Phase 0 Exit Readiness Audit reverse-lookup note
    was added to team.yaml directly, without an ADR, specifically BECAUSE team.yaml
    is not an ADR/Constitution-tier artifact) confirm this.

No other effective delta is proposed by this design candidate — every other
  adoption question resolved to KEEP_NO_CHANGE, TOOLING_FOLLOWUP, or DEFER, none of
  which involve any governance TEXT change requiring an ADR Scope Rule
  classification of their own.

Consolidated adoption-package ADR disposition: ADR_NOT_REQUIRED.
  This consolidated disposition covers ONLY the two deltas actually identified
  above (both individually ADR_NOT_REQUIRED, neither touching Governance/Approval
  process, Platform Invariants, Event Schema, Module Taxonomy/dependency graph, or
  >1 module, and neither hard to reverse). A FUTURE adoption transaction that
  actually authors either delta MUST independently re-run the ADR Scope Rule at its
  own boundary against its own actual final wording — this document's disposition
  does not bind that future re-run, per this track's own established discipline
  throughout this entire review cycle (never assume a prior ADR Scope Rule result
  automatically inherits to a later, distinct transaction).
```

## 9. Transaction minimization — shortest safe future sequence

```text
Because nearly every adoption question resolved to KEEP_NO_CHANGE, TOOLING_FOLLOWUP,
  or DEFER, the future effective-adoption sequence, if the Product Owner later
  chooses to activate anything from this design, is SHORT:

Required only if Delta 1 (G-ORCH-005) is activated:
  ONE bounded transaction: amend execution-rules.md's G-ORCH section (add
    G-ORCH-005, bump execution-rules.md's own `version`, append its own Change
    history entry per its established pattern), update MANIFEST's current-state
    section for execution-rules.md's version in the SAME transaction (per P3-TXN-001
    §11.6-style atomicity — no separate bookkeeping transaction), and close this
    adoption-design candidate's own relevant item, ALL atomically. Review depth for
    this ONE transaction is determined by G-REV-001/P3-REVIEW-001 AT THAT TIME (this
    document does not presume a full Review A/Independent Review B chain is
    mandatory — execution-rules.md's own change history shows several of its prior
    G-* amendments were Product-Owner-accepted directly as narrow interpretive
    clarifications; whether THIS addition warrants a bounded semantic re-review or
    direct Product Owner acceptance is that future transaction's own determination,
    not fixed here).
  This is the ONE transaction genuinely identified as required BY existing authority
    IF Delta 1 is adopted — because execution-rules.md is an EFFECTIVE, living
    document and any semantic addition to it requires ITS OWN version bump and
    acceptance record, per its own frontmatter lifecycle fields (`operational_state:
    EFFECTIVE`, `accepted_by`/`accepted_at`) — this is not an invented governance
    step, it is the document's own already-established amendment mechanism.

Optional, deferred, NOT required for this adoption package to be considered
  complete:
  A future team.yaml clarifying-note transaction (Delta 2), only if/when Mode B is
    actually used for Independent Review B with a non-Claude principal in practice
    — no urgency, no rule currently blocks that scenario from working correctly
    without the note (ADR-031 §8 already governs it); the note is a readability
    improvement for future record-writers, not a correctness requirement.

Explicitly NOT proposed, consistent with this task's own transaction-minimization
  instruction:
  - No standalone Review Evidence transaction (question 1 resolved KEEP_NO_CHANGE —
    the target atomic-fold behavior is already the default).
  - No separate bookkeeping transaction for this adoption-design candidate's own
    Product Owner acceptance — folded directly into this same transaction's own
    frontmatter/§0 recording, above.
  - No Review A/Independent Review B for any purely mechanical recording step.
  - No duplicated or parallel governance taxonomy — every disposition above cites
    and defers to existing rule IDs, never inventing a competing rule numbering
    scheme.
```

## 10. Explicit non-effect of this transaction

```text
KHÔNG activates any governance rule change. KHÔNG amends execution-rules.md,
  phase-3-rules.md, any Constitution chapter, any ADR, team.yaml, or Testing
  Convention. KHÔNG closes P3-PI-A-MAJ-01/-MAJ-02/-MIN-01 on the reviewed v0.3
  proposal (those remain that document's own, untouched finding states). KHÔNG
  installs the mutation-compatibility shim. KHÔNG reruns the mutation baseline.
  KHÔNG changes Feature Engine's Chapter 13 QG state, module approval state, Phase 3
  Approval Gate state, or LIVE authorization state. KHÔNG satisfies or substitutes
  for P3-RETRO-001.
This document is `ADOPTION DESIGN CANDIDATE / NOT EFFECTIVE`. `adopted_by`/
  `adopted_at`: null. Activating any item above requires a separate, future,
  governed transaction, each independently re-running the ADR Scope Rule and
  applying whatever review depth its own actual semantic delta warrants.
```

## 11. Change history

```text
v0.1  2026-09-03  Authored -- vai trò: `Phase 3 Process Improvement Adoption Design
      Author`. Designs the minimum effective delta for proposal v0.3's five
      adoption questions. Resolved: standalone Review Evidence elimination ->
      KEEP_NO_CHANGE (P3-TXN-001 + Chapter 11 §11.6 already require atomic default
      fold); prompt-created-precondition -> TIGHTEN_EXISTING, one candidate
      G-ORCH-005 sentence proposed (not activated); Independent Review B identity
      -> KEEP_NO_CHANGE at the core semantic level (ADR-031 §8 already establishes
      role-not-identity), TIGHTEN_EXISTING/DEFERRED for an optional future
      team.yaml readability note (not made here); review purpose/compact metadata
      -> KEEP_NO_CHANGE (G-REV-001/003, G-ID-003, P3-IDENTITY-001 already cover
      it); automation -> TOOLING_FOLLOWUP, all items, no governance text implicated.
      Consolidated ADR disposition: ADR_NOT_REQUIRED for both identified deltas
      (re-run required at actual future adoption boundary). Minimal future sequence:
      at most ONE bounded transaction (execution-rules.md G-ORCH-005 addition +
      atomic MANIFEST update), plus one optional/deferred team.yaml note — no
      standalone Review Evidence transaction, no separate bookkeeping transaction,
      no Review A/B for mechanical recording, no duplicated taxonomy. Product
      Owner's "ACCEPT ... FOR ADOPTION DESIGN" decision folded into this same
      transaction, not a separate recorder. `design_state: ADOPTION DESIGN
      CANDIDATE / NOT EFFECTIVE`. `adopted_by`/`adopted_at`: null. Does not activate
      any rule. Next governed step: Review A of this adoption-design candidate.
```
