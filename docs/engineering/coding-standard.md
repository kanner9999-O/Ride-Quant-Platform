---
id: engineering-coding-standard
title: "Engineering Foundation — Coding Standard"
version: "0.1"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-11"
last_review: null
next_review: null
depends_on: ["../constitution/03-engineering-principles", "../adr/ADR-008", "monorepo"]
---

# Engineering Foundation — Coding Standard

**Vai trò của tài liệu này:** convention document THỨ HAI của Phase 1.5 — Engineering Foundation (Chapter 3 §3.2), phạm vi CHỈ category **Coding Standard** (Chapter 14 §14.2's Phase 1.5 scope list) — đúng `EF-TXN-002` (một category = một transaction bounded). KHÔNG Constitution chapter, KHÔNG ADR, KHÔNG redefine Module Taxonomy/dependency graph/ngôn ngữ allocation — `ADR-008` (Approved) VẪN LÀ authority DUY NHẤT cho Python/Go/Rust layer assignment, `docs/engineering/monorepo.md` (Approved v0.5) VẪN LÀ authority cho repository topology. Tài liệu này CHỈ quy định coding-quality convention CHUNG áp cho MỌI module — KHÔNG PHẢI Naming/Logging/Config/Error Handling/Testing/CI-CD (category riêng, CHƯA triển khai, xem §11).

## 1. Source formatting

```text
Mỗi ngôn ngữ triển khai (Python, Go — theo ADR-008) PHẢI có MỘT automated
  formatter bắt buộc, enforce được trong CI (khi CI/CD category triển
  khai) — style KHÔNG được quyết định thủ công/tùy ý per-PR.
Go: dùng `gofmt` (bundled trong Go toolchain chính thức — KHÔNG PHẢI
  3rd-party brand choice, KHÔNG cần quyết định riêng).
Python: formatter cụ thể (black/ruff format/...) CHƯA chọn — Python
  KHÔNG có formatter bundled chính thức (khác Go) — deferred tới
  transaction build module Python đầu tiên (Phase 3) hoặc một tooling-
  selection transaction riêng, đúng logic deferral đã dùng cho package-
  manager tại `monorepo.md` §5 (chọn brand khi chưa có code LÀ
  speculative).
```

## 2. Lint / static analysis

```text
Mỗi ngôn ngữ PHẢI có MỘT static-analysis step bắt buộc trước khi merge
  (khi CI/CD category triển khai) — phát hiện lỗi rõ ràng (unused
  import, unreachable code, type mismatch cơ bản) TRƯỚC runtime.
Go: dùng `go vet` (bundled). Linter mở rộng cụ thể (staticcheck/
  golangci-lint...) CHƯA chọn — deferred, cùng lý do formatter.
Python: linter/type-checker cụ thể CHƯA chọn — deferred tới first-
  module-build hoặc tooling-selection transaction riêng.
```

## 3. Language-version / support policy

```text
Mỗi ngôn ngữ PHẢI pin một MINIMUM supported version tường minh TRƯỚC KHI
  module đầu tiên của ngôn ngữ đó được build — version cụ thể (vd
  "Python >= 3.X", "Go >= 1.Y") KHÔNG pin tại tài liệu này: chưa có code
  nào cần chạy, pin trước LÀ speculative VÀ có nguy cơ stale tới lúc
  Phase 3 thực sự bắt đầu (đúng G-VERIFY-001/EF-VERIFY-001).
Quy tắc: version PHẢI verify trực tiếp (tài liệu chính thức ngôn ngữ đó)
  TẠI transaction build module đầu tiên của ngôn ngữ đó, ghi vào chính
  transaction đó — KHÔNG copy từ trí nhớ/convention chung.
```

## 4. Dependency hygiene

```text
Mọi dependency (package Python, module Go) PHẢI có lý do sử dụng rõ ràng
  (giải quyết nhu cầu cụ thể, KHÔNG add "phòng khi cần"). Version pin
  CHÍNH XÁC (KHÔNG dùng range mở/`latest` cho production dependency —
  cùng nguyên tắc G-ID-002 áp dụng tương tự cho dependency identity).
  Cơ chế lockfile cụ thể (requirements.txt/poetry.lock/go.sum...) do
  package-manager choice (§1/`monorepo.md` §5) quyết định — CHƯA chọn
  tại đây.
```

## 5. Import / package discipline

```text
KHÔNG circular import/circular package dependency trong CÙNG một
  module_id — vi phạm phải sửa bằng tái cấu trúc, KHÔNG bằng lazy-
  import/workaround che giấu cycle.
KHÔNG import trực tiếp giữa hai module_id khác nhau bỏ qua dependency
  graph đã khai báo tại `module-registry.yaml` — import PHẢI khớp
  `depends_on` đã đăng ký (Chapter 7, dependency-graph change LÀ ADR
  Required); import KHÔNG khai báo LÀ một architecture violation, KHÔNG
  PHẢI style issue thuần túy.
Wildcard import (`import *`, `. "package"`) KHÔNG dùng — mọi symbol
  import PHẢI explicit.
```

## 6. Generated code

```text
Code generated tự động (protobuf/gRPC stub, ORM model, OpenAPI client...)
  PHẢI đánh dấu tường minh (header comment/naming convention riêng) —
  KHÔNG edit tay trực tiếp file generated; thay đổi phải qua nguồn sinh
  ra nó. Coverage/lint threshold riêng cho generated code thuộc Testing
  category (deferred, §11).
```

## 7. Comments / docstring

```text
Comment giải thích TẠI SAO (why), KHÔNG giải thích CÁI GÌ (what) khi code
  đã tự rõ nghĩa qua naming — tránh comment lặp lại tên function/
  variable.
Public API (function/class expose ra module khác) PHẢI có docstring/doc
  comment mô tả contract (input/output/side effect/exception) —
  internal-only helper KHÔNG bắt buộc.
KHÔNG PHẢI Documentation Convention (Chapter 3 §3.2's mục riêng, = cấu
  trúc `/docs`) — mục này CHỈ code-level comment/docstring, tách biệt,
  KHÔNG định nghĩa lại.
```

## 8. Dead code / warnings

```text
KHÔNG commit code đã comment-out/unreachable "để sau" — xóa hẳn, lịch sử
  đã có trong git. Compiler/linter warning PHẢI resolve trước merge (khi
  CI/CD category triển khai) — KHÔNG suppress warning hàng loạt bằng
  global flag để "cho qua"; suppress CHỈ per-instance có lý do ghi kèm.
```

## 9. Deterministic / reproducible development

```text
Build/test PHẢI reproducible từ đúng commit + đúng dependency lock —
  KHÔNG phụ thuộc trạng thái máy local không ghi lại (biến môi trường
  ngầm, cache ẩn). Đúng tinh thần I-2 Decision Parity (Research/
  Production cùng hàm) — mục này CHỈ khẳng định lại nguyên tắc
  reproducibility ở tầng build/dev, KHÔNG redefine I-2 (thuộc
  Constitution).
```

## 10. Exceptions / deviations

```text
Một deviation khỏi Coding Standard ĐƯỢC PHÉP khi có lý do kỹ thuật cụ
  thể (vd generated code, vendor lib không sửa được) — PHẢI ghi lại tại
  chính điểm deviation (comment/commit message), KHÔNG âm thầm.
  Deviation LÀ ADR Optional/Not Required class (Chapter 3 §"Nguyên tắc
  bắt buộc") — KHÔNG cần ADR trừ khi deviation đó THỰC SỰ thuộc ADR
  Required (Chapter 0 §4b).
```

## 11. Boundary với category khác (Phase 1.5) — KHÔNG absorb

```text
Naming Convention (symbol/domain vocabulary):  deferred tới Naming
  category riêng — §5 trên CHỈ nói "import phải explicit," KHÔNG định
  nghĩa quy ước tên biến/hàm/class.
Logging (schema/level):                        deferred tới Logging
  category riêng.
Config (runtime configuration architecture):   deferred tới Config
  category riêng.
Error Handling (exception hierarchy/error
  contract):                                    deferred tới Error
  Handling category riêng — §10 trên CHỈ nói "ghi lại deviation," KHÔNG
  định nghĩa exception hierarchy.
Testing (framework/coverage/tier):              deferred tới Testing
  category riêng — §8 trên CHỈ nói "warning phải resolve," KHÔNG định
  nghĩa test structure.
CI/CD (pipeline/enforcement mechanism):         deferred tới CI/CD
  category riêng — mọi "PHẢI enforce trong CI" ở trên LÀ principle chờ
  CI/CD category thực sự implement enforcement, KHÔNG tự tạo pipeline
  tại đây.
```

## 12. ADR-scope check (`EF-ADR-001`/`G-ADR-004`)

```text
Quyết định tại tài liệu này: coding-quality convention CHUNG (format/
  lint/version-policy/dependency-hygiene/import-discipline/generated-
  code/comment/dead-code/determinism/exception-rule) — TẤT CẢ ở mức
  principle, KHÔNG pin brand/version cụ thể nào (trừ Go's bundled
  gofmt/go vet, KHÔNG PHẢI 3rd-party choice).
KHÔNG mục nào: thêm/sửa Platform Invariant, đổi Event Schema, đổi
  Module Taxonomy/dependency graph (§5's import discipline THỰC THI
  dependency graph ĐÃ có, KHÔNG tạo/đổi edge nào), thay đổi Governance/
  Approval process, hay tạo constraint kiến trúc platform-wide khó đảo
  ngược nào — mọi rule ở đây refactor-class, sửa được bất kỳ lúc nào
  qua version bump.
Kết luận (Chapter 0 §4b + Chapter 3 §"Nguyên tắc bắt buộc"): **ADR Not
  Required** — convention/tooling change, refactor-class. Lịch sử thay
  đổi ghi tại CHANGELOG.md.
```

## Change history

```text
v0.1  2026-08-11  Established — vai trò: `Phase 1.5 Coding Standard
      Foundation Executor`. Bounded EF-TXN-002 category transaction
      (Coding Standard only). Verify trực tiếp trước khi author: current
      HEAD, ADR-008 language allocation (Approved), monorepo.md v0.5
      (Approved), python//go/ chỉ chứa README marker (KHÔNG code), KHÔNG
      coding-standard/lint/format artifact nào tồn tại trước đây.
      Established 10 principle: source formatting (Go: gofmt bundled;
      Python: formatter brand deferred), lint/static-analysis (Go: go
      vet bundled; Python deferred), language-version policy (KHÔNG pin
      version cụ thể — verify tại first-module-build), dependency
      hygiene (exact pin, no range/latest), import/package discipline
      (no circular, PHẢI khớp module-registry.yaml depends_on, no
      wildcard import), generated-code treatment, comment/docstring
      expectation (tách biệt Documentation Convention), dead-code/
      warning handling, deterministic/reproducible dev expectation,
      exception/deviation rule. KHÔNG tool/version cụ thể nào pin
      ngoài Go's bundled gofmt/go vet (KHÔNG PHẢI 3rd-party brand
      choice) — mọi Python tooling brand + concrete version number
      deferred, đúng speculative-tooling avoidance đã dùng cho
      `monorepo.md`. KHÔNG absorb Naming/Logging/Config/Error Handling/
      Testing/CI-CD category (§11 tường minh defer). ADR-scope check
      (`EF-ADR-001`): ADR Not Required. KHÔNG chạm `monorepo.md`/
      `ADR-008`/`ADR-024`/`module-registry.yaml`/Constitution.
      `status: Draft` — not self-approved (`G-ORCH-002`).
```
