---
id: phase-2-batch-01-traceability
title: "Phase 2 Prototype — Batch 01 — Traceability Artifact"
version: "1.0"
status: Candidate
owner: Product Owner
created_at: "2026-08-13"
---

# Phase 2 Prototype — Batch 01 — Traceability Artifact

**Vai trò của tài liệu này:** đây LÀ I-12 (Single Source of Truth) conformance evidence cho Batch 01, per `docs/phase-dod/phase-2-dod.md` §2's applicable Trigger A / I-12 requirement — mọi phần tử prototype trong batch này PHẢI trace được TRỰC TIẾP về đúng một hoặc nhiều `SCR-XXX`/`VIEW-XXX`/`NAV-XXX`/`FLOW-XXX`/`STATE-XXX` đã `Consolidated Stable` trong [`docs/product/ux-blueprint.md`](../../../docs/product/ux-blueprint.md), VÀ về đúng `UC-XXX`/`PR-XXX` đã tồn tại. Prototype LÀ derived representation — KHÔNG một UC/PR/domain concept nào originate tại đây.

## 1. Element-level traceability map

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

## 2. Reconciliation statement (I-12 Verification)

```text
Mọi hàng ở §1 trên trace được, đối chiếu trực tiếp, về đúng một section cụ thể trong
  docs/product/ux-blueprint.md (Package 0.3-C, Consolidated Stable) — đây LÀ "rebuild hoặc đối
  chiếu hoàn toàn từ authoritative source" per I-12's Verification (Chapter 2 §I-12).
KHÔNG một SCR-XXX/VIEW-XXX/NAV-XXX/FLOW-XXX/STATE-XXX/UC-XXX/PR-XXX ID nào xuất hiện trong Batch 01
  mà KHÔNG có hàng tương ứng ở trên.
KHÔNG một UC/PR/domain concept mới nào originate trong Batch 01 — verify trực tiếp: prototype/
  phase-2/batch-01/*.{html,css,js} KHÔNG tạo entity/event/state-machine mới, KHÔNG author API/
  database/event contract, KHÔNG redefine Decision/Risk/Execution semantics.
```

## 3. Excluded-by-design (not a gap — batch-selection rule application)

```text
SCR-002..SCR-011, VIEW-003..VIEW-006 (14 of 17 surfaces): KHÔNG author trong Batch 01 — đúng
  batch-selection rule ("do not pull Replay/Backtest/Paper/Review/Improve surfaces into Batch 01
  merely because they appear later in the overall flow"). Nav affordance tồn tại (points to
  #screen-deferred), substantive screen content KHÔNG.
UC-004..UC-021 (18 of 21 UC): KHÔNG covered trong Batch 01 — same reason, deferred to later
  batches per P2-PROTOTYPE-001.
```
