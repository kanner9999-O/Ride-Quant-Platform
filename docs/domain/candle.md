---
id: candle
title: Candle
version: "0.1"
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

> **Vai trò của tài liệu này:** Domain Contract đầu tiên của Phase 0.2 — worked conformance example chứng minh `context-map.yaml` resolve đúng đầu cuối theo [Chapter 4 §4.2](../constitution/04-domain-principles.md). Đây vẫn là `Draft`, chưa qua review nào (§13).

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
  một cửa sổ effective_time xác định. Subject KHÔNG có một opaque ID riêng — identity là
  tổ hợp tường minh (instrument_id, venue_id, timeframe, effective_time.window_start),
  dùng trực tiếp làm subject_ref/scope (Chapter 8 §8.2.2), không phải một chuỗi bị parse
  ngược để suy ra business meaning (Chapter 6 §6.8).
invariants:
  - "effective_time là interval [window_start, window_end) xác định bởi timeframe — không đổi qua mọi observation/correction của cùng subject."
  - "instrument_id, venue_id, timeframe bất biến sau khi subject được quan sát lần đầu — đổi bất kỳ field nào tạo ra một subject KHÁC, không phải mutate subject cũ."
  - "Không suy diễn business meaning từ việc parse bất kỳ ID nào (Chapter 6 §6.8) — mọi field định danh đều tường minh, không nhúng trong một ID cơ hội."
schema:
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
    - {from: PROVISIONAL, to: PROVISIONAL}
    - {from: PROVISIONAL, to: CLOSED}
  terminal_states: []
events_emitted: [CandleObserved, CandleClosed, CandleCorrected, CandleDataGapObserved]
events_consumed: []
commands: []
queries: []
```

`terminal_states: []` — **CLOSED không phải strictly terminal**: một `CandleCorrected` vẫn hợp lệ tham chiếu tới một subject đã CLOSED (§4). Đây là ví dụ đúng của [Chapter 2 I-13](../constitution/02-platform-invariants.md): *"Constitution không tự áp đặt 'mọi terminal state = zero outbound transition' cho mọi entity — đó là quyết định của từng Domain Contract."*

## 2. `CandleObserved` — `kind: event`

```yaml
id: candle-observed
kind: event
capability_id: market-data
domain_context_id: market-data-observation
description: >
  Một quan sát OHLCV khi Candle còn PROVISIONAL (đang forming). Có thể phát sinh nhiều lần
  cho cùng một Logical Candle Subject trước khi đóng — mỗi lần là một event record riêng
  (Chapter 6 §6.2: New Event ID ≠ New Entity ID), append-only, không ghi đè observation trước.
invariants:
  - "Không mutate hay xóa observation trước đó — mọi CandleObserved trước vẫn giữ nguyên trong log (I-3)."
  - "state luôn PROVISIONAL trên event này — CLOSED chỉ hợp lệ trên CandleClosed."
  - "market_time (khi venue cung cấp) = window_start theo Chapter 5 §5.2 — không tạo market_time giả."
schema:
  subject_ref:
    instrument_id: {type: string, required: true}
    venue_id: {type: string, required: true}
    timeframe: {type: string, required: true}
    effective_time: {kind: interval, window_start: timestamp, window_end: timestamp, required: true}
  state: {type: enum, value: PROVISIONAL, required: true}
  open: {type: decimal, required: true}
  high: {type: decimal, required: true}
  low: {type: decimal, required: true}
  close: {type: decimal, required: true}
  volume: {type: decimal, required: true}
  recorded_time: {type: timestamp, required: true}
  market_time: {type: timestamp, required: false}
  source_identity: {type: object, required: false}
```

## 3. `CandleClosed` — `kind: event`

```yaml
id: candle-closed
kind: event
capability_id: market-data
domain_context_id: market-data-observation
description: >
  Quan sát OHLCV cuối cùng, authoritative, khi cửa sổ effective_time đã đóng. Đánh dấu
  Logical Candle Subject chuyển PROVISIONAL → CLOSED. KHÔNG xóa hay ghi đè các CandleObserved
  trước đó — chúng vẫn là bằng chứng lịch sử hợp lệ cho no-repaint audit (I-3).
invariants:
  - "Đúng một CandleClosed authoritative cho mỗi Logical Candle Subject, trước khi có correction."
  - "effective_time giống hệt mọi CandleObserved cùng subject."
  - "data_quality PHẢI khai báo tường minh — không mặc định 'complete' khi không xác nhận được (§9)."
