---
id: instrument
title: Instrument
version: "0.6"
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

**`instrument-registered`/`instrument-metadata-revised`/`instrument-status-changed`/`instrument-fact-invalidated`/`instrument-current-view`/`tradable-listing-created`/`tradable-listing-metadata-revised`/`tradable-listing-status-changed`/`tradable-listing-fact-invalidated`/`tradable-listing-current-view`/`active-listing-activation-requested`/`active-listing-reserved`/`active-listing-reservation-released`/`active-listing-activation-rejected`/`active-listing-reservation-fact-invalidated` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây. Display name, concept ID, và `event_type` là ba đại lượng khác nhau, không cạnh tranh identity — cùng nguyên tắc `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`/`context.md` đã khóa.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B:** envelope binding cho mọi `*FactInvalidated` (`subject_ref`/`effective_time` kế thừa từ fact bị invalidate, không tự khai báo độc lập); tách bạch **forward-looking revision** (fact mới, effective_time mới, fact cũ vẫn giữ nguyên hợp lệ cho window lịch sử của nó — KHÔNG phải correction) khỏi **correction** (invalidate + replace, đúng khi một fact lịch sử ĐÃ SAI); no-row Current View semantics trước fact đầu tiên, `view_state` chỉ có `VALID`/`PENDING_CORRECTION`; mọi canonical policy identifier chỉ khai báo ĐÚNG MỘT NƠI; opaque identity — không parse `instrument_id`/`venue_id`/`listing_id` để suy diễn business meaning (Chapter 6 §6.8).

**v0.2 — ChatGPT Review A narrow correction, đóng `RA-C1-MAJ-01`/`RA-C1-MAJ-02`/`RA-C1-MAJ-03`:** (a) `RA-C1-MAJ-01` — scope identity v0.1 (base/quote/type/expiry) không đủ discriminate cho derivatives; thêm `instrument_identity_ref`; `OPTION` gỡ khỏi enum active, `RESERVED_NOT_AUTHORED` (§8); `settlement_type` bắt buộc tường minh cho FUTURE/PERPETUAL. (b) `RA-C1-MAJ-02` — pin canonical `revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET` (§17). (c) `RA-C1-MAJ-03` — pin canonical `initial_fact_correction_policy: INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES` (§17, §19).

**v0.3 — Independent Review B narrow correction, đóng `IRB-C1-MAJ-01`/`IRB-C1-MAJ-02`/`IRB-C1-MAJ-03`/`IRB-C1-MAJ-04`:** (a) `IRB-C1-MAJ-01` — `PENDING_CORRECTION` v0.2 không phân biệt "chờ replacement tạm thời" với "vĩnh viễn invalid do scope error"; thêm discriminator đóng `pending_correction_class` (`AWAITING_SAME_SUBJECT_REPLACEMENT`/`TERMINAL_SCOPE_INVALIDATION`), áp dụng thống nhất `InstrumentCurrentView`/`TradableListingCurrentView`/`VenueCurrentView` (§19). (b) `IRB-C1-MAJ-02` — TradableListing eligibility v0.2 chỉ cấm ACTIVE khi Instrument RETIRED, KHÔNG đối xứng cho Venue RETIRED; v0.3 thêm invariant đối xứng tại §10/§11/§13, cộng derived `eligibility_state` tại `TradableListingCurrentView` (§15) — KHÔNG fabricate authoritative status event. (c) `IRB-C1-MAJ-03` — "tối đa một ACTIVE listing per pair" thiếu cross-stream authority boundary; thêm `ActiveListingReservation` pair-scoped subject + `ActiveListingReserved`/`ActiveListingReservationReleased`/`ActiveListingActivationRejected` (§16), pin `active_listing_arbitration_policy: PAIR_SCOPED_AUTHORITATIVE_RESERVATION` (§17), không automatic promotion. (d) `IRB-C1-MAJ-04` — status fold v0.2 mô tả mơ hồ ("derived bằng fold recorded_time"); pin canonical `status_fold_order_policy: RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER` (§17), thuật toán 5-phase tường minh tại §7 Bước 3 (áp dụng cho Instrument/TradableListing/Venue status). Narrow correction — không redesign toàn package, `instrument_id`/`venue_id`/`listing_id` không đổi tên/shape.

**v0.4 — Independent Review B (v0.3 round) narrow correction cuối cùng, đóng `IRB-C1-V03-MAJ-01`/`IRB-C1-V03-MAJ-02`/`IRB-C1-V03-MAJ-03`/`IRB-C1-V03-MAJ-04`:** (a) `IRB-C1-V03-MAJ-01` — v0.3 `ActiveListingReserved` causation_refs trỏ tới activation event (`TradableListingCreated`/`StatusChanged`), ĐỒNG THỜI activation event đó causation_refs trỏ ngược tới `ActiveListingReserved` — chu trình causal. Thêm `ActiveListingActivationRequested` (§16) làm pre-arbitration request tường minh: request → grant/reject (causal tới request, KHÔNG tới activation event) → activation event (causal tới grant) — chuỗi causal tuyến tính, không chu trình. (b) `IRB-C1-V03-MAJ-02` — `TradableListingCurrentView` Bước 4–5 v0.3 dùng `InstrumentCurrentView`/`VenueCurrentView` (read model, đã tự khóa "KHÔNG được dùng làm input") làm input — mâu thuẫn nội tại. v0.4 Bước 4–5 nay reconstruct TRỰC TIẾP từ authoritative Instrument/Venue event stream, dùng đúng fold algorithm §7 — Current View CHỈ còn là cache tùy chọn, provably equivalent, KHÔNG BAO GIỜ là authority. (c) `IRB-C1-V03-MAJ-03` — reservation fact (`ActiveListingReserved`/`Released`/`ActivationRejected`) v0.3 không có correction lineage; thêm `ActiveListingReservationFactInvalidated` (§16) + `supersedes_fact_ref` trên cả ba event, đóng `RESERVATION_METADATA_ERROR`/`RESERVATION_PAIR_SCOPE_ERROR`. (d) `IRB-C1-V03-MAJ-04` — reservation fold v0.3 không có effective-time eligibility tường minh; pin `reservation_fold_order_policy: RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER` (§17), thuật toán 5-phase đầy đủ (§16) đối xứng `status_fold_order_policy`. Narrow correction cuối cùng — không redesign, `instrument_id`/`venue_id`/`listing_id` không đổi tên/shape; `venue.md` KHÔNG cần sửa transaction này (không có nội dung normative nào của venue.md bị chạm bởi bốn finding trên — mọi cross-reference `instrument.md §N` từ venue.md vẫn đúng số vì KHÔNG có section mới được chèn ở tầng top-level, chỉ nội dung bên trong §2/§7/§10/§11/§13/§15/§16/§17/§18/§24 thay đổi).

**v0.5 — Independent Review B (v0.4 round) bounded final correction, đóng `IRB-C1-V04-MAJ-01`:** v0.4 `ActiveListingActivationRequested` KHÔNG có stable logical request identity — chỉ có `event_id` (đổi mỗi physical record) và `subject_ref`/scope (không đủ phân biệt request khác nhau cho cùng listing). Dưới ingress retry/redelivery (Phase 1, at-least-once), không dedup được, không idempotent được, exactly-one-outcome (§16) không executable. v0.5 thêm `activation_request_id` — logical identity ổn định, opaque, KHÔNG bằng `event_id`, KHÔNG regenerate khi retry, vĩnh viễn bind đúng một (instrument_id, venue_id, listing_id, requested_target_status). Pin `activation_request_idempotency_policy: STABLE_ID_SAME_PAYLOAD_IS_IDEMPOTENT` (§17): exact retry idempotent (không tạo request/outcome thứ hai); changed-payload replay reject (deterministic conflict). `ActiveListingActivationRequested` không có correction lineage riêng — request sai KHÔNG sửa, chỉ dùng `activation_request_id` MỚI cho intent đã sửa. `ActiveListingReserved`/`ActiveListingActivationRejected` thêm `activation_request_id` (required, phải khớp request được `activation_request_ref` trỏ tới) — exactly-one-outcome nay keyed theo `activation_request_id` (logical), không chỉ theo event ref. `TradableListingCreated`/`TradableListingStatusChanged(ACTIVE)` thêm `activation_request_id` (required khi ACTIVE) — grant phải cùng request ID VÀ cùng scope, cấm dùng grant của request khác, cấm hai activation event consume cùng một grant (trừ idempotent duplicate). Outcome type (grant/reject) bất biến — correction KHÔNG BAO GIỜ flip type; đảo type cần invalidate + activation_request_id MỚI. Thêm "Request dedup và replay algorithm" (7 bước) tại §16. Bounded correction — không redesign activation arbitration, không đổi reservation correction lineage/parent reconstruction/bitemporal folding hiện có; `venue.md` KHÔNG cần sửa (không nội dung normative nào bị chạm; không cross-reference nào tới instrument.md bị lệch số vì KHÔNG chèn section top-level mới).

