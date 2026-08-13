---
id: phase-2-batch-03-manifest
title: "Phase 2 Prototype — Batch 03 — Batch Manifest"
version: "1.1"
status: Candidate
owner: Product Owner
created_at: "2026-08-13"
---

# Phase 2 Prototype — Batch 03 — Batch Manifest

**Vai trò của tài liệu này:** batch-level evidence record cho Batch 03, đúng `phase-2-rules.md` `P2-PROTOTYPE-001` (review theo batch/milestone, KHÔNG per-screen governance cycle riêng). Batch 03 LÀ candidate/in-review — **KHÔNG self-approved** (chờ Review A + Independent Review B theo batch, đúng `P2-PROTOTYPE-001`).

**v1.1 — bounded correction (2026-08-13), Review A trên v1.0: `P2-B03-A-MAJ-01` (Major) + `P2-B03-A-MIN-01` (Minor) — đóng CẢ HAI tại transaction này.** `P2-B03-A-MAJ-01`: UC-008 Panel B chỉ render simulated economic evidence per Decision (bước 1), KHÔNG render ordered exposure/position progression theo thời gian xuyên suốt khoảng interval (bước 2, `use-case-workflow.md` UC-008 Main flow) — sửa bằng `app.js` `positionProgression()` helper + `.progression-table` mới, dẫn xuất deterministic từ `run.decisions` sẵn có (KHÔNG fixture/entity mới). `P2-B03-A-MIN-01`: current-state evidence (§4/§17) mô tả sai 5/17, 5/21 như "Batch 01 verified + Batch 02 candidate" — sửa: cả năm UC-001..005/SCR-001/VIEW-001/VIEW-002/SCR-002/VIEW-003 ĐÃ independently verified (Batch 01 Independent Review B + Batch 02 v1.3 Independent bounded Review B, cả hai verdict `READY_FOR_NEXT_PHASE2_BATCH`), KHÔNG còn hedge Batch 02 là "candidate." Minh bạch: ghi nhận chính thức verdict Batch 02 vào `batch-02/batch-manifest.md`'s own §17 VẪN LÀ một governed transaction riêng, CHƯA issue — batch-02's own file KHÔNG bị sửa bởi transaction này. Blob mới: `app.js`; `styles.css`; `traceability.md` v1.1; `README.md` (fixed stale "§16" cross-reference → §17, incidental — xem §6 cho tất cả blob). `index.html` KHÔNG đổi. KHÔNG đổi A/B/C partition, KHÔNG surface mới, KHÔNG UC/PR/domain concept mới. Batch VẪN `CANDIDATE`, KHÔNG self-approved.

## 1. Batch identity

```text
Batch:              Phase 2 — Batch 03 (Backtest setup + run detail + run comparison)
Phase:               Phase 2 — Product Prototype (AUTHORIZED TO BEGIN)
Authoritative DoD:   docs/phase-dod/phase-2-dod.md v0.3, status Approved,
                     post-acceptance blob de399900a93c7ec7ee64577093513de1643ebb33
Status:              CANDIDATE — chờ Review A + Independent Review B (batch-level,
                     P2-PROTOTYPE-001)
Created:             2026-08-13
Depends on (real,
  read-only link,
  KHÔNG modified):    prototype/phase-2/batch-01/ — READY_FOR_NEXT_PHASE2_BATCH (Independent
                     Review B verdict), CANDIDATE lifecycle, untouched by this transaction.
                     prototype/phase-2/batch-02/ — READY_FOR_NEXT_PHASE2_BATCH (Independent
                     bounded Review B verdict on v1.3, task-relayed baseline — xem §4 cho nguồn
                     đầy đủ; ghi nhận chính thức vào batch-02's own file VẪN LÀ transaction
                     riêng, CHƯA issue), CANDIDATE lifecycle, untouched by this transaction.
                     Verified: git diff --quiet trên toàn bộ prototype/phase-2/batch-01/ VÀ
                     prototype/phase-2/batch-02/.
```

## 2. Semantic scope

