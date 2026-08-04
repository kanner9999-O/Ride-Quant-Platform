---
id: security-custody-baseline
title: "Package 1.2 — Security & Custody Baseline"
version: "0.2"
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

**CANDIDATE — status: Draft, KHÔNG Consolidated Stable, KHÔNG Approved, ADR-GATED.** Package 1.2 v0.2 — bounded correction, đóng `P12-A-MAJ-01`/`P12-IRB-MAJ-01`/`P12-A-MAJ-02`/`P12-IRB-MAJ-02` trên candidate v0.1. Author dựa trên Package 1.1 `Consolidated Stable` (v0.4, xem §1) — theo `phase-1-plan.md` v0.4 (`Approved`) §"Package 1.2 — Security & Custody Baseline (cross-cutting)".

**Một ADR decision requirement NAY ACTIVE (§15).** Package 1.2 CÓ THỂ tiếp tục ở `Draft` và tiếp tục bounded review, NHƯNG KHÔNG được trở thành `Consolidated Stable` cho tới khi một ADR `Approved` resolve đủ security trust boundary và custody/signing authority boundary cho đúng phần baseline đang được consolidate. Correction này KHÔNG tự tạo/approve ADR đó — CHỈ ghi nhận yêu cầu và stop condition (§15/§16).

Chưa qua Review A/Independent Review B cho v0.2, chưa có Product Owner consolidation decision.

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

**Module inventory resolved (script-verified, module-registry.yaml v0.4):** ĐÚNG MỘT module có `phase.elaborated_by: "1.2"` — `account-service`. Package 1.2 do đó có HAI trách nhiệm tách biệt, cả hai đều nằm trong CHÍNH artifact này: (a) elaborate kiến trúc kỹ thuật của `account-service` (module DUY NHẤT được gán); (b) thiết lập trust boundary map/isolation checklist CHO các module class khác (`trust_boundary_candidate`, `custody_adjacent`) MÀ KHÔNG re-elaborate chức năng của chúng — các module đó (`market-data-ingestion`→1.3-A, `risk-gateway`/`execution-engine`→1.3-D, `command-query-api-surface`→1.4) đã/đang được elaborate CHỨC NĂNG bởi package riêng của chúng; Package 1.2 CHỈ thêm layer bảo mật/isolation YÊU CẦU áp dụng lên các module đó — KHÔNG redefine responsibility/dependency đã pin.

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
account.md v0.2 (Package 0.2-C2, Consolidated     controlling domain semantic authority
  Stable):                                          cho Account entity — Consolidated
                                                    Stable, KHÔNG redefine tại đây
module-registry.yaml v0.4 (Consolidated Stable):  module identity/taxonomy/dependency
                                                    authority — KHÔNG redefine tại đây
risk-execution-architecture.md v0.2 (Package      Package 1.3-D consumer của Package 1.2
  1.3-D, review-clean, consolidation blocked      baseline — consumed như một forward
  pending Package 1.2):                            reference, KHÔNG redefine
phase-1-plan.md v0.4 (Approved):                  Phase 1 work-breakdown/package-boundary
                                                    authority, nguồn CHÍNH của §0 scope
                                                    resolution
Package 1.2 (tài liệu này):                       technical elaboration authority ONLY,
                                                    cho account-service VÀ cross-cutting
                                                    trust boundary map/checklist
