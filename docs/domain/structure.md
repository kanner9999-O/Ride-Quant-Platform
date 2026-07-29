---
id: structure
title: Market Structure
version: "0.4"
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

> **Vai trò của tài liệu này:** Domain Contract thứ hai của Package 0.2-B1 — hoàn thiện chuỗi `Candle → Swing → Structure`. Draft, chưa Approved/Locked. Thuộc capability `market-structure` / context `market-structure-analysis` (đã đăng ký tại [`context-map.yaml`](./context-map.yaml)), **cùng context với `swing.md`** — Swing → Structure là quan hệ intra-context, không phải cross-context edge (§9). **v0.2** xử lý ChatGPT Review A + Independent Review B (consolidated) trên baseline v0.1 — 3 Major: **C-B1-STR-MAJ-01** (tách `StructureInvalidated` thành `StructureFactInvalidated` — phủ định MỘT historical fact, KHÔNG tự động chuyển orientation — và `StructureRecomputed` — event DUY NHẤT xác lập orientation mới sau cascade, §5/§5a), **C-B1-STR-MAJ-02** (định nghĩa executable, total-order cho "Swing level nào đang relevant" — §6a, mới), **C-B1-STR-MAJ-03** (bỏ wording "most-recent-first", thay bằng dependency-forward invalidation tường minh — §10). **v0.3** là **narrow delta revision** xử lý 2 Major còn lại từ ChatGPT Review A delta + Independent Review B delta (clean-room) trên baseline v0.2 — **D-B1-STR-MAJ-01** (`broken_swing_ref` v0.2 mất chính xác Swing lifecycle generation — thay bằng canonical reference revision-qualified `{swing_id, swing_revision, swing_confirmed_event_ref, direction}`, §6a), **D-B1-STR-MAJ-02** (total order v0.2 không định nghĩa so sánh cross-stream — thay bằng 8-tiêu-chí tường minh, mỗi tiêu chí có hướng ASC/DESC rõ ràng, §6a). **v0.4** là **final narrow correction** xử lý 2 finding cuối từ Independent Review B final delta trên baseline v0.3 — **IRB-FD-STR-MAJ-01** (một câu trong §6a mâu thuẫn với chính lexicographic rule đã khai — nói "bỏ qua tiêu chí 5, chuyển thẳng tiêu chí 6" khi tiêu chí 3/4 lệch, thay vì dừng lại đúng tại 3/4; thay bằng thuật toán chuẩn tường minh + 3 ví dụ minh họa, §6a), **IRB-FD-STR-MIN-01** (§9 còn sót identifier `relevant_swing_selection_policy` lỗi thời của 4-tier order v0.2; xóa, thay bằng tham chiếu normative duy nhất tới §6a — chỉ một canonical identifier tồn tại). `swing.md` v0.2 và `context-map.yaml` v0.5 **không đổi** ở revision này (cả hai vẫn Clean).

Market Structure bao gồm **năm concept riêng biệt**:

1. **Logical Structure Subject** (`kind: entity`) — identity ổn định của "structure interpretation này", **một subject liên tục theo scope** (khác Swing/Candle — không có subject mới per pivot/window; xem §1).
2. **`BreakOfStructureDetected`** (`kind: event`) — orientation tiếp diễn hoặc được thiết lập lần đầu.
3. **`ChangeOfCharacterDetected`** (`kind: event`) — orientation đảo chiều.
4. **`StructureFactInvalidated`** (`kind: event`) — phủ định MỘT BOS/CHoCH lịch sử cụ thể, KHÔNG tự nó là orientation transition (§5).
5. **`StructureRecomputed`** (`kind: event`) — event DUY NHẤT xác lập current orientation mới sau khi một cascade invalidation hoàn tất (§5a).

Cộng một **read model tùy chọn** (`StructureCurrentView`) — projection tiện dụng, không authoritative.

**Không gộp Swing, BOS, CHoCH, và trend state vào một object mutable mơ hồ.** Mỗi orientation transition là một event append-only riêng biệt (I-3); orientation "hiện tại" chỉ tồn tại như derived state rebuild được từ chuỗi event, không phải trường dữ liệu ghi đè tại chỗ. **Ghi nhận một historical fact sai (StructureFactInvalidated) và quyết định orientation hiện tại là gì (StructureRecomputed) là HAI mối quan tâm tách biệt** (đóng C-B1-STR-MAJ-01) — v0.1 từng gộp cả hai vào một event duy nhất (`StructureInvalidated`), event đó **không còn tồn tại** trong v0.2 (Draft chưa từng Approved/Locked — thay thế trực tiếp, không cần deprecation notice).

