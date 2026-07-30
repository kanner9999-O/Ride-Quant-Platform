---
id: instrument
title: Instrument
version: "0.1"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-07-30"
last_review: null
next_review: null
---

# Instrument

> **Vai trò của tài liệu này:** Domain Contract đầu tiên của Package 0.2-C1 (Reference Foundation) — định nghĩa **Logical Instrument**, identity venue-neutral của một sản phẩm giao dịch, cộng **TradableListing** (subordinate concept, gắn kết Instrument với một Venue cụ thể). Draft, chưa Approved/Locked. Thuộc capability `market-reference` / context `instrument-venue-reference` (đã đăng ký sẵn từ Package 0.2-A tại [`context-map.yaml`](./context-map.yaml), forward-declared → authored). Đúng [ADR-007](../adr/ADR-007.md): Domain Model **không được hardcode giả định crypto-only** — Instrument là identity trung lập theo asset class, không giả định chỉ có spot crypto.

Instrument **KHÔNG phải** raw venue symbol, KHÔNG phải Candle, KHÔNG phải Strategy/Decision/Risk/Account/Position/Order/Fill, KHÔNG phải live market price. Nó là **identity và metadata tham chiếu, bitemporal, authoritative** cho một sản phẩm giao dịch — venue-neutral ở tầng Logical Instrument, và gắn kết cụ thể với từng Venue qua TradableListing.

**`instrument_id`/`venue_id` là hai identifier đã được MỌI Domain Contract Package 0.2-B tham chiếu trước (`candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`/`context.md`, mỗi nơi `{type: string, required: true, ref: instrument}`/`{..., ref: venue}`) — tài liệu này là nguồn định nghĩa CHÍNH THỨC cho hai identifier đó. KHÔNG đổi tên, KHÔNG đổi shape (`opaque string`) — mọi Domain Contract B-package hiện có tiếp tục hoạt động không cần sửa.**

Instrument bao gồm **hai họ subject riêng biệt, không gộp làm một aggregate**:

1. **Logical Instrument** (`kind: entity`) — identity venue-neutral của sản phẩm giao dịch (ví dụ "BTC/USDT spot" như một khái niệm, không gắn một venue cụ thể nào).
2. **TradableListing** (`kind: entity`, subordinate) — sự gắn kết của MỘT Logical Instrument với MỘT Venue cụ thể; mang venue symbol, price/quantity increment, min quantity/notional, session/calendar reference, listing status. **KHÔNG phải một Domain Contract file riêng ở C1** — subordinate concept trong chính tài liệu này, nhưng có identity/lifecycle/event riêng, tách bạch khỏi Logical Instrument.

Đây là **quyết định thiết kế tường minh** (đóng câu hỏi ownership ở Part E của authoring task): Logical Instrument sở hữu venue-neutral product semantics; TradableListing sở hữu venue-specific trading constraints. Gộp hai khái niệm này vào một aggregate sẽ vi phạm venue-neutral requirement của ADR-007 (một Logical Instrument thường list trên NHIỀU venue, mỗi venue có symbol/tick/lot khác nhau — không thể biểu diễn bằng một identity duy nhất).

**`instrument-registered`/`instrument-metadata-revised`/`instrument-status-changed`/`instrument-fact-invalidated`/`instrument-current-view`/`tradable-listing-created`/`tradable-listing-metadata-revised`/`tradable-listing-status-changed`/`tradable-listing-fact-invalidated`/`tradable-listing-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây. Display name, concept ID, và `event_type` là ba đại lượng khác nhau, không cạnh tranh identity — cùng nguyên tắc `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`/`context.md` đã khóa.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B:** envelope binding cho mọi `*FactInvalidated` (`subject_ref`/`effective_time` kế thừa từ fact bị invalidate, không tự khai báo độc lập); tách bạch **forward-looking revision** (fact mới, effective_time mới, fact cũ vẫn giữ nguyên hợp lệ cho window lịch sử của nó — KHÔNG phải correction) khỏi **correction** (invalidate + replace, đúng khi một fact lịch sử ĐÃ SAI); no-row Current View semantics trước fact đầu tiên, `view_state` chỉ có `VALID`/`PENDING_CORRECTION`; mọi canonical policy identifier chỉ khai báo ĐÚNG MỘT NƠI; opaque identity — không parse `instrument_id`/`venue_id`/`listing_id` để suy diễn business meaning (Chapter 6 §6.8).

## 1. Logical Instrument Subject — `kind: entity`

```yaml
id: instrument
kind: entity
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Identity venue-neutral, ổn định, của một sản phẩm giao dịch — KHÔNG gắn với bất kỳ venue cụ
  thể nào, KHÔNG phải raw venue symbol (ví dụ "BTCUSDT"). Một Logical Instrument là MỘT subject
  liên tục theo scope (giống Structure/Regime/Feature/Context — không có subject mới per
  window/event; metadata thay đổi qua thời gian là thuộc tính của chuỗi fact, không phải subject
  mới).
