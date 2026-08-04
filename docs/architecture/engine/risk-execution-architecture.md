---
id: risk-execution-architecture
title: "Package 1.3-D — Risk Gateway & Execution Engine Architecture"
version: "0.1"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-04"
last_review: null
next_review: null
depends_on: ["00-governance", "02-platform-invariants", "03-engineering-principles", "04-domain-principles", "05-time-model", "06-identity-model", "07-module-taxonomy", "08-event-model", "13-quality-gates", "14-roadmap"]
---

# Package 1.3-D — Risk Gateway & Execution Engine Architecture

**CANDIDATE — status: Draft, KHÔNG Consolidated Stable, KHÔNG Approved.** Package 1.3-D v0.1 là candidate đầu tiên, author dựa trên Package 1.1 `Consolidated Stable` (v0.4), Package 1.3-A `Consolidated Stable`, Package 1.3-B `Consolidated Stable`, và Package 1.3-C `Consolidated Stable` (xem §1), theo [`phase-1-plan.md`](../phase-1-plan.md) v0.4 (`Approved`) §8 Package 1.3-D block. Chưa qua Review A/Independent Review B, chưa có Product Owner consolidation decision.

## 0. Vai trò của tài liệu này

Package 1.3-D elaborate **kiến trúc kỹ thuật** cho SÁU module ĐÃ được Package 1.1 (`Consolidated Stable`, [`module-registry.yaml`](../module-registry.yaml) v0.4 blob `6c4daa3eda3ef560b201de516dd019564d264c08`, [`system-decomposition.md`](../system-decomposition.md) v0.4 blob `8e60b9e6051956cfbe83f33e1c82f404bc082e37`) gán `phase.elaborated_by: "1.3-D"`: `risk-gateway`, `execution-engine`, `execution-result-processor`, `fill-processor`, `position-projection`, `paper-execution-boundary`. Tài liệu này **KHÔNG redefine** module identity/taxonomy/dependency đã pin ở Package 1.1, **KHÔNG redefine** Domain Contract semantics đã pin ở `risk.md`/`execution-intent.md`/`order.md`/`execution-result.md`/`fill.md`/`position.md`, và **KHÔNG redefine** Package 1.3-C's Decision authority model — chỉ elaborate: responsibility boundary chi tiết, mandatory non-bypass flow (Decision Authority Service → Risk Gateway → Execution Engine → Position), PAPER execution boundary, kill-switch/idempotency mapping, determinism/replay/no-repaint treatment, và open gap — đúng phạm vi `phase-1-plan.md` §8 Package 1.3-D "Purpose: Kiến trúc kỹ thuật cho Risk Gateway (Trade Intent → Risk Evaluation → Execution Intent) và Execution Engine (→ Order → ExecutionResult → Fill → Position)".

**Xác nhận tường minh (yêu cầu task — "Do not repeat the Package 1.3-C omission pattern"):** toàn bộ `module-registry.yaml` v0.4 đã được quét cho `phase.elaborated_by: "1.3-D"` (§2 dưới, script-verified) — SÁU module tìm thấy, TẤT CẢ đều elaborate tại tài liệu này. Không module nào bị bỏ sót.

**KHÔNG thuộc phạm vi tài liệu này:** field-level event schema (đã khóa tại sáu Domain Contract trên, Package 0.2-C5/C6/C7, `Consolidated Stable`); Risk Policy formula/sizing algorithm; venue adapter protocol; custody implementation; database schema; deployment/runtime topology cụ thể; Package 1.1/1.3-A/1.3-B/1.3-C content (KHÔNG redefine, `Consolidated Stable`).

## 1. Governing authority

