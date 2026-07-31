---
id: order
title: Order
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

# Order

> **Vai trò của tài liệu này:** Domain Contract duy nhất của Package 0.2-C6 (Order Foundation) — định nghĩa **Order** (bản ghi authoritative, bất biến, của MỘT execution instruction nội bộ được tạo từ ĐÚNG MỘT Execution Intent eligible), **OrderCreationAttempt** (bản ghi authoritative của MỘT LẦN THỬ tạo Order — kể cả khi không dẫn tới Order), và **OrderSubmissionRequest** (bản ghi authoritative của MỘT lần Ride yêu cầu gửi một Order hợp lệ tới PAPER execution boundary). Draft, chưa Approved/Locked. Thuộc capability `execution-management` / context `order-management` (đăng ký MỚI tại [`context-map.yaml`](./context-map.yaml)). Kiến trúc controlling: [`execution-intent.md`](./execution-intent.md) v0.2 Draft §6a (`eligible_for_new_order_creation`, KHÔNG sửa), [`risk.md`](./risk.md) v0.3 Draft (bốn bài học đã trả giá qua C4/C5's các vòng correction — ÁP DỤNG LẠI đúng semantic đã proven, KHÔNG sao chép cơ học), [Chapter 8 §8.1.1/§8.2/§8.5](../constitution/08-event-model.md) (Locked, Referenced Authoritative Artifact + canonical Replay Cursor — TÁI SỬ DỤNG nguyên vẹn, KHÔNG tạo schema gần giống). Tài liệu này CHỈ implement field/invariant mà các nguồn trên yêu cầu, KHÔNG tự quyết architecture mới ngoài phạm vi đã khóa.

Order **KHÔNG phải** Execution Intent (`execution-intent.md`, file riêng — Order KHÔNG redefine Risk authorization semantics), exchange payload, venue acceptance, execution confirmation, Fill hay Position (Package 0.2-C7, chưa author), hay bằng chứng execution đã xảy ra. Nó là **bản ghi authoritative, bất biến, tự-giải-thích được** của một internal execution instruction đã được Risk Gateway (qua Execution Intent) authorize — trả lời chính xác bảy câu hỏi: Execution Intent nào được xem xét? Có eligible cho Order creation không? Lần thử tạo cụ thể nào đã xảy ra? Order bất biến chính xác nào được tạo? Ride có yêu cầu gửi tới PAPER execution boundary không? Pre-Fill lifecycle state hiện tại là gì? Order có eligible cho C7 processing trong tương lai không?

**Ví dụ walking-skeleton duy nhất dùng để validate thiết kế (KHÔNG phải yêu cầu xây dựng general order-management engine):** một Execution Intent `OPEN_EXPOSURE` eligible, một Account, một TradableListing, environment PAPER, một strictly positive approved quantity, một Order `MARKET` duy nhất, zero hoặc một Order từ Execution Intent đó, một `OrderSubmissionRequested` tùy chọn. Hai mươi bốn Scenario chấp nhận (1–24, xem §17) đều dựa trên ví dụ này.

**`order-creation-attempt-recorded`/`order-created`/`order-status-changed`/`order-submission-requested`/`order-fact-invalidated`/`order-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây, tách biệt display name/`event_type`, cùng nguyên tắc mọi Domain Contract trước.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/C1–C5** (đóng trước, không chờ review round phát hiện): opaque identity không derive từ scope; envelope binding cho `*FactInvalidated`; fold algorithm "visible-valid-head per logical key" cho Current View; Current View KHÔNG BAO GIỜ authority; canonical policy identifier khai báo ĐÚNG MỘT NƠI, độc lập theo context; **ba bài học riêng từ C4/C5 correction (áp dụng NGAY TỪ v0.1, KHÔNG lặp lại lỗi đã trả giá):** (1) KHÔNG circular reference giữa Attempt và Order — Attempt KHÔNG mang field trỏ tới Order, chỉ Order trỏ ngược lại Attempt qua `causation_refs` (one-way sequence, đóng trước lớp lỗi `C4-DELTA-MAJ-01`-style); (2) `order_creation_attempt_id` (identity cá nhân một lần thử) TÁCH BIỆT khỏi logical creation key (`originating_execution_intent_id`) — idempotency scoped theo `order_creation_attempt_id`, KHÔNG theo logical key, cho phép nhiều attempt (kể cả outcome khác nhau) cùng key (đóng trước lớp lỗi `C4-DELTA-MAJ-02`-style); (3) `attempt_outcome = CREATED` CHỈ ghi SAU KHI bounded Order payload computation đã hoàn tất trọn vẹn — KHÔNG BAO GIỜ ghi TRƯỚC (đóng trước lớp lỗi `C5-MAJ-01`-style); (4) `FAILED_BEFORE_CREATION` tường minh RETRYABLE, KHÔNG permanently block same-origin recovery.

**Phạm vi bounded tường minh:** KHÔNG author Fill/Position/Replay Event (Package 0.2-C7). KHÔNG định nghĩa partial fill/venue acceptance/rejection/external order ID/exchange API payload/order routing/exchange adapter behavior. KHÔNG Limit/Stop/advanced order type — v0.1 CHỈ `MARKET`. KHÔNG TIF/IOC/FOK/post_only/reduce_only. KHÔNG fee/slippage/accounting. KHÔNG margin/leverage/liquidation model. KHÔNG resize/clamp/round lại Risk-approved quantity — quantity LUÔN copy nguyên vẹn từ Execution Intent. KHÔNG redefine Execution Intent/Risk contract — mọi evidence tham chiếu qua `ref:` trực tiếp hoặc `event_record_ref` opaque. KHÔNG Live behavior. KHÔNG submission retry worker/queue. KHÔNG general workflow engine. KHÔNG sửa `execution-intent.md`/`risk.md`/`decision.md`/`trade-intent.md`/C1–C5/ADR/Constitution.

**v0.2 — bounded correction, đóng `C6-MAJ-01`/`C6-MAJ-02`/`C6-MAJ-03` (consolidated Review A + Independent Review B findings):** (a) `C6-MAJ-01` — thêm `supersedes_fact_ref` vào `OrderCreated.payload` (thiếu trong v0.1 dù correction prose đã yêu cầu); pin CHÍNH XÁC convention direct-predecessor-fact-targeting (đối xứng `risk.md` §10 — `supersedes_fact_ref` trỏ TRỰC TIẾP predecessor `OrderCreated` fact, KHÔNG trỏ `OrderFactInvalidated`; `causation_refs` mới là nơi trỏ event invalidation đó); thêm mười invariant correction lineage tường minh; cập nhật fold algorithm Tầng 1 dựng EXPLICIT chain theo `supersedes_fact_ref` (KHÔNG chọn head chỉ bằng "newest uninvalidated fact"). (b) `C6-MAJ-02` — cho phép `OrderFactInvalidated` target `OrderSubmissionRequested` (invalidate-only, KHÔNG same-ID replacement bắt buộc); cập nhật fold algorithm Tầng 2 loại trừ request đã invalidate khỏi lifecycle/duplicate-suppression/C7 readiness (KHÔNG compensating event); một request MỚI CÓ THỂ append sau nếu `eligible_for_new_submission_request` true lại. (c) `C6-MAJ-03` — `eligible_for_execution_result_processing` (§8b) nay dùng TRỌN VẸN `eligible_for_new_order_creation` (bao gồm điều kiện 1, `ExecutionIntent.current_status(C) == ISSUED`, trước đây bị bỏ sót) VÀ pin CHÍNH XÁC `current_status == SUBMISSION_REQUESTED` (trước đây chỉ "khác WITHDRAWN/EXPIRED", sai cho phép `CREATED` pass). Bounded — không đổi opaque `order_id`, logical creation key, per-attempt identity, truthful Attempt ordering, retry sau `FAILED_BEFORE_CREATION`, zero-or-one valid Order head, exact origin preservation, strictly positive quantity, no resize/clamp/round, PAPER/OPEN_EXPOSURE/MARKET boundary, no cross-stream atomicity, time/cursor/no-look-ahead, non-authoritative Current View, C1–C5 semantics, Context Map ownership/dependency edge, C6/C7 boundary.

## 1. Order — `kind: entity`

```yaml
id: order
kind: entity
capability_id: execution-management
domain_context_id: order-management
description: >
  Bản ghi authoritative, bất biến, của MỘT internal execution instruction được tạo từ ĐÚNG MỘT
  Execution Intent eligible. Định nghĩa Ride ĐỊNH gửi gì tới bounded PAPER execution boundary —
  KHÔNG chứng minh đã submit, đã venue-accept, hay đã execute. Scope hoàn toàn bất biến sau khi
  tạo — KHÔNG có "mutable metadata" tách biệt (đối xứng ExecutionIntentIssued, execution-intent.md
  §1). Lifecycle tối thiểu (CREATED/SUBMISSION_REQUESTED/WITHDRAWN/EXPIRED, §5/§6) là phần DUY NHẤT
  thay đổi qua thời gian.
invariants:
  - "order_id là opaque, globally unique trong toàn Ride, gán tại OrderCreated — KHÔNG derive/resolve từ originating_execution_intent_id hay bất kỳ field scope nào. Bất biến, KHÔNG tái sử dụng cho subject khác (Chapter 6 §6.1)."
  - "MỘT Order originate từ ĐÚNG MỘT Execution Intent (originating_execution_intent_id, ref: execution-intent), eligible_for_new_order_creation == true TẠI order_context_cursor — không multi-intent aggregation, đúng §9 cardinality."
  - "`originating_execution_intent_id` là logical creation key — tại một cursor cho trước, tối đa MỘT Order VALID (visible-valid-head) cho mỗi `originating_execution_intent_id` (§11 `order_creation_derivation_idempotency_policy: ONE_VALID_ORDER_PER_ORIGINATING_EXECUTION_INTENT`). Retry cùng origin + cùng payload → idempotent, trả về `order_id` đã tồn tại; retry cùng origin + payload KHÁC (predecessor chưa invalidate) → deterministic conflict, reject."
  - "originating_risk_evaluation_id/trade_intent_id/account_id/instrument_selection_ref/direction/quantity/quantity_unit PHẢI BẰNG HỆT origin chain tương ứng của originating_execution_intent_id (execution-intent.md §1) — Order KHÔNG được tự chọn Account/instrument/direction/quantity khác Execution Intent gốc đã pin (Scenario 6, §17)."
  - "quantity PHẢI finite, STRICTLY POSITIVE (> 0), VÀ CHÍNH XÁC BẰNG `approved_quantity` của originating_execution_intent_id (execution-intent.md §1) — Order KHÔNG BAO GIỜ resize/clamp/round lại Risk-approved quantity. quantity_unit PHẢI CHÍNH XÁC BẰNG `quantity_unit` gốc."
  - "Order KHÔNG BAO GIỜ mutate Execution Intent scope — mọi field liên quan chỉ COPY từ Execution Intent gốc để tiện truy vấn, KHÔNG phải nguồn authoritative thứ hai; nguồn authoritative luôn là chính Execution Intent (execution-intent.md §1/§3)."
  - "Order KHÔNG tự chứng minh đã submit/đã venue-accept/đã execute dưới bất kỳ hình thức nào — `OrderCreated` chỉ thiết lập instruction bất biến; submission request (§6) là một fact RIÊNG, execution/Fill hoàn toàn thuộc Package 0.2-C7 (chưa author)."
schema:
  order_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  originating_execution_intent_id: {type: string, required: true, ref: execution-intent, description: "đúng một Execution Intent, eligible_for_new_order_creation == true tại order_context_cursor"}
  originating_risk_evaluation_id: {type: string, required: true, ref: risk, description: "= execution-intent.md §1 originating_risk_evaluation_id, copied"}
  trade_intent_id: {type: string, required: true, ref: trade-intent, description: "= execution-intent.md §1"}
  account_id: {type: string, required: true, ref: account, description: "= execution-intent.md §1"}
  environment: {type: enum, values: [PAPER], required: true, description: "v0.1: chỉ PAPER — copied từ origin chain đã policy-gated PAPER-only tại risk.md §5c bước 8; Order KHÔNG tự enforce lại policy đó, chỉ phản ánh"}
  instrument_selection_ref:
    type: object
    required: true
    description: "= execution-intent.md §1 — CÙNG shape strategy.md §5/§10"
    fields:
      instrument_id: {type: string, required: true}
      venue_id: {type: string, required: true}
      listing_id: {type: string, required: true}
  direction: {type: enum, values: [LONG, SHORT], required: true, description: "= execution-intent.md §1 — PHẢI khớp chính xác"}
  order_action: {type: enum, values: [OPEN_EXPOSURE], required: true, description: "v0.1: chỉ OPEN_EXPOSURE — đối xứng execution_action, KHÔNG mở rộng"}
  order_type: {type: enum, values: [MARKET], required: true, description: "v0.1: chỉ MARKET — KHÔNG Limit/Stop/advanced order type"}
  quantity: {type: decimal, required: true, description: "finite, STRICTLY POSITIVE, CHÍNH XÁC BẰNG approved_quantity gốc — KHÔNG resize/clamp/round"}
  quantity_unit: {type: string, required: true, description: "= execution-intent.md §1"}
  order_context_cursor: {type: object, required: true, description: "Replay Cursor hợp lệ, TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1 — xem §2"}
  order_effective_time: {type: timestamp, required: true, description: "effective-axis value — xem §4"}
state_machine:
  initial_state: UNSEEN
  states: [UNSEEN, CREATED, SUBMISSION_REQUESTED, WITHDRAWN, EXPIRED]
  transitions:
    - {from: UNSEEN, to: CREATED, caused_by: OrderCreated}
    - {from: CREATED, to: SUBMISSION_REQUESTED, caused_by: OrderSubmissionRequested}
    - {from: CREATED, to: WITHDRAWN, caused_by: OrderStatusChanged}
    - {from: CREATED, to: EXPIRED, caused_by: OrderStatusChanged}
    - {from: SUBMISSION_REQUESTED, to: WITHDRAWN, caused_by: OrderStatusChanged}
    - {from: SUBMISSION_REQUESTED, to: EXPIRED, caused_by: OrderStatusChanged}
  terminal_states: [WITHDRAWN, EXPIRED]
events_emitted: [OrderCreationAttemptRecorded, OrderCreated, OrderStatusChanged, OrderSubmissionRequested, OrderFactInvalidated]
events_consumed: []
commands: []
queries: []
```

**`UNSEEN` là notional initial state** — cùng convention xuyên suốt tài liệu. Lifecycle tối thiểu — chỉ đủ để C7 (Fill/Position, chưa author) xác định Order còn eligible cho execution-result processing hay không: `CREATED` (Order bất biến đã tạo, chưa yêu cầu gửi); `SUBMISSION_REQUESTED` (Ride đã yêu cầu gửi tới PAPER execution boundary — KHÔNG chứng minh venue acceptance); `WITHDRAWN` (rút lại trước khi execution — lý do cụ thể thuộc Phase 1); `EXPIRED` (hết hiệu lực theo thời gian — chính sách hết hạn cụ thể Phase 1, §15). **KHÔNG author** `SUBMITTED`/`ACCEPTED`/`REJECTED_BY_VENUE`/`PARTIALLY_FILLED`/`FILLED`/`CANCELLED_BY_VENUE` — những state đó thuộc Package 0.2-C7. `WITHDRAWN`/`EXPIRED` là terminal CHO FORWARD TRANSITION nhưng correctable append-only (§7, đóng trước lớp lỗi `C2-MAJ-02`/`C3-MAJ-02`-style, không chờ review round phát hiện) — `supersedes_fact_ref` có mặt ngay từ v0.1 trên `OrderStatusChanged`.

## 2. Canonical event envelope — áp dụng cho mọi Order/OrderCreationAttempt/OrderSubmissionRequest event (§3–§7)

Mọi event trong tài liệu này là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). KHÔNG event nào trong tài liệu này thuộc `event_class: decision` — dùng envelope tiêu chuẩn, KHÔNG `decision_time`/`decision_context_cursor`. Order dùng `effective_time` tiêu chuẩn (semantic: `order_effective_time` trên `OrderCreated`) VÀ `order_context_cursor`/`submission_context_cursor` như **PAYLOAD field** (KHÔNG phải envelope-level), TÁI SỬ DỤNG nguyên vẹn shape Replay Cursor Chapter 8 §8.5.1 — đúng pattern `risk.md` §3/`decision.md` §3 đã dùng.

```yaml
envelope:
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2)
  event_contract_ref: {cardinality: required}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}             # khi Ride ghi nhận fact này
  subject_ref: {cardinality: "required — shape canonical, xem dưới. Trên OrderFactInvalidated, PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate."}
  stream_ref: {cardinality: required}                # Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # Phase 1, chưa author
  correlation_id: {cardinality: "required — Order LUÔN thuộc một correlation flow tường minh (originating Execution Intent)"}
  causation_refs: {cardinality: "OrderCreationAttemptRecorded: zero-or-more (Order Engine internal trigger, Phase 1, chưa author). OrderCreated: KHÔNG BAO GIỜ rỗng — PHẢI chứa OrderCreationAttemptRecorded tương ứng (§3), CỘNG OrderFactInvalidated của predecessor nếu là correction replacement (§9). OrderStatusChanged/OrderSubmissionRequested/OrderFactInvalidated: KHÔNG BAO GIỜ rỗng."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3."}
  effective_time: {cardinality: "required trên mọi event trong tài liệu này — semantic = order_effective_time trên OrderCreated (§4); semantic khác trên các event còn lại, xem §3/§5/§6/§7."}
  decision_time: {cardinality: "PROHIBITED — event_class: decision KHÔNG áp dụng cho Order."}
  decision_context_cursor: {cardinality: "PROHIBITED (envelope-level) — order_context_cursor/submission_context_cursor sống ở PAYLOAD."}
  market_time: {cardinality: "PROHIBITED — Order là internal instruction authoritative, không phải quan sát trực tiếp venue (Chapter 5 §5.2)."}
  source_identity: {cardinality: "PROHIBITED — luôn phát sinh nội bộ từ Order Engine (Phase 1, chưa author), KHÔNG BAO GIỜ từ external feed."}

order_context_cursor / submission_context_cursor (shape, đúng canonical Replay Cursor — Chapter 8 §8.5.1, TÁI SỬ DỤNG nguyên vẹn, KHÔNG một schema gần giống):
  recorded_time: <timestamp>                          # required — knowledge boundary
  input_contract_ref: {contract_id: <string>, contract_version: <string>}   # required — versioned, immutable (§8.1.1)
  stream_registry_version: <string>                   # required
  lifecycle_frontier:                                  # required
    stream_id: <string>                                # canonical lifecycle stream
    position: {kind: <genesis | event>, sequence: <integer>}
  stream_positions: {<stream_id>: <sequence>, ...}     # required — map, mọi stream thuộc universe của cursor

subject_ref (Order — dùng cho OrderCreated/OrderStatusChanged):
  context_id: order-management
  subject_kind: entity
  subject_type: Order
  subject_id: <order_id — opaque, stable, xem §1>
  scope:
    originating_execution_intent_id: <string>

subject_ref (OrderCreationAttempt, §3):
  context_id: order-management
  subject_kind: entity
  subject_type: OrderCreationAttempt
  subject_id: <order_creation_attempt_id — opaque, stable, xem §3>
  scope:
    originating_execution_intent_id: <string>

subject_ref (OrderSubmissionRequest, §6):
  context_id: order-management
  subject_kind: entity
  subject_type: OrderSubmissionRequest
  subject_id: <submission_request_id — opaque, stable, xem §6>
  scope:
    order_id: <string>

event_types:
  OrderCreationAttemptRecorded: ORDER_CREATION_ATTEMPT_RECORDED
  OrderCreated: ORDER_CREATED
  OrderStatusChanged: ORDER_STATUS_CHANGED
  OrderSubmissionRequested: ORDER_SUBMISSION_REQUESTED
  OrderFactInvalidated: ORDER_FACT_INVALIDATED
```

`stream_ref`/`producer_ref` — Phase 1, chưa tồn tại. `order_context_cursor`/`submission_context_cursor` field SHAPE bắt buộc ngay v0.1 (tái sử dụng Chapter 8 §8.5.1 Locked); MECHANISM resolve (Stream Registry cụ thể) deferred Phase 1.

**Relational invariants bắt buộc trên `order_context_cursor`/`submission_context_cursor`** (Chapter 8 §8.5.2, tái khẳng định KHÔNG lặp lại toàn văn):
```text
order_context_cursor.recorded_time ≤ OrderCreated.recorded_time
submission_context_cursor.recorded_time ≤ OrderSubmissionRequested.recorded_time
fact.recorded_time ≤ tương ứng cursor.recorded_time (mọi authoritative fact dùng cho creation/submission)
```
Vi phạm bất kỳ điều nào → **invalid event, PHẢI bị từ chối khi append** — cơ chế thực thi no-look-ahead cho Order.

## 3. `OrderCreationAttemptRecorded` — `kind: event`

Kế thừa envelope §2.

```yaml
id: order-creation-attempt-recorded
kind: event
capability_id: execution-management
domain_context_id: order-management
description: >
  Fact AUTHORITATIVE DUY NHẤT ghi nhận MỘT lần thử tạo Order — LUÔN LUÔN phát, bất kể outcome.
invariants:
  - "payload.order_creation_attempt_id PHẢI khớp đúng subject_ref.subject_id."
  - "envelope.effective_time = order_context_cursor.recorded_time (payload) — mặc định, trừ khi backfill lịch sử tường minh pin giá trị khác."
  - "attempt_outcome = CREATED: reason_code/checked_evidence_refs TUYỆT ĐỐI ABSENT (evidence đầy đủ sống trên OrderCreated, §4). Ghi CHỈ SAU KHI bounded Order payload computation (§4a) đã hoàn tất trọn vẹn — KHÔNG BAO GIỜ ghi cho một computation CHƯA hoàn tất. KHÔNG payload field nào trỏ tới Order — one-way sequence: computation hoàn tất TRƯỚC, Attempt CREATED ghi SAU đó, RỒI OrderCreated.causation_refs trỏ ngược lại attempt (§4) — KHÔNG atomic multi-event transaction giữa ba bước này."
  - "attempt_outcome = INELIGIBLE: reason_code = EXECUTION_INTENT_INELIGIBLE (`eligible_for_new_order_creation(originating_execution_intent_id, order_context_cursor) == false`, execution-intent.md §6a) — checked_evidence_refs khuyến nghị trỏ fact execution-intent.md/risk.md/trade-intent.md xác nhận điều kiện fail."
  - "attempt_outcome = FAILED_BEFORE_CREATION: reason_code = ORDER_ENGINE_COMPUTATION_BOUNDARY_ERROR (v0.1 CHỈ một giá trị — KHÔNG model broad runtime exception taxonomy/observability infrastructure, deferred §15); checked_evidence_refs thường rỗng. Tường minh RETRYABLE — một OrderCreationAttemptRecorded MỚI (order_creation_attempt_id khác) tại CÙNG logical creation key sau đó là hợp lệ."
  - "Idempotency scoped theo TỪNG order_creation_attempt_id (§11 `order_creation_attempt_idempotency_policy`) — KHÔNG theo logical creation key."
  - "No-look-ahead: mọi checked_evidence_refs PHẢI thỏa fact.recorded_time ≤ order_context_cursor.recorded_time."
payload:
  order_creation_attempt_id: {type: string, required: true}
  originating_execution_intent_id: {type: string, required: true}
  order_context_cursor: {type: object, required: true, description: "cùng shape §2 — payload field"}
  attempt_outcome: {type: enum, values: [CREATED, INELIGIBLE, FAILED_BEFORE_CREATION], required: true}
  reason_code: {type: enum, values: [EXECUTION_INTENT_INELIGIBLE, ORDER_ENGINE_COMPUTATION_BOUNDARY_ERROR], required: false}
  checked_evidence_refs: {type: array, items: event_record_ref, required: false}
```

**Attempt→Order query (non-authoritative convenience, KHÔNG cần linking event mới):** cho một attempt CREATED, resolve Order tương ứng qua HAI cách tương đương — (a) `GetOrderForExecutionIntent(originating_execution_intent_id, cursor)` (§8); hoặc (b) reverse-lookup trực tiếp trên authoritative OrderCreated stream cho fact có `causation_refs` chứa chính `event_record_ref` của attempt này. Cả hai đều dùng field/cơ chế ĐÃ CÓ SẴN (`causation_refs`, logical creation key) — KHÔNG tạo event/field liên kết mới, đúng đối xứng `risk.md` §4.

## 4. `OrderCreated` — `kind: event`

Kế thừa envelope §2. Payload đặc thù:

```yaml
id: order-created
kind: event
capability_id: execution-management
domain_context_id: order-management
description: >
  Fact AUTHORITATIVE cho việc tạo MỘT Order — thiết lập TOÀN BỘ scope (originating_execution_intent_id,
  originating_risk_evaluation_id, trade_intent_id, account_id, environment, instrument_selection_ref,
  direction, order_action, order_type, quantity, quantity_unit) cùng lúc, BẤT BIẾN. CHỈ được phát khi
  OrderCreationAttemptRecorded (§3) tương ứng có attempt_outcome = CREATED (§4a).
invariants:
  - "payload.order_id PHẢI khớp đúng subject_ref.subject_id VÀ payload.originating_execution_intent_id PHẢI khớp đúng subject_ref.scope.originating_execution_intent_id."
  - "envelope.effective_time (order_effective_time) = mặc định bằng order_context_cursor.recorded_time trừ khi backfill lịch sử tường minh pin giá trị khác."
  - "causation_refs PHẢI chứa OrderCreationAttemptRecorded (§3) tương ứng, attempt_outcome = CREATED, cùng originating_execution_intent_id/order_context_cursor — chứng minh attempt đã ghi nhận CREATED TRƯỚC khi Order này được tạo. Quan hệ MỘT CHIỀU — attempt KHÔNG mang tham chiếu ngược, loại bỏ circular append-order dependency (đúng bài học §4a intro)."
  - "Nếu logical creation key (originating_execution_intent_id) ĐÃ CÓ một Order VALID (visible-valid-head, §8) tại thời điểm ghi, OrderCreated MỚI PHẢI resolve/reuse order_id đã tồn tại (payload giống hệt — §1 idempotency) HOẶC bị reject (payload khác, chưa invalidate predecessor) — TUYỆT ĐỐI KHÔNG tạo order_id thứ hai cho CÙNG key trừ khi predecessor ĐÃ invalidate VÀ correction lineage (§9) cho phép."
  - "quantity/quantity_unit/direction/account_id/instrument_selection_ref PHẢI khớp CHÍNH XÁC origin chain của originating_execution_intent_id (execution-intent.md §1) TẠI order_context_cursor — KHÔNG dùng bất kỳ latest-state Current View nào (ExecutionIntentCurrentView, RiskEvaluationCurrentView, TradeIntentCurrentView) làm input."
  - "quantity PHẢI finite, strictly positive (> 0) — KHÔNG resize/clamp/round lại approved_quantity gốc."
  - "**v0.2 (đóng C6-MAJ-01):** `supersedes_fact_ref` TUYỆT ĐỐI ABSENT cho Order gốc (KHÔNG có predecessor). BẮT BUỘC có mặt cho correction replacement, trỏ TRỰC TIẾP predecessor `OrderCreated` fact (KHÔNG trỏ `OrderFactInvalidated`, đúng convention `risk.md` §10 — phân biệt tường minh với `causation_refs`, xem invariant dưới). Khi có mặt: `payload.order_id` PHẢI KHÁC `supersedes_fact_ref`-target's `order_id`; `payload.originating_execution_intent_id` PHẢI BẰNG HỆT `supersedes_fact_ref`-target's `originating_execution_intent_id` (logical creation key bất biến xuyên chain); replacement PHẢI supersede đúng lineage head hiện tại — KHÔNG nhảy cóc qua một head trung gian (§9 invariant 5)."
  - "**v0.2 (đóng C6-MAJ-01):** khi `supersedes_fact_ref` có mặt, `causation_refs` PHẢI CỘNG THÊM chứa chính `OrderFactInvalidated` targeting predecessor (bên cạnh `OrderCreationAttemptRecorded` đã bắt buộc ở invariant trên) — predecessor PHẢI đã invalidate VÀ visible TRƯỚC khi replacement này được ghi (đối xứng `risk.md` §10 invariant 4)."
```

**§4a — Precondition: OrderCreationAttempt CREATED, đúng thứ tự.** OrderCreated CHỈ được phát SAU KHI một `OrderCreationAttemptRecorded` (§3) đã ghi nhận `attempt_outcome = CREATED` cho cùng logical creation key — VÀ `CREATED` CHỈ ghi SAU KHI bounded Order payload computation đã hoàn tất trọn vẹn:

```text
1. eligible_for_new_order_creation(originating_execution_intent_id, order_context_cursor) == true   (execution-intent.md §6a)
→ NẾU false: OrderCreationAttemptRecorded(attempt_outcome=INELIGIBLE, reason_code=EXECUTION_INTENT_INELIGIBLE) ghi — KHÔNG OrderCreated nào phát (Scenario 2, §17). Không cần chạy Order payload computation.

2. NẾU (1) thỏa: Order Engine CHẠY TRỌN VẸN bounded computation TRƯỚC — copy nguyên vẹn scope từ
   Execution Intent (originating_risk_evaluation_id/trade_intent_id/account_id/environment/
   instrument_selection_ref/direction/quantity/quantity_unit), pin order_action=OPEN_EXPOSURE,
   order_type=MARKET — toàn bộ Order payload đã xác định XONG.
   → NẾU lỗi kỹ thuật/domain boundary xảy ra TRONG lúc computation (TRƯỚC khi hoàn tất):
     OrderCreationAttemptRecorded(attempt_outcome=FAILED_BEFORE_CREATION) ghi — KHÔNG OrderCreated
     nào phát, KHÔNG CREATED attempt nào để lại (Scenario 3, §17).
   → NẾU computation hoàn tất trọn vẹn: OrderCreationAttemptRecorded(attempt_outcome=CREATED) ghi
     NGAY SAU, RỒI OrderCreated phát (causation_refs trỏ attempt vừa ghi) (Scenario 1, §17).

Thứ tự bắt buộc: computation hoàn tất → Attempt CREATED ghi → OrderCreated ghi. KHÔNG BAO GIỜ đảo
ngược, KHÔNG atomic transaction giữa ba bước (mỗi bước là một append riêng, recoverable độc lập).
```

**Recoverable append gap (đối xứng nguyên tắc "no unstated cross-stream atomicity" đã proven, risk.md §2):** khoảng trống giữa Attempt CREATED đã ghi VÀ OrderCreated chưa ghi (ví dụ crash ngay sau khi Attempt CREATED append) là một RECOVERABLE APPEND GAP — KHÔNG phải data-integrity violation. Recovery logic (Phase 1) PHẢI resolve deterministic bằng cách re-run CÙNG computation TẠI CÙNG `originating_execution_intent_id`, VÀ append OrderCreated với `causation_refs` trỏ ĐÚNG attempt CREATED đã tồn tại đó (KHÔNG tạo `order_creation_attempt_id` MỚI) (Scenario 4, §17).

```yaml
payload:
  order_id: {type: string, required: true}
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
  order_action: {type: enum, values: [OPEN_EXPOSURE], required: true}
  order_type: {type: enum, values: [MARKET], required: true}
  quantity: {type: decimal, required: true}
  quantity_unit: {type: string, required: true}
  order_context_cursor: {type: object, required: true, description: "cùng shape §2 — payload field"}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho Order gốc; BẮT BUỘC cho correction replacement — trỏ TRỰC TIẾP predecessor OrderCreated fact (KHÔNG trỏ OrderFactInvalidated) — xem invariants và §9 (v0.2, đóng C6-MAJ-01)"}
```

## 5. `OrderStatusChanged` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: order-status-changed
kind: event
capability_id: execution-management
domain_context_id: order-management
description: >
  Fact AUTHORITATIVE cho một operational status transition của Order (§1 state_machine) —
  CREATED→WITHDRAWN, CREATED→EXPIRED, SUBMISSION_REQUESTED→WITHDRAWN, SUBMISSION_REQUESTED→EXPIRED.
  Cả hai terminal CHO FORWARD TRANSITION (§1) — nhưng correctable append-only qua same-slice
  replacement, supersedes_fact_ref có mặt ngay từ v0.1.
invariants:
  - "new_status PHẢI là một transition hợp lệ theo state_machine §1 từ current_status hiện tại — current_status resolve theo fold algorithm §8 (visible-valid-head per slice, total-order effective_time ASC/recorded_time ASC/event_id ASC)."
  - "new_status = WITHDRAWN hoặc EXPIRED trên valid lineage hiện hành KHÔNG được có OrderStatusChanged forward transition tiếp theo cho cùng order_id (§1 terminal_states) — ràng buộc FORWARD LIFECYCLE, không áp dụng cho correction record."
  - "Một WITHDRAWN/EXPIRED fact ghi SAI vẫn correctable qua OrderFactInvalidated + same-slice OrderStatusChanged replacement (§7, cùng (order_id, effective_time) slice, supersedes_fact_ref trỏ đúng fact bị invalidate) — correction KHÔNG bị chặn bởi terminality. Fold algorithm (§8) PHẢI recompute current_status từ valid corrected lineage."
  - "envelope.effective_time = thời điểm status transition này thực sự có hiệu lực."
  - "Order CHỈ eligible cho submission request MỚI (§8a) khi current_status = CREATED tại effective_time liên quan — WITHDRAWN/EXPIRED CẤM submission request mới (Scenario 10, §17)."
  - "supersedes_fact_ref VẮNG MẶT cho forward transition bình thường; BẮT BUỘC cho same-slice correction replacement — khi có mặt, PHẢI trỏ đúng OrderStatusChanged bị OrderFactInvalidated target, cùng subject/effective_time (§7)."
payload:
  order_id: {type: string, required: true}
  new_status: {type: enum, values: [WITHDRAWN, EXPIRED], required: true}
  reason: {type: string, required: false}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho forward transition bình thường; BẮT BUỘC cho same-slice correction replacement — xem invariants và §7"}
```

## 6. `OrderSubmissionRequested` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: order-submission-requested
kind: event
capability_id: execution-management
domain_context_id: order-management
description: >
  Fact AUTHORITATIVE cho việc Ride yêu cầu gửi MỘT Order hợp lệ tới bounded PAPER execution
  boundary. KHÔNG chứng minh boundary đã accept, venue đã acknowledge, external order ID tồn tại,
  execution đã xảy ra, hay Fill tồn tại — thuần túy là internal handoff fact. **v0.2 (đóng
  C6-MAJ-02):** CÓ THỂ bị invalidate qua `OrderFactInvalidated` (§7) — invalidate-only, KHÔNG same-ID
  replacement (một request MỚI, khác `submission_request_id`, CÓ THỂ append sau nếu eligible, §9).
invariants:
  - "payload.submission_request_id PHẢI khớp đúng subject_ref.subject_id VÀ payload.order_id PHẢI khớp đúng subject_ref.scope.order_id."
  - "envelope.effective_time (submission_effective_time) = mặc định bằng submission_context_cursor.recorded_time trừ khi backfill lịch sử tường minh pin giá trị khác."
  - "CHỈ hợp lệ khi eligible_for_new_submission_request(order_id, submission_context_cursor) == true (§8a) TẠI thời điểm ghi — false thì reject khi append (Scenario 10/11 §17)."
  - "target_environment PHẢI = PAPER (v0.1 CHỈ PAPER, đối xứng environment trên Order §1) — KHÔNG Live routing dưới bất kỳ hình thức nào."
  - "envelope.effective_time PHẢI thỏa `effective_time >= OrderCreated.order_effective_time` — một submission request KHÔNG BAO GIỜ effective TRƯỚC Order gốc của nó."
  - "envelope.recorded_time PHẢI `> OrderCreated.recorded_time` (strict causal ordering — Scenario 14, §17)."
  - "Idempotency scoped theo `order_id` (§11 `order_submission_idempotency_policy`) — trước khi ghi, PHẢI kiểm tra order_id chưa có OrderSubmissionRequested VALID (visible, chưa invalidate) nào khác; nếu đã có VÀ payload giống hệt, đây là idempotent retry (KHÔNG ghi bản ghi mới, trả về submission_request_id đã tồn tại); nếu đã có VÀ payload khác, đây là deterministic conflict (reject, KHÔNG ghi) (Scenario 9, §17). Một request ĐÃ invalidate KHÔNG tính vào check này — KHÔNG chặn một request MỚI hợp lệ (Scenario 19, §17)."
  - "causation_refs PHẢI chứa OrderCreated (§4) tương ứng — chứng minh Order đã tồn tại VÀ hợp lệ trước khi submission request phát."
payload:
  submission_request_id: {type: string, required: true, description: "opaque, stable, gán tại event này — identity riêng cho fact này, KHÔNG phải derivation key (derivation key = order_id, §11)"}
  order_id: {type: string, required: true, ref: order}
  submission_context_cursor: {type: object, required: true, description: "cùng shape §2 — payload field"}
  target_environment: {type: enum, values: [PAPER], required: true}
```

## 7. `OrderFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2. `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: order-fact-invalidated
kind: event
capability_id: execution-management
domain_context_id: order-management
description: >
  Phủ định MỘT fact lịch sử cụ thể ĐÃ SAI của Order. Ba hành vi khác nhau theo target: (a) target
  = OrderCreated → correction lineage CHUẨN (đối xứng RiskEvaluationRecorded, risk.md §10) — replacement
  NHẬN order_id MỚI, CÙNG logical creation key (originating_execution_intent_id), replacement's
  `supersedes_fact_ref` trỏ TRỰC TIẾP predecessor OrderCreated fact (KHÔNG trỏ event này —
  `causation_refs` của replacement mới là nơi trỏ event này, §4), một visible-valid-head duy nhất;
  (b) target = OrderStatusChanged → same-slice replacement HỢP LỆ, đúng correction lineage chuẩn
  (§8), kể cả khi giá trị bị invalidate là WITHDRAWN/EXPIRED; (c) **v0.2 (đóng C6-MAJ-02)** target =
  OrderSubmissionRequested → invalidate-only, KHÔNG bắt buộc replacement — một submission request
  ghi sai chỉ cần bị loại khỏi lifecycle fold/duplicate-suppression/C7 readiness (§8), một request
  MỚI (submission_request_id khác, CÙNG order_id) CÓ THỂ append sau đó nếu `eligible_for_new_submission_request`
  (§8a) true, KHÔNG cần `supersedes_fact_ref` trên OrderSubmissionRequested (§9).
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref."
  - "invalidated_fact_ref PHẢI trỏ một OrderCreated, OrderStatusChanged, hoặc **(v0.2, đóng C6-MAJ-02)** OrderSubmissionRequested, CHƯA từng nhận invalidation khác — một fact chỉ bị invalidate đúng một lần. KHÔNG BAO GIỜ trỏ một OrderFactInvalidated khác (cấm invalidation-of-invalidation)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref (strict — invalidation KHÔNG BAO GIỜ đồng thời hay trước predecessor)."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead) — thấy fact gốc VALID (Scenario 23, §17); replay TẠI/SAU recorded_time của invalidation thấy fact đó EXCLUDED khỏi mọi fold (lifecycle/duplicate-suppression/C7 readiness) (Scenario 24, §17)."
  - "Target = OrderCreated: mong đợi (không bắt buộc ngay lập tức) một OrderCreated replacement CÙNG originating_execution_intent_id (logical creation key), order_id MỚI, replacement's supersedes_fact_ref TRỎ TRỰC TIẾP predecessor OrderCreated fact (KHÔNG trỏ event này) — xem §4/§9 cho đầy đủ mười invariant."
  - "Target = OrderStatusChanged: mong đợi (không bắt buộc ngay lập tức) một OrderStatusChanged replacement CÙNG order_id VÀ cùng effective_time slice, supersedes_fact_ref = fact bị target (KHÔNG trỏ event này) (§9)."
  - "**v0.2 (đóng C6-MAJ-02)** Target = OrderSubmissionRequested: KHÔNG mong đợi replacement bắt buộc — invalidate-only đủ cho v0.2. `eligible_for_new_submission_request` (§8a) CÓ THỂ trở lại true ngay sau invalidation (nếu mọi điều kiện khác vẫn thỏa), cho phép một `OrderSubmissionRequested` MỚI (submission_request_id KHÁC, CÙNG order_id) được append sau đó — KHÔNG cần supersedes_fact_ref trên fact mới đó (§9)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 8. `OrderCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §3–§7.

```text
Trước khi OrderCreated tồn tại cho một originating_execution_intent_id:
  → KHÔNG có OrderCurrentView row nào tồn tại
  → GetOrderForExecutionIntent trả về NOT_FOUND / ABSENT
```

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION`. Khi `PENDING_CORRECTION`, `pending_correction_class` BẮT BUỘC có mặt (đúng pattern đã proven tại `risk.md` §7):

```text
view_state = VALID              → pending_correction_class: CẤM (phải absent)
view_state = PENDING_CORRECTION → pending_correction_class: BẮT BUỘC

target = OrderCreated (invalidate, chờ same-key replacement với order_id MỚI) → pending_correction_class = AWAITING_SAME_SUBJECT_REPLACEMENT
target = OrderStatusChanged (invalidate, chờ same-slice replacement) → pending_correction_class = AWAITING_SAME_SUBJECT_REPLACEMENT

**v0.2 (đóng C6-MAJ-02):** target = OrderSubmissionRequested (invalidate) KHÔNG BAO GIỜ đưa view_state
sang PENDING_CORRECTION — invalidate-only, KHÔNG replacement bắt buộc (§7/§9); request bị invalidate
chỉ đơn giản bị loại khỏi Tầng 2 fold dưới đây, view vẫn VALID nếu Tầng 1 head hợp lệ.
```

**Fold algorithm (v0.2, hai tầng — đóng `C6-MAJ-01`/`C6-MAJ-02`, MỘT quy tắc chung, đúng pattern đã proven tại `risk.md` §7 kết hợp `execution-intent.md` §6):**

```text
Tầng 1 — xác định visible-valid-head order_id cho logical creation key (originating_execution_intent_id)
bằng EXPLICIT REPLACEMENT LINEAGE CHAIN (v0.2, đóng C6-MAJ-01 — KHÔNG chọn head chỉ bằng "newest
uninvalidated fact"):
1. Group mọi OrderCreated theo logical creation key = originating_execution_intent_id.
2. Trong một key, dựng chain TƯỜNG MINH theo supersedes_fact_ref: O1 (gốc, KHÔNG supersedes_fact_ref)
   → O2 (supersedes_fact_ref = O1, TRỰC TIẾP) → ... (cấm fork/nhảy cóc — §9 invariant 5/6, Scenario
   17, §17).
3. Với mỗi Oi trong chain, resolve OrderFactInvalidated visibility tại cursor (recorded_time <=
   cursor) target Oi.
4. Duyệt chain từ O1: dừng tại link ĐẦU TIÊN chưa bị invalidate visible tại cursor — đó là
   visible-valid-head. current_order_id = head đó.
5. NẾU link cuối cùng đã duyệt bị invalidate visible VÀ KHÔNG CÓ link kế tiếp visible → view_state
   = PENDING_CORRECTION, pending_correction_class = AWAITING_SAME_SUBJECT_REPLACEMENT, DỪNG.

Tầng 2 — với current_order_id đã xác định ở Tầng 1, fold lifecycle (v0.2, đóng C6-MAJ-02 — cộng thêm
xử lý OrderFactInvalidated targeting OrderSubmissionRequested):
6. Thu thập, cho current_order_id: mọi OrderStatusChanged (group theo (order_id, effective_time)
   slice) VÀ mọi OrderSubmissionRequested (KHÔNG slice theo effective_time — mỗi fact độc lập, §9).
7. Loại trừ bất kỳ fact nào có OrderFactInvalidated visible tại cursor C: với OrderStatusChanged,
   loại trừ slice head chưa có replacement visible (không "giữ giá trị cũ"); với
   OrderSubmissionRequested, loại trừ fact đó HOÀN TOÀN — invalidate-only, KHÔNG cần replacement
   (§7/§9) — fact bị invalidate đóng góp KHÔNG GÌ vào lifecycle, KHÔNG compensating event nào được
   emit (Scenario 18, §17).
8. Áp dụng mọi fact valid còn lại theo total-order XÁC ĐỊNH: effective_time ASC, recorded_time ASC,
   event_id ASC.
9. Lifecycle fold: state mặc định NGAY SAU OrderCreated là CREATED. Duyệt total-order ở bước 8 theo
   thứ tự — MỖI fact valid kế tiếp PHẢI được validate/áp dụng LÊN state ĐÃ FOLD từ mọi fact valid XẾP
   TRƯỚC nó trong CÙNG total-order (v0.2, đóng C6-MAJ-02 — same-effective-time transition KHÔNG được
   validate đối với một snapshot cũ, PHẢI đối với state đã fold thật sự): OrderSubmissionRequested
   valid → SUBMISSION_REQUESTED; OrderStatusChanged valid (WITHDRAWN/EXPIRED) → terminal state đó.
   `current_status` = state đạt được SAU KHI fold hết toàn bộ total-order.
```

```yaml
id: order-current-view
kind: read_model
capability_id: execution-management
domain_context_id: order-management
description: >
  Projection tiện dụng: order_id "hiện tại" + status "hiện tại" (latest-state, KHÔNG
  cursor-addressable theo mặc định) cho một originating_execution_intent_id, rebuild được từ
  §3–§7. KHÔNG authoritative — CHỈ query/UI, KHÔNG BAO GIỜ là input hợp lệ cho Order creation,
  submission request, hay C7 processing (Package 0.2-C7, chưa author), kể cả khi "trông giống"
  cùng giá trị. Downstream field PHẢI resolve qua authoritative Order event stream (`ref: order`)
  TẠI CÙNG cursor mà computation đó đang dùng (§12).
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho Order creation/submission/C7 processing hay bất kỳ computation nào khác — CHỈ query/UI."
  - "view_state PHẢI đúng theo fold algorithm §8 Tầng 1 — creation lineage head quyết định."
  - "pending_correction_class BẮT BUỘC có mặt khi view_state = PENDING_CORRECTION; CẤM có mặt khi view_state = VALID."
  - "current_status PHẢI recompute đúng theo fold algorithm §8 Tầng 2 — một WITHDRAWN/EXPIRED fact đã invalidate mà chưa có replacement visible KHÔNG được góp phần vào current_status. **v0.2 (đóng C6-MAJ-02):** một OrderSubmissionRequested đã invalidate KHÔNG được góp phần vào current_status dưới bất kỳ hình thức nào (KHÔNG compensating event, KHÔNG 'giữ giá trị cũ') — recompute trực tiếp từ mọi fact valid còn lại."
schema:
  originating_execution_intent_id: {type: string, required: true, description: "logical creation key"}
  current_order_id: {type: string, required: false, description: "order_id của visible valid head — chỉ có mặt khi view_state = VALID"}
  scope: {result: string, required: true, description: "chỉ có mặt khi view_state = VALID — toàn bộ payload head hiện hành"}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  pending_correction_class: {type: enum, values: [AWAITING_SAME_SUBJECT_REPLACEMENT], required: false}
  current_status: {type: enum, values: [CREATED, SUBMISSION_REQUESTED, WITHDRAWN, EXPIRED], required: false, description: "chỉ có mặt khi view_state = VALID"}
  last_recorded_time: timestamp
queries: [GetOrderForExecutionIntent, GetOrderById, GetOrderHistory]
```

### 8a. Submission eligibility — `eligible_for_new_submission_request` (v0.2)

**Vai trò:** một rule normative, derived, deterministic — trả lời "Order này còn đủ điều kiện cho một submission request MỚI hay không." Đánh giá TẠI cùng cursor C:

```text
eligible_for_new_submission_request(order_id, C) =
      Order là visible-valid-head cho logical creation key của nó TẠI C                          (§8 Tầng 1)
  AND Order.current_status(C) == CREATED                                                          (§8 Tầng 2 — SUBMISSION_REQUESTED/WITHDRAWN/EXPIRED đều KHÔNG eligible)
  AND eligible_for_new_order_creation(originating_execution_intent_id, C) == true                  (execution-intent.md §6a, đầy đủ NĂM điều kiện)
  AND KHÔNG có OrderSubmissionRequested VALID (visible, CHƯA invalidate) nào tồn tại cho order_id này TẠI C   (§6 idempotency)
```

Một Order `WITHDRAWN` hoặc `EXPIRED` là **ineligible** cho submission request mới (Scenario 10, §17). Khi Execution Intent gốc (hoặc origin chain xa hơn — Risk/Trade Intent/Decision) trở nên invalid, Order **vẫn giữ nguyên `current_status`** (KHÔNG tự động chuyển WITHDRAWN) nhưng trở **ineligible cho submission request mới** — điều kiện thứ ba ở trên fail (Scenario 11, §17). **v0.2 (đóng C6-MAJ-02):** một request ĐÃ invalidate KHÔNG tính vào điều kiện thứ tư — KHÔNG chặn một request MỚI hợp lệ; điều kiện thứ tư đánh giá LẠI TẠI cursor C, chỉ xét fact còn VALID (visible, chưa invalidate) tại đúng cursor đó (Scenario 19, §17).

### 8b. Future C7 boundary — `eligible_for_execution_result_processing` (v0.2, đóng `C6-MAJ-03`)

**Vai trò:** một rule derived, xác định "Order này có đủ điều kiện để Package 0.2-C7 (chưa author) xử lý một execution result trong tương lai hay không" — KHÔNG author Fill semantics, CHỈ pin readiness boundary.

```text
eligible_for_execution_result_processing(order_id, C) =
      Order là visible-valid-head cho logical creation key originating_execution_intent_id của nó TẠI C   (§8 Tầng 1)
  AND eligible_for_new_order_creation(originating_execution_intent_id, C) == true                          (execution-intent.md §6a, đầy đủ NĂM điều kiện — BAO GỒM ExecutionIntent.current_status(C) == ISSUED)
  AND ĐÚNG MỘT OrderSubmissionRequested VALID (visible, chưa invalidate) tồn tại cho order_id này TẠI C     (§6)
  AND Order.current_status(C) == SUBMISSION_REQUESTED                                                       (§8 Tầng 2 — KHÔNG chỉ "khác WITHDRAWN/EXPIRED")
```

**v0.2 (đóng `C6-MAJ-03`):** điều kiện thứ hai nay dùng TRỌN VẸN `eligible_for_new_order_creation` (execution-intent.md §6a) — bao gồm điều kiện 1 (`ExecutionIntent.current_status(C) == ISSUED`), KHÔNG CHỈ điều kiện 2–5 như trước (thiếu điều kiện 1 khiến rule bỏ sót trường hợp Execution Intent tự nó đã `WITHDRAWN`/`EXPIRED`). Điều kiện thứ tư nay pin CHÍNH XÁC `current_status == SUBMISSION_REQUESTED` (§8 Tầng 2) — SUBMISSION_REQUESTED CHỈ derive từ một `OrderSubmissionRequested` VALID hiện hữu (theo fold algorithm §8 Tầng 2 bước 9); KHÔNG còn đủ nếu chỉ "khác WITHDRAWN/EXPIRED" (trước đây cho phép sai `CREATED` — chưa từng request — cũng pass). Quy tắc đầy đủ này đảm bảo transitively: Execution Intent ISSUED, Risk Evaluation valid APPROVED head, Trade Intent valid, Decision valid, Order valid head, Submission Request valid, Order lifecycle SUBMISSION_REQUESTED (Scenario 20, §17).

**Điều này CHỈ có nghĩa** C7 (chưa author) CÓ THỂ xử lý một execution result tương lai cho Order này. Nó **KHÔNG có nghĩa**: một Fill tồn tại; execution đã thành công; quantity đã filled; venue đã accept request. Khi Execution Intent trở `WITHDRAWN`/`EXPIRED`, `eligible_for_execution_result_processing = false` — Order và submission request lịch sử VẪN historically resolvable (Scenario 15/16, §17). `order.md` KHÔNG author Order behavior nào cho C7 — C7 (chưa author) chịu trách nhiệm CONSUME rule này.

## 9. Correction lineage

Correction lineage scoped theo hai loại subject, đúng nguyên tắc đã khóa xuyên suốt `instrument.md`/`venue.md`/`account.md`/`strategy.md`/`decision.md`/`trade-intent.md`/`risk.md`/`execution-intent.md`.

**`OrderCreated` — correction lineage CHUẨN, same-key replacement với `order_id` MỚI (đối xứng `risk.md` §10 RiskEvaluationRecorded, KHÔNG đối xứng `execution-intent.md` §5 ExecutionIntentIssued invalidate-only):**

```text
O1 (OrderCreated, originating_execution_intent_id = E1, KHÔNG supersedes_fact_ref)
  → OrderFactInvalidated targeting O1
  → O2 (OrderCreated MỚI), order_id KHÁC O1, CÙNG originating_execution_intent_id = E1,
    O2.supersedes_fact_ref = O1 TRỰC TIẾP (KHÔNG trỏ OrderFactInvalidated — event đó nằm trong
    O2.causation_refs, §4), O2.causation_refs CHỨA CẢ OrderCreationAttemptRecorded(CREATED) LẪN
    OrderFactInvalidated targeting O1 → một visible-valid-head duy nhất

Correction tiếp theo:
O2 → OrderFactInvalidated targeting O2 → O3, O3.supersedes_fact_ref = O2 TRỰC TIẾP
  (KHÔNG được O3.supersedes_fact_ref = O1 — cấm nhảy cóc)
```

**Mười invariant bắt buộc (v0.2, đóng `C6-MAJ-01` — đối xứng `risk.md` §10, `decision.md` §11):**

1. Order gốc (O1, KHÔNG có predecessor) KHÔNG có `supersedes_fact_ref`.
2. Replacement (correction) BẮT BUỘC có `supersedes_fact_ref`, trỏ TRỰC TIẾP predecessor `OrderCreated` fact bị invalidate (KHÔNG trỏ `OrderFactInvalidated`).
3. Replacement PHẢI CÙNG `originating_execution_intent_id` với fact bị supersede (logical creation key bất biến xuyên chain, dù `order_id` đổi).
4. `causation_refs` của replacement PHẢI chứa chính `OrderFactInvalidated` targeting predecessor (CỘNG `OrderCreationAttemptRecorded` tương ứng, §4) — predecessor PHẢI đã invalidate VÀ visible TRƯỚC khi replacement được ghi.
5. Replacement PHẢI supersede đúng lineage head HIỆN TẠI — KHÔNG nhảy cóc qua một head trung gian (§8 Tầng 1 bước 2/4).
6. Một fact bị invalidate có **tối đa một** replacement authoritative trực tiếp — cấm fork (Scenario 17, §17: O2 KHÔNG được append khi O1 vẫn VALID, chưa invalidate).
7. Replacement không được "visible" (`recorded_time`) trước invalidation tương ứng.
8. Mọi lineage member lịch sử giữ nguyên trong log — append-only, KHÔNG mutate; `order_id` cũ (O1) vẫn resolvable mãi mãi qua `GetOrderById`.
9. Một fact đã invalidate **không bao giờ** bị tái sử dụng ngầm — `OrderCurrentView` (§8) phải loại trừ nó tường minh khỏi Tầng 1 chain traversal.
10. Retry của cùng logical creation key với payload KHÁC, KHI predecessor CHƯA invalidate, VẪN LÀ conflict (KHÔNG tự động trở thành correction) — correction CHỈ hợp lệ qua chuỗi tường minh invalidate-rồi-replace ở trên (§1 idempotency invariant).

**Prior `OrderSubmissionRequested` KHÔNG được O2 kế thừa:** submission request (nếu có) gắn O1 vẫn historical dưới O1, KHÔNG cascade-delete, KHÔNG tự động chuyển sang O2 — O1 trở ineligible cho submission request MỚI (§8a); O2 khởi đầu `current_status = CREATED` VÀ PHẢI nhận submission request RIÊNG của chính nó nếu cần (Scenario 21, §17). Replay TRƯỚC correction thấy O1 (VALID); replay SAU correction thấy O2 (VALID), O1 EXCLUDED khỏi head resolution nhưng vẫn historically resolvable (§8).

**`OrderStatusChanged` — correction lineage chuẩn, same-slice replacement (§5/§7, đối xứng `execution-intent.md` §8, mười invariant chuẩn, KHÔNG lặp lại toàn văn):**

```text
F1 (OrderStatusChanged)
  → OrderFactInvalidated targeting F1
  → replacement (cùng event type OrderStatusChanged), supersedes_fact_ref = F1 TRỰC TIẾP
```

**`OrderSubmissionRequested` — v0.2 (đóng `C6-MAJ-02`), invalidate-only, KHÔNG same-ID/same-slot replacement bắt buộc:**

```text
S1 (OrderSubmissionRequested, order_id = O)
  → OrderFactInvalidated targeting S1
  → S1 EXCLUDED khỏi lifecycle fold (§8 Tầng 2)/duplicate-suppression (§8a)/C7 readiness (§8b) TỪ
    cursor invalidation trở đi — KHÔNG compensating status event
  → eligible_for_new_submission_request(O, C) CÓ THỂ trở lại true (§8a, nếu mọi điều kiện khác
    vẫn thỏa) — CHO PHÉP một request MỚI:
S2 (OrderSubmissionRequested, submission_request_id KHÁC S1, CÙNG order_id = O)
  → KHÔNG supersedes_fact_ref trên S2 — v0.2 KHÔNG cần replacement lineage cho subject này (edge
    case hiếm hơn OrderCreated/OrderStatusChanged, invalidate-only đủ; general workflow semantics
    KHÔNG cần thêm)
```

## 10. Time semantics và bitemporal correctness

- `effective_time` — required trên mọi event trong tài liệu này.
- `recorded_time` — recorded axis, universal.
- `ExecutionIntentIssued.effective_time <= OrderCreated.order_effective_time` — Order KHÔNG BAO GIỜ effective trước Execution Intent gốc.
- `ExecutionIntentIssued.recorded_time < OrderCreated.recorded_time` — strict causal ordering.
- `OrderCreated.recorded_time < OrderSubmissionRequested.recorded_time` — strict causal ordering (§6, Scenario 14 §17).
- Mọi authoritative fact dùng cho creation PHẢI thỏa `fact.recorded_time <= order_context_cursor.recorded_time <= OrderCreated.recorded_time`.
- Mọi authoritative fact dùng cho submission readiness PHẢI visible TẠI `submission_context_cursor`.
- Replay tại cursor T chỉ thấy fact có `recorded_time ≤ T` — invalidation ghi SAU T KHÔNG visible tại T.
- `market_time` PROHIBITED xuyên suốt tài liệu này.

## 11. Canonical policy identifiers — nguồn duy nhất (context `order-management`)

**Bốn canonical policy identifier, khai báo ĐÚNG MỘT LẦN tại đây cho context `order-management`** — đúng pattern đã proven tại `risk.md` §12, khai báo ĐỘC LẬP vì đây là context khác:

```yaml
initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS
order_creation_derivation_idempotency_policy: ONE_VALID_ORDER_PER_ORIGINATING_EXECUTION_INTENT
order_creation_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT
order_submission_idempotency_policy: STABLE_ORDER_ID_SAME_PAYLOAD_IS_IDEMPOTENT
order_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE
```

**`initial_fact_correction_policy`** — áp dụng CHỈ cho `OrderCreationAttemptRecorded` (§3, KHÔNG có same-ID replacement — attempt sai thực tế deferred §15). `OrderCreated` KHÔNG dùng policy này thuần túy — xem `order_correction_lineage_policy` dưới.

**`order_creation_derivation_idempotency_policy: ONE_VALID_ORDER_PER_ORIGINATING_EXECUTION_INTENT`** — logical creation key = `originating_execution_intent_id`; retry cùng key + cùng payload (chưa invalidate) → idempotent no-op, trả về `order_id` đã tồn tại; retry cùng key + payload KHÁC (chưa invalidate predecessor) → deterministic conflict, reject (§1, §9). **KHÔNG unstated cross-stream atomicity** — Execution Intent và Order là hai authoritative stream RIÊNG, KHÔNG có transaction ngầm định đảm bảo cả hai append cùng lúc.

**`order_creation_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT`** — idempotency scoped theo TỪNG `order_creation_attempt_id` cá nhân, KHÔNG theo logical creation key: retry CÙNG `order_creation_attempt_id` + CÙNG payload → idempotent no-op; CÙNG `order_creation_attempt_id` + payload KHÁC → deterministic conflict. Logical creation key KHÔNG BẮT BUỘC unique — nhiều attempt (kể cả outcome khác nhau) CÓ THỂ tồn tại cùng key.

**`order_submission_idempotency_policy: STABLE_ORDER_ID_SAME_PAYLOAD_IS_IDEMPOTENT`** — derivation/idempotency key cho `OrderSubmissionRequested` là `order_id` (§6), KHÔNG một `submission_request_id`-scoped identity riêng (task không yêu cầu individual submission-attempt identity cho walking skeleton v0.1) — same `order_id` + same submission payload → idempotent no-op/reuse `submission_request_id` đã tồn tại; same `order_id` + changed payload → deterministic conflict, reject (Scenario 9, §17). Missing submission request sau Order creation là recoverable gap — KHÔNG data-integrity violation.

**`order_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE`** — correction `OrderCreated` KHÔNG same-ID replacement (`order_id` vẫn bất biến/không tái sử dụng per-fact), NHƯNG logical creation key CÓ THỂ nhận `OrderCreated` MỚI (`order_id` khác) sau khi predecessor invalidate — xem §9 cho đầy đủ.

## 12. Downstream reference contract (cho Package 0.2-C7 — Fill/Position, chưa author)

Package sau (Fill/Position, Package 0.2-C7, chưa author) tham chiếu Order qua ĐÚNG các field sau, KHÔNG hơn:

```yaml
order_id: {type: string, required: true, ref: order}
originating_execution_intent_id: {type: string, description: "= §1, ref: execution-intent"}
originating_risk_evaluation_id: {type: string, description: "= §1, ref: risk"}
trade_intent_id: {type: string, description: "= §1, ref: trade-intent"}
account_id: {type: string, ref: account, description: "= §1"}
environment: {type: enum, values: [PAPER], description: "= §1"}
instrument_selection_ref: {type: object, description: "= §1 — {instrument_id, venue_id, listing_id}"}
direction: {type: enum, values: [LONG, SHORT], description: "= §1"}
order_action: {type: enum, values: [OPEN_EXPOSURE], description: "= §1"}
order_type: {type: enum, values: [MARKET], description: "= §1"}
quantity: {type: decimal, description: "= §1 — GUARANTEE: LUÔN strictly positive (> 0), CHÍNH XÁC bằng Risk-approved quantity gốc"}
quantity_unit: {type: string, description: "= §1"}
current_status: {type: enum, values: [CREATED, SUBMISSION_REQUESTED, WITHDRAWN, EXPIRED], description: "PHẢI resolve từ authoritative event stream TẠI cursor, KHÔNG OrderCurrentView latest-state"}
eligible_for_execution_result_processing: {type: boolean, description: "derived, xem §8b — C7 PHẢI kiểm tra rule này TRƯỚC khi xử lý execution result, KHÔNG chỉ dựa current_status"}
```

**Downstream authority rule — MỘT quy tắc duy nhất, không ngoại lệ:** downstream package PHẢI resolve mọi field trên TRỰC TIẾP từ authoritative Order event stream (§3–§7) TẠI ĐÚNG cursor mà chính computation đó đang dùng. `OrderCurrentView` latest-state (§8) KHÔNG BAO GIỜ được dùng làm input. C7 (chưa author) PHẢI áp dụng `eligible_for_execution_result_processing` (§8b) TRƯỚC khi xử lý bất kỳ execution result nào. `order.md` KHÔNG author semantics của Fill/Position (Package 0.2-C7, chưa author).

## 13. Explanation contract

**Explanation là derived, non-authoritative rendering — KHÔNG UI copy, KHÔNG natural-language generation infrastructure.** Structured facts (§1/§3–§6) là authoritative; text rendering CHỈ là một hàm thuần túy của evidence đã có.

```text
Explanation(order_id) = deterministic render của {originating Execution Intent scope, eligibility
result, Order scope, creation attempt, submission state} — KHÔNG computation mới, KHÔNG external
lookup, KHÔNG dùng bất kỳ giá trị nào không có mặt trong §1/§3–§6.
```

**Invariant:** hai Order với cùng scope PHẢI cho cùng explanation render (deterministic). Explanation KHÔNG có event/subject riêng — một PROJECTION thuần túy của OrderCreated + OrderStatusChanged + OrderSubmissionRequested.

## 14. Prohibitions

**Order/OrderCreationAttempt/OrderSubmissionRequest KHÔNG được sở hữu:** Execution Intent/RiskEvaluation/Trade Intent/Decision identity semantics; Fill/Position/Replay Event semantics (Package 0.2-C7, chưa author); partial fill/venue acceptance/rejection/external order ID/exchange API payload/order routing/exchange adapter behavior; Limit/Stop/advanced order type; TIF/IOC/FOK/post_only/reduce_only; fees/slippage/accounting; margin/leverage/liquidation model; general workflow/saga engine; broad runtime exception telemetry/observability infrastructure; UI copy/natural-language generation infrastructure; database transaction/outbox/message-broker technology.

## 15. Ngoài phạm vi — defer

- Stream Registry/Input Contract implementation cụ thể — `order_context_cursor`/`submission_context_cursor` field SHAPE pin ngay v0.1, MECHANISM resolve deferred Phase 1.
- Chính sách hết hạn cụ thể (`EXPIRED` trigger timing/mechanism) — Phase 1.
- Lý do `WITHDRAWN` cụ thể — Phase 1 concern, deferred.
- Reference price cho deterministic PAPER simulation evidence — v0.1 CHỦ ĐỘNG OMIT (task cho phép pin CHỈ khi "strictly necessary"; walking skeleton v0.1 KHÔNG cần vì Order KHÔNG tự tính toán gì — quantity copy nguyên vẹn, không có sizing computation nào cần một reference price để deterministic) — nếu Phase 1 cần một PAPER simulation evidence cụ thể, thêm qua correction riêng, KHÔNG retrofit ở đây.
- Granular exception/technical-failure sub-taxonomy cho `FAILED_BEFORE_CREATION` — v0.1 CHỈ một reason_code.
- Individual submission-attempt identity riêng (tách biệt `submission_request_id` khỏi `order_id` derivation key) — v0.1 KHÔNG cần, `order_id` đủ làm derivation key cho walking skeleton.
- Correction lineage riêng cho `OrderCreationAttempt`/`OrderSubmissionRequested` — edge case hiếm, append-only đủ cho v0.1.
- Implementation technology cho Execution Intent→Order và Order→Submission recovery (retry queue/outbox/message-broker) — boundary semantic pin, KHÔNG chọn công nghệ.
- Runtime worker ownership, transaction boundaries, retry/backoff, monitoring/escalation (Phase 1, cùng nguyên tắc defer đã áp dụng xuyên suốt Package 0.2).
- Fill/Position semantics — hoàn toàn ngoài phạm vi Domain Contract này (Package 0.2-C7).

## 16. Open questions ngoài phạm vi

- Cơ chế cụ thể generate `order_id`/`order_creation_attempt_id`/`submission_request_id` — chưa quyết, Phase 1.
- Retention/resolvability horizon cụ thể cho Order/OrderCreationAttempt/OrderSubmissionRequest đã lâu.
- Không đóng OQ-002/OQ-003.

## 17. Acceptance scenarios (v0.2: hai mươi bốn scenario — mười một kế thừa v0.1 + ba mở rộng đóng `C6-MAJ-01`/`C6-MAJ-02`/`C6-MAJ-03` + mười bổ sung — validation, không phải executable test tại C6)

**Scenario 1 — Eligible Order creation:** Execution Intent ISSUED, `eligible_for_new_order_creation=true`, PAPER, `OPEN_EXPOSURE`, `quantity>0` → Order payload computation hoàn tất → Attempt CREATED ghi → một `OrderCreated`.

**Scenario 2 — Ineligible Execution Intent:** `eligible_for_new_order_creation=false` → `OrderCreationAttemptRecorded(attempt_outcome=INELIGIBLE, reason_code=EXECUTION_INTENT_INELIGIBLE)` — KHÔNG `OrderCreated`.

**Scenario 3 — Failure and retry:** Attempt A1 (`FAILED_BEFORE_CREATION`) ghi; Attempt A2 (CÙNG `originating_execution_intent_id`, `CREATED`) ghi sau đó — HỢP LỆ, KHÔNG mâu thuẫn với A1.

**Scenario 4 — Crash after successful Attempt:** Order payload computed → Attempt CREATED appended → crash TRƯỚC `OrderCreated` → recovery: re-run CÙNG computation, tái sử dụng attempt CREATED đã tồn tại (KHÔNG tạo attempt mới), append/reuse ĐÚNG MỘT `OrderCreated`.

**Scenario 5 — Creation idempotency:** cùng Execution Intent + cùng payload → cùng `order_id`, KHÔNG duplicate; cùng Execution Intent + payload KHÁC (chưa invalidate predecessor) → deterministic conflict.

**Scenario 6 — Scope mismatch:** reject bất kỳ Order nào thay đổi `direction`/`account_id`/`instrument_selection_ref`/`quantity`/`quantity_unit`/origin IDs so với Execution Intent gốc.

**Scenario 7 — Zero quantity:** `quantity <= 0` → invalid Order — KHÔNG Order nào được tạo (giá trị này KHÔNG BAO GIỜ xảy ra hợp lệ vì Execution Intent gốc đã pin `approved_quantity > 0`, execution-intent.md §1 — pin tường minh làm safety invariant).

**Scenario 8 — Submission request:** một `OrderCreated` VALID → `OrderSubmissionRequested` → lifecycle chuyển `SUBMISSION_REQUESTED` — KHÔNG ngụ ý acknowledgement hay execution.

**Scenario 9 — Duplicate submission request:** cùng Order + cùng request payload → idempotent; cùng Order + payload KHÁC → deterministic conflict.

**Scenario 10 — Withdrawn or expired Order:** `current_status ∈ {WITHDRAWN, EXPIRED}` → KHÔNG submission request mới (`eligible_for_new_submission_request=false`) → KHÔNG eligible cho future C7 execution-result processing.

**Scenario 11 — Origin invalidated:** Execution Intent trở nên ineligible, hoặc origin chain xa hơn (Risk/Trade Intent/Decision) trở nên invalid → Order vẫn historical, KHÔNG submission request mới, KHÔNG eligible cho C7 processing tương lai.

**Scenario 12 — Initial Order (v0.2, đóng `C6-MAJ-01`):** O1 tạo → `O1.supersedes_fact_ref` TUYỆT ĐỐI ABSENT (Order gốc, KHÔNG predecessor).

**Scenario 13 — Corrected Order (v0.2, đóng `C6-MAJ-01`, mở rộng scenario correction cũ):** O1 → invalidate O1 → O2 `order_id` MỚI, CÙNG `originating_execution_intent_id`, `O2.supersedes_fact_ref` TRỰC TIẾP trỏ O1 (KHÔNG trỏ `OrderFactInvalidated`), `O2.causation_refs` chứa CẢ `OrderCreationAttemptRecorded(CREATED)` LẪN `OrderFactInvalidated` targeting O1 → một visible-valid-head. Replay TRƯỚC correction thấy O1; replay SAU correction thấy O2.

**Scenario 14 — Time ordering:** reject `OrderCreated.recorded_time <= ExecutionIntentIssued.recorded_time`; reject `OrderSubmissionRequested.recorded_time <= OrderCreated.recorded_time`.

**Scenario 15 — Execution Intent withdrawn (v0.2, đóng `C6-MAJ-03`):** Order valid, Submission Request valid, Execution Intent `WITHDRAWN` → `eligible_for_new_order_creation` điều kiện 1 fail → `eligible_for_execution_result_processing=false`. Order/request lịch sử vẫn resolvable.

**Scenario 16 — Execution Intent expired (v0.2, đóng `C6-MAJ-03`):** đồng dạng Scenario 15, Execution Intent `EXPIRED` thay vì `WITHDRAWN` → `eligible_for_execution_result_processing=false`.

**Scenario 17 — Direct fork rejected (v0.2, đóng `C6-MAJ-01`):** O1 VALID (chưa invalidate) → thử append O2 CÙNG logical creation key MÀ KHÔNG có `OrderFactInvalidated` visible targeting O1 → reject (§9 invariant 6, cấm fork).

**Scenario 18 — False submission request correction (v0.2, đóng `C6-MAJ-02`):** O1 CREATED → S1 (`OrderSubmissionRequested`) → lifecycle `SUBMISSION_REQUESTED` → invalidate S1 → S1 historical, KHÔNG còn valid, lifecycle RECOMPUTE trực tiếp từ history còn lại → `CREATED` (KHÔNG compensating `CREATED` status event nào được emit — §8 Tầng 2 bước 7).

**Scenario 19 — Reissue after invalidation (v0.2, đóng `C6-MAJ-02`):** tiếp Scenario 18 — `eligible_for_new_submission_request` trở lại true → S2 (`submission_request_id` KHÁC S1, CÙNG `order_id`) append hợp lệ → lifecycle `SUBMISSION_REQUESTED` trở lại.

**Scenario 20 — Complete valid chain (v0.2, đóng `C6-MAJ-03`, thay thế C7-boundary scenario cũ):** Execution Intent ISSUED, origin chain (Risk Evaluation APPROVED head/Trade Intent/Decision) valid, Order visible-valid-head, ĐÚNG MỘT Submission Request valid, `current_status == SUBMISSION_REQUESTED` → `eligible_for_execution_result_processing=true`. KHÔNG Fill nào được author ở đây.

**Scenario 21 — Order replacement does not inherit submission (v0.2, đóng `C6-MAJ-01`, mở rộng scenario cũ):** O1 + S1 (`SUBMISSION_REQUESTED`) → invalidate O1 → O2 replacement → S1 vẫn historical DƯỚI O1 (KHÔNG cascade/inherit sang O2) → O2 khởi đầu `current_status = CREATED` → O2 PHẢI nhận submission request RIÊNG của chính nó nếu cần.

**Scenario 22 — Invalidated request and C7 (v0.2, đóng `C6-MAJ-02`/`C6-MAJ-03`):** S1 (`OrderSubmissionRequested`, VALID trước đó) bị invalidate → `current_status` recompute (§8 Tầng 2) KHÔNG còn `SUBMISSION_REQUESTED` → `eligible_for_execution_result_processing=false` (điều kiện thứ tư §8b fail).

**Scenario 23 — Replay before request invalidation (v0.2, đóng `C6-MAJ-02`):** cursor TRƯỚC `recorded_time` của `OrderFactInvalidated` targeting S1 → S1 visible VÀ valid → `current_status = SUBMISSION_REQUESTED`.

**Scenario 24 — Replay after request invalidation (v0.2, đóng `C6-MAJ-02`):** cursor TẠI/SAU `recorded_time` của invalidation → S1 EXCLUDED khỏi lifecycle fold/duplicate-suppression/C7 readiness → `current_status` recompute (Scenario 18) → C7 readiness false (Scenario 22).
