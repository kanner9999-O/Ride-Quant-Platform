---
id: execution-result
title: Execution Result
version: "0.3"
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

> **Vai trò của tài liệu này:** Domain Contract thứ nhất của Package 0.2-C7 (Execution Result, Fill, Position and Replay Integration Foundation) — định nghĩa **ExecutionResultComputation** (bản ghi authoritative, bất biến, đại diện ĐÚNG MỘT authorized Execution Result computation lifecycle — neo authorization VÀ idempotency vào computation identity, KHÔNG vào cursor), **PaperExecutionObservation** (bản ghi authoritative, bất biến, DURABLE của MỘT lần bounded PAPER simulation computation, gắn CHÍNH XÁC một ExecutionResultComputation), **ExecutionResult** (bản ghi authoritative, bất biến, COPY nguyên vẹn `result_type` từ Observation visible-valid), và **ExecutionResultProcessingAttempt** (bản ghi authoritative của MỘT LẦN THỬ xử lý execution result). Draft, chưa Approved/Locked. Thuộc capability `execution-management` / context `execution-result-management` (đăng ký tại [`context-map.yaml`](./context-map.yaml), không đổi trong correction này). Kiến trúc controlling: [`order.md`](./order.md) v0.2 Draft §8b (`eligible_for_execution_result_processing`, KHÔNG sửa), [`risk.md`](./risk.md) v0.3 Draft (bốn trục evidence pattern), [Chapter 8 §8.1.1/§8.2/§8.5](../constitution/08-event-model.md) (Locked). Tài liệu này CHỈ implement field/invariant mà các nguồn trên yêu cầu, KHÔNG author algorithm simulation thực tế, KHÔNG author workflow/saga/command infrastructure.

ExecutionResult **KHÔNG phải** một OrderSubmissionRequest, một Fill, venue acknowledgement, exchange payload, hay Live routing. Nó **KHÔNG BAO GIỜ tự computation/reinterpret `result_type`** — CHỈ copy nguyên vẹn từ `PaperExecutionObservation` visible-valid mà nó reference (đóng `C7-MAJ-01`). PaperExecutionObservation là **bản ghi authoritative, bất biến, DURABLE** của chính lần simulation computation đó. **v0.3 (đóng `C7-DELTA-MAJ-01`):** Observation KHÔNG còn tự mình là điểm neo authorization — `ExecutionResultComputation` MỚI là identity authoritative đại diện "một lần computation ĐÃ ĐƯỢC AUTHORIZE" (qua domain eligibility cho INITIAL, hoặc qua correction lineage cho CORRECTION); cursor vẫn là immutable computation context/replay evidence NHƯNG KHÔNG còn tự nó authorize một computation mới.

**Ví dụ walking-skeleton duy nhất dùng để validate thiết kế:** một Order `MARKET`/`OPEN_EXPOSURE` PAPER hợp lệ, một `OrderSubmissionRequested` visible-valid duy nhất, một Account, một TradableListing, environment PAPER, một authorized computation (INITIAL) sản sinh một simulated PAPER execution observation (`EXECUTED` hoặc `NOT_EXECUTED`) với simulation evidence durable. Ba mươi bảy Scenario chấp nhận toàn Package 0.2-C7 (1–37, xem `fill.md`/`position.md`/`replay-event.md` cho phần còn lại; `execution-result.md` §19 liệt kê phần liên quan trực tiếp) đều dựa trên ví dụ này.

**`execution-result-computation-authorized`/`paper-execution-observation-recorded`/`execution-result-processing-attempt-recorded`/`execution-result-recorded`/`execution-result-fact-invalidated`/`execution-result-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/C1–C6:** opaque identity không derive từ scope; envelope binding cho `*FactInvalidated`; fold algorithm "visible-valid-head per logical key" cho Current View; Current View KHÔNG BAO GIỜ authority; canonical policy identifier khai báo ĐÚNG MỘT NƠI; direct-predecessor-fact-targeting cho `supersedes_fact_ref`; **bốn bài học riêng từ C4–C6 correction:** (1) KHÔNG circular reference giữa Attempt và ExecutionResult; (2) attempt identity TÁCH BIỆT khỏi logical result key; (3) `attempt_outcome = PROCESSED` CHỈ ghi SAU KHI computation đã hoàn tất trọn vẹn; (4) `FAILED_BEFORE_RESULT` tường minh RETRYABLE. **Logical result key = `submission_request_id`, KHÔNG `order_id`** — preserved, KHÔNG đổi trong correction này.

**v0.3 — second bounded correction, đóng `C7-DELTA-MAJ-01` (consolidated Review A + Independent Review B findings trên baseline v0.2):** logical computation key cũ `(submission_request_id, observation_cursor)` KHÔNG phân biệt được authoritatively giữa initial computation/authorized correction/illegal rerun tại cursor mới/orphan Observation — vì một cursor MỚI tự nhiên tạo một logical key MỚI mà KHÔNG chứng minh một computation MỚI thực sự được authorize. Sửa: thêm `ExecutionResultComputation` (entity MỚI, §2) — identity authoritative đại diện ĐÚNG MỘT authorized computation lifecycle, `computation_purpose ∈ {INITIAL, CORRECTION}`. INITIAL: tối đa MỘT computation cho mỗi `submission_request_id`, BẤT KỂ cursor khác nhau — retry tại cursor khác KHÔNG tạo computation thứ hai, deterministic conflict. CORRECTION: bắt buộc `predecessor_execution_result_ref` + `correction_authorization_ref` (trỏ `ExecutionResultFactInvalidated` targeting predecessor), tối đa MỘT correction trực tiếp cho mỗi predecessor (cấm fork). `PaperExecutionObservation` logical identity nay = `execution_result_computation_id` (KHÔNG còn `(submission_request_id, cursor)`) — một computation → zero hoặc một Observation. Thứ tự corrected: `ExecutionResultComputationAuthorized` → computation hoàn tất → Observation → Attempt PROCESSED → Result. Cursor vẫn immutable computation context/replay evidence, KHÔNG còn tự authorize computation mới. Bounded — KHÔNG đổi `C7-MAJ-02`/`C7-MAJ-03`/`C7-MAJ-04` đã đóng, Result logical key (`submission_request_id`), Result correction direct-predecessor lineage, Fill logical key, full-Fill boundary, no cross-stream atomicity, Position non-authority, C1–C6 semantics, PAPER-only boundary.

**Phạm vi bounded tường minh:** KHÔNG author Fill/Position/Replay Event (file riêng). KHÔNG author Live behavior, exchange API payload, external order ID, routing/adapter, cancellation/replacement protocol. KHÔNG venue-specific rejection taxonomy. KHÔNG partial-fill semantics. KHÔNG fee/slippage/PnL/accounting. KHÔNG general workflow/saga/command infrastructure — `ExecutionResultComputationAuthorized` là một domain authorization fact, KHÔNG một orchestration step. KHÔNG author simulation algorithm thực tế. KHÔNG cross-stream atomic transaction. KHÔNG redefine Order/Execution Intent/Risk contract. KHÔNG sửa `order.md`/`execution-intent.md`/`risk.md`/`decision.md`/`trade-intent.md`/C1–C6/ADR/Constitution.

## 1. PaperExecutionObservation — `kind: entity`

```yaml
id: paper-execution-observation
kind: entity
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Bản ghi authoritative, bất biến, DURABLE của MỘT lần bounded PAPER simulation computation — pin
  chính xác simulation evidence identity VÀ output cùng lúc, gắn CHÍNH XÁC một
  ExecutionResultComputation (§2) đã authorized. ExecutionResult (§8) KHÔNG BAO GIỜ tự computation/
  reinterpret result_type — CHỈ copy nguyên vẹn từ Observation visible-valid mà nó reference. Đóng
  `C7-MAJ-01`/`C7-DELTA-MAJ-01`. KHÔNG author algorithm simulation thực tế.
