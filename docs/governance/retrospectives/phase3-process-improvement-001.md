---
id: phase3-process-improvement-001
title: "Phase 3 Process Improvement Proposal #001 — Feature Engine / Mutation-Testing Review Cycle"
document_type: process-improvement-proposal
proposal_version: "0.2"
proposal_state: "PROPOSAL / NOT YET EFFECTIVE"
authored_at: "2026-09-03"
satisfies_rule: null
adopted_by: null
adopted_at: null
---

# Phase 3 Process Improvement Proposal #001 — Feature Engine / Mutation-Testing Review Cycle

**State: `PROPOSAL / NOT YET EFFECTIVE`.**

**v0.2 BOUNDED CORRECTION (2026-09-03), vai trò: `Phase 3 Process Improvement Proposal v0.2 Bounded Correction Executor`.** Remediates three Review A findings on v0.1: `P3-PI-A-MAJ-01` (v0.1 read as proposing a PARALLEL governance taxonomy — Class A/B/C — without mapping it against already-effective controls, risking duplicate or conflicting authority), `P3-PI-A-MAJ-02` (v0.1's automation proposal hard-coded "Review A CLEAN + Independent Review B CLEAN" as a universal approval prerequisite, which is not what higher authority actually requires), `P3-PI-A-MIN-01` (v0.1's motivating narrative miscounted the compatibility-candidate correction chain as "three bounded semantic-correction rounds" when the actual sequence was two semantic-correction rounds, v0.14 and v0.15, plus one separate mechanical date-fidelity correction, v0.16). `proposal_version: "0.1" → "0.2"`. `proposal_state` VẪN `PROPOSAL / NOT YET EFFECTIVE`, `adopted_by`/`adopted_at` VẪN `null`/`null`. Does NOT adopt the proposal. v0.1's own text is corrected directly in place below (this document has never been Approved/effective and carries no immutable-history obligation analogous to an ADR or an already-approved Testing Convention banner) — the correction is recorded transparently in §12 Change history rather than by leaving v0.1's now-superseded prose standing.

**Vai trò của tài liệu này:** đây LÀ một process-improvement PROPOSAL, now reframed per Review A as a **gap analysis against existing effective controls** — KHÔNG một ADR, KHÔNG một Approval Gate, KHÔNG the formal `P3-RETRO-001` Phase 3 retrospective (that retrospective remains separately required, in full, before Phase 4 substantive work begins — this document does NOT satisfy it and is not a substitute for it), KHÔNG a Constitution/Testing Convention/execution-rules amendment, KHÔNG a Quality Gate/Review A/B rerun, and KHÔNG a retroactive reclassification of any already-completed transaction. This document identifies which already-effective controls already address the observed workflow pattern (`KEEP`), which could be applied more consistently (`TIGHTEN`), and which small number of items are not currently covered by any existing rule (`NEW GAP`) — for future, separate, governed consideration. Nothing in this document changes current governance by existing.

## 1. Motivating observation (evidence-based, corrected sequence)

