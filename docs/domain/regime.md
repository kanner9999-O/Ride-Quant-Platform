---
id: regime
title: Raw Regime
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

# Raw Regime

> **Vai trò của tài liệu này:** Domain Contract của Package 0.2-B2 — bắt đầu chuỗi `Candle → Raw Regime → Feature`, song song và **độc lập hoàn toàn** với chuỗi `Candle → Swing → Structure` (Package 0.2-B1), đúng [ADR-003](../adr/ADR-003.md) (Approved). Draft, chưa Approved/Locked. Thuộc capability `market-regime` / context `raw-regime-analysis` — **đã đăng ký sẵn** tại [`context-map.yaml`](./context-map.yaml) từ Package 0.2-A (forward-declared), nay authored. **v0.2** là **narrow revision** xử lý toàn bộ findings từ ChatGPT Review A + Independent Review B trên baseline v0.1 — `RA-B2-MIN-01`/`IRB-B2-MIN-03` (cùng một Current View ambiguity, xử lý bằng một correction duy nhất — no-row semantics trước fact đầu tiên, loại bỏ `UNAVAILABLE`, §5/§11), `IRB-B2-MAJ-01` (canonical Candle evidence normalization — `candle_evidence_refs` là tập toán học, không phải array thứ tự tùy ý, §8a), `IRB-B2-MAJ-02` (invalidation envelope binding — `RegimeFactInvalidated.subject_ref`/`effective_time` PHẢI kế thừa nguyên vẹn từ fact bị invalidate, không tự khai báo độc lập, §2/§4).

Raw Regime **KHÔNG phải** Structure, Feature, Context, strategy signal, market prediction, hay trade recommendation. Nó là một **phân loại thống kê, deterministic, authoritative** về điều kiện thị trường quan sát được, tính trực tiếp từ raw market-data fact (hiện tại: Candle) — không phụ thuộc diễn giải Structure (Swing/BOS/CHoCH), không tiêu thụ Feature/Context/Strategy/Account/Risk, không khuyến nghị hành động, không dự đoán giá tương lai.

Raw Regime bao gồm **bốn concept riêng biệt**:

1. **Logical Regime Subject** (`kind: entity`) — identity ổn định của "chuỗi phân loại theo một dimension này", **một subject liên tục theo scope** (giống Structure — không có subject mới per window; window chỉ là thuộc tính của từng fact, không phải identity).
2. **`RegimeClassified`** (`kind: event`) — fact authoritative cho MỘT completed valid analysis window — dùng cho cả original computation lẫn correction replacement.
3. **`RegimeFactInvalidated`** (`kind: event`) — phủ định MỘT `RegimeClassified` lịch sử cụ thể, KHÔNG tự nó tuyên bố classification mới.

Cộng một **read model tùy chọn** (`RegimeCurrentView`) — projection tiện dụng, không authoritative.

**Không mô hình hóa Regime như chuỗi state-transition class-to-class.** Mỗi completed valid analysis window sinh ra đúng một fact authoritative — kể cả khi class không đổi so với window liền trước (đóng quyết định "classification frequency" đã chốt ở vòng planning revision: "same class → no event" bị bác bỏ, xem §9). Class transition là dữ liệu **derived** (so sánh hai fact liên tiếp), không phải một event riêng.

**`regime-classified` / `regime-fact-invalidated` / `regime-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây, và đúng giá trị `contract_id` mà [`context-map.yaml`](./context-map.yaml) đã trích dẫn (candle-closed/candle-corrected → raw-regime-analysis, đã đăng ký từ Package 0.2-A). Display name, concept ID, và `event_type` là ba đại lượng khác nhau, không cạnh tranh identity — cùng nguyên tắc `candle.md`/`swing.md`/`structure.md` đã khóa.

## 1. Logical Regime Subject — `kind: entity`

```yaml
id: regime
kind: entity
capability_id: market-regime
domain_context_id: raw-regime-analysis
description: >
  Chuỗi phân loại authoritative liên tục cho MỘT regime dimension (ví dụ Volatility, hoặc
  Directional Persistence), tại một instrument/venue/timeframe, theo một Regime Definition
  Version cụ thể. Subject có identity LOGIC ổn định (`regime_subject_id`, năm field, KHÔNG
  bao gồm analysis window) — KHÔNG phải Entity không-identity. Analysis window KHÔNG phải một
  trục identity: nó định danh MỘT fact cụ thể trong chuỗi fact của subject này (§3), không
  phải subject riêng. Đây là điểm khác biệt cấu trúc bắt buộc phải nêu rõ so với `swing.md`
  (subject mới cho mỗi pivot) và giống `structure.md` (một subject liên tục theo scope) — trừ
  việc, khác Structure, Regime KHÔNG theo dõi "current classification" như một state cần
  transition: mỗi completed valid window sinh MỘT fact độc lập, current view chỉ là một QUERY
  (§11) trên chuỗi fact đó, không phải state lưu trữ riêng.
invariants:
  - "regime_subject_id resolve deterministic từ ĐÚNG NĂM field qualifying scope: instrument_id, venue_id, timeframe, regime_dimension, regime_definition_version — cùng năm-field-scope luôn cho cùng regime_subject_id; khác bất kỳ field nào trong năm field đó cho regime_subject_id KHÁC. regime_subject_id bất biến, KHÔNG tái sử dụng cho một subject khác (Chapter 6 §6.1)."
  - "regime_subject_id là opaque — domain logic KHÔNG được parse nó để suy diễn instrument/venue/timeframe/dimension/definition (Chapter 6 §6.8); mọi quyết định nghiệp vụ phải dùng field tường minh trong scope."
  - "instrument_id, venue_id, timeframe, regime_dimension, regime_definition_version bất biến sau khi subject được quan sát lần đầu — đổi bất kỳ field nào tạo ra một subject KHÁC, không phải mutate subject cũ. Đổi regime_definition_version tạo subject mới hoàn toàn — chuỗi fact cũ dưới definition cũ giữ nguyên, không bị diễn giải lại (Chapter 8 §8.1.1 Referenced Authoritative Artifact)."
  - "Analysis window (analysis_window.window_start/window_end, §3) KHÔNG thuộc identity scope của subject — nó là thuộc tính của từng RegimeClassified fact. Hai fact khác window trên cùng subject là hai fact riêng biệt của CÙNG một subject, không phải hai subject."
  - "regime_dimension là enum đóng ở v0.1: [volatility, directional_persistence] — mở rộng thêm dimension (ví dụ activity, liquidity) là một thay đổi Domain Contract tường minh (bump version), không tự phát sinh ngầm."
schema:
  regime_subject_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  instrument_id: {type: string, required: true, ref: instrument}
  venue_id: {type: string, required: true, ref: venue}
  timeframe: {type: string, required: true}
  regime_dimension: {type: enum, values: [volatility, directional_persistence], required: true}
  regime_definition_version: {type: string, required: true, description: "pin chính xác Regime Definition policy đã dùng — §6"}
