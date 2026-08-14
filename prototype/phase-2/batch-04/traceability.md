---
id: phase-2-batch-04-traceability
title: "Phase 2 Prototype — Batch 04 — Traceability Artifact"
version: "1.0"
status: Candidate
owner: Product Owner
created_at: "2026-08-14"
---

# Phase 2 Prototype — Batch 04 — Traceability Artifact

**Vai trò của tài liệu này:** đây LÀ I-12 (Single Source of Truth) conformance evidence cho Batch 04, per `docs/phase-dod/phase-2-dod.md` §2's applicable Trigger A / I-12 requirement — mọi phần tử prototype trong batch này PHẢI trace được TRỰC TIẾP về đúng một hoặc nhiều `SCR-XXX`/`NAV-XXX`/`STATE-XXX` đã `Consolidated Stable` trong [`docs/product/ux-blueprint.md`](../../../docs/product/ux-blueprint.md), VÀ về đúng `UC-XXX` đã `Consolidated Stable` trong [`docs/product/use-case-workflow.md`](../../../docs/product/use-case-workflow.md), VÀ về đúng `PR-XXX`/Domain Contract field đã tồn tại. Prototype LÀ derived representation — KHÔNG một UC/PR/domain concept nào originate tại đây. Áp dụng ĐÚNG taxonomy A/B/C đã establish tại `../batch-01/traceability.md` §0, kế thừa nguyên vẹn qua Batch 02/03.

## 0. UC accounting taxonomy (kế thừa nguyên vẹn từ Batch 01/02/03, KHÔNG redefine)

```text
A. SUBSTANTIVELY COVERED — Batch tự author ĐỦ representation (screen/view + required context +
   primary/blocked states + exit behavior đúng ux-blueprint.md/use-case-workflow.md spec) để tính
   vào 21-UC completion numerator (phase-2-dod.md §3).
B. PARTIAL / REFERENCED — UC xuất hiện qua global shell context, nav-button existence, handoff
   affordance, hay deferred-placeholder destination — KHÔNG đủ để tính vào numerator.
C. DEFERRED / NOT YET REPRESENTED — KHÔNG một element nào trong batch tham chiếu UC đó.
```

## 1. Batch-04-authored substantive contribution (distinct từ cumulative ledger, §2 dưới)

```text
Batch-04-authored substantive UC (NEW tại batch này, 5):
  UC-011 (SCR-006 — Paper initiation, upstream Decision evidence, precondition/Risk truncation)
  UC-012 (SCR-007 ExecutionResult tab — EXECUTED/NOT_EXECUTED)
  UC-013 (SCR-007 Fill tab — economics + simulation evidence)
  UC-014 (SCR-007 Position tab — FLAT/LONG/SHORT/NON_EVALUABLE)
  UC-015 (SCR-007 No-real-exchange tab)

UC-011 was previously hạng B (referenced only via NAV-004's nav-button-existence citation, Batch
  01/02/03) — nay promote lên A vì SCR-006 tự author đủ representation (bốn precondition riêng
  biệt, upstream Decision evidence tách biệt downstream causation, initiation control thật sự
  drive state, branch truncation chính xác) đúng `ux-blueprint.md` §7.4 SCR-006 spec VÀ
  `use-case-workflow.md` UC-011 detailed block.
UC-012/013/014/015 previously hạng B (UC-015 via WS-001/STATE-027 citation) hoặc C (UC-012/013/
  014, zero reference) — nay promote lên A vì SCR-007 tự author đủ representation (bốn panel
  tách biệt) đúng `ux-blueprint.md` §7.4 SCR-007 spec VÀ `use-case-workflow.md` UC-012/013/014/
  015 detailed block.

Batch-01/02/03-verified substantive UC (KHÔNG re-authored, KHÔNG double-counted, VẪN A):
  UC-001..UC-010.
```

