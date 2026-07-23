---
id: architecture-index
status: Not Started
owner: Product Owner
created_at: "2026-07-16"
---
# Architecture — Phase 1 (chưa bắt đầu)

Sẽ chứa System Architecture, UX Architecture, Security & Custody Baseline, API/Database/Engine design chi tiết khi vào Phase 1.

## Reference Pipeline (bản nháp — chuyển từ Chapter 7, CHƯA phải quyết định kiến trúc chính thức)

Sơ đồ dưới đây là bản nháp định hướng, giữ ở đây thay vì trong Constitution để pipeline có thể thay đổi mà không phải sửa Constitution. Quyết định chính thức thuộc Phase 1 System Architecture (kèm ADR nếu thuộc diện ADR Required).

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
    Context Projection (CQRS, KHÔNG business decision, chỉ aggregate)
            ▼
        Strategy ──► Decision ──► Risk Gateway ──► Execution
```

Xem [ADR-003](../adr/ADR-003.md) cho quyết định Regime Engine độc lập với Structure Engine.
