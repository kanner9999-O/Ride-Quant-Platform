---
id: 12-approval-gates
title: Approval Gates
version: "1.1"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-16"
next_review: null
depends_on: ["00-governance", "11-adr-process"]
---

# 12. Approval Gates

Mọi Phase kết thúc bằng một cổng phê duyệt trước khi Phase kế tiếp bắt đầu — **không được nhảy phase**.

**Approval Authority:** Product Owner là người approve duy nhất (xem [Chapter 0](./00-governance.md) — đã bỏ luật "3/3" từ ADR-004, xem lịch sử ở [ADR-005](../adr/ADR-005.md)). ChatGPT Review + Claude Review là bước bắt buộc phải xảy ra trước mỗi Approval, không phải điều kiện approve.

Mỗi Phase phải có **Definition of Done (DoD)** cụ thể, ví dụ:

- Phase 0 Done khi: Product Requirement + Domain Model + Workflow + UX Blueprint + ADR liên quan + Approved
- Phase 1 Done khi: Architecture + API + Database + Event Flow + ADR + Approved
- Phase 3 (từng module) Done khi: Unit Test theo Tier + Benchmark + Documentation + Demo + Capability Matrix cập nhật + Approved

**Quy tắc bắt buộc:** mọi Phase trong [Roadmap](./14-roadmap.md) phải có DoD cụ thể được viết ra và duyệt **trước khi** Phase đó mở Approval Gate.
