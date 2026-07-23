---
id: 08-event-model
title: Event Model
version: "2.0"
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

> **⚠️ Ràng buộc trước khi Lock:** §8.3 (OQ-005) và §8.4 (OQ-006) là **đề xuất của Claude, CHƯA được Product Owner quyết**. Cả hai thuộc diện **ADR Required** ([Governance §4b](./00-governance.md) — thay đổi Event Model, ảnh hưởng nhiều module). Chapter 8 KHÔNG được Lock cho tới khi Product Owner chốt và ADR tương ứng được ghi.

## 8.1 Authoritative source — event log, KHÔNG phải transport

**Durable append-only event log** là authoritative source cho **runtime facts và decision history** ([I-12](./02-platform-invariants.md)). Transport/broker cụ thể (Redpanda, Kafka, hay công nghệ thay thế sau này) **KHÔNG** tự thân là source of truth — đổi transport không được làm thay đổi authority.

Event log KHÔNG phải "nguồn sự thật duy nhất của toàn platform": theo I-12, mỗi concept có authoritative source riêng (document status → `MANIFEST.md`; architecture decision → ADR; domain concept → Domain Contract; platform rule → Constitution). Event log chỉ authoritative cho runtime facts/decision history.

## 8.2 Event Envelope

Mọi authoritative event mang envelope sau. Field time tuân [Chapter 5](./05-time-model.md); field identity tuân [Chapter 6](./06-identity-model.md) — Chapter 8 chỉ định nghĩa **cách chúng nằm trong schema**, không định nghĩa lại ngữ nghĩa.

```yaml
# --- Record identity (§6.2) ---
event_id:        # bất biến, duy nhất cho mỗi event record
event_type:      # naming theo Chapter 3 §3.2, không định nghĩa lại ở đây
schema_version:  # quy tắc tương thích do Chapter 10 sở hữu

# --- Subject được mô tả (§6.2, §6.1) ---
subject_ref:     # qualified reference — đủ scope để resolve duy nhất
  context_id:
  account_id:
  entity_type:
  entity_id:

# --- Time (Chapter 5) ---
recorded_time:   # BẮT BUỘC với mọi authoritative event
effective_time:  # khi domain fact có thời điểm/khoảng hiệu lực
market_time:     # CHỈ market-data event, khi source cung cấp — không tạo giả

# --- Ordering (§8.3) ---
stream_id:       # event thuộc đúng 1 ordered stream
sequence:        # monotonic trong stream đó

# --- Causality (§6.7) ---
correlation_id:  # nhóm event cùng một luồng xử lý logic
causation_refs:  # TẬP (không phải 1 giá trị) — hỗ trợ multi-source causality

# --- Dedup (§6.6) ---
source_identity: # khi source có khả năng retry/redelivery
```

`causation_refs` là **tập hợp** chứ không phải một trường đơn — bắt buộc để biểu diễn multi-source causality mà §6.7 yêu cầu (ví dụ `ArbitrageDecisionCreated` phụ thuộc đồng thời quote 2 sàn + risk state; ép 1 parent sẽ làm mất causal prerequisite).

## 8.3 Ordering Mechanism — ĐỀ XUẤT (giải OQ-005, chờ Product Owner + ADR)

Chapter 5 §5.4 (Locked) yêu cầu 2 mức: **Mức 1** intra-partition determinism, **Mức 2** cross-context causal correctness. Đề xuất giải bằng **2 cơ chế riêng biệt** thay vì một global clock:

**Mức 1 — Per-stream monotonic sequence.** Mỗi event thuộc đúng 1 ordered stream (`stream_id`); trong stream đó, `sequence` do một single-writer/coordinator của stream cấp phát, tăng đơn điệu. Thứ tự trong stream = thứ tự `sequence`, hoàn toàn deterministic khi replay, không phụ thuộc physical clock. (Cách cấp phát này hợp lệ theo [§6.1](./06-identity-model.md): ordering assignment được phép cần coordinator, khác với identity uniqueness.)