invariants:
  - "execution_observation_id là opaque, globally unique, gán tại PaperExecutionObservationRecorded — KHÔNG derive từ execution_result_computation_id/submission_request_id/observation_cursor hay bất kỳ field scope nào. Bất biến."
  - "**v0.3 (đóng C7-DELTA-MAJ-01):** Logical identity = `execution_result_computation_id` (KHÔNG còn `(submission_request_id, observation_cursor)`) — một ExecutionResultComputation (§2) → zero hoặc một PaperExecutionObservation (§11)."
  - "Same execution_result_computation_id + same observation_cursor + same evidence bundle (simulation_policy_ref/simulation_configuration_ref/simulation_build_ref/deterministic_input_ref) + same output → idempotent reuse execution_observation_id đã tồn tại — computation PHẢI deterministic."
  - "Same execution_result_computation_id + observation_cursor KHÁC → deterministic conflict — computation_cursor đã bất biến kể từ khi ExecutionResultComputation authorized (§2), MỘT Observation KHÔNG được đổi cursor cho CÙNG computation identity (Scenario C, §19)."
  - "Same execution_result_computation_id + evidence HOẶC output KHÁC (cùng cursor) → deterministic conflict, reject khi append — KHÔNG silently overwrite (Scenario D, §19)."
  - "result_type = EXECUTED: executed_quantity/execution_price/price_currency BẮT BUỘC có mặt, finite, strictly positive (executed_quantity CHÍNH XÁC bằng order_quantity), price_currency CHÍNH XÁC bằng TradableListing quote currency. result_type = NOT_EXECUTED: executed_quantity/execution_price/price_currency TUYỆT ĐỐI ABSENT."
  - "Observation KHÔNG có correction lineage riêng (§11) — mỗi ExecutionResultComputation sinh ĐÚNG MỘT Observation immutable, append-only. Correction result_type dùng MỘT ExecutionResultComputation(CORRECTION) MỚI (§2), sinh Observation MỚI HOÀN TOÀN ĐỘC LẬP (execution_observation_id khác, KHÔNG supersedes_fact_ref — vì KHÔNG cùng logical identity, computation identity khác nhau tự nhiên tách biệt) — Observation cũ vẫn historically resolvable nguyên vẹn."
schema:
  execution_observation_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  execution_result_computation_id: {type: string, required: true, description: "v0.3, đóng C7-DELTA-MAJ-01 — logical identity, ref: execution-result-computation (§2)"}
  order_id: {type: string, required: true, ref: order}
  submission_request_id: {type: string, required: true, description: "PHẢI BẰNG HỆT execution_result_computation_id's Computation.submission_request_id (§6)"}
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
  observation_cursor: {type: object, required: true, description: "PHẢI BẰNG HỆT execution_result_computation_id's Computation.computation_cursor (§6) — Replay Cursor hợp lệ, TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1"}
  simulation_policy_ref: {type: string, required: true, description: "opaque versioned artifact ref — trục thứ nhất"}
  simulation_configuration_ref: {type: string, required: true, description: "opaque versioned artifact ref — trục thứ hai"}
  simulation_build_ref: {type: string, required: true, description: "opaque versioned artifact ref — trục thứ ba"}
  deterministic_input_ref: {type: string, required: true, description: "opaque versioned artifact ref — trục thứ tư"}
  result_type: {type: enum, values: [EXECUTED, NOT_EXECUTED], required: true}
  executed_quantity: {type: decimal, required: false, description: "BẮT BUỘC khi result_type=EXECUTED; TUYỆT ĐỐI ABSENT khi NOT_EXECUTED"}
  execution_price: {type: decimal, required: false, description: "BẮT BUỘC khi result_type=EXECUTED; TUYỆT ĐỐI ABSENT khi NOT_EXECUTED"}
  price_currency: {type: string, required: false, description: "BẮT BUỘC khi result_type=EXECUTED; TUYỆT ĐỐI ABSENT khi NOT_EXECUTED"}
events_emitted: [PaperExecutionObservationRecorded]
events_consumed: []
commands: []
queries: []
```

## 2. ExecutionResultComputation — `kind: entity` (v0.3, MỚI, đóng `C7-DELTA-MAJ-01`)

```yaml
id: execution-result-computation
kind: entity
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Bản ghi authoritative, bất biến, đại diện ĐÚNG MỘT authorized Execution Result computation
  lifecycle: ExecutionResultComputation → PaperExecutionObservation → ExecutionResultProcessingAttempt
  → ExecutionResult. Computation identity — KHÔNG cursor — quyết định authorization VÀ idempotency.
  KHÔNG author workflow/saga/command infrastructure — CHỈ pin identity/authorization binding fact.
invariants:
  - "execution_result_computation_id là opaque, globally unique, gán tại ExecutionResultComputationAuthorized — KHÔNG derive từ submission_request_id/order_id/computation_cursor/predecessor_execution_result_ref. Bất biến."
  - "computation_purpose = INITIAL: submission_request_id BẮT BUỘC; predecessor_execution_result_ref/correction_authorization_ref TUYỆT ĐỐI ABSENT."
  - "computation_purpose = CORRECTION: predecessor_execution_result_ref/correction_authorization_ref BẮT BUỘC; correction_authorization_ref PHẢI trỏ một ExecutionResultFactInvalidated (§9) targeting CHÍNH XÁC predecessor_execution_result_ref, visible TRƯỚC computation này authorized."
  - "Logical INITIAL key = submission_request_id — tại một cursor cho trước, tối đa MỘT ExecutionResultComputation(INITIAL) cho mỗi submission_request_id, BẤT KỂ computation_cursor/simulation evidence/process invocation khác nhau (§5, Scenario A)."
  - "Logical CORRECTION key = predecessor_execution_result_ref — tối đa MỘT ExecutionResultComputation(CORRECTION) trực tiếp cho mỗi predecessor ExecutionResult (§5, cấm correction fork, Scenario H)."
  - "computation_cursor bất biến sau khi authorized — retry với cursor KHÁC cho CÙNG execution_result_computation_id là deterministic conflict (Scenario C), KHÔNG tạo computation mới."
  - "ExecutionResultComputation KHÔNG có correction lineage riêng — append-only, immutable. Correction result_type dùng MỘT ExecutionResultComputation(CORRECTION) MỚI, HOÀN TOÀN ĐỘC LẬP identity, KHÔNG sửa/invalidate computation cũ."
schema:
  execution_result_computation_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  computation_purpose: {type: enum, values: [INITIAL, CORRECTION], required: true}
  order_id: {type: string, required: true, ref: order}
  submission_request_id: {type: string, required: true, description: "logical INITIAL key khi computation_purpose=INITIAL; PHẢI BẰNG HỆT predecessor's submission_request_id khi CORRECTION"}
  computation_cursor: {type: object, required: true, description: "Replay Cursor hợp lệ, TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1, bất biến sau khi authorized"}
  predecessor_execution_result_ref: {type: event_record_ref, required: false, description: "BẮT BUỘC khi computation_purpose=CORRECTION; TUYỆT ĐỐI ABSENT khi INITIAL — logical CORRECTION key"}
  correction_authorization_ref: {type: event_record_ref, required: false, description: "BẮT BUỘC khi computation_purpose=CORRECTION; TUYỆT ĐỐI ABSENT khi INITIAL — trỏ ExecutionResultFactInvalidated targeting predecessor_execution_result_ref"}
