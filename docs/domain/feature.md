---
id: feature
title: Feature
version: "0.2"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-07-29"
last_review: null
next_review: null
---

# Feature

> **Vai trò của tài liệu này:** Domain Contract của Package 0.2-B3 — điểm fan-in **có kiểm soát** duy nhất từ Structure/Raw Regime/Candle sang giá trị deterministic, strategy-consumable, đúng [ADR-003](../adr/ADR-003.md) (Approved: "Feature Engine: fan-in CÓ CHỌN LỌC từ cả hai — đây là nơi xử lý đồng bộ hóa (join) giữa 2 luồng event nếu cần"). Draft, chưa Approved/Locked. Thuộc capability `feature-engineering` / context `feature-engineering` — **đã đăng ký sẵn** tại [`context-map.yaml`](./context-map.yaml) từ Package 0.2-A (forward-declared), nay authored. **Phạm vi B3 là scope tối thiểu** — đúng ba founding feature type, không phải một framework indicator tổng quát.

Feature **KHÔNG phải** trade signal, action recommendation, Strategy decision, Context snapshot, Risk/Account state, arbitrary-code execution framework, hay universal indicator catalog. Nó là một **giá trị số học hoặc phân loại deterministic, authoritative**, tính từ authoritative upstream fact (Candle, Swing, Raw Regime) theo một Feature Definition đã pin — atomic, không tự kết hợp nhiều domain interpretation thành một kết luận.

Feature bao gồm **bốn concept riêng biệt**:

1. **Logical Feature Subject** (`kind: entity`) — identity ổn định của "chuỗi tính toán theo một feature type + definition version này", **một subject liên tục theo scope** (giống `regime.md` — không có subject mới per computation point; window/point chỉ là thuộc tính của từng fact, không phải identity).
2. **`FeatureComputed`** (`kind: event`) — fact authoritative cho MỘT completed valid computation point/window — dùng cho cả original computation lẫn correction replacement.
3. **`FeatureFactInvalidated`** (`kind: event`) — phủ định MỘT `FeatureComputed` lịch sử cụ thể, KHÔNG tự nó tuyên bố giá trị mới.

Cộng một **read model tùy chọn** (`FeatureCurrentView`) — projection tiện dụng, không authoritative.

**`feature-computed` / `feature-fact-invalidated` / `feature-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây, và đúng giá trị `contract_id` mà [`context-map.yaml`](./context-map.yaml) sẽ trích dẫn. Display name, concept ID, và `event_type` là ba đại lượng khác nhau, không cạnh tranh identity — cùng nguyên tắc `candle.md`/`swing.md`/`structure.md`/`regime.md` đã khóa.

**Ba concept lặp lại, học trực tiếp từ `regime.md` v0.2 (đã qua review đầy đủ)** — tài liệu này áp dụng ngay từ v0.1 các bài học đã trả giá ở Package 0.2-B2, không lặp lại lỗi: (a) `FeatureFactInvalidated` PHẢI kế thừa `subject_ref`/`effective_time` từ fact bị invalidate, không tự khai báo độc lập (đóng trước IRB-B2-MAJ-02-style defect); (b) `input_fact_refs` là tập toán học, normalize theo lexicographic order trước khi tính identity/hash/dedup (đóng trước IRB-B2-MAJ-01-style defect); (c) `FeatureCurrentView` dùng no-row semantics trước fact đầu tiên, `view_state` chỉ có `VALID`/`PENDING_CORRECTION`, không có `UNAVAILABLE` (đóng trước RA-B2-MIN-01-style defect); (d) mọi canonical policy identifier chỉ khai báo ĐÚNG MỘT NƠI trong tài liệu (đóng trước IRB-B2-MIN-01-style defect).

**v0.2 xử lý `RA-B3-MAJ-01`/`IRB-B3-MAJ-01`** (cùng một defect, một correction): eligible-Swing selection cho `distance_to_last_confirmed_swing` (§9a v0.1) thiếu một **effective-time cutoff filter** tường minh — một Swing có `pivot_effective_time.window_start` xảy ra CÙNG LÚC hoặc SAU reference Candle's `effective_time.window_end` có thể bị chọn nhầm chỉ vì nó recorded-time visible tại cursor, vi phạm bitemporal correctness ([Chapter 5](../constitution/05-time-model.md)) — "recorded-time visible" KHÔNG tương đương "effective-time eligible". v0.2 pin canonical cutoff decision `eligible_swing_effective_cutoff_policy: REFERENCE_CANDLE_WINDOW_END_EXCLUSIVE` (§6) và viết lại §9a thành một **ordered filter pipeline 5 bước tường minh** — effective-time eligibility LUÔN là một filter chạy TRƯỚC candidate ordering, không bao giờ để total order hợp thức hóa một Swing effective muộn hơn (§9a, §12, §13).

## 1. Logical Feature Subject — `kind: entity`

```yaml
id: feature
kind: entity
capability_id: feature-engineering
domain_context_id: feature-engineering
description: >
  Chuỗi computation authoritative liên tục cho MỘT feature type theo MỘT Feature Definition
  Version cụ thể, tại một instrument/venue/timeframe. Subject có identity LOGIC ổn định
  (`feature_subject_id`, năm field, KHÔNG bao gồm effective window/point) — KHÔNG phải Entity
  không-identity. Effective window/point KHÔNG phải một trục identity: nó định danh MỘT fact
  cụ thể trong chuỗi fact của subject này (§3), không phải subject riêng — cùng pattern
  `regime.md` §1 đã khóa.
invariants:
  - "feature_subject_id resolve deterministic từ ĐÚNG NĂM field qualifying scope: instrument_id, venue_id, timeframe, feature_type, feature_definition_version — cùng năm-field-scope luôn cho cùng feature_subject_id; khác bất kỳ field nào cho feature_subject_id KHÁC. feature_subject_id bất biến, KHÔNG tái sử dụng cho một subject khác (Chapter 6 §6.1)."
  - "feature_subject_id là opaque — domain logic KHÔNG được parse nó (Chapter 6 §6.8); mọi quyết định nghiệp vụ phải dùng field tường minh trong scope."
  - "feature_definition_version là opaque VÀ globally unique xuyên suốt mọi feature_definition_id (§6) — hai feature_definition_id khác nhau KHÔNG BAO GIỜ dùng chung một giá trị feature_definition_version. Vì vậy scope chỉ cần feature_definition_version (không cần feature_definition_id riêng) để xác định chính xác definition đang dùng — feature_type có mặt trong scope thuần túy cho query tiện dụng (redundant có chủ đích), đúng nguyên tắc candle.md/swing.md/structure.md/regime.md."
  - "Tham số riêng của một feature_type (ví dụ swing_direction cho distance_to_last_confirmed_swing) PHẢI pin trong Feature Definition (§6), KHÔNG được thêm thành field scope riêng — vì feature_definition_version đã bất biến, hai giá trị tham số khác nhau BẮT BUỘC là hai feature_definition_version khác nhau, tự động tạo hai subject khác nhau mà không cần mở rộng identity."
  - "instrument_id, venue_id, timeframe, feature_type, feature_definition_version bất biến sau khi subject được quan sát lần đầu — đổi bất kỳ field nào tạo ra một subject KHÁC, không phải mutate subject cũ. Đổi feature_definition_version tạo subject mới hoàn toàn — chuỗi fact cũ dưới definition cũ giữ nguyên, không bị diễn giải lại (Chapter 8 §8.1.1 Referenced Authoritative Artifact)."
  - "Effective window/point (§3) KHÔNG thuộc identity scope của subject — nó là thuộc tính của từng FeatureComputed fact. Hai fact khác window trên cùng subject là hai fact riêng biệt của CÙNG một subject, không phải hai subject."
  - "feature_type là enum đóng ở v0.1: [volatility_metric, directional_persistence_metric, distance_to_last_confirmed_swing] — mở rộng thêm feature type là một thay đổi Domain Contract tường minh (bump version), không tự phát sinh ngầm."
schema:
  feature_subject_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  instrument_id: {type: string, required: true, ref: instrument}
  venue_id: {type: string, required: true, ref: venue}
  timeframe: {type: string, required: true}
  feature_type: {type: enum, values: [volatility_metric, directional_persistence_metric, distance_to_last_confirmed_swing], required: true}
  feature_definition_version: {type: string, required: true, description: "pin chính xác Feature Definition đã dùng — §6"}