```text
Target semantic slice: Backtest setup + run detail + run comparison (NAV-003 + SCR-003 + SCR-004
  + SCR-005) — resolved directly from ux-blueprint.md §5a NAV-003, §7.3 (SCR-003/SCR-004/SCR-005
  detailed spec), §11 (STATE-001/002/004/005/009/010), use-case-workflow.md UC-006–UC-010
  detailed block (v0.6, đóng P03B-V05-B-MAJ-01's causal-direction fix), decision.md §5e/§10,
  risk.md §1.
Batch-selection rule application: NAV-003 + SCR-003 + SCR-004 + SCR-005 authored as ONE coherent
  Backtest milestone (P2-PROTOTYPE-001, batch/milestone review, KHÔNG per-screen cycle riêng) —
  explicit instruction not to split into separate governance cycles. SCR-006/SCR-007 (Paper)
  explicitly excluded. SCR-011 (Strategy Definition Version Comparison) explicitly excluded
  despite SCR-005's own "Exit points" pointing toward it — represented as a navigation
  affordance to a deferred placeholder only, per the instruction not to author SCR-011
  substantively.
```

## 3. Included IDs

```text
SCR:    SCR-003 (Backtest Run Setup), SCR-004 (Backtest Run Detail), SCR-005 (Backtest Run
        Comparison)
VIEW:   (none new)
NAV:    NAV-003 (Backtest — fully represented, incl. precondition-gate/read-only-inspection
        behavior per ux-blueprint.md §5a); NAV-001 (real link to Batch 01, not re-authored);
        NAV-002 (real link to Batch 02, not re-authored); NAV-004..NAV-006 (nav-button-
        existence/read-only-navigation-affordance only, substantive screens NOT authored)
FLOW:   (no new FLOW-XXX authored — SCR-003/004/005 sit within FLOW-001's existing scope
        ("UC-006 → FLOW-001, NAV-003, SCR-003..."), and UC-009/UC-010 additionally within
        FLOW-003's existing scope (Backtest → Paper judgment gate, ux-blueprint.md §8) —
        Batch 03 does NOT author any part of FLOW-003's SCR-006-facing half, does NOT redefine
        either FLOW, already Consolidated Stable)
STATE:  STATE-001 (loading, cited at SCR-003), STATE-002 (empty, SCR-004/SCR-005), STATE-004
        (cited at NAV-003 level, distinction from its own catalogue "VIEW-001" applicability
        preserved explicitly), STATE-005 (missing historical evidence), STATE-009 (Backtest
        evidence insufficient), STATE-010 (Backtest run identity unresolved)
```

## 4. Covered UC IDs — substantive accounting (A/B/C taxonomy, kế thừa từ `../batch-01/traceability.md` §0, recomputed đầy đủ tại `traceability.md` §2)

```text
Batch-03-authored substantive (A, +5 mới): UC-006 (SCR-003), UC-007 (SCR-004 Panel A), UC-008
  (SCR-004 Panel B), UC-009 (SCR-004 Panel C), UC-010 (SCR-005).

Cumulative A (10 of 21): UC-001, UC-002, UC-003, UC-004, UC-005 (Batch 01+02, ĐÃ independently
  verified — v1.1, đóng `P2-B03-A-MIN-01`, xem dưới) + UC-006, UC-007, UC-008, UC-009, UC-010
  (Batch 03, candidate — CHƯA independently verified).

Cumulative B (8 of 21, giảm từ 9 vì UC-006 promote lên A):
  UC-011, UC-015, UC-016, UC-017, UC-018, UC-019, UC-020, UC-021.

Cumulative C (3 of 21, giảm từ 7 vì UC-007/008/009/010 promote lên A):
  UC-012, UC-013, UC-014.

Partition validation: |A|=10, |B|=8, |C|=3, tổng=21. A∩B=A∩C=B∩C=∅ (verify mechanically, xem
  traceability.md §2). Union = {UC-001..UC-021}, mỗi UC đúng một lần — KHÔNG thiếu, KHÔNG dư.

21-UC substantive completion progress: candidate cumulative 10/21 (A only) — Batch 03's own +5
  (UC-006..010) CHƯA independently verified tại transaction này (chờ Review A + Independent
  Review B trên Batch 03). Last INDEPENDENTLY VERIFIED progress 5/21 (UC-001..005 — Batch 01
  Independent Review B `READY_FOR_NEXT_PHASE2_BATCH` + Batch 02 v1.3 Independent bounded
  Review B `READY_FOR_NEXT_PHASE2_BATCH`, v1.1 đóng `P2-B03-A-MIN-01` — KHÔNG còn mô tả
  Batch 02's phần này là "candidate").
```

