---
id: engineering-testing
title: "Engineering Foundation — Testing Convention"
version: "0.1"
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

**Vai trò của tài liệu này:** convention document THỨ BẢY của Phase 1.5 — Engineering Foundation (Chapter 3 §3.2), phạm vi CHỈ category **Testing** (Chapter 14 §14.2's Phase 1.5 scope list) — đúng `EF-TXN-002` (một category = một transaction bounded). **KHÔNG author dưới authority một ADR mới** — ADR Scope Check (transaction riêng biệt trước) đã kết luận `ADR_NOT_REQUIRED`: [Chapter 3 §3.2](../constitution/03-engineering-principles.md) (Locked v1.4) ĐÃ established sẵn cả hai phần quyết định baseline-existence — (1) CÓ một Testing Convention category trong Engineering Foundation, VÀ (2) scope của nó GIỚI HẠN style/tooling (framework, cấu trúc test file, naming test case), coverage/tier requirement ĐÃ có đầy đủ tại [Chapter 13](../constitution/13-quality-gates.md) (Locked), KHÔNG định nghĩa lại. Tài liệu này CHỈ implement chi tiết reversible dưới boundary ĐÃ Locked đó — KHÔNG lặp lại/redefine bất kỳ Chapter 13 substance nào.

**Nguyên tắc chi phối (Chapter 3 §3.2 + Chapter 13 §13.2, tái khẳng định KHÔNG redefine):** Testing Convention CHỈ quản lý style/tooling — test structure, naming, isolation mechanics, fixture/mocking guidance, ngôn ngữ idiom, local command convention, flaky-test tooling mechanics. Chapter 13 VẪN authority DUY NHẤT cho coverage percentage/tier, tier resolution, parity substance (I-2), determinism/reproducibility substance (I-2/I-3/I-12, Chapter 5), quality-gate pass/fail semantics, immutable gate evidence contract, flaky-test POLICY (§13.10), module criticality (Chapter 7 §7.5). Tài liệu này KHÔNG tạo domain/architecture acceptance semantics mới.

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
Style/tooling guidance (KHÔNG tạo platform determinism rule mới, CHỈ
  hỗ trợ test tuân thủ determinism substance ĐÃ có, §13.2):
  injectable/fake clock — module cung cấp clock qua dependency
    injection/parameter khi cần test time-dependent logic, KHÔNG gọi
    trực tiếp system clock không kiểm soát được trong test;
  seeded randomness — mọi randomness dùng trong test PHẢI seeded rõ
    ràng, kết quả reproducible;
  deterministic fixture (§5 dưới) — dữ liệu input cố định, KHÔNG sinh
    ngẫu nhiên không seed;
  explicit event-time input — khi domain logic phụ thuộc effective-
    time/event-time (Chapter 5 Time Model, KHÔNG đổi), test PHẢI cung
    cấp giá trị đó explicit, KHÔNG suy diễn từ thời điểm chạy test;
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
Testing Convention KHÔNG sở hữu coverage threshold nào — Chapter 13
  (`13-quality-gates.md`, Locked) LÀ authority DUY NHẤT cho coverage
  percentage/floor VÀ tier mapping (§13.3/§13.4). Tài liệu này KHÔNG
  copy lại con số ngưỡng cụ thể (Tier 0 ≥ 95%/Tier 1 ≥ 90%/Tier 2 ≥
  80%/Tier 3 ≥ 60%, §13.3) để tránh tạo một "bản sao" số liệu dễ lệch
  khỏi Chapter 13 gốc theo thời gian (I-12 Single Source of Truth) —
  khi cần tham chiếu, PHẢI trỏ trực tiếp tới `13-quality-gates.md`
  §13.3/§13.4, KHÔNG lặp lại số cụ thể tại đây. Tài liệu này KHÔNG tạo
  một coverage policy thay thế nào.
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
```
