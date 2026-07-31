---
id: risk
title: Risk
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

# Risk

> **Vai trò của tài liệu này:** Một trong hai Domain Contract của Package 0.2-C5 (Risk Gateway and Execution Intent Foundation) — định nghĩa **RiskEvaluation** (bản ghi authoritative của MỘT lần Risk Gateway đánh giá deterministic một Trade Intent eligible tại một risk computation cursor) và **RiskEvaluationAttempt** (bản ghi authoritative của MỘT LẦN THỬ đánh giá — kể cả khi không dẫn tới RiskEvaluation). Draft, chưa Approved/Locked. Thuộc capability `risk-management` / context `risk-gateway` (đăng ký MỚI tại [`context-map.yaml`](./context-map.yaml)). Kiến trúc controlling: [`trade-intent.md`](./trade-intent.md) v0.2 Draft §6a (`eligible_for_new_risk_evaluation`), [`decision.md`](./decision.md) v0.3 Draft (bốn trục evidence pattern, correction lineage pattern, attempt-identity pattern — ÁP DỤNG LẠI đúng semantic đã proven, KHÔNG sao chép cơ học), [Chapter 9 §9.1](../constitution/09-plugin-model.md) (Locked, bốn lớp Plugin identity áp dụng platform-wide), [Chapter 8 §8.1.1/§8.2/§8.5](../constitution/08-event-model.md) (Locked, Referenced Authoritative Artifact + canonical Replay Cursor — TÁI SỬ DỤNG nguyên vẹn, KHÔNG tạo schema gần giống). Tài liệu này CHỈ implement field/invariant mà các nguồn trên yêu cầu, KHÔNG tự quyết architecture mới ngoài phạm vi đã khóa.

RiskEvaluation **KHÔNG phải** Strategy Decision (`decision.md`), Trade Intent (`trade-intent.md`), Execution Intent (`execution-intent.md`, file riêng), Order/Fill/Position (Package 0.2-C6–C7, chưa author), exchange acknowledgement, portfolio rebalance, hay một mutable approval flag. Nó là **bản ghi authoritative, bitemporal, deterministic, tự-giải-thích được** của một lần Risk Gateway đánh giá MỘT Trade Intent eligible — trả lời chính xác bảy câu hỏi: Trade Intent nào được đánh giá? Có eligible cho Risk evaluation mới không? Risk policy/configuration chính xác nào được áp dụng? Account/environment/TradableListing nào được đánh giá? Capital/exposure evidence nào visible? Kết quả Risk gì? Tại sao? Có tạo Execution Intent không?

**Ví dụ walking-skeleton duy nhất dùng để validate thiết kế (KHÔNG phải yêu cầu xây dựng general portfolio-risk engine):** một Trade Intent LONG/OPEN hợp lệ, một Account, một TradableListing, environment PAPER, một risk policy bounded (risk budget cố định + notional cap), một quantity calculation deterministic. Mười tám Scenario chấp nhận (1–18, xem §17) đều dựa trên ví dụ này.

**`risk-evaluation-attempt-recorded`/`risk-evaluation-recorded`/`risk-evaluation-fact-invalidated`/`risk-evaluation-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây, tách biệt display name/`event_type`, cùng nguyên tắc mọi Domain Contract trước.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/C1–C4** (đóng trước, không chờ review round phát hiện): opaque identity không derive từ scope; envelope binding cho `*FactInvalidated`; fold algorithm "visible-valid-head per logical key" cho Current View; Current View KHÔNG BAO GIỜ authority; canonical policy identifier khai báo ĐÚNG MỘT NƠI, độc lập theo context; **ba bài học riêng từ C4 correction (áp dụng NGAY TỪ v0.1, KHÔNG lặp lại lỗi đã trả giá):** (1) KHÔNG circular reference giữa Attempt và RiskEvaluation — Attempt KHÔNG mang field trỏ tới RiskEvaluation, chỉ RiskEvaluation trỏ ngược lại Attempt qua `causation_refs` (one-way sequence, đóng trước lớp lỗi `C4-DELTA-MAJ-01`-style); (2) `evaluation_attempt_id` (identity cá nhân một lần thử) TÁCH BIỆT khỏi logical computation key (nhóm nhiều attempt) — idempotency scoped theo `evaluation_attempt_id`, KHÔNG theo logical key, cho phép nhiều attempt (kể cả outcome khác nhau) cùng key (đóng trước lớp lỗi `C4-DELTA-MAJ-02`-style); (3) operational failure (`FAILED_BEFORE_EVALUATION`) tường minh RETRYABLE, KHÔNG permanently block same-cursor recovery.

**Phạm vi bounded tường minh:** KHÔNG author Order/Fill/Position/Replay Event (Package 0.2-C6–C7). KHÔNG định nghĩa order type/limit price/stop price/exchange payload/order routing/exchange adapter behavior. KHÔNG portfolio-level arbitration/multi-account netting/advanced margin/liquidation model. KHÔNG xây dựng Risk DSL tổng quát — chỉ MỘT bounded sizing method đủ cho walking skeleton (§5c). KHÔNG redefine Account/Candle/Feature/Decision/Trade Intent contract — mọi evidence tham chiếu qua `event_record_ref` opaque hoặc `ref:` trực tiếp. KHÔNG backtest/optimizer infrastructure. KHÔNG FX conversion. KHÔNG signed/netted exposure arithmetic. KHÔNG general unit framework — chỉ bounded v0.1 unit model (§5b1). KHÔNG sửa `decision.md`/`trade-intent.md`/C1–C4/ADR-010/ADR-012/ADR-013/Constitution.

**v0.2 — bounded correction, đóng `C5-MAJ-01`/`C5-MAJ-02`/`C5-MAJ-03`/`C5-MAJ-04`/`C5-MAJ-05`/`C5-MAJ-06` (consolidated Review A + Independent Review B findings):** (a) `C5-MAJ-01` — sửa thứ tự Attempt EVALUATED: bounded policy computation PHẢI hoàn tất TRƯỚC KHI `RiskEvaluationAttemptRecorded(EVALUATED)` ghi (KHÔNG còn "Attempt ghi trước rồi engine chạy") — crash trước khi computation hoàn tất KHÔNG được để lại một EVALUATED attempt; crash SAU Attempt nhưng TRƯỚC RiskEvaluation là recoverable append gap (đối xứng nguyên tắc "no unstated cross-stream atomicity" đã proven, §9). (b) `C5-MAJ-02` — thêm `evidence_availability` (bảy khóa đóng, năm giá trị đóng) — mọi ref/scalar field trở thành conditional (required: false), field CHỈ present khi khóa tương ứng = AVAILABLE; KHÔNG còn required field không tồn tại được trong NON_EVALUABLE bundle. (c) `C5-MAJ-03` — thêm bounded v0.1 unit model (§5b1) — mọi Risk arithmetic PHẢI cùng currency với TradableListing quote asset; mismatch → NON_EVALUABLE/INCOMPATIBLE_EVIDENCE_UNIT; KHÔNG FX conversion, KHÔNG signed exposure. (d) `C5-MAJ-04` — `approved_quantity` PHẢI strictly positive sau floor-rounding — bằng 0 → REJECTED/QUANTITY_ROUNDS_TO_ZERO, zero Execution Intent; Execution Intent PHẢI pin `approved_quantity > 0`. (e) `C5-MAJ-05` — pin domain số học chính xác cho mọi scalar input, disclose bounded `quantity_precision` maximum = 18 (không tìm thấy repository-wide bound sẵn có, chọn tường minh v0.1, xem self-review); exposure âm → REJECTED/INVALID_SIZING_INPUT, KHÔNG bypass cap. (f) `C5-MAJ-06` — `eligible_for_new_order_creation` (execution-intent.md §6a) mở rộng đủ NĂM điều kiện, transitively đảm bảo Decision→Trade Intent→RiskEvaluation→Execution Intent đều valid. Bounded — không đổi opaque identity, per-attempt identity, multiple attempts per key, retry sau FAILED_BEFORE_EVALUATION, one visible valid head, invalidate-first correction lineage, replay semantics, bốn trục risk evidence separation, no-look-ahead, Decision/Trade Intent causality, Risk-to-Execution-Intent idempotency, no cross-stream atomicity, Execution Intent lifecycle, C1–C4 semantics, C5/C6 boundary.

## 1. RiskEvaluation — `kind: entity`

```yaml
id: risk-evaluation
kind: entity
capability_id: risk-management
domain_context_id: risk-gateway
description: >
  Bản ghi authoritative của MỘT lần Risk Gateway đánh giá deterministic một Trade Intent eligible
  tại một risk_context_cursor cụ thể. MỘT RiskEvaluationRecorded fact là BẤT BIẾN sau khi ghi.
  risk_evaluation_id BẤT BIẾN, globally unique, KHÔNG BAO GIỜ tái sử dụng cho fact khác — kể cả một
  correction replacement mang risk_evaluation_id HOÀN TOÀN MỚI (đúng semantic đã proven tại
  decision.md §1, đóng trước lớp lỗi C4-MAJ-03-style). Correction lineage (§10) cho phép MỘT logical
  computation key (trade_intent_id, risk_context_cursor) có NHIỀU RiskEvaluationRecorded theo thời
  gian: fact SAI invalidate qua RiskEvaluationFactInvalidated (§6), fact THAY THẾ mang
  risk_evaluation_id MỚI + supersedes_fact_ref trỏ fact bị invalidate, CÙNG logical key. Tại một
  cursor, đúng MỘT visible valid head cho mỗi logical key (§7 fold algorithm).
invariants:
  - "risk_evaluation_id là opaque, globally unique trong toàn Ride, gán tại RiskEvaluationRecorded — KHÔNG derive/resolve từ trade_intent_id, risk_context_cursor, hay bất kỳ field nội dung nào. Bất biến, KHÔNG tái sử dụng cho subject khác — kể cả correction replacement (Chapter 6 §6.1)."
  - "MỘT RiskEvaluation thuộc ĐÚNG MỘT Trade Intent (`trade_intent_id`, ref: trade-intent) — không multi-intent aggregation, không batch nhiều Trade Intent."
  - "Logical computation key = (trade_intent_id, risk_context_cursor) — tại một cursor cho trước, đúng MỘT visible valid head RiskEvaluationRecorded cho mỗi key (§7 fold algorithm). MỘT key CÓ THỂ có nhiều RiskEvaluationRecorded lịch sử qua correction lineage (§10) — mỗi fact có risk_evaluation_id RIÊNG, liên kết qua supersedes_fact_ref."
  - "Retry của MỘT logical computation attempt (chưa từng invalidate) với evidence bundle giống hệt PHẢI idempotent no-op — trả về risk_evaluation_id đã tồn tại, KHÔNG tạo bản ghi thứ hai (§12 `risk_computation_idempotency_policy`, §2 RiskEvaluationAttempt). Retry với evidence khác (chưa invalidate predecessor) PHẢI reject tường minh (deterministic conflict) — KHÔNG BAO GIỜ tạo hai RiskEvaluationRecorded VALID cùng key với evidence khác nhau MÀ KHÔNG qua correction lineage tường minh (§10)."
  - "RiskEvaluation KHÔNG mutable dưới bất kỳ hình thức nào — không PATCH event, không revision event tại chỗ. Historical RiskEvaluation (kể cả đã bị supersede) vẫn resolvable — bằng chứng lịch sử độc lập trạng thái hiện tại của Trade Intent/Decision."