## 5. Covered PR IDs (Batch 03 mới)

```text
PR-021, PR-022, PR-023 (SCR-003, UC-006)
PR-004, PR-005, PR-009, PR-021 (SCR-004 Panel A, UC-007)
PR-033 (SCR-004 Panel B, UC-008)
PR-034, PR-022 (SCR-004 Panel C, UC-009)
PR-034 (SCR-005, UC-010)
```

## 6. Prototype artifact identities

```text
prototype/phase-2/batch-03/index.html         blob 0c3b3601f3d89d712b09ba7950b478503e9cc197 (unchanged since v1.0)
prototype/phase-2/batch-03/app.js              blob a33f969724e18ae4ad13906f9076ec19a2c00706 (CURRENT — v1.1, đóng P2-B03-A-MAJ-01; historical pre-fix blob 9ddc87dd833b10e048f5d04142afa08325b74839, superseded)
prototype/phase-2/batch-03/styles.css          blob af973c0ad6e46dc7d66bb032af015bb6da3fb2ed (CURRENT — v1.1, thêm .progression-table class, presentation-only; historical pre-fix blob 92e2dd485b496c50737f2f7639ea1a58abc6c590, superseded)
prototype/phase-2/batch-03/traceability.md     blob 06d18b66f420e3f5f11603568837843cff0184d7 (CURRENT — v1.1, đóng P2-B03-A-MAJ-01 + P2-B03-A-MIN-01; historical v1.0 blob 3406b6de95f96a5fdf3045f7d49ede329f9d1cef, superseded)
prototype/phase-2/batch-03/README.md           blob 482420c661a347a93d327319c8de91c338b643ca (CURRENT — v1.1, fixed stale "§16" cross-reference to correct §17; historical pre-fix blob 369453dad6d00811a33db31243f1cab036f70d8c, superseded)
```

## 7. Authority sources consumed (reference only, none modified)

```text
docs/product/ux-blueprint.md          (Package 0.3-C, Consolidated Stable) §5a NAV-003, §7.3
                                       SCR-003/SCR-004/SCR-005, §8 FLOW-001/FLOW-003 (existing
                                       scope only), §11 STATE-001/002/004/005/009/010
docs/product/use-case-workflow.md     (Package 0.3-B, Consolidated Stable, v0.6, đóng
                                       P03B-V05-B-MAJ-01) UC-006, UC-007, UC-008, UC-009, UC-010
                                       detailed block
docs/domain/decision.md               §5e/§9/§10 (result enum LONG/SHORT/NO_ACTION; NO_ACTION →
                                       zero Trade Intent)
docs/domain/risk.md                   §1 (RiskEvaluation evaluates a Trade Intent, which only
                                       exists AFTER a LONG/SHORT Decision — causal direction
                                       boundary)
docs/domain/strategy.md               (Strategy Definition Version/Strategy Instance vocabulary
                                       reference only)
docs/product/product-requirement.md   (Package 0.3-A, Consolidated Stable) PR-004/005/009/021/
                                       022/023/033/034
docs/domain/trade-intent.md, execution-intent.md, order.md, execution-result.md, fill.md,
  position.md (vocabulary reference only — no schema/field authored; referenced ONLY to define
  the boundary of what is NOT created/reused by Backtest)
```

## 8. Known deferred surfaces / non-substantive UC (not a gap — explicit batch boundary, đúng A/B/C taxonomy)

```text
9 of 17 surfaces not yet substantively covered (17 total; 8 candidate substantive — SCR-001/
  VIEW-001/VIEW-002 Batch 01, SCR-002/VIEW-003 Batch 02, SCR-003/SCR-004/SCR-005 Batch 03; 9
  remaining: SCR-006..SCR-011 = 6 + VIEW-004..VIEW-006 = 3 = 9) deferred: represented ONLY as
  read-only nav-bar/handoff affordance leading to a labelled "Deferred" or "not authored"
  placeholder — no substantive screen/view content for any of them.

11 of 21 UC NOT substantively covered (traceability.md §2 — B=8, C=3, KHÔNG collapsed thành một
  bucket, KHÔNG double-count):
  B — Partial/referenced (8): UC-011, UC-015, UC-016, UC-017, UC-018, UC-019, UC-020, UC-021.
  C — Deferred/not yet represented (3): UC-012, UC-013, UC-014.
```

