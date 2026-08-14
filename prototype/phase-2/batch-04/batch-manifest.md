---
id: phase-2-batch-04-manifest
title: "Phase 2 Prototype — Batch 04 — Batch Manifest"
version: "1.0"
status: Candidate
owner: Product Owner
created_at: "2026-08-14"
---

# Phase 2 Prototype — Batch 04 — Batch Manifest

**Vai trò của tài liệu này:** batch-level evidence record cho Batch 04, đúng `phase-2-rules.md` `P2-PROTOTYPE-001` (review theo batch/milestone, KHÔNG per-screen governance cycle riêng). Batch 04 LÀ candidate/in-review — **KHÔNG self-approved** (chờ Review A + Independent Review B theo batch, đúng `P2-PROTOTYPE-001`).

## 1. Batch identity

```text
Batch:              Phase 2 — Batch 04 (Paper initiation + execution evidence/detail)
Phase:               Phase 2 — Product Prototype (AUTHORIZED TO BEGIN)
Authoritative DoD:   docs/phase-dod/phase-2-dod.md v0.3, status Approved,
                     post-acceptance blob de399900a93c7ec7ee64577093513de1643ebb33
Status:              CANDIDATE — chờ Review A + Independent Review B (batch-level,
                     P2-PROTOTYPE-001)
Created:             2026-08-14
Depends on (real,
  read-only link,
  KHÔNG modified):    prototype/phase-2/batch-01/ — CANDIDATE, review COMPLETE, verdict
                     READY_FOR_NEXT_PHASE2_BATCH, untouched by this transaction.
                     prototype/phase-2/batch-02/ — CANDIDATE, review COMPLETE, verdict
                     READY_FOR_NEXT_PHASE2_BATCH, untouched by this transaction.
                     prototype/phase-2/batch-03/ — CANDIDATE, review COMPLETE, verdict
                     READY_FOR_NEXT_PHASE2_BATCH, untouched by this transaction.
                     Verified: git diff --quiet trên toàn bộ prototype/phase-2/batch-01/,
                     prototype/phase-2/batch-02/, prototype/phase-2/batch-03/.
```

## 2. Semantic scope

```text
Target semantic slice: PAPER initiation + execution evidence/detail (NAV-004 + SCR-006 + SCR-007)
  — resolved directly from ux-blueprint.md §5a NAV-004, §7.4 (SCR-006/SCR-007 detailed spec),
  §11 (STATE-002/003/011/013/014/015/016/017/018/019/020/021/028/029), use-case-workflow.md
  UC-011–UC-015 detailed block, decision.md/trade-intent.md/risk.md/execution-intent.md/
  order.md/execution-result.md/fill.md/position.md/strategy.md.
Batch-selection rule application: NAV-004 + SCR-006 + SCR-007 authored as ONE coherent PAPER
  milestone (P2-PROTOTYPE-001, batch/milestone review, KHÔNG per-screen cycle riêng) — explicit
  instruction not to expand into Review/Improve. SCR-008/SCR-009/VIEW-004/SCR-010/VIEW-006/
  SCR-011/VIEW-005 explicitly excluded — SCR-007's own "Exit points" pointing toward SCR-008
  represented as a navigation affordance to a deferred placeholder only.
```

## 3. Included IDs

```text
SCR:    SCR-006 (Paper Execution Initiation), SCR-007 (Paper Order/Execution Detail)
VIEW:   (none new — VIEW-001 represented only via a bounded Paper-local pin fixture, NOT
        re-authored as a new surface)
NAV:    NAV-004 (Paper — fully represented, incl. four distinct precondition-blocked causes/
        read-only-inspection behavior per ux-blueprint.md §5a); NAV-001/002/003 (real links to
        Batch 01/02/03, not re-authored); NAV-005/006 (nav-button-existence/read-only-
        navigation-affordance only, substantive screens NOT authored)
FLOW:   (no new FLOW-XXX authored — UC-011 sits within FLOW-001's existing scope per
        use-case-workflow.md; §9 "Backtest → Paper handoff" judgment-gate framing preserved,
        NOT re-authored as a new FLOW)
STATE:  STATE-002 (empty, SCR-007), STATE-003 (invalid Account/Instrument/Venue), STATE-011
        (PAPER Decision lineage unavailable), STATE-013 (Risk REJECTED), STATE-014 (Risk
        NON_EVALUABLE), STATE-015 (ExecutionResult EXECUTED), STATE-016 (ExecutionResult
        NOT_EXECUTED), STATE-017 (Fill absent), STATE-018 (Position FLAT), STATE-019 (Position
        LONG), STATE-020 (Position SHORT), STATE-021 (Position NON_EVALUABLE), STATE-028 (Paper
        Strategy Instance not selected), STATE-029 (Paper Strategy Instance selected but not
        pinned)
```

