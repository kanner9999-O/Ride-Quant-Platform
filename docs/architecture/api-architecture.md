---
id: api-architecture
title: "Package 1.4 — API Architecture"
version: "0.5"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-05"
last_review: null
next_review: null
depends_on: ["00-governance", "02-platform-invariants", "07-module-taxonomy", "08-event-model", "09-plugin-model", "10-compatibility-capability-contract", "13-quality-gates", "14-roadmap"]
---

# Package 1.4 — API Architecture

**CONSOLIDATED STABLE (package lifecycle, 2026-08-06, Product Owner decision) — status: Draft, KHÔNG Approved/Locked.** Product Owner đã quyết định nguyên văn (as supplied in the transaction request): "APPROVE PACKAGE 1.4 V0.5 CONSOLIDATION." Decision date: 2026-08-06 (exact clock time KHÔNG được cung cấp — date-only metadata, KHÔNG một giá trị giả định nào được invent). Review evidence trên v0.5 (post `P14V04-A-MAJ-01` correction): Review A `CLEAN`, Independent Review B `CLEAN`, Blocker 0/Major 0/Minor 0. Mechanical lifecycle transaction — `version: "0.5"` UNCHANGED (no content/architecture change), `package lifecycle: candidate → Consolidated Stable`. **Preserved unchanged (byte-identical, transaction này CHỈ đổi lifecycle prose/field):** `command-query-api-surface → backtest-orchestrator` route; 17-module dependency baseline; `backtest-orchestrator.consumes` (`[event, query]`), `.emits` (`[event]`), `module_type` (`runtime_service`), `hybrid` (`null`), `owns_authoritative_state` (`deferred`); Decision authority (`decision-authority-service`); RiskEvaluation authority (`risk-gateway`); API Surface non-authority (`owns_authoritative_state: false`); §6 non-bypass invariants; current Package 1.1 v0.8/v0.9 references (§0/§1/§10, post `P14V04-A-MAJ-01`); mọi implementation exclusion. `ADR-018`/`ADR-019`/Package 1.1 (`module-registry.yaml`/`system-decomposition.md`) KHÔNG sửa. `DD-001`/VIEW-002 VẪN unresolved. `ux-architecture.md`/Package 1.6 KHÔNG sửa — VẪN `candidate`/blocked. `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi — `Consolidated Stable` LÀ package lifecycle/readiness state, KHÔNG có nghĩa artifact `Approved`/`Locked` (Chapter 0 §7.1). KHÔNG authorize implementation/Gate 2/Phase 2/LIVE.

**CANDIDATE (package lifecycle, reverted from Consolidated Stable, 2026-08-06, HISTORICAL — superseded bởi quyết định Consolidated Stable trên; current version `0.5` sau bounded correction `P14V04-A-MAJ-01`, xem v0.5 entry dưới) — status: Draft, KHÔNG Approved/Locked.** Package 1.4 v0.3 → v0.4: genuine semantic parity-transcription change — EXACT mechanical transcription của Approved [ADR-019](../adr/ADR-019.md) v0.2 (`Approved`, `approved_at: "2026-08-06"`, NAV-003 Gap A) VÀ Package 1.1's now-`Consolidated Stable` v0.8/v0.9 baseline (`module-registry.yaml`/`system-decomposition.md`) — NOT a new architecture decision, NOT a new ADR. `command-query-api-surface.depends_on` gains `backtest-orchestrator` (17th module, registered edge — Package 1.1 v0.8, Consolidated Stable) — §2.1/§2.3/§9 updated to reflect this route: exposes the non-authoritative bounded Backtest run correlation query, `backtest-orchestrator` composes the view from existing Decision (`decision-authority-service`) and RiskEvaluation (`risk-gateway`) facts, receives queries via `consumes: [event, query]`. Same precedent as the ADR-017 → Package 1.4 alignment (Package 1.2 custody/signing registration) — a genuine architectural/semantic parity change, NOT a bounded wording-only correction, reverts `package_lifecycle` from `Consolidated Stable` to `candidate`. This transaction does NOT reconsolidate — a separate Review A + Independent Review B + Product Owner consolidation decision MUST complete before this baseline returns to `Consolidated Stable`. **Preserved unchanged:** Decision authority (`decision-authority-service`), RiskEvaluation authority (`risk-gateway`), all other 16 dependency edges, `forbidden_dependencies`, `consumes: [event, query, command]`/`emits: [query, command]` of `command-query-api-surface` itself, `owns_authoritative_state: false`, every non-bypass invariant (§6), every documented gap/non-goal (§10), PAPER-only execution, LIVE Unauthorized. No field-level API path/schema/transport/caching/storage/indexing/auth mechanics chosen — architecture-level route only. `DD-001`, `backtest-orchestrator.owns_authoritative_state`, and VIEW-002 remain unresolved — untouched. ADR-018, ADR-019, and Package 1.1 (`module-registry.yaml`/`system-decomposition.md`) are NOT modified by this transaction. `ux-architecture.md`/Package 1.6 are NOT modified — remain candidate and blocked.

**v0.5 — bounded correction (2026-08-06), đóng `P14V04-A-MAJ-01`, vai trò: `Package 1.4 v0.4 Baseline-Reference Correction Executor`:** Ba tham chiếu current-normative tới Package 1.1 v0.7 (đã stale kể từ v0.4's ADR-019 alignment, module-registry.yaml/system-decomposition.md nay v0.8/v0.9 Consolidated Stable) được sửa: (a) §0 — `command-query-api-surface (module-registry.yaml v0.7...)` → `v0.8`; (b) §1 Governing authority — `system-decomposition.md v0.7 (Consolidated Stable): semantic parity với module-registry.yaml v0.7` → `system-decomposition.md v0.9 (Consolidated Stable): semantic parity với module-registry.yaml v0.8`; (c) §10 non-goals — "Bất kỳ dependency edge mới nào ngoài `module-registry.yaml` v0.7 đã đăng ký" (mâu thuẫn nội bộ với chính §2.1/§2.3/§9's `backtest-orchestrator` edge — vốn ĐÃ registered tại v0.8, KHÔNG mới) sửa thành tham chiếu đúng baseline hiện tại (`module-registry.yaml` v0.8/`system-decomposition.md` v0.9), xác nhận tường minh edge đó ĐÃ registered, KHÔNG một invention mới của Package 1.4. **KHÔNG đổi:** ADR-019 route, 17-module dependency set, contract category nào, Decision/RiskEvaluation authority, §6 non-bypass invariant, hay bất kỳ implementation detail nào — CHỈ ba tham chiếu baseline-version sửa. Tham chiếu v0.7 BÊN TRONG các bản ghi lifecycle lịch sử tường minh (banner v0.1 candidate, HISTORICAL; changelog paragraph v0.4 mô tả transition v0.7→v0.8; §12 precedent citation tới Package 1.1's chính transition đó) GIỮ NGUYÊN, KHÔNG sửa — đó LÀ mô tả trung thực trạng thái tại thời điểm lịch sử, KHÔNG PHẢI current-normative claim. `module-registry.yaml`/`system-decomposition.md`/`ADR-018`/`ADR-019`/Package 1.6 KHÔNG sửa. `package lifecycle: candidate` KHÔNG đổi — KHÔNG reconsolidate. `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi. `DD-001`/VIEW-002 VẪN unresolved.

