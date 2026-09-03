---
id: phase3-process-improvement-001
title: "Phase 3 Process Improvement Proposal #001 — Feature Engine / Mutation-Testing Review Cycle"
document_type: process-improvement-proposal
proposal_version: "0.1"
proposal_state: "PROPOSAL / NOT YET EFFECTIVE"
authored_at: "2026-09-03"
satisfies_rule: null
adopted_by: null
adopted_at: null
---

# Phase 3 Process Improvement Proposal #001 — Feature Engine / Mutation-Testing Review Cycle

**State: `PROPOSAL / NOT YET EFFECTIVE`.**

**Vai trò của tài liệu này:** đây LÀ một process-improvement PROPOSAL — KHÔNG một ADR, KHÔNG một Approval Gate, KHÔNG the formal `P3-RETRO-001` Phase 3 retrospective (that retrospective remains separately required, in full, before Phase 4 substantive work begins — this document does NOT satisfy it and is not a substitute for it), KHÔNG a Constitution/Testing Convention/execution-rules amendment, KHÔNG a Quality Gate/Review A/B rerun, and KHÔNG a retroactive reclassification of any already-completed transaction. This document captures workflow lessons observed during the Phase 3 Feature Engine mutation-testing mechanism/compatibility-candidate review cycle and PROPOSES three risk-based transaction classes, a semantic/bookkeeping lane split, batched-finding review, deterministic-check automation, and a MANIFEST-scope reduction — for future, separate, governed consideration. Nothing in this document changes current governance by existing.

## 1. Motivating observation (evidence-based, no invented lessons)

```text
The Feature Engine mutation-testing/compatibility-candidate cycle (Testing Convention
  v0.8 through v0.16, docs/MANIFEST.md sections from the mutmut candidate-authoring
  transaction through the v0.16 Product Owner approval) produced a long chain of
  separate, sequential transactions: mechanism candidate authoring, four evidence-
  fidelity correction rounds (v0.9-v0.12), mechanical approval recording, installation,
  two baseline attempts (one blocked by a test-isolation defect, one blocked by a
  distinct mutmut-internal defect), a root-cause investigation, a compatibility-shim
  candidate authoring transaction, three bounded semantic-correction rounds addressing
  Review A findings on that candidate (textual-spoof detection -> structural detection
  -> call-site-authenticated detection; ADR taxonomy correction), one pure date-
  fidelity correction, one review-evidence-recording transaction, and one Product-
  Owner-approval-recording transaction.
This observation is offered as MOTIVATION for the proposal below, not as a graded
  audit of any individual transaction's necessity — per this task's own instruction,
  no current transaction is retroactively classified into Class A/B/C by this document.
  The pattern worth naming plainly: several of the LATER transactions in this chain
  (date-fidelity correction, review-evidence recording, approval recording) were purely
  mechanical/bookkeeping in nature, yet were each authored, verified, and pushed as
  fully independent transactions with their own boundary re-verification, MANIFEST
  section, and CHANGELOG entry — proportionate rigor for a Class-A architectural
  decision, arguably disproportionate for a fact-recording step once the underlying
  semantic content is already settled.
```

## 2. Proposal: three risk-based transaction classes

```text
Class A -- High-risk semantic / architecture / QG mechanism.
  Examples: architecture semantics, contracts/invariants, governance rules, Quality
    Gate measurement mechanisms, changes affecting multiple modules or difficult-to-
    reverse behavior.
  Default path: Review A -> Independent Review B -> Product Owner decision.
  Rationale: these decisions are expensive to reverse and cross-cutting; the full
    independent-review chain is the correct, non-negotiable default.

Class B -- Tests / evidence / bounded remediation.
  Examples: test additions, evidence generation, bounded finding remediation,
    diagnostic corrections.
  Proposal: use risk-based review depth rather than automatically requiring the full
    Class-A chain for every mechanical evidence transaction. A bounded remediation
    that closes a single, already-scoped finding (e.g. a structural-detection redesign
    responding to one Review A finding) may warrant a single bounded re-review rather
    than a fresh full A+B+PO cycle, PROVIDED the finding's own scope was not itself
    reopened or expanded.

Class C -- Mechanical / bookkeeping / factual docs.
  Examples: lifecycle recording, exact-date correction, MANIFEST/CHANGELOG
    synchronization, already-completed review-evidence recording, deterministic
    arithmetic/count corrections.
  Proposal: prefer deterministic validation and fail-closed automation (see §5) over
    repeated semantic A+B review. A Class-C transaction records facts that are already
    established elsewhere (a commit timestamp, a reviewer's already-issued verdict, a
    Product Owner's already-issued decision) -- it does not itself exercise judgment,
    and treating it identically to a Class-A semantic decision does not add safety,
    only overhead.

This is a PROPOSAL only. No current or past transaction in this repository is
  retroactively classified into Class A, B, or C by this document.
```

