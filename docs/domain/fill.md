---
id: fill
title: Fill
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

# Fill

> **Vai trò của tài liệu này:** Domain Contract thứ hai của Package 0.2-C7 (Execution Result, Fill, Position and Replay Integration Foundation) — định nghĩa **Fill**, bản ghi authoritative, bất biến, của quantity/price ĐÃ THỰC SỰ executed cho một [`execution-result.md`](./execution-result.md) `result_type = EXECUTED`. Draft, chưa Approved/Locked. Thuộc capability `execution-management` / context `fill-management` (đăng ký tại [`context-map.yaml`](./context-map.yaml), không đổi trong bounded correction này). Kiến trúc controlling: [`execution-result.md`](./execution-result.md) v0.2 Draft §1/§6 (PaperExecutionObservation + ExecutionResult, KHÔNG sửa), [`order.md`](./order.md) v0.2 Draft (origin chain, KHÔNG sửa), [Chapter 8 §8.1.1/§8.2/§8.5](../constitution/08-event-model.md) (Locked). Tài liệu này CHỈ implement field/invariant mà các nguồn trên yêu cầu.

Fill **KHÔNG phải** một ExecutionResult, một PaperExecutionObservation (cả hai `execution-result.md`, file riêng), một Position (`position.md`, file riêng), venue acknowledgement, hay bằng chứng price-guarantee/limit price. Nó là **bản ghi authoritative, bất biến, tự-giải-thích được** của quantity/price ĐÃ THỰC SỰ executed. **v0.2 (đóng `C7-MAJ-02`):** Fill KHÔNG BAO GIỜ độc lập quan sát/tính toán lại `fill_quantity`/`fill_price`/`price_currency` — TOÀN BỘ economics PHẢI copy CHÍNH XÁC từ `PaperExecutionObservation` (execution-result.md §1) visible-valid mà ExecutionResult (execution-result.md §6) tham chiếu, qua chuỗi `fill.execution_result_id → ExecutionResult.execution_observation_id → PaperExecutionObservation`.

**Ví dụ walking-skeleton (tiếp `execution-result.md`):** một ExecutionResult `EXECUTED` (tham chiếu một Observation cụ thể) → đúng một full Fill, `fill_quantity == Observation.executed_quantity == Order.quantity`, `fill_price == Observation.execution_price` — v0.1/v0.2 KHÔNG partial-fill semantics (disclosed bounded rule, §12).

**`fill-recorded`/`fill-fact-invalidated`/`fill-current-view` là canonical contract concept ID.**

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/C1–C7:** opaque identity không derive từ scope; direct-predecessor-fact-targeting cho `supersedes_fact_ref`; fold algorithm "visible-valid-head per logical key" cho Current View; Current View KHÔNG BAO GIỜ authority. **Fill KHÔNG có processing Attempt riêng** — derivation từ `ExecutionResultRecorded(EXECUTED)` là deterministic trực tiếp.

**v0.2 — bounded correction, đóng `C7-MAJ-02`/`C7-MAJ-03` (consolidated Review A + Independent Review B findings — `C7-MAJ-01` đóng tại `execution-result.md`, `C7-MAJ-04` đóng tại `position.md`):** (a) `C7-MAJ-02` — Fill economics (`fill_quantity`/`fill_price`/`price_currency`/`quantity_unit`) nay BẮT BUỘC copy CHÍNH XÁC từ `PaperExecutionObservation` (execution-result.md §1) visible-valid, qua `execution_observation_id` (field MỚI trên Fill payload, §1/§3) — Fill KHÔNG BAO GIỜ độc lập quan sát/recompute; Fill recovery (Result→Fill append gap, §3a) KHÔNG BAO GIỜ recompute giá — CHỈ copy persisted economics. (b) `C7-MAJ-03` — loại bỏ hoàn toàn ngôn ngữ "cặp bắt buộc"/"atomic-adjacent" giữa `FillFactInvalidated` và ExecutionResult correction (§4/§6) — thay bằng continuing eligibility rule `eligible_as_position_contributing_fill(fill_id, C)` (§6, MỚI) đánh giá LIÊN TỤC tại mọi cursor C — một Fill trở derived-ineligible cho Position NGAY LẬP TỨC khi ExecutionResult nó tham chiếu không còn là visible-valid EXECUTED head, ĐỘC LẬP hoàn toàn với việc/thời điểm `FillFactInvalidated` được append. Bounded — không đổi logical Fill key, full-Fill boundary, opaque Fill identity, Fill correction lineage (mười invariant), Position structural key, non-negative magnitude representation, C1–C6 semantics, PAPER-only boundary.

