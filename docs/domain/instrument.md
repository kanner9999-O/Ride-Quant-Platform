---
id: instrument
title: Instrument
version: "0.3"
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

Đây là **quyết định thiết kế tường minh**: Logical Instrument sở hữu venue-neutral product semantics; TradableListing sở hữu venue-specific trading constraints. Gộp hai khái niệm này vào một aggregate sẽ vi phạm venue-neutral requirement của ADR-007 (một Logical Instrument thường list trên NHIỀU venue, mỗi venue có symbol/tick/lot khác nhau — không thể biểu diễn bằng một identity duy nhất).

Cộng **`ActiveListingReservation`** (`kind: entity`, pair-scoped, §16) — authority subject riêng, độc lập TradableListing, xác lập deterministic listing nào đang ACTIVE cho một cặp (instrument_id, venue_id).

**`instrument-registered`/`instrument-metadata-revised`/`instrument-status-changed`/`instrument-fact-invalidated`/`instrument-current-view`/`tradable-listing-created`/`tradable-listing-metadata-revised`/`tradable-listing-status-changed`/`tradable-listing-fact-invalidated`/`tradable-listing-current-view`/`active-listing-reserved`/`active-listing-reservation-released`/`active-listing-activation-rejected` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây. Display name, concept ID, và `event_type` là ba đại lượng khác nhau, không cạnh tranh identity — cùng nguyên tắc `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`/`context.md` đã khóa.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B:** envelope binding cho mọi `*FactInvalidated` (`subject_ref`/`effective_time` kế thừa từ fact bị invalidate, không tự khai báo độc lập); tách bạch **forward-looking revision** (fact mới, effective_time mới, fact cũ vẫn giữ nguyên hợp lệ cho window lịch sử của nó — KHÔNG phải correction) khỏi **correction** (invalidate + replace, đúng khi một fact lịch sử ĐÃ SAI); no-row Current View semantics trước fact đầu tiên, `view_state` chỉ có `VALID`/`PENDING_CORRECTION`; mọi canonical policy identifier chỉ khai báo ĐÚNG MỘT NƠI; opaque identity — không parse `instrument_id`/`venue_id`/`listing_id` để suy diễn business meaning (Chapter 6 §6.8).

**v0.2 — ChatGPT Review A narrow correction, đóng `RA-C1-MAJ-01`/`RA-C1-MAJ-02`/`RA-C1-MAJ-03`:** (a) `RA-C1-MAJ-01` — scope identity v0.1 (base/quote/type/expiry) không đủ discriminate cho derivatives; thêm `instrument_identity_ref`; `OPTION` gỡ khỏi enum active, `RESERVED_NOT_AUTHORED` (§8); `settlement_type` bắt buộc tường minh cho FUTURE/PERPETUAL. (b) `RA-C1-MAJ-02` — pin canonical `revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET` (§17). (c) `RA-C1-MAJ-03` — pin canonical `initial_fact_correction_policy: INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES` (§17, §19).

**v0.3 — Independent Review B narrow correction, đóng `IRB-C1-MAJ-01`/`IRB-C1-MAJ-02`/`IRB-C1-MAJ-03`/`IRB-C1-MAJ-04`:** (a) `IRB-C1-MAJ-01` — `PENDING_CORRECTION` v0.2 không phân biệt "chờ replacement tạm thời" với "vĩnh viễn invalid do scope error"; thêm discriminator đóng `pending_correction_class` (`AWAITING_SAME_SUBJECT_REPLACEMENT`/`TERMINAL_SCOPE_INVALIDATION`), áp dụng thống nhất `InstrumentCurrentView`/`TradableListingCurrentView`/`VenueCurrentView` (§19). (b) `IRB-C1-MAJ-02` — TradableListing eligibility v0.2 chỉ cấm ACTIVE khi Instrument RETIRED, KHÔNG đối xứng cho Venue RETIRED; v0.3 thêm invariant đối xứng tại §10/§11/§13, cộng derived `eligibility_state` tại `TradableListingCurrentView` (§15) — KHÔNG fabricate authoritative status event. (c) `IRB-C1-MAJ-03` — "tối đa một ACTIVE listing per pair" thiếu cross-stream authority boundary; thêm `ActiveListingReservation` pair-scoped subject + `ActiveListingReserved`/`ActiveListingReservationReleased`/`ActiveListingActivationRejected` (§16), pin `active_listing_arbitration_policy: PAIR_SCOPED_AUTHORITATIVE_RESERVATION` (§17), không automatic promotion. (d) `IRB-C1-MAJ-04` — status fold v0.2 mô tả mơ hồ ("derived bằng fold recorded_time"); pin canonical `status_fold_order_policy: RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER` (§17), thuật toán 5-phase tường minh tại §7 Bước 3 (áp dụng cho Instrument/TradableListing/Venue status). Narrow correction — không redesign toàn package, `instrument_id`/`venue_id`/`listing_id` không đổi tên/shape.

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
  - "instrument_id resolve deterministic từ TOÀN BỘ scope identity bất biến: instrument_identity_ref, base_asset_ref, quote_asset_ref, instrument_type, contract_expiry_ref (khi FUTURE), settlement_type (khi FUTURE/PERPETUAL) — cùng scope luôn cho cùng instrument_id; khác bất kỳ field scope nào (kể cả CHỈ khác instrument_identity_ref, dù các field mô tả còn lại giống hệt) cho instrument_id KHÁC (đóng RA-C1-MAJ-01). instrument_id bất biến, KHÔNG tái sử dụng cho một subject khác (Chapter 6 §6.1)."
  - "instrument_identity_ref là discriminator opaque, KHÔNG derive từ base_asset_ref/quote_asset_ref/instrument_type/contract_expiry_ref/settlement_type — trách nhiệm đảm bảo hai Logical Instrument kinh tế khác nhau có instrument_identity_ref khác nhau thuộc về registration authority bên ngoài (external reference feed hoặc Product Owner/operator workflow, §23 deferred); Domain Contract KHÔNG tự sinh giá trị này. Hai fact có base/quote/type/expiry/settlement giống hệt nhưng instrument_identity_ref khác nhau là HAI Logical Instrument hợp lệ, khác nhau (đóng attack scenario 'two derivative products with otherwise similar descriptive fields')."
  - "instrument_id là opaque — domain logic KHÔNG được parse nó để suy diễn base/quote asset, instrument_type, hay bất kỳ business meaning nào (Chapter 6 §6.8); mọi quyết định nghiệp vụ phải dùng field tường minh trong scope."
  - "instrument_id KHÔNG được là raw venue symbol (ví dụ 'BTCUSDT') — venue symbol chỉ tồn tại trong TradableListing (§10), không bao giờ trong Logical Instrument identity."
  - "Toàn bộ scope field (instrument_identity_ref, base_asset_ref, quote_asset_ref, instrument_type, contract_expiry_ref, settlement_type) bất biến sau khi subject được đăng ký lần đầu — đổi bất kỳ field nào là tạo một Logical Instrument KHÁC (instrument_id khác), không phải mutate subject cũ (một SPOT không bao giờ 'trở thành' một PERPETUAL; một cash-settled future không bao giờ 'trở thành' physically-settled)."
  - "instrument_id KHÔNG phụ thuộc bất kỳ venue nào — một Logical Instrument có thể có ZERO, MỘT, hoặc NHIỀU TradableListing trên nhiều Venue khác nhau, đồng thời hoặc theo thời gian (§10)."
