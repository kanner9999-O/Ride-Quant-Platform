---
id: architecture-index
status: Draft
owner: Product Owner
created_at: "2026-07-16"
last_review: "2026-08-03"
---
# Architecture — Phase 1 (Active — planning baseline authored, chưa Complete)

Phase 0 Approval Gate `Approved` (2026-08-03, xem [MANIFEST](../MANIFEST.md) "Phase 0 Approval Gate — Decision") — Phase 1 `Active`. Sẽ chứa System Architecture, UX Architecture, Security & Custody Baseline, API/Database/Engine design chi tiết.

**Planning baseline:** [`phase-1-plan.md`](./phase-1-plan.md) (v0.2, Draft — package lifecycle `Consolidated Stable`, xem [MANIFEST](../MANIFEST.md) cho review evidence đầy đủ) — work breakdown, dependency order, authority map, review/gate structure cho chín package Phase 1 (1.1, 1.2, 1.3-A/B/C/D, 1.4, 1.5, 1.6). Đây là planning artifact, KHÔNG phải architecture decision — architecture design cụ thể chưa author (chờ package tương ứng).

**Package 1.1 — System Decomposition & Module Registry (candidate, v0.2, 2026-08-03 — bounded correction đóng `P11-A-MAJ-01`/`P11-A-MAJ-02`/`P11-A-MIN-01`, CHƯA verified):** [`module-registry.yaml`](./module-registry.yaml) + [`system-decomposition.md`](./system-decomposition.md) (cả hai v0.2, Draft) — 22 module, dependency graph, Product/UC/UX/Domain coverage (34 PR/21 UC/17 screen/11 capability/15 context, zero orphan). **CANDIDATE — KHÔNG Consolidated Stable, KHÔNG Approved.** `system-decomposition.md` §12 vẫn phát hiện HAI quyết định `ADR REQUIRED` (module dependency graph chính thức; `decision-engine` hybrid taxonomy, không đổi bởi correction này) — Package 1.1 KHÔNG thể Consolidated Stable cho tới khi ADR liên quan `Approved`. KHÔNG ADR nào được tạo/approve tại transaction này. `risk-gateway` KHÔNG còn `hybrid` (đóng `P11-A-MAJ-01` — Runtime Service taxonomy tự nó cho phép authoritative business policy, không cần khai báo hybrid/ADR); Plugin Definition identity/taxonomy authority nay DUY NHẤT ở `module-registry.yaml` (đóng `P11-A-MAJ-02`, module đổi tên `plugin-registry-service` → `plugin-release-manager`, thu hẹp về operational fact only).

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
