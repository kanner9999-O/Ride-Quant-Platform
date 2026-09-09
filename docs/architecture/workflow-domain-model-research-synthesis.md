# Workflow Domain Model Research Synthesis — n8n, Temporal, Camunda, Zapier, Make

> **Status:** RESEARCH / EXPLORATION — NON-AUTHORITATIVE
>
> **Purpose:** lưu lại các căn cứ nghiên cứu và kết luận trao đổi về Workflow để dùng cho các vòng thiết kế RIDE sau này.
>
> **Scope:** từ lúc phân tích domain model của **n8n** đến phần tổng hợp **n8n + Temporal + Camunda + Zapier + Make** và proposal Workflow cho RIDE.
>
> **Important:** tài liệu này **KHÔNG phải ADR, KHÔNG phải Domain Contract, KHÔNG thay đổi architecture hiện hành, KHÔNG tự authorize Workflow Engine mới**. Phần RIDE proposal chỉ là design candidate / research basis.
>
> **Repository baseline khi ghi tài liệu:** `main` tại `c1e7823c219a972058e4d24de76700f0a479a3b8` (2026-09-09).

---

## 1. Bối cảnh nghiên cứu

Điểm xuất phát là việc `Strategy` và `Workflow` trong RIDE có nguy cơ bị hiểu lẫn nhau.

Ví dụ trading được dùng xuyên suốt:

```text
1. Check D1 candle is green
2. Check W1 candle is green
3. Check >6 green M15 candles in London session
4. Wait for 3 red M15 candles
5. Enter order
6. Manage position
```

Nhìn từ góc user, đây rõ ràng là một luồng công việc trading. Nhưng điều đó không tự động có nghĩa:

```text
Strategy = Workflow
```

và càng không có nghĩa:

```text
Strategy Engine = Workflow Engine
```

Nghiên cứu 5 platform nhằm trả lời:

- Workflow thực sự gồm những domain nào?
- `Node`, `Step`, `Task`, `Action`, `Execution`, `Run` khác nhau ra sao?
- Definition và runtime nên tách thế nào?
- Strategy đứng ở đâu so với Workflow?
- RIDE hiện tại đã có những mảnh nào?
- Nếu bổ sung Workflow sau này thì nên thêm ở layer nào để không phá architecture hiện hành?

---

# PART I — PLATFORM RESEARCH

## 2. n8n — Node Graph / Technical Composition

### 2.1. Worldview

```text
n8n
=
Workflow
  ↓
Node Graph
  ↓
Execution
```

n8n lấy **technical composition** làm trung tâm. User ghép technical building blocks thành graph và engine chạy graph đó.

Các domain chính:

```text
Workflow Definition
Trigger / Event
Flow Control / Orchestration
Execution Runtime
Data
Integration / Action
State / Persistence
AI / Agent
Reliability / Observability
Governance / Platform
```

### 2.2. Workflow Definition

Workflow là definition, không phải một lần chạy.

```text
Workflow
 ├── Node
 ├── Node
 └── Connection
```

### 2.3. Node

`Node` là technical object trên canvas.

Một Node thường có:

```text
type
configuration
credentials
input/output
parameters
```

Ví dụ:

```text
GetChatKannerDemo  ← Node
Code in Python     ← Node
```

### 2.4. “Add Node” vs “Execute step”

Đây là điểm đã được làm rõ trong trao đổi.

Khi thiết kế:

```text
Add Node
```

vì đang thêm một object vào graph.

Khi test riêng phần tử:

```text
Execute step
```

`step` ở đây chủ yếu là UX/process language: “chạy bước này của flow”. Nó không chứng minh rằng n8n có một first-class `Step` domain object độc lập song song với `Node`.

Cách nhớ:

```text
Node = technical graph object
Step = cách con người mô tả vai trò của phần tử trong flow
```

### 2.5. Node / Step / Run / Execution / Task

```text
Workflow Definition
│
├── Node A
├── Node B
└── Node C
```

Khi chạy:

```text
Execution #123
│
├── Node A run
├── Node B run
└── Node C run
```

- **Node** = technical definition/building block.
- **Step** = process/semantic/UX description; không nên mặc định là first-class runtime entity của n8n.
- **Node Run** = một lần Node thực sự execute.
- **Execution** = một lần toàn Workflow chạy.
- **Task** = không nên mặc định map với Node/Step; một business task có thể cần nhiều nodes.

### 2.6. Business Step không nhất thiết = Node

Ví dụ:

```text
Business Step:
Check D1 candle is green
```

có thể implement bằng:

```text
HTTP Binance Node
      ↓
Code Node
      ↓
IF Node
```

Tức:

