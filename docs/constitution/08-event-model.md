---
id: 08-event-model
title: Event Model
version: "1.2"
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

> **Ràng buộc bắt buộc trước khi Lock (từ Chapter 5):** Chapter này PHẢI giải quyết **OQ-005** (cơ chế ordering authoritative cụ thể — sequence/logical/hybrid clock, cho cả intra-partition determinism lẫn cross-context causal correctness) và cân nhắc **OQ-006** (`decision_time` formal definition, nếu Decision concept được sở hữu tại đây thay vì Chapter 9). Chapter 5 đã định nghĩa *nguyên tắc* ordering; Chapter 8 sở hữu *cơ chế*. Không Lock Chapter 8 khi OQ-005 còn Open.

- **Event Bus là nguồn sự thật duy nhất** (Redpanda — Kafka-API compatible).
- Mọi event: bất biến, có schema versioned, mang `market_time` + `event_time` + correlation ID (phục vụ truy vết quyết định — I-1).
- Naming: `PAST_TENSE_UPPER_SNAKE`.
- Determinism: cùng một event log + cùng phiên bản code phải luôn cho ra cùng kết quả khi replay — cơ chế thực thi [Parity Principle](./02-platform-invariants.md) (I-2).
- External Decision Dependency (I-5) tuân theo cùng cơ chế event hóa như mọi event nội bộ khác.
