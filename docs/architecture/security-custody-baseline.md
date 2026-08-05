---
id: security-custody-baseline
title: "Package 1.2 — Security & Custody Baseline"
version: "0.4"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-04"
last_review: null
next_review: null
depends_on: ["00-governance", "02-platform-invariants", "06-identity-model", "07-module-taxonomy", "08-event-model", "09-plugin-model", "13-quality-gates", "14-roadmap"]
---

# Package 1.2 — Security & Custody Baseline

**CANDIDATE — status: Draft, KHÔNG Consolidated Stable, KHÔNG Approved.** Package 1.2 v0.3 — substantive extension candidate, author dựa trên Package 1.1 `Consolidated Stable` (v0.6, 25 module, xem §1) VÀ [ADR-017](../adr/ADR-017.md) v0.2 (`Approved`, 2026-08-04T20:08:00+07:00, Product Owner — Option C: Custody/Signing Service + Exchange Adapter split). Đây LÀ một authoring transaction, KHÔNG PHẢI một consolidation transaction.

**ADR gate (§15) NAY RESOLVED — KHÔNG còn ACTIVE/pending.** v0.2's §15 ghi nhận một ADR decision requirement ACTIVE chặn Consolidated Stable; ADR-017 v0.2 Approved đã resolve đủ tám mục decision scope đó (§15.2 cũ) — xem §15 (viết lại) cho xác nhận đầy đủ. Việc ADR gate resolved KHÔNG tự động làm Package 1.2 `Consolidated Stable` — v0.3 CẦN Review A + Independent Review B MỚI trên chính candidate này, VÀ một Package 1.1 alignment transaction riêng biệt (§16a) trước khi Product Owner consolidation decision có thể xảy ra.

**Phạm vi v0.3 — mở rộng, KHÔNG chỉ correction:** thêm elaboration kiến trúc đầy đủ cho `custody-signing-service` (module ADR-017 đã chọn, đã đăng ký tại Package 1.1 v0.5/v0.6 NHƯNG `phase.elaborated_by: null` — v0.3 LÀ candidate elaboration đó, KHÔNG PHẢI xác nhận một assignment đã tồn tại). `exchange-adapter` VẪN functionally unelaborated tại transaction này — registered nhưng KHÔNG có home package (§7/§14). Chưa qua Review A/Independent Review B cho v0.3, chưa có Product Owner consolidation decision, chưa có Package 1.1 alignment transaction.

**v0.4 — bounded correction (2026-08-05), đóng bốn Review A finding trên v0.3 (`P12V03-A-BLK-01`/`P12V03-A-MAJ-01`/`P12V03-A-MIN-01`/`P12V03-A-MIN-02`), KHÔNG substantive extension mới:** (a) `P12V03-A-BLK-01` — loại bỏ mọi statement/exception (co-location, chia sẻ process/host, network zone, deployment topology) cho phép Execution Engine raw-secret access — custody-signing-service LÀ module DUY NHẤT được phép dùng exchange credential trực tiếp dưới ADR-017 Option C, KHÔNG ngoại lệ (§3.2, §6); (b) `P12V03-A-MAJ-01` — loại bỏ terminal-outcome claim sai ("PHẢI fail closed, KHÔNG hoàn tất SIGNED") cho một SigningAttempt in-flight bị credential revocation/execution suspension ảnh hưởng — hành vi đó VẪN UNRESOLVED pending một ADR Approved riêng, chỉ rule chặn SigningRequest/SigningAttempt MỚI được giữ (§4a.9); (c) `P12V03-A-MIN-01` — sửa tham chiếu §4a nội bộ sai lệch (§4a.2, §4a.3), KHÔNG renumber tài liệu; (d) `P12V03-A-MIN-02` — phân biệt tường minh `forbidden_dependencies` (chiều custody-signing-service → module khác) khỏi caller-authorization boundary (chiều module khác → custody-signing-service) tại §4a.7, KHÔNG dùng cái này làm bằng chứng cho cái kia. Mọi nội dung khác của v0.3 GIỮ NGUYÊN.

## 0. Vai trò của tài liệu này — scope resolved từ controlling source (bắt buộc, yêu cầu task)

**Xác nhận tường minh (yêu cầu task — "Do not infer scope from Package 1.3-D wording alone"):** Package 1.3-D's text tham chiếu "Package 1.2 baseline (custody-adjacent boundary, I-11)" một cách MÔ TẢ, KHÔNG phải định nghĩa authoritative. Scope THỰC SỰ của Package 1.2 được resolve TRỰC TIẾP từ `phase-1-plan.md` (Approved, controlling), nguyên văn:

```text
Package ID:   1.2
Name:         Security & Custody Baseline
Purpose:      Xác lập baseline evidence set cho I-4 (Strategy Isolation), I-7 (Plugin
              Non-Bypass), I-11 (Secrets & Custody) — áp dụng NGANG qua mọi package
              Phase 1 khác, KHÔNG PHẢI một deliverable tuần tự độc lập.
Outputs:      docs/architecture/security-custody-baseline.md — trust boundary map,
              isolation requirement per module class, checklist mà mọi package khác
              PHẢI thỏa trước khi tự Consolidated Stable.
Explicit      KHÔNG design authentication implementation cụ thể; KHÔNG design custody
non-goals:    implementation cụ thể (key management, HSM, v.v.); KHÔNG chọn security
              vendor/tool.
Dependencies: 1.1 (cần baseline module list để map trust boundary theo module) — CHỈ
              cần baseline, KHÔNG cần 1.1 Consolidated Stable đầy đủ.
ADR           Likely tạo ADR riêng cho security trust boundary + custody boundary —
dependencies: package 1.2 PHẢI dừng tại đúng boundary đó chờ ADR Approved trước khi tự
              Consolidated Stable cho phần liên quan.
```

**Đây là MỘT artifact duy nhất** (`docs/architecture/security-custody-baseline.md`) — `phase-1-plan.md`'s "Expected artifact paths" liệt kê CHỈ một file, KHÔNG nhiều bounded artifact, KHÔNG cấu trúc `docs/architecture/engine/` (khác Package 1.3-A/B/C/D — Package 1.2 là cross-cutting baseline, KHÔNG một engine pipeline stage).

**Module inventory resolved (script-verified, module-registry.yaml v0.6, 25 module — cập nhật v0.3, đóng stale 23-module/v0.4 reference):** ĐÚNG MỘT module CÓ registry `phase.elaborated_by: "1.2"` HIỆN TẠI — `account-service`. `custody-signing-service` (đăng ký Package 1.1 v0.5, ADR-017 v0.2 Approved) mang `phase.elaborated_by: null` — KHÔNG được registry assign cho Package 1.2 (hay bất kỳ package nào) tại thời điểm này; v0.3 đề xuất Package 1.2 làm elaborating package tự nhiên (§4a), NHƯNG registry assignment đó CHƯA xảy ra — CHỈ xảy ra qua một Package 1.1 alignment transaction riêng biệt SAU KHI v0.3 pass Review A/B (§16a). Package 1.2 v0.3 do đó có BA trách nhiệm tách biệt: (a) elaborate kiến trúc kỹ thuật của `account-service` (module DUY NHẤT registry ĐÃ assign, KHÔNG đổi từ v0.2); (b) đề xuất elaboration đầy đủ cho `custody-signing-service` (module ADR-017 đã chọn, CHƯA registry-assigned — §4a); (c) thiết lập trust boundary map/isolation checklist CHO các module class khác (`trust_boundary_candidate` — nay 5 module bao gồm `exchange-adapter`, `secret_consuming` — `custody-signing-service` tự nó) MÀ KHÔNG re-elaborate chức năng CỦA module ngoài phạm vi (a)/(b) — các module đó (`market-data-ingestion`→1.3-A, `risk-gateway`/`execution-engine`→1.3-D, `command-query-api-surface`→1.4, `exchange-adapter`→KHÔNG package nào, §14) đã/đang được elaborate CHỨC NĂNG bởi package riêng của chúng (hoặc CHƯA có package nào, trường hợp `exchange-adapter`); Package 1.2 CHỈ thêm layer bảo mật/isolation YÊU CẦU áp dụng lên các module đó — KHÔNG redefine responsibility/dependency đã pin.

**KHÔNG thuộc phạm vi tài liệu này:** authentication implementation cụ thể; custody implementation cụ thể (key management, HSM); security vendor/tool selection; field-level event schema (đã khóa tại `account.md`, Package 0.2-C2, `Consolidated Stable`); Package 1.1/1.3-A/1.3-B/1.3-C/1.3-D content (KHÔNG redefine, `Consolidated Stable`).

## 1. Governing authority

```text
Constitution (Chapter 0–14, Locked):              highest architectural authority, đặc
                                                    biệt I-4 (Strategy Isolation), I-6
                                                    (Fail-Safe by Scope), I-7 (Plugin
                                                    Non-Bypass), I-8 (Kill Switch), I-11
                                                    (Secrets & Custody Isolation)
Chapter 9 (Plugin Model, Locked):                  §9.6 Permission boundary (Declaration/
                                                    Grant/Enforcement/Verification bốn
                                                    tầng) — áp dụng cho mọi module, đặc
                                                    biệt plugin-hosting
Approved ADR-007 (Vision scope):                  internal/single-team, crypto-only
                                                    Phase 0-3 — Account first-class từ
                                                    đầu, KHÔNG multi-tenant/RBAC ngay
Approved ADR-012 (Account-to-Boundary               exactly-one-boundary Account,
  Cardinality):                                    canonical Account Boundary model,
                                                    §6 tường minh trỏ "Phase 1 Security &
                                                    Custody Baseline" cho credential
                                                    reference mechanism cụ thể
Approved ADR-017 (Custody & Signing Trust           Option C selected — split
  Boundary, v0.2, 2026-08-04T20:08:00+07:00):       Custody/Signing Service +
                                                    Exchange Adapter; resolves đủ tám mục
                                                    decision scope mà §15 (v0.2) ghi nhận
                                                    ACTIVE (mới, v0.3) — xem §15 viết lại
account.md v0.2 (Package 0.2-C2, Consolidated     controlling domain semantic authority
  Stable):                                          cho Account entity — Consolidated
                                                    Stable, KHÔNG redefine tại đây
module-registry.yaml v0.6 (Consolidated Stable,   module identity/taxonomy/dependency
  25 module, cập nhật v0.3):                       authority — KHÔNG redefine tại đây;
                                                    `custody-signing-service`/
                                                    `exchange-adapter` ĐÃ đăng ký,
                                                    `phase.elaborated_by: null` cho cả hai
system-decomposition.md v0.6 (Consolidated        semantic parity với module-registry.yaml
  Stable, cập nhật v0.3):                          v0.6 — KHÔNG redefine tại đây
risk-execution-architecture.md v0.2 (Package      Package 1.3-D consumer của Package 1.2
  1.3-D, review-clean, consolidation blocked      baseline — consumed như một forward
  pending Package 1.2):                            reference, KHÔNG redefine
phase-1-plan.md v0.4 (Approved):                  Phase 1 work-breakdown/package-boundary
                                                    authority, nguồn CHÍNH của §0 scope
                                                    resolution
Package 1.2 (tài liệu này):                       technical elaboration authority ONLY,
                                                    cho account-service, custody-signing-
                                                    service (đề xuất, §4a), VÀ cross-cutting
                                                    trust boundary map/checklist
```

Package 1.2 KHÔNG redefine domain entity/event semantics, module identity/taxonomy, hay bất kỳ package đã Consolidated Stable nào — mọi nội dung dưới đây chỉ **elaborate** kiến trúc kỹ thuật trong ranh giới đã pin.

## 2. Module scope (v0.3 — hai module elaborate đầy đủ, năm module tham chiếu trust-boundary-only)

| module_id | module_type | owns_authoritative_state | depends_on | forbidden_dependencies | consumes | emits | security_classification | phase.elaborated_by |
|---|---|---|---|---|---|---|---|---|
| `account-service` | runtime_service | true | (none, root) | (none) | `command` | `event`, `query` | `custody_adjacent` | **`1.2`** |
| `custody-signing-service` | runtime_service | true (scoped, §4a.2) | `account-service` | 10 module (§4a.1) | `command`, `query` | `event`, `query` | `secret_consuming` | `null` (registry) — **`1.2` đề xuất, xem §4a/§16a** |
| `market-data-ingestion` | runtime_service | true | `market-reference-service` | (none) | `query` | `event` | `trust_boundary_candidate` | `1.3-A` (tham chiếu §3 CHỈ) |
| `risk-gateway` | runtime_service | true | `decision-authority-service`, `account-service` | (none) | `event` | `event` | `trust_boundary_candidate` | `1.3-D` (tham chiếu §3 CHỈ) |
| `execution-engine` | runtime_service | true | `risk-gateway`, `paper-execution-boundary` | `strategy-engine`, `strategy-plugin-host`, `context-aggregator` | `event` | `event`, `command` | `trust_boundary_candidate` | `1.3-D` (tham chiếu §3 CHỈ) |
| `exchange-adapter` | runtime_service | true (scoped, ADR-017 §3.2a) | `custody-signing-service` | 9 module (ADR-017 §3.2) | `command` | `event` | `trust_boundary_candidate` | `null` (registry) — KHÔNG package nào, §14 gap |
| `command-query-api-surface` | runtime_service | false | (16 module, xem §2 note) | (none) | `event`, `query`, `command` | `query`, `command` | `trust_boundary_candidate` | `1.4` (tham chiếu §3 CHỈ) |

**Module registration cập nhật (v0.3 — thay thế nội dung v0.1/v0.2, ĐÃ stale sau ADR-017/Package 1.1 v0.5/v0.6):** `custody-signing-service` và `exchange-adapter` NAY registered tại `module-registry.yaml` v0.6 (Package 1.1, Consolidated Stable) — đăng ký theo Approved [ADR-017](../adr/ADR-017.md) v0.2 (Option C). Package 1.2 KHÔNG tự đăng ký hai module này (đã được Package 1.1 correction transaction thực hiện riêng biệt, ngoài phạm vi Package 1.2) — v0.3 CHỈ elaborate kiến trúc chi tiết của `custody-signing-service` (§4a) như một candidate PROPOSAL cho registry alignment tương lai (§16a), VÀ tham chiếu `exchange-adapter` như trust-boundary-only (functionally unelaborated, KHÔNG package nào sở hữu, §14 gap).

