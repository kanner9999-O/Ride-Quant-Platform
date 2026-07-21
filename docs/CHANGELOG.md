# Changelog — Ride Quant Platform Docs

Format dựa theo [Keep a Changelog](https://keepachangelog.com/), áp dụng cho toàn bộ `/docs`.

## [v0.1] — 2026-07-16 (Phase 0, đang tiến hành, chưa release chính thức)

### Added
- Constitution 15 chương (00-governance → 14-roadmap), tách thành docs-as-code.
- Platform Invariants I-1 → I-11.
- Domain Principles, Time Model, Identity Model, Module Taxonomy.
- Event Model, Plugin Model, Compatibility & Capability Contract.
- ADR Process, Approval Gates, Quality Gates, Roadmap.
- MANIFEST.md (lockfile ghim version/status toàn bộ docs).
- ADR-001 (Event Sourcing), ADR-002 (Strategy Isolation), ADR-003 (Regime Engine Split) — ghi hồi tố các quyết định đã chốt qua thảo luận nhưng chưa từng thành file.
- ADR-004 → ADR-005: Governance Model v1 (Tri-party 3/3 + Blocking/Non-blocking + Challenge Round + Devil's Advocate).
- Folder structure: constitution/, adr/, domain/, architecture/, research/, meeting-notes/, templates/.

### Changed
- ADR-005 rev.2: đơn giản hóa Governance sau review của ChatGPT — bỏ luật 3/3 (Product Owner là approve authority duy nhất), bỏ Blocking/Non-blocking (thay bằng Concern/Risk/Recommendation), bỏ Devil's Advocate, gọn Challenge Round thành 1 field "Scale check" trong ADR template thay vì một quy trình riêng.
- Document status enum mở rộng: Not Started → Draft → In Review → Revision Requested → Approved → Locked (+ Deprecated/Superseded), thay cho "Debating".
- Thêm metadata chuẩn cho mọi file: owner, reviewers, approved_by, last_review, next_review.

### Open
- OQ-001: Data Retention Policy & Access Control Model — chưa quyết, cần trước Phase 1.
- Toàn bộ Constitution vẫn ở trạng thái `In Review`, chưa có Approval chính thức từ Product Owner.

## [Unreleased] — sau ChatGPT review round 3 (chuẩn bị Lock Chapter 0)

### Changed
- Tách vai trò **Product Owner** và **Chief Architect** thành 2 role độc lập (trước đó gộp chung) — cho phép delegate Chief Architect cho người khác trong tương lai mà không ảnh hưởng quyền Product Owner.
- Đổi "Architecture Discussion" → "Architecture Review" trong Decision Workflow (chuyên nghiệp hơn, ngụ ý có output/concern/recommendation).
- Decision Workflow: thêm trạng thái "ADR Accepted" trước "ADR Locked" (tách trạng thái quyết định khỏi hành động đóng băng tài liệu).
- `scale_check` template: thêm field `reason_if_no` — bắt buộc điền nếu `decision_still_valid: NO` nhưng vẫn quyết định tiến hành.
- **Single Source of Truth nâng thành Platform Invariant I-12** (trước đó chỉ là một rule trong Governance — tự mâu thuẫn với chính nguyên tắc SSOT nếu định nghĩa nó ở 2 nơi).
- Xóa cụm "Blocking Objection" còn sót trong lý giải của ADR-005 (khái niệm này đã bị loại bỏ khỏi Governance, không nên còn xuất hiện như đang tồn tại).

### Backlog (v1.1, Medium Priority — chưa làm ngay theo đề xuất ChatGPT)
- BL-001: `review_status` machine-readable trong metadata.
- BL-002: `Traceability` — related_constitution/related_domain/related_engine trong ADR frontmatter.

## [Unreleased] — sau ChatGPT review round 4 (9.8/10, recommend LOCK Chapter 0)

### Added
- **ADR Scope Rule (4b)** — bảng ADR Required / Optional / Not Required, tránh "cái gì cũng phải ADR".
- `created_at`, `approved_at` vào metadata mọi file (tách khỏi `last_review`).
- Ghi chú **Decision ≠ Documentation** (hệ quả của I-12) — mỗi loại tài liệu chỉ làm đúng 1 việc.

### Changed
- Tách quy tắc xung đột Product Owner/Chief Architect ra khỏi bảng Roles thành mục riêng **2b. Conflict Resolution**.
- Đổi "Technical Architect #1/#2" → "AI Technical Architect (ChatGPT)" / "(Claude)" — bỏ đánh số, future-proof cho AI khác tham gia sau này.
- ADR-005: sửa câu cảm tính "không có phản đối kỹ thuật nào đủ mạnh" → lý do kỹ thuật cụ thể (Trade-off accepted vì...).
- 11-adr-process.md: xác nhận ADR dùng chung Document Lifecycle (Mục 7) thay vì viết thêm "ADR Lifecycle" riêng — phát hiện: `Deprecated`/`Superseded` đã tồn tại sẵn ở đó, ChatGPT backlog item này thực ra đã được giải quyết, chỉ cần trỏ tham chiếu.

### Backlog (giữ nguyên, chưa làm)
- DoD cho từng Chapter (sẽ áp dụng bắt đầu từ Chapter 1 — Vision).
- BL-001, BL-002 (không đổi từ round trước).

## [Unreleased] — mở rộng Team Governance (chuẩn bị scale 1 → nhiều người)

### Added
- **`/docs/team/`** — tầng mới tách biệt hoàn toàn khỏi Constitution: `team.yaml` (gán Người/AI ↔ Role), `roles.md`, `responsibility-matrix.md` (RACI), `onboarding.md`.
- Role mới trong Governance: **Module Owner** (tránh 1 người ôm hiểu toàn bộ hệ thống khi Phase 3 bắt đầu).

### Changed
- **Sửa lỗi kiến trúc thật:** bảng Roles ở `00-governance.md` trước đó ghi thẳng "User"/"ChatGPT"/"Claude" — vi phạm chính nguyên tắc Role-vs-Person. Sửa thành: Constitution chỉ định nghĩa Role, việc gán Người/AI cụ thể chuyển sang `/team/team.yaml`.
- **Giữ nguyên vị trí ngang hàng giữa ChatGPT và Claude** (cả hai đều là "AI Technical Architect", không phân cấp) — phản đối đề xuất đặt Claude làm cấp dưới "Lead Technical Architect (ChatGPT)", vì sẽ làm mất giá trị 2 góc nhìn độc lập phản biện lẫn nhau đã chứng minh hiệu quả qua nhiều vòng review.
- Xác nhận: rule "Engineer không được tự đổi kiến trúc" không phải rule mới — đã được bao phủ bởi 4b (ADR Scope Rule), chỉ làm rõ áp dụng cho MỌI contributor.

### Note
- Toàn bộ thay đổi trong mục này **không chặn việc Lock Chapter 0** — theo đúng logic Role-vs-Person, nội dung `/team` nằm ngoài phạm vi Constitution.

## [Unreleased] — ADR-006: quyết định Product Owner đầu tiên khi 2 AI bất đồng

### Added
- **ADR-006** (Approved) — Product Owner quyết: ChatGPT và Claude giữ vai trò AI Technical Architect **ngang hàng**, khác nhau ở `focus` (ChatGPT: Discovery/consistency-check; Claude: Documentation/Implementation), không có hierarchy. Đây là ADR đầu tiên đạt trạng thái `Approved` chính thức từ Product Owner (các ADR-001~003 là ghi hồi tố, ADR-004 Superseded, ADR-005 vẫn `In Review`).
- `team.yaml` cập nhật field `focus` cho ChatGPT/Claude khớp ADR-006.

## [Milestone] — 2026-07-16 — 🔒 Chapter 0 (Governance) LOCKED

Product Owner chính thức Approve + Lock:
- `constitution/00-governance.md` → `Locked`
- `adr/ADR-005.md` (Lean Governance Model) → `Locked`
- `adr/ADR-006.md` (ChatGPT/Claude ngang hàng) → `Locked`

Từ thời điểm này, **ADR Immutable Rule có hiệu lực** với cả 3 file trên: không sửa trực tiếp, mọi thay đổi phải qua ADR mới (ADR-007+). Đây là mốc khóa chính thức đầu tiên của Ride Quant Platform — kết thúc ~5-6 vòng phản biện giữa Product Owner, ChatGPT, Claude.

**Next Milestone:** Chapter 1 — Vision.

## [Unreleased] — Vision v2.0 (soạn cùng ChatGPT) + ADR-007

### Added
- **ADR-007** (Locked) — chốt phạm vi Vision Phase 0-3: nội bộ (không multi-tenant/RBAC ngay) + crypto only (không đa tài sản ngay), nhưng kiến trúc chừa chỗ mở rộng qua `Account` first-class entity.
- `06-identity-model.md`: thêm `AccountID`, ghi rõ Account là entity first-class từ Phase 0.2 theo ADR-007.
- Vision v2.0: nội dung phong phú hơn nhiều từ bản soạn cùng ChatGPT (Core Beliefs, Product Principles, Non-Goals, Out of Scope, North Star), chuẩn hóa lại frontmatter khớp schema chung, thêm Mục 1.1 "Current Scope" phân biệt rõ Phase 0-3 vs Long-term Vision.

### Changed
- OQ-001: từ `Open` → `Partially Resolved` — hướng đã chốt (single-operator now, multi-tenant-ready later), thiết kế RBAC cụ thể vẫn mở nhưng không còn chặn Phase 1.

### Fixed (phát hiện khi review)
- Bản Vision nháp ban đầu (từ ChatGPT) ngầm định multi-tenant SaaS (Target Users nhiều nhóm độc lập) và bỏ mất phạm vi Crypto — mâu thuẫn với toàn bộ kiến trúc đã thiết kế (Position Ledger, Risk Gateway, I-9 Numerical Precision giả định crypto). Đã làm rõ qua ADR-007 trước khi hợp nhất vào 01-vision.md.

## [Unreleased] — Vision review round 2 (ChatGPT phản biện Claude)

### Fixed (Claude tự nhận sai lý luận, quyết định vẫn đúng)
- Issue #1 (Target Users): Claude từng suy luận "Target Users nhiều persona → ngầm định multi-tenant" — ChatGPT chỉ ra đây là 2 khái niệm tách biệt (Target Users = persona thiết kế tính năng, Deployment Model = hạ tầng chạy). Quyết định ở ADR-007 (nội bộ trước, chừa chỗ multi-tenant) vẫn đúng, chỉ sửa lại lý luận/câu chữ trong Vision (không mở ADR mới vì ADR-007 đã Locked và nội dung quyết định không đổi).
- Vision 1.3/1.5: thêm 2 câu rõ ràng (theo đề xuất chính xác của ChatGPT) — Ride ban đầu cho cá nhân/1 team, kiến trúc chừa chỗ multi-workspace/multi-tenant sau; Ride ban đầu cho Crypto, kiến trúc asset-agnostic để mở rộng sau.

### Changed
- Giảm overlap Vision/Mission/Long-term Vision (ChatGPT Issue #3): Mission (1.4) chỉ còn "What Ride does", bỏ câu trùng với Core Beliefs.
- Thêm Product Principle **"Everything Must Be Measurable"** (ChatGPT Issue #4) — đối xứng với tagline mở đầu (Explainable, Measurable, Continuously Improving), trước đó thiếu.
- Mở rộng BL-002 (Traceability, backlog) — thêm chiều Principle → ADR → Architecture theo đề xuất ChatGPT, không tạo backlog item mới trùng lặp.

## [Unreleased] — Vision review round 3 (ChatGPT, "Approve with required changes")

### Fixed — Critical
- **V2-01 (semantic error trong Parity/Reproducible):** Vision từng viết "cùng 1 kết quả bất kể execution mode" — SAI, vì execution outcome (fill, slippage, latency) được phép khác nhau giữa Live/Backtest/Paper. Sửa đúng bản chất: Parity nằm ở tầng **Decision** (phải giống nhau với cùng input/config/state), không phải tầng **Execution Result**. Bài học: paraphrase lại một Invariant (I-2) ở nơi khác có rủi ro làm sai lệch bản chất kỹ thuật — nhắc lại đúng tinh thần I-12.

### Fixed — Major
- **V2-02 (quá nhiều chi tiết implementation trong Vision):** gỡ bỏ chi tiết `AccountID`/Capability Matrix gate cụ thể khỏi Vision — chuyển thành **OQ-002** (Strategy Lifecycle Gate) trong Manifest, chỉ giữ nguyên tắc cấp cao "Research Before Capital".
- **V2-03 (1.1 và 1.3 lặp nhau):** 1.3 Product Positioning rút gọn chỉ còn phát biểu định vị sản phẩm, không lặp lại bảng Current Scope đã có ở 1.1.
- **V2-04 (Target Users phòng thủ quá mức):** bỏ ví dụ VSCode và lời giải thích tranh luận giữa 2 AI — không cần thiết cho người đọc Vision, lịch sử đã lưu ở ADR-007 + CHANGELOG.
- **V2-05 (Measurable chưa nối xuống đo lường):** thêm câu ràng buộc outcome ở Success Definition phải chuyển hóa thành leading/lagging indicators, KHÔNG nhét KPI chi tiết vào Vision — chuyển thành **OQ-003** (Product Metrics) trong Manifest.

### Added
- **OQ-002, OQ-003** trong MANIFEST.md — 2 chi tiết implementation được "trục xuất" khỏi Vision đúng chỗ, không mất thông tin, chỉ đổi nơi lưu.

### Note
- ChatGPT: "Approve with required changes — sau commit này, Approve & Lock Chapter 1, không cần thêm vòng rewrite lớn."

## [Unreleased] — Vision v2.2: Product Positioning phân tầng Identity/Capability (Product Owner trực tiếp yêu cầu)

### Changed
- 1.3 Product Positioning: tách "Quant Trading Platform" và "Trading Operating System" đang đứng ngang hàng (nối bằng "và") thành 2 tầng rõ ràng — **Identity** (Trading Operating System) và **Core Capability** (strategy-agnostic Quant Trading Platform) — khớp với cách câu mở đầu chương đã định danh Ride từ đầu.

## [Unreleased] — Vision v2.3: bỏ lặp Identity ở 1.3

### Changed
- Bỏ nhãn "Identity" khỏi 1.3 (đã tuyên bố ở câu mở đầu chương) — 1.3 giờ chỉ còn "Core Capability", trỏ ngược lại Identity đã nêu, tránh lặp.

## [Milestone] — 2026-07-17 — 🔒 Chapter 1 (Vision) LOCKED

Product Owner chính thức Approve + Lock `constitution/01-vision.md` (v2.3), sau 3 vòng review (ChatGPT + Claude) qua Vision v2.0 → v2.1 → v2.2 → v2.3.

Từ thời điểm này, **ADR Immutable Rule có hiệu lực** với `01-vision.md`: không sửa trực tiếp, mọi thay đổi phải qua ADR mới.

**Đã Locked tới nay:** Chapter 0 (Governance), Chapter 1 (Vision), ADR-005, ADR-006, ADR-007.

**Next Milestone:** Chapter 2 — Platform Invariants.

## [Unreleased] — Platform Invariants v2.0 (ChatGPT review: "Revision Requested" → xử lý toàn bộ)

### Fixed — Blocker
- **I-8 (Kill Switch):** câu cũ quá tuyệt đối ("circuit breaker 1 sàn không ảnh hưởng sàn khác") tạo lỗ hổng naked exposure cho strategy arbitrage/hedge đa sàn. Sửa: per-exchange isolation ở tầng hạ tầng vẫn giữ, nhưng Risk Gateway phải được phép pause/unwind cross-exchange khi có dependency/exposure thật.

### Fixed — Major
- **I-2 (Parity → Decision Parity):** thiếu Paper Trading mode, và là NGUỒN GỐC của lỗi semantic đã sửa ở Vision V2-01 — tôi từng sửa bản sao (Vision) mà quên sửa bản gốc (I-2). Nay sửa đúng tại nguồn: Parity ở tầng Decision, không phải Execution Result, đủ cả 4 mode.
- **I-3 (No Repaint → No Repaint/No Look-Ahead):** event immutability (append-only) KHÔNG tự động đảm bảo No Repaint — engine vẫn có thể look-ahead bias nếu không phân biệt provisional/confirmed. Bổ sung rõ.
- **I-6 (Fail-Safe → Fail-Safe by Scope):** "1 engine lỗi → dừng toàn platform" quá rộng, phá isolation, giảm availability. Thêm khái niệm blast radius/scope (symbol/strategy/account/exchange/platform).
- **I-10 (Idempotency Key → Idempotent Execution Effect):** idempotency key tự thân không đảm bảo exactly-once economic effect (exchange có thể nhận lệnh nhưng response thất lạc...). Yêu cầu reconciliation trước khi retry.

### Fixed — Minor
- I-1: mở rộng evidence cần capture (config version, code/build version, risk policy version, correlation chain...).
- I-5: mở rộng từ "external data" thành "decision-time observable dependency" (bao gồm cả feature flags, risk limits, config, model artifact — không chỉ nguồn ngoài).
- I-7: thay "Core Engine" (thuật ngữ không tồn tại trong Module Taxonomy) bằng contract cụ thể (versioned event/query/command contract).
- I-9: phân biệt giá trị authoritative (bắt buộc decimal) vs phân tích không-authoritative (float được phép, có boundary conversion).
- I-12: "Event Bus" chỉ là transport, sửa thành "durable append-only event log" làm authority; làm rõ "1 nguồn sự thật" = 1 authoritative source PER SCOPE, không phải 1 database duy nhất toàn platform.

### Changed
- Toàn bộ 12 invariant viết lại theo cấu trúc Statement/Required guarantees/Prohibited behavior/Scope/Verification — đủ để triển khai và test, thay vì mỗi invariant chỉ 1 dòng.

## [Unreleased] — Platform Invariants v2.1 (ChatGPT review round 2: "Approve with required changes")

### Fixed — Blocker
- **I-12 tự mâu thuẫn SSOT:** bản v2.0 gọi MANIFEST.md/Decision Log/Domain Model là "bản sao dẫn xuất có thể rebuild từ event log" — SAI, mâu thuẫn trực tiếp với Governance đã Locked (MANIFEST.md là authoritative cho document status, Domain Model là authoritative cho domain concept, không phải projection của event log). Sửa: phân biệt rõ authoritative source theo từng loại concept (runtime→event log, document status→MANIFEST, ADR→architecture decision, Domain Contract→domain concept), chỉ Projection/cache/index/dashboard mới là derived representation.

### Fixed — Major
- **I-6:** thêm rõ Fail-Safe by Scope KHÔNG được chặn risk-reducing action (cancel, reduce-only, close, hedge, controlled unwind) — chỉ chặn action làm TĂNG exposure.
- **I-2:** Verification đổi từ "decision hash comparison" (dễ fail sai do lẫn runtime metadata như DecisionID/timestamp/trace ID) sang "canonical semantic-decision hash" — chỉ hash payload nghiệp vụ, loại trừ metadata vận hành.

### Fixed — Minor
- I-1: Verification không còn dựa vào "1 decision ngẫu nhiên" — yêu cầu 100% trace-completeness cho production, CI sample-based cho volume lớn, audit định kỳ.
- I-5: cho phép immutable content-addressed reference + checksum cho dependency lớn (model artifact, calendar dataset) thay vì bắt buộc inline toàn bộ; cấm reference dạng mutable ("latest-model").
- I-11: siết least privilege — chỉ Exchange Adapter/Custody-Signing Service giữ raw secret, Execution Engine chỉ tương tác qua contract trừ khi cùng trust boundary.
- I-8: đổi "pause hoặc unwind" (nghe như nghĩa vụ) thành "pause/cancel/hedge/reduce/controlled unwind theo risk policy" (được phép, không phải bắt buộc luôn unwind) — tránh khóa lỗ/mất hedge khi xử lý vội.

## [Unreleased] — Platform Invariants v2.2 (ChatGPT review round 3, fetch trực tiếp GitHub blob SHA `252cd63`)

### Fixed — Major
- **I-11:** Required Guarantees và Verification từng nói NGƯỢC NHAU (Guarantee: Execution không đọc secret; Verification: xác nhận Execution có quyền đọc) — lỗi do sửa 1 phần không đồng bộ. Sửa Verification khớp Guarantee, đổi "read secret store" → "use credential" (KMS/signing service có thể ký mà không lộ raw secret).
- **I-5:** "immutable content-addressed reference" không tự động đảm bảo Replay offline được (artifact có thể chỉ nằm ở remote store). Tách rõ 2 giai đoạn: Replay preparation (được resolve artifact qua mạng) vs Replay execution (bắt buộc network-free) — verification đổi thành "self-contained replay test" sau khi materialize.
- **I-9:** Verification cũ vô tình hợp thức hóa "exchange price → float → decimal → Ledger", mất precision không phục hồi được. Sửa: giá trị authoritative (price/quantity/fee/balance) phải parse trực tiếp từ lossless representation, KHÔNG BAO GIỜ qua float ở bất kỳ bước nào; float chỉ dành cho analytical output, qua explicit quantization boundary khi thành financial intent.

### Fixed — Minor
- I-8: sửa câu ví dụ mâu thuẫn đại từ ("exchange lỗi" và "hoạt động bình thường" cùng câu) — làm rõ 2 chân hedge nằm trên 2 exchange khác nhau.
- I-4: Verification mở rộng — static import scan không đủ, thêm runtime test (`ExecutionIntentAccepted` phải trace tới `RiskApproved`), network-policy test, credential audit.
- I-7: Verification mở rộng — thêm network ACL, API authorization scope, event schema compatibility, command authorization, capability declaration, kiểm tra truy cập storage module khác.
- I-2: bỏ hardcode field list (strategy_instance, instrument...) khỏi Verification — nguy cơ tự vi phạm I-12 nếu Decision Contract đổi sau này. Trỏ về "Decision Contract authoritative" ở `/docs/domain/` (chưa tạo, sẽ có ở Phase 0.2).
- I-3: bổ sung yêu cầu test bitemporal (effective/event time vs knowledge/recorded time) cho trường hợp data correction, trỏ về Time Model.

### Added
- **BL-003** (Manifest) — Invariant Conformance Matrix, thuộc Architecture/Engineering Phase (không phải Constitution), chỉ làm khi module/contract thật tồn tại.
- **OQ-004** (Manifest) — Time Model (Chapter 5) cần bổ sung bitemporal, xử lý khi Chapter 5 vào vòng review riêng.

### Note
- ChatGPT: "Sau khi ba Major được sửa, Chapter 2 đủ điều kiện Approve & Lock." Không thêm Motivation/Examples/Severity vào 12 invariant (tránh phình tài liệu) — giữ nguyên khuyến nghị này.

## [Unreleased] — Platform Invariants v2.4 (ChatGPT review round 4, fetch blob SHA `657e33b`)

### Fixed — Major
- **I-1:** Statement cũ tự mâu thuẫn — đòi evidence "capture tại decision time" nhưng Required Guarantees lại yêu cầu "execution outcome" (chỉ tồn tại SAU decision time). Sửa: tách decision inputs (frozen tại decision time) khỏi subsequent outcomes (capture khi được quan sát), nối bằng causation/correlation chain.
- **I-10:** Statement cũ ngầm định quan hệ 1 execution intent → 1 client order (số ít), không hỗ trợ order slicing, TWAP/VWAP, cancel-replace, multi-venue routing — có thể khóa sai Execution model. Sửa: 1 intent → nhiều child order/execution attempt hợp lệ, miễn tổng economic effect không vượt quá intent đã approved; mỗi child order truy vết được về intent gốc.

### Fixed — Minor
- I-5: "Replay chỉ đọc event" chưa khớp việc Replay còn đọc immutable artifact bundle — làm rõ Replay execution đọc cả event lẫn artifact đã materialize+checksum.
- I-8: Verification cũ chỉ nói "pause", hẹp hơn Guarantee (cho phép pause/cancel/hedge/reduce/unwind) — mở rộng Verification khớp đủ các action.
- I-12: terminology không nhất quán ("Domain Contract" ở Required Guarantees vs "Domain Model" ở Scope) — ironic vì đây là invariant về SSOT. Chuẩn hóa dùng "Domain Contract" xuyên suốt.

### Cross-check (Claude tự xác nhận, không phải từ ChatGPT)
- Fix I-1 (causation chain) và fix I-10 (ExecutionIntentID → nhiều ChildOrderID) phải nhất quán với nhau — đã xác nhận: I-10 sinh nhiều child order, I-1 phải trace được toàn bộ qua đúng 1 causation chain. Hai fix củng cố lẫn nhau, không mâu thuẫn.

### Note
- I-3/Chapter 5 boundary: ChatGPT xác nhận ví dụ bitemporal hiện tại trong I-3 Verification là đúng kỹ thuật, không cần bỏ — chỉ nhắc khi review Chapter 5 phải giữ thuật ngữ khớp hoàn toàn với I-3.

## [Unreleased] — Platform Invariants v2.5 (ChatGPT review round 5, fetch blob SHA `a8879aa`)

### Fixed — Major
- **I-6:** Statement cũ "không phát sinh exposure mới" mâu thuẫn trực tiếp với Required Guarantees cho phép hedge (hedge luôn tăng GROSS exposure dù giảm NET risk). Sửa: phân biệt risk-increasing action (bị cấm) vs risk-reducing action theo risk model authoritative (được phép, kể cả khi tăng gross exposure) — ví dụ cụ thể: long 1 BTC exchange A, hedge short 1 BTC exchange B → net ~0 nhưng gross tăng gấp đôi, vẫn hợp lệ vì risk model xác nhận giảm net risk.

### Fixed — Minor
- I-7: Statement cũ "mọi module mới" quá rộng so với Scope thật (chỉ Plugin) — có thể vô tình áp cho Exchange Adapter, Custody/Signing Service, event storage, schema registry... không phải module nào cũng nên mặc định là Event Bus consumer. Thu hẹp về đúng phạm vi Plugin/extension module.

### Note
- 4 vòng liên tiếp (v2.0→v2.5): số vấn đề mới phát hiện giảm dần (6 → 4 → 5 → 2+3 → 1+1) — tín hiệu hội tụ rõ ràng, không phải vòng lặp tìm lỗi vô hạn.

## [Unreleased] — Platform Invariants v3.0: thêm I-13 State Transition Integrity (ChatGPT đề xuất, ⭐⭐⭐⭐⭐)

### Added
- **I-13 — State Transition Integrity:** invariant còn thiếu thật — mọi entity có vòng đời trạng thái (Position, Order, Risk Decision, Strategy Instance, Portfolio, Session) chỉ được chuyển state qua transition đã khai báo tường minh, không tồn tại illegal transition, terminal state không nhận thêm transition. Khác I-3 (No Repaint — trục thời gian) ở chỗ I-13 kiểm soát trục cấu trúc đồ thị trạng thái — 2 invariant độc lập, không trùng.
- Tự sửa trước khi thêm: KHÔNG hardcode state machine cụ thể (OPEN/PARTIAL/CLOSED...) vào Platform Invariants — chỉ dùng làm ví dụ minh họa, danh sách state/transition thật phải sống ở Domain Contract (`/docs/domain/`, Phase 0.2 chưa bắt đầu) — áp dụng đúng bài học từ lỗi I-2 (hardcode field list) đã sửa trước đó, tránh vi phạm I-12.
- Cập nhật `team/onboarding.md`: 12 → 13 Invariant.

### Version bump note
- Bump lên 3.0 (không phải patch nhỏ) vì đây là thêm invariant mới, thay đổi số lượng nguyên tắc bất biến của Constitution — khác các lần sửa nội dung/wording trước (2.0→2.5).
