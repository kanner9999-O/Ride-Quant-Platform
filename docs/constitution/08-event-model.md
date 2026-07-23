---
id: 08-event-model
title: Event Model
version: "2.7"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-18"
next_review: null
depends_on: ["02-platform-invariants", "03-engineering-principles", "05-time-model", "06-identity-model", "07-module-taxonomy"]
---

# 8. Event Model

> **⚠️ Ràng buộc trước khi Lock:** §8.3 (OQ-005) và §8.4 (OQ-006) là **đề xuất, CHƯA được Product Owner quyết**. Cả hai thuộc diện **ADR Required** ([Governance §4b](./00-governance.md)). Chapter 8 KHÔNG được Lock cho tới khi Product Owner chốt và ADR tương ứng được ghi.

## 8.1 Authoritative source — event log, KHÔNG phải transport

**Durable append-only event log** là authoritative source cho **runtime facts và decision history** ([I-12](./02-platform-invariants.md)). Transport/broker cụ thể (Redpanda, Kafka, hay công nghệ thay thế sau này) **KHÔNG** tự thân là source of truth — đổi transport không làm thay đổi authority.

Event log KHÔNG phải "nguồn sự thật duy nhất của toàn platform": theo I-12, mỗi concept có authoritative source riêng (document status → `MANIFEST.md`; architecture decision → ADR; domain concept → Domain Contract; platform rule → Constitution).

### 8.1.1 Quy tắc chung cho mọi Referenced Authoritative Artifact

Chapter này giới thiệu nhiều artifact được **event hoặc cursor tham chiếu** (Stream Registry, Event Contract, Input Contract, và bất kỳ artifact nào thêm sau này). **Mọi artifact thuộc loại đó — hiện tại và tương lai — bắt buộc thỏa 5 điều kiện sau**, không cần lặp lại ở từng mục:

1. **Versioned** — mọi thay đổi tạo version mới, không sửa tại chỗ.
2. **Immutable sau khi được tham chiếu** — một khi có authoritative event, Decision, replay run, hoặc cursor trỏ tới version nào, version đó bất biến vĩnh viễn.
3. **Không tái sử dụng identifier** — version identifier đã dùng không được gán lại cho nội dung khác.
4. **Persistently resolvable** — phải resolve được trong toàn bộ **replay/audit horizon mà platform cam kết**. Hết horizon phải có **explicit retention/archive policy**; không được mất artifact ngoài ý muốn. *(Phân biệt với điều 2: nội dung **bất biến vĩnh viễn** — không bao giờ được sửa; nhưng khả năng **truy xuất** được cam kết theo horizon, không phải vô hạn vô điều kiện.)*
5. **Verifiable content identity** — phải truy được tới immutable content identity (commit SHA, content hash, hoặc tương đương). Bắt buộc là *verifiability*, không phải một field cụ thể; identity có thể nằm ở run manifest thay vì lặp trên mọi event.

*Lý do đặt thành quy tắc chung: pin một identifier nhưng nội dung sau identifier đó vẫn sửa được thì **không thực sự là pin** — historical meaning của mọi reference sẽ đổi ngầm, phá deterministic replay, Decision Parity, audit, và I-12. Quy tắc này áp dụng tự động cho artifact mới, không chờ phát hiện từng cái một.*

## 8.2 Event Envelope

**Phân chia thẩm quyền:** Chapter 8 sở hữu **envelope (metadata)**; **Event Contract** của từng `event_type` sở hữu **payload schema/semantic**; [Chapter 10](./10-compatibility-capability-contract.md) sở hữu **compatibility/version rules**. Chapter 8 KHÔNG định nghĩa payload của bất kỳ domain event cụ thể nào.

```yaml
metadata:            # Chapter 8 sở hữu
  event_id:
  event_type:
  event_contract_ref: {contract_id, contract_version}
  schema_version:
  subject_ref: {...}
  recorded_time:
  stream_ref: {stream_id, registry_version}
  sequence:
  ...
payload:             # Event Contract của event_type sở hữu
  ...
```