**v0.6 — Independent Review B (v0.5 round) narrow correction, đóng `IRB-C1-V05-MAJ-01`:** v0.5 pin `ActiveListingActivationRequested` immutable, không có correction lineage riêng — nhưng KHÔNG định nghĩa điều gì xảy ra khi một request ĐÃ pass ingress validation, ĐÃ ghi nhận authoritative, rồi SAU ĐÓ phát hiện SAI thực tế (factual error) — không có invalidation append-only, không có replay exclusion/classification, canonical semantic payload chưa liệt kê đầy đủ. v0.6 thêm `ActiveListingActivationRequestFactInvalidated` (§16) — CHỈ target `ActiveListingActivationRequested`, KHÔNG replacement dưới cùng `activation_request_id` (giữ nguyên quyết định bounded "immutable, không metadata-patchable" của v0.5). Pin canonical request validity: `VALID`/`TERMINALLY_INVALID` — invalidation visible tại cursor ⟹ TERMINALLY_INVALID vĩnh viễn, KHÔNG BAO GIỜ quay lại VALID. Định nghĩa hệ quả deterministic lên arbitration outcome theo ba trường hợp thời điểm (chưa có outcome; có rejection; có grant chưa activation; có grant VÀ activation đã ghi nhận) — case cuối tái dùng cơ chế `TradableListingFactInvalidated` (§14) VÀ `ActiveListingReservationReleased` (§16) đã có sẵn, KHÔNG phát minh cơ chế thứ hai. `ActiveListingReserved`/`ActiveListingActivationRejected`/`TradableListingCreated`/`TradableListingStatusChanged(ACTIVE)` thêm invariant: request tham chiếu PHẢI visible VÀ VALID (không TERMINALLY_INVALID) tại cursor liên quan — không rewrite causation lịch sử. Cập nhật "Request dedup và replay algorithm" thành 10 bước (thêm resolve/classify request validity). Liệt kê đầy đủ canonical semantic payload cho `ActiveListingActivationRequested` — thêm `request_reason` (non-authoritative, loại khỏi idempotency equality); `requested_by_ref` pin là semantic (phải khớp chính xác khi redelivery cùng ID); làm rõ `source_identity`/`causation_refs`/`related_event_refs` không phải business request scope. Narrow correction — không redesign activation arbitration, không đổi reservation authority structure, không đổi parent reconstruction, không đổi status/reservation fold policy.

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
  subject_ref: {cardinality: "required — shape canonical, xem dưới. Trên mọi *FactInvalidated (§6, §14, §16), PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate."}
  stream_ref: {cardinality: required}                # Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # Phase 1, chưa author
  correlation_id: {cardinality: "required khi computation thuộc một correlation flow tường minh; optional khi độc lập"}
  causation_refs: {cardinality: "InstrumentRegistered/TradableListingCreated ORIGINAL (không supersedes_fact_ref): zero-or-more (fact gốc, không nhất thiết có causal ancestor authoritative — đăng ký thủ công hoặc từ external reference feed, Phase 1). InstrumentRegistered/TradableListingCreated REPLACEMENT (có supersedes_fact_ref, §19): KHÔNG BAO GIỜ rỗng, PHẢI chứa chính InstrumentFactInvalidated/TradableListingFactInvalidated đang được supersede. Mọi event khác (revision/status-change/invalidation/reservation/activation-request): KHÔNG BAO GIỜ rỗng — xem §3–§6, §11–§14, §16. **Chu trình causal (A causal B, B causal A, trực tiếp hoặc gián tiếp qua chuỗi) CẤM TUYỆT ĐỐI xuyên toàn bộ tài liệu này — đóng IRB-C1-V03-MAJ-01, xem §16 cho chuỗi causal tuyến tính ActiveListingActivationRequested → ActiveListingReserved/ActiveListingActivationRejected → TradableListingCreated/TradableListingStatusChanged ACTIVE.**"}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3. Một InstrumentRegistered cho SUBJECT MỚI (sau một SCOPE_ERROR correction, §19) CÓ THỂ tham chiếu non-causal tới InstrumentFactInvalidated của subject cũ để truy vết, nhưng KHÔNG bắt buộc và KHÔNG phải causal ancestor. ActiveListingActivationRejected (§16) NÊN tham chiếu non-causal tới ActiveListingReserved đang HELD hiện tại. **`related_event_refs` KHÔNG BAO GIỜ được dùng để che giấu một causal dependency thực sự (đóng IRB-C1-V03-MAJ-01, attack scenario 'using related_event_refs to hide a causal dependency') — nếu một event B thực sự phụ thuộc causal vào event A, A PHẢI nằm trong `causation_refs` của B, không phải `related_event_refs`.**"}
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
  ActiveListingActivationRequested: ACTIVE_LISTING_ACTIVATION_REQUESTED
  ActiveListingActivationRequestFactInvalidated: ACTIVE_LISTING_ACTIVATION_REQUEST_FACT_INVALIDATED
  ActiveListingReserved: ACTIVE_LISTING_RESERVED
  ActiveListingReservationReleased: ACTIVE_LISTING_RESERVATION_RELEASED
  ActiveListingActivationRejected: ACTIVE_LISTING_ACTIVATION_REJECTED
  ActiveListingReservationFactInvalidated: ACTIVE_LISTING_RESERVATION_FACT_INVALIDATED
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
  - "KHÔNG được dùng làm input cho bất kỳ Domain Contract khác hay Decision — chỉ query/UI. **`InstrumentCurrentView` KHÔNG PHẢI authority (v0.4, đóng IRB-C1-V03-MAJ-02) — kể cả `TradableListingCurrentView` (§15 Bước 4) cũng KHÔNG được query artifact này làm input; §15 Bước 4 PHẢI reconstruct trực tiếp từ authoritative Instrument event stream (§3–§6) dùng ĐÚNG fold algorithm mô tả tại đây. Một implementation CÓ THỂ dùng row đã materialize của `InstrumentCurrentView` làm cache nội bộ CHỈ KHI provably equivalent với authoritative reconstruction tại CÙNG recorded cursor, effective cursor, contract version, configuration — cache lookup KHÔNG BAO GIỜ thay thế được normative authoritative reconstruction; khi không chứng minh được equivalence (cache stale, cursor lệch, version lệch), PHẢI reconstruct trực tiếp.**"
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
  - "CẤM khi Logical Instrument HOẶC Logical Venue tương ứng đã RETIRED tại envelope.effective_time đó — xác định qua authoritative reconstruction TRỰC TIẾP từ Instrument/Venue event stream (§15 Bước 4–5), KHÔNG qua `InstrumentCurrentView`/`VenueCurrentView` (đóng IRB-C1-MAJ-02, IRB-C1-V03-MAJ-02, đối xứng Instrument/Venue — §1/§10 cross-subject invariant)."
  - "payload.reservation_grant_ref PHẢI trỏ chính ActiveListingReserved (§16) đang grant reservation cho listing_id này cho cặp (instrument_id, venue_id); causation_refs PHẢI THÊM chính event đó — TradableListingCreated KHÔNG hợp lệ nếu không có reservation tương ứng (đóng IRB-C1-MAJ-03). ActiveListingReserved này KHÔNG được causally trỏ ngược lại chính TradableListingCreated này hay bất kỳ event nào phụ thuộc causal vào nó — cấm chu trình causal (đóng IRB-C1-V03-MAJ-01, xem §16)."
  - "**v0.5 (đóng IRB-C1-V04-MAJ-01):** payload.activation_request_id BẮT BUỘC — PHẢI khớp CHÍNH XÁC payload.activation_request_id của ActiveListingReserved mà reservation_grant_ref trỏ tới. reservation_grant_ref PHẢI trỏ ActiveListingReserved với CÙNG activation_request_id VÀ CÙNG (instrument_id, venue_id, listing_id) scope — CẤM dùng grant của request khác (đóng attack scenario 'activation uses grant from another request', 'grant for listing A activating listing B')."
  - "reservation_grant_ref PHẢI là VALID lineage head của ActiveListingReserved tại recorded cursor của TradableListingCreated này (đúng §16 reservation correction lineage) — CẤM dùng một grant đã bị ActiveListingReservationFactInvalidated mà chưa có replacement visible (đóng attack scenario 'activation uses invalidated grant')."
  - "Một ActiveListingReserved chỉ được consume bởi ĐÚNG MỘT activation event (TradableListingCreated HOẶC TradableListingStatusChanged) — CẤM hai activation event cùng trỏ một reservation_grant_ref, TRỪ KHI một trong hai là idempotent duplicate theo §16 dedup algorithm (đóng attack scenario 'two activation events consume one grant')."
  - "**v0.6 (Part E, đóng `IRB-C1-V05-MAJ-01`):** activation_request_id được trỏ tới (qua ActiveListingReserved mà reservation_grant_ref chỉ tới) PHẢI visible VÀ `request_validity_state = VALID` (KHÔNG `TERMINALLY_INVALID`, §16 Terminal request disposition) TẠI recorded cursor của chính TradableListingCreated này — một request invalidation visible tại cursor replay vô hiệu hóa quyền dùng grant đó cho activation MỚI, NGAY CẢ KHI bản thân ActiveListingReserved chưa bị invalidate riêng (đóng attack scenario 'activation consumes grant from terminally invalid request'). KHÔNG rewrite causation lịch sử — invariant này chỉ ràng buộc việc TẠO activation event mới, không sửa causation_refs đã ghi."
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
  activation_request_id: {type: string, required: true, description: "PHẢI khớp payload.activation_request_id của ActiveListingReserved được reservation_grant_ref trỏ tới — đóng IRB-C1-V04-MAJ-01"}
  reservation_grant_ref: {type: event_record_ref, required: true, description: "trỏ chính ActiveListingReserved (§16) grant reservation cho listing_id này — đóng IRB-C1-MAJ-03/IRB-C1-V03-MAJ-01, xem invariants"}
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
  - "new_status = ACTIVE CẤM khi Logical Instrument HOẶC Logical Venue tương ứng đã RETIRED tại effective_time đó — xác định qua authoritative reconstruction TRỰC TIẾP từ Instrument/Venue event stream (§15 Bước 4–5), KHÔNG qua `InstrumentCurrentView`/`VenueCurrentView` (§1/§10 cross-subject invariant, ĐỐI XỨNG — v0.3 đóng IRB-C1-MAJ-02, v0.4 đóng IRB-C1-V03-MAJ-02)."
  - "new_status = ACTIVE: payload.reservation_grant_ref PHẢI trỏ chính ActiveListingReserved (§16) đang grant reservation cho listing_id này cho cặp (instrument_id, venue_id); causation_refs PHẢI THÊM chính event đó — KHÔNG hợp lệ nếu không có reservation tương ứng (đóng IRB-C1-MAJ-03). ActiveListingReserved này KHÔNG được causally trỏ ngược lại chính TradableListingStatusChanged này — cấm chu trình causal (đóng IRB-C1-V03-MAJ-01, xem §16)."
  - "**v0.5 (đóng IRB-C1-V04-MAJ-01):** new_status = ACTIVE: payload.activation_request_id BẮT BUỘC — PHẢI khớp CHÍNH XÁC payload.activation_request_id của ActiveListingReserved mà reservation_grant_ref trỏ tới; VẮNG MẶT khi new_status ∈ {SUSPENDED, DELISTED}. reservation_grant_ref PHẢI trỏ ActiveListingReserved CÙNG activation_request_id VÀ CÙNG (instrument_id, venue_id, listing_id) scope — CẤM dùng grant của request khác."
  - "new_status = ACTIVE: reservation_grant_ref PHẢI là VALID lineage head của ActiveListingReserved tại recorded cursor của TradableListingStatusChanged này — CẤM dùng grant đã ActiveListingReservationFactInvalidated mà chưa có replacement visible."
  - "Một ActiveListingReserved chỉ được consume bởi ĐÚNG MỘT activation event — CẤM hai activation event cùng trỏ một reservation_grant_ref, TRỪ KHI idempotent duplicate theo §16 dedup algorithm."
  - "**v0.6 (Part E, đóng `IRB-C1-V05-MAJ-01`):** new_status = ACTIVE: activation_request_id được trỏ tới (qua ActiveListingReserved mà reservation_grant_ref chỉ tới) PHẢI visible VÀ `request_validity_state = VALID` (KHÔNG `TERMINALLY_INVALID`) TẠI recorded cursor của chính TradableListingStatusChanged này — cùng nguyên tắc §11, không rewrite causation lịch sử."
  - "new_status ∈ {SUSPENDED, DELISTED} khi listing đang held reservation (§16): PHẢI có một ActiveListingReservationReleased tương ứng, causation_refs của event đó trỏ tới chính TradableListingStatusChanged này, reason = VOLUNTARY_STATUS_CHANGE — giải phóng cặp (instrument_id, venue_id) (đóng IRB-C1-MAJ-03)."