**18 module còn lại (`security_classification: none`, KHÔNG đổi từ v0.2 ngoài đếm lại tổng — đóng `P12-A-MAJ-02`/`P12-IRB-MAJ-02`, lịch sử):** `none` nghĩa CHỈ là Package 1.1 KHÔNG gán classification đặc biệt nào cho module đó — KHÔNG PHẢI một affirmative security clearance, KHÔNG PHẢI bằng chứng "không có external interaction/không có sensitive evidence/không liên quan credential/không có nghĩa vụ bảo mật riêng/loại trừ vĩnh viễn khỏi trust-boundary review". 18 module này (25 - 1 `custody_adjacent` - 1 `secret_consuming` - 5 `trust_boundary_candidate`) VẪN nằm ngoài phạm vi elaborate chức năng chi tiết VÀ ngoài phạm vi trust-boundary-map riêng của §3's bốn lớp có tên (`trust_boundary_candidate`/`custody_adjacent`/`secret_consuming`), NHƯNG KHÔNG được miễn trừ khỏi class-neutral minimum security baseline (§3.1) — mọi module trong 25-module inventory, không phân biệt classification, đều chịu baseline đó. Chi tiết đầy đủ: §3.0/§3.1.

## 3. Trust boundary map — theo module class (bắt buộc, yêu cầu task, KHÔNG re-elaborate chức năng module khác)

**Nguyên tắc bắt buộc:** mục này định nghĩa YÊU CẦU security/isolation ÁP DỤNG LÊN mỗi `security_classification`, KHÔNG redefine responsibility/dependency/authority đã pin tại Package 1.1/1.3-A/1.3-D/1.4. Package sở hữu chức năng của từng module (1.3-A/1.3-D/1.4) VẪN là authority cho chính module đó — Package 1.2 CHỈ thêm layer bảo mật.

### 3.0 Corrected semantics của `security_classification: none` (bounded correction, đóng `P12-A-MAJ-02`/`P12-IRB-MAJ-02`)

**Finding đóng:** v0.1 của §3 diễn giải SAI `security_classification: none` như một affirmative proof rằng 19 module đó "KHÔNG chạm external network boundary trực tiếp, KHÔNG sở hữu credential/secret material" — đây là silent invention, KHÔNG phải điều `module-registry.yaml` (Package 1.1, Consolidated Stable) thực sự tuyên bố.

```text
security_classification: none nghĩa CHỈ LÀ: Package 1.1 KHÔNG gán một classification
đặc biệt nào (trust_boundary_candidate/custody_adjacent) cho module đó tại thời điểm
đăng ký.

KHÔNG PHẢI một affirmative security clearance.

KHÔNG chứng minh: module đó không có external interaction; module đó không liên quan
sensitive evidence; module đó không liên quan credential; module đó không có nghĩa vụ
bảo mật riêng; module đó được loại trừ vĩnh viễn khỏi trust-boundary review.
```

### 3.1 Class-neutral minimum security baseline (áp dụng cho MỌI 25 module đã đăng ký, không phân biệt classification — v0.2 gốc, cập nhật số liệu v0.3)

18 module `security_classification: none` VẪN nằm ngoài phạm vi elaborate chức năng chi tiết của Package 1.2 (không author lại architecture riêng cho từng module đó — đó là thẩm quyền package sở hữu chức năng của chúng), NHƯNG KHÔNG được miễn trừ khỏi baseline sau — baseline này áp dụng ĐỒNG NHẤT cho cả 25 module, kể cả `account-service`, `custody-signing-service`, và năm module `trust_boundary_candidate`:

```text
1. Published-contract-only interaction — module chỉ tương tác qua contract category đã
   đăng ký (event/query/command, module-registry.yaml), KHÔNG qua kênh ngầm/side-channel.

2. Không raw-secret hay private-key exposure — không module nào (bất kể classification)
   được lộ raw exchange credential/private key trong payload, log, snapshot, hay replay
   artifact, trừ phạm vi đã pin riêng cho custody_adjacent/future credential-using
   boundary (§3.2).

3. Least-privilege service và data access — module chỉ truy cập đúng dữ liệu/service cần
   cho trách nhiệm đã đăng ký của nó (Chapter 7 §7.3), không quyền truy cập rộng hơn.

4. Authorization validation cho command và privileged operation — mọi command/thao tác
   có tác động (đặc biệt command mutating authoritative state) PHẢI qua authorization
   validation, KHÔNG tự động chấp nhận vì đến từ nội bộ hệ thống.

5. Không suy authority từ transport, routing, hay việc sở hữu signed material — cùng
   nguyên tắc đã pin tại §5 (transport KHÔNG BAO GIỜ tự thân là authority), áp dụng
   chung cho MỌI module, không riêng execution path.

6. Không ambient mutable-state access ngoài contract đã khai báo — module KHÔNG được
   đọc/ghi authoritative state của module khác ngoài qua published contract.

7. Auditability cho hành động privileged/security-relevant — hành động có ý nghĩa bảo
   mật (đặc biệt của bốn module trust_boundary_candidate và account-service) PHẢI truy
   vết được (I-1 Explainability nguyên tắc chung, §12).

8. Fail-closed khi authority/permission/identity/security evidence absent, stale,
   invalid, unknown, hoặc mismatched — cùng nguyên tắc I-6 đã pin tại §10, áp dụng cho
   MỌI module, không riêng custody/boundary state.

9. Mandatory reassessment và khả năng reclassification khi connectivity, privilege,
   external exposure, hoặc secret-derived evidence handling của module thay đổi — một
   module `none` hôm nay KHÔNG tự động vẫn `none` mãi mãi nếu trách nhiệm/kết nối của nó
   thay đổi; reclassification là quyết định Package 1.1 (registry authority, KHÔNG phải
   Package 1.2 — Package 1.2 KHÔNG tự reclassify module nào tại transaction này).
```

**Xác nhận tường minh:** baseline chín mục trên là YÊU CẦU architecture-level (WHAT phải đúng), KHÔNG author cơ chế/implementation cụ thể nào (forbidden scope §13 không đổi) — KHÔNG mở lại/redefine `module-registry.yaml`, KHÔNG reclassify module nào tại transaction này.

### 3.2 Class-specific additions (trên NỀN baseline §3.1 — KHÔNG thay thế)

```text
Class: trust_boundary_candidate (5 module — v0.3 thêm exchange-adapter: market-data-
  ingestion, risk-gateway, execution-engine, exchange-adapter, command-query-api-surface)
  Baseline:  §3.1 (bắt buộc, không miễn trừ).
  Bổ sung:   module CÓ TIỀM NĂNG chạm external network boundary (venue connection,
    custody-adjacent execution surface, hoặc API ingress/egress) — nhận thêm boundary
    và ingress/egress scrutiny NGOÀI baseline chung — IDENTIFICATION ONLY tại package
    sở hữu chức năng (§2 note) cho bốn module gốc; `exchange-adapter` (v0.3, ADR-017
    §3.2) CŨNG identification-only tại Package 1.2 — KHÔNG functional elaboration
    (thẩm quyền một package TƯƠNG LAI chưa xác định, §14 gap).
  Yêu cầu I-4/I-7 áp dụng:  I-4 Scope liệt kê tường minh "Strategy Engine, Decision
    Engine, Risk Gateway, Execution Engine" — mọi trade intent PHẢI qua Risk Gateway
    trước khi tới Execution Engine (ĐÃ script-verified tại Package 1.3-C/1.3-D, KHÔNG
    redefine tại đây). I-7 Scope "Mọi Plugin" — command-query-api-surface là routing/
    exposure layer (Package 1.1 notes: "KHÔNG business logic riêng"), PHẢI verify theo
    I-7 Verification bốn mục bổ sung cho hệ polyglot/distributed: network ACL check ·
    API authorization scope check · event schema compatibility check · command
    authorization check.
  Yêu cầu I-11 áp dụng:  market-data-ingestion (external venue connection), execution-
    engine (execution surface tương tác Paper Execution Boundary hiện tại — PAPER path
    KHÔNG đổi; future LIVE venue-submission boundary via exchange-adapter, ADR-017 §8.1,
    KHÔNG active edge), VÀ exchange-adapter (venue-facing transport, KHÔNG raw-secret
    access dưới Option C, ADR-017 §3.2) — KHÔNG module nào trong nhóm này được cấp
    quyền đọc raw secret dưới BẤT KỲ hình thức nào — co-location, chia sẻ process, chia
    sẻ host, cùng network zone, hay bất kỳ deployment topology nào ĐỀU KHÔNG chuyển giao
    credential-use authority (ADR-017 Option C, §4a.2/§4a.3): custody-signing-service LÀ
    module DUY NHẤT được phép dùng exchange credential trực tiếp; execution-engine
    KHÔNG BAO GIỜ được cấp ngoại lệ đó dưới kiến trúc ĐÃ Approved này.
  Design status:  IDENTIFICATION ONLY — Package 1.2 KHÔNG design concrete auth
    mechanism/network ACL implementation cho năm module này (forbidden scope).

Class: custody_adjacent (1 module: account-service)
  Baseline:  §3.1 (bắt buộc, không miễn trừ).
  Bổ sung:   module sở hữu identity/metadata GẦN custody nhưng KHÔNG sở hữu raw secret
    (account-service responsibilities, nguyên văn: "KHÔNG sở hữu credential/secret
    material (I-11)") — CHỈ opaque credential reference, KHÔNG raw-secret ownership.
  Yêu cầu I-11 áp dụng:  đầy đủ tại §6 dưới — account-service CHỈ giữ
    `credential_reference` (opaque), KHÔNG BAO GIỜ raw secret.
  Design status:  §4 dưới elaborate ĐẦY ĐỦ kiến trúc (module DUY NHẤT registry-assigned
    cho Package 1.2) — bao gồm identification, KHÔNG bao gồm credential storage
    implementation.

Class: secret_consuming (1 module — MỚI v0.3, thay thế placeholder "future credential-
  using boundary" của v0.1/v0.2: custody-signing-service)
  Baseline:  §3.1 (bắt buộc, không miễn trừ).
  Bổ sung:   module DUY NHẤT trong toàn platform được phép sử dụng exchange credential
    trực tiếp (I-11, ADR-017 §3.1) — direct-secret authority ĐÃ được cấp qua Approved
    ADR-017 v0.2 VÀ registry-level established tại `module-registry.yaml` v0.5/v0.6
    (Package 1.1) — KHÔNG còn là "future"/hypothetical (khác v0.1/v0.2). §4a dưới
    elaborate ĐẦY ĐỦ kiến trúc (candidate proposal cho Package 1.2, registry
    `phase.elaborated_by` VẪN `null` cho tới alignment transaction, §16a).
  Yêu cầu I-11 áp dụng:  đầy đủ tại §4a/§6 dưới — sole direct-credential-use authority,
    KHÔNG BAO GIỜ trả raw secret cho caller (bounded signing-request pattern).
  Design status:  §4a dưới elaborate architecture-level (responsibility, authority,
    credential-reference model, signing-request lifecycle, fail-closed rules, audit) —
    KHÔNG bao gồm Vault/KMS/HSM vendor, signing algorithm, credential rotation protocol,
    hay bất kỳ implementation nào (forbidden scope §13, KHÔNG đổi).

Class: none (18 module còn lại, đóng P12-A-MAJ-02/P12-IRB-MAJ-02, lịch sử)
  Baseline:  §3.1 (bắt buộc, không miễn trừ — KHÔNG "no isolation requirement" như v0.1
    sai tuyên bố).
  Bổ sung:   KHÔNG bổ sung riêng ngoài §3.1 — 18 module này KHÔNG nhận boundary/
    ingress-egress scrutiny bổ sung của trust_boundary_candidate, KHÔNG nhận custody
    treatment của custody_adjacent/secret_consuming, NHƯNG VẪN chịu đầy đủ chín mục
    §3.1.
  Design status:  KHÔNG elaborate chức năng chi tiết riêng tại Package 1.2 (thẩm quyền
    package sở hữu chức năng của từng module) — KHÔNG đồng nghĩa "không cần đánh giá
    baseline bảo mật nào" (sửa từ v0.1). Reassessment/reclassification khi thay đổi
    kết nối/privilege/exposure — §3.1 mục 9.
```

## 4. Module boundary — Account Service (module DUY NHẤT gán cho Package 1.2, elaborate đầy đủ)

**Trách nhiệm (Package 1.1, KHÔNG đổi):** "Sở hữu Trading Account identity, account boundary binding (ADR-012), environment distinction (PAPER/LIVE), lifecycle tối thiểu." + "KHÔNG sở hữu credential/secret material (I-11)."

### 4.1 Registry classification (bảo toàn nguyên vẹn)

```text
module_type:               runtime_service
owns_authoritative_state:  true
consumes:                  command
emits:                     event, query
depends_on:                (none — root)
forbidden_dependencies:    (none)
plugin_relation:           none
security_classification:   custody_adjacent
```

### 4.2 Authoritative ownership (elaboration, đúng `account.md`)

```text
Account Service sở hữu authoritative:
  AccountRegistered/AccountMetadataRevised/AccountStatusChanged/AccountFactInvalidated
    (account.md §3–§6) — Trading Account identity, `account_boundary_ref` (ADR-012 §2.1
    canonical model: {boundary_type: venue|broker_account, boundary_id}), `environment`
    (PAPER|LIVE, bất biến), lifecycle tối thiểu (ACTIVE/SUSPENDED/CLOSED).

Account Service KHÔNG sở hữu:
  raw exchange credential (API key, private key, token, password) — account.md §10/§15
    prohibition tường minh; CHỈ giữ `credential_reference` opaque (§6 dưới).
  Instrument/Venue semantics — chỉ tham chiếu `venue_id` qua `account_boundary_ref` khi
    `boundary_type: venue` (account.md §1 invariant), KHÔNG redefine `venue.md`.
  Strategy/Decision/Risk/Execution Intent/Order/Fill/Position semantics — hoàn toàn
    ngoài phạm vi (account.md §15).
  billing/tenant/organization/IAM identity — Chapter 6 §6.4 "Account ≠ Tenant".
```

### 4.3 Account-to-boundary architecture (ADR-012, bắt buộc, yêu cầu task)