## 9. I-11 — Secrets & Custody Isolation — bounded Phase-2 Access-control audit

```text
Authoritative Verification (Chapter 2 §I-11, NOT redefined here): Access-control audit.
Bounded Phase-2 interpretation (phase-2-dod.md §2/§4, same as Batch 01/02):
  (1) No credential-use capability established:      CONFIRMED — no code path in app.js/
                                                       index.html uses, stores, or transmits a
                                                       credential.
  (2) No credential access-control surface required
      or introduced:                                  CONFIRMED — no login/auth UI, no session
                                                       token, no permission gate.
  (3) No backend/custody/signing integration exists:   CONFIRMED — static files only, no
                                                       fetch/XHR/WebSocket/axios/.ajax in app.js.
  (4) No real secret/credential used or required:      CONFIRMED — MOCK_STRATEGY_CONTEXT/
                                                       MOCK_INTERVALS/seedRuns() are hardcoded
                                                       illustrative values.
Result: AUDIT PASS.
```

## 10. I-11 — secret-pattern scan (supporting evidence only, NOT a substitute for the audit)

```text
Command: grep -niE "api[_-]?key|secret|password|private[_-]?key|token|credential|apikey|
  auth[_-]?header|bearer" prototype/phase-2/batch-03/*.html *.css *.js
Result (re-run post-v1.1 correction): one match, app.js:5 — inside the file-header comment
  explicitly disclaiming credentials. No actual credential-like value found. Same clean pattern
  as Batch 01/02.
```

## 11. I-12 — Single Source of Truth — traceability/reconciliation result

```text
Full element-by-element mapping: prototype/phase-2/batch-03/traceability.md §3.
Result: PASS — every prototype element traces to an existing SCR/VIEW/NAV/FLOW/STATE + UC + PR +
  exact ux-blueprint.md/use-case-workflow.md/decision.md/risk.md section. Zero new UC/PR/domain
  concept originated (verified directly, traceability.md §4) — no BacktestOrder/
  BacktestExecutionResult/BacktestFill/BacktestPosition entity, no simulation/Decision/Risk
  engine, no fee/slippage/accounting/PnL formula, no KPI threshold.
```

## 12. Trigger B/C/D/E boundary confirmation (phase-2-dod.md §2/§4 — re-confirmed, not re-resolved)

```text
No authoritative executable implementation:  CONFIRMED — static HTML/CSS/vanilla JS, mock data
                                              only, no module-registry.yaml entry, no simulation/
                                              Decision/Risk engine implemented (every Decision/
                                              RiskEvaluation/exposure-change value is a hardcoded
                                              deterministic fixture).
No registered runtime module:                 CONFIRMED.
No authoritative financial data:              CONFIRMED — all run/decision/evidence values
                                              hardcoded and labelled "illustrative"/"non-
                                              authoritative"/"simulated."
No real backend:                              CONFIRMED — grep for fetch/XHR/WebSocket/axios/
                                              .ajax across app.js/index.html returned no match.
No production/operational deployment:         CONFIRMED — files exist only under prototype/,
                                              no deployment config/pipeline touches them.
No published API/database/event contract:     CONFIRMED — no schema file, no contract
                                              definition authored; no BacktestOrder/
                                              BacktestExecutionResult/BacktestFill/
                                              BacktestPosition entity.
No migration:                                 CONFIRMED — not applicable.
Result: boundary preserved. Trigger B/C/D/E conclusions from phase-2-dod.md §2 remain valid for
  this batch — no re-resolution triggered.
```

## 13. Backtest/Paper authority separation (batch-specific critical boundary)