**`break-of-structure-detected` / `change-of-character-detected` / `structure-fact-invalidated` / `structure-recomputed` / `structure-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây, và đúng giá trị `contract_id` mà [`context-map.yaml`](./context-map.yaml) sẽ trích dẫn (khi có edge cross-context — §9). Display name, concept ID, và `event_type` là ba đại lượng khác nhau, không cạnh tranh identity — cùng nguyên tắc `candle.md`/`swing.md` đã khóa.

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
  ChangeOfCharacterDetected (normal flow) / StructureRecomputed (correction flow, §5a). Đây là
  quyết định thiết kế tường minh: một
  "current interpretation" chỉ có ý nghĩa khi nó là MỘT state machine instance duy nhất theo
  thời gian, không phải nhiều instance rời rạc.
invariants:
  - "structure_subject_id resolve deterministic từ ĐÚNG BỐN field qualifying scope: instrument_id, venue_id, timeframe, structure_definition_version — cùng bốn-field-scope luôn cho cùng structure_subject_id; khác bất kỳ field nào cho structure_subject_id KHÁC. structure_subject_id bất biến, KHÔNG tái sử dụng cho một subject khác (Chapter 6 §6.1)."
  - "structure_subject_id là opaque — domain logic KHÔNG được parse nó (Chapter 6 §6.8); mọi quyết định nghiệp vụ phải dùng field tường minh trong scope."
  - "instrument_id, venue_id, timeframe, structure_definition_version bất biến sau khi subject được quan sát lần đầu — đổi bất kỳ field nào tạo ra một subject KHÁC, không phải mutate subject cũ. Đổi swing_definition_version mà structure_definition_version phụ thuộc (§9) BẮT BUỘC bump chính structure_definition_version — không cho phép một structure_subject_id âm thầm đổi ý nghĩa vì dependency đổi mà version của chính nó không đổi."
  - "current_orientation KHÔNG phải một field độc lập ghi đè tại chỗ — nó là derived state, rebuild được bằng cách apply tuần tự mọi BreakOfStructureDetected/ChangeOfCharacterDetected/StructureRecomputed của subject theo recorded_time (§8 no-repaint). StructureFactInvalidated KHÔNG tham gia fold current_orientation trực tiếp — nó chỉ đánh dấu một fact lịch sử cụ thể không còn hiệu lực (§5/§5a, đóng C-B1-STR-MAJ-01)."
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
    # Normal flow — BOS/CHoCH transition current_orientation trực tiếp (§6, §7)
    - {from: UNDETERMINED, to: BULLISH, caused_by: BreakOfStructureDetected}
    - {from: UNDETERMINED, to: BEARISH, caused_by: BreakOfStructureDetected}
    - {from: NEUTRAL, to: BULLISH, caused_by: BreakOfStructureDetected}
    - {from: NEUTRAL, to: BEARISH, caused_by: BreakOfStructureDetected}
    - {from: BULLISH, to: BULLISH, caused_by: BreakOfStructureDetected}
    - {from: BEARISH, to: BEARISH, caused_by: BreakOfStructureDetected}
    - {from: BULLISH, to: BEARISH, caused_by: ChangeOfCharacterDetected}
    - {from: BEARISH, to: BULLISH, caused_by: ChangeOfCharacterDetected}
    # Correction flow — StructureRecomputed là event DUY NHẤT đổi current_orientation sau cascade (§5a, §10)
    - {from: NEUTRAL, to: NEUTRAL, caused_by: StructureRecomputed}
    - {from: NEUTRAL, to: BULLISH, caused_by: StructureRecomputed}
    - {from: NEUTRAL, to: BEARISH, caused_by: StructureRecomputed}
    - {from: BULLISH, to: NEUTRAL, caused_by: StructureRecomputed}
    - {from: BULLISH, to: BULLISH, caused_by: StructureRecomputed}
    - {from: BULLISH, to: BEARISH, caused_by: StructureRecomputed}
    - {from: BEARISH, to: NEUTRAL, caused_by: StructureRecomputed}
    - {from: BEARISH, to: BULLISH, caused_by: StructureRecomputed}
    - {from: BEARISH, to: BEARISH, caused_by: StructureRecomputed}
  terminal_states: []
  note: "StructureFactInvalidated KHÔNG xuất hiện trong bảng transition này — nó ghi nhận việc phủ định MỘT historical fact cụ thể (§5), KHÔNG tự nó là một orientation transition. current_orientation chỉ đổi qua BreakOfStructureDetected/ChangeOfCharacterDetected (normal flow) hoặc StructureRecomputed (correction flow, đúng MỘT lần cho mỗi cascade — §5a)."
events_emitted: [BreakOfStructureDetected, ChangeOfCharacterDetected, StructureFactInvalidated, StructureRecomputed]
events_consumed: [SwingConfirmed, SwingInvalidated, CandleClosed, CandleCorrected]
commands: []
queries: []
```

**`UNDETERMINED` là notional initial state** — cùng convention `UNSEEN` mà `candle.md`/`swing.md` đã khóa: không event nào khẳng định "subject đang UNDETERMINED"; đây là điểm khởi đầu ngầm định trước khi có Swing nào đủ để xác định orientation.

**`NEUTRAL` KHÁC `UNDETERMINED`** — `NEUTRAL` là một giá trị **authoritative**, chỉ đạt được qua `StructureRecomputed` với `resulting_orientation: NEUTRAL` (§5a): "sau cascade invalidation, không còn fact nào biện minh cho một orientation cụ thể." `UNDETERMINED` không bao giờ được tái khẳng định bằng event — một khi subject đã rời `UNDETERMINED`, nó không quay lại đó; trạng thái "không có orientation rõ ràng" sau này luôn là `NEUTRAL` (một fact tường minh, qua `StructureRecomputed`), không phải `UNDETERMINED` (một non-fact).

**Không có transition nào rời khỏi `NEUTRAL` qua `ChangeOfCharacterDetected`** — CHoCH theo định nghĩa yêu cầu một **prior orientation trực tiếp (`BULLISH`/`BEARISH`)** để "đảo chiều" (§7); từ `NEUTRAL`, việc thiết lập orientation mới dùng đúng cơ chế `BreakOfStructureDetected` như từ `UNDETERMINED` (§6 — cùng executable criterion, không phân biệt).

## 2. Canonical event envelope — áp dụng cho mọi Structure event (§3–§5a)

Mọi event ở §3–§5a là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). Mục này khóa **envelope chung** một lần.

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
  StructureFactInvalidated: STRUCTURE_FACT_INVALIDATED
  StructureRecomputed: STRUCTURE_RECOMPUTED
