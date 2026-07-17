---
id: onboarding
status: In Review
owner: Product Owner
created_at: "2026-07-16"
---
# Onboarding — Thành viên mới

1. Đọc [`/docs/constitution/00-governance.md`](../constitution/00-governance.md) — hiểu Roles, Decision Workflow, ADR Scope Rule.
2. Đọc [`/docs/constitution/02-platform-invariants.md`](../constitution/02-platform-invariants.md) — 12 Invariant KHÔNG được vi phạm dù bất kỳ lý do gì.
3. Xem role của bạn trong [`team.yaml`](./team.yaml).
4. Xem trách nhiệm cụ thể trong [`responsibility-matrix.md`](./responsibility-matrix.md).
5. **Quy tắc quan trọng nhất cho Engineer:** không được tự ý đổi kiến trúc (Module Taxonomy, Event Schema, dependency giữa Engine...) — mọi thay đổi loại này là **ADR Required** (xem 4b trong Governance). Phát hiện vấn đề khi code → viết Technical Proposal → AI Technical Architect review → Product Owner quyết → ADR → mới được refactor.
6. Trạng thái hiện tại của toàn bộ tài liệu: xem [`/docs/MANIFEST.md`](../MANIFEST.md).