schema:
  risk_evaluation_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  trade_intent_id: {type: string, required: true, ref: trade-intent, description: "đúng một Trade Intent, eligible_for_new_risk_evaluation == true TẠI cursor (§4/§5a)"}
  risk_context_cursor: {type: object, required: true, description: "Replay Cursor hợp lệ, TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1 — xem §3"}
  risk_evaluation_time: {type: timestamp, required: true, description: "effective-axis value — xem §5"}
  result: {type: enum, values: [APPROVED, REJECTED, NON_EVALUABLE], required: true, description: "xem §5e"}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho RiskEvaluation gốc; BẮT BUỘC cho correction replacement, xem §10"}
events_emitted: [RiskEvaluationRecorded, RiskEvaluationFactInvalidated]
events_consumed: []
commands: []
queries: []
```

## 2. RiskEvaluationAttempt — `kind: entity`

**Vai trò:** bản ghi authoritative của MỘT LẦN THỬ Risk Gateway đánh giá — KHÔNG PHÂN BIỆT kết quả có dẫn tới RiskEvaluation hay không. **Mọi lần thử ĐỀU được ghi nhận — KHÔNG BAO GIỜ represented bằng event absence** (đóng trước yêu cầu tương đương `C4-MAJ-04`, ngay từ v0.1). Subject RIÊNG BIỆT khỏi RiskEvaluation — attempt outcome `EVALUATED` chứng minh policy engine đã chạy TỚI ĐÍCH thành công (dẫn tới đúng MỘT RiskEvaluationRecorded, `result ∈ {APPROVED, REJECTED, NON_EVALUABLE}` — CẢ BA đều là fact THẬT, KHÔNG absence); hai outcome còn lại (`INELIGIBLE`/`FAILED_BEFORE_EVALUATION`) KHÔNG dẫn tới RiskEvaluation nào.

**Hai identity KHÁC NHAU, KHÔNG gộp (đóng trước yêu cầu tương đương `C4-DELTA-MAJ-02`, ngay từ v0.1):**

```text
evaluation_attempt_id:      định danh MỘT LẦN THỬ cá nhân — opaque, globally unique, per attempt
logical computation key:    (trade_intent_id, risk_context_cursor) — nhóm NHIỀU attempt CÓ THỂ chia
                             sẻ CÙNG key, mỗi attempt có evaluation_attempt_id RIÊNG
```

MỘT logical computation key CÓ THỂ có NHIỀU `RiskEvaluationAttemptRecorded` theo thời gian, KỂ CẢ với `attempt_outcome` KHÁC NHAU (ví dụ `FAILED_BEFORE_EVALUATION` rồi sau đó retry thành công `EVALUATED` tại CÙNG cursor) — điều này KHÔNG phải data-integrity violation.

```yaml
id: risk-evaluation-attempt
kind: entity
capability_id: risk-management
domain_context_id: risk-gateway
description: >
  Bản ghi authoritative, BẤT BIẾN, của MỘT lần thử đánh giá Risk — độc lập việc lần thử đó có dẫn
  tới RiskEvaluation hay không. evaluation_attempt_id (identity cá nhân) và logical computation
  key (trade_intent_id, risk_context_cursor — nhóm nhiều attempt) là HAI khái niệm tách biệt.
invariants:
  - "evaluation_attempt_id là opaque, globally unique trong toàn Ride, gán tại RiskEvaluationAttemptRecorded — KHÔNG derive từ trade_intent_id/risk_context_cursor. Bất biến, KHÔNG tái sử dụng."
  - "Idempotency áp dụng theo TỪNG evaluation_attempt_id — retry CÙNG evaluation_attempt_id + CÙNG payload → idempotent no-op; CÙNG evaluation_attempt_id + payload KHÁC → deterministic conflict, reject (§12 `risk_evaluation_attempt_idempotency_policy`, đối xứng `instrument.md` §17)."
  - "Logical computation key (trade_intent_id, risk_context_cursor) KHÔNG BẮT BUỘC unique — nhiều RiskEvaluationAttemptRecorded (evaluation_attempt_id RIÊNG cho mỗi cái) CÓ THỂ tồn tại cùng key, KỂ CẢ với attempt_outcome khác nhau. Đây KHÔNG phải data-integrity violation."
  - "attempt_outcome = EVALUATED KHÔNG mang, KHÔNG yêu cầu một field trỏ tới RiskEvaluation — attempt này CHỈ chứng minh 'policy engine đã chạy tới đích thành công, một RiskEvaluationRecorded được kỳ vọng NGAY SAU' (§4/§5, one-way sequence). Muốn biết RiskEvaluation nào tương ứng một attempt EVALUATED, PHẢI resolve TỪ authoritative RiskEvaluation history — qua `GetRiskEvaluationForComputation(trade_intent_id, risk_context_cursor, cursor)` (§7) HOẶC reverse-lookup RiskEvaluationRecorded có `causation_refs` chứa chính attempt event này — KHÔNG BAO GIỜ qua một field lưu sẵn trên Attempt."
  - "**v0.2 (đóng C5-MAJ-01):** `attempt_outcome = EVALUATED` CHỈ được ghi SAU KHI bounded policy computation (§5c) đã hoàn tất TRỌN VẸN — toàn bộ evidence bundle đã resolve/tính xong, kết quả cuối cùng (APPROVED/REJECTED/NON_EVALUABLE) đã xác định. `EVALUATED` là bằng chứng 'computation đã hoàn tất,' KHÔNG BAO GIỜ ghi TRƯỚC KHI computation hoàn tất. Nếu engine crash TRƯỚC KHI computation hoàn tất, KHÔNG được để lại một `RiskEvaluationAttemptRecorded(EVALUATED)` nào cho lần thử đó — hoặc KHÔNG ghi gì (retry tạo evaluation_attempt_id MỚI), hoặc ghi `FAILED_BEFORE_EVALUATION` nếu crash được phát hiện/handled (§4)."
  - "**v0.2 (đóng C5-MAJ-01):** khoảng trống giữa Attempt EVALUATED đã ghi VÀ RiskEvaluationRecorded chưa ghi (crash giữa hai bước append) là một RECOVERABLE APPEND GAP — KHÔNG phải data-integrity violation, đối xứng nguyên tắc 'no unstated cross-stream atomicity' đã pin cho RiskEvaluation→ExecutionIntent (§9). Computation TẠI (trade_intent_id, risk_context_cursor) là deterministic (§1 `risk_computation_idempotency_policy`) — recovery logic (Phase 1) PHẢI resolve deterministic bằng cách re-run CÙNG computation (cùng cursor → cùng evidence → cùng kết quả, guaranteed by determinism) VÀ append RiskEvaluationRecorded với `causation_refs` trỏ ĐÚNG attempt EVALUATED đã tồn tại đó (KHÔNG tạo evaluation_attempt_id MỚI cho computation ĐÃ EVALUATED thành công). Implementation technology (retry queue, transient state cache) hoàn toàn deferred (Phase 1, forbidden scope) — Domain Contract chỉ pin ORDER requirement, KHÔNG pin MECHANISM."
  - "attempt_outcome ∈ {INELIGIBLE, FAILED_BEFORE_EVALUATION}: KHÔNG RiskEvaluation nào được tạo cho lần thử này. FAILED_BEFORE_EVALUATION tường minh RETRYABLE — một attempt EVALUATED sau đó tại CÙNG logical key hoàn toàn hợp lệ."
  - "Khi một attempt_outcome = EVALUATED được ghi tại một logical key ĐÃ CÓ một RiskEvaluationRecorded VALID (visible-valid-head, §7), attempt MỚI PHẢI resolve/reuse risk_evaluation_id đã tồn tại đó (nếu evidence giống hệt — RiskEvaluation-layer idempotency, §1/§12) hoặc deterministic conflict (nếu evidence khác) — TUYỆT ĐỐI KHÔNG được tạo risk_evaluation_id thứ hai cho CÙNG key trừ khi predecessor ĐÃ invalidate VÀ correction lineage (§10) cho phép."
  - "RiskEvaluationAttempt KHÔNG có correction lineage riêng, KHÔNG có lifecycle/state machine, KHÔNG có scheduler/retry workflow — retry đơn thuần là ghi một RiskEvaluationAttemptRecorded MỚI (evaluation_attempt_id mới) tại cùng logical key, deferred §15."
schema:
  evaluation_attempt_id: {type: string, required: true, description: "opaque, stable, per-attempt identity"}
  trade_intent_id: {type: string, required: true, ref: trade-intent}
  risk_context_cursor: {type: object, required: true, description: "cùng shape §3 — một phần logical computation key"}
  attempt_outcome: {type: enum, values: [EVALUATED, INELIGIBLE, FAILED_BEFORE_EVALUATION], required: true}
  reason_code: {type: string, required: false, description: "BẮT BUỘC khi attempt_outcome != EVALUATED; TUYỆT ĐỐI ABSENT khi EVALUATED — xem §4 cho enum đóng"}
  checked_evidence_refs: {type: array, items: event_record_ref, required: false, description: "authoritative fact đã kiểm tra để xác định outcome — CÓ THỂ RỖNG"}
