---
id: execution-result
title: Execution Result
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

# Execution Result

> **Vai trò của tài liệu này:** Domain Contract thứ nhất của Package 0.2-C7 (Execution Result, Fill, Position and Replay Integration Foundation) — định nghĩa **PaperExecutionObservation** (bản ghi authoritative, bất biến, DURABLE của MỘT lần bounded PAPER simulation computation — pin simulation evidence identity + output cùng lúc), **ExecutionResult** (bản ghi authoritative, bất biến, COPY nguyên vẹn `result_type` từ Observation visible-valid mà nó reference), và **ExecutionResultProcessingAttempt** (bản ghi authoritative của MỘT LẦN THỬ xử lý execution result). Draft, chưa Approved/Locked. Thuộc capability `execution-management` / context `execution-result-management` (đăng ký tại [`context-map.yaml`](./context-map.yaml), không đổi trong bounded correction này). Kiến trúc controlling: [`order.md`](./order.md) v0.2 Draft §8b (`eligible_for_execution_result_processing`, KHÔNG sửa), [`risk.md`](./risk.md) v0.3 Draft (bốn trục evidence pattern — ÁP DỤNG LẠI cho simulation evidence), [Chapter 8 §8.1.1/§8.2/§8.5](../constitution/08-event-model.md) (Locked). Tài liệu này CHỈ implement field/invariant mà các nguồn trên yêu cầu, KHÔNG author algorithm simulation thực tế.

ExecutionResult **KHÔNG phải** một OrderSubmissionRequest, một Fill, venue acknowledgement, exchange payload, hay Live routing. Nó **KHÔNG BAO GIỜ tự computation/reinterpret `result_type`** — CHỈ copy nguyên vẹn từ `PaperExecutionObservation` visible-valid mà nó reference (v0.2, đóng `C7-MAJ-01`). PaperExecutionObservation là **bản ghi authoritative, bất biến, DURABLE** của chính lần simulation computation đó — pin simulation evidence (policy/configuration/build/deterministic input, đều opaque versioned artifact ref) VÀ output (result_type, executed_quantity, execution_price) cùng lúc, KHÔNG author algorithm simulation thực tế (chỉ pin identity/evidence/output shape).

**Ví dụ walking-skeleton duy nhất dùng để validate thiết kế:** một Order `MARKET`/`OPEN_EXPOSURE` PAPER hợp lệ, một `OrderSubmissionRequested` visible-valid duy nhất, một Account, một TradableListing, environment PAPER, một simulated PAPER execution observation (`EXECUTED` hoặc `NOT_EXECUTED`) với simulation evidence durable. Ba mươi mốt Scenario chấp nhận toàn Package 0.2-C7 (1–31, xem `fill.md`/`position.md`/`replay-event.md` cho phần còn lại; `execution-result.md` §17 liệt kê phần liên quan trực tiếp) đều dựa trên ví dụ này.

**`paper-execution-observation-recorded`/`execution-result-processing-attempt-recorded`/`execution-result-recorded`/`execution-result-fact-invalidated`/`execution-result-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/C1–C6:** opaque identity không derive từ scope; envelope binding cho `*FactInvalidated`; fold algorithm "visible-valid-head per logical key" cho Current View; Current View KHÔNG BAO GIỜ authority; canonical policy identifier khai báo ĐÚNG MỘT NƠI; direct-predecessor-fact-targeting cho `supersedes_fact_ref`; **bốn bài học riêng từ C4–C6 correction:** (1) KHÔNG circular reference giữa Attempt và ExecutionResult; (2) `execution_result_processing_attempt_id` TÁCH BIỆT khỏi logical result key; (3) `attempt_outcome = PROCESSED` CHỈ ghi SAU KHI computation đã hoàn tất trọn vẹn; (4) `FAILED_BEFORE_RESULT` tường minh RETRYABLE. **Logical result key = `submission_request_id`, KHÔNG `order_id`** — preserved từ v0.1, KHÔNG đổi trong bounded correction này.

**v0.2 — bounded correction, đóng `C7-MAJ-01`/`C7-MAJ-03` (consolidated Review A + Independent Review B findings — `C7-MAJ-02`/`C7-MAJ-04` đóng tại `fill.md`/`position.md`):** (a) `C7-MAJ-01` — thêm `PaperExecutionObservation` (entity MỚI, §1) — durable, immutable record của simulation evidence (policy/configuration/build/deterministic input refs) VÀ output; `ExecutionResult` (§6) nay CHỈ copy `result_type` từ Observation visible-valid, KHÔNG tự computation; thứ tự corrected: computation hoàn tất → Observation ghi → Attempt PROCESSED ghi → Result ghi (§6a); hai recoverable gap tường minh (Observation-không-Attempt, Observation+Attempt-không-Result); correction EXECUTED↔NOT_EXECUTED dùng Observation MỚI tại cursor MỚI, KHÔNG invalidate Observation cũ (tránh excessive correction machinery). (b) `C7-MAJ-03` — loại bỏ hoàn toàn ngôn ngữ "cặp bắt buộc"/"atomic-adjacent" giữa `ExecutionResultFactInvalidated` và `FillFactInvalidated` (§7/§9) — thay bằng continuing eligibility rule (`eligible_as_position_contributing_fill`, `fill.md` §6) đánh giá LIÊN TỤC tại mọi cursor, KHÔNG phụ thuộc thời điểm cleanup. KHÔNG cross-stream transaction nào được introduce. Bounded — không đổi logical Result key, Attempt identity separation, C6 eligibility rule, Result correction direct-predecessor lineage, C1–C6 semantics, PAPER-only boundary.

**Phạm vi bounded tường minh:** KHÔNG author Fill/Position/Replay Event (file riêng). KHÔNG author Live behavior, exchange API payload, external order ID, routing/adapter, cancellation/replacement protocol. KHÔNG venue-specific rejection taxonomy — v0.1 CHỈ hai `result_type`: `EXECUTED`/`NOT_EXECUTED`. KHÔNG partial-fill semantics. KHÔNG fee/slippage/PnL/accounting. KHÔNG general workflow/saga engine. KHÔNG author simulation algorithm thực tế — CHỈ pin evidence/output shape, refs opaque. KHÔNG cross-stream atomic transaction. KHÔNG redefine Order/Execution Intent/Risk contract. KHÔNG sửa `order.md`/`execution-intent.md`/`risk.md`/`decision.md`/`trade-intent.md`/C1–C6/ADR/Constitution.

## 1. PaperExecutionObservation — `kind: entity`

```yaml
id: paper-execution-observation
kind: entity
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Bản ghi authoritative, bất biến, DURABLE của MỘT lần bounded PAPER simulation computation — pin
  chính xác simulation evidence identity (policy/configuration/build/deterministic input, đều opaque
  versioned artifact ref) VÀ output (result_type, executed_quantity, execution_price) cùng lúc.
  ExecutionResult (§6) KHÔNG BAO GIỜ tự computation/reinterpret result_type — CHỈ copy nguyên vẹn từ
  Observation visible-valid mà nó reference. Đóng `C7-MAJ-01` (durable Result simulation evidence).
  KHÔNG author algorithm simulation thực tế — CHỈ pin identity/evidence/output shape.