state_machine:
  initial_state: UNCLASSIFIED
  states: [UNCLASSIFIED, CLASSIFIED]
  transitions:
    - {from: UNCLASSIFIED, to: CLASSIFIED, caused_by: RegimeClassified}
    - {from: CLASSIFIED, to: CLASSIFIED, caused_by: RegimeClassified}
  terminal_states: []
events_emitted: [RegimeClassified, RegimeFactInvalidated]
events_consumed: [CandleClosed, CandleCorrected]
commands: []
queries: []
```

**`UNCLASSIFIED` là notional initial state** — cùng convention `UNSEEN`/`UNDETERMINED` mà `candle.md`/`swing.md`/`structure.md` đã khóa: không event nào khẳng định "subject đang UNCLASSIFIED"; đây là điểm khởi đầu ngầm định trước khi có window nào đủ điều kiện classify (§7 warm-up).

**`CLASSIFIED → CLASSIFIED` là self-transition cho MỌI `RegimeClassified` kế tiếp** — kể cả khi class không đổi, kể cả khi đây là một correction replacement (§9). State machine ở đây chỉ mô tả "subject đã từng classify hay chưa" (existence lifecycle) — **KHÔNG** mã hóa class hiện tại là gì; class hiện tại của một window cụ thể chỉ đọc được từ chính fact đó, và "current view" tổng hợp là một **query** (§11), không phải một trường state lưu trữ. Đây là khác biệt thiết kế cố ý so với `structure.md` (nơi `current_orientation` LÀ một trường state có transition tường minh theo từng class) — Regime không có khái niệm "current_orientation" tương đương, vì mỗi window là một fact độc lập, không phải một chuỗi diễn giải phụ thuộc lẫn nhau (không có `prior_orientation`-style chain).

## 2. Canonical event envelope — áp dụng cho mọi Regime event (§3–§4)

Mọi event ở §3–§4 là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). Mục này khóa **envelope chung** một lần — từng event bên dưới chỉ khai báo **payload đặc thù**. Chapter 8 sở hữu nguyên vẹn semantic của envelope; mục này **chỉ áp dụng, không định nghĩa lại**.

```yaml
envelope:                                          # Chapter 8 §8.2.1 — cardinality nguyên văn
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2) — xem bảng dưới
  event_contract_ref: {cardinality: required}        # {contract_id, contract_version}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}             # Chapter 5 — khi Ride tính/ghi nhận fact này, KHÔNG phải effective window time
  subject_ref: {cardinality: required}               # shape canonical — xem dưới. Trên RegimeFactInvalidated (§4), PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate — không tự khai báo độc lập (đóng IRB-B2-MAJ-02).
  stream_ref: {cardinality: required}                # {stream_id, registry_version} — Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # {module_id, implementation_version, run_id} — Phase 1, chưa author
  correlation_id: {cardinality: "required khi computation thuộc một correlation flow tường minh (ví dụ một lần backfill/replay cụ thể); optional khi computation độc lập"}
  causation_refs: {cardinality: "KHÔNG BAO GIỜ rỗng cho bất kỳ Regime event nào — Regime LUÔN là derived fact từ Candle fact (+ khi là correction replacement, RegimeFactInvalidated liền trước). Xem §3–§4 cho nội dung cụ thể."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3"}
  effective_time: {cardinality: "required — semantic KHÁC NHAU theo event type (đóng IRB-B2-MAJ-02): trên RegimeClassified (§3), = analysis_window CỦA CHÍNH fact đó, KHÁC theo từng fact, KHÔNG bất biến xuyên chuỗi fact của subject (khác structure.md, nơi effective_time bất biến xuyên revision). Trên RegimeFactInvalidated (§4), = analysis_window CỦA FACT ĐANG BỊ INVALIDATE (F) — KẾ THỪA nguyên vẹn từ F, KHÔNG tự khai báo/tính toán độc lập."}
  market_time: {cardinality: "PROHIBITED — Regime là derived/computed fact, không phải quan sát trực tiếp venue; market_time chỉ hợp lệ trên event mà venue cung cấp timestamp trực tiếp (candle.md §2)."}
  source_identity: {cardinality: "PROHIBITED — Regime không có external source retry/redelivery risk (Chapter 6 §6.6 áp cho inbound external fact); dedup của Regime dùng computation identity, xem §8."}

subject_ref:                                       # shape canonical — Chapter 8 §8.2.2
  context_id: raw-regime-analysis
  subject_kind: entity
  subject_type: Regime
  subject_id: <regime_subject_id — opaque, stable, xem §1>
  scope:
    instrument_id: <string>
    venue_id: <string>
    timeframe: <string>
    regime_dimension: <volatility | directional_persistence>
    regime_definition_version: <string>

event_types:                                       # Chapter 3 §3.2 naming — tham chiếu, không định nghĩa lại quy tắc đặt tên
  RegimeClassified: REGIME_CLASSIFIED
  RegimeFactInvalidated: REGIME_FACT_INVALIDATED
```

`stream_ref`/`producer_ref` resolve từ `stream-registry.yaml`/`module-registry.yaml` — cả hai thuộc Phase 1, chưa tồn tại tại Phase 0.2, cùng nguyên tắc defer mà `candle.md`/`swing.md`/`structure.md` đã áp dụng.

**`subject_id` luôn giống nhau cho cùng năm-field scope, bất kể window nào đang được classify** — mọi `RegimeClassified`/`RegimeFactInvalidated` mô tả cùng `(instrument_id, venue_id, timeframe, regime_dimension, regime_definition_version)` PHẢI mang cùng `subject_ref.subject_id`. Event record vẫn có `event_id` riêng, bất biến, cho từng bản ghi (Chapter 6 §6.2).

## 3. `RegimeClassified` — `kind: event`

Kế thừa nguyên vẹn envelope §2. Payload đặc thù:

```yaml
id: regime-classified
kind: event
capability_id: market-regime
domain_context_id: raw-regime-analysis
description: >
  Fact AUTHORITATIVE cho MỘT completed valid analysis window — dùng cho CẢ HAI trường hợp:
  (a) original computation (window chưa từng được classify); (b) correction replacement
  (window đã có fact trước đó, nay bị Candle correction ảnh hưởng, §9). Phát sinh cho MỌI
  completed valid window, KỂ CẢ khi class không đổi so với window liền trước — đóng quyết
  định classification-frequency: window là fact identity, không phải class. Class transition
  là dữ liệu derived (so sánh hai fact liên tiếp cùng subject theo analysis_window), KHÔNG có
  event riêng cho "class changed" hay "class unchanged".
invariants:
  - "causation_refs KHÔNG BAO GIỜ rỗng: (a) original computation — PHẢI chứa toàn bộ candle_evidence_refs; (b) correction replacement — PHẢI chứa candle_evidence_refs đã cập nhật VÀ chính RegimeFactInvalidated đang được supersede."
  - "envelope.effective_time = analysis_window (interval) của CHÍNH fact này — [window_start, window_end)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của Candle fact mới nhất trong candle_evidence_refs — KHÔNG được classify trước khi đủ evidence tồn tại (§7, chống look-ahead)."
  - "payload.regime_subject_id VÀ payload.regime_dimension PHẢI khớp đúng subject_ref.subject_id VÀ subject_ref.scope.regime_dimension — trường lặp lại có chủ đích cho query tiện dụng, không phải trục identity thứ hai (cùng nguyên tắc candle.md/swing.md)."
  - "payload.regime_definition_version PHẢI khớp đúng subject_ref.scope.regime_definition_version."
  - "candle_evidence_refs PHẢI thỏa mãn CHÍNH XÁC window_candle_count đã pin ở regime_definition_version (§6) cho analysis_window đã khai — không thiếu, không thừa, không trùng lặp; mọi ref PHẢI là candle-closed hoặc candle-corrected đang authoritative, KHÔNG dùng CandleObserved provisional."
  - "candle_evidence_refs PHẢI được serialize theo đúng canonical normalized order đã định nghĩa ở §8 (đóng RA-B2-MIN-01) — KHÔNG phải thứ tự phát sinh tùy ý của computation. Hai tập evidence fact giống hệt nhau nhưng đến theo thứ tự khác nhau PHẢI cho ra cùng một `candle_evidence_refs` đã serialize, cùng một computation identity."
  - "supersedes_fact_ref VẮNG MẶT khi và chỉ khi đây là original computation cho (regime_subject_id, analysis_window) đó — CHƯA từng có RegimeClassified nào khác cho đúng cặp subject+window này (đóng correction-lineage rule 1)."
  - "supersedes_fact_ref BẮT BUỘC có mặt khi (regime_subject_id, analysis_window) đó đã có một RegimeClassified trước đó — đây là correction replacement (đóng rule 2)."
  - "supersedes_fact_ref, khi có mặt, PHẢI trỏ đúng lineage head HIỆN TẠI của (regime_subject_id, analysis_window) đó — fact CHƯA từng là supersedes_fact_ref của bất kỳ RegimeClassified nào khác (cấm fork, đóng rule 6), VÀ đã nhận đúng một RegimeFactInvalidated visible (§4) — không được trỏ tới một fact đã bị supersede trước đó (cấm nhảy cóc qua lineage, đóng rule 4/5)."
  - "Khi supersedes_fact_ref có mặt, envelope.recorded_time của fact này PHẢI muộn hơn recorded_time của RegimeFactInvalidated đang được tham chiếu gián tiếp qua fact bị supersede — replacement không được 'visible' trước invalidation của chính fact nó thay thế (đóng rule 7)."
  - "Replacement fact PHẢI dùng ĐÚNG CÙNG (regime_subject_id, analysis_window.window_start, analysis_window.window_end) với fact bị supersede — không được đổi window khi correction (đóng rule 3)."
  - "candle_evidence_refs của replacement PHẢI phản ánh Candle ancestry ĐÃ SỬA — không được giữ nguyên ref cũ đã không còn authoritative (đóng rule 8)."
payload:
  regime_subject_id: {type: string, required: true}
  regime_dimension: {type: enum, values: [volatility, directional_persistence], required: true}
  class: {type: enum, required: true, description: "enum cụ thể theo regime_dimension — xem §6"}
  computed_metric: {type: decimal, required: true, description: "giá trị số học chính xác đã sinh ra class, theo metric formula pin ở regime_definition_version (§6) — I-9: decimal, không float"}
  analysis_window:
    kind: interval
    window_start: {type: timestamp, required: true}
    window_end: {type: timestamp, required: true}
  candle_evidence_refs: {type: array, items: event_record_ref, required: true}
  regime_definition_version: {type: string, required: true}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho original computation; BẮT BUỘC cho correction replacement — xem invariants. Không thêm classification_origin enum riêng — invariant trên field này đã đủ executable, tránh field dư thừa."}
```

## 4. `RegimeFactInvalidated` — `kind: event`

Kế thừa nguyên vẹn envelope §2 — `causation_refs` không rỗng. Payload đặc thù:

```yaml
id: regime-fact-invalidated
kind: event
capability_id: market-regime
domain_context_id: raw-regime-analysis
description: >
  Phủ định MỘT RegimeClassified lịch sử cụ thể — thuần túy ghi nhận "fact này không còn hợp
  lệ", KHÔNG tự nó tuyên bố classification mới và KHÔNG tự nó mutate RegimeCurrentView (§11 tự
  resolve trạng thái PENDING_CORRECTION khi thấy event này mà chưa có replacement). Nguyên
  nhân DUY NHẤT trong B2 (khác structure.md — Regime không tiêu thụ Swing nên không có nhánh
  swing_invalidated/chained_invalidation): một CandleCorrected ảnh hưởng tới candle_evidence_refs
  của fact bị invalidate. Là event MỚI, append-only (I-3) — không mutate record gốc.
  **Envelope binding bắt buộc (đóng IRB-B2-MAJ-02):** `subject_ref` và `effective_time` của
  chính event này KHÔNG được khai báo độc lập — chúng PHẢI kế thừa nguyên vẹn từ
  `invalidated_fact_ref` (fact F đang bị invalidate), không tính toán/suy diễn riêng. Đây là
  cơ chế duy nhất ngăn một invalidation "nhắm nhầm" subject hoặc window khác với fact nó tuyên
  bố đang phủ định.
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref (F) — cùng context_id, subject_kind, subject_type, subject_id, VÀ toàn bộ scope (instrument_id, venue_id, timeframe, regime_dimension, regime_definition_version). KHÔNG được khai báo subject_ref độc lập/khác biệt. Cấm target một fact thuộc subject KHÁC — kể cả khi mọi field khác đúng nhưng regime_definition_version sai (khác subject theo §1) hoặc regime_dimension sai (khác subject theo §1)."
  - "envelope.effective_time PHẢI BẰNG HỆT analysis_window của invalidated_fact_ref (F) — [window_start, window_end) giống hệt, không sai lệch dù chỉ một trong hai biên. Cấm target một fact đúng subject nhưng SAI window."
  - "payload.invalidated_fact_ref PHẢI resolve đúng CHÍNH XÁC bản ghi event F — dùng event_record_ref (Chapter 8 §8.2.3: canonical locator + event_id verification field), không phải một mô tả gần đúng."
  - "causation_refs PHẢI trỏ: invalidated_fact_ref (RegimeClassified đang bị invalidate — bắt buộc, đúng một, PHẢI trùng chính xác payload.invalidated_fact_ref); VÀ CandleCorrected là nguyên nhân trực tiếp."
  - "invalidated_fact_ref PHẢI trỏ một RegimeClassified CHƯA từng nhận RegimeFactInvalidated khác — một fact chỉ bị invalidate đúng một lần (không invalidate trùng lặp)."
  - "Đúng một RegimeClassified có thể trỏ supersedes_fact_ref về invalidated_fact_ref này (§3 rule 6 — cấm fork) — invariant này thuộc về fact thay thế, không phải chính event này, nhưng RegimeFactInvalidated là điều kiện TIÊN QUYẾT cho một replacement hợp lệ (§3 rule 2)."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref VÀ muộn hơn recorded_time của CandleCorrected gây ra nó."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead)."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 5. `RegimeCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event — không chịu envelope §2** (§2 áp dụng cho event record; read model là derived projection — Chapter 7 §7.4 Type 2 Projection). Rebuild được từ §3–§4. Một row cho mỗi `regime_subject_id` — tức mỗi dimension có view riêng (Volatility và Directional Persistence KHÔNG gộp vào một row, đúng §1 — mỗi dimension là một subject độc lập).

**Canonical decision — no-row trước khi có fact đầu tiên (đóng RA-B2-MIN-01/IRB-B2-MIN-03):**

```text
Trước khi RegimeClassified ĐẦU TIÊN tồn tại cho một regime_subject_id:
  → KHÔNG có RegimeCurrentView row nào tồn tại
  → GetCurrentRegime trả về NOT_FOUND / ABSENT theo quy ước tầng query
  → KHÔNG materialize một row placeholder, KHÔNG có view_state giả định