### 8.2.1 Cardinality của từng field

| Field | Cardinality | Rule |
|---|---|---|
| `event_id` | **Required** | Mọi event record (§6.2) |
| `event_type` | **Required** | Naming theo [Chapter 3 §3.2](./03-engineering-principles.md) |
| `event_contract_ref` | **Required** | Qualified `{contract_id, contract_version}` — pin đúng immutable Event Contract snapshot đã áp dụng (§8.2.5) |
| `schema_version` | **Required** | Version của **payload schema** cho compatibility. Mọi authoritative event record (kể cả event nội bộ không qua public bus — vẫn cần cho replay/migration). Quy tắc tương thích do Chapter 10 sở hữu |
| `recorded_time` | **Required** | Mọi authoritative event ([Chapter 5](./05-time-model.md)) |
| `subject_ref` | **Required** | Polymorphic + qualified (xem 8.2.2) |
| `stream_ref` | **Required** | Qualified `{stream_id, registry_version}` — event phải tự đủ để resolve stream definition đã áp dụng lúc append (§8.3.1) |
| `sequence` | **Required** | Vị trí trong stream đó (§8.3.2) |
| `producer_ref` | **Required** | Truy vết authoritative producer (xem 8.2.4) |
| `correlation_id` | **Required** với event thuộc một luồng xử lý; **Optional** với event khởi phát độc lập | §6.7 |
| `causation_refs` | **Zero-to-many** | Root event có thể rỗng (`[]`); không absent (xem 8.2.3) |
| `effective_time` | **Conditional** | Khi domain fact có thời điểm/khoảng hiệu lực. Có thể là instant hoặc interval. **Prohibited với Decision event** — Decision dùng `decision_time` (xem §8.4) |
| `decision_time` | **Required với Decision event · Prohibited với event khác** | Effective-axis time value của Decision; semantic do Decision Domain Contract sở hữu (§8.4) |
| `decision_context_cursor` | **Required với authoritative Decision event** | Knowledge boundary mà Decision dựa vào — thiếu nó thì không chứng minh được input visibility cho parity/replay (§8.4) |
| `market_time` | **Conditional** | CHỈ market-data event, khi source cung cấp — không tạo giả |
| `source_identity` | **Conditional** | Khi source có khả năng retry/redelivery (§6.6) |

Implementation KHÔNG được tự suy luận cardinality — field nào thiếu quy định phải bổ sung vào bảng này qua ADR.

### 8.2.2 `subject_ref` — polymorphic, không mặc định account-scoped entity

Không phải authoritative event nào cũng mô tả một entity thuộc một Account. Ví dụ: `MARKET_DATA_OBSERVED` (subject = instrument, scope = venue), `RISK_POLICY_VERSION_ACTIVATED` (subject = policy version), `PLATFORM_KILL_SWITCH_ACTIVATED` (subject = platform).

```yaml
subject_ref:
  context_id:                    # Required — Domain Context (Chapter 4)
  subject_kind:                  # Required — entity | policy | stream | instrument | account | platform
  subject_type:                  # Required
  subject_id:                    # Required
  scope:                         # Conditional — chỉ các field mà Event Contract khai báo là cần
    account_id:
    venue_id:
    ...
```

**`subject_kind` KHÔNG bao gồm `value`.** Theo [Chapter 6 §6.2](./06-identity-model.md) (Locked), Value Object không có identity riêng (equality by value, không cấp ID) — nên không thể làm subject của một event reference vốn đòi hỏi `subject_id` resolvable. Value Object được biểu diễn **trong payload** hoặc trong `scope` theo value semantics.

```yaml
# ĐÚNG — subject là entity, Value Object nằm trong payload
subject_ref: {subject_kind: entity, subject_type: Order, subject_id: order_123}
payload:
  limit_price: {amount: "65000", currency: USDT}   # Value Object — không có ID

# SAI — ép Value Object có identity, vi phạm Chapter 6
subject_ref: {subject_kind: value, subject_type: Price, subject_id: price_123}
```

