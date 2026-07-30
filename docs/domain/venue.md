---
id: venue
title: Venue
version: "0.2"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-07-30"
last_review: null
next_review: null
---

# Venue

> **Vai trò của tài liệu này:** Domain Contract thứ hai của Package 0.2-C1 (Reference Foundation) — định nghĩa **Venue**, identity và metadata tham chiếu của một địa điểm giao dịch/thực thi. Draft, chưa Approved/Locked. Thuộc capability `market-reference` / context `instrument-venue-reference` (đã đăng ký sẵn từ Package 0.2-A tại [`context-map.yaml`](./context-map.yaml), forward-declared → authored, **cùng context với `instrument.md`** — Instrument ↔ Venue là quan hệ intra-context qua TradableListing, không phải cross-context edge). Đúng [ADR-007](../adr/ADR-007.md): kiến trúc **không được giả định crypto-only, không giả định 24/7, không giả định một timezone/session/API adapter/account model/symbol format duy nhất**.

Venue **KHÔNG phải** account credential, KHÔNG phải trading account, KHÔNG phải exchange adapter implementation, KHÔNG phải order execution/fill/position, KHÔNG phải risk hay strategy decision. Nó là **identity và metadata tham chiếu, bitemporal, authoritative** cho một địa điểm giao dịch.

**`venue_id` là identifier đã được MỌI Domain Contract Package 0.2-B tham chiếu trước (cùng `instrument_id`, xem `instrument.md` phần mở đầu) — tài liệu này là nguồn định nghĩa CHÍNH THỨC. KHÔNG đổi tên, KHÔNG đổi shape (`opaque string`).**

Venue bao gồm **bốn concept riêng biệt**:

1. **Logical Venue Subject** (`kind: entity`) — identity ổn định của một địa điểm giao dịch, một subject liên tục theo scope (giống `instrument.md` §1 — không có subject mới per metadata change).
2. **`VenueRegistered`** (`kind: event`) — đăng ký (original hoặc same-scope correction replacement, §11).
3. **`VenueMetadataRevised`** (`kind: event`) — forward-looking metadata change (timezone/calendar/session policy, precision/increment default), dùng PATCH semantics (§9).
4. **`VenueOperationalStatusChanged`** (`kind: event`) — operational status transition.

Cộng **`VenueFactInvalidated`** (correction lineage, có thể target initial fact — §11) và một **read model tùy chọn** (`VenueCurrentView`).

**`venue-registered`/`venue-metadata-revised`/`venue-operational-status-changed`/`venue-fact-invalidated`/`venue-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây. Display name, concept ID, và `event_type` là ba đại lượng khác nhau, không cạnh tranh identity — cùng nguyên tắc mọi Domain Contract trước.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/instrument.md:** envelope binding cho `VenueFactInvalidated`; tách bạch forward-looking revision khỏi correction (đúng `instrument.md` §4/§17); no-row Current View semantics; canonical policy identifier khai báo ĐÚNG MỘT NƠI; opaque identity — không parse `venue_id` (Chapter 6 §6.8).

**v0.2 — ChatGPT Review A narrow correction, đóng `RA-C1-MAJ-01`/`RA-C1-MAJ-02`/`RA-C1-MAJ-03`:** (a) `RA-C1-MAJ-01` — `venue_type`/`jurisdiction_ref` là classification, không phải unique identity; thêm `venue_identity_ref` — discriminator opaque bất biến, bắt buộc, tham gia đầy đủ scope/subject_ref/VenueRegistered/Current View; hai Logical Venue phân biệt PHẢI có `venue_identity_ref` khác nhau dù `venue_type`/`jurisdiction_ref` trùng. (b) `RA-C1-MAJ-02` — `VenueMetadataRevised` v0.1 dùng optional field rời rạc; pin canonical `revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET` (định nghĩa đầy đủ tại `instrument.md` §16, tham chiếu tại đây, không lặp lại). (c) `RA-C1-MAJ-03` — `VenueRegistered` v0.1 không bao giờ correctable; pin `initial_fact_correction_policy: INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES` (định nghĩa đầy đủ tại `instrument.md` §18, áp dụng nguyên văn cho Venue tại đây). Narrow correction — `venue_id` không đổi tên/shape.

## 1. Logical Venue Subject — `kind: entity`

```yaml
id: venue
kind: entity
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Identity ổn định của một địa điểm giao dịch/thực thi — KHÔNG gắn với environment cụ thể
  (production/sandbox), KHÔNG phải API hostname/WebSocket URL, KHÔNG phải account credential.
  Một Logical Venue là MỘT subject liên tục theo scope — không có subject mới per metadata
  change (giống `instrument.md` §1).