**v0.4 — Package 1.4 ADR-019 parity transcription (2026-08-06), vai trò: `Package 1.4 ADR-019 Parity Executor`, mechanical transcription của [ADR-019](../adr/ADR-019.md) v0.2 (`Approved`) VÀ Package 1.1 v0.8/v0.9 (`Consolidated Stable`):** §2.1's registry classification block cập nhật — `command-query-api-surface.depends_on` nay 17 module (`backtest-orchestrator` thêm), nguyên văn tham chiếu `module-registry.yaml` cập nhật v0.7 → v0.8. §2.3's "16 module" → "17 module", thêm một bullet xác nhận CÓ edge tới `backtest-orchestrator` (khác biệt với các bullet "KHÔNG có edge" hiện có). §9 thêm một entry mới "Backtest Orchestrator" — route non-authoritative bounded Backtest run correlation query, `backtest-orchestrator` compose view từ Decision (`decision-authority-service`) VÀ RiskEvaluation (`risk-gateway`) fact ĐÃ tồn tại, KHÔNG tự submit/own hai loại fact đó; nhận query qua `consumes: [event, query]` (Package 1.1 v0.8 alignment). §11's `module-registry.yaml v0.7` reference cập nhật → v0.8. **KHÔNG chọn/author:** HTTP/RPC path, request/response field, pagination, filtering syntax, transport protocol, caching, storage, indexing, authentication/authorization mechanics, implementation topology — architecture-level route ONLY. **KHÔNG đổi:** Decision authority (`decision-authority-service`), RiskEvaluation authority (`risk-gateway`), 16 dependency edge còn lại, `forbidden_dependencies`, `command-query-api-surface`'s own `consumes`/`emits`/`owns_authoritative_state: false`, mọi non-bypass invariant (§6), mọi gap/non-goal (§10), PAPER-only execution, LIVE Unauthorized. `module-registry.yaml`/`system-decomposition.md`/`ADR-018`/`ADR-019` KHÔNG sửa. KHÔNG module/Domain fact/entity/event/schema mới nào tạo. `DD-001`, `backtest-orchestrator.owns_authoritative_state`, VÀ VIEW-002 VẪN unresolved. `ux-architecture.md`/Package 1.6 KHÔNG sửa — VẪN `candidate`/blocked. `status: Draft`, `approved_by: null`, `approved_at: null`, `package lifecycle: candidate` (revert từ `Consolidated Stable`, KHÔNG tự động — xem banner đầu tài liệu) KHÔNG reconsolidate tại transaction này.

**CONSOLIDATED STABLE (package lifecycle, 2026-08-05T15:16:00+07:00, Product Owner decision, HISTORICAL — superseded bởi v0.4 trên) — status: Draft, KHÔNG Approved.** Package 1.4 v0.3 đạt `Consolidated Stable` SAU: Review A (REVISE trên v0.1, đóng `P14-A-MAJ-01`/`P14-A-MAJ-02`/`P14-A-MIN-01`) → final bounded verification (CLEAN, Blocker 0/Major 0/Minor 0) → Independent Review B (CLEAN, Blocker 0/Major 0/Minor 0, consolidation readiness: READY) → Product Owner consolidation decision. Product Owner đã quyết định nguyên văn: "I approve consolidation of Package 1.4 v0.3 as the current Consolidated Stable API Architecture baseline, while preserving the command-query-api-surface as a non-authoritative routing and exposure boundary, all authoritative service, causal-lineage, compatibility, custody, security, failure and environment boundaries, all documented unresolved gaps and non-goals, the PAPER-only execution path, and LIVE Unauthorized." `Consolidated Stable` LÀ package lifecycle/readiness state (Chapter 0 §7.1) — KHÔNG có nghĩa artifact `Approved`; `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi. Mechanical lifecycle transaction — `version: "0.3"` UNCHANGED (no content/architecture change), package lifecycle: `candidate → Consolidated Stable`.

**CANDIDATE (package lifecycle, HISTORICAL — superseded bởi Consolidated Stable trên) — status: Draft, khi đó KHÔNG Consolidated Stable, KHÔNG Approved.** Package 1.4 v0.1 — candidate đầu tiên, author dựa trên Package 1.1 `Consolidated Stable` (v0.7, 25 module, module-registry.yaml/system-decomposition.md), Package 1.2 `Consolidated Stable` (v0.4), Package 1.3-A/1.3-B/1.3-C/1.3-D `Consolidated Stable` (v0.2), VÀ [`phase-1-plan.md`](phase-1-plan.md) v0.4 (`Approved`) §"Package 1.4 — API Architecture". Đây LÀ một authoring transaction, KHÔNG PHẢI một review/consolidation transaction. Chưa qua Review A/Independent Review B, chưa có Product Owner consolidation decision.

**v0.2 — bounded correction (2026-08-05), đóng ba Review A finding trên v0.1 (`P14-A-MAJ-01`/`P14-A-MAJ-02`/`P14-A-MIN-01`), KHÔNG redesign/mở rộng scope:** (a) `P14-A-MAJ-01` — §6 sửa: dependency-edge absence (§2.1/§2.3) KHÔNG còn được trình bày như bằng chứng ĐẦY ĐỦ cho caller exclusion/invocation impossibility/payload-flow exclusion/raw-secret isolation/authority non-bypass/causal authorization — `depends_on` LÀ prerequisite relation, KHÔNG PHẢI một complete caller-access/dataflow-control model; thêm bộ architecture-level invariant mới (transport KHÔNG BAO GIỜ tạo eligibility, effect-producing command PHẢI qua authoritative boundary, lineage fail-closed, secrets/signing material bị cấm khỏi API payload); (b) `P14-A-MAJ-02` — §8 sửa: bỏ claim mọi request dùng đủ ba trục Chapter 10, bỏ claim Plugin Version là trục universal, bỏ claim API Surface LÀ canonical compatibility evaluator/PHẢI tạo Compatibility Result cho mọi request — thay bằng bounded rule: compatibility evaluation VẪN thuộc module authoritative/designated đã đăng ký, API Surface CHỈ carry/route/expose evidence; (c) `P14-A-MIN-01` — §5 sửa: `emits` loại trừ `event` CHỈ chứng minh API Surface KHÔNG phải registered authoritative event emitter, KHÔNG chứng minh một transport topology cụ thể nào — transport mechanism CÓ THỂ chọn sau, exposure VẪN read-only, event identity/provenance/ordering/correction KHÔNG đổi. Mọi nội dung khác của v0.1 GIỮ NGUYÊN.

**v0.3 — micro-correction (2026-08-05), đóng residual bounded-verification finding `P14-A-MAJ-01` (hai contradiction sót lại sau v0.2), KHÔNG reopen `P14-A-MAJ-02`/`P14-A-MIN-01`, KHÔNG redesign:** (a) §2.1 — parenthetical "non-bypass enforced structurally bởi ABSENCE khỏi depends_on" (sót lại từ v0.1, KHÔNG bị v0.2 sửa) thay bằng: absence khỏi `depends_on` CHỈ xác nhận KHÔNG có registered direct prerequisite edge, KHÔNG độc lập chứng minh caller exclusion/transport access control/transitive payload flow/causal authorization/complete non-bypass — non-bypass được thiết lập bởi bộ invariant tại §6, KHÔNG PHẢI bởi riêng registry fact này. (b) §11 Independent Review B scope — criterion "script-checkable qua absence trong depends_on" (sót lại từ v0.1) thay bằng bounded criterion đòi hỏi verify CẢ HAI: registry parity/absence của unauthorized dependency edge, VÀ §6's normative invariant (authoritative acceptance, eligible lineage, authorization, fail-closed, secret confinement) — KHÔNG một mình dependency-graph script chứng minh complete non-bypass. §6 (v0.2 correction), §8 (P14-A-MAJ-02), §5 (P14-A-MIN-01) GIỮ NGUYÊN KHÔNG đổi.

## 0. Vai trò của tài liệu này — scope resolved từ controlling source (bắt buộc, yêu cầu task)

Scope resolve TRỰC TIẾP từ `phase-1-plan.md` (Approved, controlling), nguyên văn:

```text
Package ID:              1.4
Name:                     API Architecture
Purpose:                  Command/query/event contract topology cho toàn bộ platform —
                          bề mặt API mà UX Architecture (1.6) và external integration
                          (nếu có) bind vào.
Outputs:                  docs/architecture/api-architecture.md — API surface map
                          (command/query/event theo mỗi capability), versioning strategy
                          áp dụng Chapter 10 §10.3, KHÔNG schema cụ thể từng field.
Explicit non-goals:       KHÔNG author API schema chi tiết (field-level); KHÔNG chọn
                          API technology (REST/GraphQL/gRPC); KHÔNG authentication
                          implementation.
Dependencies:              1.3-A, 1.3-B, 1.3-C, 1.3-D (cần contract surface đầy đủ của
                          engine pipeline).
