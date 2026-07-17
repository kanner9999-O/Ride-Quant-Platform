---
id: 13-quality-gates
title: Quality Gates
version: "1.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-16"
next_review: null
depends_on: ["07-module-taxonomy"]
---

# 13. Quality Gates

Coverage yêu cầu phân theo **mức độ nguy hiểm**, không dùng một ngưỡng chung cho toàn hệ thống:

| Tier | Thành phần | Coverage tối thiểu | Yêu cầu thêm |
|---|---|---|---|
| Tier 0 — Critical | Risk Gateway, Execution Engine, Position Ledger | ≥ 95% | Bắt buộc Chaos Test (exchange timeout, partial fill, duplicate order, order reject) |
| Tier 1 — Core Logic | Strategy Engine, Feature Engine, Structure Engine, Regime Engine | ≥ 90% | Bắt buộc Parity Test (Replay phải khớp Live) |
| Tier 2 — Supporting | API layer, Data Ingestion | ≥ 80% | |
| Tier 3 — UI | Frontend | ≥ 60% | Ưu tiên E2E test hơn unit test |

**Performance Gate:** không được merge nếu benchmark chậm hơn version liền trước (regression check bắt buộc trong CI/CD).