invariants:
  - "venue_id resolve deterministic từ TOÀN BỘ scope identity bất biến: venue_identity_ref, venue_type, jurisdiction_ref (khi có) — cùng scope luôn cho cùng venue_id; khác bất kỳ field scope nào (kể cả CHỈ khác venue_identity_ref, dù venue_type/jurisdiction_ref giống hệt) cho venue_id KHÁC (đóng RA-C1-MAJ-01). venue_id bất biến, KHÔNG tái sử dụng cho một subject khác (Chapter 6 §6.1)."
  - "venue_identity_ref là canonical legal/operator/reference identity của Logical Venue — opaque, KHÔNG parse, ổn định xuyên suốt display-name/endpoint/adapter/environment change. Hai Logical Venue phân biệt PHẢI có venue_identity_ref khác nhau, NGAY CẢ KHI venue_type và jurisdiction_ref giống hệt (đóng attack scenario 'two centralized exchanges in the same jurisdiction', 'two brokers in the same jurisdiction', 'same display name for two venues'). KHÔNG dùng URL, hostname, display name, API adapter ID, credential, hay environment name làm venue_identity_ref — trách nhiệm gán giá trị đúng thuộc registration authority bên ngoài (§17, deferred)."
  - "venue_id là opaque — domain logic KHÔNG được parse nó để suy diễn venue_type, API endpoint, hay bất kỳ business meaning nào (Chapter 6 §6.8)."
  - "venue_id KHÔNG được là API hostname/URL, không phải display name (đóng attack scenario 'API URL used as venue_id')."
  - "Toàn bộ scope field (venue_identity_ref, venue_type, jurisdiction_ref) bất biến sau khi subject được đăng ký lần đầu — đổi bất kỳ field nào là tạo một Venue KHÁC (venue_id khác)."
  - "Logical Venue identity KHÔNG được mang production endpoint, sandbox endpoint, API credential, adapter instance, hay deployment environment (§9 — những khái niệm đó thuộc runtime/architecture, Phase 1, không phải Domain Model). Display name đổi (rebrand) hoặc URL/endpoint đổi KHÔNG đổi venue_id (đóng attack scenario 'venue display name changes', 'URL/endpoint changes without Venue identity change')."
schema:
  venue_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  venue_identity_ref: {type: string, required: true, description: "Canonical legal/operator/reference identity của Logical Venue. Opaque, KHÔNG parse. Ổn định xuyên suốt display-name/endpoint/adapter/environment change. Đóng RA-C1-MAJ-01, xem invariants."}
  venue_type: {type: enum, values: [CENTRALIZED_EXCHANGE, DECENTRALIZED_EXCHANGE, BROKER], required: true, description: "đóng ở v0.1, đủ tối thiểu để không hardcode crypto-CEX-only; mở rộng thêm giá trị là thay đổi Domain Contract tường minh; classification, KHÔNG còn một mình gánh global uniqueness (đóng RA-C1-MAJ-01)"}
  jurisdiction_ref: {type: string, required: false, description: "opaque reference, KHÔNG parse — chỉ cho mục đích tham chiếu/compliance tương lai, không mang business logic ở C1"}
