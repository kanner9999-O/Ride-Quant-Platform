---
id: system-decomposition
title: "Package 1.1 — System Decomposition & Module Registry"
version: "0.8"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-03"
last_review: null
next_review: null
depends_on: ["00-governance", "02-platform-invariants", "03-engineering-principles", "04-domain-principles", "07-module-taxonomy", "08-event-model", "09-plugin-model", "10-compatibility-capability-contract", "11-adr-process", "12-approval-gates", "13-quality-gates", "14-roadmap"]
---

# Package 1.1 — System Decomposition & Module Registry

**CANDIDATE (package lifecycle, reverted from Consolidated Stable, 2026-08-06) — artifact status: Draft, KHÔNG Approved/Locked.** Package 1.1 v0.7 → v0.8: genuine semantic registry change — EXACT mechanical transcription của [ADR-019](../adr/ADR-019.md) v0.2 (`Approved`, 2026-08-06, `approved_at: "2026-08-06"`) — NAV-003 Gap A architecture decision, KHÔNG một quyết định kiến trúc mới, KHÔNG một ADR mới. Controlled bởi [ADR-018](../adr/ADR-018.md) v0.2 (`Approved`, NAV-003 Gap B classification, KHÔNG đổi) VÀ ADR-019 v0.2 (KHÔNG đổi). ĐÚNG HAI thay đổi: (1) `command-query-api-surface.depends_on += backtest-orchestrator` (MỘT edge mới — query-exposure route ADR-019 §2 quyết định); (2) `backtest-orchestrator.consumes: [event] → [event, query]` (contract-category expansion ADR-019 §2 quyết định BẮT BUỘC, precedent `decision-authority-service`). Cùng tiền lệ v0.4 → v0.5 (ADR-017 alignment) VÀ v0.6 → v0.7 (ADR-016/Package 1.2 alignment) — một genuine architectural/semantic change, KHÔNG một bounded parity/wording correction, `package_lifecycle` revert từ `Consolidated Stable` VỀ `candidate`. Transaction này KHÔNG reconsolidate — một Review A + Independent Review B + Product Owner consolidation decision RIÊNG BIỆT PHẢI hoàn tất TRƯỚC KHI baseline này trở lại `Consolidated Stable`. **Preserved unchanged:** `backtest-orchestrator.emits` (`[event]`), `module_type` (`runtime_service`), `hybrid` (`null`), `owns_authoritative_state` (`deferred`); `decision-authority-service`/`risk-gateway`'s `owns_authoritative_state` (`true`/`true`, Decision/RiskEvaluation authority KHÔNG đổi); module inventory (VẪN 25 module — KHÔNG module mới); mọi `depends_on`/`forbidden_dependencies`/`consumes`/`emits`/taxonomy/authority/phase assignment KHÁC. KHÔNG Domain entity/event/schema/authoritative fact Backtest nào tạo. `DD-001`, `backtest-orchestrator.owns_authoritative_state` (giá trị cụ thể), VÀ VIEW-002 VẪN unresolved — KHÔNG chạm bởi transaction này. Package 1.4 (`api-architecture.md`) VÀ Package 1.6 (`ux-architecture.md`) KHÔNG sửa tại transaction này — một Package 1.4 parity-transcription transaction VÀ một Package 1.6 correction transaction riêng biệt VẪN pending.

**v0.8 — semantic Package 1.1 alignment (2026-08-06), vai trò: `NAV-003 Gap A Package 1.1 Alignment Executor`, mechanical transcription của [ADR-019](../adr/ADR-019.md) v0.2 (`Approved`, 2026-08-06):** `command-query-api-surface.depends_on` thêm `backtest-orchestrator` (MỘT edge mới — đóng NAV-003 Gap A's query-exposure route, `ux-architecture.md` §13 gap #2's upstream prerequisite). `backtest-orchestrator.consumes` mở rộng `[event]` → `[event, query]` (§8, ngoại lệ tường minh mới thêm — CẦN THIẾT để module trực tiếp nhận query request từ API surface, precedent `decision-authority-service`). §5 dependency-graph text cập nhật khớp (17 module trong `command-query-api-surface.depends_on`, trước 16). Cả hai thay đổi LÀ EXACT transcription của ADR-019 §2 — KHÔNG một lựa chọn kiến trúc mới nào được thực hiện tại transaction này. **KHÔNG đổi:** `backtest-orchestrator.emits` (`[event]`), `module_type` (`runtime_service`), `hybrid` (`null`), `owns_authoritative_state` (`deferred`); `decision-authority-service`/`risk-gateway`'s authority (`owns_authoritative_state: true`/`true`, KHÔNG đổi); 25-module inventory; module identity/taxonomy/responsibility/dependency/forbidden_dependencies/security_classification của MỌI module khác; capability/context mapping; PR/UC/UX/Domain coverage totals (34/21/17/11/15); `DD-001`/`DD-003`/Structure-aware-Regime deferral/OQ-001/OQ-002/OQ-003. KHÔNG Domain entity/event/schema Backtest nào tạo. `status: Draft`, `approved_by: null`, `approved_at: null`, `package_lifecycle: candidate` (revert từ `Consolidated Stable`, KHÔNG tự động — xem banner đầu tài liệu). `api-architecture.md`/`ux-architecture.md` KHÔNG sửa tại transaction này. KHÔNG resolve `DD-001`/VIEW-002. KHÔNG authorize implementation/Gate 2/Phase 2/LIVE. Blob trước: xem MANIFEST.md cho blob transition đầy đủ.

**CONSOLIDATED STABLE (package lifecycle, 2026-08-05T13:51:00+07:00, Product Owner decision, HISTORICAL — superseded bởi v0.8 trên) — artifact status: Draft, KHÔNG Approved/Locked.** Package 1.1 v0.7 đạt `Consolidated Stable` SAU Review A CLEAN + Independent Review B CLEAN trên Package 1.2 v0.4 (custody-signing-service elaborating artifact, Blocker 0/Major 0/Minor 0) VÀ Product Owner consolidation decision. Product Owner đã quyết định nguyên văn: "I approve consolidation of Package 1.1 v0.7 as the current Consolidated Stable module-registry and system-decomposition baseline, including the assignment of custody-signing-service.phase.elaborated_by to Package 1.2, while preserving exchange-adapter.phase.elaborated_by as null, the PAPER-only execution path, and LIVE Unauthorized." `Consolidated Stable` LÀ package lifecycle/readiness state (Chapter 0 §7.1) — KHÔNG có nghĩa artifact `Approved`/`Locked`; `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi, đúng package-lifecycle/artifact-lifecycle separation đã dùng nhất quán trong toàn bộ session này. Mechanical lifecycle transaction — `version: "0.7"` UNCHANGED (no content/architecture change), `package_lifecycle: candidate → Consolidated Stable`.

**Cập nhật (2026-08-05T13:51:00+07:00, Product Owner consolidation decision) — Package 1.1 v0.7 nay `Consolidated Stable`:** Review A CLEAN + Independent Review B CLEAN trên Package 1.2 v0.4 (elaborating artifact cho custody-signing-service) hoàn tất — Blocker 0/Major 0/Minor 0. Product Owner đã quyết định (nguyên văn ở banner trên) — `package lifecycle: candidate → Consolidated Stable` (xem `module-registry.yaml` `package_lifecycle` field). Consolidated baseline chứa ĐÚNG 25 module, bao gồm `custody-signing-service` (`phase.elaborated_by: "1.2"`, sole direct exchange-credential-use authority) và `exchange-adapter` (`phase.elaborated_by: null`, raw venue-interaction evidence authority only, KHÔNG đổi). **KHÔNG đổi:** module inventory, module identity, taxonomy classification, responsibilities, authority ownership, dependencies, forbidden dependencies, module counts, phase assignment nào khác ngoài đúng assignment đã ghi nhận tại v0.7, capability/context mapping, preserved gap nào — architecture semantics của candidate v0.7 giữ nguyên byte-for-byte về nội dung kiến trúc, CHỈ lifecycle-state field/prose thay đổi. `execution-engine.depends_on` KHÔNG đổi (`risk-gateway`, `paper-execution-boundary` — KHÔNG `exchange-adapter`); PAPER path KHÔNG đổi; LIVE Unauthorized. `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi. Consolidation này KHÔNG tự động: sửa Package 1.2 v0.4 nội dung; consolidate Package 1.2; kích hoạt Execution Engine → Exchange Adapter; authorize LIVE execution; authorize implementation; resolve kill-switch-state ownership; resolve in-flight signing/revocation behavior; resolve DD-003; pass Gate 2; tuyên bố Phase 1 hoàn thành; mở Phase 2.

**v0.7 — semantic Package 1.1 alignment (2026-08-05), vai trò: `Package 1.1 Custody Assignment Alignment Executor`, sau Package 1.2 v0.4 Review A CLEAN + Independent Review B CLEAN (Blocker 0/Major 0/Minor 0), lịch sử:** `custody-signing-service.phase.elaborated_by` đổi `null` → `"1.2"` tại `module-registry.yaml` — Package 1.2 ([security-custody-baseline.md](../architecture/security-custody-baseline.md) v0.4 §4a) NAY LÀ elaborating artifact chính thức cho module này, sau khi elaboration đầy đủ (authority model, credential-reference model, signing-request lifecycle, caller-authorization boundary, fail-closed rules, kill-switch participation, audit/provenance) đạt review-clean — đúng chính xác điều kiện mà v0.6's correction từng ghi nhận là còn thiếu. §4 inventory table's "Elaborated by" column cho `custody-signing-service` đổi `*(unassigned — §11)*` → `` `1.2` ``. §11's "Custody & Signing Service elaborating package" deferred item ĐÓNG (RESOLVED) — xem §11 cho ghi chú đóng. **KHÔNG đổi:** `exchange-adapter.phase.elaborated_by` VẪN `null` (§11 deferred item riêng của nó KHÔNG đổi); 25-module inventory; module identity/taxonomy/responsibility/dependency/forbidden_dependencies/security_classification của MỌI module; `execution-engine.depends_on` (KHÔNG `exchange-adapter`); absence của `execution-engine → exchange-adapter` edge; PAPER path; LIVE Unauthorized; kill-switch-state ownership gap (VẪN unresolved); in-flight signing/revocation behavior gap (VẪN unresolved, security-custody-baseline.md §4a.9); DD-001/DD-003/OQ-001/OQ-002/OQ-003; coverage totals. Package 1.2 v0.4's nội dung KHÔNG bị sửa bởi transaction này (ngoài phạm vi Package 1.1) — Package 1.2 VẪN KHÔNG `Consolidated Stable`, pending Package 1.1 alignment verification (bounded consistency check này) VÀ Product Owner consolidation decision riêng cho chính Package 1.2. KHÔNG activate LIVE dưới bất kỳ hình thức nào.