```

Package 1.2 KHÔNG redefine domain entity/event semantics, module identity/taxonomy, hay bất kỳ package đã Consolidated Stable nào — mọi nội dung dưới đây chỉ **elaborate** kiến trúc kỹ thuật trong ranh giới đã pin.

## 2. Module scope (một module elaborate đầy đủ, bốn module tham chiếu trust-boundary-only)

| module_id | module_type | owns_authoritative_state | depends_on | forbidden_dependencies | consumes | emits | security_classification | phase.elaborated_by |
|---|---|---|---|---|---|---|---|---|
| `account-service` | runtime_service | true | (none, root) | (none) | `command` | `event`, `query` | `custody_adjacent` | **`1.2`** |
| `market-data-ingestion` | runtime_service | true | `market-reference-service` | (none) | `query` | `event` | `trust_boundary_candidate` | `1.3-A` (tham chiếu §3 CHỈ) |
| `risk-gateway` | runtime_service | true | `decision-authority-service`, `account-service` | (none) | `event` | `event` | `trust_boundary_candidate` | `1.3-D` (tham chiếu §3 CHỈ) |
| `execution-engine` | runtime_service | true | `risk-gateway`, `paper-execution-boundary` | `strategy-engine`, `strategy-plugin-host`, `context-aggregator` | `event` | `event`, `command` | `trust_boundary_candidate` | `1.3-D` (tham chiếu §3 CHỈ) |
| `command-query-api-surface` | runtime_service | false | (16 module, xem §2 note) | (none) | `event`, `query`, `command` | `query`, `command` | `trust_boundary_candidate` | `1.4` (tham chiếu §3 CHỈ) |

**KHÔNG recreate/invent module (xác nhận tường minh, yêu cầu task):** module-registry.yaml v0.4 KHÔNG đăng ký bất kỳ module nào tên "Exchange Adapter", "Custody-Signing Service", "Vault", "KMS", hay tương đương — I-11's "Chỉ Exchange Adapter hoặc dedicated Custody/Signing Service được phép sử dụng exchange credential trực tiếp" tham chiếu một AUTHORITY CHƯA ĐƯỢC ĐĂNG KÝ trong 23-module inventory hiện tại. Package 1.2 KHÔNG tạo module này (xem §15 ADR assessment — thêm module MỚI với published boundary/responsibility riêng LÀ architecture change, ADR Required theo Chapter 9 §9.10 "thay đổi module dependency graph"). Carry forward §15 gap.

**19 module còn lại (`security_classification: none`, đóng `P12-A-MAJ-02`/`P12-IRB-MAJ-02`):** `none` nghĩa CHỈ là Package 1.1 KHÔNG gán classification đặc biệt nào cho module đó — KHÔNG PHẢI một affirmative security clearance, KHÔNG PHẢI bằng chứng "không có external interaction/không có sensitive evidence/không liên quan credential/không có nghĩa vụ bảo mật riêng/loại trừ vĩnh viễn khỏi trust-boundary review". 19 module này VẪN nằm ngoài phạm vi elaborate chức năng chi tiết VÀ ngoài phạm vi trust-boundary-map riêng của §3's ba lớp có tên (`trust_boundary_candidate`/`custody_adjacent`), NHƯNG KHÔNG được miễn trừ khỏi class-neutral minimum security baseline (§3.1) — mọi module trong 23-module inventory, không phân biệt classification, đều chịu baseline đó. Chi tiết đầy đủ: §3.0/§3.1.

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

### 3.1 Class-neutral minimum security baseline (áp dụng cho MỌI 23 module đã đăng ký, không phân biệt classification — mới, đóng `P12-A-MAJ-02`/`P12-IRB-MAJ-02`)

19 module `security_classification: none` VẪN nằm ngoài phạm vi elaborate chức năng chi tiết của Package 1.2 (không author lại architecture riêng cho từng module đó — đó là thẩm quyền package sở hữu chức năng của chúng), NHƯNG KHÔNG được miễn trừ khỏi baseline sau — baseline này áp dụng ĐỒNG NHẤT cho cả 23 module, kể cả `account-service` và bốn module `trust_boundary_candidate`:

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
Class: trust_boundary_candidate (4 module: market-data-ingestion, risk-gateway,
  execution-engine, command-query-api-surface)
  Baseline:  §3.1 (bắt buộc, không miễn trừ).
  Bổ sung:   module CÓ TIỀM NĂNG chạm external network boundary (venue connection,
    custody-adjacent execution surface, hoặc API ingress/egress) — nhận thêm boundary
    và ingress/egress scrutiny NGOÀI baseline chung — IDENTIFICATION ONLY tại package
    sở hữu chức năng (§2 note, đúng nguyên văn "identification only, no auth/isolation
    design (Package 1.2)" mà cả bốn module đều mang trong notes/elaboration của package
    sở hữu).
  Yêu cầu I-4/I-7 áp dụng:  I-4 Scope liệt kê tường minh "Strategy Engine, Decision
    Engine, Risk Gateway, Execution Engine" — mọi trade intent PHẢI qua Risk Gateway
    trước khi tới Execution Engine (ĐÃ script-verified tại Package 1.3-C/1.3-D, KHÔNG
    redefine tại đây). I-7 Scope "Mọi Plugin" — command-query-api-surface là routing/
    exposure layer (Package 1.1 notes: "KHÔNG business logic riêng"), PHẢI verify theo
    I-7 Verification bốn mục bổ sung cho hệ polyglot/distributed: network ACL check ·
    API authorization scope check · event schema compatibility check · command
    authorization check.
  Yêu cầu I-11 áp dụng:  market-data-ingestion (external venue connection) VÀ
    execution-engine (execution surface tương tác Paper Execution Boundary hiện tại,
    venue adapter thật tương lai) — CẢ HAI KHÔNG được cấp quyền đọc raw secret rộng
    hơn cần thiết trừ khi cùng trust boundary với Exchange Adapter/Custody-Signing
    Service (I-11 Prohibited behavior) — Exchange Adapter CHƯA tồn tại (§2), nên
    boundary CỤ THỂ CHƯA thể xác nhận, carry forward §15 (nay ADR-gated, KHÔNG chỉ một
    generic gap).
  Design status:  IDENTIFICATION ONLY — Package 1.2 KHÔNG design concrete auth
    mechanism/network ACL implementation cho bốn module này (forbidden scope).

Class: custody_adjacent (1 module: account-service)
  Baseline:  §3.1 (bắt buộc, không miễn trừ).
  Bổ sung:   module sở hữu identity/metadata GẦN custody nhưng KHÔNG sở hữu raw secret
    (account-service responsibilities, nguyên văn: "KHÔNG sở hữu credential/secret
    material (I-11)") — CHỈ opaque credential reference, KHÔNG raw-secret ownership.
  Yêu cầu I-11 áp dụng:  đầy đủ tại §6 dưới — account-service CHỈ giữ
    `credential_reference` (opaque), KHÔNG BAO GIỜ raw secret.
  Design status:  §4 dưới elaborate ĐẦY ĐỦ kiến trúc (module DUY NHẤT gán cho Package
    1.2) — bao gồm identification, KHÔNG bao gồm credential storage implementation.

Class: none (19 module còn lại, đóng P12-A-MAJ-02/P12-IRB-MAJ-02)
  Baseline:  §3.1 (bắt buộc, không miễn trừ — KHÔNG "no isolation requirement" như v0.1
    sai tuyên bố).
  Bổ sung:   KHÔNG bổ sung riêng ngoài §3.1 — 19 module này KHÔNG nhận boundary/
    ingress-egress scrutiny bổ sung của trust_boundary_candidate, KHÔNG nhận custody
    treatment của custody_adjacent, NHƯNG VẪN chịu đầy đủ chín mục §3.1.
  Design status:  KHÔNG elaborate chức năng chi tiết riêng tại Package 1.2 (thẩm quyền
    package sở hữu chức năng của từng module) — KHÔNG đồng nghĩa "không cần đánh giá
    baseline bảo mật nào" (sửa từ v0.1). Reassessment/reclassification khi thay đổi
    kết nối/privilege/exposure — §3.1 mục 9.

Class: future credential-using boundary (Exchange Adapter/Custody-Signing Service —
  CHƯA đăng ký, §2/§7)
  Baseline:  §3.1 (áp dụng khi/nếu module được đăng ký).
  Bổ sung:   direct-secret authority CHỈ được cấp SAU KHI có một ADR Approved (§15) VÀ
    module đó được registry-level established tại `module-registry.yaml` (thẩm quyền
    Package 1.1) — Package 1.2 KHÔNG tự cấp quyền này, KHÔNG tự đăng ký module, KHÔNG
    tự tạo ADR đó tại transaction này (§13/§15).
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

Venue acknowledgment (Exchange Adapter response, CHƯA tồn tại module) KHÁC execution
  observation (ExecutionResult/Fill, Package 1.3-D authority) — venue acknowledgment
  (nếu/khi venue thật được mô hình hóa) sẽ là MỘT input evidence cho execution
  observation, KHÔNG PHẢI observation tự thân.
```