```

`view_state` ở v0.2 chỉ còn **hai** giá trị — **`UNAVAILABLE` đã bị loại bỏ hoàn toàn** khỏi schema/invariants/thuật toán/prose (không còn mơ hồ giữa "row không tồn tại" và "row tồn tại với state UNAVAILABLE"): một khi subject đã CLASSIFIED (§1 — tức đã có RegimeClassified đầu tiên), luôn resolve được đúng một trong hai state dưới đây — không có nhánh thứ ba.

```yaml
id: regime-current-view
kind: read_model
capability_id: market-regime
domain_context_id: raw-regime-analysis
description: >
  Projection tiện dụng: kết quả classification "hiện tại" (window mới nhất hợp lệ) của một
  Regime subject, rebuild được từ RegimeClassified/RegimeFactInvalidated. KHÔNG authoritative
  — mọi audit/replay/parity, và mọi input cho Feature (khi được author), phải dùng
  authoritative event stream, KHÔNG dùng view này làm nguồn sự thật (I-12, Chapter 7 §7.4).
  Cursor-bounded — không có "current" ngoài một cursor cụ thể khi dùng cho bất kỳ mục đích
  decision-relevant. Selection algorithm và deterministic total order — xem §11. Row chỉ tồn
  tại SAU khi RegimeClassified đầu tiên đã visible — trước đó, không có row (không phải row
  với state đặc biệt).
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream cùng regime_definition_version đã pin, cùng implementation version (Chapter 7 §7.4 rebuild determinism) — không có state độc lập ngoài event log."
  - "KHÔNG được dùng làm input cho bất kỳ Domain Contract khác (kể cả chính regime.md) hay Decision — chỉ query/UI (Chapter 7 §7.4, Chapter 9 §9.5)."
  - "Không có view row nào tồn tại khi subject còn UNCLASSIFIED (§1) — kỳ vọng bình thường, KHÔNG phải missing-data condition. Đây KHÔNG phải view_state = UNAVAILABLE (giá trị đó không tồn tại ở v0.2) — đây là sự VẮNG MẶT của chính row đó."
  - "view_state PHẢI đúng theo §11: VALID khi lineage head của target window (window_end lớn nhất đã từng có fact) hợp lệ, không có invalidation visible; PENDING_CORRECTION khi lineage head của target window có invalidation visible nhưng replacement CHƯA visible. KHÔNG có giá trị thứ ba. KHÔNG BAO GIỜ fallback về một fact đã invalidate, và KHÔNG BAO GIỜ fallback về một window cũ hơn target window."