**Cập nhật (2026-08-05T08:40:00+07:00, Product Owner consolidation decision, HISTORICAL — superseded bởi v0.7 trên) — Package 1.1 v0.6 khi đó `Consolidated Stable`:** Review A CLEAN + Independent Review B CLEAN trên candidate v0.6 (post `P11V05-A-MAJ-01`/`P11-v0.5-IRB-MAJ-01` bounded correction) hoàn tất — Blocker 0/Major 0/Minor 0. Product Owner đã quyết định: "I approve consolidation of Package 1.1 v0.6 as the current Consolidated Stable module-registry and system-decomposition baseline." — `package lifecycle: candidate → Consolidated Stable` (xem `module-registry.yaml` `package_lifecycle` field). Consolidated baseline chứa ĐÚNG 25 module, bao gồm `custody-signing-service` (sole direct exchange-credential-use authority, `phase.elaborated_by: null`) và `exchange-adapter` (raw venue-interaction evidence authority only, `phase.elaborated_by: null`) — cả hai `elaborated_by` VẪN `null`, KHÔNG assign package nào tại transaction này. **KHÔNG đổi:** module inventory, module identity, taxonomy classification, responsibilities, authority ownership, dependencies, forbidden dependencies, module counts, phase assignment, capability/context mapping, preserved gap nào — architecture semantics của candidate v0.6 giữ nguyên byte-for-byte về nội dung kiến trúc, CHỈ lifecycle-state field/prose thay đổi. `execution-engine.depends_on` KHÔNG đổi (`risk-gateway`, `paper-execution-boundary` — KHÔNG `exchange-adapter`); PAPER path KHÔNG đổi. `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi. Consolidation này KHÔNG tự động: assign elaborating package cho `custody-signing-service`/`exchange-adapter`; mở rộng Package 1.2 review coverage; sửa Package 1.2/Package 1.3-D; kích hoạt Execution Engine → Exchange Adapter; authorize LIVE execution; authorize implementation; resolve kill-switch-state ownership; resolve DD-003; pass Gate 2; tuyên bố Phase 1 hoàn thành; mở Phase 2.

**v0.6 — bounded correction (2026-08-05), đóng `P11V05-A-MAJ-01`/`P11-v0.5-IRB-MAJ-01`** (Package 1.1 v0.5 Review A/Independent Review B confirmed finding, lịch sử): v0.5's `custody-signing-service.phase.elaborated_by: "1.2"` tạo ra một false package-coverage/readiness claim — [`security-custody-baseline.md`](../architecture/security-custody-baseline.md) v0.2 đã được author VÀ review TRƯỚC KHI module này tồn tại (module đăng ký lần đầu tại Package 1.1 v0.5, SAU Package 1.2 v0.2's review-clean state), nên Package 1.2 CHƯA thực sự elaborate nó. Sửa: `custody-signing-service.phase.elaborated_by` đổi `"1.2"` → `null` — cùng deferred/null representation đã dùng cho `exchange-adapter`. §4 inventory table's "Elaborated by" column cho `custody-signing-service` đổi `1.2` → `*(unassigned — §11)*`. Module này VẪN được đăng ký bởi Package 1.1 dưới Approved ADR-017; elaborating package chi tiết CHƯA được authoritatively assign — Package 1.2 LÀ ứng viên mở rộng tự nhiên trong tương lai (cùng cross-cutting custody purpose đã elaborate `account-service`), NHƯNG KHÔNG assignment hay completed elaboration nào được tuyên bố tại transaction này. **Package 1.2 v0.2 VẪN review-clean CHỈ cho đúng phạm vi đã review của nó, nơi `account-service` là module Package 1.2 DUY NHẤT được fully assign.** §11 thêm một deferred item mới (custody-signing-service elaborating package, cùng dạng với exchange-adapter's). **KHÔNG đổi:** 25-module inventory, identity/authority/dependency/forbidden_dependencies/security_classification của cả hai module mới, module type nào khác, `execution-engine` dependencies, absence của `execution-engine → exchange-adapter` edge, PAPER path, LIVE Unauthorized, Decision/Risk/Execution/Fill authority, kill-switch-state ownership gap, DD-003, `implements_capabilities: []`/`serves_contexts: []`, Package 1.1 candidate lifecycle. KHÔNG cần architecture decision mới cho correction này. `status: Draft`, `package_lifecycle: candidate` KHÔNG đổi — KHÔNG tuyên bố Consolidated Stable.

**v0.5 — bounded ADR-017 authorized correction (2026-08-04), thực hiện đúng ADR-017 §9 registry-impact scope (KHÔNG mở rộng ngoài đó):** Đăng ký `custody-signing-service` (runtime_service, `owns_authoritative_state: true` cho credential-binding/signing-operational state, `security_classification: secret_consuming` — giá trị enum đã tồn tại sẵn trong field-reference comment của `module-registry.yaml`, lần đầu được gán, KHÔNG invent mới; `depends_on: [account-service]`; module DUY NHẤT được phép dùng exchange credential trực tiếp) và `exchange-adapter` (runtime_service, `owns_authoritative_state: true` CHỈ cho raw venue-interaction evidence phạm vi hẹp — ADR-017 §3.2a, KHÔNG execution observation/ExecutionResult; `security_classification: trust_boundary_candidate`; `depends_on: [custody-signing-service]`; KHÔNG raw-secret access). Module count 23 → **25**. Taxonomy tally `runtime_service` 14 → 16 (`compute_engine`/`projection` không đổi). State-authority tally `true` 13 → 15 (`false`/`deferred` không đổi). Security-classification tally `secret_consuming` 0 → 1, `trust_boundary_candidate` 4 → 5. **KHÔNG thêm** `execution-engine.depends_on → exchange-adapter` — registry KHÔNG có cơ chế biểu diễn "future/inactive dependency" nào không ngụ ý current architectural availability; cạnh đó bị GIỮ VẮNG, ghi lại như một future prerequisite tại notes của `execution-engine` (Stage 2, ADR-017 §9a) thay vì đăng ký — PAPER dependency hiện có (`execution-engine → paper-execution-boundary`) KHÔNG đổi. `exchange-adapter.phase.elaborated_by` cố tình để `null` — không package nào trong chín package Phase 1 hiện tại (tất cả PAPER-focused) elaborate chức năng đầy đủ của nó; KHÔNG invent package ID mới (đúng chỉ dẫn ADR-017). **KHÔNG đổi:** 23 module hiện có (identity/taxonomy/dependency/forbidden_dependencies/responsibility, TRỪ một note bổ sung tại `execution-engine`), coverage totals gốc (34/21/17/11/15, xem §10 cho treatment mới của hai module này), DD-001/DD-003/Structure-aware-Regime/OQ-001/OQ-002/OQ-003. KHÔNG tạo/approve ADR mới — ADR-017 đã Approved, transaction này CHỈ thực hiện registry-impact scope ĐÃ authorize (§9 ADR-017), KHÔNG tự ý mở rộng. KHÔNG kích hoạt LIVE execution path nào.

**Ghi chú tường minh bắt buộc (§12):** Package này phát hiện HAI quyết định thuộc diện **ADR REQUIRED** — Decision 1 (module dependency graph chính thức, §5/`module-registry.yaml`) và Decision 2 (`decision-engine` hybrid taxonomy). Cả hai `Approved` — Decision 1 qua [ADR-015](../adr/ADR-015.md) v0.3 (Approved, 2026-08-03), Decision 2 qua [ADR-016](../adr/ADR-016.md) v0.8 (Approved, 2026-08-04, Candidate B/split, Mechanism A) — xem §12. **Cập nhật (2026-08-04, Product Owner consolidation decision):** ADR gate condition (Decision 1 + Decision 2 Approved) THỎA, VÀ Review A CLEAN + Independent Review B CLEAN (Blocker 0/Major 0/Minor 0) trên chính candidate v0.3 này đã hoàn tất — Package 1.1 nay **`Consolidated Stable`** (package lifecycle, §15). KHÔNG ADR nào được tạo/approve/sửa tại transaction này — cả hai ADR immutable, KHÔNG đổi. Consolidation KHÔNG tự động resolve Domain gap, KHÔNG authorize implementation, KHÔNG tuyên bố Phase 1 hoàn thành, KHÔNG mở Phase 2, KHÔNG authorize Live.

**v0.3 — bounded ADR-016 alignment correction (2026-08-04)** (Product Owner-authorized correction, aligning candidate với Approved ADR-016 v0.8 — KHÔNG một finding ID review-round, một mechanical Package 1.1 correction transaction sau Decision 2 §12 resolve): Decision 2 (§12) — `decision-engine` hybrid taxonomy — nay **RESOLVED**: ADR-016 v0.8 (Approved, 2026-08-04, Product Owner) chọn **Candidate B (split)** dưới **Mechanism A** — hybrid REJECTED, KHÔNG còn module nào classified Chapter 7 hybrid trong candidate này. `decision-engine` tách thành hai module: `decision-evaluation-engine` (compute_engine, non-authoritative deterministic evaluation) + `decision-authority-service` (runtime_service, sole Decision/Trade Intent authority). Mechanism A: ADR-016 v0.8 tự nó amend hiệu lực kiểm soát của ADR-015 SCOPED cho module identity/dependency edge liên quan — ADR-015 vẫn controlling/immutable cho 21/22 module còn lại (không đổi). Đã cập nhật: module inventory (§4, 22→23 module), taxonomy tally (compute_engine 4→5), state-authority tally (true 13→13, false 8→9, tổng 22→23), dependency graph (§5, risk-gateway/replay-integration-service/review-evidence-service/command-query-api-surface nay depends_on `decision-authority-service` — KHÔNG `decision-evaluation-engine`; backtest-orchestrator depends_on CẢ HAI), §10 coverage table (mọi `decision-engine` reference thay bằng `decision-authority-service` hoặc CẢ HAI tùy dependency-edge tương ứng đã pin tại `module-registry.yaml`), §12 Decision 1 (ADR-015 Approved, RESOLVED) + Decision 2 (ADR-016 Approved, RESOLVED). Bốn residual risk từ ADR-016 v0.8 Accepted risks GIỮ NGUYÊN, KHÔNG resolve tại đây (Strategy Plugin/Evaluation boundary; evaluation-proposal Domain Contract gap; `attempt_outcome` mapping gap; operational/dependency/replay complexity). Bounded — KHÔNG reopen module boundary khác (Market/Data, Structure/Regime/Feature/Context, Strategy Engine, ExecutionResult/Fill/Position, Replay, Backtest, Paper boundary, API Surface, Review Evidence, UX Shell responsibility content ngoài dependency-edge fix), KHÔNG đổi PR/UC/UX/Domain coverage totals (34/21/17/11/15 không đổi), KHÔNG đổi DD-001/DD-003/Structure-aware-Regime deferral/OQ-001/OQ-002/OQ-003. `status: Draft`, `approved_by: null`, `approved_at: null`, `package lifecycle: candidate` không đổi — **KHÔNG tự động Consolidated Stable/Approved** dù cả Decision 1 VÀ Decision 2 nay Approved — Review A + Independent Review B trên chính candidate v0.3 này + Product Owner consolidation decision vẫn CHƯA thực hiện (§15).

**Cập nhật (2026-08-04, Product Owner consolidation decision) — Package 1.1 v0.3 nay `Consolidated Stable`:** Review A CLEAN + Independent Review B CLEAN trên candidate v0.3 (post-ADR-016-alignment correction) hoàn tất — Blocker 0/Major 0/Minor 0. Product Owner đã quyết định: "I approve consolidation of Package 1.1 v0.3 as the current stable Phase 1 System Decomposition and Module Registry baseline." — `package lifecycle: candidate → Consolidated Stable` (xem `module-registry.yaml` `package_lifecycle` field). **KHÔNG đổi:** module inventory, module identity, taxonomy classification, responsibilities, authority ownership, dependencies, forbidden dependencies, module counts, residual gap, ADR reference nào — architecture semantics của candidate v0.3 giữ nguyên byte-for-byte về nội dung kiến trúc, CHỈ lifecycle-state field/prose thay đổi. `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi — Consolidated Stable là package lifecycle/readiness state, KHÔNG có nghĩa artifact `Approved`/`Locked` (Chapter 0 §7.1). Consolidation này KHÔNG tự động: resolve bốn residual risk (Strategy Plugin/Evaluation boundary; evaluation-proposal Domain Contract gap; `attempt_outcome` mapping gap; operational/dependency/replay complexity); authorize implementation; pass Gate 2 (Gate 2 governance riêng theo `phase-1-plan.md` §6.1, không tự động pass qua Package 1.1 consolidation); tuyên bố Phase 1 hoàn thành; mở Phase 2; authorize Live.