```text
The Feature Engine mutation-testing/compatibility-candidate cycle (Testing Convention
  v0.8 through v0.16, docs/MANIFEST.md sections from the mutmut candidate-authoring
  transaction through the v0.16 Product Owner approval) produced this sequence:
  mechanism candidate authoring (v0.8); four evidence-fidelity correction rounds
  (v0.9-v0.12); mechanical approval recording (v0.12 approval); installation; two
  baseline attempts (one blocked by a test-isolation defect, one blocked by a distinct
  mutmut-internal defect); a root-cause investigation; a compatibility-shim CANDIDATE
  authoring transaction (v0.13); TWO bounded semantic-correction rounds addressing
  Review A findings on that candidate (v0.14: textual-spoof detection -> structural
  detection, plus an ADR-scope resolution; v0.15: structural detection ->
  call-site-authenticated detection, plus an ADR-taxonomy correction); ONE separate,
  purely MECHANICAL date-fidelity correction (v0.16, correcting two incorrect
  transaction-date literals — not a semantic change); one review-evidence-recording
  transaction; and one Product-Owner-approval-recording transaction.
  [CORRECTED, P3-PI-A-MIN-01: v0.1 miscounted this as "three bounded semantic-
  correction rounds," conflating the mechanical v0.16 date fix with the two genuine
  semantic-correction rounds (v0.14, v0.15). There were exactly two semantic-
  correction rounds on the compatibility candidate, not three.]

Distinguishing avoidable churn from legitimately required separation:
  - LEGITIMATELY REQUIRED separation, not avoidable churn: the review-evidence-
    recording transaction and the Product-Owner-approval-recording transaction were
    each necessarily separate from the v0.16 date-fix and from each other, because
    each one's own content did not exist yet at the time the prior transaction ran —
    Review A's and Independent Review B's dispositions were issued (externally) AFTER
    v0.16 was authored, and the Product Owner's decision was issued AFTER that review
    evidence existed. This is chronology-driven separation (the evidence a later
    transaction records literally did not exist before), not process overhead, and is
    exactly the case P3-TXN-001 already permits a bookkeeping transaction to be
    separate ("independent evidence PHẢI tồn tại trước").
  - CANDIDATE avoidable churn: the two-round v0.14/v0.15 semantic-correction sequence
    on the SAME underlying detection-mechanism design (textual match -> structural
    marker -> call-site-authenticated marker) is the kind of pattern
    P3-CORRECTION-CHAIN-001 and G-REV-004 already exist to bound and interrupt. Two
    rounds is well under P3-CORRECTION-CHAIN-001's three-round non-stabilization
    trigger, so no existing rule was violated or shown insufficient here — but the
    pattern is still worth naming as the concrete motivating case for §4 below (batch
    findings within one bounded review where reasonably foreseeable).
This observation is offered as MOTIVATION only, not as a graded audit of any
  individual transaction's necessity, and no current or past transaction is
  retroactively classified into any class/label by this document.
```

## 2. Existing effective-control mapping (`KEEP` / `TIGHTEN` / `NEW GAP`)