```text
Canonical Account Boundary model (ADR-012 §2.1, account.md §1):
  account_boundary_ref: {boundary_type: venue | broker_account, boundary_id: <opaque
    immutable reference>}
  Mọi Account có ĐÚNG MỘT account_boundary_ref — bất biến sau khi đăng ký; rebinding =
    tạo Account KHÁC (SCOPE_ERROR correction lineage, account.md §11), KHÔNG mutate
    subject hiện có.

Venue boundary (boundary_type: venue, ADR-012 §2.2):
  Account thuộc trực tiếp đúng MỘT Venue — boundary_id resolve tới venue_id đã
  VenueRegistered (venue.md §3, Consolidated Stable, KHÔNG redefine). Execution venue có
  thể inherit từ Account khi contract liên quan (Order/Fill, Package 1.3-D) cho phép.

Broker account boundary (boundary_type: broker_account, ADR-012 §2.3):
  Account thuộc trực tiếp một Broker Account Boundary — boundary_id là opaque reference,
  CHƯA có Domain Contract riêng (account.md §14 deferred — "chưa cần cho walking skeleton
  hiện tại, Phase 0-3 chỉ có venue boundary thực tế, ADR-012 §5 Scale check"). Mỗi
  Order/Fill PHẢI mang execution_venue_id tường minh khi boundary_type = broker_account
  (ADR-012 §2.3) — KHÔNG suy diễn ngầm từ Account.

Position scope dưới Account Boundary (ADR-012 §2.5 — carry forward, KHÔNG redefine
  Package 1.3-D's Position Projection boundary):
  venue-bound Account: Position CÓ THỂ inherit execution Venue từ Account; nếu mang
    Venue tường minh, PHẢI khớp — xung đột reject.
  broker-bound Account: MỌI transactional Position PHẢI mang execution_venue_id tường
    minh; authority của MỘT transactional Position scope bởi Account · execution Venue ·
    instrument · settlement/margin scope bổ sung (Domain Contract tương lai). Balance/
    collateral/margin/liquidation/settlement/fill-attribution venue-native KHÔNG được
    gộp xuyên-Venue trong một transactional Position.
  broker-level exposure: net Position/Exposure cấp broker là `kind: read_model`/
    projection — KHÔNG transactional Position authority, KHÔNG thay thế authority của
    transactional Position bên dưới — Package 1.3-D's `position-projection` (v0.1/v0.2
    walking skeleton, environment PAPER, boundary venue-bound implied) KHÔNG bị đổi bởi
    quan sát này.

Environment eligibility (account.md §8):
  PAPER/LIVE là enum ĐÓNG DUY NHẤT — LIVE CHỈ phân biệt account environment, KHÔNG tự
  authorize Live execution của platform (governance decision riêng, tách bạch — §8
  dưới). PAPER/LIVE Account dùng CHUNG structural contract (ADR-012 §2.4, I-2 Decision
  Parity) — KHÔNG nhánh schema riêng.
```

### 4.4 Account suspension và execution eligibility (bắt buộc, yêu cầu task)

```text
Account current_status (ACTIVE/SUSPENDED/CLOSED, account.md §1/§5) resolve theo fold
algorithm "visible-valid-head per slice" (account.md §7) TẠI computation cursor — KHÔNG
`AccountCurrentView` latest-state.

Account CHỈ hợp lệ cho action MỚI (Order/Execution, Package 1.3-D) khi current_status =
ACTIVE tại cursor liên quan (account.md §5 invariant) — SUSPENDED/CLOSED CẤM action mới.
Đây LÀ ràng buộc account.md đã PIN cho Domain Contract tương lai — risk.md §5c bước 7
(Package 1.3-D, Consolidated Stable) ĐÃ implement chính xác ràng buộc này:
`account_id.current_status(risk_context_cursor) == ACTIVE`, fail → REJECTED/
ACCOUNT_NOT_ACTIVE. Package 1.2 KHÔNG redefine — CHỈ xác nhận consistency xuyên hai
tài liệu.

CLOSED là terminal CHO FORWARD TRANSITION (account.md §1) nhưng correctable append-only
qua AccountFactInvalidated + same-slice replacement (account.md §5/§11, kể cả khi giá
trị bị invalidate là CLOSED) — KHÔNG reopening workflow riêng.
```

## 4a. Module boundary — Custody & Signing Service (MỚI v0.3 — đề xuất elaboration, ĐÃ đăng ký Package 1.1, CHƯA registry-assigned cho Package 1.2, xem §16a)

**Xác nhận tường minh (bắt buộc, yêu cầu task):** `custody-signing-service` ĐÃ registered tại `module-registry.yaml` v0.5/v0.6 (Package 1.1, Consolidated Stable) theo Approved [ADR-017](../adr/ADR-017.md) v0.2 — NHƯNG `phase.elaborated_by: null` tại registry. Package 1.2 v0.3 LÀ candidate elaboration PROPOSAL cho module này — KHÔNG PHẢI xác nhận một registry assignment đã tồn tại. Sau khi v0.3 pass Review A + Independent Review B, một Package 1.1 alignment transaction RIÊNG BIỆT phải đổi `elaborated_by: null → "1.2"` trước khi assignment đó chính thức (§16a) — KHÔNG thực hiện tại §4a này.

### 4a.1 Registry classification (hiện tại — bảo toàn nguyên vẹn, KHÔNG sửa registry)

```text
module_id:                 custody-signing-service
module_type:                runtime_service
owns_authoritative_state:   true (scoped, §4a.2)
consumes:                   command, query
emits:                      event, query
depends_on:                 account-service
forbidden_dependencies:     decision-authority-service, risk-gateway, execution-engine,
                             exchange-adapter, strategy-engine, strategy-plugin-host,
                             decision-evaluation-engine, context-aggregator,
                             position-projection, command-query-api-surface
plugin_relation:             none
security_classification:    secret_consuming
phase (registry hiện tại):  { identified_in: "1.1", elaborated_by: null }
phase (đề xuất v0.3):        elaborated_by: "1.2" — CHƯA thực hiện, xem §16a
```

### 4a.2 Authority model — được VÀ KHÔNG được authoritative (bắt buộc, yêu cầu task)

```text
Custody/Signing Service CÓ THỂ authoritative CHỈ cho:
  credential-binding identity và state (CredentialBinding, §4a.4);
  credential eligibility, suspension, và revocation state (CredentialEligibility/
    CredentialRevocationState, §4a.4);
  signing-attempt identity (SigningAttempt, §4a.4);
  signing-attempt lifecycle (§4a.5);
  signing outcome operational fact (SigningOutcome/SigningFailure, §4a.4);
  custody/signing audit provenance (§4a.11).

Custody/Signing Service KHÔNG được authoritative cho:
  raw secret material như một domain fact — secret material nằm HOÀN TOÀN ngoài Domain
    Contract scope (forbidden implementation, §13) — KHÔNG BAO GIỜ trở thành một "fact"
    được ghi nhận, kể cả gián tiếp;
  Account identity hay lifecycle — account-service's authority, KHÔNG đổi (§4);
  Decision — decision-authority-service's authority, KHÔNG đổi;
  Trade Intent — decision-authority-service's authority, KHÔNG đổi;
  RiskEvaluation — risk-gateway's authority, KHÔNG đổi;
  Execution Intent — risk-gateway's authority, KHÔNG đổi;
  Order — execution-engine's authority, KHÔNG đổi;
  Order eligibility — execution-engine's authority, KHÔNG đổi;
  ExecutionObservation — execution-result-processor's authority, KHÔNG đổi;
  ExecutionResult — execution-result-processor's authority, KHÔNG đổi;
  Fill — fill-processor's authority, KHÔNG đổi;
  Position — position-projection (non-authoritative), KHÔNG đổi;
  kill-switch authoritative state — CHƯA established cho bất kỳ module nào (§9), KHÔNG
    claim tại đây;
  venue interaction evidence — exchange-adapter's authority (raw venue-interaction
    evidence, ADR-017 §3.2a), KHÔNG đổi.

Bảo toàn (KHÔNG đổi bởi §4a):
  Account Service:                 Account identity/lifecycle, opaque credential_reference.
  Decision Authority Service:      Decision và Trade Intent.
  Risk Gateway:                    RiskEvaluation và Execution Intent.
  Execution Engine:                Order và submission orchestration.
  Exchange Adapter:                raw venue-interaction evidence only.
  Execution Result Processor:      ExecutionObservation và ExecutionResult.
  Fill Processor:                  Fill.
  Position Projection:             non-authoritative.
```

### 4a.3 Trách nhiệm (bắt buộc, yêu cầu task)

```text
Sole platform module permitted direct use của exchange credential (I-11).
Resolution của Account Service's opaque credential_reference — dưới đúng Account
  Boundary, environment, và venue scope (§4.3 trên).
Validation của Account Boundary (§4.3), environment eligibility (§8), và venue scope
  cho MỖI signing request.
Credential-binding identity và lifecycle (§4a.4 CredentialBinding).
Credential eligibility, suspension, và revocation state (§4a.4
  CredentialEligibility/CredentialRevocationState).
Bounded signing-request acceptance (§4a.5/§4a.6).
Signing-attempt identity và lifecycle (§4a.4/§4a.5).
Signing outcome và failure evidence (§4a.4 SigningOutcome/SigningFailure).
Signature hay signed-payload return KHÔNG raw-secret disclosure (I-11 Verification —
  "KMS/signing service có thể ký request mà KHÔNG BAO GIỜ trả secret cho caller").
Fail-closed behavior (§4a.8).
Audit và provenance emission (§4a.11).
Kill-switch/execution-suspension participation cho signing effect MỚI (§4a.10).
```

### 4a.4 Credential-reference model — architecture-level concept (bắt buộc, yêu cầu task, KHÔNG field-level schema)

```text
CredentialReference:            opaque reference sở hữu bởi Account Service
                                 (account.md §10, `credential_reference` field) — trỏ tới
                                 MỘT binding cụ thể bên trong Custody/Signing Service.
                                 CredentialReference tự nó KHÔNG chứa raw secret, KHÔNG
                                 resolve được ngoài Custody/Signing Service.

CredentialBinding:               concept nội bộ Custody/Signing Service — bind một
                                 CredentialReference tới: Account Boundary (§4.3);
                                 environment (PAPER | LIVE); venue; credential class/
                                 purpose (vd. trading vs withdrawal, KHÔNG field cụ thể);
                                 lifecycle status (active/suspended/revoked, phạm vi hẹp,
                                 KHÔNG conflate với Account current_status, §4.4).

CredentialEligibility:           trạng thái phái sinh xác nhận một CredentialBinding CÓ
                                 THỂ dùng cho một signing request cụ thể tại thời điểm
                                 evaluate (Account Boundary/environment/venue/purpose
                                 khớp, lifecycle status active) — KHÔNG một fact lưu trữ
                                 riêng, được evaluate MỖI signing request.

CredentialRevocationState:       trạng thái MỘT CredentialBinding cụ thể đã bị revoke
                                 hoặc suspend — tách biệt khỏi Account SUSPENDED/CLOSED
                                 (§4.4, lifecycle-level của CHÍNH Account) — một
                                 credential CÓ THỂ revoked trong khi Account vẫn ACTIVE.

SigningRequest:                  immutable request identity mang: intended Account
                                 Boundary; environment; venue; payload hoặc payload
                                 digest (KHÔNG raw payload content được author tại đây);
                                 authorization evidence (§4a.6); protocol/purpose context
                                 (bounded category, KHÔNG field-level).

SigningAttempt:                  MỘT lần thử ký cụ thể gắn với một SigningRequest — một
                                 SigningRequest CÓ THỂ có nhiều SigningAttempt (retry,
                                 §4a.5) nhưng PHẢI cùng logical identity/payload binding.

SigningOutcome:                  kết quả THÀNH CÔNG của một SigningAttempt — signature
                                 hay signed-payload evidence, KHÔNG BAO GIỜ raw secret.

SigningFailure:                  kết quả THẤT BẠI của một SigningAttempt — category lý
                                 do (§4a.7/§4a.8), KHÔNG raw secret, KHÔNG chi tiết nội
                                 bộ nhạy cảm.

SigningAuthorizationEvidence:    immutable evidence MÀ một SigningRequest PHẢI mang hoặc
                                 tham chiếu để chứng minh causal ancestry hợp lệ (ADR-017
                                 §8.2/§8.4) — KHÔNG tự nó là business authorization
                                 (§4a.6), CHỈ là bằng chứng để Custody/Signing Service
                                 xác nhận request đó eligible trước khi ký.
```

**Quan hệ (bắt buộc, yêu cầu task):**

```text
Account owns hoặc references một CredentialReference opaque.
CredentialReference resolves CHỈ bên trong Custody/Signing Service (§4a.3) — KHÔNG
  module nào khác resolve được nó.
CredentialBinding binds CredentialReference tới: Account Boundary; environment; venue;
  credential class/purpose; lifecycle status.
SigningRequest references: immutable request identity; intended Account Boundary;
  environment; venue; payload hoặc payload digest; authorization evidence; protocol/
  purpose context.
```

**Xác nhận tường minh (bắt buộc, yêu cầu task):** raw secret KHÔNG BAO GIỜ xuất hiện trong bất kỳ published contract nào — CredentialReference, CredentialBinding, SigningRequest, SigningOutcome, SigningFailure, và mọi audit record (§4a.11) đều KHÔNG chứa raw secret material. KHÔNG field-level schema nào được author cho bất kỳ concept nào ở trên (forbidden scope §13).

### 4a.5 Signing-request lifecycle (bắt buộc, yêu cầu task — minimum state distinction, KHÔNG concrete state machine implementation)

```text
RECEIVED:                request nhận, CHƯA validate.
VALIDATING:               đang validate Account Boundary/environment/venue/authorization
                          evidence/payload binding (§4a.6/§4a.7).
REJECTED:                 validation thất bại — fail-closed, KHÔNG signing attempt nào
                          được tạo (§4a.7).
AUTHORIZED_FOR_SIGNING:   validation qua, eligible cho một SigningAttempt.
SIGNING:                  một SigningAttempt đang tiến hành.
SIGNED:                   cryptographic signing HOÀN TẤT — xem xác nhận bắt buộc dưới.
FAILED:                   signing KHÔNG sinh ra signed material hợp lệ (§4a.7).
CANCELLED:                caller hoặc service hủy request TRƯỚC KHI SIGNED/FAILED chung
                          cuộc (§4a.8).
UNKNOWN_OUTCOME:          local certainty về kết quả signing operation KHÔNG đủ (§4a.8).
EXPIRED:                  request vượt quá bounded validity window mà KHÔNG đạt trạng
                          thái chung cuộc (thời gian cụ thể — forbidden scope, §13).
```

**Xác nhận bắt buộc (yêu cầu task, nguyên văn ý nghĩa):**

