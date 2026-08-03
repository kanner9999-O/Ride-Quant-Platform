---
id: system-decomposition
title: "Package 1.1 — System Decomposition & Module Registry"
version: "0.2"
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

**CANDIDATE — status: Draft, KHÔNG Consolidated Stable, KHÔNG Approved.** Đây là first authored candidate cho Package 1.1, theo `docs/architecture/phase-1-plan.md` v0.2 (`Consolidated Stable`) §5.3/§7/§8. Tài liệu này KHÔNG tự approve/consolidate chính nó — Product Owner decision riêng, sau Review A + Independent Review B, mới có thẩm quyền đó (§15).

**Ghi chú tường minh bắt buộc (§12):** Package này phát hiện MỘT quyết định thuộc diện **ADR REQUIRED** — chính module dependency graph chính thức đề xuất tại §5/`module-registry.yaml`. Theo đúng "Important boundary" của task gốc: candidate này ĐƯỢC author đầy đủ, quyết định ADR-required được ghi lại tường minh, nhưng Package 1.1 **KHÔNG được đánh dấu `Consolidated Stable`** cho tới khi ADR đó `Approved` (hoặc Product Owner quyết định khác qua Decision Workflow). KHÔNG ADR nào được tạo/approve tại transaction này.

**v0.2 — bounded correction (2026-08-03), đóng `P11-A-MAJ-01`/`P11-A-MAJ-02`/`P11-A-MIN-01`** (Review A REVISE + Independent Review B REVISE trên v0.1, findings CONFIRMED — Blocker 0, Major 2, Minor 1): (1) `P11-A-MAJ-01` — `risk-gateway` trước đây khai `hybrid` với `adr_status: "ADR NOT REQUIRED"`, sai vì Chapter 7 §7.1 điều kiện 4 đòi ADR cho MỌI hybrid retained, kể cả worked example — sửa: `risk-gateway` nay `hybrid: null`, `runtime_service` thuần, risk policy logic là primary responsibility hợp lệ theo Chapter 7 §7.3 (KHÔNG phải secondary taxonomy) — KHÔNG tạo ADR. (2) `P11-A-MAJ-02` — `plugin-registry-service` trước đây claim sở hữu Plugin Definition identity/taxonomy, xung đột authority với chính `module-registry.yaml` (I-12/Chapter 9 §9.1) — sửa: đổi tên thành `plugin-release-manager`, thu hẹp về operational fact ONLY (Plugin Version→artifact resolution, runtime compatibility, activation coordination); `module-registry.yaml` tường minh là authority DUY NHẤT cho Plugin Definition identity/taxonomy/architecture responsibility. (3) `P11-A-MIN-01` — taxonomy tally và state-authority tally trước đây sai số (đếm nhầm, category chồng lấn "cross-cutting no state") — sửa: hai tally tách biệt, script-verified, exhaustive/mutually-exclusive (§4). Bounded — KHÔNG reopen module boundary khác (Market/Data, Structure/Regime/Feature/Context, Strategy Engine, Decision→Risk→Execution ordering, ExecutionResult/Fill/Position, Replay, Backtest, Paper boundary, API Surface, Review Evidence, UX Shell), KHÔNG đổi PR/UC/UX/Domain coverage, KHÔNG đổi DD-001/DD-003/Structure-aware-Regime deferral/OQ-001/OQ-002/OQ-003. `decision-engine` hybrid vẫn `ADR REQUIRED` (§12 Decision 2, không đổi). Module count vẫn 22 (đổi tên, không thêm/bớt). `status: Draft`, `approved_by: null`, `approved_at: null`, `package lifecycle: candidate` không đổi. Findings corrected nhưng CHƯA verified — chờ bounded Review A + independent bounded Review B mới.

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

**22 module** — xem `module-registry.yaml` cho định nghĩa đầy đủ từng field. Tóm tắt:

| module_id | Taxonomy | Owns authoritative state | Elaborated by |
|---|---|---|---|
| `market-reference-service` | runtime_service | Yes | 1.3-A |
| `market-data-ingestion` | runtime_service | Yes | 1.3-A |
| `structure-engine` | compute_engine | Yes | 1.3-A |
| `raw-regime-engine` | compute_engine | Yes | 1.3-A |
| `feature-engine` | compute_engine | Yes | 1.3-B |
| `context-aggregator` | projection | No | 1.3-B |
| `account-service` | runtime_service | Yes | 1.2 |
| `strategy-engine` | runtime_service | Yes | 1.3-C |
| `plugin-release-manager` | runtime_service | Yes (operational fact only, §12 Decision 5b) | 1.3-C |
| `strategy-plugin-host` | compute_engine | No | 1.3-C |
| `decision-engine` | runtime_service (potential hybrid, ADR REQUIRED, §12 Decision 2) | Yes | 1.3-C |
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