```

`stream_ref`/`producer_ref` — Phase 1, chưa tồn tại, cùng nguyên tắc defer đã áp dụng ở `candle.md`/`swing.md`.

**`StructureStateChanged` KHÔNG được introduce như một event tổng hợp thứ năm** — mọi orientation transition (kể cả thiết lập lần đầu từ `UNDETERMINED`/`NEUTRAL`, và correction flow) đã biểu diễn đầy đủ qua bốn event đã khai (`BreakOfStructureDetected`/`ChangeOfCharacterDetected` cho normal flow; `StructureRecomputed` cho correction flow; `StructureFactInvalidated` cho historical fact record không mang orientation, §5); một event tổng hợp thêm sẽ tạo hai nguồn authority cạnh tranh cho cùng một orientation change (I-12).

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
  - "broken_swing_ref PHẢI là Eligible Swing theo total order §6a — Swing fact CONFIRMED, đúng cặp (swing_id, swing_revision) đó CHƯA từng là broken_swing_ref của một BreakOfStructureDetected/ChangeOfCharacterDetected trước đó còn hiệu lực (chưa nhận StructureFactInvalidated) — cấm cùng một (swing_id, swing_revision) được báo 'phá' hai lần độc lập; MỘT revision khác của cùng swing_id (ví dụ sau correction) là một cặp khác, đủ điều kiện độc lập (§6a, §11 same-level-broken-twice, đóng D-B1-STR-MAJ-01)."
  - "broken_swing_ref.direction PHẢI khớp bảng quyết định ở §6 theo new_orientation."
  - "broken_swing_ref.swing_confirmed_event_ref PHẢI trỏ đúng SwingConfirmed cho chính xác swing_id, swing_revision, direction, và instrument/venue/timeframe/swing_definition_version yêu cầu (§6a)."
  - "causation_refs PHẢI chứa: broken_swing_ref.swing_confirmed_event_ref; VÀ breaking_candle_refs (một hoặc nhiều candle-closed/candle-corrected) cung cấp bằng chứng break theo break_price_basis đã pin (§9)."
  - "envelope.effective_time = effective_time của Candle cuối cùng trong breaking_candle_refs (§7)."
  - "new_orientation != prior_orientation KHI prior_orientation là BULLISH hoặc BEARISH và new_orientation khác — TRƯỜNG HỢP ĐÓ KHÔNG HỢP LỆ trên event này (đó là ChangeOfCharacterDetected, §4), không phải BreakOfStructureDetected."
payload:
  prior_orientation: {type: enum, values: [UNDETERMINED, NEUTRAL, BULLISH, BEARISH], required: true}
  new_orientation: {type: enum, values: [BULLISH, BEARISH], required: true}
  broken_swing_ref: {type: broken_swing_ref, required: true, description: "revision-qualified reference — schema canonical tại §6a, đóng D-B1-STR-MAJ-01"}
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
  - "broken_swing_ref PHẢI là Eligible Swing theo total order §6a — Swing fact CONFIRMED, đúng cặp (swing_id, swing_revision) đó chưa từng là broken_swing_ref của một event trước đó còn hiệu lực (chưa nhận StructureFactInvalidated); một revision khác của cùng swing_id đủ điều kiện độc lập (§6a, đóng D-B1-STR-MAJ-01)."
  - "broken_swing_ref.swing_confirmed_event_ref PHẢI trỏ đúng SwingConfirmed cho chính xác swing_id, swing_revision, direction, và instrument/venue/timeframe/swing_definition_version yêu cầu (§6a)."
  - "causation_refs PHẢI chứa: broken_swing_ref.swing_confirmed_event_ref; VÀ breaking_candle_refs cung cấp bằng chứng break."
  - "envelope.effective_time = effective_time của Candle cuối cùng trong breaking_candle_refs."
payload:
  prior_orientation: {type: enum, values: [BULLISH, BEARISH], required: true}
  new_orientation: {type: enum, values: [BULLISH, BEARISH], required: true}
  broken_swing_ref: {type: broken_swing_ref, required: true, description: "revision-qualified reference — schema canonical tại §6a, đóng D-B1-STR-MAJ-01"}
  breaking_candle_refs: {type: array, items: event_record_ref, required: true}
```

## 5. `StructureFactInvalidated` — `kind: event` (đóng C-B1-STR-MAJ-01)

Kế thừa nguyên vẹn envelope §2 — `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: structure-fact-invalidated
kind: event
capability_id: market-structure
domain_context_id: market-structure-analysis
description: >
  Phủ định MỘT BreakOfStructureDetected hoặc ChangeOfCharacterDetected cụ thể của cùng
  structure_subject_id, do correction cascade — thuần túy ghi nhận "fact lịch sử này không
  còn hợp lệ", KHÔNG BAO GIỜ tự động tuyên bố hay ngụ ý một orientation transition (đóng
  C-B1-STR-MAJ-01 — tách bạch khỏi StructureRecomputed, §5a). KHÔNG BAO GIỜ do "giá tiếp tục
  di chuyển" (đó là một BOS/CHoCH mới thuộc normal flow, không phải invalidation — §8
  no-repaint). BA nguyên nhân, khai báo tường minh qua payload.invalidation_cause:
  (a) swing_invalidated — broken_swing_ref của fact đang bị invalidate đã nhận SwingInvalidated
      (upstream_correction, swing.md §5) — level dùng làm căn cứ break không còn hợp lệ;
  (b) breaking_candle_corrected — một Candle trong breaking_candle_refs bị CandleCorrected
      khiến nó không còn thỏa break criterion (§9) theo payload đã sửa;
  (c) chained_invalidation — fact này phụ thuộc (qua prior_orientation, §6/§7) vào MỘT fact
      khác vừa nhận StructureFactInvalidated trong CÙNG cascade — dependency-forward theo
      chuỗi orientation gốc, KHÔNG phải "most-recent-first" theo recorded_time (đóng
      C-B1-STR-MAJ-03, xem worked example §10).
  Là event MỚI, append-only (I-3). HỢP LỆ ngay cả khi current_orientation hiện tại ĐÃ LÀ
  NEUTRAL (ví dụ một cascade thứ hai chồng lên cascade trước) — event này không kiểm tra hay
  phụ thuộc current_orientation, chỉ phủ định đúng MỘT fact record cụ thể. Một cascade phát
  NHIỀU StructureFactInvalidated liên tiếp — một cho mỗi fact bị ảnh hưởng (§10) — rồi kết
  thúc bằng đúng MỘT StructureRecomputed (§5a).
invariants:
  - "causation_refs PHẢI trỏ: event BOS/CHoCH đang bị invalidate (bắt buộc, đúng một); VÀ nguyên nhân — SwingInvalidated (a), CandleCorrected (b), hoặc StructureFactInvalidated của fact mà nó phụ thuộc trong cascade (c)."
  - "invalidation_cause = swing_invalidated CHỈ hợp lệ khi SwingInvalidated được trỏ tới khớp ĐÚNG CẢ: swing_id VÀ swing_revision của broken_swing_ref của fact bị invalidate (không chỉ swing_id) — và, khi có, khớp đúng swing_confirmed_event_ref đã tham chiếu (đóng D-B1-STR-MAJ-01, rule 5). Một SwingInvalidated cho revision N KHÔNG được dùng làm nguyên nhân invalidate một Structure fact có broken_swing_ref.swing_revision = M ≠ N trên cùng swing_id — dù cùng swing_id, hai revision là hai pair (swing_id, swing_revision) độc lập (rule 6: 'SwingInvalidated cho revision 1 không được invalidate một Structure fact đã dùng revision 2')."
  - "invalidation_cause = breaking_candle_corrected CHỈ hợp lệ khi Candle bị sửa nằm trong breaking_candle_refs của fact bị invalidate VÀ payload đã sửa không còn thỏa break criterion (§9)."
  - "invalidation_cause = chained_invalidation CHỈ hợp lệ khi payload.prior_orientation của fact bị invalidate bằng đúng new_orientation của fact NGAY TRƯỚC nó trong chuỗi orientation gốc (§6/§7 decision table) — xác định bằng dependency graph, KHÔNG bằng recorded_time phát sinh của invalidation (§10)."
  - "Một BreakOfStructureDetected/ChangeOfCharacterDetected chỉ nhận ĐÚNG MỘT StructureFactInvalidated authoritative — không invalidate trùng lặp cùng một fact hai lần (§11)."
  - "Event này KHÔNG mang bất kỳ field orientation nào (không prior_orientation/new_orientation) — nó không phải, và không được diễn giải là, một state transition (§1)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của event gây invalidation trực tiếp (nguyên nhân (a)/(b)/(c))."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true, description: "BreakOfStructureDetected hoặc ChangeOfCharacterDetected bị phủ định — trùng với causation_refs, khai báo tường minh trong payload để query không cần đọc lại envelope"}
  invalidation_cause: {type: enum, values: [swing_invalidated, breaking_candle_corrected, chained_invalidation], required: true}
  invalidation_reason: {type: string, required: false}
```

