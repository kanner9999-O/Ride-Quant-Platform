---
id: engineering-config
title: "Engineering Foundation — Config Convention"
version: "0.2"
status: Approved
owner: Product Owner
reviewers: []
approved_by: Product Owner
approved_at: "2026-08-11"
created_at: "2026-08-11"
last_review: null
next_review: null
depends_on: ["../constitution/03-engineering-principles", "../adr/ADR-008", "../adr/ADR-028", "../adr/ADR-017", "logging", "naming", "coding-standard"]
---

# Engineering Foundation — Config Convention

**APPROVED (2026-08-11) — status: Draft → Approved.** Product Owner decision: **"APPROVE CONFIG CONVENTION V0.2 — ACCEPT EF-CONFIG-B-MIN-01 AS NON-BLOCKING RESIDUAL."** Reviewed candidate: v0.2, blob `805bd9a351d1792e5d9283ea0f4989129aa36295`. `version: "0.2"` KHÔNG đổi (pure mechanical lifecycle approval — KHÔNG bump). Tài liệu này VẪN LÀ living document (Chapter 3 §3.2 "tài liệu SỐNG, không bất biến"; Chapter 0 §7.1 lifecycle Draft→...→Approved→Locked) — `Approved` KHÔNG đồng nghĩa immutable byte-for-byte như ADR (Chapter 11 §11.3 KHÔNG áp dụng ở đây); thay đổi tương lai vẫn hợp lệ qua version bump + re-review (Chapter 0 §8), VÀ mọi thay đổi SEMANTIC PHẢI tự rerun ADR Scope Rule đúng §15.

**Review evidence tại approval này:**

```text
Đóng (trước approval, v0.2): EF-CONFIG-A-MAJ-01.

Bounded Review A re-review trên v0.2:
  EF-CONFIG-A-MAJ-01: CLOSED
  New Blocker 0 / New Major 0 / New Minor 0
  CLEAN — READY_FOR_INDEPENDENT_REVIEW_B

Independent Review B trên đúng v0.2:
  EF-CONFIG-A-MAJ-01: CLOSED
  New Blocker 0 / New Major 0 / New Minor 1

  EF-CONFIG-B-MIN-01: candidate-identity/provenance wording VẪN stale
    tại — mục "Non-goals" heading (nói "v0.1"), "ADR-scope disposition"
    (tham chiếu "config.md v0.1"/"v0.1"). Finding VALID, non-blocking.

  Verdict: READY_FOR_PRODUCT_OWNER_DECISION
```

**`EF-CONFIG-B-MIN-01`: VẪN `OPEN — accepted non-blocking residual`** — Product Owner chấp nhận LÀM residual tại chính approval này, KHÔNG sửa/KHÔNG đóng tại transaction này (correction riêng biệt, nếu thực hiện, sẽ đóng finding này sau, KHÔNG tại đây). Stale "v0.1" wording tại mục "Non-goals" heading VÀ "ADR-scope disposition" GIỮ NGUYÊN KHÔNG sửa.

**Approval này KHÔNG đổi Config Convention semantics nào** (§1–§15 dưới byte-equivalent ngoài banner/lifecycle metadata/change history này, VÀ ngoài residual `EF-CONFIG-B-MIN-01` stale wording đã accept KHÔNG sửa) — KHÔNG chạm `ADR-028`/`ADR-017` (Approved, immutable)/`account.md`/`ADR-027`/`logging.md`/`ADR-026`/`naming.md`/`ADR-025`/`coding-standard.md`/`ADR-024`/`monorepo.md`/`ADR-008`/`module-registry.yaml`/Constitution/Phase 1.5 rules, KHÔNG tạo ADR-029, KHÔNG mở Error Handling/Testing/CI-CD category, KHÔNG chọn config/secret tooling, KHÔNG authorize Phase 2, KHÔNG authorize LIVE.

