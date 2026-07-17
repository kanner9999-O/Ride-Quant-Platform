---
id: 05-time-model
title: Time Model
version: "1.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-16"
next_review: null
depends_on: ["04-domain-principles"]
---

# 5. Time Model

Bốn khái niệm thời gian phải được phân biệt rõ trong toàn hệ thống:

| Loại thời gian | Định nghĩa |
|---|---|
| **Market Time** | Timestamp do sàn giao dịch cung cấp (exchange-provided) |
| **Event Time** | Thời điểm event được publish vào Event Bus nội bộ |
| **Processing Time** | Thời điểm một engine xử lý xong event đó |
| **Replay Time** | Thời điểm giả lập khi hệ thống chạy lại (replay) event log |

**Quy tắc:**
- Mọi event tối thiểu phải mang cả `market_time` và `event_time` (Dual Timestamping) — bắt buộc để phát hiện dữ liệu trễ/stale khi arbitrage đa sàn.
- Event ordering trong pipeline xử lý theo **Event Time**; **Market Time** dùng để tính độ trễ và phát hiện stale data giữa các sàn.
- Replay dùng lại **Event Time đã ghi trong log**, không dùng đồng hồ hệ thống hiện tại.