**Phạm vi bounded tường minh:** KHÔNG author Position semantics (`position.md`, file riêng). KHÔNG partial fill. KHÔNG slippage/price-guarantee semantics. KHÔNG fee/commission/funding. KHÔNG FX conversion. KHÔNG Live behavior. KHÔNG cross-stream atomic transaction. KHÔNG redefine ExecutionResult/PaperExecutionObservation/Order contract. KHÔNG sửa `execution-result.md`/`order.md`/`execution-intent.md`/`risk.md`/`decision.md`/`trade-intent.md`/C1–C6/ADR/Constitution.

## 1. Fill — `kind: entity`

```yaml
id: fill
kind: entity
capability_id: execution-management
domain_context_id: fill-management
description: >
  Bản ghi authoritative, bất biến, của quantity/price ĐÃ THỰC SỰ executed cho MỘT ExecutionResult
  result_type = EXECUTED. **v0.2 (đóng C7-MAJ-02):** mọi economics field (fill_quantity/fill_price/
  price_currency/quantity_unit) PHẢI copy CHÍNH XÁC từ PaperExecutionObservation (execution-result.md
  §1) mà ExecutionResult tham chiếu — Fill KHÔNG BAO GIỜ độc lập quan sát/tính toán. Scope hoàn toàn
  bất biến sau khi tạo. KHÔNG lifecycle riêng.
invariants:
  - "fill_id là opaque, globally unique, gán tại FillRecorded — KHÔNG derive từ execution_result_id hay bất kỳ field scope nào. Bất biến."
  - "MỘT Fill originate từ ĐÚNG MỘT ExecutionResult (execution_result_id, ref: execution-result), result_type = EXECUTED — logical Fill key = execution_result_id, tại một cursor cho trước tối đa MỘT Fill VALID cho mỗi execution_result_id (§7 `fill_derivation_idempotency_policy: ONE_VALID_FILL_PER_EXECUTION_RESULT`)."
  - "order_id/submission_request_id/originating_execution_intent_id/originating_risk_evaluation_id/trade_intent_id/account_id/environment/instrument_selection_ref/direction PHẢI BẰNG HỆT origin chain tương ứng của execution_result_id (execution-result.md §6) — Fill KHÔNG được tự chọn Account/instrument/direction khác ExecutionResult gốc đã pin (Scenario 9, §14)."
  - "**v0.2 (đóng C7-MAJ-02):** `execution_observation_id` PHẢI BẰNG HỆT `execution_result_id`'s ExecutionResult.execution_observation_id (execution-result.md §6). `fill_quantity` PHẢI BẰNG HỆT Observation.executed_quantity; `quantity_unit` PHẢI BẰNG HỆT Observation.quantity_unit; `fill_price` PHẢI BẰNG HỆT Observation.execution_price; `price_currency` PHẢI BẰNG HỆT Observation.price_currency — KHÔNG BAO GIỜ độc lập quan sát/tính toán lại (đóng đúng yêu cầu 'Fill must derive all execution economics from the immutable Observation')."
  - "fill_quantity PHẢI finite, STRICTLY POSITIVE (> 0) — v0.1/v0.2 executed result sản sinh CHÍNH XÁC một full Fill, KHÔNG partial-fill semantics (§12, disclosed bounded rule)."
  - "fill_price PHẢI finite, STRICTLY POSITIVE (> 0)."
  - "price_currency PHẢI CHÍNH XÁC BẰNG TradableListing quote currency (qua Observation, resolve từ instrument_selection_ref — KHÔNG redefine tại đây) — KHÔNG FX conversion."
  - "environment PHẢI = PAPER."
  - "Fill KHÔNG BAO GIỜ mutate ExecutionResult/Observation scope — mọi field origin chỉ COPY để tiện truy vấn, KHÔNG phải nguồn authoritative thứ hai."
schema:
  fill_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  execution_result_id: {type: string, required: true, ref: execution-result, description: "đúng một ExecutionResult, result_type = EXECUTED — logical Fill key"}
  execution_observation_id: {type: string, required: true, description: "v0.2 (đóng C7-MAJ-02) — PHẢI BẰNG HỆT execution_result_id's ExecutionResult.execution_observation_id, ref: execution-result.md §1 PaperExecutionObservation — nguồn CHO mọi economics field dưới đây"}
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
  fill_quantity: {type: decimal, required: true, description: "= Observation.executed_quantity, CHÍNH XÁC (v0.2, đóng C7-MAJ-02) — finite, STRICTLY POSITIVE"}
  quantity_unit: {type: string, required: true, description: "= Observation.quantity_unit, CHÍNH XÁC"}
  fill_price: {type: decimal, required: true, description: "= Observation.execution_price, CHÍNH XÁC (v0.2, đóng C7-MAJ-02) — finite, STRICTLY POSITIVE"}
  price_currency: {type: string, required: true, description: "= Observation.price_currency, CHÍNH XÁC"}
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
  causation_refs: {cardinality: "FillRecorded: KHÔNG BAO GIỜ rỗng — PHẢI chứa ExecutionResultRecorded (EXECUTED) tương ứng (execution-result.md §6), CỘNG FillFactInvalidated của predecessor nếu là correction replacement (§6). FillFactInvalidated: KHÔNG BAO GIỜ rỗng."}
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
  Fact AUTHORITATIVE cho MỘT Fill — thiết lập TOÀN BỘ scope cùng lúc, BẤT BIẾN. CHỈ được phát khi
  ExecutionResultRecorded (execution-result.md §6) tương ứng có result_type = EXECUTED (§3a). **v0.2
  (đóng C7-MAJ-02):** mọi economics field PHẢI copy CHÍNH XÁC từ PaperExecutionObservation tham
  chiếu qua ExecutionResult.execution_observation_id.
invariants:
  - "payload.fill_id PHẢI khớp đúng subject_ref.subject_id VÀ payload.execution_result_id PHẢI khớp đúng subject_ref.scope.execution_result_id."
  - "envelope.effective_time (fill_effective_time) = mặc định bằng fill_context_cursor.recorded_time."
  - "causation_refs PHẢI chứa ExecutionResultRecorded tương ứng (execution-result.md §6), result_type = EXECUTED, cùng execution_result_id."
  - "Logical Fill key = execution_result_id. Nếu key ĐÃ CÓ một Fill VALID tại thời điểm ghi, FillRecorded MỚI PHẢI resolve/reuse fill_id đã tồn tại (payload giống hệt) HOẶC bị reject (payload khác, chưa invalidate predecessor)."
  - "Mọi field origin (order_id/submission_request_id/originating_execution_intent_id/originating_risk_evaluation_id/trade_intent_id/account_id/environment/instrument_selection_ref/direction) PHẢI khớp CHÍNH XÁC ExecutionResult tương ứng (execution-result.md §6) TẠI fill_context_cursor."
  - "**v0.2 (đóng C7-MAJ-02):** `payload.execution_observation_id` PHẢI BẰNG HỆT ExecutionResult.execution_observation_id. `fill_quantity` PHẢI BẰNG HỆT Observation.executed_quantity; `quantity_unit` PHẢI BẰNG HỆT Observation.quantity_unit; `fill_price` PHẢI BẰNG HỆT Observation.execution_price; `price_currency` PHẢI BẰNG HỆT Observation.price_currency — TUYỆT ĐỐI KHÔNG được là một giá trị độc lập quan sát/tính toán khác."
  - "reject khi: fill_quantity <= 0; fill_price <= 0; fill_quantity != Observation.executed_quantity; quantity_unit != Observation.quantity_unit; fill_price != Observation.execution_price; price_currency != Observation.price_currency; environment != PAPER; origin IDs mismatch; execution_result.result_type != EXECUTED; execution_result_id không phải visible-valid-head (execution-result.md §8); submission request/Order không hợp lệ."
  - "`supersedes_fact_ref` TUYỆT ĐỐI ABSENT cho Fill gốc. BẮT BUỘC có mặt cho correction replacement, trỏ TRỰC TIẾP predecessor FillRecorded fact."
  - "Khi `supersedes_fact_ref` có mặt, `causation_refs` PHẢI CỘNG THÊM chứa chính FillFactInvalidated targeting predecessor."
```

