---
id: engineering-error-handling
title: "Engineering Foundation — Error Handling Convention"
version: "0.2"
status: Approved
owner: Product Owner
reviewers: []
approved_by: Product Owner
approved_at: "2026-08-12"
created_at: "2026-08-12"
last_review: null
next_review: null
depends_on: ["../constitution/03-engineering-principles", "../adr/ADR-008", "../adr/ADR-029", "../adr/ADR-017", "logging", "config"]
---

# Engineering Foundation — Error Handling Convention

**APPROVED (2026-08-12) — status: Draft → Approved.** Product Owner decision: **"APPROVE ERROR HANDLING CONVENTION V0.2 — ACCEPT EF-ERR-B-MIN-01 AS NON-BLOCKING RESIDUAL."** Reviewed candidate: v0.2, blob `10c1b259ec28bdfb0caa318ceffda81228a707da`. `version: "0.2"` KHÔNG đổi (pure mechanical lifecycle approval — KHÔNG bump). Tài liệu này VẪN LÀ living document (Chapter 3 §3.2 "tài liệu SỐNG, không bất biến"; Chapter 0 §7.1 lifecycle Draft→...→Approved→Locked) — `Approved` KHÔNG đồng nghĩa immutable byte-for-byte như ADR (Chapter 11 §11.3 KHÔNG áp dụng ở đây); thay đổi tương lai vẫn hợp lệ qua version bump + re-review (Chapter 0 §8), VÀ mọi thay đổi SEMANTIC PHẢI tự rerun ADR Scope Rule đúng ADR-scope disposition dưới.

**Review evidence tại approval này:**

```text
Đóng (trước approval, v0.2): EF-ERR-A-MAJ-01.

Bounded Review A re-review trên v0.2:
  EF-ERR-A-MAJ-01: CLOSED
  New Blocker 0 / New Major 0 / New Minor 0
  CLEAN — READY_FOR_INDEPENDENT_REVIEW_B

Independent Review B trên đúng v0.2:
  New Blocker 0 / New Major 0 / New Minor 1

  EF-ERR-B-MIN-01: candidate/provenance wording VẪN stale, tham chiếu
    "v0.1" tại nhiều mục KHÔNG đổi (vd Non-goals heading, ADR-scope
    disposition, Change history v0.1 entry). Finding VALID, non-
    blocking.

  Verdict: READY_FOR_PRODUCT_OWNER_DECISION
```

**`EF-ERR-B-MIN-01`: VẪN `OPEN — accepted non-blocking residual`** — Product Owner chấp nhận LÀM residual tại chính approval này, KHÔNG sửa/KHÔNG đóng tại transaction này (đúng `G-REV-004` — KHÔNG correction churn khi KHÔNG có Major/Blocker mới; correction riêng biệt, nếu thực hiện, sẽ đóng finding này sau, KHÔNG tại đây). Stale "v0.1" wording tại các mục liên quan GIỮ NGUYÊN KHÔNG sửa.

**Approval này KHÔNG đổi Error Handling Convention semantics nào** (§1–§15 dưới byte-equivalent ngoài banner/lifecycle metadata/change history này, VÀ ngoài residual `EF-ERR-B-MIN-01` stale wording đã accept KHÔNG sửa) — KHÔNG chạm `ADR-029` (Approved, immutable)/`ADR-028`/`config.md`/`ADR-027`/`logging.md`/`ADR-026`/`naming.md`/`ADR-025`/`coding-standard.md`/`ADR-024`/`monorepo.md`/`ADR-008`/`ADR-017`/`module-registry.yaml`/Domain Contract/Constitution/Phase 1.5 rules, KHÔNG tạo ADR-030, KHÔNG mở Testing/CI-CD category, KHÔNG chọn framework/library/error-code schema nào, KHÔNG đóng `EF-CONFIG-B-MIN-01`, KHÔNG authorize Phase 2, KHÔNG authorize LIVE.