invariants:
  - "execution_observation_id là opaque, globally unique, gán tại PaperExecutionObservationRecorded — KHÔNG derive từ submission_request_id/observation_cursor hay bất kỳ field scope nào. Bất biến."
  - "Logical computation key = (submission_request_id, observation_cursor) — đối xứng risk.md's (trade_intent_id, risk_context_cursor). Idempotency VÀ correction-lineage fold ĐỀU scoped theo compound key này (§9) — KHÔNG order_id alone (đóng trước lớp lỗi tương tự C6-MAJ-01/C7-MAJ-01 nếu chỉ dùng order_id)."
  - "Same logical computation key + same evidence bundle (simulation_policy_ref/simulation_configuration_ref/simulation_build_ref/deterministic_input_ref) → same result_type/executed_quantity/execution_price payload — computation PHẢI deterministic."
  - "Same logical computation key + evidence HOẶC output KHÁC → deterministic conflict, reject khi append — KHÔNG silently overwrite (Scenario 25, §17)."
  - "result_type = EXECUTED: executed_quantity/execution_price/price_currency BẮT BUỘC có mặt, finite, strictly positive (executed_quantity CHÍNH XÁC bằng order_quantity), price_currency CHÍNH XÁC bằng TradableListing quote currency. result_type = NOT_EXECUTED: executed_quantity/execution_price/price_currency TUYỆT ĐỐI ABSENT (Scenario 6, §17)."
  - "Observation KHÔNG có correction lineage riêng ở v0.2 (§9, đóng bounded, tránh excessive correction machinery theo yêu cầu task) — mỗi (submission_request_id, observation_cursor) sinh ĐÚNG MỘT Observation immutable, append-only. Correction ExecutionResult (EXECUTED↔NOT_EXECUTED) dùng MỘT Observation MỚI tại observation_cursor MỚI (§6a/§9) — KHÔNG invalidate Observation cũ, Observation cũ vẫn historically resolvable nguyên vẹn."
schema:
  execution_observation_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  order_id: {type: string, required: true, ref: order}
  submission_request_id: {type: string, required: true, description: "một phần logical computation key"}
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
  order_quantity: {type: decimal, required: true, description: "= Order.quantity, copied"}
  quantity_unit: {type: string, required: true}
  observation_cursor: {type: object, required: true, description: "= execution_result_cursor shape (§3) — một phần logical computation key, Replay Cursor hợp lệ, TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1"}
  simulation_policy_ref: {type: string, required: true, description: "opaque versioned artifact ref — semantic simulation policy meaning, KHÔNG BAO GIỜ 'latest' (đúng ADR-013 §2.3 pattern áp dụng lại cho trục thứ nhất)"}
  simulation_configuration_ref: {type: string, required: true, description: "opaque versioned artifact ref — configured simulation parameter values (trục thứ hai)"}
  simulation_build_ref: {type: string, required: true, description: "opaque versioned artifact ref — exact executable identity đang chạy simulation, Chapter 9 §9.1/ADR-013 §2.5 pattern (trục thứ ba)"}
  deterministic_input_ref: {type: string, required: true, description: "opaque versioned artifact ref — exact deterministic input snapshot dùng cho computation này, KHÔNG redefine nội dung (trục thứ tư)"}
  result_type: {type: enum, values: [EXECUTED, NOT_EXECUTED], required: true}
  executed_quantity: {type: decimal, required: false, description: "BẮT BUỘC khi result_type=EXECUTED; TUYỆT ĐỐI ABSENT khi NOT_EXECUTED. finite, strictly positive, CHÍNH XÁC bằng order_quantity"}
  execution_price: {type: decimal, required: false, description: "BẮT BUỘC khi result_type=EXECUTED; TUYỆT ĐỐI ABSENT khi NOT_EXECUTED. finite, strictly positive"}
  price_currency: {type: string, required: false, description: "BẮT BUỘC khi result_type=EXECUTED; TUYỆT ĐỐI ABSENT khi NOT_EXECUTED. CHÍNH XÁC bằng TradableListing quote currency"}
events_emitted: [PaperExecutionObservationRecorded]
events_consumed: []
commands: []
queries: []
```

## 2. ExecutionResultProcessingAttempt — `kind: entity`

```yaml
id: execution-result-processing-attempt
kind: entity
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Bản ghi authoritative của MỘT lần thử xử lý execution-result observation cho một Order Submission
  Request — kể cả khi không dẫn tới ExecutionResult (INELIGIBLE/FAILED_BEFORE_RESULT). Tách biệt
  hoàn toàn khỏi ExecutionResult identity (§6) VÀ khỏi PaperExecutionObservation identity (§1).
invariants:
  - "execution_result_processing_attempt_id là opaque, globally unique, gán tại ExecutionResultProcessingAttemptRecorded — KHÔNG derive từ order_id/submission_request_id hay bất kỳ field scope nào."
  - "Logical result key = submission_request_id (KHÔNG order_id) — nhiều attempt (kể cả outcome khác nhau) CÓ THỂ tồn tại cùng logical key; idempotency scoped theo execution_result_processing_attempt_id (§11), KHÔNG theo logical key."
schema:
  execution_result_processing_attempt_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  order_id: {type: string, required: true, ref: order}
  submission_request_id: {type: string, required: true, description: "logical result key — xem §6"}
  execution_result_cursor: {type: object, required: true, description: "Replay Cursor hợp lệ, TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1 — xem §3 canonical envelope"}