| UC | Classification | Evidence / reason |
|---|---|---|
| UC-011 | **A — Substantive** (Batch 04, promoted từ B) | SCR-006 fully authored: bốn precondition tách biệt (STATE-003/028/029/011), upstream PAPER Decision evidence (outcome/Strategy Instance/Definition Version/recorded input snapshot) hiển thị TRƯỚC initiation, tách biệt tường minh khỏi downstream causation; initiate-intent control (KHÔNG order payload input) thật sự drive `state.execution`; Risk APPROVED/REJECTED (STATE-013)/NON_EVALUABLE (STATE-014) branch truncation chính xác — matches `ux-blueprint.md` §7.4 SCR-006 spec + `use-case-workflow.md` UC-011 Main flow. |
| UC-012 | **A — Substantive** (Batch 04, promoted từ C) | SCR-007 ExecutionResult tab fully authored: STATE-015 EXECUTED / STATE-016 NOT_EXECUTED (zero Fill explicit), gắn đúng Order/OrderSubmissionRequest identity, environment=PAPER — matches `ux-blueprint.md` §7.4 SCR-007 spec (a) + `use-case-workflow.md` UC-012. |
| UC-013 | **A — Substantive** (Batch 04, promoted từ C) | SCR-007 Fill tab fully authored: fill_quantity/fill_price/price_currency + bốn trục simulation evidence (policy/configuration/build/deterministic-input ref), khớp CÙNG PaperExecutionObservation với ExecutionResult tab (`execution_observation_id` equality, `fill.md` v0.2); STATE-017 Fill absent khi NOT_EXECUTED — matches `ux-blueprint.md` §7.4 SCR-007 spec (b) + `use-case-workflow.md` UC-013. |
| UC-014 | **A — Substantive** (Batch 04, promoted từ C) | SCR-007 Position tab fully authored: STATE-018 FLAT/STATE-019 LONG/STATE-020 SHORT (net_quantity/average_entry_price khi applicable) + STATE-021 NON_EVALUABLE (`contributing_fill_refs` đầy đủ, KHÔNG chọn một Fill/aggregate/report FLAT sai) — matches `ux-blueprint.md` §7.4 SCR-007 spec (c) + `use-case-workflow.md` UC-014 + `position.md` §1/§2. |
| UC-015 | **A — Substantive** (Batch 04, promoted từ B) | SCR-007 No-real-exchange tab fully authored: environment=PAPER confirmation, "no real exchange order placed," "no real network route trong prototype này" — KHÔNG tuyên bố một network audit kỹ thuật đã chạy — matches `ux-blueprint.md` §7.4 SCR-007 spec (d) + `use-case-workflow.md` UC-015. |
| UC-001..UC-010 | **A — Substantive** (Batch 01/02/03, giữ nguyên) | Fully authored + independently verified tại Batch 01/02/03 (mỗi batch tự nó qua đầy đủ Review A + Independent Review B, verdict `READY_FOR_NEXT_PHASE2_BATCH`). Batch 04 CHỈ link tới Research/Replay/Backtest (real nav link) — KHÔNG re-author, NHƯNG cumulative classification VẪN A (một UC KHÔNG thể vừa A vừa B/C). |

## 2. Cumulative Phase-2 UC ledger (Batch 01 + Batch 02 + Batch 03 + Batch 04, candidate — Batch 04's own +5 CHƯA independently verified)

```text
Trước Batch 04 (Batch 01+02+03, ĐÃ independently verified — xem ../batch-03/traceability.md §2):
  A = {001,002,003,004,005,006,007,008,009,010}              (10)
  B = {011,015,016,017,018,019,020,021}                        (8)
  C = {012,013,014}                                             (3)

Batch 04 di chuyển UC-011,015 từ B → A (SCR-006/SCR-007 tự author đủ representation).
Batch 04 di chuyển UC-012,013,014 từ C → A (SCR-007 ba panel còn lại tự author đủ
  representation).

Sau Batch 04:
  A = {001,002,003,004,005,006,007,008,009,010,011,012,013,014,015}    (15)
  B = {016,017,018,019,020,021}                                          (6)
  C = {}                                                                  (0)
```

