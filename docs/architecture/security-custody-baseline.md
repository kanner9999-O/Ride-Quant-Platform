---
id: security-custody-baseline
title: "Package 1.2 — Security & Custody Baseline"
version: "0.1"
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

**CANDIDATE — status: Draft, KHÔNG Consolidated Stable, KHÔNG Approved.** Package 1.2 v0.1 là candidate đầu tiên, author dựa trên Package 1.1 `Consolidated Stable` (v0.4, xem §1) — theo `phase-1-plan.md` v0.4 (`Approved`) §"Package 1.2 — Security & Custody Baseline (cross-cutting)". Chưa qua Review A/Independent Review B, chưa có Product Owner consolidation decision.

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

**KHÔNG recreate/invent module (xác nhận tường minh, yêu cầu task):** module-registry.yaml v0.4 KHÔNG đăng ký bất kỳ module nào tên "Exchange Adapter", "Custody-Signing Service", "Vault", "KMS", hay tương đương — I-11's "Chỉ Exchange Adapter hoặc dedicated Custody/Signing Service được phép sử dụng exchange credential trực tiếp" tham chiếu một AUTHORITY CHƯA ĐƯỢC ĐĂNG KÝ trong 23-module inventory hiện tại. Package 1.2 KHÔNG tạo module này (xem §16 ADR assessment — thêm module MỚI với published boundary/responsibility riêng LÀ architecture change, ADR Required theo Chapter 9 §9.10 "thay đổi module dependency graph"). Carry forward §15 gap.

**19 module còn lại (`security_classification: none`):** KHÔNG thuộc phạm vi trust boundary treatment của Package 1.2 — không cần isolation requirement bổ sung ngoài baseline platform-wide (I-4/I-7 scope chung).

## 3. Trust boundary map — theo module class (bắt buộc, yêu cầu task, KHÔNG re-elaborate chức năng module khác)

**Nguyên tắc bắt buộc:** mục này định nghĩa YÊU CẦU security/isolation ÁP DỤNG LÊN mỗi `security_classification`, KHÔNG redefine responsibility/dependency/authority đã pin tại Package 1.1/1.3-A/1.3-D/1.4. Package sở hữu chức năng của từng module (1.3-A/1.3-D/1.4) VẪN là authority cho chính module đó — Package 1.2 CHỈ thêm layer bảo mật.

