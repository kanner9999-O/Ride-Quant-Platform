---
id: phase-2-batch-02-traceability
title: "Phase 2 Prototype — Batch 02 — Traceability Artifact"
version: "1.0"
status: Candidate
owner: Product Owner
created_at: "2026-08-13"
---

# Phase 2 Prototype — Batch 02 — Traceability Artifact

**Vai trò của tài liệu này:** đây LÀ I-12 (Single Source of Truth) conformance evidence cho Batch 02, per `docs/phase-dod/phase-2-dod.md` §2's applicable Trigger A / I-12 requirement — mọi phần tử prototype trong batch này PHẢI trace được TRỰC TIẾP về đúng một hoặc nhiều `SCR-XXX`/`VIEW-XXX`/`NAV-XXX`/`FLOW-XXX`/`STATE-XXX` đã `Consolidated Stable` trong [`docs/product/ux-blueprint.md`](../../../docs/product/ux-blueprint.md) VÀ [`docs/domain/decision.md`](../../../docs/domain/decision.md) §9a, VÀ về đúng `UC-XXX`/`PR-XXX` đã tồn tại. Prototype LÀ derived representation — KHÔNG một UC/PR/domain concept nào originate tại đây. Áp dụng ĐÚNG taxonomy A/B/C đã establish tại `../batch-01/traceability.md` §0.

## 0. UC accounting taxonomy (kế thừa nguyên vẹn từ Batch 01, KHÔNG redefine)

```text
A. SUBSTANTIVELY COVERED — Batch tự author ĐỦ representation (screen/view + required context +
   primary/blocked states + exit behavior đúng ux-blueprint.md/decision.md §9a spec) để tính vào
   21-UC completion numerator (phase-2-dod.md §3).
B. PARTIAL / REFERENCED — UC xuất hiện qua global shell context, nav-button existence, handoff
   affordance, hay deferred-placeholder destination — KHÔNG đủ để tính vào numerator.
C. DEFERRED / NOT YET REPRESENTED — KHÔNG một element nào trong batch tham chiếu UC đó.
```

## 1. Batch-02 UC classification

| UC | Classification | Evidence / reason |
|---|---|---|
| UC-004 | **A — Substantive** | SCR-002 fully authored: NAV-002 precondition gate (Strategy Instance/verification), required context, cursor selection bound to prototype-local state, full lineage display (Decision→...→Position) at cursor, STATE-001/STATE-006 — matches `ux-blueprint.md` §7.2 SCR-002 spec. |
| UC-005 | **A — Substantive** | VIEW-003 fully authored: optional (never automatic) entry from SCR-002, recorded-vs-recomputed Canonical Decision Semantic Representation comparison, nine pinned axes, digest-definition-unresolved note, MATCH/MISMATCH/INDETERMINATE (STATE-007/008/030), MISMATCH→Review handoff, explicit absence of any promote/save/replace/ReplayDecision action — matches `ux-blueprint.md` §7.2 VIEW-003 spec + `decision.md` §9a.1–§9a.7. |
| UC-002 | **B — Partial/referenced** (unchanged from Batch 01) | Cited only as NAV-002's own "Strategy Instance đã pin (VIEW-001 → VIEW-002 PASSED, commit-gate)" required-context justification, represented in Batch 02 ONLY as simulated incoming context (QA panel), NOT as a re-implementation of VIEW-001/VIEW-002. |
| UC-001 | **A — Substantive** (already counted in Batch 01, NOT double-counted here) | SCR-001 fully authored in Batch 01 — Batch 02 only links to it (Research nav item), does not re-author it. |
| UC-003 | **A — Substantive** (already counted in Batch 01, NOT double-counted here) | VIEW-002 fully authored in Batch 01 — Batch 02 only references its PASSED/FAILED/INDETERMINATE outcome as simulated incoming context. |
| UC-006, UC-009, UC-010 | **B — Partial/referenced** | UC-006 (Backtest entry) referenced only via NAV-003 nav-button existence (deferred placeholder); UC-009/UC-010 not referenced by Batch 02 at all — see §4 for the full cumulative Phase-2 UC ledger. |
| UC-016..UC-018 | **B — Partial/referenced** (via NAV-005 nav-button + VIEW-003 MISMATCH handoff button existence) | The "Continue to Review" handoff button (MISMATCH outcome) and NAV-005's nav-button existence reference the Review destination without authoring SCR-008/SCR-009/VIEW-004's substantive behavior. |
| UC-019, UC-020, UC-021 | **B — Partial/referenced** (unchanged reason from Batch 01, NAV-006 nav-button existence only) | Same as Batch 01 — no change from this batch. |
| UC-011, UC-015 | **B — Partial/referenced** (unchanged from Batch 01) | STATE-027 global label + NAV-004 nav-button existence only — no change from this batch. |
| UC-007, UC-008, UC-012, UC-013, UC-014 | **C — Deferred** | Zero reference anywhere in Batch 01 or Batch 02. |