## 6. Custody và signing isolation (I-11, bắt buộc, yêu cầu task)

```text
Credential/secret isolation (account.md §10, ADR-012 §2.4, I-11 nguyên văn):
  API key/secret/private key KHÔNG BAO GIỜ lưu dạng plaintext — bắt buộc qua Vault/KMS
  (concrete mechanism deferred, §15). Account Service CHỈ giữ `credential_reference` —
  opaque reference tới credential binding BÊN NGOÀI Domain Contract, TUYỆT ĐỐI KHÔNG
  raw secret dưới bất kỳ hình thức nào (payload/snapshot/log/replay artifact).

Signing requests vs signed payloads (I-11 phân biệt, elaboration):
  "sử dụng credential trực tiếp" (I-11 Required guarantees) KHÔNG nhất thiết nghĩa là
  đọc raw secret — I-11's Verification clause nguyên văn: "KMS/signing service có thể ký
  request mà KHÔNG BAO GIỜ trả secret cho caller." Một signing-request pattern (module
  gửi payload cần ký, nhận lại signature, KHÔNG BAO GIỜ thấy private key) là kiến trúc
  hợp lệ theo I-11 — Package 1.2 KHÔNG chọn pattern cụ thể (Mô hình A trực tiếp vs Mô
  hình B qua signing service — cùng nguyên tắc "hai mô hình hợp lệ, không hardcode"
  Chapter 9 §9.1 đã dùng cho Plugin artifact resolution) — carry forward §15.

Least-privilege access (I-11 Required guarantees, nguyên văn):
  "Execution Engine tương tác qua contract (gửi execution command), KHÔNG cần đọc raw
  secret TRỪ KHI được triển khai cùng trust boundary với Adapter." Execution Engine
  (Package 1.3-D) mặc định KHÔNG có quyền đọc raw secret — chỉ được cấp quyền đó nếu
  deployment manifest (Phase 1, CHƯA author) chứng minh cùng trust boundary với Exchange
  Adapter VÀ quyền đó đã phê duyệt rõ ràng (I-11 Verification).

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
                                            module nào (module-registry.yaml v0.4).
  Projection (Position Projection,        KHÔNG được cấp quyền — projection module
    Package 1.3-D):                        (owns_authoritative_state: false) không có
                                            business hay custody nào cần secret.
  General API (command-query-api-         KHÔNG được cấp quyền đọc raw secret — API
    surface, Package 1.4):                 surface là routing/exposure layer (module-
                                            registry.yaml notes), KHÔNG business logic
                                            riêng; account-service.depends_on rỗng
                                            (root) — command-query-api-surface chỉ
                                            tương tác qua published command/query
                                            contract (`credential_reference` opaque),
                                            KHÔNG raw secret nào lộ qua surface đó.

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

## 7. Venue-adapter/execution-boundary treatment (bắt buộc, yêu cầu task — KHÔNG invent module)

```text
Xác nhận tường minh (§2 trên): KHÔNG module "Exchange Adapter"/"Custody-Signing Service"
nào được đăng ký trong module-registry.yaml v0.4 — I-11's authority reference ("Chỉ
Exchange Adapter hoặc dedicated Custody/Signing Service") là một khái niệm Constitution
đã Locked NHƯNG CHƯA có module tương ứng trong 23-module inventory hiện tại.

