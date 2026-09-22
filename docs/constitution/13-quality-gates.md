---
id: 13-quality-gates
title: Quality Gates
version: "1.8"
status: Draft
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: null
next_review: null
depends_on: ["02-platform-invariants", "07-module-taxonomy"]
---

# 13. Quality Gates

> **Trạng thái:** `Locked`. Product Owner đã **Approve and Lock** Chapter 13 v1.7. Theo [Chapter 12 §12.3](./12-approval-gates.md), chương này từ nay là **binding authoritative Quality Gates contract** — đúng contract mà [Chapter 12 §12.2(5)](./12-approval-gates.md) yêu cầu cho applicable quality gates. Quality Gate vẫn khác Product Owner Approval Gate (§13.1) — trạng thái Locked không đổi phân biệt đó.
>
> **v1.8 CANDIDATE (2026-09-22) — `Draft`, NOT reviewed, NOT approved, NOT controlling.** Authored per Chapter 0 §5.1 (a Locked living document cannot be edited in place at the same version — a new candidate version must be authored and pass its own fresh approval gate). Adds new §13.8.1 ("Bounded-measurement reproducibility for `UNSTABLE_TIMEOUT_TRIAGE` populations"). **`CONSOLIDATION` (root-cause pass, `P3-CORRECTION-CHAIN-001`, following three narrow correction rounds that did not converge):** §13.8.1 is now the **sole normative source** for this rule — self-contained, requiring no reference to any ADR to understand or apply correctly. `docs/adr/ADR-044.md` v0.5 (`Draft`) carries the architecture rationale, alternatives, and consequences only, with no second executable copy of the gate semantics; a clause-trace table there maps every ADR guarantee to its exact normative clause here. If ADR prose and this section ever disagree, **this section controls Quality-Gate semantics** (§13.13). This consolidation restores the per-mutant/gate-level reproducibility reconciliation that a prior correction round had inadvertently dropped, clarifies Testing Convention item 8's evidence-layer precedence without ambiguous wording, and makes protocol provenance a structural (property-based) requirement rather than a reference to an unpinned "presently-governed" protocol. **`v1.7`, `Locked`, remains the sole controlling authoritative version of this chapter until this `v1.8` candidate is itself reviewed, accepted, and activated** — see MANIFEST for current authoritative pointer (I-12). No other section of this chapter is touched by this candidate; §13.8's own existing fail-closed text (above the new §13.8.1) is byte-unchanged.

## 13.1 Purpose and scope

**Quality Gate** là một **fail-closed eligibility check** sinh ra **immutable pass/fail evidence** về việc một artifact có đạt các quality criteria đã định nghĩa hay không. Quality Gate trả lời đúng một câu hỏi:

> Artifact này có pass Quality Gate hay không, và dựa trên evidence nào?

**Quality Gate KHÁC Approval Gate:**

```text
Quality Gate pass  ≠  Product Owner approval
Quality Gate fail  ≠  Product Owner rejection
Quality Gate       →  sinh eligibility evidence
Approval Gate      →  consume evidence đó (Chapter 12 §12.2(5))
```

- Quality Gate **không** approve, **không** lock, **không** quyết định phase transition. Nó chỉ cung cấp evidence cho [Chapter 12](./12-approval-gates.md); Product Owner vẫn là **authority duy nhất** quyết định (Ch12 §12.2, [Chapter 0 §3](./00-governance.md)).
- Reviewer recommendation và validator result **không phải** gate pass/fail; validator là blocking consistency check, không phải quality authority ([Chapter 11 §11.9](./11-adr-process.md)).

**Phạm vi áp dụng** — các quality-bearing artifact:

| Artifact class | Ví dụ |
|---|---|
| Runtime module | Compute Engine / Projection / Runtime Service ([Chapter 7](./07-module-taxonomy.md)) |
| Published contract / schema | event schema, API/query/command contract, Domain Contract |
| Release / build | deployable artifact, tagged build |
| Migration | data/schema/state migration + rollback |
| Phase deliverable | evidence do phase plan/roadmap yêu cầu |

**Không đóng open question:** chương này **không** giải quyết **OQ-002** (Strategy Lifecycle Live-gate) hay **OQ-003** (Product Metrics). Quality Gate cung cấp **input evidence** cho các gate/metric đó, nhưng khai báo "gate pass" **không** đồng nghĩa "được phép lên Live" — nhất quán [Chapter 9 §9.10](./09-plugin-model.md) và [Chapter 10 §10.8.2](./10-compatibility-capability-contract.md) (không chapter nào được đóng ngầm OQ-002).

## 13.2 Quality dimensions

Quality Gate đánh giá **nhiều chiều**, không quy về một con số coverage. Mỗi dimension có authority sở hữu **substance**; Chapter 13 chỉ sở hữu việc **gom chúng thành gate + evidence**.

| Dimension | Ý nghĩa | Substance authority |
|---|---|---|
| Correctness / invariant conformance | Hành vi đúng theo Platform Invariant | [Chapter 2](./02-platform-invariants.md) (I-1…I-13) |
| Determinism / reproducibility | Cùng input → cùng output; rebuild được | I-2, I-3, I-12; [Chapter 5](./05-time-model.md) |
| Parity | Replay/Backtest/Paper/Live cùng Decision | I-2 |
| Resilience / fault tolerance | Hành vi đúng khi lỗi/timeout/partial | I-6, I-8, I-10 |
| Performance | Không regress ngoài budget (§13.7) | Chapter 13 (§13.7) |
| Security / custody | Isolation, secret không rò rỉ | I-4, I-7, I-11 |
| Data quality / numerical precision | Lossless, đúng precision/quantization | I-9 |
| Contract / schema compatibility | Tương thích theo chiều đã cam kết | [Chapter 10 §10.3](./10-compatibility-capability-contract.md) |
| Migration / rollback safety | Migrate và rollback an toàn | I-13; Chapter 10 |
| Observability / operational readiness | Đo được, vận hành được | [Roadmap](./14-roadmap.md); Phase 1.5/9 |
| Explainability / auditability | Trace tái dựng từ evidence | I-1 |

Coverage (§13.3–§13.4) là **một tín hiệu**, không phải toàn bộ chất lượng.

## 13.3 Coverage — semantics và anti-gaming

**Coverage PASS rule (deterministic):** coverage của một artifact đạt yêu cầu **khi và chỉ khi cả hai** metric độc lập đều đạt floor của tier áp dụng:

```text
line coverage   >= applicable tier floor
AND
branch coverage >= applicable tier floor
```

Cả hai phải đạt **độc lập** — chỉ cần một metric dưới floor thì coverage **không** đạt (không bù trừ giữa hai metric, không dùng con số tổng hợp). Floor theo tier (§13.4): **Tier 0 ≥ 95% · Tier 1 ≥ 90% · Tier 2 ≥ 80% · Tier 3 ≥ 60%**, áp cho **từng** metric. Đo trên **authoritative implementation** của capability ([Chapter 3 §3.1](./03-engineering-principles.md)). Condition/MC-DC coverage là **tùy chọn theo tier** (khuyến nghị Tier 0), **không** tính vào floor bắt buộc.

**Thiếu một trong hai metric, hoặc evidence không resolve được → `FAIL — evidence`** (§13.8–§13.9), **không** phải pass mặc định. Coverage là **floor signal về sự hiện diện của test**, **không** phải bằng chứng chất lượng test. Không khóa tool/vendor cụ thể (defer §13.14).

**Anti-gaming (bắt buộc):**