## 5a. `StructureRecomputed` — `kind: event` (đóng C-B1-STR-MAJ-01)

Kế thừa nguyên vẹn envelope §2 — `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: structure-recomputed
kind: event
capability_id: market-structure
domain_context_id: market-structure-analysis
description: >
  Fact AUTHORITATIVE thiết lập current_orientation MỚI sau khi một cascade invalidation (một
  hoặc nhiều StructureFactInvalidated, §5) đã hoàn tất — event DUY NHẤT thay đổi
  current_orientation trong correction flow (đóng C-B1-STR-MAJ-01; đối xứng normal flow nơi
  BreakOfStructureDetected/ChangeOfCharacterDetected trực tiếp transition orientation, §1).
  Luôn phát sinh SAU khi TOÀN BỘ fact bị ảnh hưởng trong cascade đã nhận
  StructureFactInvalidated — không có StructureRecomputed "một phần". `resulting_orientation`
  do refold trực tiếp toàn bộ Swing/Candle fact còn hiệu lực tại `input_cursor_ref` quyết định
  — có thể là NEUTRAL (không còn fact nào biện minh cho một hướng) hoặc BULLISH/BEARISH (một
  fact còn hiệu lực, hoặc một chuỗi suy luận lại từ input, vẫn biện minh cho hướng đó).
invariants:
  - "causation_refs PHẢI trỏ đủ MỌI StructureFactInvalidated thuộc cùng cascade — không được sót một fact vừa invalidate ngoài causation (§10)."
  - "payload.resulting_orientation PHẢI thuộc {NEUTRAL, BULLISH, BEARISH} — KHÔNG BAO GIỜ UNDETERMINED (một khi đã có fact từng tồn tại và bị invalidate, kết luận hợp lệ tối thiểu là NEUTRAL, không lùi về notional UNDETERMINED, §1)."
  - "payload.justifying_fact_ref REQUIRED khi resulting_orientation ∈ {BULLISH, BEARISH} — PHẢI trỏ một BreakOfStructureDetected/ChangeOfCharacterDetected CÒN HIỆU LỰC (chưa nhận StructureFactInvalidated) biện minh trực tiếp cho hướng đó; PROHIBITED khi resulting_orientation = NEUTRAL (không có fact nào 'sống sót' biện minh cho một hướng — đó chính là ý nghĩa của NEUTRAL)."
  - "payload.input_cursor_ref BẮT BUỘC trên mọi resulting_orientation (kể cả NEUTRAL) — pin chính xác cursor/input set (Swing + Candle fact còn hiệu lực) dùng để refold, đủ để tái tạo kết quả này một cách deterministic (tinh thần Chapter 8 §8.1.1 Referenced Authoritative Artifact)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của StructureFactInvalidated cuối cùng trong cascade."
  - "Đúng một StructureRecomputed cho mỗi cascade — không phát nhiều StructureRecomputed cho cùng một cascade invalidation set."
payload:
  resulting_orientation: {type: enum, values: [NEUTRAL, BULLISH, BEARISH], required: true}
  justifying_fact_ref: {type: event_record_ref, required: false, description: "REQUIRED khi resulting_orientation != NEUTRAL, PROHIBITED khi NEUTRAL — xem invariants"}
  input_cursor_ref: {type: object, required: true, description: "pin cursor/input set dùng để refold — xem invariants"}
```

## 6. BOS semantics — executable criterion

**Broken level (bảng quyết định):**

| `prior_orientation` | `new_orientation` | `broken_swing_ref.direction` |
|---|---|---|
| `UNDETERMINED` / `NEUTRAL` | `BULLISH` | `HIGH` |
| `UNDETERMINED` / `NEUTRAL` | `BEARISH` | `LOW` |
| `BULLISH` | `BULLISH` (continuation) | `HIGH` |
| `BEARISH` | `BEARISH` (continuation) | `LOW` |

**`broken_swing_ref` PHẢI là Eligible `(swing_id, swing_revision)` theo total order §6a** — không phải "Swing gần nhất" mơ hồ, và không phải `swing_id` một mình. §6a định nghĩa executable, deterministic selection rule đầy đủ (đóng C-B1-STR-MAJ-02, delta D-B1-STR-MAJ-01/02), bao gồm rule ngăn "same level broken twice": một khi một `(swing_id, swing_revision)` cụ thể đã là `broken_swing_ref` của một fact còn hiệu lực, ĐÚNG CẶP đó không đủ điều kiện làm căn cứ cho một BOS/CHoCH thứ hai — nhưng một revision KHÁC của cùng `swing_id` là một cặp riêng, đủ điều kiện độc lập.

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

## 6a. Deterministic relevant Swing selection — total order (đóng C-B1-STR-MAJ-02, delta D-B1-STR-MAJ-01/02)

**Canonical `broken_swing_ref` schema** — dùng thống nhất bởi §3 (BOS) và §4 (CHoCH), thay thế shorthand `{swing_id, direction}` v0.2 (đóng D-B1-STR-MAJ-01 — reference trước đây mất chính xác lifecycle generation nào của Swing đã được tiêu thụ):

```yaml
broken_swing_ref:
  swing_id: {type: string, required: true}                        # logical identity — swing.md §1
  swing_revision: {type: integer, required: true}                 # generation identity — swing.md §1a
  swing_confirmed_event_ref: {type: event_record_ref, required: true}   # trỏ đúng SwingConfirmed của (swing_id, swing_revision) này
  direction: {type: enum, values: [HIGH, LOW], required: true}
```

Cả bốn field BẮT BUỘC tường minh — không field nào được omit hay suy diễn ngầm từ field khác. `swing_confirmed_event_ref` là **verification field**, cùng nguyên tắc `event_record_ref` (Chapter 8 §8.2.3): `(swing_id, swing_revision, direction)` là logical locator, `swing_confirmed_event_ref` xác minh đúng bản ghi vật lý.

