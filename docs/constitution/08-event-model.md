---
id: 08-event-model
title: Event Model
version: "4.2"
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

> **⚠️ Trạng thái & ràng buộc trước khi Lock**
>
> **OQ-005 và OQ-006: hướng ĐÃ ĐƯỢC Product Owner duyệt** (2026-07-18). [ADR-009](../adr/ADR-009.md) và [ADR-010](../adr/ADR-010.md) hiện là **`Draft`, CHƯA được accept**.
>
> OQ-005/OQ-006 vẫn `Open` và **Chapter 8 KHÔNG được Lock** cho tới khi **đủ cả 5** điều kiện:
> 1. ADR-009 được Product Owner **accept**;
> 2. ADR-010 được **accept** theo dependency gate (ADR-010 §7 — không accept trước ADR-009);
> 3. OQ-005/OQ-006 chuyển sang `Resolved` trong MANIFEST;
> 4. ~~§8.4.1 có quyết định của Product Owner~~ — **✅ ĐÃ XONG** (Model A, 2026-07-18; ghi tại ADR-010 §2.6);
> 5. Consolidation review hoàn tất.
>
> *("ADR đã được ghi" KHÔNG đủ — Draft là đã ghi nhưng chưa accept.)*

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
  stream_ref: {stream_id, registry_version}     # locator = (stream_id, sequence); registry_version chỉ là definition reference
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
| `stream_ref` | **Required** | `{stream_id, registry_version}` — `stream_id` **ổn định xuyên mọi registry version**; `registry_version` pin stream definition snapshot đã áp dụng lúc append, **KHÔNG thuộc identity locator** (§8.3.1) |
| `sequence` | **Required** | Vị trí trong stream đó (§8.3.2) |
| `producer_ref` | **Required** | Truy vết authoritative producer (xem 8.2.4) |
| `correlation_id` | **Required** với event thuộc một luồng xử lý; **Optional** với event khởi phát độc lập | §6.7 |
| `causation_refs` | **Zero-to-many** | Direct domain causal predecessor (semantic: [§6.7](./06-identity-model.md)); root event có thể rỗng (`[]`), không absent. Ràng buộc scope thuộc `causal_closure_policy` của Input Contract, KHÔNG phải của event (§8.2.3) |
| `related_event_refs` | **Zero-to-many** | Quan hệ KHÔNG mang causal meaning; KHÔNG tham gia `P_causation` (§8.2.3) |
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

**Hai loại reference — TÁCH SCHEMA, semantic do Chapter 6 sở hữu:**

| Field | Ngữ nghĩa (theo [§6.7](./06-identity-model.md) — Chapter 6 Locked sở hữu) | Tham gia `P_causation`? |
|---|---|---|
| `causation_refs` | **Direct domain causal predecessor/prerequisite** — event/fact đã sinh ra event này. KHÔNG bị thu hẹp thành "chỉ state input": `DECISION_CREATED → RISK_REJECTED` là nhân quả nghiệp vụ thật kể cả khi consumer không đọc payload | **CÓ** |
| `related_event_refs` | Quan hệ **KHÔNG mang causal meaning** (identity/audit reference) | **KHÔNG** |

*Chapter 8 chỉ sở hữu **representation và cardinality** của hai field này; **semantic thuộc Chapter 6 §6.7 + Event Contract**. Chapter 8 KHÔNG được định nghĩa lại nghĩa của causation.*

**Causal closure là ràng buộc ở tầng Input Contract / run validation, KHÔNG phải semantic của event:**
- `causation_refs` là metadata **bất biến cấp event**; Input Contract là scope **cấp run/consumer**. Cùng một event được nhiều Input Contract dùng → **không tồn tại** "Input Contract universe của event" để append-validator kiểm. Vì vậy không được đặt ràng buộc scope vào semantic của event.
- Mỗi **Input Contract phải khai báo `causal_closure_policy`**. Với mọi event B mà contract authoritative-apply, nếu processor **cần payload/state** của một `causation_ref` A thì stream của A **BẮT BUỘC** thuộc input scope + cursor universe của contract đó. Causal predecessor **không phải state-input** của consumer hiện tại thì không bị ép vào scope — chỉ cần xác minh identity/existence.
- Vi phạm closure policy đã khai báo → **Input Contract invalid**, không phải event invalid.

*(Phương án thay thế đã cân nhắc: bắt **mọi** Input Contract causally closed hoàn toàn dưới `causation_refs`. Loại vì quá rộng — một portfolio-view contract sẽ buộc phải include mọi decision/risk stream chỉ để thỏa closure, dù không đọc payload nào.)*

Cả hai field dùng chung schema `event_record_ref` (§8.2.3) và chịu **tuple consistency invariant**. Vi phạm scope là integrity violation → fail-safe theo [I-6](./02-platform-invariants.md).

Mỗi phần tử là **qualified reference** (vì [§6.1](./06-identity-model.md) không đảm bảo `event_id` globally unique):

```yaml
causation_refs:
  - stream_id: binance-btc-book    # canonical locator: (stream_id, sequence)
    sequence: 98123
    event_id: evt_001              # verification field
```

**Canonical locator là `(stream_id, sequence)`** — KHÔNG kèm definition version, vì `stream_id` ổn định xuyên mọi registry version và `sequence` liên tục xuyên writer handoff (§8.3.1). Đưa definition version vào locator sẽ khiến cùng một event có 2 locator khác nhau tùy registry version đang xét.

**Schema canonical `event_record_ref` — dùng thống nhất ở MỌI nơi tham chiếu một event record** (`causation_refs`, `activation_boundary`, `retirement_boundary`, và bất kỳ reference nào thêm sau này):

```yaml
event_record_ref:
  stream_id:      # canonical locator phần 1
  sequence:       # canonical locator phần 2
  event_id:       # verification field
```

Dùng một schema duy nhất thay vì nhiều hình dạng gần giống (`{stream_id, sequence, event_id}` chỗ này, `{control_stream_id, sequence, event_id}` chỗ khác) để tuple-consistency, validation, và historical resolution chỉ có **một** quy tắc — giảm lớp lỗi "cùng concept, nhiều reference shape" đã lặp lại nhiều lần trong chapter này.

**Tuple consistency invariant:** `(stream_id, sequence)` phải resolve đúng `event_id` đã khai báo. Mismatch là **integrity violation**; consumer KHÔNG được chọn một field làm fallback rồi tiếp tục. `event_id` là verification field.

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

## 8.3 Ordering Mechanism — HƯỚNG ĐÃ ĐƯỢC PO DUYỆT · chờ ADR-009 accept

