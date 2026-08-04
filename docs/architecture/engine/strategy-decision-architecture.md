---
id: strategy-decision-architecture
title: "Package 1.3-C — Strategy & Decision Engine Architecture"
version: "0.2"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-04"
last_review: null
next_review: null
depends_on: ["00-governance", "02-platform-invariants", "03-engineering-principles", "04-domain-principles", "05-time-model", "06-identity-model", "07-module-taxonomy", "08-event-model", "09-plugin-model", "10-compatibility-capability-contract", "13-quality-gates", "14-roadmap"]
---

# Package 1.3-C — Strategy & Decision Engine Architecture

**CANDIDATE — status: Draft, KHÔNG Consolidated Stable, KHÔNG Approved.** Package 1.3-C v0.1 là candidate đầu tiên, author dựa trên Package 1.1 `Consolidated Stable` (v0.4), Package 1.3-A `Consolidated Stable`, và Package 1.3-B `Consolidated Stable` (xem §1), theo [`phase-1-plan.md`](../phase-1-plan.md) v0.4 (`Approved`) §8 Package 1.3-C block. Chưa qua Review A/Independent Review B, chưa có Product Owner consolidation decision.

**v0.2 — bounded correction (2026-08-04), đóng `P13C-IRB-MAJ-01`/`P13C-A-MIN-01`/`P13C-IRB-MIN-01`** (findings confirmed từ Review A/Independent Review B trên v0.1). `P13C-IRB-MAJ-01`: `module-registry.yaml` v0.4 gán `plugin-release-manager.phase.elaborated_by: "1.3-C"` từ trước (Package 1.1 assignment KHÔNG sai, KHÔNG cần sửa) nhưng v0.1 của tài liệu này KHÔNG elaborate module đó — sửa: mở rộng scope bốn → **năm module**, thêm §5a "Module boundary — Plugin Release Manager". `P13C-A-MIN-01`/`P13C-IRB-MIN-01`: §7.3 (v0.1) gộp nhầm "Feature Engine/Context Aggregator" chung một nhóm "authoritative source DUY NHẤT" — SAI vì `feature-engine.owns_authoritative_state: true` nhưng `context-aggregator.owns_authoritative_state: false` (projection); sửa tách bạch tường minh tại §7.3 + thêm terminology block tại §9. KHÔNG đổi Decision authority model đã Approved (ADR-016 v0.8), KHÔNG đổi mandatory non-bypass sequence, KHÔNG đổi Context fail-closed conditions, KHÔNG resolve context.md terminology gap, KHÔNG tạo ADR.

## 0. Vai trò của tài liệu này

Package 1.3-C elaborate **kiến trúc kỹ thuật** cho năm module ĐÃ được Package 1.1 (`Consolidated Stable`, [`module-registry.yaml`](../module-registry.yaml) v0.4 blob `6c4daa3eda3ef560b201de516dd019564d264c08`, [`system-decomposition.md`](../system-decomposition.md) v0.4 blob `8e60b9e6051956cfbe83f33e1c82f404bc082e37`) thiết lập identity/taxonomy/dependency: `strategy-engine`, `strategy-plugin-host`, `plugin-release-manager`, `decision-evaluation-engine`, `decision-authority-service` — **v0.2 correction (2026-08-04), đóng `P13C-IRB-MAJ-01`: thêm `plugin-release-manager`** (module-registry.yaml v0.4 đã gán `phase.elaborated_by: "1.3-C"` cho module này từ trước; v0.1 bỏ sót elaboration, sửa tại v0.2, xem §5a). Tài liệu này **KHÔNG redefine** module identity/taxonomy/dependency đã pin ở Package 1.1, **KHÔNG redefine** Domain Contract semantics đã pin ở `strategy.md`/`decision.md`, và **KHÔNG redefine** ADR-016's approved taxonomy decision — chỉ elaborate: responsibility boundary chi tiết, mandatory non-bypass flow, sole Decision-authority proof, Context criticality consumption (không đổi Package 1.3-B), determinism/replay/no-repaint treatment, và open gap — đúng phạm vi `phase-1-plan.md` §8 Package 1.3-C "Purpose: Kiến trúc kỹ thuật cho Strategy Engine → Decision Engine, bao gồm Plugin hosting boundary (Strategy Plugin)".

**KHÔNG thuộc phạm vi tài liệu này:** field-level event schema (đã khóa tại `strategy.md` v0.3/`decision.md` v0.3, Package 0.2-C3/C4, `Consolidated Stable`); Strategy Plugin algorithm; evaluation-proposal field-level schema (chưa tồn tại — §13 gap); database schema; deployment/runtime topology cụ thể; Risk/Execution semantics (Package 1.3-D); Package 1.3-A/1.3-B content (KHÔNG redefine, `Consolidated Stable`).

## 1. Governing authority

```text
Constitution (Chapter 0–14, Locked):              highest architectural authority
Approved ADR-009 (ordering):                      per-stream sequence + explicit causation,
                                                    KHÔNG global total order
Approved ADR-010 (Decision Time Model):            decision_time/decision_context_cursor/
                                                    Append-and-Revalidate
Approved ADR-013 (Strategy Definition Version):    bốn trục evidence độc lập
Approved ADR-015 (module dependency graph,         controlling cho 21/22 module KHÔNG bị
  scoped amendment qua ADR-016):                   ADR-016 chạm tới
Approved ADR-016 v0.8 (Candidate B/split,           controlling cho split Decision Evaluation
  Mechanism A):                                     Engine vs Decision Authority Service —
                                                    sole authoritative source cho quyết định
                                                    taxonomy này
Domain Contract (strategy.md v0.3, decision.md     controlling domain semantic authority —
  v0.3 — Package 0.2-C3/C4, Consolidated Stable):  Consolidated Stable, KHÔNG redefine tại đây
Chapter 9 (Plugin Model, Locked):                  Plugin Definition/Version/Package-Build-
                                                    Artifact/Plugin Runtime bốn tầng; Decision-
                                                    time visibility (§9.5); published-contract-
                                                    only interaction (§9.2)
module-registry.yaml v0.4 (Consolidated Stable):  module identity/taxonomy/dependency
                                                    authority — KHÔNG redefine tại đây
system-decomposition.md v0.4 (Consolidated        official Phase 1 module dependency graph
  Stable):                                         — KHÔNG redefine tại đây
feature-context-architecture.md v0.2 (Package     Context Aggregator criticality/failure
  1.3-B, Consolidated Stable):                     policy boundary — consumed UNCHANGED (§9)
phase-1-plan.md v0.4 (Approved):                  Phase 1 work-breakdown/package-boundary
                                                    authority
Package 1.3-C (tài liệu này):                     technical elaboration authority ONLY, cho
                                                    đúng năm module trong scope (v0.2, đóng
                                                    P13C-IRB-MAJ-01)
```

Package 1.3-C KHÔNG redefine domain entity/event semantics, module identity/taxonomy, hay ADR decision nào — mọi nội dung dưới đây chỉ **elaborate** kiến trúc kỹ thuật trong ranh giới đã pin.

## 2. Module scope (năm module, pin nguyên trạng từ Package 1.1 v0.4 — v0.2 mở rộng, đóng `P13C-IRB-MAJ-01`)

Năm module dưới đây trích dẫn NGUYÊN VĂN `module-registry.yaml` v0.4 (identity/taxonomy/dependency KHÔNG đổi) — cột "Elaboration" là nội dung MỚI của tài liệu này. **`plugin-release-manager` thêm tại v0.2** — Package 1.1 đã gán `phase.elaborated_by: "1.3-C"` cho module này từ trước (assignment KHÔNG sai, KHÔNG cần sửa Package 1.1); v0.1 của tài liệu này bỏ sót elaboration, sửa tại đây:

| module_id | module_type | owns_authoritative_state | depends_on | forbidden_dependencies |
|---|---|---|---|---|
| `strategy-engine` | runtime_service | true | `account-service` | (none) |
| `strategy-plugin-host` | compute_engine | false | `strategy-engine`, `context-aggregator`, `plugin-release-manager` | `execution-engine`, `risk-gateway`, `paper-execution-boundary`, `decision-authority-service` |
| `plugin-release-manager` | runtime_service | true | (none) | (none) |
| `decision-evaluation-engine` | compute_engine | false | `strategy-engine`, `strategy-plugin-host`, `context-aggregator` | `execution-engine`, `risk-gateway`, `paper-execution-boundary` |
| `decision-authority-service` | runtime_service | true | `decision-evaluation-engine`, `strategy-engine` | `execution-engine`, `paper-execution-boundary` |

**KHÔNG recreate `decision-engine` (xác nhận tường minh, yêu cầu task):** module `decision-engine` (hybrid cũ, Candidate A) KHÔNG còn tồn tại trong `module-registry.yaml` v0.4 — ADR-016 v0.8 (Approved) đã REJECT Candidate A, chọn Candidate B (split). Tài liệu này KHÔNG tham chiếu `decision-engine` như một entity/module còn hiệu lực dưới bất kỳ hình thức nào ngoài historical/lineage reference (ví dụ khi trích dẫn nguyên văn ADR-016).

**Module tham chiếu, KHÔNG elaborate đầy đủ tại đây (out of scope cho Package 1.3-C, task chỉ liệt kê năm module trên):** `context-aggregator` (Package 1.3-B, `Consolidated Stable`, KHÔNG redefine); `account-service` (Package 1.2, chưa elaborate); `risk-gateway` (Package 1.3-D, downstream boundary, KHÔNG elaborate).

## 3. Mandatory architecture flow (non-bypass sequence — KHÔNG runtime topology)

```text
Context Aggregator (Package 1.3-B, Consolidated Stable)
      │
      ▼
Strategy Engine (runtime_service — owns Strategy Definition Version/Instance identity,
                 orchestrates eligibility, strategy.md §9a)
      │
      ▼
Strategy Plugin Host (compute_engine — MANDATORY published-contract execution boundary,
                       KHÔNG bypassable)
      │  (candidate analytical/advisory output — KHÔNG Decision)
      ▼
Decision Evaluation Engine (compute_engine — non-authoritative, deterministic evaluation)
      │  (non-authoritative evaluation proposal — KHÔNG Decision)
      ▼
Decision Authority Service (runtime_service — SOLE authoritative Decision/Trade Intent
                             authority, MANDATORY, KHÔNG bypassable)
      │  (authoritative Decision / Trade Intent)
      ▼
Risk Gateway (Package 1.3-D — KHÔNG thuộc phạm vi tài liệu này)
```

**Xác nhận tường minh (yêu cầu task):** đây là responsibility/mandatory-ordering view — KHÔNG phải authorization triển khai một synchronous pipeline hay runtime topology cụ thể (process/container/host, đồng bộ/bất đồng bộ, message broker). Internal interaction có thể là event/query/command theo đúng contract category đã pin tại `module-registry.yaml` v0.4 (§2 trên) — Package 1.3-C KHÔNG chọn cơ chế cụ thể.

**Reconciliation với module-level `depends_on` thực tế (bắt buộc làm rõ, tránh đọc nhầm mũi tên trên thành một dependency edge đơn nhất):** mũi tên "Context Aggregator → Strategy Engine" ở trên biểu diễn **thứ tự trách nhiệm/data-availability tổng thể** trong luồng, KHÔNG PHẢI một dependency edge module-registry-level giữa `strategy-engine` và `context-aggregator` — `strategy-engine.depends_on` (§2) CHỈ chứa `account-service`, KHÔNG chứa `context-aggregator`. Dependency edge THỰC SỰ cho việc tiêu thụ Context nằm ở **hai điểm khác**, cả hai ĐÃ pin tại `module-registry.yaml` v0.4:

```text
strategy-plugin-host.depends_on        chứa context-aggregator  (Plugin Host cung cấp
                                                                   Context như published-
                                                                   contract input cho plugin,
                                                                   Chapter 9 §9.5)
decision-evaluation-engine.depends_on  chứa context-aggregator  (Decision Evaluation Engine
                                                                   tự tiêu thụ Context trực
                                                                   tiếp cho deterministic
                                                                   evaluation rule, §9 dưới)
```

Strategy Engine's vai trò trong luồng là **orchestration của Strategy Definition/Instance eligibility** (`eligible_for_new_computation`, strategy.md §9a — sáu điều kiện KHÔNG bao gồm Context availability) — KHÔNG phải chính nó tiêu thụ nội dung Context. Package 1.3-C KHÔNG thêm một edge `strategy-engine → context-aggregator` mới vào registry — điều đó sẽ vi phạm "KHÔNG modify Package 1.1" của chính task này.

**Non-bypass — ba module KHÔNG được bypass (xác nhận qua `forbidden_dependencies`/`depends_on`, script-verifiable, xem §10):**

```text
Strategy Plugin Host:      strategy-plugin-host.forbidden_dependencies chứa
                            decision-authority-service — Plugin Host KHÔNG được reach
                            authority append trực tiếp, PHẢI qua Decision Evaluation
                            Engine (§6).
Decision Authority         risk-gateway.depends_on CHỈ chứa decision-authority-service
  Service:                  (KHÔNG chứa decision-evaluation-engine, KHÔNG chứa
                            strategy-plugin-host) — Risk Gateway KHÔNG có đường consume
                            nào khác ngoài chính module authority này (§8).
Risk Gateway:               decision-evaluation-engine.forbidden_dependencies VÀ
                            strategy-plugin-host.forbidden_dependencies đều chứa
                            risk-gateway — cả hai module upstream KHÔNG được tự ý reach
                            Risk Gateway, bắt buộc qua Decision Authority Service.
```

## 4. Module boundary — Strategy Engine

**Trách nhiệm (Package 1.1, KHÔNG đổi):** "Sở hữu Strategy Definition Version identity (ADR-013) và Strategy Instance identity (bốn trục evidence độc lập + account_id + instrument_selection)."

### 4.1 Architecture-level orchestration (elaboration)

```text
Strategy Engine sở hữu authoritative:
  StrategyDefinitionVersionRegistered/StrategyDefinitionVersionFactInvalidated
    (strategy.md §3/§4); StrategyInstanceRegistered/StrategyInstanceStatusChanged/
    StrategyInstanceFactInvalidated (strategy.md §6–§8).
  Orchestration của eligible_for_new_computation (strategy.md §9a) — sáu điều kiện AND:
    Strategy Instance current_status == ACTIVE; Strategy Definition Version VALID; Account
    ACTIVE; environment resolve nhất quán; bốn trục evidence persistently resolvable;
    instrument_selection_ref eligible (TradableListing ELIGIBLE).

Strategy Engine KHÔNG sở hữu:
  Context/Feature/Structure/Regime fact (Package 1.3-A/1.3-B); Plugin execution (Strategy
    Plugin Host, §5); Decision evaluation (Decision Evaluation Engine, §6); Decision/Trade
    Intent identity (Decision Authority Service, §7); Risk/Execution semantics (Package
    1.3-D).
```

### 4.2 Preserved boundary (bắt buộc, yêu cầu task — KHÔNG được vi phạm)

