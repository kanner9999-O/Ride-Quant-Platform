---
id: phase-2-batch-03-traceability
title: "Phase 2 Prototype — Batch 03 — Traceability Artifact"
version: "1.2"
status: Candidate
owner: Product Owner
created_at: "2026-08-13"
---

# Phase 2 Prototype — Batch 03 — Traceability Artifact

**Vai trò của tài liệu này:** đây LÀ I-12 (Single Source of Truth) conformance evidence cho Batch 03, per `docs/phase-dod/phase-2-dod.md` §2's applicable Trigger A / I-12 requirement — mọi phần tử prototype trong batch này PHẢI trace được TRỰC TIẾP về đúng một hoặc nhiều `SCR-XXX`/`VIEW-XXX`/`NAV-XXX`/`FLOW-XXX`/`STATE-XXX` đã `Consolidated Stable` trong [`docs/product/ux-blueprint.md`](../../../docs/product/ux-blueprint.md), VÀ về đúng `UC-XXX` đã `Consolidated Stable` trong [`docs/product/use-case-workflow.md`](../../../docs/product/use-case-workflow.md) (v0.6, đóng `P03B-V05-B-MAJ-01`), VÀ về đúng `PR-XXX` đã tồn tại. Prototype LÀ derived representation — KHÔNG một UC/PR/domain concept nào originate tại đây. Áp dụng ĐÚNG taxonomy A/B/C đã establish tại `../batch-01/traceability.md` §0, kế thừa nguyên vẹn qua `../batch-02/traceability.md`.

**v1.1 — bounded correction (2026-08-13), Review A trên v1.0: `P2-B03-A-MAJ-01` (Major) + `P2-B03-A-MIN-01` (Minor) — đóng CẢ HAI tại transaction này.** `P2-B03-A-MAJ-01`: `use-case-workflow.md` UC-008 yêu cầu CẢ HAI — (1) simulated economic evidence per Decision→exposure change, VÀ (2) exposure/position progression theo thời gian xuyên suốt khoảng interval của run (Main flow bước 2, tách biệt bước 1) — v1.0's `renderEconomicEvidence()` chỉ render (1), KHÔNG render một ordered temporal progression nào (biến `progression` cục bộ được cập nhật nhưng KHÔNG BAO GIỜ hiển thị). Sửa: thêm `positionProgression()` helper (`app.js`) — dẫn xuất deterministic TRỰC TIẾP từ `run.decisions` sẵn có (KHÔNG fixture mới, KHÔNG simulation engine) — MỘT ordered row/Decision (kể cả điểm không đổi), hiển thị dưới dạng bảng `.progression-table` (# / Decision / Position before / Simulated change / Position after) tại SCR-004 Panel B, ngay dưới danh sách per-Decision change đã có. Khác run → khác progression (dẫn xuất từ chính run's decisions, KHÔNG một timeline giả chung). STATE-009 giữ nguyên hành vi — KHÔNG progression nào render cho run insufficient-evidence (guard KHÔNG đổi). `P2-B03-A-MIN-01`: §2 dưới's "Last INDEPENDENTLY VERIFIED" provenance mô tả sai 5/17, 5/21 như thể "Batch 01 verified + Batch 02 candidate" — SAI, tại boundary khởi đầu Batch 03, Batch 02 v1.3 ĐÃ có Independent bounded Review B verdict `READY_FOR_NEXT_PHASE2_BATCH` (task-relayed baseline cho transaction authoring Batch 03 gốc, đã ghi nhận nguyên văn tại `docs/CHANGELOG.md`'s Baseline block cho Batch 03 — "Batch 02: READY_FOR_NEXT_PHASE2_BATCH per task baseline" — nhưng KHÔNG được carry forward nhất quán vào tài liệu này, vốn tự ý hedge thành "candidate contribution"). Sửa: §2 viết lại — 5/17, 5/21 nay ghi nhận LÀ last independently verified (KHÔNG hedge UC-004/UC-005 hay SCR-002/VIEW-003 là "candidate"). Lưu ý minh bạch: việc ghi nhận chính thức verdict này VÀO `batch-02/batch-manifest.md`'s own §17 review-state section VẪN LÀ một governed transaction riêng, CHƯA issue — tài liệu batch-02 tự thân KHÔNG bị sửa bởi transaction này (đúng "Preserve unchanged: Batch 02").