[Chapter 5 §5.4](./05-time-model.md) (Locked) yêu cầu 2 mức: **Mức 1** intra-partition determinism, **Mức 2** cross-context causal correctness. Đề xuất giải bằng **2 cơ chế riêng biệt**, không dùng global clock:

### 8.3.1 Stream — định nghĩa và thẩm quyền

Một **stream** là một ordered log partition có đúng **một writer authority** cấp phát `sequence`. Mỗi authoritative event thuộc **đúng một** stream.

**Authoritative source duy nhất: `/docs/architecture/stream-registry.yaml`** — sở hữu stream identity, topology, writer authority, lifecycle, và sequence policy. Event Contract **chỉ được tham chiếu** stream, không định nghĩa stream (theo [I-12](./02-platform-invariants.md): một concept + scope = đúng một authoritative source).

```yaml
# stream-registry.yaml — authoritative cho stream definition
registry_version: v3
effective_from:                   # BẮT BUỘC với mọi version sau Genesis
  event_ref:                      # schema canonical event_record_ref (§8.2.3)
    stream_id: platform-lifecycle
    sequence: 900
    event_id: evt_registry_v3_activated
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

#### Stream Identity ổn định ≠ Stream Definition Version

Phân biệt bắt buộc (nếu gộp sẽ tạo mâu thuẫn với sequence continuity xuyên writer handoff):

| Khái niệm | Vai trò |
|---|---|
| **`stream_id`** — Logical Stream Identity | **Ổn định xuyên MỌI registry version**, không bao giờ tái sử dụng trong toàn platform. Là thành phần của canonical locator |
| **`registry_version`** — Stream Definition Snapshot | Pin phiên bản `stream-registry.yaml` chứa định nghĩa (writer authority, lifecycle, sequence policy, genesis) đã áp dụng lúc append. **KHÔNG thuộc identity locator** |

**Canonical event locator = `(stream_id, sequence)`** — resolve duy nhất một event record, đúng xuyên mọi registry transition. Ví dụ: stream `btc-book` có sequence 1–500 dưới registry v3, tiếp tục 501–700 dưới v4 sau writer handoff; locator `(btc-book, 500)` vẫn resolve đúng dù cursor đang pin registry v4.

**Không có version namespace riêng cho từng stream:** `stream_ref.registry_version` chính là `stream-registry.yaml.registry_version` — một registry snapshot, không phải số version riêng của từng stream. Dùng thẳng tên `registry_version` để tránh tạo thêm một thuật ngữ version dễ gây suy diễn sai.

**Registry applicability tại thời điểm append:** với mọi authoritative append,
```
event.stream_ref.registry_version = active_registry_at(append_lifecycle_frontier)

append_lifecycle_frontier = lifecycle frontier đã committed ngay TRƯỚC append transaction
                            (pre-append, KHÔNG phải post-append)
```

**Registry activation event KHÔNG được validate bằng chính registry mà nó kích hoạt** (chống vòng tự kích hoạt). Với activation event `E@n` của registry mới:
```
E.stream_ref.registry_version   = active_registry_at(pre_append_frontier)   # = registry CŨ
new_registry.effective_from     = E
active_registry_at(frontier ≥ n) = new_registry                             # registry mới active TỪ n
```
Tức E được **old registry / old writer** append; registry mới chỉ active *sau khi* E committed. Nhất quán với §8.3.5 (activation event phải nằm trên stream đã active trước boundary). Nếu E đồng thời chuyển lifecycle writer: old writer append `E@n`, new writer bắt đầu từ `n+1`.
Không có invariant này, event có thể pin registry **tương lai chưa active** (ví dụ v4 active từ lifecycle sequence 900 nhưng append đang ở frontier 800 lại pin v4 → dùng future configuration knowledge), hoặc pin registry **cũ đã bị supersede**. Representation/evidence của `append_lifecycle_frontier` (ghi trực tiếp · append transaction manifest · coordinator checkpoint · tương đương) thuộc **Phase 1 design spec**; semantic "registry phải active tại append" khóa ở đây.

**Eligibility validation phải dùng registry version mà event pin, KHÔNG phải registry hiện tại.** Khi append hoặc validate một event, validator phải: (1) resolve `event.stream_ref.registry_version`; (2) xác nhận stream tồn tại và `active` **trong đúng version đó**; (3) kiểm tra `stream_id` nằm trong `allowed_streams` của đúng Event Contract version tương ứng.

Nếu validate bằng registry hiện tại, một event lịch sử hoàn toàn hợp lệ sẽ trở thành "không hợp lệ" chỉ vì stream đã bị retire sau này — phá vỡ khả năng replay/audit lịch sử.

- Tạo/xóa/tách stream, hoặc đổi writer authority, là thay đổi Event Model → **ADR Required**, kèm bump `registry_version`.
- Một module có thể ghi vào nhiều stream, nhưng mỗi stream chỉ có 1 writer authority (điều kiện để `sequence` contiguous).

#### Registry version phải visible tại lifecycle frontier

Pin một registry version chưa được chứng minh là **đã authoritative tại knowledge boundary** cho phép cursor dùng topology/writer definition từ tương lai. Ví dụ hỏng: lifecycle sequence 900 mới là `REGISTRY_VERSION_V4_ACTIVATED`, nhưng cursor pin `stream_registry_version: v4` với `lifecycle_frontier.position.sequence: 800` — cursor dùng v4 trong khi lifecycle knowledge mới thấy tới 800.

**Bắt buộc:** mọi registry version **sau Genesis** phải khai báo `effective_from.event_ref` trỏ tới lifecycle activation event của chính nó, trên canonical lifecycle stream.

**Cursor validity:** `cursor.stream_registry_version` chỉ hợp lệ khi **(a)** nó là Genesis Registry, **hoặc (b)** `registry.effective_from.event_ref.sequence ≤ cursor.lifecycle_frontier.position.sequence` (cả hai reference nằm trên canonical lifecycle stream nên phép so có nghĩa — §8.3.5).

**Registry applicability interval — cursor phải dùng registry ĐANG active tại frontier của nó:**

```
active_registry_at(frontier):
  1. Nếu KHÔNG có post-Genesis registry nào có effective_from ≤ frontier
     → trả về Genesis Registry.          # base case: bao gồm cả frontier kind=genesis
  2. Ngược lại
     → trả về registry DUY NHẤT có effective_from lớn nhất, ≤ frontier.
