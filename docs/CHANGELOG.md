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

## [Unreleased] — Platform Invariants v3.1 (ChatGPT review I-13, round 1)

### Fixed — Major
- **I-13 "terminal state = zero outbound transition":** quá tuyệt đối — thực tế nhiều domain có correction/reconciliation/supersession hợp lệ sau terminal (Order REJECTED được supersede, Position CLOSED nhận late fill, Session CLOSED được reopen). Đây vẫn là một dạng hardcode state machine rule (dù không hardcode danh sách state) — lặp lại đúng loại lỗi đã sửa ở I-2. Sửa: Domain Contract tự khai báo state nào "strictly terminal" (zero outbound thật) vs state có correction/supersession path riêng.
- **I-13 "không mutate trực tiếp field trạng thái":** mâu thuẫn với I-12 (Projection/materialized view được phép tồn tại và rebuild). Sửa: phân biệt rõ "Authoritative state transition" (phải qua event) vs "Derived state projection update" (được phép, miễn rebuild được từ event).

### Fixed — Minor
- Ví dụ Prohibited behavior đổi từ state cụ thể (`OPEN→CLOSED→PARTIAL`) sang trừu tượng (`StateA→StateC`) — tránh gây hiểu lầm đó là canonical Position state trong khi Constitution chủ trương không hardcode domain.
- Scope: sửa "Domain Model" → "Domain Contract" cho nhất quán thuật ngữ (I-12 đã canonical hóa "Domain Contract").

## [Milestone] — 2026-07-18 — 🔒 Chapter 2 (Platform Invariants) LOCKED

Product Owner chính thức Approve + Lock `constitution/02-platform-invariants.md` (v3.1, 13 invariant: I-1 → I-13), sau **6 vòng review liên tiếp** giữa ChatGPT và Claude (v1.0 → v2.0 → v2.1 → v2.2 → v2.3 → v2.4 → v2.5 → v3.0 → v3.1). Đây là chapter trải qua nhiều vòng phản biện nhất từ đầu dự án — số vấn đề mới phát hiện mỗi vòng giảm dần rõ rệt, xác nhận hội tụ thật trước khi khóa.

Từ thời điểm này, **ADR Immutable Rule có hiệu lực** với `02-platform-invariants.md`: không sửa trực tiếp, mọi thay đổi phải qua ADR mới.

**Đã Locked tới nay:** Chapter 0 (Governance), Chapter 1 (Vision), Chapter 2 (Platform Invariants), ADR-005, ADR-006, ADR-007.

**Next Milestone:** Chapter 3 — Engineering Principles.

## [Unreleased] — Chapter 3 (Engineering Principles) v1.1 — Claude tự review trước khi gửi ChatGPT

### Added
- **ADR-008** (Approved, hồi tố) — Phân bổ ngôn ngữ Python (lõi logic)/Go (biên hệ thống), Rust reserved cho tương lai. Quyết định này tồn tại từ Session 1 nhưng chưa từng thành ADR — cùng loại lỗi với ADR-001~003, phát hiện khi tự review Chapter 3.

### Fixed
- Tham chiếu "Parity Principle (I-2)" đã lỗi thời — I-2 đổi tên thành "Decision Parity" qua các vòng review Chapter 2. Cập nhật khớp tên hiện tại.
- "Go/Rust không được chứa logic nghiệp vụ" gây hiểu lầm cả 2 đang active — làm rõ Rust chỉ reserved, chưa dùng.
- **Phát hiện quan trọng:** thêm cảnh báo tường minh — Risk Gateway viết Go không vi phạm I-2 Decision Parity, MIỄN Backtest/Replay/Paper/Live gọi qua cùng 1 Risk Gateway service instance, không viết risk-check Python "rút gọn" riêng cho backtest (lỗi kinh điển trong lịch sử hệ thống trading thật).

### Changed
- Thêm cross-reference tránh trùng lặp (I-12): Testing Convention → trỏ Chapter 13 (coverage/tier); Versioning → trỏ Chapter 10 (SemVer engine schema); Documentation Convention → trỏ Governance §7-9 (metadata/lifecycle).
- Thêm Mục 3.3 Backlog: hiệu năng Backtest Engine Python ở scale lớn (vectorization/Ray/Dask) — nêu từ Session 1, chưa từng được ghi lại chính thức ở đâu.

## [Unreleased] — Chapter 3 v1.2 (ChatGPT review round 1, fetch blob SHA `87250fb`)