```text
Strategy Engine KHÔNG được:
  host untrusted plugin execution TRỰC TIẾP — plugin_relation: none (module-registry.yaml
    v0.4, §2) — KHÔNG plugin_relation: hosts (đó là strategy-plugin-host, §5); Strategy
    Engine KHÔNG tự thực thi Strategy Plugin logic.
  append authoritative Decision records — decision-authority-service SOLE authority (§7).
  sở hữu Trade Intent identity — decision-authority-service SOLE authority (§7).
  thực hiện Risk approval — risk-gateway (Package 1.3-D, ngoài phạm vi).
  route Execution — execution-engine (Package 1.3-D, ngoài phạm vi).
  âm thầm thay thế Context stale — Strategy Engine KHÔNG tự nó tiêu thụ Context (§3), và
    fail-closed behavior của Context là trách nhiệm của Decision Evaluation Engine (§9),
    KHÔNG của Strategy Engine.
```

### 4.3 Strategy Definition Version pinning (ADR-013, Chapter 9 — bảo toàn nguyên vẹn)

```text
Bốn trục evidence độc lập (ADR-013 §2.1, strategy.md §11, strategy_evidence_axis_policy:
  FOUR_INDEPENDENT_AXES_NO_PROXY):
    Strategy Definition Version  — business/decision semantics (strategy.md §1)
    Plugin Version                — implementation-release identity (Chapter 9 §9.1)
    Configuration Version         — parameter tuning cho instance cụ thể (Chapter 9 §9.1)
    Package/Build Artifact        — exact executable bytes (Chapter 9 §9.1, ADR-013 §2.5)

KHÔNG trục nào proxy trục khác — cấm derive plugin_version_ref từ configuration_version_ref
  hay ngược lại; cấm dùng Plugin Version/source commit hash làm proxy cho
  package_build_artifact_ref (ADR-013 §2.5, Chapter 9 §9.5 "mixed-build activation is
  integrity violation"). Mỗi trục bump ĐỘC LẬP.

Strategy Instance pin ĐỦ bốn trục + account_id + instrument_selection_ref (strategy.md §5)
  — Instance là MỘT subject liên tục; đổi bất kỳ trục nào tạo Instance MỚI, KHÔNG mutate
  binding hiện có (Chapter 9 §9.3 mục 2).
```

## 5. Module boundary — Strategy Plugin Host

**Trách nhiệm (Package 1.1, KHÔNG đổi):** "Host/execute Strategy Plugin (Decision Advisor) logic — Compute Engine điển hình theo Chapter 9 §9.1." + "Tuân Decision-time visibility (Chapter 9 §9.5) — mọi input cursor-bounded, cấm đọc ambient/current state."

### 5.1 Mandatory published-contract execution boundary (bắt buộc, yêu cầu task)

```text
Strategy Plugin Host LÀ ranh giới thực thi BẮT BUỘC cho mọi Strategy Plugin — KHÔNG
Strategy Plugin nào được thực thi ngoài module này (Chapter 9 §9.2: Plugin CHỈ tương tác
qua published contract — event/query/command; cấm gọi trực tiếp implementation nội bộ
hoặc mutable state của module khác).

Được phép (Chapter 9 §9.1/§9.2/§9.5, task requirement):
  load một registered plugin ELIGIBLE (Plugin Definition đã đăng ký tại module-registry.yaml
    — KHÔNG plugin registry thứ hai, Chapter 9 §9.1);
  validate plugin compatibility/capability metadata (Chapter 10, referenced KHÔNG redefine
    tại đây);
  cung cấp CHỈ published contract input (query/event/command đã pin — KHÔNG raw internal
    state của module khác);
  cô lập plugin invocation ở tầng kiến trúc (published boundary, I-7 Verification: network
    ACL/API authorization scope/event schema compatibility/command authorization/capability
    declaration/không truy cập storage module khác);
  trả về deterministic plugin evaluation output — Decision-time visibility bắt buộc
    (Chapter 9 §9.5: mọi input/query cursor-bounded hoặc snapshot-bounded, cấm đọc
    ambient/current mutable state, cấm "latest" ngầm).
```

### 5.2 Preserved boundary (bắt buộc, yêu cầu task — KHÔNG được vi phạm)

```text
Strategy Plugin Host KHÔNG được:
  append Decision — decision-authority-service SOLE authority (§7); Plugin output LÀ
    "candidate analytical signal, NOT the authoritative Decision fact" (module-registry.yaml
    v0.4 notes, §2).
  tạo Trade Intent identity — decision-authority-service SOLE authority (§7).
  approve Risk — forbidden_dependencies chứa risk-gateway (§2).
  gọi Execution trực tiếp — forbidden_dependencies chứa execution-engine/
    paper-execution-boundary (§2).
  đọc arbitrary internal module state — Chapter 9 §9.2 published-contract-only; §9.5 cấm
    đọc ambient/current state.
  bypass Strategy Engine orchestration — depends_on chứa strategy-engine (§2), KHÔNG có
    đường độc lập truy cập Strategy Definition/Instance identity nào khác.
  bypass Decision Evaluation Engine — forbidden_dependencies chứa decision-authority-
    service TƯỜNG MINH (§2, ADR-016 v0.8 correction) — Plugin Host KHÔNG có đường trực
    tiếp nào tới authority append; mọi output PHẢI qua Decision Evaluation Engine trước.
```

### 5.3 ADR-016 unresolved boundary — carry forward tường minh (BẮT BUỘC, yêu cầu task)

**KHÔNG resolve tại đây (đúng yêu cầu task "Explicitly carry forward ADR-016's unresolved Plugin Host versus Decision Evaluation boundary. Do not invent the missing evaluation-proposal Domain Contract"):**

```text
ADR-016 v0.8 Accepted risk #1 (nguyên văn): "Redundancy/boundary risk với strategy-plugin-
  host: Decision Evaluation Engine (compute_engine, sinh non-authoritative candidate
  signal) có trách nhiệm gần giống strategy-plugin-host đã tồn tại — ranh giới CHÍNH XÁC
  chưa được authoritative resolve, đòi hỏi author Decision algorithm (ngoài phạm vi ADR
  này) để phân biệt dứt khoát."

Package 1.3-C KHÔNG resolve ranh giới CHÍNH XÁC giữa "candidate analytical signal" (Strategy
  Plugin Host output, §5.1) và "non-authoritative evaluation proposal" (Decision Evaluation
  Engine output, §6.1) — cả hai đều non-authoritative, cả hai đều KHÔNG phải Decision,
  nhưng nội dung/semantics CHÍNH XÁC phân biệt hai output này (ví dụ: Plugin Host output có
  phải MỘT input trong nhiều input của Decision Evaluation Engine, hay Decision Evaluation
  Engine chỉ re-validate/wrap output đó?) đòi hỏi Decision algorithm CỤ THỂ — ngoài phạm vi
  kiến trúc của Package 1.3-C (forbidden scope: "author Strategy Plugin algorithm"). Xem
  §13 cho gap đầy đủ.
```

## 5a. Module boundary — Plugin Release Manager (MỚI, v0.2, đóng `P13C-IRB-MAJ-01`)

**Trách nhiệm (Package 1.1, KHÔNG đổi):** "Resolve Plugin Version → exact Package/Build Artifact content identity (content hash, target platform, build identity) HOẶC immutable release manifest (Chapter 9 §9.1, mô hình A/B) — operational resolution, KHÔNG architecture identity." + "Theo dõi runtime compatibility/availability status của Plugin Runtime replica đã deploy." + "Điều phối activation/deactivation boundary (Chapter 9 §9.5 — validated compatibility set, atomic activation) — operational coordination fact, KHÔNG Plugin Definition identity." + "KHÔNG sở hữu Plugin Definition identity, taxonomy type, hay bất kỳ architecture responsibility nào — authority đó thuộc DUY NHẤT `module-registry.yaml`."

### 5a.1 Registry classification (bảo toàn nguyên vẹn, yêu cầu task)

```text
module_type:               runtime_service
owns_authoritative_state:  true (operational fact ONLY — §5a.3 dưới, KHÔNG Plugin
                            Definition identity)
consumes:                  command
emits:                     event, query
depends_on:                (none — root)
forbidden_dependencies:    (none)
plugin_relation:           manages_release
security_classification:   none
```