```

**Invariant để hàm này total + unique** (nếu thiếu, hàm có thể trả về zero hoặc nhiều kết quả):
- Mỗi post-Genesis registry version có **đúng một** `effective_from`.
- **KHÔNG** hai registry version nào dùng chung một `effective_from.event_ref`.
- Lifecycle activation event phải **định danh chính xác** registry version được activate.
- Duplicate hoặc ambiguous activation là **integrity violation** → append bị từ chối; dữ liệu lịch sử phát hiện ambiguity phải fail-safe theo [I-6](./02-platform-invariants.md).

Với mọi **authoritative** cursor (Live, Paper, Decision, replay có tính parity evidence):
```
cursor.stream_registry_version  =  active_registry_at(cursor.lifecycle_frontier)
```

*Vì sao không đủ khi chỉ yêu cầu "đã từng visible trước frontier":* giả sử v3 `effective_from` sequence 900, v4 `effective_from` sequence 1200, cursor có frontier 1500 pin v3 — rule cũ cho qua vì `900 ≤ 1500`, nhưng tại frontier 1500 thì **v4 mới là authoritative**. Cursor khi đó kết hợp *knowledge boundary mới* với *registry state cũ*: writer authority cũ, stream vẫn `active` dù v4 đã retire, thiếu `terminal_position` → Live và Replay có thể diễn giải khác stream universe hoặc chờ vô hạn trên stream đã retire.

Historical replay **tự nhiên** pin đúng registry từng active tại frontier lịch sử của nó — không cần ngoại lệ. Contract stability được bảo toàn vì frontier lịch sử nằm trong khoảng v3 còn hiệu lực.

**Chạy registry cũ tại frontier mới** (ví dụ để nghiên cứu "nếu giữ topology cũ thì sao") là hợp lệ nhưng phải phân loại tường minh là **counterfactual simulation** — KHÔNG phải authoritative replay, KHÔNG được dùng làm Live parity evidence.

#### Registry version là immutable snapshot

Pin một version nhưng nội dung version đó vẫn sửa được thì **không thực sự là pin** — historical meaning của mọi `stream_ref` sẽ đổi ngầm. Bắt buộc:

- Mỗi `registry_version` là một **immutable snapshot**.
- Sau khi bất kỳ authoritative event hoặc cursor nào tham chiếu một registry version: version đó **không được sửa tại chỗ** và **không được tái sử dụng** identifier.
- Mọi thay đổi registry tạo version **mới**.
- Registry version đã được tham chiếu phải được **lưu và resolve được trong toàn bộ replay/audit horizon**.
- **Content integrity phải xác minh được (bắt buộc):** registry snapshot phải có **immutable content identity** — commit SHA, content hash, hoặc tương đương. Bắt buộc ở đây là **verifiability**, không phải một field cụ thể: checksum không cần lặp trong mọi event, nhưng event hoặc run manifest phải **truy được tới content identity bất biến** của registry snapshot đã dùng.

#### Writer authority handoff — exclusive, sequence liên tục

"Có đúng một writer authority" ở trạng thái tĩnh chưa đủ; phải bảo toàn trong **quá trình chuyển giao** (nếu không sẽ tạo duplicate hoặc gap — cả hai là integrity violation theo §8.3.2). Invariant bắt buộc:

1. Có một **writer-authority transition boundary** (`handoff_boundary`) authoritative cho việc chuyển giao — **thuật ngữ tách biệt với "activation boundary"** của việc một stream bắt đầu active (§8.3.5). Hai loại khác semantic: quy tắc "activation event không được nằm trên chính stream đang activate" **KHÔNG** áp cho handoff — trong handoff, transfer event hoàn toàn có thể do old writer append trên chính stream đó, rồi new writer tiếp tục sequence kế tiếp.
2. Writer cũ **không được append** sau boundary.
3. Writer mới chỉ được append **sau khi** nhận được last committed sequence.
4. Event đầu tiên của writer mới phải thỏa `next_sequence = previous_sequence + 1` (sequence **liên tục xuyên qua** registry version).
5. **Không có khoảng thời gian nào hai writer cùng authoritative.**
6. Handoff failure phải **fail-safe** ([I-6](./02-platform-invariants.md)); **cấm** tự chọn writer theo wall clock.

Representation cụ thể (ví dụ `writer_authority.valid_from_sequence`, hay một event `STREAM_WRITER_AUTHORITY_TRANSFERRED`) thuộc **Phase 1 design spec** — ADR-009 khóa model, Constitution khóa invariant.

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

### 8.3.4 Deterministic Application Order và Causal Precedence

Khi replay/consume nhiều stream, cần một **merge policy deterministic** để interleave. **Input Contract sở hữu duy nhất final merge policy** — Event Contract KHÔNG định nghĩa merge order (nếu một họ event có yêu cầu riêng, Event Contract chỉ khai báo **constraint**, và Input Contract phải chọn policy thỏa mọi constraint đó).

```yaml
# Input Contract — authoritative cho input scope + merge + frontier. Versioned + immutable theo §8.1.1
input_contract_ref:
  contract_id: btc-arbitrage-input
  contract_version: v1
stream_registry_version: v3
included_streams: [binance-btc-book, bybit-btc-book, risk-state]

merge_policy:
  algorithm: deterministic-causal-topological-order   # causal precedence LUÔN đứng trước
  concurrent_tie_break: [stream_id, sequence]         # chỉ áp cho event KHÔNG có quan hệ nhân quả

frontier_policy:                                       # BẮT BUỘC (§8.3.4) — versioned cùng contract
  mechanism:
  completeness_rule:
  late_arrival_behavior:
  buffer_limit_policy:
  incomplete_frontier_behavior:
```

**Partial order authoritative = hợp của HAI hard constraint** (cả hai đều bất biến, không được version hóa qua tie-break):

```
P_authoritative = P_stream ∪ P_causation

P_stream:     (stream_id, n) ≺ (stream_id, n+1)     — per-stream sequence precedence
P_causation:  cause ≺ effect                         — từ `causation_refs` (domain causation, kể cả bắc cầu);
                                                    `related_event_refs` KHÔNG tham gia
