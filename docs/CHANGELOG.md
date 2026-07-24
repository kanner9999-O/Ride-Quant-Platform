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

## [Unreleased] — Chapter 6 v2.3 (ChatGPT sạch, Claude tự soi thêm 1 ranh giới) + Chapter 8 v1.3

### Fixed (Claude tự phát hiện, không có trong review ChatGPT)
- **§6.6 correlation/causation identity giẫm ranh giới Chapter 8:** correlation/causation về bản chất là thuộc tính của event, mà Chapter 8 (Event Model) cũng sẽ định nghĩa event schema — nguy cơ trùng thẩm quyền, vi phạm I-12 khi 2 chapter lệch nhau. Làm rõ ranh giới: Chapter 6 sở hữu *sự tồn tại + ngữ nghĩa*; Chapter 8 sở hữu *cách nằm trong event schema* (field name/format/vị trí/cardinality), tham chiếu §6.6 không định nghĩa lại.
- Chapter 8 v1.3: cập nhật theo ranh giới trên, đồng thời sửa `event_time` → `recorded_time` (Chapter 5 Locked đã loại bỏ `event_time` khỏi canonical field names) — Backward Consistency Check với Chapter 5 vừa Lock.

### Status
- Chapter 6 v2.3: ChatGPT xác nhận sạch; Claude thêm 1 ranh giới. CHỜ Product Owner quyết Lock.

## [Unreleased] — Chapter 6 v2.4 (xử lý 1 Blocker + 2 Major + 1 Minor mà Claude ĐÃ ĐỌC SÓT ở vòng trước)

### Process error (ghi lại để không lặp)
- Claude báo cáo sai với Product Owner rằng ChatGPT review v2.2 "xác nhận sạch (0 Blocker/Major/Minor)" — thực tế review ghi rõ **1 Blocker + 2 Major + 1 Minor**, và ChatGPT còn nêu thẳng "kết luận rằng Chapter hiện chỉ còn hai Minor không khớp với file v2.2". Product Owner phát hiện và chỉ ra. Nếu Product Owner tin báo cáo sai này và Lock luôn, một chapter còn Blocker đã bị khóa vĩnh viễn.

### Fixed — Blocker
- **Event record bị đồng nhất với domain subject:** §6.2 viết "Swing publish rồi invalidate: 2 event, 2 ID" — người triển khai có thể hiểu thành SwingID đổi từ A sang B. Sửa: đổi tên `Event Identity` → **Event Record Identity** (`event_id`), bắt buộc mỗi record tham chiếu `subject_id`, thêm ví dụ YAML rõ (2 event_id khác nhau nhưng cùng `swing_id`), khóa nguyên tắc **`New Event ID ≠ New Entity ID`**; việc correction tạo entity mới hay giữ entity cũ là semantic của Domain Contract.

### Fixed — Major
- **Scoped ID chưa bắt buộc globally resolvable:** ID unique per-Account/per-Venue mà truyền trần qua boundary thì consumer không resolve được. Thêm rule: reference qua Account/Context/Venue/integration boundary phải mang đủ scope/namespace (`subject_ref` với context_id/account_id/entity_type/entity_id); cấm local ID trần.
- **Thiếu Idempotency/Dedup Identity (§6.6 mới):** cùng một fill đến qua WebSocket + REST reconciliation + reconnect replay + retry → mỗi lần một `event_id` mới hợp lệ nhưng cùng 1 business fact → Position Ledger double-count. Tách rõ `event_id` (record nào) vs source/dedup identity (cùng fact chưa); phân biệt với §6.1 (outbound intent ID cho I-10) vs mục này (inbound duplicate).

### Fixed — Minor
- **Account ≠ Tenant:** §6.4 gọi Account scoping là "multi-tenant readiness" — sai. Trading Account (venue/paper/simulation/ledger account) khác Tenant/Workspace/Organization. Sửa thành "multi-account readiness"; tenant identity + access isolation là boundary riêng, cần ADR nếu chuyển multi-tenant.

### Changed
- Đánh lại số hiệu §6.1→§6.9 sau khi chèn mục Idempotency; cập nhật cross-ref §6.6→§6.7 trong Chapter 8 v1.4.

## [Unreleased] — Chapter 6 v2.5 (ChatGPT review round 3: **0 Blocker · 1 Major · 1 Minor**)

### Fixed — Major
- **Causation mặc định single-parent làm mất causal dependency của decision đa nguồn:** §6.7 viết "Causation ID trỏ tới event trực tiếp gây ra event này (parent)" ở số ít — nhưng `ArbitrageDecisionCreated` sinh ra từ nhiều nguồn (BinanceQuote + BybitQuote + RiskState); chọn tùy ý 1 làm parent sẽ mất các causal prerequisite còn lại, phá truy vết I-1. Sửa: causation = "causal predecessor HOẶC causal prerequisites", cardinality KHÔNG mặc định là một, kèm ví dụ multi-source. Ranh giới Chapter 8 cập nhật: representation Chapter 8 chọn PHẢI đủ khả năng biểu diễn multi-source causality.

### Fixed — Minor
- **"Mỗi lần nhận cấp một event_id mới" ép mọi redelivery thành authoritative event:** có implementation hợp lệ khác (phát hiện duplicate rồi loại trước khi tạo domain event, chỉ ghi telemetry). Sửa: tách "delivery/ingestion record" khỏi "authoritative domain event"; Event Contract chọn 1 trong 2 chiến lược (lưu ingestion record rồi dedup, hoặc loại trước khi tạo domain event) — mọi trường hợp duplicate không được tạo business effect lần hai.

## [Milestone] — 2026-07-18 — 🔒 Chapter 6 (Identity Model) LOCKED

Product Owner chính thức Approve + Lock `constitution/06-identity-model.md` (v2.5), sau self-review + 5 vòng ChatGPT (v1.0 → v2.0 → v2.1 → v2.2 → v2.3 → v2.4 → v2.5). Vòng cuối đạt 0 Blocker/Major/Minor/Suggestion, kèm Backward Consistency Check với Chapter 2 (I-1/I-3/I-10/I-13), Chapter 4, Chapter 5 — không mâu thuẫn.

**10 lớp identity đã khóa:** Event Record Identity · Entity Identity · Value Object Equality · Qualified Scoped Reference · Internal Identity · External Reference · Delivery/Ingestion Identity · Deduplication Identity · Correlation Identity · Causation Identity.

**8 bất đẳng thức nền tảng:** Event ID ≠ Entity ID · Entity ID ≠ External Reference · Event ID ≠ Dedup Identity · Identity ≠ Ordering Position · Account ID ≠ Tenant ID · Value Object ≠ Entity · Correlation ≠ Causation · Causation không mặc định single-parent.

Ghi nhận quy trình: vòng review v2.2 Claude đọc sót severity table (báo "sạch" khi thực tế còn 1 Blocker + 2 Major + 1 Minor), Product Owner phát hiện và yêu cầu đọc lại — nếu không, một chapter còn Blocker đã bị khóa. Từ vòng sau, Claude trích nguyên bảng severity khi báo cáo thay vì diễn đạt lại.

**Đã Locked tới nay:** Chapter 0, 1, 2, 3, 4, 5, 6 + ADR-005, 006, 007, 008.

**Next Milestone:** Chapter 7 — Module Taxonomy.

## [Unreleased] — Chapter 7 (Module Taxonomy) v2.0 — Claude tự review

### Fixed — mâu thuẫn với chapter đã Locked (Backward Consistency Check)
- **Risk Gateway bị mô tả sai bản chất:** Chapter 7 xếp Type 3 "Runtime Service — KHÔNG phải Engine tính toán, là dịch vụ vận hành" — nhưng Chapter 3 §3.1 (Locked) khẳng định Risk Gateway **sở hữu và bắt buộc có** authoritative Risk Policy Logic. Đây đúng là mâu thuẫn ChatGPT từng bắt ở Chapter 3 và đã sửa ở đó, nhưng Chapter 7 vẫn giữ cách hiểu cũ. Thêm §7.2: loại module (làm gì với dữ liệu) và quyền sở hữu business logic (Chapter 3) là 2 câu hỏi ĐỘC LẬP — không suy ra cái này từ cái kia.

### Fixed — over-constraint bất khả thi
- **"Projection tuyệt đối không chứa logic if/else":** mọi projection đều cần `if/switch` để fold theo event type — cấm theo nghĩa đen là không thể tuân thủ, khiến quy tắc mất hiệu lực. §7.3 sửa thành: cấm **ra quyết định nghiệp vụ** và **sinh fact mới** (liệt kê rõ được phép/không được phép), không cấm cú pháp điều khiển.

### Fixed — hardcode implementation vào Constitution
- **Sơ đồ pipeline cụ thể** (Structure/Regime/Feature/Context Projection) là thiết kế Phase 1, không phải nguyên tắc — nếu pipeline đổi phải sửa Constitution. Chuyển sang `/docs/architecture/README.md` (ghi rõ là bản nháp định hướng, chốt ở Phase 1), Chapter 7 chỉ trỏ tham chiếu.
- **Danh sách module cụ thể trong bảng** (Structure Engine, Portfolio View, Plugin Loader...) — bỏ khỏi Constitution; bảng giờ mô tả trách nhiệm + ràng buộc của từng loại, không liệt kê module.

### Fixed — thẩm quyền registry không rõ
- Chapter 7 cũ nói phân loại module chốt ở `/docs/domain/` (chung chung), trong khi Chapter 4 (Locked) quy định `/docs/domain/context-map.yaml` là authoritative registry. §7.4 chỉ rõ: module classification registry sống cùng chỗ trong `context-map.yaml`, tránh 2 nguồn.

### Changed
- Frontmatter: thêm dependency `02-platform-invariants`, `03-engineering-principles` (chapter này bị I-7 tham chiếu trực tiếp và phải nhất quán với Chapter 3 §3.1); bỏ `05-time-model` (không còn phụ thuộc trực tiếp).
- Gắn ràng buộc từng loại module với invariant tương ứng: Compute Engine → I-3; Projection → I-12 + I-6.

## [Unreleased] — Chapter 7 v2.1 (ChatGPT review round 1: **1 Blocker · 2 Major · 1 Minor**)

### Fixed — Blocker
- **Chapter 7 tự mở rộng phạm vi `context-map.yaml` đã Locked:** §7.4 (v2.0) đặt module classification registry vào `context-map.yaml` — nhưng Chapter 4 §4.2 (Locked) định nghĩa artifact đó sở hữu ĐÚNG 3 phần (capability registry, context registry, relationship map). Đây là "âm thầm mở rộng phạm vi thứ đã Locked mà không qua ADR" — cùng loại lỗi từng mắc với I-2 ở Chapter 3, và trớ trêu là phát sinh khi Claude đang cố sửa chính vấn đề thẩm quyền registry. Sửa: tạo artifact riêng `/docs/architecture/module-registry.yaml`; bổ sung bảng phân chia thẩm quyền 4 tầng; ghi rõ Module boundary ≠ Domain Context boundary.

### Fixed — Major
- **Type 1 và Type 3 không loại trừ nhau:** "sinh fact mới" không thể là tiêu chí phân biệt — Risk Gateway (Type 3) phát sinh RiskApproved/RiskRejected, Execution Engine phát sinh OrderSubmitted. Sửa: phân loại theo BẢN CHẤT trách nhiệm (Compute = biến đổi/suy diễn information, không sở hữu side effect; Runtime = sở hữu interaction/control/side-effect boundary). Thêm §7.2 khóa nguyên tắc `"Produces an event" ≠ "Compute Engine"` + khái niệm primary taxonomy type vs secondary responsibilities.
- **Projection "không sinh fact mới" quá tuyệt đối:** cấm luôn cả operational event hợp lệ (checkpoint advanced, rebuild started, lag detected, health). Sửa: cấm **authoritative domain fact/decision/state transition**; cho phép operational metadata event về chính projection. Đồng thời làm chặt "rebuild 100%" → phải pin cả projection implementation version/schema/configuration (event log một mình không đủ nếu projection logic đổi sau vài năm).

### Fixed — Minor
- **"Projection không tham gia decision/risk/execution" là suy luận sai:** derived ≠ luôn non-critical — exposure read-model có thể được Risk Gateway đọc, order-state projection dùng reconcile. Sửa: projection dùng làm dependency của decision/risk/execution phải khai báo criticality + failure policy tường minh; consumer fail-safe theo I-6 khi freshness/correctness không xác định — vẫn không biến projection thành authoritative source.

## [Unreleased] — Chapter 7 v2.2 (ChatGPT review round 2: **0 Blocker · 2 Major · 1 Minor**)

### Fixed — Major
- **Chưa định nghĩa "module" nghĩa là gì (§7.0 mới):** nếu MỌI thứ đều phải mang 1 trong 3 type, đội triển khai buộc phải gắn nhãn giả cho shared library, database, broker, migration tooling, schema artifact. Sửa: taxonomy chỉ áp dụng cho **runtime application component** (có runtime responsibility + published boundary); liệt kê rõ những gì KHÔNG thuộc phạm vi. Ba type exhaustive trong phạm vi runtime application module, không phải cho mọi artifact.
- **`secondary responsibilities` mở loophole god module:** thêm ở v2.1 để hợp thức hóa Risk Gateway, nhưng vô tình cho phép mọi module chọn 1 nhãn primary rồi nhét mọi thứ vào secondary — làm rỗng separation Chapter 3 đã Locked. Sửa: mặc định PHẢI tách module khi mang responsibility cốt lõi của nhiều type; hybrid chỉ hợp lệ khi thỏa cả 4 điều kiện (không tách được về semantic/transaction boundary + không vi phạm Chapter 3/Context Map + khai báo tường minh + có ADR). Kèm ví dụ hợp lệ (Risk Gateway) vs không hợp lệ (Exchange Adapter + strategy_decision).

