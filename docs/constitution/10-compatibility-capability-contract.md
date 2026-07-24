---
id: 10-compatibility-capability-contract
title: Compatibility & Capability Contract
version: "2.3"
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
| **Compatibility Policy identity · version · activation state** | **Đúng một canonical authority được designate cho mỗi loại fact/scope** (§10.4.3) — Constitution khóa cardinality và yêu cầu, không chọn technology và không tự làm registry |
| Tên capability cụ thể · schema/format khai báo | Registry/Contract được designate là authority cho **chính loại khai báo đó** — mỗi loại đúng một, không phải lựa chọn giữa nhiều nguồn |

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

### 10.3.1 Schema compatibility — semantic độc lập format

[Chapter 8 §8.6](./08-event-model.md) (Locked) delegate schema versioning/compatibility sang Chapter 10. Nếu không khóa semantic tối thiểu thì hai team cùng tuyên bố "SemVer nghiêm ngặt" vẫn có thể phân loại ngược nhau cho cùng một thay đổi (ví dụ thêm required field không default: bên gọi minor, bên gọi major).

**Hai chiều compatibility — phải nói rõ chiều nào được yêu cầu:**

```
Backward compatible : consumer CŨ vẫn đọc/validate đúng dữ liệu MỚI
Forward compatible  : consumer MỚI vẫn đọc/validate đúng dữ liệu CŨ
Breaking            : ít nhất một chiều mà contract YÊU CẦU không còn thỏa
```

Một thay đổi chỉ "breaking" hay không **so với chiều mà contract cam kết** — contract phải khai báo chiều nào bắt buộc; không khai báo thì không suy diễn mặc định.

**Hành vi bắt buộc khi thiếu declaration** (nếu chỉ nói "không suy diễn mặc định" thì mỗi team vẫn tự chọn một mặc định khác nhau): published contract nằm trong phạm vi compatibility evaluation mà **không khai báo chiều compatibility bắt buộc** là **invalid declaration** → **không được chứng nhận compatible** → `eligible = false` theo [I-6](./02-platform-invariants.md), và reason phải ghi *khai báo invalid* hoặc *không đủ policy*, **KHÔNG** ghi *đã chứng minh không tương thích* (§10.4.2).

Contract **được phép** tuyên bố không cam kết chiều nào — nhưng phải là **declaration tường minh** (ví dụ một giá trị mang nghĩa "không cam kết compatibility"), **không phải field bị thiếu**. Vắng mặt là mơ hồ; tuyên bố tường minh là một lựa chọn có thể audit.

**Nguyên tắc phân loại tối thiểu:**
- thêm element **optional** có semantic/default an toàn cho reader chưa biết nó → **có thể** non-breaking;
- thêm element **required** không có fallback → **breaking**;
- remove · rename · đổi type · đổi nullability · đổi default · **đổi ý nghĩa** của element đang tồn tại → **breaking**, trừ khi có migration contract chứng minh compatibility theo chiều được yêu cầu;
- mở rộng/thu hẹp enum → phải đánh giá **theo từng chiều reader/writer**, không có kết luận chung;
- element `deprecated` nhưng còn giữ → chưa breaking, nhưng việc **gỡ bỏ** nó là breaking và phải theo đúng chu kỳ đã cam kết.

**Hai điều cấm suy diễn:**
- **`schema_version` bump không tự chứng minh compatibility** — bump chỉ là dấu hiệu có thay đổi, không phải bằng chứng thay đổi đó an toàn;
- **major version bump không tự làm một thay đổi trở nên an toàn** — nó thông báo breaking, không miễn trừ nghĩa vụ đánh giá downstream impact (§10.7).

Quy tắc **theo từng format cụ thể** (JSON Schema, Avro, Protobuf...) thuộc Domain Contract/Phase 1 — Constitution chỉ khóa semantic trên.

## 10.4 Compatibility Result — artifact bất biến, không phải một lần kiểm tra thoáng qua

[Chapter 9 §9.5](./09-plugin-model.md) (Locked) yêu cầu `required capability/compatibility result` là thành phần của **validated compatibility set** tại activation boundary. Một kết quả kiểm tra chỉ tồn tại trong bộ nhớ lúc khởi động **không pin được**. Vì vậy compatibility result phải:

