---
id: domain-index
title: Domain Contract Index
status: Not Started
created_at: "2026-07-16"
owner: Product Owner
reviewers: [ChatGPT, Claude]
---

# Domain Contract & Glossary — Phase 0.2 (chưa bắt đầu)

Thư mục này sẽ chứa Domain Contract cho từng khái niệm miền, mỗi file = 1 khái niệm, theo format quy định tại [04-domain-principles.md](../constitution/04-domain-principles.md):

```yaml
<TenKhaiNiem>:
  description: "..."
  schema: { ... }
  events: [...]
  invariants: [...]
```

**Thứ tự định nghĩa dự kiến (theo dependency đã chốt ở [ADR-003](../adr/ADR-003.md) và [07-module-taxonomy.md](../constitution/07-module-taxonomy.md)):**

candle.md → swing.md → structure.md → regime.md → feature.md → context.md → strategy.md → decision.md → risk.md → position.md → replay-event.md

Chưa có file nào được tạo — đây là việc tiếp theo sau khi Constitution (bao gồm Chapter 0 Governance) được Approve 3/3.
