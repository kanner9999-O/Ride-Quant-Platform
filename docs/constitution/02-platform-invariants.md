---
id: 02-platform-invariants
title: Platform Invariants
version: "3.1"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-18"
next_review: null
depends_on: ["00-governance", "01-vision"]
---

# 2. Platform Invariants (Bất biến — áp dụng cho MỌI chiến lược, không thương lượng)

Đây là ranh giới quan trọng nhất của toàn bộ Constitution: **Platform Invariants khác với Strategy-level Philosophy.** Platform Invariants áp dụng cho toàn hệ thống, không phụ thuộc trường phái chiến lược nào. Triết lý của một chiến lược cụ thể (ví dụ "giữ vị thế đến khi bị vô hiệu hóa thay vì TP cố định" của Ride Negation Strategy) **không được** đưa vào đây — nó thuộc về `strategy.json`/metadata của riêng chiến lược đó.

Mỗi invariant có cấu trúc: **Statement** (phát biểu) · **Required guarantees** (bắt buộc đảm bảo) · **Prohibited behavior** (hành vi bị cấm) · **Scope** (áp dụng ở đâu) · **Verification** (làm sao kiểm chứng tuân thủ).

---

### I-1 — Explainability

**Statement:** Mọi Decision và Risk Action phải tái dựng được từ immutable evidence trong một causation trace duy nhất — decision inputs phải được frozen tại decision time, còn subsequent outcomes (execution intent, acknowledgment, fill, rejection...) phải được capture bất biến tại đúng thời điểm chúng được quan sát, nối vào cùng trace qua correlation/causation chain.

**Required guarantees:**
- Input data snapshot tại decision time.
- Model/strategy version + strategy instance ID; configuration version; code/build version.
- Risk policy/version áp dụng tại thời điểm đó.
- Correlation/causation chain nối các event liên quan.
- Decision time (Event Time, xem [05-time-model.md](./05-time-model.md)).
- External dependency snapshot nếu có (xem I-5).
- Execution intent và outcome liên quan.

**Prohibited behavior:**
- Suy luận lại lý do quyết định sau khi xảy ra, khi không có evidence lưu sẵn.
- Xóa/ghi đè evidence đã capture.

**Scope:** Toàn bộ Decision Pipeline (Structure/Regime/Feature → Strategy → Decision → Risk Gateway → Execution).

**Verification:** Mọi Decision/Risk Action production phải vượt trace-completeness validation (100%, không phải mẫu). CI thực hiện sample-based deep reconstruction trên volume lớn; audit định kỳ chọn mẫu sâu để xác nhận không có evidence bị thiếu.

---

### I-2 — Decision Parity

**Statement:** Với cùng input event log, configuration, strategy/model version và deterministic state, Replay, Backtest, Paper Trading và Live phải tạo ra **cùng một Decision**.

**Required guarantees:**
- Cả 4 execution mode (Replay/Backtest/Paper/Live) dùng chung decision logic và event pipeline — không có 2 codebase logic khác nhau cho research và production.
- Execution outcome được phép khác nhau (do liquidity, latency, slippage, partial fill, rejection, venue behavior) — nhưng mọi khác biệt phải được capture và giải thích được.

**Prohibited behavior:**
- Coi khác biệt ở execution outcome là "vi phạm Parity" — Parity nằm ở tầng **Decision**, không phải tầng **Execution Result**.
- Dùng logic quyết định khác nhau giữa các mode.

**Scope:** Decision pipeline; cả 4 execution mode.

**Verification:** Golden event-log test · canonical semantic-decision hash comparison theo **Decision Contract authoritative** (danh sách field cụ thể sống trong Domain/Event Contract ở `/docs/domain/`, KHÔNG hardcode trong Constitution — tránh vi phạm I-12 khi Decision Contract thay đổi) · runtime identity, transport metadata, và processing metadata phải bị loại khỏi canonicalization · configuration/version equality check.

---

### I-3 — No Repaint / No Look-Ahead

**Statement:** Một output đã publish không được sửa hoặc xóa; thay đổi phải biểu diễn bằng event mới. Engine không được sử dụng dữ liệu chưa tồn tại tại decision time để tạo, xác nhận, hoặc backdate output.

**Required guarantees:**
- Append-only event history (event immutability).
- Trạng thái `provisional/candidate` và `confirmed` có semantic riêng, phân biệt rõ.
- Replay tại thời điểm T chỉ được quan sát thông tin đã biết và publish không muộn hơn T.