```text
Batch-02-authored substantive UC: UC-004, UC-005 (2 new).
Cumulative substantive UC after Batch 02 (candidate, chờ Review A/B): UC-001, UC-002... — xem §4
  dưới cho ledger đầy đủ, KHÔNG suy diễn từ bảng trên riêng lẻ.
```

## 2. Cumulative Phase-2 UC ledger (Batch 01 + Batch 02, candidate — KHÔNG independently verified tại transaction này)

```text
A — Substantively covered (candidate, 5 of 21):
  UC-001 (Batch 01, SCR-001), UC-002 (Batch 01, VIEW-001), UC-003 (Batch 01, VIEW-002),
  UC-004 (Batch 02, SCR-002), UC-005 (Batch 02, VIEW-003).

B — Partial/referenced (7 of 21, unchanged set from Batch 01 -- Batch 02 does not add or remove
  any B-category UC, it only adds evidence for existing B entries UC-002/UC-006/UC-011/UC-015/
  UC-019/UC-020/UC-021 without promoting any of them to A):
  UC-006, UC-011, UC-015, UC-019, UC-020, UC-021 (từ Batch 01, giữ nguyên) — UC-002 chuyển vai
  trò tham chiếu (trước: Batch 01's VIEW-001 commit-gate source; nay CŨNG: Batch 02's NAV-002
  precondition source) NHƯNG VẪN category B, KHÔNG PHẢI A (VIEW-001 KHÔNG được Batch 02
  re-author).

C — Deferred/not yet represented (9 of 21, giảm từ 11 vì UC-004/UC-005 chuyển từ C sang A):
  UC-007, UC-008, UC-009, UC-010, UC-012, UC-013, UC-014, UC-016, UC-017, UC-018.

Kiểm tra: 5 + 7(B, giữ nguyên set — UC-002 vẫn nằm trong 7 này) + 9(C) = 21. Đúng — B set KHÔNG
  đổi kích thước (vẫn 7 UC), CHỈ C giảm từ 11 xuống 9 vì hai UC chuyển sang A.

21-UC substantive completion progress (candidate): 5/21 -- CHỈ đếm hạng mục A, CHƯA independently
  verified (chờ Review A + Independent Review B trên Batch 02, đúng P2-PROTOTYPE-001).
```

## 3. Element-level traceability map

**Ghi chú:** cột "UC" liệt kê MỌI UC một element trace được về, kể cả hạng mục B — bảng này LÀ element-to-source mapping (I-12 reconciliation), KHÔNG PHẢI substantive-completion accounting. Dùng §0/§1/§2 phía trên cho substantive-completion accounting.

