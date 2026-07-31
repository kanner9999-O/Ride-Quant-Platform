---
id: replay-event
title: Replay Integration
version: "0.1"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-07-31"
last_review: null
next_review: null
---

# Replay Integration

> **Vai trò của tài liệu này:** Domain Contract thứ tư và cuối cùng của Package 0.2-C7 (Execution Result, Fill, Position and Replay Integration Foundation) — định nghĩa **ReplayStateProjection**, một INTEGRATION CONTRACT mô tả cách các authoritative fact ĐÃ TỒN TẠI (Decision, Trade Intent, RiskEvaluation, Execution Intent, Order, OrderSubmissionRequest, ExecutionResult, Fill) được select và fold TẠI một canonical Replay Cursor để tái tạo end-to-end state. Draft, chưa Approved/Locked. Thuộc capability `execution-management` / context `replay-integration` (đăng ký MỚI tại [`context-map.yaml`](./context-map.yaml)). Kiến trúc controlling: [Chapter 8 §8.5](../constitution/08-event-model.md) (Locked, canonical Replay Cursor — TÁI SỬ DỤNG nguyên vẹn, KHÔNG tạo schema gần giống), toàn bộ tám Domain Contract authoritative đã author (`decision.md`/`trade-intent.md`/`risk.md`/`execution-intent.md`/`order.md`/`execution-result.md`/`fill.md`) cộng derived `position.md`. Tài liệu này CHỈ tham chiếu (`ref:`) các stream đã tồn tại, KHÔNG author fact mới, KHÔNG duplicate authority.

Replay Integration **KHÔNG phải** một authoritative event stream thứ hai cho Decision/Order/Fill, **KHÔNG phải** một "ReplayDecision"/"ReplayOrder"/"ReplayFill" event nào cả, **KHÔNG phải** một cơ chế mutate lại lịch sử. Nó là **một hàm thuần túy, deterministic** — tại một cursor C cho trước, select + fold TOÀN BỘ visible-valid lineage từ MỌI Domain Contract đã author, VÀ derive Position projection (`position.md` §2) — trả lời chính xác một câu hỏi: "Tại cursor C, end-to-end state của TOÀN BỘ chuỗi Decision→Trade Intent→Risk→Execution Intent→Order→Submission Request→Execution Result→Fill→Position là gì?"

**Ví dụ walking-skeleton (tổng hợp toàn Package 0.2-C7):** replay tái tạo state TRƯỚC Submission Request, SAU Submission Request, SAU Execution Result, SAU Fill, SAU Fill invalidation, SAU replacement Fill, SAU Execution Result invalidation, SAU replacement Execution Result — tám mốc cursor, đúng yêu cầu task. Xem §4 cho danh sách cursor mốc đầy đủ.

**Phạm vi bounded tường minh:** KHÔNG author bất kỳ authoritative event/entity mới nào — mọi fact tham chiếu qua `ref:` tới stream ĐÃ TỒN TẠI. KHÔNG duplicate Decision/Trade Intent/Risk/Execution Intent/Order/Fill authority trong một stream thứ hai. KHÔNG tạo cursor schema gần giống — TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1. KHÔNG author accounting/settlement/tax semantics. KHÔNG sửa `fill.md`/`execution-result.md`/`order.md`/`execution-intent.md`/`risk.md`/`decision.md`/`trade-intent.md`/C1–C6/ADR/Constitution.

## 1. `ReplayStateProjection` — `kind: read_model` (integration contract, KHÔNG authoritative)