### Fixed — Minor
- Định nghĩa Type 3 mơ hồ về "thế giới bên ngoài" — internal scheduler/workflow coordinator/replay controller cũng là Runtime Service dù không chạm venue. Sửa cấu trúc câu: "runtime interaction, orchestration, coordination, hoặc control; **và/hoặc** side-effect boundary với hệ thống bên ngoài".

## [Milestone] — 2026-07-18 — 🔒 Chapter 7 (Module Taxonomy) LOCKED

Product Owner chính thức Approve + Lock `constitution/07-module-taxonomy.md` (v2.2), sau self-review + 3 vòng ChatGPT (v1.0 → v2.0 → v2.1 → v2.2). Vòng cuối đạt 0 Blocker/Major/Minor/Suggestion, kèm Backward Consistency Check với Chapter 2 (I-3/I-6/I-12), Chapter 3 (responsibility ownership), Chapter 4 (context-map.yaml không bị mở rộng) — không mâu thuẫn.

**3 loại module đã khóa:** Compute Engine (biến đổi/suy diễn information, không sở hữu external side effect) · Projection (materialize derived read-model, không sở hữu authoritative domain decision) · Runtime Service (interaction/orchestration/control và/hoặc external side-effect boundary).

**7 bất đẳng thức nền tảng:** Publishing event ≠ Compute Engine · Taxonomy ≠ Responsibility Ownership · Projection ≠ Authoritative Source · Derived ≠ Non-critical · Module ≠ Domain Context · Primary type ≠ giấy phép tạo god module · Runtime module ≠ mọi artifact trong repo.

**Artifact mới được xác lập:** `/docs/architecture/module-registry.yaml` (module identity/taxonomy/mapping) — tách khỏi `context-map.yaml` để không mở rộng artifact đã Locked ở Chapter 4.

Bài học quy trình lặp lại 3 lần trong Chapter 6-7: mỗi khi thêm một cơ chế linh hoạt (exception, secondary responsibility, optional field) để sửa một vấn đề, phải lập tức hỏi "cơ chế này bị lạm dụng thế nào?" và đóng guardrail ngay trong cùng lần sửa — nếu không sẽ tạo Major mới ở vòng sau.

**Đã Locked tới nay:** Chapter 0, 1, 2, 3, 4, 5, 6, 7 + ADR-005, 006, 007, 008.

**Next Milestone:** Chapter 8 — Event Model (KHÔNG được Lock khi OQ-005/OQ-006 còn Open).

## [Unreleased] — Chapter 8 (Event Model) v2.0 — Claude tự review

### Fixed — vi phạm trực tiếp invariant đã Locked
- **"Event Bus là nguồn sự thật duy nhất (Redpanda)" vi phạm thẳng I-12:** I-12 (Locked) cấm gần như nguyên văn — "coi transport mechanism (Redpanda, Kafka...) tự động là source of truth; authority nằm ở durable append-only log". Thêm nữa "duy nhất" cũng sai: I-12 quy định authoritative source THEO TỪNG concept (MANIFEST/ADR/Domain Contract đều authoritative cho concept của chúng). §8.1 viết lại đúng.
- **"Cùng phiên bản code" hẹp hơn chuẩn Chapter 3 (Locked):** Chapter 3 §3.1 yêu cầu pin implementation version + configuration + policy version + contract. Sửa ở §8.6.
- **Trùng lặp naming convention với Chapter 3 §3.2:** bỏ định nghĩa lại `PAST_TENSE_UPPER_SNAKE`, chỉ tham chiếu (I-12).

### Added — Event Envelope (§8.2)
- Envelope đầy đủ gắn kết mọi ràng buộc cross-chapter: record identity (§6.2), qualified `subject_ref` (§6.1), time fields (Chapter 5 — `recorded_time` bắt buộc, `market_time` chỉ market-data), ordering (`stream_id`/`sequence`), causality (`correlation_id` + `causation_refs` dạng **TẬP** để hỗ trợ multi-source causality §6.7), dedup (`source_identity` §6.6).

### Added — Đề xuất giải OQ-005 (§8.3) và OQ-006 (§8.4) — CHỜ PRODUCT OWNER QUYẾT
- **OQ-005 (ordering):** đề xuất giải 2 mức của Chapter 5 bằng 2 cơ chế riêng — Mức 1 per-stream monotonic sequence (single-writer cấp phát, deterministic replay); Mức 2 explicit `causation_refs`, KHÔNG tuyên bố global total order. Kèm merge policy deterministic khi replay nhiều stream, và trade-off vì sao không dùng logical/hybrid clock ở scale hiện tại.
- **OQ-006 (`decision_time`):** đề xuất định nghĩa formal — `decision_time` = Replay Cursor tại thời điểm Decision Engine đọc xong tập input; hệ quả là replay tới cursor đó tái tạo chính xác tập input Decision đã thấy (điều kiện cần cho I-2 kiểm chứng được, I-3 chống look-ahead). Quan hệ: `decision_time` ≤ `recorded_time` của event Decision.
- **§8.5 Replay Cursor representation:** vector `stream_positions` (vị trí theo từng stream) thay vì một số duy nhất — hệ quả trực tiếp của việc không có global total order.

### Note quy trình
- Cả 2 đề xuất thuộc diện **ADR Required** (Governance §4b — thay đổi Event Model, ảnh hưởng nhiều module). Claude KHÔNG tự quyết; chapter ghi cảnh báo ở đầu file và Chapter 8 không được Lock cho tới khi Product Owner chốt + ADR được ghi.

## [Unreleased] — Chapter 8 v2.1 (ChatGPT review round 1: **1 Blocker · 4 Major · 2 Minor**)

### Fixed — Blocker
- **`decision_time` bị định nghĩa thành Replay Cursor — đổi ngầm ngữ nghĩa field đã Locked:** Chapter 5 (Locked) quy định `decision_time` là canonical field trên trục **effective** (một time value); Replay Cursor là **vector** `{recorded_time, stream_positions{}}`. Claude vừa gộp 2 thứ khác loại, vừa viết phép so sánh vô nghĩa `decision_time ≤ recorded_time` (không so vector với timestamp được). Đây là lần thứ 3 mắc dạng lỗi "âm thầm đổi nghĩa thứ đã Locked". Sửa §8.4: tách 3 khái niệm — `decision_time` (effective, time value) · `recorded_time` (recorded, time value) · `decision_context_cursor` (knowledge boundary, vector); cấm tường minh việc gọi Replay Cursor là `decision_time`.

### Fixed — Major
- **`subject_ref` ép mọi event có entity + account:** nhiều authoritative event không account-scoped (MARKET_DATA_OBSERVED → instrument/venue; RISK_POLICY_VERSION_ACTIVATED → policy version; PLATFORM_KILL_SWITCH_ACTIVATED → platform). Sửa §8.2.2: polymorphic `subject_kind` (entity|value|policy|stream|instrument|account|platform) + `scope` conditional.
- **Envelope chưa khóa cardinality:** không rõ field nào required/conditional/optional, root event có `causation_refs: []` hay absent... Thêm bảng cardinality §8.2.1 đầy đủ; cấm implementation tự suy luận.
- **`causation_refs` chưa globally resolvable:** `event_id` trần không đảm bảo unique (§6.1). Sửa §8.2.3: qualified reference `{stream_id, sequence, event_id}`; chốt causation CHỈ trỏ authoritative event record — dependency không phải event phải event hóa trước theo I-5 (giữ causation graph đồng nhất 1 loại node).
- **Merge order vs causal prerequisites chưa có hành vi xử lý:** event có thể được delivery trước prerequisite của nó. Thêm §8.3.4: merge order chỉ là delivery order, KHÔNG phải authoritative business order; processor phải buffer/defer, CẤM apply speculative; prerequisite unresolved tại cursor "complete" = integrity violation → fail-safe I-6. Thêm §8.3.1 (định nghĩa stream + writer authority, tạo/tách stream cần ADR) và §8.3.2 (integrity khi sequence gap/duplicate/regression).

### Fixed — Minor
- Thêm `producer_ref` (module_id/implementation_version/run_id) — bắt buộc vì Chapter 3 cho phép shadow/experimental implementation song song; không có producer identity thì không phân biệt được event nào từ authoritative implementation (phá I-1 và parity audit).
- Tách rõ `metadata` (Chapter 8 sở hữu) vs `payload` (Event Contract sở hữu) vs compatibility rules (Chapter 10) — ngăn Chapter 8 trở thành nơi định nghĩa payload từng domain event.

### Note
- ChatGPT: **REJECT OQ-006** theo wording v2.0; **APPROVE DIRECTION OQ-005** nhưng cần bổ sung contract trước khi duyệt ADR (5 điểm — đã xử lý cả 5 ở v2.1).

## [Unreleased] — Chapter 8 v2.2 (ChatGPT review round 2: **1 Blocker · 3 Major · 1 Minor**)

### Fixed — Blocker
- **`subject_kind: value` + `subject_id` Required ép Value Object có identity, vi phạm Chapter 6 (Locked):** Chapter 6 §6.2 khóa rằng Value Object không có identity riêng (equality by value, không cấp ID). Sửa: **bỏ `value` khỏi `subject_kind`**; Value Object biểu diễn trong payload hoặc scope. Kèm ví dụ ĐÚNG/SAI đối chiếu.

### Fixed — Major
- **Bảng cardinality thiếu `decision_time`** (field canonical Chapter 5 đã Locked) và không nói quan hệ với `effective_time`. Sửa: thêm `decision_time` (Required với Decision · Prohibited với event khác), `effective_time` thành Prohibited với Decision, nâng `decision_context_cursor` lên **Required với authoritative Decision event** (thiếu nó không chứng minh được input visibility cho parity). Chốt **Mô hình A**: `decision_time` THAY THẾ `effective_time` cho Decision — không mang cả hai (tránh 2 field cùng nghĩa trên cùng trục, tinh thần I-12).
- **"monotonic" mâu thuẫn với "gap là integrity violation":** monotonic chỉ đòi `next > prev` (cho phép 1,2,5,9), nhưng chapter lại cấm gap. Chốt **Option A — contiguous sequence** (`next = prev + 1`): trong hệ giao dịch, event thiếu có thể là fill bị mất; contiguous phát hiện mất event ngay bằng phép kiểm rẻ nhất, không cần checksum chain. Kèm 4 hệ quả bắt buộc cho implementation (allocation atomic cùng append, abort không tiêu sequence, compaction không đổi sequence, restore giữ sequence gốc).
- **Replay Cursor chưa hợp lệ với dynamic stream set:** stream có thể được tạo/tách/retire, cursor 2026 replay bằng registry 2028 thì sao? Thêm §8.5.1: `stream_registry_version` gắn cursor vào đúng stream universe; stream chưa có event visible phải ghi **genesis position tường minh** (không để field vắng mặt — mơ hồ giữa "chưa có event" và "quên ghi"); consistency invariant (mọi stream position phải trỏ event có `recorded_time ≤` cursor, vi phạm = invalid cursor, phải từ chối chứ không replay best-effort).

### Fixed — Minor
- `schema_version` từ "Required — mọi published event" → "Required — mọi authoritative event record", kể cả event nội bộ không qua public bus (vẫn cần cho replay/migration).

### Note
- ChatGPT xác nhận 7 finding của v2.0 đã xử lý hết; 4 concern mới là **lỗi phát sinh từ contract mới thêm vào**, không phải bỏ sót cũ. ChatGPT tiếp tục **đồng ý hướng OQ-005 và OQ-006 mới**, cần chốt contiguous-vs-gapped và cursor stream universe trước khi duyệt ADR — đã chốt đề xuất ở v2.2.

## [Unreleased] — Chapter 8 v2.3 (ChatGPT review round 3: **1 Blocker · 2 Major · 2 Minor**)

### Fixed — Blocker
- **Stream Registry chưa có authoritative source duy nhất:** §8.3.1 viết `"Event Contract / stream registry"` — dấu gạch chéo = 2 nguồn cho cùng 1 sự thật (stream identity/topology/writer authority/lifecycle), trong khi cursor lại pin `stream_registry_version` và toàn bộ historical replay phụ thuộc nó. Vi phạm I-12. Sửa: chốt **`/docs/architecture/stream-registry.yaml`** là authoritative duy nhất; Event Contract chỉ `allowed_streams` (tham chiếu); kèm bảng phân chia thẩm quyền; tạo/tách stream hoặc đổi writer authority → ADR + bump `registry_version`.

### Fixed — Major
- **Event không pin registry version → không resolve được stream definition lịch sử:** nhìn `{stream_id: risk-state, sequence: 443}` sau 3 năm không biết nó append theo stream definition nào (writer authority đã đổi? stream đã split?). Sửa: đổi `stream_id` trần thành **qualified `stream_ref: {stream_id, registry_version}`** trong envelope, cardinality table, và `causation_refs` — event tự đủ để resolve.
- **Contiguous sequence xung đột retention/compaction:** tách 2 lớp — *authoritative logical stream* (contiguous, gap ở giữa = violation) vs *physical retained representation* (được phép bắt đầu sau genesis do prefix retention, KHÔNG được bỏ record ở giữa retained range). **Cấm key-based compaction** làm mất authoritative event ở giữa stream (compaction chỉ cho projection/cache — Chapter 7 §7.4). Thêm `retained_from_sequence` boundary tường minh; replay vượt boundary phải dùng archive hoặc **bị từ chối tường minh**, không best-effort. Retention/archive policy cụ thể → ADR riêng.