events_emitted: [RiskEvaluationAttemptRecorded]
events_consumed: []
commands: []
queries: []
```

## 3. Canonical event envelope — áp dụng cho mọi RiskEvaluation/RiskEvaluationAttempt event (§4–§6)

Mọi event trong tài liệu này là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). KHÔNG event nào trong tài liệu này thuộc `event_class: decision` — `decision_time`/`decision_context_cursor` (envelope-level, ADR-010) là field RIÊNG của `decision.md`'s `DecisionRecorded`, KHÔNG áp dụng ở đây. RiskEvaluation dùng `effective_time` tiêu chuẩn (semantic: `risk_evaluation_time`) VÀ `risk_context_cursor` như **PAYLOAD field** (KHÔNG phải envelope-level), TÁI SỬ DỤNG nguyên vẹn shape Replay Cursor Chapter 8 §8.5.1 — đúng pattern `decision.md` §3/§4 đã dùng cho `DecisionEvaluationAttemptRecorded`.

```yaml
envelope:
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2)
  event_contract_ref: {cardinality: required}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}             # khi Ride ghi nhận fact này
  subject_ref: {cardinality: "required — shape canonical, xem dưới. Trên RiskEvaluationFactInvalidated, PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate."}
  stream_ref: {cardinality: required}                # Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # Phase 1, chưa author
  correlation_id: {cardinality: "required — Risk evaluation LUÔN thuộc một correlation flow tường minh (originating Trade Intent)"}
  causation_refs: {cardinality: "RiskEvaluationAttemptRecorded: zero-or-more (Risk Gateway internal trigger, Phase 1, chưa author). RiskEvaluationRecorded: KHÔNG BAO GIỜ rỗng — PHẢI chứa RiskEvaluationAttemptRecorded tương ứng (§5), CỘNG RiskEvaluationFactInvalidated của predecessor nếu là correction replacement (§10). RiskEvaluationFactInvalidated: KHÔNG BAO GIỜ rỗng."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3."}
  effective_time: {cardinality: "required trên mọi event trong tài liệu này — semantic = risk_evaluation_time trên RiskEvaluationRecorded (§5); semantic khác trên RiskEvaluationAttemptRecorded/RiskEvaluationFactInvalidated, xem §4/§6."}
  decision_time: {cardinality: "PROHIBITED — event_class: decision KHÔNG áp dụng cho RiskEvaluation (thuộc riêng decision.md)."}
  decision_context_cursor: {cardinality: "PROHIBITED (envelope-level) — risk_context_cursor sống ở PAYLOAD, xem risk_context_cursor shape dưới."}
  market_time: {cardinality: "PROHIBITED — RiskEvaluation/RiskEvaluationAttempt là computation authoritative, không phải quan sát trực tiếp venue (Chapter 5 §5.2)."}
  source_identity: {cardinality: "PROHIBITED — luôn phát sinh nội bộ từ Risk Gateway (Phase 1, chưa author), KHÔNG BAO GIỜ từ external feed."}

risk_context_cursor (shape, đúng canonical Replay Cursor — Chapter 8 §8.5.1, TÁI SỬ DỤNG nguyên vẹn, KHÔNG một schema gần giống):
  recorded_time: <timestamp>                          # required — knowledge boundary
  input_contract_ref: {contract_id: <string>, contract_version: <string>}   # required — versioned, immutable (§8.1.1)
  stream_registry_version: <string>                   # required
  lifecycle_frontier:                                  # required
    stream_id: <string>                                # canonical lifecycle stream
    position: {kind: <genesis | event>, sequence: <integer>}
  stream_positions: {<stream_id>: <sequence>, ...}     # required — map, mọi stream thuộc universe của cursor

subject_ref (RiskEvaluation):
  context_id: risk-gateway
  subject_kind: entity
  subject_type: RiskEvaluation
  subject_id: <risk_evaluation_id — opaque, stable, xem §1>
  scope:
    trade_intent_id: <string>

subject_ref (RiskEvaluationAttempt, §2):
  context_id: risk-gateway
  subject_kind: entity
  subject_type: RiskEvaluationAttempt
  subject_id: <evaluation_attempt_id — opaque, stable, xem §2>
  scope:
    trade_intent_id: <string>

event_types:
  RiskEvaluationAttemptRecorded: RISK_EVALUATION_ATTEMPT_RECORDED
  RiskEvaluationRecorded: RISK_EVALUATION_RECORDED
  RiskEvaluationFactInvalidated: RISK_EVALUATION_FACT_INVALIDATED
```

`stream_ref`/`producer_ref` — Phase 1, chưa tồn tại. `risk_context_cursor` field SHAPE bắt buộc ngay v0.1 (tái sử dụng Chapter 8 §8.5.1 Locked); MECHANISM resolve (Stream Registry cụ thể) deferred Phase 1.

**Relational invariants bắt buộc trên `risk_context_cursor`** (Chapter 8 §8.5.2, tái khẳng định KHÔNG lặp lại toàn văn):
```text
risk_context_cursor.recorded_time ≤ RiskEvaluationRecorded.recorded_time
evidence_fact.recorded_time ≤ risk_context_cursor.recorded_time
cursor.stream_registry_version = registry version mà input_contract_ref pin
```
Vi phạm bất kỳ điều nào → **invalid `risk_context_cursor`, RiskEvaluationRecorded PHẢI bị từ chối khi append** — cơ chế thực thi no-look-ahead (I-3) cho Risk.

## 4. `RiskEvaluationAttemptRecorded` — `kind: event`

Kế thừa envelope §3 (KHÔNG thuộc `event_class: decision`).

```yaml
id: risk-evaluation-attempt-recorded
kind: event
capability_id: risk-management
domain_context_id: risk-gateway
description: >
  Fact AUTHORITATIVE DUY NHẤT ghi nhận MỘT lần thử đánh giá Risk — LUÔN LUÔN phát, bất kể outcome.
invariants:
  - "payload.evaluation_attempt_id PHẢI khớp đúng subject_ref.subject_id."
  - "envelope.effective_time = risk_context_cursor.recorded_time (payload) — mặc định, trừ khi backfill lịch sử tường minh pin giá trị khác."
  - "attempt_outcome = EVALUATED: reason_code/checked_evidence_refs TUYỆT ĐỐI ABSENT (evidence đầy đủ sống trên RiskEvaluationRecorded, §5). **v0.2 (đóng C5-MAJ-01):** ghi CHỈ SAU KHI bounded policy computation (§5c) đã hoàn tất trọn vẹn — KHÔNG BAO GIỜ ghi cho một computation CHƯA hoàn tất. KHÔNG payload field nào trỏ tới RiskEvaluation — one-way sequence: computation hoàn tất TRƯỚC, Attempt EVALUATED ghi SAU đó, RỒI RiskEvaluationRecorded.causation_refs trỏ ngược lại attempt (§5) — KHÔNG atomic multi-event transaction giữa ba bước này."
  - "attempt_outcome = INELIGIBLE: reason_code = TRADE_INTENT_INELIGIBLE (`eligible_for_new_risk_evaluation(trade_intent_id, cursor) == false`, trade-intent.md §6a) — checked_evidence_refs khuyến nghị trỏ fact trade-intent.md/decision.md xác nhận điều kiện fail."
  - "attempt_outcome = FAILED_BEFORE_EVALUATION: reason_code = RISK_ENGINE_COMPUTATION_BOUNDARY_ERROR (v0.1 CHỈ một giá trị — KHÔNG model broad runtime exception taxonomy/observability infrastructure, deferred §15); checked_evidence_refs thường rỗng. Tường minh RETRYABLE — một RiskEvaluationAttemptRecorded MỚI (evaluation_attempt_id khác) tại CÙNG logical computation key sau đó là hợp lệ."
  - "Idempotency scoped theo TỪNG evaluation_attempt_id (§2, §12 `risk_evaluation_attempt_idempotency_policy`) — KHÔNG theo logical computation key."
  - "No-look-ahead: mọi checked_evidence_refs PHẢI thỏa fact.recorded_time ≤ risk_context_cursor.recorded_time (đối xứng §5d)."
payload:
  evaluation_attempt_id: {type: string, required: true}
  trade_intent_id: {type: string, required: true}
  risk_context_cursor: {type: object, required: true, description: "cùng shape §3 — payload field"}
  attempt_outcome: {type: enum, values: [EVALUATED, INELIGIBLE, FAILED_BEFORE_EVALUATION], required: true}
  reason_code: {type: enum, values: [TRADE_INTENT_INELIGIBLE, RISK_ENGINE_COMPUTATION_BOUNDARY_ERROR], required: false}
  checked_evidence_refs: {type: array, items: event_record_ref, required: false}
```

**Attempt→RiskEvaluation query (non-authoritative convenience, KHÔNG cần linking event mới):** cho một attempt EVALUATED, resolve RiskEvaluation tương ứng qua HAI cách tương đương — (a) `GetRiskEvaluationForComputation(trade_intent_id, risk_context_cursor, cursor)` (§7); hoặc (b) reverse-lookup trực tiếp trên authoritative RiskEvaluationRecorded stream cho fact có `causation_refs` chứa chính `event_record_ref` của attempt này. Cả hai đều dùng field/cơ chế ĐÃ CÓ SẴN (`causation_refs`, logical computation key) — KHÔNG tạo event/field liên kết mới, đúng đối xứng `decision.md` §4.

## 5. `RiskEvaluationRecorded` — `kind: event`

Kế thừa envelope §3. Payload đặc thù:

```yaml
id: risk-evaluation-recorded
kind: event
capability_id: risk-management
domain_context_id: risk-gateway
description: >
  Fact AUTHORITATIVE cho một lần Risk Gateway đánh giá deterministic — thiết lập TOÀN BỘ nội dung
  (trade evidence, risk evidence axes, sizing/policy evidence, result) cùng lúc, BẤT BIẾN. CHỈ
  được phát khi RiskEvaluationAttemptRecorded (§4) tương ứng có attempt_outcome = EVALUATED (§5a).
invariants:
  - "payload.risk_evaluation_id PHẢI khớp đúng subject_ref.subject_id VÀ payload.trade_intent_id PHẢI khớp đúng subject_ref.scope.trade_intent_id."
  - "envelope.effective_time (risk_evaluation_time) = mặc định bằng risk_context_cursor.recorded_time trừ khi backfill lịch sử tường minh pin giá trị khác."
  - "causation_refs PHẢI chứa RiskEvaluationAttemptRecorded (§4) tương ứng, attempt_outcome = EVALUATED, cùng trade_intent_id/risk_context_cursor — chứng minh attempt đã ghi nhận EVALUATED TRƯỚC khi RiskEvaluation này được tạo. Quan hệ MỘT CHIỀU — attempt KHÔNG mang tham chiếu ngược, loại bỏ circular append-order dependency (đúng bài học §5a intro)."
  - "Nếu logical computation key (trade_intent_id, risk_context_cursor) ĐÃ CÓ một RiskEvaluationRecorded VALID (visible-valid-head, §7) tại thời điểm ghi, RiskEvaluationRecorded MỚI PHẢI resolve/reuse risk_evaluation_id đã tồn tại (evidence giống hệt — §1 idempotency) HOẶC bị reject (evidence khác, chưa invalidate predecessor) — TUYỆT ĐỐI KHÔNG tạo risk_evaluation_id thứ hai cho CÙNG key trừ khi predecessor ĐÃ invalidate VÀ correction lineage (§10) cho phép."
  - "TẤT CẢ risk evidence axes (§5b3) VÀ authoritative evidence facts (§5d) PHẢI resolve deterministic từ authoritative event stream TẠI ĐÚNG risk_context_cursor — KHÔNG dùng bất kỳ latest-state Current View nào (TradeIntentCurrentView, DecisionCurrentView, AccountCurrentView, RiskEvaluationCurrentView) làm input."
```

**§5a — Precondition: RiskEvaluationAttempt EVALUATED, đúng thứ tự (v0.2, đóng `C5-MAJ-01`).** RiskEvaluationRecorded CHỈ được phát SAU KHI một `RiskEvaluationAttemptRecorded` (§4) đã ghi nhận `attempt_outcome = EVALUATED` cho cùng logical computation key — VÀ `EVALUATED` CHỈ ghi SAU KHI bounded policy computation (§5c–§5e) đã hoàn tất trọn vẹn:

```text
1. eligible_for_new_risk_evaluation(trade_intent_id, risk_context_cursor) == true   (trade-intent.md §6a)
→ NẾU false: RiskEvaluationAttemptRecorded(attempt_outcome=INELIGIBLE, reason_code=TRADE_INTENT_INELIGIBLE) ghi — KHÔNG RiskEvaluationRecorded nào phát (Scenario 14, §17). Không cần chạy policy computation.

2. NẾU (1) thỏa: policy engine CHẠY TRỌN VẸN bounded computation (§5c — 13 bước, resolve evidence availability/unit/domain, sizing) TRƯỚC — toàn bộ bundle (trade_evidence, risk_evidence, sizing_evidence, evidence_availability, evidence_facts, result) đã xác định XONG.
   → NẾU lỗi kỹ thuật/domain boundary xảy ra TRONG lúc computation (TRƯỚC khi hoàn tất): RiskEvaluationAttemptRecorded(attempt_outcome=FAILED_BEFORE_EVALUATION) ghi — KHÔNG RiskEvaluationRecorded nào phát, KHÔNG EVALUATED attempt nào để lại (Scenario 2, §17).
   → NẾU computation hoàn tất trọn vẹn (bất kể result cuối là gì — APPROVED/REJECTED/NON_EVALUABLE ĐỀU tính là 'hoàn tất'): RiskEvaluationAttemptRecorded(attempt_outcome=EVALUATED) ghi NGAY SAU, RỒI RiskEvaluationRecorded phát (causation_refs trỏ attempt vừa ghi) với result đã xác định — CẢ BA kết quả đều là fact THẬT (Scenario 1/13/4, §17).

Thứ tự bắt buộc: computation hoàn tất → Attempt EVALUATED ghi → RiskEvaluationRecorded ghi. KHÔNG BAO GIỜ đảo ngược, KHÔNG atomic transaction giữa ba bước (mỗi bước là một append riêng, recoverable độc lập — §2/§4 invariant).
```

**§5b — Trade evidence (BẮT BUỘC, PIN tại risk_context_cursor, COPY làm scalar bất biến):**

```yaml
trade_evidence:
  originating_decision_id: {type: string, required: true, description: "= trade-intent.md §1, copied cho tiện truy vấn/explanation — nguồn authoritative luôn là chính Trade Intent"}
  strategy_instance_id: {type: string, required: true, description: "= trade-intent.md §1"}
  account_id: {type: string, required: true, ref: account, description: "= trade-intent.md §1"}
  environment: {type: enum, values: [PAPER, LIVE], required: true, description: "resolve qua account_id TẠI cursor — KHÔNG dùng AccountCurrentView (account.md §13); v0.1 CHỈ PAPER được policy chấp nhận (§5c)"}
  instrument_selection_ref:
    instrument_id: {type: string, required: true}
    venue_id: {type: string, required: true}
    listing_id: {type: string, required: true}
  direction: {type: enum, values: [LONG, SHORT], required: true, description: "= trade-intent.md §1 — RiskEvaluation KHÔNG BAO GIỜ thay đổi direction"}
  intent_type: {type: enum, values: [OPEN], required: true, description: "= trade-intent.md §1"}
```

`trade_evidence` LUÔN BẮT BUỘC đầy đủ (resolve từ Trade Intent/Decision, đã xác nhận eligible ở §5a mục 1) — KHÔNG conditional theo `evidence_availability` (§5b2), vì đây là precondition đã pass TRƯỚC khi computation bắt đầu, KHÔNG phải evidence được resolve TRONG lúc computation.

**§5b1 — Bounded v0.1 unit model (đóng `C5-MAJ-03`) — KHÔNG general unit framework, KHÔNG FX conversion, KHÔNG signed/netted exposure:**

```yaml
unit_evidence:
  listing_quote_currency: {type: string, required: false, description: "resolve từ TradableListing (instrument_selection_ref, instrument.md — KHÔNG redefine tại đây) — quote asset của listing, ANCHOR cho mọi so sánh currency dưới đây"}
  budget_currency: {type: string, required: false, description: "currency của configured_risk_budget (§5c) — nguồn authoritative = risk_policy_configuration_version_ref"}
  equity_currency: {type: string, required: false, description: "currency của available_account_equity_value (§5d)"}
  exposure_notional_currency: {type: string, required: false, description: "currency của current_instrument_exposure_value (§5d)"}
  reference_price_base_unit: {type: string, required: false, description: "base asset unit của reference_price_value (§5d) — PHẢI = quantity_unit (§5e)"}
  reference_price_quote_currency: {type: string, required: false, description: "quote currency của reference_price_value (§5d)"}
  approved_notional_currency: {type: string, required: false, description: "currency của approved_notional (§5e) — chỉ có mặt khi APPROVED, PHẢI = listing_quote_currency"}
```

**Invariant bắt buộc (v0.1, KHÔNG FX conversion — mọi so sánh currency là string equality TUYỆT ĐỐI, KHÔNG convert):**

```text
budget_currency = equity_currency = exposure_notional_currency = reference_price_quote_currency
  = approved_notional_currency = listing_quote_currency
  → mismatch bất kỳ (khi các field liên quan đều AVAILABLE, §5b2) → result = NON_EVALUABLE,
    rejection_reason = INCOMPATIBLE_EVIDENCE_UNIT (Scenario 6, §17)

reference_price_base_unit = quantity_unit
  → mismatch → result = NON_EVALUABLE, rejection_reason = INCOMPATIBLE_EVIDENCE_UNIT

current_instrument_exposure_value PHẢI được diễn giải là GROSS quote-notional exposure,
KHÔNG signed, KHÔNG netted — dấu âm KHÔNG BAO GIỜ được phép làm giảm projected exposure hay
bypass max_requested_notional cap (§5c bước 10; giá trị âm resolved là REJECTED/INVALID_SIZING_INPUT,
§5c bước 6, Scenario 9 §17) — v0.1 KHÔNG hỗ trợ short-exposure netting/portfolio hedging.
```

**§5b2 — Evidence availability (bảy khóa đóng, năm giá trị đóng, đóng `C5-MAJ-02`) — bounded representation, KHÔNG fabricate placeholder/null ref/sentinel scalar khi evidence không AVAILABLE:**

```yaml
evidence_availability:
  available_account_equity: {type: enum, values: [AVAILABLE, MISSING, INVALID, UNRESOLVABLE, INCOMPATIBLE_UNIT], required: true}
  current_instrument_exposure: {type: enum, values: [AVAILABLE, MISSING, INVALID, UNRESOLVABLE, INCOMPATIBLE_UNIT], required: true}
  reference_price: {type: enum, values: [AVAILABLE, MISSING, INVALID, UNRESOLVABLE, INCOMPATIBLE_UNIT], required: true}
  risk_policy_definition_version: {type: enum, values: [AVAILABLE, MISSING, INVALID, UNRESOLVABLE, INCOMPATIBLE_UNIT], required: true}
  risk_policy_configuration_version: {type: enum, values: [AVAILABLE, MISSING, INVALID, UNRESOLVABLE, INCOMPATIBLE_UNIT], required: true}
  risk_plugin_version: {type: enum, values: [AVAILABLE, MISSING, INVALID, UNRESOLVABLE, INCOMPATIBLE_UNIT], required: true}
  package_build_artifact: {type: enum, values: [AVAILABLE, MISSING, INVALID, UNRESOLVABLE, INCOMPATIBLE_UNIT], required: true}
```

**`evidence_availability` LUÔN LUÔN có mặt đầy đủ bảy khóa, BẤT KỂ `result` cuối cùng** — đây là bằng chứng tường minh policy engine ĐÃ KIỂM TRA từng khóa (KHÔNG phải absence). Invariant:

```text
result ∈ {APPROVED, REJECTED} → TẤT CẢ bảy khóa evidence_availability = AVAILABLE (mọi evidence cần
  cho các check ĐÃ thực hiện đều sẵn sàng; risk_evidence §5b3/evidence_facts §5d field tương ứng
  BẮT BUỘC có mặt với exact ref + copied value)

result = NON_EVALUABLE → ÍT NHẤT MỘT khóa evidence_availability != AVAILABLE (reason xác định class
  lỗi, §5e); field ref/scalar TƯƠNG ỨNG khóa đó TUYỆT ĐỐI ABSENT (KHÔNG fabricate); các khóa VẪN
  AVAILABLE khác CÓ THỂ giữ nguyên ref/scalar (resolved evidence không bị xóa chỉ vì evidence khác
  thiếu — Scenario 4/5, §17)
```

**§5b3 — Risk evidence axes (bốn trục, CONDITIONAL theo `evidence_availability`, đóng `C5-MAJ-02`):**

```yaml
risk_evidence:
  risk_policy_definition_version_ref: {type: string, required: false, description: "trục 1/4 — BẮT BUỘC khi evidence_availability.risk_policy_definition_version = AVAILABLE; TUYỆT ĐỐI ABSENT khi khác. Sở hữu semantic policy meaning, exact immutable pin, KHÔNG BAO GIỜ 'latest' (đúng ADR-013 §2.3 pattern áp dụng lại)"}
  risk_policy_configuration_version_ref: {type: string, required: false, description: "trục 2/4 — BẮT BUỘC khi evidence_availability.risk_policy_configuration_version = AVAILABLE; TUYỆT ĐỐI ABSENT khi khác. Sở hữu configured parameter values (configured_risk_budget, max_requested_notional, sizing_method, quantity_precision, §5c) — NẾU trục này UNRESOLVABLE/MISSING/INVALID, MỌI scalar phụ thuộc (configured_risk_budget/max_requested_notional/quantity_precision/budget_currency) CŨNG TUYỆT ĐỐI ABSENT (Scenario 5, §17)"}
  risk_plugin_version_ref: {type: string, required: false, description: "trục 3/4 — BẮT BUỘC khi evidence_availability.risk_plugin_version = AVAILABLE; TUYỆT ĐỐI ABSENT khi khác. Implementation-release identity, Chapter 9 §9.1 (Locked, áp dụng platform-wide cho mọi Plugin Definition, bao gồm Risk Gateway — KHÔNG phải trục phát minh riêng cho C5)"}
  package_build_artifact_ref: {type: string, required: false, description: "trục 4/4 — BẮT BUỘC khi evidence_availability.package_build_artifact = AVAILABLE; TUYỆT ĐỐI ABSENT khi khác. Exact executable identity đang chạy, Chapter 9 §9.1/ADR-013 §2.5 pattern; hai executable khác bytes PHẢI khác giá trị này"}
```

**Invariant:** bốn trục risk evidence PHẢI persistently resolvable TẠI cursor (Chapter 8 §8.1.1 mục 4) để được coi `AVAILABLE` — nếu KHÔNG (`UNRESOLVABLE`/`MISSING`/`INVALID`), `result = NON_EVALUABLE`, `rejection_reason = RISK_POLICY_EVIDENCE_UNAVAILABLE` (§5e, tách biệt khỏi `REQUIRED_EVIDENCE_UNAVAILABLE` — dành riêng cho `evidence_facts` §5d).

**§5c — Sizing/policy evidence + thuật toán deterministic (v0.2, đóng `C5-MAJ-01`/`C5-MAJ-02`/`C5-MAJ-03`/`C5-MAJ-04`/`C5-MAJ-05`, KHÔNG DSL, KHÔNG liquidation/leverage model):**

```yaml
sizing_evidence:
  sizing_method: {type: enum, values: [FIXED_RISK_BUDGET_NOTIONAL], required: true, description: "v0.1: đúng một giá trị — bounded, mở rộng sau bằng giá trị enum MỚI khi có sizing method khác, KHÔNG redesign shape hiện có. LUÔN có mặt (nguồn phi-configuration, cố định cho v0.1)"}
  configured_risk_budget: {type: decimal, required: false, description: "BẮT BUỘC khi risk_policy_configuration_version_ref AVAILABLE (§5b3); TUYỆT ĐỐI ABSENT khi khác. Domain: finite, > 0 (§5c domain check). Notional budget cho Trade Intent — v0.1 KHÔNG stop-distance/leverage concept"}
  max_requested_notional: {type: decimal, required: false, description: "BẮT BUỘC khi risk_policy_configuration_version_ref AVAILABLE; TUYỆT ĐỐI ABSENT khi khác. Domain: finite, > 0"}
  quantity_precision: {type: integer, required: false, description: "BẮT BUỘC khi risk_policy_configuration_version_ref AVAILABLE; TUYỆT ĐỐI ABSENT khi khác. Domain: integer, >= 0, <= 18 (bounded v0.1 maximum — không tìm thấy repository-wide decimal precision bound sẵn có tại thời điểm author, chọn tường minh 18 theo quy ước phổ biến crypto base-asset decimals, xem self-review)"}
```

**Thuật toán sizing deterministic v0.2 (MỘT quy tắc duy nhất, đánh giá theo ĐÚNG thứ tự dưới — dừng tại check đầu tiên fail, mười ba bước):**

```text
1. Validate Trade Intent eligibility — đã thực hiện ở §5a mục 1 (eligible_for_new_risk_evaluation),
   TRƯỚC KHI bước này bắt đầu. Nếu false, thuật toán KHÔNG chạy (attempt_outcome=INELIGIBLE).

2. Resolve bốn trục risk evidence (§5b3): risk_policy_definition_version_ref/
   risk_policy_configuration_version_ref/risk_plugin_version_ref/package_build_artifact_ref —
   ghi evidence_availability tương ứng (§5b2).

3. Resolve evidence_facts (§5d: available_account_equity/current_instrument_exposure/
   reference_price) VÀ unit_evidence (§5b1) — ghi evidence_availability tương ứng.

4. NẾU BẤT KỲ khóa nào trong {available_account_equity, current_instrument_exposure,
   reference_price} != AVAILABLE:
   → NON_EVALUABLE, rejection_reason = REQUIRED_EVIDENCE_UNAVAILABLE. DỪNG.
   NẾU BẤT KỲ khóa nào trong {risk_policy_definition_version, risk_policy_configuration_version,
   risk_plugin_version, package_build_artifact} != AVAILABLE:
   → NON_EVALUABLE, rejection_reason = RISK_POLICY_EVIDENCE_UNAVAILABLE. DỪNG.

5. NẾU unit_evidence KHÔNG thỏa invariant §5b1 (currency/base-unit mismatch):
   → NON_EVALUABLE, rejection_reason = INCOMPATIBLE_EVIDENCE_UNIT. DỪNG.

6. Validate numeric domain cho MỌI scalar đã resolved (§5c domain — configured_risk_budget finite>0,
   max_requested_notional finite>0, available_account_equity_value finite>=0,
   current_instrument_exposure_value finite>=0, reference_price_value finite>0, quantity_precision
   integer 0..18):
   → NẾU BẤT KỲ scalar nào NGOÀI domain (kể cả current_instrument_exposure_value < 0, Scenario 9):
     REJECTED, rejection_reason = INVALID_SIZING_INPUT. DỪNG. (Exposure âm KHÔNG BAO GIỜ bypass
     cap ở bước 10 — nó bị chặn NGAY TẠI bước domain-validation này.)

7. account_id.current_status(risk_context_cursor) == ACTIVE (account.md §3–§7, reconstruct TẠI cursor)
   → FAIL: REJECTED, rejection_reason = ACCOUNT_NOT_ACTIVE. DỪNG.

8. environment == PAPER (v0.1 — LIVE KHÔNG được policy chấp nhận, tách bạch hoàn toàn khỏi Live
   authorization platform-wide, KHÔNG phải cùng cơ chế)
   → FAIL: REJECTED, rejection_reason = ENVIRONMENT_NOT_ALLOWED. DỪNG.

9. available_account_equity_value >= configured_risk_budget
   → FAIL: REJECTED, rejection_reason = RISK_BUDGET_EXCEEDED. DỪNG.

10. projected_instrument_notional = current_instrument_exposure_value + configured_risk_budget
    (GROSS quote-notional, §5b1 — KHÔNG signed/netted)
    projected_instrument_notional <= max_requested_notional
    → FAIL: REJECTED, rejection_reason = REQUESTED_EXPOSURE_EXCEEDED. DỪNG.

11. approved_notional = configured_risk_budget
    approved_quantity_raw = approved_notional / reference_price_value
    approved_quantity = FLOOR(approved_quantity_raw, quantity_precision)   (luôn floor, KHÔNG
    BAO GIỜ round-up/round-nearest, tránh vượt approved_notional đã duyệt)

12. NẾU approved_quantity == 0:
    → REJECTED, rejection_reason = QUANTITY_ROUNDS_TO_ZERO. approved_quantity/approved_notional
      TUYỆT ĐỐI ABSENT (§5e — REJECTED KHÔNG mang output field, đúng convention §5e). Scenario 8, §17.

13. NGƯỢC LẠI (approved_quantity > 0, strictly positive):
    → APPROVED, approved_notional/approved_quantity/quantity_unit có mặt (§5e).
```

**Invariant:** `approved_quantity` (khi APPROVED) PHẢI **strictly positive** (`> 0`) VÀ finite — bước 12 chặn tường minh trường hợp bằng 0; công thức KHÔNG BAO GIỜ cho kết quả âm/vô cực/NaN vì đã qua domain-validation bước 6. Rounding LUÔN LUÔN floor.

**§5d — Authoritative evidence facts (CONDITIONAL theo `evidence_availability` §5b2, đóng `C5-MAJ-02` — KHÔNG chỉ copied value, KHÔNG redefine Account/Candle/Feature contract):**

```yaml
evidence_facts:
  available_account_equity_ref: {type: event_record_ref, required: false, description: "BẮT BUỘC khi evidence_availability.available_account_equity = AVAILABLE; TUYỆT ĐỐI ABSENT khi khác. Opaque, nguồn cụ thể (Account/Ledger contract) KHÔNG định nghĩa ở đây, deferred §15"}
  current_instrument_exposure_ref: {type: event_record_ref, required: false, description: "BẮT BUỘC khi evidence_availability.current_instrument_exposure = AVAILABLE; TUYỆT ĐỐI ABSENT khi khác. Cho ĐÚNG instrument_selection_ref này — opaque, nguồn cụ thể deferred §15"}
  reference_price_fact_ref: {type: event_record_ref, required: false, description: "BẮT BUỘC khi evidence_availability.reference_price = AVAILABLE; TUYỆT ĐỐI ABSENT khi khác. Opaque, KHÔNG redefine candle.md schema tại đây"}
  available_account_equity_value: {type: decimal, required: false, description: "BẮT BUỘC khi AVAILABLE; TUYỆT ĐỐI ABSENT khi khác. Copied scalar, domain finite>=0 (§5c bước 6)"}
  current_instrument_exposure_value: {type: decimal, required: false, description: "BẮT BUỘC khi AVAILABLE; TUYỆT ĐỐI ABSENT khi khác. Domain finite>=0, GROSS quote-notional (§5b1) — KHÔNG signed"}
  reference_price_value: {type: decimal, required: false, description: "BẮT BUỘC khi AVAILABLE; TUYỆT ĐỐI ABSENT khi khác. Domain finite>0"}
```

**Invariant no-look-ahead (I-3):** mọi `*_ref` PRESENT (AVAILABLE) trong `evidence_facts` PHẢI thỏa `fact.recorded_time ≤ risk_context_cursor.recorded_time` — vi phạm → invalid RiskEvaluationRecorded, PHẢI bị từ chối khi append. **Trường hợp một evidence fact KHÔNG resolvable/invalid/missing TẠI cursor** (ví dụ chưa có candle nào, chưa có equity snapshot nào visible): `evidence_availability` tương ứng ghi `MISSING`/`INVALID`/`UNRESOLVABLE` (§5b2), field ref/scalar tương ứng TUYỆT ĐỐI ABSENT (KHÔNG fabricate placeholder/null ref/sentinel scalar), `result = NON_EVALUABLE`, `rejection_reason = REQUIRED_EVIDENCE_UNAVAILABLE` (§5e, Scenario 4) — attempt VẪN `EVALUATED` (engine đã chạy trọn vẹn tới bước xác định NON_EVALUABLE, §5a, KHÔNG phải `attempt_outcome=INELIGIBLE`/`FAILED_BEFORE_EVALUATION`).

**§5e — Result (v0.2, đóng `C5-MAJ-02`/`C5-MAJ-04`):**

```yaml
result: {type: enum, values: [APPROVED, REJECTED, NON_EVALUABLE], required: true}
rejection_reason: {type: enum, values: [ACCOUNT_NOT_ACTIVE, ENVIRONMENT_NOT_ALLOWED, INVALID_SIZING_INPUT, RISK_BUDGET_EXCEEDED, REQUESTED_EXPOSURE_EXCEEDED, QUANTITY_ROUNDS_TO_ZERO, REQUIRED_EVIDENCE_UNAVAILABLE, RISK_POLICY_EVIDENCE_UNAVAILABLE, INCOMPATIBLE_EVIDENCE_UNIT], required: false, description: "BẮT BUỘC khi result ∈ {REJECTED, NON_EVALUABLE}; TUYỆT ĐỐI ABSENT khi APPROVED. {REQUIRED_EVIDENCE_UNAVAILABLE, RISK_POLICY_EVIDENCE_UNAVAILABLE, INCOMPATIBLE_EVIDENCE_UNIT} CHỈ hợp lệ với result=NON_EVALUABLE; sáu giá trị còn lại CHỈ hợp lệ với result=REJECTED."}
approved_notional: {type: decimal, required: false, description: "BẮT BUỘC khi APPROVED; TUYỆT ĐỐI ABSENT khi khác (kể cả REJECTED/QUANTITY_ROUNDS_TO_ZERO — xem §5c bước 12) — xem §5c"}
approved_quantity: {type: decimal, required: false, description: "BẮT BUỘC khi APPROVED; TUYỆT ĐỐI ABSENT khi khác — xem §5c, STRICTLY POSITIVE (> 0), finite, floor-rounded theo quantity_precision (đóng C5-MAJ-04)"}
quantity_unit: {type: string, required: false, description: "BẮT BUỘC khi APPROVED — đơn vị base asset của instrument_selection_ref (ví dụ 'BTC'), copied scalar, nguồn = instrument.md (không redefine tại đây); PHẢI = unit_evidence.reference_price_base_unit (§5b1)"}
```

**Ba trường hợp PHÂN BIỆT tường minh (đúng yêu cầu "do not collapse"):** `APPROVED` (policy evaluated, tất cả check pass, `approved_quantity > 0`); `REJECTED` (policy evaluated, MỘT check cụ thể fail — reason ∈ {ACCOUNT_NOT_ACTIVE, ENVIRONMENT_NOT_ALLOWED, INVALID_SIZING_INPUT, RISK_BUDGET_EXCEEDED, REQUESTED_EXPOSURE_EXCEEDED, QUANTITY_ROUNDS_TO_ZERO}); `NON_EVALUABLE` (policy engine chạy nhưng evidence bắt buộc thiếu/invalid/unresolved/incompatible-unit — reason ∈ {REQUIRED_EVIDENCE_UNAVAILABLE, RISK_POLICY_EVIDENCE_UNAVAILABLE, INCOMPATIBLE_EVIDENCE_UNIT}). Tách biệt khỏi `attempt_outcome ∈ {INELIGIBLE, FAILED_BEFORE_EVALUATION}` (§2/§4 — hai trường hợp KHÔNG có RiskEvaluationRecorded nào cả).

## 6. `RiskEvaluationFactInvalidated` — `kind: event`

Kế thừa envelope §3. `causation_refs` không rỗng.

```yaml
id: risk-evaluation-fact-invalidated
kind: event
capability_id: risk-management
domain_context_id: risk-gateway
description: >
  Phủ định MỘT RiskEvaluationRecorded ĐÃ SAI thực tế. Correction lineage CHO PHÉP một replacement
  RiskEvaluationRecorded MỚI (risk_evaluation_id khác, supersedes_fact_ref trỏ về đây) CÙNG logical
  computation key — đúng semantic đã proven tại decision.md §6/§11.
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT risk_evaluation_time của RiskEvaluationRecorded bị invalidate."
  - "invalidated_fact_ref PHẢI trỏ một RiskEvaluationRecorded, CHƯA từng nhận invalidation khác — một fact chỉ bị invalidate đúng một lần. KHÔNG BAO GIỜ trỏ một RiskEvaluationFactInvalidated/RiskEvaluationAttemptRecorded khác."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead)."
  - "Sau invalidation, risk_evaluation_id đó VĨNH VIỄN TERMINALLY_INVALID (§7) — KHÔNG BAO GIỜ có replacement dưới CÙNG risk_evaluation_id. Logical computation key (trade_intent_id, risk_context_cursor) CÓ THỂ nhận một RiskEvaluationRecorded MỚI (risk_evaluation_id khác, supersedes_fact_ref = event này) — xem §10 cho invariant đầy đủ."
  - "Nếu risk_evaluation_id bị invalidate đã có ExecutionIntentIssued (execution-intent.md §3) trỏ về nó, Execution Intent liên quan KHÔNG tự động invalidate — Execution Intent lifecycle độc lập; origin-validity của Execution Intent đó cho Order creation MỚI được xử lý qua `eligible_for_new_order_creation` (execution-intent.md §6a), KHÔNG qua cascade tự động ở đây (Scenario 11, §17)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 7. `RiskEvaluationCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §5–§6.

