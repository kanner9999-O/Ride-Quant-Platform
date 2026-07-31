---
id: execution-result
title: Execution Result
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

# Execution Result

> **Vai trò của tài liệu này:** Domain Contract thứ nhất của Package 0.2-C7 (Execution Result, Fill, Position and Replay Integration Foundation) — định nghĩa **ExecutionResult** (bản ghi authoritative, bất biến, của MỘT observation trả về từ bounded PAPER execution boundary cho một Order Submission Request) và **ExecutionResultProcessingAttempt** (bản ghi authoritative của MỘT LẦN THỬ xử lý execution result — kể cả khi không dẫn tới ExecutionResult). Draft, chưa Approved/Locked. Thuộc capability `execution-management` / context `execution-result-management` (đăng ký MỚI tại [`context-map.yaml`](./context-map.yaml)). Kiến trúc controlling: [`order.md`](./order.md) v0.2 Draft §8b (`eligible_for_execution_result_processing`, KHÔNG sửa), [`risk.md`](./risk.md) v0.3 Draft/[`decision.md`](./decision.md) v0.3 Draft (bốn bài học đã trả giá qua C4–C6's các vòng correction — ÁP DỤNG LẠI đúng semantic đã proven), [Chapter 8 §8.1.1/§8.2/§8.5](../constitution/08-event-model.md) (Locked, Referenced Authoritative Artifact + canonical Replay Cursor — TÁI SỬ DỤNG nguyên vẹn). Tài liệu này CHỈ implement field/invariant mà các nguồn trên yêu cầu, KHÔNG tự quyết architecture mới ngoài phạm vi đã khóa.

ExecutionResult **KHÔNG phải** một OrderSubmissionRequest (`order.md`, file riêng — Request KHÔNG chứng minh execution đã xảy ra), một Fill (`fill.md`, file riêng — Result CHỈ tuyên bố executed/not-executed, KHÔNG mang exact quantity/price), venue acknowledgement, exchange payload, hay bất kỳ hình thức Live routing nào. Nó là **bản ghi authoritative, bất biến, tự-giải-thích được** của observation Ride nhận được từ bounded PAPER execution boundary về MỘT Order Submission Request cụ thể — trả lời chính xác bảy câu hỏi: Order/Submission Request nào tạo ra kết quả này? Xử lý result có eligible không? Lần thử xử lý cụ thể nào đã xảy ra? Kết quả chính xác quan sát được là gì? Có Fill nào được sản sinh không (câu hỏi — không phải fact, xem `fill.md`)? Toàn bộ origin chain có còn valid tại thời điểm xử lý không? Replay trước/sau correction thấy gì?

**Ví dụ walking-skeleton duy nhất dùng để validate thiết kế (KHÔNG phải yêu cầu xây dựng general execution-management engine):** một Order `MARKET`/`OPEN_EXPOSURE` PAPER hợp lệ, một `OrderSubmissionRequested` visible-valid duy nhất, một Account, một TradableListing, environment PAPER, một simulated execution result (`EXECUTED` hoặc `NOT_EXECUTED`). Hai mươi bốn Scenario chấp nhận (1–24, xem `fill.md`/`position.md`/`replay-event.md` cho phần còn lại của walking skeleton; `execution-result.md` §15 liệt kê phần liên quan trực tiếp) đều dựa trên ví dụ này.

**`execution-result-processing-attempt-recorded`/`execution-result-recorded`/`execution-result-fact-invalidated`/`execution-result-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây, tách biệt display name/`event_type`, cùng nguyên tắc mọi Domain Contract trước.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/C1–C6** (đóng trước, không chờ review round phát hiện): opaque identity không derive từ scope; envelope binding cho `*FactInvalidated`; fold algorithm "visible-valid-head per logical key" cho Current View; Current View KHÔNG BAO GIỜ authority; canonical policy identifier khai báo ĐÚNG MỘT NƠI, độc lập theo context; direct-predecessor-fact-targeting cho `supersedes_fact_ref` (đúng convention đã khóa tại `risk.md` §10/`order.md` §9, KHÔNG trỏ event invalidation); **bốn bài học riêng từ C4–C6 correction (áp dụng NGAY TỪ v0.1, KHÔNG lặp lại lỗi đã trả giá):** (1) KHÔNG circular reference giữa Attempt và ExecutionResult; (2) `execution_result_processing_attempt_id` (identity cá nhân một lần thử) TÁCH BIỆT khỏi logical result key (`submission_request_id`) — idempotency scoped theo attempt id, KHÔNG theo logical key; (3) `attempt_outcome = PROCESSED` CHỈ ghi SAU KHI bounded result payload computation đã hoàn tất trọn vẹn (đóng trước lớp lỗi `C5-MAJ-01`-style); (4) `FAILED_BEFORE_RESULT` tường minh RETRYABLE. **Logical result key = `submission_request_id`, KHÔNG `order_id`** — một Order có thể nhận Submission Request MỚI sau khi request cũ invalidate (`order.md` §9), ExecutionResult của request cũ TUYỆT ĐỐI KHÔNG được trở thành ExecutionResult của request mới (đóng trước một lớp lỗi tương tự `C6-MAJ-01`-style ngay từ v0.1).

**Phạm vi bounded tường minh:** KHÔNG author Fill/Position/Replay Event (file riêng, cùng Package 0.2-C7). KHÔNG author Live behavior, exchange API payload, external order ID, routing/adapter, cancellation/replacement protocol. KHÔNG venue-specific rejection taxonomy — v0.1 CHỈ hai `result_type`: `EXECUTED`/`NOT_EXECUTED`. KHÔNG partial-fill semantics — v0.1: `result_type = EXECUTED` LUÔN NGỤ Ý đúng một full Fill sản sinh (`fill.md`). KHÔNG fee/slippage/PnL/accounting. KHÔNG general workflow/saga engine. KHÔNG redefine Order/Execution Intent/Risk contract — mọi evidence tham chiếu qua `ref:` trực tiếp. KHÔNG sửa `order.md`/`execution-intent.md`/`risk.md`/`decision.md`/`trade-intent.md`/C1–C6/ADR/Constitution.

## 1. ExecutionResultProcessingAttempt — `kind: entity`

```yaml
id: execution-result-processing-attempt
kind: entity
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Bản ghi authoritative của MỘT lần thử xử lý execution-result observation cho một Order Submission
  Request — kể cả khi không dẫn tới ExecutionResult (INELIGIBLE/FAILED_BEFORE_RESULT). Tách biệt
  hoàn toàn khỏi ExecutionResult identity (§2), đúng pattern OrderCreationAttempt/RiskEvaluationAttempt
  đã proven.
invariants:
  - "execution_result_processing_attempt_id là opaque, globally unique, gán tại ExecutionResultProcessingAttemptRecorded — KHÔNG derive từ order_id/submission_request_id hay bất kỳ field scope nào."
  - "Logical result key = submission_request_id (KHÔNG order_id) — nhiều attempt (kể cả outcome khác nhau) CÓ THỂ tồn tại cùng logical key; idempotency scoped theo execution_result_processing_attempt_id (§9), KHÔNG theo logical key."
schema:
  execution_result_processing_attempt_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  order_id: {type: string, required: true, ref: order}
  submission_request_id: {type: string, required: true, description: "logical result key — xem §2"}
  execution_result_cursor: {type: object, required: true, description: "Replay Cursor hợp lệ, TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1 — xem §2 canonical envelope"}
events_emitted: [ExecutionResultProcessingAttemptRecorded]
events_consumed: []
commands: []
queries: []
```

## 2. Canonical event envelope — áp dụng cho mọi ExecutionResultProcessingAttempt/ExecutionResult event (§3–§5)

Mọi event trong tài liệu này là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). KHÔNG event nào trong tài liệu này thuộc `event_class: decision` — dùng envelope tiêu chuẩn. ExecutionResult dùng `effective_time` tiêu chuẩn (semantic: `result_effective_time` trên `ExecutionResultRecorded`) VÀ `execution_result_cursor` như **PAYLOAD field** (KHÔNG envelope-level), TÁI SỬ DỤNG nguyên vẹn shape Replay Cursor Chapter 8 §8.5.1 — đúng pattern `order.md` §2 đã dùng.

```yaml
envelope:
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE
  event_contract_ref: {cardinality: required}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}
  subject_ref: {cardinality: "required — shape canonical, xem dưới. Trên ExecutionResultFactInvalidated, PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate."}
  stream_ref: {cardinality: required}                # Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # Phase 1, chưa author
  correlation_id: {cardinality: "required — luôn thuộc correlation flow tường minh (originating OrderSubmissionRequested)"}
  causation_refs: {cardinality: "ExecutionResultProcessingAttemptRecorded: zero-or-more (Execution Result Engine internal trigger, Phase 1, chưa author). ExecutionResultRecorded: KHÔNG BAO GIỜ rỗng — PHẢI chứa ExecutionResultProcessingAttemptRecorded tương ứng (§3), CỘNG ExecutionResultFactInvalidated của predecessor nếu là correction replacement (§7). ExecutionResultFactInvalidated: KHÔNG BAO GIỜ rỗng."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3."}
  effective_time: {cardinality: "required — semantic = result_effective_time trên ExecutionResultRecorded (§4); semantic khác trên các event còn lại."}
  decision_time: {cardinality: "PROHIBITED — event_class: decision KHÔNG áp dụng."}
  decision_context_cursor: {cardinality: "PROHIBITED (envelope-level) — execution_result_cursor sống ở PAYLOAD."}
  market_time: {cardinality: "PROHIBITED — ExecutionResult là bounded PAPER boundary observation authoritative, KHÔNG phải quan sát trực tiếp venue thật (Chapter 5 §5.2)."}
  source_identity: {cardinality: "PROHIBITED — luôn phát sinh nội bộ từ bounded PAPER execution boundary/Execution Result Engine (Phase 1, chưa author), KHÔNG BAO GIỜ từ external feed."}

execution_result_cursor (shape, đúng canonical Replay Cursor — Chapter 8 §8.5.1, TÁI SỬ DỤNG nguyên vẹn):
  recorded_time: <timestamp>
  input_contract_ref: {contract_id: <string>, contract_version: <string>}
  stream_registry_version: <string>
  lifecycle_frontier: {stream_id: <string>, position: {kind: <genesis | event>, sequence: <integer>}}
  stream_positions: {<stream_id>: <sequence>, ...}

subject_ref (ExecutionResult — dùng cho ExecutionResultRecorded):
  context_id: execution-result-management
  subject_kind: entity
  subject_type: ExecutionResult
  subject_id: <execution_result_id — opaque, stable, xem §4>
  scope:
    submission_request_id: <string>

subject_ref (ExecutionResultProcessingAttempt, §1):
  context_id: execution-result-management
  subject_kind: entity
  subject_type: ExecutionResultProcessingAttempt
  subject_id: <execution_result_processing_attempt_id — opaque, stable, xem §1>
  scope:
    submission_request_id: <string>

event_types:
  ExecutionResultProcessingAttemptRecorded: EXECUTION_RESULT_PROCESSING_ATTEMPT_RECORDED
  ExecutionResultRecorded: EXECUTION_RESULT_RECORDED
  ExecutionResultFactInvalidated: EXECUTION_RESULT_FACT_INVALIDATED
```

`stream_ref`/`producer_ref` — Phase 1, chưa tồn tại. `execution_result_cursor` field SHAPE bắt buộc ngay v0.1; MECHANISM resolve deferred Phase 1.

**Relational invariants bắt buộc trên `execution_result_cursor`** (Chapter 8 §8.5.2, tái khẳng định KHÔNG lặp lại toàn văn):
```text
execution_result_cursor.recorded_time ≤ ExecutionResultRecorded.recorded_time
fact.recorded_time ≤ execution_result_cursor.recorded_time (mọi authoritative fact dùng cho processing)
```
Vi phạm bất kỳ điều nào → **invalid event, PHẢI bị từ chối khi append** — cơ chế thực thi no-look-ahead.

## 3. `ExecutionResultProcessingAttemptRecorded` — `kind: event`

Kế thừa envelope §2.

```yaml
id: execution-result-processing-attempt-recorded
kind: event
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Fact AUTHORITATIVE DUY NHẤT ghi nhận MỘT lần thử xử lý execution result — LUÔN LUÔN phát, bất kể
  outcome.
invariants:
  - "payload.execution_result_processing_attempt_id PHẢI khớp đúng subject_ref.subject_id."
  - "envelope.effective_time = execution_result_cursor.recorded_time (payload) — mặc định."
  - "attempt_outcome = PROCESSED: reason_code/checked_evidence_refs TUYỆT ĐỐI ABSENT (evidence đầy đủ sống trên ExecutionResultRecorded, §4). Ghi CHỈ SAU KHI bounded result payload computation (§4a) đã hoàn tất trọn vẹn — one-way sequence: computation hoàn tất TRƯỚC, Attempt PROCESSED ghi SAU đó, RỒI ExecutionResultRecorded.causation_refs trỏ ngược lại attempt — KHÔNG atomic multi-event transaction."
  - "attempt_outcome = INELIGIBLE: reason_code = ORDER_RESULT_PROCESSING_INELIGIBLE (`eligible_for_execution_result_processing(order_id, execution_result_cursor) == false`, order.md §8b) — checked_evidence_refs khuyến nghị trỏ fact order.md/execution-intent.md/risk.md xác nhận điều kiện fail."
  - "attempt_outcome = FAILED_BEFORE_RESULT: reason_code = EXECUTION_RESULT_ENGINE_COMPUTATION_BOUNDARY_ERROR (v0.1 CHỈ một giá trị — KHÔNG model broad runtime exception taxonomy, deferred §13); checked_evidence_refs thường rỗng. Tường minh RETRYABLE — một ExecutionResultProcessingAttemptRecorded MỚI (attempt id khác) tại CÙNG logical result key sau đó là hợp lệ."
  - "Idempotency scoped theo TỪNG execution_result_processing_attempt_id (§9) — KHÔNG theo logical result key."
  - "No-look-ahead: mọi checked_evidence_refs PHẢI thỏa fact.recorded_time ≤ execution_result_cursor.recorded_time."
payload:
  execution_result_processing_attempt_id: {type: string, required: true}
  order_id: {type: string, required: true}
  submission_request_id: {type: string, required: true}
  execution_result_cursor: {type: object, required: true, description: "cùng shape §2 — payload field"}
  attempt_outcome: {type: enum, values: [PROCESSED, INELIGIBLE, FAILED_BEFORE_RESULT], required: true}
  reason_code: {type: enum, values: [ORDER_RESULT_PROCESSING_INELIGIBLE, EXECUTION_RESULT_ENGINE_COMPUTATION_BOUNDARY_ERROR], required: false}
  checked_evidence_refs: {type: array, items: event_record_ref, required: false}
```

**Attempt→ExecutionResult query (non-authoritative convenience, KHÔNG cần linking event mới):** cho một attempt PROCESSED, resolve ExecutionResult tương ứng qua `GetExecutionResultForSubmissionRequest(submission_request_id, cursor)` (§6) hoặc reverse-lookup trên authoritative `ExecutionResultRecorded` stream cho fact có `causation_refs` chứa `event_record_ref` của attempt này — đúng đối xứng `order.md` §3.

## 4. `ExecutionResultRecorded` — `kind: event`

Kế thừa envelope §2. Payload đặc thù:

```yaml
id: execution-result-recorded
kind: event
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Fact AUTHORITATIVE cho MỘT execution-result observation từ bounded PAPER execution boundary —
  thiết lập TOÀN BỘ scope (order_id, submission_request_id, originating_execution_intent_id,
  originating_risk_evaluation_id, trade_intent_id, account_id, environment, instrument_selection_ref,
  direction, order_quantity, quantity_unit, result_type) cùng lúc, BẤT BIẾN. CHỈ được phát khi
  ExecutionResultProcessingAttemptRecorded (§3) tương ứng có attempt_outcome = PROCESSED (§4a).
invariants:
  - "payload.execution_result_id PHẢI khớp đúng subject_ref.subject_id VÀ payload.submission_request_id PHẢI khớp đúng subject_ref.scope.submission_request_id."
  - "envelope.effective_time (result_effective_time) = mặc định bằng execution_result_cursor.recorded_time trừ khi backfill lịch sử tường minh pin giá trị khác."
  - "causation_refs PHẢI chứa ExecutionResultProcessingAttemptRecorded (§3) tương ứng, attempt_outcome = PROCESSED, cùng submission_request_id/execution_result_cursor. Quan hệ MỘT CHIỀU — attempt KHÔNG mang tham chiếu ngược."
  - "Logical result key = submission_request_id (KHÔNG order_id). Nếu logical key ĐÃ CÓ một ExecutionResult VALID (visible-valid-head, §6) tại thời điểm ghi, ExecutionResultRecorded MỚI PHẢI resolve/reuse execution_result_id đã tồn tại (payload giống hệt — §9 idempotency) HOẶC bị reject (payload khác, chưa invalidate predecessor) — TUYỆT ĐỐI KHÔNG tạo execution_result_id thứ hai cho CÙNG key trừ khi predecessor ĐÃ invalidate."
  - "order_id/originating_execution_intent_id/originating_risk_evaluation_id/trade_intent_id/account_id/environment/instrument_selection_ref/direction/order_quantity/quantity_unit PHẢI khớp CHÍNH XÁC chuỗi visible-valid tại execution_result_cursor: Order visible-valid-head (order.md §8), submission_request_id chính là visible-valid OrderSubmissionRequested của Order đó (order.md §6/§8a), Execution Intent/RiskEvaluation/TradeIntent/Decision đều valid (order.md §8b, `eligible_for_execution_result_processing`). Reject nếu bất kỳ điều nào sau đúng: predecessor Order (đã bị supersede); Order đã invalidate; Submission Request đã invalidate; submission_request_id thuộc Order KHÁC; Order `WITHDRAWN`/`EXPIRED`; Execution Intent không còn `ISSUED`; Risk/Trade Intent/Decision chain invalid; Account/listing/direction/unit/environment đổi so với origin chain — KHÔNG dùng bất kỳ latest-state Current View nào (OrderCurrentView, ExecutionIntentCurrentView, RiskEvaluationCurrentView) làm input."
  - "**v0.1 (đóng trước lớp lỗi `C6-MAJ-01`-style):** `supersedes_fact_ref` TUYỆT ĐỐI ABSENT cho ExecutionResult gốc (KHÔNG có predecessor). BẮT BUỘC có mặt cho correction replacement, trỏ TRỰC TIẾP predecessor `ExecutionResultRecorded` fact (KHÔNG trỏ `ExecutionResultFactInvalidated` — event đó nằm trong `causation_refs`, xem invariant dưới). Khi có mặt: `payload.execution_result_id` PHẢI KHÁC predecessor; `payload.submission_request_id` PHẢI BẰNG HỆT predecessor (logical result key bất biến xuyên chain); replacement PHẢI supersede đúng lineage head HIỆN TẠI — KHÔNG nhảy cóc."
  - "Khi `supersedes_fact_ref` có mặt, `causation_refs` PHẢI CỘNG THÊM chứa chính `ExecutionResultFactInvalidated` targeting predecessor — predecessor PHẢI đã invalidate VÀ visible TRƯỚC khi replacement này được ghi."
  - "result_type = EXECUTED: đúng MỘT Fill (`fill.md`) được kỳ vọng theo sau (fill.md §4a). result_type = NOT_EXECUTED: KHÔNG Fill nào được phép tồn tại (fill.md §1 invariant)."
```

**§4a — Precondition: ExecutionResultProcessingAttempt PROCESSED, đúng thứ tự.** ExecutionResultRecorded CHỈ được phát SAU KHI một `ExecutionResultProcessingAttemptRecorded` (§3) đã ghi nhận `attempt_outcome = PROCESSED` cho cùng logical result key — VÀ `PROCESSED` CHỈ ghi SAU KHI bounded result payload computation đã hoàn tất trọn vẹn:

```text
1. eligible_for_execution_result_processing(order_id, execution_result_cursor) == true   (order.md §8b)
→ NẾU false: ExecutionResultProcessingAttemptRecorded(attempt_outcome=INELIGIBLE, reason_code=ORDER_RESULT_PROCESSING_INELIGIBLE) ghi — KHÔNG ExecutionResultRecorded nào phát (Scenario 2, §15). Không cần chạy result payload computation.

2. NẾU (1) thỏa: Execution Result Engine CHẠY TRỌN VẸN bounded computation TRƯỚC — copy nguyên vẹn
   scope từ chuỗi visible-valid Order/Submission Request/Execution Intent/Risk/Trade Intent tại
   execution_result_cursor, VÀ xác định result_type (EXECUTED/NOT_EXECUTED) — cơ chế simulation
   PAPER cụ thể deferred Phase 1 (§13), tài liệu này CHỈ pin shape/rule của kết quả, KHÔNG pin
   thuật toán simulation — toàn bộ ExecutionResult payload đã xác định XONG.
   → NẾU lỗi kỹ thuật/domain boundary xảy ra TRONG lúc computation (TRƯỚC khi hoàn tất):
     ExecutionResultProcessingAttemptRecorded(attempt_outcome=FAILED_BEFORE_RESULT) ghi — KHÔNG
     ExecutionResultRecorded nào phát, KHÔNG PROCESSED attempt nào để lại (Scenario 3, §15).
   → NẾU computation hoàn tất trọn vẹn (bất kể result_type cuối là gì):
     ExecutionResultProcessingAttemptRecorded(attempt_outcome=PROCESSED) ghi NGAY SAU, RỒI
     ExecutionResultRecorded phát (causation_refs trỏ attempt vừa ghi) (Scenario 1/5/6, §15).

Thứ tự bắt buộc: computation hoàn tất → Attempt PROCESSED ghi → ExecutionResultRecorded ghi. KHÔNG
BAO GIỜ đảo ngược, KHÔNG atomic transaction giữa ba bước.
```

**Recoverable append gap:** khoảng trống giữa Attempt PROCESSED đã ghi VÀ ExecutionResultRecorded chưa ghi là một RECOVERABLE APPEND GAP — KHÔNG phải data-integrity violation. Recovery logic (Phase 1) PHẢI resolve deterministic: re-run CÙNG computation TẠI CÙNG `submission_request_id`, VÀ append ExecutionResultRecorded với `causation_refs` trỏ ĐÚNG attempt PROCESSED đã tồn tại đó (KHÔNG tạo attempt id MỚI) (Scenario 4, §15).

```yaml
payload:
  execution_result_id: {type: string, required: true}
  order_id: {type: string, required: true}
  submission_request_id: {type: string, required: true}
  originating_execution_intent_id: {type: string, required: true}
  originating_risk_evaluation_id: {type: string, required: true}
  trade_intent_id: {type: string, required: true}
  account_id: {type: string, required: true}
  environment: {type: enum, values: [PAPER], required: true}
  instrument_selection_ref:
    instrument_id: {type: string, required: true}
    venue_id: {type: string, required: true}
    listing_id: {type: string, required: true}
  direction: {type: enum, values: [LONG, SHORT], required: true}
  order_quantity: {type: decimal, required: true, description: "= Order.quantity, order.md §1 — copied, KHÔNG resize"}
  quantity_unit: {type: string, required: true}
  result_type: {type: enum, values: [EXECUTED, NOT_EXECUTED], required: true}
  execution_result_cursor: {type: object, required: true, description: "cùng shape §2 — payload field"}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho ExecutionResult gốc; BẮT BUỘC cho correction replacement — trỏ TRỰC TIẾP predecessor ExecutionResultRecorded fact"}
```

## 5. `ExecutionResultFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2. `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: execution-result-fact-invalidated
kind: event
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Phủ định MỘT `ExecutionResultRecorded` lịch sử ĐÃ SAI. Correction lineage CHUẨN (đối xứng
  `risk.md` §10/`order.md` §9) — replacement NHẬN execution_result_id MỚI, CÙNG logical result key
  (submission_request_id), replacement's `supersedes_fact_ref` trỏ TRỰC TIẾP predecessor
  ExecutionResultRecorded (KHÔNG trỏ event này — `causation_refs` của replacement mới là nơi trỏ
  event này), một visible-valid-head duy nhất. **Ràng buộc bắt buộc với Fill (fill.md):** nếu
  predecessor có `result_type = EXECUTED` VÀ một Fill visible-valid đang tham chiếu predecessor's
  `execution_result_id`, correction PHẢI ĐI KÈM (cùng transaction hoặc atomic-adjacent, xem fill.md
  §2 invariant) một `FillFactInvalidated` targeting Fill đó — KHÔNG được để một Fill visible-valid
  tồn tại dưới một ExecutionResult không còn là visible-valid-head EXECUTED (Scenario 17, §15).
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref."
  - "invalidated_fact_ref PHẢI trỏ một ExecutionResultRecorded, CHƯA từng nhận invalidation khác — một fact chỉ bị invalidate đúng một lần. KHÔNG BAO GIỜ trỏ một ExecutionResultFactInvalidated khác (cấm invalidation-of-invalidation)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead) — thấy predecessor VALID; replay TẠI/SAU recorded_time thấy predecessor EXCLUDED khỏi head resolution (§6)."
  - "Mong đợi (không bắt buộc cùng lúc, nhưng PHẢI trước khi bất kỳ Fill mới nào dùng logical key này) một ExecutionResultRecorded replacement CÙNG submission_request_id, execution_result_id MỚI, supersedes_fact_ref TRỎ TRỰC TIẾP predecessor (§4/§7)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 6. `ExecutionResultCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §3–§5.

```text
Trước khi ExecutionResultRecorded tồn tại cho một submission_request_id:
  → KHÔNG có ExecutionResultCurrentView row nào tồn tại
  → GetExecutionResultForSubmissionRequest trả về NOT_FOUND / ABSENT
```

**Fold algorithm (đúng pattern đã proven tại `risk.md` §7/`order.md` §8 Tầng 1 — explicit chain, KHÔNG "newest uninvalidated fact"):**

```text
1. Group mọi ExecutionResultRecorded theo logical result key = submission_request_id.
2. Trong một key, dựng chain TƯỜNG MINH theo supersedes_fact_ref: E1 (gốc, KHÔNG supersedes_fact_ref)
   → E2 (supersedes_fact_ref = E1, TRỰC TIẾP) → ... (cấm fork/nhảy cóc).
3. Với mỗi Ei trong chain, resolve ExecutionResultFactInvalidated visibility tại cursor.
4. Duyệt chain từ E1: dừng tại link ĐẦU TIÊN chưa bị invalidate visible tại cursor — đó là
   visible-valid-head. current_execution_result_id = head đó.
5. NẾU link cuối cùng đã duyệt bị invalidate visible VÀ KHÔNG CÓ link kế tiếp visible → view_state
   = PENDING_CORRECTION, pending_correction_class = AWAITING_SAME_SUBJECT_REPLACEMENT, DỪNG.
```

```yaml
id: execution-result-current-view
kind: read_model
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Projection tiện dụng: execution_result_id "hiện tại" cho một submission_request_id, rebuild được
  từ §3–§5. KHÔNG authoritative — CHỈ query/UI, KHÔNG BAO GIỜ là input hợp lệ cho Fill derivation
  hay bất kỳ computation nào khác (Package 0.2-C7, `fill.md`). Downstream field PHẢI resolve qua
  authoritative ExecutionResult event stream (`ref: execution-result`) TẠI CÙNG cursor mà computation
  đó đang dùng (§10).
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho Fill derivation hay bất kỳ computation nào khác — CHỈ query/UI."
  - "view_state PHẢI đúng theo fold algorithm trên."
  - "pending_correction_class BẮT BUỘC có mặt khi view_state = PENDING_CORRECTION; CẤM có mặt khi view_state = VALID."
schema:
  submission_request_id: {type: string, required: true, description: "logical result key"}
  current_execution_result_id: {type: string, required: false, description: "chỉ có mặt khi view_state = VALID"}
  scope: {result: string, required: true, description: "chỉ có mặt khi view_state = VALID — toàn bộ payload head hiện hành"}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  pending_correction_class: {type: enum, values: [AWAITING_SAME_SUBJECT_REPLACEMENT], required: false}
  last_recorded_time: timestamp
queries: [GetExecutionResultForSubmissionRequest, GetExecutionResultById, GetExecutionResultHistory]
```

## 7. Correction lineage

`ExecutionResultRecorded` — correction lineage CHUẨN, same-key replacement với `execution_result_id` MỚI (đối xứng `risk.md` §10/`order.md` §9):

```text
E1 (ExecutionResultRecorded, submission_request_id = S1, KHÔNG supersedes_fact_ref)
  → ExecutionResultFactInvalidated targeting E1
  → E2 (ExecutionResultRecorded MỚI), execution_result_id KHÁC E1, CÙNG submission_request_id = S1,
    E2.supersedes_fact_ref = E1 TRỰC TIẾP, E2.causation_refs CHỨA CẢ
    ExecutionResultProcessingAttemptRecorded(PROCESSED) LẪN ExecutionResultFactInvalidated targeting
    E1 → một visible-valid-head duy nhất
```

**Mười invariant bắt buộc (đối xứng `risk.md` §10/`order.md` §9, KHÔNG lặp lại toàn văn):** (1) gốc KHÔNG supersedes_fact_ref; (2) replacement BẮT BUỘC supersedes_fact_ref trỏ TRỰC TIẾP predecessor; (3) replacement CÙNG `submission_request_id`; (4) `causation_refs` của replacement chứa chính invalidation event, predecessor invalidate+visible TRƯỚC; (5) supersede đúng head hiện tại, cấm nhảy cóc; (6) tối đa một replacement trực tiếp, cấm fork; (7) replacement không visible trước invalidation; (8) append-only, `execution_result_id` cũ vẫn resolvable; (9) fact đã invalidate không tái sử dụng ngầm — `ExecutionResultCurrentView` (§6) loại trừ tường minh; (10) retry payload khác khi predecessor chưa invalidate vẫn là conflict.

**Ràng buộc bổ sung riêng cho `execution-result.md` (Scenario 17, §15):** nếu `E1.result_type = EXECUTED` và một Fill visible-valid tham chiếu `E1.execution_result_id`, correction E1→E2 (bất kể `E2.result_type`) PHẢI ĐI KÈM một `FillFactInvalidated` targeting Fill đó (fill.md §2/§4) — KHÔNG có trạng thái trung gian nào trong đó Fill visible-valid tồn tại dưới một ExecutionResult không còn là visible-valid-head EXECUTED. `S1 KHÔNG kế thừa sang S2`: nếu Submission Request S1 bị invalidate và S2 thay thế (order.md §9), ExecutionResult của S1 (nếu có) VẪN gắn với `submission_request_id = S1`, KHÔNG BAO GIỜ tự động áp dụng cho S2 — S2 cần processing Attempt/ExecutionResult RIÊNG của chính nó nếu tới lượt eligible.

## 8. Time semantics và bitemporal correctness

- `effective_time` — required trên mọi event trong tài liệu này.
- `recorded_time` — recorded axis, universal.
- `OrderSubmissionRequested.recorded_time < ExecutionResultRecorded.recorded_time` — strict causal ordering (Scenario N-equivalent, xem `fill.md` §7 cho continuation).
- `OrderSubmissionRequested.effective_time <= ExecutionResultRecorded.result_effective_time`.
- Mọi authoritative fact dùng cho processing PHẢI thỏa `fact.recorded_time <= execution_result_cursor.recorded_time <= ExecutionResultRecorded.recorded_time`.
- Replay tại cursor T chỉ thấy fact có `recorded_time ≤ T` — invalidation ghi SAU T KHÔNG visible tại T.
- `market_time` PROHIBITED xuyên suốt tài liệu này.

## 9. Canonical policy identifiers — nguồn duy nhất (context `execution-result-management`)

```yaml
initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS
execution_result_derivation_idempotency_policy: ONE_VALID_RESULT_PER_SUBMISSION_REQUEST
execution_result_processing_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT
execution_result_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE
```

**`initial_fact_correction_policy`** — áp dụng CHỈ cho `ExecutionResultProcessingAttemptRecorded` (§3, KHÔNG same-ID replacement).

**`execution_result_derivation_idempotency_policy: ONE_VALID_RESULT_PER_SUBMISSION_REQUEST`** — logical result key = `submission_request_id` (KHÔNG `order_id`); retry cùng key + cùng payload (chưa invalidate) → idempotent no-op; retry cùng key + payload KHÁC (chưa invalidate predecessor) → deterministic conflict. **KHÔNG unstated cross-stream atomicity** — OrderSubmissionRequested và ExecutionResult là hai authoritative stream RIÊNG.

**`execution_result_processing_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT`** — idempotency scoped theo TỪNG `execution_result_processing_attempt_id`, KHÔNG theo logical result key.

**`execution_result_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE`** — xem §7 cho đầy đủ.

## 10. Downstream reference contract (cho `fill.md`)

`fill.md` tham chiếu ExecutionResult qua ĐÚNG các field sau, KHÔNG hơn:

```yaml
execution_result_id: {type: string, required: true, ref: execution-result}
order_id: {type: string, description: "= §4, ref: order"}
submission_request_id: {type: string, description: "= §4 — logical result key"}
originating_execution_intent_id: {type: string, description: "= §4, ref: execution-intent"}
originating_risk_evaluation_id: {type: string, description: "= §4, ref: risk"}
trade_intent_id: {type: string, description: "= §4, ref: trade-intent"}
account_id: {type: string, ref: account, description: "= §4"}
environment: {type: enum, values: [PAPER], description: "= §4"}
instrument_selection_ref: {type: object, description: "= §4 — {instrument_id, venue_id, listing_id}"}
direction: {type: enum, values: [LONG, SHORT], description: "= §4"}
order_quantity: {type: decimal, description: "= §4"}
quantity_unit: {type: string, description: "= §4"}
result_type: {type: enum, values: [EXECUTED, NOT_EXECUTED], description: "= §4 — GUARANTEE: EXECUTED → đúng một Fill kỳ vọng; NOT_EXECUTED → KHÔNG Fill nào được phép"}
```

**Downstream authority rule:** `fill.md` PHẢI resolve mọi field trên TRỰC TIẾP từ authoritative ExecutionResult event stream (§3–§5) TẠI ĐÚNG cursor mà chính computation đó đang dùng — VÀ PHẢI xác nhận field đó là visible-valid-head (§6 fold, KHÔNG dùng `ExecutionResultCurrentView` latest-state làm input). `execution-result.md` KHÔNG author semantics của Fill/Position (file riêng).

## 11. Explanation contract

**Explanation là derived, non-authoritative rendering.** Structured facts (§1/§3–§4) là authoritative; text rendering CHỈ là một hàm thuần túy của evidence đã có.

```text
Explanation(execution_result_id) = deterministic render của {originating Order/Submission Request
scope, eligibility result, processing attempt, result_type} — KHÔNG computation mới, KHÔNG external
lookup, KHÔNG dùng bất kỳ giá trị nào không có mặt trong §1/§3–§4.
```

## 12. Prohibitions

**ExecutionResult/ExecutionResultProcessingAttempt KHÔNG được sở hữu:** Order/Execution Intent/RiskEvaluation/Trade Intent/Decision identity semantics; Fill/Position semantics (`fill.md`/`position.md`, file riêng); venue-specific rejection taxonomy; external order ID/exchange payload/routing/adapter behavior; fee/slippage/PnL/accounting; general workflow/saga engine; broad runtime exception telemetry/observability infrastructure; UI copy/natural-language generation infrastructure; database transaction/outbox/message-broker technology.

## 13. Ngoài phạm vi — defer

- Stream Registry/Input Contract implementation cụ thể — `execution_result_cursor` field SHAPE pin ngay v0.1, MECHANISM resolve deferred Phase 1.
- Cơ chế/thuật toán PAPER simulation cụ thể xác định `result_type` (§4a) — tài liệu này CHỈ pin shape/rule của kết quả, KHÔNG pin thuật toán simulation.
- Granular exception/technical-failure sub-taxonomy cho `FAILED_BEFORE_RESULT` — v0.1 CHỈ một reason_code.
- Correction lineage riêng cho `ExecutionResultProcessingAttempt` — edge case hiếm, append-only đủ cho v0.1.
- Implementation technology cho Order Submission Request→ExecutionResult và ExecutionResult→Fill recovery (retry queue/outbox/message-broker) — boundary semantic pin, KHÔNG chọn công nghệ.
- Runtime worker ownership, transaction boundaries, retry/backoff, monitoring/escalation.
- Fill/Position/Replay Event semantics — hoàn toàn ngoài phạm vi Domain Contract này (`fill.md`/`position.md`/`replay-event.md`).

## 14. Open questions ngoài phạm vi

- Cơ chế cụ thể generate `execution_result_id`/`execution_result_processing_attempt_id` — chưa quyết, Phase 1.
- Retention/resolvability horizon cụ thể cho ExecutionResult/Attempt đã lâu.
- Không đóng OQ-002/OQ-003.

## 15. Acceptance scenarios (validation, không phải executable test tại C7 — phần liên quan trực tiếp `execution-result.md`; xem `fill.md`/`position.md`/`replay-event.md` cho scenario liên quan Fill/Position/Replay)

**Scenario 1 — Eligible result processing:** Order visible-valid-head, một Submission Request valid, Order status `SUBMISSION_REQUESTED`, complete origin chain valid (`eligible_for_execution_result_processing=true`) → processing Attempt `PROCESSED` → một `ExecutionResultRecorded`.

**Scenario 2 — Ineligible result processing:** `eligible_for_execution_result_processing=false` → Attempt `INELIGIBLE` → KHÔNG ExecutionResult, KHÔNG Fill.

**Scenario 3 — Failure and retry:** Attempt A1 (`FAILED_BEFORE_RESULT`); Attempt A2 (CÙNG `submission_request_id`, `PROCESSED`) sau đó — HỢP LỆ, recovery allowed.

**Scenario 4 — Result append gap:** Attempt `PROCESSED` → crash TRƯỚC `ExecutionResultRecorded` → recovery: tái sử dụng attempt PROCESSED, append/reuse ĐÚNG MỘT ExecutionResult.

**Scenario 5 — Executed:** `result_type=EXECUTED` → đúng một Fill kỳ vọng theo sau (`fill.md` Scenario 5).

**Scenario 6 — Not executed:** `result_type=NOT_EXECUTED` → zero Fill (`fill.md` Scenario 6), Position unchanged.

**Scenario 17 — Result correction EXECUTED→NOT_EXECUTED:** E1 `EXECUTED` → F1 tồn tại → invalidate E1 → E2 `NOT_EXECUTED` → E1 invalidation PHẢI ĐI KÈM `FillFactInvalidated` targeting F1 (§7) — trạng thái corrected cuối cùng KHÔNG chứa Fill visible-valid nào; Position recompute theo (`position.md` Scenario 17).

**Scenario 18 — Invalidated Submission Request:** Submission Request invalidate TRƯỚC khi result processing → `eligible_for_execution_result_processing=false` (order.md §8b điều kiện 3 fail) → KHÔNG eligible result processing nào.

**Scenario 19 — Order replacement:** O1 + S1 → invalidate O1 → O2 replacement → S1 gắn O1 KHÔNG còn hợp lệ cho processing MỚI (O1 không còn visible-valid-head) → O2 cần Submission Request RIÊNG, rồi ExecutionResult RIÊNG.

**Scenario 20 — Execution Intent withdrawn:** Execution Intent `WITHDRAWN` → `eligible_for_execution_result_processing=false` (order.md §8b điều kiện 2 fail, transitively) → result processing ineligible.
