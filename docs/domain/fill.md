---
id: fill
title: Fill
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

# Fill

> **Vai trò của tài liệu này:** Domain Contract thứ hai của Package 0.2-C7 (Execution Result, Fill, Position and Replay Integration Foundation) — định nghĩa **Fill**, bản ghi authoritative, bất biến, của quantity/price đã thực sự executed cho một [`execution-result.md`](./execution-result.md) `result_type = EXECUTED`. Draft, chưa Approved/Locked. Thuộc capability `execution-management` / context `fill-management` (đăng ký MỚI tại [`context-map.yaml`](./context-map.yaml)). Kiến trúc controlling: [`execution-result.md`](./execution-result.md) v0.1 Draft §4 (ExecutionResult, KHÔNG sửa), [`order.md`](./order.md) v0.2 Draft (origin chain, KHÔNG sửa), [Chapter 8 §8.1.1/§8.2/§8.5](../constitution/08-event-model.md) (Locked, Referenced Authoritative Artifact + canonical Replay Cursor — TÁI SỬ DỤNG nguyên vẹn). Tài liệu này CHỈ implement field/invariant mà các nguồn trên yêu cầu, KHÔNG tự quyết architecture mới ngoài phạm vi đã khóa.

Fill **KHÔNG phải** một ExecutionResult (`execution-result.md`, file riêng — ExecutionResult CHỈ tuyên bố executed/not-executed, KHÔNG mang exact quantity/price), một Position (`position.md`, file riêng — Position là PROJECTION dẫn xuất từ Fill history, KHÔNG phải authoritative fact độc lập), venue acknowledgement, hay bằng chứng price-guarantee/limit price. Nó là **bản ghi authoritative, bất biến, tự-giải-thích được** của quantity/price ĐÃ THỰC SỰ executed — trả lời chính xác năm câu hỏi: ExecutionResult nào sản sinh Fill này? Quantity/price chính xác đã executed là gì? Origin chain có được bảo toàn không? Fill có bất biến, tránh trùng lặp cho cùng ExecutionResult không? Replay trước/sau correction thấy gì?

**Ví dụ walking-skeleton (tiếp `execution-result.md`):** một ExecutionResult `EXECUTED` → đúng một full Fill, `fill_quantity == Order.quantity` (v0.1: **executed result sản sinh CHÍNH XÁC một full Fill — KHÔNG partial-fill semantics**, disclosed judgment call theo yêu cầu task, xem §12). Hai mươi bốn Scenario chấp nhận toàn Package 0.2-C7 (1–24) — phần liên quan trực tiếp Fill liệt kê tại §13.

**`fill-recorded`/`fill-fact-invalidated`/`fill-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/C1–C7 (`execution-result.md`):** opaque identity không derive từ scope; direct-predecessor-fact-targeting cho `supersedes_fact_ref`; fold algorithm "visible-valid-head per logical key" cho Current View; Current View KHÔNG BAO GIỜ authority; canonical policy identifier khai báo ĐÚNG MỘT NƠI. **Fill KHÔNG có processing Attempt riêng** — derivation từ `ExecutionResultRecorded(EXECUTED)` là deterministic trực tiếp (KHÔNG cần một Attempt subject bổ sung, task không yêu cầu; recoverable append gap vẫn pin tường minh, §5).

**Phạm vi bounded tường minh:** KHÔNG author Position semantics (`position.md`, file riêng). KHÔNG partial fill — v0.1 CHỈ full Fill. KHÔNG slippage/price-guarantee semantics — `fill_price` LÀ giá PAPER execution quan sát được, KHÔNG phải limit price hay reference price trước đó. KHÔNG fee/commission/funding. KHÔNG FX conversion — `price_currency` PHẢI CHÍNH XÁC bằng TradableListing quote currency. KHÔNG Live behavior. KHÔNG redefine ExecutionResult/Order contract — mọi evidence tham chiếu qua `ref:` trực tiếp. KHÔNG sửa `execution-result.md`/`order.md`/`execution-intent.md`/`risk.md`/`decision.md`/`trade-intent.md`/C1–C6/ADR/Constitution.

## 1. Fill — `kind: entity`

```yaml
id: fill
kind: entity
capability_id: execution-management
domain_context_id: fill-management
description: >
  Bản ghi authoritative, bất biến, của quantity/price ĐÃ THỰC SỰ executed cho MỘT ExecutionResult
  result_type = EXECUTED. Scope hoàn toàn bất biến sau khi tạo — KHÔNG "mutable metadata" tách
  biệt. KHÔNG lifecycle riêng — một Fill VALID vĩnh viễn giữ nguyên payload cho tới khi
  invalidate/replace qua correction lineage (§4).