schema:
  subject_ref: {instrument_id: string, venue_id: string, timeframe: string, effective_time: interval, required: true}
  state: {type: enum, value: CLOSED, required: true}
  open: {type: decimal, required: true}
  high: {type: decimal, required: true}
  low: {type: decimal, required: true}
  close: {type: decimal, required: true}
  volume: {type: decimal, required: true}
  data_quality: {type: enum, values: [complete, complete_zero_volume], required: true}
  recorded_time: {type: timestamp, required: true}
  market_time: {type: timestamp, required: false}
  source_identity: {type: object, required: false}
```

## 4. `CandleCorrected` — `kind: event`

```yaml
id: candle-corrected
kind: event
capability_id: market-data
domain_context_id: market-data-observation
description: >
  Sửa một CandleClosed (hoặc một CandleCorrected trước đó) đã publish, khi venue gửi
  correction muộn — đúng ví dụ Chapter 5 §5.1 đã dùng (candle 10:00 bị sửa lúc 10:07). Là
  event MỚI, KHÔNG mutate record gốc (I-3 append-only).
invariants:
  - "effective_time KHÔNG đổi so với fact gốc — correction mô tả lại cùng cửa sổ, không tạo cửa sổ mới."
  - "recorded_time PHẢI mới hơn recorded_time của fact đang được sửa."
  - "causation_refs PHẢI trỏ chính xác event đang được sửa (Chapter 8 §8.2.3) — cấm correction không tham chiếu fact gốc."
  - "Replay tại cursor trước recorded_time của correction KHÔNG được thấy correction này (Chapter 5 §5.1/§5.3 — chống look-ahead)."
schema:
  subject_ref: {instrument_id: string, venue_id: string, timeframe: string, effective_time: interval, required: true}
  state: {type: enum, value: CLOSED, required: true}
  open: {type: decimal, required: true}
  high: {type: decimal, required: true}
  low: {type: decimal, required: true}
  close: {type: decimal, required: true}
  volume: {type: decimal, required: true}
  correction_reason: {type: string, required: false}
  causation_refs: {type: array, of: event_record_ref, required: true, min_items: 1}
  recorded_time: {type: timestamp, required: true}
  market_time: {type: timestamp, required: false}
  source_identity: {type: object, required: false}
```

## 5. `CandleDataGapObserved` — `kind: event` (optional, ingestion-adapter-emitted)

```yaml
id: candle-data-gap-observed
kind: event
capability_id: market-data
domain_context_id: market-data-observation
description: >
  Tín hiệu tường minh "không có dữ liệu đáng tin cậy cho cửa sổ này", phát sinh bởi
  ingestion adapter khi phiên đang mở nhưng dữ liệu bị thiếu/trễ/không khả dụng. Tồn tại để
  downstream (Structure/Regime/Feature) phân biệt "im lặng vì chưa ai gửi gì" khỏi "im lặng
  vì đã xác nhận thiếu dữ liệu" — xem §9.
invariants:
  - "KHÔNG chứa field OHLC — cấm dùng event này để tổng hợp giá trị Candle."
  - "KHÔNG tự phát sinh khi phiên (session) đã đóng theo Venue/session authority — đó là case hợp lệ, không phải gap (§9)."
  - "Là optional/best-effort signal — vắng mặt CandleDataGapObserved KHÔNG chứng minh dữ liệu đầy đủ."
schema:
  subject_ref: {instrument_id: string, venue_id: string, timeframe: string, effective_time: interval, required: true}
  reason: {type: enum, values: [source_unavailable, delayed_beyond_threshold, unknown], required: true}
  recorded_time: {type: timestamp, required: true}