*Nguyên tắc: Resolvable subject reference ≠ mọi subject đều có identity. Value Object ≠ Identified Entity.*

**Quy tắc:** mọi authoritative event phải có subject reference đủ để resolve duy nhất semantic subject trong scope của Event Contract ([§6.1](./06-identity-model.md) — không truyền local ID trần qua boundary). Các field scope (`account_id`, `venue_id`, `instrument_id`, `strategy_id`...) là **conditional**, không bắt buộc toàn cục.

### 8.2.3 `causation_refs` — qualified, chỉ trỏ authoritative event record

`causation_refs` là **tập hợp** (bắt buộc để biểu diễn multi-source causality theo [§6.7](./06-identity-model.md) — ví dụ `ARBITRAGE_DECISION_CREATED` phụ thuộc đồng thời quote 2 sàn + risk state).

**Chỉ được tham chiếu authoritative event record.** Dependency không phải event (model artifact, configuration, policy version...) phải được **event hóa trước** theo [I-5](./02-platform-invariants.md), rồi causation trỏ tới event đó — cách này giữ causation graph đồng nhất một loại node.

Mỗi phần tử là **qualified reference** (vì [§6.1](./06-identity-model.md) không đảm bảo `event_id` globally unique):

```yaml
causation_refs:
  - stream_ref: {stream_id: binance-btc-book, registry_version: v3}
    sequence: 98123
    event_id: evt_001        # verification field
```

**Tuple consistency invariant:** ba thành phần là một tuple bất biến — `(stream_ref, sequence)` phải resolve đúng `event_id` đã khai báo. Mismatch là **integrity violation**; consumer KHÔNG được chọn một field làm fallback rồi tiếp tục. `(stream_ref, sequence)` là canonical locator; `event_id` là verification field.

### 8.2.4 `producer_ref` — truy vết implementation đã sinh event

[Chapter 3 §3.1](./03-engineering-principles.md) (Locked) cho phép shadow/experimental/migration implementation tồn tại song song với authoritative implementation. Không có producer identity thì không phân biệt được event nào do authoritative implementation sinh ra — phá [I-1](./02-platform-invariants.md) và parity audit.

```yaml
producer_ref:
  module_id:                # theo module-registry.yaml (Chapter 7 §7.5)
  implementation_version:
  run_id:
  # instance_id: operational metadata, KHÔNG phải domain identity — thuộc telemetry
```

### 8.2.5 `event_contract_ref` — pin Event Contract, tách khỏi `schema_version`

Event Contract là **Referenced Authoritative Artifact** (§8.1.1) nên phải được pin bằng version tường minh. Dùng **Model A**: event pin trực tiếp `event_contract_ref: {contract_id, contract_version}`.

**Vì sao KHÔNG dùng `schema_version` làm proxy cho Event Contract version:** Event Contract sở hữu nhiều thứ hơn payload schema — `event_class`, `allowed_streams`, `merge_constraints`, payload semantic. Hai contract version có thể có **cùng payload schema** nhưng khác `event_class` hoặc khác `allowed_streams`; khi đó `schema_version` không phân biệt được, và historical validator không biết dùng contract nào. Hai thứ này tiến hóa độc lập:

```yaml
event_contract_ref: {contract_id: arbitrage-decision-created, contract_version: v3}
schema_version: 2      # payload schema có thể giữ nguyên qua nhiều contract version
```

## 8.3 Ordering Mechanism — ĐỀ XUẤT (giải OQ-005, chờ Product Owner + ADR)

[Chapter 5 §5.4](./05-time-model.md) (Locked) yêu cầu 2 mức: **Mức 1** intra-partition determinism, **Mức 2** cross-context causal correctness. Đề xuất giải bằng **2 cơ chế riêng biệt**, không dùng global clock:

### 8.3.1 Stream — định nghĩa và thẩm quyền

Một **stream** là một ordered log partition có đúng **một writer authority** cấp phát `sequence`. Mỗi authoritative event thuộc **đúng một** stream.

