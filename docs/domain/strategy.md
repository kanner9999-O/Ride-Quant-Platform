---
id: strategy
title: Strategy
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

# Strategy

> **Vai trò của tài liệu này:** Domain Contract duy nhất của Package 0.2-C3 (Strategy Foundation) — định nghĩa **Strategy Definition Version** và **Strategy Instance**, đủ để package sau (Trade Intent, Decision — Package 0.2-C4, chưa authorize) tham chiếu deterministic một Strategy mà KHÔNG phải tự phát minh identity/version/evidence semantics. Draft, chưa Approved/Locked. Thuộc capability `strategy-management` / context `strategy-definition` (đăng ký MỚI tại [`context-map.yaml`](./context-map.yaml) trong transaction này). Kiến trúc controlling: [ADR-013](../adr/ADR-013.md) v0.3 **Approved** (Strategy Definition Version — Independent Evidence Axis) — tài liệu này CHỈ implement field/invariant mà ADR-013 §2 yêu cầu, KHÔNG lặp lại toàn văn ADR, KHÔNG tự quyết architecture mới ngoài phạm vi đã khóa. Cũng tuân thủ [Chapter 9 §9.1](../constitution/09-plugin-model.md)/[§9.3](../constitution/09-plugin-model.md) (Locked) cho Plugin Version/Package-Build-Artifact/Strategy Instance identity boundary.

Strategy **KHÔNG phải** Plugin Definition/Plugin Version/module-registry entry ([Chapter 9 §9.1](../constitution/09-plugin-model.md): `Plugin Definition ≠ Strategy Definition ≠ Strategy Instance`), KHÔNG phải strategy DSL hay executable code, KHÔNG phải optimizer/backtest engine, KHÔNG phải Trade Intent/Decision/Risk/Execution Intent/Order/Fill/Position (Package 0.2-C4–C7, chưa author), KHÔNG phải capital allocation/multi-strategy arbitration, KHÔNG phải Live activation workflow. Nó là **identity, version, và evidence tham chiếu tối thiểu**, bitemporal, authoritative, cho business/decision semantics của một chiến lược VÀ cho runtime binding cụ thể của chiến lược đó — đủ để C4 pin đúng bốn trục evidence mà [ADR-010 §75](../adr/ADR-010.md) yêu cầu.

**`strategy_definition_version_id`/`strategy_instance_id` là hai identifier MỚI, CHƯA từng được Domain Contract nào trước đây tham chiếu** — tài liệu này là nguồn định nghĩa CHÍNH THỨC. Package 0.2-C4–C7 PHẢI dùng đúng tên/shape này (`opaque string`, `ref: strategy`) khi tham chiếu Strategy — không tự đặt tên khác.

**Ghi chú tổ chức file (Product Owner authorized):** ADR-013 §2.1 mô tả `strategy-definition.md`/`strategy-instance.md` như hai tên file giả định khi ADR được author (2026-07-28, trước khi C3 thực sự authorize) — quyết định tổ chức file KHÔNG thuộc phạm vi ADR-013 (ADR chỉ khóa kiến trúc bốn-trục độc lập, không khóa Domain Contract file boundary). Product Owner đã xác nhận tường minh cho transaction C3 này: **một file `strategy.md` duy nhất** định nghĩa cả Strategy Definition Version lẫn Strategy Instance — không tạo `strategy-definition.md`/`strategy-instance.md` riêng. Điều này KHÔNG vi phạm ADR-013 (bốn-trục độc lập vẫn giữ nguyên, §5/§10 dưới), chỉ là một quyết định tổ chức tài liệu.

Strategy bao gồm **hai concept riêng biệt, không gộp làm một aggregate**:

1. **Strategy Definition Version** (`kind: entity`) — business/decision semantics bất biến của một chiến lược tại một phiên bản cụ thể: thesis, supported capability/instrument-class, required input contracts, decision-rule reference, explanation contract, downstream output capability. Một `strategy_definition_id` (family, opaque, KHÔNG tự có registration event riêng — chỉ là scope field nhóm các Version, xem §1) có thể có NHIỀU Version bất biến.
2. **Strategy Instance** (`kind: entity`) — runtime binding cụ thể: pin ĐỦ bốn trục evidence độc lập (Strategy Definition Version · Plugin Version · Configuration Version · Package/Build Artifact) + Account + instrument selection, theo đúng [ADR-013 §2.4](../adr/ADR-013.md)/[Chapter 9 §9.3](../constitution/09-plugin-model.md).

**`strategy-definition-version-registered`/`strategy-definition-version-fact-invalidated`/`strategy-instance-registered`/`strategy-instance-status-changed`/`strategy-instance-fact-invalidated`/`strategy-instance-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây. Display name, concept ID, và `event_type` là ba đại lượng khác nhau, không cạnh tranh identity — cùng nguyên tắc mọi Domain Contract trước.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/0.2-C1/0.2-C2** (đóng trước, không chờ review round phát hiện): opaque identity không parse/không derive từ scope (đóng trước lớp lỗi `C2-MAJ-01`-style); envelope binding cho `*FactInvalidated`; correction lineage cho phép sửa cả terminal-state fact (đóng trước lớp lỗi `C2-MAJ-02`-style, kèm `supersedes_fact_ref` trên MỌI event correctable ngay từ đầu); fold algorithm "visible-valid-head per slice" (đóng trước lớp lỗi `C2-MAJ-03`-style); Current View KHÔNG BAO GIỜ là authority, latest-state KHÔNG cursor-addressable, cache chỉ chấp nhận khi cursor-addressable + provably equivalent (đóng trước lớp lỗi `C2-MAJ-04`-style); canonical policy identifier khai báo ĐÚNG MỘT NƠI trong file này (context `strategy-definition` riêng, KHÔNG cross-reference `instrument.md`/`account.md`).

**Phạm vi bounded tường minh (v0.1):** KHÔNG author Trade Intent/Decision semantics (Package 0.2-C4). KHÔNG author strategy DSL/executable code. KHÔNG author optimizer/backtest engine. KHÔNG author capital allocation/multi-strategy arbitration. KHÔNG author Live activation workflow — `environment: LIVE` (kế thừa qua `account_id`, §6) chỉ là domain value phân biệt, KHÔNG authorize Live execution của platform. Đây là minimum executable specification, không phải perfect document — dễ revise từ implementation evidence (Phase 1).

**v0.2 — bounded correction, đóng `C3-MAJ-01`/`C3-MAJ-02`/`C3-MAJ-03`/`C3-MAJ-04`/`C3-MIN-01`/`C3-MIN-02` (consolidated Review A + Independent Review B findings):** (a) `C3-MAJ-01` — `instrument_selection_ref` v0.1 là opaque string, shape chưa pin, khiến C4 phải tự phát minh; v0.2 pin shape cụ thể `{instrument_id, venue_id, listing_id}` — đúng MỘT TradableListing cụ thể, cả ba field bắt buộc, resolve từ authoritative C1 history (`instrument.md`/`venue.md`) TẠI cùng cursor, KHÔNG tạo Selection aggregate (§5). (b) `C3-MAJ-02` — pin Strategy Instance chỉ eligible cho computation MỚI khi `strategy_definition_version_ref` VALID tại computation cursor; invalidation KHÔNG tự động pause/retire Instance, lịch sử computation trước cursor giữ nguyên, Definition Version đã sửa cần Strategy Instance MỚI (§9a). (c) `C3-MAJ-03` — pin Strategy Instance chỉ eligible cho computation MỚI khi Account `ACTIVE` tại cùng cursor; SUSPENDED/CLOSED KHÔNG tự động mutate Instance lifecycle, historical evidence giữ nguyên, KHÔNG author Order/Position/recovery behavior (§9a). (d) `C3-MAJ-04` — pin cả bốn trục evidence phải persistently resolvable tại computation cursor; không resolvable ⟹ computation mới deterministically ineligible, KHÔNG mutable-latest/inferred fallback/proxy nào được chấp nhận, Instance KHÔNG bị mutate (§9a, §11). (e) `C3-MIN-01` — thắt chặt `strategy_definition_id`: gán tại Version ĐẦU TIÊN của gia đình, KHÔNG BAO GIỜ tái sử dụng cho gia đình Strategy khác, KHÔNG tạo family aggregate/registration event/version graph/approval workflow (§1). (f) `C3-MIN-02` — thêm MỘT normative derived rule `eligible_for_new_computation`, hợp nhất sáu điều kiện (Instance ACTIVE, Definition Version VALID, Account ACTIVE, environment resolve nhất quán, bốn trục evidence resolvable, instrument selection eligible), cùng cursor (§9a) — thuộc Strategy eligibility ONLY, KHÔNG author Trade Intent/Decision/Risk/Execution behavior. Bounded — không đổi Strategy Definition Version/Strategy Instance separation, bốn trục độc lập, immutable Instance binding, lifecycle ACTIVE/PAUSED/RETIRED, RETIRED forward terminality, status correction lineage, no-mutable-latest, same-cursor authoritative reconstruction, Current View non-authority, một file `strategy.md` duy nhất, ADR-013.

**v0.3 — micro-correction, đóng `C3-DELTA-MAJ-01` (repository-wide shape consistency):** hai vị trí còn sót lại khai báo `instrument_selection_ref` là scalar `string` sau khi v0.2 đã pin shape object — `StrategyInstanceCurrentView.scope` (§9) và C4 downstream reference contract (§10) — đều thay bằng đúng object `{instrument_id, venue_id, listing_id}` đã pin tại §5/§6. Shape nay nhất quán tại tất cả sáu vị trí: Strategy Instance entity schema (§5), `subject_ref.scope` (§2), `StrategyInstanceRegistered` payload (§6), `StrategyInstanceCurrentView.scope` (§9), C4 downstream reference contract (§10), unified eligibility rule (§9a). Micro-correction thuần shape — không đổi eligibility semantics, identity, lifecycle, correction/replay semantics, bốn trục evidence, hay bất kỳ nội dung normative nào khác; vẫn đúng MỘT TradableListing cụ thể, không Selection aggregate, không multi-instrument.

## 1. Strategy Definition Version — `kind: entity`

**Strategy Definition thực hiện HOÀN TOÀN qua Version — không có registration event riêng cho family.** `strategy_definition_id` là một SCOPE field nhóm nhiều Version bất biến lại với nhau (family identity), tương tự cách `instrument_id`/`venue_id` là scope field của TradableListing — KHÔNG phải một subject/entity được đăng ký độc lập. Điều này tránh phát minh một cơ chế "family registration" không cần thiết: family identity đơn giản là giá trị `strategy_definition_id` nhất quán xuyên suốt mọi Version thuộc cùng chiến lược.

```yaml
id: strategy-definition-version
kind: entity
capability_id: strategy-management
domain_context_id: strategy-definition
description: >
  Identity bất biến của MỘT phiên bản business/decision semantics cho một chiến lược — đúng
  ADR-013 §2.1/§2.3 (Referenced Authoritative Artifact, Chapter 8 §8.1.1: versioned, immutable
  sau khi tham chiếu, không tái dùng identifier, persistently resolvable, verifiable content
  identity). KHÔNG có "current/latest definition" mutable — mọi thay đổi business/decision
  semantics tạo MỘT Version MỚI, KHÔNG sửa Version đang có (ADR-013 §2.3, cấm tường minh).
