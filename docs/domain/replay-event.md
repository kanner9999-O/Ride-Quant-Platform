---
id: replay-event
title: Replay Integration
version: "0.2"
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

> **Vai trò của tài liệu này:** Domain Contract thứ tư và cuối cùng của Package 0.2-C7 (Execution Result, Fill, Position and Replay Integration Foundation) — định nghĩa **ReplayStateProjection**, một INTEGRATION CONTRACT mô tả cách các authoritative fact ĐÃ TỒN TẠI (Decision, Trade Intent, RiskEvaluation, Execution Intent, Order, OrderSubmissionRequest, PaperExecutionObservation, ExecutionResult, Fill) được select và fold TẠI một canonical Replay Cursor để tái tạo end-to-end state. Draft, chưa Approved/Locked. Thuộc capability `execution-management` / context `replay-integration` (đăng ký tại [`context-map.yaml`](./context-map.yaml), không đổi trong bounded correction này). Kiến trúc controlling: [Chapter 8 §8.5](../constitution/08-event-model.md) (Locked, canonical Replay Cursor), toàn bộ Domain Contract authoritative đã author cộng derived `position.md`. Tài liệu này CHỈ tham chiếu (`ref:`) các stream đã tồn tại, KHÔNG author fact mới, KHÔNG duplicate authority.

Replay Integration **KHÔNG phải** một authoritative event stream thứ hai, **KHÔNG phải** một "ReplayDecision"/"ReplayOrder"/"ReplayFill" event nào cả, **KHÔNG phải** một cơ chế mutate lại lịch sử. Nó là **một hàm thuần túy, deterministic** — tại một cursor C cho trước, select + fold TOÀN BỘ visible-valid lineage từ MỌI Domain Contract đã author (bao gồm `PaperExecutionObservation` lineage, v0.2, MỚI), VÀ derive Fill continuing eligibility (`fill.md` §6) VÀ Position projection status (`position.md` §2) — trả lời chính xác một câu hỏi: "Tại cursor C, end-to-end state của TOÀN BỘ chuỗi Decision→Trade Intent→Risk→Execution Intent→Order→Submission Request→Observation→Execution Result→Fill (continuing eligibility)→Position (projection status) là gì?"

**Ví dụ walking-skeleton (tổng hợp toàn Package 0.2-C7):** replay tái tạo state tại MƯỜI mốc cursor — trước Observation, sau Observation, sau Attempt, sau Result, sau Fill, sau Result invalidation TRƯỚC Fill invalidation, sau Fill invalidation, sau Result replacement, sau Fill replacement, VÀ trạng thái nhiều Fill lineage eligible đồng thời. Xem §4 cho danh sách cursor mốc đầy đủ.

**v0.2 — bounded correction (đóng liên đới `C7-MAJ-01`/`C7-MAJ-03`/`C7-MAJ-04`, KHÔNG finding riêng cho `replay-event.md` — cập nhật theo thay đổi tại `execution-result.md`/`fill.md`/`position.md`):** thêm `paper_execution_observation_lineage` vào `ReplayState(C)` (§2, MỚI, phản ánh C7-MAJ-01); thêm `fill_continuing_eligibility` field, phản ánh `eligible_as_position_contributing_fill` (fill.md §6, MỚI, phản ánh C7-MAJ-03 — KHÔNG cross-stream atomicity); `derived_position` nay phản ánh `projection_status`/`projection_reason_code`/`contributing_fill_refs` (position.md §1/§2, phản ánh C7-MAJ-04). Mười cursor mốc thay thế tám mốc cũ (§4) — bao gồm mốc "Result invalidation TRƯỚC Fill invalidation" (chứng minh Fill orphan bị loại khỏi Position mà KHÔNG cần cleanup đồng thời) VÀ mốc "nhiều eligible Fill lineage" (chứng minh `NON_EVALUABLE` deterministic).

**Phạm vi bounded tường minh:** KHÔNG author bất kỳ authoritative event/entity mới nào. KHÔNG duplicate authority trong một stream thứ hai. KHÔNG tạo cursor schema gần giống. KHÔNG author accounting/settlement/tax semantics. KHÔNG sửa `fill.md`/`execution-result.md`/`order.md`/`execution-intent.md`/`risk.md`/`decision.md`/`trade-intent.md`/C1–C6/ADR/Constitution.