payload:
  listing_id: {type: string, required: true}
  new_status: {type: enum, values: [ACTIVE, SUSPENDED, DELISTED], required: true}
  activation_request_id: {type: string, required: false, description: "BẮT BUỘC khi new_status = ACTIVE, VẮNG MẶT khi new_status ∈ {SUSPENDED, DELISTED} — PHẢI khớp payload.activation_request_id của ActiveListingReserved được reservation_grant_ref trỏ tới, đóng IRB-C1-V04-MAJ-01"}
  reservation_grant_ref: {type: event_record_ref, required: false, description: "BẮT BUỘC khi new_status = ACTIVE, VẮNG MẶT khi new_status ∈ {SUSPENDED, DELISTED} — trỏ chính ActiveListingReserved (§16), xem invariants"}
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

**Không phải authoritative event.** Rebuild được từ §11–§14, §16, cùng thứ tự tính toán 7-bước PIN cứng (v0.3/v0.4, đóng `IRB-C1-MAJ-02`/`IRB-C1-MAJ-03`/`IRB-C1-MAJ-04`/`IRB-C1-V03-MAJ-01`/`IRB-C1-V03-MAJ-02`/`IRB-C1-V03-MAJ-03`/`IRB-C1-V03-MAJ-04`) — mọi implementation PHẢI theo đúng thứ tự này, dùng CÙNG cặp cursor (recorded-time cursor, effective-time cursor) và CÙNG Definition/contract version/configuration xuyên suốt cả 7 bước; KHÔNG dùng current/latest parent state cho historical replay; KHÔNG dùng parent Current View làm authority (Bước 4–5); KHÔNG dùng reservation latest/current state cho historical replay (Bước 6).

**Canonical decision — no-row trước khi có fact đầu tiên:**

```text
Trước khi TradableListingCreated tồn tại cho một listing_id:
  → KHÔNG có TradableListingCurrentView row nào tồn tại
  → GetCurrentListing trả về NOT_FOUND / ABSENT
```

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION`. Khi `PENDING_CORRECTION`, `pending_correction_class` BẮT BUỘC có mặt (§19).

**Fold algorithm (v0.4):**

```text
Bước 1 — rebuild valid listing creation lineage head, đúng §7 Bước 1 áp dụng cho
  TradableListingCreated/TradableListingFactInvalidated (§11, §14). NẾU PENDING_CORRECTION (chờ
  same-subject replacement hoặc SCOPE_ERROR vĩnh viễn) → dừng tại đây, view_state =
  PENDING_CORRECTION, pending_correction_class theo §19 mapping, không resolve field nào khác.

Bước 2 — fold TradableListingMetadataRevised (patch), đúng §7 Bước 2 áp dụng cho §12
  (metadata_fold_order_policy, §17).

Bước 3 — fold TradableListingStatusChanged (status), đúng §7 Bước 3 5-phase
  (status_fold_order_policy, §17) → current_status THÔ (chưa tính eligibility/reservation).

Bước 4 — reconstruct Instrument eligibility TRỰC TIẾP từ authoritative Instrument event stream
  (§3–§6), dùng ĐÚNG NGUYÊN VĂN fold algorithm đã pin tại §7 (Bước 1 registration lineage head →
  Bước 2 metadata patch fold → Bước 3 status fold 5-phase), TẠI CÙNG cặp cursor (recorded-time,
  effective-time) đã dùng ở Bước 1–3 của thuật toán này — KHÔNG dùng cursor khác, KHÔNG dùng "hiện
  tại" (đóng attack scenario "Instrument and Venue evaluated at different cursors", IRB-C1-MAJ-02).
  **`InstrumentCurrentView` (§7) KHÔNG PHẢI authority cho bước này (v0.4, đóng
  IRB-C1-V03-MAJ-02) — CẤM query artifact/read-model đó làm input bình thường; CHỈ được dùng một
  row đã materialize của nó làm cache nội bộ NẾU provably equivalent với kết quả reconstruction
  trực tiếp tại CÙNG cặp cursor, CÙNG contract version, CÙNG configuration — nếu không chứng minh
  được equivalence, PHẢI reconstruct trực tiếp từ event stream.** Instrument ELIGIBLE khi: fold
  result view_state = VALID VÀ current_status != RETIRED.

Bước 5 — reconstruct Venue eligibility TRỰC TIẾP từ authoritative Venue event stream (`venue.md`
  §3–§6), dùng ĐÚNG NGUYÊN VĂN fold algorithm `venue.md` §7 (áp dụng nguyên văn `instrument.md`
  §7), TẠI CÙNG cặp cursor y hệt Bước 4 (đối xứng Bước 4, đóng IRB-C1-MAJ-02). **`VenueCurrentView`
  (`venue.md` §7) KHÔNG PHẢI authority cho bước này, cùng nguyên tắc Bước 4 (đóng
  IRB-C1-V03-MAJ-02).** Venue ELIGIBLE khi: fold result view_state = VALID VÀ current_status !=
  RETIRED.

Bước 6 — reconstruct pair-scoped active-listing reservation (§16) TRỰC TIẾP từ authoritative
  reservation event stream (`ActiveListingActivationRequested`/`ActiveListingReserved`/
  `ActiveListingReservationReleased`/`ActiveListingActivationRejected`/
  `ActiveListingReservationFactInvalidated`), dùng `reservation_fold_order_policy` 5-phase (§16,
  §17, đóng IRB-C1-MAJ-04/IRB-C1-V03-MAJ-03/IRB-C1-V03-MAJ-04), TẠI CÙNG cặp cursor (recorded-time,
  effective-time) y hệt Bước 4–5 VÀ CÙNG reservation correction lineage visible tại recorded
  cursor đó (đóng attack scenario "reservation evaluated at different cursor"). Fold result ∈
  {AVAILABLE, HELD, PENDING_CORRECTION} (§16). current_status THÔ (Bước 3) = ACTIVE chỉ HỢP LỆ
  nếu fold result = HELD VÀ holder = listing_id này; nếu fold result = PENDING_CORRECTION, coi
  Bước 6 là PENDING_CORRECTION (không phải defensive fallback — đây là kết quả chính thức của
  reservation correction lineage, §16); nếu event stream mâu thuẫn khác không thuộc hai trường
  hợp trên (không nên xảy ra dưới event stream hợp lệ, §16 invariant), coi là defensive
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
  - "Bước 4/5 (Instrument/Venue eligibility) PHẢI reconstruct trực tiếp từ authoritative event stream tương ứng, KHÔNG được query `InstrumentCurrentView`/`VenueCurrentView` làm input bình thường (đóng IRB-C1-V03-MAJ-02). Bước 6 (reservation) PHẢI dùng `reservation_fold_order_policy` bitemporal (recorded cursor + effective cursor + correction lineage), KHÔNG dùng reservation state 'hiện tại/mới nhất' cho historical replay (đóng IRB-C1-V03-MAJ-04)."
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

**v0.4 (đóng `IRB-C1-V03-MAJ-01`):** v0.3 có chu trình causal — `ActiveListingReserved.causation_refs` trỏ tới activation event (`TradableListingCreated`/`TradableListingStatusChanged`), ĐỒNG THỜI activation event đó (§11, §13) `causation_refs` trỏ NGƯỢC tới `ActiveListingReserved`. v0.4 thêm `ActiveListingActivationRequested` làm pre-arbitration request tường minh, phá vỡ chu trình bằng chuỗi causal TUYẾN TÍNH:

```text
ActiveListingActivationRequested
  → ActiveListingReserved  OR  ActiveListingActivationRejected   (causal tới REQUEST, KHÔNG tới activation event)
  → TradableListingCreated (ACTIVE)  OR  TradableListingStatusChanged (ACTIVE)   (causal tới GRANT, §11/§13)
```

Một request tạo ra ĐÚNG MỘT authoritative arbitration outcome — `ActiveListingReserved` HOẶC `ActiveListingActivationRejected`, KHÔNG BAO GIỜ cả hai.

**Đây là Domain Contract authority rule — KHÔNG author runtime implementation, database locking, hay module design** (Phase 1, deferred, §23).

### `ActiveListingActivationRequested` — `kind: event`

Kế thừa nguyên vẹn envelope §2 (subject_ref.subject_type = TradableListing, scope = {instrument_id, venue_id}, subject_id = listing_id — listing_id được chọn TRƯỚC bởi requester, cùng nguyên tắc `instrument_id`/`listing_id` opaque client-assigned đã khóa xuyên suốt tài liệu; KHÔNG bắt buộc `TradableListingCreated` đã tồn tại — request này là pre-arbitration, độc lập correction lineage §18 của TradableListing). Payload đặc thù:

**v0.5 (đóng `IRB-C1-V04-MAJ-01`):** v0.4 KHÔNG có logical request identity ổn định — `event_id` không đủ, vì retry/redelivery ở tầng ingress (network retry, at-least-once delivery, Phase 1 chưa author cơ chế) có thể tạo NHIỀU physical event record cho CÙNG một business request, mỗi record một `event_id` khác nhau. Không có cách phân biệt "đây là redelivery của request cũ" với "đây là request mới" → không dedup được, không idempotent được, exactly-one-outcome (§16 dưới) không executable dưới retry. v0.5 thêm `activation_request_id` — logical identity ỔN ĐỊNH, độc lập `event_id`.

