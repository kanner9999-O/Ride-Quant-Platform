---
id: 00-governance
title: Governance
version: "1.2"
status: Locked
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: Product Owner
approved_at: "2026-08-18T17:25:00+07:00"
created_at: "2026-07-16"
last_review: "2026-08-18"
next_review: null
depends_on: []
---

# 0. Governance

Chapter 0 — đứng trước cả Vision, vì nó quy định CÁCH mọi quyết định khác được tạo ra.

> **Ghi chú lịch sử:** phiên bản đầu của chương này có luật "Approval 3/3" + Challenge Round (nghi lễ theo vòng) + Devil's Advocate. Sau review của ChatGPT (round 2), các cơ chế này được đơn giản hóa để phù hợp quy mô 1 Product Owner + 2 AI Architect — xem [ADR-005](../adr/ADR-005.md) cho lịch sử quyết định.
>
> **Governance migration:** phiên bản 1.1 kích hoạt mô hình đã được Product Owner chấp thuận tại [ADR-011](../adr/ADR-011.md): ADR file bất biến sau approval, review gate dựa trên role với tối thiểu hai independent reviewers, và MANIFEST là authority cho current ADR/OQ state.
>
> **Governance migration (v1.2, ACTIVE):** phiên bản 1.2 kích hoạt mô hình đã được Product Owner approve tại [ADR-031](../adr/ADR-031.md) (Approved) — mở rộng independent-review eligibility từ principal-only sang Mode A (`DISTINCT_PRINCIPAL`, giữ nguyên preferred khi practical) HOẶC Mode B (`SAME_PRINCIPAL_DISTINCT_EXECUTION`, có execution-isolation evidence contract, ADR-031 §5). Atomic Activation Boundary (ADR-031 §11) hoàn tất TẠI ĐÚNG activation commit này, cùng lúc với Chapter 11 §11.5/§11.9 (v2.2, Locked) và Chapter 12 (v1.6, Locked) wording sync, cùng ADR template evidence-table update — Product Owner decision nguyên văn "ACTIVATE ADR-031 GOVERNANCE MIGRATION," 2026-08-18T17:25:00+07:00.

## 1. Purpose

Quy định cách mọi quyết định kiến trúc/kỹ thuật của Ride Quant Platform được đề xuất, phản biện, và chốt — để đủ chặt không đổ vỡ, nhưng đủ đơn giản để không tốn thời gian quản lý quy trình hơn viết sản phẩm.

## 2. Roles

| Role | Quyền hạn / Nhiệm vụ | Ai đang giữ role này? |
|---|---|---|
| **Product Owner** | Quyết định cuối cùng về scope, priority, và **approve/reject mọi ADR**. Không AI nào có quyền override. | xem [`/team/team.yaml`](../team/team.yaml) |
| **Chief Architect** | Thẩm quyền kỹ thuật cao nhất về tính đúng đắn kiến trúc — vai trò kỹ thuật, tách biệt khỏi Product Owner dù có thể do cùng một người nắm giữ. Tham gia phản biện ngang hàng với AI Technical Architect. | xem `/team/team.yaml` |
| **AI Technical Architect** | Phản biện kiến trúc độc lập, kiểm tra tính nhất quán giữa các Phase/dependency/DDD/CQRS/Event Sourcing, viết tài liệu/thiết kế chi tiết, sau này review implementation. **Có thể có nhiều người/AI cùng giữ role này, tất cả NGANG HÀNG nhau** — không có "Lead" hay hệ thống cấp bậc giữa các AI Technical Architect. Khác nhau ở trọng tâm công việc, không phải cấp bậc. | xem `/team/team.yaml` |
| **Module Owner** | Chịu trách nhiệm kỹ thuật cho 1 Engine/module cụ thể. | Gán theo từng module khi Phase 3 bắt đầu, xem `/team/team.yaml` |
| **Software Engineer / QA Engineer / Research Engineer** | Roles thực thi. Không có quyền tự ý thay đổi kiến trúc; thay đổi thuộc ADR Scope Rule phải qua ADR. | xem `/team/team.yaml` |