schema:
  regime_subject_id: {type: string, required: true}
  scope: {instrument_id: string, venue_id: string, timeframe: string, regime_dimension: string, regime_definition_version: string, required: true}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  class: {type: enum, required: false, description: "chỉ có mặt khi view_state = VALID"}
  computed_metric: {type: decimal, required: false, description: "chỉ có mặt khi view_state = VALID"}
  analysis_window: {kind: interval, required: false, description: "chỉ có mặt khi view_state = VALID"}
  lineage_head_fact_ref: {type: event_record_ref, required: false, description: "chỉ có mặt khi view_state = VALID — xem §11"}
  last_recorded_time: timestamp
queries: [GetCurrentRegime, GetRegimeHistory]
```

## 6. Classification representation — Regime Definition (pinned policy, không hardcode một trường phái)

Class + computed_metric + threshold **PHẢI pin theo `regime_definition_version`** (§1 schema) — Domain Contract này **không** chọn một công thức/ngưỡng phân tích cụ thể làm chuẩn phổ quát duy nhất, đúng tinh thần đã áp dụng cho `swing_definition`/`structure_definition`.

```yaml
regime_definition:                     # schema tối thiểu — KHÔNG khóa giá trị cụ thể
  regime_definition_version: <string>  # opaque, immutable pin — Referenced Authoritative Artifact (Chapter 8 §8.1.1)
  dimensions:
    volatility:
      window_candle_count: <integer>          # số Candle trong analysis window
      metric_formula_id: <string>              # định danh công thức tính computed_metric — KHÔNG khóa công thức cụ thể ở đây
      class_thresholds: <ordered threshold set>  # ranh giới LOW|NORMAL|HIGH|EXTREME
      threshold_comparison_policy: <strict | inclusive>
      warm_up_policy: <window_candle_count Candle liên tiếp bắt buộc trước khi classify>
      gap_policy: <xử lý CandleDataGapObserved trong window — §7>
      decimal_precision_policy: <rounding mode + số chữ số thập phân>
    directional_persistence:
      window_candle_count: <integer>
      metric_formula_id: <string>
      class_thresholds: <ordered threshold set>  # ranh giới NON_DIRECTIONAL|DIRECTIONAL|TRANSITIONAL
      threshold_comparison_policy: <strict | inclusive>
      warm_up_policy: <...>
      gap_policy: <...>
      decimal_precision_policy: <...>
  current_view_selection_policy: analysis_window_end_desc_then_window_start_desc_then_recorded_time_asc_then_stream_id_asc_then_registry_version_asc_then_sequence_asc_then_event_id_asc   # §11, canonical duy nhất
  candle_evidence_normalization_policy: window_start_asc_then_window_end_asc_then_stream_id_asc_then_registry_version_asc_then_sequence_asc_then_event_id_asc   # §8a, canonical duy nhất (đóng RA-B2-MIN-01)
