---
id: trade-intent
title: Trade Intent
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

# Trade Intent

> **Vai trò của tài liệu này:** Domain Contract thứ hai của Package 0.2-C4 (Trade Intent and Decision Foundation) — định nghĩa **Trade Intent**, một request Strategy-originated biểu thị mong muốn market exposure/hành động, PHÁT SINH từ một [`decision.md`](./decision.md) `result ∈ {LONG, SHORT}` (§8 decision.md), TRƯỚC Risk Gateway và Execution. Draft, chưa Approved/Locked. Thuộc capability `decision-management` / context `strategy-decision` (đăng ký cùng `decision.md` tại [`context-map.yaml`](./context-map.yaml) trong transaction này — hai file, MỘT context, đúng quyết định tổ chức "hai concept riêng biệt, KHÔNG gộp làm một file" nhưng cùng thuộc phạm vi ra-quyết-định). Kiến trúc controlling: [`decision.md`](./decision.md) v0.1 Draft §8 (Decision-to-Trade-Intent cardinality), [ADR-013](../adr/ADR-013.md) v0.3 Approved (qua `strategy.md`), Chapter 8 (Locked, envelope tiêu chuẩn — Trade Intent KHÔNG phải `event_class: decision`).

Trade Intent **KHÔNG phải**: một Order (không order type/limit price/stop price/exchange payload); một Execution Intent; một Fill; một Position; một risk approval; một exchange instruction; bằng chứng execution đã xảy ra. Nó thuần túy là **request** — biểu thị "Strategy muốn exposure X," CHƯA được Risk Gateway duyệt, CHƯA gửi tới Execution.

**`trade-intent-issued`/`trade-intent-status-changed`/`trade-intent-fact-invalidated`/`trade-intent-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây, tách biệt display name/`event_type`, cùng nguyên tắc mọi Domain Contract trước.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/C1/C2/C3** (đóng trước, không chờ review round phát hiện): opaque identity không derive từ scope; `supersedes_fact_ref` có mặt ngay từ v0.1 trên `TradeIntentStatusChanged`; fold algorithm "visible-valid-head per slice"; Current View KHÔNG BAO GIỜ authority; canonical policy identifier khai báo ĐÚNG MỘT NƠI, độc lập theo context (dùng CHUNG context `strategy-decision` với `decision.md`, nhưng canonical identifier khai báo riêng, KHÔNG trùng lặp).

**Phạm vi bounded tường minh (v0.1):** KHÔNG author risk approval/rejection (Package 0.2-C5). KHÔNG author execution acceptance/order submission/fill status/position state (Package 0.2-C5–C7). KHÔNG định nghĩa order type/limit price/stop price/exchange payload. KHÔNG multi-instrument portfolio decomposition. Vocabulary hướng/action tối thiểu: `LONG`/`SHORT` — EXIT/FLAT KHÔNG author vì walking skeleton (§16 decision.md) không cần (§14).

## 1. Trade Intent — `kind: entity`

```yaml
id: trade-intent
kind: entity
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Request Strategy-originated biểu thị mong muốn market exposure — pin ĐÚNG MỘT Decision gốc
  (originating_decision_id), ĐÚNG MỘT Account, ĐÚNG MỘT TradableListing — CÙNG Account/instrument
  selection với Decision gốc (§7 invariant). Scope hoàn toàn bất biến sau khi đăng ký — KHÔNG có
  "mutable metadata" tách biệt (đối xứng StrategyInstanceRegistered, strategy.md §6). Lifecycle tối
  thiểu (ISSUED/WITHDRAWN/EXPIRED, §4) là phần DUY NHẤT thay đổi qua thời gian.