```text
[NEW, P3-PI-A-MAJ-01: added per Review A. Every substantive idea below is checked
  against already-effective Global (`G-*`) and Phase-3 (`P3-*`) rules BEFORE being
  carried forward as a proposal. Existing governance taxonomy and rule text control
  on any conflict with this document's own wording — this mapping is descriptive, not
  a redefinition of any cited rule.]

Idea: risk-proportional review depth (three named tiers)
  Existing authority: Global G-REV-001 ("review effort proportional to real semantic
    risk, not transaction count") + P3-REVIEW-001's own four-row table (new
    architecture/authority/contract semantics -> full Review A/B; bounded semantic
    correction -> bounded semantic re-review, scope only; mechanical factual
    correction -> deterministic verification; evidence/bookkeeping recording ->
    validation only).
  Disposition: KEEP. P3-REVIEW-001's table is THE controlling authority already —
    this proposal's §3 below is relabeled as non-authoritative shorthand for that
    same table, not a new taxonomy.

Idea: bookkeeping must not create/reinterpret/close a semantic finding; fail closed
  on premise mismatch
  Existing authority: Global G-TXN-003/G-TXN-004 (deterministic bookkeeping fold is
    permitted only while staying semantically mechanical; a "mechanical" transaction
    that turns semantic must be relabeled, never silently expanded) + P3-VERIFY-001
    (any transaction citing a review/QG/decision as input must verify it against the
    original artifact, not assert it) + P3-REVIEW-001's own "THÊM" clause (a
    recording/verification transaction that finds cited evidence contradicts the
    assertion being recorded must stop and route to governed remediation, never
    self-fix inside the recorder) + P3-TXN-001 (a bookkeeping transaction that itself
    discovers a semantic conflict must route to P3-REVIEW-001, not "fix" the
    evidence).
  Disposition: KEEP. This is already fully covered, already-effective authority —
    §4 below is retained only as a plain-language restatement citing these rules,
    not a new rule.

Idea: stop correction churn; batch findings within a bounded review's own scope
  Existing authority: Global G-REV-004 (stop correction churn when no new
    Major/Blocker) + P3-CORRECTION-CHAIN-001 (three non-stabilizing correction rounds
    on any single artifact trigger a mandatory root-cause consolidation transaction,
    not a fourth patch round).
  Disposition: KEEP for the reactive circuit-breaker (already covered, unchanged).
    NEW GAP for one narrow, PREVENTIVE piece: neither rule currently states a
    reviewer-diligence expectation to actively probe for foreseeable adjacent
    findings within an already-authorized bounded scope BEFORE round 1 closes,
    rather than only intervening reactively after round 3 fails to stabilize. This
    gap is advisory/soft (reviewer thoroughness is not mechanically enforceable) and
    is retained in §4 as the one genuinely new, narrow candidate from this idea.

Idea: automate deterministic checks (SHA/parent, changed-file scope, MANIFEST
  version transition, lifecycle consistency, arithmetic consistency, protected-path
  byte-identity, reviewed-boundary vs. evidence-recording-boundary distinction)
  Existing authority: the underlying MANUAL verification requirement for most of
    these items already exists (P3-VERIFY-001 for evidence/boundary/identity
    verification; P3-IDENTITY-001 for reviewer/evaluator identity pre-check; G-ID-001
    for the reviewed-semantic-identity vs. lifecycle-record-identity distinction;
    G-ID-002 for exact-identity pinning). No existing rule mandates building AUTOMATED
    TOOLING that performs these checks mechanically rather than relying on an
    executor's per-transaction manual diligence.
  Disposition: NEW GAP, narrowly scoped — the gap is "no tooling exists to automate
    already-required manual checks," not "no rule requires the checks." §5 is
    corrected accordingly (see §5 and `P3-PI-A-MAJ-02` correction below).

Idea: MANIFEST = compact current-state SSOT; detailed history lives in
  CHANGELOG/evidence artifacts/retrospectives
  Existing authority: Global G-ID-003, verbatim: "MANIFEST ưu tiên compact
    current-state resolution (exact version/status/blob hiện tại) — lịch sử chi tiết
    thuộc CHỦ YẾU về CHANGELOG.md/evidence table, KHÔNG lặp lại toàn bộ history trong
    mỗi MANIFEST row." Also relevant: P3-BUDGET-001's ≤1,500-word-per-edit guidance
    for MANIFEST sections.
  Disposition: KEEP — this is not a new proposal, it is ALREADY-EFFECTIVE Global
    authority. §6 is reframed as an observation that G-ID-003 could be applied more
    consistently in recent MANIFEST entries (a compliance/practice question, not an
    authority gap), not as a new rule to invent.

Idea: preserve independent review, Product Owner sole authority, phase separation,
  no self-approval, no fabricated evidence, LIVE separately authorized
  Existing authority: Constitution Chapter 11 §11.5 (independent-review minimum),
    ADR-031 (Mode A `DISTINCT_PRINCIPAL` / Mode B `SAME_PRINCIPAL_DISTINCT_EXECUTION`
    reviewer-independence mechanism), Chapter 12 (Product Owner as sole Approval Gate
    authority), and the entire established pattern of this session's own transaction
    history (implementation/measurement/threshold/approval kept as four distinct
    steps, never collapsed).
  Disposition: KEEP — §7 is retained as an explicit list purely so this proposal
    itself never appears to weaken any of these, cross-referenced to the actual
    controlling authority rather than restated as free-standing new principle.
```

## 3. Non-authoritative shorthand for P3-REVIEW-001's existing review-depth table