```

**`P_authoritative` BẮT BUỘC là một DAG** — topological order chỉ tồn tại khi graph không có cycle. Một causation edge KHÔNG được:
- tạo cycle trực tiếp hoặc bắc cầu (ví dụ A causes B, B causes A);
- mâu thuẫn per-stream sequence precedence (ví dụ `A@100.causation_refs = [A@101]` → `A ≺ B ≺ A`, không có thứ tự hợp lệ);
- khiến effect đứng trước cause trong cùng logical stream.

**Cycle hoặc precedence contradiction là integrity violation:** event append/import phải **bị từ chối**; dữ liệu lịch sử phát hiện cycle phải **fail-safe** theo [I-6](./02-platform-invariants.md) — **cấm** tự bỏ một edge để tiếp tục. Thuật toán phát hiện và phạm vi kiểm tra thuộc **Phase 1 design spec** (ADR-009 khóa yêu cầu, không khóa thuật toán); **acyclicity là constitutional invariant**, không để implementation tự suy luận.

Merge policy phải tạo **deterministic topological order trên hợp của hai partial order này**. `concurrent_tie_break` CHỈ được áp dụng cho các event **không bị ordered bởi cả hai** — tức không cùng stream VÀ không có quan hệ causal ancestry.

*Vì sao per-stream precedence phải là hard constraint, không phải tie-break:* hai event `A100`, `A101` cùng stream nhưng không có `causation_refs` trực tiếp với nhau vẫn **đã được** sequence khóa thứ tự (§8.3.2). Nếu chỉ dựa vào tie-break `[stream_id, sequence]`, một Input Contract tương lai đổi thành `[event_type, stream_id, sequence]` sẽ **đảo ngược** thứ tự hai event cùng stream — phá authoritative intra-stream order.

**`recorded_time` KHÔNG được làm primary authoritative ordering key giữa các stream** (nhất quán [Chapter 5 §5.4](./05-time-model.md) Locked). Nó được dùng cho: visibility boundary (§8.5) · đo latency · observability · chọn ứng viên *bên trong* một thuật toán đã bảo toàn causal precedence. Ví dụ hỏng nếu dùng làm primary key:

```
A: QUOTE_OBSERVED       recorded_time = 10:00:01.100
B: DECISION_CREATED     recorded_time = 10:00:01.050, causation_refs = [A]
sort theo recorded_time → B trước A     ← SAI nhân quả
causal-topological      → A trước B     ← ĐÚNG
```

*(Nếu cần một thứ tự hiển thị theo thời gian cho UI/report, đó là **presentation order** — tách hoàn toàn khỏi **authoritative apply order**; Decision Engine KHÔNG được dùng presentation order làm state-transition order.)*

**`frontier_policy` là thành phần BẮT BUỘC và versioned của Input Contract.** Thay đổi frontier/completeness, late-arrival, hoặc buffer/fail-safe semantics **bắt buộc tạo Input Contract version mới** — nếu để ngoài contract, hai run cùng pin `btc-arbitrage-input@v1` vẫn có thể dùng watermark 500ms vs committed frontier và cho ra input cut khác nhau.

**Input Contract là CROSS-MODE — không chỉ dành cho Replay.** Khi **so sánh hoặc tái tạo cùng một logical Decision/run** giữa **cả 4 execution mode** (Live, Backtest, Paper Trading, Replay), mọi mode phải pin **cùng một** versioned Input Contract xác định input stream scope + deterministic interleave semantics + registry version. Đây là điều kiện cần để [I-2 Decision Parity](./02-platform-invariants.md) kiểm chứng được: Live không thể dùng input topology A rồi Replay dùng contract B mà vẫn tuyên bố parity. **Cấm gắn Input Contract hồi tố** — contract phải tồn tại và được pin **tại thời điểm Decision được tạo**, kể cả trong Live.

*(Tên gọi: artifact này từng được gọi **`Replay Contract`** ở các bản nháp trước. Đổi thành **`Input Contract`** vì nó áp dụng cross-mode, không chỉ phục vụ replay — giữ tên cũ sẽ gây hiểu nhầm khi Live Decision phải pin nó. Vẫn là **một** artifact duy nhất, không thêm surface area; replay-run control cụ thể — cursor bắt đầu/kết thúc, tốc độ — là cấu hình của lần chạy, không thuộc contract này.)*

**Tuân đầy đủ §8.1.1** — mọi thay đổi `included_streams`, `merge_policy`, `frontier_policy`, hoặc constraint resolution đều **bắt buộc** tạo `contract_version` mới; version đã được cursor/Decision tham chiếu là bất biến. (Nếu contract cùng ID bị sửa nội dung, cùng một cursor lịch sử sẽ cho interleave khác — phá deterministic replay và Decision Parity.)

```yaml
# Event Contract — chỉ constraint, không sở hữu policy
event_type: ARBITRAGE_DECISION_CREATED
allowed_streams: [{stream_id: arbitrage-decisions}]
merge_constraints:
  prerequisite_policy: causation_must_resolve_before_apply
```

Phân chia thẩm quyền:
```
Event semantic + causal constraint          → Event Contract
Cross-mode input scope
  + deterministic application order
  + completeness/frontier semantics         → Input Contract
```

#### Completeness / Frontier semantics (bắt buộc cho cross-mode)

Merge policy sắp theo `recorded_time` dễ thực hiện khi replay một tập event hữu hạn, nhưng trong **Live** consumer không biết liệu một event có `recorded_time` sớm hơn còn đang đến trễ từ stream khác hay không:

```
Event X đã được append trên stream Bybit với recorded_time 10:00:00.900,
nhưng cross-stream consumer chỉ NHẬN được nó lúc 10:00:03 do delivery delay.

10:00:01 — Live nhận Binance event (recorded_time 10:00:01) → apply ngay
10:00:03 — Live mới nhận event X (recorded_time 10:00:00.900, đã append từ trước)

