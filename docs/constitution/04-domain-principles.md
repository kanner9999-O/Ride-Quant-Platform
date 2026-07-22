---
id: 04-domain-principles
title: Domain Principles
version: "2.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-18"
next_review: null
depends_on: ["02-platform-invariants"]
---

# 4. Domain Principles

## 4.1 Ubiquitous Language

Một thuật ngữ = một nghĩa duy nhất trong toàn bộ dự án. Không có chuyện Structure Engine hiểu "Swing" khác Feature Engine.

## 4.2 Domain Contract (thuật ngữ canonical — không dùng "Domain Model" song song)

Mỗi khái niệm miền phải có đầy đủ:
- `description` — mô tả khái niệm.
- `schema` — cấu trúc dữ liệu, kèm khai báo rõ **type/precision** cho giá trị tài chính authoritative (theo [I-9 Numerical Precision](./02-platform-invariants.md) — decimal/fixed-point, không phải float).
- `events` — những event khái niệm này phát sinh.
- `invariants` — quy tắc bất biến của riêng khái niệm đó.
- `state_machine` — tập state hợp lệ + tập transition hợp lệ (bắt buộc theo [I-13 State Transition Integrity](./02-platform-invariants.md) nếu khái niệm có vòng đời trạng thái).

```yaml
Swing:
  description: "..."
  schema: { ... }
  events: [SwingCreated, SwingInvalidated]
  invariants:
    - "Một Swing không bao giờ bị sửa sau khi publish, chỉ có thể invalidate bằng event mới"
  state_machine:
    states: [CANDIDATE, CONFIRMED, INVALIDATED]
    transitions:
      - from: CANDIDATE
        to: CONFIRMED
      - from: CANDIDATE
        to: INVALIDATED
      - from: CONFIRMED
        to: INVALIDATED
    terminal_states: [INVALIDATED]
```

**Glossary hợp nhất với Domain Contract** — không tách thành hai tài liệu riêng, vì tách ra dễ khiến chúng lệch nhau theo thời gian. Mỗi file trong `/docs/domain/` (ví dụ `swing.md`) là Domain Contract đầy đủ cho khái niệm đó — đây là authoritative source duy nhất cho khái niệm miền đó (theo [I-12](./02-platform-invariants.md)).

## 4.3 Business Capability (canonical hóa thuật ngữ Chapter 3 đã hoãn)

Chapter 3 (Locked) chủ động tránh dùng "bounded context" trước khi chapter này canonical hóa nó. Đây là định nghĩa chính thức, dùng thuật ngữ **Business Capability** (tương đương khái niệm "bounded context" trong DDD cổ điển, nhưng chọn tên riêng để nhất quán với ngôn ngữ đã dùng ở Chapter 3, tránh tồn tại song song 2 thuật ngữ cho cùng 1 khái niệm):

- **Định nghĩa:** một Business Capability là một phạm vi trách nhiệm nghiệp vụ rõ ràng, sở hữu một tập Domain Contract riêng, và (khi có nhân sự) do một Module Owner phụ trách (xem [Governance §2](./00-governance.md)).
- **Ranh giới:** xác định bởi single responsibility — một capability chỉ nên trả lời một loại câu hỏi nghiệp vụ (ví dụ: Strategy/Decision capability trả lời "nên trade gì", Risk Policy capability trả lời "có được phép trade không", Execution capability trả lời "trade thế nào trên sàn").
- **Giao tiếp giữa các capability:** chỉ qua published contract — event, query/read contract, hoặc command contract đã công bố (nhất quán với [I-4 Strategy Isolation](./02-platform-invariants.md) và [I-7 Plugin Non-Bypass](./02-platform-invariants.md)) — không truy cập trực tiếp state/implementation nội bộ của capability khác.
- **Ví dụ capability đã xác định** (từ [03-engineering-principles.md](./03-engineering-principles.md) §3.1): Strategy/Decision, Risk Policy, Market Data, Execution/Venue.

## 4.4 Trình tự Domain Modeling

Domain Modeling (Business Capability + Domain Contract) phải hoàn thành trước UX Blueprint — thứ tự này đã quy định tại [Roadmap, Phase 0](./14-roadmap.md), không lặp lại ở đây ngoài việc trỏ tham chiếu. Lý do: UX Blueprint giả định các khái niệm miền đã được định nghĩa rõ ràng.