```text
1 Business Step
=
3 technical Nodes
```

Ngược lại, một Code Node có thể chứa nhiều business steps.

**Kết luận quan trọng:**

> `Business Step ≠ Execution Node`.

### 2.7. Bài học n8n cho RIDE

Nên lấy:

- explicit graph composition;
- definition ≠ execution;
- execution inspection;
- visual workflow UX;
- branching/wait;
- integration components.

Không nên copy nguyên:

> Không để mọi semantic domain element = `Node`.

---

## 3. Temporal — Durable Workflow Runtime

### 3.1. Worldview

```text
Temporal
=
Workflow Code
  ↓
Durable Workflow Execution
  ↓
Event History / Replay
```

Temporal giải quyết bài toán process sống lâu, có state, external side effect, wait, crash/network failure nhưng vẫn phải tiếp tục chính xác.

### 3.2. Domain model

```text
Namespace
Workflow
  ├── Workflow Type
  ├── Workflow Definition
  └── Workflow Execution
Activity
  ├── Activity Definition
  └── Activity Execution
Event History
Task
  ├── Workflow Task
  └── Activity Task
Task Queue
Worker
Interaction
  ├── Signal
  ├── Query
  └── Update
Time
  ├── Timer
  └── Schedule
Reliability
  ├── Retry Policy
  ├── Timeout
  ├── Heartbeat
  ├── Continue-As-New
  └── Child Workflow
```

### 3.3. Workflow Definition ≠ Workflow Execution

```text
Workflow Definition
      ↓ instantiate
Workflow Execution #1
Workflow Execution #2
...
```

### 3.4. Workflow không phải Node Graph

Temporal workflow thường là code:

```python
if condition:
    ...

for item in items:
    ...

await timer
```

Control flow của programming language chính là orchestration definition.

### 3.5. Activity

Workflow quyết định:

```text
What should happen next?
```

Activity thực hiện:

```text
Do something in the outside world.
```

Ví dụ:

```text
Workflow
  ├── Activity: fetch market data
  ├── Activity: place order
  ├── Activity: notify
  └── Activity: write DB
```

### 3.6. Event History

Temporal giữ append-only history của Workflow Execution.

```text
WorkflowStarted
ActivityScheduled
ActivityStarted
ActivityCompleted
TimerStarted
SignalReceived
WorkflowCompleted
```

Sau crash:

```text
New Worker
   ↓
load Event History
   ↓
replay Workflow code
   ↓
reconstruct state
   ↓
continue
```

Đây là lesson quan trọng nhất của Temporal.

### 3.7. Task / Task Queue / Worker

Temporal `Task` là runtime dispatch unit, không phải business task.

```text
Temporal Service
      ↓
Task Queue
      ↓
Worker
```

### 3.8. Signal / Query / Update

```text
Signal = async command/event
Query  = read workflow state
Update = sync command + response
```

External event có thể đánh thức đúng existing execution.

### 3.9. Timer / Schedule

```text
Schedule → start Workflow
Timer    → pause/resume existing Workflow
```

Timer là durable primitive, không phải thread sleep.

### 3.10. Reliability

First-class:

```text
Retry
Timeout
Heartbeat
Cancellation
Continue-As-New
Child Workflow
```

Important trading lesson:

> External side effect không trở thành exactly-once chỉ vì dùng Temporal. Cần idempotency/reconciliation phù hợp.

### 3.11. Bài học Temporal cho RIDE

Nên lấy:

- Definition ≠ Execution;
- durable execution;
- history-driven reconstruction;
- wait/event primitive;
- signals vào existing execution;
- retry/timeout;
- external work separated from orchestration;
- child workflow;
- worker dispatch isolation.

Không nên copy nguyên:

- RIDE đã có authoritative Event Log; tránh tạo competing history authority.

---

## 4. Camunda — Executable Business Process Model

### 4.1. Worldview

```text
Camunda
=
Business Process
  ↓
BPMN Process Model
  ↓
Process Definition
  ↓
Process Instance
```

Camunda lấy **business process semantics** làm trung tâm.

### 4.2. Domain model

```text
Process Application
│
├── BPMN Process Model
│    ├── Events
│    ├── Tasks
│    ├── Gateways
│    ├── Subprocesses
│    └── Sequence Flows
│
├── Process Definition
│    ↓
│  Process Instance
│    ├── Element Instances
│    ├── Variables / Scopes
│    ├── Jobs
│    ├── User Task Instances
│    ├── Messages
│    ├── Timers
│    └── Incidents
│
├── DMN Decisions
└── Forms
```

### 4.3. Task — business semantic

Camunda `Task` gần với **Business Step** hơn technical Node.