Live apply thực tế:        Binance → X
Replay đọc từ log:          X → Binance      ← KHÁC NHAU, phá parity
```

*(Lưu ý semantic: `recorded_time` là thời điểm event được ghi vào durable log — KHÔNG phải thời điểm consumer nhận được, cũng không phải timestamp của sàn. Chênh lệch ở đây đến từ **delivery delay** giữa append và nhận; một nguồn khác là **clock skew** giữa các append node khiến physical recorded_time không phản ánh đúng thứ tự nhân quả.)*

**Invariant bắt buộc:** một cross-mode merge policy chỉ hợp lệ khi Input Contract định nghĩa **deterministic completeness/frontier semantics** — quy tắc cho biết khi nào một prefix đa stream đã đủ hoàn chỉnh để được authoritative-apply.

- **Live KHÔNG được authoritative-apply một merged prefix mà Replay sau đó có thể chèn thêm event visible trước nó** theo cùng Input Contract.
- Khi frontier chưa complete: processor phải **buffer/defer** hoặc **fail-safe** ([I-6](./02-platform-invariants.md)).
- **CẤM suy luận completeness từ wall clock.**

**Ràng buộc với watermark / bounded lateness:** hai cơ chế này chỉ hợp lệ nếu **clock/frontier source của chúng được pin, event hóa, và replay được** — ví dụ watermark do source phát ra dưới dạng event, hoặc timer được event hóa vào log. **Processing wall clock cục bộ KHÔNG được làm completeness authority** (nếu không, replay sẽ cho frontier khác Live). Điều này không mâu thuẫn với việc cấm suy completeness từ wall clock ở trên: cái bị cấm là *đồng hồ cục bộ lúc xử lý*, cái được phép là *frontier signal đã trở thành fact bất biến trong log*.

**Phân tầng thẩm quyền:** [ADR-009](../adr/ADR-009.md) khóa **architectural model** và các invariant bắt buộc của frontier. **Phase 1 phải tạo architecture/design specification** cho: per-stream committed frontier · multi-stream completeness rule · late-arrival behavior · buffer limit/fail-safe behavior · coordinator/checkpoint · cách capture `decision_context_cursor` tại frontier. Nếu Phase 1 phát sinh lựa chọn làm **thay đổi semantic đã khóa trong ADR-009** → bắt buộc mở **follow-up ADR**, không sửa ngầm.

Không có default ngầm (Chapter 5 đã khóa: ordering giữa event visible dựa trên Ordering Authority, không phải so `recorded_time` trực tiếp).

**Merge policy quyết định deterministic authoritative-application order** cho processor, và order này **phải giống nhau giữa mọi execution mode** (điều kiện cần cho [I-2 Parity](./02-platform-invariants.md) khi processor có state — hai thứ tự apply khác nhau trên cùng tập event có thể cho Decision khác nhau).

Phân biệt 4 khái niệm, không gộp:

| Khái niệm | Nghĩa |
|---|---|
| **Causal precedence** | Partial order authoritative của dependency (từ `causation_refs`) |
| **Deterministic application order** | Thứ tự authoritative mà processor dùng để chuyển trạng thái — chính là merge policy, giống nhau mọi mode |
| **Domain causation** | Quan hệ nhân quả nghiệp vụ — **KHÔNG được suy ra từ tie-break** |
| **Presentation order** | Thứ tự hiển thị cho UI/report — không authoritative |

**Tie-break giữa các event causally incomparable KHÔNG tạo thêm quan hệ nhân quả hay business precedence trong domain** — nó chỉ chọn một thứ tự ổn định để mọi mode xử lý giống nhau. Nói cách khác: `authoritative apply order ≠ domain causal meaning`. Processor **không được** tự ý apply theo thứ tự khác merge policy đã công bố.

Quy tắc bắt buộc cho processor:
- Trước khi authoritative-apply một event có causal prerequisites, processor phải xác nhận **mọi** prerequisite trong `causation_refs` đã visible và resolved tại cursor hiện tại.
- Nếu prerequisite chưa available: event phải được **buffer/defer**, hoặc replay cursor/merge plan phải được điều chỉnh. **Cấm apply speculative.**
- Nếu một prerequisite vẫn unresolved tại một cursor được coi là **complete**: đây là **integrity violation** → fail-safe theo I-6, không được bỏ qua.

### 8.3.5 Stream Lifecycle and Bootstrap

**Retirement và terminal frontier (Model B — đề xuất):** một stream bị retire **vẫn thuộc universe** nếu Input Contract chọn nó, nhưng vị trí bị đóng tại `terminal_position` và frontier của nó được coi là **terminal** (không chờ thêm). Chọn Model B thay vì Model A (loại stream retired khỏi universe) vì: loại khỏi universe sẽ làm **biến mất một phần input history** khỏi cursor, phá replay/audit của giai đoạn stream còn hoạt động.

```yaml
retirement_boundary:
  event_ref:                    # schema canonical event_record_ref (§8.2.3)
    stream_id:
    sequence:
    event_id:
terminal_position:
  sequence:                     # sequence cuối cùng hợp lệ của stream
```

**Invariant bắt buộc cho retirement** (tương đương mức chặt của writer handoff §8.3.1):
1. `terminal_position.sequence` phải **bằng last committed sequence** của stream.
2. **Không event nào được append sau** `terminal_position`.
3. Writer authority phải **dừng append trước khi** retirement trở thành authoritative.
4. Retirement boundary chỉ được publish **sau khi** terminal position đã được xác nhận bất biến.
5. Retirement event **không được nằm trên chính stream đang retire** (cùng lý do bootstrap cycle như activation).
6. `(stream_id, terminal_position.sequence)` không resolve được đúng last event là **integrity violation**.
7. Một stream retired **KHÔNG được khiến frontier chờ vô hạn** — phải có authoritative visible boundary và terminal position, hoặc quy tắc loại khỏi universe tường minh trong Input Contract.

Protocol cụ thể (ví dụ `stop writer → confirm last sequence → append retirement event`, hay atomic coordinator protocol khác) thuộc **Phase 1 design spec**; ADR-009 khóa model, Constitution khóa **outcome**.

**Activation phải theo authoritative visible boundary, KHÔNG theo wall clock:** một stream thuộc universe khi **activation boundary authoritative của nó đã visible/resolved tại cursor**. Không suy luận activation chỉ từ physical timestamp hay từ trạng thái registry hiện tại.

Lý do: nếu dùng wall clock, sẽ gặp tình huống "registry nói stream active từ 10:00:00 nhưng activation fact chỉ được recorded lúc 10:00:03" — replay tại 10:00:01 sẽ *nhìn thấy trước* một fact hệ thống chưa biết, vi phạm [I-3](./02-platform-invariants.md). Điều này cũng nhất quán với §8.3.1 (writer handoff cấm chọn authority theo wall clock).

Stream Registry phải mang lifecycle metadata trỏ tới **authoritative boundary**, dùng một **bootstrap-safe locator độc lập** — canonical locator `(stream_id, sequence)` trên một control stream:

```yaml
activation_boundary:
  event_ref:                           # schema canonical event_record_ref (§8.2.3)
    stream_id: platform-lifecycle
    sequence: 812
    event_id: evt_stream_activated