**Nguyên tắc:** Constitution chỉ định nghĩa **Role**, không ghi tên người/AI cụ thể trong governance rule. Việc gán Người/AI ↔ Role sống trong `/team/team.yaml`.

> Tên cụ thể trong review evidence là historical attribution, không phải thứ tự ưu tiên hay governance rule vĩnh viễn.

## 2b. Conflict Resolution

Nếu Product Owner và Chief Architect là 2 người khác nhau và bất đồng: Product Owner thắng về business priority, nhưng ADR phải ghi rõ phản đối của Chief Architect theo Concern/Risk.

## 3. Decision Workflow

```text
Requirement
→ Independent AI Technical Architect Reviews
→ Architecture Review
→ Product Owner Decision
→ ADR Accepted
→ ADR Locked
→ Sang Phase tiếp theo
```

*(Accepted = quyết định đã được Product Owner chốt; Locked = current lifecycle state được MANIFEST ghim sau khi decision artifact đã ổn định. Với ADR, file đã bất biến ngay tại approval boundary.)*

**Review gate bắt buộc (v1.2, ACTIVE — xem banner "Governance migration" phía trên):**

- Trước khi Product Owner quyết một ADR hoặc tài liệu thuộc approval gate, phải có tối thiểu **hai independent reviews**.
- Mỗi reviewer phải đang giữ role `AI Technical Architect` tại review boundary — role eligibility LUÔN thuộc về **principal** (person/AI đã đăng ký giữ role tại `/team/team.yaml`), KHÔNG BAO GIỜ thuộc về một execution/session cụ thể; một execution kế thừa eligibility từ principal đã đăng ký của nó, TỰ NÓ KHÔNG có role riêng.
- Independent-review eligibility được thỏa bởi MỘT trong hai independence mode (ADR-031):
  - **Mode A — `DISTINCT_PRINCIPAL`:** hai review do hai principal identity khác nhau thực hiện — vẫn LÀ diversity path preferred khi practical.
  - **Mode B — `SAME_PRINCIPAL_DISTINCT_EXECUTION`:** hai review do CÙNG một principal thực hiện qua hai execution/session cô lập, CHỈ eligible KHI execution-isolation evidence contract (ADR-031 §5) được thỏa đầy đủ — một nhãn tự do (free-form execution label) một mình KHÔNG BAO GIỜ LÀ bằng chứng độc lập.
- Reviewer set cụ thể (principal identity, execution identity nếu Mode B, review boundary, independence mode) phải được pin trong review evidence hoặc metadata của decision boundary.
- Các reviewer ngang hàng; không reviewer nào có veto.
- Product Owner là authority duy nhất approve/reject.
- Nếu KHÔNG resolve được đầy đủ Mode A HOẶC Mode B tại review boundary — bao gồm KHÔNG đủ execution-isolation evidence cho Mode B — decision CHƯA đủ điều kiện đi tới Product Owner approval gate (fail-closed, đúng nguyên tắc "eligibility incomplete," KHÔNG phải reviewer veto).
- Constitution khóa role, minimum cardinality, VÀ hai independence mode hợp lệ (Mode A/Mode B); actor ↔ role assignment sống trong `/team/team.yaml`; execution-isolation evidence contract chi tiết sống trong [ADR-031](../adr/ADR-031.md) (Approved) — Constitution KHÔNG lặp lại nguyên văn evidence contract, chỉ tham chiếu.

Mỗi review output tối thiểu:

```text
Concern:        điều gì đáng lưu ý
Risk:           mức độ ảnh hưởng nếu bỏ qua
Recommendation: nên làm gì
```

Nếu một Concern có Risk cao và liên quan trực tiếp đến vi phạm [Platform Invariant](./02-platform-invariants.md), nhưng Product Owner vẫn quyết định tiến hành, ADR phải ghi rõ `Chấp nhận rủi ro: ...`. Đây là transparency requirement, không phải veto.

## 4. ADR Workflow