Task types:

```text
Service Task
User Task
Business Rule Task
Receive Task
Send Task
Script Task
Manual Task
```

Lesson:

> RIDE Step/Task domain nên có semantic rõ, không phải mọi thứ = generic node.

### 4.4. Definition ≠ Instance

```text
Process Definition
      ↓
Process Instance
```

và:

```text
BPMN Element
    ↓
Element Instance
```

### 4.5. Gateway

```text
Exclusive Gateway
Parallel Gateway
Inclusive Gateway
Event-Based Gateway
```

### 4.6. Event

```text
Start Event
Intermediate Event
End Event
Boundary Event
```

với semantics như:

```text
Message
Timer
Error
Escalation
Signal
Compensation
Terminate
```

### 4.7. Message Correlation

```text
Message Name
+
Correlation Key
```

Ví dụ:

```text
Trade #123
WAITING_FOR_FILL

ORDER_FILLED
correlationKey = order_123
```

### 4.8. Service Task → Job → Job Worker

```text
Service Task
    ↓ runtime
Job
    ↓
Job Worker
    ↓
External Service
```

`Task ≠ Job`.

### 4.9. Human Task

Camunda first-class hóa human work:

```text
AI proposes trade
      ↓
Trader Approval
      ↓
Place Order
```

### 4.10. Process ≠ Decision

Camunda tách BPMN và DMN:

```text
BPMN
=
what happens / when / next

DMN
=
given inputs, what decision is true?
```

RIDE lesson:

```text
Workflow = WHEN / WHAT NEXT
Strategy/Decision = WHAT DOES THIS MEAN / WHAT SHOULD BE DECIDED
```

### 4.11. Business Error ≠ Technical Failure

```text
Order rejected
```

là expected business outcome.

```text
Binance timeout
```

là technical failure.

Hai loại cần policy khác nhau.

### 4.12. Bài học Camunda cho RIDE

Nên lấy:

- business-semantic elements;
- Task/Event/Gateway/Decision/Wait/Subprocess separation;
- Definition ≠ Instance;
- human task extension;
- process logic ≠ decision logic;
- event correlation;
- business error ≠ technical failure.

Đây là nguồn lesson mạnh nhất cho **Workflow Definition domain**.

---

## 5. Zapier — Event-driven Integration Automation

### 5.1. Worldview

```text
Zapier
=
Event
  ↓
Zap
  ↓
Trigger + Steps
  ↓
App Actions
```

Zapier lấy integration automation làm trung tâm.

### 5.2. Domain model

```text
Account / Workspace
│
├── Apps
│    └── App Connections
│
├── Zap Definition
│    ├── Trigger Step
│    ├── Action Step
│    ├── Search Step
│    ├── Filter
│    ├── Paths
│    ├── Delay
│    ├── Loop
│    └── Sub-Zap
│
├── Zap Run
│    └── Step Runs
│
├── Data Mapping
├── History / Replay
└── Tables / Storage
```

### 5.3. Zap / Step / Zap Run / Step Run

```text
Zap Definition
   ├── Step
   └── Step

       ↓ execute

Zap Run
   ├── Step Run
   └── Step Run
```

### 5.4. Trigger / Action

```text
Trigger = something happened
Action  = do something
```

### 5.5. App ≠ App Connection

```text
Google Calendar
=
App / Integration Definition

Dung's Google Account
=
App Connection
```

RIDE analogue:

```text
Binance Adapter
      ↓
Connection
      ↓
Binance Account X
```

Workflow không nên sở hữu credential binding trực tiếp.

### 5.6. Capability model

Integration expose:

```text
Events / Triggers
Actions
Queries / Searches
```

Ví dụ exchange:

```text
Events:
OrderFilled
PriceUpdated

Actions:
PlaceOrder
CancelOrder
AmendOrder

Queries:
GetBalance
GetOrder
```

Workflow reference capability thay vì concrete API endpoint/class.

### 5.7. `Task` warning

```text
Zapier Task
≠
Camunda Task
≠
Temporal Task
```

Zapier Task chủ yếu là usage/billing unit.

### 5.8. Bài học Zapier cho RIDE

Nên lấy:

- Trigger/Action capability abstraction;
- Integration Definition ≠ Connection;
- workflow reference capability, không raw API;
- Definition/Run/Step Run separation;
- subworkflow.

Không nên copy:

- mọi semantic business thing = generic Step.

---

## 6. Make.com — Module Graph / Data-flow Automation

### 6.1. Worldview

```text
Make
=
Scenario
  ↓
Module Graph
  ↓
Bundle Data Flow
  ↓
Operations
```

Make nổi bật ở **data unit** và **execution unit**.