**Authoritative source duy nhất: `/docs/architecture/stream-registry.yaml`** — sở hữu stream identity, topology, writer authority, lifecycle, và sequence policy. Event Contract **chỉ được tham chiếu** stream, không định nghĩa stream (theo [I-12](./02-platform-invariants.md): một concept + scope = đúng một authoritative source).

```yaml
# stream-registry.yaml — authoritative cho stream definition
registry_version: v3
streams:
  - stream_id: binance-btc-book
    status: active                    # active | retired
    writer_authority:
      module_id: market-data-ingestion    # theo module-registry.yaml (Chapter 7 §7.5)
      capability_version: v2
    sequence_policy: contiguous
    genesis_position: 0
```

```yaml
# Event Contract — authoritative DUY NHẤT cho event-to-stream eligibility
event_type: MARKET_DATA_OBSERVED
event_class: decision | observation | ...
allowed_streams:
  - stream_id: binance-btc-book
```

Phân chia thẩm quyền (mỗi concept đúng một nguồn — I-12):
```
Stream identity / topology / writer authority / lifecycle
  / sequence policy / genesis position                     → stream-registry.yaml

Event class / payload / semantic / stream eligibility      → Event Contract

Cursor                                                     → pin registry_version
```

**Stream Registry KHÔNG chứa `allowed_event_types`.** Quan hệ "event type X có được ghi vào stream Y không" chỉ được khai báo **một chiều** tại Event Contract (`allowed_streams`) — khai báo cả hai chiều tạo 2 danh sách có thể lệch nhau mà không có rule phân xử (vi phạm I-12).

**Eligibility validation phải dùng registry version mà event pin, KHÔNG phải registry hiện tại.** Khi append hoặc validate một event, validator phải: (1) resolve `event.stream_ref.registry_version`; (2) xác nhận stream tồn tại và `active` **trong đúng version đó**; (3) kiểm tra `stream_id` nằm trong `allowed_streams` của đúng Event Contract version tương ứng.

Nếu validate bằng registry hiện tại, một event lịch sử hoàn toàn hợp lệ sẽ trở thành "không hợp lệ" chỉ vì stream đã bị retire sau này — phá vỡ khả năng replay/audit lịch sử.

- Tạo/xóa/tách stream, hoặc đổi writer authority, là thay đổi Event Model → **ADR Required**, kèm bump `registry_version`.
- Một module có thể ghi vào nhiều stream, nhưng mỗi stream chỉ có 1 writer authority (điều kiện để `sequence` contiguous).

#### Registry version là immutable snapshot

Pin một version nhưng nội dung version đó vẫn sửa được thì **không thực sự là pin** — historical meaning của mọi `stream_ref` sẽ đổi ngầm. Bắt buộc:

- Mỗi `registry_version` là một **immutable snapshot**.
- Sau khi bất kỳ authoritative event hoặc cursor nào tham chiếu một registry version: version đó **không được sửa tại chỗ** và **không được tái sử dụng** identifier.
- Mọi thay đổi registry tạo version **mới**.
- Registry version đã được tham chiếu phải được **lưu và resolve được trong toàn bộ replay/audit horizon**.
- **Content integrity phải xác minh được (bắt buộc):** registry snapshot phải có **immutable content identity** — commit SHA, content hash, hoặc tương đương. Bắt buộc ở đây là **verifiability**, không phải một field cụ thể: checksum không cần lặp trong mọi event, nhưng event hoặc run manifest phải **truy được tới content identity bất biến** của registry snapshot đã dùng.

#### Writer authority handoff — exclusive, sequence liên tục

"Có đúng một writer authority" ở trạng thái tĩnh chưa đủ; phải bảo toàn trong **quá trình chuyển giao** (nếu không sẽ tạo duplicate hoặc gap — cả hai là integrity violation theo §8.3.2). Invariant bắt buộc:

1. Có một **activation boundary** authoritative cho việc chuyển giao.
2. Writer cũ **không được append** sau boundary.
3. Writer mới chỉ được append **sau khi** nhận được last committed sequence.
4. Event đầu tiên của writer mới phải thỏa `next_sequence = previous_sequence + 1` (sequence **liên tục xuyên qua** registry version).
5. **Không có khoảng thời gian nào hai writer cùng authoritative.**
6. Handoff failure phải **fail-safe** ([I-6](./02-platform-invariants.md)); **cấm** tự chọn writer theo wall clock.

Representation cụ thể (ví dụ `writer_authority.valid_from_sequence`, hay một event `STREAM_WRITER_AUTHORITY_TRANSFERRED`) do ADR-009 quyết định — Constitution chỉ khóa invariant.

### 8.3.2 Mức 1 — Per-stream contiguous sequence

Trong mỗi stream, `sequence` là **số nguyên liên tiếp, tăng nghiêm ngặt**: với hai record kế tiếp nhau, `next_sequence = previous_sequence + 1`. Thứ tự authoritative trong stream = thứ tự `sequence` — deterministic khi replay, không phụ thuộc physical clock. (Hợp lệ theo [§6.1](./06-identity-model.md): ordering assignment được phép cần coordinator, khác identity uniqueness.)

**Chọn contiguous (Option A) thay vì "strictly increasing, cho phép gap" (Option B) — đề xuất:** trong hệ thống giao dịch, một event thiếu có thể là một fill bị mất, ảnh hưởng trực tiếp Position Ledger. Với contiguous sequence, mất event bị phát hiện **ngay lập tức** bằng phép kiểm tra rẻ nhất có thể (`next != prev + 1`), không cần cơ chế checksum chain phụ. Đánh đổi: writer authority phải cấp `sequence` **atomically cùng lúc với append** — không được reserve trước rồi ghi sau (reserve-then-crash sẽ tạo lỗ hổng vĩnh viễn).

Hệ quả bắt buộc với implementation:
- Sequence allocation và append phải nằm trong cùng một atomic operation.
- Transaction abort không được để lại sequence đã tiêu.
- Compaction/retention không được đổi `sequence` của record còn lại.
- Restore/migration phải giữ nguyên `sequence` gốc.

**Integrity:** duplicate hoặc regression của `sequence` là **integrity violation**. Về gap, phải phân biệt **logical stream** và **physical retained representation**:

- **Authoritative logical stream: contiguous, không gap.** Mọi gap bên trong là integrity violation.
- **Physical retained/archived representation:** được phép **bắt đầu sau genesis** do retention policy (prefix retention), nhưng **KHÔNG được bỏ record ở giữa** retained range.
- **Key-based compaction làm mất authoritative event ở giữa stream bị CẤM** — compaction chỉ áp dụng cho projection/cache ([Chapter 7 §7.4](./07-module-taxonomy.md)), không áp cho authoritative event log.

```yaml
stream_segment:
  retained_from_sequence: 100001   # boundary tường minh
  first_sequence: 100001
  last_sequence: 250000
```

Khoảng trước `retained_from_sequence` **không bị coi là gap**, nhưng replay vượt qua boundary đó phải dùng archive hoặc **bị từ chối tường minh** — không replay best-effort với dữ liệu thiếu. Retention/archive policy cụ thể (giữ bao lâu, archive ở đâu, có giữ vĩnh viễn không) là quyết định storage/cost lớn → **ADR riêng**, chưa chốt ở đây.

Khi phát hiện integrity violation: scope liên quan phải fail-safe theo [I-6](./02-platform-invariants.md) (chặn action tăng risk, vẫn cho risk-reducing action), và không được tự động "vá" bằng cách cấp lại sequence hay bỏ qua gap.

### 8.3.3 Mức 2 — Explicit causation, KHÔNG global total order

Platform **không tuyên bố** có global total order giữa các stream độc lập. Causal correctness đến từ `causation_refs` tường minh (§8.2.3).

### 8.3.4 Merge order ≠ authoritative causal order