invariants:
  - "fill_id là opaque, globally unique, gán tại FillRecorded — KHÔNG derive từ execution_result_id hay bất kỳ field scope nào. Bất biến, KHÔNG tái sử dụng cho subject khác (Chapter 6 §6.1)."
  - "MỘT Fill originate từ ĐÚNG MỘT ExecutionResult (execution_result_id, ref: execution-result), result_type = EXECUTED — logical Fill key = execution_result_id, tại một cursor cho trước tối đa MỘT Fill VALID (visible-valid-head) cho mỗi execution_result_id (§7 `fill_derivation_idempotency_policy: ONE_VALID_FILL_PER_EXECUTION_RESULT`)."
  - "order_id/submission_request_id/originating_execution_intent_id/originating_risk_evaluation_id/trade_intent_id/account_id/environment/instrument_selection_ref/direction PHẢI BẰNG HỆT origin chain tương ứng của execution_result_id (execution-result.md §4) — Fill KHÔNG được tự chọn Account/instrument/direction khác ExecutionResult gốc đã pin (Scenario 9, §13)."
  - "fill_quantity PHẢI finite, STRICTLY POSITIVE (> 0), VÀ CHÍNH XÁC BẰNG Order.quantity (order.md §1) — v0.1 executed result sản sinh CHÍNH XÁC một full Fill, KHÔNG partial-fill semantics (§12, disclosed bounded rule). quantity_unit PHẢI CHÍNH XÁC BẰNG Order.quantity_unit."
  - "fill_price PHẢI finite, STRICTLY POSITIVE (> 0) — giá PAPER execution quan sát được, KHÔNG phải limit price/reference price trước đó, KHÔNG slippage/price-guarantee model."
  - "price_currency PHẢI CHÍNH XÁC BẰNG TradableListing quote currency (resolve từ instrument_selection_ref, instrument.md — KHÔNG redefine tại đây) — KHÔNG FX conversion."
  - "environment PHẢI = PAPER (v0.1 CHỈ PAPER, copied từ origin chain)."
  - "Fill KHÔNG BAO GIỜ mutate ExecutionResult scope — mọi field origin chỉ COPY từ ExecutionResult gốc để tiện truy vấn, KHÔNG phải nguồn authoritative thứ hai."
schema:
  fill_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  execution_result_id: {type: string, required: true, ref: execution-result, description: "đúng một ExecutionResult, result_type = EXECUTED — logical Fill key"}
  order_id: {type: string, required: true, ref: order}
  submission_request_id: {type: string, required: true}
  originating_execution_intent_id: {type: string, required: true, ref: execution-intent}
  originating_risk_evaluation_id: {type: string, required: true, ref: risk}
  trade_intent_id: {type: string, required: true, ref: trade-intent}
  account_id: {type: string, required: true, ref: account}
  environment: {type: enum, values: [PAPER], required: true}
  instrument_selection_ref:
    type: object
    required: true
    fields:
      instrument_id: {type: string, required: true}
      venue_id: {type: string, required: true}
      listing_id: {type: string, required: true}
  direction: {type: enum, values: [LONG, SHORT], required: true}
  fill_quantity: {type: decimal, required: true, description: "finite, STRICTLY POSITIVE, CHÍNH XÁC BẰNG Order.quantity — v0.1 full Fill duy nhất"}
  quantity_unit: {type: string, required: true}
  fill_price: {type: decimal, required: true, description: "finite, STRICTLY POSITIVE — giá PAPER execution quan sát được"}
  price_currency: {type: string, required: true, description: "CHÍNH XÁC BẰNG TradableListing quote currency"}
  fill_context_cursor: {type: object, required: true, description: "Replay Cursor hợp lệ, TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1 — xem §2"}
  fill_effective_time: {type: timestamp, required: true, description: "effective-axis value — xem §3"}
