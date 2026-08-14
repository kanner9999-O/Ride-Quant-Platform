---
id: phase-2-batch-05-manifest
title: "Phase 2 Prototype — Batch 05 — Batch Manifest"
version: "1.0"
status: Candidate
owner: Product Owner
created_at: "2026-08-14"
---

# Phase 2 Prototype — Batch 05 — Batch Manifest

**Vai trò của tài liệu này:** batch-level evidence record cho Batch 05, đúng `phase-2-rules.md`
`P2-PROTOTYPE-001` (review theo batch/milestone, KHÔNG per-screen governance cycle riêng). Đây LÀ
transaction AUTHORING đầu tiên cho Batch 05 — Review A/Independent Review B **CHƯA thực hiện**.
Lifecycle `CANDIDATE`, chưa self-approved, chưa review.

## 1. Batch identity

```text
Batch:              Phase 2 — Batch 05 (Review / causation / historical comparison / correction
                     inspection)
Phase:               Phase 2 — Product Prototype (AUTHORIZED TO BEGIN)
Authoritative DoD:   docs/phase-dod/phase-2-dod.md v0.3, status Approved,
                     post-acceptance blob de399900a93c7ec7ee64577093513de1643ebb33
Status:              CANDIDATE — authoring transaction, Review A + Independent Review B CHƯA thực
                     hiện. KHÔNG READY_FOR_NEXT_PHASE2_BATCH verdict tại transaction này.
Created:             2026-08-14
Starting HEAD:       988e3c368d452345329d27c47fa9d6963d31d3ff (verified via git rev-parse HEAD
                     trước khi tạo file, đúng G-VERIFY-001)
Depends on (real,
  read-only link,
  KHÔNG modified):    prototype/phase-2/batch-01/ — CANDIDATE, review COMPLETE, verdict
                     READY_FOR_NEXT_PHASE2_BATCH, untouched by this transaction.
                     prototype/phase-2/batch-02/ — CANDIDATE, review COMPLETE, verdict
                     READY_FOR_NEXT_PHASE2_BATCH, untouched by this transaction.
                     prototype/phase-2/batch-03/ — CANDIDATE, review COMPLETE, verdict
                     READY_FOR_NEXT_PHASE2_BATCH, untouched by this transaction.
                     prototype/phase-2/batch-04/ — CANDIDATE, review COMPLETE, verdict
                     READY_FOR_NEXT_PHASE2_BATCH, untouched by this transaction.
                     Verified: git status --porcelain=v1 -uall trên toàn bộ prototype/phase-2/
                     batch-01/, batch-02/, batch-03/, batch-04/ returned empty (zero diff).
```

## 2. Semantic scope

```text
Target semantic slice: Review — causation trace + historical comparison + correction inspection
  (NAV-005 + SCR-008 + SCR-009 + VIEW-004) — resolved directly from ux-blueprint.md §5a NAV-005,
  §7.5 (SCR-008/SCR-009/VIEW-004 detailed spec), §11 STATE-002 row + its rationale note,
  use-case-workflow.md UC-016–UC-018 detailed block, decision.md/risk.md/execution-result.md/
  fill.md/position.md/replay-event.md.
Batch-selection rule application: NAV-005 + SCR-008 + SCR-009 + VIEW-004 authored as ONE coherent
  Review milestone (P2-PROTOTYPE-001, batch/milestone review, KHÔNG per-screen cycle riêng) —
  explicit instruction not to expand into Improve. SCR-010/VIEW-006/SCR-011/VIEW-005 explicitly
  excluded — Improve is represented only as a labelled "Deferred" placeholder (nav-button-
  existence/read-only-navigation-affordance only), same convention as Batch 01-04's own deferred
  stages.
Read-only inspection boundary (INV-1, critical): every element in SCR-008/SCR-009/VIEW-004 is
  read-only — no create/overwrite/correct/invalidate/promote/"apply correction"/"accept
  replacement"/"save reconstructed state" action exists anywhere.
```

## 3. Included IDs

