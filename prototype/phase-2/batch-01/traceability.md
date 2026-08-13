---
id: phase-2-batch-01-traceability
title: "Phase 2 Prototype — Batch 01 — Traceability Artifact"
version: "1.1"
status: Candidate
owner: Product Owner
created_at: "2026-08-13"
---

# Phase 2 Prototype — Batch 01 — Traceability Artifact

**Vai trò của tài liệu này:** đây LÀ I-12 (Single Source of Truth) conformance evidence cho Batch 01, per `docs/phase-dod/phase-2-dod.md` §2's applicable Trigger A / I-12 requirement — mọi phần tử prototype trong batch này PHẢI trace được TRỰC TIẾP về đúng một hoặc nhiều `SCR-XXX`/`VIEW-XXX`/`NAV-XXX`/`FLOW-XXX`/`STATE-XXX` đã `Consolidated Stable` trong [`docs/product/ux-blueprint.md`](../../../docs/product/ux-blueprint.md), VÀ về đúng `UC-XXX`/`PR-XXX` đã tồn tại. Prototype LÀ derived representation — KHÔNG một UC/PR/domain concept nào originate tại đây.

**v1.1 — bounded correction (2026-08-13), đóng `P2-B01-A-MIN-01`.** Thêm §0 "UC accounting taxonomy" (A Substantive / B Partial-referenced / C Deferred) VÀ §1 "Full 21-UC classification" (toàn bộ 21 UC classify tường minh) — giải quyết ambiguity giữa UC xuất hiện tại element-level map (§2, cũ §1) như một REFERENCE và UC được substantively cover đủ tính vào 21-UC completion numerator. Progress `3/21` KHÔNG đổi (UC-001/002/003, hạng mục A) — CHỈ accounting logic được làm rõ tường minh, KHÔNG inflate. §4 (cũ §3, "Excluded-by-design") cập nhật đồng bộ để phân biệt 7 UC hạng mục B khỏi 11 UC hạng mục C. KHÔNG đổi §2 element-level map's nội dung hàng (row content giữ nguyên, CHỈ thêm ghi chú disclaimer phía trên bảng).

## 0. UC accounting taxonomy (đóng `P2-B01-A-MIN-01`)

Mọi `UC-XXX` xuất hiện BẤT KỲ ĐÂU trong tài liệu này (kể cả chỉ qua shell/nav/handoff/global
context) PHẢI classify vào ĐÚNG MỘT trong ba hạng mục dưới đây — tránh ambiguity giữa "UC được
tham chiếu" và "UC được substantively cover" (per `phase-2-dod.md` §3's 21-UC completion
requirement, riêng biệt khỏi 17-surface completion, KHÔNG cái nào thay thế cái kia):

```text
A. SUBSTANTIVELY COVERED — Batch 01 author ĐỦ representation (screen/view + required
   context + primary/blocked states + exit behavior đúng ux-blueprint.md spec) để tính vào
   21-UC completion numerator (phase-2-dod.md §3).
B. PARTIAL / REFERENCED — UC xuất hiện qua global shell context, nav-button existence, handoff
   affordance, hay deferred-placeholder destination — KHÔNG đủ để tính vào numerator. Referenced
   KHÔNG PHẢI fabricated: mỗi tham chiếu B trace được về đúng phần source spec MÀ Batch 01 THỰC
   SỰ author (vd: một nav button "tồn tại và khả dụng" LÀ một phần thật của NAV-XXX's "Available
   navigation behavior," dù KHÔNG PHẢI toàn bộ NAV-XXX spec).
C. DEFERRED / NOT YET REPRESENTED — KHÔNG một element nào trong Batch 01 tham chiếu UC đó, dưới
   bất kỳ hình thức nào.
```

## 1. Full 21-UC classification (đóng `P2-B01-A-MIN-01`)

