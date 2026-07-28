---
id: candle
title: Candle
version: "0.2"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-07-28"
last_review: null
next_review: null
---

# Candle

> **Vai trò của tài liệu này:** Domain Contract đầu tiên của Phase 0.2 — worked conformance example chứng minh `context-map.yaml` resolve đúng đầu cuối theo [Chapter 4 §4.2](../constitution/04-domain-principles.md). Đây vẫn là `Draft`, chưa qua Independent Review B / consolidation. **v0.2** xử lý ChatGPT Review A (M-01, m-01, m-02) trên baseline v0.1.

Candle bao gồm **năm concept riêng biệt**, cùng thuộc capability `market-data` / context `market-data-observation` (đăng ký tại [`context-map.yaml`](./context-map.yaml)):

1. **Logical Candle Subject** (`kind: entity`) — identity ổn định của "candle này".
2. **`CandleObserved`** (`kind: event`) — quan sát khi còn PROVISIONAL.
3. **`CandleClosed`** (`kind: event`) — quan sát cuối, authoritative, khi cửa sổ đã đóng.
4. **`CandleCorrected`** (`kind: event`) — sửa một fact đã publish.
5. **`CandleDataGapObserved`** (`kind: event`, optional) — tín hiệu tường minh thiếu dữ liệu.

Cộng một **read model** (`CandleCurrentView`) — projection tiện dụng, không authoritative.

Không mô hình hóa Candle như **một bản ghi mutable** mà lịch sử provisional bị ghi đè — mọi observation là event append-only riêng biệt (I-3), theo đúng pattern `state_machine` mà [Chapter 4 §4.3](../constitution/04-domain-principles.md) đã minh họa cho Swing.

## 1. Logical Candle Subject — `kind: entity`

```yaml
id: candle
kind: entity
capability_id: market-data
domain_context_id: market-data-observation
description: >
  Trạng thái tổng hợp OHLCV của một instrument, tại một venue, theo một timeframe, trong
  một cửa sổ effective_time xác định. Subject CÓ một identity opaque, ổn định
  (`candle_subject_id`) — KHÔNG phải một Entity không-identity — cộng một qualifying scope
  tường minh (instrument_id, venue_id, timeframe, window_start, window_end). Hai đại lượng
  này KHÔNG trùng nhau và KHÔNG cạnh tranh nhau: `candle_subject_id` là handle opaque dùng để
  so khớp identity (Chapter 6 §6.1/§6.8 — domain logic cấm parse nó); `scope` là dữ liệu tường
  minh dùng để lọc/truy vấn theo nghiệp vụ. Cả hai cùng có mặt trong `subject_ref` của mọi
  event mô tả subject này (§2).
invariants:
  - "candle_subject_id bất biến, KHÔNG tái sử dụng cho một subject khác, và resolve deterministic từ đúng một qualifying scope (instrument_id, venue_id, timeframe, window_start) — cùng scope luôn cho cùng candle_subject_id, khác scope không bao giờ trùng candle_subject_id (Chapter 6 §6.1)."
  - "candle_subject_id là opaque — domain logic KHÔNG được parse nó để suy diễn instrument/venue/timeframe/window (Chapter 6 §6.8); mọi quyết định nghiệp vụ phải dùng field tường minh trong scope, không phải giải mã ID."
  - "effective_time là interval [window_start, window_end) xác định bởi timeframe — không đổi qua mọi observation/correction của cùng subject."
  - "instrument_id, venue_id, timeframe, effective_time bất biến sau khi subject được quan sát lần đầu — đổi bất kỳ field nào tạo ra một subject KHÁC (candle_subject_id khác), không phải mutate subject cũ."
schema:
  candle_subject_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  instrument_id: {type: string, required: true, ref: instrument}
  venue_id: {type: string, required: true, ref: venue}
  timeframe: {type: string, required: true}
  effective_time:
    kind: interval
    window_start: {type: timestamp, required: true}
    window_end: {type: timestamp, required: true}
state_machine:
  states: [PROVISIONAL, CLOSED]
  transitions:
    - {from: PROVISIONAL, to: PROVISIONAL, caused_by: CandleObserved}
    - {from: PROVISIONAL, to: CLOSED, caused_by: CandleClosed}
    - {from: CLOSED, to: CLOSED, caused_by: CandleCorrected}
  terminal_states: []
events_emitted: [CandleObserved, CandleClosed, CandleCorrected, CandleDataGapObserved]
events_consumed: []
commands: []
queries: []
```