invariants:
  - "strategy_definition_version_id là opaque, globally unique trong toàn Ride, gán tại thời điểm StrategyDefinitionVersionRegistered — KHÔNG derive/resolve từ strategy_definition_id hay bất kỳ field nội dung nào (đóng trước lớp lỗi C2-MAJ-01-style). Bất biến, KHÔNG tái sử dụng cho nội dung khác (Chapter 6 §6.1, Chapter 8 §8.1.1 mục 3)."
  - "**v0.2 (đóng C3-MIN-01):** strategy_definition_id là opaque, globally unique, stable — gán tại thời điểm Version ĐẦU TIÊN của một gia đình Strategy logic được đăng ký (StrategyDefinitionVersionRegistered đầu tiên mang giá trị strategy_definition_id đó), KHÔNG BAO GIỜ tái sử dụng cho một gia đình Strategy logic KHÁC. Một Version SAU CÓ THỂ mang lại ĐÚNG strategy_definition_id này CHỈ KHI nó thuộc CÙNG gia đình Strategy logic (business continuity — cùng chiến lược, phiên bản mới); việc gán đúng gia đình là kỷ luật tác giả/operator workflow (Phase 1, §14), KHÔNG tự động verify bởi Domain Contract này."
  - "strategy_definition_id KHÔNG tự có registration event riêng — chỉ là scope field nhóm nhiều Version (KHÔNG tạo family aggregate, KHÔNG family registration event, KHÔNG version graph, KHÔNG approval workflow). Một strategy_definition_id có thể gắn với NHIỀU strategy_definition_version_id (một Definition có nhiều Version bất biến, đúng yêu cầu 'One Definition may have multiple immutable versions')."
  - "TOÀN BỘ payload của một Version (thesis, supported_scope, required_input_contracts, decision_rule_ref, explanation_contract_ref, downstream_output_capability) là NỘI DUNG BẤT BIẾN — không có field nào 'mutable metadata' tách biệt như Account/Venue. KHÔNG có AccountMetadataRevised-style PATCH event cho subject này — bất kỳ thay đổi nội dung nào, dù nhỏ, đều nghĩa là MỘT strategy_definition_version_id MỚI (đúng ADR-013 §2.2/§2.3)."
  - "strategy_definition_id, một khi gán cho một strategy_definition_version_id, KHÔNG được đổi cho chính record đó — nhưng KHÔNG cấm một Version MỚI (ID khác) thuộc một strategy_definition_id khác, kể cả khi nó là bản 'sửa' của một Version trước — xem §3 correction lineage (KHÔNG có same-ID replacement path cho subject này, chỉ có 'invalidate + đăng ký Version MỚI')."
  - "account_id KHÔNG xuất hiện trong Strategy Definition Version — Definition Version là business/decision semantics độc lập Account (nhiều Strategy Instance, thuộc nhiều Account khác nhau, có thể cùng pin một Definition Version, §5)."
schema:
  strategy_definition_version_id: {type: string, required: true, description: "opaque, globally unique, immutable — xem invariants"}
  strategy_definition_id: {type: string, required: true, description: "opaque, stable — scope field nhóm Version cùng gia đình chiến lược, KHÔNG phải subject riêng"}
  thesis: {type: string, required: true, description: "mô tả business rationale — nội dung tự do, opaque với domain logic"}
  supported_scope: {type: string, required: true, description: "capability/instrument-CLASS (ví dụ 'trend-following trên crypto major liquid pairs') — KHÔNG phải instrument cụ thể (đúng ADR-013 §2.2). Instrument cụ thể thuộc Strategy Instance, §5."}
  required_input_contracts: {type: array, items: string, required: true, description: "opaque list of contract reference (ví dụ concept ID của context/feature Domain Contract) — KHÔNG resolve/validate bởi chính Domain Contract này; C4 (Decision, chưa author) chịu trách nhiệm resolve thực tế"}
  decision_rule_ref: {type: string, required: true, description: "opaque reference tới decision-rule identity — KHÔNG author Decision semantics ở đây (Package 0.2-C4, chưa author)"}
  explanation_contract_ref: {type: string, required: true, description: "opaque reference tới explanation contract (I-1 Explainability liên quan) — KHÔNG định nghĩa schema explanation contract ở đây"}
  downstream_output_capability: {type: string, required: true, description: "opaque capability tag mô tả loại output Version này có khả năng sinh ra downstream (ví dụ 'trade-intent-capable') — KHÔNG author Trade Intent semantics ở đây"}
