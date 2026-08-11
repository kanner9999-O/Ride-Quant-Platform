---
id: engineering-naming
title: "Engineering Foundation — Naming Convention"
version: "0.1"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-11"
last_review: null
next_review: null
depends_on: ["../constitution/03-engineering-principles", "../adr/ADR-008", "../adr/ADR-026", "coding-standard", "monorepo"]
---

# Engineering Foundation — Naming Convention

**Vai trò của tài liệu này:** convention document THỨ BA của Phase 1.5 — Engineering Foundation (Chapter 3 §3.2), phạm vi CHỈ category **Naming Convention** (Chapter 14 §14.2's Phase 1.5 scope list) — đúng `EF-TXN-002` (một category = một transaction bounded). **`ADR-026` v0.1 (Approved 2026-08-11) LÀ authority cho chính việc CÓ một cross-module Naming Convention baseline bắt buộc** — tài liệu này LÀ living convention chứa chi tiết rule dưới authority đó, KHÔNG lặp lại decision text của ADR-026. KHÔNG Constitution chapter, KHÔNG ADR, KHÔNG redefine Module Taxonomy/dependency graph/ngôn ngữ allocation/Coding Standard — `module-registry.yaml` VẪN authority module identity/dependency, `ADR-008` VẪN authority ngôn ngữ, `ADR-024` VẪN authority repository topology, `ADR-025`/`coding-standard.md` VẪN authority Coding Standard. Mọi thay đổi SEMANTIC tương lai vào tài liệu này PHẢI tự chạy lại ADR Scope Rule (Chapter 0 §4b) hiện hành TẠI chính thời điểm đổi — reversibility của kỹ thuật thay đổi KHÔNG hủy/miễn vế ">1 module" nếu vế đó đã thỏa (đúng lesson `ADR-025`/`coding-standard.md` §12/§3, KHÔNG redefine).

## 1. General naming principles

```text
Identifier PHẢI thể hiện RÕ domain/capability meaning — KHÔNG tên viết
  tắt mơ hồ, KHÔNG synonym không cần thiết cho CÙNG một concept đã có
  tên (một concept ĐÃ established → dùng ĐÚNG root term đó xuyên module,
  KHÔNG đặt tên khác cho cùng nghĩa).
KHÔNG encode type information dư thừa vào tên biến thông thường (vd
  KHÔNG `orderList` khi type hệ thống đã rõ; type hint/annotation LÀM
  việc đó, KHÔNG PHẢI tên biến).
Implementation naming KHÔNG được redefine domain/contract terminology
  đã canonical (Domain Contract tại `/docs/domain/`, Event Contract,
  API contract VẪN authority DUY NHẤT cho Ý NGHĨA — naming ở đây CHỈ
  quyết định REPRESENTATION/style của identifier).
Tài liệu này KHÔNG invent domain vocabulary mới CHỈ để minh họa — ví dụ
  dưới đây (nếu có) LÀ minh họa naming PATTERN, KHÔNG PHẢI canonical
  domain concept/event/DTO/interface mới.
```

## 2. Python naming

```text
Module/file:              snake_case
Function/method:          snake_case
Variable:                 snake_case
Class/type:                PascalCase
Constant:                  UPPER_SNAKE_CASE
Private/internal:          leading `_` khi phù hợp (convention, KHÔNG
                          enforce cứng bởi ngôn ngữ)
Đây LÀ idiomatic Python tiêu chuẩn (PEP 8) — KHÔNG chọn formatter/
  linter tool cụ thể tại đây (deferred, `coding-standard.md` §1/§2).
```

## 3. Go naming

```text
Package name:               ngắn, lowercase, KHÔNG snake_case/camelCase
Exported identifier:        PascalCase
Unexported identifier:      camelCase
Constant:                    theo idiomatic Go convention (PascalCase
                            nếu exported, camelCase nếu KHÔNG) — KHÔNG
                            ép buộc UPPER_SNAKE_CASE kiểu Python.
KHÔNG ép visual uniformity xuyên ngôn ngữ — Python và Go giữ đúng idiom
  riêng của chính ngôn ngữ đó (đúng ADR-008's "idiom riêng ĐƯỢC PHÉP
  khác, PHẢI nhất quán baseline" — nhất quán ở tầng PATTERN chung, vd
  event representation §7, KHÔNG ở tầng casing chi tiết).
```

## 4. File / package naming

```text
Tên file/package PHẢI phản ánh nội dung chính bên trong — KHÔNG tên
  generic (`utils.py`, `helper.go`) trừ khi thực sự chứa utility chung
  không thuộc một concept cụ thể nào.
File/package naming PHẢI nhất quán casing đúng ngôn ngữ (§2/§3) — KHÔNG
  trộn casing trong CÙNG một ngôn ngữ.
```

## 5. Acronym / initialism handling

```text
Xử lý acronym theo idiom ngôn ngữ, KHÔNG ép một quy tắc chung cho cả
  hai — minh họa (pattern, KHÔNG canonical vocabulary):
  Go:      HTTPClient, APIClient, OrderID (acronym giữ nguyên case theo
           idiomatic Go — Effective Go convention).
  Python:  http_client, api_client, order_id (snake_case tự nhiên hóa
           acronym, đúng PEP 8).
```

## 6. Canonical `module_id` references

```text
`module-registry.yaml` VẪN LÀ authority DUY NHẤT cho canonical module
  identity/`module_id` — tài liệu này KHÔNG tạo authority `module_id`
  thứ hai, KHÔNG rename module_id nào. Khi tham chiếu module trong code/
  tài liệu, PHẢI giữ ĐÚNG spelling `module_id` đã đăng ký (kebab-case,
  vd `feature-engine`, `risk-gateway`, `market-data-ingestion` — verify
  trực tiếp `module-registry.yaml`, chỉ trích dẫn LÀM ví dụ đã tồn tại,
  KHÔNG tạo mới). Source directory naming (`python/<module_id>/` hoặc
  `go/<module_id>/`) đã pin tại `monorepo.md` §3 — KHÔNG redefine ở đây.
```

## 7. Event-name representation

```text
Quy ước: identifier đại diện cho một event dùng `PAST_TENSE_UPPER_SNAKE`
  (vd hình thức `ORDER_FILLED`, `POSITION_CLOSED`). **Rule này được
  ESTABLISH TẠI CHÍNH tài liệu này, dưới authority ADR-026 — KHÔNG PHẢI
  một Chapter 3 mandate có sẵn.** Chapter 3 §3.2's ví dụ minh họa CHỈ LÀ
  minh họa (tự Chapter 3 khai báo "không phải canonical domain vocabulary
  bắt buộc") — tài liệu này CHỌN adopt pattern đó làm representation
  convention, KHÔNG suy diễn nó đã sẵn canonical trước khi tài liệu này
  tồn tại.
Phân biệt bắt buộc: **event naming representation/style ≠ event
  existence/schema/semantic authority.** Việc một identifier VIẾT như
  thế nào KHÔNG quyết định event đó CÓ tồn tại hay Ý NGHĨA của nó — Event
  Contract/Domain Contract (`/docs/domain/`) VẪN authority DUY NHẤT cho
  event existence/schema. Tài liệu này KHÔNG invent canonical event
  inventory nào — `ORDER_FILLED`/`POSITION_CLOSED` (nếu xuất hiện) CHỈ
  LÀ ví dụ pattern kế thừa từ Chapter 3, KHÔNG tuyên bố các event đó
  chính thức tồn tại trong Domain Contract.
```

## 8. Interface / type naming

```text
Tài liệu này KHÔNG tự động mandate `I`-prefix (Chapter 3 §3.2's ví dụ
  `IStructureEngine`) — `I`-prefix KHÔNG idiomatic Go (Go convention
  thường đặt tên interface theo BEHAVIOR, vd hậu tố `-er` cho interface
  một method, hoặc noun mô tả trực tiếp, KHÔNG prefix `I`) VÀ KHÔNG
  idiomatic Python (`typing.Protocol`/ABC KHÔNG có convention prefix
  `I` trong ecosystem Python).
Quy tắc CHỌN tại đây (bounded, reversible — living convention, KHÔNG
  ADR text): interface/type đặt tên theo danh từ mô tả trực tiếp
  responsibility của nó, PHÙ HỢP idiom từng ngôn ngữ (§2/§3) — KHÔNG
  prefix/suffix nhân tạo áp đặt xuyên ngôn ngữ. Lý do: nhất quán idiom
  ngôn ngữ giúp code đọc tự nhiên hơn cho dev quen ngôn ngữ đó, ĐÚNG
  tinh thần ADR-026 §3 "idiom riêng ĐƯỢC PHÉP khác, PHẢI nhất quán
  baseline chung" (baseline chung ở đây LÀ "đặt tên theo responsibility
  rõ ràng," KHÔNG PHẢI một prefix cụ thể).
KHÔNG invent interface inventory nào tại đây — quyết định CHỌN tên cho
  một interface CỤ THỂ thuộc phạm vi implementation transaction của
  chính module đó (Phase 3+), KHÔNG tại convention document này.
```

## 9. DTO / data-structure naming

```text
Tài liệu này KHÔNG tự động mandate suffix `DTO` cho MỌI data structure
  (khác Chapter 3 §3.2's ví dụ minh họa `SwingDTO`/`DecisionDTO` áp
  dụng rộng). Suffix `DTO` CHỈ dùng khi type đó THỰC SỰ đại diện một
  transfer boundary (dữ liệu đi qua boundary serialization/API/event/
  cross-module reference) VÀ phân biệt đó thực sự hữu ích (tách bạch
  khỏi domain entity/value object nội bộ). Data structure nội bộ KHÔNG
  qua transfer boundary KHÔNG cần suffix `DTO`.
KHÔNG invent DTO inventory nào tại đây — quyết định type nào LÀ DTO
  thuộc phạm vi implementation transaction của chính module đó.
```

## 10. Boolean / predicate naming

```text
Ưu tiên predicate dạng khẳng định, dễ đọc — minh họa pattern:
  Python:  is_active, has_position, can_execute
  Go:      isActive, hasPosition, canExecute
Tránh double negative (vd KHÔNG `is_not_disabled` — dùng `is_enabled`).
```

## 11. Constants / enums

```text
Constant: theo §2/§3 (Python `UPPER_SNAKE_CASE`, Go idiomatic
  PascalCase/camelCase theo export scope).
Enum member: PHẢI mô tả giá trị domain rõ ràng, KHÔNG viết tắt mơ hồ —
  tên member LÀ representation, Ý NGHĨA của giá trị đó (nếu thuộc
  domain concept) VẪN do Domain Contract quyết định (§1's nguyên tắc
  chung).
```

## 12. Deviations / exceptions

```text
Một deviation khỏi Naming Convention ĐƯỢC PHÉP khi có lý do kỹ thuật cụ
  thể (vd tuân theo API/SDK bên ngoài không kiểm soát được, generated
  code — xem `coding-standard.md` §6) — PHẢI ghi lại tại chính điểm
  deviation (comment/commit message), KHÔNG âm thầm. Deviation LÀ ADR
  Optional/Not Required class (Chapter 3 §"Nguyên tắc bắt buộc") — KHÔNG
  cần ADR trừ khi deviation đó THỰC SỰ thuộc ADR Required (Chapter 0
  §4b).
```

## 13. Boundary với Coding Standard và category khác (Phase 1.5) — KHÔNG absorb

```text
Coding Standard (formatting/lint/dependency-hygiene/reproducibility
  policy):                  VẪN thuộc `coding-standard.md` — tài liệu
  này CHỈ quyết định TÊN identifier, KHÔNG style tool/dependency/
  reproducibility nào.
Logging (schema/level):      deferred tới Logging category riêng.
Config (runtime configuration architecture): deferred tới Config
  category riêng.
Error Handling (exception hierarchy/error contract): deferred tới Error
  Handling category riêng — §12 trên CHỈ nói "ghi lại deviation," KHÔNG
  định nghĩa exception hierarchy.
Testing (framework/coverage/tier): deferred tới Testing category riêng.
CI/CD (pipeline/enforcement mechanism): deferred tới CI/CD category
  riêng — "PHẢI" ở các mục trên LÀ principle chờ CI/CD category thực sự
  implement enforcement, KHÔNG tự tạo pipeline tại đây.
Documentation Convention (Chapter 3 §3.2's mục riêng, = cấu trúc
  `/docs`): KHÔNG redefine — tách biệt hoàn toàn khỏi code-identifier
  naming tại đây.
```

## 14. ADR-scope disposition

```text
Quyết định "CÓ một Naming Convention baseline chung bắt buộc cho MỌI
  module" LÀ platform-wide, thỏa vế ">1 module" của Chapter 0 §4b — ĐÃ
  ADR Required (KHÔNG PHẢI ADR Not Required — reversibility của chi
  tiết rule bên trong tài liệu này KHÔNG hủy/miễn vế đó).
`ADR-026` v0.1 (Approved 2026-08-11, "APPROVE ADR-026 V0.1") LÀ ADR đó
  — satisfy chính xác quyết định baseline-existence này. Tài liệu này
  (`naming.md`) LÀ living convention ALIGNED dưới `ADR-026` — chứa chi
  tiết rule reversible (§1–§13 trên), KHÔNG lặp lại decision text của
  ADR-026.
Mọi thay đổi SEMANTIC tương lai vào tài liệu này (KHÔNG PHẢI mọi sửa —
  CHỈ khi đổi Ý NGHĨA rule) PHẢI tự chạy lại ADR Scope Rule hiện hành
  TẠI chính thời điểm đổi — KHÔNG suy diễn "reversible/refactor-class"
  LÀ đủ để miễn ADR (đúng `ADR-026` §3/`ADR-025` §3, KHÔNG redefine).
  Naming KHÔNG generally "ADR Not Required" — baseline-existence đã
  resolved bởi ADR-026, NHƯNG một semantic baseline change MỚI (áp dụng
  cho MỌI module) vẫn CÓ THỂ tự thỏa lại vế ">1 module."
Residual `ADR026-A-MIN-01` (Alternative 3 của ADR-026 hơi overstate
  Chapter 3 §3.2's ví dụ) VẪN `OPEN — accepted non-blocking` — tài liệu
  này KHÔNG lặp lại overstatement đó (§7/§8/§9 trên đều tách bạch tường
  minh "minh họa" khỏi "canonical"), KHÔNG tự đóng finding đó (thuộc
  phạm vi correction riêng cho `ADR-026.md`, KHÔNG tại đây).
```

## Change history

```text
v0.1  2026-08-11  Established — vai trò: `Phase 1.5 Naming Foundation
      Executor`. Bounded EF-TXN-002 category transaction (Naming only).
      Verify trực tiếp trước khi author: current HEAD, ADR-026 v0.1
      Approved identity (blob `7f1980db...`), `docs/engineering/
      naming.md` KHÔNG tồn tại trước đây. Established 14 mục: general
      principles, Python naming (idiomatic PEP 8), Go naming (idiomatic,
      KHÔNG ép uniformity với Python), file/package naming, acronym
      handling, canonical `module_id` reference (module-registry.yaml
      authority, KHÔNG tạo authority thứ hai), event-name representation
      (`PAST_TENSE_UPPER_SNAKE` — rule ESTABLISH tại đây dưới ADR-026,
      KHÔNG PHẢI Chapter 3 mandate có sẵn; representation ≠ existence/
      schema authority), interface/type naming (KHÔNG mandate `I`-prefix
      — chọn responsibility-based naming idiomatic mỗi ngôn ngữ),
      DTO/data-structure naming (KHÔNG mandate suffix `DTO` toàn bộ —
      CHỈ khi thực sự transfer boundary), boolean/predicate naming,
      constants/enums, deviations/exceptions, boundary với Coding
      Standard/category khác (KHÔNG absorb), ADR-scope disposition
      (baseline-existence ĐÃ ADR Required, `ADR-026` satisfy, semantic
      update tương lai vẫn PHẢI tự rerun ADR Scope Rule — KHÔNG tuyên bố
      Naming generally ADR Not Required). KHÔNG invent canonical event/
      domain/API vocabulary hay inventory nào (event/interface/DTO ví dụ
      đều đánh dấu "minh họa pattern," KHÔNG canonical). KHÔNG tạo
      module→language mapping nào. KHÔNG chọn formatter/linter/package-
      manager nào. `ADR026-A-MIN-01` VẪN `OPEN — accepted non-blocking`,
      KHÔNG đóng tại đây. KHÔNG chạm `ADR-026`(Approved, immutable)/
      `ADR-025`/`coding-standard.md`/`ADR-008`/`ADR-024`/
      `module-registry.yaml`/Constitution/Phase 1.5 rules. KHÔNG bắt
      đầu Logging/Config/Error Handling/Testing/CI-CD. `status: Draft`
      — not self-approved (`G-ORCH-002`).
```