| UC | Classification | Evidence / reason |
|---|---|---|
| UC-001 | **A — Substantive** | SCR-001 fully authored: required context, information displayed, primary/blocked states (STATE-001/003/005), exit action — matches `ux-blueprint.md` §7.1 SCR-001 spec. |
| UC-002 | **A — Substantive** | VIEW-001 fully authored: instance list, select/pin action, STATE-004 empty — matches §7.1 VIEW-001 spec; FLOW-002 (selection/pin) fully represented. |
| UC-003 | **A — Substantive** | VIEW-002 fully authored: tri-state PASSED/FAILED/INDETERMINATE (STATE-022/023/024), reason disclosure, blocked progression — matches §7.1 VIEW-002 spec. |
| UC-004 | **B — Partial/referenced** | NAV-002 nav-button exists (available-navigation-behavior fragment only) + VIEW-002 PASSED "Continue to Replay" handoff button — both lead to `#screen-deferred`. SCR-002's own required-context/information-displayed/state behavior NOT authored. |
| UC-005 | **C — Deferred** | Zero reference anywhere in Batch 01 (VIEW-003 not touched by any element). |
| UC-006 | **B — Partial/referenced** | NAV-003 nav-button exists + VIEW-002 PASSED "Continue to Backtest" handoff button — both lead to `#screen-deferred`. SCR-003's substantive behavior NOT authored. |
| UC-007 | **C — Deferred** | Zero reference. |
| UC-008 | **C — Deferred** | Zero reference. |
| UC-009 | **C — Deferred** | Zero reference. |
| UC-010 | **C — Deferred** | Zero reference. |
| UC-011 | **B — Partial/referenced** | Cited only as the source-spec justification for WS-001's Account-context/Strategy-Instance-context rows and STATE-027's global label, and NAV-004's nav-button existence — none of SCR-006's own required-context/action/state behavior authored. |
| UC-012 | **C — Deferred** | Zero reference. |
| UC-013 | **C — Deferred** | Zero reference. |
| UC-014 | **C — Deferred** | Zero reference. |
| UC-015 | **B — Partial/referenced** | Cited only as the source-spec justification for STATE-027 (Live unauthorized, global static label) — no other Batch 01 element touches it. |
| UC-016 | **C — Deferred** | Zero reference. |
| UC-017 | **C — Deferred** | Zero reference. |
| UC-018 | **C — Deferred** | Zero reference. |
| UC-019 | **B — Partial/referenced** | Cited only as NAV-006's nav-button-existence source-spec justification — SCR-010's substantive behavior NOT authored. |
| UC-020 | **B — Partial/referenced** | Same as UC-019 — NAV-006 nav-button existence only. |
| UC-021 | **B — Partial/referenced** | Same as UC-019 — NAV-006 nav-button existence only. |

```text
Tally: A (substantive) = 3 (UC-001, UC-002, UC-003).
       B (partial/referenced) = 7 (UC-004, UC-006, UC-011, UC-015, UC-019, UC-020, UC-021).
       C (deferred/not yet represented) = 11 (UC-005, UC-007, UC-008, UC-009, UC-010, UC-012,
         UC-013, UC-014, UC-016, UC-017, UC-018).
       3 + 7 + 11 = 21. Đúng.
21-UC completion progress (phase-2-dod.md §3) = 3/21 — CHỈ đếm hạng mục A. Hạng mục B KHÔNG được
  cộng vào numerator dù xuất hiện trong §2 dưới — đây CHÍNH LÀ điều `P2-B01-A-MIN-01` yêu cầu làm
  rõ tường minh.
```

## 2. Element-level traceability map

**Ghi chú (đóng `P2-B01-A-MIN-01`):** cột "UC" dưới đây liệt kê MỌI UC một element trace được về, kể cả hạng mục B (Partial/referenced) — bảng này LÀ element-to-source mapping (I-12 reconciliation), KHÔNG PHẢI substantive-completion accounting. Dùng §0/§1 phía trên cho substantive-completion accounting (3/21), KHÔNG suy diễn substantive completion từ việc một UC xuất hiện tại bảng dưới đây.

