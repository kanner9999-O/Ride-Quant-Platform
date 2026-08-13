---
id: engineering-ci-cd
title: "Engineering Foundation — CI/CD Convention (CI only)"
version: "0.1"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-13"
last_review: null
next_review: null
depends_on: ["../constitution/03-engineering-principles", "../constitution/12-approval-gates", "../constitution/13-quality-gates", "../adr/ADR-030", "../adr/ADR-017", "coding-standard", "naming", "logging", "config", "error-handling", "testing"]
---

# Engineering Foundation — CI/CD Convention (CI only)

**Vai trò của tài liệu này:** convention document THỨ TÁM VÀ CUỐI CÙNG của Phase 1.5 — Engineering Foundation (Chapter 3 §3.2), phạm vi CHỈ category **CI/CD** (Chapter 14 §14.2's Phase 1.5 scope list) — đúng `EF-TXN-002` (một category = một transaction bounded). **`ADR-030` v0.3 (Approved 2026-08-12) LÀ authority cho chính việc CÓ một cross-module CI/CD Convention baseline bắt buộc, GIỚI HẠN Foundation-level CI** — tài liệu này LÀ living convention chứa chi tiết rule reversible dưới authority đó, KHÔNG lặp lại decision text của ADR-030 (xem `ADR-030.md` cho full architecture text, KHÔNG duplicate tại đây).

**Nguyên tắc chi phối (ADR-030 §3, tái khẳng định KHÔNG redefine):** tên category "CI/CD" LÀ tên Roadmap category (Chapter 14 §14.2) — tài liệu này CHỈ establish phần **CI** (Continuous Integration: build/test/lint/validation automation, Foundation-level). Phần **CD** (deployment/promotion/release/LIVE) KHÔNG được authorize tại tài liệu này dưới bất kỳ hình thức nào — thuộc `Phase 7 — Deployment` (Chapter 14 §14.2, Approval Gate riêng, downstream) VÀ governance riêng biệt khác tại chính decision boundary đó tương lai (KHÔNG gán một authority cụ thể nào tại đây, đúng `ADR-030` §3/§6 v0.3). Một Trading Account mang `environment: LIVE` (`account.md` §8, KHÔNG đổi) KHÔNG tự nó authorize platform LIVE execution.

**Residual accepted riêng của category khác: `EF-CONFIG-B-MIN-01` VÀ `EF-ERR-B-MIN-01` VẪN `OPEN — accepted non-blocking`** — KHÔNG chạm, KHÔNG đóng tại đây (thuộc phạm vi correction riêng cho `config.md`/`error-handling.md` tương ứng, KHÔNG tại living convention document này).

## 1. CI purpose and authority boundary

```text
CI (Continuous Integration) tại Phase 1.5 LÀ automation execute các
  check ĐÃ authoritative (validation/lint/test/quality-evidence check/
  build verification khi applicable, §2 dưới) VÀ collect/forward kết
  quả — CI KHÔNG PHẢI một authority mới cho Ý NGHĨA của check đó.
CI orchestration CÓ THỂ chạy check VÀ report kết quả — KHÔNG được
  redefine owning authority của chính check đó (§3/§4 dưới).
**Boundary bắt buộc (ADR-030 §6, tái khẳng định KHÔNG redefine):**
  CI success ≠ Product Owner approval;
  CI success ≠ phase transition;
  CI failure ≠ Product Owner rejection.
  CI CÓ THỂ supply evidence cho Chapter 12/13 sử dụng; Product Owner
  VẪN LÀ sole lifecycle/phase decision authority (Chapter 12 §12.2(5),
  KHÔNG đổi) — tài liệu này KHÔNG redefine Approval Gate semantics.
```

## 2. Validation/lint/test/build-check orchestration

```text
Phạm vi check CI CÓ THỂ orchestrate (Foundation-level, ĐÃ authoritative
  ở nơi khác — CI CHỈ chạy VÀ report, KHÔNG invent):
  validation check (theo Chapter 13 §13.2 dimension đã established);
  lint/format check (theo `coding-standard.md`, Approved);
  identifier naming check khi applicable (theo `naming.md`, Approved);
  test execution (theo `testing.md`, Approved — §7 dưới);
  quality/evidence-producing check (theo Chapter 13 §13.9 evidence
    contract);
  build verification (§12 dưới, CHỈ khi ground truth tồn tại).
Thứ tự orchestration cụ thể (lint trước test, test trước build...) LÀ
  provider-neutral convention (§9 dưới) — tài liệu này KHÔNG bắt buộc
  MỘT thứ tự duy nhất, CHỈ khuyến nghị: check rẻ/nhanh (lint/format)
  chạy TRƯỚC check tốn kém hơn (test/build) để fail-fast, giảm chi phí
  vòng lặp.
```

## 3. Inheritance from existing authorities

```text
CI CÓ THỂ enforce/execute/validate conformance theo ĐÚNG rule ĐÃ
  authoritative — KHÔNG invent rule mới tại chính tài liệu này:
  Coding Standard (`coding-standard.md`, Approved)   — lint/format/
    dependency-hygiene rule, KHÔNG redefine.
  Naming (`naming.md`, Approved)                     — identifier
    naming rule, KHÔNG redefine.
  Logging (`logging.md`, Approved)                   — CI CÓ THỂ
    validate conformance (vd structured-log check), KHÔNG redefine
    level/field/schema.
  Config (`config.md`, Approved)                     — CI CÓ THỂ
    validate conformance (vd config schema check), KHÔNG redefine
    validation/startup rule (§11 dưới cho secret boundary riêng).
  Error Handling (`error-handling.md`, Approved)      — CI CÓ THỂ
    validate conformance, KHÔNG redefine taxonomy/boundary-translation/
    retry-classification.
  Testing (`testing.md`, Approved)                    — CI CÓ THỂ
    invoke test/consume output, KHÔNG redefine test structure/naming/
    isolation/tooling mechanics (§7 dưới cho flaky-test riêng).
Nếu một check CI cần chạy CHƯA có authority ĐÃ established (vd một
  loại validation hoàn toàn mới), đó LÀ một gap thuộc category tương
  ứng (Coding Standard/Testing/Logging/Config/Error Handling), KHÔNG
  tự invent tại `ci-cd.md`.
```

## 4. Chapter 13 quality/evidence boundary

```text
Chapter 13 (Locked) VẪN authority DUY NHẤT cho quality dimension,
  coverage/tier policy, tier resolution, gate applicability, pass/fail
  semantics, evidence contract (§13.9), waiver/exception semantics
  (§13.11) — KHÔNG đổi tại đây.
CI CÓ THỂ:
  execute check;
  collect raw result;
  produce hoặc transport evidence THEO ĐÚNG contract Chapter 13 §13.9
    ĐÃ established (§8 dưới cho evidence hand-off mechanics).
CI TUYỆT ĐỐI KHÔNG được:
  invent quality criteria mới;
  đổi coverage floor;
  reinterpret gate pass/fail;
  tạo competing evidence semantics (vd một "CI-owned" evidence schema
    thay thế Chapter 13 §13.9's contract).
```

## 5. Fail-safe handling khi required check KHÔNG evaluate được

```text
Khi một required check (theo Chapter 13 tier-resolution/gate
  applicability ĐÃ established) KHÔNG THỂ evaluate được tại thời điểm
  CI chạy (vd tool crash, dependency unavailable, tier KHÔNG resolve
  được) — CI PHẢI fail closed: KHÔNG tự suy diễn PASS, KHÔNG bỏ qua
  check đó âm thầm — đúng nguyên tắc Chapter 13 §13.8 "undefined tier
  applicability → fail-closed → eligibility incomplete," tái khẳng
  định nhất quán cho CI execution context, KHÔNG redefine.
CI report trạng thái "KHÔNG evaluate được" LÀM MỘT kết quả riêng biệt
  (KHÔNG PHẢI PASS, KHÔNG PHẢI FAIL thông thường) — Chapter 13 VẪN
  authority DUY NHẤT diễn giải trạng thái đó thành eligibility evidence
  (§13.8/§13.9, KHÔNG đổi).
```

## 6. Local-vs-CI logical parity

```text
Check chạy trong CI NÊN tương đương về mặt logic với check developer
  chạy local (cùng lint rule, cùng test suite, cùng validation logic)
  — tránh tình huống "pass local, fail CI" hay ngược lại CHỈ vì khác
  biệt environment KHÔNG cần thiết (vd version tool khác nhau, config
  khác nhau).
Tài liệu này KHÔNG mandate identical MÔI TRƯỜNG thực thi (local máy
  developer luôn khác CI runner ít nhiều) — CHỈ yêu cầu logic check
  (rule set, command semantic) nhất quán, KHÔNG PHẢI byte-identical
  infrastructure.
Local test command convention ĐÃ pin tại `testing.md` §13 (predictable
  entry point, KHÔNG hardcode tool chưa chọn) — CI orchestration NÊN
  tái sử dụng ĐÚNG entry point đó khi khả dụng, KHÔNG tạo một bộ lệnh
  song song khác biệt.
```

## 7. Test/quarantine interaction (Chapter 13 + Testing authority split)

```text
Đúng authority split ĐÃ pin tại `ADR-030` §6 (v0.2, KHÔNG đổi):
  Chapter 13 §13.10 (Locked)   VẪN authority DUY NHẤT cho flaky-test
    POLICY (cấm retry-until-green, quarantine required, flaky ≠
    passing evidence) — CI KHÔNG redefine.
  Testing Convention (`testing.md` §12, Approved)   VẪN authority CHỈ
    cho flaky-test/quarantine TOOLING MECHANICS (quarantine marker/
    owner/reason/CI-visibility) — KHÔNG PHẢI chính policy.
CI CÓ THỂ:
  invoke test (§2 trên);
  expose quarantine state/result (đọc marker ĐÃ định nghĩa tại
    `testing.md` §12, hiển thị trong report/output);
  collect/forward evidence theo ĐÚNG hai authority trên.
CI TUYỆT ĐỐI KHÔNG được:
  retry-until-green để đưa gate về pass (§13.10, KHÔNG đổi);
  tính một test quarantined LÀM passing evidence (§13.10, KHÔNG đổi);
  tự tạo quarantine mechanism mới ngoài `testing.md` §12 ĐÃ pin.
```

## 8. Evidence hand-off mechanics

```text
CI CÓ THỂ định nghĩa CÁCH kết quả check được hand off cho Chapter 13
  gate evaluation (vd format nội bộ CI dùng để lưu tạm kết quả trước
  khi Chapter 13's evidence-consuming process đọc) — KHÔNG tạo một
  evidence SCHEMA cạnh tranh với Chapter 13 §13.9's evidence contract.
Evidence hand-off PHẢI preserve tối thiểu những gì Chapter 13 §13.9 đã
  khóa (versioned + retained, KHÔNG ghi đè lịch sử) — CHI TIẾT storage/
  serialization mechanism cụ thể VẪN deferred (§13.14, KHÔNG đổi;
  Non-goals dưới).
CI KHÔNG PHẢI nguồn sự thật cho current state/version của evidence —
  MANIFEST VẪN authority đó theo I-12 (Chapter 13 §13.9, KHÔNG đổi).
```

## 9. Provider-neutral trigger/check organization

```text
Trigger convention (khi nào CI chạy — vd push, pull request, schedule)
  VÀ check organization (thứ tự stage: lint → test → build verification)
  PHẢI diễn đạt provider-neutral tại tầng convention này — CỤ THỂ
  workflow file/syntax của một provider CỤ THỂ (GitHub Actions YAML,
  GitLab CI YAML, Jenkinsfile...) KHÔNG author tại đây (§13 dưới).
Nguyên tắc tối thiểu:
  CI PHẢI chạy trên MỌI thay đổi đề xuất tích hợp vào nhánh chính
    (khái niệm "propose integration," KHÔNG PHẢI syntax trigger cụ
    thể của một provider);
  check organization NÊN theo thứ tự fail-fast (§2 trên);
  kết quả CI PHẢI visible/traceable (§14 dưới).
```

## 10. Affected-area/caching/concurrency mechanics (chỉ khi có ích)

```text
CI CÓ THỂ áp dụng affected-area detection (chỉ chạy check liên quan
  tới phần thay đổi, KHÔNG PHẢI toàn bộ repository mỗi lần) VÀ caching/
  concurrency optimization — CHỈ khi thực sự có ích cho tốc độ/chi
  phí, KHÔNG bắt buộc tại v0.1 này (0 module đã build, chưa có ground
  truth để tối ưu cụ thể).
Affected-area detection (nếu dùng) PHẢI conservative — KHÔNG bỏ sót
  check required THẬT SỰ liên quan tới thay đổi (đúng nguyên tắc fail-
  closed, §5 trên) — khi KHÔNG chắc chắn phạm vi ảnh hưởng, chạy đầy
  đủ hơn LÀ an toàn hơn bỏ sót.
Cơ chế cụ thể (tool/algorithm affected-area detection, caching key
  strategy, concurrency limit) VẪN deferred — thuộc implementation-
  readiness transaction riêng biệt tương lai (Non-goals dưới).
```

## 11. ADR-017/Config secret boundary

```text
CI/CD KHÔNG tạo custody/signing authority mới — `ADR-017` VẪN
  authority DUY NHẤT cho architecture-level Custody & Signing Trust
  Boundary (KHÔNG đổi).
NẾU CI cần secret-related configuration tương lai (vd một token để
  publish artifact, credential để access một dependency riêng tư), nó
  PHẢI inherit boundary ĐÃ pin tại `ADR-017`/`config.md` §8:
  reference/locator được phép, raw credential KHÔNG được phép trong
  ordinary config, KHÔNG log/persist secret (đúng `logging.md`/
  `error-handling.md` §"Security and redaction," tái khẳng định nhất
  quán cho CI context).
Raw exchange credential/private signing material KHÔNG được trở thành
  CI-owned authority CHỈ VÌ automation cần access — `custody-signing-
  service`'s authority (ADR-017 §3.1) giữ nguyên vẹn.
Credential mechanism/provider (Vault/KMS/HSM/secret manager, CI
  platform's built-in secret store...) VẪN NGOÀI phạm vi tài liệu này
  — deferred (Non-goals dưới), đúng `ADR-030` §6 v0.3.
```

## 12. Build verification (CHỈ khi ground truth tồn tại)

```text
Build verification (compile/package check) LÀ MỘT phần Foundation CI
  CHỈ khi implementation/executable artifact ĐÃ tồn tại VÀ existing
  authority yêu cầu nó (Chapter 13 tier-resolution, `module-
  registry.yaml`) — verify trực tiếp tại boundary transaction này: 0
  module đã build (Scale Check pattern nhất quán xuyên Phase 1.5),
  KHÔNG executable artifact nào tồn tại trong repository.
Tài liệu này KHÔNG author concrete build-verification mechanism tại
  v0.1 này — CHỈ pin nguyên tắc: khi implementation ground truth xuất
  hiện (Phase 3+, module đầu tiên build), build verification convention
  cụ thể (build command, target, output check) PHẢI author dưới ĐÚNG
  authority này (`ci-cd.md`, version bump reversible), KHÔNG tự động
  suy đoán trước tại đây.
```

## 13. Provider/operator VÀ workflow implementation — deferred

```text
Verify trực tiếp tại transaction này: KHÔNG CI provider/operator cụ
  thể nào (GitHub Actions, GitLab CI, Jenkins, Buildkite, CircleCI,
  hay bất kỳ hệ thống nào khác) đã được authoritatively pin bởi bất kỳ
  existing authority (`ADR-030`, Chapter 13 §13.14 CHỈ defer mechanism,
  KHÔNG chọn) — `.github/` VÀ mọi CI workflow/provider config KHÔNG
  tồn tại trong repository tại boundary transaction này.
Repository đang host trên GitHub KHÔNG tự động ngụ ý chọn GitHub
  Actions — tài liệu này KHÔNG chọn provider CHỈ vì tiện lợi đó.
Provider/tool selection, workflow file cụ thể, concrete build system,
  package/artifact format VẪN deferred tới một transaction
  implementation-readiness riêng biệt tương lai — lựa chọn đó PHẢI tự
  verify trực tiếp KHÔNG tự thỏa lại Chapter 0 §4b (vd một provider
  choice có hard-to-reverse vendor lock-in đáng kể CÓ THỂ tự trigger
  ADR riêng, KHÔNG tự động miễn trừ CHỈ vì `ADR-030` đã tồn tại).
```

## 14. Explainability/visibility

```text
Kết quả CI (pass/fail/KHÔNG evaluate được, §5) PHẢI visible/traceable
  — operator/developer PHẢI xác định được: check nào chạy, kết quả gì,
  liên quan tới thay đổi nào (§9's "propose integration" trigger).
Tài liệu này KHÔNG mandate một tooling/dashboard cụ thể để đạt
  visibility đó — CHỈ yêu cầu khả năng đó PHẢI tồn tại, implementation
  detail deferred (§13).
```

## 15. Authority boundaries

```text
Chapter 12 (Approval Gates)  VẪN authority DUY NHẤT cho Approval Gate
                        semantics/Product Owner authority (§1 trên,
                        KHÔNG đổi).
Chapter 13 (Quality Gates)   VẪN authority DUY NHẤT cho quality
                        dimension/coverage-tier/gate applicability/
                        pass-fail/evidence contract/waiver semantics
                        (§4/§5/§8 trên, KHÔNG đổi). Chapter 13 §13.10
                        VẪN authority DUY NHẤT cho flaky-test policy
                        (§7 trên, KHÔNG đổi).
Testing Convention (`testing.md`, Approved)  VẪN authority cho test
                        structure/naming/isolation/flaky-test-
                        quarantine tooling mechanics (§7 trên, KHÔNG
                        đổi).
Coding Standard/Naming/Logging/Config/Error Handling (Approved)  VẪN
                        authority riêng từng category (§3 trên, KHÔNG
                        đổi).
ADR-017                VẪN authority DUY NHẤT cho Custody & Signing
                        Trust Boundary (§11 trên, KHÔNG đổi).
module-registry.yaml   VẪN authority DUY NHẤT cho module identity/
                        dependency graph — KHÔNG đổi module identity/
                        edge nào.
ADR-008/ADR-024/monorepo.md  VẪN authority ngôn ngữ/repository
                        topology — KHÔNG đổi.
Phase 7 — Deployment (Chapter 14 §14.2)  VẪN authority riêng cho
                        deployment/promotion/release, downstream —
                        tài liệu này KHÔNG preempt, KHÔNG bypass
                        sequence đó.
LIVE execution authorization  VẪN NGOÀI phạm vi tài liệu này — KHÔNG
                        authorize LIVE, KHÔNG gán một authority cụ thể
                        nào tại đây (đúng `ADR-030` v0.3, KHÔNG
                        redefine). Account `environment: LIVE` KHÔNG
                        tự nó authorize platform LIVE execution.
```

## Non-goals (KHÔNG chọn/redefine tại v0.1 này)

```text
CI provider/operator cụ thể (GitHub Actions/GitLab CI/Jenkins/
  Buildkite/CircleCI/khác);
workflow file/syntax implementation cụ thể;
concrete build system;
package/artifact format cụ thể;
container registry;
deployment platform;
infrastructure-as-code selection;
release/tagging strategy;
environment promotion;
production deployment;
LIVE authorization;
secret manager/KMS/Vault/HSM selection cụ thể;
quality criteria mới/coverage-tier policy mới (Chapter 13 CHỈ sở hữu);
testing semantics mới (`testing.md` CHỈ sở hữu);
governance/approval process mới (Chapter 12 CHỈ sở hữu);
affected-area detection algorithm/caching strategy/concurrency limit
  cụ thể.
```

## ADR-scope disposition

```text
Tài liệu này (`ci-cd.md` v0.1) implement living-detail authority ĐÃ
  được `ADR-030` v0.3 (`Approved`) explicitly delegate — KHÔNG một mục
  nào tại §1–§14 trên tự nó tạo một quyết định >1-module hay khó đảo
  ngược MỚI vượt ngoài phạm vi ADR-030 đã Approved. Mọi rule tại đây
  LÀ reversible detail-level convention (orchestration mechanics,
  inheritance boundary, evidence hand-off, trigger organization,
  visibility) — KHÔNG mở rộng scope sang CD/deployment/LIVE dưới bất
  kỳ hình thức nào.
KHÔNG rule nào tại v0.1 này độc lập trigger Chapter 0 §4b ngoài phạm
  vi ADR-030 đã cover — KHÔNG tạo ADR-031 tại transaction này.
Mọi thay đổi SEMANTIC tương lai vào tài liệu này (KHÔNG PHẢI mọi sửa —
  CHỈ khi đổi Ý NGHĨA rule, vd mở rộng scope sang deployment/mở rộng
  sang provider selection có hard-to-reverse lock-in đáng kể) PHẢI tự
  chạy lại ADR Scope Rule (Chapter 0 §4b) hiện hành TẠI chính thời
  điểm đổi — KHÔNG suy diễn "reversible/refactor-class" LÀ đủ để miễn
  ADR (đúng lesson `ADR-025`–`ADR-030` §3, KHÔNG redefine).
```

## Change history

```text
v0.1  2026-08-13  Established — vai trò: `Phase 1.5 CI/CD Convention
      v0.1 Authoring Executor`. Bounded EF-TXN-002 category transaction
      (CI/CD only, CI-side CHỈ, KHÔNG CD/deployment). Authored dưới
      authority `ADR-030` v0.3 (`Approved`, blob
      e02853e2ad21e14cf679099480397344c6bcf3c7). Verify trực tiếp
      trước khi author: current HEAD
      (907c0aa651fec51f1062357e94aeac732a1915ab),
      `docs/engineering/ci-cd.md` KHÔNG tồn tại trước đây, `.github/`
      VÀ mọi CI workflow/provider config KHÔNG tồn tại, 0 module đã
      build (KHÔNG executable artifact nào). Established 15 mục: CI
      purpose/authority boundary (CI success ≠ approval/phase
      transition, CI failure ≠ rejection), validation/lint/test/build-
      check orchestration, inheritance từ Coding Standard/Naming/
      Logging/Config/Error Handling/Testing (KHÔNG invent rule mới),
      Chapter 13 quality/evidence boundary (KHÔNG invent criteria/đổi
      coverage/reinterpret pass-fail), fail-safe khi required check
      KHÔNG evaluate được (fail-closed, đúng Chapter 13 §13.8), local-
      vs-CI logical parity, test/quarantine interaction (Chapter 13
      §13.10 policy vs `testing.md` §12 tooling mechanics, tách bạch
      tường minh đúng ADR-030 §6), evidence hand-off mechanics (KHÔNG
      competing schema với Chapter 13 §13.9), provider-neutral trigger/
      check organization, affected-area/caching/concurrency (chỉ khi
      có ích, conservative, cơ chế cụ thể deferred), ADR-017/Config
      secret boundary (KHÔNG custody authority mới, credential
      mechanism deferred), build verification (CHỈ khi ground truth
      tồn tại — hiện tại 0 module, deferred), provider/operator/
      workflow implementation deferred (KHÔNG chọn GitHub Actions dù
      repo host trên GitHub), explainability/visibility, authority
      boundaries. Non-goals liệt kê tường minh. ADR-scope disposition:
      v0.1 implement living-detail authority ĐÃ delegate bởi ADR-030,
      KHÔNG rule nào độc lập trigger Chapter 0 §4b mới, KHÔNG tạo
      ADR-031. KHÔNG chạm `ADR-030` (Approved, immutable)/Chapter 12/
      Chapter 13/`ADR-017`/`ADR-025`–`ADR-029`/`coding-standard.md`/
      `naming.md`/`logging.md`/`config.md`/`error-handling.md`/
      `testing.md`/`ADR-008`/`ADR-024`/`monorepo.md`/`module-
      registry.yaml`/Constitution/Phase 1.5 rules. `EF-CONFIG-B-MIN-01`
      VÀ `EF-ERR-B-MIN-01` KHÔNG chạm, KHÔNG đóng. KHÔNG tạo workflow
      file/provider config/deployment configuration nào. `status:
      Draft` — not self-approved (`G-ORCH-002`). KHÔNG authorize
      deployment/Phase 2/LIVE.
```