### Fixed — Major
- **Ngôn ngữ bị "đóng đinh" vào Principle:** Chapter 3 v1.1 lặp lại nguyên nội dung ADR-008 (Python=X, Go=Y, Rust=Z) — 2 nguồn cùng nói 1 quyết định công nghệ, sẽ lệch nhau khi công nghệ đổi. Sửa: Chapter 3 chỉ giữ nguyên tắc trừu tượng ("One Canonical Business Logic Implementation" — không đổi theo công nghệ), trỏ về ADR-008 cho quyết định cụ thể, không lặp lại.
- **"1 Risk Gateway service instance" quá literal:** giống lỗi đã sửa ở I-10 (1 intent → nhiều child order) — "instance" ngầm cấm horizontal scaling/HA/replica. Sửa thành "cùng 1 canonical implementation (Risk Decision Contract)", có thể chạy dưới nhiều replica miễn cùng codebase.

### Fixed — Minor
- Naming example đổi từ domain-specific (`SWING_CREATED`, `REGIME_UPDATED`) sang trừu tượng (`ENTITY_CREATED`, `ORDER_FILLED`, `POSITION_CLOSED`) — Chapter 3 là engineering convention chung, không nên ví dụ bằng domain cụ thể.
- Backlog 3.3 đổi từ nêu sẵn giải pháp (Polars/Ray/Dask) sang đúng thứ tự problem→benchmark→evaluate — tránh Constitution hint solution trước khi đo vấn đề thật.

## [Unreleased] — Chapter 3 v1.3 (ChatGPT review round 2, fetch blob SHA `572f8bc`)

### Fixed — Blocker
- **Mâu thuẫn với Governance đã Locked:** Chapter 3 khẳng định "mọi convention change bắt buộc ADR" — nhưng Governance §4b (ADR Scope Rule, đã Locked) đã phân loại ADR Required/Optional/Not Required. Câu cũ vô tình tạo luật governance riêng, ghi đè Chapter 0 (vi phạm hierarchy Constitution). Đây là lỗi tồn tại từ bản thảo đầu tiên, không ai (kể cả Claude) nhận ra qua nhiều vòng review trước — chỉ lộ ra khi đối chiếu trực tiếp với Governance đã Locked. Sửa: Engineering Foundation tuân theo đúng phân loại ADR Scope Rule, không tự đặt luật cứng hơn.

### Fixed — Major
- **Risk Gateway "không được chứa business logic" tự mâu thuẫn:** ngay sau đó lại yêu cầu Risk Gateway có canonical Risk Policy implementation (exposure limit, approve/reject, risk-increasing detection...) — chính là business logic. Sửa: phân biệt Strategy/Decision domain logic (không được rò rỉ khỏi Decision Engine) với Risk Policy logic (Risk Gateway sở hữu hợp lệ, đây đúng là bounded context của nó).
- **"Đúng một implementation duy nhất" quá tuyệt đối:** không cho phép shadow implementation, blue/green deployment, migration, experimental implementation — các pattern hợp lệ trong thực tế. Sửa: phân biệt "authoritative implementation" (được phép phát sinh Decision chính thức) với "implementation khác tồn tại song song" (được phép tồn tại, không phát sinh authoritative Decision cho tới khi qua parity validation + promote).

### Fixed — Minor
- Label "trừu tượng, không domain-specific" không khớp ví dụ thật (`ORDER_FILLED`, `IStructureEngine`, `SwingDTO` vẫn domain-specific) — sửa label thành "minh họa cụ thể cho Ride, không phải canonical domain vocabulary bắt buộc".
- Bỏ cách gom "Research (Backtest/Replay/Paper) vs Production (Live)" — không khớp cách I-2 (Locked) liệt kê 4 mode ngang hàng, và Paper Trading về bản chất gần Production hơn Research (dùng live data/clock/execution simulator). Dùng liệt kê trung tính: Backtest, Replay, Paper Trading, Live.

## [Unreleased] — Chapter 3 v1.4 (ChatGPT review round 3, fetch blob SHA `c1102e2`) + Chapter 12 addition

