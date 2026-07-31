---
id: execution-intent
title: Execution Intent
version: "0.2"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-01"
last_review: null
next_review: null
---

# Execution Intent

> **Vai trò của tài liệu này:** Domain Contract thứ hai của Package 0.2-C5 (Risk Gateway and Execution Intent Foundation) — định nghĩa **Execution Intent**, một request nội bộ PHÁT SINH từ một [`risk.md`](./risk.md) `result = APPROVED` (§9 risk.md), biểu thị bounded execution action đã được Risk Gateway authorize — TRƯỚC Order/Execution Engine. Draft, chưa Approved/Locked. Thuộc capability `risk-management` / context `risk-gateway` (đăng ký cùng `risk.md` tại [`context-map.yaml`](./context-map.yaml) — hai file, MỘT context, đúng quyết định tổ chức "hai concept riêng biệt, KHÔNG gộp làm một file" nhưng cùng thuộc phạm vi risk-gateway). Kiến trúc controlling: [`risk.md`](./risk.md) v0.1 Draft §9 (RiskEvaluation-to-Execution-Intent cardinality), [`trade-intent.md`](./trade-intent.md) v0.2 Draft (cấu trúc/pattern đã proven, ÁP DỤNG LẠI đúng semantic), Chapter 8 (Locked, envelope tiêu chuẩn — Execution Intent KHÔNG phải `event_class: decision`).

Execution Intent **KHÔNG phải**: một Order (không order type/limit price/stop price/exchange payload); exchange payload; routed instruction; venue acknowledgement; một Fill; một Position; bằng chứng execution đã xảy ra. Nó thuần túy là **request nội bộ** — biểu thị "Risk Gateway đã authorize bounded execution action X," CHƯA gửi tới Order/Execution Engine, CHƯA routed tới bất kỳ venue nào.

**`execution-intent-issued`/`execution-intent-status-changed`/`execution-intent-fact-invalidated`/`execution-intent-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây, tách biệt display name/`event_type`, cùng nguyên tắc mọi Domain Contract trước.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/C1–C4** (đóng trước, không chờ review round phát hiện): opaque identity không derive từ scope; `supersedes_fact_ref` có mặt ngay từ v0.1 trên `ExecutionIntentStatusChanged`; fold algorithm "visible-valid-head per slice"; Current View KHÔNG BAO GIỜ authority; canonical policy identifier khai báo ĐÚNG MỘT NƠI, độc lập theo context (dùng CHUNG context `risk-gateway` với `risk.md`, nhưng canonical identifier khai báo riêng, KHÔNG trùng lặp); origin-uniqueness/idempotency qua `originating_risk_evaluation_id` (đúng semantic đã proven tại `trade-intent.md` §1/§10 cho `originating_decision_id` — RiskEvaluation KHÔNG tự tuyên bố đã issue, đóng trước lớp lỗi `C4-MAJ-01`/`C4-MAJ-02`-style ngay từ v0.1); origin-validity rule cho C6 (đúng semantic đã proven tại `trade-intent.md` §6a cho `eligible_for_new_risk_evaluation`).

**Phạm vi bounded tường minh:** KHÔNG author Order acceptance/submission/routing (Package 0.2-C6). KHÔNG author Fill status/Position state (Package 0.2-C6–C7). KHÔNG định nghĩa order type/limit price/stop price/exchange payload. KHÔNG multi-instrument portfolio decomposition. Vocabulary action tối thiểu: `OPEN_EXPOSURE` — CLOSE/REDUCE KHÔNG author vì walking skeleton không cần (§13).

**v0.2 — bounded correction, đóng `C5-MAJ-04`/`C5-MAJ-06` (consolidated Review A + Independent Review B findings):** (a) `C5-MAJ-04` — `approved_quantity` PHẢI strictly positive (`> 0`) trên cả entity (§1) VÀ `ExecutionIntentIssued` precondition (§3) — vì nguồn duy nhất luôn là một RiskEvaluation `APPROVED` (risk.md §5c/§5e đã pin `approved_quantity > 0` cho v0.2), KHÔNG `OPEN_EXPOSURE` Execution Intent nào được phép mang zero quantity. (b) `C5-MAJ-06` — `eligible_for_new_order_creation` (§6a) mở rộng đủ NĂM điều kiện transitive (Execution Intent ISSUED, RiskEvaluation gốc visible-valid-head VÀ APPROVED, đúng risk_evaluation_id được tham chiếu, cùng trade_intent_id, VÀ `eligible_for_new_risk_evaluation` true) — đảm bảo transitively Decision→Trade Intent→RiskEvaluation→Execution Intent đều valid, KHÔNG chỉ kiểm tra cục bộ RiskEvaluation head. Bounded — không đổi lifecycle tối thiểu, idempotency, cross-stream atomicity boundary, hay C5/C6 boundary đã pin.

## 1. Execution Intent — `kind: entity`

```yaml
id: execution-intent
kind: entity
capability_id: risk-management
domain_context_id: risk-gateway
description: >
  Request nội bộ PHÁT SINH từ một RiskEvaluation APPROVED — pin ĐÚNG MỘT RiskEvaluation gốc
  (originating_risk_evaluation_id), ĐÚNG MỘT Trade Intent, ĐÚNG MỘT Account, ĐÚNG MỘT
  TradableListing — CÙNG Account/instrument selection/direction với RiskEvaluation gốc (§7
  invariant). Scope hoàn toàn bất biến sau khi đăng ký — KHÔNG có "mutable metadata" tách biệt
  (đối xứng TradeIntentIssued, trade-intent.md §3). Lifecycle tối thiểu (ISSUED/WITHDRAWN/EXPIRED,
  §4) là phần DUY NHẤT thay đổi qua thời gian.
