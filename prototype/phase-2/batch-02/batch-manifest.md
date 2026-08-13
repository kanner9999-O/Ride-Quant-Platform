---
id: phase-2-batch-02-manifest
title: "Phase 2 Prototype — Batch 02 — Batch Manifest"
version: "1.1"
status: Candidate
owner: Product Owner
created_at: "2026-08-13"
---

# Phase 2 Prototype — Batch 02 — Batch Manifest

**Vai trò của tài liệu này:** batch-level evidence record cho Batch 02, đúng `phase-2-rules.md` `P2-PROTOTYPE-001` (review theo batch/milestone, KHÔNG per-screen governance cycle riêng). Batch 02 LÀ candidate/in-review — **KHÔNG self-approved** (chờ Review A + Independent Review B theo batch, đúng `P2-PROTOTYPE-001`).

**v1.1 — bounded correction (2026-08-13), đóng `P2-B02-A-MAJ-01` (Review A).** v1.0's §4 cumulative UC ledger KHÔNG PHẢI một valid partition — `UC-002` xuất hiện CẢ trong A LẪN B; `UC-009`/`UC-010` bị gọi B trong khi mô tả nói zero-reference; C ghi "9 of 21" nhưng liệt kê 10 UC; "5+7+9=21" do đó sai. Sửa: §4 viết lại — B recompute TỪ ĐẦU trực tiếp từ `ux-blueprint.md` §5a's NAV-003/004/005/006 UC traceability (loại UC-002/UC-004 vì đã A), kết quả A=5/B=9/C=7, tổng=21, ba set đôi một rời nhau (verify mechanically, xem `traceability.md` v1.1 §2). KHÔNG đổi Replay/parity behavior, KHÔNG surface mới, KHÔNG đổi 3/17→5/17 surface progress (surface accounting KHÔNG bị ảnh hưởng bởi finding này).

## 1. Batch identity

```text
Batch:              Phase 2 — Batch 02 (Replay reconstruction + optional parity verification)
Phase:               Phase 2 — Product Prototype (AUTHORIZED TO BEGIN)
Authoritative DoD:   docs/phase-dod/phase-2-dod.md v0.3, status Approved,
                     post-acceptance blob de399900a93c7ec7ee64577093513de1643ebb33
Status:              CANDIDATE — chờ Review A + Independent Review B (batch-level,
                     P2-PROTOTYPE-001)
Created:             2026-08-13
Depends on (real,
  read-only link,
  KHÔNG modified):    prototype/phase-2/batch-01/ — READY_FOR_NEXT_PHASE2_BATCH (Independent
                     Review B verdict), remains CANDIDATE lifecycle, untouched by this
                     transaction (verified: git diff --quiet trên toàn bộ prototype/phase-2/
                     batch-01/).
```

## 2. Semantic scope

```text
Target semantic slice: Replay reconstruction (SCR-002) + optional parity recomputation
  (VIEW-003) — resolved directly from ux-blueprint.md §7.2 (SCR-002/VIEW-003 detailed spec),
  §5a NAV-002, §11 (STATE-001/004/006/007/008/030), và decision.md §9a (Canonical Decision
  Semantic Representation/parity outcome model).
Batch-selection rule application: NAV-002 (Replay nav destination) + SCR-002 + VIEW-003 met the
  inclusion criteria (authoritative Replay slice; VIEW-003 explicitly an optional action FROM
  SCR-002 per its own "Entry points" spec, not a separate unrelated surface). Backtest
  (SCR-003/004/005) explicitly excluded despite NAV-003 existing as a nav-bar affordance. Review
  (SCR-009) explicitly excluded despite VIEW-003's MISMATCH handoff pointing toward it — the
  handoff is represented as a navigation affordance to a deferred placeholder only, per the
  instruction not to author SCR-009 substantively in Batch 02.
```

## 3. Included IDs

```text
SCR:    SCR-002 (Replay Cursor & Historical Reconstruction)
VIEW:   VIEW-003 (Parity Recomputation Result)
NAV:    NAV-002 (Replay — fully represented, incl. precondition-gate/read-only-inspection
        behavior per ux-blueprint.md §5a); NAV-001 (real link to Batch 01, not re-authored);
        NAV-003..NAV-006 (nav-button-existence/read-only-navigation-affordance only,
        substantive screens NOT authored)
FLOW:   (no new FLOW-XXX authored — SCR-002/VIEW-003 sit within FLOW-001's existing scope,
        "SCR-002 (Replay, UC-004) → [tuỳ chọn VIEW-003, UC-005]", ux-blueprint.md §8, already
        Consolidated Stable — Batch 02 does not redefine it)
STATE:  STATE-001 (loading), STATE-004 (cited at NAV-002 level, distinction from its own
        catalogue "VIEW-001" applicability preserved explicitly), STATE-006 (Replay reference
        unavailable), STATE-007 (parity match), STATE-008 (parity mismatch), STATE-030 (parity
        indeterminate)
```

## 4. Covered UC IDs — substantive accounting (A/B/C taxonomy, kế thừa từ `../batch-01/traceability.md` §0, recomputed đúng tại v1.1, đóng `P2-B02-A-MAJ-01`)