**v1.2 — deterministic bookkeeping reconciliation (2026-08-14), vai trò: `Phase 2 Prototype Review-State Bookkeeping Reconciliation Executor`, đúng `G-TXN-003`.** KHÔNG PHẢI lifecycle transition, KHÔNG PHẢI prototype semantic correction. §2's tiêu đề VÀ kết luận, VÀ §6's kết luận, vẫn nói "candidate — KHÔNG independently verified" / "CHƯA independently verified (chờ Review A + Independent Review B trên Batch 03)" — mâu thuẫn trực tiếp với governed review history ĐÃ hoàn tất từ v1.1 (bounded Review A re-review v1.1 CLEAN; Independent Review B v1.1: `P2-B03-A-MAJ-01` CLOSED, `P2-B03-A-MIN-01` CLOSED, 0/0/0, verdict `READY_FOR_NEXT_PHASE2_BATCH`). Sửa: §2's tiêu đề + kết luận, VÀ §6's kết luận, viết lại để phản ánh 10/21 VÀ 8/17 ĐÃ independently verified — batch-02/batch-01's own contribution's provenance (ghi tại v1.1) KHÔNG đổi. KHÔNG đổi §0/§1/§3/§4/§5 (A/B/C partition, element-level map, reconciliation statement, Backtest/Paper authority separation KHÔNG đổi — VẪN A=10/B=8/C=3/tổng=21).

## 0. UC accounting taxonomy (kế thừa nguyên vẹn từ Batch 01/02, KHÔNG redefine)

```text
A. SUBSTANTIVELY COVERED — Batch tự author ĐỦ representation (screen/view + required context +
   primary/blocked states + exit behavior đúng ux-blueprint.md/use-case-workflow.md spec) để tính
   vào 21-UC completion numerator (phase-2-dod.md §3).
B. PARTIAL / REFERENCED — UC xuất hiện qua global shell context, nav-button existence, handoff
   affordance, hay deferred-placeholder destination — KHÔNG đủ để tính vào numerator.
C. DEFERRED / NOT YET REPRESENTED — KHÔNG một element nào trong batch tham chiếu UC đó.
```

## 1. Batch-03-authored substantive contribution (distinct từ cumulative ledger, §2 dưới)

```text
Batch-03-authored substantive UC (NEW tại batch này, 5):
  UC-006 (SCR-003 — Backtest setup/run start)
  UC-007 (SCR-004 Panel A — Decision/RiskEvaluation trace)
  UC-008 (SCR-004 Panel B — simulated economic/exposure evidence)
  UC-009 (SCR-004 Panel C — strategy-level evaluable result)
  UC-010 (SCR-005 — run comparison)

UC-006 was previously hạng B (referenced only via NAV-003's nav-button-existence citation,
  Batch 01/02) — nay promote lên A vì SCR-003 tự author đủ representation (required context,
  information displayed, primary/blocked states STATE-001/STATE-005, exit action) đúng
  `ux-blueprint.md` §7.3 SCR-003 spec.
UC-007/008/009/010 previously hạng C (zero reference, Batch 01/02) — nay promote lên A vì
  SCR-004 (ba panel tách biệt) và SCR-005 tự author đủ representation đúng `ux-blueprint.md`
  §7.3 SCR-004/SCR-005 spec VÀ `use-case-workflow.md` UC-007/UC-008/UC-009/UC-010 detailed block.

Batch-01/02-verified substantive UC (KHÔNG re-authored, KHÔNG double-counted, VẪN A):
  UC-001 (SCR-001), UC-002 (VIEW-001), UC-003 (VIEW-002), UC-004 (SCR-002), UC-005 (VIEW-003).
```

