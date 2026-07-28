---
id: structure
title: Market Structure
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

# Market Structure

> **Vai trò của tài liệu này:** Domain Contract thứ hai của Package 0.2-B1 — hoàn thiện chuỗi `Candle → Swing → Structure`. Draft, chưa qua review nào (author self-review only), chưa Approved/Locked. Thuộc capability `market-structure` / context `market-structure-analysis` (đã đăng ký tại [`context-map.yaml`](./context-map.yaml)), **cùng context với `swing.md`** — Swing → Structure là quan hệ intra-context, không phải cross-context edge (§9).

Market Structure bao gồm **bốn concept riêng biệt**:

1. **Logical Structure Subject** (`kind: entity`) — identity ổn định của "structure interpretation này", **một subject liên tục theo scope** (khác Swing/Candle — không có subject mới per pivot/window; xem §1).
2. **`BreakOfStructureDetected`** (`kind: event`) — orientation tiếp diễn hoặc được thiết lập lần đầu.
3. **`ChangeOfCharacterDetected`** (`kind: event`) — orientation đảo chiều.
4. **`StructureInvalidated`** (`kind: event`) — fact mới phủ định một BOS/CHoCH trước đó, do correction cascade.

Cộng một **read model tùy chọn** (`StructureCurrentView`) — projection tiện dụng, không authoritative.

**Không gộp Swing, BOS, CHoCH, và trend state vào một object mutable mơ hồ.** Mỗi orientation transition là một event append-only riêng biệt (I-3); orientation "hiện tại" chỉ tồn tại như derived state rebuild được từ chuỗi event, không phải trường dữ liệu ghi đè tại chỗ.

**`break-of-structure-detected` / `change-of-character-detected` / `structure-invalidated` / `structure-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây, và đúng giá trị `contract_id` mà [`context-map.yaml`](./context-map.yaml) sẽ trích dẫn (khi có edge cross-context — §9). Display name, concept ID, và `event_type` là ba đại lượng khác nhau, không cạnh tranh identity — cùng nguyên tắc `candle.md`/`swing.md` đã khóa.

## 1. Logical Structure Subject — `kind: entity`

```yaml
id: structure
kind: entity
capability_id: market-structure
domain_context_id: market-structure-analysis
description: >
  Trạng thái orientation authoritative "hiện tại" của market structure, cho một
  instrument/venue/timeframe, theo một Structure Definition Version cụ thể. KHÁC pattern
  Candle (subject per window) và Swing (subject per pivot): Structure có ĐÚNG MỘT subject
  liên tục cho mỗi qualifying scope — subject này KHÔNG bao giờ "kết thúc" và một subject mới
  bắt đầu; nó tiến hóa qua toàn bộ vòng đời của scope đó qua chuỗi BreakOfStructureDetected /
  ChangeOfCharacterDetected / StructureInvalidated. Đây là quyết định thiết kế tường minh: một
  "current interpretation" chỉ có ý nghĩa khi nó là MỘT state machine instance duy nhất theo
  thời gian, không phải nhiều instance rời rạc.
invariants:
  - "structure_subject_id resolve deterministic từ ĐÚNG BỐN field qualifying scope: instrument_id, venue_id, timeframe, structure_definition_version — cùng bốn-field-scope luôn cho cùng structure_subject_id; khác bất kỳ field nào cho structure_subject_id KHÁC. structure_subject_id bất biến, KHÔNG tái sử dụng cho một subject khác (Chapter 6 §6.1)."
  - "structure_subject_id là opaque — domain logic KHÔNG được parse nó (Chapter 6 §6.8); mọi quyết định nghiệp vụ phải dùng field tường minh trong scope."
  - "instrument_id, venue_id, timeframe, structure_definition_version bất biến sau khi subject được quan sát lần đầu — đổi bất kỳ field nào tạo ra một subject KHÁC, không phải mutate subject cũ. Đổi swing_definition_version mà structure_definition_version phụ thuộc (§9) BẮT BUỘC bump chính structure_definition_version — không cho phép một structure_subject_id âm thầm đổi ý nghĩa vì dependency đổi mà version của chính nó không đổi."
  - "current_orientation KHÔNG phải một field độc lập ghi đè tại chỗ — nó là derived state, rebuild được bằng cách apply tuần tự mọi BreakOfStructureDetected/ChangeOfCharacterDetected/StructureInvalidated của subject theo recorded_time (§8 no-repaint)."
  - "current structural leg (Swing pivot nào đang là 'level' liên quan) KHÔNG thuộc identity scope — đây là derived/current-state fact, thay đổi sau mỗi event; chỉ bốn field ở trên xác định identity bất biến của subject."