```

**Candidate class enum (v0.1, đóng dưới `class_thresholds` của từng dimension — không hardcode giá trị ngưỡng, chỉ khóa tập nhãn):**

```text
volatility:              LOW | NORMAL | HIGH | EXTREME
directional_persistence: NON_DIRECTIONAL | DIRECTIONAL | TRANSITIONAL
```

Mỗi enum PHẢI mutually exclusive và executable dưới definition đã pin — không có nhánh "không xác định" ngầm ngoài warm-up/valid-absence (§7).

**`directional_persistence` KHÔNG được mã hóa Bullish/Bearish orientation** — đây là điểm khác biệt bắt buộc phải nêu tường minh so với `structure.md`'s `current_orientation` (`BULLISH`/`BEARISH`/`NEUTRAL`): Structure orientation là kết luận **rời rạc** suy ra từ chuỗi Swing pivot break đã CONFIRMED (một mô hình price-action cụ thể); Directional Persistence Regime là một **đo lường thống kê liên tục** về việc chuyển động giá gần đây có tính chất trending hay mean-reverting, hoàn toàn độc lập với bất kỳ Swing/break event nào. Hai đại lượng này **được phép mâu thuẫn tại cùng một thời điểm** (ví dụ: Regime đọc `DIRECTIONAL` trong khi Structure vẫn `NEUTRAL` vì chưa có BOS confirmed; hoặc Structure `BULLISH` trong khi Regime đọc `TRANSITIONAL` vì đường đi choppy) — đây KHÔNG phải lỗi, mà là bằng chứng hai contract đang đo hai đại lượng khác nhau đúng như ADR-003 yêu cầu.

**Không có confidence score hay ML model ở B2** — chỉ threshold-based deterministic classification, `computed_metric` luôn được expose tường minh làm evidence, tránh rủi ro "non-explainable model output".

## 7. Time semantics

```text
analysis_window               — [window_start, window_end) của CHÍNH fact đó (§3) — mỗi fact có window riêng, không bất biến xuyên subject
recorded_time                  — khi Ride tính/ghi nhận fact này (bắt buộc, mọi event — envelope §2)
market_time                    — PROHIBITED (§2) — Regime không phải quan sát venue trực tiếp
```

**Không dùng `event_time`** (loại bỏ khỏi Constitution — Chapter 5).

**Warm-up — valid absence, không phải null:** trước khi đủ `window_candle_count` Candle CLOSED authoritative liên tiếp tồn tại cho một window ứng viên, **không** phát `RegimeClassified` — đây là valid absence (kỳ vọng bình thường), không phải missing-data condition.

**Incomplete window (data gap):** nếu một `CandleDataGapObserved` tồn tại cho một cửa sổ Candle cần thiết trong analysis window, **không** classify speculative qua gap — chờ gap resolve bằng `CandleClosed` authoritative, đúng chính sách `gap_policy` đã pin (§6). Đối xứng nguyên tắc `swing.md` §11.

**Historical batch/Backtest computation:** khi nạp dữ liệu lịch sử đã có đủ Candle cho nhiều window liên tiếp, engine tính TUẦN TỰ từng window theo đúng cadence Candle-count đã pin — **không** được nhảy thẳng tới window cuối cùng và bỏ qua các window trung gian mà lẽ ra đã completed valid theo đúng cadence đó (điều này sẽ vi phạm §9 classification-frequency: mỗi window completed valid PHẢI có fact riêng, kể cả trong historical ingestion).

**Correction visibility:** `RegimeFactInvalidated` và replacement `RegimeClassified` đều có `recorded_time` mới; replay tại cursor trước đó chỉ thấy fact gốc — không có backfill giả vờ đã biết sớm hơn thực tế.

**Không có Candle nào vượt quá `analysis_window.window_end` hoặc replay cursor được dùng làm evidence** — hệ quả trực tiếp của `candle_evidence_refs` invariant (§3) và cursor visibility.

## 8. Fact identity và deduplication

### 8a. Canonical Candle evidence normalization (đóng RA-B2-MIN-01)

**Vấn đề:** `candle_evidence_refs` biểu diễn như một array, nhưng computation identity coi nó như một **tập hợp toán học** (mathematical set). Không normalize, `[C1, C2, C3]` và `[C3, C1, C2]` — cùng một tập evidence facts, khác thứ tự đến — có thể sinh ra hai serialized identity khác nhau hoặc hai kết quả dedup khác nhau. Đây là lỗi.

**Định nghĩa bắt buộc:** `candle_evidence_refs` PHẢI:

- chứa các authoritative Candle event reference **duy nhất** (không trùng lặp — hai reference cùng resolve một Candle fact chỉ giữ đúng một);
- chứa **CHÍNH XÁC** `window_candle_count` phần tử (đã pin ở §6);
- được **normalize vào một canonical order duy nhất, deterministic** TRƯỚC khi: xây dựng computation identity; hashing; so sánh bằng nhau (equality); dedup; serialize event (bất kỳ đâu cần canonical serialization).

**Canonical order (6 tiêu chí):**

| # | Tiêu chí | Hướng |
|---|---|---|
| 1 | Candle `effective_time.window_start` | **ASC** |
| 2 | Candle `effective_time.window_end` | **ASC** |
| 3 | `stream_ref.stream_id` | **ASC**, lexical |
| 4 | `stream_ref.registry_version` | **ASC**, lexical |
| 5 | `sequence` | **ASC** — CHỈ khi (3) VÀ (4) đã hòa |
| 6 | `event_id` | **ASC**, lexical |

**Thuật toán chuẩn (normative, cùng nguyên tắc lexicographic đã khóa ở §11 — không lặp lại lỗi "bỏ qua tiêu chí, nhảy tới tiêu chí khác" của `structure.md`'s IRB-FD-STR-MAJ-01):**

```text
So sánh tiêu chí 1 đến 6 theo đúng thứ tự.
Tiêu chí ĐẦU TIÊN có giá trị khác nhau quyết định thứ tự.
Các tiêu chí sau đó KHÔNG được đánh giá.
```

`sequence` (tiêu chí 5) chỉ được đánh giá khi CẢ `stream_ref.stream_id` (3) VÀ `stream_ref.registry_version` (4) đều bằng nhau — **cấm tuyệt đối** so sánh `sequence` thô giữa hai stream identity khác nhau như một global order ([Chapter 8 §8.3.3](../constitution/08-event-model.md)).

**Nếu cả sáu giá trị đều khớp giữa hai reference, chúng là duplicate representation của cùng một authoritative Candle fact — chỉ giữ đúng MỘT canonical reference** (loại bỏ trùng lặp trước khi đếm `window_candle_count`).

**Danh sách đã normalize LÀ tập evidence toán học:**

```text
same evidence facts, khác thứ tự đến (incoming order)
→ same normalized evidence list
→ same computation identity
```

**Canonical policy identifier — nguồn duy nhất tại §6, đóng RA-B2-MIN-01 (không lặp lại chuỗi ở đây — cùng bài học `structure.md`'s IRB-FD-STR-MIN-01: một canonical string chỉ được khai báo ĐÚNG MỘT NƠI, mọi chỗ khác chỉ tham chiếu theo tên field `candle_evidence_normalization_policy`, tránh hai bản có thể lệch nhau theo thời gian).**

### 8b. Computation identity và dedup

Computation identity cho một `RegimeClassified`:

```text
(regime_subject_id,
 analysis_window.window_start,
 analysis_window.window_end,
 regime_definition_version,
 candle_evidence_refs ĐÃ NORMALIZE theo §8a)