| UC | Classification | Evidence / reason |
|---|---|---|
| UC-006 | **A — Substantive** (Batch 03, promoted từ B) | SCR-003 fully authored: NAV-003 precondition gate (Strategy Instance pinned), read-only existing-run list (always visible), bounded interval input, stable run identity assignment visibly bound to interval + Strategy Instance + Strategy Definition Version + configuration/policy version, STATE-001/STATE-005 — matches `ux-blueprint.md` §7.3 SCR-003 spec + `use-case-workflow.md` UC-006 Main flow. |
| UC-007 | **A — Substantive** (Batch 03, promoted từ C) | SCR-004 Panel A fully authored: mỗi Decision hiển thị tách biệt tường minh (A) outcome LONG/SHORT/NO_ACTION, (B) upstream explainability (Strategy Instance/Definition Version/configuration/input snapshot/evaluation evidence), (C) downstream lineage khi tồn tại (Trade Intent/RiskEvaluation/Execution Intent) — RiskEvaluation LUÔN ở nhóm C, KHÔNG BAO GIỜ nhóm B (đúng `use-case-workflow.md` UC-007 v0.6, đóng `P03B-V05-B-MAJ-01`'s causal-direction fix). STATE-002/STATE-010 phân biệt tường minh. |
| UC-008 | **A — Substantive** (Batch 03, promoted từ C; v1.1 đóng `P2-B03-A-MAJ-01`) | SCR-004 Panel B fully authored: (1) simulated economic evidence per Decision→exposure-change; (2) ordered exposure/position progression theo thời gian xuyên suốt khoảng interval, `.progression-table` (#/Decision/Position before/Simulated change/Position after, một hàng/Decision, dẫn xuất deterministic từ `run.decisions`) — v1.0 chỉ có (1), (2) bị bỏ sót (`P2-B03-A-MAJ-01`, nay đóng); nhãn non-PAPER simulated tường minh, KHÔNG PAPER Order/ExecutionResult/Fill/Position tạo/tái sử dụng, STATE-009 khi zero exposure-changing Decision (progression KHÔNG render cho run này) — matches `ux-blueprint.md` §7.3 SCR-004 spec (b) + `use-case-workflow.md` UC-008 Main flow bước 1+2. |
| UC-009 | **A — Substantive** (Batch 03, promoted từ C) | SCR-004 Panel C fully authored: strategy-level evaluable result gắn CHÍNH XÁC run/version tuple, threshold-neutral (KHÔNG KPI/pass-fail/Sharpe/win-rate/profitability criterion — `OQ-003` unresolved, tường minh disclosed), STATE-009 khi thiếu evidence — matches `ux-blueprint.md` §7.3 SCR-004 spec (c) + `use-case-workflow.md` UC-009. |
| UC-010 | **A — Substantive** (Batch 03, promoted từ C) | SCR-005 fully authored: chọn hai run (select thật sự bind vào rendering), kết quả evaluable cạnh nhau giữ nguyên run/version identity riêng, KHÔNG gộp/aggregate, STATE-002 khi dưới hai run hoàn tất, STATE-009 per-run khi một run thiếu evidence (run khác vẫn hiển thị), deferred SCR-011 handoff (KHÔNG author substantively) — matches `ux-blueprint.md` §7.3 SCR-005 spec + `use-case-workflow.md` UC-010. |
| UC-001, UC-002, UC-003, UC-004, UC-005 | **A — Substantive** (Batch 01/02, giữ nguyên; v1.1 sửa provenance, đóng `P2-B03-A-MIN-01`) | SCR-001/VIEW-001/VIEW-002/SCR-002/VIEW-003 fully authored, VÀ ĐÃ independently verified — Batch 01 (Independent Review B verdict `READY_FOR_NEXT_PHASE2_BATCH`) VÀ Batch 02 v1.3 (Independent bounded Review B verdict `READY_FOR_NEXT_PHASE2_BATCH`, task-relayed baseline cho Batch 03 authoring, xem §2). Batch 03 CHỈ link tới Research/Replay (real nav link) VÀ simulate incoming context (QA panel) — KHÔNG re-author, NHƯNG cumulative classification VẪN A (một UC KHÔNG thể vừa A vừa B/C, đúng nguyên tắc đã đóng `P2-B02-A-MAJ-01`). |

## 2. Cumulative Phase-2 UC ledger (Batch 01 + Batch 02 + Batch 03 — ĐÃ independently verified, v1.2 bookkeeping reconciliation, Independent Review B v1.1 verdict READY_FOR_NEXT_PHASE2_BATCH)

**Recompute trực tiếp từ Batch 02's đã-verified partition (A=5/B=9/C=7, `../batch-02/traceability.md` §2) + Batch 03's năm UC mới promote lên A — KHÔNG suy diễn/copy hình dạng kỳ vọng nào mà KHÔNG verify:**

```text
Trước Batch 03 (Batch 01+02, đã verify mechanically tại ../batch-02/traceability.md §2):
  A = {001,002,003,004,005}                                  (5)
  B = {006,011,015,016,017,018,019,020,021}                  (9)
  C = {007,008,009,010,012,013,014}                          (7)

Batch 03 di chuyển UC-006 từ B → A (SCR-003 tự author đủ representation).
Batch 03 di chuyển UC-007,008,009,010 từ C → A (SCR-004 ba panel + SCR-005 tự author đủ
  representation).

Sau Batch 03:
  A = {001,002,003,004,005,006,007,008,009,010}              (10)
  B = {011,015,016,017,018,019,020,021}                       (8)
  C = {012,013,014}                                            (3)
```

```text
Partition validation (mechanical):
  |A| = 10, |B| = 8, |C| = 3.  10 + 8 + 3 = 21.  Đúng.
  A ∩ B: {001..010} ∩ {011,015,016,017,018,019,020,021} = ∅.  Đúng.
  A ∩ C: {001..010} ∩ {012,013,014} = ∅.  Đúng.
  B ∩ C: {011,015,016,017,018,019,020,021} ∩ {012,013,014} = ∅.  Đúng.
  A ∪ B ∪ C = {001..021} — liệt kê tuần tự xác nhận KHÔNG thiếu UC nào: 001(A) 002(A) 003(A)
    004(A) 005(A) 006(A) 007(A) 008(A) 009(A) 010(A) 011(B) 012(C) 013(C) 014(C) 015(B) 016(B)
    017(B) 018(B) 019(B) 020(B) 021(B) — 21 UC, mỗi UC xuất hiện ĐÚNG MỘT LẦN.

21-UC substantive completion progress: 10/21 (A only) — ĐÃ independently verified (v1.2
  bookkeeping reconciliation, 2026-08-14 — Batch 03's own bounded Review A re-review v1.1 CLEAN +
  Independent Review B v1.1 verdict `READY_FOR_NEXT_PHASE2_BATCH`, 0/0/0, đóng `P2-B03-A-MAJ-01`
  + `P2-B03-A-MIN-01`). Lifecycle VẪN CANDIDATE (verdict review ≠ lifecycle promotion). Nguồn cho
  từng UC:
    UC-001, UC-002, UC-003 — Batch 01 Independent Review B verdict READY_FOR_NEXT_PHASE2_BATCH.
    UC-004, UC-005 — Batch 02 v1.3 Independent bounded Review B verdict
      READY_FOR_NEXT_PHASE2_BATCH.
    UC-006, UC-007, UC-008, UC-009, UC-010 — Batch 03 v1.1 Independent Review B verdict
      READY_FOR_NEXT_PHASE2_BATCH.
  Minh bạch: ghi nhận chính thức verdict Batch 02 vào `batch-02/batch-manifest.md`'s own §17 (nay
  đã thực hiện, xem `../batch-02/batch-manifest.md` v1.4).
  Historical (TRƯỚC Batch 03's own review hoàn tất, giữ nguyên làm bằng chứng lịch sử): last
    independently verified 5/21 (Batch 01+02 only, v1.1's provenance-correction baseline).
```

## 3. Element-level traceability map

**Ghi chú:** cột "UC" liệt kê MỌI UC một element trace được về. SCR-004's ba panel trace RIÊNG BIỆT về UC-007/UC-008/UC-009 (KHÔNG gộp thành một hàng), VÀ nhóm A/B/C bên trong Panel A trace RIÊNG BIỆT (outcome / upstream / downstream) — đúng yêu cầu tường minh của transaction này.

| Prototype element (file:selector) | UX Blueprint / Domain ID | UC | PR | Authoritative source section |
|---|---|---|---|---|
| `index.html` `#shell`/`#context-bar` (bounded subset, reused convention) | WS-001 | UC-011, UC-001/UC-011, UC-002/UC-011, UC-011/UC-015 | PR-002, PR-003, PR-001, PR-016, PR-027 | `ux-blueprint.md` §5 "WS-001" table (same authority as Batch 01/02, re-derived independently in this batch's own files) |
| `index.html` `#nav-bar [data-nav="NAV-001"]` (Research, real link to `../batch-01/index.html`) | NAV-001 | UC-001 | PR-003, PR-015, PR-017 | `ux-blueprint.md` §5a "NAV-001"; genuine navigation to Batch 01's already-authored SCR-001, NOT a new representation |
| `index.html` `#nav-bar [data-nav="NAV-002"]` (Replay, real link to `../batch-02/index.html`) | NAV-002 | UC-002 (precondition), UC-004 | PR-001, PR-016, PR-008, PR-018, PR-020 | `ux-blueprint.md` §5a "NAV-002"; genuine navigation to Batch 02's already-authored SCR-002/VIEW-003, NOT a new representation |
| `index.html` `#nav-bar [data-nav="NAV-003"]` (Backtest, active) | NAV-003 | UC-002 (precondition), UC-006 | PR-001, PR-016, PR-021, PR-022, PR-023 | `ux-blueprint.md` §5a "NAV-003 — Backtest" |
| `index.html` `[data-nav="NAV-004"]`..`[data-nav="NAV-006"]` → `#screen-deferred` | NAV-004..NAV-006 (destination existence only) | see each NAV's own §5a traceability (unchanged from Batch 01/02's equivalent citation pattern) | — | `ux-blueprint.md` §5a; §3 UX-P-5 (read-only inspection navigation always available) |
| `app.js` `state.incomingContext` = `"incoming-no-instance"` / `renderStartFormSection()` blocked branch | NAV-003 "Required context"/"Available navigation behavior" (blocked/prompt), STATE-004 cited at NAV level | UC-002, UC-006 | PR-001, PR-021 | `ux-blueprint.md` §5a NAV-003; §11 STATE-004 row (Applicable screen/view = VIEW-001 — distinction preserved explicitly, same pattern as Batch 02's NAV-002) |
| `app.js` `renderRunListSection()` (read-only existing-run list, always visible) | NAV-003 "Read-only inspection behavior" | UC-006 | PR-021 | `ux-blueprint.md` §5a NAV-003 "Read-only inspection behavior" |
| `index.html` `#interval-select` / `app.js` `MOCK_INTERVALS` | SCR-003 "Available user actions" — nhập khoảng thời gian bounded | UC-006 | PR-021, PR-022, PR-023 | `ux-blueprint.md` §7.3 SCR-003 "Available user actions"; `use-case-workflow.md` UC-006 "Inputs" |
| `app.js` `renderStartFormSection()` normal branch (Strategy Instance/Definition Version/configuration display) | SCR-003 "Information displayed" | UC-006 | PR-021, PR-022, PR-023 | `ux-blueprint.md` §7.3 SCR-003 "Information displayed" |
| `app.js` `startBacktestRun()` STATE-005 blocked branch | STATE-005 missing historical evidence | UC-006 (alternate/failure) | PR-015, PR-021 | `ux-blueprint.md` §11 STATE-005 row; `use-case-workflow.md` UC-006 "Alternate/failure"; §8 "Missing historical evidence" |
| `app.js` `startBacktestRun()` success branch (stable run identity bound to interval + Strategy Instance + Strategy Definition Version + configuration/policy version) | SCR-003 "System-owned actions"; STATE-001 (transient) | UC-006 | PR-021, PR-022, PR-023 | `ux-blueprint.md` §7.3 SCR-003 "System-owned actions"; §11 STATE-001 row (SCR-003 listed applicable); `use-case-workflow.md` UC-006 Main flow steps 1–2 |
| `index.html` `#screen-scr-004` / `app.js` `renderScr004()` STATE-002 branch (empty run list) | STATE-002 empty | UC-007, UC-008, UC-009 | PR-021, PR-034 | `ux-blueprint.md` §11 STATE-002 row (SCR-004 "danh sách Backtest run rỗng") |
| `app.js` `renderScr004()` STATE-010 branch (unresolved run identity) | STATE-010 Backtest run identity unresolved | UC-007 (alternate/failure) | PR-021 | `ux-blueprint.md` §11 STATE-010 row; `use-case-workflow.md` UC-007 "Alternate/failure" (§8 "Backtest run identity does not resolve") |
| `app.js` `renderDecisionTrace()` `.outcome-badge` (group A — Decision outcome) | SCR-004 Panel (a), group A | UC-007 | PR-004, PR-021 | `use-case-workflow.md` UC-007 Main flow step 2A (decision.md §5e/§5b `result` enum LONG/SHORT/NO_ACTION) |
| `app.js` `renderDecisionTrace()` `.evidence-group-upstream` (group B — upstream Decision origin/explainability) | SCR-004 Panel (a), group B | UC-007 | PR-005, PR-009, PR-021 | `use-case-workflow.md` UC-007 Main flow step 2B — Strategy Instance/Definition Version/configuration, recorded input snapshot, recorded evaluation evidence, resolve TRỰC TIẾP từ recorded fact |
| `app.js` `renderDecisionTrace()` `.evidence-group-downstream` (group C — downstream lineage, incl. RiskEvaluation) | SCR-004 Panel (a), group C | UC-007 | PR-009, PR-021 | `use-case-workflow.md` UC-007 Main flow step 2C — Trade Intent/RiskEvaluation/Execution Intent, "causally derived from/related to Decision, KHÔNG PHẢI evidence dùng để tạo ra nó"; `risk.md` §1 (RiskEvaluation đánh giá Trade Intent SINH RA SAU Decision — RiskEvaluation LUÔN thuộc C, KHÔNG BAO GIỜ B, đóng cùng causal-direction requirement đã fix tại `P03B-V05-B-MAJ-01`) |
| `app.js` `renderDecisionTrace()` "Downstream lineage: none" branch (NO_ACTION) | SCR-004 Panel (a) | UC-007 | PR-021 | `use-case-workflow.md` UC-007; `decision.md` §10 "result = NO_ACTION → ZERO Trade Intent LUÔN LUÔN" |
| `app.js` `renderEconomicEvidence()` normal branch, `.lineage-list` rows (Decision → simulated exposure change, per changing Decision) | SCR-004 Panel (b) | UC-008 | PR-033 | `ux-blueprint.md` §7.3 SCR-004 "Information displayed" (b); `use-case-workflow.md` UC-008 Main flow bước 1 ("simulated economic evidence deterministic cho mỗi điểm Decision→simulated exposure change") |
| `app.js` `positionProgression()` / `.progression-table` (v1.1, đóng `P2-B03-A-MAJ-01` — ordered exposure/position progression, một hàng/Decision, TÁCH BIỆT khỏi hàng trên) | SCR-004 Panel (b) | UC-008 | PR-033 | `ux-blueprint.md` §7.3 SCR-004 "Information displayed" (b); `use-case-workflow.md` UC-008 Main flow bước 2 ("exposure/position progression theo thời gian trong suốt khoảng interval") — dẫn xuất deterministic từ `run.decisions`, KHÔNG fixture/entity mới, KHÔNG simulation engine |
| `app.js` `renderEconomicEvidence()` STATE-009 branch (KHÔNG progression nào render) | STATE-009 Backtest evidence insufficient | UC-008 (alternate/failure) | PR-033, PR-034 | `ux-blueprint.md` §11 STATE-009 row; `use-case-workflow.md` UC-008 "Alternate/failure" |
| `app.js` `renderEvaluableResult()` normal branch (strategy-level evaluable result, threshold-neutral) | SCR-004 Panel (c) | UC-009 | PR-034, PR-022 | `ux-blueprint.md` §7.3 SCR-004 "Information displayed" (c); `use-case-workflow.md` UC-009 Main flow — "KHÔNG threshold/target cụ thể (`OQ-003`)" |
| `app.js` `renderEvaluableResult()` STATE-009 branch | STATE-009 Backtest evidence insufficient | UC-009 (alternate/failure) | PR-034 | `ux-blueprint.md` §11 STATE-009 row; `use-case-workflow.md` UC-009 "Alternate/failure" |
| `index.html` `#btn-to-scr-005` ("Compare with another run") | SCR-004 "Exit points" (SCR-005) | UC-007, UC-008, UC-009, UC-010 | PR-034 | `ux-blueprint.md` §7.3 SCR-004 "Exit points" |
| `index.html` `#screen-scr-005` / `app.js` `renderScr005()` STATE-002 branch (fewer than two completed runs) | STATE-002 empty (SCR-005) | UC-010 | PR-021, PR-034 | `ux-blueprint.md` §11 STATE-002 row (SCR-005 "dưới hai Backtest run hoàn tất") |
| `app.js` `#compare-a-select`/`#compare-b-select` / `comparisonColumn()` (selects thật sự bind vào rendering) | SCR-005 "Available user actions"; "Information displayed" | UC-010 | PR-034 | `ux-blueprint.md` §7.3 SCR-005 "Available user actions"/"Information displayed"; `use-case-workflow.md` UC-010 Main flow |
| `app.js` `comparisonColumn()` STATE-009 per-column branch (một run thiếu evidence, run khác vẫn hiển thị) | STATE-009 Backtest evidence insufficient (per-run, SCR-005) | UC-010 (alternate/failure) | PR-034 | `ux-blueprint.md` §11 STATE-009 row; `use-case-workflow.md` UC-010 "Alternate/failure" |
| `index.html` "Continue to Improve (Strategy Definition Version comparison)" button → `#screen-deferred` | SCR-005 "Exit points" (SCR-011, deferred handoff only — SCR-011 KHÔNG authored substantively); NAV-006 nav-button-existence only | UC-010 | PR-034 | `ux-blueprint.md` §7.3 SCR-005 "Exit points"; §5a NAV-006 |
| Absence of any "Execute this Backtest Decision in Paper"/"Promote run to Paper"/"Convert Backtest Decision to Paper Decision"/reuse-Backtest-Fill-as-PAPER-Fill action anywhere in Batch 03 | SCR-003/SCR-004/SCR-005 "Out-of-scope boundary" (explicit prohibition); `FLOW-003` "KHÔNG action nào tự động chuyển Backtest Decision thành PAPER Decision" | UC-006, UC-007, UC-008, UC-009, UC-010 | PR-021, PR-022, PR-023, PR-004, PR-005, PR-009, PR-033, PR-034 | `ux-blueprint.md` §7.3 SCR-003/SCR-004/SCR-005 "Out-of-scope boundary"; §8 FLOW-003; `use-case-workflow.md` UC-006..UC-010 "Out-of-scope boundary" |
| `#screen-deferred` panel (Paper/Review/Improve) | (Batch-scoping placeholder — a prototype-batch concept, not a UX Blueprint state) | — | — | N/A — same convention as Batch 01/02, intentionally represents ONLY "not included in this batch" |
| `#qa-panel`/`#qa-body` (QA state switcher, incl. incoming-context simulation) | (Prototype tooling — explicitly NOT part of authoritative UX) | — | — | N/A — exists only to let every included STATE-XXX and NAV-003 precondition be inspected without the prototype pretending to compute real simulation/Decision/Risk logic |

## 4. Reconciliation statement (I-12 Verification)

```text
Mọi hàng ở §3 trên trace được, đối chiếu trực tiếp, về đúng một section cụ thể trong
  docs/product/ux-blueprint.md (Package 0.3-C, Consolidated Stable), docs/product/use-case-
  workflow.md (Package 0.3-B, Consolidated Stable, v0.6), hoặc docs/domain/decision.md/risk.md —
  đây LÀ "rebuild hoặc đối chiếu hoàn toàn từ authoritative source" per I-12's Verification
  (Chapter 2 §I-12).
KHÔNG một SCR-XXX/VIEW-XXX/NAV-XXX/FLOW-XXX/STATE-XXX/UC-XXX/PR-XXX ID nào xuất hiện trong Batch
  03 mà KHÔNG có hàng tương ứng ở §3.
KHÔNG một UC/PR/domain concept mới nào originate trong Batch 03 — verify trực tiếp: prototype/
  phase-2/batch-03/*.{html,css,js} KHÔNG tạo entity/event/state-machine mới (KHÔNG "BacktestOrder"/
  "BacktestExecutionResult"/"BacktestFill"/"BacktestPosition" entity — use-case-workflow.md UC-006/
  UC-008 Out-of-scope boundary xác nhận tường minh KHÔNG entity như vậy được tạo), KHÔNG author
  API/database/event contract, KHÔNG redefine Decision/Risk/Execution semantics, KHÔNG implement
  simulation/Decision/Risk engine (mọi Decision/RiskEvaluation/exposure-change value hardcoded
  deterministic fixture, KHÔNG computed), KHÔNG định nghĩa fee/slippage/accounting/PnL formula,
  KHÔNG định nghĩa KPI threshold/target/aggregate score (`OQ-003` unresolved, tường minh disclosed
  tại §3's evaluable-result row).
§2's cumulative UC ledger LÀ completion accounting (Chapter 12/phase-2-dod.md §3 purpose) —
  TÁCH BIỆT khỏi §3's element-to-authority traceability map (I-12 purpose). Mọi UC cited tại §3
  (element-level, cho phép multi-UC per element) đều resolve nhất quán vào ĐÚNG MỘT hạng mục tại
  §2's partition — verify trực tiếp, KHÔNG UC nào tại §3 rơi ngoài {A, B, C} đã định nghĩa tại §2.
```

## 5. Backtest/Paper authority separation (critical boundary, verified explicitly)

```text
Verified trực tiếp across prototype/phase-2/batch-03/*.{html,js}:
  - KHÔNG PAPER Order/ExecutionResult/Fill/Position được tạo hay tái sử dụng ở bất kỳ đâu — mọi
    "exposure change"/"position" label đều tường minh "simulated" + "Backtest" + "non-PAPER".
  - KHÔNG entity BacktestOrder/BacktestExecutionResult/BacktestFill/BacktestPosition được định
    nghĩa hay implied.
  - KHÔNG action "execute this Backtest Decision in Paper", "promote Backtest run to Paper",
    "convert Backtest Decision to Paper Decision", hay "reuse Backtest simulated Fill/Position as
    PAPER Fill/Position" tồn tại — SCR-004's "Compare with another run" CHỈ dẫn tới SCR-005
    (Backtest), KHÔNG dẫn tới SCR-006 (Paper); nav bar's "Paper" item VẪN chỉ dẫn tới
    #screen-deferred (đọc-only placeholder, giống hệt Batch 01/02's convention).
  - `FLOW-003` (Backtest → Paper handoff, Consolidated Stable, KHÔNG sửa) xác nhận judgment gate —
    "người dùng TỰ QUYẾT ĐỊNH", "KHÔNG action nào tự động chuyển Backtest Decision thành PAPER
    Decision" — Batch 03 KHÔNG author bất kỳ phần nào của FLOW-003's SCR-006-facing half (đúng
    "Do not expand into Paper").
```

## 6. Excluded-by-design (not a gap — batch-selection rule application)

```text
Surface accounting (v1.2 bookkeeping reconciliation — 8/17 nay ĐÃ independently verified, KHÔNG
  còn "candidate"):
  Batch 01+02 independently verified prior contribution:  SCR-001, VIEW-001, VIEW-002 (Batch 01,
                                                       Independent Review B `READY_FOR_NEXT_
                                                       PHASE2_BATCH`) + SCR-002, VIEW-003 (Batch
                                                       02 v1.3, Independent bounded Review B
                                                       `READY_FOR_NEXT_PHASE2_BATCH`) (5).
  Batch 03 independently verified contribution
    (v1.1, Independent Review B verdict
    `READY_FOR_NEXT_PHASE2_BATCH`):                     SCR-003, SCR-004, SCR-005 (3).
  Verified cumulative total:                           8/17.
  Remaining (17 − 8):                                  9/17 — SCR-006..SCR-011 (6) +
                                                       VIEW-004..VIEW-006 (3) = 9. KHÔNG author
                                                       trong Batch 03 — đúng batch-selection rule
                                                       ("do not author SCR-006/SCR-007," "do not
                                                       expand into Paper," "do not author SCR-011
                                                       substantively"). Nav/handoff affordance tồn
                                                       tại (dẫn tới #screen-deferred), substantive
                                                       screen content KHÔNG.
  Ghi nhận chính thức verdict Batch 02 vào batch-02's own `batch-manifest.md` §17 nay đã thực
    hiện (v1.4, transaction riêng, 2026-08-14).
  Historical (TRƯỚC Batch 03's own review hoàn tất): last independently verified 5/17 (Batch 01
    3 + Batch 02 2).
  Lifecycle VẪN CANDIDATE — verdict review (READY_FOR_NEXT_PHASE2_BATCH) ≠ lifecycle promotion.

11 of 21 UC KHÔNG substantively covered (§2 ledger — B=8, C=3, KHÔNG collapse thành một bucket,
  đúng lesson từ Batch 01's `P2-B01-A-MIN-01`, VÀ KHÔNG double-count bất kỳ UC nào vào cả hai
  hạng mục, đúng lesson từ `P2-B02-A-MAJ-01`):
  B — Partial/referenced (8): UC-011, UC-015, UC-016, UC-017, UC-018, UC-019, UC-020, UC-021.
  C — Deferred/not yet represented (3): UC-012, UC-013, UC-014.
```