**Một semantic duy nhất cho correction — không mơ hồ (đóng m-01):** `CandleCorrected` **KHÔNG** đưa subject ra khỏi `CLOSED`. Subject **giữ nguyên `CLOSED`**; correction là một **self-transition `CLOSED → CLOSED`** tường minh trong `state_machine` ở trên, và thay thế fact-đang-hiệu-lực trong `CandleCurrentView` (§7) — **không** phải một entity-state transition đưa subject sang trạng thái khác. `terminal_states: []` chỉ phản ánh đúng một sự kiện: subject không bao giờ **rời khỏi** `CLOSED` để quay lại `PROVISIONAL`, nhưng vẫn tiếp tục nhận `CandleCorrected` dưới dạng self-transition. Đây là ví dụ hợp lệ của [Chapter 2 I-13](../constitution/02-platform-invariants.md): *"Constitution không tự áp đặt 'mọi terminal state = zero outbound transition' cho mọi entity — đó là quyết định của từng Domain Contract."*

## 2. Canonical event envelope — áp dụng cho mọi Candle event (§3–§6)

Mọi event ở §3–§6 là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). Mục này khóa **envelope chung** một lần — từng event bên dưới chỉ khai báo **payload đặc thù**, KHÔNG lặp lại envelope (tránh duplicate declaration của cùng một authority). Chapter 8 sở hữu nguyên vẹn semantic của envelope; mục này **chỉ áp dụng, không định nghĩa lại**.

```yaml
envelope:                                          # Chapter 8 §8.2.1 — cardinality nguyên văn
  event_id: {cardinality: required}                # mọi event record (Chapter 6 §6.2)
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2) — xem bảng dưới
  event_contract_ref: {cardinality: required}        # {contract_id, contract_version} — pin đúng Event Contract của event_type này
  schema_version: {cardinality: required}            # version payload schema (khác event_contract_ref — Chapter 8 §8.2.5)
  recorded_time: {cardinality: required}             # Chapter 5
  subject_ref: {cardinality: required}               # shape canonical — xem dưới
  stream_ref: {cardinality: required}                # {stream_id, registry_version} — thuộc stream-registry.yaml (Chapter 8 §8.3.1, Phase 1, chưa author)
  sequence: {cardinality: required}                  # vị trí trong stream (Chapter 8 §8.3.2)
  producer_ref: {cardinality: required}              # {module_id, implementation_version, run_id} — module_id thuộc module-registry.yaml (Chapter 7 §7.5, Phase 1, chưa author)
  correlation_id: {cardinality: "required nếu event thuộc một luồng xử lý; optional nếu khởi phát độc lập — Candle event là root/independent observation tại ingestion nên mặc định Optional, trừ khi chính ingestion run gắn một correlation_id (ví dụ một lần backfill/replay cụ thể)"}
  causation_refs: {cardinality: "zero-to-many; PHẢI là [] tường minh cho root event (CandleObserved, CandleClosed, CandleDataGapObserved không sửa fact nào trước — Chapter 8 §8.2.1: 'root event có thể rỗng ([]), không absent'). CandleCorrected KHÔNG rỗng — xem §5."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3"}
  effective_time: {cardinality: "required cho Candle — đây là fact có effective time (khác Decision event, nơi effective_time bị cấm và decision_time thay thế — Chapter 8 §8.4). Giá trị = interval [window_start, window_end) của Logical Candle Subject (§1)."}
  market_time: {cardinality: "conditional — chỉ khi venue cung cấp (Chapter 5 §5.2)"}
  source_identity: {cardinality: "conditional — bắt buộc khi source có khả năng retry/redelivery (Chapter 6 §6.6) — xem §9"}

subject_ref:                                       # shape canonical — Chapter 8 §8.2.2
  context_id: market-data-observation
  subject_kind: entity
  subject_type: Candle
  subject_id: <candle_subject_id — opaque, stable, xem §1>
  scope:
    instrument_id: <string>
    venue_id: <string>
    timeframe: <string>
    window_start: <timestamp>
    window_end: <timestamp>

event_types:                                       # Chapter 3 §3.2 naming — tham chiếu, không định nghĩa lại quy tắc đặt tên
  CandleObserved: CANDLE_OBSERVED
  CandleClosed: CANDLE_CLOSED
  CandleCorrected: CANDLE_CORRECTED
  CandleDataGapObserved: CANDLE_DATA_GAP_OBSERVED
```