**Vai trò của tài liệu này:** convention document THỨ NĂM của Phase 1.5 — Engineering Foundation (Chapter 3 §3.2), phạm vi CHỈ category **Config** (Chapter 14 §14.2's Phase 1.5 scope list) — đúng `EF-TXN-002` (một category = một transaction bounded). **`ADR-028` v0.2 (Approved 2026-08-11) LÀ authority cho chính việc CÓ một cross-module Config Convention baseline bắt buộc** — tài liệu này LÀ living convention chứa chi tiết rule reversible dưới authority đó, KHÔNG lặp lại decision text của ADR-028. KHÔNG Constitution chapter, KHÔNG ADR, KHÔNG redefine Module Taxonomy/dependency graph/ngôn ngữ allocation/Coding Standard/Naming Convention/Logging Convention/Custody & Signing Trust Boundary — `module-registry.yaml` VẪN authority module identity/dependency, `ADR-008` VẪN authority ngôn ngữ, `ADR-024`/`monorepo.md` VẪN authority repository topology, `ADR-025`/`coding-standard.md` VẪN authority Coding Standard, `ADR-026`/`naming.md` VẪN authority identifier naming, `ADR-027`/`logging.md` VẪN authority Logging, `ADR-017` VẪN authority architecture-level Custody & Signing Trust Boundary. Mọi thay đổi SEMANTIC tương lai vào tài liệu này PHẢI tự chạy lại ADR Scope Rule (Chapter 0 §4b) hiện hành TẠI chính thời điểm đổi — reversibility của kỹ thuật thay đổi KHÔNG hủy/miễn vế ">1 module" nếu vế đó đã thỏa (đúng lesson `ADR-025`/`ADR-026`/`ADR-027`/`ADR-028` §3, KHÔNG redefine — xem §15 dưới).

**v0.2 — bounded correction (2026-08-11), đóng `EF-CONFIG-A-MAJ-01`, vai trò: `Phase 1.5 Config v0.2 Bounded Correction Executor`.** v0.1 §4/§9 dùng "LIVE-vs-PAPER environment selection" LÀM ví dụ setting Config-owned cần explicit-config/fail-closed default, VÀ liệt kê PAPER/LIVE cùng cấp với deployment-style environment (dev/test/staging/production) — tạo alternate-source-of-truth ambiguity với `account.md` (Account authority: `environment` required, immutable, gán TẠI `AccountRegistered`, `account.md` §1/§8). Sửa: §4 bỏ ví dụ PAPER/LIVE khỏi danh sách Config-owned sensitive setting; §9 tách bạch tường minh — `Account.environment` VẪN LÀ domain value thuộc Account authority DUY NHẤT, Config KHÔNG own/derive/default/override/replace giá trị đó, source precedence (§2) KHÔNG BAO GIỜ được hiểu LÀ cách thay đổi `Account.environment`; Config VẪN CÓ THỂ định nghĩa operational setting được scope/condition bởi một giá trị ĐÃ authoritative, MIỄN LÀ KHÔNG tự đặt/suy diễn chính giá trị đó; configuration KHÔNG BAO GIỜ silently convert PAPER→LIVE; LIVE execution authorization VẪN LÀ quyết định governance riêng biệt. **KHÔNG đổi:** configuration model (§1, VẪN LÀ controlling principle, KHÔNG suy yếu), source precedence (§2), environment-variable mapping (§3), defaults policy ngoài ví dụ PAPER/LIVE đã bỏ (§4 phần còn lại), required/optional semantics (§5), validation (§6), startup/activation rule (§7), secrets boundary (§8), overrides (§10), reloadability (§11), local-development rules (§12), Python/Go boundary (§13), Logging interaction (§14), authority boundaries (§15), Non-goals, ADR-scope disposition, future ADR Scope Rule rerun requirement. KHÔNG chạm `account.md`/`ADR-028`/`ADR-017`/`ADR-007`. KHÔNG tạo ADR-029, KHÔNG redesign Account/environment semantics, KHÔNG authorize LIVE. `status` VẪN `Draft`.

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
  signing interaction) KHÔNG được gán permissive default CHỈ VÌ
  convenience (vd KHÔNG default "bỏ qua kill-switch observation" — mọi
  giá trị loại này PHẢI yêu cầu explicit configuration, fail-closed
  nếu absent, xem §7).