### 5a.2 Architecture-level responsibility (elaboration, đúng yêu cầu task)

```text
Plugin Release Manager chịu trách nhiệm cho:
  registered plugin release metadata (Plugin Version → Package/Build Artifact resolution
    record, Chapter 9 §9.1);
  Plugin Definition / Plugin Version / Package-Build Artifact resolution — CHỈ resolution
    (tra cứu/xác nhận), KHÔNG sở hữu Plugin Definition identity (đó là module-registry.yaml
    chính nó, Chapter 7 §7.5/Chapter 9 §9.1 — "Module này KHÔNG phải, và KHÔNG tạo, một
    plugin registry thứ hai");
  compatibility và capability evidence — theo dõi runtime compatibility/availability
    status của Plugin Runtime replica đã deploy (Chapter 10, referenced KHÔNG redefine);
  activation eligibility coordination — điều phối activation/deactivation boundary
    (Chapter 9 §9.5: validated compatibility set phải đồng bộ atomic — Plugin Contract
    version, Input Contract version, published contract references, permission grant
    version, required capability/compatibility result, runtime implementation/deployment
    version, exact Package/Build Artifact content identity đã qua parity/compatibility
    validation);
  immutable release-manifest hoặc exact artifact resolution nơi ĐÃ được Chapter 9 §9.1
    cho phép (Mô hình A — Decision pin trực tiếp artifact: plugin_definition_id ·
    plugin_version · artifact_content_hash; Mô hình B — Version manifest bất biến trỏ
    exact artifact theo target platform) — Package 1.3-C KHÔNG chọn giữa hai mô hình,
    chỉ ghi nhận cả hai đều hợp lệ theo Chapter 9;
  cung cấp eligible release identity cho Strategy Plugin Host (§5) — Strategy Plugin Host
    depends_on chứa plugin-release-manager (§2) chính vì lý do này: Plugin Host cần biết
    release/artifact nào eligible TRƯỚC khi load/execute plugin.
```

### 5a.3 Preserved boundary (bắt buộc, yêu cầu task — KHÔNG được vi phạm)

```text
Plugin Release Manager KHÔNG được:
  thực thi Strategy Plugin algorithm — đó là strategy-plugin-host (§5) responsibility,
    KHÔNG phải Plugin Release Manager.
  host plugin runtime invocation — plugin_relation: manages_release (§5a.1), KHÔNG
    plugin_relation: hosts (đó là strategy-plugin-host); Plugin Release Manager KHÔNG tự
    thực thi bất kỳ Plugin logic nào.
  tiêu thụ live Context cho strategy evaluation — depends_on: (none) (§5a.1); KHÔNG có
    edge nào tới context-aggregator; Plugin Release Manager KHÔNG chạm Context dưới bất
    kỳ hình thức nào.
  sinh plugin analytical output — đó là strategy-plugin-host's output ("candidate
    analytical signal", §5.2), KHÔNG phải Plugin Release Manager's responsibility.
  append Decision — decision-authority-service SOLE authority (§7).
  assign Decision hay Trade Intent identity — decision-authority-service SOLE authority
    (§7).
  thực hiện Decision evaluation — decision-evaluation-engine (§6) responsibility.
  approve Risk — ngoài phạm vi hoàn toàn (Package 1.3-D); forbidden_dependencies rỗng
    (§5a.1) nhưng KHÔNG có depends_on nào tới risk-gateway, KHÔNG có architecture path
    nào để làm việc này.
  route Execution — cùng lý do trên, ngoài phạm vi hoàn toàn (Package 1.3-D).
  mutate Strategy Definition semantics — strategy-engine (§4) SOLE authority cho Strategy
    Definition Version/Instance identity; Plugin Release Manager KHÔNG sở hữu bất kỳ
    Strategy semantic nào.
  âm thầm thay thế mutable-latest plugin artifact — Chapter 9 §9.1 cấm tường minh: "Chỉ
    trùng Plugin Version là KHÔNG đủ để activation eligible" — runtime implementation
    thực tế phải resolve duy nhất tới đúng artifact ĐÃ nằm trong validated compatibility
    set (§9.5); mixed-build activation (artifact khác dù cùng Plugin Version) LÀ integrity
    violation, fail-safe (I-6).
```

### 5a.4 Plugin Release Manager vs Strategy Plugin Host — phân biệt tường minh (BẮT BUỘC, yêu cầu task)

```text
Plugin Release Manager quyết định release/artifact ĐÃ ĐĂNG KÝ nào eligible và resolvable
  (§5a.2) — CHỈ resolution/coordination, KHÔNG execution.

Strategy Plugin Host thực thi artifact eligible ĐÃ được chọn thông qua published contract
  (§5.1) — CHỈ execution trong ranh giới cursor-bounded, KHÔNG tự resolve artifact
  identity của chính nó (đó là lý do strategy-plugin-host.depends_on chứa
  plugin-release-manager, §2).

Đây là HAI trách nhiệm TÁCH BIỆT — module-registry.yaml v0.4 xác nhận qua hai
  plugin_relation khác nhau (manages_release vs hosts, §5a.1/§5.1) — và KHÔNG module nào
  trong hai module này được bypass Decision Evaluation Engine hay Decision Authority
  Service: `plugin-release-manager.forbidden_dependencies` rỗng NHƯNG `depends_on` cũng
  rỗng (root, §5a.1) — KHÔNG architecture path nào tồn tại từ Plugin Release Manager tới
  decision-authority-service/risk-gateway/execution-engine; `strategy-plugin-host.
  forbidden_dependencies` chứa `decision-authority-service` tường minh (§2/§5.2) — non-
  bypass đã bảo toàn cho CẢ HAI module, không chỉ Strategy Plugin Host.
```

### 5a.5 KHÔNG invent (bắt buộc, yêu cầu task)

```text
Package 1.3-C KHÔNG invent tại §5a này:
  plugin lifecycle state mới — Chapter 9 §9.8 đã khóa runtime lifecycle facts (installed/
    deployed/created/activated/paused/deactivated/promoted/rolled-back/retired) là
    authoritative event log, KHÔNG registry status; Package 1.3-C KHÔNG thêm state nào.
  capability type mới — Chapter 10 (referenced, KHÔNG redefine) sở hữu compatibility/
    capability algorithm.
  activation protocol mới — Chapter 9 §9.5's validated compatibility set là ranh giới
    ĐÃ khóa; cơ chế fencing/transaction/deployment-coordinator cụ thể "có thể defer sang
    Phase 1 design spec" (Chapter 9 §9.5, nguyên văn) — Package 1.3-C KHÔNG author cơ chế
    đó, chỉ ghi nhận atomic semantic đã khóa.
  field-level release schema — KHÔNG author payload/schema cho Plugin Version/Package-
    Build-Artifact resolution record.
  artifact-signing implementation — ngoài phạm vi hoàn toàn (Package 1.2 security/custody
    concern nếu có).
  deployment topology — Package 1.3-C KHÔNG chọn process/container/host cho Plugin
    Release Manager.
  runtime isolation technology — cơ chế cô lập cụ thể (container, sandbox, process
    boundary) là Phase 1/Package 1.2 concern, KHÔNG author tại đây.

Nơi exact release activation hoặc compatibility mechanics còn chưa resolve (Mô hình A vs
  B lựa chọn cụ thể; fencing/transaction mechanism; capability matching algorithm cụ thể)
  — carry forward như gap tường minh tại §13, KHÔNG chọn implementation.
```

## 6. Module boundary — Decision Evaluation Engine

