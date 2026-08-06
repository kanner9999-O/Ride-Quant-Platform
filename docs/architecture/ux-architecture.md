---
id: ux-architecture
title: "Package 1.6 — UX Architecture"
version: "0.4"
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

# Package 1.6 — UX Architecture

**CANDIDATE — status: Draft, KHÔNG Consolidated Stable, KHÔNG Approved.** Package 1.6 v0.1 — candidate đầu tiên, author dựa trên Package 1.1 `Consolidated Stable` (v0.7, 25 module), Package 1.2 `Consolidated Stable` (v0.4), Package 1.3-A/1.3-B/1.3-C/1.3-D `Consolidated Stable`, Package 1.4 `Consolidated Stable` (v0.3), Package 1.5 `Consolidated Stable` (v0.2), [`ux-blueprint.md`](../product/ux-blueprint.md) (Package 0.3-C, `Consolidated Stable`), VÀ [`phase-1-plan.md`](phase-1-plan.md) v0.4 (`Approved`) §"Package 1.6 — UX Architecture". Đây LÀ một authoring transaction, KHÔNG PHẢI một review/consolidation transaction. Chưa qua Review A/Independent Review B, chưa có Product Owner consolidation decision.

**v0.4 — bounded correction (2026-08-06), đóng phần VIEW-002 của `P16-A-MAJ-02` (VIEW-002/VIEW-003 synthesis-owner gap), KHÔNG redesign/mở rộng scope, vai trò: `Package 1.6 VIEW-002 Correction Executor`:** Approved [ADR-020](../adr/ADR-020.md) v0.1 quyết định `review-evidence-service` LÀ computation boundary cho UC-003 Research verification existence-check — VIEW-002's registry/API-binding blocker (§13 gap #1, phần VIEW-002) nay RESOLVED. §1/§2/§4.1/§4.3/§4.5/§7/§13/§14/§15 sửa: VIEW-002 KHÔNG còn trình bày TECHNICALLY BLOCKED bởi absence của computation owner/route API. Binding established: `ux-application-shell → command-query-api-surface → review-evidence-service` (route ĐÃ đăng ký từ Package 1.4 v0.1, KHÔNG edge/contract-category mới — cả bốn module nguồn ĐÃ CÓ trong `review-evidence-service.depends_on`, Package 1.1 v0.9); query LÀ non-authoritative, interval-bounded UC-003 existence-check, kết quả `PASSED / FAILED / INDETERMINATE`, tính trên Decision (`decision-authority-service`), RiskEvaluation VÀ Execution Intent (CẢ HAI tại `risk-gateway`), Order (`execution-engine`), ExecutionResult (`execution-result-processor`) fact ĐÃ tồn tại — `review-evidence-service` CHỈ thực hiện existence-check, KHÔNG tái tính toán Decision/Risk/Execution logic, KHÔNG author entity/event authoritative mới, `owns_authoritative_state: false` KHÔNG đổi. **VIEW-003 KHÔNG resolve tại transaction này** — VẪN TECHNICALLY BLOCKED, `P16-A-MAJ-02` KHÔNG đóng hoàn toàn (CHỈ nửa VIEW-002); VIEW-003 KHÔNG chia sẻ kết quả/computation owner của VIEW-002 — computation owner VIEW-003 CHƯA chọn (route tương lai VẪN cùng hình dạng ba tầng `ux-application-shell → command-query-api-surface → [module TBD]`, module cụ thể CHƯA quyết định), `canonical semantic-decision hash` (decision.md, Package 0.2-C4) VẪN chưa định nghĩa, VIEW-003's INDETERMINATE-equivalent outcome VẪN unresolved — ADR-020 §4/§12 xác nhận đây LÀ một scope conflict tường minh, KHÔNG một silent decision. Current-normative upstream reference cập nhật đúng baseline hiện tại: `module-registry.yaml` v0.8 → v0.9, `system-decomposition.md` v0.9 → v1.0, `api-architecture.md` v0.5 → v0.6 (§0/§1/§2.1/§13/§14) — tham chiếu v0.8/v0.5 BÊN TRONG bản ghi lịch sử tường minh (banner v0.1/v0.2/v0.3 phía trên, VÀ mọi citation NAV-003-specific tại §4.1/§4.3/§4.5/§7/§13/§14/§15) GIỮ NGUYÊN, KHÔNG sửa — đó LÀ mô tả trung thực trạng thái NAV-003 tại thời điểm v0.3, KHÔNG PHẢI current-normative claim cho VIEW-002. Ba missing semantic item UC-003 (Research-session interval identity mechanism, evidence-completeness determination mechanism, correction-arrival-during-window handling) VẪN unresolved — Product-level, KHÔNG resolve tại transaction này, VIEW-002 KHÔNG trình bày như implementation-ready. **KHÔNG đổi:** NAV-003 binding (§4.1/§4.3, v0.3, byte-identical); DD-001/`backtest-orchestrator.owns_authoritative_state` classification (VẪN deferred/unresolved, KHÔNG liên quan); `ux-application-shell.forbidden_dependencies` (14 entry, KHÔNG đổi — `review-evidence-service` VẪN nằm trong đó, UX Shell VẪN KHÔNG có route trực tiếp); accessibility/design-token gap (§13 gap #3); Package 1.5 interaction gap; identifier accounting (59/59, KHÔNG đổi); UX Blueprint screen/flow/state semantics (KHÔNG redefine); component decomposition (§5)/state model (§6) — byte-identical; field-level API schema; frontend framework/technology choice; Package 1.6 module registry classification (§2.1, byte-identical). `package lifecycle: candidate` KHÔNG đổi — KHÔNG consolidate tại transaction này. `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi.

**v0.3 — bounded correction (2026-08-06), đóng upstream prerequisite của `P16-A-MAJ-01` (NAV-003 registry/API-binding gap), KHÔNG redesign/mở rộng scope, vai trò: `Package 1.6 NAV-003 Binding Correction Executor`:** Package 1.1 v0.8 (`Consolidated Stable`, ADR-019 alignment) VÀ Package 1.4 v0.5 (`Consolidated Stable`) nay đã established route `command-query-api-surface → backtest-orchestrator` — NAV-003's registry/API binding blocker (§13 gap #2) nay RESOLVED. §1/§2/§4.1/§4.3/§4.5/§7/§13/§14/§15 sửa: SCR-003/SCR-004/SCR-005 KHÔNG còn trình bày TECHNICALLY BLOCKED bởi absence của route API; phần `backtest-orchestrator` của SCR-011/VIEW-005 tương tự KHÔNG còn blocked. Binding established: `ux-application-shell → command-query-api-surface → backtest-orchestrator`; query LÀ non-authoritative bounded Backtest run correlation view, composed từ Decision (`decision-authority-service`) VÀ RiskEvaluation (`risk-gateway`) fact ĐÃ tồn tại — authority của cả hai KHÔNG đổi. Run identity VẪN LÀ khái niệm correlation/grouping của ADR-018, KHÔNG một entity/event/authoritative fact mới. `backtest-orchestrator.owns_authoritative_state` VẪN `deferred` (DD-001 CHƯA resolve, Package 1.1 §11) — KHÔNG resolve tại transaction này, KHÔNG chuyển `true`/`false`. Current-normative upstream reference cập nhật đúng baseline hiện tại: `module-registry.yaml` v0.7 → v0.8, `system-decomposition.md` v0.7 → v0.9, `api-architecture.md` v0.3 → v0.5 (§1/§2/§7/§13/§14) — tham chiếu v0.7/v0.3 BÊN TRONG bản ghi lịch sử tường minh (banner v0.1/v0.2 phía trên) GIỮ NGUYÊN, KHÔNG sửa. **KHÔNG đổi:** VIEW-002/VIEW-003 synthesis-owner gap (§13 gap #1, VẪN TECHNICALLY BLOCKED, `P16-A-MAJ-02` VẪN unresolved); DD-001/`owns_authoritative_state` classification (VẪN deferred/unresolved); identifier accounting (59/59, KHÔNG đổi); UX Blueprint screen/flow/state semantics (KHÔNG redefine); component decomposition (§5)/state model (§6) — byte-identical; field-level API schema; frontend framework/technology choice; Package 1.6 module registry classification (§2.1, byte-identical). `package lifecycle: candidate` KHÔNG đổi — KHÔNG reconsolidate tại transaction này. `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi.

**v0.2 — bounded correction (2026-08-05), đóng bốn Review A finding trên v0.1 (`P16-A-MAJ-01`/`P16-A-MAJ-02`/`P16-A-MIN-01`/`P16-A-MIN-02`), KHÔNG redesign/mở rộng scope:** (a) `P16-A-MAJ-01` — §4.1/§4.3/§13 sửa: NAV-003 (SCR-003/SCR-004/SCR-005, cộng phần backtest-orchestrator của SCR-011/VIEW-005) KHÔNG còn trình bày như fully bound — `command-query-api-surface.depends_on` v0.7 KHÔNG chứa `backtest-orchestrator`, route API KHÔNG tồn tại; xác nhận identifier/component placement VẪN accounted for NHƯNG backend binding technically blocked, LÀ upstream registry/API-alignment prerequisite (KHÔNG Package 1.6 resolve, KHÔNG tự thêm edge/invent contract). (b) `P16-A-MAJ-02` — §3/§4.1/§13 sửa: bỏ "ngoại lệ có điều kiện" cho VIEW-002 tự thực hiện synthesis — non-authoritative output VẪN đòi hỏi computation owner/contract đã established; `ux-application-shell` KHÔNG sở hữu, `command-query-api-surface` KHÔNG tự động sở hữu; Package 1.6 KHÔNG chọn client-side/API-side; VIEW-002/VIEW-003 binding VẪN technically blocked. (c) `P16-A-MIN-01` — §4.1/§4.5/§14/§15 sửa: tách bạch tường minh identifier accounting (59/59 VẪN đầy đủ, KHÔNG đổi) khỏi technical-realization completeness (KHÔNG COMPLETE trong khi hai Major prerequisite trên VẪN unresolved) — KHÔNG identifier nào bị xóa/claim missing. (d) `P16-A-MIN-02` — §12/§13 sửa: qualify accessibility/design-token gap — Package 1.6 KHÔNG THỂ tự establish WCAG/breakpoint/branding/design-token requirement qua bất kỳ correction transaction nào, đòi hỏi governed upstream Product/UX decision trước, KHÔNG silently trở thành UX acceptance-semantics authority. Mọi nội dung khác của v0.1 GIỮ NGUYÊN — KHÔNG registry/API architecture nào sửa, KHÔNG upstream gap nào resolve, KHÔNG review mới thực hiện.

## 0. Vai trò của tài liệu này — scope resolved từ controlling source (bắt buộc, yêu cầu task)

Scope resolve TRỰC TIẾP từ `phase-1-plan.md` (Approved, controlling), nguyên văn:

```text
Package ID:              1.6
Name:                     UX Architecture
Purpose:                  Technical realization của Package 0.3-C UX Blueprint (17
                          screen/view, WS-001, NAV-001–006) — component decomposition,
                          state management, frontend module boundary.
Inputs:                   ux-blueprint.md (Package 0.3-C, Consolidated Stable), 1.4 API
                          Architecture (data/command contract surface để bind).
Outputs:                  docs/architecture/ux-architecture.md.
Explicit non-goals:       KHÔNG author component code; KHÔNG chọn frontend framework;
                          KHÔNG pixel-level design; KHÔNG redefine screen/flow/state đã
                          bounded ở ux-blueprint.md.
Dependencies:              1.4 (để Consolidated Stable).
Review A scope:            Mọi SCR/VIEW/WS/NAV/FLOW/STATE trace được về component
                          architecture — không mồ côi, không invent UX behavior mới
                          ngoài ux-blueprint.md.
Independent Review B
  scope:                   Độc lập xác nhận data-binding khớp đúng API Architecture
                          (1.4) contract surface, không tự phát minh contract riêng.
Product Owner decision
  point:                   Sau Review A/B CLEAN.
Consolidation condition:  Zero unresolved Blocker/Major; 1.4 Consolidated Stable; toàn
                          bộ acceptance surface UX Blueprint có component tương ứng.
```

**Đây là MỘT artifact duy nhất** (`docs/architecture/ux-architecture.md`) elaborate kiến trúc kỹ thuật cho ĐÚNG MỘT module đã đăng ký assign cho Package 1.6 tại Package 1.1: `ux-application-shell` (`module-registry.yaml` v0.9, `Consolidated Stable`, `phase.elaborated_by: "1.6"` — script-verified, MỘT VÀ CHỈ MỘT module mang assignment này).

**KHÔNG thuộc phạm vi tài liệu này:** React/Vue/Svelte hay bất kỳ frontend framework choice nào; component source code; CSS/design-system implementation; pixel-perfect layout; field-level API schema; Product/UX behavior MỚI ngoài `ux-blueprint.md` đã Consolidated Stable; authentication implementation; database persistence design; custody implementation; backend orchestration; Package 1.5 gap resolution (§9); LIVE activation.

## 1. Governing authority

```text
Constitution (Chapter 0–14, Locked):              highest architectural authority, đặc
                                                    biệt I-1 (Explainability), I-3 (No
                                                    Repaint), I-6 (Fail-Safe by Scope),
                                                    I-7 (Plugin Non-Bypass), I-11 (Secrets
                                                    & Custody Isolation), I-12 (Single
                                                    Source of Truth)
Chapter 7 (Module Taxonomy, Locked):               §7.4 Projection constraint (Locked);
                                                    §7.5 module classification authority
                                                    = module-registry.yaml
module-registry.yaml v0.9 (Consolidated
  Stable, 25 module):                              module identity/taxonomy/dependency
                                                    authority — KHÔNG redefine tại đây;
                                                    `ux-application-shell` ĐÃ đăng ký,
                                                    `phase.elaborated_by: "1.6"`;
                                                    `command-query-api-surface →
                                                    backtest-orchestrator` edge ĐÃ
                                                    registered (v0.8, ADR-019 v0.2
                                                    Approved alignment);
                                                    `review-evidence-service.
                                                    responsibilities` +1 VIEW-002/UC-003
                                                    existence-check (v0.9, ADR-020 v0.1
                                                    Approved alignment, KHÔNG edge mới)
system-decomposition.md v1.0 (Consolidated
  Stable):                                         semantic parity với module-registry.yaml
                                                    v0.9 — KHÔNG redefine tại đây
api-architecture.md v0.6 (Package 1.4,
  Consolidated Stable):                             command-query-api-surface exposure/
                                                    routing/non-bypass boundary VÀ contract
                                                    governance — Package 1.6 bind VÀO đúng
                                                    boundary đó, KHÔNG redefine; §9 NAV-003
                                                    Backtest route (`backtest-orchestrator`)
                                                    VÀ VIEW-002 existence-check
                                                    (`review-evidence-service`) ĐÃ elaborate
                                                    tại boundary đó
database-architecture.md v0.2 (Package 1.5,
  Consolidated Stable):                             persistence authority model, review-
                                                    evidence-service boundary, contract-
                                                    category interaction gap — consumed
                                                    như forward reference cho §10 dưới,
                                                    KHÔNG resolve
security-custody-baseline.md v0.4 (Package
  1.2, Consolidated Stable):                        custody/signing trust boundary — Package
                                                    1.6 elaborate CHỈ absence-of-access
                                                    treatment (§8 dưới), KHÔNG redefine
Package 1.3-A/1.3-B/1.3-C/1.3-D (Consolidated
  Stable):                                          Data/Structure/Regime/Feature/Context/
                                                    Decision/Risk/Execution boundary —
                                                    consumed như forward reference, KHÔNG
                                                    redefine
ux-blueprint.md (Package 0.3-C, Consolidated
  Stable):                                          17 screen/view (11 SCR, 6 VIEW), WS-001,
                                                    NAV-001–006, FLOW-001–006, STATE-001–029,
                                                    UX-INV-1–10, UX-P-1–5 — controlling
                                                    authority cho MỌI screen/flow/state
                                                    semantics; Package 1.6 KHÔNG redefine,
                                                    CHỈ technical-realize
product-requirement.md / use-case-workflow.md:     PR-XXX/UC-XXX authority mà ux-blueprint.md
                                                    đã trace — tham chiếu gián tiếp qua
                                                    ux-blueprint.md, KHÔNG redefine trực
                                                    tiếp tại đây
phase-1-plan.md v0.4 (Approved):                   Phase 1 work-breakdown/package-boundary
                                                    authority, nguồn CHÍNH của §0 scope
                                                    resolution
Package 1.6 (tài liệu này):                        technical elaboration authority ONLY,
                                                    cho ux-application-shell — component
                                                    decomposition/state management/frontend
                                                    module boundary/API binding
```

Package 1.6 KHÔNG redefine domain entity/event semantics, module identity/taxonomy, screen/flow/state semantics đã pin tại `ux-blueprint.md`, hay bất kỳ package đã Consolidated Stable nào — mọi nội dung dưới đây chỉ **elaborate** technical realization trong ranh giới đã pin.

## 2. Module boundary — UX Application Shell (module DUY NHẤT gán cho Package 1.6, registry parity, bắt buộc yêu cầu task)

### 2.1 Registry classification (bảo toàn nguyên vẹn, KHÔNG sửa registry)

```text
module_id:                 ux-application-shell
name:                      UX Application Shell
module_type:               runtime_service
owns_authoritative_state:  false
consumes:                  query
emits:                     command
depends_on:                command-query-api-surface
forbidden_dependencies:    structure-engine, raw-regime-engine, feature-engine,
                           context-aggregator, strategy-engine, decision-evaluation-
                           engine, decision-authority-service, risk-gateway,
                           execution-engine, execution-result-processor, fill-processor,
                           position-projection, replay-integration-service,
                           review-evidence-service
plugin_relation:           none
security_classification:   none
implements_capabilities:   []
serves_contexts:           []
phase:                     { identified_in: "1.1", elaborated_by: "1.6" }
```

**Xác nhận tường minh (bắt buộc, yêu cầu task):** classification, `depends_on` (đúng MỘT edge: `command-query-api-surface`), `forbidden_dependencies` (14 entry), `emits`/`consumes`, `implements_capabilities: []`/`serves_contexts: []`, VÀ `phase.elaborated_by: "1.6"` trên đây LÀ nguyên trạng từ `module-registry.yaml` v0.9 (Consolidated Stable) — Package 1.6 KHÔNG sửa/redefine bất kỳ field nào trong số này, KHÔNG thêm/bớt một dependency edge, capability, context, authority, hay contract category nào. Registry `notes` (nguyên văn): "Forbidden direct-engine dependencies enforce UX must go through command-query-api-surface, not bypass it (same non-bypass principle applied to UI as to plugins)."

### 2.2 Authority status — technical realization boundary, KHÔNG business/domain authority

```text
ux-application-shell.owns_authoritative_state: false — module KHÔNG sở hữu bất kỳ
  authoritative domain fact nào (Decision, Trade Intent, RiskEvaluation, Execution
  Intent, Order, ExecutionResult, Fill, Account, credential/signing fact — tất cả thuộc
  authority của module registered elaborate riêng, KHÔNG đổi bởi Package 1.6). Position
  KHÔNG một authoritative fact (position-projection.owns_authoritative_state: false,
  Package 1.5 §2.2/§5) — KHÔNG bị conflate với authoritative fact khi UX Shell present.

implements_capabilities: [] / serves_contexts: [] (registry, KHÔNG đổi) — cùng nguyên
  tắc đã dùng cho command-query-api-surface (Package 1.4 §2.2) VÀ review-evidence-service
  (Package 1.5 §2.2): tránh silent invention một capability/domain-context identity
  cạnh tranh ngoài context-map.yaml.
```

## 3. UX authority boundary (bắt buộc, yêu cầu task)

```text
UX Blueprint (Package 0.3-C, Consolidated Stable) sở hữu screen, view, workspace,
  navigation, flow, VÀ UI-state semantics — WHAT mỗi screen/view/flow/state LÀ, khi
  nào nó xuất hiện, nó hiển thị gì. Package 1.6 KHÔNG redefine bất kỳ semantics nào
  trong số này (§0).

Package 1.6 CHỈ sở hữu technical realization — component decomposition (§5), state
  management architecture (§6), frontend module boundary (§2/§7), API binding (§7) —
  HOW ux-blueprint.md's WHAT được hiện thực hoá ở mức kiến trúc, KHÔNG source code.

UX Application Shell KHÔNG sở hữu Domain hay business authority nào — `owns_
  authoritative_state: false` (§2.2) áp dụng TUYỆT ĐỐI, KHÔNG ngoại lệ cho bất kỳ
  screen/view nào kể cả command-emitting screen (SCR-006, SCR-010, VIEW-006).

Rendering, local interaction, VÀ command orchestration KHÔNG tạo business acceptance:
  UX Shell render một view, xử lý local interaction (click/input/navigation), VÀ
  orchestrate command emission (`emits: [command]`, registry) — KHÔNG hành động nào
  trong số này TỰ THÂN tạo ra một authoritative outcome; command PHẢI được authoritative
  owning boundary chấp nhận VÀ validate (cùng nguyên tắc "transport acceptance ≠
  business acceptance" đã pin tại Package 1.4 §3, KHÔNG đổi, áp dụng ĐỒNG NHẤT ở đây).

UX KHÔNG được recompute Decision, Risk, Execution, Position, hay review truth: mọi giá
  trị hiển thị PHẢI đến từ query result của module authoritative/designated tương ứng
  (§7 dưới) — UX Shell KHÔNG tự tính toán một giá trị "tương đương" thay vì forward
  kết quả đã tồn tại (cùng nguyên tắc no-recompute đã pin cho review-evidence-service,
  Package 1.5 §4, áp dụng ĐỒNG NHẤT cho UX presentation layer), KHÔNG ngoại lệ.

Xác nhận tường minh (bắt buộc, v0.2 correction, đóng `P16-A-MAJ-02`): VIEW-002's
  workflow-visible PASSED/FAILED/INDETERMINATE result VÀ VIEW-003's parity match/
  mismatch result ĐỀU LÀ non-authoritative output (UC-003/UC-005, use-case-workflow.md,
  nguyên văn) — NHƯNG một non-authoritative output VẪN đòi hỏi một computation owner VÀ
  contract đã established RÕ RÀNG, KHÔNG tự động suy ra từ việc nó "không authoritative".
  `ux-application-shell` KHÔNG sở hữu computation này (`owns_authoritative_state: false`,
  §2.2, KHÔNG thay đổi bởi tính chất non-authoritative của kết quả). `command-query-api-
  surface` VẪN LÀ routing/exposure-only (Package 1.4 §2.2, Consolidated Stable, KHÔNG
  đổi) — KHÔNG TỰ ĐỘNG sở hữu synthesis chỉ vì nó route request. Package 1.6 KHÔNG chọn
  giữa client-side hay API-side execution cho synthesis này — quyết định đó đòi hỏi một
  controlling ownership/contract CHƯA established. §4 VIEW-002/VIEW-003 row VÀ §13 gap
  #1 ghi nhận binding này VẪN technically blocked, KHÔNG một "exception" nào cho phép
  UX tự thực hiện synthesis tại v0.1/v0.2.

`command-query-api-surface` VẪN LÀ backend dependency đã đăng ký DUY NHẤT (§2.1
  `depends_on`) — UX KHÔNG có route nào khác tới bất kỳ backend module nào.
```

## 4. Complete acceptance-surface traceability (bắt buộc, yêu cầu task)

**Nguyên tắc bắt buộc (phạm vi bảng):** bảng chi tiết bảy-cột dưới đây áp dụng cho ĐÚNG 17 SCR/VIEW (đơn vị acceptance-surface chính mà `phase-1-plan.md` VÀ `ux-blueprint.md` đặt tên tường minh). `WS-001`, sáu `NAV-XXX`, sáu `FLOW-XXX`, VÀ 29 `STATE-XXX` LÀ supporting element ĐÃ có đầy đủ UC/PR traceability tại `ux-blueprint.md` (§5/§5a/§8/§11) — Package 1.6 trace MỖI ID đó về đúng SCR/VIEW sở hữu VÀ phân loại state/API category (bảng compact §4.2–§4.4 dưới), KHÔNG lặp lại toàn bộ nội dung §5–§11 của `ux-blueprint.md` (tránh copy full upstream content) — xác nhận KHÔNG ID nào bị bỏ sót (§4.5).

### 4.1 Ma trận 17 SCR/VIEW — bảy cột đầy đủ (bắt buộc, yêu cầu task)

**Bảng A — ownership, component, VÀ API binding:**

| ID | Owning UX surface (NAV) | Component/container responsibility (§5) | Required API interaction (qua command-query-api-surface) |
|---|---|---|---|
| SCR-001 | NAV-001 Research | Route/surface container + query-bound view component | Query: market-reference-service (Instrument/Venue), market-data-ingestion (Candle), structure-engine/raw-regime-engine/feature-engine/context-aggregator (market-analysis derived fact) |
| VIEW-001 | NAV-001 Research (global commit-gate) | Command interaction component (selection) + environment/account context boundary | Query: strategy-engine (Strategy Instance identity), account-service (Account context). "Pin" LÀ local/session UX state (§6), KHÔNG backend command — KHÔNG `PaperSession` entity (ux-blueprint.md §3, nguyên văn) |
| VIEW-002 | NAV-001 Research (commit-gate) | Query-bound view component | **Established (v0.4, đóng phần VIEW-002 của `P16-A-MAJ-02`)**: Query qua `command-query-api-surface → review-evidence-service` (route ĐÃ đăng ký từ Package 1.4 v0.1, KHÔNG edge/contract-category mới) — `review-evidence-service` LÀ computation boundary duy nhất (ADR-020 v0.1 Approved), thực hiện non-authoritative, interval-bounded UC-003 existence-check trên Decision (`decision-authority-service`), RiskEvaluation VÀ Execution Intent (CẢ HAI tại `risk-gateway`), Order (`execution-engine`), ExecutionResult (`execution-result-processor`) fact ĐÃ tồn tại — bốn module nguồn ĐÃ CÓ trong `review-evidence-service.depends_on` (Package 1.1 v0.9); KHÔNG tái tính toán Decision/Risk/Execution logic, KHÔNG append/replace/sở hữu fact nguồn, KHÔNG author entity/event authoritative mới — `owns_authoritative_state: false` KHÔNG đổi |
| SCR-002 | NAV-002 Replay | Route/surface container + query-bound view component | Query: replay-integration-service (canonical Replay Cursor, Chapter 8 §8.5) + authoritative stream tại cursor đó (decision-authority-service/risk-gateway/execution-engine chain, per rebuild determinism) |
| VIEW-003 | NAV-002 Replay | Query-bound view component (component placement CHỈ — computation owner CHƯA established, xem dưới) | Underlying evidence: replay-integration-service + authoritative comparison evidence — **TECHNICALLY BLOCKED (đóng nửa VIEW-003 của `P16-A-MAJ-02`)**: KHÔNG computation owner established cho parity match/mismatch synthesis, KHÔNG UX/API-side selection tại Package 1.6; VIEW-003 KHÔNG chia sẻ computation/route của VIEW-002 (§13 gap #1, phần VIEW-003) — `canonical semantic-decision hash` (decision.md, Package 0.2-C4) VẪN chưa định nghĩa, ADR-020 §4/§12 xác nhận đây LÀ một scope conflict tường minh, KHÔNG resolve tại transaction này |
| SCR-003 | NAV-003 Backtest | Command interaction component | **Established (v0.3, đóng upstream prerequisite của `P16-A-MAJ-01`)**: Command/Query qua `command-query-api-surface → backtest-orchestrator` (registered edge — Package 1.1 v0.8/Package 1.4 v0.5, `Consolidated Stable`); `backtest-orchestrator` composes non-authoritative bounded Backtest run correlation view từ Decision (`decision-authority-service`)/RiskEvaluation (`risk-gateway`) fact ĐÃ tồn tại; `owns_authoritative_state: deferred` VẪN (DD-001 CHƯA resolve, Package 1.1 §11) — ảnh hưởng authoritative-state classification của Backtest run evidence, KHÔNG còn ảnh hưởng route/binding establishment |
| SCR-004 | NAV-003 Backtest | Query-bound view component | **Established (v0.3)**: cùng route SCR-003 — `backtest-orchestrator` reachable qua `command-query-api-surface` (Package 1.1 v0.8); Backtest run evidence scoped riêng biệt khỏi PAPER (`forbidden_dependencies` loại trừ execution-engine/paper-execution-boundary/execution-result-processor/fill-processor/position-projection) KHÔNG đổi; `owns_authoritative_state: deferred` VẪN unresolved (DD-001) |
| SCR-005 | NAV-003 Backtest | Query-bound view component | **Established (v0.3)**: cùng route SCR-003/SCR-004 |
| SCR-006 | NAV-004 Paper | Command interaction component (initiation) + environment/account context boundary | Command: execution-engine (khởi tạo, qua mandatory non-bypass chain risk-gateway → execution-engine, Package 1.3-D §3/§10, KHÔNG đổi); Query: risk-gateway/execution-engine/decision-authority-service (PAPER Decision lineage) |
| SCR-007 | NAV-004 Paper | Query-bound view component | Query: execution-engine (Order), execution-result-processor (ExecutionResult), fill-processor (Fill), position-projection (Position — projection evidence, §9) |
| SCR-008 | NAV-005 Review | Evidence/review presentation component | Query: review-evidence-service (Package 1.5) — Decision→Position lineage trace, KẾ THỪA contract-category interaction gap của Package 1.5 (position-projection/replay-integration-service dưới `consumes: [event]`, §9/§10, KHÔNG resolve tại Package 1.6) |
| SCR-009 | NAV-005 Review | Evidence/review presentation component | Query: review-evidence-service (Historical State Comparison) — cùng interaction gap kế thừa |
| VIEW-004 | NAV-005 Review | Evidence/review presentation component | Query: review-evidence-service (Correction Inspection, correction lineage) — cùng interaction gap kế thừa |
| SCR-010 | NAV-006 Improve | Command interaction component | Command: strategy-engine (Strategy Definition Version creation) |
| VIEW-006 | NAV-006 Improve | Command interaction component | Command: strategy-engine (Strategy Instance registration, gắn version mới) |
| SCR-011 | NAV-006 Improve | Query-bound view component (comparison) | Query: strategy-engine (Strategy Instance/Version identity — established route) + backtest-orchestrator chain (outcome evidence per version, ≥2 Instance) — phần `backtest-orchestrator` **Established (v0.3)**, cùng route SCR-003 (Package 1.1 v0.8/Package 1.4 v0.5); phần strategy-engine KHÔNG blocked |
| VIEW-005 | NAV-006 Improve | Evidence/review presentation component | Query: execution-engine/execution-result-processor/fill-processor chain (PAPER family — established route) VÀ/HOẶC backtest-orchestrator (Backtest family — **Established (v0.3)**, cùng route SCR-003), resolve ĐỘC LẬP per FLOW-005; PAPER-family phần KHÔNG blocked |

**Bảng B — state classification, failure treatment, environment boundary, VÀ implementation status:**

| ID | Local vs authoritative state (§6) | Loading/empty/error/stale/unauthorized treatment (§10) | Environment/Account boundary (§8) | Implementation status |
|---|---|---|---|---|
| SCR-001 | API transport state (query pending/result) — KHÔNG local business state | STATE-001 loading; STATE-003 invalid Instrument/Venue; STATE-005 missing historical evidence | Instrument/Venue selector giới hạn TradableListing đã đăng ký (UX-INV-2); Account context read-only (UX-INV-1) | architecture-only |
| VIEW-001 | Local/session UX state (selected/pinned Strategy Instance — KHÔNG persisted backend) | STATE-004 missing Strategy Instance; STATE-028/STATE-029 Paper-specific not-selected/not-pinned | Strategy Instance pin scoped theo Account/environment (PAPER/LIVE distinct, §8) | architecture-only |
| VIEW-002 | Workflow-visible computed result (non-authoritative per UC-003) + API transport state | STATE-001 loading (SCR-001 chỉ — VIEW-002 KHÔNG tự có STATE-001 riêng theo bảng blueprint); STATE-022/STATE-023/STATE-024 PASSED/FAILED/INDETERMINATE | Verification window scoped theo phiên hiện tại, KHÔNG cross-Account | architecture-only (computation/API binding established v0.4, §4.1/§13 gap #1 phần VIEW-002 RESOLVED — Research-session interval identity/evidence-completeness/correction-arrival mechanism VẪN Product-level gap, KHÔNG implementation-ready) |
| SCR-002 | Designated projection state (Replay Cursor-bounded reconstruction) | STATE-001 loading; STATE-006 Replay reference unavailable | Historical cursor scoped theo Account Boundary đã pin (§8) | architecture-only |
| VIEW-003 | Workflow-visible computed result (parity synthesis) | STATE-007/STATE-008 parity match/mismatch | Cùng cursor/Account scope với SCR-002 | identifier/component accounted for — technical realization NOT COMPLETE (synthesis binding blocked, §4.1/§13 gap #1 phần VIEW-003, VẪN unresolved) |
| SCR-003 | API transport state (command pending) | STATE-001 loading (KHÔNG liệt kê tường minh — chỉ SCR-001/002/003 theo bảng blueprint §11, SCR-003 CÓ trong danh sách ba screen); STATE-005 missing historical evidence | Backtest scoped theo Strategy Instance đã pin (§4 commit-gate) | architecture-only (API binding established v0.3, §4.1/§13 gap #2 RESOLVED) |
| SCR-004 | Designated projection/query-result state (Backtest run evidence, KHÔNG PAPER authority) | STATE-002 empty (chưa run nào); STATE-009 evidence insufficient; STATE-010 run identity unresolved | KHÔNG PAPER/LIVE environment field (Backtest scoped riêng, non-PAPER simulated authority) | architecture-only (API binding established v0.3, §4.1/§13 gap #2 RESOLVED) |
| SCR-005 | Designated projection/query-result state | STATE-002 empty (dưới 2 run); STATE-009 evidence insufficient | Cùng Backtest scope | architecture-only (API binding established v0.3, §4.1/§13 gap #2 RESOLVED) |
| SCR-006 | Command-pending state + authoritative backend state (RiskEvaluation/Order, sau khi confirm) | STATE-011 PAPER lineage unavailable; STATE-012/STATE-013/STATE-014 Risk APPROVED/REJECTED/NON_EVALUABLE; STATE-027 Live unauthorized; STATE-028/STATE-029 Paper Instance not selected/not pinned | `environment: PAPER` bất biến, exactly-one Account Boundary (ADR-012 §2.1); STATE-027 hiển thị Live Unauthorized global | architecture-only |
| SCR-007 | Authoritative backend state (Order/ExecutionResult/Fill) + designated projection state (Position) | STATE-002 empty (chưa Order/Fill); STATE-015/016 ExecutionResult; STATE-017 Fill absent; STATE-018/019/020/021 Position | `environment: PAPER`, cùng Account Boundary với SCR-006 | architecture-only |
| SCR-008 | Designated projection/evidence-record state (review-evidence-service, non-authoritative) | STATE-002 empty (chưa Fill/Position contribution) | Lineage trace scoped theo Account Boundary của Fill/Position nguồn | architecture-only |
| SCR-009 | Designated projection/evidence-record state | STATE-002 empty (chưa Replay Cursor đã chạy) | Cùng Account Boundary scope | architecture-only |
| VIEW-004 | Designated projection/evidence-record state (correction lineage) | (KHÔNG STATE-XXX riêng liệt kê tại blueprint §11 cho VIEW-004 — trace qua SCR-008/SCR-009 context) | Cùng Account Boundary scope | architecture-only |
| SCR-010 | Command-pending state → authoritative backend state (Strategy Definition Version) sau confirm | (KHÔNG STATE-XXX UX-level — validation nội dung thuộc strategy.md, ux-blueprint.md §7.6) | KHÔNG environment-specific (Strategy Definition Version là cross-environment identity) | architecture-only |
| VIEW-006 | Command-pending state → authoritative backend state (Strategy Instance) sau confirm | Registration unavailable khi thiếu version identity mới (ux-blueprint.md §7.6) | Instance registration scoped theo Account (khi tạo binding cho PAPER/Backtest scope liên quan) | architecture-only |
| SCR-011 | Designated projection/query-result state (comparison) | STATE-002 empty (dưới 2 Instance để so sánh) | Cross-version comparison, KHÔNG cross-Account (mỗi Instance vẫn giữ đúng Account Boundary riêng) | architecture-only (backtest-orchestrator portion established v0.3, §13 gap #2 RESOLVED; strategy-engine portion đã established trước đó) |
| VIEW-005 | Designated projection/evidence-record state (old-version, resolve độc lập hai family) | STATE-025 complete; STATE-026 partially unavailable | Cùng Account Boundary với Instance/version nguồn | architecture-only (Backtest-family portion established v0.3, §13 gap #2 RESOLVED; PAPER-family portion đã established trước đó) |

**Xác nhận tường minh (bắt buộc, v0.2 correction, đóng `P16-A-MIN-01`):** toàn bộ 17 SCR/VIEW ĐÃ trace — KHÔNG ID nào mồ côi, KHÔNG một screen/workflow/state/navigation path/user action nào bị invent ngoài `ux-blueprint.md` §6/§7. Identifier accounting (17/17 traced về đúng surface/component category) VÀ technical-realization completeness LÀ HAI khái niệm TÁCH BIỆT — mọi 17 ID ĐÃ trace; technical realization của SCR-003/SCR-004/SCR-005 (NAV-003, §13 gap #2) nay Established (v0.3, upstream prerequisite của `P16-A-MAJ-01` resolved qua Package 1.1 v0.8/Package 1.4 v0.5); VIEW-002 (§13 gap #1, phần VIEW-002) nay Established (v0.4, ADR-020 v0.1 Approved, `review-evidence-service` computation boundary); VIEW-003 (§13 gap #1, phần VIEW-003) VẪN KHÔNG COMPLETE — gap đó VẪN unresolved, KHÔNG chia sẻ resolution của VIEW-002 — KHÔNG tự invent một contract để lấp gap đó.

### 4.2 WS-001 — Ride Workspace Shell (supporting element, trace compact)

```text
WS-001 sở hữu ĐÚNG bốn item (ux-blueprint.md §5, v0.3 bounded — KHÔNG mở rộng): Current
  Account context (read-only, UC-011/PR-002); Instrument/Venue context (selector, UC-001/
  UC-011, PR-003); Strategy Instance context (hiển thị pin read-only, UC-002/UC-011,
  PR-001/PR-016); Historical cursor context (hiển thị khi ở SCR-002/SCR-009, UC-004/
  UC-017, PR-008/PR-012/PR-029). CỘNG STATE-027 (Live unauthorized, global).

Component classification: Application shell (§5) — container mức cao nhất, host toàn
  bộ NAV-001–006 destination bên trong nó.
API interaction: Query account-service (Account context); query strategy-engine
  (Strategy Instance context hiển thị); query replay-integration-service (Historical
  cursor context khi active). KHÔNG command riêng của WS-001 tự thân.
State classification: Local/session UX state (Account/Instrument-Venue/Strategy-
  Instance/cursor context đều LÀ hiển thị của giá trị đã resolve qua query, KHÔNG WS-001
  tự authoritative hoá).
Environment/Account boundary: Current Account context LÀ MỘT Account duy nhất (UX-INV-1,
  KHÔNG switcher — chưa UC/PR nào authorize).
Implementation status: architecture-only.
```

### 4.3 NAV-001–006 (supporting element, trace compact)

| ID | Destination (SCR/VIEW) | Required context | API interaction category | Non-bypass note (§7) |
|---|---|---|---|---|
| NAV-001 Research | SCR-001, VIEW-001, VIEW-002 | Không cần Strategy Instance để vào SCR-001 (entry-first) | Query market/analysis modules; query strategy-engine/account-service tại commit-gate; query `review-evidence-service` (VIEW-002 existence-check, v0.4, ADR-020 v0.1 Approved — route ĐÃ đăng ký, KHÔNG mới) | Route CHỈ qua API Surface — KHÔNG edge trực tiếp tới structure-engine/raw-regime-engine/feature-engine/context-aggregator/review-evidence-service (`ux-application-shell.forbidden_dependencies`, 14 entry, KHÔNG đổi) |
| NAV-002 Replay | SCR-002, VIEW-003 | Strategy Instance đã pin (VIEW-001→VIEW-002 PASSED) | Query replay-integration-service + authoritative stream tại cursor | Route CHỈ qua API Surface — KHÔNG edge trực tiếp tới replay-integration-service |
| NAV-003 Backtest | SCR-003, SCR-004, SCR-005 | Strategy Instance đã pin, cùng ràng buộc NAV-002 | **Established (v0.3, đóng upstream prerequisite của `P16-A-MAJ-01`)** — command/query `backtest-orchestrator` route ĐÃ established | Route CHỈ qua API Surface (đúng, KHÔNG đổi) — `command-query-api-surface → backtest-orchestrator` (registered edge, Package 1.1 v0.8 `Consolidated Stable`, ADR-019 v0.2 Approved alignment; elaborated tại API Architecture Package 1.4 v0.5 `Consolidated Stable` §9) nay LÀ route hợp lệ; query LÀ non-authoritative bounded Backtest run correlation view composed từ Decision (`decision-authority-service`)/RiskEvaluation (`risk-gateway`) fact ĐÃ tồn tại, authority KHÔNG đổi; run identity VẪN LÀ khái niệm correlation/grouping của ADR-018, KHÔNG entity/event/authoritative fact mới; `backtest-orchestrator.owns_authoritative_state` VẪN `deferred` (DD-001 CHƯA resolve, Package 1.1 §11) — KHÔNG resolve tại transaction này — §13 gap #2 RESOLVED, KHÔNG tự thêm edge/invent contract nào ngoài route ĐÃ registered |
| NAV-004 Paper | SCR-006, SCR-007 | Account context + Instrument/Venue + Strategy Instance pin CHO Paper (thứ tự riêng) | Command/query execution-engine/execution-result-processor/fill-processor/position-projection/risk-gateway | Route CHỈ qua API Surface — KHÔNG edge trực tiếp tới execution-engine/risk-gateway/execution-result-processor/fill-processor/position-projection |
| NAV-005 Review | SCR-008, SCR-009, VIEW-004 | Fill/Position contribution HOẶC Replay Cursor đã chạy (để mở trace cụ thể) | Query review-evidence-service | Route CHỈ qua API Surface — KHÔNG edge trực tiếp tới review-evidence-service |
| NAV-006 Improve | SCR-010, VIEW-006, SCR-011, VIEW-005 | Strategy Definition đã tồn tại (SCR-010); version mới (VIEW-006); ≥2 Instance (SCR-011) | Command/query strategy-engine; query backtest-orchestrator/execution chain (VIEW-005) | Route CHỈ qua API Surface — KHÔNG edge trực tiếp tới strategy-engine/decision-evaluation-engine/decision-authority-service |

### 4.4 FLOW-001–006 VÀ STATE-001–029 (supporting element, trace compact)

```text
FLOW-001 Primary end-to-end journey:      spans TOÀN BỘ sáu NAV — trace qua §4.3 trên,
  KHÔNG một component riêng (route sequencing LÀ ux-application-shell's navigation-frame
  concern, §5).
FLOW-002 Strategy Instance selection/pin:  trace tại VIEW-001 (§4.1) — local/session
  state, KHÔNG backend command.
FLOW-003 Backtest → Paper handoff:         judgment gate, KHÔNG hard handoff — trace tại
  SCR-004/SCR-005 → SCR-006 (§4.1), KHÔNG tự động chuyển Backtest Decision thành PAPER
  Decision (ux-blueprint.md §8 FLOW-003, nguyên văn, KHÔNG đổi).
FLOW-004 Paper execution initiation:       system-owned chain — trace tại SCR-006/SCR-007
  (§4.1), mandatory non-bypass Decision→Risk→Execution→Fill→Position (Package 1.3-D §3,
  KHÔNG đổi).
FLOW-005 Old-version evidence access:      trace tại SCR-011/VIEW-005 (§4.1).
FLOW-006 Improve → Research loop-back:     trace tại SCR-010/VIEW-006/VIEW-001/VIEW-002/
  SCR-001 (§4.1/§4.3).

Toàn bộ sáu FLOW-XXX ĐÃ trace về đúng SCR/VIEW/NAV sở hữu — KHÔNG flow nào mồ côi,
KHÔNG flow mới nào invent. Implementation status: architecture-only cho cả sáu.

STATE-001–029 (29 trạng thái presentation-only, ux-blueprint.md §11, UX-INV-9 — KHÔNG
domain state mới) — phân loại theo state model (§6) VÀ owning screen ĐÃ trace tại §4.1
(cột "Loading/empty/error/stale/unauthorized treatment"):
  API transport state:              STATE-001 (loading), STATE-002 (empty).
  Query-result/validation state:    STATE-003, STATE-004, STATE-005, STATE-006,
    STATE-009, STATE-010, STATE-011.
  Authoritative-backend-observed
    state (read-only presentation
    của fact ĐÃ authoritative):     STATE-012–STATE-017 (Risk/ExecutionResult/Fill).
  Designated-projection-observed
    state (non-authoritative,
    rebuildable):                   STATE-018/STATE-019/STATE-020/STATE-021 (Position),
    STATE-025/STATE-026
    (old-version evidence family).
  Workflow-visible computed state
    (non-authoritative synthesis,
    UC-003/UC-005 self-declared):   STATE-007/STATE-008 (parity), STATE-022/STATE-023/STATE-024
    (Research verification).
  Local/session UX state (KHÔNG
    backend query, session-scoped):  STATE-028/STATE-029 (Paper Strategy Instance selection/
    pin status).
  Static/config-level state
    (governance decision, KHÔNG
    query):                          STATE-027 (Live unauthorized — ADR-007, KHÔNG đổi).

Toàn bộ 29 STATE-XXX ĐÃ trace về đúng category VÀ owning screen tại ux-blueprint.md §11
— KHÔNG state nào mồ côi, KHÔNG state mới nào invent, KHÔNG concrete error code/UI copy
nào author (§10).
```

### 4.5 Xác nhận đầy đủ (bắt buộc, v0.2 correction, đóng `P16-A-MIN-01` — tách bạch identifier accounting khỏi technical-realization completeness)

```text
Identifier accounting (KHÔNG đổi, VẪN đầy đủ):
  17/17 SCR/VIEW traced về đúng owning surface/component category (§4.1).
  1/1 WS-001 traced (§4.2).
  6/6 NAV-001–006 traced (§4.3).
  6/6 FLOW-001–006 traced (§4.4).
  29/29 STATE-001–029 traced (§4.4).
  Tổng: 59/59 established UX identifier từ ux-blueprint.md ĐÃ represent VÀ trace về
    đúng UX surface/component category — KHÔNG identifier nào bị bỏ sót, KHÔNG
    identifier mới nào invent. Xác nhận này KHÔNG đổi bởi v0.2 correction.

Technical-realization completeness (v0.4 correction — CHƯA COMPLETE, phân biệt tường
  minh khỏi identifier accounting ở trên):
  17/17 SCR/VIEW có identifier/component placement; nay 16/17 có backend command/query
    binding ĐẦY ĐỦ established (KHÔNG blocked) — CHỈ 1/17 (VIEW-003) VẪN technically
    blocked pending upstream resolution (§13 gap #1, phần VIEW-003 của `P16-A-MAJ-02`).
  NAV-003 (Backtest) API-binding gap RESOLVED (v0.3, đóng upstream prerequisite của
    `P16-A-MAJ-01`) — SCR-003/SCR-004/SCR-005 VÀ phần backtest-orchestrator của
    SCR-011/VIEW-005 nay established qua route `command-query-api-surface →
    backtest-orchestrator` (Package 1.1 v0.8/Package 1.4 v0.5, `Consolidated Stable`)
    — §4.3.
  VIEW-002 computation ownership/API-binding gap RESOLVED (v0.4, đóng phần VIEW-002 của
    `P16-A-MAJ-02`) — VIEW-002 nay established qua route `command-query-api-surface →
    review-evidence-service` (Package 1.1 v0.9/Package 1.4 v0.6, `Consolidated Stable`,
    ADR-020 v0.1 Approved) — §4.1/§4.3. VIEW-003 KHÔNG chia sẻ resolution này — VẪN
    technically blocked, `P16-A-MAJ-02` KHÔNG đóng hoàn toàn.
  Package 1.6 KHÔNG claim complete acceptance-surface technical realization tại v0.4 —
    MỘT Major prerequisite còn lại (VIEW-003 synthesis ownership, §13 gap #1 phần
    VIEW-003) PHẢI resolve bởi transaction upstream riêng biệt (Domain Contract
    amendment + một ADR kế tiếp, ADR-020 §4/§12) TRƯỚC KHI technical-realization
    completeness đạt được (§14 Consolidation condition).
```

## 5. Component decomposition (bắt buộc, yêu cầu task — KHÔNG component code/framework API/file tree)

```text
Application shell:                    container mức cao nhất, host WS-001 (§4.2) — sở
                                       hữu global context bar (Account/Instrument-Venue/
                                       Strategy-Instance/cursor display) VÀ global nav
                                       bar (route tới sáu NAV-XXX).

Workspace/navigation frame:            điều phối route giữa sáu NAV-001–006 destination
                                       (§4.3) — sở hữu FLOW-001's sequencing concern,
                                       KHÔNG business logic.

Route/surface container:              container cho mỗi SCR/VIEW cụ thể (§4.1 cột
                                       "Component/container responsibility") — chịu
                                       trách nhiệm mount đúng query-bound view/command
                                       interaction component bên trong, xử lý STATE-001/
                                       STATE-002 transport-level presentation.

Query-bound view component:           component render dữ liệu đọc-CHỈ từ API Surface
                                       query (SCR-001/SCR-002/SCR-004/SCR-005/SCR-007/
                                       SCR-011, §4.1) — KHÔNG tự authoritative hoá dữ liệu
                                       nhận được, KHÔNG recompute (§3).

Command interaction component:        component xử lý user-initiated action emit command
                                       (VIEW-001 pin — local; SCR-003/SCR-006/SCR-010/
                                       VIEW-006, §4.1) — phân biệt trực quan user action
                                       khỏi system-owned action (UX-P-2, ux-blueprint.md
                                       §3, KHÔNG đổi).

Evidence/review presentation
  component:                          component chuyên biệt cho non-authoritative
                                       evidence display (SCR-008/SCR-009/VIEW-004/
                                       VIEW-005, §4.1/§9) — PHẢI mang nhãn mode
                                       (Research/Replay/Backtest/Paper) VÀ authority
                                       status (UX-P-1, ux-blueprint.md §3, KHÔNG đổi),
                                       PHẢI hiển thị correction lineage tường minh
                                       (UX-INV-6).

Environment/account context boundary: component/wrapper đảm bảo mọi query-bound VÀ
                                       command interaction component bên trong nó CHỈ
                                       thao tác trong đúng environment (PAPER/LIVE) VÀ
                                       Account Boundary đã pin (§8) — KHÔNG cross-
                                       boundary leakage.

Shared non-authoritative presentation
  utility:                             utility dùng chung (label formatting, mode-badge
                                       rendering theo UX-P-1, state-treatment rendering
                                       theo §4.4 category) — KHÔNG business logic, KHÔNG
                                       authoritative computation, CHỈ presentation-layer
                                       formatting của giá trị đã nhận từ query.
```

**Xác nhận tường minh:** tám classification trên LÀ Package 1.6 technical classification ở mức kiến trúc — KHÔNG một module registry mới (Chapter 7 §7.5 VẪN authority DUY NHẤT cho module identity/taxonomy), KHÔNG component code, KHÔNG framework API (component/hook/directive cụ thể), KHÔNG file tree nào được author tại §5.

## 6. State model (bắt buộc, yêu cầu task — KHÔNG invent frontend persistence authority)

```text
Authoritative backend state:          Decision/Trade Intent/RiskEvaluation/Execution
                                       Intent/Order/ExecutionResult/Fill/Account —
                                       resolve TRỰC TIẾP từ query, KHÔNG BAO GIỜ cache
                                       lâu dài như thể một second source of truth (I-12,
                                       KHÔNG đổi).

Designated projection state:          Position (position-projection), review-evidence-
                                       service output, old-version evidence family —
                                       hiển thị KÈM marker non-authoritative tường minh
                                       (§3, §9), rebuild được từ authoritative input
                                       (Chapter 7 §7.4, KHÔNG đổi).

API transport state:                  loading/pending/network-condition (STATE-001) VÀ
                                       empty-result (STATE-002) — thuần transport-layer,
                                       KHÔNG domain semantics (§4.4).

Local ephemeral UI state:             Strategy Instance pin (VIEW-001, session-scoped,
                                       KHÔNG PaperSession entity — ux-blueprint.md §3,
                                       KHÔNG đổi); form input trước khi command emit;
                                       navigation/route position; STATE-028/STATE-029.

Persisted user preference (CHỈ nơi
  upstream semantics established):    ux-blueprint.md KHÔNG establish một user-
                                       preference persistence semantic nào tại v0.5 hiện
                                       tại — Package 1.6 KHÔNG invent một preference
                                       persistence mechanism mới; nếu tương lai
                                       ux-blueprint.md thêm semantic đó, Package 1.6 sẽ
                                       cần một correction transaction riêng.

Stale/loading/error/unknown state:    §4.4 category "API transport state" (loading/
                                       empty) + §10 (validation/domain/processing
                                       failure, unknown outcome) — PHẢI phân biệt được
                                       tường minh, KHÔNG collapse thành một generic
                                       "error".

Command pending VÀ unresolved
  authoritative outcome:               sau command emit (SCR-006/SCR-010/VIEW-006), UX
                                       PHẢI giữ trạng thái "pending" tách biệt khỏi bất
                                       kỳ authoritative outcome nào cho tới khi API
                                       Surface/module authoritative trả về outcome xác
                                       nhận — cùng nguyên tắc UNKNOWN_OUTCOME đã pin
                                       (Package 1.2 §4a.5/§4a.9, Package 1.4 §3) áp dụng
                                       ĐỒNG NHẤT: UX KHÔNG BAO GIỜ tự diễn giải pending
                                       thành success/failure.
```

**Xác nhận tường minh bắt buộc:** UX state KHÔNG BAO GIỜ overwrite, merge, hay replace authoritative source truth — mọi authoritative/projection state hiển thị PHẢI resolve lại từ query MỖI KHI cursor/version yêu cầu thay đổi (cùng nguyên tắc "KHÔNG mutable-latest substitution" đã pin tại Package 1.4 §8/Package 1.5 §6, KHÔNG đổi). Package 1.6 KHÔNG invent một frontend persistence authority mới (vd. một local database, offline-first authoritative cache) — mọi persistence authority thật sự VẪN thuộc Package 1.5 boundary, KHÔNG đổi.

## 7. API binding (bắt buộc, yêu cầu task — KHÔNG field-level API schema)

```text
Toàn bộ UX data VÀ command CHỈ bind qua `command-query-api-surface` — registry fact
  (§2.1 `depends_on`) LÀ edge DUY NHẤT được phép; UX consume `query` VÀ emit `command`
  ĐÚNG như đã đăng ký (§2.1 `consumes`/`emits`), KHÔNG field mới nào thêm.

KHÔNG direct engine/projection/evidence-service/custody/signing access: `ux-application-
  shell.depends_on` (§2.1) KHÔNG chứa bất kỳ module nào trong số đó — decision-authority-
  service, risk-gateway, execution-engine, execution-result-processor, fill-processor,
  position-projection, replay-integration-service, review-evidence-service ĐỀU nằm
  trong `forbidden_dependencies` (§2.1, 14 entry) — cấm tường minh; custody-signing-
  service VÀ exchange-adapter KHÔNG nằm trong `depends_on` CỦA CẢ ux-application-shell
  LẪN command-query-api-surface (Package 1.4 §2.1/§6, Consolidated Stable, KHÔNG đổi) —
  hai lớp absence-of-edge kết hợp xác nhận UX KHÔNG có route hợp lệ nào tới custody/
  signing (§8 dưới).

API validation/transport acceptance KHÔNG PHẢI business acceptance: cùng nguyên tắc đã
  pin tại Package 1.4 §3 (KHÔNG đổi) — UX Shell nhận response transport-thành-công
  KHÔNG ngụ ý command đó ĐÃ được authoritative module chấp nhận; UX PHẢI phân biệt
  tường minh hai trạng thái này trong mọi presentation (§6, §10).

Cursor, version, freshness, provenance, correlation, VÀ environment evidence PHẢI bảo
  toàn: mọi evidence Package 1.4 §4/§8 đã yêu cầu API Surface preserve (cursor/version/
  freshness khi expose query, correlation/idempotency identity khi relay command) PHẢI
  được UX forward nguyên vẹn trong presentation — KHÔNG strip, KHÔNG thay bằng "latest"
  ngầm định (cùng nguyên tắc KHÔNG mutable-latest, §6).

Unknown hay unresolved outcome VẪN unresolved cho tới khi authoritative owner resolve:
  UX KHÔNG BAO GIỜ tự diễn giải một UNKNOWN_OUTCOME/pending state thành success/failure
  (§6) — chờ đúng module authoritative reconcile (Package 1.2 §4a.9, KHÔNG đổi).

KHÔNG field-level API schema nào được author tại §7 — mọi mục trên là YÊU CẦU
  architecture-level (WHAT phải đúng), KHÔNG concrete request/response shape.

Traceability/API-binding gap (bắt buộc ghi nhận thay vì invent contract, đúng yêu cầu
  task): một trường hợp còn lại tại §4.1 (VIEW-003 synthesis-layer, parity match/
  mismatch) LÀ gap KHÔNG resolve tại Package 1.6 — carry forward §11; VIEW-003 KHÔNG
  chia sẻ computation/route của VIEW-002. NAV-003 Backtest binding gap
  (`backtest-orchestrator` trong `command-query-api-surface.depends_on`) ĐÃ RESOLVED
  (v0.3) — `backtest-orchestrator` nay LÀ registered edge (`module-registry.yaml` v0.8,
  elaborated tại `api-architecture.md` v0.5 §9), KHÔNG còn một traceability/API-binding
  gap. VIEW-002 Research verification binding gap ĐÃ RESOLVED (v0.4, ADR-020 v0.1
  Approved) — `review-evidence-service` nay LÀ computation boundary qua route ĐÃ đăng
  ký (`module-registry.yaml` v0.9, elaborated tại `api-architecture.md` v0.6 §9), KHÔNG
  còn một traceability/API-binding gap cho VIEW-002.
```

## 8. Non-bypass và forbidden dependencies (bắt buộc, yêu cầu task)

```text
Xác nhận tường minh (bắt buộc, yêu cầu task — đúng nguyên tắc đã bounded-correct tại
  Package 1.4 §6, v0.2/v0.3, KHÔNG lặp lại lỗi over-claim đó): `forbidden_dependencies`
  (§2.1, 14 entry) VÀ `depends_on` (§2.1, đúng một edge) LÀ prerequisite/prohibition
  relation ở mức registry — chúng xác nhận KHÔNG có registered direct module
  prerequisite nào ngoài `command-query-api-surface`, NHƯNG graph shape đó, TỰ THÂN,
  KHÔNG PHẢI một complete caller/access-control proof — non-bypass đầy đủ PHẢI dựa
  thêm vào invariant kiến trúc bên dưới VÀ authority/eligibility validation thật sự
  được thực thi tại module authoritative (§3/§7, Package 1.4 §3/§6 — KHÔNG đổi).

Positive invariant bắt buộc (bốn mục):
  1. Mọi backend query/command PHẢI đi qua command-query-api-surface — KHÔNG route
     nào khác được UX author/invoke.
  2. UX KHÔNG THỂ trực tiếp invoke engine (decision-authority-service/risk-gateway/
     execution-engine/execution-result-processor/fill-processor), projection
     (position-projection/replay-integration-service/context-aggregator), Review
     Evidence Service, hay custody/signing/venue-adapter module nào — cả registry
     `forbidden_dependencies` (14 entry, tường minh) LẪN absence-of-edge tổng thể
     (§7, custody/signing/exchange-adapter KHÔNG có edge ở CẢ HAI tầng UX VÀ API
     Surface) đều xác nhận.
  3. Transport (API request/response) KHÔNG BAO GIỜ tự tạo Decision/Risk/Execution/
     signing authorization — cùng nguyên tắc "transport KHÔNG BAO GIỜ tự thân là
     authority" đã pin xuyên suốt Package 1.2/1.3-D/1.4/1.5 (KHÔNG đổi), áp dụng
     ĐỒNG NHẤT cho UX transport layer.
  4. Invalid, stale, unauthorized, hay causally-unrelated action PHẢI fail an toàn
     (I-6 Fail-Safe by Scope, Chapter 2, Locked) — UX PHẢI relay đúng fail-closed
     outcome từ authoritative boundary, KHÔNG tự override thành một trạng thái
     "thành công giả định".
```

## 9. Environment và Account Boundary (bắt buộc, yêu cầu task — KHÔNG author LIVE activation UX)

```text
PAPER VÀ LIVE distinction bảo toàn: `environment` (PAPER|LIVE, bất biến, account.md
  §8/ADR-012 §2.4, KHÔNG đổi) LÀ trục hiển thị bắt buộc tại mọi screen liên quan
  execution (SCR-006/SCR-007, §4.1) — UX KHÔNG trộn lẫn hai scope.

LIVE VẪN Unauthorized: STATE-027 (ux-blueprint.md §11, "Live unauthorized") LÀ static/
  config-level presentation (§4.4) — UX PHẢI hiển thị trạng thái này TẠI WS-001 (global)
  VÀ SCR-006, KHÔNG action/screen/label nào ngụ ý Live khả dụng (UX-INV-10, ux-blueprint.md
  §3, KHÔNG đổi).

Immutable environment/account reference (nơi đã established): `account_boundary_ref`
  (ADR-012 §2.1, exactly-one-boundary) VÀ Account identity (account-service, Package
  1.2 §4) LÀ bất biến — UX Shell CHỈ hiển thị giá trị đã resolve, KHÔNG tự tạo/đổi một
  reference mới.

KHÔNG cross-account hay cross-environment state leakage: mọi query-bound/command
  interaction component (§5) PHẢI scoped đúng environment/Account Boundary context đã
  pin (§4.1 cột "Environment/Account boundary") — component "environment/account context
  boundary" (§5) chịu trách nhiệm enforce ranh giới này ở mức kiến trúc.

Visible environment indication (nơi UX Blueprint yêu cầu): Current Account context
  (WS-001, §4.2, UX-INV-1) VÀ environment field tại SCR-006/SCR-007 LÀ hiển thị BẮT
  BUỘC — Package 1.6 KHÔNG bớt yêu cầu này.

KHÔNG hidden transition từ research/replay/backtest/PAPER sang LIVE: FLOW-001 (§4.4,
  ux-blueprint.md §8, nguyên văn) xác nhận "Live KHÔNG phải một bước — chỉ nhắc như
  lifecycle boundary bị hoãn... KHÔNG NAV/SCR nào dẫn tới Live" — Package 1.6 KHÔNG
  author một LIVE activation UX path nào, KHÔNG thêm route/screen/state mới hướng tới
  LIVE.
```

## 10. Review, replay, và evidence surfaces (bắt buộc, yêu cầu task)

```text
Review Evidence Service VẪN non-authoritative: `review-evidence-service.owns_
  authoritative_state: false` (Package 1.5 §2.2, Consolidated Stable, KHÔNG đổi) — SCR-008/
  SCR-009/VIEW-004 (§4.1) PHẢI hiển thị marker non-authoritative tường minh cho MỌI
  evidence từ module này (§5 "Evidence/review presentation component").

Position LÀ projection evidence, KHÔNG authoritative truth: SCR-007's Position display
  (STATE-018/019/020/021, §4.1/§4.4) PHẢI mang marker "derived/rebuildable projection" — cùng
  nguyên tắc bắt buộc đã pin tại Package 1.5 §2.2/§8 (P15-A-MAJ-02 correction, KHÔNG đổi).

Correction lineage, provenance, VÀ incomplete-evidence marker VẪN hiển thị: UX-INV-6
  (mọi correction hiển thị CẢ fact gốc LẪN fact thay thế, liên kết tường minh) VÀ
  UX-INV-4 (mọi Decision/Risk Action hiển thị PHẢI kèm evidence trace truy cập được)
  ÁP DỤNG tường minh tại VIEW-004/SCR-008 (§4.1) — Package 1.6 KHÔNG bớt yêu cầu này;
  incomplete-evidence PHẢI đánh dấu tường minh (STATE-026, cùng nguyên tắc Package 1.5
  §4 "fail closed/trả về explicit evidence unavailable marker").

Replay/backtest/PAPER outcome VẪN tách biệt: SCR-002 (Replay), SCR-003/004/005
  (Backtest, non-PAPER simulated authority, `backtest-orchestrator.forbidden_
  dependencies` loại trừ execution-engine/paper-execution-boundary/execution-result-
  processor/fill-processor/position-projection — Package 1.1, KHÔNG đổi), VÀ SCR-006/
  SCR-007 (PAPER, `environment: PAPER`) LÀ BA scope tách biệt cấu trúc — UX KHÔNG trộn
  lẫn evidence giữa ba scope này trong bất kỳ presentation nào.

UX KHÔNG được silently collapse correction history thành mutable latest: cùng nguyên
  tắc "KHÔNG mutable-latest substitution" (§6, Package 1.4 §8/Package 1.5 §6, KHÔNG
  đổi) — mọi historical/correction view PHẢI resolve đúng cursor/slice đã yêu cầu.

Package 1.5 contract-category interaction gap VẪN unresolved, KHÔNG fixed tại UX: gap
  đã ghi nhận tại Package 1.5 §4/§11 (Consolidated Stable, KHÔNG đổi) — review-evidence-
  service's cơ chế lấy output từ position-projection/replay-integration-service (hai
  query-emitting dependency) dưới `consumes: [event]` của chính nó CHƯA fully
  established. SCR-008/SCR-009/VIEW-004 (§4.1) kế thừa gap này NGUYÊN VẸN — Package 1.6
  KHÔNG tự invent một cơ chế mới để "sửa" gap đó (vd. UX tự query trực tiếp position-
  projection để bù đắp — bị CẤM tường minh, §7/§8), CHỈ ghi nhận evidence từ review-
  evidence-service CÓ THỂ incomplete cho tới khi Package 1.5 gap resolve (§11).
```

## 11. Failure và interaction semantics (bắt buộc, yêu cầu task — KHÔNG concrete error code/retry algorithm/UI copy mới)

Mười category PHẢI phân biệt được ở mức architecture (KHÔNG concrete implementation, transcribe/technical-realize CHỈ những gì `ux-blueprint.md` đã bounded):

```text
Loading:                    STATE-001 (§4.4) — API transport pending.
Empty:                      STATE-002 (§4.4) — query trả về collection/record rỗng
                             genuine, KHÔNG unfilled-form.
Stale:                      cursor/version đã yêu cầu KHÔNG còn hiệu lực tại thời điểm
                             hiển thị — PHẢI fail closed (I-6), cùng nguyên tắc Package
                             1.4 §7/Package 1.5 §10.
Unavailable:                STATE-005/006/009/010/011 (§4.4) — nguồn evidence KHÔNG
                             resolve được.
Unauthorized:                STATE-027 (Live unauthorized, §4.4/§9) — governance-level,
                             KHÔNG action nào bị chặn bởi missing user permission model
                             (RBAC/IAM CHƯA established, Package 1.1 §11 gap, KHÔNG
                             resolve tại Package 1.6).
Validation rejection:        transport/structural rejection TRƯỚC KHI chạm authoritative
                             module (cùng category "Validation failure" đã pin tại
                             Package 1.4 §7, KHÔNG đổi).
Domain rejection:            authoritative module TỰ NÓ decline (vd. STATE-013 Risk
                             REJECTED, §4.4) — UX CHỈ relay, KHÔNG tự phát sinh.
Processing failure:          authoritative module nhận request hợp lệ NHƯNG xử lý thất
                             bại phía nó (vd. STATE-016 ExecutionResult NOT_EXECUTED)
                             — UX CHỈ relay.
Unknown/unresolved outcome:  command pending chưa xác nhận (§6) — UX PHẢI relay đúng
                             category này, KHÔNG BAO GIỜ tự diễn giải thành success/
                             failure.
Partial/unverifiable
  evidence:                  STATE-026 (old-version evidence partially unavailable, §4.1/
                             §10) — UX PHẢI đánh dấu tường minh, KHÔNG present như đầy đủ.
```

**Xác nhận tường minh:** KHÔNG error code, retry algorithm, hay UI copy MỚI nào được author tại §11 ngoài những gì `ux-blueprint.md` đã tường minh bounded (§11 "bốn nguyên tắc fallback" — workflow stops/state remains observable/reason is disclosed/no downstream authoritative action occurs, nguyên văn, KHÔNG đổi).

## 12. Accessibility, responsiveness, và presentation constraints (bắt buộc, yêu cầu task — CHỈ transcribe/technical-realize constraint đã established)

```text
Xác nhận tường minh (bắt buộc, yêu cầu task): `ux-blueprint.md` (Package 0.3-C,
  Consolidated Stable) KHÔNG establish một accessibility acceptance rule, breakpoint,
  design token, hay branding rule cụ thể nào tại v0.5 hiện tại (§1–§18 đã đọc đầy đủ,
  KHÔNG section nào định nghĩa các mục này). Package 1.6 KHÔNG tự invent pixel value,
  design token, branding rule, breakpoint, hay accessibility acceptance rule nào KHÔNG
  có nguồn upstream — đúng non-goal đã pin tại phase-1-plan.md §"Package 1.6" (KHÔNG
  pixel-level design).

UX-P-1 through UX-P-5 (ux-blueprint.md §3) VÀ UX-INV-1 through UX-INV-10 (§3) LÀ
  presentation-CONSTRAINT ở mức semantic (mode label, action/system-action distinction,
  reason disclosure, entity-existence honesty, read-only/authoritative separation) —
  Package 1.6 technical-realize CHÚNG qua component classification (§5) VÀ state
  treatment (§4.1/§4.4), KHÔNG thêm constraint mới ngoài mười lăm mục đã pin.

Gap ghi nhận (technical realization đòi hỏi upstream decision, KHÔNG resolve tại
  Package 1.6): accessibility acceptance criteria cụ thể (WCAG level, keyboard nav
  requirement, screen-reader requirement); responsive breakpoint; design token/branding
  system — TẤT CẢ carry forward như gap tới một future ux-blueprint.md correction hoặc
  Package 1.6 correction transaction, KHÔNG tự quyết tại v0.1/v0.2 này.

Xác nhận tường minh (bắt buộc, v0.2 correction, đóng `P16-A-MIN-02`): Package 1.6 CHỈ
  được phép technical-realize accessibility/responsiveness/design-token requirement ĐÃ
  established bởi Product/UX authority (`ux-blueprint.md`, Package 0.3-C) — Package 1.6
  KHÔNG THỂ, VÀ KHÔNG được phép, tự establish một WCAG target, breakpoint semantic,
  branding rule, hay design-token acceptance requirement nào, dù thông qua một bounded
  correction transaction như v0.2 này. Thiết lập những yêu cầu đó ĐÒI HỎI một governed
  upstream Product/UX decision TRƯỚC (vd. một `ux-blueprint.md` correction transaction
  với thẩm quyền Product Owner tương ứng), HOẶC một transaction khác được tường minh
  authorize để update controlling source đó — KHÔNG PHẢI một Package 1.6 correction tự
  quyết. Package 1.6 KHÔNG BAO GIỜ được phép silently trở thành UX acceptance-semantics
  authority — vai trò đó VẪN thuộc Product/UX layer, KHÔNG Package 1.6.
```

## 13. Preserved gaps and non-goals (bắt buộc, yêu cầu task)

**Gap ghi nhận tại Package 1.6 (v0.2 correction cập nhật khung ngôn ngữ cho gap #1/#2,
đóng `P16-A-MAJ-01`/`P16-A-MAJ-02`; gap #3 qualify thêm, đóng `P16-A-MIN-02`; v0.3
correction RESOLVE gap #2 qua upstream Package 1.1 v0.8/Package 1.4 v0.5, đóng
upstream prerequisite của `P16-A-MAJ-01`; v0.4 correction RESOLVE phần VIEW-002 của
gap #1 qua Approved ADR-020 v0.1 VÀ upstream Package 1.1 v0.9/Package 1.4 v0.6 —
`P16-A-MAJ-02` KHÔNG đóng hoàn toàn, phần VIEW-003 của gap #1 VÀ gap #3 VẪN
unresolved):**

```text
1a. VIEW-002 computation-owner/contract gap (§3/§4.1, RESOLVED v0.4, đóng phần
   VIEW-002 của `P16-A-MAJ-02`): PASSED/FAILED/INDETERMINATE (VIEW-002, UC-003) LÀ
   non-authoritative output ĐÃ tự xác nhận bởi UC-003 — Approved [ADR-020](../adr/ADR-020.md)
   v0.1 quyết định `review-evidence-service` LÀ computation boundary duy nhất, qua route
   `ux-application-shell → command-query-api-surface → review-evidence-service` (route
   ĐÃ đăng ký, KHÔNG edge/contract-category mới — bốn module nguồn ĐÃ CÓ trong
   `review-evidence-service.depends_on`, Package 1.1 v0.9). `review-evidence-service`
   CHỈ thực hiện existence-check (KHÔNG tái tính toán Decision/Risk/Execution logic,
   KHÔNG append/replace/sở hữu fact nguồn, KHÔNG author entity/event authoritative mới)
   — `owns_authoritative_state: false` KHÔNG đổi. Ba missing semantic item Product-level
   (Research-session interval identity mechanism, evidence-completeness determination
   mechanism, correction-arrival-during-window handling) VẪN unresolved — Package 1.6
   KHÔNG resolve, KHÔNG trình bày VIEW-002 như implementation-ready.
1b. VIEW-003 synthesis owner/contract gap (§3/§4.1, TECHNICALLY BLOCKED, VẪN unresolved,
   phần VIEW-003 của `P16-A-MAJ-02`): parity match/mismatch (VIEW-003, UC-005) LÀ
   non-authoritative output ĐÃ tự xác nhận bởi UC-005 — NHƯNG một non-authoritative
   output VẪN đòi hỏi một computation owner VÀ contract đã established. KHÔNG module
   registry nào (`ux-application-shell`, `command-query-api-surface`, hay module khác,
   BAO GỒM `review-evidence-service`) hiện sở hữu computation này tường minh — VIEW-003
   KHÔNG chia sẻ resolution của VIEW-002 (1a trên), computation của hai VIEW này khác
   biệt về bản chất (existence-check vs. recomputation-và-so-sánh). Package 1.6 KHÔNG
   chọn client-side/API-side, KHÔNG cấp một "exception" nào cho UX tự thực hiện — VIEW-003
   binding VẪN technically blocked cho tới khi (a) `canonical semantic-decision hash`
   (decision.md, Package 0.2-C4) được định nghĩa VÀ (b) một Product Owner quyết định về
   INDETERMINATE-equivalent outcome cho VIEW-003 VÀ (c) một ADR kế tiếp/độc lập chọn
   computation owner — CẢ BA prerequisite này (ADR-020 §4/§12, scope conflict tường
   minh) PHẢI resolve TRƯỚC. Route tương lai VẪN cùng hình dạng ba tầng
   `ux-application-shell → command-query-api-surface → [module TBD]` — module cụ thể
   CHƯA chọn.
2. NAV-003 Backtest API-binding gap (§4.3/§4.1, RESOLVED v0.3): `backtest-orchestrator`
   nay LÀ registered edge trong `command-query-api-surface.depends_on` (module-
   registry.yaml v0.8, ADR-019 v0.2 Approved alignment; elaborated tại api-
   architecture.md v0.5 §9, cả hai `Consolidated Stable`) — route API cho Backtest
   command/query ĐÃ tồn tại. Upstream registry/API-alignment prerequisite (thẩm quyền
   Package 1.1/Package 1.4) ĐÃ được thiết lập bởi transaction governed riêng biệt,
   TRƯỚC transaction v0.3 này — NAV-003/SCR-003/SCR-004/SCR-005 (VÀ phần
   backtest-orchestrator của SCR-011/VIEW-005) nay đạt technical-realization
   establishment (§4.1). Package 1.6 KHÔNG tự thêm dependency edge nào ngoài route ĐÃ
   registered, KHÔNG tự invent contract; `backtest-orchestrator.owns_authoritative_state`
   VẪN `deferred` (DD-001, Package 1.1 §11) — KHÔNG resolve tại transaction này (xem
   carry-forward gap dưới).
3. Accessibility/responsiveness/design-token gap (§12, qualified v0.2): `ux-blueprint.md`
   KHÔNG establish constraint cụ thể — technical realization đòi hỏi một governed
   upstream Product/UX decision (`ux-blueprint.md` correction hoặc transaction khác
   được tường minh authorize update controlling source) TRƯỚC. Package 1.6 KHÔNG THỂ
   tự establish những yêu cầu đó qua bất kỳ correction transaction nào, KHÔNG được
   silently trở thành UX acceptance-semantics authority.
```

**Carry forward nguyên vẹn từ upstream (KHÔNG resolve tại Package 1.6):**

```text
Kill-switch authoritative-state ownership — VẪN unresolved (Package 1.3-D §16).
In-flight signing/revocation behavior — VẪN unresolved (Package 1.2 §4a.9).
LIVE Domain Contract (Execution Engine ↔ Exchange Adapter) — VẪN CHƯA author.
DD-003, DD-001 — VẪN Deferred (backtest-orchestrator's `owns_authoritative_state:
  deferred` — KHÔNG resolve tại Package 1.6; binding path SCR-003/004/005 (§4.1)
  established v0.3 qua route ĐÃ registered, NHƯNG authoritative-state classification
  của Backtest run evidence VẪN chờ DD-001, KHÔNG bị thay đổi bởi route establishment).
Exchange Adapter elaborating package assignment — VẪN unresolved.
Package 1.5 contract-category interaction gap VÀ retention/deletion ownership gap —
  VẪN unresolved (§10, KHÔNG fixed tại UX).
RBAC/Access Control Model — VẪN Open/Partially Resolved (OQ-001, Package 1.1 §11) —
  ảnh hưởng trực tiếp "Unauthorized" treatment tại §11, KHÔNG resolve tại Package 1.6.
```

**Non-goals riêng của Package 1.6 (KHÔNG author tại transaction này):**

```text
React/Vue/Svelte, hay bất kỳ frontend framework choice nào.
Component source code.
CSS/design-system implementation.
Pixel-perfect layout.
Field-level API schema (request/response shape cụ thể).
Product/UX behavior MỚI ngoài ux-blueprint.md đã Consolidated Stable — KHÔNG screen/
  flow/state/navigation path/user action mới nào invent.
Authentication implementation cụ thể.
Database persistence design (thẩm quyền Package 1.5, KHÔNG Package 1.6).
Custody implementation (thẩm quyền Package 1.2, KHÔNG Package 1.6).
Backend orchestration (thẩm quyền Package 1.3-C/1.3-D, KHÔNG Package 1.6).
Bất kỳ registry change nào (`module-registry.yaml`/`system-decomposition.md` KHÔNG sửa).
Bất kỳ dependency edge, capability, context, hay authority mới nào ngoài `module-
  registry.yaml` v0.9 đã đăng ký.
Package 1.5 gap resolution (§10/§13, carry forward).
KHÔNG tạo/approve ADR tại transaction này.
KHÔNG mark Package 1.6 Consolidated Stable.
KHÔNG tuyên bố Phase 1 hoàn thành, KHÔNG mở Gate 2/Phase 2, KHÔNG authorize Live.
```

## 14. Review and consolidation conditions

```text
Review A scope:               Mọi SCR/VIEW/WS/NAV/FLOW/STATE trace được về component
                               architecture (§4, đúng phase-1-plan.md) — KHÔNG mồ côi,
                               KHÔNG invent UX behavior mới ngoài ux-blueprint.md; module
                               boundary (§2) nhất quán với module-registry.yaml v0.9
                               (Consolidated Stable) — KHÔNG dependency edge mới nào bị
                               invent ngoài route `command-query-api-surface →
                               backtest-orchestrator` ĐÃ registered (v0.3) VÀ route
                               `command-query-api-surface → review-evidence-service` ĐÃ
                               registered (v0.4, VIEW-002 capability MỚI qua edge ĐÃ CÓ
                               SẴN — KHÔNG edge mới); §8 non-bypass claim KHÔNG
                               over-claim graph shape như complete proof (đúng bài học
                               Package 1.4 P14-A-MAJ-01); gap còn lại (§13 gap #1 phần
                               VIEW-003) ghi nhận trung thực, KHÔNG silently resolved
                               bằng một invented contract.
Independent Review B
  scope:                      Độc lập xác nhận data-binding (§7) khớp đúng API
                               Architecture (Package 1.4 v0.6, Consolidated Stable)
                               contract surface — KHÔNG tự phát minh contract riêng (đúng
                               phase-1-plan.md Independent Review B scope cho Package
                               1.6); xác nhận Position/review-evidence-service treatment
                               (§10) khớp đúng Package 1.5 §2.2/§8 non-authoritative
                               status; xác nhận VIEW-002's existence-check treatment
                               (§4.1) khớp đúng ADR-020 v0.1 (Approved)/api-architecture.md
                               v0.6 §9 — KHÔNG recompute/authority claim nào invent; xác
                               nhận LIVE Unauthorized/PAPER-LIVE separation (§9) KHÔNG bị
                               đổi.
Product Owner decision
  point:                      Sau Review A/B CLEAN VÀ sau khi prerequisite còn lại dưới
                               đây resolve.
Consolidation condition
  (v0.4 correction — phần
  VIEW-002 của gap #1
  RESOLVED, đóng phần
  VIEW-002 của `P16-A-MAJ-02`;
  v0.3 correction — gap #2
  RESOLVED, đóng upstream
  prerequisite của
  `P16-A-MAJ-01`; v0.2
  correction đóng
  `P16-A-MIN-01` — tách bạch
  identifier accounting khỏi
  technical-realization
  completeness — vẫn áp
  dụng):                       Zero unresolved Blocker/Major trên baseline hiện tại
                               (v0.4, post bounded correction đóng phần VIEW-002 của
                               P16-A-MAJ-02; P16-A-MAJ-01/P16-A-MIN-01/P16-A-MIN-02 vẫn
                               tại trạng thái đã đóng trước đó); Package 1.4
                               Consolidated Stable (ĐÃ thỏa, v0.6); TOÀN BỘ 59/59
                               identifier ĐÃ trace về đúng component category (§4.5,
                               identifier accounting — ĐÃ thỏa) — NHƯNG "component
                               tương ứng" KHÔNG tự động nghĩa là "technical-realization
                               HOÀN TẤT": Package 1.6 KHÔNG đạt consolidation readiness
                               cho tới khi prerequisite còn lại sau resolve bởi
                               transaction upstream governed riêng biệt (KHÔNG Package
                               1.6 tự resolve):
                                 (a) NAV-003 Backtest API-binding (`P16-A-MAJ-01`, §13
                                     gap #2) — route command-query-api-surface →
                                     backtest-orchestrator ĐÃ established (v0.3,
                                     RESOLVED — Package 1.1 v0.8/Package 1.4 v0.5);
                                 (b) VIEW-002 computation owner/contract (§13 gap #1
                                     phần VIEW-002) — ĐÃ established (v0.4, RESOLVED —
                                     ADR-020 v0.1 Approved, Package 1.1 v0.9/Package 1.4
                                     v0.6);
                                 (c) VIEW-003 synthesis owner/contract (`P16-A-MAJ-02`
                                     phần VIEW-003, §13 gap #1) — computation owner PHẢI
                                     established, chờ Domain Contract amendment
                                     (`canonical semantic-decision hash`) VÀ một ADR kế
                                     tiếp — VẪN unresolved.
                               Đúng phase-1-plan.md Consolidation condition cho Package
                               1.6, diễn giải nghiêm ngặt hơn: "toàn bộ acceptance
                               surface có component tương ứng" ĐÃ thỏa (identifier
                               accounting), NHƯNG "Zero unresolved Blocker/Major" CHƯA
                               thỏa cho tới khi (c) resolve.
```

## 15. Lifecycle treatment

```text
Package 1.6:
  version: 0.4
  status: Draft
  package lifecycle/readiness: candidate
  not Consolidated Stable
  Review A findings (P16-A-MAJ-01/P16-A-MAJ-02/P16-A-MIN-01/P16-A-MIN-02) corrected —
    pending bounded verification
  NAV-003 API-binding upstream prerequisite (§13 gap #2) RESOLVED (v0.3) — route
    command-query-api-surface → backtest-orchestrator established (Package 1.1 v0.8/
    Package 1.4 v0.5, Consolidated Stable)
  VIEW-002 computation-owner/API-binding prerequisite (§13 gap #1, phần VIEW-002)
    RESOLVED (v0.4) — route command-query-api-surface → review-evidence-service
    established (ADR-020 v0.1 Approved, Package 1.1 v0.9/Package 1.4 v0.6, Consolidated
    Stable)
  pending upstream binding resolution (VIEW-003 synthesis owner, §13 gap #1 phần
    VIEW-003) — Major prerequisite còn lại, KHÔNG resolve tại Package 1.6, chờ Domain
    Contract amendment (canonical semantic-decision hash) VÀ một ADR kế tiếp
  pending Independent Review B
  pending Product Owner consolidation decision

Package 1.6 v0.1 LÀ candidate đầu tiên — v0.2 LÀ bounded correction đóng bốn Review A
  finding trên v0.1 (banner đầu tài liệu), KHÔNG invalidate identifier accounting của
  v0.1 (§4.5, VẪN 59/59), CHỈ sửa binding/coverage-terminology/accessibility-authority
  claim đã over-state, KHÔNG redesign/mở rộng scope. v0.3 LÀ bounded correction (đóng
  upstream prerequisite của `P16-A-MAJ-01`, vai trò `Package 1.6 NAV-003 Binding
  Correction Executor`) — cập nhật NAV-003 binding/current baseline reference sau khi
  Package 1.1 v0.8 VÀ Package 1.4 v0.5 established route command-query-api-surface →
  backtest-orchestrator, KHÔNG redesign/mở rộng scope, KHÔNG resolve VIEW-002/VIEW-003
  (`P16-A-MAJ-02`, §13 gap #1, VẪN Major prerequisite còn lại), KHÔNG resolve DD-001,
  KHÔNG reconsolidate. v0.4 LÀ bounded correction (đóng phần VIEW-002 của
  `P16-A-MAJ-02`, vai trò `Package 1.6 VIEW-002 Correction Executor`) — cập nhật
  VIEW-002 binding/current baseline reference sau khi Approved ADR-020 v0.1 VÀ Package
  1.1 v0.9/Package 1.4 v0.6 established route command-query-api-surface →
  review-evidence-service, KHÔNG redesign/mở rộng scope, KHÔNG resolve VIEW-003 (§13
  gap #1 phần VIEW-003, VẪN Major prerequisite còn lại), KHÔNG resolve DD-001, KHÔNG
  reconsolidate. Toàn bộ chín package Phase 1 (1.1–1.6, cộng 1.3-A/B/C/D) nay có
  candidate/Consolidated Stable artifact — Gate 2/Phase 2 VẪN KHÔNG mở cho tới khi TẤT
  CẢ package đạt Consolidated Stable VÀ mọi consolidation condition (§14) thỏa, BAO GỒM
  prerequisite còn lại (VIEW-003 synthesis owner) ghi nhận tại v0.2, VẪN unresolved tại
  v0.4.
```