invariants:
  - "execution_intent_id là opaque, globally unique trong toàn Ride, gán tại ExecutionIntentIssued — KHÔNG derive/resolve từ originating_risk_evaluation_id hay bất kỳ field scope nào. Bất biến, KHÔNG tái sử dụng cho subject khác (Chapter 6 §6.1)."
  - "MỘT Execution Intent originate từ ĐÚNG MỘT RiskEvaluation (originating_risk_evaluation_id, ref: risk), `result = APPROVED` — không multi-evaluation aggregation, đúng risk.md §9 cardinality."
  - "`originating_risk_evaluation_id` là UNIQUE KEY trên toàn bộ ExecutionIntentIssued VALID — tại một cursor cho trước, tối đa MỘT ExecutionIntentIssued VALID cho mỗi `originating_risk_evaluation_id` (§10 `execution_intent_derivation_idempotency_policy: ONE_VALID_INTENT_PER_ORIGINATING_RISK_EVALUATION`). Retry cùng origin + cùng payload → idempotent, trả về `execution_intent_id` đã tồn tại; retry cùng origin + payload KHÁC → deterministic conflict, reject."
  - "trade_intent_id/account_id/instrument_selection_ref/direction PHẢI BẰNG HỆT trade_evidence tương ứng của originating_risk_evaluation_id (risk.md §5b) — Execution Intent KHÔNG được tự chọn Trade Intent/Account/instrument/direction khác RiskEvaluation gốc đã pin (Scenario 18, risk.md §17)."
  - "approved_quantity/quantity_unit PHẢI BẰNG HỆT §5e của originating_risk_evaluation_id (risk.md §5e) — Execution Intent KHÔNG BAO GIỜ tự tính lại/thay đổi quantity."
  - "**v0.2 (đóng C5-MAJ-04):** `approved_quantity` PHẢI STRICTLY POSITIVE (`> 0`) — KHÔNG BAO GIỜ bằng 0 hay âm. Vì `originating_risk_evaluation_id` bắt buộc `result = APPROVED` (invariant trên), VÀ RiskEvaluation `APPROVED` bắt buộc `approved_quantity > 0` (risk.md §5c bước 12–13/§5e), một Execution Intent với `approved_quantity == 0` KHÔNG BAO GIỜ có thể tồn tại hợp lệ — KHÔNG `OPEN_EXPOSURE` Execution Intent nào được phép mang zero quantity."
  - "Execution Intent KHÔNG BAO GIỜ mutate Risk evidence — mọi field liên quan chỉ COPY từ RiskEvaluation gốc để tiện truy vấn, KHÔNG phải nguồn authoritative thứ hai; nguồn authoritative luôn là chính RiskEvaluation (risk.md §5)."
  - "Execution Intent KHÔNG tự authorize submission/routing dưới bất kỳ hình thức nào — `execution_action` chỉ là request nội bộ, KHÔNG phải quyết định gửi lệnh; order submission/routing hoàn toàn thuộc Package 0.2-C6 (chưa author)."
schema:
  execution_intent_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  originating_risk_evaluation_id: {type: string, required: true, ref: risk, description: "đúng một RiskEvaluation, result = APPROVED"}
  trade_intent_id: {type: string, required: true, ref: trade-intent, description: "= risk.md §5b trade_evidence.trade_intent_id (qua subject_ref.scope)"}
  account_id: {type: string, required: true, ref: account, description: "= risk.md §5b trade_evidence.account_id"}
  instrument_selection_ref:
    type: object
    required: true
    description: "= risk.md §5b trade_evidence.instrument_selection_ref — CÙNG shape strategy.md §5/§10"
    fields:
      instrument_id: {type: string, required: true}
      venue_id: {type: string, required: true}
      listing_id: {type: string, required: true}
  direction: {type: enum, values: [LONG, SHORT], required: true, description: "= risk.md §5b trade_evidence.direction — PHẢI khớp chính xác"}
  execution_action: {type: enum, values: [OPEN_EXPOSURE], required: true, description: "v0.1: chỉ OPEN_EXPOSURE — CLOSE/REDUCE deferred (§13), walking skeleton không cần"}
  approved_quantity: {type: decimal, required: true, description: "= risk.md §5e — STRICTLY POSITIVE (> 0), finite, KHÔNG tự tính lại (v0.2, đóng C5-MAJ-04)"}
  quantity_unit: {type: string, required: true, description: "= risk.md §5e"}
state_machine:
  initial_state: UNSEEN
  states: [UNSEEN, ISSUED, WITHDRAWN, EXPIRED]
  transitions:
    - {from: UNSEEN, to: ISSUED, caused_by: ExecutionIntentIssued}
    - {from: ISSUED, to: WITHDRAWN, caused_by: ExecutionIntentStatusChanged}
    - {from: ISSUED, to: EXPIRED, caused_by: ExecutionIntentStatusChanged}
  terminal_states: [WITHDRAWN, EXPIRED]
