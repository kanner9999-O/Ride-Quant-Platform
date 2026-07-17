---
id: 04-domain-principles
title: Domain Principles
version: "1.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-16"
next_review: null
depends_on: ["02-platform-invariants"]
---

# 4. Domain Principles

- **Ubiquitous Language:** một thuật ngữ = một nghĩa duy nhất trong toàn bộ dự án. Không có chuyện Structure Engine hiểu "Swing" khác Feature Engine.
- **Domain Model = Domain Contract:** mỗi khái niệm miền không chỉ có `description` và `schema`, mà bắt buộc có `events` (những event nó phát sinh) và `invariants` (quy tắc bất biến của riêng khái niệm đó). Ví dụ:

```yaml
Swing:
  description: "..."
  schema: { ... }
  events: [SwingCreated, SwingInvalidated]
  invariants:
    - "Một Swing không bao giờ bị sửa sau khi publish, chỉ có thể invalidate bằng event mới"
```

- **Glossary hợp nhất với Domain Model** — không tách thành hai tài liệu riêng, vì tách ra dễ khiến chúng lệch nhau theo thời gian. Mỗi file trong `/docs/domain/` (ví dụ `swing.md`) là Domain Contract đầy đủ cho khái niệm đó.
- Domain Modeling phải hoàn thành **trước** UX Blueprint, vì UX giả định các khái niệm này đã được định nghĩa rõ ràng.
