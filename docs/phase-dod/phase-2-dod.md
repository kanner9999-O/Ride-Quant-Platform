---
id: phase-2-dod
title: "Phase 2 — Product Prototype Definition of Done"
version: "0.3"
status: Approved
owner: Product Owner
reviewers: []
approved_by: Product Owner
approved_at: "2026-08-13"
created_at: "2026-08-13"
last_review: null
next_review: null
depends_on: ["00-governance", "11-adr-process", "12-approval-gates", "13-quality-gates", "14-roadmap"]
---

# Phase 2 — Product Prototype: Definition of Done (DoD)

**ACCEPTED VÀ INCORPORATED (2026-08-13, Product Owner decision) — status: Draft → Approved.** `phase-2-dod.md` v0.3 nay ĐÃ được Product Owner accept VÀ incorporate làm authoritative Phase 2 DoD, qua transaction mechanical `Phase 2 DoD v0.3 Acceptance + Canonical Incorporation Recorder` (2026-08-13). Nguyên văn quyết định: **"ACCEPT PHASE 2 DOD V0.3 — INCORPORATE INTO PHASE 2 CANONICAL PHASE PLAN."** Review evidence trước acceptance: Review A trên v0.1 (`P2-DOD-A-MAJ-01`/`P2-DOD-A-MIN-01`, `REVISION_REQUIRED`) → v0.2 đóng cả hai → bounded Review A re-review v0.2 `CLEAN` → Independent Review B v0.2 (Blocker 0/Major 3/Minor 0 — `P2-DOD-B-MAJ-01`/`02`/`03`, `REVISION_REQUIRED`) → v0.3 đóng cả ba → bounded Review A verification v0.3 `CLEAN` (Blocker 0/Major 0/Minor 0) → Independent bounded Review B v0.3 (`P2-DOD-B-MAJ-01`/`02`/`03` CLOSED, New Blocker 0/New Major 0/New Minor 0, regression check `CLEAN`, `ADR_NOT_REQUIRED`, `READY_FOR_PRODUCT_OWNER_DECISION`). Xem §14 "Acceptance status" phía dưới cho incorporation record đầy đủ theo bốn điều kiện [Chapter 14 §14.3.1](../constitution/14-roadmap.md). **Lifecycle:** `version: "0.3"` UNCHANGED (mechanical acceptance/incorporation transaction, KHÔNG substantive content change), `status: Draft → Approved`, `approved_by: Product Owner`, `approved_at: "2026-08-13"`. `Approved` — KHÔNG `Locked` — LÀ document lifecycle state (Chapter 12 §12.2 điểm 5 công nhận `Approved` một mình đã authoritative cho mục đích Chapter 12/13 sử dụng, KHÔNG bắt buộc `Locked` bổ sung). **Hệ quả:** §2's gate-set declaration (Trigger A applicable, {I-11, I-12}; Trigger B/C/D/E NOT APPLICABLE, mỗi kết luận điều kiện trên §4's boundary) nay LÀ authoritative Phase 2 gate-set declaration cho mục đích Chapter 12/13 sử dụng — chấp nhận declaration KHÔNG PHẢI Quality Gate PASS, KHÔNG PHẢI gate nào đã "pass." **Transaction acceptance/incorporation này KHÔNG:** sửa §§1–13 substantive DoD criteria (bao gồm 17-surface + 21-UC completion requirement, I-11 Access-control audit authority, I-12 traceability requirement, Trigger B/C/D/E semantics, prototype boundary, evidence/review/BCC/validator requirements, `P2-RETRO-001` boundary, `ADR_NOT_REQUIRED` result); tuyên bố prototype substantively complete; chạy full-scope Backward Consistency Check (§10); sinh Quality Gate PASS evidence (§2/§6); thực hiện Phase-level Gate review (§8); thực hiện `P2-RETRO-001` (§11); mở Gate 3; approve Phase 2; authorize Phase 3/deployment/implementation/LIVE; sửa Product/UX authority, Constitution, Phase 2 rules, ADR, hay architecture nào.

