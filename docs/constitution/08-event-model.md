---
id: 08-event-model
title: Event Model
version: "1.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-16"
next_review: null
depends_on: ["05-time-model", "06-identity-model", "02-platform-invariants"]
---

# 8. Event Model

- **Event Bus là nguồn sự thật duy nhất** (Redpanda — Kafka-API compatible).
- Mọi event: bất biến, có schema versioned, mang `market_time` + `event_time` + correlation ID (phục vụ truy vết quyết định — I-1).
- Naming: `PAST_TENSE_UPPER_SNAKE`.
- Determinism: cùng một event log + cùng phiên bản code phải luôn cho ra cùng kết quả khi replay — cơ chế thực thi [Parity Principle](./02-platform-invariants.md) (I-2).
- External Decision Dependency (I-5) tuân theo cùng cơ chế event hóa như mọi event nội bộ khác.
