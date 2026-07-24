---
id: 11-adr-process
title: ADR Process
version: "2.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-24"
next_review: null
depends_on: ["00-governance", "02-platform-invariants"]
---

# 11. ADR Process

Chapter 11 khóa **quy trình và metadata contract** của ADR. Nó **không** định nghĩa lại Document Lifecycle, Freeze Policy hay ADR Scope Rule — những thứ đó thuộc [Chapter 0](./00-governance.md) và Chapter 11 chỉ tham chiếu ([I-12](./02-platform-invariants.md)).

## 11.1 Template và phạm vi

Template chuẩn tại [`/docs/templates/adr-template.md`](../templates/adr-template.md) — mỗi ADR là một file riêng trong `/docs/adr/`, gồm: Context, Decision, Alternatives considered, Concerns/Risks noted, **Scale check**, Consequences.

**Khi nào cần ADR:** xem [Chapter 0 §4b — ADR Scope Rule](./00-governance.md) — không phải mọi quyết định đều cần. Chapter 11 không định nghĩa lại tiêu chí này.

**Status của ADR dùng chung Document Lifecycle** tại [Chapter 0 §7](./00-governance.md) (`Not Started → Draft → In Review → Revision Requested → Approved → Locked`, rẽ nhánh `Deprecated`/`Superseded`) — không có "ADR Lifecycle" riêng.

## 11.2 ADR identity — cấp số, uniqueness, không tái sử dụng

M��t ADR number là **identity**, không phải số thứ tự thuận tiện. Vì mọi tài liệu Locked đều tham chiếu ADR bằng số, số bị trùng hoặc bị dùng lại sẽ phá khả năng resolve của toàn bộ tham chiếu lịch sử.

- **Đúng một authority cấp số ADR** cho toàn repo — designation của authority này thuộc governance, không phải quy ước ngầm giữa các contributor. Hai contributor soạn song song **không** được tự chọn số.
- **Uniqueness scope:** số ADR là duy nhất trên toàn `/docs/adr/`, vĩnh viễn.
- **Không tái sử dụng:** số của một ADR bị hủy/bỏ dở (không bao giờ đạt `Approved`) **KHÔNG** được cấp lại cho quyết định khác. Nếu cần ghi nhận việc hủy, dùng đúng lifecycle của Chapter 0 §7, không "trả số về kho".
- **Không đổi số:** một ADR đã rời `Draft` không được renumber. Sai số phải xử lý bằng ADR mới, không bằng đổi tên file.
- Path convention `/docs/adr/ADR-XXX.md` là quy ước tổ chức file; **authority của identity là số ADR**, không phải đường dẫn.

## 11.3 Immutability boundary — decision content vs lifecycle metadata

[Chapter 0 §5](./00-governance.md) khóa: ADR đã `Approved`/`Locked` **không được sửa**, muốn đổi quyết định thì tạo ADR mới và liên kết qua `supersedes`/`superseded_by`. Đồng thời [Chapter 0 §7](./00-governance.md) khóa lifecycle có nhánh `Approved`/`Locked → Deprecated`/`Superseded`. Hai điều này chỉ cùng đúng khi phân biệt rõ **cái gì bị đóng băng**:

| Nhóm field | Sau khi Approved/Locked | Lý do |
|---|---|---|
| **Decision content** — Context · Decision · Alternatives considered · Concerns/Risks · Scale check · Consequences | **Bất biến tuyệt đối.** Không sửa, không "rev2/rev3". Muốn đổi → ADR mới | Đây là bản ghi quyết định tại thời điểm đó; sửa nó là viết lại lịch sử |
| **Lifecycle/link metadata** — `status` · `superseded_by` · `deprecated_at` và tương đương | **Được phép chuyển trạng thái theo đúng lifecycle Chapter 0 §7**, và **chỉ** theo các transition mà lifecycle đó cho phép | Chính Chapter 0 §7 yêu cầu `status` đổi sau khi Locked (nhánh Deprecated/Superseded); nếu mọi field đều đóng băng thì nhánh này không thể tồn tại |
| **Approval metadata** — `approved_by` · `approved_at` | Bất biến sau khi set | Là bằng chứng ai quyết định và khi nào |