```text
SCR:    SCR-008 (Decision → Position Lineage Trace), SCR-009 (Historical State Comparison)
VIEW:   VIEW-004 (Correction Inspection)
NAV:    NAV-005 (Review — fully represented, incl. required-context routing/read-only-inspection
        behavior per ux-blueprint.md §5a); NAV-001/002/003/004 (real links to Batch 01/02/03/04,
        not re-authored); NAV-006 (nav-button-existence/read-only-navigation-affordance only,
        substantive screen NOT authored)
FLOW:   (no new FLOW-XXX authored — UC-016/017/018 sit within FLOW-001's existing scope per
        use-case-workflow.md)
STATE:  STATE-002 (empty, cited at NAV-005 level per its own text — see traceability.md §3 for
        the explicit disclaimer distinguishing this from STATE-002's own narrower canonical
        catalogue row, which lists only SCR-004/SCR-005/SCR-007/SCR-011)
```

## 4. Covered UC IDs — substantive accounting (A/B/C taxonomy, kế thừa từ `../batch-01/traceability.md` §0, recomputed đầy đủ tại `traceability.md` §2)

```text
Batch-05-authored substantive (A, +3 mới, CANDIDATE — CHƯA independently verified): UC-016
  (SCR-008), UC-017 (SCR-009), UC-018 (VIEW-004).

Candidate cumulative A (18 of 21): UC-001..UC-015 (Batch 01+02+03+04, ĐÃ independently verified)
  + UC-016, UC-017, UC-018 (Batch 05, CANDIDATE — CHƯA independently verified, Review A +
  Independent Review B CHƯA thực hiện).

Candidate cumulative B (3 of 21, giảm từ 6 vì UC-016/017/018 promote lên A):
  UC-019, UC-020, UC-021.

Candidate cumulative C (0 of 21, không đổi):
  (rỗng).

Partition validation: |A|=18, |B|=3, |C|=0, tổng=21. A∩B=A∩C=B∩C=∅ (verify mechanically, xem
  traceability.md §2). Union = {UC-001..UC-021}, mỗi UC đúng một lần — KHÔNG thiếu, KHÔNG dư.

21-UC substantive completion progress: 18/21 (A only) — CANDIDATE (Batch 05's own Review A +
  Independent Review B CHƯA thực hiện tại transaction này). Last independently verified: 15/21
  (UC-001..015, Batch 01+02+03+04 baseline, mỗi batch đã qua đầy đủ Review A + Independent
  Review B).
```

## 5. Covered PR IDs (Batch 05 mới)

```text
PR-028, PR-004, PR-005 (SCR-008, UC-016)
PR-029 (SCR-009, UC-017)
PR-011, PR-030 (VIEW-004, UC-018)
PR-028, PR-029, PR-011, PR-030 (NAV-005)
```

## 6. Prototype artifact identities

```text
prototype/phase-2/batch-05/index.html         blob 6946e9524ce8f1e92436e78796f02db06c147675 (CURRENT — v1.0)
prototype/phase-2/batch-05/app.js              blob 547e763d8c5cdf62872512542b2204b820efbeb2 (CURRENT — v1.0)
prototype/phase-2/batch-05/styles.css          blob a3e7898e047a4b7d0f84506def01e442934d707e (CURRENT — v1.0)
prototype/phase-2/batch-05/traceability.md     blob a66982a13400c673f405d7ffc2b4d8b9fece4597 (CURRENT — v1.0)
prototype/phase-2/batch-05/batch-manifest.md   (this file — CURRENT, v1.0)
prototype/phase-2/batch-05/README.md           (CURRENT, v1.0)
```

## 7. Authority sources consumed (reference only, none modified)

```text
docs/product/ux-blueprint.md          (Package 0.3-C, Consolidated Stable) §5a NAV-005, §7.5
                                       SCR-008/SCR-009/VIEW-004, §11 STATE-002 row + rationale
docs/product/use-case-workflow.md     (Package 0.3-B, Consolidated Stable) UC-016, UC-017,
                                       UC-018 detailed block
docs/domain/decision.md               DecisionRecorded (supersedes_fact_ref, §11) + §6
                                       DecisionFactInvalidated (invalidated_fact_ref/
                                       invalidation_reason) — direct-predecessor-fact-targeting
docs/domain/trade-intent.md           Trade Intent identity (referenced, not redefined)
docs/domain/risk.md                   RiskEvaluation identity + correction-lineage pattern
                                       (referenced only, not separately fixtured)
docs/domain/execution-intent.md       Execution Intent identity (referenced, not redefined)
docs/domain/order.md                  Order identity (referenced, not redefined)
docs/domain/execution-result.md       §2 ExecutionResultComputation CORRECTION three-way
                                       linkage (referenced only, disclosed as out-of-scope for
                                       interactive demo); §11 PaperExecutionObservation has no
                                       correction lineage of its own
docs/domain/fill.md                   Fill identity + correction-lineage pattern (§25, referenced
                                       only, not separately fixtured)
docs/domain/position.md               §1 read_model / derived projection — no correction lineage
                                       (explicit boundary: no Position correction fact invented)
docs/domain/replay-event.md           §2 ReplayState(C) fold formula, no-look-ahead invariant
                                       (fact.recorded_time ≤ C.recorded_time)
docs/product/product-requirement.md   (Package 0.3-A, Consolidated Stable) PR-004/005/011/028/
                                       029/030
```

