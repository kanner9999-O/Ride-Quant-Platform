---
id: decision
title: Decision
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

# Decision

> **Vai trò của tài liệu này:** Một trong hai Domain Contract của Package 0.2-C4 (Trade Intent and Decision Foundation) — định nghĩa **Decision**, bản ghi authoritative của MỘT lần Strategy Instance đánh giá deterministic tại một computation cursor cụ thể. Draft, chưa Approved/Locked. Thuộc capability `decision-management` / context `strategy-decision` (đăng ký MỚI tại [`context-map.yaml`](./context-map.yaml) trong transaction này). Kiến trúc controlling: [ADR-010](../adr/ADR-010.md) **Approved** (Decision Time Model — `decision_time`/`decision_context_cursor`/Append-and-Revalidate), [Chapter 8 §8.2.1/§8.4/§8.4.1/§8.5](../constitution/08-event-model.md) (Locked, decision-class event cardinality + canonical Replay Cursor schema), [ADR-013](../adr/ADR-013.md) v0.3 Approved (bốn trục evidence độc lập, qua `strategy.md`), [`strategy.md`](./strategy.md) v0.3 Draft §9a/§10 (computation eligibility + chín-field evidence). Tài liệu này CHỈ implement field/invariant mà các nguồn trên yêu cầu, KHÔNG lặp lại toàn văn, KHÔNG tự quyết architecture mới ngoài phạm vi đã khóa.

Decision **KHÔNG phải** Strategy/Strategy Instance (`strategy.md`, đã author), KHÔNG phải Trade Intent (`trade-intent.md`, author cùng transaction này nhưng file riêng), KHÔNG phải Risk Action/Risk Approval, KHÔNG phải Execution Intent/Order/Fill/Position/Replay Event (Package 0.2-C5–C7, chưa author), KHÔNG phải một workflow engine hay rule DSL. Nó là **bản ghi authoritative, bitemporal, deterministic, tự-giải-thích được** của một lần đánh giá — trả lời chính xác bảy câu hỏi: Strategy Instance nào đánh giá? Trục evidence chính xác nào được dùng? Rule nào được đánh giá? Input authoritative nào visible? Kết quả gì? Tại sao? Có tạo Trade Intent không?

**Ví dụ walking-skeleton duy nhất dùng để validate thiết kế (KHÔNG phải yêu cầu xây dựng DSL tổng quát):** "Go LONG khi candle hiện tại đóng cửa strictly above EMA(period), và candle trước đóng cửa ≤ EMA trước đó." Bảy Scenario chấp nhận (A–G, xem §16) đều dựa trên ví dụ này.

**`decision-recorded`/`decision-fact-invalidated`/`decision-revalidated`/`decision-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây, tách biệt display name/`event_type`, cùng nguyên tắc mọi Domain Contract trước.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/C1/C2/C3** (đóng trước, không chờ review round phát hiện): opaque identity không derive từ scope; envelope binding cho `*FactInvalidated`; correction lineage; fold algorithm "visible-valid-head per slice" cho Current View; Current View KHÔNG BAO GIỜ authority; canonical policy identifier khai báo ĐÚNG MỘT NƠI, độc lập theo context.

**Phạm vi bounded tường minh (v0.1):** KHÔNG author Risk/Execution Intent/Order/Fill/Position/Replay Event (Package 0.2-C5–C7). KHÔNG định nghĩa order type/limit price/stop price/exchange payload. KHÔNG định nghĩa position sizing/capital allocation/portfolio arbitration. KHÔNG xây dựng DSL/expression language/parser/rule graph/strategy compiler tổng quát — chỉ một **bounded typed rule-evidence shape** đủ cho walking skeleton (§4). KHÔNG redefine Candle/Feature/Context contract — mọi input authoritative tham chiếu qua `event_record_ref` opaque, KHÔNG resolve/redefine schema nguồn. KHÔNG author UI copy/natural-language generation. KHÔNG sửa `strategy.md`/ADR-013/ADR-010/Constitution/C1-C3 semantics.

## 1. Decision — `kind: entity`

```yaml
id: decision
kind: entity
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Bản ghi authoritative, BẤT BIẾN, của MỘT lần Strategy Instance đánh giá deterministic tại một
  decision_context_cursor cụ thể (ADR-010 §2.3, Chapter 8 §8.4). Một Decision subject KHÔNG có
  "revision" — mọi field (identity, strategy evidence, rule evidence, input evidence, result) cố
  định tại thời điểm DecisionRecorded (§3). Correction chỉ qua invalidate-only (§4, KHÔNG same-ID
  replacement — cùng lý do StrategyDefinitionVersionRegistered/StrategyInstanceRegistered,
  strategy.md §3/§6: TOÀN BỘ scope bất biến, không có "mutable metadata" tách biệt). Revalidation
  (§5, ADR-010 §2.6/Chapter 8 §8.4.1) là một fact VẬN HÀNH riêng, KHÔNG phải correction.
invariants:
  - "decision_id là opaque, globally unique trong toàn Ride, gán tại DecisionRecorded — KHÔNG derive/resolve từ strategy_instance_id, decision_context_cursor, hay bất kỳ field nội dung nào. Bất biến, KHÔNG tái sử dụng cho subject khác (Chapter 6 §6.1)."
  - "MỘT Decision thuộc ĐÚNG MỘT Strategy Instance (`strategy_instance_id`, ref: strategy) — không multi-instance Decision, không aggregate nhiều Instance."
  - "MỘT Decision đánh giá ĐÚNG MỘT rule invocation — `decision_rule_ref` + rule evidence (§4) pin một lần đánh giá cụ thể, KHÔNG batch nhiều rule."
  - "**Logical computation key = (strategy_instance_id, decision_context_cursor)** — đúng MỘT authoritative DecisionRecorded VALID cho mỗi key. Retry của CÙNG logical computation (cùng key) PHẢI: (a) idempotent no-op nếu evidence bundle giống hệt (trả về decision_id đã tồn tại, KHÔNG tạo bản ghi thứ hai); hoặc (b) reject tường minh nếu evidence khác (changed-payload retry — cùng nguyên tắc `STABLE_ID_SAME_PAYLOAD_IS_IDEMPOTENT` đã proven tại `instrument.md` §17, khai báo độc lập tại §11 dưới dạng `decision_computation_idempotency_policy`). KHÔNG BAO GIỜ hai DecisionRecorded VALID cùng key với evidence khác nhau."
  - "Decision KHÔNG mutable dưới bất kỳ hình thức nào — không PATCH event, không revision event. Historical Decision vẫn resolvable sau khi Strategy Instance pause/retire (strategy.md §5/§7) — Decision là bằng chứng lịch sử độc lập lifecycle hiện tại của Instance (đúng Chapter 9 §9.3: 'lifecycle transitions must never invalidate already-computed Decision evidence')."