```text
SIGNED KHÔNG có nghĩa: venue submission đã xảy ra; Order đã executed; ExecutionResult
  hay Fill đã established — SIGNED CHỈ xác nhận cryptographic signing operation hoàn
  tất tại Custody/Signing Service, hoàn toàn TÁCH BIỆT khỏi execution-observation/
  ExecutionResult authority (exchange-adapter/execution-result-processor, §4a.2).

FAILED nghĩa signing KHÔNG sinh ra valid signed material — KHÔNG ngụ ý bất kỳ diễn giải
  nào về business/execution outcome.

UNKNOWN_OUTCOME nghĩa local certainty KHÔNG đủ — PHẢI KHÔNG được coi là thành công mà
  không qua reconciliation (§4a.8).
```

### 4a.6 Identity, idempotency, và correlation (bắt buộc, yêu cầu task — KHÔNG concrete ID format/database)

```text
Immutable SigningRequest identity — MỘT SigningRequest giữ ĐÚNG một identity xuyên suốt
  toàn bộ lifecycle (§4a.5), bất kể bao nhiêu SigningAttempt được thử.
Một logical signing request xuyên retry — retry KHÔNG tạo một logical request MỚI, CHỈ
  một SigningAttempt mới gắn cùng SigningRequest identity.
Idempotency scope — scoped ĐÚNG một SigningRequest identity (cùng nguyên tắc I-10 áp
  dụng tương tự cho signing attempt như đã áp dụng cho execution attempt, Package
  1.3-D).
Duplicate request detection — một request mới mang cùng logical identity (nếu tái gửi)
  PHẢI reconcile với request hiện có, KHÔNG tạo signing effect thứ hai độc lập.
Payload-digest binding — MỌI SigningAttempt của cùng SigningRequest PHẢI bind cùng
  payload digest — retry KHÔNG được silently ký một payload KHÁC dưới cùng logical
  identity (yêu cầu bắt buộc, xem dưới).
Authorization-evidence binding — MỌI SigningAttempt PHẢI bind cùng
  SigningAuthorizationEvidence đã validate tại RECEIVED/VALIDATING (§4a.5) — evidence
  KHÔNG được thay đổi giữa các attempt của cùng request.
Account Boundary/environment/venue binding — bảo toàn xuyên suốt mọi SigningAttempt của
  cùng SigningRequest — mismatch giữa attempt PHẢI fail closed (§4a.7).
Correlation bắt buộc:  execution submission request (Execution Engine → Exchange
  Adapter, ADR-017 §8.1, KHÔNG chạm PAPER) ↔ signing request (Exchange Adapter →
  Custody/Signing Service, §4a.11) ↔ signing attempt ↔ signing outcome ↔ future venue
  submission evidence (Exchange Adapter, ADR-017 §3.2a) — bốn khâu này PHẢI correlate
  được, KHÔNG thiết kế concrete correlation ID/mechanism tại đây (§14 gap, kế thừa
  ADR-017 §14 gap #12).

**Bất biến bắt buộc:** một retry KHÔNG BAO GIỜ được phép silently ký một payload KHÁC
dưới cùng logical identity — vi phạm bất biến này LÀ một fail-closed condition (§4a.7),
KHÔNG một hành vi hợp lệ dưới bất kỳ tình huống nào.
```

### 4a.7 Caller authorization boundary (bắt buộc, yêu cầu task)

```text
Allowed caller categories (KHÔNG invent runtime implementation):
  future authorized Exchange Adapter interaction (ADR-017 §8.5 — Exchange Adapter là
    caller CHÍNH, sau khi module đó functionally elaborate và hoàn thiện, §14 gap);
  explicitly approved administrative custody operation, NẾU governance (RBAC/OQ-001,
    §14 gap) cho phép — KHÔNG tự cấp quyền này tại đây.

Prohibited — direct signing access CẤM tường minh cho (tối thiểu):
  strategy-engine
  strategy-plugin-host
  decision-evaluation-engine
  decision-authority-service
  risk-gateway
  context-aggregator
  position-projection
  command-query-api-surface
  ux-application-shell

(`forbidden_dependencies` (§4a.1) VÀ caller-authorization boundary này LÀ HAI kiểm soát
tách biệt, khác chiều, v0.4 correction — bắt buộc phân biệt tường minh: `forbidden_
dependencies` kiểm soát module NÀO custody-signing-service ĐƯỢC PHÉP tự phụ thuộc/gọi
(chiều custody-signing-service → module khác); caller-authorization boundary kiểm soát
module NÀO ĐƯỢC PHÉP submit SigningRequest tới custody-signing-service (chiều NGƯỢC LẠI,
module khác → custody-signing-service). `forbidden_dependencies` KHÔNG BAO GIỜ được dùng
làm bằng chứng cho caller authorization — trùng lặp một phần giữa hai danh sách (strategy-
engine, strategy-plugin-host, decision-evaluation-engine, decision-authority-service,
risk-gateway, context-aggregator, position-projection, command-query-api-surface xuất
hiện ở CẢ HAI) là kết quả riêng biệt của domain logic hiện tại, KHÔNG PHẢI suy diễn một
chiều từ chiều kia. `exchange-adapter` minh họa rõ sự khác biệt: nó nằm trong `forbidden_
dependencies` của custody-signing-service (custody-signing-service KHÔNG được phụ thuộc/
gọi ngược exchange-adapter) NHƯNG đồng thời LÀ caller CHÍNH tương lai được phép (trên,
§4a.7 — ADR-017 §8.5) — hai vai trò này KHÔNG mâu thuẫn vì thuộc hai chiều khác nhau.
`execution-engine` KHÔNG gọi trực tiếp Custody/Signing Service (ADR-017 §8.5) — đây LÀ
một xác nhận caller-authorization riêng biệt, KHÔNG suy ra chỉ vì nó cũng nằm trong
`forbidden_dependencies`.)
```

**Xác nhận tường minh (bắt buộc, yêu cầu task, khớp ADR-017 §8.4/§7 trên):**

```text
Carrying immutable SigningAuthorizationEvidence KHÔNG tạo một dependency lên Decision
  Authority Service hay Risk Gateway — evidence được CARRY trong request, KHÔNG PHẢI
  một runtime call ngược lại authority đó (forbidden_dependencies §4a.1 giữ nguyên).
Possession của một payload KHÔNG tự nó authorize signing — request PHẢI qua validation
  (§4a.5 VALIDATING) trước khi AUTHORIZED_FOR_SIGNING.
Possession của một valid signature KHÔNG tạo business authorization — cùng nguyên tắc
  đã pin tại §5/ADR-017 §7 — signature hợp lệ CHỈ chứng minh custody authority đã hoạt
  động đúng, KHÔNG chứng minh Decision/Risk/Execution authorization.
```

### 4a.8 Fail-closed rules (bắt buộc, yêu cầu task)

Signing PHẢI fail closed khi bất kỳ điều kiện bắt buộc nào sau đây:

```text
missing               — CredentialReference/CredentialBinding/authorization evidence
                         không resolve được.
invalid                — CredentialBinding/authorization evidence không đúng dạng mong
                         đợi (semantic, KHÔNG field-level).
stale                  — evidence/binding không còn hiệu lực tại cursor/thời điểm request.
revoked                — CredentialRevocationState active cho binding liên quan.
suspended              — CredentialEligibility tạm ngưng (khác Account suspension, §4.4).
expired                — SigningRequest vượt bounded validity window (§4a.5 EXPIRED).
environment-mismatched — request environment (PAPER|LIVE) không khớp CredentialBinding.
venue-mismatched        — request venue không khớp CredentialBinding.
Account-Boundary-       — request Account Boundary không khớp CredentialBinding (§4.3).
  mismatched
payload-mismatched      — SigningAttempt retry mang payload digest KHÁC attempt trước
                         của cùng SigningRequest (§4a.6 bất biến).
authorization-evidence- — SigningAttempt retry mang evidence KHÁC attempt trước của cùng
  mismatched              SigningRequest (§4a.6).
unsupported             — request category/purpose KHÔNG được Custody/Signing Service
                         hỗ trợ (bounded category, KHÔNG field-level).
ambiguous               — nhiều hơn một CredentialBinding eligible cạnh tranh cho cùng
                         request mà KHÔNG resolve dứt khoát được.
unverifiable            — Custody/Signing Service KHÔNG thể verify một điều kiện bắt
                         buộc trên (do bất kỳ lý do gì) tại thời điểm cần quyết định.
```

**Xác nhận bắt buộc:** fail-closed behavior KHÔNG BAO GIỜ leak raw-secret material — SigningFailure category/reason KHÔNG chứa raw secret, private key, hay bất kỳ sensitive credential material nào (§4a.11).

### 4a.9 Timeout, cancellation, và uncertain outcome (bắt buộc, yêu cầu task — KHÔNG timing numbers/algorithm)

```text
Request timeout:                     SigningRequest KHÔNG đạt trạng thái chung cuộc
                                     trong bounded validity window → EXPIRED (§4a.5).
Signing-operation timeout:           một SigningAttempt cụ thể KHÔNG hoàn tất trong
                                     bounded window → góp phần UNKNOWN_OUTCOME (dưới),
                                     KHÔNG tự động FAILED.
Caller cancellation:                 caller (Exchange Adapter, §4a.7) yêu cầu hủy TRƯỚC
                                     KHI SIGNED/FAILED → CANCELLED, nếu cursor lifecycle
                                     cho phép.
Service cancellation:                Custody/Signing Service tự hủy (vd. do fail-closed
                                     condition kích hoạt giữa chừng, §4a.8) → CANCELLED
                                     hoặc REJECTED tùy giai đoạn lifecycle.
Credential revocation during        nếu CredentialRevocationState kích hoạt giữa một
  signing:                          SigningAttempt đang tiến hành → in-flight handling
                                     CHƯA established (§4a.10/§14 gap #6, KHÔNG resolve
                                     tại đây, v0.4 correction) — revocation CHẶN
                                     SigningRequest/SigningAttempt MỚI (§4a.5), KHÔNG tự
                                     động quyết định outcome của attempt đã in-flight.
Execution suspension during         nếu execution-suspension (kill-switch, §4a.10) kích
  signing:                          hoạt giữa một SigningAttempt đang tiến hành → in-
                                     flight handling CHƯA established (§4a.10/§14 gap,
                                     KHÔNG resolve tại đây).
Unknown signing outcome:             local certainty không đủ để xác nhận SIGNED hay
                                     FAILED → UNKNOWN_OUTCOME (§4a.5).
Retry after uncertain outcome:       PHẢI reconcile trước khi retry — retry mù KHÔNG
                                     được phép; reconciliation mechanism cụ thể CHƯA
                                     thiết kế (§14 gap, kế thừa ADR-017 §14 gap #12).
```

**Yêu cầu bắt buộc (nguyên văn ý nghĩa, yêu cầu task):**

```text
Timeout KHÔNG tương đương failure trừ khi CONFIRMED (qua reconciliation hoặc terminal
  signal xác nhận).
Timeout KHÔNG tương đương success.
Unknown outcome ĐÒI HỎI reconciliation HOẶC explicit terminal handling — KHÔNG được để
  ở trạng thái mơ hồ vô thời hạn.
Retry PHẢI bảo toàn logical identity và payload binding (§4a.6 bất biến).
Revocation hay execution suspension CHẶN signing effect MỚI (§4a.10) — KHÔNG chặn việc
  reconcile một attempt đã in-flight (khác nhau, KHÔNG conflate).
In-flight handling VẪN tường minh UNRESOLVED nơi CHƯA có một safe rule được Approved
  bởi ADR — KHÔNG tự phát minh rule đó tại đây.
```

### 4a.10 Kill-switch participation (custody-specific — bắt buộc, yêu cầu task, KHÔNG assign state ownership)

```text
Đã established (Package 1.3-D §11 + ADR-017 §10, KHÔNG đổi):
  Risk Gateway sở hữu kill-switch policy evaluation/enforcement.
  Custody/Signing Service LÀ fail-safe participant — SELECTED bởi ADR-017 như một
    consequence của I-6/I-8/I-11 kết hợp (I-8 KHÔNG literally name module này — khác
    Exchange Adapter, xem dưới).
  Exchange Adapter LÀ future execution-suspension participant — expressly ANTICIPATED
    bởi I-8 Scope tường minh ("Risk Gateway, Execution Engine, mọi Exchange Adapter").

CHƯA established (KHÔNG assign tại đây):
  authoritative kill-switch-state owner — VẪN unresolved, KHÔNG claim cho
    custody-signing-service, exchange-adapter, account-service, hay bất kỳ module nào
    khác (§9, ADR-017 §10, Package 1.3-D §16 gap #4).

Observation requirement (architecture-level ONLY, bắt buộc yêu cầu task):
  Custody/Signing Service KHÔNG được sinh ra signed material MỚI khi execution
  suspension đang active, stale, hoặc unknown — tuân theo fail-closed policy đã Approved
  (§4a.8, ADR-017 §10). KHÔNG author observation mechanism cụ thể (CHƯA established).

In-flight behavior — KHÔNG fully resolve tại đây trừ khi ĐÃ controlled bởi một ADR
  Approved (chưa có) — kế thừa nguyên vẹn §4a.9 trên, Package 1.3-D §16 gap #4, ADR-017
  §14 gap #3.
```

### 4a.11 Audit và provenance (bắt buộc, yêu cầu task)

**Required audit categories:**

```text
credential-reference resolution attempt (thành công hay thất bại);
credential eligibility evaluation (kết quả VÀ tiêu chí evaluate — category, KHÔNG raw
  credential data);
signing-request receipt;
request validation outcome (§4a.5 RECEIVED → VALIDATING → REJECTED|AUTHORIZED_FOR_
  SIGNING);
authorization-evidence validation outcome;
signing-attempt start;
signing-attempt outcome (SIGNED|FAILED|CANCELLED|UNKNOWN_OUTCOME|EXPIRED);
rejection reason category (§4a.8 fail-closed condition category, KHÔNG raw secret);
revocation/suspension observation (CredentialRevocationState transition observed);
timeout/cancellation/unknown outcome events (§4a.9);
caller identity hay caller boundary evidence (WHO gửi request, KHÔNG raw credential);
Account Boundary/environment/venue binding (§4a.3, cho mỗi request/attempt);
payload-digest hay non-secret binding evidence tương đương (KHÔNG raw payload content
  khi policy đánh dấu sensitive).
```

**Audit records PHẢI loại trừ (bắt buộc, yêu cầu task):**