events_emitted: [ExecutionResultProcessingAttemptRecorded]
events_consumed: []
commands: []
queries: []
```

## 3. Canonical event envelope — áp dụng cho mọi PaperExecutionObservation/ExecutionResultProcessingAttempt/ExecutionResult event (§4–§7)

Mọi event trong tài liệu này là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). KHÔNG event nào trong tài liệu này thuộc `event_class: decision` — dùng envelope tiêu chuẩn. `observation_cursor`/`execution_result_cursor` (CÙNG shape, dùng tên khác theo entity sở hữu) là **PAYLOAD field**, TÁI SỬ DỤNG nguyên vẹn shape Replay Cursor Chapter 8 §8.5.1.

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
  causation_refs: {cardinality: "PaperExecutionObservationRecorded: zero-or-more (Execution Result Engine internal trigger, Phase 1, chưa author). ExecutionResultProcessingAttemptRecorded: khi attempt_outcome=PROCESSED, BẮT BUỘC chứa PaperExecutionObservationRecorded tương ứng (§4) — KHÔNG rỗng; khi INELIGIBLE/FAILED_BEFORE_RESULT, zero-or-more. ExecutionResultRecorded: KHÔNG BAO GIỜ rỗng — PHẢI chứa CẢ ExecutionResultProcessingAttemptRecorded(PROCESSED) (§5) LẪN PaperExecutionObservationRecorded (§4) tương ứng, CỘNG ExecutionResultFactInvalidated của predecessor nếu là correction replacement (§9). ExecutionResultFactInvalidated: KHÔNG BAO GIỜ rỗng."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3."}
  effective_time: {cardinality: "required — semantic = observation_effective_time trên PaperExecutionObservationRecorded (§4); = result_effective_time trên ExecutionResultRecorded (§6); semantic khác trên các event còn lại."}
  decision_time: {cardinality: "PROHIBITED — event_class: decision KHÔNG áp dụng."}
  decision_context_cursor: {cardinality: "PROHIBITED (envelope-level) — cursor sống ở PAYLOAD."}
  market_time: {cardinality: "PROHIBITED — mọi event trong tài liệu này là bounded PAPER boundary observation authoritative, KHÔNG phải quan sát trực tiếp venue thật (Chapter 5 §5.2)."}
  source_identity: {cardinality: "PROHIBITED — luôn phát sinh nội bộ (Phase 1, chưa author), KHÔNG BAO GIỜ từ external feed."}

observation_cursor / execution_result_cursor (shape, đúng canonical Replay Cursor — Chapter 8 §8.5.1, TÁI SỬ DỤNG nguyên vẹn):
  recorded_time: <timestamp>
  input_contract_ref: {contract_id: <string>, contract_version: <string>}
  stream_registry_version: <string>
  lifecycle_frontier: {stream_id: <string>, position: {kind: <genesis | event>, sequence: <integer>}}
  stream_positions: {<stream_id>: <sequence>, ...}

subject_ref (PaperExecutionObservation, §1):
  context_id: execution-result-management
  subject_kind: entity
  subject_type: PaperExecutionObservation
  subject_id: <execution_observation_id — opaque, stable, xem §1>
  scope:
    submission_request_id: <string>

subject_ref (ExecutionResult — dùng cho ExecutionResultRecorded):
  context_id: execution-result-management
  subject_kind: entity
  subject_type: ExecutionResult
  subject_id: <execution_result_id — opaque, stable, xem §6>
  scope:
    submission_request_id: <string>

subject_ref (ExecutionResultProcessingAttempt, §2):
  context_id: execution-result-management
  subject_kind: entity
  subject_type: ExecutionResultProcessingAttempt
  subject_id: <execution_result_processing_attempt_id — opaque, stable, xem §2>
  scope:
    submission_request_id: <string>

event_types:
  PaperExecutionObservationRecorded: PAPER_EXECUTION_OBSERVATION_RECORDED
  ExecutionResultProcessingAttemptRecorded: EXECUTION_RESULT_PROCESSING_ATTEMPT_RECORDED
  ExecutionResultRecorded: EXECUTION_RESULT_RECORDED
  ExecutionResultFactInvalidated: EXECUTION_RESULT_FACT_INVALIDATED
```

`stream_ref`/`producer_ref` — Phase 1, chưa tồn tại. **Nếu Observation và Attempt cùng chia sẻ một stream vật lý (Phase 1 implementation, KHÔNG pin ở đây):** thứ tự append BẮT BUỘC — `PaperExecutionObservationRecorded` LUÔN append TRƯỚC `ExecutionResultProcessingAttemptRecorded(PROCESSED)` tương ứng, đúng §6a.

**Relational invariants bắt buộc trên cursor** (Chapter 8 §8.5.2):
```text
observation_cursor.recorded_time ≤ PaperExecutionObservationRecorded.recorded_time
execution_result_cursor.recorded_time ≤ ExecutionResultRecorded.recorded_time
fact.recorded_time ≤ tương ứng cursor.recorded_time (mọi authoritative fact dùng cho processing)
```

## 4. `PaperExecutionObservationRecorded` — `kind: event`

Kế thừa envelope §3. Payload đặc thù:

```yaml
id: paper-execution-observation-recorded
kind: event
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Fact AUTHORITATIVE DUY NHẤT ghi nhận MỘT lần bounded PAPER simulation computation — thiết lập
  TOÀN BỘ scope + simulation evidence + output cùng lúc, BẤT BIẾN. Đóng `C7-MAJ-01`. KHÔNG algorithm
  implementation nào được author tại đây.
invariants:
  - "payload.execution_observation_id PHẢI khớp đúng subject_ref.subject_id VÀ payload.submission_request_id PHẢI khớp đúng subject_ref.scope.submission_request_id."
  - "envelope.effective_time (observation_effective_time) = mặc định bằng observation_cursor.recorded_time."
  - "Ghi CHỈ SAU KHI bounded PAPER simulation computation đã hoàn tất trọn vẹn (§6a) — evidence bundle (simulation_policy_ref/simulation_configuration_ref/simulation_build_ref/deterministic_input_ref) VÀ output (result_type + optional executed_quantity/execution_price/price_currency) đã xác định XONG trước khi ghi."
  - "Nếu logical computation key (submission_request_id, observation_cursor) ĐÃ CÓ một Observation VALID tại thời điểm ghi, PaperExecutionObservationRecorded MỚI PHẢI resolve/reuse execution_observation_id đã tồn tại (evidence + output giống hệt — §1 idempotency) HOẶC bị reject (evidence/output khác) — TUYỆT ĐỐI KHÔNG tạo execution_observation_id thứ hai cho CÙNG key (Scenario 25, §17)."
  - "order_id/originating_execution_intent_id/originating_risk_evaluation_id/trade_intent_id/account_id/environment/instrument_selection_ref/direction/order_quantity/quantity_unit PHẢI khớp CHÍNH XÁC chuỗi visible-valid tại observation_cursor — KHÔNG dùng bất kỳ latest-state Current View nào làm input."
  - "No-look-ahead: mọi evidence ref PHẢI thỏa (khi có thể verify) fact liên quan có recorded_time ≤ observation_cursor.recorded_time."
payload:
  execution_observation_id: {type: string, required: true}
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
  order_quantity: {type: decimal, required: true}
  quantity_unit: {type: string, required: true}
  observation_cursor: {type: object, required: true, description: "cùng shape §3 — payload field"}
  simulation_policy_ref: {type: string, required: true}
  simulation_configuration_ref: {type: string, required: true}
  simulation_build_ref: {type: string, required: true}
  deterministic_input_ref: {type: string, required: true}
  result_type: {type: enum, values: [EXECUTED, NOT_EXECUTED], required: true}
  executed_quantity: {type: decimal, required: false}
  execution_price: {type: decimal, required: false}
  price_currency: {type: string, required: false}
```

