---
id: 08-event-model
title: Event Model
version: "2.2"
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

## 8.2 Event Envelope

**Phân chia thẩm quyền:** Chapter 8 sở hữu **envelope (metadata)**; **Event Contract** của từng `event_type` sở hữu **payload schema/semantic**; [Chapter 10](./10-compatibility-capability-contract.md) sở hữu **compatibility/version rules**. Chapter 8 KHÔNG định nghĩa payload của bất kỳ domain event cụ thể nào.

```yaml
metadata:            # Chapter 8 sở hữu
  event_id:
  event_type:
  schema_version:
  subject_ref: {...}
  recorded_time:
  stream_id:
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
| `schema_version` | **Required** | Mọi authoritative event record (kể cả event nội bộ không đi qua public bus — vẫn cần cho replay/migration). Quy tắc tương thích do Chapter 10 sở hữu |
| `recorded_time` | **Required** | Mọi authoritative event ([Chapter 5](./05-time-model.md)) |
| `subject_ref` | **Required** | Polymorphic + qualified (xem 8.2.2) |
| `stream_id` | **Required** | Mọi authoritative log event (§8.3) |
| `sequence` | **Required** | Mọi authoritative log event (§8.3) |
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
  - stream_id: binance-btc-book
    sequence: 98123
    event_id: evt_001
```

### 8.2.4 `producer_ref` — truy vết implementation đã sinh event

[Chapter 3 §3.1](./03-engineering-principles.md) (Locked) cho phép shadow/experimental/migration implementation tồn tại song song với authoritative implementation. Không có producer identity thì không phân biệt được event nào do authoritative implementation sinh ra — phá [I-1](./02-platform-invariants.md) và parity audit.

```yaml
producer_ref:
  module_id:                # theo module-registry.yaml (Chapter 7 §7.5)
  implementation_version:
  run_id:
  # instance_id: operational metadata, KHÔNG phải domain identity — thuộc telemetry
```

## 8.3 Ordering Mechanism — ĐỀ XUẤT (giải OQ-005, chờ Product Owner + ADR)

[Chapter 5 §5.4](./05-time-model.md) (Locked) yêu cầu 2 mức: **Mức 1** intra-partition determinism, **Mức 2** cross-context causal correctness. Đề xuất giải bằng **2 cơ chế riêng biệt**, không dùng global clock:

### 8.3.1 Stream — định nghĩa và thẩm quyền

Một **stream** là một ordered log partition có đúng **một writer authority** cấp phát `sequence`. Mỗi authoritative event thuộc **đúng một** stream.

- Danh sách stream và writer authority tương ứng được khai báo trong **Event Contract / stream registry**, không hardcode trong Constitution.
- Tạo/xóa/tách stream là thay đổi Event Model → **ADR Required**.
- Một module có thể ghi vào nhiều stream, nhưng mỗi stream chỉ có 1 writer authority (điều kiện để `sequence` monotonic).

### 8.3.2 Mức 1 — Per-stream contiguous sequence

Trong mỗi stream, `sequence` là **số nguyên liên tiếp, tăng nghiêm ngặt**: với hai record kế tiếp nhau, `next_sequence = previous_sequence + 1`. Thứ tự authoritative trong stream = thứ tự `sequence` — deterministic khi replay, không phụ thuộc physical clock. (Hợp lệ theo [§6.1](./06-identity-model.md): ordering assignment được phép cần coordinator, khác identity uniqueness.)

**Chọn contiguous (Option A) thay vì "strictly increasing, cho phép gap" (Option B) — đề xuất:** trong hệ thống giao dịch, một event thiếu có thể là một fill bị mất, ảnh hưởng trực tiếp Position Ledger. Với contiguous sequence, mất event bị phát hiện **ngay lập tức** bằng phép kiểm tra rẻ nhất có thể (`next != prev + 1`), không cần cơ chế checksum chain phụ. Đánh đổi: writer authority phải cấp `sequence` **atomically cùng lúc với append** — không được reserve trước rồi ghi sau (reserve-then-crash sẽ tạo lỗ hổng vĩnh viễn).

Hệ quả bắt buộc với implementation:
- Sequence allocation và append phải nằm trong cùng một atomic operation.
- Transaction abort không được để lại sequence đã tiêu.
- Compaction/retention không được đổi `sequence` của record còn lại.
- Restore/migration phải giữ nguyên `sequence` gốc.

**Integrity:** gap, duplicate, hoặc regression của `sequence` là **integrity violation**, không phải sự cố vận hành bình thường. Khi phát hiện: scope liên quan phải fail-safe theo [I-6](./02-platform-invariants.md) (chặn action tăng risk, vẫn cho risk-reducing action), và không được tự động "vá" bằng cách cấp lại sequence hay bỏ qua gap.

### 8.3.3 Mức 2 — Explicit causation, KHÔNG global total order

Platform **không tuyên bố** có global total order giữa các stream độc lập. Causal correctness đến từ `causation_refs` tường minh (§8.2.3).

