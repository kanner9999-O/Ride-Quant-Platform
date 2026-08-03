---
id: phase-0-dod
title: "Phase 0 — Vision & Foundation: Definition of Done"
version: "0.1"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-03"
last_review: null
next_review: null
depends_on: ["00-governance", "12-approval-gates", "14-roadmap"]
---

# Phase 0 — Vision & Foundation: Definition of Done (DoD)

**Vai trò của tài liệu này:** đây là **DoD artifact** mà [Chapter 12 §12.1](../constitution/12-approval-gates.md) (Locked) khóa rule ("mỗi Phase phải có DoD cụ thể, viết ra và Product Owner chấp nhận TRƯỚC KHI phase/gate mở"), và [Chapter 14 §14.3](../constitution/14-roadmap.md) (Locked) khóa cardinality/nơi ở ("mỗi Phase phải resolve được đúng một authoritative DoD artifact"). Tài liệu này **định nghĩa tiêu chí** — nó **KHÔNG** phải bằng chứng "đã đạt tiêu chí", và nó **KHÔNG** tự nó là Product Owner acceptance. `Approved` là outcome của Approval Gate ([Chapter 12 §12.1](../constitution/12-approval-gates.md)) — **KHÔNG** phải một mục trong DoD này, và mục này **KHÔNG chứa** chính outcome đó (tránh vòng lặp định nghĩa đã bị Chapter 12 cấm tường minh).

**Authority boundary:** tài liệu này sở hữu **substantive DoD content của Phase 0** (criteria/evidence/validator/review/finding-closure/repository-consistency/phase-decision-bundle requirements áp cho chính Phase 0) — theo delegation từ [Chapter 14 §14.3](../constitution/14-roadmap.md). Nó **KHÔNG** định nghĩa lại: phase approval orchestration ([Chapter 12](../constitution/12-approval-gates.md)); review eligibility/cardinality ([Chapter 0 §3](../constitution/00-governance.md), [Chapter 11 §11.5](../constitution/11-adr-process.md)); quality-gate semantics/trigger A–E ([Chapter 13](../constitution/13-quality-gates.md)); ADR Scope Rule ([Chapter 0 §4b](../constitution/00-governance.md)); phase sequence/canonical Phase-plan model ([Chapter 14 §14.1–§14.2](../constitution/14-roadmap.md)); current version/status/state của bất kỳ tài liệu nào ([MANIFEST](../MANIFEST.md) theo [I-12](../constitution/02-platform-invariants.md)).

**Lifecycle state của chính DoD artifact này:** `status: Draft`, `approved_by: null`, `approved_at: null`. Đây là **DoD mới được author lần đầu** — theo Chapter 0 §7.1 Document Lifecycle (`Not Started → Draft → In Review → Revision Requested → Approved → Locked`), nó bắt đầu tại `Draft`. **Product Owner acceptance/incorporation của DoD này CHƯA được ghi nhận tại đây** — [Chapter 14 §14.3.1](../constitution/14-roadmap.md) khóa: canonical incorporation chỉ tồn tại khi Product Owner acceptance evidence resolve được VÀ xác định tường minh Phase identity/Roadmap-phase-section version/DoD version/explicit incorporation decision, tại một transaction RIÊNG do chính Product Owner tạo ra qua Decision Workflow ([Chapter 0 §3](../constitution/00-governance.md)). Tài liệu này **không tự claim** acceptance đó.

## 1. Phase identity

```text
Phase:              Phase 0 — Vision & Foundation
Roadmap source:     Chapter 14 §14.2 (Locked, v1.6, xem MANIFEST cho current version/status)
Sub-phase (work
unit, KHÔNG mở
Approval Gate
riêng — Chapter 14
§14.1):             0.1  Constitution (Chapter 0–14) + governance activation
                    0.2  Domain Model & Domain Contract (/docs/domain/)
                    0.3  Product Requirement · Use Case & Workflow · UX Blueprint
Phase-level output
bắt buộc:            ADR cho quyết định Domain thuộc diện ADR Required (Chapter 0 §4b)
Approval Gate:       một (1) — đơn vị chịu gate là Phase, không phải sub-phase (Chapter 14 §14.1)
```