**Prohibited behavior:**
- Backdate một event mới như thể nó đã tồn tại trước đó.
- Dùng dữ liệu tương lai (so với decision time) để sinh hoặc xác nhận output ở quá khứ — kể cả khi event log vẫn giữ tính append-only (event immutability KHÔNG tự động đảm bảo No Repaint).

**Scope:** Mọi Compute Engine phát sinh output theo thời gian (Structure, Regime, Feature, Strategy...).

**Verification:** Look-ahead audit test — so sánh output tại Replay time T với đúng tập dữ liệu available tại T, bao gồm cả trường hợp bitemporal (xem [05-time-model.md](./05-time-model.md)): dữ liệu có `effective/event time` khác với `knowledge/recorded time` (ví dụ candle thuộc 10:00 nhưng bị correction lúc 10:07) — Replay tại 10:03 không được thấy correction đó, dù event_time của candle là 10:00.

---

### I-4 — Strategy Isolation

**Statement:** Strategy/Decision Engine không bao giờ được gọi trực tiếp Exchange API.

**Required guarantees:** Mọi trade intent phải đi qua Risk Gateway trước khi tới Execution Engine.

**Prohibited behavior:** Strategy/Decision Engine tự thực thi lệnh hoặc truy cập Exchange Adapter trực tiếp.

**Scope:** Strategy Engine, Decision Engine, Risk Gateway, Execution Engine.

**Verification:** Static dependency scan (Strategy/Decision module không import/reference Exchange Adapter) · Runtime architecture test — mọi `ExecutionIntentAccepted` phải truy vết được tới một `RiskApproved` ancestor, không có risk approval chain thì execution bị reject · Network-policy test — Strategy/Decision không có egress tới exchange endpoint · Credential audit — Strategy/Decision không sở hữu exchange credential.

---

### I-5 — Decision-Time Observable Dependency

**Statement:** Mọi dependency không thể đảm bảo tái tạo nguyên trạng sau này — feature flags, risk limits, configuration, model artifact, venue metadata, exchange filters, clock/calendar/session definitions, funding rate, sentiment, LLM output... — khi được dùng để ra quyết định, phải được ghi thành event bất biến tại thời điểm capture.

**Required guarantees:** Replay chỉ đọc lại event đã lưu, không bao giờ gọi lại nguồn ngoài/service khác lúc replay. Với dependency lớn (model artifact, calendar dataset, venue metadata đầy đủ), được phép capture bằng **immutable, content-addressed reference kèm checksum** thay vì inline toàn bộ binary vào event. **Trước khi Replay execution bắt đầu**, mọi referenced artifact phải được resolve và materialize vào một self-contained replay bundle hoặc local immutable cache — tách rõ 2 giai đoạn: *Replay preparation* (được phép resolve immutable artifact qua mạng) và *Replay execution* (không được phụ thuộc network).

**Prohibited behavior:** Query lại nguồn ngoài hoặc config service lúc Replay execution thay vì đọc snapshot đã lưu tại decision time. Dùng reference dạng mutable (ví dụ "latest-model" hoặc URL có nội dung có thể đổi) thay vì immutable content-addressed reference. Coi content-addressed reference là đủ để đảm bảo offline — nếu artifact chưa materialize trước khi Replay execution, Replay vẫn có thể fail khi cắt mạng.

**Scope:** Mọi input non-deterministic hoặc mutable-over-time dùng trong Decision Pipeline.

**Verification:** Self-contained replay test — Replay execution chỉ đọc event đã lưu và immutable artifact đã được materialize + xác thực checksum + tham chiếu từ event; không gọi lại mutable external source hoặc service. Sau bước materialization (Replay preparation), ngắt toàn bộ network; Replay execution vẫn phải chạy thành công và checksum của mọi artifact phải khớp.

---

### I-6 — Fail-Safe by Scope

**Statement:** Khi không thể xác định tính đúng đắn của dữ liệu, trạng thái, risk hoặc execution trong một scope, hệ thống phải chuyển scope đó về trạng thái an toàn. Mặc định không được mở thêm risk-increasing exposure; chỉ các risk-reducing action được fail-safe policy cho phép mới được thực hiện.

**Required guarantees:** Phạm vi dừng phải nhỏ nhất nhưng đủ để bảo toàn an toàn — có thể là symbol, strategy, account, exchange, hoặc toàn platform tùy mức độ ảnh hưởng. Safe state phải chặn action làm **tăng risk** theo risk model authoritative, nhưng vẫn cho phép risk-reducing action được policy cho phép: cancel, reduce-only, close, hedge, hoặc controlled unwind. Hedge có thể làm tăng **gross exposure** (thêm vị thế ở venue khác) nhưng chỉ được phép khi risk policy xác định nó làm giảm **tổng risk** theo risk model authoritative — không phải mọi hành động "tạo position mới" đều bị cấm, chỉ hành động làm tăng risk mới bị cấm.