## 5. `ExecutionResultProcessingAttemptRecorded` — `kind: event`

Kế thừa envelope §3.

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
  - "**v0.2 (đóng C7-MAJ-01):** attempt_outcome = PROCESSED: reason_code/checked_evidence_refs TUYỆT ĐỐI ABSENT (evidence đầy đủ sống trên PaperExecutionObservationRecorded §4 VÀ ExecutionResultRecorded §6). Ghi CHỈ SAU KHI `PaperExecutionObservationRecorded` (§4) tương ứng đã ghi nhận trọn vẹn cho CÙNG logical computation key — PROCESSED xác nhận 'computation hoàn tất VÀ evidence đã durably recorded thành Observation,' KHÔNG BAO GIỜ ghi TRƯỚC khi Observation tồn tại. `payload.execution_observation_id` BẮT BUỘC có mặt khi PROCESSED, TUYỆT ĐỐI ABSENT khi khác. KHÔNG payload field nào trỏ tới ExecutionResult — one-way sequence: Observation ghi TRƯỚC, Attempt PROCESSED ghi SAU đó, RỒI ExecutionResultRecorded.causation_refs trỏ ngược lại CẢ Attempt LẪN Observation (§6) — KHÔNG atomic multi-event transaction giữa các bước này."
  - "attempt_outcome = INELIGIBLE: reason_code = ORDER_RESULT_PROCESSING_INELIGIBLE (`eligible_for_execution_result_processing(order_id, execution_result_cursor) == false`, order.md §8b) — checked_evidence_refs khuyến nghị trỏ fact order.md/execution-intent.md/risk.md xác nhận điều kiện fail."
  - "attempt_outcome = FAILED_BEFORE_RESULT: reason_code = EXECUTION_RESULT_ENGINE_COMPUTATION_BOUNDARY_ERROR (v0.1 CHỈ một giá trị); checked_evidence_refs thường rỗng. Tường minh RETRYABLE. **v0.2:** áp dụng CHO CẢ hai khoảng trước-Observation VÀ trước-Attempt-nhưng-Observation-đã-tồn-tại — trường hợp sau PHẢI resolve theo §6a recoverable gap (tái sử dụng Observation đã có, KHÔNG rerun simulation), KHÔNG ghi FAILED_BEFORE_RESULT mới cho cùng Observation."
  - "Idempotency scoped theo TỪNG execution_result_processing_attempt_id (§11) — KHÔNG theo logical result key."
payload:
  execution_result_processing_attempt_id: {type: string, required: true}
  order_id: {type: string, required: true}
  submission_request_id: {type: string, required: true}
  execution_result_cursor: {type: object, required: true, description: "cùng shape §3 — payload field"}
  attempt_outcome: {type: enum, values: [PROCESSED, INELIGIBLE, FAILED_BEFORE_RESULT], required: true}
  execution_observation_id: {type: string, required: false, description: "BẮT BUỘC khi attempt_outcome=PROCESSED; TUYỆT ĐỐI ABSENT khi khác — trỏ Observation (§1) đã ghi nhận cho lần PROCESSED này (v0.2, đóng C7-MAJ-01)"}
  reason_code: {type: enum, values: [ORDER_RESULT_PROCESSING_INELIGIBLE, EXECUTION_RESULT_ENGINE_COMPUTATION_BOUNDARY_ERROR], required: false}
  checked_evidence_refs: {type: array, items: event_record_ref, required: false}
```

## 6. `ExecutionResultRecorded` — `kind: event`

Kế thừa envelope §3. Payload đặc thù:

```yaml
id: execution-result-recorded
kind: event
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Fact AUTHORITATIVE cho MỘT execution-result determination — thiết lập TOÀN BỘ scope cùng lúc,
  BẤT BIẾN. **v0.2 (đóng C7-MAJ-01):** `result_type` KHÔNG BAO GIỜ tự computation — CHỈ copy
  CHÍNH XÁC từ `execution_observation_id`'s PaperExecutionObservation (§1) visible-valid. CHỈ được
  phát khi ExecutionResultProcessingAttemptRecorded (§5) tương ứng có attempt_outcome = PROCESSED
  (§6a).
invariants:
  - "payload.execution_result_id PHẢI khớp đúng subject_ref.subject_id VÀ payload.submission_request_id PHẢI khớp đúng subject_ref.scope.submission_request_id."
  - "envelope.effective_time (result_effective_time) = mặc định bằng execution_result_cursor.recorded_time."
  - "causation_refs PHẢI chứa CẢ ExecutionResultProcessingAttemptRecorded (§5) tương ứng, attempt_outcome = PROCESSED, LẪN PaperExecutionObservationRecorded (§4) tương ứng — chứng minh CẢ Attempt PROCESSED LẪN Observation đã tồn tại TRƯỚC khi ExecutionResult này được tạo."
  - "**v0.2 (đóng C7-MAJ-01):** `payload.execution_observation_id` BẮT BUỘC, PHẢI trỏ đúng PaperExecutionObservation (§1) visible-valid tại execution_result_cursor. `payload.result_type` PHẢI BẰNG HỆT `execution_observation_id`'s Observation.result_type — TUYỆT ĐỐI KHÔNG tự tính lại/reinterpret. `payload.order_quantity`/`quantity_unit` PHẢI BẰNG HỆT Observation tương ứng."
  - "Logical result key = submission_request_id. Nếu key ĐÃ CÓ một ExecutionResult VALID (visible-valid-head, §8) tại thời điểm ghi, ExecutionResultRecorded MỚI PHẢI resolve/reuse execution_result_id đã tồn tại (payload giống hệt) HOẶC bị reject (payload khác, chưa invalidate predecessor) — TUYỆT ĐỐI KHÔNG tạo execution_result_id thứ hai cho CÙNG key trừ khi predecessor ĐÃ invalidate."
  - "order_id/originating_execution_intent_id/originating_risk_evaluation_id/trade_intent_id/account_id/environment/instrument_selection_ref/direction PHẢI khớp CHÍNH XÁC chuỗi visible-valid tại execution_result_cursor: Order visible-valid-head (order.md §8), submission_request_id chính là visible-valid OrderSubmissionRequested của Order đó, Execution Intent/RiskEvaluation/TradeIntent/Decision đều valid (order.md §8b). Reject nếu bất kỳ điều nào sau đúng: predecessor Order; Order đã invalidate; Submission Request đã invalidate; submission_request_id thuộc Order KHÁC; Order WITHDRAWN/EXPIRED; Execution Intent không còn ISSUED; Risk/Trade Intent/Decision chain invalid; Account/listing/direction/unit/environment đổi — KHÔNG dùng bất kỳ latest-state Current View nào làm input."
  - "`supersedes_fact_ref` TUYỆT ĐỐI ABSENT cho ExecutionResult gốc. BẮT BUỘC có mặt cho correction replacement, trỏ TRỰC TIẾP predecessor `ExecutionResultRecorded` fact (KHÔNG trỏ `ExecutionResultFactInvalidated`). Khi có mặt: `execution_result_id` PHẢI KHÁC predecessor; `submission_request_id` PHẢI BẰNG HỆT predecessor; **v0.2:** `execution_observation_id` CÓ THỂ trỏ MỘT Observation KHÁC (mới, tại cursor mới) so với predecessor — đây là cơ chế duy nhất để correction đổi `result_type` (§9), KHÔNG cần invalidate Observation cũ."
  - "Khi `supersedes_fact_ref` có mặt, `causation_refs` PHẢI CỘNG THÊM chứa chính `ExecutionResultFactInvalidated` targeting predecessor — predecessor PHẢI đã invalidate VÀ visible TRƯỚC khi replacement này được ghi."
  - "result_type = EXECUTED: đúng MỘT Fill (`fill.md`) được kỳ vọng theo sau, VỚI economics (quantity/price/currency) COPY CHÍNH XÁC từ Observation (fill.md §3a). result_type = NOT_EXECUTED: KHÔNG Fill nào được phép tồn tại VALID."