```yaml
id: replay-state-projection
kind: read_model
capability_id: execution-management
domain_context_id: replay-integration
description: >
  INTEGRATION CONTRACT thuần túy — định nghĩa cách select + fold các authoritative fact ĐÃ TỒN TẠI
  (KHÔNG author fact mới) tại một canonical Replay Cursor C để tái tạo ReplayState(C), bao gồm derived
  Position projection. KHÔNG authoritative, KHÔNG event stream riêng, KHÔNG mutable command.
invariants:
  - "ReplayStateProjection KHÔNG BAO GIỜ là nguồn authoritative cho bất kỳ computation nào — mọi field trong ReplayState(C) PHẢI resolve trực tiếp từ authoritative event stream tương ứng (§2) TẠI cursor C, KHÔNG một bản sao/cache riêng."
  - "KHÔNG event mới nào được emit bởi tài liệu này — 'ReplayDecision'/'ReplayOrder'/'ReplayFill' hay bất kỳ event trùng lặp nào TUYỆT ĐỐI KHÔNG author (đúng yêu cầu 'must not duplicate Decision, Risk, Order or Fill authority in a second event stream')."
  - "Mọi lineage thành phần (§2) PHẢI dùng ĐÚNG fold algorithm đã pin tại Domain Contract sở hữu nó — replay-event.md KHÔNG tự định nghĩa lại visible-valid-head logic cho bất kỳ stream nào."
  - "Cursor C TÁI SỬ DỤNG nguyên vẹn canonical Replay Cursor shape (Chapter 8 §8.5.1) — MỘT cursor DUY NHẤT áp dụng đồng thời cho TẤT CẢ lineage thành phần trong ReplayState(C), KHÔNG cursor riêng theo từng contract."
schema:
  replay_cursor: {type: object, required: true, description: "canonical Replay Cursor — Chapter 8 §8.5.1, TÁI SỬ DỤNG nguyên vẹn, xem §2"}
  decision_lineage: {type: object, required: false, description: "= decision.md §5 fold algorithm TẠI replay_cursor — ref: decision"}
  trade_intent_lineage: {type: object, required: false, description: "= trade-intent.md fold algorithm TẠI replay_cursor — ref: trade-intent"}
  risk_evaluation_lineage: {type: object, required: false, description: "= risk.md §7 fold algorithm TẠI replay_cursor — ref: risk"}
  execution_intent: {type: object, required: false, description: "= execution-intent.md §6 fold algorithm TẠI replay_cursor — ref: execution-intent"}
  order_lineage: {type: object, required: false, description: "= order.md §8 Tầng 1/2 fold algorithm TẠI replay_cursor — ref: order"}
  submission_request: {type: object, required: false, description: "= order.md §6/§8 Tầng 2 fold TẠI replay_cursor — ref: order"}
  execution_result_lineage: {type: object, required: false, description: "= execution-result.md §6 fold algorithm TẠI replay_cursor — ref: execution-result"}
  fill_lineage: {type: object, required: false, description: "= fill.md §5 fold algorithm TẠI replay_cursor — ref: fill"}
  derived_position: {type: object, required: false, description: "= position.md §2 fold algorithm TẠI replay_cursor — derived, KHÔNG authoritative — ref: position"}
queries: [GetReplayState]
```

## 2. `ReplayState(C)` — công thức fold đầy đủ

```text
ReplayState(C) =
  visible valid Decision lineage                (decision.md §5, TẠI C)
  visible valid Trade Intent lineage             (trade-intent.md fold, TẠI C)
  visible valid Risk Evaluation lineage          (risk.md §7, TẠI C)
  visible valid Execution Intent                 (execution-intent.md §6, TẠI C)
  visible valid Order lineage                    (order.md §8 Tầng 1, TẠI C)
  visible valid Submission Request               (order.md §6/§8 Tầng 2, TẠI C)
  visible valid Execution Result lineage         (execution-result.md §6, TẠI C)
  visible valid Fill lineage                     (fill.md §5, TẠI C)
  derived Position projection                    (position.md §2, TẠI C — fold từ Fill lineage trên)
```

**MỘT quy tắc duy nhất:** mỗi thành phần trong công thức trên PHẢI resolve qua ĐÚNG fold algorithm đã pin tại Domain Contract sở hữu nó (đã dẫn ở trên), tại CHÍNH XÁC cùng một cursor `C` — `replay-event.md` KHÔNG tự tính lại, KHÔNG tạo một biến thể fold algorithm nào khác. `replay_cursor` (schema §1) TÁI SỬ DỤNG nguyên vẹn canonical Replay Cursor (Chapter 8 §8.5.1) — KHÔNG một schema gần giống, KHÔNG cursor riêng theo từng thành phần.

**No-look-ahead xuyên suốt toàn bộ ReplayState(C):** mọi thành phần fact PHẢI thỏa `fact.recorded_time ≤ C.recorded_time` — tái khẳng định (KHÔNG lặp lại toàn văn) no-look-ahead invariant đã pin riêng tại từng Domain Contract sở hữu (decision.md/trade-intent.md/risk.md/execution-intent.md/order.md/execution-result.md/fill.md).

## 3. Không duplicate authority

**Ràng buộc bắt buộc, không ngoại lệ:** `replay-event.md` KHÔNG BAO GIỜ:
- author một event/entity mới nào đại diện lại cho Decision/Trade Intent/RiskEvaluation/Execution Intent/Order/OrderSubmissionRequest/ExecutionResult/Fill;
- tạo một "replay stream" riêng biệt song song với stream authoritative gốc;
- cho phép ReplayStateProjection (§1) trở thành input cho bất kỳ computation nào khác NGOÀI query/UI/replay-demonstration (KHÔNG execution mới, KHÔNG re-derive Order/Fill mới từ ReplayState).

