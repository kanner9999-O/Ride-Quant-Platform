---
id: 11-adr-process
title: ADR Process
version: "1.1"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-16"
next_review: null
depends_on: ["00-governance"]
---

# 11. ADR Process

Template chuẩn tại [`/docs/templates/adr-template.md`](../templates/adr-template.md) — mỗi ADR là 1 file riêng trong `/docs/adr/ADR-XXX.md`, gồm: Context, Decision, Alternatives considered, Concerns/Risks noted, **Scale check**, Consequences.

**Status của ADR dùng chung Document Lifecycle** tại [Chapter 0, Mục 7](./00-governance.md) (`Not Started → Draft → In Review → Revision Requested → Approved → Locked`, rẽ nhánh `Deprecated`/`Superseded`) — không định nghĩa một "ADR Lifecycle" riêng, theo đúng I-12 (Single Source of Truth).

**Xem [4b. ADR Scope Rule](./00-governance.md) để biết khi nào cần viết ADR** — không phải mọi quyết định đều cần.

**Quy tắc bắt buộc:**
- ADR phải được ghi khi: (a) có quyết định kiến trúc mới, (b) một phase sau muốn sửa quyết định của phase trước.
- **Không phase nào được coi là Approved nếu có quyết định kỹ thuật quan trọng chưa được ghi thành ADR.**
- **Không phase nào được tự ý sửa phase trước** mà không qua quy trình ở [Chapter 0](./00-governance.md).
- ChatGPT Review + Claude Review là bắt buộc trước khi Product Owner quyết (không phải điều kiện approve — chỉ là input bắt buộc phải có).
