---
id: roles-definition
status: In Review
owner: Product Owner
created_at: "2026-07-16"
---
# Role Definitions

Định nghĩa chi tiết từng Role — nguồn sự thật chính thức là [`/docs/constitution/00-governance.md`](../constitution/00-governance.md) Mục 2 (Roles). File này chỉ diễn giải thêm cho người mới, không định nghĩa lại (I-12).

| Role | Xem định nghĩa tại |
|---|---|
| Product Owner | constitution/00-governance.md §2 |
| Chief Architect | constitution/00-governance.md §2 |
| AI Technical Architect | constitution/00-governance.md §2 |
| Module Owner | constitution/00-governance.md §2 |
| Software / QA / Research Engineer | constitution/00-governance.md §2 |

**Reviewer-identity alias (F-04, 2026-08-03):** khi review evidence pin một reviewer identity không khớp trực tiếp tên actor trong [`team.yaml`](./team.yaml) (ví dụ `"Independent Review B"` tại ADR-012/ADR-013), identity đó resolve qua field `aliases` của member entry tương ứng trong `team.yaml` — KHÔNG phải một actor/role mới. `team.yaml` là nguồn resolve DUY NHẤT cho alias ↔ actor mapping (I-12).
