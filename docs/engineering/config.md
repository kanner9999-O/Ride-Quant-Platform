---
id: engineering-config
title: "Engineering Foundation — Config Convention"
version: "0.1"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-11"
last_review: null
next_review: null
depends_on: ["../constitution/03-engineering-principles", "../adr/ADR-008", "../adr/ADR-028", "../adr/ADR-017", "logging", "naming", "coding-standard"]
---

# Engineering Foundation — Config Convention

**Vai trò của tài liệu này:** convention document THỨ NĂM của Phase 1.5 — Engineering Foundation (Chapter 3 §3.2), phạm vi CHỈ category **Config** (Chapter 14 §14.2's Phase 1.5 scope list) — đúng `EF-TXN-002` (một category = một transaction bounded). **`ADR-028` v0.2 (Approved 2026-08-11) LÀ authority cho chính việc CÓ một cross-module Config Convention baseline bắt buộc** — tài liệu này LÀ living convention chứa chi tiết rule reversible dưới authority đó, KHÔNG lặp lại decision text của ADR-028. KHÔNG Constitution chapter, KHÔNG ADR, KHÔNG redefine Module Taxonomy/dependency graph/ngôn ngữ allocation/Coding Standard/Naming Convention/Logging Convention/Custody & Signing Trust Boundary — `module-registry.yaml` VẪN authority module identity/dependency, `ADR-008` VẪN authority ngôn ngữ, `ADR-024`/`monorepo.md` VẪN authority repository topology, `ADR-025`/`coding-standard.md` VẪN authority Coding Standard, `ADR-026`/`naming.md` VẪN authority identifier naming, `ADR-027`/`logging.md` VẪN authority Logging, `ADR-017` VẪN authority architecture-level Custody & Signing Trust Boundary. Mọi thay đổi SEMANTIC tương lai vào tài liệu này PHẢI tự chạy lại ADR Scope Rule (Chapter 0 §4b) hiện hành TẠI chính thời điểm đổi — reversibility của kỹ thuật thay đổi KHÔNG hủy/miễn vế ">1 module" nếu vế đó đã thỏa (đúng lesson `ADR-025`/`ADR-026`/`ADR-027`/`ADR-028` §3, KHÔNG redefine — xem §15 dưới).

## 1. Configuration model

```text
Configuration LÀ externally-supplied operational/runtime setting (vd
  endpoint, timeout, feature toggle, environment identity, credential
  REFERENCE) — KHÔNG PHẢI domain fact, KHÔNG PHẢI authoritative
  business state.
Configuration KHÔNG được trở thành một nguồn sự thật thay thế cho:
  Domain Contract state (`/docs/domain/`);
  Event Contract meaning;
  API contract meaning;
  module identity/dependency (`module-registry.yaml`);
  execution/replay/audit evidence.
Một giá trị config CÓ THỂ ẢNH HƯỞNG hành vi runtime (vd bật/tắt một
  capability, chọn timeout) NHƯNG KHÔNG tự nó tạo/redefine domain
  semantics — vd config KHÔNG được dùng để "quyết định" một Order LÀ
  gì, hay một event nghĩa LÀ gì; đó VẪN thuộc Domain/Event Contract
  authority DUY NHẤT.
```

## 2. Source precedence

```text
MỘT deterministic precedence model, technology-neutral, áp dụng xuyên
  module (thứ tự ưu tiên GIẢM DẦN — nguồn sau CHỈ override nguồn trước
  khi nguồn sau THỰC SỰ cung cấp giá trị, KHÔNG override bằng giá trị
  rỗng/absent):

  1. built-in safe default (hard-coded trong code, an toàn nhất,
     KHÔNG execution/security-sensitive permissive default — xem §4);
  2. config file (nếu module/runtime hỗ trợ — format cụ thể KHÔNG
     chọn tại đây, xem Non-goals);
  3. environment variable (nếu module/runtime hỗ trợ);
  4. command-line/runtime override (nếu module/runtime hỗ trợ,
     explicit tại thời điểm khởi động/invocation).

Một module/runtime KHÔNG bắt buộc hỗ trợ TẤT CẢ bốn source class trên
  — module CÓ THỂ chỉ hỗ trợ một tập con (vd chỉ built-in default +
  environment variable). NẾU một source class KHÔNG được hỗ trợ bởi
  module/runtime đó, nó PHẢI bị BỎ QUA hoàn toàn khỏi precedence chain
  của module đó — KHÔNG được silently thay đổi Ý NGHĨA thứ tự của các
  source class CÒN LẠI mà module đó CÓ hỗ trợ (vd nếu module KHÔNG hỗ
  trợ config file, environment variable VẪN override built-in default
  đúng thứ tự trên, KHÔNG nhảy vị trí).
Tài liệu này KHÔNG chọn remote config service/vendor nào (Non-goals) —
  nếu một remote config source được thêm tương lai, vị trí của nó
  trong precedence chain LÀ một semantic decision cần tự rerun ADR
  Scope Rule (§15).
```

## 3. Environment variables

```text
Mọi environment variable dùng cho configuration PHẢI có quan hệ
  explicit, deterministic với đúng MỘT canonical config key — KHÔNG
  ambiguous alias (hai tên biến môi trường khác nhau trỏ tới CÙNG một
  config key mà KHÔNG có lý do kỹ thuật rõ ràng, vd backward-
  compatibility đã ghi lại), KHÔNG silent fallback giữa hai tên biến
  KHÔNG liên quan (vd đọc `DB_HOST` khi `DATABASE_HOST` absent mà
  KHÔNG document quan hệ đó tường minh).
Giá trị environment variable (LUÔN LUÔN string ở tầng OS) PHẢI được
  parse/validate thành typed configuration value (§6) TRƯỚC KHI business
  logic tiêu thụ nó — business logic KHÔNG BAO GIỜ đọc trực tiếp raw
  environment-variable string chưa qua validation.
Tài liệu này KHÔNG redefine general identifier naming authority
  (`ADR-026`/`naming.md` VẪN authority DUY NHẤT cho identifier naming
  convention) — CHỈ pin semantic rule về deterministic mapping/KHÔNG
  ambiguous alias PHÍA TRÊN naming convention đó, KHÔNG chọn casing
  convention riêng cho environment-variable name tại đây.
```

## 4. Defaults

```text
Default value cho một config key PHẢI explicit VÀ documented (tại code
  hoặc tài liệu module tương ứng) — KHÔNG default "ngầm" chỉ tồn tại
  trong đầu người viết code.
Setting unsafe/security-sensitive/execution-sensitive (vd credential
  handling, execution-suspension/kill-switch observation, custody/
  signing interaction, LIVE-vs-PAPER environment selection) KHÔNG được
  gán permissive default CHỈ VÌ convenience (vd KHÔNG default "cho
  phép LIVE" hay "bỏ qua kill-switch observation" — mọi giá trị loại
  này PHẢI yêu cầu explicit configuration, fail-closed nếu absent, xem
  §7).
Sự vắng mặt (absence) của một required value PHẢI PHÂN BIỆT được với
  một giá trị đã configure explicit (vd absence ≠ empty string ≠ zero
  ≠ false một cách ngầm định) — implementation PHẢI có cách xác định
  "giá trị này CHƯA được cung cấp" tách biệt khỏi "giá trị này ĐÃ được
  cung cấp VÀ LÀ falsy."
Tài liệu này KHÔNG invent concrete trading/risk default nào (vd KHÔNG
  chọn default risk limit, default order size...) — những giá trị đó
  (nếu cần) thuộc domain/business authority riêng, KHÔNG tại Config
  Convention.
```

## 5. Required / optional semantics

```text
Mỗi config key PHẢI có required/optional semantics RÕ RÀNG, xác định
  bởi CHÍNH module sở hữu việc sử dụng key đó (KHÔNG một registry
  trung tâm nào quyết định required/optional cho MỌI module — mỗi
  module tự biết key nào nó cần).
KHÔNG implicit "missing means false/zero/empty" — nếu một key optional
  VÀ absent, hành vi PHẢI LÀ default đã document (§4), KHÔNG PHẢI suy
  diễn ngầm từ absence. Nếu một key required VÀ absent, đó LÀ một
  validation failure (§6)/startup failure (§7), KHÔNG PHẢI âm thầm coi
  LÀ falsy.
```

## 6. Validation

```text
Configuration PHẢI được validate TRƯỚC KHI business logic tiêu thụ nó
  — validation bao gồm tối thiểu:
  type validation       (giá trị parse đúng type mong đợi — int,
                         bool, string, enum, duration...);
  range/domain validation (khi applicable — vd một timeout PHẢI > 0,
                         một enum value PHẢI thuộc tập giá trị hợp
                         lệ đã document);
  malformed/unrecognized value behavior (giá trị KHÔNG parse được
                         PHẢI fail validation tường minh, KHÔNG
                         silently coerce về một giá trị "gần đúng");
  unknown-key policy    (config key KHÔNG được module nhận diện —
                         module PHẢI có policy rõ ràng, documented,
                         cho việc bỏ qua có log hay reject — KHÔNG
                         silent ignore KHÔNG ghi nhận gì).
Kết quả validation PHẢI deterministic — CÙNG input config PHẢI luôn
  cho CÙNG kết quả validation (pass/fail VÀ giá trị đã parse), KHÔNG
  phụ thuộc thứ tự đọc source hay timing.
Tài liệu này KHÔNG thiết kế Error Handling exception hierarchy (thuộc
  category riêng, Chapter 14 §14.2, chưa mở tại transaction này) — CHỈ
  yêu cầu validation PHẢI xảy ra VÀ deterministic, KHÔNG định nghĩa
  cách raise/propagate lỗi đó.
```

## 7. Startup / activation boundary

```text
Khi required startup configuration invalid/missing/malformed, module
  NÊN fail closed — KHÔNG khởi động/tiếp tục thực hiện responsibility
  chính của nó — TẠI những trường hợp module KHÔNG THỂ an toàn thực
  hiện responsibility đó với configuration invalid (vd một module
  custody/signing/execution-sensitive KHÔNG THỂ khởi động thiếu
  credential-reference hợp lệ).
Phân biệt: một capability CỤ THỂ bị disable (vd một optional feature
  KHÔNG được kích hoạt tại environment này) CÓ THỂ hợp lệ THIẾU config
  key liên quan riêng tới capability đó — required/optional semantics
  (§5) áp dụng THEO capability đang active, KHÔNG PHẢI một rule toàn
  cục "mọi key PHẢI luôn có mặt."
Tài liệu này KHÔNG absorb Error Handling category (retry/recovery
  policy, exception hierarchy) — CHỈ pin nguyên tắc fail-closed tại
  activation boundary, KHÔNG định nghĩa CÁCH module recover/retry sau
  startup failure.
```

## 8. Secrets boundary

```text
Configuration CÓ THỂ mang một reference/locator/identifier cho secret-
  related material (vd `credential_reference` — account.md/ADR-012,
  KHÔNG đổi tại đây) TẠI những nơi authority hiện hành đã cho phép
  reference đó tồn tại — Config Convention KHÔNG tự tạo một secret-
  reference scheme mới ngoài những gì Domain Contract/ADR-017 đã
  established.
Ordinary application config (file/environment variable/CLI override
  thông thường) KHÔNG được chứa raw exchange credential hay private
  signing material — đúng `ADR-017` §3.1/§11 (custody-signing-service
  LÀ module DUY NHẤT được phép sử dụng exchange credential trực tiếp,
  KHÔNG BAO GIỜ trả raw secret cho caller) VÀ `ADR-028` §3/§6 (Config
  Convention KHÔNG redefine/absorb custody/signing authority đó).
KHÔNG log giá trị secret (đúng `logging.md` §8 — baseline prohibition
  secrets/credentials/token/private auth material, KHÔNG redefine tại
  đây, CHỈ tái khẳng định áp dụng cho config-related log, xem §14
  dưới).
KHÔNG persist raw secret vào config file/example/sample config trong
  repository — mọi ví dụ config trong tài liệu implementation tương
  lai PHẢI dùng placeholder, KHÔNG giá trị thật.
`custody-signing-service`'s direct-credential-use/custody-signing
  authority giữ NGUYÊN VẸN ĐÚNG như `ADR-017` định nghĩa (§3.1) — tài
  liệu này KHÔNG redefine, KHÔNG absorb, KHÔNG làm suy yếu authority
  đó. `module-registry.yaml` KHÔNG tự nó tạo custody/signing authority
  — authority đó thuộc `ADR-017`, KHÔNG suy diễn từ registry (đúng
  lesson `EF-LOG-A-MAJ-03`/`ADR028-A-MAJ-01`, tái khẳng định tại đây,
  KHÔNG redefine).
Tài liệu này KHÔNG chọn Vault/KMS/HSM/secret manager/backend cụ thể
  nào (Non-goals) — concrete mechanism đó VẪN deferred/unresolved,
  CHÍNH `ADR-017` (§3.3/§14 gap #1) đã forbidden scope những mục đó.
Tài liệu này KHÔNG redefine credential custody/rotation/signing
  protocol — những mục đó VẪN thuộc `ADR-017`, KHÔNG tại Config
  Convention.
```

## 9. Environment-specific configuration

```text
Config Convention cho phép semantic handling khác nhau theo môi
  trường vận hành (dev/test/staging/production-like, VÀ PAPER/LIVE
  đúng `account.md` §8 environment enum, KHÔNG đổi) — KHÔNG hardcode
  deployment topology cụ thể (container platform, orchestration,
  network layout — Non-goals) vào chính semantic đó.
Behavior khác biệt xuyên môi trường PHẢI explicit VÀ documented tại
  đúng config key/category liên quan — KHÔNG hidden behavior
  difference (vd một module KHÔNG được tự động thay đổi business logic
  chỉ vì "đang chạy tại staging" mà KHÔNG có config key tương ứng
  explicit).
Environment KHÔNG được silently thay đổi business semantics TRỪ KHI
  explicitly configured VÀ authorized qua đúng authority hiện hành
  (vd chuyển PAPER sang LIVE KHÔNG BAO GIỜ tự động qua config — đúng
  `account.md` §8/`ADR-007` "Live execution authorization là quyết
  định governance riêng," KHÔNG đổi tại đây).
Tài liệu này KHÔNG authorize LIVE execution dưới bất kỳ hình thức nào
  — quyết định đó VẪN thuộc một governance transaction riêng biệt,
  hoàn toàn ngoài phạm vi Config Convention.
```

## 10. Overrides

```text
Override (command-line/runtime, §2 mức 4) PHẢI deterministic — CÙNG
  tập override input PHẢI luôn cho CÙNG effective configuration value,
  KHÔNG phụ thuộc thứ tự invocation ngẫu nhiên.
Implementation PHẢI có khả năng xác định (provenance/explainability)
  ĐÚNG nguồn nào (built-in default/config file/environment variable/
  override) đã cung cấp effective value cho MỖI config key — mức độ
  chi tiết cụ thể (log, introspection API, debug dump...) KHÔNG được
  quyết định tại đây (implementation detail), CHỈ yêu cầu khả năng đó
  PHẢI tồn tại.
Tài liệu này KHÔNG yêu cầu một observability vendor cụ thể nào để đạt
  provenance đó (Non-goals) — có thể đơn giản LÀ log tại startup (§14)
  hay một introspection API nội bộ, KHÔNG chọn mechanism tại đây.
```

## 11. Reloadability

```text
Tài liệu này KHÔNG mandate hot-reload cho MỌI config key/category —
  hot-reload LÀ một khả năng CÓ THỂ áp dụng CHỌN LỌC, KHÔNG một yêu
  cầu toàn cục.
Mỗi config key/category PHẢI được PHÂN LOẠI rõ ràng (bởi module sở
  hữu nó) vào MỘT trong ba nhóm:
  requires restart          (thay đổi CHỈ có hiệu lực sau khi restart
                             process — an toàn nhất, default hợp lý
                             cho setting execution/security-sensitive);
  may be reloaded safely     (thay đổi CÓ THỂ áp dụng khi process đang
                             chạy, MIỄN LÀ module đã implement reload
                             logic tương ứng — KHÔNG tự động giả định);
  immutable during process lifetime (thay đổi KHÔNG được áp dụng dưới
                             bất kỳ hình thức nào cho tới khi process
                             mới khởi động, dù có "reload" hay không —
                             khác "requires restart" ở chỗ đây LÀ một
                             invariant kiến trúc, KHÔNG PHẢI giới hạn
                             implementation hiện tại).
Tài liệu này KHÔNG thiết kế mechanism reload cụ thể (file watcher,
  signal handler, polling...) — CHỈ yêu cầu phân loại rõ ràng PHẢI tồn
  tại cho mỗi key/category (implementation detail deferred).
```

## 12. Local development

```text
Local-development convenience (vd một `.env`-style file cho máy dev cá
  nhân, default rộng hơn cho một số setting non-sensitive) ĐƯỢC PHÉP
  bounded — MIỄN LÀ KHÔNG làm suy yếu production security/behavior
  semantics đã pin tại §4/§8/§9.
Local default/example config trong repository KHÔNG được chứa
  credential thật dưới bất kỳ hình thức nào (đúng §8) — CHỈ placeholder
  rõ ràng LÀ placeholder.
Local-dev behavior KHÔNG được silently trở thành production behavior —
  một convenience CHỈ áp dụng khi environment explicit xác định LÀ
  local-dev (§9), KHÔNG tự động lan sang môi trường khác qua một default
  chung mập mờ.
```

## 13. Python / Go boundary

```text
Python VÀ Go (`ADR-008` pin ngôn ngữ theo layer) ĐƯỢC PHÉP dùng
  idiomatic config library/API riêng của chính ngôn ngữ đó — tài liệu
  này KHÔNG yêu cầu internal config object model hay library giống
  nhau xuyên hai ngôn ngữ.
Yêu cầu DUY NHẤT: mỗi implementation PHẢI conform đúng SEMANTIC
  requirement chung tại §1–§12 trên (source precedence, environment-
  variable rule, defaults, required/optional, validation, startup
  boundary, secrets boundary, environment handling, override
  provenance, reloadability classification, local-dev boundary) —
  KHÔNG PHẢI identical syntax/API/object shape.
Tài liệu này KHÔNG chọn config library cụ thể cho Python HAY Go tại
  transaction này (Non-goals) — lựa chọn library cụ thể thuộc một
  transaction implementation-readiness riêng, KHÔNG tại đây.
```

## 14. Logging / explainability interaction

```text
Config-related log (khi module log về configuration của chính nó, vd
  tại startup) CÓ THỂ report:
  config source category (built-in default/config file/environment
    variable/override — §2/§10, KHÔNG cần chi tiết implementation);
  key identity (canonical config key name, KHÔNG raw environment-
    variable string nếu khác tên);
  validation/result status (pass/fail, KHÔNG giá trị nếu giá trị đó
    LÀ secret-related, xem dưới).
Config-related log KHÔNG BAO GIỜ expose giá trị secret (§8) — đúng
  `logging.md` §8 baseline prohibition, KHÔNG redefine tại đây, CHỈ
  tái khẳng định áp dụng nhất quán cho config-related log cụ thể.
Tài liệu này KHÔNG redefine Logging level semantics hay field model
  (`ADR-027`/`logging.md` VẪN authority DUY NHẤT) — CHỈ pin nguyên tắc
  what-may-be-logged cho chính config context, KHÔNG chọn level nào
  PHẢI dùng.
```

## 15. Authority boundaries

```text
ADR-017                VẪN authority DUY NHẤT cho architecture-level
                        Custody & Signing Trust Boundary —
                        custody-signing-service's direct-credential-use
                        authority giữ nguyên vẹn (§8 trên, KHÔNG
                        redefine).
module-registry.yaml   VẪN authority DUY NHẤT cho module identity/
                        dependency graph — KHÔNG đổi module identity/
                        edge nào, KHÔNG tạo module→config mapping.
ADR-008                VẪN authority DUY NHẤT cho ngôn ngữ theo layer.
ADR-024 / monorepo.md  VẪN authority DUY NHẤT cho repository topology.
ADR-025 / coding-standard.md  VẪN authority cho Coding Standard —
                        Config KHÔNG absorb formatting/lint/dependency.
ADR-026 / naming.md    VẪN authority cho identifier naming — Config
                        KHÔNG redefine naming convention (§3 trên CHỈ
                        pin semantic mapping rule, KHÔNG casing).
ADR-027 / logging.md   VẪN authority cho Logging — Config KHÔNG
                        redefine logging semantics (§14 trên).
Domain/Event/API contract authority (/docs/domain/)  VẪN authority
                        DUY NHẤT cho event/domain/API existence/schema/
                        meaning — Config Convention KHÔNG invent
                        canonical domain/event/API nào (§1 trên).
Error Handling          category riêng, chưa mở — Config KHÔNG absorb
                        exception hierarchy/retry policy (§6/§7 trên
                        CHỈ pin validation/fail-closed principle).
CI/CD                   category riêng, chưa mở — Config KHÔNG absorb
                        pipeline/enforcement mechanism.
Deployment mechanism    (container orchestration, platform, topology)
                        — KHÔNG chọn tại đây (Non-goals), tách biệt
                        khỏi Config semantic content.
```

## Non-goals (KHÔNG chọn tại v0.1 này)

```text
dotenv/Pydantic/Viper/Cobra hay bất kỳ library cụ thể khác;
YAML/JSON/TOML/.env hay bất kỳ format cụ thể LÀM canonical config
  format;
Vault/KMS/HSM/secret manager cụ thể;
remote config service;
feature-flag vendor;
container orchestration platform;
deployment platform/pipeline;
config schema technology (JSON Schema, protobuf...);
hot-reload mechanism cụ thể (file watcher, signal, polling...).
```

## ADR-scope disposition

```text
Tài liệu này (`config.md` v0.1) implement living-detail authority ĐÃ
  được cấp sẵn bởi `ADR-028` v0.2 (`Approved`) — KHÔNG một mục nào tại
  §1–§14 trên tự nó tạo một quyết định >1-module hay khó đảo ngược MỚI
  vượt ngoài phạm vi ADR-028 đã Approved. Mọi rule tại đây LÀ reversible
  detail-level convention (source precedence, env-var mapping,
  defaults, validation, reloadability classification...), đúng loại
  nội dung ADR-028 §3 đã explicitly defer tới `config.md`.
KHÔNG rule nào tại v0.1 này độc lập trigger Chapter 0 §4b ngoài phạm
  vi đã ADR-028 đã cover — KHÔNG tạo ADR-029 tại transaction này.
Mọi thay đổi SEMANTIC tương lai vào tài liệu này (KHÔNG PHẢI mọi sửa —
  CHỈ khi đổi Ý NGHĨA rule) PHẢI tự chạy lại ADR Scope Rule (Chapter 0
  §4b) hiện hành TẠI chính thời điểm đổi — KHÔNG suy diễn "reversible/
  refactor-class" LÀ đủ để miễn ADR (đúng lesson `ADR-025`/`ADR-026`/
  `ADR-027`/`ADR-028` §3, KHÔNG redefine). Vì baseline áp dụng cho MỌI
  module, phần lớn semantic update sẽ thỏa lại vế ">1 module" — Config
  KHÔNG generally "ADR Not Required."
```

## Change history

```text
v0.1  2026-08-11  Established — vai trò: `Phase 1.5 Config Convention
      v0.1 Authoring Executor`. Bounded EF-TXN-002 category transaction
      (Config only). Verify trực tiếp trước khi author: current HEAD
      (7f3559a34079f9a1c522f030732c00470dc67285), ADR-028 v0.2 Approved
      identity (blob 016fbe8786d7e5df5609579d8aeea7ffb1f06178),
      `docs/engineering/config.md` KHÔNG tồn tại trước đây. Established
      15 mục: configuration model (KHÔNG PHẢI domain fact/authoritative
      state), source precedence (built-in default → config file →
      environment variable → runtime override, technology-neutral,
      source class KHÔNG bắt buộc hỗ trợ toàn bộ), environment
      variables (deterministic mapping, KHÔNG ambiguous alias, parse
      trước khi dùng), defaults (explicit/documented, KHÔNG permissive
      default cho sensitive setting, absence phân biệt khỏi explicit
      value), required/optional semantics (module sở hữu key tự định
      nghĩa, KHÔNG implicit missing-means-falsy), validation (type/
      range/malformed/unknown-key, deterministic, KHÔNG thiết kế Error
      Handling hierarchy), startup/activation boundary (fail-closed
      cho required invalid config, phân biệt disabled-capability CASE,
      KHÔNG absorb retry/recovery policy), secrets boundary (align
      ADR-017/ADR-028 — reference/locator được phép, raw credential
      KHÔNG được phép trong ordinary config, KHÔNG log secret, KHÔNG
      persist secret vào example, custody-signing-service authority
      nguyên vẹn, KHÔNG chọn Vault/KMS/HSM), environment-specific
      configuration (dev/test/staging/production/PAPER/LIVE semantic
      handling KHÔNG hardcode topology, KHÔNG silent semantic change,
      KHÔNG authorize LIVE), overrides (deterministic, provenance
      required, KHÔNG chọn observability vendor), reloadability (KHÔNG
      mandate hot-reload toàn cục, phân loại ba nhóm mỗi key/category),
      local development (bounded convenience, KHÔNG credential thật,
      KHÔNG silent production leakage), Python/Go boundary (idiomatic
      library riêng, semantic conformance CHỈ, KHÔNG chọn library),
      logging/explainability interaction (report source/key/status,
      KHÔNG secret value, KHÔNG redefine Logging Convention), authority
      boundaries (ADR-017/module-registry/ADR-008/ADR-024/monorepo.md/
      ADR-025/coding-standard.md/ADR-026/naming.md/ADR-027/logging.md/
      Domain-Event-API/Error Handling/CI-CD/deployment — tất cả preserved
      riêng biệt). Non-goals liệt kê tường minh (KHÔNG library/format/
      secret-manager/remote-config/feature-flag-vendor/orchestration/
      deployment/schema-tech/reload-mechanism nào chọn). ADR-scope
      disposition: v0.1 implement living-detail authority ĐÃ cấp sẵn
      bởi ADR-028, KHÔNG rule nào độc lập trigger Chapter 0 §4b mới,
      KHÔNG tạo ADR-029 tại transaction này. KHÔNG chạm `ADR-028`/
      `ADR-017` (Approved, immutable)/`ADR-027`/`logging.md`/`ADR-026`/
      `naming.md`/`ADR-025`/`coding-standard.md`/`ADR-024`/
      `monorepo.md`/`ADR-008`/`module-registry.yaml`/Security & Custody
      architecture/Constitution/Phase 1.5 rules. KHÔNG bắt đầu Error
      Handling/Testing/CI-CD. `status: Draft` — not self-approved
      (`G-ORCH-002`). KHÔNG authorize Phase 2/LIVE.
```
