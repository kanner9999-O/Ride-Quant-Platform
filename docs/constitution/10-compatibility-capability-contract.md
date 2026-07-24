---
id: 10-compatibility-capability-contract
title: Compatibility & Capability Contract
version: "2.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-24"
next_review: null
depends_on: ["02-platform-invariants", "03-engineering-principles", "04-domain-principles", "07-module-taxonomy", "08-event-model", "09-plugin-model"]
---

# 10. Compatibility & Capability Contract

**Version đúng không đảm bảo dữ liệu đủ.** Hai component có thể khớp version nhưng vẫn không dùng được cùng nhau vì bên cung cấp không còn (hoặc chưa) cung cấp capability mà bên tiêu thụ cần. Chapter 10 khóa **quy tắc đánh giá** compatibility/capability — không khóa tên capability cụ thể, không khóa schema, không khóa thuật toán triển khai.

## 10.1 Phạm vi và ranh giới thẩm quyền

**Chapter 10 sở hữu:** quy tắc so khớp compatibility/capability · thời điểm bắt buộc đánh giá · yêu cầu đối với kết quả đánh giá · hành vi khi không khớp · quy tắc đánh giá downstream impact · cấu trúc/semantic của Capability Matrix.

**Chapter 10 KHÔNG sở hữu** (chỉ tham chiếu — [I-12](./02-platform-invariants.md)):

| Sự thật | Authority |
|---|---|
| Business Capability identity/definition/status | `context-map.yaml` ([Chapter 4 §4.2](./04-domain-principles.md)) — mọi `capability_id` phải tồn tại sẵn ở registry, không tài liệu nào tự đặt tên mới |
| Module identity · taxonomy type · mapping | `module-registry.yaml` ([Chapter 7 §7.5](./07-module-taxonomy.md)) |
| Event Contract version · payload semantic · `schema_version` | Event Contract + [Chapter 8 §8.2.5](./08-event-model.md) |
| Plugin identity 4 tầng · Plugin Contract declaration groups · promotion/activation boundary | [Chapter 9](./09-plugin-model.md) |
| Authoritative implementation per capability · execution mode canonical | [Chapter 3 §3.1](./03-engineering-principles.md) |
| Tên capability cụ thể · schema/format khai báo | Domain Contract / registry tương ứng |

**Delegation Chapter 10 nhận từ các chapter Locked** (phải được đáp ứng ở đây, không được để trống):
- [Chapter 3](./03-engineering-principles.md) §Engineering Foundation — SemVer cho schema/capability;
- [Chapter 8 §8.6](./08-event-model.md) — schema versioning/compatibility;
- [Chapter 9 §9.5](./09-plugin-model.md) — `required capability/compatibility result` trong validated compatibility set;
- [Chapter 9 §9.7](./09-plugin-model.md) — SemVer, capability declaration, Capability Matrix, hành vi khi không khớp, **và** downstream impact rules.

**Chapter 10 KHÔNG tạo authority mới.** Thành phần thực hiện đánh giá phải là module đã đăng ký trong `module-registry.yaml` với taxonomy type hợp lệ (Chapter 7); Constitution **không đặt tên component** và không tự phong quyền chặn cho một component chưa đăng ký. Enforcement/verification vẫn đi qua đúng phân tầng đã khóa ở [Chapter 9 §9.6](./09-plugin-model.md) (Declaration · Grant · Enforcement · Verification).

## 10.2 Ba loại "capability" — KHÔNG được gộp

| Loại | Ý nghĩa | Authority của identity |
|---|---|---|
| **Business Capability** | Ranh giới trách nhiệm nghiệp vụ, có `capability_id` và capability version ([Chapter 3 §3.1](./03-engineering-principles.md)) | `context-map.yaml` (Chapter 4) |
| **Required platform capability** | Capability một plugin **đòi hỏi** từ platform để chạy được ([Chapter 9 §9.6](./09-plugin-model.md) — nhóm khai báo `Required capabilities`) | Plugin Contract khai báo; platform/registry định nghĩa tập hợp lệ |
| **Provided contract capability** | Hành vi/output mà một **published contract** cam kết cung cấp cho consumer ([Chapter 9 §9.2](./09-plugin-model.md)) | Published contract tương ứng |

Gộp ba loại vào một danh sách phẳng làm việc so khớp mất nghĩa: không xác định được đang khớp *nhu cầu với nền tảng*, *nhu cầu với contract của provider*, hay *implementation với business capability*. **Mọi capability reference phải resolve được về registry sở hữu nó**; reference tới capability chưa đăng ký là **invalid declaration**, không phải "capability mới".