`stream_ref`/`producer_ref` resolve từ `stream-registry.yaml`/`module-registry.yaml` — cả hai thuộc Phase 1, chưa tồn tại tại Phase 0.2. Domain Contract chỉ khóa **field phải có mặt**, không chốt giá trị cụ thể trước khi các registry đó được author — cùng nguyên tắc defer mechanism mà toàn bộ Chapter 8 đã áp dụng.

**`subject_id` luôn giống nhau cho cùng cửa sổ logic:** mọi `CandleObserved`/`CandleClosed`/`CandleCorrected`/`CandleDataGapObserved` mô tả cùng một `(instrument_id, venue_id, timeframe, window_start)` PHẢI mang cùng `subject_ref.subject_id`. Event record vẫn có `event_id` riêng, bất biến, cho từng bản ghi (Chapter 6 §6.2: New Event ID ≠ New Entity ID) — `subject_id` KHÔNG thay thế `event_id`.

## 3. `CandleObserved` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: candle-observed
kind: event
capability_id: market-data
domain_context_id: market-data-observation
description: >
  Một quan sát OHLCV khi Candle còn PROVISIONAL (đang forming). Có thể phát sinh nhiều lần
  cho cùng một Logical Candle Subject trước khi đóng — mỗi lần là một event record riêng,
  append-only, không ghi đè observation trước. Envelope đầy đủ theo §2; `causation_refs: []`
  (root event).
invariants:
  - "Không mutate hay xóa observation trước đó — mọi CandleObserved trước vẫn giữ nguyên trong log (I-3)."
  - "payload.state luôn PROVISIONAL trên event này — CLOSED chỉ hợp lệ trên CandleClosed."
  - "market_time (khi venue cung cấp, trong envelope §2) = window_start theo Chapter 5 §5.2 — không tạo market_time giả."
payload:
  state: {type: enum, value: PROVISIONAL, required: true}
  open: {type: decimal, required: true}
  high: {type: decimal, required: true}
  low: {type: decimal, required: true}
  close: {type: decimal, required: true}
  volume: {type: decimal, required: true}
```

## 4. `CandleClosed` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: candle-closed
kind: event
capability_id: market-data
domain_context_id: market-data-observation
description: >
  Quan sát OHLCV cuối cùng, authoritative, khi cửa sổ effective_time đã đóng. Đánh dấu
  Logical Candle Subject chuyển PROVISIONAL → CLOSED (§1). KHÔNG xóa hay ghi đè các
  CandleObserved trước đó. Envelope đầy đủ theo §2; `causation_refs: []` (root event —
  không sửa một fact nào trước; correction dùng CandleCorrected, §5).
invariants:
  - "Đúng một CandleClosed authoritative cho mỗi Logical Candle Subject, trước khi có correction."
  - "envelope.effective_time giống hệt mọi CandleObserved cùng subject."
  - "payload.data_quality PHẢI khai báo tường minh — không mặc định 'complete' khi không xác nhận được."
  - "payload.data_quality = complete_zero_volume CHỈ hợp lệ khi thỏa đủ điều kiện provenance ở §10 — không được suy diễn chỉ từ việc vắng mặt trade/message."
payload:
  state: {type: enum, value: CLOSED, required: true}
  open: {type: decimal, required: true}
  high: {type: decimal, required: true}
  low: {type: decimal, required: true}
  close: {type: decimal, required: true}
  volume: {type: decimal, required: true}
  data_quality: {type: enum, values: [complete, complete_zero_volume], required: true}
```

