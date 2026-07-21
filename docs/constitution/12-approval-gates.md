---
id: 12-approval-gates
title: Approval Gates
version: "1.2"
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

## 12.1 Backward Consistency Check

Khi một chapter hoặc invariant mới được Approved/Locked, reviewer phải rà các tài liệu tồn tại (đặc biệt chapter đã viết trước đó nhưng chưa Locked) xem có bị ảnh hưởng không, và ghi kết quả rõ ràng: `No conflict` / `Revision required` / `ADR required`.

*(Bài học rút ra khi Chapter 3 phát hiện mâu thuẫn với Governance đã Locked từ rất lâu mà không ai đối chiếu ngược — một câu tồn tại từ bản thảo đầu tiên, chỉ lộ ra khi tình cờ rà lại. Đặt quy tắc này ở đây, không phải ở Governance §4 vốn đã Locked, để không cần mở ADR chỉ để thêm 1 dòng process — Chapter 12 vẫn `In Review`, sửa trực tiếp được.)*