**v0.4 — bounded parity correction (2026-08-04), đóng `P13B-IRB-MAJ-01`/`P13B-IRB-MAJ-02`/`P13B-IRB-MAJ-03`/`P13B-A-MIN-01`/`P13B-IRB-MIN-01`** (findings confirmed during Package 1.3-B Review A/Independent Review B, root cause là một registry gap tại Package 1.1 v0.3 — KHÔNG một kiến trúc option mới, KHÔNG một ADR-required decision): `feature-engine.depends_on` và `context-aggregator.depends_on` trước đây thiếu `market-data-ingestion` dù cả hai module đã trực tiếp tiêu thụ `candle-closed`/`candle-corrected` theo đúng `feature.md`/`context.md` (Package 0.2-B3/B4, Consolidated Stable, KHÔNG đổi) — sửa: thêm `market-data-ingestion` vào `depends_on` của cả hai (§5.1). `context-aggregator.emits` trước đây `[query]` dù `context.md` §3/§4 đã khóa `MarketContextSnapshot`/`MarketContextFactInvalidated` là event category — sửa: `emits: [event, query]` (§8, ngoại lệ tường minh mới thêm). Terminology clarification (§8): `event` của `context-aggregator` là append-only projection snapshot/invalidation record (record-integrity), KHÔNG phải authoritative domain fact theo nghĩa Chapter 7 §7.4 cấm — `owns_authoritative_state: false` KHÔNG đổi. **KHÔNG đổi:** module inventory (vẫn 23), module identity, `module_type`, `owns_authoritative_state`, `responsibilities`, `forbidden_dependencies`, taxonomy tally, state-authority tally, module nào khác ngoài hai module này. `status: Draft`, `approved_by: null`, `approved_at: null`, `package lifecycle: Consolidated Stable` KHÔNG đổi (correction KHÔNG reopen consolidation — bounded verification riêng, KHÔNG full Review A+B round mới). KHÔNG tạo/approve ADR — correction này áp dụng semantics đã pin sẵn tại `feature.md`/`context.md`, KHÔNG phải một quyết định kiến trúc mới. Blob trước: `ab09d031183014c1af259895dadf86aaf644cc04` (`module-registry.yaml`), `c72dfdf54d2ac86bc7ad83de742dda485da11328` (`system-decomposition.md`, chính file này).

## 1. Purpose and scope

Package 1.1 thiết lập **official Phase 1 module inventory** + `module-registry.yaml` (Chapter 7 §7.5) — nền tảng technical-realization mà Package 1.2–1.6 elaborate chi tiết. Phạm vi: module identity, taxonomy classification, responsibility boundary, dependency-direction graph, ownership/authority map, contract category (event/command/query), Product/UC/UX/Domain coverage-completeness evidence.

**KHÔNG thuộc phạm vi** (elaborated bởi package khác hoặc decision riêng): concrete module interface, API field-level schema, database schema/DDL, deployment infrastructure/cloud provider, programming language/framework, authentication/authorization/custody implementation, Engine algorithm, source code, Phase 1 DoD, Package 1.2–1.6 detailed architecture.

## 2. Governing authority

```text
Constitution (Chapter 0–14, Locked):         highest architectural authority
Approved/Locked ADR (ADR-001–014):           decision authority
Domain Contract (/docs/domain/):              domain semantic authority
context-map.yaml (Chapter 4 §4.2):            capability/context identity + relationship authority
product-requirement.md (Package 0.3-A):       product requirement authority
use-case-workflow.md (Package 0.3-B):         behavior/workflow authority
ux-blueprint.md (Package 0.3-C):              user-facing acceptance-surface authority
phase-1-plan.md (Consolidated Stable v0.2):   Phase 1 work-breakdown/dependency-order authority
Package 1.1 (tài liệu này):                    technical module-realization authority ONLY
```

Package 1.1 KHÔNG redefine domain entities, domain invariants, product behavior, use-case outcomes, UX acceptance requirements, hay existing ADR decisions — mọi module chỉ **MAP** vào semantics đã tồn tại, KHÔNG **REINTERPRET**.

## 3. Module-design principles

```text
1. Module identity = deployable/independently-operated runtime component (Chapter 7 §7.0)
   — KHÔNG shared library, schema artifact, infrastructure resource, documentation.
2. Một module = một primary taxonomy type (compute_engine | projection | runtime_service,
   Chapter 7 §7.1) — exhaustive, KHÔNG type thứ tư.
3. Hybrid (≥2 core taxonomy type) CHỈ hợp lệ khi thỏa cả 4 điều kiện Chapter 7 §7.1, điều
   kiện 4 là ADR — KHÔNG tự động approve hybrid tại đây (xem §12).
4. Module boundary ≠ Domain Context boundary (Chapter 4 §4.4: 1 Context có thể có 0..n
   module; Chapter 7 §7.5) — KHÔNG one-module-per-domain-entity, KHÔNG one-module-per-PR,
   KHÔNG one-module-per-UC, KHÔNG one-module-per-screen.
5. Mọi module phải bounded: nêu rõ sở hữu gì / tính toán gì / publish gì / tiêu thụ gì /
   KHÔNG được sở hữu gì / dependency direction nào — cấm generic module (CoreService,
   CommonService, PlatformManager, SharedEngine, UtilityModule) trừ khi bounded/justified.
6. implements_capabilities/serves_contexts PHẢI trỏ về ID đã tồn tại sẵn trong
   context-map.yaml (Chapter 4 §4.2) — module-registry KHÔNG tự định nghĩa capability/
   context mới.
7. Dependency direction bảo toàn engine pipeline đã established (§5) VÀ authority
   boundary product/domain layer đã pin (§7).
```

## 4. Official module inventory

**25 module** (v0.5 — 23→25, `custody-signing-service` + `exchange-adapter` đăng ký theo ADR-017 v0.2 Approved, Option C split) — xem `module-registry.yaml` cho định nghĩa đầy đủ từng field. Tóm tắt:

| module_id | Taxonomy | Owns authoritative state | Elaborated by |
|---|---|---|---|
| `market-reference-service` | runtime_service | Yes | 1.3-A |
| `market-data-ingestion` | runtime_service | Yes | 1.3-A |
| `structure-engine` | compute_engine | Yes | 1.3-A |
| `raw-regime-engine` | compute_engine | Yes | 1.3-A |
| `feature-engine` | compute_engine | Yes | 1.3-B |
| `context-aggregator` | projection | No | 1.3-B |
| `account-service` | runtime_service | Yes | 1.2 |
| `custody-signing-service` | runtime_service (ADR-017 v0.2 Approved, §12 Decision 8) | Yes (credential-binding/signing-operational state only) | `1.2` (v0.7, §11) |
| `exchange-adapter` | runtime_service (ADR-017 v0.2 Approved, §12 Decision 8) | Yes (raw venue-interaction evidence only) | *(unassigned — §11)* |
| `strategy-engine` | runtime_service | Yes | 1.3-C |
| `plugin-release-manager` | runtime_service | Yes (operational fact only, §12 Decision 5b) | 1.3-C |
| `strategy-plugin-host` | compute_engine | No | 1.3-C |
| `decision-evaluation-engine` | compute_engine (ADR-016 v0.8 Approved, §12 Decision 2) | No | 1.3-C |
| `decision-authority-service` | runtime_service (ADR-016 v0.8 Approved, §12 Decision 2 — no hybrid) | Yes | 1.3-C |
| `risk-gateway` | runtime_service (no hybrid — §12 Decision 2b) | Yes | 1.3-D |
| `execution-engine` | runtime_service | Yes | 1.3-D |
| `execution-result-processor` | runtime_service | Yes | 1.3-D |
| `fill-processor` | runtime_service | Yes | 1.3-D |
| `position-projection` | projection | No | 1.3-D |
| `replay-integration-service` | projection | No | 1.3-A |
| `backtest-orchestrator` | runtime_service | Deferred (DD-001) | 1.3-A |
| `paper-execution-boundary` | runtime_service | No | 1.3-D |
| `command-query-api-surface` | runtime_service | No | 1.4 |
| `review-evidence-service` | projection | No | 1.5 |
| `ux-application-shell` | runtime_service | No | 1.6 |

**Taxonomy tally (v0.5 — script-verified against `module-registry.yaml`, exhaustive/mutually-exclusive, sums to 25; updated for ADR-017 v0.2 split registration):**

```text
compute_engine   5   structure-engine, raw-regime-engine, feature-engine, strategy-plugin-host,
                      decision-evaluation-engine
projection       4   context-aggregator, position-projection, replay-integration-service,
                      review-evidence-service
runtime_service  16  market-reference-service, market-data-ingestion, account-service,
                      custody-signing-service, exchange-adapter, strategy-engine,
                      plugin-release-manager, decision-authority-service,
                      risk-gateway, execution-engine, execution-result-processor,
                      fill-processor, backtest-orchestrator, paper-execution-boundary,
                      command-query-api-surface, ux-application-shell
total            25
```