state_machine:
  initial_state: UNSEEN
  states: [UNSEEN, REGISTERED, ACTIVE, SUSPENDED, RETIRED]
  transitions:
    - {from: UNSEEN, to: REGISTERED, caused_by: VenueRegistered}
    - {from: REGISTERED, to: ACTIVE, caused_by: VenueOperationalStatusChanged}
    - {from: ACTIVE, to: SUSPENDED, caused_by: VenueOperationalStatusChanged}
    - {from: SUSPENDED, to: ACTIVE, caused_by: VenueOperationalStatusChanged}
    - {from: ACTIVE, to: RETIRED, caused_by: VenueOperationalStatusChanged}
    - {from: SUSPENDED, to: RETIRED, caused_by: VenueOperationalStatusChanged}
    - {from: REGISTERED, to: RETIRED, caused_by: VenueOperationalStatusChanged}
  terminal_states: [RETIRED]
events_emitted: [VenueRegistered, VenueMetadataRevised, VenueOperationalStatusChanged, VenueFactInvalidated]
events_consumed: []
commands: []
queries: []
```

**`UNSEEN` là notional initial state**, cùng convention xuyên suốt. **`RETIRED` là terminal** — cùng nguyên tắc `instrument.md` §1. **Khi một Venue `RETIRED`, mọi TradableListing của nó KHÔNG được ở trạng thái `ACTIVE`** (`instrument.md` §10 cross-subject invariant, đối xứng).

## 2. Canonical event envelope — áp dụng cho mọi Venue event (§3–§6)

Kế thừa nguyên vẹn shape đã khóa tại `instrument.md` §2 (Chapter 8 §8.2) — mục này chỉ khai báo phần khác biệt của Venue.

```yaml
subject_ref:
  context_id: instrument-venue-reference
  subject_kind: entity
  subject_type: Venue
  subject_id: <venue_id — opaque, stable, xem §1>
  scope:
    venue_identity_ref: <string>
    venue_type: <CENTRALIZED_EXCHANGE | DECENTRALIZED_EXCHANGE | BROKER>
    jurisdiction_ref: <string, optional>

event_types:
  VenueRegistered: VENUE_REGISTERED
  VenueMetadataRevised: VENUE_METADATA_REVISED
  VenueOperationalStatusChanged: VENUE_OPERATIONAL_STATUS_CHANGED
  VenueFactInvalidated: VENUE_FACT_INVALIDATED