| Prototype element (file:selector) | UX Blueprint ID | UC | PR | Authoritative source section |
|---|---|---|---|---|
| `index.html` `#shell` / `#context-bar` (Account, Instrument/Venue, Strategy Instance, Live labels) | WS-001 | UC-011 (Account), UC-001/UC-011 (Instrument/Venue), UC-002/UC-011 (Strategy Instance), UC-011/UC-015 (Live) | PR-002, PR-003, PR-001, PR-016, PR-027 | `ux-blueprint.md` §5 "WS-001 — Ride Workspace Shell" table |
| `index.html` `#nav-bar` (six-stage bar, existence/order) | (six-stage structure, inherited — no single owning UC/PR per WS-001 §5 note) | — | — | `ux-blueprint.md` §5 "Item KHÔNG còn thuộc bảng trực tiếp của WS-001" note; `use-case-workflow.md` §4 |
| `index.html` `#nav-bar [data-nav="NAV-001"]` (Research button) | NAV-001 | UC-001 | PR-003, PR-015, PR-017 | `ux-blueprint.md` §5a "NAV-001 — Research" |
| `index.html` `[data-nav="NAV-002"]`..`[data-nav="NAV-006"]` → `#screen-deferred` placeholder | NAV-002..NAV-006 (destination existence only — read-only inspection navigation, UX-P-5) | UC-002/UC-004 (NAV-002) .. UC-019/UC-002/UC-020/UC-021 (NAV-006) | see §5a per NAV | `ux-blueprint.md` §5a "NAV-002".."NAV-006"; §3 UX-P-5 (read-only inspection navigation always available) |
| `index.html` `#screen-scr-001` (Market Analysis Workspace) | SCR-001 | UC-001 | PR-003, PR-015, PR-017 | `ux-blueprint.md` §7.1 "SCR-001 — Market Analysis Workspace" |
| `app.js` `MOCK_INSTRUMENTS` / `#instrument-select` | SCR-001 required context (Instrument/Venue, UX-INV-2) | UC-001 | PR-003 | `ux-blueprint.md` §7.1 SCR-001 "Required context"; §3 UX-INV-2 |
| `app.js` `renderScr001()` normal-content branch (Candle/Swing/Structure/Regime/Feature/Market Context) | SCR-001 "Information displayed" | UC-001 | PR-003, PR-015, PR-017 | `ux-blueprint.md` §7.1 SCR-001 "Information displayed"; domain vocabulary candle.md/swing.md/structure.md/regime.md/feature.md/context.md/instrument.md/venue.md (referenced, not redefined) |
| `app.js` `renderScr001()` loading branch | STATE-001 loading | UC-001 | PR-003, PR-018 | `ux-blueprint.md` §11 STATE-001 row |
| `app.js` `renderScr001()` invalid-Instrument branch | STATE-003 invalid Instrument/Venue | UC-001, UC-011 | PR-003 | `ux-blueprint.md` §11 STATE-003 row |
| `app.js` `renderScr001()` missing-evidence branch | STATE-005 missing historical evidence | UC-001, UC-006 | PR-015, PR-021 | `ux-blueprint.md` §11 STATE-005 row |
| `index.html` `#screen-view-001` (Strategy Instance Selector) | VIEW-001 | UC-002, UC-011 | PR-001, PR-016 | `ux-blueprint.md` §7.1 "VIEW-001 — Strategy Instance Selector" |
| `app.js` `MOCK_STRATEGY_INSTANCES` / `renderView001()` list branch | VIEW-001 "Information displayed" / "Available user actions" | UC-002 | PR-001, PR-016 | `ux-blueprint.md` §7.1 VIEW-001 |
| `app.js` `renderView001()` empty branch | STATE-004 missing Strategy Instance | UC-002 | PR-001 | `ux-blueprint.md` §11 STATE-004 row |
| `index.html` `#screen-view-002` (Research Verification Result) | VIEW-002 | UC-003 | PR-017 | `ux-blueprint.md` §7.1 "VIEW-002 — Research Verification Result" |
| `app.js` `renderView002()` PASSED branch | STATE-022 | UC-003 | PR-017 | `ux-blueprint.md` §11 STATE-022 row |
| `app.js` `renderView002()` FAILED branch | STATE-023 | UC-003 | PR-017 | `ux-blueprint.md` §11 STATE-023 row |
| `app.js` `renderView002()` INDETERMINATE branch | STATE-024 | UC-003 | PR-017 | `ux-blueprint.md` §11 STATE-024 row |
| `index.html` `#ctx-live` "Unauthorized" badge | STATE-027 Live unauthorized (global, static) | UC-011, UC-015 | PR-027 | `ux-blueprint.md` §11 STATE-027 row; §3 UX-INV-10 |
| Instance selection → pin → advance to VIEW-002 (`app.js` click handler in `renderView001()`) | FLOW-002 (Strategy Instance selection/pin) | UC-002 | PR-001, PR-016 | `ux-blueprint.md` §8 "FLOW-002" |
| SCR-001 → VIEW-001 → VIEW-002 → [PASSED] → deferred Replay/Backtest (`app.js` overall navigation sequence) | FLOW-001 (initial segment, up to commit gate) | UC-001, UC-002, UC-003 | PR-001, PR-016, PR-017 | `ux-blueprint.md` §8 "FLOW-001" (WS-001 → NAV-001 → SCR-001 → commit gate → VIEW-001 → VIEW-002 segment only) |
| Research → Replay/Backtest handoff affordance (VIEW-002 PASSED "Continue" buttons, both lead to `#screen-deferred`) | Research → Replay handoff (existence of the handoff only, not the destination screens) | UC-004 (Replay entry), UC-006 (Backtest entry) — NOT authored | — | `ux-blueprint.md` §9 "Research → Replay" |
| `#screen-deferred` panel | (Batch-scoping placeholder — a prototype-batch concept, not a UX Blueprint state) | — | — | N/A — this element intentionally represents ONLY "not included in Batch 01," never a UX Blueprint `STATE-XXX` |
| `#qa-panel` / `#qa-body` (QA state switcher) | (Prototype tooling — explicitly NOT part of authoritative UX, labelled as such in the UI itself) | — | — | N/A — exists only to let every included `STATE-XXX` be inspected without the prototype pretending to compute real verification/data-availability logic |