1. **Bất biến** sau khi tạo — không được tính lại rồi ghi đè;
2. Có **content identity** và **resolvable trong replay/audit horizon** platform cam kết — thỏa Referenced Authoritative Artifact rules ([Chapter 8 §8.1.1](./08-event-model.md)) khi bị event/cursor/compatibility set tham chiếu;
3. **Pin đủ subject đã được đánh giá**, tối thiểu: Plugin Version · exact Package/Build Artifact content identity hoặc immutable release manifest + target/runtime discriminator ([Chapter 9 §9.1](./09-plugin-model.md)) · contract references liên quan · capability requirement set · version/capability của phía cung cấp;
4. **Pin đủ evaluation provenance** — xem §10.4.1;
5. Cho ra **kết luận eligibility nhị phân trong phạm vi đã đánh giá**: eligible hoặc không. **Không có trạng thái "một phần"** ngầm — nếu chỉ một tập con hợp lệ, phạm vi đó phải được khai báo tường minh trong chính result, không suy ra lúc dùng. Kèm theo là **reason classification** (§10.4.2), vì "không eligible" gộp nhiều nguyên nhân khác hẳn nhau.

### 10.4.1 Evaluation provenance — pin cả *ai đánh giá* và *theo luật nào*

Pin subject là chưa đủ. Cùng một bộ input có thể cho hai kết luận trái ngược dưới hai rule-set khác nhau:

```
inputs giống hệt (Plugin Version · artifact hash · contract · requirement set)
  dưới compatibility rule-set v1 → eligible
  dưới compatibility rule-set v2 → ineligible
```

Một result chỉ ghi `inputs + eligible=true` không trả lời được: luật nào đã áp, ai đánh giá, người đánh giá có thẩm quyền không, result sinh trước hay sau một rule transition, và audit có tái kiểm chứng được kết luận không. Vì Chapter 9 dùng result này như thành phần **mở activation boundary**, một result thiếu provenance là **"vé eligible" tự chứng nhận**.

Đây cùng nguyên tắc với [Chapter 3 §3.1](./03-engineering-principles.md) (Locked): tuyên bố parity phải pin đủ implementation version + configuration + **policy version** + contract — không chỉ pin dữ liệu đầu vào.

**Compatibility Result phải pin bất biến, tối thiểu:**
- **subject scope** — phạm vi kết luận áp dụng;
- **input references** (§10.4 mục 3);
- **compatibility policy/rule-set version** đã áp dụng;
- **evaluator module identity** ([Chapter 7](./07-module-taxonomy.md) — module đã đăng ký);
- **evaluator implementation version + exact artifact** hoặc immutable manifest ([Chapter 9 §9.1](./09-plugin-model.md));
- **evaluation time/boundary**;
- **result** + **reason classification** (§10.4.2) + evidence references.

**Result không resolve được evaluator identity · evaluator implementation/artifact · compatibility policy/rule-set version · evaluation scope/boundary thì KHÔNG hợp lệ và KHÔNG được đưa vào validated compatibility set** ([Chapter 9 §9.5](./09-plugin-model.md)). Schema cụ thể thuộc registry/Domain Contract; **provenance semantic là bắt buộc**.

**Chống self-certification:** component đang được đánh giá **KHÔNG mặc định** có quyền tự cấp eligibility cho chính nó. Việc evaluator là module đã đăng ký trong `module-registry.yaml` **không** đồng nghĩa được cấp quyền phán quyết eligibility — registry membership là *identity*, không phải *grant*. Quyền đánh giá phải đi qua đúng phân tầng đã khóa ở [Chapter 9 §9.6](./09-plugin-model.md): **Declaration → Grant → Enforcement → Verification**, với `granted ⊆ declared`. Trường hợp self-evaluation chỉ hợp lệ khi authorization model cho phép **tường minh** và có **independent verification** tương ứng.

### 10.4.2 Reason classification — eligibility nhị phân, lý do thì không

Quyết định eligibility là nhị phân, nhưng **lý do phải phân biệt được** — nếu không, audit mất khả năng phân biệt hai tình huống hoàn toàn khác nhau:

```
"đã chứng minh có mismatch"          ≠  "không đủ evidence để chứng minh compatible"
```

**Bắt buộc phân loại tối thiểu:** *đã chứng minh tương thích* · *đã chứng minh không tương thích* · *không đủ evidence/không đánh giá được* · *khai báo invalid* · *reference không resolve được* · *policy mismatch*. Danh sách mã cụ thể thuộc registry/Domain Contract — Constitution khóa **semantic**, không khóa enum.

**Quy tắc:** không chứng minh được tương thích → `eligible = false` (fail-safe [I-6](./02-platform-invariants.md)); **nhưng KHÔNG được ghi thành "đã chứng minh không tương thích"**. Chặn đúng mà ghi sai lý do là mất explainability ([I-1](./02-platform-invariants.md)).