**Eligible Swing** cho một `broken_swing_ref` (dùng chung bởi BOS §6 và CHoCH §7) tại một cursor recorded-time — hoạt động trên ĐÚNG CẶP `(swing_id, swing_revision)`, không phải `swing_id` một mình:

```text
Eligible (swing_id, swing_revision) =
  SwingConfirmed cho ĐÚNG cặp (swing_id, swing_revision) đó (swing.md §4)
  visible tại cursor recorded_time hiện tại (swing.md §7 — không look-ahead)
  matching instrument_id/venue_id/timeframe/direction theo bảng quyết định §6/§7
  matching structure_definition_version.depends_on_swing_definition_version (§9)
  KHÔNG có SwingInvalidated visible cho ĐÚNG cặp (swing_id, swing_revision) đó tại cursor (swing.md §5)
  KHÔNG đã được dùng làm broken_swing_ref của một BOS/CHoCH còn hiệu lực cho ĐÚNG cặp đó (chưa StructureFactInvalidated, §3/§4 invariant)
  = revision hợp lệ MỚI NHẤT của swing_id đó tại cursor (swing.md §1a — không có revision nào mới hơn còn hiệu lực đứng trước nó bị bỏ qua)
```

**Consumed semantics áp dụng CHO ĐÚNG CẶP, không cho `swing_id` toàn cục (đóng D-B1-STR-MAJ-01, rule 3):** một `(swing_id, swing_revision)` đã là `broken_swing_ref` của một fact còn hiệu lực thì cặp đó — và chỉ cặp đó — không đủ điều kiện làm `broken_swing_ref` lần nữa. Một revision KHÁC của cùng `swing_id` (ví dụ revision N+1 sau khi revision N bị `SwingInvalidated`) là một cặp khác, **đủ điều kiện độc lập** ngay khi nó CONFIRMED — không bị "khóa" bởi việc revision N từng được tiêu thụ (rule 4). Đối xứng: một `SwingInvalidated` cho revision N **không được** dùng làm nguyên nhân invalidate một Structure fact đã tiêu thụ revision M ≠ N của cùng `swing_id` (rule 6, §5 invariant).

**Total order khi nhiều Eligible Swing thỏa cùng điều kiện** — 8 tiêu chí, áp dụng tuần tự, dừng ở tiêu chí đầu tiên phân biệt được hai ứng viên (đóng D-B1-STR-MAJ-02, thay hoàn toàn 4-tier v0.2):

| # | Tiêu chí | Hướng |
|---|---|---|
| 1 | `pivot_effective_time.window_start` | **DESC** — pivot gần cursor nhất ưu tiên ("level gần nhất chưa bị phá") |
| 2 | `SwingConfirmed.recorded_time` | **ASC** — biết sớm hơn ưu tiên (T vs T+n, `swing.md` §7) |
| 3 | `stream_ref.stream_id` | **ASC**, lexical — xác lập **stream identity** làm cơ sở so `sequence` ở (5) |
| 4 | `stream_ref.registry_version` | **ASC**, lexical — cùng `stream_id` nhưng khác registry snapshot vẫn phân biệt được (Chapter 8 §8.3.1) |
| 5 | `sequence` | **ASC** — CHỈ có nghĩa **trong cùng stream identity** đã xác lập bởi (3)+(4); xem ràng buộc dưới |
| 6 | `swing_revision` | **DESC** — khi mọi tiêu chí business-time ở trên hòa, revision hợp lệ MỚI NHẤT thắng |
| 7 | `swing_id` | **ASC**, lexical — tie-break kỹ thuật thuần túy |
| 8 | `SwingConfirmed.event_id` | **ASC**, lexical — tie-break kỹ thuật cuối cùng |

**Thuật toán chuẩn (normative, đóng IRB-FD-STR-MAJ-01 — loại bỏ mâu thuẫn giữa "dừng ở tiêu chí đầu tiên phân biệt được" và cách diễn đạt cũ về tiêu chí 5):**

```text
So sánh tiêu chí 1 đến 8 theo đúng thứ tự.
Tiêu chí ĐẦU TIÊN có giá trị khác nhau quyết định ứng viên thắng.
Các tiêu chí sau đó KHÔNG được đánh giá.
```

Đây là **lexicographic comparison nghiêm ngặt** — không có nhánh "bỏ qua tiêu chí X, chuyển thẳng tiêu chí Y" nào khác ngoài việc dừng lại đúng tại tiêu chí đầu tiên phân biệt được.

**Ràng buộc bắt buộc cho tiêu chí (5) — điều kiện tiên quyết để tiêu chí này có nghĩa:** `sequence` **chỉ được diễn giải nghiệp vụ khi VÀ CHỈ KHI** `stream_ref.stream_id` bằng nhau **VÀ** `stream_ref.registry_version` bằng nhau (tức (3) VÀ (4) đã hòa) — đây là điều kiện tiên quyết để tiêu chí (5) **có thể được đánh giá**, không phải một ngoại lệ cho phép "nhảy" qua tiêu chí (5):

- **Nếu tiêu chí (3) khác nhau** → tiêu chí (3) quyết định ứng viên thắng → **dừng so sánh tại đây** — tiêu chí (4)-(8) KHÔNG được đánh giá.
- **Nếu tiêu chí (3) hòa nhưng tiêu chí (4) khác nhau** → tiêu chí (4) quyết định ứng viên thắng → **dừng so sánh tại đây** — tiêu chí (5)-(8) KHÔNG được đánh giá.
- **CHỈ khi cả (3) VÀ (4) đều hòa**, tiêu chí (5) mới được đánh giá.

**Cấm tuyệt đối:** so sánh `sequence` thô giữa hai stream khác nhau như thể chúng tạo thành một global order — đúng nguyên tắc [Chapter 8 §8.3.3](../constitution/08-event-model.md) (platform không tuyên bố global total order giữa các stream độc lập) và [ADR-009](../adr/ADR-009.md) (per-stream contiguous sequence, không global sequence). **Prohibition này KHÔNG làm suy yếu vai trò ordering criterion của (3)/(4)** — ngược lại, chính (3)/(4) là lý do duy nhất khiến (5) không bao giờ được dùng để so hai stream khác nhau: khi (3) hoặc (4) khác nhau, việc dừng lại ngay tại (3)/(4) (chứ không "nhảy" tới (5) rồi mới nhận ra không so được) chính là cơ chế ngăn so sánh `sequence` xuyên stream.