events_emitted: [StrategyDefinitionVersionRegistered, StrategyDefinitionVersionFactInvalidated]
events_consumed: []
commands: []
queries: []
```

**Khi nào BẮT BUỘC tạo Version mới (ADR-013 §2.2, kỷ luật tác giả, không tự động enforce được bởi Domain Contract):** thay đổi `thesis`; thay đổi `supported_scope`; thay đổi `required_input_contracts`; thay đổi `decision_rule_ref`; thay đổi `explanation_contract_ref`. **Khi nào KHÔNG bắt buộc Version mới** (đúng yêu cầu task, đúng ADR-013 §2.2): plugin refactor (Plugin Version đổi độc lập, §5); thay đổi parameter/Configuration Version; Account reassignment (thuộc Instance, §5, không thuộc Definition); chọn instrument tương thích khác trong CÙNG supported_scope class; rebuilt executable artifact (Package/Build Artifact đổi độc lập, §5, đúng ADR-013 §2.5).

## 2. Canonical event envelope — áp dụng cho mọi Strategy event (§3–§4, §6–§8)

Mọi event trong tài liệu này là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). Mục này khóa **envelope chung** một lần.

```yaml
envelope:
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2)
  event_contract_ref: {cardinality: required}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}             # khi Ride ghi nhận fact này
  subject_ref: {cardinality: "required — shape canonical, xem dưới. Trên mọi *FactInvalidated (§4, §8), PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate."}
  stream_ref: {cardinality: required}                # Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # Phase 1, chưa author
  correlation_id: {cardinality: "required khi computation thuộc một correlation flow tường minh; optional khi độc lập"}
  causation_refs: {cardinality: "StrategyDefinitionVersionRegistered/StrategyInstanceRegistered: zero-or-more (fact gốc, không nhất thiết có causal ancestor authoritative — đăng ký thủ công qua operator workflow, Phase 1). Mọi event khác (status-change/invalidation): KHÔNG BAO GIỜ rỗng."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3."}
  effective_time: {cardinality: "required — semantic khác theo event type, xem §3–§4/§6–§8 cho nội dung cụ thể."}
  market_time: {cardinality: "PROHIBITED — Strategy là reference/evidence data authoritative, không phải quan sát trực tiếp venue theo nghĩa market_time (Chapter 5 §5.2)."}
  source_identity: {cardinality: "optional — có mặt khi fact đến từ external onboarding feed có khả năng retry/redelivery (Chapter 6 §6.6); PROHIBITED khi đăng ký thủ công qua Product Owner/operator workflow (Phase 1, chưa author)."}

subject_ref (Strategy Definition Version):
  context_id: strategy-definition
  subject_kind: entity
  subject_type: StrategyDefinitionVersion
  subject_id: <strategy_definition_version_id — opaque, stable, xem §1>
  scope:
    strategy_definition_id: <string>

subject_ref (Strategy Instance, §5):
  context_id: strategy-definition
  subject_kind: entity
  subject_type: StrategyInstance
  subject_id: <strategy_instance_id — opaque, stable, xem §5>
  scope:
    strategy_definition_version_ref: <string>
    plugin_version_ref: <string>
    configuration_version_ref: <string>
    package_build_artifact_ref: <string>
    account_id: <string>
    instrument_selection_ref: {instrument_id: <string>, venue_id: <string>, listing_id: <string>}   # v0.2, đóng C3-MAJ-01

event_types:
  StrategyDefinitionVersionRegistered: STRATEGY_DEFINITION_VERSION_REGISTERED
  StrategyDefinitionVersionFactInvalidated: STRATEGY_DEFINITION_VERSION_FACT_INVALIDATED
  StrategyInstanceRegistered: STRATEGY_INSTANCE_REGISTERED
  StrategyInstanceStatusChanged: STRATEGY_INSTANCE_STATUS_CHANGED
  StrategyInstanceFactInvalidated: STRATEGY_INSTANCE_FACT_INVALIDATED
```

`stream_ref`/`producer_ref` — Phase 1, chưa tồn tại, cùng nguyên tắc defer xuyên suốt Package 0.2-B/C1/C2.

## 3. `StrategyDefinitionVersionRegistered` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: strategy-definition-version-registered
kind: event
capability_id: strategy-management
domain_context_id: strategy-definition
description: >
  Fact AUTHORITATIVE cho việc đăng ký MỘT Strategy Definition Version bất biến — thiết lập TOÀN
  BỘ nội dung (thesis, supported_scope, required_input_contracts, decision_rule_ref,
  explanation_contract_ref, downstream_output_capability) và scope family (strategy_definition_id)
  cùng lúc, KHÔNG tách "identity bất biến" khỏi "mutable metadata" như Account/Venue — mọi field
  ở đây bất biến (§1). KHÔNG có supersedes_fact_ref — subject này KHÔNG BAO GIỜ có same-ID
  replacement (§4 giải thích lý do).
invariants:
  - "payload.strategy_definition_version_id PHẢI khớp đúng subject_ref.subject_id VÀ payload.strategy_definition_id PHẢI khớp đúng subject_ref.scope.strategy_definition_id."
  - "envelope.effective_time = thời điểm Version này có hiệu lực làm reference/evidence data — mặc định bằng recorded_time trừ khi backfill lịch sử tường minh pin effective_time sớm hơn (§9)."
  - "KHÔNG có field supersedes_fact_ref trong payload — subject này KHÔNG hỗ trợ same-ID correction replacement (§4)."
payload:
  strategy_definition_version_id: {type: string, required: true}
  strategy_definition_id: {type: string, required: true}
  thesis: {type: string, required: true}
  supported_scope: {type: string, required: true}
  required_input_contracts: {type: array, items: string, required: true}
  decision_rule_ref: {type: string, required: true}
  explanation_contract_ref: {type: string, required: true}
  downstream_output_capability: {type: string, required: true}
```

## 4. `StrategyDefinitionVersionFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2 — `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: strategy-definition-version-fact-invalidated
kind: event
capability_id: strategy-management
domain_context_id: strategy-definition
description: >
  Phủ định MỘT StrategyDefinitionVersionRegistered ĐÃ SAI thực tế — thuần túy ghi nhận "fact này
  không còn hợp lệ", KHÔNG tự nó tuyên bố giá trị mới. **KHÔNG có same-ID replacement path** —
  vì TOÀN BỘ payload của một Version là nội dung bất biến (§1, không có "mutable metadata"
  tách biệt để sửa tại chỗ), correction LUÔN LUÔN nghĩa là đăng ký một strategy_definition_version_id
  MỚI (giữ nguyên hoặc đổi strategy_definition_id tùy bản chất lỗi — KHÔNG BAO GIỜ supersede
  record cũ). Điều này đơn giản hóa so với Account/Instrument (không cần
  METADATA_ERROR/SCOPE_ERROR distinction, vì không có trường hợp 'sửa tại chỗ' nào tồn tại cho
  subject này).
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref."
  - "invalidated_fact_ref PHẢI trỏ một StrategyDefinitionVersionRegistered, CHƯA từng nhận invalidation khác — một fact chỉ bị invalidate đúng một lần. KHÔNG BAO GIỜ trỏ một StrategyDefinitionVersionFactInvalidated khác (cấm invalidation-of-invalidation)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead)."
  - "Sau invalidation, strategy_definition_version_id đó VĨNH VIỄN TERMINALLY_INVALID (§9) — KHÔNG BAO GIỜ có replacement dưới cùng ID. Bất kỳ StrategyInstanceRegistered nào tham chiếu strategy_definition_version_ref TỚI ID này PHẢI kiểm tra validity TẠI cursor liên quan trước khi đăng ký (§7)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

**Validity query (non-authoritative, KHÔNG ngụ ý 'latest/current' — đúng ADR-013 §2.3):** `GetStrategyDefinitionVersionValidity(strategy_definition_version_id, recorded_cursor) → VALID | TERMINALLY_INVALID`. Đây KHÔNG phải một `AccountCurrentView`-style read model đầy đủ — chỉ là một validity check tại một `strategy_definition_version_id` CỤ THỂ đã biết, tuyệt đối KHÔNG trả về "phiên bản mới nhất của family X" dưới bất kỳ hình thức nào (tránh tạo mutable "current definition" mà ADR-013 §2.3 cấm tường minh). `ListStrategyDefinitionVersions(strategy_definition_id)` (nếu implementation cần) chỉ trả về TẬP HỢP các `strategy_definition_version_id` VALID thuộc family đó — KHÔNG có thứ tự ngụ ý "current", không có field "latest".

## 5. Strategy Instance — `kind: entity`

```yaml
id: strategy-instance
kind: entity
capability_id: strategy-management
domain_context_id: strategy-definition
description: >
  Runtime binding cụ thể — pin ĐỦ bốn trục evidence độc lập (đúng ADR-013 §2.1/§2.4, Chapter 9
  §9.3) cộng Account và instrument selection. Một Strategy Instance là MỘT subject liên tục theo
  scope — không có subject mới per status change; nhưng bất kỳ thay đổi nào ở BỐN TRỤC, account_id,
  hay instrument_selection_ref đều tạo một Strategy Instance KHÁC (KHÔNG mutate binding hiện có,
  đúng Chapter 9 §9.3 mục 2: "Đổi plugin version hoặc configuration phải tạo binding mới hoặc
  instance version mới — KHÔNG mutate ngầm").
invariants:
  - "strategy_instance_id là opaque, globally unique trong toàn Ride, gán tại StrategyInstanceRegistered — KHÔNG derive/resolve từ bất kỳ trục nào trong sáu field scope (đóng trước lớp lỗi C2-MAJ-01-style). Bất biến, KHÔNG tái sử dụng cho subject khác (Chapter 6 §6.1, Chapter 9 §9.3 mục 1: 'Instance identity ổn định qua restart/redeploy')."
  - "**Bốn trục evidence BẮT BUỘC độc lập (đóng ADR-013 §2, §10 dưới):** strategy_definition_version_ref · plugin_version_ref · configuration_version_ref · package_build_artifact_ref — KHÔNG trục nào được derive/resolve/proxy từ trục khác. Domain logic CẤM suy diễn một trục từ trục còn lại (ví dụ CẤM suy plugin_version_ref từ configuration_version_ref, hay ngược lại)."
  - "strategy_definition_version_ref PHẢI trỏ một StrategyDefinitionVersionRegistered VALID (KHÔNG TERMINALLY_INVALID, §4/§9) TẠI recorded cursor của chính StrategyInstanceRegistered này."
  - "plugin_version_ref/package_build_artifact_ref PHẢI resolvable theo đúng yêu cầu Chapter 9 §9.1 (Package/Build Artifact là exact executable bytes/content identity đang THỰC SỰ chạy — KHÔNG dùng Plugin Version hay source commit hash làm proxy cho artifact identity, ADR-013 §2.5)."
  - "account_id PHẢI trỏ một Account đã AccountRegistered (account.md §3) — Instance KHÔNG hợp lệ nếu account_id chưa tồn tại. MỘT Instance bind ĐÚNG MỘT Account — không có multi-account Instance."
  - "environment KHÔNG PHẢI field riêng của Strategy Instance — resolve TRỰC TIẾP từ Account (account.md §1, immutable) qua account_id, TẠI cùng cursor mà computation đang dùng (đóng yêu cầu 'Account and environment must resolve from authoritative same-cursor history') — tránh duplicate source of truth (I-12). KHÔNG lưu bản sao environment trên Instance."
  - "**Instrument selection ownership — MỘT quy tắc duy nhất (đóng yêu cầu 'pin one authoritative ownership rule'):** `instrument_selection_ref` thuộc Strategy Instance (field bắt buộc, dưới đây) — KHÔNG thuộc Configuration Version. Configuration Version (Chapter 9 §9.1 concept, chưa author ở C3) có thể mang thêm tham số tinh chỉnh khác, nhưng KHÔNG sở hữu instrument selection — Instance là authoritative pin DUY NHẤT cho việc instrument/TradableListing nào Instance này target."
  - "**v0.2 (đóng C3-MAJ-01):** `instrument_selection_ref` pin ĐÚNG MỘT TradableListing cụ thể — `{instrument_id, venue_id, listing_id}`, cả BA field bắt buộc (KHÔNG phải object rỗng/partial). `instrument_id` PHẢI trỏ một Logical Instrument đã `InstrumentRegistered` (`instrument.md` §3); `venue_id` PHẢI trỏ một Venue đã `VenueRegistered` (`venue.md` §3); `listing_id` PHẢI trỏ một `TradableListing` đã `TradableListingCreated` cho ĐÚNG cặp (`instrument_id`, `venue_id`) đó (`instrument.md` §10) — cùng scope ba field đối xứng `instrument.md` §10, KHÔNG tự phát minh shape khác. Resolvability PHẢI kiểm tra tại authoritative C1 event stream (Instrument/Venue/TradableListing) TẠI CÙNG cursor mà `StrategyInstanceRegistered` (hoặc computation liên quan, §9a) đang dùng — KHÔNG dùng `InstrumentCurrentView`/`VenueCurrentView`/`TradableListingCurrentView` latest-state làm input (cùng nguyên tắc Current-View-never-authority đã khóa xuyên suốt `instrument.md` §7/§15)."
  - "instrument_selection_ref PHẢI nằm trong supported_scope của strategy_definition_version_ref tương ứng (§1) — Instance KHÔNG được chọn instrument ngoài class mà Definition Version hỗ trợ; xác minh cụ thể (parsing supported_scope) là Phase 1/C4 concern, ở đây chỉ pin RULE."
  - "Multi-instrument set, universe, và dynamic selection (nhiều listing cho một Instance, hoặc selection thay đổi theo thời gian) KHÔNG được hỗ trợ ở v0.1/v0.2 — MỘT Instance pin ĐÚNG MỘT listing, bất biến cùng toàn bộ scope (đúng invariant đầu tiên §5); mở rộng multi-instrument vẫn deferred (§14), KHÔNG tạo Selection aggregate."
  - "`environment: LIVE` (resolve qua account_id) KHÔNG tự động authorize Live execution của platform — đây thuần túy là domain value phân biệt account environment (đúng nguyên tắc account.md §8), Live execution authorization là quyết định governance riêng, tách bạch hoàn toàn."
schema:
  strategy_instance_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  strategy_definition_version_ref: {type: string, required: true, ref: strategy, description: "trục 1/4 — business/decision semantics"}
  plugin_version_ref: {type: string, required: true, description: "trục 2/4 — implementation-release identity (Chapter 9 §9.1)"}
  configuration_version_ref: {type: string, required: true, description: "trục 3/4 — exact parameter values cho instance này (Chapter 9 §9.1)"}
  package_build_artifact_ref: {type: string, required: true, description: "trục 4/4 — exact executable/deployable artifact identity đang chạy (Chapter 9 §9.1/§9.5, ADR-013 §2.5)"}
  account_id: {type: string, required: true, ref: account, description: "đúng MỘT Account — environment resolve qua đây, KHÔNG lưu riêng"}
  instrument_selection_ref:
    type: object
    required: true
    description: "concrete single-TradableListing selection — thuộc Instance, KHÔNG thuộc Configuration Version (xem invariants); v0.2 pin shape, đóng C3-MAJ-01"
    fields:
      instrument_id: {type: string, required: true, description: "opaque, trỏ Logical Instrument đã InstrumentRegistered (instrument.md §3)"}
      venue_id: {type: string, required: true, description: "opaque, trỏ Venue đã VenueRegistered (venue.md §3)"}
      listing_id: {type: string, required: true, description: "opaque, trỏ TradableListing đã TradableListingCreated cho đúng cặp (instrument_id, venue_id) — instrument.md §10"}
  display_name: {type: string, required: false, description: "mô tả tiện dụng, KHÔNG phải identity, gán một lần tại registration — KHÔNG có revision mechanism ở v0.1 (minimal, deferred §14)"}
state_machine:
  initial_state: UNSEEN
  states: [UNSEEN, ACTIVE, PAUSED, RETIRED]
  transitions:
    - {from: UNSEEN, to: ACTIVE, caused_by: StrategyInstanceRegistered}
    - {from: ACTIVE, to: PAUSED, caused_by: StrategyInstanceStatusChanged}
    - {from: PAUSED, to: ACTIVE, caused_by: StrategyInstanceStatusChanged}
    - {from: ACTIVE, to: RETIRED, caused_by: StrategyInstanceStatusChanged}
    - {from: PAUSED, to: RETIRED, caused_by: StrategyInstanceStatusChanged}
  terminal_states: [RETIRED]
events_emitted: [StrategyInstanceRegistered, StrategyInstanceStatusChanged, StrategyInstanceFactInvalidated]
events_consumed: []
commands: []
queries: []
```

**`UNSEEN` là notional initial state** — cùng convention xuyên suốt tài liệu. **`RETIRED` là terminal CHO FORWARD TRANSITION trên valid lineage** — không có `StrategyInstanceStatusChanged` forward nào được phép sau một RETIRED fact VALID (đúng Chapter 9 §9.8 "runtime lifecycle facts → event log"). Điều này KHÔNG chặn correction: một RETIRED fact ghi SAI vẫn correctable append-only qua `StrategyInstanceFactInvalidated` + same-slice replacement (§8, đóng trước lớp lỗi `C2-MAJ-02`-style — KHÔNG chờ review round phát hiện). **Ba state thực sự cần** (`ACTIVE`/`PAUSED`/`RETIRED`) — đúng yêu cầu "minimum lifecycle required to determine eligibility for new computation"; không thêm state onboarding/approval/parity-validation (đó là Phase 1/C4 operational concern, §14).

## 6. `StrategyInstanceRegistered` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: strategy-instance-registered
kind: event
capability_id: strategy-management
domain_context_id: strategy-definition
description: >
  Fact AUTHORITATIVE cho việc đăng ký MỘT Strategy Instance — thiết lập bốn trục evidence + Account
  + instrument selection cùng lúc, TOÀN BỘ bất biến (§5). KHÔNG có supersedes_fact_ref — subject
  này KHÔNG hỗ trợ same-ID correction replacement, cùng lý do như StrategyDefinitionVersionRegistered
  (§4): mọi field ở đây là scope bất biến, không có "mutable metadata" tách biệt. state_machine
  (§5) đưa Instance thẳng vào ACTIVE.
invariants:
  - "payload.strategy_instance_id PHẢI khớp đúng subject_ref.subject_id VÀ toàn bộ scope field PHẢI khớp subject_ref.scope."
  - "causation_refs PHẢI trỏ AccountRegistered (account.md §3) của account_id tương ứng — chứng minh Account đã tồn tại trước khi Instance đăng ký."
  - "**v0.2 (đóng C3-MAJ-01):** causation_refs PHẢI (cộng thêm) trỏ TradableListingCreated (instrument.md §10) của listing_id trong instrument_selection_ref — chứng minh TradableListing đã tồn tại trước khi Instance đăng ký, đối xứng invariant Account ở trên."
  - "envelope.effective_time = thời điểm Instance này thực sự bắt đầu hiệu lực (có thể khác recorded_time nếu backfill/future-dated activation)."
  - "KHÔNG có field supersedes_fact_ref trong payload — subject này KHÔNG hỗ trợ same-ID correction replacement (§8: correction luôn đăng ký strategy_instance_id MỚI)."
payload:
  strategy_instance_id: {type: string, required: true}
  strategy_definition_version_ref: {type: string, required: true}
  plugin_version_ref: {type: string, required: true}
  configuration_version_ref: {type: string, required: true}
  package_build_artifact_ref: {type: string, required: true}
  account_id: {type: string, required: true}
  instrument_selection_ref:
    instrument_id: {type: string, required: true}
    venue_id: {type: string, required: true}
    listing_id: {type: string, required: true}
  display_name: {type: string, required: false}
```

## 7. `StrategyInstanceStatusChanged` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: strategy-instance-status-changed
kind: event
capability_id: strategy-management
domain_context_id: strategy-definition
description: >
  Fact AUTHORITATIVE cho một operational status transition của Strategy Instance (§5
  state_machine) — ACTIVE↔PAUSED, (ACTIVE|PAUSED)→RETIRED. RETIRED là terminal CHO FORWARD
  TRANSITION (§5) — nhưng correctable append-only qua same-slice replacement (đóng trước lớp lỗi
  C2-MAJ-02-style: supersedes_fact_ref có mặt ngay từ v0.1, KHÔNG chờ review round phát hiện).
invariants:
  - "new_status PHẢI là một transition hợp lệ theo state_machine §5 từ current_status hiện tại — current_status resolve theo fold algorithm §9 (visible-valid-head per slice, total-order effective_time ASC/recorded_time ASC/event_id ASC), KHÔNG dùng raw recorded_time đơn thuần, KHÔNG dùng sequence xuyên stream, KHÔNG dùng một RETIRED fact đã bị invalidate mà chưa có replacement visible."
  - "new_status = RETIRED trên valid lineage hiện hành KHÔNG được có StrategyInstanceStatusChanged forward transition tiếp theo cho cùng strategy_instance_id (§5 terminal_states) — đây là ràng buộc FORWARD LIFECYCLE, không áp dụng cho correction record."
  - "Một RETIRED fact (hoặc bất kỳ StrategyInstanceStatusChanged nào khác) ghi SAI vẫn correctable qua StrategyInstanceFactInvalidated + same-slice StrategyInstanceStatusChanged replacement (§8, cùng (strategy_instance_id, effective_time) slice, supersedes_fact_ref trỏ đúng fact bị invalidate) — correction KHÔNG bị chặn bởi RETIRED terminality. Fold algorithm (§9) PHẢI recompute current_status từ valid corrected lineage sau khi replacement visible. KHÔNG thêm state/enum mới, KHÔNG thêm reactivation command ngoài cơ chế correction đã có."
  - "envelope.effective_time = thời điểm status transition này thực sự có hiệu lực (có thể khác recorded_time nếu biết trước lịch pause/retire)."
  - "**v0.2 (đóng C3-MIN-02):** current_status = ACTIVE là MỘT trong sáu điều kiện bắt buộc của unified computation-eligibility rule `eligible_for_new_computation` (§9a) — PAUSED/RETIRED CẤM computation mới, nhưng ĐƠN LẺ current_status = ACTIVE KHÔNG đủ điều kiện; xem §9a cho định nghĩa đầy đủ (Definition Version validity, Account lifecycle, evidence-reference resolvability, instrument selection eligibility). Đây là RÀNG BUỘC lên Domain Contract tương lai (Decision, Package 0.2-C4+, chưa author) — strategy.md chỉ PIN quy tắc, không tự enforce vì chưa có consumer nào tồn tại."
  - "supersedes_fact_ref VẮNG MẶT cho forward transition bình thường; BẮT BUỘC cho same-slice correction replacement — khi có mặt, PHẢI trỏ đúng StrategyInstanceStatusChanged (kể cả RETIRED) bị StrategyInstanceFactInvalidated target, cùng subject/effective_time (§8)."
payload:
  strategy_instance_id: {type: string, required: true}
  new_status: {type: enum, values: [ACTIVE, PAUSED, RETIRED], required: true}
  reason: {type: string, required: false}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho forward transition bình thường; BẮT BUỘC cho same-slice correction replacement — xem invariants và §8"}
```

## 8. `StrategyInstanceFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2 — `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: strategy-instance-fact-invalidated
kind: event
capability_id: strategy-management
domain_context_id: strategy-definition
description: >
  Phủ định MỘT fact lịch sử cụ thể ĐÃ SAI của Strategy Instance. Hai hành vi khác nhau theo
  target: (a) target = StrategyInstanceRegistered → KHÔNG BAO GIỜ có replacement dưới cùng
  strategy_instance_id (scope hoàn toàn bất biến, không có mutable metadata để sửa tại chỗ —
  cùng lý do §4) — correction thực tế là đăng ký một strategy_instance_id MỚI; (b) target =
  StrategyInstanceStatusChanged → same-slice replacement HỢP LỆ, đúng correction lineage chuẩn
  (§9), kể cả khi giá trị bị invalidate là RETIRED (đóng C2-MAJ-02-style).
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_time của invalidated_fact_ref."
  - "invalidated_fact_ref PHẢI trỏ một StrategyInstanceRegistered hoặc StrategyInstanceStatusChanged, CHƯA từng nhận invalidation khác — một fact chỉ bị invalidate đúng một lần. KHÔNG BAO GIỜ trỏ một StrategyInstanceFactInvalidated khác (cấm invalidation-of-invalidation)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead)."
  - "Target = StrategyInstanceRegistered: sau invalidation, strategy_instance_id đó VĨNH VIỄN TERMINALLY_INVALID (§9) — KHÔNG BAO GIỜ có replacement dưới cùng ID; correction thực tế đăng ký strategy_instance_id MỚI hoàn toàn độc lập."
  - "Target = StrategyInstanceStatusChanged: mong đợi (không bắt buộc ngay lập tức) một StrategyInstanceStatusChanged replacement CÙNG strategy_instance_id VÀ cùng effective_time slice, supersedes_fact_ref = event này (§9)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 9. `StrategyInstanceCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §6–§8.

**Canonical decision — no-row trước khi có fact đầu tiên (đúng convention xuyên suốt Package 0.2):**

```text
Trước khi StrategyInstanceRegistered tồn tại cho một strategy_instance_id:
  → KHÔNG có StrategyInstanceCurrentView row nào tồn tại
  → GetCurrentStrategyInstance trả về NOT_FOUND / ABSENT
```

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION`. Khi `PENDING_CORRECTION`, `pending_correction_class` BẮT BUỘC có mặt (đóng ngay từ v0.1, đúng pattern đã proven tại `instrument.md`/`venue.md`/`account.md`):

```text
view_state = VALID              → pending_correction_class: CẤM (phải absent)
view_state = PENDING_CORRECTION → pending_correction_class: BẮT BUỘC

target = StrategyInstanceRegistered (invalidate, không bao giờ replacement) → pending_correction_class = TERMINAL_SCOPE_INVALIDATION
target = StrategyInstanceStatusChanged (invalidate, chờ same-slice replacement) → pending_correction_class = AWAITING_SAME_SUBJECT_REPLACEMENT
```

`TERMINAL_SCOPE_INVALIDATION` KHÔNG BAO GIỜ transition về `VALID`; subject cũ vẫn queryable qua `GetStrategyInstanceHistory` làm historical evidence; consumer/retry worker KHÔNG được coi đây là "chờ và thử lại sau" (đúng nguyên tắc đã khóa tại `instrument.md` §19/`account.md` §7, áp dụng độc lập tại đây cho context `strategy-definition`).

**Fold algorithm (v0.1, "visible-valid-head per slice" — MỘT quy tắc chung, đóng ngay từ đầu, không chờ review round phát hiện như C2-MAJ-03):**

```text
1. Group mọi fact theo correction lineage/effective-time slice — mỗi (strategy_instance_id,
   effective_time) là một slice riêng.
2. Với mỗi slice, resolve StrategyInstanceFactInvalidated visibility tại cursor
   (recorded_time <= cursor).
3. Loại trừ khỏi lineage bất kỳ fact nào đã có invalidation visible tại cursor.
4. Chọn head hợp lệ (visible valid head) của slice: fact CHƯA bị invalidate visible, hoặc
   replacement mới nhất (chuỗi supersedes_fact_ref, CHỈ áp dụng cho StrategyInstanceStatusChanged,
   §8) CHƯA bị invalidate visible, chính head đó PHẢI visible tại cursor.
5. NẾU slice registration bị invalidate visible → toàn view chuyển PENDING_CORRECTION,
   pending_correction_class = TERMINAL_SCOPE_INVALIDATION (KHÔNG BAO GIỜ có replacement), DỪNG —
   không resolve field nào khác.
6. NẾU registration hợp lệ, tiếp tục fold StrategyInstanceStatusChanged: một slice status bị
   invalidate chưa có replacement visible KHÔNG đóng góp fact nào (không "giữ giá trị cũ") —
   fold dùng head hợp lệ của slice effective_time gần nhất trước đó.
7. Tổng hợp mọi visible-valid-head còn lại, total-order: effective_time ASC, recorded_time ASC,
   event_id ASC — KHÔNG dùng raw sequence xuyên stream — rồi mới lifecycle fold → current_status.
```

```yaml
id: strategy-instance-current-view
kind: read_model
capability_id: strategy-management
domain_context_id: strategy-definition
description: >
  Projection tiện dụng: status "hiện tại" (latest-state, KHÔNG cursor-addressable theo mặc định)
  của một Strategy Instance, rebuild được từ §6–§8 theo fold algorithm ở trên. KHÔNG authoritative
  — `GetCurrentStrategyInstance`/`GetStrategyInstanceHistory` CHỈ dùng cho query/UI, KHÔNG BAO GIỜ
  là input hợp lệ cho Domain Contract khác (Trade Intent/Decision, Package 0.2-C4+) hay Decision
  dưới BẤT KỲ hình thức nào, kể cả khi "trông giống" cùng giá trị — pin ngay từ v0.1 (đóng trước
  lớp lỗi C2-MAJ-04-style, KHÔNG chờ review round phát hiện). Downstream field PHẢI resolve qua
  authoritative Strategy Instance event stream (`ref: strategy`) TẠI CÙNG recorded/effective
  cursor mà computation đó đang dùng (§10). Một materialized projection CHỈ được dùng làm input
  tính toán khi ĐỒNG THỜI: (a) cursor-addressable — hỗ trợ query "as-of cursor X"; VÀ (b) provably
  equivalent với authoritative reconstruction tại đúng cursor/contract version/configuration.
  `GetCurrentStrategyInstance` KHÔNG thỏa điều kiện (a) — KHÔNG BAO GIỜ được downstream dùng làm
  input, kể cả như cache.
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism) — mọi implementation dùng cùng fold algorithm PHẢI cho cùng kết quả."
  - "KHÔNG được dùng làm input cho bất kỳ Domain Contract khác, Decision, hay computation nào — CHỈ query/UI, không có ngoại lệ cho artifact CỤ THỂ này."
  - "view_state PHẢI đúng theo Bước 4–5 của fold algorithm — registration lineage head quyết định, KHÔNG BAO GIỜ fallback về một registration đã invalidate."
  - "pending_correction_class BẮT BUỘC có mặt khi view_state = PENDING_CORRECTION; CẤM có mặt khi view_state = VALID."
  - "current_status PHẢI recompute đúng theo Bước 6–7 (visible-valid-head per slice) — một RETIRED fact đã invalidate mà chưa có replacement visible KHÔNG được góp phần vào current_status."