```text
[CORRECTED, P3-PI-A-MAJ-01: no longer presented as a new "Class A/B/C" taxonomy.]

This document uses the labels "Class A / Class B / Class C" ONLY as informal,
  non-authoritative shorthand for P3-REVIEW-001's own four existing rows (new
  architecture/authority/contract semantics; bounded semantic correction; mechanical
  factual correction; evidence/bookkeeping recording). Where this document's wording
  and P3-REVIEW-001's actual text conflict in any way, P3-REVIEW-001 (and the Global
  G-REV rules it implements) controls, without exception.

Explicit statements required by Review A:
  - These labels carry NO independent authority of their own; they exist only to aid
    readability of this proposal's own §1/§4 discussion.
  - Classification of any real transaction is based on its ACTUAL semantic delta —
    what genuinely changed in architecture, authority, contract, security, or
    Quality-Gate-mechanism terms — never on the transaction's own self-declared name
    or label ("mechanical," "bounded," "bookkeeping").
  - A transaction labeled "bounded remediation" that, in substance, changes
    architecture, authority, contract, security, or Quality-Gate-mechanism semantics
    CANNOT be downgraded to reduced review depth merely because of that label — it is
    a Row-1 ("new architecture/authority/contract semantics -> full Review A/B")
    change under P3-REVIEW-001 regardless of what it is called, and full independent
    Review A + Review B remains required wherever P3-REVIEW-001 (or any higher
    authority) actually requires it. This document proposes nothing that overrides
    that.
```

## 4. Observation: batch findings within an already-authorized bounded review scope

```text
[CORRECTED, P3-PI-A-MAJ-01: reframed as a narrow, advisory addition on top of
  already-effective G-REV-004/P3-CORRECTION-CHAIN-001, not a new rule.]

Already-effective, unchanged: G-REV-004 (stop churn on zero new Major/Blocker) and
  P3-CORRECTION-CHAIN-001 (mandatory root-cause consolidation after three
  non-stabilizing rounds on one artifact) already bound and interrupt correction
  churn reactively. This document proposes nothing to replace either.

Narrow observed gap (advisory only, not a new binding rule): within a review that is
  ALREADY authorized to inspect a given bounded scope, actively probing for
  foreseeable adjacent findings before closing round 1 — rather than only reacting
  after a subsequent round surfaces a residual — can avoid an otherwise-avoidable
  round-trip. The compatibility-candidate detection-mechanism sequence (textual match
  -> structural marker -> call-site-authenticated marker, v0.14/v0.15) is the
  motivating case: two rounds, not three, so no existing circuit-breaker was
  triggered or shown insufficient, but a single sufficiently thorough first pass
  asking "does this authenticate the actual call site, or only that some
  construction occurred" might have reached the final design directly.

Exception, explicitly preserved: where a discovered issue materially changes the
  review surface itself (a fix reveals a class of attack the design did not
  previously have, or a redesign opens genuinely new surface a prior pass could not
  have anticipated because the design did not yet exist), a follow-up bounded review
  round remains appropriate and is not discouraged. The observation is about avoiding
  AVOIDABLE round-trips, not suppressing legitimate iterative discovery.
```

## 5. Proposal: automated deterministic-check tooling (corrected approval-evidence criteria)