## 2. Applicable gate set (Chapter 14 §14.4 declaration)

Theo [Chapter 13 §13.12](../constitution/13-quality-gates.md) (Locked), gate áp dụng theo **điều kiện kích hoạt** (trigger A–E), không phải mặc định. Phase 0 deliverable là tài liệu Constitution/Domain Contract/Product artifact — **không có executable implementation, không runtime module, không tier assignment, không isolation/custody/authorization boundary đã triển khai, không authoritative performance budget, không nằm trên production/operational path**. Phân tích trigger:

```text
A. Universal — invariant conformance:
   ÁP DỤNG cho MỌI Phase 0 deliverable, theo đúng Scope mà từng Platform Invariant
   (Chapter 2) tự khai báo. Đây là gate set chính của Phase 0.

B. Executable-implementation-triggered (coverage):
   KHÔNG áp dụng — Phase 0 deliverable không có executable implementation (resolved
   "not applicable", KHÔNG phải fail-closed — Chapter 13 §13.12 phân biệt tường minh
   "coverage not applicable" ≠ "coverage applicable but evidence missing").

C. Tier-triggered (Chaos/Parity Test):
   KHÔNG áp dụng — tier assignment (Chapter 13 §13.4) chưa xảy ra tại Phase 0; không
   module nào được build.

D. Responsibility/boundary-triggered (Security/data-quality/performance/observability):
   KHÔNG áp dụng — chưa có isolation/custody/authorization boundary triển khai (I-4/
   I-7/I-11), chưa có authoritative performance budget cho tài liệu Phase 0, Phase 0
   không nằm trên production/operational path. Domain Contract ĐỊNH NGHĨA schema cho
   authoritative/financial data nhưng KHÔNG "xử lý" nó (chưa có execution) — data-
   quality gate chưa trigger tại Phase 0.

E. Lifecycle-triggered (Schema/contract compatibility):
   ÁP DỤNG CÓ ĐIỀU KIỆN — CHỈ cho deliverable publish event schema/contract (Chapter
   10 §10.3): các Domain Contract dưới /docs/domain/ đã `Consolidated Stable` publish
   schema theo nghĩa đó — Chapter 10 compatibility discipline (đã hoạt động độc lập từ
   Phase 0.2) áp dụng cho MỌI thay đổi tiếp theo tới các schema này. Product
   Requirement/Use Case & Workflow/UX Blueprint (Package 0.3-A/B/C) KHÔNG publish
   event schema — E không áp dụng cho ba artifact đó.
```

**Gate set chính thức cho Phase deliverable của Phase 0 = Trigger A (universal invariant conformance, mọi deliverable) + Trigger E (schema/contract compatibility, chỉ Domain Contract publish schema).** Đây là gate-set declaration mà [Chapter 12 §12.2(5)](../constitution/12-approval-gates.md) resolve tới khi đánh giá Phase 0 Approval Gate — theo đúng authority bridge [Chapter 14 §14.3.1](../constitution/14-roadmap.md) khóa, declaration này CHỈ trở thành authoritative gate-set input cho Chapter 12/13 tại đúng thời điểm DoD này được Product Owner accept VÀ incorporate theo §14.3.1 — **chưa xảy ra tại thời điểm authoring này**.

## 3. Substantive completion criteria