schema:
  strategy_instance_id: {type: string, required: true}
  scope: {strategy_definition_version_ref: string, plugin_version_ref: string, configuration_version_ref: string, package_build_artifact_ref: string, account_id: string, instrument_selection_ref: {instrument_id: string, venue_id: string, listing_id: string}, required: true, description: "chỉ có mặt khi view_state = VALID"}   # v0.3, đóng C3-DELTA-MAJ-01
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  pending_correction_class: {type: enum, values: [AWAITING_SAME_SUBJECT_REPLACEMENT, TERMINAL_SCOPE_INVALIDATION], required: false}
  current_status: {type: enum, values: [ACTIVE, PAUSED, RETIRED], required: false, description: "chỉ có mặt khi view_state = VALID"}
  display_name: {type: string, required: false}
  last_recorded_time: timestamp
queries: [GetCurrentStrategyInstance, GetStrategyInstanceHistory]
```

### 9a. Computation eligibility — unified rule (v0.2, đóng `C3-MAJ-02`/`C3-MAJ-03`/`C3-MAJ-04`/`C3-MIN-02`)

**Vai trò:** MỘT rule normative, derived, deterministic, đánh giá TẠI cùng computation cursor mà Package 0.2-C4 (Trade Intent/Decision, chưa author) đang dùng — trả lời câu hỏi "Strategy Instance này có đủ điều kiện sinh computation MỚI hay không". Rule này thuộc **Strategy eligibility ONLY** — strategy.md KHÔNG author Trade Intent/Decision/Risk/Execution behavior; strategy.md chỉ PIN định nghĩa deterministic, KHÔNG tự enforce (chưa có consumer nào tồn tại, đúng nguyên tắc §7).

**Definition Version validity (đóng `C3-MAJ-02`):** computation MỚI chỉ eligible khi `GetStrategyDefinitionVersionValidity(strategy_definition_version_ref, cursor)` (§4) trả về `VALID` — KHÔNG `TERMINALLY_INVALID`. Khi invalidation của Definition Version trở nên visible tại một cursor sau này:
- computation MỚI bị cấm từ cursor đó trở đi;
- Strategy Instance's `current_status`/state_machine (§5) **KHÔNG tự động** chuyển PAUSED/RETIRED — không có cascade tự động nào giữa `StrategyDefinitionVersionFactInvalidated` và Instance lifecycle;
- computation lịch sử đã tính TRƯỚC invalidation cursor giữ nguyên authoritative, không bị ảnh hưởng (append-only, đúng nguyên tắc "lifecycle transitions must never invalidate already-computed Decision evidence", Chapter 9 §9.3);
- Definition Version đã sửa (Version mới đăng ký qua `StrategyDefinitionVersionRegistered`, §3) **PHẢI** dùng cho một `strategy_instance_id` MỚI — `strategy_definition_version_ref` là scope bất biến trên Instance (§5), KHÔNG thể rebind tại chỗ, đúng "immutable Instance binding" đã preserve.

**Account eligibility (đóng `C3-MAJ-03`):** computation MỚI chỉ eligible khi Account (resolve qua `account_id`, `account.md` §3–§6, reconstruct authoritative TẠI cùng cursor) có `current_status = ACTIVE`. Khi Account là `SUSPENDED` hoặc `CLOSED` tại cursor:
- computation MỚI bị cấm;
- Strategy Instance lifecycle (§5 state_machine) **KHÔNG tự động** mutate — không có cascade tự động nào giữa Account status và Instance status;
- historical evidence (computation đã tính trước đó) giữ nguyên, không bị ảnh hưởng;
- **strategy.md KHÔNG author** Order/Position/recovery behavior nào cho tình huống này — đây thuộc phạm vi Package 0.2-C4–C7 (chưa author) hoàn toàn.

`environment` (§10) **VẪN LUÔN** resolve từ Account (`account.md` §1, bất biến) TẠI cùng cursor — bất kể Account `ACTIVE`/`SUSPENDED`/`CLOSED`; đây KHÔNG phải một điều kiện có thể "fail" độc lập (environment luôn resolve được vì bất biến), liệt kê trong rule dưới đây chỉ để tường minh đầy đủ chuỗi resolve.

**Evidence-reference resolvability (đóng `C3-MAJ-04`):** cả bốn trục evidence (`strategy_definition_version_ref`/`plugin_version_ref`/`configuration_version_ref`/`package_build_artifact_ref`, §5/§11) PHẢI persistently resolvable TẠI computation cursor (Chapter 8 §8.1.1 mục 4). Nếu BẤT KỲ trục nào KHÔNG resolvable tại cursor đó:
- computation MỚI deterministically ineligible;
- KHÔNG mutable-latest, KHÔNG inferred fallback, KHÔNG proxy reference nào được dùng để "vá" một tham chiếu không resolve được (tái khẳng định §11 no-proxy);
- Strategy Instance **KHÔNG bị mutate**;
- historical evidence đã tính trước đó giữ nguyên authoritative, không bị ảnh hưởng.

`strategy.md` KHÔNG thiết kế registry/retention infrastructure, artifact registry implementation, hay recovery mechanism cho tình huống unresolvable này — Phase 1/Chapter 9 registry concern (§14), ở đây chỉ pin RULE.

**Instrument selection eligibility:** `instrument_selection_ref` (§5) PHẢI resolve đúng MỘT TradableListing hợp lệ VÀ eligible TẠI cursor — "eligible" tái sử dụng đúng khái niệm `eligibility_state` đã pin tại `instrument.md` §15 (`ELIGIBLE` khi Instrument VÀ Venue của listing đó CHƯA `RETIRED`; `INELIGIBLE_PARENT_STATE` khi ngược lại), KHÔNG fabricate một authoritative event mới.

**Unified rule (đóng `C3-MIN-02`) — đánh giá tại computation cursor C, sáu điều kiện, AND-conjunction:**

```text
eligible_for_new_computation(strategy_instance_id, C) =
      StrategyInstance.current_status(C)  ==  ACTIVE                                    (§5/§7, visible-valid-head fold TẠI C)
  AND GetStrategyDefinitionVersionValidity(strategy_definition_version_ref, C)  ==  VALID  (§4)
  AND Account.current_status(C)  ==  ACTIVE                                              (account.md §3–§7, reconstruct TẠI C)
  AND Account.environment resolve nhất quán TẠI C                                        (account.md §1, bất biến — luôn true khi Account tồn tại)
  AND plugin_version_ref, configuration_version_ref, package_build_artifact_ref,
      strategy_definition_version_ref  ĐỀU persistently resolvable TẠI C                 (Chapter 8 §8.1.1 mục 4)
  AND instrument_selection_ref resolve đúng MỘT TradableListing eligibility_state == ELIGIBLE TẠI C   (instrument.md §15)
