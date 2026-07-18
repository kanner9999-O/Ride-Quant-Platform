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
