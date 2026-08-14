---
id: phase-2-batch-04-traceability
title: "Phase 2 Prototype — Batch 04 — Traceability Artifact"
version: "1.3"
status: Candidate
owner: Product Owner
created_at: "2026-08-14"
---

# Phase 2 Prototype — Batch 04 — Traceability Artifact

**v1.2 — bounded correction (2026-08-14), Independent Review B trên v1.1: `P2-B04-B-MAJ-01` (Major) + `P2-B04-B-MAJ-02` (Major) — đóng CẢ HAI tại transaction này (`P2-B04-A-MAJ-01`/`P2-B04-A-MAJ-02` từ v1.1 xác nhận CLOSED, KHÔNG reopen).** `P2-B04-B-MAJ-01`: STATE-020/Position SHORT KHÔNG materially reachable — `MOCK_PAPER_DECISION.outcome = "LONG"` cố định, `derivePositionNatural()` đọc trực tiếp từ đó, nhánh render SHORT LÀ dead code. Sửa: thay MỘT Decision fixture bằng `MOCK_PAPER_DECISIONS.LONG`/`MOCK_PAPER_DECISIONS.SHORT` — hai illustrative PAPER-context Decision fact RIÊNG BIỆT (cùng Strategy Instance pinned, khác Decision identity/outcome/input snapshot/evaluation evidence), chọn qua QA (`state.paperDecisionScenario`). `buildExecutionChain()` nay nhận decision LÀM tham số, gán `chain.fill.direction = decision.outcome` (field CÓ THẬT trong `fill.md` schema, trước đây bị bỏ sót) — `derivePositionNatural()` nay đọc `execution.fill.direction` (KHÔNG một global mutable) → SHORT scenario tạo ra Fill direction=SHORT → Position SHORT materially reachable qua tương tác thật. `P2-B04-B-MAJ-02`: sau khi một execution đã tạo, QA có thể mutate `paperPin`/`decisionAvailable`/`accountValid` MÀ KHÔNG invalidate `state.execution` — SCR-007 hiển thị "Strategy Instance (pinned, continuous from SCR-006)" trong khi context bar hiện tại nói "not pinned"/"selected-not-pinned" — mâu thuẫn current-state. Sửa: áp dụng preferred minimal model — `CONTEXT_MUTATION_KEYS` (Account/Instrument/Venue validity, Paper Strategy Instance selection/pin, PAPER Decision availability, PAPER Decision scenario LONG/SHORT) invalidate `state.execution` (set `null`) khi thay đổi; SCR-007 quay về STATE-002 cho tới khi một initiation MỚI xảy ra dưới context (có thể đã đổi) đó. Risk/execution-outcome QA keys (NEXT-initiation scenario) VÀ Position-demo-mode key KHÔNG nằm trong `CONTEXT_MUTATION_KEYS` — KHÔNG retroactively mutate execution đã tạo, đúng yêu cầu tường minh. SCR-007's Decision lineage row nay đọc snapshot `execution.decisionId`/`execution.decisionOutcome` (bound tại thời điểm chain được build), KHÔNG global hiện tại. KHÔNG PaperSession entity, KHÔNG production session/context invalidation semantics — prototype-local demo-state hygiene only. KHÔNG đổi A/B/C partition, KHÔNG surface mới, KHÔNG UC/PR/domain concept mới.

**v1.3 — deterministic bookkeeping reconciliation (2026-08-14), vai trò: `Phase 2 Prototype Batch 04 Review-State Reconciliation Executor`, đúng `G-TXN-003`.** KHÔNG PHẢI lifecycle transition, KHÔNG PHẢI prototype semantic correction. §2's tiêu đề VÀ kết luận vẫn nói "candidate — Batch 04's own +5 CHƯA independently verified" / "CHƯA independently verified (chờ Review A + Independent Review B trên Batch 04)" — mâu thuẫn trực tiếp với governed review history ĐÃ hoàn tất từ v1.2 (final bounded Review A v1.2: bốn finding tất cả CLOSED, 0/0/0, CLEAN; final Independent Review B v1.2: cùng bốn finding CLOSED, 0/0/0, verdict `READY_FOR_NEXT_PHASE2_BATCH`). Sửa: §2's tiêu đề + kết luận viết lại để phản ánh 15/21 ĐÃ independently verified. KHÔNG đổi §0/§1/§3/§4/§5 (A/B/C partition, element-level map, reconciliation statement, năm PAPER invariant verification KHÔNG đổi — VẪN A=15/B=6/C=0/tổng=21).