[v0.2 sửa, đóng `EF-CONFIG-A-MAJ-01`: v0.1 dùng "LIVE-vs-PAPER
  environment selection" LÀM ví dụ setting cần explicit-config/fail-
  closed NGAY TẠI ĐÂY — đọc được như Config Convention sở hữu/default/
  select giá trị đó. SAI: `Account.environment` (PAPER|LIVE) LÀ
  required, immutable domain value do Account authority (`account.md`
  §1/§8) gán TẠI `AccountRegistered`, KHÔNG PHẢI một Config-owned
  setting — Config KHÔNG own/derive/default/override/replace giá trị
  đó dưới bất kỳ hình thức nào (xem §9 dưới, chi tiết đầy đủ). Ví dụ đó
  bỏ khỏi danh sách trên.]
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
[v0.2 sửa, đóng `EF-CONFIG-A-MAJ-01`: v0.1 liệt kê "PAPER/LIVE đúng
  account.md §8 environment enum" NGAY TẠI cùng cấp với deployment-
  style environment (dev/test/staging/production) — ngụ ý Config
  Convention quản lý/sở hữu giá trị PAPER/LIVE đó cùng cách như một
  environment category thông thường, tạo alternate-source-of-truth
  ambiguity với Account domain authority. Sửa: tách bạch tường minh
  dưới đây — §1's nguyên tắc "configuration KHÔNG PHẢI domain fact"
  VẪN LÀ controlling principle, KHÔNG suy yếu.]

Config Convention cho phép semantic handling khác nhau theo môi
  trường vận hành kiểu deployment (dev/test/staging/production-like)
  — KHÔNG hardcode deployment topology cụ thể (container platform,
  orchestration, network layout — Non-goals) vào chính semantic đó.

`Account.environment` (PAPER|LIVE) LÀ required, immutable domain value
  thuộc Account authority DUY NHẤT (`account.md` §1 "environment BẮT
  BUỘC, BẤT BIẾN — gán tại `AccountRegistered`, KHÔNG tái gán sau đó";
  §8 closed enum, "KHÔNG tự authorize Live execution của platform") —
  Config Convention KHÔNG own, KHÔNG derive, KHÔNG default, KHÔNG
  override, KHÔNG replace giá trị đó dưới bất kỳ hình thức nào. Source
  precedence (§2 — config file/environment variable/runtime override)
  KHÔNG BAO GIỜ được hiểu LÀ một cách để thay đổi `Account.environment`
  đã authoritative — precedence đó CHỈ áp dụng cho Config-owned
  operational/runtime setting, KHÔNG áp dụng cho domain value thuộc
  authority khác.

Config CÓ THỂ định nghĩa operational/runtime setting được scope/
  condition bởi một giá trị ĐÃ authoritative (vd một module đọc một
  endpoint/timeout config khác nhau TÙY THEO `Account.environment` ĐÃ
  resolve từ Account authority tại runtime) — MIỄN LÀ existing
  authority (Account/`ADR-007`) cho phép việc đọc/condition đó, VÀ
  Config KHÔNG tự đặt/suy diễn/tạo ra chính giá trị PAPER/LIVE đó.