**Taxonomy tally (P11-A-MIN-01 correction — script-verified against `module-registry.yaml`, exhaustive/mutually-exclusive, sums to 22):**

```text
compute_engine   4   structure-engine, raw-regime-engine, feature-engine, strategy-plugin-host
projection       4   context-aggregator, position-projection, replay-integration-service,
                      review-evidence-service
runtime_service  14  market-reference-service, market-data-ingestion, account-service,
                      strategy-engine, plugin-release-manager, decision-engine, risk-gateway,
                      execution-engine, execution-result-processor, fill-processor,
                      backtest-orchestrator, paper-execution-boundary,
                      command-query-api-surface, ux-application-shell
total            22
```

**State-authority tally (separate dimension — DO NOT overlap with taxonomy tally above; script-verified, exhaustive/mutually-exclusive, sums to 22):**

```text
owns_authoritative_state: true      13  market-reference-service, market-data-ingestion,
                                         structure-engine, raw-regime-engine, feature-engine,
                                         account-service, strategy-engine,
                                         plugin-release-manager, decision-engine, risk-gateway,
                                         execution-engine, execution-result-processor,
                                         fill-processor
owns_authoritative_state: false     8   context-aggregator, strategy-plugin-host,
                                         position-projection, replay-integration-service,
                                         paper-execution-boundary, command-query-api-surface,
                                         review-evidence-service, ux-application-shell
owns_authoritative_state: deferred  1   backtest-orchestrator
total                                22
```

Ghi chú bắt buộc (đóng `P11-A-MIN-01`): "false" KHÔNG đồng nghĩa "Projection" — 4/8 module `false` là `runtime_service`/`compute_engine` (`strategy-plugin-host`, `paper-execution-boundary`, `command-query-api-surface`, `ux-application-shell`), KHÔNG chỉ bốn `projection` type. Hai chiều (taxonomy, state-authority) tách biệt hoàn toàn, KHÔNG dùng chung một bảng/tally.

## 5. Dependency graph

### 5.1 Text form (normative — diagram ở §5.2 chỉ minh họa)

```text
market-reference-service (root)
market-data-ingestion            → depends_on: market-reference-service
structure-engine                 → depends_on: market-data-ingestion
raw-regime-engine                → depends_on: market-data-ingestion
                                    (forbidden_dependencies: structure-engine — ADR-003/014)
feature-engine                   → depends_on: structure-engine, raw-regime-engine
context-aggregator               → depends_on: structure-engine, raw-regime-engine, feature-engine

account-service (root)

strategy-engine                  → depends_on: account-service
plugin-release-manager (root)
strategy-plugin-host             → depends_on: strategy-engine, context-aggregator,
                                    plugin-release-manager
                                    (forbidden_dependencies: execution-engine, risk-gateway,
                                    paper-execution-boundary)

decision-engine                  → depends_on: strategy-engine, strategy-plugin-host,
                                    context-aggregator
                                    (forbidden_dependencies: execution-engine,
                                    paper-execution-boundary)
risk-gateway                     → depends_on: decision-engine, account-service
execution-engine                 → depends_on: risk-gateway, paper-execution-boundary
                                    (forbidden_dependencies: strategy-engine,
                                    strategy-plugin-host, context-aggregator)
execution-result-processor       → depends_on: execution-engine, paper-execution-boundary
fill-processor                   → depends_on: execution-result-processor
position-projection              → depends_on: fill-processor

replay-integration-service       → depends_on: decision-engine, risk-gateway,
                                    execution-engine, execution-result-processor,
                                    fill-processor, position-projection

backtest-orchestrator            → depends_on: strategy-engine, decision-engine, risk-gateway
                                    (forbidden_dependencies: execution-engine,
                                    paper-execution-boundary, execution-result-processor,
                                    fill-processor, position-projection)
paper-execution-boundary (root — referenced BY execution-engine/execution-result-processor)

command-query-api-surface        → depends_on: [all 16 authoritative/projection modules]
review-evidence-service          → depends_on: decision-engine, risk-gateway,
                                    execution-engine, execution-result-processor,
                                    fill-processor, position-projection,
                                    replay-integration-service
ux-application-shell             → depends_on: command-query-api-surface
                                    (forbidden_dependencies: all 13 engine/projection
                                    modules directly — must go through API surface)
```