```text
Class: trust_boundary_candidate (4 module: market-data-ingestion, risk-gateway,
  execution-engine, command-query-api-surface)
  Ý nghĩa:  module CÓ TIỀM NĂNG chạm external network boundary (venue connection,
    custody-adjacent execution surface, hoặc API ingress/egress) — IDENTIFICATION ONLY
    tại package sở hữu chức năng (§2 note, đúng nguyên văn "identification only, no
    auth/isolation design (Package 1.2)" mà cả bốn module đều mang trong notes/
    elaboration của package sở hữu).
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
    boundary CỤ THỂ CHƯA thể xác nhận, carry forward §15.
  Design status:  IDENTIFICATION ONLY — Package 1.2 KHÔNG design concrete auth
    mechanism/network ACL implementation cho bốn module này (forbidden scope).

Class: custody_adjacent (1 module: account-service)
  Ý nghĩa:  module sở hữu identity/metadata GẦN custody nhưng KHÔNG sở hữu raw secret
    (account-service responsibilities, nguyên văn: "KHÔNG sở hữu credential/secret
    material (I-11)").
  Yêu cầu I-11 áp dụng:  đầy đủ tại §6 dưới — account-service CHỈ giữ
    `credential_reference` (opaque), KHÔNG BAO GIỜ raw secret.
  Design status:  §4 dưới elaborate ĐẦY ĐỦ kiến trúc (module DUY NHẤT gán cho Package
    1.2) — bao gồm identification, KHÔNG bao gồm credential storage implementation.

Class: none (19 module còn lại)
  Ý nghĩa:  KHÔNG chạm external network boundary trực tiếp, KHÔNG sở hữu credential/
    secret material — baseline platform-wide I-4/I-7 vẫn áp dụng NHƯNG KHÔNG cần
    isolation requirement bổ sung riêng.
  Design status:  KHÔNG elaborate riêng tại Package 1.2 — I-4/I-7 baseline chung đã đủ.
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

Package 1.2 KHÔNG tạo module này (§16 ADR assessment — thêm module MỚI với published
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

```text
1. Exchange Adapter/Custody-Signing Service module registration — KHÔNG tồn tại trong
   module-registry.yaml v0.4 (§2/§7). Đăng ký module này là Package 1.1 correction
   transaction, thuộc diện ADR Required (Chapter 9 §9.10, "thay đổi module dependency
   graph"/"thêm plugin type/capability mới" nếu module đó có plugin_relation).

2. Credential reference concrete mechanism (Vault/KMS binding, signing service
   integration) — account.md §14/§16 VÀ ADR-012 §6 đều tường minh defer TỚI "Phase 1
   Security & Custody Baseline" — Package 1.2 v0.1 elaborate YÊU CẦU (§6) nhưng KHÔNG
   chọn mechanism cụ thể (forbidden scope) — carry forward cho version tương lai của
   CHÍNH artifact này hoặc một correction.

3. Signing-request pattern lựa chọn cụ thể (Mô hình A trực tiếp vs Mô hình B qua signing
   service, §6) — hai mô hình đều hợp lệ theo I-11, KHÔNG chọn tại đây.

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

## 15. ADR assessment (bắt buộc, yêu cầu task — báo cáo, KHÔNG tự quyết)

```text
Đúng ADR rule của task: "Stop and report a decision requirement only if Package 1.2
genuinely needs to select: a new credential or signing authority owner; a custody
source of truth; a new venue-adapter authority; a new PAPER/LIVE isolation model; an
execution bypass; a dependency or topology absent from approved authority."

Đánh giá TỪNG mục:
  new credential/signing authority owner:  Package 1.2 KHÔNG chọn — §6/§7 xác nhận
    Exchange Adapter/Custody-Signing Service CHƯA đăng ký, Package 1.2 KHÔNG tự đăng ký
    module đó (đó là Package 1.1 scope). KHÔNG kích hoạt ADR tại transaction NÀY.
  custody source of truth:  Package 1.2 KHÔNG chọn — §6 pin YÊU CẦU (credential_reference
    opaque, Vault/KMS bên ngoài), KHÔNG chọn hệ thống cụ thể nào làm source of truth.
    KHÔNG kích hoạt ADR.
  new venue-adapter authority:  cùng lý do "credential/signing authority owner" — KHÔNG
    kích hoạt.
  new PAPER/LIVE isolation model:  §8 xác nhận isolation HIỆN TẠI (identity-level,
    environment field) đã đủ cho phạm vi Package 1.2 — KHÔNG author isolation model mới.
    KHÔNG kích hoạt ADR.
  execution bypass:  KHÔNG — §5 xác nhận business/custody/transport authorization TÁCH
    BIỆT, KHÔNG bypass nào được tạo ra. KHÔNG kích hoạt ADR.
  dependency/topology ngoài Approved authority:  KHÔNG — Package 1.2 KHÔNG thêm dependency
    edge nào vào module-registry.yaml (account-service.depends_on giữ nguyên rỗng),
    KHÔNG chọn runtime topology. KHÔNG kích hoạt ADR.

Kết luận: KHÔNG mục nào trong sáu mục trên bị kích hoạt tại transaction v0.1 này — Package
1.2 KHÔNG tạo ADR. Đúng `phase-1-plan.md`'s dự đoán riêng ("Likely tạo ADR riêng cho
security trust boundary + custody boundary") — bản CANDIDATE v0.1 này CHƯA tới điểm cần
quyết định đó, vì nó CHƯA chọn concrete mechanism nào (đúng forbidden scope). ADR khả năng
sẽ cần thiết tại một transaction TƯƠNG LAI, KHI Package 1.2 (hoặc Package 1.1) thực sự
tiến tới đăng ký Exchange Adapter/Custody-Signing Service module HOẶC chọn concrete
credential mechanism — CẢ HAI đều KHÔNG xảy ra tại v0.1 này.
```

## 16. Review and consolidation conditions

```text
Review A scope:               Baseline có bao phủ đủ I-4/I-7/I-11 Scope đã khai báo
                               (§3/§5/§6, đúng phase-1-plan.md); không vi phạm ADR-007
                               boundary (internal/crypto-only, §8); account-service
                               module boundary (§4) nhất quán với module-registry.yaml
                               v0.4 (Consolidated Stable) — không silent semantic
                               invention; §7 xác nhận KHÔNG module mới được tạo; §15 ADR
                               assessment đúng — không mục nào bị silently kích hoạt hay
                               silently bỏ qua; mọi gap (§14) carry forward trung thực.
Independent Review B
  scope:                      Độc lập kiểm tra checklist (§3/§6/§9/§10) đủ để MỌI package
                               khác (1.3-A..D, 1.4, 1.5) tham chiếu được, không mơ hồ —
                               đúng phase-1-plan.md Independent Review B scope; xác nhận
                               KHÔNG business/custody/transport authorization nào bị
                               conflate (§5); xác nhận kill-switch state ownership KHÔNG
                               bị silently claimed (§9); xác nhận PAPER/LIVE treatment
                               (§8) không invent LIVE support mới.
Product Owner decision
  point:                      Sau Review A/B CLEAN cho baseline (chưa cần đợi mọi package
                               khác dùng xong checklist, đúng phase-1-plan.md).
Consolidation condition:      Baseline checklist explicit, versioned, pinned; zero
                               unresolved Blocker/Major; ADR liên quan (nếu có, §15 —
                               CHƯA phát sinh tại v0.1) Approved cho đúng phần baseline
                               đã pin.
```