```yaml
id: active-listing-activation-requested
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE — pre-arbitration request cho việc một listing_id muốn giành reservation cho
  pair (instrument_id, venue_id) (v0.4, đóng IRB-C1-V03-MAJ-01). KHÔNG tự nó thay đổi reservation
  state hay TradableListing state — chỉ ghi nhận "request này đã xảy ra". Là causal predecessor
  DUY NHẤT hợp lệ cho ActiveListingReserved/ActiveListingActivationRejected (§16). Một request
  KHÔNG có grant/reject visible KHÔNG có hiệu lực gì lên listing lifecycle hay reservation state
  (Part B "abandoned request" — không invent runtime retry/timeout scheduling).
invariants:
  - "causation_refs: zero-to-many — activation intent reference (operator/strategy/risk-approved workflow, Phase 1/Package 0.2-C2+ chưa author) HOẶC rỗng nếu request phát sinh từ nguồn khác theo envelope §2 cardinality chung; KHÔNG BAO GIỜ trỏ tới ActiveListingReserved/ActiveListingActivationRejected/TradableListingCreated/TradableListingStatusChanged đang chờ nó — cấm chu trình causal."
  - "envelope.effective_time = effective_time mong muốn của activation nếu request được grant (dùng làm effective_time cho ActiveListingReserved/activation event kết quả, nếu có)."
  - "Một request KHÔNG BAO GIỜ tự nó là causal ancestor của chính nó, trực tiếp hoặc gián tiếp qua bất kỳ chuỗi causation_refs nào (đóng IRB-C1-V03-MAJ-01, attack scenario 'causal cycle attempted')."
  - "`activation_request_id` là opaque, KHÔNG parse (Chapter 6 §6.8), KHÔNG BẰNG `event_id`, KHÔNG regenerate mỗi lần retry/redelivery — CÙNG một business request PHẢI mang CÙNG `activation_request_id` xuyên mọi physical event record của nó (đóng IRB-C1-V04-MAJ-01)."
  - "**Permanent scope binding (Part B):** MỘT KHI `activation_request_id` lần đầu được ghi nhận authoritative (first delivery, xem policy dưới), nó vĩnh viễn gắn CHÍNH XÁC MỘT bộ (instrument_id, venue_id, listing_id, requested_target_status = ACTIVE) — KHÔNG BAO GIỜ đổi. Cùng `activation_request_id` xuất hiện lại với instrument_id/venue_id/listing_id/requested_target_status KHÁC → REJECT tường minh, KHÔNG được diễn giải là correction, request mới, retry, hay superseding request — một activation intent thực sự khác PHẢI dùng `activation_request_id` MỚI."
  - "`activation_request_idempotency_policy: STABLE_ID_SAME_PAYLOAD_IS_IDEMPOTENT` (§17): first delivery (activation_request_id mới + scope hợp lệ) → ghi nhận MỘT authoritative record. Exact retry/redelivery (CÙNG activation_request_id, CÙNG scope bất biến, CÙNG canonical semantic payload — xem định nghĩa đầy đủ dưới) → idempotent duplicate — KHÔNG tạo logical request thứ hai, KHÔNG tạo arbitration outcome thứ hai; physical duplicate record PHẢI bị reject trước authoritative append, hoặc normalize về tham chiếu record đã ghi nhận — KHÔNG BAO GIỜ tồn tại HAI original request fact authoritative cùng logical ID. Changed-payload replay (CÙNG activation_request_id, KHÁC canonical semantic payload) → deterministic conflict → reject; KHÔNG được tự chọn bản mới nhất hay cũ nhất."
  - "**v0.6 (Part I, đóng `IRB-C1-V05-MAJ-01`) — Idempotency sau invalidation:** redelivery CHÍNH XÁC (cùng activation_request_id, cùng canonical semantic payload) cho một request ĐÃ `TERMINALLY_INVALID` (xem Terminal request disposition dưới) KHÔNG tái tạo, KHÔNG kích hoạt lại request — normalize về record `TERMINALLY_INVALID` đã ghi nhận, KHÔNG tạo request mới, KHÔNG tạo arbitration outcome mới (đóng attack scenario 'invalidated request redelivered with same payload'). Redelivery với canonical semantic payload THAY ĐỔI cho một `activation_request_id` đã `TERMINALLY_INVALID` VẪN LÀ deterministic conflict/reject — cùng quy tắc changed-payload chung, KHÔNG có ngoại lệ vì đã invalid (đóng attack scenario 'invalidated request redelivered with changed payload')."
  - "**Không metadata-patchable, không có replacement dưới cùng activation_request_id (Part D v0.5, tái khẳng định Part H v0.6):** `ActiveListingActivationRequested` KHÔNG có `supersedes_fact_ref` — payload bất biến, KHÔNG có 'sửa tại chỗ' dưới cùng activation_request_id trong BẤT KỲ trường hợp nào. Ba trường hợp tách bạch tường minh (v0.6, đóng IRB-C1-V05-MAJ-01, Part H): (1) **ingress-invalid** — request KHÔNG pass validation, bị reject TRƯỚC authoritative append, KHÔNG BAO GIỜ trở thành fact authoritative, KHÔNG cần invalidation (chưa từng tồn tại authoritative); (2) **valid request, business intent sau đó đổi** — request gốc VẪN valid lịch sử cho effective_time của nó, KHÔNG invalidate; intent mới dùng `activation_request_id` MỚI hoàn toàn; (3) **request authoritative SAU ĐÓ phát hiện SAI thực tế** (đã pass validation, đã ghi nhận, factual error phát hiện sau — v0.6, đóng IRB-C1-V05-MAJ-01) — emit `ActiveListingActivationRequestFactInvalidated` (dưới đây), corrected intent dùng `activation_request_id` MỚI. KHÔNG được lẫn lộn ba trường hợp này."
  - "Với mỗi `activation_request_id` hợp lệ: đúng MỘT valid original `ActiveListingActivationRequested` lineage head (đóng Part D) — dedup key là `payload.activation_request_id`, KHÔNG phải `event_id`, KHÔNG phải `subject_ref`."
  - "`activation_request_id` KHÔNG được tái sử dụng xuyên nhiều pair authority stream khác nhau — một ID đã bind với pair (instrument_id, venue_id) nào thì vĩnh viễn thuộc về CHÍNH pair đó (đóng attack scenario 'request ID reused in another pair authority stream')."
  - "**v0.6 (Part G, đóng `IRB-C1-V05-MAJ-01`) — Canonical semantic payload, liệt kê đầy đủ:** identity/scope field (`activation_request_id`, `instrument_id`, `venue_id`, `listing_id`, `requested_target_status`) LUÔN semantic (Part B). `requested_by_ref` LÀ semantic — PHẢI khớp CHÍNH XÁC giữa các physical record cùng `activation_request_id` (bao gồm trường hợp field này chuyển từ absent sang có giá trị hoặc ngược lại); khác nhau → changed-payload replay, deterministic conflict, reject (đóng attack scenario 'requested_by_ref changed under same ID'). `request_reason` LÀ non-authoritative descriptive field — LOẠI KHỎI idempotency equality: hai physical record cùng `activation_request_id`/scope/`requested_by_ref` nhưng khác `request_reason` VẪN LÀ idempotent duplicate, KHÔNG phải conflict (đóng attack scenario 'request_reason changed under same ID') — cùng nguyên tắc field mô tả `reason`/`invalidation_reason` non-canonical xuyên suốt tài liệu này."
  - "**v0.6 — Envelope delivery metadata KHÔNG phải business request scope:** `event_id`/`recorded_time`/transport retry metadata KHÔNG BAO GIỜ tạo logical request mới (dedup key luôn là `payload.activation_request_id`). `source_identity` là delivery/dedup evidence (Chapter 6 §6.6), KHÔNG phải business request scope — thay đổi giữa các physical record cùng `activation_request_id` KHÔNG tạo conflict (đóng attack scenario 'source_identity changed on retry'). `causation_refs` là semantic lineage — PHẢI KHÔNG mâu thuẫn với request gốc (ví dụ không được rỗng ở lần đầu rồi có giá trị ở lần redelivery theo cách ngụ ý một nguồn gốc khác — nếu causation thực sự khác, đây là dấu hiệu business intent khác, xử lý theo changed-payload path) (đóng attack scenario 'causation_refs contradict original request'). `related_event_refs` non-causal, LOẠI KHỎI logical request identity — thay đổi giữa các physical record KHÔNG tạo conflict (đóng attack scenario 'related_event_refs change on retry')."
payload:
  activation_request_id: {type: string, required: true, description: "logical identity ổn định của request — opaque, KHÔNG parse, KHÔNG bằng event_id, KHÔNG regenerate khi retry/redelivery, gắn vĩnh viễn với đúng một (instrument_id, venue_id, listing_id, requested_target_status) — đóng IRB-C1-V04-MAJ-01, xem invariants"}
  instrument_id: {type: string, required: true}
  venue_id: {type: string, required: true}
  listing_id: {type: string, required: true, description: "listing_id đang request activation — opaque, chọn trước bởi requester"}
  requested_target_status: {type: enum, values: [ACTIVE], required: true, description: "phần của permanent scope binding (Part B) — đóng ở v0.5, chỉ ACTIVE; mở rộng giá trị tương lai là Domain Contract revision tường minh"}
  requested_by_ref: {type: string, required: false, description: "opaque reference tới nguồn request (operator/strategy/risk workflow) — KHÔNG author Account/Strategy/Risk ở C1, chỉ opaque reference, deferred §23. SEMANTIC — phần của canonical semantic payload (v0.6, đóng IRB-C1-V05-MAJ-01), PHẢI khớp chính xác cho cùng activation_request_id."}
  request_reason: {type: string, required: false, description: "mô tả tiện dụng cho lý do request — non-authoritative, LOẠI KHỎI idempotency equality (v0.6, đóng IRB-C1-V05-MAJ-01); khác giá trị giữa các physical record cùng activation_request_id KHÔNG tạo conflict."}
```

### `ActiveListingActivationRequestFactInvalidated` — `kind: event` (v0.6, đóng `IRB-C1-V05-MAJ-01`)

Kế thừa nguyên vẹn envelope §2 — `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: active-listing-activation-request-fact-invalidated
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Phủ định MỘT ActiveListingActivationRequested fact ĐÃ pass ingress validation, ĐÃ ghi nhận
  authoritative, rồi SAU ĐÓ phát hiện SAI thực tế (factual error) — đóng gap IRB-C1-V05-MAJ-01
  (v0.5 pin request immutable nhưng không có cơ chế append-only invalidation cho trường hợp
  này). CHỈ target ActiveListingActivationRequested — KHÔNG target ActiveListingReserved,
  ActiveListingActivationRejected, activation event (TradableListingCreated/
  TradableListingStatusChanged), một invalidation khác, hay một request KHÔNG LIÊN QUAN. KHÔNG có
  `supersedes_fact_ref`, KHÔNG có replacement dưới cùng activation_request_id — giữ nguyên quyết
  định bounded "request immutable, không metadata-patchable" (§16, invariant "Không
  metadata-patchable" ở trên); corrected intent PHẢI dùng activation_request_id MỚI.
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_request_fact_ref (TradableListing subject, cùng scope, §10/§16)."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_request_fact_ref."
  - "invalidated_request_fact_ref PHẢI trỏ một ActiveListingActivationRequested, CHƯA từng nhận invalidation khác — một request fact chỉ bị invalidate đúng một lần (cấm double invalidation)."
  - "invalidated_request_fact_ref KHÔNG BAO GIỜ trỏ ActiveListingReserved/ActiveListingActivationRejected/TradableListingCreated/TradableListingStatusChanged/một ActiveListingActivationRequestFactInvalidated khác/một request KHÔNG LIÊN QUAN — CẤM invalidation-of-invalidation, CẤM target ngoài phạm vi request fact, CẤM invalidation subject mismatch."
  - "payload.activation_request_id PHẢI khớp CHÍNH XÁC activation_request_id của invalidated_request_fact_ref (đóng attack scenario 'invalidation targets another request ID')."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_request_fact_ref (đóng rule 1: invalidation recorded sau target)."
  - "Replay tại cursor trước recorded_time của invalidation này thấy request VALID nguyên trạng (rule 7); replay tại cursor >= recorded_time này thấy request TERMINALLY_INVALID (rule 8, chống look-ahead)."
  - "KHÔNG thay đổi identity/scope của request — invalidated_request_fact_ref giữ nguyên nội dung gốc, chỉ bị đánh dấu invalid; append-only, KHÔNG xóa/mutate fact gốc (rule 4, rule 10); request đã invalidate vẫn queryable làm historical evidence (rule 9)."
  - "KHÔNG có supersedes_fact_ref, KHÔNG có replacement request dưới cùng activation_request_id (rule 5) — corrected intent PHẢI dùng activation_request_id MỚI (rule 6, §16 Part H)."
payload:
  invalidated_request_fact_ref: {type: event_record_ref, required: true}
  activation_request_id: {type: string, required: true, description: "PHẢI khớp activation_request_id của invalidated_request_fact_ref — đóng IRB-C1-V05-MAJ-01"}
  request_invalidation_class: {type: enum, values: [FACTUAL_REQUEST_ERROR], required: true}
  invalidation_reason: {type: string, required: false}
```

