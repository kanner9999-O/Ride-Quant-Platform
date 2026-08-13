---
id: phase-2-batch-02-traceability
title: "Phase 2 Prototype — Batch 02 — Traceability Artifact"
version: "1.1"
status: Candidate
owner: Product Owner
created_at: "2026-08-13"
---

# Phase 2 Prototype — Batch 02 — Traceability Artifact

**Vai trò của tài liệu này:** đây LÀ I-12 (Single Source of Truth) conformance evidence cho Batch 02, per `docs/phase-dod/phase-2-dod.md` §2's applicable Trigger A / I-12 requirement — mọi phần tử prototype trong batch này PHẢI trace được TRỰC TIẾP về đúng một hoặc nhiều `SCR-XXX`/`VIEW-XXX`/`NAV-XXX`/`FLOW-XXX`/`STATE-XXX` đã `Consolidated Stable` trong [`docs/product/ux-blueprint.md`](../../../docs/product/ux-blueprint.md) VÀ [`docs/domain/decision.md`](../../../docs/domain/decision.md) §9a, VÀ về đúng `UC-XXX`/`PR-XXX` đã tồn tại. Prototype LÀ derived representation — KHÔNG một UC/PR/domain concept nào originate tại đây. Áp dụng ĐÚNG taxonomy A/B/C đã establish tại `../batch-01/traceability.md` §0.

**v1.1 — bounded correction (2026-08-13), đóng `P2-B02-A-MAJ-01` (Review A).** v1.0's cumulative A/B/C ledger KHÔNG PHẢI một valid partition: (1) `UC-002` xuất hiện CẢ trong A (Batch 01 substantive) LẪN trong cumulative B — vi phạm "once A, never also B/C"; (2) `UC-009`/`UC-010` bị gọi B trong khi chính mô tả nói "not referenced by Batch 02 at all" — tự mâu thuẫn; (3) C ghi "9 of 21" nhưng danh sách liệt kê 10 UC; (4) "5+7+9=21" do đó KHÔNG PHẢI một proof hợp lệ vì các set chồng lấn/cardinality sai. Sửa: §0-§2 viết lại hoàn toàn — recompute B TỪ ĐẦU bằng cách inspect trực tiếp `ux-blueprint.md` §5a's chính xác UC traceability của NAV-003 (`UC-002, UC-006`), NAV-004 (`UC-002, UC-011`), NAV-005 (`UC-016, UC-017, UC-018`), NAV-006 (`UC-019, UC-002, UC-020, UC-021`) — loại `UC-002`/`UC-004` khỏi B (VẪN A từ Batch 01/02), giữ `UC-006`/`UC-011`/`UC-016`/`UC-017`/`UC-018`/`UC-019`/`UC-020`/`UC-021` (8 UC từ NAV citation) + `UC-015` (WS-001/STATE-027 citation, KHÔNG qua NAV nào) = B đúng 9 UC. `UC-009`/`UC-010` (VÀ `UC-007`/`UC-008`/`UC-012`/`UC-013`/`UC-014`) KHÔNG một element nào trong Batch 01/02 tham chiếu — verify trực tiếp, C đúng 7 UC. Kết quả: A=5, B=9, C=7, tổng=21, A∩B=A∩C=B∩C=∅ (verify mechanically tại §2 dưới). KHÔNG đổi Replay/parity UX behavior, KHÔNG surface/screen mới, KHÔNG đổi §3 element-level map's hàng hiện có (CHỈ bổ sung explicit NAV-003..006 citation detail cho auditability).

## 0. UC accounting taxonomy (kế thừa nguyên vẹn từ Batch 01, KHÔNG redefine)

```text
A. SUBSTANTIVELY COVERED — Batch tự author ĐỦ representation (screen/view + required context +
   primary/blocked states + exit behavior đúng ux-blueprint.md/decision.md §9a spec) để tính vào
   21-UC completion numerator (phase-2-dod.md §3).
B. PARTIAL / REFERENCED — UC xuất hiện qua global shell context, nav-button existence, handoff
   affordance, hay deferred-placeholder destination — KHÔNG đủ để tính vào numerator.
C. DEFERRED / NOT YET REPRESENTED — KHÔNG một element nào trong batch tham chiếu UC đó.
```