invariants:
  - "instrument_id resolve deterministic từ scope identity bất biến (base_asset_ref, quote_asset_ref, instrument_type, và contract_expiry_ref khi instrument_type ∈ {FUTURE, OPTION}, xem schema dưới đây) — cùng scope luôn cho cùng instrument_id; khác bất kỳ field scope nào cho instrument_id KHÁC. instrument_id bất biến, KHÔNG tái sử dụng cho một subject khác (Chapter 6 §6.1)."
  - "instrument_id là opaque — domain logic KHÔNG được parse nó để suy diễn base/quote asset, instrument_type, hay bất kỳ business meaning nào (Chapter 6 §6.8); mọi quyết định nghiệp vụ phải dùng field tường minh trong scope."
  - "instrument_id KHÔNG được là raw venue symbol (ví dụ 'BTCUSDT') — venue symbol chỉ tồn tại trong TradableListing (§10), không bao giờ trong Logical Instrument identity."
  - "instrument_type bất biến sau khi subject được đăng ký lần đầu — đổi instrument_type là tạo một Logical Instrument KHÁC (instrument_id khác), không phải mutate subject cũ (một SPOT không bao giờ 'trở thành' một PERPETUAL)."
  - "instrument_id KHÔNG phụ thuộc bất kỳ venue nào — một Logical Instrument có thể có ZERO, MỘT, hoặc NHIỀU TradableListing trên nhiều Venue khác nhau, đồng thời hoặc theo thời gian (§10)."