```text
Batch-02-authored substantive (A, +2 mới): UC-004 (SCR-002), UC-005 (VIEW-003).

Cumulative A (candidate, 5 of 21): UC-001, UC-002, UC-003 (Batch 01) + UC-004, UC-005 (Batch 02).
  UC-001/002/003 GIỮ NGUYÊN A dù Batch 02 tiêu thụ chúng LÀM prerequisite/incoming-context —
  KHÔNG hạ xuống B (một UC KHÔNG thể vừa A vừa B, đóng finding 1 của `P2-B02-A-MAJ-01`).

Cumulative B (9 of 21, recomputed TỪ ĐẦU trực tiếp từ ux-blueprint.md §5a — KHÔNG copy Batch
  01's set cũ, KHÔNG bao gồm UC-002/UC-004 vì đã A):
  UC-006 (NAV-003), UC-011 (NAV-004/WS-001/STATE-027), UC-015 (WS-001/STATE-027), UC-016/017/018
  (NAV-005 + VIEW-003 MISMATCH→Review handoff), UC-019/020/021 (NAV-006).

Cumulative C (7 of 21 — verify trực tiếp: KHÔNG element nào trong Batch 01/02 tham chiếu, kể cả
  UC-009/UC-010 dù cùng Backtest lifecycle stage với UC-006 — NAV-003's OWN citation CHỈ UC-002/
  UC-006, KHÔNG UC-009/UC-010):
  UC-007, UC-008, UC-009, UC-010, UC-012, UC-013, UC-014.

Partition validation: |A|=5, |B|=9, |C|=7, tổng=21. A∩B=A∩C=B∩C=∅ (verify mechanically, xem
  traceability.md v1.1 §2). Union = {UC-001..UC-021}, mỗi UC đúng một lần — KHÔNG thiếu, KHÔNG dư.

21-UC substantive completion progress: candidate 5/21 (A only) -- CHƯA independently verified
  tại transaction này (chờ Review A + Independent Review B trên Batch 02). Last INDEPENDENTLY
  VERIFIED progress VẪN 3/21 (Batch 01 only).
```

## 5. Covered PR IDs (Batch 02 mới)

```text
PR-008, PR-018, PR-020 (SCR-002)
PR-010, PR-019 (VIEW-003)
```

## 6. Prototype artifact identities

```text
prototype/phase-2/batch-02/index.html         blob c69502da70e32db07572848a795d74f67ecc838d
prototype/phase-2/batch-02/styles.css          blob bcd250d57cfb5b56e3558fbdbede0cca89cf1b82
prototype/phase-2/batch-02/app.js              blob 8f5fba218457b965dd2f9ecdc1576de9b61639a6
prototype/phase-2/batch-02/traceability.md     blob 61e7f2afe44f0d0795cbfbe98c3041d10d4fb425
```

## 7. Authority sources consumed (reference only, none modified)

```text
docs/product/ux-blueprint.md       (Package 0.3-C, Consolidated Stable) §5a NAV-002, §7.2
                                    SCR-002/VIEW-003, §8 FLOW-001 (existing scope only), §11
                                    STATE-001/004/006/007/008/030
docs/domain/decision.md            §9a.1-§9a.7 (Consolidated Stable, Canonical Decision
                                    Semantic Representation, nine pinned axes, MATCH/MISMATCH/
                                    INDETERMINATE outcome model, authority boundary)
docs/product/use-case-workflow.md  (Package 0.3-B, Consolidated Stable) UC-004, UC-005 (via
                                    ux-blueprint.md's inherited mapping)
docs/product/product-requirement.md (Package 0.3-A, Consolidated Stable) PR-008/010/018/019/020
docs/domain/replay-event.md, trade-intent.md, risk.md, execution-intent.md, order.md,
  execution-result.md, fill.md, position.md (vocabulary reference only — no schema/field
  authored)
```

## 8. Known deferred surfaces / non-substantive UC (not a gap — explicit batch boundary, đúng A/B/C taxonomy từ đầu — KHÔNG lặp lại `P2-B01-A-MIN-01`'s "deferred" collapse defect)

```text
13 of remaining 15 surfaces (relative to full 17: SCR-001/VIEW-001/VIEW-002 done at Batch 01,
  SCR-002/VIEW-003 done at Batch 02, SCR-003..SCR-011 + VIEW-004..VIEW-006 remain) deferred:
  represented ONLY as read-only nav-bar/handoff affordance leading to a labelled "Deferred" or
  "not authored" placeholder — no substantive screen/view content for any of them.

16 of 21 UC NOT substantively covered (§4 above — B=9, C=7, KHÔNG collapsed thành một bucket,
  KHÔNG double-count UC-002 vào A, đúng `P2-B02-A-MAJ-01` correction):
  B — Partial/referenced (9): UC-006, UC-011, UC-015, UC-016, UC-017, UC-018, UC-019, UC-020,
    UC-021.
  C — Deferred/not yet represented (7): UC-007, UC-008, UC-009, UC-010, UC-012, UC-013, UC-014.
```

