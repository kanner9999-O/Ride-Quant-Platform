---
id: phase-2-batch-05-manifest
title: "Phase 2 Prototype — Batch 05 — Batch Manifest"
version: "1.2"
status: Candidate
owner: Product Owner
created_at: "2026-08-14"
---

# Phase 2 Prototype — Batch 05 — Batch Manifest

**Vai trò của tài liệu này:** batch-level evidence record cho Batch 05, đúng `phase-2-rules.md`
`P2-PROTOTYPE-001` (review theo batch/milestone, KHÔNG per-screen governance cycle riêng). Batch
05 đã qua đầy đủ Review A + Independent Review B trên v1.1 — verdict `READY_FOR_NEXT_PHASE2_BATCH`
— **NHƯNG lifecycle VẪN `CANDIDATE`** (`READY_FOR_NEXT_PHASE2_BATCH` LÀ completed-review verdict,
KHÔNG PHẢI lifecycle status; Product Owner CHƯA issue một lifecycle-promotion transaction riêng).

**v1.2 — deterministic bookkeeping reconciliation (2026-08-14), vai trò: `Phase 2 Prototype
Batch 05 Review-State Reconciliation Executor`, đúng `G-TXN-003`.** KHÔNG PHẢI lifecycle
transition, KHÔNG PHẢI prototype semantic correction — reconcile review-state/current-progress
bookkeeping tại role statement/§1/§4/§17 để khớp với governed review history ĐÃ hoàn tất (final
bounded Review A v1.1: `P2-B05-A-MAJ-01`/`P2-B05-A-MIN-01` cả hai CLOSED, new Blocker/Major/Minor
= 0/0/0, CLEAN — `READY_FOR_INDEPENDENT_REVIEW_B`; final Independent Review B v1.1: cùng hai
finding CLOSED, 0/0/0, verdict `READY_FOR_NEXT_PHASE2_BATCH`) — history này trước đây CHƯA được
ghi nhận vào tài liệu này, khiến role statement/§1/§4/§17 stale ("Independent Review B CHƯA thực
hiện," "candidate 18/21 CHƯA verified"). KHÔNG sửa nội dung semantic/artifact evidence (§2/§3/
§5–§16 giữ nguyên); KHÔNG sửa `index.html`/`app.js`/`styles.css` (blob KHÔNG đổi, verified
byte-identical). `traceability.md`/`README.md` sửa RIÊNG, tối thiểu, chỉ nơi có direct
current-state contradiction (xem hai tài liệu đó's own banner nếu có sửa). v1.0/v1.1
authoring/finding/correction history GIỮ NGUYÊN — KHÔNG rewrite như thể finding chưa từng tồn
tại (xem §17 "Review history," không thay đổi).

**v1.1 — bounded correction (2026-08-14), Review A trên v1.0: `P2-B05-A-MAJ-01` (Major) +
`P2-B05-A-MIN-01` (Minor) — đóng CẢ HAI tại transaction này.** `P2-B05-A-MAJ-01`: SCR-009's
correction-visible branch chỉ disclose invalidation, KHÔNG hiển thị later replacement/explicit
old→new difference — UC-017 KHÔNG thỏa mãn nếu KHÔNG đi tiếp VIEW-004. Sửa: thêm panel "Later-
correction comparison" (historical cursor, fact gốc KHÔNG đổi, invalidation đầy đủ, later
replacement `PD-101`/`LONG` với `supersedes_fact_ref=PD-100`, comparison-result `NO_ACTION → LONG`
gắn nhãn non-authoritative) — dùng LẠI `MOCK_DECISION_CORRECTION`, KHÔNG duplicate fixture,
historical panel gốc KHÔNG đổi (no repaint). `P2-B05-A-MIN-01`: SCR-008's exit button ngụ ý sai
cursor của lineage đang chọn được carry forward sang SCR-009. Sửa: đổi tên "Open Historical State
Comparison (SCR-009)" + disclosure tường minh cursor được chọn độc lập tại SCR-009. Blob mới:
`app.js`, `traceability.md`, `README.md` (incidental — mô tả SCR-009 cập nhật). `index.html`/
`styles.css` KHÔNG đổi. KHÔNG đổi A/B/C partition, KHÔNG surface mới, KHÔNG UC/PR/domain concept
mới, KHÔNG claim independently verified.