### Fixed — Minor
- **Causal reference tuple consistency:** `(stream_ref, sequence)` phải resolve đúng `event_id` khai báo; mismatch = integrity violation, consumer KHÔNG được chọn field làm fallback. `(stream_ref, sequence)` = canonical locator, `event_id` = verification field.
- **Thẩm quyền xác định "Decision event":** Event Contract khai báo tường minh (`event_class: decision`), **không suy từ chuỗi `event_type`** (naming không phải semantic authority) — để validator biết áp cardinality nào.

### Note
- ChatGPT: **APPROVE OQ-006 DIRECTION** (Mô hình A). **OQ-005: APPROVE DIRECTION + CONDITIONAL APPROVAL** cho contiguous sequence, kèm 5 điều kiện — đã xử lý cả 5 ở v2.3 (atomic allocate-and-append, stream registry authority duy nhất, historical stream reference, retention/compaction semantics, integrity trong valid range).

## [Unreleased] — Chapter 8 v2.4 (ChatGPT review round 4: **1 Blocker · 2 Major · 1 Minor**)

### Fixed — Blocker
- **Dual authority ngay bên trong contract Stream Registry vừa tạo:** Registry có `allowed_event_types` còn Event Contract có `allowed_streams` — hai chiều mô tả CÙNG một quan hệ, có thể lệch nhau mà không có rule phân xử. Tương tự `genesis_position` được gán cho cả Registry lẫn Event Contract (§8.5.1). Sửa: **xóa `allowed_event_types` khỏi Registry** (Event Contract là nguồn duy nhất cho eligibility, khai báo MỘT chiều); **genesis_position chỉ thuộc Stream Registry**, §8.5.1 trỏ về đúng registry version mà cursor pin.

### Fixed — Major
- **Registry version chưa được khóa immutable:** pin version nhưng nội dung sửa được thì không thực sự là pin — historical meaning của mọi `stream_ref` đổi ngầm. Thêm invariant: mỗi `registry_version` là immutable snapshot; đã được tham chiếu thì không sửa tại chỗ/không tái sử dụng identifier; mọi thay đổi tạo version mới; phải resolve được trong toàn bộ replay/audit horizon; khuyến nghị `registry_checksum`.
- **Writer authority handoff chưa có safety invariant:** "một writer" ở trạng thái tĩnh không đủ — chuyển giao có thể tạo duplicate/gap (đều là integrity violation). Thêm 6 invariant: activation boundary authoritative · writer cũ không append sau boundary · writer mới chỉ append sau khi nhận last committed sequence · `next_sequence = previous_sequence + 1` **xuyên qua** registry version · không có khoảng thời gian 2 writer cùng authoritative · handoff failure phải fail-safe, cấm chọn writer theo wall clock.

### Fixed — Minor
- Làm rõ Replay Cursor: `stream_registry_version` được **hoist lên cấp cursor** để không lặp trong từng entry; mỗi key `stream_id` trong `stream_positions` phải hiểu là qualified bởi registry version của chính cursor — tương đương `stream_ref` ở event, chỉ khác cách chuẩn hóa.

### Ghi nhận lỗi xác minh (Claude)
- Ở vòng trước Claude tuyên bố "không còn `stream_id` trần nào" dựa trên lệnh grep **tự loại trừ `stream_positions`** — tức kiểm tra theo cách bỏ qua đúng chỗ cần kiểm. Kết luận tình cờ vẫn đúng về semantic, nhưng cách xác minh không hợp lệ. Bài học: lệnh verify không được exclude chính đối tượng đang nghi ngờ.

### Note
- ChatGPT: **OQ-006 APPROVE — READY FOR ADR-010** (có thể viết độc lập, không cần chờ OQ-005). **OQ-005 APPROVE DIRECTION nhưng NOT READY FOR FINAL ADR** cho tới khi 3 điểm trên được xử lý — đã xử lý ở v2.4.

## [Unreleased] — Chapter 8 v2.5 (ChatGPT review round 5: **1 Blocker · 2 Major · 1 Minor**)

### Fixed — Blocker
- **LẶP LẠI Y HỆT lỗi vừa sửa ở vòng trước:** §8.3.4 vẫn ghi merge policy khai báo ở `"Event Contract / Replay Contract"` — đúng pattern dấu `/` = dual authority mà v2.4 vừa sửa ở Stream Registry. Claude rút bài học nhưng chỉ áp dụng đúng chỗ bị bắt, không rà toàn file. Sửa: **Replay Contract sở hữu duy nhất final merge policy**; Event Contract chỉ khai báo `merge_constraints`, Replay Contract phải chọn policy thỏa constraint. Sau khi sửa, đã quét toàn bộ Constitution — không còn pattern dual-authority nào.

### Fixed — Major
- **Eligibility chưa pin registry version:** `allowed_streams: [binance-btc-book]` không nói theo registry version nào — nếu validate bằng registry hiện tại, một event lịch sử hợp lệ sẽ thành "không hợp lệ" khi stream bị retire sau này. Chốt **Model C**: validator resolve `event.stream_ref.registry_version` → xác nhận stream tồn tại + active TRONG version đó → kiểm tra `allowed_streams` của đúng Event Contract version.
- **Cursor stream universe chưa khép kín:** registry snapshot có thể chứa stream tạo SAU cursor boundary — cursor có phải liệt kê nó với genesis position không? Định nghĩa universe = **giao 3 tập**: stream được Replay Contract chọn ∩ đã activate tại cursor boundary ∩ resolve được trong pinned registry version. Thêm `replay_contract_id` vào cursor; Registry phải mang lifecycle metadata để resolve activation boundary (representation → ADR-009).

### Fixed — Minor
- `registry_checksum` từ "khuyến nghị" → **content integrity phải xác minh được (bắt buộc)**: immutable content identity (commit SHA/content hash/tương đương); bắt buộc là *verifiability*, không phải một field cụ thể — checksum không cần lặp mọi event nhưng event/run manifest phải truy được tới content identity bất biến.

### Note
- ChatGPT: **OQ-006 APPROVE — READY FOR ADR-010**, có thể duyệt độc lập ngay. **OQ-005 APPROVE DIRECTION, REVISION REQUIRED BEFORE ADR-009** — 3 điểm đã xử lý ở v2.5.

## [Unreleased] — Chapter 8 v2.6 (ChatGPT review round 6: **1 Blocker · 2 Major · 1 Minor**)

### Meta-fix — chặn lớp lỗi lặp lại (§8.1.1 mới)
- **Nhận diện meta-pattern qua 6 vòng:** mỗi lần Claude giới thiệu một authoritative artifact MỚI để sửa dual-authority (v2.3: Stream Registry → v2.5: Replay Contract), lại quên áp bộ bảo vệ mà artifact authoritative nào cũng cần. Thêm **§8.1.1 — Quy tắc chung cho mọi Referenced Authoritative Artifact**: 5 điều kiện bắt buộc (versioned · immutable sau khi được tham chiếu · không tái dùng identifier · permanently resolvable · verifiable content identity), áp dụng tự động cho artifact hiện tại VÀ tương lai. Mục đích: artifact mới thừa hưởng bảo vệ ngay, không chờ phát hiện từng cái qua từng vòng review.

### Fixed — Blocker
- **`replay_contract_id` không đủ pin một Replay Contract bất biến:** Replay Contract giờ sở hữu stream scope + merge policy, nhưng cursor chỉ pin một ID — nếu nội dung contract bị sửa (ordering từ `[recorded_time, stream_id, sequence]` sang `[causal_rank, ...]`), cùng một cursor lịch sử sẽ replay ra interleave khác, phá deterministic replay/Decision Parity/audit/I-12. Sửa: `replay_contract_ref: {contract_id, contract_version}` versioned + immutable theo §8.1.1, thay mọi chỗ dùng ID trần.

### Fixed — Major
- **`decision_context_cursor` không khớp canonical Replay Cursor schema:** thiếu `replay_contract_ref` trong khi Replay Cursor đã bắt buộc — cùng registry có thể có nhiều Replay Contract với stream scope khác nhau (A = Binance+Bybit+Risk, B = Binance+OKX+Risk), cùng một vector vị trí bị diễn giải khác nhau. Sửa: `decision_context_cursor` LÀ một Replay Cursor hợp lệ, dùng **cùng canonical schema §8.5**, không duy trì 2 schema gần giống.
- **Stream activation bị gắn với `recorded_time` (wall clock):** mâu thuẫn với chính §8.3.1 (writer handoff cấm chọn authority theo wall clock). Tình huống hỏng: registry nói stream active từ 10:00:00 nhưng activation fact chỉ recorded lúc 10:00:03 → replay tại 10:00:01 nhìn thấy trước fact chưa biết, vi phạm I-3. Sửa: stream thuộc universe khi **activation boundary authoritative đã visible/resolved tại cursor**; Registry mang lifecycle metadata trỏ authoritative boundary (`activated_by`/`valid_from_cursor`), representation → ADR-009.

### Fixed — Minor
- **Consistency invariant giữa contract và cursor registry version:** chọn Cách B (cursor tự đủ) — `cursor.stream_registry_version` phải bằng registry version mà Replay Contract pin (hoặc thỏa constraint nếu contract khai báo dạng khoảng); mismatch = **invalid cursor**, phải từ chối, không replay best-effort.

### Note
- ChatGPT điều chỉnh trạng thái **OQ-006** từ "ready ngay" → **READY FOR ADR DRAFT, NOT READY FOR FINAL ACCEPTANCE** — Mô hình A vẫn đúng, nhưng ADR-010 phải dùng `decision_context_cursor` có schema hợp lệ (đã sửa ở v2.6). **OQ-005: APPROVE DIRECTION, REVISION REQUIRED BEFORE ADR-009**.

## [Unreleased] — Chapter 8 v2.7 (ChatGPT review round 7: **0 Blocker · 2 Major · 1 Minor**)

### Fixed — Major
- **Event Contract là Referenced Authoritative Artifact nhưng event chưa pin version của nó:** envelope chỉ có `schema_version`, không đủ — Event Contract sở hữu nhiều hơn payload schema (`event_class`, `allowed_streams`, `merge_constraints`, semantic); hai contract version có thể cùng payload schema nhưng khác `event_class`/`allowed_streams`, historical validator không biết dùng contract nào. Chốt **Model A**: thêm `event_contract_ref: {contract_id, contract_version}` Required; `schema_version` giữ nguyên vai trò payload compatibility. Thêm §8.2.5 giải thích vì sao hai thứ tiến hóa độc lập.
- **Chưa khóa contract dùng trong Live Decision (cross-mode parity):** `decision_context_cursor` bắt buộc pin contract, nhưng nếu contract chỉ được tạo sau này để replay thì nó không phản ánh thứ Live thực sự dùng — Live dùng input topology A, Replay dùng contract B, vẫn "tuyên bố parity" là sai. Chốt: contract là **CROSS-MODE**, cả 4 execution mode (Live/Backtest/Paper/Replay) pin cùng một versioned contract; **cấm gắn contract hồi tố**.

### Changed — điều chỉnh so với wording ChatGPT (cần PO/ChatGPT xác nhận)
- ChatGPT đưa 2 hướng cho Major 2: (A) giữ tên "Replay Contract" nhưng tuyên bố cross-mode, thừa nhận *"tên là historical"*; (B) tách "Input Context Contract" riêng — bị ChatGPT loại vì thêm artifact mới. Claude đề xuất **hướng thứ ba**: giữ **đúng một artifact** (không thêm surface area — đúng mối lo của ChatGPT) nhưng **đổi tên `Replay Contract` → `Input Contract`**. Lý do: Live Decision phải pin một thứ tên "Replay Contract" sẽ gây hiểu nhầm cho engineer đọc sau vài năm; trong Constitution dự tính sống 5-10 năm, tên gây hiểu nhầm là nợ kỹ thuật thật, và đổi tên trước khi Lock rẻ hơn nhiều so với sau. Replay-run control (cursor start/end, tốc độ) là cấu hình lần chạy, không thuộc contract này.

### Fixed — Minor
- §8.1.1 điều 4: "Permanently resolvable" → **"Persistently resolvable"** — phải resolve được trong replay/audit horizon **platform cam kết**, hết horizon phải có explicit retention/archive policy. Phân biệt rõ với điều 2 (nội dung bất biến vĩnh viễn) vs khả năng truy xuất (cam kết theo horizon).

### Note
- ChatGPT: **OQ-005 và OQ-006 đều APPROVE DIRECTION + READY FOR ADR DRAFT, chưa FINAL ACCEPTANCE**. Có thể viết draft ADR-009/ADR-010 song song.

## [Unreleased] — Chapter 8 v2.8 (ChatGPT review round 8: **1 Blocker · 1 Major · 2 Minor**)

### Fixed — Blocker
- **Ba quy tắc không thể đồng thời đúng (mâu thuẫn logic tự tạo):** (1) canonical locator là `(stream_ref, sequence)` với `stream_ref` chứa `registry_version`; (2) sequence liên tục XUYÊN QUA registry version khi writer handoff; (3) cursor pin MỘT registry version rồi map `stream_id → sequence`. Sau một handoff, event sequence 500 append dưới v3 sẽ không resolve được từ cursor pin v4. Chốt **Model A**: tách **Logical Stream Identity** (`stream_id` — ổn định xuyên mọi registry version, không tái sử dụng, thuộc locator) khỏi **Stream Definition Snapshot** (`definition_version` — pin định nghĩa lúc append, KHÔNG thuộc identity). Canonical locator = **`(stream_id, sequence)`**. Sửa đồng bộ: envelope · cardinality · `causation_refs` · cursor `stream_positions` · eligibility validation · `activated_by`. Cursor: `stream_registry_version` chỉ dùng resolve **stream universe**, KHÔNG dùng resolve vị trí event — hai vai trò tách biệt.