## 3. Proposal: separate the semantic lane from the bookkeeping lane

```text
Semantic lane:
  candidate/design -> review -> remediation -> approval

Mechanical bookkeeping lane:
  record already-established facts/decisions/evidence

Proposed rule: a bookkeeping-lane transaction MUST NOT create, reinterpret, or close
  a semantic finding on its own authority. It may only RECORD a disposition that a
  semantic-lane actor (Review A, Independent Review B, Product Owner) has already,
  externally, issued. If a bookkeeping transaction discovers that the cited semantic
  disposition does not actually match the repository's current recorded state (a
  premise mismatch), it must fail closed and report the mismatch rather than either
  fabricating the missing disposition or silently proceeding -- this repeats a
  discipline already practiced ad hoc multiple times in this exact review cycle (e.g.
  refusing to record a Product Owner approval when the required review-chain evidence
  was not yet actually present in the governance record) and proposes making it an
  explicit, named rule rather than an implicit practice.
```

## 4. Proposal: batch bounded findings within one review pass

```text
Proposed default:
  complete bounded review -> consolidated finding set -> one bounded remediation
  transaction -> bounded re-review

Avoid, where reasonably foreseeable within the review's own already-authorized scope:
  finding -> commit -> re-review -> residual finding -> commit -> re-review -> ...

Rationale: this review cycle's own compatibility-candidate correction chain surfaced
  MAJ-01 and MAJ-02 together in one Review A pass (good -- batched), but then
  surfaced a RESIDUAL on MAJ-01 (marker proved construction but not real call-site
  origin) only in a SUBSEQUENT round, after the first correction had already been
  reviewed and (partially) accepted. A sufficiently thorough single review pass that
  explicitly asked "does this detection mechanism authenticate the actual call site,
  or only that some construction occurred somewhere" might have surfaced both the
  textual-spoof defect and the call-site-authentication gap in the same bounded review,
  avoiding one additional commit/re-review round.

Exception, explicitly preserved: where a discovered issue materially changes the
  review surface itself (e.g. a fix reveals a previously-inapplicable class of attack,
  or a structural redesign opens new attack surface a prior review pass could not have
  anticipated because the design did not yet exist), a follow-up bounded review round
  remains appropriate and is NOT discouraged by this proposal. The goal is avoiding
  AVOIDABLE round-trips, not suppressing legitimate iterative discovery.
```

## 5. Proposal: automate deterministic governance checks

```text
Proposed automatable, fail-closed checks (tooling, not yet built, not yet run):
  - HEAD / parent SHA verification (the exact required boundary equals the actual
    current HEAD, and the new commit's parent equals the pre-transaction HEAD).
  - Exact changed-file scope (the actual `git status --porcelain` output matches the
    transaction's own declared expected-file list, no more, no less).
  - MANIFEST version transition (the frontmatter `manifest_version` field increments
    by exactly the declared amount, no skips, no double-bumps).
  - Document lifecycle consistency (a `status: Approved` document has non-null
    `approved_by`/`approved_at`; a `status: Draft` document has both null; a version
    bump on an Approved document resets `approved_by`/`approved_at` to null unless the
    transaction is itself a mechanical approval of that exact new version).
  - Finding-state consistency (a finding referenced as CLOSED in one section is not
    simultaneously referenced as OPEN/PENDING elsewhere in the same current-state
    view, absent an explicit historical/superseded annotation).
  - Stale "PENDING REVIEW"/"PENDING VALIDATION" detection (flagging findings that have
    remained in a pending state across N consecutive transactions without forward
    progress, for human attention -- not auto-resolution).
  - Review-evidence presence before lifecycle approval (a mechanical Product-Owner-
    approval-recording transaction can be blocked automatically, before any edit, if
    the required Review A CLEAN + Independent Review B CLEAN dispositions are not
    already present in the governance record against the exact cited boundary --
    exactly the check this review cycle's own approval-recording task required a human
    judgment call to perform manually, once).
  - Package/count/arithmetic consistency (e.g. an inventory claiming "N methods"
    actually sums to N across its own enumerated list -- this exact defect class
    recurred multiple times in the mutmut mutation-surface inventory history, v0.10
    through v0.12).
  - Protected-path byte-identity (declared "must not change" paths are verified
    byte-identical via `git diff --quiet`, not merely asserted in prose).
  - Governance invariant checks (threshold/QG/approval-state fields that a
    transaction claims to "preserve unchanged" are actually verified unchanged, not
    merely repeated as text).
  - Semantic reviewed boundary vs. evidence-recording boundary distinction (when a
    later transaction records review evidence or approval for an earlier commit's
    semantic content, the tooling requires and displays BOTH SHAs distinctly, exactly
    as was done by hand in the two most recent transactions of this cycle).

Automation MUST fail closed: on any check failure, block the transaction and report
  the mismatch; never silently proceed, never auto-correct a semantic disposition.
Automation MUST NOT invent reviewer dispositions or Product Owner decisions -- it may
  only verify that ALREADY-RECORDED dispositions are internally consistent and
  correctly cited; it can never manufacture a review or approval that did not happen.
This proposal does not specify a concrete implementation (script, CI job, or agent
  skill) -- that is a separate, future, governed design decision.
```