events_emitted: [ExecutionResultComputationAuthorized]
events_consumed: []
commands: []
queries: [GetExecutionResultComputationById, GetObservationForComputation]
```

**Queries §2 — non-authoritative convenience (§18):** `GetExecutionResultComputationById(K)` và `GetObservationForComputation(K)` hỗ trợ resolve trực tiếp Observation/Attempt/Result gắn một computation identity cụ thể — CHỈ tiện dụng cho recovery lookup/query/UI, KHÔNG BAO GIỜ thay thế direct authoritative fold khi domain validation (§18).

## 3. ExecutionResultProcessingAttempt — `kind: entity`

```yaml
id: execution-result-processing-attempt
kind: entity
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Bản ghi authoritative của MỘT lần thử xử lý execution-result — kể cả khi không dẫn tới
  ExecutionResult (INELIGIBLE/FAILED_BEFORE_RESULT). Tách biệt hoàn toàn khỏi ExecutionResult
  identity (§8), PaperExecutionObservation identity (§1), VÀ ExecutionResultComputation identity
  (§2).
invariants:
  - "execution_result_processing_attempt_id là opaque, globally unique, gán tại ExecutionResultProcessingAttemptRecorded — KHÔNG derive từ order_id/submission_request_id/execution_result_computation_id hay bất kỳ field scope nào."
  - "Logical result key = submission_request_id (KHÔNG order_id) — nhiều attempt (kể cả outcome khác nhau) CÓ THỂ tồn tại cùng logical key; idempotency scoped theo execution_result_processing_attempt_id (§13), KHÔNG theo logical key."
schema:
  execution_result_processing_attempt_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  order_id: {type: string, required: true, ref: order}
  submission_request_id: {type: string, required: true, description: "logical result key — xem §8"}
  execution_result_cursor: {type: object, required: true, description: "Replay Cursor hợp lệ, TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1 — xem §4 canonical envelope"}
events_emitted: [ExecutionResultProcessingAttemptRecorded]
events_consumed: []
commands: []
queries: []
```

## 4. Canonical event envelope — áp dụng cho mọi ExecutionResultComputation/PaperExecutionObservation/ExecutionResultProcessingAttempt/ExecutionResult event (§5–§9)

Mọi event trong tài liệu này là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). KHÔNG event nào trong tài liệu này thuộc `event_class: decision`. `computation_cursor`/`observation_cursor`/`execution_result_cursor` (CÙNG shape, tên khác theo entity sở hữu) là **PAYLOAD field**, TÁI SỬ DỤNG nguyên vẹn shape Replay Cursor Chapter 8 §8.5.1.

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
  causation_refs: {cardinality: "ExecutionResultComputationAuthorized: INITIAL zero-or-more (internal trigger); CORRECTION BẮT BUỘC chứa correction_authorization_ref's ExecutionResultFactInvalidated — KHÔNG rỗng. PaperExecutionObservationRecorded: BẮT BUỘC chứa ExecutionResultComputationAuthorized tương ứng (§5) — KHÔNG rỗng (v0.3, đóng C7-DELTA-MAJ-01). ExecutionResultProcessingAttemptRecorded: attempt_outcome=INELIGIBLE zero-or-more (không computation nào authorized); FAILED_BEFORE_RESULT BẮT BUỘC chứa ExecutionResultComputationAuthorized tương ứng — KHÔNG rỗng; PROCESSED BẮT BUỘC chứa PaperExecutionObservationRecorded tương ứng — KHÔNG rỗng. ExecutionResultRecorded: KHÔNG BAO GIỜ rỗng — PHẢI chứa CẢ ExecutionResultProcessingAttemptRecorded(PROCESSED) LẪN PaperExecutionObservationRecorded tương ứng, CỘNG ExecutionResultFactInvalidated của predecessor nếu là correction replacement. ExecutionResultFactInvalidated: KHÔNG BAO GIỜ rỗng."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3."}
  effective_time: {cardinality: "required — semantic khác theo event type, xem §5–§9."}
  decision_time: {cardinality: "PROHIBITED — event_class: decision KHÔNG áp dụng."}
  decision_context_cursor: {cardinality: "PROHIBITED (envelope-level) — cursor sống ở PAYLOAD."}
  market_time: {cardinality: "PROHIBITED — mọi event trong tài liệu này là bounded PAPER boundary observation authoritative (Chapter 5 §5.2)."}
  source_identity: {cardinality: "PROHIBITED — luôn phát sinh nội bộ (Phase 1, chưa author), KHÔNG BAO GIỜ từ external feed."}

computation_cursor / observation_cursor / execution_result_cursor (shape, đúng canonical Replay Cursor — Chapter 8 §8.5.1, TÁI SỬ DỤNG nguyên vẹn):
  recorded_time: <timestamp>
  input_contract_ref: {contract_id: <string>, contract_version: <string>}
  stream_registry_version: <string>
  lifecycle_frontier: {stream_id: <string>, position: {kind: <genesis | event>, sequence: <integer>}}
  stream_positions: {<stream_id>: <sequence>, ...}

subject_ref (ExecutionResultComputation, §2):
  context_id: execution-result-management
  subject_kind: entity
  subject_type: ExecutionResultComputation
  subject_id: <execution_result_computation_id — opaque, stable, xem §2>
  scope:
    submission_request_id: <string>

subject_ref (PaperExecutionObservation, §1):
  context_id: execution-result-management
  subject_kind: entity
  subject_type: PaperExecutionObservation
  subject_id: <execution_observation_id — opaque, stable, xem §1>
  scope:
    execution_result_computation_id: <string>

subject_ref (ExecutionResult — dùng cho ExecutionResultRecorded):
  context_id: execution-result-management
  subject_kind: entity
  subject_type: ExecutionResult
  subject_id: <execution_result_id — opaque, stable, xem §8>
  scope:
    submission_request_id: <string>

subject_ref (ExecutionResultProcessingAttempt, §3):
  context_id: execution-result-management
  subject_kind: entity
  subject_type: ExecutionResultProcessingAttempt
  subject_id: <execution_result_processing_attempt_id — opaque, stable, xem §3>
  scope:
    submission_request_id: <string>

event_types:
  ExecutionResultComputationAuthorized: EXECUTION_RESULT_COMPUTATION_AUTHORIZED
  PaperExecutionObservationRecorded: PAPER_EXECUTION_OBSERVATION_RECORDED
  ExecutionResultProcessingAttemptRecorded: EXECUTION_RESULT_PROCESSING_ATTEMPT_RECORDED
  ExecutionResultRecorded: EXECUTION_RESULT_RECORDED
  ExecutionResultFactInvalidated: EXECUTION_RESULT_FACT_INVALIDATED
```

`stream_ref`/`producer_ref` — Phase 1, chưa tồn tại.

**Relational invariants bắt buộc trên cursor** (Chapter 8 §8.5.2):
```text
computation_cursor.recorded_time ≤ ExecutionResultComputationAuthorized.recorded_time
observation_cursor.recorded_time ≤ PaperExecutionObservationRecorded.recorded_time
execution_result_cursor.recorded_time ≤ ExecutionResultRecorded.recorded_time
fact.recorded_time ≤ tương ứng cursor.recorded_time (mọi authoritative fact dùng cho authorization/processing)
```

## 5. `ExecutionResultComputationAuthorized` — `kind: event` (v0.3, MỚI, đóng `C7-DELTA-MAJ-01`)

Kế thừa envelope §4. Payload đặc thù:

```yaml
id: execution-result-computation-authorized
kind: event
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Fact AUTHORITATIVE DUY NHẤT thiết lập MỘT ExecutionResultComputation identity. "Authorized" nghĩa
  là domain eligibility (INITIAL, order.md §8b) HOẶC correction lineage (CORRECTION, targeting một
  predecessor ExecutionResult đã invalidate) đã cho phép computation này — KHÔNG ngụ ý Product Owner
  thủ công authorize từng runtime computation. KHÔNG author workflow/saga/command infrastructure.
invariants:
  - "payload.execution_result_computation_id PHẢI khớp đúng subject_ref.subject_id VÀ payload.submission_request_id PHẢI khớp đúng subject_ref.scope.submission_request_id."
  - "computation_purpose=INITIAL: CHỈ ghi SAU KHI eligible_for_execution_result_processing(order_id, computation_cursor) == true (order.md §8b) TRỌN VẸN TẠI computation_cursor. Nếu logical INITIAL key (submission_request_id) ĐÃ CÓ một ExecutionResultComputation(INITIAL) tồn tại, MỚI PHẢI resolve/reuse execution_result_computation_id đã tồn tại (Scenario A, §19) — TUYỆT ĐỐI KHÔNG tạo INITIAL thứ hai, KỂ CẢ computation_cursor/simulation evidence/process invocation khác (Scenario A/C, §19)."
  - "computation_purpose=CORRECTION: correction_authorization_ref PHẢI trỏ một ExecutionResultFactInvalidated (§9) visible TRƯỚC khi event này ghi, targeting CHÍNH XÁC predecessor_execution_result_ref. predecessor_execution_result_ref PHẢI là visible-valid-head TRỰC TIẾP (ngay trước khi bị invalidate) cho logical result key liên quan — KHÔNG được target một fact ĐÃ bị supersede trước đó (Scenario G, §19). Nếu logical CORRECTION key (predecessor_execution_result_ref) ĐÃ CÓ một ExecutionResultComputation(CORRECTION) trực tiếp tồn tại, một computation CORRECTION KHÁC targeting CÙNG predecessor PHẢI bị reject (Scenario H, §19 — cấm fork)."
  - "submission_request_id (khi CORRECTION) PHẢI BẰNG HỆT predecessor_execution_result_ref's submission_request_id — correction KHÔNG được đổi logical result key (Scenario G, §19)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của correction_authorization_ref (khi CORRECTION) — strict causal ordering (§12)."
  - "computation_cursor bất biến ngay từ event này — không sửa/thay thế sau khi authorized."
payload:
  execution_result_computation_id: {type: string, required: true}
  computation_purpose: {type: enum, values: [INITIAL, CORRECTION], required: true}
  order_id: {type: string, required: true}
  submission_request_id: {type: string, required: true}
  computation_cursor: {type: object, required: true, description: "cùng shape §4 — payload field, bất biến sau khi ghi"}
  predecessor_execution_result_ref: {type: event_record_ref, required: false, description: "BẮT BUỘC khi computation_purpose=CORRECTION; TUYỆT ĐỐI ABSENT khi INITIAL"}
  correction_authorization_ref: {type: event_record_ref, required: false, description: "BẮT BUỘC khi computation_purpose=CORRECTION; TUYỆT ĐỐI ABSENT khi INITIAL"}
```

## 6. `PaperExecutionObservationRecorded` — `kind: event`

Kế thừa envelope §4. Payload đặc thù:

```yaml
id: paper-execution-observation-recorded
kind: event
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Fact AUTHORITATIVE DUY NHẤT ghi nhận MỘT lần bounded PAPER simulation computation — thiết lập
  TOÀN BỘ scope + simulation evidence + output cùng lúc, BẤT BIẾN, gắn CHÍNH XÁC một
  ExecutionResultComputation (§2) đã authorized. Đóng `C7-MAJ-01`/`C7-DELTA-MAJ-01`.
invariants:
  - "payload.execution_observation_id PHẢI khớp đúng subject_ref.subject_id VÀ payload.execution_result_computation_id PHẢI khớp đúng subject_ref.scope.execution_result_computation_id."
  - "envelope.effective_time (observation_effective_time) = mặc định bằng observation_cursor.recorded_time."
  - "causation_refs PHẢI chứa ExecutionResultComputationAuthorized (§5) tương ứng — chứng minh computation đã authorized TRƯỚC khi Observation này được ghi (v0.3, đóng C7-DELTA-MAJ-01)."
  - "**v0.3 (đóng C7-DELTA-MAJ-01):** `payload.order_id`/`submission_request_id`/`observation_cursor` PHẢI BẰNG HỆT `execution_result_computation_id`'s ExecutionResultComputation.order_id/submission_request_id/computation_cursor (§2)."
  - "Ghi CHỈ SAU KHI bounded PAPER simulation computation đã hoàn tất trọn vẹn (§8a) — evidence bundle VÀ output đã xác định XONG trước khi ghi."
  - "Nếu logical identity execution_result_computation_id ĐÃ CÓ một Observation VALID tại thời điểm ghi, PaperExecutionObservationRecorded MỚI PHẢI resolve/reuse execution_observation_id đã tồn tại (cursor + evidence + output giống hệt — §1 idempotency) HOẶC bị reject (cursor/evidence/output khác) — TUYỆT ĐỐI KHÔNG tạo execution_observation_id thứ hai cho CÙNG computation (Scenario C/D, §19)."
  - "order_id/originating_execution_intent_id/originating_risk_evaluation_id/trade_intent_id/account_id/environment/instrument_selection_ref/direction/order_quantity/quantity_unit PHẢI khớp CHÍNH XÁC chuỗi visible-valid tại observation_cursor — KHÔNG dùng bất kỳ latest-state Current View nào làm input."
payload:
  execution_observation_id: {type: string, required: true}
  execution_result_computation_id: {type: string, required: true, description: "v0.3, đóng C7-DELTA-MAJ-01 — trỏ ExecutionResultComputation (§2) đã authorized"}
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
  observation_cursor: {type: object, required: true, description: "cùng shape §4 — payload field"}
  simulation_policy_ref: {type: string, required: true}
  simulation_configuration_ref: {type: string, required: true}
  simulation_build_ref: {type: string, required: true}
  deterministic_input_ref: {type: string, required: true}
  result_type: {type: enum, values: [EXECUTED, NOT_EXECUTED], required: true}
  executed_quantity: {type: decimal, required: false}
  execution_price: {type: decimal, required: false}
  price_currency: {type: string, required: false}
```

## 7. `ExecutionResultProcessingAttemptRecorded` — `kind: event`

Kế thừa envelope §4.

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
  - "**v0.3 (đóng C7-DELTA-MAJ-01) — bộ ba outcome, mỗi outcome pin computation/observation presence tường minh:**"
  - "attempt_outcome = INELIGIBLE: `eligible_for_execution_result_processing == false` (order.md §8b) — KHÔNG ExecutionResultComputation nào được authorized (eligibility fail TRƯỚC bước authorize). `execution_result_computation_id`/`execution_observation_id` TUYỆT ĐỐI ABSENT. reason_code = ORDER_RESULT_PROCESSING_INELIGIBLE."
  - "attempt_outcome = FAILED_BEFORE_RESULT: ExecutionResultComputation ĐÃ authorized (eligibility đã pass), NHƯNG lỗi kỹ thuật/domain boundary xảy ra TRONG lúc simulation computation, TRƯỚC KHI Observation kịp durably recorded. `execution_result_computation_id` BẮT BUỘC có mặt (trỏ computation đã authorized); `execution_observation_id` TUYỆT ĐỐI ABSENT. reason_code = EXECUTION_RESULT_ENGINE_COMPUTATION_BOUNDARY_ERROR. Tường minh RETRYABLE — resolve theo Gap recovery (§8a) TÁI SỬ DỤNG CHÍNH computation identity đó, KHÔNG tạo computation mới."
  - "attempt_outcome = PROCESSED: `execution_result_computation_id` VÀ `execution_observation_id` ĐỀU BẮT BUỘC có mặt — Observation CHÍNH XÁC đã persisted TRƯỚC. reason_code/checked_evidence_refs TUYỆT ĐỐI ABSENT. Ghi CHỈ SAU KHI PaperExecutionObservationRecorded (§6) tương ứng đã ghi nhận trọn vẹn — one-way sequence: Computation → Observation → Attempt PROCESSED → RỒI ExecutionResultRecorded.causation_refs trỏ ngược lại — KHÔNG atomic multi-event transaction."
  - "Idempotency scoped theo TỪNG execution_result_processing_attempt_id (§13) — KHÔNG theo logical result key."