Khi replay/consume nhiều stream, cần một **merge policy deterministic** để interleave. **Input Contract sở hữu duy nhất final merge policy** — Event Contract KHÔNG định nghĩa merge order (nếu một họ event có yêu cầu riêng, Event Contract chỉ khai báo **constraint**, và Input Contract phải chọn policy thỏa mọi constraint đó).

```yaml
# Input Contract — authoritative cho input scope + merge policy. Versioned + immutable theo §8.1.1
input_contract_ref:
  contract_id: btc-arbitrage-input
  contract_version: v1
stream_registry_version: v3
included_streams: [binance-btc-book, bybit-btc-book, risk-state]
merge_policy:
  id: deterministic-interleave-v1
  ordering: [recorded_time, stream_id, sequence]
```

**Input Contract là CROSS-MODE — không chỉ dành cho Replay.** Mọi Decision run ở **cả 4 execution mode** (Live, Backtest, Paper Trading, Replay) đều phải pin **cùng một** versioned Input Contract xác định input stream scope + deterministic interleave semantics + registry version. Đây là điều kiện cần để [I-2 Decision Parity](./02-platform-invariants.md) kiểm chứng được: Live không thể dùng input topology A rồi Replay dùng contract B mà vẫn tuyên bố parity. **Cấm gắn Input Contract hồi tố** — contract phải tồn tại và được pin **tại thời điểm Decision được tạo**, kể cả trong Live.

*(Tên gọi: artifact này từng được gọi "Input Contract" ở các bản nháp trước. Đổi thành **Input Contract** vì nó không chỉ phục vụ replay — giữ tên cũ sẽ gây hiểu nhầm khi Live Decision phải pin nó. Vẫn là **một** artifact duy nhất, không thêm surface area; replay-run control cụ thể — cursor bắt đầu/kết thúc, tốc độ — là cấu hình của lần chạy, không thuộc contract này.)*

**Tuân đầy đủ §8.1.1** — mọi thay đổi `included_streams`, `merge_policy`, hoặc constraint resolution đều tạo `contract_version` mới; version đã được cursor/Decision tham chiếu là bất biến. (Nếu contract cùng ID bị sửa nội dung, cùng một cursor lịch sử sẽ cho interleave khác — phá deterministic replay và Decision Parity.)

```yaml
# Event Contract — chỉ constraint, không sở hữu policy
event_type: ARBITRAGE_DECISION_CREATED
allowed_streams: [{stream_id: arbitrage-decisions}]
merge_constraints:
  prerequisite_policy: causation_must_resolve_before_apply
```

Phân chia thẩm quyền:
```
Event semantic + causal constraint        → Event Contract
Replay stream set + interleave policy     → Input Contract
```

Không có default ngầm (Chapter 5 đã khóa: ordering giữa event visible dựa trên Ordering Authority, không phải so `recorded_time` trực tiếp).

**Merge order chỉ quyết định delivery/interleave order — KHÔNG phải authoritative business order.**

Quy tắc bắt buộc cho processor:
- Trước khi authoritative-apply một event có causal prerequisites, processor phải xác nhận **mọi** prerequisite trong `causation_refs` đã visible và resolved tại cursor hiện tại.
- Nếu prerequisite chưa available: event phải được **buffer/defer**, hoặc replay cursor/merge plan phải được điều chỉnh. **Cấm apply speculative.**
- Nếu một prerequisite vẫn unresolved tại một cursor được coi là **complete**: đây là **integrity violation** → fail-safe theo I-6, không được bỏ qua.

## 8.4 Decision time fields — ĐỀ XUẤT (giải OQ-006, chờ Product Owner + ADR)

Ba khái niệm khác nhau, **không được gộp**:

**Thẩm quyền xác định "Decision event":** **Event Contract** khai báo tường minh (`event_class: decision` hoặc `semantic_roles: [decision]`) — **KHÔNG suy luận từ chuỗi `event_type`** (naming không phải semantic authority; một event tên chứa `DECISION` chưa chắc là Decision class, và ngược lại). Validator dựa vào khai báo này để áp đúng cardinality ở §8.2.1.