state_machine:
  initial_state: UNCOMPUTED
  states: [UNCOMPUTED, COMPUTED]
  transitions:
    - {from: UNCOMPUTED, to: COMPUTED, caused_by: FeatureComputed}
    - {from: COMPUTED, to: COMPUTED, caused_by: FeatureComputed}
  terminal_states: []
events_emitted: [FeatureComputed, FeatureFactInvalidated]
events_consumed: [CandleClosed, CandleCorrected, SwingConfirmed, SwingInvalidated, RegimeClassified, RegimeFactInvalidated]
commands: []
queries: []
```

**`UNCOMPUTED` là notional initial state** — cùng convention `UNSEEN`/`UNDETERMINED`/`UNCLASSIFIED` mà `candle.md`/`swing.md`/`structure.md`/`regime.md` đã khóa. **`COMPUTED → COMPUTED` là self-transition cho MỌI `FeatureComputed` kế tiếp** — state machine chỉ mô tả "subject đã từng compute hay chưa" (existence lifecycle), KHÔNG mã hóa giá trị hiện tại — đúng lý do `regime.md` §1 đã nêu (mỗi computation point là một fact độc lập, "current view" là một query, §11, không phải state lưu trữ).

## 2. Canonical event envelope — áp dụng cho mọi Feature event (§3–§4)

Mọi event ở §3–§4 là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). Mục này khóa **envelope chung** một lần — từng event bên dưới chỉ khai báo **payload đặc thù**. Chapter 8 sở hữu nguyên vẹn semantic của envelope; mục này **chỉ áp dụng, không định nghĩa lại**.

```yaml
envelope:                                          # Chapter 8 §8.2.1 — cardinality nguyên văn
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2) — xem bảng dưới
  event_contract_ref: {cardinality: required}        # {contract_id, contract_version}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}             # Chapter 5 — khi Ride tính/ghi nhận fact này, KHÔNG phải effective window time
  subject_ref: {cardinality: "required — shape canonical, xem dưới. Trên FeatureFactInvalidated (§4), PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate — không tự khai báo độc lập (đóng trước lớp lỗi IRB-B2-MAJ-02)."}
  stream_ref: {cardinality: required}                # {stream_id, registry_version} — Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # {module_id, implementation_version, run_id} — Phase 1, chưa author
  correlation_id: {cardinality: "required khi computation thuộc một correlation flow tường minh (ví dụ một lần backfill/replay cụ thể); optional khi computation độc lập"}
  causation_refs: {cardinality: "KHÔNG BAO GIỜ rỗng cho bất kỳ Feature event nào — Feature LUÔN là derived fact từ upstream authoritative fact (+ khi là correction replacement, FeatureFactInvalidated liền trước). Xem §3–§4 cho nội dung cụ thể."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3"}
  effective_time: {cardinality: "required — semantic KHÁC NHAU theo event type: trên FeatureComputed (§3), = effective_window CỦA CHÍNH fact đó, KHÁC theo từng fact. Trên FeatureFactInvalidated (§4), = effective_window CỦA FACT ĐANG BỊ INVALIDATE — KẾ THỪA nguyên vẹn, KHÔNG tự khai báo/tính toán độc lập."}
  market_time: {cardinality: "PROHIBITED — Feature là derived/computed fact, không phải quan sát trực tiếp venue."}
  source_identity: {cardinality: "PROHIBITED — Feature không có external source retry/redelivery risk; dedup của Feature dùng computation identity, xem §8."}

subject_ref:                                       # shape canonical — Chapter 8 §8.2.2
  context_id: feature-engineering
  subject_kind: entity
  subject_type: Feature
  subject_id: <feature_subject_id — opaque, stable, xem §1>
  scope:
    instrument_id: <string>
    venue_id: <string>
    timeframe: <string>
    feature_type: <volatility_metric | directional_persistence_metric | distance_to_last_confirmed_swing>
    feature_definition_version: <string>

event_types:                                       # Chapter 3 §3.2 naming — tham chiếu, không định nghĩa lại quy tắc đặt tên
  FeatureComputed: FEATURE_COMPUTED
  FeatureFactInvalidated: FEATURE_FACT_INVALIDATED
```

`stream_ref`/`producer_ref` resolve từ `stream-registry.yaml`/`module-registry.yaml` — cả hai thuộc Phase 1, chưa tồn tại tại Phase 0.2, cùng nguyên tắc defer đã áp dụng xuyên suốt.

**`subject_id` luôn giống nhau cho cùng năm-field scope, bất kể window/point nào đang được compute** — mọi `FeatureComputed`/`FeatureFactInvalidated` mô tả cùng `(instrument_id, venue_id, timeframe, feature_type, feature_definition_version)` PHẢI mang cùng `subject_ref.subject_id`.

## 3. `FeatureComputed` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: feature-computed
kind: event
capability_id: feature-engineering
domain_context_id: feature-engineering
description: >
  Fact AUTHORITATIVE cho MỘT completed valid computation point/window — dùng cho CẢ HAI
  trường hợp: (a) original computation; (b) correction replacement (§10). Phát sinh cho MỌI
  computation point mà Feature Definition (§6) yêu cầu, KỂ CẢ khi value không đổi so với
  point liền trước — đúng nguyên tắc classification-frequency của `regime.md` §9, áp dụng
  tương tự ở đây: một computation point khác KHÔNG BAO GIỜ là duplicate chỉ vì value trùng.
invariants:
  - "causation_refs KHÔNG BAO GIỜ rỗng: (a) original computation — PHẢI chứa toàn bộ input_fact_refs; (b) correction replacement — PHẢI chứa input_fact_refs đã cập nhật VÀ chính FeatureFactInvalidated đang được supersede."
  - "envelope.effective_time = effective_window (interval) của CHÍNH fact này."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của input fact mới nhất trong input_fact_refs — KHÔNG được compute trước khi đủ evidence tồn tại (§7, chống look-ahead)."
  - "payload.feature_subject_id, payload.feature_type, payload.feature_definition_version PHẢI khớp đúng subject_ref.subject_id VÀ toàn bộ subject_ref.scope — trường lặp lại có chủ đích cho query tiện dụng, không phải trục identity thứ hai."
  - "input_fact_refs PHẢI thỏa mãn ĐÚNG role cardinality mà Feature Definition (§6) pin cho feature_type này — không thiếu, không thừa, không trùng lặp; mọi ref PHẢI là authoritative fact (candle-closed/candle-corrected/swing-confirmed/regime-classified tùy feature_type) — KHÔNG dùng CandleObserved, SwingCandidateDetected, hay bất kỳ *-current-view nào."
  - "input_fact_refs PHẢI được serialize theo đúng canonical normalized order đã định nghĩa ở §8 — KHÔNG phải thứ tự phát sinh tùy ý của computation. Hai tập input fact giống hệt nhau nhưng đến theo thứ tự khác nhau PHẢI cho ra cùng một input_fact_refs đã serialize, cùng một computation identity."
  - "value PHẢI dùng kiểu decimal — CẤM binary float — khi cần exact deterministic parity (I-9), đúng mọi feature_type ở B3."
  - "supersedes_fact_ref VẮNG MẶT khi và chỉ khi đây là original computation cho (feature_subject_id, effective_window) đó — CHƯA từng có FeatureComputed nào khác cho đúng cặp subject+window này (đóng correction-lineage rule 1)."
  - "supersedes_fact_ref BẮT BUỘC có mặt khi (feature_subject_id, effective_window) đó đã có một FeatureComputed trước đó — đây là correction replacement (đóng rule 2)."
  - "supersedes_fact_ref, khi có mặt, PHẢI trỏ đúng lineage head HIỆN TẠI của (feature_subject_id, effective_window) đó — fact CHƯA từng là supersedes_fact_ref của bất kỳ FeatureComputed nào khác (cấm fork, đóng rule 6), VÀ đã nhận đúng một FeatureFactInvalidated visible (§4) — không được trỏ tới một fact đã bị supersede trước đó (cấm nhảy cóc qua lineage, đóng rule 4/5)."
  - "Khi supersedes_fact_ref có mặt, envelope.recorded_time của fact này PHẢI muộn hơn recorded_time của FeatureFactInvalidated tương ứng — replacement không được 'visible' trước invalidation của chính fact nó thay thế (đóng rule 7)."
  - "Replacement fact PHẢI dùng ĐÚNG CÙNG (feature_subject_id, effective_window) với fact bị supersede — không được đổi window khi correction (đóng rule 3)."
  - "input_fact_refs của replacement PHẢI phản ánh ancestry ĐÃ SỬA — không được giữ nguyên ref cũ đã không còn authoritative (đóng rule 8)."
  - "KHÔNG có shortcut khi value không đổi: nếu một upstream correction ảnh hưởng input_fact_refs, cặp FeatureFactInvalidated + replacement PHẢI phát sinh — kể cả khi value cuối cùng giữ nguyên sau khi tính lại — đúng nguyên tắc `regime.md` §10."
payload:
  feature_subject_id: {type: string, required: true}
  feature_type: {type: enum, values: [volatility_metric, directional_persistence_metric, distance_to_last_confirmed_swing], required: true}
  feature_definition_version: {type: string, required: true}
  value: {type: decimal, required: true, description: "kết quả — KHÔNG phải một phần computation identity, xem §8"}
  unit: {type: string, required: true, description: "đơn vị số học — pin ở Feature Definition (§6)"}
  effective_window:
    kind: interval
    window_start: {type: timestamp, required: true}
    window_end: {type: timestamp, required: true}
  input_fact_refs: {type: array, items: event_record_ref, required: true}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho original computation; BẮT BUỘC cho correction replacement — xem invariants."}
```

## 4. `FeatureFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2 — `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: feature-fact-invalidated
kind: event
capability_id: feature-engineering
domain_context_id: feature-engineering
description: >
  Phủ định MỘT FeatureComputed lịch sử cụ thể — thuần túy ghi nhận "fact này không còn hợp
  lệ", KHÔNG tự nó tuyên bố giá trị mới và KHÔNG tự nó mutate FeatureCurrentView (§11 tự
  resolve trạng thái PENDING_CORRECTION khi thấy event này mà chưa có replacement). Nguyên
  nhân PHỤ THUỘC feature_type (khác `regime.md` — chỉ một nguyên nhân duy nhất, vì Feature có
  nhiều upstream contract khác nhau tùy feature_type):
  (a) candle_corrected — CandleCorrected ảnh hưởng một Candle ref trong input_fact_refs
      (áp dụng khi feature_type dùng upstream_source: candle, hoặc distance_to_last_confirmed_swing
      với reference Candle bị sửa);
  (b) regime_fact_invalidated — RegimeFactInvalidated (hoặc replacement RegimeClassified,
      regime.md §10) ảnh hưởng RegimeClassified ref trong input_fact_refs (áp dụng khi
      feature_type dùng upstream_source: regime);
  (c) swing_invalidated — SwingInvalidated ảnh hưởng SwingConfirmed ref trong input_fact_refs
      (áp dụng CHỈ cho distance_to_last_confirmed_swing khi Swing đã chọn bị invalidate).
  Là event MỚI, append-only (I-3) — không mutate record gốc.
  **Envelope binding bắt buộc:** `subject_ref` và `effective_time` của chính event này KHÔNG
  được khai báo độc lập — chúng PHẢI kế thừa nguyên vẹn từ `invalidated_fact_ref` (fact F đang
  bị invalidate), đúng nguyên tắc `regime.md` §4 (đóng IRB-B2-MAJ-02-style class defect từ đầu).
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref (F) — cùng context_id, subject_kind, subject_type, subject_id, VÀ toàn bộ scope. KHÔNG được khai báo subject_ref độc lập/khác biệt. Cấm target một fact thuộc subject KHÁC — kể cả khi mọi field khác đúng nhưng feature_definition_version sai (khác subject theo §1) hoặc feature_type sai (khác subject theo §1)."
  - "envelope.effective_time PHẢI BẰNG HỆT effective_window của invalidated_fact_ref (F) — [window_start, window_end) giống hệt, không sai lệch dù chỉ một trong hai biên. Cấm target một fact đúng subject nhưng SAI window."
  - "payload.invalidated_fact_ref PHẢI resolve đúng CHÍNH XÁC bản ghi event F — dùng event_record_ref (Chapter 8 §8.2.3: canonical locator + event_id verification field)."
  - "invalidation_cause PHẢI khớp đúng loại upstream contract mà Feature Definition (§6) của feature_type này thực sự khai báo — cấm dùng regime_fact_invalidated cho một feature_type chỉ dùng upstream_source: candle, và tương tự cho các cause khác."
  - "causation_refs PHẢI trỏ: invalidated_fact_ref (FeatureComputed đang bị invalidate — bắt buộc, đúng một, PHẢI trùng chính xác payload.invalidated_fact_ref); VÀ event authoritative là nguyên nhân trực tiếp (CandleCorrected/RegimeFactInvalidated/SwingInvalidated tùy invalidation_cause)."
  - "invalidated_fact_ref PHẢI trỏ một FeatureComputed CHƯA từng nhận FeatureFactInvalidated khác — một fact chỉ bị invalidate đúng một lần."
  - "Đúng một FeatureComputed có thể trỏ supersedes_fact_ref về invalidated_fact_ref này (§3 rule 6 — cấm fork)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref VÀ muộn hơn recorded_time của event gây ra nó."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_cause: {type: enum, values: [candle_corrected, regime_fact_invalidated, swing_invalidated], required: true}
  invalidation_reason: {type: string, required: false}