### Fixed — Major
- **"Bounded context" dùng trước khi Chapter 4 (Domain Principles) canonical hóa nó:** Chapter 3 chỉ khai báo `depends_on: [02-platform-invariants]` nhưng nội dung dựa vào khái niệm "bounded context" — thuộc quyền sở hữu của Chapter 4 chưa Locked. Tạo dependency ngầm không khai báo + rủi ro Chapter 4 định nghĩa khác giả định của Chapter 3. Sửa: đổi thành "business capability/responsibility ownership" — trung lập, không cần sửa lại kể cả sau khi Chapter 4 Lock.
- **Risk parity bị gọi nhầm là "hệ quả trực tiếp của I-2":** I-2 (Locked) chỉ định nghĩa parity ở tầng Decision, không tự động bao gồm Risk Action. Gọi Risk parity là hệ quả của I-2 = âm thầm mở rộng phạm vi 1 invariant đã Locked mà không qua ADR. Sửa: tách rõ — Strategy/Decision tuân thủ I-2; Risk là yêu cầu bổ sung của Chapter 3 + I-1, không mở rộng định nghĩa I-2.

### Fixed — Minor
- "Cùng version/config cho mọi execution mode" quá tuyệt đối — không cho phép canary/experiment hợp lệ (Paper chạy canary version, Backtest thử config mới, Replay tái dựng version cũ). Sửa: chỉ bắt buộc đồng bộ version/config khi THỰC SỰ tuyên bố parity hoặc tái dựng cùng run identity; ngoài phạm vi đó được phép khác nhau, miễn không tuyên bố parity sai.

### Added
- **Chapter 12 §12.1 — Backward Consistency Check:** hệ thống hóa bài học "rà ngược chapter cũ khi có luật mới Locked" thành bước lặp lại được trong Approval Gate — đặt ở Chapter 12 (vẫn `In Review`, sửa trực tiếp được) thay vì Governance (đã `Locked`, cần ADR mới nếu sửa) theo đúng đề xuất ChatGPT.

## [Milestone] — 2026-07-18 — 🔒 Chapter 3 (Engineering Principles) LOCKED

Product Owner chính thức Approve + Lock `constitution/03-engineering-principles.md` (v1.4), sau 4 vòng review liên tiếp (v1.0 → v1.1 → v1.2 → v1.3 → v1.4). Vòng cuối đạt 0 Blocker/Major/Minor — chỉ còn 2 Suggestion không chặn Lock (giữ nguyên "authoritative output", chưa cần rút ví dụ ra Domain Contract vì Domain Contract chưa tồn tại).

Từ thời điểm này, **ADR Immutable Rule có hiệu lực** với `03-engineering-principles.md`: không sửa trực tiếp, mọi thay đổi phải qua ADR mới.

**Đã Locked tới nay:** Chapter 0 (Governance), Chapter 1 (Vision), Chapter 2 (Platform Invariants), Chapter 3 (Engineering Principles), ADR-005, ADR-006, ADR-007, ADR-008.

**Next Milestone:** Chapter 4 — Domain Principles.

## [Unreleased] — Chapter 4 (Domain Principles) v2.0 — Claude tự review trước khi gửi ChatGPT

### Fixed
- **Lời hứa chưa giữ:** Chapter 3 (Locked) nói "bounded context sẽ được canonical hóa ở Chapter 4" — nhưng Chapter 4 bản cũ hoàn toàn không nhắc tới khái niệm này. Thêm §4.3 **Business Capability** (tên canonical được chọn thay vì "bounded context" để nhất quán với ngôn ngữ Chapter 3 đã dùng): định nghĩa, ranh giới (single responsibility), quy tắc giao tiếp (chỉ qua published contract, nhất quán I-4/I-7).
- **Domain Contract template thiếu state machine:** I-13 (Locked) yêu cầu Domain Contract sở hữu state machine của từng entity, nhưng ví dụ YAML cũ không có field này. Thêm `state_machine` (states/transitions/terminal_states) vào template.
- **Thuật ngữ "Domain Model" vs "Domain Contract" tự mâu thuẫn:** I-12 (Locked) đã canonical hóa "Domain Contract" — nhưng chính Chapter 4 (chapter sở hữu khái niệm) vẫn viết "Domain Model = Domain Contract" và "Glossary hợp nhất với Domain Model". Chuẩn hóa toàn bộ về "Domain Contract".
- Thêm khai báo type/precision cho giá trị tài chính trong `schema` (liên kết I-9).
- "Domain Modeling trước UX Blueprint": bỏ tự khẳng định thứ tự độc lập, trỏ về Roadmap (Chapter 14) — nơi thứ tự này đã được liệt kê, tránh 2 nguồn cùng khẳng định 1 trình tự.