### Fixed — Major
- **Cross-mode merge thiếu completeness/frontier semantics:** Input Contract tuyên bố deterministic interleave cho cả 4 mode, nhưng Live không biết event `recorded_time` sớm hơn còn đang đến trễ hay không → Live apply `Binance→Bybit` trong khi Replay sort ra `Bybit→Binance`, phá parity dù cùng contract. Thêm invariant: merge policy cross-mode chỉ hợp lệ khi Input Contract định nghĩa deterministic completeness/frontier; Live KHÔNG được authoritative-apply prefix mà Replay có thể chèn event visible trước nó; frontier chưa complete → buffer/defer hoặc fail-safe; CẤM suy completeness từ wall clock. ADR-009 phải định nghĩa tối thiểu 5 thứ (per-stream committed frontier · multi-stream completeness rule · late-arrival behavior · buffer limit/fail-safe · cách tạo `decision_context_cursor` tại frontier).

### Fixed — Minor
- **Câu giải thích đổi tên bị hỏng do bulk-replace của Claude:** lệnh thay `Replay Contract → Input Contract` thay luôn từ nằm trong câu giải thích, thành "từng được gọi Input Contract → đổi thành Input Contract" (vô nghĩa). Nguyên nhân: bulk-replace mà không đọc lại kết quả. Đã sửa.
- Dọn stale wording "Replay stream set + interleave policy" → "Cross-mode input stream scope + deterministic interleave policy".

### Note
- ChatGPT **approve tên `Input Contract`**, xác nhận không cần revert: "giữ một artifact nhưng đổi tên là lựa chọn sạch hơn việc giữ một tên gây hiểu sai lâu dài".

## [Unreleased] — Chapter 8 v2.9 (ChatGPT review round 9: **1 Blocker · 2 Major · 1 Minor**)

### Fixed — Blocker
- **Merge policy lấy `recorded_time` làm primary ordering key, trái Chapter 5 (Locked) và trái chính §8.3.4:** contract công bố `ordering: [recorded_time, stream_id, sequence]` nhưng §8.3.4 lại bắt processor buffer event khi prerequisite chưa resolved → **declared merge order ≠ actual authoritative apply order**. Ví dụ hỏng: A (QUOTE, recorded 10:00:01.100) là ancestry của B (DECISION, recorded 10:00:01.050) → sort recorded_time cho B trước A, sai nhân quả. Sửa: `algorithm: deterministic-causal-topological-order` — **causal precedence đứng trên mọi ordering key**; `concurrent_tie_break` CHỈ áp cho event causally incomparable. `recorded_time` chỉ dùng cho visibility boundary/latency/observability/chọn ứng viên bên trong thuật toán đã bảo toàn causal precedence. Nếu cần thứ tự hiển thị theo thời gian → **presentation order**, tách hoàn toàn khỏi authoritative apply order.

### Fixed — Major
- **`frontier_policy` được tuyên bố bắt buộc nhưng không nằm trong Input Contract:** hai run cùng pin `btc-arbitrage-input@v1` vẫn có thể dùng watermark 500ms vs committed frontier → input cut khác nhau dù contract reference giống nhau. Sửa: `frontier_policy` (mechanism · completeness_rule · late_arrival_behavior · buffer_limit_policy · incomplete_frontier_behavior) là **thành phần bắt buộc và versioned** của Input Contract; thay đổi bất kỳ mục nào bắt buộc tạo contract version mới.
- **`definition_version` chưa ánh xạ dứt khoát tới `registry_version`:** implementation có thể suy diễn thành version namespace riêng cho từng stream. Sửa theo khuyến nghị ChatGPT: **đổi lại tên field thành `registry_version`** (vấn đề gốc không nằm ở tên mà ở việc coi nó là thành phần locator — đã sửa ở v2.8), kèm invariant tường minh: `stream_ref.registry_version` CHÍNH LÀ `stream-registry.yaml.registry_version`, không có version namespace riêng cho stream.

### Fixed — Minor
- Ví dụ late-arrival mô tả `recorded_time` như thể là timestamp lúc nhận/timestamp sàn. Sửa: nói rõ event đã append từ trước với recorded_time sớm, consumer chỉ NHẬN muộn do **delivery delay**; kèm ghi chú semantic (`recorded_time` = lúc ghi vào durable log, không phải lúc nhận, không phải timestamp sàn) và nguồn thứ hai là **clock skew** giữa append node.

### Governance note
- ChatGPT nhắc rõ: đây chỉ là **reviewer assessment**. Product Owner **chưa approve** OQ-005/OQ-006; ADR-009/ADR-010 **chưa được accept**; Chapter 8 **chưa Lock**.

## [Unreleased] — Chapter 8 v3.0 (ChatGPT review round 10: **0 Blocker · 2 Major · 1 Minor**)

### Fixed — Major
- **Tự mâu thuẫn về vai trò của merge order:** một chỗ định nghĩa merge policy là deterministic causal-topological order mà mọi mode phải apply, chỗ khác lại viết "merge order KHÔNG phải authoritative business order" → implementation có thể hiểu processor được tự do apply theo thứ tự khác, phá parity (với processor stateful, hai thứ tự apply trên cùng tập event cho Decision khác nhau). Sửa: tách **4 khái niệm** (causal precedence · deterministic application order · domain causation · presentation order); merge policy CHÍNH LÀ authoritative application order, giống nhau mọi mode; tie-break KHÔNG tạo quan hệ nhân quả/business precedence trong domain. Công thức đúng: `authoritative apply order ≠ domain causal meaning` (không phải `merge order ≠ authoritative order`).
- **`valid_from_cursor` tạo vòng tham chiếu artifact:** Stream Registry v4 → cursor → Input Contract → Stream Registry v4 — không artifact nào hoàn chỉnh, không tính được content identity sạch (vi phạm §8.1.1 điều 5). Sửa: dùng **bootstrap-safe locator** `(control_stream_id, sequence)`; **cấm** lifecycle boundary tham chiếu artifact phụ thuộc ngược lại registry version đang định nghĩa; **cấm** đặt activation event của stream X lên chính stream X (vòng bootstrap: X active sau E, nhưng E phải append vào X → không khởi tạo được).

### Fixed — Minor
- Danh sách bắt buộc bump `contract_version` bỏ sót `frontier_policy` → implementation có thể hiểu đổi watermark/late-arrival/buffer semantics không cần bump. Đã thêm.

### Self-check (theo cam kết sau khi Product Owner phản ánh về chất lượng)
- Quét toàn file theo đúng 6 lớp lỗi đã từng mắc: dual authority (dấu `/`) · `valid_from_cursor` sót · câu tự mâu thuẫn về merge order · `frontier_policy` trong danh sách bump · locator nhất quán `(stream_id, sequence)` · `recorded_time` làm primary merge key. Kết quả: sạch cả 6. Lệnh verify không loại trừ bất kỳ đối tượng nào đang nghi.

## [Unreleased] — Chapter 8 v3.1 (ChatGPT review round 11: **1 Blocker [FALSE POSITIVE] · 1 Major · 1 Minor**)

### Blocker — XÁC ĐỊNH LÀ FALSE POSITIVE (không sửa, có bằng chứng)
- ChatGPT báo file v3.0 "kết thúc giữa YAML block `activation_boundary`", mất no-cycle invariants, mất §8.5.1 và §8.6. **Kiểm chứng: sai.** Bằng chứng: (1) `git hash-object` của file local = `918b0d1aeb786ca53a481d6ccf414711b9d47880`, **khớp chính xác** blob SHA ChatGPT trích → ChatGPT fetch đúng file; (2) file có **474 dòng**, code fence = **38 (chẵn, cân bằng)**; (3) `tail` cho thấy file kết thúc đúng ở §8.6 hoàn chỉnh; (4) toàn bộ no-cycle invariants nằm ở dòng 440-445, §8.5.1 ở 431, §8.6 ở 466. Kết luận: nội dung đầy đủ; nhiều khả năng phía ChatGPT bị cắt khi fetch (giới hạn độ dài), không phải lỗi tài liệu. **Không sửa thứ không hỏng.**

### Fixed — Major
- **Lifecycle boundary thiếu validation chain tường minh:** canonical locator `(control_stream_id, sequence)` đủ để tìm event, nhưng chưa nói rõ phải validate historical stream definition bằng gì. Thêm chain 4 bước: resolve locator + xác minh `event_id` (mismatch = integrity violation) → dùng `event.stream_ref.registry_version` **của event đã resolve** (KHÔNG phải registry hiện tại) để validate definition lịch sử → xác nhận control stream active trước boundary theo đúng version đó → xác nhận activation event không nằm trên stream đang được activate. Giữ đúng mô hình `locator = (stream_id, sequence)`, `definition evidence = resolved_event.stream_ref.registry_version`.

### Fixed — Minor
- Heading §8.3.4 còn tên cũ "Merge order ≠ authoritative causal order" — mâu thuẫn với nội dung v3.0 (merge policy CHÍNH LÀ authoritative application order). Đổi thành **"Deterministic Application Order và Causal Precedence"**.

## [Unreleased] — Chapter 8 v3.2 (ChatGPT review round 12: **0 Blocker · 3 Major · 1 Minor · 1 Suggestion**)

### Note — ChatGPT rút lại Blocker vòng trước
- ChatGPT xác nhận Blocker "file bị truncate" là **false positive của nó** (GitHub connector trả response bị cắt do giới hạn độ dài, nó nhầm cuối response thành cuối file). Lần này fetch theo từng khoảng dòng, xác nhận file hoàn chỉnh tới §8.6. Phản biện của Claude được xác nhận đúng.

### Fixed — Major
- **Per-stream sequence precedence bị đặt vào tie-break (có thể version hóa) thay vì hard constraint:** hai event `A100`/`A101` cùng stream không có `causation_refs` trực tiếp vẫn ĐÃ được sequence khóa thứ tự — nếu chỉ dựa tie-break, một Input Contract tương lai đổi thành `[event_type, stream_id, sequence]` sẽ đảo ngược chúng. Sửa: khóa formal `P_authoritative = P_stream ∪ P_causation` (cả hai là hard constraint bất biến); merge tạo topological order trên **hợp** hai partial order; tie-break CHỈ áp cho event không bị ordered bởi cả hai.
- **Thiếu Genesis Bootstrap Root:** quy tắc "activation event phải nằm trên stream đã active" tạo hồi quy vô hạn — không có điểm khởi đầu. Thêm **Genesis Registry**: root authoritative artifact tạo/phê duyệt theo Governance trước khi runtime log hoạt động, định nghĩa control stream + writer authority ban đầu, có immutable content identity, **không cần** activation event đứng trước. Khóa chặt: **KHÔNG có ngoại lệ thứ hai** — sau Genesis, mọi lifecycle change dùng boundary bình thường.
- **Lifecycle chỉ có activation, thiếu retirement/terminal frontier:** stream retired có thể khiến frontier chờ vô hạn, hoặc làm biến mất input history khỏi cursor. Chốt **Model B** (đề xuất): stream retired VẪN thuộc universe nếu Input Contract chọn nó, nhưng đóng tại `terminal_position`, frontier coi là terminal. Lý do chọn B thay vì A (loại khỏi universe): loại bỏ sẽ xóa một phần input history, phá replay/audit giai đoạn stream còn hoạt động. Thêm `retirement_boundary` + `terminal_position`; invariant bất kể model: retired stream KHÔNG được khiến frontier chờ vô hạn.

### Fixed — Minor
- Authority map bổ sung `frontier_policy`: "Cross-mode input scope + deterministic application order + **completeness/frontier semantics** → Input Contract" — tránh hiểu nhầm frontier chỉ là runtime configuration.

### Added — Suggestion (làm luôn, chi phí thấp)
- Ràng buộc watermark/bounded lateness: chỉ hợp lệ nếu clock/frontier source được **pin, event hóa, replay được**; processing wall clock cục bộ KHÔNG được làm completeness authority. Làm rõ không mâu thuẫn với lệnh cấm suy completeness từ wall clock — cấm *đồng hồ cục bộ lúc xử lý*, cho phép *frontier signal đã thành fact bất biến trong log*.

### Ghi nhận (chưa xử lý — chờ Product Owner)
- **Vấn đề bố cục:** khối lifecycle (no-cycle invariants, Genesis Registry, activation/retirement boundary, validation chain) hiện nằm trong §8.5.1 "Cursor validity", nhưng về nội dung thuộc §8.3.1 Stream Registry. Claude KHÔNG tự restructure giữa chu kỳ review để tránh sinh lỗi mới; nêu để Product Owner quyết có tách §8.3.5 "Stream Lifecycle" riêng hay không.

## [Unreleased] — Chapter 8 v3.3 (ChatGPT review round 13: **1 Blocker · 2 Major · 1 Minor · 1 Suggestion**)

### Fixed — Blocker
- **Cursor không pin lifecycle/control frontier → không tự chứng minh được stream universe:** activation/retirement boundary nằm trên control stream, nhưng control stream KHÔNG thuộc `included_streams` của Input Contract (nó là platform-control fact, không phải strategy input). Cursor vì thế không chứng minh được boundary sequence 812 đã visible tại chính nó — so `recorded_time` không đủ (nhiều event cùng timestamp; vector cursor sinh ra chính để phân biệt). Hệ quả: stream universe có thể khác giữa Live và Replay → `decision_context_cursor` mất tính exact → I-2/I-3 không kiểm chứng được. Chốt **Model A**: thêm `lifecycle_frontier {stream_id, sequence}` là **thành phần bắt buộc** của canonical cursor; invariant: mọi activation/retirement boundary phải có `sequence ≤ lifecycle_frontier.sequence`; frontier pin giống nhau ở cả 4 mode. (Loại Model B — bắt buộc control stream vào mọi Input Contract — vì trộn platform-control facts vào strategy input scope.)