```text
[CORRECTED, P3-PI-A-MAJ-02: the approval-evidence check below no longer hard-codes
  "Review A CLEAN + Independent Review B CLEAN" as a universal prerequisite.]

Proposed automatable, fail-closed checks (tooling design only — not yet built, not
  yet run; underlying manual requirement for most items already exists per §2's
  mapping, this proposes automating enforcement of already-required checks):
  - HEAD / parent SHA verification.
  - Exact changed-file scope (`git status --porcelain` matches the transaction's own
    declared expected-file list, no more, no less).
  - MANIFEST version transition (increments by exactly the declared amount).
  - Document lifecycle consistency (Approved <-> non-null approved_by/approved_at;
    Draft <-> both null; a version bump on an Approved document resets both to null
    unless the transaction IS the mechanical approval of that exact new version).
  - Finding-state consistency (no finding simultaneously CLOSED and OPEN/PENDING in
    the same current-state view, absent an explicit historical/superseded
    annotation).
  - Stale "PENDING REVIEW"/"PENDING VALIDATION" detection, for human attention only —
    never auto-resolution.
  - Package/count/arithmetic consistency (an inventory claiming "N items" actually
    sums to N across its own enumerated list — this exact defect class recurred
    multiple times in the mutmut mutation-surface inventory history, v0.10-v0.12).
  - Protected-path byte-identity (`git diff --quiet` on declared "must not change"
    paths, not merely asserted in prose).
  - Governance invariant checks (fields a transaction claims to "preserve unchanged"
    are actually verified unchanged, not merely repeated as text).
  - Semantic reviewed boundary vs. evidence-recording boundary distinction (both SHAs
    required and displayed distinctly, per G-ID-001's existing identity distinction).
  - Approval-progression eligibility (CORRECTED — see below).

Corrected approval-progression eligibility check: automation may verify that
  progression from review to a Product Owner decision is ELIGIBLE by checking —
    (a) the required, eligible independent reviews for this transaction's actual
        classification (per P3-REVIEW-001/G-REV-001, not a hard-coded universal
        two-review assumption) actually exist in the governance record;
    (b) the exact reviewed boundary cited by each review matches the boundary the
        approval decision is about to cite;
    (c) reviewer identity/independence requirements resolve per P3-IDENTITY-001 and
        ADR-031's Mode A/Mode B mechanism (not merely an unregistered execution-
        identity label);
    (d) the ACTUAL recorded dispositions — whatever they literally are, not a
        hard-coded "CLEAN" string — permit progression under whatever standard
        actually applies to this artifact/finding class;
    (e) any unresolved finding is surfaced EXACTLY as recorded (severity, ID, state),
        never summarized away or silently dropped;
    (f) any accepted-non-blocking residual (e.g. a Minor the reviewer explicitly
        deemed non-blocking) is routed for EXPLICIT Product Owner treatment — noted,
        acknowledged, or otherwise dispositioned by the Product Owner — never
        silently waved through by the automation itself.
  Explicit statement (per the existing NON-NORMATIVE INTERPRETATION under
  `execution-rules.md`'s G-REV section, point 6, cited not reinvented): zero Minor
  findings / a "CLEAN" disposition is NOT a universal approval prerequisite unless
  applicable higher authority explicitly requires it for that specific artifact class
  — automation must check for WHATEVER the applicable standard actually is, not
  assume "CLEAN" is always the bar.
  Automation MUST NEVER auto-accept a residual finding on the Product Owner's behalf,
  and MUST NEVER invent, infer, or fabricate a reviewer disposition or a Product
  Owner decision — it may only verify that already-recorded dispositions are
  internally consistent, correctly cited, and eligible to progress.

This proposal does not specify a concrete implementation (script, CI job, or agent
  skill) — that remains a separate, future, governed design decision.
```

## 6. Observation: apply existing G-ID-003 more consistently (not a new proposal)

```text
[CORRECTED, per §2 mapping: reclassified from "proposal" to "observation," since
  G-ID-003 already states this exact target as already-effective Global authority.]

Global G-ID-003, verbatim: "MANIFEST ưu tiên compact current-state resolution (exact
  version/status/blob hiện tại) — lịch sử chi tiết thuộc CHỦ YẾU về CHANGELOG.md/
  evidence table, KHÔNG lặp lại toàn bộ history trong mỗi MANIFEST row." This is
  already the governing rule; this document invents no new one.

Observation only: recent MANIFEST sections in the mutation-testing/compatibility-
  candidate cycle (this document's own §1 motivating chain) carried substantial
  historical-narrative prose alongside current-state facts. Whether that reflects an
  actual G-ID-003 compliance gap, or reflects necessary provenance G-ID-003 itself
  permits retaining, is a question for the artifact's own owners to assess — this
  document does not adjudicate it and performs no MANIFEST migration itself.

Constraint restated (unchanged from G-ID-003 and P3-BUDGET-001): MANIFEST must retain
  enough provenance (finding IDs, exact commit SHAs, exact blob hashes, exact
  reviewer dispositions) to resolve current state deterministically without
  reconstructing history from CHANGELOG — trimming narrative retelling is the target,
  never the load-bearing identifiers current-state resolution depends on.

No migration is performed by this document.
```