```text
raw secret;
private key;
seed phrase;
recovery secret;
full sensitive credential material dưới bất kỳ hình thức nào;
unredacted signed payload KHI policy đánh dấu sensitive (redaction policy cụ thể —
  forbidden scope, §13).
```

**Authoritative source cho mỗi custody/signing audit fact:** `custody-signing-service` LÀ nguồn authoritative DUY NHẤT cho toàn bộ danh sách audit category trên (§4a.2 authority model) — KHÔNG module nào khác phát sinh các fact này song song. KHÔNG author audit log schema/storage cụ thể (forbidden scope §13 — database schema) — CHỈ pin YÊU CẦU category audit trail phải tồn tại VÀ thuộc đúng module nào, đúng nguyên tắc đã dùng cho account-service (§12).

### 4a.12 Interaction boundaries (bắt buộc, yêu cầu task)

```text
Account Service → Custody/Signing Service:
  opaque credential reference VÀ account-boundary facts (Account Boundary, environment)
  cần thiết để resolve CredentialBinding (§4a.3/§4a.4) — qua published query contract
  (module-registry.yaml: custody-signing-service.depends_on: [account-service]).

Future Exchange Adapter → Custody/Signing Service:
  bounded signing request (SigningRequest, §4a.3) — qua published command contract.
  KHÔNG active tại v0.3 (exchange-adapter functionally unelaborated, §14) — interaction
  boundary được ĐỊNH DANH architecture-level, KHÔNG activated runtime.

Custody/Signing Service → Future Exchange Adapter:
  signature hoặc signed-payload evidence (SigningOutcome, §4a.3) — KHÔNG BAO GIỜ raw
  secret; signing failure hoặc rejection evidence (SigningFailure, §4a.3) khi áp dụng.

Custody/Signing Service → audit/evidence consumers:
  non-secret custody/signing provenance (§4a.11) — qua published query contract
  (`emits: [event, query]`, §4a.1), category-only, KHÔNG field-level schema.
```

**KHÔNG active tại v0.3 (bắt buộc, yêu cầu task):** `execution-engine → exchange-adapter` dependency edge KHÔNG được thêm — cùng xác nhận đã pin tại ADR-017 §8.1/§9a (Stage 1 registration ≠ Stage 2 LIVE-path activation) và Package 1.1 v0.5/v0.6 (`execution-engine.depends_on` giữ nguyên `[risk-gateway, paper-execution-boundary]`). Package 1.2 v0.3 KHÔNG activate LIVE dưới bất kỳ hình thức nào (§8 dưới).

## 5. Execution authorization vs transport (bắt buộc, yêu cầu task — consistency check với Package 1.3-D)

**Xác nhận tường minh:** Package 1.2 KHÔNG redefine ranh giới đã pin tại Package 1.3-D v0.2 (§8.1, đóng `P13D-A-MAJ-01`/`P13D-IRB-MAJ-01`) — CHỈ xác nhận consistency:

```text
Business authorization (Decision/Risk/Execution Intent) LÀ authority của Decision
  Authority Service/Risk Gateway (Package 1.3-C/1.3-D, Consolidated Stable/review-clean)
  — Package 1.2 KHÔNG chạm, KHÔNG tạo đường business-authority thay thế.

Custody/signing authorization (§6 dưới) LÀ MỘT authority KHÁC HOÀN TOÀN — I-11 Scope:
  "Chỉ Exchange Adapter hoặc dedicated Custody/Signing Service được phép sử dụng
  exchange credential trực tiếp." HAI loại authorization này KHÔNG BAO GIỜ được conflate
  — một business-approved Execution Intent (Risk Gateway) KHÔNG tự động cấp quyền truy
  cập credential (Custody/Signing Service, riêng biệt); ngược lại, một credential hợp lệ
  KHÔNG tự nó tạo business authorization (Risk Gateway vẫn PHẢI approve trước).

Transport delivery (API/Event Bus/scheduler/orchestration, Package 1.3-D §8.1 v0.2
  correction) KHÔNG BAO GIỜ tạo execution authorization tự thân — nguyên tắc NÀY áp
  dụng ĐỒNG NHẤT cho cả business VÀ custody/signing authorization: transport CHỈ mang
  request, KHÔNG BAO GIỜ tự thân là authority.

Raw venue-interaction evidence (Exchange Adapter, ADR-017 §3.2a — module NAY đăng ký,
  functionally unelaborated, §14) KHÁC execution observation (ExecutionResult/Fill,
  Package 1.3-D authority) — raw venue-interaction evidence sẽ là MỘT input evidence cho
  execution observation KHI exchange-adapter functionally elaborate VÀ execution-engine
  → exchange-adapter được kích hoạt (Stage 2, ADR-017 §9a — KHÔNG active tại v0.3), KHÔNG
  PHẢI observation tự thân.

Signing outcome (custody-signing-service, §4a.5 SIGNED/FAILED) KHÁC CẢ HAI khái niệm
  trên — SIGNED CHỈ xác nhận cryptographic signing operation hoàn tất, KHÔNG ngụ ý venue
  interaction hay execution observation nào (§4a.5 xác nhận bắt buộc).
```

## 6. Custody và signing isolation (I-11, bắt buộc, yêu cầu task — §4a nay elaborate đầy đủ hơn cho custody-signing-service, mục này giữ nguyên làm cross-cutting summary)

```text
Credential/secret isolation (account.md §10, ADR-012 §2.4, I-11 nguyên văn):
  API key/secret/private key KHÔNG BAO GIỜ lưu dạng plaintext — bắt buộc qua Vault/KMS
  (concrete mechanism deferred, §14). Account Service CHỈ giữ `credential_reference` —
  opaque reference tới credential binding BÊN NGOÀI Domain Contract, TUYỆT ĐỐI KHÔNG
  raw secret dưới bất kỳ hình thức nào (payload/snapshot/log/replay artifact).

Signing requests vs signed payloads (I-11 phân biệt, elaboration — v0.3 cập nhật: pattern
  ĐÃ chọn qua ADR-017):
  "sử dụng credential trực tiếp" (I-11 Required guarantees) KHÔNG nhất thiết nghĩa là
  đọc raw secret — I-11's Verification clause nguyên văn: "KMS/signing service có thể ký
  request mà KHÔNG BAO GIỜ trả secret cho caller." ADR-017 v0.2 Approved đã CHỌN signing-
  request pattern (Option C — module gửi payload cần ký tới `custody-signing-service`,
  nhận lại signature, KHÔNG BAO GIỜ thấy private key, §4a.3/§4a.5) — KHÔNG còn "hai mô
  hình chưa chọn" như v0.1/v0.2; concrete signing algorithm/protocol VẪN forbidden scope
  (§13).

Least-privilege access (I-11 Required guarantees, nguyên văn — Chapter 2, Locked, KHÔNG
  sửa tại đây):
  "Execution Engine tương tác qua contract (gửi execution command), KHÔNG cần đọc raw
  secret TRỪ KHI được triển khai cùng trust boundary với Adapter." Văn bản Locked này
  giữ nguyên conditional clause đó ở mức constitutional — Package 1.2 KHÔNG sửa/xóa I-11.

  Áp dụng CỤ THỂ dưới ADR-017 v0.2 (Approved) Option C (bắt buộc, v0.4 correction): Option
  C ĐÃ CHỌN custody-signing-service làm module DUY NHẤT trong toàn platform được phép sử
  dụng exchange credential trực tiếp (§4a.2/§4a.3) — quyết định kiến trúc CỤ THỂ này
  KHÔNG exercise conditional trust-boundary exception mà I-11 cho phép ở mức nguyên tắc
  chung. Dưới kiến trúc ĐÃ Approved này: Execution Engine (Package 1.3-D) KHÔNG BAO GIỜ
  được cấp quyền đọc raw secret trực tiếp, dưới BẤT KỲ hình thức nào — co-location, chia
  sẻ process, chia sẻ host, cùng network zone, hay bất kỳ deployment topology nào ĐỀU
  KHÔNG chuyển giao credential-use authority sang Execution Engine. Exchange Adapter
  (venue-facing transport, §7) nhận CHỈ signature hay signed-payload evidence từ
  custody-signing-service (SigningOutcome, §4a.4/§4a.5) — KHÔNG BAO GIỜ raw secret. Một
  kiến trúc tương lai muốn exercise conditional exception đó cho Execution Engine sẽ cần
  một ADR MỚI thay thế/bổ sung ADR-017 — KHÔNG PHẢI điều Package 1.2 tự cấp hay carry
  forward tại đây.

Secret non-exposure — xác nhận tường minh cho TỪNG layer (yêu cầu task):
  Strategy/Plugin (Package 1.3-C):        KHÔNG được cấp quyền — I-11 Prohibited
                                            behavior tường minh: "Strategy/Decision Engine
                                            được cấp quyền truy cập trực tiếp secret của
                                            sàn" là vi phạm.
  Decision (Package 1.3-C):               KHÔNG được cấp quyền — cùng lý do trên.
  Risk (Package 1.3-D):                    KHÔNG được cấp quyền — Risk Gateway's business
                                            authorization (§5 trên) hoàn toàn tách biệt
                                            khỏi credential access; risk-gateway
                                            KHÔNG có depends_on edge tới bất kỳ custody
                                            module nào (module-registry.yaml v0.6);
                                            `custody-signing-service.forbidden_
                                            dependencies` cũng loại trừ risk-gateway
                                            hai chiều (§4a.1).
  Decision Evaluation/Authority           KHÔNG được cấp quyền — cùng lý do trên;
    (Package 1.3-C):                       `custody-signing-service.forbidden_
                                            dependencies` loại trừ CẢ HAI (§4a.1/§4a.7).
  Projection (Position Projection,        KHÔNG được cấp quyền — projection module
    Context Aggregator, Package 1.3-B/D):  (owns_authoritative_state: false) không có
                                            business hay custody nào cần secret;
                                            `custody-signing-service.forbidden_
                                            dependencies` loại trừ cả hai (§4a.1).
  General API/UX (command-query-api-      KHÔNG được cấp quyền đọc raw secret — API
    surface, ux-application-shell,        surface là routing/exposure layer (module-
    Package 1.4/1.6):                     registry.yaml notes), KHÔNG business logic
                                            riêng; account-service.depends_on rỗng
                                            (root) — command-query-api-surface chỉ
                                            tương tác qua published command/query
                                            contract (`credential_reference` opaque),
                                            KHÔNG raw secret nào lộ qua surface đó;
                                            `custody-signing-service.forbidden_
                                            dependencies` loại trừ command-query-api-
                                            surface tường minh (§4a.1/§4a.7).
  Execution Engine (Package 1.3-D):        KHÔNG được cấp quyền gọi trực tiếp
                                            custody-signing-service — chỉ Exchange
                                            Adapter (future, functionally unelaborated)
                                            LÀ caller được phép (§4a.7); execution-engine
                                            → custody-signing-service KHÔNG phải một
                                            interaction hợp lệ dưới bất kỳ hình thức nào
                                            (ADR-017 §8.5).

Account-to-boundary cardinality:  §4.3 trên — canonical model đã pin, ADR-012 Approved.

Environment và venue eligibility:  §4.3/§8 dưới — PAPER/LIVE closed enum, venue eligibility
  qua `account_boundary_ref` (§4.3).

Audit evidence:  §12 dưới.

Revocation hay suspension handling:  account.md §5 (Account SUSPENDED/CLOSED, §4.4 trên)
  là lifecycle-level suspension của CHÍNH Account — KHÁC credential revocation (thu hồi
  MỘT credential_reference cụ thể trong khi Account vẫn ACTIVE). Credential rotation dùng
  AccountMetadataRevised (§4, forward-looking, field `credential_reference` clearable,
  account.md §10) — "Cơ chế vận hành thực tế của việc rotate (khi nào, ai kích hoạt, đồng
  bộ với Vault/KMS) là Phase 1 operational concern" (account.md §10, nguyên văn) — carry
  forward §15, Package 1.2 KHÔNG author cơ chế đó.

Fail-closed unknown state:  §13 dưới.
```

**Xác nhận tường minh (yêu cầu task — "Do not author key storage implementation; HSM or vault selection; exchange API fields; signature algorithms; credential rotation protocol; database schema; network topology; cloud provider design"):** mọi mục trên là YÊU CẦU architecture-level (WHAT phải đúng) — Package 1.2 KHÔNG chọn Vault/KMS vendor cụ thể, KHÔNG author signing algorithm, KHÔNG author database schema cho credential storage, KHÔNG chọn network topology hay cloud provider.

## 7. Venue-adapter/execution-boundary treatment (bắt buộc, yêu cầu task — cập nhật v0.3, module NAY đăng ký, exchange-adapter VẪN functionally unelaborated)

```text
Cập nhật tường minh (v0.3, thay thế nội dung v0.1/v0.2 ĐÃ stale): CẢ HAI module
"Exchange Adapter" (`exchange-adapter`) VÀ "Custody-Signing Service"
(`custody-signing-service`) NAY đăng ký tại module-registry.yaml v0.6 (Package 1.1,
Consolidated Stable) theo Approved ADR-017 v0.2 (Option C split) — I-11's authority
reference ("Chỉ Exchange Adapter hoặc dedicated Custody/Signing Service") NAY có CẢ HAI
module tương ứng trong 25-module inventory.

`custody-signing-service` — direct-secret-use authority — được §4a elaborate ĐẦY ĐỦ tại
transaction này (candidate proposal, §16a).

`exchange-adapter` — venue protocol translation/transport — VẪN functionally
unelaborated: Package 1.2 KHÔNG elaborate chức năng của module này (thẩm quyền một
package TƯƠNG LAI CHƯA xác định, §14 gap — `phase.elaborated_by: null`, KHÔNG package
nào trong chín package Phase 1 hiện tại PAPER-focused sở hữu nó). Package 1.2 KHÔNG tạo
elaborating package mới cho module này (ngoài thẩm quyền Package 1.2).

Yêu cầu ĐÃ established (I-11/Chapter 9/ADR-017, KHÔNG invent) áp dụng NGAY cho cả hai
module NAY registered:
  custody-signing-service, VÀ CHỈ nó, được phép sử dụng exchange credential trực tiếp
    (I-11, ADR-017 §3.1/§4a.2) — exchange-adapter KHÔNG raw-secret access (Option C).
  Execution Engine (Package 1.3-D) tương tác với exchange-adapter qua published contract
    (command category, ADR-017 §8.1) — MỘT contract boundary RIÊNG BIỆT khỏi PAPER
    (Paper Execution Boundary), KHÔNG active tại v0.3 (execution-engine.depends_on KHÔNG
    đổi, §4a.12).
  I-8 Kill Switch Scope MỞ RỘNG bao gồm exchange-adapter ("Risk Gateway, Execution
    Engine, mọi Exchange Adapter") — ANTICIPATED tường minh (§4a.10/§9 dưới);
    custody-signing-service's kill-switch participation ĐƯỢC CHỌN bởi ADR-017 dưới I-6/
    I-8/I-11 kết hợp (§4a.10) — KHÔNG resolve state ownership cho module nào.
  I-11 Grant layer (Chapter 9 §9.6) áp dụng: permission GRANT (quyền THỰC SỰ được cấp)
    PHẢI versioned, KHÔNG suy từ declaration; Enforcement tại đúng runtime authority
    (custody-signing-service); Verification qua network ACL/API authorization scope/
    credential audit (§4a.11).
```