`ActiveListingActivationRequestFactInvalidated` KHÔNG nằm trong `events_emitted` của `ActiveListingReservation` hay `TradableListing` (§10) — cùng nguyên tắc `ActiveListingActivationRequested` đã pin ở trên, subject là `TradableListing`, không phải reservation subject.

### Terminal request disposition (Part C, v0.6, đóng `IRB-C1-V05-MAJ-01`)

Canonical request validity — đóng, hai giá trị:

```text
request_validity_state ∈ {VALID, TERMINALLY_INVALID}

ActiveListingActivationRequested visible tại cursor VÀ KHÔNG có
ActiveListingActivationRequestFactInvalidated visible tại cùng cursor:
  → request_validity_state = VALID

ActiveListingActivationRequestFactInvalidated visible tại cursor:
  → request_validity_state = TERMINALLY_INVALID
```

**`TERMINALLY_INVALID` KHÔNG BAO GIỜ quay lại `VALID`** — không có cursor, không có replacement, không có sự kiện tương lai nào thay đổi kết quả này cho `activation_request_id` đó (cùng nguyên tắc `TERMINAL_SCOPE_INVALIDATION` đã pin cho Instrument/Venue/TradableListing/Reservation, §19 — nhưng đây là một discriminator RIÊNG, `request_validity_state`, KHÔNG tái sử dụng `pending_correction_class`/`view_state`, vì request family KHÔNG có khái niệm "chờ same-subject replacement": Part B đã cấm tuyệt đối replacement dưới cùng ID, nên KHÔNG có trạng thái tạm thời tương tự `AWAITING_SAME_SUBJECT_REPLACEMENT` — mọi invalidation của request đều vĩnh viễn ngay lập tức).

Một `activation_request_id` MỚI (corrected intent, business intent khác) có validity/outcome lineage ĐỘC LẬP HOÀN TOÀN — không kế thừa `TERMINALLY_INVALID` từ ID cũ, không "làm sống lại" request cũ. Request cũ (`TERMINALLY_INVALID`) vẫn queryable làm historical evidence. **Không retry worker nào được diễn giải một request `TERMINALLY_INVALID` là "đang chờ sửa tạm thời"** — đây là tín hiệu đóng, dừng polling/retry cho `activation_request_id` đó.

### Effect on arbitration outcomes khi request bị invalidate (Part D, v0.6, đóng `IRB-C1-V05-MAJ-01`)

**Invalidation TRƯỚC khi có outcome:** một khi `ActiveListingActivationRequestFactInvalidated` visible tại cursor, KHÔNG một `ActiveListingReserved` hay `ActiveListingActivationRejected` nào được emit SAU đó cho `activation_request_id` này — mọi grant/reject emit sau invalidation là INVALID (vi phạm Part E invariant tại `ActiveListingReserved`/`ActiveListingActivationRejected`, xem dưới).

**Outcome đã tồn tại TRƯỚC khi request invalidate — invalidation KHÔNG xóa ngầm outcome, hệ quả deterministic theo từng trường hợp:**

```text
Trường hợp 1 — đã có ActiveListingActivationRejected:
  request → TERMINALLY_INVALID
  rejection VẪN LÀ historical audit evidence, không bị sửa/xóa
  KHÔNG activation nào được phép xảy ra (đã đúng theo quy tắc reject hiện có, không đổi)

Trường hợp 2 — đã có ActiveListingReserved, activation event CHƯA ghi nhận:
  grant KHÔNG CÒN authorize activation nào nữa (Part E, xem dưới)
  reservation PHẢI được giải phóng qua ActiveListingReservationReleased tường minh,
    reason = REQUEST_INVALIDATION (giá trị MỚI, thêm vào enum reason — xem định nghĩa
    ActiveListingReservationReleased dưới), causation_refs PHẢI chứa chính
    ActiveListingActivationRequestFactInvalidated này
  cho tới khi release VISIBLE VÀ EFFECTIVE: reservation LỊCH SỬ vẫn HELD (reservation state
    history KHÔNG đổi hồi tố) NHƯNG grant KHÔNG eligible cho activation consumption mới —
    đây là HAI khái niệm tách bạch: reservation state (§16 Phase 5 fold — vẫn HELD cho tới
    release) khác với activation authorization eligibility (Part E — mất ngay khi invalidation
    visible, không chờ release)

Trường hợp 3 — đã có ActiveListingReserved VÀ activation event (TradableListingCreated/
  TradableListingStatusChanged ACTIVE) ĐÃ ghi nhận:
  KHÔNG silently mutate activation history — activation event VẪN LÀ historical authoritative
    evidence, causation_refs KHÔNG bị viết lại.
  Request invalidation ĐÁNH DẤU causal request lineage invalid nhưng KHÔNG tự động cascade —
    đây là tín hiệu, KHÔNG phải trigger tự động (tránh vi phạm append-only/no-fabrication khi
    tự động phát sinh một correction event).
  HÀNH ĐỘNG DOWNSTREAM BẮT BUỘC (tái dùng cơ chế đã có, KHÔNG phát minh cơ chế thứ hai):
    operator/hệ thống PHẢI emit TradableListingFactInvalidated (§14) target chính activation
    event đó, đúng initial_fact_correction_class hiện có (METADATA_ERROR hoặc SCOPE_ERROR, §19)
    — việc này TỰ ĐỘNG kích hoạt ActiveListingReservationReleased (reason =
    CORRECTION_INVALIDATION, §16, cơ chế đã pin từ v0.4) theo đúng quy trình hiện hành.
  Cho tới khi TradableListingFactInvalidated đó visible: TradableListing/reservation state giữ
    nguyên "pending correction" ở mức package (không phải view_state mới) — activation event và
    TradableListingCurrentView của nó VẪN eligible/hiển thị bình thường theo mọi quy tắc hiện
    có (§15) cho tới khi correction downstream đó thực sự visible; đây là quyết định có chủ đích
    (không tự động suy đoán) — người vận hành chịu trách nhiệm phát hiện và kích hoạt correction
    downstream, đúng cùng nguyên tắc "invalidation là tín hiệu, không phải tự động hóa" xuyên
    suốt tài liệu này.
```

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
  - "`state_machine` dưới đây mô tả CHỈ hai state 'thực' (AVAILABLE/HELD), driven bởi ActiveListingReserved/ActiveListingReservationReleased. `PENDING_CORRECTION` KHÔNG phải một state trong state_machine này — đó là kết quả fold-level (view_state) khi correction lineage chưa resolve, đúng cùng nguyên tắc view_state tách biệt current_status xuyên suốt tài liệu (§7, §15); xem thuật toán fold 5-phase dưới (đóng IRB-C1-V03-MAJ-03/04)."
schema:
  instrument_id: {type: string, required: true, ref: instrument}
  venue_id: {type: string, required: true, ref: venue}
state_machine:
  initial_state: AVAILABLE
  states: [AVAILABLE, HELD]
  transitions:
    - {from: AVAILABLE, to: HELD, caused_by: ActiveListingReserved}
    - {from: HELD, to: AVAILABLE, caused_by: ActiveListingReservationReleased}