**Ví dụ minh họa (đóng IRB-FD-STR-MAJ-01):**

```text
# Ví dụ 1 — khác stream_id
A.stream_id = alpha
B.stream_id = beta

alpha < beta
→ A thắng tại tiêu chí 3
→ tiêu chí 4–8 KHÔNG được đánh giá

# Ví dụ 2 — cùng stream_id, khác registry_version
A.stream_id = alpha
B.stream_id = alpha
A.registry_version = v1
B.registry_version = v2

v1 < v2
→ A thắng tại tiêu chí 4
→ tiêu chí 5–8 KHÔNG được đánh giá

# Ví dụ 3 — cùng stream identity, khác sequence
A.stream_id = alpha, A.registry_version = v1, A.sequence = 100
B.stream_id = alpha, B.registry_version = v1, B.sequence = 105

cùng stream_id, cùng registry_version → tiêu chí 5 được phép đánh giá
100 < 105
→ A thắng tại tiêu chí 5 (sequence nhỏ hơn thắng)
```

**`swing_revision DESC` (tiêu chí 6)** đảm bảo: khi hai `SwingConfirmed` hòa cả năm tiêu chí business-time/stream đầu tiên (trường hợp cực hiếm, ví dụ hai revision cùng pivot, cùng recorded_time, cùng stream) — revision hợp lệ MỚI NHẤT (số lớn hơn) thắng, đúng tinh thần "recompute luôn ưu tiên interpretation mới nhất" của swing.md §1a.

**`swing_id` (7) và `event_id` (8) là tie-break kỹ thuật thuần túy** — deterministic theo string ordering của opaque ID, KHÔNG mang ý nghĩa nghiệp vụ. **Opaque identifier (bao gồm mọi ID dùng trong bảng trên) KHÔNG được parse để suy ra timestamp hay business semantics** ([Chapter 6 §6.8](../constitution/06-identity-model.md)) — string ordering chỉ dùng để đảm bảo total order, không diễn giải nội dung ID.

**Nếu cả 8 giá trị đều khớp, hai bản ghi là duplicate của cùng một authoritative fact** (§11 dedup) — không có tiêu chí thứ chín.

**Canonical policy identifier — nguồn duy nhất, pin trong `structure_definition_version` (§9, đóng IRB-FD-STR-MIN-01):**

```yaml
relevant_swing_selection_policy: pivot_effective_time_window_start_desc_then_recorded_time_asc_then_stream_id_asc_then_registry_version_asc_then_sequence_asc_then_swing_revision_desc_then_swing_id_asc_then_event_id_asc
```

Đây là **giá trị canonical duy nhất** cho `relevant_swing_selection_policy` của Structure v0.3/v0.4 — §9 chỉ tham chiếu tới mục này theo tên field, KHÔNG lặp lại chuỗi, để không thể có hai bản identifier lệch nhau.

Một `structure_definition_version` tương lai có thể chọn thứ tự khác, nhưng PHẢI vẫn total + deterministic + tương thích [ADR-009](../adr/ADR-009.md) (không dùng physical wall clock; không suy ordering từ ID nhúng timestamp, [Chapter 6 §6.3](../constitution/06-identity-model.md); không so `sequence` xuyên stream như một global order).

**`StructureCurrentView.current_relevant_swing_ref` (§14) resolve theo đúng total order 8-tiêu-chí này** — luôn trỏ Eligible `(swing_id, swing_revision)` hiện tại, không còn mơ hồ "Swing nào đó gần đây" (đóng D-B1-STR-MAJ-02, rule 10).

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

- **`BreakOfStructureDetected`/`ChangeOfCharacterDetected` KHÔNG BAO GIỜ bị ghi đè tại chỗ** — một khi phát sinh, chỉ có thể bị phủ định qua `StructureFactInvalidated` với nguyên nhân tường minh (§5), KHÔNG BAO GIỜ vì "giá tiếp tục di chuyển theo hướng khác" — đó luôn là một BOS/CHoCH **mới**, không phải invalidation của fact cũ. `current_orientation` sau một cascade chỉ đổi qua đúng một `StructureRecomputed` (§5a) — không suy diễn ngầm từ việc các fact cũ bị invalidate.
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
  relevant_swing_selection_policy: <string>   # total-order policy identifier cho Eligible Swing — PHẢI khớp NGUYÊN VĂN identifier canonical đã khai báo tại §6a (đóng IRB-FD-STR-MIN-01 — không lặp lại chuỗi ở đây để tránh hai bản có thể lệch nhau theo thời gian; §6a là authoritative duy nhất cho giá trị chính xác)
```

**`relevant_swing_selection_policy` chỉ có ĐÚNG MỘT canonical identifier cho Structure v0.3/v0.4** — giá trị chính xác được khai báo tại §6a; mục này KHÔNG lặp lại chuỗi để tránh drift giữa hai bản sao (đóng IRB-FD-STR-MIN-01, thay thế identifier v0.2 đã lỗi thời `pivot_effective_time_desc_then_recorded_time_then_stream_then_swing_id` — identifier đó chỉ phản ánh 4-tier order cũ, không còn hợp lệ từ v0.3).

**`depends_on_swing_definition_version` bắt buộc** — Structure không tự định nghĩa lại policy nhận diện Swing; nó chỉ tiêu thụ Swing fact đã CONFIRMED theo policy Swing đã pin sẵn (§1 invariant: đổi dependency bắt buộc bump `structure_definition_version`).

**Không chọn một trường phái làm chuẩn phổ quát duy nhất** — `wick` vs `close`, `strict` vs `inclusive` đều hợp lệ, chọn qua `structure_definition_version`, đúng yêu cầu tách "Structure semantic contract" khỏi "specific strategy/configuration policy."

## 10. Correction cascade — dependency-forward invalidation (đóng C-B1-STR-MAJ-03)

```text
CandleCorrected
  → (a) nếu Candle là pivot/evidence của một Swing  → SwingInvalidated (swing.md §10) → StructureFactInvalidated (invalidation_cause: swing_invalidated) cho fact BOS/CHoCH có broken_swing_ref trỏ Swing đó
  → (b) nếu Candle là breaking_candle_refs của một BOS/CHoCH mà KHÔNG qua Swing nào bị invalidate → StructureFactInvalidated (invalidation_cause: breaking_candle_corrected) trực tiếp