**Kiểm chứng (Scenario 24, §5):** replay integration CHỈ reference và fold authoritative fact ĐÃ TỒN TẠI — KHÔNG tạo authority Decision/Order/Fill trùng lặp nào.

## 4. Cursor mốc bắt buộc — walking skeleton end-to-end

Replay PHẢI chứng minh khả năng tái tạo ReplayState(C) tại ĐỦ tám mốc cursor sau (theo đúng thứ tự thời gian của walking skeleton):

```text
C0 — trước Submission Request     (Order CREATED, chưa có OrderSubmissionRequested)
C1 — sau Submission Request       (Order SUBMISSION_REQUESTED, submission_request có mặt)
C2 — sau Execution Result         (execution_result_lineage có mặt, result_type xác định)
C3 — sau Fill                     (fill_lineage có mặt — CHỈ nếu result_type=EXECUTED; derived_position LONG/SHORT)
C4 — sau Fill invalidation        (fill_lineage EXCLUDES Fill đã invalidate; derived_position → FLAT hoặc PENDING theo fill.md §5)
C5 — sau replacement Fill         (fill_lineage → replacement Fill; derived_position → LONG/SHORT theo replacement)
C6 — sau Execution Result invalidation   (execution_result_lineage → PENDING_CORRECTION hoặc predecessor excluded)
C7 — sau replacement Execution Result    (execution_result_lineage → replacement head, fill_lineage/derived_position recompute theo — bắt buộc coupling execution-result.md §7/fill.md §4)
```

Tại mỗi cursor `Ci`, `ReplayState(Ci)` PHẢI resolve chính xác theo §2 — KHÔNG shortcut, KHÔNG dùng bất kỳ Current View latest-state nào (`OrderCurrentView`/`ExecutionResultCurrentView`/`FillCurrentView`) làm nguồn cho ReplayState.

## 5. Downstream reference contract

`replay-event.md` **KHÔNG có downstream package nào tiêu thụ nó ở Phase 0.2** — ReplayStateProjection là điểm TIÊU THỤ CUỐI (query/UI/audit), KHÔNG phải một upstream contract cho bất kỳ Domain Contract nào khác. Không cần khai báo downstream reference contract.

## 6. Prohibitions

**Replay Integration KHÔNG được sở hữu:** bất kỳ authoritative event/entity semantics nào (Decision/Trade Intent/RiskEvaluation/Execution Intent/Order/OrderSubmissionRequest/ExecutionResult/Fill — tất cả thuộc file riêng); Position semantics ngoài việc reference `position.md` §2; mutable replay command; general workflow/saga engine; UI copy/natural-language generation infrastructure; database transaction/outbox/message-broker technology; execution/re-derivation mới từ replay state.

## 7. Ngoài phạm vi — defer

- Cơ chế/implementation technology cụ thể cho replay execution (batch job, streaming re-fold, materialized cache) — deferred Phase 1, boundary semantic pin only.
- Retention/resolvability horizon cụ thể cho cursor lịch sử xa — chưa pin ở v0.1.
- UI/audit tooling cụ thể tiêu thụ ReplayStateProjection — ngoài phạm vi Domain Contract.
- Không đóng OQ-002/OQ-003.

## 8. Open questions ngoài phạm vi

- Cơ chế cụ thể chọn/generate `replay_cursor` cho một audit request — chưa quyết, Phase 1.
- Không đóng OQ-002/OQ-003.

## 9. Acceptance scenarios (validation, không phải executable test tại C7 — phần liên quan trực tiếp Replay Integration)

**Scenario 24 — No duplicate replay authority:** Replay integration CHỈ reference và fold authoritative fact ĐÃ TỒN TẠI (§2/§3) — KHÔNG tạo authority Decision/Order/Fill trùng lặp nào. Verified: `replay-event.md` không author bất kỳ `event_types:` block nào trong toàn tài liệu.

**Cursor mốc §4 (C0–C7)** — mỗi mốc là một acceptance check riêng, đối xứng trực tiếp scenario tương ứng tại `execution-result.md`/`fill.md`/`position.md` §15/§13/§9 (Scenario 1/8/12/17/21/22/23) — `replay-event.md` KHÔNG lặp lại nội dung, CHỈ xác nhận `ReplayState(Ci)` fold đúng công thức §2 tại từng mốc.
