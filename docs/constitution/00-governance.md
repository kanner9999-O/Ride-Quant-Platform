---
id: 00-governance
title: Governance
version: "1.0"
status: Locked
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: Product Owner
approved_at: "2026-07-16"
created_at: "2026-07-16"
last_review: "2026-07-16"
next_review: null
depends_on: []
---

# 0. Governance

Chapter 0 — đứng trước cả Vision, vì nó quy định CÁCH mọi quyết định khác được tạo ra.

> **Ghi chú lịch sử:** phiên bản đầu của chương này có luật "Approval 3/3" + Challenge Round (nghi lễ theo vòng) + Devil's Advocate. Sau review của ChatGPT (round 2), các cơ chế này được đơn giản hóa để phù hợp quy mô 1 Product Owner + 2 AI Architect — xem [ADR-005](../adr/ADR-005.md) cho lịch sử quyết định.

## 1. Purpose

Quy định cách mọi quyết định kiến trúc/kỹ thuật của Ride Quant Platform được đề xuất, phản biện, và chốt — để đủ chặt không đổ vỡ, nhưng đủ đơn giản để không tốn thời gian quản lý quy trình hơn viết sản phẩm.

## 2. Roles

| Role | Quyền hạn / Nhiệm vụ | Ai đang giữ role này? |
|---|---|---|
| **Product Owner** | Quyết định cuối cùng về scope, priority, và **approve/reject mọi ADR**. Không AI nào có quyền override. | xem [`/team/team.yaml`](../team/team.yaml) |
| **Chief Architect** | Thẩm quyền kỹ thuật cao nhất về tính đúng đắn kiến trúc — vai trò kỹ thuật, tách biệt khỏi Product Owner dù có thể do cùng một người nắm giữ. Tham gia phản biện ngang hàng với AI Technical Architect. | xem `/team/team.yaml` |
| **AI Technical Architect** | Phản biện kiến trúc độc lập, kiểm tra tính nhất quán giữa các Phase/dependency/DDD/CQRS/Event Sourcing, viết tài liệu/thiết kế chi tiết, sau này review implementation. **Có thể có nhiều người/AI cùng giữ role này, tất cả NGANG HÀNG nhau** — không có "Lead" hay hệ thống cấp bậc giữa các AI Technical Architect, để giữ giá trị cốt lõi của việc có nhiều góc nhìn độc lập phản biện lẫn nhau. Khác nhau ở trọng tâm công việc (ví dụ: Discovery-focus, Documentation-focus), không phải cấp bậc. | xem `/team/team.yaml` |
| **Module Owner** | Chịu trách nhiệm kỹ thuật cho 1 Engine/module cụ thể (ví dụ: Structure Engine Owner). Tránh tình trạng cả platform chỉ có 1 người hiểu toàn bộ hệ thống. | Gán theo từng module khi Phase 3 bắt đầu, xem `/team/team.yaml` |
| **Software Engineer / QA Engineer / Research Engineer** | Roles thực thi — implementation, testing, research/spike. **Không có quyền tự ý thay đổi kiến trúc** (Module Taxonomy, Event Schema, dependency graph...) — bất kỳ thay đổi nào thuộc diện này đã là **ADR Required** theo [4b. ADR Scope Rule](#4b-adr-scope-rule--khi-nào-cần-adr), áp dụng cho MỌI contributor, không riêng Product Owner/Chief Architect. | xem `/team/team.yaml` |

**Nguyên tắc:** Constitution chỉ định nghĩa **Role**, không bao giờ ghi tên người/AI cụ thể. Việc gán Người/AI ↔ Role sống trong `/team/team.yaml` — tách biệt hoàn toàn khỏi Constitution, để mở rộng từ 1 người lên 10+ người mà không phải sửa Constitution mỗi lần có thành viên mới.

> Không đánh số (#1/#2) — nếu sau này có thêm AI Architect khác (Codex, Gemini...) tham gia, đánh số sẽ vô nghĩa. Tên cụ thể (ChatGPT/Claude) là định danh, không phải thứ tự ưu tiên.

## 2b. Conflict Resolution

Nếu Product Owner và Chief Architect là 2 người khác nhau (tương lai) và bất đồng: Product Owner thắng (business priority quyết định) — nhưng ADR phải ghi rõ phản đối của Chief Architect (cùng cơ chế minh bạch như Concern/Risk ở Mục 3). Đây là quy tắc **quyền lực**, tách khỏi bảng Roles (định nghĩa **trách nhiệm**) để tránh lẫn hai khái niệm khác nhau.

## 3. Decision Workflow

```
Requirement → ChatGPT Review → Claude Review → Architecture Review
   → Product Owner Decision → ADR Accepted → ADR Locked → Sang Phase tiếp theo
```

*(Accepted = trạng thái quyết định đã chốt; Locked = hành động đóng băng tài liệu — tách riêng để sau này dễ tự động hóa.)*

**Quy tắc:** ChatGPT Review và Claude Review là bước **bắt buộc phải xảy ra** trước khi Product Owner quyết — không skip — nhưng không bên AI nào có quyền chặn (veto) quyết định của Product Owner. Mỗi review output theo format:

```
Concern:        điều gì đáng lưu ý
Risk:           mức độ ảnh hưởng nếu bỏ qua (thấp/trung bình/cao)
Recommendation: nên làm gì
```

**Lưới an toàn duy nhất còn giữ lại:** nếu một Concern có Risk cao và liên quan trực tiếp đến việc vi phạm một [Platform Invariant](./02-platform-invariants.md) (I-1 đến I-11), và Product Owner vẫn quyết định tiến hành, ADR phải ghi rõ dòng "Chấp nhận rủi ro: ..." — không được bỏ qua trong im lặng. Đây không phải veto, chỉ là yêu cầu minh bạch.

## 4. ADR Workflow

Dùng template tại [`/docs/templates/adr-template.md`](../templates/adr-template.md). Mỗi ADR bắt buộc có trường **Scale check**: *"Nếu 2 năm nữa platform có 50 strategy, 10 exchange, 100 plugin, quyết định này có còn đúng không?"* — đây là câu hỏi bắt buộc điền, không phải một quy trình review riêng (không có "Challenge Round" như một nghi lễ tách biệt).

## 4b. ADR Scope Rule — khi nào cần ADR

Không phải mọi quyết định đều cần ADR — nếu có, việc ra quyết định sẽ quá nặng nề.

| Loại | Ví dụ | Có cần ADR? |
|---|---|---|
| **ADR Required** | Thêm/sửa Platform Invariant · thay đổi Event Schema · thay đổi Module Taxonomy hoặc dependency graph giữa Engine · thay đổi Governance/Approval process · quyết định ảnh hưởng > 1 module hoặc khó đảo ngược (chọn message broker, chọn ngôn ngữ cho 1 tầng) · bất kỳ thay đổi nào sửa/supersede một ADR đã Locked | **Bắt buộc** |
| **ADR Optional** | Thay đổi nội bộ trong 1 module không ảnh hưởng contract/schema công khai, nhưng ảnh hưởng đáng kể hiệu năng/maintainability (ví dụ: đổi thuật toán tính feature, giữ nguyên output schema) | Tùy người viết tự đánh giá mức độ quan trọng |
| **ADR Not Required** | Thay đổi thẩm mỹ/UI thuần túy (ví dụ: đổi màu button) · refactor nội bộ không đổi behavior/contract · sửa lỗi chính tả/formatting | **Không cần** |

**Nguyên tắc kiểm tra nhanh:** nếu quyết định này sai, có ảnh hưởng đến module khác hoặc khó sửa lại không? Nếu có → ADR Required.

## 5. Freeze Policy & ADR Immutable Rule

Tài liệu/ADR ở trạng thái **Approved** hoặc **Locked** không được sửa trực tiếp. Muốn sửa → phải mở ADR mới, version tăng.

**ADR Immutable Rule (quan trọng — phân biệt ADR với Document version thường):** một ADR là **Decision Record**, không phải một tài liệu được version-hóa tại chỗ.

```
Draft / In Review  → được sửa tại chỗ, được overwrite, KHÔNG đặt tên "rev2/rev3"
        ↓ (Product Owner approve)
   Approved → Locked
        ↓
   TUYỆT ĐỐI không sửa lại, không "rev2", không "rev3"
   Muốn thay đổi quyết định → tạo ADR MỚI (ví dụ ADR-004 → supersede bởi ADR-005),
   liên kết qua field supersedes/superseded_by — đây là cách ĐÚNG để nối lịch sử
   quyết định, khác với việc sửa nội dung một ADR đã Locked.
```

Trước khi Locked: sửa trực tiếp là hợp lệ (ADR-005 từng được sửa nhiều lần khi còn `In Review` — hợp lệ theo đúng luật này). Sau khi Locked: mọi thay đổi bắt buộc là một ADR mới, không bao giờ "rev" ADR cũ.

## 5b. Single Source of Truth — áp dụng cụ thể trong Governance

Định nghĩa đầy đủ nằm tại **I-12** ([02-platform-invariants.md](./02-platform-invariants.md)) — không lặp lại định nghĩa ở đây (đúng tinh thần của chính nguyên tắc này). Ví dụ áp dụng cụ thể trong tài liệu Governance:
- Decision Log sống trong `MANIFEST.md`, không có folder `/docs/decisions/` riêng trùng lặp.
- Glossary hợp nhất với Domain Model (xem [04-domain-principles.md](./04-domain-principles.md)).
- Version/status của toàn bộ tài liệu chỉ ghim tại `MANIFEST.md`.

**Decision ≠ Documentation (hệ quả trực tiếp của I-12):** mỗi loại tài liệu chỉ làm đúng 1 việc, không thay thế nhau — ADR lưu *quyết định*, Constitution lưu *quy tắc*, `/docs/architecture/` lưu *thiết kế*, `/docs/domain/` lưu *khái niệm nghiệp vụ*. Không viết quyết định vào Constitution, không viết quy tắc vào ADR.

## 6. Disagree and Commit

Sau khi một ADR đã Approved/Locked, không tranh luận lại — trừ khi có MỘT trong hai điều kiện:
1. Một sự cố/lỗi thật đã xảy ra, truy vết được trực tiếp về quyết định đó.
2. Một yêu cầu mới **mâu thuẫn cấu trúc** với quyết định cũ.

## 7. Document Lifecycle

```
Not Started → Draft → In Review → Revision Requested → Approved → Locked
                                                              ↓
                                                    Deprecated / Superseded
```

## 8. Versioning Policy

Mỗi tài liệu (Constitution chapter, ADR, Domain Contract) có `version` riêng (SemVer). Toàn bộ tổ hợp version+status hiện tại được ghim tại [`MANIFEST.md`](../MANIFEST.md) — không có Manifest, "phiên bản hiện tại của Constitution" là một khái niệm mơ hồ một khi đã tách nhiều file.

## 9. Review Policy

Mọi file có `owner`, `reviewers`, `approved_by`, `last_review`, `next_review` trong frontmatter. `next_review` không được để trống quá lâu với tài liệu Tier cao (Platform Invariants, ADR ảnh hưởng Risk/Execution) — mặc định review lại mỗi khi có Phase mới mở Approval Gate.