**v1.1 — bounded correction (2026-08-14), Review A trên v1.0: `P2-B04-A-MAJ-01` (Major) + `P2-B04-A-MAJ-02` (Major) — đóng CẢ HAI tại transaction này.** `P2-B04-A-MAJ-01`: `buildExecutionChain()` v1.0 bỏ qua hai domain concept riêng biệt bắt buộc theo `execution-result.md` — `ExecutionResultComputation` (§2, authorized computation identity/binding fact) VÀ `PaperExecutionObservation` (§1, simulation evidence bốn trục + economics) — ExecutionResult v1.0 chỉ mang một chuỗi `observationId` rời rạc, Fill mang `executionObservationId` riêng, KHÔNG một entity `paperExecutionObservation` nào thực sự tồn tại trong chain object. Sửa: thêm `chain.executionResultComputation` (id/computationPurpose/orderId/submissionRequestId/computationCursor, đúng schema §2) VÀ `chain.paperExecutionObservation` (id/executionResultComputationId/orderId/submissionRequestId/observationCursor/bốn trục simulation evidence/resultType/economics khi EXECUTED, đúng schema §1) LÀ hai node riêng biệt giữa OrderSubmissionRequest VÀ ExecutionResult. Fill's economics (`quantity`/`price`/`priceCurrency`) nay literally copy từ `paperExecutionObservation`'s field (KHÔNG một literal độc lập thứ hai) — khớp `fill.md` v0.2's invariant "PHẢI BẰNG HỆT Observation" tại code level. REJECTED/NON_EVALUABLE branch VẪN KHÔNG tạo Computation/Observation nào (`return` sớm trước khi hai node này được gán). NOT_EXECUTED: Computation + Observation tồn tại (`resultType: NOT_EXECUTED`, economics field absent đúng invariant), ExecutionResult copy `resultType`, zero Fill. SCR-006's `renderInitiationResult()` VÀ SCR-007's `renderExecutionResultTab()`/`renderFillTab()` cập nhật hiển thị hai identity mới LÀM supporting evidence (KHÔNG biến SCR-007 thành computation-debugging surface — chỉ thêm hai hàng identity). `P2-B04-A-MAJ-02`: `derivePosition()`'s NON_EVALUABLE demo v1.0 fabricate `FILL-002` KHÔNG có evidence basis, VÀ có thể render dù execution hiện tại LÀ NOT_EXECUTED (zero Fill) — mâu thuẫn trực tiếp với Fill/ExecutionResult tab. Sửa: NON_EVALUABLE demo nay CHỈ render khi execution hiện tại thực sự có Fill (EXECUTED) — `contributing_fill_refs` khi đó ghép Fill THẬT của execution hiện tại VỚI một `MOCK_PRIOR_FILL_LABEL` illustrative prior Fill được disclose tường minh (KHÔNG một Fill hiện tại thứ hai không giải thích). Khi override được chọn nhưng execution hiện tại KHÔNG có Fill, override KHÔNG áp dụng — trạng thái Position THẬT được hiển thị thay thế (KHÔNG collapse cưỡng bức về FLAT — chỉ LÀ trạng thái thật sự đúng lúc đó), kèm `demoNote` giải thích tường minh lý do. KHÔNG đổi A/B/C partition, KHÔNG surface mới, KHÔNG UC/PR/domain concept mới, KHÔNG order-sizing/fee/slippage engine.

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
| UC-011 | **A — Substantive** (Batch 04, promoted từ B; v1.1 đóng `P2-B04-A-MAJ-01`; v1.2 đóng `P2-B04-B-MAJ-01`/`P2-B04-B-MAJ-02`) | SCR-006 fully authored: bốn precondition tách biệt (STATE-003/028/029/011), upstream PAPER Decision evidence (outcome/Strategy Instance/Definition Version/recorded input snapshot) hiển thị TRƯỚC initiation, tách biệt tường minh khỏi downstream causation — nay chọn được giữa HAI Decision fixture riêng biệt (`PD-LONG-001`/`PD-SHORT-001`, v1.2); initiate-intent control (KHÔNG order payload input) thật sự drive `state.execution`; Risk APPROVED/REJECTED (STATE-013)/NON_EVALUABLE (STATE-014) branch truncation chính xác; downstream chain nay bao gồm `ExecutionResultComputation` VÀ `PaperExecutionObservation` LÀ hai node riêng biệt; thay đổi initiation-context (pin/decision-availability/PAPER Decision scenario/Account validity) nay invalidate execution đã tạo (v1.2, đóng `P2-B04-B-MAJ-02`) — matches `ux-blueprint.md` §7.4 SCR-006 spec + `use-case-workflow.md` UC-011 Main flow. |
| UC-012 | **A — Substantive** (Batch 04, promoted từ C; v1.1 đóng `P2-B04-A-MAJ-01`) | SCR-007 ExecutionResult tab fully authored: STATE-015 EXECUTED / STATE-016 NOT_EXECUTED (zero Fill explicit), gắn đúng Order/OrderSubmissionRequest identity, environment=PAPER, VÀ nay expose `ExecutionResultComputation`/`PaperExecutionObservation` identity LÀM supporting evidence (KHÔNG computation-debugging surface) — matches `ux-blueprint.md` §7.4 SCR-007 spec (a) + `use-case-workflow.md` UC-012. |
| UC-013 | **A — Substantive** (Batch 04, promoted từ C; v1.1 đóng `P2-B04-A-MAJ-01`) | SCR-007 Fill tab fully authored: fill_quantity/fill_price/price_currency + bốn trục simulation evidence (policy/configuration/build/deterministic-input ref), nay đọc TRỰC TIẾP từ `paperExecutionObservation` (owner thật sự theo `execution-result.md` §1, v1.0 sai đặt trên chính `fill` object), khớp CÙNG PaperExecutionObservation identity với ExecutionResult tab (`execution_observation_id` equality, `fill.md` v0.2); STATE-017 Fill absent khi NOT_EXECUTED — matches `ux-blueprint.md` §7.4 SCR-007 spec (b) + `use-case-workflow.md` UC-013. |
| UC-014 | **A — Substantive** (Batch 04, promoted từ C; v1.1 đóng `P2-B04-A-MAJ-02`; v1.2 đóng `P2-B04-B-MAJ-01`) | SCR-007 Position tab fully authored: STATE-018 FLAT/STATE-019 LONG/STATE-020 SHORT (net_quantity/average_entry_price khi applicable) + STATE-021 NON_EVALUABLE (`contributing_fill_refs` đầy đủ, KHÔNG chọn một Fill/aggregate/report FLAT sai). **Cả bốn trạng thái nay materially reachable** — v1.1 STATE-020 CHỈ tồn tại dưới dạng dead code (Decision fixture cố định LONG); v1.2 sửa: `derivePositionNatural()` đọc `execution.fill.direction` (field thật của `fill.md` schema, bound tại `buildExecutionChain()` từ Decision đã chọn) — chọn SHORT Decision scenario qua QA rồi initiate → Fill direction=SHORT → Position SHORT hiển thị thật sự — matches `ux-blueprint.md` §7.4 SCR-007 spec (c) + `use-case-workflow.md` UC-014 + `position.md` §1/§2. |
| UC-015 | **A — Substantive** (Batch 04, promoted từ B) | SCR-007 No-real-exchange tab fully authored: environment=PAPER confirmation, "no real exchange order placed," "no real network route trong prototype này" — KHÔNG tuyên bố một network audit kỹ thuật đã chạy — matches `ux-blueprint.md` §7.4 SCR-007 spec (d) + `use-case-workflow.md` UC-015. |
| UC-001..UC-010 | **A — Substantive** (Batch 01/02/03, giữ nguyên) | Fully authored + independently verified tại Batch 01/02/03 (mỗi batch tự nó qua đầy đủ Review A + Independent Review B, verdict `READY_FOR_NEXT_PHASE2_BATCH`). Batch 04 CHỈ link tới Research/Replay/Backtest (real nav link) — KHÔNG re-author, NHƯNG cumulative classification VẪN A (một UC KHÔNG thể vừa A vừa B/C). |

