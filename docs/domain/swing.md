---
id: swing
title: Swing
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

# Swing

> **Vai trò của tài liệu này:** Domain Contract đầu tiên của Package 0.2-B1 (Data & analysis chain) — mở đầu chuỗi `Candle → Swing → Structure`. Draft, chưa qua review nào (author self-review only), chưa Approved/Locked. Thuộc capability `market-structure` / context `market-structure-analysis` (đã đăng ký tại [`context-map.yaml`](./context-map.yaml)).

Swing bao gồm **bốn concept riêng biệt**:

1. **Logical Swing Subject** (`kind: entity`) — identity ổn định của "swing pivot này".
2. **`SwingCandidateDetected`** (`kind: event`) — quan sát provisional, khi pivot vừa xuất hiện nhưng chưa đủ right-side evidence.
3. **`SwingConfirmed`** (`kind: event`) — fact authoritative, khi pivot đã thỏa confirmation policy.
4. **`SwingInvalidated`** (`kind: event`) — fact mới phủ định một candidate hoặc confirmed Swing trước đó.

Cộng một **read model tùy chọn** (`SwingCurrentView`) — projection tiện dụng, không authoritative.

**Không mô hình hóa Swing như một bản ghi mutable bị ghi đè.** Mọi observation/confirmation/invalidation là event append-only riêng biệt (I-3), đúng pattern `state_machine` mà [Chapter 4 §4.3](../constitution/04-domain-principles.md) đã minh họa cho chính Swing, và đúng ba loại identity (`event_id`/`entity_id`/value object) mà [Chapter 6 §6.2](../constitution/06-identity-model.md) đã dùng Swing làm ví dụ minh họa trực tiếp (`swing_id` giữ nguyên xuyên `SwingPublished`/`SwingInvalidated` — ở đây cụ thể hóa thành `SwingCandidateDetected`/`SwingConfirmed`/`SwingInvalidated`).

**`swing-candidate-detected` / `swing-confirmed` / `swing-invalidated` / `swing-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây, và đúng giá trị `contract_id` mà [`context-map.yaml`](./context-map.yaml) sẽ trích dẫn. Display name (`SwingConfirmed`), concept ID (`swing-confirmed`), và `event_type` (`SWING_CONFIRMED`) là ba đại lượng khác nhau, không cạnh tranh identity — cùng nguyên tắc [`candle.md`](./candle.md) đã khóa.

## 1. Logical Swing Subject — `kind: entity`

```yaml
id: swing
kind: entity
capability_id: market-structure
domain_context_id: market-structure-analysis
description: >
  Một pivot điểm cấu trúc (local high hoặc local low) trên một chuỗi Candle authoritative,
  tại một instrument/venue/timeframe, theo một Swing Definition Version cụ thể. Subject có
  một identity opaque, ổn định (`swing_id`) — KHÔNG phải Entity không-identity — cộng một
  qualifying scope tường minh. Hai đại lượng này KHÔNG cạnh tranh nhau: `swing_id` là handle
  opaque dùng để so khớp identity (Chapter 6 §6.1/§6.8 — domain logic cấm parse nó); scope là
  dữ liệu tường minh dùng để lọc/truy vấn theo nghiệp vụ.
invariants:
  - "swing_id resolve deterministic từ ĐÚNG SÁU field qualifying scope: instrument_id, venue_id, timeframe, direction, pivot_candle_subject_id, swing_definition_version — cùng sáu-field-scope luôn cho cùng swing_id; khác bất kỳ field nào trong sáu field đó cho swing_id KHÁC. swing_id bất biến, KHÔNG tái sử dụng cho một subject khác (Chapter 6 §6.1)."
  - "swing_id là opaque — domain logic KHÔNG được parse nó để suy diễn instrument/venue/timeframe/direction/pivot/definition (Chapter 6 §6.8); mọi quyết định nghiệp vụ phải dùng field tường minh trong scope."
  - "pivot_candle_subject_id tham chiếu đúng candle_subject_id của Logical Candle Subject (candle.md §1) chứa giá trị pivot — KHÔNG phải một reference tới một event record cụ thể; subject reference này bất biến kể cả khi CandleClosed của cửa sổ đó sau bị CandleCorrected (§10)."
  - "swing_definition_version thuộc scope identity — HAI Swing hợp lệ, khác nhau, được phép cùng tồn tại trên cùng pivot_candle_subject_id + direction nếu chúng dùng swing_definition_version khác nhau (§9). KHÔNG được thiết kế identity theo cách chỉ cho phép một cách diễn giải Swing tồn tại trên một Candle."
  - "instrument_id, venue_id, timeframe, direction, pivot_candle_subject_id, swing_definition_version bất biến sau khi subject được quan sát lần đầu (CANDIDATE hoặc CONFIRMED trực tiếp) — đổi bất kỳ field nào tạo ra một subject KHÁC (swing_id khác), không phải mutate subject cũ."
  - "pivot_effective_time PHẢI khớp effective_time của Candle mà pivot_candle_subject_id trỏ tới (candle.md §1) — không được lệch; đây là dữ liệu tường minh trùng lặp có chủ đích cho query, không phải trục identity độc lập thứ bảy."