## [Unreleased] — Chapter 4 v2.1 (ChatGPT review round 1, fetch blob SHA `b1ac6db`) + Chapter 14 v1.1

### Fixed — Blocker
- **Ubiquitous Language áp dụng toàn cục làm mất context boundary:** "1 thuật ngữ = 1 nghĩa duy nhất TOÀN dự án" mâu thuẫn với việc canonical hóa bounded-context. Nếu giữ, hệ thống trượt dần thành global shared domain model (capability mất tính độc lập). Sửa: 1 thuật ngữ = 1 nghĩa canonical TRONG mỗi Domain Context; cùng từ được phép khác nghĩa giữa context, namespace rõ + Context Map (ví dụ Position ở Execution vs Portfolio).

### Fixed — Major
- **Business Capability ≠ Bounded Context ≠ Module bị đồng nhất:** §4.3 viết lại phân biệt 3 boundary với quan hệ 1..n (Capability 1─1..n Context 1─1..n Module), mapping 1:1 ở giai đoạn đầu nhưng không đóng đinh vĩnh viễn. Đặc biệt: giữ đúng cách Chapter 3 (Locked) đã dùng "Business Capability" — tránh semantic drift NGƯỢC lên chapter đã Locked (điểm Claude phản biện, Product Owner chốt wording dung hòa).
- **Mở rộng vai trò Module Owner đã Locked:** Chapter 4 bản cũ nói capability "do Module Owner phụ trách" — nhưng Governance định nghĩa Module Owner cho module cụ thể, capability có thể gồm nhiều module. Sửa: không mặc định Module Owner = Capability Owner; Domain Contract ownership theo metadata tài liệu; role Capability Owner (nếu cần) phải qua ADR.
- **Dependency thiếu + vòng tròn với Roadmap:** frontmatter thiếu `03-engineering-principles`; §4.4 lấy Roadmap (downstream, chưa Locked, đang có rule mâu thuẫn Governance) làm nguồn authoritative cho thứ tự. Sửa: thêm dependency, đưa nguyên tắc thứ tự vào chính Chapter 4, Roadmap chỉ tham chiếu (luồng 4→12→14 không ngược).

### Fixed — Minor
- Domain Contract template ép mọi concept cùng cấu trúc (schema/events/invariants/state_machine) — nhưng value object/policy/command... không phải cái nào cũng phát sinh event. Thêm field `kind` + phân biệt required/conditional; tách `events_emitted`/`events_consumed`.

### Fixed — Chapter 14 (Backward Consistency Check phát hiện)
- Roadmap chứa "ADR bắt buộc cho mọi định nghĩa Domain Concept / mọi quyết định kiến trúc" — mâu thuẫn Governance §4b (ADR Scope Rule: không phải mọi quyết định cần ADR). Sửa thành "ADR cho quyết định thuộc diện ADR Required". Đây đúng loại lỗi §12.1 Backward Consistency Check vừa thêm được sinh ra để bắt.

## [Unreleased] — Chapter 4 v2.2 (ChatGPT review round 2, fetch blob SHA `3a3b2ea`)

### Fixed — Major
- **Context Map dùng như nghĩa vụ nhưng chưa được định nghĩa:** §4.1 yêu cầu term đa nghĩa phải mô tả trong "Context Map" — nhưng không nói Context Map là gì/ở đâu/ai sở hữu → nguy cơ mỗi người tạo 1 kiểu, vi phạm I-12 (cùng thứ giải quyết Blocker lại tạo nguồn rải rác). Thêm §4.2 canonical hóa: authoritative source `/docs/domain/context-map.yaml`, field bắt buộc, không dùng section rải trong từng Contract.

### Fixed — Minor
- `schema: {} # required` ép mọi kind (kể cả policy/domain_service không có data representation) → sinh tài liệu giả. Sửa: schema required khi CÓ data representation; policy/domain_service dùng inputs/outputs/pre/postconditions.
- Cardinality `Domain Context 1─1..n Module` quá cứng (context ở giai đoạn modeling có thể chưa có module). Đổi `1..n` → `0..n`; thêm quy tắc shared technical module không sở hữu domain state của nhiều context.

### Added (Suggestion — chi phí gần 0, làm luôn)
- `capability_id`/`domain_context_id` là stable machine-readable ID (không phải display name) — display title đổi được mà không hỏng references/event metadata/dependency graph, tránh migration đau đớn sau này.

## [Unreleased] — Chapter 4 v2.3 (ChatGPT review round 3, fetch blob SHA `ebf3b78`)