```

Mọi thành phần bên phải PHẢI reconstruct từ authoritative event stream tương ứng TẠI CÙNG cursor C — KHÔNG dùng bất kỳ Current View latest-state nào (`StrategyInstanceCurrentView` §9, `AccountCurrentView` account.md §7, `InstrumentCurrentView`/`VenueCurrentView`/`TradableListingCurrentView` instrument.md §7/§15) làm input trực tiếp cho quyết định eligibility, trừ khi cursor-addressable VÀ provably equivalent (cùng ngoại lệ cache đã pin tại §9/§10/account.md §13). **Convenience query non-authoritative** (nếu implementation cần): `GetStrategyInstanceComputationEligibility(strategy_instance_id, cursor) → ELIGIBLE | INELIGIBLE` — CHỈ query/UI, KHÔNG BAO GIỜ là input cho computation khác, cùng nguyên tắc §9.

**Rule này thuộc Strategy eligibility ONLY** — canonical policy identifier `computation_eligibility_policy: ALL_CONDITIONS_TRUE_AT_SAME_CURSOR` (§12). C4 (Trade Intent/Decision, chưa author) chịu trách nhiệm CONSUME rule này khi quyết định có tạo Trade Intent/Decision mới hay không; `strategy.md` KHÔNG author Trade Intent/Decision/Risk/Execution behavior nào, KHÔNG tự enforce rule (chưa có consumer tồn tại).

## 10. Downstream reference contract (cho Package 0.2-C4)

Package sau (Trade Intent, Decision — Package 0.2-C4, chưa author) tham chiếu Strategy qua ĐÚNG chín field, KHÔNG hơn:

```yaml
strategy_instance_id: {type: string, required: true, ref: strategy}
strategy_definition_id: {type: string, description: "resolve qua strategy_definition_version_ref → StrategyDefinitionVersionRegistered.strategy_definition_id"}
strategy_definition_version_id: {type: string, description: "= strategy_definition_version_ref của Instance (§5) — exact immutable pin, KHÔNG BAO GIỜ 'latest' (ADR-013 §2.3)"}
plugin_version_ref: {type: string, description: "trục 2/4, xem §5"}
configuration_version_ref: {type: string, description: "trục 3/4, xem §5"}
package_build_artifact_ref: {type: string, description: "trục 4/4, xem §5"}
account_id: {type: string, ref: account, description: "đúng một Account, xem §5"}
environment: {type: enum, values: [PAPER, LIVE], description: "resolve qua account_id → Account event stream TẠI cursor — KHÔNG lưu riêng trên Strategy Instance, KHÔNG dùng AccountCurrentView làm input (account.md §13)"}
instrument_selection_ref:
  type: object
  required: true
  description: "thuộc Instance (§5), TUYỆT ĐỐI KHÔNG thuộc Configuration Version — v0.3 (đóng C3-DELTA-MAJ-01): C4 PHẢI tiêu thụ object này TRỰC TIẾP — KHÔNG serialize thành string, KHÔNG dùng opaque proxy ID, KHÔNG dùng tagged reference thay thế, KHÔNG mở rộng thành Selection aggregate hay multi-instrument cardinality"
  fields:
    instrument_id: {type: string, required: true}
    venue_id: {type: string, required: true}
    listing_id: {type: string, required: true}