```text
0.1 Constitution + governance activation:
  - Chapter 0–14 mỗi chapter resolve đúng một current version/status tại MANIFEST.
  - Chapter thuộc diện phải Locked trước khi Phase 0 gate mở: Chapter 0, 1, 2, 3, 4,
    5, 6, 7, 8, 9, 10, 11, 12, 13, 14 — TẤT CẢ `Locked` (xác nhận tại MANIFEST).
  - Governance activation (role-based review gate, ADR file immutability) hoạt động —
    xem ADR-011.

0.2 Domain Model & Domain Contract:
  - Toàn bộ Domain Contract package đã author (Package 0.2-A, B1–B3, C1–C7) đạt
    `Consolidated Stable` tại MANIFEST.
  - context-map.yaml resolve đầy đủ owned_contracts cho mọi context đã đăng ký.
  - Không Domain Contract nào còn finding Major/Blocker chưa resolved.

0.3 Product Requirement · Use Case & Workflow · UX Blueprint:
  - Package 0.3-A (`product-requirement.md`), 0.3-B (`use-case-workflow.md`), 0.3-C
    (`ux-blueprint.md`) mỗi package đạt `Consolidated Stable` tại MANIFEST.
  - PR→UC→UX lineage đầy đủ — mọi PR-XXX material-trace được tại ít nhất một UC-XXX
    (khi Use Case & Workflow là consuming layer) VÀ mọi UC/UX stable ID trace được về
    PR-XXX đã tồn tại — không mồ côi traceability theo bất kỳ hướng nào.
  - Baseline blob pinned tại mỗi package's `Consolidated Stable` transaction PHẢI
    khớp current content — không baseline nào stale mà chưa được flag tường minh cho
    review riêng.

ADR cho quyết định Domain thuộc diện ADR Required (Chapter 0 §4b):
  - Mọi quyết định Phase 0 rơi vào ADR Scope Rule đã có ADR tương ứng, ADR đó
    `Approved` (Chapter 11 §11.5–§11.6).

Toàn Phase 0 (cross-cutting):
  - Zero unresolved Blocker/Major finding trên bất kỳ deliverable nào thuộc scope
    Phase 0 tại thời điểm gate evaluation (xem §6 Finding-closure requirements).
  - Backward Consistency Check (Chapter 12 §12.4) = `No conflict` giữa toàn bộ
    deliverable Phase 0 và mọi authority đã Locked liên quan.
```

## 4. Evidence requirements

```text
Required deliverable evidence (Chapter 12 §12.1):
  - Constitution: 15 chapter file, mỗi chapter version/status/approved_by/approved_at
    resolve tại MANIFEST.
  - Domain Model: toàn bộ file dưới /docs/domain/ + context-map.yaml, mỗi package
    (0.2-A/B1-B3/C1-C7) có review evidence (ChatGPT Review A + Independent Review B)
    pinned.
  - Product Requirement/Use Case & Workflow/UX Blueprint: mỗi package (0.3-A/B/C) có
    review evidence pinned, đúng exact baseline blob per Consolidated Stable
    transaction.
  - ADR: file ADR tương ứng, `status: Approved`, review evidence pinned tại chính
    ADR file (Chapter 11 §11.6).

Evidence pinning rule: mọi evidence trên phải pin exact blob/commit identity — KHÔNG
mutable "phiên bản mới nhất" reference (Chapter 14 §14.3 "cấm mutable reference").
```

## 5. Validator requirements

```text
- MANIFEST freshness check (Chapter 11 §11.9, I-12): mọi deliverable Phase 0 resolve
  đúng version/status/blob hiện tại tại MANIFEST — không stale pointer.
- Stable-ID integrity: mọi ID namespace (PR-XXX/UC-XXX/WS/NAV/SCR/VIEW/FLOW/STATE/
  Domain Contract entity-event) unique, sequential, contiguous trong phạm vi đã khai
  báo — không gap, không renumber ngầm.
- YAML frontmatter validity: mọi living document frontmatter parse được, field bắt
  buộc (id/version/status/owner/approved_by/approved_at) hiện diện.
- Cross-reference resolvability: mọi internal link/reference (PR→UC, UC→UX, Domain
  Contract cross-context) resolve được về đúng một target tồn tại.
```

## 6. Review requirements

```text
Theo Chapter 0 §3 / Chapter 11 §11.5 (tham chiếu, KHÔNG định nghĩa lại):
  - Tối thiểu hai independent review từ actor giữ role AI Technical Architect tại
    review boundary.
  - Hai actor identity khác nhau thực hiện (xem team.yaml cho alias resolution, đóng
    F-04).
  - Reviewer evidence pinned tại đúng deliverable/decision boundary.
  - Reviewer ngang hàng — sự TỒN TẠI của review là điều kiện bắt buộc; kết luận
    KHÔNG ràng buộc quyết định cuối của Product Owner.
```