## 8. PAPER và LIVE — xác nhận CHÍNH XÁC những gì Package 1.2 thiết lập, KHÔNG invent thêm (bắt buộc, yêu cầu task)

```text
Đã thiết lập BỞI account.md (Package 0.2-C2, Consolidated Stable, KHÔNG sửa tại đây),
Package 1.2 CHỈ xác nhận:
  environment: [PAPER, LIVE] — enum ĐÓNG hai giá trị (account.md §8) — Account entity
    CÓ THỂ mang environment: LIVE ngay từ v0.1 (Account first-class từ ADR-007), NHƯNG
    LIVE value KHÔNG tự authorize Live execution của platform (account.md §8, ADR-007
    "Live execution authorization là quyết định governance riêng").
  PAPER và LIVE Account dùng CHUNG structural contract — KHÔNG nhánh schema riêng (I-2
    Decision Parity, ADR-012 §2.4/§2.6 mục 8).

Package 1.2 KHÔNG thiết lập (KHÔNG invent LIVE support để thỏa mãn Package 1.3-D, đúng
yêu cầu task):
  bất kỳ venue/execution/custody LIVE path THẬT nào — Package 1.3-D §3/§8.1 đã xác nhận
    toàn bộ sáu Domain Contract (risk.md → position.md) là PAPER-only tại v0.1/v0.2;
    Package 1.2 KHÔNG thêm LIVE path mới ở tầng account-service/custody boundary để
    "hoàn thiện" pipeline đó. `custody-signing-service` ĐÃ elaborate architecture-level
    (§4a) như MỘT future-capable security boundary — KHÔNG activate như một phần của
    LIVE execution path bởi package này (§4a.12 xác nhận tường minh).
  `exchange-adapter` VẪN registered nhưng functionally unelaborated — KHÔNG active
    execution path (§7 trên).

Prerequisite còn lại cho LIVE tương lai (carry forward, KHÔNG resolve tại đây, cập nhật
v0.3 — module registration NAY resolved, các mục còn lại KHÔNG đổi):
  DD-003 (PAPER-context authoritative Decision establishment mechanism, Package 1.3-D
    §8.2/§16 — KHÔNG chạm Package 1.2, ngoài phạm vi hoàn toàn).
  Exchange Adapter functional elaboration + elaborating package assignment (§7/§14 —
    module registration ĐÃ resolved qua ADR-017/Package 1.1 v0.5, nhưng CHỨC NĂNG VẪN
    chưa elaborate bởi bất kỳ package nào).
  Execution Engine → Exchange Adapter LIVE path activation (Stage 2, ADR-017 §9a — Stage
    1 registration KHÔNG tự kích hoạt).
  Broker Account Boundary Domain Contract (account.md §14, khi boundary_type=
    broker_account cần schema chi tiết hơn opaque reference).
  Venue adapter protocol (Package 1.3-D §16 gap #3, CHƯA author bởi bất kỳ package nào).

PAPER state isolation từ future LIVE custody/venue state:
  cấu trúc HIỆN TẠI (environment field trên MỌI entity liên quan — Account, Order,
  ExecutionResult, Fill, Position) đã đảm bảo PAPER/LIVE là hai giá trị scope TÁCH BIỆT
  theo cấu trúc identity (account.md §1: environment bất biến, đổi environment = Account
  KHÁC) — Package 1.3-D §9.3 đã xác nhận Position key BAO GỒM `environment`. Khi LIVE
  execution path thật được mô hình hóa (tương lai), isolation NÀY đã có SẴN ở tầng
  identity — Package 1.2 KHÔNG cần thêm cơ chế runtime isolation mới cho phần identity,
  NHƯNG credential/custody isolation GIỮA PAPER-simulated credential_reference (nếu có)
  và LIVE-thật credential_reference CHƯA có ràng buộc tường minh nào ngoài "PAPER và LIVE
  Account dùng chung structural contract" — carry forward §15 gap.
```

## 9. Kill-switch interaction (bắt buộc, yêu cầu task — KHÔNG silently claim state ownership)

```text
Xác nhận tường minh, KHÔNG mở rộng: Package 1.3-D v0.2 (§11, đóng `P13D-IRB-MAJ-02`) đã
xác lập chính xác:
  Risk Gateway sở hữu kill-switch POLICY EVALUATION/ENFORCEMENT — ĐÃ established.
  Authoritative kill-switch-state ownership — CHƯA established.

Package 1.2 KHÔNG silently claim state ownership đó cho `account-service` hay bất kỳ
module custody/venue nào khác — KHÔNG controlling source (Chapter 2, module-registry.yaml,
account.md) gán trách nhiệm này cho account-service.

Custody/venue participation ĐÃ established (I-8 Scope, nguyên văn: "Risk Gateway,
Execution Engine, mọi Exchange Adapter") — Exchange Adapter PHẢI observe kill-switch nay
module đó ĐÃ tồn tại (registered, §7 trên) — Package 1.2 CHỈ xác nhận yêu cầu SCOPE này,
KHÔNG author observation mechanism (CHƯA established, đúng Package 1.3-D §11).
`custody-signing-service`'s participation (fail-safe, KHÔNG literal I-8 Scope entry —
đầy đủ tại §4a.10) ĐƯỢC CHỌN bởi ADR-017 dưới I-6/I-8/I-11 kết hợp — KHÔNG conflate với
`exchange-adapter`'s literal I-8 Scope anticipation.

account-service's vai trò trong kill-switch scope: I-8 Scope KHÔNG liệt kê account-service
tường minh — account-service's liên quan CHỈ gián tiếp qua Account current_status
(SUSPENDED/CLOSED, §4.4 trên) là MỘT input evidence riêng biệt cho Risk Gateway's
existing eligibility check (risk.md §5c bước 7, KHÔNG phải kill-switch mechanism). Package
1.2 KHÔNG conflate hai khái niệm này — Account suspension (business/operational lifecycle)
KHÁC kill-switch (risk-scope safety control, I-8).

Owner/representation/freshness/observation/in-flight gap — bảo toàn NGUYÊN VẸN từ Package
1.3-D §16 gap #4 (KHÔNG resolve, KHÔNG mở rộng, KHÔNG thu hẹp tại Package 1.2).
```

## 10. Fail-safe behavior — custody/boundary state absent, stale, unknown, version-mismatched (I-6, bắt buộc, yêu cầu task)

```text
Nguyên tắc chung (I-6 Fail-Safe by Scope, Chapter 2, Locked, nguyên văn): "Khi không thể
xác định tính đúng đắn của dữ liệu, trạng thái, risk hoặc execution trong một scope, hệ
thống phải chuyển scope đó về trạng thái an toàn. Mặc định không được mở thêm
risk-increasing exposure."

Áp dụng cho custody/boundary state (elaboration, KHÔNG author mechanism):
  Account boundary reference (`account_boundary_ref`) unresolvable tại cursor — account.md
    §1 invariant: `boundary_type: venue` PHẢI resolve tới venue_id đã VenueRegistered;
    unresolvable → Account registration invalid, PHẢI reject khi append (account.md §3
    invariant) — fail-closed tại chính domain layer, KHÔNG cần cơ chế bổ sung.
  credential_reference absent/unresolvable tại thời điểm cần dùng — Package 1.2 KHÔNG
    author cơ chế resolve cụ thể (§6, §14 gap: "cơ chế credential reference cụ thể...
    Phase 1 Security & Custody Baseline" — account.md §14/ADR-012 §6 đã defer chính XÁC
    tới đây, NHƯNG "defer tới đây" KHÔNG nghĩa là "author tại v0.3 candidate này" — carry
    forward, đúng forbidden scope "key storage implementation"). §4a.8 nay elaborate đầy
    đủ chín điều kiện fail-closed cụ thể cho `custody-signing-service` (missing/invalid/
    stale/revoked/suspended/expired/environment-mismatched/venue-mismatched/Account-
    Boundary-mismatched/payload-mismatched/authorization-evidence-mismatched/
    unsupported/ambiguous/unverifiable) — KHÔNG author mechanism cụ thể, CHỈ điều kiện.
  Account current_status stale/unknown TẠI cursor — risk.md §5c bước 7 (Package 1.3-D,
    Consolidated Stable) ĐÃ pin: reconstruct TẠI cursor từ authoritative Account event
    stream, KHÔNG AccountCurrentView latest-state; nếu KHÔNG resolve được ACTIVE tường
    minh tại cursor đó → RiskEvaluation NON_EVALUABLE (risk.md §5c Branch A) — fail-closed
    ĐÃ hoạt động ở tầng domain hiện có.
  custody/venue boundary state version-mismatch (definition version pinning tương tự
    risk.md §5b3 bốn trục) — KHÔNG áp dụng trực tiếp cho account-service (account.md
    KHÔNG có "definition version" axis riêng cho credential — chỉ opaque reference).
    `exchange-adapter` (registered §7, functionally unelaborated) version-mismatch
    fail-safe sẽ cần elaborate riêng bởi package tương lai sở hữu nó — carry forward §14.

KHÔNG author cơ chế detect "stale/unknown" cụ thể ngoài những gì Domain Contract đã pin
(đúng nguyên tắc "Do not invent" xuyên suốt task) — Package 1.2 CHỈ áp dụng I-6 như
nguyên tắc chung, tổng hợp các fail-closed behavior ĐÃ tồn tại tại Domain Contract/
Package 1.3-D, KHÔNG thêm cơ chế mới.
```

## 11. Idempotency (I-10 tie-in, elaboration ngắn — KHÔNG mở rộng phạm vi task)

```text
account-service.consumes: [command] — mọi command (register/revise/status-change) PHẢI
tuân idempotency pattern ĐÃ pin tại account.md (§9 canonical policy identifiers:
`revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET`, `initial_fact_correction_policy:
INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES`) — Package 1.2
KHÔNG author idempotency key/mechanism mới, CHỈ trích dẫn.

custody-signing-service.consumes: [command, query] — §4a.6 (mới, v0.3) elaborate đầy đủ
idempotency/identity/correlation requirement cho SigningRequest (immutable identity,
một logical request xuyên retry, payload-digest binding, authorization-evidence
binding) — KHÔNG concrete ID format/database, KHÔNG mở rộng ngoài §4a.6.
```

## 12. Audit/provenance requirements (bắt buộc, yêu cầu task)

```text
account.md (Package 0.2-C2, Consolidated Stable) ĐÃ pin đầy đủ audit/provenance cho
Account entity — Package 1.2 CHỈ tổng hợp, KHÔNG author mới:
  mọi event là authoritative event record (Chapter 8 §8.2, Locked) — append-only, I-3
    No Repaint.
  correction lineage đầy đủ (account.md §11) — `AccountFactInvalidated` +
    `supersedes_fact_ref` trỏ TRỰC TIẾP predecessor, mười invariant chuẩn.
  `AccountCurrentView` KHÔNG BAO GIỜ authoritative — mọi audit/replay PHẢI dùng
    authoritative event stream TẠI cursor (account.md §7/§13).
  time semantics tách bạch effective_time/recorded_time (account.md §12) — historical
    replay dùng đúng metadata có hiệu lực TẠI computation cursor.

Cross-cutting audit requirement MỚI (elaboration, đúng phạm vi Package 1.2's baseline
checklist role):
  mọi module `trust_boundary_candidate`/`custody_adjacent`/`secret_consuming` (§3) PHẢI
    đảm bảo hành động của nó truy vết được về đúng evidence authoritative đã dùng (I-1
    Explainability, nguyên tắc chung — KHÔNG field/schema mới, chỉ áp dụng nguyên tắc đã
    Locked).
  credential/secret access (custody-signing-service, NAY registered VÀ elaborate đầy đủ,
    §4a.11) PHẢI có audit trail — I-11 Verification: "Access-control audit — xác nhận
    chỉ Exchange Adapter hoặc dedicated Custody/Signing Service được phép sử dụng
    credential trực tiếp." §4a.11 pin đầy đủ mười ba required audit category VÀ sáu mục
    PHẢI loại trừ (raw secret/private key/seed phrase/recovery secret/sensitive
    credential material/unredacted sensitive signed payload). Package 1.2 KHÔNG author
    audit LOG schema cụ thể (forbidden scope: database schema) — CHỈ pin YÊU CẦU audit
    trail phải tồn tại.
```

## 12a. Cross-cutting control matrix (MỚI v0.3, bắt buộc, yêu cầu task — cập nhật cho toàn bộ 25 module)

**Nguyên tắc bắt buộc:** ma trận dưới đây áp dụng class-neutral baseline (§3.1) cộng class-specific addition (§3.2) cho MỌI 25 module — KHÔNG ngụ ý mọi module cần rule riêng ngoài baseline chung; CHỈ bốn class có tên (`custody_adjacent`/`secret_consuming`/`trust_boundary_candidate`/`none`) nhận additional treatment như đã pin tại §3.2.