Behavior khác biệt xuyên deployment-style environment (dev/test/
  staging/production-like) PHẢI explicit VÀ documented tại đúng config
  key/category liên quan — KHÔNG hidden behavior difference (vd một
  module KHÔNG được tự động thay đổi business logic chỉ vì "đang chạy
  tại staging" mà KHÔNG có config key tương ứng explicit).

Configuration KHÔNG BAO GIỜ silently convert một Account PAPER thành
  LIVE hay ngược lại — đúng bất biến `account.md` §1 (đổi environment
  LÀ tạo Account khác, KHÔNG PHẢI một "nâng cấp" tại chỗ). LIVE
  execution authorization VẪN LÀ một quyết định governance riêng biệt,
  hoàn toàn tách khỏi Config Convention (`account.md` §8/`ADR-007`
  "Live execution authorization là quyết định governance riêng,"
  KHÔNG đổi tại đây).

Tài liệu này KHÔNG authorize LIVE execution dưới bất kỳ hình thức nào,
  KHÔNG invent một environment model mới nào ngoài Account authority đã
  pin — quyết định LIVE authorization VẪN thuộc một governance
  transaction riêng biệt, hoàn toàn ngoài phạm vi Config Convention.
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
v0.2  2026-08-11  Bounded correction, đóng `EF-CONFIG-A-MAJ-01`. v0.1
      §4 dùng "LIVE-vs-PAPER environment selection" LÀM ví dụ setting
      Config-owned cần explicit-config/fail-closed default, VÀ §9
      liệt kê PAPER/LIVE cùng cấp với deployment-style environment
      (dev/test/staging/production) — tạo alternate-source-of-truth
      ambiguity với `account.md` (Account authority: `environment`
      required, immutable, gán TẠI `AccountRegistered`, §1/§8, KHÔNG
      tự authorize Live execution). Sửa: §4 bỏ ví dụ PAPER/LIVE khỏi
      danh sách Config-owned sensitive setting. §9 tách bạch tường
      minh — `Account.environment` VẪN LÀ domain value thuộc Account
      authority DUY NHẤT; Config KHÔNG own/derive/default/override/
      replace giá trị đó; source precedence (§2) KHÔNG BAO GIỜ được
      hiểu LÀ cách thay đổi `Account.environment` đã authoritative;
      Config VẪN CÓ THỂ định nghĩa operational setting được scope/
      condition bởi một giá trị ĐÃ authoritative, MIỄN LÀ KHÔNG tự
      đặt/suy diễn chính giá trị PAPER/LIVE đó; configuration KHÔNG
      BAO GIỜ silently convert PAPER→LIVE; LIVE execution authorization
      VẪN LÀ quyết định governance riêng biệt. **KHÔNG đổi:** §1
      (configuration model, VẪN LÀ controlling principle, KHÔNG suy
      yếu), §2 (source precedence), §3 (environment-variable mapping),
      §4 phần còn lại (defaults policy), §5 (required/optional), §6
      (validation), §7 (startup/activation), §8 (secrets boundary),
      §10 (overrides), §11 (reloadability), §12 (local development),
      §13 (Python/Go boundary), §14 (Logging interaction), §15
      (authority boundaries), Non-goals, ADR-scope disposition, future
      ADR Scope Rule rerun requirement. KHÔNG chạm `account.md`
      (Account domain authority)/`ADR-028`/`ADR-017`/`ADR-007`. KHÔNG
      tạo ADR-029, KHÔNG redesign Account/environment semantics, KHÔNG
      authorize LIVE. `status` VẪN `Draft`.
ACCEPTANCE  2026-08-11  Product Owner lifecycle approval — mechanical,
      vai trò: `Config Convention v0.2 Mechanical Approval Recorder`.
      Quyết định: "APPROVE CONFIG CONVENTION V0.2 — ACCEPT
      EF-CONFIG-B-MIN-01 AS NON-BLOCKING RESIDUAL." Reviewed candidate:
      v0.2, blob 805bd9a351d1792e5d9283ea0f4989129aa36295 (bounded
      Review A re-review CLEAN, New Blocker/Major/Minor 0/0/0, đóng
      `EF-CONFIG-A-MAJ-01`; Independent Review B trên đúng v0.2: New
      Blocker 0/New Major 0/New Minor 1 — `EF-CONFIG-B-MIN-01`
      (candidate-identity/provenance wording stale tại "Non-goals"
      heading VÀ "ADR-scope disposition," VALID, non-blocking),
      `READY_FOR_PRODUCT_OWNER_DECISION`). `status: Draft -> Approved`,
      `approved_by: null -> Product Owner`, `approved_at: null ->
      "2026-08-11"`. `version` KHÔNG bump (pure mechanical lifecycle
      approval) — VẪN `0.2`. `EF-CONFIG-B-MIN-01` VẪN `OPEN — accepted
      non-blocking residual`, KHÔNG đóng, KHÔNG sửa stale "v0.1"
      wording tại đây (correction riêng biệt tương lai, KHÔNG tại
      transaction này). KHÔNG semantic content nào đổi (§1–§15 byte-
      equivalent ngoài banner/lifecycle metadata/change history này VÀ
      residual stale wording đã accept). Tài liệu VẪN LÀ living
      document — `Approved` KHÔNG immutable byte-for-byte như ADR;
      thay đổi SEMANTIC tương lai VẪN PHẢI tự rerun ADR Scope Rule
      đúng §15. KHÔNG chạm `ADR-028`/`ADR-017` (Approved, immutable)/
      `account.md`/`ADR-027`/`logging.md`/`ADR-026`/`naming.md`/
      `ADR-025`/`coding-standard.md`/`ADR-024`/`monorepo.md`/`ADR-008`/
      `module-registry.yaml`/Constitution/Phase 1.5 rules, KHÔNG tạo
      ADR-029, KHÔNG mở Engineering Foundation category khác, KHÔNG
      chọn config/secret tooling nào, KHÔNG authorize Phase 2/LIVE.
```