**§3a — Precondition, ordering, và Result→Fill append-gap recovery (v0.2, đóng `C7-MAJ-02`).**

```text
1. ExecutionResultRecorded(result_type=EXECUTED) đã tồn tại, visible-valid-head (execution-result.md
   §8), tham chiếu một PaperExecutionObservation (execution-result.md §1) visible-valid.
2. Fill payload derive TRỰC TIẾP từ Observation — KHÔNG computation mới: fill_quantity =
   Observation.executed_quantity, quantity_unit = Observation.quantity_unit, fill_price =
   Observation.execution_price, price_currency = Observation.price_currency. Toàn bộ Fill payload
   đã xác định XONG bằng PHÉP COPY THUẦN TÚY.
3. FillRecorded phát (causation_refs trỏ ExecutionResultRecorded tương ứng).

Thứ tự bắt buộc toàn chuỗi: PaperExecutionObservationRecorded → ExecutionResultProcessingAttemptRecorded
(PROCESSED) → ExecutionResultRecorded → FillRecorded. KHÔNG BAO GIỜ đảo ngược, KHÔNG atomic
transaction giữa ExecutionResultRecorded và FillRecorded.
```

**Recoverable append gap (Result→Fill, v0.2 đóng `C7-MAJ-02`):** `ExecutionResultRecorded(EXECUTED)` đã ghi, NHƯNG crash TRƯỚC khi `FillRecorded` kịp append là một RECOVERABLE APPEND GAP. Recovery logic PHẢI: resolve CHÍNH XÁC Observation immutable đã persist (qua `execution_result_id → execution_observation_id`); COPY nguyên vẹn economics đã persisted (KHÔNG recompute giá dưới bất kỳ hình thức nào); append/reuse ĐÚNG MỘT Fill — TUYỆT ĐỐI KHÔNG duplicate, TUYỆT ĐỐI KHÔNG một fill_price khác (Scenario 7, §14).