```

**`class` và `computed_metric` là KẾT QUẢ, KHÔNG phải một phần identity** — hai computation với cùng input tuple trên PHẢI cho cùng kết quả (determinism), nhưng identity được xác lập bởi input tuple (đã normalize), không phải output.

**Dedup rule:**

```text
same regime_subject_id
same analysis window (window_start, window_end)
same regime_definition_version
same normalized candle_evidence_refs (§8a)
→ duplicate delivery → KHÔNG append event authoritative thứ hai
```

**Một window khác KHÔNG BAO GIỜ là duplicate chỉ vì class giống window trước** — khác `window_start`/`window_end` (và do đó khác `candle_evidence_refs`) đã đủ để là một fact riêng biệt, bất kể `class` bằng nhau (đóng quyết định classification-frequency, §9 dưới).

**Same window computation delivered twice** (re-run sau restart, hoặc Live/Backtest/Replay tính độc lập trên cùng input, có thể trả evidence theo thứ tự khác nhau): với cùng `regime_definition_version` và cùng Candle causal ancestry, computation PHẢI cho ra cùng `regime_subject_id`, cùng `analysis_window`, cùng `candle_evidence_refs` normalized, và cùng kết quả — đây là điều kiện dedup; recomputation là **idempotent**, không phải nguồn tạo duplicate, **bất kể thứ tự evidence đến ban đầu**.

**Out-of-order Candle correction:** không được xử lý một `CandleCorrected` trước khi `CandleClosed` (hoặc `CandleCorrected` trước) mà nó sửa đã được apply — đúng causal precedence bắt buộc của [Chapter 8 §8.3.4](../constitution/08-event-model.md).

**Deterministic replay (mode parity):** với cùng `regime_definition_version` và cùng input Candle causal ancestry, Live/Backtest/Paper Trading/Replay PHẢI cho ra cùng tập fact, **cùng `candle_evidence_refs` normalized** — nền tảng bắt buộc để downstream Feature/Decision (khi trở thành decision-relevant) thỏa [I-2 Decision Parity](../constitution/02-platform-invariants.md).

## 9. Classification frequency — một fact cho MỖI completed valid window (đóng quyết định planning revision)

**MỘT `RegimeClassified` PHẢI phát sinh cho MỖI completed valid analysis window** — kể cả khi class không đổi so với window liền trước. Ví dụ:

```text
W1 → HIGH
W2 → HIGH
W3 → HIGH
```

phải sinh **ba fact riêng biệt**, vì:

- mỗi fact có `effective` window khác nhau;
- mỗi fact có Candle evidence set khác nhau;
- Feature và Replay cần một fact visible tại đúng cursor đó, không phải "kế thừa" fact từ window trước;
- một Candle correction sau này phải nhắm đúng vào fact của window bị ảnh hưởng — không có target chính xác nếu window trung gian không có fact riêng;
- evidence hiện tại không được phép "đứng yên" tại một window cũ khi đã có window mới hợp lệ hơn.

**Class transition là dữ liệu derived** — so sánh `class` của hai fact liên tiếp cùng `regime_subject_id` (theo `analysis_window` thứ tự) — **không có event riêng** cho "class changed"/"class unchanged". Dedup (§8) chỉ áp dụng cho literal duplicate computation của CÙNG một window, không bao giờ áp dụng chỉ vì class trùng.

## 10. Correction lineage

Correction lineage scoped chính xác theo `(regime_subject_id, analysis_window.window_start, analysis_window.window_end)` — mỗi window có chuỗi lineage RIÊNG, độc lập với mọi window khác trên cùng subject.

**Không có shortcut khi class không đổi:** nếu `CandleCorrected` ảnh hưởng `candle_evidence_refs` của một fact, cặp `RegimeFactInvalidated` + replacement `RegimeClassified` **PHẢI** phát sinh — **kể cả khi `computed_metric` thay đổi nhưng `class` kết quả giữ nguyên**, và **kể cả khi cả `computed_metric` lẫn `class` cuối cùng đều giữ nguyên sau khi tính lại**. Không được "bỏ qua" correction chỉ vì kết luận bề ngoài không đổi — evidence (chính xác Candle nào tạo ra kết luận đó) phải luôn trung thực và truy vết được (I-1 Explainability); một fact còn trỏ tới Candle ancestry đã không còn authoritative là vi phạm append-only integrity dù kết luận cuối có trùng hay không.

**Luồng bắt buộc:**

```text
RegimeClassified F1
  → RegimeFactInvalidated targeting F1
  → replacement RegimeClassified F2, supersedes_fact_ref = F1

Correction tiếp theo:
F2
  → RegimeFactInvalidated targeting F2
  → F3, supersedes_fact_ref = F2   (KHÔNG được supersedes_fact_ref = F1 — cấm nhảy cóc)