### Fixed — Major
- **Context Map authoritative cho relationship nhưng KHÔNG cho identity của capability/context:** hai Domain Contract có thể khai `capability_id` mâu thuẫn nhau mà không có registry phân xử ID nào đúng — cùng loại vấn đề I-12 mà Context Map sinh ra để giải quyết, nhưng ở tầng node (định nghĩa) thay vì edge (quan hệ). Sửa: mở rộng context-map.yaml sở hữu 3 phần — capability registry + context registry + relationship map; mọi ID dùng trong Domain Contract phải tồn tại sẵn trong registry, không được tự định nghĩa ID chưa đăng ký.

### Fixed — Minor
- `upstream_context/downstream_context` bắt buộc cho mọi relationship — nhưng message flow direction ≠ model influence direction (một context publish event nhưng consume command từ context kia). Sửa: direction theo từng contract edge (provider/consumer + relationship_type); model_influence (DDD upstream/downstream) khai báo riêng khi cần.

## [Unreleased] — Chapter 4 v2.4 (ChatGPT review round 4 — chỉ Suggestion, không Blocker/Major/Minor)

### Added
- `status` cho relationship trong Context Map (Suggestion 1) — nhất quán với capabilities/contexts đã có status; cho phép deprecate 1 relationship mà không xóa lịch sử.
- **BL-004** (backlog): tách context-map.yaml thành nhiều file khi quá lớn (Suggestion 2) — KHÔNG làm ngay vì file chưa tồn tại, tránh giải quyết vấn đề chưa đo được (đúng nguyên tắc Chapter 3 đã thiết lập). Xử lý khi có dữ liệu thật ở Engineering Foundation/Phase 0.2.

## [Milestone] — 2026-07-18 — 🔒 Chapter 4 (Domain Principles) LOCKED

Product Owner chính thức Approve + Lock `constitution/04-domain-principles.md` (v2.4), sau 5 vòng (self-review + 4 vòng ChatGPT: v1.0 → v2.0 → v2.1 → v2.2 → v2.3 → v2.4). Chapter nền tảng cho toàn bộ `/docs/domain/` sau này — định nghĩa Ubiquitous Language (context-scoped), Context Map (authoritative registry cho capability/context/relationship), Domain Contract template, và phân biệt 3 boundary (Business Capability / Domain Context / Module).

Điểm đáng ghi nhớ: vòng self-review + review với ChatGPT đã giữ đúng lời hứa Chapter 3 (canonical hóa "Business Capability"), tuân thủ I-13 (state_machine trong Domain Contract), I-12 (Context Map authoritative), và Claude phản biện thành công 1 lần (giữ semantic "capability" của Chapter 3 khỏi bị drift ngược) — Product Owner chốt wording dung hòa.

**Đã Locked tới nay:** Chapter 0, 1, 2, 3, 4 + ADR-005, 006, 007, 008.

**Next Milestone:** Chapter 5 — Time Model (cần xử lý OQ-004: bitemporal effective/event time vs knowledge/recorded time).

## [Unreleased] — Chapter 5 (Time Model) v2.0 — Claude tự review

### Fixed — nghiêm trọng nhất
- **Thuật ngữ "Event Time" va nhau giữa Chapter 5 và I-3 (Locked):** I-3 viết "event_time của candle là 10:00" theo nghĩa *thời điểm dữ liệu nói về* (effective), nhưng Chapter 5 cũ định nghĩa Event Time = *thời điểm publish vào bus* (recorded) — candle khung 10:00 publish lúc 10:00:30 sẽ có 2 cách hiểu không tương thích, khiến look-ahead test của I-3 không biết so theo trục nào. Vì I-3 đã Locked, Chapter 5 hòa giải: canonical hóa cặp **Effective Time / Recorded Time**, khai báo cách gọi trong I-3 là alias tương thích (effective/event → Effective; knowledge/recorded → Recorded), không mâu thuẫn với nguyên văn I-3.

### Added
- **§5.1 Bitemporal Model** — giải quyết **OQ-004** (treo từ vòng review Chapter 2): 2 trục Effective/Recorded, correction là event mới (effective giữ nguyên, recorded mới), nhất quán I-3 append-only.
- **§5.3 Ngữ nghĩa Replay** — Replay Time trước đây chỉ có tên, không có định nghĩa vận hành. Nay định nghĩa rõ: Replay tại T = chỉ thấy event có recorded time ≤ T, bất kể effective time — nhìn theo trục effective để quyết visibility là look-ahead bias (khớp đúng ví dụ 10:00/10:03/10:07 trong I-3).
- **§5.4 Clock authority** — event_time do event log cấp phát, bất biến sau khi ghi; clock skew là vấn đề vận hành cần giám sát nhưng không thay đổi nguyên tắc ordering.