### 8.3.4 Merge order ≠ authoritative causal order

Khi replay/consume nhiều stream, cần một **merge policy deterministic** để interleave — policy này phải được khai báo trong **Event Contract / Replay Contract**, không có default ngầm (Chapter 5 đã khóa: ordering giữa event visible dựa trên Ordering Authority, không phải so `recorded_time` trực tiếp).

**Merge order chỉ quyết định delivery/interleave order — KHÔNG phải authoritative business order.**

Quy tắc bắt buộc cho processor:
- Trước khi authoritative-apply một event có causal prerequisites, processor phải xác nhận **mọi** prerequisite trong `causation_refs` đã visible và resolved tại cursor hiện tại.
- Nếu prerequisite chưa available: event phải được **buffer/defer**, hoặc replay cursor/merge plan phải được điều chỉnh. **Cấm apply speculative.**
- Nếu một prerequisite vẫn unresolved tại một cursor được coi là **complete**: đây là **integrity violation** → fail-safe theo I-6, không được bỏ qua.

## 8.4 Decision time fields — ĐỀ XUẤT (giải OQ-006, chờ Product Owner + ADR)

Ba khái niệm khác nhau, **không được gộp**:

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
decision_context_cursor:                      # KHÔNG phải time — knowledge boundary
  recorded_time: 2026-07-23T10:00:01.100Z
  stream_registry_version: v3
  stream_positions:
    binance-btc: 18721
    bybit-btc:   9481
    risk-state:  443
```

**Vì sao cần `decision_context_cursor` riêng:** replay tới đúng cursor này tái tạo **chính xác** tập input mà Decision đã thấy — điều kiện cần để [I-2 Decision Parity](./02-platform-invariants.md) kiểm chứng được và [I-3](./02-platform-invariants.md) đảm bảo không có input "từ tương lai".

**Cấm gọi Replay Cursor là `decision_time`:** Replay Cursor là cấu trúc vector, không so sánh trực tiếp được với timestamp; `decision_time` theo Chapter 5 (Locked) phải là time value trên trục effective. Đổi ngữ nghĩa `decision_time` sẽ là thay đổi field canonical đã Locked → cần ADR riêng, không được làm ngầm trong Chapter 8.

## 8.5 Replay Cursor Representation

[Chapter 5 §5.3](./05-time-model.md) (Locked): Replay Cursor = Recorded Time boundary + **opaque ordering position** khi cần. Chapter 8 sở hữu representation của ordering position:

```yaml
replay_cursor:
  recorded_time:                  # knowledge boundary
  stream_registry_version:        # stream universe mà cursor này gắn vào
  stream_positions:               # vị trí chính xác trong TỪNG stream thuộc registry version đó
    <stream_id>: <sequence>
```

Dùng **vector vị trí theo từng stream** (không phải một số duy nhất) vì §8.3 không tuyên bố global total order — cắt chính xác đòi hỏi biết vị trí trong mỗi stream, cho phép dừng đúng ranh giới giữa hai event cùng `recorded_time`.

### 8.5.1 Cursor validity với dynamic stream set

Stream topology thay đổi được (tạo/tách/retire stream — §8.3.1, ADR Required). Một cursor phải tự đủ để diễn giải lại sau nhiều năm, nên bắt buộc:

- **`stream_registry_version`**: cursor gắn với đúng một phiên bản stream registry. Stream không thuộc registry version của cursor **không tham gia** boundary — replay cursor 2026 vẫn diễn giải được bằng registry 2026 dù registry hiện tại đã khác.
- **Stream thuộc scope nhưng chưa có event visible**: phải biểu diễn tường minh bằng **genesis position** (giá trị quy ước trong Event Contract, ví dụ `0`), **KHÔNG được để field vắng mặt** — vắng mặt là mơ hồ giữa "chưa có event" và "quên ghi".
- **Consistency invariant:** mọi `stream_positions[s]` phải trỏ tới event có `recorded_time ≤ recorded_time` của cursor. Cursor vi phạm điều này là **invalid cursor** (không phải "cursor lạ") — phải bị từ chối, không được replay best-effort.

## 8.6 Các quy tắc thuộc chapter khác — chỉ tham chiếu, không định nghĩa lại

Theo [I-12](./02-platform-invariants.md):
- **Event naming** → [Chapter 3 §3.2](./03-engineering-principles.md).
- **Schema versioning/compatibility** → [Chapter 10](./10-compatibility-capability-contract.md).
- **Payload schema/semantic của từng event_type** → Event Contract tương ứng.
- **Ngữ nghĩa** correlation/causation → [§6.7](./06-identity-model.md); identity/dedup → [Chapter 6](./06-identity-model.md); time semantics → [Chapter 5](./05-time-model.md).
- **Determinism/Parity:** replay cùng event log cho cùng kết quả khi pin đủ **implementation version + configuration + policy version + contract** ([Chapter 3 §3.1](./03-engineering-principles.md)).
- **External Decision Dependency** (I-5) event hóa theo cùng cơ chế như mọi event nội bộ khác.