```text
Partition validation (mechanical):
  |A| = 15, |B| = 6, |C| = 0.  15 + 6 + 0 = 21.  Đúng.
  A ∩ B: {001..015} ∩ {016,017,018,019,020,021} = ∅.  Đúng.
  A ∩ C: {001..015} ∩ {} = ∅.  Đúng (trivial).
  B ∩ C: {016,017,018,019,020,021} ∩ {} = ∅.  Đúng (trivial).
  A ∪ B ∪ C = {001..021} — liệt kê tuần tự xác nhận KHÔNG thiếu UC nào: 001..015 (A, 15 liên
    tiếp) 016(B) 017(B) 018(B) 019(B) 020(B) 021(B) — 21 UC, mỗi UC xuất hiện ĐÚNG MỘT LẦN.

21-UC substantive completion progress: BA trạng thái tách biệt, KHÔNG conflate:
  Candidate (sau Batch 04 authoring):               15/21 (A only) — CHƯA independently verified
                                                     (chờ Review A + Independent Review B trên
                                                     Batch 04, đúng P2-PROTOTYPE-001).
  Last INDEPENDENTLY VERIFIED (Batch 01+02+03,
    mỗi batch tự nó qua đầy đủ Review A +
    Independent Review B, verdict
    READY_FOR_NEXT_PHASE2_BATCH):                    10/21 (UC-001..010).
```

## 3. Element-level traceability map

**Ghi chú:** cột "UC" liệt kê MỌI UC một element trace được về. SCR-006 trace RIÊNG BIỆT theo mười khía cạnh yêu cầu (pin/precondition, Account/Instrument/Venue validity, upstream Decision evidence, initiate-intent control, Risk APPROVED/REJECTED/NON_EVALUABLE, PAPER Decision unavailable, downstream causal chain, PAPER/non-Live boundary). SCR-007 trace RIÊNG BIỆT theo tám khía cạnh yêu cầu (ExecutionResult, NOT_EXECUTED/zero Fill, Fill economics, Fill simulation evidence, Position bốn trạng thái, no-real-exchange, STATE-002 empty, Review handoff) — KHÔNG một hàng gộp nào cho UC-012..UC-015.