## 1. Batch-02-authored substantive contribution (distinct từ cumulative ledger, §2 dưới)

```text
Batch-02-authored substantive UC (NEW tại batch này): UC-004 (SCR-002), UC-005 (VIEW-003).
Batch-01-verified substantive UC (KHÔNG re-authored, KHÔNG double-counted, VẪN A vì Batch 02
  tiêu thụ chúng LÀM prerequisite context, KHÔNG PHẢI VÌ Batch 02 tự re-cover chúng):
  UC-001 (SCR-001), UC-002 (VIEW-001), UC-003 (VIEW-002).
```

| UC | Classification | Evidence / reason |
|---|---|---|
| UC-004 | **A — Substantive** (Batch 02, mới) | SCR-002 fully authored: NAV-002 precondition gate (Strategy Instance/verification), required context, cursor selection bound to prototype-local state, full lineage display (Decision→...→Position) at cursor, STATE-001/STATE-006 — matches `ux-blueprint.md` §7.2 SCR-002 spec. |
| UC-005 | **A — Substantive** (Batch 02, mới) | VIEW-003 fully authored: optional (never automatic) entry from SCR-002, recorded-vs-recomputed Canonical Decision Semantic Representation comparison, nine pinned axes, digest-definition-unresolved note, MATCH/MISMATCH/INDETERMINATE (STATE-007/008/030), MISMATCH→Review handoff, explicit absence of any promote/save/replace/ReplayDecision action — matches `ux-blueprint.md` §7.2 VIEW-003 spec + `decision.md` §9a.1–§9a.7. |
| UC-001, UC-002, UC-003 | **A — Substantive** (Batch 01, giữ nguyên — KHÔNG PHẢI B chỉ vì Batch 02 tiêu thụ chúng LÀM prerequisite/incoming-context) | SCR-001/VIEW-001/VIEW-002 fully authored tại Batch 01 (Independent Review B verdict `READY_FOR_NEXT_PHASE2_BATCH`). Batch 02 CHỈ link tới Research (real nav link) VÀ simulate incoming context (QA panel) — KHÔNG re-author, NHƯNG cumulative classification của CHÍNH các UC này VẪN A, KHÔNG hạ xuống B (đóng `P2-B02-A-MAJ-01` finding 1: một UC KHÔNG thể vừa A vừa B). |

## 2. Cumulative Phase-2 UC ledger (Batch 01 + Batch 02, candidate — KHÔNG independently verified tại transaction này)

**Recompute B TỪ ĐẦU (đóng `P2-B02-A-MAJ-01`), verify trực tiếp từng NAV's UC traceability tại `ux-blueprint.md` §5a (KHÔNG suy diễn/copy từ Batch 01):**

```text
NAV-003 (line 316):  "UC-002 (Strategy Instance precondition), UC-006."      -> UC-006 mới (UC-002 đã A)
NAV-004 (line 349):  "UC-002, UC-011 (Paper pin, v0.3)."                     -> UC-011 mới (UC-002 đã A)
NAV-005 (line 376):  "UC-016, UC-017, UC-018."                                -> UC-016/017/018 mới, ĐẦY ĐỦ
                      (cùng nav-button-existence citation, đúng NAV-005's spec CHÍNH NÓ KHÔNG
                      phân biệt UC nào "chính" hơn UC nào — VIEW-003's MISMATCH→Review handoff
                      bổ sung một second citation path cho UC-016 riêng, KHÔNG đổi kết luận)
NAV-006 (line 407):  "UC-019, UC-002 (...), UC-020, UC-021."                  -> UC-019/020/021 mới
                      (UC-002 đã A)
WS-001 §5 table +
  STATE-027 §11 row:  "UC-011 (...), UC-011/UC-015 (Live)"                    -> UC-015 mới (UC-011
                      đã trùng NAV-004)
```