```text
Full verification: prototype/phase-2/batch-03/traceability.md §5.
Summary: no PAPER Order/ExecutionResult/Fill/Position created or reused anywhere; no
  BacktestFill/BacktestPosition/BacktestExecutionResult entity defined; no action resembling
  "execute in Paper"/"promote to Paper"/"convert to Paper Decision"/"reuse as PAPER Fill/
  Position." SCR-004's only forward exit is SCR-005 (Backtest); the global nav's "Paper" item
  remains an unchanged read-only deferred placeholder, same convention as Batch 01/02. FLOW-003
  (Backtest → Paper judgment gate, Consolidated Stable) is NOT modified and its SCR-006-facing
  half is NOT authored here.
```

## 14. LIVE boundary

```text
Live representation: static "Unauthorized" badge (STATE-027) in the global context bar,
  identical convention to Batch 01/02, always visible. No action/link/button anywhere leads
  toward a Live path. OQ-002 not touched, not resolved.
```

## 15. Domain/architecture boundary

```text
No new domain entity, no new state machine, no architecture change, no backend contract choice,
  no API/event/database schema, no reinterpretation of Decision/Risk/Execution semantics --
  verified directly: docs/domain/, docs/architecture/, docs/constitution/ untouched by this
  transaction. No simulation/Decision/Risk engine invented -- every SCR-004/SCR-005 value is a
  hardcoded deterministic fixture (seedRuns()/decision() helper), never computed from real
  market/domain logic. No fee/slippage/accounting/PnL formula, no KPI threshold/target/aggregate
  score defined (OQ-003 remains unresolved, disclosed explicitly at the evaluable-result panel).
```

## 16. Unresolved gaps

```text
None within this batch's scope. 9/17 surfaces not yet substantively covered (SCR-006..SCR-011 = 6
  + VIEW-004..VIEW-006 = 3) and 11/21 UC not substantively covered (8 partial/referenced —
  UC-011, UC-015, UC-016, UC-017, UC-018, UC-019, UC-020, UC-021 + 3 deferred — UC-012, UC-013,
  UC-014, matching §4's partition exactly) remain for later batches -- the expected, planned
  state of a third milestone, not an unresolved defect.
```

## 17. Batch lifecycle / review state

```text
Status:            CANDIDATE — corrected (v1.1 app.js/styles.css/traceability.md), NOT
                    self-approved.

Review history:
  Review A (v1.0):                     P2-B03-A-MAJ-01 (UC-008 progression missing) + P2-B03-A-
                                       MIN-01 (stale last-verified provenance) found,
                                       REVISION_REQUIRED.
  v1.1 (transaction này):               đóng CẢ HAI tại transaction này.

Progress — BA trạng thái tách biệt, KHÔNG conflate:
  Candidate (Batch 03's own contribution, CHƯA verified):
    17-surface cumulative:              8/17 (5/17 Batch 01+02, independently verified + 3/17
                                        Batch 03: SCR-003+SCR-004+SCR-005, candidate).
    21-UC substantive cumulative:        10/21 (5/21 Batch 01+02, independently verified + 5/21
                                        Batch 03: UC-006..010, candidate).

  Last INDEPENDENTLY VERIFIED (v1.1, đóng P2-B03-A-MIN-01 — sửa provenance):
    17-surface:                          5/17 (SCR-001/VIEW-001/VIEW-002 — Batch 01 Independent
                                        Review B verdict READY_FOR_NEXT_PHASE2_BATCH + SCR-002/
                                        VIEW-003 — Batch 02 v1.3 Independent bounded Review B
                                        verdict READY_FOR_NEXT_PHASE2_BATCH — cả năm ĐÃ verified,
                                        KHÔNG còn "candidate"). Nguồn: task-relayed baseline cho
                                        Batch 03 authoring transaction gốc (docs/CHANGELOG.md's
                                        Batch-03 Baseline block). Minh bạch: ghi nhận chính thức
                                        vào batch-02/batch-manifest.md's own §17 VẪN LÀ governed
                                        transaction riêng, CHƯA issue.
    21-UC substantive:                    5/21 (cùng nguồn).

Next step:          Bounded Review A re-review + Independent bounded Review B on this v1.1
                     Batch 03 candidate (one coherent Backtest milestone, per P2-PROTOTYPE-001)
                     — a separate governed transaction.
```
