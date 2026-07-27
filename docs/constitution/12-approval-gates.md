---
id: 12-approval-gates
title: Approval Gates
version: "1.4"
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

## 12.1 Definition of Done (DoD)

Mỗi Phase phải có **Definition of Done (DoD)** cụ thể. DoD criteria phải được **viết ra và được Product Owner chấp nhận trước khi** phase/gate tương ứng sử dụng chúng — đây là điều kiện *định nghĩa tiêu chí*, không phải *đã đạt tiêu chí*.

- DoD criteria/deliverables là **substantive completion evidence** của phase.
- Evidence được đánh giá **trước** phase approval decision.
- `Approved` là **outcome của Approval Gate**, không phải một mục trong DoD — DoD không được chứa chính outcome của gate (tránh vòng lặp định nghĩa).

Ví dụ evidence (minh họa, không phải danh sách đóng — sequence/DoD cụ thể thuộc roadmap/phase plan, xem §12.3):

- **Phase 0 evidence:** Product Requirement · Domain Model · Use Case & Workflow · UX Blueprint · ADR cho quyết định thuộc ADR Scope Rule ([Chapter 0 §4b](./00-governance.md))
- **Phase 1 evidence:** Architecture · API · Database · Event Flow · ADR liên quan
- **Phase 3 evidence (từng module):** Unit Test theo Tier · Benchmark · Documentation · Demo · Capability Matrix cập nhật

**Quy tắc bắt buộc:** mọi Phase trong [Roadmap](./14-roadmap.md) phải có DoD cụ thể được viết ra và duyệt **trước khi** Phase đó mở Approval Gate.

> Khi applicable evidence và **toàn bộ gate prerequisites (§12.2)** pass, Product Owner mới quyết định phase `Approved` / `Rejected` / `Revision Requested`.

## 12.2 Phase Approval Gate — prerequisite aggregation

Section này chỉ **tổng hợp quan hệ prerequisite** của một phase Approval Gate; nó **không định nghĩa lại** internal rule thuộc chapter/contract khác (xem authority map §12.3).

Trước Product Owner phase decision, **gate eligibility** phải xác nhận:

1. phase-specific DoD criteria đã được định nghĩa và chấp nhận (§12.1);
2. required deliverables/evidence complete (§12.1);
3. required dependencies ở state phù hợp;
4. mọi quyết định thuộc [ADR Scope Rule (Chapter 0 §4b)](./00-governance.md) đã có required ADR và ADR đó đã `Approved` ([Chapter 11 §11.5–§11.6](./11-adr-process.md));
5. applicable quality gates — được yêu cầu bởi một **Approved/Locked authoritative quality contract hoặc phase plan** — đã pass;
6. Backward Consistency Check = `No conflict` (§12.4);
7. applicable validator/MANIFEST freshness checks pass ([Chapter 11 §11.9](./11-adr-process.md), [I-12](./02-platform-invariants.md));
8. minimum-two eligible independent reviews complete và evidence được pin ([Chapter 0 §3](./00-governance.md), [Chapter 11 §11.5](./11-adr-process.md)).

Sau khi eligibility đầy đủ, **Product Owner là authority duy nhất** quyết định: `Approve` · `Reject` · `Revision Requested`.

Ràng buộc:

- **fail closed = eligibility incomplete**, không phải reviewer veto;
- reviewer recommendation **không phải** Product Owner decision;
- validator **không phải** approval authority — chỉ là blocking consistency check;
- **không được bắt đầu phase tiếp theo** trước khi current phase decision/state đã được ghi vào authoritative documentation state (MANIFEST).

## 12.3 Authority boundary

Chapter 12 sở hữu **phase approval orchestration**. Các gate/authority khác chỉ được **tham chiếu**, không định nghĩa lại:

| Concern | Authority |
|---|---|
| Review eligibility (số lượng, role, no-veto) | [Chapter 0 §3](./00-governance.md) / [Chapter 11 §11.5](./11-adr-process.md) |
| ADR approval & lifecycle | [Chapter 11](./11-adr-process.md) |
| Phase approval orchestration | **Chapter 12 (chương này)** |
| Quality criteria/gate | Approved/Locked quality contract — intended owner: Chapter 13 (Quality Gates, hiện `In Review`) |
| Phase-specific sequence & DoD content | Approved roadmap hoặc phase plan — intended owner: Chapter 14 (Roadmap, hiện `In Review`) |
| Governance activation | governing ADR + atomic authoritative state transition ([ADR-011 §4](../adr/ADR-011.md)) |
| Current ADR/OQ state · document version/status | [MANIFEST](../MANIFEST.md) theo [I-12](./02-platform-invariants.md) |

Chapter 13 và Chapter 14 hiện `In Review`: được prose-reference như **intended owner**, nhưng nội dung draft hiện tại **không phải binding Locked authority**. Chapter 12 **không** thêm Chapter 14 vào `depends_on` vì Chapter 14 đã `depends_on` Chapter 12 (tránh dependency cycle).

## 12.4 Backward Consistency Check

Backward Consistency Check có **hai chiều tách biệt**:

### A. Pre-decision consistency với Locked authority

Trước Product Owner decision đối với một candidate document/invariant:

- reviewer phải đối chiếu candidate với các authority đã `Approved`/`Locked` có liên quan;
- result và evidence phải được **pin tại review boundary**;
- `No conflict` → đủ điều kiện tiếp tục;
- `Revision required` → approval gate **vẫn đóng**, candidate quay lại revision;
- `ADR required` → approval gate **vẫn đóng** cho tới khi required ADR được `Approved` và check được chạy lại.

Đây là **eligibility condition, không phải reviewer veto**.

### B. Post-approval propagation tới living documents khác

Sau khi một document/invariant mới được `Approved`/`Locked`:

- reviewer rà ảnh hưởng tới các living documents khác đang `Draft`/`In Review`;
- impact cần revision được ghi thành **explicit follow-up** trong MANIFEST backlog/OQ hoặc authoritative tracking location;
- follow-up này **không tự invalidate** artifact vừa được approve;
- nếu phát hiện conflict với một authority đã `Locked` mà đáng lẽ phải bị bắt ở pre-decision check (A), ghi **integrity violation** và xử lý theo [Chapter 0 governance workflow](./00-governance.md).

Chapter này **không** tự đặt rule mutate document `Locked`; chỉ tham chiếu [Chapter 0 Freeze Policy §5](./00-governance.md) và ADR workflow.

*(Bài học rút ra khi Chapter 3 phát hiện mâu thuẫn với Governance đã Locked từ rất lâu mà không ai đối chiếu ngược — một câu tồn tại từ bản thảo đầu tiên, chỉ lộ ra khi tình cờ rà lại. Chiều A đóng đúng lỗ hổng đó: candidate không thể qua gate nếu còn conflict với authority đã Locked. Đặt quy tắc này ở Chapter 12 — vẫn `In Review` — thay vì ở một chương Governance đã Locked, để không cần mở ADR chỉ để thêm process line.)*