**Cấm suy lại compatibility từ trạng thái runtime hiện tại.** Đánh giá lại sinh ra một result **mới**; nó không sửa lịch sử và không hồi tố hợp thức hóa một activation đã xảy ra — cùng nguyên tắc "evidence sau khi chạy ≠ eligibility tại activation" mà [Chapter 9 §9.5](./09-plugin-model.md) đã khóa.

### 10.4.3 Compatibility Policy / rule-set — authority, identity, lifecycle

§10.4.1 bắt Compatibility Result pin `compatibility policy/rule-set version`. Nếu chính policy đó không có identity và authority thì provenance mới chỉ có **field**, chưa có **gốc**: hai result cùng ghi nhãn `compat-v2` vẫn có thể chạy hai bộ luật khác nhau, và một result hoàn toàn có thể tự khai một `policy_version` không tồn tại rồi trở thành vé activation.

**Compatibility Policy phải là versioned immutable authoritative artifact:**

1. **Stable logical identity** + **immutable version/content identity** cho từng version — pin bằng nhãn version tự do là **không hợp lệ**; result phải **exact-pin** artifact/content identity (cùng nguyên tắc Referenced Authoritative Artifact, [Chapter 8 §8.1.1](./08-event-model.md));
2. **Declared scope** — policy áp cho phạm vi nào (execution mode · account · plugin class · contract class...); result nằm ngoài scope của policy nó viện dẫn là **invalid**;
3. **Identity/definition/version authority — đúng MỘT canonical authority.** Constitution không hardcode tên file hay technology, nhưng architecture **phải designate chính xác một** authority sở hữu identity + version của policy. **KHÔNG được tồn tại "Policy Contract" và "registry" như hai peer source** cho cùng sự thật này — đó là cấu trúc `A hoặc B` mà [Chapter 9](./09-plugin-model.md) đã phải loại bỏ ở quan hệ Input Contract / decision-dependency contract. Chapter 10 là luật cấp cao, **không tự động trở thành runtime policy artifact**;
4. **Runtime applicability/activation — đúng MỘT canonical authority cho mỗi scope.** "Policy version nào đang active cho scope nào" là **runtime fact** ([I-12](./02-platform-invariants.md)), không suy từ tài liệu Constitution. Configuration **có thể** là desired-state input và event log **có thể** là recorded transition, nhưng **chỉ một nguồn là canonical current/historical truth** cho scope đó; nguồn còn lại **không được tự tạo competing activation fact**. Nếu hai nguồn cùng trả lời được câu hỏi này, evaluator sẽ chọn được nguồn thuận lợi và cùng một subject cho ra hai kết luận eligibility trái ngược;

   **Designation của cả hai authority trên phải được version hóa và governance phê duyệt.** Thiếu designation, hoặc tồn tại nhiều peer authority cho cùng một loại policy fact trong cùng scope → **policy reference invalid** → `eligible = false` ([I-6](./02-platform-invariants.md)), reason ghi *khai báo invalid*/*reference không resolve được* (§10.4.2). Mô hình cụ thể (ví dụ: registry giữ identity + immutable definition · authoritative event log giữ activation/retirement fact · configuration chỉ là desired input) thuộc **thiết kế Phase 1**; Chapter 10 chỉ khóa **cardinality**: mỗi loại policy fact, trong mỗi declared scope, đúng một canonical authority;
5. **Lifecycle transition authoritative** — tạo/approve/activate/retire một policy version phải để lại authoritative record; **cấm mutate nội dung dưới cùng một version identity**;
6. **Historical content** immutable và resolvable theo đúng horizon cam kết (§10.4.4);
7. **Evaluator chỉ được dùng policy version đã được grant cho scope đó** — nối tiếp rule chống self-certification ở §10.4.1: quyền dùng policy là **grant**, không suy từ việc evaluator biết tên policy.

**Phương án thay thế được chấp nhận:** nếu dự án không muốn tạo artifact policy riêng ở giai đoạn này, có thể exact-pin **version của Chapter 10 cùng tập format-specific rules** mà nó tham chiếu — nhưng vẫn phải có **một root path authoritative và machine-resolvable**, không phải một chuỗi tên tự do. Cơ chế/format cụ thể defer Phase 1 (§10.9).

### 10.4.4 Retention của Compatibility Result và Policy

Result và policy version đã dùng là **immutable**: không được sửa, ghi đè, hay hồi tố. Nhưng **immutable ≠ giữ online vô hạn** — hai việc khác nhau:

- phải **resolve được trong toàn bộ replay/audit horizon** mà platform cam kết ([Chapter 8 §8.1.1](./08-event-model.md));
- **sau horizon** phải tuân **explicit retention/archive policy** đã công bố;
- nếu đã archive, reference lịch sử vẫn phải có **cách xử lý đúng theo policy đã công bố** — không được trở thành dangling reference im lặng.

Constitution **không** cam kết infinite retention.

## 10.5 Khi nào bắt buộc đánh giá — startup là chưa đủ

Đánh giá compatibility/capability là **bắt buộc tại tối thiểu** các điểm sau:

| Điểm đánh giá | Lý do |
|---|---|
| Đăng ký/cài đặt một Plugin Version hoặc Package/Build Artifact mới | Bắt lỗi trước khi bất kỳ runtime nào dùng |
| **Activation boundary** của decision-relevance promotion | [Chapter 9 §9.5](./09-plugin-model.md) yêu cầu result nằm trong compatibility set được validate |
| Runtime deployment đổi artifact hoặc target platform — **kể cả rebuild cùng Plugin Version** | Chapter 9 khóa mixed-build activation là integrity violation; nếu không đánh giá lại thì vi phạm này không có điểm phát hiện |
| Consumer đổi **pinned reference** của mình | Binding mới = subject mới, phải có result mới |
| **Active binding resolve sang** version/contract/capability/artifact khác | Thứ đang thực sự được dùng đã đổi, không phải chỉ có thứ mới tồn tại |
| Artifact/contract đã pin bị **explicit revoke** hoặc mất resolvability theo policy có thẩm quyền | Subject đã pin không còn hợp lệ/không còn resolve được |
| **Permission/capability grant** liên quan thay đổi ([Chapter 9 §9.6](./09-plugin-model.md)) | `granted ⊆ declared` có thể không còn thỏa |
| **Compatibility policy/rule-set** áp cho activation mới thay đổi | Kết luận phụ thuộc rule-set (§10.4.1) |
| Startup của runtime | Chặn cấu hình sai trước khi phục vụ traffic |

**Startup check một mình là KHÔNG đủ** và không được coi là thỏa yêu cầu của Chapter 9: một plugin đã khởi động thành công vẫn có thể trở nên không tương thích khi binding, capability, artifact hoặc grant đổi sau đó.

**Việc provider publish một version mới KHÔNG phải trigger.** Nếu consumer vẫn pin một immutable reference cũ thì binding của nó không đổi, và sự tồn tại của version mới không làm activation cũ trở nên stale:

```
Consumer pin Contract v2 · Provider publish Contract v3
→ binding vẫn là v2 → KHÔNG revalidate activation cũ
```

Suy diễn ngược lại ("có version mới → activation lịch sử phải xét lại") phá immutable reference, phá independent versioning ([Chapter 9 §9.7](./09-plugin-model.md)), và sửa hồi tố eligibility của một boundary đã đóng. **Historical Compatibility Result là immutable** — không sửa, không ghi đè, không hồi tố; resolvability theo đúng horizon cam kết ở **§10.4.4** (immutable ≠ giữ online vô hạn). Mọi đánh giá mới sinh **result mới cho boundary mới**, không ghi đè và không hồi tố hợp thức hóa hay vô hiệu hóa quá khứ.

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

**Assessment phải resolve được tập consumer đang pin phiên bản/contract bị ảnh hưởng.** Nếu không resolve được, **eligibility = false** — **không** được mặc định "chắc là tương thích". Đây là mặc định an toàn theo [I-6](./02-platform-invariants.md), không phải một tùy chọn vận hành.

**Nhưng phải ghi đúng lý do:** không resolve được tập consumer là *không đủ evidence*, **không phải** *đã chứng minh không tương thích* — phân loại theo §10.4.2. Chặn thì giống nhau, nhưng ghi sai lý do làm audit về sau không phân biệt được "contract này thực sự vỡ" với "lúc đó ta không biết ai đang dùng".

## 10.8 Capability Matrix

**Chapter 10 sở hữu cấu trúc và semantic:** Capability Matrix ghi nhận những execution mode mà một subject hỗ trợ. **Danh sách execution mode canonical thuộc [Chapter 3 §3.1](./03-engineering-principles.md)** (Backtest · Replay · Paper Trading · Live) — Chapter 10 không tự định nghĩa danh sách khác, và không tự thêm chiều mới bằng prose.

**Mỗi entry phải pin subject identity đủ cụ thể**, vì capability thay đổi theo tầng identity ([Chapter 9 §9.1](./09-plugin-model.md)) chứ không cố định theo logical plugin:
- module/Plugin Definition;
- **implementation/Plugin Version** — `v2.0` và `v3.0` của cùng Definition có thể hỗ trợ khác nhau;
- **artifact/target discriminator** khi capability phụ thuộc build/platform;
- **configuration/profile** khi capability phụ thuộc config — phải pin **configuration/profile identity + immutable configuration version hoặc content identity**, không chỉ tên profile: một nhãn như `live-default` là **mutable reference**, hôm nay bật Live tuần sau có thể đã đổi, và entry sẽ không còn resolve đúng snapshot config đã được đánh giá.

**CẤM suy capability của mọi version/artifact chỉ từ logical Plugin Definition** — đó là declaration quá rộng, và sẽ mâu thuẫn với chính yêu cầu exact-artifact eligibility mà [Chapter 9 §9.5](./09-plugin-model.md) đã khóa.

### 10.8.1 Declared support ≠ Validated capability

Rule chống self-certification ở §10.4.1 áp cho Compatibility Result **cũng phải áp cho Capability Matrix**. Nếu không, một plugin tự khai `Live = YES` sẽ đi thẳng vào input của lifecycle gate mà chưa có evaluator, policy, evidence hay approval nào.

| Lớp | Ý nghĩa | Hệ quả |
|---|---|---|
| **Declared support** | Component **tuyên bố** nó được thiết kế để hỗ trợ mode nào | **KHÔNG tự tạo eligibility**; là input để đánh giá, không phải kết luận |
| **Validated capability / readiness** | Đã được đánh giá bằng policy/evidence nào, đủ điều kiện làm input cho gate | Chỉ lớp này mới được dùng làm căn cứ readiness |

**Hai lớp này không được gộp** trong cùng một ô "supports: yes".

**Mỗi validated entry phải pin tối thiểu:** subject identity/version/artifact/config (§10.8) · evaluation policy/result hoặc evidence reference · evaluator/verification authority ([Chapter 9 §9.6](./09-plugin-model.md) — quyền đánh giá là **grant**, không phải tự nhận) · validation boundary/time · **immutable matrix version hoặc source frontier**.

### 10.8.2 Authority và versioning của Capability Matrix

Capability Matrix phải là **versioned, resolvable artifact** — hoặc **projection của một authoritative source đã được designate**, theo đúng cardinality "một canonical authority cho mỗi loại fact" ở §10.4.3. Nếu là projection, kết quả phải chỉ ra source frontier/version như mọi projection dùng cho quyết định ([Chapter 7 §7.4](./07-module-taxonomy.md)).

- **Cập nhật Matrix KHÔNG được ghi đè lịch sử** — tạo version mới, giữ nguyên version cũ (cùng nguyên tắc immutability + horizon ở §10.4.4);
- **Gate phải pin đúng Matrix snapshot** (hoặc authoritative evidence set) **đã dùng tại thời điểm đánh giá** — không đọc "matrix hiện tại", vì như vậy kết luận của gate sẽ đổi hồi tố theo trạng thái sau này;
- Matrix reference không resolve được về một version/frontier cụ thể → không dùng được làm input cho gate → xử lý theo §10.4.2 (*reference không resolve được*), không phải bỏ qua.

**Chapter 10 KHÔNG sở hữu lifecycle gate.** Việc *khi nào* một strategy được phép chuyển sang Live là **OQ-002**, hiện vẫn `Open`, thuộc **Quality Gates / Strategy Lifecycle** — [Chapter 9 §9.10](./09-plugin-model.md) đã khóa rằng không chapter nào được đóng ngầm nó. Capability Matrix là **input** cho gate đó, không phải bản thân gate; khai báo "hỗ trợ Live" không đồng nghĩa "được phép lên Live". Các rule ở §10.8.1/§10.8.2 **không** giải quyết OQ-002 — chúng chỉ bảo đảm thứ đưa sang gate đó không phải một bảng mutable tự khai.

## 10.9 Ngoài phạm vi Chapter 10 — defer Phase 1

Constitution khóa *yêu cầu*, không khóa *cơ chế*:
- thuật toán so khớp cụ thể · cú pháp version range · storage/format/schema của compatibility result;
- component nào chạy đánh giá, deployment coordinator, fencing/transaction tại activation boundary ([Chapter 9 §9.5](./09-plugin-model.md) cũng defer phần này);
- retention/archive protocol cụ thể cho compatibility result và artifact;
- tooling, CI gate, báo cáo.

Tên capability cụ thể và schema khai báo thuộc **registry/Contract được designate cho từng loại khai báo** (§10.1), không thuộc Constitution.