**Prohibited behavior:**
- Một lỗi ở thành phần read-only/projection không critical (ví dụ Explainability projection lag, dashboard chết) làm dừng toàn platform.
- Một lỗi ảnh hưởng decision/risk/execution bị xử lý với phạm vi quá hẹp, để lan ra ngoài scope cần thiết.
- Fail-safe chặn luôn risk-reducing action cần thiết, khiến exposure hiện tại không thể được giảm (liên kết trực tiếp với I-8).
- Hiểu "không phát sinh exposure mới" theo nghĩa đen tuyệt đối đến mức cấm cả hedge hợp lệ (hedge luôn tăng gross exposure dù giảm net risk) — hoặc ngược lại, gắn nhãn "risk-reducing" cho mọi hedge mà không qua risk model authoritative xác nhận.

**Scope:** Mọi Compute Engine, Projection, Runtime Service.

**Verification:** Fault injection test theo từng scope (symbol/strategy/account/exchange) — xác nhận blast radius đúng thiết kế, không quá rộng cũng không quá hẹp. Bổ sung assertion: action được fail-safe cho phép không làm tăng risk theo risk metric/policy authoritative, kể cả khi gross position danh nghĩa tăng do hedge.

---

### I-7 — Plugin Non-Bypass

**Statement:** Module mở rộng (plugin/extension) không được mặc định trở thành thành phần nội bộ của Decision Pipeline. Plugin mới chỉ được tương tác qua published contracts; muốn tham gia Decision Pipeline phải được khai báo và kiểm soát như Strategy Plugin/Decision Advisor.

**Required guarantees:** Plugin chỉ tương tác qua versioned event, query/read contract, và command contract đã công bố (không phải khái niệm "Core Engine" chung chung — xem [07-module-taxonomy.md](./07-module-taxonomy.md) cho 3 loại module thật: Compute Engine/Projection/Runtime Service).

**Prohibited behavior:** Plugin gọi trực tiếp implementation nội bộ hoặc mutable state của module khác.

**Scope:** Mọi Plugin (Strategy, AI Decision Advisor...).

**Verification:** Contract compliance test — plugin chỉ gọi qua published interface, không import module nội bộ khác. Trong hệ thống polyglot/distributed, bổ sung: network ACL check · API authorization scope check · event schema compatibility check · command authorization check · capability declaration check · kiểm tra plugin không truy cập trực tiếp storage thuộc module khác (ví dụ query thẳng database của Position Ledger) — bypass không nhất thiết xuất hiện dưới dạng import code.

---

### I-8 — Kill Switch / Circuit Breaker

**Statement:** Hệ thống phải hỗ trợ kill switch ở cấp platform, account, strategy, và exchange.

**Required guarantees:** Circuit breaker của một exchange KHÔNG mặc định làm dừng các exchange độc lập khác — NHƯNG Risk Gateway phải được phép **pause, cancel, hedge, reduce, hoặc controlled unwind theo risk policy đã định nghĩa** đối với mọi strategy, account, hay position có dependency/exposure liên quan đến exchange đang gặp sự cố. Ví dụ: khi một chân hedge nằm trên exchange bị lỗi, chân còn lại nằm trên exchange vẫn hoạt động bình thường vẫn có thể phải bị pause, hedge, reduce hoặc unwind theo policy để tránh naked exposure. Unwind KHÔNG phải nghĩa vụ tự động thực hiện mỗi khi có sự cố — quyết định pause/cancel/hedge/reduce/unwind tuân theo risk policy, vì unwind vội có thể khóa lỗ, mất hedge khi venue lỗi phục hồi, hoặc tạo market impact không cần thiết khi state chưa reconcile.

**Prohibited behavior:** Coi per-exchange isolation là tuyệt đối đến mức không cho phép Risk Gateway can thiệp cross-exchange khi có dependency thật (arbitrage, hedge).

**Scope:** Risk Gateway, Execution Engine, mọi Exchange Adapter.

**Verification:** Cross-exchange dependency fault test — ví dụ kịch bản arbitrage 2 sàn, một sàn bị circuit breaker kích hoạt, xác nhận Risk Gateway chọn đúng policy action (pause/cancel/hedge/reduce/controlled unwind), áp dụng đúng dependency scope, và không tác động tới phần độc lập.

---

### I-9 — Numerical Precision