## 1. `ReplayStateProjection` — `kind: read_model` (integration contract, KHÔNG authoritative)

```yaml
id: replay-state-projection
kind: read_model
capability_id: execution-management
domain_context_id: replay-integration
description: >
  INTEGRATION CONTRACT thuần túy — định nghĩa cách select + fold các authoritative fact ĐÃ TỒN TẠI
  (KHÔNG author fact mới) tại một canonical Replay Cursor C để tái tạo ReplayState(C), bao gồm
  PaperExecutionObservation lineage, Fill continuing eligibility, VÀ derived Position projection
  status. KHÔNG authoritative, KHÔNG event stream riêng, KHÔNG mutable command.
invariants:
  - "ReplayStateProjection KHÔNG BAO GIỜ là nguồn authoritative cho bất kỳ computation nào — mọi field trong ReplayState(C) PHẢI resolve trực tiếp từ authoritative event stream tương ứng (§2) TẠI cursor C, KHÔNG một bản sao/cache riêng."
  - "KHÔNG event mới nào được emit bởi tài liệu này — 'ReplayDecision'/'ReplayOrder'/'ReplayFill' hay bất kỳ event trùng lặp nào TUYỆT ĐỐI KHÔNG author."
  - "Mọi lineage thành phần (§2) PHẢI dùng ĐÚNG fold algorithm đã pin tại Domain Contract sở hữu nó — replay-event.md KHÔNG tự định nghĩa lại visible-valid-head logic cho bất kỳ stream nào."
  - "Cursor C TÁI SỬ DỤNG nguyên vẹn canonical Replay Cursor shape (Chapter 8 §8.5.1) — MỘT cursor DUY NHẤT áp dụng đồng thời cho TẤT CẢ lineage thành phần trong ReplayState(C)."
  - "**v0.2:** `fill_continuing_eligibility` PHẢI dùng CHÍNH XÁC `eligible_as_position_contributing_fill` (fill.md §6) — KHÔNG một biến thể fold riêng nào. `derived_position` PHẢI dùng CHÍNH XÁC `position.md` §2 fold (bao gồm `projection_status`/`projection_reason_code`/`contributing_fill_refs` khi NON_EVALUABLE)."
schema:
  replay_cursor: {type: object, required: true, description: "canonical Replay Cursor — Chapter 8 §8.5.1, TÁI SỬ DỤNG nguyên vẹn, xem §2"}
  decision_lineage: {type: object, required: false, description: "= decision.md §5 fold algorithm TẠI replay_cursor — ref: decision"}
  trade_intent_lineage: {type: object, required: false, description: "= trade-intent.md fold algorithm TẠI replay_cursor — ref: trade-intent"}
  risk_evaluation_lineage: {type: object, required: false, description: "= risk.md §7 fold algorithm TẠI replay_cursor — ref: risk"}
  execution_intent: {type: object, required: false, description: "= execution-intent.md §6 fold algorithm TẠI replay_cursor — ref: execution-intent"}
  order_lineage: {type: object, required: false, description: "= order.md §8 Tầng 1/2 fold algorithm TẠI replay_cursor — ref: order"}
  submission_request: {type: object, required: false, description: "= order.md §6/§8 Tầng 2 fold TẠI replay_cursor — ref: order"}
  paper_execution_observation_lineage: {type: object, required: false, description: "v0.2, MỚI (đóng liên đới C7-MAJ-01) — = execution-result.md §1 (append-only, immutable) TẠI replay_cursor — ref: execution-result (paper-execution-observation)"}
  execution_result_lineage: {type: object, required: false, description: "= execution-result.md §8 fold algorithm TẠI replay_cursor — ref: execution-result"}
  fill_lineage: {type: object, required: false, description: "= fill.md §5 fold algorithm (stream riêng, view_state) TẠI replay_cursor — ref: fill"}
  fill_continuing_eligibility: {type: object, required: false, description: "v0.2, MỚI (đóng liên đới C7-MAJ-03) — = fill.md §6 eligible_as_position_contributing_fill(fill_id, replay_cursor) cho MỌI Fill liên quan — TÁCH BIỆT khỏi fill_lineage's view_state (một Fill CÓ THỂ VALID trong stream riêng nhưng derived-ineligible)"}
  derived_position: {type: object, required: false, description: "= position.md §2 fold algorithm TẠI replay_cursor — derived, KHÔNG authoritative — bao gồm projection_status/projection_reason_code/contributing_fill_refs khi NON_EVALUABLE (v0.2, đóng liên đới C7-MAJ-04) — ref: position"}
queries: [GetReplayState]
```