Package 1.2 KHÔNG tạo module này (§15 ADR assessment — thêm module MỚI với published
boundary/responsibility riêng LÀ architecture change, Chapter 9 §9.10 "thay đổi module
dependency graph" → ADR Required, thuộc thẩm quyền Package 1.1, KHÔNG phải Package 1.2
authoring transaction này).

Khi module đó được đăng ký (Package 1.1 correction tương lai, ngoài phạm vi transaction
này), các yêu cầu SAU ĐÂY (đã established tại I-11/Chapter 9, KHÔNG invent) sẽ áp dụng
NGAY:
  module đó, VÀ CHỈ module đó, được phép sử dụng exchange credential trực tiếp (I-11);
  Execution Engine (Package 1.3-D) tương tác với module đó qua published contract
    (event/query/command, Chapter 9 §9.2) — KHÔNG gọi trực tiếp implementation nội bộ;
  I-8 Kill Switch Scope MỞ RỘNG bao gồm module đó ("Risk Gateway, Execution Engine, mọi
    Exchange Adapter") — Package 1.3-D §11 đã ghi nhận "Exchange Adapter CHƯA tồn tại...
    KHÔNG thể xác nhận observe boundary cho module đó" — Package 1.2 XÁC NHẬN LẠI gap
    này, KHÔNG resolve.
  I-11 Grant layer (Chapter 9 §9.6) áp dụng: permission GRANT (quyền THỰC SỰ được cấp)
    PHẢI versioned, KHÔNG suy từ declaration; Enforcement tại đúng runtime authority
    (module đó); Verification qua network ACL/API authorization scope/credential audit.
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
    "hoàn thiện" pipeline đó.
  Exchange Adapter/Custody-Signing Service module (§7 trên).

Prerequisite còn lại cho LIVE tương lai (carry forward, KHÔNG resolve tại đây):
  DD-003 (PAPER-context authoritative Decision establishment mechanism, Package 1.3-D
    §8.2/§16 — KHÔNG chạm Package 1.2, ngoài phạm vi hoàn toàn).
  Exchange Adapter/Custody-Signing Service registration (Package 1.1 correction, §7/§16).
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
Execution Engine, mọi Exchange Adapter") — Exchange Adapter PHẢI observe kill-switch khi
module đó tồn tại (§7 trên) — Package 1.2 CHỈ xác nhận yêu cầu SCOPE này, KHÔNG author
observation mechanism (CHƯA established, đúng Package 1.3-D §11).

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
    author cơ chế resolve cụ thể (§6, §15 gap: "cơ chế credential reference cụ thể...
    Phase 1 Security & Custody Baseline" — account.md §14/ADR-012 §6 đã defer chính XÁC
    tới đây, NHƯNG "defer tới đây" KHÔNG nghĩa là "author tại v0.1 candidate này" — carry
    forward, đúng forbidden scope "key storage implementation").
  Account current_status stale/unknown TẠI cursor — risk.md §5c bước 7 (Package 1.3-D,
    Consolidated Stable) ĐÃ pin: reconstruct TẠI cursor từ authoritative Account event
    stream, KHÔNG AccountCurrentView latest-state; nếu KHÔNG resolve được ACTIVE tường
    minh tại cursor đó → RiskEvaluation NON_EVALUABLE (risk.md §5c Branch A) — fail-closed
    ĐÃ hoạt động ở tầng domain hiện có.
  custody/venue boundary state version-mismatch (definition version pinning tương tự
    risk.md §5b3 bốn trục) — KHÔNG áp dụng trực tiếp cho account-service (account.md
    KHÔNG có "definition version" axis riêng cho credential — chỉ opaque reference); khi
    Exchange Adapter/Custody-Signing Service được đăng ký (§7), version-mismatch fail-
    safe cho MODULE đó sẽ cần elaborate riêng — carry forward §15.

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
  mọi module `trust_boundary_candidate`/`custody_adjacent` (§3) PHẢI đảm bảo hành động
    của nó truy vết được về đúng evidence authoritative đã dùng (I-1 Explainability,
    nguyên tắc chung — KHÔNG field/schema mới, chỉ áp dụng nguyên tắc đã Locked).
  credential/secret access (khi Exchange Adapter/Custody-Signing Service tồn tại, §7)
    PHẢI có audit trail — I-11 Verification: "Access-control audit — xác nhận chỉ
    Exchange Adapter hoặc dedicated Custody/Signing Service được phép sử dụng credential
    trực tiếp." Package 1.2 KHÔNG author audit LOG schema cụ thể (forbidden scope:
    database schema) — CHỈ pin YÊU CẦU audit trail phải tồn tại.
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
KHÔNG tạo module "Exchange Adapter"/"Custody-Signing Service" mới trong
  module-registry.yaml — đó là Package 1.1 correction transaction riêng, thuộc diện ADR
  Required (Chapter 9 §9.10).
