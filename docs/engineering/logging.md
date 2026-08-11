---
id: engineering-logging
title: "Engineering Foundation — Logging Convention"
version: "0.1"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-11"
last_review: null
next_review: null
depends_on: ["../constitution/03-engineering-principles", "../adr/ADR-008", "../adr/ADR-027", "coding-standard", "naming"]
---

# Engineering Foundation — Logging Convention

**Vai trò của tài liệu này:** convention document THỨ TƯ của Phase 1.5 — Engineering Foundation (Chapter 3 §3.2), phạm vi CHỈ category **Logging** (Chapter 14 §14.2's Phase 1.5 scope list) — đúng `EF-TXN-002` (một category = một transaction bounded). **`ADR-027` v0.2 (Approved 2026-08-11) LÀ authority cho chính việc CÓ một cross-module Logging Convention baseline bắt buộc** — tài liệu này LÀ living convention chứa chi tiết rule reversible dưới authority đó, KHÔNG lặp lại decision text của ADR-027. KHÔNG Constitution chapter, KHÔNG ADR, KHÔNG redefine Module Taxonomy/dependency graph/ngôn ngữ allocation/Coding Standard/Naming Convention — `module-registry.yaml` VẪN authority module identity/dependency, `ADR-008` VẪN authority ngôn ngữ, `ADR-024`/`monorepo.md` VẪN authority repository topology, `ADR-025`/`coding-standard.md` VẪN authority Coding Standard, `ADR-026`/`naming.md` VẪN authority identifier naming. Mọi thay đổi SEMANTIC tương lai vào tài liệu này PHẢI tự chạy lại ADR Scope Rule (Chapter 0 §4b) hiện hành TẠI chính thời điểm đổi — reversibility của kỹ thuật thay đổi KHÔNG hủy/miễn vế ">1 module" nếu vế đó đã thỏa (đúng lesson `ADR-025`/`ADR-026` §3, KHÔNG redefine — xem §13 dưới).

**Residual ADR finding `ADR027-B-MIN-01` (§4 Alternatives của ADR-027): VẪN `OPEN — accepted non-blocking`** — quan sát riêng của chính ADR-027, KHÔNG chạm/KHÔNG đóng tại đây (thuộc phạm vi correction riêng cho `ADR-027.md`, KHÔNG tại living convention document này). Rule bên dưới derive ĐỘC LẬP dưới ADR-027 §3's living-convention authority — KHÔNG suy diễn từ §4's rationale sentence như đã là detailed policy quyết định sẵn.

## 1. Purpose and authority

```text
`ADR-027` (v0.2, Approved) LÀ authority cho quyết định "CÓ một cross-
  module Logging Convention baseline chung bắt buộc" — tài liệu này CHỈ
  chứa chi tiết rule reversible dưới authority đó, KHÔNG lặp lại decision
  text của ADR-027.
Logging Convention KHÔNG tạo domain/event/API authority nào — **log
  record ≠ domain event.** Một log record CÓ THỂ mô tả một event/action
  đã xảy ra, NHƯNG KHÔNG tự nó tạo canonical event existence/schema nào
  — Domain Contract/Event Contract (`/docs/domain/`) VẪN authority DUY
  NHẤT cho event existence/schema (ADR-027 §3, KHÔNG redefine tại đây).
Tài liệu này KHÔNG invent canonical domain/event/module identity nào —
  ví dụ dưới đây (nếu có) LÀ minh họa pattern, KHÔNG PHẢI canonical
  vocabulary mới.
```

## 2. Structured logging

```text
Log record PHẢI LÀ structured record (key/value hoặc tương đương), KHÔNG
  free-form string-only làm default cho log có ý nghĩa vận hành/debugging
  — free-form message field VẪN được phép LÀM MỘT trong các field (§3
  `message`), NHƯNG record tổng thể PHẢI structured để tool downstream
  parse được nhất quán xuyên module.
Common semantic record model (tối thiểu, §3) ĐỦ cho cross-module
  diagnostics hiện tại — tài liệu này KHÔNG đặc tả object/API/class cụ
  thể của bất kỳ logging library nào (Python/Go idiom tự quyết định
  representation, §10 dưới).
KHÔNG chọn serialization format cụ thể (JSON/text/binary...) tại đây —
  thuộc phạm vi §11 (Output/sink boundary), deferred.
```

## 3. Minimum common fields

```text
Required-always (mọi log record PHẢI có):
  timestamp        theo §4 dưới.
  level             theo §5 dưới.
  message           human-readable, mô tả sự việc/lý do log record tồn
                    tại — KHÔNG PHẢI structured payload thay thế cho
                    field khác.
  module_id         canonical module identity — PHẢI dùng ĐÚNG spelling
                    `module_id` đã đăng ký tại `module-registry.yaml`
                    (kebab-case, vd `feature-engine`, `risk-gateway` —
                    minh họa, KHÔNG tạo module mới). Tài liệu này KHÔNG
                    tạo authority `module_id` thứ hai.

Contextual/optional (CHỈ khi context liên quan thực sự tồn tại — KHÔNG
  bắt buộc field trống/giả):
  correlation_id / causation_id    theo §6 dưới, CHỈ khi request/
                                    workflow context đã tồn tại.
  error/exception context           theo §7 dưới, CHỈ khi log record LÀ
                                    error/exception log.
  bất kỳ field bổ sung khác theo nhu cầu module cụ thể — KHÔNG bị cấm,
    NHƯNG KHÔNG bắt buộc bởi baseline này.

Tài liệu này KHÔNG invent trace/span/distributed-tracing semantics nào
  (`trace_id`/`span_id` kiểu OpenTelemetry...) — KHÔNG existing authority
  hiện tại (Domain/Event/API contract, ADR-027) establish nhu cầu đó;
  nếu tương lai cần, đó LÀ một semantic addition PHẢI tự rerun ADR Scope
  Rule (§13 dưới), KHÔNG tự động suy diễn tại đây.
```

## 4. Timestamp

```text
Timestamp representation: ISO 8601 string, UTC, có timezone designator
  rõ ràng (vd `2026-08-11T09:15:32.123Z`) — chọn vì: (1) human-readable
  trực tiếp trong raw log file/text sink (KHÔNG cần decode timestamp
  epoch); (2) sort/so sánh lexicographic đúng thứ tự thời gian mà KHÔNG
  cần parse; (3) hỗ trợ cross-module ordering nhất quán khi mọi module
  cùng dùng UTC, KHÔNG lệ thuộc local timezone của host/container.
Mọi log record PHẢI ghi timestamp theo UTC — KHÔNG local timezone,
  KHÔNG offset khác UTC. Module chạy ở bất kỳ timezone host nào PHẢI tự
  convert sang UTC trước khi ghi log.
Tài liệu này KHÔNG chọn storage backend nào lưu timestamp đó (deferred,
  §11) — CHỈ quyết định representation của chính field trong log record.
```

## 5. Log levels

```text
Level tối thiểu cần cho vận hành Ride (bounded, KHÔNG language-library-
  specific API):
  DEBUG      thông tin chi tiết chỉ cần khi debug/dev — KHÔNG bật default
             tại production trừ khi đang điều tra sự việc cụ thể.
  INFO       sự việc vận hành bình thường, đáng ghi lại nhưng KHÔNG PHẢI
             lỗi/cảnh báo (vd module start/stop, một step xử lý hoàn
             tất).
  WARN       tình trạng bất thường/đáng chú ý NHƯNG hệ thống VẪN tiếp
             tục hoạt động đúng (KHÔNG cần can thiệp ngay).
  ERROR      một lỗi cụ thể xảy ra, ảnh hưởng tới xử lý hiện tại (một
             request/workflow/step thất bại) — xem §7 cho boundary với
             Error Handling category.
  CRITICAL   lỗi nghiêm trọng đe dọa continuity của module/hệ thống (vd
             mất kết nối tới dependency PHẢI có để hoạt động) — dùng hạn
             chế, KHÔNG lạm dụng thay ERROR thông thường.

Mỗi module PHẢI dùng level idiomatic của chính logging library/runtime
  đó (Python `logging`/Go tương đương) MIỄN LÀ level đó map ĐÚNG semantic
  5 mức trên — tài liệu này KHÔNG chọn library/API level enum cụ thể
  (§10 dưới).
KHÔNG dùng level để encode business logic (vd KHÔNG dùng ERROR level làm
  control-flow signal) — level CHỈ mô tả severity của chính log record.
```

## 6. Correlation and causation

```text
Khi một request/workflow/transaction context ĐÃ tồn tại (vd một request
  ID/correlation ID đã được tạo/truyền qua module boundary bởi authority
  hiện hành — API surface, message/event metadata...), log record liên
  quan tới context đó PHẢI mang lại correlation_id (và causation_id khi
  phân biệt được "cái gì gây ra cái gì" trong cùng luồng) — hỗ trợ I-1
  Explainability, cho phép trace một luồng xử lý xuyên module.
Tài liệu này KHÔNG tạo canonical correlation/causation ID scheme mới,
  KHÔNG tạo distributed-tracing architecture (trace/span propagation
  protocol) — CHỈ yêu cầu: nếu identifier đó ĐÃ tồn tại dưới authority
  đúng của nó (API/event/domain contract), logging PHẢI mang nó theo,
  KHÔNG bỏ qua.
KHÔNG bắt buộc correlation_id/causation_id khi KHÔNG có context liên
  quan (vd một log record nội bộ module, KHÔNG thuộc bất kỳ cross-module
  request/workflow nào) — field này contextual/optional (§3), KHÔNG
  required-always.
```

## 7. Error / exception logging boundary

```text
Khi log record mô tả một error/exception, log record đó NÊN preserve
  error identity/context sẵn có (vd exception type/class name, error
  message gốc từ exception — KHÔNG tự sinh message mới thay thế message
  gốc) — hỗ trợ debugging/explainability, KHÔNG che mất nguyên nhân gốc.
Tránh log trùng lặp không kiểm soát cho CÙNG một error/exception (vd
  log lại full stack trace ở MỌI layer nó truyền qua) — NÊN log đầy đủ
  context (bao gồm stack trace nếu ngôn ngữ hỗ trợ) một lần TẠI layer
  xử lý/quyết định cuối cùng cho error đó, các layer trung gian truyền
  error tiếp KHÔNG cần re-log toàn bộ nếu KHÔNG thêm context mới.
Tài liệu này CHỈ quyết định Logging-side presentation requirement trên
  (làm sao ghi lại error đã xảy ra) — KHÔNG thiết kế exception hierarchy/
  error contract/retry policy (thuộc Error Handling category riêng,
  Chapter 14 §14.2, chưa mở tại transaction này).
```

## 8. Sensitive information

```text
Log record KHÔNG BAO GIỜ chứa (baseline prohibition, KHÔNG optional):
  secrets/credentials (password, private key...);
  API key/token/session token/bearer token;
  private authentication material khác (vd signing key — xem
    `custody-signing-service`/`account-service` trong
    `module-registry.yaml`, minh họa module CÓ THỂ xử lý dữ liệu nhạy
    cảm, KHÔNG tạo authority mới);
  bất kỳ giá trị nào hiển nhiên nhạy cảm khác theo domain context của
    chính module đó (vd raw customer PII nếu tồn tại — quyết định "gì
    LÀ nhạy cảm cho module cụ thể" thuộc trách nhiệm module đó, tài liệu
    này CHỈ pin baseline prohibition chung).
Khi một field CÓ THỂ chứa giá trị nhạy cảm NHƯNG field đó vẫn cần xuất
  hiện trong log để debug (vd một identifier gắn với secret), module
  PHẢI redact/mask giá trị đó trước khi log (vd che một phần, hash, hoặc
  bỏ hẳn field) — KHÔNG log giá trị gốc "tạm thời" rồi sửa sau.
Tài liệu này KHÔNG tạo một hệ thống classification bảo mật/privacy đầy
  đủ (data sensitivity tier, compliance mapping...) — CHỈ pin baseline
  prohibition/redaction expectation tối thiểu cần cho implementation
  hiện tại.
```

## 9. Event vs log distinction

```text
Đúng ADR-027 §3, giữ nguyên tại đây: domain event existence/schema
  authority VẪN thuộc DUY NHẤT Domain Contract/Event Contract
  (`/docs/domain/`) — logging một sự việc KHÔNG tự nó tạo event contract
  nào.
Log record CÓ THỂ tham chiếu một canonical event identifier/name CHỈ khi
  event đó ĐÃ tồn tại dưới authority đúng của nó (Domain/Event Contract)
  — tài liệu này KHÔNG invent event mới CHỈ để minh họa logging pattern;
  nếu ví dụ event xuất hiện dưới đây, đó LÀ minh họa naming pattern
  (đúng `naming.md` §7's `PAST_TENSE_UPPER_SNAKE`, vd `ORDER_FILLED`),
  KHÔNG tuyên bố event đó chính thức tồn tại trong Domain Contract.
`log record ≠ domain event` (ADR-027 §3) — phân biệt này PHẢI giữ tường
  minh mọi lúc khi tài liệu này/implementation tương lai đề cập tới
  "event" trong context logging.
```

## 10. Language/runtime boundary

```text
Python VÀ Go (ADR-008 pin ngôn ngữ theo layer) ĐƯỢC PHÉP dùng API/
  representation logging idiomatic riêng của chính ngôn ngữ đó (vd
  Python `logging`/`structlog`-style dict, Go structured-logging idiom
  riêng) — tài liệu này KHÔNG yêu cầu internal logging object byte-
  identical xuyên hai ngôn ngữ.
Yêu cầu DUY NHẤT: mỗi implementation PHẢI conform đúng SEMANTIC
  requirement chung tại §2–§9 trên (structured record, minimum field
  §3, timestamp representation §4, level semantics §5, correlation
  khi có context §6, error-logging boundary §7, sensitive-data
  prohibition §8, event-vs-log distinction §9) — KHÔNG PHẢI identical
  syntax/API/object shape.
Tài liệu này KHÔNG chọn logging library cụ thể cho Python HAY Go tại
  transaction này (deferred, §11 dưới) — lựa chọn library/tooling cụ
  thể thuộc một transaction implementation-readiness riêng (nếu cần
  trước khi module đầu tiên build) hoặc CI/CD category tương lai.
```

## 11. Output / sink boundary

```text
Tài liệu này KHÔNG chọn tại đây:
  log collector/aggregator cụ thể;
  observability vendor (APM, metrics platform...);
  storage/retention backend (nơi log được lưu dài hạn);
  deployment topology cho pipeline log (sidecar, agent, direct-ship...).
Application-output expectation tối thiểu cần cho implementation-
  readiness hiện tại (technology-neutral, KHÔNG chọn vendor/backend):
  mỗi module implementation (Python/Go) PHẢI ghi structured log record
  (§2–§3) ra một output stream mà runtime/deployment environment CÓ THỂ
  thu thập được (vd stdout/stderr theo container logging convention phổ
  biến, hoặc file — CHỌN CỤ THỂ nào thuộc CI/CD/deployment category
  tương lai) — module KHÔNG tự implement riêng một sink/transport
  logging phức tạp (network log shipper tự viết...) khi runtime
  environment đã cung cấp collection mechanism chuẩn.
Serialization format cụ thể (JSON line, key=value text...) deferred tới
  transaction implementation-readiness riêng hoặc CI/CD category — CHỈ
  yêu cầu: format đó PHẢI parse được structured record §2–§3 nhất quán,
  KHÔNG free-form-only.
```

## 12. Determinism / explainability

```text
Log record PHẢI mô tả sự việc/fact ĐÃ xảy ra tại runtime — KHÔNG suy
  diễn/log một causality chưa thực sự xác nhận (vd KHÔNG log "X gây ra
  Y" khi hệ thống chỉ quan sát được X và Y riêng biệt, chưa xác nhận
  quan hệ nhân quả).
Logging KHÔNG PHẢI substitute cho canonical execution/replay/domain
  evidence — khi cần xác nhận chính xác một luồng xử lý/quyết định đã
  xảy ra thế nào (audit, replay, compliance), authority ĐÚNG LÀ Domain
  Contract/Event Contract/replay-integration-service (xem
  `module-registry.yaml`) và execution evidence tương ứng — KHÔNG dùng
  log record LÀM nguồn sự thật duy nhất cho quyết định/replay đó.
Nguyên tắc này hỗ trợ I-1 Explainability tại tầng logging — log record
  LÀ observation phụ trợ, KHÔNG PHẢI canonical decision/event record.
```

## 13. Deviations

```text
Một deviation khỏi Logging Convention ĐƯỢC PHÉP khi có lý do kỹ thuật
  cụ thể (vd một external SDK/generated code/runtime constraint không
  kiểm soát được buộc log theo format khác — cùng nguyên tắc
  `coding-standard.md` §6/`naming.md` §12) — PHẢI ghi lại tại chính điểm
  deviation (comment/commit message), KHÔNG âm thầm.
Mọi thay đổi SEMANTIC tương lai vào tài liệu này (KHÔNG PHẢI mọi sửa —
  CHỈ khi đổi Ý NGHĨA rule, vd thêm required field mới bắt buộc cho MỌI
  module, đổi timestamp representation, thêm trace/span semantics mới)
  PHẢI tự chạy lại ADR Scope Rule (Chapter 0 §4b) hiện hành TẠI chính
  thời điểm đổi — KHÔNG suy diễn "reversible/refactor-class" LÀ đủ để
  miễn ADR (đúng lesson `ADR-025`/`ADR-026`/`ADR-027` §3, KHÔNG
  redefine). Vì baseline áp dụng cho MỌI module, phần lớn semantic
  update sẽ thỏa lại vế ">1 module" — reversibility của kỹ thuật thay
  đổi KHÔNG liên quan tới việc vế đó có thỏa hay không.
```

## 14. Boundary với category khác (Phase 1.5) — KHÔNG absorb

```text
Coding Standard (formatting/lint/dependency-hygiene):     VẪN thuộc
  `coding-standard.md` — tài liệu này KHÔNG redefine.
Naming Convention (identifier naming):                     VẪN thuộc
  `naming.md` — tài liệu này CHỈ dùng canonical `module_id` reference
  (§3), KHÔNG tự đặt naming rule mới cho field/identifier khác ngoài
  logging-record field đã pin tại §3.
Config (runtime configuration architecture):                deferred tới
  Config category riêng.
Error Handling (exception hierarchy/error contract/retry policy):
  deferred tới Error Handling category riêng — §7 trên CHỈ nói
  "presentation requirement," KHÔNG định nghĩa exception hierarchy.
Testing (framework/coverage/tier):                          deferred tới
  Testing category riêng.
CI/CD (pipeline/enforcement mechanism, log collector/observability
  vendor selection):                                        deferred tới
  CI/CD category riêng — §11's "PHẢI ghi ra output stream thu thập
  được" LÀ principle chờ CI/CD category thực sự chọn collection
  mechanism, KHÔNG tự tạo pipeline tại đây.
```

## 15. ADR-scope disposition

```text
Quyết định "CÓ một Logging Convention baseline chung bắt buộc cho MỌI
  module" LÀ platform-wide, thỏa vế ">1 module" của Chapter 0 §4b — ĐÃ
  ADR Required (KHÔNG PHẢI ADR Not Required — reversibility của chi
  tiết rule bên trong tài liệu này KHÔNG hủy/miễn vế đó).
`ADR-027` v0.2 (Approved 2026-08-11, "APPROVE ADR-027 V0.2") LÀ ADR đó —
  satisfy chính xác quyết định baseline-existence này. Tài liệu này
  (`logging.md`) LÀ living convention ALIGNED dưới `ADR-027`, chứa chi
  tiết rule reversible (§1–§14 trên), KHÔNG lặp lại decision text của
  ADR-027.
Mọi thay đổi SEMANTIC tương lai vào tài liệu này PHẢI tự chạy lại ADR
  Scope Rule hiện hành TẠI chính thời điểm đổi (xem §13 trên) — Logging
  KHÔNG generally "ADR Not Required" — baseline-existence đã resolved
  bởi ADR-027, NHƯNG một semantic baseline change MỚI (áp dụng cho MỌI
  module) vẫn CÓ THỂ tự thỏa lại vế ">1 module."
Residual `ADR027-B-MIN-01` (§4 Alternatives của ADR-027) VẪN
  `OPEN — accepted non-blocking` — tài liệu này KHÔNG tự đóng finding đó
  (thuộc phạm vi correction riêng cho `ADR-027.md`, KHÔNG tại đây).
```

## Change history

```text
v0.1  2026-08-11  Established — vai trò: `Phase 1.5 Logging Foundation
      Executor`. Bounded EF-TXN-002 category transaction (Logging only).
      Verify trực tiếp trước khi author: current HEAD
      (95577bc4d22c97b4a67f2481943bee2dd623355e), ADR-027 v0.2 Approved
      identity (blob `b89d0f9d1d7109d41e45cc7d302f5b398f100b09`),
      `docs/engineering/logging.md` KHÔNG tồn tại trước đây, canonical
      `module_id` field (`module-registry.yaml`). Established 15 mục:
      purpose/authority (log record ≠ domain event, ADR-027 giữ nguyên),
      structured logging (record structured, KHÔNG free-form-only,
      KHÔNG chọn serialization), minimum common fields (required-always:
      timestamp/level/message/module_id; contextual: correlation_id/
      causation_id/error context; KHÔNG invent trace/span semantics),
      timestamp (ISO 8601 UTC, lý do explicit, KHÔNG chọn storage
      backend), log levels (DEBUG/INFO/WARN/ERROR/CRITICAL, semantic
      bounded, KHÔNG language-API-specific), correlation/causation (chỉ
      khi context tồn tại, KHÔNG tạo tracing architecture mới), error/
      exception logging boundary (presentation-only, KHÔNG absorb Error
      Handling), sensitive information (baseline prohibition: secrets/
      credentials/token/private auth material, redact khi cần, KHÔNG
      tạo classification system đầy đủ), event-vs-log distinction (giữ
      nguyên ADR-027 §3, KHÔNG invent canonical event), language/runtime
      boundary (Python/Go idiom riêng ĐƯỢC PHÉP khác, conform semantic
      chung, KHÔNG chọn library), output/sink boundary (KHÔNG chọn
      collector/vendor/backend/topology, chỉ pin technology-neutral
      output-stream expectation tối thiểu), determinism/explainability
      (log KHÔNG suy diễn causality, KHÔNG substitute canonical
      evidence), deviations (justified + documented, semantic change
      tương lai PHẢI rerun ADR Scope Rule), boundary với category khác
      (KHÔNG absorb Coding Standard/Naming/Config/Error Handling/
      Testing/CI-CD), ADR-scope disposition (baseline-existence ĐÃ ADR
      Required, ADR-027 satisfy, semantic update tương lai vẫn PHẢI tự
      rerun ADR Scope Rule — KHÔNG tuyên bố Logging generally ADR Not
      Required). KHÔNG invent canonical event/domain/API vocabulary hay
      inventory nào (event ví dụ tại §9 đánh dấu "minh họa," KHÔNG
      canonical). KHÔNG chọn logging library/observability vendor/
      storage backend nào. KHÔNG absorb Error Handling exception
      hierarchy. `ADR027-B-MIN-01` VẪN `OPEN — accepted non-blocking`,
      KHÔNG đóng tại đây, KHÔNG sửa `ADR-027.md`. KHÔNG chạm `ADR-027`
      (Approved, immutable)/`ADR-026`/`naming.md`/`ADR-025`/
      `coding-standard.md`/`ADR-024`/`monorepo.md`/`ADR-008`/
      `module-registry.yaml`/Constitution/Phase 1.5 rules. KHÔNG bắt đầu
      Config/Error Handling/Testing/CI-CD. `status: Draft` — not
      self-approved (`G-ORCH-002`).
```