## 4. Covered UC IDs — substantive accounting (A/B/C taxonomy, kế thừa từ `../batch-01/traceability.md` §0, recomputed đầy đủ tại `traceability.md` §2)

```text
Batch-04-authored substantive (A, +5 mới): UC-011 (SCR-006), UC-012 (SCR-007 ExecutionResult),
  UC-013 (SCR-007 Fill), UC-014 (SCR-007 Position), UC-015 (SCR-007 No-real-exchange).

Cumulative A (15 of 21): UC-001..UC-010 (Batch 01+02+03, independently verified) + UC-011,
  UC-012, UC-013, UC-014, UC-015 (Batch 04, candidate — CHƯA independently verified).

Cumulative B (6 of 21, giảm từ 8 vì UC-011/UC-015 promote lên A):
  UC-016, UC-017, UC-018, UC-019, UC-020, UC-021.

Cumulative C (0 of 21, giảm từ 3 vì UC-012/013/014 promote lên A):
  (rỗng — mọi UC còn lại đã ở hạng A hoặc B).

Partition validation: |A|=15, |B|=6, |C|=0, tổng=21. A∩B=A∩C=B∩C=∅ (verify mechanically, xem
  traceability.md §2). Union = {UC-001..UC-021}, mỗi UC đúng một lần — KHÔNG thiếu, KHÔNG dư.

21-UC substantive completion progress: candidate 15/21 (A only) — Batch 04's own +5
  (UC-011..015) CHƯA independently verified tại transaction này (chờ Review A + Independent
  Review B trên Batch 04). Last INDEPENDENTLY VERIFIED progress VẪN 10/21 (UC-001..010, Batch
  01+02+03 baseline).
```

## 5. Covered PR IDs (Batch 04 mới)

```text
PR-001, PR-006, PR-007, PR-016, PR-024 (NAV-004)
PR-004, PR-005, PR-006, PR-007, PR-014, PR-016, PR-024 (SCR-006, UC-011)
PR-007, PR-014, PR-024 (SCR-007 ExecutionResult, UC-012)
PR-025 (SCR-007 Fill, UC-013)
PR-026 (SCR-007 Position, UC-014)
PR-027 (SCR-007 No-real-exchange, UC-015)
```

## 6. Prototype artifact identities

```text
prototype/phase-2/batch-04/index.html         blob 2a9ccffef9b5728801fc09c8d1267f1e10584d46
prototype/phase-2/batch-04/app.js              blob 935d2ca00e9cbcdbb54674b876c264e2d57c5c15
prototype/phase-2/batch-04/styles.css          blob 0539d04fda7161798261c5418a0c804ff47e5015
prototype/phase-2/batch-04/traceability.md     blob 56902559106ca24184afe98919f58ad40b781af7
prototype/phase-2/batch-04/README.md           blob 0300f8943fbf907cd1d84b58f02e24dcb4055898
```

## 7. Authority sources consumed (reference only, none modified)

