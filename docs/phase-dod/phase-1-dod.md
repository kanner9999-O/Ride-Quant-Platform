---
id: phase-1-dod
title: "Phase 1 — System Architecture Definition of Done"
version: "0.1"
status: Approved
owner: Product Owner
reviewers: []
approved_by: Product Owner
approved_at: "2026-08-07"
created_at: "2026-08-07"
last_review: null
next_review: null
depends_on: ["00-governance", "11-adr-process", "12-approval-gates", "13-quality-gates", "14-roadmap"]
---

# Phase 1 — System Architecture: Definition of Done (DoD)

**ACCEPTED VÀ INCORPORATED (2026-08-07, Product Owner decision) — status: Approved.** `phase-1-dod.md` v0.1 LÀ **candidate DoD artifact đầu tiên** cho Phase 1, author bởi transaction `Phase 1 DoD Candidate Author` — nay ĐÃ được Product Owner accept VÀ incorporate làm authoritative Phase 1 DoD, qua transaction mechanical `Phase 1 DoD v0.1 Acceptance + Canonical Incorporation Executor` (2026-08-07). Review evidence trước acceptance: Review A `CLEAN`, Independent Review B `CLEAN`, Blocker 0/Major 0/Minor 0. Xem §12 "Acceptance status" phía dưới cho incorporation record đầy đủ theo bốn điều kiện [Chapter 14 §14.3.1](../constitution/14-roadmap.md). **Lifecycle:** `version: "0.1"` UNCHANGED (mechanical acceptance/incorporation transaction, KHÔNG substantive content change), `status: Draft → Approved`, `approved_by: Product Owner`, `approved_at: "2026-08-07"`. `Approved` — KHÔNG `Locked` — LÀ package/document lifecycle state (Chapter 12 §12.2 điểm 5 công nhận `Approved` một mình đã authoritative cho mục đích Chapter 12/13 sử dụng, KHÔNG bắt buộc `Locked` bổ sung). **Transaction acceptance/incorporation này KHÔNG:** sửa §§1–11 substantive DoD criteria; chạy full-scope Backward Consistency Check; sinh Quality Gate PASS evidence; thực hiện Phase-level Gate review; approve Phase 1; mở Gate 2; mở Phase 2; authorize implementation/LIVE; sửa `phase-1-plan.md`, Constitution chapter, ADR, package architecture artifact, Domain Contract, hay Product artifact nào.

**Vai trò của tài liệu này:** đây LÀ **DoD artifact** mà [Chapter 12 §12.1](../constitution/12-approval-gates.md) (Locked, v1.5) khóa rule ("mỗi Phase phải có DoD cụ thể, viết ra và Product Owner chấp nhận TRƯỚC KHI phase/gate mở"), VÀ [Chapter 14 §14.3](../constitution/14-roadmap.md) (Locked, v1.6) khóa cardinality/nơi ở ("mỗi Phase phải resolve được đúng một authoritative DoD artifact"). Tài liệu này **định nghĩa tiêu chí** cho Phase 1 — nó **KHÔNG** phải bằng chứng "đã đạt tiêu chí", VÀ nó **KHÔNG** tự nó là Product Owner acceptance. `Approved`/`Phase 1 Approved` LÀ outcome của Phase 1 Approval Gate ([Chapter 12 §12.1](../constitution/12-approval-gates.md)) — **KHÔNG** phải một mục trong DoD này, VÀ mục này **KHÔNG chứa** chính outcome đó (tránh vòng lặp định nghĩa Chapter 12 đã cấm tường minh).

**Nguồn gốc:** tài liệu này chuyển hóa [`phase-1-plan.md` §10](../architecture/phase-1-plan.md) ("Candidate Phase 1 completion criteria — planning input, KHÔNG phải Phase 1 DoD chính thức") thành explicit Phase 1 gate criteria, đúng pattern §10 đã tường minh dự trù ("input cho một Phase 1 DoD artifact riêng sau này, theo pattern `phase-0-dod.md`"). Nó cũng tham chiếu [`phase-1-plan.md` §9](../architecture/phase-1-plan.md) (Quality-gate trigger map) VÀ [§11](../architecture/phase-1-plan.md) (Deferred/open items) làm nguồn cho §2/§9 dưới đây.