**Trách nhiệm (Package 1.1, KHÔNG đổi):** "Platform-owned deterministic Decision evaluation của Strategy Instance tại decision_context_cursor (ADR-010, Chapter 8 §8.4-§8.5) — sinh non-authoritative evaluation output/proposal." + "KHÔNG sở hữu Decision identity, KHÔNG Decision append authority, KHÔNG Trade Intent identity, KHÔNG Risk approval authority, KHÔNG Execution authority (ADR-016 v0.8, Candidate B)."

### 6.1 module_type/authority (bắt buộc, yêu cầu task)

```text
module_type: compute_engine
authority:   non-authoritative (owns_authoritative_state: false, module-registry.yaml v0.4)
```

### 6.2 Responsibilities (elaboration, đúng yêu cầu task)

```text
Consume:
  eligible Strategy/plugin evaluation output (từ strategy-plugin-host, §5) PLUS Context
  (trực tiếp từ context-aggregator, depends_on §2 — KHÔNG route qua Strategy Plugin Host).

Apply:
  deterministic Decision evaluation rules — decision.md §5c bounded typed rule-evidence
  shape (v0.1 walking skeleton: rule_family PRICE_CROSSES_REFERENCE_SERIES, price_source/
  reference_series_type/reference_series_period/crossing_policy/evaluation_timing —
  KHÔNG DSL/parser/rule graph tổng quát).

Produce:
  MỘT non-authoritative evaluation proposal — KHÔNG phải Decision (§8 non-bypass
  statement). Package 1.3-C KHÔNG khẳng định proposal này đồng nhất với bất kỳ event
  cụ thể nào của decision.md (DecisionEvaluationAttemptRecorded hay khác) — xem §13 cho
  lý do (mapping CHƯA resolve, ADR-016 Accepted risk #1/#2).

Preserve:
  provenance (input_evidence event_record_ref, decision.md §5d); definition versions
  (bốn trục Strategy evidence, §4.3 trên — persistently resolvable tại
  decision_context_cursor, decision.md §5b); causal ancestry (causation_refs, Chapter 8
  §8.2.3 — KHÔNG BAO GIỜ rỗng cho fact derived, ADR-009 §2.4 causation model).

Mode parity:
  cùng definition_version + cùng input causal ancestry → cùng evaluation output, mọi
  execution mode (Live/Backtest/Paper/Replay) — I-2 Decision Parity, §10 dưới.
```

### 6.3 Preserved boundary (bắt buộc, yêu cầu task — KHÔNG được vi phạm)

```text
Decision Evaluation Engine KHÔNG được:
  append authoritative Decision records — decision-authority-service SOLE authority (§7).
  assign authoritative Decision identity — decision_id authority thuộc DUY NHẤT decision-
    authority-service (ADR-016 v0.8, decision.md §1 invariant).
  assign Trade Intent identity — decision-authority-service SOLE authority (§7).
  thực hiện final invariant validation (sở hữu bởi decision-authority-service, §7 —
    "Final acceptance/rejection tại authority boundary — validate evaluation proposal
    identity/version/cursor/eligibility từ decision-evaluation-engine trước khi append",
    module-registry.yaml v0.4 §2).
  approve Risk — forbidden_dependencies chứa risk-gateway (§2).
  route Execution — forbidden_dependencies chứa execution-engine/paper-execution-
    boundary (§2).
```

### 6.4 Evaluation-proposal artifact — explicit unresolved Domain gap (BẮT BUỘC, yêu cầu task)

```text
"The evaluation-proposal artifact remains an explicit unresolved Domain gap unless
already formally registered by controlling source" (yêu cầu task) — kiểm tra tường minh:
KHÔNG controlling source nào (strategy.md/decision.md/ADR-009/ADR-010/ADR-013/ADR-016/
Chapter 9) đã formally register một artifact riêng biệt tên "evaluation proposal" với
identity/schema/lifecycle của chính nó. ADR-016 v0.8 Accepted risk #2 (nguyên văn):
"Evaluation-proposal artifact governance/Domain gap: loại artifact MỚI (evaluation
proposal, identity/version/retention policy) chưa có Domain Contract. CHẤP NHẬN — cần
Domain Contract correction (decision.md hoặc contract mới) trước implementation, KHÔNG
tự động authorize tại ADR này."

Package 1.3-C KHÔNG author field-level schema cho artifact này (forbidden scope) — gap
carry forward nguyên vẹn tại §13.
```

## 7. Module boundary — Decision Authority Service

**Trách nhiệm (Package 1.1, KHÔNG đổi):** "Sole invariant-validation authority; sole authoritative Decision append authority; sole Decision identity authority (ADR-010, Chapter 8 §8.4/§8.5) và Trade Intent identity." + "Final acceptance/rejection tại authority boundary — validate evaluation proposal identity/version/cursor/eligibility từ `decision-evaluation-engine` trước khi append."

### 7.1 module_type/role (bắt buộc, yêu cầu task, ADR-016 preserved chính xác)

```text
module_type: runtime_service
role:        sole authoritative Decision authority
```

### 7.2 Sole authority (bắt buộc, yêu cầu task)

```text
Decision Authority Service, VÀ CHỈ Decision Authority Service, được phép:
  thực hiện final Decision invariant validation — decision.md §3 relational invariants
    (cursor.recorded_time ≤ DecisionRecorded.recorded_time; input_event.recorded_time ≤
    cursor.recorded_time; lifecycle_event.recorded_time ≤ cursor.recorded_time;
    cursor.stream_registry_version = registry version mà input_contract_ref pin —
    Chapter 8 §8.5.2); vi phạm bất kỳ điều nào → PHẢI reject khi append.
  accept hoặc reject một evaluation proposal tại authority boundary (module-registry.yaml
    v0.4 notes §2 — xem §6.4 cho gap: outcome "reject" CHƯA có representation tường minh
    trong decision.md hiện có, §13).
  append authoritative Decision records — DecisionRecorded (decision.md §5), event_class:
    decision (Chapter 8 §8.2.1/§8.4).
  assign authoritative Decision identity — decision_id (decision.md §1, opaque, globally
    unique, bất biến, KHÔNG derive từ bất kỳ field nội dung nào).
  establish Trade Intent identity theo đúng controlling Domain semantics (decision.md §10:
    result = LONG/SHORT → zero HOẶC MỘT TradeIntentIssued, keyed UNIQUE bởi
    originating_decision_id, derivation idempotent; result = NO_ACTION → ZERO Trade Intent
    LUÔN LUÔN — Package 1.3-C KHÔNG author field-level Trade Intent schema, chỉ trích dẫn
    cardinality rule đã pin tại decision.md §10 cho chính module authority này).
```

### 7.3 Preserved boundary (bắt buộc, yêu cầu task — KHÔNG được vi phạm)

```text
Decision Authority Service KHÔNG được:
  thực thi strategy/plugin algorithm — đó là strategy-plugin-host (§5)/decision-evaluation-
    engine (§6) responsibility.
  tự tính lại Feature — Feature Engine LÀ authoritative owner của Feature fact
    (owns_authoritative_state: true, Package 1.3-B).
  tự tính lại Context — Context Aggregator LÀ designated producer của eligible,
    cursor-bounded Context projection record (owns_authoritative_state: false, projection,
    rebuildable — Package 1.3-B, KHÔNG authoritative source, §9 dưới; correction v0.2,
    đóng `P13C-A-MIN-01`/`P13C-IRB-MIN-01` — trước đây gộp nhầm Feature Engine và Context
    Aggregator chung một nhóm "authoritative source DUY NHẤT", SAI vì hai module có
    `owns_authoritative_state` khác nhau).
  thực hiện Risk Policy evaluation — risk-gateway (Package 1.3-D).
  tạo Execution Intent — execution-engine (Package 1.3-D); forbidden_dependencies chứa
    execution-engine/paper-execution-boundary (§2).
  route order — cùng lý do trên.
  cho phép authoritative Decision creation qua bất kỳ module nào khác — module-registry.yaml
    v0.4 §2 xác nhận: KHÔNG module nào khác trong toàn 23-module inventory có
    owns_authoritative_state: true VÀ implements_capabilities: [decision-management] —
    decision-authority-service là entry DUY NHẤT thỏa cả hai điều kiện (xem §10 cho script
    verification).
```