payload:
  execution_result_processing_attempt_id: {type: string, required: true}
  order_id: {type: string, required: true}
  submission_request_id: {type: string, required: true}
  execution_result_cursor: {type: object, required: true, description: "cùng shape §4 — payload field"}
  attempt_outcome: {type: enum, values: [PROCESSED, INELIGIBLE, FAILED_BEFORE_RESULT], required: true}
  execution_result_computation_id: {type: string, required: false, description: "v0.3 — BẮT BUỘC khi attempt_outcome ∈ {PROCESSED, FAILED_BEFORE_RESULT}; TUYỆT ĐỐI ABSENT khi INELIGIBLE"}
  execution_observation_id: {type: string, required: false, description: "BẮT BUỘC khi attempt_outcome=PROCESSED; TUYỆT ĐỐI ABSENT khi khác"}
  reason_code: {type: enum, values: [ORDER_RESULT_PROCESSING_INELIGIBLE, EXECUTION_RESULT_ENGINE_COMPUTATION_BOUNDARY_ERROR], required: false}
  checked_evidence_refs: {type: array, items: event_record_ref, required: false}
```

## 8. `ExecutionResultRecorded` — `kind: event`

Kế thừa envelope §4. Payload đặc thù:

```yaml
id: execution-result-recorded
kind: event
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Fact AUTHORITATIVE cho MỘT execution-result determination — thiết lập TOÀN BỘ scope cùng lúc,
  BẤT BIẾN. `result_type` KHÔNG BAO GIỜ tự computation — CHỈ copy CHÍNH XÁC từ Observation visible-
  valid. CHỈ được phát khi ExecutionResultProcessingAttemptRecorded (§7) tương ứng có attempt_outcome
  = PROCESSED (§8a).
invariants:
  - "payload.execution_result_id PHẢI khớp đúng subject_ref.subject_id VÀ payload.submission_request_id PHẢI khớp đúng subject_ref.scope.submission_request_id."
  - "envelope.effective_time (result_effective_time) = mặc định bằng execution_result_cursor.recorded_time."
  - "causation_refs PHẢI chứa CẢ ExecutionResultProcessingAttemptRecorded (§7) tương ứng, attempt_outcome = PROCESSED, LẪN PaperExecutionObservationRecorded (§6) tương ứng."
  - "**v0.3 (đóng C7-DELTA-MAJ-01):** `payload.execution_result_computation_id` BẮT BUỘC, PHẢI BẰNG HỆT Attempt.execution_result_computation_id VÀ Observation.execution_result_computation_id (three-way equality)."
  - "`payload.execution_observation_id` BẮT BUỘC, PHẢI trỏ đúng PaperExecutionObservation (§1) visible-valid. `payload.result_type` PHẢI BẰNG HỆT Observation.result_type — TUYỆT ĐỐI KHÔNG tự tính lại/reinterpret."
  - "Logical result key = submission_request_id (KHÔNG đổi, preserved). Nếu key ĐÃ CÓ một ExecutionResult VALID (visible-valid-head, §10) tại thời điểm ghi, ExecutionResultRecorded MỚI PHẢI resolve/reuse execution_result_id đã tồn tại (payload giống hệt) HOẶC bị reject (payload khác, chưa invalidate predecessor)."
  - "order_id/originating_execution_intent_id/originating_risk_evaluation_id/trade_intent_id/account_id/environment/instrument_selection_ref/direction PHẢI khớp CHÍNH XÁC chuỗi visible-valid tại execution_result_cursor — Order visible-valid-head, submission_request_id chính là visible-valid OrderSubmissionRequested, Execution Intent/RiskEvaluation/TradeIntent/Decision đều valid (order.md §8b) — KHÔNG dùng latest-state Current View."
  - "`supersedes_fact_ref` TUYỆT ĐỐI ABSENT cho ExecutionResult gốc. BẮT BUỘC có mặt cho correction replacement, trỏ TRỰC TIẾP predecessor `ExecutionResultRecorded` fact. Khi có mặt: `execution_result_id` PHẢI KHÁC predecessor; `submission_request_id` PHẢI BẰNG HỆT predecessor; `execution_result_computation_id` PHẢI là một ExecutionResultComputation(CORRECTION) VỚI `predecessor_execution_result_ref` trỏ ĐÚNG predecessor này (v0.3, đóng C7-DELTA-MAJ-01 — thay cơ chế 'Observation mới tại cursor mới' cũ bằng computation identity tường minh)."
  - "Khi `supersedes_fact_ref` có mặt, `causation_refs` PHẢI CỘNG THÊM chứa chính `ExecutionResultFactInvalidated` targeting predecessor."
  - "result_type = EXECUTED: đúng MỘT Fill được kỳ vọng theo sau, VỚI economics copy CHÍNH XÁC từ Observation (fill.md §3a). result_type = NOT_EXECUTED: KHÔNG Fill nào được phép tồn tại VALID."
```

**§8a — Corrected event ordering (v0.3, đóng `C7-DELTA-MAJ-01`).** ExecutionResultRecorded CHỈ được phát SAU KHI toàn bộ chuỗi sau hoàn tất TRỌN VẸN theo ĐÚNG thứ tự:

```text
0. eligible_for_execution_result_processing(order_id, cursor) == true   (order.md §8b, KIỂM TRA cho
   INITIAL — CHO CORRECTION, thay bằng predecessor invalidation + correction_authorization_ref, §5)
   → NẾU false (INITIAL): ExecutionResultProcessingAttemptRecorded(attempt_outcome=INELIGIBLE) ghi —
     KHÔNG ExecutionResultComputationAuthorized, KHÔNG Observation, KHÔNG ExecutionResultRecorded
     nào phát (Scenario 2, §19).

1. ExecutionResultComputationAuthorized (§5) ghi — INITIAL (nếu (0) thỏa VÀ chưa có INITIAL nào cho
   submission_request_id này, Scenario A) HOẶC CORRECTION (nếu predecessor đã invalidate hợp lệ,
   Scenario F). Đây LÀ điểm authorization — domain eligibility/correction lineage đã cho phép
   computation này, KHÔNG phải Product Owner thủ công authorize từng lần.

2. Bounded PAPER simulation computation hoàn tất — copy nguyên vẹn scope, resolve bốn trục simulation
   evidence, xác định result_type (VÀ executed_quantity/execution_price/price_currency nếu EXECUTED).
   → NẾU lỗi kỹ thuật/domain boundary xảy ra TRONG lúc bước này (TRƯỚC khi Observation ghi ở bước 3):
     ExecutionResultProcessingAttemptRecorded(attempt_outcome=FAILED_BEFORE_RESULT,
     execution_result_computation_id = computation vừa authorized) ghi — KHÔNG Observation, KHÔNG
     ExecutionResultRecorded nào phát (Scenario 3, §19).

3. PaperExecutionObservationRecorded (§6) ghi — durable record, causation_refs trỏ
   ExecutionResultComputationAuthorized. Đây LÀ điểm "không quay đầu": SAU khi Observation ghi cho
   một computation identity, computation KHÔNG BAO GIỜ được rerun để lấy kết quả khác cho CÙNG
   execution_result_computation_id — mọi bước tiếp theo PHẢI dùng CHÍNH XÁC Observation này.

4. ExecutionResultProcessingAttemptRecorded(attempt_outcome=PROCESSED, execution_result_computation_id
   = computation, execution_observation_id = Observation vừa ghi) ghi NGAY SAU.

5. ExecutionResultRecorded phát — causation_refs trỏ CẢ Attempt PROCESSED LẪN Observation,
   execution_result_computation_id BẰNG HỆT cả hai, result_type COPY CHÍNH XÁC từ Observation
   (Scenario 1, §19).