**Authority boundary:** tài liệu này sở hữu **substantive DoD content của Phase 1** (criteria/evidence/validator/review/finding-closure/repository-consistency/phase-decision-bundle requirements áp cho chính Phase 1) — theo delegation từ [Chapter 14 §14.3](../constitution/14-roadmap.md). Nó **KHÔNG** định nghĩa lại: phase approval orchestration ([Chapter 12](../constitution/12-approval-gates.md)); review eligibility/cardinality ([Chapter 0 §3](../constitution/00-governance.md), [Chapter 11 §11.5](../constitution/11-adr-process.md)); quality-gate semantics/trigger A–E ([Chapter 13 §13.12](../constitution/13-quality-gates.md)); ADR Scope Rule ([Chapter 0 §4b](../constitution/00-governance.md)); phase sequence/canonical Phase-plan model ([Chapter 14 §14.1–§14.2](../constitution/14-roadmap.md)); current version/status/state của bất kỳ tài liệu nào ([MANIFEST](../MANIFEST.md) theo [I-12](../constitution/02-platform-invariants.md)).

## 1. Phase identity

```text
Phase:              Phase 1 — System Architecture
Roadmap source:     Chapter 14 §14.2 (Locked, v1.6, xem MANIFEST cho current version/status)
Workstream (Chapter
14 §14.2):           Software · UX Architecture · Security & Custody Baseline · API ·
                     Database · Engine
Package decomposition
(phase-1-plan.md
§4, KHÔNG redefine
tại đây):            1.1  Module Registry & System Decomposition
                     1.2  Security & Custody Baseline
                     1.3-A  Structure/Raw-Regime Engine Architecture
                     1.3-B  Feature/Context Engine Architecture
                     1.3-C  Strategy/Decision Engine Architecture
                     1.3-D  Risk/Execution Engine Architecture
                     1.4  API Architecture
                     1.5  Database Architecture
                     1.6  UX Architecture
Phase-level output
bắt buộc:            ADR cho quyết định kiến trúc thuộc diện ADR Required (Chapter 0 §4b)
Approval Gate:       một (1) — đơn vị chịu gate LÀ Phase, KHÔNG phải package/sub-phase
                     (Chapter 14 §14.1)
```

Package→artifact mapping cụ thể (đường dẫn file, để tiện resolve — **KHÔNG** authoritative cho version/lifecycle, current state PHẢI resolve từ [MANIFEST](../MANIFEST.md) theo I-12, KHÔNG từ bảng này):

```text
1.1     architecture/module-registry.yaml, architecture/system-decomposition.md
1.2     architecture/security-custody-baseline.md
1.3-A   architecture/engine/structure-regime-architecture.md
1.3-B   architecture/engine/feature-context-architecture.md
1.3-C   architecture/engine/strategy-decision-architecture.md
        (package-1.3-c-decision-taxonomy-exploration.md LÀ exploration artifact hỗ trợ,
        KHÔNG phải package deliverable chính thức — non-authoritative, KHÔNG đếm vào
        tiêu chí §3 dưới)
1.3-D   architecture/engine/risk-execution-architecture.md
1.4     architecture/api-architecture.md
1.5     architecture/database-architecture.md
1.6     architecture/ux-architecture.md
```

## 2. Applicable gate set (Chapter 14 §14.4 declaration)

Theo [Chapter 13 §13.12](../constitution/13-quality-gates.md) (Locked), gate áp dụng theo **điều kiện kích hoạt** (trigger A–E), KHÔNG phải mặc định. Phase 1 deliverable LÀ **architecture artifact** — KHÔNG có executable implementation, KHÔNG runtime module đã build, KHÔNG tier assignment đã thực thi (dù module-registry.yaml đã đăng ký module identity cho tier-resolution tương lai). Phân tích trigger (nguồn: [`phase-1-plan.md` §9](../architecture/phase-1-plan.md) trigger map, chuyển hóa thành gate-set declaration chính thức tại đây):