```

**Đây là MỘT artifact duy nhất** (`docs/architecture/api-architecture.md`) elaborate kiến trúc kỹ thuật cho ĐÚNG MỘT module đã đăng ký tại Package 1.1: `command-query-api-surface` (`module-registry.yaml` v0.8, `phase.elaborated_by: "1.4"`). Package 1.4 KHÔNG author Package 1.5 (Database Architecture) hay Package 1.6 (UX Architecture) — cả hai được liệt kê như tương lai/consumer, KHÔNG elaborate content tại đây.

**KHÔNG thuộc phạm vi tài liệu này:** authentication implementation cụ thể; RBAC/IAM product cụ thể; rate limiting implementation; API technology (HTTP/REST/GraphQL/gRPC/WebSocket); API gateway/vendor; field-level command/query/event schema; deployment/network topology; retry/timeout timing value cụ thể; observability implementation; review-evidence persistence (Package 1.5, KHÔNG elaborate); UX behavior/component (Package 1.6, KHÔNG elaborate); LIVE activation.

## 1. Governing authority

```text
Constitution (Chapter 0–14, Locked):              highest architectural authority, đặc
                                                    biệt I-1 (Explainability), I-3 (No
                                                    Repaint), I-4 (Strategy Isolation), I-6
                                                    (Fail-Safe by Scope), I-7 (Plugin
                                                    Non-Bypass), I-8 (Kill Switch), I-11
                                                    (Secrets & Custody Isolation)
Chapter 8 (Event Model, Locked):                   §8.1 event log authoritative source;
                                                    §8.2 append-only event record; §8.6
                                                    schema versioning delegated tới
                                                    Chapter 10
Chapter 9 (Plugin Model, Locked):                  §9.1 four-tier identity; §9.6
                                                    Permission boundary (Declaration/Grant/
                                                    Enforcement/Verification) — áp dụng
                                                    cho mọi module tương tác qua contract,
                                                    đặc biệt Plugin
Chapter 10 (Compatibility & Capability
  Contract, Locked):                               §10.3 version compatibility (ba trục
                                                    độc lập, breaking theo published
                                                    contract surface); §10.4 Compatibility
                                                    Result artifact bất biến; controlling
                                                    authority cho §8 (API contract
                                                    governance) dưới đây
Approved ADR-007 (Vision scope):                   internal/single-team, crypto-only
                                                    Phase 0-3 — LIVE Unauthorized cho tới
                                                    governance decision riêng
Approved ADR-012 (Account-to-Boundary
  Cardinality):                                    canonical Account Boundary/environment
                                                    model — KHÔNG redefine tại đây
Approved ADR-017 (Custody & Signing Trust
  Boundary, v0.2):                                 Option C — custody-signing-service sole
                                                    direct-credential-use authority; API
                                                    Surface KHÔNG có edge tới module này
                                                    (§6 dưới)
module-registry.yaml v0.8 (Consolidated
  Stable, 25 module):                              module identity/taxonomy/dependency
                                                    authority — KHÔNG redefine tại đây;
                                                    `command-query-api-surface` ĐÃ đăng
                                                    ký, `phase.elaborated_by: "1.4"`
system-decomposition.md v0.9 (Consolidated
  Stable):                                         semantic parity với module-registry.yaml
                                                    v0.8 — KHÔNG redefine tại đây
security-custody-baseline.md v0.4 (Package
  1.2, Consolidated Stable):                       custody/signing trust boundary — Package
                                                    1.4 elaborate CHỈ non-bypass exposure
                                                    treatment, KHÔNG redefine
risk-execution-architecture.md v0.2 (Package
  1.3-D, Consolidated Stable):                     Risk Gateway/Execution Engine/Execution
                                                    Result Processor/Fill Processor/
                                                    Position Projection authority — consumed
                                                    như một forward reference, KHÔNG redefine
Package 1.3-A/1.3-B/1.3-C (Consolidated
  Stable):                                         Data/Structure/Regime/Feature/Context/
                                                    Decision boundary — consumed như forward
                                                    reference, KHÔNG redefine
phase-1-plan.md v0.4 (Approved):                   Phase 1 work-breakdown/package-boundary
                                                    authority, nguồn CHÍNH của §0 scope
                                                    resolution
Package 1.4 (tài liệu này):                        technical elaboration authority ONLY,
                                                    cho command-query-api-surface — API
                                                    exposure/routing boundary
```

Package 1.4 KHÔNG redefine domain entity/event semantics, module identity/taxonomy, hay bất kỳ package đã Consolidated Stable nào — mọi nội dung dưới đây chỉ **elaborate** kiến trúc kỹ thuật trong ranh giới đã pin.

## 2. Module boundary — Command/Query/Event API Surface (module DUY NHẤT gán cho Package 1.4)

### 2.1 Registry classification (bảo toàn nguyên vẹn, KHÔNG sửa registry)

```text
module_id:                 command-query-api-surface
name:                      Command/Query/Event API Surface
module_type:               runtime_service
owns_authoritative_state:  false
consumes:                  event, query, command
emits:                     query, command
depends_on:                market-reference-service, market-data-ingestion,
                           structure-engine, raw-regime-engine, feature-engine,
                           context-aggregator, account-service, strategy-engine,
                           decision-authority-service, risk-gateway, execution-engine,
                           execution-result-processor, fill-processor,
                           position-projection, replay-integration-service,
                           review-evidence-service, backtest-orchestrator (v0.4,
                           ADR-019 v0.2 Approved / Package 1.1 v0.8 Consolidated
                           Stable alignment — NAV-003 Gap A query-exposure route)
forbidden_dependencies:    (none registered tại registry — absence khỏi `depends_on`
                           (v0.3 correction, đóng `P14-A-MAJ-01` residual) xác nhận
                           KHÔNG có registered direct prerequisite edge tới
                           custody-signing-service/exchange-adapter/strategy-plugin-
                           host/decision-evaluation-engine; absence đó, TỰ THÂN, KHÔNG
                           độc lập chứng minh caller exclusion, transport access
                           control, transitive payload flow, causal authorization, hay
                           complete non-bypass — non-bypass được thiết lập bởi bộ
                           authoritative-boundary/lineage/authorization/fail-closed/
                           secret-confinement invariant tại §6, KHÔNG PHẢI bởi riêng
                           registry fact này)
plugin_relation:           none
security_classification:   trust_boundary_candidate
phase:                     { identified_in: "1.1", elaborated_by: "1.4" }
```

**Xác nhận tường minh (bắt buộc, yêu cầu task):** classification, `depends_on`, `emits`/`consumes`, VÀ `phase.elaborated_by: "1.4"` trên đây LÀ nguyên trạng từ `module-registry.yaml` v0.8 (Consolidated Stable) — Package 1.4 KHÔNG sửa/redefine bất kỳ field nào trong số này, KHÔNG tự thêm/bớt một dependency edge nào (v0.4 CHỈ transcribe edge ĐÃ registered qua ADR-019/Package 1.1 alignment, KHÔNG tự invent).

### 2.2 Authority status — exposure/routing boundary, KHÔNG business authority (bắt buộc, yêu cầu task)

```text
API Surface owns_authoritative_state: false — module KHÔNG sở hữu bất kỳ authoritative
  business state nào (Decision, Trade Intent, RiskEvaluation, Execution Intent, Order,
  ExecutionResult, Fill, Position, Account, credential/signing fact — tất cả thuộc
  authority của module registered elaborate riêng, KHÔNG đổi bởi Package 1.4).

API Surface LÀ routing/exposure layer THUẦN TÚY (module-registry.yaml notes, nguyên
  văn: "routing/exposure, KHÔNG business logic riêng") — nhận command/query/event từ
  caller, route/expose tới đúng module authoritative/projection đã đăng ký tại
  `depends_on`, KHÔNG tự đánh giá/quyết định business outcome.

implements_capabilities: [] / serves_contexts: [] (registry, KHÔNG đổi) — API Surface
  KHÔNG phải một capability/domain-context owner riêng, tránh silent invention một
  capability identity cạnh tranh ngoài context-map.yaml (Chapter 4 §4.2).