schema:
  decision_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  strategy_instance_id: {type: string, required: true, ref: strategy, description: "đúng một Strategy Instance"}
  decision_context_cursor: {type: object, required: true, description: "Replay Cursor hợp lệ (ADR-010 §2.3, Chapter 8 §8.5.1) — xem §2"}
  decision_time: {type: timestamp, required: true, description: "effective-axis value của Decision (ADR-010 §2.2, THAY effective_time — Chapter 8 §8.2.1)"}
  decision_rule_ref: {type: string, required: true, description: "PHẢI khớp đúng decision_rule_ref của strategy_definition_version_id đang pin (strategy.md §1) — xem §4"}
  result: {type: enum, values: [LONG, SHORT, NO_ACTION], required: true, description: "xem §4"}
events_emitted: [DecisionRecorded, DecisionFactInvalidated, DecisionRevalidated]
events_consumed: []
commands: []
queries: []
```

## 2. Canonical event envelope — áp dụng cho mọi Decision event (§3–§6)

Mọi event trong tài liệu này là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). Trường hợp `event_class: decision` (CHỈ `DecisionRecorded`, §3) áp dụng thêm cardinality riêng theo [Chapter 8 §8.2.1](../constitution/08-event-model.md)/[§8.4](../constitution/08-event-model.md); `DecisionFactInvalidated`/`DecisionRevalidated` KHÔNG thuộc `event_class: decision` — dùng envelope tiêu chuẩn.

```yaml
envelope:
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2)
  event_contract_ref: {cardinality: required}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}             # khi Ride ghi nhận fact này
  subject_ref: {cardinality: "required — shape canonical, xem dưới. Trên DecisionFactInvalidated, PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate."}
  stream_ref: {cardinality: required}                # Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # Phase 1, chưa author
  correlation_id: {cardinality: "required khi computation thuộc một correlation flow tường minh (ví dụ chuỗi revalidation); optional khi độc lập"}
  causation_refs: {cardinality: "DecisionRecorded: zero-or-more (Decision Engine internal computation trigger, Phase 1, chưa author). DecisionFactInvalidated/DecisionRevalidated: KHÔNG BAO GIỜ rỗng — PHẢI chứa fact gốc liên quan (xem §4/§5)."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3."}
  effective_time: {cardinality: "PROHIBITED trên DecisionRecorded (event_class: decision — Chapter 8 §8.2.1, ADR-010 §2.2, thay bằng decision_time). REQUIRED trên DecisionFactInvalidated/DecisionRevalidated (không phải event_class: decision) — xem §4/§5 cho giá trị chính xác."}
  decision_time: {cardinality: "REQUIRED trên DecisionRecorded — PROHIBITED trên mọi event khác (Chapter 8 §8.2.1). Effective-axis time value, ADR-010 §2.2 — semantic domain cụ thể xem §3."}
  decision_context_cursor: {cardinality: "REQUIRED trên DecisionRecorded — PROHIBITED trên mọi event khác (Chapter 8 §8.2.1). Replay Cursor hợp lệ, xem shape dưới."}
  market_time: {cardinality: "PROHIBITED — Decision là computation authoritative, không phải quan sát trực tiếp venue (Chapter 5 §5.2)."}
  source_identity: {cardinality: "PROHIBITED — Decision luôn phát sinh nội bộ từ Decision Engine (Phase 1, chưa author), KHÔNG BAO GIỜ từ external feed có khả năng retry/redelivery (Chapter 6 §6.6)."}

decision_context_cursor (shape, đúng canonical Replay Cursor — Chapter 8 §8.5.1, KHÔNG một schema gần giống):
  recorded_time: <timestamp>                          # required — knowledge boundary
  input_contract_ref: {contract_id: <string>, contract_version: <string>}   # required — versioned, immutable (§8.1.1)
  stream_registry_version: <string>                   # required
  lifecycle_frontier:                                  # required
    stream_id: <string>                                # canonical lifecycle stream
    position: {kind: <genesis | event>, sequence: <integer>}
  stream_positions: {<stream_id>: <sequence>, ...}     # required — map, mọi stream thuộc universe của cursor

subject_ref (Decision):
  context_id: strategy-decision
  subject_kind: entity
  subject_type: Decision
  subject_id: <decision_id — opaque, stable, xem §1>
  scope:
    strategy_instance_id: <string>

event_types:
  DecisionRecorded: DECISION_RECORDED
  DecisionFactInvalidated: DECISION_FACT_INVALIDATED
  DecisionRevalidated: DECISION_REVALIDATED
```

`stream_ref`/`producer_ref`/registry-cụ-thể-sau-`decision_context_cursor` (Stream Registry/Input Contract implementation, canonical Audit Stream) — Phase 1, chưa tồn tại cụ thể, cùng nguyên tắc defer xuyên suốt Package 0.2-B/C1-C3. `decision_context_cursor` field SHAPE và cardinality/invariant (§8.5.1/§8.5.2) là BẮT BUỘC ngay từ v0.1 (ADR-010/Chapter 8 Approved/Locked, không thể defer field structure) — chỉ MECHANISM resolve (registry cụ thể) là Phase 1.

**Relational invariants bắt buộc trên `decision_context_cursor`** (Chapter 8 §8.5.2, tái khẳng định KHÔNG lặp lại toàn văn):
```text
cursor.recorded_time ≤ DecisionRecorded.recorded_time            (Cursor → Decision, §8.5.2)
input_event.recorded_time ≤ cursor.recorded_time                 (mọi input evidence event, §2.4 ADR-010)
lifecycle_event.recorded_time ≤ cursor.recorded_time              (Lifecycle → Cursor, §8.5.2)
cursor.stream_registry_version = registry version mà input_contract_ref pin  (Registry → Contract, §8.5.2)
```
Vi phạm bất kỳ điều nào → **invalid `decision_context_cursor`, DecisionRecorded PHẢI bị từ chối khi append** (Chapter 8 §8.5.1). Đây chính là cơ chế thực thi no-look-ahead (I-3) cho Decision.

## 3. `DecisionRecorded` — `kind: event` (`event_class: decision`)

Kế thừa envelope §2 CỘNG `decision_time`/`decision_context_cursor` bắt buộc, `effective_time`/`market_time`/`source_identity` cấm. Payload đặc thù:

```yaml
id: decision-recorded
kind: event
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Fact AUTHORITATIVE DUY NHẤT cho một lần Strategy Instance đánh giá deterministic — thiết lập TOÀN
  BỘ nội dung (chín-field strategy evidence tại cursor, rule evidence, input evidence, result,
  trade_intent_outcome) cùng lúc, BẤT BIẾN. CHỈ được phát khi §3a (precondition) thỏa — nếu
  ineligible hoặc missing input, KHÔNG event nào được phát (§3a, tái sử dụng style
  missing_input_policy của context.md §9, khai báo độc lập §11).
invariants:
  - "payload.decision_id PHẢI khớp đúng subject_ref.subject_id VÀ payload.strategy_instance_id PHẢI khớp đúng subject_ref.scope.strategy_instance_id."
  - "envelope.decision_time = thời điểm domain Decision có hiệu lực — mặc định bằng decision_context_cursor.recorded_time trừ khi backfill lịch sử tường minh pin giá trị khác (semantic chi tiết thuộc Decision Domain Contract, ADR-010 §4)."
  - "TẤT CẢ chín field strategy evidence (§3b) PHẢI resolve deterministic từ authoritative Strategy/Account/Instrument/Venue event stream TẠI ĐÚNG decision_context_cursor — KHÔNG dùng StrategyInstanceCurrentView/AccountCurrentView/InstrumentCurrentView/VenueCurrentView/TradableListingCurrentView latest-state (strategy.md §9a/§10, account.md §13, instrument.md §7/§15)."
```

**§3a — Precondition: `eligible_for_new_computation == true` (strategy.md §9a, TẠI đúng `decision_context_cursor`).** DecisionRecorded CHỈ được phát khi tất cả đúng theo thứ tự:

```text
1. eligible_for_new_computation(strategy_instance_id, decision_context_cursor) == true   (strategy.md §9a, sáu điều kiện)
2. Mọi required input evidence (§3d) VISIBLE và resolvable TẠI decision_context_cursor    (§11 decision_non_creation_policy)
→ NẾU CẢ HAI thỏa: DecisionRecorded PHẢI phát, result (§3c) phản ánh rule evaluation THẬT (LONG/SHORT/NO_ACTION — NO_ACTION nghĩa là "rule evaluated false", một fact THẬT, KHÔNG phải absence).
→ NẾU (1) false: KHÔNG DecisionRecorded nào được phát cho cursor đó — "Strategy was ineligible", deterministic thông qua kiểm tra trực tiếp strategy.md §9a tại cursor (§11).
→ NẾU (2) false (input missing/pending): KHÔNG DecisionRecorded nào được phát — "rule could not be evaluated", deterministic thông qua kiểm tra trực tiếp upstream input stream tại cursor (§11).
```

**Ba trường hợp trên PHÂN BIỆT tường minh, KHÔNG collapse:** `NO_ACTION` (fact thật, evidence đầy đủ, rule trả false) ≠ `input missing` (absence, kiểm chứng qua upstream stream) ≠ `strategy ineligible` (absence, kiểm chứng qua strategy.md §9a) — mỗi trường hợp deterministic-reconstructable từ ĐÚNG MỘT nguồn authoritative riêng (§11), không cần một event "rejection" fabricate thêm (đóng yêu cầu "define smallest deterministic representation ... only if needed" — quyết định KHÔNG cần, vì cả hai absence-case đã deterministic qua nguồn có sẵn).

**§3b — Strategy evidence (chín field, PIN tại decision_context_cursor, COPY làm scalar bất biến — đúng I-1: "Model/strategy version + strategy instance ID; configuration version; code/build version" PHẢI frozen tại decision time):**

```yaml
strategy_evidence:
  strategy_definition_id: {type: string, required: true, description: "strategy.md §10"}
  strategy_definition_version_id: {type: string, required: true, description: "exact immutable pin, KHÔNG BAO GIỜ 'latest' — ADR-013 §2.3"}
  plugin_version_ref: {type: string, required: true, description: "trục 2/4 — strategy.md §11"}
  configuration_version_ref: {type: string, required: true, description: "trục 3/4 — strategy.md §11"}
  package_build_artifact_ref: {type: string, required: true, description: "trục 4/4 — exact executable identity đang chạy, ADR-013 §2.5; hai executable khác bytes PHẢI khác giá trị này (Scenario F, §16)"}
  account_id: {type: string, required: true, ref: account, description: "đúng một Account, strategy.md §5"}
  environment: {type: enum, values: [PAPER, LIVE], required: true, description: "resolve qua account_id TẠI cursor — KHÔNG dùng AccountCurrentView (account.md §13)"}
  instrument_selection_ref:
    instrument_id: {type: string, required: true}
    venue_id: {type: string, required: true}
    listing_id: {type: string, required: true}
```

**Invariant bổ sung:** bốn trục evidence (`strategy_definition_version_id`/`plugin_version_ref`/`configuration_version_ref`/`package_build_artifact_ref`) PHẢI persistently resolvable TẠI cursor (Chapter 8 §8.1.1 mục 4, strategy.md §9a/§11) — nếu KHÔNG, đây thuộc trường hợp `eligible_for_new_computation == false` (§3a mục 1), KHÔNG DecisionRecorded nào được phát.

**§3c — Rule evidence (bounded typed rule-reference, KHÔNG DSL/parser/rule graph):**

```yaml
rule_evidence:
  decision_rule_ref: {type: string, required: true, description: "PHẢI khớp đúng decision_rule_ref của strategy_definition_version_id đang pin (strategy.md §1) — semantic rule identity thuộc Strategy Definition Version, KHÔNG thuộc Decision"}
  rule_family: {type: enum, values: [PRICE_CROSSES_REFERENCE_SERIES], required: true, description: "v0.1: đúng một giá trị — bounded, mở rộng sau bằng giá trị enum MỚI khi có rule family khác, KHÔNG redesign shape hiện có"}
  price_source: {type: enum, values: [CLOSE, HIGH, LOW, OPEN], required: true, description: "copied scalar, nguồn authoritative = configuration_version_ref (§3b) — KHÔNG hardcode trên Strategy Definition Version trừ khi rule coi giá trị này là fixed business semantics (task instruction, KHÔNG áp dụng ở walking skeleton)"}
  reference_series_type: {type: enum, values: [EMA], required: true, description: "copied scalar — nguồn authoritative = configuration_version_ref"}
  reference_series_period: {type: integer, required: true, description: "copied scalar (ví dụ 50 hoặc 100) — nguồn authoritative = configuration_version_ref, KHÔNG trên Strategy Definition Version (Scenario C, §16)"}
  crossing_policy: {type: enum, values: [STRICT_CROSS, SIMPLY_ABOVE], required: true, description: "copied scalar — nguồn authoritative = configuration_version_ref. STRICT_CROSS: previous_condition_met AND current_condition_met (crossing thật). SIMPLY_ABOVE: chỉ current_condition_met, không yêu cầu crossing."}
  evaluation_timing: {type: enum, values: [CANDLE_CLOSE, INTRABAR], required: true, description: "v0.1 CHỈ hỗ trợ CANDLE_CLOSE — INTRABAR reserved (enum value tồn tại cho type-safety tương lai), PROHIBITED dùng thực tế ở v0.1 (§14)"}
  previous_price_value: {type: decimal, required: true, description: "copied scalar cho explanation — xem §3d cho authoritative reference"}
  previous_reference_value: {type: decimal, required: true}
  current_price_value: {type: decimal, required: true}
  current_reference_value: {type: decimal, required: true}
  previous_condition_met: {type: boolean, required: true, description: "previous_price_value <= previous_reference_value"}
  current_condition_met: {type: boolean, required: true, description: "current_price_value > current_reference_value"}
```

**Invariant:** `rule_family = PRICE_CROSSES_REFERENCE_SERIES` PHẢI đi kèm CẢ chín sub-field trên — không partial. Với `evaluation_timing = CANDLE_CLOSE`, `current_price_fact_ref`/`previous_price_fact_ref` (§3d) PHẢI trỏ candle fact ở lifecycle state CLOSED (không phải provisional/open) — vi phạm là invalid DecisionRecorded.

**§3d — Input evidence (authoritative reference, KHÔNG chỉ copied value — KHÔNG redefine Candle/Feature/Context contract, tham chiếu opaque):**

```yaml
input_evidence:
  previous_price_fact_ref: {type: event_record_ref, required: true, description: "authoritative candle fact cung cấp previous_price_value — opaque, KHÔNG redefine candle.md schema tại đây"}
  current_price_fact_ref: {type: event_record_ref, required: true, description: "authoritative candle fact cung cấp current_price_value"}
  previous_reference_fact_ref: {type: event_record_ref, required: true, description: "authoritative fact cung cấp previous_reference_value (ví dụ EMA trước) — nguồn cụ thể (Feature type hay contract khác) KHÔNG định nghĩa ở đây, deferred §14, opaque reference"}
  current_reference_fact_ref: {type: event_record_ref, required: true, description: "authoritative fact cung cấp current_reference_value"}
  timeframe: {type: string, required: true, description: "copied scalar, nguồn authoritative = configuration_version_ref"}
```

**Invariant no-look-ahead (I-3, ADR-010 §2.4):** mọi `*_fact_ref` trong `input_evidence` PHẢI thỏa `fact.recorded_time ≤ decision_context_cursor.recorded_time` — vi phạm → invalid DecisionRecorded, PHẢI bị từ chối khi append (Scenario D, §16). Replay tại cursor trước KHÔNG được thấy correction ghi nhận sau cursor đó (bitemporal — Chapter 5 §5.2).

**§3e — Result và Trade Intent outcome:**

```yaml
result: {type: enum, values: [LONG, SHORT, NO_ACTION], required: true, description: "rule evaluation THẬT — LONG/SHORT khi current_condition_met true theo crossing_policy; NO_ACTION khi false. KHÔNG bao giờ dùng cho ineligible/missing-input case (§3a — những case đó KHÔNG có DecisionRecorded)."}
trade_intent_outcome: {type: enum, values: [ISSUED, SUPPRESSED_DUPLICATE], required: false, description: "BẮT BUỘC khi result ∈ {LONG, SHORT}; TUYỆT ĐỐI ABSENT khi result = NO_ACTION (§8). ISSUED: một TradeIntentIssued (trade-intent.md §3) được phát, causally trỏ decision_id này. SUPPRESSED_DUPLICATE: computation này trùng logical key với một DecisionRecorded VALID đã có TradeIntentIssued — idempotent retry, KHÔNG phát TradeIntent thứ hai (§1 idempotency invariant). KHÔNG Risk semantics nào khác được biểu diễn ở đây (forbidden scope C5)."}
```

## 4. `DecisionFactInvalidated` — `kind: event`

Kế thừa envelope §2 (KHÔNG thuộc `event_class: decision` — dùng `effective_time` tiêu chuẩn, `decision_time`/`decision_context_cursor` bị CẤM trên chính event này). `causation_refs` không rỗng.

```yaml
id: decision-fact-invalidated
kind: event
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Phủ định MỘT DecisionRecorded ĐÃ SAI thực tế (lỗi capture evidence, KHÔNG phải registry-transition
  staleness — trường hợp đó dùng DecisionRevalidated, §5). KHÔNG có same-ID replacement — TOÀN BỘ
  Decision là scope bất biến (§1, không "mutable metadata" tách biệt), correction LUÔN LUÔN nghĩa
  là: fact cũ invalidate, KHÔNG có DecisionRecorded mới nào "sửa" cùng decision_context_cursor
  (logical computation key đã dùng bởi fact sai — occupied nhưng TERMINALLY_INVALID). Một tính
  toán LẠI hợp lệ (nếu cursor khác) là một DecisionRecorded HOÀN TOÀN MỚI, độc lập.
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT decision_time của DecisionRecorded bị invalidate (DecisionFactInvalidated không phải event_class: decision nên KHÔNG mang decision_time — kế thừa giá trị effective-axis của fact gốc vào effective_time tiêu chuẩn của chính nó, đúng tinh thần 'PHẢI BẰNG HỆT effective_time của invalidated_fact_ref' áp dụng xuyên suốt mọi *FactInvalidated khác trong repository)."
  - "invalidated_fact_ref PHẢI trỏ một DecisionRecorded, CHƯA từng nhận invalidation khác — một fact chỉ bị invalidate đúng một lần. KHÔNG BAO GIỜ trỏ một DecisionFactInvalidated/DecisionRevalidated khác."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead)."
  - "Sau invalidation, decision_id đó VĨNH VIỄN TERMINALLY_INVALID (§6) — logical computation key (strategy_instance_id, decision_context_cursor) KHÔNG BAO GIỜ có DecisionRecorded thay thế dưới key đó — nếu Decision đúng cho cursor này thực sự cần tồn tại, nó PHẢI được tính lại dưới decision_id MỚI, với decision_context_cursor có thể khác (một cursor mới, một tính toán mới)."
  - "Nếu decision_id bị invalidate đã có trade_intent_outcome = ISSUED, TradeIntent liên quan (trade-intent.md §3) KHÔNG tự động invalidate — Trade Intent lifecycle độc lập (trade-intent.md §7), correction Decision KHÔNG cascade tự động sang Trade Intent đã issue; xử lý Trade Intent liên quan (nếu cần) là một hành động RIÊNG qua trade-intent.md §5, KHÔNG tự động."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 5. `DecisionRevalidated` — `kind: event`

