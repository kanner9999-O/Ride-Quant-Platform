---
id: 13-quality-gates
title: Quality Gates
version: "1.3"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-27"
next_review: null
depends_on: ["02-platform-invariants", "07-module-taxonomy"]
---

# 13. Quality Gates

> **Trạng thái:** `In Review`. Theo [Chapter 12 §12.3](./12-approval-gates.md) (Locked), khi còn `In Review` chương này được prose-reference như **intended owner** của quality criteria/gate, nhưng nội dung draft **chưa phải binding Locked authority**. Các gate requirement dưới đây chỉ trở thành authoritative quality contract mà [Chapter 12 §12.2(5)](./12-approval-gates.md) yêu cầu **sau khi** Product Owner Approve/Lock.

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

## 13.9 Evidence contract — pinning & reproducibility

Quality-gate evidence là **immutable, resolvable artifact** (cùng tinh thần Compatibility Result bất biến, [Chapter 10 §10.4](./10-compatibility-capability-contract.md); và review-evidence pinning, [Chapter 0 §3](./00-governance.md)). Mỗi evidence entry phải pin tối thiểu:

- **subject identity + version/artifact/config** — theo exact-artifact rule ([Chapter 10 §10.8](./10-compatibility-capability-contract.md)); **cấm** mutable reference như nhãn `latest`/`live-default`;
- **criteria/policy version** đã áp dụng;
- **evaluator/authority** đã đánh giá (quyền đánh giá là grant, không tự nhận — [Chapter 9 §9.6](./09-plugin-model.md));
- **measurement boundary/time**;
- **input data/config identity** đủ để reproduce.

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
- **Trigger** (phải thỏa **cả ba**): artifact có **authoritative executable implementation** + **resolvable coverage boundary** + **resolvable applicable tier**.
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
- **Release / build** → **rollup** hợp gate set của các constituent artifact + performance (nếu có budget) + operational readiness (nếu vào production path); bản thân release không tự sinh coverage ngoài coverage của constituent;
- **Migration** → A + E migration/rollback + data-quality (nếu chạm authoritative data) + compatibility (nếu đổi schema). Coverage (B) **chỉ** áp khi **chính migration có executable implementation** thỏa trigger B;
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
- quarantine mechanism (§13.10) và waiver storage format (§13.11).