KHÔNG chọn một authoritative kill-switch-state owner (§9).
KHÔNG reclassify `security_classification` của module nào (§3.0/§3.1 — Package 1.1
  authority, KHÔNG Package 1.2; class-neutral baseline áp dụng KHÔNG cần reclassify).
KHÔNG redefine module identity/taxonomy/dependency đã pin tại Package 1.1
  (module-registry.yaml/system-decomposition.md v0.4, Consolidated Stable).
KHÔNG redefine Package 1.3-A/1.3-B/1.3-C/1.3-D content (Consolidated Stable/review-clean).
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

**Bounded correction note (đóng `P12-A-MAJ-01`/`P12-IRB-MAJ-01`):** Gap #1, #2, #3 dưới đây KHÔNG còn là generic "chờ tương lai" gap — chúng CÙNG cấu thành đúng ranh giới ADR decision requirement NAY ACTIVE tại §15. Gap được disclosed và intentionally unresolved; trạng thái unresolved đó CHẶN Package 1.2 `Consolidated Stable` (§15.4/§16) cho tới khi một ADR Approved resolve §15.2. Tránh chọn một concrete mechanism KHÔNG loại bỏ yêu cầu phải có một Approved architectural decision.

```text
1. Exchange Adapter/Custody-Signing Service module registration — KHÔNG tồn tại trong
   module-registry.yaml v0.4 (§2/§7). Đăng ký module này là một phần của ADR decision
   scope §15.2 (mục 2/3/6) — thuộc diện ADR Required (Chapter 9 §9.10, "thay đổi module
   dependency graph"/"thêm plugin type/capability mới" nếu module đó có
   plugin_relation). **Pre-consolidation ADR gate — xem §15.**

2. Credential reference concrete mechanism (Vault/KMS binding, signing service
   integration) — account.md §14/§16 VÀ ADR-012 §6 đều tường minh defer TỚI "Phase 1
   Security & Custody Baseline" — Package 1.2 v0.2 elaborate YÊU CẦU (§6) nhưng KHÔNG
   chọn mechanism cụ thể (forbidden scope). Nguồn thật (§15.2 mục 4) KHÔNG thể pin cho
   tới khi ADR đó Approved. **Pre-consolidation ADR gate — xem §15.**

3. Signing-request pattern lựa chọn cụ thể (Mô hình A trực tiếp vs Mô hình B qua signing
   service, §6) — hai mô hình đều hợp lệ theo I-11, KHÔNG chọn tại đây; lựa chọn cụ thể
   phụ thuộc vào chính custody/signing authority owner (§15.2 mục 1/3) — **cùng
   pre-consolidation ADR gate, xem §15.**

4. Kill-switch state ownership/representation/lifecycle/observation/in-flight handling
   — kế thừa NGUYÊN VẸN từ Package 1.3-D §16 gap #4, KHÔNG mở rộng/resolve tại Package
   1.2 (§9).

5. PAPER-simulated vs LIVE-thật credential_reference isolation cụ thể — cấu trúc
   identity-level (environment field) đã tách biệt, NHƯNG chưa có ràng buộc runtime
   isolation tường minh nào ngoài đó (§8).

6. Broker Account Boundary Domain Contract riêng (account.md §14) — khi
   boundary_type=broker_account cần schema/field chi tiết hơn opaque reference — chưa
   cần cho walking skeleton hiện tại.

7. DD-003 (PAPER-context authoritative Decision establishment mechanism) — hoàn toàn
   ngoài phạm vi Package 1.2, kế thừa từ Package 1.3-D, KHÔNG resolve.

8. RBAC/Access Control Model cụ thể (OQ-001, Partially Resolved) — "single-operator now,
   multi-tenant-ready later" hướng đã xác nhận (ADR-007), NHƯNG RBAC cụ thể vẫn Open,
   liên quan Package 1.2 VÀ Package 1.5 (Database Architecture — retention) — Package
   1.2 KHÔNG đóng OQ-001 tại transaction này.

9. Audit log concrete schema/storage — YÊU CẦU pin tại §12, MECHANISM cụ thể (database
   schema, retention) deferred — liên quan Package 1.5.

10. Venue-adapter protocol chi tiết (kế thừa Package 1.3-D §16 gap #3) — chưa author bởi
    bất kỳ package Phase 1 nào tính đến transaction này.

11. Toàn bộ gap Package 1.3-D preserved (§16 của risk-execution-architecture.md v0.2) VẪN
    là upstream/downstream context liên quan — Package 1.2 KHÔNG resolve gap nào trong
    số đó, CHỈ cung cấp phần custody-adjacent baseline mà Package 1.3-D consolidation
    condition yêu cầu.
```