```

### 2.3 Dependency và forbidden-dependency treatment (bảo toàn, KHÔNG mở rộng)

`depends_on` (17 module, nguyên trạng — v0.4 cập nhật khớp `module-registry.yaml` v0.8, `backtest-orchestrator` thêm qua ADR-019/Package 1.1 alignment, KHÔNG một lựa chọn tự ý của Package 1.4) là danh sách ĐẦY ĐỦ module mà API Surface được phép route/expose tới — Package 1.4 KHÔNG tự thêm dependency edge nào ngoài danh sách ĐÃ registered này (§9 dưới, "Do not invent new dependency edges beyond Package 1.1"). Đáng chú ý (bắt buộc xác nhận):

```text
CÓ edge tới `backtest-orchestrator` (v0.4, ADR-019 v0.2 Approved, Package 1.1 v0.8
  Consolidated Stable alignment — NAV-003 Gap A) — API Surface route/expose query tới
  bounded Backtest run correlation view; `backtest-orchestrator` compose view từ
  Decision (`decision-authority-service`)/RiskEvaluation (`risk-gateway`) fact ĐÃ tồn
  tại, KHÔNG tự authoritative cho hai loại fact đó (§9 dưới cho boundary đầy đủ).
KHÔNG có edge tới `custody-signing-service` — API Surface KHÔNG THỂ route/expose trực
  tiếp tới module custody/signing (§6).
KHÔNG có edge tới `exchange-adapter` — cùng nguyên tắc, cộng với exchange-adapter VẪN
  functionally unelaborated (Package 1.2 §7/§14).
KHÔNG có edge tới `strategy-plugin-host` hay `decision-evaluation-engine` — API Surface
  KHÔNG route/expose trực tiếp logic plugin-hosted/non-authoritative evaluation (§6).
KHÔNG có edge tới `paper-execution-boundary` trực tiếp — tương tác (nếu có) CHỈ qua
  `execution-engine`/`execution-result-processor` đã đăng ký.
```

## 3. Command boundary (bắt buộc, yêu cầu task — architecture-level, KHÔNG field-level schema)

```text
Authentication/identity context CARRIED, KHÔNG invented bởi API: API Surface CHỈ mang
  (carry) identity/authentication evidence đã cấp bởi cơ chế bên ngoài (concrete
  mechanism deferred, §10) tới module authoritative liên quan — KHÔNG tự phát minh
  identity claim, KHÔNG tự cấp quyền dựa trên việc sở hữu transport connection (cùng
  nguyên tắc "transport KHÔNG BAO GIỜ tự thân là authority" đã pin tại
  security-custody-baseline.md §5/ADR-017 §7, áp dụng ĐỒNG NHẤT cho API transport).

Authorization evidence REQUIRED nơi controlling architecture yêu cầu: mọi command chạm
  tới một module đã đăng ký authorization/eligibility validation riêng (vd. Risk
  Gateway's RiskEvaluation, custody-signing-service's SigningAuthorizationEvidence,
  §4a.4 Package 1.2) PHẢI mang/tham chiếu đúng evidence đó — API Surface KHÔNG tạo
  evidence thay, KHÔNG bypass yêu cầu đó, CHỈ relay.

Command routing: API Surface's `consumes: [event, query, command]` / `emits: [query,
  command]` (registry) xác nhận vai trò pass-through — nhận command từ caller, route
  (emit) tới đúng module trong `depends_on` sở hữu authoritative state cho domain
  concept liên quan (vd. `account-service` — `consumes: [command]` tại registry, module
  DUY NHẤT route Account command tới). API Surface KHÔNG tự route command tới một
  module KHÔNG có trong `depends_on`.

API Surface KHÔNG evaluate Decision, Risk, execution eligibility, hay custody
  eligibility: các quyết định đó thuộc authority riêng biệt ĐÃ pin — Decision Authority
  Service (Package 1.3-C, Consolidated Stable), Risk Gateway (Package 1.3-D §4,
  Consolidated Stable), Execution Engine (Package 1.3-D §5), custody-signing-service
  (Package 1.2 §4a.2/§4a.5-§4a.8, Consolidated Stable) — API Surface CHỈ route command
  tới; KHÔNG có logic đánh giá song song hay thay thế bất kỳ authority nào trong số
  này.

Transport acceptance ≠ business acceptance: API Surface nhận command thành công qua
  transport (vd. request được route hợp lệ) KHÔNG ngụ ý command đó ĐÃ được authoritative
  module chấp nhận (vd. RiskEvaluation APPROVED, SigningRequest AUTHORIZED_FOR_SIGNING,
  §4a.5 Package 1.2) — hai khái niệm PHẢI tách biệt tường minh trong mọi response/status
  exposure.

Command rejection VÀ authoritative outcome PHẢI phân biệt được: transport/validation-
  level rejection (API Surface fail TRƯỚC KHI command chạm authoritative module, §7 dưới)
  KHÁC authoritative-module-issued rejection (vd. RiskEvaluation REJECTED/NON_EVALUABLE,
  SigningFailure, §4a.5/§4a.8 Package 1.2) — API Surface PHẢI relay/preserve đúng loại
  nào đã xảy ra, KHÔNG conflate hai loại thành một generic "rejected" response.
```

**Xác nhận tường minh (bắt buộc, yêu cầu task):** KHÔNG field-level command schema nào được author tại §3 — mọi mục trên là YÊU CẦU architecture-level (WHAT phải đúng), KHÔNG concrete request/response shape.

## 4. Query boundary (bắt buộc, yêu cầu task)

```text
Query routing: tới đúng authoritative service (vd. `account-service` cho Account fact)
  HOẶC projection đã đăng ký (vd. `position-projection`, `owns_authoritative_state:
  false`, cho Position read-model; `review-evidence-service`, §9 dưới) — API Surface
  KHÔNG tự chọn nguồn khác ngoài `depends_on` đã đăng ký.

KHÔNG recompute authoritative fact bên trong API Surface: mọi authoritative fact PHẢI
  đọc TRỰC TIẾP từ nguồn đã đăng ký (Chapter 7 §7.4 Type 1/Type 2 phân biệt Compute
  Engine/Projection khỏi Runtime Service authoritative) — API Surface KHÔNG tái tính
  toán/derive một giá trị "tương đương" thay vì forward kết quả đã có (cùng nguyên tắc
  "no-recompute" đã pin cho review-evidence-service, module-registry.yaml notes).

Cursor/version/freshness evidence PHẢI bảo toàn nơi available: khi nguồn upstream mang
  cursor (replay cursor, Chapter 8 §8.5), version (Compatibility Result, Chapter 10
  §10.4), hay freshness marker, API Surface PHẢI forward evidence đó nguyên vẹn trong
  response — KHÔNG strip, KHÔNG thay bằng "latest" ngầm định (§8 dưới).

Projection output KHÔNG được trình bày như authoritative khi nguồn `owns_authoritative_
  state: false`: `position-projection` (Chapter 7 §7.4, non-authoritative theo Fill
  history) và `review-evidence-service` (read-only aggregation, KHÔNG authoritative
  fact mới) PHẢI được API Surface expose kèm marker rõ ràng "projection/non-
  authoritative", KHÔNG launder thành một response trông như authoritative source.

Stale, missing, hay ambiguous source state PHẢI fail closed nơi controlling
  architecture yêu cầu (I-6 Fail-Safe by Scope, Chapter 2 Locked, nguyên văn: "Khi
  không thể xác định tính đúng đắn của dữ liệu... hệ thống phải chuyển scope đó về
  trạng thái an toàn") — API Surface KHÔNG tự suy diễn một giá trị thay thế khi nguồn
  authoritative KHÔNG resolve được tại thời điểm query.
```

## 5. Event and streaming exposure (bắt buộc, yêu cầu task — KHÔNG design WebSocket/SSE/Kafka implementation)

