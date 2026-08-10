---
id: contract-compatibility-authority-p14-trigger-e-grant
title: "Evaluator Grant — contract-compatibility-authority — Package 1.4 Trigger E"
grant_version: "1.0"
grant_status: Active
granted_to: contract-compatibility-authority
owner: Product Owner
granted_by: Product Owner
granted_at: "2026-08-10"
revoked: false
revoked_at: null
supersedes: null
superseded_by: null
---

# Evaluator Grant — `contract-compatibility-authority` — Package 1.4 Trigger E

**Vai trò của tài liệu này:** đây LÀ tài liệu Grant/configuration governance ("Deployment/authorization configuration, versioned" — [Chapter 9 §9.6](../../constitution/09-plugin-model.md) Permission boundary phân tầng thẩm quyền, Locked) — KHÔNG PHẢI một ADR, KHÔNG PHẢI một quyết định architecture mới, KHÔNG thay đổi Declaration đã pin tại [ADR-023](../../adr/ADR-023.md) v0.5 §4.1/§5. Tài liệu này resolve CHÍNH XÁC phần Grant mà ADR-023 §9 tường minh để lại chưa resolve, đúng yêu cầu Chapter 10 [§10.4.1](../../constitution/10-compatibility-capability-contract.md).

## 1. Purpose

Cấp (Grant) quyền vận hành cho module đã Declare — `contract-compatibility-authority` (`module_type: compute_engine`, `owns_authoritative_state: true`, đăng ký `docs/architecture/module-registry.yaml` v1.1, `package_lifecycle: Consolidated Stable`) — để thực sự tạo Compatibility Result (Chapter 10 §10.4) cho đúng phạm vi Package 1.4 Trigger E compatibility-evaluation đã Declare tại ADR-023 §5. Đây LÀ Grant-tier work dưới existing Approved authority (ADR-022 v0.3 Approved, ADR-023 v0.5 Approved) — KHÔNG một quyết định architecture mới, KHÔNG tạo ADR-024.

## 2. Grant identity

```text
grant_id:                    contract-compatibility-authority-p14-trigger-e-grant
grant_version:                "1.0"
grant_status:                 Active
content identity:            git blob hash của CHÍNH file này — resolvable/pinned
                              tại docs/MANIFEST.md (I-12 tracking convention, GIỐNG
                              HỆT mọi artifact khác trong repository — KHÔNG khác
                              biệt đặc quyền nào cho tài liệu Grant này; xem §5 dưới
                              cho phân biệt tường minh giữa "MANIFEST tracks identity"
                              VÀ "MANIFEST is the Grant authority" — HAI khái niệm
                              KHÁC NHAU).
granted_to:                   contract-compatibility-authority
granted_by:                   Product Owner
granted_at:                   2026-08-10
```

## 3. Declaration reference (KHÔNG redefine — chỉ tham chiếu, `granted ⊆ declared`)

```text
Declaration authority:  ADR-023 v0.5 (Approved, 2026-08-10, blob
                         623ac8f9d048ad42158e2979e8646bf9bd2c8be7) §4.1/§5.
module_id:               contract-compatibility-authority
module_type:              compute_engine (Type 1, Chapter 7 §7.1)
owns_authoritative_state: true (CHỈ cho phạm vi Compatibility Result nó tạo)
depends_on:                []
Package 1.1 registration: docs/architecture/module-registry.yaml v1.1,
                          package_lifecycle: Consolidated Stable, blob
                          eda6b3e0c8cffba4024b5dc2458ee0f5cf722ef5.
```

## 4. Declared Grant scope (đúng SUBSET của Declaration §5 — KHÔNG mở rộng)

Grant này CHỈ cấp đúng phạm vi ADR-023 §5 đã Declare — KHÔNG một quyền nào rộng hơn:

```text
ĐƯỢC PHÉP (granted):
  - Đánh giá Package 1.4 published SEMANTIC contract surface compatibility,
    đúng backward-only commitment (ADR-022 §3.2), giữa hai version/content
    identity của api-architecture.md.
  - Áp dụng compliance với policy root ĐÃ pin (ADR-022 §4.1: Chapter 10 v2.7
    + Package 1.4 contract-governance artifact), đúng exact-artifact
    eligibility rule (ADR-022 §5.2).
  - Sinh reason classification cho eligibility result (Chapter 10 §10.4.2):
    đã chứng minh tương thích / đã chứng minh không tương thích / không đủ
    evidence / khai báo invalid / reference không resolve được / policy
    mismatch.
  - Issue (tạo) Compatibility Result bất biến (Chapter 10 §10.4) cho đúng
    phạm vi trên — ĐÂY LÀ quyền cốt lõi mà Grant này cấp, KHÔNG tồn tại
    trước Grant này (§9's "Authority tạo Compatibility Result CHỈ tồn tại
    SAU KHI một Grant hợp lệ tồn tại").

KHÔNG ĐƯỢC PHÉP (KHÔNG granted — đúng ADR-023 §5 "Evaluator KHÔNG ĐƯỢC PHÉP
judge"):
  - Field-level schema compatibility.
  - Bất kỳ contract nào khác ngoài Package 1.4 published-contract scope
    (Plugin Contract, Event Contract version, v.v.).
  - Decision/RiskEvaluation/Execution semantic correctness.
  - command-query-api-surface's module identity/taxonomy/dependency graph
    classification.
  - Compatibility-policy identity/version HAY applicability/activation fact
    tự thân — CẢ HAI VẪN thuộc MANIFEST (ADR-022 §5.2, KHÔNG đổi bởi Grant
    này) — evaluator CHỈ áp dụng policy ĐÃ resolve, KHÔNG tự quyết định
    policy nào đang active.
  - Bất kỳ hành động nào khác ngoài "issue Compatibility Result cho đúng
    phạm vi trên."
```

**Subset check:** danh sách "ĐƯỢC PHÉP" trên LÀ chính xác danh sách ADR-023 §5's "Evaluator ĐƯỢC PHÉP judge" (KHÔNG thêm, KHÔNG bớt) cộng đúng MỘT quyền vận hành mới — quyền issue Compatibility Result, vốn ADR-023 §9 tường minh nói "CHỈ tồn tại SAU KHI một Grant hợp lệ tồn tại" (tức là quyền này LÀ chính xác điều Grant tồn tại để cấp, KHÔNG phải một mở rộng scope Declaration). `granted ⊆ declared` — THỎA.

## 5. Canonical Grant-authority designation