schema:
  instrument_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  instrument_identity_ref: {type: string, required: true, description: "Canonical external/reference identity cho economic instrument này. Opaque, KHÔNG parse bởi domain logic. Bất biến trong suốt vòng đời Logical Instrument. Hai instrument kinh tế khác nhau PHẢI có giá trị khác nhau — đóng RA-C1-MAJ-01, xem invariants."}
  base_asset_ref: {type: string, required: true, description: "external/reference identifier cho base asset — KHÔNG phải một Asset Domain Contract riêng ở C1 (§23, deferred); opaque, không parse; field mô tả, KHÔNG còn một mình gánh global uniqueness (đóng RA-C1-MAJ-01)"}
  quote_asset_ref: {type: string, required: true, description: "external/reference identifier cho quote/settlement asset — cùng nguyên tắc base_asset_ref"}
  instrument_type: {type: enum, values: [SPOT, PERPETUAL, FUTURE], required: true, description: "đóng ở v0.2 — OPTION RESERVED_NOT_AUTHORED (§8); không thêm equities/bonds/other asset class trừ khi Constitution/ADR hiện tại yêu cầu tường minh"}
  contract_expiry_ref: {type: string, required: false, description: "opaque reference tới thời điểm đáo hạn — REQUIRED khi instrument_type = FUTURE, PROHIBITED khi instrument_type ∈ {SPOT, PERPETUAL}. Cơ chế resolve cụ thể (calendar/timestamp) deferred (§23)."}
  settlement_type: {type: enum, values: [CASH, PHYSICAL], required: false, description: "REQUIRED (explicit) khi instrument_type ∈ {FUTURE, PERPETUAL} — đóng RA-C1-MAJ-01 (ví dụ USDT-margined vs coin-margined perpetual, cash-settled vs physically-settled future là các Logical Instrument kinh tế KHÁC nhau); PROHIBITED khi instrument_type = SPOT."
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

**`RETIRED` ở tầng Logical Instrument KHÔNG tự động retire mọi TradableListing của nó** — đây là hai lifecycle độc lập (§10); tuy nhiên một invariant liên-subject bắt buộc, ĐỐI XỨNG cho cả hai parent: **KHÔNG được có TradableListing ở trạng thái `ACTIVE` khi Logical Instrument HOẶC Logical Venue (`venue.md` §1) của nó đã `RETIRED`** (§10/§11/§13 cross-subject invariant, v0.3 đóng `IRB-C1-MAJ-02` — v0.2 chỉ enforce phía Instrument, không đối xứng phía Venue). Một listing thỏa invariant này TẠI THỜI ĐIỂM activation event nhưng có parent RETIRED SAU đó **KHÔNG** bị retroactively invalidate — event lịch sử giữ nguyên authoritative; `TradableListingCurrentView` derive `eligibility_state` riêng cho mục đích read-model (§15).

## 2. Canonical event envelope — áp dụng cho mọi Instrument/TradableListing/ActiveListingReservation event (§3–§6, §11–§14, §16)

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
  causation_refs: {cardinality: "InstrumentRegistered/TradableListingCreated ORIGINAL (không supersedes_fact_ref): zero-or-more (fact gốc, không nhất thiết có causal ancestor authoritative — đăng ký thủ công hoặc từ external reference feed, Phase 1). InstrumentRegistered/TradableListingCreated REPLACEMENT (có supersedes_fact_ref, §19): KHÔNG BAO GIỜ rỗng, PHẢI chứa chính InstrumentFactInvalidated/TradableListingFactInvalidated đang được supersede. Mọi event khác (revision/status-change/invalidation/reservation): KHÔNG BAO GIỜ rỗng — xem §3–§6, §11–§14, §16."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3. Một InstrumentRegistered cho SUBJECT MỚI (sau một SCOPE_ERROR correction, §19) CÓ THỂ tham chiếu non-causal tới InstrumentFactInvalidated của subject cũ để truy vết, nhưng KHÔNG bắt buộc và KHÔNG phải causal ancestor. ActiveListingActivationRejected (§16) NÊN tham chiếu non-causal tới ActiveListingReserved đang HELD hiện tại."}
  effective_time: {cardinality: "required — semantic khác theo event type, xem §3–§6/§11–§14/§16 cho nội dung cụ thể."}
  market_time: {cardinality: "PROHIBITED — Instrument/TradableListing/ActiveListingReservation là reference data authoritative, không phải quan sát trực tiếp venue theo nghĩa market_time (Chapter 5 §5.2)."}
  source_identity: {cardinality: "optional — có mặt khi fact đến từ external reference feed có khả năng retry/redelivery (Chapter 6 §6.6); PROHIBITED khi đăng ký thủ công qua Product Owner/operator workflow (Phase 1, chưa author)."}

subject_ref (Logical Instrument):
  context_id: instrument-venue-reference
  subject_kind: entity
  subject_type: Instrument
  subject_id: <instrument_id — opaque, stable, xem §1>
  scope:
    instrument_identity_ref: <string>
    base_asset_ref: <string>
    quote_asset_ref: <string>
    instrument_type: <SPOT | PERPETUAL | FUTURE>
    contract_expiry_ref: <string, optional>
    settlement_type: <CASH | PHYSICAL, optional>

subject_ref (TradableListing, §10):
  context_id: instrument-venue-reference
  subject_kind: entity
  subject_type: TradableListing
  subject_id: <listing_id — opaque, stable, xem §10>
  scope:
    instrument_id: <string>
    venue_id: <string>

subject_ref (ActiveListingReservation, §16):
  context_id: instrument-venue-reference
  subject_kind: entity
  subject_type: ActiveListingReservation
  subject_id: <reservation_id — opaque, deterministic từ (instrument_id, venue_id), xem §16>
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
  ActiveListingReserved: ACTIVE_LISTING_RESERVED
  ActiveListingReservationReleased: ACTIVE_LISTING_RESERVATION_RELEASED
  ActiveListingActivationRejected: ACTIVE_LISTING_ACTIVATION_REJECTED
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
  Fact AUTHORITATIVE cho việc đăng ký một Logical Instrument — thiết lập scope identity bất biến
  (instrument_identity_ref, base_asset_ref, quote_asset_ref, instrument_type,
  contract_expiry_ref, settlement_type) VÀ mutable metadata ban đầu (display_name). Dùng cho CẢ
  HAI trường hợp (v0.2, đóng RA-C1-MAJ-03): (a) **original registration** — lần đăng ký đầu
  tiên cho instrument_id đó, KHÔNG có supersedes_fact_ref; (b) **same-scope correction
  replacement** — sau một InstrumentFactInvalidated target chính registration này vì mutable
  metadata (ví dụ display_name) ghi sai, CÙNG scope identity, CÓ supersedes_fact_ref (§19). KHÔNG
  dùng cho forward-looking metadata change (đó là InstrumentMetadataRevised, §4).
invariants:
  - "Tại một thời điểm, đúng MỘT VALID registration lineage head cho mỗi instrument_id — KHÔNG phải 'đúng một event record duy nhất mãi mãi' (đóng RA-C1-MAJ-03, xem §19 cho correction policy đầy đủ). Lineage head là fact chưa bị invalidate, hoặc là replacement mới nhất chưa bị invalidate."
  - "payload.instrument_id PHẢI khớp đúng subject_ref.subject_id VÀ toàn bộ scope field PHẢI khớp subject_ref.scope."
  - "contract_expiry_ref BẮT BUỘC có mặt khi instrument_type = FUTURE; CẤM có mặt khi instrument_type ∈ {SPOT, PERPETUAL}."
  - "settlement_type BẮT BUỘC có mặt khi instrument_type ∈ {FUTURE, PERPETUAL}; CẤM có mặt khi instrument_type = SPOT (đóng RA-C1-MAJ-01)."
  - "supersedes_fact_ref VẮNG MẶT cho original registration; BẮT BUỘC cho same-scope correction replacement — khi có mặt, TOÀN BỘ scope field (instrument_identity_ref, base_asset_ref, quote_asset_ref, instrument_type, contract_expiry_ref, settlement_type) PHẢI GIỐNG HỆT fact bị supersede (nếu scope khác, đây KHÔNG phải correction hợp lệ — phải đăng ký subject MỚI theo §19 SCOPE_ERROR path, không dùng supersedes_fact_ref)."
  - "Khi supersedes_fact_ref có mặt: causation_refs PHẢI chứa chính InstrumentFactInvalidated đang được supersede; envelope.recorded_time PHẢI muộn hơn recorded_time của InstrumentFactInvalidated đó (replacement không visible trước invalidation)."
  - "envelope.effective_time = thời điểm registration record này có hiệu lực làm reference data — mặc định bằng recorded_time trừ khi backfill lịch sử tường minh pin effective_time sớm hơn (§20)."
payload:
  instrument_id: {type: string, required: true}
  instrument_identity_ref: {type: string, required: true}
  base_asset_ref: {type: string, required: true}
  quote_asset_ref: {type: string, required: true}
  instrument_type: {type: enum, values: [SPOT, PERPETUAL, FUTURE], required: true}
  contract_expiry_ref: {type: string, required: false}
  settlement_type: {type: enum, values: [CASH, PHYSICAL], required: false}
  display_name: {type: string, required: false, description: "mô tả tiện dụng, KHÔNG phải identity — đổi display_name không tạo instrument_id mới; sửa qua InstrumentMetadataRevised (§4, forward) hoặc replacement registration (§19, correction)"}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho original registration; BẮT BUỘC cho same-scope correction replacement — xem invariants và §19"}
```

## 4. `InstrumentMetadataRevised` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: instrument-metadata-revised
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE cho một thay đổi metadata mô tả MUTABLE (KHÔNG phải scope identity — đổi
  bất kỳ scope field nào là tạo instrument_id khác, §1). **Forward-looking theo mặc định:** một
  revision mới có effective_time MỚI, fact liền trước vẫn hợp lệ nguyên vẹn cho window lịch sử
  của nó — KHÔNG phải correction. Correction (sửa một fact ĐÃ SAI trong quá khứ) dùng
  InstrumentFactInvalidated + replacement (§6) — hai khái niệm tách bạch tường minh, không gộp.
  **v0.2 (đóng RA-C1-MAJ-02):** payload dùng canonical PATCH policy `revision_policy:
  EXPLICIT_PATCH_WITH_CLEAR_SET` (§17) — `changed_fields`/`clear_fields` tường minh thay vì
  optional field rời rạc.
invariants:
  - "envelope.effective_time = thời điểm metadata này bắt đầu có hiệu lực (forward-looking) — KHÁC recorded_time khi biết trước/backfill."
  - "supersedes_fact_ref VẮNG MẶT cho forward-looking revision bình thường (fact liền trước KHÔNG bị phủ định, chỉ 'hết hiệu lực về sau' theo effective_time thứ tự)."
  - "supersedes_fact_ref BẮT BUỘC có mặt CHỈ KHI đây là correction replacement sau một InstrumentFactInvalidated (§6) — dùng đúng cùng nguyên tắc correction lineage §18."
  - "envelope.recorded_time PHẢI muộn hơn hoặc bằng recorded_time của InstrumentRegistered/revision liền trước cho cùng subject."
  - "changed_fields và clear_fields PHẢI tuân thủ đầy đủ `revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET` (§17) — whitelist patchable field CHỈ gồm: display_name (optional, clearable), classification_tags (optional, clearable). Field scope/identity (instrument_id, instrument_identity_ref, base_asset_ref, quote_asset_ref, instrument_type, contract_expiry_ref, settlement_type) TUYỆT ĐỐI CẤM xuất hiện trong changed_fields hoặc clear_fields."
payload:
  instrument_id: {type: string, required: true}
  changed_fields: {type: map, required: true, description: "field→value PHẢI set — key CHỈ trong whitelist {display_name, classification_tags}; map CÓ THỂ rỗng NẾU clear_fields không rỗng — xem §17 'ít nhất một effective change'"}
  clear_fields: {type: array, items: string, required: true, description: "field CẦN xóa giá trị (đưa về absent) — key CHỈ trong whitelist các field OPTIONAL {display_name, classification_tags}; mảng CÓ THỂ rỗng NẾU changed_fields không rỗng"}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho forward revision bình thường; BẮT BUỘC cho correction replacement — xem invariants và §18"}
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
  - "new_status PHẢI là một transition hợp lệ theo state_machine §1 từ current_status hiện tại — current_status resolve theo `status_fold_order_policy: RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER` (§7 Bước 3, đóng IRB-C1-MAJ-04), KHÔNG đơn thuần theo recorded_time fold."
  - "new_status = RETIRED KHÔNG được có transition tiếp theo nào cho cùng instrument_id."
  - "envelope.effective_time = thời điểm status transition này thực sự có hiệu lực (có thể khác recorded_time nếu biết trước lịch retire, ví dụ future-dated retirement announcement — §20)."
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
  Phủ định MỘT fact lịch sử cụ thể ĐÃ SAI của Logical Instrument — thuần túy ghi nhận "fact này
  không còn hợp lệ", KHÔNG tự nó tuyên bố giá trị mới. **KHÔNG dùng cho forward-looking change**
  (đó là InstrumentMetadataRevised/InstrumentStatusChanged bình thường, không phải invalidation).
  **v0.2 (đóng RA-C1-MAJ-03):** InstrumentRegistered NAY LÀ target hợp lệ. Xem §19 cho policy đầy
  đủ phân biệt METADATA_ERROR (chờ replacement cùng subject) vs SCOPE_ERROR (subject này KHÔNG
  BAO GIỜ có replacement, đăng ký subject mới thay thế).
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref (F) — cùng context_id, subject_kind, subject_type, subject_id, VÀ toàn bộ scope."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref (F)."
  - "payload.invalidated_fact_ref PHẢI trỏ một InstrumentRegistered, InstrumentMetadataRevised, hoặc InstrumentStatusChanged — KHÔNG BAO GIỜ một InstrumentFactInvalidated khác."
  - "invalidated_fact_ref PHẢI trỏ một fact CHƯA từng nhận InstrumentFactInvalidated khác — một fact chỉ bị invalidate đúng một lần."
  - "initial_fact_correction_class BẮT BUỘC có mặt CHỈ KHI invalidated_fact_ref là InstrumentRegistered; CẤM có mặt khi invalidated_fact_ref là InstrumentMetadataRevised/InstrumentStatusChanged."
  - "initial_fact_correction_class = METADATA_ERROR: mong đợi (không bắt buộc ngay lập tức) một InstrumentRegistered replacement CÙNG instrument_id, supersedes_fact_ref = event này (§19)."
  - "initial_fact_correction_class = SCOPE_ERROR: CẤM mọi InstrumentRegistered replacement dưới CÙNG instrument_id — subject này vĩnh viễn không có lineage head VALID nào khác; correction thực tế nằm ở việc đăng ký một instrument_id MỚI hoàn toàn độc lập (§19)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  initial_fact_correction_class: {type: enum, values: [METADATA_ERROR, SCOPE_ERROR], required: false, description: "chỉ có mặt khi invalidated_fact_ref là InstrumentRegistered — xem invariants và §19"}
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

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION` — **không có `UNAVAILABLE`**. Khi `PENDING_CORRECTION`, `pending_correction_class` BẮT BUỘC có mặt (đóng `IRB-C1-MAJ-01`, xem §19 cho mapping đóng đầy đủ).

**Fold algorithm (v0.3, đóng RA-C1-MAJ-02/RA-C1-MAJ-03/IRB-C1-MAJ-01/IRB-C1-MAJ-04):**

```text
Bước 1 — resolve REGISTRATION lineage head tại cursor:
  walk chuỗi InstrumentRegistered (original → replacement → replacement...) qua supersedes_fact_ref,
  visible tại cursor (recorded_time <= cursor), tìm lineage head hiện tại.
  NẾU lineage head có InstrumentFactInvalidated visible VÀ replacement CHƯA visible:
    → view_state = PENDING_CORRECTION, pending_correction_class theo mapping §19, KHÔNG có
      scope/metadata field nào khác được resolve.
  NẾU lineage head KHÔNG có invalidation visible:
    → scope field (instrument_identity_ref, base_asset_ref, quote_asset_ref, instrument_type,
      contract_expiry_ref, settlement_type) = từ lineage head đó (bất biến, luôn giống nhau xuyên
      lineage vì METADATA_ERROR replacement bắt buộc cùng scope, §19).
    → tiếp tục Bước 2.

Bước 2 — fold InstrumentMetadataRevised (mutable metadata patch):
  bắt đầu từ display_name (nếu có) của registration lineage head (Bước 1).
  lấy tập InstrumentMetadataRevised lineage head hợp lệ (đã loại trừ fact bị supersede/invalidate
  chưa có replacement, đúng nguyên tắc §18), visible tại cursor, sắp theo
  `metadata_fold_order_policy` (§17): effective_time ASC (rồi tie-break).
  áp dụng TUẦN TỰ: field trong changed_fields → SET giá trị mới; field trong clear_fields → XÓA
  (absent); field không nhắc tới → GIỮ NGUYÊN từ bước trước.
  Nếu MỘT revision trong chuỗi đang PENDING_CORRECTION (invalidated, chưa có replacement) và
  chính revision đó là bản MỚI NHẤT theo effective_time (tức "hiện tại" đang chờ sửa):
    → view_state = PENDING_CORRECTION, pending_correction_class =
      AWAITING_SAME_SUBJECT_REPLACEMENT (§19 — MetadataRevised correction LUÔN same-subject,
      KHÔNG BAO GIỜ TERMINAL_SCOPE_INVALIDATION), metadata field dừng tại giá trị patch liền
      trước. Nếu revision pending KHÔNG phải bản mới nhất, dừng fold tại patch liền trước nó
      nhưng KHÔNG đổi view_state tổng thể (chỉ registration lineage head mới quyết định
      view_state tổng thể theo mặc định, Bước 1).

Bước 3 — fold InstrumentStatusChanged theo `status_fold_order_policy:
  RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER` (v0.3, đóng IRB-C1-MAJ-04 — thay thế hoàn toàn mô tả
  "derived bằng fold recorded_time" mơ hồ của v0.2):

  Phase 1 — recorded visibility: giữ lại CHỈ InstrumentStatusChanged/InstrumentFactInvalidated/
    replacement có recorded_time <= replay/computation cursor.

  Phase 2 — lineage validity: với mỗi status lineage (một InstrumentStatusChanged có thể tự nó bị
    InstrumentFactInvalidated + replacement, đúng §18 correction lineage), loại bỏ fact đã bị
    invalidate visible tại cursor; chọn lineage head hợp lệ; cấm fork/nhảy cóc (§18 mười
    invariant); KHÔNG dùng một replacement chưa visible tại cursor.

  Phase 3 — effective eligibility: một status event hợp lệ (sau Phase 1–2) chỉ tham gia fold khi
    effective_time <= business/effective cursor.

  Phase 4 — total deterministic ordering: sắp các status event hợp lệ (sau Phase 1–3) theo
    (1) effective_time ASC, (2) recorded_time ASC, (3) event_id ASC. KHÔNG dùng raw cross-stream
    `sequence` để xác định thứ tự — `sequence` chỉ có ý nghĩa NỘI BỘ trong cùng một stream,
    không so sánh được xuyên nhiều instrument/listing/venue stream khác nhau.

  Phase 5 — transition validation: fold tuần tự theo thứ tự Phase 4, validate từng transition
    theo state_machine §1. NẾU hai status event của CÙNG subject có CÙNG effective_time nhưng
    tạo transition KHÔNG tương thích (ví dụ một ACTIVE, một RETIRED, cùng effective_time):
      → conflict — KHÔNG có Current View VALID result cho status field
      → view_state: PENDING_CORRECTION
      → pending_correction_class: AWAITING_SAME_SUBJECT_REPLACEMENT (§19)
      (đóng attack scenario "same-effective-time incompatible status changes" — quyết định đóng,
      không để implementation tự chọn "ai tới trước thắng").

  current_status = kết quả transition CUỐI CÙNG sau khi fold toàn bộ chuỗi hợp lệ theo Phase 4–5
  (KHÔNG phải "status event mới nhất theo recorded_time" — đóng wording sai của v0.2).

  Future-effective status event ĐÃ recorded (Phase 1 visible) nhưng effective_time > cursor hiện
  tại (Phase 3 chưa eligible) KHÔNG ảnh hưởng current_status tại cursor đó — chỉ ảnh hưởng từ
  cursor >= effective_time của nó trở đi (không look-ahead, đóng "future-effective retirement
  already recorded" / "replay before retirement effective time").
```

```yaml
id: instrument-current-view
kind: read_model
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Projection tiện dụng: metadata/status "hiện tại" của một Logical Instrument, rebuild được từ
  §3–§6 theo fold algorithm ở trên. KHÔNG authoritative — mọi input cho Domain Contract khác PHẢI
  dùng authoritative event stream (`ref: instrument`), KHÔNG BAO GIỜ dùng view này (I-12,
  Chapter 7 §7.4).
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism) — mọi implementation dùng cùng fold algorithm PHẢI cho cùng kết quả (đóng RA-C1-MAJ-02, IRB-C1-MAJ-04)."
  - "KHÔNG được dùng làm input cho bất kỳ Domain Contract khác hay Decision — chỉ query/UI."
  - "view_state PHẢI đúng theo Bước 1 của fold algorithm — registration lineage head quyết định, KHÔNG BAO GIỜ fallback về một registration đã invalidate."
  - "pending_correction_class BẮT BUỘC có mặt khi view_state = PENDING_CORRECTION; CẤM có mặt khi view_state = VALID (đóng IRB-C1-MAJ-01, mapping đóng tại §19)."
schema:
  instrument_id: {type: string, required: true}
  scope: {instrument_identity_ref: string, base_asset_ref: string, quote_asset_ref: string, instrument_type: string, contract_expiry_ref: string, settlement_type: string, required: true, description: "chỉ có mặt khi view_state = VALID (Bước 1 fold)"}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  pending_correction_class: {type: enum, values: [AWAITING_SAME_SUBJECT_REPLACEMENT, TERMINAL_SCOPE_INVALIDATION], required: false, description: "BẮT BUỘC khi view_state = PENDING_CORRECTION, CẤM khi VALID — đóng IRB-C1-MAJ-01, mapping §19"}
  current_status: {type: enum, values: [REGISTERED, ACTIVE, SUSPENDED, RETIRED], required: false, description: "chỉ có mặt khi view_state = VALID"}
  display_name: {type: string, required: false}
  classification_tags: {type: array, items: string, required: false}
  last_recorded_time: timestamp
queries: [GetCurrentInstrument, GetInstrumentHistory]
```

## 8. Instrument types — closed enum

```text
SPOT       — giao ngay, không đáo hạn, không settlement_type
PERPETUAL  — hợp đồng vĩnh viễn (funding-rate mechanism), không đáo hạn, settlement_type bắt buộc
FUTURE     — hợp đồng tương lai, contract_expiry_ref + settlement_type bắt buộc
```

**Đóng ở v0.2** — không thêm equities/bonds/forex spot pairs hay asset class khác trừ khi Constitution/ADR hiện tại yêu cầu tường minh (đúng [ADR-007](../adr/ADR-007.md): kiến trúc chừa chỗ multi-asset, nhưng KHÔNG mở rộng ngay).

**`OPTION is RESERVED_NOT_AUTHORED in C1` (v0.2, đóng RA-C1-MAJ-01):** `OPTION` KHÔNG còn trong active enum — v0.1 để `OPTION` trong enum nhưng KHÔNG author đầy đủ schema-specific (strike, option side, exercise style), tạo partial-support ambiguity. v0.2 gỡ hoàn toàn khỏi `instrument_type` active values; bất kỳ attempt đăng ký `instrument_type: OPTION` đều KHÔNG hợp lệ theo schema (đóng attack scenario "OPTION creation attempted while option schema is deferred"). Thêm lại `OPTION` trong tương lai đòi hỏi author ĐẦY ĐỦ, KHÔNG PARTIAL: `option_type` (CALL/PUT), strike representation, exercise style (American/European), `contract_expiry_ref`, `settlement_type`, và mọi field mang identity — một Domain Contract revision tường minh, không tự phát sinh ngầm (§23).

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
  - "TẠI MỘT THỜI ĐIỂM, tối đa MỘT TradableListing ở trạng thái ACTIVE cho cùng cặp (instrument_id, venue_id) — authority boundary duy nhất là `ActiveListingReservation` (§16, đóng IRB-C1-MAJ-03); cấm hai listing đang active đồng thời cho cùng cặp (đóng attack scenario 'duplicate listing identity'). Một listing cũ phải DELISTED/SUSPENDED (giải phóng reservation, §16) trước khi một listing_id mới cho cùng cặp có thể trở thành ACTIVE."
  - "KHÔNG được ACTIVE khi Logical Instrument HOẶC Logical Venue (`venue.md` §1) của nó đã RETIRED tại effective_time đó — ĐỐI XỨNG cho cả hai parent (§1 cross-subject invariant, v0.3 đóng IRB-C1-MAJ-02: v0.2 chỉ enforce phía Instrument). Vi phạm tại thời điểm activation event là invalid event; parent RETIRED SAU một activation hợp lệ KHÔNG retroactively invalidate authoritative event — chỉ ảnh hưởng derived eligibility_state tại Current View (§15)."
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

**KHÔNG chứa:** credential, execution state, order/fill/position (§21).

## 11. `TradableListingCreated` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: tradable-listing-created
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE cho việc tạo một TradableListing — thiết lập scope identity bất biến
  (instrument_id, venue_id, listing_id) và mutable metadata ban đầu (venue symbol, increment, min
  quantity/notional, session reference). Dùng cho CẢ HAI trường hợp (v0.2, đóng RA-C1-MAJ-03):
  (a) original creation, KHÔNG có supersedes_fact_ref; (b) same-scope correction replacement,
  sau TradableListingFactInvalidated target chính creation này, CÓ supersedes_fact_ref (§19).
  state_machine (§10) đưa listing thẳng vào ACTIVE — do đó mọi TradableListingCreated PHẢI thỏa
  điều kiện eligibility như một activation (v0.3, đóng IRB-C1-MAJ-02/IRB-C1-MAJ-03).
invariants:
  - "Tại một thời điểm, đúng MỘT VALID creation lineage head cho mỗi listing_id (đóng RA-C1-MAJ-03, xem §19)."
  - "payload.listing_id/instrument_id/venue_id PHẢI khớp đúng subject_ref.subject_id/scope."
  - "causation_refs PHẢI trỏ InstrumentRegistered của instrument_id VÀ VenueRegistered (venue.md §3) của venue_id — chứng minh cả hai subject đã tồn tại trước khi listing được tạo. Khi supersedes_fact_ref có mặt, causation_refs PHẢI THÊM chính TradableListingFactInvalidated đang được supersede."
  - "supersedes_fact_ref VẮNG MẶT cho original creation; BẮT BUỘC cho same-scope correction replacement — khi có mặt, scope (instrument_id, venue_id, listing_id) PHẢI GIỐNG HỆT fact bị supersede (nếu scope khác, đăng ký subject MỚI theo §19 SCOPE_ERROR path)."
  - "envelope.effective_time = thời điểm listing này thực sự bắt đầu tradable (có thể khác recorded_time nếu backfill/future-dated launch)."
  - "CẤM khi Logical Instrument HOẶC Logical Venue tương ứng đã RETIRED tại envelope.effective_time đó (đóng IRB-C1-MAJ-02, đối xứng Instrument/Venue — §1/§10 cross-subject invariant)."
  - "causation_refs PHẢI THÊM chính ActiveListingReserved (§16) đang grant reservation cho listing_id này cho cặp (instrument_id, venue_id) — TradableListingCreated KHÔNG hợp lệ nếu không có reservation tương ứng (đóng IRB-C1-MAJ-03)."
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
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho original creation; BẮT BUỘC cho same-scope correction replacement — xem invariants và §19"}
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
  TẠI thời điểm computation, không phải giá trị hiện tại — §20). Correction dùng
  TradableListingFactInvalidated (§14). **v0.2 (đóng RA-C1-MAJ-02):** payload dùng canonical
  PATCH policy `revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET` (§17).
invariants:
  - "envelope.effective_time = thời điểm metadata mới bắt đầu có hiệu lực (forward-looking)."
  - "supersedes_fact_ref VẮNG MẶT cho forward-looking revision bình thường; BẮT BUỘC CHỈ KHI là correction replacement sau TradableListingFactInvalidated (§14, §18)."
  - "changed_fields và clear_fields PHẢI tuân thủ đầy đủ `revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET` (§17) — whitelist patchable field: venue_symbol (REQUIRED, KHÔNG clearable), price_increment (REQUIRED, KHÔNG clearable), quantity_increment (REQUIRED, KHÔNG clearable), min_quantity (optional, clearable), min_notional (optional, clearable), session_calendar_ref (REQUIRED, KHÔNG clearable). Field scope/identity (listing_id, instrument_id, venue_id) TUYỆT ĐỐI CẤM xuất hiện trong changed_fields hoặc clear_fields."
payload:
  listing_id: {type: string, required: true}
  changed_fields: {type: map, required: true, description: "field→value PHẢI set — key CHỈ trong whitelist {venue_symbol, price_increment, quantity_increment, min_quantity, min_notional, session_calendar_ref}; map CÓ THỂ rỗng NẾU clear_fields không rỗng"}
  clear_fields: {type: array, items: string, required: true, description: "field CẦN xóa giá trị — key CHỈ trong whitelist các field OPTIONAL {min_quantity, min_notional}; mảng CÓ THỂ rỗng NẾU changed_fields không rỗng"}
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
  - "new_status = ACTIVE CẤM khi Logical Instrument HOẶC Logical Venue tương ứng đã RETIRED tại effective_time đó (§1/§10 cross-subject invariant, ĐỐI XỨNG — v0.3 đóng IRB-C1-MAJ-02, v0.2 chỉ enforce phía Instrument)."
  - "new_status = ACTIVE PHẢI có causation_refs chứa chính ActiveListingReserved (§16) đang grant reservation cho listing_id này cho cặp (instrument_id, venue_id) — KHÔNG hợp lệ nếu không có reservation tương ứng (đóng IRB-C1-MAJ-03)."
  - "new_status ∈ {SUSPENDED, DELISTED} khi listing đang held reservation (§16): PHẢI có một ActiveListingReservationReleased tương ứng, causation_refs của event đó trỏ tới chính TradableListingStatusChanged này, reason = VOLUNTARY_STATUS_CHANGE — giải phóng cặp (instrument_id, venue_id) (đóng IRB-C1-MAJ-03)."
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
  Phủ định MỘT fact lịch sử cụ thể ĐÃ SAI của TradableListing — cùng nguyên tắc
  InstrumentFactInvalidated (§6). **v0.2 (đóng RA-C1-MAJ-03):** TradableListingCreated NAY LÀ
  target hợp lệ — xem §19 cho policy đầy đủ. **v0.3:** khi fact bị invalidate là một
  TradableListingCreated/TradableListingStatusChanged đang HELD reservation (§16), invalidation
  này PHẢI kích hoạt một ActiveListingReservationReleased tương ứng (reason:
  CORRECTION_INVALIDATION) — đóng IRB-C1-MAJ-03 rule 7.
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref."
  - "invalidated_fact_ref PHẢI trỏ một TradableListingCreated, TradableListingMetadataRevised, hoặc TradableListingStatusChanged, CHƯA từng nhận invalidation khác."
  - "initial_fact_correction_class BẮT BUỘC có mặt CHỈ KHI invalidated_fact_ref là TradableListingCreated; CẤM có mặt khi invalidated_fact_ref là TradableListingMetadataRevised/TradableListingStatusChanged. Cùng semantic METADATA_ERROR/SCOPE_ERROR như InstrumentFactInvalidated (§6, §19)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Nếu invalidated_fact_ref đang là activation event HELD reservation (§16) tại recorded_time của chính invalidation này: PHẢI có một ActiveListingReservationReleased causally-linked (causation_refs trỏ tới chính event này), reason = CORRECTION_INVALIDATION."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  initial_fact_correction_class: {type: enum, values: [METADATA_ERROR, SCOPE_ERROR], required: false}
  invalidation_reason: {type: string, required: false}
```

## 15. `TradableListingCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §11–§14, §16, cùng thứ tự tính toán 7-bước PIN cứng (v0.3, đóng `IRB-C1-MAJ-02`/`IRB-C1-MAJ-03`/`IRB-C1-MAJ-04`) — mọi implementation PHẢI theo đúng thứ tự này, dùng CÙNG cặp cursor (recorded-time cursor, effective-time cursor) và CÙNG Definition/contract version xuyên suốt cả 7 bước; KHÔNG dùng current/latest parent state cho historical replay.

**Canonical decision — no-row trước khi có fact đầu tiên:**

```text
Trước khi TradableListingCreated tồn tại cho một listing_id:
  → KHÔNG có TradableListingCurrentView row nào tồn tại
  → GetCurrentListing trả về NOT_FOUND / ABSENT
```

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION`. Khi `PENDING_CORRECTION`, `pending_correction_class` BẮT BUỘC có mặt (§19).

**Fold algorithm (v0.3):**

```text
Bước 1 — rebuild valid listing creation lineage head, đúng §7 Bước 1 áp dụng cho
  TradableListingCreated/TradableListingFactInvalidated (§11, §14). NẾU PENDING_CORRECTION (chờ
  same-subject replacement hoặc SCOPE_ERROR vĩnh viễn) → dừng tại đây, view_state =
  PENDING_CORRECTION, pending_correction_class theo §19 mapping, không resolve field nào khác.

Bước 2 — fold TradableListingMetadataRevised (patch), đúng §7 Bước 2 áp dụng cho §12
  (metadata_fold_order_policy, §17).

Bước 3 — fold TradableListingStatusChanged (status), đúng §7 Bước 3 5-phase
  (status_fold_order_policy, §17) → current_status THÔ (chưa tính eligibility/reservation).

Bước 4 — resolve Instrument eligibility: query InstrumentCurrentView (§7) TẠI CÙNG cặp cursor
  (recorded-time, effective-time) đã dùng ở Bước 1–3 — KHÔNG dùng cursor khác, KHÔNG dùng "hiện
  tại" (đóng attack scenario "Instrument and Venue evaluated at different cursors", IRB-C1-MAJ-02).
  Instrument ELIGIBLE khi: view_state = VALID VÀ current_status != RETIRED.

Bước 5 — resolve Venue eligibility: query VenueCurrentView (venue.md §7) TẠI CÙNG cặp cursor y
  hệt Bước 4 (đối xứng Bước 4, đóng IRB-C1-MAJ-02). Venue ELIGIBLE khi: view_state = VALID VÀ
  current_status != RETIRED.

Bước 6 — resolve pair-scoped active-listing reservation (§16): tại cùng recorded-time cursor, xác
  định holder hiện tại (nếu có) của reservation slot (instrument_id, venue_id) từ
  ActiveListingReserved/ActiveListingReservationReleased visible. current_status THÔ (Bước 3) =
  ACTIVE chỉ HỢP LỆ nếu listing_id này ĐÚNG LÀ holder hiện tại theo reservation stream — nếu event
  stream mâu thuẫn (không nên xảy ra dưới event stream hợp lệ, §16 invariant), coi là defensive
  PENDING_CORRECTION, pending_correction_class = AWAITING_SAME_SUBJECT_REPLACEMENT.

Bước 7 — produce derived listing eligibility/Current View:
  NẾU Bước 4 VÀ Bước 5 đều ELIGIBLE:
    → eligibility_state = ELIGIBLE
    → current_status = kết quả THÔ Bước 3 (không đổi)
  NẾU Bước 4 HOẶC Bước 5 KHÔNG eligible (parent RETIRED, hoặc parent view_state =
    PENDING_CORRECTION — chính identity parent đang bất định):
    → eligibility_state = INELIGIBLE_PARENT_STATE
    → current_status = SUSPENDED — đây là DERIVED OVERRIDE CHỈ cho read model này; KHÔNG fabricate
      một TradableListingStatusChanged authoritative nào; authoritative event stream (§11–§14) giữ
      nguyên, không bị sửa/mutate (đóng IRB-C1-MAJ-02, "preferred" mechanism của Part B).

Một retirement muộn của parent (SAU khi listing activation event đã visible và hợp lệ tại thời
điểm đó) KHÔNG mutate lịch sử — chỉ ảnh hưởng derived eligibility_state/current_status TỪ
effective_time của parent retirement trở đi (Bước 4/5 evaluate TẠI cursor, không phải toàn cục),
đóng attack scenario "retirement becomes visible after historical listing activation". Khi parent
retirement SAU đó bị invalidate/correct (§19), Bước 4/5 tại cursor SAU correction visible tự động
trả về ELIGIBLE trở lại — KHÔNG cần sửa gì ở TradableListing (đóng "parent retirement correction
restores eligibility").
```

```yaml
id: tradable-listing-current-view
kind: read_model
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Projection tiện dụng: metadata/status/eligibility "hiện tại" của một TradableListing, rebuild
  được từ §11–§14, §16 theo fold algorithm 7-bước ở trên. KHÔNG authoritative — mọi input cho
  Domain Contract khác PHẢI dùng authoritative event stream, KHÔNG BAO GIỜ dùng view này (I-12,
  Chapter 7 §7.4, đóng attack scenario "listing uses Current View rather than authoritative
  parent facts").
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism), đúng thứ tự 7 bước — mọi implementation PHẢI cho cùng kết quả."
  - "KHÔNG được dùng làm input cho bất kỳ Domain Contract khác hay Decision — chỉ query/UI."
  - "view_state PHẢI đúng: VALID khi creation lineage head hợp lệ, không invalidation visible; PENDING_CORRECTION khi có invalidation visible nhưng replacement CHƯA visible (vĩnh viễn nếu SCOPE_ERROR, §19)."
  - "pending_correction_class BẮT BUỘC khi view_state = PENDING_CORRECTION; CẤM khi VALID (§19)."
  - "eligibility_state BẮT BUỘC khi view_state = VALID; CẤM khi PENDING_CORRECTION; PHẢI đúng theo Bước 4–7 (đóng IRB-C1-MAJ-02)."
schema:
  listing_id: {type: string, required: true}
  scope: {instrument_id: string, venue_id: string, required: true}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  pending_correction_class: {type: enum, values: [AWAITING_SAME_SUBJECT_REPLACEMENT, TERMINAL_SCOPE_INVALIDATION], required: false}
  eligibility_state: {type: enum, values: [ELIGIBLE, INELIGIBLE_PARENT_STATE], required: false, description: "chỉ có mặt khi view_state = VALID — đóng IRB-C1-MAJ-02, xem Bước 4–7"}
  current_status: {type: enum, values: [ACTIVE, SUSPENDED, DELISTED], required: false, description: "chỉ có mặt khi view_state = VALID; derived SUSPENDED khi eligibility_state = INELIGIBLE_PARENT_STATE (§ Bước 7)"}
  venue_symbol: {type: string, required: false}
  price_increment: {type: decimal, required: false}
  quantity_increment: {type: decimal, required: false}
  min_quantity: {type: decimal, required: false}
  min_notional: {type: decimal, required: false}
  session_calendar_ref: {type: string, required: false}
  last_recorded_time: timestamp
queries: [GetCurrentListing, GetListingHistory]
```

## 16. Pair-scoped active-listing arbitration

**`active_listing_arbitration_policy: PAIR_SCOPED_AUTHORITATIVE_RESERVATION`** (v0.3, đóng `IRB-C1-MAJ-03`) — invariant "tối đa một TradableListing ACTIVE per (instrument_id, venue_id)" (§10) trước đây (v0.2) không có cơ chế xác định authority xuyên nhiều listing stream; raw `sequence`/ingestion arrival order KHÔNG đủ để xác lập precedence xuyên stream khác nhau (`sequence`, Chapter 8, chỉ có ý nghĩa nội bộ MỘT stream). v0.3 pin một pair-scoped authoritative subject riêng, độc lập TradableListing, làm authority boundary duy nhất cho quyết định "listing nào đang ACTIVE cho pair này".

**Đây là Domain Contract authority rule — KHÔNG author runtime implementation, database locking, hay module design** (Phase 1, deferred, §23).

### `ActiveListingReservation` — `kind: entity` (pair-scoped authority subject)

```yaml
id: active-listing-reservation
kind: entity
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Subject continuous, độc lập với TradableListing (§10), resolve deterministic từ CHÍNH XÁC một
  cặp (instrument_id, venue_id) — KHÔNG phải một giá trị opaque tùy ý, KHÔNG có subject mới mỗi
  lần reserve/release (liên tục theo pair, giống Logical Instrument/Venue liên tục theo scope).
  Tại một thời điểm, slot này held bởi TỐI ĐA MỘT listing_id — đây LÀ authority boundary duy nhất
  cho invariant "tối đa một ACTIVE listing per pair" (§10).
invariants:
  - "reservation_id (subject_id) resolve deterministic từ CHÍNH XÁC (instrument_id, venue_id) — hai pair khác nhau luôn có reservation subject khác nhau; cùng pair luôn cùng reservation subject."
  - "Tại một thời điểm, TỐI ĐA MỘT ActiveListingReserved đang 'held' (chưa có ActiveListingReservationReleased tương ứng) cho subject này — held mới chỉ được emit SAU KHI held cũ (nếu có) đã release, visible tại recorded_time của reservation mới."
  - "Quyết định held/release cho MỘT subject reservation LUÔN nằm trong CHÍNH stream của subject đó — đây là authority stream/linearizable boundary duy nhất; KHÔNG so sánh raw sequence xuyên TradableListing stream khác nhau để xác định 'ai tới trước' (đóng IRB-C1-MAJ-03 rule 4/5)."
schema:
  instrument_id: {type: string, required: true, ref: instrument}
  venue_id: {type: string, required: true, ref: venue}
state_machine:
  initial_state: AVAILABLE
  states: [AVAILABLE, HELD]
  transitions:
    - {from: AVAILABLE, to: HELD, caused_by: ActiveListingReserved}
    - {from: HELD, to: AVAILABLE, caused_by: ActiveListingReservationReleased}
events_emitted: [ActiveListingReserved, ActiveListingReservationReleased, ActiveListingActivationRejected]
events_consumed: []
commands: []
queries: []
```

### `ActiveListingReserved` — `kind: event`

Kế thừa nguyên vẹn envelope §2 (subject_ref.subject_type = ActiveListingReservation). Payload đặc thù:

```yaml
id: active-listing-reserved
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE cho việc một listing_id GIÀNH được reservation cho pair (instrument_id,
  venue_id) — grant duy nhất cho phép TradableListingCreated/TradableListingStatusChanged mang
  new_status=ACTIVE trở nên hợp lệ (§11, §13). Serialize trong CHÍNH stream reservation subject.
invariants:
  - "CẤM emit khi reservation subject đang ở state HELD bởi một listing_id KHÁC (chưa release) — trường hợp đó PHẢI emit ActiveListingActivationRejected thay vào đó, KHÔNG emit ActiveListingReserved (rule 3)."
  - "causation_refs PHẢI chứa chính TradableListingCreated hoặc TradableListingStatusChanged (new_status=ACTIVE) đang request reservation này."
  - "envelope.effective_time = effective_time của activation event đang request (cùng effective_time, cùng nguyên tắc envelope binding §2)."
  - "recorded_time xác định thứ tự grant xuyên nhiều request đồng thời cho CÙNG pair — KHÔNG dùng sequence của TradableListing stream khác nhau, KHÔNG dùng ingestion arrival order độc lập với recorded_time của CHÍNH reservation stream (đóng rule 4/5)."
payload:
  instrument_id: {type: string, required: true}
  venue_id: {type: string, required: true}
  listing_id: {type: string, required: true, description: "listing đang giữ reservation"}
```

### `ActiveListingReservationReleased` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: active-listing-reservation-released
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE cho việc reservation của một pair được giải phóng — pair trở về AVAILABLE.
  KHÔNG tự động cấp lại cho bất kỳ listing nào khác.
invariants:
  - "CHỈ hợp lệ khi reservation subject đang ở state HELD bởi đúng listing_id trong payload."
  - "reason = VOLUNTARY_STATUS_CHANGE: causation_refs PHẢI chứa chính TradableListingStatusChanged (new_status ∈ {SUSPENDED, DELISTED}) gây ra release này."
  - "reason = CORRECTION_INVALIDATION: causation_refs PHẢI chứa chính TradableListingFactInvalidated (§14) đang invalidate activation event (TradableListingCreated hoặc TradableListingStatusChanged mang new_status=ACTIVE) đang held reservation này — đóng rule 7 'correction/invalidation of the winning activation or reservation causes deterministic re-evaluation'."
  - "Sau release, reservation subject = AVAILABLE — một listing_id KHÁC (kể cả một listing từng bị ActiveListingActivationRejected trước đó cho pair này) KHÔNG tự động trở thành holder mới; CẦN một ActiveListingReserved MỚI, gắn với một activation request MỚI tường minh, PHẢI xảy ra SAU khi release này visible (recorded_time) — cấm automatic promotion (đóng rule 8, 'preferred rule': không có candidate 'chờ sẵn')."
payload:
  instrument_id: {type: string, required: true}
  venue_id: {type: string, required: true}
  listing_id: {type: string, required: true}
  reason: {type: enum, values: [VOLUNTARY_STATUS_CHANGE, CORRECTION_INVALIDATION], required: true}
```

### `ActiveListingActivationRejected` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: active-listing-activation-rejected
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE — audit record cho một activation request KHÔNG giành được reservation vì
  pair đang HELD bởi listing khác. KHÔNG đổi state reservation subject (vẫn HELD bởi holder hiện
  tại) — thuần túy ghi nhận sự kiện "request này đã xảy ra và bị từ chối" (đóng attack scenario
  'two listing activations recorded concurrently on separate streams').
invariants:
  - "CHỈ hợp lệ khi reservation subject đang ở state HELD bởi một listing_id KHÁC listing_id trong payload tại thời điểm request."
  - "causation_refs PHẢI chứa chính TradableListingCreated/TradableListingStatusChanged (new_status=ACTIVE) đang bị từ chối."
  - "related_event_refs (non-causal) NÊN trỏ chính ActiveListingReserved đang HELD hiện tại, cho mục đích truy vết — không bắt buộc."
  - "Rejected listing KHÔNG được coi là 'candidate chờ' — không có promotion tự động khi holder release (đóng rule 8)."
payload:
  instrument_id: {type: string, required: true}
  venue_id: {type: string, required: true}
  rejected_listing_id: {type: string, required: true}
  held_by_listing_id: {type: string, required: true, description: "listing hiện đang giữ reservation tại thời điểm reject"}
```

### Historical replay và Current View authority restriction

Replay tại một cursor reconstruct reservation holder CHỈ từ `ActiveListingReserved`/`ActiveListingReservationReleased` visible tại `recorded_time <= cursor` (đúng nguyên tắc bitemporal chung, §20) — KHÔNG dùng `ActiveListingActivationRejected` để xác định holder (đó chỉ là audit record, không authoritative cho state). KHÔNG có read model/Current View riêng cho `ActiveListingReservation` ở C1 — `TradableListingCurrentView` (§15 Bước 6) là điểm consume DUY NHẤT của reservation state cho mục đích derived eligibility; không Domain Contract nào khác được query reservation event stream trực tiếp làm input cho Decision/Risk/Execution (đối xứng I-12, Chapter 7 §7.4).

## 17. Canonical policy identifiers — nguồn duy nhất

**Năm canonical policy identifier, khai báo ĐÚNG MỘT LẦN tại đây — mọi nơi khác trong tài liệu chỉ tham chiếu theo tên, không lặp lại chuỗi (đóng trước lớp lỗi IRB-B2-MIN-01-style):**

```yaml
revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET
initial_fact_correction_policy: INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES
metadata_fold_order_policy: effective_time_asc_then_recorded_time_asc_then_stream_id_asc_then_registry_version_asc_then_sequence_asc_then_event_id_asc
status_fold_order_policy: RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER
active_listing_arbitration_policy: PAIR_SCOPED_AUTHORITATIVE_RESERVATION
```

**`revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET`** — áp dụng cho `InstrumentMetadataRevised` (§4), `TradableListingMetadataRevised` (§12), và `venue.md`'s `VenueMetadataRevised`. Quy tắc bắt buộc:

```text
changed_fields   — required field trong payload (map), key CHỈ trong whitelist patchable của event đó
clear_fields     — required field trong payload (array), key CHỈ trong whitelist patchable OPTIONAL của event đó

absent field (không trong changed_fields lẫn clear_fields)  → UNCHANGED (giữ nguyên giá trị trước)
field trong changed_fields                                   → SET về giá trị supplied
field trong clear_fields                                     → CLEAR (đưa về absent/removed) — CHỈ hợp lệ cho optional field

changed_fields keys ∩ clear_fields  →  PHẢI RỖNG (cấm vừa set vừa clear cùng field trong một patch)
required field (theo whitelist)     →  KHÔNG BAO GIỜ được xuất hiện trong clear_fields
unknown field hoặc scope/identity field  →  CẤM tuyệt đối trong cả changed_fields lẫn clear_fields
ít nhất một effective change         →  BẮT BUỘC — changed_fields và clear_fields KHÔNG được cùng rỗng (đóng attack scenario "empty patch")
```

**`initial_fact_correction_policy: INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES`** — xem §19 cho định nghĩa đầy đủ.

**`metadata_fold_order_policy`** — total order dùng khi fold nhiều `*MetadataRevised` cùng `effective_time` (hiếm, cần tie-break deterministic): `effective_time` ASC, `recorded_time` ASC, `stream_id` ASC, `registry_version` ASC, `sequence` ASC (CHỈ trong cùng stream identity), `event_id` ASC — dùng bởi Current View fold (§7, §15).

**`status_fold_order_policy: RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER`** (v0.3, đóng `IRB-C1-MAJ-04`) — total order + visibility discipline dùng khi fold `InstrumentStatusChanged`/`TradableListingStatusChanged`/`VenueOperationalStatusChanged`. Thuật toán đầy đủ 5-phase (recorded visibility → lineage validity → effective eligibility → total deterministic ordering effective_time ASC/recorded_time ASC/event_id ASC, KHÔNG dùng raw sequence xuyên stream → transition validation với conflict rejection cho same-effective-time incompatible transition) — xem §7 Bước 3 cho định nghĩa đầy đủ, áp dụng nguyên văn cho Instrument/TradableListing/Venue.

**`active_listing_arbitration_policy: PAIR_SCOPED_AUTHORITATIVE_RESERVATION`** (v0.3, đóng `IRB-C1-MAJ-03`) — xem §16 cho định nghĩa đầy đủ: pair-scoped `ActiveListingReservation` subject là authority boundary duy nhất cho "tối đa một ACTIVE listing per (instrument_id, venue_id)"; không dùng raw cross-stream sequence hay ingestion order; không automatic promotion sau release.

## 18. Correction lineage (cả hai họ subject)

Correction lineage scoped chính xác theo `(subject_id, effective_time)` — mỗi effective_time-slice có chuỗi lineage RIÊNG.

```text
InstrumentRegistered/TradableListingCreated/InstrumentMetadataRevised/... F1
  → *FactInvalidated targeting F1
  → replacement (cùng event type), supersedes_fact_ref = F1

Correction tiếp theo:
F2
  → *FactInvalidated targeting F2
  → F3, supersedes_fact_ref = F2   (KHÔNG được supersedes_fact_ref = F1 — cấm nhảy cóc)
```

**Mười invariant bắt buộc** (đã pin tại §3–§6, §11–§14, tổng hợp lại đây — v0.2 mở rộng cho initial fact, đóng RA-C1-MAJ-03):

1. Original fact (`InstrumentRegistered`/`TradableListingCreated` KHÔNG có supersedes_fact_ref) không có `supersedes_fact_ref`.
2. Replacement fact (correction, kể cả replacement registration/creation) bắt buộc có `supersedes_fact_ref`; forward-looking revision bình thường thì không.
3. Replacement dùng đúng cùng subject và cùng `effective_time` với fact bị supersede.
4. Replacement PHẢI supersede đúng lineage head hiện tại.
5. Replacement không được nhảy cóc qua một head trung gian.
6. Một fact bị invalidate có **tối đa một** replacement authoritative trực tiếp — cấm fork.
7. Replacement không được "visible" (`recorded_time`) trước invalidation tương ứng.
8. Mọi lineage member lịch sử giữ nguyên trong log — append-only (I-3), không mutate.
9. Một fact đã invalidate **không bao giờ** bị tái sử dụng ngầm — Current View (§7 cho Instrument, §15 cho TradableListing) phải loại trừ nó tường minh.
10. **Forward-looking revision KHÔNG BAO GIỜ dùng cơ chế invalidation** — chỉ correction (sửa sai sót thực sự trong quá khứ) mới dùng `*FactInvalidated` + replacement.

`ActiveListingReserved`/`ActiveListingReservationReleased`/`ActiveListingActivationRejected` (§16) **KHÔNG có `*FactInvalidated` riêng** — correction của reservation state đi qua invalidation của activation event gốc (`TradableListingCreated`/`TradableListingStatusChanged`) + `ActiveListingReservationReleased` (reason: `CORRECTION_INVALIDATION`) causally-linked, đúng §16, không nhân đôi cơ chế correction.

## 19. Initial-fact correction policy

**`initial_fact_correction_policy: INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES`** (v0.2, đóng `RA-C1-MAJ-03`) — v0.1 KHÔNG cho phép correct `InstrumentRegistered`/`TradableListingCreated` dưới bất kỳ hình thức nào; điều này không thực tế (registration/creation vẫn có thể ghi sai). v0.2 pin đúng MỘT policy đóng, phân biệt hai trường hợp:

### Same-scope metadata error

Khi registration/creation gốc có **scope identity ĐÚNG** nhưng **mutable metadata SAI** (ví dụ `display_name` ghi sai lúc đăng ký):

```text
invalidate initial fact (InstrumentFactInvalidated/TradableListingFactInvalidated,
  initial_fact_correction_class = METADATA_ERROR)
→ emit replacement registration/creation fact CHO CÙNG subject
  (instrument_id/listing_id không đổi, TOÀN BỘ scope field giống hệt,
  supersedes_fact_ref trỏ về fact vừa invalidate)
```

**"Một registration" nghĩa là MỘT VALID lineage head, không phải một event record duy nhất mãi mãi** (§3, §11 invariant) — một `instrument_id` có thể có NHIỀU `InstrumentRegistered` record trong log (một original + N correction replacement), nhưng tại một thời điểm CHỈ đúng MỘT trong số đó là lineage head VALID (append-only, §18).

### Scope/identity error

Khi registration/creation gốc có **scope identity SAI** (ví dụ `base_asset_ref`/`instrument_type`/`instrument_identity_ref` nhập nhầm ngay từ đầu — đây KHÔNG phải lỗi mutable metadata, đây là "cả subject này bị định danh sai"):

```text
invalidate initial fact SAI (InstrumentFactInvalidated/TradableListingFactInvalidated,
  initial_fact_correction_class = SCOPE_ERROR)
→ KHÔNG replace dưới subject cũ — CẤM tuyệt đối một replacement registration
  với supersedes_fact_ref trỏ về đây (§3, §11 invariant)
→ đăng ký một subject MỚI: instrument_id / venue_id / listing_id MỚI, với scope ĐÚNG
```

**Subject cũ KHÔNG được tiếp tục authoritative** — sau invalidation, subject cũ vĩnh viễn không có lineage head VALID nào khác (không có replacement, theo định nghĩa của SCOPE_ERROR).

### Current View correction classification — `pending_correction_class` (v0.3, đóng `IRB-C1-MAJ-01`)

```text
Invalidation visible, replacement/subject-mới registration CHƯA visible (hoặc SẼ KHÔNG BAO GIỜ
visible dưới subject cũ, trường hợp SCOPE_ERROR):
  → subject cũ Current View = PENDING_CORRECTION

initial_fact_correction_class = METADATA_ERROR:
  → view_state: PENDING_CORRECTION
  → pending_correction_class: AWAITING_SAME_SUBJECT_REPLACEMENT
  → trạng thái TẠM THỜI, chờ replacement cùng subject; một cursor tương lai (sau khi replacement
    visible) đưa subject này về VALID.

initial_fact_correction_class = SCOPE_ERROR:
  → view_state: PENDING_CORRECTION
  → pending_correction_class: TERMINAL_SCOPE_INVALIDATION
  → trạng thái VĨNH VIỄN cho subject này — KHÔNG cursor tương lai nào đưa nó về VALID (không có
    replacement hợp lệ dưới subject cũ, theo policy). TERMINAL_SCOPE_INVALIDATION KHÔNG BAO GIỜ
    transition ngược về VALID, dưới bất kỳ cursor nào.
```

**`pending_correction_class` — discriminator bắt buộc khi `view_state = PENDING_CORRECTION`, CẤM khi `view_state = VALID`:**

```yaml
pending_correction_class:
  type: enum
  values: [AWAITING_SAME_SUBJECT_REPLACEMENT, TERMINAL_SCOPE_INVALIDATION]
```

Áp dụng thống nhất cho `InstrumentCurrentView` (§7), `TradableListingCurrentView` (§15), `VenueCurrentView` (`venue.md` §7):

```text
view_state = VALID              → pending_correction_class: CẤM (phải absent)
view_state = PENDING_CORRECTION → pending_correction_class: BẮT BUỘC

Mapping đóng, không implementation-selected:
  initial_fact_correction_class = METADATA_ERROR                      → AWAITING_SAME_SUBJECT_REPLACEMENT
  initial_fact_correction_class = SCOPE_ERROR                         → TERMINAL_SCOPE_INVALIDATION
  đang chờ replacement một *MetadataRevised/*StatusChanged             → AWAITING_SAME_SUBJECT_REPLACEMENT
    (§7 Bước 2, KHÔNG BAO GIỜ TERMINAL_SCOPE_INVALIDATION — MetadataRevised/StatusChanged
    correction luôn same-subject theo định nghĩa)
  same-effective-time status conflict (§7 Bước 3 Phase 5)               → AWAITING_SAME_SUBJECT_REPLACEMENT
  reservation/listing state mâu thuẫn, defensive case (§15 Bước 6)      → AWAITING_SAME_SUBJECT_REPLACEMENT
```

Pin bổ sung (đóng attack scenario "retry worker confuses terminal invalidation with temporary pending"):

- `TERMINAL_SCOPE_INVALIDATION` KHÔNG BAO GIỜ transition về `VALID` — không có cursor, không có replacement, không có sự kiện tương lai nào thay đổi kết quả này cho subject cũ.
- Một subject MỚI được đăng ký sau SCOPE_ERROR (`instrument_id`/`venue_id`/`listing_id` mới) có Current View ĐỘC LẬP HOÀN TOÀN — không kế thừa `PENDING_CORRECTION`/`TERMINAL_SCOPE_INVALIDATION` từ subject cũ, không "trở thành VALID lại" của subject cũ (đây là hai subject riêng biệt, §1/§10).
- Subject cũ (`TERMINAL_SCOPE_INVALIDATION`) vẫn queryable qua `GetInstrumentHistory`/`GetListingHistory`/`GetVenueHistory` — làm historical invalid evidence (audit trail), KHÔNG bị xóa khỏi hệ thống.
- Consumer (bao gồm retry worker, background job) KHÔNG được coi `TERMINAL_SCOPE_INVALIDATION` là "chờ và thử lại sau" — đây là tín hiệu đóng, dừng polling/retry cho subject này; hành vi đúng là tra cứu subject MỚI (nếu có, qua `related_event_refs` non-causal traceability, §2) hoặc coi như không tồn tại.

Đây là quy tắc **duy nhất, đóng** cho cả hai trường hợp — không để implementation tự chọn hành vi khác.

## 20. Time semantics và bitemporal correctness

```text
effective_time    — khi fact này THỰC SỰ có hiệu lực làm reference data (forward-looking cho revision, hoặc lịch sử cho correction)
recorded_time     — khi Ride ghi nhận fact này (bắt buộc, mọi event — envelope §2)
market_time       — PROHIBITED (§2)
```

**Không dùng `event_time`.**

**Historical Replay PHẢI dùng đúng metadata có hiệu lực TẠI computation cursor, không phải giá trị hiện tại** — ví dụ: Backtest tại thời điểm T dùng `price_increment` có `effective_time <= T` MỚI NHẤT tại T, KHÔNG dùng `price_increment` hiện tại của TradableListing (đóng attack scenario "current metadata accidentally used for historical replay", "tick size changes historically"). Selection algorithm: role-specific "latest valid fact với `effective_time <= cursor` VÀ `recorded_time <= replay cursor`" — cùng nguyên tắc recorded-time-visibility + effective-time-eligibility đã khóa ở `feature.md` §12/`context.md` §14 (không look-ahead).

**Correction visibility:** `*FactInvalidated` và replacement đều có `recorded_time` mới; replay tại cursor trước đó chỉ thấy fact gốc (đóng attack scenario "replay before initial-fact invalidation", "replay after invalidation but before replacement", "correction visible after replay cursor" — correction KHÔNG BAO GIỜ visible cho một replay cursor trước recorded_time của chính correction đó, kể cả khi effective_time của correction rơi vào quá khứ xa hơn).

## 21. Prohibitions

**Instrument (Logical Instrument) KHÔNG được sở hữu:** live market price; Candle; Strategy; Decision; Risk; Account; Position; Order; Fill; execution status.

**TradableListing KHÔNG được chứa:** credential; execution state; Order/Fill/Position semantics (đóng attack scenario "Order/Fill/Position semantics accidentally introduced").

**`ActiveListingReservation` KHÔNG được chứa:** bất kỳ business/execution semantic nào ngoài phạm vi arbitration (§16) — không phải lock/queue implementation, không phải execution ordering mechanism.

## 22. Venue & asset-class neutrality

Đúng [ADR-007](../adr/ADR-007.md): KHÔNG giả định crypto-only, KHÔNG giả định 24/7 (session/calendar reference luôn tường minh qua `venue.md` §8, không hardcode "00:00–24:00 liên tục" — đóng attack scenario "crypto 24/7 assumption"). Một Logical Instrument có thể có **nhiều TradableListing đồng thời trên nhiều Venue** (đóng "same logical instrument listed on two venues"), và **nhiều variant khác `instrument_type`/`settlement_type` cho cùng underlying** (ví dụ BTC/USDT SPOT và BTC-PERPETUAL cash-settled và BTC-PERPETUAL coin-margined là BA `instrument_id` khác nhau, không phải các state của cùng một subject — đóng "one instrument has spot and perpetual variants", "cash-settled and physically-settled future with same base/quote/expiry").

## 23. Ngoài phạm vi — defer

**Deferred tường minh, không author ở C1:** Asset như một Domain Contract riêng (chỉ dùng `base_asset_ref`/`quote_asset_ref` opaque); OPTION schema đầy đủ (strike, option side/type, exercise style — §8); cơ chế resolve cụ thể `contract_expiry_ref`/`session_calendar_ref`/`instrument_identity_ref` (calendar/reference service, Phase 1); `stream_ref`/`producer_ref` (Phase 1); cơ chế đăng ký Instrument/Listing cụ thể (thủ công qua Product Owner, hay tự động từ external reference feed — cả hai đều hợp lệ theo envelope §2, không chọn một cách duy nhất); cơ chế runtime cụ thể (locking, serialization engine, message queue) cho `ActiveListingReservation` authority stream (§16 — đây CHỈ là Domain Contract rule, không phải implementation); Account/Strategy/Decision/Risk/Order/Fill/Position/Execution/Trade Intent/Execution Intent/Replay Event (Package 0.2-C2–C7, chưa authorize).

**Out of scope theo ranh giới domain:** live market price, Candle semantics (thuộc `candle.md`), bất kỳ business decision nào — vi phạm trực tiếp định nghĩa Instrument nếu thêm vào (§21).

## 24. Open questions ngoài phạm vi

- `instrument_identity_ref` hiện là opaque string, KHÔNG có cơ chế/registry cụ thể nào định nghĩa giá trị hợp lệ hay đảm bảo global uniqueness tự động (trách nhiệm thuộc registration authority ngoài Domain Contract, §1/§23). Cần quyết định khi Package 0.2-C có nhu cầu thực tế đầu tiên (đối xứng ghi chú các Domain Contract trước).
- `contract_expiry_ref`/`session_calendar_ref` hiện là opaque string reference — chưa có Domain Contract hay registry cụ thể nào định nghĩa format/resolve mechanism.
- `OPTION` deferred hoàn toàn (§8) — chưa rõ thời điểm Package 0.2-C nào sẽ thực sự cần author đầy đủ option schema; không đóng OQ-002/OQ-003.
- Cơ chế cụ thể (serialization engine, distributed lock, single-writer stream) hiện thực hóa "authority stream" cho `ActiveListingReservation` (§16) chưa được quyết — đây là Phase 1 Engineering/Plugin Model concern, Domain Contract chỉ pin RULE (một authority boundary duy nhất, không dùng raw cross-stream sequence), không pin MECHANISM.