Kế thừa envelope §2 (KHÔNG thuộc `event_class: decision`). `causation_refs` không rỗng — PHẢI chứa `DecisionRecorded` gốc. Thực thi chính xác **Append-and-Revalidate policy** (ADR-010 §2.6, Chapter 8 §8.4.1) — KHÔNG phải correction, là một fact VẬN HÀNH độc lập ghi nhận kết quả revalidate một Decision đã có knowledge cut TRƯỚC một registry transition nhưng append SAU transition đó.

```yaml
id: decision-revalidated
kind: event
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Kết quả revalidation của một DecisionRecorded đã in-flight qua registry transition (ADR-010
  §2.6). Decision gốc VẪN append như immutable historical fact (KHÔNG tự động có execution
  eligibility) — event này ghi nhận kết quả revalidate theo registry đang active làm authoritative
  fact, KHÔNG phải trạng thái ngầm (Chapter 8 §8.4.1, 4 guardrail).
invariants:
  - "causation_refs PHẢI trỏ chính xác DecisionRecorded gốc (§3) — KHÔNG dùng success của Decision khác (Chapter 8 §8.4.1, Revalidation evidence chain mục 1)."
  - "PHẢI ghi evidence registry/knowledge boundary đã dùng để revalidate — field revalidated_against_registry_version, revalidated_against_frontier_ref (KHÔNG dùng success dưới registry khác, mục 2)."
  - "outcome = SUCCEEDED chỉ cấp execution eligibility TRONG registry applicability interval của chính lần revalidate này (Chapter 8 §8.4.1 mục 5) — registry transition xảy ra SAU đó khiến eligibility quay lại blocked, cần revalidate lại. Cơ chế enforcement cụ thể (atomic check, fencing token) là Phase 1 (§14); boundary semantic pin tại đây."
  - "outcome = STALE hoặc REJECTED: Decision gốc KHÔNG bị sửa/xóa — chỉ ghi nhận revalidation KHÔNG cấp eligibility. Nếu target stream đã retire hoặc event không còn eligible dưới registry mới, preservation fact riêng trên canonical Audit Stream áp dụng (Chapter 8 §8.4.1 — deferred §14, cần Stream Registry/Audit Stream infrastructure Phase 1 chưa tồn tại)."
  - "Một DecisionRecorded có thể nhận NHIỀU DecisionRevalidated qua thời gian (mỗi registry transition mới có thể cần revalidate lại, mục 5) — KHÔNG giới hạn một-lần-duy-nhất."
payload:
  original_decision_ref: {type: event_record_ref, required: true, description: "trỏ chính xác DecisionRecorded gốc"}
  outcome: {type: enum, values: [SUCCEEDED, STALE, REJECTED], required: true}
  revalidated_against_registry_version: {type: string, required: true}
  revalidated_against_frontier_ref: {type: event_record_ref, required: true, description: "lifecycle/registry boundary event đã dùng để revalidate"}
  reason: {type: string, required: false}
```