## 8. Known deferred surfaces / non-substantive UC (not a gap — explicit batch boundary, đúng A/B/C taxonomy)

```text
4 of 17 surfaces not yet substantively covered (17 total; 13 candidate substantive — SCR-001/
  VIEW-001/VIEW-002 Batch 01, SCR-002/VIEW-003 Batch 02, SCR-003/SCR-004/SCR-005 Batch 03,
  SCR-006/SCR-007 Batch 04, SCR-008/SCR-009/VIEW-004 Batch 05; 4 remaining: SCR-010, SCR-011,
  VIEW-005, VIEW-006) deferred: represented ONLY as read-only nav-bar/handoff affordance leading
  to a labelled "Deferred" placeholder — no substantive screen/view content for any of them.

3 of 21 UC NOT substantively covered (traceability.md §2 — B=3, C=0, KHÔNG collapsed thành một
  bucket, KHÔNG double-count):
  B — Partial/referenced (3): UC-019, UC-020, UC-021.
  C — Deferred/not yet represented (0): none.
```

## 9. I-11 — Secrets & Custody Isolation — bounded Phase-2 Access-control audit

```text
Authoritative Verification (Chapter 2 §I-11, NOT redefined here): Access-control audit.
Bounded Phase-2 interpretation (phase-2-dod.md §2/§4, same as Batch 01-04):
  (1) No credential-use capability established:      CONFIRMED — no code path in app.js/
                                                       index.html uses, stores, or transmits a
                                                       credential.
  (2) No credential input surface required
      or introduced:                                  CONFIRMED — no login/auth UI, no session
                                                       token, no permission gate, no <input>
                                                       element anywhere in index.html/app.js
                                                       (verified directly, grep clean).
  (3) No signing key / custody / backend integration
      exists:                                          CONFIRMED — static files only, no
                                                       fetch/XHR/WebSocket/axios/.ajax in app.js.
  (4) No real secret/credential used or required:      CONFIRMED — MOCK_ACCOUNT_CONTEXT/
                                                       MOCK_STRATEGY_CONTEXT/LINEAGE_FILLS/
                                                       MOCK_DECISION_CORRECTION/REPLAY_CURSORS
                                                       are hardcoded illustrative values.
Result: AUDIT PASS.
```

## 10. I-11 — secret-pattern scan (supporting evidence only, NOT a substitute for the audit)

```text
Command: grep -niE "api[_-]?key|secret|password|private[_-]?key|token|credential|apikey|
  auth[_-]?header|bearer" prototype/phase-2/batch-05/*.html *.css *.js
Result: zero match. Same clean pattern as Batch 01/02/03/04.
```

## 11. I-12 — Single Source of Truth — traceability/reconciliation result

```text
Full element-by-element mapping: prototype/phase-2/batch-05/traceability.md §3.
Result: PASS — every prototype element traces to an existing NAV/SCR/VIEW/STATE + UC + PR + exact
  ux-blueprint.md/use-case-workflow.md/Domain Contract section. Zero new UC/PR/domain concept
  originated (verified directly, traceability.md §4) — no generic universal correction schema,
  no Position correction fact, no Risk/execution/simulation/replay engine, no new entity/event.
```

## 12. Trigger B/C/D/E boundary confirmation (phase-2-dod.md §2/§4 — re-confirmed, not re-resolved)