## 2. `ReplayState(C)` — công thức fold đầy đủ (v0.2)

```text
ReplayState(C) =
  visible valid Decision lineage                        (decision.md §5, TẠI C)
  visible valid Trade Intent lineage                     (trade-intent.md fold, TẠI C)
  visible valid Risk Evaluation lineage                  (risk.md §7, TẠI C)
  visible valid Execution Intent                         (execution-intent.md §6, TẠI C)
  visible valid Order lineage                            (order.md §8 Tầng 1, TẠI C)
  visible valid Submission Request                       (order.md §6/§8 Tầng 2, TẠI C)
  visible PaperExecutionObservation lineage               (execution-result.md §1, append-only, TẠI C — v0.2, MỚI)
  visible valid Execution Result lineage                  (execution-result.md §8, TẠI C)
  Fill lineage (stream riêng)                             (fill.md §5, TẠI C)
  Fill continuing eligibility, cho mọi Fill liên quan      (fill.md §6 eligible_as_position_contributing_fill, TẠI C — v0.2, MỚI)
  derived Position projection (status + economics/reason)  (position.md §2, TẠI C — fold từ Fill continuing eligibility trên, v0.2)
```

**MỘT quy tắc duy nhất:** mỗi thành phần trong công thức trên PHẢI resolve qua ĐÚNG fold algorithm đã pin tại Domain Contract sở hữu nó, tại CHÍNH XÁC cùng một cursor `C` — `replay-event.md` KHÔNG tự tính lại. **v0.2 lưu ý quan trọng:** `Fill lineage` (stream riêng) VÀ `Fill continuing eligibility` là HAI khái niệm TÁCH BIỆT (đúng `fill.md` §5/§6 — Position projection CHỈ dùng `Fill continuing eligibility`, KHÔNG BAO GIỜ `Fill lineage`'s `view_state` trực tiếp).

**No-look-ahead xuyên suốt toàn bộ ReplayState(C):** mọi thành phần fact PHẢI thỏa `fact.recorded_time ≤ C.recorded_time`.

## 3. Không duplicate authority

**Ràng buộc bắt buộc, không ngoại lệ:** `replay-event.md` KHÔNG BAO GIỜ:
- author một event/entity mới nào đại diện lại cho Decision/Trade Intent/RiskEvaluation/Execution Intent/Order/OrderSubmissionRequest/PaperExecutionObservation/ExecutionResult/Fill;
- tạo một "replay stream" riêng biệt song song với stream authoritative gốc;
- cho phép ReplayStateProjection (§1) trở thành input cho bất kỳ computation nào khác NGOÀI query/UI/replay-demonstration.

**Kiểm chứng (Scenario 24, §9):** replay integration CHỈ reference và fold authoritative fact ĐÃ TỒN TẠI — KHÔNG tạo authority nào trùng lặp. `replay-event.md` không author bất kỳ `event_types:` block nào trong toàn tài liệu.

## 4. Cursor mốc bắt buộc — walking skeleton end-to-end (v0.2, mười mốc)

```text
C0 — trước Observation             (Order SUBMISSION_REQUESTED, chưa có PaperExecutionObservation)
C1 — sau Observation                (paper_execution_observation_lineage có mặt, evidence + output đã xác định)
C2 — sau Attempt                    (ExecutionResultProcessingAttemptRecorded PROCESSED có mặt, trỏ Observation)
C3 — sau Result                     (execution_result_lineage có mặt, result_type copy từ Observation)
C4 — sau Fill                       (fill_lineage có mặt — CHỈ nếu result_type=EXECUTED; fill_continuing_eligibility=true; derived_position EVALUABLE LONG/SHORT)
C5 — sau Result invalidation, TRƯỚC Fill invalidation   (v0.2, MỚI — execution_result_lineage → predecessor excluded; fill_lineage KHÔNG đổi, Fill VẪN VALID trong stream riêng; fill_continuing_eligibility → false NGAY LẬP TỨC; derived_position EXCLUDES Fill này, KHÔNG chờ FillFactInvalidated)
C6 — sau Fill invalidation          (fill_lineage EXCLUDES Fill đã invalidate; fill_continuing_eligibility vẫn false; derived_position không đổi so với C5)
C7 — sau Result replacement         (execution_result_lineage → replacement head, paper_execution_observation_lineage có thể có Observation MỚI nếu result_type đổi)
C8 — sau Fill replacement           (fill_lineage → replacement Fill, CHỈ khi Result vẫn EXECUTED; fill_continuing_eligibility → true cho Fill mới; derived_position EVALUABLE theo Fill mới)
C9 — nhiều eligible Fill lineage    (v0.2, MỚI — hai Fill continuing-eligible cùng Position key; derived_position → NON_EVALUABLE, projection_reason_code=UNSUPPORTED_MULTIPLE_FILL_LINEAGES, contributing_fill_refs liệt kê đầy đủ)
```

Tại mỗi cursor `Ci`, `ReplayState(Ci)` PHẢI resolve chính xác theo §2 — KHÔNG shortcut, KHÔNG dùng bất kỳ Current View latest-state nào làm nguồn. **Mốc C5 là minh chứng trực tiếp cho `C7-MAJ-03`** (Position correctness KHÔNG phụ thuộc thời điểm `FillFactInvalidated` được append) VÀ **mốc C9 là minh chứng trực tiếp cho `C7-MAJ-04`** (deterministic `NON_EVALUABLE`, KHÔNG silently sai).

## 5. Downstream reference contract

`replay-event.md` **KHÔNG có downstream package nào tiêu thụ nó ở Phase 0.2** — ReplayStateProjection là điểm TIÊU THỤ CUỐI. Không cần khai báo downstream reference contract.

## 6. Prohibitions

**Replay Integration KHÔNG được sở hữu:** bất kỳ authoritative event/entity semantics nào; Position semantics ngoài việc reference `position.md` §2; mutable replay command; general workflow/saga engine; UI copy/natural-language generation infrastructure; database transaction/outbox/message-broker technology; execution/re-derivation mới từ replay state.

## 7. Ngoài phạm vi — defer

- Cơ chế/implementation technology cụ thể cho replay execution.
- Retention/resolvability horizon cụ thể cho cursor lịch sử xa.
- UI/audit tooling cụ thể tiêu thụ ReplayStateProjection.
- Không đóng OQ-002/OQ-003.

## 8. Open questions ngoài phạm vi

- Cơ chế cụ thể chọn/generate `replay_cursor` cho một audit request — chưa quyết, Phase 1.
- Không đóng OQ-002/OQ-003.

## 9. Acceptance scenarios (v0.2 — phần liên quan trực tiếp Replay Integration)

**Scenario 24 — No duplicate replay authority:** Replay integration CHỈ reference và fold authoritative fact ĐÃ TỒN TẠI (§2/§3) — KHÔNG tạo authority trùng lặp nào.

**Scenario 30 — Replay correction gap (v0.2, MỚI, đóng `C7-MAJ-03`):** cursor SAU Result invalidation, TRƯỚC Fill invalidation (mốc C5, §4) → orphan Fill EXCLUDED khỏi Position qua `fill_continuing_eligibility=false` — KHÔNG cần `FillFactInvalidated` đã append.

**Scenario 31 — Replay multiple Fill state (v0.2, MỚI, đóng `C7-MAJ-04`):** hai eligible Fill lineage cho CÙNG Position key (mốc C9, §4) → `derived_position` deterministic `NON_EVALUABLE`, `projection_reason_code=UNSUPPORTED_MULTIPLE_FILL_LINEAGES`.

**Cursor mốc §4 (C0–C9)** — mỗi mốc là một acceptance check riêng, đối xứng trực tiếp scenario tương ứng tại `execution-result.md`/`fill.md`/`position.md` §17/§14/§9 — `replay-event.md` KHÔNG lặp lại nội dung, CHỈ xác nhận `ReplayState(Ci)` fold đúng công thức §2 tại từng mốc.