```yaml
payload:
  fill_id: {type: string, required: true}
  execution_result_id: {type: string, required: true}
  execution_observation_id: {type: string, required: true, description: "v0.2, đóng C7-MAJ-02 — nguồn CHO economics dưới đây"}
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
  Phủ định MỘT `FillRecorded` lịch sử ĐÃ SAI. Correction lineage CHUẨN — replacement NHẬN fill_id
  MỚI, CÙNG logical Fill key (execution_result_id), replacement's `supersedes_fact_ref` trỏ TRỰC
  TIẾP predecessor FillRecorded. **v0.2 (đóng C7-MAJ-03) — KHÔNG cross-stream atomicity yêu cầu:**
  event này KHÔNG BẮT BUỘC được append đồng thời/atomic-adjacent với bất kỳ ExecutionResult
  correction nào. Fill có thể được invalidate độc lập (ví dụ Fill fact tự nó sai), HOẶC như một
  cleanup fact sau khi ExecutionResult tham chiếu đã ngừng là visible-valid EXECUTED head — trong
  cả hai trường hợp, `eligible_as_position_contributing_fill` (§6) là nguồn sự thật CHO Position,
  KHÔNG phải thời điểm event này được append.
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref."
  - "invalidated_fact_ref PHẢI trỏ một FillRecorded, CHƯA từng nhận invalidation khác."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này — thấy predecessor VALID trong stream RIÊNG của Fill (Scenario 21, §14); nhưng lưu ý: một Fill CÓ THỂ đã derived-ineligible cho Position (§6) TRƯỚC KHI event này tồn tại — hai khái niệm 'Fill valid trong stream riêng' và 'Fill eligible cho Position' TÁCH BIỆT hoàn toàn (v0.2, đóng C7-MAJ-03)."
  - "Mong đợi (không bắt buộc ngay lập tức) một FillRecorded replacement CÙNG execution_result_id, fill_id MỚI, supersedes_fact_ref TRỎ TRỰC TIẾP predecessor — CHỈ khi ExecutionResult tham chiếu VẪN visible-valid EXECUTED (nếu KHÔNG, KHÔNG replacement nào được kỳ vọng, §6)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 5. `FillCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §3–§4. **v0.2 lưu ý quan trọng:** view này CHỈ phản ánh trạng thái Fill fact TRONG STREAM RIÊNG của nó (`view_state`) — KHÔNG phản ánh `eligible_as_position_contributing_fill` (§6), vốn là một rule RIÊNG, đánh giá kết hợp CẢ Fill lineage LẪN ExecutionResult lineage. `position.md` KHÔNG BAO GIỜ dùng `FillCurrentView` làm input (đúng nguyên tắc Current-View-never-authority, cộng thêm lý do §6 dưới).