invariants:
  - "trade_intent_id là opaque, globally unique trong toàn Ride, gán tại TradeIntentIssued — KHÔNG derive/resolve từ originating_decision_id hay bất kỳ field scope nào. Bất biến, KHÔNG tái sử dụng cho subject khác (Chapter 6 §6.1)."
  - "MỘT Trade Intent originate từ ĐÚNG MỘT Decision (originating_decision_id, ref: decision) — không multi-Decision aggregation, đúng decision.md §8 cardinality (LONG/SHORT → tối đa một Trade Intent)."
  - "account_id/instrument_selection_ref PHẢI BẰNG HỆT strategy_evidence.account_id/instrument_selection_ref của originating_decision_id tương ứng (decision.md §3b) — Trade Intent KHÔNG được tự chọn Account/instrument khác Decision gốc đã pin."
  - "Trade Intent KHÔNG BAO GIỜ mutate Strategy evidence — mọi field strategy-evidence-liên-quan chỉ COPY từ Decision gốc để tiện truy vấn, KHÔNG phải nguồn authoritative thứ hai; nguồn authoritative luôn là chính Decision (decision.md §3b)."
  - "Trade Intent KHÔNG tự authorize execution dưới bất kỳ hình thức nào — `intent_type`/`direction` chỉ là request, KHÔNG phải quyết định thực thi; execution eligibility hoàn toàn thuộc Risk Gateway/Execution (Package 0.2-C5, chưa author)."
schema:
  trade_intent_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  originating_decision_id: {type: string, required: true, ref: decision, description: "đúng một Decision, result ∈ {LONG, SHORT}"}
  strategy_instance_id: {type: string, required: true, ref: strategy, description: "= subject_ref.scope.strategy_instance_id của originating_decision_id"}
  account_id: {type: string, required: true, ref: account, description: "= strategy_evidence.account_id của originating_decision_id — xem invariants"}
  instrument_selection_ref:
    type: object
    required: true
    description: "= strategy_evidence.instrument_selection_ref của originating_decision_id — CÙNG shape strategy.md §5/§10"
    fields:
      instrument_id: {type: string, required: true}
      venue_id: {type: string, required: true}
      listing_id: {type: string, required: true}
  direction: {type: enum, values: [LONG, SHORT], required: true, description: "= originating_decision_id.result — PHẢI khớp chính xác (LONG→LONG, SHORT→SHORT)"}
  intent_type: {type: enum, values: [OPEN], required: true, description: "v0.1: chỉ OPEN (request mở exposure theo direction) — CLOSE/REDUCE/FLAT deferred (§14), walking skeleton không cần"}
state_machine:
  initial_state: UNSEEN
  states: [UNSEEN, ISSUED, WITHDRAWN, EXPIRED]
  transitions:
    - {from: UNSEEN, to: ISSUED, caused_by: TradeIntentIssued}
    - {from: ISSUED, to: WITHDRAWN, caused_by: TradeIntentStatusChanged}
    - {from: ISSUED, to: EXPIRED, caused_by: TradeIntentStatusChanged}
  terminal_states: [WITHDRAWN, EXPIRED]