```text
docs/product/ux-blueprint.md          (Package 0.3-C, Consolidated Stable) §5a NAV-004, §7.4
                                       SCR-006/SCR-007, §11 STATE-002/003/011/013/014/015/016/
                                       017/018/019/020/021/028/029
docs/product/use-case-workflow.md     (Package 0.3-B, Consolidated Stable) UC-011, UC-012,
                                       UC-013, UC-014, UC-015 detailed block
docs/domain/decision.md               result enum LONG/SHORT/NO_ACTION (reused convention)
docs/domain/trade-intent.md           Trade Intent identity (referenced, not redefined)
docs/domain/risk.md                   §1 RiskEvaluation result APPROVED/REJECTED/NON_EVALUABLE,
                                       reason_code enum (INVALID_SIZING_INPUT,
                                       REQUIRED_EVIDENCE_UNAVAILABLE, etc.)
docs/domain/execution-intent.md       Execution Intent identity (referenced, not redefined)
docs/domain/order.md                  Order/OrderSubmissionRequest identity, environment=PAPER
                                       enum
docs/domain/execution-result.md       §1 PaperExecutionObservation (simulation_policy_ref/
                                       simulation_configuration_ref/simulation_build_ref/
                                       deterministic_input_ref), §8 ExecutionResult
                                       EXECUTED/NOT_EXECUTED
docs/domain/fill.md                   §1 Fill (fill_quantity/fill_price/price_currency, copied
                                       exactly from Observation)
docs/domain/position.md               §1/§2 Position read_model, projection_status
                                       EVALUABLE/NON_EVALUABLE, contributing_fill_refs
docs/domain/strategy.md               Strategy Definition Version/Strategy Instance vocabulary
                                       reference only
docs/product/product-requirement.md   (Package 0.3-A, Consolidated Stable) PR-001/004/005/006/
                                       007/014/016/024/025/026/027
```

## 8. Known deferred surfaces / non-substantive UC (not a gap — explicit batch boundary, đúng A/B/C taxonomy)

```text
7 of 17 surfaces not yet substantively covered (17 total; 10 candidate substantive — SCR-001/
  VIEW-001/VIEW-002 Batch 01, SCR-002/VIEW-003 Batch 02, SCR-003/SCR-004/SCR-005 Batch 03,
  SCR-006/SCR-007 Batch 04; 7 remaining: SCR-008/SCR-009/SCR-010/SCR-011 = 4 +
  VIEW-004/VIEW-005/VIEW-006 = 3 = 7) deferred: represented ONLY as read-only nav-bar/handoff
  affordance leading to a labelled "Deferred" or "not authored" placeholder — no substantive
  screen/view content for any of them.

6 of 21 UC NOT substantively covered (traceability.md §2 — B=6, C=0, KHÔNG collapsed thành một
  bucket, KHÔNG double-count):
  B — Partial/referenced (6): UC-016, UC-017, UC-018, UC-019, UC-020, UC-021.
  C — Deferred/not yet represented (0): none.
```

## 9. I-11 — Secrets & Custody Isolation — bounded Phase-2 Access-control audit

```text
Authoritative Verification (Chapter 2 §I-11, NOT redefined here): Access-control audit.
Bounded Phase-2 interpretation (phase-2-dod.md §2/§4, same as Batch 01/02/03):
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
                                                       MOCK_STRATEGY_CONTEXT/MOCK_PAPER_DECISION
                                                       are hardcoded illustrative values.
Result: AUDIT PASS.
```

## 10. I-11 — secret-pattern scan (supporting evidence only, NOT a substitute for the audit)

```text
Command: grep -niE "api[_-]?key|secret|password|private[_-]?key|token|credential|apikey|
  auth[_-]?header|bearer" prototype/phase-2/batch-04/*.html *.css *.js
Result: one match, app.js:5 — inside the file-header comment explicitly disclaiming
  credentials/signing/custody. No actual credential-like value found. Same clean pattern as
  Batch 01/02/03.
```

## 11. I-12 — Single Source of Truth — traceability/reconciliation result

```text
Full element-by-element mapping: prototype/phase-2/batch-04/traceability.md §3.
Result: PASS — every prototype element traces to an existing NAV/SCR/STATE + UC + PR + exact
  ux-blueprint.md/use-case-workflow.md/Domain Contract section. Zero new UC/PR/domain concept
  originated (verified directly, traceability.md §4) — no PaperSession entity, no new Order/
  RiskEvaluation/ExecutionResult/Fill/Position schema, no Risk/execution/simulation engine, no
  PAPER-context Decision creation mechanism defined.
```

## 12. Trigger B/C/D/E boundary confirmation (phase-2-dod.md §2/§4 — re-confirmed, not re-resolved)