```

## 6. `CandleCurrentView` — `kind: read_model`

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
  subject_ref: {instrument_id: string, venue_id: string, timeframe: string, effective_time: interval, required: true}
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

## 7. Time semantics — không overload một field hai nghĩa

Dùng đúng field canonical [Chapter 5](../constitution/05-time-model.md) — **không dùng `event_time`** (đã bị loại bỏ khỏi Constitution vì từng mang hai nghĩa đối nghịch):

```text
window_start / window_end   — biên của cửa sổ aggregation, thuộc schema effective_time (interval)
effective_time               — chính là [window_start, window_end) — KHÔNG phải field riêng thứ ba
recorded_time                — khi Ride ghi nhận fact này (bắt buộc, mọi event)
market_time                  — timestamp venue cung cấp, = window_start khi có (Chapter 5 §5.2)
```

`effective_time` dùng dạng **interval** (Chapter 8 §8.2.1 cho phép "instant hoặc interval") thay vì hai field `open_time`/`close_time` cạnh tranh nghĩa với nó — tránh hai field cùng biểu diễn một trục thời gian ([I-12](../constitution/02-platform-invariants.md)).

## 8. Provisional và Closed — không ghi đè lịch sử

Mọi `CandleObserved` trong lúc PROVISIONAL **giữ nguyên trong log** kể cả sau khi `CandleClosed` phát sinh — đây chính là evidence cần thiết cho no-repaint audit test ([I-3](../constitution/02-platform-invariants.md) Verification): so sánh output tại Replay time T với đúng tập dữ liệu available tại T đòi hỏi các observation PROVISIONAL vẫn truy được, không bị "gộp" hay xóa khi candle đóng.

## 9. Correction

`CandleCorrected` là event mới, `causation_refs` trỏ đúng fact bị sửa, `effective_time` không đổi, `recorded_time` mới hơn. Không có đường nào mutate `CandleClosed`/`CandleObserved` gốc.

## 10. Missing data — ba trường hợp tách bạch, không tự tổng hợp

| Trường hợp | Xử lý |
|---|---|
| **Venue/session hợp lệ đóng** | **Không thuộc phạm vi candle.md** — trả lời bởi Venue/session authority ở context `instrument-venue-reference` (đăng ký tại `context-map.yaml`, contract chưa author). Candle không tự suy session state từ việc vắng mặt candle. |
| **Session mở, không có trade** | `CandleClosed` với `data_quality: complete_zero_volume` — **chỉ hợp lệ khi chính source contract cung cấp nó như một observation authoritative** (ví dụ venue xác nhận "không trade nhưng đã đóng nến"), không phải suy diễn ngầm. |
| **Thiếu/trễ/không khả dụng** | **Cấm tự tổng hợp OHLC giả.** Không có `CandleClosed` cho cửa sổ đó; ingestion adapter **có thể** phát `CandleDataGapObserved` như tín hiệu tường minh, nhưng vắng mặt event này **không chứng minh** dữ liệu đầy đủ — downstream phải coi window thiếu là data-quality condition tường minh, không phải "coi như flat". |

## 11. Deduplication

`source_identity` theo [Chapter 6 §6.6](../constitution/06-identity-model.md) — hai delivery của cùng một authoritative source fact (ví dụ WS reconnect replay gửi lại cùng candle) **không được** tạo hai business effect. Schema ví dụ, cùng pattern §6.6 đã minh họa:

```yaml
source_identity:
  venue: binance
  instrument_id: BTCUSDT
  type: kline_update_id     # hoặc tương đương do venue cung cấp
  value: "..."
```

## 12. Venue & session neutrality (ADR-007)

Cửa sổ `[window_start, window_end)` phải suy ra từ **trading calendar/session của Venue** (context `instrument-venue-reference`), **không hardcode** giả định "00:00–24:00 UTC liên tục" như một quy tắc phổ quát — kể cả khi crypto hiện tại luôn 24/7. Không leak raw field venue-specific (ví dụ cờ "is-closed" riêng của một venue) vào schema canonical ở trên — normalize tại ranh giới ingestion adapter, trước khi tạo event.

## 13. Replay/Backtest/Paper/Live parity

Cả bốn execution mode tiêu thụ **đúng cùng** `CandleObserved`/`CandleClosed`/`CandleCorrected` contract ở trên ([I-2](../constitution/02-platform-invariants.md)) — adapter nạp dữ liệu có thể khác theo mode (WS stream cho Live, historical file cho Backtest), nhưng domain semantic không đổi theo mode.

## 14. Authority boundary

Contract này sở hữu: Candle observation/closure/correction semantics, `CandleCurrentView` projection shape. **Không sở hữu:** Instrument/Venue identity (thuộc `instrument-venue-reference`, chưa author); ordering/replay cursor mechanics (thuộc [Chapter 5](../constitution/05-time-model.md)/[Chapter 8](../constitution/08-event-model.md), chỉ áp dụng ở đây, không định nghĩa lại); dedup mechanism cụ thể (thuộc [Chapter 6 §6.6](../constitution/06-identity-model.md), áp dụng không định nghĩa lại).

## 15. Ngoài phạm vi — defer

Enum cụ thể cho `timeframe`; storage/schema/serialization format; ngưỡng `delayed_beyond_threshold` của `CandleDataGapObserved`; cơ chế chuẩn hóa venue-specific field tại ingestion adapter. Tất cả thuộc Engineering Foundation/Phase 1, không khóa ở Domain Contract này.