### 6.2. Domain model

```text
Scenario
│
├── Modules
│    ├── Trigger
│    ├── Search
│    ├── Action
│    └── Universal/API
│
├── Routes
│    ├── Router
│    └── Filters
│
├── Data transformation
│    ├── Iterator
│    └── Aggregator
│
├── Connections
├── Schedule / Webhook
└── Inputs / Outputs

      ↓ execute

Scenario Run
│
├── Cycle(s)
│    ├── Operations
│    └── Commit / Rollback
└── Bundles
```

### 6.3. Scenario / Module / Operation

```text
Scenario     = definition
Module       = technical building block
Scenario Run = one execution
Operation    = one module invocation
```

### 6.4. Bundle

Bundle là data unit.

```text
Module A
   ↓
Bundle(s)
   ↓
Module B
```

**Key lesson:**

> `Data Unit ≠ Execution Unit`.

### 6.5. Iterator / Aggregator

```text
Iterator   1 → N
Aggregator N → 1
```

Rất phù hợp multi-instrument/portfolio flows.

### 6.6. Router / Filter

```text
Router = topology branching
Filter = edge predicate
```

### 6.7. Transaction / ACID awareness

```text
Operations
   ↓
Commit
or
Rollback
```

Nhưng external side effect như:

```text
Place Exchange Order
```

không phải database rollbackable.

Trading cần:

```text
cancel
compensate
hedge
reconcile
```

### 6.8. Failure / incomplete execution

Make explicit hóa:

```text
Skip
Retry
Resume
Commit
Rollback
```

và recoverable incomplete execution.

### 6.9. Bài học Make cho RIDE

Nên lấy:

- Data Unit ≠ Execution Unit;
- fan-out/fan-in;
- Router/Filter;
- Connection boundary;
- transaction/side-effect awareness;
- recoverable failed execution;
- scenario input/output contract.

Không nên copy:

- `Everything = Module`.

---

# PART II — CROSS-PLATFORM SYNTHESIS

## 7. Phân loại 5 platform

| Platform | Abstraction trung tâm | Strength chính |
|---|---|---|
| **n8n** | `Workflow → Node Graph → Execution` | Technical composition / visual workflow |
| **Zapier** | `Trigger → Steps → App Actions` | Integration / capability abstraction |
| **Make** | `Scenario → Modules → Bundles → Operations` | Data-flow / fan-out / fan-in |
| **Camunda** | `Business Process → BPMN → Process Instance` | Business process semantics |
| **Temporal** | `Workflow Code → Durable Workflow Execution` | Durable runtime / recovery |

```text
n8n      = COMPOSITION-centric
Zapier   = INTEGRATION-centric
Make     = DATA-FLOW-centric
Camunda  = BUSINESS-PROCESS-centric
Temporal = DURABLE-RUNTIME-centric
```

Không có thằng nào tự nó là full model tối ưu cho RIDE.

---

## 8. Cross-platform concept matrix

| Domain | n8n | Zapier | Make | Camunda | Temporal |
|---|---|---|---|---|---|
| Whole definition | Workflow | Zap | Scenario | Process Definition | Workflow Definition |
| Structural technical unit | Node | Step | Module | BPMN Element | code construct |
| Business work semantic | weak/implicit | weak/implicit | weak/implicit | **Task first-class** | app semantics |
| Runtime whole | Execution | Zap Run | Scenario Run | Process Instance | Workflow Execution |
| Small runtime unit | Node run | Step Run | Operation | Element Instance / Job | Workflow/Activity Task |
| Data unit | Item/JSON | step data | **Bundle** | Variables | state/payload |
| Start | Trigger | Trigger | Trigger/Schedule/Webhook | Start Event | Start/Schedule |
| Branch | IF/Switch | Paths | Router/Filter | Gateway | code |
| External work | Integration Node | Action | Action Module | Service Task/Job | Activity |
| Wait | Wait | Delay | wait patterns | Timer/Message Event | Durable Timer |
| Existing execution interaction | webhook patterns | limited | webhook patterns | Message/Event | Signal/Query/Update |
| Subprocess | Sub-workflow | Sub-Zap | Subscenario | Subprocess/Call Activity | Child Workflow |
| Persistent state | external/DB | Tables/Storage | Data Store | Process Variables | Workflow state |
| Reliability | retry/error | Replay | Incomplete Execution | Retry/Incident | Event History/Retry |
| Human work | integration-based | integration-based | integration-based | **User Task** | app-level |
| Decision separation | weak | weak | weak | **DMN** | application code |
| Connection binding | Credentials | **App Connection** | **Connection** | Connector/Worker | Activity impl |

---

