---
id: 14-roadmap
title: Roadmap
version: "1.5"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-28"
next_review: null
depends_on: ["00-governance", "01-vision", "02-platform-invariants", "03-engineering-principles", "04-domain-principles", "05-time-model", "06-identity-model", "07-module-taxonomy", "08-event-model", "09-plugin-model", "10-compatibility-capability-contract", "11-adr-process", "12-approval-gates", "13-quality-gates"]
---

# 14. Roadmap

> **Trạng thái:** `In Review`. Theo [Chapter 12 §12.3](./12-approval-gates.md) (Locked), khi còn `In Review` chương này được prose-reference như **intended owner** của phase sequence và DoD content, nhưng nội dung draft **chưa phải binding Locked authority**. Các yêu cầu dưới đây chỉ trở thành authoritative phase plan mà [Chapter 12 §12.1–§12.2](./12-approval-gates.md) và [Chapter 13 §13.12](./13-quality-gates.md) tham chiếu **sau khi** Product Owner Approve/Lock.

## 14.1 Phạm vi và thẩm quyền

Chapter 14 sở hữu **phase sequence · nội dung/deliverable của từng Phase · nơi ở và cardinality của Definition of Done (DoD) · khai báo gate set áp cho phase deliverable**.

Chapter 14 **không** sở hữu và **không định nghĩa lại**:

- **cơ chế phase approval** — thuộc [Chapter 12](./12-approval-gates.md) (Locked);
- **quality gate semantics/applicability** — thuộc [Chapter 13](./13-quality-gates.md) (Locked);
- **ADR Scope Rule** — thuộc [Chapter 0 §4b](./00-governance.md) / [Chapter 11](./11-adr-process.md);
- **module taxonomy/dependency graph** — thuộc [Chapter 7](./07-module-taxonomy.md);
- **current version/status/state của tài liệu** — thuộc [MANIFEST](../MANIFEST.md) theo [I-12](./02-platform-invariants.md).

**Đơn vị chịu Approval Gate là `Phase`.** Sub-phase (ví dụ 0.1/0.2/0.3) là **work unit bên trong** một Phase — sub-phase **không** tự mở Approval Gate riêng. `Phase 1.5` là một **Phase** đầy đủ (không phải sub-phase) và có Approval Gate riêng.

### 14.1.1 Canonical Phase-plan model

Nhiều Locked chapter (ví dụ [Chapter 12 §12.3](./12-approval-gates.md), [Chapter 13 §13.12](./13-quality-gates.md)) dùng cụm **"approved phase plan/roadmap"** — cụm này có thể đọc thành hai artifact khác nhau (một "Phase plan" tách biệt, cạnh Roadmap). Mục này khóa dứt điểm: **không tồn tại "Phase plan" như một artifact type riêng, cạnh tranh với Roadmap.**

