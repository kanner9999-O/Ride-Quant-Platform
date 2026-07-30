---
id: account
title: Account
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

# Account

> **Vai trò của tài liệu này:** Domain Contract duy nhất của Package 0.2-C2 (Trading Account Foundation) — định nghĩa **Trading Account**, identity và metadata tham chiếu tối thiểu để package sau (Strategy, Risk, Execution, Order, Fill, Position — Package 0.2-C3–C7, chưa authorize) có thể scope theo một Account. Draft, chưa Approved/Locked. Thuộc capability `account-management` / context `account-reference` (đăng ký MỚI tại [`context-map.yaml`](./context-map.yaml) trong transaction này — Package 0.2-C1's `market-reference`/`instrument-venue-reference` KHÔNG bao trùm Account, đây là capability/context riêng). Kiến trúc controlling: [ADR-012](../adr/ADR-012.md) v0.3 **Approved** — tài liệu này CHỈ implement field/invariant mà ADR-012 yêu cầu, KHÔNG lặp lại toàn văn ADR, KHÔNG tự quyết architecture mới ngoài phạm vi ADR-012 đã khóa.

Account **KHÔNG phải** raw exchange credential, KHÔNG phải Instrument/Venue (tham chiếu `venue.md`, không định nghĩa lại — [ADR-007](../adr/ADR-007.md)), KHÔNG phải Strategy/Decision/Risk/Execution Intent/Order/Fill/Position (Package 0.2-C3–C7, chưa author), KHÔNG phải tenant/organization/IAM identity ([Chapter 6 §6.4](../constitution/06-identity-model.md): "Account ≠ Tenant"), KHÔNG phải billing hay custody implementation. Nó là **identity và metadata tham chiếu tối thiểu, bitemporal, authoritative** cho một trading account — đủ để package sau scope Position/Order/Execution theo đúng một Account, không hơn.

**`account_id` là identifier MỚI, CHƯA từng được Domain Contract nào trước đây tham chiếu** (khác `instrument_id`/`venue_id`/`listing_id` đã tồn tại từ Package 0.2-B/C1) — tài liệu này là nguồn định nghĩa CHÍNH THỨC. Package 0.2-C3–C7 (Strategy, Risk, Execution, Order, Fill, Position) PHẢI dùng đúng tên/shape này (`opaque string`, `ref: account`) khi tham chiếu Account — không tự đặt tên khác (ví dụ KHÔNG dùng `trading_account_id`).

Account bao gồm **ba concept riêng biệt**:

1. **Trading Account Subject** (`kind: entity`) — identity ổn định của một trading account, một subject liên tục theo scope (giống `instrument.md` §1/`venue.md` §1 — không có subject mới per metadata change).
2. **`AccountRegistered`** (`kind: event`) — đăng ký (original hoặc same-scope correction replacement, §11).
3. **`AccountMetadataRevised`** (`kind: event`) — forward-looking metadata change (credential reference, display name), dùng PATCH semantics (§9).

Cộng **`AccountStatusChanged`** (lifecycle transition), **`AccountFactInvalidated`** (correction lineage, có thể target initial fact — §11), và một **read model tùy chọn** (`AccountCurrentView`).

**`account-registered`/`account-metadata-revised`/`account-status-changed`/`account-fact-invalidated`/`account-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây. Display name, concept ID, và `event_type` là ba đại lượng khác nhau, không cạnh tranh identity — cùng nguyên tắc mọi Domain Contract trước.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/0.2-C1** (đóng trước, không lặp lại chu trình 5 vòng correction của C1): envelope binding cho `AccountFactInvalidated` (`subject_ref`/`effective_time` kế thừa từ fact bị invalidate); tách bạch forward-looking revision khỏi correction; no-row Current View semantics trước fact đầu tiên; `view_state` chỉ `VALID`/`PENDING_CORRECTION` với `pending_correction_class` bắt buộc khi `PENDING_CORRECTION` (đóng trước lớp lỗi `IRB-C1-MAJ-01`-style — phân biệt tường minh "chờ same-subject replacement" với "vĩnh viễn invalid do scope error", KHÔNG chờ review round phát hiện); canonical PATCH policy (`changed_fields`/`clear_fields`) cho metadata revision (đóng trước lớp lỗi `RA-C1-MAJ-02`-style); canonical policy identifier khai báo ĐÚNG MỘT NƠI trong file này (context `account-reference` riêng, KHÔNG cross-reference `instrument.md`); opaque identity — không parse `account_id` (Chapter 6 §6.8); Current View KHÔNG BAO GIỜ là authority cho Domain Contract khác (đóng trước lớp lỗi `IRB-C1-V03-MAJ-02`-style — pin ngay từ v0.1).

**Phạm vi bounded tường minh (v0.1):** KHÔNG có multi-party arbitration nào trong Account (khác `instrument.md` §16 `ActiveListingReservation` — đó là bài toán "nhiều TradableListing tranh một pair slot", Account không có bài toán tương tự trong chính nó). KHÔNG onboarding/KYC/broker workflow. KHÔNG billing/multi-tenant IAM. KHÔNG custody/secret-manager implementation. Đây là minimum executable specification, không phải perfect document — dễ revise từ implementation evidence (Phase 1).

**v0.2 — bounded correction, đóng `C2-MAJ-01`/`C2-MAJ-02`/`C2-MAJ-03`/`C2-MAJ-04` (consolidated Review A + Review B findings):** (a) `C2-MAJ-01` — v0.1 SAI khi mô tả `account_id` "resolve deterministic từ scope" (`account_boundary_ref` + `environment`), ngụ ý collapse nhiều Account hợp lệ chung boundary/environment thành một; v0.2 pin `account_id` là opaque, globally unique, gán tại `AccountRegistered`, KHÔNG derive từ scope — một `account_id` có đúng một boundary/environment bất biến, nhưng một cặp boundary/environment CÓ THỂ chứa nhiều `account_id` (§1). (b) `C2-MAJ-02` — làm rõ CLOSED chỉ terminal cho FORWARD transition trên valid lineage; correction (`AccountFactInvalidated` + same-slice `AccountStatusChanged` replacement) vẫn hợp lệ ngay cả khi fact bị sửa là CLOSED — không thêm reopening workflow, chỉ tái khẳng định cơ chế correction lineage đã có (§5, §11); thêm `supersedes_fact_ref` còn thiếu vào payload `AccountStatusChanged`. (c) `C2-MAJ-03` — thay fold algorithm (§7) bằng quy tắc chung "visible-valid-head per slice": group theo correction lineage/effective-time slice, loại fact đã invalidate visible, chọn head hợp lệ per slice, slice invalidate chưa có replacement KHÔNG đóng góp fact nào (không "giữ giá trị cũ"), total-order effective_time/recorded_time/event_id ASC, rồi mới PATCH hoặc lifecycle fold — dùng chung cho AccountMetadataRevised và AccountStatusChanged. (d) `C2-MAJ-04` — pin MỘT quy tắc downstream authority duy nhất: field PHẢI resolve từ authoritative Account stream TẠI cursor, `AccountCurrentView` latest-state KHÔNG BAO GIỜ là input hợp lệ (không cursor-addressable); một cache chỉ được chấp nhận khi VỪA cursor-addressable VỪA provably equivalent tại đúng cursor (§7, §13); `venue_id` xác nhận ABSENT (không chỉ optional) khi `boundary_type: broker_account`. Bounded correction — không đổi exactly-one-boundary/venue-broker distinction/immutable environment/PAPER-LIVE parity/lifecycle value set/credential boundary/PATCH whitelist/METADATA_ERROR-SCOPE_ERROR distinction/same-scope registration correction/C1 semantics/ADR-012.

## 1. Trading Account Subject — `kind: entity`

```yaml
id: account
kind: entity
capability_id: account-management
domain_context_id: account-reference
description: >
  Identity ổn định của một trading account — KHÔNG phải raw exchange credential, KHÔNG phải
  tenant/organization identity (Chapter 6 §6.4: "Account ≠ Tenant"). Một Trading Account là MỘT
  subject liên tục theo scope — không có subject mới per metadata change; rebinding boundary
  (§2, ADR-012 §2.1) tạo một Account KHÁC, không phải mutate subject hiện có.
invariants:
  - "**v0.2 (đóng C2-MAJ-01):** account_id là opaque identifier, globally unique trong toàn Ride, gán tại thời điểm AccountRegistered — KHÔNG derive/resolve/uniquify từ account_boundary_ref hay environment, KHÔNG có công thức tất định nào từ scope. account_id bất biến, KHÔNG tái sử dụng cho một subject khác (Chapter 6 §6.1)."
  - "Một account_id → đúng MỘT account_boundary_ref bất biến VÀ đúng MỘT environment bất biến (một Account luôn có scope cố định, không đổi sau đăng ký) — nhưng chiều ngược lại KHÔNG đúng: một cặp (account_boundary_ref, environment) CÓ THỂ chứa NHIỀU account_id phân biệt (ví dụ nhiều Account PAPER khác nhau cùng trỏ một Venue) — v0.1 sai khi ngụ ý boundary+environment tự nó uniquify account_id, gây collapse nhiều Account hợp lệ thành một; v0.2 sửa triệt để."
  - "account_id là opaque — domain logic KHÔNG được parse nó để suy diễn venue, owner, environment, credential, hay account type (Chapter 6 §6.8, đóng yêu cầu 'Không encode: venue; owner; environment; credential; account type'). Mọi quyết định nghiệp vụ phải dùng field tường minh trong scope, không suy diễn từ cấu trúc ID."
  - "account_boundary_ref BẮT BUỘC, BẤT BIẾN — gán tại thời điểm AccountRegistered, KHÔNG được tái gán sau đó (ADR-012 §2.1). Rebinding (đổi boundary_type hoặc boundary_id) nghĩa là tạo một Account identity MỚI — dùng correction lineage §11 SCOPE_ERROR path, KHÔNG mutate subject hiện có."
  - "account_boundary_ref.boundary_type ∈ {venue, broker_account}, đóng theo ADR-012 §2.1 — không mở rộng giá trị nào khác ở v0.1."
  - "boundary_type = venue: boundary_id PHẢI resolve tới một venue_id đã VenueRegistered (venue.md §3) — Account thuộc trực tiếp đúng một Venue (ADR-012 §2.2). account.md KHÔNG định nghĩa lại Venue semantics — chỉ tham chiếu qua venue_id đã có."
  - "boundary_type = broker_account: boundary_id là opaque reference tới một Broker Account Boundary — khái niệm này CHƯA được author như Domain Contract riêng ở C2 (deferred, §14); Account KHÔNG được giả định transitively resolve về đúng một Venue khi boundary_type = broker_account (ADR-012 §2.3)."
  - "environment BẮT BUỘC, BẤT BIẾN — gán tại thời điểm AccountRegistered, KHÔNG được tái gán sau đó (cùng nguyên tắc bất biến như account_boundary_ref — đổi environment là tạo Account khác, không phải một 'nâng cấp' PAPER→LIVE tại chỗ; promotion workflow deferred, §14)."
  - "PAPER và LIVE Account dùng CHUNG một structural contract — không có nhánh schema/validation riêng cho Account mô phỏng (ADR-012 §2.4, §2.6 mục 8; I-2 Decision Parity)."
  - "credential_reference (nếu có) là opaque reference tới credential binding bên ngoài (Vault/KMS, Phase 1) — TUYỆT ĐỐI KHÔNG chứa raw secret (API key, private key, token, password) dưới bất kỳ hình thức nào, trong payload, snapshot, log, hay replay artifact nào (I-11, §10)."
schema:
  account_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  account_boundary_ref:
    type: object
    required: true
    description: "canonical boundary model, đúng ADR-012 §2.1 — bất biến sau khi đăng ký"
    fields:
      boundary_type: {type: enum, values: [venue, broker_account], required: true}
      boundary_id: {type: string, required: true, description: "opaque immutable reference — resolve tới venue_id (khi boundary_type=venue) hoặc Broker Account Boundary reference (khi boundary_type=broker_account, deferred §14)"}
  environment: {type: enum, values: [PAPER, LIVE], required: true, description: "bất biến — KHÔNG tự authorize Live execution của platform, chỉ phân biệt account environment (xem §8)"}
  credential_reference: {type: string, required: false, description: "opaque reference tới external secure credential binding — KHÔNG BAO GIỜ raw secret (I-11, §10)"}
  display_name: {type: string, required: false, description: "mô tả tiện dụng, KHÔNG phải identity"}
state_machine:
  initial_state: UNSEEN
  states: [UNSEEN, ACTIVE, SUSPENDED, CLOSED]
  transitions:
    - {from: UNSEEN, to: ACTIVE, caused_by: AccountRegistered}
    - {from: ACTIVE, to: SUSPENDED, caused_by: AccountStatusChanged}
    - {from: SUSPENDED, to: ACTIVE, caused_by: AccountStatusChanged}
    - {from: ACTIVE, to: CLOSED, caused_by: AccountStatusChanged}
    - {from: SUSPENDED, to: CLOSED, caused_by: AccountStatusChanged}
  terminal_states: [CLOSED]
events_emitted: [AccountRegistered, AccountMetadataRevised, AccountStatusChanged, AccountFactInvalidated]
events_consumed: []
commands: []
queries: []
```

**`UNSEEN` là notional initial state** — cùng convention xuyên suốt tài liệu: không event nào khẳng định "subject đang UNSEEN". **`CLOSED` là terminal** — một Account đã closed không quay lại `ACTIVE`/`SUSPENDED` (nếu cần giao dịch lại, đăng ký một `account_id` mới — closing không phải "tạm khóa", nó là kết thúc vòng đời logic, cùng nguyên tắc `RETIRED` của Instrument/Venue).

**Enum lifecycle tối thiểu, ba giá trị thực sự cần** (`ACTIVE`/`SUSPENDED`/`CLOSED`) — không thêm state onboarding/KYC/pending-approval; nếu implementation cần một quy trình phê duyệt trước khi Account sẵn sàng, đó là workflow BÊN NGOÀI Domain Contract (Phase 1 operational concern, §14) — `AccountRegistered` chỉ được emit khi Account đã sẵn sàng dùng, đưa thẳng vào `ACTIVE` (cùng shape `TradableListingCreated`, `instrument.md` §11).

## 2. Canonical event envelope — áp dụng cho mọi Account event (§3–§6)

Mọi event trong tài liệu này là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). Mục này khóa **envelope chung** một lần.

```yaml
envelope:
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2)
  event_contract_ref: {cardinality: required}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}             # khi Ride ghi nhận fact này
  subject_ref: {cardinality: "required — shape canonical, xem dưới. Trên AccountFactInvalidated (§6), PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate."}
  stream_ref: {cardinality: required}                # Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # Phase 1, chưa author
  correlation_id: {cardinality: "required khi computation thuộc một correlation flow tường minh; optional khi độc lập"}
  causation_refs: {cardinality: "AccountRegistered ORIGINAL (không supersedes_fact_ref): zero-or-more (fact gốc, không nhất thiết có causal ancestor authoritative — đăng ký thủ công qua operator workflow, Phase 1). AccountRegistered REPLACEMENT (có supersedes_fact_ref, §11): KHÔNG BAO GIỜ rỗng, PHẢI chứa chính AccountFactInvalidated đang được supersede. Mọi event khác (revision/status-change/invalidation): KHÔNG BAO GIỜ rỗng."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3. Một AccountRegistered cho SUBJECT MỚI (sau một SCOPE_ERROR correction, §11) CÓ THỂ tham chiếu non-causal tới AccountFactInvalidated của subject cũ để truy vết, nhưng KHÔNG bắt buộc và KHÔNG phải causal ancestor."}
  effective_time: {cardinality: "required — semantic khác theo event type, xem §3–§6 cho nội dung cụ thể."}
  market_time: {cardinality: "PROHIBITED — Account là reference data authoritative, không phải quan sát trực tiếp venue theo nghĩa market_time (Chapter 5 §5.2)."}
  source_identity: {cardinality: "optional — có mặt khi fact đến từ external onboarding feed có khả năng retry/redelivery (Chapter 6 §6.6); PROHIBITED khi đăng ký thủ công qua Product Owner/operator workflow (Phase 1, chưa author)."}

subject_ref (Trading Account):
  context_id: account-reference
  subject_kind: entity
  subject_type: Account
  subject_id: <account_id — opaque, stable, xem §1>
  scope:
    account_boundary_ref: {boundary_type: <venue | broker_account>, boundary_id: <string>}
    environment: <PAPER | LIVE>

event_types:
  AccountRegistered: ACCOUNT_REGISTERED
  AccountMetadataRevised: ACCOUNT_METADATA_REVISED
  AccountStatusChanged: ACCOUNT_STATUS_CHANGED
  AccountFactInvalidated: ACCOUNT_FACT_INVALIDATED
```

`stream_ref`/`producer_ref` — Phase 1, chưa tồn tại, cùng nguyên tắc defer xuyên suốt Package 0.2-B/C1.

## 3. `AccountRegistered` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: account-registered
kind: event
capability_id: account-management
domain_context_id: account-reference
description: >
  Fact AUTHORITATIVE cho việc đăng ký một Trading Account — thiết lập scope identity bất biến
  (account_boundary_ref, environment) VÀ mutable metadata ban đầu (credential_reference,
  display_name). Dùng cho CẢ HAI trường hợp: (a) original registration — lần đăng ký đầu tiên
  cho account_id đó, KHÔNG có supersedes_fact_ref; (b) same-scope correction replacement — sau
  một AccountFactInvalidated target chính registration này vì mutable metadata (ví dụ
  credential_reference) ghi sai, CÙNG scope identity, CÓ supersedes_fact_ref (§11). KHÔNG dùng
  cho forward-looking metadata change (đó là AccountMetadataRevised, §4).
invariants:
  - "Tại một thời điểm, đúng MỘT VALID registration lineage head cho mỗi account_id — KHÔNG phải 'đúng một event record duy nhất mãi mãi' (§11 cho correction policy đầy đủ). Lineage head là fact chưa bị invalidate, hoặc là replacement mới nhất chưa bị invalidate."
  - "payload.account_id PHẢI khớp đúng subject_ref.subject_id VÀ toàn bộ scope field PHẢI khớp subject_ref.scope."
  - "boundary_type = venue: causation_refs PHẢI trỏ VenueRegistered (venue.md §3) của venue_id tương ứng — chứng minh Venue đã tồn tại trước khi Account đăng ký dưới boundary đó."
  - "supersedes_fact_ref VẮNG MẶT cho original registration; BẮT BUỘC cho same-scope correction replacement — khi có mặt, TOÀN BỘ scope field (account_boundary_ref, environment) PHẢI GIỐNG HỆT fact bị supersede (nếu scope khác, đây KHÔNG phải correction hợp lệ — phải đăng ký subject MỚI theo §11 SCOPE_ERROR path, không dùng supersedes_fact_ref)."
  - "Khi supersedes_fact_ref có mặt: causation_refs PHẢI chứa chính AccountFactInvalidated đang được supersede; envelope.recorded_time PHẢI muộn hơn recorded_time của AccountFactInvalidated đó (replacement không visible trước invalidation)."
  - "envelope.effective_time = thời điểm registration record này có hiệu lực làm reference data — mặc định bằng recorded_time trừ khi backfill lịch sử tường minh pin effective_time sớm hơn (§12)."
payload:
  account_id: {type: string, required: true}
  account_boundary_ref:
    boundary_type: {type: enum, values: [venue, broker_account], required: true}
    boundary_id: {type: string, required: true}
  environment: {type: enum, values: [PAPER, LIVE], required: true}
  credential_reference: {type: string, required: false, description: "opaque, KHÔNG raw secret — xem §10"}
  display_name: {type: string, required: false}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho original registration; BẮT BUỘC cho same-scope correction replacement — xem invariants và §11"}
```

## 4. `AccountMetadataRevised` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: account-metadata-revised
kind: event
capability_id: account-management
domain_context_id: account-reference
description: >
  Fact AUTHORITATIVE cho một thay đổi metadata mô tả MUTABLE (KHÔNG phải scope identity — đổi
  account_boundary_ref hoặc environment là tạo account_id khác, §1). **Forward-looking theo mặc
  định:** một revision mới có effective_time MỚI, fact liền trước vẫn hợp lệ nguyên vẹn cho
  window lịch sử của nó — KHÔNG phải correction. Correction (sửa một fact ĐÃ SAI trong quá khứ)
  dùng AccountFactInvalidated + replacement (§6) — hai khái niệm tách bạch tường minh, không gộp.
  Payload dùng canonical PATCH policy `revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET` (§9) —
  `changed_fields`/`clear_fields` tường minh, cùng pattern đã proven tại `instrument.md`/
  `venue.md`, khai báo độc lập trong context `account-reference` này (không cross-reference).
invariants:
  - "envelope.effective_time = thời điểm metadata này bắt đầu có hiệu lực (forward-looking) — KHÁC recorded_time khi biết trước/backfill."
  - "supersedes_fact_ref VẮNG MẶT cho forward-looking revision bình thường (fact liền trước KHÔNG bị phủ định, chỉ 'hết hiệu lực về sau' theo effective_time thứ tự)."
  - "supersedes_fact_ref BẮT BUỘC có mặt CHỈ KHI đây là correction replacement sau một AccountFactInvalidated (§6) — dùng đúng cùng nguyên tắc correction lineage §11."
  - "envelope.recorded_time PHẢI muộn hơn hoặc bằng recorded_time của AccountRegistered/revision liền trước cho cùng subject."
  - "changed_fields và clear_fields PHẢI tuân thủ đầy đủ `revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET` (§9) — whitelist patchable field CHỈ gồm: credential_reference (optional, clearable — ví dụ khi credential rotation binding đổi, Phase 1 mechanism cụ thể deferred §14), display_name (optional, clearable). Field scope/identity (account_id, account_boundary_ref, environment) TUYỆT ĐỐI CẤM xuất hiện trong changed_fields hoặc clear_fields."
payload:
  account_id: {type: string, required: true}
  changed_fields: {type: map, required: true, description: "field→value PHẢI set — key CHỈ trong whitelist {credential_reference, display_name}; map CÓ THỂ rỗng NẾU clear_fields không rỗng — xem §9 'ít nhất một effective change'"}
  clear_fields: {type: array, items: string, required: true, description: "field CẦN xóa giá trị (đưa về absent) — key CHỈ trong whitelist {credential_reference, display_name}; mảng CÓ THỂ rỗng NẾU changed_fields không rỗng"}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho forward revision bình thường; BẮT BUỘC cho correction replacement — xem invariants và §11"}
```

## 5. `AccountStatusChanged` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: account-status-changed
kind: event
capability_id: account-management
domain_context_id: account-reference
description: >
  Fact AUTHORITATIVE cho một operational status transition của Trading Account (§1
  state_machine) — ACTIVE↔SUSPENDED, (ACTIVE|SUSPENDED)→CLOSED. **v0.2 (đóng C2-MAJ-02):**
  CLOSED là terminal CHO FORWARD TRANSITION trên valid lineage hiện hành — không có
  `AccountStatusChanged` forward nào (ACTIVE/SUSPENDED/CLOSED) được phép sau một CLOSED fact
  VALID. Điều này KHÔNG ngăn correction: một CLOSED fact ghi SAI (ví dụ đóng nhầm account) vẫn
  correctable append-only qua `AccountFactInvalidated` + same-slice replacement (§11) — đây là
  correction record, KHÔNG PHẢI forward lifecycle transition, nên KHÔNG vi phạm terminality.
  KHÔNG có reopening workflow nào được thêm — chỉ đúng cơ chế correction lineage đã có sẵn cho
  mọi event type khác trong tài liệu này.
invariants:
  - "new_status PHẢI là một transition hợp lệ theo state_machine §1 từ current_status hiện tại — current_status resolve theo fold algorithm §7 (visible-valid-head per effective-time slice, total-order effective_time ASC/recorded_time ASC/event_id ASC), KHÔNG dùng raw recorded_time đơn thuần, KHÔNG dùng sequence xuyên stream, KHÔNG dùng một CLOSED fact đã bị invalidate mà chưa có replacement visible."
  - "new_status = CLOSED trên valid lineage hiện hành KHÔNG được có `AccountStatusChanged` forward transition tiếp theo cho cùng account_id (§1 terminal_states) — đây là ràng buộc FORWARD LIFECYCLE, không áp dụng cho correction record."
  - "**v0.2 (đóng C2-MAJ-02):** Một CLOSED fact (hoặc bất kỳ `AccountStatusChanged` nào khác) ghi SAI vẫn correctable qua `AccountFactInvalidated` + same-slice `AccountStatusChanged` replacement (§11, cùng `(account_id, effective_time)` slice, `supersedes_fact_ref` trỏ đúng fact bị invalidate) — correction KHÔNG bị chặn bởi CLOSED terminality, vì correction không phải một forward transition mới; fold algorithm (§7) PHẢI recompute current_status từ valid corrected lineage sau khi replacement visible. KHÔNG thêm state/enum mới, KHÔNG thêm reopening command — cơ chế correction đã có sẵn (§11) áp dụng nguyên vẹn cho AccountStatusChanged, kể cả khi giá trị bị invalidate là CLOSED."
  - "envelope.effective_time = thời điểm status transition này thực sự có hiệu lực (có thể khác recorded_time nếu biết trước lịch đóng account)."
  - "Account CHỈ hợp lệ cho action mới (ví dụ Order/Execution mới ở Package 0.2-C3+) khi current_status = ACTIVE tại effective_time liên quan — SUSPENDED/CLOSED CẤM action mới; đây là RÀNG BUỘC lên Domain Contract tương lai (Order/Execution, chưa author), account.md chỉ PIN quy tắc, không tự enforce vì chưa có consumer nào tồn tại (§13)."
  - "**v0.2:** supersedes_fact_ref VẮNG MẶT cho forward transition bình thường; BẮT BUỘC cho same-slice correction replacement — khi có mặt, PHẢI trỏ đúng `AccountStatusChanged` (kể cả CLOSED) bị `AccountFactInvalidated` target, cùng subject/effective_time (§11)."
payload:
  account_id: {type: string, required: true}
  new_status: {type: enum, values: [ACTIVE, SUSPENDED, CLOSED], required: true}
  reason: {type: string, required: false}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho forward transition bình thường; BẮT BUỘC cho same-slice correction replacement (v0.2, đóng C2-MAJ-02) — xem invariants và §11"}
```

## 6. `AccountFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2 — `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: account-fact-invalidated
kind: event
capability_id: account-management
domain_context_id: account-reference
description: >
  Phủ định MỘT fact lịch sử cụ thể ĐÃ SAI của Trading Account — thuần túy ghi nhận "fact này
  không còn hợp lệ", KHÔNG tự nó tuyên bố giá trị mới. **KHÔNG dùng cho forward-looking change**
  (đó là AccountMetadataRevised/AccountStatusChanged bình thường, không phải invalidation).
  AccountRegistered LÀ target hợp lệ — đóng ngay từ v0.1 (đóng trước lớp lỗi
  `RA-C1-MAJ-03`-style, không chờ review round phát hiện). Xem §11 cho policy đầy đủ phân biệt
  METADATA_ERROR (chờ replacement cùng subject) vs SCOPE_ERROR (subject này KHÔNG BAO GIỜ có
  replacement, đăng ký subject mới thay thế — đúng ADR-012 §2.1 "rebinding = tạo Account khác").
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref (F) — cùng context_id, subject_kind, subject_type, subject_id, VÀ toàn bộ scope."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref (F)."
  - "payload.invalidated_fact_ref PHẢI trỏ một AccountRegistered, AccountMetadataRevised, hoặc AccountStatusChanged — KHÔNG BAO GIỜ một AccountFactInvalidated khác (cấm invalidation-of-invalidation)."
  - "invalidated_fact_ref PHẢI trỏ một fact CHƯA từng nhận AccountFactInvalidated khác — một fact chỉ bị invalidate đúng một lần."
  - "account_fact_correction_class BẮT BUỘC có mặt CHỈ KHI invalidated_fact_ref là AccountRegistered; CẤM có mặt khi invalidated_fact_ref là AccountMetadataRevised/AccountStatusChanged."
  - "account_fact_correction_class = METADATA_ERROR: mong đợi (không bắt buộc ngay lập tức) một AccountRegistered replacement CÙNG account_id, supersedes_fact_ref = event này (§11)."
  - "account_fact_correction_class = SCOPE_ERROR: CẤM mọi AccountRegistered replacement dưới CÙNG account_id — subject này vĩnh viễn không có lineage head VALID nào khác; correction thực tế nằm ở việc đăng ký một account_id MỚI hoàn toàn độc lập (§11, ADR-012 §2.1 rebinding rule)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  account_fact_correction_class: {type: enum, values: [METADATA_ERROR, SCOPE_ERROR], required: false, description: "chỉ có mặt khi invalidated_fact_ref là AccountRegistered — xem invariants và §11"}
  invalidation_reason: {type: string, required: false}
```

## 7. `AccountCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §3–§6.

**Canonical decision — no-row trước khi có fact đầu tiên (đúng convention xuyên suốt Package 0.2):**

```text
Trước khi AccountRegistered tồn tại cho một account_id:
  → KHÔNG có AccountCurrentView row nào tồn tại
  → GetCurrentAccount trả về NOT_FOUND / ABSENT
```

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION`. Khi `PENDING_CORRECTION`, `pending_correction_class` BẮT BUỘC có mặt (đóng ngay từ v0.1 — pattern đã proven tại `instrument.md`/`venue.md`, tránh lặp lại chu trình phát hiện-rồi-sửa của C1):

```text
view_state = VALID              → pending_correction_class: CẤM (phải absent)
view_state = PENDING_CORRECTION → pending_correction_class: BẮT BUỘC

account_fact_correction_class = METADATA_ERROR → pending_correction_class = AWAITING_SAME_SUBJECT_REPLACEMENT
account_fact_correction_class = SCOPE_ERROR    → pending_correction_class = TERMINAL_SCOPE_INVALIDATION
```

`TERMINAL_SCOPE_INVALIDATION` KHÔNG BAO GIỜ transition về `VALID`; subject cũ vẫn queryable qua `GetAccountHistory` làm historical evidence; consumer/retry worker KHÔNG được coi đây là "chờ và thử lại sau" (đúng nguyên tắc đã khóa tại `instrument.md` §19, áp dụng độc lập tại đây cho context `account-reference`).

**Fold algorithm (v0.2, đóng C2-MAJ-02/C2-MAJ-03 — visible-valid-head per slice, MỘT quy tắc chung dùng cho cả ba họ fact, không cần 5-phase như Instrument/TradableListing vì Account không có multi-party arbitration):**

**Quy tắc chung — visible-valid-head per slice** (áp dụng CHO CẢ BA họ fact — `AccountRegistered`, `AccountMetadataRevised`, `AccountStatusChanged` — tại một recorded-time cursor cho trước; mỗi `(account_id, effective_time)` là một slice riêng theo §11):

```text
1. Group mọi fact của họ event đó theo correction lineage/effective-time slice — trong một
   slice, fact gốc + mọi replacement liên tiếp (chuỗi supersedes_fact_ref) là MỘT lineage.
2. Với mỗi slice, resolve AccountFactInvalidated visibility tại cursor (recorded_time <=
   cursor).
3. Loại trừ khỏi lineage bất kỳ fact nào đã có AccountFactInvalidated visible tại cursor — fact
   đó KHÔNG BAO GIỜ được coi là head, dù trước đây từng là head.
4. Chọn head hợp lệ (visible valid head) của slice: fact CHƯA bị invalidate visible, hoặc
   replacement mới nhất (theo chuỗi supersedes_fact_ref) CHƯA bị invalidate visible — VÀ chính
   head đó PHẢI visible tại cursor (recorded_time <= cursor).
5. NẾU slice đó bị invalidate visible VÀ replacement CHƯA visible tại cursor → slice này KHÔNG
   ĐÓNG GÓP fact nào cho fold (không "giữ giá trị cũ", không "coi như rỗng dùng default" — đơn
   giản bị loại khỏi tập input của bước 6–7). Riêng slice registration: toàn `AccountCurrentView`
   chuyển `PENDING_CORRECTION` (Bước 1 dưới). Riêng một slice metadata/status không phải slice
   mới nhất: CHỈ đóng góp của slice đó bị bỏ, KHÔNG ảnh hưởng slice khác (đóng yêu cầu "invalidated
   PATCH must contribute no residual fields", "invalidated status fact must not affect current
   status").
6. Tổng hợp mọi visible-valid-head còn lại (sau bước 3–5) xuyên các slice, total-order:
   (a) `effective_time` ASC, (b) `recorded_time` ASC, (c) `event_id` ASC — KHÔNG dùng raw
   sequence xuyên stream.
7. Áp dụng PATCH (`AccountMetadataRevised`) hoặc lifecycle fold (`AccountStatusChanged`) trên
   tập head đã sắp, theo đúng thứ tự Bước 6.
```

```text
Bước 1 — REGISTRATION: áp dụng Quy tắc chung cho họ AccountRegistered. NẾU slice registration
  hiện hành KHÔNG có visible-valid-head (bước 5 của quy tắc chung áp dụng cho chính registration)
  → view_state = PENDING_CORRECTION, pending_correction_class theo mapping trên, KHÔNG resolve
  field nào khác — DỪNG tại đây. NẾU CÓ → scope field (account_boundary_ref, environment) = từ
  head đó, tiếp tục Bước 2.

Bước 2 — METADATA: áp dụng Quy tắc chung cho họ AccountMetadataRevised. Một slice bị invalidate
  chưa có replacement visible ĐÓNG GÓP KHÔNG GÌ — KHÔNG residual field nào từ patch của nó lọt
  vào kết quả; fold tiếp tục với head hợp lệ của các slice khác theo thứ tự Bước 6. Áp dụng
  `changed_fields`/`clear_fields` của mọi visible-valid-head còn lại, tuần tự theo thứ tự Bước 6
  → `credential_reference`/`display_name` hiện tại.

Bước 3 — STATUS: áp dụng Quy tắc chung cho họ AccountStatusChanged. Một `AccountStatusChanged`
  bị invalidate (kể cả mang `new_status: CLOSED`, §5/§11, đóng C2-MAJ-02) mà chưa có replacement
  visible KHÔNG ảnh hưởng `current_status` — slice đó bị loại (bước 5), fold dùng head hợp lệ của
  slice effective_time gần nhất trước đó. Sau khi replacement (nếu có) visible, `current_status`
  recompute từ lineage đã sửa — CÓ THỂ khác giá trị CLOSED cũ nếu correction đổi kết luận (đóng
  yêu cầu "fold must recompute lifecycle state from the valid corrected lineage").
```

```yaml
id: account-current-view
kind: read_model
capability_id: account-management
domain_context_id: account-reference
description: >
  Projection tiện dụng: metadata/status "hiện tại" (latest-state, KHÔNG cursor-addressable theo
  mặc định) của một Trading Account, rebuild được từ §3–§6 theo fold algorithm ở trên. KHÔNG
  authoritative — **v0.2 (đóng C2-MAJ-04):** `GetCurrentAccount`/`GetAccountHistory` (schema
  dưới) CHỈ dùng cho query/UI, KHÔNG BAO GIỜ là input hợp lệ cho Domain Contract khác
  (Strategy/Risk/Execution, Package 0.2-C3+) hay Decision dưới BẤT KỲ hình thức nào — kể cả khi
  "trông giống" cùng giá trị. Downstream field PHẢI resolve qua authoritative Account event
  stream (`ref: account`) TẠI CÙNG recorded/effective cursor mà computation đó đang dùng (§13).
  Một implementation CHỈ được dùng một MATERIALIZED PROJECTION làm input tính toán khi projection
  đó đồng thời: (a) **cursor-addressable** — hỗ trợ query "as-of cursor X" cụ thể, KHÔNG PHẢI
  chỉ một row latest-state duy nhất; VÀ (b) **provably equivalent** với authoritative
  reconstruction tại ĐÚNG cursor, contract version, và configuration đó. `AccountCurrentView`
  như định nghĩa dưới đây (`GetCurrentAccount`) KHÔNG thỏa điều kiện (a) — nó là latest-state
  duy nhất, không tham số hóa theo cursor — nên KHÔNG BAO GIỜ được downstream dùng làm input,
  kể cả như cache (I-12, Chapter 7 §7.4).
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism) — mọi implementation dùng cùng fold algorithm PHẢI cho cùng kết quả."
  - "**v0.2 (đóng C2-MAJ-04):** KHÔNG được dùng làm input cho bất kỳ Domain Contract khác, Decision, hay computation nào — CHỈ query/UI, không có ngoại lệ cho artifact CỤ THỂ này (latest-state, không cursor-addressable). Một cursor-addressable materialization RIÊNG (khác `GetCurrentAccount`, hỗ trợ resolve tại cursor tùy ý) CÓ THỂ dùng làm cache tính toán CHỈ KHI provably equivalent với authoritative reconstruction tại đúng cursor/contract version/configuration đang dùng — xem §13."
  - "view_state PHẢI đúng theo Bước 1 của fold algorithm — registration lineage head quyết định, KHÔNG BAO GIỜ fallback về một registration đã invalidate."
  - "pending_correction_class BẮT BUỘC có mặt khi view_state = PENDING_CORRECTION; CẤM có mặt khi view_state = VALID."
  - "current_status PHẢI recompute đúng theo Bước 3 (visible-valid-head per slice) — một CLOSED fact đã invalidate mà chưa có replacement visible KHÔNG được góp phần vào current_status (đóng C2-MAJ-02/C2-MAJ-03)."
schema:
  account_id: {type: string, required: true}
  scope: {account_boundary_ref: object, environment: string, required: true, description: "chỉ có mặt khi view_state = VALID (Bước 1 fold)"}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  pending_correction_class: {type: enum, values: [AWAITING_SAME_SUBJECT_REPLACEMENT, TERMINAL_SCOPE_INVALIDATION], required: false}
  current_status: {type: enum, values: [ACTIVE, SUSPENDED, CLOSED], required: false, description: "chỉ có mặt khi view_state = VALID"}
  credential_reference: {type: string, required: false}
  display_name: {type: string, required: false}
  last_recorded_time: timestamp
queries: [GetCurrentAccount, GetAccountHistory]
```

## 8. Environment — closed enum

```text
PAPER  — simulated/paper trading account
LIVE   — live trading account
```

**Đóng ở v0.1** — chỉ hai giá trị. `LIVE` **CHỈ LÀ domain value để phân biệt account environment** — nó **KHÔNG authorize Live execution của platform**. Live execution authorization là quyết định governance riêng, tách bạch hoàn toàn khỏi việc một Account record mang `environment: LIVE` (đúng thần chú xuyên suốt mọi transaction Package 0.2-C1: authoring/registering một domain value không bao giờ tự động cấp quyền vận hành). PAPER và LIVE Account dùng **chung một structural contract** (§1 invariant, ADR-012 §2.4, I-2 Decision Parity) — không có nhánh schema riêng.

## 9. Canonical policy identifiers — nguồn duy nhất (context `account-reference`)

**Hai canonical policy identifier, khai báo ĐÚNG MỘT LẦN tại đây cho context `account-reference`** — cùng pattern đã proven tại `instrument.md`/`venue.md` (context `instrument-venue-reference`), khai báo ĐỘC LẬP vì đây là context khác, tránh cross-context coupling không cần thiết:

```yaml
revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET
initial_fact_correction_policy: INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES
```

**`revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET`** — áp dụng cho `AccountMetadataRevised` (§4). Quy tắc bắt buộc:

```text
changed_fields   — required field trong payload (map), key CHỈ trong whitelist {credential_reference, display_name}
clear_fields     — required field trong payload (array), key CHỈ trong whitelist {credential_reference, display_name}

absent field (không trong changed_fields lẫn clear_fields)  → UNCHANGED (giữ nguyên giá trị trước)
field trong changed_fields                                   → SET về giá trị supplied
field trong clear_fields                                     → CLEAR (đưa về absent/removed)

changed_fields keys ∩ clear_fields  →  PHẢI RỖNG (cấm vừa set vừa clear cùng field trong một patch)
unknown field hoặc scope/identity field (account_id, account_boundary_ref, environment)  →  CẤM tuyệt đối trong cả changed_fields lẫn clear_fields
ít nhất một effective change         →  BẮT BUỘC — changed_fields và clear_fields KHÔNG được cùng rỗng (đóng attack scenario "empty patch")
```

**`initial_fact_correction_policy: INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES`** — xem §11 cho định nghĩa đầy đủ.

## 10. Credential và secret boundary (I-11)

**Domain Contract này TUYỆT ĐỐI KHÔNG chứa raw secret** — API key, private key, token, password, exchange credential dưới bất kỳ hình thức nào — trong payload, `AccountCurrentView` snapshot, log, hay replay artifact nào. Account **chỉ giữ `credential_reference`** — một opaque reference tới credential binding thực sự, sống BÊN NGOÀI Domain Contract (Vault/KMS hoặc Custody/Signing Service tương đương, Phase 1 — [I-11](../constitution/02-platform-invariants.md)).

**Chỉ Exchange Adapter hoặc dedicated Custody/Signing Service được phép sử dụng credential trực tiếp** (I-11) — Strategy/Decision/Risk/Execution Engine (Package 0.2-C3+, chưa author) **không được** cấp quyền đọc raw secret; chúng chỉ tương tác qua `credential_reference` opaque, giống cách `instrument_id`/`venue_id` opaque không mang business meaning parse được (Chapter 6 §6.8).

**Credential reference resolve trong đúng boundary đã chọn** (ADR-012 §2.4): với `boundary_type: venue`, `credential_reference` scoped cho 1 venue; với `boundary_type: broker_account`, scoped đúng broker relationship đó — account.md KHÔNG định nghĩa cơ chế resolve cụ thể (Phase 1 Security & Custody Baseline, deferred §14, đúng ADR-012 §6 "Thuộc Domain Contract, KHÔNG thuộc ADR này: cơ chế credential reference cụ thể").

**Rotation/rebind credential:** thay đổi giá trị `credential_reference` (ví dụ rotate key) dùng `AccountMetadataRevised` (§4, forward-looking, field `credential_reference` clearable) — KHÔNG phải correction, KHÔNG tạo Account mới, vì bản thân credential_reference KHÔNG thuộc scope bất biến (§1). Cơ chế vận hành thực tế của việc rotate (khi nào, ai kích hoạt, đồng bộ với Vault/KMS) là Phase 1 operational concern, deferred (§14).

## 11. Correction lineage (`AccountRegistered`, đúng ADR-012 §2.1)

Correction lineage scoped chính xác theo `(account_id, effective_time)` — mỗi effective_time-slice có chuỗi lineage RIÊNG, cùng nguyên tắc đã khóa xuyên suốt `instrument.md`/`venue.md`.

```text
AccountRegistered/AccountMetadataRevised/AccountStatusChanged F1
  → AccountFactInvalidated targeting F1
  → replacement (cùng event type), supersedes_fact_ref = F1

Correction tiếp theo:
F2
  → AccountFactInvalidated targeting F2
  → F3, supersedes_fact_ref = F2   (KHÔNG được supersedes_fact_ref = F1 — cấm nhảy cóc)
```

**Mười invariant bắt buộc** (đã pin tại §3–§6, tổng hợp lại đây):

1. Original fact (`AccountRegistered` KHÔNG có supersedes_fact_ref) không có `supersedes_fact_ref`.
2. Replacement fact (correction, kể cả replacement registration) bắt buộc có `supersedes_fact_ref`; forward-looking revision bình thường thì không.
3. Replacement dùng đúng cùng subject và cùng `effective_time` với fact bị supersede.
4. Replacement PHẢI supersede đúng lineage head hiện tại.
5. Replacement không được nhảy cóc qua một head trung gian.
6. Một fact bị invalidate có **tối đa một** replacement authoritative trực tiếp — cấm fork.
7. Replacement không được "visible" (`recorded_time`) trước invalidation tương ứng.
8. Mọi lineage member lịch sử giữ nguyên trong log — append-only (I-3), không mutate.
9. Một fact đã invalidate **không bao giờ** bị tái sử dụng ngầm — Current View (§7) phải loại trừ nó tường minh.
10. **Forward-looking revision KHÔNG BAO GIỜ dùng cơ chế invalidation** — chỉ correction (sửa sai sót thực sự trong quá khứ) mới dùng `AccountFactInvalidated` + replacement.

**`AccountStatusChanged` correction, kể cả CLOSED (v0.2, đóng C2-MAJ-02):** mười invariant trên áp dụng NGUYÊN VẸN cho `AccountStatusChanged` — bao gồm khi fact bị invalidate mang `new_status: CLOSED`. Terminal state (§1/§5) chỉ chặn FORWARD transition trên valid lineage (`caused_by: AccountStatusChanged` mới với `supersedes_fact_ref` vắng mặt) — nó KHÔNG chặn correction record (`supersedes_fact_ref` có mặt, cùng `(account_id, effective_time)` slice, đúng invariant 1–10). Sau khi replacement visible, fold algorithm (§7) recompute `current_status` từ lineage head hợp lệ mới — có thể KHÁC CLOSED nếu correction đó là "CLOSED ghi sai, đúng ra vẫn ACTIVE/SUSPENDED". KHÔNG có command "reopen" nào được thêm — đây thuần túy là sửa một fact lịch sử sai, không phải một hành động nghiệp vụ mới.

**`initial_fact_correction_policy: INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES`** (§9) — phân biệt hai trường hợp, đúng ADR-012 §2.1:

### Same-scope metadata error

Khi registration gốc có **scope identity ĐÚNG** (`account_boundary_ref`, `environment` đúng) nhưng **mutable metadata SAI** (ví dụ `credential_reference` ghi sai lúc đăng ký):

```text
invalidate initial fact (AccountFactInvalidated, account_fact_correction_class = METADATA_ERROR)
→ emit replacement registration fact CHO CÙNG subject
  (account_id không đổi, TOÀN BỘ scope field giống hệt,
  supersedes_fact_ref trỏ về fact vừa invalidate)
```

**"Một registration" nghĩa là MỘT VALID lineage head, không phải một event record duy nhất mãi mãi** — một `account_id` có thể có NHIỀU `AccountRegistered` record trong log (một original + N correction replacement), nhưng tại một thời điểm CHỈ đúng MỘT trong số đó là lineage head VALID (append-only).

### Scope/identity error (đúng ADR-012 §2.1 "rebinding")

Khi registration gốc có **scope identity SAI** (`account_boundary_ref` hoặc `environment` gán nhầm ngay từ đầu — đây KHÔNG phải lỗi mutable metadata, đây là "Account này bị định danh sai boundary/environment"):

```text
invalidate initial fact SAI (AccountFactInvalidated, account_fact_correction_class = SCOPE_ERROR)
→ KHÔNG replace dưới subject cũ — CẤM tuyệt đối một replacement registration
  với supersedes_fact_ref trỏ về đây
→ đăng ký một subject MỚI: account_id MỚI (opaque, globally unique, KHÔNG derive từ scope
  đúng — đóng C2-MAJ-01, xem §1), với scope ĐÚNG
```

**Subject cũ KHÔNG được tiếp tục authoritative** — sau invalidation, subject cũ vĩnh viễn không có lineage head VALID nào khác. Đây chính là "rebinding" mà ADR-012 §2.1 đã cấm thực hiện tại chỗ — account.md implement quy tắc này bằng correction lineage đóng, không phát minh cơ chế khác. **account_id MỚI này KHÔNG liên quan gì tới scope cũ hay mới về mặt cấu trúc** — nó là một opaque identifier độc lập, gán mới, chỉ TÌNH CỜ mang scope đúng trong invariant của nó (§1) — không có công thức nào suy account_id mới từ account_id cũ hay từ scope (đóng C2-MAJ-01).

## 12. Time semantics và bitemporal correctness

```text
effective_time    — khi fact này THỰC SỰ có hiệu lực làm reference data (forward-looking cho revision, hoặc lịch sử cho correction)
recorded_time     — khi Ride ghi nhận fact này (bắt buộc, mọi event — envelope §2)
market_time       — PROHIBITED (§2)
```

**Không dùng `event_time`.**

**Historical Replay PHẢI dùng đúng metadata có hiệu lực TẠI computation cursor, không phải giá trị hiện tại** — cùng nguyên tắc recorded-time-visibility + effective-time-eligibility đã khóa xuyên suốt Package 0.2 (không look-ahead).

**Correction visibility:** `AccountFactInvalidated` và replacement đều có `recorded_time` mới; replay tại cursor trước đó chỉ thấy fact gốc — correction KHÔNG BAO GIỜ visible cho một replay cursor trước recorded_time của chính correction đó.

## 13. Downstream reference contract (cho Package 0.2-C3–C7)

Package sau (Strategy, Risk, Execution Intent, Order, Fill, Position — chưa author) tham chiếu Account qua ĐÚNG bốn field, KHÔNG hơn:

```yaml
account_id: {type: string, required: true, ref: account}
venue_id: {type: string, required: false, description: "CHỈ có mặt khi boundary_type=venue (§1) — TUYỆT ĐỐI ABSENT (không phải empty string, không phải null-placeholder) khi boundary_type=broker_account (v0.2, đóng C2-MAJ-04); KHÔNG parse từ account_id"}
environment: {type: enum, values: [PAPER, LIVE], description: "bất biến theo Account — resolve theo quy tắc downstream authority dưới"}
account_status: {type: enum, values: [ACTIVE, SUSPENDED, CLOSED], description: "resolve TẠI cursor liên quan theo quy tắc downstream authority dưới — CHỈ ACTIVE mới eligible cho action mới, §5"}
```

**Downstream authority rule — MỘT quy tắc duy nhất, không ngoại lệ (v0.2, đóng C2-MAJ-04):** downstream package PHẢI resolve `venue_id`/`environment`/`account_status` TRỰC TIẾP từ authoritative Account event stream (§3–§6) TẠI ĐÚNG recorded/effective cursor mà chính computation đó đang dùng. `AccountCurrentView` latest-state thông thường (§7, `GetCurrentAccount`) KHÔNG BAO GIỜ được dùng làm input — nó không cursor-addressable, chỉ query/UI. Một materialized projection CHỈ được chấp nhận làm cache tính toán khi ĐỒNG THỜI: (a) cursor-addressable (hỗ trợ resolve tại một cursor cụ thể, không chỉ "mới nhất"); VÀ (b) provably equivalent với authoritative reconstruction tại đúng cursor, contract version, configuration đang dùng (§7). Vi phạm điển hình cần tránh: dùng row `GetCurrentAccount` "mới nhất" cho một historical replay ở cursor cũ hơn — đây là look-ahead, CẤM tuyệt đối. KHÔNG package nào được tự phát minh identity/boundary semantics khác — `account_id`/`account_boundary_ref`/`environment` là nguồn định nghĩa DUY NHẤT tại đây.

**account.md KHÔNG author** bất kỳ semantic nào của Strategy/Decision/Risk/Execution Intent/Order/Fill/Position — các Domain Contract đó (Package 0.2-C3–C7, chưa authorize) tự định nghĩa cách chúng dùng bốn field trên, account.md chỉ đảm bảo bốn field này tồn tại, ổn định, và resolve được đúng.

## 14. Ngoài phạm vi — defer

**Deferred tường minh, không author ở C2 (Phase 1 implementation concern, non-blocking):**

- Cơ chế credential reference cụ thể (Vault/KMS binding, signing service integration) — đúng ADR-012 §6 "Thuộc Domain Contract, KHÔNG thuộc ADR này: cơ chế credential reference cụ thể."
- Runtime worker ownership cho việc emit/consume Account event (Phase 1 Engineering/Plugin Model).
- Transaction boundary cụ thể khi ghi Account event (Phase 1).
- Retry/backoff cho ingress Account registration/update (Phase 1, cùng nguyên tắc defer đã áp dụng cho `instrument.md`).
- Monitoring và escalation khi Account SUSPENDED/CLOSED bất ngờ (Phase 1 operational concern).
- Operational recovery orchestration (Phase 1).
- **Broker Account Boundary** Domain Contract riêng (khi `boundary_type: broker_account` cần schema/field chi tiết hơn opaque reference) — chưa cần cho walking skeleton hiện tại (Phase 0-3 chỉ có venue boundary thực tế, đúng ADR-012 §5 Scale check).
- Onboarding/KYC/broker approval workflow — hoàn toàn ngoài phạm vi Domain Contract, thuộc operational/compliance process.
- PAPER→LIVE "promotion" workflow — không author; đổi environment nghĩa là Account mới (§1), quy trình vận hành thực tế (nếu có) là Phase 1 concern.
- Billing, multi-tenant IAM, organization/tenant model — KHÔNG đồng nhất với Account (Chapter 6 §6.4 "Account ≠ Tenant"), không author ở đây hay bất kỳ đâu trong Package 0.2-C mà không có ADR riêng.
- Custody system implementation.
- Strategy/Decision/Risk/Execution Intent/Order/Fill/Position/Replay Event semantics (Package 0.2-C3–C7, chưa authorize).

## 15. Prohibitions

**Account KHÔNG được sở hữu:** raw exchange credential (API key, private key, token, password — §10); Strategy/Decision/Risk conclusion; Execution Intent/Order/Fill/Position semantics; billing state; tenant/organization/IAM identity (Chapter 6 §6.4); custody/signing implementation; Instrument/Venue semantics (chỉ tham chiếu `venue_id` qua `account_boundary_ref` khi `boundary_type: venue`, không định nghĩa lại `venue.md`).

## 16. Open questions ngoài phạm vi

- Cơ chế cụ thể generate `credential_reference` và binding thực tế tới Vault/KMS — chưa quyết, Phase 1 Security & Custody Baseline (đúng ADR-012 §6).
- `boundary_id` khi `boundary_type: broker_account` hiện là opaque string thuần túy — chưa có Domain Contract hay registry nào định nghĩa format/resolve mechanism; cần quyết khi Package 0.2-C thực sự cần một broker-routed Account đầu tiên.
- Cơ chế đăng ký Account cụ thể (thủ công qua Product Owner/operator workflow, hay tự động từ external onboarding feed) — cả hai đều hợp lệ theo envelope §2, không chọn một cách duy nhất, cùng nguyên tắc `instrument.md`/`venue.md`.
- Không đóng OQ-002/OQ-003.