```text
A. Universal — invariant conformance:
   ÁP DỤNG cho MỌI 9 package Phase 1, theo đúng Scope mà từng Platform Invariant
   (Chapter 2) tự khai báo. Đây LÀ gate set chính của Phase 1 — invariant conformance
   BY DESIGN phải verify được ngay ở tầng architecture, dù chưa có code.

B. Executable-implementation-triggered (coverage):
   DEFERRED tới implementation (Phase 3) cho MỌI 9 package — KHÔNG package Phase 1 nào
   có executable implementation tại giai đoạn này (resolved "not applicable" tại Phase
   1 gate, KHÔNG phải fail-closed — cùng logic phase-0-dod.md §2 đã áp dụng cho Product
   artifact, Chapter 13 §13.12 phân biệt tường minh "coverage not applicable" ≠
   "coverage applicable but evidence missing").

C. Tier-triggered (Chaos/Parity Test):
   DEFERRED tới implementation cho MỌI 9 package — tier assignment (Chapter 13 §13.4)
   registered tại module-registry.yaml (1.1) NHƯNG chưa thực thi build; Chaos Test
   (Tier 0, liên quan 1.3-D)/Parity Test (Tier 1, liên quan 1.3-A/1.3-C) KHÔNG áp dụng
   tại Phase 1 architecture gate.

D. Responsibility/boundary-triggered (Security/data-quality/performance/observability):
   ĐIỀU KIỆN — CHỈ áp dụng khi artifact kiến trúc thực sự định nghĩa một concrete
   boundary (KHÔNG áp dụng cho tuyên bố nguyên tắc chung). Cụ thể theo §9
   phase-1-plan.md: Package 1.2 (Security & Custody Baseline) — điều kiện, khi định
   nghĩa concrete boundary; Package 1.3-D (Risk/Execution) — điều kiện, custody-
   adjacent boundary. Package khác — N/A tại boundary hiện tại, trừ khi một concrete
   boundary declaration mới phát sinh trước gate evaluation.

E. Lifecycle-triggered (Schema/contract compatibility):
   **Package 1.4 (API Architecture) — ÁP DỤNG tường minh** (publish contract qua
   command-query-api-surface, Chapter 10 §10.3) — Package 1.4 LÀ published-contract
   artifact theo đúng Chapter 13 §13.12 artifact-class rollup ("Published contract /
   schema → A + E compatibility"). Package 1.1 (module-registry.yaml/system-
   decomposition.md) VÀ Package 1.5 (Database Architecture) — điều kiện, áp dụng nếu
   registry/persistence boundary được coi LÀ published schema tại thời điểm gate
   evaluation. Package 1.3-C — điều kiện. Package khác (1.2, 1.3-A/B/D, 1.6) — N/A tại
   boundary hiện tại.
```

**Gate set chính thức cho Phase deliverable của Phase 1 = Trigger A (universal, mọi 9 package) + Trigger D (điều kiện, chỉ khi concrete boundary — Package 1.2/1.3-D tại thời điểm authoring) + Trigger E (Package 1.4 áp dụng tường minh; Package 1.1/1.5/1.3-C điều kiện).** Trigger B/C DEFERRED tới Phase 3 cho toàn bộ 9 package — KHÔNG áp dụng tại Phase 1 gate. Đây LÀ gate-set declaration mà [Chapter 12 §12.2(5)](../constitution/12-approval-gates.md) resolve tới khi đánh giá Phase 1 Approval Gate — theo đúng authority bridge [Chapter 14 §14.3.1](../constitution/14-roadmap.md) khóa, declaration này CHỈ trở thành authoritative gate-set input cho Chapter 12/13 tại đúng thời điểm DoD này được Product Owner accept VÀ incorporate theo §14.3.1 — **chưa xảy ra tại thời điểm authoring này**.

**Xác nhận bắt buộc (fail-closed rule, Chapter 13 §13.12):** nếu một trigger condition (D/E cụ thể) KHÔNG resolve được cho một package cụ thể tại thời điểm gate evaluation thực tế — applicability chưa xác định = eligibility incomplete, **KHÔNG** được mặc định "gate không áp dụng" để bỏ qua. Bảng trên LÀ đánh giá tại boundary authoring (2026-08-07); gate evaluation thực tế PHẢI re-confirm trigger D/E cho từng package tại đúng thời điểm đó.

## 3. Substantive completion criteria