## 10.3 Version compatibility

**SemVer áp cho Plugin Version** — tầng thứ hai trong 4 tầng identity của [Chapter 9 §9.1](./09-plugin-model.md), không phải Plugin Definition, không phải Package/Build Artifact, không phải Plugin Runtime. Nguyên tắc tương đương áp cho version của published contract và của module implementation ([Chapter 7](./07-module-taxonomy.md)) — Chapter 10 khóa *quy tắc*, không khóa danh sách component.

**Breaking change được xác định theo published contract surface**, không theo internal implementation: thay đổi làm consumer hợp lệ hiện tại không còn hợp lệ (bỏ/đổi nghĩa field, thu hẹp giá trị chấp nhận, bỏ capability đã cam kết, siết precondition, nới hậu điều kiện theo hướng consumer không kiểm được) **bắt buộc bump major**. Refactor không đổi contract surface **không** được bump major để "cho an toàn" — làm vậy phá khả năng đọc ý nghĩa của version.

**Ba trục version độc lập, cấm dùng trục này làm proxy cho trục kia:**

```
Event Contract version   (Chapter 8 §8.2.5 — sở hữu event_class, allowed_streams, merge_constraints, payload semantic)
schema_version           (Chapter 8 — payload schema, có thể giữ nguyên qua nhiều Event Contract version)
Plugin Version           (Chapter 9 §9.1 — semantic implementation release)
```

Chapter 10 định nghĩa quy tắc so khớp **trên từng trục**; không hợp nhất chúng thành một con số. Canonical field name theo Chapter 8 là `schema_version` — không dùng biến thể viết khác.

**Compatibility requirement** (ví dụ khoảng version chấp nhận được) phải được khai báo trong Plugin Contract ([Chapter 9 §9.6](./09-plugin-model.md)). **Cú pháp/format cụ thể của requirement thuộc registry/Domain Contract**, không hardcode trong Constitution.

## 10.4 Compatibility Result — artifact bất biến, không phải một lần kiểm tra thoáng qua

[Chapter 9 §9.5](./09-plugin-model.md) (Locked) yêu cầu `required capability/compatibility result` là thành phần của **validated compatibility set** tại activation boundary. Một kết quả kiểm tra chỉ tồn tại trong bộ nhớ lúc khởi động **không pin được**. Vì vậy compatibility result phải:

1. **Bất biến** sau khi tạo — không được tính lại rồi ghi đè;
2. Có **content identity** và **resolvable trong replay/audit horizon** platform cam kết — thỏa Referenced Authoritative Artifact rules ([Chapter 8 §8.1.1](./08-event-model.md)) khi bị event/cursor/compatibility set tham chiếu;
3. **Pin đủ input đã được đánh giá**, tối thiểu: Plugin Version · exact Package/Build Artifact content identity hoặc immutable release manifest + target/runtime discriminator ([Chapter 9 §9.1](./09-plugin-model.md)) · contract references liên quan · capability requirement set · version/capability của phía cung cấp;
4. Cho ra **kết luận nhị phân trong phạm vi đã đánh giá**: eligible hoặc không. **Không có trạng thái "một phần"** ngầm — nếu chỉ một tập con hợp lệ, phạm vi đó phải được khai báo tường minh trong chính result, không suy ra lúc dùng.

**Cấm suy lại compatibility từ trạng thái runtime hiện tại.** Đánh giá lại sinh ra một result **mới**; nó không sửa lịch sử và không hồi tố hợp thức hóa một activation đã xảy ra — cùng nguyên tắc "evidence sau khi chạy ≠ eligibility tại activation" mà [Chapter 9 §9.5](./09-plugin-model.md) đã khóa.

## 10.5 Khi nào bắt buộc đánh giá — startup là chưa đủ

Đánh giá compatibility/capability là **bắt buộc tại tối thiểu** các điểm sau:

| Điểm đánh giá | Lý do |
|---|---|
| Đăng ký/cài đặt một Plugin Version hoặc Package/Build Artifact mới | Bắt lỗi trước khi bất kỳ runtime nào dùng |
| **Activation boundary** của decision-relevance promotion | [Chapter 9 §9.5](./09-plugin-model.md) yêu cầu result nằm trong compatibility set được validate |
| Runtime deployment đổi artifact hoặc target platform — **kể cả rebuild cùng Plugin Version** | Chapter 9 khóa mixed-build activation là integrity violation; nếu không đánh giá lại thì vi phạm này không có điểm phát hiện |
| Provider đổi published contract/capability mà consumer đang pin | `Independent versioning ≠ zero downstream impact` (§10.7) |
| Startup của runtime | Chặn cấu hình sai trước khi phục vụ traffic |