## 8. Decision non-bypass requirements (bắt buộc, yêu cầu task — tuyên bố tường minh)

```text
Plugin output KHÔNG PHẢI một Decision — nó là candidate analytical/advisory signal
  (module-registry.yaml v0.4 §2, strategy-plugin-host notes).

Evaluation proposal KHÔNG PHẢI một Decision — nó là non-authoritative deterministic
  evaluation output (module-registry.yaml v0.4 §2, decision-evaluation-engine
  responsibilities).

CHỈ Decision Authority Service được thiết lập một authoritative Decision — xem §7.2.

Risk Gateway CHỈ được tiêu thụ authoritative Decision/Trade Intent output — KHÔNG được
  tiêu thụ raw plugin output HAY evaluation proposal. Xác nhận: risk-gateway.depends_on
  (module-registry.yaml v0.4) CHỈ chứa [decision-authority-service, account-service] —
  KHÔNG chứa strategy-plugin-host, KHÔNG chứa decision-evaluation-engine. risk-gateway
  notes (nguyên văn): "Risk Gateway consumes authoritative Decision output từ
  `decision-authority-service` (ADR-016 v0.8) — KHÔNG trực tiếp từ
  `decision-evaluation-engine` (non-authoritative)."

KHÔNG Strategy, Plugin Host, Context, Event Bus, projection, API surface, hay Decision
  Evaluation component nào được append authoritative Decision records — xem "Approved
  authoritative responsibility definition" của ADR-016 v0.8 (nguyên văn): "Decision
  Evaluation Engine: non-authoritative... Strategy Plugin Host: advisory output only...
  Context Aggregator/Event Bus/Projection: KHÔNG có Decision authority." Package 1.3-C
  bảo toàn nguyên vẹn bốn ràng buộc này, KHÔNG suy diễn thêm.
```

## 9. Context criticality và fail-closed handling (consume Package 1.3-B §8 UNCHANGED — bắt buộc, yêu cầu task)

**Xác nhận tường minh:** mục này trích dẫn NGUYÊN VẸN `feature-context-architecture.md` v0.2 (Package 1.3-B, `Consolidated Stable`) §8 "Context criticality và failure policy" — Package 1.3-C KHÔNG redefine, KHÔNG resolve `context.md` authority-terminology gap, KHÔNG gọi Context là authoritative domain-state owner.

```text
Decision Evaluation Engine (§6, module có dependency edge trực tiếp tới context-aggregator,
§2/§3) PHẢI fail closed khi (Package 1.3-B §8, nguyên văn ba điều kiện):
  (a) KHÔNG có eligible cursor-bounded MarketContextSnapshot projection record tương ứng
      tại computation cursor của Decision evaluation (absence);
  (b) lineage head applicable đang view_state: PENDING_CORRECTION;
  (c) required context_definition_version của Decision Evaluation Engine KHÔNG khớp
      context_definition_version đã pin tại snapshot có sẵn (definition-version mismatch).

Cả ba trường hợp là fail-safe-by-scope (I-6, Chapter 7 §7.4) tại consumer — Package 1.3-B
  chỉ pin YÊU CẦU boundary, KHÔNG author cơ chế/algorithm cụ thể; Package 1.3-C (tài liệu
  này) là nơi cơ chế đó ĐÁNG LẼ được author, NHƯNG vẫn KHÔNG author tại v0.1 này — chỉ ghi
  nhận Decision Evaluation Engine LÀ module chịu trách nhiệm implement yêu cầu boundary
  này (§13, forbidden scope: "author evaluation-proposal schema" và "author Strategy
  Plugin algorithm" cấm cả cơ chế cụ thể).
```

**Context KHÔNG BAO GIỜ được gọi là authoritative domain-state owner (xác nhận tường minh, đúng Package 1.3-B §5.1/§5.3):** `context-aggregator` vẫn `module_type: projection`, `owns_authoritative_state: false`, rebuildable, KHÔNG authoritative source cho upstream (Structure/Regime/Feature) hay business domain state (Strategy/Decision/Risk/Account/Position/Execution) — Package 1.3-C bảo toàn nguyên vẹn.

**Terminology (correction v0.2, đóng `P13C-A-MIN-01`/`P13C-IRB-MIN-01` — bắt buộc, KHÔNG resolve `context.md` terminology gap, KHÔNG đổi Context sang authoritative ownership):**

```text
Feature Engine LÀ authoritative owner của Feature fact (feature-engine,
  owns_authoritative_state: true, Package 1.3-B).

Context Aggregator LÀ designated producer của eligible, cursor-bounded Context projection
  record (context-aggregator, owns_authoritative_state: false, projection, rebuildable,
  Package 1.3-B) — KHÔNG phải authoritative source.

Decision Authority Service KHÔNG được tự tính lại CẢ HAI — không tính lại Feature fact (đó
  là Feature Engine's authoritative computation, Package 1.3-B §4), không tính lại Context
  projection (đó là Context Aggregator's as-of aggregation, Package 1.3-B §5.2).
```

Trước correction này, §7.3 (Decision Authority Service preserved boundary) gộp nhầm "Feature Engine/Context Aggregator" chung một nhóm "authoritative source DUY NHẤT" — SAI vì hai module có `owns_authoritative_state` khác nhau (`true` vs `false`); đã sửa tại §7.3 để tách bạch tường minh hai vai trò riêng biệt.

## 10. Determinism, replay và no-repaint

```text
Strategy Definition Version pinning (ADR-013, §4.3 trên):  bốn trục evidence độc lập,
  persistently resolvable tại computation cursor — KHÔNG mutable-latest, KHÔNG proxy.

Plugin Definition/compatibility pinning (Chapter 9 §9.1/§9.5):  exact Package/Build
  Artifact resolution (Mô hình A trực tiếp / Mô hình B immutable release manifest);
  validated compatibility set đồng bộ atomic tại activation boundary — Plugin Version một
  mình KHÔNG đủ, phải resolve duy nhất tới exact artifact đã qua parity-validate.

Decision evaluation definition/version pinning (nơi đã established, KHÔNG hơn):  bốn trục
  Strategy evidence (§4.3) VÀ decision_rule_ref (decision.md §5c, khớp đúng
  strategy_definition_version_id đang pin) ĐÃ established. MỘT trục "Decision Evaluation
  Engine implementation version" riêng (platform-owned evaluation logic version, tách biệt
  khỏi bốn trục Strategy) CHƯA established tại bất kỳ controlling source nào — carry
  forward tại §13 (cùng họ gap Definition Version registry mechanism).

Recorded-time visibility:  input_event.recorded_time ≤ cursor.recorded_time (ADR-010
  §2.4) — universal, mọi input evidence.

Effective-time eligibility:  decision_context_cursor relational invariants (Chapter 8
  §8.5.2, decision.md §3): cursor.recorded_time ≤ DecisionRecorded.recorded_time;
  lifecycle_event.recorded_time ≤ cursor.recorded_time; cursor.stream_registry_version
  khớp registry version mà input_contract_ref pin — vi phạm bất kỳ điều nào → invalid,
  PHẢI reject khi append.

Cursor-bounded replay:  decision_context_cursor = canonical Replay Cursor (Chapter 8
  §8.5.1) — recorded_time · input_contract_ref · stream_registry_version ·
  lifecycle_frontier · stream_positions. Thiếu field bắt buộc nào → invalid Decision
  event, phải bị từ chối khi append (decision.md §3).

Explicit causation/provenance:  causation_refs (Chapter 8 §8.2.3, ADR-009 §2.4) — mọi
  fact derived KHÔNG BAO GIỜ rỗng; DecisionRecorded PHẢI trỏ đúng evaluation attempt
  tương ứng (decision.md §5, one-way — attempt KHÔNG trỏ ngược Decision, đóng
  C4-DELTA-MAJ-01).

ADR-009 per-stream ordering, KHÔNG global sequence:  mỗi authoritative event thuộc đúng
  MỘT ordered stream, sequence liên tiếp trong stream; causal correctness qua
  causation_refs tường minh, KHÔNG global total order; cấm so sánh sequence thô xuyên
  stream khác nhau (Chapter 8 §8.3.3, ADR-009 §2.1/§2.2).

Mode parity (I-2):  cùng definition_version + cùng upstream causal ancestry → cùng tập
  fact/evaluation output, mọi execution mode (Live/Backtest/Paper/Replay) — ADR-010 §2.4:
  "mọi mode phải pin cùng một Input Contract version; cấm gắn hồi tố" khi so sánh/tái tạo
  cùng một logical Decision/run.

Append-only authoritative Decision correction/invalidation semantics (decision.md §11):
  DecisionRecorded KHÔNG mutable — correction LUÔN qua DecisionFactInvalidated +
  replacement DecisionRecorded MỚI (decision_id KHÁC, supersedes_fact_ref trỏ fact bị
  invalidate), cùng logical computation key (strategy_instance_id, decision_context_cursor)
  — KHÔNG nhảy cóc, cấm fork (tối đa một replacement trực tiếp).

No silent historical repaint (I-3):  replay tại cursor T chỉ thấy fact có recorded_time ≤
  T — invalidation/replacement ghi SAU T KHÔNG visible tại T (decision.md §12).
  DecisionRevalidated (ADR-010 §2.6 Append-and-Revalidate) là fact VẬN HÀNH riêng, KHÔNG
  phải correction — Decision gốc KHÔNG BAO GIỜ bị sửa/xóa dù registry transition khiến nó
  cần revalidate.
```