```

## 5. `FeatureCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event — không chịu envelope §2** (§2 áp dụng cho event record; read model là derived projection — Chapter 7 §7.4 Type 2 Projection). Rebuild được từ §3–§4. Một row cho mỗi `feature_subject_id`.

**Canonical decision — no-row trước khi có fact đầu tiên (đúng `regime.md` §5, đóng trước RA-B2-MIN-01-style ambiguity):**

```text
Trước khi FeatureComputed ĐẦU TIÊN tồn tại cho một feature_subject_id:
  → KHÔNG có FeatureCurrentView row nào tồn tại
  → GetCurrentFeature trả về NOT_FOUND / ABSENT theo quy ước tầng query
  → KHÔNG materialize một row placeholder, KHÔNG có view_state giả định
```

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION` — **không có `UNAVAILABLE`**.

```yaml
id: feature-current-view
kind: read_model
capability_id: feature-engineering
domain_context_id: feature-engineering
description: >
  Projection tiện dụng: giá trị "hiện tại" (computation point mới nhất hợp lệ) của một Feature
  subject, rebuild được từ FeatureComputed/FeatureFactInvalidated. KHÔNG authoritative — mọi
  audit/replay/parity, và mọi input cho Context/Strategy (khi được author), phải dùng
  authoritative event stream, KHÔNG dùng view này làm nguồn sự thật (I-12, Chapter 7 §7.4).
  Cursor-bounded. Row chỉ tồn tại SAU khi FeatureComputed đầu tiên đã visible — trước đó,
  không có row. Selection algorithm và deterministic total order — xem §11.
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream cùng feature_definition_version đã pin, cùng implementation version (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho bất kỳ Domain Contract khác (kể cả chính feature.md) hay Decision/Context/Strategy — chỉ query/UI (Chapter 7 §7.4, Chapter 9 §9.5)."
  - "Không có view row nào tồn tại khi subject còn UNCOMPUTED (§1) — kỳ vọng bình thường, KHÔNG phải missing-data condition. Đây KHÔNG phải view_state = UNAVAILABLE (giá trị đó không tồn tại) — đây là sự VẮNG MẶT của chính row đó."
  - "view_state PHẢI đúng theo §11: VALID khi lineage head của target window hợp lệ, không có invalidation visible; PENDING_CORRECTION khi lineage head của target window có invalidation visible nhưng replacement CHƯA visible. KHÔNG có giá trị thứ ba. KHÔNG BAO GIỜ fallback về một fact đã invalidate, và KHÔNG BAO GIỜ fallback về một window cũ hơn target window."
schema:
  feature_subject_id: {type: string, required: true}
  scope: {instrument_id: string, venue_id: string, timeframe: string, feature_type: string, feature_definition_version: string, required: true}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  value: {type: decimal, required: false, description: "chỉ có mặt khi view_state = VALID"}
  unit: {type: string, required: false, description: "chỉ có mặt khi view_state = VALID"}
  effective_window: {kind: interval, required: false, description: "chỉ có mặt khi view_state = VALID"}
  lineage_head_fact_ref: {type: event_record_ref, required: false, description: "chỉ có mặt khi view_state = VALID — xem §11"}
  last_recorded_time: timestamp
queries: [GetCurrentFeature, GetFeatureHistory]
```

## 6. Feature Definition — Referenced Authoritative Artifact (pinned policy, không hardcode một trường phái)

Value + upstream path + threshold/formula **PHẢI pin theo `feature_definition_version`** — Domain Contract này **không** chọn một công thức/nguồn dữ liệu cụ thể làm chuẩn phổ quát duy nhất, đúng tinh thần đã áp dụng cho `swing_definition`/`structure_definition`/`regime_definition`. **Định nghĩa bất biến sau khi được tham chiếu** (Chapter 8 §8.1.1) — đổi tham số semantic tạo `feature_definition_version` MỚI.

```yaml
feature_definition:                      # schema tối thiểu — KHÔNG khóa giá trị cụ thể
  feature_definition_id: {type: string, required: true, description: "định danh ổn định cho MỘT công thức/config family — nhiều feature_definition_version có thể thuộc cùng một feature_definition_id (các bản sửa/tinh chỉnh nối tiếp)"}
  feature_definition_version: {type: string, required: true, description: "opaque, immutable, GLOBALLY UNIQUE xuyên mọi feature_definition_id — xem §1 invariant"}
  feature_type: {type: enum, values: [volatility_metric, directional_persistence_metric, distance_to_last_confirmed_swing], required: true, description: "feature_definition_id PHẢI thuộc về đúng một feature_type — không dùng chung feature_definition_id cho hai feature_type khác nhau"}

  # === CHỈ áp dụng cho volatility_metric / directional_persistence_metric ===
  upstream_source: {type: enum, values: [candle, regime], description: "BẮT BUỘC chọn ĐÚNG MỘT — cấm hai path ambiguous cho cùng một feature_definition_version"}
  upstream_contract_refs: {type: array, description: "candle-closed/candle-corrected nếu upstream_source=candle; regime-classified/regime-fact-invalidated nếu upstream_source=regime — PHẢI khớp đúng upstream_source đã chọn, không được trộn"}
  required_upstream_definition_version: {type: string, description: "regime_definition_version PHẢI pin khi upstream_source=regime (đúng regime_dimension tương ứng feature_type); N/A khi upstream_source=candle"}
  window_candle_count: {type: integer, description: "chỉ áp dụng khi upstream_source=candle — số Candle trong effective window"}
  formula_id: {type: string, description: "định danh công thức/transformation — KHÔNG khóa công thức cụ thể ở đây"}
  parameters: {type: object, description: "tham số formula — schema riêng theo formula_id"}

  # === CHỈ áp dụng cho distance_to_last_confirmed_swing ===
  swing_direction: {type: enum, values: [HIGH, LOW], description: "HIGH hoặc LOW — pin trong definition, KHÔNG thuộc subject identity (§1)"}
  distance_representation: {type: enum, values: [signed, absolute]}
  reference_price_field: {type: string, description: "ví dụ candle.close — trường giá dùng làm điểm tham chiếu"}
  eligible_swing_selection_policy: {type: string, description: "canonical identifier — tái sử dụng methodology structure.md §6a total order, xem §9a. Feature pin giá trị RIÊNG của mình, không phụ thuộc registry 'đã tiêu thụ' của Structure. CHỈ áp dụng cho các ứng viên ĐÃ vượt qua eligible_swing_effective_cutoff_policy — total order không bao giờ chạy trước filter đó (§9a)."}
  eligible_swing_effective_cutoff_policy: {type: enum, values: [REFERENCE_CANDLE_WINDOW_END_EXCLUSIVE], required: true, description: "canonical cutoff quyết định một SwingConfirmed có effective-time eligible hay không, TÁCH BIỆT với recorded-time visibility — xem §9a bước 3. v0.2: đúng một giá trị hợp lệ, xem 'Giá trị canonical mặc định' dưới đây."}
  required_swing_definition_version: {type: string, description: "swing_definition_version PHẢI pin — swing.md §9"}
  normalization_policy: {type: string, required: false}

  # === CHUNG cho mọi feature_type ===
  unit: {type: string, required: true}
  decimal_precision_policy: {type: string, required: true, description: "rounding mode + số chữ số thập phân"}
  warm_up_policy: {type: string, required: true}
  missing_input_policy: {type: string, required: true}
  correction_policy: {type: string, value: "always_invalidate_and_replace_no_shortcut", description: "đúng §3 invariant — không shortcut khi value không đổi"}
  effective_window_policy: {type: string, required: true, description: "định nghĩa effective_window cho feature_type này — xem §7. Với distance_to_last_confirmed_swing: PHẢI dùng CHÍNH reference Candle làm mốc — effective_window của Feature fact KHÔNG được vượt quá effective_window của reference Candle đó (window_end trùng nhau); Eligible Swing được chọn (§9a) PHẢI effective strictly trước window_end này, đúng eligible_swing_effective_cutoff_policy."}
  output_schema: {value: decimal, unit: string}
  current_view_selection_policy: {type: string, required: true, description: "canonical identifier — xem §11, khai báo DUY NHẤT tại đây"}
  input_normalization_policy: {type: string, required: true, description: "canonical identifier — xem §8, khai báo DUY NHẤT tại đây"}
```

**Giá trị canonical mặc định (v0.2) — nguồn duy nhất cho bốn policy identifier, mọi nơi khác trong tài liệu chỉ tham chiếu theo tên field, không lặp lại chuỗi (đóng trước lớp lỗi IRB-B2-MIN-01-style ngay từ v0.1; `eligible_swing_effective_cutoff_policy` bổ sung tại v0.2, đóng `RA-B3-MAJ-01`/`IRB-B3-MAJ-01`):**

```yaml
input_normalization_policy: effective_time_window_start_asc_then_window_end_asc_then_stream_id_asc_then_registry_version_asc_then_sequence_asc_then_event_id_asc   # §8a
current_view_selection_policy: effective_window_end_desc_then_window_start_desc_then_recorded_time_asc_then_stream_id_asc_then_registry_version_asc_then_sequence_asc_then_event_id_asc   # §11
eligible_swing_selection_policy: pivot_effective_time_window_start_desc_then_recorded_time_asc_then_stream_id_asc_then_registry_version_asc_then_sequence_asc_then_swing_revision_desc_then_swing_id_asc_then_event_id_asc   # §9a — CHỈ áp dụng CHO các ứng viên đã qua eligible_swing_effective_cutoff_policy, cùng methodology structure.md §6a
eligible_swing_effective_cutoff_policy: REFERENCE_CANDLE_WINDOW_END_EXCLUSIVE   # §9a bước 3 — reference_cutoff = reference Candle effective_time.window_end; điều kiện S.pivot_effective_time.window_start < reference_cutoff (strict, half-open, KHÔNG bao gồm biên)
```

Một `feature_definition_version` tương lai có thể chọn identifier khác cho từng policy, nhưng PHẢI vẫn total + deterministic + tương thích [ADR-009](../adr/ADR-009.md) — không dùng physical wall clock, không so `sequence` xuyên stream.

**Không hardcode một trường phái phân tích** — `formula_id`/`parameters` để ngỏ giá trị cụ thể, chọn qua `feature_definition_version`, đúng yêu cầu tách "Feature semantic contract" khỏi "specific formula/configuration policy" (cùng nguyên tắc `swing_definition`/`structure_definition`/`regime_definition`).

## 7. Ba founding feature type — semantics chi tiết

### 7.1 `volatility_metric`

**Mục đích:** expose giá trị volatility deterministic cho Context/Strategy downstream. **Input authority — ĐÚNG MỘT path, không ambiguous:**

- `upstream_source: candle` — tính độc lập từ `window_candle_count` Candle authoritative (candle-closed/candle-corrected), công thức riêng (`formula_id`) — KHÔNG liên quan tới `regime.md`'s volatility computation.
- `upstream_source: regime` — expose lại `computed_metric` của đúng MỘT `RegimeClassified` fact có `regime_dimension: volatility` (regime.md §3) — Feature không tự tính lại, chỉ chuẩn hóa unit/rounding theo Feature Definition riêng của mình.

Một `feature_definition_version` PHẢI pin đúng MỘT trong hai path trên — không được để implementation tự chọn ngầm.

### 7.2 `directional_persistence_metric`

**Mục đích:** expose giá trị số học đứng sau Directional Persistence Regime. **Cùng cấu trúc dual-path như 7.1** — `upstream_source: candle` (tính độc lập) hoặc `upstream_source: regime` (expose lại `computed_metric` của `RegimeClassified` với `regime_dimension: directional_persistence`).

**Bắt buộc:** giữ nguyên **thống kê, liên tục** — KHÔNG mã hóa Bullish/Bearish, KHÔNG tiêu thụ Structure orientation (`current_orientation`, `BreakOfStructureDetected`, `ChangeOfCharacterDetected`) dưới bất kỳ hình thức nào — đúng ranh giới `regime.md` §6 đã khóa cho chính Directional Persistence Regime, Feature chỉ expose lại, không được "làm giàu" thêm ý nghĩa price-action.

### 7.3 `distance_to_last_confirmed_swing`

**Mục đích:** expose khoảng cách deterministic (signed hoặc absolute) từ một giá tham chiếu tới Swing CONFIRMED gần nhất, đúng hướng (`HIGH`/`LOW`) đã pin, dưới một selection policy deterministic.

**Input:**

- **Đúng một** Candle fact authoritative (candle-closed/candle-corrected) cho giá tham chiếu (`reference_price_field`, ví dụ `close`).
- **Đúng một** `SwingConfirmed` fact — Swing eligible được chọn theo total order riêng của Feature (§9a).
- **KHÔNG** tiêu thụ `SwingCurrentView`/`StructureCurrentView`/`RegimeCurrentView` hay bất kỳ non-authoritative projection nào.
- **KHÔNG** tiêu thụ Structure event nào (`BreakOfStructureDetected`/`ChangeOfCharacterDetected`/`StructureFactInvalidated`/`StructureRecomputed`) — chỉ tái sử dụng **methodology** total-order của `structure.md` §6a (xem §9a), không tiêu thụ event hay registry "đã consume" của Structure.

**Feature Definition PHẢI pin:** `swing_direction` (HIGH/LOW); `distance_representation` (signed/absolute); `reference_price_field`; `unit`; `normalization_policy` (nếu có); `eligible_swing_effective_cutoff_policy` (§9a bước 3 — v0.2, đóng `RA-B3-MAJ-01`/`IRB-B3-MAJ-01`); `eligible_swing_selection_policy` (§9a total order, CHỈ áp dụng SAU khi cutoff filter đã chạy); `required_swing_definition_version`.

**Canonical effective-time cutoff decision:** `reference_cutoff = reference Candle effective_time.window_end` (chính Candle dùng làm `reference_price_field`, §6 `effective_window_policy`). Một Swing chỉ eligible khi `SwingConfirmed.pivot_effective_time.window_start < reference_cutoff` — **strict, half-open**; một Swing có pivot bắt đầu ĐÚNG bằng `window_end` KHÔNG eligible cho computation point đó. **KHÔNG được dùng:** batch completion time; wall clock hiện tại; Swing được ghi nhận (recorded) mới nhất bất kể effective time; cutoff tự chọn ở tầng implementation; `FeatureCurrentView`'s time. Chi tiết thuật toán và ví dụ bắt buộc tại §9a.

## 8. Fact identity và input normalization

### 8a. Canonical input evidence normalization

**Định nghĩa bắt buộc (đúng `regime.md` §8a, tổng quát hóa cho input đa dạng loại event):** `input_fact_refs` PHẢI:

- chứa các authoritative event reference **duy nhất** (không trùng lặp);
- chứa **ĐÚNG role cardinality** mà Feature Definition (§6) pin cho `feature_type` này (ví dụ: `distance_to_last_confirmed_swing` = đúng 1 Candle ref + đúng 1 `SwingConfirmed` ref; `volatility_metric` path `candle` = đúng `window_candle_count` Candle ref; path `regime` = đúng 1 `RegimeClassified` ref);
- được **normalize vào một canonical order duy nhất, deterministic** TRƯỚC khi: xây dựng computation identity; hashing; so sánh bằng nhau; dedup; serialize event.

**Canonical order (6 tiêu chí — tổng quát hóa cho MỌI loại authoritative event, dùng field envelope chung `effective_time`/`stream_ref`/`sequence`/`event_id`, KHÔNG giả định mọi ref đều là Candle như `regime.md` §8a):**

| # | Tiêu chí | Hướng |
|---|---|---|
| 1 | ref's `effective_time.window_start` (hoặc instant, nếu không phải interval) | **ASC** |
| 2 | ref's `effective_time.window_end` (hoặc bằng window_start nếu instant) | **ASC** |
| 3 | `stream_ref.stream_id` | **ASC**, lexical |
| 4 | `stream_ref.registry_version` | **ASC**, lexical |
| 5 | `sequence` | **ASC** — CHỈ khi (3) VÀ (4) đã hòa |
| 6 | `event_id` | **ASC**, lexical |

**Thuật toán chuẩn (normative, lexicographic nghiêm ngặt — đúng bài học `structure.md` v0.4 sau IRB-FD-STR-MAJ-01, áp dụng ngay từ v0.1 tại đây):**

```text
So sánh tiêu chí 1 đến 6 theo đúng thứ tự.
Tiêu chí ĐẦU TIÊN có giá trị khác nhau quyết định thứ tự.
Các tiêu chí sau đó KHÔNG được đánh giá.
```

`sequence` (tiêu chí 5) chỉ được đánh giá khi CẢ `stream_ref.stream_id` VÀ `stream_ref.registry_version` đều bằng nhau — **cấm tuyệt đối** so sánh `sequence` thô giữa hai stream identity khác nhau ([Chapter 8 §8.3.3](../constitution/08-event-model.md)).

**Nếu cả sáu giá trị đều khớp giữa hai reference, chúng là duplicate representation của cùng một authoritative fact — chỉ giữ đúng MỘT canonical reference.**

```text
same input facts, khác thứ tự đến (incoming order)
→ same normalized input_fact_refs
→ same computation identity
```

**Canonical policy identifier — nguồn duy nhất tại §6 (`input_normalization_policy`)** — không lặp lại chuỗi ở nơi khác trong tài liệu này.

### 8b. Computation identity và dedup

Computation identity cho một `FeatureComputed`:

```text
(feature_subject_id,
 effective_window.window_start,
 effective_window.window_end,
 feature_definition_version,
 input_fact_refs ĐÃ NORMALIZE theo §8a)
```

**`value` là KẾT QUẢ, KHÔNG phải một phần identity** — hai computation với cùng input tuple PHẢI cho cùng kết quả (determinism), nhưng identity được xác lập bởi input tuple đã normalize, không phải output.

**Dedup rule:**

```text
same feature_subject_id
same effective window
same feature_definition_version
same normalized input_fact_refs
→ duplicate delivery → KHÔNG append event authoritative thứ hai
```

**Một computation point khác KHÔNG BAO GIỜ là duplicate chỉ vì value giống point trước** — khác `effective_window` (và do đó khác `input_fact_refs`) đã đủ để là một fact riêng biệt, bất kể `value` bằng nhau. Ví dụ:

```text
W1 → 0.025
W2 → 0.025
```

phải sinh **hai fact riêng biệt** khi W1 và W2 là hai computation point được Feature Definition yêu cầu độc lập — đúng nguyên tắc `regime.md` §8b/§9.

**Out-of-order upstream correction:** không được xử lý một correction event trước khi fact mà nó sửa đã được apply — đúng causal precedence bắt buộc của [Chapter 8 §8.3.4](../constitution/08-event-model.md).

**Deterministic replay (mode parity):** với cùng `feature_definition_version` và cùng input causal ancestry, Live/Backtest/Paper Trading/Replay PHẢI cho ra cùng tập fact, cùng `input_fact_refs` normalized.

## 9. Correction lineage

Correction lineage scoped chính xác theo `(feature_subject_id, effective_window.window_start, effective_window.window_end)` — mỗi window có chuỗi lineage RIÊNG, độc lập với mọi window khác trên cùng subject.

**Luồng bắt buộc:**

```text
FeatureComputed F1
  → FeatureFactInvalidated targeting F1
  → replacement FeatureComputed F2, supersedes_fact_ref = F1

Correction tiếp theo:
F2
  → FeatureFactInvalidated targeting F2
  → F3, supersedes_fact_ref = F2   (KHÔNG được supersedes_fact_ref = F1 — cấm nhảy cóc)
```

**Mười invariant bắt buộc** (đã pin tại §3/§4, tổng hợp lại đây):

1. Original fact không có `supersedes_fact_ref`.
2. Replacement fact bắt buộc có `supersedes_fact_ref`.
3. Replacement dùng đúng cùng subject và cùng `effective_window`.
4. Replacement PHẢI supersede đúng lineage head hiện tại — không target một fact đã bị supersede.
5. Replacement không được nhảy cóc qua một head trung gian (hệ quả trực tiếp của #4).
6. Một fact bị invalidate có **tối đa một** replacement authoritative trực tiếp — cấm fork.
7. Replacement không được "visible" (`recorded_time`) trước invalidation tương ứng của nó.
8. Replacement pin ancestry ĐÃ SỬA — không giữ ref cũ không còn authoritative.
9. Mọi lineage member lịch sử giữ nguyên trong log — append-only (I-3), không mutate.
10. Một fact đã invalidate **không bao giờ** bị tái sử dụng ngầm — `FeatureCurrentView` (§5, §11) phải loại trừ nó tường minh.

**Một upstream correction có thể ảnh hưởng NHIỀU Feature fact overlapping cùng lúc** (ví dụ một Candle correction nằm trong evidence window của nhiều computation point liên tiếp). Với MỖI fact bị ảnh hưởng: **invalidate đúng fact đó → phát replacement ĐỘC LẬP cho đúng window đó** — **KHÔNG có dependency-forward ordering giữa các window độc lập**, trừ khi một Feature-to-Feature dependency thực sự được author tường minh (§10, B3 KHÔNG author dependency này).

### 9a. Eligible-Swing selection — chỉ cho `distance_to_last_confirmed_swing`

**Tái sử dụng methodology của `structure.md` §6a — KHÔNG tiêu thụ event hay registry "đã consume" của Structure.** Feature pin giá trị policy RIÊNG của mình (`eligible_swing_selection_policy`, §6), độc lập với `structure_definition_version`'s registry state — tránh coupling correctness của Feature vào trạng thái nội bộ của Structure.

**v0.2 — `RA-B3-MAJ-01`/`IRB-B3-MAJ-01`:** v0.1 chỉ lọc theo recorded-time visibility rồi chạy thẳng total order — **thiếu một effective-time cutoff filter độc lập**, cho phép một Swing effective MUỘN HƠN reference Candle bị chọn nhầm chỉ vì nó recorded-time visible sớm. **Recorded-time visible KHÔNG tương đương effective-time eligible** — đây là hai trục bitemporal tách biệt ([Chapter 5](../constitution/05-time-model.md)). v0.2 tách Eligible-Swing selection thành **hai giai đoạn tường minh, không được gộp lại**: (1) một **ordered filter pipeline** (5 bước, AND — một ứng viên phải qua CẢ NĂM mới eligible) quyết định TẬP ứng viên; (2) total order 8 tiêu chí (không đổi so với v0.1) chỉ dùng để phá vỡ hòa (tie-break) TRONG tập đã qua bước (1). **Effective-time eligibility LÀ MỘT FILTER chạy TRƯỚC candidate ordering — total order không bao giờ được dùng để hợp thức hóa một Swing ineligible về effective time.**

**Bước 0 — canonical cutoff decision (bắt buộc, pin đúng một lần tại §6):**

```text
reference_cutoff = reference Candle C (§7.3 — Candle dùng làm reference_price_field).effective_time.window_end

eligible_swing_effective_cutoff_policy = REFERENCE_CANDLE_WINDOW_END_EXCLUSIVE (§6)
  → điều kiện: S.pivot_effective_time.window_start < reference_cutoff   (strict "<", half-open, KHÔNG "<=")
```

KHÔNG dùng: batch completion time; wall clock hiện tại; Swing recorded mới nhất bất kể effective time; cutoff tự chọn ở tầng implementation; `FeatureCurrentView`'s time.

**Eligible-Swing filter pipeline — cho một computation tại reference Candle `C`, cursor recorded-time `R`, một `SwingConfirmed S` là ứng viên hợp lệ CHỈ KHI cả 5 điều kiện dưới đây đều đúng, đánh giá THEO ĐÚNG THỨ TỰ này:**

```text
1. Identity/scope match
   S.instrument_id                    == Feature subject instrument_id
   S.venue_id                         == Feature subject venue_id
   S.timeframe                        == Feature subject timeframe
   S.swing_definition_version         == required_swing_definition_version (§6)
   S.swing_direction                  == swing_direction đã pin (§6)

2. Recorded-time visibility (swing.md §7 — không look-ahead)
   S.recorded_time <= R

3. Effective-time cutoff (MỚI — v0.2, đóng RA-B3-MAJ-01/IRB-B3-MAJ-01)
   S.pivot_effective_time.window_start < C.effective_time.window_end
   (đúng eligible_swing_effective_cutoff_policy = REFERENCE_CANDLE_WINDOW_END_EXCLUSIVE, Bước 0)

4. Latest valid revision
   S = revision hợp lệ MỚI NHẤT của swing_id đó, visible tại R (swing.md §1a)

5. Not invalidated
   KHÔNG có SwingInvalidated visible tại R cho ĐÚNG cặp (swing_id, swing_revision) của S (swing.md §5)
```

Một ứng viên KHÔNG qua được bước nào thì bị loại NGAY — không đánh giá các bước sau, không đưa vào total order. Bước 3 áp dụng ĐỘC LẬP với bước 2 — một Swing qua được bước 2 (recorded-time visible) vẫn có thể bị loại ở bước 3 (effective-time ineligible), và ngược lại đây là lý do bước 3 phải tồn tại như một bước riêng chứ không gộp vào bước 2.

**Không loại trừ Swing "đã dùng làm broken_swing_ref"** — đây là khác biệt tường minh so với `structure.md` §6a (nơi một Swing đã consume thì không đủ điều kiện lần nữa cho BOS/CHoCH); Feature chỉ đo khoảng cách, không "tiêu thụ" Swing theo nghĩa Structure — cùng một Swing có thể là Eligible Swing cho Feature bất kể Structure đã dùng nó làm break level hay chưa. (Điều kiện này không liên quan và không thay đổi bởi effective-time cutoff ở trên.)

**Ví dụ bắt buộc (normative, đóng `RA-B3-MAJ-01`/`IRB-B3-MAJ-01`):**

```text
Reference Candle C:
  effective_time.window_end = T10

Swing A:
  pivot_effective_time.window_start = T8
  recorded_time = R20

Swing B:
  pivot_effective_time.window_start = T15
  recorded_time = R30

Historical batch cursor: R100

Kết quả bắt buộc:
  Swing A → ELIGIBLE   (bước 2: R20 <= R100 OK; bước 3: T8 < T10 OK)
  Swing B → REJECTED   (bước 2: R30 <= R100 OK; bước 3: T15 < T10 FAIL — T15 >= T10)

→ CẢ HAI đều recorded-time visible tại cursor R100 (bước 2 pass), nhưng Swing B vẫn bị loại
  vì effective-time ineligible (bước 3 fail). Total order (dưới đây) KHÔNG BAO GIỜ chạy tới
  Swing B vì nó đã bị loại từ bước 3 — total order chỉ thấy tập {Swing A}.
```

**Correction-recorded-old-pivot — "recorded muộn hơn không có nghĩa effective muộn hơn":** một Swing revision được recorded SAU (correction) vẫn có thể eligible nếu chính revision đó thỏa cả 5 bước — cụ thể: `revised S.recorded_time <= R` VÀ `revised S.pivot_effective_time.window_start < reference_cutoff` VÀ đây là revision hợp lệ hiện tại (bước 4) VÀ không bị invalidate (bước 5). Ví dụ: một correction tới Swing A phát sinh recorded_time = R50 (sau R20 gốc) nhưng pivot vẫn `window_start = T8` (không đổi effective time) — revision mới này vẫn eligible tại cursor R100, thay thế revision cũ theo đúng correction lineage (swing.md). Ngược lại, một correction dời pivot tới `T15` (>= T10) sẽ khiến chính Swing đó chuyển từ eligible sang ineligible tại bước 3 — bất kể recorded_time của correction là gì. **"Recorded muộn hơn" và "effective muộn hơn" là hai trục độc lập** — bitemporal correctness đòi hỏi đánh giá riêng biệt, không suy luận trục này từ trục kia.

**Total order khi nhiều ứng viên ĐÃ QUA CẢ 5 BƯỚC LỌC trên vẫn thỏa cùng điều kiện — 8 tiêu chí, lexicographic nghiêm ngặt (không đổi so với v0.1, giống hệt bảng `structure.md` §6a):**

```text
1. pivot_effective_time.window_start   DESC
2. SwingConfirmed.recorded_time        ASC
3. stream_ref.stream_id                ASC (lexical)
4. stream_ref.registry_version         ASC (lexical)
5. sequence                            ASC (CHỈ trong cùng stream identity đã xác lập bởi 3+4)
6. swing_revision                      DESC
7. swing_id                            ASC (lexical)
8. SwingConfirmed.event_id             ASC (lexical)
```

So sánh tiêu chí 1 đến 8 theo đúng thứ tự; tiêu chí đầu tiên khác nhau quyết định; các tiêu chí sau KHÔNG được đánh giá; `sequence` chỉ so trong cùng stream identity — cấm so sánh xuyên stream. **Total order này CHỈ chạy trên tập đã qua filter pipeline ở trên — không bao giờ được áp dụng cho một ứng viên chưa qua bước 3 (effective-time cutoff), dù ứng viên đó thắng theo tiêu chí 1 (`pivot_effective_time.window_start DESC`).**

**Không có Eligible Swing nào tồn tại** (chưa có Swing nào qua được cả 5 bước lọc — kể cả trường hợp có Swing recorded-time visible nhưng effective-time ineligible như Swing B ở ví dụ trên): `distance_to_last_confirmed_swing` KHÔNG được compute — valid absence, không phát `FeatureComputed` (§7 warm-up/missing-input).

## 10. Feature-to-Feature dependency — deferred (B3 KHÔNG author)

**Ưu tiên: không FeatureComputed nào tiêu thụ một FeatureComputed khác** — cả ba founding feature type tính trực tiếp từ authoritative upstream domain fact (Candle/Swing/Regime), KHÔNG từ output của một Feature khác. Điều này tránh một hidden feature dependency graph ngay trong contract đầu tiên. Feature DAG, derived Feature-to-Feature composition, và bất kỳ cơ chế compose Feature-trên-Feature nào đều **deferred tường minh** (§19) — không author ở B3.

## 11. `FeatureCurrentView` — validity rules và deterministic total order

**Bước 0 — row existence precondition:** nếu `feature_subject_id` CHƯA từng có `FeatureComputed` visible tại cursor → **KHÔNG có row nào tồn tại** — `GetCurrentFeature` trả `NOT_FOUND`/`ABSENT`. Không materialize placeholder. Chỉ khi Bước 0 xác nhận có ít nhất một fact tồn tại, các bước dưới đây mới chạy — `view_state` LUÔN resolve được (VALID hoặc PENDING_CORRECTION), không có nhánh thứ ba.

**Bước 1 — xác định TARGET WINDOW trước khi loại trừ bất cứ điều gì:** target window = window có `effective_window.window_end` lớn nhất trong TOÀN BỘ tập window mà subject này đã từng có ít nhất một `FeatureComputed` visible tại cursor (KỂ CẢ nếu lineage head của window đó hiện đang invalidate). **Không được xác định target window SAU KHI đã loại trừ fact invalidate** — sẽ khiến một window mới nhất đang chờ correction bị bỏ qua âm thầm, view lùi về báo cáo một window CŨ HƠN như thể "hiện tại" (đúng bài học `regime.md` §11).

**Bước 2 — trong lineage của TARGET WINDOW đó, loại trừ:** mọi `FeatureComputed` đã bị supersede; mọi replacement mà `FeatureFactInvalidated` tương ứng CHƯA visible; mọi computation dùng ancestry chưa resolve hoặc không authoritative.

**Bước 3 — resolve view_state cho TARGET WINDOW:**

```text
lineage head của target window tồn tại VÀ KHÔNG có FeatureFactInvalidated visible  → trả về nó (view_state: VALID)
lineage head của target window có FeatureFactInvalidated visible, replacement CHƯA visible → view_state: PENDING_CORRECTION (KHÔNG lùi về window cũ hơn dù window đó vẫn VALID)
KHÔNG BAO GIỜ fallback về một giá trị đã invalidate, và KHÔNG BAO GIỜ fallback về một window cũ hơn target window chỉ vì target window đang pending
```

**Deterministic total order — 7 tiêu chí, lexicographic nghiêm ngặt:**

```text
1. effective_window.window_end   DESC
2. effective_window.window_start DESC
3. FeatureComputed.recorded_time ASC
4. stream_ref.stream_id          ASC (lexical)
5. stream_ref.registry_version   ASC (lexical)
6. sequence                      ASC (CHỈ khi 4+5 đã hòa)
7. FeatureComputed.event_id      ASC (lexical)
```

So sánh tiêu chí 1 đến 7 theo đúng thứ tự; tiêu chí đầu tiên khác nhau quyết định; các tiêu chí sau KHÔNG được đánh giá. Nếu cả bảy giá trị đều khớp, hai bản ghi là duplicate representation của cùng một authoritative fact (§8) — không có tiêu chí thứ tám.

**Canonical policy identifier — nguồn duy nhất tại §6 (`current_view_selection_policy`)** — không lặp lại chuỗi ở nơi khác trong tài liệu này.

## 12. Time semantics

```text
effective_window              — [window_start, window_end) của CHÍNH fact đó (§3) — mỗi fact có window riêng, không bất biến xuyên subject
recorded_time                  — khi Ride tính/ghi nhận fact này (bắt buộc, mọi event — envelope §2)
market_time                    — PROHIBITED (§2)
```

**Không dùng `event_time`.**

**Warm-up — valid absence, không phải null:** trước khi đủ input evidence tồn tại theo `warm_up_policy` (§6) cho một computation point ứng viên, **không** phát `FeatureComputed`.

**Missing-input (unresolved gap, hoặc không có Eligible Swing — §9a):** không compute speculative — chờ resolve, đúng `missing_input_policy` (§6).

**Historical batch/Backtest computation:** khi nạp dữ liệu lịch sử đã có đủ input cho nhiều computation point liên tiếp, engine tính TUẦN TỰ từng point theo đúng cadence đã pin — không nhảy thẳng tới point cuối cùng.

**Correction visibility:** `FeatureFactInvalidated` và replacement `FeatureComputed` đều có `recorded_time` mới; replay tại cursor trước đó chỉ thấy fact gốc — không backfill giả vờ đã biết sớm hơn thực tế.

**Input eligibility — v0.2, đóng `RA-B3-MAJ-01`/`IRB-B3-MAJ-01`: hai điều kiện ĐỘC LẬP, cả hai PHẢI đúng cho MỌI Feature input, không điều kiện nào thay thế được điều kiện kia:**

```text
(a) input.recorded_time <= computation cursor      — recorded-time visibility (đã có từ v0.1)
(b) input effective time thỏa cutoff riêng của feature_type đó, pin tại Feature Definition (§6)
```

`(a)` một mình KHÔNG đủ — một input recorded-time visible vẫn có thể effective-time ineligible (§9a ví dụ bắt buộc: Swing B). Với `distance_to_last_confirmed_swing`, `(b)` cụ thể là: `Eligible Swing.pivot_effective_time.window_start < reference Candle.effective_time.window_end` (§9a bước 3, `eligible_swing_effective_cutoff_policy`). Quy tắc chung **"không có input nào vượt quá `effective_window.window_end` hoặc replay cursor được dùng làm evidence"** PHẢI được đọc CÙNG với `(b)` — đây không phải một rule đứng riêng mơ hồ, mà tham chiếu đúng cutoff cụ thể mà Feature Definition của feature_type đó đã pin (§6/§9a cho `distance_to_last_confirmed_swing`; §7.1/§7.2 cho `volatility_metric`/`directional_persistence_metric` — evidence window chỉ dùng Candle/Regime fact có effective time không vượt quá `window_candle_count`/`upstream_source` đã pin).

## 13. No repaint và mode parity

- **`FeatureComputed` KHÔNG BAO GIỜ bị ghi đè tại chỗ** — chỉ có thể bị phủ định qua `FeatureFactInvalidated` + replacement, luôn append-only (I-3).
- **Không in-place mutation ở bất kỳ đâu** — mọi lineage member (kể cả đã bị supersede) giữ nguyên vĩnh viễn trong log.
- **Effective-time vs recorded-time tách bạch trung thực** — đúng T-vs-T+n discipline đã khóa xuyên suốt `candle.md`/`swing.md`/`structure.md`/`regime.md`.
- **Cursor-correct pending correction** — replay giữa invalidation và replacement thấy đúng `PENDING_CORRECTION` (§11), không âm thầm dùng giá trị cũ.
- **Cùng một chuỗi computation xuyên Backtest/Replay/Paper/Live** — deterministic given `(feature_definition_version, upstream causal ancestry)` — bắt buộc SINH RA đủ MỌI computation point giống nhau ở mọi mode.
- **Warm-up/missing-input deterministic** — áp dụng đồng nhất mọi mode.
- **No look-ahead qua batch recomputation — v0.2, đóng `RA-B3-MAJ-01`/`IRB-B3-MAJ-01`:** historical Backtest/Replay tại một recorded cursor MUỘN (ví dụ nạp lại toàn bộ lịch sử tại cursor R100) PHẢI reconstruct MỖI Feature fact chỉ dùng input thỏa **CẢ HAI** điều kiện tại đúng computation cursor của CHÍNH fact đó (§12): recorded-time visible VÀ effective-time eligible. Việc một Swing/Candle/Regime fact được nhìn thấy trong batch tại cursor muộn (recorded-time visible) **KHÔNG BAO GIỜ** cho phép nó "nhảy vào" một computation point SỚM HƠN mà nó effective-time ineligible tại điểm đó (§9a — Swing B trong ví dụ bắt buộc vẫn bị loại dù cursor batch là R100). Bảo đảm này ĐỘC LẬP với mode — Live/Paper/Replay/Backtest đều PHẢI cho cùng một tập Eligible Swing tại cùng một computation point, không có "batch mode advantage" nhìn thấy trước.
- **Rounding/threshold boundary deterministic** — `decimal_precision_policy` (§6) pin cùng definition version, cùng kết quả mọi mode; `value` luôn kiểu `decimal` (I-9, không float).

## 14. Input contracts — chỉ authoritative facts thực sự cần

Feature tiêu thụ **chỉ những contract mà founding feature type thực sự cần**, không hơn:

```text
candle-closed            — volatility_metric/directional_persistence_metric (path candle); distance_to_last_confirmed_swing (giá tham chiếu)
candle-corrected          — như trên, correction
swing-confirmed           — distance_to_last_confirmed_swing
swing-invalidated         — distance_to_last_confirmed_swing (correction)
regime-classified         — volatility_metric/directional_persistence_metric (path regime)
regime-fact-invalidated   — như trên, correction
```

**Không tiêu thụ:** `CandleObserved`; `CandleCurrentView`; `SwingCandidateDetected`; `SwingCurrentView`; bất kỳ Structure event nào (`BreakOfStructureDetected`/`ChangeOfCharacterDetected`/`StructureFactInvalidated`/`StructureRecomputed`) hay `StructureCurrentView`; `RegimeCurrentView`; Context projection; Strategy/Decision/Risk/Account/Execution fact nào — tất cả chưa tồn tại hoặc không thuộc phạm vi input authority của Feature ở B3.

## 15. Fan-in và Feature/Context boundary

Feature là điểm fan-in **có kiểm soát** duy nhất ở tầng phân tích (ADR-003): `Candle → Feature`, `Raw Regime → Feature`, `Swing (+ Candle) → Feature` — hợp lệ. Feature **output atomic engineered value**, KHÔNG kết hợp account/position/strategy/risk state — những thứ đó thuộc downstream (Context, chưa author).

Feature **không được author**: `MarketContextSnapshot`; kết luận multi-domain strategy-ready; trade setup; signal strength; entry/exit recommendation — bất kỳ hình thức nào của những khái niệm này vi phạm trực tiếp định nghĩa Feature (§ mở đầu tài liệu). Context (context-projection, đã đăng ký, forward-declared, chưa author) là nơi tổng hợp nhiều Feature/Structure/Regime fact thành một snapshot, theo [Chapter 7 §7.4](../constitution/07-module-taxonomy.md) (Type 2 Projection, không sở hữu business decision) — KHÔNG author ở B3.

## 16. Venue & timeframe neutrality

Cùng nguyên tắc [ADR-007](../adr/ADR-007.md)/`candle.md`/`swing.md`/`structure.md`/`regime.md`: `instrument_id`/`venue_id`/`timeframe` là scope tường minh, không hardcode giả định venue cụ thể hay timeframe "chuẩn". Hai Feature subject trên cùng instrument nhưng khác `venue_id` hoặc `timeframe` là hai subject **độc lập hoàn toàn**.

## 17. Replay/Backtest/Paper/Live parity

Cả bốn execution mode tiêu thụ đúng cùng envelope (§2) và payload (§3–§4) — pattern nạp input có thể khác theo mode (historical batch tính tuần tự, §12), nhưng domain semantic của Feature không đổi theo mode (§8b, §13).

## 18. Authority boundary

**Contract này sở hữu:** semantic tính toán cho ba founding feature type, `FeatureCurrentView` projection shape, `feature_definition_version` policy schema tối thiểu (§6), Eligible-Swing selection policy riêng của Feature (§9a), Current View total-order policy (§11). **Áp dụng, không định nghĩa lại:** event envelope ([Chapter 8 §8.2](../constitution/08-event-model.md)); ordering/replay cursor mechanics ([Chapter 5](../constitution/05-time-model.md)/[Chapter 8](../constitution/08-event-model.md)); ID opaque rule ([Chapter 6 §6.8](../constitution/06-identity-model.md)); Regime independence từ Structure ([ADR-003](../adr/ADR-003.md)); Swing/Structure/Regime semantics (`swing.md`/`structure.md`/`regime.md`); Candle observation semantics (`candle.md`). **Không sở hữu:** Context snapshot semantics (chưa author); Strategy/Decision/Risk/Account/Execution semantics (Package 0.2-C, chưa author); giá trị cụ thể của `feature_definition_version` policy (configuration/Phase 1); mọi feature type ngoài ba founding type (§19).

## 19. Ngoài phạm vi — defer

**Deferred tường minh, không author ở B3:** arbitrary user-defined expression language; Feature DAG / Feature-to-Feature dependency (§10); ML embeddings; confidence model; feature marketplace; feature persistence/storage architecture; distributed compute; caching; online/offline feature-store parity infrastructure; large indicator catalog (bất kỳ feature type nào ngoài ba founding type); account-aware feature; strategy-specific feature. Cơ chế tính `feature_subject_id` deterministic cụ thể; giá trị cụ thể cho `formula_id`/`parameters`/`decimal_precision_policy`/`warm_up_policy`/`missing_input_policy` (thuộc configuration instance, §6); cơ chế lưu trữ/versioning cụ thể của `feature_definition_version` registry (Phase 1, cùng ghi chú `swing.md`/`structure.md`/`regime.md`).

**Out of scope theo ranh giới domain (không phải "chưa làm"):** Context snapshot, trade signal, action recommendation, entry/exit setup — vi phạm trực tiếp định nghĩa Feature nếu thêm vào (§15).

## 20. Open questions ngoài phạm vi

- Khi `upstream_source: regime` cho `volatility_metric`/`directional_persistence_metric`, Feature Definition có cần cho phép một `unit`/`decimal_precision_policy` KHÁC với Regime's own `computed_metric` (yêu cầu convert), hay bắt buộc giữ nguyên? Chưa quyết ở đây — author-level ambiguity note, không phải governance-level OQ, không đóng OQ-002/OQ-003.
- `feature_definition_version` registry/lifecycle chưa có authoritative source riêng — tạm coi là Referenced Authoritative Artifact theo Chapter 8 §8.1.1 (§6), nhưng **chưa** có file/registry cụ thể nào author nó trong Package 0.2-B3. Cần quyết định khi có nhu cầu thực tế đầu tiên (đối xứng ghi chú `swing.md`/`structure.md`/`regime.md`).
- **Deferred, non-blocking (ghi chú tài liệu, không phải executable finding):** [`context-map.yaml`](./context-map.yaml) hiện mô tả `feature-engineering` (cả capability lẫn context) bằng cụm từ "Feature/Signal" (ví dụ: "...thành Feature/Signal dùng cho Strategy"). Cụm này có thể gây hiểu lầm cạnh definition tường minh ở đầu tài liệu này — **Feature KHÔNG phải trade signal** (§ mở đầu). Đây KHÔNG phải một finding cần sửa ở B3 narrow revision này (`context-map.yaml` không nằm trong phạm vi file được phép đổi của revision này) — chỉ ghi nhận như một documentation cleanup item hoãn lại cho lần cập nhật `context-map.yaml` kế tiếp.
