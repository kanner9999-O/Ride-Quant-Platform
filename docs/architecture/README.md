---
id: architecture-index
status: Draft
owner: Product Owner
created_at: "2026-07-16"
last_review: "2026-08-03"
---
# Architecture — Phase 1 (Active — planning baseline authored, chưa Complete)

Phase 0 Approval Gate `Approved` (2026-08-03, xem [MANIFEST](../MANIFEST.md) "Phase 0 Approval Gate — Decision") — Phase 1 `Active`. Sẽ chứa System Architecture, UX Architecture, Security & Custody Baseline, API/Database/Engine design chi tiết.

**Planning baseline:** [`phase-1-plan.md`](./phase-1-plan.md) (v0.2, Draft) — work breakdown, dependency order, authority map, review/gate structure cho chín package Phase 1 (1.1, 1.2, 1.3-A/B/C/D, 1.4, 1.5, 1.6). Đây là planning artifact, KHÔNG phải architecture decision — architecture design cụ thể chưa author (chờ package tương ứng).

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