```text
Constitution (Chapter 0–14, Locked):              highest architectural authority, đặc biệt
                                                    I-6 (Fail-Safe by Scope), I-8 (Kill
                                                    Switch), I-9 (Numerical Precision), I-10
                                                    (Idempotent Execution Effect), I-11
                                                    (Secrets & Custody Isolation)
Approved ADR-009 (ordering):                      per-stream sequence + explicit causation,
                                                    KHÔNG global total order
Approved ADR-012 (Account-to-Boundary              exactly-one-boundary Account, Position
  Cardinality):                                    scope dưới Account Boundary (§2.5)
Approved ADR-015/ADR-016 (module dependency         controlling cho 23-module inventory,
  graph, Candidate B/split):                       KHÔNG chạm bởi Package 1.3-D
Domain Contract (risk.md v0.3, execution-intent.md controlling domain semantic authority —
  v0.2, order.md v0.2, execution-result.md v0.3,   Consolidated Stable, KHÔNG redefine tại đây
  fill.md v0.3, position.md v0.3 — Package
  0.2-C5/C6/C7, Consolidated Stable):
module-registry.yaml v0.4 (Consolidated Stable):  module identity/taxonomy/dependency
                                                    authority — KHÔNG redefine tại đây
system-decomposition.md v0.4 (Consolidated        official Phase 1 module dependency graph
  Stable):                                         — KHÔNG redefine tại đây
strategy-decision-architecture.md v0.2 (Package    Decision Authority Service sole authority
  1.3-C, Consolidated Stable):                     boundary — consumed UNCHANGED (§10)
phase-1-plan.md v0.4 (Approved):                  Phase 1 work-breakdown/package-boundary
                                                    authority
Package 1.2 baseline (custody-adjacent boundary,  KHÔNG tồn tại tại transaction này (không
  I-11):                                            có `docs/architecture/*` file cho Package
                                                    1.2) — required TRƯỚC KHI Package 1.3-D tự
                                                    Consolidated Stable (phase-1-plan.md §8),
                                                    KHÔNG bắt buộc trước khi authoring bắt đầu
                                                    — ghi nhận gap tường minh (§16)
Package 1.3-D (tài liệu này):                     technical elaboration authority ONLY, cho
                                                    đúng sáu module trong scope
```

Package 1.3-D KHÔNG redefine domain entity/event semantics, module identity/taxonomy, hay Package 1.3-C's Decision authority nào — mọi nội dung dưới đây chỉ **elaborate** kiến trúc kỹ thuật trong ranh giới đã pin.

## 2. Module scope (sáu module, pin nguyên trạng từ Package 1.1 v0.4)

Sáu module dưới đây trích dẫn NGUYÊN VĂN `module-registry.yaml` v0.4 (identity/taxonomy/dependency KHÔNG đổi) — cột "Elaboration" là nội dung MỚI của tài liệu này:

| module_id | module_type | owns_authoritative_state | depends_on | forbidden_dependencies | consumes | emits | plugin_relation | security_classification |
|---|---|---|---|---|---|---|---|---|
| `risk-gateway` | runtime_service | true | `decision-authority-service`, `account-service` | (none) | `event` | `event` | none | `trust_boundary_candidate` |
| `execution-engine` | runtime_service | true | `risk-gateway`, `paper-execution-boundary` | `strategy-engine`, `strategy-plugin-host`, `context-aggregator` | `event` | `event`, `command` | none | `trust_boundary_candidate` |
| `execution-result-processor` | runtime_service | true | `execution-engine`, `paper-execution-boundary` | (none) | `event` | `event` | none | none |
| `fill-processor` | runtime_service | true | `execution-result-processor` | (none) | `event` | `event` | none | none |
| `position-projection` | projection | false | `fill-processor` | (none) | `event` | `query` | none | none |
| `paper-execution-boundary` | runtime_service | false | (none, root) | (none) | `command` | `event` | none | none |

**KHÔNG recreate module đã bị xóa/chưa đăng ký (xác nhận tường minh, yêu cầu task):** không có module `position-ledger` nào tồn tại trong `module-registry.yaml` v0.4 — module đã đăng ký là `position-projection` (§9 dưới làm rõ terminology). Tài liệu này KHÔNG tạo/giả định một module `position-ledger` riêng biệt.

**Module tham chiếu, KHÔNG elaborate đầy đủ tại đây (out of scope cho Package 1.3-D theo đúng `phase.elaborated_by`):** `decision-authority-service` (Package 1.3-C, `Consolidated Stable`, KHÔNG redefine); `account-service` (Package 1.2, chưa elaborate); `strategy-engine`/`strategy-plugin-host`/`context-aggregator` (Package 1.3-B/C, forbidden dependencies cho `execution-engine`, KHÔNG chạm).

**Quan sát minh bạch (KHÔNG thuộc phạm vi sửa của Package 1.3-D):** `replay-integration-service` (`module-registry.yaml` v0.4) có `depends_on: [decision-authority-service, risk-gateway, execution-engine, execution-result-processor, fill-processor, position-projection]` — phụ thuộc trực tiếp VÀO năm trong sáu module Package 1.3-D — nhưng `phase.elaborated_by: "1.3-A"` (KHÔNG `"1.3-D"`), và Package 1.3-A đã `Consolidated Stable` (`structure-regime-architecture.md` v0.1) mà KHÔNG elaborate `replay-integration-service` (chỉ elaborate bốn module Data Ingestion/Structure/Regime). Đây là một khoảng trống elaboration tương tự pattern `P13C-IRB-MAJ-01` đã đóng cho `plugin-release-manager` — NHƯNG thuộc phạm vi Package 1.3-A (đã Consolidated Stable, KHÔNG được sửa bởi Package 1.3-D theo đúng "Do not modify Package 1.1 or Package 1.3-A/B/C semantics"). Ghi nhận minh bạch tại §16, KHÔNG tự ý elaborate module thuộc package khác.

## 3. Mandatory non-bypass flow (KHÔNG runtime topology)

```text
Decision Authority Service (Package 1.3-C, Consolidated Stable)
      │  authoritative Decision / Trade Intent
      ▼
Risk Gateway (runtime_service — sole RiskEvaluation + Execution Intent authority)
      │  Risk Evaluation (APPROVED/REJECTED/NON_EVALUABLE)
      │  approved Execution Intent ONLY (result = APPROVED)
      ▼
Execution Engine (runtime_service — sole Order identity authority)
      │  Order (CREATED) → OrderSubmissionRequested (target_environment: PAPER)
      ▼
Paper Execution Boundary (runtime_service, non-authoritative boundary surface)
      │  bounded PAPER simulation trigger/output
      ▼
Execution Result Processor (runtime_service — sole ExecutionResultComputation/
                             PaperExecutionObservation/ExecutionResult authority)
      │  ExecutionResult (EXECUTED → Fill kỳ vọng; NOT_EXECUTED → zero Fill)
      ▼
Fill Processor (runtime_service — sole Fill authority)
      │  Fill (authoritative, immutable economics)
      ▼
Position Projection (projection, non-authoritative — derived TRỌN VẸN từ Fill)
```

**PAPER boundary (bắt buộc, yêu cầu task — KHÔNG được bypass Risk Gateway hay Decision Authority Service):**

```text
authoritative Decision (Decision Authority Service, Package 1.3-C)
      ▼
Risk Gateway (MANDATORY — mọi Trade Intent PHẢI qua đây trước bất kỳ execution path nào)
      ▼
Paper Execution Boundary (CHỈ reachable qua Execution Engine, KHÔNG có đường tắt)
```

**Xác nhận tường minh (yêu cầu task):** đây là responsibility/mandatory-ordering view — KHÔNG phải authorization triển khai một synchronous pipeline hay runtime topology cụ thể (process/container/host, đồng bộ/bất đồng bộ, message broker). Package 1.3-D KHÔNG chọn cơ chế thực thi cụ thể.

**PAPER-only xác nhận (v0.1/v0.2 toàn bộ sáu Domain Contract, KHÔNG suy diễn thêm):** `environment: [PAPER]` là giá trị enum ĐÓNG DUY NHẤT trên `Order`/`PaperExecutionObservation`/`ExecutionResult`/`Fill`/`Position` (order.md §1, execution-result.md §1/§6/§8, fill.md §1, position.md §1) — Domain Contract hiện tại KHÔNG mô hình hóa LIVE execution path nào. Đây là lý do PAPER Execution Boundary hiện là đường execution DUY NHẤT được author — KHÔNG phải một trong nhiều lựa chọn.

## 4. Module boundary — Risk Gateway

**Trách nhiệm (Package 1.1, KHÔNG đổi):** "Sở hữu RiskEvaluation identity (bốn trục risk evidence độc lập) và Execution Intent identity." + "Risk Policy logic (exposure limit, approve/reject, risk-increasing detection, kill switch) — LÀ business logic hợp lệ của đúng responsibility này (Chapter 7 §7.3), KHÔNG phải secondary taxonomy type/hybrid."

### 4.1 Mandatory gate (bắt buộc, yêu cầu task)

```text
Risk Gateway LÀ ranh giới BẮT BUỘC giữa authoritative Decision/Trade Intent và MỌI execution
path. KHÔNG module nào khác trong Package 1.3-D có `depends_on` trỏ TRỰC TIẾP tới
decision-authority-service (§10 script-check) — execution-engine/execution-result-processor/
fill-processor/position-projection/paper-execution-boundary ĐỀU KHÔNG có edge tới
decision-authority-service, chỉ risk-gateway có edge đó (§2).

Risk Gateway được phép (yêu cầu task):
  consume CHỈ authoritative Decision/Trade Intent output từ decision-authority-service
    (depends_on §2 — module-level connectivity; risk.md §5a mục 1 xác nhận trade_evidence
    resolve từ trade-intent.md/decision.md TẠI risk_context_cursor, KHÔNG evaluation
    proposal, KHÔNG raw plugin output);
  resolve applicable Account/Risk Policy reference ĐÃ authorized bởi controlling contract
    (account_id qua trade_evidence, risk.md §5b; risk_policy_definition_version_ref/
    risk_policy_configuration_version_ref — bốn trục risk evidence, risk.md §5b3 — Package
    1.3-D KHÔNG author policy VALUE cụ thể, chỉ pin resolution boundary);
  thực hiện deterministic Risk evaluation (risk.md §5c — mười ba bước thuật toán ĐÃ khóa,
    KHÔNG author lại tại đây — Package 1.3-D CHỈ trích dẫn architecture-level flow, xem
    §4.3 dưới);
  sinh authoritative RiskEvaluation record NƠI ĐÃ established (risk.md §1/§5 —
    RiskEvaluationRecorded, event_class tiêu chuẩn, KHÔNG event_class: decision);
  issue Execution Intent CHỈ SAU một Risk outcome APPROVED (execution-intent.md §3
    invariant: causation_refs PHẢI trỏ chính xác RiskEvaluationRecorded APPROVED — §4.4
    dưới);
  preserve provenance/cursor/policy version/causal ancestry (risk_context_cursor —
    canonical Replay Cursor, Chapter 8 §8.5.1, TÁI SỬ DỤNG nguyên vẹn; causation_refs
    một-chiều Attempt→RiskEvaluation, risk.md §5).
```

### 4.2 Preserved boundary (bắt buộc, yêu cầu task — KHÔNG được vi phạm)

```text
Risk Gateway KHÔNG được:
  tiêu thụ raw plugin output — risk.md §5b's trade_evidence resolve từ Trade Intent/
    Decision (authoritative), KHÔNG từ strategy-plugin-host output; risk-gateway KHÔNG có
    depends_on edge tới strategy-plugin-host (§2).
  tiêu thụ một Decision Evaluation proposal — risk-gateway.depends_on CHỈ chứa
    decision-authority-service (§2) — KHÔNG decision-evaluation-engine (non-authoritative,
    Package 1.3-C §6). Notes gốc (module-registry.yaml, nguyên văn): "Risk Gateway
    consumes authoritative Decision output từ `decision-authority-service` (ADR-016 v0.8)
    — KHÔNG trực tiếp từ `decision-evaluation-engine` (non-authoritative)."
  tạo hay đổi Decision identity — decision_id authority thuộc DUY NHẤT decision-authority-
    service (Package 1.3-C §7.2); Risk Gateway CHỈ tham chiếu Decision qua Trade Intent
    (trade-intent.md, `originating_decision_id`), KHÔNG BAO GIỜ mutate.
  thực thi Strategy hay Plugin logic — ngoài phạm vi hoàn toàn (Package 1.3-B/C).
  route venue order trực tiếp trừ khi registry tường minh gán vai trò đó — `module-
    registry.yaml` v0.4 KHÔNG gán venue-routing responsibility cho risk-gateway; venue/
    execution surface thuộc execution-engine/paper-execution-boundary (§6/§8).
  bypass Account hay custody-adjacent constraint — risk-gateway.depends_on chứa
    account-service (§2); risk.md §5c bước 7 xác nhận `account_id.current_status(cursor)
    == ACTIVE` là một domain-gate check bắt buộc (REJECTED/ACCOUNT_NOT_ACTIVE nếu fail).
  approve dựa trên input stale/missing/version-mismatched — risk.md §5b2/§5c bước 4
    (Branch A — Availability failure) VÀ bước 5 (Branch B — Compatibility failure) BẮT
    BUỘC NON_EVALUABLE khi evidence không AVAILABLE hoặc unit/currency mismatch — KHÔNG
    approve được dưới điều kiện đó (§4.3 dưới).
  âm thầm biến một Risk REJECTED outcome thành Execution Intent — execution-intent.md §3
    invariant tường minh: "RiskEvaluation `result = REJECTED`/`QUANTITY_ROUNDS_TO_ZERO`
    KHÔNG BAO GIỜ có `approved_quantity`, do đó KHÔNG BAO GIỜ có thể làm `causation_refs`
    hợp lệ cho ExecutionIntentIssued — chỉ `result = APPROVED` mới hợp lệ làm nguồn."
```

### 4.3 Deterministic Risk evaluation — architecture-level flow (KHÔNG author formula, yêu cầu task)

```text
risk.md §5c pin THUẬT TOÁN mười ba bước (validate eligibility → resolve bốn trục risk
evidence → resolve evidence_facts/unit_evidence → Branch A availability-gate → Branch B
compatibility-gate → numeric domain validation → Account ACTIVE check → ... → sizing →
positive-quantity floor-round). Package 1.3-D KHÔNG author lại thuật toán này (forbidden
scope: "author Risk formulas or sizing algorithms") — CHỈ xác nhận architecture-level flow
tồn tại DUY NHẤT bên trong ranh giới module risk-gateway, KHÔNG rò rỉ ra module khác
(Chapter 3 §3.1 responsibility ownership).

Tuyên bố tường minh (bắt buộc, yêu cầu task):
  KHÔNG authoritative Decision  → KHÔNG Risk evaluation (risk.md §5a mục 1 —
                                    eligible_for_new_risk_evaluation == false → attempt
                                    INELIGIBLE, KHÔNG RiskEvaluationRecorded nào phát).
  KHÔNG approved Risk outcome   → KHÔNG Execution Intent (execution-intent.md §3 — nguồn
                                    DUY NHẤT hợp lệ là result = APPROVED).
  KHÔNG Execution Intent         → KHÔNG execution attempt (§6 dưới — execution-engine
                                    KHÔNG có input nào khác để tạo Order).
```

## 4a. Execution Intent authority/lifecycle boundary (thuộc Risk Gateway, elaboration riêng theo yêu cầu task)

**Xác nhận sở hữu:** Execution Intent identity thuộc DUY NHẤT `risk-gateway` (module-registry.yaml v0.4 §2 responsibilities: "...và Execution Intent identity") — KHÔNG module riêng nào khác trong `module-registry.yaml` sở hữu Execution Intent. Đây là elaboration của MỘT phần trách nhiệm risk-gateway đã pin, KHÔNG một module mới.

```text
Ai tạo Execution Intent identity:  Risk Gateway, DUY NHẤT — execution_intent_id opaque,
  globally unique, gán tại ExecutionIntentIssued (execution-intent.md §1/§3).

RiskEvaluation nào Execution Intent PHẢI tham chiếu:  ĐÚNG MỘT, result = APPROVED
  (originating_risk_evaluation_id, execution-intent.md §1 invariant — causation_refs
  PHẢI trỏ chính xác RiskEvaluationRecorded APPROVED đó).

Một Risk approval → zero hay một Execution Intent:  execution-intent.md §1/§10 —
  `originating_risk_evaluation_id` là UNIQUE KEY trên MỌI ExecutionIntentIssued VALID —
  tại một cursor, tối đa MỘT ExecutionIntentIssued VALID cho mỗi RiskEvaluation APPROVED
  (`execution_intent_derivation_idempotency_policy:
  ONE_VALID_INTENT_PER_ORIGINATING_RISK_EVALUATION`). "Zero" xảy ra khi RiskEvaluation
  APPROVED tồn tại NHƯNG issuance CHƯA/KHÔNG xảy ra (recoverable append gap, §12 dưới) —
  KHÔNG phải một quy tắc cấm; "một" là cardinality tối đa khi issuance đã xảy ra.

Idempotency/duplicate-prevention boundary:  same origin (`originating_risk_evaluation_id`)
  + same payload → idempotent, trả về `execution_intent_id` đã tồn tại; same origin +
  payload KHÁC → deterministic conflict, reject (execution-intent.md §1/§10). KHÔNG
  unstated cross-stream atomicity — RiskEvaluation và Execution Intent là hai authoritative
  stream RIÊNG (§12 dưới).

Correction/cancellation behavior:  ExecutionIntentIssued — invalidate-only, KHÔNG same-ID
  replacement (scope hoàn toàn bất biến — một Execution Intent sai nghĩa là "RiskEvaluation
  này không nên tạo Execution Intent," KHÔNG "sửa nội dung," execution-intent.md §5/§8).
  Lifecycle status (ISSUED/WITHDRAWN/EXPIRED) dùng correction lineage chuẩn same-slice
  replacement, `supersedes_fact_ref` có mặt ngay từ v0.1 (execution-intent.md §4/§5/§8).

Recorded-time/effective-time eligibility:  `ExecutionIntentIssued.effective_time >=
  originating RiskEvaluationRecorded.risk_evaluation_time` (KHÔNG BAO GIỜ effective TRƯỚC
  RiskEvaluation gốc); `recorded_time > originating RiskEvaluationRecorded.recorded_time`
  (strict causal ordering, execution-intent.md §3/§9). `eligible_for_new_order_creation`
  (execution-intent.md §6a) — năm điều kiện transitive (Execution Intent ISSUED,
  RiskEvaluation gốc visible-valid-head VÀ APPROVED, đúng risk_evaluation_id tham chiếu,
  cùng trade_intent_id, VÀ `eligible_for_new_risk_evaluation` true) — Execution Engine
  (§6 dưới) PHẢI kiểm tra rule này TRƯỚC Order creation mới, KHÔNG chỉ dựa
  current_status = ISSUED cục bộ.
```

**Xác nhận tường minh (yêu cầu task — "Do not invent field-level schemas or new lifecycle states"):** mục này KHÔNG author schema mới — mọi field/invariant trích dẫn nguyên văn `execution-intent.md`. KHÔNG state mới ngoài UNSEEN/ISSUED/WITHDRAWN/EXPIRED đã khóa.

## 5. Module boundary — Execution Engine

**Trách nhiệm (Package 1.1, KHÔNG đổi):** "Sở hữu Order identity (bất biến), OrderCreationAttempt, OrderSubmissionRequest."

### 5.1 Responsibilities (elaboration)

```text
Execution Engine được phép (yêu cầu task):
  tiêu thụ CHỈ eligible authoritative Execution Intent — order.md §4a mục 1:
    eligible_for_new_order_creation(originating_execution_intent_id, order_context_cursor)
    == true (execution-intent.md §6a) PHẢI true TRƯỚC KHI Order Engine chạy bounded
    computation; false → attempt INELIGIBLE, KHÔNG OrderCreated nào phát.
  thực hiện idempotent execution orchestration — order_creation_attempt_id TÁCH BIỆT khỏi
    logical creation key (originating_execution_intent_id); idempotency scoped theo TỪNG
    attempt (order.md §3/§11 `order_creation_attempt_idempotency_policy`), logical key
    scoped theo `order_creation_derivation_idempotency_policy:
    ONE_VALID_ORDER_PER_ORIGINATING_EXECUTION_INTENT`.
  tạo Order identity NƠI ĐÃ established — order_id opaque, globally unique, gán tại
    OrderCreated (order.md §1/§4), quantity COPY CHÍNH XÁC approved_quantity gốc, KHÔNG
    resize/clamp/round (order.md §1 invariant).
  tương tác với ranh giới venue/custody-adjacent adapter ĐÃ khai báo — v0.1/v0.2 CHỈ ranh
    giới đó là Paper Execution Boundary (§8 dưới, `execution-engine.depends_on` chứa
    `paper-execution-boundary`, §2); KHÔNG venue adapter thật nào được author (forbidden
    scope).
  ghi nhận Execution Result — KHÔNG, xác nhận CHÍNH XÁC: Execution Engine KHÔNG sở hữu
    ExecutionResult identity (đó là `execution-result-processor`, §6 dưới) — Execution
    Engine CHỈ sở hữu Order/OrderSubmissionRequest, là input contract-boundary cho
    execution-result-processor (execution-engine.depends_on KHÔNG bao gồm cross-ownership
    nào của ExecutionResult).
  preserve causation từ Execution Intent xuyên Order tới kết quả — causation_refs
    OrderCreated PHẢI chứa OrderCreationAttemptRecorded tương ứng (một chiều, order.md §4);
    OrderSubmissionRequested.causation_refs PHẢI chứa OrderCreated tương ứng (order.md §6).
```

**Xác nhận CHÍNH XÁC (làm rõ nội dung task's "record Execution Result"):** trách nhiệm ghi nhận `ExecutionResult`/`PaperExecutionObservation` KHÔNG thuộc `execution-engine` — thuộc DUY NHẤT `execution-result-processor` (§6 dưới, module-registry.yaml v0.4 §2 responsibilities: "Sở hữu ExecutionResult identity"). Execution Engine's ranh giới kết thúc tại `OrderSubmissionRequested` — event handoff tới Paper Execution Boundary (§8), KHÔNG tự nó ghi execution result.

### 5.2 Preserved boundary (bắt buộc, yêu cầu task — KHÔNG được vi phạm)

```text
Execution Engine KHÔNG được:
  tiêu thụ raw Decision/plugin output làm execution authorization — forbidden_dependencies
    chứa strategy-engine/strategy-plugin-host/context-aggregator (§2, module-registry.yaml
    v0.4) — KHÔNG đường nào tới các module đó.
  thực hiện Risk approval — risk-gateway (§4) SOLE authority; execution-engine.depends_on
    chứa risk-gateway (§2) CHỈ để consume approved Execution Intent, KHÔNG để tự đánh giá
    Risk.
  đổi Decision/RiskEvaluation/Execution Intent authority — order.md §1 invariant: mọi
    field origin (originating_risk_evaluation_id/trade_intent_id/account_id/
    instrument_selection_ref/direction/quantity/quantity_unit) PHẢI BẰNG HỆT origin chain
    của Execution Intent gốc — Order KHÔNG được tự chọn khác.
  âm thầm retry KHÔNG có stable idempotency identity — order.md §3 invariant: idempotency
    scoped theo TỪNG order_creation_attempt_id, retry cùng attempt + cùng payload →
    idempotent no-op, retry cùng attempt + payload khác → deterministic conflict, reject.
  coi transport acknowledgment là một Fill — Execution Engine KHÔNG sở hữu Fill identity
    (đó là fill-processor, §7 dưới); OrderSubmissionRequested (order.md §6) tường minh
    "KHÔNG chứng minh boundary đã accept, venue đã acknowledge, external order ID tồn
    tại, execution đã xảy ra, hay Fill tồn tại — thuần túy internal handoff fact."
  derive Position authority trực tiếp không qua Fill/ledger rule — Execution Engine KHÔNG
    có depends_on edge nào tới position-projection (§2) — KHÔNG đường architecture nào để
    làm việc này.
  bypass kill-switch hay execution-suspension control — §11 dưới (Risk Gateway sở hữu
    kill-switch policy, module-registry.yaml v0.4 responsibilities) — Execution Engine
    PHẢI quan sát trạng thái đó trước khi tạo execution attempt mới (§11 mapping, cơ chế
    quan sát cụ thể CHƯA established — gap, §16).
```

## 6. Module boundary — Execution Result Processor

**Trách nhiệm (Package 1.1, KHÔNG đổi):** "Sở hữu ExecutionResult identity — observation trả về từ bounded PAPER execution boundary." + "ExecutionResultProcessingAttempt."

### 6.1 Authoritative ownership (elaboration)

```text
Execution Result Processor sở hữu authoritative:
  ExecutionResultComputation (execution-result.md §2) — identity đại diện ĐÚNG MỘT
    authorized computation lifecycle (INITIAL hoặc CORRECTION), quyết định authorization
    VÀ idempotency — KHÔNG cursor.
  PaperExecutionObservation (execution-result.md §1) — bản ghi DURABLE của MỘT lần bounded
    PAPER simulation computation, gắn CHÍNH XÁC một ExecutionResultComputation.
  ExecutionResultProcessingAttempt (execution-result.md §3) — mọi lần thử xử lý, kể cả
    INELIGIBLE/FAILED_BEFORE_RESULT.
  ExecutionResult (execution-result.md §8) — `result_type` COPY CHÍNH XÁC từ Observation
    visible-valid, KHÔNG BAO GIỜ tự computation/reinterpret.

Execution Result Processor KHÔNG sở hữu:
  Order/OrderSubmissionRequest identity (execution-engine, §5).
  Fill identity (fill-processor, §7).
  simulation algorithm THẬT (forbidden scope — Package 1.3-D KHÔNG author).
```

### 6.2 Paper Execution Boundary handoff (elaboration — quan hệ với §8)

```text
execution-result-processor.depends_on chứa CẢ execution-engine LẪN paper-execution-
boundary (§2) — hai input riêng biệt: execution-engine cung cấp OrderSubmissionRequested
(context cho eligibility, order.md §8b eligible_for_execution_result_processing);
paper-execution-boundary cung cấp bounded PAPER simulation trigger/output MÀ Execution
Result Processor consume để tạo PaperExecutionObservation. Paper Execution Boundary
KHÔNG tự sở hữu Observation/ExecutionResult (§8 dưới xác nhận owns_authoritative_state:
false cho chính module đó) — Execution Result Processor mới là authoritative owner.
```

### 6.3 Preserved boundary (bắt buộc, đúng nguyên tắc chung — KHÔNG được vi phạm)

```text
Execution Result Processor KHÔNG được:
  tự computation/reinterpret result_type — CHỈ copy nguyên vẹn từ PaperExecutionObservation
    visible-valid (execution-result.md §8 invariant — "TUYỆT ĐỐI KHÔNG tự tính lại/
    reinterpret").
  ghi ExecutionResultRecorded trước khi computation hoàn tất trọn vẹn — thứ tự bắt buộc:
    authorize → computation hoàn tất → Observation ghi → Attempt PROCESSED ghi →
    ExecutionResultRecorded ghi (execution-result.md §8a, KHÔNG BAO GIỜ đảo ngược).
  tạo hai ExecutionResultComputation(INITIAL) cho cùng submission_request_id — logical
    INITIAL key = submission_request_id, tối đa MỘT (execution-result.md §2).
  bypass Risk/Decision authority — execution-result-processor.depends_on KHÔNG chứa
    risk-gateway/decision-authority-service (§2) — KHÔNG đường architecture nào tồn tại.
```

## 7. Module boundary — Fill Processor

**Trách nhiệm (Package 1.1, KHÔNG đổi):** "Sở hữu Fill identity (bất biến) — quantity/price đã executed cho ExecutionResult result_type=EXECUTED."

```text
Fill Processor sở hữu authoritative:
  FillRecorded/FillFactInvalidated (fill.md §1/§3/§4) — economics (fill_quantity/
  fill_price/price_currency/quantity_unit) PHẢI copy CHÍNH XÁC từ PaperExecutionObservation
  (qua ExecutionResult.execution_observation_id, fill.md §1 invariant) — Fill Processor
  KHÔNG BAO GIỜ độc lập quan sát/tính toán economics.

Fill Processor KHÔNG sở hữu:
  ExecutionResult/PaperExecutionObservation identity (execution-result-processor, §6).
  Position semantics (position-projection, §9 — hoàn toàn ngoài phạm vi Fill, fill.md §12
    prohibition).
  processing Attempt riêng — fill.md tường minh: "Fill KHÔNG có processing Attempt riêng
    — derivation từ ExecutionResultRecorded(EXECUTED) là deterministic trực tiếp" (§1
    module-registry.yaml không liệt kê FillProcessingAttempt nào).

depends_on CHỈ execution-result-processor (§2) — Fill Processor KHÔNG có đường nào tới
  Risk Gateway/Execution Engine/Paper Execution Boundary trực tiếp; mọi input đến qua
  ExecutionResultRecorded(EXECUTED) DUY NHẤT.

full-Fill boundary (v0.1/v0.2, disclosed judgment call, fill.md §13): result_type=EXECUTED
  LUÔN sản sinh CHÍNH XÁC MỘT full Fill — KHÔNG partial-fill semantics author tại C7/
  Package 1.3-D.
```

## 8. Module boundary — Paper Execution Boundary

**Trách nhiệm (Package 1.1, KHÔNG đổi):** "Bounded PAPER execution boundary mà OrderSubmissionRequest/ExecutionResult tham chiếu — chưa chứng minh venue acceptance/execution thật."

### 8.1 Execution-mode boundary, KHÔNG Decision hay Risk authority (bắt buộc, yêu cầu task)

```text
Paper Execution Boundary PRESERVE như một execution-MODE boundary — KHÔNG một Decision
hay Risk authority thay thế. owns_authoritative_state: false (§2, module-registry.yaml
v0.4) — module NÀY không sở hữu bất kỳ authoritative fact nào; Observation/
ExecutionResult (§6) và Fill (§7) đều thuộc module KHÁC downstream. Paper Execution
Boundary là ĐIỂM CHẠM/consumes: command, emits: event — surface tiếp nhận
OrderSubmissionRequested-driven trigger và phát sinh raw simulation output MÀ Execution
Result Processor (§6) consume để tạo authoritative fact.

Paper Execution Boundary KHÔNG được (bắt buộc, yêu cầu task):
  tạo authoritative Decision — depends_on: (none, root, §2) — KHÔNG đường nào tới
    decision-authority-service/risk-gateway; module này KHÔNG bao giờ tự phát Decision.
  bypass Risk Gateway — depends_on rỗng nghĩa là Paper Execution Boundary CHỈ reachable
    NHƯ MỘT DEPENDENCY của execution-engine (execution-engine.depends_on chứa
    paper-execution-boundary, §2) — KHÔNG đường nào cho phép một Trade Intent/Decision đi
    thẳng tới Paper Execution Boundary bỏ qua risk-gateway.
  reinterpret một Risk REJECTED thành APPROVED — Paper Execution Boundary KHÔNG tiêu thụ
    RiskEvaluation trực tiếp (KHÔNG depends_on risk-gateway) — nó chỉ nhận input đã đi
    qua Execution Engine (đã pass Risk Gateway + eligible_for_new_order_creation).
  chia sẻ mutable Live venue state — v0.1/v0.2 KHÔNG LIVE state nào tồn tại trong Domain
    Contract (§3 xác nhận PAPER-only) — KHÔNG venue state thật nào được mô hình hóa.
  âm thầm contaminate Live Order/Fill/Position state — environment: [PAPER] là enum ĐÓNG
    DUY NHẤT trên Order/ExecutionResult/Fill/Position (§3) — KHÔNG giá trị LIVE nào tồn
    tại để contaminate; PAPER/LIVE isolation hiện tại là TRIVIAL (LIVE chưa được mô hình
    hóa), KHÔNG phải một cơ chế isolation runtime đã thiết kế (§16 gap).
  resolve DD-003 — xem §8.2 dưới.
```

### 8.2 DD-003 — KHÔNG resolve (bắt buộc, yêu cầu task)

```text
DD-003 (PAPER-context authoritative Decision establishment mechanism, phase-1-plan.md §11)
VẪN unresolved. module-registry.yaml v0.4 notes (nguyên văn) cho paper-execution-boundary:
"DEFERRED COVERAGE — DD-003 (PAPER-context authoritative Decision establishment
mechanism): the exact trigger/mechanism for establishing an eligible PAPER-context
Decision lineage is NOT decided (mandatory before UC-011 runtime design, per MANIFEST
Deferred Decisions register). This module identifies the BOUNDARY only, does not invent
the establishment mechanism."

Package 1.3-D (tài liệu này) KHÔNG tự phát minh mechanism đó — CHỈ ghi nhận: mọi Domain
Contract elaborate tại đây (risk.md → position.md) đã GIẢ ĐỊNH một Trade Intent/Decision
hợp lệ đã tồn tại (`environment: PAPER` qua account_id) TRƯỚC KHI Risk Gateway bắt đầu
đánh giá — CƠ CHẾ chính xác nào thiết lập PAPER-context Decision lineage đó (trigger
runtime, UC-011 flow) KHÔNG thuộc phạm vi bốn package Phase 1 Engine (1.3-A/B/C/D) đã
author — carry forward §16 nguyên vẹn.
```

## 9. Module boundary — Position Projection (colloquially "Position Ledger" tại `phase-1-plan.md`)

**Trách nhiệm (Package 1.1, KHÔNG đổi):** "Deterministic, NON-authoritative projection dẫn xuất từ visible-valid Fill history (Chapter 7 §7.4 Type 2)."

### 9.1 Terminology (bắt buộc, yêu cầu task — "if that is the current registry/domain assignment")

```text
Xác nhận tường minh: module ĐÃ đăng ký trong module-registry.yaml v0.4 là `position-
projection` — module_type: projection, owns_authoritative_state: false. `phase-1-plan.md`
§8 Package 1.3-D block dùng cụm "Position Ledger" (Applicable quality-gate triggers: "Trigger
C ... Risk Gateway/Execution Engine/Position Ledger") — đây là NGÔN NGỮ MÔ TẢ non-binding,
KHÔNG một module identity riêng biệt. `position.md` (Package 0.2-C7, Consolidated Stable)
tự khóa tường minh: "Position KHÔNG phải một authoritative fact độc lập, KHÔNG có event
stream riêng... một hàm thuần túy, deterministic."

Task yêu cầu: "Define it as the sole authoritative owner of Position state IF THAT IS the
current registry/domain assignment." Xác nhận: ĐÓ KHÔNG PHẢI assignment hiện tại — CẢ hai
nguồn controlling (module-registry.yaml VÀ position.md) đồng thuận Position là projection
KHÔNG authoritative. Package 1.3-D KHÔNG author một "Position Ledger" authoritative
ownership không tồn tại trong registry/domain — Fill Processor (§7) là authoritative
source DUY NHẤT cho mọi dữ liệu Position dẫn xuất.
```

### 9.2 Responsibilities (elaboration, đúng yêu cầu task)

```text
Position Projection được phép:
  tiêu thụ authoritative Fill fact — depends_on CHỈ fill-processor (§2); consumes: event
    (§2).
  áp dụng deterministic ledger transition — Position fold algorithm (position.md §2, năm
    bước: group theo Position key → đánh giá eligible_as_position_contributing_fill
    (fill.md §6) cho mọi Fill → 0 eligible = FLAT/EVALUABLE → 1 eligible =
    LONG|SHORT/EVALUABLE → >1 eligible = NON_EVALUABLE, KHÔNG silently chọn/aggregate).
  duy trì append-only Position lineage — KHÔNG mutate incremental, KHÔNG compensating
    Position event/command (position.md §4) — recompute TRỌN VẸN mỗi khi
    eligible_as_position_contributing_fill result thay đổi cho Fill liên quan.
  hỗ trợ rebuild từ authoritative Fill history — Chapter 7 §7.4 rebuild determinism,
    position.md §1 (KHÔNG event stream riêng — pure derived).
  preserve Account/instrument/venue/execution provenance — Position key = (account_id,
    environment, instrument_selection_ref); mọi field copy nguyên vẹn từ Fill (position.md
    §1/§2).
```

### 9.3 Preserved boundary (bắt buộc, yêu cầu task — KHÔNG được vi phạm)

```text
Position Projection KHÔNG được:
  infer Fill từ Order status ĐƠN THUẦN — Position CHỈ tiêu thụ Fill (authoritative,
    fill-processor, §7), KHÔNG Order/ExecutionResult trực tiếp; `eligible_as_position_
    contributing_fill` (fill.md §6) LÀ nguồn sự thật DUY NHẤT — bản thân rule đó ĐÃ kiểm
    tra ExecutionResult/Observation lineage, Position KHÔNG tự làm việc đó lại.
  nhận Strategy/Decision/Risk mutation trực tiếp — depends_on CHỈ fill-processor (§2) —
    KHÔNG đường nào tới strategy-engine/decision-authority-service/risk-gateway.
  để Execution Engine ghi đè Position state — execution-engine KHÔNG có depends_on edge
    tới position-projection (§2, §5.2 trên) — KHÔNG đường architecture nào tồn tại.
  gộp PAPER và LIVE position mà KHÔNG một ranh giới tường minh — Position key BAO GỒM
    `environment` (position.md §1) — hai Position khác `environment` LÀ hai key khác nhau
    theo cấu trúc; v0.1/v0.2 chỉ có PAPER (§3), LIVE isolation TRIVIAL hiện tại (§8.1, §16
    gap khi LIVE được mô hình hóa trong tương lai).
  dùng mutable current view làm nguồn sự thật — FillCurrentView (fill.md §5) tường minh
    CẤM làm input cho Position; Position PHẢI dùng `eligible_as_position_contributing_fill`
    (fill.md §6) TRỰC TIẾP từ authoritative event stream.
```

### 9.4 Correction, reversal, và replay behavior (elaboration, KHÔNG author accounting formula)

```text
Correction:  Fill correction (invalidate + same-key replacement, fill.md §7) HOẶC
  ExecutionResult correction (execution-result.md §9, CORRECTION computation) đều làm
  eligible_as_position_contributing_fill thay đổi NGAY LẬP TỨC tại cursor liên quan
  (fill.md §6 continuing validity rule — KHÔNG chờ FillFactInvalidated được append) —
  Position projection PHẢI recompute TRỌN VẸN từ scratch (position.md §1/§4), KHÔNG
  compensating event.

Reversal:  KHÔNG có "reversal" command riêng — một Fill trở derived-ineligible (khi
  ExecutionResult tham chiếu không còn visible-valid EXECUTED) tự động khiến Position
  recompute (có thể về FLAT nếu không còn Fill eligible khác, position.md §4). KHÔNG
  close/reduce/reversal arithmetic được author (position.md §"Phạm vi bounded", forbidden
  scope của chính Domain Contract).

Multi-Fill conflict:  NHIỀU eligible Fill lineage cùng Position key → projection_status =
  NON_EVALUABLE, `contributing_fill_refs` liệt kê đầy đủ — KHÔNG chọn một Fill, KHÔNG
  aggregate, KHÔNG weighted average (position.md §2 bước 5) — Package 1.3-D KHÔNG author
  công thức aggregation cho trường hợp này (deferred, position.md §7).

Replay:  Position rebuild TỪ ĐẦU tại mọi cursor C được yêu cầu (position.md §2 bước 6) —
  KHÔNG cache mutate incremental làm nguồn authoritative; downstream consumer PHẢI kiểm
  tra `projection_status` TRƯỚC khi đọc bất kỳ economics field nào (position.md §5).
```

## 10. Authority và non-bypass proof (bắt buộc, yêu cầu task)

```text
Raw plugin output KHÔNG BAO GIỜ là execution authorization — risk-gateway KHÔNG có
  depends_on edge tới strategy-plugin-host (§2); §4.2 xác nhận.

Evaluation proposal KHÔNG BAO GIỜ là execution authorization — risk-gateway.depends_on
  CHỈ chứa decision-authority-service, KHÔNG decision-evaluation-engine (§2, §4.2).

CHỈ một authoritative Decision/Trade Intent được phép vào Risk Gateway — trade_evidence
  (risk.md §5b) resolve từ authoritative Trade Intent/Decision stream, KHÔNG evaluation
  proposal/plugin candidate signal nào khác.

CHỈ một approved Risk output được phép thiết lập Execution Intent — execution-intent.md
  §3 invariant (causation_refs PHẢI trỏ RiskEvaluationRecorded APPROVED).

Execution Engine tiêu thụ Execution Intent, KHÔNG raw Decision — execution-engine.
  forbidden_dependencies chứa strategy-engine/strategy-plugin-host/context-aggregator
  (§2); execution-engine.depends_on chứa risk-gateway (nguồn Execution Intent), KHÔNG
  decision-authority-service trực tiếp.

Position Projection tiêu thụ Fill, KHÔNG Strategy/Decision/Risk instruction — position-
  projection.depends_on CHỈ chứa fill-processor (§2).

KHÔNG API, Event Bus, projection, PAPER module, hay venue adapter nào được bypass Decision
  Authority Service hay Risk Gateway — script-verifiable qua module-registry.yaml v0.4:
```

**Script verification (Python, thực hiện tại transaction này):**

```text
Với mọi module M trong sáu module Package 1.3-D:
  M != risk-gateway  ⟹  'decision-authority-service' NOT IN M.depends_on   (TRUE, xác nhận)
  execution-engine.forbidden_dependencies ⊇ {strategy-engine, strategy-plugin-host,
    context-aggregator}                                                    (TRUE, xác nhận)
  risk-gateway.depends_on == {decision-authority-service, account-service}  (TRUE, xác nhận)
  paper-execution-boundary.depends_on == {}                                 (TRUE, xác nhận —
    root, KHÔNG đường nào từ trên xuống thẳng module này ngoài qua execution-engine)
  position-projection.depends_on == {fill-processor}                        (TRUE, xác nhận)
  fill-processor.depends_on == {execution-result-processor}                 (TRUE, xác nhận)
  execution-result-processor.depends_on == {execution-engine,
    paper-execution-boundary}                                               (TRUE, xác nhận)
```

## 11. Kill switch và safety controls (I-8, bắt buộc, yêu cầu task)

```text
Module nào sở hữu kill-switch state (ĐÃ established, KHÔNG invent thêm):  risk-gateway.
  module-registry.yaml v0.4 responsibilities (nguyên văn): "Risk Policy logic (exposure
  limit, approve/reject, risk-increasing detection, kill switch) — LÀ business logic hợp
  lệ của đúng responsibility này." I-8 (Chapter 2, Locked) Statement: "Hệ thống phải hỗ
  trợ kill switch ở cấp platform, account, strategy, và exchange"; Required guarantees:
  "Risk Gateway phải được phép pause, cancel, hedge, reduce, hoặc controlled unwind theo
  risk policy đã định nghĩa."

Module nào PHẢI observe kill-switch:  I-8 Scope (nguyên văn): "Risk Gateway, Execution
  Engine, mọi Exchange Adapter." Trong ranh giới sáu module Package 1.3-D: risk-gateway
  (owner) VÀ execution-engine (PHẢI observe — §5.2 "bypass kill-switch hay execution-
  suspension control" đã liệt kê tường minh trong preserved boundary). Exchange Adapter
  CHƯA tồn tại (Package 1.2/venue adapter, chưa author) — KHÔNG thể xác nhận observe
  boundary cho module đó tại đây.

Nơi execution mới bị chặn:  tại Risk Gateway (KHÔNG Risk evaluation mới nếu kill-switch
  active trong scope liên quan — I-8 "pause" action) VÀ/HOẶC tại Execution Engine (KHÔNG
  Order creation mới nếu execution-suspension active) — CẢ HAI điểm chặn hợp lý theo I-8
  Scope, NHƯNG cơ chế CHÍNH XÁC (field/event nào biểu diễn kill-switch state, ai emit nó,
  Execution Engine query/subscribe ra sao) CHƯA established tại bất kỳ Domain Contract
  nào đã đọc (risk.md/execution-intent.md/order.md KHÔNG có kill-switch field/event nào)
  — Package 1.3-D KHÔNG invent — carry forward §16 gap.

In-flight handling:  KHÔNG established — risk.md/execution-intent.md/order.md/execution-
  result.md KHÔNG định nghĩa hành vi cho một Execution Intent/Order ĐÃ ISSUED/CREATED
  trước khi kill-switch kích hoạt. Carry forward §16 gap tường minh, KHÔNG tự phát minh.

Stale/unknown kill-switch state fail-safe:  áp dụng I-6 (Fail-Safe by Scope, Chapter 2,
  Locked) như nguyên tắc chung — "Khi không thể xác định tính đúng đắn của dữ liệu, trạng
  thái, risk hoặc execution trong một scope, hệ thống phải chuyển scope đó về trạng thái
  an toàn. Mặc định không được mở thêm risk-increasing exposure." Package 1.3-D áp dụng
  nguyên tắc NÀY cho kill-switch cụ thể (stale/unknown state → treat như active/fail-
  closed cho risk-increasing action, vẫn cho phép risk-reducing action theo I-6) — NHƯNG
  KHÔNG author cơ chế detect "stale/unknown" cụ thể (thiếu event/field xác nhận kill-
  switch state đã pin ở Domain Contract level) — carry forward §16 gap.

PAPER và LIVE isolation:  TRIVIAL hiện tại — v0.1/v0.2 Domain Contract KHÔNG mô hình hóa
  LIVE path (§3/§8.1) — KHÔNG cần isolation runtime giữa hai environment CHƯA CẢ HAI cùng
  tồn tại. Khi LIVE được mô hình hóa (tương lai, ngoài phạm vi), kill-switch scope theo
  I-8 ("cấp platform, account, strategy, và exchange") sẽ cần áp dụng ĐỘC LẬP cho từng
  environment — carry forward §16 gap, KHÔNG thiết kế trước.
```

## 12. Idempotency (I-10, bắt buộc, yêu cầu task)

```text
Execution Intent issuance:      `execution_intent_derivation_idempotency_policy:
                                 ONE_VALID_INTENT_PER_ORIGINATING_RISK_EVALUATION`
                                 (execution-intent.md §10) — same origin + same payload →
                                 idempotent reuse; same origin + payload khác →
                                 deterministic conflict.

Order creation/submission:      `order_creation_derivation_idempotency_policy:
                                 ONE_VALID_ORDER_PER_ORIGINATING_EXECUTION_INTENT` (order.md
                                 §11) cho creation; `order_submission_idempotency_policy`
                                 scoped theo order_id (order.md §6/§11) cho submission
                                 request — trước khi ghi, kiểm tra order_id chưa có
                                 OrderSubmissionRequested VALID nào khác.

Venue retry:                    KHÔNG established — v0.1/v0.2 Domain Contract KHÔNG mô
                                 hình hóa venue thật (chỉ PAPER boundary, §3/§8) — I-10's
                                 "venue order, child order" concept CHƯA có tương ứng
                                 domain fact nào được author. Carry forward §16 gap (đối
                                 xứng "venue-adapter protocol and authority boundary" đã
                                 yêu cầu carry forward).

Execution Result ingestion:     `execution_result_computation_id` là logical identity
                                 (execution-result.md §2) — INITIAL: tối đa MỘT
                                 computation cho mỗi submission_request_id BẤT KỂ cursor
                                 khác nhau; CORRECTION: tối đa MỘT cho mỗi predecessor
                                 (cấm fork). Idempotency neo vào computation identity,
                                 KHÔNG cursor — v0.3 correction (`C7-DELTA-MAJ-01`) đóng
                                 chính xác gap này.

Fill ingestion:                 `fill_derivation_idempotency_policy:
                                 ONE_VALID_FILL_PER_EXECUTION_RESULT` (fill.md §8) —
                                 logical Fill key = execution_result_id; same key + same
                                 payload → idempotent reuse; same key + payload khác →
                                 deterministic conflict.

Position application:           KHÔNG idempotency key riêng cần thiết — Position KHÔNG
                                 có "apply" command trực tiếp, CHỈ recompute TRỌN VẸN
                                 (position.md §2/§4) — recompute nhiều lần với CÙNG tập
                                 eligible Fill LUÔN cho CÙNG kết quả (pure function,
                                 deterministic theo cấu trúc, KHÔNG cần duplicate-
                                 suppression riêng).
```

**Xác nhận tường minh (yêu cầu task — "Do not design concrete keys, databases, locks or retry algorithms"):** mọi identity trên trích dẫn NGUYÊN VĂN Domain Contract đã khóa — Package 1.3-D KHÔNG author concrete key format, database, lock mechanism, hay retry algorithm nào.

## 13. Determinism, replay và no-repaint

```text
Risk Policy/version pinning:       bốn trục risk evidence (risk_policy_definition_
                                    version_ref/risk_policy_configuration_version_ref/
                                    risk_plugin_version_ref/package_build_artifact_ref,
                                    risk.md §5b3) — persistently resolvable tại cursor
                                    (Chapter 8 §8.1.1 mục 4) để AVAILABLE; nếu không →
                                    NON_EVALUABLE.

Account/execution-boundary          risk.md §5c bước 7: account_id.current_status(cursor)
  eligibility tại evaluation cursor: == ACTIVE (reconstruct TẠI cursor, KHÔNG
                                    AccountCurrentView). order.md §4a: eligible_for_new_
                                    order_creation transitive check.

Recorded-time visibility:          universal — mọi authoritative fact dùng cho evidence
                                    PHẢI thỏa fact.recorded_time ≤ cursor.recorded_time
                                    (risk_context_cursor/order_context_cursor/
                                    observation_cursor/fill_context_cursor — TẤT CẢ tái sử
                                    dụng nguyên vẹn canonical Replay Cursor, Chapter 8
                                    §8.5.1).

Effective-time eligibility:        chuỗi causal đầy đủ bắt buộc: RiskEvaluation.
                                    risk_evaluation_time ≤ ExecutionIntentIssued.
                                    effective_time ≤ OrderCreated.order_effective_time ≤
                                    OrderSubmissionRequested.effective_time ≤
                                    PaperExecutionObservationRecorded.effective_time ≤
                                    ExecutionResultRecorded.result_effective_time ≤
                                    FillRecorded.fill_effective_time (tổng hợp từ risk.md
                                    §12/execution-intent.md §9/order.md §14/execution-
                                    result.md §12 (offset)/fill.md §9 — KHÔNG một field
                                    mới, chỉ tổng hợp chuỗi đã khóa riêng lẻ).

ADR-009 per-stream ordering:       mỗi authoritative event thuộc đúng MỘT ordered stream,
                                    causal correctness qua causation_refs tường minh,
                                    KHÔNG global total order — cấm so sánh sequence thô
                                    xuyên stream (Chapter 8 §8.3.3) — áp dụng đồng nhất
                                    cho cả sáu module.

Explicit causation Decision→        causation_refs one-way chain xuyên suốt: Attempt→
  Position:                        RiskEvaluation (risk.md §5) → RiskEvaluation→Execution
                                    Intent (execution-intent.md §3) → Attempt→Order
                                    (order.md §4) → Order→OrderSubmissionRequested (order.md
                                    §6) → ExecutionResultComputationAuthorized→Observation
                                    →Attempt→ExecutionResult (execution-result.md §5-§8) →
                                    ExecutionResult→Fill (fill.md §3) — mọi liên kết
                                    KHÔNG BAO GIỜ rỗng, một chiều, KHÔNG circular reference
                                    (bài học C4-DELTA-MAJ-01 áp dụng lặp lại xuyên suốt cả
                                    sáu Domain Contract).

Mode parity nơi áp dụng:           v0.1/v0.2 CHỈ PAPER — I-2 Decision Parity áp dụng đầy
                                    đủ ở tầng Decision/Trade Intent (Package 1.3-C) nhưng
                                    Execution Result/Fill LÀ bounded PAPER SIMULATION
                                    (execution-result.md §1 "bounded PAPER simulation
                                    computation") — KHÔNG một "real venue" tồn tại để so
                                    sánh Live/Paper parity tại tầng này; mode parity nghĩa
                                    hẹp: cùng computation identity + cùng evidence → cùng
                                    simulated output, deterministic (execution-result.md
                                    §1 invariant).

Append-only correction/            RiskEvaluation (risk.md §10), Execution Intent
  invalidation:                    (execution-intent.md §8, invalidate-only cho Issued),
                                    Order (order.md §9, correction lineage chuẩn cho
                                    Created, invalidate-only cho SubmissionRequested),
                                    ExecutionResult (execution-result.md §11, correction
                                    lineage chuẩn qua ExecutionResultComputation(CORRECTION)),
                                    Fill (fill.md §7, correction lineage chuẩn) — TẤT CẢ
                                    dùng invalidate-then-replace, KHÔNG PATCH tại chỗ.

No silent mutation:                mọi entity BẤT BIẾN sau khi ghi — correction LUÔN qua
                                    một fact MỚI (ID khác) + `supersedes_fact_ref` trỏ
                                    TRỰC TIẾP predecessor (KHÔNG trỏ FactInvalidated —
                                    convention nhất quán risk.md §10/order.md §9/execution-
                                    result.md §11/fill.md §7).

Projection/ledger rebuild          Position Projection (§9) rebuild TỪ ĐẦU tại mọi cursor
  determinism:                     — Chapter 7 §7.4 rebuild determinism, KHÔNG cache
                                    mutate incremental làm nguồn authoritative.
```

**External venue outcomes — KHÔNG deterministically reproducible (bắt buộc, yêu cầu task):**

```text
v0.1/v0.2 Domain Contract KHÔNG chạm venue thật — mọi execution outcome hiện tại là bounded
PAPER SIMULATION (execution-result.md §1), tự thân deterministic theo evidence bundle
(simulation_policy_ref/simulation_configuration_ref/simulation_build_ref/
deterministic_input_ref, execution-result.md §1). Khi Package tương lai (ngoài phạm vi
1.3-D) mô hình hóa LIVE venue execution, kết quả từ MỘT venue thật (fill price/timing/
partial-fill) KHÔNG deterministically reproducible bằng Replay — Replay CHỈ có thể
represent RECORDED outcome (ExecutionResult/Fill đã ghi) như evidence lịch sử, KHÔNG re-
execute venue call. Đây là nguyên tắc chung (đối xứng ADR-010 §2.6 Append-and-Revalidate
— "Decision đã tính vẫn phải tái dựng được... KHÔNG phải re-run venue"), Package 1.3-D
KHÔNG author venue-replay mechanism cụ thể vì venue adapter CHƯA tồn tại (forbidden scope
+ §16 gap).
```

## 14. Security / trust-boundary identification

```text
risk-gateway:                security_classification: trust_boundary_candidate
                              (module-registry.yaml v0.4, KHÔNG đổi) — Risk Policy
                              boundary, tiềm năng chạm Account/custody-adjacent scope
                              (account-service, custody_adjacent — Package 1.2). IDENTIFICATION
                              ONLY tại đây — KHÔNG auth mechanism/credential design.
execution-engine:             security_classification: trust_boundary_candidate — venue/
                              custody-adjacent execution surface tiềm năng (Paper Execution
                              Boundary hiện tại, venue adapter thật tương lai).
execution-result-processor,   security_classification: none (module-registry.yaml v0.4,
  fill-processor, position-    KHÔNG đổi) — internal authoritative stream/projection
  projection, paper-execution- thuần túy, KHÔNG chạm external network boundary/credential
  boundary:                    trực tiếp.

I-11 (Secrets & Custody Isolation, Locked) boundary:  "Chỉ Exchange Adapter hoặc dedicated
  Custody/Signing Service được phép sử dụng exchange credential trực tiếp." KHÔNG module
  nào trong sáu module Package 1.3-D là Exchange Adapter/Custody-Signing Service — venue
  adapter CHƯA tồn tại (§16 gap). Package 1.3-D KHÔNG design credential storage/signing
  (forbidden scope).

Trigger D (quality-gate, phase-1-plan.md §8 Package 1.3-D block, KHÔNG redefine):  CÓ ĐIỀU
  KIỆN — "áp dụng khi kiến trúc định nghĩa concrete custody-adjacent boundary." Package
  1.3-D chưa định nghĩa concrete boundary (Package 1.2 chưa tồn tại, §16) — Trigger D
  evaluation deferred.
Trigger C (Chaos Test, Tier 0):  deferred tới implementation NHƯNG PHẢI thiết kế chaos-
  testable by design (phase-1-plan.md §8) — idempotency mapping (§12) là nền tảng cho
  yêu cầu này, Package 1.3-D KHÔNG author test cụ thể (forbidden scope: "author source
  code or tests").
```

## 15. Preserved boundaries (xác nhận tường minh, yêu cầu task)

```text
Package 1.1 (module identity/taxonomy/dependency, v0.4, Consolidated Stable):  KHÔNG đổi
  — §2 trích dẫn nguyên văn, không thêm/sửa module hay edge nào.

Package 1.3-A (Structure/Regime independence, Feature Engine downstream role,
  Consolidated Stable):  KHÔNG chạm — ngoài phạm vi hoàn toàn của sáu module trong
  Package 1.3-D.

Package 1.3-B (Feature/Context boundary, Consolidated Stable):  KHÔNG chạm.

Package 1.3-C (Strategy/Decision authority model, mandatory non-bypass sequence tới
  Decision Authority Service, Consolidated Stable):  KHÔNG đổi — §4/§10 trích dẫn nguyên
  vẹn "Decision Authority Service SOLE authority" đã Approved (ADR-016 v0.8), KHÔNG
  redefine.

ADR-012 (Account-to-Boundary Cardinality):  KHÔNG đổi — §2.5 Position scope rules dưới
  Account Boundary (venue-bound/broker-bound) trích dẫn nguyên vẹn tại §9 (khi liên quan)
  — Package 1.3-D KHÔNG author execution_venue_id concrete mechanism (chưa có venue
  adapter, §16).

risk.md/execution-intent.md/order.md/execution-result.md/fill.md/position.md (Package
  0.2-C5/C6/C7, Consolidated Stable):  KHÔNG đổi — mọi trích dẫn tại §4–§13 nguyên văn,
  KHÔNG redefine entity/event/invariant nào.
```

## 16. Preserved unresolved gaps (KHÔNG resolve, chỉ carry forward — bắt buộc, yêu cầu task)

```text
1. DD-003 — PAPER-context authoritative Decision establishment mechanism remains
   unresolved (phase-1-plan.md §11, §8.2 trên). Package 1.3-D KHÔNG tự phát minh mechanism
   này — chỉ escalate, đúng explicit non-goal đã pin tại phase-1-plan.md §8 Package 1.3-D
   block.

2. Custody-adjacent boundary details CHƯA established bởi Package 1.2 — KHÔNG file kiến
   trúc nào tồn tại tại `docs/architecture/` cho Package 1.2 tính đến baseline HEAD của
   transaction này (§1 xác nhận). `account-service.security_classification:
   custody_adjacent` (module-registry.yaml) là identification ONLY — KHÔNG design.

3. Venue-adapter protocol và authority boundary — hoàn toàn CHƯA author (forbidden scope);
   `execution-engine`/`paper-execution-boundary` là ranh giới CHỈ dành cho PAPER simulation
   hiện tại (§3/§8), KHÔNG venue thật nào được mô hình hóa.

4. Kill-switch ownership CỤ THỂ về in-flight behavior — §11 xác nhận risk-gateway sở hữu
   kill-switch POLICY (established), NHƯNG cơ chế field/event representation, observation
   protocol cụ thể (Execution Engine), VÀ in-flight handling (Execution Intent/Order đã
   issued trước khi kill-switch kích hoạt) đều CHƯA established tại bất kỳ Domain Contract
   nào — carry forward nguyên vẹn.

5. External venue retry/idempotency mechanism — I-10's "venue order, child order,
   execution attempt" concept CHƯA có domain fact tương ứng (v0.1/v0.2 chỉ PAPER
   simulation, §12). Carry forward.

6. Partial-fill và correction mechanics nơi Domain Contract tự defer — fill.md §13 "Full-
   Fill boundary (disclosed v0.1 judgment call)" — v0.1/v0.2 KHÔNG partial-fill semantics;
   position.md §7 "Multiple-Fill-per-Position-key resolution" — KHÔNG aggregation formula
   cho >1 eligible Fill lineage (NON_EVALUABLE thay vì tự ý tính). Cả hai deferred tường
   minh bởi chính Domain Contract, Package 1.3-D KHÔNG resolve.

7. ADR-009 concrete ordering protocol implementation — per-stream sequence allocation,
   watermark/frontier mechanism, late-arrival protocol, writer handoff/retirement
   protocol, storage/archive/retention policy — deferred sang Phase 1 (ADR-009 §6), Package
   1.3-D chỉ áp dụng nguyên tắc (§13), KHÔNG author protocol cụ thể.

8. Definition Version registry mechanism — feature_definition_version/context_definition_
   version (Package 1.3-A/1.3-B) CỘNG risk_policy_definition_version/risk_policy_
   configuration_version/risk_plugin_version/package_build_artifact (risk.md §5b3) CỘNG
   simulation_policy_ref/simulation_configuration_ref/simulation_build_ref/
   deterministic_input_ref (execution-result.md §1) — cơ chế lưu trữ/versioning CỤ THỂ
   của mọi registry này là Phase 1 concern CHƯA elaborate.

9. context.md authority-terminology gap — kế thừa nguyên vẹn từ Package 1.3-B §13/Package
   1.3-C §13 (context.md §2 "authoritative event record" framing vs module-registry.yaml
   Type 2 Projection classification) — KHÔNG trực tiếp chạm Package 1.3-D (sáu module
   Package 1.3-D KHÔNG depends_on context-aggregator), nhưng ghi nhận như một upstream
   prerequisite tension chưa resolve, theo yêu cầu task "context.md authority-terminology
   gap where referenced."

10. Toàn bộ chín gap đã preserved tại Package 1.3-C (Consolidated Stable, §13 của chính
    tài liệu đó) VẪN LÀ upstream prerequisite cho Package 1.3-D — đặc biệt: Plugin Host vs
    Decision Evaluation exact boundary; evaluation-proposal Domain Contract absence;
    attempt_outcome rejection-mapping gap — các gap này ảnh hưởng TRỰC TIẾP input mà
    Risk Gateway (§4) tiêu thụ (authoritative Decision/Trade Intent output của Decision
    Authority Service) — Package 1.3-D KHÔNG resolve, chỉ ghi nhận phụ thuộc ngược dòng.

11. `replay-integration-service` elaboration gap (§2 "Quan sát minh bạch" trên) — thuộc
    phạm vi Package 1.3-A (đã Consolidated Stable), KHÔNG được Package 1.3-D sửa — ghi
    nhận minh bạch, KHÔNG tự ý elaborate.
```

## 17. Explicit non-goals

```text
KHÔNG author field-level event schema (đã khóa tại sáu Domain Contract, Package
  0.2-C5/C6/C7, Consolidated Stable) — chỉ contract CATEGORY (event/query/command).
KHÔNG author Risk Policy formula/sizing algorithm cụ thể.
KHÔNG author venue adapter field-level protocol.
KHÔNG author custody implementation.
KHÔNG author credential storage/signing design.
KHÔNG author database hay API schema.
KHÔNG chọn exchange/broker/database/framework/deployment topology.
KHÔNG author source code hay test.
KHÔNG resolve DD-003 (§8.2/§16 gap #1).
KHÔNG redefine module identity/taxonomy/dependency đã pin tại Package 1.1
  (module-registry.yaml/system-decomposition.md v0.4, Consolidated Stable).
KHÔNG redefine Package 1.3-A/1.3-B/1.3-C content (Consolidated Stable).
KHÔNG tạo/approve ADR nào — mechanical elaboration của registry/Domain Contract hiện có
  KHÔNG cần ADR mới (đúng ADR rule của task — KHÔNG custody/credential authority owner
  mới, KHÔNG execution-authority owner mới, KHÔNG Risk Gateway bypass, KHÔNG source-of-
  truth boundary mới, KHÔNG PAPER/LIVE isolation model mới, KHÔNG dependency/topology
  ngoài Approved authority hiện có).
KHÔNG mark Package 1.3-D Consolidated Stable.
KHÔNG pass Gate 2.
KHÔNG tuyên bố Phase 1 hoàn thành.
KHÔNG mở Phase 2.
KHÔNG authorize Live.
```

## 18. Review and consolidation conditions

```text
Review A scope:               Decision → Trade Intent → RiskEvaluation → Execution Intent
                               thứ tự bảo toàn (§3/§4a, script-check qua causation_refs
                               chain); Risk Policy logic KHÔNG rò rỉ ra ngoài Risk Gateway
                               (Chapter 3 §3.1, §4.3); module boundary elaboration (§4–§9)
                               nhất quán với module-registry.yaml v0.4 (Consolidated
                               Stable) — không silent semantic invention; Position
                               terminology (§9.1) đúng — KHÔNG authoritative ownership bị
                               fabricate; mọi gap (§16) carry forward trung thực, KHÔNG bị
                               silently resolved (đặc biệt DD-003, custody-adjacent, kill-
                               switch in-flight).
Independent Review B
  scope:                      Độc lập xác nhận I-8 (Kill Switch)/I-10 (Idempotent
                               Execution) scope được map đúng module trong kiến trúc
                               (§11/§12, đúng phase-1-plan.md §8 Package 1.3-D
                               Independent Review B scope) — KHÔNG invent ownership/
                               mechanism nào chưa established; xác nhận Risk Gateway
                               KHÔNG bypassable (§10 script verification); xác nhận
                               Execution Engine/Position Projection KHÔNG có đường nào
                               tới Decision Authority Service/Strategy layer ngoài qua
                               Risk Gateway; xác nhận PAPER Execution Boundary KHÔNG được
                               mô tả như một Decision/Risk authority thay thế (§8.1).
Product Owner decision
  point:                      Sau Review A/B CLEAN.
Consolidation condition:      Zero unresolved Blocker/Major; ADR custody-boundary (nếu
                               ảnh hưởng trực tiếp) Approved; Package 1.2 baseline đủ dùng
                               cho phần custody-adjacent đã pin (phase-1-plan.md §8 —
                               KHÔNG bắt buộc trước khi authoring, NHƯNG bắt buộc trước
                               khi Package 1.3-D tự Consolidated Stable).
```