```text
No authoritative executable implementation:  CONFIRMED — static HTML/CSS/vanilla JS, mock data
                                              only, no module-registry.yaml entry, no
                                              Replay/correction engine implemented (every
                                              lineage/cursor/correction value is a hardcoded
                                              deterministic fixture).
No registered runtime module/tier:            CONFIRMED.
Representation vs. authority (Trigger D):     Prototype REPRESENTS authoritative-class fact
                                              display (authority=authoritative labels on
                                              SCR-008/VIEW-004; a mixed authoritative/non-
                                              authoritative label pair on SCR-009) but every
                                              actual value remains mock/static/non-authoritative
                                              — no authoritative financial computation, no
                                              custody/security implementation, no production
                                              operational path.
No real backend:                              CONFIRMED — grep for fetch/XHR/WebSocket/axios/
                                              .ajax across app.js/index.html returned no match.
No production/operational deployment:         CONFIRMED — files exist only under prototype/,
                                              no deployment config/pipeline touches them.
No published API/database/event contract,
  no new Domain Contract, no migration:        CONFIRMED — no schema file, no contract
                                              definition authored.
Result: boundary preserved. Trigger B/C/D/E conclusions from phase-2-dod.md §2 remain valid for
  this batch — no re-resolution triggered.
```

## 13. Four Review invariants (batch-specific critical boundary)

```text
Full verification: prototype/phase-2/batch-05/traceability.md §5.
Summary: INV-1 (read-only) — no create/overwrite/correct/invalidate/promote action anywhere,
  verified by grep. INV-2 (downstream lineage vs. Decision explainability distinct) — two
  visually-separated evidence groups on SCR-008, never merged. INV-3 (historical comparison
  never repaints history) — SCR-009's reconstructed and recorded-at-cursor panels are the same
  object by construction; a correction after the cursor is disclosed in a separate panel, never
  altering the historical panel. INV-4 (correction inspection preserves both lineages) — VIEW-004
  unconditionally renders both the original fact and the invalidation+replacement fact, with an
  explicit supersedes_fact_ref binding.
```

## 14. LIVE boundary

```text
Live representation: static "Unauthorized" badge (STATE-027) in the global context bar,
  identical convention to Batch 01-04, always visible. No action/link/button anywhere leads
  toward a Live path. OQ-002 not touched, not resolved.
```

## 15. Domain/architecture boundary

```text
No new domain entity, no new state machine, no architecture change, no backend contract choice,
  no API/event/database schema, no reinterpretation of Decision/RiskEvaluation/ExecutionResult/
  Fill/Position/Replay semantics — verified directly: docs/domain/, docs/architecture/,
  docs/constitution/ untouched by this transaction. No Replay/correction engine invented — every
  SCR-008/SCR-009/VIEW-004 value is a hardcoded deterministic fixture (LINEAGE_FILLS/
  REPLAY_CURSORS/MOCK_DECISION_CORRECTION), never computed. No generic universal correction
  schema invented — VIEW-004 uses decision.md's own exact field names only. No Position
  correction fact invented.
```

## 16. Unresolved gaps

```text
None within this batch's scope. 4/17 surfaces not yet substantively covered (SCR-010, SCR-011,
  VIEW-005, VIEW-006) and 3/21 UC not substantively covered (3 partial/referenced — UC-019,
  UC-020, UC-021, matching §4's partition exactly) remain for later batches — the expected,
  planned state of a fifth milestone, not an unresolved defect.
```

## 17. Batch lifecycle / review state

```text
Status:            CANDIDATE — v1.0 authoring transaction. Review A + Independent Review B CHƯA
                    thực hiện. KHÔNG self-approved, KHÔNG READY_FOR_NEXT_PHASE2_BATCH verdict.

Review history (chronological, KHÔNG rewrite):
  (none yet — this is the initial authoring transaction)

CURRENT TRUTH (v1.0, authoring transaction, 2026-08-14):
  Review verdict:                 NONE — chưa qua Review A.
  Candidate Batch-05 contribution: +3/17 surfaces (SCR-008, SCR-009, VIEW-004); +3/21 candidate
                                 substantive UC (UC-016, UC-017, UC-018) — CHƯA independently
                                 verified.
  Candidate cumulative (Batch
    01+02+03+04+05):               13/17 surfaces; 18/21 candidate substantive UC.
  Last independently verified
    (Batch 01+02+03+04 baseline):  10/17 surfaces; 15/21 UC.
  Remaining (post-Batch-05
    candidate):                    4/17 surfaces; 3/21 UC not substantive (§8/§16).
  Batch lifecycle:                CANDIDATE.
  Next governed step:              Review A on this v1.0 artifact (not authored by this
                                 transaction — per instruction, this executor does not author
                                 the next-task prompt).
```