```

Mọi cardinality khác (`event_id`, `recorded_time`, `causation_refs` — bao gồm quy tắc replacement registration PHẢI chứa `VenueFactInvalidated` đang supersede, `related_event_refs`, `effective_time`, `market_time: PROHIBITED`, `source_identity`, `stream_ref`/`producer_ref`) — áp dụng nguyên văn theo `instrument.md` §2, không định nghĩa lại.

## 3. `VenueRegistered` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: venue-registered
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE cho việc đăng ký một Venue — thiết lập scope identity bất biến
  (venue_identity_ref, venue_type, jurisdiction_ref khi có) VÀ mutable reference metadata ban
  đầu (timezone, default session/calendar policy, default precision policy). Dùng cho CẢ HAI
  trường hợp (v0.2, đóng RA-C1-MAJ-03): (a) original registration, KHÔNG có supersedes_fact_ref;
  (b) same-scope correction replacement sau VenueFactInvalidated target chính registration này,
  CÙNG scope, CÓ supersedes_fact_ref — xem `instrument.md` §18 cho policy đầy đủ, áp dụng nguyên
  văn cho Venue.
invariants:
  - "Tại một thời điểm, đúng MỘT VALID registration lineage head cho mỗi venue_id — KHÔNG phải 'đúng một event record duy nhất mãi mãi' (đóng RA-C1-MAJ-03, xem `instrument.md` §18)."
  - "payload.venue_id PHẢI khớp đúng subject_ref.subject_id VÀ toàn bộ scope field."
  - "supersedes_fact_ref VẮNG MẶT cho original registration; BẮT BUỘC cho same-scope correction replacement — khi có mặt, TOÀN BỘ scope field (venue_identity_ref, venue_type, jurisdiction_ref) PHẢI GIỐNG HỆT fact bị supersede (nếu scope khác, đăng ký venue_id MỚI theo `instrument.md` §18 SCOPE_ERROR path, không dùng supersedes_fact_ref)."
  - "Khi supersedes_fact_ref có mặt: causation_refs PHẢI chứa chính VenueFactInvalidated đang được supersede; envelope.recorded_time PHẢI muộn hơn recorded_time của VenueFactInvalidated đó."
  - "envelope.effective_time = thời điểm registration record này có hiệu lực làm reference data."
payload:
  venue_id: {type: string, required: true}
  venue_identity_ref: {type: string, required: true}
  venue_type: {type: enum, values: [CENTRALIZED_EXCHANGE, DECENTRALIZED_EXCHANGE, BROKER], required: true}
  jurisdiction_ref: {type: string, required: false}
  display_name: {type: string, required: false}
  timezone_ref: {type: string, required: true, description: "opaque reference tới timezone của venue (ví dụ IANA tz identifier hoặc registry reference) — KHÔNG hardcode UTC/24-7 (§8)"}
  default_session_calendar_ref: {type: string, required: true, description: "reference tới trading calendar/session policy mặc định của venue (§8) — TradableListing (instrument.md §11) có thể override per-listing"}
  default_precision_policy_ref: {type: string, required: false, description: "reference tới quy tắc precision/increment mặc định (§9) — TradableListing pin giá trị cụ thể per-listing, đây chỉ là default tham chiếu"}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho original registration; BẮT BUỘC cho same-scope correction replacement — xem invariants và `instrument.md` §18"}
```

## 4. `VenueMetadataRevised` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: venue-metadata-revised
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE cho một thay đổi metadata mô tả MUTABLE của Venue — ví dụ timezone/calendar
  policy đổi (đóng "venue timezone/calendar change"), default precision policy đổi.
  **Forward-looking theo mặc định** — cùng nguyên tắc `instrument.md` §4: fact liền trước vẫn
  hợp lệ cho window lịch sử của nó. Correction dùng VenueFactInvalidated (§6). **v0.2 (đóng
  RA-C1-MAJ-02):** payload dùng canonical PATCH policy `revision_policy:
  EXPLICIT_PATCH_WITH_CLEAR_SET` (định nghĩa đầy đủ tại `instrument.md` §16).
invariants:
  - "envelope.effective_time = thời điểm metadata mới bắt đầu có hiệu lực (forward-looking)."
  - "supersedes_fact_ref VẮNG MẶT cho forward-looking revision bình thường; BẮT BUỘC CHỈ KHI là correction replacement sau VenueFactInvalidated (§6, §11)."
  - "changed_fields và clear_fields PHẢI tuân thủ đầy đủ `revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET` (`instrument.md` §16) — whitelist patchable field: display_name (optional, clearable), timezone_ref (REQUIRED, KHÔNG clearable), default_session_calendar_ref (REQUIRED, KHÔNG clearable), default_precision_policy_ref (optional, clearable). Field scope/identity (venue_id, venue_identity_ref, venue_type, jurisdiction_ref) TUYỆT ĐỐI CẤM xuất hiện trong changed_fields hoặc clear_fields."
payload:
  venue_id: {type: string, required: true}
  changed_fields: {type: map, required: true, description: "field→value PHẢI set — key CHỈ trong whitelist {display_name, timezone_ref, default_session_calendar_ref, default_precision_policy_ref}; map CÓ THỂ rỗng NẾU clear_fields không rỗng"}
  clear_fields: {type: array, items: string, required: true, description: "field CẦN xóa giá trị — key CHỈ trong whitelist các field OPTIONAL {display_name, default_precision_policy_ref}; mảng CÓ THỂ rỗng NẾU changed_fields không rỗng"}
  supersedes_fact_ref: {type: event_record_ref, required: false}