```text
Control area              | Áp dụng                                    | Nguồn
---------------------------|---------------------------------------------|------------------
Raw-secret access          | CHỈ custody-signing-service (§4a.2/§4a.7)   | I-11, ADR-017 §3.1
Credential-reference       | account-service (owns opaque reference);   | account.md §10,
  access                   | custody-signing-service (resolves nó)      | §4.2/§4a.3
Signing-request initiation | CHỈ future Exchange Adapter (§4a.7) hoặc    | ADR-017 §8.5,
                            | explicitly-approved administrative op       | §4a.7
Signed-material receipt    | CHỈ caller đã khởi tạo đúng SigningRequest  | §4a.6/§4a.7
                            | (correlation binding bắt buộc)              |
Venue transport             | CHỈ exchange-adapter (registered, chưa     | ADR-017 §3.2,
                            | functionally elaborate, §7)                  | §7
Business authorization      | Decision Authority Service (Decision/Trade | §4a.2, Package
                            | Intent); Risk Gateway (RiskEvaluation/     | 1.3-C/1.3-D
                            | Execution Intent) — custody/signing         |
                            | authority KHÔNG BAO GIỜ conflate            |
Audit visibility            | mọi module trust_boundary_candidate/       | §3.1 mục 7, §12,
                            | custody_adjacent/secret_consuming; đặc      | §4a.11
                            | biệt custody-signing-service (§4a.11)       |
Replay/backtest exclusion   | raw credential/signing material KHÔNG BAO  | §12b (mới)
                            | GIỜ vào replay/backtest dataset              |
Log/event/snapshot          | audit record loại trừ raw secret/private   | §4a.11, §12b
  redaction                | key/seed phrase/recovery secret/sensitive   |
                            | signed payload                              |
Plugin isolation            | strategy-plugin-host/decision-evaluation-  | §4a.7,
                            | engine KHÔNG được signing access trực tiếp  | forbidden_
                            | (forbidden_dependencies, §4a.1)             | dependencies
API/UI restrictions         | command-query-api-surface/ux-application-  | §4a.7,
                            | shell KHÔNG được signing access trực tiếp   | forbidden_
                            | (forbidden_dependencies, §4a.1)             | dependencies
Fail-closed behavior        | mọi module (§3.1 mục 8) — custody-signing- | §3.1, §4a.8,
                            | service's mười ba điều kiện cụ thể (§4a.8)  | §10
```

**Xác nhận tường minh:** ma trận trên KHÔNG author implementation/mechanism nào (network ACL cụ thể, database RBAC, log storage) — CHỈ pin YÊU CẦU kiểm soát ở mức architecture, khớp đúng forbidden scope (§13).

## 12b. Replay/backtest constraints (MỚI v0.3, bắt buộc, yêu cầu task)

```text
Raw credential, credential binding, signing request chứa sensitive material, signature,
VÀ signed payload KHÔNG BAO GIỜ được phép vào:
  market replay (Package 1.3-A, replay-integration-service);
  strategy replay;
  backtest dataset (backtest-orchestrator, DD-001);
  deterministic simulation snapshot (Paper Execution Boundary, Package 1.3-D);
  general analytical event stream;
  user-facing journal export.

Non-secret audit metadata (§4a.11 — request receipt/validation outcome/signing-attempt
outcome/rejection category/caller boundary evidence/Account Boundary-environment-venue
binding/payload-digest evidence) CÓ THỂ được retain CHỈ dưới explicit classification VÀ
redaction rule — Package 1.2 KHÔNG author classification/redaction mechanism cụ thể tại
đây (forbidden scope, database schema, §13) — CHỈ pin nguyên tắc: bất kỳ retention nào
PHẢI qua đúng classification, KHÔNG mặc định "audit nên giữ mọi thứ".

`replay-integration-service` (Chapter 8 §8.5 canonical Replay Cursor authority, Package
1.3-A) fold TOÀN BỘ authoritative fact (Decision→Position) — Package 1.2 xác nhận
custody-signing-service's SigningOutcome/SigningFailure (§4a.3) KHÔNG PHẢI một phần của
chuỗi authoritative fact đó (Decision→Position, KHÔNG bao gồm custody/signing operational
fact) — replay/backtest KHÔNG cần, và KHÔNG được, tái tạo signing operation.
```

## 13. Explicit non-goals

```text
KHÔNG author field-level event schema (đã khóa tại account.md, Package 0.2-C2,
  Consolidated Stable) — chỉ contract CATEGORY (event/query/command).
KHÔNG author authentication implementation cụ thể.
KHÔNG author custody implementation cụ thể (key management, HSM, v.v.).
KHÔNG chọn security vendor/tool.
KHÔNG author key storage implementation; HSM/vault selection; exchange API fields;
  signature algorithm; credential rotation protocol.
KHÔNG author database hay API schema.
KHÔNG chọn network topology hay cloud provider design.
KHÔNG author source code hay test.
KHÔNG resolve DD-003.
KHÔNG tự sửa `module-registry.yaml`/`system-decomposition.md` — `custody-signing-
  service`/`exchange-adapter` ĐÃ đăng ký bởi Package 1.1 correction transaction riêng
  (v0.5/v0.6, đã thực hiện) — Package 1.2 v0.3 CHỈ đề xuất elaboration/registry-alignment
  tương lai (§16a), KHÔNG tự thực hiện registry change nào tại transaction này.
KHÔNG tạo elaborating package mới cho `exchange-adapter` (§7/§14 — ngoài thẩm quyền
  Package 1.2).
KHÔNG chọn một authoritative kill-switch-state owner (§9/§4a.10).
KHÔNG reclassify `security_classification` của module nào (§3.0/§3.1 — Package 1.1
  authority, KHÔNG Package 1.2; class-neutral baseline áp dụng KHÔNG cần reclassify).
KHÔNG redefine module identity/taxonomy/dependency đã pin tại Package 1.1
  (module-registry.yaml/system-decomposition.md v0.6, Consolidated Stable).
KHÔNG redefine Package 1.3-A/1.3-B/1.3-C/1.3-D content (Consolidated Stable/review-clean).
KHÔNG tự thực hiện Package 1.1 alignment transaction (§16a — CHỈ SAU KHI Review A/B pass).
Deferred implementation scope (KHÔNG được trình bày như completed architecture, bắt buộc
  yêu cầu task): Vault/KMS/HSM vendor; cryptographic algorithm; key generation ceremony;
  credential import UX; physical storage topology; database implementation; network/
  service mesh; deployment topology; concrete RBAC product; rotation schedule; venue-
  specific signing details; SLA và timeout value cụ thể; full incident-response runbook.
KHÔNG tạo/approve ADR nào tại transaction này (§16 assessment — báo cáo nhu cầu, KHÔNG
  tự quyết).
KHÔNG mark Package 1.2 Consolidated Stable.
KHÔNG consolidate Package 1.3-D.
KHÔNG pass Gate 2.
KHÔNG tuyên bố Phase 1 hoàn thành.
KHÔNG mở Phase 2.
KHÔNG authorize Live.
```

## 14. Preserved unresolved gaps (KHÔNG resolve, chỉ carry forward — bắt buộc, yêu cầu task)

