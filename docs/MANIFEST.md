---
manifest_version: "5.2"
schema_version: "1"
project: "Ride Quant Platform"
project_version: "v0.1"
constitution_version: "1.0.0"
current_phase: "Phase 0 — Vision & Foundation"
compatible_adr_range: "ADR-001 ~ ADR-008"
generated_at: "2026-07-16"
---

# Documentation Manifest (Lockfile)

Nguồn sự thật về tổ hợp version+status chính xác của toàn bộ tài liệu tại một thời điểm — tương tự `package-lock.json` cho code. Mỗi khi một file trong `/docs` đổi version/status, Manifest phải cập nhật cùng lúc, nếu không bị coi là stale.

**Project Version:** Ride Quant Platform v0.1 (Phase 0)
**Constitution Version:** 1.0.0 — độc lập với Project Version (Project có thể lên v0.8 trong khi Constitution vẫn 1.0.0, hoặc ngược lại)
**Schema Version của Manifest:** 1 — đổi format Manifest sau này phải bump field này để tooling không vỡ ngầm.

**Chapter 0 — Governance: `Locked`** (2026-07-16). **Chapter 1 — Vision: `Locked`** (2026-07-17). **Chapter 2 — Platform Invariants: `Locked`** (2026-07-18, 13 invariant). **Chapter 3 — Engineering Principles: `Locked`** (2026-07-18). **Chapter 4 — Domain Principles: `Locked`** (2026-07-18). **Chapter 5 — Time Model: `Locked`** (2026-07-18). Các chapter còn lại (06-14) vẫn `In Review`.

## Constitution

| File | Version | Status | Owner | Depends On |
|---|---|---|---|---|
| constitution/00-governance.md | 1.0 | **Locked** | Product Owner | — |
| constitution/01-vision.md | 2.3 | **Locked** | Product Owner | 00-governance |
| constitution/02-platform-invariants.md | 3.1 | **Locked** | Product Owner | 00-governance, 01-vision |
| constitution/03-engineering-principles.md | 1.4 | **Locked** | Product Owner | 02-platform-invariants |
| constitution/04-domain-principles.md | 2.4 | **Locked** | Product Owner | 02-platform-invariants, 03-engineering-principles |
| constitution/05-time-model.md | 2.4 | **Locked** | Product Owner | 04-domain-principles, 02-platform-invariants |
| constitution/06-identity-model.md | 1.0 | In Review | Product Owner | 02-platform-invariants |
| constitution/07-module-taxonomy.md | 1.0 | In Review | Product Owner | 04-domain-principles, 05-time-model |
| constitution/08-event-model.md | 1.2 | In Review | Product Owner | 05-time-model, 06-identity-model, 02-platform-invariants |
| constitution/09-plugin-model.md | 1.0 | In Review | Product Owner | 02-platform-invariants, 07-module-taxonomy |
| constitution/10-compatibility-capability-contract.md | 1.0 | In Review | Product Owner | 09-plugin-model |
| constitution/11-adr-process.md | 1.1 | In Review | Product Owner | 00-governance |
| constitution/12-approval-gates.md | 1.2 | In Review | Product Owner | 00-governance, 11-adr-process |
| constitution/13-quality-gates.md | 1.0 | In Review | Product Owner | 07-module-taxonomy |
| constitution/14-roadmap.md | 1.1 | In Review | Product Owner | ALL |

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
| adr/ADR-008.md — Phân bổ ngôn ngữ Python/Go, Rust reserved | **Approved** | — | — |

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
| ADR-008 | Approved | 2026-07-18 | Phân bổ ngôn ngữ Python (lõi logic)/Go (biên hệ thống), Rust reserved — ghi hồi tố khi Claude tự review Chapter 3 |

## Open Questions