```

## 5. `VenueOperationalStatusChanged` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: venue-operational-status-changed
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Fact AUTHORITATIVE cho một operational status transition của Venue (§1 state_machine) —
  REGISTERED→ACTIVE, ACTIVE↔SUSPENDED, (REGISTERED|ACTIVE|SUSPENDED)→RETIRED. RETIRED là
  terminal. Operational status ở đây là reference-data status (venue có đang được platform coi
  là khả dụng để tham chiếu/list hay không) — KHÔNG phải trạng thái kết nối API runtime
  (Phase 1, §10).
invariants:
  - "new_status PHẢI là transition hợp lệ theo state_machine §1."
  - "new_status = RETIRED KHÔNG được có transition tiếp theo cho cùng venue_id."
payload:
  venue_id: {type: string, required: true}
  new_status: {type: enum, values: [ACTIVE, SUSPENDED, RETIRED], required: true}
  reason: {type: string, required: false}
```

## 6. `VenueFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2 — `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: venue-fact-invalidated
kind: event
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Phủ định MỘT fact lịch sử cụ thể ĐÃ SAI của Venue — cùng nguyên tắc `instrument.md` §6. **v0.2
  (đóng RA-C1-MAJ-03):** VenueRegistered NAY LÀ target hợp lệ — xem `instrument.md` §18 cho
  policy đầy đủ, áp dụng nguyên văn cho Venue.
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref."
  - "invalidated_fact_ref PHẢI trỏ một VenueRegistered, VenueMetadataRevised, hoặc VenueOperationalStatusChanged, CHƯA từng nhận invalidation khác."
  - "initial_fact_correction_class BẮT BUỘC có mặt CHỈ KHI invalidated_fact_ref là VenueRegistered; CẤM có mặt khi invalidated_fact_ref là VenueMetadataRevised/VenueOperationalStatusChanged. Semantic METADATA_ERROR (chờ replacement cùng subject) / SCOPE_ERROR (subject vĩnh viễn không replacement, venue_id mới thay thế) — đúng `instrument.md` §18."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref. Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  initial_fact_correction_class: {type: enum, values: [METADATA_ERROR, SCOPE_ERROR], required: false}
  invalidation_reason: {type: string, required: false}
```

## 7. `VenueCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §3–§6, cùng fold algorithm shape đã pin ở `instrument.md` §7 (registration lineage head trước — quyết định `view_state`, vĩnh viễn `PENDING_CORRECTION` nếu `SCOPE_ERROR`; rồi fold metadata patch theo `metadata_fold_order_policy`; rồi fold status độc lập).

**Canonical decision — no-row trước khi có fact đầu tiên:**

```text
Trước khi VenueRegistered tồn tại cho một venue_id:
  → KHÔNG có VenueCurrentView row nào tồn tại
  → GetCurrentVenue trả về NOT_FOUND / ABSENT
```

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION`.

```yaml
id: venue-current-view
kind: read_model
capability_id: market-reference
domain_context_id: instrument-venue-reference
description: >
  Projection tiện dụng: metadata/status "hiện tại" của một Venue, rebuild được từ §3–§6 theo fold
  algorithm `instrument.md` §7 (áp dụng tương tự). KHÔNG authoritative — mọi input cho Domain
  Contract khác PHẢI dùng authoritative event stream (`ref: venue`), KHÔNG BAO GIỜ dùng view này
  (I-12, Chapter 7 §7.4).
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism) — mọi implementation dùng cùng fold algorithm PHẢI cho cùng kết quả (đóng RA-C1-MAJ-02)."
  - "KHÔNG được dùng làm input cho bất kỳ Domain Contract khác hay Decision — chỉ query/UI."
  - "view_state PHẢI đúng theo fold algorithm `instrument.md` §7 Bước 1 — registration lineage head quyết định; PENDING_CORRECTION vĩnh viễn nếu initial_fact_correction_class = SCOPE_ERROR."