Thứ tự bắt buộc: authorize → computation hoàn tất → Observation ghi → Attempt PROCESSED ghi →
ExecutionResult ghi. KHÔNG BAO GIỜ đảo ngược, KHÔNG atomic transaction giữa các bước.
```

**Recoverable append gap — HAI khoảng trống tường minh, resolve BẰNG computation identity (v0.3, đóng `C7-DELTA-MAJ-01`):**

```text
Gap A — Computation authorized, Observation ghi, Attempt chưa ghi:
  Recovery PHẢI: resolve K (GetExecutionResultComputationById); resolve ĐÚNG MỘT Observation cho K
  (GetObservationForComputation — KHÔNG search chỉ bằng submission_request_id, KHÔNG chọn Observation
  mới nhất, KHÔNG chọn cursor khác); append/reuse Attempt cho K/Observation; append/reuse
  ExecutionResultRecorded (Scenario B, §19).

Gap B — Computation + Observation + Attempt PROCESSED đã ghi, ExecutionResultRecorded chưa ghi:
  Recovery PHẢI: reuse K; reuse Observation; reuse Attempt PROCESSED; append hoặc reuse ĐÚNG MỘT
  ExecutionResultRecorded (Scenario E, §19).

Recovery TUYỆT ĐỐI KHÔNG được: search Observation chỉ bằng submission_request_id; chọn Observation
mới nhất; chọn một cursor khác; rerun simulation; tạo Observation thứ hai cho K; tạo một
ExecutionResultComputation(INITIAL) thứ hai cho submission_request_id đó.
```

```yaml
payload:
  execution_result_id: {type: string, required: true}
  execution_result_computation_id: {type: string, required: true, description: "v0.3, đóng C7-DELTA-MAJ-01 — PHẢI BẰNG HỆT Attempt/Observation"}
  execution_observation_id: {type: string, required: true, description: "trỏ PaperExecutionObservation (§1) visible-valid — nguồn authoritative CHO result_type"}
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
  order_quantity: {type: decimal, required: true, description: "= Order.quantity, copied"}
  quantity_unit: {type: string, required: true}
  result_type: {type: enum, values: [EXECUTED, NOT_EXECUTED], required: true, description: "COPY CHÍNH XÁC từ Observation.result_type"}
  execution_result_cursor: {type: object, required: true, description: "cùng shape §4 — payload field"}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho ExecutionResult gốc; BẮT BUỘC cho correction replacement — trỏ TRỰC TIẾP predecessor ExecutionResultRecorded fact"}
```

## 9. `ExecutionResultFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §4. `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: execution-result-fact-invalidated
kind: event
capability_id: execution-management
domain_context_id: execution-result-management
description: >
  Phủ định MỘT `ExecutionResultRecorded` lịch sử ĐÃ SAI. Correction lineage CHUẨN — replacement
  NHẬN execution_result_id MỚI, CÙNG logical result key (submission_request_id), replacement's
  `supersedes_fact_ref` trỏ TRỰC TIẾP predecessor. **v0.3:** event này chính là fact mà một
  ExecutionResultComputation(CORRECTION) tương lai PHẢI trỏ tới qua `correction_authorization_ref`
  (§2/§5) — event này KHÔNG tự nó authorize correction computation, CHỈ là bằng chứng invalidation
  mà computation authorization sau đó tham chiếu. KHÔNG cross-stream atomicity yêu cầu (đóng
  `C7-MAJ-03`, không đổi) — invalidation KHÔNG bắt buộc đi kèm FillFactInvalidated cùng lúc, xem
  `eligible_as_position_contributing_fill` (fill.md §6).
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref."
  - "invalidated_fact_ref PHẢI trỏ một ExecutionResultRecorded, CHƯA từng nhận invalidation khác — một fact chỉ bị invalidate đúng một lần. KHÔNG BAO GIỜ trỏ một ExecutionResultFactInvalidated khác."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này; replay TẠI/SAU thấy predecessor EXCLUDED khỏi head resolution (§10)."
  - "Mong đợi (không bắt buộc ngay lập tức) một ExecutionResultComputation(CORRECTION) MỚI (§2) với correction_authorization_ref = event này, predecessor_execution_result_ref = invalidated_fact_ref, RỒI một ExecutionResultRecorded replacement CÙNG submission_request_id, execution_result_id MỚI, supersedes_fact_ref TRỎ TRỰC TIẾP predecessor (§11)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 10. `ExecutionResultCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §6–§9.

```text
Trước khi ExecutionResultRecorded tồn tại cho một submission_request_id:
  → KHÔNG có ExecutionResultCurrentView row nào tồn tại
  → GetExecutionResultForSubmissionRequest trả về NOT_FOUND / ABSENT
```

**Fold algorithm (đúng pattern đã proven tại `risk.md` §7/`order.md` §8 Tầng 1 — explicit chain, KHÔNG "newest uninvalidated fact"):**

```text
1. Group mọi ExecutionResultRecorded theo logical result key = submission_request_id.
2. Trong một key, dựng chain TƯỜNG MINH theo supersedes_fact_ref: E1 (gốc) → E2 (supersedes_fact_ref
   = E1, TRỰC TIẾP) → ... (cấm fork/nhảy cóc — thực thi qua computation cardinality, §2/§5).
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
  từ §6–§9. KHÔNG authoritative — CHỈ query/UI, KHÔNG BAO GIỜ là input hợp lệ cho Fill derivation
  hay bất kỳ computation nào khác. "Newest Observation for Submission Request" KHÔNG BAO GIỜ được
  dùng làm authority (v0.3, đóng C7-DELTA-MAJ-01) — authoritative resolution PHẢI qua
  ExecutionResultComputation identity (§2/§18).
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

## 11. Correction lineage

**`ExecutionResultComputation` (§2) — append-only, KHÔNG correction lineage riêng:** một computation identity KHÔNG BAO GIỜ được sửa/invalidate — correction result_type dùng MỘT computation(CORRECTION) MỚI HOÀN TOÀN, KHÔNG sửa computation cũ.

**`PaperExecutionObservation` (§1) — append-only, logical identity = `execution_result_computation_id`, KHÔNG correction lineage riêng:** mỗi computation sinh ĐÚNG MỘT Observation; correction dùng Observation của computation(CORRECTION) MỚI, HOÀN TOÀN ĐỘC LẬP identity (KHÔNG `supersedes_fact_ref` — hai computation KHÁC NHAU, KHÔNG cùng logical identity để supersede).

**`ExecutionResultRecorded` — correction lineage CHUẨN, same-key replacement với `execution_result_id` MỚI (không đổi từ v0.2, đối xứng `risk.md` §10/`order.md` §9):**

```text
E1 (ExecutionResultRecorded, submission_request_id = S1, execution_result_computation_id = K1)
  → ExecutionResultFactInvalidated I1 targeting E1
  → ExecutionResultComputationAuthorized K2 (computation_purpose=CORRECTION,
    predecessor_execution_result_ref = E1, correction_authorization_ref = I1,
    submission_request_id = S1)
  → Observation O2 (execution_result_computation_id = K2)
  → Attempt A2 PROCESSED (execution_result_computation_id = K2)
  → E2 (ExecutionResultRecorded MỚI), execution_result_id KHÁC E1, CÙNG submission_request_id = S1,
    execution_result_computation_id = K2, E2.supersedes_fact_ref = E1 TRỰC TIẾP, E2.causation_refs
    CHỨA CẢ A2 LẪN O2 LẪN I1 → một visible-valid-head duy nhất