```text
1. Package completion:
   - TOÀN BỘ chín (9) package Phase 1 (1.1, 1.2, 1.3-A, 1.3-B, 1.3-C, 1.3-D, 1.4, 1.5,
     1.6) đạt `Consolidated Stable` (package lifecycle) tại MANIFEST.
   - Artifact `status: Draft` LÀ hợp lệ khi package lifecycle đã `Consolidated Stable`
     — package lifecycle VÀ artifact lifecycle LÀ hai dimension tách biệt (Chapter 0
     §7.1) — KHÔNG được conflate; `Draft` artifact status KHÔNG tự nó là một finding
     hay một tiêu chí unresolved.

2. ADR closure:
   - MỌI ADR thực sự được kích hoạt (actually-triggered) dưới ADR Scope Rule (Chapter
     0 §4b) LIÊN QUAN Phase 1 architecture decision phải `Approved` (Chapter 11 §11.5–
     §11.6) trước Phase 1 Approval Gate.
   - "Thực sự kích hoạt" nghĩa LÀ: một quyết định kiến trúc cụ thể đã được đề xuất/
     thực hiện VÀ rơi vào ADR Required column (Chapter 0 §4b — thêm/sửa Platform
     Invariant, thay đổi Event Schema, Module Taxonomy/dependency graph, Governance/
     Approval process, quyết định ảnh hưởng >1 module hoặc khó đảo ngược, sửa/
     supersede ADR đã Locked).
   - ADR CONDITIONALLY REQUIRED (phase-1-plan.md §7 — LIKELY/CONDITIONAL anticipation
     map) chỉ bắt buộc khi trigger cụ thể của điều kiện đó thực sự xảy ra tại thời
     điểm gate evaluation — hypothetical conditional ADR KHÔNG được yêu cầu nếu trigger
     KHÔNG xảy ra. KHÔNG suy diễn ngược — một ADR "có thể cần" nhưng trigger chưa xảy
     ra KHÔNG chặn gate.
   - phase-1-plan.md §7 ADR-scope anticipation map LÀ planning guidance tham khảo,
     KHÔNG phải danh sách đóng — ADR thực sự kích hoạt phải resolve từ chính quyết
     định đã ghi nhận (MANIFEST/CHANGELOG evidence), KHÔNG từ anticipation map.

3. Zero unresolved architecture Blocker/Major:
   - KHÔNG unresolved Phase 1 architecture-review Blocker hay Major nào được phép còn
     lại trên bất kỳ deliverable Phase 1 nào tại thời điểm gate evaluation (xem §7
     Finding-closure requirements).
   - Documented Product-level/Domain-level/implementation-level carry-forward gap (xem
     §9 Explicit carry-forward classification) KHÔNG tự động LÀ blocker — CHỈ khi một
     tiêu chí authoritative khác (Constitution/Domain Contract/ADR/Chapter 13 gate cụ
     thể) tường minh biến nó thành gate-blocking mới tính LÀ Blocker/Major cho mục đích
     tiêu chí này.

4. Cross-package consistency:
   - 1.3-A/1.3-B/1.3-C/1.3-D dependency/authority ordering coherent, đúng dependency
     graph tại phase-1-plan.md §5 VÀ module-registry.yaml — KHÔNG authority cạnh tranh
     giữa bốn package Engine.
   - Package 1.4 (API Architecture) VÀ Package 1.5 (Database Architecture) KHÔNG
     redefine authority của nhau, hay của module domain khác — mỗi package CHỈ elaborate
     đúng module đã đăng ký cho chính nó (Chapter 7 §7.5).
   - Package 1.6 (UX Architecture) consume published API binding từ Package 1.4 (route
     qua command-query-api-surface) — KHÔNG tự phát minh contract song song, KHÔNG tự
     chọn computation owner ngoài route ĐÃ đăng ký/ADR ĐÃ Approved.
   - Package 1.1 (module-registry.yaml/system-decomposition.md) LÀ exact reviewed
     baseline DUY NHẤT cho mọi downstream package resolution VÀ cho mọi tier-resolution
     tương lai (Chapter 13 §13.4) — downstream package KHÔNG được tự invent module
     identity/dependency edge ngoài baseline này.
```

## 4. Evidence requirements

