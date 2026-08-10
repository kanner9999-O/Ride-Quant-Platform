---
id: database-architecture
title: "Package 1.5 — Database Architecture"
version: "0.3"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-05"
last_review: null
next_review: null
depends_on: ["00-governance", "02-platform-invariants", "07-module-taxonomy", "08-event-model", "13-quality-gates", "14-roadmap"]
---

# Package 1.5 — Database Architecture

**v0.3 — bounded freshness correction (2026-08-10), đóng `P15-BCC-MAJ-01` (Phase-wide Backward Consistency Check finding, `phase1-bcc-001.md`), KHÔNG redesign persistence, KHÔNG mở lại Review A/Independent Review B/Product Owner consolidation decision, KHÔNG reconsolidate, vai trò: `Package 1.5 BCC Major Bounded Correction Executor`:** §2.1's registry-classification transcription VÀ tự-chứng-nhận fidelity claim đã stale — `review-evidence-service.depends_on` liệt kê ĐÚNG bảy module, tự chứng nhận "nguyên trạng từ `module-registry.yaml` v0.7... KHÔNG thêm/bớt một dependency edge" — SAI so với registry HIỆN TẠI (v1.1): một edge thứ tám (`decision-evaluation-engine`) ĐÃ được thêm SAU Package 1.5 v0.2's Consolidated Stable boundary (2026-08-05T16:45), bởi ADR-021 alignment (2026-08-07, VIEW-003 Decision replay-parity recomputation delegation, non-authoritative) — một transaction governed HOÀN TOÀN riêng biệt, KHÔNG bởi Package 1.5. Sửa: §2.1's `depends_on` nay liệt kê ĐÚNG tám module VÀ tự-chứng-nhận đúng lịch sử (Package 1.5 CHÍNH NÓ KHÔNG tự thêm/bớt edge nào; edge thứ tám ĐÃ được thêm SAU bởi ADR-021, riêng biệt); registry authority reference sửa `v0.7 → v1.1`; §4 bổ sung một `[Cập nhật]` paragraph bounded ghi nhận edge thứ tám VÀ carry-forward interaction-mechanism gap tương ứng cho nó (CÙNG loại gap đã ghi nhận cho hai query-emitting dependency, KHÔNG resolve). **KHÔNG đổi:** `review-evidence-service` VẪN `module_type: projection`, `owns_authoritative_state: false`; persistence authority model/store-per-concept map/projection rebuild strategy (KHÔNG store/category mới — `decision-evaluation-engine` KHÔNG sở hữu persistence authority, §5); ADR-021's recomputation delegation VẪN non-authoritative; retention/deletion policy ownership gap VẪN unresolved; mọi Preserved gap khác (§11, KHÔNG đổi); §3/§5–§13 (byte-identical, KHÔNG chạm). `module-registry.yaml`/ADR-021/ADR-022/ADR-023/mọi package khác KHÔNG sửa tại transaction này (byte-identical, git diff empty). `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi — **`package lifecycle` VẪN `Consolidated Stable`, KHÔNG revert về `candidate`** (đây LÀ bounded factual correction — sửa một transcription/self-certification claim đã stale khớp lại registry hiện tại, KHÔNG một quyết định architecture mới, KHÔNG mở lại baseline đã review — cùng nguyên tắc đã dùng cho `structure-regime-architecture.md` v0.4's bounded freshness correction, KHÔNG cần reconsolidate). `P15-BCC-MAJ-01` CLOSED. `G2-RDY-BLK-02` VẪN chờ xác nhận riêng (transaction Phase-wide BCC follow-up, KHÔNG tại đây). KHÔNG Phase-level Gate review nào thực hiện, KHÔNG Gate 2 decision, KHÔNG rerun Quality Gate.

**CONSOLIDATED STABLE (package lifecycle, 2026-08-05T16:45:00+07:00, Product Owner decision) — status: Draft, KHÔNG Approved.** Package 1.5 v0.2 đạt `Consolidated Stable` SAU: Review A (REVISE trên v0.1, đóng `P15-A-MAJ-01`/`P15-A-MAJ-02`/`P15-A-MIN-01`/`P15-A-MIN-02`) → bounded verification (CLEAN, Blocker 0/Major 0/Minor 0) → Independent Review B (CLEAN, Blocker 0/Major 0/Minor 0, consolidation readiness: READY) → Product Owner consolidation decision. Product Owner đã quyết định nguyên văn: "I approve consolidation of Package 1.5 v0.2 as the current Consolidated Stable Database Architecture baseline, while preserving review-evidence-service as a non-authoritative projection and evidence boundary, all existing source-of-truth and authoritative ownership boundaries, the documented contract-category interaction gap, the unresolved retention/deletion policy ownership gap, all append-only correction, projection rebuild, custody, security, failure, replay, PAPER/LIVE separation, and non-goal constraints, and LIVE Unauthorized." `Consolidated Stable` LÀ package lifecycle/readiness state (Chapter 0 §7.1) — KHÔNG có nghĩa artifact `Approved`; `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi. Mechanical lifecycle transaction — `version: "0.2"` UNCHANGED (no content/architecture change), package lifecycle: `candidate → Consolidated Stable`.

**CANDIDATE (package lifecycle, HISTORICAL — superseded bởi Consolidated Stable trên) — status: Draft, khi đó KHÔNG Consolidated Stable, KHÔNG Approved.** Package 1.5 v0.1 — candidate đầu tiên, author dựa trên Package 1.1 `Consolidated Stable` (v0.7, 25 module, module-registry.yaml/system-decomposition.md), Package 1.2 `Consolidated Stable` (v0.4), Package 1.3-A/1.3-B/1.3-C/1.3-D `Consolidated Stable`, Package 1.4 `Consolidated Stable` (v0.3), VÀ [`phase-1-plan.md`](phase-1-plan.md) v0.4 (`Approved`) §"Package 1.5 — Database Architecture". Đây LÀ một authoring transaction, KHÔNG PHẢI một review/consolidation transaction. Chưa qua Review A/Independent Review B, chưa có Product Owner consolidation decision.

**v0.2 — bounded correction (2026-08-05), đóng bốn Review A finding trên v0.1 (`P15-A-MAJ-01`/`P15-A-MAJ-02`/`P15-A-MIN-01`/`P15-A-MIN-02`), KHÔNG redesign/mở rộng scope:** (a) `P15-A-MAJ-01` — §4 sửa: bỏ claim review-evidence-service consume event từ đủ bảy dependency — phân biệt tường minh năm event-emitting dependency (decision-authority-service/risk-gateway/execution-engine/execution-result-processor/fill-processor) khỏi hai query-emitting projection (position-projection/replay-integration-service); ghi nhận contract-category interaction gap (registry xác lập dependency relationship NHƯNG KHÔNG đầy đủ xác lập cơ chế lấy output từ hai query-emitting dependency dưới `consumes: [event]`); KHÔNG invent event emission mới, KHÔNG invent query consumption mới, KHÔNG dependency edge mới. (b) `P15-A-MAJ-02` — §2.2/§8 sửa: bỏ mọi statement gộp Position với Order/ExecutionResult/Fill như authoritative fact — xác nhận Position LÀ deterministic/derived/rebuildable projection từ Fill history, `position-projection.owns_authoritative_state: false`, KHÔNG một authority owner nào; PAPER evidence wording, provenance chain wording sửa tương ứng. (c) `P15-A-MIN-01` — §3 sửa: sáu category persistence xác nhận LÀ một Package 1.5 architecture-level classification derive dưới I-12/Chapter 7/Chapter 8/package baseline, KHÔNG PHẢI taxonomy I-12 trực tiếp mandate, KHÔNG tạo module taxonomy/authority type/locked constitutional taxonomy mới. (d) `P15-A-MIN-02` — §6 sửa: `supersedes_fact_ref` xác nhận LÀ một ví dụ mechanism (account.md §11), KHÔNG một universal field Package 1.5 áp đặt — correction lineage PHẢI theo controlling Domain Contract của từng concept; §5 retention/deletion owner claim qualify lại thành "KHÔNG identify được trong các baseline ĐÃ review", KHÔNG một exhaustive-proof claim across toàn repository. Mọi nội dung khác của v0.1 GIỮ NGUYÊN.

