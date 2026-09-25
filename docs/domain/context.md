---
id: context
title: Market Context
version: "0.4"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-07-29"
last_review: null
next_review: null
---

# Market Context

> **Vai trò của tài liệu này:** Domain Contract của Package 0.2-B4 — điểm hội tụ **deterministic, có kiểm soát** của `Structure + Raw Regime + Feature` thành một market-state snapshot duy nhất, đúng ranh giới `context-projection` đã forward-declare từ Package 0.2-A tại [`context-map.yaml`](./context-map.yaml) (nay chuyển forward-declared → authored). Draft, chưa Approved/Locked. Thuộc capability `context-aggregation` / context `context-projection`. **Phạm vi B4 là scope tối thiểu** — đúng một Context type (`market_context`), không phải một rule engine tổng quát.
>
> **Quan hệ với [ADR-003](../adr/ADR-003.md):** ADR-003 (Approved, 2026-07-16) khóa Raw Regime độc lập hoàn toàn với Structure, và nguyên văn mô tả Feature Engine là "điểm fan-in duy nhất" giữa Structure và Regime. Văn bản đó, đọc theo nghĩa đen, KHÔNG tường minh phân biệt "Feature computation fan-in" (Feature Engine tự tính giá trị) với "Context snapshot aggregation" (Context chỉ chọn as-of và sao chép fact có sẵn) — đây là gốc rễ `IRB-B4-MAJ-03` (§ xem CHANGELOG; sửa từ tham chiếu cũ sai `RA-B4-MAJ-01`/`IRB-B4-MAJ-01` — đóng `IRB-ADR014-MIN-01`, traceability-only). ADR-003 **Approved và immutable byte-for-byte** ([Chapter 11 §11.3](../constitution/11-adr-process.md)) — không được sửa trực tiếp, và embedded document status của chính `ADR-003.md` vẫn `Approved` vĩnh viễn. [ADR-014](../adr/ADR-014.md) đề xuất narrow amendment (supersede có kiểm soát) phân biệt tường minh hai fan-in operation này, giữ nguyên toàn bộ quyết định độc lập Regime/Structure của ADR-003 — **Product Owner đã approve ADR-014 ngày 2026-07-30** (sau ChatGPT + Claude narrow delta review Clean), `supersedes: [ADR-003]` nay có hiệu lực, MANIFEST ghi nhận ADR-003 chuyển `Superseded` ở current authoritative lifecycle state (embedded document status không đổi). **ADR-014 nay là controlling authority** cho ranh giới Feature computation fan-in vs Context snapshot aggregation — `context.md` v0.2 author đúng theo thiết kế này (khác biệt với Feature computation fan-in, xem §17). Approval ADR-014 KHÔNG tự động Approve/Lock/Consolidate Package 0.2-B4 — B4 vẫn `status: Draft`, architecture blocker (`IRB-B4-MAJ-03`) đã governance-resolved nhưng B4 còn cần package delta review/consolidation transaction riêng trước khi `Consolidated Stable`.

Market Context **KHÔNG phải** trade signal, entry/exit recommendation, setup score, strategy selection, Risk/Account/Position/Execution state, hay bất kỳ business decision nào. Nó là một **snapshot authoritative, deterministic, atomic** của các fact phân tích đã tồn tại (Structure orientation, hai Regime dimension, ba Feature value), theo một Context Definition đã pin — không tự diễn giải thêm ý nghĩa nào ngoài những gì upstream fact đã tuyên bố.

Market Context bao gồm **bốn concept riêng biệt**:

1. **Logical Market Context Subject** (`kind: entity`) — identity ổn định của "chuỗi snapshot theo một context type + definition version này", một subject liên tục theo scope (giống `regime.md`/`feature.md` — không có subject mới per computation point).
2. **`MarketContextSnapshot`** (`kind: event`) — fact authoritative cho MỘT completed valid computation point — dùng cho cả original computation lẫn correction replacement.
3. **`MarketContextFactInvalidated`** (`kind: event`) — phủ định MỘT `MarketContextSnapshot` lịch sử cụ thể, KHÔNG tự nó tuyên bố giá trị mới.

Cộng một **read model tùy chọn** (`MarketContextCurrentView`) — projection tiện dụng, không authoritative.