**Cập nhật v0.3 (đóng v0.2's ADR gate qua ADR-017 Approved — §15 viết lại):** Gap #1/#2/#3 của v0.2 (module registration, credential mechanism, signing-request pattern) NAY MỘT PHẦN RESOLVED — module registration VÀ signing-request pattern (Option C) ĐÃ quyết định qua ADR-017 v0.2 Approved; concrete credential mechanism (Vault/KMS binding) VẪN forbidden scope, KHÔNG resolve. Danh sách dưới đây thay thế hoàn toàn danh sách v0.2, phản ánh trạng thái sau ADR-017 + Package 1.1 v0.6 + §4a elaboration.

```text
1. Exchange Adapter functional elaboration VÀ elaborating package assignment — module
   ĐÃ registered (module-registry.yaml v0.6, `phase.elaborated_by: null`) NHƯNG KHÔNG
   package nào trong chín package Phase 1 hiện tại sở hữu chức năng của nó (§7). Escalation:
   Phase 1 amendment/package mới, Product Owner, ngoài phạm vi Package 1.2.

2. Future LIVE venue-submission Domain Contract — contract Execution Engine ↔ Exchange
   Adapter (ADR-017 §8.3, mười mục prerequisite) CHƯA author field-level; Package 1.2 v0.3
   KHÔNG author nó (§4a.12).

3. Execution Engine → Exchange Adapter activation (Stage 2, ADR-017 §9a) — Stage 1
   registration (ĐÃ xảy ra) KHÔNG tự kích hoạt; một future LIVE governance authorization
   riêng biệt là bắt buộc.

4. Raw venue-interaction evidence Domain Contract (ADR-017 §3.2a) — evidence identity/
   lifecycle/correction/idempotency/schema CHƯA author, prerequisite cho Exchange
   Adapter's future elaboration VÀ Execution Result Processor's future LIVE integration.

5. Kill-switch authoritative-state ownership — VẪN UNRESOLVED (§9/§4a.10), kế thừa
   nguyên vẹn Package 1.3-D §16 gap #4/ADR-017 §14 gap #2 — Package 1.2 KHÔNG silently
   claim cho custody-signing-service/exchange-adapter/account-service hay bất kỳ module
   nào khác.

6. Approved in-flight signing/submission behavior — kill-switch/revocation race với một
   SigningAttempt hay execution submission đang tiến hành CHƯA có safe rule Approved
   (§4a.9/§4a.10) — carry forward, KHÔNG tự phát minh rule.

7. Concrete signing correlation mechanism — correlation giữa execution submission
   request ↔ signing request ↔ signing attempt ↔ signing outcome ↔ future venue
   submission evidence (§4a.6) CHƯA thiết kế cụ thể — forbidden scope.

8. Concrete timeout/reconciliation mechanism — timing value, reconciliation protocol cho
   UNKNOWN_OUTCOME (§4a.9) CHƯA thiết kế — forbidden scope.

9. Vault/KMS/HSM implementation — credential-binding concrete mechanism (account.md
   §14/§16, ADR-012 §6, ADR-017 §14 gap #1) VẪN forbidden scope tại §4a/§6.

10. Credential rotation protocol VÀ signing algorithm — concrete mechanism CHƯA author
    (§4a/§13 forbidden scope).

11. DD-003 (PAPER-context authoritative Decision establishment mechanism) — hoàn toàn
    ngoài phạm vi Package 1.2, kế thừa từ Package 1.3-D, KHÔNG resolve.

12. Future LIVE governance authorization — quyết định riêng biệt, Product Owner, để thực
    sự AUTHORIZE LIVE execution (§8) — Package 1.2 v0.3 KHÔNG PHẢI quyết định đó.

13. PAPER-simulated vs LIVE-thật credential_reference isolation cụ thể — cấu trúc
    identity-level (environment field) đã tách biệt, NHƯNG chưa có ràng buộc runtime
    isolation tường minh nào ngoài đó (§8).

14. Broker Account Boundary Domain Contract riêng (account.md §14) — khi
    boundary_type=broker_account cần schema/field chi tiết hơn opaque reference — chưa
    cần cho walking skeleton hiện tại.

15. RBAC/Access Control Model cụ thể (OQ-001, Partially Resolved) — "single-operator now,
    multi-tenant-ready later" hướng đã xác nhận (ADR-007), NHƯNG RBAC cụ thể vẫn Open,
    liên quan Package 1.2 VÀ Package 1.5 (Database Architecture — retention); ảnh hưởng
    trực tiếp caller-authorization mechanism cụ thể cho custody-signing-service (§4a.7)
    — Package 1.2 KHÔNG đóng OQ-001 tại transaction này.

16. Audit log concrete schema/storage — YÊU CẦU pin tại §12/§4a.11, MECHANISM cụ thể
    (database schema, retention, classification/redaction rule §12b) deferred — liên
    quan Package 1.5.

17. Venue-adapter protocol chi tiết (kế thừa Package 1.3-D §16 gap #3) — chưa author bởi
    bất kỳ package Phase 1 nào tính đến transaction này.

18. Toàn bộ gap Package 1.3-D preserved (§16 của risk-execution-architecture.md v0.2) VÀ
    toàn bộ gap ADR-017 preserved (§14 ADR-017) VẪN là upstream/downstream context liên
    quan — Package 1.2 KHÔNG resolve gap nào trong số đó, CHỈ cung cấp phần
    custody-adjacent baseline mà Package 1.3-D consolidation condition yêu cầu.
```

## 15. ADR assessment — ADR gate RESOLVED (v0.3 — đóng bởi Approved ADR-017 v0.2)

**Xác nhận tường minh (v0.3, thay thế kết luận v0.2):** ADR decision requirement mà §15 (v0.2) ghi nhận ACTIVE NAY RESOLVED — [ADR-017](../adr/ADR-017.md) v0.2 (Approved, Product Owner, 2026-08-04T20:08:00+07:00) đã quyết định: "I approve ADR-017 v0.2 — Custody & Signing Trust Boundary — selecting Option C, the split Custody/Signing Service and Exchange Adapter architecture, as the current Approved architecture decision." Đối chiếu đủ tám mục §15.2 (dưới, giữ nguyên làm historical decision scope) với ADR-017's nội dung:

```text
1. Authoritative custody/signing boundary                RESOLVED — ADR-017 §7 (business
                                                          vs custody/signing vs transport,
                                                          KHÔNG conflate).
2. Registered module identity/architectural boundary      RESOLVED — custody-signing-
                                                          service + exchange-adapter,
                                                          ADR-017 §3.1/§3.2, registered
                                                          module-registry.yaml v0.5/v0.6.
3. Direct credential-use authority                        RESOLVED — custody-signing-
                                                          service, VÀ CHỈ nó (ADR-017
                                                          §3.1, §4a.2).
4. Credential-reference source-of-truth relationship      RESOLVED architecture-level —
                                                          custody-signing-service resolves
                                                          account-service's opaque
                                                          credential_reference (ADR-017
                                                          §3.1, §4a.3) — concrete Vault/
                                                          KMS binding VẪN forbidden scope
                                                          (§14 gap #9).
5. Published interaction boundary với Execution Engine     RESOLVED — Execution Engine →
                                                          Exchange Adapter, MỘT contract
                                                          boundary riêng biệt khỏi PAPER
                                                          (ADR-017 §8.1) — field-level
                                                          schema VẪN forbidden (§14 gap
                                                          #2).
6. Dependency-graph implications                           RESOLVED — custody-signing-
                                                          service.depends_on:
                                                          [account-service]; exchange-
                                                          adapter.depends_on: [custody-
                                                          signing-service]; execution-
                                                          engine → exchange-adapter KHÔNG
                                                          active (Stage 2, §14 gap #3).
7. Audit and provenance responsibility                     RESOLVED — custody-signing-
                                                          service authoritative cho audit
                                                          category (ADR-017 §12, §4a.11)
                                                          — concrete schema VẪN forbidden
                                                          (§14 gap #16).
8. Kill-switch observation/enforcement participation       RESOLVED participation-only —
                                                          exchange-adapter anticipated
                                                          I-8; custody-signing-service
                                                          selected bởi ADR-017 (§4a.10) —
                                                          state ownership VẪN unresolved
                                                          (§14 gap #5, KHÔNG resolve).
```

**Kết luận:** cả tám mục ADR decision scope ĐÃ resolve ở mức architecture-decision bởi ADR-017 v0.2 Approved — ADR gate (§16 "ADR gate condition") NAY THỎA. Package 1.2 v0.3 VẪN KHÔNG `Consolidated Stable` — điều kiện review CLEAN + Package 1.1 alignment transaction (§16a) VẪN ĐỘC LẬP, CHƯA thỏa (§16).

### 15.0 Lịch sử — nội dung §15 v0.2 gốc (GIỮ NGUYÊN làm historical record, KHÔNG reopen)

**Finding đóng (v0.2, lịch sử):** v0.1's kết luận "KHÔNG mục nào... bị kích hoạt... Package 1.2 KHÔNG tạo ADR" là SAI — tự mâu thuẫn với chính `phase-1-plan.md` đã được quote nguyên văn tại §0 ("Likely tạo ADR riêng cho security trust boundary + custody boundary — package 1.2 PHẢI dừng tại đúng boundary đó chờ ADR Approved trước khi tự Consolidated Stable"). Candidate v0.1 ĐÃ đi tới đúng ranh giới đó (nội dung §6/§7 elaborate đầy đủ YÊU CẦU nhưng dừng lại trước concrete mechanism) — nhưng §15 v0.1 lại tuyên bố ranh giới đó "không kích hoạt ADR", tức phủ nhận chính observation mà tài liệu tự đưa ra. Sửa (v0.2): ghi nhận yêu cầu ADR là ACTIVE ngay bây giờ, KHÔNG chờ tới "một transaction tương lai" mới ghi nhận.

```text
An ADR decision requirement is now active. (v0.2 — NAY RESOLVED tại v0.3, xem trên)

Package 1.2 may remain Draft and continue bounded review, but it must not become
Consolidated Stable until an Approved ADR resolves the security trust boundary and
custody/signing authority boundary sufficiently for the baseline being consolidated.
```

### 15.1 Vì sao yêu cầu ADR active (đánh giá lại sáu điều kiện gốc của ADR rule)

```text
Đúng ADR rule của task gốc: "a decision requirement... a new credential or signing
authority owner; a custody source of truth; a new venue-adapter authority; a new
PAPER/LIVE isolation model; an execution bypass; a dependency or topology absent from
approved authority."

new credential/signing authority owner:   ACTIVE — §7 xác nhận I-11 yêu cầu "CHỈ Exchange
  Adapter hoặc dedicated Custody/Signing Service được phép dùng credential trực tiếp"
  nhưng KHÔNG module nào giữ vai trò đó được đăng ký (§2). Baseline ĐANG được consolidate
  (§6 §7 §3.2 "future credential-using boundary") PHỤ THUỘC vào việc ai/module nào SẼ giữ
  vai trò authority đó — đây LÀ một quyết định chưa có, không phải một fact đã pin có thể
  chỉ "trích dẫn". Package 1.2 KHÔNG tự chọn owner đó (vẫn đúng, KHÔNG đổi) — NHƯNG việc
  baseline cần owner đó tồn tại để hoàn thiện chính nó LÀ điều kích hoạt ADR gate.
custody source of truth:                 ACTIVE — cùng lý do trên; §6 pin YÊU CẦU
  (credential_reference opaque, nguồn thật bên ngoài Domain Contract) nhưng "nguồn thật"
  cụ thể là gì (Vault/KMS/signing service nào, quan hệ với module nào) là quyết định
  authoritative-source-of-truth CHƯA có — điều kiện "custody source of truth" trigger.
new venue-adapter authority:              ACTIVE — cùng module gap tại §7; venue-adapter
  authority CHƯA established, baseline hiện tại chỉ carry forward "khi module đó tồn tại,
  các yêu cầu sau áp dụng" — bản thân việc CHƯA có authority này chặn baseline hoàn thiện
  phần venue-adapter interaction boundary với Execution Engine (§5).
new PAPER/LIVE isolation model:           KHÔNG active — §8 xác nhận isolation hiện tại
  (identity-level, environment field) đã đủ cho phạm vi hiện tại; Package 1.2 KHÔNG cần
  một isolation model mới cho phần này. KHÔNG kích hoạt ADR ở mục riêng này.
execution bypass:                         KHÔNG active — §5 xác nhận business/custody/
  transport authorization tách biệt, KHÔNG bypass nào được tạo. KHÔNG kích hoạt ADR ở
  mục riêng này.
dependency/topology ngoài Approved        KHÔNG active riêng lẻ — Package 1.2 KHÔNG tự
  authority:                              thêm dependency edge nào vào module-registry.yaml
                                           tại transaction này; NHƯNG dependency-graph
                                           implications của việc MỘT module custody mới
                                           (nếu/khi đăng ký) sẽ cần edge tới Execution
                                           Engine/Risk Gateway LÀ một phần của chính
                                           quyết định ADR nói trên (§15.2 mục 6) — ghi
                                           nhận như một phần của decision scope, KHÔNG
                                           như một trigger độc lập mới.

Kết luận: BA trong sáu điều kiện gốc (credential/signing authority owner, custody source
of truth, venue-adapter authority) đã đạt điểm cần quyết định — KHÔNG PHẢI vì Package 1.2
chọn resolve chúng (KHÔNG chọn, đúng nguyên tắc "does not choose among possible
solutions" — §15.3), mà vì baseline ĐÃ elaborate đủ sâu (§6/§7) để lộ ra rằng các phần đó
KHÔNG THỂ hoàn thiện/consolidate nếu thiếu một quyết định kiến trúc Approved. Đây chính
là ranh giới `phase-1-plan.md` đã tiên đoán — KHÔNG một tình huống mới.
```

### 15.2 ADR decision scope (mô tả ở architecture level — KHÔNG chọn giải pháp)

```text
1. Authoritative custody/signing boundary — ranh giới trust boundary chính xác giữa nơi
   business authorization kết thúc và custody/signing authorization bắt đầu.
2. Registered module identity, hoặc một architectural boundary khác đã được approve tường
   minh, cho vai trò "Exchange Adapter hoặc dedicated Custody/Signing Service" (I-11).
3. Direct credential-use authority — module/boundary nào (và CHỈ nó) được cấp quyền dùng
   exchange credential trực tiếp.
4. Credential-reference source-of-truth relationship — `account-service`'s
   `credential_reference` (opaque, §4/§6) quan hệ CHÍNH XÁC thế nào với nguồn thật giữ raw
   secret.
5. Published interaction boundary với Execution Engine — Execution Engine (Package 1.3-D)
   tương tác với custody/signing boundary đó qua contract nào, theo mô hình nào (§5).
6. Dependency-graph implications — module/boundary mới đó cần edge gì trong
   module-registry.yaml (thẩm quyền Package 1.1, KHÔNG Package 1.2).
7. Audit and provenance responsibility — ai chịu trách nhiệm audit trail cho credential
   access (§12 đã pin YÊU CẦU audit trail phải tồn tại; ADR quyết định AI thực hiện).
8. Kill-switch observation and enforcement participation scope — custody/signing boundary
   đó tham gia I-8 kill-switch scope thế nào (§7/§9 đã ghi nhận gap, KHÔNG resolve).
```

### 15.3 Xác nhận tường minh — candidate KHÔNG chọn giải pháp

```text
The candidate does not choose among possible solutions.

Package 1.2 v0.2 KHÔNG author: một ADR document; một module mới; một registry correction;
một dependency edge; một sản phẩm Vault hay HSM cụ thể; credential storage; signing
algorithm; network topology; API hay event schema. Tất cả tám mục tại §15.2 được MÔ TẢ ở
mức architecture-level (WHAT cần quyết định), KHÔNG đề xuất giải pháp nào trong số đó.
```

### 15.4 Pre-consolidation stop condition

```text
The gap is disclosed and intentionally unresolved.

Its unresolved status blocks Package 1.2 Consolidated Stable.

Avoiding a concrete mechanism does not remove the requirement for an Approved
architectural decision.
```

**Cập nhật v0.3:** ADR riêng đó ĐÃ xảy ra — [ADR-017](../adr/ADR-017.md) v0.2, Approved, Product Owner, 2026-08-04T20:08:00+07:00 — resolve đủ tám mục tại §15.2 (xem xác nhận tại đầu §15). Package 1.2 v0.3 KHÔNG tự tạo/approve ADR đó (đã Approved bởi transaction riêng biệt trước) — §13 non-goals cập nhật tương ứng. Package 1.2 v0.3 VẪN KHÔNG `Consolidated Stable` — điều kiện review CLEAN + Package 1.1 alignment (§16a) VẪN CHƯA thỏa.

## 16. Review and consolidation conditions (viết lại v0.3)

```text
Review A scope:               Baseline có bao phủ đủ I-4/I-7/I-11 Scope đã khai báo
                               (§3/§5/§6, đúng phase-1-plan.md); không vi phạm ADR-007
                               boundary (internal/crypto-only, §8); account-service
                               module boundary (§4) VÀ custody-signing-service module
                               boundary (§4a, MỚI) nhất quán với module-registry.yaml
                               v0.6 (Consolidated Stable, 25 module) — không silent
                               semantic invention, KHÔNG claim registry assignment chưa
                               tồn tại (§4a's phase.elaborated_by: null xác nhận đúng);
                               §7 xác nhận exchange-adapter registered NHƯNG functionally
                               unelaborated, KHÔNG package mới bị tự ý tạo; §15 ADR
                               assessment đúng — ADR gate RESOLVED đúng qua ADR-017 v0.2
                               Approved (KHÔNG under-claim, KHÔNG over-claim); §3.0/§3.1
                               xác nhận `security_classification: none` được diễn giải
                               đúng và class-neutral baseline áp dụng cho toàn bộ 25
                               module; §4a's credential-reference model/signing-request
                               lifecycle/fail-closed rules/audit categories KHÔNG author
                               field-level schema/implementation nào (forbidden scope
                               §13); mọi gap (§14) carry forward trung thực, KHÔNG resolve
                               ngầm.
Independent Review B
  scope:                      Độc lập kiểm tra checklist (§3/§4a/§5/§6/§9/§10) đủ để MỌI
                               package khác (1.3-A..D, 1.4, 1.5) tham chiếu được, không
                               mơ hồ — đúng phase-1-plan.md Independent Review B scope;
                               xác nhận KHÔNG business/custody/transport authorization
                               nào bị conflate (§5/§4a.2); xác nhận kill-switch state
                               ownership KHÔNG bị silently claimed (§9/§4a.10); xác nhận
                               PAPER/LIVE treatment (§8) không invent LIVE support mới,
                               custody-signing-service KHÔNG activate như một phần LIVE
                               path; xác nhận §4a's caller-authorization boundary (§4a.7)
                               KHÔNG tạo dependency lên Decision/Risk authority; xác nhận
                               §4a's fail-closed rules (§4a.8) KHÔNG leak raw-secret; xác
                               nhận không có execution-engine → exchange-adapter edge nào
                               được thêm/đề xuất active; xác nhận §16a's Package 1.1
                               alignment dependency được mô tả đúng (KHÔNG thực hiện
                               registry change tại v0.3).
Product Owner decision
  point:                      Sau Review A/B CLEAN cho baseline v0.3 VÀ sau khi Package
                               1.1 alignment transaction (§16a) hoàn tất VÀ required
                               consistency verification pass — CẢ BA điều kiện ĐỘC LẬP,
                               KHÔNG điều kiện nào tự đủ.
ADR gate condition:            RESOLVED (§15) — ADR-017 v0.2 Approved, 2026-08-04T20:08:00
                               +07:00. KHÔNG còn một điều kiện pending riêng — thay bằng
                               Package 1.1 alignment condition (§16a) dưới.
Consolidation condition:      Baseline checklist explicit, versioned, pinned; zero
                               unresolved Blocker/Major trên v0.3; ADR gate condition
                               THỎA (§15); Package 1.1 alignment (§16a) HOÀN TẤT — KHÔNG
                               Consolidated Stable nếu thiếu BẤT KỲ điều kiện nào trong
                               số này.
```

## 16a. Package 1.1 alignment dependency (MỚI v0.3, bắt buộc, yêu cầu task)

```text
Package 1.2 v0.3 CÓ THỂ trở thành review-clean (Review A CLEAN + Independent Review B
CLEAN) TRONG KHI `custody-signing-service.phase.elaborated_by` VẪN `null` tại
module-registry.yaml — review-clean đánh giá CHẤT LƯỢNG/ĐÚNG ĐẮN của candidate v0.3,
KHÔNG PHẢI registry assignment tự thân.

SAU KHI Package 1.2 v0.3 pass Review A VÀ Independent Review B (CLEAN, Blocker 0/Major
0), một Package 1.1 bounded alignment transaction RIÊNG BIỆT PHẢI thực hiện:

  custody-signing-service.phase.elaborated_by:  null → "1.2"

Transaction đó (ngoài phạm vi Package 1.2, thuộc thẩm quyền Package 1.1) PHẢI kèm theo
required consistency verification (script-check module-registry.yaml/system-
decomposition.md v0.6 → v0.7, cùng nguyên tắc bounded correction đã dùng cho v0.5→v0.6).

CHỈ SAU KHI alignment đó HOÀN TẤT VÀ verification PASS, Package 1.2 mới CÓ THỂ nhận
Product Owner consolidation decision (§16 Product Owner decision point).

Package 1.2 v0.3 KHÔNG tự thực hiện registry change nào tại transaction này (§13
non-goals) — §16a CHỈ ghi nhận dependency VÀ trình tự bắt buộc, KHÔNG thực hiện.
```

## 17. Lifecycle treatment (MỚI v0.3)

```text
Package 1.2:
  version: 0.4
  status: Draft
  package lifecycle/readiness: candidate
  not Consolidated Stable
  pending Review A verification (bounded correction v0.3 → v0.4)
  pending Independent Review B
  pending Package 1.1 alignment (§16a)
  pending Product Owner consolidation decision

Package 1.2 v0.2 VẪN là historical review-clean evidence cho phạm vi gốc của nó
  (account-service, ĐÚNG MỘT module registry-assigned) — v0.3 KHÔNG invalidate v0.2's
  review evidence cho phạm vi ĐÓ, CHỈ mở rộng phạm vi baseline sang custody-signing-
  service (đề xuất, CHƯA registry-assigned).
```