**State-authority tally (v0.5 — separate dimension — DO NOT overlap with taxonomy tally above; script-verified, exhaustive/mutually-exclusive, sums to 25; updated for ADR-017 v0.2 split registration):**

```text
owns_authoritative_state: true      15  market-reference-service, market-data-ingestion,
                                         structure-engine, raw-regime-engine, feature-engine,
                                         account-service, custody-signing-service,
                                         exchange-adapter, strategy-engine,
                                         plugin-release-manager, decision-authority-service,
                                         risk-gateway, execution-engine,
                                         execution-result-processor, fill-processor
owns_authoritative_state: false     9   context-aggregator, strategy-plugin-host,
                                         decision-evaluation-engine, position-projection,
                                         replay-integration-service, paper-execution-boundary,
                                         command-query-api-surface, review-evidence-service,
                                         ux-application-shell
owns_authoritative_state: deferred  1   backtest-orchestrator
total                                25
```

**Bounded scope note (v0.5):** `custody-signing-service`'s `true` là CHỈ cho credential-binding/signing-operational state (KHÔNG raw secret material — ngoài Domain Contract scope). `exchange-adapter`'s `true` là CHỈ cho raw venue-interaction evidence trực tiếp chứng kiến (KHÔNG platform ExecutionObservation/ExecutionResult — `execution-result-processor` VẪN authority đó, KHÔNG đổi). Cả hai KHÔNG mở rộng ý nghĩa `true` ngoài phạm vi hẹp đã định nghĩa tại ADR-017 §3.1/§3.2a.

Ghi chú bắt buộc (đóng `P11-A-MIN-01`, giữ nguyên nguyên tắc, cập nhật số liệu v0.5): "false" KHÔNG đồng nghĩa "Projection" — 5/9 module `false` là `runtime_service`/`compute_engine` (`strategy-plugin-host`, `decision-evaluation-engine`, `paper-execution-boundary`, `command-query-api-surface`, `ux-application-shell`), KHÔNG chỉ bốn `projection` type. Hai chiều (taxonomy, state-authority) tách biệt hoàn toàn, KHÔNG dùng chung một bảng/tally.

## 5. Dependency graph

### 5.1 Text form (normative — diagram ở §5.2 chỉ minh họa)

```text
market-reference-service (root)
market-data-ingestion            → depends_on: market-reference-service
structure-engine                 → depends_on: market-data-ingestion
raw-regime-engine                → depends_on: market-data-ingestion
                                    (forbidden_dependencies: structure-engine — ADR-003/014)
feature-engine                   → depends_on: market-data-ingestion, structure-engine,
                                    raw-regime-engine
                                    [P13B-IRB-MAJ-01 correction, 2026-08-04 — feature-engine
                                    directly consumes candle-closed/candle-corrected
                                    (feature.md §7.1/§7.3 reference-price/candle path);
                                    this permits the definition-pinned Candle input path
                                    already established by feature.md, it does NOT create
                                    universal fan-in]
context-aggregator               → depends_on: market-data-ingestion, structure-engine,
                                    raw-regime-engine, feature-engine
                                    [P13B-IRB-MAJ-02 correction, 2026-08-04 — context-
                                    aggregator directly consumes candle-closed/candle-
                                    corrected as the authoritative cutoff/trigger Candle
                                    already required by context.md §7.0/§11; this does NOT
                                    route Candle through Feature Engine]

account-service (root)

custody-signing-service          → depends_on: account-service
                                    (forbidden_dependencies: decision-authority-service,
                                    risk-gateway, execution-engine, exchange-adapter,
                                    strategy-engine, strategy-plugin-host,
                                    decision-evaluation-engine, context-aggregator,
                                    position-projection, command-query-api-surface)
                                    [ADR-017 v0.2 Approved, 2026-08-04T20:08:00+07:00 —
                                    Option C split, sole direct exchange-credential-use
                                    authority]
exchange-adapter                 → depends_on: custody-signing-service
                                    (forbidden_dependencies: decision-authority-service,
                                    risk-gateway, strategy-engine, strategy-plugin-host,
                                    decision-evaluation-engine, context-aggregator,
                                    position-projection, account-service,
                                    command-query-api-surface)
                                    [ADR-017 v0.2 Approved — venue protocol translation/
                                    external transport, no raw-secret access, authoritative
                                    ONLY for raw venue-interaction evidence directly
                                    witnessed (§3.2a) — NOT execution-observation/
                                    ExecutionResult. Stage 1 registration only — NO active
                                    execution-engine → exchange-adapter edge added (see
                                    execution-engine note below); LIVE path activation is a
                                    Stage 2 concern, separate future authorization]

strategy-engine                  → depends_on: account-service
plugin-release-manager (root)
strategy-plugin-host             → depends_on: strategy-engine, context-aggregator,
                                    plugin-release-manager
                                    (forbidden_dependencies: execution-engine, risk-gateway,
                                    paper-execution-boundary)

decision-evaluation-engine        → depends_on: strategy-engine, strategy-plugin-host,
                                    context-aggregator
                                    (forbidden_dependencies: execution-engine, risk-gateway,
                                    paper-execution-boundary)
                                    [ADR-016 v0.8 Approved — non-authoritative deterministic
                                    evaluation, replaces `decision-engine` hybrid]
decision-authority-service        → depends_on: decision-evaluation-engine, strategy-engine
                                    (forbidden_dependencies: execution-engine,
                                    paper-execution-boundary)
                                    [ADR-016 v0.8 Approved — sole Decision/Trade Intent
                                    authority, replaces `decision-engine` hybrid]
risk-gateway                     → depends_on: decision-authority-service, account-service
execution-engine                 → depends_on: risk-gateway, paper-execution-boundary
                                    (forbidden_dependencies: strategy-engine,
                                    strategy-plugin-host, context-aggregator)
                                    [ADR-017 v0.2 Approved — depends_on intentionally does
                                    NOT include exchange-adapter; a future LIVE
                                    venue-submission dependency is authorized in principle
                                    but registering it as an active edge is a Stage 2
                                    concern requiring separate future LIVE architecture/
                                    governance authorization (ADR-017 §9a) — current PAPER
                                    dependency (paper-execution-boundary) unchanged]
execution-result-processor       → depends_on: execution-engine, paper-execution-boundary
fill-processor                   → depends_on: execution-result-processor
position-projection              → depends_on: fill-processor

replay-integration-service       → depends_on: decision-authority-service, risk-gateway,
                                    execution-engine, execution-result-processor,
                                    fill-processor, position-projection

backtest-orchestrator            → depends_on: strategy-engine, decision-evaluation-engine,
                                    decision-authority-service, risk-gateway
                                    (forbidden_dependencies: execution-engine,
                                    paper-execution-boundary, execution-result-processor,
                                    fill-processor, position-projection)
paper-execution-boundary (root — referenced BY execution-engine/execution-result-processor)

command-query-api-surface        → depends_on: [all 17 authoritative/projection modules —
                                    decision-authority-service, NOT decision-evaluation-engine
                                    (same exclusion pattern as strategy-plugin-host);
                                    backtest-orchestrator ADDED (v0.8, ADR-019 v0.2
                                    Approved, NAV-003 Gap A query-exposure route)]
review-evidence-service          → depends_on: decision-authority-service, risk-gateway,
                                    execution-engine, execution-result-processor,
                                    fill-processor, position-projection,
                                    replay-integration-service
ux-application-shell             → depends_on: command-query-api-surface
                                    (forbidden_dependencies: all 14 engine/projection
                                    modules directly — must go through API surface)
```

Validated (script-checked before commit, §13): 25 unique `module_id`; every `depends_on`/`forbidden_dependencies` reference resolves to an existing `module_id`; zero cycles in the `depends_on` graph; zero module has the same ID in both `depends_on` and `forbidden_dependencies`.

### 5.2 Diagram (illustrative only — §5.1 is normative)

```text
Market Data
   ├──────────────┐
   ▼              ▼
Structure Engine   Raw Regime Engine        (độc lập)
   │                    │
   └────────┬───────────┘
            ▼
     Feature Engine (fan-in có chọn lọc)
            ▼
    Context Aggregator (Projection, KHÔNG business decision)
            ▼
 Strategy Engine ──► Strategy Plugin Host ──► Decision Evaluation Engine ──► Decision
                                               (non-authoritative,             Authority Service
                                                compute_engine)                (sole authority,
                                                                                runtime_service)
                                                                                     │
                                                                                     ▼
                                                                               Risk Gateway
                                                                                     │
                                                                                     ▼
                                            Execution Engine ◄── Paper Execution Boundary
                                                    │
                                                    ▼
                                      Execution Result Processor
                                                    │
                                                    ▼
                                              Fill Processor
                                                    │
                                                    ▼
                                           Position Projection

(Account Service, Plugin Release Manager: independent roots referenced by Strategy/Risk.)
(ADR-017 v0.2 Approved, 2026-08-04T20:08:00+07:00 — Option C split: Account Service
 → Custody & Signing Service → Exchange Adapter is a registered architecture boundary
 chain, Stage 1 only (ADR-017 §9a) — NOT depicted as connected to the Execution Engine
 chain above, because NO active Execution Engine → Exchange Adapter edge exists in §5.1;
 activating that edge is a Stage 2 concern requiring separate future LIVE architecture/
 governance authorization. Custody & Signing Service is the sole module permitted direct
 exchange-credential use; Exchange Adapter is authoritative ONLY for raw
 venue-interaction evidence it directly witnesses, NOT for execution-observation/
 ExecutionResult, which remains Execution Result Processor's authority, unchanged.)
(Replay Integration Service, Review Evidence Service: cross-cutting read layers over the chain
 — consume Decision Authority Service authoritative fact only, NOT Decision Evaluation
 Engine's non-authoritative proposal.)
(Backtest Orchestrator: parallel non-PAPER path — depends on BOTH Decision Evaluation Engine
 and Decision Authority Service — explicitly forbidden from touching
 Execution/Paper/ExecutionResult/Fill/Position modules.)
(Command/Query/API Surface: fan-in from every authoritative/projection module — Decision
 Authority Service only, same exclusion pattern as Strategy Plugin Host for
 Decision Evaluation Engine.)
(UX Application Shell: depends ONLY on API Surface, never engines directly.)
(ADR-016 v0.8 Approved, 2026-08-04 — Candidate B/split, Mechanism A: `decision-engine` hybrid
 replaced by the two modules shown above. This is a responsibility/dependency view, NOT
 authorization to implement a synchronous pipeline or specific runtime topology.)
(Feature Engine, Context Aggregator: both also depend directly on Market Data Ingestion for
 the Candle cutoff/reference-price/trigger input — simplified out of the diagram above for
 readability; §5.1 text form is normative and includes this edge, per P13B-IRB-MAJ-01/
 P13B-IRB-MAJ-02 correction, 2026-08-04.)
```