Validated (script-checked before commit, §13): 22 unique `module_id`; every `depends_on`/`forbidden_dependencies` reference resolves to an existing `module_id`; zero cycles in the `depends_on` graph; zero module has the same ID in both `depends_on` and `forbidden_dependencies`.

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
 Strategy Engine ──► Strategy Plugin Host ──► Decision Engine
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
(Replay Integration Service, Review Evidence Service: cross-cutting read layers over the chain.)
(Backtest Orchestrator: parallel non-PAPER path — explicitly forbidden from touching
 Execution/Paper/ExecutionResult/Fill/Position modules.)
(Command/Query/API Surface: fan-in from every authoritative/projection module.)
(UX Application Shell: depends ONLY on API Surface, never engines directly.)
```

## 6. Responsibility and ownership boundaries

Mỗi module trong `module-registry.yaml` khai báo tường minh `responsibilities` (sở hữu/tính toán gì), `emits`/`consumes` (publish/tiêu thụ loại contract gì), `forbidden_dependencies` (KHÔNG được phụ thuộc gì), và `owns_authoritative_state` (có phải nguồn thật duy nhất hay không, I-12). Không module nào generic — mỗi entry map trực tiếp về đúng một `capability_id`/`domain_context_id` đã đăng ký (§4.2), TRỪ ba module cross-cutting (`command-query-api-surface`, `review-evidence-service`, `ux-application-shell`) vốn KHÔNG sở hữu capability/context riêng theo thiết kế (routing/read/presentation layer thuần túy, không domain authority).

**God-module check:** không module nào có tên generic không bounded (không `CoreService`/`CommonService`/`PlatformManager`/`SharedEngine`/`UtilityModule`); mỗi module có đúng MỘT primary responsibility statement cụ thể.

## 7. Authority/source-of-truth map

Dùng ĐÚNG state-authority tally đã pin tại §4 (P11-A-MIN-01 correction) — KHÔNG lặp lại con số riêng ở đây (tránh hai nguồn lệch nhau, I-12):

```text
owns_authoritative_state: true      13  (xem §4 cho danh sách đầy đủ)
owns_authoritative_state: false     8   (xem §4 — KHÔNG chỉ bốn Projection; gồm cả
                                         strategy-plugin-host/paper-execution-boundary/
                                         command-query-api-surface/ux-application-shell)