| Field | Trục | Nghĩa |
|---|---|---|
| `decision_time` | **Effective** (một time value, theo [Chapter 5](./05-time-model.md) Locked) | Thời điểm domain mà Decision có hiệu lực. Semantic chi tiết do Decision Domain Contract quy định |
| `recorded_time` | **Recorded** | Thời điểm event Decision được append vào authoritative log |
| `decision_context_cursor` | **Knowledge boundary** (KHÔNG phải time value — là vector) | Ranh giới tri thức chính xác mà Decision dựa vào |

**Quan hệ với `effective_time` — chọn Mô hình A (đề xuất):** với Decision event, `decision_time` **thay thế** `effective_time` (nó chính là time value trên trục effective, đặc thù hóa cho Decision). Decision event **không** mang cả hai field — tránh 2 field cùng nghĩa trên cùng một trục (tinh thần I-12) và tránh implementation phải đoán field nào authoritative.

*(Mô hình B đã cân nhắc: Decision mang cả `effective_time` lẫn `decision_time` với semantic khác nhau do Domain Contract định nghĩa. Loại bỏ vì chưa có nhu cầu thực tế nào cần phân biệt, và mở đường cho hai nguồn thời gian mâu thuẫn.)*

```yaml
decision_time:   2026-07-23T10:00:00Z        # effective axis — time value (thay effective_time)
recorded_time:   2026-07-23T10:00:01.250Z    # recorded axis — time value
decision_context_cursor:                      # KHÔNG phải time — là một Replay Cursor hợp lệ
  recorded_time: 2026-07-23T10:00:01.100Z
  input_contract_ref: {contract_id: btc-arbitrage-input, contract_version: v1}
  stream_registry_version: v3
  stream_positions:
    binance-btc: 18721
    bybit-btc:   9481
    risk-state:  443
```

**`decision_context_cursor` LÀ một Replay Cursor hợp lệ** tại thời điểm Decision đọc xong input — dùng **cùng canonical schema §8.5**, không phải một schema gần giống nhưng khác field. Bắt buộc pin `input_contract_ref` vì chỉ registry version là chưa đủ: cùng một registry có thể có nhiều Input Contract với stream scope khác nhau (Contract A = Binance+Bybit+Risk, Contract B = Binance+OKX+Risk) — cùng một vector vị trí sẽ được diễn giải khác nhau.

**Vì sao cần `decision_context_cursor` riêng:** replay tới đúng cursor này tái tạo **chính xác** tập input mà Decision đã thấy — điều kiện cần để [I-2 Decision Parity](./02-platform-invariants.md) kiểm chứng được và [I-3](./02-platform-invariants.md) đảm bảo không có input "từ tương lai".

**Cấm gọi Replay Cursor là `decision_time`:** Replay Cursor là cấu trúc vector, không so sánh trực tiếp được với timestamp; `decision_time` theo Chapter 5 (Locked) phải là time value trên trục effective. Đổi ngữ nghĩa `decision_time` sẽ là thay đổi field canonical đã Locked → cần ADR riêng, không được làm ngầm trong Chapter 8.

## 8.5 Replay Cursor Representation

[Chapter 5 §5.3](./05-time-model.md) (Locked): Replay Cursor = Recorded Time boundary + **opaque ordering position** khi cần. Chapter 8 sở hữu representation của ordering position:

```yaml
replay_cursor:
  recorded_time:                  # knowledge boundary
  input_contract_ref:            # replay scope — versioned, immutable (§8.1.1)
    contract_id:
    contract_version:
  stream_registry_version:        # stream universe mà cursor này gắn vào
  stream_positions:               # vị trí chính xác trong từng stream thuộc universe
    <stream_id>: <sequence>
```

**Consistency invariant:** `cursor.stream_registry_version` phải **bằng** registry version mà Input Contract đã pin (hoặc thỏa registry constraint của contract nếu contract khai báo dạng khoảng). Mismatch là **invalid cursor** — phải từ chối, không replay best-effort. Cursor lặp lại registry version để **tự đủ** (self-contained), nhưng không được mâu thuẫn với contract.