## 2. Cumulative Phase-2 UC ledger (Batch 01 + Batch 02 + Batch 03 + Batch 04 — ĐÃ independently verified, v1.3 bookkeeping reconciliation, final Independent Review B trên Batch 04 v1.2 verdict READY_FOR_NEXT_PHASE2_BATCH)

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

21-UC substantive completion progress: 15/21 (A only) — ĐÃ independently verified (v1.3
  bookkeeping reconciliation, 2026-08-14 — final bounded Review A v1.2 CLEAN (bốn finding
  CLOSED) + final Independent Review B v1.2 verdict READY_FOR_NEXT_PHASE2_BATCH, 0/0/0). Lifecycle
  VẪN CANDIDATE (verdict review ≠ lifecycle promotion).
  Historical (TRƯỚC Batch 04's own review hoàn tất): last independently verified 10/21
  (UC-001..010, Batch 01+02+03 baseline).
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
| `app.js` `currentPaperDecision()` / `.evidence-group-upstream` block in `renderScr006()` (v1.2, đóng `P2-B04-B-MAJ-01` — đọc `MOCK_PAPER_DECISIONS[state.paperDecisionScenario]`, KHÔNG một global cố định) | SCR-006 "Information displayed" — upstream Decision evidence shown BEFORE initiation | UC-011 | PR-004, PR-005 | `ux-blueprint.md` §7.4 SCR-006 "Information displayed"/"Required context"; `use-case-workflow.md` UC-011 Main flow bước 2 (upstream evidence, tách biệt downstream causation) |
| `index.html` `[data-qa="decision-long"]`/`[data-qa="decision-short"]` / `app.js` `state.paperDecisionScenario` (v1.2, MỚI, đóng `P2-B04-B-MAJ-01` — hai illustrative PAPER-context Decision fixture riêng biệt, `MOCK_PAPER_DECISIONS.LONG`/`.SHORT`, KHÔNG một Decision mutate thành cái kia) | SCR-006 "Information displayed"/"Required context" — WHICH eligible PAPER-context Decision lineage is current | UC-011 | PR-004, PR-005 | `ux-blueprint.md` §7.4 SCR-006 "Information displayed"; `use-case-workflow.md` UC-011 "Decision này TUYỆT ĐỐI KHÔNG phải Decision phát sinh từ Backtest/Research được carry-forward/promote/reuse" (mỗi fixture riêng, KHÔNG derive lẫn nhau) |
| `index.html` `#btn-initiate` / `app.js` `buildExecutionChain()` call | SCR-006 "Available user actions" — initiate-intent (KHÔNG order payload) | UC-011 | PR-007, PR-024 | `ux-blueprint.md` §7.4 SCR-006 "Available user actions"/"Out-of-scope boundary" (KHÔNG order type/sizing/fee/slippage UI) |
| `app.js` `buildExecutionChain()` `riskOutcome === "APPROVED"` branch (continues downstream) | RiskEvaluation APPROVED — chain continues | UC-011 | PR-006, PR-014 | `ux-blueprint.md` §7.4 SCR-006 "Primary states"; `use-case-workflow.md` UC-011 Main flow bước 4-5 |
| `app.js` `buildExecutionChain()` `riskOutcome === "REJECTED"` branch / `renderInitiationResult()` STATE-013 | STATE-013 Risk REJECTED | UC-011 (alternate/failure) | PR-006, PR-014 | `ux-blueprint.md` §11 STATE-013 row; `use-case-workflow.md` UC-011 "Alternate/failure" |
| `app.js` `buildExecutionChain()` `riskOutcome === "NON_EVALUABLE"` branch / `renderInitiationResult()` STATE-014 | STATE-014 Risk NON_EVALUABLE | UC-011 (alternate/failure) | PR-006, PR-014 | `ux-blueprint.md` §11 STATE-014 row; `use-case-workflow.md` UC-011 "Alternate/failure" |
| `app.js` `buildExecutionChain()` full (Trade Intent → RiskEvaluation → Execution Intent → Order → OrderSubmissionRequest → ExecutionResultComputation → PaperExecutionObservation → ExecutionResult → Fill) | SCR-006 "System-owned actions"/"Evidence produced" — downstream causal chain, system-owned throughout | UC-011 | PR-007, PR-024 | `ux-blueprint.md` §7.4 SCR-006 "System-owned actions"; `use-case-workflow.md` UC-011 Main flow bước 3-9 |
| `app.js` `buildExecutionChain()` `chain.executionResultComputation` (v1.1, đóng `P2-B04-A-MAJ-01` — id/computationPurpose=INITIAL/orderId/submissionRequestId/computationCursor, chỉ tồn tại khi APPROVED) | ExecutionResultComputation — authorized computation identity, bound to Order/OrderSubmissionRequest | UC-011 | PR-007, PR-024 | `execution-result.md` §2 "ExecutionResultComputation" schema (`execution_result_computation_id`/`computation_purpose`/`order_id`/`submission_request_id`/`computation_cursor`) |
| `app.js` `buildExecutionChain()` `chain.paperExecutionObservation` (v1.1, đóng `P2-B04-A-MAJ-01` — id/executionResultComputationId/orderId/submissionRequestId/observationCursor/bốn trục simulation evidence/resultType/economics khi EXECUTED) | PaperExecutionObservation — bound to ExecutionResultComputation, carries simulation evidence + economics that ExecutionResult/Fill copy from | UC-011 | PR-007, PR-024 | `execution-result.md` §1 "PaperExecutionObservation" schema |
| `index.html` `.mode-label`/`.authority-label-authoritative` ("Paper"/"authoritative PAPER") + `#ctx-live` static "Unauthorized" badge | SCR-006/SCR-007 "Authority labels"; STATE-027 Live unauthorized (global, reused convention) | UC-011, UC-015 | PR-001, PR-016, PR-027 | `ux-blueprint.md` §7.4 SCR-006/SCR-007 "Authority labels"; §11 STATE-027 row |
| Absence of any "Execute this Backtest Decision in Paper"/"Promote Backtest Decision"/"Convert Backtest result to PAPER Decision" action, and absence of quantity/order-type/sizing/fee/slippage input anywhere in Batch 04 | SCR-006 "Available user actions"/"Out-of-scope boundary" (explicit prohibition) | UC-011 | PR-001, PR-004, PR-005, PR-006, PR-007, PR-016, PR-024 | `ux-blueprint.md` §7.4 SCR-006 "Out-of-scope boundary"; `use-case-workflow.md` UC-011 "Out-of-scope boundary" |
| `app.js` `renderScr007()` STATE-002 branch (no `state.execution.order`) | STATE-002 empty | UC-012, UC-013, UC-014 | PR-021, PR-034 | `ux-blueprint.md` §11 STATE-002 row (SCR-007 "chưa Order/Fill nào tồn tại") |
| `app.js` `renderExecutionResultTab()` STATE-015 branch, incl. Execution Result Computation/PaperExecutionObservation identity rows (v1.1, đóng `P2-B04-A-MAJ-01` — supporting evidence, KHÔNG computation-debugging surface) | STATE-015 ExecutionResult EXECUTED | UC-012 | PR-007, PR-014, PR-024 | `ux-blueprint.md` §11 STATE-015 row; `use-case-workflow.md` UC-012 Main flow |
| `app.js` `renderExecutionResultTab()` STATE-016 branch (zero Fill explicit), incl. Execution Result Computation/PaperExecutionObservation identity rows (v1.1, đóng `P2-B04-A-MAJ-01`) | STATE-016 ExecutionResult NOT_EXECUTED | UC-012 (alternate/failure) | PR-007, PR-014, PR-024 | `ux-blueprint.md` §11 STATE-016 row; `use-case-workflow.md` UC-012 "Alternate/failure" — "người dùng thấy rõ zero Fill kèm theo" |
| `app.js` `buildExecutionChain()` `chain.fill.direction = decision.outcome` (v1.2, MỚI, đóng `P2-B04-B-MAJ-01` — field CÓ THẬT trong `fill.md` schema, v1.0/v1.1 bỏ sót) | Fill's own `direction` field, bound to the exact Decision that produced this chain | UC-013 | PR-025 | `fill.md` §1 schema (`direction: {type: enum, values: [LONG, SHORT], required: true}`) |
| `app.js` `renderFillTab()` economics rows (`f.quantity`/`f.price`/`f.priceCurrency`, LUÔN copy TRỰC TIẾP từ `paperExecutionObservation` tại `buildExecutionChain()`) | SCR-007 Panel (b) — Fill economics | UC-013 | PR-025 | `ux-blueprint.md` §7.4 SCR-007 "Information displayed" (b); `fill.md` §1 (`fill_quantity`/`fill_price`/`price_currency`, copied exactly from Observation) |
| `app.js` `renderFillTab()` `.simulation-table` (v1.1, đóng `P2-B04-A-MAJ-01` — đọc TRỰC TIẾP `obs.simulationPolicyRef`/`obs.simulationConfigurationRef`/`obs.simulationBuildRef`/`obs.deterministicInputRef` từ `ex.paperExecutionObservation`, KHÔNG còn field riêng trên `fill`) | SCR-007 Panel (b) — Fill simulation evidence, matching same PaperExecutionObservation identity hiển thị tại ExecutionResult tab | UC-013 | PR-025 | `execution-result.md` §1 PaperExecutionObservation (`simulation_policy_ref`/`simulation_configuration_ref`/`simulation_build_ref`/`deterministic_input_ref`); `use-case-workflow.md` UC-013 Main flow — "khớp byte-for-byte PaperExecutionObservation gốc" |
| `app.js` `renderFillTab()` STATE-017 branch | STATE-017 Fill absent | UC-013 (alternate/failure) | PR-025 | `ux-blueprint.md` §11 STATE-017 row; `use-case-workflow.md` UC-013 "Alternate/failure" |
| `app.js` `renderPositionTab()` STATE-018 branch (FLAT), incl. `demoNote` khi NON_EVALUABLE override KHÔNG áp dụng (v1.1, đóng `P2-B04-A-MAJ-02`) | STATE-018 Position FLAT | UC-014 | PR-026 | `ux-blueprint.md` §11 STATE-018 row; `position.md` §2 fold algorithm bước 3 (zero eligible Fill) |
| `app.js` `derivePositionNatural()` `direction: execution.fill.direction` / `renderPositionTab()` STATE-019/STATE-020 branches (LONG/SHORT), incl. `demoNote` khi NON_EVALUABLE override KHÔNG áp dụng (v1.1, đóng `P2-B04-A-MAJ-02`; v1.2, đóng `P2-B04-B-MAJ-01` — STATE-020 nay materially reachable qua SHORT Decision scenario, KHÔNG còn dead code) | STATE-019/STATE-020 Position LONG/SHORT | UC-014 | PR-026 | `ux-blueprint.md` §11 STATE-019/020 rows; `position.md` §2 fold algorithm bước 4 (`net_quantity`/`average_entry_price` = Fill's, `position_direction` = Fill's `direction`) |
| `app.js` `derivePosition()` `positionDemoOverride === "non-evaluable"` / `renderPositionTab()` STATE-021 branch (v1.1, đóng `P2-B04-A-MAJ-02` — CHỈ render khi `execution.fill` tồn tại thật, ghép Fill THẬT của execution hiện tại với `MOCK_PRIOR_FILL_LABEL` illustrative prior Fill tường minh disclosed; v1.0 fabricate `FILL-002` KHÔNG evidence basis VÀ có thể mâu thuẫn với NOT_EXECUTED, nay đóng) | STATE-021 Position NON_EVALUABLE | UC-014 (alternate/failure) | PR-026 | `ux-blueprint.md` §11 STATE-021 row; `position.md` §1/§2 (`projection_status = NON_EVALUABLE`, `contributing_fill_refs` bắt buộc, KHÔNG chọn một Fill/aggregate/report FLAT) |
| `app.js` `derivePosition()` fallback khi NON_EVALUABLE override được chọn NHƯNG `execution.fill` KHÔNG tồn tại (v1.1, MỚI, đóng `P2-B04-A-MAJ-02` — trả về trạng thái Position THẬT kèm `demoNote` giải thích, KHÔNG silently drop override, KHÔNG collapse cưỡng bức về FLAT) | Override-inapplicable disclosure — KHÔNG một STATE-XXX riêng, chỉ ghi chú minh bạch trên STATE-018/019/020 đang render thật | UC-014 | PR-026 | `position.md` §1/§2 (Position LUÔN resolve TRỰC TIẾP qua fold algorithm tại đúng eligible-Fill-count hiện tại — override KHÔNG được phép tạo evidence giả) |
| `app.js` `renderSafetyTab()` (always available regardless of chain state) | SCR-007 Panel (d) — no-real-exchange confirmation | UC-015 | PR-027 | `ux-blueprint.md` §7.4 SCR-007 "Information displayed" (d); `use-case-workflow.md` UC-015 Main flow — environment field trên Order/ExecutionResult |
| `index.html` "Continue to Review" button → `#screen-deferred` | SCR-007 "Exit points" (SCR-008, deferred handoff only — SCR-008 KHÔNG authored substantively); NAV-005 nav-button-existence only | UC-012, UC-013, UC-014, UC-015 | PR-007, PR-025, PR-026, PR-027 | `ux-blueprint.md` §7.4 SCR-007 "Exit points"; §5a NAV-005 |
| `app.js` `CONTEXT_MUTATION_KEYS` / `wireQaPanel()` invalidation (`state.execution = null`) (v1.2, MỚI, đóng `P2-B04-B-MAJ-02`) | SCR-007 "Required context" — "Order đã đi qua SCR-006, có ExecutionResult visible-valid" chỉ còn đúng cho execution được tạo DƯỚI initiation context hiện tại; đổi Account/Instrument/Venue validity, Paper Strategy Instance pin, PAPER Decision availability, hoặc PAPER Decision scenario invalidate execution cũ | UC-011, UC-012, UC-013, UC-014 | PR-001, PR-016, PR-024 | `ux-blueprint.md` §7.4 SCR-007 "Required context"; §5a NAV-004 "Required context" (ba điều kiện theo thứ tự — thay đổi bất kỳ điều kiện nào nghĩa là context initiation đã khác) — prototype-local demo-state hygiene only, KHÔNG production session/context invalidation semantics |
| `app.js` `renderScr007()` `el5("Strategy Instance (pinned, continuous from SCR-006)", ...)` + `el5("Decision lineage", execution.decisionId + " (" + execution.decisionOutcome + ")")` (v1.2, đóng `P2-B04-B-MAJ-02` — Decision lineage row nay đọc snapshot `execution.decisionId`/`execution.decisionOutcome` bound tại thời điểm `buildExecutionChain()` chạy, KHÔNG global hiện tại; kết hợp với `CONTEXT_MUTATION_KEYS` invalidation, "continuous from SCR-006" LUÔN đúng — execution hiển thị LUÔN được tạo dưới context hiện tại, KHÔNG BAO GIỜ stale) | SCR-007 "Information displayed" — "giữ nguyên liên tục từ SCR-006 — KHÔNG đổi giữa chừng" (UX-INV-3) | UC-011, UC-012, UC-013, UC-014 | PR-001, PR-016 | `ux-blueprint.md` §7.4 SCR-007 "Information displayed"; §3 UX-INV-3 (Strategy Instance identity continuity) |
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
  Decision's creation mechanism is not defined (deferred). v1.2 (đóng `P2-B04-B-MAJ-01`) adds a
  SECOND distinct fixture (`MOCK_PAPER_DECISIONS.SHORT`) alongside the original LONG one — the
  two are independent objects (own id/outcome/inputSnapshot/evaluationEvidence), never one
  mutated into the other, never derived from each other, and neither is a Backtest/Research
  Decision carried forward.
INV-2 (user supplies intent only): verified — SCR-006's "Available user actions" row; zero
  quantity/order-type/sizing/fee/slippage/execution-model input exists anywhere in
  index.html/app.js (verified directly, grep clean for any such input field).
INV-3 (upstream vs downstream): verified — `.evidence-group-upstream` shown BEFORE initiation,
  visually distinct (border-left style, separate section) from `renderInitiationResult()`'s
  downstream causation, shown only AFTER the initiate button is clicked. RiskEvaluation never
  appears in the upstream evidence group.
INV-4 (exact branch truncation): verified — `buildExecutionChain()`'s REJECTED/NON_EVALUABLE
  branches `return` immediately after setting `riskEvaluation`, before `executionIntent`/`order`/
  `submissionRequest`/`executionResultComputation`/`paperExecutionObservation`/`executionResult`/
  `fill` are ever assigned (all remain `null`) — v1.1 (đóng `P2-B04-A-MAJ-01`) confirms this now
  covers the two newly-distinct Computation/Observation nodes too, not just ExecutionResult/Fill.
  NOT_EXECUTED sets Computation + Observation (result_type NOT_EXECUTED, economics fields left
  unset per execution-result.md §1's conditional-absence invariant) but returns before `fill` is
  assigned. EXECUTED sets Observation's economics fields THEN assigns exactly one `fill` object
  that copies them.
INV-5 (identity continuity + Position semantics): verified — SCR-006 and SCR-007 read the SAME
  `MOCK_STRATEGY_CONTEXT`/`MOCK_ACCOUNT_CONTEXT`/`state.execution` objects (single shared JS
  module scope, single page) — no teleportation between screens. `derivePosition()` never labels
  Position as an authoritative fact (hint text quotes position.md §1 explicitly); NON_EVALUABLE is
  never guessed/collapsed/aggregated (v1.1, đóng `P2-B04-A-MAJ-02`: dedicated branch,
  `contributing_fill_refs` always present when NON_EVALUABLE, AND now only reachable when the
  current execution's Fill genuinely exists — pairing it with one explicitly-labelled illustrative
  prior Fill rather than fabricating a second current Fill; when it doesn't apply, the actual
  Position state is returned with a disclosed `demoNote`, never silently forced to FLAT). v1.2
  (đóng `P2-B04-B-MAJ-02`) hardens identity continuity further: `CONTEXT_MUTATION_KEYS` invalidate
  `state.execution` whenever Account/Instrument/Venue validity, Paper Strategy Instance pin, PAPER
  Decision availability, or PAPER Decision scenario changes — so SCR-007's "continuous from
  SCR-006" claim is now structurally guaranteed true (the displayed execution can only ever have
  been created under the CURRENT initiation context), never a stale claim against a since-changed
  context. Position direction is now read from `execution.fill.direction` (fill.md's own schema
  field, bound to whichever Decision produced the chain) rather than a mutable global, closing
  `P2-B04-B-MAJ-01`'s STATE-020 unreachability alongside this same identity-binding fix.
```