*Đây là **làm rõ trong phạm vi wording sẵn có** của Chapter 0 (§5 nói về nội dung quyết định, §7 yêu cầu status chuyển tiếp), KHÔNG phải định nghĩa lại Chapter 0 đã Locked. Nếu reviewer đánh giá đây là redefinition chứ không phải clarification, bắt buộc mở **ADR** sửa Chapter 0 — Chapter 11 không được tự làm.*

**Cập nhật lifecycle metadata không phải một "lần sửa ADR" độc lập:** nó chỉ hợp lệ khi là **một phần của transition atomic** ở §11.5, không bao giờ là một thay đổi rời rạc do ai đó tự ghi vào file.

## 11.4 Metadata contract

Dùng chung Document Lifecycle ở [Chapter 0 §7](./00-governance.md):

| Field | Semantic |
|---|---|
| `addresses: [OQ-xxx]` | ADR đang **xử lý** OQ đó — **KHÔNG** làm OQ chuyển `Resolved`. Dùng khi ADR còn `Draft`/`In Review` |
| `resolves: [OQ-xxx]` | ADR **đóng** OQ đó — **CHỈ có hiệu lực khi ADR đạt `Approved`/`Locked`**. ADR còn Draft không được dùng field này |
| `depends_on: [ADR-yyy]` | ADR-yyy phải đạt `Approved`/`Locked` **trước** khi ADR hiện tại được rời `Draft`/`In Review` |
| `supersedes: [ADR-yyy]` | ADR hiện tại **thay thế** quyết định của ADR-yyy. Chỉ có hiệu lực khi ADR hiện tại đạt `Approved`/`Locked` |
| `superseded_by: ADR-zzz` | Ghi trên ADR **bị thay thế**, trỏ tới ADR thay thế nó. Là **lifecycle metadata** (§11.3), chỉ được set trong transition atomic ở §11.5 |

**Quan hệ supersede phải hai chiều và nhất quán:** `ADR-B.supersedes` chứa `ADR-A` **khi và chỉ khi** `ADR-A.superseded_by = ADR-B` và `ADR-A.status = Superseded`. Một chiều mà thiếu chiều kia là **trạng thái không hợp lệ**, không phải "chưa cập nhật xong".

**Cấm phụ thuộc vòng:** `depends_on` giữa các ADR phải là đồ thị **acyclic**. Nếu A `depends_on` B và B `depends_on` A thì không ADR nào rời được `Draft`/`In Review` — đây là deadlock, phải xử lý bằng cách tách/gộp quyết định, không bằng ngoại lệ thủ công.

## 11.5 Transition phải ATOMIC

**Approve một ADR** — một documentation change duy nhất:

```
status:      Draft/In Review  →  Approved
addresses:   [OQ-x]           →  []
resolves:    []               →  [OQ-x]
approved_by / approved_at     →  set
MANIFEST OQ-x                 →  Resolved   (projection, §11.6)
```

Nếu approve trước rồi mới đổi `addresses` → `resolves` ở lần sửa sau, lần sửa đó **vi phạm ADR Immutable Rule**. Toàn bộ transition phải nằm trong cùng một thay đổi.

**Supersede một ADR đã Approved/Locked** — cũng là một thay đổi duy nhất, gồm cả hai file:

```
ADR mới:  status → Approved · supersedes: [ADR-cũ] · approved_by/approved_at set
ADR cũ:   status → Superseded · superseded_by: ADR-mới
MANIFEST: cập nhật status/version của cả hai
```

Không được approve ADR mới trước rồi mới quay lại đánh dấu ADR cũ ở commit sau — khoảng giữa hai bước đó là trạng thái mà hai ADR cùng có hiệu lực cho một quyết định.

**`Approved → Locked`:** Approved và Locked **cùng** chịu Freeze Policy ([Chapter 0 §5](./00-governance.md)) — cả hai đều không được sửa decision content. Locked là xác nhận ADR đã ổn định và được MANIFEST ghim; chuyển `Approved → Locked` là thay đổi **lifecycle metadata**, đồng bộ atomic với MANIFEST. Vì Approved đã bất biến, transition này **không** mở lại cơ hội chỉnh sửa nội dung.

