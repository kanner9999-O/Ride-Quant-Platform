---
id: phase-1.5-dod
title: "Phase 1.5 — Engineering Foundation Definition of Done"
version: "0.2"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-13"
last_review: null
next_review: null
depends_on: ["00-governance", "11-adr-process", "12-approval-gates", "13-quality-gates", "14-roadmap"]
---

# Phase 1.5 — Engineering Foundation: Definition of Done (DoD)

**Vai trò của tài liệu này:** đây LÀ **DoD candidate artifact** mà [Chapter 12 §12.1](../constitution/12-approval-gates.md) (Locked, v1.5) khóa rule ("mỗi Phase phải có DoD cụ thể, viết ra và Product Owner chấp nhận TRƯỚC KHI phase/gate mở"), VÀ [Chapter 14 §14.3](../constitution/14-roadmap.md) (Locked, v1.6) khóa cardinality/nơi ở ("mỗi Phase phải resolve được đúng một authoritative DoD artifact"). Tài liệu này **định nghĩa tiêu chí** cho Phase 1.5 — nó **KHÔNG** phải bằng chứng "đã đạt tiêu chí", VÀ nó **KHÔNG** tự nó là Product Owner acceptance. `Approved`/`Phase 1.5 Approved` LÀ outcome của Phase 1.5 Approval Gate ([Chapter 12 §12.1](../constitution/12-approval-gates.md)) — **KHÔNG** phải một mục trong DoD này, VÀ mục này **KHÔNG chứa** chính outcome đó (tránh vòng lặp định nghĩa Chapter 12 đã cấm tường minh).

**Nguồn gốc:** tài liệu này chuyển hóa Chapter 14 §14.2's Phase 1.5 deliverable list ("Monorepo · Coding Standard · Naming · Logging · Config · Error Handling · Testing · CI/CD") thành explicit Phase 1.5 gate criteria, theo cùng pattern `phase-0-dod.md`/`phase-1-dod.md` — DoD artifact riêng biệt cho mỗi Phase, KHÔNG tái sử dụng structure của Phase khác LÀM authority, CHỈ LÀM structural precedent (theo đúng chỉ dẫn task này).

**Authority boundary:** tài liệu này sở hữu **substantive DoD content của Phase 1.5** (criteria/evidence/validator/review/finding-closure/repository-consistency/phase-decision-bundle requirements áp cho chính Phase 1.5) — theo delegation từ [Chapter 14 §14.3](../constitution/14-roadmap.md). Nó **KHÔNG** định nghĩa lại: phase approval orchestration ([Chapter 12](../constitution/12-approval-gates.md)); review eligibility/cardinality ([Chapter 0 §3](../constitution/00-governance.md), [Chapter 11 §11.5](../constitution/11-adr-process.md)); quality-gate semantics/trigger A–E ([Chapter 13 §13.12](../constitution/13-quality-gates.md)); ADR Scope Rule ([Chapter 0 §4b](../constitution/00-governance.md)); phase sequence/canonical Phase-plan model ([Chapter 14 §14.1–§14.2](../constitution/14-roadmap.md)); current version/status/state của bất kỳ tài liệu nào ([MANIFEST](../MANIFEST.md) theo [I-12](../constitution/02-platform-invariants.md)); hay `EF-RETRO-001` (Phase 1.5 rules, KHÔNG redefine — xem §11 dưới cho boundary chính xác).