**Startup check một mình là KHÔNG đủ** và không được coi là thỏa yêu cầu của Chapter 9: một plugin đã khởi động thành công vẫn có thể trở nên không tương thích khi contract, capability, artifact hoặc grant đổi sau đó.

## 10.6 Hành vi khi không khớp

- **Không khớp → không được cấp eligibility.** Trong decision-relevant path, không khớp nghĩa là **không được sinh authoritative Decision** ([Chapter 9 §9.5](./09-plugin-model.md)).
- **Áp fail-safe theo [I-6](./02-platform-invariants.md)** — phạm vi nhỏ nhất nhưng đủ (symbol · strategy · account · exchange · platform tùy mức ảnh hưởng). **Không** mặc định dừng toàn platform vì một plugin không critical không khớp; cũng **không** thu hẹp phạm vi tới mức để ảnh hưởng lan ra ngoài scope cần thiết.
- **CẤM degrade ngầm:** không tự bỏ bớt capability không khớp, không tự hạ version, không chạy tiếp với subset để "vẫn hoạt động". Chạy với tập capability khác tập đã đánh giá là **mixed-state activation**, xử lý như integrity violation.
- **Mọi từ chối phải để lại evidence resolvable** — compatibility result đã dùng để từ chối phải truy được, đủ để trả lời "vì sao lúc đó bị chặn" ([I-1](./02-platform-invariants.md)).
- **Không khớp không tự động là lỗi vận hành cần ADR.** Xử lý theo lifecycle/quality gate; chỉ thay đổi *architecture/contract* mới thuộc diện ADR Required ([Chapter 9 §9.10](./09-plugin-model.md)).

## 10.7 Downstream impact assessment

Nhận trực tiếp từ [Chapter 9 §9.7](./09-plugin-model.md): **`Independent versioning ≠ zero downstream impact`**. Khi một Plugin Version hoặc published contract đổi, impact assessment phải xét tối thiểu:

- published contract surface (event · query/read · command);
- output semantic (kể cả khi schema không đổi);
- capability set cung cấp và đòi hỏi;
- permission requirement ([Chapter 9 §9.6](./09-plugin-model.md));
- freshness/latency commitment mà consumer đang dựa vào;
- dependency graph — consumer nào đang pin cái gì.

**Assessment phải resolve được tập consumer đang pin phiên bản/contract bị ảnh hưởng.** Nếu không resolve được, kết quả là **incompatible** — **không** được mặc định "chắc là tương thích". Đây là mặc định an toàn theo [I-6](./02-platform-invariants.md), không phải một tùy chọn vận hành.

## 10.8 Capability Matrix

**Chapter 10 sở hữu cấu trúc và semantic:** Capability Matrix ghi nhận, với mỗi module/plugin, những execution mode nó hỗ trợ. **Danh sách execution mode canonical thuộc [Chapter 3 §3.1](./03-engineering-principles.md)** (Backtest · Replay · Paper Trading · Live) — Chapter 10 không tự định nghĩa danh sách khác, và không tự thêm chiều mới bằng prose.

**Chapter 10 KHÔNG sở hữu lifecycle gate.** Việc *khi nào* một strategy được phép chuyển sang Live là **OQ-002**, hiện vẫn `Open`, thuộc **Quality Gates / Strategy Lifecycle** — [Chapter 9 §9.10](./09-plugin-model.md) đã khóa rằng không chapter nào được đóng ngầm nó. Capability Matrix là **input** cho gate đó, không phải bản thân gate; khai báo "hỗ trợ Live" không đồng nghĩa "được phép lên Live".

## 10.9 Ngoài phạm vi Chapter 10 — defer Phase 1

Constitution khóa *yêu cầu*, không khóa *cơ chế*:
- thuật toán so khớp cụ thể · cú pháp version range · storage/format/schema của compatibility result;
- component nào chạy đánh giá, deployment coordinator, fencing/transaction tại activation boundary ([Chapter 9 §9.5](./09-plugin-model.md) cũng defer phần này);
- retention/archive protocol cụ thể cho compatibility result và artifact;
- tooling, CI gate, báo cáo.

Tên capability cụ thể và schema khai báo thuộc **Domain Contract / registry**, không thuộc Constitution.