Dùng template tại [`/docs/templates/adr-template.md`](../templates/adr-template.md). Mỗi ADR bắt buộc có **Scale check**.

## 4b. ADR Scope Rule — khi nào cần ADR

| Loại | Ví dụ | Có cần ADR? |
|---|---|---|
| **ADR Required** | Thêm/sửa Platform Invariant · thay đổi Event Schema · Module Taxonomy/dependency graph · Governance/Approval process · quyết định ảnh hưởng >1 module hoặc khó đảo ngược · sửa/supersede ADR đã Locked | **Bắt buộc** |
| **ADR Optional** | Thay đổi nội bộ một module không đổi contract nhưng ảnh hưởng đáng kể | Tùy đánh giá |
| **ADR Not Required** | UI thẩm mỹ · refactor không đổi behavior/contract · typo/formatting | **Không cần** |

## 5. Freeze Policy & ADR Immutable Rule

### 5.1 Living documents

Constitution chapter, architecture specification và domain contract là living documents có version. Khi đã `Approved` hoặc `Locked`, không được sửa trực tiếp cùng version. Muốn thay đổi phải tăng version, mở ADR nếu thuộc ADR Scope Rule và đi qua approval gate.

### 5.2 ADR file immutability

ADR là immutable decision record.

```text
Draft / In Review
→ được sửa tại chỗ

Product Owner approval boundary
→ toàn bộ ADR file bị đóng băng byte-for-byte
```

Sau approval:

- không sửa decision content;
- không sửa frontmatter;
- không đổi `status` trong file ADR;
- không thêm `superseded_by`, `deprecated_at` hoặc lifecycle metadata;
- không tạo `rev2/rev3` cho cùng ADR identity.

Muốn thay đổi quyết định phải tạo ADR mới. ADR mới khai báo `supersedes: [ADR-cũ]` khi có quyết định thay thế.

Current lifecycle state (`Approved`, `Locked`, `Superseded`, `Deprecated`) và reverse lookup `superseded_by` được ghi authoritative trong `MANIFEST.md`. File ADR cũ giữ nguyên byte-for-byte từ approval boundary.

Git history là audit evidence, không thay thế authority mapping của I-12.

## 5b. Single Source of Truth — áp dụng trong Governance

Định nghĩa đầy đủ nằm tại **I-12**.

- Decision Log sống trong `MANIFEST.md`.
- Version/status hiện tại của tài liệu được ghim tại `MANIFEST.md`.
- Current lifecycle state của ADR và reverse supersession relation sống tại `MANIFEST.md`.
- Current OQ status sống tại `MANIFEST.md`; ADR giữ decision evidence và transition cause.

**Decision ≠ Documentation:** ADR lưu quyết định; Constitution lưu quy tắc; architecture lưu thiết kế; domain lưu khái niệm nghiệp vụ.

## 6. Disagree and Commit

Sau khi ADR đã Approved, chỉ mở lại khi có sự cố truy vết được về quyết định hoặc yêu cầu mới mâu thuẫn cấu trúc với quyết định cũ.

## 7. Document Lifecycle

### 7.1 Living documents

```text
Not Started → Draft → In Review → Revision Requested → Approved → Locked
                                                              ↓
                                                    Deprecated / Superseded
```

### 7.2 ADR

```text
Draft → In Review → Revision Requested → Approved
```

Tại `Approved`, ADR file freeze vĩnh viễn. `Locked`, `Deprecated`, `Superseded` sau đó là **current lifecycle state tại MANIFEST**, không phải mutation của ADR file.

## 8. Versioning Policy

Living document có SemVer riêng và được ghim tại MANIFEST.

Đối với ADR, `version` chỉ dùng trước approval để nhận diện draft được review. Sau approval không bump version và không sửa file; thay đổi quyết định dùng ADR identity mới.

## 9. Review Policy

Living document có `owner`, `reviewers`, `approved_by`, `last_review`, `next_review`. Với ADR, các field được pin tại approval boundary và sau đó bất biến.