- **Chapter 14 (chính chương này) là canonical Roadmap duy nhất** của project.
- **Canonical Phase plan của một Phase = đúng phần Phase tương ứng trong Roadmap (§14.2) cộng exact accepted DoD của Phase đó, đã incorporated** ([§14.3.1](#1431-dod-incorporation-vào-canonical-phase-plan)). Đây **không** phải hai nguồn ngang hàng — DoD là **thành phần được incorporate**, không phải một Phase-plan cạnh tranh.
- Cụm "phase plan/roadmap" ở các chapter khác **resolve về đúng một thực thể này** — không phải lựa chọn giữa hai nguồn.
- **Mỗi Phase phải resolve được đúng một canonical Phase-plan content tại evaluation boundary** (Roadmap phase-section version + accepted DoD version). Zero hoặc multiple accepted DoD cạnh tranh cho cùng Phase → **fail-closed** ([§14.3](#143-definition-of-done--cardinality-và-nơi-ở)).
- **Không có implicit precedence** (không "bản mới nhất thắng", không "bản cụ thể hơn thắng") — resolve thất bại thì fail-closed, không tự chọn.
- **Historical Phase decision không được resolve lại từ Roadmap/DoD hiện tại.** Quyết định đã đưa ra tại một boundary vẫn phải tái dựng được với đúng Roadmap-phase-section version + DoD version đã pin tại boundary đó ([§14.4.1](#1441-immutable-phase-decision-bundle)) — thay đổi Roadmap/DoD về sau **không** reinterpret quyết định cũ.

Mô hình này **chấm dứt đệ quy** tại chính Roadmap này (Locked artifact duy nhất mà Chapter 12/13 tham chiếu) cộng DoD acceptance (fact do Product Owner tạo ra qua Decision Workflow, [Chapter 0 §3](./00-governance.md)) — không cần một "Phase-plan-của-Phase-plan" nào khác để tự hợp thức hóa.

## 14.2 Phase sequence

Theo [Chapter 12](./12-approval-gates.md) (Locked): **mọi Phase kết thúc bằng một Approval Gate trước khi Phase kế tiếp bắt đầu — không được nhảy phase.** Sequence dưới đây khai báo Approval Gate cho **mọi** Phase, không có ngoại lệ.

```text
Phase 0 — Vision & Foundation
  0.1  Constitution (Chapter 0–14) + governance activation
  0.2  Domain Model & Domain Contract (/docs/domain/)
       — sub-phase này được tham chiếu bởi Chapter 6 §6.4 (Account first-class)
         và Chapter 7 §7.5 (module-registry placement)
  0.3  Product Requirement · Use Case & Workflow · UX Blueprint
  → ADR cho quyết định Domain thuộc diện ADR Required (Governance §4b, không phải mọi định nghĩa)
  → Approval Gate

Phase 1 — System Architecture
  Software · UX Architecture · Security & Custody Baseline · API · Database · Engine
  → ADR cho quyết định kiến trúc thuộc diện ADR Required (Governance §4b)
  → Approval Gate

Phase 1.5 — Engineering Foundation (tài liệu SỐNG, sửa qua ADR)
  Monorepo · Coding Standard · Naming · Logging · Config · Error Handling · Testing · CI/CD
  → Approval Gate

Phase 2 — Product Prototype (HTML/React/Figma — công cụ không quan trọng)
  → Approval Gate

Phase 3 — Core Backend (build ĐÚNG theo dependency graph ở 07-module-taxonomy.md)
  Data Layer → Structure Engine & Raw Regime Engine (song song, độc lập)
             → Feature Engine → Context Projection
             → Strategy → Decision → Risk Gateway → Execution
  → Quality Gate theo Tier (13-quality-gates.md) — cấp module/artifact
  → Approval Gate

Phase 4 — Frontend
  → Approval Gate

Phase 5 — Integration
  → Approval Gate

Phase 6 — Simulation Platform
  Replay · Backtest · Walk-Forward · Paper Trade · Monte Carlo · Stress Test · Scenario Test
  → Kiểm chứng Parity Principle (I-2) ở CẤP PLATFORM — KHÔNG thay thế Parity Test
    cấp module mà Chapter 13 §13.4 đã yêu cầu cho Tier 1 tại Phase 3
  → Approval Gate

Phase 7 — Deployment
  → Approval Gate

Phase 8 — Research Platform (tách biệt khỏi Production)
  Strategy Comparison · Parameter/Genetic Optimization · Feature Importance
  · Regime Analysis · Performance Attribution
  → Approval Gate

Phase 9 — Observability
  Metrics · Logs · Tracing · Alerts · Dashboard · Health
  → Approval Gate

Ghi chú:
  - AI Layer KHÔNG là một Phase riêng — theo Invariant I-7, nó chỉ là
    consumer mới của published contract, trừ khi tham gia Decision (khi đó là
    Decision Advisor, theo 09-plugin-model.md).
```

## 14.3 Definition of Done — cardinality và nơi ở

[Chapter 12 §12.1](./12-approval-gates.md) (Locked) đã khóa **rule**: mỗi Phase phải có DoD cụ thể, được viết ra và Product Owner chấp nhận **trước khi** Phase đó mở Approval Gate; `Approved` là outcome của gate, **không** được là một mục trong DoD. Chapter 14 **không định nghĩa lại** rule đó — chương này đáp ứng phần [Chapter 12 §12.3](./12-approval-gates.md) delegate cho nó: **DoD content thuộc về đâu và resolve thế nào**.

- **Cardinality:** mỗi Phase phải resolve được **đúng một** authoritative DoD artifact cho Phase đó. Nhiều DoD cạnh tranh cho cùng một Phase → không resolve được → fail-closed.
- **Tồn tại trước gate:** DoD của Phase N phải tồn tại và được chấp nhận **trước khi** Phase N mở Approval Gate — cùng nguyên tắc "criteria defined before used" ([Chapter 12 §12.1](./12-approval-gates.md), [Chapter 13 §13.7](./13-quality-gates.md)).
- **Resolvable + versioned/pinned:** DoD artifact phải explicit, versioned và pin được vào đúng Phase; **cấm** mutable reference kiểu "bản mới nhất".
- **Fail-closed:** DoD không tồn tại, không resolve được, hoặc chưa được chấp nhận → **eligibility incomplete** theo [Chapter 12 §12.2](./12-approval-gates.md), **không** phải reviewer veto và **không** phải Product Owner rejection.
- **Không tạo state store cạnh tranh:** current version/status của DoD artifact resolve từ **MANIFEST** theo [I-12](./02-platform-invariants.md).

**Storage/format/filename cụ thể của DoD artifact defer** — Constitution khóa *tồn tại + property*, không khóa cơ chế (§14.6).

### 14.3.1 DoD incorporation vào canonical Phase plan

DoD **không phải một Phase-plan authority cạnh tranh** ([§14.1.1](#1411-canonical-phase-plan-model)) — nó là **thành phần được incorporate** vào canonical Phase plan của đúng Phase đó.

**Canonical incorporation establishment — không phải registry riêng.** Incorporation không phải một fact tách biệt khỏi DoD acceptance — nó là **một phần của chính Product Owner acceptance evidence** (§14.3). Canonical incorporation tồn tại **khi và chỉ khi**:

1. Product Owner acceptance evidence cho DoD đó (§14.3) resolve được;
2. **cùng evidence đó** xác định tường minh: Phase identity · Roadmap phase-section version/content identity · DoD version/content identity · **explicit incorporation decision** — không suy từ việc DoD tồn tại, được publish, hay được accept cho mục đích khác;
3. evidence tồn tại **trước** Phase gate evaluation (§14.3);
4. **đúng một** incorporation như vậy resolve cho Phase đó.

Không có con đường nào khác tạo incorporation hợp lệ. Một record tuyên bố "incorporate DoD X vào Phase Y" nhưng **không nằm trong chính Product Owner acceptance evidence** — dù immutable, versioned, pinned đến đâu — **không** canonical; validator chỉ **kiểm tra** record có nằm trong đúng PO acceptance evidence hay không (Decision Workflow, [Chapter 0 §3](./00-governance.md)), **không** tự suy diễn hay tự tạo incorporation, cùng nguyên tắc anti-self-certification mà [Chapter 13 §13.4.1](./13-quality-gates.md) đã khóa cho quality-tier authority (tham chiếu, không định nghĩa lại). DoD đã accept nhưng **chưa thỏa cả 4 điều kiện trên** → **chưa incorporate** → **không** phải một phần canonical Phase plan → mọi declaration bên trong nó (kể cả gate-set declaration, §14.4) → **invalid** cho mục đích Chapter 12/13 dùng.

- **Gate-set declaration của DoD đã incorporate = gate-set declaration của canonical Phase plan.** Đây là authority bridge mà [Chapter 12 §12.2(5)](./12-approval-gates.md) ("Approved/Locked authoritative quality contract **hoặc phase plan**") và [Chapter 13 §13.12](./13-quality-gates.md) ("approved phase plan/roadmap") tham chiếu tới.
- **Zero incorporation → fail-closed** (không mặc định "không gate nào áp dụng", §14.4). **Multiple/conflicting incorporation** (ví dụ hai Product Owner acceptance evidence khác nhau của cùng Phase khai gate set khác nhau) **→ fail-closed** — không có precedence ngầm giữa các nguồn.
- **Chapter 14 không định nghĩa lại gate semantics** — trigger A–E cấp artifact vẫn thuộc [Chapter 13 §13.12](./13-quality-gates.md) nguyên vẹn; mục này chỉ khóa **con đường** một declaration cấp-Phase trở thành authoritative input cho Chapter 12/13, không khóa **nội dung** gate.
- **Historical immutability:** DoD hoặc Product Owner acceptance evidence thay đổi về sau (DoD v2 trở thành current, hoặc acceptance mới) **không** reinterpret incorporation, gate evaluation, hay Phase decision đã dùng đúng version đã incorporate tại boundary cũ — evidence cũ giữ nguyên đúng version đã pin ([§14.4.1](#1441-immutable-phase-decision-bundle)); cần đánh giá lại thì tạo incorporation/evaluation **mới** cho boundary mới, không ghi đè.

## 14.4 Quality gate declaration cho phase deliverable

[Chapter 13 §13.12](./13-quality-gates.md) (Locked) khai báo: **Phase deliverable → gate set mà approved phase plan/roadmap ([Chapter 14](./14-roadmap.md)) khai báo áp dụng.** Đây là delegation Chapter 14 phải đáp ứng — nếu để trống, prerequisite [Chapter 12 §12.2(5)](./12-approval-gates.md) không có nguồn resolve.

- **Gate set áp cho phase deliverable của mỗi Phase phải được khai báo tường minh trong DoD artifact của chính Phase đó** (§14.3), và phải resolve được **trước** gate evaluation.
- **Không khai báo được → fail-closed** (§14.3), **không** được mặc định "không gate nào áp dụng".
- **Chapter 14 KHÔNG định nghĩa lại gate applicability cấp artifact.** Trigger A–E của [Chapter 13 §13.12](./13-quality-gates.md) (universal invariant conformance · executable-implementation-triggered coverage · tier-triggered · responsibility/boundary-triggered · lifecycle-triggered) vẫn thuộc Chapter 13 và áp độc lập với khai báo ở đây.
- **Quality Gate KHÔNG chỉ tồn tại ở Phase 3.** Dòng `Quality Gate theo Tier` trong sequence Phase 3 (§14.2) là **nhấn mạnh** giai đoạn build module, **không** phải giới hạn phạm vi. Mọi Phase Approval Gate đều chịu [Chapter 12 §12.2(5)](./12-approval-gates.md): applicable quality gates phải **thực sự PASS**.
- **Quality Gate ≠ Approval Gate** ([Chapter 13 §13.1](./13-quality-gates.md)): gate pass chỉ sinh eligibility evidence; Product Owner vẫn là authority duy nhất quyết định phase transition.

### 14.4.1 Immutable Phase-decision bundle

§14.1.1–§14.4 định nghĩa canonical Phase plan và gate-set declaration tại **evaluation boundary**, nhưng chưa bắt buộc bundle đó **resolvable được sau này** mà không phải tái dựng từ repository archaeology. Mục này khóa yêu cầu **pin** — **không** định nghĩa lại orchestration ([Chapter 12](./12-approval-gates.md)) hay evidence semantics của Quality Gate ([Chapter 13 §13.9](./13-quality-gates.md)).

**Bundle có hai lớp nội dung, tách bạch bắt buộc** (đóng circular reference giữa bundle và MANIFEST transition — xem [§14.4.2](#1442-authoritative-recording-boundary) cho model đầy đủ):

- **Prepared content — phải sẵn sàng trước boundary, thuộc authority của Chapter 14 (pin trực tiếp tại đây):** canonical Phase identity · exact Roadmap version/content identity đã dùng (§14.2) · exact accepted-DoD identity/content version đã incorporate ([§14.3.1](#1431-dod-incorporation-vào-canonical-phase-plan)) · exact gate-set declaration identity/content resolve từ đó (§14.4).
- **Prepared content — phải sẵn sàng trước boundary, thuộc authority của chapter khác (bundle chỉ REFERENCE, không redefine nội dung/format của chúng):** Product Owner DoD-acceptance evidence ([Chapter 0 §3](./00-governance.md)) · required/submitted deliverable evidence ([Chapter 12 §12.1](./12-approval-gates.md)) · applicable Quality Gate result/evidence ([Chapter 13 §13.9](./13-quality-gates.md), evidence contract nguyên vẹn) · Backward Consistency Check result ([Chapter 12 §12.4](./12-approval-gates.md)) · validator/freshness result ([Chapter 11 §11.9](./11-adr-process.md)) · independent review evidence ([Chapter 0 §3](./00-governance.md)) · Product Owner decision fact.
- **KHÔNG thuộc prepared content — chỉ trở thành authoritative TẠI atomic recording boundary:** **resulting MANIFEST transition identity/version** ([I-12](./02-platform-invariants.md)). Bundle **không** được yêu cầu resolve giá trị này **trước** boundary — đòi hỏi đó tạo circular reference (bundle cần transition đã ghi; transition chỉ authoritative sau khi bundle complete). §14.4.2 khóa cách hai fact này trở thành authoritative **cùng lúc**.

**Phân biệt bắt buộc:**

```text
current state          → resolve từ MANIFEST (I-12)
historical decision     → resolve từ immutable pinned Phase-decision bundle, KHÔNG từ current state
```

Git history có thể hỗ trợ audit nhưng **không** phải cách duy nhất để tái dựng bundle — cùng nguyên tắc [Chapter 0 §5b](./00-governance.md) đã khóa cho Decision Log.

Storage/format cụ thể của bundle defer (§14.6); mục này chỉ khóa **phải resolve được gì**, không khóa cách lưu.

### 14.4.2 Authoritative recording boundary

§14.4.1 khóa **bundle phải pin gì**; mục này khóa **thời điểm và cách** hai fact — bundle và MANIFEST transition — trở thành authoritative, **không tạo circular reference**: bundle không cần transition đã ghi mới complete; transition không tự authoritative nếu bundle chưa sẵn sàng. Hai fact này trở thành authoritative **cùng lúc, tại một atomic recording boundary duy nhất**.

**Trình tự bắt buộc** (không định nghĩa lại eligibility hay orchestration của [Chapter 12](./12-approval-gates.md) — chỉ khóa recording sequencing của đúng artifact Chapter 14 sở hữu):

```text
eligibility complete (Chapter 12 §12.2, không đổi)
→ Product Owner decision (fact — có thể xảy ra ngay khi eligibility complete)
→ prepared bundle content (§14.4.1) sẵn sàng đầy đủ — TRỪ resulting MANIFEST transition identity
→ ATOMIC RECORDING BOUNDARY: bundle (giờ pin cả transition identity) VÀ MANIFEST transition
   cùng trở thành authoritative — không cái nào authoritative một mình, không có thứ tự trước/sau giữa hai cái
→ Phase kế tiếp được phép bắt đầu
```

- **"Prepared" ≠ "authoritative".** Prepared bundle content (§14.4.1) là nội dung đã sẵn sàng nhưng **chưa** phải historical record — nó chỉ trở thành **immutable Phase-decision bundle** thật sự tại chính boundary, đồng thời với MANIFEST transition. Trước boundary, không bên nào có quyền coi prepared content là authoritative.
- **Không "đoán trước" resulting transition identity.** Không có convention nào cho phép precompute/guess MANIFEST transition identity rồi coi bundle complete dựa trên giá trị đoán đó — value này chỉ tồn tại và trở thành authoritative chính tại boundary sinh ra nó, không phải trước đó.
- **Product Owner decision authority ≠ validator/recording authority.** PO quyết định `Approve/Reject/Revision Requested` chỉ dưới eligibility đã complete theo [Chapter 12 §12.2](./12-approval-gates.md) — mục này **không** thêm prerequisite mới vào danh sách đó.
- **Partial success không tạo authoritative state.** Nếu chỉ bundle được ghi mà MANIFEST transition không, hoặc ngược lại — cả hai đều **non-authoritative**; **current Phase giữ nguyên** là authoritative state; cần **remediation/retry** boundary; **không** có next-Phase activation.
- **Retry sau uncertain partial failure phải cho đúng một authoritative completion** — không tạo double transition, không tạo hai bundle cạnh tranh cho cùng Phase decision. Đây là **yêu cầu ngữ nghĩa** (semantic requirement), Constitution **không** kê đơn cơ chế (transaction/database/lock service/2PC) — defer §14.6.
- **Phase kế tiếp không được bắt đầu cho tới khi atomic boundary thành công** — decision đã ra, và boundary đã kích hoạt cả bundle lẫn MANIFEST transition.
- **Recording incomplete/thất bại TRƯỚC boundary** — **không** phải `Product Owner rejection`, **không** phải reviewer/validator veto (cùng họ với "fail-closed = eligibility incomplete" của [Chapter 12 §12.2](./12-approval-gates.md), nhưng là một loại khác — recording, không phải eligibility). Product Owner **không** bắt buộc phải quyết định lại trừ khi chính governance workflow yêu cầu.
- **Sau khi atomic boundary đã thành công hợp lệ:** evidence sau đó mất/hỏng là **integrity violation** ([Chapter 0](./00-governance.md) governance workflow) — **không** tự động đảo ngược quyết định, **không** thay thế lịch sử đã mất bằng current state, giữ nguyên historical decision identity. Remediation/audit là governance matter, không phải tự động re-derive.
- **Chapter 14 không tạo Approval Gate thứ hai, không tạo reviewer/validator veto mới, không định nghĩa lại prerequisite list của [Chapter 12 §12.2](./12-approval-gates.md).** Mục này chỉ khóa **semantic atomicity của recording**, không phải điều kiện approve/reject; **không** kê đơn database, Git transaction, CI vendor, lock service, hay two-phase-commit protocol cụ thể.

Cơ chế lưu trữ/persistence cụ thể (transaction, retry/idempotency policy, phân biệt storage outage tạm thời vs corruption vĩnh viễn ở tầng implementation) **defer** (§14.6) — mục này chỉ khóa **semantic atomicity + trình tự** (prepared trước boundary → atomic activation → integrity violation sau boundary), không khóa cơ chế.

## 14.5 Authority boundary

| Concern | Authority |
|---|---|
| Phase sequence · phase deliverable · DoD cardinality/nơi ở · gate-set declaration cho phase deliverable · canonical Phase-plan model · DoD incorporation establishment · Phase-decision bundle pinning · authoritative recording boundary (atomic sequencing) | **Chapter 14 (chương này)** |
| Phase approval orchestration · DoD rule · prerequisite aggregation | [Chapter 12](./12-approval-gates.md) |
| Quality criteria · gate semantics · gate applicability cấp artifact · evidence contract | [Chapter 13](./13-quality-gates.md) |
| Review eligibility (số lượng, role, no-veto) | [Chapter 0 §3](./00-governance.md) / [Chapter 11 §11.5](./11-adr-process.md) |
| ADR Scope Rule · ADR lifecycle | [Chapter 0 §4b](./00-governance.md) / [Chapter 11](./11-adr-process.md) |
| Module taxonomy · dependency graph · module→tier registry | [Chapter 7](./07-module-taxonomy.md) |
| Platform invariants + verification | [Chapter 2](./02-platform-invariants.md) |
| Current version/status/state · Decision Log · OQ state | [MANIFEST](../MANIFEST.md) theo [I-12](./02-platform-invariants.md) |

Chapter 14 **không** tạo competing authority; **không** tự mở phase transition; **không** thay Product Owner quyết định.

## 14.6 Ngoài phạm vi — defer

- **Storage/format/filename cụ thể** của DoD artifact, của gate-set declaration, và của Phase-decision bundle (§14.3–§14.4.1) — Constitution khóa *tồn tại + property*, không khóa filename/schema/tooling.
- **Persistence/recording mechanism cụ thể** (transaction, retry policy, storage outage vs corruption ở tầng implementation, §14.4.2) — Constitution khóa *semantic trình tự*, không khóa cơ chế lưu.
- **Nội dung DoD cụ thể của từng Phase** — viết khi Phase đó chuẩn bị mở gate, theo đúng §14.3.
- **Không đóng open question:** chương này **không** giải quyết **OQ-002** (Strategy Lifecycle Live-gate) hay **OQ-003** (Product Metrics). Việc Phase 6 có Paper Trade và Phase 7 có Deployment **không** đồng nghĩa "được phép lên Live" — điều kiện đó vẫn thuộc OQ-002, nhất quán [Chapter 9 §9.10](./09-plugin-model.md), [Chapter 10 §10.8.2](./10-compatibility-capability-contract.md) và [Chapter 13 §13.1](./13-quality-gates.md) (không chapter nào được đóng ngầm OQ-002).