## 9. Terminology warning

Cùng một từ ở các platform có thể mang semantic khác hoàn toàn.

### `Task`

```text
Zapier Task
=
usage/billing unit

Camunda Task
=
business/process work unit

Temporal Task
=
runtime dispatch unit
```

RIDE phải tự định nghĩa semantic nội bộ.

### `Node` vs `Step`

```text
Node
=
technical graph component

Business Step
=
semantic process unit
```

Không khóa invariant:

```text
1 Step = 1 Node
```

---

# PART III — LESSONS FOR RIDE

## 10. Definition ≠ Execution

RIDE nên có:

```text
WorkflowDefinitionVersion
        ↓ instantiate
WorkflowExecution
```

và:

```text
Step Definition
        ↓
Step Execution
```

---

## 11. Business Step ≠ Technical Component

Domain layer nên nói:

```text
Evaluate Setup
Wait Pullback
Evaluate Risk
Submit Execution
Wait Fill
Manage Position
```

Không nên nói bằng:

```text
PythonNode
HttpNode
KafkaNode
IfNode
```

---

## 12. Workflow ≠ Decision Logic

Workflow trả lời:

```text
WHEN?
WHAT NEXT?
WAIT FOR WHAT?
WHICH PATH?
```

Strategy/Decision trả lời:

```text
WHAT DOES MARKET STATE MEAN?
IS ENTRY VALID?
WHAT DECISION SHOULD BE PRODUCED?
```

Ví dụ đúng:

```text
Decision Engine
    ↓
ENTRY_VALID = true

Workflow Router
    ↓
if ENTRY_VALID → Risk
else → End/Wait
```

Workflow không nên hard-code Strategy rules nếu đó là authority của Strategy/Decision.

---

## 13. Integration/Capability ≠ Connection

```text
Integration / Adapter
      ↓ exposes
Capabilities
      ↓ bound through
Connection
      ↓
External Account/System
```

Ví dụ:

```text
Binance Adapter
├── Query: GetOrder
├── Query: GetBalance
├── Action: PlaceOrder
├── Action: CancelOrder
└── Event: OrderFilled

Connection
↓
Binance Account A
```

---

## 14. Data Unit ≠ Execution Unit

Candidate conceptual split:

```text
ExecutionItem
=
data moving through workflow

StepExecution
=
execution work performed
```

Một Step có thể:

```text
1 input → N outputs
N inputs → 1 output
```

---

## 15. Wait / Event phải first-class

Không nên:

```python
while not filled:
    sleep(1)
```

Nên:

```text
WaitStep
  event = OrderFilled
  correlation = order_id
  timeout = 30s
```

Runtime:

```text
WorkflowExecution = WAITING
```

---

## 16. Runtime phải recoverable

```text
Authoritative Event Log
      ↓ fold/replay
Workflow Execution State
```

Trading workflow sống nhiều giờ/ngày không được mất state sau restart.

---

## 17. Retry ≠ Blind Retry

```text
FetchMarketData
```

có thể safe retry.

```text
PlaceOrder
```

sau network timeout có thể ambiguous.

Cần các policy kiểu:

```text
RetryPolicy
TimeoutPolicy
IdempotencyPolicy
FailurePolicy
CompensationPolicy
ReconciliationPolicy
```

External financial side effect thường cần reconcile/cancel/offset/hedge, không phải generic rollback.

---

## 18. Definition phải immutable/versioned

```text
Execution #123 → WorkflowDefinitionVersion v2
```

Deploy v3:

```text
existing #123 → vẫn v2
new #124      → v3
```

Không dùng mutable `latest` cho historical execution.

---

## 19. Visual Editor là representation layer

```text
UI Node
    ↓ represents
Workflow Step
```

Canvas không được ép domain model thành `Node`.

---

# PART IV — CURRENT RIDE CONSTRAINTS

## 20. Strategy hiện tại không phải Workflow

Current `docs/domain/strategy.md` định nghĩa hai concept:

```text
Strategy Definition Version
Strategy Instance
```

và scope hiện tại nói rõ Strategy không phải:

```text
strategy DSL
executable code
optimizer/backtest engine
Trade Intent / Decision / Risk / Execution
Live activation workflow
```

Không nên sửa Strategy thành Workflow chỉ vì một Strategy của user trông giống sequence.

---

## 21. Không nên khóa `Strategy ⊂ Workflow`

Sau nghiên cứu 5 platform, model sạch hơn là:

```text
Strategy
=
trading / decision semantics

Workflow
=
orchestration semantics
```

Quan hệ:

```text
Workflow
   ↓ uses/references
Strategy Instance
```

hoặc:

```text
Strategy Instance
   ↓ participates in
Workflow Execution
```

Không cần ontology subset.

---

## 22. RIDE đã có chỗ cho Workflow Orchestrator

Current Chapter 7 có:

```text
Type 3 — Runtime Service
```

sở hữu runtime interaction/orchestration/coordination/control.

Internal scheduler, workflow coordinator, replay controller đều phù hợp Runtime Service.

Candidate:

```text
workflow-orchestrator
module_type: runtime_service
```

Không cần module taxonomy type mới.

---

## 23. Workflow Orchestrator không được thành god module

Workflow chỉ nên sở hữu:

```text
ordering
coordination
routing
waiting/resume
retry/timeouts
execution lifecycle
subworkflow coordination
```

Không sở hữu lại:

```text
Feature Engine
Regime/Structure
Strategy / Decision
Risk Gateway
Execution Engine
Exchange Adapter
```

---

# PART V — PROPOSED RIDE WORKFLOW DOMAIN (CANDIDATE)

## 24. Synthesis proposal

> **Camunda-like ở Domain Definition.**
>
> **Temporal-like ở Runtime Execution.**
>
> **Zapier-like ở Capability / Integration Boundary.**
>
> **Make-like ở Data Flow.**
>
> **n8n-like ở Visual Editor / Composition UX.**

Đây là chọn abstraction, không phải copy platform.

---

## 25. Layered model

```text
                 DOMAIN / DEFINITION LAYER

Strategy Domain
      │ reference/use
      ↓
Workflow Definition
      ├── Trigger
      ├── Business Steps
      ├── Transitions
      └── Policies

────────────────────────────────────────────

                    RUNTIME LAYER

Workflow Orchestrator
      ↓
Workflow Execution
      ↓
Step Execution
      ↓
Wait / Resume / Retry / Timeout / Compensation

────────────────────────────────────────────

                  CAPABILITY LAYER

Capability
      ↓
Runtime Module / Adapter
      ↓
Connection
      ↓
External System / Venue

────────────────────────────────────────────

                 DATA / STATE LAYER

Authoritative Event Log
Execution Items / Fact References
Timers / Correlations
Workflow Execution projection/state
```

---

## 26. Proposed Definition Model

```text
WorkflowDefinition
      │
      └── WorkflowDefinitionVersion
              ├── Trigger
              ├── Steps
              │    ├── ComputeStep
              │    ├── DecisionStep
              │    ├── WaitStep
              │    ├── ActionStep
              │    ├── SubworkflowStep
              │    └── HumanTaskStep [future]
              └── Transitions
                   ├── unconditional
                   └── conditional
```

`WorkflowDefinitionVersion` phù hợp với strong version/evidence/replay requirements của RIDE.

---

## 27. Proposed Step semantics

### ComputeStep

Invoke compute capability như Feature/Regime/Structure.

Không chứa logic engine bên trong Workflow.

### DecisionStep

Invoke Strategy/Decision semantics.

Workflow consume domain result để route.

### WaitStep

```text
event_type
correlation_policy
timeout_policy
```

### ActionStep

Invoke side-effect capability.

Cần failure/idempotency semantics rõ.

### SubworkflowStep

Composition boundary.

### HumanTaskStep [future]

Extension path cho:

```text
manual approval
trade review
risk override request
operator recovery
```

---

## 28. Transition model

Transition route theo result đã được authority phù hợp tạo ra.

```text
DecisionStep
  output = ENTRY_VALID
      ↓
Conditional Transition
  ENTRY_VALID == true
      ↓
RiskStep
```

Routing không tự tạo Strategy decision.

---

## 29. Proposed Runtime Model

```text
WorkflowExecution
├── workflow_definition_version_ref
├── execution_id
├── parent_execution_ref?
├── scope/context
├── status
├── started_at
└── completed_at?
```

```text
StepExecution
├── workflow_execution_ref
├── step_ref
├── attempt
├── status
├── inputs / refs
├── outputs / refs
├── started_at
├── completed_at?
└── failure / result
```

Illustrative states only:

```text
CREATED → RUNNING → WAITING / FAILED / CANCELLED / COMPLETED
```

```text
PENDING → RUNNING → SUCCEEDED / WAITING / FAILED / CANCELLED
```

Exact enums chưa được quyết định.

---

## 30. Execution History proposal

Không tạo competing history chỉ vì Temporal có Event History.

Candidate:

```text
RIDE Authoritative Event Log
        ↓ fold/replay
Workflow Execution State
```

Illustrative events:

```text
WorkflowExecutionStarted
StepExecutionStarted
StepExecutionSucceeded
WorkflowWaiting
WorkflowSignalReceived
StepExecutionFailed
StepExecutionRetried
WorkflowExecutionCompleted
```