```text
Trước khi FillRecorded tồn tại cho một execution_result_id:
  → KHÔNG có FillCurrentView row nào tồn tại
  → GetFillForExecutionResult trả về NOT_FOUND / ABSENT
```

**Fold algorithm (đúng pattern explicit-chain đã proven tại `order.md` §8 Tầng 1/`execution-result.md` §8):**

```text
1. Group mọi FillRecorded theo logical Fill key = execution_result_id.
2. Trong một key, dựng chain TƯỜNG MINH theo supersedes_fact_ref: F1 (gốc) → F2 (supersedes_fact_ref
   = F1, TRỰC TIẾP) → ... (cấm fork/nhảy cóc).
3. Với mỗi Fi trong chain, resolve FillFactInvalidated visibility tại cursor.
4. Duyệt chain từ F1: dừng tại link ĐẦU TIÊN chưa bị invalidate visible — visible-valid-head trong
   stream RIÊNG của Fill. current_fill_id = head đó.
5. NẾU link cuối cùng đã duyệt bị invalidate visible VÀ KHÔNG CÓ link kế tiếp visible → view_state =
   PENDING_CORRECTION (hoặc ABSENT), DỪNG.
```

```yaml
id: fill-current-view
kind: read_model
capability_id: execution-management
domain_context_id: fill-management
description: >
  Projection tiện dụng: fill_id "hiện tại" TRONG STREAM RIÊNG của một execution_result_id, rebuild
  được từ §3–§4. KHÔNG authoritative — CHỈ query/UI, KHÔNG BAO GIỜ là input hợp lệ cho Position
  projection (`position.md`) hay bất kỳ computation nào khác — Position PHẢI dùng
  `eligible_as_position_contributing_fill` (§6) TRỰC TIẾP từ authoritative event stream, KHÔNG view
  này.
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho Position projection hay bất kỳ computation nào khác — CHỈ query/UI."
  - "view_state PHẢI đúng theo fold algorithm trên — CHỈ phản ánh Fill stream riêng, KHÔNG phản ánh eligible_as_position_contributing_fill (§6)."
schema:
  execution_result_id: {type: string, required: true, description: "logical Fill key"}
  current_fill_id: {type: string, required: false, description: "chỉ có mặt khi view_state = VALID"}
  scope: {result: string, required: true, description: "chỉ có mặt khi view_state = VALID"}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  pending_correction_class: {type: enum, values: [AWAITING_SAME_SUBJECT_REPLACEMENT], required: false}
  last_recorded_time: timestamp
queries: [GetFillForExecutionResult, GetFillById, GetFillHistory]
```

## 6. Continuing Fill contribution eligibility — `eligible_as_position_contributing_fill` (v0.2, MỚI, đóng `C7-MAJ-03`)

**Vai trò:** một rule normative, derived, deterministic, đánh giá LIÊN TỤC tại MỌI cursor C (KHÔNG chỉ tại thời điểm append) — trả lời "Fill này CÓ ĐANG hợp lệ để đóng góp vào Position projection tại cursor C hay không." Đây LÀ nguồn sự thật DUY NHẤT cho Position (`position.md` §2) — KHÔNG phải `FillCurrentView` (§5), KHÔNG phải sự hiện diện/vắng mặt của `FillFactInvalidated`.

```text
eligible_as_position_contributing_fill(fill_id, C) =
      Fill là visible-valid-head cho execution_result_id của nó TẠI C                              (§5 fold, stream riêng Fill)
  AND ExecutionResult được reference (fill.execution_result_id) là visible-valid-head cho
      submission_request_id của nó TẠI C                                                            (execution-result.md §8 fold)
  AND ExecutionResult đó có result_type == EXECUTED TẠI C
  AND PaperExecutionObservation được ExecutionResult đó reference là visible tại C
      (execution-result.md §1 — append-only, luôn visible một khi recorded_time ≤ C)
  AND Fill payload (fill_quantity/quantity_unit/fill_price/price_currency) khớp CHÍNH XÁC economics
      của Observation đó                                                                             (§1 invariant, luôn true nếu Fill được ghi hợp lệ — pin tường minh làm continuing check, KHÔNG chỉ append-time check)
```