schema:
  instrument_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  base_asset_ref: {type: string, required: true, description: "external/reference identifier cho base asset — KHÔNG phải một Asset Domain Contract riêng ở C1 (§20, deferred); opaque, không parse"}
  quote_asset_ref: {type: string, required: true, description: "external/reference identifier cho quote/settlement asset — cùng nguyên tắc base_asset_ref"}
  instrument_type: {type: enum, values: [SPOT, PERPETUAL, FUTURE, OPTION], required: true, description: "đóng ở v0.1 — không thêm equities/bonds/other asset class trừ khi Constitution/ADR hiện tại yêu cầu tường minh (§8)"}
  contract_expiry_ref: {type: string, required: false, description: "opaque reference tới thời điểm đáo hạn — REQUIRED khi instrument_type ∈ {FUTURE, OPTION} (đóng góp vào scope identity khi có mặt), PROHIBITED khi instrument_type ∈ {SPOT, PERPETUAL}. Cơ chế resolve cụ thể (calendar/timestamp) deferred (§20)."
  settlement_type: {type: enum, values: [CASH, PHYSICAL], required: false, description: "chỉ có ý nghĩa cho FUTURE/OPTION; N/A cho SPOT/PERPETUAL"}
state_machine:
  initial_state: UNSEEN
  states: [UNSEEN, REGISTERED, ACTIVE, SUSPENDED, RETIRED]
  transitions:
    - {from: UNSEEN, to: REGISTERED, caused_by: InstrumentRegistered}
    - {from: REGISTERED, to: ACTIVE, caused_by: InstrumentStatusChanged}
    - {from: ACTIVE, to: SUSPENDED, caused_by: InstrumentStatusChanged}
    - {from: SUSPENDED, to: ACTIVE, caused_by: InstrumentStatusChanged}
    - {from: ACTIVE, to: RETIRED, caused_by: InstrumentStatusChanged}
    - {from: SUSPENDED, to: RETIRED, caused_by: InstrumentStatusChanged}
    - {from: REGISTERED, to: RETIRED, caused_by: InstrumentStatusChanged}
  terminal_states: [RETIRED]
events_emitted: [InstrumentRegistered, InstrumentMetadataRevised, InstrumentStatusChanged, InstrumentFactInvalidated]
events_consumed: []
commands: []
queries: []
```

**`UNSEEN` là notional initial state** — cùng convention `candle.md`/`swing.md`/`structure.md` đã khóa: không event nào khẳng định "subject đang UNSEEN". **`RETIRED` là terminal** — một Instrument đã retired không quay lại `ACTIVE` (nếu cần giao dịch lại sản phẩm tương tự, đăng ký một `instrument_id` mới — retirement không phải "tạm khóa", nó là kết thúc vòng đời logic).

**`RETIRED` ở tầng Logical Instrument KHÔNG tự động retire mọi TradableListing của nó** — đây là hai lifecycle độc lập (§10); tuy nhiên một invariant liên-subject bắt buộc: **KHÔNG được có TradableListing ở trạng thái `ACTIVE` khi Logical Instrument của nó đã `RETIRED`** (§13 cross-subject invariant).

## 2. Canonical event envelope — áp dụng cho mọi Instrument/TradableListing event (§3–§6, §11–§14)

Mọi event trong tài liệu này là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). Mục này khóa **envelope chung** một lần.

```yaml
envelope:
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2)
  event_contract_ref: {cardinality: required}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}             # khi Ride ghi nhận fact này
  subject_ref: {cardinality: "required — shape canonical, xem dưới. Trên mọi *FactInvalidated (§6, §14), PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate."}
  stream_ref: {cardinality: required}                # Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # Phase 1, chưa author
  correlation_id: {cardinality: "required khi computation thuộc một correlation flow tường minh; optional khi độc lập"}
  causation_refs: {cardinality: "InstrumentRegistered/TradableListingCreated: cardinality zero-or-more (fact gốc, không nhất thiết có causal ancestor authoritative — đăng ký thủ công hoặc từ external reference feed, Phase 1). Mọi event khác (revision/status-change/invalidation): KHÔNG BAO GIỜ rỗng — xem §3–§6, §11–§14."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3"}
  effective_time: {cardinality: "required — semantic khác theo event type, xem §3–§6/§11–§14 cho nội dung cụ thể."}
  market_time: {cardinality: "PROHIBITED — Instrument/TradableListing là reference data authoritative, không phải quan sát trực tiếp venue theo nghĩa market_time (Chapter 5 §5.2)."}
  source_identity: {cardinality: "optional — có mặt khi fact đến từ external reference feed có khả năng retry/redelivery (Chapter 6 §6.6); PROHIBITED khi đăng ký thủ công qua Product Owner/operator workflow (Phase 1, chưa author)."}

subject_ref (Logical Instrument):
  context_id: instrument-venue-reference
  subject_kind: entity
  subject_type: Instrument
  subject_id: <instrument_id — opaque, stable, xem §1>
  scope:
    base_asset_ref: <string>
    quote_asset_ref: <string>
    instrument_type: <SPOT | PERPETUAL | FUTURE | OPTION>
    contract_expiry_ref: <string, optional>

subject_ref (TradableListing, §10):
  context_id: instrument-venue-reference
  subject_kind: entity
  subject_type: TradableListing
  subject_id: <listing_id — opaque, stable, xem §10>
  scope:
    instrument_id: <string>
    venue_id: <string>

event_types:
  InstrumentRegistered: INSTRUMENT_REGISTERED
  InstrumentMetadataRevised: INSTRUMENT_METADATA_REVISED
  InstrumentStatusChanged: INSTRUMENT_STATUS_CHANGED
  InstrumentFactInvalidated: INSTRUMENT_FACT_INVALIDATED
  TradableListingCreated: TRADABLE_LISTING_CREATED
  TradableListingMetadataRevised: TRADABLE_LISTING_METADATA_REVISED
  TradableListingStatusChanged: TRADABLE_LISTING_STATUS_CHANGED
  TradableListingFactInvalidated: TRADABLE_LISTING_FACT_INVALIDATED
```

`stream_ref`/`producer_ref` — Phase 1, chưa tồn tại, cùng nguyên tắc defer xuyên suốt Package 0.2-B.

## 3. `InstrumentRegistered` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: instrument-registered
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE, DUY NHẤT cho việc đăng ký lần đầu một Logical Instrument — thiết lập
  scope identity bất biến (base_asset_ref, quote_asset_ref, instrument_type, contract_expiry_ref
  khi có). KHÔNG dùng cho revision — mọi thay đổi metadata SAU đăng ký dùng
  InstrumentMetadataRevised (§4). Một instrument_id chỉ có ĐÚNG MỘT InstrumentRegistered.
invariants:
  - "Đúng MỘT InstrumentRegistered cho mỗi instrument_id — không đăng ký trùng lặp cho cùng scope identity (base_asset_ref, quote_asset_ref, instrument_type, contract_expiry_ref)."
  - "payload.instrument_id PHẢI khớp đúng subject_ref.subject_id VÀ toàn bộ scope field PHẢI khớp subject_ref.scope."
  - "contract_expiry_ref BẮT BUỘC có mặt khi instrument_type ∈ {FUTURE, OPTION}; CẤM có mặt khi instrument_type ∈ {SPOT, PERPETUAL}."
  - "envelope.effective_time = thời điểm registration record này có hiệu lực làm reference data — mặc định bằng recorded_time trừ khi backfill lịch sử tường minh pin effective_time sớm hơn (§17)."
payload:
  instrument_id: {type: string, required: true}
  base_asset_ref: {type: string, required: true}
  quote_asset_ref: {type: string, required: true}
  instrument_type: {type: enum, values: [SPOT, PERPETUAL, FUTURE, OPTION], required: true}
  contract_expiry_ref: {type: string, required: false}
  settlement_type: {type: enum, values: [CASH, PHYSICAL], required: false}
  display_name: {type: string, required: false, description: "mô tả tiện dụng, KHÔNG phải identity — đổi display_name không tạo instrument_id mới"}
```

## 4. `InstrumentMetadataRevised` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: instrument-metadata-revised
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE cho một thay đổi metadata mô tả (KHÔNG phải scope identity — đổi
  base_asset_ref/quote_asset_ref/instrument_type/contract_expiry_ref là tạo instrument_id khác,
  §1) — ví dụ display_name. **Forward-looking theo mặc định:** một revision mới có
  effective_time MỚI, fact liền trước vẫn hợp lệ nguyên vẹn cho window lịch sử của nó — KHÔNG
  phải correction (đóng "tick size changes historically"-style attack scenario, áp dụng tương tự
  ở TradableListing §12 nơi thực sự có tick/lot). Correction (sửa một fact ĐÃ SAI trong quá khứ)
  dùng InstrumentFactInvalidated + replacement (§6) — hai khái niệm tách bạch tường minh, không
  gộp.
invariants:
  - "envelope.effective_time = thời điểm metadata này bắt đầu có hiệu lực (forward-looking) — KHÁC recorded_time khi biết trước/backfill."
  - "supersedes_fact_ref VẮNG MẶT cho forward-looking revision bình thường (fact liền trước KHÔNG bị phủ định, chỉ 'hết hiệu lực về sau' theo effective_time thứ tự)."
  - "supersedes_fact_ref BẮT BUỘC có mặt CHỈ KHI đây là correction replacement sau một InstrumentFactInvalidated (§6) — dùng đúng cùng nguyên tắc correction lineage §16."
  - "envelope.recorded_time PHẢI muộn hơn hoặc bằng recorded_time của InstrumentRegistered/revision liền trước cho cùng subject."
payload:
  instrument_id: {type: string, required: true}
  display_name: {type: string, required: false}
  classification_tags: {type: array, items: string, required: false, description: "tag mô tả tùy chọn, KHÔNG mang business logic — chỉ query/UI"}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho forward revision bình thường; BẮT BUỘC cho correction replacement — xem invariants và §16"}
```

## 5. `InstrumentStatusChanged` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: instrument-status-changed
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE cho một operational status transition của Logical Instrument (§1
  state_machine) — REGISTERED→ACTIVE, ACTIVE↔SUSPENDED, (REGISTERED|ACTIVE|SUSPENDED)→RETIRED.
  RETIRED là terminal — không transition nào rời khỏi RETIRED.
invariants:
  - "new_status PHẢI là một transition hợp lệ theo state_machine §1 từ status hiện tại (derived bằng fold recorded_time)."
  - "new_status = RETIRED KHÔNG được có transition tiếp theo nào cho cùng instrument_id."
  - "envelope.effective_time = thời điểm status transition này thực sự có hiệu lực (có thể khác recorded_time nếu biết trước lịch retire, ví dụ future-dated retirement announcement — §11)."
payload:
  instrument_id: {type: string, required: true}
  new_status: {type: enum, values: [ACTIVE, SUSPENDED, RETIRED], required: true}
  reason: {type: string, required: false}
```

## 6. `InstrumentFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2 — `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: instrument-fact-invalidated
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Phủ định MỘT InstrumentMetadataRevised hoặc InstrumentStatusChanged lịch sử cụ thể ĐÃ SAI
  (ví dụ nhập nhầm effective_time, hoặc metadata ghi sai) — thuần túy ghi nhận "fact này không
  còn hợp lệ", KHÔNG tự nó tuyên bố giá trị mới. **KHÔNG dùng cho forward-looking change** (đó
  là InstrumentMetadataRevised/InstrumentStatusChanged bình thường, không phải invalidation) —
  phân biệt tường minh: correction sửa một SAI SÓT trong quá khứ; revision là một THAY ĐỔI THẬT
  xảy ra theo thời gian. InstrumentRegistered KHÔNG BAO GIỜ là target hợp lệ (đóng registration
  sai là edge case ngoài phạm vi B4/C1, §20).
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref (F) — cùng context_id, subject_kind, subject_type, subject_id, VÀ toàn bộ scope."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref (F)."
  - "payload.invalidated_fact_ref PHẢI trỏ một InstrumentMetadataRevised hoặc InstrumentStatusChanged — KHÔNG BAO GIỜ một InstrumentRegistered hay một InstrumentFactInvalidated khác."
  - "invalidated_fact_ref PHẢI trỏ một fact CHƯA từng nhận InstrumentFactInvalidated khác — một fact chỉ bị invalidate đúng một lần."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 7. `InstrumentCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §3–§6.

**Canonical decision — no-row trước khi có fact đầu tiên (đúng `regime.md`/`feature.md`/`context.md` §5):**

```text
Trước khi InstrumentRegistered tồn tại cho một instrument_id:
  → KHÔNG có InstrumentCurrentView row nào tồn tại
  → GetCurrentInstrument trả về NOT_FOUND / ABSENT