```text
Xác nhận tường minh (bắt buộc, v0.2 correction, đóng `P14-A-MIN-01`): registry fact
  `command-query-api-surface.emits: [query, command]` (KHÔNG bao gồm `event`) chứng
  minh CHÍNH XÁC một điều — API Surface KHÔNG được registered như một authoritative
  event emitter (Chapter 8, module-registry.yaml) — fact này KHÔNG chứng minh, VÀ
  KHÔNG được diễn giải thành, một transport topology cụ thể nào (vd. polling-only,
  request/response-only, hay loại trừ streaming). Event/streaming exposure (nếu có)
  CÓ THỂ dùng bất kỳ transport mechanism nào được chọn SAU tại một transaction riêng
  (§14 gap, KHÔNG author tại đây) — bất kể mechanism nào được chọn, exposure đó VẪN
  read-only từ góc độ API authority (API Surface KHÔNG author/emit event mới dưới BẤT
  KỲ transport nào); KHÔNG transport mechanism nào được phép biến API Surface thành
  một event authority — registry's `emits` field VẪN LÀ nguồn xác nhận DUY NHẤT cho
  authority status đó, KHÔNG một implementation choice nào override được.

Read-only event/stream exposure: mọi event stream expose cho client LÀ relay/read-
  surface của event đã authoritative-published bởi module sở hữu (`consumes: [event]`
  — input để re-expose qua `query`), KHÔNG một event-authoring path độc lập.

Preservation của identity/ordering/correction/provenance: append-only event record
  (Chapter 8 §8.2, Locked) VÀ correction lineage (`supersedes_fact_ref` pattern dùng
  xuyên suốt Domain Contract, vd. account.md §11) PHẢI giữ nguyên khi expose qua API —
  API Surface KHÔNG reorder, KHÔNG drop correction record, KHÔNG merge/collapse identity
  khác nhau thành một.

KHÔNG mutation hay rewriting authoritative event nào: I-3 No Repaint (Chapter 2,
  Locked) — "một output đã publish KHÔNG được sửa hoặc xóa" — áp dụng ĐỒNG NHẤT cho
  API exposure layer, KHÔNG riêng compute engine gốc.

Client disconnection, retry, và resumption LÀ transport concern THUẦN TÚY: cùng nguyên
  tắc "transport KHÔNG BAO GIỜ tự thân là authority" — một client mất kết nối/retry/
  resume KHÔNG tạo ra, KHÔNG hủy, KHÔNG thay đổi bất kỳ authoritative fact nào; resumption
  PHẢI resolve lại đúng cursor/identity đã tồn tại, KHÔNG tái tạo effect mới.

Replay/backtest/live environment separation: `replay-integration-service` (Chapter 8
  §8.5, canonical Replay Cursor authority, Package 1.3-A) VÀ PAPER/LIVE environment field
  (đóng bất biến trên mọi entity liên quan, account.md §1/ADR-012 §2.4) đã đảm bảo tách
  biệt cấu trúc — API Surface KHÔNG trộn lẫn replay/backtest stream với live-facing
  stream, KHÔNG expose replay data như thể một live event tại thời điểm khác. Raw
  credential/signing material tuyệt đối KHÔNG BAO GIỜ vào bất kỳ stream/event exposure
  nào (§6 dưới, security-custody-baseline.md §12b, KHÔNG đổi).
```

**Xác nhận tường minh:** KHÔNG WebSocket/SSE/Kafka/message-broker implementation nào được thiết kế tại §5 — mọi mục trên là YÊU CẦU architecture-level, KHÔNG transport technology cụ thể.

## 6. Security và non-bypass (I-4/I-7/I-8/I-11, bắt buộc, yêu cầu task)

```text
Xác nhận tường minh (bắt buộc, v0.2 correction, đóng `P14-A-MAJ-01`): `depends_on`
  (module-registry.yaml) LÀ một prerequisite relation — nó khai báo module NÀO một
  module ĐƯỢC PHÉP phụ thuộc/gọi tới, KHÔNG PHẢI một complete caller-access hay
  dataflow-control model. Absence của một edge tại `depends_on` (§2.1/§2.3) LÀ registry
  fact CÓ THẬT VÀ preserved nguyên vẹn dưới đây, NHƯNG absence đó, TỰ THÂN, KHÔNG chứng
  minh đầy đủ: caller exclusion (ai được phép GỌI vào một module, khác chiều với
  depends_on); direct hay indirect invocation impossibility; payload-flow exclusion
  (dữ liệu gì CÓ THỂ chảy qua một route hợp lệ khác); raw-secret isolation; authority
  non-bypass; hay causal authorization. Các claim đó đòi hỏi bằng chứng bổ sung ngoài
  một dependency-graph fact đơn lẻ — §6 dưới đây KHÔNG còn trình bày absence-of-edge
  như bằng chứng đầy đủ cho bất kỳ mục nào trong số này.

Registry fact bảo toàn (KHÔNG đổi, script-verifiable): `command-query-api-surface.
  depends_on` KHÔNG chứa `custody-signing-service`, `exchange-adapter`,
  `strategy-plugin-host`, hay `decision-evaluation-engine`; `ux-application-shell.
  depends_on` CHỈ chứa `command-query-api-surface` (§2.1/§2.3, KHÔNG đổi). Những fact
  này LÀ tiền đề cần thiết (necessary) cho non-bypass ở tầng registry — KHÔNG PHẢI điều
  kiện đủ (sufficient) cho toàn bộ non-bypass/isolation guarantee, vốn PHẢI dựa thêm
  vào các invariant kiến trúc bên dưới, VÀ vào authority/eligibility validation thật sự
  được thực thi tại module authoritative (§3, §4a.2/§4a.7 Package 1.2, §4/§5 Package
  1.3-D — KHÔNG đổi).

Mọi command/query PHẢI đi qua module authoritative đã đăng ký (`decision-authority-
  service`, `risk-gateway`, `execution-engine`, v.v.) — I-7 Plugin Non-Bypass (Chapter
  2, Locked, nguyên văn: "Plugin chỉ tương tác qua published contracts... Prohibited:
  Plugin gọi trực tiếp implementation nội bộ hoặc mutable state của module khác") ĐÒI
  HỎI cả route hợp lệ (registry) LẪN validation thật tại authority đó (§3) — KHÔNG một
  mình route absence.

Raw exchange credential VÀ signing material: registry fact (API Surface KHÔNG có
  dependency edge tới `custody-signing-service`/`exchange-adapter`) LÀ MỘT layer bảo
  vệ, KHÔNG PHẢI toàn bộ bảo đảm — bảo đảm ĐẦY ĐỦ đến từ VIỆC custody-signing-service
  (Package 1.2 §4a.2/§4a.5, Consolidated Stable) tự thân KHÔNG BAO GIỜ trả raw secret
  qua bất kỳ published contract nào (SigningOutcome), CỘNG VỚI invariant bắt buộc
  "secrets/signing material bị cấm khỏi API payload" dưới đây — hai lớp kết hợp, KHÔNG
  CHỈ dependency-edge absence đơn lẻ.

API VÀ UX tương tác với custody signing: `ux-application-shell.depends_on:
  [command-query-api-surface]` (registry, edge DUY NHẤT được phép) VÀ
  `command-query-api-surface.depends_on` KHÔNG chứa `custody-signing-service` (registry
  fact, trên) — hai fact NÀY, kết hợp với việc KHÔNG module nào khác trong registry
  cung cấp một route thay thế, LÀ căn cứ cho việc UX/API KHÔNG có route hợp lệ tới
  custody signing; đây là kết luận rút ra từ TOÀN BỘ dependency graph registry (script-
  verifiable), KHÔNG một tuyên bố tổng quát rằng "absence của MỘT edge" tự nó loại trừ
  mọi invocation path có thể có.

Plugin capability qua API: API Surface KHÔNG có edge tới `strategy-plugin-host`/
  `decision-evaluation-engine` (§2.3) — route qua API KHÔNG cấp thêm published contract
  nào cho plugin logic ngoài những gì Chapter 9/Package 1.3-C đã established; plugin
  VẪN CHỈ tương tác qua published contract đã pin tại Package 1.3-C, KHÔNG đổi. Đây là
  registry-level fact hỗ trợ non-bypass, KHÔNG PHẢI toàn bộ bảo đảm — bảo đảm đầy đủ
  vẫn phụ thuộc invariant/authority validation bên dưới.

**Architecture-level invariant bổ sung (bắt buộc, v0.2 correction, đóng `P14-A-MAJ-01` —
KHÔNG field-level lineage schema, KHÔNG authorization protocol, KHÔNG middleware,
KHÔNG token format, KHÔNG network topology):**

```text
API transport KHÔNG BAO GIỜ tự tạo Decision, Risk, execution, custody, hay signing
  eligibility — cùng nguyên tắc "transport KHÔNG BAO GIỜ tự thân là authority" đã pin
  tại security-custody-baseline.md §5/ADR-017 §7, áp dụng ĐỒNG NHẤT cho API transport
  layer.

Mọi effect-producing command PHẢI được chấp nhận VÀ validate bởi đúng authoritative
  owning boundary của nó (Decision Authority Service/Risk Gateway/Execution Engine/
  custody-signing-service tùy domain concept) — API Surface route KHÔNG thay thế
  validation đó.