schema:
  structure_subject_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  instrument_id: {type: string, required: true, ref: instrument}
  venue_id: {type: string, required: true, ref: venue}
  timeframe: {type: string, required: true}
  structure_definition_version: {type: string, required: true, description: "pin chính xác Structure Definition policy đã dùng — §9, bao gồm reference tới swing_definition_version phụ thuộc"}
state_machine:
  initial_state: UNDETERMINED
  states: [UNDETERMINED, NEUTRAL, BULLISH, BEARISH]
  transitions:
    - {from: UNDETERMINED, to: BULLISH, caused_by: BreakOfStructureDetected}
    - {from: UNDETERMINED, to: BEARISH, caused_by: BreakOfStructureDetected}
    - {from: NEUTRAL, to: BULLISH, caused_by: BreakOfStructureDetected}
    - {from: NEUTRAL, to: BEARISH, caused_by: BreakOfStructureDetected}
    - {from: BULLISH, to: BULLISH, caused_by: BreakOfStructureDetected}
    - {from: BEARISH, to: BEARISH, caused_by: BreakOfStructureDetected}
    - {from: BULLISH, to: BEARISH, caused_by: ChangeOfCharacterDetected}
    - {from: BEARISH, to: BULLISH, caused_by: ChangeOfCharacterDetected}
    - {from: BULLISH, to: NEUTRAL, caused_by: StructureInvalidated}
    - {from: BEARISH, to: NEUTRAL, caused_by: StructureInvalidated}
  terminal_states: []