```

**§6a — Precondition và corrected Attempt/Observation/Result ordering (v0.2, đóng `C7-MAJ-01`).** ExecutionResultRecorded CHỈ được phát SAU KHI toàn bộ chuỗi năm bước sau hoàn tất TRỌN VẸN theo ĐÚNG thứ tự:

```text
1. eligible_for_execution_result_processing(order_id, execution_result_cursor) == true   (order.md §8b)
→ NẾU false: ExecutionResultProcessingAttemptRecorded(attempt_outcome=INELIGIBLE, reason_code=ORDER_RESULT_PROCESSING_INELIGIBLE) ghi — KHÔNG PaperExecutionObservationRecorded, KHÔNG ExecutionResultRecorded nào phát (Scenario 2, §17). Không cần chạy simulation computation.

2. NẾU (1) thỏa: bounded PAPER simulation computation hoàn tất — copy nguyên vẹn scope từ chuỗi
   visible-valid Order/Submission Request tại execution_result_cursor, resolve bốn trục simulation
   evidence (simulation_policy_ref/simulation_configuration_ref/simulation_build_ref/
   deterministic_input_ref), xác định result_type (VÀ executed_quantity/execution_price/
   price_currency nếu EXECUTED) — toàn bộ Observation payload đã xác định XONG.

3. PaperExecutionObservationRecorded (§4) ghi — durable record của evidence + output. Đây LÀ điểm
   "không quay đầu": SAU khi Observation ghi, computation KHÔNG BAO GIỜ được rerun để lấy một kết
   quả khác cho CÙNG logical computation key — mọi bước tiếp theo PHẢI dùng CHÍNH XÁC Observation
   này (§6a recoverable gap dưới).

4. ExecutionResultProcessingAttemptRecorded(attempt_outcome=PROCESSED, execution_observation_id =
   Observation vừa ghi) ghi NGAY SAU.

5. ExecutionResultRecorded phát — causation_refs trỏ CẢ Attempt PROCESSED LẪN Observation vừa ghi,
   result_type COPY CHÍNH XÁC từ Observation (Scenario 1/6, §17).

→ NẾU lỗi kỹ thuật/domain boundary xảy ra TRONG lúc bước (2) (TRƯỚC khi Observation ghi ở bước 3):
  ExecutionResultProcessingAttemptRecorded(attempt_outcome=FAILED_BEFORE_RESULT) ghi — KHÔNG
  Observation, KHÔNG ExecutionResultRecorded nào phát (Scenario 3, §17).

Thứ tự bắt buộc: computation hoàn tất → Observation ghi → Attempt PROCESSED ghi → ExecutionResult
ghi. KHÔNG BAO GIỜ đảo ngược, KHÔNG atomic transaction giữa bốn bước (mỗi bước là một append riêng,
recoverable độc lập).
```

**Recoverable append gap — HAI khoảng trống tường minh (v0.2, đóng `C7-MAJ-01`):**

```text
Gap A — Observation ghi, Attempt PROCESSED chưa ghi:
  Recovery PHẢI: tái sử dụng execution_observation_id đã tồn tại (KHÔNG rerun simulation); append/
  reuse ExecutionResultProcessingAttemptRecorded(PROCESSED) trỏ Observation đó; append/reuse
  ExecutionResultRecorded (Scenario 1, §17).

Gap B — Observation VÀ Attempt PROCESSED đã ghi, ExecutionResultRecorded chưa ghi:
  Recovery PHẢI: tái sử dụng Observation đã tồn tại; tái sử dụng Attempt PROCESSED đã tồn tại; append
  hoặc reuse ĐÚNG MỘT ExecutionResultRecorded — TUYỆT ĐỐI KHÔNG rerun simulation, KHÔNG tạo Attempt
  mới, KHÔNG tạo Observation mới.

TUYỆT ĐỐI KHÔNG BAO GIỜ rerun simulation để lấy một result_type/executed_quantity/execution_price
CÓ THỂ khác sau khi Observation đã tồn tại cho logical computation key đó — cả hai gap trên đều
resolve bằng cách TÁI SỬ DỤNG evidence đã durably persisted, KHÔNG bao giờ tính toán lại.
```

```yaml
payload:
  execution_result_id: {type: string, required: true}
  execution_observation_id: {type: string, required: true, description: "trỏ PaperExecutionObservation (§1) visible-valid — nguồn authoritative CHO result_type (v0.2, đóng C7-MAJ-01)"}
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
  order_quantity: {type: decimal, required: true, description: "= Order.quantity, copied — PHẢI BẰNG HỆT Observation"}
  quantity_unit: {type: string, required: true}
  result_type: {type: enum, values: [EXECUTED, NOT_EXECUTED], required: true, description: "COPY CHÍNH XÁC từ execution_observation_id's Observation.result_type — KHÔNG tự computation (v0.2, đóng C7-MAJ-01)"}
  execution_result_cursor: {type: object, required: true, description: "cùng shape §3 — payload field"}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho ExecutionResult gốc; BẮT BUỘC cho correction replacement — trỏ TRỰC TIẾP predecessor ExecutionResultRecorded fact"}