```

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION` — **không có `UNAVAILABLE`**.

```yaml
id: instrument-current-view
kind: read_model
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Projection tiện dụng: metadata/status "hiện tại" của một Logical Instrument, rebuild được từ
  §3–§6. KHÔNG authoritative — mọi input cho Domain Contract khác PHẢI dùng authoritative event
  stream (`ref: instrument`), KHÔNG BAO GIỜ dùng view này (I-12, Chapter 7 §7.4).
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho bất kỳ Domain Contract khác hay Decision — chỉ query/UI."
  - "view_state PHẢI đúng: VALID khi lineage head hợp lệ, không có invalidation visible; PENDING_CORRECTION khi lineage head có invalidation visible nhưng replacement CHƯA visible."
schema:
  instrument_id: {type: string, required: true}
  scope: {base_asset_ref: string, quote_asset_ref: string, instrument_type: string, contract_expiry_ref: string, required: true}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  current_status: {type: enum, values: [REGISTERED, ACTIVE, SUSPENDED, RETIRED], required: false, description: "chỉ có mặt khi view_state = VALID"}
  display_name: {type: string, required: false}
  last_recorded_time: timestamp
queries: [GetCurrentInstrument, GetInstrumentHistory]
```

## 8. Instrument types — closed enum

```text
SPOT       — giao ngay, không đáo hạn, không đòn bẩy structural
PERPETUAL  — hợp đồng vĩnh viễn (funding-rate mechanism), không đáo hạn
FUTURE     — hợp đồng tương lai, có contract_expiry_ref bắt buộc
OPTION     — hợp đồng quyền chọn, có contract_expiry_ref bắt buộc
```