Dùng **vector vị trí theo từng stream** (không phải một số duy nhất) vì §8.3 không tuyên bố global total order — cắt chính xác đòi hỏi biết vị trí trong mỗi stream, cho phép dừng đúng ranh giới giữa hai event cùng `recorded_time`.

### 8.5.1 Cursor validity với dynamic stream set

Stream topology thay đổi được (tạo/tách/retire stream — §8.3.1, ADR Required). Một cursor phải tự đủ để diễn giải lại sau nhiều năm, nên bắt buộc:

**Định nghĩa stream universe của cursor** — giao của 3 tập:
```
stream được Input Contract chọn (input_contract_ref)
  ∩ tồn tại/đã activate tại cursor boundary
  ∩ resolve được trong stream_registry_version đã pin
```

**Activation phải theo authoritative visible boundary, KHÔNG theo wall clock:** một stream thuộc universe khi **activation boundary authoritative của nó đã visible/resolved tại cursor**. Không suy luận activation chỉ từ physical timestamp hay từ trạng thái registry hiện tại.

Lý do: nếu dùng wall clock, sẽ gặp tình huống "registry nói stream active từ 10:00:00 nhưng activation fact chỉ được recorded lúc 10:00:03" — replay tại 10:00:01 sẽ *nhìn thấy trước* một fact hệ thống chưa biết, vi phạm [I-3](./02-platform-invariants.md). Điều này cũng nhất quán với §8.3.1 (writer handoff cấm chọn authority theo wall clock).

Stream Registry phải mang lifecycle metadata trỏ tới **authoritative boundary** (ví dụ `activated_by: {stream_ref, sequence, event_id}` hoặc `valid_from_cursor`) — representation cụ thể do ADR-009 quyết định; semantic bắt buộc là *activation visibility theo authoritative boundary*, không phải so timestamp thuần túy.

- **`stream_registry_version`**: cursor gắn với đúng một phiên bản stream registry. Stream không thuộc registry version của cursor **không tham gia** boundary — replay cursor 2026 vẫn diễn giải được bằng registry 2026 dù registry hiện tại đã khác. *(Representation: `stream_registry_version` được **hoist lên cấp cursor** để không lặp trong từng entry; mỗi key `stream_id` trong `stream_positions` phải được hiểu là **qualified bởi registry version của chính cursor** — tương đương `stream_ref` ở event, chỉ khác cách chuẩn hóa.)*
- **Stream thuộc universe nhưng chưa có event visible**: phải biểu diễn tường minh bằng **`genesis_position` được định nghĩa trong đúng Stream Registry version mà cursor pin** (§8.3.1 — Registry sở hữu genesis position), **KHÔNG được để field vắng mặt** — vắng mặt là mơ hồ giữa "chưa có event" và "quên ghi".
- **Consistency invariant:** mọi `stream_positions[s]` phải trỏ tới event có `recorded_time ≤ recorded_time` của cursor. Cursor vi phạm điều này là **invalid cursor** (không phải "cursor lạ") — phải bị từ chối, không được replay best-effort.

## 8.6 Các quy tắc thuộc chapter khác — chỉ tham chiếu, không định nghĩa lại

Theo [I-12](./02-platform-invariants.md):
- **Event naming** → [Chapter 3 §3.2](./03-engineering-principles.md).
- **Schema versioning/compatibility** → [Chapter 10](./10-compatibility-capability-contract.md).
- **Payload schema/semantic của từng event_type** → Event Contract tương ứng.
- **Ngữ nghĩa** correlation/causation → [§6.7](./06-identity-model.md); identity/dedup → [Chapter 6](./06-identity-model.md); time semantics → [Chapter 5](./05-time-model.md).
- **Determinism/Parity:** replay cùng event log cho cùng kết quả khi pin đủ **implementation version + configuration + policy version + contract** ([Chapter 3 §3.1](./03-engineering-principles.md)).
- **External Decision Dependency** (I-5) event hóa theo cùng cơ chế như mọi event nội bộ khác.