Tên/schema chưa authorized.

---

## 31. External Event Correlation

Ví dụ:

```text
Place Order
   ↓
WaitStep
  event = OrderFilled
  correlation = order_id
   ↓
Manage Position
```

Runtime phải xác định event nào thuộc execution/step nào bằng identity/correlation contract rõ ràng.

---

## 32. Capability Binding

Workflow Definition không phụ thuộc concrete implementation.

```text
Step
  capability_ref: risk.evaluate
```

Resolver:

```text
risk.evaluate
   ↓
Risk Gateway
   ↓
published contract
```

External:

```text
execution.place_order
   ↓
Execution Engine / Exchange Adapter
   ↓
Connection
   ↓
Venue Account
```

---

## 33. Data Flow

Không dùng một giant mutable JSON context làm authority.

Ưu tiên:

```text
immutable values
+
authoritative fact/event refs
+
execution-local derived values
```

Candidate primitive:

```text
ExecutionItem
```

Tên provisional.

Use cases:

```text
fan-out
fan-in
mapping
aggregation
per-item execution
```

---

## 34. Failure Policy

Candidate concepts:

```text
RetryPolicy
TimeoutPolicy
IdempotencyPolicy
FailurePolicy
CompensationPolicy
ReconciliationPolicy
```

Distinction bắt buộc:

```text
Expected business outcome
≠
Technical failure
```

Ví dụ:

```text
RiskRejected = normal business result
Binance timeout = technical failure
```

và:

```text
OrderRejected = execution/business outcome
Unknown submission after timeout = ambiguous side-effect state
```

---

## 35. Strategy ↔ Workflow

Không redesign Strategy để làm Workflow.

Candidate relationship:

```text
WorkflowDefinitionVersion
      ↓ references
StrategyInstance
```

Ví dụ:

```text
Workflow: London Intraday Trading

Wait London Open
  ↓
Prepare Inputs
  ↓
Evaluate Strategy
  ↓
Decision Valid?
  ↓
Risk Evaluate
  ↓
Submit Execution
  ↓
Wait Fill
  ↓
Manage Position
```

Strategy sở hữu strategy semantics; Workflow sở hữu orchestration semantics.

---

## 36. Không phải mọi Strategy đều cần Workflow

Nếu chỉ:

```text
inputs
  ↓
Strategy evaluation
  ↓
Decision
```

thì current pipeline có thể đủ.

Workflow đáng dùng khi có:

```text
multi-step orchestration
wait / timer
long-running state
cross-module coordination
retry / recovery
external event
human approval
fan-out/fan-in
subworkflow
```

Ví dụ:

```text
Wait London Open
  ↓
Evaluate
  ↓
Wait Pullback
  ↓
Enter
  ↓
Wait Fill
  ↓
Manage Position for hours
  ↓
Exit
```

---

# PART VI — IMPLEMENTATION STRATEGY

## 37. Recommended rollout

### V1 — Domain Model only

Author minimal concepts:

```text
WorkflowDefinitionVersion
Trigger
Step
Transition
WorkflowExecution
StepExecution
```

Initial Step semantics:

```text
Compute
Decision
Wait
Action
Subworkflow
```

Không visual editor.
Không giant DSL.
Không generic agent framework.

### V2 — Runtime Coordinator

Implement bounded runtime:

```text
start
sequential step
conditional branch
wait/resume
timeout
retry
complete/fail
```

Execution state reconstructable từ current RIDE event architecture.

Likely module:

```text
workflow-orchestrator
module_type: runtime_service
```

Exact module identity cần governance process bình thường.

### V3 — Advanced runtime

Chỉ thêm khi real use case justify:

```text
fan-out / fan-in
parallel branches
signals/updates
subworkflow lifecycle
compensation
human task
advanced scheduling
```

### V4 — Visual Workflow Editor

Sau cùng mới build n8n/Make-style UX:

```text
Canvas
Nodes
Connections
Execution visualization
Debug/run state
```

UI Node chỉ represent domain Step.

---

## 38. What not to build first

Không bắt đầu bằng:

- drag/drop canvas;
- universal `Node` abstraction;
- custom DSL;
- duplicate event/history system;
- god Workflow Engine sở hữu Strategy/Risk/Execution;
- exactly-once fantasy cho exchange side effects;
- distributed scheduler quá sớm;
- human task system khi chưa có use case;
- thay tất cả Strategy evaluation bằng Workflow.

Bắt đầu từ semantic boundaries + runtime boundaries, rồi mới UI.

---

# PART VII — STATUS / OPEN QUESTIONS