**Đóng ở v0.1** — không thêm equities/bonds/forex spot pairs hay asset class khác trừ khi Constitution/ADR hiện tại yêu cầu tường minh (đúng [ADR-007](../adr/ADR-007.md): kiến trúc chừa chỗ multi-asset, nhưng KHÔNG mở rộng ngay). `OPTION` enum value được **reserve** ở v0.1 — schema-specific cho option (strike price, option type CALL/PUT) **deferred** (§20), chưa có nhu cầu thực tế ở C1.

## 9. Required distinction — Logical Instrument / Venue Listing / Venue Symbol

```text
Logical Instrument:  BTC/USDT spot                      — venue-neutral identity (§1)
Venue Listing:       Binance listing của BTC/USDT spot   — TradableListing (§10)
Venue Symbol:        BTCUSDT                              — field bên trong TradableListing (§10), KHÔNG BAO GIỜ là instrument_id
```

**Ví dụ trên chỉ minh họa — KHÔNG hardcode Binance hay crypto vào contract này** (đúng ADR-007). Ba khái niệm này **không được gộp thành một identity** — một Logical Instrument list trên nhiều Venue, mỗi Venue Listing có một Venue Symbol riêng, có thể khác nhau qua thời gian trên cùng một venue (§12 — venue symbol changes).

## 10. TradableListing — `kind: entity` (subordinate concept)

**Quyết định ownership tường minh:** TradableListing là **subordinate concept nằm trong `instrument.md`** (không phải file Domain Contract riêng ở C1) — nhưng có identity, lifecycle, và event riêng, tách bạch khỏi Logical Instrument (§1). Lý do: TradableListing luôn tồn tại TRONG BỐI CẢNH một Logical Instrument cụ thể (không có TradableListing độc lập, mồ côi) — nhưng semantic của nó (venue symbol, tick/lot, session reference, listing status) là venue-specific, khác về bản chất so với venue-neutral Instrument identity (§9).