Execution-affecting route PHẢI bảo toàn eligible authoritative lineage VÀ correlation
  về đúng chuỗi Decision → Risk → Execution đang kiểm soát (causation_refs chain, §3/
  §4a Package 1.3-D) — API Surface KHÔNG được route một effect-producing command tách
  rời khỏi lineage đó.

Lineage missing, stale, invalidated, ambiguous, duplicated, unauthorized, hay causally-
  unrelated PHẢI fail closed TẠI authoritative boundary (I-6 Fail-Safe by Scope, Chapter
  2, Locked) — KHÔNG tại API Surface bằng một quyết định thay thế.

API validation hay transport acceptance KHÔNG THỂ thay thế authoritative eligibility
  (§3 trên, "transport acceptance ≠ business acceptance") — một request được API
  Surface chấp nhận về mặt transport/structural KHÔNG ngụ ý eligibility đã confirm.

Secrets VÀ signing material PHẢI bị reject khỏi public/API payload VÀ giữ nguyên
  confined trong custody boundary dưới Package 1.2 (§4a, Consolidated Stable) — API
  Surface KHÔNG BAO GIỜ relay, log, hay echo lại raw secret/signing material trong bất
  kỳ request/response nào, kể cả lỗi.
```

Environment VÀ Account Boundary isolation bảo toàn: `account_boundary_ref`
  (ADR-012 §2.1, canonical, exactly-one-boundary) VÀ `environment` (PAPER|LIVE, bất
  biến, account.md §8) KHÔNG bị API Surface redefine hay bypass — mọi command/query
  route qua API PHẢI mang/tôn trọng đúng boundary/environment scope đã pin, KHÔNG suy
  diễn ngầm.

PAPER VÀ LIVE VẪN tách biệt: cùng cấu trúc identity-level (environment field bất biến)
  đã pin tại Package 1.2 §8/Package 1.3-D — API Surface KHÔNG thêm cơ chế mới, KHÔNG
  trộn hai scope.

LIVE VẪN Unauthorized: Package 1.4 KHÔNG authorize LIVE execution dưới bất kỳ hình
  thức nào — KHÔNG thêm dependency edge `execution-engine → exchange-adapter`, KHÔNG
  activate venue-submission path nào (ADR-017 §9a Stage 2, KHÔNG active).
```

## 7. Error và failure semantics (bắt buộc, yêu cầu task — KHÔNG concrete error code/HTTP status mapping)

Sáu category PHẢI phân biệt được ở mức architecture (KHÔNG concrete code):

```text
Transport failure:              request KHÔNG tới được API Surface (connectivity/network)
                                 — TRƯỚC KHI bất kỳ xử lý logic nào bắt đầu.
Validation failure:              request tới API Surface NHƯNG KHÔNG đạt structural/
                                 shape requirement TRƯỚC KHI chạm module authoritative
                                 (vd. missing bounded category, malformed correlation) —
                                 KHÔNG PHẢI một business/domain judgment.
Authorization rejection:         identity/authorization evidence missing, invalid, stale,
                                 hay KHÔNG đủ điều kiện route (I-6 fail-closed) — xảy ra
                                 TRƯỚC KHI hoặc TẠI boundary của module authoritative,
                                 KHÁC domain rejection dưới.
Domain rejection:                module authoritative TỰ NÓ decline theo đúng business
                                 rule đã pin (vd. RiskEvaluation REJECTED/NON_EVALUABLE,
                                 Account SUSPENDED reject action mới, Package 1.3-D §4a/
                                 Package 1.2 §4.4) — API Surface CHỈ relay, KHÔNG tự
                                 phát sinh loại rejection này.
Authoritative processing
  failure:                       module authoritative NHẬN request hợp lệ NHƯNG xử lý
                                 THẤT BẠI phía nó (vd. SigningFailure, §4a.5 Package 1.2)
                                 — KHÁC domain rejection (request bị từ chối vì
                                 business rule) VÀ khác unknown outcome dưới.
Unknown/unresolved outcome:      local certainty KHÔNG đủ để xác nhận thành công hay
                                 thất bại (vd. UNKNOWN_OUTCOME, §4a.5/§4a.9 Package 1.2)
                                 — API Surface PHẢI relay đúng category này, KHÔNG BAO
                                 GIỜ tự diễn giải thành success/failure khi nguồn chưa
                                 xác nhận, PHẢI đòi hỏi reconciliation đúng nguyên tắc
                                 đã pin tại module authoritative liên quan.
```

**Xác nhận tường minh:** KHÔNG error code, HTTP status mapping, hay exception taxonomy cụ thể nào được author tại §7 — mọi mục trên là phân loại architecture-level BẮT BUỘC PHẢI phân biệt được, KHÔNG concrete representation.

## 8. API contract governance (bắt buộc, yêu cầu task — KHÔNG OpenAPI/GraphQL/protobuf schema)

```text
Xác nhận tường minh (bắt buộc, v0.2 correction, đóng `P14-A-MAJ-02`): Chapter 10 §10.3's
  ba trục ĐỘC LẬP (Event Contract version, schema_version, Plugin Version) áp dụng THEO
  ĐÚNG artifact loại của chúng — KHÔNG PHẢI mọi API request đều mang/dùng đủ CẢ BA trục;
  Plugin Version CHỈ áp dụng cho artifact/interaction liên quan Plugin (Chapter 9 §9.1),
  KHÔNG PHẢI một trục universal cho mọi API request. API Surface KHÔNG PHẢI canonical
  compatibility evaluator VÀ KHÔNG bắt buộc tạo một Compatibility Result (Chapter 10
  §10.4) cho MỌI request — compatibility evaluation VẪN thuộc authority của module
  registered authoritative/designated bởi controlling architecture cho đúng contract
  đó (vd. Plugin Contract compatibility — Chapter 9 §9.6, KHÔNG API Surface).

Versioned published contract (bounded rule): mọi published API contract (command/
  query/event category API Surface expose) PHẢI identify đúng contract/schema version
  áp dụng của nó theo controlling contract liên quan (Chapter 8 §8.2.5 Event Contract
  version cho event; Chapter 8 `schema_version` cho payload schema) — KHÔNG hardcode
  format cụ thể tại đây (Chapter 10 §10.3, nguyên văn).

Backward compatibility policy: breaking change PHẢI xác định theo published contract
  SURFACE, KHÔNG theo internal implementation (Chapter 10 §10.3, nguyên văn) — mọi
  contract API Surface expose PHẢI khai báo tường minh chiều compatibility yêu cầu
  (backward/forward, §10.3.1); THIẾU declaration → invalid declaration → `eligible:
  false` (I-6), KHÔNG được suy diễn mặc định.

Compatibility evaluation ownership (bounded rule): đánh giá compatibility (Compatibility
  Result, Chapter 10 §10.4 — artifact bất biến mang evaluation provenance, ai đánh giá/
  theo luật nào, §10.4.1) VẪN thuộc module authoritative/designated ĐÃ đăng ký cho đúng
  contract đó — API Surface KHÔNG tự tạo, KHÔNG override, KHÔNG độc lập author một
  compatibility authority mới. API Surface CHỈ carry, route, VÀ expose compatibility
  evidence (Compatibility Result đã tồn tại) nơi controlling architecture yêu cầu —
  KHÔNG tự đánh giá thay. Absence hay ambiguity của compatibility evidence bắt buộc
  PHẢI fail closed (I-6) HOẶC được route tới đúng module sở hữu để đánh giá — API
  Surface KHÔNG tự quyết định thay.

Deprecation evidence: một contract element `deprecated` nhưng còn giữ CHƯA breaking,
  NHƯNG việc gỡ bỏ nó LÀ breaking VÀ PHẢI theo đúng chu kỳ đã cam kết (Chapter 10
  §10.3.1, nguyên văn) — API Surface PHẢI ghi nhận VÀ expose evidence deprecation đó
  (trạng thái, chu kỳ cam kết), KHÔNG âm thầm gỡ.

Idempotency VÀ correlation preservation: mọi command relay qua API Surface PHẢI bảo
  toàn đúng logical identity xuyên retry — cùng nguyên tắc I-10 đã established cho
  SigningRequest (Package 1.2 §4a.6: "một logical signing request xuyên retry — retry
  KHÔNG tạo một logical request MỚI") VÀ execution attempt (Package 1.3-D) — API Surface
  KHÔNG tự phát minh idempotency scheme mới, CHỈ preserve identity/correlation đã pin
  tại module authoritative.

KHÔNG mutable-latest substitution: cùng nguyên tắc `AccountCurrentView` KHÔNG BAO GIỜ
  authoritative (account.md §7/§13) — API Surface KHÔNG được present một "latest"
  mutable view như thể thay thế nguồn append-only authoritative; mọi read PHẢI resolve
  đúng cursor/version đã yêu cầu, KHÔNG một "current state" ngầm định thay thế.

Audit/provenance cho exposed command VÀ outcome: I-1 Explainability (Chapter 2, Locked)
  áp dụng cho lớp exposure — hành động có ý nghĩa (command route, outcome relay) PHẢI
  truy vết được, cùng nguyên tắc audit trail requirement đã pin cho custody/signing
  (Package 1.2 §4a.11/§12) VÀ account-service (§12) — API Surface KHÔNG author audit log
  schema/storage cụ thể (forbidden scope, §10), CHỈ pin YÊU CẦU audit trail phải tồn
  tại cho command/outcome exposure.
```