events_emitted: [TradeIntentIssued, TradeIntentStatusChanged, TradeIntentFactInvalidated]
events_consumed: []
commands: []
queries: []
```

**`UNSEEN` là notional initial state** — cùng convention xuyên suốt tài liệu. Lifecycle tối thiểu — chỉ đủ để C5 (Risk, chưa author) xác định Trade Intent còn eligible cho Risk evaluation hay không: `ISSUED` (mặc định, đủ điều kiện Risk evaluation); `WITHDRAWN` (Strategy/operator rút lại trước khi Risk xử lý — lý do cụ thể thuộc Phase 1); `EXPIRED` (hết hiệu lực theo thời gian — chính sách hết hạn cụ thể Phase 1, §14). **KHÔNG author** risk approval/rejection, execution acceptance, order submission, fill status, position state — những state đó thuộc Package 0.2-C5–C7. `WITHDRAWN`/`EXPIRED` là terminal CHO FORWARD TRANSITION nhưng correctable append-only (§5, đóng trước lớp lỗi `C2-MAJ-02`/`C3-MAJ-02`-style, không chờ review round phát hiện) — `supersedes_fact_ref` có mặt ngay từ v0.1 trên `TradeIntentStatusChanged`.

## 2. Canonical event envelope — áp dụng cho mọi Trade Intent event (§3–§5)

Mọi event trong tài liệu này là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). KHÔNG event nào trong tài liệu này thuộc `event_class: decision` — dùng envelope tiêu chuẩn, KHÔNG `decision_time`/`decision_context_cursor`.

```yaml
envelope:
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2)
  event_contract_ref: {cardinality: required}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}             # khi Ride ghi nhận fact này
  subject_ref: {cardinality: "required — shape canonical, xem dưới. Trên TradeIntentFactInvalidated, PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate."}
  stream_ref: {cardinality: required}                # Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # Phase 1, chưa author
  correlation_id: {cardinality: "required — Trade Intent LUÔN thuộc một correlation flow tường minh (originating Decision, xem §3)"}
  causation_refs: {cardinality: "TradeIntentIssued: KHÔNG BAO GIỜ rỗng, PHẢI chứa chính DecisionRecorded (decision.md §3) gốc. TradeIntentStatusChanged/TradeIntentFactInvalidated: KHÔNG BAO GIỜ rỗng."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3."}
  effective_time: {cardinality: "required — semantic khác theo event type, xem §3–§4 cho nội dung cụ thể."}
  market_time: {cardinality: "PROHIBITED — Trade Intent là request nội bộ authoritative, không phải quan sát trực tiếp venue (Chapter 5 §5.2)."}
  source_identity: {cardinality: "PROHIBITED — Trade Intent luôn phát sinh nội bộ từ Decision Engine/Strategy Engine (Phase 1, chưa author), KHÔNG BAO GIỜ từ external feed."}

subject_ref (Trade Intent):
  context_id: strategy-decision
  subject_kind: entity
  subject_type: TradeIntent
  subject_id: <trade_intent_id — opaque, stable, xem §1>
  scope:
    originating_decision_id: <string>
    account_id: <string>
    instrument_selection_ref: {instrument_id: <string>, venue_id: <string>, listing_id: <string>}

event_types:
  TradeIntentIssued: TRADE_INTENT_ISSUED
  TradeIntentStatusChanged: TRADE_INTENT_STATUS_CHANGED
  TradeIntentFactInvalidated: TRADE_INTENT_FACT_INVALIDATED
```

`stream_ref`/`producer_ref` — Phase 1, chưa tồn tại, cùng nguyên tắc defer xuyên suốt Package 0.2-B/C1–C4.

## 3. `TradeIntentIssued` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: trade-intent-issued
kind: event
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Fact AUTHORITATIVE cho việc phát MỘT Trade Intent — thiết lập TOÀN BỘ scope (originating_decision_id,
  strategy_instance_id, account_id, instrument_selection_ref, direction, intent_type) cùng lúc,
  BẤT BIẾN. CHỈ được phát khi `decision.md` §3e `trade_intent_outcome = ISSUED` (đúng MỘT
  TradeIntentIssued per Decision, decision.md §8). KHÔNG có supersedes_fact_ref — subject này KHÔNG
  BAO GIỜ có same-ID replacement (§5 giải thích lý do, đối xứng TradeIntentRegistered-style pattern
  của strategy.md §6).
invariants:
  - "payload.trade_intent_id PHẢI khớp đúng subject_ref.subject_id VÀ toàn bộ scope field PHẢI khớp subject_ref.scope."
  - "causation_refs PHẢI trỏ chính xác DecisionRecorded (decision.md §3) của originating_decision_id — chứng minh Decision đã tồn tại VÀ result ∈ {LONG, SHORT} trước khi Trade Intent phát."
  - "direction PHẢI khớp CHÍNH XÁC result của originating_decision_id (LONG→LONG, SHORT→SHORT) — KHÔNG được đảo/tự chọn direction khác Decision gốc."
  - "account_id/instrument_selection_ref PHẢI khớp CHÍNH XÁC strategy_evidence tương ứng của originating_decision_id (decision.md §3b) — không lệch."
  - "envelope.effective_time = thời điểm Trade Intent này thực sự có hiệu lực làm request — mặc định bằng recorded_time trừ khi backfill lịch sử tường minh pin effective_time sớm hơn (§9)."
  - "KHÔNG có field supersedes_fact_ref trong payload — subject này KHÔNG hỗ trợ same-ID correction replacement (§5: correction luôn invalidate, KHÔNG replacement — vì originating_decision_id KHÔNG BAO GIỜ đổi sau khi issue)."
payload:
  trade_intent_id: {type: string, required: true}
  originating_decision_id: {type: string, required: true}
  strategy_instance_id: {type: string, required: true}
  account_id: {type: string, required: true}
  instrument_selection_ref:
    instrument_id: {type: string, required: true}
    venue_id: {type: string, required: true}
    listing_id: {type: string, required: true}
  direction: {type: enum, values: [LONG, SHORT], required: true}
  intent_type: {type: enum, values: [OPEN], required: true}
```

## 4. `TradeIntentStatusChanged` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: trade-intent-status-changed
kind: event
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Fact AUTHORITATIVE cho một operational status transition của Trade Intent (§1 state_machine) —
  ISSUED→WITHDRAWN, ISSUED→EXPIRED. Cả hai terminal CHO FORWARD TRANSITION (§1) — nhưng correctable
  append-only qua same-slice replacement (đóng trước lớp lỗi C2-MAJ-02/C3-MAJ-02-style,
  supersedes_fact_ref có mặt ngay từ v0.1, KHÔNG chờ review round phát hiện).
invariants:
  - "new_status PHẢI là một transition hợp lệ theo state_machine §1 từ current_status hiện tại — current_status resolve theo fold algorithm §6 (visible-valid-head per slice, total-order effective_time ASC/recorded_time ASC/event_id ASC)."
  - "new_status = WITHDRAWN hoặc EXPIRED trên valid lineage hiện hành KHÔNG được có TradeIntentStatusChanged forward transition tiếp theo cho cùng trade_intent_id (§1 terminal_states) — ràng buộc FORWARD LIFECYCLE, không áp dụng cho correction record."
  - "Một WITHDRAWN/EXPIRED fact ghi SAI vẫn correctable qua TradeIntentFactInvalidated + same-slice TradeIntentStatusChanged replacement (§5, cùng (trade_intent_id, effective_time) slice, supersedes_fact_ref trỏ đúng fact bị invalidate) — correction KHÔNG bị chặn bởi terminality. Fold algorithm (§6) PHẢI recompute current_status từ valid corrected lineage."
  - "envelope.effective_time = thời điểm status transition này thực sự có hiệu lực."
  - "Trade Intent CHỈ eligible cho Risk evaluation MỚI (Package 0.2-C5, chưa author) khi current_status = ISSUED tại effective_time liên quan — WITHDRAWN/EXPIRED CẤM Risk evaluation mới; đây là RÀNG BUỘC lên Domain Contract tương lai (Risk, chưa author), trade-intent.md chỉ PIN quy tắc, không tự enforce vì chưa có consumer nào tồn tại."
  - "supersedes_fact_ref VẮNG MẶT cho forward transition bình thường; BẮT BUỘC cho same-slice correction replacement — khi có mặt, PHẢI trỏ đúng TradeIntentStatusChanged bị TradeIntentFactInvalidated target, cùng subject/effective_time (§5)."
payload:
  trade_intent_id: {type: string, required: true}
  new_status: {type: enum, values: [WITHDRAWN, EXPIRED], required: true}
  reason: {type: string, required: false}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho forward transition bình thường; BẮT BUỘC cho same-slice correction replacement — xem invariants và §5"}
```

## 5. `TradeIntentFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2. `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: trade-intent-fact-invalidated
kind: event
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Phủ định MỘT fact lịch sử cụ thể ĐÃ SAI của Trade Intent. Hai hành vi khác nhau theo target: (a)
  target = TradeIntentIssued → KHÔNG BAO GIỜ có replacement dưới cùng trade_intent_id (scope hoàn
  toàn bất biến — cùng lý do §3: originating_decision_id không đổi, một Trade Intent sai thực chất
  nghĩa là "Decision này không nên tạo Trade Intent," KHÔNG phải "Trade Intent sai cần sửa nội
  dung") — correction thực tế là invalidate, KHÔNG đăng ký trade_intent_id mới cho cùng Decision
  (một Decision LONG/SHORT tối đa một Trade Intent, decision.md §8 — nếu Trade Intent gốc sai, Decision
  gốc thường cũng cần xem lại qua decision.md §4, KHÔNG tự động ở đây); (b) target =
  TradeIntentStatusChanged → same-slice replacement HỢP LỆ, đúng correction lineage chuẩn (§6), kể
  cả khi giá trị bị invalidate là WITHDRAWN/EXPIRED.
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref."
  - "invalidated_fact_ref PHẢI trỏ một TradeIntentIssued hoặc TradeIntentStatusChanged, CHƯA từng nhận invalidation khác — một fact chỉ bị invalidate đúng một lần. KHÔNG BAO GIỜ trỏ một TradeIntentFactInvalidated khác (cấm invalidation-of-invalidation)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead)."
  - "Target = TradeIntentIssued: sau invalidation, trade_intent_id đó VĨNH VIỄN TERMINALLY_INVALID (§6) — KHÔNG BAO GIỜ có replacement dưới cùng ID."
  - "Target = TradeIntentStatusChanged: mong đợi (không bắt buộc ngay lập tức) một TradeIntentStatusChanged replacement CÙNG trade_intent_id VÀ cùng effective_time slice, supersedes_fact_ref = event này (§6)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 6. `TradeIntentCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §3–§5.

```text
Trước khi TradeIntentIssued tồn tại cho một trade_intent_id:
  → KHÔNG có TradeIntentCurrentView row nào tồn tại
  → GetCurrentTradeIntent trả về NOT_FOUND / ABSENT
```

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION`. Khi `PENDING_CORRECTION`, `pending_correction_class` BẮT BUỘC có mặt (đóng ngay từ v0.1, đúng pattern đã proven tại `strategy.md` §9):

```text
view_state = VALID              → pending_correction_class: CẤM (phải absent)
view_state = PENDING_CORRECTION → pending_correction_class: BẮT BUỘC

target = TradeIntentIssued (invalidate, không bao giờ replacement) → pending_correction_class = TERMINAL_SCOPE_INVALIDATION
target = TradeIntentStatusChanged (invalidate, chờ same-slice replacement) → pending_correction_class = AWAITING_SAME_SUBJECT_REPLACEMENT
```

**Fold algorithm (v0.1, "visible-valid-head per slice" — MỘT quy tắc chung, đóng ngay từ đầu, đúng pattern đã proven tại `strategy.md` §9):**

```text
1. Group mọi fact theo correction lineage/effective-time slice — mỗi (trade_intent_id, effective_time)
   là một slice riêng.
2. Với mỗi slice, resolve TradeIntentFactInvalidated visibility tại cursor (recorded_time <= cursor).
3. Loại trừ khỏi lineage bất kỳ fact nào đã có invalidation visible tại cursor.
4. Chọn head hợp lệ (visible valid head) của slice: fact CHƯA bị invalidate visible, hoặc
   replacement mới nhất (chuỗi supersedes_fact_ref, CHỈ áp dụng cho TradeIntentStatusChanged, §5)
   CHƯA bị invalidate visible.
5. NẾU slice issuance bị invalidate visible → toàn view chuyển PENDING_CORRECTION,
   pending_correction_class = TERMINAL_SCOPE_INVALIDATION, DỪNG.
6. NẾU issuance hợp lệ, tiếp tục fold TradeIntentStatusChanged: một slice status bị invalidate
   chưa có replacement visible KHÔNG đóng góp fact nào (không "giữ giá trị cũ") — fold dùng head
   hợp lệ của slice effective_time gần nhất trước đó.
7. Tổng hợp mọi visible-valid-head còn lại, total-order: effective_time ASC, recorded_time ASC,
   event_id ASC — rồi mới lifecycle fold → current_status.
```

```yaml
id: trade-intent-current-view
kind: read_model
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Projection tiện dụng: status "hiện tại" (latest-state, KHÔNG cursor-addressable theo mặc định)
  của một Trade Intent, rebuild được từ §3–§5. KHÔNG authoritative — CHỈ query/UI, KHÔNG BAO GIỜ là
  input hợp lệ cho Risk/Execution (Package 0.2-C5, chưa author) hay computation nào khác, kể cả khi
  "trông giống" cùng giá trị. Downstream field PHẢI resolve qua authoritative Trade Intent event
  stream (`ref: trade-intent`) TẠI CÙNG cursor mà computation đó đang dùng (§11). Cache chỉ chấp
  nhận khi ĐỒNG THỜI cursor-addressable VÀ provably equivalent với authoritative reconstruction.
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho Risk/Execution hay bất kỳ computation nào khác — CHỈ query/UI."
  - "view_state PHẢI đúng theo Bước 4–5 của fold algorithm — issuance lineage head quyết định."
  - "pending_correction_class BẮT BUỘC có mặt khi view_state = PENDING_CORRECTION; CẤM có mặt khi view_state = VALID."
  - "current_status PHẢI recompute đúng theo Bước 6–7 — một WITHDRAWN/EXPIRED fact đã invalidate mà chưa có replacement visible KHÔNG được góp phần vào current_status."
schema:
  trade_intent_id: {type: string, required: true}
  scope: {originating_decision_id: string, strategy_instance_id: string, account_id: string, instrument_selection_ref: object, direction: string, intent_type: string, required: true, description: "chỉ có mặt khi view_state = VALID"}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  pending_correction_class: {type: enum, values: [AWAITING_SAME_SUBJECT_REPLACEMENT, TERMINAL_SCOPE_INVALIDATION], required: false}
  current_status: {type: enum, values: [ISSUED, WITHDRAWN, EXPIRED], required: false, description: "chỉ có mặt khi view_state = VALID"}
  last_recorded_time: timestamp
queries: [GetCurrentTradeIntent, GetTradeIntentHistory]
```

## 7. Decision-to-Trade-Intent cardinality — xem `decision.md` §8

Định nghĩa authoritative đầy đủ tại [`decision.md`](./decision.md) §8 — trade-intent.md KHÔNG lặp lại, chỉ tái khẳng định ràng buộc chiều ngược: **mọi TradeIntentIssued PHẢI causally trace về đúng MỘT DecisionRecorded với `result ∈ {LONG, SHORT}` VÀ `trade_intent_outcome = ISSUED`** (§3 invariant) — KHÔNG có TradeIntentIssued "mồ côi" không originating Decision, KHÔNG có TradeIntentIssued nào từ một Decision `result = NO_ACTION`.

## 8. Correction lineage

Correction lineage scoped chính xác theo `(subject_id, effective_time)` — mỗi effective_time-slice có chuỗi lineage RIÊNG, cùng nguyên tắc đã khóa xuyên suốt `instrument.md`/`venue.md`/`account.md`/`strategy.md`.

**`TradeIntentIssued` — invalidate-only, KHÔNG replacement (§3/§5):**

```text
F1 (TradeIntentIssued)
  → TradeIntentFactInvalidated targeting F1
  → KHÔNG có replacement dưới cùng trade_intent_id — correction thực tế là invalidate, KHÔNG
    đăng ký trade_intent_id mới cho cùng originating_decision_id.
```

**`TradeIntentStatusChanged` — correction lineage chuẩn, same-slice replacement (§4/§5), mười invariant chuẩn (đối xứng `strategy.md` §13, KHÔNG lặp lại toàn văn):**

```text
F1 (TradeIntentStatusChanged)
  → TradeIntentFactInvalidated targeting F1
  → replacement (cùng event type TradeIntentStatusChanged), supersedes_fact_ref = F1
```

## 9. Time semantics và bitemporal correctness

- `effective_time` — required trên mọi event trong tài liệu này (KHÔNG `decision_time`/`decision_context_cursor` — những field đó CHỈ thuộc `decision.md`'s `DecisionRecorded`, `event_class: decision`).
- `recorded_time` — recorded axis, universal.
- Replay tại cursor T chỉ thấy fact có `recorded_time ≤ T` — invalidation ghi SAU T KHÔNG visible tại T.
- `market_time` PROHIBITED xuyên suốt tài liệu này.

## 10. Canonical policy identifiers — nguồn duy nhất (context `strategy-decision`, riêng cho Trade Intent)

**Một canonical policy identifier bổ sung, khai báo tại đây** — context `strategy-decision` đã có `initial_fact_correction_policy`/`decision_computation_idempotency_policy`/`decision_non_creation_policy` khai báo tại `decision.md` §11 (áp dụng cho Decision subject); Trade Intent tái sử dụng CHÍNH `initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS` (đúng giá trị, KHÔNG khai báo trùng lặp — cùng context, một lần duy nhất tại `decision.md` §11 là đủ, áp dụng cho CẢ `TradeIntentIssued`) cho phần registration bất biến; `TradeIntentStatusChanged` dùng correction lineage chuẩn (§8), KHÔNG cần policy identifier riêng (đối xứng cách `strategy.md` §12 xử lý `StrategyInstanceStatusChanged`).

## 11. Downstream reference contract (cho Package 0.2-C5 Risk, chưa author)

Package sau (Risk, Package 0.2-C5, chưa author) tham chiếu Trade Intent qua ĐÚNG các field sau, KHÔNG hơn:

```yaml
trade_intent_id: {type: string, required: true, ref: trade-intent}
originating_decision_id: {type: string, description: "= §1, ref: decision"}
strategy_instance_id: {type: string, description: "= §1"}
account_id: {type: string, ref: account, description: "= §1"}
instrument_selection_ref: {type: object, description: "= §1 — {instrument_id, venue_id, listing_id}"}
direction: {type: enum, values: [LONG, SHORT], description: "= §1"}
intent_type: {type: enum, values: [OPEN], description: "= §1"}
current_status: {type: enum, values: [ISSUED, WITHDRAWN, EXPIRED], description: "PHẢI resolve từ authoritative event stream TẠI cursor, KHÔNG TradeIntentCurrentView latest-state — xem invariant dưới"}
```

**Downstream authority rule — MỘT quy tắc duy nhất, không ngoại lệ (đúng pattern đã proven `account.md` §13/`strategy.md` §10/`decision.md` §12):** downstream package PHẢI resolve mọi field trên TRỰC TIẾP từ authoritative Trade Intent event stream (§3–§5) TẠI ĐÚNG cursor mà chính computation đó đang dùng. `TradeIntentCurrentView` latest-state (§6) KHÔNG BAO GIỜ được dùng làm input. `trade-intent.md` KHÔNG author semantics của Risk approval/rejection/execution (Package 0.2-C5, chưa author).

## 12. Prohibitions

**Trade Intent KHÔNG được sở hữu:** Decision evidence/rule semantics (thuộc `decision.md`); Risk approval/rejection/limit/sizing (Package 0.2-C5, chưa author); Execution acceptance/order submission/fill status/position state (Package 0.2-C5–C7); order type/limit price/stop price/exchange payload; capital allocation/multi-strategy arbitration; module-registry entry.

## 13. Ngoài phạm vi — defer

**Deferred tường minh, không author ở C4 (Phase 1 implementation concern, non-blocking):**

- Chính sách hết hạn cụ thể (`EXPIRED` trigger timing/mechanism) — Phase 1.
- Lý do `WITHDRAWN` cụ thể (operator action, Strategy Instance pause cascade hay không) — Phase 1/C5 concern, deferred.
- `EXIT`/`FLAT`/`CLOSE`/`REDUCE` intent_type — walking skeleton (decision.md §16) không cần, tránh premature action taxonomy (đúng yêu cầu "avoid prematurely designing advanced order types").
- Multi-instrument/portfolio-level Trade Intent — v0.1 tối đa một instrument selection per Trade Intent (§1), đúng cardinality decision.md §8.
- Runtime worker ownership, transaction boundaries, retry/backoff, monitoring/escalation (Phase 1, cùng nguyên tắc defer đã áp dụng xuyên suốt Package 0.2).

## 14. Open questions ngoài phạm vi

- Cơ chế cụ thể generate `trade_intent_id` — chưa quyết, Phase 1, cùng nguyên tắc defer đã áp dụng cho `decision_id`.
- Retention/resolvability horizon cụ thể cho Trade Intent đã WITHDRAWN/EXPIRED — chưa pin ở v0.1.
- Không đóng OQ-002/OQ-003.