## 7. Finding-closure requirements

```text
- Mọi finding Blocker/Major từ bất kỳ review round nào (author self-review, ChatGPT
  Review A, Independent Review B, delta review, audit — bao gồm Phase 0 Exit
  Readiness Audit F-01–F-08) phải resolved (đóng) tại MANIFEST/CHANGELOG evidence
  TRƯỚC khi Phase 0 Approval Gate mở.
- Finding Minor có thể remain open nếu Product Owner tường minh chấp nhận rủi ro tồn
  đọng (ghi rõ tại decision evidence) — KHÔNG ngầm định.
- Finding "chưa đóng" KHÔNG tự động chặn gate NẾU Product Owner tường minh accept
  residual risk — nhưng phải ghi nhận tường minh, không suy diễn.
```

## 8. Repository-consistency requirements

```text
- Backward Consistency Check (Chapter 12 §12.4, cả hai chiều A và B) chạy trên TOÀN
  BỘ deliverable Phase 0 đối chiếu mọi authority Locked liên quan — kết quả `No
  conflict` bắt buộc trước gate.
- MANIFEST là authoritative source DUY NHẤT cho current version/status/state — không
  state store cạnh tranh (I-12).
- Package lifecycle (`Consolidated Stable`) và artifact lifecycle (`Draft`/`Approved`/
  `Locked`) giữ tách biệt tường minh trên MỌI package — không conflate.
```

## 9. Phase-decision bundle requirements (Chapter 14 §14.4.1–§14.4.2)

Tại đúng atomic recording boundary (Chapter 14 §14.4.2), bundle phải pin — **Chapter 14 authority (prepared trực tiếp tại DoD/Roadmap):**

```text
- canonical Phase identity (= "Phase 0 — Vision & Foundation")
- exact Roadmap version/content identity đã dùng (Chapter 14 §14.2, hiện v1.6)
- exact accepted-DoD identity/content version đã incorporate (tài liệu này, khi được
  accept — hiện v0.1, CHƯA accepted)
- exact gate-set declaration identity/content resolve từ đó (§2 phía trên)
```

**Reference-only (authority chapter khác, DoD KHÔNG redefine):** Product Owner DoD-acceptance evidence (Chapter 0 §3); required/submitted deliverable evidence (§4 phía trên, Chapter 12 §12.1); applicable Quality Gate result/evidence (Chapter 13 §13.9); Backward Consistency Check result (Chapter 12 §12.4); validator/freshness result (Chapter 11 §11.9); independent review evidence (Chapter 0 §3); Product Owner decision fact.

**KHÔNG thuộc prepared content — chỉ authoritative TẠI atomic recording boundary:** resulting MANIFEST transition identity (Chapter 14 §14.4.1) — tài liệu này KHÔNG đoán trước giá trị đó.

## 10. Explicit non-inclusion

`Approved` (phase decision outcome) **KHÔNG** phải một mục DoD tại đây (Chapter 12 §12.1 cấm tường minh vòng lặp định nghĩa) — nó là **outcome** của Approval Gate, xảy ra SAU khi mọi mục §3–§9 ở trên đã resolve.

## 11. Acceptance status

```text
Product Owner acceptance của DoD này:  CHƯA ghi nhận.
Canonical incorporation (Chapter 14
  §14.3.1) vào Phase-plan của Phase 0:  CHƯA tồn tại — bốn điều kiện §14.3.1 (evidence
                                        resolve, Phase/Roadmap-version/DoD-version/
                                        explicit-incorporation-decision xác định, tồn
                                        tại trước gate, đúng một incorporation) CHƯA
                                        thỏa.
Hệ quả:                                Mọi gate-set declaration tại §2 KHÔNG hợp lệ
                                        cho mục đích Chapter 12/13 sử dụng cho tới khi
                                        Product Owner cung cấp acceptance evidence
                                        đúng định dạng yêu cầu, tại một task/transaction
                                        RIÊNG.
```

**Tài liệu này KHÔNG tuyên bố Phase 0 hoàn thành, KHÔNG mở Approval Gate, KHÔNG authorize Phase 1.**