events_emitted: [ActiveListingReserved, ActiveListingReservationReleased, ActiveListingActivationRejected, ActiveListingReservationFactInvalidated]
events_consumed: []
commands: []
queries: []
```

`ActiveListingActivationRequested` (định nghĩa ở trên) KHÔNG nằm trong `events_emitted` của `ActiveListingReservation` — subject của nó là `TradableListing` (§10), không phải reservation subject.

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
  Dùng cho CẢ HAI trường hợp (v0.4, đóng IRB-C1-V03-MAJ-03): (a) original grant, KHÔNG có
  supersedes_fact_ref; (b) same-subject correction replacement sau
  ActiveListingReservationFactInvalidated target chính grant này, CÙNG pair scope, CÓ
  supersedes_fact_ref (§16 correction lineage dưới).
invariants:
  - "CẤM emit khi reservation subject đang ở state HELD bởi một listing_id KHÁC (chưa release) — trường hợp đó PHẢI emit ActiveListingActivationRejected thay vào đó, KHÔNG emit ActiveListingReserved (rule 3)."
  - "payload.activation_request_ref PHẢI trỏ chính ActiveListingActivationRequested đang được grant; causation_refs PHẢI chứa CHÍNH request đó — KHÔNG BAO GIỜ trỏ tới TradableListingCreated/TradableListingStatusChanged (activation event) đang chờ grant này, dù trực tiếp hay gián tiếp qua chuỗi causation (v0.4, đóng IRB-C1-V03-MAJ-01 — activation event MỚI LÀ bên causal PHỤ THUỘC vào grant này, §11/§13, không phải ngược lại)."
  - "envelope.effective_time = effective_time của ActiveListingActivationRequested đang được grant (cùng effective_time, cùng nguyên tắc envelope binding §2)."
  - "recorded_time xác định thứ tự grant xuyên nhiều request đồng thời cho CÙNG pair — KHÔNG dùng sequence của TradableListing stream khác nhau, KHÔNG dùng ingestion arrival order độc lập với recorded_time của CHÍNH reservation stream (đóng rule 4/5)."
  - "supersedes_fact_ref VẮNG MẶT cho original grant; BẮT BUỘC cho same-subject correction replacement — khi có mặt, scope (instrument_id, venue_id) PHẢI GIỐNG HỆT fact bị supersede (nếu pair khác, đây là RESERVATION_PAIR_SCOPE_ERROR — đăng ký dưới reservation subject ĐÚNG, không dùng supersedes_fact_ref, xem correction lineage dưới). **v0.5:** replacement PHẢI giữ NGUYÊN `activation_request_id` — correction KHÔNG BAO GIỜ đổi request nào đang được grant (đóng IRB-C1-V04-MAJ-01, Part F)."
  - "**v0.5 (đóng IRB-C1-V04-MAJ-01):** payload.activation_request_id BẮT BUỘC, PHẢI khớp CHÍNH XÁC payload.activation_request_id của event mà activation_request_ref trỏ tới — `activation_request_ref` trỏ event, `activation_request_id` là logical key; hai giá trị PHẢI đồng thuận (đóng attack scenario 'outcome request ref and request ID disagree')."
  - "**v0.5 — Exactly-one-outcome keyed theo activation_request_id (đóng IRB-C1-V04-MAJ-01, thay thế cách keying chỉ theo event ref của v0.4):** Với mỗi activation_request_id hợp lệ, đúng MỘT valid ORIGINAL arbitration outcome lineage — ActiveListingReserved XOR ActiveListingActivationRejected, KHÔNG BAO GIỜ cả hai cùng activation_request_id (kể cả khi activation_request_ref trỏ tới các physical event record khác nhau do redelivery — dedup PHẢI xảy ra ở tầng activation_request_id trước khi outcome được ghi nhận). CẤM: hai ActiveListingReserved gốc cùng activation_request_id; outcome quyết định bởi ingestion order."
  - "Outcome instrument_id/venue_id/listing_id PHẢI khớp CHÍNH XÁC scope bất biến của activation_request_id tương ứng (Part B) — CẤM grant cho listing/pair khác với request gốc."
  - "**v0.6 (Part E, đóng `IRB-C1-V05-MAJ-01`):** activation_request_id được trỏ tới PHẢI visible VÀ `request_validity_state = VALID` (KHÔNG `TERMINALLY_INVALID`, §16 Terminal request disposition) TẠI recorded cursor của chính ActiveListingReserved này — CẤM emit grant sau khi ActiveListingActivationRequestFactInvalidated của request đó đã visible."
  activation_request_id: {type: string, required: true, description: "PHẢI khớp payload.activation_request_id của request được activation_request_ref trỏ tới — logical outcome key, đóng IRB-C1-V04-MAJ-01"}
  instrument_id: {type: string, required: true}
  venue_id: {type: string, required: true}
  listing_id: {type: string, required: true, description: "listing đang giữ reservation"}
  activation_request_ref: {type: event_record_ref, required: true, description: "trỏ chính ActiveListingActivationRequested đang được grant — đóng IRB-C1-V03-MAJ-01"}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho original grant; BẮT BUỘC cho same-subject correction replacement — đóng IRB-C1-V03-MAJ-03"}
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
  KHÔNG tự động cấp lại cho bất kỳ listing nào khác. **v0.4 (đóng IRB-C1-V03-MAJ-03):** dùng cho
  CẢ HAI trường hợp: (a) original release, KHÔNG có supersedes_fact_ref; (b) same-subject
  correction replacement sau ActiveListingReservationFactInvalidated target chính release này, CÓ
  supersedes_fact_ref. **v0.4 (Part G, làm rõ hành vi):** invalidate activation event đang HELD
  reservation (§14) TỰ NÓ KHÔNG rewrite reservation fact — event release này là BẮT BUỘC, riêng
  biệt, causally-linked; cho tới khi release VISIBLE (recorded_time) VÀ EFFECTIVE (effective_time),
  reservation VẪN held; replay trước release tiếp tục thấy held; replay sau release thấy
  available. Nếu bản thân grant gốc SAI (không phải activation event sai) thì dùng reservation
  correction lineage (RESERVATION_METADATA_ERROR/RESERVATION_PAIR_SCOPE_ERROR dưới), KHÔNG dùng
  release đơn thuần. **v0.6 (đóng IRB-C1-V05-MAJ-01):** reason thêm giá trị REQUEST_INVALIDATION
  — dùng khi grant đã cấp nhưng activation event CHƯA ghi nhận, VÀ activation request gốc bị
  ActiveListingActivationRequestFactInvalidated (§16 Part D) — cùng nguyên tắc tách bạch reservation
  state history khỏi activation authorization eligibility như CORRECTION_INVALIDATION.
invariants:
  - "CHỈ hợp lệ khi reservation subject đang ở state HELD bởi đúng listing_id trong payload (tại effective_time của chính release này, theo reservation fold §16)."
  - "reason = VOLUNTARY_STATUS_CHANGE: causation_refs PHẢI chứa chính TradableListingStatusChanged (new_status ∈ {SUSPENDED, DELISTED}) gây ra release này."
  - "reason = CORRECTION_INVALIDATION: causation_refs PHẢI chứa chính TradableListingFactInvalidated (§14) đang invalidate activation event (TradableListingCreated hoặc TradableListingStatusChanged mang new_status=ACTIVE) đang held reservation này — đóng rule 7 'correction/invalidation of the winning activation or reservation causes deterministic re-evaluation'. Bản thân invalidation đó KHÔNG tự động đổi reservation state — CHÍNH release event này (khi visible và effective) mới đổi."
  - "**v0.6 (đóng IRB-C1-V05-MAJ-01):** reason = REQUEST_INVALIDATION: causation_refs PHẢI chứa chính ActiveListingActivationRequestFactInvalidated (§16 Part D) đang invalidate activation request gốc của grant đang HELD này — CHỈ hợp lệ khi activation event (TradableListingCreated/TradableListingStatusChanged mang new_status=ACTIVE) CHƯA ghi nhận cho grant này (nếu ĐÃ ghi nhận, dùng reason = CORRECTION_INVALIDATION qua TradableListingFactInvalidated, §16 Part D Trường hợp 3, KHÔNG dùng REQUEST_INVALIDATION). Bản thân request invalidation KHÔNG tự động đổi reservation state — CHÍNH release event này (khi visible và effective) mới đổi; cho tới đó, reservation LỊCH SỬ vẫn HELD nhưng grant KHÔNG eligible activation consumption mới (Part E)."
  - "Sau release VISIBLE VÀ EFFECTIVE, reservation subject = AVAILABLE — một listing_id KHÁC (kể cả một listing từng bị ActiveListingActivationRejected trước đó cho pair này) KHÔNG tự động trở thành holder mới; CẦN một ActiveListingActivationRequested + ActiveListingReserved MỚI, PHẢI xảy ra SAU khi release này visible (recorded_time) — cấm automatic promotion (đóng rule 8, 'preferred rule': không có candidate 'chờ sẵn')."
  - "supersedes_fact_ref VẮNG MẶT cho original release; BẮT BUỘC cho same-subject correction replacement (ví dụ reason ghi sai) — khi có mặt, scope (instrument_id, venue_id) PHẢI GIỐNG HỆT fact bị supersede."
payload:
  instrument_id: {type: string, required: true}
  venue_id: {type: string, required: true}
  listing_id: {type: string, required: true}
  reason: {type: enum, values: [VOLUNTARY_STATUS_CHANGE, CORRECTION_INVALIDATION, REQUEST_INVALIDATION], required: true}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho original release; BẮT BUỘC cho same-subject correction replacement — đóng IRB-C1-V03-MAJ-03"}
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
  'two listing activations recorded concurrently on separate streams'). **v0.4 (đóng
  IRB-C1-V03-MAJ-01/IRB-C1-V03-MAJ-03):** causal predecessor là ActiveListingActivationRequested
  (KHÔNG phải activation event); dùng cho CẢ HAI trường hợp: original rejection (KHÔNG có
  supersedes_fact_ref) hoặc same-subject correction replacement (CÓ supersedes_fact_ref).
invariants:
  - "CHỈ hợp lệ khi reservation subject đang ở state HELD bởi một listing_id KHÁC listing_id trong payload tại thời điểm request."
  - "payload.activation_request_ref PHẢI trỏ chính ActiveListingActivationRequested đang bị từ chối; causation_refs PHẢI chứa CHÍNH request đó — KHÔNG BAO GIỜ trỏ tới TradableListingCreated/TradableListingStatusChanged (activation event không tồn tại/không hợp lệ trong trường hợp reject, đóng IRB-C1-V03-MAJ-01)."
  - "related_event_refs (non-causal) NÊN trỏ chính ActiveListingReserved đang HELD hiện tại, cho mục đích truy vết — không bắt buộc."
  - "Rejected listing KHÔNG được coi là 'candidate chờ' — không có promotion tự động khi holder release (đóng rule 8)."
  - "**v0.5 (đóng IRB-C1-V04-MAJ-01):** payload.activation_request_id BẮT BUỘC, PHẢI khớp CHÍNH XÁC payload.activation_request_id của event mà activation_request_ref trỏ tới (đóng attack scenario 'outcome request ref and request ID disagree')."
  - "**v0.5 — Exactly-one-outcome keyed theo activation_request_id:** Với mỗi activation_request_id hợp lệ, đúng MỘT valid ORIGINAL arbitration outcome lineage — ActiveListingReserved XOR ActiveListingActivationRejected, KHÔNG BAO GIỜ cả hai cùng activation_request_id. CẤM: hai ActiveListingActivationRejected gốc cùng activation_request_id; outcome quyết định bởi ingestion order."
  - "rejected_listing_id PHẢI khớp CHÍNH XÁC listing_id bất biến của activation_request_id tương ứng (Part B) — CẤM rejection nêu tên listing/pair khác với request gốc."
  - "**v0.6 (Part E, đóng `IRB-C1-V05-MAJ-01`):** activation_request_id được trỏ tới PHẢI visible VÀ `request_validity_state = VALID` (KHÔNG `TERMINALLY_INVALID`, §16 Terminal request disposition) TẠI recorded cursor của chính ActiveListingActivationRejected này — CẤM emit rejection sau khi ActiveListingActivationRequestFactInvalidated của request đó đã visible."
  - "supersedes_fact_ref VẮNG MẶT cho original rejection; BẮT BUỘC cho same-subject correction replacement (ví dụ held_by_listing_id ghi sai) — khi có mặt, scope (instrument_id, venue_id) PHẢI GIỐNG HỆT fact bị supersede, VÀ activation_request_id PHẢI giữ NGUYÊN — correction KHÔNG BAO GIỜ đổi request nào đang bị reject (đóng IRB-C1-V04-MAJ-01, Part F)."
payload:
  activation_request_id: {type: string, required: true, description: "PHẢI khớp payload.activation_request_id của request được activation_request_ref trỏ tới — logical outcome key, đóng IRB-C1-V04-MAJ-01"}
  instrument_id: {type: string, required: true}
  venue_id: {type: string, required: true}
  rejected_listing_id: {type: string, required: true}
  held_by_listing_id: {type: string, required: true, description: "listing hiện đang giữ reservation tại thời điểm reject"}
  activation_request_ref: {type: event_record_ref, required: true, description: "trỏ chính ActiveListingActivationRequested bị từ chối — đóng IRB-C1-V03-MAJ-01"}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho original rejection; BẮT BUỘC cho same-subject correction replacement — đóng IRB-C1-V03-MAJ-03"}
```

### `ActiveListingReservationFactInvalidated` — `kind: event` (v0.4, đóng `IRB-C1-V03-MAJ-03`)

Kế thừa nguyên vẹn envelope §2 — `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: active-listing-reservation-fact-invalidated
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Phủ định MỘT fact lịch sử cụ thể ĐÃ SAI của `ActiveListingReservation` — cùng nguyên tắc
  `InstrumentFactInvalidated` (§6)/`TradableListingFactInvalidated` (§14), áp dụng cho họ
  reservation. v0.3 KHÔNG có cơ chế này (reservation fact không correctable) — v0.4 đóng gap này
  (đóng IRB-C1-V03-MAJ-03).
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref — cùng reservation subject (instrument_id, venue_id)."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref."
  - "invalidated_fact_ref PHẢI trỏ một ActiveListingReserved, ActiveListingReservationReleased, hoặc ActiveListingActivationRejected, CHƯA từng nhận invalidation khác — một fact chỉ bị invalidate đúng một lần."
  - "invalidated_fact_ref KHÔNG BAO GIỜ trỏ một ActiveListingReservationFactInvalidated khác — cấm invalidation-of-invalidation."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead)."
  - "reservation_correction_class BẮT BUỘC có mặt, một trong hai giá trị đóng: RESERVATION_METADATA_ERROR (same-pair correction — cùng (instrument_id, venue_id), chờ replacement CÙNG reservation subject, supersedes_fact_ref trỏ về đây) hoặc RESERVATION_PAIR_SCOPE_ERROR (fact gốc gán SAI pair — CẤM replacement dưới reservation subject cũ, correction thực tế nằm ở việc emit fact ĐÚNG dưới reservation subject khác/đúng, KHÔNG dùng supersedes_fact_ref trỏ về đây)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  reservation_correction_class: {type: enum, values: [RESERVATION_METADATA_ERROR, RESERVATION_PAIR_SCOPE_ERROR], required: true}
  invalidation_reason: {type: string, required: false}
```