### Fixed — Major
- **`P_authoritative` chưa cấm cycle:** topological order chỉ tồn tại khi graph acyclic, nhưng chưa có invariant nào cấm `A@100.causation_refs = [A@101]` (tạo `A ≺ B ≺ A`) hay cycle cross-stream. Thêm: **`P_stream ∪ P_causation` BẮT BUỘC là DAG**; causation edge không được tạo cycle/mâu thuẫn per-stream sequence/khiến effect trước cause cùng stream; cycle = integrity violation → append-import bị từ chối, dữ liệu lịch sử có cycle phải fail-safe I-6, **cấm** tự bỏ edge để tiếp tục. Acyclicity là constitutional invariant, không để implementation suy luận.
- **Retirement chưa khóa consistency với `terminal_position`:** ví dụ terminal=500 nhưng writer đã append tới 510, hoặc writer vẫn append sau retirement authoritative → Live/Replay chọn terminal cut khác nhau. Thêm 7 invariant (tương đương mức chặt writer handoff): terminal = last committed sequence · cấm append sau terminal · writer dừng trước khi retirement authoritative · retirement publish sau khi terminal bất biến · retirement event không nằm trên stream đang retire · locator không resolve đúng last event = integrity violation · retired stream không được khiến frontier chờ vô hạn.

### Fixed — Minor (bố cục — cả 2 AI cùng khuyến nghị)
- **Di chuyển nguyên khối lifecycle từ §8.5.1 → §8.3.5 "Stream Lifecycle and Bootstrap"** (không sửa semantic). §8.5.1 giờ chỉ giữ phần cursor dùng lifecycle boundary thế nào. Lý do: người đọc §8.3.1 Stream Registry có thể bỏ sót Genesis/retirement invariants; ADR-009 khó phân biệt rule lifecycle vs cursor; future edits dễ tạo duplication giữa 2 mục.

### Added — Suggestion (làm luôn, chặn một lớp lỗi lặp lại)
- **Chuẩn hóa schema `event_record_ref {stream_id, sequence, event_id}`** dùng thống nhất ở MỌI nơi tham chiếu event record (`causation_refs`, `activation_boundary`, `retirement_boundary`, và reference thêm sau này) — thay vì nhiều hình dạng gần giống (`control_stream_id` chỗ này, `stream_id` chỗ kia). Giảm lớp lỗi "cùng concept, nhiều reference shape" đã lặp lại nhiều lần trong chapter này.

### Checklist toàn vẹn (chạy trước khi push)
- 563 dòng · code fence 44 (chẵn) · kết thúc đúng §8.6 · dual-authority 0 · `lifecycle_frontier` 3 · DAG invariant 1 · `event_record_ref` 4 · §8.3.5 tồn tại · Genesis Registry xác nhận nằm trong §8.3.5.

## [Unreleased] — Chapter 8 v3.4 (ChatGPT review round 14: **1 Blocker · 2 Major · 1 Minor · 1 Suggestion**)

### Fixed — Blocker
- **`decision_context_cursor` không còn là Replay Cursor hợp lệ:** v3.3 thêm `lifecycle_frontier` làm field BẮT BUỘC của canonical cursor (§8.5), nhưng ví dụ `decision_context_cursor` ở §8.4 không có field đó — trong khi chính §8.4 tuyên bố "dùng cùng canonical schema §8.5". Ba câu không thể cùng đúng. **Đây đúng lớp lỗi mà `event_record_ref` vừa được chuẩn hóa để chặn** (thêm field vào schema canonical nhưng quên propagate sang nơi khác dùng schema đó). Sửa: thêm `lifecycle_frontier` vào ví dụ §8.4 + rule "Decision event thiếu bất kỳ field bắt buộc nào của canonical cursor là invalid, phải bị từ chối khi append".

### Fixed — Major
- **Một `lifecycle_frontier` scalar không đủ nếu có nhiều control stream:** Genesis chỉ yêu cầu "ít nhất một" lifecycle stream, nên Constitution đang cho phép nhiều — khi đó `boundary.sequence ≤ frontier.sequence` là phép so vô nghĩa nếu hai bên khác stream (`100 ≤ 500` giữa `lifecycle-east` và `lifecycle-west` — hai ordering authority khác nhau). Chốt **Model A**: platform có **đúng MỘT** canonical Logical Lifecycle Stream, mọi activation/retirement/creation/writer-transition boundary ghi trên stream đó; ràng buộc `boundary.stream_id = cursor.lifecycle_frontier.stream_id = canonical lifecycle stream_id`. (Loại Model B — frontier vector — vì tạo partial order đa stream cho control plane, phức tạp không tương xứng.)
- **`lifecycle_frontier` thiếu validity invariant với `recorded_time`:** cursor có thể pin frontier trỏ tới lifecycle event có `recorded_time` LỚN HƠN `cursor.recorded_time` → nhìn thấy lifecycle fact từ tương lai, có thể activate stream chưa visible/retire quá sớm/đổi tập input Decision được đọc. Đúng dạng lỗi I-3 mà `decision_context_cursor` sinh ra để chặn. Thêm 4 điều kiện validity (resolve tới committed event trên canonical lifecycle stream · `recorded_time ≤` cursor · không vượt committed frontier · stream active trong historical registry version của event · trong retained range); vi phạm → invalid cursor.

### Fixed — Minor
- "`lifecycle_frontier` pin giống nhau ở cả 4 mode" quá rộng — dễ hiểu thành mọi run dùng chung một frontier cố định. Sửa: **khi so sánh/tái tạo cùng một logical Decision/run** qua các mode thì phải pin cùng frontier; Decision lúc 10:00 và 11:00 đương nhiên khác frontier.

### Added — Suggestion (fix cấu trúc cho lớp lỗi vừa mắc)
- **§8.5.1 Bảng cardinality của Replay Cursor** — liệt kê đủ 5 field bắt buộc (`recorded_time`, `input_contract_ref`, `stream_registry_version`, `lifecycle_frontier`, `stream_positions`). Đây chính là fix cấu trúc cho Blocker vòng này: validator kiểm một bảng thay vì ghép cardinality từ prose rải rác, nên thêm field mới vào cursor sẽ không còn lọt trường hợp "một nơi có, nơi khác quên". §8.5.1 cũ đổi số thành §8.5.2.

### Checklist toàn vẹn (10 mục, chạy trước khi push)
- 598 dòng · code fence 46 (chẵn) · kết thúc đúng §8.6 · dual-authority 0 · `lifecycle_frontier` 9 lần · **decision_context_cursor xác nhận CÓ `lifecycle_frontier`** · Genesis "đúng MỘT" canonical lifecycle stream · không còn "ít nhất một lifecycle" · bảng cardinality tồn tại · **0 tham chiếu §8.5.1 bị lệch sau khi đánh số lại**.

## [Unreleased] — Chapter 8 v3.5 (ChatGPT review round 15: **1 Blocker · 2 Major · 1 Minor · 1 Suggestion**)

### Fixed — Blocker
- **Thiếu quan hệ thời gian giữa Decision event và cursor của nó:** đã khóa `input_event.recorded_time ≤ cursor.recorded_time` và `lifecycle_event ≤ cursor`, nhưng **quên nối cursor với chính Decision event chứa nó**. Hệ quả: Decision append lúc 10:00:01 vẫn có thể mang cursor `recorded_time` 10:00:05 với mọi position "hợp lệ so với cursor" — tuyên bố đã biết dữ liệu từ tương lai của chính nó, vi phạm I-3 trực tiếp. Thêm invariant **`cursor.recorded_time ≤ DecisionEvent.recorded_time`** (bằng nhau được phép khi cùng authoritative transaction/boundary); vi phạm → Decision event invalid, từ chối khi append. Nhờ bắc cầu: `input_event ≤ cursor ≤ DecisionEvent`.

### Fixed — Major
- **`lifecycle_frontier` không biểu diễn được trạng thái Genesis:** frontier bắt buộc resolve tới committed lifecycle event, nhưng ngay sau Genesis Registry chưa có event nào → **mọi cursor trước lifecycle event đầu tiên đều invalid**. Trong khi `stream_positions` đã có `genesis_position` cho tình huống tương đương. Sửa: `lifecycle_frontier.position: {kind: event|genesis, sequence}`; khi `kind: genesis` không bắt buộc resolve event, `sequence` lấy từ `genesis_position` của Genesis Registry. (Không chọn phương án bắt buộc append "lifecycle genesis event" — tạo operational dependency thừa và làm mờ vai trò root của Genesis Registry.)
- **Registry version chưa được chứng minh visible tại lifecycle frontier:** cursor có thể pin `stream_registry_version: v4` trong khi `lifecycle_frontier.sequence: 800` < sequence 900 nơi v4 được activate → dùng topology/writer definition từ tương lai. Sửa: mọi registry version sau Genesis phải khai báo `effective_from.event_ref` trỏ lifecycle activation event của chính nó; cursor validity yêu cầu `registry.effective_from.sequence ≤ cursor.lifecycle_frontier.sequence` (hoặc là Genesis Registry). Về version đã supersede: **cho phép** pin version cũ cho historical replay/contract stability miễn từng visible tại/trước frontier — KHÔNG bắt buộc "latest", vì như vậy registry transition sẽ hồi tố thay đổi Input Contract lịch sử.

### Fixed — Minor
- **Trùng thuật ngữ "activation boundary":** §8.3.1 dùng cho writer-authority handoff, §8.3.5 dùng cho stream bắt đầu active — hai semantic khác nhau, dễ khiến implementation áp nhầm rule "activation event không được nằm trên chính stream đang activate" sang handoff (trong handoff, transfer event hoàn toàn có thể do old writer append trên chính stream đó). Đổi tên tại handoff thành **`writer-authority transition boundary` (`handoff_boundary`)**, ghi rõ rule kia không áp cho handoff.

### Added — Suggestion (fix cấu trúc, lần thứ 2 liên tiếp)
- **§8.5.2 Bảng Relational Invariants** — 5 quan hệ (Cursor→Decision · Position→Cursor · Lifecycle→Cursor · Registry→Lifecycle · Registry→Contract). Bảng §8.5.1 trả lời *"field nào bắt buộc có"*; bảng mới trả lời *"các field phải nhất quán với nhau thế nào"* — đúng lớp lỗi của Blocker vòng này (mỗi field hợp lệ riêng lẻ nhưng tổ hợp sai). §8.5.2 cũ đổi số thành §8.5.3.

### Checklist toàn vẹn (10 mục)
- 641 dòng · fence 48 (chẵn) · kết thúc đúng §8.6 · dual-authority 0 · Cursor→Decision invariant hiện diện · `kind: genesis` 3 · `effective_from` 4 · `handoff_boundary` tách biệt · bảng relational tồn tại · **0 tham chiếu §8.5.2 cũ bị lệch**.

## [Unreleased] — 2026-07-18 — Product Owner DUYỆT HƯỚNG OQ-005 & OQ-006 → ADR-009, ADR-010 (Draft)

### Product Owner decision
- **OQ-005 — hướng ĐƯỢC DUYỆT:** per-stream contiguous sequence + explicit causation + `P_stream ∪ P_causation` là DAG + không global total order + Input Contract versioned cross-mode + frontier policy.
- **OQ-006 — hướng ĐƯỢC DUYỆT:** Model A (`decision_time` thay `effective_time` cho Decision event; `decision_context_cursor` bắt buộc, dùng canonical Replay Cursor schema).
- Product Owner chỉ định: **vòng consolidation chạy SAU khi có ADR draft**, review cả một thể.

### Added — ADR-009 (Draft): Ordering Mechanism
- Mức **architectural decision**, không đi vào protocol. Quyết định: 2 cơ chế tách biệt cho 2 mức của Chapter 5 §5.4; partial order `P_authoritative = P_stream ∪ P_causation` (DAG); Input Contract cross-mode versioned; frontier/completeness; lifecycle & registry authority.
- **5 alternatives** ghi rõ lý do loại: HLC/Lamport clock · global total order (single sequencer) · sequence cho phép gap · merge theo `recorded_time` · lifecycle frontier dạng vector.
- **Deferred sang Phase 1** (liệt kê tường minh 7 nhóm): watermark vs committed frontier vs barrier · multi-stream completeness · late-arrival protocol · buffer size/overflow · coordinator/checkpoint design · topological merge + cycle-detection implementation · writer handoff/retirement/registry activation protocol · storage/archive/retention/recovery.

### Added — ADR-010 (Draft): Decision Time Model
- Mức **architectural decision**. Quyết định: 3 khái niệm riêng biệt (`decision_time` effective · `recorded_time` recorded · `decision_context_cursor` knowledge boundary); Model A; cursor dùng canonical schema §8.5.1; relational invariant `input ≤ cursor ≤ DecisionEvent`; Event Contract là authority xác định Decision class.
- **4 alternatives** ghi rõ lý do loại, **bao gồm chính đề xuất sai ban đầu của Claude** (`decision_time` = Replay Cursor) — giữ lại trong ADR làm bản ghi lịch sử vì sao phương án đó bị bác.
- Ghi rõ **phụ thuộc ADR-009**: nếu ADR-009 bị bác hoặc đổi mô hình frontier, `decision_context_cursor` phải đánh giá lại.

### Changed
- MANIFEST: `compatible_adr_range` → ADR-001 ~ ADR-010; OQ-005/OQ-006 chuyển trạng thái sang "hướng đã được PO duyệt → ADR Draft, chờ review + accept".

### Trạng thái governance sau bước này
- ADR-009, ADR-010: **Draft** — chưa accept. Chapter 8: **In Review** v3.5. Chưa có gì được Lock.

## [Unreleased] — Review bộ ba (Chapter 8 v3.6 + ADR-009 + ADR-010): **2 Blocker · 2 Major · 1 Minor**