| # | Chủ đề | Trạng thái | Owner | Ghi chú |
|---|---|---|---|---|
| OQ-001 | Data Retention Policy & Access Control Model chi tiết (RBAC cụ thể khi multi-tenant) | Partially Resolved | Product Owner | Hướng đã chốt qua ADR-007: single-operator NGAY BÂY GIỜ, kiến trúc chừa chỗ (Account first-class) cho multi-tenant sau. Thiết kế RBAC cụ thể vẫn mở, cần quyết trước khi thực sự mở multi-tenant (không phải trước Phase 1 nữa). |
| OQ-002 | Strategy Lifecycle Gate: Capability Matrix phải xác nhận Backtest=YES + Paper Trade=YES trước khi strategy chuyển Live | Open | Product Owner | Chuyển ra khỏi Vision (V2-02) — thuộc về Quality Gates/Strategy Lifecycle, cần ADR khi Phase 3 định nghĩa Strategy Lifecycle |
| OQ-006 | `decision_time` được Chapter 5 liệt kê là canonical field name nhưng CHƯA định nghĩa (đúng chỗ: thuộc chapter sở hữu Decision — Chapter 8 Event Model hoặc Chapter 9 Plugin/Decision). Phải định nghĩa formal + quan hệ với recorded_time trước khi chapter đó Lock | Open | Product Owner | ChatGPT Observation khi review Chapter 5 v2.4 — tránh decision_time rơi vào khoảng trống như OQ-005 |
| OQ-005 | Cơ chế ordering authoritative cụ thể (sequence number per partition / logical clock / hybrid logical clock) cho cross-node/cross-exchange event ordering — Chapter 5 đã định nghĩa NGUYÊN TẮC (total order deterministic, không dựa thuần physical clock), cơ chế cụ thể quyết định ở Chapter 8 Event Model | Open | Product Owner | Phát hiện: Claude tự soi Chapter 5 v2.1, ChatGPT xác nhận Major. Quan trọng cho arbitrage đa sàn (thứ tự event = lãi/lỗ) |
| OQ-004 | Time Model (Chapter 5) cần bổ sung rõ bitemporal: effective/event time vs knowledge/recorded time | Resolved (Chapter 5 v2.0) | Product Owner | Đã xử lý: §5.1 Bitemporal Model canonical hóa Effective/Recorded Time, hòa giải thuật ngữ với I-3 Locked, §5.3 định nghĩa vận hành Replay theo trục Recorded |
| OQ-003 | Product Metrics cụ thể cho nguyên tắc "Measurable" (vd: decision-rationale coverage rate, risk-policy violation rate, replay-to-live parity deviation, thời gian hypothesis→validated strategy...) | Open | Product Owner | Chuyển ra khỏi Vision (V2-05) — cần tài liệu Product Metrics riêng, không nhét KPI chi tiết vào Vision |

## Backlog (Constitution v1.1 — Medium Priority, chưa làm ngay)

| # | Nội dung | Nguồn đề xuất |
|---|---|---|
| BL-001 | `review_status` dạng machine-readable trong metadata (thay vì list `reviewers` dạng text) | ChatGPT review |
| BL-005 | Processing Observation (Chapter 5 §5.2) cần schema đầy đủ + observability convention (processor/attempt/started_at/completed_at) — thuộc Engineering Foundation (Phase 1.5), không phải Constitution | ChatGPT Observation (Chapter 5 v2.4) |
| BL-004 | context-map.yaml có thể tách file (capabilities/ contexts/ relationships riêng) KHI file quá lớn — chưa làm vì file chưa tồn tại, tránh giải quyết vấn đề chưa đo được. Xử lý ở Engineering Foundation/Phase 0.2 khi có dữ liệu thật | ChatGPT review (Chapter 4 round 4) |
| BL-003 | Invariant Conformance Matrix (Invariant → Architecture mechanism → Owning module → Enforcement → Automated test → Runtime metric/alert → Evidence location) — thuộc Architecture/Engineering Phase, KHÔNG phải Constitution. Chỉ làm khi module/contract thật đã tồn tại, không điền tên ADR/tài liệu chưa tạo (tránh tham chiếu giả) | ChatGPT review (Chapter 2 round 3) |
| BL-002 | `Traceability` — thêm `related_constitution` / `related_domain` / `related_engine` vào frontmatter ADR để tool trace ảnh hưởng của 1 quyết định. **Mở rộng (Vision review round 2):** nên trace được cả chiều Principle → ADR → Architecture (vd: "Everything Must Be Explainable" → I-1 → Decision Log/Replay/Context Projection) | ChatGPT review |

---

**Trạng thái tổng quát:** `In Review` cho Chapter 06-14, NHƯNG **Chapter 0, 1, 2, 3, 4, 5 đã `Locked`** — cùng ADR-005, ADR-006, ADR-007, ADR-008. Từ giờ mọi thay đổi vào các file đã Locked bắt buộc qua ADR mới. Chapter 6 — Identity Model là mục tiêu tiếp theo. Lưu ý: Chapter 8 (Event Model) KHÔNG được Lock khi OQ-005/OQ-006 còn Open. Xem [CHANGELOG.md](./CHANGELOG.md).