```yaml
id: tradable-listing
kind: entity
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Sự gắn kết của MỘT Logical Instrument với MỘT Venue — mang venue symbol, price/quantity
  increment, min quantity/notional, session/calendar reference, listing status. Subject liên
  tục theo scope (instrument_id, venue_id, listing_id) — không có subject mới per revision.
invariants:
  - "listing_id resolve deterministic từ ĐÚNG BA field qualifying scope: instrument_id, venue_id, listing_id — listing_id là opaque, KHÔNG derive tự động chỉ từ (instrument_id, venue_id), để cho phép một lần relist SAU KHI delist trước đó là một TradableListing subject HOÀN TOÀN MỚI (không phải reactivate subject cũ, đối xứng nguyên tắc swing_revision generation của swing.md §1a)."
  - "instrument_id PHẢI trỏ một Logical Instrument đã InstrumentRegistered (§3) — không tạo TradableListing cho một instrument_id chưa tồn tại."
  - "venue_id PHẢI trỏ một Venue đã VenueRegistered (venue.md §3) — không tạo TradableListing cho một venue_id chưa tồn tại."
  - "instrument_id, venue_id, listing_id bất biến sau khi subject được tạo lần đầu — đổi bất kỳ field nào tạo một TradableListing subject KHÁC."
  - "TẠI MỘT THỜI ĐIỂM, tối đa MỘT TradableListing ở trạng thái ACTIVE cho cùng cặp (instrument_id, venue_id) — cấm hai listing đang active đồng thời cho cùng cặp (đóng attack scenario 'duplicate listing identity'). Một listing cũ phải DELISTED trước khi một listing_id mới cho cùng cặp có thể trở thành ACTIVE."
  - "KHÔNG được ACTIVE khi Logical Instrument của nó đã RETIRED (§1 cross-subject invariant)."
schema:
  listing_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  instrument_id: {type: string, required: true, ref: instrument}
  venue_id: {type: string, required: true, ref: venue}
state_machine:
  initial_state: UNSEEN
  states: [UNSEEN, ACTIVE, SUSPENDED, DELISTED]
  transitions:
    - {from: UNSEEN, to: ACTIVE, caused_by: TradableListingCreated}
    - {from: ACTIVE, to: SUSPENDED, caused_by: TradableListingStatusChanged}
    - {from: SUSPENDED, to: ACTIVE, caused_by: TradableListingStatusChanged}
    - {from: ACTIVE, to: DELISTED, caused_by: TradableListingStatusChanged}
    - {from: SUSPENDED, to: DELISTED, caused_by: TradableListingStatusChanged}
  terminal_states: [DELISTED]
events_emitted: [TradableListingCreated, TradableListingMetadataRevised, TradableListingStatusChanged, TradableListingFactInvalidated]
events_consumed: []
commands: []
queries: []
```

**KHÔNG chứa:** credential, execution state, order/fill/position (§18).

## 11. `TradableListingCreated` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: tradable-listing-created
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE, DUY NHẤT cho việc tạo một TradableListing — thiết lập scope identity bất
  biến (instrument_id, venue_id, listing_id) và mutable metadata ban đầu (venue symbol,
  increment, min quantity/notional, session reference).
invariants:
  - "Đúng MỘT TradableListingCreated cho mỗi listing_id."
  - "payload.listing_id/instrument_id/venue_id PHẢI khớp đúng subject_ref.subject_id/scope."
  - "causation_refs PHẢI trỏ InstrumentRegistered của instrument_id VÀ VenueRegistered (venue.md §3) của venue_id — chứng minh cả hai subject đã tồn tại trước khi listing được tạo."
  - "envelope.effective_time = thời điểm listing này thực sự bắt đầu tradable (có thể khác recorded_time nếu backfill/future-dated launch)."
payload:
  listing_id: {type: string, required: true}
  instrument_id: {type: string, required: true}
  venue_id: {type: string, required: true}
  venue_symbol: {type: string, required: true, description: "raw symbol venue dùng, ví dụ 'BTCUSDT' — CHỈ tồn tại ở đây, KHÔNG BAO GIỜ leak vào instrument_id (§9)"}
  price_increment: {type: decimal, required: true, description: "tick size — I-9, decimal không float"}
  quantity_increment: {type: decimal, required: true, description: "lot size"}
  min_quantity: {type: decimal, required: false}
  min_notional: {type: decimal, required: false}
  session_calendar_ref: {type: string, required: true, description: "reference tới trading calendar/session policy của Venue (venue.md §8) — venue-neutral, không hardcode 24/7"}
```

## 12. `TradableListingMetadataRevised` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: tradable-listing-metadata-revised
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE cho một thay đổi metadata của TradableListing — ví dụ venue symbol đổi
  (rebrand), tick size đổi, lot size đổi. **Forward-looking theo mặc định** — cùng nguyên tắc
  InstrumentMetadataRevised (§4): fact liền trước vẫn hợp lệ cho window lịch sử của nó (đóng
  "tick size changes historically" — Historical Replay dùng ĐÚNG price_increment có hiệu lực
  TẠI thời điểm computation, không phải giá trị hiện tại — §17). Correction dùng
  TradableListingFactInvalidated (§14).
invariants:
  - "envelope.effective_time = thời điểm metadata mới bắt đầu có hiệu lực (forward-looking)."
  - "supersedes_fact_ref VẮNG MẶT cho forward-looking revision bình thường; BẮT BUỘC CHỈ KHI là correction replacement sau TradableListingFactInvalidated (§14, §16)."
  - "Ít nhất một field mutable (venue_symbol/price_increment/quantity_increment/min_quantity/min_notional/session_calendar_ref) PHẢI thay đổi so với fact liền trước — không phát fact trùng lặp không mang thông tin mới."
payload:
  listing_id: {type: string, required: true}
  venue_symbol: {type: string, required: false}
  price_increment: {type: decimal, required: false}
  quantity_increment: {type: decimal, required: false}
  min_quantity: {type: decimal, required: false}
  min_notional: {type: decimal, required: false}
  session_calendar_ref: {type: string, required: false}
  supersedes_fact_ref: {type: event_record_ref, required: false}
```