```

Cả hai nhánh **đều** trigger cascade — đây là lý do Structure tiêu thụ **trực tiếp** `candle-closed`/`candle-corrected` (§12) thay vì chỉ dựa vào `swing-invalidated`: nhánh (b) không đi qua Swing nào cả (breaking Candle có thể nằm ngoài evidence window của bất kỳ Swing nào — nó chỉ là Candle xác nhận break, không phải Candle cấu thành pivot).

**Thứ tự xử lý — dependency-forward, KHÔNG "most-recent-first":**

1. Emit `StructureFactInvalidated` cho fact BOS/CHoCH bị ảnh hưởng **trực tiếp** (nhánh (a) hoặc (b)) — đây là **direct invalidated ancestor** của cascade.
2. Traverse các Structure fact **phụ thuộc** (causally dependent) theo ĐÚNG thứ tự chuỗi orientation GỐC (không phải recorded_time invalidation): fact `E(k+1)` phụ thuộc `E(k)` khi `E(k+1).prior_orientation = E(k).new_orientation` (§6/§7 decision table) và `E(k+1)` phát sinh sau `E(k)` trong chuỗi gốc.
3. Emit MỘT `StructureFactInvalidated` cho mỗi fact phụ thuộc, theo đúng thứ tự traverse ở bước 2 — dependency order, đi từ ancestor trực tiếp xuôi theo chuỗi, không phải ngược thời gian phát sinh.
4. Mỗi `StructureFactInvalidated` trong chuỗi causation trỏ tới: (i) fact nó phủ định; (ii) `StructureFactInvalidated` NGAY TRƯỚC nó trong cùng cascade (`chained_invalidation`) — hoặc trực tiếp nguyên nhân gốc (`SwingInvalidated`/`CandleCorrected`) nếu chính nó là fact đầu tiên của cascade (`swing_invalidated`/`breaking_candle_corrected`).
5. Sau khi TOÀN BỘ fact bị ảnh hưởng đã nhận `StructureFactInvalidated`, emit ĐÚNG MỘT `StructureRecomputed` (§5a).
6. `StructureRecomputed.causation_refs` trỏ đủ toàn bộ tập `StructureFactInvalidated` vừa phát trong cascade.
7. KHÔNG descendant invalidation nào được causation tới một invalidation CHƯA commit — mỗi `StructureFactInvalidated` trong chuỗi chỉ được phát SAU KHI fact nó phụ thuộc (bước 4.ii) đã committed.
8. Replay trước `recorded_time` của TỪNG event KHÔNG được thấy event đó (đối xứng §8) — áp dụng độc lập cho mỗi `StructureFactInvalidated` và cho `StructureRecomputed`.

**Worked example (dependency-forward, thay hoàn toàn "most-recent-first"; broken_swing_ref revision-qualified — đóng D-B1-STR-MAJ-01):**

```text
E1 (broken_swing_ref = swing_id S-A, revision 1) → E2 (broken_swing_ref = swing_id S-B, revision 1) → E3 (broken_swing_ref = swing_id S-C, revision 1)
  chuỗi orientation gốc: E1.new_orientation = E2.prior_orientation; E2.new_orientation = E3.prior_orientation

correction invalidates SwingInvalidated(S-A, revision 1) — CHỈ khớp broken_swing_ref có ĐÚNG (swing_id: S-A, swing_revision: 1);
  KHÔNG ảnh hưởng bất kỳ fact nào tiêu thụ (S-A, revision 2) nếu revision đó tồn tại (§6a, đóng D-B1-STR-MAJ-01 rule 6)

I1 invalidates E1                    — cause: swing_invalidated (SwingInvalidated của đúng S-A revision 1); causation = [E1, SwingInvalidated(S-A, rev 1)]
I2 invalidates E2, cause I1          — invalidation_cause: chained_invalidation; causation = [E2, I1]
I3 invalidates E3, cause I2          — invalidation_cause: chained_invalidation; causation = [E3, I2]
R1 recomputes orientation, cause [I1, I2, I3]   — StructureRecomputed; causation = [I1, I2, I3]