## 5. `CandleCorrected` — `kind: event`

Kế thừa nguyên vẹn envelope §2 — **ngoại lệ duy nhất: `causation_refs` KHÔNG rỗng.** Payload đặc thù:

```yaml
id: candle-corrected
kind: event
capability_id: market-data
domain_context_id: market-data-observation
description: >
  Sửa một CandleClosed (hoặc một CandleCorrected trước đó) đã publish, khi venue gửi
  correction muộn — đúng ví dụ Chapter 5 §5.1 đã dùng (candle 10:00 bị sửa lúc 10:07). Là
  event MỚI, KHÔNG mutate record gốc (I-3 append-only). KHÔNG đưa Logical Candle Subject ra
  khỏi CLOSED — self-transition CLOSED → CLOSED (§1).
invariants:
  - "envelope.effective_time KHÔNG đổi so với fact gốc — correction mô tả lại cùng cửa sổ, không tạo cửa sổ mới, subject_id không đổi."
  - "envelope.recorded_time PHẢI mới hơn recorded_time của fact đang được sửa."
  - "envelope.causation_refs PHẢI trỏ chính xác event đang được sửa (Chapter 8 §8.2.3), KHÔNG được rỗng — cấm correction không tham chiếu fact gốc."
  - "Replay tại cursor trước recorded_time của correction KHÔNG được thấy correction này (Chapter 5 §5.1/§5.3 — chống look-ahead)."
  - "payload.state luôn CLOSED — correction không tạo trạng thái mới cho subject (§1)."
payload:
  state: {type: enum, value: CLOSED, required: true}
  open: {type: decimal, required: true}
  high: {type: decimal, required: true}
  low: {type: decimal, required: true}
  close: {type: decimal, required: true}
  volume: {type: decimal, required: true}
  correction_reason: {type: string, required: false}
```

## 6. `CandleDataGapObserved` — `kind: event` (optional, ingestion-adapter-emitted)

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: candle-data-gap-observed
kind: event
capability_id: market-data
domain_context_id: market-data-observation
description: >
  Tín hiệu tường minh "không có dữ liệu đáng tin cậy cho cửa sổ này", phát sinh bởi
  ingestion adapter khi phiên đang mở nhưng dữ liệu bị thiếu/trễ/không khả dụng. Envelope đầy
  đủ theo §2; `causation_refs: []` (root event). Tồn tại để downstream (Structure/Regime/
  Feature) phân biệt "im lặng vì chưa ai gửi gì" khỏi "im lặng vì đã xác nhận thiếu dữ liệu"
  — xem §10.
invariants:
  - "payload KHÔNG chứa field OHLC — cấm dùng event này để tổng hợp giá trị Candle."
  - "KHÔNG tự phát sinh khi phiên (session) đã đóng theo Venue/session authority — đó là case hợp lệ, không phải gap (§10)."
  - "Là optional/best-effort signal — vắng mặt CandleDataGapObserved KHÔNG chứng minh dữ liệu đầy đủ."
payload:
  reason: {type: enum, values: [source_unavailable, delayed_beyond_threshold, unknown], required: true}
```

## 7. `CandleCurrentView` — `kind: read_model`

**Không phải authoritative event — không chịu envelope §2** (§2 áp dụng cho event record; read model là derived projection, không phải fact được append). Rebuild được từ §3–§6.

```yaml
id: candle-current-view
kind: read_model
capability_id: market-data
domain_context_id: market-data-observation
description: >
  Projection tiện dụng: giá trị Candle "hiện tại" cho một subject, rebuild được từ
  CandleObserved/CandleClosed/CandleCorrected. KHÔNG authoritative — chỉ derived
  representation (I-12); mọi audit/replay/parity phải dùng authoritative event stream,
  không dùng view này làm nguồn sự thật.
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (I-12) — không có state độc lập ngoài event log."
  - "Không được dùng làm input cho Decision khi chưa qua cursor-bounded query (Chapter 9 §9.5, một khi Candle trở thành decision-relevant)."
