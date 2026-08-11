---
id: engineering-coding-standard
title: "Engineering Foundation — Coding Standard"
version: "0.2"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-11"
last_review: null
next_review: null
depends_on: ["../constitution/03-engineering-principles", "../adr/ADR-008", "../adr/ADR-025", "monorepo"]
---

# Engineering Foundation — Coding Standard

**Vai trò của tài liệu này:** convention document THỨ HAI của Phase 1.5 — Engineering Foundation (Chapter 3 §3.2), phạm vi CHỈ category **Coding Standard** (Chapter 14 §14.2's Phase 1.5 scope list) — đúng `EF-TXN-002` (một category = một transaction bounded). KHÔNG Constitution chapter, KHÔNG ADR, KHÔNG redefine Module Taxonomy/dependency graph/ngôn ngữ allocation — `ADR-008` (Approved) VẪN LÀ authority DUY NHẤT cho Python/Go/Rust layer assignment, `docs/engineering/monorepo.md` (Approved v0.5) VẪN LÀ authority cho repository topology, `module-registry.yaml` VẪN LÀ single source of truth cho module/dependency identity. **`ADR-025` v0.2 (Approved 2026-08-11) LÀ authority cho chính việc CÓ một cross-module Coding Standard baseline bắt buộc** (§12 dưới, sửa tại v0.2, đóng `EF-CODE-B-MAJ-01`) — tài liệu này LÀ living convention chứa chi tiết rule dưới authority đó, KHÔNG lặp lại decision text của ADR-025. Tài liệu này CHỈ quy định coding-quality convention CHUNG áp cho MỌI module — KHÔNG PHẢI Naming/Logging/Config/Error Handling/Testing/CI-CD (category riêng, CHƯA triển khai, xem §11).

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
[v0.2 sửa, đóng EF-CODE-A-MIN-01: bỏ analogy G-ID-002 — G-ID-002 quản
  governance/evidence identity (blob/version tài liệu), KHÔNG PHẢI
  package dependency resolution; dependency exact-pinning dưới đây LÀ
  MỘT Coding Standard convention riêng của chính nó, KHÔNG cần mượn
  authority từ G-ID-002.]

Mọi dependency (package Python, module Go) PHẢI có lý do sử dụng rõ ràng
  (giải quyết nhu cầu cụ thể, KHÔNG add "phòng khi cần"). Version pin
  CHÍNH XÁC (KHÔNG dùng range mở/`latest` cho production dependency) —
  đây LÀ Coding Standard convention riêng, đảm bảo build reproducible
  (xem §9). Cơ chế lockfile cụ thể (requirements.txt/poetry.lock/
  go.sum...) do package-manager choice (§1/`monorepo.md` §5) quyết
  định — CHƯA chọn tại đây.
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
[v0.2 sửa, đóng EF-CODE-A-MIN-02: "commit + dependency lock" (v0.1)
  ngụ ý MỘT lockfile representation chung cho mọi ngôn ngữ — SAI, §1/§4
  tường minh CHƯA chọn package-manager/lockfile mechanism nào. Sửa
  thành ecosystem-neutral: yêu cầu LÀ exact reproducibility của
  dependency/environment state, KHÔNG PHẢI một cơ chế cụ thể.]

Build/test PHẢI reproducible từ đúng source revision (commit) CỘNG một
  dependency/toolchain/configuration state CÓ THỂ reconstruct chính
  xác — KHÔNG phụ thuộc trạng thái máy local không ghi lại (biến môi
  trường ngầm, cache ẩn). Representation cụ thể của dependency/
  toolchain state (lockfile, checksum/module metadata, pinned manifest,
  toolchain declaration, hay cơ chế khác) do transaction tooling/
  package-management liên quan chọn (§1/§4/`monorepo.md` §5) — KHÔNG
  chọn tại đây, KHÔNG PHẢI MỘT lockfile format bắt buộc cho mọi ngôn
  ngữ. Đúng tinh thần I-2 Decision Parity (Research/Production cùng
  hàm) — mục này CHỈ khẳng định lại nguyên tắc reproducibility ở tầng
  build/dev, KHÔNG redefine I-2 (thuộc Constitution).
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

## 12. ADR-scope disposition — RESOLVED tại v0.2 bởi `ADR-025` (đóng `EF-CODE-B-MAJ-01`)

```text
[v0.1 kết luận SAI "ADR Not Required" cho chính việc CÓ một baseline
  chung — chỉ đánh giá vế "refactor-class, dễ đảo ngược" của Chapter 0
  §4b, bỏ sót hoàn toàn vế ">1 module." Việc "CÓ một Coding Standard
  baseline bắt buộc cho MỌI module" tự nó LÀ quyết định platform-wide,
  thỏa vế ">1 module" — ĐÃ ADR Required, bất kể chi tiết rule bên
  trong dễ sửa/đảo ngược tới đâu (reversibility KHÔNG hủy vế đó).]

Current state (v0.2, RESOLVED): `ADR-025` v0.2 (Approved 2026-08-11,
  "APPROVE ADR-025 V0.2") LÀ ADR đó — establish chính xác authority
  cho việc CÓ một cross-module Coding Standard baseline bắt buộc. Tài
  liệu này (`coding-standard.md`) LÀ living convention ALIGNED dưới
  `ADR-025` — chứa chi tiết rule reversible (format/lint/version-
  policy/dependency-hygiene/import-discipline/generated-code/comment/
  dead-code/determinism/exception-rule), KHÔNG lặp lại decision text
  của ADR-025.

Mọi thay đổi SEMANTIC tương lai vào tài liệu này (KHÔNG PHẢI mọi sửa —
  chỉ khi đổi Ý NGHĨA rule, không phải wording/typo) PHẢI tự chạy lại
  ADR Scope Rule (Chapter 0 §4b) hiện hành TẠI chính thời điểm đổi —
  KHÔNG suy diễn "reversible/refactor-class" LÀ đủ để miễn ADR (đúng
  `ADR-025` §3's nguyên tắc, KHÔNG redefine ở đây). Đa số thay đổi
  semantic baseline (áp dụng cho MỌI module) sẽ thỏa vế ">1 module"
  lại — CẦN đánh giá, KHÔNG tự động "đã có ADR-025 rồi nên miễn."

KHÔNG mục nào khác: thêm/sửa Platform Invariant, đổi Event Schema, đổi
  Module Taxonomy/dependency graph (§5's import discipline THỰC THI
  dependency graph ĐÃ có, KHÔNG tạo/đổi edge nào), thay đổi Governance/
  Approval process nào — nằm ngoài phạm vi ADR-025 đã resolve. Lịch sử
  thay đổi ghi tại CHANGELOG.md.
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
v0.2  2026-08-11  ADR-025 alignment + bounded correction, đóng
      `EF-CODE-B-MAJ-01`/`EF-CODE-A-MIN-01`/`EF-CODE-A-MIN-02`, vai trò:
      `Phase 1.5 Coding Standard ADR-025 Alignment Executor`.
      `EF-CODE-B-MAJ-01`: §12 v0.1 kết luận SAI "ADR Not Required" cho
      chính việc CÓ một baseline chung — bỏ sót vế ">1 module" của
      Chapter 0 §4b (reversibility KHÔNG hủy vế đó). Sửa: §12 nay ghi
      current-state RESOLVED — `ADR-025` v0.2 (Approved 2026-08-11) LÀ
      authority cho baseline-existence decision; tài liệu này LÀ living
      convention aligned dưới ADR-025; mọi thay đổi SEMANTIC tương lai
      PHẢI tự rerun ADR Scope Rule, KHÔNG suy diễn reversible LÀ miễn
      (đúng ADR-025 §3). Preamble + `depends_on` thêm `../adr/ADR-025`.
      `EF-CODE-A-MIN-01`: §4 bỏ analogy `G-ID-002` (governance/evidence
      identity, KHÔNG PHẢI dependency resolution) — dependency exact-
      pinning giữ nguyên LÀ convention riêng, KHÔNG cần mượn authority
      sai. `EF-CODE-A-MIN-02`: §9 "commit + dependency lock" (ngụ ý MỘT
      lockfile chung) sửa thành ecosystem-neutral — reproducibility từ
      source revision + dependency/toolchain/config state CÓ THỂ
      reconstruct chính xác, representation cụ thể (lockfile/checksum/
      pinned manifest/toolchain declaration/khác) do tooling transaction
      liên quan chọn, KHÔNG chọn tại đây. KHÔNG chọn formatter/linter/
      package-manager brand nào, KHÔNG pin language version nào, KHÔNG
      tạo config/tooling file nào. KHÔNG absorb Naming/Logging/Config/
      Error Handling/Testing/CI-CD. §1/§2/§3/§5/§6/§7/§8/§10/§11 KHÔNG
      đổi semantic. KHÔNG chạm `ADR-025`(Approved, immutable)/`ADR-008`/
      `ADR-024`/`module-registry.yaml`/Constitution/Phase 1.5 rules.
      `status` VẪN `Draft` — not self-approved (`G-ORCH-002`).
```
