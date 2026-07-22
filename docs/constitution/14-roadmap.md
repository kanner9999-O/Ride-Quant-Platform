---
id: 14-roadmap
title: Roadmap
version: "1.1"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-16"
next_review: null
depends_on: ["00-governance", "01-vision", "02-platform-invariants", "03-engineering-principles", "04-domain-principles", "05-time-model", "06-identity-model", "07-module-taxonomy", "08-event-model", "09-plugin-model", "10-compatibility-capability-contract", "11-adr-process", "12-approval-gates", "13-quality-gates"]
---

# 14. Roadmap

```
Phase 0 — Vision & Foundation
  Product Requirement · Domain Model (/docs/domain/) · Use Case & Workflow · UX Blueprint
  → ADR cho quyết định Domain thuộc diện ADR Required (theo Governance §4b, không phải mọi định nghĩa)
  → Approval Gate

Phase 1 — System Architecture
  Software · UX Architecture · Security & Custody Baseline · API · Database · Engine
  → ADR cho quyết định kiến trúc thuộc diện ADR Required (theo Governance §4b)
  → Approval Gate

Phase 1.5 — Engineering Foundation (tài liệu SỐNG, sửa qua ADR)
  Monorepo · Coding Standard · Naming · Logging · Config · Error Handling · Testing · CI/CD
  → Approval Gate

Phase 2 — Product Prototype (HTML/React/Figma — công cụ không quan trọng)
  → Approval Gate

Phase 3 — Core Backend (build ĐÚNG theo dependency graph ở 07-module-taxonomy.md)
  Data Layer → Structure Engine & Raw Regime Engine (song song, độc lập)
             → Feature Engine → Context Projection
             → Strategy → Decision → Risk Gateway → Execution
  → Quality Gate theo Tier (13-quality-gates.md)
  → Approval Gate

Phase 4 — Frontend
  → Approval Gate

Phase 5 — Integration

Phase 6 — Simulation Platform
  Replay · Backtest · Walk-Forward · Paper Trade · Monte Carlo · Stress Test · Scenario Test
  → Kiểm chứng Parity Principle (I-2) tại đây

Phase 7 — Deployment

Phase 8 — Research Platform (tách biệt khỏi Production)
  Strategy Comparison · Parameter/Genetic Optimization · Feature Importance
  · Regime Analysis · Performance Attribution

Phase 9 — Observability
  Metrics · Logs · Tracing · Alerts · Dashboard · Health

Ghi chú:
  - AI Layer KHÔNG là một Phase riêng — theo Invariant I-7, nó chỉ là
    consumer mới của Event Bus, trừ khi tham gia Decision (khi đó là
    Decision Advisor, theo 09-plugin-model.md).
```