schema:
  candle_subject_id: {type: string, required: true}
  scope: {instrument_id: string, venue_id: string, timeframe: string, effective_time: interval, required: true}
  state: {type: enum, values: [PROVISIONAL, CLOSED], required: true}
  open: decimal
  high: decimal
  low: decimal
  close: decimal
  volume: decimal
  last_recorded_time: timestamp
  correction_count: {type: integer, required: true}
queries: [GetCurrentCandle, GetCandleHistory]
```

## 8. Time semantics — không overload một field hai nghĩa

Dùng đúng field canonical [Chapter 5](../constitution/05-time-model.md) — **không dùng `event_time`** (đã bị loại bỏ khỏi Constitution vì từng mang hai nghĩa đối nghịch):

```text
window_start / window_end   — biên của cửa sổ aggregation, thuộc schema effective_time (interval)
effective_time               — chính là [window_start, window_end) — KHÔNG phải field riêng thứ ba
recorded_time                — khi Ride ghi nhận fact này (bắt buộc, mọi event — envelope §2)
market_time                  — timestamp venue cung cấp, = window_start khi có (Chapter 5 §5.2)
```

`effective_time` dùng dạng **interval** (Chapter 8 §8.2.1 cho phép "instant hoặc interval") thay vì hai field `open_time`/`close_time` cạnh tranh nghĩa với nó — tránh hai field cùng biểu diễn một trục thời gian ([I-12](../constitution/02-platform-invariants.md)).

## 9. Provisional và Closed — không ghi đè lịch sử

Mọi `CandleObserved` trong lúc PROVISIONAL **giữ nguyên trong log** kể cả sau khi `CandleClosed` phát sinh — đây chính là evidence cần thiết cho no-repaint audit test ([I-3](../constitution/02-platform-invariants.md) Verification): so sánh output tại Replay time T với đúng tập dữ liệu available tại T đòi hỏi các observation PROVISIONAL vẫn truy được, không bị "gộp" hay xóa khi candle đóng.

## 10. Correction

`CandleCorrected` là event mới, `envelope.causation_refs` trỏ đúng fact bị sửa, `envelope.effective_time` không đổi, `envelope.recorded_time` mới hơn. Không có đường nào mutate `CandleClosed`/`CandleObserved` gốc. State machine semantics: xem §1 (self-transition `CLOSED → CLOSED`, không phải rời `CLOSED`).

## 11. Missing data — ba trường hợp tách bạch, không tự tổng hợp

| Trường hợp | Xử lý |
|---|---|
| **Venue/session hợp lệ đóng** | **Không thuộc phạm vi candle.md** — trả lời bởi Venue/session authority ở context `instrument-venue-reference` (đăng ký tại `context-map.yaml`, contract chưa author). Candle không tự suy session state từ việc vắng mặt candle. |
| **Session mở, không có trade** | `CandleClosed` với `payload.data_quality: complete_zero_volume` — chỉ hợp lệ khi thỏa **đủ cả năm điều kiện provenance** dưới đây. |
| **Thiếu/trễ/không khả dụng** | **Cấm tự tổng hợp OHLC giả.** Không có `CandleClosed` cho cửa sổ đó; ingestion adapter **có thể** phát `CandleDataGapObserved` như tín hiệu tường minh, nhưng vắng mặt event này **không chứng minh** dữ liệu đầy đủ — downstream phải coi window thiếu là data-quality condition tường minh, không phải "coi như flat". |

**Điều kiện provenance bắt buộc cho `data_quality: complete_zero_volume` (đóng m-02) — thiếu bất kỳ điều kiện nào thì KHÔNG hợp lệ, phải xử lý như case thứ ba (gap):**

1. Authoritative source/producer **xác nhận tường minh** một candle zero-volume đã hoàn tất (venue thực sự publish "đã đóng, không có trade"), không phải suy diễn từ im lặng.
2. `envelope.producer_ref` resolve đúng tới producer đã xác nhận điều đó ở (1).
3. `envelope.event_contract_ref` resolve tới đúng Event Contract cho phép semantic `complete_zero_volume` (không phải mọi Event Contract của `CandleClosed` mặc định cho phép giá trị này).
4. `envelope.source_identity` **có mặt** khi source đó có khả năng retry/redelivery (Chapter 6 §6.6) — để dedup đúng nếu venue gửi lại cùng xác nhận.
5. Ingestion adapter **không** tự suy `complete_zero_volume` chỉ từ việc không nhận được trade/message nào trong cửa sổ — im lặng của nguồn dữ liệu **không phải** bằng chứng "nguồn đã xác nhận zero-volume".

**Không có source assertion → không phát sinh `CandleClosed` tổng hợp → biểu diễn bằng gap/data-quality condition** (case thứ ba, `CandleDataGapObserved` nếu ingestion adapter phát hiện được).

## 12. Deduplication

`envelope.source_identity` theo [Chapter 6 §6.6](../constitution/06-identity-model.md) — hai delivery của cùng một authoritative source fact (ví dụ WS reconnect replay gửi lại cùng candle, hoặc cùng một zero-volume confirmation) **không được** tạo hai business effect. Schema ví dụ, cùng pattern §6.6 đã minh họa:

```yaml
source_identity:
  venue: binance
  instrument_id: BTCUSDT
  type: kline_update_id     # hoặc tương đương do venue cung cấp
  value: "..."