### Reservation correction lineage (Part D, đóng `IRB-C1-V03-MAJ-03`)

Correction lineage scoped chính xác theo `(reservation subject (instrument_id, venue_id), effective_time)` — cùng nguyên tắc §18, áp dụng cho họ reservation.

```text
RESERVATION_METADATA_ERROR (same-pair correction):
  invalidate erroneous reservation fact (ActiveListingReservationFactInvalidated,
    reservation_correction_class = RESERVATION_METADATA_ERROR)
  → emit corrected replacement fact CÙNG event type (Reserved→Reserved,
    Released→Released, Rejected→Rejected), CÙNG reservation subject (instrument_id, venue_id),
    supersedes_fact_ref trỏ về fact vừa invalidate

RESERVATION_PAIR_SCOPE_ERROR (wrong pair identity):
  invalidate erroneous reservation fact (ActiveListingReservationFactInvalidated,
    reservation_correction_class = RESERVATION_PAIR_SCOPE_ERROR)
  → KHÔNG replace dưới reservation subject cũ — CẤM supersedes_fact_ref trỏ về đây
  → emit fact ĐÚNG dưới reservation subject KHÁC (pair (instrument_id, venue_id) đúng)
```

Mười invariant tại §18 áp dụng nguyên văn cho họ reservation (original không supersedes_fact_ref; replacement bắt buộc có; cùng subject/effective_time; supersede đúng lineage head; cấm nhảy cóc; cấm fork; replacement không visible trước invalidation; append-only; loại trừ fact đã invalidate khỏi reservation fold; forward-looking KHÔNG áp dụng cho họ reservation — mọi reservation fact là point-in-time authoritative, không có khái niệm "forward revision" riêng).

**v0.5 (Part F, đóng `IRB-C1-V04-MAJ-01`) — Outcome type bất biến, đúng MỘT outcome lineage gốc per `activation_request_id`:**

```text
Với mỗi activation_request_id hợp lệ: đúng MỘT valid ORIGINAL arbitration outcome lineage
  (ActiveListingReserved-lineage XOR ActiveListingActivationRejected-lineage).

Correction (RESERVATION_METADATA_ERROR) tạo replacement record TRONG CÙNG lineage đó — KHÔNG
  BAO GIỜ tạo lineage độc lập thứ hai cho cùng activation_request_id.

ActiveListingReserved correction  → replacement VẪN LÀ ActiveListingReserved, CÙNG activation_request_id.
ActiveListingActivationRejected correction → replacement VẪN LÀ ActiveListingActivationRejected, CÙNG activation_request_id.

Outcome type (grant vs reject) BẤT BIẾN cho MỘT arbitration decision — supersedes_fact_ref
  KHÔNG BAO GIỜ được dùng để flip type (Reserved→Rejected hay Rejected→Reserved).

Quyết định sai cần đảo type (ví dụ đã reject nhưng lẽ ra phải grant):
  1. invalidate outcome fact sai (ActiveListingReservationFactInvalidated, đúng correction rules
     hiện có ở trên)
  2. record một activation request MỚI, activation_request_id MỚI HOÀN TOÀN
  3. pair authority evaluate lại request mới đó theo đúng quy trình bình thường (§16 Part B)
  KHÔNG silently flip type dưới cùng activation_request_id.
```

**Part E — Reservation event scope/identity validation:** Với MỌI reservation event (Reserved/Released/ActivationRejected/ReservationFactInvalidated), `subject_ref.subject_type = ActiveListingReservation`, `subject_id` = reservation_id deterministic từ (instrument_id, venue_id) (§16 entity). Payload listing reference PHẢI khớp pair: `listing.instrument_id == reservation.instrument_id` VÀ `listing.venue_id == reservation.venue_id` (xác minh qua TradableListing subject scope, §10) — CẤM: grant cho listing thuộc pair khác; release cho pair khác; rejection nêu tên holder không liên quan tới pair; replacement "same-subject correction" nhưng thực chất chuyển sang reservation subject khác (đó PHẢI là RESERVATION_PAIR_SCOPE_ERROR, không phải RESERVATION_METADATA_ERROR).

### Bitemporal reservation replay — `reservation_fold_order_policy` (Part F, đóng `IRB-C1-V03-MAJ-04`)

**`reservation_fold_order_policy: RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER`** (§17) — cùng shape 5-phase với `status_fold_order_policy` (§7 Bước 3), áp dụng cho reservation event stream của một pair:

```text
Phase 1 — recorded visibility: giữ lại CHỈ ActiveListingReserved/ActiveListingReservationReleased/
  ActiveListingActivationRejected/ActiveListingReservationFactInvalidated có
  recorded_time <= recorded cursor.

Phase 2 — correction lineage: loại bỏ fact đã bị ActiveListingReservationFactInvalidated visible
  tại cursor; chọn lineage head hợp lệ theo reservation correction lineage (trên); cấm fork/nhảy
  cóc; KHÔNG dùng một replacement chưa visible tại cursor.

Phase 3 — effective eligibility: một reservation fact hợp lệ (sau Phase 1–2) chỉ tham gia fold
  khi effective_time <= effective cursor. Future-effective grant/release ĐÃ recorded (Phase 1
  visible) nhưng effective_time > cursor hiện tại KHÔNG ảnh hưởng fold result tại cursor đó — chỉ
  ảnh hưởng từ cursor >= effective_time của nó trở đi (không look-ahead, đóng attack scenario
  "future-effective grant/release already recorded", "replay before grant/release effective
  time").

Phase 4 — deterministic ordering: trong CHÍNH pair authority stream, sắp fact hợp lệ (sau Phase
  1–3) theo (1) effective_time ASC, (2) recorded_time ASC, (3) event_id ASC. Raw `sequence` KHÔNG
  đủ xuyên nhiều stream khác nhau (Chapter 8) — cho pair authority stream, canonical total order
  VẪN LÀ effective_time/recorded_time/event_id, KHÔNG dùng sequence để override.

Phase 5 — fold reservation state:
  AVAILABLE + ActiveListingReserved (grant hợp lệ, activation_request_ref hợp lệ) → HELD
  HELD + ActiveListingReservationReleased (khớp listing_id đang held) → AVAILABLE
  ActiveListingActivationRejected → KHÔNG đổi state, audit outcome only
  Event không tương thích với state hiện tại (ví dụ Released khi đang AVAILABLE, Reserved khi
    đang HELD bởi listing khác không qua Rejected trước đó) → conflict deterministic, KHÔNG
    resolve bằng arrival order — fold result = PENDING_CORRECTION (defensive).

  Fold result cuối cùng ∈ {AVAILABLE, HELD, PENDING_CORRECTION} — AVAILABLE/HELD tương ứng
  view_state = VALID (correction lineage sạch); PENDING_CORRECTION tương ứng view_state =
  PENDING_CORRECTION, mapping pending_correction_class đúng §19 (RESERVATION_METADATA_ERROR →
  AWAITING_SAME_SUBJECT_REPLACEMENT, RESERVATION_PAIR_SCOPE_ERROR → TERMINAL_SCOPE_INVALIDATION).
```

Đây là thuật toán DUY NHẤT hợp lệ để §15 Bước 6 tiêu thụ — không dùng `ActiveListingActivationRejected` để xác định holder (đó chỉ là audit record, không authoritative cho state, per Phase 5). KHÔNG có read model/Current View top-level riêng cho `ActiveListingReservation` ở C1 — `TradableListingCurrentView` (§15 Bước 6) là điểm consume DUY NHẤT của reservation fold result cho mục đích derived eligibility; không Domain Contract nào khác được query reservation event stream trực tiếp làm input cho Decision/Risk/Execution (đối xứng I-12, Chapter 7 §7.4).

### Request dedup và replay algorithm (Part H v0.5 → Part F v0.6, đóng `IRB-C1-V04-MAJ-01`/`IRB-C1-V05-MAJ-01`)

Thuật toán lookup deterministic DUY NHẤT hợp lệ cho việc resolve một `activation_request_id` — dùng bởi implementation khi xử lý ingress redelivery, và bởi mọi historical replay/correction replay liên quan tới request/outcome. **v0.6 mở rộng từ 7 bước (v0.5) thành 10 bước — thêm resolve/classify request validity (Bước 3–4), đóng `IRB-C1-V05-MAJ-01`:**

```text
Bước 1 — group ActiveListingActivationRequested visible tại recorded cursor theo
  payload.activation_request_id.

Bước 2 — với mỗi activation_request_id, resolve ĐÚNG MỘT valid original authoritative request
  fact (Part D v0.5 — request KHÔNG có correction lineage dạng supersedes_fact_ref; nếu ingress
  nhận nhiều physical record cùng activation_request_id, chỉ MỘT được ghi nhận authoritative,
  phần còn lại là idempotent duplicate — reject trước append hoặc normalize về record đã ghi
  nhận, Part C v0.5).

Bước 3 — (v0.6) resolve ActiveListingActivationRequestFactInvalidated visibility cho request fact
  đó tại CÙNG recorded cursor — có visible invalidation hay không (§16 Part A/Terminal request
  disposition).

Bước 4 — (v0.6) classify request theo Bước 3:
    KHÔNG có invalidation visible → request_validity_state = VALID
    CÓ invalidation visible      → request_validity_state = TERMINALLY_INVALID (vĩnh viễn,
                                     §16 Terminal request disposition — KHÔNG BAO GIỜ quay lại VALID)

Bước 5 — verify permanent scope binding VÀ canonical semantic payload (Part B, Part G): với MỌI
  physical record cùng activation_request_id (kể cả record đến sau khi đã TERMINALLY_INVALID,
  Part I) — (instrument_id, venue_id, listing_id, requested_target_status, requested_by_ref)
  PHẢI khớp chính xác record authoritative; `request_reason` LOẠI KHỎI so sánh này (non-semantic).
  Record nào không khớp là changed-payload replay, reject — KHÔNG BAO GIỜ tự chọn bản mới nhất/
  cũ nhất, KHÔNG BAO GIỜ tái tạo/kích hoạt lại một request TERMINALLY_INVALID (đóng
  IRB-C1-V05-MAJ-01, attack scenario 'invalidated request redelivered with same/changed payload').

Bước 6 — CHỈ NẾU request_validity_state = VALID (Bước 4): resolve đúng MỘT valid arbitration
  outcome lineage cho activation_request_id đó (Part E v0.5) — ActiveListingReserved-lineage XOR
  ActiveListingActivationRejected-lineage, theo reservation correction lineage (trên) VÀ
  `reservation_fold_order_policy` visible tại CÙNG recorded cursor.

Bước 7 — NẾU outcome = grant (ActiveListingReserved lineage head VALID) VÀ request VALID (Bước 4):
    cho phép ĐÚNG MỘT activation lifecycle event (TradableListingCreated hoặc
    TradableListingStatusChanged mang new_status=ACTIVE) tham chiếu reservation_grant_ref/
    activation_request_id này — event thứ hai tham chiếu cùng cặp (activation_request_id,
    reservation_grant_ref) là idempotent duplicate của event thứ nhất, KHÔNG phải activation hợp
    lệ thứ hai (đóng attack scenario 'two activation events consume one grant').

Bước 8 — NẾU outcome = rejection (ActiveListingActivationRejected lineage head VALID):
    CẤM tuyệt đối mọi activation lifecycle event tham chiếu activation_request_id này.

Bước 9 — (v0.6) NẾU request_validity_state = TERMINALLY_INVALID (Bước 4), BẤT KỂ outcome resolve
  được ở Bước 6 là gì: CẤM tuyệt đối mọi arbitration outcome MỚI (ActiveListingReserved/
  ActiveListingActivationRejected emit sau invalidation là INVALID, §16 Part D/E) VÀ CẤM mọi
  activation lifecycle event MỚI tham chiếu activation_request_id này — outcome/activation event
  ĐÃ tồn tại TRƯỚC invalidation vẫn là historical evidence (§16 Part D, xử lý theo ba trường hợp
  đã pin), nhưng KHÔNG được dùng làm căn cứ cho hành động MỚI.

Bước 10 — NẾU không có outcome nào visible tại cursor VÀ request VALID (Bước 6 trả về rỗng, Bước 4
  = VALID): KHÔNG có hiệu lực gì lên listing lifecycle hay reservation state (§16 "abandoned
  request", Part B) — KHÔNG suy đoán, KHÔNG chờ với timeout ngầm định.
```