**Vai trò của tài liệu này:** convention document THỨ SÁU của Phase 1.5 — Engineering Foundation (Chapter 3 §3.2), phạm vi CHỈ category **Error Handling** (Chapter 14 §14.2's Phase 1.5 scope list) — đúng `EF-TXN-002` (một category = một transaction bounded). **`ADR-029` v0.2 (Approved 2026-08-12) LÀ authority cho chính việc CÓ một cross-module Error Handling Convention baseline bắt buộc** — tài liệu này LÀ living convention chứa chi tiết rule reversible dưới authority đó, KHÔNG lặp lại decision text của ADR-029 (xem `ADR-029.md` cho full architecture text, KHÔNG duplicate tại đây). KHÔNG Constitution chapter, KHÔNG ADR, KHÔNG redefine module identity/dependency/ngôn ngữ allocation/repository topology/Coding Standard/Naming Convention/Logging Convention/Config Convention/Custody & Signing Trust Boundary — mỗi authority đó VẪN giữ nguyên (§15 dưới). Mọi thay đổi SEMANTIC tương lai vào tài liệu này PHẢI tự chạy lại ADR Scope Rule (Chapter 0 §4b) hiện hành TẠI chính thời điểm đổi — reversibility của kỹ thuật thay đổi KHÔNG hủy/miễn vế ">1 module" nếu vế đó đã thỏa (đúng lesson `ADR-025`/`ADR-026`/`ADR-027`/`ADR-028`/`ADR-029` §3, KHÔNG redefine — xem §16 dưới).

**Residual accepted riêng của `config.md`: `EF-CONFIG-B-MIN-01` VẪN `OPEN — accepted non-blocking`** — KHÔNG chạm, KHÔNG đóng tại đây (thuộc phạm vi correction riêng cho `config.md`, KHÔNG tại living convention document này).

**Nguyên tắc chi phối (ADR-029 §3, tái khẳng định KHÔNG redefine):** technical/programming error ≠ domain/business outcome. Tài liệu này CHỈ quản lý technical error handling (exception/panic/timeout/validation failure nội bộ...) — KHÔNG BAO GIỜ redefine `RiskEvaluation` outcome/rejection reason (`risk.md` §5e), Execution Result/Fill semantics, business rejection/denial fact, Account lifecycle/domain state, hay Ý NGHĨA của bất kỳ Domain/Event/API contract nào (`/docs/domain/`).

**v0.2 — bounded correction (2026-08-12), đóng `EF-ERR-A-MAJ-01`, vai trò: `Error Handling Convention v0.2 Bounded Correction Executor`.** v0.1 §7 nói "NẾU KHÔNG tồn tại một authoritative partial-result representation nào ... module PHẢI fail explicitly (technical error)" — quá rộng: KHÔNG tồn tại MỘT representation "partial" riêng biệt KHÔNG chứng minh underlying outcome LÀ technical/programming error; Domain/Event/API authority hiện hành CÓ THỂ ĐÃ định nghĩa một business failure/rejection/result representation KHÁC cho đúng tình huống đó — Error Handling KHÔNG được reclassify một business/domain outcome ĐÃ tồn tại thành technical error CHỈ vì thiếu representation "partial" riêng. Sửa: §7 pin rõ thứ tự resolve — (1) KHÔNG silent full-success; (2) nếu Domain/Event/API contract hiện hành ĐÃ có representation/outcome hợp lệ cho ĐÚNG tình huống đó (dù KHÔNG mang tên "partial"), PHẢI dùng ĐÚNG representation đó; (3) partial-result representation CHỈ dùng khi ĐÃ established bởi authority liên quan; (4) CHỈ khi KHÔNG có representation business/domain phù hợp NÀO VÀ nguyên nhân gốc THẬT SỰ technical/infrastructure/programming, module PHẢI fail explicitly LÀM technical error; (5) nếu tình huống lộ ra một business/domain semantic CHƯA tồn tại hoặc cần published-contract outcome MỚI, KHÔNG tự invent tại `error-handling.md` — report LÀM contract/authority gap, route qua đúng authority VÀ tự rerun ADR Scope Rule nếu applicable. **KHÔNG đổi:** taxonomy bảy category (§1), expected vs unexpected (§2), cause preservation (§3), bounded boundary translation (§4), retry-related classification/retry ownership prohibition (§5), timeout/cancellation (§6), Config startup/fail-closed boundary (§8), security/redaction (§9), Logging authority (§10), Python guidance (§11), Go guidance (§12), user-facing/internal representation (§13), explainability (§14), authority boundaries (§15), Non-goals, ADR-scope disposition. `EF-CONFIG-B-MIN-01` VẪN `OPEN — accepted non-blocking`, KHÔNG chạm. KHÔNG chạm `ADR-029.md`. KHÔNG invent Domain/Event/API partial-failure state mới, KHÔNG redefine Risk/Execution/Account outcome, KHÔNG đổi retry ownership/idempotency, KHÔNG chọn framework/library/error-code schema nào. `status` VẪN `Draft`.

## 1. Error categories

```text
Taxonomy nhỏ, semantic, áp dụng nhất quán xuyên Python/Go — tối thiểu
  phân biệt:
  validation/input error         (input KHÔNG hợp lệ theo type/format/
                                  range mong đợi — TRƯỚC business logic
                                  xử lý);
  configuration error            (config invalid/missing — boundary
                                  với Config Convention, §8 dưới);
  dependency/infrastructure error (một dependency bên ngoài — DB,
                                  network call, filesystem... —
                                  không khả dụng/lỗi);
  timeout/cancellation           (§6 dưới);
  security/authorization technical failure (khi applicable — vd
                                  credential resolution/signing thất
                                  bại tại boundary `ADR-017`, KHÔNG
                                  redefine custody/signing authority
                                  đó, CHỈ representation của chính
                                  technical failure);
  invariant/programming defect   (một bất biến nội bộ code bị vi
                                  phạm — bug, KHÔNG PHẢI failure vận
                                  hành bình thường, §2 dưới);
  external/venue integration failure (một tương tác bên ngoài platform
                                  — vd venue protocol/transport — thất
                                  bại kỹ thuật, KHÔNG PHẢI raw venue-
                                  interaction evidence chính nó, xem
                                  `ADR-017` §3.2a, KHÔNG đổi).
Tài liệu này KHÔNG invent business-domain outcome category nào LÀM
  technical error (vd KHÔNG coi một `RiskEvaluation REJECTED` LÀ một
  category tại đây — đó VẪN LÀ business outcome, §"Nguyên tắc chi
  phối" trên). Tránh mở rộng taxonomy quá mức — bảy category trên ĐỦ
  cho nhu cầu hiện tại, KHÔNG thêm category suy đoán trước khi có nhu
  cầu cụ thể.
```

## 2. Expected vs unexpected

```text
Một failure LÀ "expected/handled" khi code chủ động anticipate VÀ xử
  lý CÓ chủ đích (vd validation error trả về kết quả invalid có cấu
  trúc, timeout được catch và xử lý theo §6).
Một failure LÀ "unexpected/programming defect" khi nó vi phạm một bất
  biến nội bộ code KHÔNG lường trước (vd null/nil reference không mong
  đợi, index out of bound, type mismatch nội bộ).
Unexpected invariant/programming defect KHÔNG BAO GIỜ được silently
  convert thành một successful/domain outcome bình thường — defect đó
  PHẢI propagate LÀM technical error (crash/exception/panic theo
  idiom, §12/§13 dưới), KHÔNG được "nuốt" rồi trả về một kết quả giả
  coi như thành công.
```

## 3. Cause preservation

```text
Một technical error truyền qua internal layer/module boundary PHẢI
  giữ lại ĐỦ causal context cho diagnostics (vd original exception/
  error, stack context nếu ngôn ngữ hỗ trợ, category §1 liên quan) —
  KHÔNG thay thế bằng một generic error mới xóa mất nguyên nhân gốc.
Tài liệu này KHÔNG bắt buộc một concrete serialization/wrapping library
  cụ thể — Python (`raise ... from ...`, exception chaining tự nhiên)
  và Go (wrap error giữ nguyên `Unwrap()`/cause chain theo idiom) tự
  chọn mechanism ĐẠT được yêu cầu semantic trên (§11/§12 dưới).
Tránh mất nguyên nhân gốc qua một generic replacement error (vd catch
  một error cụ thể rồi raise lại một `Exception("something failed")`
  KHÔNG giữ context nào) — luôn giữ lại HOẶC original error object HOẶC
  đủ thông tin để tái tạo causal chain.
```

## 4. Boundary translation

```text
Technical error representation ĐƯỢC PHÉP translate tại một boundary
  (vd một internal exception Python translate thành một error code/
  response tại API surface, hay một Go `error` translate thành log
  entry structured) — MIỄN LÀ:
  giữ lại semantic category (§1)/causal context (§3) khi có ích cho
    diagnostics phía nhận;
  KHÔNG redefine Ý NGHĨA của Domain/Event/API outcome ĐÃ established
    (vd translation KHÔNG được biến một technical timeout thành một
    business "REJECTED" fact giả — nếu KHÔNG có domain outcome thật
    tương ứng, technical error VẪN LÀ technical error, KHÔNG ép thành
    domain semantics);
  KHÔNG tạo published-contract semantics MỚI qua translation đó — một
    thay đổi Ý NGHĨA published-contract (Event/API schema mới, field
    mới mang domain meaning...) VẪN thuộc authority hiện hành của
    chính contract đó (`/docs/domain/`), PHẢI tự rerun ADR Scope Rule
    (Chapter 0 §4b) nếu applicable — KHÔNG PHẢI qua tài liệu này.
```

## 5. Retry-related classification

```text
Error Handling CÓ THỂ classify/annotate thông tin hữu ích cho một
  retry decision ĐÃ authorize sẵn ở nơi khác — vd đánh dấu một
  technical error LÀ "transient" hay "permanent" theo nghĩa error-
  handling (KHÔNG PHẢI ownership/policy).

Error Handling KHÔNG ĐƯỢC:
  độc lập tuyên bố một operation thất bại LÀ retryable (retryability
    thật PHẢI xác định bởi authority idempotency/execution hiện hành,
    KHÔNG PHẢI tại đây);
  assign/reassign retry ownership giữa module (đúng `ADR-029` §6 —
    ownership ĐÃ established bởi authority hiện hành, vd `ADR-017` §8,
    Package 1.3-D, CHỈ document/reflect, KHÔNG tự assign);
  tạo retry/backoff policy (framework, số lần retry, delay algorithm...
    — KHÔNG quyết định tại đây);
  override idempotency authority (I-10 Idempotent Execution Effect,
    Package 1.3-D eligibility invariant — VẪN giữ nguyên);
  suy diễn retryability CHỈ từ loại exception/error ngôn ngữ (vd KHÔNG
    tự động coi MỌI `TimeoutError`/Go `context.DeadlineExceeded` LÀ
    retryable mà KHÔNG xét idempotency scope thật của chính operation
    đó).

Existing retry/idempotency architecture (I-10, Package 1.3-D, `ADR-017`
  §8) VẪN authority DUY NHẤT — tài liệu này KHÔNG redefine.
```

## 6. Timeout and cancellation

```text
Timeout/cancellation NÊN phân biệt được khỏi arbitrary internal failure
  khi có ích cho diagnostics (vd category riêng tại §1, hoặc field
  riêng khi log theo §10) — giúp phân biệt "operation bị hủy/quá thời
  gian chờ" khỏi "operation thất bại vì lý do nội tại khác."
Tài liệu này KHÔNG invent một cross-module timeout value cụ thể nào
  (vd KHÔNG pin "mọi call PHẢI timeout sau N giây") — giá trị timeout
  cụ thể thuộc implementation/Config Convention (`config.md`) của
  chính module đó, KHÔNG tại đây.
Tài liệu này KHÔNG định nghĩa retry behavior cho timeout/cancellation
  (thuộc §5 trên — retry ownership/policy KHÔNG quyết định tại đây).
```

## 7. Partial failure

```text
[v0.2 sửa, đóng `EF-ERR-A-MAJ-01`: v0.1 nói "NẾU KHÔNG tồn tại một
  authoritative partial-result representation nào ... module PHẢI
  fail explicitly (technical error)" — quá rộng: việc KHÔNG tồn tại
  MỘT representation "partial" riêng biệt KHÔNG chứng minh underlying
  outcome LÀ technical/programming error. Domain/Event/API authority
  hiện hành CÓ THỂ ĐÃ định nghĩa một business failure/rejection/result
  representation KHÁC cho đúng tình huống đó (vd `RiskEvaluation
  REJECTED`/`NON_EVALUABLE`, risk.md §5e) — Error Handling KHÔNG được
  reclassify một business/domain outcome ĐÃ tồn tại thành technical
  error CHỈ vì thiếu một "partial" representation riêng. Sửa: pin rõ
  thứ tự resolve dưới đây, giữ nguyên nguyên tắc chi phối "technical/
  programming error ≠ domain/business outcome."]

Baseline behavior tối thiểu:
  KHÔNG silently report full success khi một phần của operation
    required đã thất bại — nếu chỉ một phần hoàn tất, kết quả PHẢI
    phản ánh đúng trạng thái đó, KHÔNG "làm tròn" thành thành công
    hoàn toàn.
  NẾU một Domain/Event/API contract hiện hành ĐÃ định nghĩa một
    representation/outcome hợp lệ cho ĐÚNG tình huống thực tế đó (dù
    KHÔNG mang tên "partial" — vd một business rejection/failure
    result ĐÃ established), module PHẢI dùng ĐÚNG representation/
    outcome authoritative đó — KHÔNG bỏ qua nó để tạo một technical
    error thay thế.
  Một partial-result representation CHỈ được dùng khi ĐÃ established
    bởi authority liên quan (Domain/Event/API contract hiện hành) —
    KHÔNG tự invent một domain state "partial" mới.
  NẾU KHÔNG tồn tại representation business/domain phù hợp nào CHO
    tình huống đó, VÀ nguyên nhân gốc THẬT SỰ LÀ technical/
    infrastructure/programming failure (đúng §1/§2 — vd dependency
    không khả dụng giữa chừng operation), module PHẢI fail explicitly
    LÀM technical error theo convention này (§1/§2/§3).
  NẾU tình huống thực tế lộ ra một business/domain semantic CHƯA tồn
    tại, hoặc cần một published-contract outcome/state MỚI (KHÔNG PHẢI
    technical failure thật):
      KHÔNG tự invent semantic/state đó tại `error-handling.md`;
      report gap đó LÀM một contract/authority gap (thuộc phạm vi
        Domain/Event/API authority tương ứng, KHÔNG tại đây);
      một semantic change được đề xuất PHẢI đi qua đúng authority liên
        quan VÀ tự rerun ADR Scope Rule (Chapter 0 §4b) hiện hành TẠI
        chính thời điểm đó nếu applicable — KHÔNG tự động qua living
        convention này.
  Giữ nguyên nguyên tắc chi phối: technical/programming error ≠
    domain/business outcome (§"Nguyên tắc chi phối" trên) — §7 này
    KHÔNG redefine domain outcome nào, CHỈ pin thứ tự resolve khi
    partial failure xảy ra.
```

## 8. Startup/config failures

```text
Align với `ADR-028`/`config.md` (`Approved`) — missing/invalid required
  configuration PHẢI preserve ĐÚNG fail-closed semantics ĐÃ pin tại
  `config.md` §7 (startup/activation boundary), KHÔNG redefine tại đây.
Error Handling Convention CHỈ governs representation/propagation QUANH
  failure đó (vd category §1 nào áp dụng — "configuration error," cách
  cause được preserve §3, cách log §10) — Config Convention VẪN
  authority DUY NHẤT cho validation/startup config semantics ĐÃ
  Approved (`config.md` §6/§7).
`EF-CONFIG-B-MIN-01` (residual riêng của `config.md`) VẪN `OPEN —
  accepted non-blocking`, KHÔNG chạm tại đây.
```

## 9. Security and redaction

```text
Technical error message/context KHÔNG BAO GIỜ expose:
  credential/secret/API key/token;
  private signing material;
  raw secret value dưới bất kỳ hình thức nào;
  sensitive payload bị restrict bởi security authority hiện hành
    (`ADR-017`).
Đúng nguyên tắc `logging.md` §8/`config.md` §8, tái khẳng định nhất
  quán cho error message/context — KHÔNG redefine, KHÔNG chọn redaction
  vendor/library cụ thể tại đây.
```

## 10. Logging interaction

```text
Align với `ADR-027`/`logging.md` (`Approved`) — Error Handling PHẢI
  preserve đủ safe context (§3, KHÔNG chứa secret §9) cho việc log/
  diagnostics sau đó, NHƯNG:
  Logging Convention VẪN authority DUY NHẤT cho log level semantics
    (`logging.md` §5);
  Logging Convention VẪN authority DUY NHẤT cho required field/schema
    semantics (`logging.md` §3);
  Error Handling KHÔNG redefine log structure/level nào tại đây.
KHÔNG duplicate-log CÙNG một error tại MỌI layer nó truyền qua theo
  default (đúng `logging.md` §7's nguyên tắc tránh log trùng lặp
  không kiểm soát, KHÔNG redefine) — ƯU TIÊN log tại layer nào THÊM
  được operational context có ý nghĩa, HOẶC layer nơi error thực sự
  terminate (KHÔNG truyền tiếp nữa), trong khi VẪN preserve cause qua
  các layer thấp hơn (§3) để layer log cuối cùng CÓ đủ causal chain.
Đây LÀ convention guidance cho error-log interaction, KHÔNG PHẢI một
  observability architecture mới — KHÔNG chọn tooling/vendor nào.
```

## 11. Python guidance

```text
Idiomatic, implementation-light:
  dùng exception cho exceptional technical failure (§1/§2);
  preserve exception chaining/cause khi phù hợp (`raise ... from ...`,
    §3);
  KHÔNG catch broad exception (`except Exception:`/bare `except:`) CHỈ
    để suppress nó mà KHÔNG xử lý/re-raise/log có ý nghĩa;
  KHÔNG dùng exception LÀM normal business-outcome control flow khi
    một domain result type ĐÃ tồn tại cho tình huống đó (vd một
    `RiskEvaluation REJECTED` KHÔNG nên được model LÀM một exception
    Python trong code xử lý domain logic — đó LÀ một valid domain
    outcome, KHÔNG PHẢI error, đúng §"Nguyên tắc chi phối").
Tài liệu này KHÔNG định nghĩa một concrete platform exception hierarchy
  tại v0.1 này — CHƯA có existing repository authority nào yêu cầu rõ
  một hierarchy cụ thể; nếu tương lai cần, đó LÀ một quyết định
  implementation-readiness riêng (bounded, reversible, KHÔNG tự động
  ADR Required trừ khi tự thỏa Chapter 0 §4b theo đúng nghĩa của nó).
```

## 12. Go guidance

```text
Idiomatic, implementation-light:
  return error explicitly (đúng Go idiom `if err != nil`), KHÔNG dùng
    panic LÀM control flow thông thường;
  wrap error khi propagate, giữ nguyên cause/identity khi cần (Go
    `%w`/`errors.Is`/`errors.As`-compatible pattern, §3);
  check/propagate error nhất quán tại mọi call site liên quan;
  panic CHỈ dành riêng cho tình huống programmer/invariant genuinely
    unrecoverable (§2's "unexpected/programming defect") — KHÔNG PHẢI
    ordinary expected operational failure (timeout, validation error,
    dependency unavailable... PHẢI return error, KHÔNG panic).
Tài liệu này KHÔNG mandate một concrete custom error struct/sentinel-
  error framework cụ thể — module tự chọn pattern ĐẠT semantic trên
  (§3/§4), MIỄN LÀ conform.
```

## 13. User-facing/internal representation

```text
Internal stack trace, secret (§9), hay implementation detail nhạy cảm
  KHÔNG được expose trực tiếp ra external/user-facing boundary (API
  response, UI message...).
User/API representation của một technical error (khi cần hiển thị)
  PHẢI theo ĐÚNG published contract authority hiện hành (API contract,
  `/docs/domain/`) — tài liệu này KHÔNG tạo representation schema mới
  nào, KHÔNG redefine API contract meaning (§4 trên).
```

## 14. Explainability

```text
Một operator/developer PHẢI xác định được (I-1 Explainability, KHÔNG
  redefine — CHỈ áp dụng nguyên tắc chung cho error-handling context):
  technical-error category nào xảy ra (§1);
  boundary/layer nào observe nó đầu tiên;
  causal chain/root cause khi available (§3);
  error đó CÓ được translate qua boundary nào không (§4);
  retryability/ownership (nếu liên quan) ĐẾN TỪ authority nào KHÁC
    (§5), KHÔNG PHẢI suy diễn tại chỗ.
Tài liệu này KHÔNG mandate một tooling mechanism cụ thể để đạt
  explainability đó (log, trace, introspection API...) — CHỈ yêu cầu
  khả năng đó PHẢI tồn tại, implementation detail deferred.
```

## 15. Authority boundaries

```text
Domain/Event/API contract authority (/docs/domain/)  VẪN authority
                        DUY NHẤT cho business outcome semantics —
                        RiskEvaluation result/rejection_reason
                        (risk.md §5e), Execution Result/Fill semantics,
                        business rejection/denial fact. Error Handling
                        KHÔNG redefine, KHÔNG collapse những outcome đó
                        (§"Nguyên tắc chi phối"/§4/§7).
Account lifecycle/domain state (account.md)  VẪN authority DUY NHẤT.
ADR-017                VẪN authority DUY NHẤT cho architecture-level
                        Custody & Signing Trust Boundary VÀ retry/
                        idempotency scope liên quan (§8) — Error
                        Handling KHÔNG redefine (§1/§5).
Retry/idempotency authority hiện hành (I-10, Package 1.3-D, ADR-017
                        §8)  VẪN authority — Error Handling KHÔNG
                        establish policy rộng, KHÔNG assign/reassign
                        ownership (§5).
ADR-027 / logging.md   VẪN authority cho Logging — Error Handling
                        KHÔNG redefine log level/field/schema (§10).
ADR-028 / config.md    VẪN authority cho Config — Error Handling KHÔNG
                        redefine validation/startup config semantics
                        (§8). `EF-CONFIG-B-MIN-01` KHÔNG chạm.
module-registry.yaml   VẪN authority DUY NHẤT cho module identity/
                        dependency graph — KHÔNG đổi module identity/
                        edge nào.
ADR-008                VẪN authority DUY NHẤT cho ngôn ngữ theo layer.
ADR-024 / monorepo.md  VẪN authority DUY NHẤT cho repository topology.
ADR-025 / coding-standard.md  VẪN authority cho Coding Standard.
ADR-026 / naming.md    VẪN authority cho identifier naming.
```

## Non-goals (KHÔNG chọn tại v0.1 này)

```text
concrete Python exception hierarchy;
concrete Go sentinel-error/custom-error framework;
error-handling library/framework cụ thể;
retry framework;
backoff algorithm;
retry ownership reassignment;
HTTP middleware choice;
error serialization technology;
observability vendor;
Domain/Event/API outcome semantics mới;
Security architecture redesign.
```

## ADR-scope disposition

```text
Tài liệu này (`error-handling.md` v0.1) implement reversible living-
  detail semantics ĐÃ được `ADR-029` v0.2 (`Approved`) explicitly
  delegate — KHÔNG một mục nào tại §1–§14 trên tự nó tạo một architecture
  decision mới, một published-contract semantic mới, một module
  responsibility/dependency change, một Platform Invariant change, hay
  bất kỳ quyết định ADR-required nào khác vượt ngoài phạm vi ADR-029 đã
  Approved. Mọi rule tại đây LÀ reversible detail-level convention (error
  taxonomy, cause preservation, boundary translation mechanics, retry-
  related classification KHÔNG PHẢI ownership, logging/security
  interaction, Python/Go idiomatic guidance), đúng loại nội dung
  ADR-029 §3 đã explicitly defer tới `error-handling.md`.
KHÔNG rule nào tại v0.1 này độc lập trigger Chapter 0 §4b ngoài phạm vi
  ADR-029 đã cover — KHÔNG tạo ADR-030 tại transaction này.
Mọi thay đổi SEMANTIC tương lai vào tài liệu này (KHÔNG PHẢI mọi sửa —
  CHỈ khi đổi Ý NGHĨA rule) PHẢI tự chạy lại ADR Scope Rule (Chapter 0
  §4b) hiện hành TẠI chính thời điểm đổi — KHÔNG suy diễn "reversible/
  refactor-class" LÀ đủ để miễn ADR (đúng lesson `ADR-025`/`ADR-026`/
  `ADR-027`/`ADR-028`/`ADR-029` §3, KHÔNG redefine). Vì baseline áp
  dụng cho MỌI module, phần lớn semantic update sẽ thỏa lại vế ">1
  module" — Error Handling KHÔNG generally "ADR Not Required."
```

## Change history

```text
v0.1  2026-08-12  Established — vai trò: `Phase 1.5 Error Handling
      Convention v0.1 Authoring Executor`. Bounded EF-TXN-002 category
      transaction (Error Handling only). Verify trực tiếp trước khi
      author: current HEAD (c39392942ee3a53dcbfd7ad1f34931b3bea455c4),
      ADR-029 v0.2 Approved identity (blob
      9c8877d3e16a54c1908c37f1b214ef185744cd9c),
      `docs/engineering/error-handling.md` KHÔNG tồn tại trước đây.
      Established 15 mục: error categories (7 category nhỏ semantic,
      KHÔNG invent business-outcome category), expected vs unexpected
      (programming defect KHÔNG silently convert thành success), cause
      preservation (giữ causal context xuyên boundary, KHÔNG mandate
      library), boundary translation (technical representation CHỈ,
      KHÔNG redefine domain/API outcome/published-contract semantics),
      retry-related classification (metadata support CHỈ, KHÔNG
      ownership/policy/idempotency override, KHÔNG suy diễn từ
      exception type), timeout/cancellation (phân biệt khi có ích,
      KHÔNG invent giá trị/retry behavior), partial failure (KHÔNG
      silent full-success, CHỈ surface qua representation đã hợp lệ,
      fail explicitly nếu KHÔNG có representation), startup/config
      failures (align config.md §7, KHÔNG redefine), security/
      redaction (KHÔNG expose secret, KHÔNG chọn vendor), logging
      interaction (align logging.md, KHÔNG redefine level/schema,
      tránh duplicate-log), Python guidance (exception idiomatic,
      KHÔNG mandate hierarchy), Go guidance (error-return idiomatic,
      panic CHỈ cho unrecoverable defect, KHÔNG mandate framework),
      user-facing/internal representation (KHÔNG expose internal
      detail, theo published contract), explainability (category/
      boundary/cause/translation/retry-source xác định được, KHÔNG
      mandate tooling), authority boundaries (Domain/Event/API/
      Account/ADR-017/retry-idempotency/Logging/Config/module-registry/
      ADR-008/monorepo/Coding-Standard/Naming — tất cả preserved riêng
      biệt). Non-goals liệt kê tường minh. ADR-scope disposition: v0.1
      implement living-detail authority ĐÃ delegate bởi ADR-029, KHÔNG
      rule nào độc lập trigger Chapter 0 §4b mới, KHÔNG tạo ADR-030.
      KHÔNG chạm `ADR-029` (Approved, immutable)/`ADR-028`/`config.md`/
      `ADR-027`/`logging.md`/`ADR-026`/`naming.md`/`ADR-025`/
      `coding-standard.md`/`ADR-024`/`monorepo.md`/`ADR-008`/
      `ADR-017`/`module-registry.yaml`/Domain Contract/Constitution/
      Phase 1.5 rules. `EF-CONFIG-B-MIN-01` KHÔNG chạm, KHÔNG đóng.
      KHÔNG chọn framework/library/schema/vendor nào. KHÔNG bắt đầu
      Testing/CI-CD. `status: Draft` — not self-approved (`G-ORCH-002`).
      KHÔNG authorize Phase 2/LIVE.
v0.2  2026-08-12  Bounded correction, đóng `EF-ERR-A-MAJ-01`. v0.1 §7
      nói "NẾU KHÔNG tồn tại một authoritative partial-result
      representation nào ... module PHẢI fail explicitly (technical
      error)" — quá rộng: KHÔNG tồn tại MỘT representation "partial"
      riêng biệt KHÔNG chứng minh underlying outcome LÀ technical/
      programming error; Domain/Event/API authority hiện hành CÓ THỂ
      ĐÃ định nghĩa một business failure/rejection/result
      representation KHÁC cho đúng tình huống đó (vd `RiskEvaluation
      REJECTED`/`NON_EVALUABLE`, risk.md §5e) — reclassify outcome đó
      thành technical error CHỈ vì thiếu representation "partial"
      riêng LÀ vi phạm nguyên tắc chi phối. Sửa: §7 pin rõ thứ tự
      resolve — (1) KHÔNG silent full-success; (2) dùng ĐÚNG
      representation/outcome authoritative nếu Domain/Event/API
      contract hiện hành ĐÃ có cho đúng tình huống đó; (3) partial-
      result representation CHỈ dùng khi ĐÃ established bởi authority
      liên quan; (4) fail explicitly LÀM technical error CHỈ khi
      KHÔNG có representation business/domain phù hợp VÀ nguyên nhân
      gốc THẬT SỰ technical/infrastructure/programming; (5) nếu lộ ra
      một business/domain semantic CHƯA tồn tại hoặc cần published-
      contract outcome MỚI, KHÔNG tự invent tại đây — report LÀM
      contract/authority gap, route qua đúng authority VÀ tự rerun ADR
      Scope Rule nếu applicable. Nguyên tắc chi phối "technical/
      programming error ≠ domain/business outcome" giữ nguyên, KHÔNG
      suy yếu. **KHÔNG đổi:** §1 (taxonomy), §2 (expected/unexpected),
      §3 (cause preservation), §4 (boundary translation), §5 (retry-
      related classification/ownership prohibition), §6 (timeout/
      cancellation), §8 (Config startup boundary), §9 (security/
      redaction), §10 (Logging authority), §11 (Python guidance), §12
      (Go guidance), §13 (user-facing/internal representation), §14
      (explainability), §15 (authority boundaries), Non-goals, ADR-
      scope disposition. KHÔNG invent Domain/Event/API partial-failure
      state mới, KHÔNG redefine Risk/Execution/Account outcome, KHÔNG
      đổi retry ownership/idempotency, KHÔNG chọn framework/library/
      error-code schema nào. `EF-CONFIG-B-MIN-01` VẪN `OPEN — accepted
      non-blocking`, KHÔNG chạm. KHÔNG chạm `ADR-029.md` (Approved,
      immutable, verified byte-identical). `status` VẪN `Draft` — not
      self-approved (`G-ORCH-002`), KHÔNG authorize Phase 2/LIVE.
ACCEPTANCE  2026-08-12  Product Owner lifecycle approval — mechanical,
      vai trò: `Error Handling Convention v0.2 Mechanical Approval
      Recorder`. Quyết định: "APPROVE ERROR HANDLING CONVENTION V0.2
      — ACCEPT EF-ERR-B-MIN-01 AS NON-BLOCKING RESIDUAL." Reviewed
      candidate: v0.2, blob 10c1b259ec28bdfb0caa318ceffda81228a707da
      (bounded Review A re-review CLEAN, New Blocker/Major/Minor
      0/0/0, đóng `EF-ERR-A-MAJ-01`; Independent Review B trên đúng
      v0.2: New Blocker 0/New Major 0/New Minor 1 — `EF-ERR-B-MIN-01`
      (candidate/provenance wording stale "v0.1" tại nhiều mục KHÔNG
      đổi, VALID, non-blocking), `READY_FOR_PRODUCT_OWNER_DECISION`).
      `status: Draft -> Approved`, `approved_by: null -> Product
      Owner`, `approved_at: null -> "2026-08-12"`. `version` KHÔNG
      bump (pure mechanical lifecycle approval) — VẪN `0.2`.
      `EF-ERR-B-MIN-01` VẪN `OPEN — accepted non-blocking residual`,
      KHÔNG đóng, KHÔNG sửa stale "v0.1" wording tại đây — đúng
      `G-REV-004` (KHÔNG correction churn khi KHÔNG có Major/Blocker
      mới), correction riêng biệt tương lai (nếu thực hiện) sẽ đóng
      finding này. KHÔNG semantic content nào đổi (§1–§15 byte-
      equivalent ngoài banner/lifecycle metadata/change history này VÀ
      residual stale wording đã accept). Tài liệu VẪN LÀ living
      document — `Approved` KHÔNG immutable byte-for-byte như ADR;
      thay đổi SEMANTIC tương lai VẪN PHẢI tự rerun ADR Scope Rule.
      KHÔNG chạm `ADR-029` (Approved, immutable)/`ADR-028`/`config.md`/
      `ADR-027`/`logging.md`/`ADR-026`/`naming.md`/`ADR-025`/
      `coding-standard.md`/`ADR-024`/`monorepo.md`/`ADR-008`/
      `ADR-017`/`module-registry.yaml`/Domain Contract/Constitution/
      Phase 1.5 rules, KHÔNG tạo ADR-030, KHÔNG mở Engineering
      Foundation category khác, KHÔNG chọn framework/library/error-
      code schema nào, KHÔNG đóng `EF-CONFIG-B-MIN-01`, KHÔNG
      authorize Phase 2/LIVE.
```