events_emitted: [BreakOfStructureDetected, ChangeOfCharacterDetected, StructureInvalidated]
events_consumed: [SwingConfirmed, SwingInvalidated, CandleClosed, CandleCorrected]
commands: []
queries: []
```

**`UNDETERMINED` là notional initial state** — cùng convention `UNSEEN` mà `candle.md`/`swing.md` đã khóa: không event nào khẳng định "subject đang UNDETERMINED"; đây là điểm khởi đầu ngầm định trước khi có Swing nào đủ để xác định orientation.

**`NEUTRAL` KHÁC `UNDETERMINED`** — `NEUTRAL` là một giá trị **authoritative**, chỉ đạt được qua `StructureInvalidated` (§5): "orientation trước đó không còn hợp lệ, và chưa có orientation mới thay thế ngay." `UNDETERMINED` không bao giờ được tái khẳng định bằng event — một khi subject đã rời `UNDETERMINED`, nó không quay lại đó; trạng thái "không có orientation rõ ràng" sau này luôn là `NEUTRAL` (một fact tường minh), không phải `UNDETERMINED` (một non-fact).

**Không có transition nào rời khỏi `NEUTRAL` qua `ChangeOfCharacterDetected`** — CHoCH theo định nghĩa yêu cầu một **prior orientation trực tiếp (`BULLISH`/`BEARISH`)** để "đảo chiều" (§7); từ `NEUTRAL`, việc thiết lập orientation mới dùng đúng cơ chế `BreakOfStructureDetected` như từ `UNDETERMINED` (§6 — cùng executable criterion, không phân biệt).

## 2. Canonical event envelope — áp dụng cho mọi Structure event (§3–§5)

Mọi event ở §3–§5 là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). Mục này khóa **envelope chung** một lần.

```yaml
envelope:
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2) — xem bảng dưới
  event_contract_ref: {cardinality: required}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}             # khi Ride tính/ghi nhận fact này
  subject_ref: {cardinality: required}
  stream_ref: {cardinality: required}                # Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # Phase 1, chưa author
  correlation_id: {cardinality: "required khi computation thuộc một correlation flow tường minh; optional khi độc lập"}
  causation_refs: {cardinality: "KHÔNG BAO GIỜ rỗng — mọi Structure event là derived fact từ Swing fact và/hoặc Candle fact. Xem §3–§5 cho nội dung cụ thể."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3"}
  effective_time: {cardinality: "required — = effective_time của Candle cung cấp bằng chứng break/invalidation (§7), KHÔNG phải recorded_time."}
  market_time: {cardinality: "PROHIBITED — Structure là derived/computed fact, không phải quan sát trực tiếp venue."}
  source_identity: {cardinality: "PROHIBITED — không có external source retry/redelivery risk; dedup dùng computation identity, §12."}

subject_ref:
  context_id: market-structure-analysis
  subject_kind: entity
  subject_type: Structure
  subject_id: <structure_subject_id — opaque, stable, xem §1>
  scope:
    instrument_id: <string>
    venue_id: <string>
    timeframe: <string>
    structure_definition_version: <string>

event_types:
  BreakOfStructureDetected: BREAK_OF_STRUCTURE_DETECTED
  ChangeOfCharacterDetected: CHANGE_OF_CHARACTER_DETECTED
  StructureInvalidated: STRUCTURE_INVALIDATED
```

`stream_ref`/`producer_ref` — Phase 1, chưa tồn tại, cùng nguyên tắc defer đã áp dụng ở `candle.md`/`swing.md`.

**`StructureStateChanged` KHÔNG được introduce** — mọi orientation transition (kể cả thiết lập lần đầu từ `UNDETERMINED`/`NEUTRAL`) đã biểu diễn đầy đủ qua ba event đã khai (§6–§8); một event tổng hợp thêm sẽ tạo hai nguồn authority cạnh tranh cho cùng một orientation change (I-12).

## 3. `BreakOfStructureDetected` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: break-of-structure-detected
kind: event
capability_id: market-structure
domain_context_id: market-structure-analysis
description: >
  Giá phá qua một Swing level cụ thể theo hướng phù hợp để tiếp diễn HOẶC thiết lập lần đầu
  một orientation (BULLISH hoặc BEARISH) — KHÔNG BAO GIỜ tạo ra NEUTRAL (§1). `prior_orientation`
  có thể là UNDETERMINED, NEUTRAL, BULLISH, hoặc BEARISH; `new_orientation` luôn BULLISH hoặc
  BEARISH. Executable criterion giống hệt dù prior_orientation là gì (§6) — chỉ interpretation
  (thiết lập lần đầu vs tiếp diễn) khác nhau, đó là lý do không cần một event riêng cho "lần
  đầu thiết lập" (§2).
invariants:
  - "broken_swing_ref PHẢI trỏ một Swing fact CONFIRMED (swing-confirmed), chưa từng là broken_swing_ref của một BreakOfStructureDetected/ChangeOfCharacterDetected trước đó CHƯA bị StructureInvalidated — cấm cùng một Swing level được báo 'phá' hai lần độc lập (§11 same-level-broken-twice)."
  - "broken_swing_ref.direction PHẢI khớp bảng quyết định ở §6 theo new_orientation."
  - "causation_refs PHẢI chứa: SwingConfirmed của broken_swing_ref; VÀ breaking_candle_refs (một hoặc nhiều candle-closed/candle-corrected) cung cấp bằng chứng break theo break_price_basis đã pin (§9)."
  - "envelope.effective_time = effective_time của Candle cuối cùng trong breaking_candle_refs (§7)."
  - "new_orientation != prior_orientation KHI prior_orientation là BULLISH hoặc BEARISH và new_orientation khác — TRƯỜNG HỢP ĐÓ KHÔNG HỢP LỆ trên event này (đó là ChangeOfCharacterDetected, §4), không phải BreakOfStructureDetected."
payload:
  prior_orientation: {type: enum, values: [UNDETERMINED, NEUTRAL, BULLISH, BEARISH], required: true}
  new_orientation: {type: enum, values: [BULLISH, BEARISH], required: true}
  broken_swing_ref: {type: object, required: true, description: "{swing_id, direction} — Swing level bị phá, xem §6"}
  breaking_candle_refs: {type: array, items: event_record_ref, required: true}
```

## 4. `ChangeOfCharacterDetected` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: change-of-character-detected
kind: event
capability_id: market-structure
domain_context_id: market-structure-analysis
description: >
  Giá phá qua một Swing level đối lập, đảo chiều orientation authoritative đang có
  (BULLISH → BEARISH hoặc BEARISH → BULLISH). PHẢI có prior_orientation trực tiếp là BULLISH
  hoặc BEARISH — CHoCH KHÔNG hợp lệ từ UNDETERMINED hay NEUTRAL (§1, §6 — trường hợp đó dùng
  BreakOfStructureDetected). CHoCH thay đổi authoritative structure state NGAY LẬP TỨC — KHÔNG
  tạo một 'candidate transition' chờ xác nhận riêng (quyết định thiết kế, §7): Swing level bị
  phá đã tự thân là fact CONFIRMED (swing-confirmed), và Candle phá level đó đã là fact
  authoritative (candle-closed/candle-corrected) — không còn 'điều kiện chưa chắc chắn' nào
  cần thêm một vòng candidate riêng ở tầng Structure.
invariants:
  - "prior_orientation PHẢI là BULLISH hoặc BEARISH — không hợp lệ trên UNDETERMINED/NEUTRAL."
  - "new_orientation PHẢI là orientation đối lập chính xác với prior_orientation (BULLISH↔BEARISH) — không có giá trị thứ ba."
  - "broken_swing_ref.direction PHẢI khớp bảng quyết định ở §7 (đối lập với direction mà một continuation BOS cùng prior_orientation sẽ dùng)."
  - "broken_swing_ref PHẢI trỏ một Swing fact CONFIRMED, chưa từng là broken_swing_ref của một event trước đó chưa bị invalidate."
  - "causation_refs PHẢI chứa: SwingConfirmed của broken_swing_ref; VÀ breaking_candle_refs cung cấp bằng chứng break."
  - "envelope.effective_time = effective_time của Candle cuối cùng trong breaking_candle_refs."
payload:
  prior_orientation: {type: enum, values: [BULLISH, BEARISH], required: true}
  new_orientation: {type: enum, values: [BULLISH, BEARISH], required: true}
  broken_swing_ref: {type: object, required: true, description: "{swing_id, direction} — xem §7"}
  breaking_candle_refs: {type: array, items: event_record_ref, required: true}
```

## 5. `StructureInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2 — `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: structure-invalidated
kind: event
capability_id: market-structure
domain_context_id: market-structure-analysis
description: >
  Phủ định một BreakOfStructureDetected hoặc ChangeOfCharacterDetected trước đó của cùng
  structure_subject_id, do correction cascade — KHÔNG BAO GIỜ do "giá tiếp tục di chuyển"
  (đó là một BOS/CHoCH mới, không phải invalidation của fact cũ — §8 no-repaint). BA nguyên
  nhân, khai báo tường minh qua payload.invalidation_cause:
  (a) swing_invalidated — broken_swing_ref của fact đang bị invalidate đã nhận SwingInvalidated
      (upstream_correction, swing.md §5) — level dùng làm căn cứ break không còn hợp lệ;
  (b) breaking_candle_corrected — một Candle trong breaking_candle_refs bị CandleCorrected
      khiến nó không còn thỏa break criterion (§9) theo payload đã sửa;
  (c) chained_invalidation — fact này KHÔNG bị ảnh hưởng trực tiếp bởi (a)/(b), nhưng
      `payload.prior_orientation` của nó trỏ tới `new_orientation` của một event SỚM HƠN cùng
      subject vừa bị invalidate (qua (a) hoặc (b), hoặc qua chính (c) một cách bắc cầu) — chuỗi
      orientation không còn nhất quán nếu fact này vẫn đứng yên (§10, đóng attack scenario
      "correction cascade invalidates multiple downstream facts").
  Là event MỚI, KHÔNG mutate record gốc (I-3). Orientation sau invalidation luôn chuyển về
  NEUTRAL (§1) tại chính event này; nếu recompute cho ra orientation mới ngay, một
  BreakOfStructureDetected/ChangeOfCharacterDetected MỚI được phát riêng, causation trỏ đúng
  StructureInvalidated này (đối xứng swing.md §10).
invariants:
  - "causation_refs PHẢI trỏ: (a)/(b) — event đang bị invalidate + SwingInvalidated hoặc CandleCorrected là nguyên nhân trực tiếp; (c) — event đang bị invalidate + StructureInvalidated của event sớm hơn gây ra chain break."
  - "invalidation_cause = swing_invalidated CHỈ hợp lệ khi broken_swing_ref của fact bị invalidate khớp đúng subject của SwingInvalidated được trỏ tới."
  - "invalidation_cause = breaking_candle_corrected CHỈ hợp lệ khi Candle bị sửa nằm trong breaking_candle_refs của fact bị invalidate VÀ payload đã sửa không còn thỏa break criterion (§9)."
  - "invalidation_cause = chained_invalidation CHỈ hợp lệ khi payload.prior_orientation của fact bị invalidate bằng đúng new_orientation của event vừa nhận StructureInvalidated (qua bất kỳ nguyên nhân nào) ngay trước nó theo recorded_time trên cùng subject — không dùng cause này khi fact bị invalidate là nguyên nhân trực tiếp (a)/(b) của chính nó."
  - "Xử lý cascade PHẢI theo thứ tự most-recent-first: mọi BreakOfStructureDetected/ChangeOfCharacterDetected phát sinh SAU event bị invalidate trực tiếp (a)/(b), theo cùng subject, PHẢI nhận StructureInvalidated (chained_invalidation) trước khi hệ thống được coi là nhất quán trở lại — không được để một fact còn hiệu lực trỏ prior_orientation tới một orientation đã bị phủ định (§10)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của event gây invalidation."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này."
payload:
  invalidation_cause: {type: enum, values: [swing_invalidated, breaking_candle_corrected, chained_invalidation], required: true}
  invalidation_reason: {type: string, required: false}
```

## 6. BOS semantics — executable criterion

**Broken level (bảng quyết định):**

| `prior_orientation` | `new_orientation` | `broken_swing_ref.direction` |
|---|---|---|
| `UNDETERMINED` / `NEUTRAL` | `BULLISH` | `HIGH` |
| `UNDETERMINED` / `NEUTRAL` | `BEARISH` | `LOW` |
| `BULLISH` | `BULLISH` (continuation) | `HIGH` |
| `BEARISH` | `BEARISH` (continuation) | `LOW` |

**`broken_swing_ref` PHẢI là Swing hiện đang "structurally relevant"** — Swing CONFIRMED gần nhất, đúng `direction` theo bảng trên, **chưa từng bị dùng làm `broken_swing_ref`** của một event trước đó còn hiệu lực (§3 invariant). Điều này ngăn "same level broken twice": một khi một Swing đã là `broken_swing_ref`, nó không đủ điều kiện làm căn cứ cho một BOS/CHoCH thứ hai — Swing kế tiếp thỏa điều kiện (được Swing Engine confirm sau đó) mới trở thành level liên quan tiếp theo.

**Break criterion (price basis + comparison):** pin qua `structure_definition_version.break_price_basis` (`wick` hoặc `close`, §9) và `comparison_policy` (`strict` hoặc `inclusive`, §9) — **không hardcode một trường phái**:

```text
wick + strict:      candle.high > broken_swing.pivot_price   (HIGH break)  |  candle.low < broken_swing.pivot_price   (LOW break)
wick + inclusive:    candle.high ≥ broken_swing.pivot_price   (HIGH break)  |  candle.low ≤ broken_swing.pivot_price   (LOW break)
close + strict:      candle.close > broken_swing.pivot_price  (HIGH break)  |  candle.close < broken_swing.pivot_price  (LOW break)
close + inclusive:   candle.close ≥ broken_swing.pivot_price  (HIGH break)  |  candle.close ≤ broken_swing.pivot_price  (LOW break)
```

**Equal-high/equal-low touch (giá chạm đúng level, không vượt):** chỉ coi là break khi `comparison_policy: inclusive`; với `strict`, một touch không phá — Structure giữ nguyên orientation, không phát event nào (valid absence, §11).

**Wick crosses nhưng close không (hoặc ngược lại):** hoàn toàn phụ thuộc `break_price_basis` đã pin — nếu pin `close`, một wick vượt qua level nhưng close không vượt **KHÔNG** cấu thành break; contract không tự ý dùng basis còn lại làm fallback.

**Required confirmation:** break chỉ hợp lệ dựa trên Candle **authoritative** (`candle-closed`/`candle-corrected`) — không dùng `CandleObserved` provisional, đối xứng `swing.md` §13.

**Effective time của break:** = `effective_time` của Candle cuối cùng trong `breaking_candle_refs` (§2) — **recorded_time** mới là lúc Ride biết fact này, tách bạch đúng nguyên tắc T vs T+n mà `swing.md` §7 đã khóa.

**Duplicate detection / same level broken multiple times:** xem §11.

## 7. CHoCH semantics — đảo chiều, thay đổi ngay lập tức

**Yêu cầu prior orientation:** PHẢI là `BULLISH` hoặc `BEARISH` trực tiếp (§4 invariant) — không có CHoCH "từ neutral".

**Broken level (đối lập continuation BOS):**

| `prior_orientation` | `new_orientation` | `broken_swing_ref.direction` |
|---|---|---|
| `BULLISH` | `BEARISH` | `LOW` |
| `BEARISH` | `BULLISH` | `HIGH` |

Đây chính là điểm khác biệt cấu trúc với continuation BOS: một continuation `BULLISH → BULLISH` phá một `HIGH` swing (tiếp diễn theo hướng đã có); một CHoCH `BULLISH → BEARISH` phá một `LOW` swing (level đối lập, cấu thành uptrend hiện tại) — không phải cùng loại level.

**CHoCH thay đổi authoritative structure state NGAY LẬP TỨC, không qua candidate:** cả `broken_swing_ref` (đã CONFIRMED) lẫn `breaking_candle_refs` (đã authoritative) là fact chắc chắn tại thời điểm event phát sinh — không có "điều kiện chưa chắc chắn" nào để biện minh cho một trạng thái candidate riêng ở tầng Structure. (So sánh: Swing CẦN candidate vì nó phải chờ right-side evidence tích lũy theo thời gian — §9 `swing.md`. CHoCH không có độ trễ tương tự: ngay khi Swing level đã CONFIRMED và Candle phá nó đã CLOSED, break là fact tức thời, không cần chờ thêm.)

**Break criterion:** dùng cùng `break_price_basis`/`comparison_policy` như BOS (§6, §9) — một policy duy nhất áp cho cả hai event type trong cùng `structure_definition_version`.

## 8. No repaint

- **`BreakOfStructureDetected`/`ChangeOfCharacterDetected` KHÔNG BAO GIỜ bị ghi đè tại chỗ** — một khi phát sinh, chỉ có thể bị phủ định qua `StructureInvalidated` với nguyên nhân tường minh (§5), KHÔNG BAO GIỜ vì "giá tiếp tục di chuyển theo hướng khác" — đó luôn là một BOS/CHoCH **mới**, không phải invalidation của fact cũ.
- **Replay tại cursor T chỉ thấy fact có `recorded_time ≤ T`** — một BOS với `effective_time` sớm nhưng `recorded_time` muộn (do chờ breaking Candle CLOSED) không "xuất hiện sớm hơn" khi replay lùi lại, đúng cơ chế `swing.md` §7 đã khóa.
- **Không có BOS/CHoCH lịch sử nào được backfill như thể đã biết sớm hơn thực tế** — hệ quả trực tiếp của §6/§7 (break luôn dùng Candle CLOSED authoritative, `effective_time` = Candle đó, `recorded_time` = khi thực sự tính).

## 9. Configuration evidence — pinned, không hardcode

```yaml
structure_definition:                  # schema tối thiểu — KHÔNG khóa giá trị cụ thể
  structure_definition_version: <string>    # opaque, immutable pin — Referenced Authoritative Artifact (Chapter 8 §8.1.1)
  depends_on_swing_definition_version: <string>   # PHẢI trỏ đúng swing_definition_version (swing.md §9) mà mọi broken_swing_ref dùng
  break_price_basis: <wick | close>
  comparison_policy: <strict | inclusive>
  equal_level_policy: <first_occurrence | last_occurrence>   # kế thừa/áp dụng nhất quán với swing_definition (swing.md §9) khi cả hai cùng liên quan một level
```

**`depends_on_swing_definition_version` bắt buộc** — Structure không tự định nghĩa lại policy nhận diện Swing; nó chỉ tiêu thụ Swing fact đã CONFIRMED theo policy Swing đã pin sẵn (§1 invariant: đổi dependency bắt buộc bump `structure_definition_version`).

**Không chọn một trường phái làm chuẩn phổ quát duy nhất** — `wick` vs `close`, `strict` vs `inclusive` đều hợp lệ, chọn qua `structure_definition_version`, đúng yêu cầu tách "Structure semantic contract" khỏi "specific strategy/configuration policy."

## 10. Correction cascade

```text
CandleCorrected
  → (a) nếu Candle là pivot/evidence của một Swing  → SwingInvalidated (swing.md §10) → StructureInvalidated (invalidation_cause: swing_invalidated) cho mọi BOS/CHoCH có broken_swing_ref trỏ Swing đó
  → (b) nếu Candle là breaking_candle_refs của một BOS/CHoCH mà KHÔNG qua Swing nào bị invalidate → StructureInvalidated (invalidation_cause: breaking_candle_corrected) trực tiếp
```

Cả hai nhánh **đều** trigger recomputation — đây là lý do Structure tiêu thụ **trực tiếp** `candle-closed`/`candle-corrected` (§ Inputs) thay vì chỉ dựa vào `swing-invalidated`: nhánh (b) không đi qua Swing nào cả (breaking Candle có thể nằm ngoài evidence window của bất kỳ Swing nào — nó chỉ là Candle xác nhận break, không phải Candle cấu thành pivot).

**Chained invalidation — phủ định nhiều downstream fact, không chỉ fact bị ảnh hưởng trực tiếp (§5, `invalidation_cause: chained_invalidation`):** vì mỗi `BreakOfStructureDetected`/`ChangeOfCharacterDetected` mang `prior_orientation` tham chiếu **kết quả** của event ngay trước nó trên cùng subject (§6, §7), invalidate MỘT event ở giữa chuỗi (qua (a) hoặc (b)) làm mọi event **sau đó** trên subject này rơi vào tình trạng `prior_orientation` trỏ tới một `new_orientation` đã bị phủ định — không còn nhất quán nếu để yên. Ví dụ cụ thể:

```text
t1: BreakOfStructureDetected   prior=UNDETERMINED  new=BULLISH   (broken_swing_ref = Swing A)
t2: ChangeOfCharacterDetected  prior=BULLISH        new=BEARISH   (broken_swing_ref = Swing B)
t3: ChangeOfCharacterDetected  prior=BEARISH        new=BULLISH   (broken_swing_ref = Swing C)

→ SwingInvalidated(Swing A) đến (upstream_correction)
→ StructureInvalidated(t1, cause: swing_invalidated)              — trực tiếp, (a)
→ StructureInvalidated(t2, cause: chained_invalidation)            — t2.prior_orientation (BULLISH) = t1.new_orientation vừa bị phủ định
→ StructureInvalidated(t3, cause: chained_invalidation)            — t3.prior_orientation (BEARISH) = t2.new_orientation vừa bị phủ định (bắc cầu)
→ orientation hiện tại của subject: NEUTRAL, chờ recompute
```

Thứ tự phát sinh **most-recent-first PHẢI được tôn trọng cho mục đích xác định chuỗi** (xác định t3 phụ thuộc t2 phụ thuộc t1), nhưng **các `StructureInvalidated` này là fact độc lập, mỗi fact có `recorded_time` riêng** — không có yêu cầu chúng phải cùng một event; hệ thống chỉ đảm bảo không state nào còn "treo" với `prior_orientation` trỏ về một orientation đã bị phủ định. Sau khi cascade hoàn tất, orientation quay về `NEUTRAL`; nếu recompute (dựa trên Swing/Candle fact hiện hành) cho ra một chuỗi orientation mới, các `BreakOfStructureDetected`/`ChangeOfCharacterDetected` mới được phát riêng, causation trỏ đúng `StructureInvalidated` gần nhất trong chuỗi.

**Deduplicate cascade:** nếu cả một `SwingInvalidated` VÀ một `CandleCorrected` trực tiếp cùng ảnh hưởng một `BreakOfStructureDetected` (trường hợp hiếm — cùng một correction gốc lan tới cả hai đường), chỉ phát **một** `StructureInvalidated` cho fact đó — `causation_refs` liệt kê đủ cả hai nguyên nhân dưới dạng nhiều phần tử, `invalidation_cause` chọn nguyên nhân **trực tiếp nhất tại chính broken_swing_ref/breaking_candle_refs của fact đang bị invalidate** (không phát hai StructureInvalidated trùng lặp cho cùng subject/event — vi phạm §3-style duplicate rule tương tự swing.md §12).

**Structure phải trace mọi output về đúng input:** `causation_refs` của mọi BOS/CHoCH/Invalidated luôn resolve ngược được về Swing fact + Candle fact gốc (I-1 Explainability).

**Preserve prior outputs:** không event nào bị xóa; `StructureInvalidated` là fact bổ sung, không phải xóa fact cũ (I-3).

**Replay visibility theo `recorded_time`:** đối xứng §8.

## 11. Deduplication và ordering

Đối xứng `swing.md` §12, áp dụng lại nguyên tắc **không copy mù các rule đặc thù của Candle**:

- **Computation identity thay `source_identity`:** Structure là fact tự tính, không có external retry/redelivery — dedup dựa trên `(subject_id, event_type, causation_refs-set, payload)` giống hệt; recompute trên input không đổi phải idempotent, không tạo bản ghi thứ hai.
- **Same level broken multiple times:** ngăn ở nguồn bằng invariant §3/§4 (`broken_swing_ref` chưa từng dùng, còn hiệu lực) — không dựa vào dedup hậu kiểm.
- **Out-of-order Candle correction / Swing invalidation:** phải tôn trọng causal precedence [Chapter 8 §8.3.4](../constitution/08-event-model.md) — không xử lý `SwingInvalidated`/`CandleCorrected` trước khi fact mà nó sửa đã được apply.
- **Deterministic replay (mode parity):** cùng `structure_definition_version` + cùng input Swing/Candle causal ancestry → cùng tập Structure fact, mọi execution mode ([I-2](../constitution/02-platform-invariants.md) khi downstream Decision tiêu thụ Structure).

## 12. Inputs — contract chính xác

Structure tiêu thụ **cả hai loại** fact — không chỉ Swing:

```text
swing-confirmed
swing-invalidated
candle-closed
candle-corrected
```

**Swing input là bắt buộc** — mọi `broken_swing_ref` phải trỏ một `swing-confirmed` fact (§3, §4); `swing-invalidated` là trigger bắt buộc của correction cascade nhánh (a) (§10).

**Direct Candle input là bắt buộc, có justification tường minh** — break confirmation (§6) cần Candle fact **sau** pivot (breaking candle), điều mà Swing Domain Contract **không** theo dõi (Swing chỉ theo dõi Candle trong evidence window của chính nó, kết thúc khi `SwingConfirmed` phát sinh — `swing.md` §9). Structure phải tự tiêu thụ `candle-closed`/`candle-corrected` để: (a) xác định breaking candle cho BOS/CHoCH; (b) nhận diện correction cascade nhánh (b) khi breaking candle (không phải Swing evidence) bị sửa (§10). Không có cách nào thỏa cả hai yêu cầu này chỉ từ Swing fact.

**Không tiêu thụ `CandleObserved`/`CandleCurrentView`/`SwingCandidateDetected`/`SwingCurrentView`** — chỉ dùng fact authoritative, đối xứng nguyên tắc `swing.md` §13.

**Không tiêu thụ Regime** — [ADR-003](../adr/ADR-003.md) khóa Structure độc lập hoàn toàn với Raw Regime; Domain Contract này không khai báo bất kỳ `events_consumed` nào thuộc `raw-regime-analysis`.

## 13. Structure scope — không global state

`structure_subject_id` scope theo đúng bốn field ở §1 — không có structure state toàn cục xuyên venue/timeframe. Hai Structure trên cùng instrument nhưng khác `venue_id` hoặc `timeframe` là hai subject **độc lập hoàn toàn** (đối xứng `swing.md` §14).

## 14. `StructureCurrentView` — `kind: read_model` (optional)

**Không phải authoritative event** (Chapter 7 §7.4 Type 2 Projection). Rebuild được từ §3–§5.

```yaml
id: structure-current-view
kind: read_model
capability_id: market-structure
domain_context_id: market-structure-analysis
description: >
  Projection tiện dụng: orientation "hiện tại" và structural leg liên quan của một Structure
  subject, rebuild được từ BreakOfStructureDetected/ChangeOfCharacterDetected/StructureInvalidated.
  KHÔNG authoritative — mọi audit/replay/parity, và mọi input cho concept khác (kể cả Feature,
  khi được author), phải dùng authoritative event stream, KHÔNG dùng view này làm nguồn sự
  thật (I-12, Chapter 7 §7.4). Cursor-bounded — không có "current" ngoài một cursor cụ thể khi
  dùng cho bất kỳ mục đích decision-relevant.
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream cùng structure_definition_version đã pin, cùng implementation version (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho bất kỳ Decision hay Domain Contract khác — chỉ query/UI (Chapter 7 §7.4)."
  - "Không có view row nào tồn tại khi subject còn UNDETERMINED (§1) — kỳ vọng bình thường, KHÔNG phải missing-data condition."
schema:
  structure_subject_id: {type: string, required: true}
  scope: {instrument_id: string, venue_id: string, timeframe: string, structure_definition_version: string, required: true}
  current_orientation: {type: enum, values: [UNDETERMINED, NEUTRAL, BULLISH, BEARISH], required: true}
  current_relevant_swing_ref: {type: object, description: "Swing level hiện đang chờ bị phá tiếp theo, nếu xác định được — derived, không authoritative"}
  last_recorded_time: timestamp
queries: [GetCurrentStructure, GetStructureHistory]
```

## 15. Authority boundary

**Contract này sở hữu:** BOS/CHoCH/invalidation semantics, structure orientation state machine, `StructureCurrentView` projection shape, `structure_definition_version` policy schema tối thiểu (§9). **Áp dụng, không định nghĩa lại:** event envelope ([Chapter 8 §8.2](../constitution/08-event-model.md)); ordering/replay cursor mechanics ([Chapter 5](../constitution/05-time-model.md)/[Chapter 8](../constitution/08-event-model.md)); ID opaque rule ([Chapter 6 §6.8](../constitution/06-identity-model.md)); Swing pivot/confirmation semantics (`swing.md`); Regime independence ([ADR-003](../adr/ADR-003.md)). **Không sở hữu:** giá trị cụ thể của `structure_definition_version` policy (configuration/Phase 1); Feature fan-in logic (Package 0.2-B, chưa author — Structure chỉ publish, không định nghĩa consumer); service boundary/module layout/deployment (Engineering/Phase 1).

## 16. Ngoài phạm vi — defer

Cơ chế tính `structure_subject_id` deterministic cụ thể; giá trị cụ thể mặc định cho `break_price_basis`/`comparison_policy`/`equal_level_policy` (configuration instance, §9); storage/schema/serialization; cơ chế lưu trữ/versioning cụ thể của `structure_definition_version` registry (Phase 1, cùng ghi chú `swing.md` §17); minimum displacement / độ lớn tối thiểu của một break (không được yêu cầu bởi controlling authority hiện tại — nếu cần, thuộc `structure_definition_version` policy tương lai, không hardcode ở Domain Contract).

## 17. Open questions ngoài phạm vi

- `StructureCurrentView.current_relevant_swing_ref` (§14) là tiện ích UI, không có nghĩa vụ chính xác tuyệt đối tại mọi thời điểm — cần làm rõ semantics chi tiết hơn (ví dụ khi nhiều Swing cùng direction đủ điều kiện đồng thời) khi có consumer thực tế; không quyết ở đây, không phải governance-level OQ.
- Structure Definition registry/lifecycle — giống ghi chú `swing.md` §18, chưa có authoritative source riêng, cần quyết định khi Package 0.2-B/0.2-C có nhu cầu thực tế đầu tiên.