```

**Downstream authority rule — MỘT quy tắc duy nhất, không ngoại lệ (đúng pattern account.md §13, đóng trước lớp lỗi `C2-MAJ-04`-style):** downstream package PHẢI resolve mọi field trên TRỰC TIẾP từ authoritative event stream (Strategy Instance §6–§8; Strategy Definition Version §3; Account, `account.md` §3–§6) TẠI ĐÚNG recorded/effective cursor mà chính computation đó đang dùng. `StrategyInstanceCurrentView` latest-state (§9) KHÔNG BAO GIỜ được dùng làm input. Vi phạm điển hình cần tránh: dùng row "mới nhất" cho một historical replay ở cursor cũ hơn (look-ahead, CẤM tuyệt đối). KHÔNG package nào được tự phát minh identity/version semantics khác — chín field trên là nguồn định nghĩa DUY NHẤT tại đây.

**strategy.md KHÔNG author** bất kỳ semantic nào của Trade Intent/Decision — Package 0.2-C4 (chưa authorize) tự định nghĩa cách nó dùng chín field trên; strategy.md chỉ đảm bảo chín field này tồn tại, ổn định, và resolve được đúng. **C4 PHẢI áp dụng unified computation-eligibility rule (§9a, v0.2) trước khi tạo Trade Intent/Decision mới** dựa trên chín field này — `strategy.md` chỉ định nghĩa rule, KHÔNG tự enforce.

## 11. Bốn-trục độc lập (ADR-013 conformance)

**`strategy_evidence_axis_policy: FOUR_INDEPENDENT_AXES_NO_PROXY`** (§12) — đúng ADR-013 §2.1/§2.4, bốn trục evidence KHÔNG được gộp, KHÔNG trục nào proxy trục khác:

| Trục | Sở hữu bởi | Field | Bump độc lập |
|---|---|---|---|
| Strategy Definition Version | `strategy.md` (§1, Domain Contract này) | `strategy_definition_version_ref` | Thesis/decision-rule/scope/input/explanation đổi (§1) |
| Plugin Version | [Chapter 9 §9.1](../constitution/09-plugin-model.md) (Locked) | `plugin_version_ref` | Implementation-release đổi — độc lập business semantics |
| Configuration Version | [Chapter 9 §9.1](../constitution/09-plugin-model.md) (Locked) | `configuration_version_ref` | Parameter tuning đổi — độc lập code/business semantics |
| Package/Build Artifact | [Chapter 9 §9.1](../constitution/09-plugin-model.md) (Locked)/ADR-013 §2.5 | `package_build_artifact_ref` | Executable bytes đổi (kể cả rebuild "giống hệt" cho bytes khác — non-reproducible build) |

**Cấm tuyệt đối (đóng yêu cầu "no axis may proxy another"):** derive `plugin_version_ref` từ `configuration_version_ref` hay ngược lại; dùng `strategy_definition_version_ref` làm proxy cho implementation identity; dùng Plugin Version hay source commit hash làm proxy cho `package_build_artifact_ref` (ADR-013 §2.5, Chapter 9 §9.5 "mixed-build activation is integrity violation"). Mỗi trục bump ĐỘC LẬP — refactor Plugin không bắt buộc Strategy Definition Version mới; đổi thesis không bắt buộc Plugin Version mới (ADR-013 §2.1).

**Referenced Authoritative Artifact (Chapter 8 §8.1.1):** cả bốn trục PHẢI thỏa 5 điều kiện chung — versioned; immutable sau khi tham chiếu; không tái dùng identifier; persistently resolvable trong replay/audit horizon; verifiable content identity. `strategy.md` chỉ pin field/reference — Plugin Version/Configuration Version/Package-Build-Artifact's chính schema/lifecycle thuộc Chapter 9/registry tương ứng (deferred, §14), `strategy_definition_version_ref` thuộc chính Domain Contract này (§1).

**Hệ quả computation eligibility (v0.2, đóng `C3-MAJ-04`):** nếu bất kỳ trục nào trong bốn trục KHÔNG persistently resolvable tại computation cursor (vi phạm Chapter 8 §8.1.1 mục 4) → computation MỚI deterministically **INELIGIBLE** (§9a) — KHÔNG mutable-latest, KHÔNG inferred fallback, KHÔNG proxy reference nào được dùng để "vá" một tham chiếu không resolve được. Strategy Instance KHÔNG bị mutate; historical evidence đã tính trước đó giữ nguyên authoritative, không bị ảnh hưởng. `strategy.md` KHÔNG thiết kế registry/retention infrastructure hay recovery mechanism cho tình huống này (Phase 1, §14) — ở đây chỉ pin RULE.

## 12. Canonical policy identifiers — nguồn duy nhất (context `strategy-definition`)

**Ba canonical policy identifier, khai báo ĐÚNG MỘT LẦN tại đây cho context `strategy-definition`** — cùng pattern đã proven tại `instrument.md`/`venue.md`/`account.md`, khai báo ĐỘC LẬP vì đây là context khác, tránh cross-context coupling không cần thiết:

```yaml
initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS
strategy_evidence_axis_policy: FOUR_INDEPENDENT_AXES_NO_PROXY
computation_eligibility_policy: ALL_CONDITIONS_TRUE_AT_SAME_CURSOR   # v0.2, đóng C3-MIN-02
```

**`initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS`** — áp dụng cho `StrategyDefinitionVersionRegistered` (§3/§4) và `StrategyInstanceRegistered` (§6/§8): TOÀN BỘ payload của hai event này là scope bất biến (không có "mutable metadata" tách biệt như Account/Venue/Instrument) — correction LUÔN LUÔN nghĩa là đăng ký một ID MỚI hoàn toàn, KHÔNG BAO GIỜ same-ID replacement (khác `initial_fact_correction_policy: INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES` của `instrument.md`/`account.md`, vốn có METADATA_ERROR same-subject path vì các subject đó có mutable metadata riêng). `StrategyInstanceStatusChanged` (§7/§8) KHÔNG thuộc policy này — nó dùng correction lineage chuẩn (same-slice replacement, §9), đúng pattern đã proven.

**`strategy_evidence_axis_policy: FOUR_INDEPENDENT_AXES_NO_PROXY`** — xem §11 cho định nghĩa đầy đủ.

**`computation_eligibility_policy: ALL_CONDITIONS_TRUE_AT_SAME_CURSOR`** (v0.2, đóng `C3-MIN-02`) — sáu điều kiện của `eligible_for_new_computation` (§9a) PHẢI ĐỀU true, đánh giá TẠI CÙNG MỘT computation cursor — không có điều kiện nào đánh giá tại cursor khác cursor còn lại (cấm "mix cursor"); xem §9a cho định nghĩa đầy đủ.

## 13. Correction lineage (cả hai subject)

Correction lineage scoped chính xác theo `(subject_id, effective_time)` — mỗi effective_time-slice có chuỗi lineage RIÊNG, cùng nguyên tắc đã khóa xuyên suốt `instrument.md`/`venue.md`/`account.md`.

**`StrategyDefinitionVersionRegistered`/`StrategyInstanceRegistered` — invalidate-only, KHÔNG replacement (§3/§4, §6/§8):**

```text
F1 (StrategyDefinitionVersionRegistered hoặc StrategyInstanceRegistered)
  → *FactInvalidated targeting F1
  → KHÔNG có replacement dưới cùng ID — correction thực tế là đăng ký một ID MỚI HOÀN TOÀN,
    độc lập, KHÔNG supersedes_fact_ref trỏ về F1