## 6. Proposal: reduce MANIFEST historical prose

```text
Proposed target state:
  MANIFEST = current authoritative state / SSOT (single source of truth for "what is
    true right now").
  Detailed historical narrative (what happened, in what order, and why) lives
    primarily in: CHANGELOG, dedicated evidence artifacts, review records, and
    retrospectives (this document's own genre).

Constraint: MANIFEST must retain enough provenance (finding IDs, exact commit SHAs,
  exact blob hashes, exact reviewer dispositions) to resolve CURRENT state
  deterministically without needing to reconstruct history from CHANGELOG -- the goal
  is trimming repeated NARRATIVE prose (multi-paragraph "how we got here" retellings
  copied forward transaction after transaction), not the load-bearing identifiers
  current-state resolution actually depends on.

This migration is NOT performed by this proposal transaction. It would itself require
  a separate, carefully bounded transaction (or series of transactions) that decides
  exactly which existing MANIFEST prose is narrative-only versus state-load-bearing,
  and MANIFEST's own current size/structure is out of scope for this document to
  touch.
```

## 7. Non-negotiable controls explicitly preserved by this proposal

```text
This proposal does not weaken, and explicitly preserves:
  - Immutable review boundaries (a reviewed SHA's content is never treated as
    interchangeable with a later SHA without a fresh review of what actually changed).
  - Fail-closed evidence handling (a check or reviewer that cannot verify a claim
    reports it as unresolved/blocking, never as passing by default).
  - Independent Review A + Review B for high-risk (Class A) semantics -- unchanged,
    unshortened.
  - Product Owner as the sole approval authority -- no automation, tooling, or Class-C
    bookkeeping process may ever substitute for or pre-empt an actual Product Owner
    decision.
  - Separation of implementation, measurement, threshold/calibration, and approval as
    four distinct governed steps -- this proposal does not collapse or reorder them.
  - No self-approval, at any class level -- an executor never closes its own finding,
    approves its own candidate, or authors its own ADR's acceptance.
  - No fabricated review/decision evidence, ever, at any class level, under any
    automation or batching rationale.
  - LIVE remains separately authorized -- nothing in this proposal, if ever adopted,
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

## 9. ADR Scope Rule check (self-certification for the act of authoring this proposal)

```text
This document is a non-effective retrospective/proposal artifact. It does not amend
  the Constitution, any ADR, the Testing Convention, `docs/governance/execution-
  rules.md`, any `phase-*-rules.md`, Quality Gate semantics, `module-registry.yaml`,
  or any approval-authority rule. It changes no current review requirement, no current
  approval requirement, and no current Quality Gate mechanism -- by its own explicit
  §8 adoption statement, it has zero effect on current governance simply by existing.
Result: ADR_NOT_REQUIRED.
This document does NOT decide the ADR classification of any future adoption
  transaction. If and when adoption is pursued, that transaction must independently
  re-run the ADR Scope Rule against its own actual proposed scope at that time (which
  may differ from this proposal's scope, and may reasonably reach ADR_REQUIRED or
  ADR_OPTIONAL depending on exactly what is adopted and how broadly).
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
  required before Phase 4 substantive work) -- that retrospective remains a separate,
  future, required transaction, evaluating the full Phase 3 execution history against
  the P1-RETRO-001/P2-RETRO-001 structural precedent plus Phase-3-specific controls
  (P3-CORRECTION-CHAIN-001/P3-TXN-001/P3-VERIFY-001/P3-REVIEW-001/P3-BUDGET-001/
  P3-IDENTITY-001/P3-MODULE-BATCH-001), per docs/governance/phases/phase-3-rules.md
  §12.
KHÔNG retroactively classifies any already-completed transaction into Class A/B/C.
```

## 11. Change history

```text
v0.1  2026-09-03  Authored -- vai trò: `Phase 3 Process Improvement Proposal Author`.
      Captures workflow lessons from the Feature Engine mutation-testing mechanism /
      compatibility-candidate review cycle (Testing Convention v0.8-v0.16). Proposes:
      three risk-based transaction classes (A/B/C); explicit semantic-lane/bookkeeping-
      lane separation; batched bounded-finding review; a list of automatable,
      fail-closed deterministic governance checks; a MANIFEST-scope-reduction target
      (not performed here); and an explicit non-negotiable-controls preservation list.
      `proposal_state: PROPOSAL / NOT YET EFFECTIVE`. `adopted_by`/`adopted_at`: null.
      ADR Scope Rule for authoring this proposal: ADR_NOT_REQUIRED. Does not satisfy
      P3-RETRO-001. Does not adopt itself.
```