**Đây LÀ một continuing cursor-bound validity rule, KHÔNG chỉ một append-time check** — kết quả CÓ THỂ chuyển từ `true` sang `false` GIỮA hai cursor liên tiếp mà KHÔNG có bất kỳ thay đổi nào trong stream RIÊNG của Fill đó (ví dụ: ExecutionResult bị invalidate ở cursor C2 > C1, `eligible_as_position_contributing_fill(fill_id, C1) = true` nhưng `eligible_as_position_contributing_fill(fill_id, C2) = false`, DÙ Fill fact chính nó KHÔNG hề bị invalidate giữa C1 và C2).

**Hành vi khi ExecutionResult bị invalidate (v0.2, đóng `C7-MAJ-03` — KHÔNG cross-stream atomicity):**

```text
Ngay tại cursor ExecutionResult E1 bị invalidate (execution-result.md §7):
  → điều kiện thứ hai/ba của eligible_as_position_contributing_fill fail NGAY LẬP TỨC cho F1
  → F1 remains historical trong stream riêng của nó (fill.md §5 view_state có thể vẫn VALID)
  → F1 MAY remain non-invalidated (FillFactInvalidated KHÔNG bắt buộc append cùng lúc)
  → F1 is NOT eligible for Position contribution — Position (position.md §2) EXCLUDES F1 (Scenario 26, §14)
  → Replay tại cursor này thấy: ExecutionResult invalid/pending correction, Fill historical NHƯNG
    derived-ineligible

FillFactInvalidated VẪN cần thiết CUỐI CÙNG để đánh dấu chính Fill fact là factually invalid trong
stream riêng của nó (cleanup/correction fact, §4) — nhưng Position correctness KHÔNG BAO GIỜ phụ
thuộc vào THỜI ĐIỂM cleanup đó xảy ra, đúng yêu cầu 'Position correctness must not depend on when
cleanup occurs.'
```

**Result correction to NOT_EXECUTED — quy tắc đầy đủ:**

```text
E1 EXECUTED → F1 tồn tại
  → invalidate E1
  → NGAY LẬP TỨC: F1 ineligible for Position (điều kiện 2/3 fail)
  → E2 (NOT_EXECUTED, Observation MỚI) ghi
  → SAU E2: F1 VẪN ineligible (E1 KHÔNG còn là head; ngay cả nếu E1 VẪN được resolve theo cách nào
    đó, result_type của head hiện tại là NOT_EXECUTED)
  → KHÔNG Fill mới nào được phép cho submission_request_id này (execution-result.md §6: result_type
    NOT_EXECUTED → KHÔNG Fill nào được phép tồn tại VALID cho ExecutionResult ĐÓ)
  → FillFactInvalidated (khi/nếu append) là explicit cleanup/correction fact CHO F1's OWN stream —
    KHÔNG có replacement Fill nào được kỳ vọng (§4 invariant cuối)
```

## 7. Correction lineage

`FillRecorded` — correction lineage CHUẨN, same-key replacement với `fill_id` MỚI, KHÔNG đổi trong bounded correction này:

```text
F1 (FillRecorded, execution_result_id = E1, KHÔNG supersedes_fact_ref)
  → FillFactInvalidated targeting F1
  → F2 (FillRecorded MỚI), fill_id KHÁC F1, CÙNG execution_result_id = E1 (E1 VẪN visible-valid
    EXECUTED tại thời điểm này — nếu KHÔNG, KHÔNG replacement Fill nào hợp lệ, §6), F2.supersedes_fact_ref
    = F1 TRỰC TIẾP → một visible-valid-head duy nhất
```