```

**Cấm dependency cycle (bắt buộc):**
- Lifecycle boundary của Stream Registry **KHÔNG được tham chiếu** một artifact mà chính nó trực tiếp hoặc gián tiếp phụ thuộc vào Stream Registry version đang được định nghĩa. Cụ thể: **không dùng full Replay Cursor** (hay bất kỳ thứ gì chứa `input_contract_ref`) làm activation boundary — sẽ tạo vòng `Stream Registry v4 → cursor → Input Contract → Stream Registry v4`, khiến không artifact nào hoàn chỉnh và không tính được content identity sạch (§8.1.1 điều 5).
- **Activation event phải nằm trên một stream đã active TRƯỚC boundary đó** — cấm đặt activation event của stream X lên chính stream X (vòng bootstrap: X chỉ active sau event E, nhưng E lại phải append vào X → không thể khởi tạo).

#### Genesis Registry — ngoại lệ root DUY NHẤT

Quy tắc trên tạo hồi quy vô hạn nếu không có điểm khởi đầu (stream A cần B active trước, B cần C...). Giải bằng **đúng một** ngoại lệ, phạm vi hẹp:

**Genesis Registry** là root authoritative artifact, được tạo và phê duyệt theo [Governance](./00-governance.md) **trước khi** runtime event log hoạt động. Nó phải:
- định nghĩa **đúng MỘT canonical Logical Lifecycle Stream** (xem ràng buộc bên dưới);
- định nghĩa writer authority ban đầu;
- có immutable content identity (§8.1.1 điều 5);
- **không cần** activation event đứng trước nó (đây chính là nội dung của ngoại lệ).

**Canonical Lifecycle Stream (Model A):** platform có **đúng một** Logical Lifecycle Stream với `stream_id` ổn định. **Mọi** activation, retirement, stream creation, và writer-authority transition boundary phải được ghi trên stream này. Lifecycle stream có thể handoff writer (§8.3.1) nhưng **không đổi logical stream identity**.

Ràng buộc kéo theo:
```
boundary.event_ref.stream_id  =  cursor.lifecycle_frontier.stream_id  =  canonical lifecycle stream_id
```
*Vì sao Model A thay vì lifecycle frontier dạng vector (Model B):* so sánh `boundary.sequence ≤ frontier.sequence` chỉ có nghĩa khi hai bên **cùng logical stream** — với nhiều control stream, `100 ≤ 500` giữa `lifecycle-east` và `lifecycle-west` là phép so vô nghĩa (hai ordering authority khác nhau). Model B (vector `lifecycle_frontiers`) tổng quát hơn nhưng tạo partial order đa stream cho control plane, phức tạp không tương xứng nhu cầu.

**Sau Genesis Registry, mọi stream creation, activation, retirement, và writer handoff bắt buộc dùng lifecycle boundary bình thường. KHÔNG có ngoại lệ thứ hai** — implementation không được tự tạo bootstrap shortcut nào khác.

**Validation chain cho lifecycle boundary** (giữ đúng mô hình `locator = (stream_id, sequence)`, `definition evidence = resolved_event.stream_ref.registry_version`):
1. Dùng `event_ref.(stream_id, sequence)` làm canonical locator để resolve event; xác minh khớp `event_ref.event_id` — mismatch là **integrity violation**.
2. Dùng `event.stream_ref.registry_version` (của **event đã resolve**, KHÔNG phải registry hiện tại) để validate historical stream definition tại thời điểm append.
3. Xác nhận control stream đã **active trước** boundary đó, theo đúng registry version ở bước 2.
4. Xác nhận activation event **không nằm trên chính stream đang được activate**.

Bỏ qua bước 2 và validate bằng registry hiện tại sẽ lặp lại đúng lỗi historical validation đã sửa ở §8.3.1.

Representation cuối cùng thuộc **Phase 1 design spec**; semantic bắt buộc là *activation visibility theo authoritative boundary* (không so timestamp thuần túy) **và không có dependency cycle**.

## 8.4 Decision time fields — HƯỚNG ĐÃ ĐƯỢC PO DUYỆT · chờ ADR-010 accept

Ba khái niệm khác nhau, **không được gộp**:

**Thẩm quyền xác định "Decision event":** **Event Contract** khai báo tường minh bằng **đúng một field canonical `event_class: decision`** (`semantic_roles` nếu tồn tại cho mục đích khác thì là **metadata KHÔNG authoritative**, cấm dùng để kích hoạt Decision cardinality — hai field authority tương đương sẽ khiến validator phân loại khác nhau) — **KHÔNG suy luận từ chuỗi `event_type`** (naming không phải semantic authority; một event tên chứa `DECISION` chưa chắc là Decision class, và ngược lại). Validator dựa vào khai báo này để áp đúng cardinality ở §8.2.1.

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
  lifecycle_frontier:                         # BẮT BUỘC — như mọi Replay Cursor (§8.5)
    stream_id: platform-lifecycle
    position: {kind: event, sequence: 812}
  stream_positions:
    binance-btc: 18721
    bybit-btc:   9481
    risk-state:  443
```

**Authoritative Decision event thiếu BẤT KỲ field bắt buộc nào của canonical Replay Cursor — gồm `lifecycle_frontier` — là invalid Decision event và phải bị từ chối khi append.** Không có nó, replay không chứng minh được tại thời điểm Decision: stream nào đã active, stream nào đã retired, terminal frontier nào đã visible — đúng thứ `decision_context_cursor` sinh ra để bảo đảm cho [I-2](./02-platform-invariants.md)/[I-3](./02-platform-invariants.md).

**`decision_context_cursor` LÀ một Replay Cursor hợp lệ** tại thời điểm Decision đọc xong input — dùng **cùng canonical schema §8.5**, không phải một schema gần giống nhưng khác field. Bắt buộc pin `input_contract_ref` vì chỉ registry version là chưa đủ: cùng một registry có thể có nhiều Input Contract với stream scope khác nhau (Contract A = Binance+Bybit+Risk, Contract B = Binance+OKX+Risk) — cùng một vector vị trí sẽ được diễn giải khác nhau.

**Vì sao cần `decision_context_cursor` riêng:** replay tới đúng cursor này tái tạo **chính xác** tập input mà Decision đã thấy — điều kiện cần để [I-2 Decision Parity](./02-platform-invariants.md) kiểm chứng được và [I-3](./02-platform-invariants.md) đảm bảo không có input "từ tương lai".

**Cấm gọi Replay Cursor là `decision_time`:** Replay Cursor là cấu trúc vector, không so sánh trực tiếp được với timestamp; `decision_time` theo Chapter 5 (Locked) phải là time value trên trục effective. Đổi ngữ nghĩa `decision_time` sẽ là thay đổi field canonical đã Locked → cần ADR riêng, không được làm ngầm trong Chapter 8.

## 8.4.1 Decision "in-flight" qua registry transition — Append-and-Revalidate (PO quyết 2026-07-18)