```text
Required deliverable evidence (Chapter 12 §12.1):
  - Mỗi 9 package: package version/status/lifecycle resolve tại MANIFEST, review
    evidence (Review A + Independent Review B) pinned tại đúng baseline blob mà package
    đạt `Consolidated Stable`.
  - ADR: file ADR tương ứng cho mọi ADR actually-triggered (§3.2), `status: Approved`,
    review evidence pinned tại chính ADR file (Chapter 11 §11.6).
  - Module-registry.yaml (Package 1.1): exact reviewed baseline blob PHẢI khớp current
    content tại thời điểm mọi downstream package resolution dùng nó — không baseline
    nào stale mà chưa được flag tường minh cho review riêng.

Applicable Quality Gate evidence (Chapter 13 §13.9 evidence contract, KHÔNG redefine
tại đây):
  - Trigger A: evidence pinned cho TOÀN BỘ 9 package tại thời điểm gate evaluation.
  - Trigger B/C: KHÔNG evidence bắt buộc tại Phase 1 gate — deferred tới Phase 3
    (implementation), đúng §2 phía trên.
  - Trigger D: evidence bắt buộc CHỈ cho package có concrete boundary trigger xác nhận
    tại thời điểm gate evaluation (Package 1.2/1.3-D tại boundary authoring — re-confirm
    tại gate evaluation, §2).
  - Trigger E: evidence bắt buộc cho Package 1.4 (explicit, publish contract) VÀ cho
    bất kỳ package nào (1.1/1.5/1.3-C) mà điều kiện Trigger E xác nhận đã xảy ra tại
    thời điểm gate evaluation.
  - Gate result PHẢI LÀ **pinned evidence** (blob/commit identity, Chapter 13 §13.9
    evidence contract) — KHÔNG được **suy diễn ngầm** chỉ từ một Review A/Independent
    Review B "CLEAN" — review clean VÀ quality-gate evidence LÀ hai fact tách biệt,
    review clean KHÔNG tự động LÀ quality-gate pass evidence.

Evidence pinning rule: mọi evidence trên PHẢI pin exact blob/commit identity — KHÔNG
mutable "phiên bản mới nhất" reference (Chapter 14 §14.3 "cấm mutable reference").
```

## 5. Validator requirements

```text
- MANIFEST freshness check (Chapter 11 §11.9, I-12): mọi deliverable Phase 1 (9
  package + ADR liên quan) resolve đúng version/status/lifecycle/blob hiện tại tại
  MANIFEST — không stale pointer.
- YAML frontmatter validity: mọi living document frontmatter (module-registry.yaml VÀ
  8 package Markdown khác) parse được, field bắt buộc (id/version/status/owner/
  approved_by/approved_at) hiện diện.
- Cross-reference resolvability: mọi internal reference (package → ADR, package →
  Domain Contract, package → Product layer, package → Package 1.1 baseline) resolve
  được về đúng một target tồn tại — không mồ côi.
- Module-registry graph integrity: dependency graph (module-registry.yaml) không cycle,
  edge count/module count khớp với claim tại mỗi package's own registry-alignment
  statement.
- Required freshness/validator check PHẢI pass TRƯỚC gate eligibility — validator LÀ
  blocking consistency check, KHÔNG phải approval authority (Chapter 12 §12.2).
```

## 6. Review requirements

```text
Theo Chapter 0 §3 / Chapter 11 §11.5 (tham chiếu, KHÔNG định nghĩa lại):
  - Tối thiểu HAI (2) eligible independent review từ actor giữ role AI Technical
    Architect **tại chính Phase Approval Gate boundary** — package-level Review A/
    Independent Review B evidence (đã pin per-package trong quá trình Phase 1) KHÔNG
    tự động thay thế yêu cầu này; đây LÀ một review boundary riêng, cấp Phase.
  - Hai actor identity khác nhau thực hiện (xem team.yaml cho alias resolution).
  - Reviewer evidence pinned tại đúng Phase Approval Gate boundary.
  - Reviewer ngang hàng — sự TỒN TẠI của review LÀ điều kiện bắt buộc; kết luận KHÔNG
    ràng buộc quyết định cuối của Product Owner.
```

## 7. Finding-closure requirements

