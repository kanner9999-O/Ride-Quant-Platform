---
id: engineering-testing
title: "Engineering Foundation — Testing Convention"
version: "0.3"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-12"
last_review: null
next_review: null
depends_on: ["../constitution/03-engineering-principles", "../constitution/13-quality-gates", "../adr/ADR-008", "naming", "coding-standard", "error-handling", "config", "logging"]
---

# Engineering Foundation — Testing Convention

**APPROVED (2026-08-12) — status: Draft → Approved.** Product Owner decision: **"APPROVE TESTING CONVENTION V0.2."** Reviewed candidate: v0.2, blob `0a325665f5ed011a7439fb8d3c349c3db79d50fa`. `version: "0.2"` KHÔNG đổi (pure mechanical lifecycle approval — KHÔNG bump). Tài liệu này VẪN LÀ living document (Chapter 3 §3.2 "tài liệu SỐNG, không bất biến"; Chapter 0 §7.1 lifecycle Draft→...→Approved→Locked) — `Approved` KHÔNG đồng nghĩa immutable byte-for-byte như ADR (Chapter 11 §11.3 KHÔNG áp dụng ở đây, VÀ tài liệu này KHÔNG dưới authority một ADR nào — `ADR_NOT_REQUIRED` VẪN đúng); thay đổi tương lai vẫn hợp lệ qua version bump + re-review (Chapter 0 §8), VÀ mọi thay đổi SEMANTIC PHẢI tự rerun ADR Scope Rule đúng ADR-scope disposition.

**Review evidence tại approval này:**

```text
Đóng (trước approval, v0.2): EF-TEST-A-MAJ-01, EF-TEST-A-MIN-01.

Bounded Review A re-review trên v0.2:
  EF-TEST-A-MAJ-01: CLOSED
  EF-TEST-A-MIN-01: CLOSED
  New Blocker 0 / New Major 0 / New Minor 0
  CLEAN — READY_FOR_INDEPENDENT_REVIEW_B

Independent Review B:
  New Blocker 0 / New Major 0 / New Minor 0
  ADR_NOT_REQUIRED: CONFIRMED
  Verdict: READY_FOR_PRODUCT_OWNER_DECISION

Không finding/residual nào từ Review B cần Product Owner acceptance
  riêng tại approval này.
```

**Approval này KHÔNG đổi Testing Convention semantics nào** (§1–§18 dưới byte-equivalent ngoài banner/lifecycle metadata/change history này) — KHÔNG chạm Chapter 3/Chapter 13 (Locked)/`ADR-008`/`ADR-017`/`ADR-024`/`monorepo.md`/`ADR-025`/`coding-standard.md`/`ADR-026`/`naming.md`/`ADR-027`/`logging.md`/`ADR-028`/`config.md`/`ADR-029`/`error-handling.md`/`module-registry.yaml`/Domain Contract/Constitution/Phase 1.5 rules, KHÔNG tạo ADR-030, KHÔNG chọn framework/vendor, KHÔNG introduce production DI/API architecture, KHÔNG đóng `EF-CONFIG-B-MIN-01`/`EF-ERR-B-MIN-01`, KHÔNG mở CI/CD, KHÔNG authorize Phase 2, KHÔNG authorize LIVE. Stale editorial/provenance reference tới v0.1 (nếu có) KHÔNG sửa tại transaction này.