**Preservation fact (Decision computation evidence trên canonical Audit Stream, khi target stream retired) — Phase 1, chưa author cụ thể (§14):** Chapter 8 §8.4.1 mục 6 bắt buộc một event type RIÊNG, dedicated Event Contract (`allowed_streams` = [canonical Audit Stream], `prohibited execution eligibility`) cho trường hợp registry transition retire chính stream đích của Decision. Cơ chế này đòi hỏi Stream Registry/canonical Audit Stream đã implement cụ thể — hạ tầng đó chưa tồn tại trong repository (cùng trạng thái defer như `stream_ref`/`producer_ref` xuyên suốt mọi Domain Contract). `decision.md` v0.1 PIN rule (Chapter 8 đã Locked yêu cầu event type này tồn tại khi hạ tầng sẵn sàng) nhưng KHÔNG tự author event type cụ thể ở đây — tránh fabricate một Event Contract phụ thuộc infrastructure chưa có.

## 6. `DecisionCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §3–§5.

```text
Trước khi DecisionRecorded tồn tại cho một decision_id:
  → KHÔNG có DecisionCurrentView row nào tồn tại
  → GetCurrentDecision trả về NOT_FOUND / ABSENT
```

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION`. Khi `PENDING_CORRECTION`, `pending_correction_class` BẮT BUỘC có mặt — CHỈ MỘT giá trị khả dĩ cho subject này (đóng ngay từ v0.1):

```text
view_state = VALID              → pending_correction_class: CẤM (phải absent)
view_state = PENDING_CORRECTION → pending_correction_class = TERMINAL_SCOPE_INVALIDATION (LUÔN LUÔN — DecisionRecorded KHÔNG có same-ID replacement path, §4, nên AWAITING_SAME_SUBJECT_REPLACEMENT KHÔNG BAO GIỜ áp dụng cho subject này)
```

`TERMINAL_SCOPE_INVALIDATION` KHÔNG BAO GIỜ transition về `VALID`; subject cũ vẫn queryable qua `GetDecisionHistory` làm historical evidence — cùng nguyên tắc đã khóa xuyên suốt `instrument.md`/`account.md`/`strategy.md`.

**Fold algorithm (v0.1, đơn giản hơn "visible-valid-head per slice" vì KHÔNG có correction lineage nhiều bước — chỉ MỘT slice, MỘT fact, tối đa MỘT invalidation):**

```text
1. Resolve DecisionFactInvalidated visibility tại cursor (recorded_time <= cursor).
2. NẾU có invalidation visible → view_state = PENDING_CORRECTION, pending_correction_class =
   TERMINAL_SCOPE_INVALIDATION — DỪNG, không resolve field nào khác.