## 0. Vai trò của tài liệu này — scope resolved từ controlling source (bắt buộc, yêu cầu task)

Scope resolve TRỰC TIẾP từ `phase-1-plan.md` (Approved, controlling), nguyên văn:

```text
Package ID:              1.5
Name:                     Database Architecture
Purpose:                  Storage/persistence architecture — event log store, projection/
                          read-model store, source-of-truth boundary per domain concept.
Inputs:                   Chapter 8 §8.1 (event log authoritative source, Locked), I-12
                          (Single Source of Truth), 1.1 (module registry), output của
                          1.3-A/B/C/D (Consolidated Stable).
Outputs:                  docs/architecture/database-architecture.md — store-per-concept
                          map, projection rebuild strategy, KHÔNG schema DDL cụ thể.
Explicit non-goals:       KHÔNG author database schema (DDL); KHÔNG chọn database
                          technology cụ thể (trừ khi ảnh hưởng authority boundary); KHÔNG
                          migration script.
Dependencies:              1.1, 1.3-A, 1.3-B, 1.3-C, 1.3-D.
```

**Đây là MỘT artifact duy nhất** (`docs/architecture/database-architecture.md`) elaborate kiến trúc kỹ thuật cho ĐÚNG MỘT module đã đăng ký assign cho Package 1.5 tại Package 1.1: `review-evidence-service` (`module-registry.yaml` v0.7, `phase.elaborated_by: "1.5"` — script-verified, MỘT VÀ CHỈ MỘT module mang assignment này). Package 1.5 KHÔNG author Package 1.6 (UX Architecture) — liệt kê như tương lai/consumer, KHÔNG elaborate content tại đây.

**KHÔNG thuộc phạm vi tài liệu này:** SQL/NoSQL/vendor choice; table/column/index design; migration tooling; ORM/framework; deployment/network topology; replication technology; backup product; concrete retention period (trừ khi đã controlled bởi Domain Contract/Chapter 8 §8.1.1); encryption product/key-management implementation; Package 1.6 UX behavior; LIVE activation; bất kỳ database schema (DDL) nào.

## 1. Governing authority

```text
Constitution (Chapter 0–14, Locked):              highest architectural authority, đặc
                                                    biệt I-12 (Single Source of Truth),
                                                    I-3 (No Repaint), I-6 (Fail-Safe by
                                                    Scope), I-11 (Secrets & Custody
                                                    Isolation)
Chapter 7 (Module Taxonomy, Locked):               §7.4 Projection constraint (KHÔNG BAO
                                                    GIỜ authoritative source; rebuild
                                                    determinism cần pin version/schema/
                                                    config); §7.5 module classification
                                                    authority = module-registry.yaml
Chapter 8 (Event Model, Locked):                   §8.1 event log authoritative source
                                                    (transport KHÔNG PHẢI authority);
                                                    §8.1.1 năm điều kiện Referenced
                                                    Authoritative Artifact (versioned,
                                                    immutable-after-reference, no
                                                    identifier reuse, persistently
                                                    resolvable với retention/archive
                                                    policy, verifiable content identity)
module-registry.yaml v0.7 (Consolidated
  Stable, 25 module):                              module identity/taxonomy/dependency
                                                    authority — KHÔNG redefine tại đây;
                                                    `review-evidence-service` ĐÃ đăng
                                                    ký, `phase.elaborated_by: "1.5"`
system-decomposition.md v0.7 (Consolidated
  Stable):                                         semantic parity với module-registry.yaml
                                                    v0.7 — KHÔNG redefine tại đây
security-custody-baseline.md v0.4 (Package
  1.2, Consolidated Stable):                       custody/signing trust boundary — Package
                                                    1.5 elaborate CHỈ persistence exclusion
                                                    treatment (§9 dưới), KHÔNG redefine
risk-execution-architecture.md v0.2 (Package
  1.3-D, Consolidated Stable):                     Risk Gateway/Execution Engine/Execution
                                                    Result Processor/Fill Processor/
                                                    Position Projection authority —
                                                    consumed như forward reference, KHÔNG
                                                    redefine
api-architecture.md v0.3 (Package 1.4,
  Consolidated Stable):                            command-query-api-surface exposure/
                                                    routing boundary — consumed như forward
                                                    reference cho §4/§7 dưới, KHÔNG redefine
Package 1.3-A/1.3-B/1.3-C (Consolidated
  Stable):                                         Data/Structure/Regime/Feature/Context/
                                                    Decision boundary — consumed như forward
                                                    reference, KHÔNG redefine
phase-1-plan.md v0.4 (Approved):                   Phase 1 work-breakdown/package-boundary
                                                    authority, nguồn CHÍNH của §0 scope
                                                    resolution
Package 1.5 (tài liệu này):                        technical elaboration authority ONLY,
                                                    cho review-evidence-service — persistence
                                                    authority model/store-per-concept map/
                                                    projection rebuild strategy
```

Package 1.5 KHÔNG redefine domain entity/event semantics, module identity/taxonomy, hay bất kỳ package đã Consolidated Stable nào — mọi nội dung dưới đây chỉ **elaborate** kiến trúc kỹ thuật trong ranh giới đã pin.

## 2. Module boundary — Review Evidence Service (module DUY NHẤT gán cho Package 1.5, registry parity, bắt buộc yêu cầu task)

### 2.1 Registry classification (bảo toàn nguyên vẹn, KHÔNG sửa registry)

```text
module_id:                 review-evidence-service
name:                      Review Evidence Service
module_type:               projection
owns_authoritative_state:  false
consumes:                  event
emits:                     query
depends_on:                decision-authority-service, risk-gateway, execution-engine,
                           execution-result-processor, fill-processor,
                           position-projection, replay-integration-service,
                           decision-evaluation-engine
forbidden_dependencies:    (none registered)
plugin_relation:           none
security_classification:   none
phase:                     { identified_in: "1.1", elaborated_by: "1.5" }
```