Tình huống: Decision đọc xong input ở frontier 899 (cursor pin Registry v3), registry v4 activate ở 900, Decision event append ở 901 (envelope pin v4). Hai rule riêng lẻ (§8.3.1 + §8.4) đều đúng nhưng cần một policy chung vì nó thay đổi authoritative Decision history.

Hai phương án đã được xem xét: **Append-and-Revalidate** (giữ Decision, revalidate trước Risk/Execution) và **Reject-and-Recompute** (từ chối tại append, tính lại). Phương án Reject-and-Recompute bị loại vì làm mất bản ghi một Decision đã thực sự được tính; muốn giữ Explainability vẫn phải ghi computation-attempt fact — khi đó gần như phương án còn lại nhưng không sạch bằng về semantic/audit.

**✅ Product Owner đã quyết (2026-07-18): chọn phương án A.** Quyết định + rationale + 4 guardrail được ghi tại [ADR-010 §2.6](../adr/ADR-010.md) (chủ sở hữu Decision Time/Context); ADR-009 giữ registry/frontier boundary và cross-reference sang đó.

**Normative rule tại Chapter 8:** Decision có knowledge cut trước transition **vẫn được append** như immutable historical fact; **KHÔNG tự động có execution eligibility**; Risk/Execution **bị chặn** cho tới khi revalidation theo registry đang active thành công; kết quả revalidation (success/stale/reject) phải là **authoritative event**; **cấm sửa/xóa** Decision gốc. **Revalidation evidence chain (relational invariant, KHÔNG được đứt):**
```
OriginalDecision  ←causation—  RevalidationSucceeded  ←causation—  RiskApproved  ←causation—  ExecutionIntentCreated
```
1. Revalidation result phải tham chiếu **chính xác** original Decision (không dùng success của Decision khác).
2. Revalidation result phải ghi **evidence của registry/knowledge boundary** đã dùng để revalidate (không dùng success dưới registry khác).
3. Risk Approval muốn cho phép tiếp tục phải **causally depend** vào successful revalidation result đó.
4. Execution Intent phải **truy vết được** tới Risk Approval và successful revalidation tương ứng.

Yêu cầu *"trace không được đứt"* là **platform-level invariant** ([I-1](./02-platform-invariants.md) cần immutable causation evidence; [I-4](./02-platform-invariants.md) cần mọi execution đi qua Risk Gateway) — không phải test fixture.

*(Event type, payload, và state machine cụ thể `computed → revalidated → rejected/superseded` thuộc **Decision/Risk Domain Contract**, không hardcode ở đây — theo I-13.)*

## 8.5 Replay Cursor Representation

[Chapter 5 §5.3](./05-time-model.md) (Locked): Replay Cursor = Recorded Time boundary + **opaque ordering position** khi cần. Chapter 8 sở hữu representation của ordering position:

```yaml
replay_cursor:
  recorded_time:                  # knowledge boundary
  input_contract_ref:             # input scope — versioned, immutable (§8.1.1)
    contract_id:
    contract_version:
  stream_registry_version:        # stream universe mà cursor này gắn vào
  lifecycle_frontier:             # BẮT BUỘC — chứng minh boundary nào đã visible
    stream_id: platform-lifecycle
    position:
      kind: event                 # event | genesis
      sequence: 812
  stream_positions:               # vị trí chính xác trong từng stream thuộc universe
    <stream_id>: <sequence>
```

**`lifecycle_frontier` là thành phần bắt buộc của canonical knowledge boundary** (Model A). Lý do: stream universe được quyết định bởi activation/retirement boundary nằm trên **control stream**, nhưng control stream không thuộc `included_streams` của Input Contract (nó là platform-control fact, không phải strategy input). Không pin frontier của nó thì cursor **không tự chứng minh được** boundary sequence 812 đã visible tại chính cursor này — so `recorded_time` là không đủ (nhiều event cùng timestamp; vector cursor sinh ra chính để phân biệt các trường hợp đó).

**Trạng thái genesis (chưa có lifecycle event nào):** ngay sau Genesis Registry, lifecycle stream tồn tại nhưng chưa có event nào được append — cursor đầu tiên vẫn phải hợp lệ. Dùng `position.kind: genesis`:

```yaml
lifecycle_frontier:
  stream_id: platform-lifecycle
  position: {kind: genesis, sequence: 0}   # "chưa có lifecycle event nào visible"
```

Khi `kind: genesis`: **không** bắt buộc resolve tới event record; `sequence` phải lấy đúng `genesis_position` của canonical lifecycle stream trong Genesis Registry/pinned registry; Genesis Registry phải có immutable content identity (§8.1.1). *(Không bắt buộc append một "lifecycle genesis event" trước mọi Decision — làm vậy tạo operational dependency thừa và làm mờ vai trò root của Genesis Registry. Cách này tương đương cơ chế `genesis_position` mà `stream_positions` đã có.)*

**Validity invariant khi `position.kind: event`** (tương đương mức chặt của `stream_positions`): `lifecycle_frontier.(stream_id, position.sequence)` phải resolve tới một **committed authoritative event record trên canonical lifecycle stream**, và event đó phải thỏa:
- `event.recorded_time ≤ cursor.recorded_time` — **cấm cursor nhìn thấy lifecycle fact từ tương lai** (nếu không, một future lifecycle event có thể activate stream chưa visible, retire stream quá sớm, hoặc đổi tập input mà Decision được phép đọc — đúng dạng lỗi [I-3](./02-platform-invariants.md) mà `decision_context_cursor` sinh ra để chặn);
- `sequence` không vượt committed/complete frontier của lifecycle stream;
- stream tồn tại và active trong historical registry version của chính event đó;
- frontier không nằm ngoài retained/archive-resolvable range (§8.3.2).

Vi phạm bất kỳ điều nào → **invalid cursor**, cấm replay hoặc process best-effort.

**Invariant:** mọi activation/retirement boundary dùng để xác định stream universe phải có `sequence ≤ lifecycle_frontier.position.sequence` của cursor (hợp lệ vì cả hai cùng nằm trên canonical lifecycle stream — §8.3.5). Nếu `kind: genesis`, chưa có lifecycle event nào visible nên **không** activation/retirement boundary nào thuộc universe. Khi **so sánh hoặc tái tạo cùng một logical Decision/run** qua các execution mode, mọi mode phải pin **cùng** `lifecycle_frontier` — nếu không, universe có thể khác nhau giữa Live và Replay, phá [I-2](./02-platform-invariants.md) và làm `decision_context_cursor` không còn là exact knowledge boundary. *(Đây KHÔNG có nghĩa mọi run phải dùng chung một frontier cố định: Decision lúc 10:00 và Decision lúc 11:00 đương nhiên có frontier khác nhau.)*