## 7. Non-negotiable controls, cross-referenced to actual controlling authority

```text
This proposal does not weaken, and explicitly preserves:
  - Immutable review boundaries — Chapter 11 §11.3/§11.5 and this session's own
    established discipline (a reviewed SHA's content is never treated as
    interchangeable with a later SHA without fresh review of the actual delta).
  - Fail-closed evidence handling — P3-VERIFY-001, G-REV-003 (Independent Review B
    must verify directly against the artifact, never rely on Review A's own
    assertion).
  - Full independent Review A + Review B wherever P3-REVIEW-001 (or higher authority)
    actually requires it — unchanged, unshortened, not overridden by any label in
    this document (see §3's explicit statement).
  - Product Owner as the sole approval authority — Chapter 12; no automation,
    tooling, or bookkeeping-lane process may ever substitute for or pre-empt an
    actual Product Owner decision.
  - Separation of implementation, measurement, threshold/calibration, and approval as
    four distinct governed steps — this session's own established pattern throughout
    the mutation-testing track; not collapsed or reordered by this proposal.
  - No self-approval, at any classification level.
  - No fabricated review/decision evidence, ever, under any automation or batching
    rationale — explicit in §5's corrected automation criteria.
  - Reviewer identity/independence — P3-IDENTITY-001, ADR-031 Mode A/Mode B.
  - LIVE remains separately authorized — nothing in this proposal, if ever adopted,
    would by itself move any module or system closer to LIVE authorization.
```

## 8. Adoption

```text
This document is PROPOSAL / NOT YET EFFECTIVE.

No current workflow, Constitution rule, ADR, Testing Convention, Quality Gate, or
approval requirement changes merely because this proposal exists.

Adoption requires a separate governed decision transaction after reviewing the
proposal against existing authority and ADR Scope Rule.
```

## 9. ADR Scope Rule check (self-certification, re-run fresh for this v0.2 correction)

```text
This v0.2 correction remains a non-effective retrospective/proposal artifact — it
  does not amend the Constitution, any ADR, the Testing Convention, `docs/governance/
  execution-rules.md`, any `phase-*-rules.md`, Quality Gate semantics,
  `module-registry.yaml`, or any approval-authority rule. It changes no current
  review requirement, no current approval requirement, and no current Quality Gate
  mechanism. The correction itself (reframing as a gap analysis, correcting the
  automation criteria, correcting the motivating date-sequence claim) is strictly a
  narrowing/clarifying edit of the document's own non-effective prose — it does not
  expand this document's own effect on current governance in any way.
Result: ADR_NOT_REQUIRED.
This document does NOT decide the ADR classification of any future adoption
  transaction — that transaction must independently re-run the ADR Scope Rule against
  its own actual proposed scope at that time.
```

## 10. Explicit non-scope of this transaction