```

## 7. `ExecutionResultFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §3. `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: execution-result-fact-invalidated
kind: event
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Phủ định MỘT `ExecutionResultRecorded` lịch sử ĐÃ SAI. Correction lineage CHUẨN — replacement
  NHẬN execution_result_id MỚI, CÙNG logical result key (submission_request_id), replacement's
  `supersedes_fact_ref` trỏ TRỰC TIẾP predecessor. **v0.2 (đóng C7-MAJ-03) — KHÔNG cross-stream
  atomicity yêu cầu:** invalidation này KHÔNG BẮT BUỘC đi kèm bất kỳ `FillFactInvalidated` nào
  cùng lúc/atomic-adjacent — Fill liên quan (nếu có) trở nên derived-ineligible cho Position NGAY
  LẬP TỨC qua continuing eligibility rule (`eligible_as_position_contributing_fill`, fill.md §6),
  ĐỘC LẬP hoàn toàn với việc `FillFactInvalidated` có được append hay chưa, VÀ ĐỘC LẬP với thời
  điểm nó được append (fill.md Scenario 26, §14). `FillFactInvalidated` VẪN cần thiết cuối cùng để đánh dấu
  chính Fill fact đó là factually invalid trong stream RIÊNG của nó (fill.md §4/§6) — nhưng Position
  correctness KHÔNG BAO GIỜ phụ thuộc vào THỜI ĐIỂM cleanup đó xảy ra.
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref."
  - "invalidated_fact_ref PHẢI trỏ một ExecutionResultRecorded, CHƯA từng nhận invalidation khác — một fact chỉ bị invalidate đúng một lần. KHÔNG BAO GIỜ trỏ một ExecutionResultFactInvalidated khác (cấm invalidation-of-invalidation)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead) — thấy predecessor VALID; replay TẠI/SAU recorded_time thấy predecessor EXCLUDED khỏi head resolution (§8)."
  - "Mong đợi (không bắt buộc ngay lập tức) một ExecutionResultRecorded replacement CÙNG submission_request_id, execution_result_id MỚI, supersedes_fact_ref TRỎ TRỰC TIẾP predecessor, VÀ execution_observation_id CÓ THỂ trỏ MỘT Observation MỚI nếu correction đổi result_type (§9)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 8. `ExecutionResultCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §4–§7.

```text
Trước khi ExecutionResultRecorded tồn tại cho một submission_request_id:
  → KHÔNG có ExecutionResultCurrentView row nào tồn tại
  → GetExecutionResultForSubmissionRequest trả về NOT_FOUND / ABSENT
```

**Fold algorithm (đúng pattern đã proven tại `risk.md` §7/`order.md` §8 Tầng 1 — explicit chain, KHÔNG "newest uninvalidated fact"):**

```text
1. Group mọi ExecutionResultRecorded theo logical result key = submission_request_id.
2. Trong một key, dựng chain TƯỜNG MINH theo supersedes_fact_ref: E1 (gốc) → E2 (supersedes_fact_ref
   = E1, TRỰC TIẾP) → ... (cấm fork/nhảy cóc).
3. Với mỗi Ei trong chain, resolve ExecutionResultFactInvalidated visibility tại cursor.
4. Duyệt chain từ E1: dừng tại link ĐẦU TIÊN chưa bị invalidate visible tại cursor — visible-valid-
   head. current_execution_result_id = head đó.
5. NẾU link cuối cùng đã duyệt bị invalidate visible VÀ KHÔNG CÓ link kế tiếp visible → view_state =
   PENDING_CORRECTION, DỪNG.
```

```yaml
id: execution-result-current-view
kind: read_model
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Projection tiện dụng: execution_result_id "hiện tại" cho một submission_request_id, rebuild được
  từ §4–§7. KHÔNG authoritative — CHỈ query/UI, KHÔNG BAO GIỜ là input hợp lệ cho Fill derivation
  hay bất kỳ computation nào khác. Downstream field PHẢI resolve qua authoritative ExecutionResult
  event stream (`ref: execution-result`) TẠI CÙNG cursor mà computation đó đang dùng (§12).
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
queries: [GetExecutionResultForSubmissionRequest, GetExecutionResultById, GetExecutionResultHistory, GetPaperExecutionObservationById]
```

## 9. Correction lineage

**`PaperExecutionObservation` — append-only, KHÔNG correction lineage riêng ở v0.2 (§1 invariant, đóng bounded tránh excessive correction machinery):**

```text
O1 (PaperExecutionObservationRecorded, logical key = (S1, cursor_1)) — immutable, append-only.
Correction đổi result_type KHÔNG invalidate O1 — thay vào đó:
O2 (PaperExecutionObservationRecorded MỚI, logical key = (S1, cursor_2) — cursor KHÁC, evidence có
  thể khác) → execution_observation_id KHÁC O1 hoàn toàn độc lập, KHÔNG supersedes_fact_ref (vì
  KHÔNG cùng logical computation key — cursor khác nhau tự nhiên tách biệt).
O1 vẫn historically resolvable nguyên vẹn, KHÔNG bị xóa/rewrite/invalidate.
```

**`ExecutionResultRecorded` — correction lineage CHUẨN, same-key replacement với `execution_result_id` MỚI (đối xứng `risk.md` §10/`order.md` §9, KHÔNG đổi trong bounded correction này):**

```text
E1 (ExecutionResultRecorded, submission_request_id = S1, execution_observation_id = O1)
  → ExecutionResultFactInvalidated targeting E1
  → E2 (ExecutionResultRecorded MỚI), execution_result_id KHÁC E1, CÙNG submission_request_id = S1,
    E2.supersedes_fact_ref = E1 TRỰC TIẾP, E2.execution_observation_id = O2 (Observation MỚI, nếu
    correction đổi result_type — v0.2, đóng C7-MAJ-01) HOẶC = O1 (nếu correction KHÔNG đổi
    result_type, chỉ sửa field khác), E2.causation_refs CHỨA CẢ Attempt PROCESSED tương ứng LẪN
    O2/O1's PaperExecutionObservationRecorded LẪN ExecutionResultFactInvalidated targeting E1 →
    một visible-valid-head duy nhất.
```