```text
No authoritative executable implementation:  CONFIRMED — static HTML/CSS/vanilla JS, mock data
                                              only, no module-registry.yaml entry, no Risk/
                                              execution/simulation engine implemented (every
                                              RiskEvaluation/ExecutionResult/Fill value is a
                                              hardcoded deterministic fixture, QA-selected).
No registered runtime module/tier:            CONFIRMED.
Representation vs. authority (Trigger D):     Prototype REPRESENTS authoritative-class PAPER
                                              semantics (authority=authoritative PAPER labels)
                                              but every actual value remains mock/static/
                                              non-authoritative — no authoritative financial
                                              computation, no custody/security implementation,
                                              no production operational path, no performance
                                              boundary created.
No real backend:                              CONFIRMED — grep for fetch/XHR/WebSocket/axios/
                                              .ajax across app.js/index.html returned no match.
No production/operational deployment:         CONFIRMED — files exist only under prototype/,
                                              no deployment config/pipeline touches them.
No published API/database/event contract,
  no new Domain Contract, no migration:        CONFIRMED — no schema file, no contract
                                              definition authored; no PaperSession entity.
Result: boundary preserved. Trigger B/C/D/E conclusions from phase-2-dod.md §2 remain valid for
  this batch — no re-resolution triggered.
```

## 13. Five PAPER invariants (batch-specific critical boundary)

```text
Full verification: prototype/phase-2/batch-04/traceability.md §5.
Summary: INV-1 (PAPER Decision distinct) — no Execute-in-Paper/Promote/Convert/Clone action
  anywhere; no Backtest evidence reused as PAPER fact; PAPER Decision creation mechanism left
  undefined (deferred). INV-2 (intent only) — zero order-payload input fields exist (verified,
  grep clean for <input). INV-3 (upstream vs downstream) — visually and structurally separated,
  RiskEvaluation never in upstream group. INV-4 (exact branch truncation) — verified via
  buildExecutionChain()'s early returns. INV-5 (identity continuity + Position semantics) —
  single shared state object, Position never claimed authoritative, NON_EVALUABLE never
  guessed/collapsed.
```

## 14. LIVE boundary

```text
Live representation: static "Unauthorized" badge (STATE-027) in the global context bar,
  identical convention to Batch 01/02/03, always visible. No action/link/button anywhere leads
  toward a Live path. OQ-002 not touched, not resolved. OQ-003 not touched where applicable.
```

## 15. Domain/architecture boundary

```text
No new domain entity, no new state machine, no architecture change, no backend contract choice,
  no API/event/database schema, no reinterpretation of Decision/Risk/Execution/Order/Fill/
  Position semantics -- verified directly: docs/domain/, docs/architecture/, docs/constitution/
  untouched by this transaction. No Risk/execution/simulation engine invented -- every SCR-006/
  SCR-007 value is a hardcoded deterministic fixture (buildExecutionChain()/derivePosition()
  helpers), never computed from real market/domain logic. No fee/slippage/execution-model
  algorithm, no PaperSession entity, no order-sizing formula.
```

## 16. Unresolved gaps

```text
None within this batch's scope. 7/17 surfaces not yet substantively covered (SCR-008/009/010/
  011 = 4 + VIEW-004/005/006 = 3) and 6/21 UC not substantively covered (6 partial/referenced —
  UC-016, UC-017, UC-018, UC-019, UC-020, UC-021, matching §4's partition exactly) remain for
  later batches -- the expected, planned state of a fourth milestone, not an unresolved defect.
```

## 17. Batch lifecycle / review state

```text
Status:            CANDIDATE — authored (v1.0), NOT self-approved.

Progress — BA trạng thái tách biệt, KHÔNG conflate:
  Candidate (sau Batch 04 authoring, CHƯA verified):
    17-surface cumulative:              10/17 (8/17 Batch 01+02+03, independently verified +
                                        2/17 Batch 04: SCR-006+SCR-007, candidate).
    21-UC substantive cumulative:        15/21 (10/21 Batch 01+02+03, independently verified +
                                        5/21 Batch 04: UC-011..015, candidate).

  Last INDEPENDENTLY VERIFIED (Batch 01+02+03, mỗi batch tự nó qua đầy đủ Review A + Independent
    Review B, verdict READY_FOR_NEXT_PHASE2_BATCH):
    17-surface:                          8/17.
    21-UC substantive:                    10/21.

Next step:          Bounded Review A + Independent bounded Review B on this Batch 04 candidate
                     (one coherent PAPER milestone, per P2-PROTOTYPE-001) — a separate governed
                     transaction.
```