## 39. Conclusions strongly supported

1. **Definition và execution phải tách.**
2. **Business Step và technical component phải tách.**
3. **Workflow orchestration và Strategy/Decision semantics không được conflated.**
4. **Workflow Orchestrator coordinate capability hiện có, không thay ownership.**
5. **Wait/external event/correlation phải first-class cho long-running trading workflow.**
6. **External side effects cần idempotency/reconciliation, không generic rollback.**
7. **Workflow definition phải immutable/versioned; execution pin exact version.**
8. **RIDE Event Log là candidate tự nhiên cho durable workflow evidence.**
9. **Integration/Adapter và Connection/account binding phải tách.**
10. **Visual Node không được quyết định domain model.**

---

## 40. Candidate decisions — NOT APPROVED

Các suggestion sau chưa phải authority:

```text
WorkflowDefinitionVersion
Business-semantic Step taxonomy
workflow-orchestrator Runtime Service
ExecutionItem
Capability reference binding
Workflow execution events in Event Log
Camunda-style definition + Temporal-style runtime
```

---

## 41. Open questions

1. Exact Workflow aggregate boundaries.
2. Có `WorkflowDefinition` family entity riêng hay chỉ `WorkflowDefinitionVersion`.
3. Exact Step taxonomy.
4. `Condition` là Step hay Transition predicate.
5. `Trigger` thuộc Definition hay start-policy/subscription riêng.
6. Exact execution events.
7. Exact execution lifecycle.
8. Correlation contract cho external events.
9. Step input/output contract.
10. Capability registry authority/resolver.
11. Retry/idempotency/compensation ownership.
12. Fan-out/fan-in deterministic ordering.
13. Workflow compatibility/version migration.
14. Existing execution khi deploy version mới.
15. Subworkflow cancellation/lifecycle.
16. Human Task/operator intervention.
17. Visual serialization/editor model.
18. Backtest/Replay/Paper/Live parity của Workflow.
19. Workflow là new Domain Context hay primarily Runtime Service capability.
20. Concrete first trading use case đủ mạnh để justify implementation.

---

# PART VIII — FINAL SYNTHESIS

## 42. One-line lesson from each platform

```text
n8n
→ technical composition + visual execution UX

Zapier
→ Trigger/Action capability + Integration/Connection separation

Make
→ Data Unit vs Execution Unit + fan-out/fan-in + side-effect awareness

Camunda
→ explicit business process semantics

Temporal
→ durable execution + waiting + recovery + history-driven runtime
```

---

## 43. Final candidate architecture statement

> **Workflow là một orchestration domain/layer độc lập. Nó không thay Strategy, Decision, Risk hay Execution. Workflow Definition mô tả bước nào xảy ra, theo thứ tự/điều kiện/event nào; Workflow Runtime giữ lifecycle durable của một execution; từng Step gọi capability thuộc module có authority đúng; external side effects dùng idempotency/reconciliation/compensation phù hợp; execution evidence dùng lại authoritative Event Log của RIDE; visual Node editor nếu có chỉ là representation layer.**

```text
Camunda-like business semantics
        +
Temporal-like durable runtime
        +
Zapier-like capability/connection boundary
        +
Make-like data flow
        +
n8n-like visual composition UX
        ↓
RIDE Workflow Orchestration
```

---

## 44. Boundary quan trọng nhất

```text
Strategy
≠
Workflow
≠
Workflow Engine
```

More precisely:

```text
Strategy
=
trading / decision semantics

Workflow
=
orchestration definition / process semantics

Workflow Engine / Orchestrator
=
runtime mechanism executing that definition
```

Và:

```text
Workflow may USE a Strategy Instance.
Strategy does not need to BECOME a Workflow.
```

---

## 45. Related current RIDE authorities

Đọc research note này cùng các authority hiện hành:

- `docs/domain/strategy.md`
- `docs/constitution/07-module-taxonomy.md`
- `docs/constitution/08-event-model.md`
- `docs/constitution/02-platform-invariants.md`
- `docs/architecture/module-registry.yaml`

Nếu proposal trong research note xung đột với authority hiện hành, **authority hiện hành thắng** cho tới khi governed change được approve.

---

## 46. Scope note — Reclaim.ai

Reclaim.ai cũng được nghiên cứu trong cùng conversation nhưng được phân tích riêng như một `policy-driven time-allocation / schedule-optimization` domain. Nó **không thuộc 5-platform Workflow synthesis** này.

Nếu cần, Reclaim nên thành một research note riêng về:

```text
Intent
Desired State
Scheduling Policy
Agent
Time Allocation
Preview Plan vs Live Calendar State
```

---

**End of research synthesis.**