```text
- Mọi finding Blocker/Major từ bất kỳ review round nào (package Review A/Independent
  Review B, delta review, Phase 1 Approval Gate consolidated review) PHẢI resolved
  (đóng) tại MANIFEST/CHANGELOG evidence TRƯỚC KHI Phase 1 Approval Gate mở.
- Blocker/Major finding KHÔNG BAO GIỜ được waive qua residual-risk acceptance hay bất
  kỳ cơ chế nào khác — con đường DUY NHẤT để một Blocker/Major thôi chặn gate LÀ
  RESOLVED (đóng), KHÔNG phải "chấp nhận rủi ro." Đây LÀ quy tắc tuyệt đối, KHÔNG có
  ngoại lệ.
- CHỈ finding Minor mới được phép remain open qua Product Owner residual-risk
  acceptance — VÀ CHỈ khi Product Owner tường minh chấp nhận rủi ro tồn đọng (ghi rõ
  tại decision evidence, theo đúng Chapter 0 §3 "Chấp nhận rủi ro: ...") — KHÔNG ngầm
  định, KHÔNG suy diễn từ im lặng.
- Documented carry-forward gap (§9 dưới) KHÔNG PHẢI một finding chưa đóng theo nghĩa
  mục này — nó LÀ một item đã được authoritative source (§9) phân loại tường minh LÀ
  "carry-forward, KHÔNG gate-blocking trừ khi tiêu chí khác nói khác" — phân biệt bắt
  buộc giữa "carry-forward gap đã classified" VÀ "unresolved review finding".
```

## 8. Repository-consistency requirements

```text
- Backward Consistency Check (Chapter 12 §12.4, cả hai chiều A và B) chạy trên TOÀN BỘ
  deliverable Phase 1 (9 package + ADR liên quan) đối chiếu MỌI authority Locked liên
  quan (Constitution, Domain Contract, Product layer) — kết quả `No conflict` bắt buộc
  trước gate.
- Per-package BCC (nếu có, thực hiện trong quá trình từng package correction/
  consolidation) KHÔNG thay thế được full-scope Phase-wide BCC này — đúng
  phase-1-plan.md §10 "Full-scope BCC requirement" tường minh khóa.
- MANIFEST LÀ authoritative source DUY NHẤT cho current version/status/state — không
  state store cạnh tranh (I-12).
- Package lifecycle (`Consolidated Stable`) VÀ artifact lifecycle (`Draft`/`Approved`/
  `Locked`) giữ tách biệt tường minh trên MỌI 9 package — không conflate.
```

## 9. Explicit carry-forward classification

Các item sau LÀ **carry-forward gap đã biết** tại thời điểm authoring DoD này (2026-08-07) — nguồn: [`phase-1-plan.md` §11](../architecture/phase-1-plan.md) (Deferred/open items) VÀ package-level §13/preserved-gap section tương ứng của từng artifact. Chúng **KHÔNG tự động LÀ gate-blocking Blocker/Major** cho mục đích §3.3 phía trên — trừ khi một tiêu chí authoritative khác (Constitution invariant, Domain Contract, ADR đã Approved, hay chính một Chapter 13 gate cụ thể) tường minh biến item đó thành gate-blocking. Tài liệu DoD này **KHÔNG resolve** bất kỳ item nào dưới đây tại chính transaction authoring này:

```text
DD-001   Backtest Domain Contract/entity/event/schema — Deferred, liên quan Package
         1.3-A. Product Owner decision tương lai, NGOÀI phạm vi DoD này.

DD-003   PAPER-context authoritative Decision establishment mechanism — Deferred,
         mandatory TRƯỚC KHI UC-011 runtime design. Liên quan Package 1.3-C — Package
         1.3-C KHÔNG được tự phát minh mechanism này.

Package 1.5 interaction/retention gap:
         Contract-category interaction gap (review-evidence-service lấy output từ
         hai query-emitting dependency dưới consumes: [event] của chính nó) VÀ
         retention/deletion policy ownership — carry-forward, KHÔNG resolve tại Phase
         1.

UC-003 Product-level mechanism gap:
         Research-session interval identity mechanism, evidence-completeness
         determination mechanism, correction-arrival-during-window handling — Product-
         level, liên quan VIEW-002 (Package 1.6), carry-forward.

Accessibility/responsive/design-token requirement:
         Package 1.6 KHÔNG THỂ tự establish WCAG target/breakpoint semantic/branding
         rule/design-token acceptance requirement — đòi hỏi governed upstream
         Product/UX decision riêng, carry-forward (P16-A-MIN-02 correction đã satisfied
         qualification, gap tự nó VẪN mở).

VIEW-003 delegation protocol:
         Recomputation request representation, response/event correlation,
         synchronous-vs-asynchronous behavior, timeout behavior, concrete failure code,
         transport giữa review-evidence-service VÀ decision-evaluation-engine —
         implementation-level, carry-forward, KHÁC biệt khỏi VIEW-003 owner/route
         blocker (đã đóng qua ADR-021).

OQ-001   Data Retention Policy & Access Control Model chi tiết — Partially Resolved,
         RBAC cụ thể vẫn mở. Liên quan Package 1.2/1.5.

OQ-002   Strategy Lifecycle Gate (Backtest=YES + Paper=YES trước Live) — Open. Liên
         quan Package 1.3-C/1.3-D — KHÔNG package nào được tự đóng ngầm OQ-002.

OQ-003   Product Metrics cụ thể cho "Measurable" — Open. Liên quan Package 1.4, KHÔNG
         resolve tại Phase 1 architecture.
```