## 9. I-11 — Secrets & Custody Isolation — bounded Phase-2 Access-control audit

```text
Authoritative Verification (Chapter 2 §I-11, NOT redefined here): Access-control audit.
Bounded Phase-2 interpretation (phase-2-dod.md §2/§4, same as Batch 01):
  (1) No credential-use capability established:      CONFIRMED — no code path in app.js/
                                                       index.html uses, stores, or transmits a
                                                       credential.
  (2) No credential access-control surface required
      or introduced:                                  CONFIRMED — no login/auth UI, no session
                                                       token, no permission gate.
  (3) No backend/custody/signing integration exists:   CONFIRMED — static files only, no
                                                       fetch/XHR/WebSocket in app.js.
  (4) No real secret/credential used or required:      CONFIRMED — MOCK_CURSORS/
                                                       MOCK_REPLAY_STATE/MOCK_REPRESENTATION are
                                                       hardcoded illustrative values.
Result: AUDIT PASS.
```

## 10. I-11 — secret-pattern scan (supporting evidence only, NOT a substitute for the audit)

```text
Command: grep -niE "api[_-]?key|secret|password|private[_-]?key|token|credential|apikey|
  auth[_-]?header|bearer" prototype/phase-2/batch-02/*.html *.css *.js
Result: one match, app.js:5 — inside a comment explicitly disclaiming credentials. No actual
  credential-like value found.
```

## 11. I-12 — Single Source of Truth — traceability/reconciliation result

```text
Full element-by-element mapping: prototype/phase-2/batch-02/traceability.md §3.
Result: PASS — every prototype element traces to an existing SCR/VIEW/NAV/FLOW/STATE + UC + PR
  + exact ux-blueprint.md/decision.md §9a section. Zero new UC/PR/domain concept originated
  (verified directly, traceability.md §4) — no Cursor entity, no ParityResult entity, no new
  Decision representation.
```

## 12. Trigger B/C/D/E boundary confirmation (phase-2-dod.md §2/§4 — re-confirmed, not re-resolved)

```text
No authoritative executable implementation:  CONFIRMED — static HTML/CSS/vanilla JS, mock data
                                              only, no module-registry.yaml entry, no replay/
                                              Decision/parity engine implemented (all outcomes
                                              demo-selected via QA panel).
No registered runtime module:                 CONFIRMED.
No authoritative financial data:              CONFIRMED — all lineage/Representation values
                                              hardcoded and labelled "illustrative"/demo.
No real backend:                              CONFIRMED — grep for fetch/XHR/WebSocket/axios/
                                              .ajax across app.js/index.html returned no match.
No production/operational deployment:         CONFIRMED — files exist only under prototype/,
                                              no deployment config/pipeline touches them.
No published API/database/event contract:     CONFIRMED — no schema file, no contract
                                              definition authored.
No migration:                                 CONFIRMED — not applicable.
Result: boundary preserved. Trigger B/C/D/E conclusions from phase-2-dod.md §2 remain valid for
  this batch — no re-resolution triggered.
```

## 13. LIVE boundary

```text
Live representation: static "Unauthorized" badge (STATE-027) in the global context bar,
  identical convention to Batch 01, always visible. No action/link/button anywhere leads toward
  a Live path. OQ-002 not touched, not resolved.
```

## 14. Domain/architecture boundary

```text
No new domain entity, no new state machine, no architecture change, no backend contract choice,
  no API/event/database schema, no reinterpretation of Decision/Risk/Execution semantics --
  verified directly: docs/domain/, docs/architecture/, docs/constitution/ untouched by this
  transaction. No parity/replay computation algorithm invented -- every VIEW-003 outcome is
  demo-selected via the QA panel, never computed from the illustrative lineage/Representation
  data. No missing-authoritative-decision gap encountered that required stopping an interaction.
```

## 15. Unresolved gaps

```text
None within this batch's scope. 13/15 remaining surfaces and 16/21 UC not substantively covered
  (7 partial/referenced + 9 deferred) remain for later batches -- the expected, planned state of
  a second milestone, not an unresolved defect.
```

## 16. Batch lifecycle / review state

```text
Status:            CANDIDATE — authored, NOT self-approved.

Candidate contribution (this transaction, CHƯA independently verified):
  17-surface cumulative:          5/17 (3/17 from Batch 01 + 2/17 from Batch 02).
  21-UC substantive cumulative:    5/21 (3/21 from Batch 01 + 2/21 from Batch 02).

Last INDEPENDENTLY VERIFIED cumulative progress (Independent Review B's verdict on Batch 01,
  READY_FOR_NEXT_PHASE2_BATCH — the authoritative number cho tới khi Batch 02 tự nó qua Review
  A/B):
  17-surface:                     3/17 (Batch 01 only).
  21-UC substantive:                3/21 (Batch 01 only).

Review A:           NOT YET PERFORMED (batch-level, P2-PROTOTYPE-001) trên Batch 02.
Independent
  Review B:          NOT YET PERFORMED trên Batch 02.
Next step:          Batch-level Review A + Independent Review B on this coherent Batch 02
                     milestone — a separate governed transaction, per this transaction's own
                     scope (authoring only).
```