## 6. Responsibility and ownership boundaries

Mỗi module trong `module-registry.yaml` khai báo tường minh `responsibilities` (sở hữu/tính toán gì), `emits`/`consumes` (publish/tiêu thụ loại contract gì), `forbidden_dependencies` (KHÔNG được phụ thuộc gì), và `owns_authoritative_state` (có phải nguồn thật duy nhất hay không, I-12). Không module nào generic — mỗi entry map trực tiếp về đúng một `capability_id`/`domain_context_id` đã đăng ký (§4.2), TRỪ NĂM module cross-cutting: ba module routing/read/presentation layer thuần túy (`command-query-api-surface`, `review-evidence-service`, `ux-application-shell` — không domain authority), VÀ hai module mới (v0.5) `custody-signing-service`/`exchange-adapter` — KHÔNG có `capability_id`/`domain_context_id` đăng ký tại `context-map.yaml` cho custody/signing/venue-adapter responsibility (đúng nguyên tắc đã dùng cho `raw-regime-engine`'s "Structure-aware Regime" deferral, §11 — Domain Context/Capability identity là thẩm quyền Chapter 4 §4.2, KHÔNG phải module-registry's để tự invent).

**God-module check:** không module nào có tên generic không bounded (không `CoreService`/`CommonService`/`PlatformManager`/`SharedEngine`/`UtilityModule`); mỗi module có đúng MỘT primary responsibility statement cụ thể.

## 7. Authority/source-of-truth map

Dùng ĐÚNG state-authority tally đã pin tại §4 (P11-A-MIN-01 correction) — KHÔNG lặp lại con số riêng ở đây (tránh hai nguồn lệch nhau, I-12):

```text
owns_authoritative_state: true      15  (xem §4 cho danh sách đầy đủ)
owns_authoritative_state: false     9   (xem §4 — KHÔNG chỉ bốn Projection; gồm cả
                                         strategy-plugin-host/decision-evaluation-engine/
                                         paper-execution-boundary/command-query-api-surface/
                                         ux-application-shell)
owns_authoritative_state: deferred  1   backtest-orchestrator (DD-001)
```