| Prototype element (file:selector) | UX Blueprint / Domain ID | UC | PR | Authoritative source section |
|---|---|---|---|---|
| `index.html` `#shell`/`#context-bar` (bounded subset, reused convention) | WS-001 | UC-011, UC-001/UC-011, UC-002/UC-011, UC-011/UC-015 | PR-002, PR-003, PR-001, PR-016, PR-027 | `ux-blueprint.md` §5 "WS-001" table (same authority as Batch 01, re-derived independently in this batch's own files) |
| `index.html` `#nav-bar [data-nav="NAV-001"]` (Research, real link to `../batch-01/index.html`) | NAV-001 | UC-001 | PR-003, PR-015, PR-017 | `ux-blueprint.md` §5a "NAV-001"; genuine navigation to Batch 01's already-authored SCR-001, NOT a new representation |
| `index.html` `#nav-bar [data-nav="NAV-002"]` (Replay, active) | NAV-002 | UC-002 (precondition), UC-004 | PR-001, PR-016, PR-008, PR-018, PR-020 | `ux-blueprint.md` §5a "NAV-002 — Replay" |
| `index.html` `[data-nav="NAV-003"]`..`[data-nav="NAV-006"]` → `#screen-deferred` | NAV-003..NAV-006 (destination existence only) | see each NAV's own §5a traceability (unchanged from Batch 01's equivalent citation pattern) | — | `ux-blueprint.md` §5a; §3 UX-P-5 |
| `app.js` `state.incomingContext` = `"incoming-ok"` (default) | NAV-002 "Required context" satisfied | UC-002, UC-004 | PR-001, PR-016 | `ux-blueprint.md` §5a NAV-002 "Required context" |
| `app.js` `state.incomingContext` = `"incoming-no-instance"` / `renderScr002()` blocked branch | NAV-002 "Available navigation behavior" (blocked/prompt option), STATE-004 cited at NAV level | UC-002 | PR-001 | `ux-blueprint.md` §5a NAV-002; §11 STATE-004 row (Applicable screen/view = VIEW-001 — distinction preserved explicitly in the panel copy and here) |
| `app.js` `state.incomingContext` = `"incoming-not-passed"` / `renderScr002()` blocked branch | NAV-002 "Read-only inspection behavior" | UC-002, UC-003 (verification outcome referenced) | PR-001, PR-016, PR-017 | `ux-blueprint.md` §5a NAV-002 "Read-only inspection behavior"; §3 UX-P-5 |
| `index.html` `#screen-scr-002` / `app.js` `renderScr002()` | SCR-002 | UC-004 | PR-008, PR-018, PR-020 | `ux-blueprint.md` §7.2 "SCR-002 — Replay Cursor & Historical Reconstruction" |
| `app.js` `MOCK_CURSORS` / `#cursor-select` | SCR-002 "Available user actions" — chọn Replay Cursor | UC-004 | PR-008, PR-018, PR-020 | `ux-blueprint.md` §7.2 SCR-002 "Available user actions"; Chapter 8 §8.5 canonical Replay Cursor (referenced, not redefined) |
| `app.js` `renderScr002()` loading branch | STATE-001 loading | UC-004 | PR-003, PR-018 | `ux-blueprint.md` §11 STATE-001 row (SCR-002 listed as applicable) |
| `app.js` `renderReconstruction()` unavailable-cursor branch (`C-003`) | STATE-006 Replay reference unavailable | UC-004 | PR-020 | `ux-blueprint.md` §11 STATE-006 row |
| `app.js` `MOCK_REPLAY_STATE` / `renderReconstruction()` normal branch (lineage list) | SCR-002 "Information displayed" — ReplayState(C) | UC-004 | PR-008, PR-018, PR-020 | `ux-blueprint.md` §7.2 SCR-002 "Information displayed"; domain vocabulary decision.md/trade-intent.md/risk.md/execution-intent.md/order.md/execution-result.md/fill.md/position.md (referenced, not redefined) |
| `app.js` `#btn-to-view-003` ("Invoke optional parity recomputation") | SCR-002 "Exit points" (VIEW-003, tuỳ chọn); VIEW-003 "Entry points" (nút hành động tuỳ chọn tại SCR-002, KHÔNG mặc định) | UC-004, UC-005 | PR-008, PR-018, PR-020, PR-010, PR-019 | `ux-blueprint.md` §7.2 SCR-002 "Exit points" + VIEW-003 "Entry points" |
| `index.html` `#screen-view-003` / `app.js` `renderView003()` | VIEW-003 | UC-005 | PR-010, PR-019 | `ux-blueprint.md` §7.2 "VIEW-003 — Parity Recomputation Result" |
| `app.js` `MOCK_REPRESENTATION` / `REPRESENTATION_FIELD_ORDER` / `representationPanel()` | Canonical Decision Semantic Representation | UC-005 | PR-010, PR-019 | `decision.md` §9a.1 (field set + exclusions verbatim; excluded fields e.g. `decision_id`/envelope/`causation_refs`/`account_id`/`plugin_version_ref` deliberately NOT rendered as comparison fields, per §9a.1's exclusion list) |
| `app.js` `PINNED_AXES` / `axisRow()` | Nine pinned axes | UC-005 | PR-010, PR-019 | `decision.md` §9a.4 (nine-axis list verbatim order) + §9a.5a (envelope pinning) + §9a.5b (definition identities) |
| `app.js` `.digest-note` static text | Digest-definition unresolved | UC-005 | PR-010, PR-019 | `decision.md` §9a.2, §9a.5b(3) — "CHƯA ESTABLISHED / unresolved... structured comparison LÀ cơ sở hợp lệ DUY NHẤT cho MATCH" quoted in substance |
| `app.js` `renderView003()` MATCH branch | STATE-007 parity match | UC-005 | PR-010, PR-019 | `ux-blueprint.md` §11 STATE-007 row; `decision.md` §9a.6 MATCH conditions (a)(b)(c) |
| `app.js` `renderView003()` MISMATCH branch | STATE-008 parity mismatch | UC-005 | PR-010, PR-019 | `ux-blueprint.md` §11 STATE-008 row; `decision.md` §9a.6 MISMATCH condition; §9a.7 "MISMATCH KHÔNG tự động invalidate" |
| `app.js` `renderView003()` INDETERMINATE branch | STATE-030 parity indeterminate | UC-005 | PR-010, PR-019 | `ux-blueprint.md` §11 STATE-030 row (Consolidated Stable, v0.6); `decision.md` §9a.6 INDETERMINATE conditions (implementation-identity axis example verbatim) |
| MISMATCH "Continue to Review" button → `#screen-deferred` | VIEW-003 "Exit points" (nếu mismatch, có thể chuyển sang Review); NAV-005 nav-button-existence only | UC-005, UC-016 (Review entry, NOT authored) | PR-010, PR-019, PR-028 | `ux-blueprint.md` §7.2 VIEW-003 "Exit points"; §5a NAV-005 |
| Absence of any "Save recomputed Decision as authoritative"/"Replace recorded Decision"/"Promote parity result"/`ReplayDecision` action anywhere in Batch 02 | VIEW-003 "Out-of-scope boundary" (explicit prohibition) | UC-005 | PR-010, PR-019 | `ux-blueprint.md` §7.2 VIEW-003 "Out-of-scope boundary"; `decision.md` §9a.4 "Recomputation KHÔNG được..."; §9a.7 authority boundary |
| `#screen-deferred` panel (Backtest/Paper/Review/Improve) | (Batch-scoping placeholder — a prototype-batch concept, not a UX Blueprint state) | — | — | N/A — same convention as Batch 01, intentionally represents ONLY "not included in this batch" |
| `#qa-panel`/`#qa-body` (QA state switcher, incl. incoming-context simulation) | (Prototype tooling — explicitly NOT part of authoritative UX) | — | — | N/A — exists only to let every included STATE-XXX and NAV-002 precondition be inspected without the prototype pretending to compute real verification/reconstruction/parity logic |

## 4. Reconciliation statement (I-12 Verification)

```text
Mọi hàng ở §3 trên trace được, đối chiếu trực tiếp, về đúng một section cụ thể trong
  docs/product/ux-blueprint.md (Package 0.3-C, Consolidated Stable) hoặc docs/domain/decision.md
  §9a (Consolidated Stable) — đây LÀ "rebuild hoặc đối chiếu hoàn toàn từ authoritative source"
  per I-12's Verification (Chapter 2 §I-12).
KHÔNG một SCR-XXX/VIEW-XXX/NAV-XXX/FLOW-XXX/STATE-XXX/UC-XXX/PR-XXX ID nào xuất hiện trong Batch
  02 mà KHÔNG có hàng tương ứng ở §3.
KHÔNG một UC/PR/domain concept mới nào originate trong Batch 02 — verify trực tiếp: prototype/
  phase-2/batch-02/*.{html,css,js} KHÔNG tạo entity/event/state-machine mới (KHÔNG "Cursor"
  entity, KHÔNG "ParityResult" entity — decision.md §9a.6 xác nhận tường minh KHÔNG một entity
  như vậy được tạo), KHÔNG author API/database/event contract, KHÔNG redefine Decision/Risk/
  Execution semantics, KHÔNG implement replay/parity computation nào (mọi outcome demo-selected
  qua QA panel, KHÔNG computed).
```

## 5. Excluded-by-design (not a gap — batch-selection rule application)

```text
SCR-003..SCR-011, VIEW-004..VIEW-006 (13 of remaining 15 surfaces, tính cả SCR-001/VIEW-001/
  VIEW-002 đã author tại Batch 01): KHÔNG author trong Batch 02 — đúng batch-selection rule
  ("do not expand into Backtest," "do not author SCR-009 substantively"). Nav/handoff affordance
  tồn tại (dẫn tới #screen-deferred), substantive screen content KHÔNG.
UC-006..UC-021 trừ UC-011/015/019/020/021 (đã B từ Batch 01): KHÔNG substantively covered trong
  Batch 02 — xem §2 ledger cho phân loại B/C chính xác, KHÔNG dùng "deferred" cho toàn bộ tập
  hợp (đúng lesson từ Batch 01's `P2-B01-A-MIN-01`).
```