## 15. ADR assessment — ADR decision requirement ACTIVE (bounded correction, đóng `P12-A-MAJ-01`/`P12-IRB-MAJ-01`)

**Finding đóng:** v0.1's kết luận "KHÔNG mục nào... bị kích hoạt... Package 1.2 KHÔNG tạo ADR" là SAI — tự mâu thuẫn với chính `phase-1-plan.md` đã được quote nguyên văn tại §0 ("Likely tạo ADR riêng cho security trust boundary + custody boundary — package 1.2 PHẢI dừng tại đúng boundary đó chờ ADR Approved trước khi tự Consolidated Stable"). Candidate v0.1 ĐÃ đi tới đúng ranh giới đó (nội dung §6/§7 elaborate đầy đủ YÊU CẦU nhưng dừng lại trước concrete mechanism) — nhưng §15 v0.1 lại tuyên bố ranh giới đó "không kích hoạt ADR", tức phủ nhận chính observation mà tài liệu tự đưa ra. Sửa: ghi nhận yêu cầu ADR là ACTIVE ngay bây giờ, KHÔNG chờ tới "một transaction tương lai" mới ghi nhận.

```text
An ADR decision requirement is now active.

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

**KHÔNG tạo ADR tại transaction này (§13 non-goals không đổi).** Một transaction ADR riêng, Product Owner-authorized, PHẢI resolve tám mục tại §15.2 trước khi Package 1.2 được xem xét `Consolidated Stable`. Correction NÀY chỉ ghi nhận yêu cầu và stop condition — KHÔNG resolve.

## 16. Review and consolidation conditions

```text
Review A scope:               Baseline có bao phủ đủ I-4/I-7/I-11 Scope đã khai báo
                               (§3/§5/§6, đúng phase-1-plan.md); không vi phạm ADR-007
                               boundary (internal/crypto-only, §8); account-service
                               module boundary (§4) nhất quán với module-registry.yaml
                               v0.4 (Consolidated Stable) — không silent semantic
                               invention; §7 xác nhận KHÔNG module mới được tạo; §15 ADR
                               assessment đúng — ADR decision requirement được ghi nhận
                               ACTIVE đúng chỗ (KHÔNG under-claim như v0.1, KHÔNG
                               over-claim bằng cách tự resolve nó); §3.0/§3.1 xác nhận
                               `security_classification: none` được diễn giải đúng
                               (absence of classification, KHÔNG affirmative clearance)
                               và class-neutral baseline áp dụng cho toàn bộ 23 module;
                               mọi gap (§14) carry forward trung thực, gap #1/#2/#3 gắn
                               đúng với ADR gate.