**Statement:** Giá trị tài chính authoritative — price, quantity, fee, balance, PnL, risk limit — phải dùng decimal/fixed-point với precision và rounding rule được định nghĩa theo instrument/venue.

**Required guarantees:** Financial values nhận từ authoritative source (exchange price, fill quantity, fee, balance, tick size, lot size) phải được **parse trực tiếp từ lossless representation** (decimal string hoặc scaled integer) sang decimal/fixed-point — **không được round-trip qua floating point ở bất kỳ bước nào** (chuyển float→decimal sau đó không phục hồi được precision đã mất). Analytical float (model confidence, volatility estimate, normalized score, indicator output) chỉ được trở thành financial intent thông qua một **explicit quantization boundary** — áp dụng instrument precision, tick size, lot size, rounding mode, và validation rule rõ ràng.

**Prohibited behavior:** Dùng float trực tiếp để đại diện giá trị tài chính authoritative. Để giá trị từ nguồn authoritative (price/quantity/fee/balance) đi qua float tại bất kỳ bước trung gian nào trước khi thành decimal — kể cả khi bước cuối cùng convert đúng rule, vì precision đã mất từ bước float không thể phục hồi.

**Scope:** Position Ledger, Execution Engine, Risk Gateway — ranh giới (boundary) giữa Feature Engine (analytical float được phép) và Execution/Ledger (bắt buộc lossless decimal từ đầu đến cuối).

**Verification:** Lossless-ingestion test cho exchange price/quantity/fee/balance (xác nhận không có bước float trung gian, **kể cả ở tầng deserialization** — nhiều JSON parser mặc định (JS `JSON.parse`, Python `json.loads` với số thực) tự động convert số thành float64 ngay khi đọc response từ Exchange, trước khi logic nghiệp vụ kịp xử lý; phải dùng parser decimal-aware ngay từ tầng nhận dữ liệu, không chỉ ở tầng lưu Ledger) · Quantization-boundary test cho analytical output khi chuyển thành financial intent · Property-based test tại các giá trị sát tick/step boundary (ví dụ `0.1 + 0.2`, min quantity, fee rounding, partial fill aggregation).

---

### I-10 — Idempotent Execution Effect

**Statement:** Mỗi execution intent phải có identity bất biến. Mọi venue order, child order, và execution attempt phát sinh từ intent đó phải có identity deterministic, duy nhất trong scope của venue, và truy vết được về intent gốc.

**Required guarantees:** Trước khi retry ở trạng thái không xác định (timeout, response thất lạc...), Execution phải reconcile với venue bằng client order ID, order status, và execution history. Một execution intent có thể sinh nhiều child order hoặc execution attempt theo Execution Policy (order slicing, TWAP/VWAP, cancel-replace, retry sau terminal rejection, route qua nhiều venue), nhưng tổng economic effect không được vượt quá intent đã được Risk Gateway phê duyệt. Retry của cùng attempt phải reconcile bằng cùng venue/client identity. Một child order mới chỉ được tạo khi state machine xác nhận đó là economic action mới được phép, không phải retry mù của action trước.

**Prohibited behavior:** Retry, timeout, hoặc recovery tạo thêm economic effect ngoài intent ban đầu (idempotency key tự thân KHÔNG đủ đảm bảo điều này). Hiểu sai quan hệ intent-order thành 1:1 cứng nhắc, cấm order slicing/multi-attempt hợp lệ.

**Scope:** Execution Engine, Exchange Adapter.

**Verification:** Chaos test cho lost response/timeout · Cancel-replace test · Partial-fill remainder test · Multi-child execution test · Aggregate economic-effect assertion ở cấp intent (tổng effect của mọi child order không vượt approved intent).

---

### I-11 — Secrets & Custody Isolation

**Statement:** API key, secret, private key không bao giờ được lưu dạng plaintext (bắt buộc qua Vault/KMS).

**Required guarantees:** Chỉ Exchange Adapter hoặc dedicated Custody/Signing Service được phép sử dụng exchange credential trực tiếp. Execution Engine tương tác qua contract (gửi execution command), không cần đọc raw secret trừ khi được triển khai cùng trust boundary với Adapter.

**Prohibited behavior:** Strategy/Decision Engine được cấp quyền truy cập trực tiếp secret của sàn. Execution Engine được cấp quyền đọc raw secret rộng hơn cần thiết khi không thuộc cùng trust boundary với Exchange Adapter.

**Scope:** Toàn hệ thống, đặc biệt Execution Engine, Exchange Adapter.