# Nếu sau đó Swing Engine confirm (S-A, revision 2) — cùng swing_id, pivot Candle không đổi (swing.md §10) —
# (S-A, revision 2) là MỘT cặp Eligible ĐỘC LẬP theo §6a, có thể trở thành broken_swing_ref của một
# BreakOfStructureDetected MỚI ngay khi đủ điều kiện — không bị "khóa" bởi việc revision 1 từng bị tiêu thụ.
```

**Orientation sau R1 — deterministic:** `R1.payload.resulting_orientation` xác định bằng cách refold TOÀN BỘ Swing/Candle fact còn hiệu lực tại `R1.payload.input_cursor_ref` theo đúng §6/§6a/§7 — KHÔNG suy luận cô lập từ việc "E1/E2/E3 đã mất". Hai kết quả khả dĩ:

- **Refold tìm thấy một fact còn hiệu lực biện minh cho một hướng** (ví dụ một BOS/CHoCH cũ hơn E1, chưa từng bị invalidate, hoặc một Eligible Swing khác theo §6a đủ điều kiện phá) → `resulting_orientation` = `BULLISH`/`BEARISH`, `justifying_fact_ref` trỏ đúng fact đó.
- **Refold không tìm thấy fact nào còn hiệu lực biện minh cho một hướng** → `resulting_orientation = NEUTRAL`, `justifying_fact_ref` vắng mặt. Nếu ngay sau đó dữ liệu mới (Swing/Candle) tạo ra một break hợp lệ, đó là một `BreakOfStructureDetected` **MỚI** thuộc normal flow (§1, §6) — không phải một phần của `R1`.

**Deduplicate cascade:** nếu cả một `SwingInvalidated` VÀ một `CandleCorrected` trực tiếp cùng ảnh hưởng một `BreakOfStructureDetected`/`ChangeOfCharacterDetected` (trường hợp hiếm — cùng một correction gốc lan tới cả hai đường), chỉ phát **một** `StructureFactInvalidated` cho fact đó — `causation_refs` liệt kê đủ cả hai nguyên nhân dưới dạng nhiều phần tử, `invalidation_cause` chọn nguyên nhân **trực tiếp nhất tại chính broken_swing_ref/breaking_candle_refs của fact đang bị invalidate** (không phát hai `StructureFactInvalidated` trùng lặp cho cùng fact — vi phạm §5 invariant, tương tự `swing.md` §12).

**Structure phải trace mọi output về đúng input:** `causation_refs` của mọi BOS/CHoCH/`StructureFactInvalidated`/`StructureRecomputed` luôn resolve ngược được về Swing fact + Candle fact gốc (I-1 Explainability).

**Preserve prior outputs:** không event nào bị xóa; `StructureFactInvalidated`/`StructureRecomputed` là fact bổ sung, không phải xóa fact cũ (I-3).

**Replay visibility theo `recorded_time`:** đối xứng §8.

## 11. Deduplication và ordering

Đối xứng `swing.md` §12, áp dụng lại nguyên tắc **không copy mù các rule đặc thù của Candle**:

- **Computation identity thay `source_identity`:** Structure là fact tự tính, không có external retry/redelivery — dedup dựa trên `(subject_id, event_type, causation_refs-set, payload)` giống hệt; recompute trên input không đổi phải idempotent, không tạo bản ghi thứ hai.
- **Same level broken multiple times:** ngăn ở nguồn bằng invariant §3/§4 — đúng cặp `(swing_id, swing_revision)` chưa từng dùng làm `broken_swing_ref` còn hiệu lực (§6a) — không dựa vào dedup hậu kiểm. Một revision khác của cùng `swing_id` không bị chặn bởi rule này (§6a).
- **Eligible Swing tie theo total order §6a:** nếu cả 8 tiêu chí đều khớp giữa hai `SwingConfirmed` ứng viên, chúng là duplicate của cùng một authoritative fact — không có nhánh thứ chín.
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

**Không phải authoritative event** (Chapter 7 §7.4 Type 2 Projection). Rebuild được từ §3–§5a.

```yaml
id: structure-current-view
kind: read_model
capability_id: market-structure
domain_context_id: market-structure-analysis
description: >
  Projection tiện dụng: orientation "hiện tại" và Eligible Swing liên quan (§6a) của một
  Structure subject, rebuild được từ BreakOfStructureDetected/ChangeOfCharacterDetected/
  StructureRecomputed (current_orientation) và StructureFactInvalidated (lịch sử fact nào
  không còn hiệu lực). KHÔNG authoritative — mọi audit/replay/parity, và mọi input cho concept
  khác (kể cả Feature, khi được author), phải dùng authoritative event stream, KHÔNG dùng view
  này làm nguồn sự thật (I-12, Chapter 7 §7.4). Cursor-bounded — không có "current" ngoài một
  cursor cụ thể khi dùng cho bất kỳ mục đích decision-relevant.
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream cùng structure_definition_version đã pin, cùng implementation version (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho bất kỳ Decision hay Domain Contract khác — chỉ query/UI (Chapter 7 §7.4)."
  - "Không có view row nào tồn tại khi subject còn UNDETERMINED (§1) — kỳ vọng bình thường, KHÔNG phải missing-data condition."
  - "current_relevant_swing_ref PHẢI resolve đúng Eligible (swing_id, swing_revision) theo total order 8-tiêu-chí §6a — không phải 'Swing gần đây' mơ hồ, và không phải swing_id một mình (đóng C-B1-STR-MAJ-02, delta D-B1-STR-MAJ-01/02)."
schema:
  structure_subject_id: {type: string, required: true}
  scope: {instrument_id: string, venue_id: string, timeframe: string, structure_definition_version: string, required: true}
  current_orientation: {type: enum, values: [UNDETERMINED, NEUTRAL, BULLISH, BEARISH], required: true}
  current_relevant_swing_ref: {type: broken_swing_ref, description: "Eligible (swing_id, swing_revision) theo total order §6a — schema canonical {swing_id, swing_revision, swing_confirmed_event_ref, direction} — derived, không authoritative"}
  last_recorded_time: timestamp
queries: [GetCurrentStructure, GetStructureHistory]
```

## 15. Authority boundary

**Contract này sở hữu:** BOS/CHoCH semantics, historical fact invalidation vs orientation recomputation split (§5/§5a), Eligible Swing total order (§6a), structure orientation state machine, `StructureCurrentView` projection shape, `structure_definition_version` policy schema tối thiểu (§9). **Áp dụng, không định nghĩa lại:** event envelope ([Chapter 8 §8.2](../constitution/08-event-model.md)); ordering/replay cursor mechanics ([Chapter 5](../constitution/05-time-model.md)/[Chapter 8](../constitution/08-event-model.md)); ID opaque rule ([Chapter 6 §6.8](../constitution/06-identity-model.md)); Swing pivot/confirmation semantics (`swing.md`); Regime independence ([ADR-003](../adr/ADR-003.md)). **Không sở hữu:** giá trị cụ thể của `structure_definition_version` policy (configuration/Phase 1); Feature fan-in logic (Package 0.2-B, chưa author — Structure chỉ publish, không định nghĩa consumer); service boundary/module layout/deployment (Engineering/Phase 1).

## 16. Ngoài phạm vi — defer

Cơ chế tính `structure_subject_id` deterministic cụ thể; giá trị cụ thể mặc định cho `break_price_basis`/`comparison_policy`/`equal_level_policy` (configuration instance, §9); storage/schema/serialization; cơ chế lưu trữ/versioning cụ thể của `structure_definition_version` registry (Phase 1, cùng ghi chú `swing.md` §17); minimum displacement / độ lớn tối thiểu của một break (không được yêu cầu bởi controlling authority hiện tại — nếu cần, thuộc `structure_definition_version` policy tương lai, không hardcode ở Domain Contract).

## 17. Open questions ngoài phạm vi

- Structure Definition registry/lifecycle — giống ghi chú `swing.md` §18, chưa có authoritative source riêng, cần quyết định khi Package 0.2-B/0.2-C có nhu cầu thực tế đầu tiên.
- `relevant_swing_selection_policy` (§6a, §9) hiện chỉ định nghĩa MỘT policy identifier mặc định; nếu tương lai cần nhiều policy khả dụng song song trong cùng platform (không chỉ tuần tự thay thế qua version), cơ chế lựa chọn giữa nhiều policy cùng lúc chưa được định nghĩa — chưa có nhu cầu thực tế ở Package 0.2-B1.

**Đã đóng ở v0.2 (không còn là Open Question):** `StructureCurrentView.current_relevant_swing_ref` semantics khi nhiều Swing cùng direction đủ điều kiện đồng thời — resolve đầy đủ bởi total order §6a (đóng C-B1-STR-MAJ-02).

**Đã đóng ở v0.3 (không còn là Open Question):** revision generation nào của một `swing_id` bị `broken_swing_ref` tiêu thụ — resolve đầy đủ bởi canonical reference revision-qualified (đóng D-B1-STR-MAJ-01); so sánh Eligible Swing xuyên nhiều stream — resolve đầy đủ bởi total order 8-tiêu-chí, mỗi tiêu chí có hướng tường minh (đóng D-B1-STR-MAJ-02).