## 3. Reconciliation statement (I-12 Verification)

```text
Mọi hàng ở §2 trên trace được, đối chiếu trực tiếp, về đúng một section cụ thể trong
  docs/product/ux-blueprint.md (Package 0.3-C, Consolidated Stable) — đây LÀ "rebuild hoặc đối
  chiếu hoàn toàn từ authoritative source" per I-12's Verification (Chapter 2 §I-12).
KHÔNG một SCR-XXX/VIEW-XXX/NAV-XXX/FLOW-XXX/STATE-XXX/UC-XXX/PR-XXX ID nào xuất hiện trong Batch 01
  mà KHÔNG có hàng tương ứng ở §2.
KHÔNG một UC/PR/domain concept mới nào originate trong Batch 01 — verify trực tiếp: prototype/
  phase-2/batch-01/*.{html,css,js} KHÔNG tạo entity/event/state-machine mới, KHÔNG author API/
  database/event contract, KHÔNG redefine Decision/Risk/Execution semantics.
```

## 4. Excluded-by-design (not a gap — batch-selection rule application)

```text
SCR-002..SCR-011, VIEW-003..VIEW-006 (14 of 17 surfaces): KHÔNG author trong Batch 01 — đúng
  batch-selection rule ("do not pull Replay/Backtest/Paper/Review/Improve surfaces into Batch 01
  merely because they appear later in the overall flow"). Nav affordance tồn tại (points to
  #screen-deferred), substantive screen content KHÔNG.
18 of 21 UC KHÔNG substantively covered trong Batch 01 (§0/§1 phía trên) — trong đó 7 (UC-004,
  UC-006, UC-011, UC-015, UC-019, UC-020, UC-021) xuất hiện dưới dạng B (Partial/referenced, qua
  shell/nav/handoff) VÀ 11 (UC-005, UC-007–UC-010, UC-012–UC-014, UC-016–UC-018) LÀ C (Deferred,
  zero reference) — cả hai hạng mục ĐỀU KHÔNG tính vào 3/21 numerator. Deferred tới batch sau,
  đúng P2-PROTOTYPE-001.
```