**Mười invariant bắt buộc (không đổi):** (1) gốc KHÔNG supersedes_fact_ref; (2) replacement BẮT BUỘC supersedes_fact_ref trỏ TRỰC TIẾP predecessor; (3) replacement CÙNG `execution_result_id`; (4) `causation_refs` chứa chính invalidation event, predecessor invalidate+visible TRƯỚC; (5) supersede đúng head hiện tại, cấm nhảy cóc; (6) tối đa một replacement trực tiếp, cấm fork; (7) replacement không visible trước invalidation; (8) append-only, `fill_id` cũ vẫn resolvable; (9) fact đã invalidate không tái sử dụng ngầm — `FillCurrentView` (§5) loại trừ tường minh; (10) retry payload khác khi predecessor chưa invalidate vẫn là conflict.

**v0.2 (đóng `C7-MAJ-03`):** KHÔNG còn ràng buộc "cặp bắt buộc"/"atomic-adjacent" với ExecutionResult correction — xem §6 cho continuing eligibility rule thay thế hoàn toàn cơ chế đó.

## 8. Canonical policy identifiers — nguồn duy nhất (context `fill-management`)

```yaml
initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS
fill_derivation_idempotency_policy: ONE_VALID_FILL_PER_EXECUTION_RESULT
fill_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE
```

**`fill_derivation_idempotency_policy: ONE_VALID_FILL_PER_EXECUTION_RESULT`** — logical Fill key = `execution_result_id`; same key + same payload → idempotent reuse `fill_id`; same key + changed payload → deterministic conflict.

**`fill_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE`** — xem §7.

## 9. Time semantics và bitemporal correctness

- **v0.2, chuỗi causal đầy đủ:** `ExecutionResultRecorded.recorded_time < FillRecorded.recorded_time` (strict, kế thừa chuỗi đầy đủ từ execution-result.md §10: `OrderSubmissionRequested < PaperExecutionObservationRecorded < ExecutionResultProcessingAttemptRecorded(PROCESSED) < ExecutionResultRecorded < FillRecorded`).
- Effective-time: `ExecutionResultRecorded.result_effective_time <= FillRecorded.fill_effective_time`.
- Mọi authoritative fact dùng cho Fill payload PHẢI thỏa `fact.recorded_time <= fill_context_cursor.recorded_time <= FillRecorded.recorded_time`.
- Replay tại cursor T chỉ thấy fact có `recorded_time ≤ T` — invalidation ghi SAU T KHÔNG visible tại T.
- Correction invalidation PHẢI ghi strict SAU target fact (§4).
- `market_time` PROHIBITED xuyên suốt tài liệu này.

## 10. Downstream reference contract (cho `position.md`)

`position.md` tham chiếu Fill qua ĐÚNG các field sau, KHÔNG hơn — VÀ PHẢI dùng `eligible_as_position_contributing_fill` (§6), KHÔNG `FillCurrentView`:

```yaml
fill_id: {type: string, required: true, ref: fill}
execution_result_id: {type: string, description: "= §1, ref: execution-result — logical Fill key"}
account_id: {type: string, ref: account, description: "= §1 — một phần Position key"}
environment: {type: enum, values: [PAPER], description: "= §1 — một phần Position key"}
instrument_selection_ref: {type: object, description: "= §1 — {instrument_id, venue_id, listing_id}, một phần Position key"}
direction: {type: enum, values: [LONG, SHORT], description: "= §1"}
fill_quantity: {type: decimal, description: "= §1 — GUARANTEE: LUÔN strictly positive, = Observation.executed_quantity"}
quantity_unit: {type: string, description: "= §1"}
fill_price: {type: decimal, description: "= §1 — GUARANTEE: LUÔN strictly positive, = Observation.execution_price"}
price_currency: {type: string, description: "= §1"}
fill_effective_time: {type: timestamp, description: "= §3"}
```

**Downstream authority rule:** `position.md` PHẢI dùng `eligible_as_position_contributing_fill(fill_id, C)` (§6) TRỰC TIẾP — KHÔNG `FillCurrentView` latest-state, KHÔNG chỉ kiểm tra Fill stream riêng.

## 11. Explanation contract

```text
Explanation(fill_id) = deterministic render của {originating ExecutionResult/Observation/Order scope,
exact fill_quantity/fill_price copy từ Observation, origin chain, eligible_as_position_contributing_fill
kết quả TẠI cursor hiện hành} — KHÔNG computation mới, KHÔNG external lookup.
```

## 12. Prohibitions