```text
Trước khi bất kỳ RiskEvaluationRecorded nào tồn tại cho một logical computation key:
  → KHÔNG có RiskEvaluationCurrentView row nào tồn tại
  → GetRiskEvaluationForComputation trả về NOT_FOUND / ABSENT
```

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION`. Khi `PENDING_CORRECTION`, `pending_correction_class` BẮT BUỘC có mặt — CHỈ MỘT giá trị khả dĩ (logical key luôn CÓ THỂ nhận replacement, đúng semantic đã proven tại `decision.md` §8):

```text
view_state = VALID              → pending_correction_class: CẤM (phải absent)
view_state = PENDING_CORRECTION → pending_correction_class = AWAITING_SAME_SUBJECT_REPLACEMENT (LUÔN LUÔN)
```

**Fold algorithm (visible-valid-head per LOGICAL COMPUTATION KEY, đúng semantic đã proven tại `decision.md` §8):**

```text
1. Group mọi RiskEvaluationRecorded/RiskEvaluationFactInvalidated theo logical computation key
   (trade_intent_id, risk_context_cursor).
2. Trong một key, dựng chain theo supersedes_fact_ref: R1 (gốc, KHÔNG supersedes_fact_ref) → R2
   (supersedes_fact_ref = R1) → ... (cấm fork, §10 invariant).