**Xác nhận tường minh (yêu cầu task — "Do not invent field-level contracts or ordering protocol implementation"):** mọi nội dung trên trích dẫn NGUYÊN VĂN semantic đã khóa tại ADR-009/ADR-010/ADR-013/`decision.md`/`strategy.md`/Chapter 8 — Package 1.3-C KHÔNG author field-level schema mới, KHÔNG author protocol implementation cụ thể của ADR-009 (per-stream sequence allocation, watermark/frontier mechanism — deferred Phase 1, ADR-009 §6).

## 11. Security / trust-boundary identification

```text
strategy-engine, strategy-plugin-host, plugin-release-manager, decision-evaluation-
  engine, decision-authority-service:  security_classification: none (module-registry.yaml
  v0.4, KHÔNG đổi) — không chạm external network boundary trực tiếp, không sở hữu
  credential/secret material. Cả năm tiêu thụ CHỈ internal authoritative event/query/
  command stream — external venue trust boundary đã cô lập hoàn toàn tại Market Data
  Ingestion (Package 1.3-A); exchange credential boundary thuộc Exchange Adapter/Custody-
  Signing Service (I-11, Chapter 9 §9.6, ngoài phạm vi năm module này).

Permission boundary (Chapter 9 §9.6, áp dụng cho Strategy Plugin Host là plugin-hosting
  module):  Declaration (Plugin Contract) → Grant (deployment/authorization config,
  KHÔNG suy từ declaration) → Enforcement (runtime authority tương ứng — Risk Gateway cho
  execution intent, Exchange Adapter/Signing Service cho credential) → Verification (I-7:
  network ACL/API authorization scope/event schema compatibility/command
  authorization/capability declaration/không truy cập storage module khác). `granted ⊆
  declared` — plugin vượt quyền là integrity violation, fail-safe (I-6). Package 1.3-C
  KHÔNG author enforcement/verification mechanism cụ thể — chỉ ghi nhận ranh giới đã
  khóa tại Chapter 9.
```

**Quality-gate triggers (phase-1-plan.md §8 Package 1.3-C block, KHÔNG redefine):** Trigger A áp dụng. Trigger C (Parity Test, Tier 1, decision-pipeline) deferred tới implementation NHƯNG PHẢI được thiết kế để pipeline tương lai pass được (parity-by-design — §10 trên). Trigger E CÓ ĐIỀU KIỆN nếu kiến trúc publish contract mới ngoài Domain Contract hiện có (Package 1.3-C KHÔNG publish contract mới tại v0.1 này — evaluation-proposal artifact vẫn CHƯA có Domain Contract, §13).

## 12. Preserved boundaries (xác nhận tường minh, yêu cầu task)

```text
Package 1.1 (module identity/taxonomy/dependency, v0.4, Consolidated Stable):  KHÔNG đổi
  — §2 trích dẫn nguyên văn, không thêm/sửa module hay edge nào.

Package 1.3-A (Structure/Regime independence, Feature Engine downstream role,
  Consolidated Stable):  KHÔNG chạm — ngoài phạm vi hoàn toàn của năm module trong
  Package 1.3-C.

Package 1.3-B (Feature selective fan-in, Context aggregation boundary, Context non-
  authority/rebuildability, Context criticality/fail-closed policy, Consolidated Stable):
  KHÔNG đổi — §9 trích dẫn nguyên vẹn, KHÔNG resolve context.md terminology gap.

ADR-016 v0.8 approved taxonomy decision (Candidate B/split, Mechanism A):  KHÔNG đổi —
  §6/§7 bảo toàn chính xác bốn authority guarantee đã Approved.

strategy.md v0.3/decision.md v0.3 (Package 0.2-C3/C4, Consolidated Stable):  KHÔNG đổi —
  mọi trích dẫn tại §4–§10 nguyên văn, KHÔNG redefine entity/event/invariant nào.

Chapter 9 Plugin Model (Locked):  KHÔNG đổi — bốn tầng identity (Plugin Definition/
  Version/Package-Build-Artifact/Runtime), Decision-time visibility (§9.5), published-
  contract-only interaction (§9.2) bảo toàn nguyên vẹn.
```

## 13. Preserved unresolved gaps (KHÔNG resolve, chỉ carry forward — bắt buộc, yêu cầu task)