**Xác nhận tường minh (bắt buộc, yêu cầu task; sửa 2026-08-10, đóng `P15-BCC-MAJ-01`):** classification, `depends_on`, `emits`/`consumes`, VÀ `phase.elaborated_by: "1.5"` trên đây LÀ nguyên trạng từ `module-registry.yaml` v1.1 (Consolidated Stable) — Package 1.5 CHÍNH NÓ KHÔNG sửa/redefine bất kỳ field nào trong số này, KHÔNG tự thêm/bớt một dependency edge, capability, hay authority nào tại transaction này hay tại v0.2 gốc. Edge thứ tám (`decision-evaluation-engine`) ĐÃ được thêm SAU Package 1.5 v0.2's Consolidated Stable boundary (2026-08-05T16:45), bởi một transaction governed RIÊNG BIỆT — ADR-021 alignment (2026-08-07, VIEW-003 Decision replay-parity recomputation delegation, non-authoritative) — KHÔNG bởi Package 1.5. Registry `notes` (nguyên văn): "Cross-cutting read/evidence layer — no new authoritative fact, no recomputation (PR-030 no-recompute preserved)."

### 2.2 Authority status — non-authoritative projection, KHÔNG business authority

```text
Xác nhận tường minh (bắt buộc, v0.2 correction, đóng `P15-A-MAJ-02`): review-evidence-
  service.owns_authoritative_state: false — module KHÔNG sở hữu bất kỳ authoritative
  domain fact nào (Decision, Trade Intent, RiskEvaluation, Execution Intent, Order,
  ExecutionResult, Fill — tất cả thuộc authority của module registered elaborate riêng:
  decision-authority-service/risk-gateway/execution-engine/execution-result-processor/
  fill-processor, KHÔNG đổi bởi Package 1.5). Position KHÔNG thuộc danh sách authoritative
  fact này — `position-projection.owns_authoritative_state: false` (§5 dưới); Position
  LÀ deterministic, derived, rebuildable projection từ eligible visible-valid Fill
  history (Chapter 7 §7.4), KHÔNG một authoritative domain fact được module NÀO sở hữu.

implements_capabilities: [] / serves_contexts: [] (registry, KHÔNG đổi) — cùng nguyên
  tắc đã dùng cho command-query-api-surface (Package 1.4 §2.2): tránh silent invention
  một capability/domain-context identity cạnh tranh ngoài context-map.yaml.
```

## 3. Persistence authority model (bắt buộc, yêu cầu task)