```text
KHÔNG modifies Constitution, any ADR, Testing Convention, Phase 3 rules
  (docs/governance/phases/phase-3-rules.md), execution-rules.md, implementation code,
  tests, CI configuration, or module-registry.yaml.
KHÔNG installs the mutation-compatibility shim.
KHÔNG reruns the mutation baseline.
KHÔNG changes Feature Engine's Chapter 13 Quality Gate state or approval state.
KHÔNG authorizes LIVE.
KHÔNG satisfies or substitutes for P3-RETRO-001 (the formal Phase 3 retrospective
  required before Phase 4 substantive work) — that retrospective remains a separate,
  future, required transaction, evaluating the full Phase 3 execution history against
  the P1-RETRO-001/P2-RETRO-001 structural precedent plus Phase-3-specific controls
  (P3-CORRECTION-CHAIN-001/P3-TXN-001/P3-VERIFY-001/P3-REVIEW-001/P3-BUDGET-001/
  P3-IDENTITY-001/P3-MODULE-BATCH-001), per docs/governance/phases/phase-3-rules.md
  §12.
KHÔNG retroactively classifies any already-completed transaction into any label used
  by this document.
KHÔNG adopts this proposal.
```

## 11. Finding states after this correction

```text
P3-PI-A-MAJ-01: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW.
P3-PI-A-MAJ-02: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW.
P3-PI-A-MIN-01: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW.
```

Not self-closed. Next step: bounded Review A re-review of v0.2.

## 12. Change history

```text
v0.1  2026-09-03  Authored -- vai trò: `Phase 3 Process Improvement Proposal Author`.
      Captured workflow lessons from the Feature Engine mutation-testing mechanism /
      compatibility-candidate review cycle (Testing Convention v0.8-v0.16). Proposed
      three risk-based transaction classes (A/B/C) without mapping them against
      already-effective controls; an automation criterion hard-coding "Review A
      CLEAN + Independent Review B CLEAN"; and a motivating narrative miscounting the
      compatibility-candidate correction chain as three semantic-correction rounds.
      `proposal_state: PROPOSAL / NOT YET EFFECTIVE`. ADR Scope Rule: ADR_NOT_REQUIRED.

v0.2  2026-09-03  Bounded correction -- vai trò: `Phase 3 Process Improvement
      Proposal v0.2 Bounded Correction Executor`. Remediates three Review A findings:
      `P3-PI-A-MAJ-01` (added §2's explicit KEEP/TIGHTEN/NEW-GAP mapping against
      Global G-REV-001/002/003/004, G-TXN-003/004, G-ID-001/002/003, P3-REVIEW-001,
      P3-TXN-001, P3-VERIFY-001, P3-IDENTITY-001, P3-BUDGET-001,
      P3-CORRECTION-CHAIN-001; reframed §3's Class A/B/C as non-authoritative
      shorthand for P3-REVIEW-001's existing table, explicit that actual semantic
      delta controls over any self-declared label; reframed §4/§6 as narrow/advisory
      or non-proposals per the mapping). `P3-PI-A-MAJ-02` (§5 corrected: removed
      "Review A CLEAN + Independent Review B CLEAN" as a hard-coded universal
      approval-progression check; replaced with eligible-review-existence, boundary-
      match, identity/independence, actual-disposition, unresolved-finding-surfacing,
      and explicit-Product-Owner-treatment-of-residuals criteria; added explicit
      "zero Minor/CLEAN is not a universal prerequisite unless higher authority
      requires it" statement citing execution-rules.md's existing NON-NORMATIVE
      INTERPRETATION point 6; explicit automation must never auto-accept a residual).
      `P3-PI-A-MIN-01` (§1 corrected: two semantic-correction rounds, v0.14/v0.15, not
      three; v0.16 was a separate mechanical date-fidelity correction; added explicit
      distinction between chronology-driven legitimate transaction separation and the
      one candidate avoidable-churn pattern). `proposal_version: "0.1" -> "0.2"`.
      `proposal_state` VẪN `PROPOSAL / NOT YET EFFECTIVE`. `adopted_by`/`adopted_at`
      VẪN `null`/`null`. Finding states: all three `REMEDIATED — PENDING BOUNDED
      REVIEW A RE-REVIEW` — NOT self-closed. ADR Scope Rule re-run fresh for this
      correction: ADR_NOT_REQUIRED. Does not adopt the proposal. Does not satisfy
      P3-RETRO-001.
```