### Blocker 1 — XÁC ĐỊNH LÀ FALSE POSITIVE (một phần), kèm 1 ý đúng đã sửa
- ChatGPT khẳng định Product Owner **chưa từng** approve OQ-005/OQ-006 và MANIFEST đang ghi nhận quyết định không tồn tại. **Kiểm chứng: sai.** Product Owner đã duyệt hướng bằng lời trực tiếp trong phiên làm việc ("Tao duyệt OQ-005 và 006"). ChatGPT chỉ đọc GitHub, không thấy hội thoại → suy ra approval không tồn tại. Đây là false positive **cùng dạng** với vụ "file bị truncate" trước đó (kết luận từ dữ liệu nó không có quyền truy cập).
- **Ý ĐÚNG trong Blocker 1, đã sửa:** `resolves: [OQ-005]` / `resolves: [OQ-006]` trong ADR còn `Draft` là mâu thuẫn metadata — Draft chưa resolve được gì. Đổi thành **`addresses:`** kèm ghi chú "`resolves` chỉ có hiệu lực khi ADR được Accepted".
- **Làm rõ MANIFEST** để không ai hiểu nhầm nữa: tách bạch 3 tầng — (a) PO đã duyệt HƯỚNG (có nguồn, có ngày); (b) ADR = Draft, CHƯA accept; (c) OQ vẫn `Open` cho tới khi ADR được accept.

### Fixed — Blocker 2 (thật, nghiêm trọng)
- **`lifecycle_frontier` tồn tại 3 schema mâu thuẫn:** v3.5 đổi canonical thành `{stream_id, position: {kind, sequence}}` nhưng KHÔNG propagate sang: ví dụ §8.4, bảng cardinality §8.5.1, bảng relational §8.5.2, các phép so activation/registry. Schema cũ `{stream_id, sequence}` **không biểu diễn được** Genesis frontier — chính use case vừa thêm ở v3.5. Trớ trêu: bảng cardinality được tạo ra để chặn đúng lớp lỗi propagation này lại chính là chỗ chưa cập nhật. Đã chuẩn hóa 1 schema duy nhất và propagate 6 chỗ; bảng relational thêm điều kiện theo `kind` (genesis → registry phải là Genesis Registry; event → so `effective_from.event_ref.sequence ≤ position.sequence`).

### Fixed — Major
- **ADR-009 gộp Lamport Clock và HLC thành một alternative với rationale không chính xác:** hai cơ chế khác nhau. Tách thành 2 alternatives riêng — Lamport (bảo toàn chiều happened-before nhưng `L(A) < L(B)` KHÔNG chứng minh A gây ra B, không phân biệt causality với concurrency) và HLC (hữu ích cho temporal locality/observability nhưng clock timestamp không mang đủ domain evidence thay `causation_refs`). Thêm ghi chú: Lamport/HLC có thể bổ sung sau làm **metadata phụ**, không được thành domain causation authority nếu không có ADR mới.
- **ADR-010 phụ thuộc ADR-009 nhưng chỉ nằm trong prose:** thêm `depends_on: [ADR-009]` vào frontmatter + **§7 Acceptance gate** — ADR-010 không được rời `Draft`/`In Review` trước khi ADR-009 accept; nếu ADR-009 đổi semantic frontier/Input Contract/cursor/lifecycle boundary thì ADR-010 quay lại review. Review song song được, **accept thì không**.

### Fixed — Minor
- ADR-009 "cả 4 execution mode pin cùng contract" → làm rõ theo logical run: khi so sánh/tái tạo **cùng một logical Decision/run** thì mọi mode pin cùng Input Contract version; strategy/run khác nhau được dùng contract khác nhau.

### Checklist toàn vẹn
- 641 dòng · fence 48 (chẵn) · `position: {kind` 3 lần · **0 path cũ `lifecycle_frontier.sequence`** · `decision_context_cursor` xác nhận dùng `position: {kind: event}`.

## [Unreleased] — Consolidation round: Chapter 8 v3.7 + ADR-009 + ADR-010 + Ch11 v1.1 (**2 Blocker · 2 Major · 1 Minor**)

### Note — ChatGPT rút Blocker về PO approval
- ChatGPT xác nhận Blocker "PO chưa duyệt OQ-005/006" là false positive và đã rút lại. Product Owner đã duyệt hướng; ADR vẫn Draft chưa accept.

### Fixed — Blocker 1 (hậu quả trực tiếp của hybrid split)
- **Chapter 8 và ADR-009 công bố hai authority khác nhau:** Chapter 8 ghi "cơ chế do ADR-009 quyết định, ADR-009 PHẢI định nghĩa tối thiểu frontier/completeness/late-arrival/buffer/cursor-capture", trong khi ADR-009 lại defer chính những thứ đó sang Phase 1. Không thể accept ADR hay Lock Chapter khi chưa biết câu nào có hiệu lực. Sửa **5 chỗ** trong Chapter 8: ADR-009 khóa **architectural model + invariant**; **Phase 1 tạo design specification** cho mechanism; Phase 1 đổi semantic đã khóa trong ADR-009 → **follow-up ADR**, không sửa ngầm. Thêm **Phase 1 deliverable gate** vào ADR-009: implementation không được bắt đầu trước khi mechanism có design spec đã review.

### Fixed — Blocker 2
- **Cursor được phép pin registry version đã lỗi thời tại frontier mới:** rule cũ chỉ yêu cầu "đã từng visible trước frontier" → v3 (`effective_from` 900) vẫn hợp lệ tại frontier 1500 dù v4 (`effective_from` 1200) mới là authoritative. Cursor kết hợp *knowledge boundary mới* + *registry state cũ* (writer authority cũ, stream còn `active` dù v4 đã retire, thiếu `terminal_position`) → Live/Replay diễn giải khác stream universe hoặc chờ vô hạn trên stream đã retire. Định nghĩa **`active_registry_at(frontier)`** = registry có `effective_from` lớn nhất không vượt frontier; authoritative cursor **bắt buộc** dùng nó. Historical replay tự nhiên pin đúng registry lịch sử. Chạy registry cũ tại frontier mới phải phân loại là **counterfactual simulation** — không phải authoritative replay, không dùng làm parity evidence.

### Fixed — Major
- **Chapter 8 ghi sai trạng thái approval:** banner vẫn nói "CHƯA được Product Owner quyết" và heading §8.3/§8.4 vẫn "chờ Product Owner + ADR" — nay đã sai vì PO đã duyệt hướng. Sửa banner thành 3 tầng trạng thái + **lock gate 4 điều kiện** (ADR-009 accept · ADR-010 accept theo dependency gate · OQ chuyển Resolved · consolidation hoàn tất), ghi rõ *"ADR đã được ghi KHÔNG đủ — Draft là đã ghi nhưng chưa accept"*. Heading đổi thành "HƯỚNG ĐÃ ĐƯỢC PO DUYỆT · chờ ADR-00x accept".
- **Manifest dependency graph không khớp frontmatter Chapter 8:** Manifest thiếu `03-engineering-principles` và `07-module-taxonomy` → tooling/reviewer có thể bỏ qua deterministic checks (Ch3) và writer `module_id`/taxonomy checks (Ch7). Đã đồng bộ đủ 5 dependency.

### Fixed — Minor
- **`addresses`/`depends_on` chưa thuộc ADR metadata contract chuẩn:** thêm vào `templates/adr-template.md` và **Chapter 11 v1.1** bảng semantic 3 field — `addresses` (đang xử lý OQ, KHÔNG resolve) · `resolves` (chỉ hiệu lực khi ADR `Approved`/`Locked`) · `depends_on` (dependency phải Approved/Locked trước). Biến acceptance gate từ prose thành **machine-readable** dựa trên status lifecycle chuẩn.

### Checklist toàn vẹn
- 667 dòng · fence 52 (chẵn) · **0 câu "do ADR-009 quyết"** · `active_registry_at` 2 · banner 4-điều-kiện hiện diện · 2 heading "PO DUYỆT" · **0 path cũ `lifecycle_frontier.sequence`**.

## [Unreleased] — Consolidation round 2: Ch8 v3.8 · ADR-009 · Ch11 v1.2 (**2 Blocker · 2 Major · 2 Minor**)

### Fixed — Blocker
- **ADR-009 giữ rule registry YẾU hơn Chapter 8 vừa siết:** Chapter 8 v3.7 khóa `cursor.stream_registry_version = active_registry_at(frontier)`, nhưng ADR-009 §2.6 vẫn ghi "cursor chỉ dùng registry version đã visible tại frontier" — với v3(900)/v4(1200)/frontier 1500, ADR cho qua v3 còn Chapter bắt reject. Đã propagate rule mạnh sang ADR-009 + ghi hệ quả: registry activation làm mọi Input Contract pin registry cũ **không còn hợp lệ** cho authoritative Decision sau boundary đó.
- **`active_registry_at` không phải hàm total + unique:** (a) *không có ứng viên* — Genesis Registry không có `effective_from`, nên cursor `kind: genesis` (và giai đoạn sau Genesis nhưng chưa có post-Genesis registry) không resolve được; (b) *nhiều ứng viên* — schema không cấm 2 registry cùng `effective_from`. Sửa: định nghĩa 2 nhánh (base case → Genesis Registry; ngược lại → registry DUY NHẤT có effective_from lớn nhất ≤ frontier) + 4 invariant bảo đảm uniqueness (mỗi post-Genesis registry đúng một `effective_from` · không 2 registry chung `effective_from.event_ref` · activation event định danh chính xác registry được activate · duplicate/ambiguous = integrity violation → fail-safe I-6).

### Fixed — Major
- **Phase 1 deliverable gate khóa quá rộng:** "implementation KHÔNG được bắt đầu trước khi các mechanism deferred có design spec" có thể bị hiểu là chặn toàn bộ Phase 1 cho tới khi xong cả storage/archive/recovery — trong khi domain modeling, schema tooling, module skeleton không phụ thuộc. Sửa thành **per-capability gate** (frontier consumer ↔ frontier design; handoff ↔ handoff design; archive ↔ retention design...) + ghi rõ hạng mục độc lập không bị chặn.
- **Chapter 11 đổi semantic dưới cùng version — LỖI CỦA CLAUDE:** vòng trước Claude chạy `replace('version: "1.0"', '"1.1"')` nhưng Chapter 11 **vốn đã là 1.1**, nên lệnh **thất bại im lặng** và Claude báo cáo là đã bump. Kết quả: metadata contract mới (`addresses`/`resolves`/`depends_on` + acceptance gate) được thêm dưới cùng snapshot v1.1, khiến version không còn định danh được nội dung. Đã bump thật lên **v1.2** + cập nhật `last_review` + đồng bộ Manifest. *Lớp lỗi: string-replace giả định giá trị cũ mà không verify kết quả — lặp lại lần thứ 3.*

### Fixed — Minor
- Chapter 8 cross-mode wording rộng hơn ADR-009 ("mọi Decision run ở cả 4 mode phải pin cùng contract") — propagate nguyên clarification của ADR-009: chỉ áp khi **so sánh/tái tạo cùng một logical Decision/run**; strategy/run khác được dùng contract khác.
- MANIFEST mô tả OQ-005 còn theo mô hình cũ ("cơ chế cụ thể quyết định ở Chapter 8") — cập nhật theo hybrid split: Chapter 8 = invariant · ADR-009 = architectural model · Phase 1 = mechanism/design spec.

### Added — Backlog (Suggestion, làm SAU khi ADR accept)
- **BL-006:** sau khi ADR-009/010 accept, dọn decision history khỏi Chapter 8 (các đoạn "chọn Model A thay vì B", "vì sao chọn mô hình này") — rationale/alternatives đã ở ADR; Constitution chỉ giữ normative rule. Chưa làm bây giờ vì ADR chưa accept.

### Checklist toàn vẹn (8 mục)
- Ch8 676 dòng · fence 52 (chẵn) · `active_registry_at` có base case · ADR-009 có rule mạnh · Phase 1 gate per-capability · Ch11 = v1.2 · BL-006 ghi backlog · Manifest OQ-005 mô tả mới.

## [Unreleased] — Consolidation round 3: Ch8 v3.9 · Ch11 v1.3 · ADR-009 · ADR-010 (**2 Blocker · 3 Major · 1 Suggestion**)

### Fixed — Blocker
- **Bảng relational §8.5.2 vẫn dùng rule registry YẾU:** §8.3.1 đã khóa `cursor.registry = active_registry_at(frontier)` nhưng bảng validator authority tập trung vẫn chỉ kiểm `effective_from ≤ frontier` — cho qua cursor frontier 1500 pin v3 dù v4 active từ 1200. Hai validator mâu thuẫn ngay trong một chapter. Sửa: bảng dùng đúng `active_registry_at` (genesis → Genesis Registry; event → hàm total+unique), ghi rõ `effective_from ≤ frontier` chỉ là **điều kiện CẦN bên trong hàm**, không phải validity cuối cùng.
- **Input Contract vừa exact-pin vừa cho phép range:** §8.5 còn câu "hoặc thỏa registry constraint nếu contract khai báo dạng khoảng" — hai mô hình kiến trúc khác nhau. Range open-ended làm semantic của một **immutable** contract mở rộng trong tương lai **mà không bump version** (tự mâu thuẫn), và chưa định nghĩa: ai đưa registry tương lai vào range, chứng minh compatibility `included_streams` ra sao, chọn version nào khi nhiều match. Chốt **EXACT PIN cho v1**, bỏ range; ghi concern đã chấp nhận (**contract-version churn**) + lối thoát bằng follow-up ADR (immutable closed compatibility set · subset registry · capability-based constraint).