**Vai trò của tài liệu này:** đây LÀ **DoD candidate artifact** mà [Chapter 12 §12.1](../constitution/12-approval-gates.md) (Locked) khóa rule — nguyên văn: "DoD criteria phải được viết ra và được Product Owner chấp nhận TRƯỚC KHI phase/gate tương ứng sử dụng chúng," VÀ "mọi Phase... phải có DoD cụ thể được viết ra và duyệt TRƯỚC KHI Phase đó MỞ APPROVAL GATE" — tức TRƯỚC KHI Gate 3 mở, KHÔNG PHẢI trước khi Phase 2 BẮT ĐẦU (Phase 2 start authorization LÀ một transaction riêng biệt, ĐÃ ghi nhận hợp lệ trước DoD này, đúng Chapter 14 §14.3's phân biệt "Phase authorized" ≠ "DoD accepted" — xem §13 dưới). VÀ [Chapter 14 §14.3](../constitution/14-roadmap.md) (Locked, v1.6) khóa cardinality/nơi ở ("mỗi Phase phải resolve được đúng một authoritative DoD artifact"). Tài liệu này **định nghĩa tiêu chí** cho Phase 2 — nó **KHÔNG** phải bằng chứng "đã đạt tiêu chí", VÀ nó **KHÔNG** tự nó là Product Owner acceptance. `Approved`/`Phase 2 Approved` LÀ outcome của Phase 2 Approval Gate (Gate 3) — **KHÔNG** phải một mục trong DoD này.

**Nguồn gốc:** Roadmap Chapter 14 §14.2 (Locked v1.6) khai báo Phase 2 CHỈ bằng "Phase 2 — Product Prototype (HTML/React/Figma — công cụ không quan trọng) → Approval Gate" — **KHÔNG** một sub-item deliverable list nào (khác Phase 0/1/1.5/3/6/8, mỗi phase đó CÓ danh sách con tường minh). Vì vậy tài liệu này derive substantive completion criteria (§3) TRỰC TIẾP từ Product/Vision/UX authority đã `Consolidated Stable` (Package 0.3-A `product-requirement.md`, 0.3-B `use-case-workflow.md`, 0.3-C `ux-blueprint.md`) — KHÔNG tự invent product scope mới, KHÔNG mở rộng ngoài 21 Use Case (`UC-001`–`UC-021`) đã tồn tại.

**Authority boundary:** tài liệu này sở hữu **substantive DoD content của Phase 2** — theo delegation từ [Chapter 14 §14.3](../constitution/14-roadmap.md). Nó **KHÔNG** định nghĩa lại: phase approval orchestration ([Chapter 12](../constitution/12-approval-gates.md)); review eligibility/cardinality ([Chapter 0 §3](../constitution/00-governance.md), [Chapter 11 §11.5](../constitution/11-adr-process.md)); quality-gate semantics/trigger A–E ([Chapter 13 §13.12](../constitution/13-quality-gates.md)); ADR Scope Rule ([Chapter 0 §4b](../constitution/00-governance.md)); Product requirement/Use Case/UX content ([`product-requirement.md`](../product/product-requirement.md)/[`use-case-workflow.md`](../product/use-case-workflow.md)/[`ux-blueprint.md`](../product/ux-blueprint.md), Package 0.3-A/B/C — CHỈ tham chiếu, KHÔNG redefine); phase sequence/canonical Phase-plan model ([Chapter 14 §14.1–§14.2](../constitution/14-roadmap.md)); current version/status/state của bất kỳ tài liệu nào ([MANIFEST](../MANIFEST.md) theo [I-12](../constitution/02-platform-invariants.md)); hay `P2-RETRO-001` (`phase-2-rules.md`, KHÔNG redefine — §11 dưới cho boundary chính xác).

**ADR Scope Rule check (áp cho chính DoD này, Chapter 0 §4b):** tài liệu này KHÔNG tạo Platform Invariant/Event Schema/Module Taxonomy/Governance-process change nào, KHÔNG quyết định architecture ảnh hưởng >1 module (chỉ định nghĩa completion criteria, tham chiếu authority đã tồn tại), KHÔNG khó đảo ngược (DoD sửa được qua bounded correction, đúng pattern Phase 0/1/1.5), KHÔNG supersede ADR Locked nào → **`ADR_NOT_REQUIRED`** cho chính transaction authoring DoD này. Bất kỳ quyết định product/architecture MỚI nào phát sinh trong lúc author DoD (nếu có) được ghi nhận LÀM external dependency (§5), KHÔNG tự quyết tại đây.

**v0.2 — bounded correction (2026-08-13), đóng `P2-DOD-A-MAJ-01`/`P2-DOD-A-MIN-01` (Review A).** (1) `P2-DOD-A-MAJ-01`: v0.1 §2 Trigger A kết luận applicable-invariant set = RỖNG bằng suy diễn "prototype không thực thi production behavior ⟹ invariant không applicable" — SAI, vi phạm Chapter 2's per-invariant Scope declaration, cụ thể I-11/I-12 khai báo Scope **"Toàn hệ thống"** (whole-system), bao trùm prototype VÀ chính tài liệu governance này. Sửa: §2 Trigger A nay đánh giá TỪNG I-1..I-13 riêng theo đúng Scope — I-11 (Secrets & Custody Isolation) VÀ I-12 (Single Source of Truth) APPLICABLE (satisfied-by-absence + concrete prototype-level conformance requirement mỗi cái); {I-1..I-10, I-13} NOT APPLICABLE (Scope exclusion structural — Decision Pipeline/Compute Engine/Strategy-Decision-Risk-Execution Engine/Plugin/Ledger/Domain-Contract-entity Scope KHÔNG bao gồm một UI prototype layer). §4 mở rộng tương ứng với hai concrete requirement (KHÔNG credential/secret thật; traceability/rebuild-được từ authoritative Product/UX baseline — đã tồn tại một phần tại v0.1, nay elevate tường minh thành I-11/I-12 gate evidence). (2) `P2-DOD-A-MIN-01`: đoạn mở đầu "Vai trò của tài liệu này" trích Chapter 12 §12.1 mơ hồ ("TRƯỚC KHI phase/gate mở") — CÓ THỂ đọc sai thành "trước khi Phase 2 bắt đầu," ngụ ý sai rằng Phase 2 Start Authorization (đã ghi nhận trước DoD này) chưa hợp lệ. Sửa: trích nguyên văn chính xác Chapter 12 §12.1 — "DoD criteria phải được viết ra và được Product Owner chấp nhận TRƯỚC KHI phase/gate TƯƠNG ỨNG sử dụng chúng," VÀ "TRƯỚC KHI Phase đó MỞ APPROVAL GATE" (Gate 3, KHÔNG PHẢI Phase 2 start) — thêm câu tường minh phân biệt "Phase authorized" ≠ "DoD accepted," KHÔNG reinterpret/reopen Phase 2 Start Authorization transaction đã ghi nhận. **KHÔNG đổi:** §1 Phase identity, §3 substantive completion criteria (9 mục), §5 external dependencies, §6-§10 (evidence/validator/review/finding-closure/BCC requirements), §11 P2-RETRO-001 boundary, §12 phase-decision bundle requirements, §13 explicit non-inclusion (9 trạng thái), §14 acceptance status, Trigger B/C/D/E kết luận (§2), ADR Scope Rule check kết luận (`ADR_NOT_REQUIRED`, KHÔNG đổi). `status` VẪN `Draft`, `approved_by`/`approved_at` VẪN `null` — CHƯA accepted, CHƯA incorporated.

**v0.3 — bounded correction (2026-08-13), đóng `P2-DOD-B-MAJ-01`/`P2-DOD-B-MAJ-02`/`P2-DOD-B-MAJ-03` (Independent Review B trên v0.2, verdict `REVISION_REQUIRED`, Blocker 0/Major 3/Minor 0).** (1) `P2-DOD-B-MAJ-01`: §3 criterion 3 làm loãng completion thành "coverage đủ cho 21 UC" — SAI, 21-UC coverage KHÔNG tương đương 17-surface completion (một UC mapping có thể trùng lặp nhiều surface, prototype có thể phủ đủ 21 UC mà VẪN bỏ sót một first-class surface). Sửa: criterion 3 nay đòi hỏi CẢ BA — (a) representation cho TOÀN BỘ 17 surface (`SCR-001`–`SCR-011`/`VIEW-001`–`VIEW-006`); (b) applicable authoritative behavior/state/handoff requirement cho MỖI surface đã represent; (c) coverage đủ 21 UC, BỔ SUNG KHÔNG thay thế (a)/(b). `P2-PROTOTYPE-001` batching giữ nguyên (KHÔNG bắt buộc TẤT CẢ 17 trong MỘT batch, KHÔNG per-screen governance cycle). KHÔNG surface thứ 18 nào invent, KHÔNG `SCR-XXX`/`VIEW-XXX` ID nào merge/xóa/rename. (2) `P2-DOD-B-MAJ-02`: §2/§4's I-11 verification wording trình bày repo-scan/grep credential-pattern NHƯ THỂ đó LÀ verification — SAI, Chapter 2 §I-11's authoritative Verification LÀ "Access-control audit," KHÔNG thể bị thay thế. Sửa: §2/§4 nay nêu tường minh authoritative Verification (Access-control audit, trích Chapter 2), định nghĩa bounded Phase-2 interpretation của audit đó (bốn điều kiện: KHÔNG credential-use capability, KHÔNG access-control surface, KHÔNG backend/custody/signing integration, KHÔNG real secret sử dụng/yêu cầu), VÀ nêu tường minh repo-scan/grep CHỈ LÀ supporting evidence, KHÔNG PHẢI thay thế/redefine Verification. I-11 VẪN APPLICABLE (KHÔNG đổi), KHÔNG custody architecture nào invent. (3) `P2-DOD-B-MAJ-03`: §12/§13/§14 chứa stale current-candidate reference ("current candidate hiện v0.1," "DoD defined... v0.1 candidate," "Review evidence trước acceptance: CHƯA thực hiện," §9 "DoD v0.1 này") — mâu thuẫn identity/review-history thật. Sửa: mọi current-candidate pointer nay ghi v0.3; §14 viết lại đầy đủ review history chính xác (Review A trên v0.1: 1 Major/1 Minor, REVISION_REQUIRED; v0.2 đóng cả hai; bounded Review A re-review v0.2 CLEAN; Independent Review B v0.2: Blocker 0/Major 3/Minor 0, REVISION_REQUIRED, `P2-DOD-B-MAJ-01..03`; v0.3 = correction ONLY, KHÔNG tuyên bố Review B đã re-review v0.3). Lịch sử v0.1/v0.2 genuine giữ nguyên (banner v0.2 phía trên, Change history dưới) — KHÔNG mechanically thay mọi "v0.1"/"v0.2." **KHÔNG đổi:** §1 Phase identity, §3 criterion 1-2/4-9, §5 external dependencies, §6/§7 (trừ pointer identity), §8-§11, Trigger B/C/D/E kết luận, I-1..I-10/I-13 kết luận, ADR Scope Rule check kết luận (`ADR_NOT_REQUIRED`, KHÔNG đổi — Review B tìm Major KHÔNG tự động trigger ADR). `status` VẪN `Draft`, `approved_by`/`approved_at` VẪN `null` — CHƯA accepted, CHƯA incorporated.

## 1. Phase identity

```text
Phase:              Phase 2 — Product Prototype
Roadmap source:     Chapter 14 §14.2 (Locked, v1.6, xem MANIFEST cho
                     current version/status)
Roadmap wording
(nguyên văn):        "Phase 2 — Product Prototype (HTML/React/Figma —
                     công cụ không quan trọng) → Approval Gate"
Tool-independence
principle:           HTML/React/Figma LÀ ví dụ công cụ, KHÔNG PHẢI định
                     nghĩa ngữ nghĩa của Phase — implementation medium
                     (Figma static mockup, static HTML, React với mock
                     data, hay tổ hợp) KHÔNG đổi bản chất "prototype,
                     non-authoritative" của deliverable (§4 dưới quy định
                     tường minh, giữ gate applicability KHÔNG phụ thuộc
                     medium).
Deliverable scope
(derive từ Product/
UX authority, KHÔNG
tự invent):          UX representation cho 21 Use Case (`UC-001`–
                     `UC-021`) đã `Consolidated Stable` — 6 stage
                     (Research · Replay · Backtest · Paper · Review ·
                     Improve), 17 screen/view (`SCR-001`–`SCR-011`,
                     `VIEW-001`–`VIEW-006`) theo `ux-blueprint.md` §6
                     catalogue (§3 dưới cho chi tiết).
Phase-level output
bắt buộc:            Approval Gate (Gate 3) — đơn vị chịu gate LÀ Phase,
                     KHÔNG phải screen/component riêng lẻ (Chapter 14
                     §14.1, `phase-2-rules.md` `P2-PROTOTYPE-001`).
```

## 2. Applicable gate set (Chapter 14 §14.4 declaration)

Đánh giá độc lập Trigger A–E ([Chapter 13 §13.12](../constitution/13-quality-gates.md)) cho lớp deliverable "Product Prototype" — **KHÔNG copy kết luận Trigger-A-only của Phase 1.5's DoD** (lớp deliverable khác hẳn: Phase 1.5 LÀ governance/convention document, Phase 2 LÀ UX/product representation, có thể chứa mã HTML/React thật). Mọi kết luận N/A dưới đây **CÓ ĐIỀU KIỆN** trên §4's deliverable boundary giữ vững — vi phạm boundary tại BẤT KỲ artifact cụ thể nào bắt buộc re-resolve gate-set CHO ĐÚNG artifact đó (fail-closed, KHÔNG grandfather theo kết luận Phase-wide này).

```text
Trigger A (universal — invariant conformance, §13.5):
  Đánh giá TỪNG invariant I-1..I-13 riêng theo đúng Scope [Chapter 2
    (02-platform-invariants.md, Locked v3.1)] khai báo — KHÔNG suy diễn
    "prototype không thực thi production behavior" ⟹ "invariant không
    applicable" (đúng chỉ dẫn task, sửa lỗi v0.1 tại đây).

  I-1 Explainability      — Scope "Toàn bộ Decision Pipeline". Prototype
                            KHÔNG PHẢI Decision Pipeline (KHÔNG tính
                            Decision thật, §4). NOT APPLICABLE — Scope
                            exclusion (structural, KHÔNG phải "absence-
                            satisfied"). Nhu cầu UX-level explainability
                            affordance VẪN LÀ một product requirement
                            (§3 mục 6), NHƯNG đó KHÔNG PHẢI I-1 gate
                            evidence.
  I-2 Decision Parity     — Scope "Decision pipeline; cả 4 execution
                            mode". Prototype KHÔNG tính Decision thật ở
                            bất kỳ mode nào. NOT APPLICABLE — Scope
                            exclusion.
  I-3 No Repaint          — Scope "Mọi Compute Engine phát sinh output
                            theo thời gian". Prototype KHÔNG PHẢI
                            Compute Engine. NOT APPLICABLE — Scope
                            exclusion.
  I-4 Strategy Isolation  — Scope "Strategy Engine, Decision Engine,
                            Risk Gateway, Execution Engine". Prototype
                            (UI layer) KHÔNG PHẢI một trong bốn engine
                            đó. NOT APPLICABLE — Scope exclusion.
  I-5 Observable Dependency — Scope "Mọi input... dùng trong Decision
                            Pipeline". KHÔNG Decision Pipeline thật tồn
                            tại trong prototype. NOT APPLICABLE — Scope
                            exclusion.
  I-6 Fail-Safe by Scope  — Scope "Mọi Compute Engine, Projection,
                            Runtime Service" (ba loại runtime module
                            theo Chapter 7 taxonomy). Prototype KHÔNG
                            PHẢI runtime module nào (KHÔNG deploy,
                            KHÔNG backend, §4) — KHÔNG PHẢI "Projection"
                            theo nghĩa Chapter 7 (runtime service type),
                            khác với "derived representation" nghĩa
                            rộng của I-12. NOT APPLICABLE — Scope
                            exclusion.
  I-7 Plugin Non-Bypass   — Scope "Mọi Plugin". Prototype KHÔNG PHẢI
                            plugin. NOT APPLICABLE — Scope exclusion.
  I-8 Kill Switch         — Scope "Risk Gateway, Execution Engine, mọi
                            Exchange Adapter". NOT APPLICABLE — Scope
                            exclusion.
  I-9 Numerical Precision — Scope "Position Ledger, Execution Engine,
                            Risk Gateway". Prototype KHÔNG PHẢI một
                            trong ba module đó, KHÔNG lưu trữ/tính toán
                            giá trị tài chính authoritative (§4, §5 —
                            CHỈ hiển thị mock/illustrative value). NOT
                            APPLICABLE — Scope exclusion (KHÔNG PHẢI
                            "absence-satisfied", vì Scope tự nó loại trừ
                            UI display layer).
  I-10 Idempotent Execution — Scope "Execution Engine, Exchange
                            Adapter". Prototype KHÔNG thực thi lệnh
                            thật (§4). NOT APPLICABLE — Scope exclusion.
  I-11 Secrets & Custody  — Scope **"Toàn hệ thống, đặc biệt Execution
                            Engine, Exchange Adapter"** — whole-system
                            Scope, bao trùm prototype. **APPLICABLE —
                            satisfied-by-absence, VỚI một concrete
                            conformance requirement:** KHÔNG một Phase 2
                            prototype artifact/code/config nào được
                            nhúng, tham chiếu, hay yêu cầu exchange API
                            key/secret/private key/credential thật dưới
                            bất kỳ hình thức nào (kể cả placeholder giả
                            danh thật) — đây LÀ completion-boundary
                            REQUIREMENT bổ sung tại §4.
                            **Authoritative Verification (KHÔNG redefine
                            tại DoD này):** Chapter 2 §I-11's chính xác
                            Verification — "Access-control audit — xác
                            nhận CHỈ Exchange Adapter hoặc dedicated
                            Custody/Signing Service được phép sử dụng
                            credential trực tiếp." **Bounded Phase-2
                            interpretation của audit đó** (proportional
                            với lớp deliverable KHÔNG có runtime/backend,
                            §4) — audit xác nhận CẢ BỐN:
                              (1) KHÔNG prototype artifact nào establish
                                  credential-use capability (KHÔNG code
                                  path nào "sử dụng" một credential);
                              (2) KHÔNG credential access-control surface
                                  nào bị required/introduced bởi
                                  prototype (KHÔNG login/auth UI kết nối
                                  hệ thống credential thật);
                              (3) KHÔNG backend/custody/signing
                                  integration nào tồn tại trong
                                  prototype;
                              (4) KHÔNG real secret/credential nào được
                                  sử dụng hay yêu cầu ở bất kỳ đâu.
                            Repository secret-pattern scan/grep **CÓ THỂ
                            dùng LÀM supporting evidence** cho audit trên
                            (mỗi batch review, §8) — **KHÔNG PHẢI thay
                            thế hay redefine** chính I-11's Verification.
                            KHÔNG custody/signing architecture nào được
                            author/invent tại DoD này hay tại Phase 2
                            (đó LÀ quyết định Phase 3/deployment riêng
                            biệt).
  I-12 Single Source of Truth — Scope **"Toàn hệ thống — cả runtime
                            (Event Log) lẫn authoritative documentation
                            như MANIFEST.md, ADR, Constitution, và
                            Domain Contract"** — whole-system Scope, bao
                            trùm prototype VÀ chính DoD này. **APPLICABLE
                            — satisfied-by-absence, VỚI một concrete
                            conformance requirement:** prototype LÀ một
                            derived representation của Product/UX
                            authority đã Consolidated Stable
                            (`product-requirement.md`/`use-case-
                            workflow.md`/`ux-blueprint.md`) — nó KHÔNG
                            được trở thành một competing source of truth
                            (KHÔNG tự tạo `UC-XXX`/`PR-XXX`/domain
                            concept mới, đúng §5/§6 đã yêu cầu). Mọi
                            prototype artifact PHẢI "rebuild hoặc đối
                            chiếu hoàn toàn" (I-12's Verification) được
                            từ baseline đó — CHÍNH LÀ traceability
                            requirement §6 đã định nghĩa (UC-XXX/SCR-XXX/
                            VIEW-XXX), nay elevate tường minh thành I-12
                            gate evidence, KHÔNG CHỈ một "nice-to-have"
                            evidence field.
  I-13 State Transition Integrity — Scope "Mọi entity có vòng đời trạng
                            thái được khai báo trong Domain Contract".
                            Prototype KHÔNG sở hữu/mutate một entity
                            Domain Contract nào (CHỈ hiển thị UX-level
                            state như "loading/blocked/empty" — KHÁC
                            entity state machine của Domain Contract).
                            NOT APPLICABLE — Scope exclusion. Liên quan
                            NHƯNG tách biệt: prototype KHÔNG được hiển
                            thị state/transition combination mà Domain
                            Contract's state machine authoritative
                            KHÔNG cho phép — đây LÀ product-level
                            non-invention constraint đã tồn tại
                            (`ux-blueprint.md` Non-Goals), KHÔNG PHẢI
                            chính I-13 gate.

  Kết luận Trigger A: applicable-invariant set **KHÔNG RỖNG** — {I-11,
    I-12} APPLICABLE (whole-system Scope, satisfied-by-absence + concrete
    prototype-level conformance requirement mỗi cái, §4 mở rộng tương
    ứng); {I-1..I-10, I-13} NOT APPLICABLE (Scope exclusion structural —
    prototype KHÔNG PHẢI runtime module/engine/pipeline/entity nào mà
    Scope tương ứng chỉ định).
  Điều kiện: nếu MỘT screen/artifact cụ thể vi phạm boundary §4 (vd wire
    thật vào authoritative Domain state, tính Decision thật, nhúng
    secret thật) → invariant Scope đó PHẢI re-resolve cho ĐÚNG artifact
    đó (có thể kích hoạt thêm I-1..I-10/I-13 cho riêng artifact đó),
    KHÔNG miễn trừ theo kết luận Phase-wide này.

Trigger B (executable-implementation-triggered coverage, §13.12-B):
  Trigger đòi hỏi CẢ BA: authoritative executable implementation +
    resolvable coverage boundary + resolvable tier.
  Kết luận: KHÔNG APPLICABLE — theo yêu cầu tường minh §4 dưới, MỌI
    Phase 2 prototype artifact (bất kể medium — Figma/static HTML/React
    với mock data) KHÔNG PHẢI authoritative executable implementation
    (KHÔNG production frontend, KHÔNG shipped code, KHÔNG entry
    `module-registry.yaml`, KHÔNG standalone-artifact tier declaration
    nào được tạo tại DoD này). Kết luận NÀY LÀ một completion-boundary
    REQUIREMENT (§4), KHÔNG PHẢI một quan sát tình cờ — do đó KHÔNG phụ
    thuộc tool choice, đúng yêu cầu "gate applicability KHÔNG ambiguous
    chỉ vì medium thay đổi."

Trigger C (tier-triggered — Chaos Test→Tier 0, Parity Test→Tier 1):
  §13.4's tier-resolution chain có ba nhánh: (1) runtime module qua
    `module-registry.yaml`; (2) executable artifact thuộc canonical
    owning module; (3) standalone executable với tier declaration
    tường minh.
  Kết luận: KHÔNG APPLICABLE — KHÔNG nhánh nào match một prototype
    artifact (KHÔNG runtime module, KHÔNG thuộc owning module nào,
    KHÔNG standalone tier declaration nào được tạo) — ĐỘC LẬP khỏi
    Trigger B (đúng phân biệt Phase 1.5's finding EF-DOD-A-MAJ-01: C LÀ
    tier-triggered riêng, KHÔNG có tiền đề B).

Trigger D (responsibility/boundary-triggered):
  Security (I-4/I-7/I-11 — isolation/custody/authorization boundary):
    KHÔNG APPLICABLE, CÓ ĐIỀU KIỆN — prototype KHÔNG được nhúng/yêu cầu
    exchange credential/API key/secret thật, KHÔNG kết nối backend thật
    (§4 boundary requirement). Vi phạm điều kiện này tại BẤT KỲ artifact
    nào → Security trigger PHẢI re-resolve cho artifact đó.
  Data quality/numerical precision (I-9/I-13 — authoritative/financial
    data): KHÔNG APPLICABLE, CÓ ĐIỀU KIỆN — prototype CHỈ hiển thị
    mock/illustrative/simulated data (đúng `ux-blueprint.md` §15 — vd
    Backtest "simulated economic evidence... nhãn product-required,
    domain-representation deferred"), KHÔNG xử lý authoritative/
    financial data thật.
  Performance (§13.7 — authoritative performance budget): KHÔNG
    APPLICABLE — KHÔNG performance budget nào được declare/accept cho
    Phase 2 prototype tại DoD này hay tại Chapter 13 (§13.7 defer
    concrete threshold tới Phase 1.5 backlog, KHÔNG liên quan prototype).
  Observability (production/operational path): KHÔNG APPLICABLE, CÓ
    ĐIỀU KIỆN — prototype KHÔNG deploy lên production/operational path
    (§4 boundary requirement).

Trigger E (lifecycle-triggered):
  Schema/contract compatibility (Chapter 10 §10.3 — publish contract/
    schema): KHÔNG APPLICABLE, CÓ ĐIỀU KIỆN — Phase 2 prototype KHÔNG
    publish API/database/event contract nào tiêu thụ bởi module khác
    (đúng `ux-blueprint.md` §16 Non-Goals: "API contract, database
    query, backend service, event transport... KHÔNG author tại đây" —
    kế thừa nguyên tắc đó cho chính prototype implementation, §4).
  Migration/rollback: KHÔNG APPLICABLE — prototype KHÔNG PHẢI migration
    artifact.

Rollup (§13.12, "Phase deliverable"):
  Gate set mà approved phase plan/roadmap khai báo áp dụng CHÍNH LÀ gate
    set DoD này khai báo (một khi accepted/incorporated, Chapter 14
    §14.4) — bundle này TỰ NÓ LÀ authority nguồn cho declaration đó,
    KHÔNG một tài liệu khác định nghĩa lại.

Kết luận tổng hợp (Chapter 14 §14.4 declaration):
  Trigger A ÁP DỤNG, applicable-invariant set = **{I-11, I-12}** (whole-
    system Scope invariant, mỗi cái satisfied-by-absence + concrete
    prototype-level conformance requirement, §4 mở rộng) — {I-1..I-10,
    I-13} NOT APPLICABLE (Scope exclusion structural, ĐỘC LẬP khỏi §4's
    boundary vì chính Scope loại trừ prototype artifact class). Trigger
    B/C/D/E KHÔNG APPLICABLE, MỖI kết luận CÓ ĐIỀU KIỆN trên §4's
    boundary giữ vững cho TỪNG artifact cụ thể. KHÔNG một trigger nào
    "undefined/không resolve được" — mọi trigger resolve rõ ràng (§13.8
    fail-closed KHÔNG bị vi phạm; "N/A có điều kiện + per-artifact
    re-resolve requirement" LÀ một resolved state, KHÔNG PHẢI ambiguity;
    "APPLICABLE non-empty" LÀ một resolved state khác, KHÔNG PHẢI gap).
```

## 3. Substantive completion criteria (Product Prototype)

Outcome-oriented — derive TRỰC TIẾP từ `ux-blueprint.md` (Package 0.3-C, `Consolidated Stable`) VÀ `use-case-workflow.md`/`product-requirement.md` (Package 0.3-A/B, `Consolidated Stable`). KHÔNG một tiêu chí nào dưới đây tạo product scope mới ngoài `UC-001`–`UC-021`/`PR-001`–`PR-034` đã tồn tại.

```text
1. Coherent end-to-end user journey: đủ representation cho lifecycle
   stage flow (`ux-blueprint.md` §8) VÀ cross-screen/cross-stage handoff
   (§9) — mỗi 21 UC có ít nhất một journey path hoàn chỉnh qua prototype.
2. Workspace/navigation model: global workspace/navigation (§5, §5a —
   sáu NAV spec) hiện diện VÀ nhất quán xuyên suốt mọi screen được
   author.
3. Major product surface: 17 screen/view (`SCR-001`–`SCR-011`,
   `VIEW-001`–`VIEW-006`, §6 catalogue) LÀ 17 first-class surface riêng
   biệt, đã Consolidated Stable — 21-UC coverage KHÔNG PHẢI thay thế
   cho 17-surface completion (một UC mapping có thể trùng lặp nhiều
   surface, prototype có thể phủ đủ 21 UC mà VẪN bỏ sót một first-class
   surface bắt buộc). Phase 2 substantive completion TRƯỚC Gate 3
   eligibility đòi hỏi CẢ BA điều kiện, KHÔNG điều kiện nào miễn trừ
   điều kiện kia:
     a. representation cho TOÀN BỘ 17 surface (`SCR-001`–`SCR-011`,
        `VIEW-001`–`VIEW-006`) — KHÔNG một surface nào bị bỏ sót;
     b. applicable authoritative behavior/state/handoff requirement
        (§7.1–§7.6 detailed spec, §11 state coverage, §9 handoff) cho
        MỖI surface đã represent;
     c. coverage đủ cho 21 UC (`UC-001`–`UC-021`) — bổ sung, KHÔNG
        thay thế điều kiện (a)/(b).
   KHÔNG bắt buộc TẤT CẢ 17 surface phải author trong MỘT Phase 2
   iteration/batch — P2-PROTOTYPE-001 (§8) VẪN áp dụng nguyên vẹn: batch/
   milestone theo category/stage, KHÔNG per-screen governance cycle
   riêng cho từng surface. Danh sách 17 surface LÀ closed set, đã pin
   tại `ux-blueprint.md` §6 — DoD này KHÔNG invent surface thứ 18,
   KHÔNG merge/xóa/rename bất kỳ `SCR-XXX`/`VIEW-XXX` ID nào.
4. Stage loop (Research · Replay · Backtest · Paper · Review · Improve,
   tên CHÍNH XÁC theo `ux-blueprint.md` §7.1–§7.6 — KHÔNG dùng paraphrase
   khác "Research→Execute→Review→Improve" vì stage taxonomy đã
   Consolidated Stable, KHÔNG tự đổi tên): mỗi stage có ít nhất một
   screen/view đại diện, thể hiện lifecycle transition Research→Replay/
   Backtest→Paper→Review→Improve.
5. Account/risk context visibility: Account context READ-ONLY hiển thị
   xuyên suốt mọi screen (`UX-INV-1`) — KHÔNG Account switcher (chưa
   UC/PR nào authorize). RiskEvaluation-liên quan evidence hiển thị CHỈ
   nơi UC-XXX đã định nghĩa (vd SCR-006/007) — KHÔNG "risk control" mới
   (editable risk parameter UI) nào ngoài UC/PR đã tồn tại.
6. Explainability affordance: evidence/authority presentation model
   (`ux-blueprint.md` §10, trực tiếp map I-1 Explainability's Scope
   Decision Pipeline) — MỌI Decision-related screen hiển thị evidence
   trace theo §10's model.
7. Replay/Backtest/Paper/Live distinction: ba mode giữ nhãn/authority
   tách biệt tường minh xuyên suốt (§17 acceptance criterion 5/6/9) —
   Live LUÔN hiển thị `Unauthorized` (`STATE-027`), KHÔNG action/screen
   nào dẫn tới Live (§17 criterion 15, `OQ-002` §5 dưới).
8. Responsive/error/empty/loading/blocked/NON_EVALUABLE state: §11
   ("Loading, empty, unavailable, blocked, failed và NON_EVALUABLE
   states") coverage cho MỌI screen được author trong batch đó —
   KHÔNG happy-path-only prototype.
9. Cross-screen interaction consistency: historical cursor/correction UX
   (§12), strategy-version comparison UX (§13), traceability matrices
   (§14) — hành vi nhất quán xuyên suốt mọi screen tham chiếu cùng entity/
   evidence family.
```

## 4. Explicit deliverable boundary

```text
Phase 2 Product Prototype LÀ:
  - UX/product representation cho hành vi ĐÃ được `product-
    requirement.md`/`use-case-workflow.md`/`ux-blueprint.md` kiểm soát
    (Consolidated Stable) — bất kể medium triển khai thực tế (Figma
    mockup, static HTML, React với mock/static data, hay tổ hợp). Đây
    LÀ derived representation của authoritative Product/UX baseline
    (I-12 Single Source of Truth, §2 — Trigger A applicable), KHÔNG BAO
    GIỜ competing source of truth: KHÔNG artifact nào tự tạo `UC-XXX`/
    `PR-XXX`/domain concept mới, mọi artifact PHẢI rebuild/đối chiếu
    được từ baseline đó (§6 traceability requirement CHÍNH LÀ I-12's
    Verification).
  - non-authoritative: KHÔNG kết nối backend thật, KHÔNG xử lý dữ liệu
    tài chính/authoritative thật, KHÔNG thực thi lệnh thật. KHÔNG một
    artifact/code/config nào được nhúng, tham chiếu, hay yêu cầu exchange
    credential/API key/secret/private key thật dưới bất kỳ hình thức nào,
    kể cả placeholder giả danh thật (I-11 Secrets & Custody Isolation,
    §2 — whole-system Scope, Trigger A applicable) — authoritative
    Verification LÀ Chapter 2 §I-11's Access-control audit (KHÔNG
    redefine tại đây, xem §2's bounded Phase-2 interpretation); repo-
    scan/grep credential-like pattern tại mỗi batch review (§8) LÀ
    supporting evidence, KHÔNG PHẢI thay thế audit đó.

Phase 2 Product Prototype KHÔNG LÀ:
  - Production frontend implementation (Phase 4 — Frontend, Chapter 14
    §14.2). KHÔNG một prototype artifact/component/code nào được carry-
    forward/reuse trực tiếp LÀM production frontend code mà KHÔNG qua
    một transaction governed riêng biệt tại Phase 3/4 (bao gồm
    `module-registry.yaml` entry + tier declaration mới) — đây LÀ
    completion-boundary REQUIREMENT, nền tảng cho Trigger B/C §2 KHÔNG
    applicable.
  - Backend implementation (Phase 3 — Core Backend).
  - Exchange/venue integration (Phase 3/Phase 5 — Integration).
  - Deployment (Phase 7 — Deployment).
  - LIVE authorization (`OQ-002`, §5 dưới — CHỈ đóng qua ADR tương lai,
    KHÔNG qua Phase 2 prototype work).
```

## 5. External dependencies / deferred items (tham chiếu, KHÔNG quyết định tại đây)

Theo chỉ dẫn "record như external dependency, KHÔNG tự quyết trong DoD" — mọi mục dưới đây LÀ authority của tài liệu khác, DoD này CHỈ tham chiếu ranh giới ĐÃ pin, KHÔNG redefine:

```text
OQ-002 (Live-gate, Open):        prototype CHỈ hiển thị "Live:
                                 Unauthorized" (STATE-027) tĩnh — KHÔNG
                                 Live UX/architecture/điều kiện chuyển
                                 Live nào được author (`ux-blueprint.md`
                                 §15). Đóng CHỈ qua ADR tương lai (Phase
                                 3), KHÔNG tại Phase 2.
OQ-003 (Product Metrics, Open):  prototype hiển thị evidence đo lường
                                 được — KHÔNG concrete KPI/unified
                                 score/automatic ranking nào được invent
                                 (`ux-blueprint.md` §15). Formula riêng
                                 chờ Product Metrics document (Vision
                                 §1.8).
Backtest domain representation
  (Deferred):                    UX may display simulated economic
                                 evidence dùng thuật ngữ mô tả — KHÔNG
                                 invent `BacktestOrder`/`BacktestFill`/
                                 tương đương/simulation algorithm/fee-
                                 slippage-PnL formula (`ux-blueprint.md`
                                 §15). Domain Contract cho Backtest [nếu
                                 Product Owner quyết định author] LÀ
                                 quyết định tương lai riêng biệt.
PAPER-context authoritative
  Decision establishment
  mechanism (Deferred):          UX may display "Paper entry available/
                                 blocked" — KHÔNG invent cơ chế cụ thể
                                 (trigger, ai ghi nhận) (`ux-blueprint.md`
                                 §15). Product Owner/Domain Contract
                                 correction tương lai.
NAV-003 / VIEW-002 (unresolved,
  không đổi):                    giữ nguyên trạng thái hiện tại trong
                                 `ux-blueprint.md` — DoD này KHÔNG resolve.
Backtest/Frontend tool choice
  (chưa fix):                    HTML/React/Figma cụ thể nào — CHƯA
                                 chọn, KHÔNG bắt buộc chọn tại DoD này
                                 (§1 tool-independence). Bất kỳ lựa chọn
                                 tool NÀO tương lai KHÔNG tự động thay
                                 đổi kết luận Trigger B/C/D/E (§2) —
                                 kết luận đó gắn với BOUNDARY (§4),
                                 KHÔNG gắn với tool.
```

## 6. Evidence requirements

```text
- Exact prototype artifact identity/content pin cho MỖI screen/view
  author trong một batch — với format text-based (HTML/React/markup),
  dùng blob (`git hash-object`, đúng I-12); với format binary/non-
  diffable (Figma file, exported asset), dùng content-hash tương đương
  (vd SHA-256 của file export) PIN VÀO MANIFEST, đúng nguyên tắc I-12
  áp dụng bất kể format underlying (§7 dưới mở rộng).
- Traceability: mỗi artifact author trace được TRỰC TIẾP về đúng một
  hoặc nhiều `UC-XXX` VÀ `SCR-XXX`/`VIEW-XXX` đã tồn tại trong
  `ux-blueprint.md` — KHÔNG artifact "seems useful" nào không truy vết
  được (đúng nguyên tắc §17 criterion 3 của `ux-blueprint.md`, kế thừa
  cho chính prototype implementation).
- Review evidence (§8 dưới) cho từng batch/milestone.
- Full-scope BCC evidence (§10 dưới) trước Gate 3 eligibility.
```

## 7. Validator requirements

```text
- MANIFEST freshness: mọi Phase 2 prototype artifact author/sửa PHẢI có
  entry MANIFEST tương ứng (version/status/blob-hoặc-content-hash/owner)
  tại đúng transaction tạo/sửa nó — KHÔNG deferred bookkeeping.
- Artifact-reference consistency: validator KHÔNG giả định format
  markdown/git-diffable cho mọi Phase 2 artifact (khác Phase 0/1/1.5) —
  với binary/non-text format, "byte-identical" verification dùng
  content-hash so sánh thay vì git diff văn bản; validator vẫn PHẢI xác
  nhận content-hash khớp reference trước khi coi một artifact "không
  đổi."
- MANIFEST table cell budget: `EF-BUDGET-001`/`P2-BUDGET-001` (Global
  §G-BUDGET siết Phase 2, `phase-2-rules.md`) áp dụng nguyên vẹn — ≤
  1,500 từ/cell tại thời điểm mỗi edit.
```

## 8. Review requirements

```text
- Batch/milestone review (`phase-2-rules.md` `P2-PROTOTYPE-001`): Phase
  2 prototype/UX work review theo BATCH gắn kết, KHÔNG theo từng screen/
  component riêng lẻ theo default — screen/component CÓ THỂ iterate BÊN
  TRONG một batch KHÔNG cần A/B/PO cycle riêng, TRỪ KHI nó tạo mới một
  architecture/authority/contract/security/Product-level decision đòi
  hỏi governance riêng.
- Risk-proportional depth (`P2-REVIEW-001`): batch tạo mới UX
  representation → full review tương xứng; correction/iteration bounded
  → bounded re-review đúng phạm vi.
- Minimum eligible independent review TẠI Phase Approval Gate boundary
  (Chapter 0 §3, Chapter 11 §11.5, Chapter 12 §12.2): tối thiểu HAI
  review độc lập TẠI chính Gate 3 boundary — batch-level review (§8
  trên) KHÔNG thay thế yêu cầu Phase-level Gate review riêng biệt, đúng
  pattern Phase 0/1/1.5's precedent.
```

## 9. Finding-closure requirements

```text
- KHÔNG Blocker/Major nào được unresolved tại Gate 3 eligibility (Chapter
  12 §12.2 — never waived qua residual acceptance).
- Minor CÓ THỂ accepted non-blocking qua Product Owner explicit
  acceptance (Chapter 0 §3) — tường minh, KHÔNG ngầm định, KHÔNG suy
  diễn từ im lặng, đúng pattern Phase 0/1/1.5's precedent. Danh sách
  accepted residual (nếu có) sẽ ghi nhận tại một bounded correction/
  acceptance transaction TƯƠNG LAI — DoD candidate hiện tại (v0.3) KHÔNG
  có residual nào (chưa substantive Phase 2 work nào bắt đầu; `P2-DOD-
  A-MAJ-01`/`A-MIN-01`/`B-MAJ-01`/`B-MAJ-02`/`B-MAJ-03` LÀ DoD-authoring
  review finding, đã CLOSED qua v0.2/v0.3 correction — KHÔNG PHẢI Phase
  2 substantive-work residual).
```

## 10. Repository-consistency requirements (full-scope Backward Consistency Check)

```text
Trước Gate 3 eligibility, PHẢI thực hiện MỘT full-scope Backward
  Consistency Check (Chapter 12 §12.4) — KHÔNG per-batch/per-screen BCC
  nào thay thế — xác nhận Phase 2 prototype work KHÔNG mâu thuẫn:
    - Constitution (mọi chapter Locked/Approved)
    - Domain Contract (`/docs/domain/`, mọi entity/state machine
      Consolidated Stable — Account/Decision/Order/Position/Fill/Risk/
      Execution/Trade Intent/Replay Event/Strategy/Regime/Structure/
      Swing/Feature/Candle/Instrument/Venue/Context)
    - Product/UX authority Consolidated Stable (Package 0.3-A/B/C,
      `product-requirement.md`/`use-case-workflow.md`/`ux-blueprint.md`)
    - Phase 1 architecture (Approved, Gate 2 PASSED)
    - Phase 1.5 Engineering Foundation (Approved, Approval Gate PASSED)
  Full-scope BCC dùng kỹ thuật git-log absence-of-touch verification
  (đề xuất PROMOTE_GLOBAL từ `phase1.5-retrospective-001.md` §10.3) —
  xác nhận trực tiếp KHÔNG artifact ngoài Phase 2 scope (§1 trên) bị
  chạm bởi bất kỳ Phase 2 prototype transaction nào.
```

## 11. Retrospective boundary (P2-RETRO-001) — KHÔNG một tiêu chí DoD tại đây

```text
`P2-RETRO-001` (`phase-2-rules.md`, `operational_state: EFFECTIVE`) TỒN
  TẠI VÀ yêu cầu một Phase 2 process retrospective — verify trực tiếp
  wording: "TRƯỚC KHI Phase 3 substantive work bắt đầu, PHẢI thực hiện
  một Phase 2 process retrospective..." Rule này gắn CHÍNH XÁC với tiền
  đề Phase 3 substantive work, KHÔNG PHẢI với Phase 2 Approval Gate
  (Gate 3) — Gate-path controls (`phase-2-rules.md` §Gate-path controls)
  liệt kê trình tự riêng cho chính Gate 3 (prototype/UX batch work →
  Phase-wide BCC nếu áp dụng → Phase-level Gate review → Product Owner
  Gate 3 decision) mà KHÔNG có bước retrospective nào trong đó — đúng
  pattern `EF-RETRO-001`'s treatment tại `phase-1.5-dod.md` §10.
Tiêu chí DoD tại tài liệu này (§1–§10 trên) **KHÔNG bao gồm** `P2-RETRO-
  001` LÀM một mục — retrospective đó VẪN LÀ một điều kiện tách biệt, bổ
  sung, áp dụng cho Phase 3 substantive work, KHÔNG PHẢI cho Phase 2
  Approval Gate. Gate 3 CÓ THỂ đạt eligibility mà KHÔNG cần retrospective
  đó hoàn tất — NHƯNG Phase 3 substantive work VẪN bị chặn bởi `P2-RETRO-
  001` (VÀ `P1-RETRO-001`/`EF-RETRO-001`, đã COMPLETE) độc lập với Gate 3
  outcome.
Tài liệu này KHÔNG thực hiện retrospective đó tại chính transaction
  authoring này.
```

## 12. Phase-decision bundle requirements (Chapter 14 §14.4.1–§14.4.2)

Tại đúng atomic recording boundary (Chapter 14 §14.4.2), bundle phải pin — **Chapter 14 authority (prepared trực tiếp tại DoD/Roadmap):**

```text
- canonical Phase identity (= "Phase 2 — Product Prototype")
- exact Roadmap version/content identity đã dùng (Chapter 14 §14.2, hiện
  v1.6, xem MANIFEST cho current version/status)
- exact accepted-DoD identity/content version đã incorporate (tài liệu
  này, khi được accept — current candidate hiện v0.3, CHƯA accepted,
  CHƯA incorporated)
- exact gate-set declaration identity/content resolve từ đó (§2 phía
  trên)
```

**Reference-only (authority chapter khác, DoD KHÔNG redefine):** Product Owner DoD-acceptance evidence (Chapter 0 §3); required/submitted deliverable evidence (§3/§6 phía trên, Chapter 12 §12.1); applicable Quality Gate result/evidence (Chapter 13 §13.9); Backward Consistency Check result (Chapter 12 §12.4); validator/freshness result (Chapter 11 §11.9); independent review evidence (Chapter 0 §3); Product Owner decision fact.

**KHÔNG thuộc prepared content — chỉ authoritative TẠI atomic recording boundary:** resulting MANIFEST transition identity (Chapter 14 §14.4.1) — tài liệu này KHÔNG đoán trước giá trị đó.

## 13. Explicit non-inclusion

```text
- `Approved`/`Phase 2 Approved` (phase decision outcome) KHÔNG phải một
  mục DoD tại đây (Chapter 12 §12.1 cấm tường minh vòng lặp định nghĩa)
  — nó LÀ outcome của Gate 3, xảy ra SAU khi mọi mục §1–§12 ở trên đã
  resolve.
- Chín trạng thái tách biệt, KHÔNG được conflate dưới bất kỳ hình thức
  nào:
    1. Phase 2 authorized (đã ghi nhận, transaction trước — "Phase 2
       Start Authorization")
    2. DoD defined (tài liệu này tồn tại, hiện v0.3 candidate)
    3. DoD accepted/incorporated (§Acceptance status §14 dưới — CHƯA)
    4. Prototype substantively complete (§3 criteria đạt — CHƯA bắt đầu)
    5. Quality Gate PASS (§2 evidence pinned theo declared gate-set —
       CHƯA)
    6. Gate 3 eligible (Chapter 12 §12.2 toàn bộ tám điểm resolve —
       CHƯA)
    7. Product Owner Phase 2 approval (Gate 3 decision — CHƯA)
    8. Phase 3 authorization (điều kiện riêng biệt bổ sung, bao gồm
       `P2-RETRO-001`, §11 trên — CHƯA)
    9. LIVE authorization (`OQ-002` phải đóng qua ADR riêng, KHÔNG qua
       Phase 2/Phase 3 authorization — CHƯA, KHÔNG được suy diễn từ bất
       kỳ trạng thái nào ở trên)
- Tài liệu này KHÔNG tự nó thực hiện: Phase-wide Backward Consistency
  Check (§10, CHỈ định nghĩa yêu cầu); Phase-level Gate review (§8);
  Phase 2 approval; `P2-RETRO-001` retrospective (§11); Phase 3 mở;
  deployment/implementation/exchange-integration authorization; LIVE
  authorization.
- Tài liệu này KHÔNG sửa Constitution/Domain Contract/ADR/Approved
  Engineering Foundation artifact/Product-UX Consolidated Stable
  content nào.
- Tài liệu này KHÔNG tạo ADR nào (§ADR Scope Rule check ở đầu tài liệu
  xác nhận `ADR_NOT_REQUIRED`).
- Tài liệu này KHÔNG author prototype screen/Figma/HTML/React artifact/
  UX flow/Product design decision/implementation code nào.
```

## 14. Acceptance status

```text
Product Owner acceptance của DoD này:   ĐÃ ghi nhận (2026-08-13,
                                        mechanical lifecycle-recording
                                        transaction `Phase 2 DoD v0.3
                                        Acceptance + Canonical
                                        Incorporation Recorder`, Decision
                                        Workflow — Chapter 0 §3). Nguyên
                                        văn: "ACCEPT PHASE 2 DOD V0.3 —
                                        INCORPORATE INTO PHASE 2
                                        CANONICAL PHASE PLAN."

Review history đầy đủ (chính xác, phân biệt lịch sử khỏi acceptance
  này):
  Review A trên v0.1:                   1 Major (`P2-DOD-A-MAJ-01`),
                                        1 Minor (`P2-DOD-A-MIN-01`),
                                        verdict `REVISION_REQUIRED`.
  v0.2 bounded correction:               đóng `P2-DOD-A-MAJ-01`/
                                        `P2-DOD-A-MIN-01`.
  Bounded Review A re-review trên v0.2:  CLEAN.
  Independent Review B trên v0.2:        Blocker 0/Major 3/Minor 0,
                                        verdict `REVISION_REQUIRED` —
                                        `P2-DOD-B-MAJ-01`/
                                        `P2-DOD-B-MAJ-02`/
                                        `P2-DOD-B-MAJ-03` identified.
  v0.3 bounded correction:               đóng `P2-DOD-B-MAJ-01`/
                                        `P2-DOD-B-MAJ-02`/
                                        `P2-DOD-B-MAJ-03`.
  Bounded Review A verification trên
    v0.3:                                CLEAN — Blocker 0/Major
                                        0/Minor 0.
  Independent bounded Review B trên
    v0.3:                                `P2-DOD-B-MAJ-01`/`02`/`03`
                                        CLOSED — New Blocker 0/New
                                        Major 0/New Minor 0, regression
                                        check CLEAN, `ADR_NOT_REQUIRED`,
                                        verdict
                                        `READY_FOR_PRODUCT_OWNER_
                                        DECISION`.

Canonical incorporation (Chapter 14
  §14.3.1) vào Phase-plan của Phase 2: ĐÃ tồn tại — bốn điều kiện
                                        §14.3.1 thỏa đầy đủ, cùng một
                                        evidence:

  1. Product Owner acceptance evidence resolve được:      CÓ (transaction
                                                            này).
  2. Cùng evidence đó xác định tường minh:
       Phase identity:                  Phase 2 — Product Prototype
       Roadmap phase-section version/
         content identity:              Chapter 14 — Roadmap, §14.2,
                                         v1.6, Locked, blob
                                         f2cd722218bd80b40241e26530a19198
                                         11fedad9 (verify trực tiếp tại
                                         transaction này, khớp MANIFEST)
       DoD version/content identity:    docs/phase-dod/phase-2-dod.md,
                                         v0.3, reviewed substantive blob
                                         876c4f099883cf3e5e2b3800d76510
                                         8662405e24 (verify trực tiếp
                                         trước edit, khớp HEAD trước
                                         transaction này)
       Explicit incorporation decision: "INCORPORATE INTO PHASE 2
                                         CANONICAL PHASE PLAN" (Product
                                         Owner, cùng nguyên văn quyết
                                         định trên)
  3. Evidence tồn tại TRƯỚC Phase 2 gate evaluation:        CÓ — Gate 3
                                                            CHƯA mở
                                                            (§Explicit
                                                            non-inclusion
                                                            §13 trên,
                                                            §2 gate-set
                                                            declaration).
  4. Đúng MỘT incorporation, KHÔNG xung đột:                CÓ — đây LÀ
                                                            acceptance
                                                            evidence DUY
                                                            NHẤT cho
                                                            Phase 2 DoD
                                                            tại boundary
                                                            này (verify
                                                            trực tiếp:
                                                            KHÔNG
                                                            candidate DoD
                                                            nào khác tồn
                                                            tại tại
                                                            `docs/
                                                            phase-dod/`).

  Hệ quả:                                Gate-set declaration tại §2 nay
                                        hợp lệ/authoritative cho mục
                                        đích Chapter 12/13 sử dụng — LÀ
                                        authoritative Phase 2 gate-set
                                        declaration kể từ transaction
                                        này (Chapter 12 §12.2 điểm 5:
                                        "Approved/Locked authoritative
                                        quality contract hoặc phase
                                        plan"): Trigger A APPLICABLE
                                        (applicable-invariant set
                                        {I-11, I-12}); Trigger B/C/D/E
                                        NOT APPLICABLE, mỗi kết luận
                                        điều kiện trên §4's deliverable
                                        boundary. **Chấp nhận declaration
                                        NÀY KHÔNG PHẢI Quality Gate
                                        PASS** — KHÔNG một gate nào đã
                                        "pass" tại transaction này.

Trạng thái hiện tại (verify trực tiếp mỗi mục, KHÔNG suy diễn):
  Product Owner acceptance:             ĐÃ ghi nhận (trên).
  Canonical incorporation:              ESTABLISHED (trên).
  Authoritative gate-set declaration:   ESTABLISHED (§2, hệ quả trên).
  Prototype substantive completion:     CHƯA established (CHƯA bắt đầu
                                        substantive Phase 2 work nào).
  Quality Gate PASS:                    CHƯA established — CHƯA chạy.
  Full-scope Backward Consistency
    Check:                              CHƯA chạy, CHƯA established
                                        "No conflict."
  Gate 3 eligibility:                   CHƯA established.
  Gate 3 mở:                             CHƯA (NOT OPENED).
  Phase 2 approval:                     CHƯA established.
  `P2-RETRO-001`:                        CHƯA thực hiện.
  Phase 3:                               NOT AUTHORIZED.
  LIVE:                                  NOT AUTHORIZED.
  Candidate uniqueness:                  Đây LÀ Phase 2 DoD candidate
                                        DUY NHẤT tồn tại (verify trực
                                        tiếp `docs/phase-dod/`) — KHÔNG
                                        conflicting candidate nào.
```

**Transaction này CHỈ ghi nhận DoD acceptance/incorporation. Nó KHÔNG:**

```text
tuyên bố Phase 2 DoD criteria (§1–§13) đã pass (VẪN LÀ tiêu chí CẦN đạt,
  KHÔNG phải ĐÃ đạt)
tuyên bố prototype substantively complete
chạy full-scope Backward Consistency Check (§10)
sinh Quality Gate PASS evidence (§2/§6)
thực hiện Phase-level Gate review (§8)
thực hiện P2-RETRO-001 retrospective (§11)
mở Gate 3
approve Phase 2
authorize Phase 3/deployment/implementation/LIVE
sửa §1–§13 substantive DoD content (17-surface + 21-UC completion
  requirement, I-11 Access-control audit authority, I-12 traceability
  requirement, Trigger B/C/D/E semantics, prototype boundary, evidence/
  review/BCC/validator requirements, P2-RETRO-001 boundary,
  ADR_NOT_REQUIRED result — tất cả byte-unchanged)
sửa Product/UX authority, Constitution, Phase 2 rules, ADR, hay
  architecture nào
```

## Change history

```text
ACCEPTANCE  2026-08-13  Product Owner acceptance + canonical
      incorporation — mechanical lifecycle recording, vai trò: `Phase 2
      DoD v0.3 Acceptance + Canonical Incorporation Recorder`. Quyết
      định: "ACCEPT PHASE 2 DOD V0.3 — INCORPORATE INTO PHASE 2
      CANONICAL PHASE PLAN." Reviewed substantive candidate: v0.3, blob
      `876c4f099883cf3e5e2b3800d765108662405e24` (Bounded Review A
      verification `CLEAN`; Independent bounded Review B: `P2-DOD-B-
      MAJ-01`/`02`/`03` CLOSED, New Blocker/Major/Minor 0/0/0,
      `ADR_NOT_REQUIRED`, `READY_FOR_PRODUCT_OWNER_DECISION`).
      `status: Draft -> Approved`, `approved_by: Product Owner`,
      `approved_at: "2026-08-13"`, `version: "0.3"` UNCHANGED (mechanical
      acceptance, KHÔNG substantive content change — §1–§13
      byte-unchanged). Canonical incorporation (Chapter 14 §14.3.1)
      established — Phase identity "Phase 2 — Product Prototype",
      Roadmap §14.2 v1.6 Locked (blob
      `f2cd722218bd80b40241e26530a1919811fedad9`), DoD v0.3/blob
      `876c4f099883cf3e5e2b3800d765108662405e24`, explicit incorporation
      decision — bốn điều kiện §14.3.1 thỏa bởi cùng evidence này.
      Gate-set declaration (§2) nay authoritative cho Chapter 12/13 —
      Trigger A applicable ({I-11, I-12}), Trigger B/C/D/E NOT
      APPLICABLE (điều kiện §4). Acceptance KHÔNG PHẢI Quality Gate
      PASS, KHÔNG chạy full-scope BCC, KHÔNG mở Gate 3, KHÔNG approve
      Phase 2, KHÔNG thực hiện `P2-RETRO-001`, KHÔNG authorize Phase 3/
      LIVE.
v0.3  2026-08-13  Bounded correction (Draft), đóng `P2-DOD-B-MAJ-01`/
      `P2-DOD-B-MAJ-02`/`P2-DOD-B-MAJ-03` (Independent Review B trên
      v0.2, Blocker 0/Major 3/Minor 0, `REVISION_REQUIRED`) — vai trò:
      `Phase 2 DoD v0.3 Bounded Correction Executor`. `P2-DOD-B-MAJ-01`:
      §3 criterion 3 sửa — 17-surface completion (`SCR-001`–`SCR-011`/
      `VIEW-001`–`VIEW-006`) VÀ 21-UC coverage nay CẢ HAI bắt buộc, KHÔNG
      cái nào thay thế cái kia; `P2-PROTOTYPE-001` batching giữ nguyên.
      `P2-DOD-B-MAJ-02`: §2/§4 sửa — I-11 authoritative Verification LÀ
      Chapter 2's Access-control audit (KHÔNG redefine), repo-scan/grep
      CHỈ LÀ supporting evidence; bounded Phase-2 interpretation (bốn
      điều kiện) định nghĩa tường minh. `P2-DOD-B-MAJ-03`: §12/§13/§14
      sửa mọi stale current-candidate pointer (v0.1 → v0.3), §14 viết
      lại review history đầy đủ chính xác (Review A v0.1 → v0.2
      correction → bounded re-review CLEAN → Independent Review B v0.2
      REVISION_REQUIRED → v0.3 correction, KHÔNG tuyên bố Review B đã
      re-review v0.3). KHÔNG đổi §1/§3 criterion 1-2/4-9/§5/§8-§11,
      Trigger B/C/D/E, I-1..I-10/I-13 kết luận, `ADR_NOT_REQUIRED`. KHÔNG
      surface/UC/SCR/VIEW ID mới, KHÔNG custody architecture invent.
      `status` VẪN `Draft`, `approved_by`/`approved_at` VẪN `null`. Blob
      v0.2 (trước) `26eb5875ef6c2c920d899581576093762c51ceff`.
v0.2  2026-08-13  Bounded correction (Draft), đóng `P2-DOD-A-MAJ-01`/
      `P2-DOD-A-MIN-01` (Review A) — vai trò: `Phase 2 DoD v0.2 Bounded
      Correction Executor`. `P2-DOD-A-MAJ-01`: §2 Trigger A v0.1 wrongly
      inferred "prototype không thực thi production behavior ⟹ mọi
      invariant không applicable" — vi phạm Chapter 2's per-invariant
      Scope. Sửa: đánh giá riêng I-1..I-13 theo đúng Scope — I-11/I-12
      (Scope "Toàn hệ thống") APPLICABLE, satisfied-by-absence + concrete
      conformance requirement; {I-1..I-10, I-13} NOT APPLICABLE, Scope
      exclusion structural. §4 mở rộng tương ứng, elevate hai requirement
      đã tồn tại một phần thành tường minh I-11/I-12 gate evidence.
      `P2-DOD-A-MIN-01`: đoạn mở đầu trích Chapter 12 §12.1 mơ hồ, sửa
      trích nguyên văn chính xác + phân biệt tường minh "trước Gate 3
      mở" KHÔNG PHẢI "trước Phase 2 bắt đầu" — KHÔNG reinterpret Phase 2
      Start Authorization đã ghi nhận. KHÔNG đổi §1/§3/§5–§14, Trigger
      B/C/D/E kết luận, ADR Scope Rule check kết luận. `status` VẪN
      `Draft`, `approved_by`/`approved_at` VẪN `null`. Blob v0.1 (trước)
      `672c0c2a4116da0ee74f39291c4fcf5260464902`.
v0.1  2026-08-13  Authored (Draft) — vai trò: `Phase 2 Product Prototype
      DoD v0.1 Candidate Author`. Derives §1 Phase identity từ Roadmap
      Chapter 14 §14.2's sparse Phase 2 declaration (KHÔNG sub-item
      list, khác mọi Phase khác) + Product/UX Consolidated Stable
      authority (Package 0.3-A/B/C). §2 Trigger A–E đánh giá ĐỘC LẬP
      (KHÔNG copy Phase 1.5's kết luận) — Trigger A applicable-nhưng-
      rỗng CÓ ĐIỀU KIỆN, Trigger B/C/D/E KHÔNG APPLICABLE CÓ ĐIỀU KIỆN,
      mọi điều kiện gắn trực tiếp §4's deliverable-boundary requirement
      (per-artifact fail-closed re-resolve nếu vi phạm). §3 completion
      criteria outcome-oriented, 9 mục, derive từ `ux-blueprint.md`
      §5–§14/§17 — dùng ĐÚNG stage taxonomy đã Consolidated (Research/
      Replay/Backtest/Paper/Review/Improve), KHÔNG paraphrase. §4
      deliverable boundary phân biệt tường minh prototype khỏi
      production frontend/backend/exchange integration/deployment/LIVE.
      §5 external dependency: OQ-002/OQ-003 + bốn `ux-blueprint.md` §15
      deferred item — tham chiếu, KHÔNG redecide. §11 `P2-RETRO-001`
      boundary: KHÔNG một Gate 3 prerequisite, CHỈ Phase 3 substantive-
      work prerequisite, đúng pattern `EF-RETRO-001`. ADR Scope Rule
      check: `ADR_NOT_REQUIRED` cho chính DoD authoring transaction này.
      `status: Draft`, `approved_by: null`, `approved_at: null` — CHƯA
      accepted, CHƯA incorporated. KHÔNG prototype screen/Figma/HTML/
      React artifact nào author tại transaction này.
```

**Việc tiếp theo:** Phase 2 substantive prototype/UX work (theo batch, `P2-PROTOTYPE-001`), sau đó một Phase 2 Approval Gate consolidated review (Review A + Independent Review B trên toàn bộ Phase 2 evidence, §8, bao gồm full-scope Backward Consistency Check, §10) — trước khi Product Owner đưa ra Gate 3 decision (Chapter 12 §12.2). Riêng biệt, ĐỘC LẬP với Approval Gate đó: `P2-RETRO-001` (§11) VẪN LÀ điều kiện bổ sung PHẢI COMPLETE trước Phase 3 substantive work, KHÔNG PHẢI trước chính Gate 3.