**v0.2 — bounded correction (2026-08-13), đóng `EF-DOD-A-MAJ-01` (Review A):** §2 v0.1 resolve Trigger C VÀ Trigger D bằng rationale KHÔNG được Chapter 13 §13.12 hỗ trợ. (1) Trigger C: v0.1 nói Chaos/Parity Test "đòi hỏi executable implementation đã build (§13.12 trigger B tiền đề)" — SAI, §13.12's mệnh đề "tier cũng đặt coverage floor (chỉ áp khi coverage đã trigger theo B)" CHỈ áp cho sub-effect "coverage floor," KHÔNG áp cho chính việc Chaos/Parity Test có trigger — Trigger C LÀ tier-triggered ĐỘC LẬP khỏi Trigger B. Sửa: đánh giá lại từ Chapter 13 §13.4's tier-resolution chain (ba nhánh: runtime module/executable-artifact-thuộc-module/standalone-executable-declared) — KHÔNG category Phase 1.5 nào (7 ADR + 8 living convention) thuộc bất kỳ nhánh nào (TẤT CẢ LÀ governance/decision document, KHÔNG runtime/executable) — Trigger C KHÔNG APPLICABLE VÌ KHÔNG nhánh tier-resolution nào áp dụng cho KIỂU artifact này, KHÔNG PHẢI vì thiếu executable LÀM tiền đề. (2) Trigger D: v0.1 dùng "KHÔNG declare boundary MỚI" LÀM tiêu chí N/A — SAI, §13.12 mục D KHÔNG phân biệt boundary mới hay kế thừa, trigger LÀ "khi artifact CÓ" boundary/responsibility đó. Sửa: đánh giá lại first-principles cho `config.md`/`ADR-028`, `error-handling.md`/`ADR-029`, `ci-cd.md`/`ADR-030` (tham chiếu `ADR-017`/`module-registry.yaml` LÀM context, KHÔNG PHẢI Phase 1.5 deliverable) — KHÔNG category nào TỰ nó CÓ isolation/custody/authorization boundary, xử lý authoritative/financial data, có performance budget áp dụng, hay nằm trên production/operational path — TẤT CẢ CHỈ mô tả/tham chiếu boundary người khác giữ (vd `ADR-017`'s custody/signing boundary), KHÔNG PHẢI TỰ nó LÀ boundary đó — Trigger D KHÔNG APPLICABLE VÌ artifact tự thân KHÔNG CÓ responsibility đó, KHÔNG PHẢI vì boundary "không mới." **KHÔNG đổi:** kết luận tổng thể (Trigger A CHỈ áp dụng, B/C/D/E KHÔNG APPLICABLE cho toàn bộ Phase 1.5) — CHỈ reasoning đằng sau C/D được sửa để authority-grounded. **KHÔNG đổi:** §1 Phase identity, §3 substantive completion criteria, §4–§8 (evidence/validator/review/finding-closure/BCC requirements), §9 residual list, §10 EF-RETRO-001 boundary, §11 phase-decision bundle requirements, §12 explicit non-inclusion, §13 acceptance status. `status` VẪN `Draft`, `approved_by`/`approved_at` VẪN `null` — CHƯA accepted, CHƯA incorporated.

## 1. Phase identity

```text
Phase:              Phase 1.5 — Engineering Foundation
Roadmap source:     Chapter 14 §14.2 (Locked, v1.6, xem MANIFEST cho current
                     version/status)
Deliverable scope
(Chapter 14 §14.2,
KHÔNG redefine
tại đây):            Monorepo · Coding Standard · Naming · Logging · Config ·
                     Error Handling · Testing · CI/CD  (tám category, "tài liệu
                     SỐNG, sửa qua ADR")
Phase-level output
bắt buộc:            ADR cho quyết định thuộc diện ADR Required (Chapter 0
                     §4b) — MỘT category (Testing) resolved trực tiếp dưới
                     existing Locked authority (Chapter 3 §3.2 carve-out),
                     KHÔNG cần ADR riêng (xem §3.2 dưới).
Approval Gate:       một (1) — đơn vị chịu gate LÀ Phase, KHÔNG phải category/
                     sub-phase (Chapter 14 §14.1)
```

Category→artifact mapping cụ thể (đường dẫn file, để tiện resolve — **KHÔNG** authoritative cho version/lifecycle, current state PHẢI resolve từ [MANIFEST](../MANIFEST.md) theo I-12, KHÔNG từ bảng này):

```text
Monorepo         adr/ADR-024.md, engineering/monorepo.md
Coding Standard  adr/ADR-025.md, engineering/coding-standard.md
Naming           adr/ADR-026.md, engineering/naming.md
Logging          adr/ADR-027.md, engineering/logging.md
Config           adr/ADR-028.md, engineering/config.md
Error Handling   adr/ADR-029.md, engineering/error-handling.md
Testing          engineering/testing.md  (KHÔNG có ADR riêng — §3.2 dưới)
CI/CD            adr/ADR-030.md, engineering/ci-cd.md  (CI-side CHỈ — CD/
                 deployment/LIVE KHÔNG thuộc phạm vi Phase 1.5, xem §3.4)
```

## 2. Applicable gate set (Chapter 14 §14.4 declaration)

Theo [Chapter 13 §13.12](../constitution/13-quality-gates.md) (Locked), gate áp dụng theo **điều kiện kích hoạt** (trigger A–E), KHÔNG phải mặc định. Phase 1.5 deliverable LÀ **Engineering Foundation convention/architecture-decision artifact** — KHÔNG có executable implementation, KHÔNG runtime module đã build (0 module đã build tại boundary authoring này, xác nhận nhất quán xuyên toàn bộ tám category transaction), KHÔNG concrete boundary/published-contract mới được declare bởi chính những artifact này. Phân tích trigger:

```text
A. Universal — invariant conformance:
   ÁP DỤNG cho TOÀN BỘ tám category deliverable (7 ADR + 8 living convention),
   theo đúng Scope mà từng Platform Invariant (Chapter 2) tự khai báo — đây
   LÀ gate set chính của Phase 1.5, cùng logic phase-1-dod.md §2 đã áp dụng
   cho architecture artifact.

B. Executable-implementation-triggered (coverage):
   KHÔNG APPLICABLE cho TOÀN BỘ tám category — verify trực tiếp: KHÔNG
   executable implementation nào tồn tại (`python/`/`go/` CHỈ chứa README
   placeholder, KHÔNG dependency manifest/build artifact). "Coverage not
   applicable" (KHÔNG executable implementation) ≠ "coverage applicable but
   evidence missing" (Chapter 13 §13.12 phân biệt tường minh) — resolved
   "not applicable" tại boundary này, KHÔNG phải fail-closed.

C. Tier-triggered (Chaos/Parity Test):
   [v0.2 sửa, đóng `EF-DOD-A-MAJ-01` phần Trigger C: v0.1 nói Chaos/Parity
     Test "đòi hỏi executable implementation đã build (§13.12 trigger B
     tiền đề)" — SAI, Chapter 13 §13.12 KHÔNG định nghĩa quan hệ tiền đề
     đó. §13.12 mục C viết: "Chaos Test → Tier 0; Parity Test → Tier 1
     (decision-pipeline responsibility); tier CŨNG đặt coverage floor (CHỈ
     áp khi coverage ĐÃ trigger theo B)" — mệnh đề "chỉ áp khi... theo B"
     CHỈ áp cho phần "tier đặt coverage floor" (một sub-effect của tier),
     KHÔNG áp cho chính việc Chaos/Parity Test có trigger hay không. Trigger
     C LÀ tier-triggered ĐỘC LẬP, KHÔNG phụ thuộc Trigger B.]
   Đánh giá lại từ nguồn: Chaos/Parity Test trigger phụ thuộc criticality
   tier CỦA CHÍNH artifact đó resolve được (Chapter 13 §13.4). §13.4 tự nó
   giới hạn tier-resolution chain cho ba loại subject: (1) runtime module
   (`module-registry.yaml`, Chapter 7 §7.5); (2) executable artifact thuộc
   MỘT canonical owning module; (3) standalone executable artifact với
   authoritative quality-tier declaration riêng. Verify trực tiếp: KHÔNG
   category nào trong tám category Phase 1.5 (7 ADR + 8 living convention)
   LÀ runtime module, executable artifact thuộc module, hay standalone
   executable artifact — TẤT CẢ LÀ governance/decision/convention document
   (KHÔNG thực thi runtime nào). KHÔNG nhánh nào của §13.4's tier-resolution
   chain áp dụng cho loại artifact này — tier KHÔNG resolve được cho bất kỳ
   category nào (KHÔNG PHẢI vì thiếu executable implementation làm tiền đề
   cho C, MÀ vì chính KIỂU artifact này nằm ngoài phạm vi §13.4 định nghĩa
   subject nào cần/có thể resolve tier). KẾT QUẢ: Chaos Test (Tier 0)/
   Parity Test (Tier 1, decision-pipeline responsibility) KHÔNG APPLICABLE
   cho toàn bộ tám category tại boundary này — KHÔNG category nào mang
   decision-pipeline responsibility hay bất kỳ tier nào khác. NẾU một
   artifact Phase 1.5 tương lai (ngoài phạm vi bảy ADR/tám convention hiện
   có) trở thành runtime module/executable artifact có tier resolve được,
   trigger C PHẢI re-confirm tại đúng thời điểm gate evaluation — KHÔNG
   suy diễn từ declaration tại đây.

D. Responsibility/boundary-triggered (Security/data-quality/performance/
   observability):
   [v0.2 sửa, đóng `EF-DOD-A-MAJ-01` phần Trigger D: v0.1 dùng tiêu chí
     "KHÔNG declare một boundary MỚI" LÀM lý do N/A — SAI, Chapter 13
     §13.12 mục D KHÔNG đòi hỏi boundary phải "mới" — trigger LÀ "khi
     artifact CÓ isolation/custody/authorization boundary" (I-4/I-7/I-11),
     "xử lý authoritative/financial data" (I-9/I-13), "CÓ authoritative
     performance budget áp dụng," hay "nằm trên production/operational
     path" — KHÔNG PHÂN BIỆT boundary đó mới hay kế thừa.]
   Đánh giá lại từ first principles, verify trực tiếp từng artifact liên
   quan (`config.md`/`ADR-028`, `error-handling.md`/`ADR-029`, `ci-cd.md`/
   `ADR-030`, tham chiếu `ADR-017`/`module-registry.yaml` LÀM context —
   CẢ HAI KHÔNG PHẢI Phase 1.5 deliverable, KHÔNG tự chịu gate tại đây):
     Security (I-4/I-7/I-11): `config.md` §8 VÀ `error-handling.md` §9
       (Security and redaction) VÀ `ci-cd.md` §11 ĐỀU CHỈ mô tả CÁCH
       future implementation code NÊN reference/tránh expose secret —
       CHÍNH những living convention document này KHÔNG tự thực thi, KHÔNG
       tự giữ credential, KHÔNG tự thực hiện authorization check tại
       runtime — chúng LÀ governance/convention artifact, KHÔNG PHẢI
       chính isolation/custody/authorization boundary đó. `ADR-017` (đã
       Approved tại Phase 1, KHÔNG PHẢI Phase 1.5 deliverable) LÀ nơi
       custody/signing boundary THẬT sự tồn tại — nhưng ADR-017 KHÔNG
       nằm trong tám category đang được DoD này gate. KẾT LUẬN: KHÔNG
       category Phase 1.5 nào (7 ADR + 8 convention) TỰ nó CÓ một
       isolation/custody/authorization boundary — Security sub-trigger
       KHÔNG APPLICABLE cho tám category, KHÔNG PHẢI vì boundary "không
       mới," MÀ vì bản thân các document Phase 1.5 KHÔNG PHẢI/KHÔNG chứa
       chính boundary đó.
     Data quality/numerical precision (I-9/I-13): KHÔNG category nào xử
       lý authoritative/financial data trực tiếp — TẤT CẢ LÀ convention/
       decision document về CÁCH code tương lai nên viết, KHÔNG PHẢI data
       processor. KHÔNG APPLICABLE.
     Performance (§13.7): KHÔNG authoritative performance budget nào áp
       dụng cho bất kỳ category Phase 1.5 nào (KHÔNG runtime code, KHÔNG
       benchmark subject). KHÔNG APPLICABLE.
     Observability: KHÔNG category nào nằm trên production/operational
       path (KHÔNG runtime component). KHÔNG APPLICABLE.
   KẾT QUẢ: Trigger D KHÔNG APPLICABLE cho toàn bộ tám category tại
   boundary này — lý do CHÍNH XÁC LÀ các artifact Phase 1.5 tự thân LÀ
   governance/convention document, KHÔNG tự CÓ/thực thi bất kỳ boundary/
   responsibility nào trong bốn sub-trigger D liệt kê, KHÔNG PHẢI vì
   boundary chúng tham chiếu "không mới." NẾU một concrete boundary/
   responsibility MỚI phát sinh (thuộc về CHÍNH một Phase 1.5 artifact,
   KHÔNG PHẢI artifact khác nó tham chiếu) trước gate evaluation thực tế,
   trigger D PHẢI re-confirm tại đúng thời điểm đó (xem "Xác nhận bắt
   buộc" dưới).

E. Lifecycle-triggered (Schema/contract compatibility):
   KHÔNG APPLICABLE — verify trực tiếp: KHÔNG category nào trong tám
   category publish một Event/API/Domain contract/schema MỚI (Chapter 10
   §10.3) — cả bảy ADR (024–030) VÀ tám living convention đều LÀ
   Engineering Foundation baseline-existence/style-tooling decision, KHÔNG
   PHẢI published-contract artifact. Domain/Event/API contract authority
   (`/docs/domain/`) KHÔNG chạm bởi bất kỳ category nào (xác nhận tường
   minh nhất quán xuyên mọi transaction Phase 1.5).
```

**Gate set chính thức cho Phase deliverable của Phase 1.5 = Trigger A CHỈ (universal, toàn bộ 7 ADR + 8 living convention).** Trigger B/C/D/E KHÔNG APPLICABLE cho toàn bộ Phase 1.5 tại boundary authoring này. Đây LÀ gate-set declaration mà [Chapter 12 §12.2(5)](../constitution/12-approval-gates.md) resolve tới khi đánh giá Phase 1.5 Approval Gate — theo đúng authority bridge [Chapter 14 §14.3.1](../constitution/14-roadmap.md) khóa, declaration này CHỈ trở thành authoritative gate-set input cho Chapter 12/13 tại đúng thời điểm DoD này được Product Owner accept VÀ incorporate theo §14.3.1 — **chưa xảy ra tại thời điểm authoring này**.

**Xác nhận bắt buộc (fail-closed rule, Chapter 13 §13.12):** nếu một trigger condition (C/D/E cụ thể) KHÔNG resolve được cho một category cụ thể tại thời điểm gate evaluation thực tế — applicability chưa xác định = eligibility incomplete, **KHÔNG** được mặc định "gate không áp dụng" để bỏ qua. Bảng trên LÀ đánh giá tại boundary authoring (2026-08-13); gate evaluation thực tế PHẢI re-confirm trigger C/D/E cho từng category tại đúng thời điểm đó — verify trực tiếp lại, KHÔNG suy diễn từ declaration này.

## 3. Substantive completion criteria

```text
3.1 Category completion:
    - TOÀN BỘ tám (8) category Phase 1.5 (Monorepo, Coding Standard, Naming,
      Logging, Config, Error Handling, Testing, CI/CD) đạt `status: Approved`
      tại MANIFEST cho MỌI artifact thuộc category đó (ADR khi applicable +
      living convention).
    - `Approved` LÀ artifact lifecycle state (Chapter 0 §7.1), KHÁC `Locked`
      — living convention `Approved` KHÔNG immutable byte-for-byte như ADR
      `Approved`; đây LÀ trạng thái hợp lệ cho mục đích tiêu chí này, KHÔNG
      cần `Locked` bổ sung.

3.2 ADR closure (bao gồm intentional ADR-absent category):
    - MỌI ADR thực sự được kích hoạt (actually-triggered) dưới ADR Scope Rule
      (Chapter 0 §4b) LIÊN QUAN Phase 1.5 category phải `Approved` (Chapter
      11 §11.5–§11.6) trước Phase 1.5 Approval Gate: `ADR-024` (Monorepo),
      `ADR-025` (Coding Standard), `ADR-026` (Naming), `ADR-027` (Logging),
      `ADR-028` (Config), `ADR-029` (Error Handling), `ADR-030` (CI/CD) —
      TẤT CẢ bảy ADR hiện `status: Approved` tại MANIFEST.
    - Testing LÀ MỘT ngoại lệ TƯỜNG MINH, KHÔNG PHẢI một gap: một ADR Scope
      Check riêng biệt (transaction trước khi author `testing.md`) kết luận
      `ADR_NOT_REQUIRED` — Chapter 3 §3.2 (Locked v1.4) ĐÃ pre-resolve cả
      baseline-existence VÀ scope boundary (style/tooling-only vs Chapter 13
      coverage/tier) cho category này, KHÔNG giống bảy category kia. Tiêu
      chí này coi Testing LÀ satisfied bởi `testing.md` `Approved` MỘT
      MÌNH, KHÔNG đòi hỏi một ADR-031/tương đương nào.
    - ADR CONDITIONALLY REQUIRED (nếu có, phát sinh trong quá trình category
      correction) chỉ bắt buộc khi trigger cụ thể của điều kiện đó thực sự
      xảy ra tại thời điểm gate evaluation — hypothetical conditional ADR
      KHÔNG được yêu cầu nếu trigger KHÔNG xảy ra.

3.3 Zero unresolved architecture-review Blocker/Major:
    - KHÔNG unresolved Phase 1.5 Blocker/Major nào được phép còn lại trên
      bất kỳ deliverable Phase 1.5 nào (7 ADR + 8 living convention) tại
      thời điểm gate evaluation (xem §7 Finding-closure requirements).
    - Accepted non-blocking Minor residual (§9 dưới) KHÔNG tự động LÀ
      Blocker/Major cho mục đích tiêu chí này — phân biệt bắt buộc.

3.4 CI-vs-CD boundary preserved:
    - `ADR-030`/`ci-cd.md` CHỈ establish phần CI (build/test/lint/validation
      automation, Foundation-level) — deployment/promotion/release/LIVE
      authorization KHÔNG thuộc phạm vi Phase 1.5 dưới bất kỳ hình thức nào,
      VẪN thuộc `Phase 7 — Deployment` (Chapter 14 §14.2) VÀ governance
      riêng biệt tương lai (`ADR-030` §3/§6, KHÔNG redefine tại đây). Tiêu
      chí này KHÔNG coi thiếu CD/deployment content LÀ một gap — đó LÀ
      phạm vi ĐÃ intentionally excluded, KHÔNG PHẢI unfinished Phase 1.5
      work.

3.5 Cross-category consistency:
    - Mỗi living convention (`monorepo.md`...`ci-cd.md`) CHỈ implement chi
      tiết reversible dưới authority ADR/Chapter tương ứng của chính nó —
      KHÔNG category nào redefine authority của category khác (vd
      `error-handling.md` KHÔNG redefine Logging level/schema; `ci-cd.md`
      KHÔNG redefine Testing/Chapter 13 flaky-test policy) — xác nhận
      tường minh, verify trực tiếp tại chính mỗi bounded-correction
      transaction đã thực hiện xuyên Phase 1.5.
    - KHÔNG category nào redefine Chapter 12 Approval Gate semantics, Chapter
      13 Quality Gate semantics, `ADR-017` Custody & Signing boundary, hay
      Domain/Event/API contract authority (`/docs/domain/`) — xác nhận
      tường minh, nhất quán xuyên toàn bộ Phase 1.5.
```

## 4. Evidence requirements

```text
Required deliverable evidence (Chapter 12 §12.1):
  - Mỗi 7 ADR (024–030): `status: Approved`, review evidence (Review A +
    Independent Review B) pinned tại chính ADR file, resulting post-approval
    lifecycle blob resolve tại MANIFEST.
  - Mỗi 8 living convention: `status: Approved` (Testing/CI-CD ngoại lệ
    KHÔNG có ADR gốc — xem §3.2), review evidence pinned, blob resolve tại
    MANIFEST.
  - ADR Scope Check evidence cho Testing (`ADR_NOT_REQUIRED`) VÀ CI/CD
    (`PARTIAL_ADR_REQUIRED`, dẫn tới `ADR-030`) — pinned tại chính
    transaction report tương ứng (CHANGELOG.md), tham chiếu được.

Applicable Quality Gate evidence (Chapter 13 §13.9 evidence contract, KHÔNG
redefine tại đây):
  - Trigger A: evidence pinned cho TOÀN BỘ 7 ADR + 8 living convention tại
    thời điểm gate evaluation.
  - Trigger B/C/D/E: KHÔNG evidence bắt buộc tại Phase 1.5 gate — resolved
    KHÔNG APPLICABLE tại boundary này (§2).
  - Gate result PHẢI LÀ **pinned evidence** (blob/commit identity) — KHÔNG
    được suy diễn ngầm CHỈ từ một Review A/Independent Review B "CLEAN" —
    review clean VÀ quality-gate evidence LÀ hai fact tách biệt.

Evidence pinning rule: mọi evidence trên PHẢI pin exact blob/commit identity
— KHÔNG mutable "phiên bản mới nhất" reference (Chapter 14 §14.3).
```

## 5. Validator requirements

```text
- MANIFEST freshness check (Chapter 11 §11.9, I-12): mọi deliverable Phase
  1.5 (7 ADR + 8 living convention) resolve đúng version/status/lifecycle/
  blob hiện tại tại MANIFEST — không stale pointer.
- YAML frontmatter validity: mọi living document/ADR frontmatter parse
  được, field bắt buộc (id/version/status/owner) hiện diện.
- Cross-reference resolvability: mọi internal reference (living convention
  → ADR authority, ADR → Constitution chapter, category → category boundary
  reference) resolve được về đúng một target tồn tại — không mồ côi.
- Required freshness/validator check PHẢI pass TRƯỚC gate eligibility —
  validator LÀ blocking consistency check, KHÔNG phải approval authority
  (Chapter 12 §12.2).
```

## 6. Review requirements

```text
Theo Chapter 0 §3 / Chapter 11 §11.5 (tham chiếu, KHÔNG định nghĩa lại):
  - Tối thiểu HAI (2) eligible independent review từ actor giữ role AI
    Technical Architect **tại chính Phase Approval Gate boundary** —
    category-level Review A/Independent Review B evidence (đã pin per-
    category trong quá trình Phase 1.5) KHÔNG tự động thay thế yêu cầu này
    — đây LÀ một review boundary riêng, cấp Phase (cùng nguyên tắc
    phase-1-dod.md §6 đã pin, KHÔNG redefine).
  - Hai actor identity khác nhau thực hiện.
  - Reviewer evidence pinned tại đúng Phase Approval Gate boundary.
  - Reviewer ngang hàng — sự TỒN TẠI của review LÀ điều kiện bắt buộc;
    kết luận KHÔNG ràng buộc quyết định cuối của Product Owner.
```

## 7. Finding-closure requirements

```text
- Mọi finding Blocker/Major từ bất kỳ review round nào (category Review A/
  Independent Review B, bounded correction, Phase 1.5 Approval Gate
  consolidated review) PHẢI resolved (đóng) tại MANIFEST/CHANGELOG evidence
  TRƯỚC KHI Phase 1.5 Approval Gate mở.
- Blocker/Major finding KHÔNG BAO GIỜ được waive qua residual-risk
  acceptance — con đường DUY NHẤT để thôi chặn gate LÀ RESOLVED (đóng),
  KHÔNG phải "chấp nhận rủi ro." Quy tắc tuyệt đối, KHÔNG ngoại lệ.
- CHỈ finding Minor mới được phép remain open qua Product Owner residual-
  risk acceptance — VÀ CHỈ khi Product Owner tường minh chấp nhận (ghi rõ
  tại decision evidence) — KHÔNG ngầm định.
- Bảy (7) residual Minor ĐÃ accepted non-blocking (§9 dưới) thỏa đúng điều
  kiện này — KHÔNG unresolved theo nghĩa mục này, KHÔNG blocking gate.
```

## 8. Repository-consistency requirements

```text
- Backward Consistency Check (Chapter 12 §12.4, cả hai chiều A và B) chạy
  trên TOÀN BỘ deliverable Phase 1.5 (7 ADR + 8 living convention) đối
  chiếu MỌI authority Locked liên quan (Constitution, Domain Contract,
  Approved architecture packages) — kết quả `No conflict` bắt buộc trước
  gate. **Full-scope Phase 1.5 BCC CHƯA chạy tại boundary authoring DoD
  này** — chỉ per-category forbidden-scope check (git diff untouched
  verification) đã thực hiện trong quá trình mỗi transaction, KHÔNG thay
  thế full-scope Phase-wide BCC này.
- MANIFEST LÀ authoritative source DUY NHẤT cho current version/status/
  state — không state store cạnh tranh (I-12).
```

## 9. Accepted non-blocking residual findings

Bảy (7) finding Minor sau ĐÃ được Product Owner accept LÀM non-blocking residual tại chính category approval transaction tương ứng — resolve trực tiếp từ MANIFEST hiện hành tại boundary authoring DoD này (2026-08-13). Tài liệu này **KHÔNG đóng, KHÔNG rewrite** bất kỳ finding nào dưới đây:

```text
EF-MONO-ADR024-B-MIN-01   monorepo.md — v0.4-era provenance wording
                          inconsistency, KHÔNG semantic/authority impact.
                          OPEN — accepted non-blocking.

ADR026-A-MIN-01           ADR-026 — §4 Alternative 3 hơi overstate Chapter
                          3 §3.2's ví dụ. OPEN — accepted non-blocking.

EF-NAME-A2-MIN-01         naming.md — Python `__init__.py` wording (§4).
                          OPEN — accepted non-blocking.

EF-NAME-B-MIN-01          naming.md — Go file/package wording (§4).
                          OPEN — accepted non-blocking.

ADR027-B-MIN-01           ADR-027 — §4 Alternatives, quan sát VALID Minor,
                          KHÔNG invalidate primary decision. OPEN —
                          accepted non-blocking.

EF-CONFIG-B-MIN-01        config.md — candidate-identity/provenance
                          wording stale "v0.1" tại Non-goals heading VÀ
                          ADR-scope disposition. OPEN — accepted non-
                          blocking.

EF-ERR-B-MIN-01           error-handling.md — candidate/provenance
                          wording stale "v0.1" tại nhiều mục. OPEN —
                          accepted non-blocking.
```

**Xác nhận bắt buộc:** đúng §7 trên, bảy finding này ĐỀU LÀ Minor (KHÔNG Blocker/Major), ĐỀU ĐÃ được Product Owner tường minh accept non-blocking tại chính transaction approval của category tương ứng (KHÔNG ngầm định, KHÔNG suy diễn) — chúng thỏa đúng điều kiện waivable duy nhất mà §7/Chapter 12 §12.4 cho phép. Danh sách này resolve trực tiếp từ MANIFEST hiện hành tại boundary 2026-08-13 — một residual mới phát sinh sau boundary này (nếu có) PHẢI được gate evaluation đối chiếu current MANIFEST state, KHÔNG CHỈ danh sách tại DoD v0.1 này.

## 10. Retrospective boundary (EF-RETRO-001) — KHÔNG một tiêu chí DoD tại đây

```text
`EF-RETRO-001` (`phase-1.5-rules.md`, `operational_state: EFFECTIVE`) TỒN
  TẠI VÀ yêu cầu một Phase 1.5 process retrospective — verify trực tiếp
  wording: "TRƯỚC KHI Phase 2 substantive work bắt đầu, PHẢI thực hiện một
  Phase 1.5 process retrospective..." Rule này gắn CHÍNH XÁC với tiền đề
  Phase 2 substantive work, KHÔNG PHẢI với Phase 1.5 Approval Gate — Gate-
  path controls (`phase-1.5-rules.md`) liệt kê trình tự riêng cho chính
  Phase 1.5 Approval Gate (rules acceptance → Foundation work → DoD accepted
  → Phase-level Gate review → Product Owner Approval Gate decision) mà
  KHÔNG có bước retrospective nào trong đó.
Tiêu chí DoD tại tài liệu này (§1–§9 trên) **KHÔNG bao gồm** `EF-RETRO-001`
  LÀM một mục — retrospective đó VẪN LÀ một điều kiện tách biệt, bổ sung,
  áp dụng cho Phase 2 substantive work, KHÔNG PHẢI cho Phase 1.5 Approval
  Gate. Phase 1.5 Approval Gate CÓ THỂ đạt eligibility mà KHÔNG cần
  retrospective đó hoàn tất — NHƯNG Phase 2 substantive work VẪN bị chặn
  bởi `EF-RETRO-001` (VÀ `P1-RETRO-001`, đã COMPLETE) độc lập với Phase 1.5
  Approval Gate outcome.
Tài liệu này KHÔNG thực hiện retrospective đó tại chính transaction authoring
  này.
```

## 11. Phase-decision bundle requirements (Chapter 14 §14.4.1–§14.4.2)

Tại đúng atomic recording boundary (Chapter 14 §14.4.2), bundle phải pin — **Chapter 14 authority (prepared trực tiếp tại DoD/Roadmap):**

```text
- canonical Phase identity (= "Phase 1.5 — Engineering Foundation")
- exact Roadmap version/content identity đã dùng (Chapter 14 §14.2, hiện
  v1.6, xem MANIFEST cho current version/status)
- exact accepted-DoD identity/content version đã incorporate (tài liệu
  này, khi được accept — current candidate hiện v0.1, CHƯA accepted, CHƯA
  incorporated)
- exact gate-set declaration identity/content resolve từ đó (§2 phía trên)
```

**Reference-only (authority chapter khác, DoD KHÔNG redefine):** Product Owner DoD-acceptance evidence (Chapter 0 §3); required/submitted deliverable evidence (§4 phía trên, Chapter 12 §12.1); applicable Quality Gate result/evidence (Chapter 13 §13.9); Backward Consistency Check result (Chapter 12 §12.4); validator/freshness result (Chapter 11 §11.9); independent review evidence (Chapter 0 §3); Product Owner decision fact.

**KHÔNG thuộc prepared content — chỉ authoritative TẠI atomic recording boundary:** resulting MANIFEST transition identity (Chapter 14 §14.4.1) — tài liệu này KHÔNG đoán trước giá trị đó.

## 12. Explicit non-inclusion

```text
- `Approved`/`Phase 1.5 Approved` (phase decision outcome) KHÔNG phải một
  mục DoD tại đây (Chapter 12 §12.1 cấm tường minh vòng lặp định nghĩa) —
  nó LÀ outcome của Phase 1.5 Approval Gate, xảy ra SAU khi mọi mục §1–§11
  ở trên đã resolve.
- DoD satisfaction (mọi mục §1–§11 resolve) CHỈ establish GATE ELIGIBILITY
  — nó KHÔNG tự động LÀ Phase 1.5 approval. Product Owner LÀ authority DUY
  NHẤT quyết định `Approve`/`Reject`/`Revision Requested` SAU KHI
  eligibility đầy đủ (Chapter 12 §12.2) — DoD này KHÔNG thay thế, KHÔNG
  bind trước quyết định đó.
- DoD criteria DEFINED (tài liệu này tồn tại) ≠ DoD criteria SATISFIED
  (§1–§11 đã đạt) ≠ Quality Gate PASS (§4 evidence pinned) ≠ Approval Gate
  eligibility (Chapter 12 §12.2 toàn bộ tám điểm resolve) ≠ Product Owner
  phase approval (Chapter 12 §12.2 outcome) ≠ Phase 2 authorization (điều
  kiện riêng biệt bổ sung, bao gồm `EF-RETRO-001`, §10 trên) — SÁU trạng
  thái tách biệt, KHÔNG được conflate dưới bất kỳ hình thức nào.
- Tài liệu này KHÔNG tự nó thực hiện: Phase-wide Backward Consistency
  Check (§8, CHỈ định nghĩa yêu cầu, KHÔNG chạy nó); Phase-level Gate
  review (§6); Phase 1.5 approval; `EF-RETRO-001` retrospective (§10);
  Phase 2 mở; deployment/implementation authorization; LIVE authorization.
- Tài liệu này KHÔNG sửa Constitution/Domain Contract/ADR/Approved
  Engineering Foundation artifact nào.
- Tài liệu này KHÔNG tạo ADR nào (kể cả cho Testing — §3.2 đã xác nhận
  `ADR_NOT_REQUIRED` VẪN đúng).
```

## 13. Acceptance status

```text
Product Owner acceptance của DoD này:   CHƯA ghi nhận. `status: Draft`,
                                        `approved_by: null`,
                                        `approved_at: null` — candidate
                                        DoD, CHƯA qua Review A/Independent
                                        Review B, CHƯA Product Owner
                                        acceptance, CHƯA canonical
                                        incorporation (Chapter 14 §14.3.1).

Canonical incorporation (Chapter 14
  §14.3.1) vào Phase-plan của Phase 1.5: CHƯA tồn tại — KHÔNG điều kiện
                                        nào trong bốn điều kiện §14.3.1
                                        thỏa tại transaction authoring này
                                        (KHÔNG Product Owner acceptance
                                        evidence nào resolve được).

Hệ quả:                                Gate-set declaration tại §2 CHƯA
                                        authoritative cho mục đích Chapter
                                        12/13 sử dụng — CHỈ trở thành
                                        authoritative TẠI đúng thời điểm
                                        Product Owner accept VÀ incorporate
                                        tài liệu này (transaction riêng
                                        biệt tương lai, KHÔNG tại đây).
```

**Transaction authoring này CHỈ tạo DoD candidate. Nó KHÔNG:**

```text
tuyên bố Phase 1.5 DoD criteria (§1–§11) đã pass
tuyên bố Phase 1.5 hoàn thành
chạy full-scope Backward Consistency Check (§8)
sinh Quality Gate PASS evidence (§4)
thực hiện Phase-level Gate review (§6)
thực hiện EF-RETRO-001 retrospective (§10)
accept/incorporate chính tài liệu này
approve Phase 1.5
mở Phase 2
authorize deployment/implementation/LIVE
sửa Constitution chapter, ADR, Approved Engineering Foundation artifact,
  Domain Contract, hay Product artifact nào
```

**Việc tiếp theo:** Review A + Independent Review B trên chính DoD candidate này (bounded, đúng Chapter 0 §3/Chapter 11 §11.5), sau đó Product Owner acceptance + canonical incorporation (Chapter 14 §14.3.1) — TRƯỚC KHI Phase-level Gate review (§6) VÀ full-scope Backward Consistency Check (§8) có thể tiến hành cho Phase 1.5 Approval Gate.