```text
A — Substantively covered (candidate, 5 of 21):
  UC-001, UC-002, UC-003 (Batch 01) + UC-004, UC-005 (Batch 02).

B — Partial/referenced (9 of 21, recomputed từ đầu — KHÔNG copy Batch 01's set cũ):
  UC-006, UC-011, UC-015, UC-016, UC-017, UC-018, UC-019, UC-020, UC-021.

C — Deferred/not yet represented (7 of 21 — verify trực tiếp: KHÔNG element nào trong Batch
  01/02 tham chiếu các UC này, kể cả UC-009/UC-010 dù cùng "Backtest" lifecycle stage với
  UC-006 — NAV-003's OWN UC traceability CHỈ cite UC-002/UC-006, KHÔNG UC-009/UC-010):
  UC-007, UC-008, UC-009, UC-010, UC-012, UC-013, UC-014.

Partition validation (mechanical):
  |A| = 5, |B| = 9, |C| = 7.  5 + 9 + 7 = 21.  Đúng.
  A ∩ B: {001,002,003,004,005} ∩ {006,011,015,016,017,018,019,020,021} = ∅.  Đúng.
  A ∩ C: {001,002,003,004,005} ∩ {007,008,009,010,012,013,014} = ∅.  Đúng.
  B ∩ C: {006,011,015,016,017,018,019,020,021} ∩ {007,008,009,010,012,013,014} = ∅.  Đúng.
  A ∪ B ∪ C = {001,002,...,021} — liệt kê tuần tự xác nhận KHÔNG thiếu UC nào: 001(A) 002(A)
    003(A) 004(A) 005(A) 006(B) 007(C) 008(C) 009(C) 010(C) 011(B) 012(C) 013(C) 014(C) 015(B)
    016(B) 017(B) 018(B) 019(B) 020(B) 021(B) — 21 UC, mỗi UC xuất hiện ĐÚNG MỘT LẦN.

21-UC substantive completion progress (candidate): 5/21 -- CHỈ đếm hạng mục A, CHƯA independently
  verified (chờ Review A + Independent Review B trên Batch 02, đúng P2-PROTOTYPE-001). Last
  INDEPENDENTLY VERIFIED progress VẪN 3/21 (Batch 01 only, Independent Review B verdict).
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
§2's cumulative UC ledger LÀ completion accounting (Chapter 12/phase-2-dod.md §3 purpose) —
  TÁCH BIỆT khỏi §3's element-to-authority traceability map (I-12 purpose). Sau `P2-B02-A-MAJ-01`
  correction, hai tài liệu này KHÔNG mâu thuẫn: mọi UC cited tại §3 (element-level, cho phép
  multi-UC per element, kể cả UC đã A) đều resolve nhất quán vào ĐÚNG MỘT hạng mục tại §2's
  partition — verify trực tiếp, KHÔNG UC nào tại §3 rơi ngoài {A, B, C} đã định nghĩa tại §2.
```

## 5. Excluded-by-design (not a gap — batch-selection rule application)

```text
SCR-003..SCR-011, VIEW-004..VIEW-006 (13 of remaining 15 surfaces, tính cả SCR-001/VIEW-001/
  VIEW-002 đã author tại Batch 01): KHÔNG author trong Batch 02 — đúng batch-selection rule
  ("do not expand into Backtest," "do not author SCR-009 substantively"). Nav/handoff affordance
  tồn tại (dẫn tới #screen-deferred), substantive screen content KHÔNG.
16 of 21 UC KHÔNG substantively covered (§2 ledger — B=9, C=7, KHÔNG collapse thành một bucket,
  đúng lesson từ Batch 01's `P2-B01-A-MIN-01`, VÀ KHÔNG double-count UC-002 vào cả A lẫn B, đúng
  fix của `P2-B02-A-MAJ-01`):
  B — Partial/referenced (9): UC-006, UC-011, UC-015, UC-016, UC-017, UC-018, UC-019, UC-020,
    UC-021.
  C — Deferred/not yet represented (7): UC-007, UC-008, UC-009, UC-010, UC-012, UC-013, UC-014.
```