**Deprecate** (quyết định không còn áp dụng nhưng **không** có ADR thay thế): `status → Deprecated`, lifecycle metadata cập nhật atomic với MANIFEST; decision content giữ nguyên. Khác `Superseded` ở chỗ không có `superseded_by`.

## 11.6 Authority của OQ status

**ADR là authority của việc một OQ đã được đóng hay chưa** — cụ thể là field `resolves` trên một ADR đạt `Approved`/`Locked` (§11.4). **MANIFEST là projection**, không phải nguồn sự thật song song ([I-12](./02-platform-invariants.md)).

- MANIFEST phải được cập nhật **atomic** trong cùng transition (§11.5), không bao giờ cập nhật rời.
- Khi MANIFEST và ADR lệch nhau → **ADR thắng**, và sai lệch đó là lỗi cần sửa MANIFEST, không phải hai nguồn "cùng hợp lệ".
- **Không tồn tại quan hệ "ADR HOẶC MANIFEST"** cho cùng một sự thật OQ status.

**OQ được `Resolved` bởi một ADR sau đó bị `Superseded`:** OQ **không tự động mở lại**. ADR thay thế phải khai báo tường minh nó xử lý OQ đó thế nào — tiếp tục đóng (`resolves`), hay mở lại (OQ trở về `Open`, ghi rõ trong ADR mới). **Im lặng không phải một lựa chọn**: nếu ADR thay thế không nói gì về OQ mà ADR cũ đã đóng, đó là **khai báo thiếu**, phải bổ sung trước khi approve.

## 11.7 Acceptance gate và validator

Ba field `addresses` · `resolves` · `depends_on` (cùng `supersedes`/`superseded_by`) là **machine-readable acceptance gate** — kiểm tra dựa vào status lifecycle chuẩn, **không** dựa vào chữ "accept" trong prose.

- **Validator không phải authority phê duyệt.** Nó kiểm tra tính nhất quán của metadata; quyền approve/reject vẫn **chỉ** thuộc Product Owner ([Chapter 0 §2](./00-governance.md)).
- **Kết quả validator là điều kiện chặn, không phải cảnh báo:** metadata không nhất quán (supersede một chiều · `resolves` trên ADR chưa Approved · `depends_on` trỏ ADR chưa Approved hoặc tạo vòng · MANIFEST lệch ADR) → ADR **không đủ điều kiện** chuyển sang `Approved`.
- **Ai vận hành validator và bằng công cụ gì thuộc Phase 1** — Constitution khóa *điều kiện phải thỏa*, không khóa cơ chế kiểm tra.

## 11.8 Quy tắc bắt buộc

- ADR phải được ghi khi: (a) có quyết định kiến trúc mới, (b) một phase sau muốn sửa quyết định của phase trước.
- **Không phase nào được coi là Approved nếu có quyết định kỹ thuật quan trọng chưa được ghi thành ADR.**
- **Không phase nào được tự ý sửa phase trước** mà không qua quy trình ở [Chapter 0](./00-governance.md).
- **Review từ các role đang giữ `AI Technical Architect` là input bắt buộc phải có trước khi Product Owner quyết** — bắt buộc *có*, không phải điều kiện *approve*; Product Owner vẫn là người quyết định cuối cùng. Việc gán Người/AI ↔ Role sống ở [`/team/team.yaml`](../team/team.yaml), **không** ghi tên cụ thể trong Constitution ([Chapter 0 §2](./00-governance.md)): số lượng và danh tính các AI Technical Architect có thể thay đổi mà không cần sửa chương này.

## 11.9 Ngoài phạm vi Chapter 11 — defer Phase 1

Tooling/CI cho validator · cơ chế cấp số ADR cụ thể · format lưu trữ và index của `/docs/adr/` · quy trình review nội bộ chi tiết. Tiêu chí *khi nào cần ADR* thuộc [Chapter 0 §4b](./00-governance.md); Freeze Policy và Document Lifecycle thuộc [Chapter 0 §5, §7](./00-governance.md).