**Verification:** Access-control audit — xác nhận chỉ Exchange Adapter hoặc dedicated Custody/Signing Service được phép **sử dụng (use)** credential trực tiếp (không nhất thiết đọc raw secret — KMS/signing service có thể ký request mà không bao giờ trả secret cho caller). Execution Engine không có quyền đọc raw secret, trừ khi deployment manifest chứng minh nó nằm trong cùng trust boundary với Adapter và quyền đó đã được phê duyệt rõ ràng.

---

### I-12 — Single Source of Truth

**Statement:** Mỗi concept và scope phải có một authoritative source được chỉ định rõ.

**Required guarantees:** Mỗi loại concept khai báo đúng authoritative source tương ứng:
- Runtime facts và decision history → durable append-only event log.
- Document version/status/Decision Log/Open Questions → `MANIFEST.md`.
- Architecture decisions → ADR tương ứng.
- Platform rules → Constitution.
- Domain concepts và ubiquitous language → Domain Contract trong `/docs/domain/`.

Projection, cache, index, dashboard, và materialized view là **derived representation** — chúng phải tham chiếu hoặc rebuild được từ authoritative source tương ứng ở trên, KHÔNG tự thân là nguồn sự thật.

**Prohibited behavior:**
- Coi transport mechanism (Redpanda, Kafka, hay công nghệ thay thế sau này) tự động là source of truth — authority nằm ở durable append-only log, không phải công nghệ transport cụ thể.
- Gọi tài liệu authoritative (MANIFEST.md, ADR, Domain Contract) là "bản sao dẫn xuất" của event log — chúng là nguồn sự thật cho concept riêng của chúng (document status, decision record, domain concept), không phải projection của runtime data.
- Hiểu "một nguồn sự thật" thành "toàn platform chỉ 1 database duy nhất" — đúng ra là **một authoritative source per scope/concept**.

**Scope:** Toàn hệ thống — cả runtime (Event Log) lẫn authoritative documentation như MANIFEST.md, ADR, Constitution, và Domain Contract.

**Verification:** Mọi derived representation (projection, cache, dashboard...) phải có thể rebuild hoặc đối chiếu hoàn toàn từ authoritative source của đúng concept đó.

---

### I-13 — State Transition Integrity

**Statement:** Mọi entity có vòng đời trạng thái chỉ được chuyển trạng thái qua transition được khai báo tường minh trong state machine authoritative của entity đó. Không transition nào được chấp nhận chỉ vì trạng thái kết quả "trông có vẻ hợp lý".

**Required guarantees:**
- Mỗi entity type phải có state machine authoritative gồm tập state, tập transition hợp lệ và transition semantics, được sở hữu bởi Domain Contract tương ứng tại `/docs/domain/`.
- Mọi authoritative state change phải được biểu diễn bằng append-only transition event. Mutable projection/materialized state được phép cập nhật từ event đó nhưng không phải authoritative source và phải rebuild được theo I-12.
- State machine phải khai báo rõ state nào là terminal hoặc strictly terminal, cùng transition correction, reconciliation, hoặc supersession được phép, nếu có (Constitution không tự áp đặt "mọi terminal state = zero outbound transition" cho mọi entity — đó là quyết định của từng Domain Contract).
- Concurrent transition attempt trên cùng entity phải được resolve deterministic bằng version/concurrency contract; không được tạo ra hai transition xung đột từ cùng một authoritative state/version.

**Prohibited behavior:**
- Thực hiện transition không tồn tại trong state machine authoritative.
- Thực hiện outbound transition từ strictly terminal state, hoặc transition correction/supersession không được khai báo tường minh.
- Thay đổi authoritative state bằng direct mutation hoặc database update bypass transition validation và transition-event emission (phân biệt rõ: Authoritative state transition ≠ Derived state projection update — projection update hợp lệ theo I-12, mutation trực tiếp bypass event thì không).
- Định nghĩa state machine domain cụ thể (danh sách state/transition thật) trong Platform Invariants thay vì Domain Contract.

**Scope:** Mọi entity có vòng đời trạng thái được khai báo trong Domain Contract hiện tại hoặc tương lai (ví dụ minh họa, không phải danh sách đóng: Position, Order, Risk Decision, Strategy Instance, Portfolio, Session).

**Verification:** Property-based test trên transition graph authoritative · illegal-transition test (ví dụ trừu tượng: thử `StateA → StateC` khi graph chỉ cho phép `StateA → StateB → StateC`, xác nhận bị reject) · strictly-terminal/correction test · concurrent transition test · Replay state reconstruction test (rebuild state cuối từ chuỗi transition event, so khớp Domain Contract).