**Mười invariant bắt buộc (không đổi, đối xứng `risk.md` §10/`order.md` §9):** (1) gốc KHÔNG supersedes_fact_ref; (2) replacement BẮT BUỘC supersedes_fact_ref trỏ TRỰC TIẾP predecessor; (3) replacement CÙNG `submission_request_id`; (4) `causation_refs` chứa chính invalidation event, predecessor invalidate+visible TRƯỚC; (5) supersede đúng head hiện tại, cấm nhảy cóc; (6) tối đa một replacement trực tiếp, cấm fork; (7) replacement không visible trước invalidation; (8) append-only, `execution_result_id` cũ vẫn resolvable; (9) fact đã invalidate không tái sử dụng ngầm — `ExecutionResultCurrentView` (§8) loại trừ tường minh; (10) retry payload khác khi predecessor chưa invalidate vẫn là conflict.

**v0.2 (đóng `C7-MAJ-03`) — KHÔNG ràng buộc cross-stream với Fill:** correction E1→E2 (bất kể `result_type` cũ/mới) KHÔNG BẮT BUỘC đi kèm bất kỳ `FillFactInvalidated` nào cùng lúc. Fill (nếu có) tham chiếu E1 tự động trở nên derived-ineligible cho Position NGAY LẬP TỨC tại cursor E1 bị invalidate (qua `eligible_as_position_contributing_fill`, fill.md §6), HOÀN TOÀN ĐỘC LẬP với việc/thời điểm `FillFactInvalidated` được append. `S1 KHÔNG kế thừa sang S2`: nếu Submission Request S1 bị invalidate và S2 thay thế (order.md §9), Observation/ExecutionResult của S1 VẪN gắn với `submission_request_id = S1`, KHÔNG BAO GIỜ tự động áp dụng cho S2.

## 10. Time semantics và bitemporal correctness

- `effective_time` — required trên mọi event trong tài liệu này.
- `recorded_time` — recorded axis, universal.
- **v0.2 (đóng C7-MAJ-01), chuỗi causal đầy đủ:** `OrderSubmissionRequested.recorded_time < PaperExecutionObservationRecorded.recorded_time < ExecutionResultProcessingAttemptRecorded(PROCESSED).recorded_time < ExecutionResultRecorded.recorded_time` — strict causal ordering, mỗi bước SAU bước trước.
- Effective-time: `OrderSubmissionRequested.effective_time <= PaperExecutionObservationRecorded.observation_effective_time <= ExecutionResultRecorded.result_effective_time`.
- Mọi authoritative fact dùng cho processing PHẢI thỏa `fact.recorded_time <= cursor.recorded_time <= resulting_event.recorded_time`.
- Replay tại cursor T chỉ thấy fact có `recorded_time ≤ T` — invalidation ghi SAU T KHÔNG visible tại T.
- `market_time` PROHIBITED xuyên suốt tài liệu này.

## 11. Canonical policy identifiers — nguồn duy nhất (context `execution-result-management`)

```yaml
initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS
paper_execution_observation_idempotency_policy: STABLE_COMPUTATION_KEY_SAME_EVIDENCE_IS_IDEMPOTENT
execution_result_derivation_idempotency_policy: ONE_VALID_RESULT_PER_SUBMISSION_REQUEST
execution_result_processing_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT
execution_result_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE
```

**`initial_fact_correction_policy`** — áp dụng CHỈ cho `ExecutionResultProcessingAttemptRecorded` (§5, KHÔNG same-ID replacement) VÀ `PaperExecutionObservationRecorded` (§4, KHÔNG same-ID replacement, append-only per §9).

**`paper_execution_observation_idempotency_policy: STABLE_COMPUTATION_KEY_SAME_EVIDENCE_IS_IDEMPOTENT`** (v0.2, đóng `C7-MAJ-01`) — logical computation key = `(submission_request_id, observation_cursor)`; retry cùng key + cùng evidence → idempotent no-op; retry cùng key + evidence KHÁC → reject tường minh. Đối xứng `risk_computation_idempotency_policy` (risk.md §12).

**`execution_result_derivation_idempotency_policy: ONE_VALID_RESULT_PER_SUBMISSION_REQUEST`** — logical result key = `submission_request_id`; same key + same payload (chưa invalidate) → idempotent no-op; same key + payload KHÁC (chưa invalidate predecessor) → deterministic conflict. **KHÔNG unstated cross-stream atomicity.**

**`execution_result_processing_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT`** — idempotency scoped theo TỪNG `execution_result_processing_attempt_id`, KHÔNG theo logical result key.

**`execution_result_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE`** — xem §9 cho đầy đủ.

## 12. Downstream reference contract (cho `fill.md`)

`fill.md` tham chiếu ExecutionResult/Observation qua ĐÚNG các field sau, KHÔNG hơn:

```yaml
execution_result_id: {type: string, required: true, ref: execution-result}
execution_observation_id: {type: string, description: "= §6, ref: paper-execution-observation — v0.2, đóng C7-MAJ-02, Fill PHẢI derive economics từ Observation này"}
order_id: {type: string, description: "= §6, ref: order"}
submission_request_id: {type: string, description: "= §6 — logical result key"}
originating_execution_intent_id: {type: string, description: "= §6, ref: execution-intent"}
originating_risk_evaluation_id: {type: string, description: "= §6, ref: risk"}
trade_intent_id: {type: string, description: "= §6, ref: trade-intent"}
account_id: {type: string, ref: account, description: "= §6"}
environment: {type: enum, values: [PAPER], description: "= §6"}
instrument_selection_ref: {type: object, description: "= §6 — {instrument_id, venue_id, listing_id}"}
direction: {type: enum, values: [LONG, SHORT], description: "= §6"}
order_quantity: {type: decimal, description: "= §6"}
quantity_unit: {type: string, description: "= §6"}
result_type: {type: enum, values: [EXECUTED, NOT_EXECUTED], description: "= §6 — COPY từ Observation, GUARANTEE: EXECUTED → đúng một Fill kỳ vọng; NOT_EXECUTED → KHÔNG Fill nào được phép"}
executed_quantity: {type: decimal, description: "= §1 (via execution_observation_id) — chỉ có mặt khi result_type=EXECUTED, nguồn CHO fill_quantity"}
execution_price: {type: decimal, description: "= §1 (via execution_observation_id) — chỉ có mặt khi result_type=EXECUTED, nguồn CHO fill_price"}
price_currency: {type: string, description: "= §1 (via execution_observation_id) — chỉ có mặt khi result_type=EXECUTED, nguồn CHO Fill price_currency"}
```