Xác nhận tường minh (bắt buộc, v0.2 correction, đóng `P15-A-MIN-01`): sáu category
dưới đây LÀ một Package 1.5 architecture-level classification — KHÔNG PHẢI một taxonomy
được I-12 trực tiếp mandate nguyên văn. Classification này được DERIVE dưới I-12 Single
Source of Truth (Chapter 2, Locked, nguyên văn: "Mỗi concept và scope PHẢI có một
authoritative source được chỉ định rõ"), Chapter 7 §7.4 projection constraint (Locked),
Chapter 8 §8.1 event-log rule (Locked), VÀ các package baseline đã Consolidated Stable
(Package 1.1-1.4) — I-12 xác lập YÊU CẦU single-source-of-truth NHƯNG KHÔNG tự thân định
nghĩa đúng sáu category này. Classification này KHÔNG tạo một module taxonomy mới
(Chapter 7 §7.5 VẪN authority DUY NHẤT), KHÔNG tạo một authority type mới, VÀ KHÔNG tạo
một locked constitutional taxonomy nào — nó LÀ một tổ chức thuật ngữ ở mức Package 1.5
để elaborate persistence boundary, KHÔNG một Chapter mới.

```text
Sáu category persistence PHẢI phân biệt được ở mức architecture (theo derivation trên):

1. Authoritative domain fact:        durable append-only event log (Chapter 8 §8.1,
     Locked) — CHỈ module `owns_authoritative_state: true` được phép author (account-
     service, custody-signing-service [scoped], exchange-adapter [scoped, unelaborated],
     market-reference-service, market-data-ingestion, structure-engine, raw-regime-
     engine, feature-engine, strategy-engine, plugin-release-manager, decision-
     authority-service, risk-gateway, execution-engine, execution-result-processor,
     fill-processor — danh sách đầy đủ, §5 dưới).

2. Append-only event/record history:  bản thân event log — mọi authoritative fact ĐÃ
     publish KHÔNG BAO GIỜ sửa/xóa (I-3 No Repaint, Chapter 2, Locked) — correction PHẢI
     biểu diễn bằng event mới (`supersedes_fact_ref` pattern, vd. account.md §11), KHÔNG
     overwrite tại chỗ.

3. Designated projection:             derived representation, `owns_authoritative_state:
     false` (Chapter 7 §7.4, Locked) — PHẢI rebuild được từ authoritative source CÙNG
     VỚI projection implementation version/schema/config đã pin (Chapter 7 §7.4, nguyên
     văn) — position-projection, context-aggregator, review-evidence-service (module
     DUY NHẤT Package 1.5) đều thuộc category này.

4. Review/evidence record:            review-evidence-service's read/aggregation output
     — LÀ một projection (category 3), KHÔNG một category riêng biệt về authority, NHƯNG
     có elaboration riêng tại §4 dưới do vai trò cross-cutting evidence/correction-
     inspection của nó (UC-016–UC-018).

5. Index, cache, VÀ rebuildable
   materialization:                   bất kỳ structure tăng tốc truy vấn (index, cache,
     denormalized view) PHẢI rebuild được từ category 1/2 — KHÔNG BAO GIỜ trở thành
     nguồn quyết định khi khác biệt với authoritative source; staleness PHẢI fail-safe
     theo I-6, KHÔNG silently trả kết quả cũ như thể current.

6. Operational storage KHÔNG trở
   thành business authority:          storage phục vụ vận hành thuần túy (checkpoint
     position, health-check state, rebuild-progress marker, notification read-model đã
     cập nhật — Chapter 7 §7.4 "operational metadata event về chính nó") KHÔNG BAO GIỜ
     được dùng thay thế authoritative domain fact, dù công nghệ lưu trữ có mạnh tới đâu.
```

**Xác nhận tường minh bắt buộc:** storage technology (bất kể SQL/NoSQL/log-structured/vendor nào) KHÔNG BAO GIỜ tự thân tạo hay chuyển giao Domain authority — I-12 xác nhận tường minh "Prohibited: coi transport mechanism... tự động là source of truth — authority nằm ở durable append-only log, không phải công nghệ transport cụ thể," VÀ nguyên tắc tương đương áp dụng ĐỒNG NHẤT cho storage/persistence layer: đổi database engine, storage format, hay indexing strategy KHÔNG đổi module NÀO là authoritative source cho concept nào — authority resolve từ module-registry.yaml + Domain Contract, KHÔNG từ storage implementation.

## 4. Review Evidence Service boundary (elaboration, bắt buộc yêu cầu task)

```text
Xác nhận tường minh (bắt buộc, v0.2 correction, đóng `P15-A-MAJ-01`): registry fact
  (`review-evidence-service.consumes: [event]`, `emits: [query]`, §2.1) VÀ bảy
  dependency đã đăng ký PHẢI phân biệt theo contract category CHÍNH XÁC của TỪNG
  dependency, KHÔNG gộp chung thành "bảy nguồn event":
```

```text
Event-emitting dependency (emits: [event], năm module — nguồn event thật cho
  review-evidence-service's consumes: [event]):
  decision-authority-service, risk-gateway, execution-engine, execution-result-
  processor, fill-processor.

Query-emitting projection (emits: [query], hai module — KHÔNG PHẢI nguồn event):
  position-projection, replay-integration-service.

Registry KHÔNG invent tại đây: position-projection KHÔNG emit event (chỉ query,
  §2.1/registry); replay-integration-service KHÔNG emit event (chỉ query, registry);
  review-evidence-service KHÔNG consume query (chỉ event, §2.1 — KHÔNG field mới nào
  thêm); KHÔNG dependency edge hay contract category mới nào được thêm ngoài registry.

Contract-category interaction gap (ghi nhận tường minh, KHÔNG resolve tại đây):
  module-registry.yaml v0.7 xác lập ĐÚNG dependency relationship (`depends_on`) giữa
  review-evidence-service VÀ cả bảy module trên, NHƯNG KHÔNG tự đầy đủ xác lập CƠ CHẾ
  review-evidence-service dùng để lấy được output của HAI query-emitting dependency
  (position-projection, replay-integration-service) dưới khai báo `consumes: [event]`
  của chính nó — một dependency edge (§7.5 Chapter 7, prerequisite relation) KHÔNG tự
  động ngụ ý contract-category compatibility hoàn chỉnh giữa consumes/emits hai phía.
  Package 1.5 KHÔNG tự phát minh cơ chế đó (vd. một internal query-pull path, một
  event-projection-of-projection, hay một contract category mới) — ghi nhận NHƯ MỘT
  gap carry forward (§11), KHÔNG resolve.

**Cập nhật (2026-08-10, đóng `P15-BCC-MAJ-01`):** SAU Package 1.5 v0.2's Consolidated Stable boundary, `module-registry.yaml` v1.1 (ADR-021 alignment, 2026-08-07) thêm ĐÚNG MỘT dependency thứ tám — `decision-evaluation-engine` (`consumes: [event, query]`, `emits: [event]`, VIEW-003 Decision replay-parity recomputation delegation, non-authoritative) — xem §2.1 đã cập nhật. Package 1.5 KHÔNG tự tạo edge này (governed bởi ADR-021, riêng biệt). Đúng nguyên tắc gap carry-forward trên: cơ chế interaction CHÍNH XÁC (request representation, response/event correlation, synchronous-vs-asynchronous, timeout, failure code, transport) giữa review-evidence-service VÀ decision-evaluation-engine cho edge thứ tám này CŨNG KHÔNG được `depends_on` edge tự động xác lập — ghi nhận NHƯ một gap carry-forward BỔ SUNG (§11), CÙNG loại với gap hai query-emitting dependency trên, KHÔNG resolve tại correction này (đúng module-registry.yaml's own note: "interaction-mechanism gap remains EXPLICITLY unresolved"). Package 1.5's persistence authority model/store-per-concept map/projection rebuild strategy KHÔNG đổi — `decision-evaluation-engine` KHÔNG sở hữu persistence authority nào (§5 dưới, "NO (compute)"), nên KHÔNG một store/category mới nào cần thiết cho edge này.

Decision→Position lineage trace VẪN LÀ một desired evidence outcome (registry
  responsibilities, UC-016–UC-018) — NHƯNG tài liệu này KHÔNG claim rằng registry hiện
  tại, TỰ THÂN, đã chứng minh một complete bảy-nguồn event-consumption path cho outcome
  đó; phần path đi qua hai query-emitting dependency VẪN CHƯA fully established (gap
  trên).

Provenance, correlation, VÀ source-reference preservation: mọi evidence record review-
  evidence-service expose PHẢI giữ nguyên tham chiếu tới authoritative event gốc (event
  identity, `supersedes_fact_ref` correction lineage nếu có, VÀ correlation/causation_
  refs chain đã pin tại module nguồn — vd. Decision→RiskEvaluation→Execution Intent→
  Order→ExecutionResult→Fill (authoritative fact) →Position (derived, non-authoritative
  projection — §2.2/§5, KHÔNG cùng loại authority với năm fact trước), Package 1.3-C/
  1.3-D) — review-evidence-service
  KHÔNG được strip provenance, KHÔNG collapse nhiều fact riêng biệt thành một entry mất
  khả năng truy vết ngược.

Non-authoritative status (đã established, KHÔNG đổi): `owns_authoritative_state: false`
  (§2.1/§2.2) — review-evidence-service's output LÀ derived read-surface, KHÔNG PHẢI
  domain fact mới; PR-030 no-recompute (registry notes) xác nhận nó KHÔNG tái tính toán
  một giá trị "tương đương" thay vì forward kết quả đã tồn tại tại nguồn authoritative.

Không có khả năng rewrite hay replace authoritative source record: I-3 No Repaint
  (Chapter 2, Locked) áp dụng ĐỒNG NHẤT — review-evidence-service KHÔNG BAO GIỜ sửa,
  xóa, hay thay thế event gốc tại decision-authority-service/risk-gateway/execution-
  engine/execution-result-processor/fill-processor/position-projection; nó CHỈ đọc VÀ
  re-present, tuyệt đối KHÔNG một write path ngược lại bất kỳ module nguồn nào (registry
  `depends_on` xác nhận review-evidence-service KHÔNG emit command/event, CHỈ query).

Quan hệ với API exposure VÀ future UX consumption: `command-query-api-surface.depends_on`
  (Package 1.4 v0.3, Consolidated Stable) ĐÃ có edge tới review-evidence-service (registry
  fact preserved, KHÔNG đổi) — API Surface CÓ THỂ route/expose query tới review-evidence-
  service theo đúng nguyên tắc đã pin tại api-architecture.md §4 (query boundary: KHÔNG
  recompute, projection non-authoritative marker giữ nguyên, cursor/version/freshness
  preserved). `ux-application-shell` (Package 1.6, CHƯA elaborate) LÀ future consumer
  gián tiếp qua API Surface — Package 1.5 KHÔNG author UX behavior/API schema tại đây.

Failure behavior khi required evidence missing/stale/incomplete/unverifiable: cùng
  nguyên tắc I-6 Fail-Safe by Scope (Chapter 2, Locked) áp dụng cho projection consumer
  (Chapter 7 §7.4 criticality clause, nguyên văn: "khi tính đúng đắn hoặc độ freshness
  của nó không xác định, consumer PHẢI fail-safe") — review-evidence-service PHẢI fail
  closed/trả về explicit "evidence unavailable/stale/incomplete" marker, KHÔNG BAO GIỜ
  present một trace record KHÔNG đầy đủ như thể complete, KHÔNG silently drop một đoạn
  lineage bị thiếu mà không đánh dấu.
```

**Xác nhận tường minh:** KHÔNG UX behavior (component/state/screen) hay API schema (field-level request/response) nào được author tại §4 — mọi mục trên là YÊU CẦU architecture-level (WHAT phải đúng), KHÔNG implementation.

## 5. Data classification và ownership matrix (bắt buộc, yêu cầu task — CHỈ fact đã established, KHÔNG assign owner mới)

**Nguyên tắc bắt buộc:** ma trận dưới đây transcribe TRỰC TIẾP từ `module-registry.yaml` v0.7 (Consolidated Stable) — KHÔNG invent authority/persistence purpose nào ngoài field đã đăng ký (`owns_authoritative_state`, `module_type`, `security_classification`). Retention/deletion decision owner KHÔNG established cho BẤT KỲ domain concept nào tại transaction này — ghi nhận NHƯ MỘT gap chung (§11), KHÔNG tự ý assign một owner mới cho bất kỳ concept nào.

```text
Source module                | Authoritative? | Persistence purpose (I-12 category, §3)     | Append/correction/rebuild treatment           | Security sensitivity
------------------------------|-----------------|----------------------------------------------|------------------------------------------------|----------------------
market-reference-service      | YES             | Category 1 — Instrument/Venue identity fact   | Append-only; correction via new event           | none
market-data-ingestion         | YES             | Category 1 — Candle fact                      | Append-only; candle-corrected = correction event| trust_boundary_candidate
structure-engine              | YES             | Category 1 — Structure fact                   | Append-only                                     | none
raw-regime-engine             | YES             | Category 1 — Raw Regime fact                  | Append-only                                     | none
feature-engine                | YES             | Category 1 — Feature fact                     | Append-only                                     | none
context-aggregator            | NO (projection) | Category 3 — MarketContextSnapshot            | Rebuildable từ event log, pinned version/config | none
account-service                | YES             | Category 1 — Account identity/boundary/env    | Append-only; AccountFactInvalidated = correction| custody_adjacent
custody-signing-service        | YES (scoped)    | Category 1 — credential-binding/signing state | Append-only; KHÔNG BAO GIỜ raw secret persisted | secret_consuming (§9)
exchange-adapter                | YES (scoped)    | Category 1 — raw venue-interaction evidence   | Append-only (functionally unelaborated, §11)    | trust_boundary_candidate
strategy-engine                | YES             | Category 1 — Strategy identity fact           | Append-only                                     | none
plugin-release-manager         | YES             | Category 1 — Plugin Version operational fact  | Append-only                                     | none
strategy-plugin-host           | NO (compute)    | KHÔNG persistence authority — ephemeral compute output feeding decision-evaluation-engine | N/A | none
decision-evaluation-engine     | NO (compute)    | KHÔNG persistence authority — non-authoritative proposal | N/A                            | none
decision-authority-service      | YES             | Category 1 — Decision/Trade Intent fact       | Append-only, immutable                          | none
risk-gateway                    | YES             | Category 1 — RiskEvaluation/Execution Intent  | Append-only                                     | trust_boundary_candidate
execution-engine                | YES             | Category 1 — Order/OrderSubmissionRequest     | Append-only, immutable Order identity           | trust_boundary_candidate
execution-result-processor      | YES             | Category 1 — ExecutionResult fact             | Append-only                                     | none
fill-processor                  | YES             | Category 1 — Fill fact                        | Append-only, immutable                          | none
position-projection             | NO (projection) | Category 3 — Position read-model              | Rebuildable từ Fill history, pinned version      | none
replay-integration-service       | NO (projection) | Category 5-adjacent — canonical Replay Cursor (Chapter 8 §8.5) | Cursor identity, KHÔNG domain fact riêng | none
backtest-orchestrator            | DEFERRED        | Category 1 candidate — Backtest run identity (DD-001, CHƯA resolve) | CHƯA established | none
paper-execution-boundary        | NO              | Boundary/simulation, KHÔNG domain fact riêng   | N/A                                             | none
command-query-api-surface       | NO              | KHÔNG persistence — routing/exposure CHỈ       | N/A                                             | trust_boundary_candidate
review-evidence-service          | NO (projection) | Category 3/4 — evidence/trace aggregation (§4)| Rebuildable từ event log, pinned version/config | none
ux-application-shell             | NO              | KHÔNG persistence — Package 1.6, CHƯA elaborate| N/A                                             | none
```

**Retention/deletion decision owner (v0.2 correction, đóng `P15-A-MIN-02`.B — qualified, KHÔNG exhaustive claim):** Package 1.5 KHÔNG identify được một retention/deletion policy decision owner đã established trong CÁC controlling baseline đã review cho transaction này (`module-registry.yaml` v0.7, `system-decomposition.md` v0.7, Package 1.2/1.3-A..D/1.4 — KHÔNG PHẢI một claim đã kiểm tra exhaustive MỌI artifact trong toàn bộ repository, trừ khi việc kiểm tra đó thực sự được thực hiện, điều CHƯA xảy ra tại đây). Chapter 8 §8.1.1 mục 4 yêu cầu "phải có explicit retention/archive policy" khi hết replay/audit horizon, NHƯNG TỰ THÂN KHÔNG chỉ định AI quyết định policy đó. Đây VẪN LÀ một preserved gap pending broader confirmation (§11) — Package 1.5 KHÔNG tự assign hay resolve owner này.

## 6. Append, correction, và no-repaint semantics (bắt buộc, yêu cầu task — KHÔNG table/schema cụ thể)

```text
Immutable identity: mọi authoritative fact (event, Decision, Order, Fill, v.v.) mang
  identity bất biến xuyên suốt lifecycle của nó (cùng nguyên tắc account.md §1, order.md,
  fill.md — KHÔNG đổi tại đây) — Package 1.5 KHÔNG author một identity scheme mới, CHỈ
  xác nhận persistence layer PHẢI bảo toàn identity đó nguyên vẹn.

Effective-time VÀ recorded-time distinction (nơi upstream contract yêu cầu): account.md
  §12 VÀ Chapter 5 (Time Model, Locked) đã pin phân biệt effective_time/recorded_time —
  persistence layer PHẢI lưu VÀ resolve được CẢ HAI trục độc lập cho historical replay,
  KHÔNG hợp nhất thành một timestamp duy nhất.

Append-only correction lineage (v0.2 correction, đóng `P15-A-MIN-02`.A): authoritative
  correction PHẢI append-only — MỘT fact MỚI trỏ predecessor, KHÔNG BAO GIỜ sửa fact cũ
  tại chỗ. Cơ chế correction lineage CỤ THỂ (field name, reference structure) PHẢI theo
  ĐÚNG controlling Domain Contract của concept đó — `supersedes_fact_ref` (account.md
  §11) LÀ MỘT ví dụ đã dùng bởi contract cụ thể đó (account.md), KHÔNG PHẢI một field
  universal mà Package 1.5 áp đặt lên mọi Domain Contract; contract khác CÓ THỂ dùng
  mechanism khác miễn thỏa append-only. Package 1.5 KHÔNG author một universal correction
  schema mới tại đây. Persistence layer PHẢI hỗ trợ resolve "visible-valid-head per
  slice" (account.md §7 pattern) tại bất kỳ cursor nào theo ĐÚNG mechanism controlling
  contract quy định, KHÔNG latest-state duy nhất.

KHÔNG silent overwrite hay historical rewriting: I-3 No Repaint (Chapter 2, Locked) —
  "một output đã publish KHÔNG được sửa hoặc xóa" — persistence layer KHÔNG author một
  cơ chế UPDATE-in-place nào cho authoritative fact, dưới bất kỳ hình thức nào.

KHÔNG mutable-latest substitution: cùng nguyên tắc `AccountCurrentView` KHÔNG BAO GIỜ
  authoritative (account.md §7/§13, đã pin tại Package 1.4 §8 — KHÔNG đổi) — persistence
  layer KHÔNG present một "current state" view như thể thay thế authoritative append-only
  source; mọi read PHẢI resolve đúng cursor đã yêu cầu.

Projection rebuildable từ eligible authoritative input (nơi đã established): Chapter 7
  §7.4 rebuild determinism — projection (context-aggregator, position-projection, review-
  evidence-service, replay-integration-service) PHẢI rebuild được từ authoritative source
  CÙNG VỚI projection implementation version/schema/config đã pin — KHÔNG rebuild "tương
  đương" mà kết quả khác biệt do version trôi.
```

**Xác nhận tường minh:** KHÔNG table, column, hay schema DDL cụ thể nào được author tại §6 — mọi mục trên là YÊU CẦU architecture-level thừa kế TRỰC TIẾP từ Domain Contract/Chapter đã Locked, KHÔNG concrete storage design.

## 7. Transaction và consistency boundaries (bắt buộc, yêu cầu task — KHÔNG chọn distributed transaction protocol/event store/ORM/database engine)

```text
Atomicity trong một authoritative write boundary: mỗi module `owns_authoritative_state:
  true` PHẢI đảm bảo write của chính nó (một fact hay một correction lineage entry) LÀ
  atomic trong phạm vi boundary của module đó — Package 1.5 KHÔNG author cơ chế cụ thể
  (database transaction, WAL, hay tương đương), CHỈ pin YÊU CẦU atomicity phải tồn tại.

Idempotency preservation: cùng nguyên tắc I-10 đã established xuyên suốt (SigningRequest,
  Package 1.2 §4a.6; execution attempt, Package 1.3-D) — persistence layer PHẢI bảo toàn
  đúng logical identity xuyên retry, KHÔNG tạo effect thứ hai độc lập cho cùng logical
  request — Package 1.5 KHÔNG tự phát minh idempotency scheme mới, CHỈ preserve đã pin
  tại module authoritative.

Ordering/cursor evidence: mọi read (đặc biệt qua projection/review-evidence-service)
  PHẢI bảo toàn cursor/ordering evidence từ authoritative source (Chapter 8 §8.5 Replay
  Cursor, replay-integration-service) — persistence layer KHÔNG strip ordering info khi
  lưu/truy vấn.

Causal VÀ correlation preservation: causation_refs chain (Decision→Risk→Execution,
  Package 1.3-D §3/§10) VÀ correlation identity (SigningRequest↔SigningAttempt, Package
  1.2 §4a.6) PHẢI bảo toàn nguyên vẹn qua persistence layer — KHÔNG lossy storage nào
  được phép làm mất khả năng trace lineage.

Cross-module write PHẢI tránh distributed authority: MỖI domain concept có ĐÚNG MỘT
  authoritative module (I-12) — persistence layer KHÔNG author một cơ chế cho phép hai
  module cùng ghi vào cùng một authoritative fact/scope; nếu một effect chạm nhiều module
  (vd. RiskEvaluation → Execution Intent → Order), MỖI module VẪN ghi authoritative fact
  của riêng nó, KHÔNG một shared/distributed write nào.

Eventual projection update KHÔNG được trình bày như authoritative completion: khi
  projection (position-projection, context-aggregator, review-evidence-service) chưa
  kịp cập nhật sau một authoritative event mới, hệ thống PHẢI KHÔNG present projection
  đó như thể đã hoàn tất/current — projection lag PHẢI observable, KHÔNG ẩn giấu (§10
  dưới).

Unknown hay partially-committed outcome PHẢI fail an toàn: cùng nguyên tắc UNKNOWN_
  OUTCOME đã pin (Package 1.2 §4a.5/§4a.9: "local certainty KHÔNG đủ... PHẢI KHÔNG được
  coi là thành công mà không qua reconciliation") — persistence layer KHÔNG tự diễn giải
  một write chưa xác nhận thành công/thất bại; PHẢI đòi hỏi reconciliation đúng nguyên
  tắc đã pin tại module authoritative liên quan.
```

## 8. Query, replay, và audit support (bắt buộc, yêu cầu task — KHÔNG conflate replay/backtest/PAPER với LIVE)

```text
Deterministic replay: `replay-integration-service` (Chapter 8 §8.5, canonical Replay
  Cursor authority, Package 1.3-A, Consolidated Stable) LÀ nguồn cursor authority DUY
  NHẤT — persistence layer PHẢI hỗ trợ resolve TOÀN BỘ authoritative fact tại một cursor
  cho trước, deterministic, KHÔNG phụ thuộc thời điểm truy vấn thực tế (I-3 No Repaint).

Backtest evidence: `backtest-orchestrator` (`owns_authoritative_state: deferred`, DD-001
  CHƯA resolve, Package 1.1 §11) — Backtest run identity/evidence VẪN CHƯA có persistence
  authority established; Package 1.5 KHÔNG resolve DD-001 tại đây, CHỈ ghi nhận gap carry
  forward (§11).

PAPER evidence (v0.2 correction, đóng `P15-A-MAJ-02`): `paper-execution-boundary`
  (Package 1.3-D, Consolidated Stable) — PAPER execution path's authoritative evidence
  (Order/ExecutionResult/Fill) LÀ authoritative fact của đúng module sở hữu (execution-
  engine/execution-result-processor/fill-processor tương ứng) dưới `environment: PAPER`.
  Position, KHÁC với ba fact trên, KHÔNG PHẢI authoritative fact — `position-projection`
  KHÔNG sở hữu authoritative state (§2.2/§5); Position evidence trong PAPER context LÀ
  deterministic, rebuildable projection từ eligible visible-valid Fill history, CÓ THỂ
  expose như projection evidence NHƯNG KHÔNG BAO GIỜ được present như một authoritative
  domain fact. Persistence layer KHÔNG author cơ chế isolation mới ngoài `environment`
  field bất biến đã pin (ADR-012 §2.4, account.md §8); persistence của Position
  projection output KHÔNG chuyển giao authority từ Fill history sang chính projection đó.

Correction-aware historical query: mọi query lịch sử (qua review-evidence-service hay
  bất kỳ projection nào) PHẢI resolve đúng "visible-valid-head per slice" TẠI cursor yêu
  cầu (account.md §7 pattern, áp dụng tương đương cho mọi Domain Contract dùng
  correction lineage) — KHÔNG latest-state ngầm định thay thế.

Audit VÀ review traceability: I-1 Explainability (Chapter 2, Locked) — review-evidence-
  service (§4) LÀ read-surface CHÍNH cho Decision→Position lineage trace/correction
  inspection (UC-016–UC-018); audit trail requirement khác (custody/signing, Package
  1.2 §4a.11; account-service, §12) VẪN thuộc authority của module gốc, KHÔNG được
  Package 1.5 redefine — persistence layer CHỈ đảm bảo audit evidence đó persistently
  resolvable trong replay/audit horizon (Chapter 8 §8.1.1 mục 4).

Environment VÀ Account Boundary separation: `environment` (PAPER|LIVE, bất biến,
  account.md §8) VÀ `account_boundary_ref` (ADR-012 §2.1, exactly-one-boundary) LÀ
  cấu trúc identity-level ĐÃ đảm bảo tách biệt (Package 1.2 §8, Package 1.3-D §9.3
  Position key bao gồm `environment`) — Package 1.5 KHÔNG cần thêm cơ chế runtime
  isolation mới cho phần identity, CHỈ xác nhận persistence layer bảo toàn field đó
  nguyên vẹn qua mọi store/projection/rebuild.
```

**Xác nhận tường minh:** replay/backtest/PAPER evidence KHÔNG BAO GIỜ được conflate với LIVE — `environment: LIVE` VẪN Unauthorized (§9 dưới); KHÔNG venue/execution/custody LIVE path thật nào được persistence layer giả định hay chuẩn bị trước tại transaction này.

## 9. Security và custody constraints (I-11, bắt buộc, yêu cầu task — bảo toàn Package 1.2 boundary)

```text
KHÔNG raw exchange credential hay signing material trong general-purpose persistence:
  custody-signing-service (Package 1.2 §4a.2, Consolidated Stable) LÀ module DUY NHẤT
  được phép dùng exchange credential trực tiếp — mọi general-purpose store/index/cache
  mà Package 1.5 elaborate (§3 category 3/5/6) TUYỆT ĐỐI KHÔNG chứa raw secret, private
  key, seed phrase, hay signing material dưới bất kỳ hình thức nào (payload/snapshot/
  log/replay artifact/audit record — cùng exclusion list đã pin tại Package 1.2 §4a.11/
  §12b, KHÔNG đổi).

Custody secret VẪN confined trong custody boundary: credential-binding/signing
  operational fact (§5, custody-signing-service row) LÀ category 1 authoritative fact
  của riêng module đó — Package 1.5 KHÔNG author một persistence path song song hay
  thay thế cho custody-signing-service's own storage boundary.

Sensitive evidence exposure tuân least privilege: review-evidence-service (§4) VÀ mọi
  projection khác PHẢI tôn trọng `security_classification` đã đăng ký của module nguồn
  (vd. `trust_boundary_candidate` cho market-data-ingestion/risk-gateway/execution-
  engine/exchange-adapter/command-query-api-surface, `secret_consuming` cho custody-
  signing-service, `custody_adjacent` cho account-service) — evidence expose KHÔNG được
  rộng hơn phạm vi mà module nguồn đã cho phép.

Storage KHÔNG tạo route trực tiếp tới custody/signing: cùng nguyên tắc absence-of-edge
  đã pin tại Package 1.4 §6 (v0.2/v0.3 correction) — review-evidence-service's `depends_
  on` (§2.1) KHÔNG chứa custody-signing-service/exchange-adapter; persistence layer nói
  chung (index/cache/projection store) KHÔNG được thiết kế tạo một access path mới tới
  custody boundary ngoài route đã đăng ký tại module-registry.yaml.

LIVE VẪN Unauthorized: Package 1.5 KHÔNG authorize LIVE execution dưới bất kỳ hình thức
  nào — KHÔNG persistence path mới nào giả định hay chuẩn bị cho venue-submission LIVE
  path (ADR-017 §9a Stage 2, KHÔNG active).
```

## 10. Failure và recovery semantics (bắt buộc, yêu cầu task — KHÔNG concrete error code/recovery mechanism)

Tám category PHẢI phân biệt được ở mức architecture (KHÔNG concrete implementation):

```text
Write rejection:                request KHÔNG đạt validation TRƯỚC KHI persist (vd.
                                 missing required identity, malformed correlation) —
                                 KHÔNG một authoritative fact nào được tạo.
Duplicate/idempotent replay:    cùng logical request đến lần thứ hai — PHẢI reconcile
                                 với write hiện có (I-10), KHÔNG tạo effect độc lập thứ
                                 hai (§7 trên).
Stale hay invalidated input:    input mang cursor/version đã KHÔNG còn hiệu lực tại
                                 thời điểm write — PHẢI fail closed (I-6), KHÔNG silently
                                 chấp nhận với dữ liệu cũ.
Partial hay unknown persistence
  outcome:                       write KHÔNG xác nhận rõ thành công/thất bại (vd. mất
                                 kết nối giữa chừng) — PHẢI ĐÒI HỎI reconciliation (§7),
                                 KHÔNG tự diễn giải thành success.
Projection lag:                 projection (position-projection/context-aggregator/
                                 review-evidence-service) chưa kịp cập nhật sau
                                 authoritative event mới — PHẢI observable/reportable,
                                 KHÔNG ẩn giấu như thể current (§7).
Missing evidence:                một đoạn lineage/trace mà review-evidence-service cần
                                 KHÔNG resolve được từ nguồn authoritative — PHẢI trả về
                                 explicit "evidence unavailable" marker (§4), KHÔNG bỏ
                                 qua âm thầm.
Corrupted hay unverifiable
  evidence:                       dữ liệu resolve được NHƯNG KHÔNG pass integrity/
                                 verifiability check (Chapter 8 §8.1.1 mục 5, verifiable
                                 content identity) — PHẢI fail closed, KHÔNG present như
                                 valid.
Authoritative source unavailable: module sở hữu authoritative fact KHÔNG resolve được
                                 tại thời điểm cần (network/store outage) — mọi projection/
                                 consumer phụ thuộc PHẢI fail-safe theo I-6, KHÔNG suy
                                 diễn giá trị thay thế.
```

**Xác nhận tường minh:** KHÔNG error code, exception taxonomy, hay concrete recovery mechanism (retry policy, circuit breaker implementation, backup/restore procedure) nào được author tại §10 — mọi mục trên là phân loại architecture-level BẮT BUỘC PHẢI phân biệt được.

## 11. Preserved gaps and non-goals (bắt buộc, yêu cầu task)

**Carry forward nguyên vẹn từ upstream (KHÔNG resolve tại Package 1.5):**

```text
Kill-switch authoritative-state ownership — VẪN unresolved (Package 1.3-D §16, Package
  1.2 §14 gap #5, Package 1.4 §10) — Package 1.5 KHÔNG claim owner nào.
In-flight signing/revocation behavior — VẪN unresolved (Package 1.2 §4a.9) — Package
  1.5 KHÔNG chạm (KHÔNG edge tới custody-signing-service, §9).
In-flight execution cancellation/reconciliation semantics — VẪN unresolved (Package
  1.3-D §16) — carry forward nguyên vẹn.
LIVE Domain Contract (Execution Engine ↔ Exchange Adapter) — VẪN CHƯA author (Package
  1.3-D §16, Package 1.2 §14 gap #2) — ngoài phạm vi hoàn toàn Package 1.5.
DD-003 (PAPER-context authoritative Decision establishment mechanism) — VẪN Deferred —
  Package 1.5 KHÔNG resolve.
DD-001 (Backtest Domain Contract/entity/event/schema, backtest-orchestrator's
  owns_authoritative_state: deferred) — VẪN Deferred (Package 1.1 §11) — Package 1.5
  KHÔNG resolve.
Exchange Adapter elaborating package assignment — VẪN unresolved (Package 1.1 §11) —
  ngoài phạm vi Package 1.5.
Retention/deletion decision owner — KHÔNG established cho bất kỳ domain concept nào
  (§5 trên) — gap MỚI ghi nhận tại Package 1.5, KHÔNG tự assign owner.
```

**Non-goals riêng của Package 1.5 (KHÔNG author tại transaction này):**

```text
SQL/NoSQL/vendor choice (PostgreSQL/EventStoreDB/Kafka/Cassandra/v.v.).
Table, column, hay index design (database schema/DDL).
Migration tooling/framework.
ORM/framework choice.
Deployment/network topology, cloud provider, service mesh.
Replication technology cụ thể.
Backup product/mechanism cụ thể.
Concrete retention period (trừ khi đã controlled bởi Domain Contract/Chapter 8
  §8.1.1 — retention/archive policy nguyên tắc CHUNG đã pin, KHÔNG con số cụ thể).
Encryption product hay key-management implementation.
Package 1.6 UX behavior/component.
Bất kỳ dependency edge mới nào ngoài `module-registry.yaml` v0.7 đã đăng ký.
Bất kỳ registry change nào (`module-registry.yaml`/`system-decomposition.md` KHÔNG sửa).
LIVE activation dưới bất kỳ hình thức nào.
KHÔNG tạo/approve ADR tại transaction này (§1 ADR dependency — database source-of-truth
  boundary MỚI, nếu concept nào chưa có authoritative source resolve được, LIKELY
  REQUIRED cho một future transaction, KHÔNG tại đây — §5's ownership matrix xác nhận
  MỌI domain concept ĐÃ có authoritative source resolve được từ module-registry.yaml,
  nên KHÔNG ADR gate nào bị kích hoạt tại v0.1 này).
KHÔNG mark Package 1.5 Consolidated Stable.
KHÔNG author Package 1.6 content.
KHÔNG tuyên bố Phase 1 hoàn thành, KHÔNG mở Phase 2, KHÔNG authorize Live.
```

## 12. Review and consolidation conditions

```text
Review A scope:               KHÔNG projection nào được coi authoritative thay
                               authoritative source (Chapter 7 §7.4, §3/§5 trên); rebuild
                               determinism (Chapter 7 §7.4) thiết kế đúng (§6); module
                               boundary (§2) nhất quán với module-registry.yaml v0.7
                               (Consolidated Stable) — KHÔNG dependency edge mới nào bị
                               invent; §5 ownership matrix transcribe đúng registry field,
                               KHÔNG assign owner mới cho retention/deletion; §9 xác nhận
                               đúng absence của edge tới custody-signing-service/
                               exchange-adapter; mọi gap (§11) carry forward trung thực,
                               KHÔNG silently resolved.
Independent Review B
  scope:                      Độc lập xác nhận MỌI domain concept có ĐÚNG MỘT
                               authoritative store resolve được — KHÔNG ambiguous/
                               competing store (đúng phase-1-plan.md Independent Review
                               B scope cho Package 1.5); xác nhận review-evidence-service
                               KHÔNG replace/rewrite authoritative source record (§4);
                               xác nhận KHÔNG custody/signing bypass nào qua persistence
                               layer (§9); xác nhận PAPER/LIVE separation VÀ LIVE
                               Unauthorized KHÔNG bị đổi (§8).
Product Owner decision
  point:                      Sau Review A/B CLEAN.
Consolidation condition:      Zero unresolved Blocker/Major trên baseline hiện tại
                               (v0.2, post bounded correction đóng P15-A-MAJ-01/
                               P15-A-MAJ-02/P15-A-MIN-01/P15-A-MIN-02); ADR source-of-
                               truth-boundary (nếu có domain concept nào lộ ra CHƯA có
                               authoritative source resolve được — §5 hiện xác nhận
                               KHÔNG mục nào như vậy) Approved (đúng phase-1-plan.md
                               Consolidation condition cho Package 1.5).
```

**Cập nhật (2026-08-05T16:45:00+07:00, Product Owner consolidation decision) — Package 1.5 v0.2 nay `Consolidated Stable`:** review evidence hoàn tất theo đúng trình tự — Review A (REVISE trên v0.1, đóng `P15-A-MAJ-01`/`P15-A-MAJ-02`/`P15-A-MIN-01`/`P15-A-MIN-02` qua v0.2) → bounded verification (CLEAN, Blocker 0/Major 0/Minor 0) → Independent Review B (CLEAN, Blocker 0/Major 0/Minor 0, consolidation readiness: READY) → Product Owner consolidation decision (nguyên văn ở banner đầu tài liệu). `package lifecycle: candidate → Consolidated Stable` — mechanical transaction, KHÔNG architecture content nào đổi. `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi. Cả hai preserved gap VẪN unresolved, KHÔNG resolve tại transaction này: contract-category interaction gap cho position-projection/replay-integration-service (§4/§11); retention/deletion policy ownership gap (§5/§11). Mọi gap khác tại §11 (kill-switch state ownership, in-flight signing/execution behavior, LIVE Domain Contract, DD-003, DD-001, exchange-adapter assignment) VẪN carry forward nguyên vẹn — Consolidated Stable KHÔNG resolve/narrow gap nào trong số đó, KHÔNG author một contract mechanism cho hai query-emitting projection, KHÔNG assign retention/deletion owner, KHÔNG author Package 1.6, KHÔNG mở Gate 2/Phase 2, KHÔNG authorize LIVE.

## 13. Lifecycle treatment

```text
Package 1.5:
  version: 0.2
  status: Draft
  package lifecycle/readiness: Consolidated Stable (2026-08-05T16:45:00+07:00, Product
    Owner decision)
  Review A: REVISE trên v0.1 — P15-A-MAJ-01/P15-A-MAJ-02/P15-A-MIN-01/P15-A-MIN-02
    CLOSED (v0.2)
  Bounded verification: CLEAN (Blocker 0/Major 0/Minor 0)
  Independent Review B: CLEAN (Blocker 0/Major 0/Minor 0), consolidation readiness:
    READY
  Product Owner consolidation decision: RECORDED (banner đầu tài liệu)

Package 1.5 v0.1 LÀ candidate đầu tiên — v0.2 LÀ bounded correction đóng bốn Review A
  finding trên v0.1 (banner đầu tài liệu), KHÔNG invalidate phần v0.1 KHÔNG bị finding
  chạm tới, KHÔNG redesign/mở rộng scope; v0.2 sau đó đạt `Consolidated Stable` qua
  transaction consolidation riêng biệt (banner đầu tài liệu) — KHÔNG version bump nào
  kèm theo mechanical lifecycle transaction này.

`Consolidated Stable` LÀ package lifecycle/readiness state (Chapter 0 §7.1) — KHÔNG có
  nghĩa artifact `Approved`/`Locked`; `status: Draft`, `approved_by: null`,
  `approved_at: null` KHÔNG đổi. Contract-category interaction gap (§4/§11) VÀ
  retention/deletion policy ownership gap (§5/§11) VẪN unresolved — Consolidated Stable
  KHÔNG resolve gap nào trong số đó, KHÔNG author một contract mechanism mới, KHÔNG
  assign owner mới, KHÔNG author Package 1.6, KHÔNG mở Gate 2/Phase 2, KHÔNG authorize
  LIVE.
```