```

**Mười invariant bắt buộc** (đã pin tại §3/§4, tổng hợp lại đây cho rõ ràng):

1. Original fact không có `supersedes_fact_ref`.
2. Replacement fact bắt buộc có `supersedes_fact_ref`.
3. Replacement dùng đúng cùng subject và cùng `analysis_window`.
4. Replacement PHẢI supersede đúng lineage head hiện tại — không target một fact đã bị supersede.
5. Replacement không được nhảy cóc qua một head trung gian (hệ quả trực tiếp của #4).
6. Một fact bị invalidate có **tối đa một** replacement authoritative trực tiếp — cấm fork.
7. Replacement không được "visible" (`recorded_time`) trước invalidation tương ứng của nó.
8. Replacement pin Candle ancestry ĐÃ SỬA — không giữ ref cũ không còn authoritative.
9. Mọi lineage member lịch sử giữ nguyên trong log — append-only (I-3), không mutate.
10. Một fact đã invalidate **không bao giờ** bị tái sử dụng ngầm — `RegimeCurrentView` (§5, §11) phải loại trừ nó tường minh.

**Một Candle correction có thể ảnh hưởng NHIỀU window overlapping cùng lúc** (rolling window: một Candle có thể nằm trong evidence set của nhiều window liên tiếp). Với MỖI fact bị ảnh hưởng:

```text
invalidate đúng fact đó → phát replacement ĐỘC LẬP cho đúng window đó
```

**KHÔNG có dependency-forward ordering giữa các window độc lập** — khác `structure.md` §10 (nơi cascade cần traversal vì các fact CHAIN vào nhau qua `prior_orientation`), các `RegimeClassified` của các window KHÁC NHAU không phụ thuộc kết luận của nhau — chỉ CÓ THỂ chia sẻ một phần Candle evidence overlap. Correction cho window A và window B (cả hai bị cùng một `CandleCorrected` ảnh hưởng) được xử lý **độc lập, thứ tự bất kỳ** — đây là một đơn giản hóa thực sự so với Structure, không phải một thiếu sót.

## 11. `RegimeCurrentView` — validity rules và deterministic total order

**Bước 0 — row existence precondition (đóng RA-B2-MIN-01/IRB-B2-MIN-03, thay thế hoàn toàn `UNAVAILABLE`):** nếu `regime_subject_id` CHƯA từng có `RegimeClassified` visible tại cursor → **KHÔNG có row nào tồn tại** — không phải "row với `view_state = UNAVAILABLE`". `GetCurrentRegime` trả về `NOT_FOUND`/`ABSENT` theo quy ước tầng query. **Không materialize một row placeholder, không phát sinh một classification giả định.** Chỉ khi Bước 0 đã xác nhận có ít nhất một fact tồn tại, các bước dưới đây mới chạy — sau điểm này, `view_state` LUÔN resolve được (VALID hoặc PENDING_CORRECTION), không có nhánh "không xác định" nào còn sót lại.

**Bước 1 — xác định TARGET WINDOW trước khi loại trừ bất cứ điều gì:** target window = window có `analysis_window.window_end` lớn nhất trong TOÀN BỘ tập window mà subject này đã từng có ít nhất một `RegimeClassified` visible tại cursor (KỂ CẢ nếu lineage head của window đó hiện đang invalidate). **Không được xác định target window SAU KHI đã loại trừ fact invalidate** — làm vậy sẽ khiến một window mới nhất đang chờ correction bị bỏ qua âm thầm, và view lùi về báo cáo một window CŨ HƠN như thể nó là "hiện tại" (đóng attack scenario "latest window pending while previous window remains valid" — window cũ hơn valid không bao giờ được dùng để che giấu việc window mới nhất đang pending).

**Bước 2 — trong lineage của TARGET WINDOW đó, loại trừ:**

- mọi `RegimeClassified` đã bị supersede (tức là đã là `supersedes_fact_ref` của một fact khác trong cùng lineage);
- mọi replacement mà `RegimeFactInvalidated` tương ứng của nó CHƯA visible tại cursor (integrity — không có replacement "mồ côi");
- mọi classification dùng Candle ancestry chưa resolve hoặc không authoritative.

**Bước 3 — resolve view_state cho TARGET WINDOW (không phải cho một window cũ hơn; chỉ hai giá trị khả dĩ, vì Bước 0 đã đảm bảo tồn tại ít nhất một fact):**

```text
lineage head của target window tồn tại VÀ KHÔNG có RegimeFactInvalidated visible  → trả về nó (view_state: VALID)
lineage head của target window có RegimeFactInvalidated visible, replacement CHƯA visible → view_state: PENDING_CORRECTION (KHÔNG lùi về window cũ hơn dù window đó vẫn VALID)
KHÔNG BAO GIỜ fallback về một giá trị đã invalidate, và KHÔNG BAO GIỜ fallback về một window cũ hơn target window chỉ vì target window đang pending
```

**Deterministic total order** — dùng khi cần chọn giữa nhiều ứng viên (ví dụ xác định "window hiệu lực mới nhất" hoặc phân giải duplicate representation):

| # | Tiêu chí | Hướng |
|---|---|---|
| 1 | `analysis_window.window_end` | **DESC** |
| 2 | `analysis_window.window_start` | **DESC** |
| 3 | `RegimeClassified.recorded_time` | **ASC** |
| 4 | `stream_ref.stream_id` | **ASC**, lexical |
| 5 | `stream_ref.registry_version` | **ASC**, lexical |
| 6 | `sequence` | **ASC** — CHỈ khi (4) VÀ (5) đã hòa |
| 7 | `RegimeClassified.event_id` | **ASC**, lexical |

**Thuật toán chuẩn (normative, đúng nguyên tắc lexicographic đã khóa lại ở `structure.md` v0.4 sau IRB-FD-STR-MAJ-01 — áp dụng ngay từ v0.1 tại đây, không lặp lại lỗi):**

```text
So sánh tiêu chí 1 đến 7 theo đúng thứ tự.
Tiêu chí ĐẦU TIÊN có giá trị khác nhau quyết định ứng viên thắng.
Các tiêu chí sau đó KHÔNG được đánh giá.
```

- Nếu tiêu chí (4) khác nhau → (4) quyết định, **dừng tại đây** — (5)-(7) KHÔNG được đánh giá.
- Nếu (4) hòa nhưng (5) khác nhau → (5) quyết định, **dừng tại đây** — (6)-(7) KHÔNG được đánh giá.
- **CHỈ khi cả (4) VÀ (5) đều hòa**, tiêu chí (6) `sequence` mới được đánh giá.
- **Cấm tuyệt đối** so sánh `sequence` thô giữa hai stream khác nhau như một global order ([Chapter 8 §8.3.3](../constitution/08-event-model.md), [ADR-009](../adr/ADR-009.md)).
- Nếu cả bảy giá trị đều khớp, hai bản ghi là **duplicate representation của cùng một authoritative fact** (§8) — không có tiêu chí thứ tám.

**Canonical policy identifier — nguồn duy nhất tại §6 (không lặp lại chuỗi ở đây — tham chiếu theo tên field `current_view_selection_policy`).** Đúng MỘT canonical identifier tồn tại xuyên suốt tài liệu này.

## 12. No repaint và mode parity

- **`RegimeClassified` KHÔNG BAO GIỜ bị ghi đè tại chỗ** — một khi phát sinh, chỉ có thể bị phủ định qua `RegimeFactInvalidated` + replacement, luôn append-only (I-3).
- **Không in-place mutation ở bất kỳ đâu** — mọi lineage member (kể cả đã bị supersede) giữ nguyên vĩnh viễn trong log.
- **Append-only invalidation và replacement** — đúng §10, mọi correction là fact mới, không xóa/sửa fact cũ.
- **Effective-time vs recorded-time tách bạch trung thực** — `analysis_window` (effective) không bao giờ bị nhầm với thời điểm Ride thực sự biết fact đó (`recorded_time`), đúng T-vs-T+n discipline đã khóa xuyên suốt `candle.md`/`swing.md`/`structure.md`.
- **Cursor-correct pending correction** — replay giữa invalidation và replacement thấy đúng trạng thái "đang chờ" (`PENDING_CORRECTION`, §11), không âm thầm dùng giá trị cũ.
- **Cùng một chuỗi classification xuyên Backtest/Replay/Paper/Live** — deterministic given `(regime_definition_version, Candle causal ancestry)` — bắt buộc SINH RA đủ MỌI window fact giống nhau ở mọi mode, không chỉ các điểm class-change (hệ quả trực tiếp của §9).
- **Warm-up deterministic** — đúng `window_candle_count` từ `regime_definition_version`, áp dụng đồng nhất mọi mode.
- **Missing-data deterministic** — `gap_policy` áp dụng đồng nhất mọi mode, không có nhánh riêng cho mode nào.
- **Rounding/threshold boundary deterministic** — `decimal_precision_policy` và `threshold_comparison_policy` (§6) pin cùng definition version, cùng kết quả mọi mode; `computed_metric` luôn kiểu `decimal` (I-9, không float).

## 13. Input contracts — chỉ authoritative Candle facts

Raw Regime tiêu thụ **chính xác hai** contract từ `market-data-observation`:

```text
candle-closed
candle-corrected
```

**Không tiêu thụ:** `CandleObserved` (provisional — cùng nguyên tắc `swing.md` §13); `CandleCurrentView` (non-authoritative read model); `Swing`/`Structure` (ADR-003 — độc lập hoàn toàn); `RegimeCurrentView` của chính nó (không tự tham chiếu read model làm authoritative input); `Feature`/`Context`/`Strategy`/`Account`/`Risk` (chưa tồn tại, và về nguyên tắc không thuộc phạm vi input của Raw Regime — §14/§15).

**B2 first-authored scope vs future Raw Regime capabilities:** chỉ Candle facts hiện có authoritative trong repository ngay bây giờ được dùng. Dimension nào cần Trade/Quote/Order-book fact (Liquidity, §"Regime dimensions") **KHÔNG** được author cho tới khi các contract đó tồn tại — tránh trích dẫn `contract_id` cho một artifact chưa tồn tại, đúng nguyên tắc `context-map.yaml` đã tự khóa.

## 14. Feature boundary

`computed_metric` trong payload `RegimeClassified` là **evidence nội bộ** phục vụ giải thích chính class đó (I-1 Explainability) — **không** tự động trở thành một Feature tái sử dụng được. Một giá trị vượt biên sang Feature khi: (a) một consumer khác (ngoài chính việc giải thích Regime) cần giá trị số học đó độc lập với kết luận classification; hoặc (b) cùng một phép tính cần lặp lại cho nhiều mục đích khác nhau ngoài Regime. `regime.md` **không** tự quyết định biên này cho tương lai — Feature Domain Contract (Package 0.2-B, chưa author) sẽ quyết định khi có nhu cầu thực tế; `regime.md` chỉ giữ `computed_metric` đúng phạm vi "bằng chứng cho classification này", không publish như một Feature riêng.

## 15. Context boundary

Raw Regime **không** kết hợp: Structure; account state; strategy state; risk state; session-specific trading intent; hay bất kỳ domain interpretation nào khác — đã được đảm bảo cấu trúc bởi input authority (§13, chỉ Candle) và identity model (§1, không có field account/strategy/session). Quan hệ tương lai:

```text
Raw Regime + Structure + Feature → Context / Structure-aware Regime
```

`context-projection` (đã đăng ký, forward-declared, chưa author) là nơi kết hợp này diễn ra sau này, theo [Chapter 7 §7.4](../constitution/07-module-taxonomy.md) (Type 2 Projection, không sở hữu business decision). **"Structure-aware Regime" là một concept TƯƠNG LAI khác, KHÔNG phải phần mở rộng của `regime.md`** — `regime.md` chỉ và luôn chỉ là Raw Regime.

## 16. Venue & timeframe neutrality

Cùng nguyên tắc [ADR-007](../adr/ADR-007.md)/`candle.md` §14/`swing.md` §14: `instrument_id`/`venue_id`/`timeframe` là scope tường minh, không hardcode giả định venue cụ thể hay timeframe "chuẩn". Hai Regime subject trên cùng instrument nhưng khác `venue_id` hoặc `timeframe` là hai subject **độc lập hoàn toàn**, không chia sẻ state. Session/activity state KHÔNG được Regime tự định nghĩa lại — thuộc `instrument-venue-reference` (chưa author) nếu cần trong tương lai (đúng ranh giới `candle.md` §12 đã khóa cho "Venue/session hợp lệ đóng").

## 17. Replay/Backtest/Paper/Live parity

Cả bốn execution mode tiêu thụ đúng cùng envelope (§2) và payload (§3–§4) — pattern nạp Candle có thể khác theo mode (historical batch tính tuần tự từng window, §7), nhưng domain semantic của Regime không đổi theo mode (§8, §12).

## 18. Authority boundary

**Contract này sở hữu:** Raw Regime classification/invalidation semantics cho Volatility và Directional Persistence, `RegimeCurrentView` projection shape, `regime_definition_version` policy schema tối thiểu (§6), Current View total-order policy (§11). **Áp dụng, không định nghĩa lại:** event envelope ([Chapter 8 §8.2](../constitution/08-event-model.md)); ordering/replay cursor mechanics ([Chapter 5](../constitution/05-time-model.md)/[Chapter 8](../constitution/08-event-model.md)); ID opaque rule ([Chapter 6 §6.8](../constitution/06-identity-model.md)); Regime independence từ Structure ([ADR-003](../adr/ADR-003.md)). **Không sở hữu:** Candle observation semantics (`candle.md`); Swing/Structure semantics (`swing.md`/`structure.md`); Instrument/Venue identity (`instrument-venue-reference`, chưa author); Feature fan-in logic (Package 0.2-B, chưa author — Regime chỉ publish, không định nghĩa consumer); giá trị cụ thể của `regime_definition_version` policy (configuration/Phase 1, không phải Domain Contract); Activity/Volume, Liquidity, Data-quality, hay Structure-aware Regime semantics (ngoài phạm vi B2 — §19).

## 19. Ngoài phạm vi — defer

**Deferred (có thể mở rộng sau, không blocked về mặt kiến trúc):** Activity/Volume regime dimension — tính được từ Candle volume field, nhưng vượt phạm vi tối thiểu B2 đã chốt (chỉ Volatility + Directional Persistence, đúng ADR-003's founding text). Cơ chế tính `regime_subject_id` deterministic cụ thể (content hash hay tương đương); giá trị cụ thể cho `window_candle_count`/`metric_formula_id`/`class_thresholds`/`threshold_comparison_policy`/`gap_policy`/`decimal_precision_policy` (thuộc configuration instance, §6, không phải Domain Contract); cơ chế lưu trữ/versioning cụ thể của `regime_definition_version` registry (Phase 1, cùng ghi chú `swing.md`/`structure.md`).

**Out of scope (blocked về cấu trúc hoặc về ranh giới domain, không phải "chưa làm"):** Liquidity regime dimension — Candle OHLCV không capture depth/spread; cần Trade/Quote/Order-book contract chưa tồn tại (§13). Data-quality regime — thuộc `candle.md` §12 (`data_quality`, `CandleDataGapObserved`) và operational/data-health concern, không phải market-condition classification — KHÔNG được thêm vào `regime.md` dưới bất kỳ hình thức nào. Session/activity state — thuộc `instrument-venue-reference`. Structure-aware Regime — concept tương lai khác, không phải phần mở rộng của contract này (§15). Strategy signal, market prediction, trade recommendation — vi phạm trực tiếp định nghĩa Raw Regime (§ mở đầu tài liệu) nếu được thêm vào.

## 20. Open questions ngoài phạm vi

- Liệu Strategy/Decision có được tiêu thụ `regime-classified` trực tiếp, bypass Feature Engine, hay Feature luôn phải là điểm fan-in duy nhất (đúng cách đọc chặt của ADR-003 "Feature Engine... là điểm fan-in duy nhất")? Không quyết ở đây — author-level ambiguity note, không phải governance-level OQ, không đóng OQ-002/OQ-003.
- `regime_definition_version` registry/lifecycle (nơi pin `window_candle_count`/`metric_formula_id`/`class_thresholds`/... cụ thể) chưa có authoritative source riêng — tạm coi là Referenced Authoritative Artifact theo Chapter 8 §8.1.1 (§6), nhưng **chưa** có file/registry cụ thể nào author nó trong Package 0.2-B2. Cần quyết định khi có nhu cầu thực tế đầu tiên (đối xứng ghi chú `swing.md` §18/`structure.md` §17).
