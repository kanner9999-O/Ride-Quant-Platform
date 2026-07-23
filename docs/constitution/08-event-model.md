---
id: 08-event-model
title: Event Model
version: "2.1"
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
| `schema_version` | **Required** | Mọi published event; quy tắc tương thích do Chapter 10 sở hữu |
| `recorded_time` | **Required** | Mọi authoritative event ([Chapter 5](./05-time-model.md)) |
| `subject_ref` | **Required** | Polymorphic + qualified (xem 8.2.2) |
| `stream_id` | **Required** | Mọi authoritative log event (§8.3) |
| `sequence` | **Required** | Mọi authoritative log event (§8.3) |
| `producer_ref` | **Required** | Truy vết authoritative producer (xem 8.2.4) |
| `correlation_id` | **Required** với event thuộc một luồng xử lý; **Optional** với event khởi phát độc lập | §6.7 |
| `causation_refs` | **Zero-to-many** | Root event có thể rỗng (`[]`); không absent (xem 8.2.3) |
| `effective_time` | **Conditional** | Khi domain fact có thời điểm/khoảng hiệu lực. Có thể là instant hoặc interval |
| `market_time` | **Conditional** | CHỈ market-data event, khi source cung cấp — không tạo giả |
| `source_identity` | **Conditional** | Khi source có khả năng retry/redelivery (§6.6) |
| `decision_context_cursor` | **Conditional** | Chỉ Decision event (xem §8.4) |

Implementation KHÔNG được tự suy luận cardinality — field nào thiếu quy định phải bổ sung vào bảng này qua ADR.

### 8.2.2 `subject_ref` — polymorphic, không mặc định account-scoped entity

Không phải authoritative event nào cũng mô tả một entity thuộc một Account. Ví dụ: `MARKET_DATA_OBSERVED` (subject = instrument, scope = venue), `RISK_POLICY_VERSION_ACTIVATED` (subject = policy version), `PLATFORM_KILL_SWITCH_ACTIVATED` (subject = platform).

```yaml
subject_ref:
  context_id:                    # Required — Domain Context (Chapter 4)
  subject_kind:                  # Required — entity | value | policy | stream | instrument | account | platform
  subject_type:                  # Required
  subject_id:                    # Required
  scope:                         # Conditional — chỉ các field mà Event Contract khai báo là cần
    account_id:
    venue_id:
    ...
```

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

### 8.3.2 Mức 1 — Per-stream monotonic sequence

Trong mỗi stream, `sequence` tăng đơn điệu, do writer authority của stream cấp phát. Thứ tự authoritative trong stream = thứ tự `sequence` — deterministic khi replay, không phụ thuộc physical clock. (Hợp lệ theo [§6.1](./06-identity-model.md): ordering assignment được phép cần coordinator, khác identity uniqueness.)

**Integrity của sequence:** gap, duplicate, hoặc regression của `sequence` trong một stream là **integrity violation**, không phải sự cố vận hành bình thường. Khi phát hiện: scope liên quan phải fail-safe theo [I-6](./02-platform-invariants.md) (chặn action tăng risk, vẫn cho risk-reducing action), và không được tự động "vá" bằng cách cấp lại sequence hay bỏ qua gap.

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

```yaml
decision_time:   2026-07-23T10:00:00Z        # effective axis — time value
recorded_time:   2026-07-23T10:00:01.250Z    # recorded axis — time value
decision_context_cursor:                      # KHÔNG phải time — knowledge boundary
  recorded_time: 2026-07-23T10:00:01.100Z
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
  recorded_time:            # knowledge boundary
  stream_positions:         # vị trí chính xác trong TỪNG stream
    <stream_id>: <sequence>
```

Dùng **vector vị trí theo từng stream** (không phải một số duy nhất) vì §8.3 không tuyên bố global total order — cắt chính xác đòi hỏi biết vị trí trong mỗi stream, cho phép dừng đúng ranh giới giữa hai event cùng `recorded_time`.

## 8.6 Các quy tắc thuộc chapter khác — chỉ tham chiếu, không định nghĩa lại

Theo [I-12](./02-platform-invariants.md):
- **Event naming** → [Chapter 3 §3.2](./03-engineering-principles.md).
- **Schema versioning/compatibility** → [Chapter 10](./10-compatibility-capability-contract.md).
- **Payload schema/semantic của từng event_type** → Event Contract tương ứng.
- **Ngữ nghĩa** correlation/causation → [§6.7](./06-identity-model.md); identity/dedup → [Chapter 6](./06-identity-model.md); time semantics → [Chapter 5](./05-time-model.md).
- **Determinism/Parity:** replay cùng event log cho cùng kết quả khi pin đủ **implementation version + configuration + policy version + contract** ([Chapter 3 §3.1](./03-engineering-principles.md)).
- **External Decision Dependency** (I-5) event hóa theo cùng cơ chế như mọi event nội bộ khác.
