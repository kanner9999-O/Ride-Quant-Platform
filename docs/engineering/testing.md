---
id: engineering-testing
title: "Engineering Foundation — Testing Convention"
version: "0.5"
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

**CANDIDATE (2026-08-28), KHÔNG self-approved — status: Approved → Draft.** `status: Approved → Draft` (mọi thay đổi SEMANTIC vào tài liệu Approved bắt buộc tăng version VÀ đi qua approval gate lại, đúng [Chapter 0 §5.1](../constitution/00-governance.md); `approved_by`/`approved_at` của v0.4 KHÔNG tự động phủ nội dung MỚI này — reset `null`, v0.4's approval record giữ nguyên nguyên vẹn phía dưới LÀM historical evidence, KHÔNG bị ghi đè), vai trò: `Python QG Coverage Mechanism Candidate Author`. Bổ sung MỘT subsection MỚI dưới "Framework/tool selection" (dưới, cùng vị trí Go branch-coverage candidate) đề xuất một **CANDIDATE** (chưa chọn/chưa cài đặt/chưa tích hợp) cho cơ chế đo **Python line coverage VÀ branch coverage** — khoảng trống evidence được xác nhận tại `feature-engine`'s formal Chapter 13 Quality Gate (`P3-FEATURE-QG-EVID-01`/`P3-FEATURE-QG-EVID-02`, `docs/MANIFEST.md`). **ADR-scope check (chạy TRƯỚC KHI author, [Chapter 0 §4b](../constitution/00-governance.md)):** kết luận `ADR_NOT_REQUIRED` — xem "Python line+branch coverage mechanism — CANDIDATE" dưới cho full reasoning, cùng pattern (b) đã dùng cho `testing.md`'s own v0.1 baseline VÀ cho v0.3's Go branch-coverage candidate: [Chapter 3 §3.2](../constitution/03-engineering-principles.md) đã có carve-out tường minh cho Testing Convention tooling, VÀ [Chapter 13 §13.3](../constitution/13-quality-gates.md)/[§13.14](../constitution/13-quality-gates.md) tự nó khóa "không khóa tool/vendor cụ thể... defer Engineering Foundation." Đây CHỈ LÀ candidate selection trong phạm vi "tooling" ĐÃ pre-authorized, KHÔNG PHẢI một baseline-existence decision mới, KHÔNG platform invariant/event schema/module taxonomy/governance-process change, KHÔNG supersede ADR đã Locked nào, KHÔNG hard-to-reverse lock-in (dev/test-time-only Python package, Apache-2.0, zero additional runtime dependency tại Python >=3.13 — verify trực tiếp PyPI metadata dưới). **KHÔNG đổi:** Chapter 13 coverage floor/tier/pass-fail semantics nào (§17/§18 dưới, KHÔNG đổi), `module-registry.yaml`, dependency graph, `feature-engine` production/test code, `P3-FEATURE-QG-EVID-01`/`-EVID-02` (KHÔNG closed/remediated tại đây — Feature formal QG VẪN `FAIL — evidence`), the existing Go branch-coverage mechanism/history (gobco candidate, `P3-GOBC-A-MAJ-01` closure) — byte-equivalent, KHÔNG re-opened, KHÔNG normalized into a cross-language "same tool" claim. KHÔNG cài đặt/pin tool nào tại transaction này. KHÔNG đo Feature Engine coverage. KHÔNG rerun Quality Gate nào. KHÔNG approve module/Data Layer nào. KHÔNG authorize LIVE. KHÔNG start Context Aggregator.

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

**v0.4 — bounded correction (2026-08-20), đóng `P3-GOBC-A-MAJ-01`, vai trò: `Go Branch-Coverage Candidate Bounded Correction Executor`.** v0.3's "Go branch-coverage mechanism — CANDIDATE" subsection conflated gobco's DEFAULT **condition coverage** mode (atomic boolean sub-expression true/false tracking — decomposes `&&`/`||`/`!` into independent operands) với gobco's distinct, explicit **`-branch`** flag mode (instruments CHỈ whole controlling condition của `if`/`switch`/`for`, KHÔNG decompose) — verify trực tiếp `instrumenter.go`'s `markConds` function (branch mode: `break` cho `UnaryExpr`/`BinaryExpr` case, KHÔNG unwrap negation/`&&`/`||`; condition mode: xóa `n` khỏi marked set, thêm operand(s) — `n.X` cho NOT, `n.X` VÀ `n.Y` cho LAND/LOR) VÀ code comment tự nó xác nhận: "In condition coverage mode (the default mode), only atomic boolean conditions are marked... In branch coverage mode, only the whole controlling condition is instrumented." v0.3 mô tả đúng cơ chế instrumentation (per-atomic-condition true/false, ví dụ output "Condition coverage: N/M") NHƯNG coi kết quả ĐÓ LÀ đủ cho Chapter 13's branch metric — SAI. Condition coverage KHÔNG suy ra được branch coverage cho compound condition: phản ví dụ trực tiếp — `if (a || b)` với 2 test case (a=T,b=F → whole=True; a=F,b=T → whole=True) đạt 100% atomic condition coverage (a cả T/F, b cả T/F) NHƯNG whole-expression KHÔNG BAO GIỜ đánh giá `False` — branch coverage CHỈ 50%. Hai metric ĐỘC LẬP, KHÔNG metric nào tự động suy ra metric kia. **Sửa (§"Go branch-coverage mechanism — CANDIDATE" dưới):** (1) proposed Chapter-13 mechanism LÀ gobco chạy VỚI `-branch` flag rõ ràng (KHÔNG default invocation); (2) condition coverage VÀ branch coverage LÀ hai metric tách biệt, KHÔNG thay thế cho nhau; (3) default condition-mode output TUYỆT ĐỐI KHÔNG được substitute LÀM Chapter-13 branch metric; (4) Chapter 13's branch floor CHỈ consume verified branch-mode (`-branch=true`) result; (5) transaction cài đặt/pin tương lai PHẢI verify trực tiếp: exact command (`gobco -branch`, cú pháp chính xác), tool version/content identity, branch-mode numerator/denominator semantics, output format (`printOutput()` đổi label thành "Branch coverage: N/M" khi `-branch=true`, verify trực tiếp lại tại thời điểm cài đặt — README hiện KHÔNG document flag này, CHỈ tồn tại trong source/flag definition, một install-time verification gap tường minh), exit-code semantics, VÀ reproducibility đối với go1.26.6/go.mod `go 1.25` hiện hành của repository — TRƯỚC KHI tool trở thành accepted evidence machinery. **Limitation review (verify trực tiếp `instrumenter.go`, KHÔNG đoán):** instrumenter xử lý `IfStmt`, `SwitchStmt` (cả expression VÀ type-switch variant), `ForStmt` condition — KHÔNG evidence nào cho `SelectStmt` handling trong cả hai mode (xác nhận lại README's tuyên bố "doesn't cover select statements," ĐÚNG cho cả branch mode). Verify trực tiếp market-reference-service's authoritative implementation hiện tại (`grep -rn "select {" go/market-reference-service`): **KHÔNG `select` statement nào tồn tại** trong subject hiện tại — unsupported construct này KHÔNG ảnh hưởng branch applicability/evidence completeness cho `market-reference-service` TẠI boundary hiện hành. Go-generics parsing support của chính gobco's AST-based instrumenter KHÔNG verify được rõ ràng từ documentation/source đã khảo sát tại transaction này (verify trực tiếp `grep -rnE` cho type-parameter syntax trong market-reference-service: **KHÔNG generic type parameter nào tồn tại** trong subject hiện tại, nên đây LÀ moot cho subject hiện tại — NHƯNG gobco's own generics support VẪN unresolved LÀ một fact chưa xác định được sạch sẽ) — ghi nhận LÀM **installation-time fail-closed verification requirement**: bất kỳ transaction cài đặt/pin tương lai nào, HOẶC bất kỳ thay đổi tương lai nào đưa `select` statement/generic type parameter vào market-reference-service (hay bất kỳ subject Go nào khác dự định dùng gobco), PHẢI tự verify lại trực tiếp gobco's generics/select support TRƯỚC KHI chấp nhận branch-mode result LÀM evidence — KHÔNG giả định support, KHÔNG tự waiver gap này. **KHÔNG đổi:** `ADR_NOT_REQUIRED` (correction này KHÔNG phát hiện §4b trigger mới nào — vẫn CHỈ LÀ làm rõ invocation-mode/limitation detail bên trong CÙNG một candidate tooling category ĐÃ pre-authorized, KHÔNG platform invariant/event schema/module taxonomy/governance-process/hard-to-reverse mới), `testing.md` `version: "0.3"` gốc's decision KHÔNG bị đảo ngược (gobco VẪN LÀ candidate, CHỈ invocation mode được làm rõ), `status` VẪN `Draft` (not self-approved, `G-ORCH-002`), Chapter 13 KHÔNG chạm, KHÔNG cài đặt tool, KHÔNG `go.mod`/`go.sum`, KHÔNG CI integration, QG VẪN `FAIL — evidence`, LIVE VẪN `NOT_AUTHORIZED`, §1–§16/§18/Non-goals/ADR-scope disposition gốc/Framework-selection general deferral KHÔNG chạm.

**v0.4 APPROVAL — mechanical (2026-08-20T09:22:00+07:00), vai trò: `Testing Convention v0.4 Mechanical Approval Recorder`.** Product Owner decision: **"APPROVE TESTING CONVENTION V0.4"** (decision time `2026-08-20T09:22:00+07:00`). Reviewed immutable boundary: HEAD `2d4f7a7497873050b2da9defee0f91fa03d5613e`, blob `269ecaa0c6ee4780a81de0b8d18b9a98c2b136a7`. `status: Draft → Approved`, `version: "0.4"` KHÔNG đổi (pure mechanical lifecycle approval — KHÔNG bump), `approved_by: Product Owner`, `approved_at: "2026-08-20"`. **Review evidence tại approval này:** Review A — COMPLETE/ELIGIBLE/CLEAN, đóng `P3-GOBC-A-MAJ-01`, Blocker 0/Major 0/Minor 0, `ADR_NOT_REQUIRED` confirmed. Independent Review B — COMPLETE/ELIGIBLE/CLEAN, Mode B (`SAME_PRINCIPAL_DISTINCT_EXECUTION`), execution reference `P3-GOBC-B-2d4f7a7-20260820T0904+0700`, isolation attestation SATISFIED, Blocker 0/Major 0/Minor 0, `ADR_NOT_REQUIRED` confirmed, `READY_FOR_PRODUCT_OWNER_DECISION`. Independent-review requirement: SATISFIED (đúng Chapter 11 §11.5 tối thiểu hai reviewer identity độc lập, áp dụng tương tự cho Testing Convention approval). **KHÔNG semantic content nào đổi tại approval này** (§1–§18/Framework-tool-selection/"Go branch-coverage mechanism — CANDIDATE" subsection/Non-goals/ADR-scope disposition/tất cả v0.2–v0.4 banner phía trên byte-equivalent ngoài chính banner approval này VÀ frontmatter lifecycle field) — gobco VẪN LÀ candidate mechanism được chọn; required invocation mode VẪN LÀ `-branch` rõ ràng; condition coverage VÀ branch coverage VẪN LÀ hai metric tách biệt, KHÔNG thay thế cho nhau; default gobco condition mode VẪN KHÔNG thỏa Chapter 13 branch metric; CHỈ verified branch-mode evidence mới được chấp nhận cho branch metric; installation/pinning tương lai VẪN PHẢI verify trực tiếp exact tool version/content identity, exact command syntax, numerator/denominator semantics, output format, exit semantics, compatibility/reproducibility TRƯỚC KHI trở thành accepted evidence machinery; `SelectStmt` limitation VẪN disclosed; current market-reference-service applicability (KHÔNG `select`/generic nào trong subject hiện tại) VẪN KHÔNG đổi; gobco's generics compatibility VẪN fail-closed/unresolved cho tới installation-time verification; Chapter 13 VẪN authority DUY NHẤT cho coverage floor/QG semantics; `ADR_NOT_REQUIRED` VẪN đúng KHÔNG đổi. **Approval này KHÔNG:** cài đặt gobco, thêm `go.mod`/`go.sum`/tool binary nào, tạo CI workflow, đổi gobco invocation semantics, chạm Chapter 13/coverage floor/`module-registry.yaml`/dependency graph/implementation/test code/`ADR-032`/Domain Contract, rerun Quality Gate, claim QG PASS, approve `market-reference-service`/Data Layer, authorize LIVE. `market-reference-service` Chapter 13 QG VẪN `FAIL — evidence` (branch coverage vẫn chưa đo được — approval này CHỈ approve chính testing.md's candidate/lifecycle content, KHÔNG tự động resolve gap evidence đó). Tài liệu VẪN LÀ living document — `Approved` KHÔNG immutable byte-for-byte như ADR; `ADR_NOT_REQUIRED` VẪN đúng (tài liệu KHÔNG dưới authority một ADR nào); thay đổi SEMANTIC tương lai VẪN PHẢI tự rerun ADR Scope Rule.

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
  2. [v0.4 sửa, đóng `P3-GOBC-A-MAJ-01`: v0.3 mô tả CHỈ default mode
     rồi coi đủ cho branch floor — SAI, xem banner correction phía
     trên cho full reasoning VÀ phản ví dụ.] gobco đo HAI metric TÁCH
     BIỆT, verify trực tiếp `instrumenter.go`'s `markConds` function —
     KHÔNG được dùng thay thế cho nhau:
       - **Condition coverage (default, `-branch=false`)** — decompose
         `&&`/`||`/`!` thành operand nguyên tử độc lập, track riêng mỗi
         atomic boolean sub-expression `true`/`false`. Đây LÀ metric
         gần với condition/MC-DC-style coverage — Chapter 13 §13.3 liệt
         kê "Condition/MC-DC coverage LÀ tùy chọn theo tier, KHÔNG tính
         vào floor bắt buộc." KHÔNG được dùng LÀM Chapter-13 branch
         metric.
       - **Branch coverage (`-branch=true`, cờ có thật, verify trực
         tiếp code — `flags.BoolVar(&g.branch, "branch", false, "cover
         branches, not conditions")`)** — CHỈ instrument whole
         controlling condition của `IfStmt`/`SwitchStmt`/`ForStmt`
         (source comment tự xác nhận: "In branch coverage mode, only
         the whole controlling condition is instrumented") — đây MỚI
         LÀ metric Chapter 13 §13.3 yêu cầu (đã evaluate cả `true` LẪN
         `false` của CHÍNH nhánh quyết định).
     Condition coverage KHÔNG suy ra branch coverage cho compound
     condition — phản ví dụ trực tiếp: `if (a || b)` với 2 test case
     (a=T,b=F → whole=`True`; a=F,b=T → whole=`True`) đạt 100% atomic
     condition coverage (a cả T/F, b cả T/F) NHƯNG whole-expression
     KHÔNG BAO GIỜ đánh giá `False` — branch coverage CHỈ 50%.
     **Mechanism được đề xuất chính xác cho Chapter 13: gobco chạy VỚI
     `-branch` flag** (KHÔNG default invocation). README hiện tại
     (verify trực tiếp) KHÔNG document flag này — CHỈ tồn tại trong
     source (`main.go` flag definition) — một install-time verification
     gap tường minh, ghi nhận tại điểm 3/6 dưới, KHÔNG che giấu.
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
  6. Local execution/tương lai CI: chạy `gobco -branch` CLI trực tiếp
     trong package directory (KHÔNG default invocation, đúng điểm 2 đã
     sửa) — instrument VÀO một temp directory riêng
     (`os.TempDir()/gobco-<random>`, copy package source sang đó), gọi
     `go test` THẬT trên bản copy đã instrument, KHÔNG sửa file gốc
     trong repository — local execution NGAY tại transaction cài đặt
     tương lai; CI suitability hợp lý (CLI đơn, exit-code/text output,
     KHÔNG cần service ngoài) nhưng KHÔNG quyết định CI integration tại
     đây (`ci-cd.md`/`ADR-030` authority riêng, KHÔNG chạm). [v0.4 sửa:
     exact flag syntax/spelling PHẢI verify trực tiếp lại (`gobco
     -help`) TẠI transaction cài đặt tương lai, vì README hiện tại
     KHÔNG document `-branch` — chỉ verify được từ source tại
     candidate transaction này.]
  7. Output format cho Chapter 13 immutable evidence: [v0.4 sửa] khi
     chạy VỚI `-branch`, `printOutput()` (verify trực tiếp source) đổi
     summary label từ "Condition coverage" thành **"Branch coverage:
     N/M"** — evidence entry PHẢI pin rõ label/mode ĐÃ dùng (`-branch`
     hay default) cùng với N/M, KHÔNG CHỈ con số trần, để tránh chính
     defect `P3-GOBC-A-MAJ-01` vừa sửa lặp lại tại evidence thật; danh
     sách từng controlling-condition chưa đạt (file/line/column/lần
     true/lần false) đủ chi tiết pin vào evidence entry (§13.9: subject
     identity, boundary, input identity) giống format `go tool cover
     -func` hiện đang dùng cho line coverage evidence — exact output
     format dưới `-branch` mode (có giữ cùng cấu trúc chi tiết như
     default mode hay không) PHẢI verify trực tiếp lại TẠI transaction
     cài đặt tương lai, KHÔNG giả định giống hệt default mode tại
     candidate này.
  11. **Limitation review (v0.4 bổ sung, verify trực tiếp
     `instrumenter.go`, KHÔNG đoán):** instrumenter xử lý `IfStmt`,
     `SwitchStmt` (cả expression VÀ type-switch variant), `ForStmt`
     condition trong CẢ HAI mode — KHÔNG evidence nào cho `SelectStmt`
     handling (xác nhận lại README's "doesn't cover select statements,"
     ĐÚNG cho cả `-branch` mode). Verify trực tiếp market-reference-
     service's authoritative implementation hiện tại
     (`grep -rn "select {" go/market-reference-service`): **KHÔNG
     `select` statement nào tồn tại** trong subject hiện tại —
     unsupported construct này KHÔNG ảnh hưởng branch applicability/
     evidence completeness cho `market-reference-service` TẠI boundary
     hiện hành. Go-generics parsing support của chính gobco's AST-based
     instrumenter KHÔNG verify được rõ ràng từ documentation/source đã
     khảo sát (verify trực tiếp market-reference-service: KHÔNG generic
     type parameter nào tồn tại trong subject hiện tại — moot cho
     subject hiện tại, NHƯNG gobco's own generics support VẪN LÀ một
     fact chưa xác định sạch sẽ) — ghi nhận LÀM **installation-time
     fail-closed verification requirement**: bất kỳ transaction cài
     đặt/pin tương lai, HOẶC bất kỳ thay đổi tương lai đưa `select`
     statement/generic type parameter vào market-reference-service (hay
     bất kỳ subject Go nào khác dự định dùng gobco), PHẢI tự verify lại
     trực tiếp gobco's select/generics support TRƯỚC KHI chấp nhận
     branch-mode result LÀM evidence — KHÔNG giả định support, KHÔNG tự
     waiver gap này.
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

### Python line+branch coverage mechanism — CANDIDATE (v0.5, pending Product Owner decision)

```text
[v0.5 bổ sung — vai trò: `Python QG Coverage Mechanism Candidate Author`. Đây LÀ
  implementation-readiness transaction §"Framework/tool selection" trên ĐÃ anticipate —
  GIỚI HẠN CHỈ Python line-coverage VÀ branch-coverage MEASUREMENT MECHANISM (Chapter 13
  §13.3's hai coverage metric, cả hai hiện thiếu cho feature-engine), KHÔNG PHẢI general
  test framework selection (pytest ĐÃ pin sẵn tại feature-engine's own pyproject.toml —
  không phải quyết định của transaction này — KHÔNG chạm).]

Vấn đề: feature-engine (Tier 1 — Core Logic, module-registry.yaml v1.7) yêu cầu line
  coverage >= 90% VÀ branch coverage >= 90%, độc lập (§13.3, KHÔNG đổi). Formal Chapter 13
  Quality Gate evaluation (`docs/MANIFEST.md`, boundary
  8374db364fd08c1592f2ae918d01e9ec3e95b131, corrected by bounded evidence correction
  7572076c35d8e07fd29599dfde5dff9d26885db5) recorded BOTH `P3-FEATURE-QG-EVID-01` (line
  coverage) VÀ `P3-FEATURE-QG-EVID-02` (branch coverage) AS `FAIL — evidence`: verify trực
  tiếp `python/feature-engine/pyproject.toml`'s `[project.optional-dependencies].dev` VÀ
  `requirements-dev.lock.txt` — KHÔNG `coverage`/`pytest-cov`/tương đương nào được pin;
  `python -c "import coverage"` trên fresh clean-room reconstruction từ lock file hiện
  hành -> `ModuleNotFoundError` (re-verified tại transaction này). KHÁC Go's gobco
  situation (native branch support KHÔNG tồn tại trong toolchain), Python's own PROBLEM ở
  đây KHÔNG PHẢI "không cơ chế nào đo được branch" — nó LÀ "chưa tool nào được accept/pin
  cho category này" (baseline-existence gap, KHÔNG capability gap).

CANDIDATE mechanism được đề xuất: **coverage.py** (PyPI package `coverage`,
  github.com/coveragepy/coveragepy, tác giả chính Ned Batchelder). Đánh giá theo 20 tiêu
  chí governing task's own list (verify trực tiếp upstream docs/PyPI metadata/empirical
  execution trong một scratch venv NGOÀI repository — KHÔNG cài vào feature-engine, KHÔNG
  từ memory/marketing summary):

  1. True line coverage: CÓ — statement-level execution tracking qua Python's own
     `sys.settrace`/`sys.monitoring` (verify trực tiếp module docstring: "uses the code
     analysis tools and tracing hooks provided in the Python standard library").
  2. True branch coverage: CÓ — **arc-based measurement**, KHÔNG phải condition/MC-DC
     decomposition (verify trực tiếp docs: "coverage.py collects pairs of line numbers: a
     source and destination for each transition from one line to another"; percentage =
     "actual executions divided by execution opportunities... each branch destination" là
     một execution opportunity). Đây LÀ whole-controlling-condition granularity — CÙNG lớp
     metric gobco's `-branch` mode đo cho Go (KHÔNG phải gobco's default condition-mode
     decomposition of `&&`/`||`) — KHÔNG có "chế độ mặc định sai" pitfall tương tự gobco,
     vì coverage.py CHỈ CÓ MỘT branch-measurement mode (bật/tắt qua `branch = True`/
     `--branch`, KHÔNG có chế độ condition-decomposition thay thế để nhầm lẫn).
  3. **Line VÀ branch có độc lập reportable không — verify trực tiếp EMPIRICALLY (KHÔNG chỉ
     đọc doc), phát hiện QUAN TRỌNG:** `coverage report`'s mặc định TEXT table hiển thị MỘT
     cột "Cover" DUY NHẤT — cột này LÀ một **BLENDED/combined percentage**
     ((covered_lines + covered_branches) / (num_statements + num_branches)), KHÔNG PHẢI
     một trong hai metric độc lập. Verify trực tiếp bằng thực nghiệm (toy module, 3 test
     case, `coverage run --branch` + `coverage report -m` + `coverage json --pretty-print`
     trong scratch venv riêng): TEXT report hiển thị "Cover: 88%" (blended, từ 15+6=21
     covered / 16+8=24 total = 87.5% -> hiển thị làm tròn 88%) — NHƯNG `coverage json`'s
     per-file/per-total `summary` object chứa BA percentage field TÁCH BIỆT:
     `percent_statements_covered` (93.75% trong thực nghiệm — line-only), 
     `percent_branches_covered` (75.0% trong thực nghiệm — branch-only), VÀ
     `percent_covered` (87.5% — BLENDED, giống hệt TEXT report's "Cover" cột). Đây LÀ
     đúng loại defect Chapter 13 §13.3 cấm tường minh ("không bù trừ giữa hai metric,
     không dùng con số tổng hợp") nếu một transaction cài đặt/evidence-recording tương lai
     vô tình dùng `percent_covered`/TEXT "Cover" cột LÀM MỘT TRONG HAI Chapter-13 metric —
     **MECHANISM ĐƯỢC ĐỀ XUẤT CHÍNH XÁC CHO CHAPTER 13: chạy `coverage run --branch` (bật
     branch instrumentation), sau đó đọc RIÊNG `percent_statements_covered` VÀ
     `percent_branches_covered` từ `coverage json`'s `totals` object — KHÔNG BAO GIỜ đọc
     `percent_covered`/TEXT report's "Cover" cột LÀM MỘT TRONG HAI floor value.** Đây LÀ
     phát hiện MỚI, tương đương pitfall gobco's condition-vs-branch mode nhưng khác cơ chế
     (Go: sai MODE; Python: sai FIELD trong cùng report).
  4. Branch semantics chi tiết (verify trực tiếp EMPIRICALLY qua toy module có if/elif/
     else + for-loop + short-circuit `and`):
     - if/elif/else: mỗi nhánh quyết định tạo MỘT arc riêng tới đích của nó (verify: `if
       x>0 and y>0: ... elif x>0: ... else: ...` tạo arc `(2,3)` [vào `if`-body],
       `(2,4)` [rớt xuống `elif`], `(4,5)` [vào `elif`-body], `(4,7)` [rớt xuống `else`] —
       4 arc tổng cho khối 3-nhánh, verify trực tiếp `missing_branches` field liệt kê
       `[4, 7]` khi nhánh `else` chưa test).
     - loop (for): tạo arc vào loop-body VÀ arc thoát loop/loop-back — verify trực tiếp
       `missing_branches` liệt kê `[13, 12]` (loop-continue backedge khi input rỗng/toàn
       bộ item fail điều kiện chưa test).
     - short-circuit boolean (`and`/`or`): coverage.py's ARC model KHÔNG decompose
       `x > 0 and y > 0` thành hai atomic sub-expression riêng (verify trực tiếp: dòng
       `if x > 0 and y > 0:` chỉ tạo ĐÚNG hai arc, `(2,3)` VÀ `(2,4)`, KHÔNG bốn arc cho
       từng operand) — nghĩa là coverage.py's branch metric LÀ decision/branch coverage cổ
       điển (whole controlling expression outcome), KHÔNG PHẢI condition/MC-DC coverage —
       khớp CHÍNH XÁC granularity Chapter 13 §13.3 yêu cầu cho floor bắt buộc (§13.3 tự nó
       phân biệt "Condition/MC-DC coverage LÀ tùy chọn theo tier, KHÔNG tính vào floor bắt
       buộc" — coverage.py's MỘT metric duy nhất tự động LÀ đúng loại cho floor, KHÔNG có
       nguy cơ nhầm condition-mode làm branch-mode như gobco).
     - exception/control-flow (try/except/finally, `with`, match statement): KHÔNG verify
       trực tiếp tại candidate này (feature-engine's authoritative implementation hiện
       KHÔNG dùng `match` statement nào — verify trực tiếp `ast.walk` script trên toàn bộ
       `src/feature_engine/*.py`, ZERO `ast.Match` node — moot cho subject hiện tại,
       NHƯNG coverage.py's own generic try/except handling KHÔNG verify sâu tại candidate
       này, ghi nhận LÀM install-time verification item nếu exception-branching logic được
       thêm sau này).
     - **partial branch**: một arc-đích được biết (static analysis) nhưng KHÔNG BAO GIỜ
       exercise được gọi LÀ "partial branch" (verify trực tiếp doc + thực nghiệm — `BrPart`
       cột trong TEXT report, `num_partial_branches`/`missing_branches` trong JSON) —
       structurally-partial construct (`while True`, `if 0`) được coverage.py's own static
       analysis tự nhận diện một số pattern, pattern tùy biến khác cần `# pragma: no
       branch` — verify trực tiếp doc, KHÔNG cần dùng tại candidate này vì
       feature-engine's hiện tại KHÔNG chứa construct dạng đó (chưa verify sâu, cần
       install-time re-check nếu construct này xuất hiện).
  5. Numerator/denominator semantics: line — `covered_lines`/`num_statements` (executable
     statement, KHÔNG comment/blank/docstring); branch — `covered_branches`/`num_branches`
     (arc destination đã biết qua static analysis). Cả hai field TÁCH BIỆT verify trực
     tiếp trong `coverage json` output (điểm 3 trên).
  6. Authoritative source boundary: `[run] source = feature_engine` (verify trực tiếp
     config doc: "A list of packages or directories, the source to measure... If set,
     `include` is ignored") — scope đo CHỈ package `feature_engine` đã cài (từ
     `src/feature_engine/`, đúng `pyproject.toml`'s `[tool.setuptools.packages.find]
     where = ["src"]`), KHÔNG đo `tests/` (test file KHÔNG thuộc package `feature_engine`,
     tự động loại khỏi numerator/denominator KHI dùng `source`, KHÔNG cần `omit` riêng cho
     test). `candle_window.py`'s permanently-fail-closed `CandleWindowFeatureEngine` path
     VẪN nằm trong `source` scope — KHÔNG omit để inflate percentage (đúng governing
     task's own instruction VÀ Chapter 13 §13.3 anti-gaming).
  7. Include/omit configuration semantics: `source` (allowlist, ưu tiên hơn `include` khi
     cả hai đặt) VÀ `omit` (blocklist glob pattern, áp DÙ `source`/`include` đã chọn) —
     verify trực tiếp config doc. KHÔNG omit nào được đề xuất tại candidate này (toàn bộ
     `src/feature_engine/**` PHẢI nằm trong boundary, KHÔNG loại trừ file khó đo).
  8. Deterministic invocation: đo trên lần chạy test THẬT qua `pytest` thật (KHÔNG mock
     kết quả) — output deterministic CHỪNG NÀO chính test suite deterministic (đúng
     §13.2/I-2/I-3 ĐÃ có, KHÔNG tạo rule mới, CÙNG nguyên tắc đã áp dụng cho gobco).
     KHÔNG network access khi chạy (chỉ cần network một lần LÚC `pip install`, giống mọi
     Python dependency).
  9. Machine-readable evidence: `coverage json --pretty-print` (verify trực tiếp field
     schema qua thực nghiệm điểm 3 trên) — JSON format có `meta.version`/
     `meta.format`/`meta.timestamp`, per-file VÀ `totals` summary object với field tách
     biệt line/branch — đủ chi tiết pin vào Chapter 13 §13.9 immutable evidence contract
     (subject identity, boundary, input identity, numerator/denominator, percentage).
     `coverage xml`/`coverage html` cũng tồn tại (KHÔNG evaluate sâu tại candidate này,
     JSON đã đủ cho evidence contract).
  10. Human-readable evidence: `coverage report -m` (TEXT table, cột Stmts/Miss/Branch/
      BrPart/Cover/Missing — verify trực tiếp thực nghiệm) — dùng LÀM supporting display
      CHỈ, KHÔNG BAO GIỜ dùng "Cover" cột LÀM Chapter-13 floor value (điểm 3 trên).
  11. Exit-code behavior: **phát hiện quan trọng, verify trực tiếp GitHub Issue #1152**
      ("Separate fail_under option for branch and statement coverage," nedbat/coveragepy,
      mở 2021-04-29, VẪN `Open`, KHÔNG assignee, KHÔNG PR) — `coverage report
      --fail-under=MIN` CHỈ áp dụng cho MỘT ngưỡng DUY NHẤT trên CHÍNH `percent_covered`
      BLENDED value (verify trực tiếp thực nghiệm: `--fail-under=90` trên toy module có
      blended 87.5% -> "Coverage failure: total of 88 is less than fail-under=90", exit
      code 2) — native `--fail-under` KHÔNG BAO GIỜ được dùng LÀM Chapter-13 pass/fail gate
      cho line HOẶC branch riêng lẻ, vì nó luôn đánh giá con số blended. **Một transaction
      cài đặt/evidence-recording tương lai PHẢI tự đọc `percent_statements_covered` VÀ
      `percent_branches_covered` từ JSON, so sánh RIÊNG từng cái với floor 90% CỦA CHÍNH
      Chapter 13 (không dùng `coverage`'s CLI exit-code cho quyết định pass/fail đó) —**
      exactly cùng discipline "không tự tạo pass/fail machinery ngoài Chapter 13" đã áp
      dụng cho mọi coverage evidence khác trong repository này.
  12. Python 3.13 compatibility: CÓ, verify trực tiếp PyPI classifier metadata (Python
      3.10–3.16 + PyPy3 hỗ trợ) VÀ thực nghiệm trực tiếp — cài `coverage==7.15.4` trên
      Python 3.13.6 (interpreter CHÍNH XÁC feature-engine's own toolchain đang dùng), chạy
      thành công, KHÔNG lỗi.
  13. pytest 9.x compatibility: CÓ, verify trực tiếp thực nghiệm — `python -m coverage run
      --branch -m pytest <subject> -q` với `pytest==9.1.1` (CHÍNH XÁC version đã pin tại
      feature-engine's `requirements-dev.lock.txt`) chạy thành công trong scratch venv.
      KHÔNG cần `pytest-cov` (plugin riêng bọc coverage.py qua `pytest --cov=`) —
      feature-engine hiện gọi `pytest` trực tiếp (KHÔNG qua wrapper plugin nào), nên invoke
      `coverage run -m pytest` (KHÔNG `pytest --cov`) giữ dependency footprint nhỏ nhất,
      KHÔNG thêm plugin thứ hai chỉ để bọc lại cùng công cụ.
  14. Maintenance health: CAO — verify trực tiếp PyPI/GitHub metadata: release gần nhất
      (7.15.4) tại thời điểm candidate này, project đã chuyển tổ chức GitHub
      `nedbat/coveragepy` -> `coveragepy/coveragepy` (transfer tổ chức, KHÔNG phải
      abandon — issue #1152 vẫn track dưới `nedbat/coveragepy` history), là de facto
      standard coverage tool cho Python ecosystem (dùng bởi pytest-cov, tox, hầu hết CI
      Python project) — maintenance-concentration risk THẤP HƠN NHIỀU so với gobco's
      single-maintainer/10-tag-total profile.
  15. License: Apache-2.0 (permissive, verify trực tiếp PyPI classifier) — rủi ro pháp lý
      thấp, CÙNG lớp permissiveness với gobco's BSD-2-Clause.
  16. Security/dependency impact: verify trực tiếp PyPI `requires_dist` — CHỈ MỘT dependency
      điều kiện, `tomli` (`python_full_version <= "3.11.0a6"`), KHÔNG áp dụng cho
      `feature-engine`'s `requires-python = ">=3.13"` — nghĩa là tại Python 3.13 (feature-
      engine's floor), `coverage` package tự nó có **ZERO transitive dependency** — dev-
      time-only dependency, KHÔNG ảnh hưởng feature-engine's own "zero production runtime
      dependency" invariant (`pyproject.toml [project].dependencies = []` KHÔNG đổi, `dev`
      optional-dependencies list LÀ nơi duy nhất dev tool được thêm).
  17. Reproducibility/pinning: pin được exact package version (`coverage==7.15.4` hoặc
      version khác tại thời điểm cài đặt thật) qua `requirements-dev.lock.txt`, CÙNG
      pattern `ruff==0.16.4`/`mypy==2.3.1`/`pytest==9.1.1` hiện hành — `pip install
      --no-deps -r requirements-dev.lock.txt` reproducibility đã verify trực tiếp (fresh
      venv, `pip check` -> "No broken requirements found," CÙNG discipline mọi QG evidence
      transaction trong repository này đã dùng).
  18. Known unsupported constructs relevant to feature-engine: verify trực tiếp AST scan
      toàn bộ `python/feature-engine/src/feature_engine/*.py` (script `ast.walk`,
      transaction này) — KHÔNG `match` statement, KHÔNG walrus operator (`:=`) nào tồn
      tại. CÓ MỘT PEP 695 generic-function syntax (`def normalize_input_facts[T](...)`,
      `contracts.py`) — verify trực tiếp EMPIRICALLY (toy module mô phỏng CHÍNH XÁC syntax
      này, `def normalize[T](items: list[T], *, flag: bool) -> list[T]: ...`, chạy
      `coverage run --branch` thành công, line/branch tracking đúng, KHÔNG lỗi parse) —
      coverage.py 7.15.4 xử lý ĐÚNG construct duy nhất "khác thường" mà feature-engine
      thực sự dùng. KHÔNG limitation nào phát hiện tại boundary hiện tại của subject này.
  19. Explicit-mode requirement risk: branch measurement đòi `branch = True` (config) hoặc
      `--branch` (CLI flag) tường minh — mặc định là `False` (verify trực tiếp doc: "Whether
      to measure branch coverage in addition to statement coverage" — boolean, default
      False) — một invocation quên flag này CHỈ sinh ra line coverage, KHÔNG branch coverage
      nào, KHÔNG BAO GIỜ được coi LÀ "branch coverage = N/A nên bỏ qua" — cùng rủi ro loại
      "quên flag" mà gobco's `-branch` cũng có, PHẢI verify tường minh tại mọi invocation
      evidence tương lai (pin rõ flag đã dùng trong evidence entry, KHÔNG CHỈ con số).
  20. Một mechanism cho cả hai metric: CÓ — coverage.py tự nó sinh CẢ line VÀ branch từ
      MỘT lần chạy (`coverage run --branch`), KHÔNG cần hai tool riêng biệt (KHÁC Go's
      tình huống, nơi `go tool cover` cho line NHƯNG cần gobco riêng cho branch) — pin RÕ
      trong evidence: hai percentage field TÁCH BIỆT từ CÙNG một `coverage.json` output,
      KHÔNG phải hai lần đo riêng biệt/hai tool riêng biệt.

Alternative mechanisms evaluated (verify trực tiếp, KHÔNG chỉ liệt kê tên):
  - `pytest-cov` (plugin wraps coverage.py via `pytest --cov=`): KHÔNG tạo branch metric
    MỚI nào — nó CHỈ LÀ một convenience wrapper GỌI coverage.py bên dưới, cùng engine/
    cùng arc semantics/cùng blended-vs-independent-field pitfall ở điểm 3 trên. KHÔNG chọn
    tại candidate này vì thêm một dependency layer (plugin) không cần thiết khi
    feature-engine's own test invocation đã đơn giản (`pytest tests/`, KHÔNG cần plugin
    injection) — invoke `coverage run -m pytest` trực tiếp giữ dependency count thấp hơn.
    KHÔNG bị loại trừ vĩnh viễn — nếu future CI integration cần pytest-plugin ecosystem
    (ví dụ song song với coverage combine cho multi-process test), một transaction cài đặt
    tương lai có thể tái đánh giá, KHÔNG quyết định trước tại đây.
  - `slipcover` (github.com/plasma-umass/slipcover): công cụ coverage thế hệ mới, tuyên bố
    tốc độ cao hơn coverage.py qua sys.monitoring (Python 3.12+); verify trực tiếp: dự án
    nhỏ hơn/community nhỏ hơn coverage.py NHIỀU (maintenance-concentration risk cao hơn),
    KHÔNG phải de facto ecosystem standard, KHÔNG được pytest/tox/CI convention nào coi LÀ
    default — REJECTED làm primary candidate tại v0.5 này (performance advantage KHÔNG
    phải yêu cầu Chapter 13 nào, correctness/maturity/ecosystem-alignment ưu tiên hơn tại
    một Tier-1 evidence-producing tool).
  - Manual/ad-hoc instrumentation (tự viết tracer qua `sys.settrace`): REJECTED tường minh
    — vi phạm chính nguyên tắc "không tự tạo cơ chế đo mới thay vì dùng công cụ đã
    established" mà cả gobco's own candidate reasoning VÀ Chapter 13 §13.3's "không khóa
    tool cụ thể NHƯNG PHẢI có cơ chế reproducible" đều ngụ ý — tái phát minh một coverage
    engine LÀ hard-to-reverse VÀ high-maintenance-burden hơn hẳn dùng ecosystem-standard
    tool.
  - "Ước lượng/suy diễn branch coverage từ line coverage" (không dùng tool riêng nào): TỪ
    CHỐI tường minh — vi phạm trực tiếp §13.3 "không estimate," CÙNG lý do gobco's
    candidate đã từ chối approach tương tự cho Go.

ADR-scope disposition (đầy đủ, chạy TRƯỚC khi author candidate này, chạy LẠI TỪ ĐẦU, KHÔNG
  copy kết luận Go): **`ADR_NOT_REQUIRED`.**
  Authority kiểm soát kết quả: [Chapter 13 §13.3](../constitution/13-quality-gates.md)
  ("Không khóa tool/vendor cụ thể (defer §13.14)") VÀ
  [Chapter 13 §13.14](../constitution/13-quality-gates.md) ("concrete tooling... defer
  sang Engineering Foundation Chapter 3 §3.2") ĐÃ Locked VÀ tự nó chỉ định CHÍNH Chapter 3
  §3.2/Testing Convention LÀM authority cho quyết định này — KHÔNG phải một chapter/ADR
  khác. Chapter 3 §3.2 dòng 44 (Locked v1.4) ĐÃ có carve-out tường minh: "Testing
  Convention ở đây chỉ quy định style/tooling (framework, cấu trúc test file, naming test
  case)" — một cơ chế đo coverage LÀ "tooling" theo đúng nghĩa đó, KHÔNG PHẢI một
  baseline-existence question mới (Testing Convention category đã tồn tại, `testing.md`
  v0.2 đã Approved, v0.4's Go candidate đã dùng CHÍNH pattern này). Verify từng nhánh
  Chapter 0 §4b riêng cho quyết định NÀY (KHÔNG suy diễn từ Go's kết luận):
  - KHÔNG Platform Invariant nào đổi (Chapter 2, KHÔNG chạm) — coverage measurement KHÔNG
    phải invariant, KHÔNG redefine I-2/I-3/I-9/I-13 substance.
  - KHÔNG Event Schema nào đổi — KHÔNG Domain Contract/`docs/domain/**` chạm.
  - KHÔNG Module Taxonomy/dependency graph nào đổi — `module-registry.yaml` KHÔNG chạm,
    cấm tường minh tại transaction này; `feature-engine`'s `depends_on`/
    `forbidden_dependencies` KHÔNG đổi (candidate KHÔNG phải một module, KHÔNG phải một
    dependency edge).
  - KHÔNG Governance/Approval process nào đổi (Chapter 12, KHÔNG chạm).
  - KHÔNG supersede ADR Locked nào (KHÔNG ADR nào hiện có về Python coverage-measurement
    tooling).
  - ">1 module HOẶC khó đảo ngược" — vế ">1 module": đọc theo ĐÚNG tiền lệ đã dùng cho
    gobco's own candidate (`ADR-030`'s "pattern (a)" LÀ cho baseline-existence/cross-module
    authority MỚI, KHÔNG PHẢI cho chọn MỘT tool cụ thể bên trong category ĐÃ pre-authorized)
    — chọn coverage.py CHO feature-engine hiện tại KHÔNG tự động ràng buộc bất kỳ module
    Python khác nào (structure-engine/raw-regime-engine) phải dùng CÙNG tool — mỗi module's
    own future coverage-evidence transaction có thể tự re-verify/re-select độc lập, đúng
    §13.14's "không khóa tool/vendor cụ thể." Vế "khó đảo ngược": KHÔNG hard-to-reverse
    lock-in (dev/test-time-only Python package, Apache-2.0, zero-dependency tại Python
    >=3.13, đổi sang candidate khác chỉ đổi lệnh invoke + field JSON đọc, KHÔNG đổi schema/
    infrastructure/production dependency nào).
  - Chapter 13 §13.4's tier/floor VÀ §13.8's pass/fail semantics KHÔNG bị candidate này
    redefine — candidate CHỈ định nghĩa CƠ CHẾ ĐO, KHÔNG định nghĩa lại ngưỡng/tier/pass-
    fail (verify trực tiếp: không con số 90%/Tier 1 nào bị lặp lại/redefine trong candidate
    text trên — mọi tham chiếu ngưỡng đều trỏ NGƯỢC về Chapter 13, KHÔNG duplicate).
  - Transaction này KHÔNG cài đặt/pin tool, KHÔNG đo Feature coverage, KHÔNG rerun QG —
    strictly bounded candidate-authoring, củng cố (KHÔNG làm yếu) kết luận
    `ADR_NOT_REQUIRED`.
  Kết luận: `ADR_NOT_REQUIRED`, KHÔNG author ADR tại transaction này. KHÔNG
    GOVERNED_DECISION_REQUIRED escalation triggered.

Installation-time verification contract (BẮT BUỘC cho bất kỳ transaction cài đặt/pin
  tương lai — fail-closed nếu bất kỳ mục nào KHÔNG resolve được):
  - exact package/tool identity (`coverage` trên PyPI, KHÔNG nhầm với package khác cùng
    tên trên index khác);
  - exact pinned version (verify trực tiếp lại — candidate landscape/latest release CÓ
    THỂ đổi giữa candidate-authoring và install-time);
  - upstream/content identity nơi thực tế được (PyPI wheel hash/sha256, `pip download`
    verify);
  - Python 3.13 compatibility (re-verify tại version cài đặt thật, KHÔNG giả định version
    tại candidate này vẫn còn support tương đương);
  - current feature-engine test-runner compatibility (`pytest` version hiện hành tại
    thời điểm cài đặt, có thể khác `9.1.1` nếu lock file đã update);
  - exact line-coverage invocation (`coverage run --source=feature_engine -m pytest ...`
    hoặc cú pháp tương đương, verify lại syntax);
  - exact branch-coverage invocation (`--branch`/`branch = True`, verify lại flag/config
    key CHƯA đổi tên/semantics giữa version);
  - numerator/denominator semantics (`percent_statements_covered`/`percent_branches_
    covered` field name/meaning CHƯA đổi giữa version — verify lại JSON schema `meta.
    format` version);
  - branch semantics (arc-based, whole-controlling-condition — verify lại KHÔNG đổi sang
    condition-decomposition mặc định ở version mới);
  - include/source boundary (`source = feature_engine` scope CHÍNH XÁC package đã cài,
    KHÔNG lẫn `tests/`);
  - omit/exclusion rules (KHÔNG omit file authoritative nào chỉ để tăng %, mọi `# pragma:
    no cover`/`no branch` nếu dùng PHẢI có lý do tường minh, KHÔNG dùng để né code khó đo);
  - output format (`coverage json` schema field names CHƯA đổi — re-verify `meta.format`
    version number tại thời điểm cài đặt);
  - machine-readable artifact (JSON file thật được tạo, KHÔNG chỉ TEXT report);
  - exit semantics (KHÔNG dùng `--fail-under`/CLI exit code LÀM Chapter-13 pass/fail —
    self-computed comparison từ JSON field, verify lại field vẫn tồn tại);
  - reproducibility trong clean environment (fresh venv, `pip install --no-deps -r
    requirements-dev.lock.txt`, `pip check` -> "No broken requirements found," CÙNG
    discipline mọi QG evidence transaction khác);
  - unsupported Python construct liên quan tới feature-engine tại THỜI ĐIỂM cài đặt (re-
    scan AST — implementation CÓ THỂ đã thêm `match`/walrus/construct mới kể từ candidate
    này được author);
  - bằng chứng KHÔNG limitation tool nào làm denominator KHÔNG đầy đủ cho subject hiện tại
    (re-verify PEP 695 generics/bất kỳ construct mới nào).
  Nếu bất kỳ mục nào KHÔNG resolve được tại thời điểm cài đặt -> fail-closed, KHÔNG chấp
  nhận tool LÀM evidence machinery cho tới khi resolve xong.

KHÔNG tại transaction này (candidate-only, tường minh):
  - KHÔNG cài đặt/`pip install coverage` (hay bất kỳ tool nào) vào `python/feature-engine`
    hay bất kỳ module Python nào trong repository (mọi thực nghiệm ở trên chạy trong một
    scratch venv NGOÀI repository, KHÔNG commit, KHÔNG ảnh hưởng `pyproject.toml`/
    `requirements-dev.lock.txt`).
  - KHÔNG thêm dependency nào vào `pyproject.toml`/`requirements-dev.lock.txt`.
  - KHÔNG đo Feature Engine coverage thật — KHÔNG con số % nào được tạo ra cho
    `feature-engine` tại transaction này.
  - KHÔNG tạo/sửa CI workflow (`ci-cd.md`/`ADR-030` authority riêng, KHÔNG chạm).
  - KHÔNG close/remediate `P3-FEATURE-QG-EVID-01`/`P3-FEATURE-QG-EVID-02` — cả hai VẪN
    `FAIL — evidence`, KHÔNG tự động resolve bởi việc có một candidate.
  - KHÔNG rerun/reinterpret feature-engine's own Chapter 13 Quality Gate — overall QG VẪN
    `FAIL — evidence` cho tới khi một formal re-evaluation thật thực thi SAU KHI line VÀ
    branch coverage thật đo được TỪ tool đã cài đặt/pin chính thức.
  - KHÔNG đổi Chapter 13 coverage floor/tier/pass-fail semantics.
  - KHÔNG approve module/Data Layer/Phase nào. KHÔNG authorize LIVE. KHÔNG start Context
    Aggregator.
  - KHÔNG chạm existing Go branch-coverage mechanism/history (gobco candidate,
    `P3-GOBC-A-MAJ-01` closure evidence, §"Go branch-coverage mechanism — CANDIDATE" phía
    trên) — byte-equivalent, KHÔNG reopen, KHÔNG normalize Python choice thành Go choice
    hay ngược lại (hai ngôn ngữ, hai candidate độc lập, KHÔNG một tool nào bắt buộc dùng
    xuyên cả hai).
  Chọn/pin/cài đặt chính thức mechanism này (hoặc bất kỳ candidate khác xuất hiện sau) LÀ
  một transaction riêng biệt tương lai — PHẢI tự verify trực tiếp lại toàn bộ 20 tiêu chí
  trên VÀ installation-time verification contract ở trên TẠI thời điểm đó (candidate
  landscape/maintenance status/version CÓ THỂ đổi), VÀ tự rerun ADR Scope Rule nếu bất kỳ
  fact nền tảng nào ở trên đổi.

CANDIDATE ≠ APPROVED/ACCEPTED ≠ INSTALLED ≠ PINNED ≠ QUALIFYING QG EVIDENCE. Mechanism đề
  xuất tại đây KHÔNG được dùng LÀM Feature QG evidence cho tới khi toàn bộ governance chain
  (Product Owner decision trên chính candidate này, installation-time verification contract
  ở trên, VÀ một formal QG re-evaluation riêng biệt) hoàn tất.
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
v0.4  2026-08-20  Bounded correction, đóng `P3-GOBC-A-MAJ-01` — vai trò:
      `Go Branch-Coverage Candidate Bounded Correction Executor`. v0.3
      conflated gobco's default **condition coverage** mode (atomic
      boolean sub-expression true/false, verify trực tiếp
      `instrumenter.go`'s `markConds`: decompose `&&`/`||`/`!`) với
      gobco's distinct, explicit **`-branch`** flag mode (instrument
      CHỈ whole controlling condition — `markConds`: `break` cho
      `UnaryExpr`/`BinaryExpr`, KHÔNG decompose; source comment tự xác
      nhận "In branch coverage mode, only the whole controlling
      condition is instrumented") — rồi coi default-mode output đủ cho
      Chapter 13's branch metric. SAI: condition coverage KHÔNG suy ra
      branch coverage cho compound condition (phản ví dụ `if (a || b)`:
      2 test case đạt 100% atomic condition coverage NHƯNG whole-
      expression KHÔNG BAO GIỜ `False`, branch coverage CHỈ 50%). Sửa:
      (1) mechanism đề xuất chính xác LÀ gobco chạy VỚI `-branch` flag,
      KHÔNG default invocation; (2) condition coverage VÀ branch
      coverage LÀ hai metric tách biệt, KHÔNG thay thế cho nhau; (3)
      default condition-mode output TUYỆT ĐỐI KHÔNG substitute LÀM
      Chapter-13 branch metric; (4) Chapter 13's branch floor CHỈ
      consume verified branch-mode (`-branch=true`) result; (5)
      transaction cài đặt/pin tương lai PHẢI verify trực tiếp exact
      command/flag syntax (README KHÔNG document `-branch`, CHỈ tồn
      tại trong source — install-time verification gap tường minh),
      tool version/content identity, branch-mode numerator/denominator
      semantics, output format (`printOutput()` đổi label thành "Branch
      coverage: N/M" khi `-branch=true`, verify lại tại install-time),
      exit-code semantics, reproducibility đối với go1.26.6/`go 1.25`
      hiện hành — TRƯỚC KHI tool trở thành accepted evidence machinery.
      Limitation review bổ sung (verify trực tiếp `instrumenter.go`):
      instrumenter xử lý `IfStmt`/`SwitchStmt` (cả hai variant)/
      `ForStmt` trong CẢ HAI mode, KHÔNG evidence nào cho `SelectStmt`
      (xác nhận README's "doesn't cover select statements," đúng cho cả
      branch mode). Verify trực tiếp market-reference-service hiện tại:
      KHÔNG `select` statement, KHÔNG generic type parameter nào tồn
      tại trong subject — unsupported constructs KHÔNG ảnh hưởng branch
      applicability/evidence completeness cho subject hiện tại; gobco's
      own generics-parsing support (tổng quát, KHÔNG riêng subject này)
      VẪN chưa xác định sạch sẽ — ghi nhận LÀM installation-time
      fail-closed verification requirement cho bất kỳ subject/thay đổi
      tương lai nào đưa `select`/generic vào phạm vi dự định dùng gobco.
      **KHÔNG đổi:** `ADR_NOT_REQUIRED` (correction này KHÔNG phát hiện
      §4b trigger mới — CHỈ làm rõ invocation-mode/limitation detail
      bên trong CÙNG một candidate tooling category ĐÃ pre-authorized),
      gobco VẪN LÀ candidate (KHÔNG đổi candidate, CHỈ invocation mode
      được làm rõ), `status` VẪN `Draft` (not self-approved,
      `G-ORCH-002`), Chapter 13 KHÔNG chạm, KHÔNG cài đặt tool, KHÔNG
      `go.mod`/`go.sum`, KHÔNG CI integration, QG VẪN `FAIL —
      evidence`, LIVE VẪN `NOT_AUTHORIZED`, §1–§16/§18/Non-goals/
      ADR-scope disposition gốc/Framework-selection general deferral
      KHÔNG chạm. KHÔNG cài đặt gobco. KHÔNG rerun Quality Gate. KHÔNG
      sửa implementation/test code nào.
ACCEPTANCE  2026-08-20T09:22:00+07:00  Product Owner lifecycle approval
      — mechanical, vai trò: `Testing Convention v0.4 Mechanical
      Approval Recorder`. Quyết định: "APPROVE TESTING CONVENTION V0.4."
      Reviewed immutable boundary: HEAD
      2d4f7a7497873050b2da9defee0f91fa03d5613e, blob
      269ecaa0c6ee4780a81de0b8d18b9a98c2b136a7. Review A: COMPLETE/
      ELIGIBLE/CLEAN, đóng `P3-GOBC-A-MAJ-01`, Blocker 0/Major 0/Minor
      0, `ADR_NOT_REQUIRED` confirmed. Independent Review B: COMPLETE/
      ELIGIBLE/CLEAN, Mode B (`SAME_PRINCIPAL_DISTINCT_EXECUTION`),
      execution reference `P3-GOBC-B-2d4f7a7-20260820T0904+0700`,
      isolation attestation SATISFIED, Blocker 0/Major 0/Minor 0,
      `ADR_NOT_REQUIRED` confirmed, `READY_FOR_PRODUCT_OWNER_DECISION`.
      Independent-review requirement SATISFIED. `status: Draft ->
      Approved`, `approved_by: null -> Product Owner`, `approved_at:
      null -> "2026-08-20"`. `version` KHÔNG bump (pure mechanical
      lifecycle approval) — VẪN `0.4`. KHÔNG semantic content nào đổi
      (§1–§18 byte-equivalent ngoài banner/lifecycle metadata/change
      history này) — gobco VẪN candidate, `-branch` mode VẪN required
      invocation, condition ≠ branch coverage VẪN đúng, installation-
      time verification requirements VẪN nguyên vẹn, `SelectStmt`
      limitation VẪN disclosed, current subject applicability KHÔNG
      đổi, generics compatibility VẪN fail-closed/unresolved, Chapter
      13 VẪN sole authority. KHÔNG cài đặt gobco, KHÔNG `go.mod`/
      `go.sum`/tool binary, KHÔNG CI workflow, KHÔNG đổi gobco
      invocation semantics, KHÔNG chạm Chapter 13/coverage floor/
      `module-registry.yaml`/dependency graph/implementation/test
      code/`ADR-032`/Domain Contract, KHÔNG rerun Quality Gate, KHÔNG
      claim QG PASS. `market-reference-service` Chapter 13 QG VẪN
      `FAIL — evidence`. KHÔNG approve `market-reference-service`/Data
      Layer nào. KHÔNG authorize LIVE. Tài liệu VẪN LÀ living document
      — `Approved` KHÔNG immutable byte-for-byte như ADR;
      `ADR_NOT_REQUIRED` VẪN đúng; thay đổi SEMANTIC tương lai VẪN
      PHẢI tự rerun ADR Scope Rule.
v0.5  2026-08-28  CANDIDATE amendment, KHÔNG self-approved — vai trò:
      `Python QG Coverage Mechanism Candidate Author`. `status: Approved
      → Draft`, `version: "0.4" → "0.5"`, `approved_by`/`approved_at`
      reset `null` (v0.4's approval record giữ nguyên nguyên vẹn phía
      trên LÀM historical evidence, KHÔNG bị ghi đè). ADR Scope Rule
      chạy LẠI TỪ ĐẦU (KHÔNG copy kết luận Go) -> `ADR_NOT_REQUIRED`.
      Bổ sung MỘT subsection MỚI dưới "Framework/tool selection":
      "Python line+branch coverage mechanism — CANDIDATE" — targets
      feature-engine's formal Chapter 13 QG findings
      `P3-FEATURE-QG-EVID-01`/`P3-FEATURE-QG-EVID-02` (line/branch
      coverage FAIL — evidence, `docs/MANIFEST.md`, boundary
      8374db364fd08c1592f2ae918d01e9ec3e95b131). CANDIDATE mechanism:
      **coverage.py** (PyPI `coverage`, github.com/coveragepy/
      coveragepy) — evaluated against 20 criteria via primary
      upstream documentation AND empirical verification in an isolated
      scratch venv (outside the repository, discarded after use, no
      module/tool ever installed into `python/feature-engine`). Key
      findings: (1) arc-based branch measurement, single mode (no
      condition-vs-branch mode pitfall unlike gobco); (2) **critical
      anti-conflation finding** — `coverage json`'s `percent_covered`
      field is a BLENDED line+branch percentage, DISTINCT from the
      separately-reportable `percent_statements_covered`/
      `percent_branches_covered` fields — only the latter two may ever
      be used as Chapter 13's two independent metrics, verified via a
      toy-module experiment; (3) native `--fail-under` applies only to
      the blended percentage (verified via GitHub Issue #1152, "Separate
      fail_under option for branch and statement coverage," open since
      2021-04-29, no assignee/PR) — a future install transaction must
      self-compute pass/fail from the two independent JSON fields, never
      from the tool's own CLI exit code; (4) empirically verified
      Python 3.13.6 + pytest 9.1.1 compatibility (feature-engine's own
      exact toolchain versions) and correct handling of the one PEP 695
      generic-function syntax construct feature-engine's own source
      actually uses (`contracts.py`'s `normalize_input_facts[T]`); (5)
      Apache-2.0 license, zero transitive runtime dependency at Python
      >=3.13 (verified via PyPI `requires_dist`), de-facto Python
      ecosystem standard (materially healthier maintenance profile than
      gobco's single-maintainer status). Alternatives evaluated and
      rejected: `pytest-cov` (adds a plugin layer wrapping the same
      engine, not chosen for this simpler invocation pattern, not
      permanently excluded); `slipcover` (smaller community, not an
      ecosystem default); manual/ad-hoc `sys.settrace` instrumentation
      and line-to-branch estimation (both explicitly rejected, same
      reasoning as the Go candidate's own rejections). Installation-time
      verification contract defined (fail-closed if any item unresolved
      at future install time). **KHÔNG** cài đặt/pin `coverage` (hay bất
      kỳ tool nào) vào bất kỳ module Python nào trong repository, KHÔNG
      thêm dependency vào `pyproject.toml`/`requirements-dev.lock.txt`,
      KHÔNG đo feature-engine coverage thật, KHÔNG tạo/sửa CI workflow,
      KHÔNG close/remediate `P3-FEATURE-QG-EVID-01`/`-EVID-02` (VẪN
      `FAIL — evidence`), KHÔNG rerun feature-engine's Chapter 13 QG
      (overall VẪN `FAIL — evidence`), KHÔNG đổi Chapter 13 floor/tier/
      pass-fail semantics, KHÔNG approve module/Phase nào, KHÔNG
      authorize LIVE, KHÔNG start Context Aggregator, KHÔNG chạm existing
      Go branch-coverage mechanism/history (gobco candidate,
      `P3-GOBC-A-MAJ-01` closure evidence — byte-equivalent, KHÔNG
      reopen, KHÔNG normalize cross-language). `module-registry.yaml`
      KHÔNG chạm. §1–§16/§18/Non-goals/v0.1–v0.4 banners/Go
      branch-coverage subsection KHÔNG chạm (byte-equivalent).
```