```

**Mười invariant bắt buộc (không đổi, đối xứng `risk.md` §10/`order.md` §9):** (1) gốc KHÔNG supersedes_fact_ref; (2) replacement BẮT BUỘC supersedes_fact_ref trỏ TRỰC TIẾP predecessor; (3) replacement CÙNG `submission_request_id`; (4) `causation_refs` chứa chính invalidation event, predecessor invalidate+visible TRƯỚC; (5) supersede đúng head hiện tại, cấm nhảy cóc; (6) tối đa một replacement trực tiếp, cấm fork; (7) replacement không visible trước invalidation; (8) append-only, `execution_result_id` cũ vẫn resolvable; (9) fact đã invalidate không tái sử dụng ngầm; (10) retry payload khác khi predecessor chưa invalidate vẫn là conflict.

**Năm điều kiện reject bổ sung cho correction computation (v0.3, đóng `C7-DELTA-MAJ-01`, §5):** (a) CORRECTION computation KHÔNG có predecessor invalidation hợp lệ → reject (Scenario G); (b) `correction_authorization_ref` targeting một Result KHÁC (không phải `predecessor_execution_result_ref`) → reject; (c) correction computation đổi `submission_request_id` so với predecessor → reject; (d) hai computation(CORRECTION) trực tiếp cùng target một predecessor → computation thứ hai reject (Scenario H, cấm fork); (e) correction computation targeting một predecessor KHÔNG phải current lineage predecessor (đã bị supersede trước đó) → reject.

**v0.2 preserved (đóng `C7-MAJ-03`) — KHÔNG ràng buộc cross-stream với Fill:** correction E1→E2 KHÔNG BẮT BUỘC đi kèm bất kỳ `FillFactInvalidated` nào cùng lúc — xem `eligible_as_position_contributing_fill` (fill.md §6). `S1 KHÔNG kế thừa sang S2`: nếu Submission Request S1 bị invalidate và S2 thay thế (order.md §9), Observation/ExecutionResult/Computation của S1 VẪN gắn với `submission_request_id = S1`, KHÔNG BAO GIỜ tự động áp dụng cho S2.

## 12. Time semantics và bitemporal correctness

- `effective_time` — required trên mọi event trong tài liệu này.
- `recorded_time` — recorded axis, universal.
- **v0.3 (đóng C7-DELTA-MAJ-01), chuỗi causal đầy đủ:** `OrderSubmissionRequested.recorded_time < ExecutionResultComputationAuthorized.recorded_time < PaperExecutionObservationRecorded.recorded_time < ExecutionResultProcessingAttemptRecorded(PROCESSED).recorded_time < ExecutionResultRecorded.recorded_time`.
- **Correction:** `ExecutionResultFactInvalidated.recorded_time < (correction) ExecutionResultComputationAuthorized.recorded_time`.
- Effective-time: `OrderSubmissionRequested.effective_time <= PaperExecutionObservationRecorded.observation_effective_time <= ExecutionResultRecorded.result_effective_time`.
- Mọi authoritative fact dùng cho computation authorization/processing PHẢI thỏa `fact.recorded_time <= computation_cursor.recorded_time <= ExecutionResultComputationAuthorized.recorded_time`.
- Replay tại cursor T chỉ thấy fact có `recorded_time ≤ T` — invalidation ghi SAU T KHÔNG visible tại T.
- `market_time` PROHIBITED xuyên suốt tài liệu này.

## 13. Canonical policy identifiers — nguồn duy nhất (context `execution-result-management`)

```yaml
initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS
execution_result_computation_initial_idempotency_policy: STABLE_SUBMISSION_REQUEST_AT_MOST_ONE_INITIAL_COMPUTATION
execution_result_computation_correction_idempotency_policy: STABLE_PREDECESSOR_AT_MOST_ONE_DIRECT_CORRECTION_COMPUTATION
paper_execution_observation_idempotency_policy: STABLE_COMPUTATION_IDENTITY_SAME_CURSOR_SAME_EVIDENCE_IS_IDEMPOTENT
execution_result_derivation_idempotency_policy: ONE_VALID_RESULT_PER_SUBMISSION_REQUEST
execution_result_processing_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT
execution_result_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE
```

**`initial_fact_correction_policy`** — áp dụng CHỈ cho `ExecutionResultProcessingAttemptRecorded` (§7), `PaperExecutionObservationRecorded` (§6), VÀ `ExecutionResultComputationAuthorized` (§5) — cả ba KHÔNG same-ID replacement, append-only.

**`execution_result_computation_initial_idempotency_policy`** (v0.3, MỚI, đóng `C7-DELTA-MAJ-01`) — logical INITIAL key = `submission_request_id`; tối đa MỘT ExecutionResultComputation(INITIAL), BẤT KỂ cursor. Retry cùng `submission_request_id` (INITIAL) + cùng payload → idempotent reuse; khác cursor/evidence → deterministic conflict.

**`execution_result_computation_correction_idempotency_policy`** (v0.3, MỚI, đóng `C7-DELTA-MAJ-01`) — logical CORRECTION key = `predecessor_execution_result_ref`; tối đa MỘT ExecutionResultComputation(CORRECTION) trực tiếp cho mỗi predecessor — cấm fork.

**`paper_execution_observation_idempotency_policy`** (v0.3, đóng `C7-DELTA-MAJ-01`) — logical identity = `execution_result_computation_id` (KHÔNG còn compound `(submission_request_id, cursor)`); same computation + same cursor + same evidence/output → idempotent; changed cursor/evidence/output → conflict. Đối xứng `risk_computation_idempotency_policy` (risk.md §12).

**`execution_result_derivation_idempotency_policy: ONE_VALID_RESULT_PER_SUBMISSION_REQUEST`** — không đổi, logical result key = `submission_request_id`. **KHÔNG unstated cross-stream atomicity.**

**`execution_result_processing_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT`** — không đổi.

**`execution_result_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE`** — xem §11.

## 14. Downstream reference contract (cho `fill.md`)

`fill.md` tham chiếu ExecutionResult/Observation qua ĐÚNG các field sau, KHÔNG hơn:

```yaml
execution_result_id: {type: string, required: true, ref: execution-result}
execution_observation_id: {type: string, description: "= §8, ref: paper-execution-observation — Fill PHẢI derive economics từ Observation này (đóng C7-MAJ-02)"}
execution_result_computation_id: {type: string, description: "= §8, ref: execution-result-computation (§2) — CÓ THỂ resolve TRANSITIVELY qua execution_result_id NẾU Fill cần traceability, KHÔNG bắt buộc field riêng trên Fill payload trừ khi cần cho self-explanation (v0.3)"}
order_id: {type: string, description: "= §8, ref: order"}
submission_request_id: {type: string, description: "= §8 — logical result key"}
originating_execution_intent_id: {type: string, description: "= §8, ref: execution-intent"}
originating_risk_evaluation_id: {type: string, description: "= §8, ref: risk"}
trade_intent_id: {type: string, description: "= §8, ref: trade-intent"}
account_id: {type: string, ref: account, description: "= §8"}
environment: {type: enum, values: [PAPER], description: "= §8"}
instrument_selection_ref: {type: object, description: "= §8 — {instrument_id, venue_id, listing_id}"}
direction: {type: enum, values: [LONG, SHORT], description: "= §8"}
order_quantity: {type: decimal, description: "= §8"}
quantity_unit: {type: string, description: "= §8"}
result_type: {type: enum, values: [EXECUTED, NOT_EXECUTED], description: "= §8 — COPY từ Observation, GUARANTEE: EXECUTED → đúng một Fill kỳ vọng; NOT_EXECUTED → KHÔNG Fill nào được phép"}
executed_quantity: {type: decimal, description: "= §1 (via execution_observation_id) — chỉ có mặt khi result_type=EXECUTED, nguồn CHO fill_quantity"}
execution_price: {type: decimal, description: "= §1 (via execution_observation_id) — chỉ có mặt khi result_type=EXECUTED, nguồn CHO fill_price"}
price_currency: {type: string, description: "= §1 (via execution_observation_id) — chỉ có mặt khi result_type=EXECUTED, nguồn CHO Fill price_currency"}
```

**Downstream authority rule:** `fill.md` PHẢI resolve mọi field trên TRỰC TIẾP từ authoritative ExecutionResult VÀ PaperExecutionObservation event stream (§6/§8) TẠI ĐÚNG cursor mà chính computation đó đang dùng — VÀ PHẢI xác nhận visible-valid-head (§10 fold, KHÔNG `ExecutionResultCurrentView` latest-state). Fill economics PHẢI COPY CHÍNH XÁC từ Observation, KHÔNG được độc lập quan sát/tính toán lại (đóng `C7-MAJ-02`, không đổi trong v0.3).

## 15. Explanation contract

```text
Explanation(execution_result_id) = deterministic render của {originating Order/Submission Request
scope, ExecutionResultComputation authorization (purpose, predecessor nếu CORRECTION), eligibility
result, processing attempt, PaperExecutionObservation evidence identity, result_type} — KHÔNG
computation mới, KHÔNG external lookup, KHÔNG dùng bất kỳ giá trị nào không có mặt trong §1/§2/§3/
§6/§8.
```

## 16. Prohibitions

**ExecutionResult/ExecutionResultComputation/PaperExecutionObservation/ExecutionResultProcessingAttempt KHÔNG được sở hữu:** Order/Execution Intent/RiskEvaluation/Trade Intent/Decision identity semantics; Fill/Position semantics; venue-specific rejection taxonomy; external order ID/exchange payload/routing/adapter behavior; simulation algorithm thực tế; fee/slippage/PnL/accounting; general workflow/saga/command infrastructure — `ExecutionResultComputationAuthorized` là domain authorization fact, KHÔNG một orchestration step; cross-stream atomic transaction; UI copy/natural-language generation infrastructure; database transaction/outbox/message-broker technology.

## 17. Ngoài phạm vi — defer

- Stream Registry/Input Contract implementation cụ thể.
- Cơ chế/thuật toán PAPER simulation cụ thể.
- Granular exception/technical-failure sub-taxonomy cho `FAILED_BEFORE_RESULT`.
- Correction lineage riêng cho `ExecutionResultComputation`/`PaperExecutionObservation`/`ExecutionResultProcessingAttempt` (append-only đủ — correction dùng computation(CORRECTION) MỚI thay vì sửa fact cũ).
- Implementation technology cho mọi recovery gap.
- Runtime worker ownership, transaction boundaries, retry/backoff, monitoring/escalation.
- Retention/resolvability horizon cho `ExecutionResultComputation` đã lâu.
- Fill/Position/Replay Event semantics — hoàn toàn ngoài phạm vi Domain Contract này.

## 18. Open questions ngoài phạm vi

- Cơ chế cụ thể generate `execution_result_computation_id`/`execution_result_id`/`execution_observation_id`/`execution_result_processing_attempt_id` — chưa quyết, Phase 1.
- Không đóng OQ-002/OQ-003.

## 19. Acceptance scenarios (v0.3 — phần liên quan trực tiếp `execution-result.md`; xem `fill.md`/`position.md`/`replay-event.md` cho phần còn lại của 36 scenario toàn Package 0.2-C7)

**Scenario 1 — Eligible result processing / durable Result observation:** Order visible-valid-head, một Submission Request valid, complete origin chain valid → `ExecutionResultComputationAuthorized`(INITIAL) → simulation computation hoàn tất → `PaperExecutionObservationRecorded` → Attempt `PROCESSED` → một `ExecutionResultRecorded` (result_type copy từ Observation, tất cả gắn CÙNG execution_result_computation_id).

**Scenario 2 — Ineligible result processing:** `eligible_for_execution_result_processing=false` → Attempt `INELIGIBLE` → KHÔNG ExecutionResultComputation, KHÔNG Observation, KHÔNG ExecutionResult, KHÔNG Fill.

**Scenario 3 — Failure and retry:** Computation K1 authorized → simulation fails TRƯỚC Observation → Attempt A1 (`FAILED_BEFORE_RESULT`, execution_result_computation_id=K1); retry TÁI SỬ DỤNG CHÍNH K1 (KHÔNG tạo computation mới) → Attempt A2 (CÙNG K1, `PROCESSED`) sau khi Observation ghi — HỢP LỆ.

**Scenario 4 — Result append gap (không đổi tên, cơ chế resolve computation-anchored):** xem Gap A (Scenario B)/Gap B (Scenario E) — recovery PHẢI resolve bằng computation identity, KHÔNG rerun simulation, KHÔNG duplicate (§8a).

**Scenario 6 — Not executed:** `result_type=NOT_EXECUTED` trên Observation → ExecutionResult copy `NOT_EXECUTED` → zero Fill, Position unchanged.

**Scenario 17 — Result correction EXECUTED→NOT_EXECUTED:** E1 (K1, `EXECUTED`) → F1 tồn tại → invalidate E1 (I1) → K2 CORRECTION (predecessor=E1, correction_authorization_ref=I1) → O2 (K2, `NOT_EXECUTED`) → E2 (K2) — F1 derived-ineligible NGAY LẬP TỨC (fill.md §6), KHÔNG bắt buộc `FillFactInvalidated` cùng lúc — chi tiết Position-side xem `position.md` Scenario 17, §9.

**Scenario 27 — Result correction to EXECUTED:** E1 (`NOT_EXECUTED`) → invalidate E1 (I1) → K2 CORRECTION → O2 (K2, `EXECUTED`) → E2 references O2 → deterministic full Fill từ O2 economics.

**Scenario 18 — Invalidated Submission Request:** Submission Request invalidate TRƯỚC khi result processing → `eligible_for_execution_result_processing=false` → KHÔNG eligible result processing nào, KHÔNG computation authorized.

**Scenario 19 — Order replacement:** O1 + S1 → invalidate O1 → O2 replacement → S1 gắn O1 KHÔNG còn hợp lệ cho processing MỚI → O2 cần Submission Request RIÊNG, rồi computation/ExecutionResult RIÊNG.

**Scenario 20 — Execution Intent withdrawn:** Execution Intent `WITHDRAWN` → `eligible_for_execution_result_processing=false` → result processing ineligible, KHÔNG computation authorized.

**Scenario 25 — Changed simulation evidence (đóng liên đới, xem Scenario D):** cùng `execution_result_computation_id`, evidence khác HOẶC output khác (cùng cursor) → deterministic conflict, reject khi append.

**Scenario 32 — Initial computation uniqueness (v0.3, MỚI, đóng `C7-DELTA-MAJ-01`):** INITIAL K1 tồn tại cho S1 → request một INITIAL computation KHÁC cho S1 (cùng HOẶC khác cursor) → deterministic conflict — KHÔNG tạo K2/O2/A2/E2.

**Scenario 33 — Same computation changed cursor (v0.3, MỚI):** K1 authorized tại C1 → attempt Observation cho K1 tại C2 (C2 != C1) → deterministic conflict — cursor bất biến sau khi computation authorized.

**Scenario 34 — Authorized correction (v0.3, MỚI, tổng quát hai chiều — xem Scenario 17/27 cho ví dụ cụ thể):** E1 invalidated bởi I1 → K2 CORRECTION references (predecessor_execution_result_ref=E1, correction_authorization_ref=I1) → O2 → A2 PROCESSED → E2 supersedes E1 → `E2.execution_result_computation_id=K2`, `E2.supersedes_fact_ref=E1`, `E2.execution_result_id != E1.execution_result_id`, `E2.submission_request_id = E1.submission_request_id` — hợp lệ.

**Scenario 35 — Unauthorized correction (v0.3, MỚI):** K2 CORRECTION KHÔNG có `correction_authorization_ref` trỏ một invalidation hợp lệ (hoặc trỏ sai predecessor/đổi submission_request_id/target một predecessor không phải current lineage) → reject.

**Scenario 36 — Correction fork (v0.3, MỚI):** K2 VÀ K3 đều CORRECTION trực tiếp targeting CÙNG E1 → computation thứ hai (K3, ghi sau) bị reject.