**Xác nhận tường minh:** KHÔNG OpenAPI, GraphQL schema, hay protobuf definition nào được author tại §8 — mọi mục trên là YÊU CẦU governance ở mức architecture (WHAT phải đúng theo Chapter 10), KHÔNG implementation.

## 9. Interaction boundaries (bắt buộc, yêu cầu task — KHÔNG invent dependency edge ngoài Package 1.1)

```text
Account Service:                 `depends_on` (registry) — route Account command/query;
                                  API Surface KHÔNG tự resolve `credential_reference`
                                  (Account Service authority, Package 1.2 §4, KHÔNG đổi).

Market/reference VÀ analytical
  read source (market-reference-
  service, market-data-ingestion,
  structure-engine, raw-regime-
  engine, feature-engine,
  context-aggregator):            `depends_on` (registry) — read/query surface CHỈ,
                                  KHÔNG business command path (các module này KHÔNG
                                  consume command theo registry).

Strategy/Decision module
  (strategy-engine,
  decision-authority-service):     `depends_on` (registry) — route tới Decision
                                  Authority Service's published contract CHỈ;
                                  `decision-evaluation-engine`/`strategy-plugin-host`
                                  KHÔNG có edge (§6) — non-authoritative/plugin-hosted
                                  logic KHÔNG được route trực tiếp qua API.

Risk Gateway:                     `depends_on` (registry) — Risk Gateway's `consumes:
                                  [event]`/`emits: [event]` (KHÔNG command/query trực
                                  tiếp tại registry) — API Surface consume event đã
                                  publish bởi Risk Gateway để expose qua `query` (read/
                                  observation surface); API Surface KHÔNG tự submit
                                  RiskEvaluation/Execution Intent (Risk Gateway's
                                  authority riêng, Package 1.3-D §4, KHÔNG đổi).

Backtest Orchestrator (v0.4,
  ADR-019 v0.2 Approved, Package
  1.1 v0.8 Consolidated Stable
  alignment — NAV-003 Gap A):      `depends_on` (registry, edge MỚI) — route/expose query
                                  tới `backtest-orchestrator` để tái tạo/trình bày một
                                  non-authoritative bounded Backtest run correlation
                                  view. `backtest-orchestrator.consumes: [event, query]`
                                  (Package 1.1 v0.8 alignment) — module nay directly
                                  query-answerable, cùng precedent `decision-authority-
                                  service`. Composed view correlate/fold Decision fact
                                  (`decision-authority-service`, authority KHÔNG đổi) VÀ
                                  RiskEvaluation fact (`risk-gateway`, authority KHÔNG
                                  đổi) ĐÃ tồn tại, bằng run identity (ADR-018 v0.2
                                  Approved) — `backtest-orchestrator` KHÔNG BAO GIỜ trở
                                  thành authoritative cho Decision hay RiskEvaluation
                                  content, KHÔNG tự submit/append fact nào; API Surface
                                  CHỈ route/expose, KHÔNG tự compose/interpret kết quả
                                  (§2.2, KHÔNG business logic riêng). `backtest-
                                  orchestrator.owns_authoritative_state: deferred`
                                  (DD-001) KHÔNG resolve, KHÔNG đổi bởi edge này. KHÔNG
                                  field-level query/response schema, API path, transport,
                                  caching, storage, indexing, hay auth mechanics nào
                                  chọn tại đây — architecture-level route ONLY (implement-
                                  ation design, ngoài phạm vi Package 1.4).

Execution VÀ result-processing
  module (execution-engine,
  execution-result-processor,
  fill-processor,
  position-projection):            `depends_on` (registry) — cùng nguyên tắc trên: đọc
                                  event đã publish, expose qua query; KHÔNG tự submit
                                  Order/ExecutionResult/Fill; `position-projection`
                                  expose ĐÚNG marker non-authoritative (§4).

Review Evidence Service:          `depends_on` (registry) ĐÃ có — `phase.elaborated_by:
                                  "1.5"` (Package 1.5, CHƯA elaborate) — Package 1.4
                                  CHỈ tham chiếu edge đã đăng ký như forward reference
                                  cho future Package 1.5 dependency, KHÔNG elaborate nội
                                  dung Review Evidence Service tại đây.

UX Application Shell:             `ux-application-shell.depends_on:
                                  [command-query-api-surface]` (registry, edge DUY
                                  NHẤT) — API Surface LÀ entry point CHÍNH cho Package
                                  1.6 (CHƯA elaborate); Package 1.4 KHÔNG author UX
                                  behavior/component tại đây.
```

**Gap ghi nhận (KHÔNG invent edge, bắt buộc yêu cầu task):**

```text
KHÔNG registered edge nào giữa command-query-api-surface và custody-signing-service/
  exchange-adapter — nếu tương lai có nhu cầu expose custody/signing status qua API
  (vd. credential-binding health, signing audit summary read-only), điều đó ĐÒI HỎI một
  Package 1.1 registry change riêng biệt (thẩm quyền Package 1.1, ngoài phạm vi Package
  1.4) TRƯỚC KHI Package 1.4 elaborate bất kỳ exposure nào — ghi nhận như gap, KHÔNG tự
  ý thêm dependency edge tại transaction này.
exchange-adapter VẪN functionally unelaborated (Package 1.2 §7/§14, KHÔNG package nào
  sở hữu) — bất kỳ future API exposure liên quan venue-adapter path đều carry forward
  gap này, KHÔNG resolve tại Package 1.4.
Review Evidence Service (Package 1.5) VÀ UX Application Shell (Package 1.6) VẪN CHƯA
  elaborate — interaction boundary trên CHỈ xác nhận edge ĐÃ đăng ký, KHÔNG author nội
  dung/behavior của hai package đó.
```

## 10. Preserved gaps and non-goals (bắt buộc, yêu cầu task)

**Carry forward nguyên vẹn từ upstream (KHÔNG resolve tại Package 1.4):**

```text
Kill-switch authoritative-state ownership — VẪN unresolved (Package 1.3-D §16,
  Package 1.2 §4a.10/§14 gap #5) — Package 1.4 KHÔNG claim owner nào.
In-flight signing/revocation behavior — VẪN unresolved (Package 1.2 §4a.9, §14 gap #6)
  — Package 1.4 KHÔNG resolve, KHÔNG chạm (API Surface KHÔNG có edge tới
  custody-signing-service, §6).
In-flight execution cancellation/reconciliation semantics — VẪN unresolved (Package
  1.3-D §16) — carry forward nguyên vẹn.
LIVE Domain Contract (Execution Engine ↔ Exchange Adapter, ADR-017 §8.3) — VẪN CHƯA
  author (Package 1.3-D §16, Package 1.2 §14 gap #2) — ngoài phạm vi hoàn toàn Package
  1.4.
DD-003 (PAPER-context authoritative Decision establishment mechanism) — VẪN Deferred
  (Package 1.3-D §16, Package 1.1 §11) — Package 1.4 KHÔNG resolve.
Exchange Adapter elaborating package assignment — VẪN unresolved (Package 1.1 §11) —
  ngoài phạm vi Package 1.4.
```