I-12 conformance: mỗi domain concept resolve đúng MỘT authoritative module — không hai module nào cùng claim `owns_authoritative_state: true` cho cùng một `serves_contexts` entry (script-checked, §13). `custody-signing-service`/`exchange-adapter` (v0.5, ADR-017 v0.2) mỗi module `true` CHỈ trong phạm vi hẹp riêng (credential-binding/signing-operational state; raw venue-interaction evidence trực tiếp chứng kiến — §4 "Bounded scope note") — KHÔNG overlap lẫn nhau, KHÔNG overlap với bất kỳ authority nào khác (đặc biệt `execution-result-processor`'s ExecutionResult authority, KHÔNG đổi). Bốn module taxonomy `projection` (`context-aggregator`, `position-projection`, `replay-integration-service`, `review-evidence-service`) KHÔNG BAO GIỜ trở thành authoritative source thay module gốc (Chapter 7 §7.4 — preserved) — đây là tập con của nhóm `owns_authoritative_state: false` (9 module), KHÔNG đồng nhất với toàn bộ nhóm đó.

## 8. Event/command/query interaction categories

`module-registry.yaml` field `consumes`/`emits` khai báo CATEGORY (`event` | `query` | `command`), KHÔNG field-level schema (đó là Package 1.4). Event log là authoritative source cho runtime fact/decision history (Chapter 8 §8.1) — transport/broker cụ thể KHÔNG authoritative (không quyết định tại Package 1.1). Mọi module authoritative emit `event`; Projection emit `query` (read contract); orchestration/boundary module (`account-service`, `strategy-engine`, `plugin-release-manager`) consume `command`.

**v0.5 (ADR-017 v0.2 Approved):** `custody-signing-service` consumes `[command, query]` (bounded signing request; credential-binding/eligibility check) và emits `[event, query]` (signing outcome — category chỉ, KHÔNG field-level schema, forbidden per ADR-017 §3.3). `exchange-adapter` consumes `[command]` (execution/submission request — MỘT contract boundary riêng biệt khỏi Execution Engine's PAPER contract với `paper-execution-boundary`, ADR-017 §8.1, KHÔNG field-level authored tại Package 1.1 hay ADR-017) và emits `[event]` (raw venue-interaction evidence — category chỉ, ADR-017 §3.2a).

**Ngoại lệ tường minh (`context-aggregator`, `emits: [event, query]`, P13B-IRB-MAJ-03 correction, 2026-08-04):** `context-aggregator` là Projection duy nhất phát `event` — `MarketContextSnapshot`/`MarketContextFactInvalidated` (context.md §3/§4). `event` ở đây là **append-only projection snapshot/invalidation record** (immutable, cursor-bounded, lineage-preserving) — KHÔNG phải authoritative domain fact theo nghĩa Chapter 7 §7.4 cấm ("phát sinh authoritative domain fact"). Ranh giới: `owns_authoritative_state: false` KHÔNG đổi — Context KHÔNG trở thành authoritative source cho Structure/Regime/Feature hay bất kỳ domain concept nào khác; nó chỉ ghi nhận CHÍNH bản ghi snapshot của nó (record integrity), không tuyên bố sở hữu domain state nó tổng hợp. Xem `docs/architecture/engine/feature-context-architecture.md` cho elaboration đầy đủ.

**Ngoại lệ tường minh (`backtest-orchestrator`, `consumes: [event, query]`, ADR-019 v0.2 Approved alignment, 2026-08-06):** `backtest-orchestrator` LÀ `runtime_service` DUY NHẤT khác (cùng `decision-authority-service`) nay directly query-answerable — `consumes` mở rộng `[event]` → `[event, query]` để nhận query request từ `command-query-api-surface` (edge mới, cùng transaction), trả lời bằng một non-authoritative correlation view compose từ Decision fact (`decision-authority-service`) VÀ RiskEvaluation fact (`risk-gateway`) ĐÃ tồn tại, bằng run identity (ADR-018, Approved). Precedent trực tiếp: `decision-authority-service` (CÙNG `module_type`, CÙNG `consumes: [event, query]`/`emits: [event]` shape, CÙNG kết hợp authoritative-adjacent role + query-answerable, KHÔNG `hybrid`) — mạnh hơn so sánh chéo với module `projection` (vốn dùng `emits: [query]` thay vì `consumes: [event, query]`, một pattern KHÁC `module_type`). Ranh giới: `owns_authoritative_state: deferred` KHÔNG đổi — `backtest-orchestrator` KHÔNG trở thành authoritative source cho Decision hay RiskEvaluation; nó CHỈ correlate/fold fact ĐÃ ghi nhận, KHÔNG rewrite/re-author/replace/derive nội dung authoritative của chúng, KHÔNG author một fact/entity/event mới nào. `emits` (`[event]`), `module_type` (`runtime_service`), `hybrid` (`null`) KHÔNG đổi. Xem [ADR-019](../adr/ADR-019.md) v0.2 §2 cho quyết định đầy đủ.

## 9. Plugin boundaries

`plugin_relation` field: `none` (mặc định), `hosts` (`strategy-plugin-host`), `manages_release` (`plugin-release-manager`).

**Authority boundary tường minh (P11-A-MAJ-02 correction, đóng finding):** `module-registry.yaml` — CHÍNH tài liệu YAML này — là **authority DUY NHẤT** cho Plugin Definition identity, module existence, primary taxonomy, và architecture responsibility của MỌI module, kể cả module liên quan plugin (Chapter 7 §7.5, Chapter 9 §9.1). KHÔNG runtime module nào — kể cả `plugin-release-manager` — được sở hữu hay mutate các architecture fact đó. `plugin-release-manager` (đổi tên từ "Plugin Registry Service", đóng `P11-A-MAJ-02`) CHỈ sở hữu OPERATIONAL fact: Plugin Version → exact Package/Build Artifact content identity resolution, immutable release-manifest resolution (Chapter 9 §9.1, mô hình A/B), runtime compatibility/availability status của Plugin Runtime replica, và activation/deactivation coordination (Chapter 9 §9.5, validated compatibility set) — KHÔNG Plugin Definition identity/taxonomy, KHÔNG một registry thứ hai. `strategy-plugin-host` (Plugin Definition, taxonomy `compute_engine`) tự nó vẫn đăng ký DUY NHẤT tại `module-registry.yaml`, không đổi.

Strategy Plugin (`strategy-plugin-host`) KHÔNG được bypass Decision/Risk Gateway — `forbidden_dependencies: [execution-engine, risk-gateway, paper-execution-boundary, decision-authority-service]` enforce tại module-boundary level, đúng I-4/I-7 (v0.3 — thêm `decision-authority-service` sau ADR-016 v0.8 split: Plugin phải KHÔNG BAO GIỜ trực tiếp reach authority append, chỉ feed advisory input qua `decision-evaluation-engine`, vốn tự nó cũng KHÔNG được bypass Decision Authority Service/Risk Gateway/Execution — `decision-evaluation-engine.forbidden_dependencies: [execution-engine, risk-gateway, paper-execution-boundary]`, cùng nguyên tắc non-bypass). Decision-time visibility (Chapter 9 §9.5) là ràng buộc của chính `strategy-plugin-host`'s runtime behavior, elaborated đầy đủ tại Package 1.3-C — Package 1.1 chỉ pin boundary, KHÔNG thiết kế cơ chế cursor-bounded cụ thể.

## 10. Product/UC/UX coverage evidence

**Coverage method:** mỗi `UC-XXX` map về module chịu trách nhiệm chính, dựa trên "Domain vocabulary used" field của chính `UC-XXX` đó (`use-case-workflow.md` §6) đối chiếu `owns_authoritative_state`/`serves_contexts` của module. Mọi `PR-XXX`/screen kế thừa coverage từ `UC-XXX` nó trace tới (catalogue `use-case-workflow.md` §5, `ux-blueprint.md` §6) — many-to-many, KHÔNG one-module-per-PR/UC/screen.

| UC | Primary module | Supporting module(s) | PR(s) | Screen(s) |
|---|---|---|---|---|
| UC-001 | `context-aggregator` | `market-data-ingestion`, `structure-engine`, `raw-regime-engine`, `feature-engine` | PR-003, PR-015, PR-017 | SCR-001, VIEW-001 |
| UC-002 | `strategy-engine` | — | PR-001, PR-016 | VIEW-001 |
| UC-003 | `decision-authority-service` | — | PR-017 | VIEW-002 |
| UC-004 | `replay-integration-service` | `decision-authority-service`, `risk-gateway`, `execution-engine`, `execution-result-processor`, `fill-processor`, `position-projection` | PR-008, PR-018, PR-020 | SCR-002 |
| UC-005 | `decision-authority-service` | `replay-integration-service` | PR-010, PR-019 | VIEW-003 |
| UC-006 | `backtest-orchestrator` | `strategy-engine`, `decision-evaluation-engine`, `decision-authority-service`, `risk-gateway` | PR-021, PR-022, PR-023 | SCR-003 |
| UC-007 | `backtest-orchestrator` | `decision-evaluation-engine`, `decision-authority-service`, `risk-gateway` | PR-021, PR-009, PR-004, PR-005 | SCR-004 |
| UC-008 | `backtest-orchestrator` | — | PR-033 | SCR-004 |
| UC-009 | `backtest-orchestrator` | `strategy-engine` | PR-034 | SCR-004 |
| UC-010 | `backtest-orchestrator` | `strategy-engine` | PR-034 | SCR-005 |
| UC-011 | `decision-authority-service` | `risk-gateway`, `execution-engine`, `paper-execution-boundary`, `account-service` | PR-007, PR-024, PR-004, PR-005 | SCR-006 |
| UC-012 | `execution-result-processor` | `execution-engine` | PR-007, PR-024 | SCR-007 |
| UC-013 | `fill-processor` | `execution-result-processor` | PR-025 | SCR-007 |
| UC-014 | `position-projection` | `fill-processor` | PR-026 | SCR-007 |
| UC-015 | `execution-engine` | `paper-execution-boundary` | PR-027 | SCR-007 |
| UC-016 | `review-evidence-service` | `decision-authority-service`…`position-projection` (full chain) | PR-028, PR-004, PR-005 | SCR-008 |
| UC-017 | `replay-integration-service` | `review-evidence-service` | PR-029 | SCR-009 |
| UC-018 | `review-evidence-service` | — | PR-011, PR-030 | VIEW-004 |
| UC-019 | `strategy-engine` | — | PR-031 | SCR-010, VIEW-006 |
| UC-020 | `strategy-engine` | `review-evidence-service` | PR-031, PR-032 | SCR-011 |
| UC-021 | `strategy-engine` | `review-evidence-service` | PR-032 | VIEW-005 |

**Totals:**

```text
34/34 Product Requirement  — covered (transitively via 21/21 UC, no orphan)
21/21 Use Case             — covered, zero orphan
17/17 UX screen/view       — covered, zero orphan (11 SCR + 6 VIEW; WS-001 → account-service
                              per phase-1-plan.md §5.3; NAV-001–006 → same modules as their
                              destination SCR)
11/11 Domain capability     — covered (script-checked, §13)
15/15 Domain context        — covered (script-checked, §13)
```

**Danh sách 34 PR (đối chiếu):** PR-001–PR-034 — mỗi PR trace được về đúng UC(s) tại `use-case-workflow.md` §5, và mỗi UC đó đã map về module ở bảng trên; KHÔNG PR nào orphan (đã verify tại Package 0.3-B consolidation, `PR traceability` field mọi UC — Package 1.1 chỉ kế thừa, không tự re-audit).

**Bổ sung — 5 PR cross-cutting/alternate-flow (KHÔNG xuất hiện ở cột "Primary PR(s)" của bảng UC catalogue §5, nhưng có traceability tường minh khác trong `use-case-workflow.md`):**

| PR | Nguồn traceability | Module |
|---|---|---|
| PR-002 | `WF-INV-1` (§4, mọi session scoped theo đúng một Account) — cross-cutting | `account-service` |
| PR-006 | UC-011 alternate flow (§8, RiskEvaluation REJECTED/NON_EVALUABLE reason disclosure) | `risk-gateway` |
| PR-012 | `WF-INV-7` (§4, historical cursor deterministic, không phụ thuộc network) — cross-cutting | `replay-integration-service` |
| PR-013 | `WF-INV-8` (§4, giá trị tài chính hiển thị lossless) — cross-cutting | `fill-processor`, `position-projection`, `execution-result-processor` |
| PR-014 | `WF-INV-9` (§4, lifecycle state hiển thị phản ánh transition đã khai báo) — cross-cutting | `decision-authority-service`, `risk-gateway`, `execution-engine`, `execution-result-processor`, `fill-processor` (mọi module sở hữu state machine — `decision-evaluation-engine` KHÔNG có Decision lifecycle state, chỉ compute non-authoritative proposal) |

Với năm PR trên, coverage đến từ **Workflow Invariant** (`WF-INV-XXX`, cross-cutting toàn bộ workflow, KHÔNG gắn riêng một UC) hoặc từ **alternate-flow** của một UC cụ thể (không xuất hiện ở "Primary PR(s)" nhưng vẫn material) — cả hai đều là traceability hợp lệ theo `use-case-workflow.md` §"Quy tắc traceability nguồn". Coverage totals §10 (34/34) đã tính đủ năm PR này.

**Deferred coverage — `custody-signing-service`/`exchange-adapter` (v0.5, ADR-017 v0.2 Approved):** ZERO coverage hiện tại — KHÔNG `PR-XXX`/`UC-XXX`/`SCR-`/`VIEW-` nào trong Product/UC/UX catalogue hiện tại (Package 0.3-A/B/C, PAPER-focused) map tới custody/signing hay venue-adapter LIVE interaction, vì catalogue đó KHÔNG bao phủ LIVE execution scope. Cùng treatment đã dùng cho `backtest-orchestrator` (DD-001, deferred) — module identity/boundary được đăng ký TRƯỚC KHI coverage evidence tồn tại, KHÔNG PHẢI một orphan cần "lấp đầy" giả tạo. Coverage totals (34/34/21/21/17/17/11/11/15/15) dưới đây KHÔNG đổi — hai module mới KHÔNG được tính vào bất kỳ mẫu số nào (Product/UC/UX catalogue hiện tại KHÔNG mở rộng phạm vi LIVE tại transaction này).

## 11. Deferred decisions and escalation points

```text
DD-001  Backtest Domain Contract/entity/event/schema — Deferred. Blocked module:
        backtest-orchestrator (owns_authoritative_state: deferred). Escalation: Product
        Owner + Domain Contract authoring decision (out of Package 1.1 scope). KHÔNG
        invent Backtest entity (BacktestOrder/BacktestFill/BacktestPosition/
        BacktestExecutionResult hay tương đương).

DD-003  PAPER-context authoritative Decision establishment mechanism — Deferred. Blocked
        module: paper-execution-boundary (mechanism unresolved). Mandatory TRƯỚC KHI
        UC-011 runtime design (Package 1.3-C/1.3-D). Escalation: Product Owner/Domain
        Contract correction tương lai. KHÔNG tự phát minh mechanism ở Package 1.1.

Structure-aware Regime — KHÔNG có capability_id/domain_context_id đăng ký tại
        context-map.yaml (Chapter 4 §4.2). Blocked: cần Domain Context/Capability
        registration TRƯỚC KHI một module riêng có thể bind vào trách nhiệm này.
        raw-regime-engine module hiện tại CHỈ cover raw-regime-analysis context đã
        đăng ký — Structure-aware Regime KHÔNG có module riêng tại candidate này.

OQ-001  Data Retention Policy & Access Control — Partially Resolved, KHÔNG đổi tại đây.
OQ-002  Strategy Lifecycle Gate — Open, KHÔNG đổi tại đây.
OQ-003  Product Metrics — Open, KHÔNG đổi tại đây.

Exchange Adapter elaborating package (v0.5, ADR-017 v0.2 Approved) — `phase.
        elaborated_by: null` tại `module-registry.yaml`. Exchange Adapter's đầy đủ
        functional architecture là một LIVE-prerequisite, NGOÀI phạm vi cả chín package
        Phase 1 hiện tại (`phase-1-plan.md` v0.4, tất cả PAPER-focused). Escalation: một
        Phase 1 amendment (package mới) HOẶC quyết định tương đương, Product Owner, ngoài
        phạm vi Package 1.1 correction transaction này — KHÔNG invent package ID.

Custody & Signing Service elaborating package — RESOLVED (v0.7, semantic Package 1.1
        alignment transaction, 2026-08-05): `phase.elaborated_by` đổi `null` → `"1.2"` tại
        `module-registry.yaml`, sau khi [security-custody-baseline.md](../architecture/security-custody-baseline.md)
        v0.4 §4a elaborate đầy đủ module này VÀ đạt Review A CLEAN + Independent Review B
        CLEAN (Blocker 0/Major 0/Minor 0) — đúng điều kiện mà v0.6's bounded correction
        (lịch sử: sửa false claim `"1.2"` tại v0.5, đổi về `null` chờ elaboration thật)
        đã ghi nhận là còn thiếu. Item này KHÔNG còn deferred. Package 1.2 v0.4 VẪN KHÔNG
        `Consolidated Stable` — pending Package 1.1 alignment verification VÀ Product
        Owner consolidation decision riêng, KHÔNG resolve tại đây.

Execution Engine → Exchange Adapter LIVE path activation (v0.5, ADR-017 v0.2 §9a) —
        module registration (Stage 1) KHÔNG tự kích hoạt dependency edge/execution path
        thật (Stage 2). Escalation: future LIVE architecture candidate + governance
        authorization riêng biệt, Product Owner, ngoài phạm vi Package 1.1 correction này.

Custody/signing implementation (Vault/KMS/HSM binding, signing algorithm, credential
        rotation protocol, RBAC/caller-authorization mechanism cho custody-signing-service)
        — kế thừa nguyên vẹn từ ADR-017 §14/Package 1.2 §14, forbidden scope tại Package
        1.1 (KHÔNG author implementation).
```

## 12. ADR Scope Rule evaluation

Áp dụng ADR Scope Rule thực tế ([Governance §4b](../constitution/00-governance.md)) cho từng quyết định CỤ THỂ candidate này đề xuất — KHÔNG lặp lại phân loại chung của `phase-1-plan.md` §7:

```text
Decision 1 — Official Phase 1 module dependency graph (§5, module-registry.yaml, lần đầu
             thiết lập chính thức):
  Classification:  ADR REQUIRED.
  Rule applied:    Governance §4b — "Module Taxonomy/dependency graph" thay đổi → Required.
                   Đây là lần ĐẦU TIÊN dependency graph chính thức được đề xuất (trước đây
                   chỉ có bản nháp Chapter 7/architecture README) — khó đảo ngược một khi
                   Package 1.2–1.6 bắt đầu elaborate dựa trên nó.
  Status (v0.3):   **RESOLVED** — [ADR-015](../adr/ADR-015.md) v0.3, `Approved` (Product
                   Owner, 2026-08-03). Official Phase 1 module decomposition/dependency-graph
                   baseline established, pin bất biến, exact-artifact reference. ADR-015 vẫn
                   controlling/immutable cho toàn bộ module inventory NGOÀI phạm vi SCOPED mà
                   ADR-016 v0.8 (Decision 2 dưới) amend.
  Consequence:     ADR gate condition cho Decision 1 nay THỎA — NHƯNG một mình Decision 1
                   Approved KHÔNG đủ cho Consolidated Stable; xem Consequence tổng hợp tại
                   Decision 2 dưới và §15.

Decision 2 — decision-engine hybrid taxonomy (primary runtime_service, secondary
             decision_evaluation):
  Classification:  ADR REQUIRED.
  Rule applied:    Chapter 7 §7.1 điều kiện 4 — hybrid declaration bắt buộc ADR. Decision
                   Engine sở hữu CẢ authoritative Decision/Trade Intent record (runtime_
                   service core) LẪN deterministic evaluation logic mà điều kiện 1 của
                   §7.1 (responsibility không thể tách hợp lý) chưa được chứng minh —
                   candidate này KHÔNG tự chứng minh đủ 4 điều kiện, do đó hybrid status
                   CHƯA hợp lệ cho tới khi ADR resolve đúng bốn điều kiện đó.
  Status (v0.3):   **RESOLVED** — [ADR-016](../adr/ADR-016.md) v0.8, `Approved` (Product
                   Owner, 2026-08-04). Outcome: **Candidate B (split) SELECTED**, hybrid
                   (Candidate A) REJECTED — `decision-engine` tách thành
                   `decision-evaluation-engine` (compute_engine, non-authoritative
                   deterministic evaluation; KHÔNG Decision/Trade Intent identity, KHÔNG
                   Risk approval, KHÔNG Execution authority) + `decision-authority-service`
                   (runtime_service, sole invariant-validation/Decision-append/Trade-Intent-
                   identity authority). Governance mechanism: **Mechanism A** — ADR-016 v0.8
                   tự nó amend hiệu lực kiểm soát của ADR-015 SCOPED cho module identity/
                   dependency edge liên quan (KHÔNG toàn bộ ADR-015 — 21/22 module còn lại
                   không đổi). Bốn residual risk CHẤP NHẬN bởi Product Owner tại approval
                   (Strategy Plugin/Evaluation boundary; evaluation-proposal Domain Contract
                   gap; `attempt_outcome` mapping gap; operational/dependency/replay
                   complexity) — GIỮ NGUYÊN, KHÔNG resolve tại Package 1.1 correction này.
  Consequence:     ADR gate condition cho CẢ Decision 1 VÀ Decision 2 nay THỎA (cả hai
                   Approved). Package 1.1 candidate (module-registry.yaml/
                   system-decomposition.md v0.3) đã align với quyết định — NHƯNG Package 1.1
                   VẪN KHÔNG được Consolidated Stable: Review A + Independent Review B trên
                   chính candidate v0.3 này (post-correction) + Product Owner consolidation
                   decision CHƯA thực hiện (§15). ADR Approved ≠ Package artifact tự động
                   Consolidated Stable — hai bước riêng biệt theo package-lifecycle/
                   artifact-lifecycle separation đã dùng nhất quán trong toàn bộ session này.

Decision 2b — risk-gateway taxonomy (P11-A-MAJ-01 correction, đóng finding):
  Classification:  ADR NOT REQUIRED — KHÔNG phải vì "Chapter 7 §7.1 worked example waive
                   ADR" (phát biểu SAI đã sửa, xem module-registry.yaml), mà vì Risk
                   Gateway KHÔNG CÒN được khai báo `hybrid` — nó là `runtime_service`
                   THUẦN, một primary taxonomy type duy nhất.
  Rule applied:    Chapter 7 §7.3 tường minh: "Việc một module thuộc Type 3 (Runtime
                   Service) KHÔNG có nghĩa nó chỉ làm I/O thuần túy" — Risk Policy logic
                   (exposure limit, approve/reject, risk-increasing detection, kill
                   switch) LÀ business logic hợp lệ CỦA CHÍNH primary responsibility Risk
                   Gateway (Chapter 3 §3.1: "Risk Policy logic... Risk Gateway sở hữu và
                   bắt buộc phải có — đây LÀ business logic hợp lệ của đúng responsibility
                   này"), KHÔNG phải một secondary taxonomy type cạnh tranh với runtime_
                   service. Runtime Service taxonomy tự nó CHO PHÉP authoritative business
                   policy/control logic — không cần khai báo hybrid, không cần ADR-7.1-
                   điều-kiện-4 cho trường hợp này. Chapter 7 §7.1's worked example (dòng
                   54, "Risk Gateway — primary runtime_service, secondary risk_policy_
                   evaluation") minh họa RẰNG risk policy CÓ THỂ được framed như secondary
                   responsibility hợp lệ NẾU một candidate chọn khai báo hybrid — nhưng
                   KHÔNG BẮT BUỘC candidate đó phải khai báo hybrid; §7.3 xác nhận cách
                   đọc thay thế (risk policy là primary-responsibility-nội-tại) hợp lệ
                   tương đương và KHÔNG kích hoạt điều kiện 4 (ADR) vì KHÔNG có hybrid nào
                   được khai báo. Correction này chọn cách đọc §7.3 — không tạo ADR.

Decision 3 — Process/runtime boundary cụ thể (module nào deploy độc lập, module nào
             in-process):
  Classification:  ADR DECISION DEFERRED.
  Rule applied:    Package 1.1 KHÔNG thiết kế deployment topology (explicit non-goal) —
                   chưa có quyết định cụ thể để phân loại; sẽ resolve khi deployment
                   topology thực sự được đề xuất (Package 1.2 trở đi).

Decision 4 — Backtest domain-entity/authoritative-ownership boundary (DD-001):
  Classification:  ADR DECISION DEFERRED.
  Rule applied:    Chưa có quyết định cụ thể — blocked trên DD-001 (Domain Contract
                   authoring), bản thân DD-001's resolution CÓ THỂ thuộc diện ADR Required
                   sau này nhưng chưa được đề xuất tại đây.

Decision 5 — strategy-plugin-host là Compute Engine (Strategy Plugin taxonomy):
  Classification:  ADR NOT REQUIRED.
  Rule applied:    Chapter 9 §9.1 đã pre-classify tường minh: "Strategy Plugin điển hình
                   là Compute Engine" — Package 1.1 chỉ áp dụng phân loại đã có, KHÔNG tạo
                   plugin type/capability mới (Chapter 9 §9.10).

Decision 5b — plugin-release-manager là module operational riêng biệt khỏi Plugin
              Definition identity (P11-A-MAJ-02 correction, đóng finding):
  Classification:  ADR NOT REQUIRED.
  Rule applied:    Module này KHÔNG sở hữu architecture identity (Plugin Definition/
                   taxonomy — authority đó DUY NHẤT ở module-registry.yaml, không đổi) —
                   chỉ operational fact (Plugin Version→artifact resolution, runtime
                   compatibility, activation coordination, Chapter 9 §9.1/§9.5). KHÔNG
                   plugin type/capability mới, KHÔNG authority/permission model mới
                   (Chapter 9 §9.10) — chỉ đổi tên + thu hẹp responsibility của một module
                   đã candidate, chưa Consolidated Stable.

Decision 6 — market-reference-service / market-data-ingestion là hai module riêng biệt
             (thay vì một "Data Layer" gộp):
  Classification:  ADR NOT REQUIRED.
  Rule applied:    Trực tiếp phản ánh hai context ĐÃ đăng ký riêng biệt tại context-map.yaml
                   (instrument-venue-reference, market-data-observation, Chapter 4 §4.2,
                   authority đã tồn tại) — không phải quyết định module-taxonomy mới.

Decision 7 — command-query-api-surface / review-evidence-service / ux-application-shell
             là module cross-cutting không sở hữu capability/context riêng:
  Classification:  ADR NOT REQUIRED.
  Rule applied:    owns_authoritative_state: false cho cả ba — không tạo authoritative
                   ownership boundary mới; định danh module KHÔNG tự nó là "process/
                   runtime boundary" hay "authority/permission model" change (Chapter 9
                   §9.10) tại mức candidate này.

Decision 8 — custody/signing trust boundary: đăng ký hai module mới
             (custody-signing-service, exchange-adapter), authority category mới
             (secret_consuming security_classification, direct exchange-credential-use
             authority), dependency-graph mở rộng (v0.5):
  Classification:  ADR REQUIRED.
  Rule applied:    Governance §4b — thêm module mới với published boundary/responsibility
                   riêng + authority mới (direct credential use) LÀ "Module Taxonomy/
                   dependency graph" change → Required, đúng nguyên tắc đã áp dụng cho
                   Decision 1.
  Status (v0.5):   **RESOLVED** — [ADR-017](../adr/ADR-017.md) v0.2, `Approved` (Product
                   Owner, 2026-08-04T20:08:00+07:00) — "I approve ADR-017 v0.2 — Custody
                   & Signing Trust Boundary — selecting Option C, the split
                   Custody/Signing Service and Exchange Adapter architecture, as the
                   current Approved architecture decision." ADR-017 §9 định nghĩa CHÍNH
                   XÁC registry-impact scope mà transaction v0.5 này thực hiện — KHÔNG mở
                   rộng ngoài đó (execution-engine → exchange-adapter LIVE edge KHÔNG
                   thêm, đúng ADR-017 §9a Stage 1/Stage 2 distinction).
  Consequence:     ADR gate condition cho Decision 8 nay THỎA — NHƯNG một mình ADR Approved
                   KHÔNG đủ cho Package 1.1 v0.5 `Consolidated Stable`; cùng nguyên tắc đã
                   áp dụng cho Decision 1/Decision 2 tại v0.2/v0.3 — package_lifecycle
                   REVERT về `candidate`, một vòng Review A + Independent Review B +
                   Product Owner consolidation decision MỚI trên chính candidate v0.5 này
                   là bắt buộc (§15), CHƯA thực hiện tại transaction này.
```

## 13. Quality-gate applicability

```text
Trigger A (universal invariant conformance):        ÁP DỤNG cho toàn bộ 25 module — mọi
                                                      responsibility/dependency-direction
                                                      claim trong module-registry.yaml phải
                                                      conform I-1..I-13 by design (đã tự-
                                                      kiểm bounded bởi §5/§6/§7 — KHÔNG
                                                      tuyên bố đã pass executable test nào).
Trigger B (executable-implementation coverage):     DEFERRED — không executable
                                                      implementation ở giai đoạn architecture
                                                      candidate này.
Trigger C (tier/chaos/parity):                       DEFERRED — cùng lý do B; tier
                                                      assignment (Tier 0/1/2/3) sẽ resolve
                                                      từ module-registry.yaml theo Chapter
                                                      13 §13.4 nhánh 1 KHI Phase 3 build,
                                                      KHÔNG tại Package 1.1.
Trigger D (responsibility/boundary-triggered):       CÓ ĐIỀU KIỆN — module có
                                                      `security_classification` ≠ `none`
                                                      (`market-data-ingestion`,
                                                      `account-service`, `risk-gateway`,
                                                      `execution-engine`,
                                                      `command-query-api-surface`,
                                                      `custody-signing-service` [v0.5,
                                                      `secret_consuming`],
                                                      `exchange-adapter` [v0.5,
                                                      `trust_boundary_candidate`]) đã được
                                                      ĐỊNH DANH nhưng KHÔNG design; Trigger D
                                                      thực sự evaluate khi Package 1.2 định
                                                      nghĩa concrete boundary.
Trigger E (schema/contract compatibility):           CÓ ĐIỀU KIỆN — `module-registry.yaml`
                                                      CÓ THỂ trở thành published schema nếu
                                                      downstream tooling tiêu thụ nó trực
                                                      tiếp; chưa xác nhận tại candidate này.
```

**KHÔNG tuyên bố bất kỳ implementation test nào đã pass** — mọi trigger trên là PLANNING/CLASSIFICATION, không phải executed evidence.

## 14. Explicit non-goals

```text
KHÔNG author Package 1.2 (Security & Custody Baseline detailed design).
KHÔNG author Package 1.3-A/B/C/D (Engine Architecture detailed design).
KHÔNG author Package 1.4 (API Architecture detailed design).
KHÔNG author Package 1.5 (Database Architecture detailed design).
KHÔNG author Package 1.6 (UX Architecture detailed design).
KHÔNG tạo implementation source code.
KHÔNG chọn cloud provider.
KHÔNG chọn programming language/framework.
KHÔNG chọn database technology.
KHÔNG chọn event broker.
KHÔNG thiết kế deployment topology ngoài mức bắt buộc tối thiểu cho module boundary
  (module_id/depends_on chỉ định danh, KHÔNG chỉ định process/container/host).
KHÔNG tạo/approve Phase 1 DoD.
KHÔNG approve Package 1.1 (tài liệu này).
KHÔNG tuyên bố Phase 1 hoàn thành.
KHÔNG mở Phase 2.
KHÔNG authorize Live.
KHÔNG design authentication/authorization implementation, key management, HSM, wallet
  custody mechanics, security vendor/tool selection.
KHÔNG author field-level API schema, endpoint list, database table, DDL, database
  technology, partitioning strategy, storage implementation.
KHÔNG author detailed UX component tree/frontend framework decision.
KHÔNG redefine domain entity, domain invariant, product behavior, use-case outcome, UX
  acceptance requirement, hay existing ADR decision nào.
```

## 15. Package review and consolidation conditions

```text
Review A scope:            Module completeness (25/25 bounded, no god module); taxonomy
                            correctness (Chapter 7 §7.1 exhaustive, no invented type);
                            dependency coherence (no cycle, established pipeline direction
                            preserved); authority/source-of-truth correctness (I-12, no
                            competing owns_authoritative_state: true cho cùng context);
                            no prohibited dependency (Raw Regime/Structure independence,
                            Plugin non-bypass, Execution non-bypass, Backtest non-PAPER
                            boundary, Custody/Signing non-bypass — tất cả script-checked
                            §13 phía trên); Product/UC/UX coverage completeness (34/34,
                            21/21, 17/17, zero orphan, custody-signing-service/
                            exchange-adapter correctly deferred not orphaned — §10);
                            Domain coverage completeness (11/11 capability, 15/15
                            context); ADR Scope Rule correctness (§12 — ba Decision REQUIRED
                            không bị silently approve); no silent semantic invention; no
                            implementation leakage (§14). **Cập nhật (v0.5):** xác nhận
                            candidate v0.5 align CHÍNH XÁC với ADR-017 v0.2 đã Approved —
                            KHÔNG expand ADR-017 §9 registry-impact scope ra ngoài đúng hai
                            module + dependency edge đã định nghĩa, KHÔNG thêm active
                            execution-engine → exchange-adapter edge (Stage 1/Stage 2
                            distinction, §9a ADR-017, đúng bảo toàn), KHÔNG silently
                            resolve preserved gap nào (§11). **Cập nhật (v0.6):** xác nhận
                            `custody-signing-service.phase.elaborated_by` KHÔNG còn tuyên
                            bố false Package 1.2 coverage — đóng `P11V05-A-MAJ-01`/
                            `P11-v0.5-IRB-MAJ-01`; xác nhận Package 1.2 v0.2 chỉ được mô tả
                            review-clean cho ĐÚNG phạm vi đã review của nó (account-service),
                            KHÔNG mở rộng ngầm sang custody-signing-service.
Independent Review B
  scope:                   Độc lập xác nhận CÙNG phạm vi trên, đặc biệt (v0.5, sau Decision
                            8 Approved): (a) xác nhận `custody-signing-service` là module
                            DUY NHẤT được phép dùng exchange credential trực tiếp
                            (forbidden_dependencies loại trừ toàn bộ business/execution/API
                            authority — script-checked); (b) xác nhận
                            `exchange-adapter`'s `owns_authoritative_state: true` CHỈ scoped
                            raw venue-interaction evidence, KHÔNG execution-observation/
                            ExecutionResult authority (execution-result-processor's authority
                            KHÔNG bị đổi); (c) xác nhận KHÔNG active
                            execution-engine → exchange-adapter edge tồn tại trong
                            `depends_on` (chỉ notes/prose ghi nhận future prerequisite); (d)
                            xác nhận `phase.elaborated_by: null` của exchange-adapter KHÔNG
                            invent package ID mới; (e) xác nhận `module-registry.yaml`
                            machine-parseable, mọi script-check (§13, unique ID/valid
                            reference/no cycle/no contradiction/full coverage) tái tạo được
                            độc lập, module count = 25.
Product Owner decision
  point:                   SAU khi Review A + Independent Review B hoàn tất trên chính
                            candidate v0.6 này (Blocker 0/Major 0/Minor 0) — Product Owner
                            mới có đủ điều kiện quyết `Consolidated Stable` cho Package 1.1
                            v0.6. **Cập nhật (2026-08-05T08:40:00+07:00, Product Owner
                            consolidation decision):** điều kiện trên nay ĐẦY ĐỦ — Review A
                            CLEAN + Independent Review B CLEAN trên candidate v0.6 (post
                            `P11V05-A-MAJ-01`/`P11-v0.5-IRB-MAJ-01` bounded correction,
                            Blocker 0/Major 0/Minor 0) hoàn tất. Product Owner đã quyết
                            định: "I approve consolidation of Package 1.1 v0.6 as the
                            current Consolidated Stable module-registry and
                            system-decomposition baseline." — Package 1.1 nay
                            **`Consolidated Stable`**.
Consolidation condition:  Decision 8 ADR (§12) Approved (**THỎA** — ADR-017 v0.2,
                            2026-08-04T20:08:00+07:00); §13 script-check tái tạo PASS
                            (**THỎA** — 25 unique module_id, mọi depends_on/
                            forbidden_dependencies reference resolve, zero cycle, zero
                            overlap, tái tạo tại transaction này); §10 coverage totals
                            (34/21/17/11/15, zero orphan) không đổi kể từ baseline trước
                            (**THỎA, xác nhận tại §10**); forbidden-scope verification
                            (không Package 1.2–1.6 content ngoài đúng registry-impact scope
                            ADR-017 §9 đã authorize, không Product/Domain semantic thay đổi,
                            KHÔNG active LIVE edge, KHÔNG resolve preserved gap) PASS (**THỎA,
                            xác nhận qua diff scope transaction này**); Review A + Independent
                            Review B trên candidate v0.6 — **THỎA, CLEAN, 2026-08-05**; Zero
                            unresolved Blocker/Major trên candidate v0.6 — **THỎA**.
                            **Mọi điều kiện consolidation ĐÃ thỏa — Package 1.1 v0.6 nay
                            `Consolidated Stable`.** Consolidation KHÔNG tự động: assign
                            elaborating package cho `custody-signing-service`/
                            `exchange-adapter`; mở rộng Package 1.2 review coverage; sửa
                            Package 1.2/Package 1.3-D; kích hoạt Execution Engine → Exchange
                            Adapter; authorize LIVE execution; authorize implementation;
                            resolve kill-switch-state ownership; resolve DD-003; pass Gate 2;
                            tuyên bố Phase 1 hoàn thành; mở Phase 2.

**Cập nhật (2026-08-04, v0.4 bounded parity correction, lịch sử):** `P13B-IRB-MAJ-01`/`P13B-IRB-MAJ-02`/`P13B-IRB-MAJ-03`/`P13B-A-MIN-01`/`P13B-IRB-MIN-01` (Package 1.3-B Review A/Independent Review B findings) sửa — xem banner phía trên. Correction áp dụng semantics ĐÃ pin sẵn tại `feature.md`/`context.md` (Package 0.2-B3/B4, Consolidated Stable, KHÔNG đổi) vào `depends_on`/`emits` registry entry còn thiếu — KHÔNG một kiến trúc option/decision mới, KHÔNG kích hoạt ADR Scope Rule (§12 KHÔNG có Decision mới). `package_lifecycle: Consolidated Stable` KHÔNG reset tại v0.4 — correction đó nhận một bounded verification riêng, KHÔNG một full Review A + Independent Review B round mới. **v0.5 KHÁC BẢN CHẤT** — đăng ký module mới + authority mới (Decision 8, ADR REQUIRED) LÀ một kiến trúc/semantic change thật, đúng nguyên tắc đã áp dụng cho v0.2→v0.3 — `package_lifecycle` REVERT về `candidate`, KHÔNG giữ `Consolidated Stable` như v0.4 đã làm.

**Cập nhật (2026-08-05T08:40:00+07:00, mechanical consolidation lifecycle transaction, lịch sử):** SAU v0.6 bounded correction (đóng `P11V05-A-MAJ-01`/`P11-v0.5-IRB-MAJ-01`, xem banner phía trên) và Review A CLEAN + Independent Review B CLEAN trên candidate v0.6, Product Owner quyết định: "I approve consolidation of Package 1.1 v0.6 as the current Consolidated Stable module-registry and system-decomposition baseline." — `package_lifecycle: candidate → Consolidated Stable`, `version: "0.6"` KHÔNG đổi (mechanical lifecycle transaction, KHÔNG content/architecture change). Đúng tiền lệ v0.3's consolidation transaction — CHỈ lifecycle-state field/prose thay đổi, architecture semantics byte-identical về nội dung.
```