**Xác nhận bắt buộc:** danh sách trên tham chiếu trực tiếp `phase-1-plan.md` §11 — KHÔNG mở rộng, KHÔNG thu hẹp scope của bất kỳ item nào. DoD này **KHÔNG tuyên bố** danh sách này LÀ exhaustive cho toàn bộ Phase 1 — một carry-forward gap khác phát sinh trong quá trình Phase 1 (ví dụ qua một bounded correction transaction) PHẢI được classified tường minh tại nguồn của chính nó (package artifact §13/preserved-gap section), gate evaluation PHẢI đối chiếu current state đó, KHÔNG chỉ danh sách tại DoD v0.1 này.

## 10. Phase-decision bundle requirements (Chapter 14 §14.4.1–§14.4.2)

Tại đúng atomic recording boundary (Chapter 14 §14.4.2), bundle phải pin — **Chapter 14 authority (prepared trực tiếp tại DoD/Roadmap):**

```text
- canonical Phase identity (= "Phase 1 — System Architecture")
- exact Roadmap version/content identity đã dùng (Chapter 14 §14.2, hiện v1.6, xem
  MANIFEST cho current version/status)
- exact accepted-DoD identity/content version đã incorporate (tài liệu này, khi được
  accept — current candidate hiện v0.1, CHƯA accepted, CHƯA incorporated)
- exact gate-set declaration identity/content resolve từ đó (§2 phía trên)
```

**Reference-only (authority chapter khác, DoD KHÔNG redefine):** Product Owner DoD-acceptance evidence (Chapter 0 §3); required/submitted deliverable evidence (§4 phía trên, Chapter 12 §12.1); applicable Quality Gate result/evidence (Chapter 13 §13.9); Backward Consistency Check result (Chapter 12 §12.4); validator/freshness result (Chapter 11 §11.9); independent review evidence (Chapter 0 §3); Product Owner decision fact.

**KHÔNG thuộc prepared content — chỉ authoritative TẠI atomic recording boundary:** resulting MANIFEST transition identity (Chapter 14 §14.4.1) — tài liệu này KHÔNG đoán trước giá trị đó.

## 11. Explicit non-inclusion

```text
- `Approved`/`Phase 1 Approved` (phase decision outcome) KHÔNG phải một mục DoD tại
  đây (Chapter 12 §12.1 cấm tường minh vòng lặp định nghĩa) — nó LÀ outcome của Phase
  1 Approval Gate, xảy ra SAU khi mọi mục §3–§10 ở trên đã resolve.
- DoD satisfaction (mọi mục §3–§10 resolve) CHỈ establish GATE ELIGIBILITY — nó KHÔNG
  tự động LÀ Phase 1 approval. Product Owner LÀ authority DUY NHẤT quyết định `Approve`
  / `Reject` / `Revision Requested` SAU KHI eligibility đầy đủ (Chapter 12 §12.2) — DoD
  này KHÔNG thay thế, KHÔNG bind trước quyết định đó.
- Tài liệu này KHÔNG tự nó thực hiện: Phase-wide Backward Consistency Check (§8, chỉ
  ĐỊNH NGHĨA yêu cầu, KHÔNG chạy nó); Gate 2 review; Gate 2 mở; Phase 1 approval; Phase
  2 mở; implementation authorization; LIVE authorization.
- Tài liệu này KHÔNG đóng OQ-001, OQ-002, hay OQ-003.
- Tài liệu này KHÔNG sửa Constitution/Domain Contract/Product/ADR/package architecture
  semantics nào.
- Tài liệu này KHÔNG tạo ADR nào.
```