schema:
  swing_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  instrument_id: {type: string, required: true, ref: instrument}
  venue_id: {type: string, required: true, ref: venue}
  timeframe: {type: string, required: true}
  direction: {type: enum, values: [HIGH, LOW], required: true}
  pivot_candle_subject_id: {type: string, required: true, ref: candle}
  pivot_effective_time: {kind: interval, window_start: {type: timestamp, required: true}, window_end: {type: timestamp, required: true}}
  swing_definition_version: {type: string, required: true, description: "pin chính xác Swing Definition policy đã dùng — §9"}
state_machine:
  initial_state: UNSEEN
  states: [UNSEEN, CANDIDATE, CONFIRMED, INVALIDATED]
  transitions:
    - {from: UNSEEN, to: CANDIDATE, caused_by: SwingCandidateDetected}
    - {from: UNSEEN, to: CONFIRMED, caused_by: SwingConfirmed}
    - {from: CANDIDATE, to: CONFIRMED, caused_by: SwingConfirmed}
    - {from: CANDIDATE, to: INVALIDATED, caused_by: SwingInvalidated}
    - {from: CONFIRMED, to: INVALIDATED, caused_by: SwingInvalidated}
  terminal_states: [INVALIDATED]
events_emitted: [SwingCandidateDetected, SwingConfirmed, SwingInvalidated]
events_consumed: [CandleClosed, CandleCorrected]
commands: []
queries: []
```

**`UNSEEN` là notional initial state** — không event nào khẳng định "subject đang UNSEEN"; cùng convention mà [`candle.md` §1](./candle.md) đã khóa cho Candle. Khai báo tường minh bằng `initial_state` để tránh mơ hồ, nhất quán minh họa gốc của [Chapter 4 §4.3](../constitution/04-domain-principles.md) (nơi `CANDIDATE` ngầm định là initial state vì không có inbound transition).

**`UNSEEN → CONFIRMED` là đường hợp lệ cho historical/closed-only ingestion** (đối xứng với `candle.md` §1's `UNSEEN → CLOSED`): khi nạp dữ liệu lịch sử đã có đủ left+right evidence sẵn (Backtest đọc toàn bộ chuỗi Candle đã đóng), subject đi thẳng `UNSEEN → CONFIRMED` qua `SwingConfirmed` — **không được fabricate một `SwingCandidateDetected` giả** chỉ để "đi đúng qua CANDIDATE trước". `SwingConfirmed` không bắt buộc phải có `SwingCandidateDetected` đứng trước nó cho cùng subject; trong trường hợp này, `causation_refs` của `SwingConfirmed` trỏ trực tiếp tới pivot Candle fact + toàn bộ right-side evidence Candle fact, không trỏ tới một candidate event không tồn tại.

**`terminal_states: [INVALIDATED]`** — khác `candle.md` (nơi Candle không có terminal state, vì `CandleCorrected` luôn còn hợp lệ trên `CLOSED`). Ở đây, một khi `INVALIDATED`, subject **không** nhận thêm transition nào — một Swing bị invalidate (dù do market evolution hay do Candle correction) không "sống lại"; nếu recompute sau correction cho ra một Swing hợp lệ trở lại, đó là một **fact mới** trên cùng `swing_id` (nếu pivot Candle subject không đổi, §10) nhưng đường đi vẫn phải qua `UNSEEN`-tương-đương của chính fact mới đó — hệ thống không tái mở một subject đã `INVALIDATED`; thay vào đó phát `SwingCandidateDetected`/`SwingConfirmed` **mới** cùng `swing_id`, với `causation_refs` trỏ rõ tới `SwingInvalidated` trước đó (chain lịch sử đầy đủ, không xóa `INVALIDATED` khỏi log). Điều này nhất quán với I-3 (append-only) — "terminal" mô tả **không có outbound transition từ chính fact đó**, không cấm cùng `swing_id` xuất hiện lại qua một chuỗi fact mới.

## 2. Canonical event envelope — áp dụng cho mọi Swing event (§3–§5)

Mọi event ở §3–§5 là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). Mục này khóa **envelope chung** một lần — từng event bên dưới chỉ khai báo **payload đặc thù**. Chapter 8 sở hữu nguyên vẹn semantic của envelope; mục này **chỉ áp dụng, không định nghĩa lại**.

```yaml
envelope:                                          # Chapter 8 §8.2.1 — cardinality nguyên văn
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2) — xem bảng dưới
  event_contract_ref: {cardinality: required}        # {contract_id, contract_version}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}             # Chapter 5 — khi Ride tính/ghi nhận fact này, KHÔNG phải pivot time
  subject_ref: {cardinality: required}               # shape canonical — xem dưới
  stream_ref: {cardinality: required}                # {stream_id, registry_version} — Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # {module_id, implementation_version, run_id} — Phase 1, chưa author
  correlation_id: {cardinality: "required khi Swing computation thuộc một correlation flow tường minh (ví dụ một lần backfill/replay cụ thể); optional khi computation độc lập"}
  causation_refs: {cardinality: "KHÔNG BAO GIỜ rỗng cho bất kỳ Swing event nào (khác Candle root event) — Swing LUÔN là derived fact từ Candle fact + (khi có) Swing event trước đó của cùng subject. Zero-to-many nhưng tối thiểu một phần tử — xem §3–§5 cho nội dung cụ thể từng event."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3"}
  effective_time: {cardinality: "required — LUÔN LUÔN = pivot_effective_time của Logical Swing Subject (§1), bất biến qua CANDIDATE/CONFIRMED/INVALIDATED của cùng swing_id. KHÔNG mở rộng theo evidence window (§9) — xem §7."}
  market_time: {cardinality: "PROHIBITED — Swing là derived/computed fact, không phải quan sát trực tiếp venue; market_time chỉ hợp lệ trên event mà venue cung cấp timestamp trực tiếp (candle.md §2)."}
  source_identity: {cardinality: "PROHIBITED — Swing không có external source retry/redelivery risk (Chapter 6 §6.6 áp cho inbound external fact); dedup của Swing dùng computation/causation identity, xem §12."}

subject_ref:                                       # shape canonical — Chapter 8 §8.2.2
  context_id: market-structure-analysis
  subject_kind: entity
  subject_type: Swing
  subject_id: <swing_id — opaque, stable, xem §1>
  scope:
    instrument_id: <string>
    venue_id: <string>
    timeframe: <string>
    direction: <HIGH | LOW>
    swing_definition_version: <string>

event_types:                                       # Chapter 3 §3.2 naming — tham chiếu, không định nghĩa lại quy tắc đặt tên
  SwingCandidateDetected: SWING_CANDIDATE_DETECTED
  SwingConfirmed: SWING_CONFIRMED
  SwingInvalidated: SWING_INVALIDATED
```

`stream_ref`/`producer_ref` resolve từ `stream-registry.yaml`/`module-registry.yaml` — cả hai thuộc Phase 1, chưa tồn tại tại Phase 0.2, cùng nguyên tắc defer mà `candle.md` §2 đã áp dụng.

**`subject_id` luôn giống nhau cho cùng qualifying scope:** mọi `SwingCandidateDetected`/`SwingConfirmed`/`SwingInvalidated` mô tả cùng một `(instrument_id, venue_id, timeframe, direction, pivot_candle_subject_id, swing_definition_version)` PHẢI mang cùng `subject_ref.subject_id`. Event record vẫn có `event_id` riêng, bất biến, cho từng bản ghi (Chapter 6 §6.2).

## 3. `SwingCandidateDetected` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: swing-candidate-detected
kind: event
capability_id: market-structure
domain_context_id: market-structure-analysis
description: >
  Một pivot vừa được phát hiện dựa trên left-side evidence đầy đủ (§9), nhưng CHƯA có đủ
  right-side evidence để confirm. Fact PROVISIONAL — có thể không bao giờ tiến tới CONFIRMED
  (§5, invalidation do market evolution), hoặc bị recompute nếu Candle trong causal ancestry
  bị correct (§10). `causation_refs` trỏ chính xác pivot Candle fact (CandleClosed hoặc
  CandleCorrected đang authoritative hiện tại) — KHÔNG rỗng, vì candidate luôn được suy ra từ
  một Candle fact cụ thể, không phải quan sát độc lập.
invariants:
  - "causation_refs PHẢI chứa đúng một event_record_ref trỏ pivot Candle fact (candle-closed hoặc candle-corrected) đang authoritative tại thời điểm detect; có thể chứa thêm left-side evidence Candle fact nếu Swing Definition Version (§9) yêu cầu chúng làm điều kiện detect."
  - "Không tạo candidate thứ hai cho cùng swing_id khi một candidate đã tồn tại và chưa bị invalidate — một pivot chỉ có đúng một SwingCandidateDetected authoritative tại một thời điểm (§12 xử lý duplicate detection)."
  - "payload.evidence_completeness luôn PARTIAL trên event này — FULL chỉ hợp lệ trên SwingConfirmed."
payload:
  pivot_price: {type: decimal, required: true, description: "giá trị extreme (high hoặc low tùy direction) tại pivot_candle_subject_id, theo price_basis đã pin ở swing_definition_version (§9)"}
  left_evidence_refs: {type: array, items: event_record_ref, required: true, description: "Candle fact làm bằng chứng bên trái, theo left_count đã pin ở swing_definition_version (§9)"}
  evidence_completeness: {type: enum, value: PARTIAL, required: true}
```

## 4. `SwingConfirmed` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: swing-confirmed
kind: event
capability_id: market-structure
domain_context_id: market-structure-analysis
description: >
  Pivot đã thỏa đủ right-side evidence theo confirmation policy (§9) — fact AUTHORITATIVE,
  analytical output chính thức của Swing Domain Contract, dùng làm input cho Structure
  (structure.md). `causation_refs` chứa: SwingCandidateDetected của cùng swing_id (nếu tồn
  tại — đường CANDIDATE → CONFIRMED), HOẶC pivot + toàn bộ right-side evidence Candle fact
  trực tiếp (đường UNSEEN → CONFIRMED, historical ingestion, §1); cộng right-side evidence
  Candle fact chưa từng xuất hiện ở candidate (nếu có).
invariants:
  - "causation_refs KHÔNG rỗng — tối thiểu trỏ pivot Candle fact; nếu đi qua CANDIDATE, PHẢI bao gồm chính SwingCandidateDetected đó."
  - "envelope.effective_time KHÔNG đổi so với SwingCandidateDetected của cùng swing_id (nếu tồn tại) — confirmation không dịch chuyển pivot time, chỉ xác nhận nó (§7)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của right-side evidence Candle fact cuối cùng cần thiết để thỏa confirmation policy — KHÔNG được confirm trước khi evidence đó tồn tại (§7, chống look-ahead)."
  - "Đúng một SwingConfirmed authoritative cho mỗi swing_id, trừ khi đã bị INVALIDATED và một chuỗi fact mới (candidate/confirmed) phát sinh sau đó trên cùng swing_id (§1, §10) — khi đó SwingConfirmed mới PHẢI causation tới SwingInvalidated trước đó."
  - "payload.evidence_completeness luôn FULL trên event này."
payload:
  pivot_price: {type: decimal, required: true}
  right_evidence_refs: {type: array, items: event_record_ref, required: true, description: "Candle fact làm bằng chứng bên phải, theo right_count đã pin ở swing_definition_version (§9)"}
  evidence_completeness: {type: enum, value: FULL, required: true}
```

## 5. `SwingInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2 — **`causation_refs` không rỗng.** Payload đặc thù:

```yaml
id: swing-invalidated
kind: event
capability_id: market-structure
domain_context_id: market-structure-analysis
description: >
  Phủ định một SwingCandidateDetected hoặc SwingConfirmed trước đó của cùng swing_id. HAI
  nguyên nhân tách biệt, PHẢI khai báo tường minh qua payload.invalidation_cause — không gộp
  chung một nhánh mơ hồ:
  (a) market_evolution — giá phá qua pivot trước khi candidate kịp confirm (chỉ hợp lệ khi
      subject đang CANDIDATE, KHÔNG hợp lệ khi đã CONFIRMED — xem §8/no-repaint);
  (b) upstream_correction — CandleCorrected làm thay đổi giá trị pivot hoặc right-side
      evidence trong causal ancestry, khiến fact trước đó không còn đúng (hợp lệ trên cả
      CANDIDATE và CONFIRMED).
  Là event MỚI, KHÔNG mutate record gốc (I-3).
invariants:
  - "causation_refs PHẢI trỏ chính xác: (a) event đang bị invalidate (SwingCandidateDetected hoặc SwingConfirmed của cùng swing_id — bắt buộc); (b) event là nguyên nhân invalidation — Candle fact phá pivot (market_evolution) hoặc CandleCorrected (upstream_correction)."
  - "invalidation_cause = market_evolution CHỈ hợp lệ khi subject đang CANDIDATE tại thời điểm phát sinh — một SwingConfirmed KHÔNG được invalidate chỉ vì giá tiếp tục di chuyển sau đó (đó là BOS/CHoCH ở tầng Structure, không phải Swing invalidation — §8)."
  - "invalidation_cause = upstream_correction hợp lệ trên cả CANDIDATE và CONFIRMED — CandleCorrected trong causal ancestry buộc recompute bất kể lifecycle stage hiện tại (§10)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của event gây invalidation."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (Chapter 5 — chống look-ahead)."
payload:
  invalidation_cause: {type: enum, values: [market_evolution, upstream_correction], required: true}
  invalidation_reason: {type: string, required: false}
```

## 6. `SwingCurrentView` — `kind: read_model` (optional)

**Không phải authoritative event — không chịu envelope §2** (§2 áp dụng cho event record; read model là derived projection — Chapter 7 §7.4 Type 2 Projection). Rebuild được từ §3–§5. Optional vì Structure (structure.md) tiêu thụ trực tiếp event stream, không bắt buộc phải qua view này — view này chỉ phục vụ query/UI tiện dụng.

```yaml
id: swing-current-view
kind: read_model
capability_id: market-structure
domain_context_id: market-structure-analysis
description: >
  Projection tiện dụng: trạng thái "hiện tại" của một Swing subject, rebuild được từ
  SwingCandidateDetected/SwingConfirmed/SwingInvalidated. KHÔNG authoritative — mọi
  audit/replay/parity, và mọi input cho Structure, phải dùng authoritative event stream, không
  dùng view này làm nguồn sự thật (I-12, Chapter 7 §7.4).
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream cùng swing_definition_version đã pin, cùng implementation version (Chapter 7 §7.4 rebuild determinism) — không có state độc lập ngoài event log."
  - "KHÔNG được dùng làm input cho Structure hay bất kỳ Decision — chỉ dùng cho query/UI (Chapter 7 §7.4, Chapter 9 §9.5 khi Swing trở thành decision-relevant)."
  - "Không có view row nào tồn tại khi subject còn UNSEEN (§1) — kỳ vọng bình thường, KHÔNG phải missing-data condition (§11)."
schema:
  swing_id: {type: string, required: true}
  scope: {instrument_id: string, venue_id: string, timeframe: string, direction: string, swing_definition_version: string, required: true}
  state: {type: enum, values: [CANDIDATE, CONFIRMED, INVALIDATED], required: true}
  pivot_price: decimal
  pivot_effective_time: interval
  last_recorded_time: timestamp
queries: [GetCurrentSwing, GetSwingHistory]
```

## 7. Time semantics — pivot time tách biệt khỏi evidence/recorded time

```text
pivot_effective_time         — [window_start, window_end) của pivot Candle (§1) — BẤT BIẾN qua mọi lifecycle stage của cùng swing_id
evidence window              — payload.left_evidence_refs / right_evidence_refs (§3–§4) — KHÔNG mở rộng envelope.effective_time
recorded_time                — khi Ride tính/ghi nhận fact này (bắt buộc, mọi event — envelope §2)
market_time                  — PROHIBITED (§2) — Swing không phải quan sát venue trực tiếp
```

**Không dùng `event_time`** (loại bỏ khỏi Constitution — Chapter 5).

**Phân biệt bắt buộc T vs T+n:** một Swing mô tả pivot tại thời điểm `pivot_effective_time` (ví dụ candle 09:00), nhưng **chỉ được biết** (`recorded_time`) tại thời điểm right-side evidence đã đủ — có thể là 09:00 + N×timeframe. `envelope.effective_time` **giữ nguyên** tại pivot time trên cả `SwingCandidateDetected` lẫn `SwingConfirmed` — chỉ `recorded_time` tiến về sau. Điều này đảm bảo: (a) truy vấn "Swing nào có pivot tại thời điểm X" luôn đúng theo effective axis; (b) truy vấn "hệ thống biết về Swing này từ khi nào" luôn đúng theo recorded axis; hai câu hỏi không bị trộn vào một field duy nhất.

**Replay cursor visibility:** tại một cursor recorded_time T, replay chỉ được thấy các Swing event có `recorded_time ≤ T` — không được suy diễn ngược "vì pivot_effective_time nằm trước T nên Swing hẳn đã được biết trước T". Một `SwingConfirmed` với `pivot_effective_time = 09:00` nhưng `recorded_time = 09:45` (do cần 9 right-side Candle ở timeframe M5) **không** visible tại cursor 09:10 — đây chính là cơ chế chống backfill/look-ahead mà §9 và §11 dựa vào.

## 8. Provisional vs authoritative — và ranh giới no-repaint

- **`SwingCandidateDetected` là provisional** — có thể không bao giờ confirm; downstream (Structure) **không được** coi candidate là fact đủ để publish BOS/CHoCH, chỉ dùng để biểu diễn "đang chờ xác nhận" nếu cần.
- **`SwingConfirmed` là authoritative analytical output** — một khi phát sinh, **không bao giờ bị ghi đè tại chỗ**; sau confirmation, Swing chỉ có thể bị phủ định qua `SwingInvalidated` với `invalidation_cause: upstream_correction` (§5) — **KHÔNG** qua `market_evolution` (giá tiếp tục di chuyển sau khi đã confirm **không** làm Swing sai; đó là input hợp lệ cho BOS/CHoCH ở structure.md, không phải lý do invalidate Swing chính nó). Đây là ranh giới no-repaint cốt lõi của contract này: **một Swing đã CONFIRMED tại recorded_time T sẽ luôn hiển thị y hệt khi replay tại mọi cursor ≥ T, trừ khi một CandleCorrected thực sự thay đổi dữ liệu nó dựa vào.**
- **Invalidation là fact mới** — không event nào mutate hay xóa fact trước đó (I-3).

## 9. Confirmation semantics — pinned policy, không hardcode một trường phái

Left/right count, price basis, và equal-level policy **là policy evidence phải pin theo `swing_definition_version`** (§1 schema) — Domain Contract này **không** chọn một phương pháp phân tích kỹ thuật cụ thể làm chuẩn phổ quát duy nhất, đúng tinh thần tách "Structure semantic contract" khỏi "specific strategy/configuration policy" mà Package 0.2-B1 yêu cầu.

```yaml
swing_definition:                    # Domain Contract của policy này — schema tối thiểu, KHÔNG khóa giá trị cụ thể
  swing_definition_version: <string>  # opaque, immutable pin — Referenced Authoritative Artifact (Chapter 8 §8.1.1: versioned, immutable sau khi tham chiếu, resolvable trong replay horizon)
  left_count: <integer>               # số Candle bên trái pivot cần thỏa left-side evidence
  right_count: <integer>              # số Candle bên phải pivot cần thỏa right-side evidence
  price_basis: <wick | close>         # wick = dùng high/low; close = dùng giá đóng cửa
  equal_level_policy: <first_occurrence | last_occurrence>   # khi hai Candle có cùng extreme giá trị
```

**Left-side evidence:** `left_count` Candle liên tiếp ngay trước pivot, mỗi Candle có extreme (theo `price_basis`) **kém cực trị hơn** pivot theo đúng `direction` (HIGH: giá thấp hơn pivot; LOW: giá cao hơn pivot). Đây là điều kiện để phát `SwingCandidateDetected` (§3).

**Right-side evidence:** `right_count` Candle liên tiếp ngay sau pivot, cùng điều kiện đối xứng. Đây là điều kiện để phát `SwingConfirmed` (§4). **Right-side Candle chỉ được coi là evidence khi đã CLOSED authoritative (candle-closed hoặc candle-corrected đang authoritative) — không dùng CandleObserved provisional (§10).** Hệ quả trực tiếp của §7: pivot không thể "được biết" trước khi đủ right-side evidence đã tồn tại làm authoritative fact.

**Equal-high/equal-low tie:** khi một Candle trong evidence window có extreme **bằng** (không kém hơn, không vượt hơn) pivot, `equal_level_policy` quyết định: `first_occurrence` — Candle sớm hơn giữ vai trò pivot, Candle sau không phá candidate; `last_occurrence` — ngược lại. Không có nhánh thứ ba ngầm định.

**`price_basis` không mặc định là universal:** nhiều trường phái phân tích dùng wick (high/low) làm authority cho break/pivot, một số khác dùng close — Contract này khóa **cả hai đều hợp lệ**, chọn qua `swing_definition_version`, không áp một lựa chọn làm chuẩn bắt buộc toàn platform (controlling authority — Chapter 4/ADR hiện tại — không yêu cầu một phương pháp duy nhất).

**Cùng một pivot Candle có thể đồng thời là swing high VÀ swing low hợp lệ** (ví dụ inside/outside candle thỏa cả hai điều kiện độc lập) — vì `direction` là một phần của qualifying scope (§1), hai kết quả này có `swing_id` khác nhau và **cùng tồn tại**, không xung đột.

## 10. Correction handling — nhất quán identity, không silent mutation

Khi `CandleCorrected` (candle.md §5) thay đổi giá trị của một Candle nằm trong causal ancestry của một Swing (pivot HOẶC bất kỳ Candle nào trong `left_evidence_refs`/`right_evidence_refs`):

- **Nếu Candle bị sửa là pivot_candle_subject_id, và correction làm thay đổi `pivot_price` NHƯNG không thay đổi việc Candle đó vẫn là extreme hợp lệ theo `direction`:** phát `SwingInvalidated` (`invalidation_cause: upstream_correction`, causation trỏ fact cũ + `CandleCorrected`), sau đó phát lại `SwingCandidateDetected`/`SwingConfirmed` mới **trên CÙNG `swing_id`** (vì `pivot_candle_subject_id` — thành phần identity — không đổi qua correction, theo candle.md §1: `candle_subject_id` bất biến qua `CandleCorrected`) với `pivot_price` đã cập nhật, `causation_refs` trỏ `SwingInvalidated` vừa phát.
- **Nếu correction làm Candle đó KHÔNG còn thỏa điều kiện extreme (mất tư cách pivot):** phát `SwingInvalidated` (`upstream_correction`) — không phát fact thay thế trên `swing_id` này; nếu một Candle khác nay trở thành pivot hợp lệ, đó là một `swing_id` **khác** (vì `pivot_candle_subject_id` khác) — subject mới đi qua đúng lifecycle từ `UNSEEN` của chính nó.
- **Nếu Candle bị sửa nằm trong evidence window (không phải pivot) và correction làm mất/thêm tư cách evidence hợp lệ:** recompute; nếu candidate mất right-side evidence, phát `SwingInvalidated` trên fact hiện tại (cùng `swing_id`) rồi — nếu vẫn còn đủ evidence khác thỏa policy — phát lại fact mới cùng `swing_id`; nếu Candle mới đủ điều kiện làm evidence bổ sung mà trước đó chưa từng xét, xử lý như một confirmation mới trên `swing_id` hiện có (không tạo subject mới, vì pivot không đổi).

**Quy tắc identity đã chọn (nhất quán nội bộ):** *correction thay đổi giá trị nhưng KHÔNG thay đổi pivot_candle_subject_id → CÙNG `swing_id`, fact mới thay thế qua Invalidated→(Candidate/Confirmed) mới. Correction làm đổi Candle nào là pivot → `swing_id` KHÁC, vì `pivot_candle_subject_id` là thành phần identity (§1).* Không có nhánh thứ ba.

**Không silent mutation:** mọi fact cũ giữ nguyên trong log (I-3); `SwingInvalidated` luôn là fact tường minh, không bao giờ suy luận ngầm từ sự vắng mặt của recompute.

**Replay trước correction không thấy interpretation đã sửa:** đúng cơ chế `recorded_time` cursor đã mô tả ở §7 — `SwingInvalidated` và fact thay thế đều có `recorded_time` mới, replay tại cursor trước đó chỉ thấy fact gốc.

## 11. Missing data — không suy diễn từ im lặng

| Trường hợp | Xử lý |
|---|---|
| **Left-side evidence chưa đủ** (chưa đủ `left_count` Candle CLOSED) | Không phát `SwingCandidateDetected` — valid absence, KHÔNG phải missing-data condition. Không có sự kiện nào biểu diễn "chưa đủ trái". |
| **Data gap trong left-side window** (`CandleDataGapObserved` tồn tại cho một cửa sổ cần thiết) | Không phát `SwingCandidateDetected` cho tới khi gap được resolve bằng `CandleClosed` authoritative — **không suy diễn candidate từ dữ liệu thiếu**. |
| **Right-side evidence chưa đủ, sau khi đã CANDIDATE** | Subject giữ nguyên `CANDIDATE` — valid absence của `SwingConfirmed`, KHÔNG phải null hay lỗi. Không auto-invalidate chỉ vì chưa đủ thời gian trôi qua. |
| **Data gap trong right-side window, sau khi đã CANDIDATE** | Subject giữ nguyên `CANDIDATE` — KHÔNG confirm speculative qua gap, và KHÔNG tự động invalidate chỉ vì gap (gap không phải bằng chứng giá đã phá pivot — đó là câu hỏi khác, xem `market_evolution` ở §5). Confirm chỉ tiếp tục khi gap được resolve bằng `CandleClosed` authoritative cho đúng cửa sổ thiếu. |
| **Correction pending** (một `CandleCorrected` đã tồn tại trong log nhưng chưa visible tại cursor hiện tại) | Xử lý theo đúng cursor/`recorded_time` visibility — computation tại một cursor cụ thể chỉ dùng fact visible tại cursor đó (§7), không "chờ" correction chưa visible. |
| **Valid absence of Swing** (không có pivot nào thỏa điều kiện) | Không có event nào — kỳ vọng bình thường, không cần tín hiệu tường minh (khác Candle, nơi im lặng session-mở cần `CandleDataGapObserved` — ở đây "không có Swing" là kết luận hợp lệ của chính domain logic, không phải thiếu dữ liệu). |

## 12. Deduplication và ordering — computation identity thay cho source identity

Swing **không có external source retry/redelivery** (đây là fact được Ride tự tính, không phải quan sát venue) — nên `source_identity` (Chapter 6 §6.6) **không áp dụng** (§2). Thay vào đó, xác định identity chống trùng lặp qua **computation/causation identity**:

- **Same pivot discovered more than once** (ví dụ re-run sau restart, hoặc Live/Backtest/Replay tính độc lập trên cùng input): với cùng `swing_definition_version` và cùng tập Candle fact causal ancestry, computation **PHẢI** cho ra cùng `swing_id` (định danh deterministic, §1) và cùng payload — đây là điều kiện dedup: nếu một fact với `(subject_id, event_type, causation_refs-set, payload)` giống hệt đã tồn tại, **không** append bản ghi thứ hai; recomputation là **idempotent**, không phải nguồn tạo duplicate.
- **Out-of-order Candle correction:** Structure/Swing Engine không được xử lý một `CandleCorrected` trước khi `CandleClosed` (hoặc `CandleCorrected` trước) mà nó sửa đã được apply — đúng causal precedence bắt buộc của [Chapter 8 §8.3.4](../constitution/08-event-model.md) (`causation_ref` in-scope phải cursor-visible và apply trước effect).
- **Deterministic replay (mode parity):** với cùng `swing_definition_version` và cùng input Candle fact causal ancestry, Live/Backtest/Paper Trading/Replay **PHẢI** cho ra cùng tập Swing fact — nền tảng bắt buộc để downstream Decision (khi Swing/Structure trở thành decision-relevant) thỏa [I-2 Decision Parity](../constitution/02-platform-invariants.md). Swing/Structure tự thân không phải Decision, nhưng phải deterministic để không phá parity của bất kỳ Decision nào tiêu thụ chúng.
- **Duplicate detection request** (ví dụ hai lần trigger recompute cho cùng candidate mà chưa có gì đổi): không tạo `SwingCandidateDetected` thứ hai cho cùng `swing_id` khi một candidate chưa-invalidate đã tồn tại (§3 invariant).

## 13. Candle input contracts — chỉ authoritative facts

Swing tiêu thụ **chính xác hai** contract từ `market-data-observation`:

```text
candle-closed
candle-corrected
```

**Không tiêu thụ `CandleObserved` (provisional)** — Swing v0.1 chỉ dùng authoritative closed/corrected Candle fact, đúng preferred default: "confirmed market structure should use authoritative closed/corrected Candle facts unless a clear provisional Swing use case is modeled separately." Không có use case provisional-Swing nào được controlling authority yêu cầu ở Package 0.2-B1 — nếu cần sau này (ví dụ "live-forming swing hint" cho UI), đó là một concept riêng, ngoài phạm vi v0.1.

**Không tiêu thụ `CandleCurrentView`** — read model không authoritative (candle.md §7), không được dùng làm input cho bất kỳ authoritative computation nào.

## 14. Venue & timeframe neutrality

Cùng nguyên tắc [ADR-007](../adr/ADR-007.md)/`candle.md` §14: `instrument_id`/`venue_id`/`timeframe` là scope tường minh, không hardcode giả định venue cụ thể hay một timeframe "chuẩn". Hai Swing trên cùng instrument nhưng khác `venue_id` hoặc khác `timeframe` là hai subject **độc lập hoàn toàn**, không chia sẻ state.

## 15. Replay/Backtest/Paper/Live parity

Cả bốn execution mode tiêu thụ đúng cùng envelope (§2) và payload (§3–§5) — pattern nạp Candle có thể khác theo mode (đi qua `UNSEEN → CONFIRMED` trực tiếp cho historical, §1), nhưng domain semantic của Swing không đổi theo mode (§12).

## 16. Authority boundary

**Contract này sở hữu:** Swing pivot detection/confirmation/invalidation semantics, `SwingCurrentView` projection shape, `swing_definition_version` policy schema tối thiểu (§9). **Áp dụng, không định nghĩa lại:** event envelope ([Chapter 8 §8.2](../constitution/08-event-model.md)); ordering/replay cursor mechanics ([Chapter 5](../constitution/05-time-model.md)/[Chapter 8](../constitution/08-event-model.md)); ID opaque rule ([Chapter 6 §6.8](../constitution/06-identity-model.md)); Regime independence ([ADR-003](../adr/ADR-003.md) — Swing/Structure không tiêu thụ Regime). **Không sở hữu:** Candle observation semantics (`candle.md`); Instrument/Venue identity (`instrument-venue-reference`, chưa author); BOS/CHoCH/structure orientation semantics (`structure.md`); giá trị cụ thể của `swing_definition_version` policy (thuộc configuration/Phase 1, không phải Domain Contract).

## 17. Ngoài phạm vi — defer

Cơ chế tính `swing_id` deterministic cụ thể (content hash hay tương đương — chỉ khóa tính chất opaque + stable + deterministic từ đúng sáu field scope, không khóa thuật toán); giá trị cụ thể mặc định cho `left_count`/`right_count`/`price_basis`/`equal_level_policy` (thuộc configuration instance, không phải Domain Contract — xem §9); storage/schema/serialization; cơ chế lưu trữ/versioning cụ thể của `swing_definition_version` registry (Phase 1); "live-forming swing hint" từ `CandleObserved` provisional (§13, chưa có use case được authorize).

## 18. Open questions ngoài phạm vi

- Liệu Swing v0.1 cần một `SwingCandidateDetected` riêng biệt cho mọi Swing Definition, hay một số definition (ví dụ definition chỉ dùng cho historical batch) có thể hợp lệ **bỏ qua hoàn toàn** CANDIDATE (luôn đi `UNSEEN → CONFIRMED` ngay cả trong Live, không chỉ historical) — không quyết ở đây; §1 hiện chỉ cho phép đường tắt này cho historical ingestion, chưa mở rộng cho Live. Không đóng OQ-002/OQ-003 nào, đây không phải governance-level OQ mà là author-level ambiguity note.
- `swing_definition_version` registry/lifecycle (nơi pin `left_count`/`right_count`/`price_basis`/`equal_level_policy` cụ thể) chưa có authoritative source riêng — tạm coi là Referenced Authoritative Artifact theo Chapter 8 §8.1.1 (§9), nhưng **chưa** có file/registry cụ thể nào author nó trong Package 0.2-B1. Cần quyết định khi Package 0.2-B/0.2-C có nhu cầu thực tế đầu tiên: một file cấu hình riêng, hay một phần của Strategy/Decision configuration.