**`market-context-snapshot` / `market-context-fact-invalidated` / `market-context-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây, và đúng giá trị `contract_id` mà [`context-map.yaml`](./context-map.yaml) sẽ trích dẫn. Display name, concept ID, và `event_type` là ba đại lượng khác nhau, không cạnh tranh identity — cùng nguyên tắc `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md` đã khóa.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá ở `structure.md`/`regime.md`/`feature.md`:** envelope binding cho `MarketContextFactInvalidated` (`subject_ref`/`effective_time` kế thừa từ fact bị invalidate, không tự khai báo độc lập); `normalized_input_fact_refs` là tập toán học, normalize theo lexicographic order trước khi tính identity/hash/dedup; `MarketContextCurrentView` no-row semantics trước fact đầu tiên, `view_state` chỉ có `VALID`/`PENDING_CORRECTION`, không có `UNAVAILABLE`; mọi canonical policy identifier chỉ khai báo ĐÚNG MỘT NƠI; **effective-time eligibility là một filter độc lập chạy TRƯỚC candidate ordering** (bài học `feature.md` v0.2, `RA-B3-MAJ-01`/`IRB-B3-MAJ-01`) — áp dụng cho cả sáu upstream role của Context, không chỉ một.

**v0.2 xử lý `RA-B4-MAJ-01`/`IRB-B4-MAJ-01`/`IRB-B4-MAJ-02`/`IRB-B4-MAJ-03`:** (a) `RA-B4-MAJ-01`/`IRB-B4-MAJ-01` — cùng một algorithmic defect: Eligible Upstream Fact selection v0.1 (§8) có một bước filter (Currency) tham chiếu NGƯỢC tới một bước sau nó (Not-invalidated) — vi phạm nguyên tắc "không bước nào được tham chiếu kết quả của bước sau"; viết lại thành hai phase tách bạch: Phase 1 (eligibility filtering, mỗi candidate tự đủ điều kiện độc lập) rồi Phase 2 (role-specific current selection, CHỈ chạy trên tập survivor của Phase 1) — không còn tham chiếu ngược (§8). (b) `IRB-B4-MAJ-02` — `missing_input_policy` (§6) là một chuỗi tự do, không pin giá trị canonical; đổi thành enum đóng, đúng một giá trị hợp lệ `NO_SNAPSHOT_WHEN_ANY_REQUIRED_ROLE_MISSING_OR_PENDING` (§6, §9) — **missing_input_policy correction closes `IRB-B4-MAJ-02`.** (c) `IRB-B4-MAJ-03` — xung đột kiến trúc với văn bản gốc ADR-003 ("Feature Engine là điểm fan-in duy nhất"); xử lý qua [ADR-014](../adr/ADR-014.md) narrow amendment — **`IRB-B4-MAJ-03` governance-resolved** kể từ khi Product Owner approve ADR-014 ngày 2026-07-30 (xem khối đầu tài liệu). Đồng thời làm rõ tường minh target-window tie-break tại `MarketContextCurrentView` (§13, non-blocking cleanup).

**Narrow traceability correction (`RA-B4-MIN-02`, không đổi version):** commit trước (`f1ea03b`) từng gán nhầm `IRB-B4-MAJ-02` cho ADR-003 conflict và `IRB-B4-MAJ-03` cho `missing_input_policy` — NGƯỢC với mapping authoritative của Independent Review B report. Đã sửa toàn bộ reference trong tài liệu này: `IRB-B4-MAJ-02` = `missing_input_policy` (resolved technically, đóng); `IRB-B4-MAJ-03` = ADR-003 fan-in authority conflict (**governance-resolved** — ADR-014 Approved bởi Product Owner ngày 2026-07-30, xem khối đầu tài liệu). Đây là metadata/reference-only correction — không đổi bất kỳ semantic/algorithm/enum/event/identity/lineage/relationship nào; `context.md` giữ nguyên `version: "0.2"`.

**v0.3 — triển khai [ADR-046](../adr/ADR-046.md) (Approved, `v0.5`, immutable, 2026-09-25) — Context Computation Cursor and Temporal Eligible-Upstream Supersession.** `ADR-046` là kiến trúc authority DUY NHẤT cho amendment này; v0.3 là **transcription có kiểm soát** của quyết định đã Approved — KHÔNG một quyết định kiến trúc mới, KHÔNG tự phát sinh bất kỳ semantic choice nào `ADR-046`/authority hiện tại chưa resolve. Nội dung chính:

- **`computation_cursor`** — canonical [Chapter 8 §8.5](../constitution/08-event-model.md) Replay Cursor, tái sử dụng NGUYÊN VẸN (KHÔNG một schema local cạnh tranh) — BẮT BUỘC trên MỌI `MarketContextSnapshot` (§3, cả original lẫn correction replacement — mỗi fact tự pin cursor CHÍNH nó, KHÔNG kế thừa) VÀ MỌI `MarketContextFactInvalidated` (§4, cursor này là `R_later`, boundary chứng minh invalidation).
- **`Cursor → Context projection record`** anti-look-ahead relation: `computation_cursor.recorded_time <= envelope.recorded_time` — fail-closed khi vi phạm, KHÔNG clamp timestamp, KHÔNG substitute field này cho field kia (§3, §4).
- **Full three-leg cursor visibility** (§14) thay thế scalar `U.recorded_time <= R` cũ (§8 Phase 1 bước 2) — stream-universe membership + same-stream position + recorded-time boundary.
- **`COVERS_CONTEXT`** (§14) — bounded, Context-scoped, **partial** knowledge-coverage relation — chứng minh `K_context(R_old) ⊆ K_context(R_new)` cộng lifecycle non-regression, KHÔNG một platform-wide cursor total order, KHÔNG một thay đổi [ADR-009](../adr/ADR-009.md).
- **Universal current-lineage invalidation coverage precondition** — `R_later COVERS_CONTEXT R_original` BẮT BUỘC trước MỌI `MarketContextFactInvalidated` publish như current-valid lineage transition, bất kể trigger class (direct correction HAY temporal supersession) — §4, §14.
- **Temporal eligible-upstream role-resolution supersession** (§8) — điều kiện mới, CHỈ áp dụng sáu role phân tích non-Candle (Structure, hai Regime, ba Feature): một upstream fact later-visible có thể trở thành §8 winner mới tại `R_later`, dù ref cũ CHƯA từng bị invalidate trực tiếp. Candle vẫn loại trừ khỏi trigger này (§8).
- **Per-role minimal-complete direct-cause set** thay thế giả định cũ "đúng một cause ref mỗi role" (§4) — `affected_upstream_roles`/`causation_refs` giữ nguyên shape flat/dedup, mỗi role có thể cần MỘT HOẶC NHIỀU ref trực tiếp, đúng ba nhánh `ADR-046` Decision item 7.
- **Case A / Case B replacement behavior** (§12) — Case A tái sử dụng CHÍNH XÁC kết quả §8 đã có tại `R_later`; Case B yêu cầu `R_replacement COVERS_CONTEXT R_later` cộng rerun §8 độc lập tại `R_replacement`, KHÔNG BAO GIỜ tái sử dụng kết quả `R_later` đã cache.
- **Context-scoped Input Contract VẪN CHƯA authored** (§16, §21) — schema semantic được định nghĩa từ v0.3, nhưng publication một Context projection record như durable evidence dưới cơ chế này VẪN fail-closed cho tới khi referenced artifact (Input Contract, Stream Registry version, lifecycle frontier, upstream Event Contract dependency authority) genuinely resolve, persistently.
- **Runtime/publication VẪN CHƯA enable** — `python/context-aggregator/**` KHÔNG bị sửa bởi amendment này (vẫn `REVIEW A VALIDATED — CLEAN`); Context Event Contract/output stream KHÔNG được mint ở v0.3 này (§21).

Fresh ADR Scope Gate cho CHÍNH amendment v0.3 này: **`ADR_NOT_REQUIRED`** — transcription thuần túy của architecture authority đã Approved, không semantic choice độc lập nào được author ở đây. Risk Classification/Review A cho v0.3 candidate này **CHƯA thực hiện**, không tự finalize bởi transaction này — `context.md` giữ nguyên `status: Draft`.

**Authority-neutral clarification (`ADR-046`, v0.3) — KHÔNG resolve terminology tension đã tồn tại.** `ADR-046` (Approved) tường minh KHÔNG đổi `module_type: projection`/`owns_authoritative_state: false` (`module-registry.yaml`, fresh-verified byte-unchanged) và KHÔNG resolve terminology tension đã preserve giữa văn bản legacy của CHÍNH tài liệu này (ví dụ §17's "Context là một authoritative market-state snapshot") và phân loại Type-2 Projection của [Chapter 7 §7.4](../constitution/07-module-taxonomy.md). `computation_cursor`/durable cursor evidence mà v0.3 thêm vào CHỈ cấp **record-integrity và replay-boundary evidence** — KHÔNG biến Context thành nguồn authoritative cho Candle/Structure/Regime/Feature/Strategy/Decision/Risk hay bất kỳ domain concept nào khác ngoài chính những gì Context tự aggregate. Terminology tension này VẪN preserve, chưa resolve, và amendment v0.3 này KHÔNG âm thầm quyết định nó — bất kỳ rewrite thuật ngữ legacy nào (ví dụ §17) đòi hỏi một transaction riêng, có kiểm soát, governed rõ ràng — KHÔNG phải một side-effect của việc transcribe `ADR-046`. Prose MỚI do v0.3 thêm vào dùng thuật ngữ trung lập **"Context projection record"** khi cần mô tả `MarketContextSnapshot`/`MarketContextFactInvalidated`; văn bản lịch sử KHÔNG bị rewrite chỉ vì lý do thuật ngữ.

**v0.4 — bounded correction of v0.3 against fresh ChatGPT Review A (`CONTEXT-DOMAIN-ADR046-AMEND-001-CORR-001`)**, addressed/remediated pending fresh Review A re-review (not self-closed by the correction executor — closure is a Review A re-review determination, never asserted here): ChatGPT Review A (`AI Technical Architect`) reviewed v0.3 (reviewed boundary `3d52c286b35c05ed1cf7cdc8055cfb3e2d96128b`, reviewed blob `c2ba2360f09c5b9a6cbec1a582a26ee1d1e40de1`) and returned **`REVISION_REQUIRED — 0 Blocker / 2 Major / 0 Minor`**, Risk `R2`, ADR Scope `ADR_NOT_REQUIRED`. This v0.4 addresses: `CONTEXT-DC-A-MAJ-01` (§14's full-cursor-visibility predicate — and its global "every 'visible' in §4/§8/§12/§13/§15" equivalence — was incorrectly globalized to also govern visibility of Context's own OUTPUT records (`MarketContextSnapshot`/`MarketContextFactInvalidated`/replacement/`MarketContextCurrentView` traversal), when `ADR-046` Decision item 4 only defines visibility for an UPSTREAM event at a Context `computation_cursor` — corrected: §14's predicate narrowed explicitly to upstream input/correction-lineage/temporal-supersession/`K_context`/`COVERS_CONTEXT` use only, §8's duplicate global claim narrowed to its own actual §8-step-4 upstream usage, §12 gains a one-sentence clarification distinguishing upstream-state visibility during rerun from output-record visibility, §13 gains an explicit output-history-visibility boundary statement — no new output cursor schema/stream/Event Contract authored, all target-window/lineage/`PENDING_CORRECTION`/no-fallback semantics preserved — §15 gains a distinguishing bullet separating historical input reconstruction from output-record visibility); `CONTEXT-DC-A-MAJ-02` (§4's compound causation branch (c) was described as "(a) cộng (b)," internally contradicting the correctly-stated `{B, I_B}` example already present in the same invariant, since `I_B` targets `B` — not necessarily `C`'s old cited ref `A` — corrected: branch (c) redefined as a genuine compound role-state transition whose cause set contains exactly and only the direct causal predecessors/prerequisites required to prove the new role-resolution state, regardless of whether each element targets an old or new ref; `affected_upstream_roles`/flat `causation_refs`/`invalidated_fact_ref`/one-or-more-refs-per-role/deterministic attribution/no new payload field/no generic `context_changed` cause/Chapter 6 §6.7 direct-causality requirement/coverage-vs-causation separation all preserved unchanged). **No change to any other ADR-046 semantic** — `computation_cursor` requirement, the anti-look-ahead relation, full three-leg UPSTREAM visibility, `COVERS_CONTEXT`, its six proof conditions, the universal invalidation coverage precondition, temporal supersession, Candle exclusion, Case A, Case B, the coverage chain, `computation_cursor` excluded from computation identity, the fail-closed referenced-artifact boundary, and authority-neutral framing all preserved unchanged. This v0.4 candidate still requires a fresh Review A before further routing; **not self-reviewed, not self-approved**, and no Product Owner decision is requested or recorded by this transaction. `CONTEXT-DC-A-MAJ-01`/`CONTEXT-DC-A-MAJ-02`: **addressed/remediated pending fresh Review A re-review** — not self-closed.

## 1. Logical Market Context Subject — `kind: entity`

```yaml
id: context
kind: entity
capability_id: context-aggregation
domain_context_id: context-projection
description: >
  Chuỗi snapshot authoritative liên tục cho MỘT context_type theo MỘT Context Definition
  Version cụ thể, tại một instrument/venue/timeframe. Subject có identity LOGIC ổn định
  (`context_subject_id`, năm field, KHÔNG bao gồm effective window/point) — cùng pattern
  `regime.md` §1 / `feature.md` §1 đã khóa. Effective window/point KHÔNG phải một trục
  identity: nó định danh MỘT fact cụ thể trong chuỗi fact của subject này (§3).
invariants:
  - "context_subject_id resolve deterministic từ ĐÚNG NĂM field qualifying scope: instrument_id, venue_id, timeframe, context_type, context_definition_version — cùng năm-field-scope luôn cho cùng context_subject_id; khác bất kỳ field nào cho context_subject_id KHÁC. context_subject_id bất biến, KHÔNG tái sử dụng cho một subject khác (Chapter 6 §6.1)."
  - "context_subject_id là opaque — domain logic KHÔNG được parse nó (Chapter 6 §6.8); mọi quyết định nghiệp vụ phải dùng field tường minh trong scope."
  - "instrument_id, venue_id, timeframe, context_type, context_definition_version bất biến sau khi subject được quan sát lần đầu — đổi bất kỳ field nào tạo ra một subject KHÁC, không phải mutate subject cũ. Đổi context_definition_version tạo subject mới hoàn toàn — chuỗi fact cũ dưới definition cũ giữ nguyên, không bị diễn giải lại (Chapter 8 §8.1.1 Referenced Authoritative Artifact)."
  - "Effective window/point (§3) KHÔNG thuộc identity scope của subject — nó là thuộc tính của từng MarketContextSnapshot fact. Hai fact khác window trên cùng subject là hai fact riêng biệt của CÙNG một subject, không phải hai subject."
  - "context_type là enum đóng ở v0.1: [market_context] — mở rộng thêm context_type khác (§21, deferred) là một thay đổi Domain Contract tường minh (bump version), không tự phát sinh ngầm. Structure/Regime/Feature value KHÔNG bao giờ được thêm vào identity scope — chỉ context_type/context_definition_version quyết định 'loại Context nào'."
schema:
  context_subject_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  instrument_id: {type: string, required: true, ref: instrument}
  venue_id: {type: string, required: true, ref: venue}
  timeframe: {type: string, required: true}
  context_type: {type: enum, values: [market_context], required: true}
  context_definition_version: {type: string, required: true, description: "pin chính xác Context Definition đã dùng — §6"}
state_machine:
  initial_state: UNCOMPUTED
  states: [UNCOMPUTED, COMPUTED]
  transitions:
    - {from: UNCOMPUTED, to: COMPUTED, caused_by: MarketContextSnapshot}
    - {from: COMPUTED, to: COMPUTED, caused_by: MarketContextSnapshot}
  terminal_states: []
events_emitted: [MarketContextSnapshot, MarketContextFactInvalidated]
events_consumed: [CandleClosed, CandleCorrected, BreakOfStructureDetected, ChangeOfCharacterDetected, StructureFactInvalidated, StructureRecomputed, RegimeClassified, RegimeFactInvalidated, FeatureComputed, FeatureFactInvalidated]
commands: []
queries: []
```

**`UNCOMPUTED` là notional initial state** — cùng convention `UNSEEN`/`UNDETERMINED`/`UNCLASSIFIED` mà `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md` đã khóa. **`COMPUTED → COMPUTED` là self-transition cho MỌI `MarketContextSnapshot` kế tiếp** — state machine chỉ mô tả "subject đã từng compute hay chưa" (existence lifecycle), KHÔNG mã hóa giá trị hiện tại — "current view" là một query (§13), không phải state lưu trữ.

## 2. Canonical event envelope — áp dụng cho mọi Context event (§3–§4)

Mọi event ở §3–§4 là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). Mục này khóa **envelope chung** một lần — từng event bên dưới chỉ khai báo **payload đặc thù**. Chapter 8 sở hữu nguyên vẹn semantic của envelope; mục này **chỉ áp dụng, không định nghĩa lại**.

```yaml
envelope:                                          # Chapter 8 §8.2.1 — cardinality nguyên văn
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2) — xem bảng dưới
  event_contract_ref: {cardinality: required}        # {contract_id, contract_version}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}             # Chapter 5 — khi Ride tính/ghi nhận fact này, KHÔNG phải effective window time
  subject_ref: {cardinality: "required — shape canonical, xem dưới. Trên MarketContextFactInvalidated (§4), PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate — không tự khai báo độc lập."}
  stream_ref: {cardinality: required}                # {stream_id, registry_version} — Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # {module_id, implementation_version, run_id} — Phase 1, chưa author
  correlation_id: {cardinality: "required khi computation thuộc một correlation flow tường minh; optional khi độc lập"}
  causation_refs: {cardinality: "KHÔNG BAO GIỜ rỗng — mọi Context event là derived fact từ authoritative upstream fact. Xem §3–§4 cho nội dung cụ thể."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3"}
  effective_time: {cardinality: "required — trên MarketContextSnapshot (§3), = effective_window CỦA CHÍNH fact đó (= effective_time của Candle định nghĩa computation point, §11). Trên MarketContextFactInvalidated (§4), = effective_window CỦA FACT ĐANG BỊ INVALIDATE — KẾ THỪA nguyên vẹn, KHÔNG tự khai báo/tính toán độc lập."}
  market_time: {cardinality: "PROHIBITED — Context là derived/computed fact, không phải quan sát trực tiếp venue."}
  source_identity: {cardinality: "PROHIBITED — Context không có external source retry/redelivery risk; dedup dùng computation identity, §10."}

subject_ref:                                       # shape canonical — Chapter 8 §8.2.2
  context_id: context-projection
  subject_kind: entity
  subject_type: MarketContext
  subject_id: <context_subject_id — opaque, stable, xem §1>
  scope:
    instrument_id: <string>
    venue_id: <string>
    timeframe: <string>
    context_type: market_context
    context_definition_version: <string>

event_types:                                       # Chapter 3 §3.2 naming — tham chiếu, không định nghĩa lại quy tắc đặt tên
  MarketContextSnapshot: MARKET_CONTEXT_SNAPSHOT
  MarketContextFactInvalidated: MARKET_CONTEXT_FACT_INVALIDATED
```

`stream_ref`/`producer_ref` — Phase 1, chưa tồn tại, cùng nguyên tắc defer đã áp dụng xuyên suốt. `subject_ref.context_id: context-projection` là `domain_context_id` (Chapter 8 §8.2.2) — trùng tên với khái niệm nghiệp vụ "Context" thuần túy do trùng thuật ngữ, KHÔNG phải một trường hợp đặc biệt.

## 3. `MarketContextSnapshot` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: market-context-snapshot
kind: event
capability_id: context-aggregation
domain_context_id: context-projection
description: >
  Fact AUTHORITATIVE cho MỘT completed valid computation point — dùng cho CẢ HAI trường hợp:
  (a) original computation; (b) correction replacement (§12). Phát sinh cho MỌI computation
  point mà cadence đã pin (§11) yêu cầu, KỂ CẢ khi context_values không đổi so với point liền
  trước — đúng nguyên tắc classification-frequency của `regime.md` §9 / `feature.md` §3, áp
  dụng tương tự ở đây.
invariants:
  - "causation_refs KHÔNG BAO GIỜ rỗng: (a) original computation — PHẢI chứa context_cutoff_source_ref VÀ toàn bộ sáu role fact ref (§9); (b) correction replacement — PHẢI chứa các ref đã cập nhật VÀ chính MarketContextFactInvalidated đang được supersede."
  - "envelope.effective_time = effective_window (interval) của CHÍNH fact này = effective_time của context_cutoff_source_ref (§11)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của fact mới nhất trong normalized_input_fact_refs — KHÔNG được compute trước khi đủ evidence tồn tại (§14, chống look-ahead)."
  - "payload.context_subject_id, payload.context_type, payload.context_definition_version PHẢI khớp đúng subject_ref.subject_id VÀ toàn bộ subject_ref.scope."
  - "Mỗi ref trong sáu role fact PHẢI là Eligible Upstream Fact theo §8 cho đúng role đó — không thiếu, không thừa, không trùng lặp vai trò (§9 role cardinality)."
  - "normalized_input_fact_refs PHẢI được serialize theo đúng canonical normalized order đã định nghĩa ở §10 — KHÔNG phải thứ tự phát sinh tùy ý của computation."
  - "context_values PHẢI là bản sao trực tiếp từ trường giá trị authoritative của đúng fact ref tương ứng (structure_orientation từ eligible Structure fact's orientation field; volatility_regime_class/directional_persistence_regime_class từ regime_fact_ref.class; volatility_metric/directional_persistence_metric/distance_to_last_confirmed_swing từ feature_fact_ref.value) — Context KHÔNG tự tính toán lại, KHÔNG diễn giải thêm ý nghĩa."
  - "context_values KHÔNG BAO GIỜ chứa: signal strength; setup quality; long/short bias; buy/sell/hold; entry price; stop loss; take profit; position size; strategy ID; account state — vi phạm trực tiếp ranh giới Context/Strategy (§17)."
  - "supersedes_fact_ref VẮNG MẶT khi và chỉ khi đây là original computation cho (context_subject_id, effective_window) đó — CHƯA từng có MarketContextSnapshot nào khác cho đúng cặp subject+window này (đóng correction-lineage rule 1)."
  - "supersedes_fact_ref BẮT BUỘC có mặt khi (context_subject_id, effective_window) đó đã có một MarketContextSnapshot trước đó — đây là correction replacement (đóng rule 2)."
  - "supersedes_fact_ref, khi có mặt, PHẢI trỏ đúng lineage head HIỆN TẠI của (context_subject_id, effective_window) đó — fact CHƯA từng là supersedes_fact_ref của bất kỳ MarketContextSnapshot nào khác (cấm fork, đóng rule 6), VÀ đã nhận đúng một MarketContextFactInvalidated visible (§4) — không được trỏ tới một fact đã bị supersede trước đó (cấm nhảy cóc, đóng rule 4/5)."
  - "Khi supersedes_fact_ref có mặt, envelope.recorded_time của fact này PHẢI muộn hơn recorded_time của MarketContextFactInvalidated tương ứng — replacement không được 'visible' trước invalidation của chính fact nó thay thế (đóng rule 7)."
  - "Replacement fact PHẢI dùng ĐÚNG CÙNG (context_subject_id, effective_window) với fact bị supersede — không được đổi window khi correction (đóng rule 3)."
  - "Tất cả ref của replacement PHẢI phản ánh ancestry ĐÃ SỬA — không được giữ nguyên ref cũ đã không còn authoritative (đóng rule 8)."
  - "KHÔNG có shortcut khi context_values không đổi: nếu một upstream correction ảnh hưởng bất kỳ role ref nào, cặp MarketContextFactInvalidated + replacement PHẢI phát sinh — kể cả khi context_values cuối cùng giữ nguyên sau khi tính lại — đúng nguyên tắc `regime.md` §10 / `feature.md` §9."
  - "payload.computation_cursor PHẢI có mặt trên MỌI MarketContextSnapshot — original computation lẫn correction replacement, KHÔNG NGOẠI LỆ — giá trị là canonical Chapter 8 §8.5 Replay Cursor, applied nguyên vẹn KHÔNG định nghĩa lại (§14, §20 authority boundary). computation_cursor PHẢI độc lập thỏa mãn toàn bộ invariant validity của chính canonical Replay Cursor đó (Position → Cursor, Lifecycle → Cursor, Registry → Lifecycle, Registry → Contract — Chapter 8 §8.5.2/§8.5.3) — tài liệu này áp dụng, KHÔNG định nghĩa lại các invariant đó (ADR-046)."
  - "computation_cursor.recorded_time PHẢI <= envelope.recorded_time của CHÍNH fact này (Cursor → Context projection record anti-look-ahead relation, ADR-046) — bằng nhau được phép khi knowledge-cut capture và record append thuộc cùng valid processing boundary; vi phạm là invalid cursor, record KHÔNG được publish. KHÔNG được clamp timestamp, KHÔNG được substitute computation_cursor.recorded_time cho envelope.recorded_time hay ngược lại — hai trục độc lập."
  - "computation_cursor của một replacement fact ĐỘC LẬP HOÀN TOÀN với computation_cursor của fact nó supersede — mỗi fact, original hay replacement, pin đúng cursor THỰC TẾ nó dùng để evaluate §8, KHÔNG kế thừa/sao chép cursor của fact trước đó, độc lập với supersedes_fact_ref's target (ADR-046 Decision item 2)."
payload:
  context_subject_id: {type: string, required: true}
  context_type: {type: enum, values: [market_context], required: true}
  context_definition_version: {type: string, required: true}
  computation_cursor: {type: replay_cursor, required: true, description: "canonical Chapter 8 §8.5 Replay Cursor (shape owned by Chapter 8, applied here, not redefined) — exact knowledge boundary R dùng để evaluate §8 cho CHÍNH fact này. KHÔNG kế thừa/copy cursor của fact bị supersede khi là replacement — mỗi fact luôn pin cursor thực tế của chính nó. Xem §14 cho full cursor visibility predicate và COVERS_CONTEXT; ADR-046 (Approved) cho decision đầy đủ. KHÔNG PHẢI một phần computation identity (§10)."}
  effective_window:
    kind: interval
    window_start: {type: timestamp, required: true}
    window_end: {type: timestamp, required: true}
  context_cutoff_source_ref: {type: event_record_ref, required: true, description: "candle-closed/candle-corrected fact whose effective_time định nghĩa computation point này (§11) — cadence/cutoff driver, KHÔNG phải một trong sáu context_values role"}
  structure_fact_ref: {type: event_record_ref, required: true, description: "Eligible Structure fact (§8) — một trong break-of-structure-detected/change-of-character-detected/structure-recomputed"}
  volatility_regime_fact_ref: {type: event_record_ref, required: true, description: "Eligible regime-classified fact, regime_dimension=volatility (§8)"}
  directional_persistence_regime_fact_ref: {type: event_record_ref, required: true, description: "Eligible regime-classified fact, regime_dimension=directional_persistence (§8)"}
  feature_fact_refs:
    volatility_metric_fact_ref: {type: event_record_ref, required: true, description: "Eligible feature-computed fact, feature_type=volatility_metric (§8)"}
    directional_persistence_metric_fact_ref: {type: event_record_ref, required: true, description: "Eligible feature-computed fact, feature_type=directional_persistence_metric (§8)"}
    distance_to_last_confirmed_swing_fact_ref: {type: event_record_ref, required: true, description: "Eligible feature-computed fact, feature_type=distance_to_last_confirmed_swing (§8)"}
  normalized_input_fact_refs: {type: array, items: event_record_ref, required: true, description: "tập toán học 7 phần tử (context_cutoff_source_ref + sáu role ref), normalize theo §10 — KHÔNG phải thứ tự phát sinh tùy ý"}
  context_values:
    structure_orientation: {type: enum, values: [NEUTRAL, BULLISH, BEARISH], required: true, description: "sao chép trực tiếp từ structure_fact_ref's orientation field — UNDETERMINED không bao giờ xuất hiện ở đây (§9 — absence, không phải giá trị)"}
    volatility_regime_class: {type: enum, values: [LOW, NORMAL, HIGH, EXTREME], required: true}
    directional_persistence_regime_class: {type: enum, values: [NON_DIRECTIONAL, DIRECTIONAL, TRANSITIONAL], required: true}
    volatility_metric: {type: decimal, required: true}
    directional_persistence_metric: {type: decimal, required: true}
    distance_to_last_confirmed_swing: {type: decimal, required: true}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho original computation; BẮT BUỘC cho correction replacement — xem invariants."}
```

**Đơn vị (`unit`) KHÔNG lặp lại trong `context_values`** — tra cứu qua `feature_fact_ref` tương ứng và `feature_definition_version` đã pin (§6) để tránh hai bản `unit` có thể lệch nhau theo thời gian.

**Fail-closed cho tới khi referenced artifact resolve (ADR-046 Decision item 10).** `computation_cursor` được định nghĩa SCHEMA từ v0.3, nhưng publish một `MarketContextSnapshot` mang `computation_cursor` như durable evidence PHẢI fail-closed cho tới khi TOÀN BỘ artifact mà cursor tham chiếu genuinely resolve, persistently: Context-scoped Input Contract instance đã publish ([Chapter 8 §8.3.4](../constitution/08-event-model.md)), phiên bản chính xác của nó theo [ADR-041](../adr/ADR-041.md), pinned Stream Registry version, và required upstream Event Contract dependency authority. KHÔNG process-local/in-memory value nào được thay thế làm durable replay evidence. Amendment v0.3 này authorize **schema** ngay bây giờ; nó KHÔNG tự nó cho phép production publication dưới cơ chế này.

## 4. `MarketContextFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2 — `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: market-context-fact-invalidated
kind: event
capability_id: context-aggregation
domain_context_id: context-projection
description: >
  Phủ định MỘT MarketContextSnapshot lịch sử cụ thể — thuần túy ghi nhận "fact này không còn
  hợp lệ", KHÔNG tự nó tuyên bố giá trị mới. Nguyên nhân thuộc đúng MỘT trong ba dạng đã pin ở
  invariants dưới (ADR-046 Decision item 7) cho MỖI role bị ảnh hưởng: (a) một hoặc nhiều
  correction/invalidation event trực tiếp làm role ref hiện tại (thuộc bảy ref C đang cite, §3)
  không còn hợp lệ hoặc unresolved theo producer-domain semantics; (b) một upstream fact
  later-visible tự nó trở thành §8 winner mới tại R_later theo §8's temporal eligible-upstream
  supersession — ref cũ KHÔNG bắt buộc từng bị invalidate trực tiếp; hoặc (c) một compound
  role-state transition đòi hỏi NHIỀU direct causal prerequisite genuine để chứng minh trạng thái
  role mới — ví dụ một successor `B` later-visible (nhánh b) MÀ CHÍNH `B` sau đó lại bị invalidate
  (`I_B`), khiến role kết thúc missing/pending tại `R_later` MÀ KHÔNG resurrect ref cũ `A`;
  minimal-complete direct-cause set cho case này là `{B, I_B}` — `I_B` nhắm CHÍNH `B`, KHÔNG bắt
  buộc nhắm `A` (v0.4, `CONTEXT-DC-A-MAJ-02`). Nhánh (c) KHÔNG đơn thuần là "nhánh (a) cộng nhánh
  (b)" — tiêu chí đúng là: tập cause chứa ĐÚNG VÀ ĐỦ mọi direct domain causal predecessor/
  prerequisite genuine cần thiết để chứng minh role-resolution state mới, bất kể mỗi phần tử của
  tập đó nhắm ref cũ hay ref mới nào. KHÔNG có nguyên nhân `context_changed` chung
  chung nào được phát minh thêm. Nếu NHIỀU role bị ảnh hưởng đồng thời
  bởi cùng một correction gốc, chỉ phát ĐÚNG MỘT MarketContextFactInvalidated cho fact đó —
  causation_refs liệt kê đủ mọi nguyên nhân dưới dạng nhiều phần tử, affected_upstream_roles
  liệt kê đủ mọi role bị ảnh hưởng (đúng nguyên tắc dedup cascade của `structure.md` §10). Là
  event MỚI, append-only (I-3). **Envelope binding bắt buộc:** `subject_ref` và `effective_time`
  của chính event này KHÔNG được khai báo độc lập — chúng PHẢI kế thừa nguyên vẹn từ
  `invalidated_fact_ref` (fact F đang bị invalidate), đúng nguyên tắc `regime.md` §4 /
  `feature.md` §4.
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref (F) — cùng context_id, subject_kind, subject_type, subject_id, VÀ toàn bộ scope. Cấm target một fact thuộc subject KHÁC."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_window của invalidated_fact_ref (F) — [window_start, window_end) giống hệt. Cấm target một fact đúng subject nhưng SAI window."
  - "payload.invalidated_fact_ref PHẢI resolve đúng CHÍNH XÁC bản ghi event F — dùng event_record_ref (Chapter 8 §8.2.3)."
  - "payload.affected_upstream_roles PHẢI không rỗng, các phần tử duy nhất (không trùng lặp). MỖI phần tử PHẢI có một minimal-complete deterministic direct-cause SET tương ứng trong causation_refs (một hoặc nhiều ref — KHÔNG bắt buộc đúng một, ADR-046 Decision item 7), thuộc đúng MỘT trong ba nhánh: (a) một hoặc nhiều correction/invalidation event trực tiếp của role đó (context_cutoff_source → CandleCorrected; structure → StructureFactInvalidated hoặc StructureRecomputed; volatility_regime/directional_persistence_regime → RegimeFactInvalidated; volatility_metric_feature/directional_persistence_metric_feature/distance_to_last_confirmed_swing_feature → FeatureFactInvalidated); (b) later-visible authoritative fact tự nó trở thành §8 winner mới tại R_later (structure-recomputed/break-of-structure-detected/change-of-character-detected/regime-classified/feature-computed đúng role) — role cũ KHÔNG bắt buộc từng bị invalidate; hoặc (c) compound role-state transition (v0.4, `CONTEXT-DC-A-MAJ-02`) — tập cause chứa ĐÚNG VÀ ĐỦ mọi direct domain causal predecessor/prerequisite genuine cần thiết để chứng minh role-resolution state mới, bất kể mỗi phần tử nhắm ref cũ hay ref mới nào (ví dụ successor B later-visible cộng invalidation của CHÍNH B, {B, I_B}, khi role kết thúc missing/pending tại R_later — I_B nhắm B, KHÔNG bắt buộc nhắm ref cũ A, §8). Nhánh (c) KHÔNG PHẢI đơn thuần "nhánh (a) cộng nhánh (b)" — tiêu chí là completeness/directness của tập cause, KHÔNG PHẢI một công thức cố định ghép hai nhánh kia. Attribution role→cause-set là deterministic từ governed event type + role discriminant (regime_dimension/feature_type khi áp dụng) + target/ref relationship (invalidated_fact_ref/supersedes_fact_ref khi có mặt) — KHÔNG từ thứ tự phần tử trong causation_refs."
  - "causation_refs PHẢI trỏ: invalidated_fact_ref (bắt buộc, đúng một, PHẢI trùng payload.invalidated_fact_ref); VÀ minimal-complete direct-cause set (một hoặc nhiều ref mỗi role, xem trên) cho MỖI role liệt kê trong affected_upstream_roles — union/dedup vào đúng MỘT flat causation_refs array — không thiếu, không thừa, không trùng lặp. Mọi phần tử PHẢI là genuine direct domain causal predecessor/prerequisite (Chapter 6 §6.7, Chapter 8 §8.2.3) — KHÔNG BAO GIỜ dùng causation_refs như một evidence bag chung; coverage evidence (K_context(R_new) - K_context(R_old), §14) KHÔNG được đưa vào đây chỉ vì nó visible tại R_later."
  - "invalidated_fact_ref PHẢI trỏ một MarketContextSnapshot CHƯA từng nhận MarketContextFactInvalidated khác — một fact chỉ bị invalidate đúng một lần."
  - "Đúng một MarketContextSnapshot có thể trỏ supersedes_fact_ref về invalidated_fact_ref này (§3 rule — cấm fork)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref VÀ muộn hơn recorded_time của MỌI event trong causation_refs còn lại."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead)."
  - "payload.computation_cursor PHẢI có mặt trên MỌI MarketContextFactInvalidated, KHÔNG NGOẠI LỆ — cùng canonical Chapter 8 §8.5 Replay Cursor shape như §3, cùng discipline validity (ADR-046). Đây là R_later — cursor boundary chứng minh invalidated_fact_ref không còn CURRENT-VALID lineage head, KHÔNG PHẢI computation_cursor của chính invalidated_fact_ref (field riêng của fact đó, §3), KHÔNG PHẢI envelope.recorded_time (append time, trục khác), KHÔNG PHẢI computation_cursor của một replacement tương lai (fact độc lập khác, §3) — ba trục độc lập, không thay thế lẫn nhau."
  - "computation_cursor.recorded_time PHẢI <= envelope.recorded_time của CHÍNH event này (Cursor → Context projection record, đối xứng invariant §3) — vi phạm là invalid cursor, record KHÔNG được publish; KHÔNG clamp, KHÔNG substitute."
  - "Universal current-lineage invalidation coverage precondition (ADR-046, §14): gọi C = MarketContextSnapshot bị invalidate qua invalidated_fact_ref, R_original = C.computation_cursor, R_later = computation_cursor CỦA CHÍNH event này — R_later COVERS_CONTEXT R_original (§14) BẮT BUỘC đúng TRƯỚC KHI event này được publish như một current-valid lineage transition, bất kể trigger class (direct correction — nhánh (a)/(c) trên — HAY temporal eligible-upstream supersession — nhánh (b), §8). Nếu coverage KHÔNG chứng minh được, event này KHÔNG được publish như một current-valid lineage transition — cursor đó VẪN được phép dùng cho historical/counterfactual replay analysis. Precondition này chỉ chứng minh knowledge KHÔNG regress — nó KHÔNG tự nó chứng minh tại sao invalidation xảy ra (câu hỏi đó do causation_refs/affected_upstream_roles trên trả lời)."
payload:
  computation_cursor: {type: replay_cursor, required: true, description: "canonical Chapter 8 §8.5 Replay Cursor — R_later, exact knowledge boundary chứng minh invalidated_fact_ref không còn current-valid lineage head. Xem §14 cho full cursor visibility predicate, COVERS_CONTEXT, và universal invalidation coverage precondition; ADR-046 (Approved) cho decision đầy đủ. KHÔNG PHẢI một phần computation identity (§10)."}
  invalidated_fact_ref: {type: event_record_ref, required: true}
  affected_upstream_roles: {type: array, items: {type: enum, values: [context_cutoff_source, structure, volatility_regime, directional_persistence_regime, volatility_metric_feature, directional_persistence_metric_feature, distance_to_last_confirmed_swing_feature]}, required: true, description: "một hoặc nhiều role bị ảnh hưởng — không rỗng, không trùng lặp"}
  invalidation_reason: {type: string, required: false}
```

## 5. `MarketContextCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event — không chịu envelope §2** (§2 áp dụng cho event record; read model là derived projection — Chapter 7 §7.4 Type 2 Projection). Rebuild được từ §3–§4. Một row cho mỗi `context_subject_id`.

**Canonical decision — no-row trước khi có fact đầu tiên (đúng `regime.md` §5 / `feature.md` §5):**

```text
Trước khi MarketContextSnapshot ĐẦU TIÊN tồn tại cho một context_subject_id:
  → KHÔNG có MarketContextCurrentView row nào tồn tại
  → GetCurrentContext trả về NOT_FOUND / ABSENT theo quy ước tầng query
  → KHÔNG materialize một row placeholder, KHÔNG có view_state giả định
```

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION` — **không có `UNAVAILABLE`**.

```yaml
id: market-context-current-view
kind: read_model
capability_id: context-aggregation
domain_context_id: context-projection
description: >
  Projection tiện dụng: snapshot "hiện tại" (computation point mới nhất hợp lệ) của một Context
  subject, rebuild được từ MarketContextSnapshot/MarketContextFactInvalidated. KHÔNG
  authoritative — mọi audit/replay/parity, VÀ mọi input cho một Domain Contract hay Strategy/
  Decision khác, PHẢI dùng authoritative event stream, KHÔNG BAO GIỜ dùng view này làm nguồn sự
  thật (I-12, Chapter 7 §7.4). Không được Strategy, Decision, hay bất kỳ Domain Contract nào
  khác tiêu thụ như authoritative input (§17). Cursor-bounded. Row chỉ tồn tại SAU khi
  MarketContextSnapshot đầu tiên đã visible — trước đó, không có row. Selection algorithm và
  deterministic total order — xem §13.
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream cùng context_definition_version đã pin, cùng implementation version (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho bất kỳ Domain Contract khác (kể cả chính context.md) hay Strategy/Decision — chỉ query/UI (Chapter 7 §7.4, Chapter 9 §9.5)."
  - "Không có view row nào tồn tại khi subject còn UNCOMPUTED (§1) — kỳ vọng bình thường, KHÔNG phải missing-data condition. Đây KHÔNG phải view_state = UNAVAILABLE (giá trị đó không tồn tại) — đây là sự VẮNG MẶT của chính row đó."
  - "view_state PHẢI đúng theo §13: VALID khi lineage head của target window hợp lệ, không có invalidation visible; PENDING_CORRECTION khi lineage head của target window có invalidation visible nhưng replacement CHƯA visible. KHÔNG có giá trị thứ ba. KHÔNG BAO GIỜ fallback về một fact đã invalidate, và KHÔNG BAO GIỜ fallback về một window cũ hơn target window."
schema:
  context_subject_id: {type: string, required: true}
  scope: {instrument_id: string, venue_id: string, timeframe: string, context_type: string, context_definition_version: string, required: true}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  context_values: {type: object, required: false, description: "chỉ có mặt khi view_state = VALID — shape đúng §3"}
  effective_window: {kind: interval, required: false, description: "chỉ có mặt khi view_state = VALID"}
  lineage_head_fact_ref: {type: event_record_ref, required: false, description: "chỉ có mặt khi view_state = VALID — xem §13"}
  last_recorded_time: timestamp
queries: [GetCurrentContext, GetContextHistory]
```

## 6. Market Context Definition — Referenced Authoritative Artifact (pinned policy, không hardcode một trường phái)

Mọi upstream role/version/policy **PHẢI pin theo `context_definition_version`** — Domain Contract này **không** chọn một cadence/cutoff/alignment cụ thể làm chuẩn phổ quát duy nhất, đúng tinh thần đã áp dụng cho `swing_definition`/`structure_definition`/`regime_definition`/`feature_definition`. **Định nghĩa bất biến sau khi được tham chiếu** (Chapter 8 §8.1.1) — đổi tham số semantic tạo `context_definition_version` MỚI.

```yaml
context_definition:                      # schema tối thiểu — KHÔNG khóa giá trị cụ thể
  context_definition_id: {type: string, required: true, description: "định danh ổn định cho MỘT cấu hình fan-in family — nhiều context_definition_version có thể thuộc cùng một context_definition_id"}
  context_definition_version: {type: string, required: true, description: "opaque, immutable, GLOBALLY UNIQUE — xem §1 invariant"}
  context_type: {type: enum, values: [market_context], required: true, description: "B4: đúng MỘT giá trị hợp lệ"}

  # === Required upstream definition versions — mỗi role đúng một version ===
  required_structure_definition_version: {type: string, required: true}
  required_volatility_regime_definition_version: {type: string, required: true}
  required_directional_persistence_regime_definition_version: {type: string, required: true}
  required_volatility_metric_feature_definition_version: {type: string, required: true}
  required_directional_persistence_metric_feature_definition_version: {type: string, required: true}
  required_distance_to_last_confirmed_swing_feature_definition_version: {type: string, required: true}

  # === Cadence / cutoff / alignment ===
  computation_cadence_policy: {type: enum, values: [DRIVEN_BY_CANDLE_CLOSE], required: true, description: "mỗi candle-closed/candle-corrected authoritative tại đúng (instrument_id, venue_id, timeframe) của subject định nghĩa đúng MỘT computation point mới — xem §11"}
  context_cutoff_policy: {type: enum, values: [CONTEXT_EFFECTIVE_WINDOW_END_INCLUSIVE], required: true, description: "context_cutoff = effective_window.window_end của computation point này = context_cutoff_source_ref.effective_time.window_end — xem §11"}
  window_alignment_policy: {type: enum, values: [LATEST_VALID_AT_OR_BEFORE_CONTEXT_CUTOFF], required: true, description: "mỗi role chọn fact hợp lệ MỚI NHẤT tại-hoặc-trước context_cutoff — xem §8"}
  eligible_upstream_fact_selection_policy: {type: string, required: true, description: "canonical identifier — total-order tie-break DÙNG CHUNG shape cho cả sáu role, CHỈ áp dụng trong Phase 2 để phá vỡ hòa giữa các survivor của Phase 1 (§8) — xem 'Giá trị canonical mặc định' dưới đây"}

  # === Missing-input / correction ===
  missing_input_policy: {type: enum, values: [NO_SNAPSHOT_WHEN_ANY_REQUIRED_ROLE_MISSING_OR_PENDING], required: true, description: "v0.2: enum đóng, đúng MỘT giá trị hợp lệ (đóng IRB-B4-MAJ-02) — pin canonical value tại 'Giá trị canonical mặc định' dưới đây, chi tiết behavior tại §9"}
  correction_policy: {type: string, value: "always_invalidate_and_replace_no_shortcut", description: "đúng §3 invariant — không shortcut khi context_values không đổi"}

  # === Output / normalization / current view ===
  output_schema: {structure_orientation: enum, volatility_regime_class: enum, directional_persistence_regime_class: enum, volatility_metric: decimal, directional_persistence_metric: decimal, distance_to_last_confirmed_swing: decimal}
  input_normalization_policy: {type: string, required: true, description: "canonical identifier — xem §10, khai báo DUY NHẤT tại đây"}
  current_view_selection_policy: {type: string, required: true, description: "canonical identifier — xem §13, khai báo DUY NHẤT tại đây"}
```

**Giá trị canonical mặc định (v0.2) — nguồn duy nhất cho ba policy identifier dạng chuỗi cộng một enum value, mọi nơi khác trong tài liệu chỉ tham chiếu theo tên field, không lặp lại chuỗi (đóng trước lớp lỗi IRB-B2-MIN-01-style ngay từ v0.1; `missing_input_policy` bổ sung tại v0.2, đóng `IRB-B4-MAJ-02`):**

```yaml
input_normalization_policy: effective_time_window_start_asc_then_window_end_asc_then_stream_id_asc_then_registry_version_asc_then_sequence_asc_then_event_id_asc   # §10
current_view_selection_policy: effective_window_end_desc_then_window_start_desc_then_recorded_time_asc_then_stream_id_asc_then_registry_version_asc_then_sequence_asc_then_event_id_asc   # §13
eligible_upstream_fact_selection_policy: effective_time_end_desc_then_effective_time_start_desc_then_recorded_time_asc_then_stream_id_asc_then_registry_version_asc_then_sequence_asc_then_event_id_asc   # §8 — dùng chung cho cả sáu role, CHỈ sau khi Phase 1 (eligibility filtering) đã lọc, dùng để phá vỡ hòa trong Phase 2
missing_input_policy: NO_SNAPSHOT_WHEN_ANY_REQUIRED_ROLE_MISSING_OR_PENDING   # §9 — enum đóng, đúng một giá trị hợp lệ ở v0.2
```

Một `context_definition_version` tương lai có thể chọn identifier khác cho từng policy, nhưng PHẢI vẫn total + deterministic + tương thích [ADR-009](../adr/ADR-009.md) — không dùng physical wall clock, không so `sequence` xuyên stream.

**Không hardcode một cấu hình fan-in cụ thể** — required definition version của từng role để ngỏ giá trị cụ thể, chọn qua `context_definition_version`, đúng yêu cầu tách "Context semantic contract" khỏi "specific upstream configuration policy" (cùng nguyên tắc mọi Domain Contract trước).

## 7. Upstream input roles — chi tiết từng role

Context tiêu thụ **đúng bảy** authoritative ref cho mỗi computation point — một cadence/cutoff driver (Candle) cộng sáu role fact (Structure/Regime×2/Feature×3). Không role nào ngoài bảy role này được thêm vào B4.

### 7.0 Context cutoff source — Candle (cadence/cutoff driver, không phải context_values role)

**Đúng một** `candle-closed`/`candle-corrected` authoritative fact tại `(instrument_id, venue_id, timeframe)` của Context subject — định nghĩa `effective_window`/`context_cutoff` của computation point này (§11). KHÔNG tiêu thụ `CandleObserved`/`CandleCurrentView`.

### 7.1 Structure — orientation hiện tại

**Đúng một** trong ba loại authoritative Structure event: `break-of-structure-detected`, `change-of-character-detected`, hoặc `structure-recomputed` — Eligible Structure fact theo §8, biểu diễn `structure_orientation` tại Context cutoff. Pin: `required_structure_definition_version`. Đối xứng: **KHÔNG** tiêu thụ `StructureCurrentView`, UI projection state, hay inferred state không được biểu diễn bởi authoritative fact.

### 7.2 Raw Regime — hai dimension bắt buộc

**Đúng một** `regime-classified` fact với `regime_dimension: volatility`, VÀ **đúng một** `regime-classified` fact với `regime_dimension: directional_persistence` — hai role độc lập, mỗi role Eligible theo §8. Pin: `required_volatility_regime_definition_version`, `required_directional_persistence_regime_definition_version`. **KHÔNG** tiêu thụ `RegimeCurrentView`.

### 7.3 Feature — đúng ba founding feature type

**Đúng một** `feature-computed` fact cho MỖI feature type: `volatility_metric`, `directional_persistence_metric`, `distance_to_last_confirmed_swing` — ba role độc lập, mỗi role Eligible theo §8. Pin: `required_volatility_metric_feature_definition_version`, `required_directional_persistence_metric_feature_definition_version`, `required_distance_to_last_confirmed_swing_feature_definition_version`. **KHÔNG** tiêu thụ `FeatureCurrentView`.

## 8. Eligible Upstream Fact selection — two-phase pipeline (dùng chung cho cả sáu role)

**v0.2 — `RA-B4-MAJ-01`/`IRB-B4-MAJ-01` (cùng một algorithmic defect):** v0.1 định nghĩa 5 bước "filter" tuần tự, nhưng bước 4 (Currency) của role Structure tham chiếu NGƯỢC tới kết quả của bước 5 (Not-invalidated) — "*U là fact có recorded_time LỚN NHẤT trong tập đã qua bước 1–3 VÀ bước 5*" — vi phạm nguyên tắc cơ bản: **không bước filter nào được tham chiếu kết quả của một bước SAU nó**. v0.2 tách rời hoàn toàn thành **hai phase độc lập, tuần tự, không tham chiếu ngược**: **Phase 1 — eligibility filtering** (mỗi candidate tự đủ điều kiện, hoàn toàn không phụ thuộc candidate khác hay phase sau) rồi **Phase 2 — role-specific current selection** (chỉ chạy trên tập SURVIVOR của Phase 1, không bao giờ quay lại Phase 1).

**Áp dụng bài học `feature.md` v0.2 (`RA-B3-MAJ-01`/`IRB-B3-MAJ-01`) — effective-time eligibility là một filter ĐỘC LẬP trong Phase 1, luôn chạy TRƯỚC Phase 2 (candidate selection/ordering), cho MỌI role, không chỉ một.**

### Phase 1 — Eligibility filtering (per-candidate, độc lập hoàn toàn với mọi candidate khác và với Phase 2)

Với một computation point tại `context_cutoff` (§11), `computation_cursor R` (§14, ADR-046 — canonical Chapter 8 §8.5 Replay Cursor mà bản thân computation point này sẽ pin lên chính fact nó tạo ra, §3/§4), và một role cụ thể (Candle cutoff source, Structure, hai Regime, ba Feature — mỗi role có tập candidate event type riêng, §7), một fact `U` **survive Phase 1** CHỈ KHI cả 4 bước dưới đây đều đúng, đánh giá THEO ĐÚNG THỨ TỰ, đánh giá ĐỘC LẬP cho từng `U` (không so sánh `U` với candidate khác ở Phase 1):

```text
1. Identity/scope match
   U.instrument_id / venue_id / timeframe == Context subject scope
   U role-specific discriminant khớp:
     Structure   → (không discriminant thêm, chỉ một Structure subject/scope)
     Regime      → U.regime_dimension khớp đúng dimension của role (volatility | directional_persistence)
     Feature     → U.feature_type khớp đúng feature_type của role
   U required definition_version khớp đúng field pin ở §6 cho role đó

2. Full cursor visibility tại computation_cursor R (v0.3, ADR-046 — thay thế scalar
   recorded-time-only test cũ; định nghĩa DUY NHẤT tại §14, tham chiếu tại đây không lặp lại)
   CẢ BA leg dưới đây đều phải đúng:
     (a) U.stream_id thuộc valid included-stream universe của R.input_contract_ref, hợp lệ tại
         R.lifecycle_frontier (Chapter 8 §8.3.5 Retained-in-Universe semantics)
     (b) U.sequence <= R.stream_positions[U.stream_id] — CHỈ so trong CÙNG logical stream,
         KHÔNG BAO GIỜ so sequence xuyên stream (Chapter 8 §8.3.3)
     (c) U.recorded_time <= R.recorded_time
   Một leg thất bại → U KHÔNG full-cursor-visible tại R, bị loại NGAY.

3. Effective-time cutoff (chống look-ahead, đóng trước RA-B3-MAJ-01-style defect) — trục ĐỘC LẬP
   với bước 2, KHÔNG BAO GIỜ collapse vào cursor visibility (§14)
   role-specific effective boundary CỦA U <= context_cutoff   (INCLUSIVE — khác Feature §9a's cutoff exclusive, xem §11)
     Structure  → U.effective_time (structure.md §2)     <= context_cutoff
     Regime     → U.analysis_window.window_end            <= context_cutoff
     Feature    → U.effective_window.window_end            <= context_cutoff
     Candle     → U.effective_time.window_end              <= context_cutoff  (= chính bằng nhau khi U là chính context_cutoff_source_ref)

4. Role-specific validity tại cursor (CHỈ xét CHÍNH candidate U — KHÔNG tham chiếu bất kỳ candidate nào khác, KHÔNG tham chiếu Phase 2)
   Structure → KHÔNG có StructureFactInvalidated visible tại R nhắm CHÍNH XÁC U (chỉ áp dụng khi U là BreakOfStructureDetected/ChangeOfCharacterDetected — StructureRecomputed không phải target hợp lệ của StructureFactInvalidated, structure.md §5; StructureRecomputed luôn survive bước này)
   Regime    → KHÔNG có RegimeFactInvalidated visible tại R nhắm CHÍNH XÁC U
   Feature   → KHÔNG có FeatureFactInvalidated visible tại R nhắm CHÍNH XÁC U
   Candle    → resolve correction lineage cho ĐÚNG cửa sổ Candle đó tại R (candle.md §10) — nếu một candle-corrected KHÁC, cùng cửa sổ, visible tại R VÀ supersede U, U KHÔNG survive bước này (chỉ current lineage head của cửa sổ mới survive)
```

Một candidate KHÔNG qua được bước nào thì bị loại NGAY khỏi tập survivor — không đánh giá các bước sau CHO CHÍNH candidate đó. **Bước 3 áp dụng ĐỘC LẬP với bước 2.** Kết thúc Phase 1: mỗi role có một **tập survivor** (có thể rỗng, một phần tử, hoặc nhiều phần tử).

**"Visible tại R" trong bước 4 (v0.3, ADR-046) resolve về ĐÚNG full-cursor-visibility predicate của bước 2/§14** — KHÔNG một scalar `recorded_time`-only shorthand yếu hơn; bước 4 xét CHÍNH XÁC các upstream correction/invalidation event (`StructureFactInvalidated`/`RegimeFactInvalidated`/`FeatureFactInvalidated`/Candle correction lineage) khi resolve producer-domain lineage tại R — đúng phạm vi upstream-input mà §14 định nghĩa (xem "Phạm vi CHÍNH XÁC" tại §14, v0.4 correction, `CONTEXT-DC-A-MAJ-01`). Trong §8, mọi lần cụm từ "visible tại R"/"visible" xuất hiện đều là CHÍNH XÁC predicate ba-leg này — KHÔNG hai nghĩa "visible" cạnh tranh nhau trong cùng một selection pipeline. Predicate này KHÔNG tự động áp dụng cho visibility của CHÍNH Context output record (`MarketContextSnapshot`/`MarketContextFactInvalidated`) trong lineage của nó — đó là output-history visibility, xem §13.

### Phase 2 — Role-specific current selection (CHỈ chạy trên tập survivor của Phase 1, không bao giờ tham chiếu ngược Phase 1 hay loại thêm candidate theo tiêu chí Phase 1)

```text
Structure → trong tập survivor role Structure, chọn candidate có recorded_time LỚN NHẤT (DESC) — mỗi BOS/CHoCH/StructureRecomputed TỰ NÓ set toàn bộ orientation (không tích lũy), nên "mới nhất theo recorded_time trong tập survivor" tương đương chính xác với fold tuần tự của structure.md §1, ĐÚNG vì Phase 1 đã loại hết fact invalidated trước đó rồi. Hòa recorded_time → total order (dưới đây) phá vỡ hòa.

Regime    → trong tập survivor role Regime (đúng dimension), chọn lineage head HIỆN TẠI: candidate mà KHÔNG survivor nào khác của cùng role có supersedes_fact_ref trỏ tới nó. KHÔNG fallback về một survivor đã bị supersede bởi survivor khác.

Feature   → tương tự Regime, đúng feature_type của role.

Candle    → trong tập survivor role Candle (Phase 1 bước 4 thường đã thu về đúng một current lineage head cho cửa sổ đó), chọn lineage head hiện tại; nếu edge case còn nhiều, total order phá vỡ hòa.
```

Winner của Phase 2 (đúng một candidate mỗi role, nếu tập survivor không rỗng) = Eligible Upstream Fact cho role đó.

**Total order tie-break** (CHỈ dùng trong Phase 2 để phá vỡ hòa giữa các survivor còn lại sau khi đã áp dụng tiêu chí role-specific ở trên — KHÔNG phải một bước filter riêng, dùng `eligible_upstream_fact_selection_policy` §6):

```text
1. role-specific effective boundary (analysis_window.window_end / effective_window.window_end / effective_time.window_end)   DESC
2. role-specific effective boundary start (analysis_window.window_start / effective_window.window_start / effective_time.window_start)   DESC
3. U.recorded_time            ASC
4. stream_ref.stream_id       ASC (lexical)
5. stream_ref.registry_version ASC (lexical)
6. sequence                   ASC (CHỈ trong cùng stream identity đã xác lập bởi 4+5)
7. U.event_id                 ASC (lexical)
```

So sánh tiêu chí 1 đến 7 theo đúng thứ tự; tiêu chí đầu tiên khác nhau quyết định; các tiêu chí sau KHÔNG được đánh giá; `sequence` chỉ so trong cùng stream identity — cấm so sánh xuyên stream. **Total order này CHỈ dùng để phá vỡ hòa TRONG Phase 2 — không bao giờ được áp dụng cho một candidate chưa survive Phase 1, dù candidate đó thắng theo tiêu chí 1.**

**Tập survivor Phase 1 rỗng cho một role (Phase 2 không có ứng viên nào để chọn):** role đó **missing** — xem §9 (role cardinality/missing-input).

### Required Structure verdict (normative, đóng `RA-B4-MAJ-01`/`IRB-B4-MAJ-01`)

```text
Structure A:
  recorded_time = R10
  valid (không có StructureFactInvalidated nào nhắm A)

Structure B:
  recorded_time = R20
  invalidated tại R30 (có StructureFactInvalidated nhắm B, visible từ R30)

Context cursor: R40

Kết quả bắt buộc: Structure A ĐƯỢC CHỌN.
```

Lý do: tại Phase 1 bước 4, B bị loại (StructureFactInvalidated nhắm B visible tại R40 >= R30) — B KHÔNG BAO GIỜ vào tập survivor, do đó KHÔNG BAO GIỜ được Phase 2 xem xét, bất kể `recorded_time` của B (R20) lớn hơn A (R10). Phase 2 chỉ thấy tập survivor `{A}`, chọn A.

**Hành vi giữa thời điểm invalidation và `StructureRecomputed`:** rebuild selection từ tập survivor Phase 1 (mọi authoritative orientation-setting event — BOS/CHoCH/StructureRecomputed — còn sống sót, visible tại cursor); Phase 2 chọn candidate MỚI NHẤT trong tập đó; KHÔNG BAO GIỜ dùng event đã invalidate (đã bị loại từ Phase 1); nếu tập survivor rỗng (không còn orientation-setting event nào sống sót), Structure role **missing** — không phát `MarketContextSnapshot` (§9).

### Temporal eligible-upstream supersession (v0.3, ADR-046)

Bounded thêm — CHỈ áp dụng **sáu role phân tích non-Candle**: Structure, volatility Regime, directional-persistence Regime, volatility-metric Feature, directional-persistence-metric Feature, distance-to-last-confirmed-swing Feature. Candle (context_cutoff_source) KHÔNG thuộc phạm vi trigger này — xem "Candle exclusion" dưới đây.

Với một `MarketContextSnapshot` C hiện CURRENT-VALID, đã evaluate tại `computation_cursor R_original`, temporal supersession tồn tại tại một `computation_cursor R_later` khi, cho ÍT NHẤT MỘT trong sáu role trên, TẤT CẢ đúng:

```text
1. role đã resolve về ref cũ A tại R_original (ref hiện C đang cite cho role đó, §3).
2. một hoặc nhiều record upstream cần thiết để xác lập trạng thái role MỚI KHÔNG full-cursor-
   visible (§14) tại R_original.
3. đúng những record đó ĐÃ full-cursor-visible (§14) tại R_later.
4. producer-domain correction/lineage semantics đã pin sẵn ở candle.md/structure.md/regime.md/
   feature.md (KHÔNG invent/redefine ở đây), VÀ effective-time eligibility (§8 bước 3, độc lập
   với cursor visibility) được áp dụng CHÍNH XÁC bằng CHÍNH các authority đó.
5. exact §8 selection tại R_later, cho ĐÚNG computation point VÀ ĐÚNG Context Definition, cho ra:
   MỘT winner KHÁC ref A; HOẶC role trở thành missing/pending (§9).
6. C do đó KHÔNG còn là CURRENT-VALID lineage head cho computation point này tại R_later — CHỈ
   một later-knowledge-boundary transition (§15 bitemporal clarification — KHÔNG rewrite lịch sử
   của chính C tại R_original).
7. R_later COVERS_CONTEXT R_original (§14) — universal invalidation coverage precondition §4 đã
   pin cho MỌI trigger class, áp dụng CHÍNH XÁC tại đây.
```

Ref cũ `A` KHÔNG bắt buộc từng bị invalidate trực tiếp — đây là một temporal winner-change condition, khác cấu trúc với repaint (§15's "KHÔNG BAO GIỜ bị ghi đè tại chỗ" không bị ảnh hưởng: `C` KHÔNG BAO GIỜ bị mutate, chỉ invalidate-rồi-replace, append-only, §12). Một candidate ĐÃ full-cursor-visible tại `R_original` (§14) nhưng KHÔNG được chọn là một **defect của computation gốc** (thuật toán §8 áp dụng sai tại `R_original`) — KHÔNG PHẢI temporal supersession theo mục này, phân biệt này giữ nguyên không đổi.

**Candle exclusion.** Candle (context_cutoff_source) KHÔNG thuộc phạm vi trigger sáu-role này — một Candle window khác, không liên quan, KHÔNG BAO GIỜ được supersede một computation point cũ hơn không thuộc về nó (Phase 1 bước 4's Candle correction-lineage resolution, cùng cửa sổ, đã đủ). Candle correction tiếp tục đi qua ĐÚNG lineage correction CÙNG computation point đã pin (§4 nhánh (a), `context_cutoff_source → CandleCorrected`). Candle direct correction VẪN thuộc phạm vi universal invalidation coverage precondition (§4) như mọi trigger khác.

## 9. Role cardinality và missing-input policy

Với MỖI computation point, yêu cầu **đúng**:

```text
1 Candle fact (context_cutoff_source_ref — cadence/cutoff driver, không phải một context_values role)
1 Structure fact
1 Volatility Regime fact
1 Directional Persistence Regime fact
1 volatility_metric Feature fact
1 directional_persistence_metric Feature fact
1 distance_to_last_confirmed_swing Feature fact
```

**Canonical `missing_input_policy` (v0.2, đóng `IRB-B4-MAJ-02`) — enum đóng, đúng một giá trị hợp lệ:**

```yaml
missing_input_policy: NO_SNAPSHOT_WHEN_ANY_REQUIRED_ROLE_MISSING_OR_PENDING   # §6
```

**Normative behavior — nếu MỘT role bất kỳ (kể cả Candle cutoff source) rơi vào bất kỳ trạng thái nào dưới đây:**

```text
absent (không có candidate nào survive Phase 1, §8)
invalidated without eligible replacement (survivor tồn tại nhưng không có lineage head hợp lệ — Regime/Feature)
pending correction (lineage head hiện tại đang chờ replacement, chưa visible)
definition-version mismatch (không candidate nào khớp required_*_definition_version đã pin, §6)
effective-time ineligible (mọi candidate đều bị loại ở Phase 1 bước 3)
```

```text
→ KHÔNG có MarketContextSnapshot nào được phát cho computation point đó
```

**Cấm tuyệt đối:**

```text
null filling
stale fallback trình bày như đang current
partial snapshot (thiếu một hoặc nhiều trong bảy ref)
implementation-selected behavior (engine tự quyết định làm gì khi role thiếu)
copy một MarketContextSnapshot cũ hơn như thể nó đại diện cho computation point hiện đang thiếu
```

Đây là **valid absence hoặc pending correction** theo lifecycle state của role đang thiếu — **không phải speculative null filling**.

## 10. Fact identity và input normalization

Computation identity cho một `MarketContextSnapshot`:

```text
(context_subject_id,
 effective_window.window_start,
 effective_window.window_end,
 context_definition_version,
 normalized_input_fact_refs ĐÃ NORMALIZE theo dưới đây)
```

`context_values` là **KẾT QUẢ, KHÔNG phải một phần identity** — hai computation với cùng input tuple PHẢI cho cùng kết quả (determinism), nhưng identity được xác lập bởi input tuple (đã normalize), không phải output.

**`normalized_input_fact_refs` PHẢI:**

- chứa **CHÍNH XÁC BẢY** phần tử (context_cutoff_source_ref + sáu role ref) — không thiếu, không thừa, không trùng lặp;
- được normalize vào một canonical order duy nhất, deterministic TRƯỚC khi: xây dựng computation identity; hashing; equality; dedup; serialize — dùng `input_normalization_policy` (§6): effective boundary `window_start` ASC, `window_end` ASC, `stream_id` ASC, `registry_version` ASC, `sequence` ASC (chỉ khi stream identity hòa), `event_id` ASC.

**Danh sách đã normalize LÀ tập evidence toán học** — cùng bảy fact, khác thứ tự đến (incoming order), PHẢI cho cùng normalized list, cùng computation identity. **Cấm tuyệt đối** so sánh `sequence` thô xuyên hai stream khác nhau như một global order ([Chapter 8 §8.3.3](../constitution/08-event-model.md)).

**Dedup rule:** cùng `context_subject_id`, cùng `effective_window`, cùng `context_definition_version`, cùng `normalized_input_fact_refs` → duplicate delivery → KHÔNG append event authoritative thứ hai; recomputation là **idempotent**.

**`computation_cursor` (§3/§4, v0.3, ADR-046) KHÔNG phải một phần computation identity/dedup.** Identity vẫn CHÍNH XÁC bốn thành phần đã pin ở trên — `context_subject_id`, `effective_window`, `context_definition_version`, `normalized_input_fact_refs` đã normalize — KHÔNG thêm `computation_cursor` vào identity/hash/dedup tuple. CÙNG evidence tuple đã evaluate dưới hai `computation_cursor` operational khác nhau (ví dụ cùng bảy ref, đến từ hai thời điểm evaluate khác nhau nhưng resolve cùng tập input) PHẢI được coi là CÙNG một computation identity — KHÔNG âm thầm tạo ra hai fact identity khác nhau chỉ vì cursor operational khác nhau; identity là hàm của evidence, KHÔNG phải hàm của cursor evaluate nó.

## 11. Snapshot cadence

**`computation_cadence_policy: DRIVEN_BY_CANDLE_CLOSE` (§6):** mỗi `candle-closed`/`candle-corrected` authoritative fact tại đúng `(instrument_id, venue_id, timeframe)` của Context subject định nghĩa đúng MỘT computation point mới — `effective_window` của `MarketContextSnapshot` = `effective_time` của chính Candle đó (`context_cutoff_source_ref`), và `context_cutoff = effective_window.window_end`.

Một `MarketContextSnapshot` mới PHẢI phát sinh cho MỌI computation point required, **KỂ CẢ khi mọi `context_values` giống hệt point liền trước** (§3 mô tả invariant tương ứng):

```text
W1 context_values = X
W2 context_values = X
```

phải sinh **hai fact riêng biệt** khi W1 và W2 là hai computation point độc lập required — đúng nguyên tắc classification-frequency của `regime.md` §9 / `feature.md` §3.

Dedup CHỈ áp dụng cho identical Context computation identity (§10), không bao giờ áp dụng chỉ vì `context_values` trùng.

## 12. Correction lineage

Correction lineage scoped chính xác theo `(context_subject_id, effective_window.window_start, effective_window.window_end)` — mỗi window có chuỗi lineage RIÊNG, độc lập với mọi window khác trên cùng subject.

**Luồng bắt buộc:**

```text
MarketContextSnapshot C1
  → MarketContextFactInvalidated targeting C1
  → replacement MarketContextSnapshot C2, supersedes_fact_ref = C1

Correction tiếp theo:
C2
  → MarketContextFactInvalidated targeting C2
  → C3, supersedes_fact_ref = C2   (KHÔNG được supersedes_fact_ref = C1 — cấm nhảy cóc)
```

**Mười invariant bắt buộc** (đã pin tại §3/§4, tổng hợp lại đây):

1. Original fact không có `supersedes_fact_ref`.
2. Replacement fact bắt buộc có `supersedes_fact_ref`.
3. Replacement dùng đúng cùng subject và cùng `effective_window`.
4. Replacement PHẢI supersede đúng lineage head hiện tại — không target một fact đã bị supersede.
5. Replacement không được nhảy cóc qua một head trung gian (hệ quả trực tiếp của #4).
6. Một fact bị invalidate có **tối đa một** replacement authoritative trực tiếp — cấm fork.
7. Replacement không được "visible" (`recorded_time`) trước invalidation tương ứng.
8. Replacement pin ancestry ĐÃ SỬA — không giữ ref cũ không còn authoritative.
9. Mọi lineage member lịch sử giữ nguyên trong log — append-only (I-3), không mutate.
10. Một fact đã invalidate **không bao giờ** bị tái sử dụng ngầm — `MarketContextCurrentView` (§5, §13) phải loại trừ nó tường minh.

**Một upstream correction (Candle/Structure/Regime/Feature) có thể ảnh hưởng NHIỀU MarketContextSnapshot overlapping cùng lúc** (ví dụ một Structure cascade hoặc một Candle correction nằm trong evidence path của nhiều computation point liên tiếp). Với MỖI fact bị ảnh hưởng: **invalidate đúng fact đó → phát replacement ĐỘC LẬP cho đúng window đó — KHÔNG có dependency-forward ordering giữa các window độc lập** (đúng nguyên tắc `regime.md` §10 / `feature.md` §9 — Context KHÔNG cần tái tạo cascade nội bộ của Structure, chỉ tiêu thụ kết quả StructureFactInvalidated/StructureRecomputed đã hoàn tất từ `structure.md`).

**Nhiều role bị ảnh hưởng đồng thời bởi cùng một correction gốc trên MỘT snapshot:** chỉ phát ĐÚNG MỘT `MarketContextFactInvalidated`, `affected_upstream_roles` liệt kê đủ mọi role, `causation_refs` liệt kê đủ mọi nguyên nhân — đúng nguyên tắc dedup cascade `structure.md` §10 (đóng attack scenario "multiple upstream corrections affect one snapshot").

### Cursor semantics cho correction lineage (v0.3, ADR-046)

Bổ sung, KHÔNG thay thế mười invariant + hai paragraph trên — TẤT CẢ vẫn giữ nguyên hiệu lực nguyên vẹn.

**Phạm vi visibility trong mục này (v0.4 correction, `CONTEXT-DC-A-MAJ-01`).** Mọi visibility của UPSTREAM state dùng khi rerun §8 (ví dụ tại `R_replacement`, mục C dưới đây) hoặc thuộc `K_context(R)` LÀ ĐÚNG predicate ba-leg §14. Bất kỳ phát biểu nào về việc CHÍNH Context invalidation/replacement OUTPUT record (fact `MarketContextFactInvalidated`/`MarketContextSnapshot` mới) trở nên visible trong event history KHÔNG PHẢI predicate upstream-input đó — đó là output-history visibility, xem §13.

**A. Precondition trước MỌI invalidation.** Trước khi một `MarketContextFactInvalidated` publish như một current-valid lineage transition: `R_later COVERS_CONTEXT R_original` (định nghĩa canonical §14, precondition pin tại §4) BẮT BUỘC đúng — với `R_original = C.computation_cursor` (C = fact bị invalidate) và `R_later` = `computation_cursor` của chính invalidation đó.

**B. Case A — cùng re-evaluation boundary.** Khi replacement được phát sinh từ ĐÚNG kết quả §8 đã evaluate tại `R_later` (không có cursor advance nào giữa invalidation và replacement):

```text
replacement.computation_cursor == invalidation.computation_cursor == R_later
```

Refs/values của replacement PHẢI CHÍNH XÁC bằng kết quả §8 đã có tại `R_later` — KHÔNG recompute riêng, KHÔNG claim một knowledge boundary khác. Case A hợp lệ CHÍNH XÁC vì `R_later COVERS_CONTEXT R_original` đã được chứng minh TRƯỚC KHI invalidation publish (mục A trên) — replacement kế thừa nguyên vẹn boundary chưa-regress đó, không cần một coverage test riêng.

**C. Case B — fresh subsequent re-evaluation.** Khi replacement KHÔNG phát sinh từ đúng boundary `R_later` đó: một `computation_cursor` hợp lệ mới `R_replacement` được dùng. TRƯỚC KHI current-valid replacement publish:

```text
R_replacement COVERS_CONTEXT R_later   (§14)
```

BẮT BUỘC đúng, VÀ exact §8 selection PHẢI được rerun ĐỘC LẬP tại `R_replacement` — KHÔNG BAO GIỜ tái sử dụng kết quả `R_later` đã cache dưới một cursor khác. Refs/values/`normalized_input_fact_refs` của replacement PHẢI CHÍNH XÁC là kết quả fresh rerun đó. Nếu bất kỳ role nào missing/pending tại `R_replacement` — KHÔNG replacement nào được phát cho tới khi §9 cho phép một snapshot đầy đủ; KHÔNG BAO GIỜ stale-fallback. Replacement vẫn PHẢI dùng ĐÚNG CÙNG `(context_subject_id, effective_window)` lineage — mười invariant đầu §12 không đổi.

**D. Coverage chain (Case B).**

```text
K_context(R_original) ⊆ K_context(R_later) ⊆ K_context(R_replacement)
```

Đây là **transitive set inclusion cho MỘT Context lineage** — kết hợp precondition mục A (`R_later COVERS_CONTEXT R_original`) với mục C (`R_replacement COVERS_CONTEXT R_later`). KHÔNG PHẢI một platform-wide Replay-Cursor total order, KHÔNG PHẢI một ordering relation giữa các stream event độc lập ([ADR-009](../adr/ADR-009.md) không đổi). Với Case A, chain thu gọn về đúng quan hệ mục A đã chứng minh (`R_replacement == R_later`).

## 13. `MarketContextCurrentView` — validity rules và deterministic total order

**Phạm vi visibility tại mục này (v0.4 correction, `CONTEXT-DC-A-MAJ-01`) — output-history visibility, KHÔNG PHẢI §14's Context-upstream-input full-cursor predicate.** Mọi cụm từ "visible"/"visible tại cursor" trong mục này nói về visibility của CHÍNH Context OUTPUT record (`MarketContextSnapshot`/`MarketContextFactInvalidated`) tại governing read/replay boundary dùng để rebuild view — KHÔNG PHẢI predicate ba-leg upstream-input mà §14 định nghĩa cho universe của Context's OWN `computation_cursor.input_contract_ref` (universe đó chứa upstream stream Context TIÊU THỤ để compute, KHÔNG chứa CHÍNH Context output — Context output stream chưa được author, §16/§21). Cơ chế/schema cursor cụ thể cho output-record visibility này VẪN thuộc [Chapter 8](../constitution/08-event-model.md) nói chung và future Context output-stream topology khi được author — KHÔNG được định nghĩa mới ở correction này, KHÔNG author Context output stream/Event Contract nào ở đây. Toàn bộ target-window, lineage, `PENDING_CORRECTION`, và no-fallback semantics dưới đây giữ nguyên KHÔNG đổi.

**Bước 0 — row existence precondition:** nếu `context_subject_id` CHƯA từng có `MarketContextSnapshot` visible tại cursor → **KHÔNG có row nào tồn tại** — `GetCurrentContext` trả `NOT_FOUND`/`ABSENT`. Không materialize placeholder.

**Bước 1 — xác định TARGET WINDOW trước khi loại trừ bất cứ điều gì (v0.2 — làm rõ tie-break, non-blocking cleanup):** target window = window thắng theo đúng 2 tiêu chí dưới đây, đánh giá THEO ĐÚNG THỨ TỰ, trong TOÀN BỘ tập window mà subject này đã từng có ít nhất một `MarketContextSnapshot` visible tại cursor (KỂ CẢ nếu lineage head của window đó hiện đang invalidate):

```text
1. effective_window.window_end   DESC
2. effective_window.window_start DESC   (tie-break khi hai window khác nhau cùng window_end)
```

Quyết định target window xảy ra TRƯỚC khi đánh giá bất kỳ lineage validity nào (Bước 2/3 dưới đây) — thứ tự này không đổi so với v0.1, chỉ làm tường minh tiêu chí tie-break thứ hai vốn đã ngầm định.

**Bước 2 — trong lineage của TARGET WINDOW đó, loại trừ:** mọi `MarketContextSnapshot` đã bị supersede; mọi replacement mà `MarketContextFactInvalidated` tương ứng CHƯA visible; mọi computation dùng ancestry chưa resolve hoặc không authoritative.

**Bước 3 — resolve view_state cho TARGET WINDOW:**

```text
lineage head của target window tồn tại VÀ KHÔNG có MarketContextFactInvalidated visible  → trả về nó (view_state: VALID)
lineage head của target window có MarketContextFactInvalidated visible, replacement CHƯA visible → view_state: PENDING_CORRECTION (KHÔNG lùi về window cũ hơn dù window đó vẫn VALID)
KHÔNG BAO GIỜ fallback về một giá trị đã invalidate, và KHÔNG BAO GIỜ fallback về một window cũ hơn target window chỉ vì target window đang pending
```

**Deterministic total order — 7 tiêu chí, lexicographic nghiêm ngặt (dùng `current_view_selection_policy`, §6):**

```text
1. effective_window.window_end   DESC
2. effective_window.window_start DESC
3. MarketContextSnapshot.recorded_time ASC
4. stream_ref.stream_id          ASC (lexical)
5. stream_ref.registry_version   ASC (lexical)
6. sequence                      ASC (CHỈ khi 4+5 đã hòa)
7. MarketContextSnapshot.event_id ASC (lexical)
```

So sánh tiêu chí 1 đến 7 theo đúng thứ tự; tiêu chí đầu tiên khác nhau quyết định; các tiêu chí sau KHÔNG được đánh giá.

## 14. Time semantics

```text
effective_window              — [window_start, window_end) của CHÍNH fact đó (§3), = effective_time của context_cutoff_source_ref
context_cutoff                 — = effective_window.window_end của computation point này (§6, §11)
computation_cursor             — canonical Chapter 8 §8.5 Replay Cursor (v0.3, ADR-046) — exact
                                  knowledge boundary R dùng để evaluate §8 cho MỘT fact cụ thể;
                                  KHÔNG một schema local — Chapter 8 sở hữu representation nguyên
                                  vẹn (§8.5.1 cardinality, §8.5.2 relational invariants, §8.5.3
                                  dynamic stream set); bắt buộc trên mọi MarketContextSnapshot/
                                  MarketContextFactInvalidated (§3, §4)
recorded_time                  — khi Ride tính/ghi nhận fact này (bắt buộc, mọi event — envelope §2)
market_time                    — PROHIBITED (§2)
```

**Không dùng `event_time`.**

**Upstream input event visibility — full cursor visibility (v0.3, ADR-046 Decision item 4; định nghĩa DUY NHẤT tại đây; §4/§8/§12/§15 tham chiếu ĐÚNG phạm vi upstream của nó, không lặp lại — xem "Phạm vi CHÍNH XÁC" ngay dưới).** Một upstream event `U` tham gia Context input selection/correction-state evaluation là **full-cursor-visible** tại Context `computation_cursor R` khi và chỉ khi CẢ BA leg dưới đây đều đúng:

```text
1. Stream-universe membership — U.stream_id thuộc valid included-stream universe của
   R.input_contract_ref, hợp lệ tại R.lifecycle_frontier (Chapter 8 §8.3.5 Retained-in-Universe
   semantics — một stream đã retire vẫn thuộc universe tới terminal_position, không bị loại ngầm).
2. Same-stream position — U.sequence <= R.stream_positions[U.stream_id] — CHỈ so trong CÙNG
   logical stream, KHÔNG BAO GIỜ so sequence xuyên stream (Chapter 8 §8.3.3).
3. Recorded-time boundary — U.recorded_time <= R.recorded_time (Chapter 5 §5.3's recorded-time
   boundary).
```

Bất kỳ leg nào fail → `U` KHÔNG full-cursor-visible tại `R`.

**Phạm vi CHÍNH XÁC của định nghĩa này (v0.4 correction, `CONTEXT-DC-A-MAJ-01`) — ADR-046 Decision item 4 chỉ định nghĩa visibility của MỘT upstream event tại Context `computation_cursor`, KHÔNG redefine mọi occurrence của "visible" trong toàn bộ Domain Contract.** Predicate ba-leg này áp dụng cho — và CHỈ cho:

```text
1. Ứng viên input tại §8 (Phase 1 bước 2).
2. Upstream correction/invalidation event được xét khi resolve producer-domain lineage tại R
   (§8 bước 4 — StructureFactInvalidated/RegimeFactInvalidated/FeatureFactInvalidated/Candle
   correction-lineage evidence).
3. Record dùng để xác lập temporal eligible-upstream supersession (§8).
4. K_context(R).
5. Chứng minh COVERS_CONTEXT.
```

Predicate này KHÔNG tự động định nghĩa visibility của `MarketContextSnapshot`, `MarketContextFactInvalidated`, replacement Context output record, hay `MarketContextCurrentView`'s own output-history traversal (§13) — đó là **output-history visibility**, một khái niệm khác, xem §13. Khi `visible`/`visible tại R` nói về một upstream event, đó LUÔN LÀ predicate ba-leg này (KHÔNG một shorthand `recorded_time`-only yếu hơn, KHÔNG hai nghĩa "visible" cạnh tranh nhau trong cùng một selection pipeline). Khi `visible` nói về CHÍNH `MarketContextSnapshot`/`MarketContextFactInvalidated`/replacement trong lineage của nó (§3, §4 phần liên quan tới chính output record, §12, §13), đó LÀ output-history visibility — hai khái niệm này KHÔNG được conflate.

**Input eligibility — hai điều kiện ĐỘC LẬP, cả hai PHẢI đúng cho MỌI role fact (v0.3 — thay thế công thức scalar `(a)` cũ bằng full cursor visibility; đúng nguyên tắc `feature.md` §12, ngăn RA-B3-MAJ-01-style defect ngay từ v0.1):**

```text
(a) full cursor visibility của role fact tại computation_cursor R (định nghĩa trên)
(b) role fact effective boundary <= context_cutoff      — effective-time eligibility (§8 bước 3, INCLUSIVE)
```

`(a)` một mình KHÔNG đủ — một fact full-cursor-visible vẫn có thể effective-time ineligible (§8). **Một fact effective muộn hơn `context_cutoff` KHÔNG BAO GIỜ được chọn cho computation point đó chỉ vì nó full-cursor-visible tại cursor batch muộn.** Cursor visibility và effective-time eligibility là HAI trục độc lập, KHÔNG BAO GIỜ collapse thành một.

**`COVERS_CONTEXT` — bounded, Context-scoped, partial knowledge-coverage relation (v0.3, ADR-046 Decision item 1b).** Định nghĩa `K_context(R)` — một khái niệm knowledge-set dùng CHỈ cho lập luận correctness, KHÔNG một payload field, KHÔNG một global cursor ordinal, KHÔNG một thay thế cho canonical Replay Cursor, KHÔNG một causation set:

```text
K_context(R) = tập toàn bộ Context-relevant upstream event record full-cursor-visible (định
               nghĩa trên) tại computation_cursor R, dưới đúng Context Input Contract universe R
               đã pin — bao gồm MỌI event family §16 authorize Context tiêu thụ: eligible
               candidate, losing candidate, correction, invalidation — KHÔNG chỉ bảy ref thắng
               (normalized_input_fact_refs, §10).
```

Với hai giá trị `computation_cursor` hợp lệ trên CÙNG một Context lineage:

```text
R_new COVERS_CONTEXT R_old   iff   K_context(R_old) ⊆ K_context(R_new)
                              AND  lifecycle/topology knowledge không regress trên canonical
                                   Lifecycle Stream (Chapter 8 §8.3.5) — lifecycle_frontier của
                                   R_new tại hoặc sau lifecycle_frontier của R_old, dùng đúng
                                   valid position ordering của CHÍNH stream đó, KHÔNG BAO GIỜ so
                                   xuyên stream.
```

`COVERS_CONTEXT` tường minh KHÔNG PHẢI: `R_new > R_old`; một platform-wide Replay-Cursor total order; một thay đổi [ADR-009](../adr/ADR-009.md); một ordering relation giữa các stream event độc lập. Đây là set-inclusion/non-regression của Context-relevant visible knowledge cho MỘT cursor progression của MỘT Context lineage, chứng minh hoàn toàn từ evidence Chapter 8 đã sở hữu sẵn.

**Chứng minh coverage — không cần field cursor mới** (sáu điều kiện canonical, v0.3, ADR-046):

```text
1. Old stream universe preserved — mọi Context input stream thuộc valid universe của R_old, mà
   lịch sử của nó relevant tới cùng Context semantics, vẫn được represent trong valid universe
   của R_new.
2. Same-stream position non-regression — dùng stable logical stream_id (Chapter 8 §8.3.1),
   R_new.stream_positions[stream_id] tại hoặc sau R_old.stream_positions[stream_id] cho MỖI
   stream áp dụng — CHỈ so trong CÙNG stream, KHÔNG BAO GIỜ so sequence xuyên stream.
3. Recorded-time non-regression — R_new.recorded_time >= R_old.recorded_time. Điều kiện 2 một
   mình KHÔNG chứng minh leg này: Chapter 5/Chapter 8 KHÔNG đảm bảo recorded_time monotonic với
   same-stream sequence. Chứng minh transitive cho MỌI E thuộc K_context(R_old):
       E.recorded_time <= R_old.recorded_time      (leg-3 visibility của CHÍNH R_old, theo định
                                                      nghĩa K_context(R_old))
       R_old.recorded_time <= R_new.recorded_time   (điều kiện này)
       do đó E.recorded_time <= R_new.recorded_time (bắc cầu)
   KHÔNG PHẢI một ordering claim — R_new.recorded_time >= R_old.recorded_time KHÔNG có nghĩa
   R_new > R_old, KHÔNG tự nó thiết lập event ordering (Chapter 5 §5.4/Chapter 8 §8.3.3 Ordering
   Authority không đổi).
4. Lifecycle-frontier non-regression — chỉ so trên canonical Lifecycle Stream (Chapter 8 §8.3.5),
   CHỈ trong CÙNG stream đó.
5. Retired streams — dùng nguyên vẹn Retained-in-Universe / terminal-position semantics của
   Chapter 8 §8.3.5 — retirement KHÔNG BAO GIỜ âm thầm loại lịch sử đã visible của stream đó khỏi
   coverage.
6. Input-Contract / Registry transition — KHÔNG yêu cầu version bằng nhau. Một Input Contract
   hoặc Stream Registry version mới hơn CHỈ được phép dưới R_new NẾU cursor kết quả vẫn preserve
   visibility của MỌI Context-relevant record đã visible tại R_old — nếu không, R_new KHÔNG cover
   R_old cho lineage transition đó; một intentional knowledge-dropping reset (nếu thực sự cần)
   đòi hỏi semantics riêng, governed riêng biệt — KHÔNG BAO GIỜ ẩn bên trong cursor replacement
   thông thường.
```

Chứng minh coverage KHÔNG BAO GIỜ so `sequence` xuyên stream identity khác nhau, KHÔNG BAO GIỜ yêu cầu `stream_registry_version`/`contract_version` bằng nhau, KHÔNG BAO GIỜ dựng một scalar cursor rank. FAIL CLOSED nếu coverage không chứng minh được cho một same-lineage transition thông thường — set inclusion KHÔNG BAO GIỜ được nới lỏng, KHÔNG một cursor rank nào được phát minh thay thế.

**Coverage vs. causation — tách biệt (v0.3, ADR-046).** `K_context(R)`/`COVERS_CONTEXT` là knowledge-boundary correctness evidence — chứng minh non-regression, KHÔNG BAO GIỜ *tại sao* một invalidation xảy ra. `causation_refs` (§4) là direct-causal-predecessor evidence — chứng minh *tại sao*. Coverage KHÔNG BAO GIỜ bị thu gọn thành một câu hỏi `causation_refs`, và `causation_refs` KHÔNG BAO GIỜ mở rộng để chứa mọi phần tử của `K_context(R_new) - K_context(R_old)` — chỉ minimal-complete direct-cause set đã pin ở §4 thuộc về `causation_refs`.

**Warm-up — valid absence, không phải null:** trước khi đủ role fact tồn tại cho một computation point ứng viên, **không** phát `MarketContextSnapshot` (§9).

**Historical batch/Backtest computation:** khi nạp dữ liệu lịch sử đã có đủ input cho nhiều computation point liên tiếp, engine tính TUẦN TỰ từng point theo đúng cadence Candle-close đã pin — không nhảy thẳng tới point cuối cùng.

**Correction visibility:** `MarketContextFactInvalidated` và replacement `MarketContextSnapshot` đều có `recorded_time` mới; replay tại cursor trước đó chỉ thấy fact gốc.

**Không có input nào vượt quá `context_cutoff` được dùng làm evidence cho computation point đó.**

## 15. No repaint và mode parity

- **Bitemporal clarification (v0.3, ADR-046) — lịch sử không bị viết lại.** Một `MarketContextSnapshot` C vẫn **immutable và historically correct** đúng như evaluate tại `computation_cursor R_original` của chính nó — một `MarketContextFactInvalidated` sau này (tại `R_later`) KHÔNG BAO GIỜ viết lại tính đúng đắn lịch sử đó, và KHÔNG BAO GIỜ tuyên bố C's own original evaluation sai. Điều duy nhất đổi tại `R_later` là: C không còn là CURRENT-VALID lineage head cho computation point của nó — một later-knowledge-boundary transition, ghi nhận đúng như mọi correction khác trong tài liệu này (append-only, §12, không repaint).
- **`MarketContextSnapshot` KHÔNG BAO GIỜ bị ghi đè tại chỗ** — chỉ có thể bị phủ định qua `MarketContextFactInvalidated` + replacement, luôn append-only (I-3).
- **Không in-place mutation ở bất kỳ đâu** — mọi lineage member (kể cả đã bị supersede) giữ nguyên vĩnh viễn trong log.
- **Effective-time vs recorded-time tách bạch trung thực** — đúng T-vs-T+n discipline xuyên suốt `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`.
- **Cursor-correct pending correction** — replay giữa invalidation và replacement thấy đúng `PENDING_CORRECTION` (§13), không âm thầm dùng giá trị cũ.
- **Hai khái niệm visibility tách biệt (v0.4 correction, `CONTEXT-DC-A-MAJ-01`) — không conflate.** (1) Historical Context INPUT reconstruction dùng `computation_cursor` riêng của từng record VÀ §14's full upstream-input predicate (bullet "No look-ahead" ngay dưới). (2) Việc Context OUTPUT record (`MarketContextSnapshot`/`MarketContextFactInvalidated`) có visible với replay/current-view traversal hay không LÀ output-history visibility (§13, bullet "Cursor-correct pending correction" trên) — KHÔNG PHẢI §14's predicate. Hai khái niệm này độc lập, không được dùng thay thế lẫn nhau.
- **No look-ahead qua batch recomputation (v0.3 — dùng đúng `computation_cursor` thực tế, ADR-046):** historical Backtest/Replay tại một recorded cursor MUỘN PHẢI reconstruct MỖI `MarketContextSnapshot` chỉ dùng fact thỏa **CẢ HAI** điều kiện tại đúng `computation_cursor` của CHÍNH fact đó (§14): full-cursor-visible (§14, ba leg — KHÔNG chỉ scalar recorded-time) VÀ effective-time eligible (§8). Một fact effective muộn hơn (Structure/Regime/Feature/Candle) **KHÔNG BAO GIỜ** được "nhảy vào" một computation point sớm hơn mà nó effective-time ineligible tại điểm đó.
- **Cùng một chuỗi computation xuyên Backtest/Replay/Paper/Live** — deterministic given `(context_definition_version, upstream causal ancestry)` — bắt buộc SINH RA đủ MỌI computation point giống nhau ở mọi mode, bao gồm cùng tập bảy Eligible fact tại cùng computation point.
- **Warm-up/missing-input deterministic** — áp dụng đồng nhất mọi mode.

## 16. Input contracts — chỉ authoritative facts thực sự cần

Context tiêu thụ **chỉ những contract mà bảy role thực sự cần**, không hơn:

```text
candle-closed                       — cadence/cutoff driver (§7.0)
candle-corrected                    — như trên, correction
break-of-structure-detected         — Structure role (§7.1)
change-of-character-detected        — Structure role
structure-fact-invalidated          — Structure role, correction
structure-recomputed                — Structure role, correction settle
regime-classified                   — hai Regime role (§7.2), dimension khác nhau
regime-fact-invalidated             — như trên, correction
feature-computed                    — ba Feature role (§7.3), feature_type khác nhau
feature-fact-invalidated            — như trên, correction
```

**Không tiêu thụ:** `CandleObserved`; bất kỳ `*-current-view` nào (`CandleCurrentView`/`StructureCurrentView`/`RegimeCurrentView`/`FeatureCurrentView`/chính `MarketContextCurrentView`); provisional/candidate fact (`SwingCandidateDetected`); `Swing` event trực tiếp (Structure đã tự tiêu thụ Swing — Context không cần đi vòng qua Structure để lấy lại Swing); Strategy/Decision/Risk/Account/Position/Execution/Order/Fill — tất cả chưa tồn tại hoặc không thuộc phạm vi input authority của Context ở B4.

**Phân biệt: §16 liệt kê EVENT FAMILY, KHÔNG PHẢI chính Context-scoped Input Contract artifact (v0.3, ADR-046).** Danh sách trên là upstream authoritative event family Context được authorize tiêu thụ — KHÔNG phải Chapter-8 Input Contract instance mà `computation_cursor.input_contract_ref` (§3, §4, ADR-046 Decision item 9) BẮT BUỘC pin. `ADR-046` (Approved) yêu cầu MỌI `computation_cursor` tương lai của Context resolve đúng MỘT Context-scoped Input Contract artifact — artifact đó **CHƯA được author ở v0.3 này**. Expected included-stream universe tương lai — derivable từ authority hiện có, `stream-registry.yaml` (fresh-verified) — là: `market-data-ingestion-candle`, `structure-engine-structure`, `raw-regime-engine-regime`, `feature-engine-feature` (bốn stream, KHÔNG Swing trực tiếp — đúng danh sách "Không tiêu thụ" trên, unaffected). `contract_id`/`contract_version`/`merge_policy`/`frontier_policy` cụ thể **KHÔNG được chọn ở đây** — không một authority hiện có nào unambiguously fix chúng; các giá trị này VẪN deferred cho tới một transaction authoring riêng, bounded, governed riêng biệt (§21).

## 17. Context và Strategy boundary

Context là một **authoritative market-state snapshot, không phải một decision**.

*(Thuật ngữ "authoritative market-state snapshot" ở trên là văn bản lịch sử, giữ nguyên KHÔNG rewrite bởi v0.3 — xem "Authority-neutral clarification (ADR-046, v0.3)" đầu tài liệu: `computation_cursor`/durable cursor evidence mà v0.3 thêm vào KHÔNG resolve/thay đổi terminology tension đã preserve với [Chapter 7 §7.4](../constitution/07-module-taxonomy.md)'s Type-2 Projection classification; câu này KHÔNG bị rewrite bởi amendment v0.3.)*

**Context KHÔNG tính toán lại — chỉ as-of select và sao chép (v0.2, làm rõ theo [ADR-014](../adr/ADR-014.md) narrow amendment, Approved 2026-07-30, controlling authority — xem khối đầu tài liệu):**

```text
Context THỰC HIỆN:
  as-of selection của authoritative Structure/Regime/Feature fact (§8)
  deterministic cutoff/window alignment (§11, §14)
  sao chép NGUYÊN VẸN giá trị đã có sẵn vào context_values (§3 invariant)
  assemble bảy fact ref thành một version-pinned market-state snapshot

Context KHÔNG BAO GIỜ:
  tự tính một engineered Feature mới
  tái sản xuất (reproduce) công thức/transformation của Feature Engine
  tự derive trade signal
  tự chấm điểm (score) setup
  đưa ra kết luận Strategy hay Decision
  thay thế Feature Engine cho bất kỳ mục đích computation nào
```

Đây là **ranh giới phân biệt Feature computation fan-in (Feature Engine sở hữu) với Context snapshot aggregation (Context sở hữu)** — hai operation khác nhau, không cạnh tranh authority, không operation nào là "chủ sở hữu thứ hai" của Feature computation semantics.

**Cho phép trong `context_values`:**

```text
structure orientation
regime class (hai dimension)
atomic Feature value (ba founding type)
exact evidence reference (bảy fact ref, §3)
```

**Cấm tuyệt đối:**

```text
LONG / SHORT / BUY / SELL / HOLD
entry / exit / stop / target
position size
trade score / setup grade
strategy selection
risk recommendation
```

Một Strategy Contract tương lai có thể tiêu thụ authoritative `market-context-snapshot`/`market-context-fact-invalidated` event — **KHÔNG author quan hệ đó ở B4** trừ khi đã đăng ký tường minh và có kiểm soát bởi `context-map.yaml` hiện tại (chưa có — §21).

## 18. Venue & timeframe neutrality

Cùng nguyên tắc [ADR-007](../adr/ADR-007.md)/`candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`: `instrument_id`/`venue_id`/`timeframe` là scope tường minh, không hardcode giả định venue cụ thể hay timeframe "chuẩn". Hai Context subject trên cùng instrument nhưng khác `venue_id` hoặc `timeframe` là hai subject **độc lập hoàn toàn**.

## 19. Replay/Backtest/Paper/Live parity

Cả bốn execution mode tiêu thụ đúng cùng envelope (§2) và payload (§3–§4) — pattern nạp input có thể khác theo mode (historical batch tính tuần tự, §14), nhưng domain semantic của Context không đổi theo mode (§10, §15).

## 20. Authority boundary

**Contract này sở hữu:** semantic aggregation (as-of selection + snapshot assembly, KHÔNG phải computation) cho `market_context`, `MarketContextCurrentView` projection shape, `context_definition_version` policy schema tối thiểu (§6), Eligible Upstream Fact selection policy hai-phase (§8), Current View total-order policy (§13); và, kể từ v0.3, các semantic Context-specific mà [ADR-046](../adr/ADR-046.md) (Approved, controlling architecture authority cho phần này) đã author: Context's own use của canonical `computation_cursor` trên `MarketContextSnapshot`/`MarketContextFactInvalidated` (§3, §4); role-resolution temporal-invalidation semantics cho sáu role non-Candle (§8); `COVERS_CONTEXT` same-lineage knowledge-non-regression semantics (§14); Case A/Case B correction-replacement cursor behavior (§12). **Áp dụng, không định nghĩa lại:** event envelope ([Chapter 8 §8.2](../constitution/08-event-model.md)); canonical Replay Cursor schema và validity invariant của chính nó ([Chapter 8 §8.5](../constitution/08-event-model.md), §8.5.1–§8.5.3); ordering/replay cursor mechanics nói chung ([Chapter 5](../constitution/05-time-model.md)/[Chapter 8](../constitution/08-event-model.md)); stream lifecycle mechanics ([Chapter 8 §8.3](../constitution/08-event-model.md)); ID opaque rule ([Chapter 6 §6.8](../constitution/06-identity-model.md)); Structure orientation semantics VÀ producer-domain correction lineage (`structure.md`); Regime independence từ Structure ([ADR-003](../adr/ADR-003.md), narrow amendment [ADR-014](../adr/ADR-014.md) Approved 2026-07-30, controlling authority — xem khối đầu tài liệu) VÀ producer-domain correction lineage (`regime.md`); Feature computation semantics VÀ producer-domain correction lineage (`feature.md`) — Context KHÔNG sở hữu, KHÔNG tái sản xuất công thức/transformation của Feature Engine (§17); Candle observation semantics VÀ producer-domain correction lineage (`candle.md`). `ADR-046` KHÔNG đổi, và amendment v0.3 này KHÔNG đổi, `module_type: projection`/`owns_authoritative_state: false` — xem "Authority-neutral clarification (ADR-046, v0.3)" đầu tài liệu. **Không sở hữu:** Strategy/Decision/Risk/Account/Execution/Position semantics (Package 0.2-C, chưa author); giá trị cụ thể của `context_definition_version` policy (configuration/Phase 1); Context type nào ngoài `market_context` (§21); bất kỳ Feature computation/formula/transformation nào (`feature.md` sở hữu duy nhất, §17).

## 21. Ngoài phạm vi — defer

**Deferred tường minh, không author ở B4:** nhiều Context type (ngoài `market_context`); nested Context composition; arbitrary rule expression; scoring/confidence model; ML Context; strategy-specific Context; account-aware Context; portfolio Context; Context-to-Context dependency; storage architecture; caching; materialized feature-store infrastructure; distributed computation; user-defined schema. Cơ chế tính `context_subject_id` deterministic cụ thể; cơ chế lưu trữ/versioning cụ thể của `context_definition_version` registry (Phase 1, cùng ghi chú `swing.md`/`structure.md`/`regime.md`/`feature.md`). Quan hệ Context → Strategy (contract Strategy chưa author, §17). **`missing_input_policy` (v0.2) KHÔNG còn là configuration instance để ngỏ** — đã pin canonical enum đóng tại §6/§9 (đóng `IRB-B4-MAJ-02`), không cần liệt kê ở đây nữa.

**Out of scope theo ranh giới domain (không phải "chưa làm"):** trade signal, entry/exit setup, risk recommendation — vi phạm trực tiếp định nghĩa Context nếu thêm vào (§17).

**Deferred bởi v0.3 (`ADR-046`) — chưa author/thực hiện ở transaction này:** Context-scoped Input Contract artifact (`contract_id`/`contract_version`/`merge_policy`/`frontier_policy`, §16); Context Event Contract (chưa tồn tại — KHÔNG mint version/`schema_version`/`allowed_streams`/output stream nào ở đây); Context output stream identity; publication wiring; cursor-aware `context-aggregator` runtime/history state (deterministic core hiện tại, `python/context-aggregator/**`, KHÔNG bị sửa bởi amendment này — vẫn `REVIEW A VALIDATED — CLEAN`); `MarketContextCurrentView` runtime implementation. Mỗi mục là một bounded, governed transaction riêng, sau khi Domain Contract v0.3 này qua Review A/Risk Classification VÀ sau khi referenced artifact ở §3/§16 genuinely resolve.

## 22. Open questions ngoài phạm vi

- `structure_orientation` chỉ có ba giá trị (`NEUTRAL`/`BULLISH`/`BEARISH`) trong `context_values` — khi Structure subject còn `UNDETERMINED` (chưa từng có BOS/CHoCH/StructureRecomputed nào), role Structure absent → không có `MarketContextSnapshot` theo §9. Liệu tương lai có cần một `context_type` biến thể chấp nhận Structure-absent (ví dụ cho instrument mới listing, chưa đủ lịch sử) hay B4's "no snapshot" behavior là đủ vĩnh viễn? Chưa quyết ở đây — author-level ambiguity note, không phải governance-level OQ, không đóng OQ-002/OQ-003.
- `context_definition_version` registry/lifecycle chưa có authoritative source riêng — tạm coi là Referenced Authoritative Artifact theo Chapter 8 §8.1.1 (§6), nhưng **chưa** có file/registry cụ thể nào author nó trong Package 0.2-B4. Cần quyết định khi có nhu cầu thực tế đầu tiên (đối xứng ghi chú `swing.md`/`structure.md`/`regime.md`/`feature.md`).
- Eligible Structure fact selection (§8, Phase 2, role Structure) dựa trên tiền đề mỗi BOS/CHoCH/StructureRecomputed tự set toàn bộ `orientation` (không tích lũy) nên "mới nhất theo recorded_time trong tập survivor" = đúng fold `structure.md` §1. `structure.md` không pin tường minh `effective_time` cho `StructureRecomputed` (không có `breaking_candle_refs` để suy ra, chỉ có `input_cursor_ref`) — Context áp dụng nguyên văn bất kỳ `effective_time` nào `structure.md` §2 thực sự gán cho event đó (không tự định nghĩa lại), nhưng đây là một ambiguity đã tồn tại sẵn trong `structure.md`, không phải do `context.md` tạo ra. Ghi nhận author-level, không chặn B4.
- **Đã đóng (2026-07-30):** [ADR-014](../adr/ADR-014.md) (narrow amendment ADR-003) đã được Product Owner **Approve** ngày 2026-07-30, sau ChatGPT + Claude narrow delta review Clean — architecture authority của `context.md` nay tường minh, `IRB-B4-MAJ-03` governance-resolved. Đây KHÔNG phải governance-level OQ (không đóng OQ-002/OQ-003) và **KHÔNG tự động đưa Package 0.2-B4 vào `Consolidated Stable`** — B4 vẫn cần một transaction package delta review/consolidation riêng, chưa thực hiện.
