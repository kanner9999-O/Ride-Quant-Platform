---
manifest_version: "1.8"
schema_version: "1"
project: "Ride Quant Platform"
project_version: "v0.1"
constitution_version: "1.0.0"
current_phase: "Phase 0 — Vision & Foundation"
compatible_adr_range: "ADR-001 ~ ADR-007"
generated_at: "2026-07-16"
---

# Documentation Manifest (Lockfile)

Nguồn sự thật về tổ hợp version+status chính xác của toàn bộ tài liệu tại một thời điểm — tương tự `package-lock.json` cho code. Mỗi khi một file trong `/docs` đổi version/status, Manifest phải cập nhật cùng lúc, nếu không bị coi là stale.

**Project Version:** Ride Quant Platform v0.1 (Phase 0)
**Constitution Version:** 1.0.0 — độc lập với Project Version (Project có thể lên v0.8 trong khi Constitution vẫn 1.0.0, hoặc ngược lại)
**Schema Version của Manifest:** 1 — đổi format Manifest sau này phải bump field này để tooling không vỡ ngầm.

**Chapter 0 — Governance: `Locked`** (2026-07-16). Các chapter còn lại (01-14) vẫn `In Review`.

## Constitution

| File | Version | Status | Owner | Depends On |
|---|---|---|---|---|
| constitution/00-governance.md | 1.0 | **Locked** | Product Owner | — |
| constitution/01-vision.md | 2.0 | In Review | Product Owner | 00-governance |
| constitution/02-platform-invariants.md | 1.0 | In Review | Product Owner | 00-governance, 01-vision |
| constitution/03-engineering-principles.md | 1.0 | In Review | Product Owner | 02-platform-invariants |
| constitution/04-domain-principles.md | 1.0 | In Review | Product Owner | 02-platform-invariants |
| constitution/05-time-model.md | 1.0 | In Review | Product Owner | 04-domain-principles |
| constitution/06-identity-model.md | 1.0 | In Review | Product Owner | 02-platform-invariants |
| constitution/07-module-taxonomy.md | 1.0 | In Review | Product Owner | 04-domain-principles, 05-time-model |
| constitution/08-event-model.md | 1.0 | In Review | Product Owner | 05-time-model, 06-identity-model, 02-platform-invariants |
| constitution/09-plugin-model.md | 1.0 | In Review | Product Owner | 02-platform-invariants, 07-module-taxonomy |
| constitution/10-compatibility-capability-contract.md | 1.0 | In Review | Product Owner | 09-plugin-model |
| constitution/11-adr-process.md | 1.1 | In Review | Product Owner | 00-governance |
| constitution/12-approval-gates.md | 1.1 | In Review | Product Owner | 00-governance, 11-adr-process |
| constitution/13-quality-gates.md | 1.0 | In Review | Product Owner | 07-module-taxonomy |
| constitution/14-roadmap.md | 1.0 | In Review | Product Owner | ALL |

## ADR

| File | Status | Supersedes | Superseded By |
|---|---|---|---|
| adr/ADR-001.md — Event Sourcing làm nguồn sự thật | Approved | — | — |
| adr/ADR-002.md — Strategy Isolation khỏi Exchange API | Approved | — | — |
| adr/ADR-003.md — Raw Regime Engine tách độc lập | Approved | — | — |
| adr/ADR-004.md — Tri-party Confirmation (bản đầu) | Superseded | — | ADR-005 |
| adr/ADR-005.md — Lean Governance Model | **Locked** | ADR-004 | — |
| adr/ADR-006.md — ChatGPT/Claude ngang hàng (AI Technical Architect) | **Locked** | — | — |
| adr/ADR-007.md — Vision Scope: nội bộ/crypto trước, chừa chỗ mở rộng | **Locked** | — | — |

## Domain

| File | Status |
|---|---|
| domain/ | Not Started — Phase 0.2 chưa bắt đầu |

## Team (tách biệt khỏi Constitution — Role vs Person)

| File | Status |
|---|---|
| team/team.yaml | In Review |
| team/roles.md | In Review |
| team/responsibility-matrix.md | In Review |
| team/onboarding.md | In Review |

## Decision Log

| ADR | Status | Ngày | Tóm tắt |
|---|---|---|---|
| ADR-001 | Approved | (hồi tố) | Event Sourcing làm nguồn sự thật duy nhất |
| ADR-002 | Approved | (hồi tố) | Strategy/Decision Engine không gọi trực tiếp Exchange |
| ADR-003 | Approved | (hồi tố) | Raw Regime Engine tách độc lập khỏi Structure Engine |
| ADR-004 | Superseded | 2026-07-16 | Tri-party Confirmation 3/3 (bản đầu, quá nặng) |
| ADR-005 | Locked | 2026-07-16 | Governance Model — lean, bỏ 3/3, giữ Scale Check |
| ADR-006 | Locked | 2026-07-16 | Product Owner quyết: ChatGPT/Claude ngang hàng, khác focus |
| ADR-007 | Locked | 2026-07-17 | Vision Phase 0-3: nội bộ + crypto only, kiến trúc chừa chỗ multi-tenant/đa tài sản |

## Open Questions

| # | Chủ đề | Trạng thái | Owner | Ghi chú |
|---|---|---|---|---|
| OQ-001 | Data Retention Policy & Access Control Model chi tiết (RBAC cụ thể khi multi-tenant) | Partially Resolved | Product Owner | Hướng đã chốt qua ADR-007: single-operator NGAY BÂY GIỜ, kiến trúc chừa chỗ (Account first-class) cho multi-tenant sau. Thiết kế RBAC cụ thể vẫn mở, cần quyết trước khi thực sự mở multi-tenant (không phải trước Phase 1 nữa). |

## Backlog (Constitution v1.1 — Medium Priority, chưa làm ngay)

| # | Nội dung | Nguồn đề xuất |
|---|---|---|
| BL-001 | `review_status` dạng machine-readable trong metadata (thay vì list `reviewers` dạng text) | ChatGPT review |
| BL-002 | `Traceability` — thêm `related_constitution` / `related_domain` / `related_engine` vào frontmatter ADR để tool trace ảnh hưởng của 1 quyết định | ChatGPT review |

---

**Trạng thái tổng quát:** `In Review` cho toàn Constitution, NHƯNG **Chapter 0 — Governance đã `Locked`** (cùng ADR-005, ADR-006) — đây là chapter đầu tiên khóa chính thức. Từ giờ mọi thay đổi vào 00-governance.md/ADR-005/ADR-006 bắt buộc qua ADR mới (không sửa trực tiếp — ADR Immutable Rule). Chapter 1 — Vision là mục tiêu tiếp theo. Xem [CHANGELOG.md](./CHANGELOG.md) cho lịch sử thay đổi.