```

## 13. Venue & session neutrality (ADR-007)

Cửa sổ `[window_start, window_end)` phải suy ra từ **trading calendar/session của Venue** (context `instrument-venue-reference`), **không hardcode** giả định "00:00–24:00 UTC liên tục" như một quy tắc phổ quát — kể cả khi crypto hiện tại luôn 24/7. Không leak raw field venue-specific (ví dụ cờ "is-closed" riêng của một venue) vào schema canonical ở trên — normalize tại ranh giới ingestion adapter, trước khi tạo event.

## 14. Replay/Backtest/Paper/Live parity

Cả bốn execution mode tiêu thụ **đúng cùng** envelope (§2) và payload (§3–§6) của `CandleObserved`/`CandleClosed`/`CandleCorrected` ([I-2](../constitution/02-platform-invariants.md)) — adapter nạp dữ liệu có thể khác theo mode (WS stream cho Live, historical file cho Backtest), nhưng domain semantic không đổi theo mode.

## 15. Authority boundary

Contract này sở hữu: Candle observation/closure/correction semantics, `CandleCurrentView` projection shape. **Áp dụng, không định nghĩa lại:** event envelope (thuộc [Chapter 8 §8.2](../constitution/08-event-model.md)); ordering/replay cursor mechanics (thuộc [Chapter 5](../constitution/05-time-model.md)/[Chapter 8](../constitution/08-event-model.md)); dedup mechanism (thuộc [Chapter 6 §6.6](../constitution/06-identity-model.md)); ID opaque rule (thuộc [Chapter 6 §6.8](../constitution/06-identity-model.md)). **Không sở hữu:** Instrument/Venue identity (thuộc `instrument-venue-reference`, chưa author); stream/module registry content (Phase 1, chưa tồn tại).

## 16. Ngoài phạm vi — defer

Enum cụ thể cho `timeframe`; storage/schema/serialization format; ngưỡng `delayed_beyond_threshold` của `CandleDataGapObserved`; cơ chế chuẩn hóa venue-specific field tại ingestion adapter; cơ chế tính `candle_subject_id` deterministic cụ thể (content hash, hay tương đương — chỉ khóa tính chất *opaque + stable + deterministic từ scope*, không khóa thuật toán). Tất cả thuộc Engineering Foundation/Phase 1, không khóa ở Domain Contract này.