**Đây LÀ quyết định trung tâm mà transaction Grant này (theo đúng ADR-023 §9's yêu cầu tường minh) PHẢI thiết lập — ADR-023 KHÔNG tiền chọn cơ chế nào.**

> **Canonical Grant-authority designation cho `contract-compatibility-authority`'s Package 1.4 Trigger E evaluator Grant LÀ CHÍNH tài liệu này** (`docs/governance/grants/contract-compatibility-authority-p14-trigger-e-grant.md`), theo đúng mô hình "Deployment/authorization configuration, versioned" đã khóa tại [Chapter 9 §9.6](../../constitution/09-plugin-model.md) — KHÔNG `MANIFEST.md`, KHÔNG `module-registry.yaml`, KHÔNG một cơ chế runtime/service mới nào.

**Lý do lựa chọn (đúng nguyên tắc "minimum existing governance/configuration mechanism", KHÔNG invent runtime service mới — cùng precedent ADR-022 §5.1 mục 1 đã loại trừ):**

```text
1. MANIFEST.md BỊ LOẠI TRỪ tường minh cho vai trò Grant-authority — đây CHÍNH
   XÁC LÀ root cause `ADR023-B-MAJ-01` (đóng tại ADR-023 v0.5 §9): MANIFEST
   §5.2 (ADR-022) CHỈ designate compatibility-POLICY identity/version +
   applicability/activation (Phase 1 architecture-only scope) — KHÔNG bao
   giờ designate evaluator-GRANT authority. Dùng MANIFEST LÀM Grant authority
   sẽ tái lặp CHÍNH XÁC lỗi conflation đã đóng — KHÔNG chấp nhận được.
2. module-registry.yaml BỊ LOẠI TRỪ — đây LÀ module identity/taxonomy/
   dependency authority (Chapter 7 §7.5), KHÔNG PHẢI authorization-
   configuration authority; dùng nó LÀM Grant authority sẽ conflate identity
   (Declaration) với quyền vận hành (Grant) — chính xác phân biệt
   `module identity ≠ evaluator grant` mà ADR-023 §9 khóa tường minh.
3. Một runtime "Grant Registry/Authorization Service" MỚI BỊ LOẠI TRỪ — Phase
   1 KHÔNG có executable implementation (Trigger B/C deferred), một runtime
   service tại giai đoạn này LÀ premature VÀ tạo một architecture
   responsibility KHÔNG cần thiết CHỈ để lưu một Grant fact (đúng nguyên tắc
   ADR-022 §5.1 mục 1 đã loại trừ cho policy authority — áp dụng TƯƠNG TỰ
   cho Grant authority).
4. Một tài liệu governance/configuration versioned RIÊNG BIỆT (chính tài liệu
   này) LÀ cơ chế TỐI THIỂU sẵn có, phù hợp CHÍNH XÁC với định nghĩa "Grant"
   tại Chapter 9 §9.6 ("Deployment/authorization configuration, versioned"):
   nó KHÔNG phải một module/architecture responsibility mới (KHÔNG entry nào
   thêm vào module-registry.yaml), nó có content identity bất biến qua git
   blob hash (đúng "immutable version/content identity" §10.4.1 yêu cầu), nó
   có thể được revoke/supersede qua một Grant version MỚI (§11 dưới) mà
   KHÔNG cần một ADR mới (Grant KHÔNG phải architecture decision, ADR-023 §9
   tường minh xác nhận), VÀ nó tự thân LÀ authoritative record — KHÔNG cần
   một nguồn thứ hai xác nhận nó, đúng cardinality "đúng MỘT canonical
   authority" (Chapter 10 §10.4.3 mục 4, áp dụng tương tự cho grant
   authority per §10.4.1).
```

**Phân biệt tường minh (tránh nhầm lẫn với `ADR023-B-MAJ-01`):** `docs/MANIFEST.md` VẪN sẽ ghi một dòng cho tài liệu Grant này — NHƯNG đó CHỈ LÀ identity/version/blob tracking convention I-12 ĐÃ áp dụng cho MỌI artifact trong repository (ADR, Constitution chapter, Domain Contract, v.v.), KHÔNG PHẢI MANIFEST trở thành nguồn xác nhận NỘI DUNG hay TÍNH HIỆU LỰC của Grant. Nội dung VÀ tính hiệu lực (active/revoked) của Grant được xác nhận DUY NHẤT bởi chính tài liệu Grant này — CHÍNH XÁC cùng nguyên tắc "MANIFEST ghi nhận ADR Approved, NHƯNG chính ADR document + Product Owner decision bên trong nó LÀ authority, KHÔNG PHẢI MANIFEST tự tạo ra fact Approved đó."

## 6. Authoritative Grant activation/applicability fact / frontier

```text
Activation fact:   Grant này ACTIVE kể từ granted_at (2026-08-10), resolvable
                   TRỰC TIẾP tại field `grant_status: Active` trong frontmatter
                   của CHÍNH tài liệu này — KHÔNG nguồn nào khác được phép tự
                   tạo một competing activation fact cho scope Grant này (đúng
                   cardinality Chapter 10 §10.4.3 mục 4, áp dụng cho grant
                   authority per §10.4.1).
Frontier:          Grant áp dụng cho MỌI Compatibility Result evaluation được
                   thực hiện TẠI HOẶC SAU 2026-08-10, trong đúng phạm vi §4
                   trên, CHO TỚI KHI (a) `revoked: true`/`revoked_at` được
                   set bởi một Grant-revocation transaction governed RIÊNG
                   BIỆT, HOẶC (b) một Grant version kế tiếp supersede tài
                   liệu này (§11 dưới) — KHÔNG frontier nào khác được suy
                   diễn.
Resolution rule:   Evaluation boundary tại thời điểm bất kỳ CHỈ cần đọc field
                   `grant_status`/`revoked` của phiên bản Grant document hiện
                   hành (git-tracked, content-addressable) — KHÔNG cần một
                   event log/runtime activation source nào khác tại Phase 1
                   architecture-only scope (cùng mô hình applicability đã
                   dùng cho compatibility-policy authority, ADR-022 §5.2,
                   NHƯNG LÀ một instance riêng biệt, KHÔNG chung nguồn).
```

## 7. Coverage / unrevoked evidence

```text
revoked:                       false
revoked_at:                     null
Coverage — policy version:      Chapter 10 v2.7 (Locked, blob
                                016e46bcad0826e983a51ee24c8ec4c3217aeba1) +
                                api-architecture.md v0.8 (Consolidated
                                Stable, blob
                                b79493e44daf5154333068454d565cb8053ed7dd) —
                                CẢ HAI hiện ĐANG active theo ADR-022 §5.2
                                (MANIFEST-resolvable, KHÔNG đổi bởi Grant
                                này).
Coverage — subject scope:      Package 1.4 published-contract artifact
                                (api-architecture.md), semantic-level CHỈ,
                                backward-only (ADR-022 §3.2).
Coverage — right to issue:      Compatibility Result issuance (Chapter 10
                                §10.4) — cấp tại §4 trên, KHÔNG tồn tại
                                trước Grant này.
Coverage — boundary:            Phase 1 architecture-only (KHÔNG runtime
                                activation event nào tồn tại) — Enforcement/
                                Verification VẪN deferred tới implementation
                                stage (ADR-023 §9, KHÔNG đổi).
```

## 8. What this Grant does NOT do

```text
KHÔNG tạo Compatibility Result nào tại transaction này — chỉ cấp QUYỀN, việc
  issue Compatibility Result THỰC SỰ LÀ một transaction governed riêng biệt,
  tương lai, SAU Grant này.
KHÔNG tạo architecture responsibility mới, KHÔNG thêm/sửa module nào trong
  module-registry.yaml/system-decomposition.md (byte-identical, git diff
  empty).
KHÔNG tạo ADR-024, KHÔNG reopen ADR-022/ADR-023.
KHÔNG rerun Phase 1 Quality Gate, KHÔNG đổi QG-P14-E-EVID-01/G2-RDY-BLK-03
  (VẪN OPEN), KHÔNG mở Gate 2, KHÔNG authorize Phase 2.
KHÔNG thay đổi compatibility-policy identity/version/applicability authority
  (VẪN MANIFEST, ADR-022 §5.2, KHÔNG chạm).
KHÔNG author Enforcement (runtime authority)/Verification (I-7 checks) —
  deferred tới implementation stage, đúng ADR-023 §9.
```

## 9. Relationship / citations

`docs/adr/ADR-023.md` v0.5 (Approved) — Declaration-tier authority, module identity/taxonomy/responsibility, KHÔNG redefine, Grant này CHỈ resolve phần Grant mà ADR-023 §9 tường minh để lại. `docs/adr/ADR-022.md` v0.3 (Approved) — compatibility commitment/policy root/MANIFEST compatibility-**policy** authority, KHÔNG redefine, KHÔNG conflate với Grant authority tại đây (đúng correction ADR-023 v0.5 §9 đã đóng `ADR023-B-MAJ-01`). `docs/constitution/09-plugin-model.md` §9.6 (Locked) — Permission boundary phân tầng thẩm quyền, nguồn của mô hình "Grant = deployment/authorization configuration, versioned" mà tài liệu này thực thi. `docs/constitution/10-compatibility-capability-contract.md` §10.4.1 (Locked) — evaluation provenance requirement, mọi field bắt buộc pin tại §2–§7 trên trực tiếp thỏa mãn checklist này cho Compatibility Result tương lai sẽ trích dẫn Grant này.

## 10. Revocation and supersession procedure

```text
Revocation:   một Grant-revocation transaction governed RIÊNG BIỆT, Product
              Owner decision tường minh, set `revoked: true`/`revoked_at:
              <date>` trong CHÍNH tài liệu này (KHÔNG file khác) — kể từ đó,
              MỌI Compatibility Result evaluation SAU revoked_at PHẢI fail
              closed (I-6) cho scope này.
Supersession: một Grant version kế tiếp (`grant_version: "2.0"` hoặc tương
              đương, file MỚI hoặc bounded correction trên chính file này
              theo đúng convention bounded-correction đã dùng cho ADR/Package
              1.1 trong repository) — set `supersedes`/`superseded_by` tường
              minh, KHÔNG mutate content dưới cùng grant_version identity
              (đúng Chapter 10 §10.4.3 mục 5's lifecycle-transition-
              authoritative rule, áp dụng tương tự cho Grant).
Historical
  Compatibility Result: revocation/supersession SAU một evaluation KHÔNG sửa
              lịch sử result đã tạo trước đó (đúng Chapter 10 §10.4.4/§10.4.1
              "revoke sau đó không sửa result lịch sử").
```

## 11. Validation and acceptance criteria

```text
1. Grant identity/version/content-identity pinned — CONFIRMED (§2).
2. Granted module = Declaration module, ZERO drift — CONFIRMED (§3).
3. Declared scope ⊆ Declaration scope (ADR-023 §5) — CONFIRMED (§4).
4. Canonical Grant-authority designation explicit, KHÔNG MANIFEST, KHÔNG
   module-registry.yaml, KHÔNG runtime service mới — CONFIRMED (§5).
5. Activation/applicability fact + frontier resolvable trực tiếp tại tài
   liệu này — CONFIRMED (§6).
6. Unrevoked evidence + đầy đủ bốn coverage dimension (policy version ×
   subject scope × right to issue × boundary) — CONFIRMED (§7).
7. KHÔNG architecture responsibility/module mới tạo — CONFIRMED (§8).
8. KHÔNG Compatibility Result tạo tại transaction này — CONFIRMED (§8).
9. QG-P14-E-EVID-01/G2-RDY-BLK-03 KHÔNG đổi (VẪN OPEN/CLOSED) — CONFIRMED
   (§8).
```

## 12. Change history

```text
v1.0  2026-08-10  Established — vai trò: `Package 1.4 Trigger E Evaluator
      Grant Executor`. Grant/configuration work dưới existing Approved
      authority (ADR-022 v0.3, ADR-023 v0.5) — KHÔNG một quyết định
      architecture mới, KHÔNG ADR-024. Cấp quyền `contract-compatibility-
      authority` issue Compatibility Result cho đúng Package 1.4 Trigger E
      scope đã Declare (ADR-023 §5). Canonical Grant-authority designation:
      chính tài liệu này — KHÔNG MANIFEST (đóng đúng cách hiểu SAI đã dẫn
      tới `ADR023-B-MAJ-01`), KHÔNG module-registry.yaml, KHÔNG runtime
      service mới. `granted_by: Product Owner`, `granted_at: 2026-08-10`,
      `revoked: false`. Compatibility Result CHƯA tạo — transaction governed
      riêng biệt tương lai. `QG-P14-E-EVID-01`/`G2-RDY-BLK-03` VẪN OPEN,
      Phase 1 Quality Gate VẪN FAIL — evidence, Gate 2 VẪN CLOSED.
```