owns_authoritative_state: deferred  1   backtest-orchestrator (DD-001)
```

I-12 conformance: mỗi domain concept resolve đúng MỘT authoritative module — không hai module nào cùng claim `owns_authoritative_state: true` cho cùng một `serves_contexts` entry (script-checked, §13). Bốn module taxonomy `projection` (`context-aggregator`, `position-projection`, `replay-integration-service`, `review-evidence-service`) KHÔNG BAO GIỜ trở thành authoritative source thay module gốc (Chapter 7 §7.4 — preserved) — đây là tập con của nhóm `owns_authoritative_state: false` (8 module), KHÔNG đồng nhất với toàn bộ nhóm đó.

## 8. Event/command/query interaction categories

`module-registry.yaml` field `consumes`/`emits` khai báo CATEGORY (`event` | `query` | `command`), KHÔNG field-level schema (đó là Package 1.4). Event log là authoritative source cho runtime fact/decision history (Chapter 8 §8.1) — transport/broker cụ thể KHÔNG authoritative (không quyết định tại Package 1.1). Mọi module authoritative emit `event`; Projection emit `query` (read contract); orchestration/boundary module (`account-service`, `strategy-engine`, `plugin-release-manager`) consume `command`.

## 9. Plugin boundaries

`plugin_relation` field: `none` (mặc định), `hosts` (`strategy-plugin-host`), `manages_release` (`plugin-release-manager`).

**Authority boundary tường minh (P11-A-MAJ-02 correction, đóng finding):** `module-registry.yaml` — CHÍNH tài liệu YAML này — là **authority DUY NHẤT** cho Plugin Definition identity, module existence, primary taxonomy, và architecture responsibility của MỌI module, kể cả module liên quan plugin (Chapter 7 §7.5, Chapter 9 §9.1). KHÔNG runtime module nào — kể cả `plugin-release-manager` — được sở hữu hay mutate các architecture fact đó. `plugin-release-manager` (đổi tên từ "Plugin Registry Service", đóng `P11-A-MAJ-02`) CHỈ sở hữu OPERATIONAL fact: Plugin Version → exact Package/Build Artifact content identity resolution, immutable release-manifest resolution (Chapter 9 §9.1, mô hình A/B), runtime compatibility/availability status của Plugin Runtime replica, và activation/deactivation coordination (Chapter 9 §9.5, validated compatibility set) — KHÔNG Plugin Definition identity/taxonomy, KHÔNG một registry thứ hai. `strategy-plugin-host` (Plugin Definition, taxonomy `compute_engine`) tự nó vẫn đăng ký DUY NHẤT tại `module-registry.yaml`, không đổi.

Strategy Plugin (`strategy-plugin-host`) KHÔNG được bypass Decision/Risk Gateway — `forbidden_dependencies: [execution-engine, risk-gateway, paper-execution-boundary]` enforce tại module-boundary level, đúng I-4/I-7. Decision-time visibility (Chapter 9 §9.5) là ràng buộc của chính `strategy-plugin-host`'s runtime behavior, elaborated đầy đủ tại Package 1.3-C — Package 1.1 chỉ pin boundary, KHÔNG thiết kế cơ chế cursor-bounded cụ thể.

## 10. Product/UC/UX coverage evidence

**Coverage method:** mỗi `UC-XXX` map về module chịu trách nhiệm chính, dựa trên "Domain vocabulary used" field của chính `UC-XXX` đó (`use-case-workflow.md` §6) đối chiếu `owns_authoritative_state`/`serves_contexts` của module. Mọi `PR-XXX`/screen kế thừa coverage từ `UC-XXX` nó trace tới (catalogue `use-case-workflow.md` §5, `ux-blueprint.md` §6) — many-to-many, KHÔNG one-module-per-PR/UC/screen.

| UC | Primary module | Supporting module(s) | PR(s) | Screen(s) |
|---|---|---|---|---|
| UC-001 | `context-aggregator` | `market-data-ingestion`, `structure-engine`, `raw-regime-engine`, `feature-engine` | PR-003, PR-015, PR-017 | SCR-001, VIEW-001 |
| UC-002 | `strategy-engine` | — | PR-001, PR-016 | VIEW-001 |
| UC-003 | `decision-engine` | — | PR-017 | VIEW-002 |
| UC-004 | `replay-integration-service` | `decision-engine`, `risk-gateway`, `execution-engine`, `execution-result-processor`, `fill-processor`, `position-projection` | PR-008, PR-018, PR-020 | SCR-002 |
| UC-005 | `decision-engine` | `replay-integration-service` | PR-010, PR-019 | VIEW-003 |
| UC-006 | `backtest-orchestrator` | `strategy-engine`, `decision-engine`, `risk-gateway` | PR-021, PR-022, PR-023 | SCR-003 |
| UC-007 | `backtest-orchestrator` | `decision-engine`, `risk-gateway` | PR-021, PR-009, PR-004, PR-005 | SCR-004 |
| UC-008 | `backtest-orchestrator` | — | PR-033 | SCR-004 |
| UC-009 | `backtest-orchestrator` | `strategy-engine` | PR-034 | SCR-004 |
| UC-010 | `backtest-orchestrator` | `strategy-engine` | PR-034 | SCR-005 |
| UC-011 | `decision-engine` | `risk-gateway`, `execution-engine`, `paper-execution-boundary`, `account-service` | PR-007, PR-024, PR-004, PR-005 | SCR-006 |
| UC-012 | `execution-result-processor` | `execution-engine` | PR-007, PR-024 | SCR-007 |
| UC-013 | `fill-processor` | `execution-result-processor` | PR-025 | SCR-007 |
| UC-014 | `position-projection` | `fill-processor` | PR-026 | SCR-007 |
| UC-015 | `execution-engine` | `paper-execution-boundary` | PR-027 | SCR-007 |
| UC-016 | `review-evidence-service` | `decision-engine`…`position-projection` (full chain) | PR-028, PR-004, PR-005 | SCR-008 |
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
| PR-014 | `WF-INV-9` (§4, lifecycle state hiển thị phản ánh transition đã khai báo) — cross-cutting | `decision-engine`, `risk-gateway`, `execution-engine`, `execution-result-processor`, `fill-processor` (mọi module sở hữu state machine) |

Với năm PR trên, coverage đến từ **Workflow Invariant** (`WF-INV-XXX`, cross-cutting toàn bộ workflow, KHÔNG gắn riêng một UC) hoặc từ **alternate-flow** của một UC cụ thể (không xuất hiện ở "Primary PR(s)" nhưng vẫn material) — cả hai đều là traceability hợp lệ theo `use-case-workflow.md` §"Quy tắc traceability nguồn". Coverage totals §10 (34/34) đã tính đủ năm PR này.

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
  Consequence:     Package 1.1 KHÔNG được Consolidated Stable cho tới khi ADR này Approved
                   (hoặc Product Owner quyết định khác qua Decision Workflow) — xem banner
                   đầu tài liệu VÀ §15.

Decision 2 — decision-engine hybrid taxonomy (primary runtime_service, secondary
             decision_evaluation):
  Classification:  ADR REQUIRED.
  Rule applied:    Chapter 7 §7.1 điều kiện 4 — hybrid declaration bắt buộc ADR. Decision
                   Engine sở hữu CẢ authoritative Decision/Trade Intent record (runtime_
                   service core) LẪN deterministic evaluation logic mà điều kiện 1 của
                   §7.1 (responsibility không thể tách hợp lý) chưa được chứng minh —
                   candidate này KHÔNG tự chứng minh đủ 4 điều kiện, do đó hybrid status
                   CHƯA hợp lệ cho tới khi ADR resolve đúng bốn điều kiện đó.

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
```