3. Với mỗi Ri trong chain, resolve RiskEvaluationFactInvalidated visibility tại cursor.
4. Duyệt chain từ R1: dừng tại link ĐẦU TIÊN chưa bị invalidate visible tại cursor — đó là visible
   valid head. current risk_evaluation_id = head đó.
5. NẾU link cuối cùng đã duyệt bị invalidate visible VÀ KHÔNG CÓ link kế tiếp visible → view_state =
   PENDING_CORRECTION, pending_correction_class = AWAITING_SAME_SUBJECT_REPLACEMENT, DỪNG.
6. NẾU tìm được head hợp lệ → view_state = VALID, resolve toàn bộ payload RiskEvaluationRecorded
   của head đó làm scope hiện tại.
```

```yaml
id: risk-evaluation-current-view
kind: read_model
capability_id: risk-management
domain_context_id: risk-gateway
description: >
  Projection tiện dụng cho query/UI, KHÔNG BAO GIỜ là input hợp lệ cho Execution Intent/Order hay
  bất kỳ computation nào khác — cùng nguyên tắc Current-View-never-authority. Downstream field
  PHẢI resolve qua authoritative RiskEvaluation event stream (`ref: risk`) TẠI CÙNG cursor mà
  computation đó đang dùng (§13). Cache chỉ chấp nhận khi ĐỒNG THỜI cursor-addressable VÀ provably
  equivalent với authoritative reconstruction.
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho Execution Intent/Order hay bất kỳ computation nào khác — CHỈ query/UI."
  - "view_state PHẢI đúng theo Bước 4–5 của fold algorithm — visible-valid-head chain quyết định."
  - "pending_correction_class BẮT BUỘC có mặt khi view_state = PENDING_CORRECTION (luôn = AWAITING_SAME_SUBJECT_REPLACEMENT); CẤM có mặt khi view_state = VALID."