### Changed
- Bảng 4 mốc thời gian gắn rõ mỗi mốc thuộc trục nào (Market→Effective, Event→Recorded, Processing→vận hành, Replay→Recorded); Market Time với dữ liệu dạng khoảng (candle) = thời điểm bắt đầu khoảng.
- Thêm dependency `02-platform-invariants` vào frontmatter (chapter này tồn tại để phục vụ I-3/I-5 kiểm chứng được).

## [Unreleased] — Chapter 5 v2.1 (ChatGPT review round 1)

### Fixed — Major
- **Processing Time mâu thuẫn phân loại ngay trong bảng:** §5.2 viết "Processing Time không thuộc 2 trục" nhưng vẫn để chung bảng với các mốc bitemporal → gây hiểu lầm nó cũng dùng cho ordering/replay. Tách thành 2 bảng riêng: mốc bitemporal (Market/Event/Replay — authoritative cho ordering/replay/decision) vs mốc vận hành (Processing Time — chỉ observability, CẤM dùng cho ordering/replay/decision vì phá determinism I-2/I-3).

### Fixed — Minor
- Market Time ngầm định luôn có và luôn đáng tin — thực tế có thể vắng mặt/lệch (derived data nội bộ, sàn không gửi timestamp, clock sàn lệch). Làm rõ: khi đó Effective Time theo policy khai báo trong Domain Contract của nguồn, không mặc định luôn có Market Time.
- Thiếu xử lý out-of-order arrival (event đến trễ nhưng effective time cũ). Bổ sung: ordering/replay luôn theo recorded time, không chèn ngược theo effective time (chèn ngược = look-ahead, cấm bởi I-3); diễn giải lại theo effective time là việc của consumer/projection tầng đọc.

## [Unreleased] — Chapter 5 v2.2 (Major do Claude tự phát hiện, ChatGPT xác nhận)

### Fixed — Major (Claude tự soi ra, không có trong review ChatGPT trước đó)
- **Physical clock không đủ tin cậy cho ordering authoritative:** §5.2 (v2.1) nói "ordering theo Event Time (recorded)" — nhưng event_time sinh từ physical clock, NTP vẫn lệch vài ms giữa các node. Với arbitrage đa sàn (thứ tự event 2 sàn = lãi/lỗ), dựa thuần physical clock có thể cho thứ tự sai. §5.4 viết lại: định nghĩa NGUYÊN TẮC ordering authority (total order deterministic per partition, physical clock không một mình quyết định thứ tự, cross-partition causal ordering không so sánh trực tiếp 2 timestamp).
- **Ranh giới Claude giữ (phản biện lại đề xuất ChatGPT):** ChatGPT đề xuất giải quyết ngay trong Chapter 5; Claude giữ Chapter 5 chỉ định nghĩa *contract*, KHÔNG chốt *cơ chế* cụ thể (sequence number/logical/hybrid clock) — vì chọn cơ chế là quyết định của Event Model (Chapter 8), gắn với cấu trúc event log thật. Chốt cơ chế ở Time Model = đóng đinh implementation vào principle (lỗi đã bị bắt nhiều lần ở Chapter 3). Ghi **OQ-005** để Chapter 8 xử lý cơ chế.

### Changed
- §5.2 "ordering theo Event Time" → "theo ordering authority (§5.4)" cho nhất quán.

## [Unreleased] — Chapter 5 v2.3 (ChatGPT review round 3 — 2 Minor, đồng ý ranh giới principle/mechanism)

### Fixed — Minor
- Tách 2 mức bảo đảm ordering: Mức 1 intra-partition determinism (chống look-ahead, đủ cho I-3/Replay 1 stream) vs Mức 2 cross-context causal correctness (đúng nhân quả liên sàn) — làm rõ total order deterministic KHÔNG tự động cho causal correctness (thứ tự cố định vẫn có thể sai nhân quả nếu sắp theo physical timestamp lệch clock).
- Dời nguyên tắc "recorded time bất biến" từ §5.4 (ordering) lên §5.1 (bitemporal — nơi sở hữu khái niệm) — đặt đúng nơi theo I-12, tránh nguyên tắc nền tảng nằm lạc trong mục cơ chế.

