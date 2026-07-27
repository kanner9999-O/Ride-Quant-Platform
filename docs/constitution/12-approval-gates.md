---
id: 12-approval-gates
title: Approval Gates
version: "1.3"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-27"
next_review: null
depends_on: ["00-governance", "11-adr-process"]
---

# 12. Approval Gates

Mọi Phase kết thúc bằng một cổng phê duyệt trước khi Phase kế tiếp bắt đầu — **không được nhảy phase**.

**Approval Authority:** Product Owner là người approve duy nhất; không AI nào có quyền override (xem [Chapter 0 §2–§3](./00-governance.md) — luật "3/3" của ADR-004 đã được lược bỏ, xem lịch sử ở [ADR-005](../adr/ADR-005.md), và governance migration sang mô hình role-based ở [ADR-011](../adr/ADR-011.md)).

Trước mỗi Approval phải có **tối thiểu hai independent review từ các actor đang giữ role `AI Technical Architect`** tại review boundary, do hai actor identity khác nhau thực hiện và được pin trong review evidence. Đây là **eligibility precondition bắt buộc**: nếu không resolve được tối thiểu hai reviewer đủ điều kiện thì decision **chưa đủ điều kiện** đi tới approval gate. Các reviewer **ngang hàng, không reviewer nào có veto** — sự **tồn tại** của review là điều kiện bắt buộc, còn **kết luận** của review không ràng buộc quyết định cuối cùng của Product Owner.

> Định nghĩa authority của review gate (số lượng, eligibility, no-veto) thuộc [Chapter 0 §3](./00-governance.md) và [Chapter 11 §11.5](./11-adr-process.md). Chương này **tham chiếu, không định nghĩa lại** — tránh tạo authority cạnh tranh. Constitution chỉ khóa **role** và **minimum cardinality**; danh tính reviewer cụ thể chỉ là historical evidence, gán Người/AI ↔ Role sống ở [`/team/team.yaml`](../team/team.yaml).

Mỗi Phase phải có **Definition of Done (DoD)** cụ thể, ví dụ:

- Phase 0 Done khi: Product Requirement + Domain Model + Workflow + UX Blueprint + ADR liên quan + Approved
- Phase 1 Done khi: Architecture + API + Database + Event Flow + ADR + Approved
- Phase 3 (từng module) Done khi: Unit Test theo Tier + Benchmark + Documentation + Demo + Capability Matrix cập nhật + Approved

**Quy tắc bắt buộc:** mọi Phase trong [Roadmap](./14-roadmap.md) phải có DoD cụ thể được viết ra và duyệt **trước khi** Phase đó mở Approval Gate.

## 12.1 Backward Consistency Check

Khi một chapter hoặc invariant mới được Approved/Locked, reviewer phải rà các tài liệu tồn tại (đặc biệt chapter đã viết trước đó nhưng chưa Locked) xem có bị ảnh hưởng không, và ghi kết quả rõ ràng: `No conflict` / `Revision required` / `ADR required`.

*(Bài học rút ra khi Chapter 3 phát hiện mâu thuẫn với Governance đã Locked từ rất lâu mà không ai đối chiếu ngược — một câu tồn tại từ bản thảo đầu tiên, chỉ lộ ra khi tình cờ rà lại. Đặt quy tắc này ở đây, không phải ở một chương Governance đã Locked, để không cần mở ADR chỉ để thêm 1 dòng process — Chapter 12 vẫn `In Review`, sửa trực tiếp được.)*