3. NẾU KHÔNG → view_state = VALID, resolve toàn bộ DecisionRecorded payload (§3) làm scope hiện tại.
4. Fold mọi DecisionRevalidated visible (§5), total-order recorded_time ASC, event_id ASC —
   revalidation_status = outcome của DecisionRevalidated MỚI NHẤT visible (hoặc absent nếu chưa
   revalidate lần nào — Decision vẫn VALID, chỉ chưa qua registry transition nào cần revalidate).
```

```yaml
id: decision-current-view
kind: read_model
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Projection tiện dụng cho query/UI, KHÔNG BAO GIỜ là input hợp lệ cho Trade Intent/Risk/Execution
  hay bất kỳ computation nào khác — cùng nguyên tắc Current-View-never-authority đã khóa xuyên
  suốt `instrument.md`/`account.md`/`strategy.md`. Downstream field PHẢI resolve qua authoritative
  Decision event stream (`ref: decision`) TẠI CÙNG cursor mà computation đó đang dùng (§12). Cache
  chỉ chấp nhận khi ĐỒNG THỜI cursor-addressable VÀ provably equivalent với authoritative
  reconstruction tại đúng cursor/contract version/configuration.
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho Trade Intent/Risk/Execution/Order/Fill/Position hay computation nào khác — CHỈ query/UI."
  - "view_state PHẢI đúng theo Bước 1–2 của fold algorithm — registration lineage head quyết định, KHÔNG BAO GIỜ fallback về một fact đã invalidate."
  - "pending_correction_class BẮT BUỘC có mặt khi view_state = PENDING_CORRECTION (luôn = TERMINAL_SCOPE_INVALIDATION cho subject này); CẤM có mặt khi view_state = VALID."