*(Chọn Model A thay vì Model B — bắt buộc control stream nằm trong mọi Input Contract — vì Model B trộn platform-control facts vào strategy input scope, làm bẩn domain boundary.)*

**Consistency invariant:** `cursor.stream_registry_version` phải **bằng** registry version mà Input Contract đã pin. Mismatch là **invalid cursor** — phải từ chối, không replay best-effort. Cursor lặp lại registry version để **tự đủ** (self-contained), nhưng không được mâu thuẫn với contract.

**Input Contract dùng EXACT PIN, KHÔNG dùng range/constraint** (chốt cho v1): `stream_registry_version: v4`, không phải `">=v3"`. Lý do: một range open-ended làm semantic của một immutable Input Contract **mở rộng trong tương lai mà không bump version** — trái chính yêu cầu versioned/immutable của contract; ngoài ra range chưa định nghĩa được registry tương lai vào range bằng authority nào, compatibility của `included_streams` chứng minh ra sao, và chọn version nào khi nhiều registry cùng match.

*Concern được GHI NHẬN trong Draft (chưa phải đã chấp nhận):* registry activation có thể tạo **contract-version churn**, kể cả khi thay đổi registry không liên quan trực tiếp tới một strategy. Tradeoff này chỉ được coi là **accepted khi Product Owner approve ADR-009**. Nếu churn trở thành vấn đề thật, mở **follow-up ADR** cho một trong các mô hình: immutable closed compatibility set · subset registry · capability-based registry constraint.

Dùng **vector vị trí theo từng stream** (không phải một số duy nhất) vì §8.3 không tuyên bố global total order — cắt chính xác đòi hỏi biết vị trí trong mỗi stream, cho phép dừng đúng ranh giới giữa hai event cùng `recorded_time`.

### 8.5.1 Cardinality của Replay Cursor

Mọi cursor (kể cả `decision_context_cursor` ở §8.4) phải có **đủ** các field sau — validator kiểm bảng này, không phải ghép cardinality từ prose rải rác nhiều mục:

| Cursor field | Cardinality | Ghi chú |
|---|---|---|
| `recorded_time` | **Required** | Knowledge boundary |
| `input_contract_ref` | **Required** | `{contract_id, contract_version}` — versioned, immutable |
| `stream_registry_version` | **Required** | Xác định stream universe; phải khớp registry version Input Contract pin |
| `lifecycle_frontier` | **Required** | `{stream_id, position: {kind, sequence}}` trên canonical lifecycle stream; `kind` ∈ `{genesis, event}` (§8.3.5) |
| `stream_positions` | **Required** | Map `stream_id → sequence`; stream chưa có event dùng `genesis_position` tường minh |

Cursor thiếu bất kỳ field nào ở trên là **invalid cursor** — cấm replay/process best-effort. Authoritative Decision event mang cursor invalid phải bị **từ chối khi append**.

### 8.5.2 Relational invariants — các field phải nhất quán với nhau

Bảng §8.5.1 trả lời *"field nào bắt buộc có"*. Bảng này trả lời *"các field phải quan hệ hợp lệ với nhau thế nào"* — hai validator authority tập trung, ngăn đúng lớp lỗi "mỗi field hợp lệ riêng lẻ nhưng tổ hợp thì sai".

| Quan hệ | Invariant |
|---|---|
| **Cursor → Decision** | `cursor.recorded_time ≤ decisionEvent.recorded_time` |
| **Position → Cursor** | `position_event.recorded_time ≤ cursor.recorded_time` |
| **Lifecycle → Cursor** | `lifecycle_event.recorded_time ≤ cursor.recorded_time` |
| **Registry → Lifecycle** | Nếu `kind: genesis`: `cursor.stream_registry_version` = **Genesis Registry**. Nếu `kind: event`: `cursor.stream_registry_version` = **`active_registry_at(cursor.lifecycle_frontier)`** — phải resolve total + unique theo §8.3.1. *(`effective_from ≤ frontier` chỉ là điều kiện CẦN bên trong hàm, KHÔNG phải điều kiện validity cuối cùng — nếu chỉ kiểm điều kiện cần, cursor frontier 1500 vẫn pin được v3 dù v4 active từ 1200.)* |
| **Registry → Contract** | `cursor.stream_registry_version` = registry version mà Input Contract pin |

**Quan hệ Cursor → Decision là bắt buộc:** với mọi authoritative Decision event, `decision_context_cursor.recorded_time ≤ DecisionEvent.recorded_time`. Bằng nhau được phép khi knowledge cut và Decision append thuộc cùng authoritative transaction/boundary. Nếu cursor lớn hơn → **Decision event invalid, phải bị từ chối khi append**.

Thiếu invariant này, một Decision append lúc 10:00:01 vẫn có thể mang cursor `recorded_time` 10:00:05 với mọi position "hợp lệ so với cursor" — tức tuyên bố đã biết dữ liệu từ tương lai của chính nó, vi phạm [I-3](./02-platform-invariants.md). Nhờ bắc cầu, chuỗi `input_event ≤ cursor ≤ DecisionEvent` chứng minh không input/lifecycle fact nào đến từ tương lai của Decision.

### 8.5.3 Cursor validity với dynamic stream set

Stream topology thay đổi được (tạo/tách/retire stream — §8.3.1, ADR Required). Một cursor phải tự đủ để diễn giải lại sau nhiều năm, nên bắt buộc:

**Định nghĩa stream universe của cursor** — giao của 3 tập:
```
stream được Input Contract chọn (input_contract_ref)
  ∩ tồn tại/đã activate tại cursor boundary
  ∩ resolve được trong stream_registry_version đã pin
```


- **`stream_positions` dùng stable `stream_id`**: key là Logical Stream Identity (ổn định xuyên mọi registry version), giá trị là `sequence`. Cặp `(stream_id, sequence)` là canonical locator (§8.3.1) nên resolve đúng **xuyên qua mọi registry transition** — cursor pin registry v4 vẫn trỏ đúng tới event sequence 500 được append dưới definition v3.
- **`stream_registry_version` ở cấp cursor** dùng để xác định **stream universe** (stream nào thuộc scope, lifecycle/activation của chúng), **KHÔNG** dùng để resolve vị trí event. Hai vai trò này tách biệt: universe resolution cần registry version; position resolution chỉ cần `(stream_id, sequence)`.
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