events_emitted: [FillRecorded, FillFactInvalidated]
events_consumed: []
commands: []
queries: []
```

## 2. Canonical event envelope — áp dụng cho mọi Fill event (§3–§4)

Mọi event trong tài liệu này là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). Fill dùng `effective_time` tiêu chuẩn (semantic: `fill_effective_time`) VÀ `fill_context_cursor` như **PAYLOAD field**, TÁI SỬ DỤNG nguyên vẹn shape Replay Cursor Chapter 8 §8.5.1.

```yaml
envelope:
  event_id: {cardinality: required}
  event_type: {cardinality: required}
  event_contract_ref: {cardinality: required}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}
  subject_ref: {cardinality: "required — shape canonical, xem dưới. Trên FillFactInvalidated, PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate."}
  stream_ref: {cardinality: required}                # Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # Phase 1, chưa author
  correlation_id: {cardinality: "required — luôn thuộc correlation flow tường minh (originating ExecutionResultRecorded)"}
  causation_refs: {cardinality: "FillRecorded: KHÔNG BAO GIỜ rỗng — PHẢI chứa ExecutionResultRecorded (EXECUTED) tương ứng (execution-result.md §4), CỘNG FillFactInvalidated của predecessor nếu là correction replacement (§4). FillFactInvalidated: KHÔNG BAO GIỜ rỗng."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3."}
  effective_time: {cardinality: "required — semantic = fill_effective_time trên FillRecorded (§3)."}
  decision_time: {cardinality: "PROHIBITED."}
  decision_context_cursor: {cardinality: "PROHIBITED (envelope-level) — fill_context_cursor sống ở PAYLOAD."}
  market_time: {cardinality: "PROHIBITED — Fill là bounded PAPER boundary observation authoritative, KHÔNG quan sát trực tiếp venue thật."}
  source_identity: {cardinality: "PROHIBITED — luôn phát sinh nội bộ, KHÔNG BAO GIỜ từ external feed."}

fill_context_cursor (shape, đúng canonical Replay Cursor — Chapter 8 §8.5.1):
  recorded_time: <timestamp>
  input_contract_ref: {contract_id: <string>, contract_version: <string>}
  stream_registry_version: <string>
  lifecycle_frontier: {stream_id: <string>, position: {kind: <genesis | event>, sequence: <integer>}}
  stream_positions: {<stream_id>: <sequence>, ...}

subject_ref (Fill):
  context_id: fill-management
  subject_kind: entity
  subject_type: Fill
  subject_id: <fill_id — opaque, stable, xem §1>
  scope:
    execution_result_id: <string>

event_types:
  FillRecorded: FILL_RECORDED
  FillFactInvalidated: FILL_FACT_INVALIDATED
```

**Relational invariants bắt buộc trên `fill_context_cursor`** (Chapter 8 §8.5.2):
```text
fill_context_cursor.recorded_time ≤ FillRecorded.recorded_time
fact.recorded_time ≤ fill_context_cursor.recorded_time (mọi authoritative fact dùng cho Fill payload)
```

## 3. `FillRecorded` — `kind: event`

Kế thừa envelope §2. Payload đặc thù:

```yaml
id: fill-recorded
kind: event
capability_id: execution-management
domain_context_id: fill-management
description: >
  Fact AUTHORITATIVE cho MỘT Fill — thiết lập TOÀN BỘ scope (execution_result_id, origin chain,
  fill_quantity, quantity_unit, fill_price, price_currency) cùng lúc, BẤT BIẾN. CHỈ được phát khi
  ExecutionResultRecorded (execution-result.md §4) tương ứng có result_type = EXECUTED (§3a).
invariants:
  - "payload.fill_id PHẢI khớp đúng subject_ref.subject_id VÀ payload.execution_result_id PHẢI khớp đúng subject_ref.scope.execution_result_id."
  - "envelope.effective_time (fill_effective_time) = mặc định bằng fill_context_cursor.recorded_time trừ khi backfill lịch sử tường minh pin giá trị khác."
  - "causation_refs PHẢI chứa ExecutionResultRecorded tương ứng (execution-result.md §4), result_type = EXECUTED, cùng execution_result_id — chứng minh ExecutionResult đã tồn tại VÀ EXECUTED trước khi Fill phát."
  - "Logical Fill key = execution_result_id. Nếu key ĐÃ CÓ một Fill VALID (visible-valid-head, §5) tại thời điểm ghi, FillRecorded MỚI PHẢI resolve/reuse fill_id đã tồn tại (payload giống hệt — §1 idempotency) HOẶC bị reject (payload khác, chưa invalidate predecessor) — TUYỆT ĐỐI KHÔNG tạo fill_id thứ hai cho CÙNG key trừ khi predecessor ĐÃ invalidate."
  - "Mọi field origin (order_id/submission_request_id/originating_execution_intent_id/originating_risk_evaluation_id/trade_intent_id/account_id/environment/instrument_selection_ref/direction) PHẢI khớp CHÍNH XÁC ExecutionResult tương ứng (execution-result.md §4) TẠI fill_context_cursor — KHÔNG dùng bất kỳ latest-state Current View nào làm input."
  - "reject khi: fill_quantity <= 0; fill_price <= 0; fill_quantity != Order.quantity; quantity_unit mismatch; price_currency mismatch; environment != PAPER; origin IDs mismatch; execution_result.result_type != EXECUTED; execution_result_id không phải visible-valid-head (execution-result.md §6); submission request không hợp lệ (đã invalidate); Order không hợp lệ (đã invalidate/WITHDRAWN/EXPIRED)."
  - "`supersedes_fact_ref` TUYỆT ĐỐI ABSENT cho Fill gốc (KHÔNG predecessor). BẮT BUỘC có mặt cho correction replacement, trỏ TRỰC TIẾP predecessor FillRecorded fact (KHÔNG trỏ FillFactInvalidated). Khi có mặt: `payload.fill_id` PHẢI KHÁC predecessor; `payload.execution_result_id` PHẢI BẰNG HỆT predecessor (logical Fill key bất biến); replacement PHẢI supersede đúng lineage head HIỆN TẠI."
  - "Khi `supersedes_fact_ref` có mặt, `causation_refs` PHẢI CỘNG THÊM chứa chính FillFactInvalidated targeting predecessor — predecessor PHẢI đã invalidate VÀ visible TRƯỚC khi replacement này được ghi."
```

**§3a — Precondition và Result→Fill ordering.** FillRecorded CHỈ được phát SAU KHI ExecutionResultRecorded (EXECUTED) tồn tại VÀ hợp lệ:

```text
1. ExecutionResultRecorded(result_type=EXECUTED) đã tồn tại, visible-valid-head (execution-result.md §6)
   tại execution_result_id tương ứng.
2. Fill Engine CHẠY TRỌN VẸN bounded computation — copy nguyên vẹn origin chain từ ExecutionResult,
   xác định fill_quantity = Order.quantity (v0.1 full Fill), fill_price quan sát được từ bounded
   PAPER simulation (cơ chế cụ thể deferred Phase 1, §11) — toàn bộ Fill payload đã xác định XONG.
3. FillRecorded phát (causation_refs trỏ ExecutionResultRecorded tương ứng).

Thứ tự bắt buộc toàn chuỗi: execution result payload computed → successful processing Attempt
recorded (execution-result.md §3/§4a) → ExecutionResultRecorded → Fill payload computed →
FillRecorded. KHÔNG BAO GIỜ đảo ngược, KHÔNG atomic transaction giữa ExecutionResultRecorded và
FillRecorded.
```

**Recoverable append gap (Result→Fill):** `ExecutionResultRecorded(EXECUTED)` đã ghi, NHƯNG crash TRƯỚC khi `FillRecorded` kịp append là một RECOVERABLE APPEND GAP — KHÔNG data-integrity violation. Recovery logic (Phase 1) PHẢI: tái sử dụng CHÍNH `execution_result_id` đó; regenerate CÙNG deterministic Fill payload; append/reuse ĐÚNG MỘT Fill — TUYỆT ĐỐI KHÔNG tạo Fill trùng lặp (Scenario 7, §13).

```yaml
payload:
  fill_id: {type: string, required: true}
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
  fill_quantity: {type: decimal, required: true}
  quantity_unit: {type: string, required: true}
  fill_price: {type: decimal, required: true}
  price_currency: {type: string, required: true}
  fill_context_cursor: {type: object, required: true, description: "cùng shape §2 — payload field"}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho Fill gốc; BẮT BUỘC cho correction replacement — trỏ TRỰC TIẾP predecessor FillRecorded fact"}
```

## 4. `FillFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2. `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: fill-fact-invalidated
kind: event
capability_id: execution-management
domain_context_id: fill-management
description: >
  Phủ định MỘT `FillRecorded` lịch sử ĐÃ SAI. Correction lineage CHUẨN (đối xứng `risk.md`
  §10/`order.md` §9/`execution-result.md` §7) — replacement NHẬN fill_id MỚI, CÙNG logical Fill key
  (execution_result_id), replacement's `supersedes_fact_ref` trỏ TRỰC TIẾP predecessor FillRecorded
  (KHÔNG trỏ event này). **CẶP BẮT BUỘC với ExecutionResult correction (execution-result.md §7):**
  nếu ExecutionResult gốc chuyển visible-valid-head sang một fact `result_type != EXECUTED` (hoặc bị
  invalidate không thay thế), MỌI Fill visible-valid tham chiếu `execution_result_id` cũ PHẢI được
  invalidate qua event này — KHÔNG được để một Fill visible-valid tồn tại dưới một ExecutionResult
  không còn EXECUTED visible-valid-head (Scenario 17, §13).
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref."
  - "invalidated_fact_ref PHẢI trỏ một FillRecorded, CHƯA từng nhận invalidation khác — một fact chỉ bị invalidate đúng một lần. KHÔNG BAO GIỜ trỏ một FillFactInvalidated khác (cấm invalidation-of-invalidation)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead) — thấy predecessor VALID (Scenario 21, §13); replay TẠI/SAU thấy predecessor EXCLUDED khỏi head resolution, Position (position.md) recompute không có Fill đó (Scenario 22, §13)."
  - "Mong đợi (không bắt buộc ngay lập tức, TRỪ khi bắt buộc bởi execution-result.md §7 coupling rule) một FillRecorded replacement CÙNG execution_result_id, fill_id MỚI, supersedes_fact_ref TRỎ TRỰC TIẾP predecessor (§3, Scenario 12/23, §13)."
  - "NẾU ExecutionResult gốc không còn visible-valid EXECUTED (execution-result.md §7), invalidation này KHÔNG có replacement — Fill history kết thúc tại invalidate, Position (position.md) recompute FLAT cho key liên quan trừ khi Fill khác đóng góp."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 5. `FillCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §3–§4.

```text
Trước khi FillRecorded tồn tại cho một execution_result_id:
  → KHÔNG có FillCurrentView row nào tồn tại
  → GetFillForExecutionResult trả về NOT_FOUND / ABSENT
```

**Fold algorithm (đúng pattern explicit-chain đã proven tại `order.md` §8 Tầng 1/`execution-result.md` §6):**

```text
1. Group mọi FillRecorded theo logical Fill key = execution_result_id.
2. Trong một key, dựng chain TƯỜNG MINH theo supersedes_fact_ref: F1 (gốc) → F2 (supersedes_fact_ref
   = F1, TRỰC TIẾP) → ... (cấm fork/nhảy cóc).
3. Với mỗi Fi trong chain, resolve FillFactInvalidated visibility tại cursor.
4. Duyệt chain từ F1: dừng tại link ĐẦU TIÊN chưa bị invalidate visible — visible-valid-head.
   current_fill_id = head đó.
5. NẾU link cuối cùng đã duyệt bị invalidate visible VÀ KHÔNG CÓ link kế tiếp visible → view_state =
   PENDING_CORRECTION (hoặc ABSENT nếu ExecutionResult không còn EXECUTED, §4), DỪNG.
```

```yaml
id: fill-current-view
kind: read_model
capability_id: execution-management
domain_context_id: fill-management
description: >
  Projection tiện dụng: fill_id "hiện tại" cho một execution_result_id, rebuild được từ §3–§4.
  KHÔNG authoritative — CHỈ query/UI, KHÔNG BAO GIỜ là input hợp lệ cho Position projection
  (`position.md`) hay bất kỳ computation nào khác — Position PHẢI fold trực tiếp từ authoritative
  Fill event stream (§10).
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho Position projection hay bất kỳ computation nào khác — CHỈ query/UI."
  - "view_state PHẢI đúng theo fold algorithm trên."
schema:
  execution_result_id: {type: string, required: true, description: "logical Fill key"}
  current_fill_id: {type: string, required: false, description: "chỉ có mặt khi view_state = VALID"}
  scope: {result: string, required: true, description: "chỉ có mặt khi view_state = VALID"}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  pending_correction_class: {type: enum, values: [AWAITING_SAME_SUBJECT_REPLACEMENT], required: false}
  last_recorded_time: timestamp
queries: [GetFillForExecutionResult, GetFillById, GetFillHistory]
```

## 6. Correction lineage

`FillRecorded` — correction lineage CHUẨN, same-key replacement với `fill_id` MỚI:

```text
F1 (FillRecorded, execution_result_id = E1, KHÔNG supersedes_fact_ref)
  → FillFactInvalidated targeting F1
  → F2 (FillRecorded MỚI), fill_id KHÁC F1, CÙNG execution_result_id = E1, F2.supersedes_fact_ref =
    F1 TRỰC TIẾP, F2.causation_refs CHỨA CẢ ExecutionResultRecorded LẪN FillFactInvalidated targeting
    F1 → một visible-valid-head duy nhất
```

**Mười invariant bắt buộc (đối xứng `risk.md` §10/`order.md` §9/`execution-result.md` §7, KHÔNG lặp lại toàn văn):** (1) gốc KHÔNG supersedes_fact_ref; (2) replacement BẮT BUỘC supersedes_fact_ref trỏ TRỰC TIẾP predecessor; (3) replacement CÙNG `execution_result_id`; (4) `causation_refs` chứa chính invalidation event, predecessor invalidate+visible TRƯỚC; (5) supersede đúng head hiện tại, cấm nhảy cóc; (6) tối đa một replacement trực tiếp, cấm fork; (7) replacement không visible trước invalidation; (8) append-only, `fill_id` cũ vẫn resolvable; (9) fact đã invalidate không tái sử dụng ngầm — `FillCurrentView` (§5) loại trừ tường minh; (10) retry payload khác khi predecessor chưa invalidate vẫn là conflict.

**Ràng buộc với ExecutionResult correction (execution-result.md §7):** nếu visible-valid ExecutionResult chuyển từ EXECUTED sang NOT_EXECUTED (hoặc invalidate không thay thế), MỌI Fill visible-valid gắn `execution_result_id` cũ PHẢI invalidate — KHÔNG replacement bắt buộc trong trường hợp này (khác correction thường: "mong đợi replacement" KHÔNG áp dụng khi source ExecutionResult không còn EXECUTED). Position (position.md) recompute trực tiếp từ Fill history còn lại.

## 7. Canonical policy identifiers — nguồn duy nhất (context `fill-management`)

```yaml
initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS
fill_derivation_idempotency_policy: ONE_VALID_FILL_PER_EXECUTION_RESULT
fill_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE
```

**`fill_derivation_idempotency_policy: ONE_VALID_FILL_PER_EXECUTION_RESULT`** — logical Fill key = `execution_result_id`; same key + same payload → idempotent reuse `fill_id`; same key + changed payload → deterministic conflict, reject. **KHÔNG unstated cross-stream atomicity** — ExecutionResult và Fill là hai authoritative stream RIÊNG.

**`fill_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE`** — xem §6 cho đầy đủ.

## 8. Time semantics và bitemporal correctness

- `ExecutionResultRecorded.recorded_time < FillRecorded.recorded_time` — strict causal ordering.
- `ExecutionResultRecorded.result_effective_time <= FillRecorded.fill_effective_time`.
- Mọi authoritative fact dùng cho Fill payload PHẢI thỏa `fact.recorded_time <= fill_context_cursor.recorded_time <= FillRecorded.recorded_time`.
- Replay tại cursor T chỉ thấy fact có `recorded_time ≤ T` — invalidation ghi SAU T KHÔNG visible tại T.
- Correction invalidation PHẢI ghi strict SAU target fact (§4).
- `market_time` PROHIBITED xuyên suốt tài liệu này.

## 9. Downstream reference contract (cho `position.md`)

`position.md` tham chiếu Fill qua ĐÚNG các field sau, KHÔNG hơn:

```yaml
fill_id: {type: string, required: true, ref: fill}
execution_result_id: {type: string, description: "= §1, ref: execution-result — logical Fill key"}
account_id: {type: string, ref: account, description: "= §1 — một phần Position key"}
environment: {type: enum, values: [PAPER], description: "= §1 — một phần Position key"}
instrument_selection_ref: {type: object, description: "= §1 — {instrument_id, venue_id, listing_id}, một phần Position key"}
direction: {type: enum, values: [LONG, SHORT], description: "= §1"}
fill_quantity: {type: decimal, description: "= §1 — GUARANTEE: LUÔN strictly positive"}
quantity_unit: {type: string, description: "= §1"}
fill_price: {type: decimal, description: "= §1 — GUARANTEE: LUÔN strictly positive"}
price_currency: {type: string, description: "= §1"}
fill_effective_time: {type: timestamp, description: "= §3"}
```

**Downstream authority rule:** `position.md` PHẢI resolve mọi field trên TRỰC TIẾP từ authoritative Fill event stream (§3–§4) TẠI ĐÚNG cursor mà chính computation đó đang dùng — VÀ PHẢI xác nhận visible-valid-head (§5 fold, KHÔNG `FillCurrentView` latest-state). `fill.md` KHÔNG author semantics của Position (file riêng).

## 10. Explanation contract

```text
Explanation(fill_id) = deterministic render của {originating ExecutionResult/Order scope, exact
fill_quantity/fill_price, origin chain} — KHÔNG computation mới, KHÔNG external lookup, KHÔNG dùng
bất kỳ giá trị nào không có mặt trong §1/§3.
```

## 11. Prohibitions

**Fill KHÔNG được sở hữu:** ExecutionResult/Order/Execution Intent/RiskEvaluation identity semantics; Position semantics (`position.md`, file riêng); partial-fill/multi-fill-per-result semantics; slippage/price-guarantee/limit-price model; fee/commission/funding; FX conversion; margin/leverage/liquidation model; realized/unrealized PnL; general workflow/saga engine; UI copy/natural-language generation infrastructure; database transaction/outbox/message-broker technology.

## 12. Ngoài phạm vi — defer

- **Full-Fill boundary (disclosed v0.1 judgment call):** `result_type = EXECUTED` LUÔN sản sinh CHÍNH XÁC MỘT full Fill, `fill_quantity == Order.quantity` — v0.1 KHÔNG partial-fill semantics. Đây là bounded scope tường minh theo yêu cầu task ("Prefer one-full-Fill semantics... If omitted, explicitly state"); partial fill deferred hoàn toàn tới Phase sau nếu cần, KHÔNG retrofit ở đây.
- Cơ chế/thuật toán PAPER simulation cụ thể xác định `fill_price` — deferred Phase 1, tài liệu này CHỈ pin domain (`>0`) và ý nghĩa (observed PAPER execution price).
- Stream Registry/Input Contract implementation cụ thể.
- Correction lineage riêng ngoài pattern chuẩn (§6) — không cần thêm.
- Implementation technology cho ExecutionResult→Fill recovery — boundary semantic pin, KHÔNG chọn công nghệ.
- Position semantics — hoàn toàn ngoài phạm vi Domain Contract này (`position.md`).

## 13. Acceptance scenarios (validation, không phải executable test tại C7 — phần liên quan trực tiếp Fill)

**Scenario 5 — Executed full Fill:** ExecutionResult `EXECUTED` → đúng một Fill, `fill_quantity == Order.quantity`, `fill_price > 0`.

**Scenario 6 — Not executed:** ExecutionResult `NOT_EXECUTED` → zero Fill, Position (position.md) unchanged.

**Scenario 7 — Result-to-Fill append gap:** `ExecutionResultRecorded(EXECUTED)` → crash TRƯỚC `FillRecorded` → recovery: tái sử dụng `execution_result_id`, append/reuse ĐÚNG MỘT Fill.

**Scenario 8 — Duplicate Fill:** cùng `execution_result_id` + cùng Fill payload → reuse `fill_id`; cùng `execution_result_id` + payload KHÁC → deterministic conflict.

**Scenario 9 — Fill origin mismatch:** reject Fill thay đổi `order_id`/`submission_request_id`/Account/TradableListing/`direction`/`quantity_unit`/`environment`/origin IDs so với ExecutionResult gốc.

**Scenario 10 — Invalid Fill quantity:** reject `fill_quantity <= 0`; reject `fill_quantity != Order.quantity`.

**Scenario 11 — Invalid Fill price:** reject `fill_price <= 0`; reject `price_currency` mismatch.

**Scenario 12 — Fill correction:** F1 → invalidate F1 → F2 `fill_id` MỚI, CÙNG `execution_result_id`, `supersedes_fact_ref` trực tiếp → một visible-valid-head.

**Scenario 17 — Result correction EXECUTED→NOT_EXECUTED (cặp với execution-result.md Scenario 17):** E1 EXECUTED → F1 tồn tại → invalidate E1 → E2 NOT_EXECUTED → F1 PHẢI invalidate (§4/§6 coupling rule) — trạng thái corrected cuối cùng KHÔNG chứa Fill visible-valid nào — KHÔNG được silently để F1 valid dưới result NOT_EXECUTED.

**Scenario 21 — Replay before Fill correction:** cursor TRƯỚC invalidation → F1 visible.

**Scenario 22 — Replay after Fill invalidation:** cursor SAU invalidation, TRƯỚC replacement → F1 EXCLUDED, Fill pending correction/absent.

**Scenario 23 — Replay after replacement Fill:** F2 visible → F2 là visible-valid-head.