schema:
  venue_id: {type: string, required: true}
  scope: {venue_identity_ref: string, venue_type: string, jurisdiction_ref: string, required: true, description: "chỉ có mặt khi view_state = VALID"}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  current_status: {type: enum, values: [REGISTERED, ACTIVE, SUSPENDED, RETIRED], required: false}
  display_name: {type: string, required: false}
  timezone_ref: {type: string, required: false}
  default_session_calendar_ref: {type: string, required: false}
  default_precision_policy_ref: {type: string, required: false}
  last_recorded_time: timestamp
queries: [GetCurrentVenue, GetVenueHistory]
```

## 8. Trading calendar/session policy — reference concept

Venue sở hữu `default_session_calendar_ref` — reference opaque tới chính sách calendar/session (khi nào venue mở/đóng cửa giao dịch). Đây là **khái niệm tham chiếu**, KHÔNG phải cơ chế resolve cụ thể (bảng lịch, timezone rule engine) — cơ chế đó deferred (§17, Phase 1). Yêu cầu bắt buộc: **KHÔNG hardcode "24/7 liên tục" như một quy tắc phổ quát** (đúng ADR-007) — kể cả khi mọi venue crypto hiện tại đều 24/7, `candle.md` §14 đã tường minh dựa vào chính reference này (`context instrument-venue-reference`) để suy ra window cửa sổ candle. `default_session_calendar_ref` có thể được **override per-listing** qua `TradableListing.session_calendar_ref` (`instrument.md` §11) khi một listing cụ thể cần lịch khác venue mặc định.

## 9. Precision/increment rules — reference concept

Venue sở hữu `default_precision_policy_ref` — reference opaque tới quy tắc precision/increment mặc định (rounding, decimal convention) áp dụng khi một TradableListing không tự pin giá trị riêng. **Giá trị cụ thể (price_increment/quantity_increment/min_quantity/min_notional) LUÔN thuộc TradableListing** (`instrument.md` §11) — đây chỉ là default tham chiếu ở tầng Venue, không phải nơi pin số liệu chính xác cho một cặp Instrument×Venue cụ thể.

## 10. Environment separation — deferred

**KHÔNG được trộn Logical Venue identity với:** production endpoint; sandbox endpoint; API credential; adapter instance; deployment environment. Một Logical Venue (`venue_id`) là identity ổn định, duy nhất — **bất kể** platform kết nối tới nó qua production hay sandbox/testnet, qua adapter nào, hay dùng credential nào (đóng attack scenario "sandbox and production endpoints for one Venue", "credentials placed in Venue"). Những khái niệm đó thuộc **future architecture/runtime concept** (Phase 1 — Engineering/Plugin Model, [Chapter 9](../constitution/09-plugin-model.md)), **không phải Domain Model ở Phase 0.2** — `venue.md` không author chúng, không dự đoán shape của chúng.

## 11. Correction lineage và initial-fact correction policy

Correction lineage scoped chính xác theo `(venue_id, effective_time)` — mỗi effective_time-slice có chuỗi lineage RIÊNG. Mười invariant — **áp dụng nguyên văn theo `instrument.md` §17**, không định nghĩa lại: original fact không supersedes_fact_ref; replacement bắt buộc có; cùng subject/effective_time; supersede đúng lineage head; cấm nhảy cóc; cấm fork; replacement không visible trước invalidation; append-only; Current View loại trừ fact đã invalidate; forward-looking revision KHÔNG BAO GIỜ dùng invalidation.

**`initial_fact_correction_policy: INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES`** (v0.2, đóng `RA-C1-MAJ-03`) — **áp dụng nguyên văn theo `instrument.md` §18**, không định nghĩa lại: same-scope metadata error → invalidate + replacement `VenueRegistered` CÙNG `venue_id`, `supersedes_fact_ref` trỏ về fact bị invalidate, TOÀN BỘ scope giống hệt; scope/identity error → invalidate, KHÔNG replace dưới `venue_id` cũ, đăng ký `venue_id` MỚI với scope đúng, subject cũ Current View `PENDING_CORRECTION` **vĩnh viễn**.

## 12. Time semantics và bitemporal correctness

Áp dụng nguyên văn theo `instrument.md` §19 — `effective_time`/`recorded_time`, không dùng `event_time`, `market_time: PROHIBITED`. **Historical Replay PHẢI dùng đúng metadata (timezone/calendar/precision default) có hiệu lực TẠI computation cursor** — không phải giá trị hiện tại (đóng attack scenario tương tự "current metadata accidentally used for historical replay", áp dụng cho Venue). Correction visibility: `VenueFactInvalidated` và replacement đều có `recorded_time` mới; replay tại cursor trước đó chỉ thấy fact gốc.

## 13. No repaint và mode parity

- `VenueRegistered`/`VenueMetadataRevised`/`VenueOperationalStatusChanged` **KHÔNG BAO GIỜ bị ghi đè tại chỗ** — chỉ phủ định qua `VenueFactInvalidated` + replacement, append-only (I-3).
- Effective-time vs recorded-time tách bạch trung thực — đúng T-vs-T+n discipline xuyên suốt.
- Cùng một chuỗi reference data xuyên Backtest/Replay/Paper/Live — deterministic given authoritative event stream ([I-2](../constitution/02-platform-invariants.md)).

## 14. Input contracts

Venue **không tiêu thụ** bất kỳ authoritative fact nào từ Domain Contract khác — đây là foundational reference data, không có upstream dependency trong Package 0.2 (`events_consumed: []`, §1).

## 15. Venue-neutral requirements

Đúng [ADR-007](../adr/ADR-007.md), Venue **không được** giả định: crypto-only markets; 24/7 trading (§8); một timezone duy nhất; một session per day; một API adapter (§10); một account model (§10, deferred tới Package 0.2-C2); một symbol format (venue symbol thuộc TradableListing, `instrument.md` §11, không thuộc Venue).

## 16. Prohibitions

Venue **KHÔNG được sở hữu:** account credential; trading account; exchange adapter implementation; order execution; fill; position; risk decision; strategy decision.

## 17. Ngoài phạm vi — defer

**Deferred tường minh, không author ở C1:** cơ chế resolve cụ thể `timezone_ref`/`default_session_calendar_ref`/`default_precision_policy_ref`/`venue_identity_ref` (calendar/timezone/reference service, Phase 1); production/sandbox endpoint, adapter instance, credential (Phase 1 Engineering/Plugin Model, §10); `stream_ref`/`producer_ref` (Phase 1); Account/Strategy/Decision/Risk/Order/Fill/Position/Execution (Package 0.2-C2–C7, chưa authorize).

**Out of scope theo ranh giới domain:** account credential, order execution, risk/strategy decision — vi phạm trực tiếp định nghĩa Venue nếu thêm vào (§16).

## 18. Open questions ngoài phạm vi

- `venue_type` enum hiện chỉ có ba giá trị (`CENTRALIZED_EXCHANGE`/`DECENTRALIZED_EXCHANGE`/`BROKER`) — đủ tối thiểu để không hardcode crypto-CEX-only, nhưng chưa rõ liệu DEX cần thêm sub-classification (AMM vs orderbook-based) khi Package tương lai thực sự cần phân biệt. Chưa quyết ở đây — author-level ambiguity, không đóng OQ-002/OQ-003.
- `jurisdiction_ref`/compliance-related metadata hiện chỉ là placeholder opaque reference — chưa có nhu cầu thực tế ở C1, chưa rõ Domain Contract nào sẽ sở hữu compliance logic tương lai.
- `venue_identity_ref` hiện là opaque string, KHÔNG có cơ chế/registry cụ thể nào định nghĩa giá trị hợp lệ hay đảm bảo global uniqueness tự động (trách nhiệm thuộc registration authority ngoài Domain Contract). Cần quyết định khi Package 0.2-C có nhu cầu thực tế đầu tiên.