schema:
  trade_intent_id: {type: string, required: true, description: "một phần logical computation key"}
  risk_context_cursor: {type: object, required: true, description: "phần còn lại logical computation key"}
  current_risk_evaluation_id: {type: string, required: false, description: "risk_evaluation_id của visible valid head — chỉ có mặt khi view_state = VALID"}
  scope: {result: string, required: true, description: "chỉ có mặt khi view_state = VALID — toàn bộ payload head hiện hành"}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  pending_correction_class: {type: enum, values: [AWAITING_SAME_SUBJECT_REPLACEMENT], required: false}
  last_recorded_time: timestamp
queries: [GetRiskEvaluationForComputation, GetRiskEvaluationById, GetRiskEvaluationHistory]
```

## 8. Explanation contract

**Explanation là derived, non-authoritative rendering — KHÔNG UI copy, KHÔNG natural-language generation infrastructure.** Structured evaluation facts (§5b–§5e) là authoritative; text rendering CHỈ là một hàm thuần túy của evidence đã có.

```text
Explanation(risk_evaluation_id) = deterministic render của {trade_evidence, unit_evidence,
evidence_availability, risk_evidence, sizing_evidence, evidence_facts, result} — KHÔNG computation
mới, KHÔNG external lookup, KHÔNG dùng bất kỳ giá trị nào không có mặt trong §5b–§5e.
```

Ví dụ walking-skeleton (đúng Scenario 1, §17) — render tương đương:

```text
Trade Intent eligible: true
Account active: true
Environment allowed: PAPER
Configured risk budget: 100 USDT
Maximum notional: 5,000 USDT
Result: APPROVED
Approved quantity: 0.04 BTC
```

**Invariant:** hai RiskEvaluation với cùng evidence PHẢI cho cùng explanation render (deterministic). Explanation KHÔNG có event/subject riêng — một PROJECTION thuần túy của RiskEvaluationRecorded.

## 9. Risk-Evaluation-to-Execution-Intent cardinality — xem `execution-intent.md` §7

Định nghĩa authoritative đầy đủ tại [`execution-intent.md`](./execution-intent.md) §7 — risk.md KHÔNG lặp lại, chỉ tái khẳng định ràng buộc chiều ngược:

```text
result = APPROVED  →  zero HOẶC MỘT ExecutionIntentIssued, keyed unique bởi originating_risk_evaluation_id
result = REJECTED | NON_EVALUABLE  →  ZERO Execution Intent LUÔN LUÔN
```

RiskEvaluation KHÔNG tự tuyên bố đã issue Execution Intent hay chưa — KHÔNG field nào trên RiskEvaluationRecorded claim điều đó (đúng bài học đã proven tại `decision.md` §10, đóng trước lớp lỗi `C4-MAJ-01`-style ngay từ v0.1). Câu hỏi resolve trực tiếp bằng query authoritative Execution Intent stream lọc `originating_risk_evaluation_id`.

## 10. Correction lineage

Correction lineage scoped chính xác theo LOGICAL COMPUTATION KEY `(trade_intent_id, risk_context_cursor)` — mỗi key có chuỗi lineage RIÊNG, đúng semantic đã proven tại `decision.md` §11.

```text
R1 (RiskEvaluationRecorded, KHÔNG supersedes_fact_ref)
  → RiskEvaluationFactInvalidated targeting R1
  → R2 (RiskEvaluationRecorded MỚI — risk_evaluation_id KHÁC R1, CÙNG trade_intent_id, CÙNG
    risk_context_cursor, supersedes_fact_ref = fact R1)