**Downstream authority rule:** `fill.md` PHẢI resolve mọi field trên TRỰC TIẾP từ authoritative ExecutionResult VÀ PaperExecutionObservation event stream (§4/§6) TẠI ĐÚNG cursor mà chính computation đó đang dùng — VÀ PHẢI xác nhận visible-valid-head (§8 fold, KHÔNG `ExecutionResultCurrentView` latest-state). Fill economics (quantity/price/currency) PHẢI COPY CHÍNH XÁC từ Observation, KHÔNG được độc lập quan sát/tính toán lại (v0.2, đóng `C7-MAJ-02`, xem `fill.md` §3a).

## 13. Explanation contract

```text
Explanation(execution_result_id) = deterministic render của {originating Order/Submission Request
scope, eligibility result, processing attempt, PaperExecutionObservation evidence identity,
result_type} — KHÔNG computation mới, KHÔNG external lookup, KHÔNG dùng bất kỳ giá trị nào không có
mặt trong §1/§2/§4/§6.
```

## 14. Prohibitions

**ExecutionResult/PaperExecutionObservation/ExecutionResultProcessingAttempt KHÔNG được sở hữu:** Order/Execution Intent/RiskEvaluation/Trade Intent/Decision identity semantics; Fill/Position semantics; venue-specific rejection taxonomy; external order ID/exchange payload/routing/adapter behavior; simulation algorithm thực tế (chỉ pin evidence/output shape); fee/slippage/PnL/accounting; general workflow/saga engine; cross-stream atomic transaction; UI copy/natural-language generation infrastructure; database transaction/outbox/message-broker technology.

## 15. Ngoài phạm vi — defer

- Stream Registry/Input Contract implementation cụ thể.
- Cơ chế/thuật toán PAPER simulation cụ thể — tài liệu này CHỈ pin evidence/output shape (`simulation_policy_ref`/`simulation_configuration_ref`/`simulation_build_ref`/`deterministic_input_ref`), KHÔNG pin thuật toán simulation.
- Granular exception/technical-failure sub-taxonomy cho `FAILED_BEFORE_RESULT`.
- Correction lineage riêng cho `ExecutionResultProcessingAttempt`/`PaperExecutionObservation` (append-only đủ cho v0.2, đóng bounded).
- Implementation technology cho mọi recovery gap.
- Runtime worker ownership, transaction boundaries, retry/backoff, monitoring/escalation.
- Fill/Position/Replay Event semantics — hoàn toàn ngoài phạm vi Domain Contract này.

## 16. Open questions ngoài phạm vi

- Cơ chế cụ thể generate `execution_result_id`/`execution_observation_id`/`execution_result_processing_attempt_id` — chưa quyết, Phase 1.
- Retention/resolvability horizon cụ thể.
- Không đóng OQ-002/OQ-003.

## 17. Acceptance scenarios (v0.2 — phần liên quan trực tiếp `execution-result.md`; xem `fill.md`/`position.md`/`replay-event.md` cho phần còn lại của 31 scenario toàn Package 0.2-C7)

**Scenario 1 — Eligible result processing / durable Result observation (v0.2, đóng `C7-MAJ-01`):** Order visible-valid-head, một Submission Request valid, Order status `SUBMISSION_REQUESTED`, complete origin chain valid → simulation computation hoàn tất → `PaperExecutionObservationRecorded` ghi → Attempt `PROCESSED` → một `ExecutionResultRecorded` (result_type copy từ Observation). Nếu crash SAU Observation, TRƯỚC Attempt/Result: recovery tái sử dụng Observation, append/reuse Attempt, append/reuse CÙNG Result — KHÔNG rerun simulation (Gap A/B, §6a).

**Scenario 2 — Ineligible result processing:** `eligible_for_execution_result_processing=false` → Attempt `INELIGIBLE` → KHÔNG Observation, KHÔNG ExecutionResult, KHÔNG Fill.

**Scenario 3 — Failure and retry:** Attempt A1 (`FAILED_BEFORE_RESULT`, TRƯỚC khi Observation ghi); Attempt A2 (CÙNG `submission_request_id`, `PROCESSED`, sau khi Observation MỚI ghi) sau đó — HỢP LỆ, recovery allowed.

**Scenario 4 — Result append gap:** Observation ghi, Attempt/Result chưa ghi (Gap A) HOẶC Observation+Attempt ghi, Result chưa ghi (Gap B) — recovery PHẢI tái sử dụng Observation/Attempt đã tồn tại, KHÔNG rerun simulation, KHÔNG duplicate (§6a).

**Scenario 6 — Not executed:** `result_type=NOT_EXECUTED` trên Observation → `executed_quantity`/`execution_price`/`price_currency` TUYỆT ĐỐI ABSENT → ExecutionResult copy `NOT_EXECUTED` → zero Fill (`fill.md` Scenario 6), Position unchanged.

**Scenario 17 — Result correction EXECUTED→NOT_EXECUTED (v0.2, đóng `C7-MAJ-01`/`C7-MAJ-03`, REVISED — không còn mandatory Fill-invalidation pairing):** E1 (execution_observation_id=O1, `EXECUTED`) → F1 tồn tại (fill.md) → invalidate E1 → E2 (execution_observation_id=O2, Observation MỚI, `NOT_EXECUTED`) — E2 KHÔNG bắt buộc đi kèm `FillFactInvalidated` targeting F1 CÙNG LÚC. F1 trở derived-ineligible cho Position NGAY LẬP TỨC tại cursor E1 invalidate (fill.md §6), ĐỘC LẬP hoàn toàn với thời điểm `FillFactInvalidated` (nếu có) được append sau đó — chi tiết Position-side xem `position.md` Scenario 17, §9.

**Scenario 27 — Result correction to EXECUTED (v0.2, MỚI):** E1 (`NOT_EXECUTED`) → invalidate E1 → Observation MỚI O2 (`EXECUTED`) → E2 references O2 → deterministic full Fill từ O2 economics (fill.md).

**Scenario 18 — Invalidated Submission Request:** Submission Request invalidate TRƯỚC khi result processing → `eligible_for_execution_result_processing=false` → KHÔNG eligible result processing nào.

**Scenario 19 — Order replacement:** O1 + S1 → invalidate O1 → O2 replacement → S1 gắn O1 KHÔNG còn hợp lệ cho processing MỚI → O2 cần Submission Request RIÊNG, rồi ExecutionResult RIÊNG.

**Scenario 20 — Execution Intent withdrawn:** Execution Intent `WITHDRAWN` → `eligible_for_execution_result_processing=false` → result processing ineligible.

**Scenario 25 — Changed simulation evidence (v0.2, mới, đóng `C7-MAJ-01`):** cùng logical observation key `(submission_request_id, observation_cursor)`, evidence khác (simulation_policy_ref/configuration_ref/input_ref khác) HOẶC output khác → deterministic conflict, reject khi append.