## 13. `TradableListingStatusChanged` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: tradable-listing-status-changed
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE cho một operational status transition của TradableListing (§10
  state_machine) — ACTIVE↔SUSPENDED, (ACTIVE|SUSPENDED)→DELISTED. DELISTED là terminal. Venue có
  thể suspend MỘT listing (ví dụ maintenance riêng cho cặp đó) mà KHÔNG ảnh hưởng Logical
  Instrument hay các TradableListing khác của cùng Instrument trên Venue khác (đóng attack
  scenario "venue suspends one listing but not the logical instrument").
invariants:
  - "new_status PHẢI là transition hợp lệ theo state_machine §10."
  - "new_status = DELISTED KHÔNG được có transition tiếp theo cho cùng listing_id — một relist dùng listing_id MỚI (§10 invariant)."
  - "new_status = ACTIVE CẤM khi Logical Instrument tương ứng đã RETIRED tại effective_time đó (§1 cross-subject invariant)."
payload:
  listing_id: {type: string, required: true}
  new_status: {type: enum, values: [ACTIVE, SUSPENDED, DELISTED], required: true}
  reason: {type: string, required: false}
```

## 14. `TradableListingFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2 — `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: tradable-listing-fact-invalidated
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Phủ định MỘT TradableListingMetadataRevised hoặc TradableListingStatusChanged lịch sử cụ thể
  ĐÃ SAI — cùng nguyên tắc InstrumentFactInvalidated (§6). TradableListingCreated KHÔNG BAO GIỜ
  là target hợp lệ.
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref."
  - "invalidated_fact_ref PHẢI trỏ một TradableListingMetadataRevised hoặc TradableListingStatusChanged, CHƯA từng nhận invalidation khác."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 15. `TradableListingCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §11–§14.

**Canonical decision — no-row trước khi có fact đầu tiên:**

```text
Trước khi TradableListingCreated tồn tại cho một listing_id:
  → KHÔNG có TradableListingCurrentView row nào tồn tại
  → GetCurrentListing trả về NOT_FOUND / ABSENT
```

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION`.

```yaml
id: tradable-listing-current-view
kind: read_model
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Projection tiện dụng: metadata/status "hiện tại" của một TradableListing (venue symbol,
  increment, listing status), rebuild được từ §11–§14. KHÔNG authoritative — mọi input cho
  Domain Contract khác PHẢI dùng authoritative event stream, KHÔNG BAO GIỜ dùng view này
  (I-12, Chapter 7 §7.4).
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho bất kỳ Domain Contract khác hay Decision — chỉ query/UI."
  - "view_state PHẢI đúng: VALID khi lineage head hợp lệ, không invalidation visible; PENDING_CORRECTION khi có invalidation visible nhưng replacement CHƯA visible."
schema:
  listing_id: {type: string, required: true}
  scope: {instrument_id: string, venue_id: string, required: true}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  current_status: {type: enum, values: [ACTIVE, SUSPENDED, DELISTED], required: false, description: "chỉ có mặt khi view_state = VALID"}
  venue_symbol: {type: string, required: false}
  price_increment: {type: decimal, required: false}
  quantity_increment: {type: decimal, required: false}
  last_recorded_time: timestamp
queries: [GetCurrentListing, GetListingHistory]
```

## 16. Correction lineage (cả hai họ subject)

Correction lineage scoped chính xác theo `(subject_id, effective_time)` — mỗi effective_time-slice có chuỗi lineage RIÊNG.

```text
InstrumentMetadataRevised F1 (hoặc TradableListingMetadataRevised/StatusChanged)
  → *FactInvalidated targeting F1
  → replacement (cùng event type), supersedes_fact_ref = F1

Correction tiếp theo:
F2
  → *FactInvalidated targeting F2
  → F3, supersedes_fact_ref = F2   (KHÔNG được supersedes_fact_ref = F1 — cấm nhảy cóc)