events_emitted: [ExecutionIntentIssued, ExecutionIntentStatusChanged, ExecutionIntentFactInvalidated]
events_consumed: []
commands: []
queries: []
```

**`UNSEEN` là notional initial state** — cùng convention xuyên suốt tài liệu. Lifecycle tối thiểu — chỉ đủ để C6 (Order, chưa author) xác định Execution Intent còn eligible cho Order creation hay không: `ISSUED` (mặc định, đủ điều kiện Order creation); `WITHDRAWN` (rút lại trước khi Order xử lý — lý do cụ thể thuộc Phase 1); `EXPIRED` (hết hiệu lực theo thời gian — chính sách hết hạn cụ thể Phase 1, §13). **KHÔNG author** `SUBMITTED`/`ACCEPTED`/`PARTIALLY_FILLED`/`FILLED`/`CANCELLED_BY_EXCHANGE`/`REJECTED_BY_EXCHANGE` — những state đó thuộc Package 0.2-C6–C7. `WITHDRAWN`/`EXPIRED` là terminal CHO FORWARD TRANSITION nhưng correctable append-only (§5, đóng trước lớp lỗi `C2-MAJ-02`/`C3-MAJ-02`-style, không chờ review round phát hiện) — `supersedes_fact_ref` có mặt ngay từ v0.1 trên `ExecutionIntentStatusChanged`.

## 2. Canonical event envelope — áp dụng cho mọi Execution Intent event (§3–§5)

Mọi event trong tài liệu này là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). KHÔNG event nào trong tài liệu này thuộc `event_class: decision` — dùng envelope tiêu chuẩn, KHÔNG `decision_time`/`decision_context_cursor`.

```yaml
envelope:
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2)
  event_contract_ref: {cardinality: required}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}             # khi Ride ghi nhận fact này
  subject_ref: {cardinality: "required — shape canonical, xem dưới. Trên ExecutionIntentFactInvalidated, PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate."}
  stream_ref: {cardinality: required}                # Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # Phase 1, chưa author
  correlation_id: {cardinality: "required — Execution Intent LUÔN thuộc một correlation flow tường minh (originating RiskEvaluation, xem §3)"}
  causation_refs: {cardinality: "ExecutionIntentIssued: KHÔNG BAO GIỜ rỗng, PHẢI chứa chính RiskEvaluationRecorded (risk.md §5) gốc. ExecutionIntentStatusChanged/ExecutionIntentFactInvalidated: KHÔNG BAO GIỜ rỗng."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3."}
  effective_time: {cardinality: "required — semantic khác theo event type, xem §3–§4 cho nội dung cụ thể."}
  market_time: {cardinality: "PROHIBITED — Execution Intent là request nội bộ authoritative, không phải quan sát trực tiếp venue (Chapter 5 §5.2)."}
  source_identity: {cardinality: "PROHIBITED — Execution Intent luôn phát sinh nội bộ từ Risk Gateway (Phase 1, chưa author), KHÔNG BAO GIỜ từ external feed."}

subject_ref (Execution Intent):
  context_id: risk-gateway
  subject_kind: entity
  subject_type: ExecutionIntent
  subject_id: <execution_intent_id — opaque, stable, xem §1>
  scope:
    originating_risk_evaluation_id: <string>
    account_id: <string>
    instrument_selection_ref: {instrument_id: <string>, venue_id: <string>, listing_id: <string>}

event_types:
  ExecutionIntentIssued: EXECUTION_INTENT_ISSUED
  ExecutionIntentStatusChanged: EXECUTION_INTENT_STATUS_CHANGED
  ExecutionIntentFactInvalidated: EXECUTION_INTENT_FACT_INVALIDATED
```

`stream_ref`/`producer_ref` — Phase 1, chưa tồn tại, cùng nguyên tắc defer xuyên suốt Package 0.2-B/C1–C5.

## 3. `ExecutionIntentIssued` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: execution-intent-issued
kind: event
capability_id: risk-management
domain_context_id: risk-gateway
description: >
  Fact AUTHORITATIVE cho việc phát MỘT Execution Intent — thiết lập TOÀN BỘ scope
  (originating_risk_evaluation_id, trade_intent_id, account_id, instrument_selection_ref, direction,
  execution_action, approved_quantity, quantity_unit) cùng lúc, BẤT BIẾN. `risk.md` KHÔNG có field
  nào tuyên bố "đã issue Execution Intent" — việc phát ExecutionIntentIssued được quyết định bởi
  Risk Gateway (Phase 1, chưa author) dựa trên `result = APPROVED` (risk.md §5e) VÀ derivation
  idempotency check (§10 dưới). KHÔNG có supersedes_fact_ref — subject này KHÔNG BAO GIỜ có
  same-ID replacement (§5 giải thích lý do).
invariants:
  - "payload.execution_intent_id PHẢI khớp đúng subject_ref.subject_id VÀ toàn bộ scope field PHẢI khớp subject_ref.scope."
  - "causation_refs PHẢI trỏ chính xác RiskEvaluationRecorded (risk.md §5) của originating_risk_evaluation_id — chứng minh RiskEvaluation đã tồn tại VÀ `result = APPROVED` trước khi Execution Intent phát."
  - "direction/account_id/instrument_selection_ref PHẢI khớp CHÍNH XÁC trade_evidence tương ứng của originating_risk_evaluation_id (risk.md §5b) — KHÔNG được đảo/tự chọn khác RiskEvaluation gốc (Scenario 18, risk.md §17)."
  - "approved_quantity/quantity_unit PHẢI khớp CHÍNH XÁC §5e của originating_risk_evaluation_id (risk.md §5e) — KHÔNG tự tính lại."
  - "**v0.2 (đóng C5-MAJ-04):** `payload.approved_quantity` PHẢI STRICTLY POSITIVE (`> 0`) — precondition bắt buộc TRƯỚC khi ghi. RiskEvaluation `result = REJECTED`/`QUANTITY_ROUNDS_TO_ZERO` (risk.md §5c bước 12) KHÔNG BAO GIỜ có `approved_quantity`, do đó KHÔNG BAO GIỜ có thể làm `causation_refs` hợp lệ cho ExecutionIntentIssued — chỉ `result = APPROVED` (đảm bảo `approved_quantity > 0`, risk.md §5c bước 13) mới hợp lệ làm nguồn. Vi phạm (approved_quantity == 0 hoặc âm) là invalid ExecutionIntentIssued, PHẢI bị từ chối khi append — KHÔNG `OPEN_EXPOSURE` Execution Intent nào được phép mang zero quantity."
  - "envelope.effective_time PHẢI thỏa `effective_time >= originating RiskEvaluationRecorded.risk_evaluation_time` — một Execution Intent KHÔNG BAO GIỜ effective TRƯỚC RiskEvaluation gốc của nó. Mặc định bằng nhau trừ khi backfill lịch sử tường minh pin giá trị MUỘN HƠN (KHÔNG BAO GIỜ sớm hơn) — vi phạm là invalid ExecutionIntentIssued, PHẢI bị từ chối khi append (Scenario 17, risk.md §17)."
  - "envelope.recorded_time PHẢI `> originating RiskEvaluationRecorded.recorded_time` (strict causal ordering — Execution Intent PHẢI được ghi nhận SAU RiskEvaluation gốc của nó, KHÔNG BAO GIỜ đồng thời hay trước)."
  - "trước khi ghi, PHẢI kiểm tra `originating_risk_evaluation_id` chưa có ExecutionIntentIssued VALID nào khác (§1 uniqueness invariant) — nếu đã có VÀ payload giống hệt, đây là idempotent retry (KHÔNG ghi bản ghi mới, trả về `execution_intent_id` đã tồn tại thay vì phát event mới); nếu đã có VÀ payload khác, đây là deterministic conflict (reject, KHÔNG ghi)."
  - "KHÔNG có field supersedes_fact_ref trong payload — subject này KHÔNG hỗ trợ same-ID correction replacement (§5: correction luôn invalidate, KHÔNG replacement — vì originating_risk_evaluation_id KHÔNG BAO GIỜ đổi sau khi issue)."
payload:
  execution_intent_id: {type: string, required: true}
  originating_risk_evaluation_id: {type: string, required: true}
  trade_intent_id: {type: string, required: true}
  account_id: {type: string, required: true}
  instrument_selection_ref:
    instrument_id: {type: string, required: true}
    venue_id: {type: string, required: true}
    listing_id: {type: string, required: true}
  direction: {type: enum, values: [LONG, SHORT], required: true}
  execution_action: {type: enum, values: [OPEN_EXPOSURE], required: true}
  approved_quantity: {type: decimal, required: true}
  quantity_unit: {type: string, required: true}
```

## 4. `ExecutionIntentStatusChanged` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: execution-intent-status-changed
kind: event
capability_id: risk-management
domain_context_id: risk-gateway
description: >
  Fact AUTHORITATIVE cho một operational status transition của Execution Intent (§1 state_machine)
  — ISSUED→WITHDRAWN, ISSUED→EXPIRED. Cả hai terminal CHO FORWARD TRANSITION (§1) — nhưng
  correctable append-only qua same-slice replacement, supersedes_fact_ref có mặt ngay từ v0.1.
invariants:
  - "new_status PHẢI là một transition hợp lệ theo state_machine §1 từ current_status hiện tại — current_status resolve theo fold algorithm §6 (visible-valid-head per slice, total-order effective_time ASC/recorded_time ASC/event_id ASC)."
  - "new_status = WITHDRAWN hoặc EXPIRED trên valid lineage hiện hành KHÔNG được có ExecutionIntentStatusChanged forward transition tiếp theo cho cùng execution_intent_id (§1 terminal_states) — ràng buộc FORWARD LIFECYCLE, không áp dụng cho correction record."
  - "Một WITHDRAWN/EXPIRED fact ghi SAI vẫn correctable qua ExecutionIntentFactInvalidated + same-slice ExecutionIntentStatusChanged replacement (§5, cùng (execution_intent_id, effective_time) slice, supersedes_fact_ref trỏ đúng fact bị invalidate) — correction KHÔNG bị chặn bởi terminality. Fold algorithm (§6) PHẢI recompute current_status từ valid corrected lineage."
  - "envelope.effective_time = thời điểm status transition này thực sự có hiệu lực."
  - "Execution Intent CHỈ eligible cho Order creation MỚI (Package 0.2-C6, chưa author) khi current_status = ISSUED tại effective_time liên quan — WITHDRAWN/EXPIRED CẤM Order creation mới; đây là RÀNG BUỘC lên Domain Contract tương lai (Order, chưa author), execution-intent.md chỉ PIN quy tắc, không tự enforce vì chưa có consumer nào tồn tại."
  - "supersedes_fact_ref VẮNG MẶT cho forward transition bình thường; BẮT BUỘC cho same-slice correction replacement — khi có mặt, PHẢI trỏ đúng ExecutionIntentStatusChanged bị ExecutionIntentFactInvalidated target, cùng subject/effective_time (§5)."
payload:
  execution_intent_id: {type: string, required: true}
  new_status: {type: enum, values: [WITHDRAWN, EXPIRED], required: true}
  reason: {type: string, required: false}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho forward transition bình thường; BẮT BUỘC cho same-slice correction replacement — xem invariants và §5"}
```

## 5. `ExecutionIntentFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2. `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: execution-intent-fact-invalidated
kind: event
capability_id: risk-management
domain_context_id: risk-gateway
description: >
  Phủ định MỘT fact lịch sử cụ thể ĐÃ SAI của Execution Intent. Hai hành vi khác nhau theo target:
  (a) target = ExecutionIntentIssued → KHÔNG BAO GIỜ có replacement dưới cùng execution_intent_id
  (scope hoàn toàn bất biến — originating_risk_evaluation_id không đổi, một Execution Intent sai
  thực chất nghĩa là "RiskEvaluation này không nên tạo Execution Intent," KHÔNG phải "Execution
  Intent sai cần sửa nội dung") — correction thực tế là invalidate, KHÔNG đăng ký execution_intent_id
  mới cho cùng RiskEvaluation (một RiskEvaluation APPROVED tối đa một Execution Intent, risk.md §9
  — nếu Execution Intent gốc sai, RiskEvaluation gốc thường cũng cần xem lại qua risk.md §6/§10,
  KHÔNG tự động ở đây); (b) target = ExecutionIntentStatusChanged → same-slice replacement HỢP LỆ,
  đúng correction lineage chuẩn (§6), kể cả khi giá trị bị invalidate là WITHDRAWN/EXPIRED.
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref."
  - "invalidated_fact_ref PHẢI trỏ một ExecutionIntentIssued hoặc ExecutionIntentStatusChanged, CHƯA từng nhận invalidation khác — một fact chỉ bị invalidate đúng một lần. KHÔNG BAO GIỜ trỏ một ExecutionIntentFactInvalidated khác (cấm invalidation-of-invalidation)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead)."
  - "Target = ExecutionIntentIssued: sau invalidation, execution_intent_id đó VĨNH VIỄN TERMINALLY_INVALID (§6) — KHÔNG BAO GIỜ có replacement dưới cùng ID."
  - "Target = ExecutionIntentStatusChanged: mong đợi (không bắt buộc ngay lập tức) một ExecutionIntentStatusChanged replacement CÙNG execution_intent_id VÀ cùng effective_time slice, supersedes_fact_ref = event này (§6)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 6. `ExecutionIntentCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §3–§5.

```text
Trước khi ExecutionIntentIssued tồn tại cho một execution_intent_id:
  → KHÔNG có ExecutionIntentCurrentView row nào tồn tại
  → GetCurrentExecutionIntent trả về NOT_FOUND / ABSENT
```

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION`. Khi `PENDING_CORRECTION`, `pending_correction_class` BẮT BUỘC có mặt (đúng pattern đã proven tại `trade-intent.md` §6):

```text
view_state = VALID              → pending_correction_class: CẤM (phải absent)
view_state = PENDING_CORRECTION → pending_correction_class: BẮT BUỘC

target = ExecutionIntentIssued (invalidate, không bao giờ replacement) → pending_correction_class = TERMINAL_SCOPE_INVALIDATION
target = ExecutionIntentStatusChanged (invalidate, chờ same-slice replacement) → pending_correction_class = AWAITING_SAME_SUBJECT_REPLACEMENT
```

**Fold algorithm (v0.1, "visible-valid-head per slice" — MỘT quy tắc chung, đúng pattern đã proven tại `trade-intent.md` §6):**

```text
1. Group mọi fact theo correction lineage/effective-time slice — mỗi (execution_intent_id, effective_time)
   là một slice riêng.
2. Với mỗi slice, resolve ExecutionIntentFactInvalidated visibility tại cursor (recorded_time <= cursor).
3. Loại trừ khỏi lineage bất kỳ fact nào đã có invalidation visible tại cursor.
4. Chọn head hợp lệ (visible valid head) của slice: fact CHƯA bị invalidate visible, hoặc
   replacement mới nhất (chuỗi supersedes_fact_ref, CHỈ áp dụng cho ExecutionIntentStatusChanged,
   §5) CHƯA bị invalidate visible.
5. NẾU slice issuance bị invalidate visible → toàn view chuyển PENDING_CORRECTION,
   pending_correction_class = TERMINAL_SCOPE_INVALIDATION, DỪNG.
6. NẾU issuance hợp lệ, tiếp tục fold ExecutionIntentStatusChanged: một slice status bị invalidate
   chưa có replacement visible KHÔNG đóng góp fact nào (không "giữ giá trị cũ") — fold dùng head
   hợp lệ của slice effective_time gần nhất trước đó.
7. Tổng hợp mọi visible-valid-head còn lại, total-order: effective_time ASC, recorded_time ASC,
   event_id ASC — rồi mới lifecycle fold → current_status.
```

```yaml
id: execution-intent-current-view
kind: read_model
capability_id: risk-management
domain_context_id: risk-gateway
description: >
  Projection tiện dụng: status "hiện tại" (latest-state, KHÔNG cursor-addressable theo mặc định)
  của một Execution Intent, rebuild được từ §3–§5. KHÔNG authoritative — CHỈ query/UI, KHÔNG BAO GIỜ
  là input hợp lệ cho Order (Package 0.2-C6, chưa author) hay computation nào khác, kể cả khi
  "trông giống" cùng giá trị. Downstream field PHẢI resolve qua authoritative Execution Intent
  event stream (`ref: execution-intent`) TẠI CÙNG cursor mà computation đó đang dùng (§11). Cache
  chỉ chấp nhận khi ĐỒNG THỜI cursor-addressable VÀ provably equivalent với authoritative
  reconstruction.
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho Order hay bất kỳ computation nào khác — CHỈ query/UI."
  - "view_state PHẢI đúng theo Bước 4–5 của fold algorithm — issuance lineage head quyết định."
  - "pending_correction_class BẮT BUỘC có mặt khi view_state = PENDING_CORRECTION; CẤM có mặt khi view_state = VALID."
  - "current_status PHẢI recompute đúng theo Bước 6–7 — một WITHDRAWN/EXPIRED fact đã invalidate mà chưa có replacement visible KHÔNG được góp phần vào current_status."
schema:
  execution_intent_id: {type: string, required: true}
  scope: {originating_risk_evaluation_id: string, trade_intent_id: string, account_id: string, instrument_selection_ref: object, direction: string, execution_action: string, approved_quantity: string, quantity_unit: string, required: true, description: "chỉ có mặt khi view_state = VALID"}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  pending_correction_class: {type: enum, values: [AWAITING_SAME_SUBJECT_REPLACEMENT, TERMINAL_SCOPE_INVALIDATION], required: false}
  current_status: {type: enum, values: [ISSUED, WITHDRAWN, EXPIRED], required: false, description: "chỉ có mặt khi view_state = VALID"}
  last_recorded_time: timestamp
queries: [GetCurrentExecutionIntent, GetExecutionIntentHistory]
```

### 6a. Origin-validity — `eligible_for_new_order_creation` (v0.2, đóng `C5-MAJ-06` — complete transitive origin-chain, mở rộng yêu cầu tương đương `C4-MAJ-06`)

**Vai trò:** một rule normative, derived, deterministic — trả lời "Execution Intent này còn đủ điều kiện cho Order creation MỚI (Package 0.2-C6, chưa author) hay không," xét TRỌN VẸN chuỗi transitive validity từ Decision → Trade Intent → RiskEvaluation → Execution Intent, KHÔNG CHỈ tình trạng lifecycle cục bộ của chính Execution Intent. Đánh giá TẠI cùng cursor C:

```text
eligible_for_new_order_creation(execution_intent_id, C) =
      ExecutionIntent.current_status(C) == ISSUED                                              (§6, visible-valid-head fold TẠI C)
  AND originating RiskEvaluation resolve đúng visible-valid-head cho logical Risk computation key
      của nó TẠI C, VÀ head đó có result = APPROVED                                             (risk.md §7 GetRiskEvaluationForComputation)
  AND visible-valid-head đó CHÍNH LÀ risk_evaluation_id mà Execution Intent này tham chiếu
      (originating_risk_evaluation_id) — KHÔNG phải một risk_evaluation_id KHÁC đã supersede nó
  AND RiskEvaluation đó tham chiếu ĐÚNG CÙNG trade_intent_id với Execution Intent này
      (risk.md §1 trade_intent_id — KHÔNG derivation mismatch)
  AND eligible_for_new_risk_evaluation(trade_intent_id, C) == true                              (trade-intent.md §6a)
```

**Năm điều kiện — KHÔNG rút gọn, KHÔNG collapse — cùng nhau đảm bảo transitively:** originating Decision vẫn valid (qua `eligible_for_new_risk_evaluation` → `trade-intent.md` §6a → `decision.md` invalidate-chain); Trade Intent vẫn valid VÀ ISSUED (điều kiện 5); RiskEvaluation vẫn valid VÀ APPROVED (điều kiện 2+3); Execution Intent vẫn ISSUED (điều kiện 1). `execution-intent.md` KHÔNG tự author Order semantics — rule này CHỈ pin definition, KHÔNG chọn C6 CÓ dùng nó ra sao.

**Khi Trade Intent hoặc RiskEvaluation gốc trở nên invalid (bị invalidate/supersede, `trade-intent.md` §10/`risk.md` §10):**
- Execution Intent liên quan trở nên **ineligible cho Order creation MỚI** (điều kiện 2/3/5 fail tùy trường hợp);
- Execution Intent **KHÔNG tự động bị xóa/rewrite** — vẫn là historical fact, `ExecutionIntentCurrentView` (§6) vẫn resolve `current_status` bình thường;
- Historical replay TRƯỚC thời điểm invalidate KHÔNG bị ảnh hưởng;
- Rút/expire tường minh (`ExecutionIntentStatusChanged`, §4) VẪN là một hành động RIÊNG, tùy chọn — `eligible_for_new_order_creation` KHÔNG tự động chuyển `current_status` sang `WITHDRAWN`;
- `execution-intent.md` KHÔNG author Order behavior nào cho tình huống này — C6 (chưa author) chịu trách nhiệm CONSUME rule này;
- Một **replacement chain** (Trade Intent MỚI, hoặc RiskEvaluation MỚI cùng logical key) CÓ THỂ derive một Execution Intent MỚI RIÊNG BIỆT — KHÔNG rewrite lịch sử (risk.md Scenario 11/12, §17).

**Một RiskEvaluation correction replacement (R2, risk.md §10) CÓ THỂ derive Execution Intent RIÊNG của nó** — Execution Intent cũ (gắn R1) và Execution Intent mới (gắn R2) là hai historical fact hoàn toàn PHÂN BIỆT, KHÔNG gộp/ghi đè lẫn nhau (risk.md Scenario 12, §17).

`execution-intent.md` KHÔNG tự enforce rule này (chưa có consumer — C6 chưa author); CHỈ pin định nghĩa deterministic.

## 7. RiskEvaluation-to-Execution-Intent cardinality — xem `risk.md` §9

Định nghĩa authoritative đầy đủ tại [`risk.md`](./risk.md) §9 — execution-intent.md KHÔNG lặp lại, chỉ tái khẳng định ràng buộc chiều ngược: **mọi ExecutionIntentIssued PHẢI causally trace về đúng MỘT RiskEvaluationRecorded với `result = APPROVED`** (§3 invariant) — KHÔNG có ExecutionIntentIssued "mồ côi" không originating RiskEvaluation, KHÔNG có ExecutionIntentIssued nào từ một RiskEvaluation `result ∈ {REJECTED, NON_EVALUABLE}`, KHÔNG có HAI ExecutionIntentIssued VALID cùng `originating_risk_evaluation_id` (§1 uniqueness invariant, §10 dưới).

## 8. Correction lineage

Correction lineage scoped chính xác theo `(subject_id, effective_time)` — mỗi effective_time-slice có chuỗi lineage RIÊNG, cùng nguyên tắc đã khóa xuyên suốt `instrument.md`/`venue.md`/`account.md`/`strategy.md`/`trade-intent.md`.

**`ExecutionIntentIssued` — invalidate-only, KHÔNG replacement (§3/§5):**

```text
F1 (ExecutionIntentIssued)
  → ExecutionIntentFactInvalidated targeting F1
  → KHÔNG có replacement dưới cùng execution_intent_id — correction thực tế là invalidate, KHÔNG
    đăng ký execution_intent_id mới cho cùng originating_risk_evaluation_id.
```

**`ExecutionIntentStatusChanged` — correction lineage chuẩn, same-slice replacement (§4/§5), mười invariant chuẩn (đối xứng `strategy.md` §13/`trade-intent.md` §8, KHÔNG lặp lại toàn văn):**

```text
F1 (ExecutionIntentStatusChanged)
  → ExecutionIntentFactInvalidated targeting F1
  → replacement (cùng event type ExecutionIntentStatusChanged), supersedes_fact_ref = F1
```

## 9. Time semantics và bitemporal correctness

- `effective_time` — required trên mọi event trong tài liệu này.
- `recorded_time` — recorded axis, universal.
- `ExecutionIntentIssued.effective_time >= originating RiskEvaluationRecorded.risk_evaluation_time` — Execution Intent KHÔNG BAO GIỜ effective trước RiskEvaluation gốc; mặc định bằng nhau (§3).
- `ExecutionIntentIssued.recorded_time > originating RiskEvaluationRecorded.recorded_time` — strict causal ordering (§3).
- Replay tại cursor T chỉ thấy fact có `recorded_time ≤ T` — invalidation ghi SAU T KHÔNG visible tại T.
- `market_time` PROHIBITED xuyên suốt tài liệu này.

## 10. Canonical policy identifiers — nguồn duy nhất (context `risk-gateway`, riêng cho Execution Intent)

**Hai canonical policy identifier bổ sung, khai báo tại đây** — context `risk-gateway` đã có `initial_fact_correction_policy`/`risk_computation_idempotency_policy`/`risk_evaluation_attempt_idempotency_policy`/`risk_correction_lineage_policy` khai báo tại `risk.md` §12 (áp dụng cho RiskEvaluation/RiskEvaluationAttempt subject); Execution Intent tái sử dụng CHÍNH `initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS` (đúng giá trị, KHÔNG khai báo trùng lặp) cho phần registration bất biến; `ExecutionIntentStatusChanged` dùng correction lineage chuẩn (§8), KHÔNG cần policy identifier riêng.

```yaml
execution_intent_derivation_idempotency_policy: ONE_VALID_INTENT_PER_ORIGINATING_RISK_EVALUATION
execution_intent_origin_validity_policy: ORIGIN_MUST_BE_VISIBLE_VALID_HEAD_AT_SAME_CURSOR
```

**`execution_intent_derivation_idempotency_policy: ONE_VALID_INTENT_PER_ORIGINATING_RISK_EVALUATION`** (đóng yêu cầu tương đương `C4-MAJ-02`, ngay từ v0.1) — `originating_risk_evaluation_id` là UNIQUE KEY trên toàn bộ ExecutionIntentIssued VALID (§1). Same origin + same payload → idempotent, trả về `execution_intent_id` đã tồn tại; same origin + changed payload → deterministic conflict, reject. **KHÔNG unstated cross-stream atomicity** — RiskEvaluation và Execution Intent là hai authoritative stream RIÊNG, KHÔNG có transaction ngầm định đảm bảo cả hai append cùng lúc; một khoảng trống tạm thời (RiskEvaluation APPROVED tồn tại, ExecutionIntentIssued CHƯA append) là trạng thái BÌNH THƯỜNG, KHÔNG phải data-integrity violation (Scenario 16, risk.md §17). Phase 1 recovery: cho một RiskEvaluation APPROVED VALID bất kỳ KHÔNG có ExecutionIntentIssued VALID tương ứng, recovery logic PHẢI resolve deterministic (idempotent derivation ở trên) và (re)thử issuance — implementation technology (retry queue, outbox, message-broker) hoàn toàn deferred (Phase 1, KHÔNG định nghĩa ở đây — forbidden scope).

**`execution_intent_origin_validity_policy: ORIGIN_MUST_BE_VISIBLE_VALID_HEAD_AT_SAME_CURSOR`** (đóng yêu cầu tương đương `C4-MAJ-06`, ngay từ v0.1) — xem §6a cho định nghĩa `eligible_for_new_order_creation` đầy đủ.

## 11. Downstream reference contract (cho Package 0.2-C6 Order, chưa author)

Package sau (Order, Package 0.2-C6, chưa author) tham chiếu Execution Intent qua ĐÚNG các field sau, KHÔNG hơn:

```yaml
execution_intent_id: {type: string, required: true, ref: execution-intent}
originating_risk_evaluation_id: {type: string, description: "= §1, ref: risk"}
trade_intent_id: {type: string, description: "= §1, ref: trade-intent"}
account_id: {type: string, ref: account, description: "= §1"}
instrument_selection_ref: {type: object, description: "= §1 — {instrument_id, venue_id, listing_id}"}
direction: {type: enum, values: [LONG, SHORT], description: "= §1"}
execution_action: {type: enum, values: [OPEN_EXPOSURE], description: "= §1"}
approved_quantity: {type: decimal, description: "= §1 — GUARANTEE (v0.2, đóng C5-MAJ-04): LUÔN strictly positive (> 0), KHÔNG BAO GIỜ 0"}
quantity_unit: {type: string, description: "= §1"}
current_status: {type: enum, values: [ISSUED, WITHDRAWN, EXPIRED], description: "PHẢI resolve từ authoritative event stream TẠI cursor, KHÔNG ExecutionIntentCurrentView latest-state"}
eligible_for_new_order_creation: {type: boolean, description: "derived, xem §6a — C6 PHẢI kiểm tra rule này TRƯỚC khi Order creation mới, KHÔNG chỉ dựa current_status = ISSUED"}
```

**Downstream authority rule — MỘT quy tắc duy nhất, không ngoại lệ:** downstream package PHẢI resolve mọi field trên TRỰC TIẾP từ authoritative Execution Intent event stream (§3–§5) TẠI ĐÚNG cursor mà chính computation đó đang dùng. `ExecutionIntentCurrentView` latest-state (§6) KHÔNG BAO GIỜ được dùng làm input. C6 (chưa author) PHẢI áp dụng `eligible_for_new_order_creation` (§6a) TRƯỚC khi Order creation mới. `execution-intent.md` KHÔNG author semantics của Order/Fill/Position (Package 0.2-C6–C7, chưa author).

## 12. Prohibitions

**Execution Intent KHÔNG được sở hữu:** RiskEvaluation evidence/sizing semantics (thuộc `risk.md`); Order acceptance/submission/routing/fill status/position state (Package 0.2-C6–C7, chưa author); order type/limit price/stop price/exchange payload; capital allocation/multi-strategy arbitration; module-registry entry.

## 13. Ngoài phạm vi — defer

**Deferred tường minh, không author ở C5 (Phase 1 implementation concern, non-blocking):**

- Chính sách hết hạn cụ thể (`EXPIRED` trigger timing/mechanism) — Phase 1.
- Lý do `WITHDRAWN` cụ thể — Phase 1/C6 concern, deferred.
- `CLOSE`/`REDUCE`/`FLAT` execution_action — walking skeleton không cần, tránh premature action taxonomy.
- Multi-instrument/portfolio-level Execution Intent — v0.1 tối đa một instrument selection per Execution Intent (§1).
- Runtime worker ownership, transaction boundaries, retry/backoff, monitoring/escalation (Phase 1, cùng nguyên tắc defer đã áp dụng xuyên suốt Package 0.2).
- Implementation technology cho RiskEvaluation→Execution Intent recovery (retry queue/outbox/message-broker, §10) — boundary semantic pin, KHÔNG chọn công nghệ.

## 14. Open questions ngoài phạm vi

- Cơ chế cụ thể generate `execution_intent_id` — chưa quyết, Phase 1, cùng nguyên tắc defer đã áp dụng cho `risk_evaluation_id`.
- Retention/resolvability horizon cụ thể cho Execution Intent đã WITHDRAWN/EXPIRED — chưa pin ở v0.1.
- Không đóng OQ-002/OQ-003.