schema:
  decision_id: {type: string, required: true}
  scope: {strategy_instance_id: string, decision_context_cursor: object, result: string, required: true, description: "chỉ có mặt khi view_state = VALID"}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  pending_correction_class: {type: enum, values: [TERMINAL_SCOPE_INVALIDATION], required: false}
  revalidation_status: {type: enum, values: [SUCCEEDED, STALE, REJECTED], required: false, description: "absent nếu chưa từng revalidate; latest outcome nếu có (Bước 4)"}
  last_recorded_time: timestamp
queries: [GetCurrentDecision, GetDecisionHistory]
```

## 7. Explanation contract

**Explanation là derived, non-authoritative rendering — KHÔNG UI copy, KHÔNG natural-language generation infrastructure.** Structured evaluation facts (§3c `rule_evidence`) là authoritative; text rendering CHỈ là một hàm thuần túy của evidence đã có, KHÔNG BAO GIỜ được introduce fact vắng mặt khỏi Decision evidence.

```text
Explanation(decision_id) = deterministic render của {rule_evidence, input_evidence, result} — KHÔNG
computation mới, KHÔNG external lookup, KHÔNG dùng bất kỳ giá trị nào không có mặt trong §3b–§3e.
```

Ví dụ walking-skeleton (đúng Scenario A, §16) — render tương đương:

```text
Previous close <= previous EMA: true      (rule_evidence.previous_condition_met)
Current close > current EMA: true          (rule_evidence.current_condition_met)
Crossing policy: strict                    (rule_evidence.crossing_policy = STRICT_CROSS)
Result: LONG                               (result)
```

**Invariant:** hai Decision với cùng `rule_evidence`/`input_evidence`/`result` PHẢI cho cùng explanation render (deterministic, không phụ thuộc thời điểm render hay implementation UI). Explanation KHÔNG có event/subject riêng — nó là một PROJECTION thuần túy của DecisionRecorded, KHÔNG BAO GIỜ authoritative độc lập khỏi Decision evidence gốc.

## 8. Decision-to-Trade-Intent cardinality

```text
result = LONG hoặc SHORT  →  trade_intent_outcome BẮT BUỘC có mặt (§3e):
    ISSUED              → chính xác MỘT TradeIntentIssued (trade-intent.md §3), causally trỏ decision_id
    SUPPRESSED_DUPLICATE → ZERO TradeIntent (idempotent retry của cùng logical computation key, §1)

result = NO_ACTION  →  trade_intent_outcome TUYỆT ĐỐI ABSENT, ZERO Trade Intent LUÔN LUÔN
```

**Một Decision → tối đa MỘT Trade Intent** (v0.1 walking skeleton — KHÔNG multi-intent portfolio decomposition, đúng yêu cầu bounded scope). Lý do suppress (nếu có) PHẢI deterministic VÀ KHÔNG import Risk semantics (C5) — v0.1 CHỈ có MỘT lý do suppress hợp lệ: `SUPPRESSED_DUPLICATE` (idempotent-retry, §1). KHÔNG có "suppressed vì risk limit"/"suppressed vì capital" ở tầng Decision — những khái niệm đó thuộc Risk Gateway (C5, chưa author), Decision KHÔNG được tự phát minh risk rejection semantics.

## 9. Correction lineage

Correction lineage scoped chính xác theo `(subject_id, effective_time-hoặc-decision_time-tương-ứng)` — cùng nguyên tắc đã khóa xuyên suốt `instrument.md`/`venue.md`/`account.md`/`strategy.md`.

**`DecisionRecorded` — invalidate-only, KHÔNG replacement (§3/§4):**

```text
F1 (DecisionRecorded)
  → DecisionFactInvalidated targeting F1
  → KHÔNG có replacement dưới cùng decision_id — logical computation key (strategy_instance_id,
    decision_context_cursor) của F1 VĨNH VIỄN không có DecisionRecorded VALID nào khác dưới key đó.
    Một tính toán lại hợp lệ (nếu thực sự cần) là một decision_id + decision_context_cursor MỚI
    HOÀN TOÀN, độc lập.