```

**Mười invariant bắt buộc** (đã pin tại §4–§6, §12–§14, tổng hợp lại đây):

1. Original fact (`InstrumentRegistered`/`TradableListingCreated`) không có `supersedes_fact_ref`, không bao giờ là target của `*FactInvalidated`.
2. Replacement fact (correction) bắt buộc có `supersedes_fact_ref`; forward-looking revision bình thường thì không.
3. Replacement dùng đúng cùng subject và cùng `effective_time` với fact bị supersede.
4. Replacement PHẢI supersede đúng lineage head hiện tại.
5. Replacement không được nhảy cóc qua một head trung gian.
6. Một fact bị invalidate có **tối đa một** replacement authoritative trực tiếp — cấm fork.
7. Replacement không được "visible" (`recorded_time`) trước invalidation tương ứng.
8. Mọi lineage member lịch sử giữ nguyên trong log — append-only (I-3), không mutate.
9. Một fact đã invalidate **không bao giờ** bị tái sử dụng ngầm — Current View (§7 cho Instrument, §15 cho TradableListing) phải loại trừ nó tường minh.
10. **Forward-looking revision KHÔNG BAO GIỜ dùng cơ chế invalidation** — chỉ correction (sửa sai sót thực sự trong quá khứ) mới dùng `*FactInvalidated` + replacement.

## 17. Time semantics và bitemporal correctness

```text
effective_time    — khi fact này THỰC SỰ có hiệu lực làm reference data (forward-looking cho revision, hoặc lịch sử cho correction)
recorded_time     — khi Ride ghi nhận fact này (bắt buộc, mọi event — envelope §2)
market_time       — PROHIBITED (§2)
```

**Không dùng `event_time`.**

**Historical Replay PHẢI dùng đúng metadata có hiệu lực TẠI computation cursor, không phải giá trị hiện tại** — ví dụ: Backtest tại thời điểm T dùng `price_increment` có `effective_time <= T` MỚI NHẤT tại T, KHÔNG dùng `price_increment` hiện tại của TradableListing (đóng attack scenario "current metadata accidentally used for historical replay", "tick size changes historically"). Selection algorithm: role-specific "latest valid fact với `effective_time <= cursor` VÀ `recorded_time <= replay cursor`" — cùng nguyên tắc recorded-time-visibility + effective-time-eligibility đã khóa ở `feature.md` §12/`context.md` §14 (không look-ahead).

**Correction visibility:** `*FactInvalidated` và replacement đều có `recorded_time` mới; replay tại cursor trước đó chỉ thấy fact gốc (đóng attack scenario "replay before metadata correction", "correction visible after replay cursor" — correction KHÔNG BAO GIỜ visible cho một replay cursor trước recorded_time của chính correction đó, kể cả khi effective_time của correction rơi vào quá khứ xa hơn).

## 18. Prohibitions

**Instrument (Logical Instrument) KHÔNG được sở hữu:** live market price; Candle; Strategy; Decision; Risk; Account; Position; Order; Fill; execution status.

**TradableListing KHÔNG được chứa:** credential; execution state; Order/Fill/Position semantics (đóng attack scenario "Order/Fill/Position semantics accidentally introduced").

## 19. Venue & asset-class neutrality

Đúng [ADR-007](../adr/ADR-007.md): KHÔNG giả định crypto-only, KHÔNG giả định 24/7 (session/calendar reference luôn tường minh qua `venue.md` §8, không hardcode "00:00–24:00 liên tục" — đóng attack scenario "crypto 24/7 assumption"). Một Logical Instrument có thể có **nhiều TradableListing đồng thời trên nhiều Venue** (đóng "same logical instrument listed on two venues"), và **nhiều variant khác `instrument_type` cho cùng underlying** (ví dụ BTC/USDT SPOT và BTC-PERPETUAL là HAI `instrument_id` khác nhau, không phải hai state của cùng một subject — đóng "one instrument has spot and perpetual variants").

## 20. Ngoài phạm vi — defer

**Deferred tường minh, không author ở C1:** Asset như một Domain Contract riêng (chỉ dùng `base_asset_ref`/`quote_asset_ref` opaque); OPTION-specific schema (strike price, option type CALL/PUT); cơ chế resolve cụ thể `contract_expiry_ref`/`session_calendar_ref` (calendar service, Phase 1); `stream_ref`/`producer_ref` (Phase 1); cơ chế đăng ký Instrument/Listing cụ thể (thủ công qua Product Owner, hay tự động từ external reference feed — cả hai đều hợp lệ theo envelope §2, không chọn một cách duy nhất); Account/Strategy/Decision/Risk/Order/Fill/Position/Execution/Trade Intent/Execution Intent/Replay Event (Package 0.2-C2–C7, chưa authorize).

**Out of scope theo ranh giới domain:** live market price, Candle semantics (thuộc `candle.md`), bất kỳ business decision nào — vi phạm trực tiếp định nghĩa Instrument nếu thêm vào (§18).

## 21. Open questions ngoài phạm vi

- Cơ chế chính xác để một `InstrumentRegistered` sai (ví dụ base_asset_ref/instrument_type nhập nhầm ngay từ đầu) được xử lý — hiện tại `InstrumentFactInvalidated` KHÔNG cho phép target `InstrumentRegistered` (§6 invariant); một registration sai cần retire instrument_id đó (`InstrumentStatusChanged: RETIRED` với `reason` giải thích) và đăng ký `instrument_id` mới đúng. Chưa quyết định liệu đây có cần một cơ chế riêng — author-level ambiguity, không đóng OQ-002/OQ-003.
- `contract_expiry_ref`/`session_calendar_ref` hiện là opaque string reference — chưa có Domain Contract hay registry cụ thể nào định nghĩa format/resolve mechanism. Cần quyết định khi Package 0.2-C có nhu cầu thực tế đầu tiên (đối xứng ghi chú các Domain Contract trước).