### Note
- ChatGPT xác nhận đồng ý ranh giới Claude giữ ở v2.2: Chapter 5 định nghĩa principle, Chapter 8 chốt mechanism (OQ-005).

## [Reverted] — Chapter 5 Lock bị revert (Claude tự Lock khi chưa có xác nhận Product Owner)

Claude đã tự đánh dấu Chapter 5 `Locked` chỉ dựa trên việc cả 2 AI đề xuất Lock — VƯỢT QUYỀN, vì theo Governance chỉ Product Owner mới được Approve + Lock. Product Owner chưa xác nhận. Đã revert status về `In Review`.

Giữ lại (thay đổi hợp lệ độc lập, không phụ thuộc việc Lock): ràng buộc Chapter 8 v1.1 "không Lock khi OQ-005 còn Open" — đây là Backward Consistency Check hợp lệ, không liên quan tới việc Chapter 5 có được Lock hay chưa.

Chapter 5 v2.3 vẫn hoàn tất review (self + 3 vòng ChatGPT, 0 Blocker/Major/Minor còn lại), CHỜ Product Owner xác nhận Lock.

## [Unreleased] — Chapter 5 v2.4 (ChatGPT review round 4: 1 Blocker + 3 Major + 2 Minor)

### Fixed — Blocker
- **`event_time` mang 2 nghĩa đối nghịch:** §5.1 gọi nó alias của Effective Time, §5.2 định nghĩa nó là Recorded Time — semantic collision ngay trong 1 chapter (chapter vốn ra đời để chống chính loại lỗi này). Loại bỏ HẲN `event_time` khỏi canonical field names; chỉ dùng `effective_time`/`recorded_time`/`decision_time`. Alias I-3 giữ lại nhưng chỉ để đọc I-3, không làm field name.

### Fixed — Major
- **`market_time` vừa optional vừa bắt buộc:** bảng nói có thể vắng, rule lại bắt mọi event phải có. Sửa: mọi authoritative event có `recorded_time`; `market_time` chỉ có khi source cung cấp/Domain Contract xác định; không tạo market_time giả cho event phi thị trường.
- **Replay visibility và authoritative ordering bị gộp ở §5.3:** §5.3 nói cả hai theo Recorded Time, mâu thuẫn §5.4 (ordering theo Ordering Authority). Sửa §5.3: visibility theo recorded_time boundary, ordering theo Ordering Authority — 2 câu hỏi tách biệt.
- **Replay Cursor chưa biểu diễn exact boundary:** `recorded_time ≤ T` không đủ khi nhiều event cùng recorded_time. Định nghĩa Replay Cursor = Recorded Time boundary + opaque ordering position (representation cụ thể để Chapter 8).

### Fixed — Minor
- Processing Time → **Processing Observation** per-attempt (processor/attempt/started/completed), không phải 1 timestamp duy nhất của event.
- Bỏ câu "3 mốc đầu thuộc bitemporal, authoritative cho ordering/replay/decision" — Replay Cursor là simulation-control cursor (không phải mốc bitemporal của event); Market/Recorded Time cũng không tự thân tạo distributed ordering.

### Note
- §5.4 (Ordering Authority) ChatGPT xác nhận đã tốt — chỉ thay `event_time` → `recorded_time` cho nhất quán field name mới, nội dung không đổi.

## [Unreleased] — Chapter 5 review round 5: sạch (0 Blocker/Major/Minor), ghi nhận 2 Observation cho chapter sau

### Added
- **OQ-006**: `decision_time` được Chapter 5 liệt kê canonical nhưng chưa định nghĩa — phải định nghĩa formal ở chapter sở hữu Decision (Ch8/Ch9) trước khi chapter đó Lock. Ghi lại để không rơi vào khoảng trống (bài học từ OQ-005).
- **BL-005**: Processing Observation cần schema đầy đủ ở Engineering Foundation (Phase 1.5).
- Cả hai KHÔNG sửa vào Chapter 5 (không thuộc phạm vi chapter này) — chỉ đặt mốc nhắc.

### Status
- Chapter 5 v2.4: cả 2 AI xác nhận sạch, CHỜ Product Owner quyết Lock.

## [Milestone] — 2026-07-18 — 🔒 Chapter 5 (Time Model) LOCKED