**Fill KHÔNG được sở hữu:** ExecutionResult/PaperExecutionObservation/Order/Execution Intent/RiskEvaluation identity semantics; Position semantics; partial-fill/multi-fill-per-result semantics; slippage/price-guarantee/limit-price model; fee/commission/funding; FX conversion; margin/leverage/liquidation model; realized/unrealized PnL; cross-stream atomic transaction; general workflow/saga engine; UI copy/natural-language generation infrastructure; database transaction/outbox/message-broker technology.

## 13. Ngoài phạm vi — defer

- **Full-Fill boundary (disclosed v0.1 judgment call, không đổi v0.2):** `result_type = EXECUTED` LUÔN sản sinh CHÍNH XÁC MỘT full Fill — v0.1/v0.2 KHÔNG partial-fill semantics.
- Cơ chế/thuật toán PAPER simulation cụ thể — deferred, xem execution-result.md §15.
- Stream Registry/Input Contract implementation cụ thể.
- Implementation technology cho ExecutionResult→Fill recovery.
- Position semantics — hoàn toàn ngoài phạm vi Domain Contract này.

## 14. Acceptance scenarios (v0.2 — phần liên quan trực tiếp Fill; xem `execution-result.md`/`position.md`/`replay-event.md` cho phần còn lại)

**Scenario 5 — Executed full Fill:** ExecutionResult `EXECUTED` → đúng một Fill, `fill_quantity == Observation.executed_quantity` (== `Order.quantity`), `fill_price == Observation.execution_price > 0`.

**Scenario 6 — Not executed:** ExecutionResult `NOT_EXECUTED` → zero Fill, Position (position.md) unchanged.

**Scenario 7 — Result-to-Fill append gap / deterministic Fill recovery (v0.2, đóng `C7-MAJ-02`):** `ExecutionResultRecorded(EXECUTED)` tham chiếu Observation(execution_price=P) → crash TRƯỚC `FillRecorded` → recovery: resolve CHÍNH XÁC Observation đó, copy P nguyên vẹn (KHÔNG BAO GIỜ recompute giá), append/reuse ĐÚNG MỘT Fill — Fill payload GIỐNG HỆT mọi lần retry.

**Scenario 8 — Duplicate Fill:** cùng `execution_result_id` + cùng Fill payload → reuse `fill_id`; cùng `execution_result_id` + payload KHÁC → deterministic conflict. **Fill correction under valid Result (mở rộng, v0.2):** khi E1 VẪN valid EXECUTED, F1 invalidate → F2 replacement CÙNG `execution_result_id` → F2 Position-eligible (qua §6, đối xứng Scenario 12/16 dưới/`position.md`).

**Scenario 9 — Fill origin mismatch:** reject Fill thay đổi `order_id`/`submission_request_id`/Account/TradableListing/`direction`/`quantity_unit`/`environment`/origin IDs so với ExecutionResult/Observation gốc.

**Scenario 10 — Invalid Fill quantity:** reject `fill_quantity <= 0`; reject `fill_quantity != Observation.executed_quantity`.

**Scenario 11 — Invalid Fill price:** reject `fill_price <= 0`; reject `fill_price != Observation.execution_price`; reject `price_currency` mismatch.

**Scenario 12 — Fill correction:** F1 → invalidate F1 → F2 `fill_id` MỚI, CÙNG `execution_result_id`, `supersedes_fact_ref` trực tiếp → một visible-valid-head trong stream riêng.

**Scenario 21 — Replay before Fill correction:** cursor TRƯỚC invalidation → F1 visible trong stream riêng.

**Scenario 22 — Replay after Fill invalidation:** cursor SAU invalidation, TRƯỚC replacement → F1 EXCLUDED khỏi stream riêng head.

**Scenario 23 — Replay after replacement Fill:** F2 visible → F2 là visible-valid-head trong stream riêng.

**Scenario 26 — Result invalidation gap (v0.2, MỚI, đóng `C7-MAJ-03`):** E1 EXECUTED → F1 tồn tại → invalidate E1 → F1 CHƯA invalidate (chưa có `FillFactInvalidated`) → `eligible_as_position_contributing_fill(F1, C) = false` NGAY LẬP TỨC (điều kiện 2/3 fail) → F1 vẫn historical trong stream riêng, CÓ THỂ VẪN `view_state=VALID` tại `FillCurrentView` (§5), NHƯNG KHÔNG eligible cho Position — Position (position.md) EXCLUDES F1.