Independent Review B
  scope:                      Độc lập kiểm tra checklist (§3/§6/§9/§10) đủ để MỌI package
                               khác (1.3-A..D, 1.4, 1.5) tham chiếu được, không mơ hồ —
                               đúng phase-1-plan.md Independent Review B scope; xác nhận
                               KHÔNG business/custody/transport authorization nào bị
                               conflate (§5); xác nhận kill-switch state ownership KHÔNG
                               bị silently claimed (§9); xác nhận PAPER/LIVE treatment
                               (§8) không invent LIVE support mới; xác nhận §15 KHÔNG tự
                               chọn giải pháp nào trong tám mục ADR decision scope
                               (§15.2/§15.3); xác nhận §3.1 chín-mục baseline KHÔNG author
                               mechanism/implementation nào (chỉ architecture-level
                               requirement).
Product Owner decision
  point:                      Sau Review A/B CLEAN cho baseline v0.2 (chưa cần đợi mọi
                               package khác dùng xong checklist, đúng phase-1-plan.md) —
                               VÀ sau khi ADR gate (§15/§15.4) đã Approved cho đúng phần
                               liên quan (xem Consolidation condition dưới).
ADR gate condition (mới,      Package 1.2 KHÔNG được `Consolidated Stable` cho tới khi
  đóng P12-A-MAJ-01/           một ADR riêng, Product Owner-authorized, Approved, resolve
  P12-IRB-MAJ-01):             đủ tám mục tại §15.2 (authoritative custody/signing
                               boundary; registered module identity hoặc boundary khác đã
                               approve; direct credential-use authority; credential-
                               reference source-of-truth relationship; published
                               interaction boundary với Execution Engine; dependency-graph
                               implications; audit/provenance responsibility; kill-switch
                               observation/enforcement participation scope) cho ĐÚNG phần
                               baseline đang được consolidate. Bounded review A/B CLEAN
                               trên v0.2 KHÔNG tự nó thỏa điều kiện này — hai điều kiện
                               (review CLEAN + ADR Approved) ĐỘC LẬP, cả hai PHẢI thỏa.
Consolidation condition:      Baseline checklist explicit, versioned, pinned; zero
                               unresolved Blocker/Major trên v0.2; ADR gate condition trên
                               đã thỏa (Approved) cho đúng phần baseline đã pin — KHÔNG
                               Consolidated Stable nếu thiếu MỘT trong hai.
```