## 13. Quality-gate applicability

```text
Trigger A (universal invariant conformance):        ÁP DỤNG cho toàn bộ 22 module — mọi
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
                                                      `command-query-api-surface`) đã được
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
Review A scope:            Module completeness (22/22 bounded, no god module); taxonomy
                            correctness (Chapter 7 §7.1 exhaustive, no invented type);
                            dependency coherence (no cycle, established pipeline direction
                            preserved); authority/source-of-truth correctness (I-12, no
                            competing owns_authoritative_state: true cho cùng context);
                            no prohibited dependency (Raw Regime/Structure independence,
                            Plugin non-bypass, Execution non-bypass, Backtest non-PAPER
                            boundary — tất cả script-checked §13 phía trên); Product/UC/UX
                            coverage completeness (34/34, 21/21, 17/17, zero orphan);
                            Domain coverage completeness (11/11 capability, 15/15
                            context); ADR Scope Rule correctness (§12 — hai Decision REQUIRED
                            không bị silently approve); no silent semantic invention; no
                            implementation leakage (§14).
Independent Review B
  scope:                   Độc lập xác nhận CÙNG phạm vi trên, đặc biệt: (a) xác nhận
                            Decision 1/Decision 2 tại §12 THỰC SỰ là ADR-required (không bị
                            hidden/downplay); (b) xác nhận DD-001/DD-003/Structure-aware-
                            Regime deferred items KHÔNG bị lấp bằng semantics tự phát minh;
                            (c) xác nhận `module-registry.yaml` machine-parseable, mọi
                            script-check (§13, unique ID/valid reference/no cycle/no
                            contradiction/full coverage) tái tạo được độc lập.
Product Owner decision
  point:                   SAU khi Review A + Review B hoàn tất VÀ Decision 1 (module
                            dependency graph ADR) + Decision 2 (decision-engine hybrid ADR)
                            đã `Approved` — Product Owner mới có đủ điều kiện quyết
                            Consolidated Stable cho Package 1.1. TRƯỚC đó, package ở
                            trạng thái candidate/reviewed nhưng KHÔNG thể Consolidated
                            Stable dù Review A/B đều CLEAN, đúng "Important boundary" của
                            task gốc.
Consolidation condition:  Zero unresolved Blocker/Major; Decision 1 + Decision 2 ADR (§12)
                            Approved; §13 script-check tái tạo PASS; §10 coverage totals
                            (34/21/17/11/15, zero orphan) không đổi kể từ Review A/B
                            baseline; forbidden-scope verification (không Package 1.2–1.6
                            content, không Product/Domain semantic thay đổi) PASS.
```