Correction tiếp theo:
R2 → RiskEvaluationFactInvalidated targeting R2 → R3, supersedes_fact_ref = R2
  (KHÔNG được supersedes_fact_ref = R1 — cấm nhảy cóc)
```

**Mười invariant bắt buộc** (đối xứng `decision.md` §11):

1. RiskEvaluation gốc (R1, KHÔNG có predecessor) KHÔNG có `supersedes_fact_ref`.
2. Replacement (correction) BẮT BUỘC có `supersedes_fact_ref`, trỏ đúng fact bị invalidate.
3. Replacement PHẢI CÙNG `trade_intent_id` VÀ CÙNG `risk_context_cursor` với fact bị supersede (logical key bất biến xuyên chain, dù `risk_evaluation_id` đổi).
4. `causation_refs` của replacement PHẢI chứa chính `RiskEvaluationFactInvalidated` targeting predecessor — predecessor PHẢI đã invalidate VÀ visible TRƯỚC khi replacement được ghi.
5. Replacement PHẢI supersede đúng lineage head hiện tại — không nhảy cóc qua một head trung gian.
6. Một fact bị invalidate có **tối đa một** replacement authoritative trực tiếp — cấm fork.
7. Replacement không được "visible" (`recorded_time`) trước invalidation tương ứng.
8. Mọi lineage member lịch sử giữ nguyên trong log — append-only (I-3), không mutate; `risk_evaluation_id` cũ (R1) vẫn resolvable mãi mãi qua `GetRiskEvaluationById`.
9. Một fact đã invalidate **không bao giờ** bị tái sử dụng ngầm — `RiskEvaluationCurrentView` (§7) phải loại trừ nó tường minh.
10. Retry của cùng logical key với evidence KHÁC, KHI predecessor CHƯA invalidate, VẪN LÀ conflict (KHÔNG tự động trở thành correction) — correction CHỈ hợp lệ qua chuỗi tường minh invalidate-rồi-replace ở trên.

**Execution Intent derived từ một RiskEvaluation bị invalidate KHÔNG tự động rewrite/xóa** — historical fact, ineligible cho Order creation mới qua `eligible_for_new_order_creation` (execution-intent.md §6a), KHÔNG cascade tự động (Scenario 11/12, §17). Replacement approved RiskEvaluation (R2) CÓ THỂ derive Execution Intent RIÊNG của nó.

## 11. Time semantics và bitemporal correctness

- `effective_time` (semantic `risk_evaluation_time` trên RiskEvaluationRecorded) — required trên mọi event trong tài liệu này. KHÔNG `decision_time`/`decision_context_cursor` (envelope-level) — những field đó CHỈ thuộc `decision.md`'s `DecisionRecorded`.
- `recorded_time` — recorded axis, universal.
- **No-future-input (I-3):** `evidence_fact.recorded_time ≤ risk_context_cursor.recorded_time ≤ RiskEvaluationRecorded.recorded_time`.
- **Replay tại cursor T** chỉ thấy fact có `recorded_time ≤ T` — invalidation/replacement ghi SAU T KHÔNG visible tại T. Replay TRƯỚC một correction thấy R1; replay SAU correction thấy R2.
- `market_time` PROHIBITED xuyên suốt tài liệu này.

## 12. Canonical policy identifiers — nguồn duy nhất (context `risk-gateway`)

**Bốn canonical policy identifier, khai báo ĐÚNG MỘT LẦN tại đây cho context `risk-gateway`** — đúng pattern đã proven tại `decision.md` §13, khai báo ĐỘC LẬP vì đây là context khác:

```yaml
initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS
risk_computation_idempotency_policy: STABLE_KEY_SAME_EVIDENCE_IS_IDEMPOTENT
risk_evaluation_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT
risk_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE
```

**`initial_fact_correction_policy`** — áp dụng CHỈ cho `RiskEvaluationAttemptRecorded` (§4, KHÔNG có same-ID replacement — attempt sai thực tế deferred §15). `RiskEvaluationRecorded` KHÔNG dùng policy này thuần túy — xem `risk_correction_lineage_policy` dưới.

**`risk_computation_idempotency_policy: STABLE_KEY_SAME_EVIDENCE_IS_IDEMPOTENT`** — logical computation key = `(trade_intent_id, risk_context_cursor)`; retry cùng key + cùng evidence (chưa invalidate) → idempotent no-op; retry cùng key + evidence KHÁC (chưa invalidate predecessor) → reject tường minh (§1, §10 invariant 10). Policy CỦA RISKEVALUATION, KHÔNG phải của Attempt.

**`risk_evaluation_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT`** — idempotency scoped theo TỪNG `evaluation_attempt_id` cá nhân, KHÔNG theo logical computation key: retry CÙNG `evaluation_attempt_id` + CÙNG payload → idempotent no-op; CÙNG `evaluation_attempt_id` + payload KHÁC → deterministic conflict. Logical computation key KHÔNG BẮT BUỘC unique — nhiều attempt (kể cả outcome khác nhau) CÓ THỂ tồn tại cùng key.

**`risk_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE`** — correction RiskEvaluationRecorded KHÔNG same-ID replacement (risk_evaluation_id vẫn bất biến/không tái sử dụng per-fact), NHƯNG logical computation key CÓ THỂ nhận RiskEvaluationRecorded MỚI (risk_evaluation_id khác) sau khi predecessor invalidate — mười invariant đầy đủ tại §10.

## 13. Downstream reference contract (cho Execution Intent §5, và Package 0.2-C6 Order — chưa author)

`execution-intent.md` và Package 0.2-C6 (Order, chưa author) tham chiếu RiskEvaluation qua ĐÚNG các field sau, KHÔNG hơn:

```yaml
risk_evaluation_id: {type: string, required: true, ref: risk}
trade_intent_id: {type: string, description: "= subject_ref.scope.trade_intent_id"}
risk_context_cursor: {type: object, description: "= §3 — cùng logical computation key"}
account_id: {type: string, ref: account, description: "= trade_evidence.account_id, §5b"}
instrument_selection_ref: {type: object, description: "= trade_evidence.instrument_selection_ref, §5b — {instrument_id, venue_id, listing_id}"}
direction: {type: enum, values: [LONG, SHORT], description: "= trade_evidence.direction, §5b"}
result: {type: enum, values: [APPROVED, REJECTED, NON_EVALUABLE], description: "= §5e"}
approved_quantity: {type: decimal, description: "= §5e, chỉ có mặt khi result=APPROVED — GUARANTEE (v0.2, đóng C5-MAJ-04): khi có mặt, LUÔN strictly positive (> 0), KHÔNG BAO GIỜ 0"}
quantity_unit: {type: string, description: "= §5e, chỉ có mặt khi result=APPROVED"}
risk_evaluation_time: {type: timestamp, description: "= §3/§5"}
```

**Downstream authority rule — MỘT quy tắc duy nhất, không ngoại lệ:** downstream contract PHẢI resolve mọi field trên TRỰC TIẾP từ authoritative RiskEvaluation event stream (§4–§6) TẠI ĐÚNG cursor mà chính computation đó đang dùng. `RiskEvaluationCurrentView` latest-state (§7) KHÔNG BAO GIỜ được dùng làm input. **Consumer cần biết "risk_evaluation_id X còn valid hay đã bị supersede" PHẢI dùng `GetRiskEvaluationById` (§7) hoặc reconstruct trực tiếp — KHÔNG giả định risk_evaluation_id một khi tồn tại thì mãi mãi là visible-valid-head cho key của nó.** `risk.md` KHÔNG author semantics của Execution Intent contents/lifecycle (thuộc `execution-intent.md`) hay Order (Package 0.2-C6, chưa author).

## 14. Prohibitions

**RiskEvaluation/RiskEvaluationAttempt KHÔNG được sở hữu:** Strategy/Decision/Trade Intent identity semantics; Execution Intent contents/lifecycle/derivation idempotency (thuộc `execution-intent.md`); Order/Fill/Position/Replay Event semantics (Package 0.2-C6–C7, chưa author); order type/limit price/stop price/exchange payload/order routing/exchange adapter behavior; general Risk DSL; portfolio-level arbitration/multi-account netting/advanced margin/liquidation model; UI copy/natural-language generation infrastructure; Account/Candle/Feature/Decision/Trade Intent contract schema; database transaction/outbox/message-broker technology; general workflow/saga engine; broad runtime exception telemetry/observability infrastructure; backtest/optimizer infrastructure; **(v0.2, đóng `C5-MAJ-03`) FX conversion giữa các currency khác nhau; signed/netted exposure arithmetic; general unit/currency framework (chỉ bounded v0.1 unit model §5b1).**

## 15. Ngoài phạm vi — defer

- Stream Registry/Input Contract implementation cụ thể — `risk_context_cursor` field SHAPE pin ngay v0.1, MECHANISM resolve deferred Phase 1.
- Nguồn cụ thể của `available_account_equity_ref`/`current_instrument_exposure_ref` (Account/Ledger contract cụ thể) — risk.md KHÔNG redefine Account contract, opaque reference.
- `sizing_method` khác `FIXED_RISK_BUDGET_NOTIONAL` — mở rộng khi có nhu cầu thực tế, KHÔNG thiết kế trước (tránh Risk DSL tổng quát).
- Correction lineage riêng cho `RiskEvaluationAttempt` — edge case hiếm, immutable append-only đủ cho v0.1.
- Granular exception/technical-failure sub-taxonomy cho `FAILED_BEFORE_EVALUATION` — v0.1 CHỈ một reason_code.
- Implementation technology cho cross-stream RiskEvaluation→Execution Intent recovery (retry queue/outbox/message-broker) — boundary semantic pin, KHÔNG chọn công nghệ.
- `environment = LIVE` policy support — v0.1 CHỈ PAPER, LIVE rejection là bounded policy value, KHÔNG phải Live authorization mechanism (tách bạch hoàn toàn).
- Portfolio-level risk/multi-strategy capital allocation/dynamic leverage/liquidation model — hoàn toàn ngoài phạm vi.
- Order/Execution/Fill/Position semantics — hoàn toàn ngoài phạm vi Domain Contract này (Package 0.2-C6–C7).
- **`quantity_precision` maximum = 18 (v0.2, đóng `C5-MAJ-05`, disclosed judgment call):** tại thời điểm author, KHÔNG tìm thấy một repository-wide decimal precision bound sẵn có/authoritative nào trong Constitution hay Domain Contract khác đã Consolidated Stable/Locked. `18` được chọn tường minh làm bounded v0.1 maximum (theo quy ước phổ biến crypto base-asset decimal precision), KHÔNG phải giá trị đã được platform pin từ trước — nếu về sau có một bound authoritative chung được thiết lập (ví dụ tại Chapter 9 hay một ADR mới), giá trị này PHẢI được rà soát lại và có thể cần một correction riêng.
- Cơ chế cụ thể resolve `evidence_availability` (§5b2) — v0.2 CHỈ pin SHAPE (bảy khóa, năm giá trị) và invariant kết quả, KHÔNG pin cơ chế/thuật toán cụ thể engine dùng để xác định MISSING/INVALID/UNRESOLVABLE/INCOMPATIBLE_UNIT — deferred Phase 1.
- Cơ chế cụ thể resolve `unit_evidence` (§5b1, ví dụ tra cứu TradableListing quote asset) — deferred Phase 1, KHÔNG redefine instrument.md tại đây.

## 16. Open questions ngoài phạm vi

- Cơ chế cụ thể generate `risk_evaluation_id`/`evaluation_attempt_id` — chưa quyết, Phase 1.
- Retention/resolvability horizon cụ thể cho RiskEvaluation/RiskEvaluationAttempt đã lâu.
- Không đóng OQ-002/OQ-003.

## 17. Acceptance scenarios (v0.2, mười hai scenario đóng bounded correction + sáu scenario nền tảng kế thừa — validation, không phải executable test tại C5)

**Scenario 1 — Truthful successful attempt:** Trade Intent valid, ISSUED, LONG/OPEN, PAPER. Bounded policy computation (§5c, 13 bước) chạy TRỌN VẸN tới bước 13 → `RiskEvaluationAttemptRecorded(attempt_outcome=EVALUATED)` ghi NGAY SAU KHI computation hoàn tất (§5a) → `RiskEvaluationRecorded` ghi ngay sau, `causation_refs` trỏ ĐÚNG attempt đó, `result=APPROVED`, `approved_quantity` strictly positive. KHÔNG fact nào tuyên bố "hoàn tất" trước khi computation thực sự hoàn tất.

**Scenario 2 — Crash before computation completion:** Engine crash giữa lúc đang chạy §5c (TRƯỚC KHI hoàn tất trọn vẹn 13 bước) → KHÔNG `EVALUATED` attempt nào được ghi cho lần thử này: hoặc KHÔNG ghi gì (retry tạo `evaluation_attempt_id` MỚI), hoặc ghi `FAILED_BEFORE_EVALUATION` (§5a mục 2). Ví dụ cụ thể: Attempt A1 (`FAILED_BEFORE_EVALUATION`) ghi nhận; Attempt A2 (CÙNG logical cursor, `EVALUATED`) ghi nhận sau đó khi retry thành công — HỢP LỆ, KHÔNG mâu thuẫn với A1 (§2/§4).

**Scenario 3 — Crash after completed Attempt (recoverable append gap):** Computation đã hoàn tất trọn vẹn, `RiskEvaluationAttemptRecorded(EVALUATED)` đã ghi thành công, NHƯNG engine crash TRƯỚC KHI `RiskEvaluationRecorded` kịp append → recovery logic (Phase 1) resolve deterministic: re-run CÙNG computation tại CÙNG `(trade_intent_id, risk_context_cursor)`, tái sử dụng CHÍNH `evaluation_attempt_id` đã `EVALUATED` đó (KHÔNG tạo attempt mới), append/reuse ĐÚNG MỘT `RiskEvaluationRecorded` referencing attempt đó (§2 invariant, đóng `C5-MAJ-01`).

**Scenario 4 — Missing equity evidence:** `evidence_availability.available_account_equity = MISSING` (hoặc `UNRESOLVABLE`/`INVALID`) → `result=NON_EVALUABLE`, `rejection_reason=REQUIRED_EVIDENCE_UNAVAILABLE`, `available_account_equity_ref`/`available_account_equity_value` TUYỆT ĐỐI ABSENT (KHÔNG fabricate placeholder ref/null/sentinel scalar) — zero Execution Intent (§5b2/§5d/§5e).

**Scenario 5 — Unresolved policy configuration:** `evidence_availability.risk_policy_configuration_version = UNRESOLVABLE` → `risk_policy_configuration_version_ref` TUYỆT ĐỐI ABSENT, VÀ mọi scalar phụ thuộc (`configured_risk_budget`/`max_requested_notional`/`quantity_precision`/`budget_currency`) CŨNG TUYỆT ĐỐI ABSENT → `result=NON_EVALUABLE`, `rejection_reason=RISK_POLICY_EVIDENCE_UNAVAILABLE` (§5b3/§5c).

**Scenario 6 — Unit mismatch:** `equity_currency=USD`, `listing_quote_currency=USDT` (mismatch phát hiện dù cả hai `evidence_availability` liên quan đều `AVAILABLE`) → `result=NON_EVALUABLE`, `rejection_reason=INCOMPATIBLE_EVIDENCE_UNIT` (§5b1 invariant, §5c bước 5) — KHÔNG FX-convert để "sửa".

**Scenario 7 — Valid unit chain:** mọi currency liên quan (`budget`/`equity`/`exposure`/`reference_price` quote/`approved_notional`) đều `USDT`, `quantity_unit=BTC`, `reference_price_base_unit=BTC`, `reference_price_quote_currency=USDT` → §5b1 invariant thỏa mãn hoàn toàn → computation tiếp tục bình thường qua §5c bước 6 trở đi (arithmetic hợp lệ).

**Scenario 8 — Zero quantity after rounding:** `approved_notional / reference_price_value` floor-rounded theo `quantity_precision` cho kết quả `0` (ví dụ `configured_risk_budget` nhỏ, `reference_price` rất cao) → `result=REJECTED`, `rejection_reason=QUANTITY_ROUNDS_TO_ZERO`, `approved_quantity`/`approved_notional` TUYỆT ĐỐI ABSENT, zero Execution Intent (§5c bước 12).

**Scenario 9 — Negative exposure:** `current_instrument_exposure_value` resolved là số âm (vi phạm domain `finite, >=0`, §5c bước 6) → `result=REJECTED`, `rejection_reason=INVALID_SIZING_INPUT` — KHÔNG được dùng để giảm `projected_instrument_notional` hay bypass `max_requested_notional` cap (chặn NGAY tại domain-validation bước 6, TRƯỚC bước 10 cap-check).

**Scenario 10 — Valid approval:** mọi evidence `AVAILABLE`, unit chain hợp lệ (Scenario 7), mọi domain check pass, mọi threshold check pass (bước 7–10), `approved_quantity` strictly positive sau floor-rounding → `result=APPROVED`, zero hoặc một Execution Intent theo idempotency (§9, `execution-intent.md` §10).

**Scenario 11 — Trade Intent invalidated after Risk approval:** R1 `APPROVED` → E1 `ISSUED` (referencing R1) → sau đó Trade Intent gốc bị invalidate (originating Decision supersede) → E1 vẫn historical, KHÔNG tự động rewrite, `eligible_for_new_order_creation(E1, cursor sau invalidation)=false` (`execution-intent.md` §6a mục 5: `eligible_for_new_risk_evaluation(trade_intent_id, C)==false`) — ineligible cho Order creation mới.

**Scenario 12 — Risk replacement chain:** R1 `APPROVED` → invalidate R1 (correction, §10) → R2 CÙNG logical key, `risk_evaluation_id` MỚI, `APPROVED`, visible valid head MỚI → Execution Intent E1 (từ R1) trở thành ineligible cho Order creation mới (R1 không còn valid APPROVED head cho key của nó, `execution-intent.md` §6a mục 2 fail) → R2 CÓ THỂ derive Execution Intent MỚI E2 (idempotency theo R2, KHÔNG theo E1) — KHÔNG history rewrite, E1 vẫn tồn tại nguyên vẹn.

**Scenario 13 — Risk budget exceeded:** `available_account_equity_value < configured_risk_budget` → `result=REJECTED`, `rejection_reason=RISK_BUDGET_EXCEEDED`, zero Execution Intent (§5c bước 9).

**Scenario 14 — Trade Intent ineligible:** originating Decision đã invalidate/supersede → `eligible_for_new_risk_evaluation=false` (`trade-intent.md` §6a) → `RiskEvaluationAttemptRecorded(attempt_outcome=INELIGIBLE, reason_code=TRADE_INTENT_INELIGIBLE)` — KHÔNG RiskEvaluation, KHÔNG Execution Intent (§5a mục 1).

**Scenario 15 — Same evaluation retry:** cùng logical Risk computation key + cùng evidence → trả về RiskEvaluation đã tồn tại (idempotent, §1/§12); evidence khác (chưa invalidate) → deterministic conflict.

**Scenario 16 — Cross-stream recovery:** RiskEvaluation R1 `APPROVED` tồn tại; `ExecutionIntentIssued` append ban đầu bị miss; retry bằng `originating_risk_evaluation_id` (`execution-intent.md` §10) → đúng MỘT E1 (idempotent). R1 KHÔNG BAO GIỜ tự tuyên bố "đã issue" sai sự thật — KHÔNG field nào trên RiskEvaluationRecorded claim điều đó (§5e/§9).

**Scenario 17 — Time ordering:** `ExecutionIntentIssued.effective_time < risk_evaluation_time` → reject (`execution-intent.md` §3/§9).

**Scenario 18 — Direction and scope preservation:** Execution Intent KHÔNG được thay đổi `direction` (LONG→SHORT), `account_id`, hay `instrument_selection_ref` so với RiskEvaluation gốc — mismatch bất kỳ PHẢI reject (`execution-intent.md` §3).