- Chỉ tính coverage từ test có **assertion có nghĩa**; test chạy-mà-không-assert (execution-only), snapshot thuần không kiểm semantic → **không tính**.
- Coverage phải đo trên authoritative implementation, **không** trên mock/generated/shadow code (I-2: research và production dùng chung logic).
- Coverage percentage **là điều kiện cần, không đủ**: với artifact **mà coverage applicable** (§13.12 nhóm B), artifact chỉ pass khi coverage đạt tier floor **và** các dimension gate áp dụng (§13.5–§13.7) pass.
- **Test-effectiveness cho Tier 0/1:** coverage number không thể chứng minh test *bắt được lỗi*. Tier 0 và Tier 1 phải có **evidence về test effectiveness** (mechanism được chấp nhận: mutation testing hoặc tương đương). Chapter 13 khóa **yêu cầu có evidence**; **ngưỡng cụ thể + tooling** defer Engineering Foundation (§13.14).

## 13.4 Coverage tiers

Coverage yêu cầu phân theo **mức độ nguy hiểm (criticality)**, không dùng một ngưỡng chung cho toàn hệ thống:

| Tier | Thành phần (initial assignment) | Coverage tối thiểu | Yêu cầu thêm |
|---|---|---|---|
| Tier 0 — Critical | Risk Gateway, Execution Engine, Position Ledger | ≥ 95% | Bắt buộc **Chaos Test** (exchange timeout, partial fill, duplicate order, order reject) — cross-ref I-10 |
| Tier 1 — Core Logic | Strategy Engine, Feature Engine, Structure Engine, Regime Engine | ≥ 90% | Bắt buộc **Parity Test** (Replay khớp Live tại tầng Decision) — cross-ref I-2 |
| Tier 2 — Supporting | API layer, Data Ingestion | ≥ 80% | |
| Tier 3 — UI | Frontend | ≥ 60% | Ưu tiên E2E test hơn unit test |

**Thẩm quyền ánh xạ tier:** Chapter 13 sở hữu **định nghĩa tier và gate requirement per tier**. Việc **module cụ thể nào thuộc tier nào** là **criticality classification** — được pin tại `module-registry.yaml` ([Chapter 7 §7.5](./07-module-taxonomy.md)) khi registry tồn tại (Phase 1), nhất quán criticality declaration của [Chapter 7 §7.4](./07-module-taxonomy.md) và [I-6](./02-platform-invariants.md). Cột "initial assignment" ở trên là ánh xạ hiện hành cho các module đã biết, **không** phải competing authority với registry; khi registry active, mapping resolve từ registry.

**Tier resolution — bắt buộc trước gate evaluation.** Mọi **coverage-applicable artifact** (§13.12 nhóm B) phải resolve được **đúng một** authoritative quality tier **trước khi** gate chạy. Chain resolution:

1. **Runtime module** → resolve tier từ `module-registry.yaml` ([Chapter 7 §7.5](./07-module-taxonomy.md)). **Không** thay đổi authority của Chapter 7.
2. **Executable artifact thuộc đúng một canonical owning module** → **inherit** tier của owning module. Ownership relationship phải **explicit · resolvable · versioned/pinned**, và **không do validator tự suy diễn**. *Ví dụ:* executable migration thuộc Position Ledger → inherit Tier 0 của Position Ledger. **Authority contract đứng sau ownership relationship này** — canonical ownership-binding authority, anti-self-selection, ownership-binding chain — khóa tại [§13.4.2](#1342-canonical-ownership-binding-authority--owned-executable-artifact).
3. **Standalone executable artifact** (không có canonical owning module) → phải có **authoritative quality-tier declaration**: **explicit · versioned · pinned** vào exact artifact/version · có **authority owner** · **tồn tại trước** gate evaluation. Gọi chung là **authoritative artifact/quality metadata** (storage/schema defer §13.14). Đây **không** phải mở rộng `module-registry.yaml` thành registry cho mọi artifact. **Authority contract đứng sau "authority owner"** — canonical designation, anti-self-certification, authority chain — khóa tại [§13.4.1](#1341-canonical-tier-designation-authority--standalone-executable-artifact).
4. **Multiple/ambiguous ownership hoặc tier không resolve** — nhiều possible owning module · ownership không resolve duy nhất · tier declarations conflict · tier không resolve được → **undefined tier applicability → fail-closed → eligibility incomplete** (§13.8). **Không** tự chọn tier cao nhất hay thấp nhất trừ khi Constitution định nghĩa explicit rule (hiện **chưa** có).
5. **Validator boundary:** validator **không** suy diễn tier, **không** default tier, **không** tạo ownership; chỉ **kiểm tra** authoritative declaration/inheritance đã resolve. Validator **không** phải quality-policy authority ([Chapter 11 §11.9](./11-adr-process.md)).

> Tier-resolution provenance (branch, ownership, tier source, resolved tier + coverage floor) phải được **pin vào immutable gate evidence** theo **§13.9** — historical result không bị reinterpret khi metadata đổi về sau.

### 13.4.1 Canonical tier-designation authority — standalone executable artifact

Nhánh 3 của tier-resolution chain (§13.4) yêu cầu standalone executable artifact có **authoritative quality-tier declaration** với **authority owner**. Mục này khóa **authority contract** đứng sau field đó — nếu không, "authority owner" chỉ là một field tự khai, và validator không có authority root để phân biệt declaration hợp lệ với self-certified declaration:

```text
standalone artifact producer
→ tự tạo tier declaration của chính nó
→ khai Tier 3, dùng floor 60%
→ declaration explicit/versioned/pinned
→ không có declaration nào khác để xung đột
→ validator không có authority root để reject
```

**Canonical tier-designation authority — bắt buộc trước gate evaluation.** Với mọi artifact/scope mà quality tier là bắt buộc (nhánh 3, §13.4):

- phải resolve được **đúng một** canonical quality-tier designation authority cho scope đó;
- authority đó phải **tồn tại trước** gate evaluation;
- authority identity/designation phải **explicit · versioned · immutable/pinned**;
- **scope của authority** phải khai báo tường minh;
- authority **không resolve được** hoặc **có nhiều authority cạnh tranh cho cùng scope** → **fail-closed** (§13.8), không tự chọn một trong số đó.

Không khóa filename, vendor, CI implementation hay serialization format cụ thể — cùng nguyên tắc §13.14.

**Canonical establishment predicate — dùng chung cho mọi canonical authority Chapter 13 yêu cầu** (áp cho cả tier-designation authority ở đây lẫn ownership-binding authority ở [§13.4.2](#1342-canonical-ownership-binding-authority--owned-executable-artifact)). Bản thân yêu cầu "đúng một canonical authority" ở trên chưa trả lời **điều gì làm một designation trở thành canonical** — thiếu predicate này, "authority owner" chỉ là field tự khai. Một designation/authority chỉ đạt trạng thái **canonical** khi thỏa **cả hai** điều kiện dưới đây — không điều nào tự thỏa được bằng nội dung do chính subject/producer tạo ra:

1. **Established qua governance approval** — việc gán scope cho authority đó phải là kết quả của **Decision Workflow** ([Chapter 0 §3](./00-governance.md)), áp đúng **ADR Scope Rule** khi thuộc diện đó ([Chapter 0 §4b](./00-governance.md)). Chapter 13 **không định nghĩa lại** cơ chế approval này — chỉ tham chiếu nó làm **external authoritative basis**, cùng pattern governance-approval anchor mà [Chapter 10 §10.4.3(4)](./10-compatibility-capability-contract.md) (Locked) đã khóa cho Compatibility Policy authority.
2. **Recorded tại một authoritative project state resolvable độc lập** với chính declaration chain của subject — ví dụ tài liệu đã qua governance approval (Locked chapter, ADR đã Approved, hoặc entry ghi nhận đúng quy trình tại MANIFEST) — **không** phải một artifact/section do chính producer publish cùng lúc với declaration nó đang cố hợp thức hóa.

**Vì sao predicate này chấm dứt đệ quy (terminating, không tạo infinite designator regress):** governance approval (Product Owner decision qua Decision Workflow, [Chapter 0 §3](./00-governance.md)) là **primitive authority** đã Locked của toàn Constitution — predicate này bottom-out tại chính quyết định đó, không tạo ra một "designation của designation" mới cần thêm một authority riêng để tự hợp thức hóa.

**Áp cho đúng failure scenario đã dẫn tới mục này:** producer P tự tạo designation D rồi tự cho D quyền authorize P → D không thỏa điều kiện 1 (không đi qua Decision Workflow/ADR Scope Rule) **và** không thỏa điều kiện 2 (D không resolvable từ authoritative project state độc lập với declaration chain của P) → D **không** canonical → mọi declaration dựa trên D → `FAIL — evidence` (§13.8–§13.9).

**Declaration không phải authority.** Tách bắt buộc:

```text
tier declaration
≠
authority to classify
≠
validated quality-gate eligibility
```

Một artifact, module, producer, author, hay declaration owner **không** có quyền phân loại tier chỉ vì nó là bên **publish** declaration đó.

**Anti-self-certification:**

- Subject artifact **không** được tự tạo eligibility cho chính nó.
- Producer/owner của artifact **không** trở thành tier authority chỉ bằng việc tự publish declaration.
- Self-classification **invalid**, trừ khi được **backing** bởi một canonical designation resolve độc lập, **explicitly authorize** đúng actor đó cho đúng scope đó.
- Declaration ownership (ai publish declaration) và classification authority (ai có quyền quyết tier) là **hai concern tách biệt** — không suy cái này từ cái kia.

*Không yêu cầu declaration owner và authority phải khác nhau về nhân sự/human identity khi Constitution không đòi hỏi điều đó — rule này nhắm vào **tách authority**, không phải cơ chế định danh cá nhân. Một actor có thể vừa publish declaration vừa là authority **chỉ khi** chính actor đó được canonical designation cấp quyền tường minh cho scope đó — không được suy quyền đó từ việc actor có khả năng publish.*

**Authority chain:**

```text
Canonical authority designation
→ authorized tier classification/declaration
→ exact resolved tier
→ applicable floor/gates
→ evaluation
→ immutable evidence
```

Declaration **không được tự tạo ra upstream designation của chính nó** — nếu declaration là bằng chứng duy nhất cho cả nội dung tier lẫn quyền tạo ra nội dung đó, chain sụp về đúng failure scenario ở đầu mục này.

**Evidence và validator:** provenance của canonical authority phải được pin vào immutable gate evidence và validator phải verify đúng chain này — xem **§13.9 (refined)**. Mục này không lặp lại field list, tránh duplicate.

**Authority boundary.** Mục này chỉ khóa **authority contract cho quality-tier designation**, nằm trong phạm vi Chapter 13 đã có ở §13.13 (quality dimensions, gate categories, evidence contract, tier-resolution authority requirement). Nó **không**:
- định nghĩa lại module identity/taxonomy ([Chapter 7](./07-module-taxonomy.md));
- định nghĩa lại plugin permission grant ([Chapter 9 §9.6](./09-plugin-model.md));
- định nghĩa lại compatibility policy authority ([Chapter 10 §10.4.3](./10-compatibility-capability-contract.md));
- định nghĩa lại phase approval ([Chapter 12](./12-approval-gates.md));
- tạo competing current-state authority với [MANIFEST](../MANIFEST.md) ([I-12](./02-platform-invariants.md));
- sửa governance review eligibility ([Chapter 0 §3](./00-governance.md), [Chapter 11 §11.5](./11-adr-process.md)).

Phân tầng **Declaration → Grant/Designation → Enforcement → Verification** ở [Chapter 9 §9.6](./09-plugin-model.md)/[Chapter 10 §10.4.3](./10-compatibility-capability-contract.md) chỉ được dùng ở đây như **pattern tham khảo cho tính nhất quán** — authority contract của mục này **tự đứng độc lập** (self-contained) trong Chapter 13, không tạo dependency mới và không mượn authority của hai chapter đó.

### 13.4.2 Canonical ownership-binding authority — owned executable artifact

Nhánh 2 của tier-resolution chain (§13.4) cho phép executable artifact **inherit** tier của canonical owning module, và đòi ownership relationship phải "explicit · resolvable · versioned/pinned". Mục này khóa **authority contract** đứng sau yêu cầu đó — nếu không, một producer có thể tự gán artifact của mình vào module có tier floor thấp nhất mà không ai xác nhận binding đó hợp lệ:

```text
Producer P tạo executable artifact A
P tự tạo ownership declaration O: "A thuộc Frontend"
Frontend hợp lệ resolve Tier 3
A inherit Tier 3
coverage floor còn 60%
```

**Ownership relationship là authority-bearing fact, không phải nhãn tự khai.** Với mọi artifact dùng nhánh 2:

- ownership relationship (artifact → owning module) tự thân là một **fact cần authority**, không phải thứ đúng ngầm chỉ vì có ai đó ghi nó ra;
- phải resolve được **đúng một** canonical ownership-binding authority cho scope áp dụng (ví dụ theo artifact class, theo owning-module class);
- authority đó phải **tồn tại trước** gate evaluation, **explicit · versioned · pinned**, scope tường minh;
- authority **không resolve được** hoặc **có nhiều authority cạnh tranh cho cùng scope** → **fail-closed** (§13.8), không tự chọn một trong số đó.

**Canonical status của ownership-binding authority phải thỏa đúng [Canonical establishment predicate](#1341-canonical-tier-designation-authority--standalone-executable-artifact) đã khóa tại §13.4.1** — không lặp lại điều kiện ở đây, tránh duplicate.

**Ownership declaration không tạo ra ownership authority.** Tách bắt buộc:

```text
ownership declaration ("A thuộc module M")
≠
authority to bind A vào M
≠
inherited tier eligibility
```

**Anti-self-selection:**

- Artifact producer/owner **không** được tự chọn module có lợi (tier thấp/floor nhẹ) chỉ bằng cách publish một ownership declaration.
- Binding chỉ hợp lệ khi được **authorize** bởi canonical ownership-binding authority của đúng scope đó — không suy quyền đó từ việc producer có khả năng publish declaration.
- Declaration ownership (ai publish declaration) và authority để bind artifact vào module (ai có quyền quyết binding) là **hai concern tách biệt**.

**Ownership-binding chain:**

```text
Canonical ownership-binding authority designation
→ authorized ownership declaration/binding
→ exact canonical owning-module identity
→ inherited resolved tier (từ module-registry, Chapter 7)
→ applicable floor/gates
→ evaluation
→ immutable evidence
```

**Evidence và validator:** provenance của ownership-binding authority phải được pin vào immutable gate evidence và validator phải verify đúng chain này — xem **§13.9 (refined)**. Mục này không lặp lại field list.

**Authority boundary.** Mục này chỉ khóa **authority contract cho việc bind artifact vào module đã tồn tại sẵn trong Chapter 7 taxonomy** — nó **không** định nghĩa lại module identity/taxonomy/`module-registry.yaml` ([Chapter 7](./07-module-taxonomy.md)); Chapter 7 vẫn là authority duy nhất cho "module nào tồn tại, thuộc type nào". Mục này chỉ thêm lớp "ai có quyền tuyên bố artifact X thuộc về module M đã tồn tại đó" — **layered on top of**, không thay thế, Chapter 7. Cùng các giới hạn với [§13.4.1](#1341-canonical-tier-designation-authority--standalone-executable-artifact): không định nghĩa lại [Chapter 9 §9.6](./09-plugin-model.md), [Chapter 10 §10.4.3](./10-compatibility-capability-contract.md), [Chapter 12](./12-approval-gates.md); không tạo competing authority với [MANIFEST](../MANIFEST.md) ([I-12](./02-platform-invariants.md)); không sửa governance review eligibility ([Chapter 0 §3](./00-governance.md)/[Chapter 11 §11.5](./11-adr-process.md)).

**Cross-branch authority parity (§13.4).** Sau §13.4.1–§13.4.2, cả ba nhánh tier-resolution đều có bảo vệ tương đương — không nhánh nào cho phép producer tự chọn nhánh dễ nhất bằng metadata tự tạo:

| Nhánh | Authoritative identity | Authoritative mapping/binding | Fail-closed nếu unresolved |
|---|---|---|---|
| 1 — Runtime module | `module-registry.yaml` entry ([Chapter 7 §7.5](./07-module-taxonomy.md), Locked — không tự publish được) | Module → tier mapping tại registry | Có (§13.8) |
| 2 — Owned executable artifact | Canonical ownership-binding authority ([§13.4.2](#1342-canonical-ownership-binding-authority--owned-executable-artifact)) | Artifact → owning module binding | Có (§13.8) |
| 3 — Standalone executable artifact | Canonical tier-designation authority ([§13.4.1](#1341-canonical-tier-designation-authority--standalone-executable-artifact)) | Declaration → tier | Có (§13.8) |

Không có quy tắc "most-specific-wins" hay ưu tiên ngầm giữa các nhánh — mỗi artifact resolve theo đúng một nhánh áp dụng (§13.4 mục 1–4); zero hoặc multiple applicable authority trong cùng scope đều fail-closed, không tự chọn.

## 13.5 Invariant conformance gate

Với mỗi artifact trong scope, **các Platform Invariant áp dụng phải pass đúng Verification mà [Chapter 2](./02-platform-invariants.md) đã định nghĩa**. Chapter 13 **không định nghĩa lại** verification của invariant — nó **gom chúng làm required evidence**.

| Invariant | Áp cho (điển hình) | Evidence (theo Verification của Ch2) |
|---|---|---|
| I-1 Explainability | Decision Pipeline | Trace-completeness **100%** (không phải mẫu) |
| I-2 Decision Parity | Decision Pipeline, 4 execution mode | Golden event-log test · canonical semantic-decision hash |
| I-3 No Repaint / Look-Ahead | Compute Engine theo thời gian | Look-ahead audit test (bitemporal, [Chapter 5](./05-time-model.md)) |
| I-4 Strategy Isolation | Strategy/Decision/Risk/Execution | Static dep scan · network-policy · credential audit |
| I-5 Observable Dependency | Decision Pipeline | Self-contained replay (materialize + checksum, cắt mạng) |
| I-6 Fail-Safe by Scope | Engine/Projection/Runtime Service | Fault injection theo scope + risk-not-increased assertion |
| I-7 Plugin Non-Bypass | Plugin | Contract compliance · ACL/schema/command/capability check |
| I-8 Kill Switch | Risk Gateway, Execution, Adapter | Cross-exchange dependency fault test |
| I-9 Numerical Precision | Ledger, Execution, Risk Gateway | Lossless-ingestion · quantization-boundary · property-based |
| I-10 Idempotent Execution | Execution, Adapter | Chaos (lost response/timeout) · aggregate economic-effect |
| I-11 Secrets & Custody | Toàn hệ thống (Execution/Adapter) | Access-control audit |
| I-12 Single Source of Truth | Mọi derived representation | Rebuild/đối chiếu từ authoritative source |
| I-13 State Transition Integrity | Entity có state machine | Property-based transition · illegal/terminal/concurrent test · replay reconstruction |

*Applicability của từng invariant theo `Scope` mà chính invariant khai báo — Chapter 13 không nới rộng scope invariant.*

## 13.6 Test category requirements (risk-based)

Test category **required khi áp dụng** cho responsibility/tier của artifact — không blanket-mandate mọi category cho mọi artifact.

| Category | Bắt buộc khi | Evidence gom về |
|---|---|---|
| Unit + coverage | Mọi module | §13.3–§13.4 |
| Property-based | Numerical/state-machine boundary | I-9, I-13 |
| Invariant / conformance | Invariant áp dụng cho artifact | §13.5 |
| Parity | Decision-pipeline (Tier 1) | I-2 |
| Deterministic replay | Artifact dùng trong Replay/Decision | I-2, I-3, I-5 |
| Chaos / fault-injection | Tier 0; risk/execution boundary | I-6, I-8, I-10 |
| Performance benchmark | Artifact có perf budget (§13.7) | §13.7 |
| Security | Isolation/custody boundary | I-4, I-11 |
| Data-quality | Ingestion, financial value | I-9 |
| Schema/contract compatibility | Published contract/schema thay đổi | [Chapter 10 §10.3](./10-compatibility-capability-contract.md) |
| Migration / rollback | Migration artifact | I-13; Chapter 10 |
| Observability | Module vào production path | §13.2; Phase 1.5/9 |

## 13.7 Performance gate — baseline, budget, ownership

Không được merge nếu benchmark **regress vượt budget** so với **baseline đã pin**.

- **Baseline:** reference đã pin (commit của baseline đã merged/approved trên integration branch), **không** mơ hồ "lần chạy trước".
- **Budget:** ngưỡng regression cho phép phải được **khai báo tường minh và có owner** (Module Owner cho module-level benchmark). Budget phải được **định nghĩa và chấp nhận trước khi** gate dùng nó — cùng nguyên tắc "criteria defined before used" của [Chapter 12 §12.1](./12-approval-gates.md).
- **Reproducibility:** measurement phải pin environment, dataset, và configuration; kết quả không reproducible → coi như evidence không hợp lệ (§13.8).
- **Noise handling:** so sánh phải ổn định thống kê (ví dụ median/percentile over N runs + margin), **không** kết luận regression từ một lần chạy đơn lẻ (tránh flaky, §13.10).
- **Ngoài phạm vi:** benchmark harness, ngưỡng số cụ thể, và perf của Backtest ở quy mô dữ liệu lớn ([Chapter 3 §3.3](./03-engineering-principles.md) backlog) defer Phase 1.5 — chương này khóa contract, không chốt số.

## 13.8 Fail-closed semantics

Gate **fail-closed**. Gate = **FAIL** khi bất kỳ điều nào sau đây:

- applicability không xác định được;
- required evidence thiếu;
- evidence không resolve/pin được về subject identity/version/config cụ thể;
- measurement không reproducible.

**Missing gate ≠ passed gate.** Nhất quán [Chapter 12 §12.2](./12-approval-gates.md): **fail-closed = eligibility incomplete**, **không** phải reviewer veto và **không** phải Product Owner rejection.

### 13.8.1 Bounded-measurement reproducibility for `UNSTABLE_TIMEOUT_TRIAGE` populations

This subsection is the **sole normative source** for bounded-uncertainty
Quality-Gate measurement/applicability/precedence/result semantics for the
narrow class of populations defined below — it is self-contained and can
be read and applied correctly without reference to any ADR (§13.13).
`docs/adr/ADR-044.md` records the architecture rationale, alternatives,
and consequences for this rule, but carries no second, independently
executable copy of it; if ADR prose and this subsection ever appear to
disagree, **this subsection controls Quality-Gate semantics**.

Ordinary §13.8 fail-closed semantics require measurement to be
reproducible. A governed, closed-scope timeout-triage classification
procedure (defined structurally under "Protocol provenance" below) MAY
leave a bounded population of individually-unresolved
`UNSTABLE_TIMEOUT_TRIAGE` classifications — a deliberate property of any
qualifying such procedure (no majority vote, no forced tie-break, no
retry-until-green). This subsection defines exactly how a Quality Gate
consumes such a population: which mutants may enter it (Applicability),
what "reproducible" means at two distinct layers (Reproducibility
reconciliation), how it relates to Testing Convention item 8's per-mutant
rule (Evidence-layer precedence), the exact arithmetic (Formal bound
definitions), and the resulting gate-level outcome (Result semantics).

**A. Applicability — closed predicate.** This subsection applies to a
Quality Gate evaluation **only when ALL of the following hold**:

```text
1. The Quality Gate is a mutation/test-effectiveness gate using the
   authoritative Ride mutation metric, denominator, and threshold
   pinned by that gate's own Quality-Gate evidence per §13.9 (current
   approved source: Testing Convention v0.17 item 7's Ride-owned
   mutation-effectiveness metric contract — this subsection depends on
   whichever Testing Convention version/item is actually pinned by that
   evidence, never a hard-coded item number that could silently drift
   under future renumbering).
2. Every mutant admitted to U carries the exact governed classification
   UNSTABLE_TIMEOUT_TRIAGE — no other status is admitted to U.
3. That classification was produced by a procedure satisfying every
   structural property in "Protocol provenance" below, pinned at the
   evaluation boundary — never a different or self-declared-equivalent
   mechanism.
4. Every U member remains counted in the gate's authoritative
   denominator — no silent exclusion.
5. U is disjoint from the confirmed-favorable numerator:
   U ∩ confirmed_favorable = ∅.
6. No other unresolved, ambiguous, or evidence-integrity status is
   folded into U.
```

**Explicitly outside this subsection's scope** — these remain governed
solely by ordinary §13.8/§13.9, and never receive bounded-uncertainty
treatment merely by analogy or convenience: `AMBIGUOUS — EVIDENCE
INSUFFICIENT`, `TOOL_IDENTITY_DRIFT`, `not_checked`, any unresolved
identity/provenance defect, missing evidence, unpinned evidence, and any
other unresolved/ambiguous category not separately, explicitly brought
into this subsection's own governed scope by a future amendment to this
chapter.

**Mixed-population rule.** If an evaluation's mutant population contains
BOTH (a) `UNSTABLE_TIMEOUT_TRIAGE` entries eligible for `U` under the
predicate above AND (b) any other unresolved or evidence-integrity defect
outside this subsection's scope, that other defect MUST be dispositioned
under its own governing authority (§13.8/§13.9, or whatever authority
governs that specific defect class) **before** this subsection may emit
any final result from the scoped `U`. The non-scoped defect never
disappears inside the bounded interval, and a `Case B` `PASS` computed
from the scoped `U` must never be read as, or substitute for, resolving a
separate `FAIL — evidence` condition arising from the non-scoped defect —
that `FAIL — evidence` stands on its own authority and controls the
overall gate result independently of this subsection's own Case A/B/C
outcome.

**Protocol provenance — structural requirement, no self-declared
equivalence.** No separate, named "canonical protocol" document exists in
this repository today beyond the Feature Engine's own formal Quality-Gate
evidence — this subsection does not invent one. Instead, a qualifying
classification procedure is defined **structurally**: evidence for a
mutant's `UNSTABLE_TIMEOUT_TRIAGE` membership in `U` must demonstrate,
pinned at the evaluation boundary (§13.9):

```text
- the exact procedure's own identity/content, pinned (e.g. the exact
  evidence artifact/section defining it);
- exactly two qualifying independent reproductions of that mutant;
- each reproduction performed under fresh regeneration/isolation
  properties required by the governing evaluation contract (no reused
  workspace, no shared state between the two reproductions);
- the exact outcome of each of the two runs, individually recorded;
- a disagreement between the two runs' outcomes produces
  UNSTABLE_TIMEOUT_TRIAGE — never resolved by any of the following:
  - no majority vote;
  - no N-of-M resolution;
  - no third-run tie-break;
  - no retry-until-green.
```

Any procedure meeting all of the above structural properties qualifies —
this is a property test, not a reference to one specific named artifact.
For the current Feature Engine `P3-FEATURE-QG-EVID-03` application (as of
this chapter's authoring), `feature-engine-mutation-step9-formal-
evidence-005.json`'s own `timeout_triage` record and `feature-engine-
mutation-step9-formal-evidence-005-correction-001.json` together document
one procedure satisfying these properties — cited here as the current,
non-normative illustration of the structural requirement, never as itself
the defining authority. No validator, evaluator, or executor may infer,
assume, or self-declare that a *different* procedure satisfies these
properties without that determination itself being pinned as part of the
evidence for that evaluation; and no future, materially different
procedure may be treated as qualifying merely by an executor's own
assertion of equivalence — establishing that requires a separately
governed, Product-Owner-approved authority decision recorded before the
relevant evaluation boundary.

**B. Reproducibility reconciliation.** Ordinary §13.8 requires
"measurement" to be reproducible. This subsection distinguishes two
separate reproducibility questions, both of which apply to every
`§13.8.1`-eligible evaluation, in every one of Cases A/B/C below:

```text
Per-mutant reproducibility (unchanged, governed exactly as §13.8/§13.9
already require):
  An UNSTABLE_TIMEOUT_TRIAGE mutant remains individually unresolved.
  Its own killed/survived/confirmed-timeout classification is NEVER
  treated as reproduced, resolved, or inferred, in Case A, B, or C
  alike.

Gate-level bounded-measurement reproducibility (the semantic this
subsection defines):
  When every authoritative interval input (confirmed-favorable
  numerator, U, denominator, T, criteria/policy version, evaluation
  boundary) is immutable and pinned per §13.9, the derived interval
  [lower_score, upper_score] (Formal bound definitions below) is itself
  a deterministic, reproducible function of those pinned inputs.

  The reproducibility of the interval does NOT imply, and must never be
  read to imply, reproducibility of any individual U member's own
  classification.
```

**Precedence with §13.8.** For a population satisfying the Applicability
predicate (A) above, §13.8's "measurement không reproducible → FAIL" rule
is evaluated against the **gate-level bounded measurement** this
subsection defines — not against any individual unresolved `U` member's
own per-mutant status. An unresolved `U` member does not, by itself, make
the bounded measurement non-reproducible when every required bound input
is valid and pinned per §13.9; the bounded measurement's own
reproducibility (defined above) is what §13.8 asks for at the gate level.
This refinement of §13.8's "measurement not reproducible" trigger exists
**only inside this subsection's own closed scope** (Applicability, A,
above) — outside that scope, ordinary §13.8 semantics apply completely
unchanged, with no refinement of any kind.

**C. Evidence-layer precedence — Testing Convention item 8.** Testing
Convention item 8's per-mutant timeout rule ("an unresolved/unreproduced
timeout is `FAIL — evidence` for that mutant") is a **per-mutant evidence
disposition** — preserved exactly, never rewritten, never treated as
resolved by this subsection. For an evaluation satisfying the closed
Applicability predicate (A) above, that per-mutant disposition:

```text
- remains attached to that mutant, unchanged;
- grants zero favorable effectiveness credit to that mutant;
- does not resolve that mutant's own classification;
- does NOT, by itself, independently force a final gate-level
  FAIL — evidence result.
```

The gate-level outcome for such a population is determined by this
subsection's own Case A/B/C (Result semantics, below) — **unless** a
separate, non-scoped evidence defect independently triggers ordinary
§13.8/§13.9 (Mixed-population rule, above), in which case that defect's
own `FAIL — evidence` controls regardless of this subsection's own Case
A/B/C result. This precedence exists specifically so that the same exact
evidence set can never simultaneously yield both a `Case B` `PASS` and a
final gate-level `FAIL — evidence`.

**D. Formal bound definitions**, reusing — never replacing — the gate's
own already-authoritative metric/denominator/threshold (no new metric, no
denominator change; threshold `T` is expressed as a percentage, so both
bounds are computed in the same percentage units):

```text
lower_numerator = confirmed favorable numerator
upper_numerator = lower_numerator + U        (U = count of eligible
                                                UNSTABLE_TIMEOUT_TRIAGE
                                                mutants, per the closed
                                                applicability predicate)
denominator      = the gate's existing authoritative denominator,
                    unchanged — every U member remains counted in it,
                    no silent exclusion
lower_score      = (lower_numerator / denominator) × 100   [percent]
upper_score      = (upper_numerator / denominator) × 100   [percent]

U ∩ confirmed_favorable = ∅   (disjointness, restated from Applicability
                                condition 5 for the arithmetic's own
                                self-sufficiency)
```

If the gate's own already-authoritative metric internally uses a
different normalized representation, that representation's exact
semantics are preserved — but `lower_score`, `upper_score`, and `T` are
always compared in identical units (percent, as defined above).

**E. Result semantics**, given the gate's own required threshold `T`, for
any evaluation satisfying the Applicability predicate above. Cases A and
B are **final Quality-Gate results** — the same `FAIL — criteria`/`PASS`
vocabulary §13.9's existing `Result semantics` block already defines,
unchanged, un-extended. **Case C is not a fourth final result — it is an
evaluation state.** This subsection does not add a fourth entry to
§13.9's `FAIL — criteria` / `FAIL — evidence` / `PASS` taxonomy:

```text
Case A — upper_score < T         -> FINAL RESULT: FAIL — criteria
Case B — lower_score >= T        -> FINAL RESULT: PASS
Case C — lower_score < T <= upper -> EVALUATION STATE: STOPPED / UNRESOLVED
                                      (NO final result emitted)
```

Required interpretation, binding for every evaluation satisfying the
Applicability predicate:

- **Case A (`FAIL — criteria`, final result)** is authorized only when
  authoritative bounded measurement proves that even the best-case
  resolution of every unresolved mutant cannot meet `T` — i.e. genuine
  §13.8-style fail-closed criteria-failure, established with certainty
  despite per-mutant uncertainty, not a guess.
- **Case B (`PASS`, final result)** is authorized only when `T` is met
  granting **zero** favorable credit to any unresolved mutant — a `PASS`
  under this subsection never relies on unresolved evidence, consistent
  with §13.10's "unstable evidence is never credited as passing evidence,"
  and never masks a separate non-scoped `FAIL — evidence` condition
  (Mixed-population rule above).
- **Case C (`STOPPED / UNRESOLVED`, evaluation state — NOT a final
  result)** applies whenever the unresolved classifications could still
  change the verdict. No `PASS`/`FAIL` is authorized or emitted. The
  bounded interval itself may be entirely valid, pinned, and reproducible
  per §13.9 — reproducibility of the *measurement* does not resolve the
  *threshold question*, since current evidence genuinely does not
  determine whether the eventual criteria outcome is PASS or FAIL. Gate
  eligibility under §13.1/§13.8 remains **incomplete**, and the gate
  remains **fail-closed** — exactly the existing "**Missing gate ≠ passed
  gate**" principle (§13.8), applied here without redefining Product Owner
  approval authority or Chapter 12's own decision authority. A downstream
  Approval Gate prerequisite requiring `PASS` (Chapter 12 §12.2(5)) is
  **not satisfied** by a Case C state — `not PASS → cannot satisfy an
  Approval-Gate prerequisite requiring PASS`. Case C's own bounded
  measurement is explicitly **not** relabeled `FAIL — evidence` merely
  because it produced no final result — that label is reserved for
  genuinely missing/invalid/unresolvable evidence (§13.9's existing
  taxonomy), and Case C's evidence, by construction, is none of those; it
  is complete, pinned, and reproducible evidence that simply does not
  yet determine a final criteria outcome.
- In all three cases, the unresolved mutants' own individual
  classifications remain exactly as unresolved as the governing per-mutant
  protocol left them — this subsection never resolves, infers, or credits
  them individually, in Case C no less than in A or B.

**Resume / follow-up (Case C only).** A later evaluation may reach a final
result only after a separately governed action changes the authoritative
inputs relevant to the interval — for example: legitimate resolution or
remediation of the underlying unresolved cases under an authorized
protocol; a new authoritative measurement/evidence boundary; or other
separately governed remediation. This subsection does not itself prescribe
which such mechanism applies to any given Case C — that remains a future,
separately governed determination. It explicitly does NOT authorize, as a
way to leave Case C: majority vote, N-of-M voting, an arbitrary third-run
tie-break, retry-until-green, or denominator manipulation — all remain
prohibited exactly as in Case A/B.

**Explicit constraints (binding on every §13.8.1-eligible gate
evaluation):**

- no majority vote; no N-of-M voting; no arbitrary third-run tie-break; no retry-until-green (§13.10, unchanged);
- no denominator manipulation — the authoritative denominator is reused exactly as already established for that gate, never altered to change the interval;
- no automatic test-level quarantine triggered by mutation-classification instability alone — §13.10's own quarantine trigger (evidence a specific *test* is itself flaky/timing-dependent) remains a distinct, separately-evidenced concern from this subsection's gate-interpretation mechanism; neither implies the other;
- §13.9's evidence/pinning rules apply to every input used to derive the interval (numerator components, `U`, denominator, `T`, policy version, evaluation boundary) — this subsection creates no exemption from §13.9;
- **no historical evidence rewrite and no retroactive reinterpretation of any prior gate evaluation** — a prior gate's own recorded `PASS`/`FAIL`/`STOPPED` result is never silently reclassified by this subsection's later existence or by any change to this chapter's own controlling version (recorded in MANIFEST, per I-12).

This subsection does not itself select, or make effective, any specific
per-mutant timeout-triage protocol — it governs only how a gate consumes
the *output* of a procedure satisfying "Protocol provenance" above.

## 13.9 Evidence contract — pinning & reproducibility

Quality-gate evidence là **immutable, resolvable artifact** (cùng tinh thần Compatibility Result bất biến, [Chapter 10 §10.4](./10-compatibility-capability-contract.md); và review-evidence pinning, [Chapter 0 §3](./00-governance.md)). Mỗi evidence entry phải pin tối thiểu:

- **subject identity + version/artifact/config** — theo exact-artifact rule ([Chapter 10 §10.8](./10-compatibility-capability-contract.md)); **cấm** mutable reference như nhãn `latest`/`live-default`;
- **criteria/policy version** đã áp dụng;
- **evaluator/authority** đã đánh giá (quyền đánh giá là grant, không tự nhận — [Chapter 9 §9.6](./09-plugin-model.md));
- **measurement boundary/time**;
- **input data/config identity** đủ để reproduce.

**Tier-resolution provenance — bắt buộc khi tier ảnh hưởng gate applicability hoặc coverage floor.** Khi applicable tier quyết định gate có áp hay không, hoặc quyết định coverage floor (§13.4, §13.12 nhóm B), evidence entry phải pin đầy đủ **authoritative tier-resolution provenance tại evaluation boundary** — áp **exact-pin pattern tương đương** [Chapter 10 §10.8](./10-compatibility-capability-contract.md) cho quality-tier (**không** duplicate Chapter 10):

- **`tier_resolution_branch`** — đúng một trong: `runtime module` · `owned executable artifact` · `standalone executable artifact` (§13.4).
- **Ownership provenance** (nếu dùng inheritance, nhánh 2) — phải pin đủ **canonical ownership-binding authority-chain evidence** ([§13.4.2](#1342-canonical-ownership-binding-authority--owned-executable-artifact)), tối thiểu:
  - **canonical ownership-authority identity** — authority nào được designate cho scope này;
  - **authority version/content identity** — immutable, không dùng nhãn mutable;
  - **authority scope**;
  - **authority owner/designation basis** — bằng chứng thỏa [Canonical establishment predicate](#1341-canonical-tier-designation-authority--standalone-executable-artifact) (§13.4.1);
  - **exact ownership declaration identity/content**;
  - **identity của actor được authorize để declare/bind ownership** — actor này phải resolve **từ chính canonical ownership-authority**, không suy từ việc actor là bên publish declaration;
  - **exact artifact identity/version**;
  - **canonical owning-module identity**;
  - **exact `module-registry` entry/version** ([Chapter 7 §7.5](./07-module-taxonomy.md));
  - **bằng chứng authority và binding đều applicable tại evaluation boundary** — không resolve lại từ mutable/current state về sau.
- **Tier source (exact):**
  - runtime module → exact `module-registry` **version/content identity** + exact module entry/reference đã dùng;
  - owned executable artifact → tier source resolve **gián tiếp qua canonical owning-module identity** đã pin ở bullet **Ownership provenance** trên — không lặp lại;
  - standalone executable artifact → phải pin đủ **canonical authority-chain evidence** ([§13.4.1](#1341-canonical-tier-designation-authority--standalone-executable-artifact)), tối thiểu:
    - **canonical designation identity** — authority nào được designate cho scope này;
    - **designation version/content identity** — immutable, không dùng nhãn mutable;
    - **designation scope** — phạm vi mà designation đó áp dụng;
    - **designation authority owner** — ai đứng sau canonical designation đó;
    - **exact tier declaration identity/content** — nội dung declaration đã dùng;
    - **identity của actor được authorize để classify/declare** — actor này phải resolve **từ chính canonical designation**, không suy từ việc actor là bên publish declaration;
    - **canonical-establishment evidence** — reference chứng minh canonical designation đã thỏa [Canonical establishment predicate](#1341-canonical-tier-designation-authority--standalone-executable-artifact) (governance-approval basis + resolvable authoritative project state), độc lập với chính declaration chain của subject;
    - **bằng chứng designation và declaration đều applicable tại evaluation boundary** — không resolve lại từ mutable/current state về sau.
- **Resolved tier result:** resolved tier value · applicable coverage floor **derive từ tier đó** · criteria/policy version định nghĩa floor.
- **Evaluation boundary:** evidence phải chứng minh các reference trên là **authoritative tại thời điểm gate evaluation**, **không** resolve lại từ mutable/current state về sau.

**Historical immutability.** Thay đổi về sau đối với **designation authority, ownership authority, classifier authorization, ownership binding, tier declaration, registry, hoặc policy** **không** được reinterpret historical `PASS`/`FAIL`; nếu cần đánh giá lại thì **sinh gate evaluation mới**, còn evidence cũ **giữ nguyên** resolution chain (kể cả canonical authority chain, [§13.4.1](#1341-canonical-tier-designation-authority--standalone-executable-artifact)/[§13.4.2](#1342-canonical-ownership-binding-authority--owned-executable-artifact)) đã pin.

**Validator** phải verify **canonical authority chain đã pin** cho cả tier-designation authority ([§13.4.1](#1341-canonical-tier-designation-authority--standalone-executable-artifact)) lẫn ownership-binding authority ([§13.4.2](#1342-canonical-ownership-binding-authority--owned-executable-artifact)) — reject **self-established designation authority**, reject **self-established ownership authority**, reject **unauthorized classifier**, reject **unauthorized ownership binder**, reject **zero hoặc multiple applicable authority cho cùng scope**, reject **authority hết hạn/future/out-of-scope**, reject **mutable hoặc unresolved reference**, reject **authority chain phụ thuộc current/mutable state khi validate historical evidence**. Mọi trường hợp trên → `FAIL — evidence`, không phải pass mặc định. Validator **không** infer, **không** default, **không** tạo authority, **không** chọn module/tier/authority có lợi, **không** tự trở thành authority ([Chapter 11 §11.9](./11-adr-process.md)).

**Result semantics** phân biệt (theo [Chapter 10 §10.4.2](./10-compatibility-capability-contract.md)):

```text
FAIL — criteria    : đã đo, không đạt tiêu chí
FAIL — evidence    : thiếu/invalid/không resolve được (KHÔNG khẳng định "đã chứng minh fail")
PASS               : đạt tiêu chí, evidence đầy đủ và pinned
```

Evidence được **versioned + retained**, không ghi đè lịch sử (cùng nguyên tắc [Chapter 10 §10.4.4](./10-compatibility-capability-contract.md)). Current state/version của artifact vẫn resolve từ **MANIFEST** theo [I-12](./02-platform-invariants.md) — Chapter 13 **không** tạo state store cạnh tranh.

## 13.10 Flaky test policy

Một test cho kết quả **không ổn định trên cùng input đã pin** là tín hiệu hoặc (a) vi phạm determinism (I-2/I-3), hoặc (b) test defective. Quy tắc:

- **Cấm retry-until-green** để đưa gate về pass — điều này che đúng loại determinism defect mà I-2/I-3 tồn tại để bắt.
- Test phụ thuộc timing/ordering/clock phải **quarantine** và ghi **explicit follow-up** (MANIFEST/backlog, theo pattern [Chapter 12 §12.4-B](./12-approval-gates.md)).
- Trong lúc còn flaky, test đó **không được tính là passing evidence** cho invariant nó tuyên bố verify.
- Quarantine tooling defer Phase 1.5.

## 13.11 Exception / waiver process

Waiver là một **exception được ghi lại**, **không** phải một cách để pass gate. Nó không thay đổi kết quả kỹ thuật của gate.

- **Waiver không thay đổi gate result.** Một gate `FAIL`/`BLOCKED` **vẫn là** `FAIL`/`BLOCKED` sau khi có waiver — waiver **không** biến `FAIL`/`BLOCKED` thành `PASS`.
- **Waiver không thỏa một prerequisite yêu cầu `PASS`.** Vì [Chapter 12 §12.2(5)](./12-approval-gates.md) yêu cầu applicable quality gates **thực sự PASS**, artifact đang mang **open waiver không đủ eligibility** cho Chapter 12 Approval Gate.
- **Phạm vi của "proceed":** chỉ áp dụng cho **bounded artifact-level activity không yêu cầu gate PASS** (ví dụ tiếp tục development/experiment trong scope của artifact). Waiver **không** mở đường cho **phase approval** hay **phase transition** — cả hai **vẫn bị chặn** cho tới khi applicable Quality Gate **thực sự PASS**.
- **Waiver phải bounded:** scope + expiry + rationale + owner, và được **pin làm evidence** (§13.9). Downstream phải thấy artifact đang mang **open waiver**, không bị ẩn thành pass.
- **Product Owner là sole risk-acceptance và approval authority** (mô hình `Chấp nhận rủi ro` của [Chapter 0 §3](./00-governance.md)); reviewer/validator **không** cấp waiver và **không** có quyền approve.
- **Waiver không bypass Locked invariant:** nếu required verification của một invariant fail, đây là **governance matter** ([Chapter 0](./00-governance.md)) — waiver chỉ ghi lại rủi ro có tài liệu được PO chấp nhận, **không** tự cho phép vi phạm invariant.
- Không thiết kế chi tiết deployment/environment policy ở đây; waiver storage format defer Phase 1.5.

## 13.12 Gate applicability — gate nào áp cho artifact nào

Applicability phải **khai báo được và resolvable**. Gate được phân theo **điều kiện kích hoạt**, **không** phải "mọi runtime module gánh mọi gate" — cụ thể, performance / security / observability **không** mặc định áp cho mọi runtime module, mà chỉ khi trigger tương ứng thỏa.

**A. Universal — mọi artifact trong scope:**
- **invariant conformance** cho các invariant **áp dụng** theo `Scope` do chính invariant khai báo (§13.5).

**B. Executable-implementation-triggered — coverage:**
- **line coverage**, **branch coverage** (theo rule deterministic §13.3), và **test-effectiveness evidence** (§13.3).
- **Trigger** (phải thỏa **cả ba**): artifact có **authoritative executable implementation** + **resolvable coverage boundary** + **resolvable applicable tier** (resolve theo **tier-resolution chain §13.4** — áp cho cả module lẫn executable non-module artifact).
- **Coverage KHÔNG universal.** Artifact **không có executable implementation** → coverage **không applicable** → artifact đó **không bị bắt** tạo line/branch coverage hay test-effectiveness evidence.

  Phân biệt bắt buộc:

  ```text
  coverage not applicable            ≠   coverage applicable but evidence missing
  (không executable implementation)      (đã thỏa trigger B mà thiếu metric/evidence)
        → coverage gate không áp             → FAIL — evidence (§13.8–§13.9)
  ```

  - **Không silently skip:** artifact **có** executable implementation nhưng **coverage boundary hoặc tier chưa resolve** → **không** được bỏ qua coverage; đây là **undefined applicability → fail-closed** (§13.8), không phải "not applicable".

**C. Tier-triggered — theo criticality tier (§13.4):**
- **Chaos Test** → Tier 0;
- **Parity Test** → Tier 1 (decision-pipeline responsibility);
- tier cũng đặt coverage floor (chỉ áp khi coverage đã trigger theo B).

**D. Responsibility / boundary-triggered — theo bản chất trách nhiệm của artifact:**
- **Security** → khi artifact có **isolation / custody / authorization boundary** (I-4, I-7, I-11);
- **Data quality / numerical precision** → khi artifact **xử lý authoritative hoặc financial data** (I-9, I-13);
- **Performance** → khi có **authoritative performance budget** áp dụng cho artifact (§13.7);
- **Observability** → khi artifact nằm trên **production / operational path**.

**E. Lifecycle-triggered — theo loại thao tác/vòng đời:**
- **Schema / contract compatibility** → khi artifact **publish** contract/schema ([Chapter 10 §10.3](./10-compatibility-capability-contract.md));
- **Migration / rollback validation** → khi artifact là **migration** (I-13; Chapter 10).

**Artifact-class rollup** (mọi class đều chịu A; các trigger B–E áp khi thỏa):
- **Runtime module** → A + **B executable coverage** (module có executable implementation) + C tier-triggered + các boundary-trigger (D) *thỏa* cho module đó (một Type 1 Compute Engine thuần không có custody boundary sẽ **không** gánh security gate chỉ vì nó là module);
- **Published contract / schema** → A + E compatibility. **Không inherit coverage (B)** chỉ vì thuộc scope — contract/schema không phải executable implementation;
- **Release / build** → **chỉ roll up** gate results của các constituent artifact + performance (nếu có budget) + operational readiness (nếu vào production path); release/build **không tự tạo một quality tier riêng** chỉ vì là release/build — trừ khi bản thân release có **standalone executable subject được khai báo riêng** (khi đó subject đó resolve tier theo §13.4);
- **Migration** → A + E migration/rollback + data-quality (nếu chạm authoritative data) + compatibility (nếu đổi schema). Coverage (B) **chỉ** áp khi **chính migration có executable implementation** thỏa trigger B; tier resolve theo §13.4 (executable migration có canonical owning module → inherit tier module; standalone executable migration → cần authoritative tier declaration; **non-executable** migration → coverage **không applicable**; tier không resolve → **fail-closed**);
- **Phase deliverable** → gate set mà **approved phase plan/roadmap** ([Chapter 14](./14-roadmap.md)) khai báo áp dụng.

**Determinism + fail-closed:** cùng một artifact, giải theo cùng bộ trigger A–E, phải cho ra **cùng một gate set**. Nếu một trigger condition **không resolve được** (không xác định được artifact có executable implementation / boundary / tier / budget / path / publish / migration liên quan hay không) → **fail-closed** theo §13.8: applicability chưa xác định = eligibility incomplete, **không** được mặc định "gate không áp dụng" để bỏ qua.

## 13.13 Authority boundary

Chapter 13 sở hữu **quality dimensions, quality gate categories, minimum evidence, pass/fail semantics, risk-based test expectations, measurement rules, evidence contract, exception/waiver handling**. Các authority khác chỉ **tham chiếu, không định nghĩa lại**:

| Concern | Authority |
|---|---|
| Quality criteria / gate / evidence | **Chapter 13 (chương này)** |
| Review eligibility (số lượng, role, no-veto) | [Chapter 0 §3](./00-governance.md) / [Chapter 11 §11.5](./11-adr-process.md) |
| Platform invariants + verification | [Chapter 2](./02-platform-invariants.md) |
| Module taxonomy · module→tier registry | [Chapter 7](./07-module-taxonomy.md) |
| Phase approval orchestration | [Chapter 12](./12-approval-gates.md) |
| Compatibility Result · Capability Matrix | [Chapter 10](./10-compatibility-capability-contract.md) |
| Time / determinism semantics | [Chapter 5](./05-time-model.md) |
| Phase sequence · DoD content | Approved roadmap / phase plan ([Chapter 14](./14-roadmap.md)) |
| Current version/status/state | [MANIFEST](../MANIFEST.md) theo [I-12](./02-platform-invariants.md) |

Chapter 13 chỉ cung cấp **quality-gate eligibility evidence** cho [Chapter 12 §12.2(5)](./12-approval-gates.md) sử dụng. Không tạo competing authority; không đóng OQ-002/OQ-003.

## 13.14 Ngoài phạm vi — defer Engineering Foundation (Phase 1.5)

Chương này khóa **contract**, không chốt **mechanism**. Defer sang Engineering Foundation ([Chapter 3 §3.2](./03-engineering-principles.md)) / Phase 1.5:

- concrete tooling, CI operator, coverage/mutation **ngưỡng số** vượt tier floor;
- benchmark harness và perf threshold cụ thể;
- test framework/style (Testing Convention — [Chapter 3 §3.2](./03-engineering-principles.md) đã park ở đây, không định nghĩa lại);
- quarantine mechanism (§13.10) và waiver storage format (§13.11);
- **storage/schema và filename cụ thể** của **authoritative artifact/quality-tier metadata**, của **canonical tier-designation authority** (§13.4 nhánh 3, [§13.4.1](#1341-canonical-tier-designation-authority--standalone-executable-artifact)), và của **canonical ownership-binding authority** (§13.4 nhánh 2, [§13.4.2](#1342-canonical-ownership-binding-authority--owned-executable-artifact)) — Constitution chỉ khóa *tồn tại + property* của declaration và của authority (explicit, versioned, pinned, có scope/owner, tồn tại trước gate), **không** khóa filename/YAML schema/CI/vendor/technology chọn làm authority;
- **field encoding / storage format** của **tier-resolution provenance** (§13.9) — Constitution khóa *phải pin những gì*, không khóa cách lưu/serialize.