**Non-goals riêng của Package 1.4 (KHÔNG author tại transaction này):**

```text
Concrete authentication implementation (SSO/OAuth/JWT/session mechanism cụ thể).
Concrete RBAC/IAM product hay permission-model implementation.
Rate limiting implementation/threshold cụ thể.
HTTP/REST/GraphQL/gRPC/WebSocket/SSE technology choice.
API gateway/vendor selection.
Field-level command/query/event schema (request/response shape cụ thể).
Deployment/network topology, cloud provider, service mesh.
Retry/timeout/backoff timing value cụ thể.
Observability implementation (logging/metrics/tracing stack cụ thể).
Review-evidence persistence mechanism (thẩm quyền Package 1.5).
UX behavior/component/state management (thẩm quyền Package 1.6).
Bất kỳ dependency edge mới nào ngoài danh sách ĐÃ đăng ký tại Package 1.1 `Consolidated
  Stable` baseline hiện tại (`module-registry.yaml` v0.8 / `system-decomposition.md`
  v0.9, bao gồm cả `backtest-orchestrator` — edge đó ĐÃ registered, KHÔNG mới invent tại
  Package 1.4).
Bất kỳ registry change nào (`module-registry.yaml`/`system-decomposition.md` KHÔNG sửa).
LIVE activation dưới bất kỳ hình thức nào.
KHÔNG tạo/approve ADR tại transaction này.
KHÔNG mark Package 1.4 Consolidated Stable.
KHÔNG author Package 1.5/Package 1.6 content.
KHÔNG tuyên bố Phase 1 hoàn thành, KHÔNG mở Phase 2, KHÔNG authorize Live.
```

## 11. Review and consolidation conditions

```text
Review A scope:               API surface trace đầy đủ về Domain Contract/Use Case đã
                               tồn tại (đúng phase-1-plan.md) — KHÔNG mồ côi, KHÔNG
                               invent capability mới ngoài PR-XXX; module boundary (§2)
                               nhất quán với module-registry.yaml v0.8 (Consolidated
                               Stable) — 17 dependency edge, ĐÚNG MỘT edge mới
                               (`backtest-orchestrator`, v0.4, transcribed từ ADR-019/
                               Package 1.1 alignment, KHÔNG invent) (§2.3/§9); §6 xác
                               nhận đúng absence của edge tới custody-signing-service/
                               exchange-adapter/strategy-plugin-host/decision-
                               evaluation-engine (KHÔNG đổi bởi v0.4); mọi gap (§10)
                               carry forward trung thực, KHÔNG silently resolved.
Independent Review B
  scope:                      Độc lập xác nhận versioning strategy khớp Chapter 10
                               §10.3, KHÔNG redefine compatibility policy đã Locked (§8);
                               xác nhận KHÔNG business/custody authority nào bị
                               conflate qua API (§3/§6); xác nhận error/failure category
                               (§7) phân biệt đúng transport/validation/authorization/
                               domain/processing/unknown; xác nhận KHÔNG Decision/Risk/
                               Execution/Custody bypass nào tồn tại — bounded criterion
                               (v0.3 correction, đóng `P14-A-MAJ-01` residual) đòi hỏi
                               xác nhận CẢ HAI: (a) registry parity VÀ absence của
                               unauthorized direct dependency edge (script-checkable qua
                               `depends_on`, §2.1/§2.3); VÀ (b) §6's normative invariant
                               — authoritative acceptance, eligible lineage,
                               authorization, fail-closed behavior, VÀ custody secret
                               confinement — ĐỀU PHẢI verify; KHÔNG một mình dependency-
                               graph script chứng minh complete non-bypass; xác nhận
                               PAPER/LIVE separation VÀ LIVE Unauthorized KHÔNG bị đổi.
Product Owner decision
  point:                      Sau Review A/B CLEAN.
Consolidation condition:      Zero unresolved Blocker/Major trên baseline hiện tại (v0.3,
                               post micro-correction đóng residual P14-A-MAJ-01, VÀ
                               P14-A-MAJ-02/P14-A-MIN-01 VẪN CLOSED từ v0.2); mọi
                               capability engine đã Consolidated
                               Stable (Package 1.3-A..D) có bề mặt API tương ứng, KHÔNG
                               bỏ sót (đúng phase-1-plan.md Consolidation condition cho
                               Package 1.4).
```

**Cập nhật (2026-08-05T15:16:00+07:00, Product Owner consolidation decision) — Package 1.4 v0.3 nay `Consolidated Stable`:** review evidence hoàn tất theo đúng trình tự — Review A (REVISE trên v0.1, đóng `P14-A-MAJ-01`/`P14-A-MAJ-02`/`P14-A-MIN-01` qua v0.2 + v0.3 micro-correction) → final bounded verification (CLEAN, Blocker 0/Major 0/Minor 0) → Independent Review B (CLEAN, Blocker 0/Major 0/Minor 0, consolidation readiness: READY) → Product Owner consolidation decision (nguyên văn ở banner đầu tài liệu). `package lifecycle: candidate → Consolidated Stable` — mechanical transaction, KHÔNG architecture content nào đổi. `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi. Mọi gap tại §10 (kill-switch state ownership, in-flight signing/execution behavior, LIVE Domain Contract, DD-003, exchange-adapter assignment, và mọi non-goal khác) VẪN carry forward nguyên vẹn — Consolidated Stable KHÔNG resolve/narrow gap nào trong số đó, KHÔNG author Package 1.5/1.6, KHÔNG mở Phase 2, KHÔNG authorize LIVE.

## 12. Lifecycle treatment

```text
Package 1.4:
  version: 0.5
  status: Draft
  package lifecycle/readiness: Consolidated Stable (2026-08-06, Product Owner decision
    — v0.5 mechanical consolidation transaction, xem banner đầu tài liệu)
  Review A: CLEAN (Blocker 0/Major 0/Minor 0)
  Independent Review B: CLEAN (Blocker 0/Major 0/Minor 0)
  Product Owner consolidation decision: RECORDED (banner đầu tài liệu)

Package 1.4 v0.1 LÀ candidate đầu tiên — v0.2 LÀ bounded correction đóng ba Review A
  finding trên v0.1 (banner đầu tài liệu); v0.3 LÀ micro-correction đóng đúng residual
  contradiction sót lại của P14-A-MAJ-01 (§2.1/§11), KHÔNG invalidate/reopen phần nào
  của v0.2 KHÔNG bị finding chạm tới, KHÔNG redesign/mở rộng scope; v0.3 sau đó đạt
  `Consolidated Stable` qua transaction consolidation riêng biệt (banner đầu tài liệu,
  HISTORICAL). v0.4 LÀ một genuine semantic parity-transcription transaction (ADR-019/
  Package 1.1 v0.8 alignment — §2.1/§2.3/§9/§11 cập nhật, `backtest-orchestrator` edge
  thêm), KHÔNG một bounded wording-only correction — reverted `package lifecycle` từ
  `Consolidated Stable` về `candidate`, cùng nguyên tắc đã dùng nhất quán cho Package
  1.1's v0.7→v0.8 ADR-019 alignment. v0.5 LÀ bounded correction đóng `P14V04-A-MAJ-01`
  (ba tham chiếu current-normative sót lại tại v0.4 vẫn anchor Package 1.1 v0.7, sửa
  khớp v0.8/v0.9) — KHÔNG đổi route/dependency-set/authority/contract semantics nào,
  KHÔNG reopen v0.4's substantive content; v0.5 sau đó đạt `Consolidated Stable` qua
  transaction consolidation riêng biệt (banner đầu tài liệu) — KHÔNG version bump nào
  kèm theo mechanical lifecycle transaction này.

`Consolidated Stable` LÀ package lifecycle/readiness state (Chapter 0 §7.1) — KHÔNG có
  nghĩa artifact `Approved`/`Locked`; `status: Draft`, `approved_by: null`,
  `approved_at: null` KHÔNG đổi. Mọi gap tại §10 VẪN unresolved — v0.4 KHÔNG resolve gap
  nào trong số đó, KHÔNG resolve `DD-001`/`backtest-orchestrator.owns_authoritative_
  state`/VIEW-002, KHÔNG authorize implementation, KHÔNG unblock Package 1.6, KHÔNG mở
  Phase 2, KHÔNG authorize LIVE.
```