**Mức 2 — Explicit causation references, KHÔNG global total order.** Platform **không tuyên bố** có global total order giữa các stream độc lập. Causal correctness đạt được bằng `causation_refs` tường minh: một consumer không được áp dụng event B như authoritative effect trước khi các causal prerequisite của B (ghi trong `causation_refs`) đã visible hoặc resolvable trong scope của consumer đó.

**Deterministic merge khi replay nhiều stream:** khi cần interleave nhiều stream, Event Contract phải khai báo merge policy deterministic (ví dụ sắp theo `recorded_time`, tie-break bằng `(stream_id, sequence)`). Merge policy này cho **thứ tự ổn định để replay tái lập được**, KHÔNG phải tuyên bố về nhân quả — nhân quả chỉ đến từ `causation_refs`.

**Trade-off đã cân nhắc:** không dùng logical/hybrid logical clock vì (a) causation tường minh đã đủ cho Mức 2 và chính xác hơn (HLC chỉ cho happens-before xấp xỉ), (b) HLC thêm phức tạp vận hành ở scale hiện tại (2-3 sàn), (c) nếu sau này cần, thêm HLC là thay đổi tăng dần, không phá `stream_id`/`sequence`. Đánh đổi: không có global total order — chấp nhận được vì partial order + causation graph đủ cho mọi yêu cầu đã biết.

## 8.4 `decision_time` — ĐỀ XUẤT (giải OQ-006, chờ Product Owner + ADR)

`decision_time` là **Effective Time của một Decision** — thời điểm quyết định có hiệu lực trong domain. Đề xuất định nghĩa formal:

> `decision_time` của một Decision = vị trí knowledge boundary mà Decision đó dựa trên, tức Replay Cursor (§8.5) tại thời điểm Decision Engine đọc xong tập input của nó.

Hệ quả: replay tới đúng cursor đó sẽ tái tạo **chính xác** tập input mà Decision đã thấy — điều kiện cần để [I-2 Decision Parity](./02-platform-invariants.md) kiểm chứng được, và để [I-3](./02-platform-invariants.md) đảm bảo không có input nào "từ tương lai" lọt vào.

Quan hệ với các mốc khác: `decision_time` (effective) ≤ `recorded_time` của chính event Decision đó (Decision được ghi vào log sau khi được tạo ra). Khoảng chênh là latency nội bộ, đo được nhưng không tham gia ordering/replay.

## 8.5 Replay Cursor Representation

[Chapter 5 §5.3](./05-time-model.md) (Locked) định nghĩa: Replay Cursor = Recorded Time boundary + **opaque ordering position** khi cần. Chapter 8 sở hữu representation cụ thể của ordering position đó:

```yaml
replay_cursor:
  recorded_time:            # knowledge boundary
  stream_positions:         # vị trí chính xác trong từng stream
    <stream_id>: <sequence>
```

Dùng **vector vị trí theo từng stream** (không phải một số duy nhất) vì §8.3 không tuyên bố global total order — cắt chính xác đòi hỏi biết vị trí trong mỗi stream. Điều này cho phép replay dừng đúng ranh giới giữa hai event có cùng `recorded_time`.

## 8.6 Các quy tắc thuộc chapter khác — chỉ tham chiếu, không định nghĩa lại

Theo [I-12](./02-platform-invariants.md):
- **Event naming** (`PAST_TENSE_UPPER_SNAKE`) → [Chapter 3 §3.2](./03-engineering-principles.md).
- **Schema versioning/compatibility** → [Chapter 10](./10-compatibility-capability-contract.md).
- **Ngữ nghĩa** correlation/causation → [§6.7](./06-identity-model.md); identity/dedup → [Chapter 6](./06-identity-model.md); time semantics → [Chapter 5](./05-time-model.md).
- **Determinism/Parity:** replay cùng event log cho cùng kết quả khi pin đủ **implementation version + configuration + policy version + contract** ([Chapter 3 §3.1](./03-engineering-principles.md) — không chỉ "cùng phiên bản code").
- **External Decision Dependency** (I-5) event hóa theo cùng cơ chế như mọi event nội bộ khác.