| Prototype element (file:selector) | UX Blueprint / Domain ID | UC | PR | Authoritative source section |
|---|---|---|---|---|
| `index.html` `#shell`/`#context-bar` (bounded subset, reused convention) | WS-001 | UC-011, UC-001/UC-011, UC-002/UC-011, UC-011/UC-015 | PR-002, PR-003, PR-001, PR-016, PR-027 | `ux-blueprint.md` §5 "WS-001" table (same authority as Batch 01/02/03, re-derived independently in this batch's own files) |
| `index.html` `[data-nav="NAV-001"]`/`[NAV-002]`/`[NAV-003]` (real links to Batch 01/02/03) | NAV-001, NAV-002, NAV-003 | UC-001, UC-002 (precondition), UC-004, UC-006 | PR-003, PR-015, PR-017, PR-001, PR-016, PR-008, PR-018, PR-020, PR-021, PR-022, PR-023 | `ux-blueprint.md` §5a NAV-001/002/003; genuine navigation to already-authored Batch 01/02/03 screens, NOT a new representation |
| `index.html` `[data-nav="NAV-004"]` (Paper, active) | NAV-004 | UC-002 (precondition), UC-011 | PR-001, PR-006, PR-007, PR-016, PR-024 | `ux-blueprint.md` §5a "NAV-004 — Paper" |
| `index.html` `[data-nav="NAV-005"]`/`[NAV-006]` → `#screen-deferred` | NAV-005, NAV-006 (destination existence only) | see each NAV's own §5a traceability | — | `ux-blueprint.md` §5a; §3 UX-P-5 (read-only inspection navigation always available) |
| `app.js` `state.accountValid = false` / `renderScr006()` STATE-003 branch | STATE-003 invalid Account/Instrument/Venue | UC-011 | PR-003 | `ux-blueprint.md` §11 STATE-003 row (SCR-006 applicable); §5a NAV-004 "Blocked behavior" |
| `app.js` `state.paperPin = "none"` / `renderScr006()` STATE-028 branch, incl. `#btn-select-pin` bounded local pin fixture | STATE-028 Paper Strategy Instance not selected; NAV-004 "provides an entry point to VIEW-001," bounded, NOT re-authored | UC-002 (precondition), UC-011 | PR-001, PR-016 | `ux-blueprint.md` §11 STATE-028 row; §7.4 SCR-006 "Entry points" ("nếu chưa có Strategy Instance pin cho Paper, NAV-004 mở SCR-006 ở STATE-028 và cung cấp lối vào VIEW-001") |
| `app.js` `state.paperPin = "selected"` / `renderScr006()` STATE-029 branch | STATE-029 Paper Strategy Instance selected but not pinned | UC-002 (precondition), UC-011 | PR-001, PR-016 | `ux-blueprint.md` §11 STATE-029 row |
| `app.js` `state.decisionAvailable = false` / `renderScr006()` STATE-011 branch | STATE-011 PAPER Decision lineage unavailable | UC-011 (alternate/failure) | PR-024 | `ux-blueprint.md` §11 STATE-011 row; `use-case-workflow.md` UC-011 "Alternate/failure" |
| `app.js` `MOCK_PAPER_DECISION` / `.evidence-group-upstream` block in `renderScr006()` | SCR-006 "Information displayed" — upstream Decision evidence shown BEFORE initiation | UC-011 | PR-004, PR-005 | `ux-blueprint.md` §7.4 SCR-006 "Information displayed"/"Required context"; `use-case-workflow.md` UC-011 Main flow bước 2 (upstream evidence, tách biệt downstream causation) |
| `index.html` `#btn-initiate` / `app.js` `buildExecutionChain()` call | SCR-006 "Available user actions" — initiate-intent (KHÔNG order payload) | UC-011 | PR-007, PR-024 | `ux-blueprint.md` §7.4 SCR-006 "Available user actions"/"Out-of-scope boundary" (KHÔNG order type/sizing/fee/slippage UI) |
| `app.js` `buildExecutionChain()` `riskOutcome === "APPROVED"` branch (continues downstream) | RiskEvaluation APPROVED — chain continues | UC-011 | PR-006, PR-014 | `ux-blueprint.md` §7.4 SCR-006 "Primary states"; `use-case-workflow.md` UC-011 Main flow bước 4-5 |
| `app.js` `buildExecutionChain()` `riskOutcome === "REJECTED"` branch / `renderInitiationResult()` STATE-013 | STATE-013 Risk REJECTED | UC-011 (alternate/failure) | PR-006, PR-014 | `ux-blueprint.md` §11 STATE-013 row; `use-case-workflow.md` UC-011 "Alternate/failure" |
| `app.js` `buildExecutionChain()` `riskOutcome === "NON_EVALUABLE"` branch / `renderInitiationResult()` STATE-014 | STATE-014 Risk NON_EVALUABLE | UC-011 (alternate/failure) | PR-006, PR-014 | `ux-blueprint.md` §11 STATE-014 row; `use-case-workflow.md` UC-011 "Alternate/failure" |
| `app.js` `buildExecutionChain()` full (Trade Intent → RiskEvaluation → Execution Intent → Order → OrderSubmissionRequest → ExecutionResultComputation → PaperExecutionObservation → ExecutionResult → Fill) | SCR-006 "System-owned actions"/"Evidence produced" — downstream causal chain, system-owned throughout | UC-011 | PR-007, PR-024 | `ux-blueprint.md` §7.4 SCR-006 "System-owned actions"; `use-case-workflow.md` UC-011 Main flow bước 3-9 |
| `index.html` `.mode-label`/`.authority-label-authoritative` ("Paper"/"authoritative PAPER") + `#ctx-live` static "Unauthorized" badge | SCR-006/SCR-007 "Authority labels"; STATE-027 Live unauthorized (global, reused convention) | UC-011, UC-015 | PR-001, PR-016, PR-027 | `ux-blueprint.md` §7.4 SCR-006/SCR-007 "Authority labels"; §11 STATE-027 row |
| Absence of any "Execute this Backtest Decision in Paper"/"Promote Backtest Decision"/"Convert Backtest result to PAPER Decision" action, and absence of quantity/order-type/sizing/fee/slippage input anywhere in Batch 04 | SCR-006 "Available user actions"/"Out-of-scope boundary" (explicit prohibition) | UC-011 | PR-001, PR-004, PR-005, PR-006, PR-007, PR-016, PR-024 | `ux-blueprint.md` §7.4 SCR-006 "Out-of-scope boundary"; `use-case-workflow.md` UC-011 "Out-of-scope boundary" |
| `app.js` `renderScr007()` STATE-002 branch (no `state.execution.order`) | STATE-002 empty | UC-012, UC-013, UC-014 | PR-021, PR-034 | `ux-blueprint.md` §11 STATE-002 row (SCR-007 "chưa Order/Fill nào tồn tại") |
| `app.js` `renderExecutionResultTab()` STATE-015 branch | STATE-015 ExecutionResult EXECUTED | UC-012 | PR-007, PR-014, PR-024 | `ux-blueprint.md` §11 STATE-015 row; `use-case-workflow.md` UC-012 Main flow |
| `app.js` `renderExecutionResultTab()` STATE-016 branch (zero Fill explicit) | STATE-016 ExecutionResult NOT_EXECUTED | UC-012 (alternate/failure) | PR-007, PR-014, PR-024 | `ux-blueprint.md` §11 STATE-016 row; `use-case-workflow.md` UC-012 "Alternate/failure" — "người dùng thấy rõ zero Fill kèm theo" |
| `app.js` `renderFillTab()` economics rows (`f.quantity`/`f.price`/`f.priceCurrency`) | SCR-007 Panel (b) — Fill economics | UC-013 | PR-025 | `ux-blueprint.md` §7.4 SCR-007 "Information displayed" (b); `fill.md` §1 (`fill_quantity`/`fill_price`/`price_currency`, copied exactly from Observation) |
| `app.js` `renderFillTab()` `.simulation-table` (policy/configuration/build/deterministic-input ref) | SCR-007 Panel (b) — Fill simulation evidence, matching same PaperExecutionObservation | UC-013 | PR-025 | `execution-result.md` §1 PaperExecutionObservation (`simulation_policy_ref`/`simulation_configuration_ref`/`simulation_build_ref`/`deterministic_input_ref`); `use-case-workflow.md` UC-013 Main flow — "khớp byte-for-byte PaperExecutionObservation gốc" |
| `app.js` `renderFillTab()` STATE-017 branch | STATE-017 Fill absent | UC-013 (alternate/failure) | PR-025 | `ux-blueprint.md` §11 STATE-017 row; `use-case-workflow.md` UC-013 "Alternate/failure" |
| `app.js` `renderPositionTab()` STATE-018 branch (FLAT) | STATE-018 Position FLAT | UC-014 | PR-026 | `ux-blueprint.md` §11 STATE-018 row; `position.md` §2 fold algorithm bước 3 (zero eligible Fill) |
| `app.js` `renderPositionTab()` STATE-019/STATE-020 branches (LONG/SHORT) | STATE-019/STATE-020 Position LONG/SHORT | UC-014 | PR-026 | `ux-blueprint.md` §11 STATE-019/020 rows; `position.md` §2 fold algorithm bước 4 (`net_quantity`/`average_entry_price` = Fill's) |
| `app.js` `derivePosition()` `positionDemoOverride === "non-evaluable"` / `renderPositionTab()` STATE-021 branch (QA demo, tường minh disclosed KHÔNG PHẢI real product path) | STATE-021 Position NON_EVALUABLE | UC-014 (alternate/failure) | PR-026 | `ux-blueprint.md` §11 STATE-021 row; `position.md` §1/§2 (`projection_status = NON_EVALUABLE`, `contributing_fill_refs` bắt buộc, KHÔNG chọn một Fill/aggregate/report FLAT) |
| `app.js` `renderSafetyTab()` (always available regardless of chain state) | SCR-007 Panel (d) — no-real-exchange confirmation | UC-015 | PR-027 | `ux-blueprint.md` §7.4 SCR-007 "Information displayed" (d); `use-case-workflow.md` UC-015 Main flow — environment field trên Order/ExecutionResult |
| `index.html` "Continue to Review" button → `#screen-deferred` | SCR-007 "Exit points" (SCR-008, deferred handoff only — SCR-008 KHÔNG authored substantively); NAV-005 nav-button-existence only | UC-012, UC-013, UC-014, UC-015 | PR-007, PR-025, PR-026, PR-027 | `ux-blueprint.md` §7.4 SCR-007 "Exit points"; §5a NAV-005 |
| `#screen-deferred` panel (Review/Improve) | (Batch-scoping placeholder — a prototype-batch concept, not a UX Blueprint state) | — | — | N/A — same convention as Batch 01/02/03, intentionally represents ONLY "not included in this batch" |
| `#qa-panel`/`#qa-body` (QA state switcher) | (Prototype tooling — explicitly NOT part of authoritative UX) | — | — | N/A — exists only to let every included STATE-XXX be inspected without the prototype pretending to compute real Risk/execution logic |

## 4. Reconciliation statement (I-12 Verification)

```text
Mọi hàng ở §3 trên trace được, đối chiếu trực tiếp, về đúng một section cụ thể trong
  docs/product/ux-blueprint.md (Package 0.3-C, Consolidated Stable), docs/product/use-case-
  workflow.md (Package 0.3-B, Consolidated Stable), hoặc Domain Contract tương ứng
  (decision.md/trade-intent.md/risk.md/execution-intent.md/order.md/execution-result.md/
  fill.md/position.md) — đây LÀ "rebuild hoặc đối chiếu hoàn toàn từ authoritative source" per
  I-12's Verification (Chapter 2 §I-12).
KHÔNG một NAV-XXX/SCR-XXX/STATE-XXX/UC-XXX/PR-XXX ID nào xuất hiện trong Batch 04 mà KHÔNG có
  hàng tương ứng ở §3.
KHÔNG một UC/PR/domain concept mới nào originate trong Batch 04 — verify trực tiếp: prototype/
  phase-2/batch-04/*.{html,css,js} KHÔNG tạo entity/event/state-machine mới (KHÔNG "PaperSession"
  entity, KHÔNG Order/RiskEvaluation/ExecutionResult/Fill/Position schema riêng — mọi identity là
  hardcoded illustrative string, KHÔNG API/database/event contract), KHÔNG implement Risk/
  execution/simulation engine (mọi outcome QA-selected fixture, KHÔNG computed), KHÔNG định nghĩa
  cơ chế thiết lập PAPER-context Decision (deferred domain/workflow dependency, giữ nguyên
  unresolved), KHÔNG clone/carry-forward/promote Backtest Decision.
§2's cumulative UC ledger LÀ completion accounting (Chapter 12/phase-2-dod.md §3 purpose) —
  TÁCH BIỆT khỏi §3's element-to-authority traceability map (I-12 purpose). Mọi UC cited tại §3
  đều resolve nhất quán vào ĐÚNG MỘT hạng mục tại §2's partition — verify trực tiếp, KHÔNG UC nào
  tại §3 rơi ngoài {A, B} đã định nghĩa tại §2 (C rỗng sau Batch 04).
```

## 5. Five non-negotiable PAPER invariants — verified explicitly

```text
INV-1 (PAPER Decision distinct): verified — traceability.md §1's UC-011 row + §3's "Absence of
  any... action" row. No Execute-in-Paper/Promote/Convert/Clone action exists anywhere; no
  Backtest economic evidence reused as PAPER ExecutionResult/Fill/Position; the PAPER-context
  Decision's creation mechanism is not defined (deferred).
INV-2 (user supplies intent only): verified — SCR-006's "Available user actions" row; zero
  quantity/order-type/sizing/fee/slippage/execution-model input exists anywhere in
  index.html/app.js (verified directly, grep clean for any such input field).
INV-3 (upstream vs downstream): verified — `.evidence-group-upstream` shown BEFORE initiation,
  visually distinct (border-left style, separate section) from `renderInitiationResult()`'s
  downstream causation, shown only AFTER the initiate button is clicked. RiskEvaluation never
  appears in the upstream evidence group.
INV-4 (exact branch truncation): verified — `buildExecutionChain()`'s REJECTED/NON_EVALUABLE
  branches `return` immediately after setting `riskEvaluation`, before `executionIntent`/`order`/
  `submissionRequest`/`executionResult`/`fill` are ever assigned (all remain `null`).
  NOT_EXECUTED returns before `fill` is assigned. EXECUTED assigns exactly one `fill` object.
INV-5 (identity continuity + Position semantics): verified — SCR-006 and SCR-007 read the SAME
  `MOCK_STRATEGY_CONTEXT`/`MOCK_ACCOUNT_CONTEXT`/`MOCK_PAPER_DECISION`/`state.execution` objects
  (single shared JS module scope, single page) — no teleportation between screens. `derivePosition()`
  never labels Position as an authoritative fact (hint text quotes position.md §1 explicitly);
  NON_EVALUABLE is never guessed/collapsed/aggregated (dedicated branch, `contributing_fill_refs`
  always present when NON_EVALUABLE).
```