## 12. Acceptance status

```text
Product Owner acceptance của DoD này:   ĐÃ ghi nhận (2026-08-07, mechanical lifecycle-
                                        recording transaction `Phase 1 DoD v0.1
                                        Acceptance + Canonical Incorporation
                                        Executor`, Decision Workflow — Chapter 0 §3).
                                        Nguyên văn: "ACCEPT AND INCORPORATE PHASE 1
                                        DOD V0.1."

Review evidence trước acceptance:
  Review A:                             CLEAN
  Independent Review B:                 CLEAN
  Blocker:                              0
  Major:                                0
  Minor:                                0

Canonical incorporation (Chapter 14
  §14.3.1) vào Phase-plan của Phase 1:  ĐÃ tồn tại — bốn điều kiện §14.3.1 thỏa đầy đủ,
                                        cùng một evidence:

  1. Product Owner acceptance evidence resolve được:      CÓ (transaction này).
  2. Cùng evidence đó xác định tường minh:
       Phase identity:                  Phase 1 — System Architecture
       Roadmap phase-section version/
         content identity:              Chapter 14 — Roadmap, v1.6, Locked (current
                                         version resolve từ MANIFEST theo I-12)
       DoD version/content identity:    docs/phase-dod/phase-1-dod.md, v0.1, accepted
                                         substantive blob
                                         31353882424f4db7d6ed6008cedd503f627d53d4
       Explicit incorporation decision: "phase-1-dod.md v0.1 is incorporated into the
                                         canonical Phase 1 plan as the single
                                         authoritative Phase 1 DoD" (Product Owner)
  3. Evidence tồn tại TRƯỚC Phase 1 gate evaluation:       CÓ — Phase 1/Gate 2 CHƯA mở
                                                            (§11 phía trên, §2 gate-set
                                                            declaration).
  4. Đúng MỘT incorporation, KHÔNG xung đột:                CÓ — đây LÀ acceptance
                                                            evidence DUY NHẤT cho Phase
                                                            1 DoD tại boundary này.

Hệ quả:                                Gate-set declaration tại §2 nay hợp lệ cho mục
                                        đích Chapter 12/13 sử dụng — LÀ authoritative
                                        Phase 1 DoD kể từ transaction này (Chapter 12
                                        §12.2 điểm 5: "Approved/Locked authoritative
                                        quality contract hoặc phase plan"). `G2-RDY-
                                        BLK-01` ("dedicated Phase 1 DoD absent") — NAY
                                        CLOSED, đóng đúng bởi transaction này.
```

**Transaction này CHỈ ghi nhận DoD acceptance/incorporation. Nó KHÔNG:**

```text
tuyên bố Phase 1 DoD criteria (§1–§10) đã pass (VẪN LÀ tiêu chí CẦN đạt, KHÔNG phải ĐÃ
  đạt)
tuyên bố Phase 1 hoàn thành
chạy full-scope Backward Consistency Check (§8)
sinh Quality Gate PASS evidence (§4)
thực hiện Phase-level Gate review (§6)
mở/thực hiện Gate 2 review
approve Phase 1
mở Phase 2
authorize implementation/LIVE
đóng `G2-RDY-BLK-02`/`G2-RDY-BLK-03`/`G2-RDY-BLK-04`/`G2-RDY-MAJ-01`/`G2-RDY-MAJ-02`/
  `G2-RDY-MIN-01` — TẤT CẢ VẪN open
tuyên bố overall Gate 2 readiness
sửa `phase-1-plan.md`, Constitution chapter, ADR, package architecture artifact,
  Domain Contract, hay Product artifact nào
```

**Việc tiếp theo:** một Phase 1 Approval Gate consolidated review (ChatGPT Review A + Independent Review B trên toàn bộ Phase 1 evidence, §4, bao gồm full-scope Backward Consistency Check, §8) — cùng việc đóng các finding Gate 2 readiness còn lại (`G2-RDY-BLK-02`/`03`/`04`, `G2-RDY-MAJ-01`/`02`, `G2-RDY-MIN-01`) — trước khi Product Owner đưa ra Phase 1 Approval Gate decision (Chapter 12 §12.2) hay Gate 2 mở.