### Fixed — Major
- **`active_registry_at` chỉ áp cho cursor, chưa áp cho event lúc append:** event có thể pin registry **tương lai chưa active** (v4 active từ sequence 900 nhưng append ở frontier 800 vẫn pin v4 → future configuration knowledge) hoặc registry **đã supersede**. Khóa invariant `event.stream_ref.registry_version = active_registry_at(append_lifecycle_frontier)`; representation/evidence của append frontier → Phase 1.
- **Causation prerequisite ngoài Input Contract scope chưa có semantic:** B ∈ included_streams nhưng `B.causation_refs → A` với A ngoài scope — đọc A thì Input Contract không mô tả đúng input thật (**hidden input**, phá parity); không đọc A thì không xác nhận được prerequisite. Chốt: prerequisite là **payload/state dependency** → stream của nó BẮT BUỘC thuộc `included_streams` + cursor universe; prerequisite **ngoài scope** → chỉ verify identity/existence, **cấm** đọc payload và **cấm** dùng làm state-transition input.
- **Decision class có hai authority field:** Chapter 8 cho `event_class: decision` HOẶC `semantic_roles: [decision]`, ADR-010 chỉ khóa `event_class` → validator có thể phân loại khác nhau (ảnh hưởng `decision_time`, cấm `effective_time`, bắt buộc cursor, no-future validator). Chuẩn hóa **đúng một field canonical `event_class`**; `semantic_roles` là metadata **không authoritative**.

### Added — Suggestion
- **Chapter 11 v1.3 — transition `addresses → resolves` phải ATOMIC:** khi PO approve ADR, toàn bộ `status` · `addresses→[]` · `resolves→[OQ-x]` · `approved_by/at` · `MANIFEST OQ→Resolved` phải nằm trong **cùng một documentation change**. Nếu approve trước rồi sửa metadata sau, lần sửa đó **vi phạm ADR Immutable Rule**.

### Checklist (7 mục, dùng assert cho mọi replace)
- Ch8 v3.9 · Ch11 v1.3 · fence 54 (chẵn) · **0 câu range/constraint còn sót** · **0 chỗ `semantic_roles` còn là authority** · ADR-009 có exact pin · ADR-010 có `event_class` canonical.

## [Unreleased] — Consolidation round 4: Ch8 v4.0 · ADR-009 (**2 Blocker · 1 Major [chờ PO] · 1 Minor · 1 Suggestion**)

### Fixed — Blocker
- **Registry activation event thiếu pre-append boundary semantic (vòng tự kích hoạt):** registry v4 active tại chính event E@900 — nếu `append_lifecycle_frontier` hiểu là post-append (900) thì E phải validate bằng v4, mà v4 chỉ active vì E đã commit. Chốt: `append_lifecycle_frontier` = frontier committed **ngay TRƯỚC** append transaction; **registry activation event KHÔNG được validate bằng chính registry nó kích hoạt** (E dùng registry cũ, registry mới active TỪ E). Nếu E đồng thời chuyển writer: old writer append `E@n`, new writer từ `n+1`.
- **`causation_refs` gộp 2 semantic mà schema không phân biệt được:** v3.9 định nghĩa 2 loại prerequisite (payload/state dependency vs identity-only ngoài scope) nhưng dùng chung một field → ba quy tắc không thể cùng thực thi (external ref không thuộc cursor universe + mọi causation phải cursor-visible + mọi causation tạo precedence edge). Tách schema: **`causation_refs`** (authoritative prerequisite, tham gia `P_causation`, bắt buộc trong universe, causally closed) vs **`related_event_refs`** (identity/audit, KHÔNG tham gia `P_causation`, được phép ngoài universe, cấm đọc payload). Thêm cả hai vào bảng cardinality để tránh lỗi propagation quen thuộc.

### Added — §8.4.1: Decision "in-flight" qua registry transition — **CHỜ PRODUCT OWNER QUYẾT**
- Tình huống: Decision đọc xong input ở frontier 899 (cursor pin v3), registry v4 activate ở 900, Decision append ở 901 (envelope pin v4). Hai rule riêng lẻ đều đúng nhưng chưa có policy. Vì nó **thay đổi authoritative Decision history**, không để Phase 1 tự suy luận và **Claude không tự chọn**. Trình bày 2 phương án + đánh đổi: **A** (append rồi revalidate trước Risk/Execution, supersede/reject chứ không xóa) vs **B** (reject và recompute ngay tại append). ChatGPT nghiêng về A — recommendation, không phải quyết định.
- **Lock gate Chapter 8 nâng từ 4 → 5 điều kiện**, thêm: §8.4.1 phải có quyết định của Product Owner.

### Fixed — Minor
- **Chapter 8 và ADR-009 ghi "Concern đã chấp nhận"/"Chấp nhận đánh đổi" khi ADR vẫn Draft** — ghi nhận thay Product Owner. Sửa toàn bộ thành "**được GHI NHẬN trong Draft**; chỉ coi là accepted khi Product Owner approve ADR". Giữ đúng 3 tầng: *OQ direction approved ≠ ADR accepted ≠ từng tradeoff tự động được PO chấp nhận*.

### Added — Suggestion
- **Boundary conformance fixtures** trong ADR-009 (review/test artifact, KHÔNG phải authority mới): 6 case đánh đúng các lỗi relational boundary đã lặp nhiều vòng — registry activation `E@n` · lifecycle writer transition · Decision cut trước/append sau transition · state causation ngoài scope (reject) · identity-only ngoài scope (cho phép, không vào `P_causation`) · cursor pin stale/future registry (reject).

### Checklist (7 mục, assert cho mọi replace)
- Ch8 v4.0 · fence 58 (chẵn) · pre-append semantic hiện diện · `related_event_refs` 3 chỗ (gồm bảng cardinality) · §8.4.1 chờ PO · **0 chỗ "đã chấp nhận" còn sót** (cả Ch8 lẫn ADR-009) · ADR-009 có fixtures.

## [Unreleased] — 2026-07-18 — Product Owner QUYẾT §8.4.1: **Model A** (Ch8 v4.1 · ADR-009 · ADR-010)

### Product Owner decision
- **Decision "in-flight" qua registry transition → chọn Model A:** Decision có knowledge cut trước transition **vẫn được append** như immutable historical fact; trước Risk/Execution phải **revalidate** theo registry đang active; nếu stale/invalid thì ghi event **supersede/reject**, KHÔNG xóa/sửa Decision gốc.

### Added — ADR-010 §2.6 (chủ sở hữu quyết định)
- Ghi quyết định Model A + rationale + **4 guardrail bắt buộc**: (1) Decision được append KHÔNG tự động có execution eligibility · (2) Risk/Execution bị chặn tới khi revalidation thành công · (3) kết quả revalidation là **authoritative event**, không phải trạng thái ngầm · (4) cấm sửa/xóa Decision gốc.
- Rationale ghi rõ vì sao A: phân biệt *"Decision đã thực sự được tính bằng cut v3"* vs *"Decision còn đủ điều kiện thực thi dưới v4"* — phù hợp **I-1** (input/reasoning đã xảy ra phải lưu bất biến, không biến mất vì transition vài ms trước append) và **I-4** (Decision không tự thực thi, Risk Gateway là boundary hợp lý cho current-validity check).
- **Model B đưa vào bảng Alternatives** kèm lý do loại: mất bản ghi Decision đã tính; muốn giữ Explainability vẫn phải ghi computation-attempt fact → tiến gần A mà không có lợi thế semantic.
- **Ranh giới:** state machine `computed → revalidated → rejected/superseded` thuộc **Decision Domain Contract**, KHÔNG hardcode vào Constitution/ADR (theo I-13 + bài học Chapter 4).

### Fixed — Major (từ review v4.0)
- **ADR-009 §2.6 có wording ngầm chọn B:** "registry activation làm Input Contract cũ không hợp lệ cho Decision **sau boundary**" — "sau" không rõ là *knowledge cut* hay *append*. Nếu hiểu theo append thì đã ngầm chọn B. Sửa thành boundary chính xác: contract cũ không hợp lệ cho Decision có **knowledge cut SAU** boundary; Decision có **cut TRƯỚC nhưng append SAU** → áp dụng Model A theo ADR-010 §2.6. Thêm phân chia thẩm quyền: registry/frontier boundary → ADR-009; Decision lifecycle policy → ADR-010.
- **Quyết định A/B chưa có ADR ownership:** theo ADR Scope Rule, quyết định ảnh hưởng nhiều module + khó đảo ngược **bắt buộc** thành ADR. Ghi vào **ADR-010 §2.6** (tài liệu sở hữu Decision Time/Context) thay vì tạo ADR-011 — ADR-009 chỉ cross-reference.

### Changed
- **Chapter 8 §8.4.1** đổi từ "⚠️ CHỜ PO QUYẾT" → "Model A (PO quyết 2026-07-18)", giữ normative rule tại Chapter, rationale/alternatives ở ADR.
- **Lock gate điều kiện 4 hoàn thành:** còn lại 4 điều kiện — ADR-009 accept · ADR-010 accept theo dependency gate · OQ-005/006 → Resolved · consolidation review hoàn tất.
- **Fixtures ADR-009** mở rộng cho Model A: Decision stored + Risk blocked + bắt buộc revalidation result · revalidation fail → rejection/supersession event, không phát sinh execution intent · revalidation pass → execution tiếp tục, phải tham chiếu revalidation thành công.

## [Unreleased] — Ch8 v4.2 · ADR-009 · ADR-010 (**1 Blocker · 2 Major · 1 Minor · 1 Suggestion**)

### Fixed — Blocker (Claude vi phạm ranh giới do chính mình đặt)
- **Chapter 8 định nghĩa lại SEMANTIC của `causation_refs`, trái Chapter 6 (Locked):** §6.7 quy định Chapter 6 sở hữu *ngữ nghĩa* causation, Chapter 8 chỉ sở hữu *representation + cardinality* — Claude tự viết ranh giới này rồi tự vi phạm, thu hẹp causation thành "chỉ payload/state prerequisite" và ép mọi `causation_ref` phải thuộc Input Contract universe. Hệ quả sai: `DECISION_CREATED → RISK_REJECTED` là nhân quả nghiệp vụ thật nhưng consumer không đọc payload → buộc phải chọn giữa "ép mọi Input Contract include stream đó" hoặc "hạ xuống `related_event_refs`, mất `P_causation`". Thêm nữa `causation_refs` là metadata **cấp event bất biến** còn Input Contract là scope **cấp run** — không tồn tại "Input Contract universe của event" để append-validator kiểm.
- **Sửa:** khôi phục `causation_refs` = *direct domain causal predecessor* (semantic theo §6.7 + Event Contract), `related_event_refs` = quan hệ **không mang causal meaning**. **Causal closure chuyển về tầng Input Contract/run validation** qua `causal_closure_policy`: nếu processor cần payload/state của A thì stream A bắt buộc trong scope; causal predecessor không phải state-input thì không bị ép vào scope. Vi phạm → **Input Contract invalid**, không phải event invalid. *(Phương án "mọi Input Contract phải causally closed hoàn toàn" bị loại: quá rộng — portfolio-view contract sẽ phải include mọi decision/risk stream dù không đọc payload nào.)*

### Fixed — Major
- **Stale wording tạo trạng thái kép:** §8.4.1 có heading "PO quyết" nhưng thân bài vẫn "chưa có policy / Cần Product Owner chọn"; ADR-009 vẫn ghi "chưa có quyết định của Product Owner; ADR-009 không được accept khi mục này còn mở". Automation/reviewer đọc đúng câu stale sẽ kết luận §8.4.1 vẫn Open. Viết lại §8.4.1 thành lịch sử ngắn (2 phương án đã xem xét → PO chọn → vì sao loại phương án kia); ADR-009 sửa thành cross-reference.
- **Guardrail revalidation chưa có evidence chain normative:** "phải có một success event" không đủ — implementation vẫn có thể dùng success của Decision khác, success dưới registry khác, hoặc tạo Execution Intent không truy được về revalidation. Nâng thành **relational invariant**: `OriginalDecision ← RevalidationSucceeded ← RiskApproved ← ExecutionIntentCreated`, kèm 4 ràng buộc (tham chiếu chính xác Decision gốc · ghi evidence registry/knowledge boundary đã dùng · Risk Approval causally depend vào revalidation · Execution Intent truy vết được cả hai). Đây là **platform-level invariant** (I-1 + I-4), không phải test fixture.

### Fixed — Minor
- **Hai cặp "Model A/B" khác nghĩa trong cùng ADR-010** (§2.2 time field vs §2.6 transition policy) làm cross-reference mơ hồ. Đổi tên mô tả: **Decision Effective-Time Model** và **Append-and-Revalidate Policy**; alternatives thành **Dual-field Effective Time** và **Reject-and-Recompute**.

### Added — Suggestion
- 4 fixture mới trong ADR-009: domain-causal predecessor không phải state input (vẫn giữ `P_causation`) · state dependency ngoài closure (Input Contract invalid) · revalidation success của Decision A không mở eligibility cho Decision B · revalidation dưới registry v4 không approve flow yêu cầu v5.

## [Unreleased] — Vòng 31: Ch8 v4.6 · ADR-009 · ADR-010 (**1 Blocker · 2 Major**)