**Vai trò của tài liệu này:** convention document THỨ BẢY của Phase 1.5 — Engineering Foundation (Chapter 3 §3.2), phạm vi CHỈ category **Testing** (Chapter 14 §14.2's Phase 1.5 scope list) — đúng `EF-TXN-002` (một category = một transaction bounded). **KHÔNG author dưới authority một ADR mới** — ADR Scope Check (transaction riêng biệt trước) đã kết luận `ADR_NOT_REQUIRED`: [Chapter 3 §3.2](../constitution/03-engineering-principles.md) (Locked v1.4) ĐÃ established sẵn cả hai phần quyết định baseline-existence — (1) CÓ một Testing Convention category trong Engineering Foundation, VÀ (2) scope của nó GIỚI HẠN style/tooling (framework, cấu trúc test file, naming test case), coverage/tier requirement ĐÃ có đầy đủ tại [Chapter 13](../constitution/13-quality-gates.md) (Locked), KHÔNG định nghĩa lại. Tài liệu này CHỈ implement chi tiết reversible dưới boundary ĐÃ Locked đó — KHÔNG lặp lại/redefine bất kỳ Chapter 13 substance nào.

**Nguyên tắc chi phối (Chapter 3 §3.2 + Chapter 13 §13.2, tái khẳng định KHÔNG redefine):** Testing Convention CHỈ quản lý style/tooling — test structure, naming, isolation mechanics, fixture/mocking guidance, ngôn ngữ idiom, local command convention, flaky-test tooling mechanics. Chapter 13 VẪN authority DUY NHẤT cho coverage percentage/tier, tier resolution, parity substance (I-2), determinism/reproducibility substance (I-2/I-3/I-12, Chapter 5), quality-gate pass/fail semantics, immutable gate evidence contract, flaky-test POLICY (§13.10), module criticality (Chapter 7 §7.5). Tài liệu này KHÔNG tạo domain/architecture acceptance semantics mới.

**v0.2 — bounded correction (2026-08-12), đóng `EF-TEST-A-MAJ-01`/`EF-TEST-A-MIN-01`, vai trò: `Testing Convention v0.2 Bounded Correction Executor`.** Đóng `EF-TEST-A-MAJ-01` (§4 v0.1 nói module "cung cấp clock qua dependency injection/parameter khi cần test time-dependent logic" — đọc được như MANDATE một production-code API/design change CHỈ để thỏa testing convention, vượt ngoài Chapter 3 §3.2's boundary "style/tooling." Sửa: pin rõ Testing Convention CHỈ định nghĩa CÁCH dùng/control một seam ĐÃ tồn tại, KHÔNG BAO GIỜ bắt buộc production module tạo MỚI một DI pattern/parameter/interface/dependency CHỈ để thỏa convention; nếu deterministic testing KHÔNG đạt được mà KHÔNG đổi production design, đó LÀ một implementation/design gap PHẢI route qua authority sở hữu production design tương ứng VÀ tự rerun ADR Scope Rule nếu applicable, KHÔNG tự giải quyết tại `testing.md`). Đóng `EF-TEST-A-MIN-01` (§17 v0.1 tuyên bố "KHÔNG copy lại con số ngưỡng cụ thể" NHƯNG ngay sau đó liệt kê chính các con số đó — tự mâu thuẫn, duplicate policy text KHÔNG cần thiết. Sửa: bỏ hẳn con số, CHỈ giữ nguyên tắc "Chapter 13 §13.3/§13.4 LÀ authority DUY NHẤT," người đọc PHẢI resolve giá trị hiện hành trực tiếp từ Chapter 13). **KHÔNG đổi:** `ADR_NOT_REQUIRED` result, Chapter 3 style/tooling-only boundary, Chapter 13 quality-policy authority, test structure (§1), naming (§2), isolation (§3 phần còn lại), fixtures/factories (§5), mocking/stubbing (§6), unit/integration distinction (§7), contract/boundary testing (§8), Python guidance (§9), Go guidance (§10), test-data guidance (§11), flaky-test tooling mechanics (§12), local command convention (§13), reusable helpers (§14), Error Handling interaction (§15), Logging/Config boundaries (§16), quality-gate boundary (§18), framework/tool selection VẪN deferred, Non-goals. KHÔNG tạo ADR-030, KHÔNG chọn framework/vendor, KHÔNG introduce production DI architecture, KHÔNG chạm Chapter 3/Chapter 13/bất kỳ Approved ADR/convention nào. `EF-CONFIG-B-MIN-01`/`EF-ERR-B-MIN-01` KHÔNG chạm. `status` VẪN `Draft`.

**v0.3 — CANDIDATE amendment (2026-08-20), KHÔNG self-approved, vai trò: `Go Branch-Coverage Mechanism Candidate Author`.** `status: Approved → Draft` (mọi thay đổi SEMANTIC vào tài liệu Approved bắt buộc tăng version VÀ đi qua approval gate lại, đúng [Chapter 0 §5.1](../constitution/00-governance.md); `approved_by`/`approved_at` của v0.2 KHÔNG tự động phủ nội dung MỚI này — reset `null`, v0.2's approval record giữ nguyên nguyên vẹn phía trên LÀM historical evidence, KHÔNG bị ghi đè). Bổ sung MỘT subsection MỚI dưới "Framework/tool selection" (dưới) đề xuất một **CANDIDATE** (chưa chọn/chưa cài đặt/chưa tích hợp) cho cơ chế đo **Go branch-coverage** — khoảng trống evidence DUY NHẤT còn lại cho `market-reference-service`'s Chapter 13 Quality Gate sau khi line coverage VÀ I-13 property-based evidence đã có (`P3-MR-QG-A-MAJ-01` closure history, `docs/MANIFEST.md`). **ADR-scope check (chạy TRƯỚC KHI author, [Chapter 0 §4b](../constitution/00-governance.md)):** kết luận `ADR_NOT_REQUIRED` — xem "Go branch-coverage mechanism — CANDIDATE" dưới cho full reasoning; tóm tắt: [Chapter 3 §3.2](../constitution/03-engineering-principles.md) dòng 44 ĐÃ có carve-out tường minh cho Testing Convention ("chỉ quy định style/tooling... coverage/tier requirement đã có đầy đủ ở Chapter 13, không định nghĩa lại") VÀ [Chapter 13 §13.3](../constitution/13-quality-gates.md)/[§13.14](../constitution/13-quality-gates.md) tự nó khóa "không khóa tool/vendor cụ thể... defer Engineering Foundation" — đây LÀ pattern (b) đã dùng cho chính `testing.md` v0.1 ban đầu (existing Locked authority ĐÃ pre-resolve baseline-existence + scope boundary), KHÁC pattern (a) `ADR-030` phải dùng cho CI/CD (KHÔNG carve-out nào tồn tại cho CI/CD tại Chapter 3 §3.2 trước ADR-030) — verify trực tiếp `docs/adr/ADR-030.md` §1 Context xác nhận chính hai pattern này. Đây CHỈ LÀ candidate selection trong phạm vi "tooling" ĐÃ pre-authorized, KHÔNG PHẢI một baseline-existence decision mới, KHÔNG platform invariant/event schema/module taxonomy/governance-process change, KHÔNG supersede ADR đã Locked nào, KHÔNG hard-to-reverse lock-in (dev/test-time-only Go CLI tool, BSD-2-Clause, không vendor/infrastructure coupling). **KHÔNG đổi:** Chapter 13 coverage floor/tier/pass-fail semantics nào (§17/§18 dưới, KHÔNG đổi), `module-registry.yaml`, dependency graph, production/test code, CI/CD (`ci-cd.md`/`ADR-030`, KHÔNG chạm), §1–§16/§18/Non-goals/ADR-scope disposition gốc (byte-equivalent). KHÔNG cài đặt/tích hợp tool nào tại transaction này. KHÔNG rerun Quality Gate nào. KHÔNG approve module/Data Layer nào. KHÔNG authorize LIVE.

## 1. Test structure

```text
Tổ chức test PHẢI predictable, nhất quán xuyên module — KHÔNG redesign
  monorepo topology (`monorepo.md` §2/§3 VẪN authority DUY NHẤT cho
  `python/<module_id>/`/`go/<module_id>/`).
Colocated test (Go idiom, `_test.go` cùng package/directory với source)
  VÀ dedicated test directory (Python idiom, vd `tests/` cấp module)
  ĐỀU được phép — mỗi ngôn ngữ dùng ĐÚNG convention idiomatic của chính
  nó (§9/§10 dưới), KHÔNG ép một layout chung xuyên Python/Go.
Test file PHẢI đặt tên phản ánh module/component nó test — Python:
  `test_<module>.py` hoặc `<module>_test.py` (nhất quán trong CÙNG một
  module, đúng PEP 8 convention thường dùng); Go: `<file>_test.go`
  (idiomatic, bắt buộc bởi chính Go toolchain).
Package/module correspondence: test file/package PHẢI map rõ ràng tới
  source unit nó verify — KHÔNG một test file lớn test nhiều unrelated
  component chỉ vì tiện.
Phân biệt unit/integration/E2E/contract-style test (§7/§8) khi có ích
  cho tổ chức — vd subdirectory riêng (`unit/`, `integration/`) hoặc
  build tag/marker riêng theo idiom ngôn ngữ — KHÔNG bắt buộc một cấu
  trúc CỤ THỂ duy nhất tại v0.1 này, MIỄN LÀ nhất quán trong CÙNG một
  module.
```

## 2. Test naming

```text
Tên test case PHẢI thể hiện RÕ behavior/condition/result đang verify —
  ưu tiên semantic behavior naming (vd
  `test_reject_when_quantity_is_zero`) hơn implementation-detail naming
  (vd `test_function_1`, `test_case_a`).
Align với `naming.md` (Approved) — general identifier naming convention
  (Python snake_case, Go PascalCase/camelCase theo export scope, §2/§3
  của `naming.md`) áp dụng ĐÚNG cho tên test function/method NHƯ MỌI
  identifier khác — tài liệu này KHÔNG tạo naming authority thứ hai,
  KHÔNG redefine `naming.md`.
Go table-driven test case (§10 dưới): tên test case con (subtest name,
  `t.Run(name, ...)`) PHẢI mô tả condition, KHÔNG PHẢI index số thứ
  tự vô nghĩa.
```

## 3. Test isolation

```text
Test PHẢI:
  tránh order dependence — kết quả một test KHÔNG được phụ thuộc test
    nào chạy TRƯỚC nó (test PHẢI pass dù chạy riêng lẻ hay chạy cùng
    suite theo thứ tự bất kỳ);
  tránh hidden shared mutable state (global/module-level state bị một
    test sửa và ảnh hưởng test khác mà KHÔNG explicit setup/teardown);
  clean up resource nó sở hữu (file tạm, connection, temp directory...)
    — KHÔNG để lại side effect ảnh hưởng test run sau;
  tránh phụ thuộc wall-clock timing khi CÓ deterministic alternative
    (§4 dưới) — vd KHÔNG `sleep()` rồi assert dựa trên thời gian thật
    trôi qua khi injectable clock khả dụng.
Tài liệu này KHÔNG redefine Chapter 13 determinism substance (I-2/I-3,
  §13.2) — CHỈ pin engineering-style isolation practice giúp test
  KHÔNG VÔ TÌNH vi phạm determinism đã yêu cầu ở tầng platform.
```

## 4. Deterministic test mechanics

```text
[v0.2 sửa, đóng `EF-TEST-A-MAJ-01`: v0.1 nói module "cung cấp clock
  qua dependency injection/parameter khi cần test time-dependent
  logic" — đọc được như MANDATE một production-code API/design change
  (buộc module thêm DI pattern/constructor-parameter/interface mới)
  CHỈ để thỏa testing convention — vượt ngoài Chapter 3 §3.2's boundary
  "style/tooling," vì đó LÀ một production architecture decision,
  KHÔNG PHẢI test-side convention. Sửa: pin rõ Testing Convention CHỈ
  quy định CÁCH dùng/control một seam ĐÃ tồn tại, KHÔNG bắt buộc tạo
  seam mới trong production code.]

Style/tooling guidance (KHÔNG tạo platform determinism rule mới, CHỈ
  hỗ trợ test tuân thủ determinism substance ĐÃ có, §13.2):
  time-dependent behavior — test PHẢI dùng một controllable
    deterministic time mechanism KHI MỘT mechanism như vậy ĐÃ tồn tại
    (vd clock/time abstraction, parameter, fake adapter, test harness,
    hay bất kỳ seam nào đã được production code/authority hiện hành
    authorize sẵn) — Testing Convention CHỈ định nghĩa CÁCH test sử
    dụng/control seam đó (vd cách inject giá trị fake clock vào seam
    ĐÃ có, cách seed nó, cách verify), KHÔNG BAO GIỜ bắt buộc một
    production module PHẢI tạo MỚI một dependency-injection pattern,
    constructor/function parameter, published interface, module
    dependency, hay bất kỳ production architecture nào CHỈ để thỏa
    convention này;
  NẾU deterministic testing cho một behavior cụ thể KHÔNG đạt được mà
    KHÔNG thay đổi production design/contract (vd module gọi trực tiếp
    system clock, KHÔNG seam nào khả dụng), đây LÀ một implementation/
    design gap — Testing Convention KHÔNG tự giải quyết gap đó tại
    đây: report gap đó, route qua đúng authority sở hữu production
    design tương ứng (vd module owner, hoặc Coding Standard/Config
    Convention nếu applicable), VÀ tự rerun ADR Scope Rule (Chapter 0
    §4b) hiện hành nếu applicable — KHÔNG tự thiết kế production
    architecture change tại `testing.md`;
  seeded randomness — mọi randomness dùng trong test PHẢI seeded rõ
    ràng, kết quả reproducible;
  deterministic fixture (§5 dưới) — dữ liệu input cố định, KHÔNG sinh
    ngẫu nhiên không seed;
  explicit event-time input — khi domain logic phụ thuộc effective-
    time/event-time (Chapter 5 Time Model, KHÔNG đổi) VÀ một seam ĐÃ
    tồn tại cho phép cung cấp giá trị đó, test NÊN cung cấp giá trị đó
    explicit qua seam sẵn có, KHÔNG suy diễn từ thời điểm chạy test —
    NẾU KHÔNG seam nào tồn tại, áp dụng nguyên tắc "implementation/
    design gap" trên, KHÔNG tự tạo seam mới tại đây;
  stable test data (§11 dưới) — dữ liệu KHÔNG thay đổi giữa các lần
    chạy trừ khi chính test đó chủ động thay đổi.
```

## 5. Fixtures and factories

```text
Reusable test data builder/factory PHẢI:
  có default value explicit (rõ ràng field nào mang giá trị gì theo
    default, KHÔNG giá trị "magic" ẩn trong factory code);
  cho phép override tại call site VISIBLE (test đọc được ngay giá trị
    nào bị override cho CHÍNH test case đó, KHÔNG phải tìm trong factory
    definition mới biết);
  tránh oversized opaque fixture (một fixture khổng lồ chứa nhiều field
    không liên quan tới test case đang verify, làm khó đọc/khó maintain);
  domain fixture (vd một `Account`/`RiskEvaluation` giả cho test) PHẢI
    VẪN hợp lệ dưới Domain Contract authority hiện hành (`/docs/domain/`)
    — KHÔNG invent domain semantics/field mới CHỈ để tiện test (vd
    KHÔNG tạo enum value giả không tồn tại trong domain contract thật).
```

## 6. Mocking and stubbing

```text
Bounded guidance:
  mock external/dependency boundary (network call, external service,
    filesystem, clock...) — KHÔNG mock behavior ĐANG được test (test
    PHẢI verify behavior thật của unit đó, KHÔNG mock chính nó);
  ưu tiên fake/stub khi nó preserve meaningful behavior (vd một in-
    memory fake repository giữ đúng semantic CRUD) hơn một mock chỉ
    trả về giá trị cứng KHÔNG phản ánh behavior thật;
  tránh mock authoritative production logic (vd domain/business rule
    thật) CHỈ để test pass dễ hơn — nếu logic đó cần verify, test PHẢI
    exercise logic thật;
  KHÔNG dùng mock LÀM coverage inflation (vd mock away toàn bộ logic
    rồi assert một call count vô nghĩa CHỈ để tăng số coverage) — đúng
    Chapter 13's anti-gaming requirement (§13.3, KHÔNG đổi) — "chỉ tính
    coverage từ test có assertion có nghĩa."
```

## 7. Unit vs integration tests

```text
Phân biệt ở tầng engineering-style (KHÔNG gán quality tier hay mandatory
  count nào — thuộc Chapter 13, KHÔNG tại đây):
  unit test  — exercise MỘT bounded implementation unit (function/
    method/class nhỏ), dependency được control (fake/stub/inject) —
    tốc độ nhanh, KHÔNG cần external system thật;
  integration test  — exercise tương tác THẬT giữa các component/
    boundary đã chọn (vd hai module giao tiếp qua contract thật, hoặc
    một component với một dependency thật/gần-thật) — verify boundary
    interaction, KHÔNG CHỈ logic nội bộ một unit.
Tài liệu này KHÔNG quyết định module/artifact nào PHẢI có bao nhiêu
  unit vs integration test, KHÔNG quyết định tier nào yêu cầu loại nào
  — Chapter 13 tier requirement (§13.4) VẪN authority DUY NHẤT cho đó.
```

## 8. Contract/boundary testing

```text
Khi một published interface tồn tại (Event/API/command/query contract,
  `/docs/domain/`), test NÊN verify:
  serialization/translation mechanics (dữ liệu encode/decode đúng
    format contract yêu cầu);
  required field có mặt/validate đúng (KHÔNG missing field required);
  error propagation (lỗi tại boundary propagate đúng theo Error
    Handling Convention, §15 dưới);
  compatibility với contract ĐÃ authoritative hiện hành (KHÔNG test
    dựa trên một contract giả định KHÔNG tồn tại).
Tài liệu này KHÔNG redefine chính những contract đó — Domain/Event/API
  contract authority (`/docs/domain/`) VẪN giữ nguyên (§18 dưới).
```

## 9. Python testing conventions

```text
Idiomatic, tool-light:
  test file naming theo §1 (`test_<module>.py` hoặc `<module>_test.py`,
    nhất quán trong module);
  fixture use theo idiom test framework hiện hành (khi framework được
    chọn — §"Framework/tool selection" dưới) — CHỈ nguyên tắc: fixture
    PHẢI explicit, scope rõ ràng (function/module/session), KHÔNG side
    effect ẩn xuyên test case KHÔNG liên quan;
  parametrized test case cho input tương tự lặp lại (giảm duplication,
    §14 dưới) — MỖI parameter set PHẢI đại diện một condition có nghĩa,
    KHÔNG parametrize CHỈ để tăng số lượng test case;
  exception assertion PHẢI verify đúng exception type/semantic category
    (§15 dưới), KHÔNG CHỈ verify "một exception nào đó" xảy ra;
  tránh broad integration setup (spin up dependency thật, network,
    DB...) trong unit test (§7) — unit test PHẢI giữ nhanh/isolated.
Tài liệu này KHÔNG chọn concrete test framework (pytest/unittest/...)
  tại v0.1 này — verify trực tiếp: KHÔNG framework nào đã pin bởi
  authority hiện hành (`coding-standard.md`/`ADR-008`/`ADR-025` KHÔNG
  chọn tool cụ thể, `python/` directory CHỈ chứa `README.md` placeholder,
  KHÔNG dependency file nào tồn tại) — framework selection VẪN deferred
  (§"Framework/tool selection" dưới).
```

## 10. Go testing conventions

```text
Idiomatic:
  `_test.go` (bắt buộc bởi Go toolchain, §1) — colocated cùng package
    với source;
  table-driven test khi có ích (nhiều input/expected-output tương tự)
    — mỗi row/case PHẢI có tên mô tả condition (§2);
  subtest (`t.Run(name, func(t *testing.T) {...})`) để tách bạch case
    trong CÙNG một test function, giúp report rõ case nào fail;
  error assertion explicit (`if err != nil` / `errors.Is`/`errors.As`
    theo idiom, §15 dưới) — KHÔNG ignore error trả về trong test;
  helper function dùng trong test PHẢI đánh dấu `t.Helper()` khi
    applicable (giúp stack trace/report chỉ đúng vị trí lỗi thật);
  tránh unnecessary mocking abstraction (Go idiom thường ưu tiên
    interface nhỏ + fake struct đơn giản hơn mocking framework nặng,
    MIỄN LÀ đạt được §6 trên).
Tài liệu này KHÔNG mandate third-party framework (testify/gomock/...)
  — verify trực tiếp: KHÔNG framework nào đã pin bởi authority hiện
  hành, `go/` directory CHỈ chứa `README.md` placeholder, KHÔNG
  `go.mod` nào tồn tại — standard library `testing` package ĐỦ cho nhu
  cầu hiện tại, framework bổ sung (nếu cần) VẪN deferred.
```

## 11. Test data

```text
Test dataset PHẢI nhỏ VÀ deterministic theo default (§4) — KHÔNG cần
  dataset lớn để verify một behavior cụ thể, TRỪ KHI chính test đó
  explicit cần scale (vd performance test, KHÔNG PHẢI unit/integration
  test thông thường).
Generated data (nếu dùng) PHẢI seeded/reproducible (§4) — KHÔNG random
  data KHÔNG seed.
Dữ liệu production nhạy cảm KHÔNG được copy vào test dưới bất kỳ hình
  thức nào TRỪ KHI security authority hiện hành (`ADR-017`, KHÔNG đổi)
  explicit cho phép — đúng nguyên tắc `logging.md`/`config.md`/
  `error-handling.md` §"Security and redaction," tái khẳng định nhất
  quán cho test data.
Golden/snapshot data (nếu dùng) PHẢI validate meaningful semantics
  (assertion CÓ Ý NGHĨA về nội dung), KHÔNG CHỈ verify "output tồn
  tại"/"output không đổi format" mà KHÔNG kiểm nội dung — đúng Chapter
  13 §13.3's "chỉ tính coverage từ test có assertion có nghĩa," tái
  khẳng định nhất quán, KHÔNG redefine.
```

## 12. Flaky-test tooling mechanics

```text
Chapter 13 §13.10 (Locked) ĐÃ pin chính POLICY — KHÔNG redefine tại
  đây:
  cấm retry-until-green để đưa gate về pass;
  flaky test (kết quả không ổn định trên cùng input đã pin) KHÔNG được
    tính LÀM passing evidence cho invariant nó tuyên bố verify;
  test phụ thuộc timing/ordering/clock PHẢI quarantine, ghi explicit
    follow-up (MANIFEST/backlog).
Chapter 13 §13.10 explicit defer "Quarantine tooling" tới Phase 1.5 —
  tài liệu này CHỈ định nghĩa tooling/style mechanics cho quarantine
  đó, KHÔNG tại lại policy:
  quarantine marker/tag/location PHẢI rõ ràng, dễ tìm (vd một marker/
    build-tag riêng theo idiom ngôn ngữ, hoặc một naming/location
    convention riêng cho test bị quarantine — công cụ cụ thể KHÔNG
    chọn tại đây, §"Framework/tool selection");
  quarantine record PHẢI mang owner/reason/reference (ai quarantine,
    tại sao, tham chiếu follow-up item nào — đúng §13.10's "explicit
    follow-up");
  test bị quarantine PHẢI VẪN visible trong CI/reporting (KHÔNG bị ẩn
    hoàn toàn khỏi report/output — chỉ KHÔNG tính LÀM gate-passing
    evidence);
  quarantine KHÔNG được silently convert failure thành pass — cơ chế
    quarantine CHỈ đổi CÁCH kết quả được TREAT bởi gate (KHÔNG tính LÀ
    evidence, đúng §13.10), KHÔNG đổi kết quả pass/fail thật của chính
    test đó.
Tài liệu này KHÔNG chọn quarantine product/plugin cụ thể — chưa authority
  nào chọn, deferred (§"Framework/tool selection").
```

## 13. Local test commands

```text
Developer-facing test command PHẢI predictable — repository NÊN cung
  cấp một entry point tài liệu hóa rõ ràng (vd một lệnh alias/task
  chuẩn per module/workspace, CỤ THỂ tool nào KHÔNG chọn tại đây) hơn
  là buộc developer nhớ nhiều raw command khác nhau cho từng module/
  ngôn ngữ.
Tài liệu này KHÔNG hardcode một build/test tool CỤ THỂ chưa được chọn
  ở nơi khác (`monorepo.md` §5 "Workspace/package-manager tooling" VẪN
  `deferred`, KHÔNG đổi tại đây) — khi tooling đó được chọn (transaction
  riêng biệt tương lai), local test command convention NÊN align theo
  nó, KHÔNG tại v0.1 này quyết định trước.
```

## 14. Reusable helpers

```text
Test helper (function/utility dùng lại xuyên nhiều test case) PHẢI:
  giảm duplication (tránh lặp lại cùng setup logic nhiều nơi);
  KHÔNG che giấu assertion quan trọng (một helper "quá thông minh" tự
    verify NGẦM một điều kiện mà test case gọi nó KHÔNG biết/KHÔNG
    explicit assert điều đó);
  KHÔNG encode domain semantics cạnh tranh với Domain Contract authority
    (đúng §5's nguyên tắc, tái khẳng định);
  giữ deterministic (§4);
  đặt tại vị trí predictable (vd một test-helper module/package riêng
    theo idiom ngôn ngữ, dễ tìm — vị trí CỤ THỂ do module tự quyết định,
    tài liệu này KHÔNG bắt buộc một path duy nhất xuyên platform).
```

## 15. Error assertions

```text
Align với `error-handling.md` (Approved) — test verify semantic failure
  behavior NÊN check đúng error category/cause (đúng error-handling.md
  §1/§3, KHÔNG đổi) khi liên quan, KHÔNG couple với implementation
  detail không cần thiết.
Tránh assert FULL raw internal error string/message khi một stable
  semantic category/cause ĐỦ để verify đúng behavior — assert message
  string đầy đủ dễ vỡ khi wording nội bộ đổi mà KHÔNG PHẢI regression
  thật.
Tài liệu này KHÔNG tạo platform error-code schema nào tại đây —
  `error-handling.md` §"Non-goals" VẪN giữ nguyên (error-code convention
  cụ thể VẪN deferred, KHÔNG tại testing.md).
```

## 16. Logging/config interaction

```text
Testing CÓ THỂ verify existing Config/Logging behavior (vd một test
  xác nhận module fail-closed đúng khi config invalid, đúng `config.md`
  §7; hay một test xác nhận log record structured đúng §2 của
  `logging.md`) — verification LÀ hợp lệ, KHÔNG redefine chính rule đó.
Testing Convention KHÔNG được redefine:
  Config validation/startup rule (`config.md` §6/§7, KHÔNG đổi);
  Logging level/field/schema semantics (`logging.md` §3/§5, KHÔNG đổi).
```

## 17. Coverage boundary

```text
[v0.2 sửa, đóng `EF-TEST-A-MIN-01`: v0.1 nói "KHÔNG copy lại con số
  ngưỡng cụ thể" NHƯNG ngay sau đó liệt kê chính các con số đó (Tier 0
  ≥ 95%/Tier 1 ≥ 90%/Tier 2 ≥ 80%/Tier 3 ≥ 60%) — tự mâu thuẫn, tạo
  duplicate policy text KHÔNG cần thiết (đúng rủi ro I-12 mà chính câu
  đó đang cảnh báo). Sửa: bỏ hẳn con số, CHỈ giữ nguyên tắc.]

Testing Convention KHÔNG sở hữu coverage threshold nào — Chapter 13
  (`13-quality-gates.md`, Locked) LÀ authority DUY NHẤT cho coverage
  percentage/floor VÀ tier mapping (§13.3/§13.4). Tài liệu này CHỦ Ý
  KHÔNG lặp lại con số ngưỡng cụ thể nào tại đây, để tránh tạo một
  "bản sao" số liệu dễ lệch khỏi Chapter 13 gốc theo thời gian (I-12
  Single Source of Truth). Khi cần biết giá trị hiện hành, người đọc
  PHẢI resolve trực tiếp từ `13-quality-gates.md` §13.3/§13.4 — tài
  liệu này KHÔNG tạo một coverage policy thay thế nào.
```

## 18. Quality-gate boundary

```text
Testing style/tooling (§1–§16 trên) sản sinh test artifact/evidence
  input (vd test result, coverage report thô) — CHÍNH Quality Gate
  semantics (eligibility, evidence contract §13.9, tier resolution
  §13.4, pass/fail determination) VẪN authority DUY NHẤT của Chapter
  13. Tài liệu này KHÔNG redefine bất kỳ mục nào trong số đó, KHÔNG tạo
  một gate/evidence authority thứ hai.
Domain/Event/API contract authority (/docs/domain/), module identity/
  dependency (`module-registry.yaml`), ngôn ngữ (`ADR-008`), repository
  topology (`monorepo.md`), Coding Standard (`coding-standard.md`),
  Naming (`naming.md`), Logging (`logging.md`), Config (`config.md`),
  Error Handling (`error-handling.md`), Custody & Signing Trust Boundary
  (`ADR-017`) — TẤT CẢ giữ nguyên, KHÔNG redefine tại đây.
```

## Framework/tool selection

```text
Verify trực tiếp tại transaction này: KHÔNG concrete test framework/
  library nào (pytest, unittest, testify, gomock, hay bất kỳ tool
  khác) đã được authoritatively pin bởi bất kỳ existing authority
  (`ADR-008`, `coding-standard.md`, `monorepo.md`, ADR-024/025) —
  `python/README.md`/`go/README.md` CHỈ LÀ source-tree marker
  (`monorepo.md`, KHÔNG chứa logic/dependency nào), KHÔNG dependency
  manifest (`requirements.txt`, `pyproject.toml`, `go.mod`...) tồn tại
  trong repository tại boundary transaction này.
Framework selection VẪN deferred — tài liệu này KHÔNG chọn pytest/
  unittest/testify/gomock/etc tại v0.1 này. Khi cần chọn (implementation-
  readiness transaction riêng biệt tương lai), lựa chọn đó PHẢI align
  với §9/§10 trên (idiomatic Python/Go convention đã pin) VÀ verify
  trực tiếp KHÔNG có authority nào khác đã chọn trước, đúng `EF-VERIFY-001`.
```

### Go branch-coverage mechanism — CANDIDATE (v0.3, pending Product Owner decision)

```text
[v0.3 bổ sung — vai trò: `Go Branch-Coverage Mechanism Candidate Author`.
  Đây LÀ implementation-readiness transaction §"Framework/tool selection"
  trên ĐÃ anticipate — GIỚI HẠN CHỈ Go branch-coverage MEASUREMENT
  MECHANISM (Chapter 13 §13.3's second, hiện thiếu, coverage metric),
  KHÔNG PHẢI general test framework selection (pytest/testify/gomock VẪN
  deferred, KHÔNG chạm tại đây).]

Vấn đề: market-reference-service Tier 2 yêu cầu line coverage >= 80% VÀ
  branch coverage >= 80%, độc lập (§13.3, KHÔNG đổi). Line coverage VÀ
  I-13 property-based evidence đã có (P3-MR-QG-A-MAJ-01 evidence
  correction/remediation, MANIFEST). Gap CÒN LẠI DUY NHẤT: branch
  coverage evidence — Go's built-in toolchain (verify trực tiếp
  `go help testflag`/`go tool cover -h`/`go tool covdata -h`, tool
  version go1.26.6 darwin/arm64) CHỈ đo statement/block coverage
  (-covermode=set|count|atomic VÀ GOCOVERDIR-based `go tool covdata`,
  KHÔNG subcommand nào tạo branch/condition metric độc lập). Verify
  trực tiếp golang/go#70306 ("proposal: cmd/cover: support branch
  coverage", mở 2024-11-12): VẪN `Open`/`Incoming`, KHÔNG assignee,
  KHÔNG PR, KHÔNG ETA — native support KHÔNG tồn tại VÀ KHÔNG sắp có.

Statement/block proxy — verify trực tiếp VÀ TỪ CHỐI (KHÔNG được tính LÀ
  branch coverage dưới bất kỳ tên gọi nào):
  - `go tool cover` / `go tool covdata` (mọi subcommand: textfmt,
    percent, func, pkglist, merge, subtract, intersect, debugdump) —
    statement/block granularity, KHÔNG branch/condition metric.
  - `gocov` (github.com/axw/gocov, archived; fork cộng đồng
    github.com/gwthm-in/gocov) + `gocov-html`/`gocov-xml` — convert/
    report statement coverage, KHÔNG đo branch.
  - `go-carpet` (github.com/msoap/go-carpet) — terminal visualizer cho
    CHÍNH `go test -cover`'s statement coverage, KHÔNG branch metric
    riêng.
  - `go-test-coverage` (github.com/vladopajic/go-test-coverage),
    `goc`, `Courtney` — threshold-gate/collection tool trên statement
    coverage profile CÓ SẴN, KHÔNG tạo branch metric mới.
  - "gocov-branch" — verify trực tiếp: KHÔNG tồn tại LÀM một project
    được maintain độc lập, xác nhận lại kết luận đã ghi tại P3-MR
    formal QG evaluation (MANIFEST).

CANDIDATE mechanism được đề xuất: **gobco**
  (github.com/rillig/gobco, tác giả Roland Illig). Đánh giá theo 10 tiêu
  chí (verify trực tiếp GitHub repo/README/main.go/pkg.go.dev, KHÔNG từ
  memory):
  1. Available/maintained: tag gần nhất v1.3.4 (2024-03-08, 10 tag từ
     2022-11-24); single-maintainer project, VẪN nhận commit activity
     sau tag gần nhất — ghi nhận LÀ maintenance-concentration risk
     tường minh, KHÔNG che giấu, KHÔNG LÀ lý do từ chối candidate (repo
     tooling khác cùng lớp — testify/gomock — cũng thường single/small-
     team-maintained, đúng pattern rủi ro chung của ecosystem này).
  2. Đo branch thật, KHÔNG statement/block dưới tên khác: instrument
     boolean sub-expression (so sánh, `&&`, `||`, `!`) VÀ track riêng
     mỗi condition được evaluate `true` VÀ `false` trong khi chạy test
     thật — đây LÀ condition/branch coverage, KHÔNG PHẢI statement
     coverage đổi tên. Granularity CHẶT hơn floor bắt buộc (§13.3 CHỈ
     yêu cầu branch, MC-DC "tùy chọn theo tier, không tính vào floor
     bắt buộc") — dư, KHÔNG thiếu, KHÔNG vi phạm.
  3. Go version/platform: yêu cầu Go 1.17+ (`go install
     github.com/rillig/gobco@<version>`) — tương thích go.mod hiện tại
     (`go 1.25`, build/test bằng go1.26.6). Generics/parser compat
     PHẢI verify lại trực tiếp (chạy `gobco -help`/thử nghiệm) TẠI
     transaction cài đặt tương lai — KHÔNG giả định tại candidate này.
  4. Reproducibility/determinism: đo trên lần chạy test thật (qua
     `go test` thật, KHÔNG mock kết quả) — output deterministic CHỪNG
     NÀO chính test suite deterministic (đúng yêu cầu §13.2/I-2/I-3 ĐÃ
     có, KHÔNG tạo rule mới). KHÔNG network access khi chạy (chỉ cần
     network một lần LÚC `go install`, giống mọi Go module dependency).
  5. Pin tool/version/content identity: Go module — pin được exact
     module path + version tag + `go.sum` content hash, cùng cấp exact-
     artifact rule Chapter 13 §13.9 đã yêu cầu cho mọi evidence khác
     (tương tự cách evidence hiện tại đã pin "go version go1.26.6
     darwin/arm64" chính xác).
  6. Local execution/tương lai CI: chạy `gobco` CLI trực tiếp trong
     package directory — instrument VÀO một temp directory riêng
     (`os.TempDir()/gobco-<random>`, copy package source sang đó), gọi
     `go test` THẬT trên bản copy đã instrument, KHÔNG sửa file gốc
     trong repository — local execution NGAY tại transaction cài đặt
     tương lai; CI suitability hợp lý (CLI đơn, exit-code/text output,
     KHÔNG cần service ngoài) nhưng KHÔNG quyết định CI integration tại
     đây (`ci-cd.md`/`ADR-030` authority riêng, KHÔNG chạm).
  7. Output format cho Chapter 13 immutable evidence: text output có
     tổng coverage (vd "Condition coverage: N/M") VÀ danh sách từng
     condition chưa đạt (file/line/column/lần true/lần false) — đủ chi
     tiết pin vào evidence entry (§13.9: subject identity, boundary,
     input identity) giống format `go tool cover -func` hiện đang dùng
     cho line coverage evidence.
  8. Anti-gaming/authoritative-implementation (§13.3): instrumentation
     copy source sang temp dir CHỈ để CHÈN counter quanh boolean sub-
     expression — KHÔNG đổi control flow/logic, KHÔNG generate/mock
     thay thế implementation thật, bản build/run vẫn LÀ authoritative
     implementation cộng counter phi-semantic — cùng category kỹ thuật
     với chính `go tool cover`'s source-to-source instrumentation
     (repository ĐÃ chấp nhận cơ chế này cho line coverage) — KHÔNG
     shadow code theo nghĩa §13.3 cấm. File gốc trong repository KHÔNG
     bị sửa bởi chính hành động đo.
  9. Maintenance/security/dependency impact: BSD-2-Clause (permissive,
     rủi ro pháp lý thấp) — verify trực tiếp `LICENSE` file. Dev/test-
     time-only dependency (KHÔNG production runtime dependency nào của
     module bị ảnh hưởng — module vẫn "zero dependencies" ở production
     path). Single-maintainer risk đã ghi tại điểm 1 — candidate note
     này KHÔNG tự cài đặt gì, risk đó PHẢI cân nhắc lại TẠI transaction
     cài đặt tương lai cùng bất kỳ candidate nào khác xuất hiện.
  10. Alternative approach KHÔNG làm yếu branch metric của Chapter 13:
     KHÔNG có — mọi alternative kiểm tra được (chấp nhận statement
     coverage LÀM proxy, ước lượng branch từ statement, bỏ qua metric)
     ĐỀU vi phạm trực tiếp §13.3's "không bù trừ giữa hai metric,
     không dùng con số tổng hợp" VÀ "không estimate" — bị từ chối
     tường minh, KHÔNG đề xuất tại đây.

ADR-scope disposition (đầy đủ, chạy TRƯỚC khi author candidate này,
  [Chapter 0 §4b](../constitution/00-governance.md)): **`ADR_NOT_REQUIRED`.**
  Authority kiểm soát kết quả: [Chapter 13 §13.3](../constitution/13-quality-gates.md)
  ("Không khóa tool/vendor cụ thể (defer §13.14)") VÀ
  [Chapter 13 §13.14](../constitution/13-quality-gates.md) ("concrete
  tooling... defer sang Engineering Foundation Chapter 3 §3.2") ĐÃ
  Locked VÀ tự nó chỉ định CHÍNH Chapter 3 §3.2/Testing Convention LÀM
  authority cho quyết định này — KHÔNG phải một chapter/ADR khác. Chapter
  3 §3.2 dòng 44 (Locked v1.4) ĐÃ có carve-out tường minh: "Testing
  Convention ở đây chỉ quy định style/tooling (framework, cấu trúc test
  file, naming test case)" — một cơ chế đo coverage LÀ "tooling" theo
  đúng nghĩa đó, KHÔNG PHẢI một baseline-existence question mới (Testing
  Convention category đã tồn tại, `testing.md` v0.2 đã Approved). Đây
  chính LÀ "pattern (b)" mà `docs/adr/ADR-030.md` §1 Context tự mô tả
  ("existing Locked authority ĐÃ pre-resolve baseline-existence + scope
  boundary → living convention author trực tiếp, KHÔNG ADR (Testing)")
  — TƯƠNG PHẢN trực tiếp với "pattern (a)" ADR-030 phải dùng cho CI/CD
  (KHÔNG carve-out tương tự tồn tại cho CI/CD tại Chapter 3 §3.2, buộc
  ADR trước khi author `ci-cd.md`). Verify từng nhánh Chapter 0 §4b:
  KHÔNG Platform Invariant nào đổi (Chapter 2, KHÔNG chạm); KHÔNG Event
  Schema nào đổi; KHÔNG Module Taxonomy/dependency graph nào đổi
  (`module-registry.yaml` KHÔNG chạm, cấm tường minh tại transaction
  này); KHÔNG Governance/Approval process nào đổi (Chapter 12, KHÔNG
  chạm); KHÔNG supersede ADR Locked nào (KHÔNG ADR nào hiện có về
  coverage-measurement tooling); ">1 module HOẶC khó đảo ngược" — vế
  ">1 module" đọc theo đúng tiền lệ `ADR-030` LÀ cho quyết định
  baseline-existence/tạo authority cross-module MỚI (CI/CD's câu hỏi
  "có nên có MỘT baseline chung bắt buộc"), KHÔNG PHẢI cho việc chọn
  một tool CỤ THỂ bên trong một category ĐÃ pre-authorized từ trước (nếu
  đọc ngược lại, MỌI amendment tương lai cho naming.md/coding-
  standard.md/logging.md/config.md/error-handling.md/chính testing.md —
  tất cả đều áp dụng xuyên >1 module theo bản chất Engineering
  Foundation — sẽ ĐỀU tự động cần ADR, mâu thuẫn trực tiếp với
  `ADR_NOT_REQUIRED` đã ghi nhận quán xuyên suốt lịch sử approval của
  chính các category đó); vế "khó đảo ngược" — candidate KHÔNG có
  hard-to-reverse lock-in (dev/test-time-only Go CLI, BSD-2-Clause,
  KHÔNG vendor/infrastructure coupling, đổi sang candidate khác chỉ đổi
  command được invoke, KHÔNG đổi schema/infrastructure) — khác hẳn loại
  rủi ro "CI provider lock-in" mà chính `ADR-030` §6 cảnh báo riêng cho
  CI/CD provider selection. Kết luận: `ADR_NOT_REQUIRED`, KHÔNG author
  ADR tại transaction này.

KHÔNG tại transaction này (candidate-only, tường minh):
  - KHÔNG cài đặt/`go install` gobco (hay bất kỳ tool nào) vào bất kỳ
    module Go nào trong repository.
  - KHÔNG thêm `go.sum`/`go.mod` dependency nào.
  - KHÔNG tạo/sửa CI workflow (`ci-cd.md`/`ADR-030` authority riêng,
    KHÔNG chạm).
  - KHÔNG rerun/reinterpret market-reference-service Quality Gate nào —
    overall QG VẪN `FAIL — evidence` cho tới khi một formal
    re-evaluation thật thực thi SAU KHI branch coverage thật đo được.
  - KHÔNG đổi Chapter 13 coverage floor/tier/pass-fail semantics.
  - KHÔNG approve module/Data Layer/Phase nào. KHÔNG authorize LIVE.
  Chọn/pin/cài đặt chính thức mechanism này (hoặc bất kỳ candidate
  khác xuất hiện sau) LÀ một transaction riêng biệt tương lai — PHẢI
  tự verify trực tiếp lại toàn bộ 10 tiêu chí trên TẠI thời điểm đó
  (candidate landscape/maintenance status CÓ THỂ đổi), VÀ tự rerun ADR
  Scope Rule nếu bất kỳ fact nền tảng nào ở trên đổi.
```

## Non-goals (KHÔNG chọn/redefine tại v0.1 này)

```text
coverage/tier policy (Chapter 13 §13.3/§13.4);
parity semantics (I-2, Chapter 13 §13.2);
determinism/reproducibility substance (I-2/I-3/I-12, Chapter 5, Chapter
  13 §13.2);
quality-gate pass/fail policy (Chapter 13 §13.8/§13.9);
module criticality (Chapter 7 §7.5, `module-registry.yaml`);
domain semantics mới (`/docs/domain/`);
CI/CD pipeline design (category riêng, chưa mở);
concrete test framework/vendor selection (§"Framework/tool selection");
performance benchmark policy vượt ngoài existing authority (Chapter 13
  §13.7, KHÔNG đổi);
security architecture change (`ADR-017`, KHÔNG đổi).
```

## ADR-scope disposition

```text
Tài liệu này (`testing.md` v0.1) KHÔNG author dưới authority một ADR
  riêng — [Chapter 3 §3.2](../constitution/03-engineering-principles.md)
  (Locked v1.4) ĐÃ established sẵn: (1) CÓ một Testing Convention
  category; (2) scope GIỚI HẠN style/tooling; (3) coverage/tier
  requirement thuộc Chapter 13 (Locked), KHÔNG định nghĩa lại. ADR
  Scope Check (transaction riêng biệt, trước tài liệu này) kết luận
  `ADR_NOT_REQUIRED` — verify trực tiếp KHÔNG existing authority nào
  khác superseded kết luận đó tại chính transaction này.
Mọi mục §1–§16 trên CHỈ implement chi tiết reversible dưới boundary ĐÃ
  Locked — KHÔNG mục nào tạo architecture responsibility mới, Platform
  Invariant mới, quality-gate policy mới, coverage/tier semantic mới,
  module ownership/criticality mapping mới, hay published contract mới.
  KHÔNG tạo ADR-030 tại transaction này.
Mọi thay đổi SEMANTIC tương lai vào tài liệu này (KHÔNG PHẢI mọi sửa —
  CHỈ khi đổi Ý NGHĨA rule) PHẢI tự chạy lại ADR Scope Rule (Chapter 0
  §4b) hiện hành TẠI chính thời điểm đổi — KHÔNG suy diễn "reversible/
  refactor-class" LÀ đủ để miễn ADR nếu thay đổi đó THẬT SỰ vượt ngoài
  boundary Chapter 3 §3.2 đã pin (vd một đề xuất thay đổi coverage
  threshold hay tier assignment tại đây SẼ là một Chapter 13 conflict,
  KHÔNG PHẢI reversible detail, PHẢI stop VÀ report gap, KHÔNG tự
  quyết ở testing.md).
```

## Change history

```text
v0.1  2026-08-12  Established — vai trò: `Phase 1.5 Testing Convention
      v0.1 Authoring Executor`. Bounded EF-TXN-002 category transaction
      (Testing only), authored TRỰC TIẾP dưới [Chapter 3
      §3.2](../constitution/03-engineering-principles.md) (Locked) —
      KHÔNG ADR (ADR Scope Check transaction riêng biệt trước kết luận
      `ADR_NOT_REQUIRED`, KHÔNG tạo ADR-030). Verify trực tiếp trước
      khi author: current HEAD
      (2fe84d04705d3f74f6a128f3f919d45608582376),
      `docs/engineering/testing.md` KHÔNG tồn tại trước đây, KHÔNG
      Testing ADR nào tồn tại, KHÔNG concrete test framework/tool nào
      đã pin (KHÔNG dependency manifest nào trong `python/`/`go/`).
      Established 18 mục: test structure (predictable, KHÔNG redesign
      monorepo topology), test naming (semantic behavior, align
      naming.md), test isolation (order-independence, no hidden shared
      state, cleanup, KHÔNG redefine Chapter 13 determinism substance),
      deterministic test mechanics (injectable clock, seeded
      randomness, KHÔNG platform determinism rule mới), fixtures/
      factories (explicit default, visible override, domain fixture
      VẪN hợp lệ dưới Domain Contract), mocking/stubbing (mock boundary
      KHÔNG PHẢI behavior under test, KHÔNG coverage inflation, align
      Chapter 13 anti-gaming), unit vs integration (engineering-style
      distinction, KHÔNG gán tier/count), contract/boundary testing
      (verify mechanics, KHÔNG redefine contract), Python guidance
      (idiomatic, framework deferred), Go guidance (idiomatic, `testing`
      standard library đủ, framework thứ ba deferred), test data (nhỏ/
      deterministic/seeded, KHÔNG production sensitive data trừ khi
      security authority cho phép, golden data PHẢI meaningful),
      flaky-test tooling mechanics (implement Chapter 13 §13.10's
      explicit-deferred tooling, KHÔNG redefine policy), local test
      commands (predictable entry point, KHÔNG hardcode tool chưa
      chọn), reusable helpers (giảm duplication, KHÔNG che assertion,
      KHÔNG domain semantics cạnh tranh), error assertions (align
      error-handling.md, semantic category over raw string, KHÔNG
      error-code schema mới), logging/config interaction (verify được,
      KHÔNG redefine), coverage boundary (Chapter 13 CHỈ sở hữu, KHÔNG
      copy số ngưỡng), quality-gate boundary (Chapter 13 CHỈ sở hữu
      eligibility/evidence/tier/pass-fail). Framework/tool selection
      VẪN deferred (verify trực tiếp KHÔNG authority nào đã chọn).
      Non-goals liệt kê tường minh. ADR-scope disposition: v0.1
      implement detail dưới Chapter 3 §3.2 đã Locked, KHÔNG tạo
      ADR-030. KHÔNG chạm Chapter 3/Chapter 13 (Locked)/`ADR-008`/
      `ADR-017`/`ADR-024`/`monorepo.md`/`ADR-025`/`coding-standard.md`/
      `ADR-026`/`naming.md`/`ADR-027`/`logging.md`/`ADR-028`/
      `config.md`/`ADR-029`/`error-handling.md`/`module-registry.yaml`/
      Domain Contract/Constitution/Phase 1.5 rules. `EF-CONFIG-B-MIN-01`
      VÀ `EF-ERR-B-MIN-01` KHÔNG chạm, KHÔNG đóng. KHÔNG bắt đầu CI/CD.
      `status: Draft` — not self-approved (`G-ORCH-002`). KHÔNG
      authorize Phase 2/LIVE.
v0.2  2026-08-12  Bounded correction, đóng `EF-TEST-A-MAJ-01`/
      `EF-TEST-A-MIN-01`. `EF-TEST-A-MAJ-01`: §4 v0.1 mandate module
      "cung cấp clock qua dependency injection/parameter" — vượt ngoài
      Chapter 3 §3.2's style/tooling boundary vì buộc một production-
      code API/design change. Sửa: Testing Convention CHỈ định nghĩa
      CÁCH dùng/control một seam (clock abstraction/parameter/fake
      adapter/harness) ĐÃ tồn tại, KHÔNG BAO GIỜ bắt buộc tạo MỚI một
      DI pattern/parameter/interface/dependency production CHỈ để thỏa
      convention; khi KHÔNG seam nào khả dụng, đó LÀ một implementation/
      design gap — report VÀ route qua authority sở hữu production
      design, tự rerun ADR Scope Rule nếu applicable, KHÔNG tự giải
      quyết tại `testing.md`. `EF-TEST-A-MIN-01`: §17 v0.1 tuyên bố
      "KHÔNG copy lại con số ngưỡng cụ thể" NHƯNG ngay sau đó liệt kê
      chính các con số đó (Tier 0 ≥ 95%/Tier 1 ≥ 90%/Tier 2 ≥ 80%/
      Tier 3 ≥ 60%) — tự mâu thuẫn. Sửa: bỏ hẳn con số, CHỈ giữ nguyên
      tắc "Chapter 13 §13.3/§13.4 LÀ authority DUY NHẤT," người đọc
      PHẢI resolve giá trị hiện hành trực tiếp từ Chapter 13. **KHÔNG
      đổi:** `ADR_NOT_REQUIRED` result, Chapter 3/Chapter 13 boundary,
      §1 (test structure), §2 (naming), §3 phần còn lại (isolation),
      §5 (fixtures/factories), §6 (mocking/stubbing), §7 (unit/
      integration), §8 (contract/boundary testing), §9 (Python
      guidance), §10 (Go guidance), §11 (test data), §12 (flaky-test
      tooling mechanics), §13 (local commands), §14 (reusable
      helpers), §15 (Error Handling interaction), §16 (Logging/Config
      interaction), §18 (quality-gate boundary), Framework/tool
      selection (VẪN deferred), Non-goals. KHÔNG tạo ADR-030, KHÔNG
      chọn framework/vendor, KHÔNG introduce production DI
      architecture, KHÔNG chạm Chapter 3/Chapter 13 (Locked)/bất kỳ
      Approved ADR/convention nào. `EF-CONFIG-B-MIN-01`/
      `EF-ERR-B-MIN-01` KHÔNG chạm. `status` VẪN `Draft` — not
      self-approved (`G-ORCH-002`), KHÔNG authorize Phase 2/LIVE.
ACCEPTANCE  2026-08-12  Product Owner lifecycle approval — mechanical,
      vai trò: `Testing Convention v0.2 Mechanical Approval Recorder`.
      Quyết định: "APPROVE TESTING CONVENTION V0.2." Reviewed
      candidate: v0.2, blob 0a325665f5ed011a7439fb8d3c349c3db79d50fa
      (bounded Review A re-review CLEAN, New Blocker/Major/Minor
      0/0/0, đóng `EF-TEST-A-MAJ-01`/`EF-TEST-A-MIN-01`; Independent
      Review B: New Blocker 0/New Major 0/New Minor 0,
      `ADR_NOT_REQUIRED` CONFIRMED, `READY_FOR_PRODUCT_OWNER_
      DECISION`). `status: Draft -> Approved`, `approved_by: null ->
      Product Owner`, `approved_at: null -> "2026-08-12"`. `version`
      KHÔNG bump (pure mechanical lifecycle approval) — VẪN `0.2`.
      KHÔNG semantic content nào đổi (§1–§18 byte-equivalent ngoài
      banner/lifecycle metadata/change history này). Tài liệu VẪN LÀ
      living document — `Approved` KHÔNG immutable byte-for-byte như
      ADR; `ADR_NOT_REQUIRED` VẪN đúng (tài liệu này KHÔNG dưới
      authority một ADR nào); thay đổi SEMANTIC tương lai VẪN PHẢI tự
      rerun ADR Scope Rule. Stale editorial/provenance reference tới
      v0.1 (nếu có) KHÔNG sửa tại transaction này. KHÔNG chạm Chapter
      3/Chapter 13 (Locked)/`ADR-008`/`ADR-017`/`ADR-024`/
      `monorepo.md`/`ADR-025`/`coding-standard.md`/`ADR-026`/
      `naming.md`/`ADR-027`/`logging.md`/`ADR-028`/`config.md`/
      `ADR-029`/`error-handling.md`/`module-registry.yaml`/Domain
      Contract/Constitution/Phase 1.5 rules, KHÔNG tạo ADR-030, KHÔNG
      chọn framework/vendor, KHÔNG introduce production DI/API
      architecture, KHÔNG đóng `EF-CONFIG-B-MIN-01`/`EF-ERR-B-MIN-01`,
      KHÔNG mở CI/CD, KHÔNG authorize Phase 2/LIVE.
v0.3  2026-08-20  CANDIDATE amendment, KHÔNG self-approved — vai trò:
      `Go Branch-Coverage Mechanism Candidate Author`. `status: Approved
      → Draft`, `version: "0.2" → "0.3"`, `approved_by`/`approved_at`
      reset `null` (v0.2's approval record giữ nguyên nguyên vẹn phía
      trên LÀM historical evidence, KHÔNG bị ghi đè/rewrite). Bổ sung
      MỘT subsection MỚI dưới "Framework/tool selection": "Go branch-
      coverage mechanism — CANDIDATE," đề xuất **gobco**
      (github.com/rillig/gobco) LÀM candidate mechanism cho gap evidence
      DUY NHẤT còn lại trên market-reference-service's Chapter 13
      Quality Gate (branch coverage — line coverage VÀ I-13 property-
      based evidence đã có, `P3-MR-QG-A-MAJ-01`). Đánh giá đầy đủ 10
      tiêu chí (maintained status, đo branch thật KHÔNG statement/block
      proxy, Go version compat, reproducibility, pin exact identity,
      local/CI execution, evidence-format sufficiency, anti-gaming/
      authoritative-implementation compliance qua temp-dir source-to-
      source instrumentation KHÔNG sửa file gốc, license/dependency
      impact, KHÔNG alternative nào làm yếu branch metric) — verify
      trực tiếp GitHub repo/README/main.go/pkg.go.dev VÀ golang/go#70306
      (native branch-coverage proposal VẪN Open/Incoming, KHÔNG ETA),
      KHÔNG từ memory. Từ chối tường minh mọi statement/block proxy đã
      khảo sát (`go tool cover`/`covdata`, `gocov`, `go-carpet`,
      `go-test-coverage`, `goc`, `Courtney`, "gocov-branch" không tồn
      tại LÀM project riêng). ADR-scope check (chạy TRƯỚC khi author):
      `ADR_NOT_REQUIRED` — [Chapter 13 §13.3](../constitution/13-quality-gates.md)/[§13.14](../constitution/13-quality-gates.md)
      (Locked) tự defer "concrete tooling" cho Chapter 3 §3.2; Chapter 3
      §3.2 dòng 44 (Locked v1.4) ĐÃ có carve-out tường minh cho Testing
      Convention's "style/tooling" scope — pattern (b) `docs/adr/
      ADR-030.md` §1 Context tự mô tả (existing Locked authority ĐÃ
      pre-resolve baseline-existence + scope boundary → living
      convention author trực tiếp, KHÔNG ADR), KHÁC pattern (a) ADR-030
      phải dùng cho CI/CD (KHÔNG carve-out tương tự tồn tại). KHÔNG
      Platform Invariant/Event Schema/Module Taxonomy/Governance-process
      nào đổi, KHÔNG supersede ADR Locked nào, KHÔNG hard-to-reverse
      lock-in (dev/test-time-only CLI, BSD-2-Clause). Vế ">1 module"
      đọc theo tiền lệ ADR-030 LÀ cho baseline-existence decision MỚI,
      KHÔNG PHẢI cho chọn tool bên trong category ĐÃ pre-authorized —
      nếu không, mọi amendment tương lai cho bất kỳ Engineering
      Foundation convention nào cũng sẽ tự động cần ADR, mâu thuẫn trực
      tiếp lịch sử approval `ADR_NOT_REQUIRED` nhất quán của chính các
      category đó. **KHÔNG cài đặt/tích hợp gobco (hay bất kỳ tool nào)
      tại transaction này** — KHÔNG `go install`, KHÔNG `go.mod`/
      `go.sum` dependency mới, KHÔNG CI workflow, KHÔNG rerun/
      reinterpret Quality Gate nào (overall QG VẪN `FAIL — evidence`).
      **KHÔNG đổi:** Chapter 13 coverage floor/tier/pass-fail semantics
      nào, `module-registry.yaml`, dependency graph, production/test
      code, `ci-cd.md`/`ADR-030` boundary, §1–§16/§18/Non-goals/
      ADR-scope disposition gốc (byte-equivalent ngoài banner/lifecycle
      metadata/change history này), Framework/tool selection's general
      deferral (pytest/testify/gomock VẪN deferred). KHÔNG tạo ADR mới.
      KHÔNG approve module/Data Layer/Phase nào. KHÔNG authorize LIVE.
      `status` = `Draft` — not self-approved (`G-ORCH-002`), chờ Product
      Owner review/decision (chấp nhận candidate, chọn candidate khác,
      hoặc yêu cầu re-khảo sát).
```
