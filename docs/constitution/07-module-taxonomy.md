---
id: 07-module-taxonomy
title: Module Taxonomy
version: "1.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-16"
next_review: null
depends_on: ["04-domain-principles", "05-time-model"]
---

# 7. Module Taxonomy

Hệ thống có **3 loại module khác nhau** — không phải mọi thứ đều là "Engine":

| Loại | Ví dụ | Đặc điểm |
|---|---|---|
| **Type 1 — Compute Engine** | Structure Engine, Raw Regime Engine, Feature Engine, Strategy Engine | Tính toán thật, publish event mới dựa trên input |
| **Type 2 — Projection** | Context Projection, Portfolio View, Decision View | **Không tính toán gì mới.** Chỉ subscribe events và aggregate thành một read-model (CQRS). Phải luôn rebuild được 100% từ event log. **Tuyệt đối không chứa logic if/else quyết định.** |
| **Type 3 — Runtime Service** | Execution Engine, Plugin Loader, Exchange Adapter, Risk Gateway, Market Data Ingestion | Không phải Engine tính toán, không phải Projection — là dịch vụ vận hành hệ thống. |

> Phân loại chi tiết từng module cụ thể được chốt chính thức ở Phase 0.2 — `/docs/domain/`. Xem [ADR-003](../adr/ADR-003.md) cho quyết định cụ thể về Regime Engine.

**Sơ đồ pipeline tham chiếu:**

```
Market Data
   ├──────────────┐
   ▼              ▼
Structure Engine   Raw Regime Engine   (độc lập — không phụ thuộc lẫn nhau)
   │                    │
   └────────┬───────────┘
            ▼
     Feature Engine (fan-in CÓ CHỌN LỌC)
            ▼
    Context Projection (CQRS, KHÔNG logic, chỉ aggregate)
            ▼
        Strategy ──► Decision ──► Risk Gateway ──► Execution
```