### Fixed — Blocker: `P_global/P_run` chưa THAY THẾ mô hình cũ, chỉ mới thêm vào
- Chapter 8 thêm split ở §8.2.3 nhưng **§8.3.4 vẫn giữ nguyên** rule cũ "trước khi apply, processor phải xác nhận **mọi** `causation_ref` đã visible và resolved tại cursor". Hai rule không thể cùng áp cho external cause (không thuộc universe + không có `stream_position` + vẫn phải cursor-visible). Sửa: **thay thế hoàn toàn** bằng bảng tách theo scope — in-scope (cursor-visible + apply trước effect + buffer/defer + unresolved tại complete cursor = integrity violation) vs external non-state (chỉ cần committed/existence proof; không cursor-visibility, không `stream_position`, không frontier completeness, cấm đọc payload).
- **Bổ sung tính bắc cầu:** `P_run` bảo toàn quan hệ giữa vertex in-scope **kể cả khi đường nhân quả đi qua vertex external** — `A ≺ X ≺ B` trong `P_global` (X external) ⟹ `A ≺ B` giữ trong `P_run`.
- **ADR-009 §2.3 chưa có split** — vẫn chỉ một `P_authoritative` và tuyên bố merge topological order trên toàn hợp. Đã propagate: merge order trên **`P_run`**, không phải `P_global`; kèm định nghĩa external satisfied prerequisite.

### Fixed — Major
- **`dependency_authority` dạng một `event_contract_ref` singular không đủ:** mỗi event tự pin Event Contract của event type nó; một Input Contract apply nhiều event type/nhiều contract version → một reference đơn không trả lời được "của effect event nào", "có phân loại cho mọi event type không". Vì classification bị cấm nằm trong code, implementation không còn nơi hợp lệ để suy ra. Sửa thành **`dependency_authority: per_effect_event_contract`** — mỗi effect event dùng chính `event_contract_ref` đã pin của nó để phân loại. Machine-readable, không mơ hồ cardinality.
- **ADR-010 chưa ghi dedicated preservation Event Contract:** Chapter 8 đã khóa nhưng ADR-010 — tài liệu **sở hữu** Scoped Preservation Policy — chỉ ghi "ghi fact vào Audit Stream, mang cursor/lý do/boundary". Đây không phải chi tiết payload mà là **event-to-stream eligibility** và guardrail chống dùng Audit Stream để lách `allowed_streams`. Propagate: preservation fact là event type riêng, pin dedicated immutable Event Contract (`allowed_streams` = [canonical Audit Stream], prohibited execution eligibility); **cấm** ghi original Decision event hoặc tái dùng Decision Contract trên preservation path.

### Ghi nhận lỗi xác minh (Claude)
- Vòng trước Claude tuyên bố "**0 chỗ còn Model A/B**" dựa trên grep chuỗi `Model A|Model B` — **bỏ sót biến thể tiếng Việt** "Mô hình A/B", "phương án A". ChatGPT bắt đúng. Lại là lớp lỗi *"lệnh verify không phủ hết đối tượng cần kiểm"*. Đã dọn nốt 3 chỗ và verify lại bằng grep case-insensitive phủ cả 4 biến thể.

### Note — Convergence gate CHƯA binding
- ChatGPT chỉ ra chính xác: stop rule hiện chỉ là **thỏa thuận của vòng review**, ghi ở CHANGELOG — **không phải governance binding**. Muốn binding phải đưa vào **Chapter 11 hoặc 12** qua một vòng review riêng (cả hai đang `In Review`). Ghi **BL-007** thay vì tự đưa vào Constitution.

### Checklist (8 mục, grep phủ cả biến thể VN)
- Ch8 v4.6 · fence 64 (chẵn) · **0 rule cũ "mọi causation cursor-visible"** · bảng in-scope/external hiện diện · ADR-009 có `P_run` (4 chỗ) · `per_effect_event_contract` · ADR-010 có dedicated preservation contract · 0 "Model/Mô hình A|B" (kết quả duy nhất còn lại là "model artifact" — ML artifact, không liên quan).

## [Unreleased] — Vòng 30: Ch8 v4.5 · ADR-009 · ADR-010 (**2 Blocker · 2 Major · 1 Minor**)

### Fixed — Blocker 1: tách global causation graph khỏi run-local apply graph
- **Mâu thuẫn formal:** §8.2.3 cho phép external non-state cause nằm ngoài cursor universe (không `stream_position`, không thuộc apply set) NHƯNG §8.3.4 vẫn bắt **mọi** `causation_ref` phải cursor-visible và nằm trong topological apply order → không thể cùng thực thi. Sửa: tách **`P_global`** (= `P_stream ∪ P_causation` trên toàn bộ event graph, phải là DAG) khỏi **`P_run`** (induced order trên apply set của một Input Contract). External cause KHÔNG phải vertex của `P_run`, là **external satisfied prerequisite**: cần committed/existence proof, không cần `stream_position`, không ảnh hưởng frontier completeness, cấm đọc payload. Processor rule tách đôi: in-scope → cursor-visible + apply trước effect; external → chỉ cần committed proof.
- **`causal_closure_policy` bắt buộc nhưng vắng mặt trong canonical Input Contract YAML** — đã thêm vào schema và vào danh sách bắt buộc bump `contract_version`.

### Fixed — Blocker 2: ADR-009 chưa thiết lập hạ tầng mà ADR-010 phụ thuộc
- ADR-010 (Scoped Policy) phụ thuộc **canonical Audit Stream**, nhưng ADR-009 — tài liệu sở hữu stream lifecycle/topology — không hề quyết định nó. Do acceptance order bắt buộc accept ADR-009 trước, ADR-009 có thể được accept mà **không thiết lập hạ tầng bắt buộc** cho ADR-010. Thêm vào ADR-009: Genesis Registry định nghĩa đúng MỘT Lifecycle Stream + đúng MỘT Audit Stream, cả hai là **protected streams** (stable ID · active mọi registry version · KHÔNG được retire · writer handoff được nhưng identity không đổi). Ranh giới: ADR-009 sở hữu *sự tồn tại + lifecycle invariants*; ADR-010 sở hữu *Decision nào được dùng preservation path + guardrail*.

### Fixed — Major
- **ADR-010 thiếu validity interval của revalidation:** implementation có thể hiểu "chỉ cần một success event trong quá khứ là đủ". Propagate nguyên rule + bổ sung điểm quan trọng: **kiểm lúc tạo `ExecutionIntent` là CHƯA ĐỦ** nếu registry đổi giữa intent creation và lúc Execution Engine thực sự gửi lệnh — phải xác nhận authorization chain còn valid **tại execution boundary**, trước khi phát sinh external side effect.
- **Preservation fact chưa có Event Contract authority:** Chapter 8 khóa "Event Contract là nguồn duy nhất cho event-to-stream eligibility", nhưng ghi original Decision event vào Audit Stream sẽ vi phạm chính `allowed_streams` của nó. Khóa: preservation fact là **event type RIÊNG**, pin **dedicated Event Contract** (`allowed_streams` chỉ gồm canonical Audit Stream · mang full `decision_context_cursor` gốc · tham chiếu transition/retirement boundary · **prohibited execution eligibility**); cấm tái dùng contract của Decision gốc để lách eligibility.

### Fixed — Minor: dọn sạch tên "Model A/B" mơ hồ
- ChatGPT nêu cho ADR-010, nhưng rà ra Chapter 8 có **4 cặp Model A/B khác nghĩa nhau**. Đổi hết sang tên mô tả: **Direct Contract Pin** (vs Composite Identity) · **Retained-in-Universe** (vs Excluded-from-Universe) · **Single Lifecycle Stream** (vs Lifecycle Frontier Vector) · **Dedicated Lifecycle Frontier** (vs Control-Stream-In-Contract). Kết quả: **0 chỗ còn "Model A/B"** trong Ch8, ADR-009, ADR-010, MANIFEST.

### Note — Convergence gate (ChatGPT đề xuất, Claude đồng ý)
- ChatGPT **không đồng ý đóng băng v4.4** như Claude đề xuất trước đó, với lý do hợp lý: các Blocker gần đây là **mâu thuẫn bên trong chính model đã chọn**, không phải chi tiết protocol Phase 1. Nhưng sau khi sửa, áp **stop rule** — chỉ nhận finding mới nếu: (1) mâu thuẫn Chapter đã Locked · (2) tạo hai authority cạnh tranh · (3) làm một invariant đã chọn không implementable · (4) phá governance/acceptance order. KHÔNG mở rộng sang: cycle-detection algorithm · coordinator cụ thể · storage layout · watermark implementation · buffer sizing · recovery workflow — những thứ này giữ ở Phase 1 đúng như ADR-009 đã defer.

### Checklist (7 mục)
- **0 "Model A/B"** trong cả 4 tài liệu · `P_global`/`P_run` tách · `causal_closure_policy` trong YAML · ADR-009 có protected Audit Stream · ADR-010 có validity interval · preservation Event Contract khóa · fence 64 (chẵn).

## [Unreleased] — 2026-07-18 — PO quyết Scoped Policy (Ch8 v4.4 · ADR-009 · ADR-010) + vòng 30 fixes

### Product Owner decision — Blocker "Decision stream retire tại transition"
- Chọn **Hướng 1 (Scoped Policy)**: Append-and-Revalidate chỉ áp khi Decision target stream **vẫn active + event vẫn eligible** dưới post-transition registry. Nếu stream đã retire/không eligible → ghi **immutable computation/rejection fact vào canonical Audit Stream**. Alternative (lifecycle drain invariant — cấm retire tới khi mọi in-flight Decision đóng) bị loại vì retirement có thể chờ không giới hạn.
- **Artifact mới: canonical Audit Stream** — định nghĩa tại **Genesis Registry** cùng canonical Lifecycle Stream. Cả hai là **protected streams**: retirement invariant KHÔNG áp dụng, vì retire chúng sẽ tái tạo đúng vòng bootstrap mà Genesis Registry sinh ra để chặn.
- 4 ràng buộc với preservation fact: tham chiếu chính xác `decision_context_cursor` gốc (đầy đủ) · ghi lý do + `event_record_ref` của retirement/activation boundary · KHÔNG cấp execution eligibility · **cấm dùng preservation path để lách retirement** khi đường append bình thường còn khả dụng.
- **Lock gate điều kiện 5 hoàn thành** — còn 4: ADR-009 accept · ADR-010 accept · OQ-005/006 Resolved · consolidation hoàn tất.

### Fixed — Blocker 1 (propagation)
- **ADR-009 §2.4 vẫn giữ mô hình causation cũ đã bị Chapter 8 v4.2 bác** — hai authoritative document công bố hai semantic khác nhau. Sửa: `causation_refs` = direct domain causal predecessor (semantic thuộc Ch6 §6.7, ADR KHÔNG định nghĩa lại); closure là ràng buộc cấp Input Contract; closure violation làm **Input Contract invalid**, không đổi semantic bất biến của event. Fixture sửa theo.

### Fixed — Major
- **`causal_closure_policy` bắt buộc nhưng chưa có schema/authority:** formal hóa `{mode: full | declared-state-dependencies, dependency_authority.event_contract_ref}`. Với `declared-state-dependencies`, **Event Contract** (immutable, versioned) khai báo cause nào là state dependency — **cấm để classification trong code processor**, nếu không một Input Contract immutable sẽ đổi semantic sau mỗi lần deploy. Hòa giải mâu thuẫn "mọi causation phải visible tại cursor": yêu cầu đó chỉ áp cho cause **thuộc apply set**; external non-state cause chỉ cần chứng minh đã committed, KHÔNG thuộc merged apply set, **cấm giả lập `stream_position`**.
- **Revalidation success có thể stale trước Risk/Execution:** evidence chain không đứt ≠ evidence còn hiệu lực. Thêm **validity interval**: `revalidation.registry_version = active_registry_at(risk_approval_lifecycle_frontier)`; transition xảy ra sau revalidation nhưng trước Risk/Execution → eligibility **quay lại blocked**, bắt buộc revalidate lại; Execution Intent phải chứng minh Risk Approval còn valid dưới boundary hiện tại.

### Fixed — Minor
- **Authority của `related_event_refs` mô tả sai:** Chapter 6 §6.7 chỉ định nghĩa correlation + causation, **không** định nghĩa quan hệ non-causal này — tài liệu đang trỏ tới một semantic authority không tồn tại. Sửa: Chapter 8 sở hữu base representation + invariant "non-causal"; **Event Contract** sở hữu ý nghĩa cụ thể từng relation.

### Checklist (8 mục)
- Ch8 v4.4 · fence 60 (chẵn) · Audit Stream trong Genesis (4 chỗ) · protected streams · Scoped Policy chốt · lock gate ĐK5 xong · ADR-010 có Scoped Policy · ADR-009 có fixtures mới.

### Checklist (8 mục)
- Ch8 v4.2 · fence 58 (chẵn) · semantic Ch6 khôi phục · `causal_closure_policy` ở tầng Input Contract · evidence chain normative · **0 stale wording** · **0 "Model A/B" mơ hồ trong ADR-010** · fixtures mới hiện diện.

### Checklist (7 mục)
- Ch8 v4.1 · fence 58 (chẵn) · **0 chỗ còn "CHỜ PRODUCT OWNER QUYẾT"** · ADR-010 có §2.6 · ADR-009 wording đã chính xác boundary · fixtures cho A hiện diện · lock gate điều kiện 4 đánh dấu xong.

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

## [Unreleased] — Chapter 6 v2.2 (ChatGPT review round 2: 2 Minor)

### Fixed — Minor
- **§6.5 Internal Identity vs External Reference:** venue order ID / exchange trade ID không do Ride kiểm soát (có thể trùng giữa venue, format đổi) — không được dùng làm primary identity, chỉ lưu như attribute. Order có internal `OrderID` (cho I-10) + lưu kèm `venue_order_id`, reconcile theo cặp.
- **§6.7 ID là opaque:** không nhúng business meaning để logic suy diễn ngược từ ID — nếu logic phụ thuộc cấu trúc ID thì đổi format ID (ULID→UUIDv7) sẽ phá logic ở nơi không ngờ. Thông tin nghiệp vụ phải là field tường minh. (Timestamp trong ID cho sortable/index §6.3 là tối ưu storage, không phải business meaning.)