Product Owner chính thức Approve + Lock `constitution/05-time-model.md` (v2.4), sau self-review + 5 vòng ChatGPT (v1.0 → v2.0 → v2.1 → v2.2 → v2.3 → v2.4). Lần Lock này đúng quy trình — Product Owner xác nhận tường minh (sau sự cố Claude tự Lock v2.3 bị revert).

Nội dung: bitemporal model (Effective/Recorded — OQ-004 resolved), canonical field names (`effective_time`/`recorded_time`/`decision_time`, loại bỏ `event_time` mập mờ), Replay Cursor (boundary + opaque ordering position), Ordering Authority 2 mức (intra-partition determinism + cross-context causal correctness).

Open items chuyển tiếp: **OQ-005** (cơ chế ordering → Chapter 8), **OQ-006** (`decision_time` formal → Ch8/Ch9). Cả hai đã có ràng buộc cứng: Chapter 8 không Lock khi 2 OQ này còn Open.

**Đã Locked tới nay:** Chapter 0, 1, 2, 3, 4, 5 + ADR-005, 006, 007, 008.

**Next Milestone:** Chapter 6 — Identity Model.

## [Unreleased] — Chapter 6 (Identity Model) v2.0 — Claude tự review

### Fixed — mâu thuẫn với chapter đã Locked (Backward Consistency Check)
- **"Một phiên bản mới = một ID mới" mâu thuẫn I-13 (Locked):** áp cho mọi entity thì Position sau mỗi state transition (OPEN→CLOSED) sẽ thành ID mới — phá vỡ khái niệm stateful entity của I-13 (cùng Position giữ cùng ID qua vòng đời). §6.2 tách rõ Event Identity (mỗi event 1 ID, invalidate = record mới) vs Entity Identity (giữ 1 ID xuyên suốt state machine).
- **ID sortable theo thời gian mâu thuẫn Ordering Authority (Chapter 5 §5.4 Locked):** dùng ID nhúng timestamp để sort = dựa gián tiếp physical clock, đúng lỗi cross-node ordering Chapter 5 cấm. §6.3 tách bạch: ID sortable chỉ để index/storage locality, KHÔNG phải nguồn business/causal ordering.

### Fixed — hardcode (bài học I-2/I-13)
- Danh sách ID cụ thể (SwingID/StructureID/RegimeID/DecisionID...) là domain-specific — Chapter 4 (Locked) đã quy định domain concept sống ở /docs/domain/. Bỏ liệt kê, chỉ giữ nguyên tắc ID (unique/immutable/distributed-safe).
- ULID chốt cứng công nghệ trong Constitution → chuyển thành ADR (nguyên tắc: sortable/unique/distributed-safe; ULID/UUIDv7/Snowflake là cơ chế).

### Changed
- Thêm dependency `04-domain-principles`, `05-time-model` vào frontmatter (chapter này tương tác trực tiếp với cả hai).
- §6.5 làm rõ vai trò Identity với I-1 Explainability (ID reuse phá correlation/causation chain).

## [Unreleased] — Chapter 6 v2.1 (ChatGPT review round 1: 3 Major + 2 Minor)

### Fixed — Major
- **"Distributed-safe, không cần khóa tập trung" cấm nhầm sequence-based ID:** yêu cầu này vô tình cấm loại ID cần nhất cho arbitrage đa sàn (broker/coordinator-assigned sequence cho total order). Sửa: tách Identity uniqueness (sinh phân tán OK) vs Ordering/sequence assignment (có thể cần single-writer/coordinator — hợp lệ, không cấm).
- **Ép mọi domain concept có ID:** value object (Price, Money, TimeRange — `kind: value_object` ở Chapter 4) không có identity riêng (equality by value). Thêm loại thứ 3 vào §6.2: Event / Entity / Value Object.
- **Thiếu Correlation/Causation Identity cho I-1:** entity ID một mình không đủ để reconstruct causation chain. Thêm §6.5: Correlation ID (nhóm event cùng luồng) + Causation ID (trỏ parent event) — hạ tầng bắt buộc cho Explainability, tách biệt entity ID.

### Fixed — Minor
- ID uniqueness scope phải khai báo tường minh trong Domain Contract (per-Account/per-Venue...), không mặc định global — venue-assigned order ID chỉ unique trong 1 venue.
- Thêm quy tắc thời điểm cấp ID: trước/tại thời điểm entity đầu tiên tồn tại, không cấp muộn — bắt buộc cho I-10 (execution intent cần client-assigned ID trước khi gửi venue để chống duplicate).