Mọi bước dùng CÙNG recorded-time cursor (visibility), effective-time cursor (khi áp dụng, ví dụ Phase 3 của reservation fold cho Bước 6), correction lineage hợp lệ của outcome VÀ của request invalidation (Bước 3), VÀ CÙNG contract version/configuration — logical `activation_request_id` PHẢI sống sót nguyên vẹn qua mọi replay/redelivery (đóng attack scenario "historical replay before/after request/outcome/invalidation").

**Optional implementation cache (Part I v0.5, quyết định KHÔNG thêm read model chính thức):** thuật toán trên đã mô tả đầy đủ deterministic lookup — KHÔNG cần một `read_model` artifact riêng cho request status ở C1. Một implementation CÓ THỂ tổ chức cache nội bộ non-authoritative, subordinate, keyed theo `activation_request_id`, với state minh họa `REQUESTED`/`GRANTED`/`REJECTED`/`TERMINALLY_INVALID` (rebuild được từ Bước 1–10 trên) — đây CHỈ là gợi ý hình dạng cache, KHÔNG phải một Domain Contract concept mới, KHÔNG bắt buộc author, và KHÔNG BAO GIỜ là authority (đúng nguyên tắc I-12/Chapter 7 §7.4 xuyên suốt tài liệu).

## 17. Canonical policy identifiers — nguồn duy nhất

**Bảy canonical policy identifier, khai báo ĐÚNG MỘT LẦN tại đây — mọi nơi khác trong tài liệu chỉ tham chiếu theo tên, không lặp lại chuỗi (đóng trước lớp lỗi IRB-B2-MIN-01-style):**

```yaml
revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET
initial_fact_correction_policy: INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES
metadata_fold_order_policy: effective_time_asc_then_recorded_time_asc_then_stream_id_asc_then_registry_version_asc_then_sequence_asc_then_event_id_asc
status_fold_order_policy: RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER
active_listing_arbitration_policy: PAIR_SCOPED_AUTHORITATIVE_RESERVATION
reservation_fold_order_policy: RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER
activation_request_idempotency_policy: STABLE_ID_SAME_PAYLOAD_IS_IDEMPOTENT
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

**`active_listing_arbitration_policy: PAIR_SCOPED_AUTHORITATIVE_RESERVATION`** (v0.3, đóng `IRB-C1-MAJ-03`; v0.4 phá vỡ chu trình causal, đóng `IRB-C1-V03-MAJ-01`) — xem §16 cho định nghĩa đầy đủ: pair-scoped `ActiveListingReservation` subject là authority boundary duy nhất cho "tối đa một ACTIVE listing per (instrument_id, venue_id)"; chuỗi causal tuyến tính `ActiveListingActivationRequested` → `ActiveListingReserved`/`ActiveListingActivationRejected` → activation event; không dùng raw cross-stream sequence hay ingestion order; không automatic promotion sau release.

**`reservation_fold_order_policy: RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER`** (v0.4, đóng `IRB-C1-V03-MAJ-04`) — xem §16 cho thuật toán 5-phase đầy đủ (đối xứng `status_fold_order_policy`): recorded visibility → correction lineage → effective eligibility → deterministic ordering (effective_time/recorded_time/event_id, KHÔNG dùng raw sequence) → fold reservation state (AVAILABLE/HELD/PENDING_CORRECTION). Reservation fact nay correctable qua `ActiveListingReservationFactInvalidated` (đóng `IRB-C1-V03-MAJ-03`).

**`activation_request_idempotency_policy: STABLE_ID_SAME_PAYLOAD_IS_IDEMPOTENT`** (v0.5, đóng `IRB-C1-V04-MAJ-01`) — xem §16 cho định nghĩa đầy đủ: `activation_request_id` là logical identity ổn định, độc lập `event_id`, gắn vĩnh viễn đúng một (instrument_id, venue_id, listing_id, requested_target_status). Exact retry/redelivery (cùng ID, cùng scope, cùng payload) là idempotent duplicate — không tạo request thứ hai, không tạo outcome thứ hai. Changed-payload replay (cùng ID, khác scope/semantics) là deterministic conflict, reject. Exactly-one arbitration outcome (ActiveListingReserved XOR ActiveListingActivationRejected) keyed theo `activation_request_id`, không phải theo event ref đơn thuần. Xem §16 "Request dedup và replay algorithm" cho thuật toán lookup đầy đủ.

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

`ActiveListingReserved`/`ActiveListingReservationReleased`/`ActiveListingActivationRejected` (§16) **NAY CÓ correction lineage riêng qua `ActiveListingReservationFactInvalidated`** (v0.4, đóng `IRB-C1-V03-MAJ-03` — v0.3 KHÔNG có cơ chế này, đây là gap đã đóng). Hai kênh correction tách bạch, KHÔNG nhầm lẫn: (a) sửa reservation FACT tự nó ghi sai (grant sai listing_id, release sai reason, reject sai holder) → dùng `ActiveListingReservationFactInvalidated` + replacement, đúng mười invariant trên; (b) activation event ĐANG HELD reservation bị invalidate vì lý do khác (ví dụ TradableListing scope sai) → dùng `ActiveListingReservationReleased` (reason: `CORRECTION_INVALIDATION`) causally-linked tới `TradableListingFactInvalidated`, KHÔNG phải sửa reservation fact — reservation grant tự nó vẫn ĐÚNG tại thời điểm nó được cấp, chỉ là listing đang giữ nó không còn hợp lệ (§16 Part G).

**`ActiveListingActivationRequested` (§16) là một MẪU HÌNH THỨ BA, tách bạch với cả hai mẫu hình trên** (v0.6, đóng `IRB-C1-V05-MAJ-01`): dùng `ActiveListingActivationRequestFactInvalidated` — invalidation-ONLY, KHÔNG BAO GIỜ có replacement/`supersedes_fact_ref` dưới cùng `activation_request_id` (khác mười invariant trên, vốn LUÔN đi kèm một replacement bắt buộc). Đây là quyết định bounded tường minh (§16 Part D/H): request là pre-arbitration intent, KHÔNG phải reference data mutable — một request sai KHÔNG được "sửa", chỉ được đánh dấu vĩnh viễn invalid; intent đã sửa PHẢI mang danh tính hoàn toàn mới (`activation_request_id` mới). Bảy trong số mười invariant chung vẫn áp dụng (recorded-sau-target, tối đa một invalidation, cấm invalidation-of-invalidation, append-only, loại trừ khỏi validity resolution, không mutate); ba invariant về replacement (2, 3 phần "replacement", 4, 5) KHÔNG áp dụng vì không có replacement.

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
  reservation_correction_class = RESERVATION_METADATA_ERROR (§16)       → AWAITING_SAME_SUBJECT_REPLACEMENT
  reservation_correction_class = RESERVATION_PAIR_SCOPE_ERROR (§16)     → TERMINAL_SCOPE_INVALIDATION
  reservation state conflict defensive case (§16 Phase 5)                → AWAITING_SAME_SUBJECT_REPLACEMENT
```

Mapping `reservation_correction_class` (v0.4, đóng `IRB-C1-V03-MAJ-03`) là mở rộng tương tự `initial_fact_correction_class` áp dụng cho họ `ActiveListingReservation` — hai enum riêng biệt (tên khác nhau, giá trị khác nhau), nhưng cùng nguyên tắc đóng: METADATA_ERROR-style → tạm thời/chờ replacement; PAIR_SCOPE_ERROR-style (đối xứng SCOPE_ERROR) → vĩnh viễn. Xem §16 cho định nghĩa đầy đủ.

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
- `ActiveListingActivationRequested.requested_by_ref` (§16, v0.4) hiện là opaque reference, chưa gắn với Account/Strategy/Risk approval workflow cụ thể — deferred tới Package 0.2-C2+ (Account/Strategy/Risk chưa authorize/author ở C1).
- Cơ chế phát hiện/khởi tạo timeout cho một `ActiveListingActivationRequested` không nhận được grant/reject (request "bị bỏ rơi") chưa được quyết — v0.4 chỉ pin rằng request không có outcome KHÔNG có hiệu lực gì (§16 Part B), không pin cơ chế phát hiện/dọn dẹp runtime.
- Cơ chế cụ thể generate `activation_request_id` (§16, v0.5) — UUID, idempotency key do requester tự sinh, hay derive từ correlation_id — chưa được quyết; Domain Contract chỉ pin RULE (opaque, stable, không bằng event_id, permanent scope binding), không pin cơ chế sinh giá trị cụ thể, đây là Phase 1/requester-side concern.
- Cơ chế ingress dedup vật lý (nơi physical duplicate event record bị reject trước append hay normalize) — v0.5 chỉ pin RULE tại Domain Contract layer (§16 Part C), không pin cơ chế queue/ingress implementation cụ thể (Phase 1, deferred).
- Cơ chế phát hiện tự động (monitoring/alerting) cho trường hợp "grant VÀ activation event đã ghi nhận, request sau đó phát hiện sai" (§16 Part D Trường hợp 3, v0.6) chưa được quyết — Domain Contract chỉ pin HÀNH ĐỘNG DOWNSTREAM bắt buộc (emit TradableListingFactInvalidated đúng cơ chế hiện có) khi operator/hệ thống phát hiện, không pin cơ chế TỰ ĐỘNG phát hiện hay bắt buộc thời hạn thực hiện — đây là Phase 1/operational concern, không phải Domain Contract semantic.