```text
1. Plugin Host vs Decision Evaluation Engine exact responsibility boundary (ADR-016 v0.8
   Accepted risk #1, nguyên văn tại §5.3 trên) — "candidate analytical signal" (Plugin
   Host) vs "non-authoritative evaluation proposal" (Decision Evaluation Engine) KHÔNG có
   ranh giới CHÍNH XÁC; đòi hỏi Decision algorithm cụ thể (ngoài phạm vi kiến trúc).

2. Evaluation-proposal Domain Contract absent (ADR-016 v0.8 Accepted risk #2, §6.4 trên)
   — artifact "evaluation proposal" chưa có identity/schema/lifecycle/retention policy tại
   bất kỳ controlling source nào; decision.md's DecisionEvaluationAttemptRecorded LÀ một
   authoritative fact đã pin nhưng KHÔNG tường minh gán cho module nào emit nó (Decision
   Evaluation Engine hay Decision Authority Service) — mapping CHƯA resolve, Package
   1.3-C KHÔNG tự gán.

3. Authority-level proposal rejection lacks attempt_outcome semantics (ADR-016 v0.8
   Accepted risk #3, nguyên văn): "decision.md's attempt_outcome enum hiện tại
   (DECIDED/INELIGIBLE/INPUT_UNAVAILABLE/FAILED_BEFORE_EVALUATION) chưa có giá trị cho
   'proposal hợp lệ nhưng bị Decision Authority Service reject (stale/duplicate/
   invalid)'." Package 1.3-C KHÔNG invent giá trị attempt_outcome mới (cấm tường minh,
   ADR-016 + forbidden scope của task này).

4. DD-003 — PAPER-context authoritative Decision establishment mechanism remains
   unresolved (phase-1-plan.md §11, Deferred, đích Phase 1, mandatory TRƯỚC KHI UC-011
   runtime design). Package 1.3-C KHÔNG tự phát minh mechanism này — chỉ escalate, đúng
   explicit non-goal đã pin tại phase-1-plan.md §8 Package 1.3-C block.

5. context.md authority-terminology tension (Package 1.3-B §13, KHÔNG thay đổi) —
   "authoritative event record" (context.md §2) vs Type 2 Projection/
   owns_authoritative_state: false (module-registry.yaml, Chapter 7 §7.4) — carry forward
   nguyên vẹn tại §9 trên, Package 1.3-C KHÔNG resolve, KHÔNG re-mở.

6. ADR-009 concrete ordering protocol implementation — per-stream sequence allocation,
   watermark/frontier mechanism, late-arrival protocol, writer handoff/retirement
   protocol, storage/archive/retention policy — tất cả deferred sang Phase 1 (ADR-009
   §6), Package 1.3-C chỉ áp dụng nguyên tắc (§10 trên), KHÔNG author protocol cụ thể.

7. Definition Version registry mechanism — feature_definition_version/
   context_definition_version (Package 1.3-A/1.3-B, đã ghi nhận) CỘNG một khả năng tương
   tự cho Strategy Definition Version/Plugin Version/Configuration Version/Package-Build-
   Artifact/"Decision Evaluation Engine implementation version" (§10 trên) — cơ chế lưu
   trữ/versioning CỤ THỂ của mọi registry này là Phase 1 concern CHƯA elaborate
   (strategy.md §14, ADR-013 §9 tự defer).

8. Operational/dependency/replay complexity của Candidate B (ADR-016 v0.8 Accepted risk
   #4, ghi nhận cho đầy đủ dù KHÔNG nằm trong danh sách gap bắt buộc của task) — thêm một
   module/node/edge, hai điểm idempotency/replay-pin so với Candidate A — CHẤP NHẬN bởi
   Product Owner tại approval ADR-016, KHÔNG resolve/giảm thiểu tại Package 1.3-C.

9. Plugin Release Manager exact release-activation/compatibility mechanics (§5a.5, MỚI
   v0.2, đóng `P13C-IRB-MAJ-01` — elaboration nay hoàn tất, NHƯNG một số mechanics cụ thể
   vẫn CHƯA resolve, carry forward thay vì chọn implementation): lựa chọn cụ thể giữa Mô
   hình A (Decision pin trực tiếp artifact) và Mô hình B (immutable release manifest,
   Chapter 9 §9.1) cho hệ thống thực tế; fencing/transaction/deployment-coordinator
   mechanism cụ thể cho activation boundary (Chapter 9 §9.5 "có thể defer sang Phase 1
   design spec" — nguyên văn); capability matching algorithm cụ thể (Chapter 10,
   referenced KHÔNG redefine). Package 1.3-C KHÔNG chọn bất kỳ mechanism nào trong ba mục
   trên tại v0.2 này.
```

## 14. Explicit non-goals

```text
KHÔNG author field-level event schema (đã khóa tại strategy.md/decision.md, Package
  0.2-C3/C4, Consolidated Stable) — chỉ contract CATEGORY (event/query/command).
KHÔNG author Strategy Plugin algorithm.
KHÔNG author evaluation-proposal field-level schema (chưa tồn tại — §13 gap #2).
KHÔNG author plugin lifecycle state mới, capability type mới, activation protocol mới,
  release field-level schema, artifact-signing implementation, deployment topology, hay
  runtime isolation technology cho Plugin Release Manager (§5a.5).
KHÔNG redefine Strategy Definition/Strategy Instance/Plugin Definition identity (Chapter
  9 §9.3 đã khóa).
KHÔNG resolve DD-003 (PAPER-context Decision establishment mechanism) — chỉ tham chiếu
  như input còn thiếu (§13 gap #4).
KHÔNG author field-level API/database schema.
KHÔNG chọn framework/broker/database/deployment topology.
KHÔNG author source code hay test.
KHÔNG author Package 1.3-D (Risk/Execution semantics).
KHÔNG tạo/approve ADR nào — mechanical elaboration của ADR-016 KHÔNG cần ADR mới (đúng
  ADR rule của task — KHÔNG một Decision Pipeline topology mới, KHÔNG authority owner
  mới, KHÔNG bypass path, KHÔNG plugin type/capability mới, KHÔNG dependency ngoài
  Approved authority hiện có).
KHÔNG redefine module identity/taxonomy/dependency đã pin tại Package 1.1
  (module-registry.yaml/system-decomposition.md v0.4, Consolidated Stable).
KHÔNG redefine Package 1.3-A/1.3-B content (Consolidated Stable).
KHÔNG resolve context.md terminology tension (§9/§13 gap #5).
KHÔNG mark Package 1.3-C Consolidated Stable.
KHÔNG pass Gate 2.
KHÔNG tuyên bố Phase 1 hoàn thành.
KHÔNG mở Phase 2.
KHÔNG authorize Live.
```

## 15. Review and consolidation conditions

```text
Review A scope:               Decision Pipeline topology không vi phạm I-2 (Decision
                               Parity) by design (§10); Plugin hosting boundary đúng
                               Chapter 9 §9.2 (published contract only, §5); sole Decision-
                               authority proof (§7/§8) verified script-checkable qua
                               forbidden_dependencies/depends_on (§3/§10); KHÔNG recreate
                               decision-engine (§2); module boundary elaboration (§4–§5a/
                               §6/§7) nhất quán với module-registry.yaml v0.4 (Consolidated
                               Stable) — không silent semantic invention; Plugin Release
                               Manager (§5a) KHÔNG host plugin execution, KHÔNG chạm
                               Context/Decision/Risk/Execution authority; Context
                               criticality (§9) trích dẫn nguyên vẹn Package 1.3-B, KHÔNG
                               redefine; Context terminology correction (§7.3/§9, đóng
                               `P13C-A-MIN-01`/`P13C-IRB-MIN-01`) đúng — Feature Engine
                               authoritative owner, Context Aggregator designated
                               producer, KHÔNG gộp chung; mọi gap (§13) carry forward
                               trung thực, KHÔNG bị silently resolved (đặc biệt §13 gap
                               #1/#2/#3/#9, ADR-016 Accepted risks).
Independent Review B
  scope:                      Độc lập xác nhận DD-003 KHÔNG bị tự resolve ngầm ở tầng
                               architecture (§13 gap #4) — mechanism cụ thể vẫn phải
                               escalate; xác nhận Risk Gateway KHÔNG có đường consume nào
                               khác ngoài decision-authority-service (§8, script-check
                               risk-gateway.depends_on); xác nhận KHÔNG evaluation-proposal
                               schema nào bị author (§6.4/§13 gap #2); xác nhận
                               attempt_outcome KHÔNG bị thêm giá trị mới (§13 gap #3); xác
                               nhận §3 "reconciliation" statement không bị đọc nhầm thành
                               một dependency edge module-registry mới; xác nhận Plugin
                               Release Manager vs Strategy Plugin Host distinction (§5a.4)
                               không rò rỉ execution/hosting responsibility chéo nhau; xác
                               nhận `plugin-release-manager.depends_on`/
                               `forbidden_dependencies` (rỗng cả hai, §5a.1) khớp CHÍNH
                               XÁC module-registry.yaml v0.4, KHÔNG bị diễn giải thêm.
Product Owner decision
  point:                      Sau Review A/B CLEAN.
Consolidation condition:      Zero unresolved Blocker/Major; ADR Decision-Pipeline-
                               topology (nếu có — KHÔNG phát sinh tại v0.1 này) Approved;
                               DD-003 vẫn explicit Deferred, không bị đóng ngầm.
```