```

**`DecisionRevalidated` KHÔNG phải correction lineage** — nó là chuỗi VẬN HÀNH độc lập (Append-and-Revalidate, §5), một DecisionRecorded có thể nhận nhiều DecisionRevalidated theo thời gian, KHÔNG invalidate/thay thế Decision gốc.

## 10. Time semantics và bitemporal correctness

- `decision_time` — effective axis, THAY `effective_time` cho DecisionRecorded (ADR-010 §2.2, Chapter 8 §8.2.1). PROHIBITED trên mọi event khác trong tài liệu này.
- `recorded_time` — recorded axis, universal trên mọi event (Chapter 5).
- `decision_context_cursor` — knowledge boundary vector, REQUIRED trên DecisionRecorded, PROHIBITED trên event khác (§2).
- **No-future-input (I-3, ADR-010 §2.4):** `input_event.recorded_time ≤ decision_context_cursor.recorded_time ≤ DecisionRecorded.recorded_time` — bắc cầu chứng minh KHÔNG input/lifecycle fact nào đến từ tương lai của chính Decision (§2 relational invariants).
- **Replay tại cursor T** chỉ thấy fact có `recorded_time ≤ T` — invalidation/revalidation ghi SAU T KHÔNG visible tại T (Scenario D, §16).
- `market_time` PROHIBITED xuyên suốt tài liệu này — Decision không phải quan sát venue trực tiếp.

## 11. Canonical policy identifiers — nguồn duy nhất (context `strategy-decision`)

**Ba canonical policy identifier, khai báo ĐÚNG MỘT LẦN tại đây cho context `strategy-decision`** — cùng pattern đã proven tại `instrument.md`/`account.md`/`strategy.md`, khai báo ĐỘC LẬP vì đây là context khác:

```yaml
initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS
decision_computation_idempotency_policy: STABLE_KEY_SAME_EVIDENCE_IS_IDEMPOTENT
decision_non_creation_policy: NO_DECISION_WHEN_INELIGIBLE_OR_REQUIRED_INPUT_MISSING_OR_PENDING
```

**`initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS`** (tái sử dụng đúng giá trị đã proven tại `strategy.md` §12, khai báo độc lập tại context này) — áp dụng cho `DecisionRecorded` (§3/§4): TOÀN BỘ payload là scope bất biến, correction LUÔN LUÔN nghĩa là invalidate, KHÔNG BAO GIỜ same-ID replacement.

**`decision_computation_idempotency_policy: STABLE_KEY_SAME_EVIDENCE_IS_IDEMPOTENT`** (v0.1, đối xứng `activation_request_idempotency_policy: STABLE_ID_SAME_PAYLOAD_IS_IDEMPOTENT` đã proven tại `instrument.md` §17, thuật ngữ đổi cho đúng context này) — logical computation key = `(strategy_instance_id, decision_context_cursor)`; retry cùng key + cùng evidence bundle → idempotent no-op (trả decision_id đã tồn tại); retry cùng key + evidence KHÁC → reject tường minh (deterministic conflict, KHÔNG tạo bản ghi cạnh tranh). Xem §1.

**`decision_non_creation_policy: NO_DECISION_WHEN_INELIGIBLE_OR_REQUIRED_INPUT_MISSING_OR_PENDING`** (v0.1, đúng MỘT giá trị hợp lệ — cùng style đóng-enum-một-giá-trị đã proven tại `context.md` §6/§9 `missing_input_policy: NO_SNAPSHOT_WHEN_ANY_REQUIRED_ROLE_MISSING_OR_PENDING`, tái sử dụng STYLE, khai báo độc lập tên/giá trị cho context `strategy-decision`) — khi `eligible_for_new_computation == false` (strategy.md §9a) HOẶC required input evidence (§3d) missing/pending tại cursor: KHÔNG DecisionRecorded nào được phát cho computation point đó. Đây là **valid deterministic absence**, KHÔNG phải "collapse" — mỗi trường hợp reconstruct được từ đúng MỘT nguồn authoritative riêng biệt (strategy.md §9a cho ineligible; upstream Candle/reference-series stream cho missing input), tách biệt tường minh khỏi `result = NO_ACTION` (một fact THẬT, §3e). CẤM: null filling, stale fallback trình bày như current, partial DecisionRecorded, implementation-selected behavior.

## 12. Downstream reference contract (cho Trade Intent §3, và Package 0.2-C5 Risk — chưa author)

`trade-intent.md` (cùng transaction này) và Package 0.2-C5 (Risk, chưa author) tham chiếu Decision qua ĐÚNG các field sau, KHÔNG hơn:

```yaml
decision_id: {type: string, required: true, ref: decision}
strategy_instance_id: {type: string, description: "= subject_ref.scope.strategy_instance_id"}
account_id: {type: string, ref: account, description: "= strategy_evidence.account_id, §3b"}
instrument_selection_ref: {type: object, description: "= strategy_evidence.instrument_selection_ref, §3b — {instrument_id, venue_id, listing_id}"}
result: {type: enum, values: [LONG, SHORT, NO_ACTION], description: "= §3e"}
decision_time: {type: timestamp, description: "= §2"}
```

**Downstream authority rule — MỘT quy tắc duy nhất, không ngoại lệ (đúng pattern đã proven `account.md` §13/`strategy.md` §10):** downstream contract PHẢI resolve mọi field trên TRỰC TIẾP từ authoritative Decision event stream (§3–§5) TẠI ĐÚNG cursor mà chính computation đó đang dùng. `DecisionCurrentView` latest-state (§6) KHÔNG BAO GIỜ được dùng làm input. `decision.md` KHÔNG author semantics của Trade Intent contents/lifecycle (thuộc `trade-intent.md`, §13 dưới) hay Risk (Package 0.2-C5, chưa author).

## 13. Prohibitions

**Decision KHÔNG được sở hữu:** Strategy/Strategy Instance identity semantics (thuộc `strategy.md`); Trade Intent contents/lifecycle (thuộc `trade-intent.md`); Risk approval/rejection, risk limit, position sizing (Package 0.2-C5, chưa author); Execution Intent/Order/Fill/Position/Replay Event semantics (Package 0.2-C5–C7); order type/limit price/stop price/exchange payload; DSL/expression language/parser/rule graph/strategy compiler tổng quát (chỉ bounded typed rule evidence, §3c); UI copy/natural-language generation infrastructure; Candle/Feature/Context contract schema (chỉ opaque `event_record_ref`, §3d).

## 14. Ngoài phạm vi — defer

**Deferred tường minh, không author ở C4 (Phase 1 implementation concern hoặc phụ thuộc hạ tầng chưa tồn tại, non-blocking):**

- Stream Registry/Input Contract/canonical Audit Stream implementation cụ thể — `decision_context_cursor`/`stream_ref`/`producer_ref` field SHAPE pin ngay v0.1 (ADR-010/Chapter 8 Locked), MECHANISM resolve deferred Phase 1.
- Preservation fact event type cụ thể trên Audit Stream cho trường hợp target stream retired tại registry transition (Chapter 8 §8.4.1 mục 6) — đòi hỏi Audit Stream infrastructure chưa tồn tại (§5).
- Cơ chế fencing/atomic-check cụ thể cho revalidation validity interval (Chapter 8 §8.4.1 mục 5) — boundary semantic pin, implementation Phase 1.
- Nguồn cụ thể của `previous_reference_fact_ref`/`current_reference_fact_ref` (EMA hay reference-series khác) — decision.md KHÔNG redefine Candle/Feature contract, opaque reference (§3d); một Feature type EMA cụ thể (nếu cần) là công việc của một package Feature riêng, KHÔNG phải C4.
- `evaluation_timing = INTRABAR` — enum value tồn tại cho type-safety, semantics/input-visibility rule chưa thiết kế, PROHIBITED dùng thực tế ở v0.1 (§3c).
- `rule_family` khác `PRICE_CROSSES_REFERENCE_SERIES` — mở rộng khi có nhu cầu thực tế, KHÔNG thiết kế trước (tránh DSL tổng quát).
- Multi-intent/portfolio decomposition từ một Decision — v0.1 tối đa MỘT Trade Intent (§8).
- Risk rejection/approval semantics, capital/sizing, order type — hoàn toàn ngoài phạm vi Domain Contract này (Package 0.2-C5–C7).

## 15. Open questions ngoài phạm vi

- Cơ chế cụ thể generate `decision_id` (UUID, content-hash, sequential) — chưa quyết, Phase 1, cùng nguyên tắc defer đã áp dụng cho `strategy_instance_id`/`account_id`.
- Retention/resolvability horizon cụ thể cho Decision đã lâu (Chapter 9 §9.3-style yêu cầu horizon tường minh) — chưa pin ở v0.1.
- Preservation-fact Event Contract cụ thể (Chapter 8 §8.4.1 mục 6) — chờ Stream Registry/Audit Stream Phase 1.
- Không đóng OQ-002/OQ-003.

## 16. Acceptance scenarios (validation, không phải executable test tại C4)

**Scenario A — EMA strict cross LONG:** `previous_price_value=99, previous_reference_value=100 → previous_condition_met=true`; `current_price_value=102, current_reference_value=101 → current_condition_met=true`; `crossing_policy=STRICT_CROSS` → `result=LONG`, `trade_intent_outcome=ISSUED`, một TradeIntentIssued được phát (trade-intent.md §3).

**Scenario B — already above, no cross:** `previous_price_value=101, previous_reference_value=100 → previous_condition_met=false`; `current_price_value=102, current_reference_value=101 → current_condition_met=true`; `crossing_policy=STRICT_CROSS` yêu cầu CẢ HAI true → `result=NO_ACTION` (fact thật, §3a nhánh 1), `trade_intent_outcome` absent, KHÔNG TradeIntent.

**Scenario C — configuration difference:** cùng candle, `reference_series_period=50` (EMA50) → giả sử `current_reference_value` khác `reference_series_period=100` (EMA100) đủ để một bên `current_condition_met=true` (→ `result=LONG`) và bên kia `false` (→ `result=NO_ACTION`) — HAI DecisionRecorded riêng biệt (khác `configuration_version_ref`, §3b, khác `decision_id`), `rule_evidence.reference_series_period` làm rõ tường minh sự khác biệt cấu hình (đóng yêu cầu "Decision evidence must make the configuration difference explicit").

**Scenario D — future correction hidden:** một candle/EMA value được CORRECT (recorded SAU `decision_context_cursor` gốc) KHÔNG được visible khi replay tại cursor gốc — invariant §2 (`input_event.recorded_time ≤ cursor.recorded_time`) chặn tường minh; DecisionRecorded gốc giữ nguyên authoritative, KHÔNG bị ảnh hưởng bởi correction ghi sau.

**Scenario E — Strategy ineligible:** Instance ACTIVE nhưng Account SUSPENDED (hoặc Definition invalidated, hoặc evidence artifact unresolvable) → `eligible_for_new_computation(strategy_instance_id, cursor) == false` (strategy.md §9a) → §3a nhánh "ineligible": KHÔNG DecisionRecorded nào được phát, KHÔNG Trade Intent nào — deterministic qua kiểm tra trực tiếp strategy.md §9a tại cursor, KHÔNG cần event riêng (§11).

**Scenario F — exact executable difference:** cùng Strategy Definition Version + Configuration Version, nhưng `package_build_artifact_ref` khác (rebuild non-reproducible, ADR-013 §2.5) → hai `strategy_evidence.package_build_artifact_ref` khác giá trị trên hai DecisionRecorded riêng biệt (dù mọi field khác giống hệt) — vẫn distinguishable tường minh trong evidence (§3b), đúng yêu cầu ADR-013 §2.5 "không proxy trục nào".

**Scenario G — correction:** một DecisionRecorded (hoặc TradeIntentIssued, trade-intent.md §3) ghi sai được sửa qua `DecisionFactInvalidated` (§4) / `TradeIntentFactInvalidated` (trade-intent.md §5) append-only — event gốc KHÔNG bị rewrite/xóa (Chapter 5/append-only I-3), KHÔNG DecisionRecorded/TradeIntentIssued nào khác được tạo dưới CÙNG decision_id/trade_intent_id (§4/§9 invalidate-only, KHÔNG same-ID replacement); replay tại cursor TRƯỚC invalidation KHÔNG thấy invalidation đó (chống leak-forward, §2/§10).