```

**`StrategyInstanceStatusChanged` — correction lineage chuẩn, same-slice replacement (§7/§8):**

```text
F1 (StrategyInstanceStatusChanged)
  → StrategyInstanceFactInvalidated targeting F1
  → replacement (cùng event type StrategyInstanceStatusChanged), supersedes_fact_ref = F1

Correction tiếp theo:
F2
  → StrategyInstanceFactInvalidated targeting F2
  → F3, supersedes_fact_ref = F2   (KHÔNG được supersedes_fact_ref = F1 — cấm nhảy cóc)
```

**Mười invariant bắt buộc cho họ `StrategyInstanceStatusChanged`** (đã pin tại §7/§8, tổng hợp lại đây):

1. Original fact (`StrategyInstanceStatusChanged` forward transition, KHÔNG có supersedes_fact_ref) không có `supersedes_fact_ref`.
2. Replacement fact (correction) bắt buộc có `supersedes_fact_ref`.
3. Replacement dùng đúng cùng subject và cùng `effective_time` với fact bị supersede.
4. Replacement PHẢI supersede đúng lineage head hiện tại.
5. Replacement không được nhảy cóc qua một head trung gian.
6. Một fact bị invalidate có **tối đa một** replacement authoritative trực tiếp — cấm fork.
7. Replacement không được "visible" (`recorded_time`) trước invalidation tương ứng.
8. Mọi lineage member lịch sử giữ nguyên trong log — append-only (I-3), không mutate.
9. Một fact đã invalidate **không bao giờ** bị tái sử dụng ngầm — Current View (§9) phải loại trừ nó tường minh.
10. **RETIRED (forward transition) KHÔNG BAO GIỜ dùng cơ chế correction để "mở lại" như một hành động nghiệp vụ mới** — chỉ correction thực sự (sửa sai sót ghi nhận trong quá khứ) mới dùng `StrategyInstanceFactInvalidated` + replacement; không có "reactivation" command riêng.

## 14. Ngoài phạm vi — defer

**Deferred tường minh, không author ở C3 (Phase 1 implementation concern, non-blocking):**

- Schema/versioning scheme cụ thể (SemVer, monotonic, content-hash) cho Plugin Version/Configuration Version/Package-Build-Artifact — đúng ADR-013 §6 "Thuộc Domain Contract, KHÔNG thuộc ADR này."
- Multi-instrument set, universe, và dynamic selection (nhiều listing cho một Instance, hoặc selection thay đổi theo thời gian) — v0.2 chỉ pin single-listing cardinality, shape `{instrument_id, venue_id, listing_id}` (§5, đóng `C3-MAJ-01`); mở rộng multi-instrument vẫn deferred, C4/Configuration Domain Contract tương lai quyết. KHÔNG tạo Selection aggregate.
- Xác minh tự động `instrument_selection_ref` nằm trong `supported_scope` của Definition Version — Phase 1/C4 concern, ở đây chỉ pin RULE.
- Registry/retention infrastructure cụ thể đảm bảo persistent resolvability của bốn trục evidence (artifact store, retention/archive policy, registry implementation) — Phase 1/Chapter 9 registry concern; `strategy.md` chỉ pin RULE hệ quả khi unresolvable (§9a/§11, đóng `C3-MAJ-04`), KHÔNG thiết kế MECHANISM.
- Runtime worker ownership, transaction boundaries, retry/backoff, monitoring/escalation, operational recovery orchestration (Phase 1, cùng nguyên tắc defer đã áp dụng cho `instrument.md`/`account.md`).
- Broker/parity-validation gate trước khi một Strategy Definition Version hay Instance được dùng cho Live — chạm nhưng KHÔNG quyết OQ-002 (Strategy Lifecycle Live-gate), để ngỏ đúng tinh thần Chapter 9 §9.10 (không đóng ngầm OQ-002).
- `display_name` revision mechanism cho Strategy Instance (§5) — minimal ở v0.1, không có PATCH event riêng.
- Strategy DSL/executable code, optimizer/backtest engine, capital allocation/multi-strategy arbitration, Live activation workflow — hoàn toàn ngoài phạm vi Domain Contract.
- Trade Intent/Decision/Risk/Execution Intent/Order/Fill/Position/Replay Event semantics (Package 0.2-C4–C7, chưa authorize).

## 15. Prohibitions

**Strategy Definition Version KHÔNG được sở hữu:** Plugin Definition/Plugin Version identity (Chapter 9 §9.1, riêng biệt); Configuration Version content; Package/Build Artifact identity; Account/environment; Trade Intent/Decision/Risk/Execution/Order/Fill/Position semantics.

**Strategy Instance KHÔNG được sở hữu:** raw exchange credential (thuộc Account, `account.md` §10); business/decision semantics (thuộc Definition Version, §1); Trade Intent/Decision/Risk/Execution/Order/Fill/Position semantics; capital allocation/multi-strategy arbitration logic; module-registry entry (Chapter 9 §9.1: Strategy Instance KHÔNG BAO GIỜ tạo `module-registry` entry mới).

## 16. Open questions ngoài phạm vi

- Cơ chế cụ thể generate `strategy_definition_version_id`/`strategy_instance_id` (UUID, content-hash, sequential) — chưa quyết, Phase 1/requester-side concern, cùng nguyên tắc defer đã áp dụng cho `instrument_id`/`account_id`.
- Retention/resolvability horizon cụ thể cho Strategy Instance đã RETIRED (Chapter 9 §9.3 yêu cầu khai báo horizon tường minh) — chưa pin ở v0.1, cần quyết định khi Package 0.2-C có nhu cầu thực tế đầu tiên.
- Liệu một Strategy Definition Version bump có cần qua review/approval gate riêng trước khi dùng cho Live — chạm nhưng KHÔNG quyết OQ-002, để ngỏ đúng ADR-013 §9.
- Không đóng OQ-002/OQ-003.