## 1. Batch identity

```text
Batch:              Phase 2 — Batch 05 (Review / causation / historical comparison / correction
                     inspection)
Phase:               Phase 2 — Product Prototype (AUTHORIZED TO BEGIN)
Authoritative DoD:   docs/phase-dod/phase-2-dod.md v0.3, status Approved,
                     post-acceptance blob de399900a93c7ec7ee64577093513de1643ebb33
Status:              CANDIDATE — review A + Independent Review B COMPLETE trên v1.1, verdict
                     READY_FOR_NEXT_PHASE2_BATCH (batch-level, P2-PROTOTYPE-001). Lifecycle VẪN
                     CANDIDATE — verdict review KHÔNG PHẢI lifecycle promotion.
Created:             2026-08-14 (v1.0); v1.1 bounded correction 2026-08-14; v1.2 bookkeeping
                     reconciliation 2026-08-14
Starting HEAD (v1.0): 988e3c368d452345329d27c47fa9d6963d31d3ff
Starting HEAD (v1.1): 22ab695bb34fcf09673237dae3365ab76fbf3242
Starting HEAD (v1.2): 8f24409c0befa5a1e399d09baabafd5930a5061d (verified via git rev-parse HEAD
                     trước khi sửa file, đúng G-VERIFY-001)
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
Batch-05-authored substantive (A, +3 mới, ĐÃ independently verified — final bounded Review A v1.1
  CLEAN + final Independent Review B v1.1 verdict READY_FOR_NEXT_PHASE2_BATCH): UC-016 (SCR-008),
  UC-017 (SCR-009), UC-018 (VIEW-004).

Cumulative A (18 of 21): UC-001..UC-015 (Batch 01+02+03+04, ĐÃ independently verified) + UC-016,
  UC-017, UC-018 (Batch 05, ĐÃ independently verified — v1.2 bookkeeping reconciliation, final
  Review A v1.1 CLEAN + final Independent Review B v1.1 verdict READY_FOR_NEXT_PHASE2_BATCH).

Cumulative B (3 of 21, giảm từ 6 vì UC-016/017/018 promote lên A):
  UC-019, UC-020, UC-021.

Cumulative C (0 of 21, không đổi):
  (rỗng).

Partition validation: |A|=18, |B|=3, |C|=0, tổng=21. A∩B=A∩C=B∩C=∅ (verify mechanically, xem
  traceability.md §2). Union = {UC-001..UC-021}, mỗi UC đúng một lần — KHÔNG thiếu, KHÔNG dư.

21-UC substantive completion progress: 18/21 (A only) — ĐÃ independently verified (v1.2
  bookkeeping reconciliation, 2026-08-14 — final bounded Review A v1.1 CLEAN (hai finding CLOSED)
  + final Independent Review B v1.1 verdict READY_FOR_NEXT_PHASE2_BATCH, 0/0/0). Lifecycle VẪN
  CANDIDATE (verdict review ≠ lifecycle promotion). Historical (TRƯỚC Batch 05's own review hoàn
  tất): last independently verified 15/21 (UC-001..015, Batch 01+02+03+04 baseline).
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
prototype/phase-2/batch-05/index.html         blob 6946e9524ce8f1e92436e78796f02db06c147675 (unchanged since v1.0; verified byte-identical at v1.2)
prototype/phase-2/batch-05/app.js              blob 287a1c8b999cf32fad4942fe8bcf037afae18e6b (unchanged since v1.1, đóng P2-B05-A-MAJ-01 + P2-B05-A-MIN-01; verified byte-identical at v1.2 — bookkeeping reconciliation touches docs only; historical v1.0 blob 547e763d8c5cdf62872512542b2204b820efbeb2, superseded)
prototype/phase-2/batch-05/styles.css          blob a3e7898e047a4b7d0f84506def01e442934d707e (unchanged since v1.0; verified byte-identical at v1.2)
prototype/phase-2/batch-05/traceability.md     blob e2eaa184d67c124009c68fe3fa71b34a58cd09a0 (CURRENT — v1.2, bookkeeping reconciliation, §2 review-progress conclusion updated to ĐÃ verified; historical v1.1 blob d2ac60bc547ded6016e66257d5d066ac42b915a0, v1.0 blob a66982a13400c673f405d7ffc2b4d8b9fece4597, both superseded)
prototype/phase-2/batch-05/batch-manifest.md   (this file — CURRENT, v1.2)
prototype/phase-2/batch-05/README.md           blob 990c6301e3d3b98dd62c947dfd6eb468e552fff5 (CURRENT — v1.2, fixed stale "not yet performed"/"candidate, not yet independently verified" claim; historical v1.1 blob e4363de91e45d454fc01a7472adbd8b6c24d6527, v1.0 unrecorded blob, both superseded)
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
Status:            CANDIDATE — v1.2 artifact candidate (bookkeeping reconciliation only,
                    behavior unchanged since v1.1), review COMPLETE, verdict
                    READY_FOR_NEXT_PHASE2_BATCH.

Review history (chronological, KHÔNG rewrite):
  Review A (v1.0):                     P2-B05-A-MAJ-01 (SCR-009 correction-visible branch thiếu
                                       later replacement/explicit old→new difference) +
                                       P2-B05-A-MIN-01 (SCR-008 exit button ngụ ý sai cursor được
                                       carry forward sang SCR-009) found, REVISION_REQUIRED.
  v1.1 bounded correction:              đóng CẢ HAI Review A finding.
  Final bounded Review A (v1.1,
    FINAL):                             P2-B05-A-MAJ-01/P2-B05-A-MIN-01 tất cả CLOSED; new
                                       Blocker/Major/Minor = 0/0/0; CLEAN —
                                       READY_FOR_INDEPENDENT_REVIEW_B.
  Final Independent Review B (v1.1,
    FINAL):                             cùng hai finding tất cả CLOSED; new Blocker/Major/Minor
                                       = 0/0/0; verdict READY_FOR_NEXT_PHASE2_BATCH.

CURRENT TRUTH (v1.2 bookkeeping reconciliation, 2026-08-14 — đóng gap "Independent Review B
  CHƯA thực hiện" trước đây, đúng G-TXN-003):
  Review verdict:                 READY_FOR_NEXT_PHASE2_BATCH (final, v1.1 artifact candidate —
                                 KHÔNG PHẢI Approved/Accepted/Complete lifecycle transition).
  Verified Batch-05 contribution: +3/17 surfaces (SCR-008, SCR-009, VIEW-004); +3/21 substantive
                                 UC (UC-016, UC-017, UC-018).
  Verified cumulative (Batch
    01+02+03+04+05):               13/17 surfaces; 18/21 substantive UC.
  Remaining:                      4/17 surfaces (SCR-010, SCR-011, VIEW-005, VIEW-006); 3/21 UC
                                 (UC-019, UC-020, UC-021) — §8/§16.
  Batch lifecycle:                CANDIDATE (unchanged — Product Owner CHƯA issue lifecycle-
                                 promotion transaction riêng cho Batch 05).
  Further Batch-05 correction/
    re-review pending:            NONE — review COMPLETE trên v1.1, KHÔNG bounded re-review nào
                                 chờ xử lý.
  Next governed step:              proceed to next Phase-2 prototype batch under
                                 `P2-PROTOTYPE-001` — not authored by this transaction, per
                                 instruction, this executor does not author the next-task prompt.
```
