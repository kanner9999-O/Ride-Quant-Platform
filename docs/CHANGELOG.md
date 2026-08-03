# Changelog — Ride Quant Platform Docs

Format dựa theo [Keep a Changelog](https://keepachangelog.com/), áp dụng cho toàn bộ `/docs`.

## [Unreleased] — 2026-08-03 — finalize Package 0.3-C UX authority boundaries

**Package 0.3-C final narrowly bounded correction — đóng đúng ba finding từ delta review trên baseline v0.2.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Perform exactly one final narrowly bounded correction for: P03C-MAJ-01/P03C-B-MAJ-01/P03C-B-MAJ-02." Đã resolved Minor findings (`P03C-MIN-01`/`P03C-MIN-02`/`P03C-MIN-03`) KHÔNG bị revisit/broaden, trừ collateral consistency edit bắt buộc. Authorization này **không** cho phép sửa `product-requirement.md`/`use-case-workflow.md`/Domain Contract/Constitution/ADR/architecture, tạo `PR-XXX`/`UC-XXX` mới, invent `PaperSession` entity/session persistence/timeout/backend lifecycle, invent Strategy Instance schema/field/validation/API/database/command/event implementation, invent permission/authorization/route-guard architecture, invent PAPER-context Decision establishment mechanism, đóng OQ-002/OQ-003, authorize Live, hay Approve/Lock/Consolidate bất kỳ artifact nào.

### Baseline and blob verification

```text
Expected HEAD:  0b890ca4ee13be5feb0971afd2aee39dcc3b6032
Actual HEAD:    0b890ca4ee13be5feb0971afd2aee39dcc3b6032  — match

ux-blueprint.md:          v0.2 Draft, blob 1d5fd9d2e2bd7b6e9c88353e193cd1230b6cd6a3  — match
product/README.md:        blob 20f407773d6a4db08a51f36067844ea1f5d8a4ae  — match
product-requirement.md:   v0.2 Draft, blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8  — match, Consolidated Stable
use-case-workflow.md:     v0.3 Draft, blob affbb723b577cde4c8627dd689550e3bfbffb5d1  — match, Consolidated Stable
```

### Finding-by-finding resolution

| Finding | Resolution |
|---|---|
| `P03C-MAJ-01` | v0.2 traceability syntactically exhaustive nhưng materially overbroad — thu hẹp toàn bộ theo nguyên tắc "presence trong destination/transient-state/parent-journey KHÔNG tự tạo material ownership". `WS-001` (§5): thu hẹp từ union gần-toàn-bộ UC-001–021/PR-001–034 xuống ĐÚNG 5 item shell thực sự sở hữu (Account context, Instrument/Venue context, Strategy Instance context, historical cursor context, Live Unauthorized label) — bỏ "Lifecycle-stage navigation bar" (thuộc NAV-XXX), "Evidence/authority labels" (thuộc từng SCR/VIEW), "Blocked/unavailable-state presentation" (thuộc từng STATE-XXX) khỏi bảng trace của WS-001. `STATE-001` loading: thu hẹp còn ĐÚNG SCR-001/SCR-002/SCR-003 — ba screen duy nhất tường minh ghi "STATE-001 loading" tại field Primary states (§7), KHÔNG còn 16. `STATE-002` empty: thu hẹp còn ĐÚNG bốn genuine empty-collection screen (SCR-004/SCR-005/SCR-007/SCR-011) — loại SCR-003/SCR-009 (unfilled form, KHÔNG phải empty collection) và SCR-008 (spec riêng tường minh "KHÔNG áp dụng" cho blocked/empty). `FLOW-001` PR traceability: thu hẹp từ ~25 PR xuống ĐÚNG 7 PR biểu diễn stage-ordering/selection-gate/Research-verification-guard/Backtest→Paper-handoff/Paper→Review-handoff/Review→Improve-handoff/Improve→Research-loop-back (PR-001/003/015/016/017/024/028/031/034) — giữ nguyên UC-001–021 toàn bộ vì FLOW-001 CHÍNH LÀ primary end-to-end journey, không phải fallback coverage. §14 rebuilt lại hoàn toàn theo union đã thu hẹp; thêm traceability-quality rule tường minh; xác nhận PR-004/PR-005/PR-014 KHÔNG có UX acceptance surface riêng (platform-level guarantee restatement, upstream invariant — thay đổi có chủ đích, không phải thiếu sót). |
| `P03C-B-MAJ-01` | Định nghĩa Paper Strategy Instance binding contract đầy đủ, KHÔNG invent `PaperSession` domain entity/architecture. Mở rộng `UX-INV-3` (§3): pin áp dụng cho Replay/Backtest/Paper (trước chỉ ngụ ý Research/Replay/Backtest); Research quan sát vẫn KHÔNG cần pin. Thêm "Paper Strategy Instance binding contract" (§3) định nghĩa ranh giới UX-visible start (ngay sau VIEW-001 pin, TRƯỚC SCR-006 resolve Decision lineage) / active (xuyên suốt SCR-006/SCR-007) / end (khi thoát bounded Paper interaction) / sau-end (Instance khác có thể pin lần sau) — KHÔNG session identifier/storage/timeout/persistence mechanism/backend lifecycle nào định nghĩa. `VIEW-001` (§7.1) mở rộng hỗ trợ pin cho Paper (entry từ NAV-004/SCR-006 khi STATE-028), giữ nguyên KHÔNG tạo Instance mới. `SCR-006` (§7.4) hiển thị tường minh danh tính Strategy Instance/Strategy Definition Version/Account/Instrument/Venue pin TRƯỚC khi resolve PAPER Decision lineage; mọi fact trong chuỗi system-owned resolve về đúng pin đó. `SCR-007` (§7.4) hiển thị liên tục cùng danh tính pin từ SCR-006 xuyên suốt C7 inspection. Bốn nguyên nhân Paper blocked phân biệt tường minh, KHÔNG BAO GIỜ gộp: `STATE-003` (invalid Instrument/Venue), `STATE-028` (Paper Strategy Instance not selected, MỚI), `STATE-029` (Paper Strategy Instance selected but not pinned, MỚI), `STATE-011` (PAPER Decision lineage unavailable, CHỈ sau khi đã pin). `NAV-004` (§5a) cập nhật Required context/Blocked behavior tương ứng theo đúng thứ tự ba điều kiện. |
| `P03C-B-MAJ-02` | Thêm `VIEW-006` — Strategy Instance Creation/Binding (§7.6, mới, first-class, đủ 20 field theo cùng format mọi SCR/VIEW khác) — bounded product handoff giữa "tạo Strategy Definition Version" (SCR-010/UC-019) và "chọn/pin Instance để dùng" (VIEW-001/UC-002); KHÔNG định nghĩa schema/field/validation/API/database/command/event implementation. Stable-ID range cập nhật: `VIEW-001`–`VIEW-006` (6 VIEW, trước 5), 17 screen/view tổng (trước 16). §4 Information Architecture cập nhật vị trí VIEW-006 dưới NAV-006. `VIEW-001` xác nhận tường minh KHÔNG BAO GIỜ tự tạo Strategy Instance — CHỈ chọn/pin Instance đã đăng ký. `SCR-010` exits sửa: VIEW-006 (đăng ký) thay vì "VIEW-001 tạo Instance"; thêm SCR-001 read-only tuỳ chọn. `FLOW-006` viết lại: SCR-010 → SCR-001 (tuỳ chọn, KHÔNG pin) → [khi cần commit] VIEW-006 (đăng ký) → VIEW-001 (chọn/pin) → VIEW-002 (verification) → SCR-002/SCR-003; lối tắt SCR-010→VIEW-006 trực tiếp vẫn khả dụng — KHÔNG hai thứ tự mandatory mâu thuẫn. §9 cross-stage handoff "Improve → Research" đồng nhất với FLOW-006. `NAV-006` (§5a) cập nhật Destination/Required context/UC/PR traceability thêm VIEW-006. |

### Exact changed-file scope

```text
docs/product/ux-blueprint.md         MODIFIED v0.2 → v0.3   blob a432782a9c74ccd971757271707c71c3f00bf4f9
docs/product/README.md               MODIFIED v0.9 → v1.0   blob b3105a873c69db22172e30842e28ef9b845d25ab
docs/MANIFEST.md                     MODIFIED manifest_version 9.88 → 9.89
docs/CHANGELOG.md                    MODIFIED (this entry)
docs/product/product-requirement.md  KHÔNG ĐỔI — blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8, verified byte-identical
docs/product/use-case-workflow.md    KHÔNG ĐỔI — blob affbb723b577cde4c8627dd689550e3bfbffb5d1, verified byte-identical
docs/domain/                          KHÔNG ĐỔI
docs/adr/                             KHÔNG ĐỔI
docs/constitution/                    KHÔNG ĐỔI
docs/architecture/                    KHÔNG ĐỔI
```

### Corrected artifact version and status

`ux-blueprint.md`: `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null`.

### Stable ID counts and ranges

`WS-001` (1); `NAV-001`–`NAV-006` (6); `SCR-001`–`SCR-011` (11); `VIEW-001`–`VIEW-006` (6, +1 từ v0.2 — `VIEW-006` mới); `FLOW-001`–`FLOW-006` (6); `STATE-001`–`STATE-029` (29, +2 từ v0.2 — `STATE-028`/`STATE-029` mới) — tất cả unique, sequential, contiguous within namespace. 17 total screen/view artifacts (11 `SCR` + 6 `VIEW`) cover all 21 Use Cases.

### Traceability materiality (script-verified)

Regex/set-comparison script xác nhận sau khi thu hẹp: mọi `UC-001`–`UC-021` (21/21) và `PR-001`–`PR-034` (34/34, trừ PR-004/PR-005/PR-014 — xác nhận có chủ đích KHÔNG có UX acceptance surface) vẫn xuất hiện tại ít nhất một artifact mapping direct/bounded; không artifact nào còn dùng full-range UC/PR union làm fallback coverage NGOẠI TRỪ `FLOW-001` (được task cho phép tường minh vì là primary journey) và các trường hợp STATE-001/STATE-002 đã liệt kê đầy đủ+chính xác theo đúng exception clause của task.

### Paper Strategy Instance binding boundary

Ranh giới UX-visible start/active/end/sau-end được định nghĩa đầy đủ tại §3 "Paper Strategy Instance binding contract" — KHÔNG `PaperSession` entity, session identifier, session storage, timeout, hay persistence mechanism nào được invent; SCR-006/SCR-007 hiển thị danh tính pin liên tục xuyên suốt; bốn nguyên nhân blocked (STATE-003/028/029/011) luôn phân biệt tường minh.

### Strategy Instance creation UX boundary

`VIEW-006` sở hữu duy nhất hành vi đăng ký Strategy Instance gắn Strategy Definition Version mới — `VIEW-001` xác nhận KHÔNG BAO GIỜ tự tạo Instance. Không schema/field/validation/API/database/command/event implementation nào được định nghĩa cho VIEW-006.

### Forbidden-scope verification

Không `PR-XXX`/`UC-XXX` mới tạo; `product-requirement.md`/`use-case-workflow.md` không đổi (verified `git diff --stat` + `git hash-object`, byte-identical); không Domain Contract/Constitution/ADR/architecture nào sửa; không `PaperSession` entity/session persistence/timeout/backend lifecycle invented; không Strategy Instance schema/field/validation/API/database/command/event implementation invented; không permission/authorization/route-guard architecture invented; không cơ chế PAPER-context Decision establishment nào invented (vẫn deferred, §15); resolved Minor findings (`P03C-MIN-01`/`P03C-MIN-02`/`P03C-MIN-03`) không bị regress; OQ-002/OQ-003 không đóng; Live không authorize; không artifact nào Approved/Locked; Package 0.3-C không mark `Consolidated Stable`.

### Author self-review

Automated re-verification: `WS`(1)/`NAV`(6)/`SCR`(11)/`VIEW`(6)/`FLOW`(6)/`STATE`(29) unique/sequential/contiguous; script-based extraction xác nhận toàn bộ `UC-001`–`UC-021` và `PR-001`–`PR-034` (trừ PR-004/005/014, chủ đích) xuất hiện tại ít nhất một artifact direct mapping; markdown table column-count consistency re-verified across toàn bộ file (không malformed row); forbidden domain-entity names (bao gồm `PaperSession` mới) confirmed appearing only inside prohibition/boundary text; YAML frontmatter re-validated via `yaml.safe_load` (`version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null`); `git status --porcelain`/`git diff --stat` xác nhận CHỈ bốn file được phép thay đổi, `product-requirement.md`/`use-case-workflow.md`/toàn bộ Domain Contract/ADR/Constitution chapter/architecture artifact byte-identical.

### Metadata / state

- `ux-blueprint.md`: **v0.2 → v0.3**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `product-requirement.md`/`use-case-workflow.md`: **không đổi** — byte-for-byte, `Consolidated Stable` package states unchanged.
- `product/README.md`: **v0.9 → v1.0**.
- `MANIFEST.md`: `manifest_version` **9.88 → 9.89**.
- Mọi Domain Contract, ADR, Constitution chapter, architecture artifact: **không đổi.**

**Package 0.3-C: final narrowly bounded correction đã author, status Draft, chưa `Consolidated Stable`, đang chờ ChatGPT Final Delta Review A.** Mandatory sequence tiếp tục: ChatGPT Final Delta Review A → Independent Review B → Product Owner consolidation decision. `OQ-002`/`OQ-003` vẫn `Open`. Không authorize Live. Không artifact nào Approved hay Locked. Phase 0.3 vẫn active — Phase 0 vẫn active và chưa hoàn tất; Phase 1 vẫn unauthorized.

## [Unreleased] — 2026-08-03 — correct Package 0.3-C review findings

**Package 0.3-C bounded correction — consolidated ChatGPT Review A + Independent Review B findings trên baseline v0.1.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.3-C bounded correction — P03C-MAJ-01/P03C-B-MAJ-01/P03C-B-MAJ-02/P03C-MIN-01/P03C-MIN-02/P03C-MIN-03." Đóng đúng một finding Major (ChatGPT) + hai finding Major (Independent Review B, subsumed vào cùng traceability overhaul) + ba finding Minor. Authorization này **không** cho phép sửa `product-requirement.md`/`use-case-workflow.md`/Domain Contract/Constitution/ADR/architecture, tạo `PR-XXX`/`UC-XXX` mới, invent routing implementation/permission architecture/route guard/authorization middleware/session token, invent organization/strategy-administration behavior, đóng OQ-002/OQ-003, authorize Live, hay Approve/Lock/Consolidate bất kỳ artifact nào.

### Baseline and blob verification

```text
Expected HEAD:  acca42fe78f890f3b4b22d4c20f67e07d3f0c883
Actual HEAD:    acca42fe78f890f3b4b22d4c20f67e07d3f0c883  — match

ux-blueprint.md:          v0.1 Draft, blob ebe052c397a64b670791cc21c3f446050588e6f0  — match
product/README.md:        blob 1d8861c58b09d5da0c18be567d5cc525644421c0  — match
product-requirement.md:   v0.2 Draft, blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8  — match, Consolidated Stable
use-case-workflow.md:     v0.3 Draft, blob affbb723b577cde4c8627dd689550e3bfbffb5d1  — match, Consolidated Stable
```

### Finding-by-finding resolution

| Finding | Resolution |
|---|---|
| `P03C-MAJ-01` | Mọi `WS`/`NAV`/`SCR`/`VIEW`/`FLOW`/`STATE` stable ID nay trace TRỰC TIẾP một hoặc nhiều `UC-XXX` VÀ một hoặc nhiều `PR-XXX` tường minh — KHÔNG còn "cross-cutting"/"mọi UC"/"inferred through the applicable screen"/"see child screen mapping" không liệt kê ID. WS-001 (§5) viết lại thành bảng bounded per-item (Account/Instrument-Venue/Strategy Instance context, lifecycle-stage nav bar, evidence/authority labels, historical cursor, blocked-state presentation, Live Unauthorized) — mỗi item cite UC/PR riêng, KHÔNG "sở hữu toàn bộ workflow behavior". Mọi `FLOW-001`–`FLOW-006` (§8) thêm field `UC traceability`/`PR traceability` riêng biệt, phủ mọi transition/guard vật chất. Mọi `STATE-001`–`STATE-027` (§11) thêm cột `UC traceability` trực tiếp; hai state presentation-generic (`STATE-001` loading/`STATE-002` empty) liệt kê ĐẦY ĐỦ UC/screen/PR áp dụng thay vì wording "cross-cutting". SCR-006 bổ sung `PR-001`(Strategy Instance precondition)/`PR-006`(Risk Gateway reason) — trước chỉ `PR-007`/`PR-024`. SCR-007 bổ sung `PR-013`(lossless financial precision, khớp panel Fill economics byte-for-byte) — trước chỉ `PR-007`/`PR-024`/`PR-025`/`PR-026`/`PR-027`. §14 rebuilt hoàn toàn thành bảy ma trận direct bắt buộc: WS→UC/PR, NAV→UC/PR, SCR/VIEW→UC/PR, FLOW→UC/PR, STATE→UC/PR, UC→UX artifacts, PR→UX artifacts — mọi `UC-001`–`UC-021` và `PR-001`–`PR-034` xác nhận xuất hiện trực tiếp (script-verified, không ID nào thiếu). |
| `P03C-B-MAJ-01` | Subsumed vào cùng traceability overhaul của `P03C-MAJ-01` — Independent Review B's finding trùng lặp yêu cầu direct UC/PR traceability cho mọi WS/NAV/FLOW/STATE artifact; resolve đầy đủ bởi cùng bộ thay đổi §5/§8/§11/§14 nêu trên. |
| `P03C-B-MAJ-02` | Subsumed vào cùng traceability overhaul của `P03C-MAJ-01` — Independent Review B's finding thứ hai (thiếu ma trận PR→UX artifact hoàn chỉnh và thiếu bounded WS-001 mapping) resolve bởi §14g (PR → UX artifacts, mới) và §5 WS-001 bounded per-item table. |
| `P03C-MIN-03` | Thêm §5a — sáu đặc tả `NAV-001`–`NAV-006` first-class, mỗi đặc tả đủ 11 field bắt buộc (Stable ID/Name/Purpose/Destination/Required context/Available navigation behavior/Read-only inspection behavior/Blocked behavior/UC traceability/PR traceability/Out-of-scope boundary). Research (NAV-001): quan sát market-analysis KHÔNG cần Strategy Instance trước. Replay/Backtest (NAV-002/003): Strategy Instance bắt buộc trước khi reconstruction/run bắt đầu; khi thiếu, hai khả năng UX hợp lệ (blocked/prompt HOẶC redirect tới VIEW-001) — KHÔNG invent routing implementation. Paper (NAV-004): read-only inspection luôn khả dụng; initiation chặn khi thiếu MỘT trong ba điều kiện (Strategy Instance pinned, PAPER-context Decision lineage eligible, Account/Instrument/Venue hợp lệ). Review (NAV-005): empty destination hiển thị được mà KHÔNG bịa evidence. Improve (NAV-006): KHÔNG organization/strategy-administration behavior nào được giới thiệu. |
| `P03C-MIN-01` | Sửa `FLOW-001` (§8) và §4 Information Architecture: quan sát market-analysis tại `SCR-001` KHÔNG còn phụ thuộc `VIEW-001` (chọn Strategy Instance) — `SCR-001` là entry-first của `NAV-001`. `VIEW-001` → `VIEW-002` (Research Verification, trước đây HOÀN TOÀN THIẾU khỏi FLOW-001) nay là commit-gate tường minh, CHỈ bắt buộc TRƯỚC khi chuyển sang `SCR-002`(Replay)/`SCR-003`(Backtest), khớp đúng UC-001 (quan sát)/UC-002 (chọn khi chuẩn bị Replay/Backtest)/UC-003 (verify khi kết thúc/chuyển tiếp). `FLOW-006` (Improve→Research loop-back) viết lại đồng nhất cùng nguyên tắc. Early optional Strategy selection vẫn khả dụng, KHÔNG còn represented như mandatory default entry path. |
| `P03C-MIN-02` | Thêm `UX-P-5` (§3) — phân tách tường minh read-only inspection navigation (luôn khả dụng để xem evidence/context/empty/blocked state đã tồn tại, kể cả khi upstream guard chưa thoả) vs. authoritative progression/action (luôn bị chặn khi upstream verification/required-authority guard chưa thoả). Áp dụng tường minh cho Research verification (VIEW-002, UC-003): PASSED cho phép tiến; FAILED/INDETERMINATE KHÔNG coi verified thành công, reason/evidence vẫn hiển thị, downstream authoritative action (tạo Backtest run, khởi tạo PAPER execution) bị chặn, nhưng navigation read-only vẫn khả dụng. Tường minh KHÔNG định nghĩa permission architecture/route guard/authorization middleware/session token. |

### Exact changed-file scope

```text
docs/product/ux-blueprint.md         MODIFIED v0.1 → v0.2   blob 1d5fd9d2e2bd7b6e9c88353e193cd1230b6cd6a3
docs/product/README.md               MODIFIED v0.8 → v0.9   blob 20f407773d6a4db08a51f36067844ea1f5d8a4ae
docs/MANIFEST.md                     MODIFIED manifest_version 9.87 → 9.88
docs/CHANGELOG.md                    MODIFIED (this entry)
docs/product/product-requirement.md  KHÔNG ĐỔI — blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8, verified byte-identical
docs/product/use-case-workflow.md    KHÔNG ĐỔI — blob affbb723b577cde4c8627dd689550e3bfbffb5d1, verified byte-identical
docs/domain/                          KHÔNG ĐỔI
docs/adr/                             KHÔNG ĐỔI
docs/constitution/                    KHÔNG ĐỔI
docs/architecture/                    KHÔNG ĐỔI
```

### Corrected artifact version and status

`ux-blueprint.md`: `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`.

### Stable ID counts and ranges (unchanged)

`WS-001` (1); `NAV-001`–`NAV-006` (6); `SCR-001`–`SCR-011` (11); `VIEW-001`–`VIEW-005` (5); `FLOW-001`–`FLOW-006` (6); `STATE-001`–`STATE-027` (27) — no ID renumbered, added, or removed; correction is bounded to content within existing IDs plus new §5a NAV specifications (reusing existing NAV-001–006 IDs already declared at §4/§6).

### Traceability completeness (script-verified)

Regex/set-comparison script confirmed: every `WS`/`NAV`/`SCR`/`VIEW`/`FLOW`/`STATE` ID has a non-empty direct `UC traceability` and `PR traceability`; `UC-001`–`UC-021` (all 21) and `PR-001`–`PR-034` (all 34) each appear in at least one direct artifact mapping; no forbidden indirect wording ("cross-cutting" alone/"mọi UC" without ID list/"see child screen mapping") remains outside the two explicitly-bounded generic states (`STATE-001`/`STATE-002`, which enumerate full ID sets directly per the task's own exception clause).

### Research journey ordering fix

`FLOW-001`/`FLOW-006`/§4 diagram: `SCR-001` (market-analysis observation) no longer requires `VIEW-001` (Strategy Instance selection) as an entry precondition — `VIEW-001 → VIEW-002` is a commit-gate positioned only before `SCR-002`/`SCR-003`, consistent with `UC-001` (no precondition) / `UC-002` (selection required only when preparing Replay/Backtest) / `UC-003` (verification at session end or before onward transition). `VIEW-002`, previously entirely absent from `FLOW-001`, is now explicit.

### Read-only inspection vs. authoritative progression

New `UX-P-5` (§3) pins the global distinction and ties it explicitly to Research verification's three outcomes (`VIEW-002`/`STATE-022`/`STATE-023`/`STATE-024`) — no permission architecture, route guard, authorization middleware, or session token defined; both are UX-only presentation/behavior distinctions.

### Forbidden-scope verification

No `PR-XXX`/`UC-XXX` created; `product-requirement.md`/`use-case-workflow.md` untouched (verified via `git diff --stat` and `git hash-object`, byte-identical); no Domain Contract/Constitution/ADR/architecture artifact modified; no routing implementation/permission architecture/route guard/authorization middleware/session token invented; no organization/strategy-administration behavior invented; no `BacktestOrder`/`BacktestFill`/`BacktestPosition`/`BacktestExecutionResult`/`ReplayDecision`/`ResearchVerification` invented (confirmed appearing only inside prohibition/boundary text); OQ-002/OQ-003 not closed; Live not authorized; no artifact Approved/Locked; Package 0.3-C not marked `Consolidated Stable`.

### Author self-review

Automated checks: `WS`(1)/`NAV`(6)/`SCR`(11)/`VIEW`(5)/`FLOW`(6)/`STATE`(27) all unique and sequentially contiguous within namespace, unchanged; all `UC-001`–`UC-021` and `PR-001`–`PR-034` present (full range, script-verified via regex extraction + range expansion); markdown table column-count consistency verified across all tables (no malformed row); forbidden domain-entity names confirmed appearing only inside prohibition/boundary text; YAML frontmatter re-validated via `yaml.safe_load` (`version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`); `git status --porcelain`/`git diff --stat` confirm only `docs/product/ux-blueprint.md` changed in the working tree prior to staging README/MANIFEST/CHANGELOG, and `product-requirement.md`/`use-case-workflow.md`/all Domain Contracts/ADRs/Constitution chapters/architecture artifacts remain byte-identical.

### Metadata / state

- `ux-blueprint.md`: **v0.1 → v0.2**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `product-requirement.md`/`use-case-workflow.md`: **không đổi** — byte-for-byte, `Consolidated Stable` package states unchanged.
- `product/README.md`: **v0.8 → v0.9**.
- `MANIFEST.md`: `manifest_version` **9.87 → 9.88**.
- Mọi Domain Contract, ADR, Constitution chapter, architecture artifact: **không đổi.**

**Package 0.3-C VẪN CHƯA đạt `Consolidated Stable` — chờ ChatGPT Delta Review A + Independent Delta Review B trên cùng exact baseline correction này.** Mandatory sequence tiếp tục: ChatGPT delta review → Independent Review B delta review → Product Owner consolidation decision. KHÔNG correction thêm dựa trên một review đơn lẻ. `OQ-002`/`OQ-003` vẫn `Open`. Không authorize Live. Không artifact nào Approved hay Locked. Phase 0.3 vẫn active — Phase 0 vẫn active và chưa hoàn tất; Phase 1 vẫn unauthorized.

## [Unreleased] — 2026-08-02 — author Package 0.3-C UX Blueprint baseline

**Package 0.3-C — UX Blueprint v0.1 authored.** Vai trò: `Domain Contract Author · AI Technical Architect`. Authorized artifacts: `docs/product/ux-blueprint.md` (new, v0.1 Draft), `docs/product/README.md` (updated). Authorization này **không** cho phép tạo `PR-XXX`/`UC-XXX` mới, sửa Package 0.3-A/0.3-B, redefine Domain Contract states/authority/cardinality/transitions, invent Backtest/Replay/Research domain entities/events, invent PAPER Decision establishment semantics, create unified Backtest/PAPER outcome model, define automatic normalization/scoring/ranking, define production API/database/software/security/custody/deployment architecture, define retention/archive/storage architecture, define visual branding/pixel styling, author implementation code, close OQ-002/OQ-003, authorize Live, Approve/Lock any artifact, mark Package 0.3-C Consolidated Stable, or declare Phase 0.3/Phase 0/Phase 1 complete or authorized.

### Baseline and upstream-blob verification

```text
Expected HEAD:  97f85dcdc5366060fdbc2e8b8bfda79482bbcb5d
Actual HEAD:    97f85dcdc5366060fdbc2e8b8bfda79482bbcb5d  — match

product-requirement.md:  v0.2 Draft, blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8  — match, Consolidated Stable
use-case-workflow.md:    v0.3 Draft, blob affbb723b577cde4c8627dd689550e3bfbffb5d1  — match, Consolidated Stable
```

### Controlling sources

`product-requirement.md` v0.2 (Package 0.3-A, `Consolidated Stable`, 34 requirements `PR-001`–`PR-034`) and `use-case-workflow.md` v0.3 (Package 0.3-B, `Consolidated Stable`, 21 Use Cases `UC-001`–`UC-021`) — sole authoritative sources; no Domain Contract, Constitution, or ADR consulted beyond what these two already cite.

### Document structure

18 mandatory sections present: (1) purpose/authority boundary, (2) actor/operating context, (3) UX principles/invariants, (4) information architecture, (5) global workspace/navigation model, (6) screen/view catalogue, (7) detailed screen/view specifications, (8) lifecycle stage flows, (9) cross-screen/cross-stage handoffs, (10) evidence/authority presentation model, (11) loading/empty/unavailable/blocked/failed/NON_EVALUABLE states, (12) historical cursor/correction UX, (13) strategy-version comparison UX, (14) traceability matrices, (15) deferred dependencies/Open Questions, (16) Non-Goals/Out-of-Scope, (17) acceptance criteria, (18) Phase 1 handoff requirements.

### Stable ID counts and ranges

`WS-001` (1); `NAV-001`–`NAV-006` (6); `SCR-001`–`SCR-011` (11); `VIEW-001`–`VIEW-005` (5); `FLOW-001`–`FLOW-006` (6); `STATE-001`–`STATE-027` (27) — all unique, sequential, contiguous within namespace. 16 total screen/view artifacts (11 `SCR` + 5 `VIEW`) cover all 21 Use Cases with no excessive decorative IDs.

### Screen/view catalogue summary

Research: SCR-001, VIEW-001, VIEW-002. Replay: SCR-002, VIEW-003. Backtest: SCR-003, SCR-004, SCR-005. Paper: SCR-006, SCR-007. Review: SCR-008, SCR-009, VIEW-004. Improve: SCR-010, SCR-011, VIEW-005.

### Coverage of UC-001–UC-021

Confirmed via §14a/§14c traceability matrices — every UC maps to exactly one primary UX artifact; UCs sharing a screen (SCR-004: UC-007/008/009; SCR-007: UC-012–015) each retain materially visible, separately described behavior within that screen's specification.

### Information architecture

Single workspace shell (WS-001) containing a global context bar (Account/Instrument-Venue/Strategy Instance/historical cursor) plus six lifecycle-stage navigation destinations (NAV-001–006), each containing its stage's screens/views — directly mirrors the six-stage lifecycle already Consolidated Stable, no additional stage introduced.

### Navigation/workspace model

Global navigation, current Account context (read-only, no switching UI), Instrument/Venue context, Strategy Instance context (pinned read-only per WF-INV-3/UX-INV-3), lifecycle-stage navigation, evidence/authority labels, historical cursor context, blocked/unavailable-state presentation — all defined at §5, matching the task's required minimum global workspace model exactly.

### Lifecycle-flow summary

Six FLOW artifacts: FLOW-001 (primary end-to-end journey), FLOW-002 (Strategy Instance selection/pin), FLOW-003 (Backtest→Paper handoff, judgment gate), FLOW-004 (Paper execution initiation, system-owned chain), FLOW-005 (old-version evidence access), FLOW-006 (Improve→Research loop-back).

### Replay authority UX

SCR-002 (historical reconstruction, default, authoritative recorded facts, no new Decision created) and VIEW-003 (parity recomputation, optional, deterministic, non-authoritative, canonical semantic-decision hash) kept visibly distinct throughout §7.2/§10; no `ReplayDecision`, no "Save recomputed Decision as authoritative"/"Replace recorded Decision"/"Promote parity result" action designed.

### Backtest authority UX

SCR-003/004/005 and VIEW-005's Backtest family visibly label mode=Backtest, authority=non-PAPER simulated, representation=product-required/domain-representation-deferred-where-applicable throughout; Backtest material never displayed as authoritative PAPER ExecutionResult/Fill/Position/submitted Order/exchange execution; no `BacktestOrder`/`BacktestFill`/`BacktestPosition`/`BacktestExecutionResult` invented.

### Paper user/system authority UX

SCR-006 frames the user action as "initiate/request PAPER execution" (intent only, no quantity/sizing/order-type/fee/slippage input); the full system-owned chain (PAPER-context Decision → Trade Intent → RiskEvaluation → Execution Intent → Order → OrderSubmissionRequest → ExecutionResultComputation → PaperExecutionObservation → ExecutionResult → Fill → Position) is explicitly system-owned; Risk APPROVED/REJECTED/NON_EVALUABLE outcomes represented per the required behavior.

### Cross-mode comparison UX

SCR-011 supports Backtest-vs-Backtest, PAPER-vs-PAPER, and cross-mode side-by-side (UC-020) with mode/authority/evidence-type/Strategy-Instance-identity/Strategy-Definition-Version-identity labels retained per evidence family; explicitly no unified outcome card, single normalized score, common execution result, authority-equivalent comparison, or automatic cross-mode ranking; OQ-003 remains Open.

### Research verification UX

VIEW-002 represents exactly three workflow-visible outcomes (PASSED/FAILED/INDETERMINATE, STATE-022/023/024); FAILED/INDETERMINATE never presented as successfully verified, reason and affected evidence disclosed, no downstream authoritative action; no `ResearchVerification` entity/event, no rollback/incident workflow invented.

### Old-version evidence UX

VIEW-005 resolves the Backtest family and PAPER family independently for an inactive Strategy Definition Version; identity always visible; partial unavailability marks only the affected family/type incomplete (STATE-026) without implying the entire history is unavailable; no retention/archival/retrieval/storage behavior defined.

### Unavailable/NON_EVALUABLE state handling

27 `STATE-XXX` entries (§11) cover every required minimum state including Position NON_EVALUABLE (STATE-021), Risk REJECTED/NON_EVALUABLE (STATE-013/014), and all Research/Backtest/PAPER/old-version unavailable states — all explicitly presentation-only (UX-INV-9), applying the four-principle fallback (workflow stops/state observable/reason disclosed/no downstream authoritative action) inherited from `use-case-workflow.md` §8.

### Historical cursor/correction UX

§12 represents canonical Replay Cursor, effective historical context, recorded-facts-available boundary, no-look-ahead boundary, and corrections-recorded-after-the-cursor distinctly; VIEW-004 always shows the original fact alongside any replacement fact with explicit `supersedes_fact_ref` lineage — never a silent replacement.

### Traceability matrices

§14 includes all seven required matrices: Workspace/Screen/View→UC, →PR, UC→Workspace/Screen/View, Lifecycle Stage→Screens/Views, State→UC/PR, Screen/View→Domain vocabulary, Deferred dependency→affected screens/views. Every `UC-001`–`UC-021` confirmed appearing in exactly one primary UX artifact.

### Deferred dependencies

§15 preserves, without solving: Backtest domain representation (deferred), Research domain representation (no standalone entity required), PAPER-context authoritative Decision establishment mechanism (deferred), OQ-002 (Open), OQ-003 (Open) — each with affected screens, what UX may display now, what UX must not invent, and what blocks later implementation.

### Forbidden-scope verification

No new `PR-XXX`/`UC-XXX` created; Package 0.3-A/0.3-B untouched (verified via `git diff --stat`); no Domain Contract state/authority/cardinality/transition redefined; no Backtest/Replay/Research domain entities invented; no unified Backtest/PAPER outcome model; no automatic normalization/scoring/ranking; no production API/database/software/security/custody/deployment architecture; no retention/archive/storage architecture; no visual branding/pixel styling/implementation code; OQ-002/OQ-003 not closed; Live not authorized; no artifact Approved/Locked; Package 0.3-C not marked Consolidated Stable; Phase 0.3/Phase 0/Phase 1 not declared complete or authorized.

### Author self-review

Automated checks: `WS`(1)/`NAV`(6)/`SCR`(11)/`VIEW`(5)/`FLOW`(6)/`STATE`(27) all unique and sequentially contiguous within namespace (caught and fixed one stray `SCR-015` reference in §11/§15 that had no corresponding screen definition — corrected to reference only defined IDs); all `UC-001`–`UC-021` referenced (21 distinct, full range); all `PR-XXX` references resolve within `PR-001`–`PR-034`; forbidden domain-entity names (`BacktestOrder`/`BacktestFill`/`BacktestPosition`/`BacktestExecutionResult`/`ReplayDecision`/`ResearchVerification`) confirmed appearing only inside prohibition/boundary text; no forbidden pixel/branding/API/database/CSS terms found outside prohibition context; YAML frontmatter re-validated via `yaml.safe_load`; `git diff --stat` confirms `product-requirement.md`, `use-case-workflow.md`, all Domain Contracts, ADRs, Constitution chapters, and architecture artifacts remain byte-identical.

### Changed-file scope

```text
docs/product/ux-blueprint.md         MỚI    v0.1 Draft   blob ebe052c397a64b670791cc21c3f446050588e6f0
docs/product/README.md               MODIFIED v0.7 → v0.8   blob 1d8861c58b09d5da0c18be567d5cc525644421c0
docs/MANIFEST.md                     MODIFIED manifest_version 9.86 → 9.87
docs/CHANGELOG.md                    MODIFIED (this entry)
docs/product/product-requirement.md  KHÔNG ĐỔI — blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8, verified byte-identical
docs/product/use-case-workflow.md    KHÔNG ĐỔI — blob affbb723b577cde4c8627dd689550e3bfbffb5d1, verified byte-identical
docs/domain/                          KHÔNG ĐỔI
docs/adr/                             KHÔNG ĐỔI
docs/constitution/                    KHÔNG ĐỔI
docs/architecture/                    KHÔNG ĐỔI
```

### Metadata / state

- `ux-blueprint.md`: **MỚI**, `version: "0.1"`, `status: Draft`, `approved_by: null`, `approved_at: null`.
- `product-requirement.md`/`use-case-workflow.md`: **không đổi** — byte-for-byte, `Consolidated Stable` package states unchanged.
- `product/README.md`: **v0.7 → v0.8**.
- `MANIFEST.md`: `manifest_version` **9.86 → 9.87**.
- Mọi Domain Contract, ADR, Constitution chapter, architecture artifact: **không đổi.**

**Package 0.3-C CHƯA đạt `Consolidated Stable` — chờ ChatGPT Review A + Independent Review B trên cùng exact baseline này.** Mandatory sequence: Author baseline → ChatGPT Review A → Independent Review B (cùng exact baseline) → merge finding → correction commit nếu cần → delta review → Product Owner consolidation decision. Package 0.2-A/B/C và 0.3-A/0.3-B vẫn `Consolidated Stable`, không đổi. `OQ-002`/`OQ-003` vẫn `Open`. Không authorize Live. Không artifact nào Approved/Locked. Phase 0.3 vẫn active — Phase 0 vẫn active và chưa hoàn tất; Phase 1 vẫn unauthorized.

## [Unreleased] — 2026-08-02 — consolidate Package 0.3-B

**Package 0.3-B Use Case & Workflow consolidated as `Consolidated Stable`.** Vai trò: `Package Lifecycle Consolidation Author · Repository Transaction Executor`. Product Owner authorized: "Package 0.3-B — Use Case & Workflow: Consolidated Stable" (2026-08-02). Authorization này cho phép ghi Package 0.3-B vào lifecycle state `Consolidated Stable` — nó KHÔNG cho phép Approve/Lock `use-case-workflow.md`, không đổi status khỏi Draft, không populate `approved_by`/`approved_at`, không authorize Package 0.3-C, không tuyên bố Phase 0.3 hoàn thành, không đóng OQ-002/OQ-003, không authorize Live, không sửa product semantics/Domain Contract/ADR/Constitution/architecture nào.

### Baseline verification

```text
Expected HEAD:  73b100f9854864f53bc7c4f86261db9c2aab8e0c
Actual HEAD:    73b100f9854864f53bc7c4f86261db9c2aab8e0c  — match

use-case-workflow.md:  v0.3 Draft, blob affbb723b577cde4c8627dd689550e3bfbffb5d1  — match
```

### Product Owner authorization recorded

```text
Package 0.3-B — Use Case & Workflow:
  Consolidated Stable
```

Meaning: the exact reviewed 0.3-B baseline is stable enough to serve as the dependency baseline for Package 0.3-C (UX Blueprint). It does not mean the artifact is Approved or Locked.

### Exact reviewed baseline pinned

```text
Consolidated baseline HEAD:  73b100f9854864f53bc7c4f86261db9c2aab8e0c

use-case-workflow.md:  v0.3 Draft, blob affbb723b577cde4c8627dd689550e3bfbffb5d1
```

### Review evidence

```text
ChatGPT second Delta Review A:        Clean — Blocker 0, Major 0, Minor 0
Independent second Delta Review B:    Clean — Blocker 0, Major 0, Minor 0
```

### Complete finding ledger — all resolved (v0.1 → v0.2 bounded correction, v0.2 → v0.3 narrow delta correction)

```text
P03B-MAJ-01:        Resolved (Backtest→Paper handoff + UC-011 — distinct PAPER-context Decision lineage)
P03B-MAJ-02:        Resolved (UC-020 separates Backtest non-PAPER authority from PAPER authoritative)
P03B-MIN-01:        Resolved (UC-011 reframed "Initiate PAPER execution")
P03B-MIN-02:        Resolved (UC-021 bounded alternate/failure for unavailable evidence)
P03B-MIN-03:        Resolved (UC-007 removed deletion-lifecycle language)
P03B-MIN-04:        Resolved (UC-020 restored PR-031/PR-032 traceability)
P03B-MIN-05:        Resolved (UC-003 observable PASSED/FAILED/INDETERMINATE outcomes)
P03B-DELTA-MIN-01:  Resolved (UC-021 rewritten to independently resolve both Backtest and PAPER
                     old-version evidence families; UC-020 updated to match)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

### Package lifecycle meaning

`Consolidated Stable` là package lifecycle/readiness state — nghĩa là: reviewed package baseline nội bộ coherent qua ba vòng correction; mọi qualifying finding đã resolved; package đủ ổn định để làm dependency baseline cho Package 0.3-C. Nó KHÔNG có nghĩa: artifact Approved; artifact Locked; status đổi khỏi Draft; Package 0.3-C tự động authorize; OQ closure; Phase 0.3 completion; Live authorization.

### Confirmation — `use-case-workflow.md` byte-identical

```text
docs/product/use-case-workflow.md   blob affbb723b577cde4c8627dd689550e3bfbffb5d1 — verified byte-identical to reviewed baseline
```

### Confirmation — Product Requirement/Domain Contract/ADR/Constitution/architecture unchanged

```text
docs/product/product-requirement.md   KHÔNG ĐỔI — verified via git diff --stat, empty
docs/domain/                           KHÔNG ĐỔI — verified via git diff --stat, empty
docs/adr/                              KHÔNG ĐỔI — verified via git diff --stat, empty
docs/constitution/                     KHÔNG ĐỔI — verified via git diff --stat, empty
docs/architecture/                     KHÔNG ĐỔI — verified via git diff --stat, empty
```

### Unchanged artifact statuses

`use-case-workflow.md`: **giữ nguyên** `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte — không sửa product semantic trong transaction này.

### Package lifecycle states pinned

```text
Package 0.3-A:    Consolidated Stable
Package 0.3-B:    Consolidated Stable
Package 0.3-C:    Unauthorized
```

### Artifact lifecycle states pinned

```text
use-case-workflow.md:  Draft, version "0.3", approved_by: null, approved_at: null, not Locked
```

### Changed-file scope

```text
docs/product/README.md               MODIFIED v0.6 → v0.7   blob 1b82af211f7bdd2df6142a030229a5efe16be769
docs/MANIFEST.md                     MODIFIED manifest_version 9.85 → 9.86
docs/CHANGELOG.md                    MODIFIED (this entry)
docs/product/use-case-workflow.md    KHÔNG ĐỔI — blob affbb723b577cde4c8627dd689550e3bfbffb5d1, verified byte-identical
docs/product/product-requirement.md  KHÔNG ĐỔI
docs/domain/                          KHÔNG ĐỔI
docs/adr/                             KHÔNG ĐỔI
docs/constitution/                    KHÔNG ĐỔI
docs/architecture/                    KHÔNG ĐỔI
```

### Metadata / state

- `use-case-workflow.md`: **không đổi** (semantic và version) — package lifecycle metadata only.
- `product/README.md`: **v0.6 → v0.7**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.85 → 9.86**; dòng `product/` cập nhật ghi nhận Package 0.3-B `Consolidated Stable`.
- Mọi Domain Contract, ADR, Constitution chapter, architecture artifact: **không đổi.**

**Package 0.3-C baseline dependency đã thỏa (0.3-B `Consolidated Stable`), eligible cho Product Owner scope authorization — CHƯA bắt đầu, CHƯA author, KHÔNG được authorize bởi transaction này.** OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.3 vẫn active. Phase 0 vẫn active và chưa hoàn tất; Phase 1 vẫn unauthorized.

## [Unreleased] — 2026-08-02 — complete old-version evidence workflow

**Package 0.3-B narrow delta correction — one consolidated finding.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.3-B narrow delta correction — P03B-DELTA-MIN-01." Đóng đúng một finding Minor. Authorization này **không** cho phép thêm/renumber Use Case, sửa Product Requirement/Domain Contract/Constitution/ADR, tạo unified Backtest/PAPER evidence entity/schema, tạo old-version evidence aggregate, tạo `BacktestOrder`/`BacktestExecutionResult`/`BacktestFill`/`BacktestPosition`, coi Backtest output là PAPER authority, redefine PAPER C7 entities/transitions, định nghĩa retention/archive/retrieval/restoration/storage architecture, định nghĩa evidence availability SLA, định nghĩa API/database/backend/frontend/infrastructure, author Package 0.3-C screens/components, đóng OQ-002/OQ-003, authorize Live, hay Approve/Lock/Consolidate bất kỳ artifact nào.

### Baseline and blob verification

```text
Expected HEAD:  243c966991052cbe3efc5acabb62626a3ad0b1b0
Actual HEAD:    243c966991052cbe3efc5acabb62626a3ad0b1b0  — match

use-case-workflow.md:    v0.2 Draft, blob 9c855f03a49b887e3ad9825ca65ee76b2884efef  — match
product/README.md:       v0.5 Draft, blob 097518c680f36704e7b1dca1655214991bfbdc60  — match
product-requirement.md:  v0.2 Draft, blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8  — match
```

### `P03B-DELTA-MIN-01` resolution

UC-021 previously operationalized only historical Decision facts, despite its broader Goal and UC-020's dependency on it for both Backtest and PAPER old-version evidence. Rewrote UC-021 in full to resolve, independently and mode-separated, both evidence families for an inactive Strategy Definition Version: the Backtest family (Decision/RiskEvaluation trace, simulated economic evidence, exposure/position progression, strategy-level evaluable result, run identity/version/configuration context — non-PAPER authority) and the PAPER family (Decision, Trade Intent, RiskEvaluation, Execution Intent, Order, OrderSubmissionRequest, ExecutionResult, Fill, Position — authoritative, with ExecutionResultComputation/PaperExecutionObservation as supporting evidence only, semantics unchanged). Version identity always remains visible; missing evidence is identified per family/type rather than implying the entire history is unavailable; available evidence is marked incomplete rather than presented as complete. UC-020 updated to consume this mode-separated scope without implying UC-021 produces a common cross-mode evidence object.

### Exact changed-file scope

```text
docs/product/use-case-workflow.md    MODIFIED v0.2 → v0.3   blob affbb723b577cde4c8627dd689550e3bfbffb5d1
docs/product/README.md               MODIFIED v0.5 → v0.6   blob 9e69e5fa98afda60592c376fe1a341007d267c0b
docs/MANIFEST.md                     MODIFIED manifest_version 9.84 → 9.85
docs/CHANGELOG.md                    MODIFIED (this entry)
docs/product/product-requirement.md  KHÔNG ĐỔI — blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8, verified byte-identical
docs/domain/                          KHÔNG ĐỔI
docs/adr/                             KHÔNG ĐỔI
docs/constitution/                    KHÔNG ĐỔI
docs/architecture/                    KHÔNG ĐỔI
```

### Corrected artifact version/status

`use-case-workflow.md`: `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null`.

### Use Case count and ID range

21, `UC-001`–`UC-021` — unchanged, no Use Case added or renumbered; the finding expressed entirely as bounded edits to UC-021 (full rewrite) and UC-020 (consistency edits), plus the failure table, vocabulary mapping, acceptance criteria, and Package 0.3-C handoff wording.

### UC-021 common identity behavior

Strategy Definition Version identity always remains visible, even when inactive and even when part of the evidence is unavailable — stated explicitly in Goal, Main flow step 1, and Alternate/failure.

### UC-021 Backtest evidence coverage

Decision/RiskEvaluation trace, simulated economic evidence, exposure/position progression, strategy-level evaluable result, run identity/version/configuration context — explicitly non-PAPER authority; explicitly never called an authoritative ExecutionResult/Fill/Position/PAPER execution outcome.

### UC-021 PAPER evidence coverage

Decision, Trade Intent, RiskEvaluation, Execution Intent, Order, OrderSubmissionRequest, ExecutionResult, Fill, Position — authoritative, preserving PAPER authority, causation lineage, Fill economics from PaperExecutionObservation, Position from eligible Fill lineage, and NON_EVALUABLE visibility; ExecutionResultComputation/PaperExecutionObservation included only as supporting evidence, semantics unchanged.

### Unavailable/partial evidence behavior

When any requested evidence cannot be resolved, the workflow stops only for the affected request; version identity, mode, and authority remain visible; other available evidence remains visible but is marked incomplete; the missing family/type is identified; reason is disclosed; nothing is fabricated or silently omitted; no partial conclusion is presented as complete; explicitly does not imply the entire Strategy history is unavailable from one missing family/type.

### UC-020 consistency

Main flow step 5, Evidence consumed, and Out-of-scope boundary updated to state UC-021 resolves each mode/family independently and does not return a common cross-mode evidence object; all three comparison modes (Backtest-vs-Backtest, PAPER-vs-PAPER, cross-mode side-by-side) and all mode/authority/evidence-type labeling requirements preserved unchanged.

### PR and Domain-vocabulary traceability

UC-021 now materially traces `PR-032` (unchanged ID, expanded material coverage). Domain vocabulary mapping (§9c) gives UC-021 its own row: `strategy.md`, `decision.md`, `risk.md` (Backtest family, evidence-source vocabulary only) plus `trade-intent.md`, `execution-intent.md`, `order.md`, `execution-result.md`, `fill.md`, `position.md` (PAPER family, authoritative) — two families kept explicitly separate.

### Preservation of all prior corrections

All seven v0.2 findings (`P03B-MAJ-01`, `P03B-MAJ-02`, `P03B-MIN-01`–`P03B-MIN-05`) remain resolved and unchanged: Backtest/Research Decision identity never enters PAPER ancestry; PAPER entry requires a distinct eligible PAPER-context Decision lineage; UC-011 frames user intent with system-owned Order/OrderSubmissionRequest; UC-020's Backtest/PAPER evidence families remain separate; UC-003 retains PASSED/FAILED/INDETERMINATE; UC-007 retains no deletion-lifecycle implication; Replay/Backtest/Paper authority boundaries unchanged.

### Forbidden-scope verification

No Use Case added or renumbered; no Product Requirement/Domain Contract/Constitution/ADR modified (verified via `git diff --stat`); no unified Backtest/PAPER evidence entity or old-version evidence aggregate created; no `BacktestOrder`/`BacktestExecutionResult`/`BacktestFill`/`BacktestPosition`; Backtest output never treated as PAPER authority; no PAPER C7 entity/transition redefined; no retention/archive/retrieval/restoration/storage architecture; no evidence availability SLA; no API/database/infrastructure defined; no Package 0.3-C content authored; OQ-002/OQ-003 not closed; Live not authorized; no artifact Approved/Locked; Package 0.3-B not marked Consolidated Stable.

### Author self-review

Automated re-verification: 21 unique/sequential UC-IDs unchanged (`UC-001`–`UC-021`); all 21 blocks retain all 13 required fields; all PR references resolve within `PR-001`–`PR-034`; UC-021 confirmed containing both "Backtest evidence family"/"họ evidence Backtest" and "PAPER evidence family"/"họ evidence PAPER" markers; forbidden Backtest entity names and `ReplayDecision` confirmed appearing only inside prohibition/boundary text across all occurrences; both YAML frontmatters re-validated via `yaml.safe_load`; `git diff --stat` confirms `product-requirement.md`, all Domain Contracts, ADRs, Constitution chapters, and architecture artifacts remain byte-identical.

### Backward Consistency Check

No conflict with `product-requirement.md` v0.2 (`Consolidated Stable`, unchanged), Package 0.2-A/B/C Domain Contracts (unchanged, all `Consolidated Stable`), Constitution Chapters 1/2/4, ADR-007 (all unchanged, byte-identical).

### Metadata / state

- `use-case-workflow.md`: **v0.2 → v0.3**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `product-requirement.md`: **không đổi** — byte-for-byte, `Consolidated Stable` package state unchanged.
- `product/README.md`: **v0.5 → v0.6**.
- `MANIFEST.md`: `manifest_version` **9.84 → 9.85**.
- Mọi Domain Contract, ADR, Constitution chapter, architecture artifact: **không đổi.**

**Package 0.3-B VẪN CHƯA đạt `Consolidated Stable` — chờ ChatGPT Delta Review A + Independent Delta Review B trên cùng exact baseline correction này.** Mandatory sequence tiếp tục: ChatGPT delta review → Independent Review B delta review → Product Owner consolidation decision. KHÔNG correction thêm dựa trên một review đơn lẻ. Package 0.3-C vẫn `Unauthorized`. `OQ-002`/`OQ-003` vẫn `Open`. Không authorize Live. Không artifact nào Approved hay Locked. Phase 0.3 vẫn active — Phase 0 vẫn active và chưa hoàn tất; Phase 1 vẫn unauthorized.

## [Unreleased] — 2026-08-02 — correct Package 0.3-B review findings

**Package 0.3-B bounded correction — consolidated Review A + Independent Review B findings.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.3-B bounded correction — P03B-MAJ-01/P03B-MAJ-02/P03B-MIN-01..05." Đóng đúng hai finding Major và năm finding Minor. Authorization này **không** cho phép sửa Product Requirement/Domain Contract/Constitution/ADR, invent PAPER Decision-generation semantics, clone/promote Backtest Decision vào PAPER authority, invent unified Backtest/PAPER outcome entity, invent cross-mode normalization/scoring, tạo `BacktestOrder`/`BacktestExecutionResult`/`BacktestFill`/`BacktestPosition`, tạo `ReplayDecision`/Replay authority stream, định nghĩa retention/archival/retrieval/storage architecture, định nghĩa Research verification domain entity/event, author Package 0.3-C, định nghĩa architecture/fee/PnL semantics, đóng OQ-002/OQ-003, authorize Live, hay Approve/Lock/Consolidate bất kỳ artifact nào.

### Baseline and blob verification

```text
Expected HEAD:  8dc5459c3f44264f419840ad0764c3e3d40a623d
Actual HEAD:    8dc5459c3f44264f419840ad0764c3e3d40a623d  — match

use-case-workflow.md:    v0.1 Draft, blob e2a66f7aff521801fbd6f9e0dfed6f59cb517493  — match
product/README.md:       v0.4 Draft, blob 3b6f5e6d42ac27e8c8159bacfe20c015a601f6cd  — match
product-requirement.md:  v0.2 Draft, blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8  — match
```

### Finding-by-finding resolution

| Finding | Resolution |
|---|---|
| `P03B-MAJ-01` | Rewrote the Backtest→Paper handoff (§7) and UC-011 in full: Backtest evidence informs user judgment only; Backtest/Research Decision identity is never carried forward, promoted, or reused as the authoritative PAPER Decision ancestor; PAPER entry requires a distinct PAPER-context authoritative Decision lineage; semantic parity may verify equivalence but never merges fact identity/authority. The exact PAPER-context Decision establishment mechanism is stated as a deferred domain/workflow dependency (§9d), not invented. Workflow stops before PAPER execution when no eligible PAPER-context Decision lineage exists (new §8 row). |
| `P03B-MAJ-02` | Rewrote UC-020 in full: separates Backtest comparison (non-PAPER authority: Decision/RiskEvaluation trace, simulated economic evidence, exposure/position progression, strategy-level evaluable result) from PAPER comparison (authoritative Decision/RiskEvaluation/Order/ExecutionResult/Fill/Position). Cross-mode viewing is user-visible juxtaposition only — identities and authority remain distinct, no unified execution-outcome fact, no automatic normalization, no common scoring formula. Backtest material is never called an authoritative `ExecutionResult`/`Fill`/`Position`. |
| `P03B-MIN-01` | UC-011 reframed from "Submit a PAPER Order" to "Initiate PAPER execution" — user supplies intent only; Order/OrderSubmissionRequest remain explicitly system-owned authoritative facts; no user-owned quantity/order-type/sizing added. |
| `P03B-MIN-02` | UC-021 rewritten to remove the "durable append-only log guarantees access is always available" overclaim; added the exact bounded alternate/failure path (workflow stops, identity remains visible, unavailable evidence identified, reason disclosed, no fabrication, no silent omission, no conclusion presented as complete); Out-of-scope boundary now explicitly excludes retention duration/archive tiering/retrieval latency/restoration process/storage architecture. |
| `P03B-MIN-03` | UC-007's "run đã bị loại bỏ" (implied deletion lifecycle) replaced with "Backtest run identity does not resolve, hoặc run evidence hiện không khả dụng" plus the exact four-principle fallback; no run state machine or archival lifecycle defined. |
| `P03B-MIN-04` | UC-020's detailed block now material-traces both `PR-031` and `PR-032` — Main flow step 5 and Evidence consumed explicitly reflect PR-032's historical old-version evidence requirement (via UC-021), not merely a cosmetic citation. |
| `P03B-MIN-05` | UC-003 rewritten with observable PASSED/FAILED/INDETERMINATE verification outcomes; FAILED/INDETERMINATE stop the workflow from proceeding as successfully verified, with status/reason/affected-evidence disclosed; explicitly no `ResearchVerification` domain entity/event created. |

### Exact changed-file scope

```text
docs/product/use-case-workflow.md    MODIFIED v0.1 → v0.2   blob 9c855f03a49b887e3ad9825ca65ee76b2884efef
docs/product/README.md               MODIFIED v0.4 → v0.5   blob 097518c680f36704e7b1dca1655214991bfbdc60
docs/MANIFEST.md                     MODIFIED manifest_version 9.83 → 9.84
docs/CHANGELOG.md                    MODIFIED (this entry)
docs/product/product-requirement.md  KHÔNG ĐỔI — blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8, verified byte-identical
docs/domain/                          KHÔNG ĐỔI
docs/adr/                             KHÔNG ĐỔI
docs/constitution/                    KHÔNG ĐỔI
docs/architecture/                    KHÔNG ĐỔI
```

### Corrected artifact version and status

`use-case-workflow.md`: `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`.

### Use Case count and ID range

21, `UC-001`–`UC-021` — unchanged, no renumbering; all seven findings expressed as bounded edits to existing Use Cases (UC-003, UC-007, UC-011, UC-020, UC-021) plus the Backtest→Paper handoff, catalogue, stage/vocabulary mappings, failure table, acceptance criteria, and Package 0.3-C handoff requirements — no new UC-ID required.

### Backtest→Paper authority resolution

Backtest/Research Decision identity is never carried forward, promoted, or reused as PAPER Decision ancestry — stated explicitly in both the handoff (§7) and UC-011's Preconditions/Evidence consumed. Decision parity may verify semantic equivalence via the canonical semantic-decision hash but never merges fact identity or authority.

### PAPER-context Decision dependency handling

Stated as a deferred domain/workflow dependency (§9d, new paragraph) — the requirement (PAPER entry needs a distinct PAPER-context authoritative Decision lineage) and the boundary (never derived from Backtest/Research) are pinned; the exact establishment mechanism is explicitly not invented here.

### UC-011 user/system authority resolution

User supplies intent to initiate PAPER execution only; Decision (PAPER-context), Trade Intent, RiskEvaluation, Execution Intent, Order, and OrderSubmissionRequest remain entirely system-owned authoritative facts; no user-owned quantity/order-type/sizing semantics added.

### UC-020 mode-separated comparison behavior

Same-mode Backtest-vs-Backtest and PAPER-vs-PAPER comparisons remain available; cross-mode side-by-side inspection is permitted but must visibly label mode, authority, and evidence type per evidence family — no unified outcome, no normalization, no scoring formula.

### Research verification outcomes

UC-003 now returns exactly one of PASSED / FAILED / INDETERMINATE, workflow-visible only — no `ResearchVerification` entity or event created.

### Backtest unavailable-evidence behavior

UC-007: "Backtest run identity does not resolve" or "run evidence is currently unavailable" applies the standard four-principle fallback — no deletion event, run state machine, or archival lifecycle implied.

### Historical-evidence accessibility behavior

UC-021: old Strategy Definition Version identity always remains visible; evidence resolves when possible; when it cannot, the workflow stops with the identified-unavailable-evidence/reason-disclosed/no-fabrication/no-silent-omission/no-complete-conclusion path — no retention/archival/retrieval/storage architecture defined.

### PR traceability correction

UC-020's detailed block cites `PR-031` and `PR-032` (was `PR-031` only); catalogue (§5), stage mapping (§9b), and vocabulary mapping (§9c) already listed both PR-031/PR-032 and Backtest/PAPER-split vocabulary respectively — vocabulary mapping updated to split UC-020 out from the UC-019/UC-021 grouping to reflect its two distinct evidence families.

### Preserved Replay behavior

UC-004/UC-005 and the Replay authority boundary unchanged: historical reconstruction by default, optional non-authoritative parity recomputation, canonical semantic-decision hash, no duplicate Decision, no Replay authority stream, no `ReplayDecision`.

### Preserved Backtest behavior

UC-006/UC-008/UC-009/UC-010 and the Backtest authority boundary unchanged: bounded run identity, Decision/RiskEvaluation trace, simulated economic evidence, exposure/position progression, strategy-level evaluable result, no PAPER-fact reuse, no Backtest domain-fact invention.

### Preserved Paper/C7 behavior

UC-012–UC-015 unchanged: exact C7 chain, Risk authority preserved, Fill economics from PaperExecutionObservation, Position derived from eligible Fill lineage with NON_EVALUABLE disclosure, no real exchange order.

### Forbidden-scope verification

No Product Requirement/Domain Contract/Constitution/ADR modified (verified via `git diff --stat`); no PAPER Decision-generation semantics invented; no Backtest Decision cloned/promoted into PAPER authority; no unified Backtest/PAPER outcome entity/schema; no cross-mode normalization/ranking/scoring; no `BacktestOrder`/`BacktestExecutionResult`/`BacktestFill`/`BacktestPosition`; no `ReplayDecision`/Replay authority stream; no retention/archival/retrieval/storage architecture; no Research verification domain entity/event; no Package 0.3-C content authored; no API/database/infrastructure architecture; no fee/slippage/accounting/PnL/settlement/attribution semantics; OQ-002/OQ-003 not closed; Live not authorized; no artifact Approved/Locked; Package 0.3-B not marked Consolidated Stable.

### Author self-review

Automated re-verification: 21 unique/sequential UC-IDs unchanged (`UC-001`–`UC-021`, no renumbering); all 21 blocks retain all 13 required fields; all PR references resolve within `PR-001`–`PR-034`; UC-020 detailed block confirmed citing both `PR-031` and `PR-032`; forbidden Backtest entity names and `ReplayDecision` confirmed appearing only inside prohibition/boundary text (10 occurrences, all verified in context); the one remaining occurrence of "đã bị loại bỏ" confirmed to be inside the v0.2 correction-summary meta-description (explaining what was removed), not operative UC-007 text; zero occurrences of the old absolute-accessibility claim; both YAML frontmatters re-validated via `yaml.safe_load`; `git diff --stat` confirms `product-requirement.md`, all Domain Contracts, ADRs, Constitution chapters, and architecture artifacts remain byte-identical.

### Backward Consistency Check

No conflict with `product-requirement.md` v0.2 (`Consolidated Stable`, unchanged), Package 0.2-A/B/C Domain Contracts (unchanged, all `Consolidated Stable`), Constitution Chapters 1/2/4, ADR-007 (all unchanged, byte-identical).

### Metadata / state

- `use-case-workflow.md`: **v0.1 → v0.2**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `product-requirement.md`: **không đổi** — byte-for-byte, `Consolidated Stable` package state unchanged.
- `product/README.md`: **v0.4 → v0.5**.
- `MANIFEST.md`: `manifest_version` **9.83 → 9.84**.
- Mọi Domain Contract, ADR, Constitution chapter, architecture artifact: **không đổi.**

**Package 0.3-B VẪN CHƯA đạt `Consolidated Stable` — chờ ChatGPT Delta Review A + Independent Delta Review B trên cùng exact baseline correction này.** Mandatory sequence tiếp tục: ChatGPT delta review → Independent Review B delta review → Product Owner consolidation decision. KHÔNG correction thêm dựa trên một review đơn lẻ. Package 0.3-C vẫn `Unauthorized`. `OQ-002`/`OQ-003` vẫn `Open`. Không authorize Live. Không artifact nào Approved hay Locked. Phase 0.3 vẫn active — Phase 0 vẫn active và chưa hoàn tất; Phase 1 vẫn unauthorized.

## [Unreleased] — 2026-08-02 — author Package 0.3-B use-case workflow baseline

**Package 0.3-B — Use Case & Workflow v0.1 authored.** Vai trò: `Domain Contract Author · AI Technical Architect`. Authorized artifacts: `docs/product/use-case-workflow.md` (new, v0.1 Draft), `docs/product/README.md` (updated). Authorization này **không** cho phép tạo/sửa product requirement, sửa Package 0.3-A (`product-requirement.md`), author Package 0.3-C screen flows/layouts/wireframes, tạo Domain Contract mới, redefine Domain Contract states/transitions, invent Backtest/Replay domain facts, tái sử dụng PAPER fact làm Backtest authority, định nghĩa UX component/API/database/backend/frontend/infrastructure/security/custody/deployment architecture, định nghĩa Product Metric threshold, định nghĩa Live-gate criteria, mở rộng multi-tenant/multi-asset scope, Approve/Lock bất kỳ artifact nào, hay mark Package 0.3-B Consolidated Stable.

### Baseline and upstream-blob verification

```text
Expected HEAD:  08bbc397dafa5f34ea7dec89dbb17a297f7c7502
Actual HEAD:    08bbc397dafa5f34ea7dec89dbb17a297f7c7502  — match

product-requirement.md:  v0.2 Draft, blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8  — match
Package 0.3-A: Consolidated Stable — match
```

### Controlling sources

`product-requirement.md` v0.2 Draft (Package 0.3-A, `Consolidated Stable`, 34 requirements `PR-001`–`PR-034`) — sole authoritative source for all workflow behavior; no Domain Contract, Constitution chapter, or ADR consulted beyond what `product-requirement.md` already cites (vocabulary reused verbatim, not re-derived).

### Document structure

13 mandatory sections present: (1) purpose/authority boundary, (2) actors/operating context, (3) workflow-wide invariants, (4) primary end-to-end journey, (5) Use Case catalogue, (6) detailed Use Cases, (7) cross-stage handoffs, (8) failure/non-evaluable paths, (9) evidence/traceability requirements (four sub-mappings), (10) deferred questions, (11) Non-Goals/Out-of-Scope, (12) acceptance criteria Package 0.3-B, (13) handoff requirements Package 0.3-C.

### Use Case count and ID range

21 Use Cases, `UC-001`–`UC-021`, unique and sequential — 3 Research, 2 Replay, 5 Backtest, 5 Paper, 3 Review, 3 Improve, covering every bullet in the task's minimum coverage list.

### Primary journey summary

Research (select Strategy Instance, inspect market state, no side-effect) → Replay (canonical cursor, historical reconstruction, optional parity recomputation) → Backtest (bounded run, Decision/RiskEvaluation trace, simulated economic evidence/exposure progression, strategy-level evaluable result, cross-run comparison) → Paper (full C7 chain to ExecutionResult/Fill/Position, PAPER-only) → Review (causation trace, reconstructed-vs-recorded comparison, correction inspection) → Improve (new Strategy Definition Version, cross-version comparison, old-version evidence preserved) → loops back to Research.

### PR traceability approach

Every Use Case's "PR traceability" field cites one or more existing `PR-XXX`; §9a/§9b provide a full Use Case→PR and Stage→PR mapping; no new product requirement created; every workflow step in every Main flow is grounded in an already-`Consolidated Stable` requirement.

### Domain vocabulary mapping approach

§9c maps every Use Case to the exact Domain Contract file(s) it consumes (candle.md…replay-event.md, strategy.md, account.md, instrument.md, venue.md) — vocabulary reused verbatim from `product-requirement.md`, no redefinition.

### Replay authority handling

UC-004/UC-005 and the inherited Replay authority boundary (product-requirement.md §9.2) preserved verbatim: historical reconstruction (default, no computation) distinct from parity recomputation (optional, non-authoritative, uses `canonical semantic-decision hash`); no duplicate Decision fact; no parallel Replay authority stream; no mutation of recorded Decisions; no `ReplayDecision` created or named.

### Backtest authority handling

UC-006–UC-010 and the inherited Backtest authority boundary (product-requirement.md §9.3) preserved verbatim: Backtest must not create or reuse PAPER Order/ExecutionResult/Fill/Position or Live facts as Backtest authority; no `BacktestOrder`/`BacktestFill`/`BacktestPosition`/`BacktestExecutionResult` invented; no simulation/fee/slippage/accounting/PnL model defined; steps lacking domain representation (UC-008/UC-009) explicitly labeled "product-required, domain-representation deferred."

### Paper/C7 consistency

UC-011–UC-015 use the exact chain: Decision → Trade Intent → RiskEvaluation → Execution Intent → Order → OrderSubmissionRequest → ExecutionResultComputation → PaperExecutionObservation → ExecutionResult → Fill → Position. Fill economics sourced from PaperExecutionObservation (UC-013); Position derived from eligible Fill lineage with explicit NON_EVALUABLE disclosure (UC-014); Paper never places a real exchange order (UC-015).

### Failure and non-evaluable handling

§8 covers all 13 required scenarios (missing Strategy Instance, invalid Instrument/Venue, missing historical evidence, unavailable Replay cursor references, parity mismatch, insufficient Backtest evidence, RiskEvaluation REJECTED/NON_EVALUABLE, Order NOT_EXECUTED, Fill absent, Position NON_EVALUABLE, correction visible after historical cursor, attempted Live use). Where no controlling behavior exists in the PRD, applies exactly the four-line fallback (workflow stops / state remains observable / reason is disclosed / no downstream authoritative action) rather than inventing resolution semantics.

### Deferred-domain dependencies

§9d states explicitly: no Backtest or Research Domain Contract exists; UC-006–UC-010 (Backtest) and UC-001–UC-003 (Research) describe product-required behavior without assuming any such Domain Contract or entity exists.

### Explicit scope exclusions

Screen layout/wireframe/component hierarchy (deferred to Package 0.3-C); Domain Contract semantics/state machines; Backtest/Replay domain facts; PAPER-fact reuse as Backtest authority; API/database/backend/frontend/infrastructure/security/custody/deployment architecture; Product Metric thresholds; Live-gate criteria; multi-tenant/multi-asset expansion; new product requirements.

### Author self-review

Automated checks: 21 unique/sequential UC-IDs (`UC-001`–`UC-021`); all 21 blocks retain all 13 required fields (Title/Primary actor/Goal/Trigger/Preconditions/Inputs/Main flow/Alternate-or-failure/Observable outcome/Evidence produced-or-consumed/PR traceability/Domain vocabulary used/Out-of-scope boundary); all PR-XXX references resolve within the existing `PR-001`–`PR-034` range; forbidden Backtest entity names and `ReplayDecision` appear only inside prohibition/boundary text; bare "Decision hash" appears only inside the explicit prohibition sentence (WF-INV-5); zero vague terms outside citation; both YAML frontmatters re-validated via `yaml.safe_load`; `git diff --stat` confirms `product-requirement.md`, all Domain Contracts, ADRs, Constitution chapters, and architecture artifacts remain byte-identical.

### Changed-file scope

```text
docs/product/use-case-workflow.md    MỚI    v0.1 Draft   blob e2a66f7aff521801fbd6f9e0dfed6f59cb517493
docs/product/README.md               MODIFIED v0.3 → v0.4   blob 3b6f5e6d42ac27e8c8159bacfe20c015a601f6cd
docs/MANIFEST.md                     MODIFIED manifest_version 9.82 → 9.83
docs/CHANGELOG.md                    MODIFIED (this entry)
docs/product/product-requirement.md  KHÔNG ĐỔI — blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8, verified byte-identical
docs/domain/                          KHÔNG ĐỔI
docs/adr/                             KHÔNG ĐỔI
docs/constitution/                    KHÔNG ĐỔI
docs/architecture/                    KHÔNG ĐỔI
```

### Metadata / state

- `use-case-workflow.md`: **MỚI**, `version: "0.1"`, `status: Draft`, `approved_by: null`, `approved_at: null`.
- `product-requirement.md`: **không đổi** — byte-for-byte, `Consolidated Stable` package state unchanged.
- `product/README.md`: **v0.3 → v0.4**.
- `MANIFEST.md`: `manifest_version` **9.82 → 9.83**.
- Mọi Domain Contract, ADR, Constitution chapter, architecture artifact: **không đổi.**

**Package 0.3-B CHƯA đạt `Consolidated Stable` — chờ ChatGPT Review A + Independent Review B trên cùng exact baseline này.** Mandatory sequence: Author baseline → ChatGPT Review A → Independent Review B (cùng exact baseline) → merge finding → correction commit nếu cần → delta review → Product Owner consolidation decision. Package 0.3-C **chưa author, chưa authorize** — phụ thuộc 0.3-B `Consolidated Stable` (chưa thỏa). Package 0.2-A/B/C và 0.3-A vẫn `Consolidated Stable`, không đổi. `OQ-002`/`OQ-003` vẫn `Open`. Không authorize Live. Không artifact nào Approved/Locked. Phase 0.3 vẫn active — Phase 0 vẫn active và chưa hoàn tất; Phase 1 vẫn unauthorized.

## [Unreleased] — 2026-08-01 — consolidate Package 0.3-A

**Package 0.3-A Product Requirement consolidated as `Consolidated Stable`.** Vai trò: `Package Lifecycle Consolidation Author · Repository Transaction Executor`. Product Owner authorized: "Package 0.3-A — Product Requirement: Consolidated Stable" (2026-08-01). Authorization này cho phép ghi Package 0.3-A vào lifecycle state `Consolidated Stable` — nó KHÔNG cho phép Approve/Lock `product-requirement.md`, không đổi status khỏi Draft, không populate `approved_by`/`approved_at`, không authorize Package 0.3-B, không tuyên bố Phase 0.3 hoàn thành, không đóng OQ-002/OQ-003, không authorize Live, không sửa product semantics/Domain Contract/ADR/Constitution/architecture nào.

### Baseline verification

```text
Expected HEAD:  a8e39c92a73ba05b9f9a196bd75e4ea4037cb285
Actual HEAD:    a8e39c92a73ba05b9f9a196bd75e4ea4037cb285  — match

product-requirement.md:  v0.2 Draft, blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8  — match
```

### Product Owner authorization recorded

```text
Package 0.3-A — Product Requirement:
  Consolidated Stable
```

Meaning: the exact reviewed 0.3-A baseline is stable enough to serve as the dependency baseline for Package 0.3-B (Use Case & Workflow). It does not mean the artifact is Approved or Locked.

### Exact reviewed baseline pinned

```text
Consolidated baseline HEAD:  a8e39c92a73ba05b9f9a196bd75e4ea4037cb285

product-requirement.md:  v0.2 Draft, blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8
```

### Review evidence

```text
ChatGPT Delta Review A:        Clean — Blocker 0, Major 0, Minor 0
Independent Delta Review B:    Clean — Blocker 0, Major 0, Minor 0
```

### Complete finding ledger — all resolved (v0.1 → v0.2 bounded correction)

```text
P03A-MAJ-01:      Resolved (PR-033/PR-034 — Backtest simulated economic evidence/exposure progression/
                   strategy-level evaluable result, Backtest authority boundary)
P03A-MIN-01:      Resolved ("Decision hash" replaced with canonical semantic-decision hash, PR-010/PR-019)
P03A-MIN-02:      Resolved ("exactly one source" rule replaced with "one or more applicable sources")
P03A-B-MIN-03:    Resolved (PR-019 splits historical reconstruction / parity recomputation, Replay
                   authority boundary)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

### Package lifecycle meaning

`Consolidated Stable` là package lifecycle/readiness state — nghĩa là: reviewed package baseline nội bộ coherent; mọi qualifying finding đã resolved; package đủ ổn định để làm dependency baseline cho Package 0.3-B. Nó KHÔNG có nghĩa: artifact Approved; artifact Locked; status đổi khỏi Draft; Package 0.3-B tự động authorize; OQ closure; Phase 0.3 completion; Live authorization.

### Confirmation — `product-requirement.md` byte-identical

```text
docs/product/product-requirement.md   blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8 — verified byte-identical to reviewed baseline
```

### Confirmation — Domain Contract/ADR/Constitution/architecture unchanged

```text
docs/domain/           KHÔNG ĐỔI — verified via git diff --stat, empty
docs/adr/               KHÔNG ĐỔI — verified via git diff --stat, empty
docs/constitution/      KHÔNG ĐỔI — verified via git diff --stat, empty
docs/architecture/      KHÔNG ĐỔI — verified via git diff --stat, empty
```

### Unchanged artifact statuses

`product-requirement.md`: **giữ nguyên** `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte — không sửa product semantic trong transaction này.

### Package lifecycle states pinned

```text
Package 0.3-A:    Consolidated Stable
Package 0.3-B:    Unauthorized
Package 0.3-C:    Unauthorized
```

### Artifact lifecycle states pinned

```text
product-requirement.md:  Draft, version "0.2", approved_by: null, approved_at: null, not Locked
```

### Changed-file scope

```text
docs/product/README.md               MODIFIED v0.2 → v0.3   blob 4b2b1df9fcb5bf684acf0eb1e0bfbbfefd0dbadc
docs/MANIFEST.md                     MODIFIED manifest_version 9.81 → 9.82
docs/CHANGELOG.md                    MODIFIED (this entry)
docs/product/product-requirement.md  KHÔNG ĐỔI — blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8, verified byte-identical
docs/domain/                          KHÔNG ĐỔI
docs/adr/                             KHÔNG ĐỔI
docs/constitution/                    KHÔNG ĐỔI
docs/architecture/                    KHÔNG ĐỔI
```

### Metadata / state

- `product-requirement.md`: **không đổi** (semantic và version) — package lifecycle metadata only.
- `product/README.md`: **v0.2 → v0.3**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.81 → 9.82**; dòng `product/` cập nhật ghi nhận Package 0.3-A `Consolidated Stable`.
- Mọi Domain Contract, ADR, Constitution chapter, architecture artifact: **không đổi.**

**Package 0.3-B baseline dependency đã thỏa (0.3-A `Consolidated Stable`), eligible cho Product Owner scope authorization — CHƯA bắt đầu, CHƯA author, KHÔNG được authorize bởi transaction này.** OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.3 vẫn active. Phase 0 vẫn active và chưa hoàn tất; Phase 1 vẫn unauthorized.

## [Unreleased] — 2026-08-01 — correct Package 0.3-A review findings

**Package 0.3-A bounded correction — consolidated Review A + Independent Review B findings.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.3-A bounded correction — P03A-MAJ-01/P03A-MIN-01/P03A-MIN-02/P03A-B-MIN-03." Đóng đúng một finding Major và ba finding Minor. Authorization này **không** cho phép author Backtest Domain Contract/entity/event/state machine/schema, tái sử dụng PAPER fact làm Backtest authority, định nghĩa simulation/fee/slippage/latency/liquidity/partial-fill semantics, accounting/PnL/ledger/settlement/performance-attribution, sửa Decision canonical field/hashing rule, sửa Domain Contract, tạo Replay authority stream hay `ReplayDecision`, author Package 0.3-B/0.3-C, định nghĩa architecture/API/database/deployment, đóng OQ-002/OQ-003, authorize Live, mark Package 0.3-A Consolidated Stable, hay Approve/Lock bất kỳ artifact nào.

### Baseline verification

```text
Expected HEAD:  e2f9b24d47d2e4b2457d984c0b73ee7ff421887d
Actual HEAD:    e2f9b24d47d2e4b2457d984c0b73ee7ff421887d  — match

product-requirement.md:  v0.1 Draft, blob 985c942668b85d0e5ecb6f735ea30d570636d0c9  — match
README.md (product):     v0.1 Draft, blob af4ab4d65c5d470f4947c25a9fcc5bed00bc75ec  — match
```

### Finding-by-finding resolution

| Finding | Resolution |
|---|---|
| `P03A-MAJ-01` | Added `PR-033` (Backtest simulated economic evidence + exposure/position progression) and `PR-034` (strategy-level evaluable result, cross-run/cross-version comparison) — new IDs, appended after `PR-023`, no renumbering. `PR-021` updated to require stable Backtest run identity/context. Added explicit **Backtest authority boundary** (§9.3): Backtest must not create/reuse PAPER Order/ExecutionResult/Fill/Position or Live execution facts as Backtest authority; defers exact Backtest Domain Contract/event schema; explicitly prohibits inventing `BacktestOrder`/`BacktestFill`/`BacktestPosition`/`BacktestExecutionResult` or equivalents; explicitly prohibits defining execution/fee/slippage/accounting/PnL models. |
| `P03A-MIN-01` | Replaced generic "Decision hash" with `canonical semantic-decision hash` in `PR-010`/`PR-019` and their acceptance evidence. Added a defining note (after `PR-010`) clarifying the hash is defined by the authoritative Decision Contract, excludes runtime identity/event-envelope/transport/processing metadata — without hardcoding the canonical field list in the PRD. |
| `P03A-MIN-02` | Replaced the "resolve to exactly one source" rule (intro Authority boundary + §14 acceptance criterion 3) with: a PR must have one or more applicable authoritative sources, may combine Vision/Platform Invariant/Domain Contract, every cited source must materially support the requirement, no PR may be orphaned. Traceability table (§10) preserved, with one new row added for `PR-033`–`PR-034`. |
| `P03A-B-MIN-03` | Rewrote `PR-019` to distinguish historical reconstruction (default, resolves/displays existing authoritative facts at a canonical Replay Cursor) from parity recomputation (optional, deterministic, non-authoritative semantic verification using the canonical semantic-decision hash) from authoritative Decision creation (never implicitly caused by running Replay). Added explicit **Replay authority boundary** (§9.2): no duplicate authoritative Decision fact, no parallel Replay authority stream, no mutation of the recorded Decision, no-look-ahead/visibility-at-cursor preserved, no `ReplayDecision` created or named. |

### Exact changed-file scope

```text
docs/product/product-requirement.md  MODIFIED v0.1 → v0.2   blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8
docs/product/README.md               MODIFIED v0.1 → v0.2   blob 0426407cebbf2ef13497da4a45746984d5697dd4
docs/MANIFEST.md                     MODIFIED manifest_version 9.80 → 9.81
docs/CHANGELOG.md                    MODIFIED (this entry)
docs/domain/                          KHÔNG ĐỔI
docs/adr/                             KHÔNG ĐỔI
docs/constitution/                    KHÔNG ĐỔI
docs/architecture/                    KHÔNG ĐỔI
```

### Corrected PRD version and status

`product-requirement.md`: `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`.

### Requirement count and ID range

34 requirements, `PR-001`–`PR-034` — all pre-existing IDs preserved unchanged in place; `PR-033`/`PR-034` are the only new IDs, appended at the end of the global sequence (discussed within §9.3 Backtest); no unrelated requirement renumbered.

### Backtest outcome model at product level

Backtest must produce, per stable run identity: deterministic simulated economic evidence tied to each Decision-driven exposure change, exposure/position progression across the bounded interval, and a strategy-level evaluable result comparable across runs/Strategy Definition Versions — all without defining a concrete KPI target and without any Backtest Domain Contract/schema being authored here.

### Backtest/PAPER authority separation

Explicit boundary text states Backtest must not create or reuse PAPER Order/ExecutionResult/Fill/Position or Live execution facts as Backtest authority — Backtest evidence is a distinct, not-yet-modeled concept, referenced against the PAPER boundary only to state what it must NOT reuse.

### Canonical semantic-decision wording

"Decision hash" replaced with `canonical semantic-decision hash` throughout operative requirement text (`PR-010`, `PR-019`); defined as excluding runtime identity, event-envelope fields, transport metadata, and processing metadata, per the authoritative Decision Contract — field list not hardcoded in the PRD, mirroring I-2 Verification wording exactly.

### Replay authority clarification

`PR-019` and the new Replay authority boundary jointly state: historical reconstruction is the default (no computation, no new authoritative fact); parity recomputation is optional and non-authoritative; Replay never implicitly causes authoritative Decision creation; no duplicate Decision fact, no parallel authority stream, no mutation of the recorded Decision, no `ReplayDecision` created or named.

### Traceability correction

Intro Authority boundary and §14 acceptance criterion 3 rewritten per `P03A-MIN-02`. Traceability table (§10) preserved with one new row (`PR-033`–`PR-034`) added; no other row content changed.

### Preserved behavior

Internal team, single workspace, one Account currently operated (Account first-class/extensible), crypto-only, 2–3 exchanges; six-stage lifecycle (Research→Replay→Backtest→Paper→Review→Improve) unchanged; `OQ-002`/`OQ-003` remain `Open`; Live remains `Unauthorized`; Package 0.3-B/0.3-C remain `Unauthorized`; all C7 Paper execution/Fill/Position semantics (`PR-024`–`PR-027`) unchanged.

### Forbidden-scope verification

No Backtest Domain Contract/entity/event/schema authored; no PAPER-fact reuse as Backtest authority; no simulation/fee/slippage/accounting/PnL model defined; no Decision canonical field/hashing rule modified; zero Domain Contract/ADR/Constitution/architecture file touched (verified via `git diff --stat`); no Replay authority stream or `ReplayDecision` created; no Package 0.3-B/0.3-C content authored; `OQ-002`/`OQ-003` not closed; Live not authorized; Package 0.3-A not marked Consolidated Stable; no artifact Approved or Locked.

### Author self-review

Automated re-verification after edits: 34 unique/sequential-by-presence PR-IDs (`PR-001`–`PR-034`, `PR-033`/`PR-034` positioned within §9.3 text but numbered as the next available global IDs, per the "append at the end of the relevant range, do not renumber unrelated requirements" instruction); all 34 blocks retain all four fields; zero bare "Decision hash" occurrences inside operative requirement text (3 remaining occurrences are meta-commentary explicitly describing/prohibiting the old term, in the v0.2 correction summary and acceptance-criteria/handoff notes); zero "resolve to exactly one source" wording remaining; forbidden Backtest entity names and `ReplayDecision` appear only inside their respective prohibition/boundary text, never as if real; both YAML frontmatters re-validated via `yaml.safe_load`.

### Backward Consistency Check

No conflict with Constitution Chapters 1/2/4 (unchanged, byte-identical), ADR-007 (unchanged, byte-identical), Package 0.2-A/B/C Domain Contracts (unchanged, byte-identical, all `Consolidated Stable`).

### Metadata / state

- `product-requirement.md`/`README.md` (product): **v0.1 → v0.2**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `MANIFEST.md`: `manifest_version` **9.80 → 9.81**.
- Mọi Domain Contract, ADR, Constitution chapter, architecture artifact: **không đổi.**

**Package 0.3-A VẪN CHƯA đạt `Consolidated Stable` — chờ ChatGPT Delta Review A + Independent Delta Review B trên cùng exact baseline correction này.** Mandatory sequence tiếp tục: ChatGPT delta review → Independent Review B delta review → Product Owner consolidation decision. KHÔNG correction thêm dựa trên một review đơn lẻ. Package 0.3-B/0.3-C vẫn `Unauthorized`. `OQ-002`/`OQ-003` vẫn `Open`. Không authorize Live. Không artifact nào Approved hay Locked. Phase 0.3 vẫn active — Phase 0 vẫn active và chưa hoàn tất; Phase 1 vẫn unauthorized.

## [Unreleased] — 2026-07-31 — author Package 0.3-A product requirement baseline

**Package 0.3-A — Product Requirement v0.1 authored.** Vai trò: `Domain Contract Author · AI Technical Architect`. Authorized artifacts: `docs/product/README.md` (new, v0.1 Draft — Phase 0.3 product-artifact index), `docs/product/product-requirement.md` (new, v0.1 Draft). Authorization này **không** cho phép author screen layout/wireframe/component hierarchy/UX architecture, backend/frontend/API/database/security/custody/deployment architecture, exchange adapter design, concrete KPI/Product Metrics (`OQ-003`), Live-gate criteria (`OQ-002`), multi-tenant/multi-asset design, Domain Contract semantic mới, sửa C1–C7/ADR/Constitution, Approve/Lock bất kỳ artifact nào, hay mark Package 0.3-A Consolidated Stable.

### Baseline verification

```text
Expected HEAD:  bf91cae2685e4f14dda358fff6fee92b4b6cf8a7
Actual HEAD:    bf91cae2685e4f14dda358fff6fee92b4b6cf8a7  — match
```

### Controlling sources

Chapter 1 (Vision, Locked v2.3); Chapter 2 (Platform Invariants, Locked v3.1, I-1..I-13); Chapter 4 §4.5 (Domain Principles, Locked — Domain Modeling stable before UX Blueprint approved); ADR-007 (Locked — nội bộ, single-workspace, crypto-only, 2-3 sàn); toàn bộ 19 Domain Contract `Consolidated Stable` (Package 0.2-A/B/C, `/docs/domain/`); MANIFEST Open Questions (`OQ-002`/`OQ-003`).

### PRD structure

15 mục bắt buộc: (1) document purpose/authority boundary, (2) product problem, (3) target users, (4) user outcomes, (5) product principles kế thừa Vision, (6) product scope, (7) functional requirements (`PR-001`–`PR-008`), (8) non-functional requirements — restating existing Constitution/Domain Contract guarantee only (`PR-009`–`PR-014`), (9) lifecycle requirements theo sáu giai đoạn Research/Replay/Backtest/Paper/Review/Improve (`PR-015`–`PR-032`), (10) traceability table, (11) Non-Goals, (12) Out-of-Scope, (13) deferred questions (`OQ-002`/`OQ-003`), (14) acceptance criteria Package 0.3-A, (15) handoff requirements Package 0.3-B.

### Requirement count and ID range

32 requirement, `PR-001`–`PR-032`, liên tục, duy nhất, mỗi requirement có đủ bốn trường `Statement`/`Rationale`/`Source`/`Acceptance evidence` tách biệt.

### Traceability approach

Mỗi `PR-XXX` resolve về ĐÚNG MỘT hoặc nhiều trong ba nguồn: Vision section, Platform Invariant, hoặc Domain Contract `Consolidated Stable` — không có requirement không truy vết được. Non-functional requirements (`PR-009`–`PR-014`) restate guarantee ĐÃ Locked (I-1/I-2/I-3/I-5/I-9/I-13), không thêm yêu cầu mới.

### Deferred-question handling

`OQ-002` (Strategy Lifecycle Live-gate) và `OQ-003` (Product Metrics) giữ nguyên `Open` — PRD yêu cầu evidence đo lường được tồn tại (đúng nguyên tắc "Measurable") nhưng KHÔNG định nghĩa KPI threshold/target hay Live-gate criteria cụ thể. Ghi nhận thêm: chưa có Domain Contract riêng cho Backtest/Research — lifecycle requirement tại §9.1/§9.3 mô tả hành vi product-level, không giả định entity chưa tồn tại.

### Explicit scope exclusions

Screen layout/wireframe/component hierarchy/UX architecture; backend/frontend/API/database/security/custody/deployment architecture; exchange adapter design; concrete KPI/Product Metrics; Live-gate criteria; multi-tenant/multi-asset design; Domain Contract semantic mới.

### Author self-review

Kiểm tra tự động: 32 `PR-ID` duy nhất/liên tục (`PR-001`–`PR-032`); mọi block có đủ bốn trường tách biệt (phát hiện + sửa 6 block NFR ban đầu dùng nhãn gộp `Rationale/Source:` — tách thành hai dòng riêng để tuân thủ đúng format bắt buộc); quét thuật ngữ mơ hồ (easy to use/fast/scalable/secure/professional/user-friendly) — 0 xuất hiện ngoài chính đoạn liệt kê cấm dùng; quét thuật ngữ kiến trúc cấm (wireframe/component hierarchy/API contract/database schema/screen layout) — 0 xuất hiện ngoài out-of-scope section; YAML frontmatter cả hai file re-validated qua `yaml.safe_load`, 0 lỗi.

### Changed-file scope

```text
docs/product/README.md                MỚI    v0.1 Draft   blob af4ab4d65c5d470f4947c25a9fcc5bed00bc75ec
docs/product/product-requirement.md   MỚI    v0.1 Draft   blob 985c942668b85d0e5ecb6f735ea30d570636d0c9
docs/MANIFEST.md                      MODIFIED manifest_version 9.79 → 9.80 (thêm mục `## Product`)
docs/CHANGELOG.md                     MODIFIED (this entry)
docs/domain/                          KHÔNG ĐỔI — mọi Domain Contract byte-for-byte không đổi
docs/adr/                             KHÔNG ĐỔI
docs/constitution/                    KHÔNG ĐỔI
docs/architecture/                    KHÔNG ĐỔI
docs/team/                            KHÔNG ĐỔI
```

### Metadata / state

- `product/README.md`/`product-requirement.md`: **MỚI**, `version: "0.1"`, `status: Draft`, `approved_by: null`, `approved_at: null`.
- `MANIFEST.md`: `manifest_version` **9.79 → 9.80**; mục `## Product` mới thêm.
- Mọi Domain Contract, ADR, Constitution chapter, Team/Architecture/Research artifact: **không đổi.**

**Package 0.3-A CHƯA đạt `Consolidated Stable` — chờ ChatGPT Review A + Independent Review B trên cùng exact baseline này.** Mandatory sequence: Author baseline → ChatGPT Review A → Independent Review B (cùng exact baseline) → merge finding → correction commit nếu cần → delta review → Product Owner consolidation decision. Package 0.3-B/0.3-C **chưa author, chưa authorize** — phụ thuộc 0.3-A `Consolidated Stable`. Package 0.2-A/B/C vẫn `Consolidated Stable`, không đổi. `OQ-002`/`OQ-003` vẫn `Open`. Không authorize Live. Không artifact nào Approved/Locked. Phase 0.3 vẫn active — Phase 0 vẫn active và chưa hoàn tất; Phase 1 vẫn unauthorized.

## [Unreleased] — 2026-07-31 — complete Phase 0.2

**Product Owner decision recorded.** Vai trò: `Package Lifecycle Consolidation Author · Repository Transaction Executor`. Metadata-only transaction — no domain semantics changed.

```text
Baseline verification:
  Expected HEAD:  95fdb01ea662e741fa08f4c2d79727cc13c1a54a
  Actual HEAD:    95fdb01ea662e741fa08f4c2d79727cc13c1a54a  — match

Phase 0.2 — Domain Model & Domain Contract:
  Complete

Completed baseline:
  95fdb01ea662e741fa08f4c2d79727cc13c1a54a

Next active sub-phase:
  Phase 0.3

Phase 0:
  not Approved

Phase 1:
  not Authorized

Domain artifacts:
  remain Draft, not Approved, not Locked

OQ-002/OQ-003:
  remain Open

Live:
  remains Unauthorized
```

**Changed:** `docs/domain/README.md` (v0.52 → v0.53), `docs/MANIFEST.md` (manifest_version 9.78 → 9.79), `docs/CHANGELOG.md` (this entry). **Unchanged, byte-identical:** all 19 domain-concept files + `context-map.yaml`, all ADRs, all Constitution chapters, all governance artifacts. No artifact Approved or Locked; `approved_by`/`approved_at` not populated; OQ-002/OQ-003 not closed; Live not authorized; Phase 0 not declared complete; Phase 1 not authorized; no Phase 0.3 deliverable authored; no Phase 0 DoD created; no Phase 0 Approval Gate work performed.

## [Unreleased] — 2026-07-31 — consolidate Package 0.2-C7

**Package 0.2-C7 Execution Result, Fill, Position and Replay Integration Foundation consolidated as `Consolidated Stable`.** Vai trò: `Package Lifecycle Consolidation Author · Repository Transaction Executor`. Product Owner authorized: "Package 0.2-C7: Consolidated Stable" (2026-07-31). Authorization này cho phép ghi Package 0.2-C7 vào lifecycle state `Consolidated Stable` — nó KHÔNG cho phép Approve/Lock `execution-result.md`/`fill.md`/`position.md`/`replay-event.md`, không sửa `context-map.yaml`/bất kỳ C1–C6 artifact/ADR nào, không sửa Constitution, không đóng OQ-002/OQ-003, không authorize Live, không author/authorize package mới, không thêm speculative edge case, không tuyên bố Phase 0.2 hoàn thành.

### Baseline verification

```text
Expected HEAD:  c671b987aedc1f4ac9d74597a1c111ae0c98683e
Actual HEAD:    c671b987aedc1f4ac9d74597a1c111ae0c98683e  — match

execution-result.md:  v0.3 Draft, blob e5cbb0ee3e3b9083920c03318e3f0dd726247304  — match
fill.md:               v0.3 Draft, blob a4a2c473086ef8495c4106b75d632a7af09ae3fc  — match
position.md:            v0.3 Draft, blob 808a3e6041af7a5521094318924fa3682be9cefa  — match
replay-event.md:        v0.3 Draft, blob f429d31c0f8ec42e2859f5658edd8a3dedf58b64  — match
context-map.yaml:      v0.19 Draft  — match
```

### Product Owner authorization recorded

```text
Package 0.2-C7:
  Consolidated Stable
```

Meaning: the exact reviewed C7 baseline (all four artifacts, second bounded correction v0.3) is stable enough to be recorded as the completed dependency baseline for Package 0.2-C as a whole. It does not mean any artifact is Approved or Locked.

### Exact reviewed baseline pinned

```text
Package 0.2-C7 reviewed HEAD:  c671b987aedc1f4ac9d74597a1c111ae0c98683e

execution-result.md:  v0.3 Draft, blob e5cbb0ee3e3b9083920c03318e3f0dd726247304
fill.md:               v0.3 Draft, blob a4a2c473086ef8495c4106b75d632a7af09ae3fc
position.md:            v0.3 Draft, blob 808a3e6041af7a5521094318924fa3682be9cefa
replay-event.md:        v0.3 Draft, blob f429d31c0f8ec42e2859f5658edd8a3dedf58b64
Integration artifact:  context-map.yaml v0.19 Draft (unchanged)
Registry baseline:     MANIFEST v9.77
```

### Review evidence

```text
ChatGPT second bounded delta Review A:        Clean — Blocker 0, Major 0, Minor 0
Independent second bounded delta Review B:    Clean — Blocker 0, Major 0, Minor 0
```

### Complete finding ledger — all resolved (v0.1 → v0.2 bounded correction, v0.2 → v0.3 second bounded correction)

```text
C7-MAJ-01:        Resolved (PaperExecutionObservation entity, durable simulation evidence + output, corrected ordering, v0.2)
C7-MAJ-02:        Resolved (Fill economics required to copy exactly from Observation, v0.2)
C7-MAJ-03:        Resolved (eligible_as_position_contributing_fill continuing eligibility rule replaces "mandatory pairing" language, v0.2)
C7-MAJ-04:        Resolved (Position projection_status EVALUABLE/NON_EVALUABLE, UNSUPPORTED_MULTIPLE_FILL_LINEAGES, v0.2)
C7-DELTA-MAJ-01:  Resolved (ExecutionResultComputation entity, computation identity replaces cursor as authorization/idempotency anchor, v0.3)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

### Package lifecycle meaning

`Consolidated Stable` là package lifecycle/readiness state — nghĩa là: reviewed package baseline nội bộ coherent qua hai vòng correction; mọi qualifying finding đã resolved; deferred limitations được ghi nhận tường minh là non-blocking Phase 1 concern; package integration đủ ổn định để coi toàn bộ Package 0.2-C (C1–C7) hoàn tất tương đương. Nó KHÔNG có nghĩa: artifact Approved; artifact Locked; ADR thay đổi; Domain Contract bất biến; OQ closure; Phase completion; implementation authorization; Live authorization.

### Confirmation — C7 semantic artifacts byte-identical

```text
docs/domain/execution-result.md  blob e5cbb0ee3e3b9083920c03318e3f0dd726247304 — verified byte-identical to reviewed baseline
docs/domain/fill.md              blob a4a2c473086ef8495c4106b75d632a7af09ae3fc — verified byte-identical to reviewed baseline
docs/domain/position.md          blob 808a3e6041af7a5521094318924fa3682be9cefa — verified byte-identical to reviewed baseline
docs/domain/replay-event.md      blob f429d31c0f8ec42e2859f5658edd8a3dedf58b64 — verified byte-identical to reviewed baseline
docs/domain/context-map.yaml     unchanged — verified byte-identical to reviewed baseline
```

### Confirmation — C1–C6 semantic artifacts byte-identical

```text
docs/domain/order.md             blob 94ec87593834362292dc3379068e99ef12d86412 — verified byte-identical
docs/domain/risk.md              blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab — verified byte-identical
docs/domain/execution-intent.md  blob afc0c1fe7bdd2f285403dff29c71849ab66af70c — verified byte-identical
docs/domain/decision.md          blob e2a26320200d350ace3da0247235bb14cef12509 — verified byte-identical
docs/domain/trade-intent.md      blob e7a306abc53ba482ff1249af1dda2829c4c82fa7 — verified byte-identical
docs/domain/instrument.md        blob 81651f6a19a3f22fa7a924173f14b02e6467c8e0 — verified byte-identical
docs/domain/venue.md             blob 0ffb9e64bcb7dec108edea0bc9c3af3a162b40d9 — verified byte-identical
docs/domain/account.md           blob 9fd2d0fb3235343d52c3435df3f1c7e08dd22781 — verified byte-identical
docs/domain/strategy.md          blob c2cadc464bc8baecff41ff8079461ec0d5dfaccc — verified byte-identical
```

### Unchanged artifact statuses

`execution-result.md`/`fill.md`/`position.md`/`replay-event.md`: **giữ nguyên** `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte — không sửa Domain Contract semantic trong transaction này. `context-map.yaml`: **giữ nguyên** `version: "0.19"`, `status: Draft`, byte-for-byte — không sửa. `order.md`/`risk.md`/`execution-intent.md`/`decision.md`/`trade-intent.md`: **giữ nguyên**, byte-for-byte — không sửa. Mọi C1–C3 Domain Contract (`instrument.md`/`venue.md`/`account.md`/`strategy.md`) và mọi ADR: **giữ nguyên**, byte-for-byte — không sửa.

### Package lifecycle states pinned

```text
Package 0.2-C1:     Consolidated Stable
Package 0.2-C2:     Consolidated Stable
Package 0.2-C3:     Consolidated Stable
Package 0.2-C4:     Consolidated Stable
Package 0.2-C5:     Consolidated Stable
Package 0.2-C6:     Consolidated Stable
Package 0.2-C7:     Consolidated Stable
```

**Package 0.2-C (C1–C7, tổng thể) nay `Consolidated Stable`.**

### Artifact lifecycle states pinned

```text
execution-result.md:  Draft, version "0.3", approved_by: null, approved_at: null, not Locked
fill.md:               Draft, version "0.3", approved_by: null, approved_at: null, not Locked
position.md:            Draft, version "0.3", approved_by: null, approved_at: null, not Locked
replay-event.md:        Draft, version "0.3", approved_by: null, approved_at: null, not Locked
context-map.yaml:      Draft, version "0.19"
```

### Changed-file scope

```text
docs/domain/README.md            MODIFIED v0.51 → v0.52
docs/MANIFEST.md                 MODIFIED manifest_version 9.77 → 9.78
docs/CHANGELOG.md                MODIFIED (this entry)
docs/domain/execution-result.md  KHÔNG ĐỔI — blob e5cbb0ee3e3b9083920c03318e3f0dd726247304, verified byte-identical
docs/domain/fill.md              KHÔNG ĐỔI — blob a4a2c473086ef8495c4106b75d632a7af09ae3fc, verified byte-identical
docs/domain/position.md          KHÔNG ĐỔI — blob 808a3e6041af7a5521094318924fa3682be9cefa, verified byte-identical
docs/domain/replay-event.md      KHÔNG ĐỔI — blob f429d31c0f8ec42e2859f5658edd8a3dedf58b64, verified byte-identical
docs/domain/context-map.yaml     KHÔNG ĐỔI — verified byte-identical
docs/domain/order.md             KHÔNG ĐỔI — blob 94ec87593834362292dc3379068e99ef12d86412, verified byte-identical
docs/domain/risk.md              KHÔNG ĐỔI — blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab, verified byte-identical
docs/domain/execution-intent.md  KHÔNG ĐỔI — blob afc0c1fe7bdd2f285403dff29c71849ab66af70c, verified byte-identical
docs/domain/decision.md          KHÔNG ĐỔI — blob e2a26320200d350ace3da0247235bb14cef12509, verified byte-identical
docs/domain/trade-intent.md      KHÔNG ĐỔI — blob e7a306abc53ba482ff1249af1dda2829c4c82fa7, verified byte-identical
```

### Metadata / state

- `execution-result.md`, `fill.md`, `position.md`, `replay-event.md`, `context-map.yaml`, `order.md`, `risk.md`, `execution-intent.md`, `decision.md`, `trade-intent.md`: **không đổi** (semantic và version) — package lifecycle metadata only.
- `README.md` (domain index): **v0.51 → v0.52**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.77 → 9.78**; dòng `domain/` cập nhật ghi nhận Package 0.2-C7 `Consolidated Stable`.
- Mọi Domain Contract khác (`instrument.md`, `venue.md`, `account.md`, `strategy.md`, `candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, `context.md`), mọi ADR file, Constitution: **không đổi.**

**Package 0.2-C (C1–C7) nay hoàn tất `Consolidated Stable` toàn bộ.** OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Không artifact nào Approved/Locked. Phase 0.2 vẫn active và chưa hoàn tất — hoàn tất Phase 0.2 là một quyết định Product Owner riêng, tách biệt khỏi `Consolidated Stable`, chưa được đưa ra trong transaction này.

## [Unreleased] — 2026-07-31 — bind C7 observations to authorized computations

**Package 0.2-C7 second bounded correction — đúng một consolidated delta finding.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C7 second bounded correction — C7-DELTA-MAJ-01." Đóng đúng một finding: `C7-DELTA-MAJ-01` (logical computation key `(submission_request_id, observation_cursor)` không authoritatively phân biệt initial computation / authorized correction computation / illegal rerun tại cursor mới / orphan Observation chờ Attempt). Authorization này **không** cho phép sửa C1–C6 semantic artifacts, `order.md`, ADR/Constitution, author simulation algorithm thực tế, Live behavior, exchange adapter/API payload, partial Fill, fees/PnL/accounting, close/reduce/reversal, aggregation/netting, margin/leverage/liquidation, cross-stream transaction, workflow/saga infrastructure, reopen `C7-MAJ-02`/`C7-MAJ-03`/`C7-MAJ-04`, Approve/Lock artifact, mark C7 Consolidated Stable, đóng OQ-002/OQ-003, hay declare Phase 0.2 complete.

### Baseline verification

```text
Expected HEAD:  11dd3c0e5b1091f21e79ee5e1ba42e6e72d15026
Actual HEAD:    11dd3c0e5b1091f21e79ee5e1ba42e6e72d15026  — match

execution-result.md:  v0.2 Draft, blob 72011d38ca0e7ad78c09eed496242a164682abaf  — match
fill.md:               v0.2 Draft, blob d001e0371f02145e0973c6f3b808f62f3d6465f7  — match
position.md:            v0.2 Draft, blob 4eeb40603804c7baa4f4bc8b7a9f13cb94db6597  — match
replay-event.md:        v0.2 Draft, blob 36cf46b69be70f4238ded433ce3eda33a3a2e99e  — match
context-map.yaml:      v0.19 Draft  — match
```

### Finding resolution summary

`C7-DELTA-MAJ-01`: introduced `ExecutionResultComputation` (execution-result.md §2, new entity) as the authoritative identity for exactly one authorized Execution Result computation lifecycle. Computation identity — not cursor — now determines authorization and idempotency. `computation_purpose ∈ {INITIAL, CORRECTION}`. Cursor remains immutable computation context/replay evidence but no longer silently authorizes a new computation.

### ExecutionResultComputation model

New entity (execution-result.md §2). `execution_result_computation_id` — opaque, globally unique, immutable, assigned at `ExecutionResultComputationAuthorized` (execution-result.md §5, new event), never derived from `submission_request_id`/`order_id`/`computation_cursor`/predecessor Result. Minimum schema: `execution_result_computation_id`, `computation_purpose`, `order_id`, `submission_request_id`, `computation_cursor`, `predecessor_execution_result_ref` (CORRECTION-only), `correction_authorization_ref` (CORRECTION-only). Append-only, no correction lineage of its own — a correction uses a brand-new computation identity, never mutates an existing one.

### Initial computation cardinality

For `computation_purpose = INITIAL`: `submission_request_id` required; `predecessor_execution_result_ref`/`correction_authorization_ref` absent. At most **one** `ExecutionResultComputation(INITIAL)` per `submission_request_id`, ever — regardless of `computation_cursor`, simulation evidence, or process invocation. A retry for the same Submission Request reuses the existing initial computation identity; a different cursor never creates a second INITIAL computation — deterministic conflict (Scenario 32).

### Correction computation authorization

For `computation_purpose = CORRECTION`: `predecessor_execution_result_ref` and `correction_authorization_ref` both required. `correction_authorization_ref` must resolve to an `ExecutionResultFactInvalidated` targeting exactly `predecessor_execution_result_ref`, visible before the correction computation is recorded. Predecessor's `submission_request_id` must equal the computation's `submission_request_id`. At most **one** direct `ExecutionResultComputation(CORRECTION)` per invalidated predecessor `ExecutionResult` — a second correction targeting the same predecessor conflicts (fork prohibited, Scenario 36). Five explicit reject conditions (execution-result.md §11): missing/invalid invalidation reference, wrong target, changed `submission_request_id`, fork, non-current-lineage predecessor (Scenario 35).

### Computation event ordering and schema

Corrected sequence (execution-result.md §8a): `ExecutionResultComputationAuthorized` → bounded simulation computation completes → `PaperExecutionObservationRecorded` → `ExecutionResultProcessingAttemptRecorded`(PROCESSED) → `ExecutionResultRecorded`. "Authorized" means domain eligibility (INITIAL, `order.md` §8b) or correction lineage (CORRECTION) permitted the computation — not manual Product Owner authorization of each runtime computation. No workflow/saga/command infrastructure introduced — `ExecutionResultComputationAuthorized` is a domain authorization fact only.

### Observation binding and idempotency

`PaperExecutionObservation` (execution-result.md §1) gained required `execution_result_computation_id`. Logical/idempotency identity changed from `(submission_request_id, observation_cursor)` to `execution_result_computation_id` alone — one computation → zero or one Observation. Same computation + same cursor + same evidence/output → idempotent reuse; same computation + changed cursor → deterministic conflict (Scenario 33); same computation + changed evidence/output → deterministic conflict (Scenario 25/D). `Observation.order_id`/`submission_request_id`/`observation_cursor` must equal `Computation`'s corresponding fields. `PaperExecutionObservationRecorded`'s `causation_refs` must now contain the exact `ExecutionResultComputationAuthorized` fact (execution-result.md §6).

### Attempt binding

`ExecutionResultProcessingAttemptRecorded` (execution-result.md §7) gained conditional `execution_result_computation_id` (`execution_observation_id` unchanged, still conditional). Bounded three-way rule: `INELIGIBLE` — no computation, no observation (eligibility check failed before authorization ever happened); `FAILED_BEFORE_RESULT` — computation present (was authorized), observation absent (simulation failed before durable output); `PROCESSED` — both present, exact Observation already persisted.

### Result binding

`ExecutionResultRecorded` (execution-result.md §8) gained required `execution_result_computation_id`, required equal to Attempt's and Observation's — three-way equality. `result_type` continues to copy exactly from the referenced Observation (`C7-MAJ-01`, unchanged). Result logical lineage key **remains `submission_request_id`** — computation identity explains which authorized computation produced the fact, it does not replace the Result's own lineage key. Correction replacement's `execution_result_computation_id` must be a CORRECTION-purpose computation whose `predecessor_execution_result_ref` points to the exact predecessor being superseded.

### Corrected ordering (Gap A / Gap B recovery)

Gap A (computation authorized, Observation persisted, Attempt absent): recovery resolves the computation (`GetExecutionResultComputationById`), resolves its exactly-one Observation (`GetObservationForComputation`), appends/reuses Attempt, appends/reuses Result — never searches Observations by `submission_request_id` alone, never picks the newest Observation, never selects a different cursor, never reruns simulation, never creates a second Observation or a second INITIAL computation for the Submission Request (Scenario B, §19 execution-result.md).

### Gap A recovery

Test: K1 authorized → O1 persisted → crash before Attempt. Recovery resolves K1 → resolves exactly one O1 for K1 → appends/reuses Attempt for K1/O1 → appends/reuses exactly one Result for K1/O1 — verified against every prohibited shortcut listed in the task (search-by-submission-request-id-only, newest-Observation selection, cursor substitution, simulation rerun, duplicate Observation/computation creation).

### Gap B recovery

Test: K1 → O1 → A1 PROCESSED → crash before E1. Recovery reuses K1/O1/A1, appends/reuses exactly one E1 — no simulation rerun, no new Attempt identity (Scenario E, execution-result.md §19).

### Illegal rerun behavior

Test: INITIAL K1 exists (S1, C1); another process requests INITIAL computation (S1, C2). Rejected as duplicate INITIAL computation — no K2/O2/A2/E2 created even though C2/simulation refs/deterministic inputs/output all differ (Scenario 32/A, execution-result.md §19).

### Authorized correction behavior

E1 exists from K1 → `ExecutionResultFactInvalidated` I1 targets E1 → CORRECTION computation K2 (`submission_request_id = E1.submission_request_id`, `predecessor_execution_result_ref = E1`, `correction_authorization_ref = I1`, `computation_cursor = C2`) → Observation O2 for K2 → Attempt A2 PROCESSED → replacement Result E2. Verified: `E2.execution_result_computation_id = K2`; `E2.supersedes_fact_ref = E1`; `E2.execution_result_id != E1.execution_result_id`; `E2.submission_request_id = E1.submission_request_id` (Scenario 34/F, execution-result.md §19).

### Replay integration

`replay-event.md` v0.2 → v0.3: `ReplayState(C)` (§2) folds an additional `execution_result_computation_lineage` component (execution-result.md §2, append-only). Twelve cursor milestones (C0–C11, replacing ten) — inserted "sau computation authorization" (C1, before Observation) and "sau correction computation authorized" (C8, predecessor invalidated, K2 authorized, before O2) — proving `C7-DELTA-MAJ-01` directly (Scenario 37). Observation-only gap milestone (C2) shows K1 authorized, O1 persisted, Attempt/Result absent — sufficient to deterministically resume K1. No duplicate replay authority introduced — `replay-event.md` still authors zero `event_types:`.

### Time/cursor semantics

`OrderSubmissionRequested.recorded_time < ExecutionResultComputationAuthorized.recorded_time < PaperExecutionObservationRecorded.recorded_time < ExecutionResultProcessingAttemptRecorded(PROCESSED).recorded_time < ExecutionResultRecorded.recorded_time` (execution-result.md §12). For correction: `ExecutionResultFactInvalidated.recorded_time < (correction) ExecutionResultComputationAuthorized.recorded_time`. Computation evidence: `fact.recorded_time <= computation_cursor.recorded_time <= ExecutionResultComputationAuthorized.recorded_time`. Canonical Replay Cursor and no-look-ahead preserved unchanged.

### Regression check for C7-MAJ-02/03/04

`C7-MAJ-02` (Fill copies exact persisted Observation economics — fill.md §1/§3 unchanged), `C7-MAJ-03` (`eligible_as_position_contributing_fill`, continuing cursor-bound rule — fill.md §6 unchanged), `C7-MAJ-04` (`projection_status ∈ {EVALUABLE, NON_EVALUABLE}` — position.md §1/§2 unchanged) — **none reopened, verified unchanged**. `fill.md`/`position.md` required only reference-consistency edits (remapped `execution-result.md §N` citations to the new section numbering caused by inserting §2/§5 into execution-result.md — zero field/invariant/schema/economics/idempotency change), disclosed transparently below rather than silently preserving stale blobs under an unchanged version.

### Changed-file scope

```text
docs/domain/execution-result.md  MODIFIED v0.2 → v0.3   blob e5cbb0ee3e3b9083920c03318e3f0dd726247304
docs/domain/replay-event.md      MODIFIED v0.2 → v0.3   blob f429d31c0f8ec42e2859f5658edd8a3dedf58b64
docs/domain/fill.md              MODIFIED v0.2 → v0.3   blob a4a2c473086ef8495c4106b75d632a7af09ae3fc  (reference-consistency-only, xem trên)
docs/domain/position.md          MODIFIED v0.2 → v0.3   blob 808a3e6041af7a5521094318924fa3682be9cefa  (reference-consistency-only, xem trên)
docs/domain/README.md            MODIFIED v0.50 → v0.51   blob 9ffcb33e7e43012b06179224a1344d4a55ac9a5c
docs/MANIFEST.md                 MODIFIED manifest_version 9.76 → 9.77
docs/CHANGELOG.md                MODIFIED (this entry)
docs/domain/context-map.yaml     KHÔNG ĐỔI — computation concept sống trong execution-result-management đã đăng ký, không cần registration mới
docs/domain/order.md              KHÔNG ĐỔI — blob 94ec87593834362292dc3379068e99ef12d86412, verified byte-identical
docs/domain/execution-intent.md   KHÔNG ĐỔI — blob afc0c1fe7bdd2f285403dff29c71849ab66af70c, verified byte-identical
docs/domain/risk.md               KHÔNG ĐỔI — blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab, verified byte-identical
docs/domain/decision.md           KHÔNG ĐỔI — blob e2a26320200d350ace3da0247235bb14cef12509, verified byte-identical
docs/domain/trade-intent.md       KHÔNG ĐỔI — blob e7a306abc53ba482ff1249af1dda2829c4c82fa7, verified byte-identical
```

### Author self-review

Adding `ExecutionResultComputation` (§2) and `ExecutionResultComputationAuthorized` (§5) shifted every subsequent execution-result.md section by 2 (old §1→§1, §2→§3, §3→§4, §4→§6, §5→§7, §6→§8, §7→§9, §8→§10, §9→§11, §10→§12, §11→§13, §12→§14, §13→§15, §14→§16, §15→§17, §16→§18, §17→§19). Applying the lesson from the immediately-prior correction's scenario-numbering collisions, a full pre-write numbering plan was drafted before editing, then a Python cross-file verification script (mapping every `**Scenario N —**` definition to its home file/section and checking every citation resolves correctly) was run against all four C7 files — result: 37 distinct scenario numbers (1–37), zero collisions, zero mismatches. A second script pass caught a real, distinct bug class: `fill.md` and `position.md` (both otherwise semantically unchanged) contained six stale `execution-result.md §N` cross-file citations pointing at the OLD section numbering (e.g. `execution-result.md §6` for `ExecutionResultRecorded`, now §8; `execution-result.md §15` for the "Ngoài phạm vi" section, now §17) — these were mechanically remapped per the exact old→new section table, and both files' versions bumped to v0.3 with an explicit "reference-consistency-only, no semantic change" disclosure rather than silently modifying content under an unchanged version number or leaving the citations stale. All YAML fenced blocks across all four files re-validated via `yaml.safe_load` — 0 errors.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, Chapter 7 §7.4 (Locked, unchanged), Chapter 8 (Locked, unchanged), `order.md` v0.2 Draft §8b (byte-for-byte unchanged, verified), Package 0.2-C1–C6 (all `Consolidated Stable`, byte-for-byte unchanged, verified).

### Metadata / state

- `execution-result.md`/`replay-event.md`: **v0.2 → v0.3**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `fill.md`/`position.md`: **v0.2 → v0.3** (reference-consistency-only, KHÔNG semantic), `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `context-map.yaml`: **không đổi.**
- `README.md` (domain index): **v0.50 → v0.51**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.76 → 9.77**.
- `order.md`, `execution-intent.md`, `risk.md`, `decision.md`, `trade-intent.md`: **không đổi** (byte-for-byte, verified) — forbidden scope, không sửa.
- Mọi ADR khác, Constitution, mọi Domain Contract khác: **không đổi.**

**Package 0.2-C7 VẪN CHƯA đạt `Consolidated Stable` — chờ second bounded delta review (ChatGPT + Independent Review B) trên cùng exact baseline correction này.** Mandatory sequence tiếp tục: ChatGPT delta review → Independent Review B delta review → Product Owner consolidation decision. KHÔNG correction thêm dựa trên một review đơn lẻ. Package 0.2-C1/C2/C3/C4/C5/C6 vẫn `Consolidated Stable`, không đổi. `C7-MAJ-02`/`C7-MAJ-03`/`C7-MAJ-04` KHÔNG reopen. KHÔNG Live behavior, exchange adapter/API payload, fee/PnL/margin/leverage/liquidation semantics nào được author. KHÔNG cross-stream atomic transaction hay workflow/saga infrastructure nào được introduce. Không artifact nào Approved hay Locked. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.



**Package 0.2-C7 bounded correction — consolidated Review A + Independent Review B findings.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C7 bounded correction — C7-MAJ-01/02/03/04." Đóng đúng bốn finding Major: `C7-MAJ-01` (durable Result simulation evidence), `C7-MAJ-02` (durable Fill-price derivation evidence), `C7-MAJ-03` (non-atomic Result–Fill correction semantics), `C7-MAJ-04` (deterministic multiple-Fill Position behavior). Authorization này **không** cho phép sửa C1–C6 semantic artifacts, `order.md`, ADR/Constitution, author simulation algorithm thực tế, exchange adapter/API payload, Live behavior, partial fills, fees/PnL/accounting, close/reduce/reversal, weighted-average aggregation, portfolio netting, margin/leverage/liquidation, cross-stream transactions, workflow/saga infrastructure, Approve/Lock artifact, mark C7 Consolidated Stable, đóng OQ-002/OQ-003, hay declare Phase 0.2 complete.

### Baseline verification

```text
Expected HEAD:  1bcc079d16ccfc61cba45f751bd486adaeb0ef86
Actual HEAD:    1bcc079d16ccfc61cba45f751bd486adaeb0ef86  — match

execution-result.md:  v0.1 Draft, blob fe19a5c66088a854ade1b294598004a04a5f4e4f  — match
fill.md:               v0.1 Draft, blob f43c9e58464f783ae34f7b1df6bb9bd036a0484c  — match
position.md:            v0.1 Draft, blob b7b6b64e6e0388c00aad416540b90e1705509af0  — match
replay-event.md:        v0.1 Draft, blob de956e6d9ab0a0fd5abdc567657e06b6e3813d81  — match
context-map.yaml:      v0.19 Draft  — match
```

### Four-finding resolution matrix

| Finding | Resolution |
|---|---|
| `C7-MAJ-01` | Added `PaperExecutionObservation` (execution-result.md §1, new entity) — durable, immutable record of simulation evidence (`simulation_policy_ref`/`simulation_configuration_ref`/`simulation_build_ref`/`deterministic_input_ref`, four opaque versioned artifact refs) and output (`result_type`, `executed_quantity`, `execution_price`), logical computation key `(submission_request_id, observation_cursor)` — mirroring `risk.md`'s `(trade_intent_id, risk_context_cursor)` pattern. `ExecutionResult` now only copies `result_type` from the visible-valid Observation it references (`execution_observation_id`, new required field) — never independently computes/reinterprets. Corrected ordering: computation completes → Observation recorded → Attempt PROCESSED → Result recorded (§6a), with two explicit recoverable gaps (Observation-without-Attempt; Observation+Attempt-without-Result), both resolved by reusing the existing Observation — never rerunning simulation. Correction that flips `EXECUTED ↔ NOT_EXECUTED` uses a brand-new Observation at a new cursor, never invalidating the old one (avoids excessive correction machinery per task's own guidance). |
| `C7-MAJ-02` | Fill (`fill.md` §1/§3) now requires `execution_observation_id` (new field) matching the referenced ExecutionResult's own `execution_observation_id`, and `fill_quantity`/`quantity_unit`/`fill_price`/`price_currency` must copy exactly from that Observation's economics — Fill never independently observes or recomputes. Result→Fill recovery (§3a) explicitly never recomputes price — only copies persisted Observation economics. |
| `C7-MAJ-03` | Removed all "mandatory pairing"/"atomic-adjacent" language between `ExecutionResultFactInvalidated` and `FillFactInvalidated` (execution-result.md §7/§9, fill.md §4/§7). Replaced with a new continuing eligibility rule, `eligible_as_position_contributing_fill(fill_id, C)` (fill.md §6) — a cursor-bound validity check re-evaluated at every cursor, independent of whether/when `FillFactInvalidated` is ever appended. Position (position.md §2) now consumes this rule directly instead of Fill stream state, so an orphaned Fill is excluded from Position the moment its ExecutionResult stops being the visible-valid EXECUTED head — no cross-stream transaction required. |
| `C7-MAJ-04` | Position (`position.md` §1/§2) gained `projection_status ∈ {EVALUABLE, NON_EVALUABLE}` and `projection_reason_code = UNSUPPORTED_MULTIPLE_FILL_LINEAGES`. Zero eligible Fill → `EVALUABLE`/FLAT; exactly one → `EVALUABLE`/LONG or SHORT; more than one → `NON_EVALUABLE` with `contributing_fill_refs` listing every conflicting eligible Fill — never silently picking one, aggregating, or reporting FLAT. |

### PaperExecutionObservation model

New entity (execution-result.md §1), immutable and append-only (no correction lineage of its own — correction uses a new Observation at a new cursor instead, per task's explicit preference to avoid excessive machinery). Logical computation key `(submission_request_id, observation_cursor)`; same key + same evidence → idempotent reuse; same key + changed evidence/output → deterministic conflict (Scenario 25). `EXECUTED` requires `executed_quantity`/`execution_price`/`price_currency` present, finite, strictly positive, matching Order quantity/TradableListing currency; `NOT_EXECUTED` requires them absent.

### Corrected Attempt/Observation/Result ordering

```text
1. eligible_for_execution_result_processing == true
2. bounded PAPER simulation computation completes
3. PaperExecutionObservationRecorded appended
4. ExecutionResultProcessingAttemptRecorded(PROCESSED) appended, referencing the Observation
5. ExecutionResultRecorded appended, causation_refs → Attempt PROCESSED + Observation
```

No Attempt→Result forward reference; no cross-stream transaction assumption.

### Result recovery model

Gap A (Observation recorded, Attempt absent): reuse `execution_observation_id`, append/reuse Attempt, append/reuse Result. Gap B (Observation + Attempt recorded, Result absent): reuse both, append/reuse exactly one Result. Simulation is never rerun once an Observation exists for a logical computation key.

### Corrected ExecutionResult schema

Added `execution_observation_id` (required). `result_type` invariant: must equal the referenced Observation's `result_type` exactly — no independent computation. Correction replacement: new `execution_result_id`, same `submission_request_id`, `execution_observation_id` may point to a brand-new Observation if `result_type` changes.

### Deterministic Fill derivation

`fill.execution_result_id → ExecutionResult.execution_observation_id → PaperExecutionObservation` — `fill_quantity`/`quantity_unit`/`fill_price`/`price_currency` all required to equal the Observation's economics exactly (fill.md §1 invariant, §3 invariant).

### Result→Fill recovery

Recovery resolves the immutable Observation via the persisted `execution_result_id → execution_observation_id` chain and copies its economics verbatim — price is never recomputed during recovery (Scenario 7).

### Continuing Fill eligibility

```text
eligible_as_position_contributing_fill(fill_id, C) =
  Fill is visible-valid head for execution_result_id at C
  AND referenced ExecutionResult is visible-valid head for submission_request_id at C
  AND that ExecutionResult.result_type == EXECUTED
  AND referenced PaperExecutionObservation is visible at C
  AND Fill payload exactly matches the Observation's economics
```

A continuing, cursor-bound rule — not merely an append-time check. Its result can flip from `true` to `false` between two cursors with zero change in the Fill's own stream.

### Non-atomic Result–Fill correction behavior

At the cursor immediately after Result invalidation but before any Fill invalidation: the Fill remains historical in its own stream (may still read `VALID` in `FillCurrentView`), yet is immediately excluded from Position via the continuing eligibility rule. `FillFactInvalidated` remains the eventual correctness-marking fact for the Fill's own stream, but Position correctness never depends on when that cleanup happens (Scenario 26).

### Corrected Position projection states

`projection_status = EVALUABLE` (0 or 1 eligible Fill) vs `NON_EVALUABLE` (>1). When `NON_EVALUABLE`: all economics fields (`position_direction`/`net_quantity`/`quantity_unit`/`average_entry_price`/`price_currency`) absent; `projection_reason_code` and `contributing_fill_refs` required.

### Multiple-Fill behavior

No aggregation, no netting, no weighted average, no arbitrary selection — deterministic `NON_EVALUABLE` with full disclosure of the conflicting Fill set (Scenario 29).

### Replay updates

`ReplayState(C)` (replay-event.md §2) now folds `paper_execution_observation_lineage` and `fill_continuing_eligibility` (distinct from Fill stream state) in addition to `derived_position` (now reflecting `projection_status`). Ten cursor milestones (C0–C9, replacing eight) — including "after Result invalidation, before Fill invalidation" (proves `C7-MAJ-03`) and "multiple eligible Fill lineages" (proves `C7-MAJ-04`).

### Time/cursor semantics

`OrderSubmissionRequested.recorded_time < PaperExecutionObservationRecorded.recorded_time < ExecutionResultProcessingAttemptRecorded(PROCESSED).recorded_time < ExecutionResultRecorded.recorded_time < FillRecorded.recorded_time` — full corrected causal chain, pinned exactly as required. Canonical Replay Cursor reused verbatim throughout, no near-duplicate schema.

### Context Map changes

None. `context-map.yaml` unchanged — `PaperExecutionObservation` lives inside `execution-result.md`, already registered under the existing `execution-result-management` context; no new registration required, consistent with the task's "prefer no new context" instruction.

### Acceptance-scenario results (31 scenarios total across four files, renumbering collisions found and fixed during self-review — see below)

Scenarios 1–4, 6, 17, 18–20, 25, 27 (execution-result.md) — pass. Scenarios 5–12, 21–23, 26 (fill.md) — pass. Scenarios 13–17, 28–29 (position.md) — pass. Scenarios 24, 30–31 (replay-event.md) — pass.

### Regression check

Logical Result key (`submission_request_id`), Attempt identity separation, C6 eligibility rule, Result correction direct-predecessor lineage, logical Fill key (`execution_result_id`), full-Fill boundary, opaque Fill identity, Fill correction lineage (ten invariants), Position structural key, non-negative magnitude representation, Position non-authority, canonical Replay Cursor, C1–C6 semantics, PAPER-only boundary — **tất cả không đổi, verified**. `context-map.yaml`/`order.md`/`execution-intent.md`/`risk.md`/`decision.md`/`trade-intent.md` byte-for-byte unchanged.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, Chapter 7 §7.4 (Locked, unchanged), Chapter 8 (Locked, unchanged), `order.md` v0.2 Draft §8b (byte-for-byte unchanged, verified), Package 0.2-C1–C6 (all `Consolidated Stable`, byte-for-byte unchanged, verified).

### Author self-review

During the rewrite, an initial pass introduced several scenario-number collisions (e.g. `fill.md`'s new "Deterministic Fill recovery" reused number 3, already assigned to "Failure and retry" in `execution-result.md`; `position.md`'s new "Zero/Multiple Fill Position" reused numbers 9/11, already assigned to `fill.md`'s "Fill origin mismatch"/"Invalid Fill price"; `fill.md`'s original "Duplicate Fill" (Scenario 8) and "Executed full Fill" (Scenario 5) were accidentally overwritten during the edit). Caught via an automated cross-file citation-consistency script (mapping every `**Scenario N —**` definition to its home file/section and verifying every `(Scenario N, §X)` citation resolves correctly) and corrected: restored Scenarios 5 and 8 in `fill.md`; renumbered the new task scenarios to unique numbers 25–29; moved "Result correction EXECUTED→NOT_EXECUTED" to the pre-existing Scenario 17 (already reserved for exactly this topic in `position.md`) instead of colliding with the original Scenario 6; fixed several off-by-one section citations left over from `fill.md`'s Prohibitions/defer section renumbering (§13→§14 for Acceptance scenarios). Final state: 31 distinct scenario numbers, zero collisions, all citations verified consistent via the same script. All 22 YAML fenced blocks (11+8+2+1) re-validated via `yaml.safe_load`.

### Changed-file scope

```text
docs/domain/execution-result.md  MODIFIED v0.1 → v0.2   blob 72011d38ca0e7ad78c09eed496242a164682abaf
docs/domain/fill.md              MODIFIED v0.1 → v0.2   blob d001e0371f02145e0973c6f3b808f62f3d6465f7
docs/domain/position.md          MODIFIED v0.1 → v0.2   blob 4eeb40603804c7baa4f4bc8b7a9f13cb94db6597
docs/domain/replay-event.md      MODIFIED v0.1 → v0.2   blob 36cf46b69be70f4238ded433ce3eda33a3a2e99e
docs/domain/README.md            MODIFIED v0.49 → v0.50   blob edabbab751c7df1bd74dbea6f17629af153dd92e
docs/MANIFEST.md                 MODIFIED manifest_version 9.75 → 9.76
docs/CHANGELOG.md                MODIFIED (this entry)
docs/domain/context-map.yaml     KHÔNG ĐỔI — không cần registration mới
docs/domain/order.md              KHÔNG ĐỔI — blob 94ec87593834362292dc3379068e99ef12d86412, verified byte-identical
docs/domain/execution-intent.md   KHÔNG ĐỔI — blob afc0c1fe7bdd2f285403dff29c71849ab66af70c, verified byte-identical
docs/domain/risk.md               KHÔNG ĐỔI — blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab, verified byte-identical
docs/domain/decision.md           KHÔNG ĐỔI — blob e2a26320200d350ace3da0247235bb14cef12509, verified byte-identical
docs/domain/trade-intent.md       KHÔNG ĐỔI — blob e7a306abc53ba482ff1249af1dda2829c4c82fa7, verified byte-identical
```

### Metadata / state

- `execution-result.md`/`fill.md`/`position.md`/`replay-event.md`: **v0.1 → v0.2**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `context-map.yaml`: **không đổi.**
- `README.md` (domain index): **v0.49 → v0.50**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.75 → 9.76**.
- `order.md`, `execution-intent.md`, `risk.md`, `decision.md`, `trade-intent.md`: **không đổi** (byte-for-byte, verified) — forbidden scope, không sửa.
- Mọi ADR khác, Constitution, mọi Domain Contract khác: **không đổi.**

**Package 0.2-C7 VẪN CHƯA đạt `Consolidated Stable` — chờ bounded delta review (ChatGPT + Independent Review B) trên cùng exact baseline correction này.** Mandatory sequence tiếp tục: ChatGPT delta review → Independent Review B delta review → Product Owner consolidation decision. KHÔNG correction thêm dựa trên một review đơn lẻ. Package 0.2-C1/C2/C3/C4/C5/C6 vẫn `Consolidated Stable`, không đổi. KHÔNG Live behavior, exchange adapter/API payload, fee/PnL/margin/leverage/liquidation semantics nào được author. KHÔNG cross-stream atomic transaction nào được introduce. Không artifact nào Approved hay Locked. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-31 — author Package 0.2-C7 execution result fill position replay

**Package 0.2-C7 — Execution Result, Fill, Position and Replay Integration Foundation v0.1 authored.** Vai trò: `Domain Contract Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C7: Execution Result, Fill, Position and Replay Integration Foundation v0.1". Authorized artifacts: `docs/domain/execution-result.md`, `docs/domain/fill.md`, `docs/domain/position.md`, `docs/domain/replay-event.md` (tất cả tạo mới, v0.1 Draft). Authorization này **không** cho phép author Live behavior, exchange API payload, external order ID, routing/adapter, cancellation/replacement protocol, partial fill (trừ khi bounded rule disclosed), fees/commissions/funding, slippage model, realized/unrealized PnL, portfolio aggregation, cross-account/cross-listing netting, margin/leverage/liquidation, settlement/tax/accounting ledger, FX conversion, general workflow engine, sửa C1–C6 artifacts, sửa ADR/Constitution, đóng OQ-002/OQ-003, Approve/Lock bất kỳ artifact nào, hay mark C7 Consolidated Stable.

### Baseline verification

```text
Expected HEAD:  45f9053487e36e2f7680ae71433422cd1c4f3ad3
Actual HEAD:    45f9053487e36e2f7680ae71433422cd1c4f3ad3  — match

Package 0.2-C1:  Consolidated Stable (không đổi)
Package 0.2-C2:  Consolidated Stable (không đổi)
Package 0.2-C3:  Consolidated Stable (không đổi)
Package 0.2-C4:  Consolidated Stable (không đổi)
Package 0.2-C5:  Consolidated Stable (không đổi)
Package 0.2-C6:  Consolidated Stable (không đổi)
order.md:          v0.2 Draft, blob 94ec87593834362292dc3379068e99ef12d86412
context-map.yaml:  v0.18 Draft, blob d87428e9919005a2cd7f7b282c92f710e5aed382
execution-result.md/fill.md/position.md/replay-event.md: absent trước transaction — đúng expected state, KHÔNG có baseline conflict
```

### Physical artifact decomposition

Bốn file riêng biệt (task's preferred decomposition, chọn để tách bạch observation khỏi execution fact): `execution-result.md` sở hữu ExecutionResult observation + processing Attempt; `fill.md` sở hữu Fill fact + Fill correction; `position.md` sở hữu deterministic Position projection (KHÔNG authoritative); `replay-event.md` sở hữu CHỈ integration/reference semantics, KHÔNG duplicate authority.

### Changed-file scope

```text
docs/domain/execution-result.md  NEW v0.1 Draft   blob fe19a5c66088a854ade1b294598004a04a5f4e4f
docs/domain/fill.md              NEW v0.1 Draft   blob f43c9e58464f783ae34f7b1df6bb9bd036a0484c
docs/domain/position.md          NEW v0.1 Draft   blob b7b6b64e6e0388c00aad416540b90e1705509af0
docs/domain/replay-event.md      NEW v0.1 Draft   blob de956e6d9ab0a0fd5abdc567657e06b6e3813d81
docs/domain/context-map.yaml     MODIFIED v0.18 → v0.19   blob d2813e774093eb9c7510f9e41955612240726f89
docs/domain/README.md            MODIFIED v0.48 → v0.49   blob dcd2dca46c0d1711ab87e644c04ca86983c505da
docs/MANIFEST.md                 MODIFIED manifest_version 9.74 → 9.75
docs/CHANGELOG.md                MODIFIED (this entry)
docs/domain/order.md              KHÔNG ĐỔI — blob 94ec87593834362292dc3379068e99ef12d86412, verified byte-identical
docs/domain/execution-intent.md   KHÔNG ĐỔI — blob afc0c1fe7bdd2f285403dff29c71849ab66af70c, verified byte-identical
docs/domain/risk.md               KHÔNG ĐỔI — blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab, verified byte-identical
docs/domain/decision.md           KHÔNG ĐỔI — blob e2a26320200d350ace3da0247235bb14cef12509, verified byte-identical
docs/domain/trade-intent.md       KHÔNG ĐỔI — blob e7a306abc53ba482ff1249af1dda2829c4c82fa7, verified byte-identical
```

### Execution-result processing Attempt model

`execution_result_processing_attempt_id` — opaque, individual attempt identity, TÁCH BIỆT khỏi logical result key (`submission_request_id`). `attempt_outcome ∈ {PROCESSED, INELIGIBLE, FAILED_BEFORE_RESULT}` (execution-result.md §1/§3) — mọi lần thử ĐỀU ghi nhận. `PROCESSED` chỉ ghi SAU KHI bounded result payload computation hoàn tất trọn vẹn (§4a) — one-way sequence, `ExecutionResultRecorded.causation_refs` trỏ ngược lại attempt. `INELIGIBLE`: `eligible_for_execution_result_processing == false` (order.md §8b). `FAILED_BEFORE_RESULT`: retryable, không permanently block recovery. KHÔNG broad operational error taxonomy — v0.1 chỉ một reason_code cho mỗi outcome cần reason.

### Execution Result identity and logical key

`execution_result_id` — opaque, globally unique, immutable. **Logical result key = `submission_request_id` (KHÔNG `order_id`)** — đóng đúng yêu cầu task "Do not use order_id alone if one Order may receive a corrected/reissued Submission Request after invalidation." Nếu S1 invalidate và S2 thay thế (order.md §9), ExecutionResult của S1 TUYỆT ĐỐI KHÔNG trở thành ExecutionResult của S2 — mỗi `submission_request_id` sở hữu lineage riêng. Cardinality: một visible-valid OrderSubmissionRequested → zero hoặc một visible-valid Execution Result head (execution-result.md §1 invariant). Idempotency: same submission request + same payload → reuse; same + changed → conflict.

### C6 readiness integration

`ExecutionResultRecorded` (§4a) precondition dùng CHÍNH XÁC `eligible_for_execution_result_processing(order_id, C)` (order.md §8b) KHÔNG rút gọn/duplicate/bypass — bao gồm cả năm điều kiện của rule đó (Order visible-valid-head, `eligible_for_new_order_creation` trọn vẹn, đúng một Submission Request valid, `current_status == SUBMISSION_REQUESTED`).

### Result origin binding

Mọi field origin (order_id/submission_request_id/originating_execution_intent_id/originating_risk_evaluation_id/trade_intent_id/account_id/environment/instrument_selection_ref/direction/order_quantity/quantity_unit) PHẢI khớp CHÍNH XÁC chuỗi visible-valid TẠI execution_result_cursor (execution-result.md §4 invariant) — reject predecessor Order, invalidated Order, invalidated Submission Request, request thuộc Order khác, Order WITHDRAWN/EXPIRED, Execution Intent không ISSUED, Risk/Trade Intent/Decision chain invalid, hay bất kỳ field origin nào đổi.

### Result idempotency and correction

`execution_result_derivation_idempotency_policy: ONE_VALID_RESULT_PER_SUBMISSION_REQUEST` (§9). Correction: append-only, `supersedes_fact_ref` trỏ TRỰC TIẾP predecessor `ExecutionResultRecorded` (KHÔNG trỏ `ExecutionResultFactInvalidated` — event đó nằm trong `causation_refs`), mười invariant đối xứng `risk.md` §10/`order.md` §9 (§7). Một visible-valid-head duy nhất per `submission_request_id`.

### Fill identity and derivation

`fill_id` — opaque, globally unique, immutable. Logical Fill key = `execution_result_id`. Cardinality: `EXECUTED` → đúng MỘT visible-valid Fill head; `NOT_EXECUTED` → zero Fill. Idempotency: same `execution_result_id` + same payload → reuse; same + changed → conflict, KHÔNG duplicate Fill cho một result.

### Fill validation and full-fill boundary

**Disclosed v0.1 bounded rule (task yêu cầu explicit disclosure):** executed result LUÔN sản sinh CHÍNH XÁC một full Fill — `fill_quantity == Order.quantity`, KHÔNG partial-fill semantics. Reject: `fill_quantity <= 0`; `fill_price <= 0`; `fill_quantity != Order.quantity`; `quantity_unit` mismatch; `price_currency` mismatch; `environment != PAPER`; origin IDs mismatch; `execution_result.result_type != EXECUTED`; execution_result không phải visible-valid-head; submission request/Order invalid. `fill_price` là giá PAPER execution quan sát được — KHÔNG limit price/price-guarantee/slippage semantics nào được author.

### Result-to-Fill append-gap recovery

Thứ tự bắt buộc: result payload computed → Attempt PROCESSED → `ExecutionResultRecorded` → Fill payload computed → `FillRecorded` (fill.md §3a). Crash sau `ExecutionResultRecorded(EXECUTED)` nhưng TRƯỚC `FillRecorded` là recoverable append gap — recovery PHẢI tái sử dụng CHÍNH `execution_result_id`, regenerate CÙNG deterministic Fill payload, append/reuse ĐÚNG MỘT Fill, TUYỆT ĐỐI KHÔNG duplicate. KHÔNG atomic result→Fill transaction assumption.

### Fill correction and replay

Append-only, `supersedes_fact_ref` trỏ TRỰC TIẾP predecessor `FillRecorded`, mười invariant đối xứng (fill.md §6). **Ràng buộc bắt buộc, ĐÓNG ĐÚNG YÊU CẦU Scenario 17:** khi ExecutionResult gốc chuyển visible-valid-head sang `result_type != EXECUTED` (hoặc invalidate không thay thế), MỌI Fill visible-valid tham chiếu `execution_result_id` cũ PHẢI invalidate qua `FillFactInvalidated` — trạng thái corrected cuối cùng KHÔNG BAO GIỜ chứa Fill visible-valid dưới một non-executed result (execution-result.md §7/fill.md §4/§6 coupling rule, KHÔNG "silently leave a valid Fill under a non-executed result" — đúng nguyên văn yêu cầu task).

### Position key and representation

Position key = (account_id, environment, instrument_selection_ref) — structural, KHÔNG opaque identity riêng. Representation: `net_quantity` LUÔN non-negative magnitude, `position_direction` (LONG/SHORT) TÁCH BIỆT tường minh khỏi magnitude — KHÔNG combine signed quantity với direction (position.md §3). `FLAT ⟺ net_quantity == 0`; `LONG/SHORT ⟺ net_quantity > 0`.

### Position fold

Deterministic projection từ visible-valid Fill history (fill.md §5 fold, KHÔNG `FillCurrentView`). Vì v0.1 CHỈ authorize `OPEN_EXPOSURE`, Position KHÔNG cần close/reduce/reversal arithmetic. **Disclosed bounded rule (task yêu cầu chọn một trong hai lựa chọn):** v0.1 walking skeleton bound tới ĐÚNG MỘT visible-valid Fill lineage đóng góp per Position key — tránh silently author portfolio netting/same-direction weighted aggregation (position.md §7, lý do đầy đủ disclosed).

### Position recomputation after Fill correction

Position KHÔNG correct bằng mutation — KHÔNG compensating Position event/command. Invalidate F1 → Position projection EXCLUDES F1 → recompute (thường FLAT nếu không còn Fill khác) → replacement F2 xuất hiện → Position recompute lại từ F2 (position.md §4).

### Replay integration model

`ReplayStateProjection` (replay-event.md §1) — integration contract thuần túy, `ReplayState(C)` (§2) fold TÁM thành phần (Decision/Trade Intent/RiskEvaluation/Execution Intent/Order/Submission Request/ExecutionResult/Fill lineage, cộng derived Position) tại MỘT canonical Replay Cursor duy nhất — mỗi thành phần dùng ĐÚNG fold algorithm đã pin tại Domain Contract sở hữu nó, KHÔNG tự định nghĩa lại. KHÔNG author event mới nào — KHÔNG "ReplayDecision"/"ReplayOrder"/"ReplayFill" (§3, đóng đúng yêu cầu "must not duplicate Decision, Risk, Order or Fill authority in a second event stream"). Tám cursor mốc bắt buộc C0–C7 (§4) chứng minh trước/sau Submission Request/Execution Result/Fill/Fill invalidation/replacement Fill/Execution Result invalidation/replacement Execution Result.

### Time/cursor semantics

`OrderSubmissionRequested.recorded_time < ExecutionResultRecorded.recorded_time < FillRecorded.recorded_time` — strict causal chain. `OrderSubmissionRequested.effective_time <= ExecutionResultRecorded.result_effective_time <= FillRecorded.fill_effective_time`. Mọi evidence: `fact.recorded_time <= computation_cursor.recorded_time <= resulting_event.recorded_time`. Correction invalidation strict SAU target fact. `execution_result_cursor`/`fill_context_cursor` TÁI SỬ DỤNG nguyên vẹn canonical Replay Cursor (Chapter 8 §8.5.1) — KHÔNG schema gần giống nào được tạo.

### Context Map integration

Bốn context MỚI CÙNG capability `execution-management` (đã có từ C6, KHÔNG capability mới): `execution-result-management`/`fill-management`/`position-management`/`replay-integration` tại `context-map.yaml` **v0.18 → v0.19**. Mười relationship edge MỚI — ba edge nội bộ chuỗi C7 (order-management→execution-result-management, execution-result-management→fill-management, fill-management→position-management) cộng bảy edge authoritative-context→replay-integration (strategy-decision×2: decision-recorded/trade-intent-issued; risk-gateway×2: risk-evaluation-recorded/execution-intent-issued; order-management: order-created; execution-result-management: execution-result-recorded; fill-management: fill-recorded). KHÔNG edge cho position-management→replay-integration (Position không có authoritative event stream, derived projection thuần túy).

### Acceptance-scenario results (24 scenarios, phân bổ across bốn file — execution-result.md §15/fill.md §13/position.md §9/replay-event.md §9)

Scenario 1 (eligible result processing) — pass. Scenario 2 (ineligible) — pass. Scenario 3 (failure and retry) — pass. Scenario 4 (result append gap) — pass. Scenario 5 (executed full Fill) — pass. Scenario 6 (not executed, zero Fill) — pass. Scenario 7 (result-to-Fill append gap) — pass. Scenario 8 (duplicate Fill) — pass. Scenario 9 (Fill origin mismatch) — pass. Scenario 10 (invalid Fill quantity) — pass. Scenario 11 (invalid Fill price) — pass. Scenario 12 (Fill correction) — pass. Scenario 13 (Position from LONG Fill) — pass. Scenario 14 (Position from SHORT Fill) — pass. Scenario 15 (Fill invalidation → Position FLAT) — pass. Scenario 16 (Fill replacement → Position recompute) — pass. Scenario 17 (result correction EXECUTED→NOT_EXECUTED, Fill mandatory invalidation) — pass. Scenario 18 (invalidated Submission Request) — pass. Scenario 19 (Order replacement) — pass. Scenario 20 (Execution Intent withdrawn) — pass. Scenario 21 (replay before Fill correction) — pass. Scenario 22 (replay after Fill invalidation) — pass. Scenario 23 (replay after replacement Fill) — pass. Scenario 24 (no duplicate replay authority) — pass.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, Chapter 7 §7.4 (Locked, Type 2 Projection — byte-for-byte unchanged), Chapter 8 §8.1.1/§8.2/§8.5 (Locked, byte-for-byte unchanged), `order.md` v0.2 Draft §8b (byte-for-byte unchanged, verified), `execution-intent.md`/`risk.md`/`decision.md`/`trade-intent.md` (byte-for-byte unchanged, verified), Package 0.2-C1/C2/C3/C4/C5/C6 (all `Consolidated Stable`, byte-for-byte unchanged, verified).

### Author self-review

Hai bounded judgment call disclosed tường minh theo yêu cầu task: (1) full-Fill boundary — executed result sản sinh chính xác một full Fill, partial-fill deferred hoàn toàn (fill.md §12); (2) one-Fill-per-Position-key bound — v0.1 walking skeleton KHÔNG author weighted aggregation cho nhiều Fill lineage cùng key, tránh silently author portfolio netting (position.md §7). `replay-event.md` verified KHÔNG chứa bất kỳ `event_types:` block nào — xác nhận không duplicate authority. Tất cả 20 YAML fenced block (9+8+2+1) trong bốn file parse qua `yaml.safe_load` — verified. Tất cả `§N` citation cross-reference verified qua grep trong cả bốn file — không có tham chiếu treo (chỉ cross-file reference hợp lệ tới order.md §8a/§8b, risk.md §5b1). Không tìm thấy finding blocking nào khác (author self-review — chưa qua Review A/B).

### Metadata / state

- `execution-result.md`/`fill.md`/`position.md`/`replay-event.md`: **NEW**, `version: "0.1"`, `status: Draft`, `approved_by: null`, `approved_at: null`.
- `context-map.yaml`: **v0.18 → v0.19** — capability `execution-management` (không mới) với bốn context MỚI, mười relationship edge MỚI.
- `README.md` (domain index): **v0.48 → v0.49**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.74 → 9.75**.
- `order.md`, `execution-intent.md`, `risk.md`, `decision.md`, `trade-intent.md`: **không đổi** (byte-for-byte, verified).
- `ADR-010.md`, `ADR-012.md`, `ADR-013.md`, `instrument.md`, `venue.md`, `account.md`, `strategy.md`: **không đổi** (byte-for-byte, verified).
- Mọi ADR khác, Constitution, mọi Domain Contract khác: **không đổi.**

**Package 0.2-C7 CHƯA đạt `Consolidated Stable` — chờ Review A + Independent Review B trên cùng exact baseline này.** Mandatory sequence: Author baseline → ChatGPT Review A → Independent Review B (cùng exact baseline) → merge finding → một correction commit được Product Owner authorize → ChatGPT delta review → Independent Review B delta review → Product Owner consolidation decision. **KHÔNG correction dựa trên một review đơn lẻ.** Package 0.2-C1/C2/C3/C4/C5/C6 vẫn `Consolidated Stable`, không đổi. KHÔNG Live behavior, exchange adapter/API payload, fee/PnL/margin/leverage/liquidation semantics nào được author. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-31 — consolidate Package 0.2-C6

**Package 0.2-C6 Order Foundation consolidated as `Consolidated Stable`.** Vai trò: `Package Lifecycle Consolidation Author · Repository Transaction Executor`. Product Owner authorized: "Package 0.2-C6: Consolidated Stable" (2026-07-31). Authorization này cho phép ghi Package 0.2-C6 vào lifecycle state `Consolidated Stable` — nó KHÔNG cho phép Approve/Lock `order.md`, không sửa `context-map.yaml`/bất kỳ C1–C5 artifact/ADR nào, không sửa Constitution, không đóng OQ, không authorize Live, không author/authorize Package 0.2-C7, không author Fill/Position, không thêm speculative edge case, không tuyên bố Phase 0.2 hoàn thành.

### Baseline verification

```text
Expected HEAD:  2c655c18aa976278c9b4f75cbe0b6aae202e5223
Actual HEAD:    2c655c18aa976278c9b4f75cbe0b6aae202e5223  — match

order.md:          v0.2 Draft, blob 94ec87593834362292dc3379068e99ef12d86412  — match
context-map.yaml:  v0.18 Draft, blob d87428e9919005a2cd7f7b282c92f710e5aed382  — match
README.md:         v0.47 Draft, blob 6e53f725c749cb9bfff2473afcd2c5af76b29481  — match
MANIFEST.md:        manifest_version 9.73  — match
```

### Product Owner authorization recorded

```text
Package 0.2-C6:
  Consolidated Stable
```

Meaning: the exact reviewed C6 baseline is stable enough to serve as the dependency baseline for Package 0.2-C7. It does not mean any artifact is Approved or Locked.

### Exact reviewed baseline pinned

```text
Package 0.2-C6 reviewed HEAD:  2c655c18aa976278c9b4f75cbe0b6aae202e5223

Primary artifact:        order.md v0.2 Draft, blob 94ec87593834362292dc3379068e99ef12d86412
Integration artifact:    context-map.yaml v0.18 Draft, blob d87428e9919005a2cd7f7b282c92f710e5aed382 (unchanged)
Registry baseline:       MANIFEST v9.73
```

### Review evidence

```text
ChatGPT bounded delta Review A:        Clean — Blocker 0, Major 0, Minor 0
Independent Delta Review B:            Clean — Blocker 0, Major 0, Minor 0
```

### Complete finding ledger — all resolved (v0.1 → v0.2 bounded correction)

```text
C6-MAJ-01:  Resolved (supersedes_fact_ref added to OrderCreated.payload, direct-predecessor-fact-targeting convention pinned, ten correction-lineage invariants, explicit-chain fold algorithm)
C6-MAJ-02:  Resolved (OrderFactInvalidated may target OrderSubmissionRequested, invalidate-only, fold algorithm excludes invalidated requests from every fold)
C6-MAJ-03:  Resolved (eligible_for_execution_result_processing uses the complete eligible_for_new_order_creation rule, pins current_status == SUBMISSION_REQUESTED exactly)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

### Package lifecycle meaning

`Consolidated Stable` là package lifecycle/readiness state — nghĩa là: reviewed package baseline nội bộ coherent; mọi qualifying finding đã resolved; deferred limitations được ghi nhận tường minh là non-blocking Phase 1 concern; package integration đủ ổn định để làm dependency baseline cho package kế tiếp (0.2-C7). Nó KHÔNG có nghĩa: artifact Approved; artifact Locked; ADR thay đổi; Domain Contract bất biến; OQ closure; Phase completion; implementation authorization; Live authorization.

### Confirmation — `order.md` and `context-map.yaml` byte-identical

```text
docs/domain/order.md          blob 94ec87593834362292dc3379068e99ef12d86412 — verified byte-identical to reviewed baseline
docs/domain/context-map.yaml  blob d87428e9919005a2cd7f7b282c92f710e5aed382 — verified byte-identical to reviewed baseline
```

### Confirmation — C1–C5 semantic artifacts byte-identical

```text
docs/domain/risk.md              blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab — verified byte-identical
docs/domain/execution-intent.md  blob afc0c1fe7bdd2f285403dff29c71849ab66af70c — verified byte-identical
docs/domain/decision.md          blob e2a26320200d350ace3da0247235bb14cef12509 — verified byte-identical
docs/domain/trade-intent.md      blob e7a306abc53ba482ff1249af1dda2829c4c82fa7 — verified byte-identical
docs/domain/instrument.md        blob 81651f6a19a3f22fa7a924173f14b02e6467c8e0 — verified byte-identical
docs/domain/venue.md             blob 0ffb9e64bcb7dec108edea0bc9c3af3a162b40d9 — verified byte-identical
docs/domain/account.md           blob 9fd2d0fb3235343d52c3435df3f1c7e08dd22781 — verified byte-identical
docs/domain/strategy.md          blob c2cadc464bc8baecff41ff8079461ec0d5dfaccc — verified byte-identical
```

### Unchanged artifact statuses

`order.md`: **giữ nguyên** `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte — không sửa Domain Contract semantic trong transaction này. `context-map.yaml`: **giữ nguyên** `version: "0.18"`, `status: Draft`, byte-for-byte — không sửa. `decision.md`/`trade-intent.md`/`risk.md`/`execution-intent.md`: **giữ nguyên**, byte-for-byte — không sửa. Mọi C1–C4 Domain Contract (`instrument.md`/`venue.md`/`account.md`/`strategy.md`) và mọi ADR: **giữ nguyên**, byte-for-byte — không sửa.

### Package lifecycle states pinned

```text
Package 0.2-C1:     Consolidated Stable
Package 0.2-C2:     Consolidated Stable
Package 0.2-C3:     Consolidated Stable
Package 0.2-C4:     Consolidated Stable
Package 0.2-C5:     Consolidated Stable
Package 0.2-C6:     Consolidated Stable
Package 0.2-C7:     unauthorized, unauthored
```

### Artifact lifecycle states pinned

```text
order.md:           Draft, version "0.2", approved_by: null, approved_at: null, not Locked
context-map.yaml:   Draft, version "0.18"
```

### Changed-file scope

```text
docs/domain/README.md            MODIFIED v0.47 → v0.48
docs/MANIFEST.md                 MODIFIED manifest_version 9.73 → 9.74
docs/CHANGELOG.md                MODIFIED (this entry)
docs/domain/order.md             KHÔNG ĐỔI — blob 94ec87593834362292dc3379068e99ef12d86412, verified byte-identical
docs/domain/context-map.yaml     KHÔNG ĐỔI — blob d87428e9919005a2cd7f7b282c92f710e5aed382, verified byte-identical
docs/domain/risk.md              KHÔNG ĐỔI — blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab, verified byte-identical
docs/domain/execution-intent.md  KHÔNG ĐỔI — blob afc0c1fe7bdd2f285403dff29c71849ab66af70c, verified byte-identical
docs/domain/decision.md          KHÔNG ĐỔI — blob e2a26320200d350ace3da0247235bb14cef12509, verified byte-identical
docs/domain/trade-intent.md      KHÔNG ĐỔI — blob e7a306abc53ba482ff1249af1dda2829c4c82fa7, verified byte-identical
```

### Metadata / state

- `order.md`, `context-map.yaml`, `risk.md`, `execution-intent.md`, `decision.md`, `trade-intent.md`: **không đổi** (semantic và version) — package lifecycle metadata only.
- `README.md` (domain index): **v0.47 → v0.48**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.73 → 9.74**; dòng `domain/` cập nhật ghi nhận Package 0.2-C6 `Consolidated Stable`.
- Mọi Domain Contract khác (`instrument.md`, `venue.md`, `account.md`, `strategy.md`, `candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, `context.md`), mọi ADR file, Constitution: **không đổi.**

**Package 0.2-C7 baseline dependency đã thỏa, eligible cho Product Owner scope authorization — CHƯA bắt đầu, CHƯA author, KHÔNG được authorize bởi transaction này.** OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất. KHÔNG Fill/Position semantics nào được author.

## [Unreleased] — 2026-07-31 — correct Package 0.2-C6 order lineage

**Package 0.2-C6 bounded correction — consolidated Review A + Independent Review B findings.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C6 bounded correction — consolidated Review A + Independent Review B findings." Đóng đúng ba finding Major: `C6-MAJ-01` (serializable Order replacement lineage), `C6-MAJ-02` (submission request invalidation), `C6-MAJ-03` (complete future C7 authority chain). Authorization này **không** cho phép sửa C1–C5 artifacts, `execution-intent.md`/`risk.md`/`decision.md`/`trade-intent.md`, ADR/Constitution, author Fill/Position, venue acknowledgement/external order ID/routing/adapters, Limit/Stop/TIF/IOC/FOK, submission retry worker/queue/general workflow engine, thay đổi Risk-approved quantity, Live, authorize C7, Approve/Lock artifact, mark C6 Consolidated Stable, đóng OQ-002/OQ-003, hay declare Phase 0.2 complete.

### Baseline verification

```text
Expected HEAD:  77364ca4440557cdc083a5eed34b505a727c1a7a
Actual HEAD:    77364ca4440557cdc083a5eed34b505a727c1a7a  — match

order.md:          v0.1 Draft, blob 912d9b6a779187f287803f2a70c1cc642bb04a4e  — match
context-map.yaml:  v0.18 Draft, blob d87428e9919005a2cd7f7b282c92f710e5aed382  — match
README.md:         v0.46 Draft, blob 31b26991a6ef3adae4af1fe558b2d2214e0e61a4  — match
MANIFEST.md:        manifest_version 9.72  — match
```

### Three-finding resolution matrix

| Finding | Resolution |
|---|---|
| `C6-MAJ-01` | Added `supersedes_fact_ref` to `OrderCreated.payload` (§4) — absent in v0.1 despite correction prose requiring it. Pinned the exact pointer convention as **direct predecessor-fact targeting** (order.md §4/§9), matching the controlling `risk.md` §10 pattern (`RiskEvaluationRecorded.supersedes_fact_ref = predecessor fact`, NOT the invalidation event) — `causation_refs` is the field that carries the `OrderFactInvalidated` reference, kept separate from `supersedes_fact_ref`. Added ten explicit correction-lineage invariants (§9). Rewrote the Current View fold algorithm (§8 Tầng 1) to resolve the head via an **explicit `supersedes_fact_ref` chain** (`O1 → O2 → O3`, cấm nhảy cóc/fork) instead of "newest uninvalidated fact." |
| `C6-MAJ-02` | `OrderFactInvalidated.invalidated_fact_ref` (§7) can now target `OrderSubmissionRequested` in addition to `OrderCreated`/`OrderStatusChanged` — invalidate-only, no same-ID replacement required. Rewrote the Current View fold algorithm (§8 Tầng 2) to exclude an invalidated request from lifecycle fold, duplicate-suppression (§8a), and C7 readiness (§8b) with no compensating event — lifecycle recomputes directly from remaining valid history. A new request (different `submission_request_id`, same `order_id`) may be appended afterward if `eligible_for_new_submission_request` becomes true again. |
| `C6-MAJ-03` | `eligible_for_execution_result_processing` (§8b) now uses the **complete** `eligible_for_new_order_creation` rule (execution-intent.md §6a, all five conditions — including condition 1, `ExecutionIntent.current_status(C) == ISSUED`, previously omitted) instead of only conditions 2–5. Also tightened the lifecycle condition from "not WITHDRAWN/EXPIRED" (which incorrectly allowed `CREATED` — never submitted — to pass) to exactly `current_status == SUBMISSION_REQUESTED`, derived only from a visible valid `OrderSubmissionRequested`. |

### Corrected `OrderCreated` schema

```yaml
payload:
  order_id: {type: string, required: true}
  # ... (unchanged fields)
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "VẮNG MẶT cho Order gốc; BẮT BUỘC cho correction replacement — trỏ TRỰC TIẾP predecessor OrderCreated fact (KHÔNG trỏ OrderFactInvalidated)"}
```

Initial `OrderCreated`: `supersedes_fact_ref` absent. Correction replacement: `supersedes_fact_ref` required, `order_id != predecessor.order_id`, `originating_execution_intent_id == predecessor.originating_execution_intent_id`, `causation_refs` additionally contains the `OrderFactInvalidated` targeting predecessor (predecessor invalidation visible before replacement is recorded).

### Explicit Order correction lineage

Ten invariants added (order.md §9), mirroring `risk.md` §10 exactly: original has no `supersedes_fact_ref`; replacement's `supersedes_fact_ref` points directly to the predecessor fact; same `originating_execution_intent_id` across the chain; replacement's `causation_refs` must contain the predecessor's `OrderFactInvalidated`; replacement must supersede the *current* lineage head (no skipping intermediate heads); at most one direct replacement per invalidated fact (fork forbidden); replacement cannot be visible before its invalidation; historical members remain append-only and forever resolvable; an invalidated fact is never implicitly reused by the fold; retry with a different payload while the predecessor is still valid remains a conflict, not an implicit correction. Prior `OrderSubmissionRequested` facts are explicitly NOT inherited by a replacement Order — they remain historical under the predecessor, which becomes ineligible for new submission requests; the replacement starts at `CREATED` and must receive its own submission request.

### Submission request invalidation model

`OrderSubmissionRequested` (order.md §6) can now be invalidated via `OrderFactInvalidated` (§7) — invalidate-only, no `supersedes_fact_ref` required on the subject itself (deferred general-replacement semantics not needed for v0.2). Standard `OrderFactInvalidated` invariants already cover: `invalidated_fact_ref` must reference a valid, not-yet-invalidated request; `subject_ref`/`effective_time` must match the target exactly; `recorded_time` strictly later; at most one invalidation per fact; no invalidation-of-invalidation.

### Corrected lifecycle fold

Current View fold algorithm (order.md §8) rewritten into two tiers: **Tầng 1** resolves the visible-valid-head `order_id` for a logical creation key by walking the *explicit* `supersedes_fact_ref` chain (O1 → O2 → ...), stopping at the first link not invalidated at cursor C — never selecting a head purely by "newest uninvalidated fact." **Tầng 2** collects `OrderStatusChanged` (sliced by effective_time) and `OrderSubmissionRequested` (each fact independent) belonging to the current head, excludes any fact with a visible `OrderFactInvalidated`, then applies the remaining valid facts in deterministic total order (`effective_time ASC, recorded_time ASC, event_id ASC`) — each fact validated against the state already folded from earlier valid facts in the *same* total order, not against a stale snapshot. Default state after `OrderCreated` is `CREATED`; a valid submission request yields `SUBMISSION_REQUESTED`; a valid forward `OrderStatusChanged` yields the terminal state; an invalidated request contributes nothing.

### Corrected submission eligibility

```text
eligible_for_new_submission_request(order_id, C) =
  Order is visible valid head at C
  AND Order.current_status(C) == CREATED
  AND eligible_for_new_order_creation(originating_execution_intent_id, C) == true
  AND no visible valid OrderSubmissionRequested exists for order_id at C
```

An invalidated request no longer counts toward the fourth condition — it does not block a later valid request (order.md §8a).

### Corrected future C7 readiness

```text
eligible_for_execution_result_processing(order_id, C) =
  Order is the visible valid head for originating_execution_intent_id at C
  AND eligible_for_new_order_creation(originating_execution_intent_id, C) == true
  AND exactly one valid OrderSubmissionRequested exists for order_id at C
  AND Order.current_status(C) == SUBMISSION_REQUESTED
```

Now transitively requires Execution Intent ISSUED, valid APPROVED Risk Evaluation head, valid Trade Intent, valid Decision, valid Order head, valid Submission Request, and lifecycle exactly `SUBMISSION_REQUESTED` (order.md §8b). If Execution Intent becomes WITHDRAWN/EXPIRED, `eligible_for_execution_result_processing = false` — historical Order/request remain resolvable. No Fill semantics authored.

### Replay-before/replay-after behavior

Cursor before an `OrderFactInvalidated` targeting a submission request: request visible and valid, lifecycle may read `SUBMISSION_REQUESTED`. Cursor at/after: request excluded from the fold, lifecycle recomputes (typically back to `CREATED`), and C7 readiness becomes false (order.md §7/§8 invariants).

### Acceptance-scenario results (order.md §17, 24 scenarios renumbered 1–24)

Scenarios 1–11 (renumbered from v0.1's A–K, unchanged semantics) — pass. Scenario 12 (initial Order, `supersedes_fact_ref` absent) — pass. Scenario 13 (corrected Order, direct `supersedes_fact_ref`, expanded from v0.1's L) — pass. Scenario 14 (time ordering, renumbered from N) — pass. Scenario 15 (Execution Intent withdrawn → C7 false) — pass. Scenario 16 (Execution Intent expired → C7 false) — pass. Scenario 17 (direct fork rejected) — pass. Scenario 18 (false submission request correction, recompute to CREATED, no compensating event) — pass. Scenario 19 (reissue after invalidation) — pass. Scenario 20 (complete valid chain → C7 true, replaces v0.1's O) — pass. Scenario 21 (Order replacement does not inherit submission, expanded from v0.1's M) — pass. Scenario 22 (invalidated request and C7 → false) — pass. Scenario 23 (replay before request invalidation) — pass. Scenario 24 (replay after request invalidation) — pass.

### Regression check

Opaque `order_id`, logical creation key, per-attempt identity, truthful Attempt ordering, retry after `FAILED_BEFORE_CREATION`, zero-or-one valid Order head, exact origin preservation, strictly positive quantity, no resize/clamp/round, PAPER/OPEN_EXPOSURE/MARKET boundary, no cross-stream atomicity, time/cursor/no-look-ahead, non-authoritative Current View, C1–C5 semantics, Context Map ownership and dependency edge, C6/C7 boundary — **tất cả không đổi, verified**. `context-map.yaml` byte-for-byte unchanged (no capability/context/relationship semantic touched by this correction).

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, Chapter 8 §8.1.1/§8.2/§8.5 (Locked, byte-for-byte unchanged), `execution-intent.md` v0.2 Draft §6a (byte-for-byte unchanged, verified), `risk.md` v0.3 Draft (byte-for-byte unchanged, verified), `decision.md` v0.3 Draft (byte-for-byte unchanged, verified), `trade-intent.md` v0.2 Draft (byte-for-byte unchanged, verified), Package 0.2-C1/C2/C3/C4/C5 (all `Consolidated Stable`, byte-for-byte unchanged, verified).

### Author self-review

While correcting §6 (`OrderSubmissionRequested`) invariants for `C6-MAJ-02`, noticed and fixed a pre-existing dangling citation (`§6a`, which does not exist in `order.md` — the actual submission-eligibility rule lives at `§8a`) on the `OrderStatusChanged` invariant list (§5) — a v0.1 authoring bug adjacent to text already being touched by this correction, fixed as a minimal citation correction (not new semantics). All lettered scenario cross-references (A–O) renumbered to 1–24 and re-verified via grep — no stale letter reference remains. All 11 YAML fenced blocks re-validated via `yaml.safe_load`. No finding blocking khác found.

### Changed-file scope

```text
docs/domain/order.md          MODIFIED v0.1 → v0.2   blob 94ec87593834362292dc3379068e99ef12d86412
docs/domain/README.md         MODIFIED v0.46 → v0.47   blob 6e53f725c749cb9bfff2473afcd2c5af76b29481
docs/MANIFEST.md              MODIFIED manifest_version 9.72 → 9.73
docs/CHANGELOG.md             MODIFIED (this entry)
docs/domain/context-map.yaml     KHÔNG ĐỔI — blob d87428e9919005a2cd7f7b282c92f710e5aed382, verified byte-identical
docs/domain/risk.md              KHÔNG ĐỔI — blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab, verified byte-identical
docs/domain/execution-intent.md  KHÔNG ĐỔI — blob afc0c1fe7bdd2f285403dff29c71849ab66af70c, verified byte-identical
docs/domain/decision.md          KHÔNG ĐỔI — blob e2a26320200d350ace3da0247235bb14cef12509, verified byte-identical
docs/domain/trade-intent.md      KHÔNG ĐỔI — blob e7a306abc53ba482ff1249af1dda2829c4c82fa7, verified byte-identical
```

### Metadata / state

- `order.md`: **v0.1 → v0.2**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `context-map.yaml`: **không đổi** — version giữ `0.18`, blob giữ nguyên.
- `README.md` (domain index): **v0.46 → v0.47**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.72 → 9.73**.
- `risk.md`, `execution-intent.md`, `decision.md`, `trade-intent.md`: **không đổi** (byte-for-byte, verified) — forbidden scope, không sửa.
- `ADR-010.md`, `ADR-012.md`, `ADR-013.md`, `instrument.md`, `venue.md`, `account.md`, `strategy.md`: **không đổi** (byte-for-byte, verified).
- Mọi ADR khác, Constitution, mọi Domain Contract khác: **không đổi.**

**Package 0.2-C6 VẪN CHƯA đạt `Consolidated Stable` — chờ bounded delta review (ChatGPT + Independent Review B) trên cùng exact baseline correction này.** Mandatory sequence tiếp tục: ChatGPT delta review → Independent Review B delta review → Product Owner consolidation decision. KHÔNG correction thêm dựa trên một review đơn lẻ. Package 0.2-C1/C2/C3/C4/C5 vẫn `Consolidated Stable`, không đổi. Package 0.2-C7 vẫn chưa authorize, chưa author, chưa authored. KHÔNG Fill/Position semantics nào được author. Không artifact nào Approved hay Locked. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-31 — author Package 0.2-C6 order foundation

**Package 0.2-C6 — Order Foundation v0.1 authored.** Vai trò: `Domain Contract Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C6: Order Foundation v0.1". Authorized artifact: `docs/domain/order.md` (tạo mới, v0.1 Draft). Authorization này **không** cho phép author Fill/Position/Replay Event (Package 0.2-C7), định nghĩa partial fill/venue acceptance/rejection/external order ID/exchange API payload/routing/adapter behavior, Limit/Stop/advanced order type, TIF/IOC/FOK/post_only/reduce_only, fees/slippage/accounting, margin/leverage/liquidation model, resize/clamp/round Risk-approved quantity, Live behavior, sửa `execution-intent.md`/`risk.md`/`decision.md`/`trade-intent.md`/C1–C5/bất kỳ ADR nào/Constitution, đóng OQ-002/OQ-003, Approve/Lock/Consolidate bất kỳ artifact/package nào, hay authorize Live.

### Baseline verification

```text
Expected HEAD:  042024f7ad22f6032d9f9d5d9370da60ae08e889
Actual HEAD:    042024f7ad22f6032d9f9d5d9370da60ae08e889  — match

Package 0.2-C1:  Consolidated Stable (không đổi)
Package 0.2-C2:  Consolidated Stable (không đổi)
Package 0.2-C3:  Consolidated Stable (không đổi)
Package 0.2-C4:  Consolidated Stable (không đổi)
Package 0.2-C5:  Consolidated Stable (không đổi)
risk.md:              v0.3 Draft, blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab
execution-intent.md:  v0.2 Draft, blob afc0c1fe7bdd2f285403dff29c71849ab66af70c
context-map.yaml:     v0.17 Draft, blob 59f11a2cee142c533280a33060c21f69f3fc50cf
order.md: absent trước transaction — đúng expected state, KHÔNG có baseline conflict
```

### Order identity and logical creation key

`order_id` — opaque, globally unique, immutable, gán tại `OrderCreated`. Logical creation key = `originating_execution_intent_id` (order.md §1) — KHÔNG cursor component (khác pattern `(trade_intent_id, risk_context_cursor)` của RiskEvaluation), vì `eligible_for_new_order_creation` (execution-intent.md §6a) tự nó đã pin đúng một Execution Intent tại một thời điểm — một Execution Intent eligible → zero hoặc một Order (visible-valid-head). `OrderCreationAttempt` (kind: entity, order.md §3) — subject RIÊNG, `order_creation_attempt_id` (identity cá nhân) TÁCH BIỆT khỏi logical creation key — ÁP DỤNG CHỦ ĐỘNG (KHÔNG chờ review round phát hiện) bốn bài học đã trả giá qua C4/C5's các vòng correction: (1) KHÔNG circular reference giữa Attempt và Order — Attempt KHÔNG mang field trỏ tới Order, chỉ `OrderCreated.causation_refs` trỏ ngược lại attempt (one-way sequence); (2) idempotency scoped theo `order_creation_attempt_id`, KHÔNG theo logical creation key — nhiều attempt (kể cả outcome khác nhau) CÓ THỂ chia sẻ cùng key; (3) `attempt_outcome = CREATED` CHỈ ghi SAU KHI bounded Order payload computation đã hoàn tất trọn vẹn — đóng trước lớp lỗi `C5-MAJ-01`-style, ngay từ v0.1; (4) `FAILED_BEFORE_CREATION` tường minh RETRYABLE, không permanently block same-origin recovery.

### Order creation Attempt model

`attempt_outcome ∈ {CREATED, INELIGIBLE, FAILED_BEFORE_CREATION}` (order.md §3) — mọi lần thử ĐỀU ghi nhận (`OrderCreationAttemptRecorded`), KHÔNG absence-based. `CREATED`: reason_code/checked_evidence_refs tuyệt đối absent, evidence đầy đủ sống trên `OrderCreated`. `INELIGIBLE`: reason_code = `EXECUTION_INTENT_INELIGIBLE`. `FAILED_BEFORE_CREATION`: reason_code = `ORDER_ENGINE_COMPUTATION_BOUNDARY_ERROR`, retryable. Recoverable append gap (đối xứng "no unstated cross-stream atomicity" đã proven, risk.md §2): crash sau Attempt CREATED nhưng trước `OrderCreated` là trạng thái BÌNH THƯỜNG — recovery re-run cùng computation, tái sử dụng attempt CREATED đã tồn tại (KHÔNG tạo attempt mới), append/reuse đúng một `OrderCreated` (order.md §4a).

### Execution Intent eligibility integration

`OrderCreated` CHỈ được phát khi `eligible_for_new_order_creation(originating_execution_intent_id, order_context_cursor) == true` (execution-intent.md §6a, KHÔNG sửa, KHÔNG duplicate/weaken) — false → `OrderCreationAttemptRecorded(attempt_outcome=INELIGIBLE, reason_code=EXECUTION_INTENT_INELIGIBLE)`, KHÔNG Order nào phát (Scenario B, order.md §17). Rule đầy đủ năm điều kiện transitive (execution-intent.md §6a, C5-MAJ-06) resolve TRỰC TIẾP từ authoritative event stream TẠI `order_context_cursor` — KHÔNG dùng `ExecutionIntentCurrentView` latest-state làm input.

### Order scope and origin preservation

`account_id`/`instrument_selection_ref`/`direction`/`quantity`/`quantity_unit`/origin ID (order.md §1) PHẢI khớp CHÍNH XÁC origin chain của Execution Intent gốc — Order KHÔNG được tự chọn khác. `quantity` PHẢI finite, strictly positive, CHÍNH XÁC bằng `approved_quantity` gốc — KHÔNG resize/clamp/round lại Risk-approved quantity dưới bất kỳ hình thức nào (Scenario F/G, §17).

### Order type boundary

v0.1 pin ba giá trị đơn, KHÔNG mở rộng: `order_action = OPEN_EXPOSURE`, `order_type = MARKET`, `environment = PAPER`. Order KHÔNG chứa `limit_price`/`stop_price`/`time_in_force`/`post_only`/`reduce_only`/IOC/FOK/venue-specific flags/exchange payload. Reference price CHỦ ĐỘNG OMIT ở v0.1 (order.md §15, disclosed judgment call) — Order không tự tính toán gì nên không cần một reference price để deterministic; nếu Phase 1 cần, thêm qua correction riêng.

### Lifecycle model

Năm state tối thiểu: `UNSEEN → CREATED → SUBMISSION_REQUESTED`; `CREATED → WITHDRAWN/EXPIRED`; `SUBMISSION_REQUESTED → WITHDRAWN/EXPIRED` (order.md §1 state_machine). `WITHDRAWN`/`EXPIRED` terminal CHO FORWARD TRANSITION nhưng correctable append-only — `supersedes_fact_ref` có mặt ngay từ v0.1 trên `OrderStatusChanged` (đóng trước lớp lỗi `C2-MAJ-02`/`C3-MAJ-02`-style). KHÔNG author `SUBMITTED`/`ACCEPTED`/`REJECTED_BY_VENUE`/`PARTIALLY_FILLED`/`FILLED`/`CANCELLED_BY_VENUE`.

### Submission-request model

`OrderSubmissionRequested` (order.md §6) — `submission_request_id` opaque per-fact identity, gán tại event này; derivation/idempotency key = `order_id` (KHÔNG một individual submission-attempt identity riêng — walking skeleton v0.1 không cần). `target_environment = PAPER` bắt buộc. Semantics: Ride yêu cầu gửi một Order hợp lệ tới bounded PAPER execution boundary — KHÔNG chứng minh boundary đã accept, venue đã acknowledge, external order ID tồn tại, execution đã xảy ra, hay Fill tồn tại.

### Creation and submission idempotency

Creation: `order_creation_derivation_idempotency_policy: ONE_VALID_ORDER_PER_ORIGINATING_EXECUTION_INTENT` (order.md §11) — same origin + same payload → idempotent reuse; same origin + changed payload (chưa invalidate predecessor) → deterministic conflict. Submission: `order_submission_idempotency_policy: STABLE_ORDER_ID_SAME_PAYLOAD_IS_IDEMPOTENT` — same `order_id` + same submission payload → idempotent reuse; same `order_id` + changed payload → deterministic conflict (Scenario E/I, §17). KHÔNG cross-stream atomicity yêu cầu ở cả hai layer.

### Correction/replay model

`OrderCreated` — correction lineage CHUẨN, đối xứng `RiskEvaluationRecorded` (risk.md §10, KHÔNG đối xứng `ExecutionIntentIssued`'s invalidate-only): `order_id` bất biến per-fact, logical creation key CÓ THỂ nhận `OrderCreated` MỚI (`order_id` khác) sau khi predecessor invalidate, `supersedes_fact_ref`, một visible-valid-head, replay trước thấy O1/replay sau thấy O2, O1 vẫn historically resolvable, prior submission requests remain historical, O1 ineligible cho submission mới, O2 có thể nhận submission riêng (order.md §9, Scenario L/M, §17). `OrderStatusChanged` — correction lineage chuẩn, same-slice replacement, đối xứng `execution-intent.md` §8.

### Future C7 eligibility boundary

`eligible_for_execution_result_processing(order_id, C)` (order.md §8b) — visible-valid-head + origin chain vẫn valid + `OrderSubmissionRequested` VALID tồn tại + `current_status` KHÔNG withdrawn/expired. Nghĩa CHỈ là: C7 (chưa author) CÓ THỂ xử lý một execution result tương lai — KHÔNG có nghĩa Fill tồn tại, execution thành công, quantity filled, hay venue đã accept (Scenario O, §17).

### Time/cursor semantics

`order_context_cursor`/`submission_context_cursor` TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1 Replay Cursor shape như PAYLOAD field. `ExecutionIntentIssued.effective_time <= OrderCreated.order_effective_time`; `ExecutionIntentIssued.recorded_time < OrderCreated.recorded_time`; `OrderCreated.recorded_time < OrderSubmissionRequested.recorded_time` — strict causal ordering (Scenario N, §17). Mọi authoritative fact PHẢI thỏa `fact.recorded_time <= cursor.recorded_time <= event.recorded_time`.

### Context Map integration

Đăng ký capability `execution-management` / context `order-management` MỚI (`owned_contracts: [order]`) tại `context-map.yaml` **v0.17 → v0.18**. MỘT relationship edge MỚI: `risk-gateway` (execution-intent) → `order-management` (order), `relationship_type: published_language`, `contract_id: execution-intent-issued` — Order thực sự tiêu thụ published-language fact này (subject_ref/scope copy + causation_refs trace-back) VÀ `eligible_for_new_order_creation` rule, khác precedent `risk-gateway`/`strategy-decision` (KHÔNG edge, chỉ opaque `ref:` lookup).

### Acceptance-scenario results (order.md §17, Scenario A–O)

Scenario A (eligible creation) — pass. Scenario B (ineligible Execution Intent) — pass. Scenario C (failure and retry) — pass. Scenario D (crash after successful Attempt) — pass. Scenario E (creation idempotency) — pass. Scenario F (scope mismatch, reject) — pass. Scenario G (zero quantity, invalid) — pass. Scenario H (submission request) — pass. Scenario I (duplicate submission request) — pass. Scenario J (withdrawn/expired, no new submission) — pass. Scenario K (origin invalidated) — pass. Scenario L (Order correction) — pass. Scenario M (invalidated Order with prior submission) — pass. Scenario N (time ordering) — pass. Scenario O (C7 boundary, no Fill authored) — pass.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, Chapter 8 §8.1.1/§8.2/§8.5 (Locked, byte-for-byte unchanged), `execution-intent.md` v0.2 Draft §6a (byte-for-byte unchanged, verified), `risk.md` v0.3 Draft (byte-for-byte unchanged, verified), `decision.md` v0.3 Draft (byte-for-byte unchanged, verified), `trade-intent.md` v0.2 Draft (byte-for-byte unchanged, verified), Package 0.2-C1/C2/C3/C4/C5 (all `Consolidated Stable`, byte-for-byte unchanged, verified).

### Author self-review

Reference price cho PAPER simulation evidence CHỦ ĐỘNG OMIT (order.md §15, disclosed judgment call) — task cho phép pin CHỈ khi "strictly necessary"; Order không tự tính toán gì (quantity copy nguyên vẹn từ Execution Intent, không có sizing computation), nên không cần. Individual submission-attempt identity riêng (tách biệt `submission_request_id` khỏi `order_id` derivation key) CHỦ ĐỘNG KHÔNG thêm — `order_id` đủ làm derivation key cho walking skeleton v0.1, `submission_request_id` chỉ là per-fact identity. Tất cả 11 YAML fenced block trong `order.md` parse qua `yaml.safe_load` — verified. Tất cả `§N` citation cross-reference verified qua grep — không có tham chiếu treo. Không tìm thấy finding blocking nào khác (author self-review — chưa qua Review A/B).

### Changed-file scope

```text
docs/domain/order.md          NEW v0.1 Draft   blob 912d9b6a779187f287803f2a70c1cc642bb04a4e
docs/domain/context-map.yaml  MODIFIED v0.17 → v0.18   blob d87428e9919005a2cd7f7b282c92f710e5aed382
docs/domain/README.md         MODIFIED v0.45 → v0.46   blob 31b26991a6ef3adae4af1fe558b2d2214e0e61a4
docs/MANIFEST.md              MODIFIED manifest_version 9.71 → 9.72
docs/CHANGELOG.md             MODIFIED (this entry)
docs/domain/risk.md              KHÔNG ĐỔI — blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab, verified byte-identical
docs/domain/execution-intent.md  KHÔNG ĐỔI — blob afc0c1fe7bdd2f285403dff29c71849ab66af70c, verified byte-identical
docs/domain/decision.md          KHÔNG ĐỔI — blob e2a26320200d350ace3da0247235bb14cef12509, verified byte-identical
docs/domain/trade-intent.md      KHÔNG ĐỔI — blob e7a306abc53ba482ff1249af1dda2829c4c82fa7, verified byte-identical
```

### Metadata / state

- `order.md`: **NEW**, `version: "0.1"`, `status: Draft`, `approved_by: null`, `approved_at: null`.
- `context-map.yaml`: **v0.17 → v0.18** — capability `execution-management`/context `order-management` MỚI, một relationship edge MỚI.
- `README.md` (domain index): **v0.45 → v0.46**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.71 → 9.72**.
- `risk.md`, `execution-intent.md`, `decision.md`, `trade-intent.md`: **không đổi** (byte-for-byte, verified).
- `ADR-010.md`, `ADR-012.md`, `ADR-013.md`, `instrument.md`, `venue.md`, `account.md`, `strategy.md`: **không đổi** (byte-for-byte, verified).
- Mọi ADR khác, Constitution, mọi Domain Contract khác: **không đổi.**

**Package 0.2-C6 CHƯA đạt `Consolidated Stable` — chờ Review A + Independent Review B trên cùng exact baseline này.** Mandatory sequence: Author baseline → ChatGPT Review A → Independent Review B (cùng exact baseline) → merge finding → một correction commit được Product Owner authorize → ChatGPT delta review → Independent Review B delta review → Product Owner consolidation decision. **KHÔNG correction dựa trên một review đơn lẻ.** Package 0.2-C1/C2/C3/C4/C5 vẫn `Consolidated Stable`, không đổi. Package 0.2-C7 vẫn chưa authorize, chưa author. KHÔNG Fill/Position semantics nào được author. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-31 — consolidate Package 0.2-C5

**Package 0.2-C5 Risk Gateway and Execution Intent Foundation consolidated as `Consolidated Stable`.** Vai trò: `Package Lifecycle Consolidation Author · Repository Transaction Executor`. Product Owner authorized: "Package 0.2-C5: Consolidated Stable" (2026-07-31). Authorization này cho phép ghi Package 0.2-C5 vào lifecycle state `Consolidated Stable` — nó KHÔNG cho phép Approve/Lock `risk.md`/`execution-intent.md`, không sửa `decision.md`/`trade-intent.md`/`context-map.yaml`/bất kỳ ADR nào, không sửa Constitution, không đóng OQ, không authorize Live, không author/authorize Package 0.2-C6–C7, không thêm speculative edge case, không tuyên bố Phase 0.2 hoàn thành.

### Baseline verification

```text
Expected HEAD:  55b9cb842de91825a7335a6563c35a690c926fe4
Actual HEAD:    55b9cb842de91825a7335a6563c35a690c926fe4  — match

risk.md:              v0.3 Draft, blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab  — match
execution-intent.md:  v0.2 Draft, blob afc0c1fe7bdd2f285403dff29c71849ab66af70c  — match
context-map.yaml:     v0.17 Draft, blob 59f11a2cee142c533280a33060c21f69f3fc50cf  — match
README.md:            v0.44 Draft, blob b6a52f819241c00554e9f334ad296441f8b4c7be  — match
MANIFEST.md:           manifest_version 9.70  — match
```

### Product Owner authorization recorded

```text
Package 0.2-C5:
  Consolidated Stable
```

Meaning: the exact reviewed C5 baseline is stable enough to serve as the dependency baseline for Package 0.2-C6. It does not mean any artifact is Approved or Locked.

### Exact reviewed baseline pinned

```text
Package 0.2-C5 reviewed HEAD:  55b9cb842de91825a7335a6563c35a690c926fe4

Primary artifacts:       risk.md v0.3 Draft, blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab
                          execution-intent.md v0.2 Draft, blob afc0c1fe7bdd2f285403dff29c71849ab66af70c
Integration artifact:    context-map.yaml v0.17 Draft, blob 59f11a2cee142c533280a33060c21f69f3fc50cf (unchanged)
Registry baseline:       MANIFEST v9.70
```

### Review evidence

```text
ChatGPT final focused delta review:        Clean — Blocker 0, Major 0, Minor 0
Independent Focused Delta Review B:        Clean — Blocker 0, Major 0, Minor 0
```

### Complete finding ledger — all resolved (v0.1 → v0.2 bounded correction, v0.2 → v0.3 micro-correction)

```text
C5-MAJ-01:        Resolved (truthful Attempt EVALUATED ordering — computation completes before Attempt EVALUATED, recoverable append gap)
C5-MAJ-02:        Resolved (evidence_availability seven fixed keys, all ref/scalar evidence fields conditional)
C5-MAJ-03:        Resolved (bounded v0.1 unit model, currency/unit mismatch → NON_EVALUABLE/INCOMPATIBLE_EVIDENCE_UNIT)
C5-MAJ-04:        Resolved (approved_quantity strictly positive after floor-rounding, QUANTITY_ROUNDS_TO_ZERO)
C5-MAJ-05:        Resolved (numeric domain constraints pinned, quantity_precision maximum = 18 disclosed)
C5-MAJ-06:        Resolved (eligible_for_new_order_creation expanded to five transitive AND-conditions)
C5-DELTA-MAJ-01:   Resolved (evidence availability separated from unit compatibility, two mutually exclusive NON_EVALUABLE branches)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

### Package lifecycle meaning

`Consolidated Stable` là package lifecycle/readiness state — nghĩa là: reviewed package baseline nội bộ coherent; mọi qualifying finding đã resolved; deferred limitations được ghi nhận tường minh là non-blocking Phase 1 concern; package integration đủ ổn định để làm dependency baseline cho package kế tiếp (0.2-C6). Nó KHÔNG có nghĩa: artifact Approved; artifact Locked; ADR thay đổi; Domain Contract bất biến; OQ closure; Phase completion; implementation authorization; Live authorization.

### Confirmation — `risk.md`, `execution-intent.md`, `context-map.yaml` byte-identical

```text
docs/domain/risk.md              blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab — verified byte-identical to reviewed baseline
docs/domain/execution-intent.md  blob afc0c1fe7bdd2f285403dff29c71849ab66af70c — verified byte-identical to reviewed baseline
docs/domain/context-map.yaml     blob 59f11a2cee142c533280a33060c21f69f3fc50cf — verified byte-identical to reviewed baseline
```

### Unchanged artifact statuses

`risk.md`: **giữ nguyên** `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte — không sửa Domain Contract semantic trong transaction này. `execution-intent.md`: **giữ nguyên** `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte. `context-map.yaml`: **giữ nguyên** `version: "0.17"`, `status: Draft`, byte-for-byte — không sửa. `decision.md`/`trade-intent.md`: **giữ nguyên**, byte-for-byte — không sửa. Mọi C1–C4 Domain Contract (`instrument.md`/`venue.md`/`account.md`/`strategy.md`) và mọi ADR: **giữ nguyên**, byte-for-byte — không sửa.

### Package lifecycle states pinned

```text
Package 0.2-C1:     Consolidated Stable
Package 0.2-C2:     Consolidated Stable
Package 0.2-C3:     Consolidated Stable
Package 0.2-C4:     Consolidated Stable
Package 0.2-C5:     Consolidated Stable
Package 0.2-C6–C7:  unauthorized, unauthored
```

### Artifact lifecycle states pinned

```text
risk.md:              Draft, version "0.3", approved_by: null, approved_at: null, not Locked
execution-intent.md:  Draft, version "0.2", approved_by: null, approved_at: null, not Locked
```

### Changed-file scope

```text
docs/domain/README.md            MODIFIED v0.44 → v0.45
docs/MANIFEST.md                 MODIFIED manifest_version 9.70 → 9.71
docs/CHANGELOG.md                MODIFIED (this entry)
docs/domain/risk.md              KHÔNG ĐỔI — blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab, verified byte-identical
docs/domain/execution-intent.md  KHÔNG ĐỔI — blob afc0c1fe7bdd2f285403dff29c71849ab66af70c, verified byte-identical
docs/domain/context-map.yaml     KHÔNG ĐỔI — blob 59f11a2cee142c533280a33060c21f69f3fc50cf, verified byte-identical
docs/domain/decision.md          KHÔNG ĐỔI — blob e2a26320200d350ace3da0247235bb14cef12509, verified byte-identical
docs/domain/trade-intent.md      KHÔNG ĐỔI — blob e7a306abc53ba482ff1249af1dda2829c4c82fa7, verified byte-identical
```

### Metadata / state

- `risk.md`, `execution-intent.md`, `context-map.yaml`, `decision.md`, `trade-intent.md`: **không đổi** (semantic và version) — package lifecycle metadata only.
- `README.md` (domain index): **v0.44 → v0.45**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.70 → 9.71**; dòng `domain/` cập nhật ghi nhận Package 0.2-C5 `Consolidated Stable`.
- Mọi Domain Contract khác (`instrument.md`, `venue.md`, `account.md`, `strategy.md`, `candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, `context.md`), mọi ADR file, Constitution: **không đổi.**

**Package 0.2-C6 baseline dependency đã thỏa, eligible cho Product Owner scope authorization — CHƯA bắt đầu, CHƯA author, KHÔNG được authorize bởi transaction này.** Package 0.2-C7 gate chưa mở. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-31 — separate C5 evidence compatibility

**Package 0.2-C5 micro-correction — evidence availability versus unit compatibility only.** Vai trò: `Domain Contract Micro-Correction Author`. Product Owner authorized: "Package 0.2-C5 micro-correction — evidence availability versus unit compatibility only." Đóng đúng một finding Major: `C5-DELTA-MAJ-01` (evidence availability and unit compatibility were conflated into a single enum, making `INCOMPATIBLE_UNIT` unreachable by the actual algorithm and contradicting the NON_EVALUABLE result invariant). Authorization này **không** cho phép reopen bất kỳ C5 design area nào khác, thêm general unit framework, FX conversion, signed/net exposure, thay đổi sizing semantics, numeric bounds, positive quantity rules, C6 eligibility, sửa C1–C4/ADR/Constitution, author Order/Fill/Position, authorize C6–C7, Approve/Lock/Consolidate C5, đóng OQ-002/OQ-003, hay authorize Live.

### Baseline verification

```text
Expected HEAD:  303c2a0c682892034bba6bc386d7d0512b91aa29
Actual HEAD:    303c2a0c682892034bba6bc386d7d0512b91aa29  — match

risk.md:              v0.2 Draft, blob a08f94851014bce5da51d98781fd9253d026fc34  — match
execution-intent.md:  v0.2 Draft, blob afc0c1fe7bdd2f285403dff29c71849ab66af70c  — match
context-map.yaml:     v0.16 Draft, blob 87e0411d1270ceacd4eb20e76340911900dedaad  — match
```

### Finding-resolution statement

`C5-DELTA-MAJ-01` — resolved. The v0.2 `evidence_availability` enum (§5b2) carried five values (`AVAILABLE`/`MISSING`/`INVALID`/`UNRESOLVABLE`/`INCOMPATIBLE_UNIT`), conflating evidence *existence* with evidence *compatibility*. The actual v0.2 algorithm never legally produced `INCOMPATIBLE_UNIT`: unit comparison (§5c step 5) only ran after all seven keys were confirmed `AVAILABLE` (step 4 already stopped otherwise), so a unit mismatch always occurred while every key was `AVAILABLE` — directly contradicting the pinned invariant "`result = NON_EVALUABLE` ⟺ at least one key != `AVAILABLE`". `evidence_availability` and unit/currency compatibility are now two separate concepts: availability lives in `evidence_availability` (§5b2, four values), compatibility lives in the existing `unit_evidence` invariant (§5b1).

### Corrected availability enum

```yaml
evidence_availability:
  <all seven keys>: {type: enum, values: [AVAILABLE, MISSING, INVALID, UNRESOLVABLE], required: true}
```

`INCOMPATIBLE_UNIT` removed from all seven keys. Conditional-presence rule unchanged: `AVAILABLE` → corresponding ref/value required; not `AVAILABLE` → ref/value absent, no placeholder/null/sentinel.

### Corrected NON_EVALUABLE branches

```text
result = NON_EVALUABLE ⟺ exactly one of two mutually exclusive branches:

Branch A — Availability failure: at least one required evidence key != AVAILABLE
  → reason ∈ {REQUIRED_EVIDENCE_UNAVAILABLE, RISK_POLICY_EVIDENCE_UNAVAILABLE}
  → unit comparison does not run
  → unavailable field's ref/value absent; other AVAILABLE keys' evidence may remain present

Branch B — Compatibility failure: ALL evidence required for unit comparison is AVAILABLE
  → exact refs, values, and unit metadata present
  → unit equality invariant (§5b1) fails
  → reason = INCOMPATIBLE_EVIDENCE_UNIT (only value valid for this branch)
  → all resolved refs/values/unit metadata remain present (evidence exists, was used to detect
    incompatibility)
```

No reason code crosses branches.

### Corrected unit-mismatch serialization

When Branch B fires, `evidence_availability` for every one of the seven keys reads `AVAILABLE` — there is no availability key that reads anything else. `unit_evidence` (§5b1), `risk_evidence` (§5b3), and `evidence_facts` (§5d) all carry their normal, fully-resolved refs/values; only `result = NON_EVALUABLE` and `rejection_reason = INCOMPATIBLE_EVIDENCE_UNIT` distinguish this from a would-be `APPROVED`/`REJECTED` outcome.

### Deterministic precedence

Algorithm ordering (risk.md §5c) unchanged — it was already correct: (1) Trade Intent eligibility; (2)–(3) resolve risk evidence axes + evidence facts + unit evidence, writing `evidence_availability`; (4) **Branch A gate** — any key != `AVAILABLE` → `NON_EVALUABLE`, availability-specific reason, STOP (unit comparison never runs); (5) **Branch B gate** — reached only when all seven keys are `AVAILABLE`; unit compatibility check → `NON_EVALUABLE`/`INCOMPATIBLE_EVIDENCE_UNIT`, STOP; (6) numeric-domain validation; (7)–(13) unchanged threshold/sizing steps. Branch A always precedes Branch B and the two are mutually exclusive by construction — no reordering was needed, only the enum and the result invariant text.

### Acceptance-scenario results (risk.md §17, nineteen scenarios — Scenario 19 new)

Scenario 1 (missing equity, Branch A) — pass. Scenario 2 (unresolved policy configuration, Branch A) — pass. Scenario 3 (unit mismatch, equity USD vs listing USDT, Branch B, all seven keys AVAILABLE) — pass. Scenario 4 (price base mismatch, reference price ETH vs quantity_unit BTC, Branch B, all seven keys AVAILABLE) — pass, new Scenario 19. Scenario 5 (fully compatible, all currencies USDT, quantity_unit BTC) — pass, continues to numeric-domain and policy checks unchanged.

### Regression check

Truthful Attempt ordering (§2/§4/§5a), Attempt identity/idempotency (§2/§12), Risk Evaluation identity (§1), logical computation key, correction lineage (§10), replay semantics, numeric-domain constraints (§5c step 6), quantity precision 0–18, positive quantity rule (§5c step 12–13/§5e), sizing formula, Risk-to-Execution-Intent derivation (§9), Execution Intent lifecycle, C6 eligibility chain (execution-intent.md §6a), no-look-ahead (§5d), C1–C4 semantics, C5/C6 boundary — **tất cả không đổi, verified**. `execution-intent.md` blob giữ nguyên byte-for-byte — không có cross-reference nào cần sửa (verified qua grep, không tham chiếu `evidence_availability`/`INCOMPATIBLE_UNIT` nào trong file).

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, Chapter 8 §8.1.1/§8.2/§8.5 (Locked, byte-for-byte unchanged), Chapter 9 §9.1 (Locked, byte-for-byte unchanged), `trade-intent.md` v0.2 Draft (byte-for-byte unchanged, verified), `decision.md` v0.3 Draft (byte-for-byte unchanged, verified), Package 0.2-C1/C2/C3/C4 (all `Consolidated Stable`, byte-for-byte unchanged, verified). `context-map.yaml` metadata-only bump (owned-contract version comment).

### Changed-file scope

```text
docs/domain/risk.md              MODIFIED v0.2 → v0.3   blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab
docs/domain/context-map.yaml     MODIFIED v0.16 → v0.17 blob 59f11a2cee142c533280a33060c21f69f3fc50cf
docs/domain/README.md            MODIFIED v0.43 → v0.44 blob b6a52f819241c00554e9f334ad296441f8b4c7be
docs/MANIFEST.md                 MODIFIED manifest_version 9.69 → 9.70
docs/CHANGELOG.md                MODIFIED (this entry)
docs/domain/execution-intent.md  KHÔNG ĐỔI — blob afc0c1fe7bdd2f285403dff29c71849ab66af70c, verified byte-identical
docs/domain/decision.md          KHÔNG ĐỔI — blob e2a26320200d350ace3da0247235bb14cef12509, verified byte-identical
docs/domain/trade-intent.md      KHÔNG ĐỔI — blob e7a306abc53ba482ff1249af1dda2829c4c82fa7, verified byte-identical
```

### Author self-review

Grepped every remaining occurrence of `INCOMPATIBLE_UNIT` after the edit — only two survive, both intentional: the explanatory v0.3 micro-correction prose paragraph (describing what was removed and why) and the historical v0.2 bounded-correction summary paragraph (left byte-for-byte as a record of that transaction, matching the precedent set by `decision.md`'s C4-DELTA micro-correction, which likewise preserved its v0.2 paragraph unedited and appended a new v0.3 paragraph rather than rewriting history). `INCOMPATIBLE_EVIDENCE_UNIT` (the `rejection_reason` value, a distinct token) is untouched and remains the sole reason for Branch B. All sixteen YAML fenced blocks in `risk.md` re-validated via `yaml.safe_load` after the edit. Confirmed `execution-intent.md` contains zero references to `evidence_availability`/`INCOMPATIBLE_UNIT`, so its blob was correctly left untouched per the task's "prefer preserving its blob" instruction. No finding blocking khác found.

### Metadata / state

- `risk.md`: **v0.2 → v0.3**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `execution-intent.md`: **không đổi** — version giữ `0.2`, blob giữ nguyên.
- `context-map.yaml`: **v0.16 → v0.17**, metadata-only (owned-contract version comment).
- `README.md` (domain index): **v0.43 → v0.44**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.69 → 9.70**.
- `decision.md`, `trade-intent.md`: **không đổi** (byte-for-byte, verified) — forbidden scope, không sửa.
- `ADR-010.md`, `ADR-012.md`, `ADR-013.md`, `instrument.md`, `venue.md`, `account.md`, `strategy.md`: **không đổi** (byte-for-byte, verified).
- Mọi ADR khác, Constitution, mọi Domain Contract khác: **không đổi.**

**Package 0.2-C5 VẪN CHƯA đạt `Consolidated Stable` — chờ focused delta re-review (ChatGPT + Independent Review B) trên cùng exact baseline micro-correction này.** Mandatory sequence tiếp tục: focused delta re-review → Product Owner consolidation decision. KHÔNG correction thêm dựa trên một review đơn lẻ. Risk và Execution Intent vẫn là HAI concept riêng biệt, KHÔNG gộp. Package 0.2-C1/C2/C3/C4 vẫn `Consolidated Stable`, không đổi. Package 0.2-C6–C7 vẫn chưa authorize, chưa author. Không artifact nào Approved hay Locked. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-31 — correct Package 0.2-C5 risk evidence

**Package 0.2-C5 bounded correction — consolidated Review A + Independent Review B findings.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C5 bounded correction — consolidated Review A + Independent Review B findings." Đóng đúng sáu finding Major: `C5-MAJ-01` (truthful Risk Attempt completion order), `C5-MAJ-02` (executable NON_EVALUABLE payload via `evidence_availability`), `C5-MAJ-03` (currency and unit compatibility), `C5-MAJ-04` (strictly positive approved quantity), `C5-MAJ-05` (numeric input domains and precision bounds), `C5-MAJ-06` (complete future C6 origin-chain eligibility). Authorization này **không** cho phép author Package 0.2-C6–C7, định nghĩa order type/limit price/stop price/exchange payload/routing/adapter behavior, thêm FX conversion/signed exposure arithmetic/portfolio optimization/leverage/liquidation/margin model, author Order/Fill/Position, thêm exchange precision table/general unit framework/general Risk DSL, authorize C6–C7, Approve/Lock/Consolidate C5, đóng OQ-002/OQ-003, hay authorize Live. Sửa `decision.md`/`trade-intent.md`/bất kỳ ADR nào/Constitution cũng KHÔNG được phép.

### Baseline verification

```text
Expected HEAD:  9e838483ae6db3fe28f5c55154b35075e22922dd
Actual HEAD:    9e838483ae6db3fe28f5c55154b35075e22922dd  — match

risk.md:              v0.1 Draft, blob fa8070b0c6a710f39bdb9dd27915076d4b36d0c2  — match
execution-intent.md:  v0.1 Draft, blob c5cb23012a4bec7517803d9f47ac0df6b0955801  — match
context-map.yaml:     v0.15 Draft, blob ac69487f929756cd913d6e8c1df5c9712b3768ae  — match
README.md:            v0.42 Draft, blob 8bcd1841624d556be762741059560061406070f8  — match
MANIFEST.md:           manifest_version "9.68", blob 47a32d641f33afe0f0548a1022f41724b1df94d7  — match
decision.md:          v0.3 Draft, blob e2a26320200d350ace3da0247235bb14cef12509  — unchanged, forbidden scope
trade-intent.md:      v0.2 Draft, blob e7a306abc53ba482ff1249af1dda2829c4c82fa7  — unchanged, forbidden scope
```

### Six-finding resolution matrix

| Finding | Resolution |
|---|---|
| `C5-MAJ-01` | `RiskEvaluationAttemptRecorded(EVALUATED)` now written ONLY after bounded policy computation (§5c) completes in full — corrected order: computation completes → Attempt EVALUATED appended → `RiskEvaluationRecorded` appended referencing Attempt via `causation_refs`. Crash before completion leaves no EVALUATED attempt (either nothing recorded, retry gets a new `evaluation_attempt_id`, or `FAILED_BEFORE_EVALUATION` recorded). Crash after Attempt but before RiskEvaluation is a recoverable append gap — recovery re-runs the same deterministic computation and reuses the existing attempt id (risk.md §2/§4/§5a) |
| `C5-MAJ-02` | New `evidence_availability` block (risk.md §5b2) — seven fixed keys (`AVAILABLE_ACCOUNT_EQUITY`/`CURRENT_INSTRUMENT_EXPOSURE`/`REFERENCE_PRICE`/`RISK_POLICY_DEFINITION_VERSION`/`RISK_POLICY_CONFIGURATION_VERSION`/`RISK_PLUGIN_VERSION`/`PACKAGE_BUILD_ARTIFACT`), five fixed values (`AVAILABLE`/`MISSING`/`INVALID`/`UNRESOLVABLE`/`INCOMPATIBLE_UNIT`), always present. Risk evidence axes (§5b3) and evidence facts (§5d) become `required: false`, gated by the corresponding key — no fabricated ref/null/sentinel scalar when not AVAILABLE. Two new reason codes: `REQUIRED_EVIDENCE_UNAVAILABLE` (market/account evidence), `RISK_POLICY_EVIDENCE_UNAVAILABLE` (policy evidence axes) |
| `C5-MAJ-03` | New bounded v0.1 unit model (risk.md §5b1, `unit_evidence`) — `listing_quote_currency`/`budget_currency`/`equity_currency`/`exposure_notional_currency`/`reference_price_base_unit`/`reference_price_quote_currency`/`approved_notional_currency`/`quantity_unit`. Invariant: budget/equity/exposure-notional/reference-price-quote/approved-notional currencies all equal the TradableListing quote asset (string equality, no FX conversion); `reference_price_base_unit = quantity_unit`; `current_instrument_exposure_value` is non-negative gross quote-notional. Mismatch → `NON_EVALUABLE`/`INCOMPATIBLE_EVIDENCE_UNIT` (third new reason code) |
| `C5-MAJ-04` | `approved_quantity` now strictly positive (`> 0`) after floor-rounding on both `risk.md` (§5c step 12–13/§5e) and `execution-intent.md` (§1/§3 new invariants). `approved_quantity == 0` → `REJECTED`/`QUANTITY_ROUNDS_TO_ZERO`, `approved_quantity`/`approved_notional` absent, zero Execution Intent. No `OPEN_EXPOSURE` Execution Intent can carry zero quantity — enforced transitively because only `APPROVED` RiskEvaluation can be a valid `causation_refs` source |
| `C5-MAJ-05` | Exact numeric domains pinned per scalar (risk.md §5c/§6 step 6): `configured_risk_budget`/`max_requested_notional`/`reference_price_value` finite `> 0`; `available_account_equity_value`/`current_instrument_exposure_value` finite `>= 0`; `quantity_precision` integer `>= 0`, bounded maximum disclosed as `18` (no existing repository-wide precision bound found — v0.1 judgment call, §15 self-review). Out-of-domain scalar → `REJECTED`/`INVALID_SIZING_INPUT`, checked BEFORE the exposure cap so negative exposure can never bypass it |
| `C5-MAJ-06` | `eligible_for_new_order_creation` (execution-intent.md §6a) expanded from three to five AND-conditions: Execution Intent ISSUED; originating RiskEvaluation resolves to the visible-valid-head APPROVED for its logical key; that head is exactly the referenced `risk_evaluation_id`; RiskEvaluation references the same `trade_intent_id`; `eligible_for_new_risk_evaluation(trade_intent_id, C) == true`. Transitively chains Decision→Trade Intent→RiskEvaluation→Execution Intent validity — no Order semantics authored |

### Corrected Attempt ordering

`RiskEvaluationAttemptRecorded(attempt_outcome=EVALUATED)` is written ONLY after the full bounded policy computation (§5c, 13 steps) has completed — the resulting bundle (`trade_evidence`, `unit_evidence`, `evidence_availability`, `risk_evidence`, `sizing_evidence`, `evidence_facts`, `result`) is fully determined before EVALUATED is recorded. `RiskEvaluationRecorded` is appended immediately after, with `causation_refs` pointing to that exact attempt — one-way sequence, no atomic multi-event transaction across the three appends (risk.md §2/§4/§5a). Any result — `APPROVED`/`REJECTED`/`NON_EVALUABLE` — counts as "completed"; only a genuine crash/technical failure during computation yields `FAILED_BEFORE_EVALUATION` or no attempt at all.

### Corrected NON_EVALUABLE evidence model

`evidence_availability` (risk.md §5b2) is always present with all seven keys, regardless of `result`. When `result ∈ {APPROVED, REJECTED}`, every key is `AVAILABLE` and every corresponding ref/scalar is present with exact values. When `result = NON_EVALUABLE`, at least one key is not `AVAILABLE`; the corresponding field is absent (never a fabricated placeholder/null ref/sentinel scalar); resolved evidence for OTHER, still-available keys may remain present. `REQUIRED_EVIDENCE_UNAVAILABLE` maps to `evidence_facts` keys; `RISK_POLICY_EVIDENCE_UNAVAILABLE` maps to `risk_evidence` axis keys; `INCOMPATIBLE_EVIDENCE_UNIT` maps to `unit_evidence` mismatch.

### Currency and unit model

Bounded v0.1 model (risk.md §5b1) — no FX conversion, no signed/netted exposure, no general unit framework. `budget_currency = equity_currency = exposure_notional_currency = reference_price_quote_currency = approved_notional_currency = TradableListing quote asset` (strict string equality); `reference_price_base_unit = quantity_unit`; `current_instrument_exposure_value` is non-negative gross quote-notional. Any mismatch (when the relevant fields are AVAILABLE) → `NON_EVALUABLE`/`INCOMPATIBLE_EVIDENCE_UNIT`.

### Numeric-domain constraints

`configured_risk_budget`/`max_requested_notional`/`reference_price_value`: finite, `> 0`. `available_account_equity_value`/`current_instrument_exposure_value`: finite, `>= 0`, gross quote-notional. `quantity_precision`: integer, `>= 0`, `<= 18` (disclosed bounded v0.1 maximum — no existing repository-wide bound found). Missing/unresolvable evidence → `NON_EVALUABLE`; incompatible unit → `NON_EVALUABLE`; resolved scalar outside domain → `REJECTED`/`INVALID_SIZING_INPUT`. Negative exposure is rejected at domain-validation (step 6), strictly before the exposure-cap check (step 10) — it can never reduce projected exposure or bypass the cap. Projected exposure remains `current gross quote-notional exposure + configured risk budget`.

### Corrected sizing algorithm

Thirteen deterministic steps (risk.md §5c), evaluated in order, stopping at the first failing check: (1) Trade Intent eligibility (already validated at §5a); (2) resolve risk evidence axes; (3) resolve evidence facts + unit evidence; (4) required-evidence availability check → `NON_EVALUABLE`/`REQUIRED_EVIDENCE_UNAVAILABLE` or `RISK_POLICY_EVIDENCE_UNAVAILABLE`; (5) unit-compatibility check → `NON_EVALUABLE`/`INCOMPATIBLE_EVIDENCE_UNIT`; (6) numeric-domain validation → `REJECTED`/`INVALID_SIZING_INPUT`; (7) account ACTIVE; (8) environment PAPER; (9) equity >= budget; (10) projected gross quote-notional <= max requested notional; (11) floor-rounded quantity; (12) zero-quantity check → `REJECTED`/`QUANTITY_ROUNDS_TO_ZERO`; (13) otherwise `APPROVED` with strictly positive quantity. Result/reason precedence is fully deterministic — exactly one terminal branch fires.

### Positive-quantity rule

`approved_quantity` is strictly positive (`> 0`) whenever present — pinned on `RiskEvaluationRecorded` (risk.md §5c step 12–13, §5e) and on `ExecutionIntent`/`ExecutionIntentIssued` (execution-intent.md §1/§3). A value of exactly `0` after floor-rounding is `REJECTED`/`QUANTITY_ROUNDS_TO_ZERO`, never `APPROVED` — `approved_quantity`/`approved_notional` absent in that case, zero Execution Intent.

### Execution Intent quantity invariant

Because an Execution Intent can only originate from a RiskEvaluation with `result = APPROVED` (execution-intent.md §1 invariant, unchanged), and `APPROVED` now guarantees `approved_quantity > 0` (risk.md §5c/§5e, v0.2), an `ExecutionIntentIssued` with zero or negative `approved_quantity` cannot exist validly — pinned as an explicit precondition invariant on `ExecutionIntentIssued` (§3) in addition to the entity-level invariant (§1), so no `OPEN_EXPOSURE` Execution Intent can carry zero quantity.

### Complete C6 eligibility chain

`eligible_for_new_order_creation(execution_intent_id, C)` (execution-intent.md §6a) now requires five AND-conditions: (1) `ExecutionIntent.current_status(C) == ISSUED`; (2) originating RiskEvaluation resolves to the visible-valid-head `APPROVED` for its logical Risk computation key at C; (3) that head is exactly the `originating_risk_evaluation_id` referenced; (4) that RiskEvaluation references the same `trade_intent_id`; (5) `eligible_for_new_risk_evaluation(trade_intent_id, C) == true`. Transitively ensures originating Decision, Trade Intent, and RiskEvaluation all remain valid, in addition to Execution Intent remaining ISSUED. When Trade Intent or RiskEvaluation becomes invalid, the old Execution Intent remains historical and ineligible for new Order creation, with no automatic history rewrite; a replacement chain may derive a new Execution Intent. No Order semantics authored.

### Correction/replay preservation

Unchanged, verified: opaque `risk_evaluation_id`/`evaluation_attempt_id`/`execution_intent_id` identity; per-attempt identity separate from logical computation key; multiple attempts per key; retry after `FAILED_BEFORE_EVALUATION`; one visible-valid-head per logical key; invalidate-first correction lineage (risk.md §10, ten invariants); replay-before/replay-after semantics; risk policy definition/configuration/plugin/build-artifact separation (four axes); no-look-ahead; Decision and Trade Intent causality; Risk-to-Execution-Intent idempotency (`execution_intent_derivation_idempotency_policy`); no cross-stream atomicity between RiskEvaluation↔Execution Intent AND now explicitly between Attempt↔RiskEvaluation; Execution Intent lifecycle (ISSUED/WITHDRAWN/EXPIRED); C1–C4 semantics; C5/C6 boundary.

### Acceptance-scenario results (risk.md §17, eighteen scenarios — twelve required + six inherited)

Scenario 1 (truthful successful attempt) — pass. Scenario 2 (crash before completion, retry) — pass. Scenario 3 (crash after completed Attempt, recoverable append gap) — pass. Scenario 4 (missing equity evidence, no fabrication) — pass. Scenario 5 (unresolved policy configuration, dependent scalars absent) — pass. Scenario 6 (unit mismatch, no FX-convert) — pass. Scenario 7 (valid unit chain) — pass. Scenario 8 (zero quantity rounds to zero) — pass. Scenario 9 (negative exposure rejected, cap not bypassed) — pass. Scenario 10 (valid approval) — pass. Scenario 11 (Trade Intent invalidated after approval, E1 historical) — pass. Scenario 12 (Risk replacement chain, E1 ineligible, R2 may derive E2) — pass. Scenario 13 (risk budget exceeded) — pass. Scenario 14 (Trade Intent ineligible) — pass. Scenario 15 (same evaluation retry, idempotent) — pass. Scenario 16 (cross-stream recovery) — pass. Scenario 17 (time ordering) — pass. Scenario 18 (direction/scope preservation) — pass.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, Chapter 8 §8.1.1/§8.2/§8.5 (Locked, byte-for-byte unchanged), Chapter 9 §9.1 (Locked, byte-for-byte unchanged), `trade-intent.md` v0.2 Draft §6a (byte-for-byte unchanged, verified), `decision.md` v0.3 Draft (byte-for-byte unchanged, verified), Package 0.2-C1/C2/C3/C4 (all `Consolidated Stable`, byte-for-byte unchanged, verified). `context-map.yaml` metadata-only bump (owned-contract version comment), no relationship edge added/removed.

### Author self-review

`quantity_precision` maximum `18` is a disclosed v0.1 judgment call (risk.md §15) — no existing repository-wide decimal precision bound was found in Constitution Chapters or other Consolidated Stable/Locked Domain Contracts at authoring time; if a repository-wide bound is established later, this value should be revisited. All lettered scenario cross-references (A–K) renumbered to 1–18 and re-verified via grep across both files — no stale letter reference remains. All sixteen (`risk.md`) + eight (`execution-intent.md`) YAML fenced blocks parse via `yaml.safe_load` — verified. `§5b` retained for `trade_evidence` (unconditional); new `§5b1`/`§5b2`/`§5b3` added for unit model/evidence-availability/risk-evidence-axes respectively — internal `§5b` cross-references audited and updated where they meant the axes (now `§5b3`) versus trade evidence (still `§5b`). No finding blocking khác found.

### Changed-file scope

```text
docs/domain/risk.md              MODIFIED v0.1 → v0.2   blob a08f94851014bce5da51d98781fd9253d026fc34
docs/domain/execution-intent.md  MODIFIED v0.1 → v0.2   blob afc0c1fe7bdd2f285403dff29c71849ab66af70c
docs/domain/context-map.yaml     MODIFIED v0.15 → v0.16 blob 87e0411d1270ceacd4eb20e76340911900dedaad
docs/domain/README.md            MODIFIED v0.42 → v0.43 blob f4732d7867fdbaac50012991d67841d6cc0ca3d9
docs/MANIFEST.md                 MODIFIED manifest_version 9.68 → 9.69
docs/CHANGELOG.md                MODIFIED (this entry)
docs/domain/decision.md          KHÔNG ĐỔI — blob e2a26320200d350ace3da0247235bb14cef12509, verified byte-identical
docs/domain/trade-intent.md      KHÔNG ĐỔI — blob e7a306abc53ba482ff1249af1dda2829c4c82fa7, verified byte-identical
```

### Metadata / state

- `risk.md`: **v0.1 → v0.2**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `execution-intent.md`: **v0.1 → v0.2**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `context-map.yaml`: **v0.15 → v0.16**, metadata-only (owned-contract version comment).
- `README.md` (domain index): **v0.42 → v0.43**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.68 → 9.69**.
- `decision.md`, `trade-intent.md`: **không đổi** (byte-for-byte, verified) — forbidden scope, không sửa.
- `ADR-010.md`, `ADR-012.md`, `ADR-013.md`, `instrument.md`, `venue.md`, `account.md`, `strategy.md`: **không đổi** (byte-for-byte, verified).
- Mọi ADR khác, Constitution, mọi Domain Contract khác: **không đổi.**

**Package 0.2-C5 VẪN CHƯA đạt `Consolidated Stable` — chờ bounded delta review (ChatGPT + Independent Review B) trên cùng exact baseline correction này.** Mandatory sequence tiếp tục: ChatGPT delta review → Independent Review B delta review → Product Owner consolidation decision. KHÔNG correction thêm dựa trên một review đơn lẻ. Risk và Execution Intent vẫn là HAI concept riêng biệt, KHÔNG gộp. Package 0.2-C1/C2/C3/C4 vẫn `Consolidated Stable`, không đổi. Package 0.2-C6–C7 vẫn chưa authorize, chưa author, chưa authored. Không artifact nào Approved hay Locked. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-08-01 — author Package 0.2-C5 risk foundation

**Package 0.2-C5 — Risk Gateway and Execution Intent Foundation v0.1 authored.** Vai trò: `Domain Contract Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C5 — Risk Gateway and Execution Intent Foundation v0.1". Authorized artifacts: `docs/domain/risk.md`, `docs/domain/execution-intent.md` (cả hai tạo mới, v0.1 Draft). Authorization này **không** cho phép author Package 0.2-C6–C7, định nghĩa order type/limit price/stop price/exchange payload/routing/adapter behavior, portfolio-level arbitration/multi-account netting/advanced margin/liquidation model, general Risk DSL, backtest/optimizer infrastructure, sửa `decision.md`/`trade-intent.md`/C1–C4 semantic/ADR-010/ADR-012/ADR-013/bất kỳ ADR nào/Constitution, đóng OQ-002/OQ-003, Approve/Lock/Consolidate bất kỳ artifact/package nào, hay authorize Live.

### Baseline verification

```text
Expected HEAD:  b6525ae181322152bef8f9f282fcc376c13e43b3
Actual HEAD:    b6525ae181322152bef8f9f282fcc376c13e43b3  — match

Package 0.2-C1:  Consolidated Stable (không đổi)
Package 0.2-C2:  Consolidated Stable (không đổi)
Package 0.2-C3:  Consolidated Stable (không đổi)
Package 0.2-C4:  Consolidated Stable (không đổi)
decision.md:       v0.3 Draft, blob e2a26320200d350ace3da0247235bb14cef12509
trade-intent.md:    v0.2 Draft, blob e7a306abc53ba482ff1249af1dda2829c4c82fa7
context-map.yaml:   v0.14 Draft, blob e7ad311419f54a60625ce05f37b0c0c8e982fafb
risk.md/execution-intent.md: absent trước transaction — đúng expected state, KHÔNG có baseline conflict
```

### Risk Evaluation identity and attempt model

`risk_evaluation_id` — opaque, globally unique, immutable, gán tại `RiskEvaluationRecorded`. Logical computation key `(trade_intent_id, risk_context_cursor)`. `RiskEvaluationAttempt` (kind: entity, §2 risk.md) — subject RIÊNG, `evaluation_attempt_id` (identity cá nhân) TÁCH BIỆT khỏi logical computation key — ÁP DỤNG CHỦ ĐỘNG (KHÔNG chờ review round phát hiện) ba bài học đã trả giá qua C4's hai vòng correction: (1) KHÔNG circular reference giữa Attempt và RiskEvaluation — Attempt KHÔNG mang field trỏ tới RiskEvaluation, chỉ RiskEvaluationRecorded.causation_refs trỏ ngược lại attempt (one-way sequence, đóng trước lớp lỗi `C4-DELTA-MAJ-01`-style); (2) idempotency scoped theo `evaluation_attempt_id`, KHÔNG theo logical key — nhiều attempt (kể cả outcome khác nhau) CÓ THỂ chia sẻ cùng key (đóng trước lớp lỗi `C4-DELTA-MAJ-02`-style); (3) `FAILED_BEFORE_EVALUATION` tường minh RETRYABLE, không permanently block same-cursor recovery. `attempt_outcome ∈ {EVALUATED, INELIGIBLE, FAILED_BEFORE_EVALUATION}` — mọi lần thử ĐỀU ghi nhận (`RiskEvaluationAttemptRecorded`), KHÔNG absence-based.

### Trade Intent/C4 eligibility integration

RiskEvaluation CHỈ được phát khi `eligible_for_new_risk_evaluation(trade_intent_id, risk_context_cursor) == true` (trade-intent.md §6a, KHÔNG sửa, KHÔNG duplicate/weaken) — false → `RiskEvaluationAttemptRecorded(attempt_outcome=INELIGIBLE, reason_code=TRADE_INTENT_INELIGIBLE)`, KHÔNG RiskEvaluation nào phát (Scenario C, risk.md §17).

### Risk policy/configuration/evidence axes

Bốn trục risk evidence (risk.md §5b), đối xứng Strategy's bốn trục (strategy.md, ADR-013): `risk_policy_definition_version_ref` (semantic policy meaning), `risk_policy_configuration_version_ref` (configured parameter values), `risk_plugin_version_ref` (implementation release — Chapter 9 §9.1, áp dụng platform-wide, KHÔNG phải trục phát minh riêng cho C5), `package_build_artifact_ref` (exact executable identity). Thay đổi configured value KHÔNG tự động require policy definition version mới; thay đổi policy meaning yêu cầu version mới — đúng bảng phân tách task. Evidence facts (risk.md §5d): `available_account_equity_ref`/`current_instrument_exposure_ref`/`reference_price_fact_ref` — opaque `event_record_ref`, KHÔNG redefine Account/Candle contract; no-look-ahead `evidence_fact.recorded_time ≤ risk_context_cursor.recorded_time ≤ RiskEvaluationRecorded.recorded_time`.

### Sizing and quantity model

`sizing_method: FIXED_RISK_BUDGET_NOTIONAL` (v0.1, đúng một giá trị bounded). Năm check tuần tự, dừng tại fail đầu tiên: (1) account active; (2) environment = PAPER; (3) reference_price hợp lệ; (4) equity >= configured_risk_budget; (5) projected_instrument_notional <= max_requested_notional. Pass cả năm → `approved_notional = configured_risk_budget`, `approved_quantity = FLOOR(approved_notional / reference_price_value, quantity_precision)` — deterministic floor-rounding, non-negative, finite. KHÔNG liquidation model, KHÔNG leverage/stop-distance concept, KHÔNG portfolio optimization.

### Outcome/reason model

`result: APPROVED | REJECTED | NON_EVALUABLE` (risk.md §5e) — ba trường hợp phân biệt tường minh, KHÔNG collapse: APPROVED (policy evaluated, mọi check pass); REJECTED (policy evaluated, MỘT check fail — reason ∈ {ACCOUNT_NOT_ACTIVE, ENVIRONMENT_NOT_ALLOWED, INVALID_SIZING_INPUT, RISK_BUDGET_EXCEEDED, REQUESTED_EXPOSURE_EXCEEDED}); NON_EVALUABLE (evidence bắt buộc thiếu/invalid/unresolved — reason=REQUIRED_EVIDENCE_UNAVAILABLE). Tách biệt khỏi attempt-level INELIGIBLE (TRADE_INTENT_INELIGIBLE)/FAILED_BEFORE_EVALUATION (RISK_ENGINE_COMPUTATION_BOUNDARY_ERROR) — bảy reason code đóng tổng cộng, đúng bounded vocabulary task yêu cầu, không thêm reason nào ngoài các check thực sự tồn tại.

### Explanation model

Explanation (risk.md §8) là derived, non-authoritative rendering — thuần hàm của evidence đã có (§5b–§5e), KHÔNG BAO GIỜ introduce fact vắng mặt. Hai RiskEvaluation cùng evidence PHẢI cho cùng explanation render.

### Correction/replay model

`risk_evaluation_id` bất biến/globally-unique per-fact — correction lineage (risk.md §10, mười invariant, đối xứng decision.md §11): logical computation key CÓ THỂ nhận RiskEvaluationRecorded MỚI (risk_evaluation_id khác, `supersedes_fact_ref`) sau khi predecessor invalidate; cấm fork; append-only; replay trước correction thấy R1, replay sau thấy R2. Execution Intent derived từ RiskEvaluation bị invalidate KHÔNG tự động rewrite/xóa — ineligible cho Order creation mới qua `eligible_for_new_order_creation` (execution-intent.md §6a).

### Execution Intent identity and lifecycle

`execution_intent_id` — opaque, globally unique, immutable. Origin từ ĐÚNG MỘT RiskEvaluation APPROVED (`originating_risk_evaluation_id`). `account_id`/`instrument_selection_ref`/`direction`/`approved_quantity`/`quantity_unit` PHẢI khớp CHÍNH XÁC RiskEvaluation gốc — KHÔNG tự tính lại (Scenario K, risk.md §17). `execution_action: OPEN_EXPOSURE` (v0.1, duy nhất — CLOSE/REDUCE deferred). Lifecycle tối thiểu ba state ISSUED/WITHDRAWN/EXPIRED, `supersedes_fact_ref` từ v0.1 (áp dụng chủ động bài học C2/C3/C4).

### Risk-to-Execution-Intent derivation/idempotency

```text
result = APPROVED               → zero HOẶC MỘT ExecutionIntentIssued, keyed unique bởi originating_risk_evaluation_id
result = REJECTED | NON_EVALUABLE → ZERO Execution Intent luôn luôn
```
RiskEvaluation KHÔNG có field nào tuyên bố "đã issue Execution Intent" (áp dụng chủ động bài học `C4-MAJ-01`/`C4-MAJ-02`, ngay từ v0.1) — câu hỏi resolve trực tiếp qua query stream lọc `originating_risk_evaluation_id` (canonical `execution_intent_derivation_idempotency_policy: ONE_VALID_INTENT_PER_ORIGINATING_RISK_EVALUATION`, execution-intent.md §10). Gap tạm thời là trạng thái BÌNH THƯỜNG, KHÔNG data-integrity violation — KHÔNG unstated cross-stream atomicity. Implementation technology deferred (Phase 1).

### Time and cursor semantics

`risk_context_cursor` TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1 Replay Cursor shape (`recorded_time`/`input_contract_ref`/`stream_registry_version`/`lifecycle_frontier`/`stream_positions`) — KHÔNG tạo schema gần giống, KHÔNG envelope-level ADR-010 field (chỉ riêng `decision.md`'s `DecisionRecorded`, `event_class: decision`). `ExecutionIntentIssued.effective_time >= risk_evaluation_time`; `ExecutionIntentIssued.recorded_time > RiskEvaluationRecorded.recorded_time` — strict causal (Scenario J, risk.md §17).

### Future C6 eligibility rule

```text
eligible_for_new_order_creation(execution_intent_id, C) =
      ExecutionIntent.current_status(C) == ISSUED
  AND originating RiskEvaluation resolve đúng visible-valid-head cho logical Risk computation key TẠI C
  AND visible-valid-head đó CHÍNH LÀ risk_evaluation_id mà Execution Intent này tham chiếu
```
Khi RiskEvaluation gốc invalidate/supersede: Execution Intent liên quan mất eligibility Order creation mới, KHÔNG tự động xóa/rewrite; replacement approved RiskEvaluation CÓ THỂ derive Execution Intent riêng (execution-intent.md §6a).

### Context Map integration

Đăng ký capability `risk-management` + context `risk-gateway` (`owned_contracts: [risk, execution-intent]`, HAI file CÙNG một context) tại `context-map.yaml` **v0.14 → v0.15**. KHÔNG thêm relationship edge nào — `risk.md`/`execution-intent.md` chỉ dùng simple `ref:` lookup (`trade_intent_id`, `account_id`) và `event_record_ref` opaque chưa gắn provider context cụ thể (evidence facts, deferred).

### Acceptance-scenario results (risk.md §17)

Scenario A (Approved PAPER): APPROVED, approved_quantity deterministic — pass. Scenario B (Risk budget exceeded): REJECTED/RISK_BUDGET_EXCEEDED — pass. Scenario C (Trade Intent ineligible): attempt INELIGIBLE, không RiskEvaluation — pass. Scenario D (Evidence unavailable): NON_EVALUABLE/REQUIRED_EVIDENCE_UNAVAILABLE — pass. Scenario E (Same evaluation retry): idempotent/conflict — pass. Scenario F (Operational failure/retry): FAILED_BEFORE_EVALUATION rồi EVALUATED cùng key — pass. Scenario G (Risk correction): R1→R2 same-key replacement — pass. Scenario H (Cross-stream recovery): retry bằng originating_risk_evaluation_id → đúng một E1 — pass. Scenario I (Risk invalidation): E1 historical, ineligible Order creation mới — pass. Scenario J (Time ordering): effective_time < risk_evaluation_time reject — pass. Scenario K (Direction/scope preservation): mismatch reject — pass.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10 (đặc biệt Chapter 8 §8.1.1/§8.2/§8.5, Chapter 9 §9.1), Package 0.2-C1/C2/C3/C4 (`instrument.md`/`venue.md`/`account.md`/`strategy.md`/`decision.md`/`trade-intent.md` byte-for-byte unchanged — verified). Preserve nguyên vẹn: opaque non-derived identity pattern; invalidate-only-no-replacement cho immutable-scope subject; correction lineage mười invariant; fold algorithm "visible-valid-head per logical key"; Current View never-authority; `eligible_for_new_risk_evaluation` (trade-intent.md §6a, không sửa/duplicate/weaken). Không order type/limit price/stop price/exchange payload/routing/adapter behavior. Không portfolio-level arbitration/multi-account netting/advanced margin/liquidation model. Không general Risk DSL. Không backtest/optimizer infrastructure.

### Author self-review

Phát hiện và disclosure tường minh: task gốc liệt kê `risk_plugin_version_ref` là "chỉ nếu repository architecture genuinely require" — self-review xác nhận Chapter 9 §9.1 (Locked) định nghĩa bốn lớp Plugin identity ÁP DỤNG PLATFORM-WIDE cho MỌI Plugin Definition (không riêng Strategy) — Risk Gateway, nếu là một Plugin Definition trong model này, GENUINELY cần trục này để phân biệt implementation-release khỏi package/build-artifact identity (đúng lý do Strategy cần nó, ADR-013 §2.5) — đã bao gồm trục này với citation rõ ràng, KHÔNG phải thêm "cho đối xứng." Không tìm thấy finding blocking nào khác trong self-review.

### Changed-file scope

```text
docs/domain/risk.md             NEW      v0.1  Draft   blob fa8070b0c6a710f39bdb9dd27915076d4b36d0c2
docs/domain/execution-intent.md NEW      v0.1  Draft   blob c5cb23012a4bec7517803d9f47ac0df6b0955801
docs/domain/context-map.yaml    MODIFIED v0.14 → v0.15  (capability/context registration + comment)
docs/domain/README.md           MODIFIED v0.41 → v0.42
docs/MANIFEST.md                MODIFIED manifest_version 9.67 → 9.68
docs/CHANGELOG.md               MODIFIED (this entry)
```

### Metadata / state

- `risk.md`/`execution-intent.md`: **tạo mới**, `version: "0.1"`, `status: Draft`, `approved_by: null`, `approved_at: null`.
- `context-map.yaml`: **v0.14 → v0.15** — thêm capability `risk-management` + context `risk-gateway`, KHÔNG thêm relationship edge.
- `README.md` (domain index): **v0.41 → v0.42**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.67 → 9.68**; dòng `domain/` cập nhật ghi nhận Package 0.2-C5 authoring transaction.
- `decision.md`, `trade-intent.md`, `strategy.md`, `account.md`, `venue.md`, `instrument.md`, mọi ADR: **không đổi** (byte-for-byte, verified).
- Mọi Domain Contract khác: **không đổi.**

**Package 0.2-C5 CHƯA đạt `Consolidated Stable` — chờ ChatGPT Review A + Independent Review B trên cùng exact baseline này.** Mandatory sequence: Author baseline → ChatGPT Review A → Independent Review B → merge finding → một correction commit (Product Owner authorize) → delta review hai vòng → Product Owner consolidation decision. KHÔNG correction dựa trên một review đơn lẻ. Package 0.2-C1/C2/C3/C4 vẫn `Consolidated Stable`, không đổi. Package 0.2-C6–C7 vẫn chưa authorize, chưa author. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-31 — consolidate Package 0.2-C4

**Package 0.2-C4 Trade Intent and Decision Foundation consolidated as `Consolidated Stable`.** Vai trò: `Package Lifecycle Consolidation Author · Repository Transaction Executor`. Product Owner authorized: "Package 0.2-C4 consolidation transaction" (2026-07-31). Authorization này cho phép ghi Package 0.2-C4 vào lifecycle state `Consolidated Stable` — nó KHÔNG cho phép Approve/Lock `decision.md`/`trade-intent.md`, không sửa ADR-010/ADR-013 hay bất kỳ ADR nào, không sửa Constitution, không đóng OQ, không authorize Live, không author/authorize Package 0.2-C5–C7, không thêm speculative edge case, không tuyên bố Phase 0.2 hoàn thành.

### Baseline verification

```text
Expected HEAD:  2f338f54d19a1eaaf1280061e418793337de7a5e
Actual HEAD:    2f338f54d19a1eaaf1280061e418793337de7a5e  — match

decision.md:       v0.3 Draft, blob e2a26320200d350ace3da0247235bb14cef12509  — match
trade-intent.md:    v0.2 Draft, blob e7a306abc53ba482ff1249af1dda2829c4c82fa7  — match
context-map.yaml:   v0.14 Draft, blob e7ad311419f54a60625ce05f37b0c0c8e982fafb  — match
README.md:          v0.40 Draft, blob 35e87b078c2ca8c21090a0e54f1f51589f1201b8  — match
MANIFEST.md:        manifest_version 9.66, blob ace9979897f793c1f2c52b543294e0a07d665835  — match
```

### Reviewed baseline pinned

```text
Package 0.2-C4 reviewed HEAD:  2f338f54d19a1eaaf1280061e418793337de7a5e

Primary artifacts:       decision.md v0.3 Draft, blob e2a26320200d350ace3da0247235bb14cef12509
                          trade-intent.md v0.2 Draft, blob e7a306abc53ba482ff1249af1dda2829c4c82fa7
Controlling architecture: ADR-010.md Approved, blob 80b1807f9b99f2a83bfbdbdbd90672bd9ff06759 (unchanged)
                          ADR-013.md v0.3 Approved, blob 02df931143f8408c61d19ee2c91d2d355d5deb1d (unchanged, qua strategy.md)
Integration artifact:    context-map.yaml v0.14 Draft, blob e7ad311419f54a60625ce05f37b0c0c8e982fafb (unchanged)
Registry baseline:       MANIFEST v9.66, blob ace9979897f793c1f2c52b543294e0a07d665835
```

### Review evidence

```text
ChatGPT final focused delta re-review:        Clean — 0 blocking finding
Independent Review B final focused delta re-review:  Clean — 0 blocking finding
```

### Complete finding ledger — all resolved (v0.1 → v0.2 bounded correction, v0.2 → v0.3 micro-correction)

```text
C4-MAJ-01:        Resolved (bỏ trade_intent_outcome/SUPPRESSED_DUPLICATE khỏi Decision, duplicate handling nay là idempotency behavior)
C4-MAJ-02:        Resolved (derivation Decision→Trade Intent idempotent qua originating_decision_id unique key)
C4-MAJ-03:        Resolved (correction lineage cho DecisionRecorded, decision_id mới + supersedes_fact_ref, visible-valid-head per logical key)
C4-MAJ-04:        Resolved (thêm DecisionEvaluationAttempt/DecisionEvaluationAttemptRecorded, mọi lần thử là authoritative fact)
C4-MAJ-05:        Resolved (invariant thứ tự effective/recorded-time giữa Trade Intent và Decision gốc)
C4-MAJ-06:        Resolved (thêm eligible_for_new_risk_evaluation origin-validity rule)
C4-DELTA-MAJ-01:   Resolved (loại bỏ resulting_decision_id, Attempt→Decision liên hệ một chiều qua causation_refs)
C4-DELTA-MAJ-02:   Resolved (tách evaluation_attempt_id khỏi logical computation key, idempotency per-attempt-identity)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

### Package lifecycle meaning

`Consolidated Stable` là package lifecycle/readiness state — nghĩa là: reviewed package baseline nội bộ coherent; mọi qualifying finding đã resolved; deferred limitations được ghi nhận tường minh là non-blocking Phase 1 concern; package integration đủ ổn định để làm dependency baseline cho package kế tiếp (0.2-C5). Nó KHÔNG có nghĩa: artifact Approved; artifact Locked; ADR-010/ADR-013 thay đổi; Domain Contract bất biến; OQ closure; Phase completion; implementation authorization; Live authorization.

### Unchanged artifact statuses

`decision.md`: **giữ nguyên** `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte — không sửa Domain Contract semantic trong transaction này. `trade-intent.md`: **giữ nguyên** `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte. `context-map.yaml`: **giữ nguyên** `version: "0.14"`, `status: Draft`, byte-for-byte — không sửa. `ADR-010.md`/`ADR-013.md`: **giữ nguyên** trạng thái Approved, byte-for-byte — không sửa. `instrument.md`/`venue.md`/`account.md`/`strategy.md`/`ADR-012.md`: **giữ nguyên**, byte-for-byte — không sửa.

### Package lifecycle states pinned

```text
Package 0.2-C1:     Consolidated Stable
Package 0.2-C2:     Consolidated Stable
Package 0.2-C3:     Consolidated Stable
Package 0.2-C4:     Consolidated Stable
Package 0.2-C5–C7:  unauthorized, unauthored
```

### Artifact lifecycle states pinned

```text
decision.md:      Draft, version "0.3", approved_by: null, approved_at: null, not Locked
trade-intent.md:  Draft, version "0.2", approved_by: null, approved_at: null, not Locked
```

### Changed-file scope

```text
docs/domain/README.md          MODIFIED v0.40 → v0.41
docs/MANIFEST.md               MODIFIED manifest_version 9.66 → 9.67
docs/CHANGELOG.md              MODIFIED (this entry)
docs/domain/decision.md        KHÔNG ĐỔI — blob e2a26320200d350ace3da0247235bb14cef12509, verified byte-identical
docs/domain/trade-intent.md    KHÔNG ĐỔI — blob e7a306abc53ba482ff1249af1dda2829c4c82fa7, verified byte-identical
docs/domain/context-map.yaml   KHÔNG ĐỔI — blob e7ad311419f54a60625ce05f37b0c0c8e982fafb, verified byte-identical
docs/adr/ADR-010.md            KHÔNG ĐỔI — blob 80b1807f9b99f2a83bfbdbdbd90672bd9ff06759, verified byte-identical
docs/adr/ADR-013.md            KHÔNG ĐỔI — blob 02df931143f8408c61d19ee2c91d2d355d5deb1d, verified byte-identical
```

### Metadata / state

- `decision.md`, `trade-intent.md`, `context-map.yaml`, `ADR-010.md`, `ADR-013.md`: **không đổi** (semantic và version) — package lifecycle metadata only.
- `README.md` (domain index): **v0.40 → v0.41**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.66 → 9.67**; dòng `domain/` cập nhật ghi nhận Package 0.2-C4 `Consolidated Stable`.
- Mọi Domain Contract khác (`instrument.md`, `venue.md`, `account.md`, `strategy.md`, `candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, `context.md`), mọi ADR file, Constitution: **không đổi.**

**Package 0.2-C5 baseline dependency đã thỏa, eligible cho Product Owner scope authorization — CHƯA bắt đầu, CHƯA author, KHÔNG được authorize bởi transaction này.** Package 0.2-C6–C7 gate chưa mở. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-31 — correct C4 evaluation attempt causality

**Package 0.2-C4 micro-correction — DecisionEvaluationAttempt only.** Vai trò: `Domain Contract Micro-Correction Author`. Product Owner authorized: "Package 0.2-C4 micro-correction — DecisionEvaluationAttempt only." Đóng đúng hai finding Major: `C4-DELTA-MAJ-01` (remove Attempt/Decision circular dependency), `C4-DELTA-MAJ-02` (separate individual attempt identity from computation key). Authorization này **không** cho phép reopen bất kỳ C4 design area nào khác, thêm general attempt workflow/retry scheduling/exception telemetry taxonomy/atomic batch semantics, sửa ADR-010/ADR-013/bất kỳ ADR nào/Constitution/C1–C3, author C5–C7, Approve/Lock/Consolidate C4, đóng OQ-002/OQ-003, hay authorize Live.

### Baseline verification

```text
Expected HEAD:  8b99dc3be8feab0b0054bf513596f950e9529027
Actual HEAD:    8b99dc3be8feab0b0054bf513596f950e9529027  — match

decision.md:       v0.2 Draft, blob 94dfd863818a2bfff139a78c3399011430e31ef9  — match
trade-intent.md:    v0.2 Draft, blob e7a306abc53ba482ff1249af1dda2829c4c82fa7  — match
context-map.yaml:   v0.14 Draft, blob e7ad311419f54a60625ce05f37b0c0c8e982fafb  — match
```

### Two-finding resolution matrix

| Finding | Resolution |
|---|---|
| `C4-DELTA-MAJ-01` | `resulting_decision_id` removed entirely from `DecisionEvaluationAttempt` schema, `DecisionEvaluationAttemptRecorded` payload/invariants, canonical policy, and scenarios; Attempt→Decision link is now strictly one-way via `DecisionRecorded.causation_refs`; reverse lookup uses existing `GetDecisionForComputation` (§8) or reverse causation_refs search — no new linking event |
| `C4-DELTA-MAJ-02` | `evaluation_attempt_id` (per-attempt identity) separated from logical computation key `(strategy_instance_id, decision_context_cursor)`; idempotency rescoped to per-`evaluation_attempt_id`; multiple attempts (including different outcomes) may now share a logical key; multiple DECIDED attempts must resolve/reuse the same Decision via Decision-layer idempotency |

### Corrected Attempt identity model

`evaluation_attempt_id` — opaque, globally unique, identifies ONE individual attempt. Logical computation key `(strategy_instance_id, decision_context_cursor)` — groups MULTIPLE attempts, no longer required unique. Idempotency (decision.md §2/§13, canonical `decision_evaluation_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT`, đối xứng `instrument.md` §17 `activation_request_idempotency_policy`) applies per `evaluation_attempt_id`: same ID + same payload → idempotent no-op; same ID + changed payload → deterministic conflict. Multiple `DecisionEvaluationAttemptRecorded` facts (distinct `evaluation_attempt_id`) sharing the same logical key — including different `attempt_outcome` values (e.g. `FAILED_BEFORE_EVALUATION` followed by `DECIDED`) — is now explicitly allowed, not a data-integrity violation.

### Corrected Attempt-to-Decision causality

`attempt_outcome = DECIDED` no longer carries or requires `resulting_decision_id`. One-way sequence pinned: `DecisionEvaluationAttemptRecorded(DECIDED)` ghi TRƯỚC → `DecisionRecorded` ghi SAU và tham chiếu attempt qua `causation_refs` (decision.md §4/§5) — loại bỏ hoàn toàn circular append-order dependency (Attempt cần Decision đã VALID để tham chiếu, trong khi Decision cần Attempt đã tồn tại trong causation_refs — không có thứ tự append hợp lệ nào ở v0.2). Query chiều ngược (Decision nào ứng với một attempt) dùng CƠ CHẾ ĐÃ CÓ: `GetDecisionForComputation(strategy_instance_id, decision_context_cursor, cursor)` (§8) hoặc reverse-lookup DecisionRecorded có `causation_refs` chứa event_record_ref của attempt — KHÔNG event/field liên kết mới (đúng yêu cầu "Do not create a new linking event unless strictly necessary. It should not be necessary for v0.3").

### Retry and recovery behavior

`FAILED_BEFORE_EVALUATION` tường minh RETRYABLE — một `DecisionEvaluationAttemptRecorded` MỚI (evaluation_attempt_id khác) tại CÙNG logical key sau đó hợp lệ (Scenario 13). `INELIGIBLE`/`INPUT_UNAVAILABLE` cùng logical key: later attempt allowed, kỳ vọng cùng kết quả nếu cursor/evidence không đổi (deterministic — cursor cố định). Same-attempt-identity retry (evaluation_attempt_id giống hệt): idempotent-same-payload hoặc conflict-changed-payload (Scenario 14). Multiple DECIDED attempts cùng key: PHẢI resolve/reuse Decision đã tồn tại (decision.md §1/§5 invariant mới, Scenario 15) — TUYỆT ĐỐI KHÔNG tạo Decision head thứ hai trừ khi predecessor đã invalidate.

### Interaction with Decision correction lineage

Controlling invariant giữ nguyên KHÔNG đổi: **một visible-valid-head Decision per logical computation key** (decision.md §8/§11, không sửa trong micro-correction này). Multiple attempts (kể cả nhiều DECIDED) tại cùng key KHÔNG BAO GIỜ tạo hai Decision head song song — chỉ correction lineage tường minh (invalidate D1 rồi ghi D2 với `supersedes_fact_ref`) mới hợp lệ tạo Decision thứ hai cho cùng key (Scenario 2 cập nhật thêm attempt-context A1/A2, Scenario 5 đúng nghĩa task).

### Acceptance-scenario results (decision.md §18, Scenario 1/1a/2/13–16 mới hoặc cập nhật)

Scenario 1 (Valid append order): A1 DECIDED không mang resulting_decision_id, D1 causation_refs→A1 — pass. Scenario 1a (same evaluation_attempt_id retry): idempotent — pass. Scenario 2 (Decision correction, attempt context): A1→D1 invalidate→A2→D2 supersedes D1 — pass. Scenario 13 (retry after engine failure): A1 FAILED_BEFORE_EVALUATION → A2 DECIDED cùng key → D1 — pass. Scenario 14 (same attempt retry): idempotent-hoặc-conflict — pass. Scenario 15 (multiple successful attempts): A2 resolve/reuse D1, không tạo D2 — pass. Scenario 16 (no attempt): phân biệt tường minh với mọi attempt đã ghi nhận — pass.

### Regression check

Decision correction lineage (§11), `decision_id` semantics (§1), `decision_time`/`decision_context_cursor` (ADR-010, §3), no-look-ahead (§3/§5d), bốn trục evidence (§5b), bounded EMA rule evidence (§5c), explanation (§9), Decision-to-Trade-Intent derivation (§10), Trade Intent time ordering (trade-intent.md §3/§9), `eligible_for_new_risk_evaluation` (trade-intent.md §6a), Trade Intent lifecycle (trade-intent.md §1) — **tất cả không đổi, verified**. `trade-intent.md` blob giữ nguyên byte-for-byte (không có cross-reference nào cần sửa, verified qua grep). C1–C3 semantics không đổi. C4/C5 boundary không đổi — không author Risk/Execution/Order/Fill/Position, không database transaction/outbox/message-broker technology, không general workflow/saga engine.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, ADR-010 Approved (byte-for-byte unchanged — verified), ADR-013 v0.3 Approved (byte-for-byte unchanged — verified), Package 0.2-C1/C2/C3 (byte-for-byte unchanged — verified). `context-map.yaml` byte-for-byte unchanged — verified (DecisionEvaluationAttempt sống trong decision.md, không cần capability/context/relationship change).

### Author self-review

Xác nhận: mọi tham chiếu `resulting_decision_id` còn lại trong file (3 chỗ) đều là prose giải thích "field đã bị loại bỏ", KHÔNG phải khai báo schema — verified qua grep. Headings/section numbering KHÔNG đổi (bounded, minimal diff — chỉ nội dung bên trong §2/§4/§5/§13/§18 thay đổi). `trade-intent.md` xác nhận KHÔNG chứa bất kỳ tham chiếu nào tới `resulting_decision_id` hay decision.md §2/§4 — blob giữ nguyên đúng yêu cầu "Prefer leaving its blob unchanged." Không tìm thấy finding blocking nào khác.

### Changed-file scope

```text
docs/domain/decision.md   MODIFIED v0.2 → v0.3   blob e2a26320200d350ace3da0247235bb14cef12509
docs/domain/README.md     MODIFIED v0.39 → v0.40
docs/MANIFEST.md          MODIFIED manifest_version 9.65 → 9.66
docs/CHANGELOG.md         MODIFIED (this entry)
docs/domain/trade-intent.md    KHÔNG ĐỔI — blob e7a306abc53ba482ff1249af1dda2829c4c82fa7, verified byte-identical
docs/domain/context-map.yaml   KHÔNG ĐỔI — blob e7ad311419f54a60625ce05f37b0c0c8e982fafb, verified byte-identical
```

### Metadata / state

- `decision.md`: **v0.2 → v0.3**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `trade-intent.md`: **không đổi** — version giữ `0.2`, blob giữ nguyên.
- `context-map.yaml`: **không đổi**.
- `README.md` (domain index): **v0.39 → v0.40**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.65 → 9.66**.
- `ADR-010.md`, `ADR-013.md`, `ADR-012.md`, `instrument.md`, `venue.md`, `account.md`, `strategy.md`: **không đổi** (byte-for-byte, verified).
- Mọi ADR khác, Constitution, mọi Domain Contract khác: **không đổi.**

**Package 0.2-C4 CHƯA đạt `Consolidated Stable` — chờ focused delta re-review (ChatGPT + Independent Review B) trên cùng exact baseline micro-correction này.** Mandatory sequence tiếp tục: focused delta re-review → Product Owner consolidation decision. KHÔNG correction thêm dựa trên một review đơn lẻ. Package 0.2-C1/C2/C3 vẫn `Consolidated Stable`, không đổi. Package 0.2-C5–C7 vẫn chưa authorize, chưa author. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-31 — correct Package 0.2-C4 decision causality

**Package 0.2-C4 bounded correction — consolidated Review A + Independent Review B findings.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C4 bounded correction — consolidated Review A + Independent Review B findings." Đóng đúng sáu finding Major: `C4-MAJ-01` (remove duplicate suppression from Decision evidence), `C4-MAJ-02` (idempotent Decision-to-Trade-Intent derivation), `C4-MAJ-03` (corrected Decision at same logical computation key), `C4-MAJ-04` (evaluation-attempt disposition), `C4-MAJ-05` (Trade Intent causal effective-time ordering), `C4-MAJ-06` (origin-validity eligibility for C5). Authorization này **không** cho phép sửa C1–C3 artifacts, `strategy.md`, ADR-010/ADR-013/bất kỳ ADR nào, author Risk approval/rejection, Execution Intent/Order/Fill/Position/Replay Event, định nghĩa database transaction/outbox/message-broker technology, tạo general workflow engine/strategy DSL, thêm portfolio/multi-intent decomposition, thêm EXIT/FLAT/CLOSE ngoài yêu cầu, authorize C5–C7, Approve/Lock/Consolidate C4, đóng OQ-002/OQ-003, hay authorize Live.

### Baseline verification

```text
Expected HEAD:  e5fe5c817981d4614b13fe6733a17ab2d2052d86
Actual HEAD:    e5fe5c817981d4614b13fe6733a17ab2d2052d86  — match

decision.md:       v0.1 Draft, blob c5b6226dcf46adf2a184ddefef6eca6a222f10da  — match
trade-intent.md:    v0.1 Draft, blob 27647dfd3538fd563ae332f6edaecd1c6eb59d97  — match
context-map.yaml:   v0.14 Draft, blob e7ad311419f54a60625ce05f37b0c0c8e982fafb  — match
README.md:          v0.38 Draft, blob 53dcedb51f87147a5abd2c5248f2b2d9b2ff44ee  — match
MANIFEST.md:        manifest_version 9.64, blob f1e8e591c7003e146efabfc10ee7f5a17bdd8035  — match
```

### Six-finding resolution matrix

| Finding | Resolution | Location |
|---|---|---|
| `C4-MAJ-01` | `trade_intent_outcome`/`SUPPRESSED_DUPLICATE` removed from `DecisionRecorded`; duplicate retry handled as idempotency behavior | decision.md §5e/§10 |
| `C4-MAJ-02` | `originating_decision_id` is a unique key across all VALID `TradeIntentIssued`; idempotent-same-payload / reject-changed-payload; canonical `trade_intent_derivation_idempotency_policy` | trade-intent.md §1/§3/§10 |
| `C4-MAJ-03` | `decision_id` stays immutable/global-unique per fact, but logical computation key `(strategy_instance_id, decision_context_cursor)` now supports invalidate + same-key replacement with a NEW `decision_id` + `supersedes_fact_ref`; visible-valid-head per logical key | decision.md §1/§8/§11 |
| `C4-MAJ-04` | New `DecisionEvaluationAttempt`/`DecisionEvaluationAttemptRecorded` — every attempt (DECIDED/INELIGIBLE/INPUT_UNAVAILABLE/FAILED_BEFORE_EVALUATION) is now an authoritative fact, never represented by absence | decision.md §2/§4 |
| `C4-MAJ-05` | `TradeIntentIssued.effective_time >= originating decision_time`; `recorded_time >` strict causal | trade-intent.md §3/§9 |
| `C4-MAJ-06` | New `eligible_for_new_risk_evaluation` — checks Trade Intent `ISSUED` AND originating Decision is still the visible-valid-head for its logical key | trade-intent.md §6a |

### Corrected Decision idempotency

Logical computation key = `(strategy_instance_id, decision_context_cursor)`. Retry (chưa invalidate predecessor) cùng key + cùng evidence → idempotent no-op, trả `decision_id` đã tồn tại; cùng key + evidence khác → deterministic conflict, reject (`decision_computation_idempotency_policy: STABLE_KEY_SAME_EVIDENCE_IS_IDEMPOTENT`, decision.md §13). `DecisionEvaluationAttempt` có idempotency riêng — cursor là knowledge boundary cố định nên cùng attempt key PHẢI cùng outcome deterministic (`decision_evaluation_attempt_idempotency_policy: STABLE_KEY_SAME_OUTCOME_IS_IDEMPOTENT`).

### Decision correction lineage

`decision_id` vẫn bất biến/globally-unique/không tái sử dụng CHO TỪNG FACT — nhưng correction lineage (đóng `C4-MAJ-03`) cho phép: D1 (gốc) → `DecisionFactInvalidated` targeting D1 → D2 (decision_id MỚI, CÙNG `strategy_instance_id`/`decision_context_cursor`, `supersedes_fact_ref = D1`). Mười invariant pin tại decision.md §11 (đối xứng `strategy.md`/`account.md`, điều chỉnh cho decision_id thay đổi xuyên chain trong khi logical key bất biến): supersedes_fact_ref absent cho gốc, bắt buộc cho replacement; predecessor phải đã invalidate và visible; cùng logical key; decision_id mới; cấm fork; cấm nhảy cóc; append-only; retry-với-evidence-khác-khi-CHƯA-invalidate vẫn là conflict (KHÔNG tự động thành correction). `DecisionCurrentView` (§8) fold algorithm viết lại hoàn toàn — khóa theo LOGICAL COMPUTATION KEY (không còn theo `decision_id` đơn lẻ), duyệt chain theo `supersedes_fact_ref`, `pending_correction_class` rút còn MỘT giá trị (`AWAITING_SAME_SUBJECT_REPLACEMENT` — không còn `TERMINAL_SCOPE_INVALIDATION` cho subject này, vì logical key luôn CÓ THỂ nhận replacement). Canonical policy mới: `decision_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE`.

### Evaluation-attempt model

`DecisionEvaluationAttempt` (kind: entity, decision.md §2) + `DecisionEvaluationAttemptRecorded` (kind: event, §4) — subject RIÊNG biệt Decision. Minimum identity: `evaluation_attempt_id`/`strategy_instance_id`/`decision_context_cursor`/`attempt_outcome`/`reason_code`/`checked_evidence_refs`/`resulting_decision_id`. Bốn outcome đóng: `DECIDED` (resulting_decision_id bắt buộc, trỏ DecisionRecorded VALID cùng key); `INELIGIBLE` (reason_code MỘT trong năm giá trị map trực tiếp strategy.md §9a's điều kiện fail: STRATEGY_INSTANCE_NOT_ACTIVE/DEFINITION_VERSION_NOT_VALID/ACCOUNT_NOT_ACTIVE/EVIDENCE_AXIS_UNRESOLVABLE/INSTRUMENT_SELECTION_INELIGIBLE); `INPUT_UNAVAILABLE` (reason_code REQUIRED_PRICE_INPUT_MISSING_OR_PENDING hoặc REQUIRED_REFERENCE_INPUT_MISSING_OR_PENDING); `FAILED_BEFORE_EVALUATION` (reason_code = ENGINE_COMPUTATION_BOUNDARY_ERROR — v0.1/v0.2 CHỈ một giá trị, KHÔNG model broad runtime exception taxonomy/observability infrastructure, deferred §16). `DecisionRecorded` nay causally trace VỀ attempt tương ứng (§5 invariant). Thay thế hoàn toàn "no event when ineligible/missing-input" của v0.1 — `decision_non_creation_policy` bị loại bỏ.

### Decision-to-Trade-Intent derivation

```text
result = LONG | SHORT  → zero HOẶC MỘT TradeIntentIssued, keyed unique bởi originating_decision_id (idempotent derivation)
result = NO_ACTION     → zero Trade Intent luôn luôn
```
Decision KHÔNG còn field nào tuyên bố "đã issue" — câu hỏi resolve trực tiếp bằng query Trade Intent stream lọc `originating_decision_id` (decision.md §10). Gap tạm thời (Decision LONG/SHORT tồn tại, Trade Intent chưa append) là trạng thái BÌNH THƯỜNG, không phải data-integrity violation — KHÔNG unstated cross-stream atomicity. Phase 1 recovery resolve deterministic; implementation technology (retry queue/outbox/message-broker) hoàn toàn deferred.

### Trade Intent effective-time rule

`TradeIntentIssued.effective_time >= originating DecisionRecorded.decision_time` (mặc định bằng nhau, backfill chỉ được MUỘN HƠN); `TradeIntentIssued.recorded_time > originating DecisionRecorded.recorded_time` (strict causal). Vi phạm → invalid TradeIntentIssued, từ chối khi append (trade-intent.md §3).

### Origin-validity/C5 eligibility rule

```text
eligible_for_new_risk_evaluation(trade_intent_id, C) =
      TradeIntent.current_status(C) == ISSUED
  AND originating Decision resolve đúng visible-valid-head cho logical computation key của nó TẠI C
  AND visible-valid-head đó = originating_decision_id mà Trade Intent tham chiếu
```
Khi Decision gốc invalidate/supersede: Trade Intent liên quan mất eligibility Risk evaluation MỚI, KHÔNG tự động xóa/rewrite; historical replay trước invalidation không đổi; withdrawal/invalidation tường minh vẫn là hành động RIÊNG, tùy chọn. Decision correction replacement (D2) CÓ THỂ derive Trade Intent riêng (T2, `trade_intent_id` mới) — T1/T2 phân biệt lịch sử (trade-intent.md §6a, canonical `trade_intent_origin_validity_policy: ORIGIN_MUST_BE_VISIBLE_VALID_HEAD_AT_SAME_CURSOR`).

### Correction và replay behavior

Replay trước một Decision correction thấy D1; replay sau thấy D2 (decision.md §8/§12). No-look-ahead giữ nguyên (`input_event.recorded_time ≤ decision_context_cursor.recorded_time ≤ DecisionRecorded.recorded_time`). Trade Intent correction lineage (`TradeIntentStatusChanged` same-slice replacement) không đổi.

### Acceptance-scenario results (decision.md §18)

Scenario 1 (same-key retry): D1/T1 idempotent, không bản ghi mới — pass. Scenario 2 (Decision correction): D1→D2 same-key replacement, một visible valid head — pass. Scenario 3 (ineligible attempt): DecisionEvaluationAttemptRecorded(INELIGIBLE) tường minh, phân biệt "không có attempt" — pass. Scenario 4 (missing input): DecisionEvaluationAttemptRecorded(INPUT_UNAVAILABLE) identify đúng boundary — pass. Scenario 5 (engine failure): DecisionEvaluationAttemptRecorded(FAILED_BEFORE_EVALUATION), không broad exception telemetry — pass. Scenario 6 (cross-stream recovery): retry bằng originating_decision_id → đúng một T1, Decision không claim sai — pass. Scenario 7 (time ordering): effective_time < decision_time reject, >= allowed — pass. Scenario 8 (Decision invalidation): T1 historical, ineligible cho Risk evaluation mới — pass. Scenario 9 (corrected Decision derives new Intent): T1/T2 phân biệt — pass.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, ADR-010 Approved (byte-for-byte unchanged — verified), ADR-013 v0.3 Approved (byte-for-byte unchanged — verified), Package 0.2-C1/C2/C3 (`instrument.md`/`venue.md`/`account.md`/`strategy.md` byte-for-byte unchanged — verified). Preserve nguyên vẹn: bốn trục evidence độc lập; bounded EMA rule evidence; Configuration Version ownership của rule parameter; structured deterministic explanation; `decision_time`/`decision_context_cursor` (ADR-010); input visibility/no-look-ahead; Trade Intent Account/TradableListing equivalence; Trade Intent lifecycle ISSUED/WITHDRAWN/EXPIRED; Current View non-authority; C1–C3 semantics; C4/C5 boundary. Không database transaction/outbox/message-broker technology. Không general workflow/saga engine. Không portfolio/multi-intent decomposition. Không EXIT/FLAT/CLOSE ngoài yêu cầu. Không Risk rejection semantics.

### Author self-review

Đã cân nhắc kỹ việc `decision_id` per-fact bất biến (yêu cầu tường minh của finding) TRONG KHI vẫn hỗ trợ correction lineage — giải pháp: logical computation key (không phải decision_id) là đơn vị "slice" cho correction, một pattern MỚI khác cả `INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT...` (Strategy) lẫn correction lineage chuẩn kiểu subject-bất-biến (StrategyInstanceStatusChanged) — ghi nhận công khai tại decision.md §13 (`decision_correction_lineage_policy`). `DecisionCurrentView` viết lại hoàn toàn (khóa theo logical key, không theo decision_id) — self-review xác nhận mọi query/schema liên quan đã cập nhật đồng bộ (§8). Không tìm thấy finding blocking nào khác.

### Changed-file scope

```text
docs/domain/decision.md        MODIFIED v0.1 → v0.2   blob 94dfd863818a2bfff139a78c3399011430e31ef9
docs/domain/trade-intent.md    MODIFIED v0.1 → v0.2   blob e7a306abc53ba482ff1249af1dda2829c4c82fa7
docs/domain/README.md          MODIFIED v0.38 → v0.39
docs/MANIFEST.md               MODIFIED manifest_version 9.64 → 9.65
docs/CHANGELOG.md              MODIFIED (this entry)
docs/domain/context-map.yaml   KHÔNG ĐỔI (không semantic Context Map change được authorize)
```

### Metadata / state

- `decision.md`/`trade-intent.md`: **v0.1 → v0.2**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `context-map.yaml`: **không đổi** — DecisionEvaluationAttempt sống trong decision.md, cùng owned_contracts đã đăng ký.
- `README.md` (domain index): **v0.38 → v0.39**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.64 → 9.65**.
- `ADR-010.md`, `ADR-013.md`, `ADR-012.md`, `instrument.md`, `venue.md`, `account.md`, `strategy.md`: **không đổi** (byte-for-byte, verified).
- Mọi ADR khác, Constitution, mọi Domain Contract khác: **không đổi.**

**Package 0.2-C4 CHƯA đạt `Consolidated Stable` — chờ ChatGPT delta Review A + Independent Review B trên cùng exact baseline correction này.** Mandatory sequence tiếp tục: delta review hai vòng → Product Owner consolidation decision. KHÔNG correction thêm dựa trên một review đơn lẻ. Package 0.2-C1/C2/C3 vẫn `Consolidated Stable`, không đổi. Package 0.2-C5–C7 vẫn chưa authorize, chưa author. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-31 — author Package 0.2-C4 decision foundation

**Package 0.2-C4 — Trade Intent and Decision Foundation v0.1 authored.** Vai trò: `Domain Contract Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C4 — Trade Intent and Decision Foundation v0.1". Authorized artifacts: `docs/domain/decision.md`, `docs/domain/trade-intent.md` (cả hai tạo mới, v0.1 Draft). Authorization này **không** cho phép author Package 0.2-C5–C7, định nghĩa order type/limit price/stop price/exchange payload, position sizing/capital allocation/portfolio arbitration, DSL/executable strategy code, optimizer/backtest infrastructure, sửa C1–C3 semantic, sửa `strategy.md`/ADR-010/ADR-013/bất kỳ ADR nào/Constitution, đóng OQ-002/OQ-003, Approve/Lock/Consolidate bất kỳ artifact/package nào, hay authorize Live.

### Baseline verification

```text
Expected HEAD:  3819f43aa4cd8c76c3d0feda087222390cce5812
Actual HEAD:    3819f43aa4cd8c76c3d0feda087222390cce5812  — match

Package 0.2-C1:  Consolidated Stable (không đổi)
Package 0.2-C2:  Consolidated Stable (không đổi)
Package 0.2-C3:  Consolidated Stable (không đổi)
strategy.md:      v0.3 Draft, blob c2cadc464bc8baecff41ff8079461ec0d5dfaccc
ADR-013.md:       v0.3 Approved, blob 02df931143f8408c61d19ee2c91d2d355d5deb1d
context-map.yaml: v0.13 Draft, blob 5f32edd625f4b66e179dff752d45b301642d76fd
decision.md/trade-intent.md: absent trước transaction — đúng expected state, KHÔNG có baseline conflict
```

### Decision identity and evidence model

`decision_id` — opaque, globally unique, immutable, gán tại `DecisionRecorded`. Logical computation key = `(strategy_instance_id, decision_context_cursor)` — retry cùng key idempotent (evidence giống hệt) hoặc reject deterministic (evidence khác), tái sử dụng đối xứng `activation_request_idempotency_policy` (`instrument.md` §17) dưới tên `decision_computation_idempotency_policy: STABLE_KEY_SAME_EVIDENCE_IS_IDEMPOTENT` (decision.md §11). Decision hoàn toàn bất biến — KHÔNG PATCH event, correction chỉ qua invalidate-only (`DecisionFactInvalidated`, §4), KHÔNG same-ID replacement (cùng `initial_fact_correction_policy` đã proven tại `strategy.md` §12). Historical Decision resolvable độc lập Strategy Instance lifecycle hiện tại (Chapter 9 §9.3).

**Envelope — controlling architecture [ADR-010](../adr/ADR-010.md) Approved + [Chapter 8 §8.2.1/§8.4/§8.5](../constitution/08-event-model.md) Locked:** `DecisionRecorded` (CHỈ event này, `event_class: decision`) mang `decision_time` (BẮT BUỘC, thay `effective_time` — PROHIBITED trên chính event này) và `decision_context_cursor` (BẮT BUỘC, canonical Replay Cursor — `recorded_time`/`input_contract_ref{contract_id, contract_version}`/`stream_registry_version`/`lifecycle_frontier{stream_id, position{kind, sequence}}`/`stream_positions{stream_id: sequence}`, Chapter 8 §8.5.1). Relational invariant bắc cầu (§2 decision.md): `input_event.recorded_time ≤ decision_context_cursor.recorded_time ≤ DecisionRecorded.recorded_time` — cơ chế thực thi no-look-ahead (I-3) cho Decision. Field SHAPE pin ngay v0.1 (ADR-010/Chapter 8 Locked, không thể defer); MECHANISM resolve (Stream Registry/Input Contract cụ thể) là Phase 1, cùng nguyên tắc defer `stream_ref`/`producer_ref` xuyên suốt repository.

### Rule/configuration separation

`decision_rule_ref` (semantic identity) thuộc Strategy Definition Version (`strategy.md` §1, KHÔNG đổi). Decision's `rule_evidence` (decision.md §3c) là bounded typed shape — KHÔNG DSL/parser/rule graph/compiler tổng quát: `rule_family: PRICE_CROSSES_REFERENCE_SERIES` (v0.1, đúng một giá trị, mở rộng sau bằng enum value mới); `price_source`/`reference_series_type`/`reference_series_period`/`crossing_policy`/`evaluation_timing` — TẤT CẢ copied scalar, nguồn authoritative = `configuration_version_ref` (KHÔNG hardcode trên Strategy Definition Version, đúng bảng phân tách task: Strategy Definition Version sở hữu semantic rule identity, Configuration Version sở hữu parameter values). Năm dimension bắt buộc phân biệt (đều đóng): close vs high (`price_source`); EMA50 vs EMA100 (`reference_series_period`); strict cross vs simply above (`crossing_policy`); candle-close vs intrabar (`evaluation_timing`, v0.1 CHỈ CANDLE_CLOSE, INTRABAR reserved/prohibited); LONG vs SHORT vs NO_ACTION (`result`, decision.md §3e, tách biệt khỏi rule_evidence).

### Input-evidence model

`input_evidence` (decision.md §3d) — `previous_price_fact_ref`/`current_price_fact_ref`/`previous_reference_fact_ref`/`current_reference_fact_ref` (tất cả `event_record_ref`, opaque — KHÔNG redefine Candle/Feature/Context contract schema) cộng copied scalar (`previous_price_value`/`previous_reference_value`/`current_price_value`/`current_reference_value`/`timeframe`). No-look-ahead invariant: mọi `*_fact_ref` PHẢI `recorded_time ≤ decision_context_cursor.recorded_time` (Scenario D). Nguồn cụ thể của reference-series fact (EMA hay Feature type khác) deferred (§14 decision.md) — không thuộc phạm vi C4.

### Evaluation-result model

`result: LONG | SHORT | NO_ACTION` (closed enum, đúng style `structure.md`/`context.md`). Ba trường hợp phân biệt tường minh, KHÔNG collapse (đúng yêu cầu task): **rule evaluated false** = `DecisionRecorded` với `result=NO_ACTION` (fact THẬT, evidence đầy đủ); **rule could not be evaluated** (input missing/pending) = KHÔNG `DecisionRecorded` nào phát, deterministic qua kiểm tra trực tiếp upstream input stream tại cursor; **Strategy was ineligible** = KHÔNG `DecisionRecorded` nào phát, deterministic qua kiểm tra trực tiếp `strategy.md` §9a tại cursor. Canonical `decision_non_creation_policy: NO_DECISION_WHEN_INELIGIBLE_OR_REQUIRED_INPUT_MISSING_OR_PENDING` (decision.md §11, tái sử dụng STYLE — đúng một giá trị đóng-enum — của `missing_input_policy` context.md §6/§9, khai báo độc lập tên/giá trị cho context `strategy-decision`).

### Explanation model

Explanation (decision.md §7) là derived, non-authoritative rendering — thuần hàm của `rule_evidence`/`input_evidence`/`result` đã có, KHÔNG BAO GIỜ introduce fact vắng mặt khỏi Decision evidence, KHÔNG UI copy/NLG infrastructure. Hai Decision cùng evidence PHẢI cho cùng explanation render (deterministic).

### Trade Intent identity and lifecycle

`trade_intent_id` (opaque, globally unique, immutable), origin từ ĐÚNG MỘT `originating_decision_id` (`ref: decision`, causally trỏ `DecisionRecorded` result ∈ {LONG, SHORT}). `account_id`/`instrument_selection_ref` PHẢI khớp CHÍNH XÁC Decision gốc (Trade Intent KHÔNG tự chọn Account/instrument khác) — Trade Intent KHÔNG mutate Strategy evidence, KHÔNG tự authorize execution. `direction: LONG | SHORT` khớp `result`; `intent_type: OPEN` (v0.1, EXIT/FLAT/CLOSE/REDUCE deferred — walking skeleton không cần). Lifecycle tối thiểu ba state `ISSUED`/`WITHDRAWN`/`EXPIRED` — terminal cho forward transition nhưng correctable append-only, `supersedes_fact_ref` có mặt ngay từ v0.1 trên `TradeIntentStatusChanged` (áp dụng chủ động bài học `C2-MAJ-02`/`C3-MAJ-02`).

### Decision-to-Trade-Intent cardinality

```text
result = LONG | SHORT  → trade_intent_outcome bắt buộc: ISSUED (một TradeIntentIssued) hoặc SUPPRESSED_DUPLICATE (idempotent retry, zero Trade Intent)
result = NO_ACTION     → trade_intent_outcome tuyệt đối absent, zero Trade Intent luôn luôn
```
Một Decision → tối đa MỘT Trade Intent (v0.1, không multi-intent portfolio decomposition). Lý do suppress duy nhất hợp lệ ở v0.1: `SUPPRESSED_DUPLICATE` — KHÔNG import Risk semantics (risk limit/capital là C5, chưa author).

### Correction/replay model

`DecisionRecorded`/`TradeIntentIssued`: invalidate-only qua `*FactInvalidated`, KHÔNG same-ID replacement — TOÀN BỘ payload là scope bất biến (canonical `initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS`, tái sử dụng đúng giá trị `strategy.md` §12, khai báo độc lập). `TradeIntentStatusChanged`: correction lineage chuẩn same-slice replacement, mười invariant đối xứng `strategy.md` §13. `DecisionRevalidated` (decision.md §5) KHÔNG phải correction — fact vận hành riêng cho Append-and-Revalidate policy (ADR-010 §2.6/Chapter 8 §8.4.1), causally trỏ `DecisionRecorded` gốc, ghi outcome SUCCEEDED/STALE/REJECTED cùng registry/frontier evidence đã dùng. Preservation fact trên canonical Audit Stream (Chapter 8 §8.4.1 mục 6, khi target stream retired tại registry transition) — RULE pin, event type cụ thể deferred (Phase 1, cần Stream Registry/Audit Stream infrastructure chưa tồn tại).

### C3 eligibility integration

`DecisionRecorded` CHỈ phát khi `eligible_for_new_computation(strategy_instance_id, decision_context_cursor) == true` (`strategy.md` §9a, sáu điều kiện) TẠI ĐÚNG `decision_context_cursor` — kiểm tra TRƯỚC khi đánh giá rule. Chín-field Strategy evidence (`strategy.md` §10) copy làm scalar bất biến trên Decision, resolve từ authoritative event stream TẠI cursor (KHÔNG Current View latest-state nào).

### Context Map integration

Đăng ký capability `decision-management` + context `strategy-decision` (`owned_contracts: [decision, trade-intent]`, HAI file CÙNG một context) tại `context-map.yaml` **v0.13 → v0.14**. KHÔNG thêm relationship edge nào — `decision.md`/`trade-intent.md` chỉ dùng simple `ref:` lookup (`strategy_instance_id`, `account_id`) và `event_record_ref` opaque chưa gắn provider context cụ thể (input evidence, deferred).

### Acceptance-scenario results (validation, decision.md §16)

Scenario A (EMA strict cross LONG): `result=LONG`, `trade_intent_outcome=ISSUED` — pass theo thiết kế. Scenario B (already above, no cross): `previous_condition_met=false` → `result=NO_ACTION`, zero Trade Intent — pass. Scenario C (configuration difference EMA50 vs EMA100): hai `DecisionRecorded` riêng biệt, `reference_series_period` làm rõ khác biệt — pass. Scenario D (future correction hidden): chặn bởi relational invariant `input_event.recorded_time ≤ cursor.recorded_time` — pass. Scenario E (Strategy ineligible): `eligible_for_new_computation=false` → KHÔNG DecisionRecorded, KHÔNG event riêng cần thiết (deterministic qua strategy.md §9a) — pass. Scenario F (exact executable difference): `package_build_artifact_ref` khác trên hai DecisionRecorded dù mọi field khác giống hệt — distinguishable tường minh trong evidence — pass. Scenario G (correction): `DecisionFactInvalidated`/`TradeIntentFactInvalidated` append-only, KHÔNG rewrite gốc, KHÔNG same-ID replacement, KHÔNG leak-forward — pass.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10 (đặc biệt Chapter 5 §5.2/§5.3, Chapter 8 §8.1.1/§8.2/§8.4/§8.4.1/§8.5, I-1/I-2/I-3/I-4), ADR-010 Approved (byte-for-byte unchanged — verified), ADR-013 v0.3 Approved (byte-for-byte unchanged — verified, qua strategy.md), Package 0.2-C1 (`instrument.md`/`venue.md` không đổi — verified byte-for-byte), Package 0.2-C2 (`account.md` không đổi), Package 0.2-C3 (`strategy.md` không đổi). Preserve nguyên vẹn: opaque non-derived identity pattern; invalidate-only-no-replacement cho immutable-scope subject; correction lineage mười invariant cho status-change event; fold algorithm "visible-valid-head per slice"; Current View never-authority. Không order type/limit price/stop price/exchange payload. Không position sizing/capital allocation/portfolio arbitration. Không DSL/executable strategy code. Không optimizer/backtest infrastructure. Không Risk approval/rejection semantics.

### Author self-review

Phát hiện và disclosure tường minh: task gốc dùng tên field "computation_cursor"/"evaluation_time" như placeholder — self-review xác nhận ADR-010 (Approved) + Chapter 8 §8.4 (Locked) đã khóa sẵn tên field chính xác là `decision_context_cursor`/`decision_time` cho MỌI Decision event, không thể tự đặt tên khác mà không vi phạm controlling architecture đã Approved; đã dùng đúng tên ADR-010/Chapter 8 quy định, ghi nhận công khai tại `decision.md` §2/§10 phần mở đầu và tại đây. Không tìm thấy finding blocking nào khác trong self-review.

### Changed-file scope

```text
docs/domain/decision.md        NEW      v0.1  Draft   blob c5b6226dcf46adf2a184ddefef6eca6a222f10da
docs/domain/trade-intent.md    NEW      v0.1  Draft   blob 27647dfd3538fd563ae332f6edaecd1c6eb59d97
docs/domain/context-map.yaml   MODIFIED v0.13 → v0.14  (capability/context registration + comment)
docs/domain/README.md          MODIFIED v0.37 → v0.38
docs/MANIFEST.md               MODIFIED manifest_version 9.63 → 9.64
docs/CHANGELOG.md              MODIFIED (this entry)
```

### Metadata / state

- `decision.md`/`trade-intent.md`: **tạo mới**, `version: "0.1"`, `status: Draft`, `approved_by: null`, `approved_at: null`.
- `context-map.yaml`: **v0.13 → v0.14** — thêm capability `decision-management` + context `strategy-decision`, KHÔNG thêm relationship edge.
- `README.md` (domain index): **v0.37 → v0.38**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.63 → 9.64**; dòng `domain/` cập nhật ghi nhận Package 0.2-C4 authoring transaction.
- `ADR-010.md`, `ADR-013.md`, `ADR-012.md`, `instrument.md`, `venue.md`, `account.md`, `strategy.md`: **không đổi** (byte-for-byte, verified).
- Mọi ADR khác, Constitution, mọi Domain Contract khác (`candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, `context.md`): **không đổi.**

**Package 0.2-C4 CHƯA đạt `Consolidated Stable` — chờ ChatGPT Review A + Independent Review B trên cùng exact baseline này.** Mandatory sequence: Author baseline → ChatGPT Review A → Independent Review B → merge finding → một correction commit (Product Owner authorize) → delta review hai vòng → Product Owner consolidation decision. KHÔNG correction dựa trên một review đơn lẻ. Package 0.2-C1/C2/C3 vẫn `Consolidated Stable`, không đổi. Package 0.2-C5–C7 vẫn chưa authorize, chưa author. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — consolidate Package 0.2-C3

**Package 0.2-C3 Strategy Foundation consolidated as `Consolidated Stable`.** Vai trò: `Package Lifecycle Consolidation Author · Repository Transaction Executor`. Product Owner authorized: "Package 0.2-C3 consolidation transaction" (2026-07-30). Authorization này cho phép ghi Package 0.2-C3 vào lifecycle state `Consolidated Stable` — nó KHÔNG cho phép Approve/Lock `strategy.md`, không sửa ADR-013 hay bất kỳ ADR nào, không sửa Constitution, không đóng OQ, không authorize Live, không author/authorize Package 0.2-C4–C7, không thêm speculative edge case, không tuyên bố Phase 0.2 hoàn thành.

### Baseline verification

```text
Expected HEAD:  922723e459ea6418d66d9cacbd83d849844c6958
Actual HEAD:    922723e459ea6418d66d9cacbd83d849844c6958  — match

strategy.md:       v0.3 Draft, blob c2cadc464bc8baecff41ff8079461ec0d5dfaccc  — match
context-map.yaml:  v0.13 Draft, blob 5f32edd625f4b66e179dff752d45b301642d76fd  — match
README.md:         v0.36 Draft, blob 76ba42693efb69a63a503e45d1115eed436eccd5  — match
MANIFEST.md:       manifest_version 9.62, blob fa585d2f0aee1274b6bd308f0519f409efe20fce  — match
ADR-013.md:        v0.3 Approved, blob 02df931143f8408c61d19ee2c91d2d355d5deb1d  — match
```

### Reviewed baseline pinned

```text
Package 0.2-C3 reviewed HEAD:  922723e459ea6418d66d9cacbd83d849844c6958

Primary artifact:        strategy.md v0.3 Draft, blob c2cadc464bc8baecff41ff8079461ec0d5dfaccc
Controlling architecture: ADR-013.md v0.3 Approved, blob 02df931143f8408c61d19ee2c91d2d355d5deb1d (unchanged)
Integration artifact:    context-map.yaml v0.13 Draft, blob 5f32edd625f4b66e179dff752d45b301642d76fd (unchanged)
Registry baseline:       MANIFEST v9.62, blob fa585d2f0aee1274b6bd308f0519f409efe20fce
```

### Review evidence

```text
ChatGPT final focused delta re-review:        Clean — 0 blocking finding
Independent Review B final focused delta re-review:  Clean — 0 blocking finding
```

### Complete finding ledger — all resolved (v0.1 → v0.2 bounded correction, v0.2 → v0.3 micro-correction)

```text
C3-MAJ-01:        Resolved (instrument_selection_ref pin {instrument_id, venue_id, listing_id}, resolve same-cursor C1 history, không Selection aggregate)
C3-MAJ-02:        Resolved (Definition Version VALID required cho computation mới, không auto-cascade Instance lifecycle, §9a)
C3-MAJ-03:        Resolved (Account ACTIVE required cho computation mới, không auto-cascade Instance lifecycle, §9a)
C3-MAJ-04:        Resolved (bốn trục evidence phải resolvable tại cursor, unresolvable ⟹ ineligible, không proxy, §9a/§11)
C3-MIN-01:        Resolved (strategy_definition_id gán tại Version đầu gia đình, không tái sử dụng cross-family, §1)
C3-MIN-02:        Resolved (unified rule eligible_for_new_computation, sáu điều kiện AND cùng cursor, §9a/§12)
C3-DELTA-MAJ-01:   Resolved (instrument_selection_ref shape consistency — §9/§10 sửa object, đồng nhất sáu vị trí)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

### Package lifecycle meaning

`Consolidated Stable` là package lifecycle/readiness state — nghĩa là: reviewed package baseline nội bộ coherent; mọi qualifying finding đã resolved; deferred limitations được ghi nhận tường minh là non-blocking Phase 1 concern; package integration đủ ổn định để làm dependency baseline cho package kế tiếp (0.2-C4). Nó KHÔNG có nghĩa: artifact Approved; artifact Locked; ADR-013 thay đổi; Domain Contract bất biến; OQ closure; Phase completion; implementation authorization; Live authorization.

### Unchanged artifact statuses

`strategy.md`: **giữ nguyên** `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte — không sửa Domain Contract semantic trong transaction này. `context-map.yaml`: **giữ nguyên** `version: "0.13"`, `status: Draft`, byte-for-byte — không sửa. `ADR-013.md`: **giữ nguyên** `version: "0.3"`, `status: Approved`, byte-for-byte — không sửa. `instrument.md`/`venue.md`/`account.md`/`ADR-012.md`: **giữ nguyên**, byte-for-byte — không sửa.

### Package lifecycle states pinned

```text
Package 0.2-C1:     Consolidated Stable
Package 0.2-C2:     Consolidated Stable
Package 0.2-C3:     Consolidated Stable
Package 0.2-C4–C7:  unauthorized, unauthored
```

### Artifact lifecycle states pinned

```text
strategy.md:  Draft, version "0.3", approved_by: null, approved_at: null, not Locked
```

### Changed-file scope

```text
docs/domain/README.md          MODIFIED v0.36 → v0.37
docs/MANIFEST.md               MODIFIED manifest_version 9.62 → 9.63
docs/CHANGELOG.md              MODIFIED (this entry)
docs/domain/strategy.md        KHÔNG ĐỔI — blob c2cadc464bc8baecff41ff8079461ec0d5dfaccc, verified byte-identical
docs/domain/context-map.yaml   KHÔNG ĐỔI — blob 5f32edd625f4b66e179dff752d45b301642d76fd, verified byte-identical
docs/adr/ADR-013.md            KHÔNG ĐỔI — blob 02df931143f8408c61d19ee2c91d2d355d5deb1d, verified byte-identical
```

### Metadata / state

- `strategy.md`, `context-map.yaml`, `ADR-013.md`: **không đổi** (semantic và version) — package lifecycle metadata only.
- `README.md` (domain index): **v0.36 → v0.37**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.62 → 9.63**; dòng `domain/` cập nhật ghi nhận Package 0.2-C3 `Consolidated Stable`.
- Mọi Domain Contract khác (`instrument.md`, `venue.md`, `account.md`, `candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, `context.md`), mọi ADR file, Constitution: **không đổi.**

**Package 0.2-C4 baseline dependency đã thỏa, eligible cho Product Owner scope authorization — CHƯA bắt đầu, CHƯA author, KHÔNG được authorize bởi transaction này.** Package 0.2-C5–C7 gate chưa mở. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — align Package 0.2-C3 instrument selection shape

**Package 0.2-C3 micro-correction — C3-DELTA-MAJ-01 only.** Vai trò: `Domain Contract Micro-Correction Author`. Product Owner authorized: "Package 0.2-C3 micro-correction — C3-DELTA-MAJ-01 only." Đóng đúng một finding Major: `C3-DELTA-MAJ-01` (repository-wide `instrument_selection_ref` shape consistency). Authorization này **không** cho phép đổi eligibility semantics, identity, lifecycle, correction/replay semantics, bốn trục evidence, sửa ADR-013 hay bất kỳ ADR nào, sửa C1/C2 artifacts, author C4–C7, tạo Selection aggregate, thêm multi-instrument support, Approve/Lock/Consolidate C3, đóng OQ-002/OQ-003, hay authorize Live.

### Baseline verification

```text
Expected HEAD:  cc6df3bfa1d6be5716e48c75056c1b9209acd4d2
Actual HEAD:    cc6df3bfa1d6be5716e48c75056c1b9209acd4d2  — match

strategy.md:  v0.2 Draft, blob eaedbc63411501262cebd3e16fe1c9b5c0062ac3  — match
```

### C3-DELTA-MAJ-01 — repository-wide shape consistency

`strategy.md` §5 (entity schema), §2 (envelope `subject_ref.scope`), và §6 (`StrategyInstanceRegistered` payload) đã pin `instrument_selection_ref` là object `{instrument_id, venue_id, listing_id}` từ v0.2 (đóng `C3-MAJ-01`) — nhưng HAI vị trí còn sót lại vẫn khai báo scalar `string`: (1) §9 `StrategyInstanceCurrentView.scope` — compact inline flow-mapping field `instrument_selection_ref: string`; (2) §10 C4 downstream reference contract — `instrument_selection_ref: {type: string, ...}`. Cả hai thay bằng đúng object shape `{instrument_id, venue_id, listing_id}`, mỗi sub-field `string`/`required: true`. §9's `scope` giữ nguyên compact inline flow-mapping style (chỉ nest thêm object cho đúng một field, không reformat năm field còn lại), đúng precedent `account.md`'s `account_boundary_ref` compact reference. §10 mở rộng thành multi-line `type: object / required: true / fields: {...}` block, đúng style §5, cộng pin tường minh "C4 PHẢI tiêu thụ object này TRỰC TIẾP — KHÔNG serialize thành string, KHÔNG dùng opaque proxy ID, KHÔNG dùng tagged reference thay thế, KHÔNG mở rộng thành Selection aggregate hay multi-instrument cardinality." Rule `scope` chỉ tồn tại khi `view_state = VALID` (§9) giữ nguyên, không đổi.

### Repository-wide `instrument_selection_ref` consistency check (trong `strategy.md`)

```text
§2  subject_ref.scope (envelope)              — object {instrument_id, venue_id, listing_id}  ✓ (v0.2, không đổi)
§5  Strategy Instance entity schema           — object {instrument_id, venue_id, listing_id}  ✓ (v0.2, không đổi)
§6  StrategyInstanceRegistered payload        — object {instrument_id, venue_id, listing_id}  ✓ (v0.2, không đổi)
§9  StrategyInstanceCurrentView.scope         — object {instrument_id, venue_id, listing_id}  ✓ (v0.3, đóng C3-DELTA-MAJ-01)
§9a unified eligibility rule (prose ref)      — tham chiếu instrument_selection_ref generic, không declare type — không cần sửa
§10 C4 downstream reference contract          — object {instrument_id, venue_id, listing_id}  ✓ (v0.3, đóng C3-DELTA-MAJ-01)

grep "instrument_selection_ref: string" strategy.md   → 0 match
grep "instrument_selection_ref: {type: string"        → 0 match
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

### Confirmation of no unrelated semantic changes

Không đổi: eligibility semantics (§9a sáu điều kiện giữ nguyên); identity (`strategy_instance_id`/`strategy_definition_id`/`strategy_definition_version_id` không chạm); lifecycle (`ACTIVE`/`PAUSED`/`RETIRED`, transition table không đổi); correction/replay semantics (correction lineage §13, fold algorithm §9 không đổi); bốn trục evidence (§11 không đổi); ADR-013 (byte-for-byte unchanged — verified); C1/C2 artifacts (`instrument.md`/`venue.md`/`account.md` byte-for-byte unchanged — verified). Cardinality vẫn đúng MỘT TradableListing — không Selection aggregate, không multi-instrument. Diff duy nhất: 2 vị trí `instrument_selection_ref` scalar → object, cộng một đoạn version-history prose ghi nhận v0.3.

### Changed-file scope

```text
docs/domain/strategy.md   MODIFIED v0.2 → v0.3   blob c2cadc464bc8baecff41ff8079461ec0d5dfaccc
docs/domain/README.md     MODIFIED v0.35 → v0.36
docs/MANIFEST.md          MODIFIED manifest_version 9.61 → 9.62
docs/CHANGELOG.md         MODIFIED (this entry)
docs/domain/context-map.yaml   KHÔNG ĐỔI (không semantic Context Map change được authorize)
```

### Metadata / state

- `strategy.md`: **v0.2 → v0.3**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `context-map.yaml`: **không đổi** — không có version-only metadata convention nào strictly require bump cho một shape-only fix không chạm capability/context/relationship.
- `README.md` (domain index): **v0.35 → v0.36**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.61 → 9.62**; dòng `domain/` cập nhật ghi nhận micro-correction.
- `ADR-013.md`, `ADR-012.md`, `instrument.md`, `venue.md`, `account.md`: **không đổi** (byte-for-byte, verified).
- Mọi ADR khác, Constitution, mọi Domain Contract khác: **không đổi.**

**Package 0.2-C3 CHƯA đạt `Consolidated Stable` — chờ focused delta re-review (ChatGPT + Independent Review B) trên cùng exact baseline micro-correction này.** Mandatory sequence tiếp tục: focused delta re-review → Product Owner consolidation decision. KHÔNG correction thêm dựa trên một review đơn lẻ. Package 0.2-C1/C2 vẫn `Consolidated Stable`, không đổi. Package 0.2-C4–C7 vẫn chưa authorize, chưa author. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — correct Package 0.2-C3 strategy eligibility

**Package 0.2-C3 bounded correction — consolidated Review A + Independent Review B findings.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C3 bounded correction — consolidated Review A + Independent Review B findings." Đóng đúng bốn finding Major: `C3-MAJ-01` (concrete instrument selection), `C3-MAJ-02` (Definition Version validity), `C3-MAJ-03` (Account eligibility), `C3-MAJ-04` (evidence-reference resolvability); cộng hai finding Minor: `C3-MIN-01` (Strategy Definition family identity), `C3-MIN-02` (unified computation-eligibility rule). Authorization này **không** cho phép sửa ADR-013 hay bất kỳ ADR nào, sửa C1/C2 semantics, tạo Strategy family aggregate, tạo Selection/universe aggregate, author C4–C7, định nghĩa strategy DSL/executable code, thiết kế registry/retention infrastructure, thêm capital allocation/multi-strategy arbitration, thêm Live activation workflow, sửa Constitution, đóng OQ-002/OQ-003, Approve/Lock/Consolidate bất kỳ artifact/package nào, hay authorize Live.

### Baseline verification

```text
Expected HEAD:  a4346ca6df54c74b70438488c676171b8eebac55
Actual HEAD:    a4346ca6df54c74b70438488c676171b8eebac55  — match

strategy.md:       v0.1 Draft, blob 66b9b8226f18ff3e39506d22df68e5940b91746d  — match
ADR-013.md:        v0.3 Approved, blob 02df931143f8408c61d19ee2c91d2d355d5deb1d  — match
context-map.yaml:  v0.12 Draft, blob fc237c51a23c8b46a0bb4b4997fcaa851edae4ac  — match
README.md:         v0.34 Draft, blob 5f1a9616c95d85917bc6551e6e9453f685100956  — match
MANIFEST.md:       manifest_version 9.60, blob f2b0dd084a640c7e8c01a8de76f9738fbdd5d8d4  — match
```

### C3-MAJ-01 — Concrete instrument selection

`instrument_selection_ref` v0.1 là opaque string, shape deferred — C4 sẽ phải tự phát minh format. v0.2 pin shape cụ thể `{instrument_id, venue_id, listing_id}` (`strategy.md` §5 schema + §2 envelope subject_ref.scope + §6 payload), đối xứng ba field scope của `TradableListing` (`instrument.md` §10). Pin: đúng MỘT listing per Strategy Instance (bất biến cùng toàn bộ scope, không multi-instrument); cả ba field bắt buộc; resolve từ authoritative C1 event stream (`InstrumentRegistered`/`VenueRegistered`/`TradableListingCreated`) TẠI cùng cursor, KHÔNG dùng `InstrumentCurrentView`/`VenueCurrentView`/`TradableListingCurrentView` latest-state làm input; Instrument/Venue/TradableListing phải ELIGIBLE (`instrument.md` §15 `eligibility_state`) tại computation cursor (§9a). `StrategyInstanceRegistered` (§6) thêm invariant causation_refs phải trỏ `TradableListingCreated` của `listing_id`, đối xứng invariant Account đã có. Multi-instrument set/universe/dynamic selection vẫn deferred (§14). KHÔNG tạo Selection aggregate — `instrument_selection_ref` vẫn là compound scope field trên chính Strategy Instance.

### C3-MAJ-02 — Definition Version validity

Thêm vào §9a (mới): computation MỚI chỉ eligible khi `strategy_definition_version_ref` `VALID` (`GetStrategyDefinitionVersionValidity`, §4) tại computation cursor. Khi invalidation trở nên visible: cấm computation mới; Strategy Instance's `current_status`/state_machine (§5) KHÔNG tự động pause/retire (không cascade tự động); computation lịch sử trước invalidation cursor giữ nguyên authoritative (đúng Chapter 9 §9.3 "lifecycle transitions must never invalidate already-computed Decision evidence"); Definition Version đã sửa PHẢI dùng cho một `strategy_instance_id` MỚI (`strategy_definition_version_ref` là scope bất biến trên Instance, không rebind tại chỗ — giữ nguyên "immutable Instance binding").

### C3-MAJ-03 — Account eligibility

Thêm vào §9a: computation MỚI chỉ eligible khi Account (`account_id`, reconstruct authoritative TẠI cùng cursor) `current_status = ACTIVE`. Khi SUSPENDED/CLOSED: cấm computation mới; Strategy Instance lifecycle KHÔNG tự động mutate (không cascade tự động); historical evidence giữ nguyên; `strategy.md` KHÔNG author Order/Position/recovery behavior nào (thuộc phạm vi C4–C7, chưa author). `environment` vẫn LUÔN resolve từ Account tại cùng cursor bất kể Account ACTIVE/SUSPENDED/CLOSED (bất biến, không phải điều kiện có thể fail độc lập).

### C3-MAJ-04 — Evidence-reference resolvability

Thêm vào §9a/§11: cả bốn trục evidence (`strategy_definition_version_ref`/`plugin_version_ref`/`configuration_version_ref`/`package_build_artifact_ref`) PHẢI persistently resolvable tại computation cursor (Chapter 8 §8.1.1 mục 4). Nếu bất kỳ trục nào không resolvable: computation mới deterministically ineligible; KHÔNG mutable-latest, KHÔNG inferred fallback, KHÔNG proxy reference; Strategy Instance KHÔNG bị mutate; historical evidence giữ nguyên. KHÔNG thiết kế registry/retention infrastructure hay recovery mechanism (Phase 1, §14) — chỉ pin RULE hệ quả.

### C3-MIN-01 — Strategy Definition family identity

`strategy_definition_id` (§1) thắt chặt: opaque, globally unique, stable — gán tại Version ĐẦU TIÊN của một gia đình Strategy logic; KHÔNG BAO GIỜ tái sử dụng cho gia đình khác; Version sau chỉ được mang lại cùng ID khi thuộc CÙNG gia đình logic (kỷ luật tác giả/operator, Phase 1). KHÔNG tạo family aggregate, family registration event, version graph, hay approval workflow — vẫn thuần là scope field.

### C3-MIN-02 — Unified computation-eligibility rule

Section MỚI `### 9a. Computation eligibility — unified rule` (giữa §9 và §10, cùng convention `feature.md` §9a — không renumbering section nào khác). Pin MỘT normative derived rule `eligible_for_new_computation`, AND-conjunction sáu điều kiện cùng computation cursor C: Strategy Instance `current_status == ACTIVE`; `strategy_definition_version_ref` `VALID`; Account `current_status == ACTIVE`; Account `environment` resolve nhất quán; cả bốn trục evidence resolvable; `instrument_selection_ref` resolve đúng một TradableListing `ELIGIBLE`. Canonical policy identifier mới tại §12: `computation_eligibility_policy: ALL_CONDITIONS_TRUE_AT_SAME_CURSOR`. Rule thuộc Strategy eligibility ONLY — `strategy.md` KHÔNG author Trade Intent/Decision/Risk/Execution behavior, KHÔNG tự enforce (chưa có consumer). Convenience query non-authoritative `GetStrategyInstanceComputationEligibility` thêm cho tiện query/UI, cùng nguyên tắc Current-View-never-authority.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10 (đặc biệt Chapter 8 §8.1.1, Chapter 9 §9.3), ADR-010 §75, ADR-013 v0.3 Approved (byte-for-byte unchanged — verified), Package 0.2-C1 (`instrument.md`/`venue.md` không đổi — verified byte-for-byte), Package 0.2-C2 (`account.md` không đổi — verified byte-for-byte). Preserve nguyên vẹn: Strategy Definition Version/Strategy Instance separation; bốn trục evidence độc lập; immutable Instance binding; lifecycle ACTIVE/PAUSED/RETIRED; RETIRED forward terminality; status correction lineage; no-mutable-latest; same-cursor authoritative reconstruction; Current View non-authority; một file `strategy.md` duy nhất. Không owner/tenant/IAM/billing semantics mới. Không Strategy DSL/executable code. Không optimizer/backtest engine. Không capital allocation/multi-strategy arbitration. Không Live activation workflow. Không Strategy family aggregate. Không Selection/universe aggregate.

### Complete finding ledger — all resolved (bounded correction, v0.1 → v0.2)

```text
C3-MAJ-01:  Resolved (instrument_selection_ref pin {instrument_id, venue_id, listing_id}, resolve same-cursor C1 history, không Selection aggregate)
C3-MAJ-02:  Resolved (Definition Version VALID required cho computation mới, không auto-cascade Instance lifecycle, §9a)
C3-MAJ-03:  Resolved (Account ACTIVE required cho computation mới, không auto-cascade Instance lifecycle, §9a)
C3-MAJ-04:  Resolved (bốn trục evidence phải resolvable tại cursor, unresolvable ⟹ ineligible, không proxy, §9a/§11)
C3-MIN-01:  Resolved (strategy_definition_id gán tại Version đầu gia đình, không tái sử dụng cross-family, §1)
C3-MIN-02:  Resolved (unified rule eligible_for_new_computation, sáu điều kiện AND cùng cursor, §9a/§12)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

### Author self-review

Không tìm thấy finding blocking nào khác trong self-review. Xác nhận: §9a chèn dạng sub-heading (`### 9a.`) đúng precedent `feature.md` §9a — KHÔNG renumbering §10–§16, mọi `§N` citation nội bộ đã rescan và khớp đúng heading thực tế. Xác nhận YAML fenced block (11 block, bao gồm hai schema nested mới `instrument_selection_ref`) parse sạch, đúng style `account_boundary_ref` precedent (`account.md` §1). Xác nhận `instrument_selection_ref` shape đối xứng đúng ba field scope `TradableListing` (`instrument.md` §10), không tự phát minh shape khác.

### Changed-file scope

```text
docs/domain/strategy.md        MODIFIED v0.1 → v0.2    blob eaedbc63411501262cebd3e16fe1c9b5c0062ac3
docs/domain/context-map.yaml   MODIFIED v0.12 → v0.13  (comment-only, không relationship edge mới)
docs/domain/README.md          MODIFIED v0.34 → v0.35
docs/MANIFEST.md               MODIFIED manifest_version 9.60 → 9.61
docs/CHANGELOG.md              MODIFIED (this entry)
```

### Metadata / state

- `strategy.md`: **v0.1 → v0.2**, `status: Draft`, `approved_by: null`, `approved_at: null` không đổi.
- `context-map.yaml`: **v0.12 → v0.13** — chỉ sửa comment ghi nhận finding closure, không thêm relationship edge.
- `README.md` (domain index): **v0.34 → v0.35**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.60 → 9.61**; dòng `domain/` cập nhật ghi nhận Package 0.2-C3 bounded correction.
- `ADR-013.md`, `ADR-012.md`, `instrument.md`, `venue.md`, `account.md`: **không đổi** (byte-for-byte, verified).
- Mọi ADR khác, Constitution, mọi Domain Contract khác: **không đổi.**

**Package 0.2-C3 CHƯA đạt `Consolidated Stable` — chờ ChatGPT delta Review A + Independent Review B trên cùng exact baseline correction này.** Mandatory sequence tiếp tục: delta review hai vòng → Product Owner consolidation decision. KHÔNG correction thêm dựa trên một review đơn lẻ. Package 0.2-C1/C2 vẫn `Consolidated Stable`, không đổi. Package 0.2-C4–C7 vẫn chưa authorize, chưa author. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — author Package 0.2-C3 strategy foundation

**Package 0.2-C3 — Strategy Foundation v0.1 authored.** Vai trò: `Domain Contract Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C3 — Strategy Foundation v0.1". Authorized artifact: `docs/domain/strategy.md` (tạo mới, v0.1 Draft). Authorization này **không** cho phép author Package 0.2-C4–C7, định nghĩa strategy DSL/executable code, optimizer/backtest engine, capital allocation/multi-strategy arbitration, Live activation workflow, sửa C1/C2 semantic, sửa ADR-013 hay bất kỳ ADR/Constitution nào, đóng OQ-002/OQ-003, Approve/Lock/Consolidate bất kỳ artifact/package nào, hay authorize Live.

### Baseline verification

```text
Expected HEAD:  05ff2d4fd8afea3825378aee2d286434df17b410
Actual HEAD:    05ff2d4fd8afea3825378aee2d286434df17b410  — match

Package 0.2-C1:  Consolidated Stable (không đổi)
Package 0.2-C2:  Consolidated Stable (không đổi)
Controlling architecture: ADR-013.md v0.3 Approved, blob 02df931143f8408c61d19ee2c91d2d355d5deb1d
strategy.md: absent trước transaction — đúng expected state, KHÔNG có baseline conflict (khác tình huống ADR-012 tại Package 0.2-C2)
```

### Strategy Definition Version model

`strategy_definition_version_id` — opaque, globally unique, immutable, gán tại `StrategyDefinitionVersionRegistered`, KHÔNG derive từ nội dung hay từ `strategy_definition_id` (áp dụng chủ động bài học `C2-MAJ-01`, không chờ review round phát hiện). `strategy_definition_id` là scope field nhóm nhiều Version cùng một gia đình chiến lược — KHÔNG có registration event riêng cho family (khác Account/Instrument, tránh phát minh cơ chế không cần thiết). TOÀN BỘ payload một Version (`thesis`, `supported_scope`, `required_input_contracts`, `decision_rule_ref`, `explanation_contract_ref`, `downstream_output_capability`) là nội dung BẤT BIẾN — KHÔNG có PATCH/metadata-revision event, đúng ADR-013 §2.3 cấm mutable-latest tường minh. Correction (`StrategyDefinitionVersionFactInvalidated`) LUÔN LUÔN đăng ký một `strategy_definition_version_id` MỚI — KHÔNG có same-ID replacement path (đơn giản hơn model METADATA_ERROR/SCOPE_ERROR hai lớp của `account.md`, vì subject này không có mutable metadata để phân biệt). KHÔNG có "current/latest Definition" read model — chỉ một validity-check non-authoritative (`GetStrategyDefinitionVersionValidity`) cho một ID cụ thể đã biết, tránh vi phạm ADR-013 §2.3 dù chỉ về mặt read-model semantics.

### Strategy Instance model

`strategy_instance_id` — opaque, globally unique, immutable. Pin ĐỦ bốn trục evidence độc lập (`strategy_definition_version_ref`/`plugin_version_ref`/`configuration_version_ref`/`package_build_artifact_ref`), cộng `account_id` (đúng một Account) và `instrument_selection_ref`. Toàn bộ scope bất biến một khi đăng ký — đổi bất kỳ trục nào tạo Instance khác, KHÔNG mutate tại chỗ (đúng Chapter 9 §9.3 mục 2). Lifecycle tối thiểu ba state `ACTIVE`/`PAUSED`/`RETIRED` — RETIRED terminal CHO FORWARD TRANSITION nhưng correctable append-only qua `StrategyInstanceFactInvalidated` + same-slice replacement; `supersedes_fact_ref` có mặt ngay từ v0.1 trên `StrategyInstanceStatusChanged` (áp dụng chủ động bài học `C2-MAJ-02`). `StrategyInstanceCurrentView` (optional, non-authoritative) dùng fold algorithm "visible-valid-head per slice" và pin "Current View không bao giờ authority" ngay từ v0.1 (áp dụng chủ động bài học `C2-MAJ-03`/`C2-MAJ-04`).

### ADR-013 four-axis conformance

Bốn trục evidence — Strategy Definition Version (`strategy.md`, §1) · Plugin Version (Chapter 9 §9.1) · Configuration Version (Chapter 9 §9.1) · Package/Build Artifact (Chapter 9 §9.1, ADR-013 §2.5) — pin độc lập tường minh tại `strategy.md` §5/§11: không trục nào derive/proxy trục khác; mỗi trục bump độc lập (refactor Plugin không bắt buộc Definition Version mới; đổi thesis không bắt buộc Plugin Version mới). Rebuilt-artifact-identity rule (ADR-013 §2.5) pin nguyên văn: hai executable artifact khác bytes vì bất kỳ lý do gì (kể cả non-reproducible build) PHẢI có `package_build_artifact_ref` khác. Capability/instrument-class vs. concrete-instrument (ADR-013 §2.2) pin qua `supported_scope` (Definition Version, class) vs. `instrument_selection_ref` (Instance, concrete). Immutable-pin/no-mutable-latest (ADR-013 §2.3) pin qua việc KHÔNG có PATCH event và KHÔNG có "current definition" read model. `ADR-013.md` **byte-for-byte unchanged, verified** — không sửa/re-author/bump.

### Account/environment/instrument binding

Một quy tắc ownership duy nhất (đúng yêu cầu task): `instrument_selection_ref` thuộc Strategy Instance — KHÔNG thuộc Configuration Version. `environment` KHÔNG lưu riêng trên Instance — luôn resolve qua `account_id` → Account event stream (`account.md` §1) TẠI cùng cursor, tránh duplicate source of truth (I-12), đồng thời thỏa yêu cầu "Account và environment phải resolve từ authoritative same-cursor history" bằng derivation thay vì lưu trữ dư thừa. `environment: LIVE` (kế thừa) KHÔNG tự động authorize Live execution — domain value phân biệt thuần túy, đúng nguyên tắc `account.md` §8.

### Lifecycle and correction model

`StrategyDefinitionVersionRegistered`/`StrategyInstanceRegistered`: TOÀN BỘ payload bất biến — correction (`*FactInvalidated`) LUÔN đăng ký ID mới, KHÔNG same-ID replacement, KHÔNG cần `pending_correction_class` phân biệt cho registration lineage (chỉ một outcome: `TERMINAL_SCOPE_INVALIDATION`). `StrategyInstanceStatusChanged`: correction lineage chuẩn — same-slice replacement qua `supersedes_fact_ref`, mười invariant chuẩn (đúng pattern đã proven `instrument.md`/`account.md`) áp dụng nguyên vẹn, RETIRED correctable không cần reactivation command riêng. Canonical policy identifier mới khai báo tại `strategy.md` §12 (context `strategy-definition`, độc lập, không cross-reference context khác): `initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS`, `strategy_evidence_axis_policy: FOUR_INDEPENDENT_AXES_NO_PROXY`.

### C4 downstream reference boundary

Chín field pin tại `strategy.md` §10: `strategy_instance_id`/`strategy_definition_id`/`strategy_definition_version_id`/`plugin_version_ref`/`configuration_version_ref`/`package_build_artifact_ref`/`account_id`/`environment` (derived)/`instrument_selection_ref` — resolve TRỰC TIẾP từ authoritative event stream TẠI cùng cursor, `StrategyInstanceCurrentView` latest-state KHÔNG BAO GIỜ là input hợp lệ (đúng "một quy tắc downstream authority duy nhất" đã proven tại `account.md` §13, áp dụng chủ động ngay từ v0.1). `strategy.md` KHÔNG author Trade Intent/Decision semantics (Package 0.2-C4, chưa authorize).

### Context Map integration

Đăng ký capability `strategy-management` + context `strategy-definition` (`owned_contracts: [strategy]`) tại `context-map.yaml` **v0.11 → v0.12**. KHÔNG thêm relationship edge nào — `strategy.md` chỉ dùng simple `ref:` lookup (`account_id` → Account, `strategy_definition_version_ref` → chính nó), không có published-language event-stream flow cross-context nào thực sự cần thiết ở v0.1, đúng precedent `account.md`'s `venue_id` ref không cần edge.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10 (đặc biệt Chapter 8 §8.1.1/§8.2, Chapter 9 §9.1/§9.3/§9.6/§9.8), ADR-010 §75, ADR-013 v0.3 Approved (byte-for-byte unchanged — verified), Package 0.2-C1 (`instrument.md`/`venue.md` không đổi — verified byte-for-byte), Package 0.2-C2 (`account.md` không đổi — verified byte-for-byte), ADR-012 (byte-for-byte unchanged — verified). Preserve nguyên vẹn: opaque non-derived identity pattern; `EXPLICIT_PATCH_WITH_CLEAR_SET`-style thinking áp dụng đúng chỗ (ở đây: KHÔNG áp dụng, vì subject bất biến — quyết định tường minh, không phải bỏ sót); correction lineage mười invariant; fold algorithm "visible-valid-head per slice"; Current View never-authority. Không owner/tenant/IAM/billing semantics mới. Không Strategy DSL/executable code. Không optimizer/backtest engine. Không capital allocation/multi-strategy arbitration. Không Live activation workflow.

### Attack-scenario kết quả

Look-ahead injection (invalidation visible trước recorded_time gốc): chặn bởi envelope invariant §2/§4/§8. Invalidation-of-invalidation: chặn tường minh (§4/§8 invariant "không bao giờ trỏ một `*FactInvalidated` khác"). Same-ID mutation giả danh correction cho Definition Version/Instance registration: chặn — chỉ `*FactInvalidated` + ID mới được chấp nhận, không có `supersedes_fact_ref` trên hai event registration. Axis proxy injection (suy `plugin_version_ref` từ `configuration_version_ref` hay ngược lại): chặn tường minh bởi invariant §5/§11. Instrument-selection ownership ambiguity (Configuration Version tự nhận sở hữu `instrument_selection_ref`): chặn — một quy tắc ownership duy nhất pin tại §5. Environment duplication/drift (Instance tự lưu `environment` khác Account): chặn — `environment` không phải field lưu trữ trên Instance, chỉ derived. Current View dùng làm input tính toán: chặn tường minh §9/§10 (cùng cơ chế đã proven `account.md` §13).

### Author self-review findings

Phát hiện và disclosure tường minh (không phải finding cần sửa, chỉ là judgment call cần minh bạch): ADR-013 §2.1 mô tả `strategy-definition.md`/`strategy-instance.md` như hai tên file giả định tại thời điểm ADR được author — quyết định tổ chức file KHÔNG thuộc phạm vi ADR-013 (ADR chỉ khóa kiến trúc bốn-trục độc lập, không khóa Domain Contract file boundary). Product Owner đã xác nhận tường minh cho transaction này dùng MỘT file `strategy.md` duy nhất — không vi phạm ADR-013, chỉ là quyết định tổ chức tài liệu, ghi nhận công khai tại `strategy.md` phần mở đầu ("Ghi chú tổ chức file"). Không tìm thấy finding blocking nào khác trong self-review.

### Changed-file scope

```text
docs/domain/strategy.md        NEW      v0.1  Draft   blob 66b9b8226f18ff3e39506d22df68e5940b91746d
docs/domain/context-map.yaml   MODIFIED v0.11 → v0.12  (capability/context registration + comment)
docs/domain/README.md          MODIFIED v0.33 → v0.34
docs/MANIFEST.md               MODIFIED manifest_version 9.59 → 9.60
docs/CHANGELOG.md              MODIFIED (this entry)
```

### Metadata / state

- `strategy.md`: **tạo mới**, `version: "0.1"`, `status: Draft`, `approved_by: null`, `approved_at: null`.
- `context-map.yaml`: **v0.11 → v0.12** — thêm capability `strategy-management` + context `strategy-definition`, KHÔNG thêm relationship edge.
- `README.md` (domain index): **v0.33 → v0.34**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.59 → 9.60**; dòng `domain/` cập nhật ghi nhận Package 0.2-C3 authoring transaction.
- `ADR-013.md`, `ADR-012.md`, `instrument.md`, `venue.md`, `account.md`: **không đổi** (byte-for-byte, verified).
- Mọi ADR khác, Constitution, mọi Domain Contract khác (`candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, `context.md`): **không đổi.**

**Package 0.2-C3 CHƯA đạt `Consolidated Stable` — chờ ChatGPT Review A + Independent Review B trên cùng exact baseline này.** Mandatory sequence: Author baseline → ChatGPT Review A → Independent Review B → merge finding → một correction commit (Product Owner authorize) → delta review hai vòng → Product Owner consolidation decision. KHÔNG correction dựa trên một review đơn lẻ. Package 0.2-C1/C2 vẫn `Consolidated Stable`, không đổi. Package 0.2-C4–C7 vẫn chưa authorize, chưa author. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — consolidate Package 0.2-C2

**Package 0.2-C2 Trading Account Foundation consolidated as `Consolidated Stable`.** Vai trò: `Package Lifecycle Consolidation Author · Repository Transaction Executor`. Product Owner authorized: "Package 0.2-C2 consolidation transaction" (2026-07-30). Authorization này cho phép ghi Package 0.2-C2 vào lifecycle state `Consolidated Stable` — nó KHÔNG cho phép Approve/Lock `account.md`, không sửa ADR-012 hay bất kỳ ADR nào, không sửa Constitution, không đóng OQ, không authorize Live, không author/authorize Package 0.2-C3–C7, không thêm speculative edge case, không tuyên bố Phase 0.2 hoàn thành.

### Reviewed baseline pinned

```text
Package 0.2-C2 reviewed HEAD:  730c07c26c2917b6599e5faf213bdaf6f96b703d

Primary artifact:        account.md v0.2 Draft, blob 9fd2d0fb3235343d52c3435df3f1c7e08dd22781
Controlling architecture: ADR-012.md v0.3 Approved, blob 59eec21774478fc862e120d8a0f9285dc24eb720 (unchanged)
Integration artifact:    context-map.yaml v0.11 Draft, blob 51c5ea73e012b0b87061375046567cc2eedc8f95
Registry baseline:       MANIFEST v9.58, blob c4c1357f66f4d0521988bf29f4c8511dac8fe8fd
```

### Review evidence

```text
ChatGPT bounded delta Review A:  Clean — 0 blocking finding
Independent Review B:            Clean with deferred limitations — 0 blocking finding
```

Deferred limitations (Phase 1 implementation concern, non-blocking): credential binding implementation; runtime worker ownership; transaction boundaries; retry/backoff; monitoring and recovery; Broker Account Boundary details; onboarding/KYC; PAPER→LIVE promotion; custody, IAM and billing. Đây KHÔNG phải Domain Contract semantic gap — `account.md` pin RULE (identity, boundary, environment, lifecycle, correction lineage, downstream authority), không pin MECHANISM triển khai, đúng nguyên tắc defer đã nhất quán xuyên suốt `account.md` §14/§16. Không mở rộng thành Domain Contract semantic mới.

### Complete finding ledger — all resolved (bounded correction, v0.1 → v0.2)

```text
C2-MAJ-01:  Resolved (account_id opaque/globally unique, không derive từ boundary+environment)
C2-MAJ-02:  Resolved (CLOSED terminal chỉ forward transition, correction append-only vẫn hợp lệ)
C2-MAJ-03:  Resolved (fold algorithm "visible-valid-head per slice", dùng chung metadata/status)
C2-MAJ-04:  Resolved (một quy tắc downstream authority duy nhất, AccountCurrentView không bao giờ là input)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

### Package lifecycle meaning

`Consolidated Stable` là package lifecycle/readiness state — nghĩa là: reviewed package baseline nội bộ coherent; mọi qualifying finding đã resolved; deferred limitations được ghi nhận tường minh là non-blocking Phase 1 concern; package integration đủ ổn định để làm dependency baseline cho package kế tiếp (0.2-C3). Nó KHÔNG có nghĩa: artifact Approved; artifact Locked; ADR-012 thay đổi; Domain Contract bất biến; OQ closure; Phase completion; implementation authorization; Live authorization.

### Unchanged artifact statuses

`account.md`: **giữ nguyên** `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte — không sửa Domain Contract semantic trong transaction này. `ADR-012.md`: **giữ nguyên** `version: "0.3"`, `status: Approved`, byte-for-byte — không sửa.

### Metadata / state

- `account.md`, `ADR-012.md`: **không đổi** (semantic và version) — package lifecycle metadata only.
- `context-map.yaml`: **v0.11 không đổi** — chỉ sửa comment ghi nhận Consolidated Stable.
- `README.md` (domain index): **v0.32 → v0.33**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.58 → 9.59**; dòng `domain/` cập nhật ghi nhận Package 0.2-C2 `Consolidated Stable`.
- Mọi Domain Contract khác (`instrument.md`, `venue.md`, `candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, `context.md`), mọi ADR file, Constitution: **không đổi.**

**Package 0.2-C3 baseline dependency đã thỏa, eligible cho Product Owner scope authorization — CHƯA bắt đầu, CHƯA author, KHÔNG được authorize bởi transaction này.** Package 0.2-C4–C7 gate chưa mở. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — correct Package 0.2-C2 account semantics

**Package 0.2-C2 bounded correction — consolidated Review A + Review B findings.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C2 bounded correction — consolidated Review A + Review B findings." Đóng đúng bốn finding Major: `C2-MAJ-01` (account identity cardinality), `C2-MAJ-02` (CLOSED terminality versus correction), `C2-MAJ-03` (metadata/status correction fold), `C2-MAJ-04` (downstream Current View authority). Authorization này **không** cho phép sửa ADR-012 hay bất kỳ ADR nào, thêm owner/tenant/IAM/billing semantics, định nghĩa Broker Account Boundary implementation, thêm external account-number taxonomy, thêm reopening/PAPER→LIVE promotion workflow, author C3–C7, sửa C1/Package B/Constitution/OQ, Approve/Lock/Consolidate bất kỳ artifact/package nào, hay authorize Live.

### C2-MAJ-01 — Account identity cardinality

v0.1 mô tả `account_id` "resolve deterministic từ TOÀN BỘ scope identity bất biến (`account_boundary_ref` + `environment`)" — SAI, vì điều này ngụ ý collapse nhiều Account hợp lệ dùng chung boundary/environment thành một. v0.2 pin: `account_id` là opaque identifier, globally unique trong toàn Ride, gán tại thời điểm `AccountRegistered`, KHÔNG derive/resolve/uniquify từ scope. Một `account_id` → đúng MỘT `account_boundary_ref` bất biến VÀ đúng MỘT `environment` bất biến (giữ nguyên); nhưng một cặp `(account_boundary_ref, environment)` CÓ THỂ chứa NHIỀU `account_id` phân biệt (sửa). SCOPE_ERROR correction path (§11) xác nhận identity mới là opaque, gán mới, KHÔNG có công thức suy từ account_id cũ hay từ scope.

### C2-MAJ-02 — CLOSED terminality versus correction

Làm rõ: CLOSED là terminal CHO FORWARD TRANSITION trên valid lineage hiện hành — không có `AccountStatusChanged` forward nào được phép sau một CLOSED fact VALID. Điều này KHÔNG chặn correction: một CLOSED fact ghi SAI vẫn correctable append-only qua `AccountFactInvalidated` + same-slice `AccountStatusChanged` replacement (§11, mười invariant chung áp dụng nguyên vẹn) — correction record khác forward transition, KHÔNG vi phạm terminality. Fold algorithm (§7) PHẢI recompute `current_status` từ valid corrected lineage sau khi replacement visible — có thể khác CLOSED nếu correction đổi kết luận. Phát hiện kèm theo: payload `AccountStatusChanged` v0.1 THIẾU field `supersedes_fact_ref` — về mặt kỹ thuật không thể emit một correction replacement hợp lệ dù §11 mô tả cơ chế này áp dụng cho cả ba họ event. v0.2 thêm field còn thiếu. KHÔNG thêm state/enum mới, KHÔNG thêm reopening command — tái dùng nguyên vẹn cơ chế correction lineage đã có.

### C2-MAJ-03 — Metadata/status correction fold

Thay fold algorithm (§7 Bước 2/Bước 3) bằng một quy tắc chung "visible-valid-head per slice", dùng thống nhất cho `AccountRegistered`/`AccountMetadataRevised`/`AccountStatusChanged`: (1) group fact theo correction lineage/effective-time slice; (2) resolve invalidation visibility tại cursor; (3) loại trừ fact đã invalidate visible khỏi lineage; (4) chọn head hợp lệ (visible valid head) cho mỗi slice; (5) slice bị invalidate mà chưa có replacement visible KHÔNG đóng góp fact nào (không "giữ giá trị cũ", không "coi như rỗng") — chỉ đóng góp CỦA SLICE ĐÓ bị bỏ, slice khác không ảnh hưởng; (6) total-order mọi head còn lại: `effective_time` ASC, `recorded_time` ASC, `event_id` ASC; (7) áp dụng PATCH (`AccountMetadataRevised`) hoặc lifecycle fold (`AccountStatusChanged`) theo thứ tự đó. Kết quả: một `AccountMetadataRevised` bị invalidate không để lại residual field nào; một `AccountStatusChanged` bị invalidate (kể cả CLOSED) không ảnh hưởng `current_status`.

### C2-MAJ-04 — Downstream Current View authority

v0.1 §13 mô tả `venue_id`/`environment` "resolve qua AccountCurrentView/reconstruction" — đọc được như hai lựa chọn ngang hàng, cho phép downstream package dùng `AccountCurrentView` làm input bình thường. v0.2 pin MỘT quy tắc duy nhất, không ngoại lệ: downstream field PHẢI resolve TRỰC TIẾP từ authoritative Account event stream TẠI cursor mà computation đó đang dùng. `AccountCurrentView` latest-state thông thường (`GetCurrentAccount`) KHÔNG BAO GIỜ là input hợp lệ — nó không cursor-addressable, chỉ query/UI. Một materialized projection CHỈ được chấp nhận làm cache tính toán khi ĐỒNG THỜI cursor-addressable (hỗ trợ resolve tại cursor cụ thể, không chỉ "mới nhất") VÀ provably equivalent với authoritative reconstruction tại đúng cursor/contract version/configuration. `venue_id` xác nhận TUYỆT ĐỐI ABSENT (không phải optional-nhưng-present, không phải null-placeholder) khi `boundary_type: broker_account`.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, ADR-007, ADR-012 v0.3 Approved (byte-for-byte unchanged — verified), Package 0.2-C1 (`instrument.md`/`venue.md` không đổi), Package B (không đổi). Preserve nguyên vẹn: exactly-one immutable Account boundary; venue/broker boundary distinction; immutable environment; PAPER/LIVE structural parity; ACTIVE/SUSPENDED/CLOSED lifecycle value set; credential-reference/raw-secret prohibition; metadata PATCH field whitelist; METADATA_ERROR/SCOPE_ERROR distinction; same-scope registration correction. Không owner/tenant/IAM/billing semantics mới. Không Broker Account Boundary implementation. Không external account-number taxonomy. Không reopening/PAPER→LIVE promotion workflow.

### Acceptance criteria — verified

1. Nhiều Account có thể chung boundary/environment (§1, account_id không derive từ scope). 2. `account_id` opaque, không scope-derived (§1). 3. Valid CLOSED vẫn terminal cho forward transition (§5). 4. CLOSED sai correctable append-only (§5/§11, `supersedes_fact_ref` thêm vào payload). 5. Invalidated metadata/status fact không bao giờ đóng góp vào fold (§7 Bước 5 quy tắc chung). 6. Mỗi correction slice chỉ đóng góp visible valid head của nó (§7). 7. Downstream replay không đọc được future latest-state Current View — chỉ resolve tại cursor từ authoritative stream (§13). 8. ADR-012 không đổi — verified byte-identical. 9. Không semantic không liên quan bị đổi — verified qua diff scope.

### Changed-file scope

`docs/domain/account.md`, `docs/domain/context-map.yaml` (comment-only), `docs/domain/README.md`, `docs/MANIFEST.md`, `docs/CHANGELOG.md`. `docs/adr/ADR-012.md` (và mọi ADR khác), `instrument.md`, `venue.md`, Package B, Constitution, OQ files, Package 0.2-C3–C7 artifacts: **không đổi.**

### Metadata / state

- `account.md`: **v0.1 → v0.2**, `status: Draft`.
- `docs/adr/ADR-012.md`: **không đổi** — `version: "0.3"`, `status: Approved`, byte-for-byte.
- `context-map.yaml`: **v0.11 không đổi** — chỉ sửa comment (finding metadata tại `owned_contracts`).
- `README.md` (domain index): **v0.31 → v0.32**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.57 → 9.58**; dòng `domain/` cập nhật ghi nhận bounded correction, 4 finding Major đã đóng.
- `instrument.md`, `venue.md`, mọi ADR file khác, Package B: **không đổi.**

**Chỉ Package 0.2-C2 được correct.** Không sửa ADR-012 hay bất kỳ ADR nào. Không author C3–C7. Không Approve/Lock/Consolidate artifact/package nào. Không đóng OQ-002/OQ-003. Không authorize Live. Package 0.2-C1 vẫn `Consolidated Stable`, không sửa semantic. Package 0.2-C3–C7 vẫn chưa authorize, chưa author. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — author Package 0.2-C2 trading account foundation

**Package 0.2-C2 — Trading Account Foundation.** Vai trò: `Domain Contract Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C2 — Trading Account Foundation" — cho phép author `docs/domain/account.md`, cập nhật metadata tích hợp (`context-map.yaml`, `README.md`, `MANIFEST.md`, `CHANGELOG.md`). Authorization này KHÔNG cho phép author Strategy/Decision/Trade Intent/Risk/Execution Intent/Order/Fill/Position/Replay Event, exchange API adapter, Live execution workflow, billing, multi-tenant IAM, custody implementation; KHÔNG sửa semantic Package C1/B/Constitution/OQ-002/OQ-003; Package 0.2-C3–C7 vẫn unauthorized.

### Baseline conflict phát hiện và giải quyết

Authorization ban đầu yêu cầu author cả `docs/domain/account.md` VÀ `docs/adr/ADR-012.md` (kỳ vọng "next repository-consistent Draft version" — ngụ ý ADR-012 chưa tồn tại). Kiểm tra baseline trước khi sửa bất kỳ file nào phát hiện `docs/adr/ADR-012.md` **đã tồn tại**: `version: "0.3"`, `status: Approved`, `approved_by: Product Owner`, `approved_at: "2026-07-28"`, blob `59eec21774478fc862e120d8a0f9285dc24eb720` — đã quyết định đúng lãnh thổ "Account-to-Boundary Cardinality — Exactly-One-Boundary Trading Account" mà task yêu cầu (account identity, venue/broker boundary, credential/secret separation, paper/live structural parity), qua ba vòng review (ChatGPT + Independent Review B), 0 finding còn lại, Approved 2026-07-28. Theo đúng kỷ luật baseline-verification-trước-mọi-edit đã áp dụng xuyên suốt session này: **STOP**, KHÔNG sửa file nào, báo cáo conflict đầy đủ (expected vs actual) cho Product Owner, chờ quyết định.

**Product Owner decision (turn tiếp theo):** treat `ADR-012.md` v0.3 Approved làm controlling architecture — KHÔNG modify/re-author/bump/replace/reinterpret ADR-012; không cần ADR mới; author `account.md` alone, constrained by ADR-012's existing decision (đặc biệt §2.1 canonical `account_boundary_ref` model, §2.2/§2.3 venue/broker_account boundary behavior, §2.4 scope rules, §2.6 executable validation obligations liên quan Account).

### `account.md` v0.1 Draft (mới)

**Trading Account Subject** (`kind: entity`) — `account_id` opaque, stable, KHÔNG encode venue/owner/environment/credential/account type (đúng yêu cầu task, Chapter 6 §6.8). Scope identity bất biến: `account_boundary_ref` (`{boundary_type: venue | broker_account, boundary_id}` — canonical model ĐÚNG NGUYÊN VĂN ADR-012 §2.1, required, immutable, không rebinding) và `environment` (enum đóng `PAPER`/`LIVE`, required, immutable — `LIVE` CHỈ là domain value phân biệt account environment, KHÔNG authorize Live execution của platform). PAPER và LIVE Account dùng chung structural contract (ADR-012 §2.4, I-2 Decision Parity) — không nhánh schema riêng.

Bốn event: `AccountRegistered` (original hoặc same-scope correction replacement — thiết lập scope bất biến + mutable metadata ban đầu `credential_reference`/`display_name`); `AccountMetadataRevised` (forward-looking, PATCH semantics `EXPLICIT_PATCH_WITH_CLEAR_SET`, whitelist `credential_reference`/`display_name`, cả hai optional/clearable); `AccountStatusChanged` (lifecycle tối thiểu — state_machine `UNSEEN→ACTIVE↔SUSPENDED→CLOSED`, ba state thực, CLOSED terminal, không onboarding/KYC/pending-approval state); `AccountFactInvalidated` (correction lineage, có thể target `AccountRegistered` — `account_fact_correction_class` ∈ {METADATA_ERROR, SCOPE_ERROR}, đúng ADR-012 §2.1 "rebinding nghĩa là tạo một Account identity khác"). Cộng `AccountCurrentView` (optional read model, non-authoritative, `view_state`/`pending_correction_class` áp dụng ngay từ v0.1).

**Venue binding:** khi `boundary_type: venue`, `boundary_id` PHẢI resolve tới một `venue_id` đã `VenueRegistered` (`venue.md` §3, `ref: venue`) — `account.md` KHÔNG định nghĩa lại Venue semantics, chỉ tham chiếu. Khi `boundary_type: broker_account`, `boundary_id` là opaque reference tới Broker Account Boundary — concept CHƯA author như Domain Contract riêng (deferred).

**Credential và secret boundary (I-11):** Account CHỈ giữ `credential_reference` — opaque reference tới external secure credential binding (Vault/KMS, Phase 1). TUYỆT ĐỐI KHÔNG raw secret (API key, private key, token, password, exchange credential) trong payload, `AccountCurrentView` snapshot, log, hay replay artifact nào. Chỉ Exchange Adapter/Custody-Signing Service dùng credential trực tiếp (I-11) — Strategy/Decision/Risk/Execution Engine (chưa author) chỉ tương tác qua `credential_reference` opaque.

**Downstream reference contract (Package 0.2-C3–C7, chưa author):** đúng bốn field — `account_id` (`ref: account`), `venue_id` (khi boundary_type=venue), `environment`, `account_status`. Downstream PHẢI resolve qua authoritative Account event stream hoặc reconstruction tương đương TẠI cùng cursor — KHÔNG dùng `AccountCurrentView` làm input bình thường (I-12, Chapter 7 §7.4, pin ngay từ v0.1). `account.md` KHÔNG author semantics của Strategy/Decision/Risk/Execution Intent/Order/Fill/Position.

### Học từ Package 0.2-C1, đóng trước — không chờ review round phát hiện

Ba pattern đã proven qua 5 vòng correction của C1, apply trực tiếp ngay từ `account.md` v0.1 thay vì chờ Review A/B phát hiện lại:

1. `pending_correction_class` (`AWAITING_SAME_SUBJECT_REPLACEMENT`/`TERMINAL_SCOPE_INVALIDATION`) — bắt buộc khi `view_state = PENDING_CORRECTION`, cấm khi `VALID` — pin ngay tại `AccountCurrentView` (§7), tránh lặp lại `IRB-C1-MAJ-01`-style finding.
2. `revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET` cho `AccountMetadataRevised` (`changed_fields`/`clear_fields`, disjoint, ít nhất một effective change) — pin ngay, tránh lặp lại `RA-C1-MAJ-02`-style finding.
3. `AccountCurrentView` pin "KHÔNG BAO GIỜ là authority cho Domain Contract khác" ngay từ v0.1 — tránh lặp lại `IRB-C1-V03-MAJ-02`-style finding.

**Bounded tường minh — KHÔNG mang theo:** `ActiveListingReservation`-style multi-party arbitration (Account không có bài toán "nhiều subject tranh một slot" trong chính nó); `ActiveListingActivationRequested`-style activation-request-identity/idempotency machinery (không applicable); 5-phase bitemporal fold policy riêng (chỉ cần total-order tie-break đơn giản effective_time/recorded_time/event_id ASC, mô tả trực tiếp không cần policy identifier riêng vì chỉ có một fold concern).

### `context-map.yaml` v0.10 → v0.11

Đăng ký capability `account-management` (title: Account Management) và context `account-reference` (title: Trading Account Reference, `capability_id: account-management`, `owned_contracts: [account]`) — **MỚI**, không thuộc phạm vi `market-reference`/`instrument-venue-reference` của Package 0.2-C1. KHÔNG thêm cross-context relationship edge — Account chỉ dùng `ref:` lookup tới `venue_id` (giống mọi Domain Contract Package 0.2-B tham chiếu `instrument_id`/`venue_id`), không publish/consume event stream qua context boundary theo nghĩa CQRS published-language, tránh speculative relationship (cùng nguyên tắc đã áp dụng cho C1 khi đăng ký `instrument-venue-reference`).

### Backward Consistency Check

No conflict với Constitution Chapters 2–10 (đặc biệt Chapter 6 §6.4 "Account ≠ Tenant", §6.8 opaque ID; I-2 Decision Parity; I-3 No Repaint; I-11 Secrets & Custody Isolation), ADR-007 (multi-account readiness), ADR-012 v0.3 Approved (byte-for-byte unchanged, mọi field/invariant account.md implement đúng những gì ADR-012 §2/§6 yêu cầu, không tự quyết thêm), Package 0.2-C1 (`instrument.md`/`venue.md` không đổi, `venue_id` reference đúng shape hiện có), Package B (không đổi). Không B-package schema change. Không C3–C7 semantics. Không OQ-002/OQ-003 closure.

### Attack-scenario/self-review kết quả

Author self-review xác nhận: account_id không encode venue/owner/environment/credential/account type; account_boundary_ref/environment bất biến, rebinding dùng SCOPE_ERROR path đúng ADR-012 §2.1; boundary_type đóng đúng hai giá trị ADR-012; venue boundary reference đúng `venue.md §3`, không định nghĩa lại Venue; broker_account boundary_id deferred tường minh; PAPER/LIVE dùng chung structural contract, LIVE domain value không tự authorize Live execution; lifecycle ba state tối thiểu, CLOSED terminal, không onboarding/KYC; credential_reference opaque, không raw secret ở bất kỳ đâu (payload/view/log/replay); PATCH semantics đầy đủ (changed_fields/clear_fields, disjoint, ít nhất một effective change); correction lineage đầy đủ 10 invariant + METADATA_ERROR/SCOPE_ERROR classification + pending_correction_class mapping; downstream reference contract đúng bốn field, Current View không phải authority; không multi-tenant/billing/custody/onboarding semantics; ADR-012.md không bị chạm (verified byte-identical); Package C1/B/Constitution/OQ không bị chạm (verified zero diff).

### Changed-file scope

`docs/domain/account.md` (mới), `docs/domain/context-map.yaml`, `docs/domain/README.md`, `docs/MANIFEST.md`, `docs/CHANGELOG.md`. `docs/adr/ADR-012.md` (và mọi ADR khác), `instrument.md`, `venue.md`, `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`/`context.md`, Constitution, OQ files, Package 0.2-C3–C7 artifacts: **không đổi.**

### Metadata / state

- `account.md`: **mới, v0.1**, `status: Draft`.
- `docs/adr/ADR-012.md`: **không đổi** — `version: "0.3"`, `status: Approved`, byte-for-byte.
- `context-map.yaml`: **v0.10 → v0.11** — capability/context mới, `status` giữ `Draft`.
- `README.md` (domain index): **v0.30 → v0.31**, `status` giữ `Draft` — mục "Package 0.2-C2" mới.
- `MANIFEST.md`: `manifest_version` **9.56 → 9.57**; dòng `domain/` cập nhật ghi nhận Package 0.2-C2 authored.
- `instrument.md`, `venue.md`, `context.md`, `feature.md`, `regime.md`, `structure.md`, `swing.md`, `candle.md`, mọi ADR file khác: **không đổi.**

**Chỉ Package 0.2-C2 được author.** Không author Strategy/Decision/Trade Intent/Risk/Execution Intent/Order/Fill/Position/Replay Event. Không sửa ADR nào (kể cả ADR-012). Không Approve/Lock artifact. Không Consolidate Package 0.2-C2. Không đóng OQ-002/OQ-003. Không authorize Live. Package 0.2-C1 vẫn `Consolidated Stable`, không sửa semantic. Package 0.2-C3–C7 vẫn chưa authorize, chưa author. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — consolidate Package 0.2-C1

**Package 0.2-C1 Reference Foundation consolidated as `Consolidated Stable`.** Vai trò: `Package Lifecycle Consolidation Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C1 consolidation transaction" (2026-07-30). Authorization này cho phép ghi Package 0.2-C1 vào lifecycle state `Consolidated Stable` — nó KHÔNG cho phép Approve/Lock `instrument.md` hay `venue.md`, không sửa ADR, không sửa Constitution, không đóng OQ, không authorize Live, không author/authorize Package 0.2-C2–C7, không redesign request/reservation behavior, không thêm speculative edge case, không tuyên bố Phase 0.2 hoàn thành.

### Reviewed baseline pinned

```text
Package 0.2-C1 reviewed HEAD:  ddc790864b3ee50a1ad402dc26146970e2791ed4

Primary artifact:      instrument.md v0.6 Draft, blob 81651f6a19a3f22fa7a924173f14b02e6467c8e0
Secondary artifact:    venue.md v0.3 Draft, blob 0ffb9e64bcb7dec108edea0bc9c3af3a162b40d9
Integration artifact:  context-map.yaml v0.10 Draft, blob 05bd2ba5bd72888d8ef206eb2ea088d03c1f50f3
Registry baseline:     MANIFEST v9.55, blob 381010a8c47ece07fdd1be8820129a8953ef33c3
```

### Review evidence

```text
ChatGPT Review A:        Clean — 0 blocking finding
Independent Review B:    Clean with deferred limitations — 0 blocking finding
```

Deferred limitations (Phase 1 implementation concern, non-blocking cho walking-skeleton readiness): runtime worker ownership; transaction boundaries; retry/backoff; monitoring và escalation; operational recovery orchestration. Đây KHÔNG phải Domain Contract semantic gap — Package 0.2-C1 pin RULE (identity, correction lineage, bitemporal fold, arbitration authority boundary), không pin MECHANISM triển khai, đúng nguyên tắc defer đã nhất quán xuyên suốt `instrument.md` §23/§24. Có thể evolve từ implementation evidence khi Phase 1 bắt đầu.

### Complete finding ledger — all resolved (năm vòng narrow correction, v0.2–v0.6)

```text
RA-C1-MAJ-01:        Resolved (instrument_identity_ref/venue_identity_ref, v0.2)
RA-C1-MAJ-02:        Resolved (revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET, v0.2)
RA-C1-MAJ-03:        Resolved (initial_fact_correction_policy, v0.2)
IRB-C1-MAJ-01:       Resolved (pending_correction_class, v0.3)
IRB-C1-MAJ-02:       Resolved (TradableListing eligibility đối xứng, v0.3)
IRB-C1-MAJ-03:       Resolved (ActiveListingReservation pair-scoped authority, v0.3)
IRB-C1-MAJ-04:       Resolved (status_fold_order_policy 5-phase, v0.3)
IRB-C1-V03-MAJ-01:   Resolved (ActiveListingActivationRequested phá vỡ chu trình causal, v0.4)
IRB-C1-V03-MAJ-02:   Resolved (authoritative parent reconstruction, v0.4)
IRB-C1-V03-MAJ-03:   Resolved (ActiveListingReservationFactInvalidated correction lineage, v0.4)
IRB-C1-V03-MAJ-04:   Resolved (reservation_fold_order_policy 5-phase, v0.4)
IRB-C1-V04-MAJ-01:   Resolved (activation_request_id logical identity/idempotency, v0.5)
IRB-C1-V05-MAJ-01:   Resolved (ActiveListingActivationRequestFactInvalidated, canonical semantic payload, v0.6)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

### Package lifecycle meaning

`Consolidated Stable` là package lifecycle/readiness state — nghĩa là: reviewed package baseline nội bộ coherent; mọi qualifying finding đã resolved; deferred limitations được ghi nhận tường minh là non-blocking Phase 1 concern; package integration đủ ổn định để làm dependency baseline cho package kế tiếp (0.2-C2). Nó KHÔNG có nghĩa: artifact Approved; artifact Locked; Domain Contract bất biến; OQ closure; Phase completion; implementation authorization; Live authorization.

### Unchanged artifact statuses

`instrument.md`: **giữ nguyên** `version: "0.6"`, `status: Draft`, `approved_by: null`, `approved_at: null` — không sửa Domain Contract semantic trong transaction này. `venue.md`: **giữ nguyên** `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null` — không sửa.

### Metadata / state

- `instrument.md`, `venue.md`: **không đổi** (semantic và version) — package lifecycle metadata only.
- `context-map.yaml`: **v0.10 không đổi** — chỉ sửa comment ghi nhận Consolidated Stable.
- `README.md` (domain index): **v0.29 → v0.30**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.55 → 9.56**; dòng `domain/` cập nhật ghi nhận Package 0.2-C1 `Consolidated Stable`.
- Mọi Domain Contract khác (`candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, `context.md`), mọi ADR file, Constitution: **không đổi.**

**Package 0.2-C2 baseline dependency đã thỏa, eligible cho Product Owner scope authorization — CHƯA bắt đầu, CHƯA author, KHÔNG được authorize bởi transaction này.** Package 0.2-C3–C7 gate chưa mở. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — finalize Package 0.2-C1 request correction semantics

**Package 0.2-C1 narrow correction — authoritative activation-request invalidation và canonical semantic payload.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C1 narrow correction — authoritative activation-request invalidation và canonical semantic payload." Đóng đúng một finding còn mở: `IRB-C1-V05-MAJ-01` (`ActiveListingActivationRequested` fact có thể pass ingress validation, được ghi nhận authoritative, rồi sau đó phát hiện SAI thực tế — contract v0.5 không có append-only invalidation/disposition, không có replay exclusion/classification, canonical semantic payload chưa liệt kê đầy đủ). Authorization này **không** cho phép redesign activation arbitration, không đổi reservation authority structure, không đổi reservation correction lineage ngoài reference bắt buộc, không đổi parent reconstruction, không đổi status/reservation fold policy, không author C2–C7, không sửa ADR, không Approve/Lock/Consolidate/đóng OQ/authorize Live.

### Part A — Request-fact invalidation event

Thêm `ActiveListingActivationRequestFactInvalidated` (`instrument.md` §16) — target CHỈ `ActiveListingActivationRequested`; KHÔNG target grant/reject/activation event/invalidation khác/request không liên quan. Envelope binding: `subject_ref` khớp hệt, `effective_time` khớp hệt. Payload: `invalidated_request_fact_ref` (required), `activation_request_id` (required, phải khớp target), `request_invalidation_class` (đóng `FACTUAL_REQUEST_ERROR`), `invalidation_reason` (optional).

### Part B — Invalidation invariants

Mười invariant pin đầy đủ: recorded sau target; một invalidation per fact; cấm invalidation-of-invalidation; identity/scope không đổi; không replacement dưới cùng `activation_request_id`; corrected intent cần ID mới; replay trước invalidation thấy request gốc; replay sau invalidation thấy invalid; request vẫn queryable làm historical evidence; append-only (không xóa/mutate). KHÔNG thêm `supersedes_fact_ref` vào `ActiveListingActivationRequested` — quyết định bounded "request immutable, không metadata-patchable" giữ nguyên.

### Part C — Terminal request disposition

Pin `request_validity_state ∈ {VALID, TERMINALLY_INVALID}` — request visible không có invalidation visible → VALID; invalidation visible → TERMINALLY_INVALID vĩnh viễn, KHÔNG BAO GIỜ quay lại VALID. Request mới (corrected intent) có validity/outcome lineage độc lập hoàn toàn, không kế thừa từ ID cũ. Không retry worker nào được diễn giải TERMINALLY_INVALID là "chờ sửa tạm thời".

### Part D — Effect on arbitration outcomes

Invalidation TRƯỚC outcome: cấm mọi grant/reject emit sau đó. Outcome ĐÃ TỒN TẠI trước invalidation — ba trường hợp deterministic: (1) đã có rejection → TERMINALLY_INVALID, rejection giữ nguyên audit evidence, không activation (đã đúng theo quy tắc hiện có); (2) đã có grant, activation CHƯA ghi nhận → grant hết hiệu lực cho activation mới, `ActiveListingReservationReleased` thêm reason `REQUEST_INVALIDATION`, causation_refs trỏ chính request invalidation, giải phóng reservation — tách bạch reservation state history (vẫn HELD lịch sử tới khi release visible+effective) khỏi activation authorization eligibility (mất ngay khi invalidation visible, không chờ release); (3) đã có grant VÀ activation đã ghi nhận → KHÔNG silently mutate activation history, HÀNH ĐỘNG DOWNSTREAM BẮT BUỘC là emit `TradableListingFactInvalidated` (§14, cơ chế đã có) target activation event, việc này tự động kích hoạt `ActiveListingReservationReleased`(`CORRECTION_INVALIDATION`, §16, cơ chế đã có từ v0.4) — KHÔNG phát minh cơ chế thứ hai; invalidation là tín hiệu cho operator, không phải trigger tự động; cho tới khi correction downstream đó visible, activation event/TradableListingCurrentView vẫn hiển thị bình thường theo mọi quy tắc hiện có.

### Part E — Outcome validity dependency

`ActiveListingReserved`/`ActiveListingActivationRejected`/`TradableListingCreated`(ACTIVE)/`TradableListingStatusChanged`(ACTIVE) thêm invariant: activation request được tham chiếu PHẢI visible VÀ `VALID` (không `TERMINALLY_INVALID`) tại recorded/effective cursor liên quan. Request invalidation visible tại cursor replay vô hiệu hóa quyền dùng grant cho activation MỚI, ngay cả khi bản thân grant chưa bị invalidate riêng. KHÔNG rewrite causation lịch sử — chỉ ràng buộc việc tạo event MỚI.

### Part F — Request replay algorithm

"Request dedup và replay algorithm" (`instrument.md` §16) mở rộng từ 7 bước (v0.5) thành 10 bước: group theo `activation_request_id` → resolve một original authoritative request → resolve request-fact invalidation visibility (mới) → classify VALID/TERMINALLY_INVALID (mới) → verify scope binding + canonical semantic payload → chỉ nếu VALID mới resolve outcome lineage → grant+VALID cho phép đúng một activation → rejection cấm activation → TERMINALLY_INVALID cấm mọi outcome/activation mới (mới) → unresolved-valid-request không hiệu lực gì. Mọi bước dùng cùng recorded/effective cursor, correction lineage hợp lệ, cùng contract version/configuration.

### Part G — Canonical semantic payload definition

Liệt kê đầy đủ canonical semantic payload cho `ActiveListingActivationRequested`: identity/scope field (`activation_request_id`/`instrument_id`/`venue_id`/`listing_id`/`requested_target_status`) luôn semantic. `requested_by_ref` pin LÀ semantic — phải khớp chính xác cho cùng ID redelivery. `request_reason` (payload field mới, thêm ở v0.6) pin non-authoritative — LOẠI KHỎI idempotency equality. Envelope delivery metadata (`event_id`/`recorded_time`/transport retry) không tạo logical request mới. `source_identity` = delivery/dedup evidence, không phải business scope. `causation_refs` = semantic lineage, không được mâu thuẫn request gốc. `related_event_refs` non-causal, loại khỏi logical request identity.

### Part H — No same-ID correction (tái khẳng định, ba trường hợp tách bạch)

(1) Ingress-invalid — reject trước authoritative append, chưa từng tồn tại authoritative, không cần invalidation. (2) Valid request, business intent sau đó đổi — request gốc vẫn valid lịch sử, intent mới dùng ID mới. (3) Request authoritative sau đó phát hiện sai thực tế — emit `ActiveListingActivationRequestFactInvalidated`, corrected intent dùng ID mới. Ba trường hợp không được lẫn lộn.

### Part I — Idempotency after invalidation

Redelivery chính xác (cùng ID, cùng canonical semantic payload) cho request `TERMINALLY_INVALID` → normalize về record đã ghi nhận, không tạo request mới, không tạo outcome mới. Redelivery với payload thay đổi cho request `TERMINALLY_INVALID` → vẫn deterministic reject, không ngoại lệ.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, ADR-007, activation request identity/idempotency (v0.5), pair reservation authority, reservation correction lineage, status/reservation bitemporal fold, Instrument/Venue identity hiện có, Context Map, B-package references. Không same-ID request mutation. Không causal-cycle regression. Không grant use từ terminally invalid request. Không silent historical deletion. Không Current View authority regression. Không reservation look-ahead. Không identifier rename. Không B-package schema change. Không C2–C7 semantics.

### Attack-scenario results — 34/34 pass

Malformed request rejected trước append; valid request superseded bởi business intent đổi; authoritative request phát hiện sai thực tế; request invalidated trước outcome; grant emitted sau invalidation (cấm); rejection emitted sau invalidation (cấm); request invalidated sau rejection; request invalidated sau grant trước activation; request invalidated sau grant và activation; reservation release chưa visible; release visible chưa effective; release visible và effective; invalidated request redelivered cùng payload (idempotent, normalize); redelivered khác payload (reject); invalidation target request ID khác (cấm); invalidation subject mismatch (cấm); invalidation effective-time mismatch (cấm); double request invalidation (cấm); invalidation-of-invalidation (cấm); request replacement dưới cùng ID (cấm); corrected intent với ID mới (đúng); requested_by_ref đổi dưới cùng ID (reject, semantic); request_reason đổi dưới cùng ID (idempotent, non-semantic); source_identity đổi khi retry (không conflict); causation_refs mâu thuẫn request gốc (reject); related_event_refs đổi khi retry (không conflict); replay trước request invalidation (thấy VALID); replay sau invalidation (thấy TERMINALLY_INVALID); replay sau invalidation trước release (vẫn HELD lịch sử, activation ineligible); replay sau release (AVAILABLE); activation dùng grant từ terminally invalid request (cấm — Part E); C2–C7 artifact introduced (không — verified absent); B-package blob changed (không — verified unchanged); venue.md changed (không — verified byte-identical).

### Self-review findings

Tự phát hiện và tự sửa/xác nhận trước commit: (1) request invalidation event missing activation_request_id — không tìm thấy, payload có field required tường minh. (2) invalidation allowing same-ID replacement — không tìm thấy, không có supersedes_fact_ref trên event mới. (3) outcome allowed after terminal invalidation — đóng bằng Part E invariant tại cả `ActiveListingReserved`/`ActiveListingActivationRejected`. (4) grant still consumable after request invalidation — đóng bằng Part E invariant tại `TradableListingCreated`/`TradableListingStatusChanged`. (5) no rule for already-existing grant — đóng bằng Part D Trường hợp 2/3 tường minh. (6) canonical semantic payload not fully enumerated — đóng bằng Part G liệt kê đầy đủ. (7) requested_by_ref ambiguity — đã quyết định tường minh: semantic. (8) source_identity treated as new request identity — không tìm thấy, pin tường minh "delivery evidence, không phải business scope". (9) exact retry after invalidation recreating request — đóng bằng Part I invariant tường minh. (10) stale v0.5 reference — đã cập nhật toàn bộ (frontmatter, intro blockquote, MANIFEST, README, CHANGELOG); mention "v0.5" còn lại là mô tả lịch sử tường minh. (11) stale section reference — automated `§N` range-scan (instrument.md 1–24, không renumbering section top-level nào) sạch. (12) venue.md accidentally modified — verified: `git diff --stat -- venue.md` rỗng, blob khớp baseline `0ffb9e64bcb7dec108edea0bc9c3af3a162b40d9` byte-for-byte.

### Changed-file scope

`docs/domain/instrument.md`, `docs/domain/README.md`, `docs/MANIFEST.md`, `docs/CHANGELOG.md`, `docs/domain/context-map.yaml` (comment-only). **`docs/domain/venue.md` KHÔNG đổi** — verified byte-identical baseline. `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`/`context.md`/ADR files/Constitution/OQ files/Package 0.2-C2–C7 artifacts: **không đổi.**

### Metadata / state

- `instrument.md`: **v0.5 → v0.6**, `status: Draft`.
- `venue.md`: **v0.3 không đổi**, `status: Draft`.
- `context-map.yaml`: **v0.10 không đổi** — chỉ sửa comment.
- `README.md` (domain index): **v0.28 → v0.29**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.54 → 9.55**; dòng `domain/` cập nhật ghi nhận narrow correction, 1 finding Major đã đóng.
- `context.md`, `feature.md`, `regime.md`, `structure.md`, `swing.md`, `candle.md`, mọi ADR file: **không đổi.**

**Chỉ Package 0.2-C1 được correct.** Không author C2–C7. Không sửa ADR. Không Approve/Lock artifact. Không Consolidate. Không đóng OQ-002/OQ-003. Không authorize Live. `instrument_id`/`venue_id`/`listing_id`/`event_id` không đổi tên/shape. Package 0.2-C2–C7 vẫn chưa authorize, chưa author. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — pin Package 0.2-C1 activation request identity

**Package 0.2-C1 bounded final correction — activation request identity, scope binding và idempotent redelivery semantics.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C1 bounded final correction — activation request identity, scope binding và idempotent redelivery semantics." Đóng đúng một finding còn mở: `IRB-C1-V04-MAJ-01` (`ActiveListingActivationRequested` thiếu stable logical request identity, idempotency/dedup semantics, permanent scope binding, và executable exactly-one-outcome rule dưới retry/redelivery). Authorization này **không** cho phép redesign activation arbitration, không đổi reservation correction lineage, không đổi parent reconstruction, không đổi status/reservation bitemporal folding, không author C2–C7, không sửa ADR, không Approve/Lock/Consolidate/đóng OQ/authorize Live.

### Part A — Canonical activation request identity

Thêm `activation_request_id` (`instrument.md` §16) — stable, opaque, KHÔNG parse (Chapter 6 §6.8), KHÔNG bằng `event_id`, KHÔNG regenerate khi retry/redelivery. Có mặt trong: payload `ActiveListingActivationRequested`; dedup rules; payload `ActiveListingReserved`; payload `ActiveListingActivationRejected`; grant correlation tại `TradableListingCreated`/`TradableListingStatusChanged(ACTIVE)`; request outcome lookup; historical replay. `instrument_id`/`venue_id`/`listing_id`/`event_id` **không đổi tên**.

### Part B — Permanent scope binding

Pin: một khi `activation_request_id` lần đầu ghi nhận authoritative, vĩnh viễn gắn CHÍNH XÁC một `(instrument_id, venue_id, listing_id, requested_target_status = ACTIVE)`. Cùng ID xuất hiện lại với scope khác → REJECT — KHÔNG diễn giải là correction/request mới/retry/superseding request. Activation intent thực sự khác PHẢI dùng `activation_request_id` MỚI.

### Part C — Idempotent redelivery

Pin `activation_request_idempotency_policy: STABLE_ID_SAME_PAYLOAD_IS_IDEMPOTENT` (`instrument.md` §17, 7th canonical policy). First delivery → ghi nhận một authoritative record. Exact retry/redelivery (cùng ID, cùng scope, cùng canonical semantic payload) → idempotent duplicate — không tạo logical request thứ hai, không tạo arbitration outcome thứ hai; physical duplicate reject trước authoritative append hoặc normalize về record đã ghi nhận — không bao giờ hai original request fact authoritative cùng logical ID. Changed-payload replay (cùng ID, khác scope/semantics) → deterministic conflict → reject, không tự chọn bản mới nhất/cũ nhất.

### Part D — Request event identity và original lineage

Pin bounded: `ActiveListingActivationRequested` KHÔNG metadata-patchable, KHÔNG có `*FactInvalidated`/`supersedes_fact_ref` riêng — request scope sai là invalid (xử lý theo event-ingress validation hiện có, không emit grant/reject cho request chưa từng valid), không phải "cần sửa". Đúng một valid original lineage head per `activation_request_id`, dedup key là `payload.activation_request_id`.

### Part E — Exactly-one arbitration outcome per logical request

`ActiveListingReserved`/`ActiveListingActivationRejected` thêm `activation_request_id` bắt buộc, PHẢI khớp `activation_request_id` của request mà `activation_request_ref` trỏ tới. Exactly-one-outcome nay keyed theo `activation_request_id` logical (thay thế cách keying chỉ theo event ref của v0.4) — cấm hai grant/hai reject/một grant một reject cùng ID; cấm outcome nêu request ID khác với event ref trỏ tới; cấm request ID tái sử dụng xuyên pair authority stream khác; cấm quyết định bởi ingestion order.

### Part F — Outcome correction lineage compatibility

Pin: đúng một valid ORIGINAL outcome lineage per `activation_request_id`; correction tạo replacement TRONG CÙNG lineage, không tạo lineage độc lập thứ hai. Outcome type (grant/reject) BẤT BIẾN — `supersedes_fact_ref` KHÔNG BAO GIỜ dùng để flip type. Đảo type cần: (1) invalidate outcome sai theo correction rules hiện có, (2) record activation request MỚI với `activation_request_id` MỚI, (3) pair authority evaluate lại theo quy trình bình thường.

### Part G — Activation event correlation

`TradableListingCreated`/`TradableListingStatusChanged(ACTIVE)` thêm `activation_request_id` bắt buộc. `reservation_grant_ref` PHẢI trỏ `ActiveListingReserved` CÙNG `activation_request_id` VÀ CÙNG pair/listing scope, PHẢI là valid lineage head tại recorded cursor. Cấm: activation dùng grant của request khác; activation dùng grant đã invalidate chưa có replacement visible; hai activation event consume cùng một grant (trừ idempotent duplicate theo dedup algorithm); grant listing A activate listing B.

### Part H — Request dedup và replay algorithm

Thêm thuật toán 7-bước tại `instrument.md` §16: (1) group request theo `activation_request_id`; (2) yêu cầu đúng một valid original authoritative request; (3) verify permanent scope binding; (4) resolve đúng một valid outcome lineage; (5) grant → cho phép đúng một activation lifecycle event (event thứ hai cùng cặp là idempotent duplicate); (6) reject → cấm mọi activation lifecycle event; (7) không outcome → không hiệu lực gì. Mọi bước dùng cùng recorded/effective cursor, correction lineage hợp lệ, cùng contract version/configuration.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, ADR-007, reservation/activation semantics hiện có, reservation correction lineage, bitemporal replay, opaque identifier rules, Context Map, B-package references. Không causal-cycle regression (chuỗi request→grant/reject→activation event vẫn tuyến tính, không đổi). Không request-ID reuse xuyên scope. Không duplicate logical outcome. Không Current View authority regression. Không reservation look-ahead. Không identifier rename. Không B-package schema change. Không C2–C7 semantics.

### Attack-scenario results — 32/32 pass

First valid request; exact duplicate delivery cùng payload (idempotent); duplicate delivery khác event_id (vẫn idempotent — dedup theo activation_request_id không phải event_id); cùng request ID khác listing_id/instrument_id/venue_id/target status (reject, deterministic conflict); cùng request ID khác requested semantics (reject); hai original request fact cho một request ID (cấm — Part D); request ID tái sử dụng ở pair authority stream khác (cấm — Part B); một request nhận cả grant lẫn reject (cấm — Part E); một request nhận hai grant/hai reject (cấm — Part E); outcome request ref và request ID bất đồng (cấm — Part E binding rule); grant/reject scope khác request scope (cấm — Part B/E); grant/reject correction trong cùng outcome lineage (cho phép — Part F); grant correction attempt trở thành reject / reject correction attempt trở thành grant (cấm — Part F, outcome type bất biến); activation dùng grant của request khác (cấm — Part G); activation dùng grant đã invalidate (cấm — Part G); hai activation event consume một grant (cấm trừ idempotent duplicate — Part G/H); unresolved request (không hiệu lực — Bước 7); duplicate redelivery sau grant/sau reject (idempotent, không tạo outcome mới); corrected intent dùng request ID mới (đúng — Part B/D); historical replay trước request/sau request trước outcome/sau outcome (đúng cursor discipline — Part H); C2–C7 artifact introduced (không — verified absent); B-package blob changed (không — verified unchanged).

### Self-review findings

Tự phát hiện và tự sửa/xác nhận trước commit: (1) exactly-one outcome keyed chỉ theo event ref — tìm thấy tại invariant v0.4 gốc, đã sửa thành keyed theo `activation_request_id` logical (cả `ActiveListingReserved` và `ActiveListingActivationRejected`). (2) missing `activation_request_id` trong grant/rejection — đã thêm cả hai, cộng `TradableListingCreated`/`TradableListingStatusChanged`. (3) request ID thiếu immutable scope binding — đóng bằng Part B invariant tường minh trên `ActiveListingActivationRequested`. (4) duplicate delivery tạo request khác — không tìm thấy, Part C/D pin tường minh dedup key = `activation_request_id`. (5) cùng request ID với payload đổi được accept — không tìm thấy, Part C pin deterministic conflict/reject. (6) outcome type đổi qua correction — không tìm thấy, Part F pin bất biến tường minh + quy trình đảo type qua invalidate + ID mới. (7) activation dùng unrelated grant — đóng bằng Part G invariant tại §11/§13. (8) stale v0.4 reference — đã cập nhật toàn bộ (frontmatter, intro blockquote, MANIFEST, README, CHANGELOG); mention "v0.4" còn lại là mô tả lịch sử tường minh. (9) stale section reference — automated `§N` range-scan (instrument.md 1–24, không renumbering section top-level nào) sạch. (10) venue.md accidentally modified — verified: `git diff --stat -- venue.md` rỗng, blob khớp baseline `0ffb9e64bcb7dec108edea0bc9c3af3a162b40d9` byte-for-byte.

### Changed-file scope

`docs/domain/instrument.md`, `docs/domain/README.md`, `docs/MANIFEST.md`, `docs/CHANGELOG.md`, `docs/domain/context-map.yaml` (comment-only). **`docs/domain/venue.md` KHÔNG đổi** — verified byte-identical baseline. `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`/`context.md`/ADR files/Constitution/OQ files/Package 0.2-C2–C7 artifacts: **không đổi.**

### Metadata / state

- `instrument.md`: **v0.4 → v0.5**, `status: Draft`.
- `venue.md`: **v0.3 không đổi**, `status: Draft`.
- `context-map.yaml`: **v0.10 không đổi** — chỉ sửa comment.
- `README.md` (domain index): **v0.27 → v0.28**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.53 → 9.54**; dòng `domain/` cập nhật ghi nhận bounded final correction, 1 finding Major đã đóng.
- `context.md`, `feature.md`, `regime.md`, `structure.md`, `swing.md`, `candle.md`, mọi ADR file: **không đổi.**

**Chỉ Package 0.2-C1 được correct.** Không author C2–C7. Không sửa ADR. Không Approve/Lock artifact. Không Consolidate. Không đóng OQ-002/OQ-003. Không authorize Live. `instrument_id`/`venue_id`/`listing_id`/`event_id` không đổi tên/shape. Package 0.2-C2–C7 vẫn chưa authorize, chưa author. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — finalize Package 0.2-C1 reservation semantics

**Package 0.2-C1 final narrow correction — acyclic activation arbitration, authoritative parent reconstruction, reservation correction lineage và bitemporal reservation replay.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C1 final narrow correction — acyclic activation arbitration, authoritative parent reconstruction, reservation correction lineage và bitemporal reservation replay." Đóng đúng bốn finding Major từ Independent Review B (vòng 2, đánh giá v0.3): `IRB-C1-V03-MAJ-01` (activation/reservation grant có causal cycle), `IRB-C1-V03-MAJ-02` (listing parent eligibility dùng non-authoritative Current View làm input), `IRB-C1-V03-MAJ-03` (reservation fact thiếu append-only correction lineage), `IRB-C1-V03-MAJ-04` (reservation replay thiếu effective-time eligibility). Authorization này **không** cho phép redesign toàn C1, không author C2–C7, không sửa ADR, không Approve/Lock/Consolidate/đóng OQ/authorize Live.

### Part A — Loại bỏ chu trình causal activation/reservation (đóng `IRB-C1-V03-MAJ-01`)

v0.3: `ActiveListingReserved.causation_refs` trỏ tới activation event (`TradableListingCreated`/`TradableListingStatusChanged`), ĐỒNG THỜI activation event đó (§11/§13) `causation_refs` trỏ NGƯỢC tới `ActiveListingReserved` — chu trình causal trực tiếp. Thêm `ActiveListingActivationRequested` (`instrument.md` §16, subject: TradableListing) làm pre-arbitration request tường minh: chuỗi causal nay TUYẾN TÍNH `ActiveListingActivationRequested → ActiveListingReserved/ActiveListingActivationRejected → TradableListingCreated/TradableListingStatusChanged(ACTIVE)`. `ActiveListingReserved`/`ActiveListingActivationRejected` payload thêm `activation_request_ref` (required) trỏ chính request; `causation_refs` nay trỏ request, KHÔNG trỏ activation event. `TradableListingCreated`/`TradableListingStatusChanged` payload thêm `reservation_grant_ref` (required khi ACTIVE) trỏ chính grant — chiều causal này KHÔNG đổi (activation event vẫn phụ thuộc causal vào grant, đúng hướng). Một request tạo ra ĐÚNG MỘT authoritative arbitration outcome (grant XOR reject). Envelope §2 pin tường minh: chu trình causal cấm tuyệt đối xuyên toàn tài liệu; `related_event_refs` không được dùng để che giấu causal dependency thực sự. Request không nhận grant/reject không có hiệu lực gì lên listing lifecycle/reservation state (không invent runtime retry/timeout).

### Part B — Ngữ nghĩa giao dịch reservation/activation

Pin thứ tự transition: (1) request recorded → (2) pair authority evaluate → (3) grant/reject recorded → (4) chỉ sau khi grant visible mới được recorded activation event. Reservation được grant nhưng không dẫn tới activation event nào vẫn giữ HELD cho tới khi có release tường minh — không timeout/expiry ngầm định.

### Part C — Authoritative parent reconstruction (đóng `IRB-C1-V03-MAJ-02`)

v0.3: `TradableListingCurrentView` Bước 4–5 query `InstrumentCurrentView`/`VenueCurrentView` (read model đã tự khóa "KHÔNG được dùng làm input") làm input — mâu thuẫn nội tại với chính §7/`venue.md` §7. v0.4: Bước 4–5 nay reconstruct TRỰC TIẾP từ authoritative Instrument/Venue event stream (§3–§6/`venue.md` §3–§6), dùng ĐÚNG NGUYÊN VĂN fold algorithm §7. Current View CHỈ còn là cache tùy chọn, hợp lệ CHỈ KHI provably equivalent với reconstruction trực tiếp tại CÙNG recorded cursor/effective cursor/contract version/configuration — cache lookup KHÔNG BAO GIỜ thay thế normative authoritative reconstruction. Áp dụng nhất quán: parent eligibility checks tại creation (§11)/activation (§13)/historical replay/correction replay.

### Part D — Reservation correction lineage (đóng `IRB-C1-V03-MAJ-03`)

Thêm `ActiveListingReservationFactInvalidated` (`instrument.md` §16) — valid target: `ActiveListingReserved`/`ActiveListingReservationReleased`/`ActiveListingActivationRejected`. Mười invariant §18 áp dụng nguyên văn (subject_ref/effective_time khớp chính xác, một invalidation per fact, invalidation sau target, cấm invalidation-of-invalidation, replay before invalidation không thấy, replacement không visible trước recorded time riêng, cấm fork/skip). `reservation_correction_class` (required): `RESERVATION_METADATA_ERROR` (same-pair — invalidate + replacement CÙNG event type CÙNG pair, `supersedes_fact_ref`) hoặc `RESERVATION_PAIR_SCOPE_ERROR` (wrong pair — invalidate, KHÔNG replace dưới subject cũ, emit fact đúng dưới pair khác). Cả ba event Reserved/Released/ActivationRejected thêm `supersedes_fact_ref` (optional). Part E: mọi reservation event pin `subject_ref.subject_type: ActiveListingReservation`, payload listing reference PHẢI khớp `listing.instrument_id == reservation.instrument_id` VÀ `listing.venue_id == reservation.venue_id` — cấm grant/release/reject cho pair sai, cấm replacement "same-subject" nhưng thực chất đổi pair.

### Part F — Bitemporal reservation replay (đóng `IRB-C1-V03-MAJ-04`)

Pin `reservation_fold_order_policy: RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER` (`instrument.md` §17), 5-phase đối xứng `status_fold_order_policy`: Phase 1 recorded visibility (`recorded_time <= cursor`); Phase 2 correction lineage (loại fact invalidated, chọn lineage head, cấm fork/skip); Phase 3 effective eligibility (`effective_time <= cursor`, future-effective grant/release đã recorded không ảnh hưởng cursor sớm hơn); Phase 4 deterministic ordering trong pair authority stream (effective_time/recorded_time/event_id ASC, KHÔNG raw sequence); Phase 5 fold state AVAILABLE/HELD/PENDING_CORRECTION (Rejected không đổi state, conflict → PENDING_CORRECTION deterministic, không arrival-order).

### Part G — Ngữ nghĩa release reservation, làm rõ

Pin rõ: invalidate activation event đang HELD reservation KHÔNG tự rewrite reservation fact; `ActiveListingReservationReleased` tường minh là bắt buộc, causally-linked tới invalidation; cho tới khi release visible+effective, reservation vẫn held; replay trước release thấy held, sau release thấy available; không automatic promotion. Nếu bản thân grant SAI (không phải activation event sai) → dùng reservation correction lineage (Part D), không dùng release đơn thuần.

### Part H — Cross-subject replay algorithm cuối cùng

`TradableListingCurrentView` (`instrument.md` §15) 7-bước: (1) resolve listing creation lineage; (2) fold metadata; (3) fold status; (4) reconstruct Instrument từ authoritative event stream; (5) reconstruct Venue từ authoritative event stream; (6) reconstruct pair reservation dùng recorded cursor + effective cursor + reservation correction lineage; (7) derive listing eligibility/Current View. Tất cả 7 bước dùng CÙNG cursor pair, contract version, configuration — cấm parent Current View làm authority, cấm reservation latest/current state cho historical replay, cấm mismatched cursor, cấm future-effective reservation visibility sớm.

### Part I — Versioning

`instrument.md` v0.3 → v0.4 (Draft). `venue.md` **giữ nguyên v0.3** — không có nội dung normative nào của venue.md bị bốn finding trên chạm tới; mọi cross-reference `instrument.md §N` từ venue.md vẫn đúng số (instrument.md KHÔNG chèn section top-level mới, chỉ sửa nội dung bên trong §2/§7/§10/§11/§13/§15/§16/§17/§18/§24). `context-map.yaml` giữ nguyên v0.10 — chỉ sửa comment. `README.md` v0.26 → v0.27. `MANIFEST.md` manifest_version 9.52 → 9.53.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, ADR-007, Instrument/Venue identity và correction semantics (v0.2/v0.3 không đổi). `instrument_id`/`venue_id`/`listing_id` — không đổi tên, không đổi shape. Không B-package schema edit. Không speculative C2–C7 semantics — `ActiveListingActivationRequested.requested_by_ref` chỉ opaque reference, không author Account/Strategy/Risk. Không cyclic causation còn sót. Không Current View authority violation còn sót. Không uncorrectable reservation fact còn sót. Không reservation look-ahead. Không runtime/module commitment (locking/serialization engine cụ thể vẫn deferred §23).

### Attack-scenario results — 32/32 pass

Activation request recorded; grant causally references request; rejection causally references request; grant và rejection cùng emit cho một request (cấm — đúng một outcome); activation emit trước grant (cấm — grant phải visible trước); grant references resulting activation event (cấm — đóng chu trình); causal cycle attempted (cấm tường minh); granted reservation không có activation event (giữ held tới release tường minh, không timeout ngầm); wrong listing ID trong grant (cấm — Part E); wrong pair trong grant (cấm — Part E); duplicate valid grant (cấm — reservation subject state machine); erroneous reservation grant (dùng correction lineage RESERVATION_METADATA_ERROR); erroneous release (correction lineage); erroneous rejection (correction lineage); reservation correction same pair (RESERVATION_METADATA_ERROR, supersedes_fact_ref); reservation correction wrong pair (RESERVATION_PAIR_SCOPE_ERROR, không replacement dưới subject cũ); reservation correction fork (cấm — mười invariant §18); double invalidation (cấm — một invalidation per fact); replacement chưa recorded (không visible); future-effective grant đã recorded (không ảnh hưởng cursor sớm hơn); replay trước grant effective time (chưa eligible); future-effective release đã recorded (tương tự); replay trước release effective time (vẫn held); held activation invalidated nhưng release chưa visible (vẫn held); release visible (available); rejected listing automatic promotion attempted (cấm tường minh); parent eligibility reconstructed dùng Current View (cấm — Part C); authoritative parent stream reconstruction (đúng, bắt buộc); Instrument và Venue evaluate ở cursor khác nhau (cấm — cùng cặp cursor); reservation evaluate ở cursor khác (cấm — Bước 6 cùng cursor Bước 4–5); C2–C7 artifact introduced (không — verified absent); B-package blob changed (không — verified unchanged).

### Self-review findings

Tự phát hiện và tự sửa/xác nhận trước commit: (1) reservation grant causally referencing activation event — tìm thấy tại `ActiveListingReserved` v0.3 invariant, đã sửa (causation nay trỏ request). (2) activation event dùng làm reservation request — không tìm thấy sót lại; `ActiveListingActivationRequested` tách bạch hoàn toàn, subject TradableListing nhưng KHÔNG phải TradableListingCreated/StatusChanged. (3) Current View dùng normatively làm parent authority — tìm thấy tại §15 Bước 4/5 v0.3 ("query InstrumentCurrentView/VenueCurrentView"), đã sửa thành authoritative reconstruction trực tiếp; xác nhận §7/`venue.md` §7 "chỉ query/UI" KHÔNG còn bị §15 mâu thuẫn. (4) reservation fold chỉ dùng recorded time — không tìm thấy trong bản v0.4 (Phase 3 effective eligibility tường minh); xác nhận đây chính là gap v0.3 đã đóng. (5) reservation event thiếu invalidation/replacement rule — đóng bằng `ActiveListingReservationFactInvalidated` + `supersedes_fact_ref` trên cả ba event. (6) grant/release thiếu effective-time eligibility — đóng bằng Phase 3 + Part G "visible VÀ effective". (7) automatic promotion wording — không tìm thấy ngoài ngữ cảnh cấm tường minh. (8) raw cross-stream sequence ordering — không tìm thấy ngoài ngữ cảnh cấm tường minh. (9) stale section reference — automated `§N` range-scan (instrument.md 1–24, không renumbering section top-level nào) sạch, manual context review xác nhận đúng ngữ nghĩa. (10) old v0.3 reference — đã cập nhật toàn bộ (frontmatter, intro blockquote, MANIFEST, README, CHANGELOG); các mention "v0.3" còn lại là mô tả lịch sử tường minh (mô tả bug đã sửa), không phải wording sống.

### Changed-file scope

`docs/domain/instrument.md`, `docs/domain/README.md`, `docs/MANIFEST.md`, `docs/CHANGELOG.md`, `docs/domain/context-map.yaml` (comment-only). **`docs/domain/venue.md` KHÔNG đổi** — xác minh: không có nội dung normative nào cần sửa (không tìm thấy cross-reference cần cập nhật do instrument.md giữ nguyên toàn bộ số section top-level; không tìm thấy contradiction với §7 query/UI-only rule). `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`/`context.md`/ADR files/Constitution/OQ files/Package 0.2-C2–C7 artifacts: **không đổi.**

### Metadata / state

- `instrument.md`: **v0.3 → v0.4**, `status: Draft`.
- `venue.md`: **v0.3 không đổi**, `status: Draft`.
- `context-map.yaml`: **v0.10 không đổi** — chỉ sửa comment.
- `README.md` (domain index): **v0.26 → v0.27**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.52 → 9.53**; dòng `domain/` cập nhật ghi nhận final narrow correction, 4 finding Major đã đóng.
- `context.md`, `feature.md`, `regime.md`, `structure.md`, `swing.md`, `candle.md`, mọi ADR file: **không đổi.**

**Chỉ Package 0.2-C1 được correct.** Không author C2–C7. Không sửa ADR. Không Approve/Lock artifact. Không Consolidate. Không đóng OQ-002/OQ-003. Không authorize Live. `instrument_id`/`venue_id`/`listing_id` không đổi tên/shape. Package 0.2-C2–C7 vẫn chưa authorize, chưa author. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — resolve Package 0.2-C1 integration semantics

**Package 0.2-C1 second narrow correction — Current View terminal-invalid semantics, listing eligibility, active-listing arbitration và deterministic status folding.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C1 second narrow correction — Current View terminal-invalid semantics, listing eligibility, active-listing arbitration và deterministic status folding." Đóng đúng bốn finding Major từ Independent Review B: `IRB-C1-MAJ-01` (temporary pending correction và permanently invalid scope-error subject externally indistinguishable), `IRB-C1-MAJ-02` (TradableListing eligibility không đối xứng cấm ACTIVE dưới Venue RETIRED), `IRB-C1-MAJ-03` (tối đa một ACTIVE listing per pair thiếu deterministic cross-stream enforcement), `IRB-C1-MAJ-04` (status folding thiếu canonical bitemporal total-order policy). Authorization này **không** cho phép redesign toàn Package C1, không author C2–C7, không sửa ADR, không Approve/Lock/Consolidate/đóng OQ/authorize Live.

### Part A — Current View correction classification (đóng `IRB-C1-MAJ-01`)

Thêm `pending_correction_class` (`instrument.md` §19) — enum đóng `AWAITING_SAME_SUBJECT_REPLACEMENT`/`TERMINAL_SCOPE_INVALIDATION`, bắt buộc khi `view_state = PENDING_CORRECTION`, cấm khi `VALID`. Mapping đóng: `initial_fact_correction_class = METADATA_ERROR` → `AWAITING_SAME_SUBJECT_REPLACEMENT`; `= SCOPE_ERROR` → `TERMINAL_SCOPE_INVALIDATION`; chờ replacement một `*MetadataRevised`/`*StatusChanged` → `AWAITING_SAME_SUBJECT_REPLACEMENT` (không bao giờ TERMINAL — correction loại này luôn same-subject); same-effective-time status conflict → `AWAITING_SAME_SUBJECT_REPLACEMENT`. Áp dụng thống nhất `InstrumentCurrentView` (§7), `TradableListingCurrentView` (§15), `VenueCurrentView` (`venue.md` §7). Pin bổ sung: `TERMINAL_SCOPE_INVALIDATION` không bao giờ transition về VALID; subject mới sau SCOPE_ERROR có Current View độc lập hoàn toàn; subject cũ vẫn queryable làm historical invalid evidence; consumer/retry worker không được coi TERMINAL là "chờ và thử lại".

### Part B — Symmetric TradableListing eligibility (đóng `IRB-C1-MAJ-02`)

`instrument.md` §10/§11/§13: `TradableListingCreated` và `TradableListingStatusChanged(new_status=ACTIVE)` nay cấm khi Logical Instrument **HOẶC** Logical Venue tương ứng đã RETIRED tại effective_time đó — v0.2 chỉ enforce phía Instrument dù `venue.md` đã claim "đối xứng" (claim không có cơ chế đứng sau). Preferred mechanism: authoritative listing lifecycle event giữ nguyên lịch sử (không fabricate `TradableListingStatusChanged`); `TradableListingCurrentView` (§15) derive `eligibility_state` (`ELIGIBLE`/`INELIGIBLE_PARENT_STATE`) và `current_status: SUSPENDED` khi parent RETIRED hoặc PENDING_CORRECTION tại cùng cursor — retirement muộn của parent không mutate lịch sử, chỉ đổi derived view từ effective_time của retirement trở đi; correction của parent retirement tự động khôi phục eligibility, không cần sửa gì ở TradableListing.

### Part C — Pair-scoped active-listing arbitration (đóng `IRB-C1-MAJ-03`)

Thêm `active_listing_arbitration_policy: PAIR_SCOPED_AUTHORITATIVE_RESERVATION` (`instrument.md` §16/§17) — subject mới `ActiveListingReservation`, continuous theo `(instrument_id, venue_id)`, độc lập TradableListing, là authority boundary duy nhất cho "tối đa một ACTIVE listing per pair". Ba event mới: `ActiveListingReserved` (grant, causal tới activation request, serialize trong chính stream reservation), `ActiveListingReservationReleased` (release — `VOLUNTARY_STATUS_CHANGE` hoặc `CORRECTION_INVALIDATION`), `ActiveListingActivationRejected` (audit record, không đổi state). `TradableListingCreated`/`TradableListingStatusChanged(ACTIVE)` nay bắt buộc causation tới `ActiveListingReserved` tương ứng. Không dùng raw cross-stream `sequence` hay ingestion arrival order để xác lập precedence. Không automatic promotion — một listing từng bị reject không tự động trở thành holder khi reservation cũ release, cần activation request mới tường minh. Correction/invalidation của activation event đang held reservation kích hoạt `ActiveListingReservationReleased` causally-linked (reason: `CORRECTION_INVALIDATION`) — tái dùng correction lineage hiện có, không nhân đôi cơ chế `*FactInvalidated`. Domain Contract authority rule thuần túy — không author runtime locking/module design.

### Part D — Canonical status fold order (đóng `IRB-C1-MAJ-04`)

Pin `status_fold_order_policy: RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER` (`instrument.md` §17), thuật toán 5-phase tường minh tại §7 Bước 3, áp dụng cho `InstrumentStatusChanged`/`TradableListingStatusChanged`/`VenueOperationalStatusChanged`: Phase 1 recorded visibility (`recorded_time <= cursor`); Phase 2 lineage validity (loại fact đã invalidate, chọn lineage head, cấm fork/nhảy cóc); Phase 3 effective eligibility (`effective_time <= cursor`); Phase 4 total deterministic ordering (`effective_time` ASC, `recorded_time` ASC, `event_id` ASC — KHÔNG dùng raw cross-stream `sequence`); Phase 5 transition validation (same-effective-time incompatible transition → conflict → `PENDING_CORRECTION`/`AWAITING_SAME_SUBJECT_REPLACEMENT`, không "ai tới trước thắng"). Loại bỏ mô tả mơ hồ v0.2 "derived bằng fold recorded_time" khỏi `InstrumentStatusChanged` (§5) và `VenueOperationalStatusChanged` (`venue.md` §5) invariant.

### Part E — Cross-subject và arbitration replay

`TradableListingCurrentView` (`instrument.md` §15) nay pin thứ tự tính toán 7-bước cứng: (1) rebuild valid listing creation lineage head; (2) fold metadata patch; (3) fold listing status (5-phase); (4) resolve Instrument eligibility TẠI CÙNG cặp cursor; (5) resolve Venue eligibility TẠI CÙNG cặp cursor; (6) resolve pair-scoped reservation; (7) produce derived eligibility/Current View. Mọi lookup dùng CÙNG recorded-time cursor, effective-time cursor, Definition/contract version — không dùng current/latest parent state cho historical replay.

### Part F — Versioning

`instrument.md` v0.2 → v0.3 (Draft). `venue.md` v0.2 → v0.3 (Draft). `context-map.yaml` **giữ nguyên v0.10** — chỉ sửa comment mô tả trạng thái review. `README.md` v0.25 → v0.26. `MANIFEST.md` manifest_version 9.51 → 9.52.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, ADR-007, Instrument/Venue identity correction v0.2 (`instrument_identity_ref`/`venue_identity_ref` không đổi). `instrument_id`/`venue_id`/`listing_id` — không đổi tên, không đổi shape — mọi B-package reference tiếp tục hoạt động. Không B-package schema edit. Không speculative C2–C7 semantics — `ActiveListingReservation` là subordinate concept trong `instrument.md`, không chạm Account/Order/Execution. Không fabricated parent status event — mechanism dùng derived read-model field, không mutate authoritative stream. Không raw cross-stream sequence ordering ở bất kỳ đâu.

### Attack-scenario results — 26/26 pass

Metadata-error subject chờ replacement; scope-error subject vĩnh viễn invalid; retry worker nhầm terminal với temporary pending; Venue RETIRED có listing ACTIVE (cấm); suspended listing kích hoạt dưới Venue RETIRED (cấm); Instrument RETIRED có listing ACTIVE (cấm); retirement visible sau khi listing activation đã lịch sử (không mutate, chỉ đổi derived view); correction retirement khôi phục eligibility tự động; hai activation ghi nhận đồng thời trên hai stream riêng (reservation stream serialize, một reject); cùng pair cùng effective_time khác listing_id (reservation quyết định); ingestion order đảo ngược (không ảnh hưởng — dùng recorded_time của reservation stream); raw cross-stream sequence trùng nhau (không dùng để xác định thứ tự); winning activation bị invalidate sau đó (kích hoạt ActiveListingReservationReleased, reason CORRECTION_INVALIDATION); reservation released (voluntary qua SUSPENDED/DELISTED); listing từng bị reject tự động promote (cấm — cần activation request mới); future-effective retirement đã recorded (không ảnh hưởng cursor hiện tại); replay trước retirement effective_time (chưa eligible); same-effective-time incompatible status change (conflict → PENDING_CORRECTION); invalidated status fact chưa có replacement visible (PENDING_CORRECTION); replacement visible (VALID trở lại); nhiều generation status correction liên tiếp (lineage head đúng); wrong-subject status replacement (cấm — envelope binding); Instrument và Venue evaluate ở cursor khác nhau (cấm — cùng cặp cursor bắt buộc); listing dùng Current View thay vì authoritative parent fact (cấm — I-12); toàn bộ B-package blob không đổi (verified); C2–C7 vẫn absent (verified).

### Self-review findings

Tự phát hiện và tự sửa/xác nhận trước commit: (1) `PENDING_CORRECTION` không có classification — đã đóng bằng `pending_correction_class` tường minh tại cả ba Current View. (2) wording chỉ enforce Instrument-only listing eligibility — đã tìm thấy và sửa tại `TradableListingCreated`/`TradableListingStatusChanged` (`instrument.md` §11/§13), thêm nhánh Venue RETIRED song song. (3) Venue text claim "đối xứng" nhưng Instrument chưa thực sự enforce — xác nhận đây chính là gap, đã đóng bằng cơ chế thật tại `instrument.md`, cập nhật `venue.md` §1 xác nhận claim nay đã đúng. (4) "latest event wins" wording — không tìm thấy trong status fold description mới (Phase 4/5 dùng total order + explicit conflict rejection, không "ai tới trước"). (5) status fold mô tả chỉ bằng recorded_time — tìm thấy tại `InstrumentStatusChanged` §5 invariant cũ ("derived bằng fold recorded_time"), đã sửa thành tham chiếu `status_fold_order_policy` 5-phase đầy đủ; xác nhận `venue.md` §5 không có wording tương tự (không cần sửa, chỉ thêm tham chiếu). (6) raw sequence cross-stream ordering — không tìm thấy sót lại; `ActiveListingReserved` invariant tường minh cấm dùng sequence xuyên stream. (7) automatic promotion — không tìm thấy; `ActiveListingReservationReleased` invariant tường minh cấm. (8) stale section reference — automated `§N` range-scan (instrument.md 1–24, venue.md 1–18, cross-file instrument.md §N 1–24) sạch, manual context review xác nhận đúng ngữ nghĩa từng citation kể cả các citation §16–§20 bị renumber do chèn section mới. (9) old v0.2 version reference — đã cập nhật toàn bộ (frontmatter, intro blockquote, MANIFEST, README, CHANGELOG).

### Changed-file scope

`docs/domain/instrument.md`, `docs/domain/venue.md`, `docs/domain/README.md`, `docs/MANIFEST.md`, `docs/CHANGELOG.md`, `docs/domain/context-map.yaml` (comment-only). `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`/`context.md`/ADR files/Constitution/OQ files/Package 0.2-C2–C7 artifacts: **không đổi.**

### Metadata / state

- `instrument.md`: **v0.2 → v0.3**, `status: Draft`.
- `venue.md`: **v0.2 → v0.3**, `status: Draft`.
- `context-map.yaml`: **v0.10 không đổi** — chỉ sửa comment.
- `README.md` (domain index): **v0.25 → v0.26**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.51 → 9.52**; dòng `domain/` cập nhật ghi nhận second narrow correction, 4 finding Major đã đóng.
- `context.md`, `feature.md`, `regime.md`, `structure.md`, `swing.md`, `candle.md`, mọi ADR file: **không đổi.**

**Chỉ Package 0.2-C1 được correct.** Không author C2–C7. Không sửa ADR. Không Approve/Lock artifact. Không Consolidate. Không đóng OQ-002/OQ-003. Không authorize Live. `instrument_id`/`venue_id`/`listing_id` không đổi tên/shape. Package 0.2-C2–C7 vẫn chưa authorize, chưa author. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — correct Package 0.2-C1 identity and revision semantics

**Package 0.2-C1 narrow correction — identity uniqueness, revision semantics và initial-fact correction.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Product Owner authorized: "Package 0.2-C1 narrow correction — identity uniqueness, revision semantics và initial-fact correction." Đóng đúng ba finding Major từ ChatGPT Review A: `RA-C1-MAJ-01` (Instrument/Venue identity scope không unique-discriminating), `RA-C1-MAJ-02` (revision payload không pin snapshot/patch/clear semantics), `RA-C1-MAJ-03` (initial authoritative registration/creation fact không thể sửa). Authorization này **không** cho phép redesign, không author C2–C7, không Approve/Lock/Consolidate/đóng OQ/authorize Live.

### Part A — Instrument identity uniqueness (đóng `RA-C1-MAJ-01`)

Thêm `instrument_identity_ref` (`instrument.md` §1) — discriminator opaque bất biến, bắt buộc, canonical external/reference identity, KHÔNG parse, ổn định suốt vòng đời Logical Instrument. Tham gia đầy đủ: immutable scope §1; `subject_ref.scope` §2; payload `InstrumentRegistered` §3; deterministic identity resolution/equality-dedup (invariant §1); `InstrumentCurrentView.scope` §7. Hai instrument kinh tế khác biệt PHẢI có `instrument_identity_ref` khác nhau — kể cả khi `base_asset_ref`/`quote_asset_ref`/`instrument_type`/`contract_expiry_ref` trùng nhau. `base_asset_ref`/`quote_asset_ref`/`instrument_type`/`contract_expiry_ref`/`settlement_type` giữ vai trò descriptive, không còn một mình gánh uniqueness. Derivative guardrail: `OPTION` **RESERVED_NOT_AUTHORED in C1** — loại khỏi active closed enum (`instrument_type: [SPOT, PERPETUAL, FUTURE]`), deferred tới khi strike/option-side/exercise-style/settlement-identity được author đầy đủ; không partial-support OPTION. FUTURE/PERPETUAL: `settlement_type` bắt buộc explicit; không identity collision dù base/quote/expiry trùng.

### Part B — Venue identity uniqueness (đóng `RA-C1-MAJ-01`)

Thêm `venue_identity_ref` (`venue.md` §1) — canonical legal/operator/reference identity, opaque, KHÔNG parse, ổn định xuyên display-name/endpoint/adapter/environment change. Tham gia đầy đủ: immutable Venue scope §1; `subject_ref.scope` §2; payload `VenueRegistered` §3; equality-dedup (invariant §1); `VenueCurrentView.scope` §7. Hai logical venue phân biệt PHẢI có `venue_identity_ref` khác nhau dù `venue_type`/`jurisdiction_ref` trùng. KHÔNG dùng: URL; hostname; display name; API adapter ID; credential; environment name.

### Part C — Canonical revision semantics (đóng `RA-C1-MAJ-02`)

Pin canonical `revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET` một nơi duy nhất (`instrument.md` §16) cho `InstrumentMetadataRevised`/`TradableListingMetadataRevised`/`VenueMetadataRevised`: `changed_fields` (map, required) = SET; `clear_fields` (array, required, may be empty) = CLEAR; field vắng mặt = UNCHANGED; `changed_fields ∩ clear_fields = ∅`; required field cấm xuất hiện trong `clear_fields`; field không rõ/immutable/scope-identity CẤM tuyệt đối; ít nhất một effective change bắt buộc (map và array không được cùng rỗng). Whitelist patchable field theo event: `InstrumentMetadataRevised` (display_name, classification_tags — cả hai optional/clearable); `VenueMetadataRevised` (display_name optional/clearable; timezone_ref, default_session_calendar_ref required/không-clearable; default_precision_policy_ref optional/clearable); `TradableListingMetadataRevised` (venue_symbol, price_increment, quantity_increment, session_calendar_ref required/không-clearable; min_quantity, min_notional optional/clearable). Current View fold algorithm pin tường minh 3 bước (registration lineage head → metadata patch fold theo `metadata_fold_order_policy` → status fold) — mọi implementation cho cùng kết quả.

### Part D — Initial-fact correction policy (đóng `RA-C1-MAJ-03`)

Pin canonical `initial_fact_correction_policy: INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES` (`instrument.md` §18, áp dụng nguyên văn cho Venue tại `venue.md` §11). `InstrumentRegistered`/`TradableListingCreated`/`VenueRegistered` nay là target hợp lệ cho `*FactInvalidated`, phân biệt qua `initial_fact_correction_class` (enum, `METADATA_ERROR`/`SCOPE_ERROR`, required chỉ khi target là initial fact): same-scope metadata error → invalidate + replacement registration fact CÙNG subject, `supersedes_fact_ref` trỏ về fact bị invalidate, scope giống hệt; scope/identity error → invalidate, KHÔNG replace dưới subject cũ, đăng ký subject MỚI với `instrument_id`/`venue_id`/`listing_id` mới, subject cũ không còn authoritative. Deterministic Current View rule: invalidation visible + replacement/new-subject không visible = `view_state: PENDING_CORRECTION` (vĩnh viễn nếu SCOPE_ERROR). "Một registration" nay nghĩa là **một VALID lineage head**, không phải "một event record duy nhất mãi mãi" — loại bỏ hoàn toàn khung diễn đạt cũ. Bảo toàn: exact subject/effective-time binding; một invalidation per fact; append-only; recorded-time visibility; no look-ahead; deterministic correction lineage.

### Part E — Versioning

`instrument.md` v0.1 → v0.2 (Draft). `venue.md` v0.1 → v0.2 (Draft). `context-map.yaml` **giữ nguyên v0.10** — chỉ sửa comment mô tả trạng thái review, không sửa structure/relationship. `README.md` v0.24 → v0.25. `MANIFEST.md` manifest_version 9.50 → 9.51. Không bump Domain Contract nào khác.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, ADR-007. `instrument_id`/`venue_id` — **không đổi tên, không đổi shape** (`opaque string`) — mọi B-package reference hiện có (`ref: instrument`/`ref: venue`) tiếp tục hoạt động không cần sửa. Context Map registry (`context-map.yaml`) không đổi structure/relationship. Không speculative relationship cho Account/Order/Execution tương lai — chỉ chuẩn bị identity đủ mạnh, không author trước những concept đó.

### Attack-scenario results — 24/24 pass

Hai derivative kinh tế khác biệt cùng base/quote/expiry/settlement (identity phân biệt qua `instrument_identity_ref`); hai venue cùng jurisdiction/type nhưng khác operator (`venue_identity_ref` phân biệt); OPTION payload cố tình gửi (cấm — reserved-not-authored); FUTURE/PERPETUAL thiếu `settlement_type` (cấm invariant); empty patch (`changed_fields`/`clear_fields` cùng rỗng — cấm, ít nhất một effective change); patch chứa scope/identity field (cấm whitelist); patch clear một required field (cấm — required không clearable); patch field không rõ/ngoài whitelist (cấm); `changed_fields`/`clear_fields` overlap cùng field (cấm disjoint); hai implementation fold cùng patch stream cho kết quả khác nhau (loại bằng `metadata_fold_order_policy` deterministic); correction InstrumentRegistered cùng scope (METADATA_ERROR → same-subject replacement); correction InstrumentRegistered khác scope (SCOPE_ERROR → subject mới, subject cũ PENDING_CORRECTION vĩnh viễn); invalidate initial fact không có `initial_fact_correction_class` (cấm — required khi target initial fact); `initial_fact_correction_class` có mặt khi target không phải initial fact (cấm); double-invalidate cùng fact (cấm — một invalidation per fact); replacement supersedes_fact_ref trỏ sai lineage head (cấm — phải đúng lineage head); replacement scope khác fact bị supersede dùng supersedes_fact_ref thay vì subject mới (cấm — phải theo SCOPE_ERROR path); replay trước correction chỉ thấy fact gốc; correction visible sau replay cursor; Current View trước bất kỳ replacement/new-subject nào (PENDING_CORRECTION); raw symbol/URL dùng làm `instrument_identity_ref`/`venue_identity_ref` (cấm — không parse, không phải display/URL/hostname/credential); credential dùng làm `venue_identity_ref` (cấm tường minh); hai TradableListing patch đồng thời cho cùng field (deterministic order theo `metadata_fold_order_policy`); B-package artifact blob không đổi (verified); `instrument_id`/`venue_id` shape/tên không đổi (verified).

### Self-review findings

Tự phát hiện và tự sửa/xác nhận trước commit: (1) stale section reference — không tìm thấy, automated `§N` range-scan (instrument.md 1–23, venue.md 1–18, cross-file `instrument.md §N` 1–23) sạch, manual context review xác nhận đúng ngữ nghĩa từng citation. (2) old enum value `OPTION` trong `instrument_type` active enum — đã loại bỏ khỏi enum values, chỉ còn trong mô tả reserved-not-authored. (3) claim "registration không bao giờ invalidate được" — đã loại bỏ khỏi `InstrumentFactInvalidated`/`VenueFactInvalidated` §6 (cả hai file), nay tường minh cho phép target initial fact. (4) literal "đúng một registration event" wording — đã thay bằng "đúng một VALID lineage head — KHÔNG phải một event record duy nhất mãi mãi" tại cả `InstrumentRegistered` (`instrument.md` §3) và `VenueRegistered` (`venue.md` §3). (5) partial-patch ambiguity — loại bỏ hoàn toàn bằng `changed_fields`/`clear_fields` tường minh, disjoint, at-least-one-effective-change. (6) identity rule chỉ dựa descriptive field — đã đóng bằng `instrument_identity_ref`/`venue_identity_ref`. (7) **judgment call tường minh:** giữ nguyên tên field `min_quantity`/`min_notional` trong `TradableListingCreated`/`TradableListingMetadataRevised` — KHÔNG đổi thành `minimum_quantity`/`minimum_notional` như văn bản mô tả task Part C liệt kê, vì coi đó là mô tả minh họa chứ không phải chỉ thị rename tường minh, và việc rename sẽ tạo bất nhất không cần thiết với schema `TradableListingCreated` hiện có (task không yêu cầu sửa field đó ngoài thêm `supersedes_fact_ref`).

### Changed-file scope

`docs/domain/instrument.md`, `docs/domain/venue.md`, `docs/domain/README.md`, `docs/MANIFEST.md`, `docs/CHANGELOG.md`, `docs/domain/context-map.yaml` (comment-only). `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`/`context.md`/ADR files/Constitution/OQ files/Package 0.2-C2–C7 artifacts: **không đổi.**

### Metadata / state

- `instrument.md`: **v0.1 → v0.2**, `status: Draft`.
- `venue.md`: **v0.1 → v0.2**, `status: Draft`.
- `context-map.yaml`: **v0.10 không đổi** — chỉ sửa comment.
- `README.md` (domain index): **v0.24 → v0.25**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.50 → 9.51**; dòng `domain/` cập nhật ghi nhận narrow correction, 3 finding Major đã đóng.
- `context.md`, `feature.md`, `regime.md`, `structure.md`, `swing.md`, `candle.md`, mọi ADR file: **không đổi.**

**Chỉ Package 0.2-C1 được correct.** Không author C2–C7. Không sửa ADR. Không Approve/Lock artifact. Không Consolidate. Không đóng OQ-002/OQ-003. Không authorize Live. `instrument_id`/`venue_id` không đổi tên/shape. Package 0.2-C2–C7 vẫn chưa authorize, chưa author. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — author Package 0.2-C1 reference foundation

**Package 0.2-C scope definition + Package 0.2-C1 minimal authoring.** Vai trò: `Domain Package Scope Author · AI Technical Architect`. Product Owner authorized: "Authorize Package 0.2-C scope definition and minimal authoring." — cho phép (1) khóa decomposition dự kiến cho Package 0.2-C, (2) mở và author minimal slice đầu tiên Package 0.2-C1, (3) author đúng hai Domain Contract `instrument.md`/`venue.md`, (4) cập nhật registry/index/manifest/changelog cần thiết. Authorization này **không** cho phép author Account/Strategy/Decision/Risk/Position/Order/Fill/Trade Intent/Execution Intent/Replay Event, sửa ADR, Approve/Lock artifact, Consolidate Package 0.2-C1, đóng OQ, authorize Live, hay tuyên bố Phase 0.2 hoàn thành.

### Package 0.2-C decomposition (planning baseline)

```text
0.2-C1 — Reference Foundation: instrument.md, venue.md
0.2-C2 — Trading Account Foundation: account.md, ADR-012 integration
0.2-C3 — Strategy Foundation: strategy.md (Definition + Instance), ADR-013 integration
0.2-C4 — Decision Contract: trade-intent.md, decision.md
0.2-C5 — Risk Gateway Contract: risk.md, execution-intent.md
0.2-C6 — Order & Execution Contract: order.md, fill.md
0.2-C7 — Position & Replay Contract: position.md, replay-event.md

Dependency direction: Instrument + Venue → Account → Strategy →
  Trade Intent/Decision → Risk/Execution Intent → Order/Fill → Position/Replay
```

Đây là planning baseline — KHÔNG phải runtime-module design cuối cùng cho Phase 0.2; một review sau này có thể xác định điều chỉnh narrow cần thiết; chỉ C1 được author trong transaction này; C2–C7 cần Product Owner authorization riêng, từng slice một.

### `instrument.md` v0.1 Draft (mới)

Hai họ subject tách bạch: **Logical Instrument** (`instrument_id` opaque, venue-neutral — `base_asset_ref`/`quote_asset_ref` opaque reference, `instrument_type` enum đóng `SPOT`/`PERPETUAL`/`FUTURE`/`OPTION`, `contract_expiry_ref` khi FUTURE/OPTION; bốn event: `InstrumentRegistered`/`InstrumentMetadataRevised`/`InstrumentStatusChanged`/`InstrumentFactInvalidated`; state machine `UNSEEN→REGISTERED→ACTIVE↔SUSPENDED→RETIRED`, RETIRED terminal) và **TradableListing** (subordinate concept, KHÔNG phải file riêng — identity `(instrument_id, venue_id, listing_id)`, mang venue symbol/price-quantity increment/min quantity-notional/session reference/listing status; bốn event riêng: `TradableListingCreated`/`MetadataRevised`/`StatusChanged`/`FactInvalidated`; cấm hai listing ACTIVE đồng thời cho cùng cặp instrument×venue). Cộng `InstrumentCurrentView` và `TradableListingCurrentView` (non-authoritative read model, no-row semantics). Prohibitions: không sở hữu live price/Candle/Strategy/Decision/Risk/Account/Position/Order/Fill/execution status; TradableListing không chứa credential/execution state/Order-Fill-Position semantics.

### `venue.md` v0.1 Draft (mới)

**Logical Venue** (`venue_id` opaque — `venue_type` enum đóng `CENTRALIZED_EXCHANGE`/`DECENTRALIZED_EXCHANGE`/`BROKER`, `jurisdiction_ref` optional; bốn event: `VenueRegistered`/`VenueMetadataRevised`/`VenueOperationalStatusChanged`/`VenueFactInvalidated`; state machine cùng shape `instrument.md`). Reference concept: timezone, default trading calendar/session policy, default precision policy — venue-neutral, không giả định crypto-only/24/7/một timezone/một session/một adapter/một account model/một symbol format (đúng ADR-007). Environment separation tường minh: KHÔNG trộn Venue identity với production/sandbox endpoint, API credential, adapter instance, deployment environment (Phase 1, deferred). Prohibitions: không sở hữu credential, trading account, adapter implementation, order execution, fill, position, risk/strategy decision.

### Tradable Listing ownership decision

TradableListing là subordinate concept trong `instrument.md` (không phải file C1 riêng) — Logical Instrument sở hữu venue-neutral product semantics; TradableListing sở hữu venue-specific trading constraints. Quyết định tường minh, không để ambiguous.

### Identity rules

`instrument_id`/`venue_id` opaque, không parse; KHÔNG BAO GIỜ là raw venue symbol/API URL; scope identity bất biến sau lần đăng ký đầu (đổi field scope tạo subject mới, không mutate). `instrument_id`/`venue_id` là identifier ĐÃ được mọi Domain Contract Package 0.2-B tham chiếu (`ref: instrument`/`ref: venue`) — `instrument.md`/`venue.md` là nguồn định nghĩa chính thức, KHÔNG đổi tên/shape, mọi Domain Contract B-package hiện có tiếp tục hoạt động không cần sửa.

### Bitemporal/correction rules

Forward-looking revision (thay đổi thật theo thời gian, fact cũ vẫn hợp lệ lịch sử) tách bạch tường minh khỏi correction (`*FactInvalidated` + replacement, sửa sai sót quá khứ) — không gộp hai khái niệm (đóng "tick size changes historically"-style ambiguity). Historical Replay dùng đúng metadata có hiệu lực TẠI cursor, không dùng giá trị hiện tại. No look-ahead. Current View no-row trước fact đầu tiên, non-authoritative.

### Context Map changes

`context-map.yaml` v0.9 → v0.10: `instrument-venue-reference.owned_contracts` forward-declared → authored cho `instrument`/`venue`. **Không** thêm capability/context mới (Account/Strategy/Decision/Risk/Execution/Position KHÔNG đăng ký). **Không** thêm cross-context relationship nào — chưa có contract nào thực sự publish/consume `instrument`/`venue` qua event stream (chỉ `ref:` lookup, không phải event consumption); tránh speculative relationship. 20 relationship hiện có giữ nguyên.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, ADR-007 (venue-neutral — instrument_type đóng không hardcode crypto-only, session/calendar reference không hardcode 24/7), Candle instrument/venue reference (`ref: instrument`/`ref: venue` đã tồn tại sẵn, không cần sửa), Swing/Structure/Regime/Feature/Context subject scope (dùng `instrument_id`/`venue_id` opaque string, không đổi tên/shape). Instrument/Venue ID sẵn sàng cho nhu cầu Account/Order/Execution tương lai mà không cần author trước.

### Attack-scenario results — 20/20 pass

Một logical instrument list trên hai venue (nhiều TradableListing đồng thời, §19 instrument.md); hai venue symbol cho một logical instrument qua thời gian (`TradableListingMetadataRevised`, forward-looking); venue symbol đổi (cùng cơ chế); tick size đổi lịch sử (Historical Replay dùng effective_time đúng cursor, không dùng giá trị hiện tại); venue suspend một listing không ảnh hưởng logical instrument (TradableListingStatusChanged độc lập InstrumentStatusChanged); logical instrument retired trên mọi venue (cross-subject invariant: không TradableListing ACTIVE khi Instrument RETIRED); sandbox/production endpoint cho một Venue (Environment separation §10 venue.md, deferred Phase 1); venue timezone/calendar đổi (`VenueMetadataRevised` forward-looking); replay trước metadata correction (chỉ thấy fact gốc); correction visible sau replay cursor (recorded_time mới); current metadata vô tình dùng cho historical replay (cấm tường minh, §17 instrument.md); raw symbol dùng làm instrument_id (cấm invariant §1); API URL dùng làm venue_id (cấm invariant §1 venue.md); credential đặt trong Venue (cấm §16 venue.md); Order/Fill/Position semantics vô tình lọt vào (cấm §18 instrument.md); giả định crypto 24/7 (cấm §19 instrument.md/§15 venue.md); một instrument có cả spot và perpetual variant (hai instrument_id khác nhau); duplicate listing identity (cấm §10 instrument.md — tối đa một ACTIVE listing/cặp); no Current View trước fact đầu tiên (§7/§15 instrument.md, §7 venue.md); B-package artifact blob không đổi (verified).

### Self-review findings

Tự phát hiện và tự sửa trước commit: (1) thiếu `TradableListingCurrentView` — instrument.md ban đầu chỉ có `InstrumentCurrentView`, không có Current View cho TradableListing dù đây là read model có giá trị thực tế cao hơn; đã bổ sung §15 (`TradableListingCurrentView`), renumbering §15–§20 cũ thành §16–§21. (2) Ba cross-reference `§N` sai trong `instrument.md` (một tự-tham-chiếu thừa ở §1, một trỏ nhầm §11 thay vì §16 cho backfill effective_time, một trỏ nhầm `venue.md §6` thay vì `venue.md §8` cho session/calendar reference — xuất hiện hai lần). (3) Hai cross-reference `§N` trong `venue.md` trỏ tới số cũ của `instrument.md` trước khi renumbering (`§15`→`§16` cho Correction lineage, `§16`→`§17` cho Time semantics) — đã đồng bộ sau khi renumbering `instrument.md`. Toàn bộ đã sửa trước commit; verified bằng automated section-range scan.

### Changed-file scope

`docs/domain/instrument.md` (mới), `docs/domain/venue.md` (mới), `docs/domain/context-map.yaml`, `docs/domain/README.md`, `docs/MANIFEST.md`, `docs/CHANGELOG.md`. `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`/`context.md`/ADR files/Constitution/OQ files/Package 0.2-C2–C7 artifacts: **không đổi.**

### Metadata / state

- `instrument.md`: **mới, v0.1**, `status: Draft`.
- `venue.md`: **mới, v0.1**, `status: Draft`.
- `context-map.yaml`: **v0.9 → v0.10**, `status` giữ `Draft`.
- `README.md` (domain index): **v0.23 → v0.24**, `status` giữ `Draft` — Package 0.2-C decomposition + mục Package 0.2-C1 mới.
- `MANIFEST.md`: `manifest_version` **9.49 → 9.50**; `generated_at` giữ `"2026-07-30"`; dòng `domain/` cập nhật ghi nhận Package 0.2-C decomposition + C1 authored.
- `context.md`, `feature.md`, `regime.md`, `structure.md`, `swing.md`, `candle.md`, mọi ADR file: **không đổi.**

**Chỉ Package 0.2-C1 được author.** Không author Account/Strategy/Decision/Risk/Position/Order/Fill/Trade Intent/Execution Intent/Replay Event. Không sửa ADR. Không Approve/Lock artifact. Không Consolidate Package 0.2-C1. Không đóng OQ-002/OQ-003. Không authorize Live. Package 0.2-C2–C7 vẫn chưa authorize, chưa author. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — consolidate Package 0.2-B4

**Package 0.2-B4 Minimal Context consolidated as `Consolidated Stable`.** Vai trò: `Package Lifecycle Consolidation Author · AI Technical Architect`. Product Owner authorized: "Authorize Package 0.2-B4 consolidation as Consolidated Stable." (2026-07-30). Authorization này cho phép ghi Package 0.2-B4 vào lifecycle state `Consolidated Stable` — nó KHÔNG cho phép Approve/Lock `context.md` hay `context-map.yaml`, không sửa ADR, không đóng OQ, không authorize Live, không author Package 0.2-C, không tuyên bố Phase 0.2 hoàn thành.

### Reviewed baseline pinned

```text
Package 0.2-B4 reviewed HEAD:  cae2b4b115db93ba5f76bcbf28b41c03362789eb

Primary artifact:      context.md v0.2 Draft, blob f9274d5749768151748b9dfa2713118a4fd77791
Integration artifact:  context-map.yaml v0.9 Draft, blob 8ac18383b6ec378f6ef2664e2141f033370277d2
Controlling architecture: ADR-014 v0.2 Approved, blob b2e5757102c360756f1649c93fa8cb61bf931f69
Registry baseline:     MANIFEST v9.48, blob e5000a290698cb3d990d8a0835e3c2e077ddcd90
```

Dependency preserved: `candle.md` v0.4 Draft (unchanged); `swing.md` v0.2 Draft, blob `5bbe666ff404209876a721b1e01cb9ac62011062`; `structure.md` v0.4 Draft, blob `78964dfb6852bbac3fa1e034d64b4fc8031c3fef`; `regime.md` v0.2 Draft, blob `edd1584377f1db84269e7b1dfdd4926d0ce01c70`; `feature.md` v0.2 Draft, blob `2262adf9253ea20c8d817d1066f50c4353d2d35d`.

### Review evidence

```text
ChatGPT final package delta:              Clean — Blocker 0, Major 0, Minor 0, Suggestion 0
Independent Review B final package review: semantic/architecture integration clean — IRB-B4-FINAL-MIN-01 identified
ChatGPT narrow MANIFEST delta:             Clean — Blocker 0, Major 0, Minor 0, Suggestion 0
Independent Review B narrow MANIFEST delta: Clean — IRB-B4-FINAL-MIN-01 Resolved, Blocker 0, Major 0, Minor 0, Suggestion 0 — ready to record Consolidated Stable
```

### Complete finding ledger — all resolved

```text
RA-B4-MAJ-01 / IRB-B4-MAJ-01:  Resolved
IRB-B4-MAJ-02:                 Resolved
IRB-B4-MAJ-03:                 Resolved technically and through ADR-014 governance approval
RA-B4-MIN-02:                  Resolved
IRB-ADR014-MAJ-01:             Resolved
IRB-ADR014-MAJ-02:             Resolved
IRB-ADR014-MIN-01:             Resolved
IRB-ADR014-MIN-02:             Resolved
IRB-B4-FINAL-MIN-01:           Resolved
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

### Package lifecycle meaning

`Consolidated Stable` là package lifecycle/readiness state — nghĩa là: reviewed package baseline nội bộ coherent; mọi qualifying finding đã resolved; package integration đủ ổn định để làm dependency baseline cho package kế tiếp. Nó KHÔNG có nghĩa: artifact Approved; artifact Locked; Domain Contract bất biến; OQ closure; Phase completion; implementation authorization; Live authorization.

### Unchanged artifact statuses

`context.md`: **giữ nguyên** `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null` — không sửa file này trong transaction. `context-map.yaml`: **giữ nguyên** `version: "0.9"`, `status: Draft` — không sửa. `ADR-014.md`: **giữ nguyên** `version: "0.2"`, `status: Approved`, controlling authority — không sửa. `ADR-003.md`: **giữ nguyên byte-for-byte**, embedded `status: Approved`, authoritative lifecycle `Superseded by ADR-014` — không sửa.

### Unchanged OQ/Live/Phase states

OQ-002/OQ-003 vẫn `Open` — không đóng. Live vẫn KHÔNG authorize. Package 0.2-C vẫn chưa có artifact nào được author. Phase 0.2 vẫn active và chưa hoàn tất.

### Package states after transaction

```text
Package 0.2-A:   Consolidated Stable
Package 0.2-B1:  Consolidated Stable
Package 0.2-B2:  Consolidated Stable
Package 0.2-B3:  Consolidated Stable
Package 0.2-B4:  Consolidated Stable
Package 0.2-C:   unauthored
```

### Backward Consistency Check

No conflict với Constitution Chapters 2–14, ADR-014 (controlling), ADR-003 (historical lifecycle Superseded), Package 0.2-A/B1/B2/B3, `context.md`, `context-map.yaml`, MANIFEST compatibility range (`ADR-001 ~ ADR-014`). Kết quả: không semantic change; không architecture change; không ADR lifecycle change; package lifecycle record only.

### Attack-scenario results — 15/15 pass

B4 marked `Consolidated Stable` CÓ Product Owner authorization tường minh (quote, 2026-07-30); `context.md` KHÔNG marked Approved; `context.md` KHÔNG marked Locked; `context-map.yaml` KHÔNG marked Approved/Locked; reviewed HEAD ghi đúng `cae2b4b...`; artifact blob ghi đúng (verified via `git ls-tree`); ADR-014 KHÔNG bị đổi/mark Draft (file untouched, verified byte-for-byte); `ADR-003.md` KHÔNG sửa (verified byte-for-byte); không finding nào bị omit (9-item ledger đầy đủ); final totals đúng 0/0/0/0; OQ-002/OQ-003 KHÔNG đóng; Live KHÔNG authorize; Package 0.2-C KHÔNG author; Phase 0.2 KHÔNG mark complete; local/origin HEAD khớp sau push (verify post-commit).

### Changed-file scope

`docs/domain/README.md`, `docs/MANIFEST.md`, `docs/CHANGELOG.md`. `docs/domain/context.md`, `docs/domain/context-map.yaml`, `docs/adr/ADR-014.md`, `docs/adr/ADR-003.md`, `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`/Constitution/OQ files/Package 0.2-C artifacts: **không đổi.**

### Metadata / state

- `README.md` (domain index): **v0.22 → v0.23**, `status` giữ `Draft` — Package 0.2-B4 section rewritten thành `Consolidated Stable` + baseline section mới.
- `MANIFEST.md`: `manifest_version` **9.48 → 9.49**; `generated_at` giữ `"2026-07-30"`; `compatible_adr_range` giữ `"ADR-001 ~ ADR-014"`; dòng `domain/` cập nhật ghi nhận Package 0.2-B4 `Consolidated Stable`.
- `context.md`, `context-map.yaml`, `ADR-014.md`, `ADR-003.md`, `candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`: **không đổi.**

**Package 0.2-B4 nay `Consolidated Stable` — Package 0.2-B (tổng thể) nay đều `Consolidated Stable`.** Không Approve/Lock `context.md` hay `context-map.yaml`; không sửa ADR; không đóng OQ-002/OQ-003; không authorize Live; không author Package 0.2-C; không tuyên bố Phase 0.2 hoàn thành. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — include controlling ADR-014 (MANIFEST metadata correction)

**Narrow lockfile/registry metadata correction — không phải approval, không phải Lock, không phải Consolidate, không đóng OQ, không authorize Live, không sửa Domain Contract hay ADR decision.** Vai trò: `Documentation Registry Correction Author · AI Technical Architect`.

### Finding resolved

`IRB-B4-FINAL-MIN-01` — `docs/MANIFEST.md` frontmatter `compatible_adr_range: "ADR-001 ~ ADR-013"` mâu thuẫn nội bộ với chính repository state: ADR-014 đã `Approved`/effective/controlling (transaction trước, commit `bb65ec2`), nhưng ADR-014 không nằm trong compatible range đã khai báo. `generated_at: "2026-07-28"` cũng stale so với lifecycle change committed ngày 2026-07-30.

### MANIFEST correction

```yaml
manifest_version: "9.47" → "9.48"
compatible_adr_range: "ADR-001 ~ ADR-013" → "ADR-001 ~ ADR-014"
generated_at: "2026-07-28" → "2026-07-30"
```

Chỉ ba field frontmatter trên thay đổi. **Không đổi:** ADR lifecycle table semantics; ADR-003 `Superseded` state; ADR-014 `Approved` state; domain package state (Package 0.2-A/B1/B2/B3/B4/C); Constitution metadata; `project_version`; `current_phase`; `schema_version`.

### Metadata-only correction — xác nhận tường minh

Đây là metadata-only correction — **không đổi domain semantic nào; không đổi ADR content nào; không phải approval; không Lock; không Consolidate Package 0.2-B4; không đóng OQ-002/OQ-003; không authorize Live.**

### Semantic no-change verification

`docs/adr/ADR-014.md`, `docs/adr/ADR-003.md`, `docs/domain/context.md`, `docs/domain/context-map.yaml`, `docs/domain/README.md` — **không chạm, không đổi.** `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`/Constitution/OQ files/Package 0.2-C artifacts — không đổi.

### Metadata / state

- `MANIFEST.md`: `manifest_version` **9.47 → 9.48**; `compatible_adr_range` **ADR-001 ~ ADR-013 → ADR-001 ~ ADR-014**; `generated_at` **2026-07-28 → 2026-07-30**.
- `ADR-014.md`: **không đổi** — vẫn `version: "0.2"`, `status: Approved`, controlling authority, `approved_at: "2026-07-30"`.
- `ADR-003.md`: **không đổi** — byte-for-byte, embedded `status: Approved`, current authoritative lifecycle `Superseded by ADR-014`.
- `context.md`: **không đổi** — `version: "0.2"`, `status: Draft`.
- `context-map.yaml`: **không đổi** — `version: "0.9"`, `status: Draft`.
- `README.md`, `candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, other ADR: **không đổi.**

MANIFEST registry nay internally coherent — ADR compatibility range phản ánh đúng ADR-001 through ADR-014. Package 0.2-B4 vẫn `Draft`, architecture/semantic review clean, **chưa `Consolidated Stable`**. Không Product Owner Approve; không Lock; không Consolidate; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-C vẫn chưa có artifact nào được author. Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — approve ADR-014 and supersede ADR-003

**ADR lifecycle transaction — Product Owner approval + atomic supersession recording.** Vai trò: `ADR Lifecycle Transaction Author · AI Technical Architect`. Product Owner decision: "Approve ADR-014." (2026-07-30). Product Owner là authority duy nhất approve ADR ([Chapter 11 §11.5](constitution/11-adr-process.md)) — quyết định này KHÔNG được diễn giải thành approval cho Package 0.2-B4, artifact Lock, consolidation, OQ closure, hay Live authorization.

### Governance objective — atomic transaction thực hiện

1. Approve `ADR-014.md` (v0.2, `Draft → Approved`).
2. Làm ADR-014 có hiệu lực (`supersedes: [ADR-003]` nay effective).
3. Ghi nhận review evidence hợp lệ (ChatGPT + Claude, narrow delta, Clean 0/0/0/0 mỗi bên).
4. Ghi nhận ADR-003 `Superseded` tại authoritative registry (MANIFEST).
5. Ghi nhận reverse supersession relation (`superseded_by: ADR-014`).
6. Clear `IRB-B4-MAJ-03` như một governance blocker.
7. Bảo toàn Package 0.2-B4 ở `Draft`, không `Consolidated Stable`.

### ADR-014 lifecycle transition

`docs/adr/ADR-014.md`: `version: "0.2"` (không đổi), `status: Draft → Approved`, `owner: Product Owner`, `approved_by: null → Product Owner`, `approved_at: null → "2026-07-30"`, `reviewers: [] → [ChatGPT, Claude]`, `last_review: null → "2026-07-30"`, `next_review: null` (giữ nguyên, đúng convention `ADR-012`/`ADR-013`), `supersedes: [ADR-003]` (không đổi, nay effective). Không sửa Decision content (Definition-pinned fan-in rule, Context prohibition list, canonical rule, Alternatives considered) — chỉ lifecycle wording thay đổi để phản ánh approval đã xảy ra.

### Review evidence

Bảng "Independent reviews" thêm 2 dòng mới: **ChatGPT** (AI Technical Architect) — Clean narrow delta, 0 Blocker/Major/Minor/Suggestion; **Claude** (AI Technical Architect) — Clean narrow delta, độc lập, 0 Blocker/Major/Minor/Suggestion. Bốn dòng lịch sử (Independent Review B, v0.1 findings) được BẢO TOÀN nguyên vẹn — không xóa "con đường" ADR-014 đạt v0.2. Không tính Product Owner, không tính tác giả revision, không đếm trùng một actor, không phát minh identity thứ ba. Reviewer REVIEW — không APPROVE; Product Owner là authority duy nhất approve/reject.

### Accepted risks

Product Owner chấp nhận đúng sáu residual risk đã ghi nhận trong ADR-014 (Coupling increase; Correction cascade; Definition-version mismatch; Duplicate temporal-alignment implementation; Context scope creep; Feature scope creep), có điều kiện theo đúng mitigation đã pin cho từng risk (không mitigation nào bị suy yếu/xóa; không risk nào ngoài sáu risk này được ghi nhận accepted).

### ADR-003 supersession

`docs/adr/ADR-003.md` **KHÔNG sửa** — byte-for-byte unchanged, blob không đổi, embedded `status: Approved` vĩnh viễn (Chapter 11 §11.3). `docs/MANIFEST.md` — cả hai bảng ADR (file-listing table với cột Supersedes/Superseded By, và ADR-lifecycle narrative table) cập nhật: ADR-003 → current authoritative lifecycle state **Superseded** (2026-07-30), `Superseded By: ADR-014`; ADR-014 → **Approved**, `Supersedes: ADR-003` (nay hiệu lực). Ghi rõ tường minh phân biệt: embedded ADR-003 document status = `Approved` và immutable; current authoritative lifecycle state = `Superseded by ADR-014`. Không tạo tuyên bố mâu thuẫn rằng ADR-003 vẫn "controlling" — **ADR-014 là controlling authority**, ADR-003 là historical immutable evidence.

### B4 blocker transition

`IRB-B4-MAJ-03` (ADR-003 fan-in authority conflict trên Package 0.2-B4) **governance-resolved bởi ADR-014 approval**. Package 0.2-B4 chuyển: `Draft`, architecture blocker cleared, technical review clean (20 attack scenario B4 v0.2 + 16 attack scenario ADR-014 v0.2, cả hai đã pass ở transaction trước) — **KHÔNG** `Approved`/`Locked`/`Consolidated Stable`/`completed`. B4 vẫn cần một transaction package delta review/consolidation riêng của chính nó.

### Context references

`docs/domain/context.md`: sửa lifecycle wording tại intro blockquote, §9a (v0.2 note), traceability-correction note, §17 (Context không tính toán lại), §20 (Authority boundary), §22 (Open questions) — tất cả từ "ADR-014 Draft/pending/governance-open" → "ADR-014 Approved/controlling authority/governance-resolved". **Không đổi:** algorithm, input role, cardinality, event schema, identity, bitemporal rule, missing-input policy, correction lineage, Current View, Feature/Context boundary. `context.md` giữ nguyên `version: "0.2"`, `status: Draft` (lifecycle reference-only). `docs/domain/context-map.yaml`: 2 comment block sửa (owned_contracts note + intro comment trước 10 relationship) — KHÔNG đổi relationship structure/provider/consumer/contract_id/purpose field nào; `version` giữ nguyên `"0.9"` (comment-only, đúng precedent transaction trước).

### Backward Consistency Check

No conflict với Constitution Chapter 11 (approval transition + supersede thực hiện đúng §11.6/§11.8), ADR-003 (nội dung Regime/Structure độc lập không đổi, chỉ boundary "Feature Engine fan-in duy nhất" được ADR-014 amend), ADR-007, ADR-009, ADR-010. `context.md`/`context-map.yaml` — không domain-semantic regression. Kết quả: ADR-014 Approved và effective; ADR-003 immutable document không đổi, authoritative lifecycle Superseded; không semantic regression nào.

### Attack-scenario results — 15/15 pass

ADR-014 marked Approved CÓ Product Owner evidence tường minh (quote "Approve ADR-014.", ngày 2026-07-30); reviewer (ChatGPT/Claude) không được diễn giải thành approver — Product Owner mới approve; không actor nào đếm trùng (ChatGPT ≠ Claude ≠ Product Owner ≠ author); `ADR-003.md` content KHÔNG sửa (blob verified identical); MANIFEST KHÔNG tuyên bố cả hai ADR đều controlling — chỉ ADR-014 controlling, ADR-003 historical; ADR-014 approved VÀ reverse supersession (`superseded_by: ADR-014` trên dòng ADR-003) ghi nhận cùng lúc, không thiếu; không risk nào ngoài 6 risk đã document được mark accepted; không mitigation nào bị xóa trong lúc accept; B4 KHÔNG bị mark `Consolidated Stable`; Context semantic contract KHÔNG đổi trong transaction này (chỉ lifecycle wording); OQ-002/OQ-003 KHÔNG đóng; Live KHÔNG authorize; Package 0.2-C KHÔNG được author; ADR-014 chỉ trở thành controlling SAU atomic transaction (không có trạng thái trung gian nửa-hiệu-lực); local và origin HEAD khớp sau push (verify post-commit).

### Changed-file scope

`docs/adr/ADR-014.md`, `docs/domain/context.md` (lifecycle wording only), `docs/domain/context-map.yaml` (2 comment block), `docs/domain/README.md`, `docs/MANIFEST.md`, `docs/CHANGELOG.md`. `docs/adr/ADR-003.md` **KHÔNG sửa** — verified byte-for-byte unchanged. `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`/other ADR: không đổi.

### Metadata / state

- `ADR-014.md`: `version` giữ `"0.2"`, `status: Draft → Approved`, `reviewers: [] → [ChatGPT, Claude]`, `approved_by/approved_at` set.
- `ADR-003.md`: **byte-for-byte unchanged.**
- `context.md`: giữ `version: "0.2"`, `status: Draft` — lifecycle reference-only correction.
- `context-map.yaml`: giữ `version: "0.9"` — comment-only.
- `README.md` (domain index): **v0.21 → v0.22**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.46 → 9.47**; ADR file-listing table + ADR-lifecycle table cập nhật ADR-003/ADR-014; dòng `domain/` cập nhật B4 blocker transition.
- `candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, other ADR: **không đổi.**

**ADR-014 nay Approved và effective — controlling authority cho ranh giới Feature computation fan-in vs Context snapshot aggregation.** Không Lock; không Consolidate Package 0.2-B4; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-B1/B2/B3 vẫn `Consolidated Stable`; Package 0.2-B4 vẫn `Draft`, architecture blocker cleared nhưng chưa `Consolidated Stable`; Package 0.2-C vẫn chưa có artifact nào được author; Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — tighten ADR-014 authority boundaries

**Narrow ADR revision correction — không phải approval, không phải Lock, không Consolidate, không đóng OQ, không authorize Live, không redesign Feature/Regime/Context.** Vai trò: `ADR Revision Author · AI Technical Architect`.

### Findings resolved

`IRB-ADR014-MAJ-01`, `IRB-ADR014-MAJ-02`, `IRB-ADR014-MIN-01`, `IRB-ADR014-MIN-02` — toàn bộ từ Independent Review B, trên `ADR-014.md` v0.1.

### Part A — Definition-pinned direct fan-in correction (`IRB-ADR014-MAJ-01`)

ADR-014 v0.1 mô tả quyền fan-in ở cấp LAYER (Feature Engine/Context Engine) — có thể bị đọc thành quyền chung, không giới hạn. Thêm quy tắc bắt buộc: fan-in trực tiếp CHỈ hợp lệ cho role/contract ID/contract version được chính Feature Definition hoặc Context Definition khai báo và pin tường minh; contract chưa khai báo, dependency tự chọn ở tầng implementation, và input fallback ngầm định đều bị cấm. Feature: chỉ tiêu thụ Structure/Regime khi `feature_definition_version` cụ thể khai báo role, pin contract ID + version, khai báo role cardinality, và input thực sự cần cho đúng một atomic Feature value — không có quyền chung đọc mọi Structure/Regime event. Context: tương tự, cần `context_definition_version` khai báo role + contract ID + version + cardinality + cutoff/alignment policy — không có quyền chung tự thêm upstream dimension mới (đòi hỏi definition version mới + Domain Contract revision). Canonical rule: "Layer capability does not authorize an input. The consuming Definition authorizes and pins the input."

### Part B — Complete Context authority prohibition (`IRB-ADR014-MAJ-02`)

Context prohibition list v0.1 chỉ có 5 mục, thiếu Risk/Account/Position/Execution và execution/order authority. Mở rộng thành 12 mục đầy đủ: compute new engineered Feature; reproduce Feature formulas; derive trade signal; score/grade setup; make Strategy/Decision/Risk/Account/Position/Execution conclusion; determine execution eligibility; authorize/reject/size/route order. Làm rõ: Context chỉ được copy upstream value khi value đó thuộc authorized input role (Definition-pinned); cấm rename một conclusion thành "context value" để lách domain ownership. Ví dụ payload cấm tuyệt đối: `risk_state`, `execution_allowed`, `position_size`, `order_eligible`.

### Part C — Traceability correction (`IRB-ADR014-MIN-01`)

`docs/domain/context.md`'s "Quan hệ với ADR-003" intro paragraph gán stale finding `RA-B4-MAJ-01`/`IRB-B4-MAJ-01` cho xung đột ADR-003 — sai. Sửa thành `IRB-B4-MAJ-03` (đúng mapping đã pin từ correction trước). Traceability-only, không đổi semantic.

### Part D — Architecture concerns and risks recorded (`IRB-ADR014-MIN-02`)

Ghi nhận đầy đủ trong ADR-014: Risk 1 Coupling increase; Risk 2 Correction cascade; Risk 3 Definition-version mismatch; Risk 4 Duplicate temporal-alignment implementation; Risk 5 Context scope creep; Risk 6 Feature scope creep — mỗi risk kèm mitigation cụ thể. Risk acceptance state ghi rõ: "These are reviewer-identified concerns and risks. They are not Product Owner accepted risks while ADR-014 is Draft." Không populate `Accepted risks` với approval evidence.

### Reviewer-evidence handling

Bốn finding trên đến từ một vòng Independent Review B đã thực sự diễn ra trên `ADR-014.md` v0.1 — ghi nhận HISTORICAL evidence của vòng review đã xảy ra (bảng "Independent reviews" điền identity "Independent Review B" cho cả 4 dòng Concern/Risk/Recommendation), KHÔNG tuyên bố bản v0.2 (transaction này) đã được re-review/delta-review. Không có bằng chứng actor identity thứ hai (ví dụ ChatGPT Review A) đã review riêng `ADR-014.md` — KHÔNG fabricate một identity thứ hai. `frontmatter.reviewers` giữ nguyên `[]` — một tập hai-reviewer hợp lệ theo Chapter 11 §11.5 CHƯA được xác lập cho chính `ADR-014.md`. Tác giả của revision này không được tính là reviewer.

### Preserved decisions

Raw Regime độc lập Structure; Structure độc lập Raw Regime; Feature computation vs Context aggregation distinction; Context direct authoritative input design (bảy role); B4 input cardinality; Context selection algorithm (Phase 1/Phase 2); missing-input policy (enum đóng); correction lineage; current-view semantics; Strategy boundary; ADR-003 nội dung bất biến — **không đổi bất kỳ mục nào trong danh sách này.**

### Backward Consistency Check

No conflict với Constitution Chapters 2–11, ADR-003 (nội dung không đổi, chỉ narrow amendment proposal siết chặt hơn), ADR-007, ADR-009, ADR-010 (không áp dụng). `structure.md`/`regime.md`/`feature.md`/`context.md`/`context-map.yaml` — chỉ 1 sửa traceability trong `context.md`, không sửa semantic nào khác. Kết quả: không còn architecture conflict nào phát sinh MỚI; ADR-014 vẫn Draft và non-effective; B4 vẫn blocked chờ clean delta review và Product Owner decision.

### Attack-scenario results — 16/16 pass

Feature đọc Regime event chưa khai báo → vi phạm rule mới, bị cấm tường minh; Feature đọc Structure role đã khai báo + pin version → hợp lệ theo rule mới; Context thêm liquidity role chưa khai báo → vi phạm rule mới; Context tiêu thụ đúng bảy role đã pin → hợp lệ; Context emit `risk_state`/`execution_allowed`/`position_size` → cấm tường minh (Part B); Context tự tính metric mới → cấm (prohibition list mục 1); Context copy Feature value hiện có thuộc authorized role → hợp lệ (đúng §17 context.md, đúng ADR-014 "copy khi thuộc authorized input role"); Feature publish toàn bộ Context snapshot → cấm (`feature.md` §15, ADR-014 "Feature KHÔNG được sản xuất multi-domain Context snapshot"); Structure correction invalidate nhiều Context snapshot → Risk 2 mitigation (independent correction, append-only); definition-version mismatch → Risk 3 mitigation (ineligible, no snapshot); Feature/Context share temporal utility không share semantic authority → Risk 4 mitigation; không ngụ ý Product Owner risk acceptance → Risk acceptance state tường minh; stale finding reference đã xóa (Part C); ADR-003 không đổi (verified blob).

### Semantic change summary

**Không đổi:** thuật toán Context selection; Feature/Regime/Structure semantics; missing-input policy; correction lineage; current-view semantics; ADR-003 nội dung. **Thay đổi:** ADR-014's Decision text — mở rộng/siết chặt boundary (Definition-pinned fan-in rule mới; Context prohibition list đầy đủ hơn) + risk documentation + 1 traceability fix trong `context.md`. Đây là governance/boundary tightening, không phải redesign.

### Changed-file scope

`docs/adr/ADR-014.md`, `docs/domain/context.md` (1 câu traceability), `docs/domain/README.md`, `docs/MANIFEST.md`. `docs/domain/context-map.yaml` **không đổi** — không có semantic/structural change nào cần thiết (đã kiểm tra, mọi `purpose` field hiện có vẫn chính xác).

### Metadata / state

- `ADR-014.md`: **v0.1 → v0.2**, `status` giữ `Draft`, `reviewers: []` không đổi, `approved_by`/`approved_at` giữ `null`.
- `context.md`: **giữ `version: "0.2"`** (reference-only correction, không phải semantic revision).
- `context-map.yaml`: **giữ `version: "0.9"`**, không đổi.
- `README.md` (domain index): **v0.20 → v0.21**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.45 → 9.46**.
- `candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, `ADR-003.md`, `ADR-012.md`, `ADR-013.md`: **không đổi.**

Không Product Owner Approve; không Lock; không Consolidate; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-B1/B2/B3 vẫn `Consolidated Stable`; Package 0.2-B4 vẫn Draft, blocked chờ ADR-014 (`IRB-B4-MAJ-03` governance-open, cùng bốn finding ADR-014-level mới resolved technically nhưng CHƯA delta-reviewed); Package 0.2-C vẫn chưa có artifact nào được author; Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-30 — correct B4 review finding traceability

**Metadata/reference-only correction — không phải approval, không phải Lock, không phải Consolidate, không đóng OQ, không authorize Live, không đổi executable domain semantic nào.** Vai trò: `Governance Traceability Correction Author · AI Technical Architect`.

### Finding resolved

`RA-B4-MIN-02` — Review finding IDs bị hoán đổi (swapped) trong commit `f1ea03b`.

### Traceability defect

Commit `f1ea03b` ("docs(domain): resolve Context review and fan-in boundary") gán SAI hai finding ID: gán `IRB-B4-MAJ-02` cho xung đột kiến trúc ADR-003, và `IRB-B4-MAJ-03` cho `missing_input_policy` chưa machine-pinned — NGƯỢC với mapping authoritative của Independent Review B report.

### Authoritative mapping (giữ nguyên chính xác)

```text
IRB-B4-MAJ-01: Structure selection circular dependency (= RA-B4-MAJ-01, cùng defect)
IRB-B4-MAJ-02: missing_input_policy is not machine-pinned
IRB-B4-MAJ-03: ADR-003 Feature-only fan-in conflict
```

### References corrected

- `docs/adr/ADR-014.md`: Context section (root-cause citation), Alternatives considered (citation), Consequences (resolved-findings list) — sửa `IRB-B4-MAJ-02`↔`IRB-B4-MAJ-03` cho đúng nghĩa; thêm tường minh câu "`IRB-B4-MAJ-03` is the ADR-003 architecture conflict" và "Final governance statement: `IRB-B4-MAJ-03` remains governance-open until ADR-014 is Approved"; thêm blockquote ghi nhận correction (`RA-B4-MIN-02`).
- `docs/domain/context.md`: intro block (mapping a/b/c), §6 (2 chỗ enum + canonical value), §9 (canonical policy), §21 (deferred-list note), §22 (resolved-findings list trong OQ ADR-014) — sửa toàn bộ 7 occurrence sai; thêm câu tường minh "missing_input_policy correction closes `IRB-B4-MAJ-02`"; thêm đoạn "Narrow traceability correction" ghi nhận sửa lỗi, `version` giữ nguyên `"0.2"`.
- `docs/domain/README.md`: mục "Narrow architecture revision" item 2/3 hoán đổi nội dung (giữ thứ tự trình bày 2→02, 3→03); dòng "Package 0.2-B4 CHƯA đạt Consolidated Stable" sửa danh sách resolved; thêm đoạn traceability-correction note.
- `docs/MANIFEST.md`: dòng `domain/` sửa 2 citation + thêm ghi chú correction.
- `docs/domain/context-map.yaml`: MỘT occurrence sai tìm thấy tại comment `context-projection.owned_contracts` (gán `IRB-B4-MAJ-02` cho "blocked pending ADR-014" — sai, đúng phải là `IRB-B4-MAJ-03`) — đã sửa. Không có occurrence sai nào khác trong file này (10 relationship `purpose` field không cite finding ID cụ thể).
- `docs/CHANGELOG.md`: entry trước (`f1ea03b`) sửa 3 occurrence sai tại chỗ (Findings/ADR conflict analysis/Missing-input policy correction/governance closing statement) để giữ historical record chính xác.

### Semantic no-change verification

Không sửa: `missing_input_policy` enum value/type; Eligible Upstream Fact selection algorithm (Phase 1/Phase 2); `MarketContextSnapshot`/`MarketContextFactInvalidated` event schema; subject identity; correction lineage invariant; `context-map.yaml` relationship (provider/consumer/contract_id/translation_policy/consumer_obligation) — chỉ 1 comment string sửa. ADR-014's architecture decision (Feature computation fan-in vs Context snapshot aggregation) không đổi — chỉ sửa citation.

### ADR lifecycle verification

`ADR-003.md`: không chạm, `status: Approved`, blob không đổi. `ADR-014.md`: vẫn `status: Draft`, `reviewers: []`, `approved_by: null`, `version` giữ `"0.1"` (correction pre-review, không cần bump theo governance — chưa từng có review nào để "revise" theo nghĩa Chapter 11 §11.4). Không fabricate review evidence.

### Metadata / state

- `context.md`: **giữ `version: "0.2"`**, `status: Draft` (reference-only correction, không phải semantic revision).
- `ADR-014.md`: **giữ `version: "0.1"`**, `status: Draft`, unreviewed, unapproved.
- `context-map.yaml`: **giữ `version: "0.9"`** (chỉ 1 comment string sửa, không phải structural change).
- `README.md`: **v0.19 → v0.20**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.44 → 9.45**.
- `candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, `ADR-003.md`, `ADR-012.md`, `ADR-013.md`: **không đổi.**

Không Product Owner Approve; không Lock; không Consolidate; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-B1/B2/B3 vẫn `Consolidated Stable`; Package 0.2-B4 vẫn Draft, blocked chờ ADR-014 (`IRB-B4-MAJ-03` governance-open); Package 0.2-C vẫn chưa có artifact nào được author; Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-29 — resolve Context review and fan-in boundary (Package 0.2-B4 narrow architecture revision)

**Không phải approval, không phải Lock, không phải Consolidated Stable, không phải re-planning toàn package.** Vai trò: `Architecture Decision Revision Author + Domain Contract Revision Author · AI Technical Architect`. Authorization gate: Product Owner xác nhận tường minh "Authorize narrow amendment of ADR-003 to distinguish Feature computation fan-in from Context snapshot aggregation." trước khi bắt đầu.

### Findings resolved

`RA-B4-MAJ-01` / `IRB-B4-MAJ-01` (cùng một algorithmic defect), `IRB-B4-MAJ-02`, `IRB-B4-MAJ-03`.

### ADR-003 conflict analysis

Văn bản gốc [ADR-003](adr/ADR-003.md) (Approved 2026-07-16): "Feature Engine... là điểm fan-in duy nhất" giữa Structure và Regime. Package 0.2-B4 author Context aggregation layer tiêu thụ trực tiếp authoritative Structure/Regime/Feature fact — đọc theo nghĩa đen, văn bản gốc không phân biệt "Feature computation fan-in" (Feature tự tính giá trị) với "Context snapshot aggregation" (Context chỉ as-of select + sao chép). Đây là root cause `IRB-B4-MAJ-03`.

### ADR lifecycle decision

[Chapter 11 §11.3](constitution/11-adr-process.md): ADR đã `Approved` bất biến byte-for-byte — **không sửa trực tiếp `ADR-003.md`**. Author **`docs/adr/ADR-014.md`** (mới) — narrow amendment qua cơ chế supersede có kiểm soát ([Chapter 11 §11.8](constitution/11-adr-process.md)): `status: Draft`, `reviewers: []`, `approved_by: null`, `supersedes: [ADR-003]` (forward relation ĐỀ XUẤT, chưa có hiệu lực cho tới khi Approved). **Không fabricate review evidence** — bảng "Independent reviews" để trống đúng template, không claim đã approve ngày 2026-07-16 hay bất kỳ ngày nào khác cho văn bản amend. ADR-003 giữ nguyên `Approved`, không mutate. **Package 0.2-B4 blocked khỏi `Consolidated Stable` cho tới khi ADR-014 được Product Owner approve** theo đúng quy trình (tối thiểu hai independent review).

### Revised Feature/Context boundary (ADR-014 nội dung)

Giữ nguyên: Raw Regime độc lập Structure; Structure độc lập Raw Regime; Regime Engine không tiêu thụ Structure; Structure Engine không tiêu thụ Regime; Regime tái sử dụng được cho non-price-action strategy. Amend: phân biệt tường minh **Feature computation fan-in** (Feature Engine sở hữu: tính atomic engineered value, công thức/transformation, selective cross-domain synthesis khi một Feature Definition cần) với **Context snapshot aggregation** (Context sở hữu: as-of selection, cutoff/window alignment, sao chép giá trị, assemble snapshot) — Context KHÔNG tính lại Feature, KHÔNG tái sản xuất công thức, KHÔNG derive signal.

### Structure algorithm correction (§8, `context.md`)

`RA-B4-MAJ-01`/`IRB-B4-MAJ-01`: v0.1 bước 4 (Currency) của role Structure tham chiếu NGƯỢC bước 5 (Not-invalidated) — "*fact có recorded_time LỚN NHẤT trong tập đã qua bước 1–3 VÀ bước 5*". Sửa thành hai phase: **Phase 1 — eligibility filtering** (per-candidate độc lập: identity/scope, recorded-time, effective boundary, role-specific validity-tại-cursor) → **Phase 2 — role-specific current selection** (CHỈ chạy trên survivor Phase 1: Structure chọn recorded_time DESC; Regime/Feature chọn lineage head hiện tại; Candle chọn lineage head hiện tại). Required verdict embedded: Structure A (R10, valid) vs Structure B (R20, invalidated tại R30), cursor R40 → **A được chọn** (B bị loại tại Phase 1, không bao giờ tới Phase 2).

### Missing-input policy correction (§6/§9, `context.md`)

`IRB-B4-MAJ-02`: `missing_input_policy` từ `{type: string}` tự do → `{type: enum, values: [NO_SNAPSHOT_WHEN_ANY_REQUIRED_ROLE_MISSING_OR_PENDING]}`, pin canonical value đúng một lần. Normative behavior: absent/invalidated-không-replacement/pending-correction/definition-version-mismatch/effective-time-ineligible → no snapshot. Cấm tường minh: null filling; stale fallback; partial snapshot; implementation-selected behavior; copy snapshot cũ.

### Context contract changes (`context.md` v0.1 → v0.2)

Intro blockquote: thêm khối "Quan hệ với ADR-003" (giải thích conflict + ADR-014 pending) và version-history note. §6: `missing_input_policy` enum + canonical value. §8: viết lại hoàn toàn thành Phase 1/Phase 2 + required Structure verdict + invalidation↔StructureRecomputed behavior. §9: normative behavior list + cấm tường minh 5 hành vi. §13: target-window tie-break tường minh (`window_end DESC` rồi `window_start DESC`). §17: thêm khối "Context KHÔNG tính toán lại" phân biệt Feature fan-in vs Context fan-in. §20: cập nhật Authority boundary tham chiếu ADR-014 + "KHÔNG sở hữu Feature computation/formula/transformation". §21: xóa `missing_input_policy` khỏi deferred list (nay đã pin canonical). §22: cập nhật OQ về Structure Phase 2 + thêm OQ mới về ADR-014 approval gate. **Không sửa** `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md`.

### Context Map changes (`context-map.yaml` v0.8 → v0.9)

Preserve nguyên vẹn 10 relationship B4 hiện có (provider/consumer/contract_id/status/model_influence/translation_policy/consumer_obligation không đổi) — chỉ **bổ sung field `purpose`** cho cả 10, phân biệt tường minh "authoritative as-of snapshot aggregation — không phải Feature computation, xem ADR-014". Comment block trước 10 relationship cập nhật tham chiếu ADR-014 pending. `owned_contracts` comment cho `context-projection` cập nhật ghi nhận v0.2. **Không thêm** Strategy/Decision/Risk/Account/Position/Execution relationship nào. **Không tái tạo** Signal wording/artifact (verified — 0 occurrence "Signal" ngoài prohibition context).

### Current View clarification (§13, non-blocking cleanup)

Target-window selection làm rõ tường minh 2 tiêu chí tie-break (`effective_window.window_end DESC` rồi `effective_window.window_start DESC`) trước khi đánh giá lineage validity — hành vi không đổi so với v0.1 (tiêu chí 2 vốn ngầm định), chỉ loại bỏ ambiguity.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, [Chapter 11](constitution/11-adr-process.md) (ADR immutability/supersede process — tuân thủ đúng, không mutate ADR-003), ADR-007, ADR-009, ADR-010 (không áp dụng, Context không phải Decision). ADR-003 decision content về Regime/Structure độc lập **không đổi**, chỉ narrow amendment (đề xuất, chưa hiệu lực) cho phần fan-in boundary. `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md` **không sửa semantic**. `context-map.yaml` chỉ additive (field `purpose`) + không relationship nào bị xóa/đổi provider-consumer-contract.

### Attack-scenario results — 20/20 pass

Structure A valid/B invalidated → A selected; B invalidated không có survivor → role missing; invalidation visible trước StructureRecomputed; StructureRecomputed visible và eligible; Regime head invalidated không replacement; Regime replacement visible; Feature head invalidated không replacement; Feature replacement visible; missing role dưới canonical policy; `fill_null` bị cấm tường minh; stale fallback bị cấm tường minh; later-effective candidate visible tại batch cursor (loại ở Phase 1, không tới Phase 2); Context aggregation không recompute Feature (§17); Structure/Regime edge tuân thủ ADR amended boundary; Feature/Context responsibility không overlap; equal window_end dùng window_start tie-break; không tiêu thụ Current View nào; không phát Strategy signal; Backtest/Replay/Paper/Live parity; không regression correction lineage/normalization.

### Preserved semantics

Đúng một Context type; subject identity năm field; Candle-driven cadence; bảy input ref; effective/recorded-time guard; role definition-version pin; normalized input identity; correction lineage (10 invariant); no-row/VALID/PENDING_CORRECTION; Context/Strategy boundary; không Feature-to-Feature change; 10 upstream relationship consolidated (chỉ bổ sung `purpose`, không đổi cấu trúc).

### Metadata / state

- `docs/adr/ADR-014.md`: **mới, v0.1**, `status: Draft`, `supersedes: [ADR-003]` (đề xuất, chưa hiệu lực).
- `docs/adr/ADR-003.md`: **không đổi** — `status: Approved`, bất biến byte-for-byte, blob không đổi.
- `context.md`: **v0.1 → v0.2**, `status` giữ `Draft`.
- `context-map.yaml`: **v0.8 → v0.9**, `status` giữ `Draft`.
- `README.md` (domain index): **v0.18 → v0.19**, `status` giữ `Draft` — Package 0.2-B row + mục Package 0.2-B4 cập nhật ghi nhận revision + ADR-014 blocker.
- `MANIFEST.md`: `manifest_version` **9.43 → 9.44**; thêm dòng ADR-014 (Draft) vào cả hai bảng ADR; dòng `domain/` cập nhật ghi nhận context.md v0.2, ADR-014 blocker.
- `candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, `ADR-012.md`, `ADR-013.md`: **không đổi.**

**KHÔNG sẵn sàng chuyển ChatGPT Review A delta cho tới khi có xác nhận tiếp theo** — findings kỹ thuật (`RA-B4-MAJ-01`/`IRB-B4-MAJ-01`/`IRB-B4-MAJ-02`) đã resolved, nhưng `IRB-B4-MAJ-03` chỉ resolved về mặt PROPOSAL (ADR-014 Draft) — chưa resolved về mặt GOVERNANCE cho tới khi Product Owner approve ADR-014. Không Product Owner Approve; không Lock; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-B1/B2/B3 vẫn `Consolidated Stable`; Package 0.2-B4 active, Draft, chưa `Consolidated Stable`, blocked chờ ADR-014; Package 0.2-C vẫn chưa có artifact nào được author; Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-29 — author minimal Context contract (Package 0.2-B4)

**Không phải approval, không phải review-complete, không phải Consolidated Stable.** Vai trò: `Domain Contract Author · AI Technical Architect`. Authorization gate: Product Owner xác nhận tường minh "Authorize Package 0.2-B4 minimal Context scope." trước khi authoring bắt đầu.

### Phạm vi authoring — scope tối thiểu, không mở rộng framework

`docs/domain/context.md` (mới, v0.1) — điểm hội tụ có kiểm soát `Structure + Raw Regime + Feature → Market Context`, đúng [ADR-003](adr/ADR-003.md). Đúng **một Context type**: `market_context`. Không author Strategy/Decision/Risk/Account/Execution (Package 0.2-C).

### Quyết định thiết kế chính

- **Subject identity — năm field, giống `regime.md`/`feature.md`:** `context_subject_id` deterministic từ `(instrument_id, venue_id, timeframe, context_type, context_definition_version)`.
- **Bảy role bắt buộc mỗi computation point:** một Candle (`context_cutoff_source_ref` — cadence/cutoff driver, KHÔNG phải một `context_values` role) + Structure + hai Regime dimension (Volatility, Directional Persistence) + ba founding Feature type (`volatility_metric`, `directional_persistence_metric`, `distance_to_last_confirmed_swing`). Thiếu bất kỳ role nào → không `MarketContextSnapshot` (valid absence).
- **Computation cadence — `DRIVEN_BY_CANDLE_CLOSE`:** mỗi `candle-closed`/`candle-corrected` tại đúng scope định nghĩa đúng một computation point; `effective_window` = `effective_time` của chính Candle đó; `context_cutoff = effective_window.window_end` (inclusive).
- **Eligible Upstream Fact selection — ordered filter pipeline 5 bước, dùng chung cho cả sáu role, áp dụng ngay từ v0.1 bài học `feature.md` v0.2 (`RA-B3-MAJ-01`/`IRB-B3-MAJ-01`):** identity/scope match → recorded-time visibility → **effective-time cutoff (độc lập, luôn chạy TRƯỚC total order)** → currency (lineage head cho Regime/Feature; "latest recorded_time còn hiệu lực" cho Structure — vì Structure không có `supersedes_fact_ref` chain, mỗi BOS/CHoCH/StructureRecomputed tự set toàn bộ orientation) → not invalidated. Total order tie-break (7 tiêu chí) CHỈ chạy trên tập đã qua cả 5 bước.
- **Structure role không tiêu thụ `StructureCurrentView`** — tự derive "current orientation" từ authoritative `BreakOfStructureDetected`/`ChangeOfCharacterDetected`/`StructureRecomputed`, tái sử dụng methodology fold của `structure.md` §1 (không tích lũy — mỗi event tự set toàn bộ orientation, nên "mới nhất còn hiệu lực" = đúng kết quả fold).
- **`MarketContextFactInvalidated` hỗ trợ nhiều role bị ảnh hưởng đồng thời** (`affected_upstream_roles`, array) — đúng một event cho một fact bị invalidate dù nhiều role cùng bị ảnh hưởng bởi cùng một correction gốc, đóng dedup cascade đúng nguyên tắc `structure.md` §10.
- **`context_values` là bản sao trực tiếp, không tự tính toán lại** — `structure_orientation`/regime class/feature value đều sao chép nguyên vẹn từ đúng fact ref tương ứng, giữ I-1 Explainability qua bảy fact ref tường minh.
- **Không tiêu thụ bất kỳ `*-current-view` nào** (Candle/Structure/Regime/Feature/chính Context) — chỉ authoritative fact.
- **Áp dụng ngay từ v0.1 mọi bài học đã trả giá ở `structure.md`/`regime.md`/`feature.md`:** envelope binding cho `MarketContextFactInvalidated`; input normalization tập toán học; `MarketContextCurrentView` no-row semantics; canonical policy identifier khai báo ĐÚNG MỘT NƠI (ba identifier: `input_normalization_policy`, `current_view_selection_policy`, `eligible_upstream_fact_selection_policy`).

### Self-review — 35 attack scenario

Chạy đủ 35 scenario theo yêu cầu authoring task — bao gồm: first snapshot; identical values hai window liên tiếp; thiếu từng role trong bảy role; Structure/Regime/Feature correction; correction không đổi context_values; nhiều correction ảnh hưởng một snapshot (dedup, `affected_upstream_roles`); một correction ảnh hưởng nhiều snapshot (independent replacement, không dependency-forward); later-effective fact visible tại batch cursor (bị loại ở bước 3, dù recorded-time visible); replacement trước/sau cutoff; duplicate delivery; thứ tự input khác nhau (normalize); duplicate ref; sai role cardinality; cross-stream sequence; invalidation sai subject/window; replacement trước invalidation; lineage fork/skip; latest window pending trong khi window cũ vẫn valid; context_definition_version đổi → subject mới; Backtest/Replay/Paper/Live parity; không tiêu thụ Current View nào; không phát Strategy signal; Context Map wording cleanup không tạo Signal contract; chỉ đúng quan hệ upstream thực sự dùng. Không phát hiện gap cần sửa trước commit.

### Context Map changes

`context-map.yaml` v0.7 → v0.8: `context-projection.owned_contracts` forward-declared → authored; 10 relationship mới (`candle-closed`/`candle-corrected` từ `market-data-observation`; `break-of-structure-detected`/`change-of-character-detected`/`structure-fact-invalidated`/`structure-recomputed` từ `market-structure-analysis`; `regime-classified`/`regime-fact-invalidated` từ `raw-regime-analysis`; `feature-computed`/`feature-fact-invalidated` từ `feature-engineering`, tất cả → `context-projection`) — đúng bảy role mà `market_context` thực sự tiêu thụ, không hơn. **Đồng thời xử lý wording concern deferred từ Package 0.2-B3:** `feature-engineering` (capability và context) responsibility text đổi "Feature/Signal" → "Feature" thuần túy — không tạo Signal capability/contract/relationship nào (đóng ghi chú `feature.md` §20). **Không đổi** bất kỳ relationship hiện có nào khác.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, ADR-003 (trực tiếp controlling, thỏa mãn đầy đủ), ADR-007 (venue-neutrality), ADR-009 (tái sử dụng causal precedence/ordering hiện có), ADR-010 (Decision Time Model — không áp dụng, Context không phải Decision, dùng `effective_time`/`recorded_time` chuẩn Chapter 5, §17 tường minh "Context không phải decision"), `candle.md`/`swing.md`/`structure.md`/`regime.md`/`feature.md` (không sửa semantic, chỉ tiêu thụ contract đã tồn tại), `context-map.yaml` (chỉ additive + một wording fix không ảnh hưởng structure). **Không cần ADR mới.**

### Metadata / state

- `context.md`: **mới, v0.1**, `status: Draft`.
- `context-map.yaml`: **v0.7 → v0.8**, `status` giữ `Draft`.
- `README.md` (domain index): **v0.17 → v0.18**, `status` giữ `Draft` — Package 0.2-B row + mục Package 0.2-B4 mới.
- `MANIFEST.md`: `manifest_version` **9.42 → 9.43**; dòng `domain/` cập nhật ghi nhận B4 Draft, review-chưa-diễn-ra.
- `candle.md`, `swing.md`, `structure.md`, `regime.md`, `feature.md`, `ADR-012.md`, `ADR-013.md`: **không đổi.**

**Sẵn sàng chuyển ChatGPT Review A.** Không Product Owner Approve; không Lock; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-B1/B2/B3 vẫn `Consolidated Stable`; Package 0.2-B4 active, Draft, chưa `Consolidated Stable`; Package 0.2-C vẫn chưa có artifact nào được author; Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-29 — consolidate Package 0.2-B3 stable baseline

**Không phải approval, không phải Lock.** Vai trò: `Domain Package Consolidation Author · AI Technical Architect`. Transaction này **ghi nhận** kết quả review đã hoàn tất — không sửa semantic của `feature.md`.

### Exact baseline

Reviewed HEAD: `ed8813030203cd9e5f779f54be752a3e94c4f68b` (parent: authoring B3 `e53d2ead2a0f5cdc34b6f8803d4105511cf5597a` → narrow revision `ed8813030203cd9e5f779f54be752a3e94c4f68b`).

### Package scope

`feature.md` — điểm fan-in có kiểm soát `Candle/Swing/Raw Regime → Feature` ([ADR-003](adr/ADR-003.md)). Đúng ba founding feature type: `volatility_metric`, `directional_persistence_metric`, `distance_to_last_confirmed_swing`.

### Final artifact blobs

```text
feature.md        v0.2   blob 2262adf9253ea20c8d817d1066f50c4353d2d35d
context-map.yaml  v0.7   blob 3a93845abcf6efb7214939f8dc2e36d02bb39b65
```

### Review evidence — final delta

**ChatGPT Review A:** `RA-B3-MAJ-01` resolved; `feature.md` v0.2: Clean — Blocker 0, Major 0, Minor 0, Suggestion 0.

**Independent Review B (narrow delta):** `IRB-B3-MAJ-01` resolved; `feature.md` v0.2: Clean; Package 0.2-B3 integration: Clean — Blocker 0, Major 0, Minor 0, Suggestion 0; Consolidation readiness: **Ready**.

**Cả hai finding (`RA-B3-MAJ-01`/`IRB-B3-MAJ-01`) đều đã xử lý trong narrow revision trước đó (v0.1 → v0.2, effective-time cutoff cho eligible-Swing selection). 0 qualifying finding còn lại.**

### Lifecycle transition

```text
Before: Package 0.2-B3 = Draft, review-clean, consolidation-ready
After:  Package 0.2-B3 = Consolidated Stable
```

`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval, KHÔNG phải `status: Approved`, KHÔNG phải Lock, KHÔNG phải Live authorization. `feature.md` giữ nguyên `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`.

### B4 gate effect

Package 0.2-B4 (Context) — baseline dependency đã thỏa, eligible cho Product Owner scope authorization. **Chưa bắt đầu, chưa author, KHÔNG được authorize bởi transaction này.** Package 0.2-B (tổng thể) vẫn chưa hoàn tất cho tới khi B4 hoàn thành.

### Context Map wording concern — deferred, non-blocking

`context-map.yaml` mô tả `feature-engineering` bằng cụm "Feature/Signal" — documentation concern đã ghi nhận tại `feature.md` §20, không phải executable finding, không chặn consolidation. **Không tạo OQ mới. `context-map.yaml` không đổi trong transaction này.**

### Governance boundaries

Không Product Owner Approve; không Lock; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-C vẫn chưa có artifact nào được author.

### Metadata / state

- `feature.md`, `context-map.yaml`, `candle.md`, `swing.md`, `structure.md`, `regime.md`: **không đổi** (bookkeeping-only transaction).
- `README.md` (domain index): **v0.16 → v0.17**, `status` giữ `Draft` — Package 0.2-B3 section chuyển sang `Consolidated Stable` baseline record.
- `MANIFEST.md`: `manifest_version` **9.41 → 9.42**; dòng `domain/` cập nhật ghi nhận Package 0.2-B3 `Consolidated Stable`.

**Package 0.2-B1/B2/B3 nay đều `Consolidated Stable`.** Package 0.2-B4 chưa bắt đầu. Package 0.2-C vẫn chưa có artifact nào được author. OQ-002/OQ-003 vẫn `Open`. Phase 0.2 vẫn active và chưa hoàn tất. Không authorize Live ở bất kỳ hình thức nào.

## [Unreleased] — 2026-07-29 — fix Feature swing effective-time cutoff (Package 0.2-B3 narrow revision)

**Không phải approval, không phải review-complete, không phải Consolidated Stable, không phải re-planning.** Vai trò: `Domain Contract Author · AI Technical Architect`. Narrow revision — xử lý ĐÚNG hai finding, không mở rộng phạm vi Feature, không sửa artifact ngoài phạm vi được cho phép.

### Findings xử lý

`RA-B3-MAJ-01` (ChatGPT Review A) và `IRB-B3-MAJ-01` (Independent Review B) — **cùng một defect, một correction**: eligible-Swing selection cho `distance_to_last_confirmed_swing` (`feature.md` v0.1 §9a) thiếu một **effective-time cutoff filter** độc lập. v0.1 chỉ lọc theo recorded-time visibility (`SwingConfirmed.recorded_time <= cursor`) rồi chạy thẳng total order 8 tiêu chí — điều này cho phép một Swing có `pivot_effective_time.window_start` xảy ra CÙNG LÚC hoặc SAU reference Candle's `effective_time.window_end` bị chọn, chỉ vì nó recorded-time visible sớm hơn cursor. **Recorded-time visible KHÔNG tương đương effective-time eligible** — vi phạm bitemporal correctness ([Chapter 5](constitution/05-time-model.md)), một dạng look-ahead bug.

### Canonical effective-time cutoff decision (pin đúng một lần, §6)

```text
reference_cutoff = reference Candle effective_time.window_end
eligible_swing_effective_cutoff_policy = REFERENCE_CANDLE_WINDOW_END_EXCLUSIVE
điều kiện: SwingConfirmed.pivot_effective_time.window_start < reference_cutoff   (strict "<", half-open)
```

Một Swing có pivot bắt đầu ĐÚNG bằng `window_end` KHÔNG eligible. KHÔNG dùng: batch completion time; wall clock hiện tại; Swing recorded mới nhất bất kể effective time; cutoff tự chọn ở implementation; `FeatureCurrentView`'s time.

### Feature Definition changes (§6, §7.3)

Thêm field bắt buộc mới `eligible_swing_effective_cutoff_policy` (enum, v0.2 đúng một giá trị hợp lệ `REFERENCE_CANDLE_WINDOW_END_EXCLUSIVE`), pin canonical value trong khối "Giá trị canonical mặc định" cùng ba policy identifier hiện có (nay bốn). `effective_window_policy` clarify: với `distance_to_last_confirmed_swing`, PHẢI dùng CHÍNH reference Candle làm mốc — effective_window của Feature fact KHÔNG vượt quá effective_window của Candle đó; Eligible Swing được chọn PHẢI effective strictly trước window_end này.

### Eligible-Swing algorithm changes (§9a — structural rewrite)

Tách Eligible-Swing selection thành **hai giai đoạn tường minh, không được gộp**: (1) ordered filter pipeline 5 bước (AND) quyết định tập ứng viên; (2) total order 8 tiêu chí (không đổi so với v0.1) chỉ tie-break TRONG tập đã qua (1). **Effective-time eligibility LÀ MỘT FILTER chạy TRƯỚC candidate ordering** — total order không bao giờ hợp thức hóa một Swing ineligible về effective time, kể cả khi Swing đó thắng theo tiêu chí 1 (`pivot_effective_time.window_start DESC`).

```text
1. Identity/scope match (instrument_id, venue_id, timeframe, swing_definition_version, swing_direction)
2. Recorded-time visibility: S.recorded_time <= R
3. Effective-time cutoff (MỚI): S.pivot_effective_time.window_start < C.effective_time.window_end
4. Latest valid revision của swing_id tại R
5. Not invalidated: không có SwingInvalidated visible cho đúng (swing_id, swing_revision) tại R
```

**Ví dụ bắt buộc, embedded normative (đóng finding):** reference Candle `effective_time.window_end = T10`; Swing A `pivot_effective_time.window_start = T8`, `recorded_time = R20`; Swing B `pivot_effective_time.window_start = T15`, `recorded_time = R30`; historical batch cursor `R100`. Kết quả bắt buộc: **Swing A eligible; Swing B rejected** (`T15 >= T10`) — dù CẢ HAI đều recorded-time visible tại `R100`.

**Correction-recorded-old-pivot clarification:** "recorded muộn hơn không có nghĩa effective muộn hơn" — một Swing revision recorded SAU (correction) vẫn eligible nếu chính revision đó thỏa cả 5 bước, cụ thể pivot của nó vẫn `< reference_cutoff`. Ngược lại một correction dời pivot tới `>= cutoff` khiến Swing chuyển từ eligible sang ineligible, bất kể `recorded_time` của correction là gì — bảo toàn bitemporal correctness.

### Time-semantics changes (§12)

Strengthen: mọi Feature input PHẢI thỏa CẢ HAI điều kiện độc lập — `(a) input.recorded_time <= computation cursor` VÀ `(b) input effective time thỏa cutoff riêng của feature_type đó (pin tại §6)`. `(a)` một mình KHÔNG đủ. Quy tắc chung "không có input nào vượt quá `effective_window.window_end`" nay tham chiếu tường minh đúng cutoff cụ thể của từng feature_type (§6/§9a cho `distance_to_last_confirmed_swing`) thay vì đứng riêng mơ hồ.

### No-repaint/parity changes (§13)

Thêm bảo đảm tường minh: historical Backtest/Replay tại cursor muộn PHẢI reconstruct mỗi Feature fact chỉ dùng input recorded-time visible VÀ effective-time eligible tại đúng computation cursor của CHÍNH fact đó — một Swing recorded-time visible trong batch KHÔNG BAO GIỜ được "nhảy vào" một computation point sớm hơn mà nó effective-time ineligible. Bảo đảm độc lập mode — Live/Paper/Replay/Backtest PHẢI cho cùng tập Eligible Swing tại cùng computation point.

### Attack-scenario results — 16/16 pass

Reference Candle T10/Swing A T8/Swing B T15/cursor R100 (A eligible, B rejected); pivot đúng bằng T10 (rejected, strict `<`); pivot ngay trước T10 (eligible); correction recorded muộn hơn với pivot T8 (eligible); correction recorded muộn hơn với pivot T15 (rejected); revision được chọn bị invalidate (loại, bước 5); replacement revision valid và trước cutoff (eligible); replacement revision valid nhưng sau cutoff (không eligible qua swing_id đó); HIGH/LOW direction mismatch (loại, bước 1); sai `swing_definition_version` (loại, bước 1); cùng pivot effective time xuyên nhiều stream (total order tie-break không đổi); không có Eligible Swing nào (valid absence, không đổi); historical Backtest vs Live parity (§13, cùng tập Eligible Swing mọi mode); không regression input normalization (§8a không đổi); không regression correction lineage (§9 10-invariant không đổi); không regression Current View (§11 không đổi).

### Preserved semantics — không đổi

Đúng ba founding feature type; subject identity năm field; Candle/Regime dual-path rule (§7.1/§7.2); correction lineage 10 invariant (§9); input normalization (§8a); `FeatureCurrentView` semantics + no-row (§5); Current View total order 7 tiêu chí (§11); Feature-to-Feature dependency deferred (§10); Context boundary (§15); Context Map relationships; không ADR mới; OQ-002/OQ-003 state không đổi.

### Context Map wording concern — deferred, non-blocking

`context-map.yaml` mô tả `feature-engineering` bằng cụm "Feature/Signal" — có thể gây hiểu lầm cạnh định nghĩa "Feature KHÔNG phải trade signal" ở đầu `feature.md`. **KHÔNG phải executable finding của revision này** — `context-map.yaml` KHÔNG nằm trong phạm vi file được sửa. Ghi nhận documentation-only tại `feature.md` §20 (Open questions), hoãn cho lần cập nhật `context-map.yaml` kế tiếp. **`context-map.yaml` giữ nguyên byte-for-byte, không có diff trong commit này.**

### Self-review checklist — 10/10 pass

Later-effective Swing bị reject; recorded-time-visible nhưng effective-ineligible Swing bị reject; old-effective corrected revision được accept; cutoff boundary dùng `<` strict (không `<=`); total order chỉ chạy sau effective filter; `effective_window_policy` và cutoff policy nhất quán; không look-ahead trong historical batch; Live/Backtest/Replay/Paper parity giữ nguyên; không sửa semantic ngoài phạm vi finding; `context-map.yaml` không đổi.

### Metadata / state

- `feature.md`: **v0.1 → v0.2**, `status` giữ `Draft`.
- `README.md` (domain index): **v0.15 → v0.16**, `status` giữ `Draft` — Package 0.2-B row + mục Package 0.2-B3 cập nhật ghi nhận revision.
- `MANIFEST.md`: `manifest_version` **9.40 → 9.41**; dòng `domain/` cập nhật ghi nhận `feature.md` v0.2, `RA-B3-MAJ-01`/`IRB-B3-MAJ-01` resolved.
- `context-map.yaml`, `candle.md`, `swing.md`, `structure.md`, `regime.md`, `ADR-012.md`, `ADR-013.md`: **không đổi.**

**Sẵn sàng chuyển ChatGPT Review A (trên `feature.md` v0.2).** Không Product Owner Approve; không Lock; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-B1/B2 vẫn `Consolidated Stable`; Package 0.2-B3 vẫn active, Draft, chưa `Consolidated Stable` (đã qua narrow revision trước Review A/B); Package 0.2-B4 chưa bắt đầu; Package 0.2-C vẫn chưa có artifact nào được author; Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-29 — author minimal Feature contract (Package 0.2-B3)

**Không phải approval, không phải review-complete, không phải Consolidated Stable.** Vai trò: `Domain Contract Author · AI Technical Architect`. Authorization gate: Product Owner xác nhận tường minh "Authorize Package 0.2-B3 minimal Feature scope." trước khi authoring bắt đầu.

### Phạm vi authoring — scope tối thiểu, không mở rộng framework

`docs/domain/feature.md` (mới, v0.1) — điểm fan-in có kiểm soát `Candle/Swing/Raw Regime → Feature`, đúng [ADR-003](adr/ADR-003.md). Đúng **ba founding feature type**: `volatility_metric`, `directional_persistence_metric`, `distance_to_last_confirmed_swing`. Không author `context.md` (B4) hay bất kỳ Package 0.2-C artifact.

### Quyết định thiết kế chính

- **Subject identity — năm field, giống `regime.md`:** `feature_subject_id` deterministic từ `(instrument_id, venue_id, timeframe, feature_type, feature_definition_version)`. Tham số riêng của một feature type (ví dụ `swing_direction` cho `distance_to_last_confirmed_swing`) PIN trong Feature Definition, KHÔNG mở rộng subject identity — vì `feature_definition_version` bất biến, hai tham số khác nhau tự động là hai definition version khác nhau, tự động là hai subject khác nhau.
- **Dual-path upstream cho `volatility_metric`/`directional_persistence_metric`:** mỗi `feature_definition_version` PIN đúng MỘT `upstream_source` (`candle` hoặc `regime`) — cấm hai path ambiguous cho cùng một definition version.
- **`distance_to_last_confirmed_swing` KHÔNG tiêu thụ Structure event** — chỉ tái sử dụng **methodology** total-order của `structure.md` §6a (8 tiêu chí lexicographic) cho Eligible Swing selection, KHÔNG tiêu thụ `BreakOfStructureDetected`/`ChangeOfCharacterDetected`/`StructureFactInvalidated`/`StructureRecomputed`, và KHÔNG loại trừ Swing "đã dùng làm broken_swing_ref" (khác Structure — Feature không "tiêu thụ" Swing theo nghĩa break level, chỉ đo khoảng cách). Feature pin policy identifier riêng, độc lập registry nội bộ của Structure.
- **Hai event type, không ba** — `FeatureComputed` (original + correction replacement qua `supersedes_fact_ref`) + `FeatureFactInvalidated`, đúng bài học `regime.md`: không cần một `FeatureRecomputed` riêng vì các computation point độc lập nhau (không chain như Structure).
- **Feature-to-Feature dependency deferred tường minh (§10)** — không FeatureComputed nào tiêu thụ FeatureComputed khác ở B3; cả ba founding feature type tính trực tiếp từ authoritative upstream domain fact.
- **Áp dụng ngay từ v0.1 mọi bài học đã trả giá ở `structure.md`/`regime.md`:** envelope binding cho `FeatureFactInvalidated` (`subject_ref`/`effective_time` kế thừa từ fact bị invalidate, không tự khai báo độc lập); canonical input evidence normalization tổng quát hóa cho input đa dạng loại event (không giả định tất cả input đều là Candle như `regime.md` §8a); `FeatureCurrentView` no-row semantics trước fact đầu tiên, `view_state` chỉ có `VALID`/`PENDING_CORRECTION`; mọi canonical policy identifier khai báo ĐÚNG MỘT NƠI.

### Self-review — 27 attack scenario, 1 gap phát hiện và xử lý

Chạy đủ 27 scenario theo yêu cầu authoring task. **26/27 covered đúng bởi thiết kế ban đầu.** Phát hiện **một gap** trước khi commit: ba canonical policy identifier (`input_normalization_policy`, `current_view_selection_policy`, `eligible_swing_selection_policy`) được mô tả như schema field placeholder ("canonical identifier") nhưng KHÔNG có giá trị literal cụ thể nào được pin — không nhất quán với tiền lệ `swing.md`/`structure.md`/`regime.md` (cả ba đều pin một chuỗi cụ thể). **Sửa:** thêm khối "Giá trị canonical mặc định (v0.1)" tại §6, pin ba chuỗi cụ thể — mỗi chuỗi khai báo ĐÚNG MỘT LẦN, các nơi khác chỉ tham chiếu theo tên field (đóng trước lớp lỗi IRB-B2-MIN-01-style ngay từ v0.1, thay vì phải sửa ở một vòng revision sau).

### Attack scenario khác đã pass không cần sửa

Value-equality không phải duplicate (ví dụ `W1→0.025, W2→0.025` vẫn hai fact); correction lineage 10 invariant đầy đủ; envelope binding sai subject/window đều bị từ chối; cross-stream sequence không bao giờ so trực tiếp; Eligible Swing "không có" → valid absence; Current View "latest pending, older valid" không fallback; Backtest/Replay/Paper/Live cùng ancestry; không tiêu thụ bất kỳ `*-current-view` nào; không author Context/Strategy conclusion.

### Context Map changes

`context-map.yaml` v0.6 → v0.7 — thuần túy additive: `feature-engineering.owned_contracts` forward-declared → authored; 6 relationship mới (`candle-closed`/`candle-corrected` từ `market-data-observation`; `swing-confirmed`/`swing-invalidated` từ `market-structure-analysis`; `regime-classified`/`regime-fact-invalidated` từ `raw-regime-analysis`, tất cả → `feature-engineering`) — đúng những gì ba founding feature type thực sự tiêu thụ, không hơn. **Không đổi** bất kỳ relationship hiện có nào. Không thêm Context/Strategy/Decision/Risk relationship.

### Backward Consistency Check

No conflict với Constitution Chapters 2–10, ADR-003 (trực tiếp controlling, thỏa mãn đầy đủ), ADR-007 (venue-neutrality), ADR-009 (tái sử dụng causal precedence/ordering hiện có), ADR-010 (không áp dụng — Feature không phải Decision event), `candle.md`/`swing.md`/`structure.md`/`regime.md` (không sửa semantic, chỉ tiêu thụ contract đã tồn tại), `context-map.yaml` (chỉ additive). **Không cần ADR mới.**

### Metadata / state

- `feature.md`: **mới, v0.1**, `status: Draft`.
- `context-map.yaml`: **v0.6 → v0.7**, `status` giữ `Draft`.
- `README.md` (domain index): **v0.14 → v0.15**, `status` giữ `Draft` — Package 0.2-B row + mục Package 0.2-B3 mới.
- `MANIFEST.md`: `manifest_version` **9.39 → 9.40**; dòng `domain/` cập nhật ghi nhận B3 Draft, review-chưa-diễn-ra.
- `candle.md`, `swing.md`, `structure.md`, `regime.md`, `ADR-012.md`, `ADR-013.md`: **không đổi.**

**Sẵn sàng chuyển ChatGPT Review A.** Không Product Owner Approve; không Lock; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-B1/B2 vẫn `Consolidated Stable`; Package 0.2-B3 active, Draft, chưa `Consolidated Stable`; Package 0.2-B4 chưa bắt đầu; Package 0.2-C vẫn chưa có artifact nào được author; Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-29 — consolidate Package 0.2-B2 stable baseline

**Không phải approval, không phải Lock.** Vai trò: `Domain Package Consolidation Author · AI Technical Architect`. Transaction này **ghi nhận** kết quả review đã hoàn tất — không sửa semantic của `regime.md`.

### Exact baseline

Reviewed HEAD: `78479ab088b1a32c580c9a729a53333896b952b3` (parent: authoring B2 `32aadc9cc075ce272b2c85bef8836c77417a5566` → narrow revision `78479ab088b1a32c580c9a729a53333896b952b3`).

### Package scope

`regime.md` — Raw Regime, hai dimension: **Volatility**, **Directional Persistence**. Độc lập hoàn toàn Structure ([ADR-003](adr/ADR-003.md)).

### Final artifact blobs

```text
regime.md         v0.2   blob edd1584377f1db84269e7b1dfdd4926d0ce01c70
context-map.yaml  v0.6   blob 5447f91435b5ffdc01424988f29e0d9d5ad76f99  (không đổi)
```

Dependency không đổi trong suốt B2: `candle.md` v0.4, `swing.md` v0.2, `structure.md` v0.4.

### ChatGPT Review A — final

`regime.md` v0.2: **Clean** — Blocker 0, Major 0, Minor 0.

### Independent Review B — narrow delta, final

`IRB-B2-MAJ-01` resolved, `IRB-B2-MAJ-02` resolved, `IRB-B2-MIN-03` resolved. Blocker 0, Major 0, Minor 0, Suggestion 0. `regime.md` v0.2: Clean. Package 0.2-B2 integration: Clean. **Package 0.2-B2: consolidation-ready.**

### Zero qualifying findings

Cả hai track (ChatGPT Review A, Independent Review B) đều Clean, 0 finding chưa xử lý.

### Package lifecycle transition

```text
Trước: Package 0.2-B2 = Draft, review-clean, consolidation-ready
Sau:   Package 0.2-B2 = Consolidated Stable
```

`Consolidated Stable` là package lifecycle/readiness state — **KHÔNG** phải document approval, **KHÔNG** phải `Approved`, **KHÔNG** phải Lock, **KHÔNG** phải Live authorization. `regime.md` giữ nguyên `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`.

### Package 0.2-B3 gate effect

Baseline dependency (B2 Consolidated Stable) đã thỏa — Package 0.2-B3 (`feature.md`) trở nên **eligible cho Product Owner scope authorization và planning**. Transaction này **không** tự author hay tự authorize B3. Package 0.2-B4 (`context.md`) tương tự chưa bắt đầu.

### Governance boundaries

Không Product Owner Approve; không Lock; không đóng OQ-002/OQ-003 (vẫn `Open`); không authorize Live. Package 0.2-B3/B4 chưa bắt đầu. Package 0.2-C vẫn chưa có artifact nào được author. Phase 0.2 vẫn active và chưa hoàn tất.

### Metadata / state

- `regime.md`, `context-map.yaml`, `swing.md`, `structure.md`, `candle.md`, `ADR-012.md`, `ADR-013.md`: **không đổi** — không nằm trong scope commit này.
- `README.md` (domain index): **v0.13 → v0.14**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.38 → 9.39**; dòng `domain/` cập nhật ghi nhận Package 0.2-B2 `Consolidated Stable` + exact blob pin.

## [Unreleased] — 2026-07-29 — resolve Raw Regime review findings (narrow revision)

**Không phải approval, không phải review-complete, không phải Consolidated Stable.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Narrow revision — không planning lại, không mở rộng scope Raw Regime, chỉ xử lý đúng bốn finding từ ChatGPT Review A + Independent Review B trên baseline v0.1.

### Findings resolved (chỉ `regime.md`, v0.1 → v0.2)

- **`RA-B2-MIN-01` + `IRB-B2-MIN-03` (cùng một ambiguity, một correction):** mâu thuẫn giữa "no row while UNCLASSIFIED" (§5) và "view_state = UNAVAILABLE khi chưa có completed valid window" (§11 cũ) — không rõ trước fact đầu tiên là "row không tồn tại" hay "row tồn tại với state UNAVAILABLE". Quyết định canonical: **trước `RegimeClassified` đầu tiên → không có row nào tồn tại** (`GetCurrentRegime` trả `NOT_FOUND`/`ABSENT` theo quy ước tầng query, không materialize placeholder). `view_state` rút còn đúng hai giá trị — `VALID`, `PENDING_CORRECTION` — loại bỏ hoàn toàn `UNAVAILABLE` khỏi schema/invariants/thuật toán/prose (§5, §11). Thêm Bước 0 (row existence precondition) vào thuật toán selection.
- **`IRB-B2-MAJ-01` — Canonical Candle evidence normalization:** `candle_evidence_refs` trước đây là array không normalize — cùng tập evidence, khác thứ tự đến, có thể sinh hai computation identity khác nhau. Thêm §8a: `candle_evidence_refs` là tập toán học, unique, đúng `window_candle_count` phần tử, normalize theo 6-tiêu-chí lexicographic order (`window_start ASC → window_end ASC → stream_id ASC → registry_version ASC → sequence ASC (chỉ khi stream_id+registry_version hòa) → event_id ASC`) TRƯỚC khi tính identity/hash/so sánh/dedup/serialize. `candle_evidence_refs` field trong payload PHẢI serialize theo đúng normalized order này (§3 invariant mới). Computation identity (§8b) dùng normalized list.
- **`IRB-B2-MAJ-02` — Invalidation envelope binding:** `RegimeFactInvalidated.invalidated_fact_ref` có thể trỏ một fact nhưng envelope (`subject_ref`/`effective_time`) khai báo subject/window khác — không có ràng buộc nào ngăn "nhắm nhầm". Thêm invariant bắt buộc: `envelope.subject_ref` PHẢI BẰNG HỆT `subject_ref` của fact bị invalidate (toàn bộ scope, không chỉ `subject_id`); `envelope.effective_time` PHẢI BẰNG HỆT `analysis_window` của fact bị invalidate — cả hai KẾ THỪA, không tự khai báo độc lập (§2, §4). Cấm tường minh: sai subject, sai window, sai `regime_definition_version` (= khác subject), sai `regime_dimension` (= khác subject).

### Self-review — 20 scenario + 1 defect bổ sung tự phát hiện

Chạy đủ 20 scenario theo yêu cầu revision task (evidence normalization theo cả hai chiều thứ tự, duplicate ref, cross-stream sequence, invalidation đúng/sai subject/window/dimension/definition-version, no-row → VALID → PENDING_CORRECTION → replacement visible, replay trước/sau revision event). **20/20 pass.**

**Phát hiện thêm một defect ngoài phạm vi 4 finding đã cho, tự sửa trước commit:** hai canonical policy identifier (`candle_evidence_normalization_policy`, `current_view_selection_policy`) bị khai báo **lặp lại hai lần** trong tài liệu — một lần tại §6 (Regime Definition, nguồn canonical) và một lần tại chính §8a/§11 (nơi thuật toán được mô tả) — đúng anti-pattern mà `structure.md`'s `IRB-FD-STR-MIN-01` đã dạy phải tránh (một canonical string chỉ tồn tại ĐÚNG MỘT NƠI). **Sửa:** §8a và §11 nay chỉ tham chiếu §6 theo tên field, không lặp lại chuỗi — đúng MỘT bản canonical cho mỗi identifier, xuyên suốt tài liệu.

**Nhân tiện sửa 4 cross-reference lỗi tiền tồn từ v0.1** (không thuộc 4 finding chính thức, nhưng phát hiện trong lúc revision khu vực liên quan): bốn chỗ trong §1/§4/§5 tham chiếu "§10" khi ý định thực sự là "§11" (`RegimeCurrentView` — validity rules và total order). §10 của tài liệu là Correction Lineage, §11 là `RegimeCurrentView` — bốn cross-reference đó viết nhầm §10 khi đang nói về §11. Sửa cả bốn về đúng §11.

### Preserved semantics — không đổi

Raw Regime độc lập Structure; five-field subject identity; one subject per dimension; per-window classification frequency; Volatility + Directional Persistence scope; hai event type (`RegimeClassified`/`RegimeFactInvalidated`, không `RegimeRecomputed`); correction lineage model (10 invariant); total order cho `RegimeCurrentView` (7 tiêu chí, không đổi thứ tự/hướng); Candle-only authoritative input; Feature/Context boundary; context-map relationships; không ADR mới; không đổi OQ nào.

### Metadata / state

- `regime.md`: **v0.1 → v0.2**, `status` giữ `Draft`.
- `context-map.yaml`, `swing.md`, `structure.md`, `candle.md`, `ADR-012.md`, `ADR-013.md`: **không đổi** — không nằm trong scope commit này.
- `README.md` (domain index): **v0.12 → v0.13**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.37 → 9.38**; dòng `domain/` cập nhật ghi nhận revision + review readiness.

**Sẵn sàng cho ChatGPT Review A và Independent Review B re-review (chỉ `regime.md` v0.2).** Không Product Owner Approve; không Lock; không Consolidated Stable; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-B1 vẫn `Consolidated Stable`; Package 0.2-B2 active, Draft, chưa `Consolidated Stable`; Package 0.2-B3/B4 chưa bắt đầu; Package 0.2-C vẫn chưa có artifact nào được author; Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-29 — author Raw Regime contract (Package 0.2-B2)

**Không phải approval, không phải review-complete, không phải Consolidated Stable.** Vai trò: `Domain Contract Author · AI Technical Architect`. Author trực tiếp `regime.md` v0.1 Draft theo scope đã Product Owner chấp thuận qua hai vòng planning (analysis-only, không commit, không sửa GitHub).

### Phạm vi authoring

`docs/domain/regime.md` (mới, v0.1) — bắt đầu chuỗi `Candle → Raw Regime → Feature`, độc lập hoàn toàn với `Candle → Swing → Structure` ([ADR-003](adr/ADR-003.md), Approved). Hai dimension: **Volatility**, **Directional Persistence**. Không author `feature.md`/`context.md` (B3/B4) hay bất kỳ Package 0.2-C artifact.

### Quyết định thiết kế chính

- **Subject identity — năm field, không gồm window:** `regime_subject_id` deterministic từ `(instrument_id, venue_id, timeframe, regime_dimension, regime_definition_version)`. Analysis window là thuộc tính của TỪNG fact, không phải trục identity — sửa đúng lỗi đếm nhầm "4-field" ở vòng planning đầu (nội dung field set đã đúng, chỉ nhãn số đếm sai).
- **Classification frequency — một fact cho MỌI completed valid window, không suppress theo class:** đảo ngược quyết định ban đầu của Round 1 planning ("same class → no event"); `RegimeClassified` phát sinh cho mọi window hoàn chỉnh hợp lệ kể cả class trùng window liền trước — bảo toàn evidence đầy đủ, correction targeting chính xác, và visibility đúng cursor cho Feature/Replay.
- **Hai event type, không ba:** `RegimeClassified` (dùng cho CẢ original computation lẫn correction replacement, phân biệt qua `supersedes_fact_ref`) + `RegimeFactInvalidated`. **Không** có `RegimeRecomputed` riêng như `structure.md` — so sánh tường minh trong tài liệu: Structure cần `RegimeRecomputed`-tương-đương vì các fact CHAIN vào nhau qua `prior_orientation`; Regime's per-window fact hoàn toàn độc lập (không có chain tương tự), nên một correction chỉ cần thay thế đúng fact của window bị ảnh hưởng — cùng pattern `CandleCorrected` của chính `candle.md`, không phải pattern cascade của `structure.md`.
- **Correction lineage — 10 invariant tường minh** (nguyên bản/replacement, không nhảy cóc, không fork, không "sống lại" trước invalidation, append-only, không tái sử dụng ngầm) — pin tại `supersedes_fact_ref` trên `RegimeClassified`.
- **Overlapping-window correction — độc lập, không cascade:** một `CandleCorrected` ảnh hưởng nhiều window chỉ cần invalidate+replace TỪNG window độc lập — không cần dependency-forward traversal như `structure.md` §10, vì các window không phụ thuộc lẫn nhau.
- **Current View total order — 7 tiêu chí, lexicographic nghiêm ngặt ngay từ v0.1** (`window_end DESC → window_start DESC → recorded_time ASC → stream_id ASC → registry_version ASC → sequence ASC (chỉ khi stream_id+registry_version hòa) → event_id ASC`) — áp dụng ngay bài học từ `structure.md`'s IRB-FD-STR-MAJ-01 (không lặp lại wording mâu thuẫn "bỏ qua tiêu chí, nhảy tới tiêu chí khác").
- **`directional_persistence` không mã hóa Bullish/Bearish** — tường minh phân biệt khỏi `structure.md`'s `current_orientation`: đo lường thống kê liên tục, độc lập hoàn toàn Swing/Structure, được phép mâu thuẫn với Structure tại cùng thời điểm.
- **Không `classification_origin` enum riêng** — invariant trên `supersedes_fact_ref` (có mặt/vắng mặt) đã đủ executable, tránh field dư thừa.
- **Không `invalidation_cause` enum trên `RegimeFactInvalidated`** — Regime chỉ có đúng MỘT nguyên nhân invalidation (CandleCorrected, không có Swing/Structure/chained như `structure.md`), nên enum một-giá-trị là dư thừa.

### Self-review — 25 attack scenario, 2 defect phát hiện và xử lý

Chạy đủ 25 scenario theo yêu cầu authoring task. **23/25 covered đúng bởi thiết kế ban đầu.** Phát hiện **hai defect thực sự** trước khi commit:

1. **Copy-paste leftover:** bảng total order §11 sót một dòng tham chiếu `SwingConfirmed` (leftover từ soạn thảo) thay vì `RegimeClassified.event_id` — sửa ngay.
2. **Lỗi thuật toán Current View selection (attack scenario "latest window pending while previous window remains valid"):** thiết kế ban đầu xác định "window hiệu lực mới nhất" SAU KHI đã loại trừ fact invalidate — nếu window mới nhất đang chờ correction, thuật toán sẽ âm thầm lùi về báo cáo một window CŨ HƠN như thể đang "hiện tại", che giấu việc window mới nhất đang pending. **Sửa:** xác định target window (theo `window_end` lớn nhất) TRƯỚC khi loại trừ, sau đó mới resolve trạng thái của ĐÚNG target window đó (VALID / PENDING_CORRECTION / UNAVAILABLE) — không bao giờ fallback về window cũ hơn chỉ vì window mới nhất đang pending.
3. **Thiếu tường minh "no shortcut khi class không đổi" (attack scenario 14):** thêm câu tường minh tại §10 — correction PHẢI luôn phát `RegimeFactInvalidated` + replacement, kể cả khi `computed_metric`/`class` cuối cùng không đổi, để bảo toàn evidence honesty (I-1).

Cả ba thay đổi được áp dụng **trước** commit, phản ánh trực tiếp trong `regime.md` v0.1 (không phải revision riêng).

### Attack scenario khác đã pass không cần sửa

Independent-dimension isolation trên cùng window; warm-up/gap valid absence; dedup trên literal duplicate (không trên class trùng); lineage rule 1-10 đầy đủ (original/replacement/no-skip/no-fork/no-early-visibility/append-only/no-silent-reuse); cross-stream total order (khác stream_id/registry_version/sequence từng tiêu chí một, không so sequence xuyên stream); definition-version-change tạo subject mới; Backtest historical sequential computation; không Structure/Swing dependency; RegimeCurrentView không tự tham chiếu làm authoritative input.

### Metadata / state

- `regime.md`: **mới, v0.1**, `status: Draft`.
- `context-map.yaml`: **v0.5 → v0.6**, `status` giữ `Draft` — `raw-regime-analysis.owned_contracts` chuyển forward-declared → authored; không relationship nào thay đổi (Candle→Raw Regime relationships đã đăng ký sẵn từ Package 0.2-A).
- `README.md` (domain index): **v0.11 → v0.12**, `status` giữ `Draft` — Package 0.2-B row + mục Package 0.2-B2 mới.
- `MANIFEST.md`: `manifest_version` **9.36 → 9.37**; dòng `domain/` cập nhật ghi nhận B2 Draft, review-chưa-diễn-ra.
- `swing.md`, `structure.md`, `candle.md`, `ADR-012.md`, `ADR-013.md`: **không đổi.**

**Sẵn sàng chuyển ChatGPT Review A.** Không Product Owner Approve; không Lock; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-B1 vẫn `Consolidated Stable`; Package 0.2-B2 active, Draft, chưa `Consolidated Stable`; Package 0.2-B3/B4 chưa bắt đầu; Package 0.2-C vẫn chưa có artifact nào được author; Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-29 — consolidate Package 0.2-B1 stable baseline

**Không phải approval, không phải Lock.** Vai trò: `Domain Package Consolidation Author · AI Technical Architect`. Transaction này **ghi nhận** kết quả review đã hoàn tất — không sửa semantic của `swing.md`, `structure.md`, hay `context-map.yaml`.

### Exact baseline

Reviewed HEAD: `d6545de3fcc767e03f74fd0712ada792372d1c33`. Lịch sử parent đầy đủ: authoring B1 (`5d46bacc8beafb4ba7087347f0af7c5b10e6e4d0`) → consolidated revision (`3813c600129efe0a6676c1cd0301913f6d2fc3e8`) → revision-qualified Structure reference (`7c789b6dbb395832e87f9b11fdce3da4997000a6`) → final ordering correction (`d6545de3fcc767e03f74fd0712ada792372d1c33`).

### Package scope

`swing.md` (Swing pivot/confirmation/invalidation, revision lifecycle §1a); `structure.md` (BOS/CHoCH, `StructureFactInvalidated`/`StructureRecomputed`, Eligible Swing total order §6a, dependency-forward cascade §10); `context-map.yaml` integration (`market-structure-analysis` context registration, Candle relationships — không self-edge Swing→Structure).

### Final artifact versions/blobs

```text
swing.md         v0.2   blob 5bbe666ff404209876a721b1e01cb9ac62011062
structure.md     v0.4   blob 78964dfb6852bbac3fa1e034d64b4fc8031c3fef
context-map.yaml v0.5   blob 0d87744e2a1ffdd592b05bdfbb0ef5dab85b5920
```

### ChatGPT Review A — kết quả đầy đủ 4 vòng

| Vòng | Baseline | Swing | Structure | Context Map | Package B1 |
|---|---|---|---|---|---|
| Initial | `5d46bacc8b...` | Revision required | Revision required | Clean | Revision required |
| Delta | `3813c60012...` | v0.2 Clean với minor correction | v0.2 Revision required | v0.5 Clean | — |
| Final delta | `7c789b6dbb...` | v0.2 Clean | v0.3 Clean | v0.5 Clean | — |
| **Final re-review** | `d6545de3fc...` | v0.2 Clean | v0.4 Clean | v0.5 Clean | **Clean, 0 finding** |

### Independent Review B — kết quả đầy đủ 4 vòng

| Vòng | Baseline | Swing | Structure | Context Map | Package B1 |
|---|---|---|---|---|---|
| Initial | `5d46bacc8b...` | Revision required | Revision required | Clean với 1 minor documentation correction | Revision required |
| Delta | `3813c60012...` | v0.2 Clean | v0.2 Revision required | v0.5 Clean | — |
| Final delta | `7c789b6dbb...` | v0.2 Clean | v0.3 Revision required | v0.5 Clean | — |
| **Final re-review** | `d6545de3fc...` | v0.2 Clean | v0.4 Clean | v0.5 Clean | **Package integration Clean, consolidation-ready** |

### Unresolved qualifying findings và backward consistency

**0 qualifying finding chưa xử lý** (cả hai track, vòng final re-review). **Backward Consistency Check: `No conflict`** (Independent Review B final re-review).

### Package lifecycle transition

```text
Trước: Draft candidate, review-complete (chờ final re-review)
Sau:   Package 0.2-B1 = Consolidated Stable
```

`Consolidated Stable` là package lifecycle/readiness state — **KHÔNG** phải document approval status, đúng định nghĩa đã khóa tại consolidation Package 0.2-A. Điều kiện đủ: authoring hoàn tất; ChatGPT Review A hoàn tất; Independent Review B hoàn tất; 0 qualifying finding; exact reviewed artifact đã pin; package đủ ổn định cho package kế tiếp (B2) planning — không ngụ ý Product Owner Approval, không ngụ ý Lock.

### Governance boundaries

- `swing.md`, `structure.md`, `context-map.yaml`: **`status: Draft`, `approved_by: null`, `approved_at: null` — không đổi.**
- Không Product Owner Approve; không Lock; không đóng OQ-002/OQ-003 (vẫn `Open`); không authorize Live.
- **Package 0.2-B2 chưa bắt đầu** — baseline dependency (B1 Consolidated Stable) đã thỏa, B2 trở nên eligible cho Product Owner scope authorization, nhưng authoring thực tế là một action riêng, chưa xảy ra trong transaction này.
- Package 0.2-B3/B4: chưa bắt đầu. Package 0.2-C: gate open (ADR-012/013 Approved), vẫn chưa có artifact nào được author.
- Phase 0.2 vẫn **active và chưa hoàn tất**.

### Metadata / state

- `swing.md`, `structure.md`, `context-map.yaml`, `candle.md`, `ADR-012.md`, `ADR-013.md`: **không đổi** — không nằm trong scope commit này.
- `README.md` (domain index): **v0.10 → v0.11**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.35 → 9.36**; dòng `domain/` cập nhật ghi nhận Package 0.2-B1 `Consolidated Stable` + exact blob pin.

## [Unreleased] — 2026-07-29 — final narrow correction: clarify Structure stream ordering

**Không phải approval, không phải Consolidate Stable.** Vai trò: `Domain Contract Final Delta Revision Author · AI Technical Architect`. Revision này chỉ xử lý 2 finding cuối — `IRB-FD-STR-MAJ-01`, `IRB-FD-STR-MIN-01` — trên `structure.md` v0.3, phát hiện bởi Independent Review B final delta. `structure.md` `status: Draft`.

### Findings resolved (chỉ `structure.md`, v0.3 → v0.4)

- **IRB-FD-STR-MAJ-01 — Loại bỏ mâu thuẫn comparator:** §6a v0.3 khai đúng lexicographic tuple ("dừng ở tiêu chí đầu tiên phân biệt được") nhưng một câu riêng lại nói: khi tiêu chí 3 hoặc 4 khác nhau, tiêu chí 5 "không so sánh được và bị BỎ QUA, chuyển thẳng sang (6)" — mâu thuẫn trực tiếp với chính rule đã khai (nếu 3/4 đã phân biệt được, so sánh phải DỪNG ở đó, không "nhảy" tới 6). Thay bằng thuật toán chuẩn tường minh:
  ```text
  So sánh tiêu chí 1 đến 8 theo đúng thứ tự.
  Tiêu chí ĐẦU TIÊN có giá trị khác nhau quyết định ứng viên thắng.
  Các tiêu chí sau đó KHÔNG được đánh giá.
  ```
  Cộng ba nhánh tường minh (tiêu chí 3 khác → dừng tại 3; tiêu chí 3 hòa nhưng 4 khác → dừng tại 4; chỉ khi cả 3 VÀ 4 hòa thì 5 mới được đánh giá) và ba ví dụ minh họa cụ thể (khác `stream_id`; cùng `stream_id` khác `registry_version`; cùng stream identity khác `sequence`) — đúng theo yêu cầu. Prohibition "không so `sequence` thô xuyên stream" được giữ nguyên và làm rõ: chính việc dừng lại ở tiêu chí 3/4 (thay vì "nhảy" tới 5) là cơ chế thực thi prohibition đó — không làm suy yếu vai trò ordering của tiêu chí 3/4.
- **IRB-FD-STR-MIN-01 — Một canonical policy identifier duy nhất:** §9 còn sót comment tham chiếu identifier lỗi thời của 4-tier order v0.2 (`pivot_effective_time_desc_then_recorded_time_then_stream_then_swing_id`) dù §6a đã có identifier 8-tiêu-chí đúng từ v0.3. Xóa identifier lặp lại ở §9; §9 nay chỉ tham chiếu **normative** tới §6a theo tên field — không còn hai bản chuỗi có thể lệch nhau theo thời gian. Đúng MỘT canonical identifier tồn tại cho Structure v0.3/v0.4, khai báo tại §6a.

### Self-review — 20 scenario (yêu cầu final correction task)

Chạy đủ 20 scenario: từng tiêu chí (1–8) là điểm phân biệt duy nhất giữa hai ứng viên; raw sequence không bao giờ so xuyên stream; khác `stream_id` dừng so sánh; khác `registry_version` dừng so sánh; cùng stream identity cho phép so `sequence`; cả 8 giá trị khớp = duplicate; Live/Backtest/Replay chọn cùng Swing; `broken_swing_ref` revision-qualified không đổi; `StructureFactInvalidated`/`StructureRecomputed`/dependency-forward cascade không đổi; không Regime dependency; `swing.md` v0.2 byte-identical. **20/20 scenario pass** — không phát hiện gap bổ sung ngoài phạm vi 2 finding đã cho.

### Preserve accepted behavior — không regress

`structure.md`: continuous Structure subject, BOS/CHoCH distinction, initial orientation qua BOS, CHoCH chỉ từ Bullish/Bearish, `StructureFactInvalidated`, `StructureRecomputed`, dependency-forward cascade, cursor-pinned recomputation, direct Candle input, Swing revision eligibility + revision-qualified `broken_swing_ref` (v0.3, không đổi ở v0.4), no Regime dependency, wick/close + strict/inclusive policy, venue/timeframe scope, no repaint, non-authoritative `StructureCurrentView` — **tất cả không đổi**, chỉ §6a comparator wording và §9 identifier reference được sửa. `swing.md` v0.2 và `context-map.yaml` v0.5: **không đổi, giữ nguyên byte-for-byte.**

### Metadata / state

- `structure.md`: **v0.3 → v0.4**, `status` giữ `Draft`.
- `swing.md`: **không đổi** — vẫn v0.2, `status` giữ `Draft` (verdict: Clean).
- `context-map.yaml`: **không đổi** — vẫn v0.5, `status` giữ `Draft` (verdict: Clean).
- `README.md` (domain index): **v0.9 → v0.10**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.34 → 9.35**; dòng `domain/` cập nhật ghi nhận final correction + review readiness.
- `candle.md`, `ADR-012.md`, `ADR-013.md`: **không đổi.**

**Sẵn sàng cho ChatGPT Review A final re-review + Independent Review B final re-review (chỉ `structure.md` v0.4).** Không Product Owner Approve; không Lock; không Consolidated Stable; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-B1 vẫn active và chưa hoàn tất; Package 0.2-B2/B3/B4 chưa bắt đầu; Package 0.2-C vẫn chưa có artifact nào được author; Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-29 — narrow delta revision: qualify Structure Swing references

**Không phải approval, không phải Consolidate Stable.** Vai trò: `Domain Contract Delta Revision Author · AI Technical Architect`. Revision này chỉ xử lý 2 Major finding còn lại, đã được cả ChatGPT Review A delta VÀ Independent Review B delta xác nhận trên baseline v0.2: `structure.md` **Revision required**; `swing.md` **Clean**; `context-map.yaml` **Clean**. `structure.md` `status: Draft`.

### Findings resolved (chỉ `structure.md`, v0.2 → v0.3)

- **D-B1-STR-MAJ-01 — Preserve exact Swing revision identity:** `broken_swing_ref` v0.2 (`{swing_id, direction}`) mất chính xác Swing lifecycle generation nào đã được Structure tiêu thụ. Thay bằng canonical reference revision-qualified, định nghĩa một lần tại §6a, dùng chung bởi BOS (§3) và CHoCH (§4):
  ```yaml
  broken_swing_ref:
    swing_id: {type: string, required: true}
    swing_revision: {type: integer, required: true}
    swing_confirmed_event_ref: {type: event_record_ref, required: true}
    direction: {type: enum, values: [HIGH, LOW], required: true}
  ```
  Cập nhật đầy đủ 7 vị trí: BOS payload/invariants (§3); CHoCH payload/invariants (§4); Eligible Swing definition — hoạt động trên đúng cặp `(swing_id, swing_revision)` thay vì `swing_id` một mình (§6a); same-level rule (§6, §6a, §11) — consumed semantics áp dụng cho đúng cặp, một revision khác của cùng `swing_id` đủ điều kiện độc lập; `StructureFactInvalidated` matching cho `swing_invalidated` — khớp đúng cả `swing_id` VÀ `swing_revision` (§5, ngăn `SwingInvalidated` của revision 1 invalidate nhầm fact đã tiêu thụ revision 2); worked example §10 (annotate revision cụ thể); `StructureCurrentView.current_relevant_swing_ref` (§14).

- **D-B1-STR-MAJ-02 — Cross-stream total order:** thứ tự 4-tier v0.2 (`pivot_effective_time → recorded_time → stream_ref/sequence → swing_id`) không định nghĩa cách so sánh hai stream khác nhau. Thay bằng 8-tiêu-chí tường minh, mỗi tiêu chí có hướng ASC/DESC rõ ràng (§6a):
  ```text
  1. pivot_effective_time.window_start   DESC
  2. SwingConfirmed.recorded_time        ASC
  3. stream_ref.stream_id                ASC (lexical)
  4. stream_ref.registry_version         ASC (lexical)
  5. sequence                            ASC (CHỈ trong cùng stream identity đã xác lập bởi 3+4 — cấm so sánh sequence xuyên stream)
  6. swing_revision                      DESC (revision mới nhất thắng khi mọi tiêu chí business-time/stream hòa)
  7. swing_id                            ASC (lexical, tie-break kỹ thuật thuần túy)
  8. SwingConfirmed.event_id             ASC (lexical, tie-break kỹ thuật cuối cùng)
  ```
  Nếu cả 8 giá trị khớp → duplicate của cùng một authoritative fact. Cập nhật `relevant_swing_selection_policy` (§9) thành policy identifier mới phản ánh đủ 8 tiêu chí; cập nhật `StructureCurrentView.current_relevant_swing_ref` (§14) dùng cùng tuple; xóa mọi wording "4-tier"/"no fifth criterion".

### Self-review — 20 scenario (yêu cầu delta task)

Chạy đủ 20 scenario: BOS/CHoCH consume revision 1; revision 1 invalidated; revision 2 confirmed và eligible độc lập; invalidation revision 1 không target fact dùng revision 2; same revision không phá hai lần khi fact cũ còn hiệu lực; revision 2 có thể phá sau khi fact của revision 1 bị invalidate; tie trên pivot_effective_time/recorded_time/stream_id/registry_version/sequence/swing_revision/event_id (7 tầng tie riêng biệt); Live/Backtest/Replay chọn cùng Swing; cascade vẫn dependency-forward; StructureRecomputed vẫn deterministic; StructureCurrentView vẫn non-authoritative; không Regime dependency. **20/20 scenario pass** — không phát hiện gap bổ sung ngoài phạm vi 2 finding đã cho.

### Preserve accepted behavior — không regress

Xác nhận giữ nguyên trên `structure.md`: continuous Structure subject, BOS/CHoCH distinction, initial orientation qua BOS, CHoCH chỉ từ Bullish/Bearish, `StructureFactInvalidated`, `StructureRecomputed`, dependency-forward cascade (§10, không đổi), cursor-pinned recomputation, direct Candle input, Swing revision eligibility, no Regime dependency, wick/close + strict/inclusive policy, venue/timeframe scope, no repaint, non-authoritative `StructureCurrentView`. `swing.md` v0.2 semantics: **không đổi** (Clean, giữ nguyên byte-for-byte).

### Metadata / state

- `structure.md`: **v0.2 → v0.3**, `status` giữ `Draft`.
- `swing.md`: **không đổi** — vẫn v0.2, `status` giữ `Draft` (delta verdict: Clean).
- `context-map.yaml`: **không đổi** — vẫn v0.5, `status` giữ `Draft` (delta verdict: Clean).
- `README.md` (domain index): **v0.8 → v0.9**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.33 → 9.34**; dòng `domain/` cập nhật ghi nhận delta revision + review readiness.
- `candle.md`, `ADR-012.md`, `ADR-013.md`: **không đổi.**

**Sẵn sàng cho ChatGPT Review A final delta + Independent Review B final delta (chỉ `structure.md` v0.3).** Không Product Owner Approve; không Lock; không Consolidated Stable; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-B1 vẫn active và chưa hoàn tất; Package 0.2-B2/B3/B4 chưa bắt đầu; Package 0.2-C vẫn chưa có artifact nào được author; Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-29 — consolidated revision: Swing and Structure correction semantics

**Không phải approval, không phải Consolidated Stable.** Vai trò: `Domain Contract Revision Author · AI Technical Architect`. Revision này xử lý findings hợp nhất từ ChatGPT Review A + Independent Review B clean-room trên baseline v0.1 (`swing.md`, `structure.md`) — 3 Major mỗi file + 1 Minor (`context-map.yaml`). `swing.md`/`structure.md`/`context-map.yaml` `status: Draft`.

### Findings resolved

**`swing.md` (v0.1 → v0.2):**

- **C-B1-SWG-MAJ-01 — Explicit Swing revision lifecycle:** thay prose "UNSEEN-tương-đương" (v0.1) bằng mô hình tường minh `swing_revision`/`supersedes_revision` (§1a mới). `swing_id` vẫn là logical identity bất biến (sáu field, KHÔNG gồm `swing_revision`); `(swing_id, swing_revision)` định danh một lifecycle generation, mỗi generation có state machine RIÊNG (`UNSEEN → CANDIDATE → CONFIRMED/INVALIDATED`), `INVALIDATED` terminal cho ĐÚNG revision đó. Revision mới bắt buộc causation tới `SwingInvalidated` của revision liền trước.
- **C-B1-SWG-MAJ-02 — Canonical subject scope đầy đủ:** `subject_ref.scope` (§2) trước đây THIẾU `pivot_candle_subject_id` (chỉ có 5/6 field). Bổ sung đủ sáu field + `revision_ref.swing_revision` lồng bên trong (generation identity, KHÔNG tham gia derive `subject_id`). `SwingCurrentView.scope` (§6) cập nhật tương ứng, cộng `current_revision` field.
- **C-B1-SWG-MAJ-03 — Full confirmation evidence:** `SwingConfirmed` (§4) trước đây chỉ có `pivot_price` + `right_evidence_refs` (thiếu `pivot_candle_ref`, `left_evidence_refs`). Thay bằng `confirmation_evidence: {pivot_candle_ref, left_evidence_refs, right_evidence_refs}` bắt buộc, đầy đủ trên MỌI đường dẫn tới CONFIRMED (CANDIDATE→CONFIRMED, historical UNSEEN→CONFIRMED, re-confirmation revision > 1) — candidate tiền nhiệm không còn được coi là bằng chứng đủ tự thân.

**`structure.md` (v0.1 → v0.2):**

- **C-B1-STR-MAJ-01 — Tách historical fact invalidation khỏi orientation transition:** `StructureInvalidated` (v0.1, gộp cả hai mối quan tâm) **không còn tồn tại** — thay bằng `StructureFactInvalidated` (§5 — phủ định MỘT fact lịch sử cụ thể, KHÔNG tự động tuyên bố orientation transition, hợp lệ ngay cả khi current_orientation đã là NEUTRAL) và `StructureRecomputed` (§5a — event DUY NHẤT xác lập current_orientation mới sau cascade, `resulting_orientation ∈ {NEUTRAL, BULLISH, BEARISH}`, `justifying_fact_ref` bắt buộc khi khác NEUTRAL). State machine (§1) cập nhật: normal flow (BOS/CHoCH) transition trực tiếp; correction flow chỉ qua `StructureRecomputed` — đủ 9 tổ hợp `{NEUTRAL,BULLISH,BEARISH}²`, không chỉ thêm `NEUTRAL → NEUTRAL`.
- **C-B1-STR-MAJ-02 — Deterministic relevant Swing total order:** thêm §6a mới — định nghĩa "Eligible Swing" executable đầy đủ + total order 4 tiêu chí (`pivot_effective_time` → `SwingConfirmed.recorded_time` → `stream_ref`/`sequence` → `swing_id` tie-break), pin qua `structure_definition_version.relevant_swing_selection_policy` (§9). Làm rõ chỉ revision hợp lệ mới nhất của một `swing_id` (swing.md §1a) mới eligible. `StructureCurrentView.current_relevant_swing_ref` (§14) cập nhật theo total order này — đóng OQ tác giả cũ về "Swing nào đó gần đây."
- **C-B1-STR-MAJ-03 — Dependency-forward cascade, bỏ "most-recent-first":** viết lại §10 — cascade traverse theo chuỗi orientation GỐC (`E(k+1).prior_orientation = E(k).new_orientation`), không theo recorded_time phát sinh invalidation. Thêm worked example đúng theo yêu cầu (`E1→E2→E3`, `I1/I2/I3`, `R1`) minh họa causation chain đầy đủ và cách `resulting_orientation` của `R1` được xác định deterministic qua refold.

**`context-map.yaml` (v0.4 → v0.5):**

- **C-B1-CM-MIN-01:** sửa comment gây hiểu nhầm "candle.md là provider contract DUY NHẤT tồn tại trong repository" thành chính xác: candle.md là provider contract DUY NHẤT hiện **cần một cross-context relationship entry tại file này** — swing.md/structure.md cũng là provider contract đã tồn tại, nhưng quan hệ Swing → Structure là intra-context (quyết định đã ghi ở transaction B1 authoring, không đổi). Không đổi relationship semantics nào.

### Self-review — 12 Swing + 16 Structure attack scenarios (yêu cầu revision task)

Chạy đầy đủ 12 scenario Swing (candidate→confirmed revision 1; candidate invalidated; confirmed invalidated by correction; same pivot → revision 2; different pivot → new swing_id; revision 2 replayed after revision 1 invalidation; historical confirmation với đủ left+right evidence; hai pivot khác nhau chỉ ở pivot Candle; canonical scope verify logical ID; cùng pivot hai definition version; out-of-order correction; cùng Candle qua HIGH và LOW) và 16 scenario Structure (initial BOS; continuation BOS; CHoCH; direct breaking Candle correction; broken Swing invalidation; E1→E2→E3 cascade; multiple invalidation khi đã NEUTRAL; recompute → NEUTRAL/BULLISH/BEARISH; hai Eligible Swing cần tie-break; revision 1 invalid + revision 2 valid; replay từng bước cascade; StructureCurrentView non-authoritative; no Regime; same level không phá hai lần). **Tất cả 28/28 scenario pass** với thiết kế v0.2 — không phát hiện gap bổ sung ngoài phạm vi 6 finding đã cho.

### Preserve accepted behavior — không regress

Xác nhận giữ nguyên: Swing — six-field logical identity, opaque `swing_id`, HIGH/LOW separation, multiple definition versions, historical direct confirmation, no-look-ahead, candidate vs authoritative, market-evolution invalidation chỉ trước confirmation, upstream correction invalidation, missing-data distinctions, four-mode parity, non-authoritative current view. Structure — continuous logical subject, BOS vs CHoCH distinction, initial orientation qua BOS, CHoCH chỉ từ Bullish/Bearish, direct Candle input, Swing input, no Regime dependency, wick/close + strict/inclusive policy pinning, same-level break rule, venue/timeframe scope, no repaint, non-authoritative current view. `candle.md` và mọi Context Map relationship hiện có: **không đổi.**

### Metadata / state

- `swing.md`: **v0.1 → v0.2**, `status` giữ `Draft`.
- `structure.md`: **v0.1 → v0.2**, `status` giữ `Draft`.
- `context-map.yaml`: **v0.4 → v0.5**, `status` giữ `Draft`.
- `README.md` (domain index): **v0.7 → v0.8**, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.32 → 9.33**; dòng `domain/` cập nhật ghi nhận revision + review readiness.
- `candle.md`, `ADR-012.md`, `ADR-013.md`: **không đổi.**

**Sẵn sàng cho ChatGPT Review A delta + Independent Review B delta.** Không Product Owner Approve; không Lock; không Consolidated Stable; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-B vẫn active và chưa hoàn tất; Package 0.2-B2/B3/B4 chưa bắt đầu; Package 0.2-C vẫn chưa có artifact nào được author; Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-28 — author Package 0.2-B1: Swing and Structure contracts

**Không phải approval, không phải review-complete, không phải Consolidated Stable.** Vai trò: `Domain Contract Author · AI Technical Architect`. Chỉ author self-review đã thực hiện — ChatGPT Review A và Independent Review B **chưa diễn ra**. `swing.md`/`structure.md` `status: Draft`.

### Phạm vi authoring — Package 0.2-B1 only

`docs/domain/swing.md` v0.1 (mới) và `docs/domain/structure.md` v0.1 (mới), hoàn thiện chuỗi `Candle → Swing → Structure`. Cả hai `capability_id: market-structure` / `domain_context_id: market-structure-analysis` — đã đăng ký sẵn tại `context-map.yaml`, không tạo capability/context mới. Không author `regime.md`/`feature.md`/`context.md` (0.2-B2/B3/B4) hay bất kỳ artifact Package 0.2-C nào.

### Quyết định thiết kế chính (semantic decisions)

- **Swing identity** — 6 field qualifying scope: `instrument_id`, `venue_id`, `timeframe`, `direction` (HIGH/LOW), `pivot_candle_subject_id`, `swing_definition_version`. `swing_definition_version` cố ý nằm trong identity scope để hai Swing Definition khác nhau cùng tồn tại hợp lệ trên cùng pivot Candle — không khóa một trường phái phân tích kỹ thuật duy nhất.
- **Swing lifecycle** — `UNSEEN → CANDIDATE → CONFIRMED/INVALIDATED`, cộng đường tắt `UNSEEN → CONFIRMED` cho historical/closed-only ingestion (đối xứng `candle.md` §1's `UNSEEN → CLOSED`), không fabricate candidate history giả.
- **No-repaint boundary cho Swing** — một `SwingConfirmed` chỉ có thể bị `SwingInvalidated` qua `invalidation_cause: upstream_correction`; **KHÔNG BAO GIỜ** qua `market_evolution` một khi đã CONFIRMED (giá tiếp tục di chuyển sau confirm không làm Swing sai — đó là input hợp lệ cho BOS/CHoCH, không phải lý do invalidate Swing).
- **Correction identity rule (Swing)** — correction đổi giá trị pivot nhưng KHÔNG đổi `pivot_candle_subject_id` → CÙNG `swing_id` (Invalidated → fact mới cùng subject); correction làm đổi Candle nào là pivot → `swing_id` KHÁC (subject mới). Một rule duy nhất, không nhánh mơ hồ.
- **Confirmation policy KHÔNG hardcode một trường phái** — `left_count`/`right_count`/`price_basis` (wick|close)/`equal_level_policy` pin qua `swing_definition_version` — Referenced Authoritative Artifact theo Chapter 8 §8.1.1.
- **Structure identity — pattern khác Candle/Swing** — MỘT subject liên tục theo `(instrument_id, venue_id, timeframe, structure_definition_version)`, không phải subject-per-instance; orientation là derived state rebuild từ chuỗi event, không phải field ghi đè.
- **Orientation state machine** — `UNDETERMINED` (notional, như `UNSEEN`) / `NEUTRAL` (authoritative, chỉ đạt qua `StructureInvalidated`) / `BULLISH` / `BEARISH`. Không tạo `StructureStateChanged` riêng — thiết lập orientation lần đầu (từ `UNDETERMINED`/`NEUTRAL`) dùng CHÍNH `BreakOfStructureDetected`, cùng executable criterion với continuation BOS, khác biệt chỉ ở diễn giải `prior_orientation`.
- **CHoCH thay đổi orientation NGAY LẬP TỨC** — không qua candidate transition riêng (justification: cả Swing level lẫn breaking Candle đã là fact authoritative tại thời điểm CHoCH phát sinh, không có độ trễ evidence như Swing cần).
- **BOS/CHoCH broken-level decision table tường minh** — continuation BOS phá level cùng hướng orientation (HIGH cho BULLISH, LOW cho BEARISH); CHoCH phá level đối lập (LOW để BULLISH→BEARISH, HIGH để BEARISH→BULLISH).
- **Structure input KHÔNG chỉ Swing** — tiêu thụ trực tiếp `candle-closed`/`candle-corrected` (justification tường minh tại `structure.md` § Inputs): cần cho break confirmation VÀ cho correction-cascade nhánh breaking-candle không đi qua Swing nào.
- **Context Map: KHÔNG thêm self-edge Swing → Structure** — sau khi đối chiếu Chapter 4 §4.2 (relationships map định nghĩa quan hệ GIỮA các context, mọi ví dụ/relationship hiện có đều cross-context), quyết định: Swing → Structure là published contract intra-context, thuộc phạm vi hai Domain Contract, không phải Context Map. Quyết định ghi tường minh làm comment trong `context-map.yaml`.

### Self-review — phát hiện và xử lý

Chạy đủ 12 attack scenario cho Swing + 16 cho Structure (yêu cầu authoring task) trước khi commit. **11/12 + 15/16 scenario đã covered by design ban đầu.** Phát hiện **một gap thực sự**: Structure attack scenario "correction cascade invalidates multiple downstream facts" — thiết kế ban đầu chỉ invalidate trực tiếp fact bị ảnh hưởng bởi Swing/Candle correction, KHÔNG xử lý các `BreakOfStructureDetected`/`ChangeOfCharacterDetected` phát sinh SAU đó mà `prior_orientation` phụ thuộc bắc cầu vào orientation vừa bị phủ định.

**Xử lý:** thêm `invalidation_cause: chained_invalidation` (giá trị enum thứ ba, `structure.md` §5) cộng invariant bắt buộc most-recent-first cascade, cộng một đoạn giải thích + ví dụ cụ thể (§10) — đảm bảo không fact nào còn "treo" với `prior_orientation` trỏ về một orientation đã invalidate. Đây là thay đổi được áp dụng **trước** commit, phản ánh trong chính nội dung `structure.md` v0.1 (không phải một revision riêng).

### Known risks / provisional defaults (không phải Open Question chặn governance)

- `swing_definition_version`/`structure_definition_version` chưa có authoritative registry/lifecycle riêng — ghi nhận tường minh ở `swing.md` §18 và `structure.md` §17 làm ghi chú tác giả, không tạo OQ repository-wide, không đóng OQ-002/OQ-003.
- Đường `UNSEEN → CONFIRMED` hiện chỉ scope cho historical ingestion, chưa mở cho Live — ghi chú tại `swing.md` §18.
- `StructureCurrentView.current_relevant_swing_ref` chưa có semantics đầy đủ khi nhiều Swing cùng hướng đủ điều kiện đồng thời — ghi chú tại `structure.md` §17, không ảnh hưởng authoritative event contract.

### Metadata / state

- `swing.md`: **mới, v0.1**, `status: Draft`.
- `structure.md`: **mới, v0.1**, `status: Draft`.
- `context-map.yaml`: **v0.3 → v0.4**, `status` giữ `Draft` — đăng ký swing/structure đã authored (owned_contracts comment), không self-edge, mọi capability/context/relationship hiện có giữ nguyên.
- `README.md` (domain index): **v0.6 → v0.7**, `status` giữ `Draft` — Package 0.2-B row + mục Package 0.2-B1 mới.
- `MANIFEST.md`: `manifest_version` **9.31 → 9.32**; dòng `domain/` cập nhật ghi nhận B1 Draft, review-chưa-diễn-ra, Package 0.2-B chưa Consolidated Stable.
- `ADR-012.md`/`ADR-013.md`/`candle.md`: **không đổi.**

**Sẵn sàng chuyển ChatGPT Review A.** Không Product Owner Approve; không Lock; không đóng OQ-002/OQ-003; không authorize Live; Package 0.2-B chưa `Consolidated Stable`; Package 0.2-B2/B3/B4 chưa bắt đầu; Package 0.2-C vẫn chưa có artifact nào được author; Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-28 — approve ADR-012 and ADR-013 (Product Owner)

**Product Owner decision — final, không phải đề xuất AI reviewer:**

```text
Approve ADR-012 v0.3
Approve ADR-013 v0.3
```

### Review completion ghi nhận tại approval boundary

- **ADR-012 v0.3:** ChatGPT Review A final re-review — Clean. Independent Review B final delta — Clean. Backward Consistency Check — `No conflict`. **0 qualifying finding.**
- **ADR-013 v0.3:** ChatGPT Review A final re-review — Clean. Independent Review B final delta — Clean. Backward Consistency Check — `No conflict`. **0 qualifying finding.**

### Approval metadata (atomic, theo Chapter 11 §11.6)

- **ADR-012:** `status: Draft → Approved`, `approved_by: Product Owner`, `approved_at: "2026-07-28"`, `last_review: "2026-07-28"`, `version` giữ `"0.3"`. Reviewer table (§4) pin: ChatGPT (`AI Technical Architect`), Independent Review B (`AI Technical Architect`) — evidence Clean/0 qualifying finding, khớp đúng nội dung đã ghi tại CHANGELOG/MANIFEST trước đó, không thêm concern/risk/recommendation mới. Không có OQ nào resolve.
- **ADR-013:** `status: Draft → Approved`, `approved_by: Product Owner`, `approved_at: "2026-07-28"`, `last_review: "2026-07-28"`, `version` giữ `"0.3"`. Reviewer table (§4) pin tương tự ADR-012. **OQ-002 KHÔNG resolve** — ADR-013 approval không quyết Strategy Lifecycle Live-gate (đã nêu rõ ở §9 Open questions ngoài phạm vi, và tường minh lại trong khối Product Owner decision của ADR).
- Kiến trúc/nội dung quyết định của cả hai ADR **không đổi** — chỉ metadata + reviewer evidence pin thay đổi. Theo Chapter 11 §11.6, sau approval, ADR file không được sửa lại nữa.
- `Approved` **≠** `Locked` — hai state khác nhau trong repository governance (xem `adr/ADR-005.md`, `ADR-006.md`, `ADR-007.md` = `Locked`; `ADR-008/009/010/011` = `Approved`, không `Locked`). ADR-012/ADR-013 dùng đúng `Approved`, không dùng `Locked`.

### Package 0.2-C — ADR dependency gate effect

ADR-012 và ADR-013 Approved → **ADR dependency gate cho Package 0.2-C nay mở.** Package 0.2-C **authorized to begin planning and authoring, subject to its normal package scope authorization and review workflow.** **Không có Package 0.2-C artifact nào được author trong transaction này.** `docs/domain/README.md` cập nhật dòng Package 0.2-C phản ánh đúng gate effect này; `version: "0.5" → "0.6"`, `status` giữ `Draft`.

### Không đổi

Package 0.2-A vẫn `Consolidated Stable` (package lifecycle/readiness state, không phải document approval status); `context-map.yaml`, `candle.md` không đổi. Package 0.2-B vẫn "authorized to begin authoring, chưa có artifact nào được author". OQ-002, OQ-003 vẫn `Open`.

### Metadata / state

- `ADR-012.md`: **v0.3, `status: Approved`**, `approved_by: Product Owner`, `approved_at: "2026-07-28"`.
- `ADR-013.md`: **v0.3, `status: Approved`**, `approved_by: Product Owner`, `approved_at: "2026-07-28"`.
- `README.md` (domain index): **v0.5 → v0.6**, `status` giữ `Draft` — Package 0.2-C row cập nhật.
- `MANIFEST.md`: `manifest_version` **9.30 → 9.31**; `compatible_adr_range` **"ADR-001 ~ ADR-011" → "ADR-001 ~ ADR-013"**; ADR table + Decision Log ghi ADR-012/ADR-013 `Approved`; dòng `domain/` cập nhật phản ánh ADR approval + Package 0.2-C gate effect.

**ADR-012 và ADR-013 đã Approved. Không Lock artifact nào (governance không yêu cầu Lock tại approval boundary này). Không đóng OQ-002/OQ-003 — cả hai vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.**

## [Unreleased] — 2026-07-28 — consolidate Package 0.2-A stable baseline (ADR-012, ADR-013, Package 0.2-A)

**Không phải approval, không phải Lock.** `status` của mọi artifact liên quan giữ `Draft`; `approved_by`/`approved_at` giữ `null`. Transaction này **ghi nhận** kết quả review/consolidation cuối cùng đã hoàn tất cho ADR-012, ADR-013 và Package 0.2-A — không tạo finding mới, không thay đổi nội dung ADR-012/ADR-013/candle.md.

### Kết quả review cuối cùng được ghi nhận

- **ADR-012 v0.3:** ChatGPT Review A final re-review — Clean. Independent Review B final delta — Clean. Backward Consistency Check — `No conflict`. **0 qualifying finding.** Disposition: `Ready for Product Owner approval boundary`. `status` giữ `Draft`.
- **ADR-013 v0.3:** ChatGPT Review A final re-review — Clean. Independent Review B final delta — Clean. Backward Consistency Check — `No conflict`. **0 qualifying finding.** Disposition: `Ready for Product Owner approval boundary`. `status` giữ `Draft`.
- **Package 0.2-A** (`context-map.yaml` + `candle.md`): ChatGPT Review A final re-review — Clean. Independent Review B final delta — **Clean với đúng 1 Suggestion không-blocking.** Backward Consistency Check — `No conflict`. **0 qualifying finding.** Final disposition: **`Consolidated Stable`**.

### Suggestion không-blocking — đã incorporate

`context-map.yaml`: cho cả hai relationship `candle-corrected` (provider `market-data-observation` → consumer `market-structure-analysis`, và → `raw-regime-analysis`), sửa cross-reference thiếu chính xác "chi tiết semantic tại candle.md §11" thành "chi tiết correction/recompute và classification semantics tại candle.md §§10–11". **Thuần túy sửa tài liệu tham chiếu, không đổi semantic** — provider/consumer/`contract_id`/`relationship_type`/`model_influence`/`translation_policy`/`consumer_obligation` giữ nguyên nội dung nghĩa. `version: "0.2" → "0.3"`, `status` giữ `Draft`.

### Consolidation recording — README.md

- Package 0.2-A: trạng thái lifecycle cập nhật thành `Consolidated Stable` — định nghĩa tường minh là **package lifecycle/readiness state, KHÔNG phải document approval status**; mọi artifact cấu thành (`context-map.yaml`, `candle.md`, `README.md`) **vẫn giữ `status: Draft`**.
- Package 0.2-B: cập nhật từ "Chưa bắt đầu" thành "Authorized to begin authoring sau khi Package 0.2-A đạt `Consolidated Stable`" — **chưa có artifact 0.2-B nào được author** trong transaction này hay bất kỳ transaction trước đó.
- `README.md`: `version: "0.4" → "0.5"`, `status` giữ `Draft`.

### Không đổi trong transaction này

`ADR-012.md` nội dung, `ADR-013.md` nội dung, `candle.md` (v0.4), Constitution, mọi Approved ADR, trạng thái OQ-002/OQ-003 (vẫn `Open`). Reviewer table của ADR-012/ADR-013 (§4) giữ nguyên trống — theo Chapter 11, việc pin reviewer evidence chỉ xảy ra tại atomic approval transaction; readiness được ghi nhận ở CHANGELOG/MANIFEST thay vì bịa reviewer name/timestamp/concern text.

### Metadata / state

- `context-map.yaml`: **v0.2 → v0.3**, `status` giữ `Draft`.
- `README.md` (domain index): **v0.4 → v0.5**, `status` giữ `Draft`.
- `candle.md`: **không đổi** — vẫn v0.4, `status` giữ `Draft`.
- `ADR-012.md`: **không đổi** — vẫn v0.3, `status` giữ `Draft`.
- `ADR-013.md`: **không đổi** — vẫn v0.3, `status` giữ `Draft`.
- `MANIFEST.md`: `manifest_version` **9.29 → 9.30**; dòng `domain/` cập nhật ghi nhận `Consolidated Stable`, ADR-012/ADR-013 review-complete-nhưng-Draft, Package 0.2-B authorized-nhưng-chưa-author.

**Package 0.2-A đạt `Consolidated Stable`; Package 0.2-B được authorize để bắt đầu authoring nhưng chưa có artifact nào được author; Package 0.2-C vẫn chưa bắt đầu.** Không Product Owner Approve artifact nào; không Lock artifact nào; không đóng OQ-002/OQ-003; không authorize Live ở bất kỳ hình thức nào; Phase 0.2 vẫn active và chưa hoàn tất.

## [Unreleased] — 2026-07-28 — candle.md v0.3 → v0.4 — strict duplicate/correction/fail-closed precedence

**Không phải approval.** `status` giữ `Draft`, `approved_by`/`approved_at`/`last_review` giữ `null`. Sửa theo ChatGPT Review A re-review + Independent Review B delta review: **1 Major (F-CND-MAJ-01)**. `context-map.yaml` **không đổi** ở vòng này (clean, không cần sửa).

### Đã sửa (Major — F-CND-MAJ-01) — precedence algorithm 5 bước thay wording mơ hồ

Viết lại toàn bộ §11 thành algorithm nghiêm ngặt, đúng thứ tự, không rẽ nhánh ngoài 5 bước:

1. **Xác lập idempotency identity** — native `source_identity` hoặc fallback do source/adapter contract khai báo tường minh (deterministic, versioned cùng contract, không bịa ad hoc, bảo toàn replay parity).
2. **Không resolve được identity → fail closed/quarantine** — không append CandleClosed, không dedupe, không phát CandleCorrected. Thiếu provenance không phải bằng chứng cho correction.
3. **Cùng identity:** payload giống hệt → duplicate, zero effect; **payload khác dù cùng identity → provenance integrity violation → fail closed** (cấm âm thầm coi là correction hợp lệ).
4. **Identity khác, cùng subject, payload authoritative đổi → CandleCorrected**, `causation_refs` trỏ đúng fact đang authoritative; yêu cầu provenance riêng cho correction (identity nguồn khác biệt resolve được, hoặc correction identity do source contract khai báo). Một second non-identical authoritative fact không bao giờ là `CandleClosed` thứ hai.
5. **Identity khác, cùng payload:** chỉ coi duplicate tương đương khi source contract khai báo tường minh equivalence semantics; ngược lại quarantine/fail closed chờ reconciliation.

Cập nhật cross-reference liên quan tại §4 (invariant), §5 (description), §13 (Deduplication) để khớp đúng 5-bước mới, không còn chỉ nói "dedupe hoặc CandleCorrected".

### Hành vi đã chấp nhận — giữ nguyên, không suy yếu

5-field Candle subject identity · `UNSEEN` state + closed-only ingestion · canonical event envelope · qualified `subject_ref` · append-only history · correction self-transition · bitemporal replay · 5-điều-kiện zero-volume provenance · missing-data semantics · venue neutrality · correction-propagation relationships (context-map.yaml, không đổi) · Replay/Backtest/Paper/Live parity.

### Metadata / state

- `candle.md`: **v0.3 → v0.4**, `status` giữ `Draft`.
- `context-map.yaml`: **không đổi** — xác nhận clean, không cần sửa.
- `README.md`: cập nhật version/lifecycle wording — ghi nhận 2 vòng review đã xử lý, `Consolidated Stable` vẫn chưa đạt.
- `MANIFEST.md`: `manifest_version` **9.28 → 9.29**; dòng `domain/` cập nhật phản ánh `candle.md` v0.4 + cross-reference ADR-012 v0.3/ADR-013 v0.3.

**Package 0.2-B vẫn chưa bắt đầu.** Không đóng OQ nào; không authorize Live.

## [Unreleased] — 2026-07-28 — ADR-013 v0.2 → v0.3 — authority-table wording cleanup

**Không phải approval.** `status` giữ `Draft`, `approved_by`/`approved_at`/`last_review` giữ `null`. Sửa theo ChatGPT Review A re-review + Independent Review B delta review: **1 Minor (F-ADR13-MIN-01)**. Product Owner direction gốc **không đổi** qua cả hai vòng review.

### Đã sửa (Minor — F-ADR13-MIN-01) — stale authority table wording

Bảng 4 trục (§2.1) cột Authority của "Strategy Definition Version" từng ghi "Domain Contract (mới, thuộc ADR này)" — đọc được thành ADR sở hữu luôn nội dung, mâu thuẫn với khối "Authority clarification" ngay bên dưới (vốn đã tách đúng: ADR sở hữu *yêu cầu trục tồn tại*, Domain Contract sở hữu *schema/lifecycle/nội dung*). Sửa cột Authority khớp đúng câu chữ với Authority clarification — một rule, không còn hai cách đọc khác nhau ở hai chỗ trong cùng file.

### Không đổi

Bốn trục evidence độc lập; no-proxy rule; rebuilt artifact identity (§2.5); OQ-002 state (vẫn không quyết, §9).

### Metadata / state

- `ADR-013.md`: **v0.2 → v0.3**, `status` giữ `Draft`. `depends_on: [ADR-010]` không đổi; ADR-010 không bị sửa.
- Reviewer table (§4) vẫn để trống — ghi nhận cả hai vòng review (baseline v0.1 và v0.2) đã diễn ra.

**Không đóng OQ-002.** Không authorize Live.

## [Unreleased] — 2026-07-28 — ADR-012 v0.2 → v0.3 — broker multi-Venue Position authority

**Không phải approval.** `status` giữ `Draft`, `approved_by`/`approved_at`/`last_review` giữ `null`. Sửa theo ChatGPT Review A re-review + Independent Review B delta review: **1 Major (F-ADR12-MAJ-01)**. Product Owner direction gốc **không đổi** qua cả hai vòng review.

### Đã sửa (Major — F-ADR12-MAJ-01) — Position scope dưới broker-bound Account

- Thêm §2.5 "Position scope dưới Account Boundary": venue-bound Account — Position có thể inherit execution Venue, xung đột tường minh thì reject; broker-bound Account — **mọi transactional Position bắt buộc mang `execution_venue_id` tường minh**, authority scope theo tổ hợp Account + execution Venue + instrument (+ settlement/margin scope nếu Position Domain Contract cần), balance/collateral/margin/liquidation/settlement/fill-attribution venue-native **không được gộp** xuyên-Venue vào một transactional Position.
- **Broker-level exposure** khóa là `kind: read_model`/projection — tổng hợp, không thay thế transactional Position authority; phải truy vết được về Account+Venue Position gốc; chỉ dùng cho Portfolio/Risk view theo rule mà Domain Contract tương lai định nghĩa.
- Thêm nghĩa vụ reject #9 (§2.6, cũ §2.5 đổi số): broker-bound transactional Position thiếu `execution_venue_id` tường minh → reject.
- Sửa §2.4 để không còn ngụ ý Account một mình đủ scope một transactional Position dưới broker_account boundary; cập nhật §6 Consequences phản ánh rule mới.

### Metadata / state

- `ADR-012.md`: **v0.2 → v0.3**, `status` giữ `Draft`. `depends_on: [ADR-007]` không đổi; ADR-007 không bị sửa.
- Reviewer table (§4) vẫn để trống — ghi nhận cả hai vòng review (baseline v0.1 và v0.2) đã diễn ra; pin evidence chờ approval boundary (Chapter 11 §11.6).

**Không đóng OQ nào.** Không authorize Live.

## [Unreleased] — 2026-07-28 — Package 0.2-A consolidated revision (context-map v0.2, candle v0.3)

**Không phải approval.** Cả hai artifact vẫn `status: Draft`. Sửa theo ChatGPT Review A + Independent Review B (consolidated) trên baseline `context-map.yaml` v0.1 / `candle.md` v0.2: **2 Major cho context-map (C-CM-MAJ-01, C-CM-MAJ-02), 2 Major + 2 Minor cho candle (C-CND-MAJ-01, C-CND-MAJ-02, C-CND-MIN-03, C-CND-MIN-04)**. Revision này **chưa qua review** — không tuyên bố re-review đã xảy ra.

### `context-map.yaml` v0.1 → v0.2

- **(Major C-CM-MAJ-01)** Thay `contract_id: CandleClosed` (display name, ambiguous) bằng scalar concept-id đúng schema Chapter 4 §4.2 (ví dụ chính chương dùng `ExecutionFill.v1`): `contract_id: candle-closed` / `contract_id: candle-corrected` — khớp đúng `id:` khai báo trong `candle.md`. Thêm comment khối giải thích 3 đại lượng tách biệt (concept id / display name / `event_type`) không được cạnh tranh làm identity.
- **(Major C-CM-MAJ-02)** Thêm 2 relationship mới cho correction propagation: `candle-corrected → market-structure-analysis` và `candle-corrected → raw-regime-analysis` (trước đó chỉ có `candle-closed`). Mỗi relationship correction mang field mở rộng `consumer_obligation`: consumer phải invalidate/recompute derived fact có causal ancestry từ Candle fact bị sửa.

### `candle.md` v0.2 → v0.3

- **(Major C-CND-MAJ-01)** Candle subject key giờ tường minh **đúng năm field**: `instrument_id, venue_id, timeframe, window_start, window_end` (trước đó invariant chỉ liệt 4 field, bỏ sót `window_end`). Cùng năm-field-scope → cùng `candle_subject_id`; khác bất kỳ field nào → khác `candle_subject_id`.
- **(Major C-CND-MAJ-02)** Thêm state `UNSEEN` (notional initial state) vào `state_machine`: `UNSEEN → PROVISIONAL` (CandleObserved), `UNSEEN → CLOSED` (CandleClosed) — cho phép historical/closed-only ingestion (Backtest nạp candle đã đóng sẵn) đi thẳng mà **không fabricate** một CandleObserved giả.
- **(Minor C-CND-MIN-03)** Thêm §11 "Duplicate CandleClosed handling": cùng `source_identity` → dedupe zero-effect; khác nội dung → phải là `CandleCorrected`, không phải `CandleClosed` thứ hai; fallback idempotency key chỉ hợp lệ khi source/adapter contract khai báo tường minh, thiếu cả native lẫn fallback → fail closed.
- **(Minor C-CND-MIN-04)** `source_identity` example (§13) đổi từ giá trị cụ thể (`binance`, `BTCUSDT`) sang placeholder venue-neutral (`<canonical_venue_id>`, `<canonical_instrument_id>`...); raw exchange symbol chỉ được tồn tại trong provenance do ingestion adapter sở hữu.
- **Sửa thêm (self-review, ngoài consolidated findings):** 3 cross-reference nội bộ bị lệch số mục từ vòng v0.1→v0.2 (khi chèn §2 Canonical envelope làm dịch số các mục sau) — đã rà và sửa lại đúng (`§9`→`§13` cho dedup, `§10`→`§12` cho missing-data provenance, ở 3 vị trí).

### Hành vi đã chấp nhận — giữ nguyên, không suy yếu

Canonical event envelope · qualified `subject_ref` · append-only provisional history · no-repaint · correction self-transition · 5-điều-kiện zero-volume provenance · phân biệt 3 case missing-data (+ phân biệt UNSEEN mới) · Chapter 5 time model · read-model non-authority · venue/session neutrality · Replay/Backtest/Paper/Live parity.

### Metadata / state

- `context-map.yaml`: **v0.1 → v0.2**, `status` giữ `Draft`.
- `candle.md`: **v0.2 → v0.3**, `status` giữ `Draft`.
- `README.md`: Package 0.2-A row cập nhật version mới + disposition "đã xử lý consolidated finding, chưa qua re-review"; `Consolidated Stable` vẫn chưa đạt.
- `MANIFEST.md`: `manifest_version` **9.27 → 9.28**; dòng `domain/` cập nhật.
- ADR-012, ADR-013: **không đổi trong commit này** (đã revise ở 2 commit riêng trước đó).

**Package 0.2-B vẫn chưa bắt đầu.** Không đóng OQ nào; không authorize Live.

## [Unreleased] — 2026-07-28 — ADR-013 v0.1 → v0.2 — authority clarification + rebuilt artifact identity

**Không phải approval.** `status` giữ `Draft`, `approved_by`/`approved_at`/`last_review` giữ `null`. Sửa theo ChatGPT Review A + Independent Review B (consolidated): **2 Suggestion (C-ADR13-SUG-01, C-ADR13-SUG-02)**. Product Owner direction gốc (4 trục evidence độc lập, không proxy) **không đổi**.

### Đã sửa (Suggestion — C-ADR13-SUG-01) — Authority clarification

Thêm khối "Authority clarification" ngay dưới bảng 4 trục (§2.1): ADR-013 chỉ sở hữu **yêu cầu kiến trúc** rằng Strategy Definition Version là trục độc lập; `strategy-definition.md` (Package 0.2-C, chưa author) sở hữu schema/lifecycle/nội dung version/field ngữ nghĩa cụ thể; Plugin Version giữ nguyên authority implementation-release identity (Chapter 9 §9.1, không đổi).

### Đã sửa (Suggestion — C-ADR13-SUG-02) — Rebuilt artifact identity

Thêm §2.5 mới: hai executable artifact khác biệt vật chất (compiler, dependency, build flags, base image, packaging, hoặc bytes cuối cùng khác — kể cả non-reproducible rebuild) **phải** có Package/Build Artifact identity khác nhau, **kể cả khi Plugin Version/source commit không đổi**; artifact identity phải resolve tới exact bytes hoặc provenance record bất biến tương đương, không dùng Plugin Version/commit hash làm proxy. Nối vào §2.4: "resolvable Package/Build Artifact" nghĩa là artifact **thực sự đang chạy**, không phải artifact lẽ ra phải giống.

### Metadata / state

- `ADR-013.md`: **v0.1 → v0.2**, `status` giữ `Draft`. `depends_on: [ADR-010]` không đổi; ADR-010 không bị sửa.
- Reviewer table (§4) vẫn để trống — cùng lý do như ADR-012 (pin evidence tại approval boundary, Chapter 11 §11.6); provenance round review này ghi tại đây.

**Không đóng OQ-002.** Không authorize Live.

## [Unreleased] — 2026-07-28 — ADR-012 v0.1 → v0.2 — canonical Account Boundary model

**Không phải approval.** `status` giữ `Draft`, `approved_by`/`approved_at`/`last_review` giữ `null`. Sửa theo ChatGPT Review A + Independent Review B (consolidated): **1 Major (C-ADR12-MAJ-01), 1 Minor (C-ADR12-MIN-02)**. Product Owner direction gốc (Account thuộc đúng một Venue/broker-account boundary) **không đổi** — chỉ chính xác hóa executable representation.

### Đã sửa (Major — C-ADR12-MAJ-01) — canonical Account Boundary model thay wording mơ hồ

- Thay "`venue_id` hoặc broker-account-boundary reference tương đương" bằng một schema duy nhất: `account_boundary_ref: {boundary_type: venue | broker_account, boundary_id}`. Mỗi Account có đúng một, required, immutable; `account_id` vẫn opaque, không nhúng/parse boundary.
- Tách rõ 2 nhánh: **venue boundary** (Account thuộc trực tiếp 1 Venue, execution venue có thể inherit) và **broker_account boundary** (Account thuộc 1 broker relationship có thể route đa-venue; **mỗi Order/Fill bắt buộc `execution_venue_id` tường minh**; **không** Domain Contract nào được giả định resolve về đúng 1 Venue trong nhánh này).
- Title đổi từ "Exactly-One-Venue Trading Account" sang **"Account-to-Boundary Cardinality — Exactly-One-Boundary Trading Account"** — khớp đúng nghĩa đen "Venue hoặc broker-account boundary" mà chính PO direction đã dùng.

### Đã sửa (Minor — C-ADR12-MIN-02) — executable validation obligations

Thêm §2.5, 8 nghĩa vụ reject bắt buộc: zero boundary · nhiều hơn một boundary · rebind tại chỗ · Order/Fill/Position không resolve đúng 1 Account · venue-bound Account xung đột execution venue khác · broker-bound thiếu `execution_venue_id` · external order ID trùng chỉ phân biệt được khi khác Account/execution-Venue scope · simulated Account phải validate cùng structural contract với live Account.

### Metadata / state

- `ADR-012.md`: **v0.1 → v0.2**, `status` giữ `Draft`. `depends_on: [ADR-007]` không đổi; ADR-007 không bị sửa.
- Reviewer table (§4) vẫn để trống — reviewer identity/concern/risk/recommendation pin tại approval boundary (Chapter 11 §11.6), không bắt buộc trước đó; provenance round review này ghi tại đây.

**Không đóng OQ nào.** Không authorize Live.

## [Unreleased] — 2026-07-28 — candle.md v0.1 → v0.2 — ChatGPT Review A conformance fixes

**Không phải approval.** `candle.md` vẫn `status: Draft`, `reviewers: []`, `approved_by`/`approved_at`/`last_review` giữ `null`. Sửa theo ChatGPT Review A trên baseline v0.1 (1 Major, 2 Minor). Independent Review B / consolidation **chưa diễn ra** — không tuyên bố review evidence hoàn tất ngoài Review A.

### Đã sửa (1 Major) — M-01: canonical event-envelope và subject_ref conformance

- Thêm **§2 Canonical event envelope** — định nghĩa một lần, dùng chung cho `CandleObserved`/`CandleClosed`/`CandleCorrected`/`CandleDataGapObserved`: đủ field bắt buộc theo [Chapter 8 §8.2](./constitution/08-event-model.md) (`event_id`, `event_type`, `event_contract_ref`, `schema_version`, `recorded_time`, `subject_ref`, `stream_ref`, `sequence`, `producer_ref`, `correlation_id` theo điều kiện, `causation_refs`, `related_event_refs`, `effective_time`, `market_time` khi có, `source_identity` khi cần dedup). Mỗi event section giờ tách rõ **envelope inheritance** (câu dẫn) khỏi **`payload:`** (chỉ field đặc thù) — không còn lặp lại field envelope trong từng event.
- Sửa `subject_ref` sang đúng shape canonical Chapter 8 §8.2.2: `{context_id, subject_kind, subject_type, subject_id, scope}` — thay vì tuple trực tiếp trước đó. `subject_id` (`candle_subject_id`) là **opaque, ổn định, deterministic** từ scope, domain logic cấm parse (Chapter 6 §6.8); `scope` giữ field tường minh (instrument/venue/timeframe/window). Không còn tuyên bố "Entity không có identity" — Logical Candle Subject giờ có identity opaque rõ ràng, tách biệt khỏi scope tường minh.
- `causation_refs`: root event (`CandleObserved`/`CandleClosed`/`CandleDataGapObserved`) khai `[]` tường minh; `CandleCorrected` là ngoại lệ duy nhất, bắt buộc không rỗng.

### Đã sửa (Minor m-01) — state-machine/correction consistency

- Chốt đúng **một** semantic: `CandleCorrected` **không** đưa subject ra khỏi `CLOSED` — thêm transition tường minh `CLOSED → CLOSED, caused_by: CandleCorrected` vào `state_machine`. Loại bỏ khả năng đọc "CLOSED không terminal" thành "correction đưa subject sang trạng thái khác".

### Đã sửa (Minor m-02) — authoritative zero-volume provenance

- Thêm 5 điều kiện bắt buộc cho `data_quality: complete_zero_volume` (§11): source/producer xác nhận tường minh · `producer_ref` resolve đúng producer đó · `event_contract_ref` resolve tới contract cho phép semantic này · `source_identity` có mặt khi cần dedup · ingestion adapter không được suy diễn chỉ từ im lặng. Thiếu điều kiện nào → xử lý như gap (`CandleDataGapObserved`), không phát `CandleClosed` tổng hợp.

### Hành vi đã chấp nhận — giữ nguyên, không suy yếu

Append-only provisional history · no-repaint (I-3) · correction là fact mới · phân biệt 3 trường hợp missing-data · không leak exchange-specific field · không giả định 24/7 phổ quát (ADR-007) · canonical Chapter 5 time field (`effective_time`/`recorded_time`/`market_time`, không dùng `event_time`) · `CandleCurrentView` không authoritative (I-12) · Replay/Backtest/Paper/Live parity (I-2).

### Metadata / state

- `candle.md`: **v0.1 → v0.2**, `status` giữ `Draft`, `reviewers: []`, `approved_by`/`approved_at`/`last_review` giữ `null`.
- `README.md`: cập nhật Package 0.2-A ghi nhận `candle.md` v0.2 và ChatGPT Review A đã xử lý; vẫn chưa `Consolidated Stable` (Independent Review B + consolidation còn thiếu); không tuyên bố approve/lock/Phase-0.2-completion.
- `MANIFEST.md`: `manifest_version` **9.26 → 9.27**; dòng `domain/` cập nhật phản ánh v0.2 + Review A đã xử lý.
- `context-map.yaml`, ADR-012, ADR-013: **không đổi**.

**Package 0.2-B vẫn chưa bắt đầu.** Không đóng OQ nào; không authorize Live.

## [Unreleased] — 2026-07-28 — Package 0.2-A Draft — Domain foundation (context-map + candle)

**Không phải approval, không phải Phase 0.2 completion.** Tất cả artifact `status: Draft`. Author self-review hoàn tất; ChatGPT Review A / Independent Review B / consolidation **chưa diễn ra** — chưa đạt `Consolidated Stable`.

- **`docs/domain/context-map.yaml` (mới, v0.1 Draft):** authoritative registry theo [Chapter 4 §4.2](./constitution/04-domain-principles.md) — 6 capability/context: `market-reference/instrument-venue-reference`, `market-data/market-data-observation`, `market-structure/market-structure-analysis` (tên lấy verbatim từ ví dụ Chapter 4 §4.2), `market-regime/raw-regime-analysis`, `feature-engineering/feature-engineering`, `context-aggregation/context-projection` (đổi từ đề xuất `decision-context` để tránh ngụ ý sở hữu Decision semantics). Package 0.2-C (Account/Strategy/Decision/Risk/Execution) **chưa đăng ký** — chờ ADR-012/ADR-013. Chỉ 2 relationship được khai báo (market-data-observation → market-structure-analysis, → raw-regime-analysis), cả hai trích dẫn `CandleClosed` — không khai báo relationship nào trỏ tới contract chưa tồn tại.
- **`docs/domain/candle.md` (mới, v0.1 Draft):** Domain Contract đầu tiên — conformance example. 5 concept: Logical Candle Subject (`kind: entity`, identity = tổ hợp tường minh instrument/venue/timeframe/effective_time, KHÔNG phải opaque ID bị parse) · `CandleObserved`/`CandleClosed`/`CandleCorrected` (`kind: event`, append-only, correction qua `causation_refs` không mutate) · `CandleDataGapObserved` (`kind: event`, optional, không mang OHLC) · `CandleCurrentView` (`kind: read_model`, không authoritative, I-12). Time fields đúng Chapter 5 (`effective_time` interval, `recorded_time`, `market_time` — không dùng `event_time`). Missing-data tách 3 case tường minh (session đóng hợp lệ / session mở không trade / thiếu-trễ-không khả dụng), cấm tự tổng hợp OHLC giả. Dedup qua `source_identity` (Chapter 6 §6.6). Venue-neutral, không hardcode 24/7 (ADR-007); không leak raw exchange field. Cả 4 execution mode dùng chung contract (I-2).
- **`docs/domain/README.md` (cập nhật, v0.2 Draft):** `context-map.yaml` là prerequisite bắt buộc; `candle.md` là conformance example đầu tiên; tách rõ Package 0.2-A/0.2-B/0.2-C; bổ sung Account/Order/Execution/Venue/Instrument/Trade-Intent/Execution-Intent vào 0.2-C (danh sách gốc thiếu); khóa rõ Package 0.2-B **không** được dựa vào authority của 0.2-A cho tới khi 0.2-A đạt `Consolidated Stable` (định nghĩa: author self-review + Review A + Independent Review B + consolidation đều hoàn tất, không còn finding treo); không tuyên bố approval/Lock/Phase-0.2-completion.
- `MANIFEST.md`: `manifest_version` **9.25 → 9.26**; dòng `domain/` cập nhật phản ánh đúng trạng thái Draft hiện tại (không còn "Not Started").

**Package 0.2-B chưa bắt đầu.** Không đóng OQ nào; không authorize Live.

## [Unreleased] — 2026-07-28 — ADR-013 Draft — Strategy Definition Version Authority

**Không phải approval.** ADR mới, `status: Draft` (v0.1), `approved_by`/`approved_at` giữ `null`, `reviewers: []`. Ghi lại nguyên văn Product Owner direction (Kanner, 2026-07-28): Strategy Definition Version là trục evidence bất biến độc lập với Plugin Version/Configuration Version/Package-Build Artifact; Definition Version sở hữu business/decision semantics, Plugin Version sở hữu implementation-release identity; không trục nào proxy trục kia.

- `docs/adr/ADR-013.md` (mới): 4 trục độc lập (Strategy Definition Version · Plugin Version · Configuration Version · Package/Build Artifact), mỗi trục bump riêng; Definition Version sở hữu supported capability/instrument-**class**, KHÔNG sở hữu lựa chọn instrument cụ thể (thuộc Configuration/Instance) — đổi instrument cùng class không bắt buộc version mới, đổi scope/decision-rule/required-input/explanation-contract thì bắt buộc; exact-pin, cấm mutable "latest"; Strategy Instance phải pin đủ cả 4 trục. `depends_on: [ADR-010]` — làm rõ/cấu trúc hóa evidence field "strategy/model version" mà ADR-010 §75 đã yêu cầu nhưng chưa định nghĩa cấu trúc; không supersede, ADR-010 không bị sửa.
- **Không cần review table điền sẵn** — Draft này chưa qua review nào.
- **Không đóng OQ nào** (`addresses: []`, `resolves: []`); §9 ghi rõ chạm nhưng không quyết OQ-002.
- Chặn hoàn thiện Package 0.2-C (Strategy Definition/Instance/Decision Domain Contract); không chặn Package 0.2-A/0.2-B.

## [Unreleased] — 2026-07-28 — ADR-012 Draft — Account-to-Venue Boundary

**Không phải approval.** ADR mới, `status: Draft` (v0.1), `approved_by`/`approved_at` giữ `null`, `reviewers: []`. Ghi lại nguyên văn Product Owner direction (Kanner, 2026-07-28): Account thuộc đúng một Venue/broker boundary; Venue có thể chứa nhiều Account; vốn/exposure liên-venue là Portfolio/Capital Allocation Group projection, không phải multi-venue Account.

- `docs/adr/ADR-012.md` (mới): Account:Venue = N:1; `account_id` vẫn opaque (Ch6 §6.8), `venue_id` là field tường minh riêng, immutable, gán tại tạo Account; đổi venue = tạo Account identity khác; Portfolio/Capital Allocation Group = `read_model`, không phải Account; Order/Fill/Position resolve qua đúng một Account; credential reference scoped 1 venue; simulated Account giữ nguyên shape. `depends_on: [ADR-007]` — mở rộng, không supersede, ADR-007 không bị sửa.
- **Không cần review table điền sẵn** — Draft này chưa qua review nào; bảng Independent reviews để trống theo đúng template.
- **Không đóng OQ nào** (`addresses: []`, `resolves: []`).
- Chặn hoàn thiện Package 0.2-C (Account/Order/Position/Risk Domain Contract); không chặn Package 0.2-A/0.2-B.

## [Milestone] — 2026-07-28 — 🔒 Chapter 14 v1.5 — Product Owner Approve and Lock

**Product Owner decision** (sole approval authority): `Kanner` — *"Approve and Lock Chapter 14 v1.5."* Decision date **2026-07-28**. Claude thực thi đúng quyết định này bằng một atomic governance commit — **không** đưa ra quyết định approval mới, **không** sửa nội dung normative của Chapter 14.

### Pre-lock baseline

- HEAD: `4c5f9592c9c646f505ff828975db6c90e5d2f7fe`
- Chapter 14 candidate blob: `2dc6a0bfd1357700158ad5a9877dc345ca95c517` (v1.5, `In Review`)

### Review evidence hoàn tất trên baseline v1.5

- ChatGPT Review A: `0 / 0 / 0 / 0`, Backward Consistency Check `No conflict`.
- Independent GPT Review B (actor riêng): `0 / 0 / 0 / 0`, Backward Consistency Check `No conflict`, verdict `Ready for consolidation`.
- ChatGPT consolidation: clean, không có finding nào qualify.
- Claude Independent Final Challenge (session riêng biệt với revision author): `0 / 0 / 0 / 0`, Backward Consistency Check `No conflict`, verdict `Consolidated clean result confirmed with non-blocking observations`.
- ChatGPT Final Disposition: `No qualifying findings` · `No conflict` · `No ADR required` · `Ready for Product Owner Decision`.

### Content disposition

- Chapter 14 version **giữ nguyên v1.5** — Lock không bump version.
- **Không cần ADR.**
- **Không** sửa Chapter 0–13 (Chapter 13 blob không đổi: `4bb697f3b43b0874a080015ef0ce6ca53de729f4`).
- **Không** đóng OQ-002/OQ-003 — cả hai vẫn `Open`.
- **Không** authorize Live ở bất kỳ hình thức nào.
- **Chapter 14 Lock không tự động hoàn tất Phase 0 Approval Gate** — Phase 0 còn sub-phase 0.2 (Domain Model & Domain Contract) và 0.3 (Product Requirement/Use Case/UX Blueprint) chưa thực hiện.

### State changes

- `constitution/14-roadmap.md`: `status: In Review → Locked`, `approved_by: Kanner`, `approved_at: "2026-07-28"`. Version giữ **1.5**; toàn bộ normative body byte-identical, chỉ frontmatter lifecycle field đổi.
- `MANIFEST.md`: `manifest_version` **9.24 → 9.25**; Chapter 14 row → `1.5 · Locked`; overview line cập nhật **Chapter 0–14 Locked** (Constitution full-locked); Chapter 0–13 rows, ADR lifecycle, OQ state, project version không đổi.

## [Unreleased] — 2026-07-28 — Chapter 14 (Roadmap) v1.4 → v1.5 — make recording boundary atomic

**Không phải approval.** Revision của chapter đang `In Review`; **không** Approve/Lock, `approved_by`/`approved_at` giữ `null`. Claude là **revision author + self-reviewer** (`AI Technical Architect`) — **không** phải Product Owner. **Không phải independent-review evidence**: v1.5 **chưa** qua ChatGPT Review A, Independent Review B, hay Claude Independent Final Challenge.

### Consolidated input đã nhận (baseline v1.4, HEAD `716624a1bd6caa7beea2f1f2772487386b3b006c`)

- ChatGPT Review A: 0/0/0/0, verdict `Ready for Independent Review B`. Independent GPT Review B (không thấy Review A): 0/1/0/0. Consolidation: **1 Major (C4-01)**, Backward Consistency Check `Revision required`.

### Finding challenge

| Finding | Disposition | Evidence |
|---|---|---|
| C4-01 | **Confirm** | v1.4 §14.4.1 liệt `resulting MANIFEST transition identity/version` là field bundle phải pin để "complete"; §14.4.2 lại bắt bundle complete **rồi mới** ghi MANIFEST transition. Vòng tròn: transition identity chưa tồn tại trước khi transition được ghi, nên bundle không bao giờ complete được theo đúng nghĩa đen — hai validator conforming có thể diverge (một validator suy ra phải precompute/guess transition identity, một validator suy ra bundle vĩnh viễn incomplete) |

Major sống → tiến hành revision v1.5.

### Recording model đã chọn: atomic boundary (không phải sequential)

Thay mô hình sequential `bundle complete → rồi ghi MANIFEST transition` bằng **atomic boundary**: `resulting MANIFEST transition identity` bị tách khỏi **prepared bundle content** — nó **không** phải thứ cần resolve trước, mà là thứ **được sinh ra chính tại** atomic recording boundary, đồng thời với chính bundle. Trước boundary: mọi field khác (Phase/Roadmap/DoD/gate-set identity, PO acceptance, deliverable evidence, Quality Gate result, BCC, validator/freshness, review evidence, PO decision fact) đã "prepared" nhưng **chưa authoritative**. Tại boundary: bundle (giờ pin cả transition identity) và MANIFEST transition **cùng** trở thành authoritative — không cái nào authoritative một mình, không có "trước/sau" giữa hai cái. Cấm mọi convention "đoán trước" transition identity.

### Đã sửa

- **§14.4.1:** tách bundle thành 3 lớp: prepared content thuộc Chapter 14, prepared content chỉ reference chapter khác, và **resulting MANIFEST transition identity — không thuộc prepared content**, chỉ authoritative tại boundary.
- **§14.4.2 (viết lại):** sequencing cũ (`bundle complete → ghi MANIFEST`) thay bằng atomic model: `eligibility complete (Ch12, không đổi) → PO decision (fact) → prepared content sẵn sàng (trừ transition identity) → ATOMIC BOUNDARY (bundle + MANIFEST transition activate cùng lúc) → Phase kế tiếp được phép bắt đầu`. Thêm: partial success (chỉ 1 trong 2 ghi được) → non-authoritative, current Phase giữ nguyên, remediation/retry; retry sau uncertain failure phải cho đúng một authoritative completion (semantic requirement, không kê đơn transaction/database/lock/2PC); post-boundary corruption vẫn là integrity violation (không đổi so với v1.4).
- §14.5 (bảng authority): "authoritative recording boundary (sequencing)" → "(atomic sequencing)".

### Author self-review (8 attacks + Locked-authority consistency)

- **Attack A (circular transition reference):** không còn — transition identity không phải prepared content, không cần resolve trước (§14.4.1, §14.4.2).
- **Attack B (đoán trước future identity):** cấm tường minh; guess không tự thiết lập authority (§14.4.2).
- **Attack C (bundle ghi được, MANIFEST fail):** non-authoritative, current Phase giữ nguyên, remediation (§14.4.2).
- **Attack D (MANIFEST ghi được, bundle fail):** non-authoritative, không next-Phase, remediation (§14.4.2).
- **Attack E (duplicate retry):** yêu cầu đúng một authoritative completion, semantic-only, không kê đơn cơ chế (§14.4.2).
- **Attack F (hai validator):** cùng đồng ý prepared-state, boundary completion, current Phase, next-Phase permission — rule deterministic ở mọi bước.
- **Attack G (historical audit sau khi Roadmap/DoD đổi):** vẫn deterministic — bundle giữ nguyên đúng version đã pin tại boundary cũ (§14.1.1, §14.3.1, §14.4.1).
- **Attack H (post-recording corruption):** integrity violation, không tự đảo ngược, không thay bằng current state (không đổi từ v1.4).
- **Locked-authority consistency:** đối chiếu Chapter 0, I-12, Chapter 11, Chapter 12 (§12.2 prerequisite list không đổi), Chapter 13 (§13.9 chỉ reference), ADR-011, MANIFEST — không phát hiện redefinition; không tạo Approval Gate/veto mới; không kê đơn database/transaction/CI vendor cụ thể.

**Author self-assessment: addressed; pending independent review.**

### Metadata / state

- `constitution/14-roadmap.md`: **v1.4 → v1.5**, status giữ `In Review`, `approved_by`/`approved_at` giữ `null`, `last_review` giữ `2026-07-28`. `depends_on` giữ nguyên.
- `MANIFEST.md`: row Chapter 14 → **v1.5**; `manifest_version` **9.23 → 9.24**; Chapter 0–13 giữ `Locked` (Chapter 13 vẫn `1.7 · Locked`, blob không đổi); Domain README không đổi; OQ-002/OQ-003 vẫn `Open`.

### ADR

**Không cần ADR** — fix nằm trong authority Chapter 14 đã tự nhận; không sửa Chapter 0–13; không thêm prerequisite mới vào Chapter 12 §12.2; không tạo Approval Gate hay veto mới; không kê đơn implementation.

### Next

`Chapter 14 v1.5 — In Review — ready for ChatGPT Review A`. Không pre-assert kết quả review hay Product Owner approval.

## [Unreleased] — 2026-07-28 — Chapter 14 (Roadmap) v1.3 → v1.4 — complete recording authority

**Không phải approval.** Revision của chapter đang `In Review`; **không** Approve/Lock, `approved_by`/`approved_at` giữ `null`. Claude là **revision author + self-reviewer** (`AI Technical Architect`) — **không** phải Product Owner. **Không phải independent-review evidence**: v1.4 **chưa** qua ChatGPT Review A, Independent Review B, hay Claude Independent Final Challenge.

### Consolidated input đã nhận (baseline v1.3, HEAD `c4f3364802062385407109207c1a22255387e21d`)

- ChatGPT Review A: 0/1/0/0. Independent GPT Review B: 0/2/0/0. Consolidation: **2 Major (C3-01, C3-02)**, Backward Consistency Check `Revision required`.

### Author challenge

| Finding | Disposition | Ghi chú |
|---|---|---|
| C3-01 | **Confirm** | §14.3.1 v1.3 nói DoD "incorporate bằng exact immutable reference" nhưng không khóa **ai** được tạo record đó — một actor bất kỳ có thể tự publish một immutable-reference record tuyên bố incorporate, không có authority root để validator reject |
| C3-02 | **Confirm** | §14.4.1 v1.3 nói rõ ràng bundle không resolve được **"không tự tạo gate/veto mới chặn phase transition đã xảy ra"** — đọc đúng nghĩa đen cho phép decision → MANIFEST transition → Phase kế tiếp bắt đầu dù bundle chưa complete |

Cả hai Major sống → tiến hành revision v1.4.

### Đã sửa — Author self-assessment: addressed; pending independent review

- **C3-01 → §14.3.1 (sửa):** thêm **canonical incorporation establishment** — incorporation **không phải registry riêng**, mà là **một phần của chính Product Owner acceptance evidence** (§14.3): cùng evidence phải xác định Phase identity + Roadmap phase-section version + DoD version/content + explicit incorporation decision, tồn tại trước gate, đúng một resolve. Không có con đường nào khác tạo incorporation hợp lệ; validator chỉ kiểm tra record có nằm trong đúng PO acceptance evidence hay không, không tự suy diễn/tạo. Dùng nguyên tắc *identity + authority + prior establishment + independent resolvability* — **không** copy nguyên khối canonical establishment predicate của Chapter 13 §13.4.1, vì Chapter 14 đã có sẵn authority đơn giản hơn (Product Owner, Chapter 0) không cần một chain designation riêng.
- **C3-02 → §14.4.1 (sửa 1 câu) + §14.4.2 (mới):** bỏ câu gây hiểu nhầm "không chặn phase transition đã xảy ra"; thêm **Authoritative recording boundary** khóa trình tự: `eligibility complete (Ch12, không đổi) → PO decision (fact) → bundle complete/pinned (= recording boundary) → MANIFEST transition → Phase kế tiếp được phép bắt đầu`. MANIFEST transition **không được ghi** trước khi bundle complete; failure trước boundary = `recording incomplete` (khác họ với PO rejection/reviewer veto, current Phase giữ nguyên, retry, PO không phải quyết lại); mất evidence **sau** khi đã ghi hợp lệ = `integrity violation` (không tự đảo ngược quyết định, không thay lịch sử bằng current state). Không tạo Approval Gate thứ hai, không tạo veto mới, không đổi prerequisite list của Chapter 12 §12.2.
- §14.5 (bảng authority) và §14.6 (defer list) cập nhật để liệt kê 2 concern mới (incorporation establishment, recording boundary/persistence mechanism).

### Author self-review (7 attacks + Locked-authority consistency)

- **Attack A (self-certified incorporation):** invalid — record không nằm trong PO acceptance evidence (§14.3.1).
- **Attack B (accept nhưng không incorporation tường minh):** không canonical, fail-closed (§14.3.1 điều kiện 2).
- **Attack C (hai PO-incorporation record xung đột):** multiple/conflicting → fail-closed, không precedence (§14.3.1).
- **Attack D (PO quyết nhưng persistence fail):** không MANIFEST transition, Phase kế tiếp không bắt đầu, decision không tự thành rejection, retry recording (§14.4.2).
- **Attack E (MANIFEST ghi trước bundle complete):** partial recording, không phải authoritative transition, không kích hoạt Phase kế tiếp (§14.4.2).
- **Attack F (evidence hỏng sau khi đã ghi hợp lệ):** integrity violation, không tự đảo ngược, không thay bằng current state (§14.4.2).
- **Attack G (hai validator, cùng pinned evidence):** rule deterministic ở mọi bước → cùng kết luận (incorporation, gate set, recording completion, next-phase permission).
- **Locked-authority consistency:** đối chiếu Chapter 0 (PO authority), I-12, Chapter 11 (validator), Chapter 12 (orchestration/prerequisite list §12.2 giữ nguyên, không thêm điều kiện), Chapter 13 (evidence semantics §13.9 chỉ reference), ADR-011, MANIFEST (current-state authority) — không phát hiện redefinition.

**Author self-assessment: addressed; pending independent review.**

### Metadata / state

- `constitution/14-roadmap.md`: **v1.3 → v1.4**, status giữ `In Review`, `approved_by`/`approved_at` giữ `null`, `last_review` giữ `2026-07-28`. `depends_on` giữ nguyên.
- `MANIFEST.md`: row Chapter 14 → **v1.4**; `manifest_version` **9.22 → 9.23**; Chapter 0–13 giữ `Locked` (Chapter 13 vẫn `1.7 · Locked`, blob không đổi); OQ-002/OQ-003 vẫn `Open`.

### ADR

**Không cần ADR** — cả hai fix nằm trong authority Chapter 14 đã tự nhận (§14.1/§14.5); không sửa Chapter 0–13; không thêm prerequisite mới vào Chapter 12 §12.2; không tạo Approval Gate hay veto mới.

### Next

`Chapter 14 v1.4 — In Review — ready for ChatGPT Review A`. Không pre-assert kết quả review hay Product Owner approval.

## [Unreleased] — 2026-07-28 — Chapter 14 (Roadmap) v1.2 → v1.3 — resolve phase-plan authority

**Không phải approval.** Revision của chapter đang `In Review`; **không** Approve/Lock, `approved_by`/`approved_at` giữ `null`. Claude là **revision author + self-reviewer** (`AI Technical Architect`) trong nhịp này — **không** phải Product Owner. Đây **không phải independent-review evidence**: v1.3 **chưa** qua bất kỳ independent review nào (ChatGPT Review A / Independent Review B / Claude Independent Final Challenge đều **chưa xảy ra** cho baseline v1.3).

### Consolidated input đã nhận (baseline v1.2, HEAD `242c566a2160b853babe5f10117d08e985a5c85c`)

- ChatGPT Review A: 0/1/0/0. Independent GPT Review B: 0/3/1/0. ChatGPT consolidation: **3 Major (C-01, C-02, C-03) · 1 Minor (C-04)**, Backward Consistency Check `Revision required`.

### Author challenge (trước khi sửa)

| Finding | Disposition | Ghi chú |
|---|---|---|
| C-01 | **Confirm** | Locked Chapter 12/13 dùng cụm "approved phase plan/roadmap" — v1.2 không khóa "phase plan" là gì so với "roadmap", không có exactly-one resolution rule |
| C-02 | **Confirm** | v1.2 §14.4 để DoD khai gate set trực tiếp nhưng không khóa **incorporation** — bridge nối DoD → canonical Phase-plan declaration còn thiếu |
| C-03 | **Partially confirm, reclassify (thu hẹp scope)** | Gap về audit trail là thật, nhưng danh sách field gốc (BCC result, validator result, review evidence, PO decision boundary) thuộc authority Chapter 12/13/11/0 — Chapter 14 chỉ pin phần thuộc chính nó (Phase/Roadmap/DoD/gate-set identity) và **reference** (không redefine) phần còn lại, tránh đè lên "Phase approval orchestration" mà chính §14.5 đã giao cho Chapter 12 |
| C-04 | **Confirm** | `docs/domain/README.md` dòng cuối còn "Approve 3/3" — stale so với governance hiện hành (ADR-011) |

Có Major sống (C-01, C-02) → tiến hành revision v1.3.

### Đã sửa — Author self-assessment: addressed; pending independent review

- **C-01 → §14.1.1 (mới):** khóa **canonical Phase-plan model** — không tồn tại "Phase plan" như artifact type riêng cạnh Roadmap; canonical Phase plan = phần Phase tương ứng trong Roadmap + accepted DoD đã incorporate; exactly-one resolution, fail-closed khi zero/multiple, không precedence ngầm, historical decision không resolve lại từ bản hiện tại. Chấm dứt đệ quy tại chính Roadmap + Product Owner DoD-acceptance (Decision Workflow, Chapter 0 §3) — không tạo authority registry mới.
- **C-02 → §14.3.1 (mới):** khóa **DoD incorporation** — DoD không phải Phase-plan cạnh tranh; incorporation là hành vi tường minh (exact immutable reference); gate-set declaration của DoD đã incorporate = declaration của canonical Phase plan (đúng authority bridge mà Ch12 §12.2(5)/Ch13 §13.12 cần); PO acceptance cần evidence boundary tường minh, không suy từ publish; zero/multiple/conflicting declaration → fail-closed; historical immutability khi DoD version đổi.
- **C-03 (thu hẹp) → §14.4.1 (mới):** khóa **Immutable Phase-decision bundle** — tách rõ field Chapter 14 pin trực tiếp (Phase identity, Roadmap version, DoD version, gate-set declaration) khỏi field chỉ **reference** tới evidence contract đã có sẵn ở Chapter 0/11/12/13 (không redefine nội dung/format của chúng); phân biệt `current state → MANIFEST` vs `historical decision → immutable bundle`.
- **C-04 → `docs/domain/README.md`:** thay "Approve 3/3" bằng tham chiếu Chapter 0 §3 hiện hành (hai independent review, Product Owner quyết) + ADR-011; không thêm rule mới, không rewrite phần còn lại.
- §14.5 (authority boundary table) và §14.6 (defer list) cập nhật để liệt kê 3 concern mới là authority của Chapter 14 và defer đúng storage/format của bundle.

### Author self-review (6 attack scenarios + 2 consistency checks)

- **Attack 1 (competing Phase plans):** không còn khả năng — "Phase plan" không phải artifact type có authority ngoài Roadmap+DoD (§14.1.1).
- **Attack 2 (accepted DoD chưa incorporate):** gate declaration bên trong **invalid** cho tới khi incorporate (§14.3.1).
- **Attack 3 (Phase plan khai G1, DoD khai G2):** không thể phát sinh — chỉ DoD là nguồn declare gate set (§14.4); §14.3.1 vẫn khóa fail-closed cho multiple/conflicting declaration làm defense-in-depth.
- **Attack 4 (DoD v2 thành current):** historical decision vẫn resolve đúng DoD v1 đã pin tại boundary (§14.3.1, §14.4.1).
- **Attack 5 (thiếu PO-acceptance evidence):** DoD không canonical, eligibility incomplete (§14.3.1, §14.3).
- **Attack 6 (hai validator, cùng pinned evidence):** rule deterministic, không có lựa chọn ngầm ở bất kỳ bước nào → cùng kết quả.
- **Locked-authority consistency:** đối chiếu Chapter 0, I-12, Chapter 7, Chapter 11, Chapter 12, Chapter 13, ADR-011, MANIFEST — không phát hiện redefinition; mọi authority ngoài Chapter 14 chỉ được **tham chiếu**.
- **Scope:** chỉ 4 file được sửa; không Locked chapter nào bị đổi; không ADR (không chapter Locked nào bị chạm, không đổi governance/approval process — chỉ hoàn thiện delegation Chapter 14 đã được giao); không dependency cycle; không đóng OQ; Phase sequence/gate/0.1–0.3/Phase 1.5 giữ nguyên.

**Author self-assessment: addressed; pending independent review.** Đây là đánh giá của chính revision author, **không** phải kết luận đã được xác nhận độc lập.

### Metadata / state

- `constitution/14-roadmap.md`: **v1.2 → v1.3**, status giữ `In Review`, `approved_by`/`approved_at` giữ `null`, `last_review` giữ `2026-07-28`. `depends_on` giữ nguyên (00→13, không cycle).
- `docs/domain/README.md`: sửa 1 câu (C-04), không đổi frontmatter/status (`Not Started`).
- `MANIFEST.md`: row Chapter 14 → **v1.3**; `manifest_version` **9.21 → 9.22**; Chapter 0–13 giữ `Locked` (Chapter 13 vẫn `1.7 · Locked`); OQ-002/OQ-003 vẫn `Open`; không close backlog nào.

### ADR

**Không cần ADR** — mọi fix nằm trong authority Chapter 14 đã tự nhận ở §14.1/§14.5 (phase sequence, DoD, gate-set declaration) cộng phần defer sang reference-only cho C-03; không sửa Locked chapter; không đổi governance/approval process.

### Next

`Chapter 14 v1.3 — In Review — ready for ChatGPT Review A`. Không pre-assert kết quả review hay Product Owner approval.

## [Unreleased] — 2026-07-28 — Chapter 14 (Roadmap) v1.1 → v1.2 — close Chapter 12/13 delegation gaps

**Không phải approval.** Revision của chapter đang `In Review`; **không** Approve/Lock, `approved_by`/`approved_at` giữ `null`. Claude là **author/self-reviewer** (`AI Technical Architect`) trong nhịp này — **không** phải Product Owner, **không** pre-assert independent review, **không** pre-assert Product Owner approval. Chapter 14 v1.2 **chưa** qua review độc lập nào.

### Review provenance

- **Nguồn:** Claude authoring review trên baseline `fa71156606a6c274d2415ce6ac124a321c137bde` (Chapter 14 v1.1, blob `70b4955f8f562d69b5b6dd4d4d534ff4d68faea9`), thực hiện **sau khi** Chapter 13 v1.7 Locked — đây là lần đối chiếu đầu tiên của Chapter 14 với Chapter 13 ở trạng thái Locked.
- **Backward Consistency Check ([Chapter 12 §12.4-A](./constitution/12-approval-gates.md)):** phát hiện **conflict với Locked authority** → `Revision required`.
- **Severity count:** **1 Blocker · 4 Major · 3 Minor · 0 Suggestion.**
- Đây là **một** review từ **một** actor identity (`Claude`). [Chapter 0 §3](./constitution/00-governance.md) yêu cầu tối thiểu **hai** independent review từ hai actor identity khác nhau trước Product Owner decision — điều kiện đó **chưa** thỏa.

### Đã sửa (1 Blocker) — B-01: Phase 5–9 không có Approval Gate, mâu thuẫn Chapter 12 (Locked)

- Chapter 12 (Locked) mở đầu: *"Mọi Phase kết thúc bằng một cổng phê duyệt trước khi Phase kế tiếp bắt đầu — không được nhảy phase."* Chapter 14 v1.1 chỉ đánh dấu Approval Gate ở Phase 0, 1, 1.5, 2, 3, 4 — **Phase 5 (Integration), 6 (Simulation Platform), 7 (Deployment), 8 (Research Platform), 9 (Observability) hoàn toàn không có gate**.
- Sửa: §14.2 khai báo Approval Gate cho **mọi** Phase, không ngoại lệ; thêm câu dẫn tham chiếu Chapter 12 (tham chiếu, **không** định nghĩa lại).

### Đã sửa (4 Major)

- **M-01 — Phase 0.2 được Locked authority tham chiếu nhưng Roadmap không định nghĩa.** `Phase 0.2` xuất hiện ở [Chapter 6 §6.4](./constitution/06-identity-model.md) (Account first-class scope), [Chapter 7 §7.5](./constitution/07-module-taxonomy.md) (module-registry placement), `MANIFEST` (domain/ status, BL-004) và `domain/README.md` — nhưng Chapter 14 v1.1 không có sub-phase nào. Roadmap là owner của phase sequence → sub-phase load-bearing phải được định nghĩa tại đây. Sửa: §14.2 định nghĩa Phase 0.1/0.2/0.3; §14.1 khóa rõ **sub-phase không tự mở Approval Gate**, `Phase 1.5` là Phase đầy đủ (giữ nguyên gate như v1.1) — tránh nhân bản gate ngoài ý Chapter 12.
- **M-02 — delegation DoD từ Chapter 12 bị bỏ trống.** [Chapter 12 §12.3](./constitution/12-approval-gates.md) chỉ định Chapter 14 là intended owner của *"Phase-specific sequence & DoD content"*, và §12.2(1) yêu cầu DoD đã định nghĩa/chấp nhận làm prerequisite. Chapter 14 v1.1 **không có một dòng nào** về DoD → prerequisite không có nguồn resolve. Sửa: thêm **§14.3** — cardinality (đúng một authoritative DoD artifact mỗi Phase), tồn tại trước gate, resolvable + versioned/pinned, fail-closed khi thiếu, không tạo state store cạnh tranh MANIFEST. Chapter 14 **không** định nghĩa lại DoD rule của §12.1.
- **M-03 — delegation quality-gate từ Chapter 13 bị bỏ trống.** [Chapter 13 §13.12](./constitution/13-quality-gates.md) (vừa Locked) khai báo *"Phase deliverable → gate set mà approved phase plan/roadmap (Chapter 14) khai báo áp dụng"* — Chapter 14 v1.1 không khai báo gì. Sửa: thêm **§14.4** — gate set cho phase deliverable khai báo trong DoD artifact của chính Phase đó, resolvable trước gate, fail-closed khi không khai báo được; trigger A–E cấp artifact vẫn thuộc Chapter 13.
- **M-04 — Quality Gate hiển thị như chỉ tồn tại ở Phase 3.** v1.1 đặt `Quality Gate theo Tier` duy nhất dưới Phase 3, đọc thành "các Phase khác không có quality gate" — mâu thuẫn [Chapter 12 §12.2(5)](./constitution/12-approval-gates.md) (applicable quality gates phải PASS ở **mọi** phase approval). Sửa: §14.4 khóa rõ dòng đó là **nhấn mạnh giai đoạn build module**, không phải giới hạn phạm vi; nhắc lại `Quality Gate ≠ Approval Gate`.

### Đã sửa (3 Minor)

- **m-01 — parity ở Phase 6 mơ hồ với parity gate cấp module.** *"Kiểm chứng Parity Principle (I-2) tại đây"* đọc thành parity chỉ được verify ở Phase 6, trong khi [Chapter 13 §13.4/§13.6](./constitution/13-quality-gates.md) bắt buộc Parity Test cho Tier 1 ngay tại Phase 3. Sửa: ghi rõ Phase 6 là parity **cấp platform**, **không** thay thế parity test cấp module ở Phase 3.
- **m-02 — mô tả AI Layer dùng thuật ngữ transport.** Ghi chú cuối v1.1 nói AI Layer là *"consumer mới của Event Bus"*, trong khi [Chapter 9 §9.2](./constitution/09-plugin-model.md) (Locked) cấm mô tả plugin theo transport và khóa rằng authority nằm ở published contract, không phải broker. Sửa: đổi thành *"consumer mới của published contract"*; giữ nguyên phần còn lại của ghi chú.
- **m-03 — `last_review` stale.** v1.1 giữ `2026-07-16`, viết trước khi Chapter 8–13 đạt version Locked hiện tại. Sửa: `last_review: 2026-07-28`.

### Thêm mới (structural)

- **§14.1 Phạm vi và thẩm quyền** + **§14.5 Authority boundary table** — khóa rõ Chapter 14 sở hữu gì và tham chiếu gì, tránh competing authority với Chapter 7/12/13 và MANIFEST.
- **§14.6 Ngoài phạm vi** — defer storage/format của DoD artifact và gate-set declaration; ghi rõ **không** đóng OQ-002/OQ-003 (Phase 6 có Paper Trade và Phase 7 có Deployment **không** đồng nghĩa "được phép lên Live").

### Metadata / state

- `constitution/14-roadmap.md`: **v1.1 → v1.2**, status giữ `In Review`, `approved_by`/`approved_at` giữ `null`, `last_review` → `2026-07-28`. `depends_on` **giữ nguyên** danh sách 00→13 (không thêm/bớt; không chapter nào depends_on 14 → không tạo cycle).
- `MANIFEST.md`: row Chapter 14 → **v1.2**; `manifest_version` **9.20 → 9.21**; `constitution_version` giữ **1.1.0**; Chapter 0–13 giữ `Locked`; OQ-002/OQ-003 vẫn `Open`; không close backlog nào.

### ADR

**Không cần ADR** — mọi thay đổi nằm trong authority sẵn có của Chapter 14 (phase sequence, phase content, DoD content/location, gate-set declaration). Không sửa Locked chapter nào; các fix **căn chỉnh Chapter 14 về đúng** Chapter 12/13 đã Locked chứ không thay đổi chúng. Không mở rộng authority Chapter 6/7/9/12/13; MANIFEST không trở thành registry mới.

### Next

`Chapter 14 v1.2 — In Review — cần tối thiểu hai independent review (Chapter 0 §3) trước Product Owner decision.` Không pre-assert kết quả review hay approval.

## [Unreleased] — 2026-07-28 — Chapter 13 v1.7 approved and locked

### Decision

- **Product Owner:** `Kanner`.
- **Decision:** `APPROVED AND LOCKED`.
- Chapter 13 version giữ **v1.7** (không bump); `status`: `In Review → Locked`.
- **Approval timestamp:** `2026-07-28T10:14:34+07:00`.
- Đây **không** phải quyết định của ChatGPT hoặc Claude — Claude chỉ ghi nhận quyết định Product Owner đã có vào repository.

### Exact decision baseline

- HEAD trước decision: `993d796e1850429771b92e80dc47699b13a1ef75`
- Chapter 13 blob trước decision: `be3052c792e56c2beb69bc655291ee4173a77805`
- MANIFEST trước decision: `9.19`

### Review evidence accepted

- ChatGPT Review A: `0 / 0 / 0 / 0`.
- Independent GPT Review B: `Confirm Review A` — `0 / 0 / 0 / 0`.
- ChatGPT consolidation: no surviving findings — `0 / 0 / 0 / 0`.
- Claude Independent Final Challenge: `Consolidated result confirmed` — `0 / 0 / 0 / 0`.
- Backward Consistency Check ([Chapter 12 §12.4](./constitution/12-approval-gates.md)): `No conflict`.

### Content disposition

- **M-01-R** — closed (v1.7).
- **M-03** — closed (v1.7).
- Không còn finding nào tồn đọng.
- **Không cần ADR.**
- Không có Locked chapter nào khác bị sửa.
- Không có dependency cycle mới.
- Không có lifecycle drift.
- **Không** đóng OQ-002 hoặc OQ-003.
- Chapter 14 **giữ nguyên** `In Review` — không chạm.

### State changes

- `constitution/13-quality-gates.md`: **v1.7**, `status: In Review → Locked`, `approved_by: Kanner`, `approved_at: "2026-07-28T10:14:34+07:00"`. Normative body không đổi; chỉ đồng bộ status prose đầu chương.
- `MANIFEST.md`: `manifest_version` **9.19 → 9.20**; Chapter 13 row → `1.7 · Locked`; overview line cập nhật **Chapter 0–13 Locked, Chapter 14 In Review**. `constitution_version` giữ **1.1.0**; Chapter 0–12 entries, Chapter 14 version/status, ADR states, OQ-002/OQ-003, dependency graph — tất cả giữ nguyên.

## [Unreleased] — 2026-07-27 — Chapter 13 (Quality Gates) v1.6 → v1.7 — close tier authority bypasses (M-01-R, M-03)

**Không phải approval/lock.** Revision của chapter đang `In Review`, thực hiện theo yêu cầu Product Owner dựa trên consolidated finding v1.6. **Không** Approve/Lock, `approved_by`/`approved_at` giữ `null`. Claude là **revision author** (`AI Technical Architect`) trong nhịp này — **không** phải Product Owner, **không** tự tuyên bố revision v1.7 đã pass review.

### Review provenance (boundary v1.6 — consolidated trước khi revision này bắt đầu)

- **Final consolidated finding count:** **0 Blocker · 2 Major (M-01-R, M-03) · 0 Minor · 0 Suggestion.**
- **Verdict:** `Revision required`.
- **m-01** (overlapping/nested scopes) — **rejected as separate finding**, không mở lại/không xử lý riêng trong revision này.

### Đã sửa (Major — M-01-R) — canonical tier-designation authority thiếu establishment predicate (§13.4.1)

- Thêm **Canonical establishment predicate** (dùng chung §13.4.1/§13.4.2): một designation/authority chỉ **canonical** khi (1) established qua **Decision Workflow** ([Chapter 0 §3](./constitution/00-governance.md)) đúng ADR Scope Rule khi thuộc diện đó, **và** (2) recorded tại một authoritative project state resolvable độc lập với chính declaration chain của subject — không phải artifact do chính producer tự publish cùng lúc.
- Predicate **terminating**: bottom-out tại Product Owner decision (Chapter 0 §3, primitive authority đã Locked) — không tạo "designation của designation" mới, không infinite regress. Cùng anchor pattern mà [Chapter 10 §10.4.3(4)](./constitution/10-compatibility-capability-contract.md) (Locked) đã dùng cho Compatibility Policy authority — tham chiếu, không định nghĩa lại.
- Đóng đúng failure scenario: producer tự tạo designation D rồi tự cho D quyền authorize chính mình → D không thỏa cả 2 điều kiện → không canonical → `FAIL — evidence`.

### Đã sửa (Major — M-03) — nhánh 2 (owned executable artifact) thiếu authority contract cho ownership binding (§13.4.2 mới)

- Thêm **§13.4.2 — Canonical ownership-binding authority**: ownership relationship (artifact → owning module) là **authority-bearing fact**; đúng một canonical ownership-binding authority phải resolve cho scope áp dụng; ownership declaration **không** tự tạo ownership authority; producer/owner không tự chọn module có lợi chỉ bằng publish declaration.
- Canonical status của ownership-binding authority dùng **chung Canonical establishment predicate** ở §13.4.1 — không duplicate.
- Ownership-binding chain: canonical authority designation → authorized declaration/binding → exact owning-module identity → inherited tier → floor/gates → evaluation → immutable evidence.
- Authority boundary: layered on top of Chapter 7 module identity/taxonomy, **không** định nghĩa lại `module-registry.yaml` hay Chapter 7.

### Cross-branch consistency

- Thêm đoạn **Cross-branch authority parity** (§13.4): cả 3 nhánh (runtime module / owned artifact / standalone artifact) giờ có bảo vệ tương đương — mỗi nhánh có authoritative identity + mapping/binding riêng, đều fail-closed khi unresolved. Xác nhận **không** có quy tắc "most-specific-wins" hay ưu tiên ngầm giữa các nhánh — giữ nguyên hành vi cũ (đúng một authority áp dụng, zero/multiple đều fail-closed).

### §13.9 refined (không duplicate Chapter 10)

- **Ownership provenance** (nhánh 2) mở rộng đủ field: canonical ownership-authority identity/version/scope/owner-basis · exact ownership declaration identity · identity actor được authorize bind · exact artifact identity/version · canonical owning-module identity · exact `module-registry` entry/version · applicable-tại-boundary evidence.
- **Standalone bullet** (nhánh 3) thêm field **canonical-establishment evidence** — reference chứng minh designation thỏa establishment predicate.
- **Validator sentence** hợp nhất reject-list cho cả hai authority: self-established designation/ownership authority · unauthorized classifier/binder · zero/multiple applicable authority · expired/future/out-of-scope · mutable/unresolved reference · authority chain phụ thuộc current state khi validate historical evidence → tất cả `FAIL — evidence`.
- **Historical-immutability sentence** mở rộng gồm ownership authority/binding (không chỉ designation/tier/registry/policy như v1.6).

### Metadata / state

- `constitution/13-quality-gates.md`: **v1.6 → v1.7**, status giữ `In Review`, `approved_by`/`approved_at` giữ `null`. `depends_on` giữ nguyên `["02-platform-invariants", "07-module-taxonomy"]`.
- `MANIFEST.md`: row Chapter 13 → **v1.7**; `manifest_version` **9.18 → 9.19**; `constitution_version` giữ **1.1.0**; Chapter 0–12 giữ `Locked`, Chapter 14 giữ `In Review`; OQ-002/OQ-003 vẫn `Open`; không close backlog khác.

### ADR

**Không cần ADR** — cả hai finding đóng trong authority sẵn có của Chapter 13, chỉ **tham chiếu** (không định nghĩa lại) Chapter 0 §3 Decision Workflow và Chapter 10 §10.4.3(4) pattern; không sửa Locked chapter; không mở rộng authority Chapter 7/9/10/12; MANIFEST không trở thành runtime tier/ownership registry mới.

### Next

`Chapter 13 v1.7 — In Review — ready for exact-baseline Review A`. Revision này **chưa** qua review — không pre-assert kết quả review v1.7 hay Product Owner approval.

## [Unreleased] — 2026-07-27 — Chapter 13 (Quality Gates) v1.5 → v1.6 — tier-designation authority root (M-01)

**Không phải approval.** Revision của chapter đang `In Review`, thực hiện theo yêu cầu Product Owner dựa trên consolidated review evidence cho boundary v1.5. **Không** Approve/Lock, `approved_by`/`approved_at` giữ `null`. Claude là **revision author** (`AI Technical Architect`) trong nhịp này — **không** phải Product Owner, **không** tự tuyên bố revision v1.6 đã pass review, **không** tự đóng review eligibility cho v1.6.

### Review provenance (boundary v1.5 — consolidated trước khi revision này bắt đầu)

- Consolidated source: **ChatGPT review package + Claude independent review (phiên độc lập) + ChatGPT consolidation**.
- **Product Owner interpretation:** Claude review trong session độc lập được tính là **independent-review evidence hợp lệ** cho boundary v1.5 — ghi nhận theo quyết định PO, không phải Claude tự tuyên bố.
- **Final consolidated finding count:** **0 Blocker · 1 Major (M-01) · 0 Minor · 0 Suggestion.**
- **M-02 — rejected**, không mở lại/xử lý trong revision này (Product Owner quyết).

### Đã sửa (1 Major — M-01) — thiếu canonical tier-designation authority contract cho standalone executable artifact (§13.4 nhánh 3, §13.9)

- Thêm **§13.4.1 — Canonical tier-designation authority**: mọi scope yêu cầu quality tier phải resolve đúng **một** canonical designation authority, tồn tại trước gate evaluation, explicit/versioned/immutable-pinned, scope tường minh; không resolve được hoặc nhiều authority cạnh tranh cùng scope → fail-closed. Không khóa filename/vendor/CI/format.
- Khóa tách bạch **tier declaration ≠ authority to classify ≠ validated quality-gate eligibility**.
- Khóa **anti-self-certification**: subject artifact/producer/owner không tự tạo eligibility hay trở thành authority chỉ bằng publish declaration; self-classification chỉ hợp lệ khi có canonical designation resolve độc lập, explicitly authorize đúng actor cho đúng scope; **không** đòi hỏi khác nhân sự/human identity khi Constitution không yêu cầu — rule nhắm vào tách authority, không phải cơ chế định danh cá nhân.
- Khóa **authority chain**: canonical designation → authorized tier classification/declaration → resolved tier → applicable floor/gates → evaluation → immutable evidence; declaration không được tự tạo upstream designation của chính nó.
- **§13.9 refined** (không duplicate Chapter 10): nhánh standalone của tier-resolution provenance giờ pin đủ canonical designation identity/version/scope/owner, exact declaration identity, identity actor được authorize để classify, và bằng chứng designation+declaration applicable tại evaluation boundary. Validator sentence refined: reject unresolved authority · unauthorized self-declaration · conflicting designation · designation/declaration hết hạn hoặc không applicable; không infer/default/tạo authority; authority không verify được → `FAIL — evidence`. Historical-immutability sentence mở rộng gồm designation/classifier authority (không chỉ ownership/tier metadata).
- **§13.14 refined:** defer list bổ sung storage/technology cụ thể của canonical tier-designation authority — cùng nguyên tắc không khóa mechanism đã áp cho declaration.
- **Authority boundary:** §13.4.1 tự đứng độc lập (self-contained) trong Chapter 13; không định nghĩa lại Chapter 7 module identity, Chapter 9 plugin grant, Chapter 10 compatibility authority, Chapter 12 phase approval; không tạo competing current-state authority với MANIFEST (I-12); không sửa governance review eligibility (Chapter 0 §3/Chapter 11 §11.5). Phân tầng Declaration→Grant/Designation→Enforcement→Verification của Chapter 9 §9.6/Chapter 10 §10.4.3 chỉ dùng như pattern tham khảo, không tạo dependency mới.

### Metadata / state

- `constitution/13-quality-gates.md`: **v1.5 → v1.6**, status giữ `In Review`, `approved_by`/`approved_at` giữ `null`. `depends_on` giữ nguyên `["02-platform-invariants", "07-module-taxonomy"]` (không thêm dependency mới).
- `MANIFEST.md`: row Chapter 13 → **v1.6**; `manifest_version` **9.17 → 9.18**; `constitution_version` giữ **1.1.0**; Chapter 0–12 giữ `Locked`, Chapter 14 giữ `In Review`; OQ-002/OQ-003 vẫn `Open`; không close backlog khác.

### ADR

**Không cần ADR** — M-01 xử lý trong authority sẵn có của Chapter 13 (quality-tier authority requirement, §13.13); không sửa Locked chapter; không mở rộng authority Chapter 7/9/10/12.

### Next

`Chapter 13 v1.6 — In Review — ready for exact-baseline re-review.` Revision này **chưa** qua review — không pre-assert kết quả review v1.6 hay Product Owner approval.

## [Unreleased] — 2026-07-27 — Chapter 13 (Quality Gates) v1.4 → v1.5 — tier-resolution evidence provenance

**Không phải approval.** Revision của chapter đang `In Review`; **không** Approve/Lock, `approved_by`/`approved_at` giữ `null`. Claude là **author/self-reviewer** (`AI Technical Architect`); **không** pre-assert future independent review, **không** pre-assert PO approval.

### Review provenance

- **ChatGPT Review A + internal Review B + consolidation = một ChatGPT review package** (một actor identity `ChatGPT`).
- **Verdict:** `Revision Requested`.
- **Severity count:** **0 Blocker · 1 Major · 0 Minor · 0 Suggestion**.

### Đã sửa (1 Major) — thiếu tier-resolution provenance trong immutable quality-gate evidence (§13.9, §13.4, §13.14)

- **Immutable gate evidence giờ pin `tier_resolution_branch`** (runtime module · owned executable artifact · standalone executable artifact) khi tier ảnh hưởng gate applicability/coverage floor.
- **Ownership declaration/reference được pin** (exact reference + version/content identity + canonical owning-module identity + authority owner) khi dùng inheritance.
- **`module-registry` hoặc standalone tier declaration được pin** exact version/content identity + entry/declaration reference.
- **Resolved tier + applicable coverage floor + criteria/policy version được pin**; evaluation boundary chứng minh reference là authoritative tại thời điểm gate, không resolve lại từ mutable state.
- **Historical result không bị reinterpret** bởi metadata hiện tại; đổi ownership/tier → sinh evaluation mới, evidence cũ giữ nguyên chain.
- **Validator chỉ verify pinned provenance**; không reconstruct bằng current/mutable metadata, không infer/default tier, không thành policy authority.
- Áp exact-pin pattern tương đương Chapter 10 §10.8 cho quality-tier — **không** duplicate Chapter 10; không tạo state store cạnh tranh MANIFEST (I-12).

### Metadata / state

- `constitution/13-quality-gates.md`: **v1.4 → v1.5**, status `In Review`. `depends_on` giữ `["02-platform-invariants", "07-module-taxonomy"]` (không thêm dependency mới).
- `MANIFEST.md`: row Chapter 13 → **v1.5**; `manifest_version` **9.16 → 9.17**; `constitution_version` giữ **1.1.0**; Chapter 0–12 giữ `Locked`, Chapter 14 giữ `In Review`; OQ-002/OQ-003 vẫn `Open`; không close backlog khác.

### ADR

**Không cần ADR** — chapter còn `In Review`, không Locked rule/invariant nào bị thay đổi; không mở rộng authority Chapter 7/10/12.

## [Unreleased] — 2026-07-27 — Chapter 13 (Quality Gates) v1.3 → v1.4 — authoritative tier resolution clarification

**Không phải approval.** Revision của chapter đang `In Review`; **không** Approve/Lock, `approved_by`/`approved_at` giữ `null`. Claude là **author/self-reviewer** (`AI Technical Architect`); **không** pre-assert future independent review, **không** pre-assert PO approval.

### Review provenance

- **ChatGPT Review A + internal Review B + consolidation = một ChatGPT review package** (một actor identity `ChatGPT`).
- **Verdict:** `Revision Requested`.
- **Severity count:** **0 Blocker · 1 Major · 0 Minor · 0 Suggestion**.

### Đã sửa (1 Major) — thiếu authoritative tier source cho executable non-module artifact (§13.4, §13.12, §13.14)

- **Runtime module** → tier resolve từ `module-registry.yaml` (authority Chapter 7 không đổi).
- **Owned executable artifact** → **inherit** tier của đúng một canonical owning module; ownership phải explicit · resolvable · versioned/pinned; **validator không suy diễn**.
- **Standalone executable artifact** → cần **authoritative quality-tier metadata** (explicit · versioned · pinned · có owner · tồn tại trước gate); storage/schema/filename defer §13.14; **không** mở rộng `module-registry.yaml` thành registry cho mọi artifact.
- **Multiple/ambiguous ownership hoặc tier không resolve** → **undefined tier applicability → fail-closed**; không tự chọn tier cao/thấp nhất khi Constitution chưa có explicit rule.
- **Validator boundary:** không infer/default tier, không tạo ownership; chỉ kiểm tra declaration/inheritance đã resolve.
- **Release/build** chỉ roll up constituent gate results; không tự tạo tier riêng trừ khi có standalone executable subject khai báo riêng.

### Metadata / state

- `constitution/13-quality-gates.md`: **v1.3 → v1.4**, status `In Review`. `depends_on` giữ `["02-platform-invariants", "07-module-taxonomy"]` (không thêm dependency mới).
- `MANIFEST.md`: row Chapter 13 → **v1.4**; `manifest_version` **9.15 → 9.16**; `constitution_version` giữ **1.1.0**; Chapter 0–12 giữ `Locked`, Chapter 14 giữ `In Review`; OQ-002/OQ-003 vẫn `Open`; không close backlog khác.

### ADR

**Không cần ADR** — chapter còn `In Review`, không Locked rule/invariant nào bị thay đổi; không mở rộng authority Chapter 7.

## [Unreleased] — 2026-07-27 — Chapter 13 (Quality Gates) v1.2 → v1.3 — coverage applicability clarification

**Không phải approval.** Revision của chapter đang `In Review`; **không** Approve/Lock, `approved_by`/`approved_at` giữ `null`. Claude là **author/self-reviewer** (`AI Technical Architect`); **không** pre-assert future independent review, **không** pre-assert PO approval.

### Review provenance

- **ChatGPT Review A + internal Review B + consolidation = một ChatGPT review package** (một actor identity `ChatGPT`).
- **Verdict:** `Revision Requested`.
- **Severity count:** **0 Blocker · 1 Major · 0 Minor · 0 Suggestion**.

### Đã sửa (1 Major) — coverage applicability quá rộng (§13.12)

- **Coverage moved out of universal artifact gate:** nhóm "Unconditional/Universal" giờ chỉ còn **invariant conformance** (theo Scope). Coverage chuyển sang nhóm mới **Executable-implementation-triggered**.
- **Coverage chỉ áp** khi artifact có **authoritative executable implementation + resolvable coverage boundary + resolvable applicable tier**.
- **Not-applicable ≠ missing evidence:** artifact không có executable implementation → coverage **không applicable** (không bị bắt tạo line/branch/test-effectiveness); chỉ khi coverage **đã applicable** mà thiếu metric/evidence → `FAIL — evidence`.
- **Rollup cập nhật:** runtime module inherit executable coverage; contract/schema **không** inherit coverage chỉ vì thuộc scope; migration chỉ có coverage nếu chính migration có executable implementation; release dùng constituent rollup; phase deliverable dùng declared gate set.
- **Fail-closed giữ nguyên:** artifact có executable implementation nhưng boundary/tier chưa resolve → không silently skip → undefined applicability → fail-closed. Runtime-module coverage vẫn giữ deterministic line + branch floors (§13.3). Consistency touch §13.3 để câu "coverage là điều kiện cần" scoped theo coverage-applicable.

### Metadata / state

- `constitution/13-quality-gates.md`: **v1.2 → v1.3**, status `In Review`. `depends_on` giữ `["02-platform-invariants", "07-module-taxonomy"]`.
- `MANIFEST.md`: row Chapter 13 → **v1.3**; `manifest_version` **9.14 → 9.15**; `constitution_version` giữ **1.1.0**; Chapter 0–12 giữ `Locked`, Chapter 14 giữ `In Review`; OQ-002/OQ-003 vẫn `Open`; không close backlog khác.

### ADR

**Không cần ADR** — chapter còn `In Review`, không Locked rule/invariant nào bị thay đổi.

## [Unreleased] — 2026-07-27 — Chapter 13 (Quality Gates) v1.1 → v1.2 — revision per consolidated review

**Không phải approval.** Revision của chapter đang `In Review`; **không** Approve/Lock, `approved_by`/`approved_at` giữ `null`. Claude là **author/self-reviewer** (`AI Technical Architect`), **không** pre-assert future independent review, **không** pre-assert PO approval.

### Review provenance

- **ChatGPT Review A + internal Review B + consolidation = một ChatGPT review package** (một actor identity `ChatGPT`).
- **Verdict:** `Revision Requested`.
- **Severity count:** **0 Blocker · 3 Major · 0 Minor · 0 Suggestion**.

### Đã sửa (3 Major)

- **Waiver semantics (§13.11):** khóa rõ waiver **không** thay đổi gate result, **không** biến `FAIL`/`BLOCKED` thành `PASS`, **không** thỏa prerequisite yêu cầu `PASS`; artifact có open waiver **không đủ eligibility** cho Chapter 12 Approval Gate; "proceed" chỉ cho bounded artifact-level activity; **phase approval/transition vẫn bị chặn** tới khi gate thực sự `PASS`; PO là sole risk-acceptance/approval authority; waiver không bypass Locked invariant.
- **Coverage semantics (§13.3):** thay wording mơ hồ `line + branch` bằng rule deterministic — `line coverage >= tier floor AND branch coverage >= tier floor`, hai metric đạt **độc lập**; thiếu metric/evidence không resolve → `FAIL — evidence`. Giữ thresholds (Tier 0 ≥95% · 1 ≥90% · 2 ≥80% · 3 ≥60%), anti-gaming và test-effectiveness rule. Không khóa tool/vendor.
- **Applicability semantics (§13.12):** tách gate thành **unconditional · tier-triggered · responsibility/boundary-triggered · lifecycle-triggered**; performance/security/observability **không** còn mặc định áp cho mọi runtime module; undefined applicability vẫn **fail-closed**; cùng artifact → cùng gate set.

### Metadata / state

- `constitution/13-quality-gates.md`: **v1.1 → v1.2**, status `In Review`. `depends_on` giữ `["02-platform-invariants", "07-module-taxonomy"]` (không thêm Chapter 12/14).
- `MANIFEST.md`: row Chapter 13 → **v1.2**; `manifest_version` **9.13 → 9.14**; `constitution_version` giữ **1.1.0**; Chapter 0–12 giữ `Locked`, Chapter 14 giữ `In Review`; OQ-002/OQ-003 vẫn `Open`; không close backlog khác.

### ADR

**Không cần ADR** — chapter còn `In Review`, không Locked rule/invariant nào bị thay đổi.

## [Unreleased] — 2026-07-27 — Chapter 13 (Quality Gates) draft v1.0 → v1.1 (In Review)

**Không phải approval.** Đây là authoring revision của một chapter đang `In Review`; **không** Approve/Lock, `approved_by`/`approved_at` giữ `null`. Không AI nào approve — Claude (`AI Technical Architect`) chỉ cung cấp self-review + draft; review package độc lập (ChatGPT) và Product Owner decision vẫn chưa diễn ra.

### Thay đổi

- `constitution/13-quality-gates.md`: **v1.0 → v1.1**. Từ một coverage-tier table mở rộng thành Quality Gate contract đầy đủ (13.1–13.14): Quality Gate vs Approval Gate + fail-closed semantics; coverage semantics + anti-gaming + test-effectiveness (Tier 0/1); invariant-conformance gate gom Verification của I-1…I-13 (tham chiếu Ch2, không định nghĩa lại); risk-based test categories; performance gate có baseline/budget/owner/reproducibility; evidence contract (pinning + result classification); flaky-test policy; exception/waiver process; gate-applicability table; authority-boundary table. **Không** đóng OQ-002/OQ-003.
- `depends_on`: đề xuất thêm `02-platform-invariants` (invariant-conformance gate gom Verification của Ch2 làm evidence cốt lõi; đã kiểm tra acyclic) bên cạnh `07-module-taxonomy`. Open cho reviewer disagreement.
- `MANIFEST.md`: row Chapter 13 → **v1.1** + depends_on cập nhật; `manifest_version` **9.12 → 9.13**; overview line ghi nhận draft v1.1. `constitution_version` giữ **1.1.0** (không bump khi chapter còn In Review).

### ADR

**Không cần ADR** — chapter còn `In Review`, chưa có Locked rule/invariant nào bị thay đổi.

## [Milestone] — 2026-07-27 — 🔒 Chapter 12 (Approval Gates) v1.4 ACTIVATED & LOCKED

**Product Owner decision** (sole approval authority): *"I, Product Owner, decide to Approve & Lock Chapter 12 v1.4. Atomic activation commit and closure of BL-008 are authorized."* — quyết định ngày **2026-07-27**.

Đây là **activation** theo quyết định của Product Owner, **không phải** một AI approval. Không AI nào (Claude/ChatGPT) approve hoặc lock chương này; các actor `AI Technical Architect` chỉ cung cấp review evidence, không có veto, và Product Owner là authority duy nhất.

### Review eligibility (đã thỏa minimum-two distinct identity)

- **Actor `ChatGPT`** (`AI Technical Architect`): consolidated review package (Review A + internal second-pass Review B + consolidation) — verdict Revision Requested.
- **Actor `Claude`** (`AI Technical Architect`): independent final review (clean session) — verdict accepted with corrections.
- Minimum-two distinct actor identity **satisfied** (`ChatGPT` + `Claude`); reviewer **không có veto**; **Product Owner** là sole authority.

### Final review result

- **0 Blocker · 0 Major · 0 Minor** còn mở.
- **Backward Consistency Check: `No conflict`** (đối chiếu Chapter 0 v1.1, Chapter 11 v2.1, I-12, ADR-011).

### Activated state (atomic — trong một commit)

- `constitution/12-approval-gates.md`: `status` **In Review → Locked**; `approved_by: Product Owner`; `approved_at: "2026-07-27"`; `last_review: "2026-07-27"`. **Version giữ 1.4** — normative body **không đổi** (byte-identical với bản đã review, blob `1126eaea…`); chỉ lifecycle metadata thay đổi. Sau approval boundary, Chapter 12 v1.4 là **Locked** và bất biến ở cùng version.
- MANIFEST: `manifest_version` **9.11 → 9.12**; row Chapter 12 → **v1.4 Locked**; status ledger + tổng quát cập nhật (Chapter 0–12 Locked, 13–14 In Review); `constitution_version` **giữ 1.1.0** (không có rule buộc bump khi lock chapter — Constitution Version độc lập, MANIFEST §Constitution Version).
- **BL-008: Closed/Resolved** — wording identity-specific đã generalize ở v1.3, approval-gate contract refined ở v1.4, review identities resolved = ChatGPT + Claude, PO approved & locked v1.4 ngày 2026-07-27.

### Atomicity

Chapter 12 lifecycle metadata + MANIFEST current state + BL-008 transition + CHANGELOG activation record **landed trong một commit duy nhất**. Không partial activation.

### ADR

**Không cần ADR** — Product Owner approve một v1.4 contract đã được review; **không** Locked governance rule hay selected invariant nào bị thay đổi.


## [Unreleased] — Chapter 12 review provenance — corrective note (forward-only, không rewrite history)

**Corrective, không phải Chapter 12 normative change.** Chỉ đính chính review-provenance evidence; Chapter 12 v1.4 normative body **không đổi**. Historical commit `5e42cd7540561a820d42e609ecfc0865fb184c81` **không bị rewrite** — sửa được ghi *forward*.

### 1. Điều đã ghi sai

Entry của commit `5e42cd7` mô tả `**ChatGPT Review A** + **Review B**` như **hai actor identity độc lập**. Đó là sai, và còn pre-assert `Review B` như completed evidence trước khi vòng review thực tế được chốt.

### 2. Semantics đúng (identity model — authoritative per Product Owner)

- `Review A` và internal `Review B` **đều do cùng một actor identity `ChatGPT`** thực hiện. `Review B` là **internal second-pass review** để tăng recall và hỗ trợ consolidation — **không** được tính là một distinct governance reviewer.
- A + B được consolidate thành **một** ChatGPT review package = review của actor `ChatGPT`.
- Một **Claude session sạch** thực hiện **independent final review**, tính là review của actor `Claude`.
- **Session count không tạo actor identity mới** (nhiều session ChatGPT vẫn là `ChatGPT`; nhiều session Claude vẫn là `Claude`).
- Claude **author/self-review** (v1.2 → v1.3) **không** được nhầm với independent final review; independent final review là vòng Claude session sạch diễn ra **sau** ChatGPT consolidation.
- Không áp rule "author permanently cannot review" (rule này không tồn tại trong Chapter 0 v1.1 / Chapter 11 v2.1); Claude final review ở session sạch là independent review của actor `Claude` trong workflow này.

### 3. Corrected review provenance (Chapter 12 v1.4 cycle)

- **Actor `ChatGPT`** — role: `AI Technical Architect` — evidence: Review A + internal Review B + consolidated review package — verdict (trước Claude challenge): **Revision Requested** (0 Blocker · 1 Major · 2 Minor · 1 Suggestion).
- **Actor `Claude`** — role: `AI Technical Architect` — evidence: independent final review/challenge của Chapter 12 review cycle culminating in v1.4 — verdict: **consolidated finding accepted with corrections**.

### 4. Minimum-two distinct identity

Requirement được hiểu đúng là **`ChatGPT` + `Claude`** (hai distinct actor identity, cùng giữ role `AI Technical Architect`, không veto), **không phải** `ChatGPT Review A + ChatGPT Review B`. Product Owner vẫn là **sole approval authority**.

### 5. Không thay đổi state

- Chapter 12: giữ **v1.4 · `In Review` · `approved_by: null` · `approved_at: null`** — entry này **không** Approve/Lock.
- MANIFEST, team.yaml: **không đổi**; không bump Chapter/MANIFEST/Constitution version.
- **BL-008** vẫn `addressed pending review`, **chưa close** — chỉ close sau khi Product Owner Approve/Lock Chapter 12.

## [Unreleased] — Chapter 12 (Approval Gates) v1.3 → v1.4 — Revision per Final Consolidated Decision (**0 Blocker · 1 Major · 2 Minor · 1 Suggestion → Revision Requested**)

Revision thực hiện theo Final Consolidated Decision của vòng review độc lập. Không mở ADR mới (Ch12 vẫn `In Review`, nằm trong hướng ADR-011 đã authorize; toàn bộ là reference/clarity trong model hiện hành). `status` giữ `In Review`; **không** tự Approve/Lock. Không đụng byte của Chapter 0 / Chapter 11 (Locked).

### Review provenance (không phải governance rule — chỉ evidence)

- Minimum-two independent review evidence của vòng này: **ChatGPT Review A** + **Review B** (hai actor identity độc lập giữ role `AI Technical Architect`).
- **Claude independent challenge** là *additional review/challenge*, **không phải** một distinct third identity; Claude author/self-review và Claude challenge session là **cùng một actor identity Claude**.
- Claude challenge: **accepted with corrections** (hạ 4 Major của consolidated draft xuống 1 Major + 2 Minor + 1 Suggestion; sửa 2 misread; thu hẹp remedy để tránh tự tạo competing authority).

### Fixed — R1 (Backward Consistency Check, §12.4)

Tách rõ hai chiều: **(A) Pre-decision vs Locked authority** — reviewer đối chiếu candidate với authority đã Approved/Locked, pin evidence tại boundary; `No conflict` → tiếp tục, `Revision required`/`ADR required` → gate **vẫn đóng** (eligibility condition, không phải veto). **(B) Post-approval propagation** — ảnh hưởng tới living docs `Draft`/`In Review` khác ghi thành explicit follow-up ở MANIFEST backlog/OQ; **không** tự invalidate artifact vừa approve; conflict-với-Locked lọt lưới A = integrity violation xử lý theo Chapter 0. Chỉ reference Chapter 0 Freeze Policy §5 + ADR workflow, không tự đặt rule mutate Locked doc.

### Fixed — R2 (DoD semantics, §12.1)

Bỏ `+ Approved` khỏi mọi list deliverable. Viết lại thành "Phase X evidence: ...". Tách rõ: DoD criteria = *substantive completion evidence* đánh giá **trước** decision; `Approved` = **outcome** của gate, không nằm trong DoD (loại vòng lặp định nghĩa). Ghi rõ DoD phải được viết + PO chấp nhận (định nghĩa tiêu chí, không phải đạt tiêu chí) trước khi gate dùng chúng.

### Fixed — R3 (Phase Approval Gate prerequisite aggregation, §12.2) + Authority boundary (§12.3)

Thêm §12.2 **reference-based**: 8 eligibility prerequisite (DoD defined+accepted · deliverables complete · dependencies ready · required ADR Approved · applicable quality gate passed · Backward Consistency = No conflict · validator/MANIFEST freshness · minimum-two independent reviews pinned) → sau đó Product Owner là authority duy nhất (Approve/Reject/Revision Requested). Ghi rõ: fail closed = eligibility incomplete (không phải veto) · reviewer recommendation ≠ PO decision · validator ≠ approval authority · không bắt đầu phase sau trước khi ghi current phase state vào MANIFEST. Thêm §12.3 authority map: Ch12 chỉ own phase orchestration; review eligibility → Ch0/Ch11, ADR lifecycle → Ch11, quality → Approved/Locked quality contract (intended owner Ch13, **hiện In Review, không binding**), phase sequence/DoD → Approved roadmap/phase plan (intended owner Ch14, **hiện In Review, không binding**), activation → governing ADR (ADR-011 §4), current ADR/OQ state → MANIFEST (I-12).

### Sync

- `constitution/12-approval-gates.md`: v1.3 → **v1.4**, `last_review` 2026-07-27, `status` giữ `In Review`, `approved_by`/`approved_at` giữ `null`, `depends_on` **giữ nguyên** `["00-governance","11-adr-process"]` (không thêm 14-roadmap → tránh cycle; không thêm 13-quality-gates vì Ch13 chưa Locked).
- MANIFEST: manifest_version 9.10 → **9.11**; row Ch12 → 1.4; `constitution_version` giữ 1.1.0; **BL-008 giữ `addressed pending review`, KHÔNG close**.

### Note

- **Không** tự tuyên bố Approve/Lock. Chờ Product Owner quyết. BL-008 chỉ close khi Chapter 12 Locked.

## [Unreleased] — Chapter 12 (Approval Gates) v1.2 → v1.3 — Claude self-review (**1 Blocker · 1 Major · 0 Minor · 3 Suggestion**)

Self-review đối chiếu Chapter 0 v1.1 (Locked) §2–§3 và Chapter 11 v2.1 (Locked) §11.5. Đóng nợ kỹ thuật **BL-008**. Không mở ADR mới: ADR-011 đã authorize hướng role-based, Chapter 12 vẫn `In Review` nên sửa trực tiếp. `status` giữ `In Review`; không tự Approve/Lock.

### Severity table

| # | Severity | Finding | Xử lý |
|---|---|---|---|
| F1 | **Blocker** | Body dùng identity-specific `ChatGPT Review + Claude Review` như governance rule — mâu thuẫn Chapter 0 §2 (Constitution chỉ định nghĩa Role, không hardcode tên AI) và §3 (role-based minimum-two independent gate). Đây là BL-008. | **Fixed** — generalize sang "tối thiểu hai independent review từ actor giữ role `AI Technical Architect`", danh tính chỉ là evidence. |
| F2 | **Major** | Wording cũ `là bước bắt buộc… không phải điều kiện approve` yếu hơn Chapter 0 §3: đọc theo nghĩa đen có thể hiểu là review không phải precondition, trong khi §3 khóa "thiếu ≥2 reviewer đủ điều kiện ⇒ decision chưa đủ điều kiện tới approval gate". Rủi ro tạo tension với chương Locked. | **Fixed** — tách rõ **tồn tại review = eligibility precondition bắt buộc** vs **kết luận review = không veto**, đúng mô hình §3. |
| F3 | Suggestion | Nguy cơ tạo authority cạnh tranh nếu Chapter 12 tự định nghĩa lại review gate. | **Fixed** — thêm blockquote "tham chiếu, không định nghĩa lại", trỏ authority về Chapter 0 §3 + Chapter 11 §11.5. |
| F4 | Suggestion | §12.1 note trỏ "Governance §4" (§4 = ADR Workflow) không sát với review process. | **Fixed nhẹ** — đổi thành "một chương Governance đã Locked" để không trỏ sai section-number của chương Locked. |
| F5 | Suggestion | DoD liệt kê Phase 0/1/3, thiếu Phase 2; enumeration nên khớp Roadmap. | **Deferred** — Chapter 14 (Roadmap) vẫn `In Review`; không tạo dependency vào nội dung chưa Locked. Danh sách là "ví dụ", không phải enumeration đóng. |

### Không phải finding (đã đối chiếu, giữ nguyên có chủ đích)

- Frontmatter `reviewers: [ChatGPT, Claude]`: giữ nguyên. Theo Chapter 11 §11.4, `reviewers` là **historical evidence**, không phải governance rule; Chapter 0 và Chapter 11 (đều Locked) cũng mang đúng field này. Đổi sẽ sai model, không đổi.
- Tham chiếu ADR-004/ADR-005/ADR-011: là **decision evidence/history**, không assert current lifecycle state ⇒ không đụng model "MANIFEST là authority" của ADR-011. Chapter 12 **không** tham chiếu current OQ status hay current ADR lifecycle state ở đâu — không có authority cạnh tranh với MANIFEST.

### Sync

- `constitution/12-approval-gates.md`: v1.2 → v1.3, `last_review` 2026-07-16 → 2026-07-27, `status` giữ `In Review`, `approved_by`/`approved_at` giữ `null`.
- MANIFEST: manifest_version 9.9 → 9.10; row Chapter 12 → 1.3; `generated_at` → 2026-07-27; BL-008 note cập nhật "addressed pending review".

### Note

- Đây là **self-review của Claude**, chưa qua vòng review độc lập thứ hai. **Không** tự tuyên bố "đã sạch" hay Approve. Chờ ChatGPT review + Product Owner Approve/Lock. BL-008 chỉ close khi Chapter 12 Locked.

## [Milestone] — 2026-07-25 — 🔒 ADR-011 Atomic Governance Migration ACTIVATED

**Product Owner Kanner approved and activated** the governance migration authorized by ADR-011 v1.1 as one atomic documentation boundary after independent Review B and Claude review returned zero blocking findings.

### Activated together

- Chapter 0 — Governance: v1.0 → v1.1, `Locked`
- Chapter 11 — ADR Process: v2.0 `In Review` → v2.1 `Locked`
- Canonical ADR template aligned with role-based reviewer evidence and immutable ADR files
- MANIFEST v9.8 → v9.9; Constitution version 1.0.0 → 1.1.0
- CHANGELOG records this activation

### Governance changes

1. ADR files are immutable byte-for-byte after Product Owner approval.
2. Current ADR lifecycle state and reverse supersession relation are authoritative in MANIFEST.
3. Approval gates require at least two independent actors holding `AI Technical Architect` at the review boundary.
4. Reviewer identities are pinned as evidence, not hardcoded as permanent Constitution rules.
5. MANIFEST is authoritative for current OQ status; ADR metadata is decision evidence and transition cause.
6. ADR approval, OQ and supersession transitions must be atomic with MANIFEST.
7. No partial activation occurred; all five governed artifacts changed in this single boundary.

### Authority and compatibility

- ADR-011 remains `Approved` and unchanged.
- ADR-006 remains in force; ADR-011 generalizes reviewer selection without superseding peer equality/non-hierarchy.
- ADR-005 remains in force; its identity-specific `ChatGPT + Claude` wording was the then-current instantiation of Governance §3, now generalized to a role-based minimum-two gate. Its normative core — lean governance, no reviewer veto and Product Owner sole authority — is preserved.
- Chapter 2 I-12 is preserved.
- ADR-001 through ADR-010 decision content is unchanged.
- Legacy ADR-004 → ADR-005 supersession remains represented in MANIFEST; no history rewrite.

### Known follow-up

- Chapter 12 (`approval-gates.md`) remains `In Review` and still contains identity-specific review wording. It must be aligned with Chapter 0 v1.1 before Chapter 12 is approved/locked.

### Integrity

Baseline commit: `805643702d2ed49c38d9f36aa98580df444a808c`

Baseline blobs:

- Chapter 0: `a317762e217d7f013d9fa5536569575435187ba1`
- Chapter 11: `1dbdfdb8d39a3f1d950b9167356945da4e7a5b2f`
- ADR template: `536aa4234deda206fef601481fafefac39c35eb4`
- MANIFEST: `6215aaf9075c1e29e0fa138d7ede6d9b8ee17b73`
- CHANGELOG: `ce583cfc1a5f0f9baf3b254c7d2d1d46a7a574fe`
- ADR-011 evidence unchanged: `023147d2039d698d33ac1d60d463e42a1db27342`

## [Historical Review] — Chapter 11 (ADR Process) v2.0 — pre-ADR-011 self-review (**2 Blocker · 4 Major · 2 Minor · 1 Suggestion**)

Chapter 11 v1.3 dài 49 dòng, `last_review: 2026-07-18`. Self-review đối chiếu Chapter 0 (Locked) và trạng thái thực tế của `/docs/adr/`.

### Fixed — Blocker
- **Cơ chế supersede mâu thuẫn trực tiếp với ADR Immutable Rule, và Ch11 không định nghĩa `supersedes`/`superseded_by`:** Ch0 §5 khóa *"sau khi Locked TUYỆT ĐỐI không sửa lại"* nhưng đồng thời bảo liên kết qua `supersedes`/`superseded_by`; Ch0 §7 lại có nhánh lifecycle `Approved`/`Locked → Deprecated`/`Superseded` (tức `status` **phải** đổi sau khi Locked). Ba điều này không thể cùng đúng nếu immutability nghĩa là "không field nào được đổi". **Mâu thuẫn đã materialize thật trong repo:** `ADR-004.md` có `status: Superseded` + `superseded_by: ADR-005` — tức đã bị ghi thêm field sau khi Locked. Ch11 — chương sở hữu ADR metadata contract — không có một dòng nào về hai field này. **Sửa — thêm §11.3 Immutability boundary:** tách **decision content** (Context · Decision · Alternatives · Concerns/Risks · Scale check · Consequences → **bất biến tuyệt đối**) khỏi **lifecycle/link metadata** (`status` · `superseded_by` · `deprecated_at` → được chuyển trạng thái, **chỉ** theo transition mà Ch0 §7 cho phép) và **approval metadata** (`approved_by`/`approved_at` → bất biến sau khi set). Ghi rõ cập nhật lifecycle metadata **không phải một "lần sửa ADR" độc lập** — chỉ hợp lệ khi nằm trong transition atomic §11.5. Kèm disclaimer: đây là clarification trong phạm vi wording sẵn có của Ch0, nếu reviewer đánh giá là redefinition thì bắt buộc mở ADR sửa Ch0 — Ch11 không tự làm. Bổ sung `supersedes`/`superseded_by` vào metadata contract §11.4 với **rule hai chiều bắt buộc**: `B.supersedes ∋ A` ⟺ `A.superseded_by = B` ∧ `A.status = Superseded`; một chiều thiếu chiều kia là **trạng thái không hợp lệ**, không phải "chưa cập nhật xong".
- **Hardcode tên AI cụ thể vào rule bắt buộc, trái nguyên tắc Locked của Ch0 §2:** v1.3 ghi *"ChatGPT Review + Claude Review là bắt buộc"*, trong khi Ch0 §2 khóa *"Constitution chỉ định nghĩa **Role**, không bao giờ ghi tên người/AI cụ thể"* và cảnh báo rõ nếu có thêm AI khác (Codex, Gemini) thì cách ghi này vô nghĩa; gán Người/AI ↔ Role phải sống ở `/team/team.yaml`. **Sửa §11.8:** đổi thành *"review từ các role đang giữ `AI Technical Architect` là input bắt buộc"*, ghi rõ số lượng và danh tính có thể thay đổi mà không cần sửa chương này. Giữ nguyên phân biệt "bắt buộc **có**" ≠ "điều kiện **approve**".

### Fixed — Major
- **ADR identity không có authority cấp số:** v1.3 chỉ có quy ước path `/docs/adr/ADR-XXX.md`, không nói ai cấp số, uniqueness scope, có được tái sử dụng số của ADR bị hủy không — trong khi Ch6 đã khóa identity/non-reuse rất chặt cho mọi thứ khác, và mọi tài liệu Locked đều tham chiếu ADR **bằng số**. **Thêm §11.2:** đúng một authority cấp số cho toàn repo (không phải quy ước ngầm giữa contributor) · uniqueness vĩnh viễn trên toàn `/docs/adr/` · **không tái sử dụng** số của ADR bị hủy · **không renumber** sau khi rời `Draft` · authority của identity là **số ADR**, không phải đường dẫn file.
- **Transition `Approved → Locked` không được định nghĩa:** Ch0 §7 có hai trạng thái riêng biệt nhưng Ch11 chỉ khóa atomic cho bước approve. **Thêm vào §11.5:** Approved và Locked **cùng** chịu Freeze Policy — cả hai đều không sửa được decision content; Locked là xác nhận ổn định + được MANIFEST ghim; chuyển `Approved → Locked` là thay đổi lifecycle metadata, atomic với MANIFEST, và **không** mở lại cơ hội chỉnh sửa nội dung. Thêm luôn transition **Deprecate** (không có ADR thay thế → `status → Deprecated`, không có `superseded_by`) và transition **Supersede atomic gồm cả hai file** — cấm approve ADR mới trước rồi mới quay lại đánh dấu ADR cũ ở commit sau, vì khoảng giữa hai bước là trạng thái hai ADR cùng có hiệu lực cho một quyết định.
- **Authority của OQ status chưa khóa:** v1.3 bảo cập nhật `MANIFEST OQ-x → Resolved` cùng lúc với `resolves` trong ADR, nhưng không nói nơi nào canonical — đúng lớp lỗi peer authority đã phải sửa ở Ch9 (`Input Contract HOẶC dependency contract`) và Ch10 (`Policy Contract HOẶC registry`). **Thêm §11.6:** **ADR là authority**, MANIFEST là **projection**; lệch nhau thì ADR thắng và MANIFEST là lỗi cần sửa; **không tồn tại quan hệ "ADR HOẶC MANIFEST"** cho cùng sự thật OQ status.
- **"Machine-readable acceptance gate" nhắc validator nhưng không có owner/hệ quả:** **Thêm §11.7:** validator **không phải authority phê duyệt** (quyền approve/reject vẫn chỉ thuộc Product Owner) · kết quả validator là **điều kiện chặn, không phải cảnh báo** — metadata không nhất quán (supersede một chiều · `resolves` trên ADR chưa Approved · `depends_on` trỏ ADR chưa Approved hoặc tạo vòng · MANIFEST lệch ADR) thì ADR **không đủ điều kiện** chuyển `Approved` · ai vận hành và bằng công cụ gì thuộc Phase 1.

### Fixed — Minor
- **Không cấm `depends_on` vòng giữa các ADR:** thêm rule đồ thị **acyclic** vào §11.4 — A↔B là deadlock (không ADR nào rời được Draft/In Review), phải xử lý bằng tách/gộp quyết định, **không** bằng ngoại lệ thủ công.
- **`depends_on` thiếu `02-platform-invariants`** dù chương viện dẫn I-12 ở hai chỗ (Single Source of Truth cho lifecycle và cho OQ authority). Bổ sung, đồng bộ MANIFEST.

### Fixed — Suggestion
- **OQ `Resolved` bởi ADR sau đó bị Superseded thì sao:** thêm vào §11.6 — OQ **không tự động mở lại**; ADR thay thế phải khai báo tường minh: tiếp tục đóng (`resolves`) hay mở lại (OQ về `Open`, ghi rõ trong ADR mới). **Im lặng không phải một lựa chọn** — không nói gì về OQ mà ADR cũ đã đóng là **khai báo thiếu**, phải bổ sung trước khi approve.

### Checklist
- Ch11 v2.0 · 9 heading §11.1→§11.9 đúng thứ tự · **0 tham chiếu §11.x gãy** (§11.3 · 11.4 · 11.5 · 11.6 đều tồn tại) · **0 tên AI cụ thể trong rule** · mọi link target tồn tại (`00-governance` · `02-platform-invariants` · `adr-template.md` · `../team/team.yaml`) · không định nghĩa lại Ch0 §4b/§5/§7 · 0 authority mới được tạo.

### Note
- Đây là **self-review của Claude**, chưa qua ChatGPT. Không tự tuyên bố Approve. Chờ ChatGPT review round 1 và Product Owner Approve/Lock.

## [Milestone] — 2026-07-24 — 🔒 Chapter 10 (Compatibility & Capability Contract) LOCKED

**Product Owner (Kanner) xác nhận Approve & Lock** Chapter 10 v2.7, theo khuyến nghị reviewer (ChatGPT round 8: 0 Blocker · 0 Major · 0 Minor · 0 Suggestion, Consolidation Review 9 mục + Backward Consistency Check toàn bộ Chapter 0-9 đạt).

`status: In Review → Locked` · `approved_by: null → Kanner` · `approved_at: null → 2026-07-24`.

### Quy mô công việc
Chapter 10 trải qua **8 revision** (v1.0 gốc → self-review v2.0 Claude → v2.7), tương ứng **7 vòng review ChatGPT** (round 1-7) sau self-review ban đầu. v1.0 chỉ 32 dòng, viết trước khi Chapter 2-9 Locked; v2.7 khóa đầy đủ:

- **Authority boundary:** Chapter 10 không tự chiếm authority của Business Capability (Ch4), module identity (Ch7), Event Contract (Ch8), Plugin Contract (Ch9) — mọi capability/schema reference resolve về registry sở hữu nó, không hardcode tên/schema trong Constitution.
- **Ba loại capability tách biệt:** Business Capability · Required platform capability · Provided contract capability — reference chưa đăng ký là invalid declaration.
- **Ba trục version độc lập:** Event Contract version · `schema_version` · Plugin Version — cấm dùng trục này làm proxy trục kia; breaking change định nghĩa theo published contract surface; schema compatibility có semantic backward/forward độc lập format, thiếu direction declaration = invalid.
- **Compatibility Result** là artifact bất biến, không phải một lần kiểm tra thoáng qua: pin subject + input · policy artifact/version + policy authority designation + policy applicability fact/frontier · evaluator identity/artifact + **evaluator grant** (identity/content/scope/authority designation/applicability frontier) · evaluation boundary · result + reason classification (phân biệt proved-incompatible với insufficient-evidence). Chống self-certification hai lớp: `module identity ≠ authorization` và `grant artifact tồn tại ≠ grant đang có hiệu lực`.
- **Compatibility Policy** là versioned immutable authoritative artifact với exactly-one canonical authority cho mỗi loại fact/scope (định nghĩa/version vs runtime applicability) — không còn cấu trúc peer authority "A hoặc B".
- **Transition semantics khép kín:** mỗi transition thuộc đúng một trong hai lớp — Immediate suspension (grant revoke · safety-critical) hoặc Bounded revalidation (policy applicability đổi · designation đổi) với deadline phải do **versioned revalidation policy + designated authority** quyết định, có maximum bound, quy tắc gia hạn giới hạn tổng cộng; thiếu điều kiện nào → rơi về immediate suspension. Historical result luôn immutable, không hồi tố.
- **Capability Matrix** hai chiều (capability assertions + execution-mode readiness, mode readiness là projection dẫn xuất) · tách Declared support khỏi Validated readiness · versioned/resolvable, gate phải pin đúng snapshot đã dùng — không đóng ngầm OQ-002.

### Deferred sang Phase 1 design spec
Matching algorithm cụ thể · storage schema của Compatibility Result/Policy · deployment coordinator · fencing/transaction mechanism tại activation boundary · timer/drain implementation cho bounded revalidation · archive protocol · tooling/CI gate.

**Đã Locked tới nay:** Chapter 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, **10** + ADR-005 → ADR-010.

**Next Milestone:** Chapter 11 — ADR Process.

## [Unreleased] — Chapter 10 v2.7 (ChatGPT review round 7: **0 Blocker · 1 Major · 0 Minor · 0 Suggestion mới**)

Không có phản biện; finding chấp nhận toàn bộ.

### Fixed — Major: bounded revalidation deadline chưa có authority/policy/bound
- v2.6 khóa "result cũ còn hiệu lực tới một **explicit, bounded, đã pin** deadline" — loại được mâu thuẫn cũ, nhưng **không nói ai có quyền chọn deadline, theo policy nào, bound tối đa bao nhiêu, gia hạn có được phép không**. Trong khi đó safety-critical classification đã bắt buộc nằm trong policy và version hóa; nhánh non-safety-critical thì chưa.
- **Lỗ hổng cụ thể:** cùng một transition tại T1, coordinator A đặt `T1+5 phút`, coordinator B đặt `T1+24 giờ` — cả hai đều explicit/bounded/pinned, nhưng sau phút thứ 5 A đã fail-safe còn B vẫn sinh Decision, **cả hai đều tuyên bố được là tuân thủ**. Nghiêm trọng hơn: đặt deadline rất xa, hoặc thay deadline mới trước khi deadline cũ hết hạn → **bounded revalidation thoái hóa thành prospective-only trên thực tế**, đúng thứ chính mục đó tuyên bố cấm.
- **Sửa — thêm tiểu mục "Deadline của lớp bounded" trong §10.5.1:** deadline phải được tạo theo **versioned revalidation policy** áp cho scope đó, bởi **authority đã được designate** (cùng quy tắc exactly-one authority của §10.4.3). Deadline fact phải resolve tới tối thiểu: policy/rule version quy định cách xác định deadline · transition class + subject scope · authority phát hành deadline + designation version · immutable deadline/boundary fact · **maximum bound hoặc computation rule** do policy quy định · quy tắc gia hạn nếu được phép · **bằng chứng deadline không vượt bound cho phép**. **Gia hạn:** cấm mutate deadline cũ, phải tạo transition/deadline fact mới, phải được policy cho phép rõ, và **policy phải quy định giới hạn tổng cộng chứ không chỉ giới hạn từng lần** (nếu không, gia hạn nhiều lần vẫn né được fail-safe vô thời hạn). **Không resolve được policy/authority/bound, hoặc deadline vượt bound → transition không đủ điều kiện thuộc lớp bounded → rơi về immediate suspension** — cùng cơ chế khép kín với rule "không có deadline pin được thì không thuộc lớp bounded".
- Mechanism (timer, drain, coordinator, cách hiện thực grace window) vẫn defer Phase 1; **authority và semantic của deadline khóa tại Constitution**, ngang cấp với policy applicability và evaluator grant.

### Checklist
- Ch10 v2.7 · 18 heading đúng thứ tự · **0 heading bị nuốt/trùng** (`## 10.6` = 1) · **0 tham chiếu §10.x gãy** · version file ↔ MANIFEST đồng bộ.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 8 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 10 v2.6 (ChatGPT review round 6: **1 Blocker · 1 Major · 0 Minor · 0 Suggestion mới**)

Reviewer đã rút lại nhận định "outcome giữ nguyên" ở vòng trước và xác nhận phản biện meta của Claude là đúng. Vòng này không có phản biện; 2 finding chấp nhận toàn bộ.

### Fixed — Blocker: §10.5.1 tự mâu thuẫn về policy transition
- **Mâu thuẫn do chính Claude tạo ra ở v2.5.** Bảng transition ghi *"activation hiện hành tiếp tục dưới snapshot đã pin **cho tới activation boundary kế tiếp**"*, nhưng đoạn ngay sau lại khóa *"trong cửa sổ... subject không được coi là eligible để mở activation mới **hay để sinh authoritative Decision qua result cũ**"*. Hai câu không thể cùng đúng: cách hiểu A (chạy tiếp tới boundary kế tiếp, vẫn sinh Decision trong T1→T2) và cách hiểu B (mất eligibility ngay tại T1, tức immediate fail-safe) đều viện dẫn được đúng một mục Constitution → hai runtime hành xử ngược nhau mà cùng "tuân thủ".
- **Sửa — thay bằng mô hình hai lớp duy nhất, không có lớp thứ ba:**
  - **Immediate suspension** — evaluator grant bị revoke/phát hiện không có quyền · transition được policy phân loại safety-critical → result cũ **hết hiệu lực làm current eligibility evidence NGAY**, subject **dừng sinh authoritative Decision**, resume sau khi có result hợp lệ mới, fail-safe I-6 phạm vi nhỏ nhất đủ.
  - **Bounded revalidation** — policy applicability đổi **không** safety-critical · authority designation đổi → result cũ **VẪN là current eligibility evidence** tới một **explicit, bounded revalidation deadline đã pin**; trong cửa sổ đó subject **ĐƯỢC PHÉP** tiếp tục sinh authoritative Decision; **quá deadline chưa có result mới → fail-safe I-6**.
- **Hai rule khép kín áp cho cả hai lớp:** (a) **mở activation MỚI luôn cần result hợp lệ dưới policy/designation đang áp dụng** — "tiếp tục" ở lớp bounded chỉ nghĩa là duy trì activation đang tồn tại, không phải mở activation mới (Ch9 §9.5 phải validate tại chính boundary đó); (b) **không có deadline explicit + bounded + pin được thì KHÔNG thuộc lớp bounded**, mặc định rơi về immediate suspension — nếu không, "bounded revalidation" thành cửa hoãn vô thời hạn.

### Fixed — Major: grant reference/version chưa đủ chứng minh grant có hiệu lực tại boundary
- v2.5 mới pin `evaluator authorization/grant reference + version`. Nhưng **grant artifact tồn tại ≠ grant đang có hiệu lực**: reference không chứng minh grant là authoritative, đúng scope, đã active, chưa bị revoke tại boundary. Ví dụ hỏng: grant `G7` cấp cho evaluator `E` scope `Paper`, revoke tại T1; result tại T2 pin đúng `G7` + version nhưng cho scope `Live` vẫn trông hợp lệ. So với policy — vốn đã được pin **cả artifact lẫn applicability fact/frontier** (§10.4.3) — grant đang ở cấp chứng cứ thấp hơn.
- **Sửa §10.4.1:** grant phải pin **cùng cấp độ chứng cứ với policy** — grant identity + immutable version/content identity · declared grant scope · **canonical grant-authority designation version** (áp cùng quy tắc exactly-one authority của §10.4.3) · **authoritative grant activation/applicability fact hoặc frontier tại evaluation boundary** · bằng chứng grant chưa bị revoke và bao phủ đủ `policy version × subject scope × quyền phát hành result × boundary`. Khóa thêm nguyên tắc song song: `module identity ≠ authorization` **và** `grant artifact tồn tại ≠ grant đang có hiệu lực`. Grant không resolve được authority/applicability, sai scope, chưa active hoặc đã revoke → **Result INVALID**, không vào validated compatibility set. Revoke **sau đó** không sửa result lịch sử (§10.4.4); §10.5.1 mới quyết định result còn dùng được cho current eligibility hay không. Cập nhật điều kiện invalid-result tương ứng.

### Checklist
- Ch10 v2.6 · 17 heading đúng thứ tự · **0 heading bị nuốt/trùng** (`## 10.6` = 1 — áp bài học v2.2/v2.5, đưa heading vào `new_str`) · **0 tham chiếu §10.x gãy** · grep xác nhận **0 occurrence** của cả hai câu gây mâu thuẫn ("cho tới activation boundary kế tiếp" · "hay để sinh authoritative Decision qua đường phụ thuộc result cũ") · version file ↔ MANIFEST đồng bộ.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 7 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 10 v2.5 (ChatGPT review round 5: **1 Blocker · 1 Major · 0 Minor · 0 Suggestion mới**)

### Note — phản biện phần meta của review (finding kỹ thuật chấp nhận toàn bộ)
Review round 5 mở đầu bằng nhận định *"repo chưa có version mới so với lượt review trước"* và *"review outcome giữ nguyên"*, cho rằng Claude dán lại phản hồi cũ. **Không khớp lịch sử repo:** round 3 review blob `88aadebea9d85cc51f58cb8a7a313b21148ed67d` = **v2.3** (reviewer tự ghi "Chapter 10 v2.3 · Revision Requested", 0 Blocker · 2 Major); hai Major đó đã được sửa trong commit `2d84f92` → **v2.4** = blob `a42dd9851d27a112935f08de7691f2421e6565bb`, hiện là remote HEAD. Blob reviewer đang cầm **chính là v2.4 mới**, không phải bản đã review. Hai finding của round 5 (**evaluator grant provenance** · **transition semantics**) chưa từng xuất hiện ở round 3 → đây là **review mới của v2.4**, không phải outcome cũ lặp lại. Đã đối chiếu bằng `git log` + `git rev-parse <commit>:<path>` + `git ls-remote` trước khi ghi note này.

### Fixed — Blocker: Compatibility Result pin evaluator identity/artifact nhưng không pin authorization/grant
- **Propagation gap lần thứ ba trong Chapter 10** (sau: exact artifact ở Ch9 vòng 8, authority designation ở Ch10 vòng 4). §10.4.1 đã khóa "quyền đánh giá là **grant**, registry membership là *identity* không phải *grant*", §10.4.3 mục 7 đã khóa "evaluator chỉ được dùng policy version đã được grant cho scope đó" — nhưng danh sách pin bắt buộc của result **không có grant reference**. Hệ quả: rule tồn tại nhưng **không kiểm chứng được từ chính result**; một evaluator ngoài phạm vi được cấp quyền vẫn phát hành được result trông hợp lệ và mở activation boundary.
- **Sửa §10.4.1:** thêm **evaluator authorization/grant reference + version** vào danh sách pin bắt buộc, chứng minh evaluator thực sự được quyền (a) dùng đúng policy version đó · (b) đánh giá đúng subject scope đó · (c) phát hành eligibility result tại đúng boundary đó. Khóa nguyên tắc `module identity ≠ authorization`: pin identity/artifact chỉ trả lời *ai đã chạy phép đánh giá*, không trả lời *người đó có quyền không*. Grant phải là **versioned reference** (Ch9 §9.6 Grant layer, `granted ⊆ declared`), không phải khẳng định trong prose. Bổ sung grant version vào điều kiện invalid-result.

### Fixed — Major: chưa khóa transition semantics khi subject đang active
- §10.5 nói *khi nào* phải đánh giá nhưng không nói **điều gì xảy ra với subject đang active** khi nền tảng kết luận cũ thay đổi (evaluator grant đổi/revoke · policy applicability đổi · authority designation đổi). Không khóa thì mỗi implementation tự chọn giữa "kết luận cũ có hiệu lực vô hạn" và "chặn ngay".
- **Sửa — thêm §10.5.1.** Bất biến chung cho cả ba loại transition: **historical result KHÔNG đổi**, vẫn diễn giải dưới đúng grant/policy/designation đã pin; transition không hồi tố. Với eligibility **hiện hành**, khóa mô hình **`revalidation-required`** (không phải `prospective-only`) — lý do: eligibility là tuyên bố về **trạng thái hiện tại**, không phải sự kiện quá khứ; prospective-only sẽ để một evaluator đã bị revoke tiếp tục "bảo lãnh" subject đang chạy, mâu thuẫn §10.4.1 và I-6. Bảng hiệu lực theo từng loại: **grant revoke → hiệu lực ngay**, result đó hết dùng được làm eligibility evidence, chờ revalidate thì fail-safe I-6 phạm vi nhỏ nhất đủ · **policy applicability đổi → revalidate chậm nhất tại activation boundary kế tiếp**, trừ khi policy phân loại là **safety-critical** thì hiệu lực ngay · **designation đổi → diễn giải lịch sử giữ nguyên**, đánh giá mới dùng designation mới, subject active revalidate chậm nhất tại boundary kế tiếp. **Phân loại safety-critical phải khai báo sẵn trong policy, versioned — cấm quyết ad hoc lúc sự cố** (nếu không sẽ thành lối thoát hoãn revalidation vô thời hạn). Trong cửa sổ chờ result mới: subject không được coi eligible để mở activation mới hay sinh authoritative Decision qua result cũ. Cơ chế (drain, grace window có bound, coordinator) defer Phase 1; **semantic khóa ở Chapter 10**.

### Fixed — lỗi biên tập nội bộ (Claude tự phát hiện, lặp lại lỗi v2.2)
- Khi chèn §10.5.1, thao tác `str_replace` **lại nuốt mất header §10.6** — đúng lỗi đã xảy ra ở v2.2 khi chèn §10.4.3. Lần này bắt được **ngay lập tức** vì đã đưa "grep header sau mỗi lần chèn" thành bước bắt buộc từ v2.2; header đã khôi phục, verify xác nhận `## 10.6` xuất hiện đúng 1 lần và 17 heading đúng thứ tự. **Bài học nâng cấp:** khi `old_str` là một heading, phải luôn đưa heading đó vào `new_str` — không dựa vào việc nhớ.

### Checklist
- Ch10 v2.5 · 17 heading đúng thứ tự §10.1→§10.9 (+ 10.3.1 · 10.4.1→10.4.4 · **10.5.1** · 10.8.1 · 10.8.2) · **0 heading bị nuốt/trùng** (`## 10.6` = 1) · **0 tham chiếu §10.x gãy** · 0 peer authority · version file ↔ MANIFEST đồng bộ.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 6 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 10 v2.4 (ChatGPT review round 4: **0 Blocker · 2 Major · 0 Minor · 0 Suggestion mới**)

Không có phản biện; 2 finding chấp nhận toàn bộ. **0 Blocker lần đầu ở Chapter 10.**

### Fixed — Major 1: authority designation đã version hóa nhưng Compatibility Result chưa pin designation đã dùng
- **Lại là propagation gap** — cùng lớp lỗi với vòng 8 của Chapter 9 (§9.1 khóa exact artifact nhưng §9.5 activation set không pin). v2.3 khóa ở §10.4.3 rằng designation của canonical authority phải version hóa + governance phê duyệt, nhưng §10.4.1 provenance không bắt result pin designation nào đã được dùng. Hệ quả: `T1: designation D1 → authority X trả lời "policy nào active"` · result ghi `policy=compat-v3 · boundary=T1 · eligible=true` · sau đó đổi sang `D2 → authority Y` → audit có thể dùng D2 **tái diễn giải** applicability tại T1, kết luận đổi hồi tố.
- **Sửa §10.4.1:** thêm vào danh sách pin bắt buộc — **canonical authority designation version cho policy identity/version** · **canonical authority designation version cho runtime applicability trong subject scope** · **authoritative applicability/activation fact hoặc frontier đã resolve tại evaluation boundary** (bằng chứng policy thực sự active trong scope lúc đánh giá). Ghi rõ vì sao exact-pin policy artifact là chưa đủ: *"policy content là gì"* và *"policy đó có authority + đang active trong scope lúc đánh giá không"* là **hai fact khác nhau**. Khóa thêm: **designation đổi về sau KHÔNG được làm thay đổi cách diễn giải một Compatibility Result lịch sử**. Bổ sung designation version vào điều kiện invalid-result.

### Fixed — Major 2: Capability Matrix mới là execution-mode readiness matrix, chưa bao phủ capability semantics của chính Chapter 10
- §10.2 đã tách 3 loại capability (Business · Required platform · Provided contract) nhưng §10.8 chỉ ghi execution mode → Matrix không trả lời được subject có năng lực cụ thể nào, năng lực nào declared, năng lực nào validated, requirement nào đang được đáp ứng. Một component có thể `Live = validated` trong khi thiếu `cursor-bounded historical projection` hoặc `multi-venue routing`; provider bỏ một provided capability mà ô `Live = validated` vẫn đứng nguyên — snapshot dù bất biến vẫn quá thô để giải thích readiness.
- **Sửa §10.8:** Matrix có **hai chiều** — **capability assertions** (required platform capability · provided contract capability · business-capability implementation mapping khi liên quan) và **execution-mode readiness** (Backtest · Replay · Paper Trading · Live). **Execution-mode readiness là projection/kết luận dẫn xuất từ capability assertion**, không phải cờ độc lập. Mỗi validated mode readiness phải exact-pin hoặc resolve tới capability requirement set · provider capability set · Compatibility Result/evidence · policy/evaluator/boundary. **`Live = validated` là invalid nếu không resolve được tập capability requirement/provider evidence làm căn cứ.** Mở rộng §10.8.1: rule declared ≠ validated áp cho **cả capability assertion lẫn execution-mode readiness**, không chỉ mode.
- **Vẫn không đóng OQ-002** — chỉ bảo đảm "Live readiness" có nghĩa kỹ thuật đầy đủ trước khi Quality Gate dùng nó.

### Checklist
- Ch10 v2.4 · 16 heading đúng thứ tự §10.1→§10.9 (+ 10.3.1 · 10.4.1→10.4.4 · 10.8.1 · 10.8.2), không mục nào bị nuốt/trùng · **0 tham chiếu §10.x gãy** · **0 cấu trúc peer authority** · version file ↔ MANIFEST đồng bộ.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 5 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 10 v2.3 (ChatGPT review round 3: **1 Blocker · 1 Major · 0 Minor · 0 Suggestion mới**)

Không có phản biện; 2 finding chấp nhận toàn bộ.

### Fixed — Blocker: Compatibility Policy vẫn có competing authority qua cấu trúc "A hoặc B"
- **Đây là lặp lại đúng lớp lỗi peer authority mà Chapter 9 đã mất hai vòng để loại bỏ** (`Input Contract HOẶC decision-dependency contract`), lần này ở tầng policy. v2.2 ghi identity authority là "Policy Contract **hoặc** registry", và runtime activation thuộc "**event/configuration** authority" — cả hai đều cho phép hai nguồn cùng trả lời một loại sự thật. Hệ quả: `Policy Contract: v3 active` vs `registry: v2 active`, hoặc `event log: POLICY_V3_ACTIVATED` vs `config: active_policy = v2` — evaluator chọn được nguồn thuận lợi, cùng một subject cho ra hai kết luận eligibility trái ngược, phá I-12 và phá chính evaluation provenance vừa khóa ở §10.4.1.
- **Sửa §10.4.3 mục 3-4:** khóa **cardinality**, không chọn technology — mỗi loại policy fact, trong mỗi declared scope, **đúng một canonical authority**. Identity/definition/version: **cấm** tồn tại Contract và registry như hai peer source. Runtime applicability: configuration **có thể** là desired-state input, event log **có thể** là recorded transition, nhưng **chỉ một nguồn là canonical current/historical truth**; nguồn còn lại không được tự tạo competing activation fact. **Designation phải version hóa + governance phê duyệt**; thiếu designation hoặc có nhiều peer authority → **policy reference invalid** → `eligible = false` (I-6), reason ghi *invalid*/*không resolve được*. Mô hình cụ thể defer Phase 1. Cập nhật dòng authority tương ứng ở §10.1.
- **Siết thêm (Claude chủ động, cùng lớp lỗi):** hai chỗ còn dùng "Domain Contract / registry" cho tên capability/schema đã đổi thành "registry/Contract được designate cho **chính loại khai báo đó** — mỗi loại đúng một, không phải lựa chọn giữa nhiều nguồn", để pattern này không tái phát ở vòng sau.

### Fixed — Major: Capability Matrix là input authoritative nhưng chưa có authority, version, provenance
- §10.8 đã pin subject scope tốt, nhưng chưa nói ai sở hữu Matrix, entry là declaration hay validated result, ai được ghi "supports Live", Matrix có version/content identity không, update ghi đè hay tạo version mới, gate pin được snapshot nào. Rule chống self-certification đã áp rất chặt cho Compatibility Result **nhưng chưa áp cho Capability Matrix** — một plugin tự khai `Live = YES` đi thẳng vào input của lifecycle gate mà chưa có evaluator, policy, evidence hay approval.
- **Sửa — thêm §10.8.1:** tách **Declared support** (component tuyên bố thiết kế hỗ trợ mode nào — **không tự tạo eligibility**) khỏi **Validated capability/readiness** (đã đánh giá bằng policy/evidence, mới được dùng làm căn cứ readiness); hai lớp không được gộp trong cùng một ô "supports: yes". Validated entry phải pin: subject identity/version/artifact/config · evaluation policy/result hoặc evidence reference · evaluator/verification authority (quyền đánh giá là **grant**, không tự nhận) · validation boundary/time · immutable matrix version hoặc source frontier.
- **Thêm §10.8.2:** Matrix phải là **versioned resolvable artifact** hoặc **projection của authoritative source đã designate** (nếu projection thì phải chỉ ra source frontier/version như mọi projection dùng cho quyết định — Ch7 §7.4). Update **không được ghi đè lịch sử**; **gate phải pin đúng snapshot đã dùng tại thời điểm đánh giá**, không đọc "matrix hiện tại" (nếu không, kết luận của gate đổi hồi tố theo trạng thái sau này); reference không resolve được về version/frontier cụ thể → không dùng làm input cho gate, xử lý theo §10.4.2.
- **Không đóng OQ-002:** ghi rõ §10.8.1/§10.8.2 chỉ bảo đảm thứ đưa sang lifecycle gate không phải một bảng mutable tự khai; *khi nào* được lên Live vẫn thuộc OQ-002/Quality Gates.

### Checklist (áp bài học v2.2 — grep toàn bộ heading, không chỉ phần vừa thêm)
- Ch10 v2.3 · 16 heading đúng thứ tự §10.1→§10.9 (+ 10.3.1 · 10.4.1→10.4.4 · 10.8.1 · 10.8.2), không mục nào bị nuốt/trùng · **0 tham chiếu §10.x gãy** (10 ref đều tồn tại) · **0 cấu trúc peer authority "A hoặc B"** còn lại · 0 hardcode technology/tên file.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 4 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 10 v2.2 (ChatGPT review round 2: **1 Blocker · 2 Major · 1 Minor · 0 Suggestion mới**)

Reviewer đã rút lại nhận định sai về metadata Chapter 9 ở vòng trước — repo đã đồng bộ đầy đủ quyết định Lock của Kanner. Không có phản biện nào ở vòng này; 4 finding chấp nhận toàn bộ.

### Fixed — Blocker: Compatibility policy/rule-set được pin nhưng chưa có authority/identity/lifecycle
- v2.1 bắt Compatibility Result pin `compatibility policy/rule-set version` (§10.4.1) nhưng toàn chapter không định nghĩa policy đó là artifact gì, ai sở hữu identity, ai được tạo version, nằm registry nào, có immutable content identity không, version transition thành authoritative bằng cách nào, rule-set nào active cho scope nào. Provenance có **field** nhưng chưa có **gốc**: hai result cùng ghi nhãn `compat-v2` vẫn có thể chạy hai bộ luật khác nhau, và một result có thể tự khai `policy_version` không tồn tại rồi thành vé activation. **Đúng cùng lớp lỗi "pin một thứ chưa được định nghĩa đầy đủ" đã gặp ở v1.0** — lần này ở tầng policy thay vì tầng result.
- **Sửa — thêm §10.4.3:** Compatibility Policy là **versioned immutable authoritative artifact** với 7 yêu cầu: stable logical identity + immutable version/content identity (**exact-pin**, cấm nhãn version tự do) · declared scope (result ngoài scope policy nó viện dẫn = invalid) · identity/definition authority thuộc **Compatibility Policy Contract/registry được governance phê duyệt** (Constitution khóa yêu cầu, không tự tạo registry, không hardcode tên file; ghi rõ **Chapter 10 là luật cấp cao, không tự động trở thành runtime policy artifact**) · runtime activation/applicability là **runtime fact** thuộc event/configuration authority theo I-12 · lifecycle transition authoritative, **cấm mutate nội dung dưới cùng version identity** · historical content immutable + resolvable theo horizon · **evaluator chỉ được dùng policy version đã được grant cho scope đó** (nối tiếp rule chống self-certification). Thêm dòng authority tương ứng vào bảng §10.1. Nêu **phương án thay thế** được chấp nhận: exact-pin version của Chapter 10 + tập format-specific rules, miễn có root path authoritative và machine-resolvable.

### Fixed — Major
- **"Historical Compatibility Result giữ nguyên vĩnh viễn" lệch retention horizon model:** §10.4 chỉ yêu cầu resolvable trong horizon cam kết, còn Chapter 8 dùng mô hình "persistently resolvable trong committed horizon, hết horizon → explicit retention/archive policy". "Không mutate lịch sử" và "giữ object online vô hạn" là hai việc khác nhau; Constitution không nên cam kết infinite retention. **Sửa:** bỏ từ "vĩnh viễn"; thêm **§10.4.4** — result và policy version là immutable (không sửa/ghi đè/hồi tố) · phải resolve trong toàn bộ replay/audit horizon cam kết · sau horizon tuân explicit retention/archive policy · nếu archive thì reference lịch sử vẫn phải có cách xử lý đúng theo policy đã công bố, không được thành dangling reference im lặng.
- **Thiếu compatibility direction chưa được khóa thành hành vi:** §10.3.1 nói "contract phải khai báo chiều bắt buộc; không khai báo thì không suy diễn mặc định" — đúng nguyên tắc nhưng chưa khóa hệ quả, nên mỗi team vẫn tự chọn mặc định riêng (backward / unknown-nhưng-vẫn-cho-minor / invalid). **Sửa:** contract trong phạm vi compatibility evaluation mà không khai báo chiều bắt buộc → **invalid declaration** → không được chứng nhận compatible → `eligible = false` theo I-6, reason ghi *khai báo invalid*/*không đủ policy*, **không** ghi *đã chứng minh không tương thích*. Cho phép contract tuyên bố **tường minh** là không cam kết chiều nào — nhưng phải là declaration, không phải field vắng mặt.

### Fixed — Minor
- **Capability Matrix pin `configuration/profile` nhưng profile name có thể trỏ tới mutable config:** `live-default` hôm nay bật Live, tuần sau cùng profile đó có thể đã đổi → entry không còn resolve đúng snapshot đã đánh giá. **Sửa §10.8:** phải pin **configuration/profile identity + immutable configuration version hoặc content identity**, không chỉ tên profile.

### Fixed — lỗi biên tập nội bộ (Claude tự phát hiện khi verify)
- Khi chèn §10.4.3, thao tác `str_replace` đã **nuốt mất header §10.4.2**, làm phần Reason classification dangling dưới §10.4.4 và sai thứ tự. Phát hiện qua grep header sau khi sửa; đã khôi phục header đúng vị trí (sau §10.4.1, trước §10.4.3) và xóa khối bị nhân đôi. **Bài học quy trình:** sau mỗi lần chèn tiểu mục mới, phải grep lại toàn bộ heading để xác nhận thứ tự và không mất mục — không chỉ kiểm nội dung vừa thêm.

### Checklist
- Ch10 v2.2 · §10.1→§10.9 liên tục · §10.4.1→§10.4.4 đủ 4 tiểu mục, đúng thứ tự, không trùng lặp · **0 tham chiếu §10.x gãy** (§10.4 · 10.4.1 · 10.4.2 · 10.4.3 · 10.4.4 · 10.7 · 10.9 đều tồn tại) · 0 occurrence "vĩnh viễn" · 0 hardcode tên file/registry · Compatibility Policy có authority row trong §10.1.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 3 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 10 v2.1 (ChatGPT review round 1: **1 Blocker · 3 Major · 1 Minor · 0 Suggestion mới**)

### Note — phản biện một điểm phi kỹ thuật trong review
Review kết luận *"GitHub metadata Chapter 9: vẫn cần atomic transition phản ánh quyết định"*. **Điểm này không đúng với trạng thái repo:** commit `cec4f1e` (trước commit Chapter 10 v2.0) đã thực hiện atomic transition — `09-plugin-model.md` trên `main` hiện là `version: 2.9 · status: Locked · approved_by: Kanner · approved_at: 2026-07-24`, MANIFEST ghi `**Locked**`, CHANGELOG có entry `[Milestone]`. Đã fetch lại remote `main` để xác minh trước khi ghi note này. Reviewer có thể đã đọc snapshot Ch9 cũ hơn `cec4f1e`. Không có hành động nào cần thực hiện thêm cho Chapter 9. **5 finding kỹ thuật còn lại: chấp nhận toàn bộ, không phản biện.**

### Fixed — Blocker: Compatibility Result pin subject nhưng không pin evaluation provenance
- v2.0 yêu cầu result immutable + pin input + kết luận nhị phân, nhưng **không** yêu cầu pin rule-set/evaluator. Cùng một bộ input có thể cho kết luận ngược nhau dưới hai compatibility rule-set khác nhau — result chỉ ghi `inputs + eligible=true` không trả lời được luật nào đã áp, ai đánh giá, người đánh giá có thẩm quyền không, result sinh trước hay sau rule transition. Vì Ch9 §9.5 dùng result này để **mở activation boundary**, thiếu provenance biến nó thành **"vé eligible" tự chứng nhận**.
- **Sửa — thêm §10.4.1:** result phải pin bất biến subject scope · input references · **compatibility policy/rule-set version** · **evaluator module identity** · **evaluator implementation version + exact artifact/manifest** · evaluation time/boundary · result + reason + evidence refs. Result không resolve được evaluator identity/artifact/rule-set/scope thì **không hợp lệ và không được đưa vào validated compatibility set**. Ghi rõ đây cùng nguyên tắc Ch3 §3.1 (Locked): parity phải pin implementation version + configuration + **policy version** + contract, không chỉ pin dữ liệu vào.
- **Chống self-certification:** component đang được đánh giá không mặc định tự cấp eligibility cho chính nó; **registry membership là identity, KHÔNG phải grant** — quyền đánh giá phải qua đúng phân tầng Declaration → Grant → Enforcement → Verification của Ch9 §9.6 với `granted ⊆ declared`. Self-evaluation chỉ hợp lệ khi authorization model cho phép tường minh + có independent verification.

### Fixed — Major
- **Trigger "provider đổi contract/capability mà consumer đang pin" gây revalidation hồi tố:** wording cũ có thể bị đọc thành "provider publish version mới → activation lịch sử phải xét lại", phá immutable reference và independent versioning. **Sửa §10.5:** trigger đúng là **transition của binding/resolution**, không phải sự tồn tại của version mới — consumer đổi pinned reference · active binding resolve sang version/artifact khác · artifact/contract đã pin bị explicit revoke hoặc mất resolvability · permission/capability grant đổi · compatibility policy đổi · runtime đổi exact artifact · startup. Ghi rõ: provider publish version mới **KHÔNG** phải trigger; **historical Compatibility Result giữ nguyên vĩnh viễn**, đánh giá mới sinh result mới cho boundary mới, không hồi tố.
- **Schema compatibility delegation từ Ch8 §8.6 chưa đủ semantic để triển khai nhất quán:** v2.0 chỉ định nghĩa breaking change theo contract surface chung, chưa khóa các trường hợp schema evolution phổ biến — hai team cùng nói "SemVer nghiêm ngặt" vẫn phân loại ngược nhau (thêm required field không default: minor hay major?). **Thêm §10.3.1** semantic độc lập format: định nghĩa backward/forward compatibility và breaking theo **chiều mà contract yêu cầu** · nguyên tắc tối thiểu cho optional/required element, remove/rename/type/nullability/default/đổi ý nghĩa, enum expansion/contraction theo từng chiều, deprecated-rồi-gỡ · hai điều cấm suy diễn: `schema_version` bump không tự chứng minh compatibility, major bump không tự làm thay đổi trở nên an toàn. Rules theo format cụ thể (JSON Schema/Avro/Protobuf) defer Domain Contract/Phase 1.
- **Unknown impact bị ghi thành proved incompatibility:** §10.7 nói không resolve được tập consumer thì "kết quả là incompatible" — đúng về hành vi chặn, sai về semantic, và mâu thuẫn nhẹ với kết luận nhị phân ở §10.4. **Thêm §10.4.2:** eligibility vẫn nhị phân, nhưng **reason classification bắt buộc phân biệt** *đã chứng minh tương thích* · *đã chứng minh không tương thích* · *không đủ evidence* · *khai báo invalid* · *reference không resolve được* · *policy mismatch*. Quy tắc: không chứng minh được tương thích → `eligible = false` (fail-safe I-6) **nhưng không được ghi thành "đã chứng minh không tương thích"** — chặn đúng mà ghi sai lý do là mất explainability (I-1). Sửa §10.7 tương ứng.

### Fixed — Minor
- **Capability Matrix chưa pin version/artifact scope:** v2.0 nói Matrix ghi nhận "với mỗi module/plugin", nhưng capability đổi theo Plugin Version, artifact/target platform và configuration/profile — gắn ở logical level tạo declaration quá rộng. **Sửa §10.8:** mỗi entry phải pin subject identity đủ cụ thể (Definition · **Plugin Version** · artifact/target discriminator khi capability phụ thuộc build/platform · configuration/profile khi phụ thuộc config); **cấm suy capability của mọi version/artifact chỉ từ Plugin Definition** — trái yêu cầu exact-artifact eligibility Ch9 §9.5.

### Đánh giá của reviewer về §10.4/§10.5
Claude nêu lo ngại hai section này có thể lấn Phase 1. Reviewer kết luận §10.4 là **semantic invariant**, đúng chỗ ở Constitution; §10.5 đúng ý tưởng nhưng cần khóa theo **state transition ảnh hưởng binding**, không theo hành động "provider đổi" nói chung — đã sửa đúng hướng đó.

### Checklist
- Ch10 v2.1 · §10.1→§10.9 liên tục (+ §10.3.1 · §10.4.1 · §10.4.2) · **0 tham chiếu §10.x gãy** (§10.4 · §10.4.1 · §10.4.2 · §10.7 đều tồn tại) · 0 hardcode tên/schema · 0 authority mới · historical result bất biến, không hồi tố.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 2 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 10 (Compatibility & Capability Contract) v2.0 — Claude tự review (**2 Blocker · 5 Major · 2 Minor · 1 Suggestion**)

Chapter 10 v1.0 viết 2026-07-16, **trước khi** Chapter 2-9 được Locked, dài 32 dòng — chưa hấp thụ bất kỳ model nào đã khóa từ đó. Self-review đối chiếu toàn bộ Chapter 2/3/4/7/8/9 Locked.

### Fixed — Blocker
- **`compatibility result` là thứ Chapter 9 (Locked) pin nhưng Chapter 10 chưa định nghĩa tồn tại:** Ch9 §9.5 khóa `required capability/compatibility result` là thành phần của validated compatibility set tại activation boundary, nhưng v1.0 chỉ nói "Plugin Loader kiểm tra lúc startup" — kết quả kiểm tra sống trong bộ nhớ, không pin được. Thêm **§10.4**: compatibility result phải bất biến · có content identity + resolvable trong replay/audit horizon (thỏa Referenced Authoritative Artifact rules Ch8 §8.1.1) · pin đủ input đã đánh giá (Plugin Version · exact artifact/manifest + target discriminator · contract refs · capability requirement set · version phía cung cấp) · kết luận nhị phân trong phạm vi đã khai báo, không có trạng thái "một phần" ngầm. Cấm suy lại từ trạng thái runtime; đánh giá lại sinh result mới, không hồi tố hợp thức hóa activation đã xảy ra.
- **Hardcode module/capability name + schema format, tạo authority cạnh tranh với Ch4 và Ch7 (Locked):** khối JSON dùng `StructureEngine` (module identity → thuộc `module-registry.yaml`, Ch7 §7.5) và `SWING_STRENGTH/BOS/CHOCH` (capability/domain concept → Ch4 §4.2 khóa mọi `capability_id` phải tồn tại sẵn trong `context-map.yaml`; Domain Contract còn không được tự đặt). Đây đúng lớp lỗi Ch9 §9.3 đã khóa ("không hardcode tên file hay format trong Constitution" — bài học I-2 field list, I-13 state machine, ADR-008). Xóa toàn bộ khối JSON; thay bằng **§10.1 bảng ranh giới thẩm quyền** trỏ mọi identity về registry sở hữu nó.

### Fixed — Major
- **"capability" bị dùng cho 3 khái niệm khác nhau:** Business Capability (Ch4, có version theo Ch3 §3.1) · Required platform capability (Ch9 §9.6) · Provided contract capability. Gộp phẳng thì so khớp mất nghĩa. Thêm **§10.2** tách 3 loại + authority của từng loại; reference tới capability chưa đăng ký = invalid declaration.
- **`schemaVersion` xung đột Ch8 §8.2.5 (Locked):** Ch8 khóa `schema_version` **không** phải proxy cho Event Contract version, hai trục tiến hóa độc lập; v1.0 gộp thành một trục và viết sai canonical field name. **§10.3** khóa 3 trục độc lập (Event Contract version · `schema_version` · Plugin Version), cấm dùng trục này làm proxy trục kia.
- **SemVer không nói áp cho tầng identity nào:** Ch9 khóa 4 tầng Definition/Version/Artifact/Runtime. **§10.3** khóa SemVer áp cho **Plugin Version**, và định nghĩa breaking change theo **published contract surface** (không theo internal implementation); cấm bump major "cho an toàn" khi contract surface không đổi. Bỏ cách nói "mỗi Engine" (bỏ sót Projection + Runtime Service của Ch7).
- **Dangling delegation — ba chapter Locked trỏ vào khoảng trống:** Ch3 §Engineering Foundation nói SemVer schema/capability "đã có **đầy đủ**" ở Ch10 · Ch8 §8.6 delegate schema versioning/compatibility · Ch9 §9.7 delegate SemVer, capability declaration, Capability Matrix, hành vi khi không khớp **và** downstream impact rules. v1.0 không có định nghĩa breaking change, không có dependency impact rule nào. **§10.1** liệt kê tường minh các delegation nhận được; **§10.6** (hành vi khi không khớp) và **§10.7** (downstream impact assessment) lấp đúng phần còn trống.
- **"Plugin Loader" là authority mới đặt bằng prose:** không thuộc taxonomy nào của Ch7, không có trong registry, nhưng được giao quyền chặn — trái phân tầng Declaration/Grant/Enforcement/Verification đã khóa ở Ch9 §9.6. **§10.1** khóa: Chapter 10 KHÔNG tạo authority mới, Constitution không đặt tên component, enforcement đi qua đúng phân tầng Ch9.

### Fixed — Minor
- **Capability Matrix có nguy cơ đóng ngầm OQ-002:** v1.0 nói Matrix "dùng làm tiêu chí readiness cho production", trong khi Ch9 §9.10 khóa không đóng ngầm OQ-002 (vẫn `Open`, thuộc Quality Gates/Strategy Lifecycle). Danh sách của v1.0 (Replay/Live/Backtest/Multi-Exchange) cũng lệch OQ-002 (Backtest + Paper Trade) và lệch execution mode canonical Ch3 §3.1. **§10.8**: Ch10 sở hữu cấu trúc/semantic của Matrix, execution mode canonical thuộc Ch3 §3.1, Matrix là **input** cho lifecycle gate chứ không phải bản thân gate — "hỗ trợ Live" ≠ "được phép lên Live".
- **`depends_on` thiếu:** chỉ khai `09-plugin-model` dù nội dung chạm trực tiếp Ch2 (I-6, I-7 verification), Ch3 (execution mode, authoritative implementation), Ch4 (capability registry), Ch7 (module registry/taxonomy), Ch8 (schema/contract version). Bổ sung đủ 6, đồng bộ MANIFEST.

### Fixed — Suggestion
- **"fail-fast lúc startup" chưa nối vào I-6:** I-6 (Locked) là fail-safe **theo scope**, phạm vi nhỏ nhất nhưng đủ. **§10.6** diễn đạt lại theo I-6, ghi rõ không mặc định dừng toàn platform vì một plugin không critical, cũng không thu hẹp scope tới mức để ảnh hưởng lan ra ngoài. Thêm: cấm degrade ngầm (tự bỏ capability/hạ version/chạy với subset = mixed-state activation) · mọi từ chối phải để lại evidence resolvable (I-1) · không khớp không tự động là việc cần ADR.

### Added — §10.5 điểm đánh giá bắt buộc
Startup-only là không đủ. Bắt buộc đánh giá tại tối thiểu: đăng ký Plugin Version/artifact mới · **activation boundary** của decision-relevance promotion (Ch9 §9.5) · runtime deployment đổi artifact/target **kể cả rebuild cùng Plugin Version** (nếu không, mixed-build activation mà Ch9 vừa khóa là integrity violation sẽ không có điểm phát hiện) · provider đổi contract/capability mà consumer đang pin · startup.

### Checklist
- Ch10 v2.0 · §10.1→§10.9 liên tục · **0 tham chiếu §10.x gãy** · grep xác nhận 0 hardcode (`StructureEngine` · `SWING_STRENGTH/BOS/CHOCH` · `Plugin Loader` · `schemaVersion`) · mọi link target tồn tại · 0 authority mới được tạo · OQ-002 không bị đóng ngầm.

### Note
- Đây là **self-review của Claude**, chưa qua ChatGPT. Không tự tuyên bố Approve. Chờ ChatGPT review round 1 và Product Owner Approve/Lock.

## [Milestone] — 2026-07-24 — 🔒 Chapter 9 (Plugin Model) LOCKED

**Product Owner (Kanner) xác nhận Approve & Lock** Chapter 9 v2.9, theo khuyến nghị reviewer (ChatGPT round 9: 0 Blocker · 0 Major · 0 Minor · 0 Suggestion, Consolidation Review + Backward Consistency Check toàn bộ Chapter 0-8 đạt).

`status: In Review → Locked` · `approved_by: null → Kanner` · `approved_at: null → 2026-07-24`.

### Quy mô công việc
Chapter 9 trải qua **10 revision** (v2.0 Claude tự review → v2.9), tương ứng **9 vòng review ChatGPT** (round 1-9) sau vòng self-review ban đầu. Các model đã khóa:

- **Identity — 4 tầng tách biệt:** Plugin Definition (logical/taxonomy) ≠ Plugin Version (immutable release) ≠ Package/Build Artifact (immutable bytes + content hash) ≠ Plugin Runtime (deployment/replica); Strategy Definition ≠ Strategy Instance, khớp ba-thứ-tách-riêng của ADR-010 (strategy/model version · instance · configuration version).
- **Module Taxonomy:** registry chỉ sở hữu module type/definition, không bao giờ sở hữu Strategy Instance runtime fact (hosted hay independently operated); `strategy_instance_id ≠ module_id`; lifecycle instance authoritative trong event log (I-12).
- **Strategy cardinality:** một Strategy Definition có thể có nhiều implementation (authoritative/shadow/experimental/migration), đúng một authoritative trong mỗi execution/parity scope — khớp Chapter 3 Locked.
- **Decision input authority:** Input Contract là root authority duy nhất mà `decision_context_cursor` pin; dependency contract chỉ có hiệu lực như subordinate immutable artifact exact-pinned, không còn peer authority/hidden-input path.
- **Decision-relevance promotion:** contract declaration (không suy runtime) · cấm silent reclassification · 4 điều kiện visibility precondition · authoritative atomic activation boundary với validated compatibility set (Plugin Contract version · Input Contract version · published refs · permission grant version · capability result · runtime deployment version · **exact Package/Build Artifact hoặc immutable manifest + target discriminator**) · mixed-version/mixed-build activation = integrity violation, fail-safe I-6.
- **Permission boundary 4 tầng:** Declaration · Grant · Enforcement (runtime) · Verification; `granted ⊆ declared`; plugin không bao giờ được cấp exchange credential trực tiếp (I-11).
- **Versioning:** độc lập với platform/plugin khác nhưng "independent versioning ≠ zero downstream impact" — impact đánh giá qua Chapter 10.
- **Governance/runtime split:** forbidden-pattern table tách rõ phần runtime-enforceable (có cột phát hiện/chặn) khỏi phần thuộc governance/process; ADR Required giới hạn đúng architecture change, không chặn operational action (§9.10).

### Deferred sang Phase 1 design spec
Fencing/transaction mechanism cho activation boundary · deployment coordinator · artifact retention/archive protocol cụ thể · Capability Matrix/compatibility algorithm chi tiết (Chapter 10 sở hữu).

**Đã Locked tới nay:** Chapter 0, 1, 2, 3, 4, 5, 6, 7, 8, **9** + ADR-005 → ADR-010.

**Next Milestone:** Chapter 10 — Compatibility & Capability Contract.

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

## [Unreleased] — Chapter 9 v2.9 (ChatGPT review round 8: **0 Blocker · 1 Major · 0 Minor · 0 Suggestion mới**)

### Fixed — Major: atomic promotion compatibility set chưa propagation exact Build Artifact
- §9.1 (v2.8) đã khóa Plugin Version một mình không đủ để xác định exact artifact đã chạy — nhưng `validated compatibility set` của atomic activation boundary ở §9.5 vẫn chỉ liệt kê `runtime implementation/deployment version`, không bắt buộc pin exact artifact/manifest. Hệ quả: activation boundary có thể mở đúng mọi version/contract/permission nhưng runtime lại đang chạy một rebuild khác (cùng Plugin Version, khác content hash) so với artifact đã parity-validate — evidence ghi lại sau khi chạy chỉ chứng minh artifact nào đã chạy, không chứng minh nó từng nằm trong tập được validate tại activation (cùng lớp lỗi với "published contract compliance ≠ decision-time visibility compliance").
- **Sửa:** thêm vào compatibility set — exact Package/Build Artifact content identity đã qua validation, hoặc immutable release manifest version/content identity + target platform/runtime discriminator resolve duy nhất tới artifact đó. Làm rõ: chỉ trùng Plugin Version không đủ eligibility. Mở rộng định nghĩa mixed-version activation để bao gồm **mixed-build activation** (runtime chạy artifact khác artifact đã validate dù cùng Plugin Version) → integrity violation, fail-safe. Làm rõ luôn: exact artifact hash trong Decision evidence phải khớp artifact đã có trong compatibility set được validate tại boundary, không chỉ khớp artifact đã chạy.

### Checklist
- Ch9 v2.9 · §9.1→§9.10 liên tục · **0 tham chiếu §9.x gãy** · atomic promotion compatibility set và §9.1 exact-artifact evidence giờ nhất quán hai chiều (evidence sau khi chạy ↔ eligibility tại activation).

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 9 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 9 v2.8 (ChatGPT review round 7: **0 Blocker · 2 Major · 0 Minor · 0 Suggestion mới**)

### Fixed — Major: Decision evidence pin Plugin Version chưa đủ để tái dựng exact implementation
- Một Plugin Version có thể có nhiều Package/Build Artifact (theo target platform, hoặc do rebuild), mỗi artifact content hash riêng. Pin chỉ Plugin Version không trả lời được artifact nào thực sự chạy, platform nào, build nào — Replay không verify được đúng binary lịch sử. **Sửa:** khóa Decision evidence phải pin Plugin Version **đồng thời** resolve bất biến tới exact Package/Build Artifact/immutable release manifest (content hash · target platform/runtime · build identity · dependency/runtime environment). Đưa ra 2 mô hình hợp lệ không hardcode schema: (A) Decision pin trực tiếp `plugin_definition_id · plugin_version · artifact_content_hash`; (B) `plugin_version` trỏ immutable release manifest exact-pin theo platform, Decision pin đủ discriminator để resolve qua manifest. Cũng làm rõ luôn 2 chỗ dùng lowercase "plugin implementation version" (§9.3) để trỏ về đúng tầng Plugin Version + yêu cầu exact-artifact mới.

### Fixed — Major: alias "Definition/Package" còn sót ở §9.1
- Dù §9.3 đã sửa ở v2.7, câu "Mỗi plugin (ở tầng Definition/Package)" ở §9.1 vẫn gộp ngược hai tầng vừa tách, ngay trong section đã khóa bốn tầng. Sửa thành "Mỗi Plugin Definition". Đã grep mở rộng toàn file theo đề xuất ChatGPT cho các alias khác (`Definition/Package` · `plugin implementation version` · `Strategy Plugin (Plugin Version)` · `runtime module type/definition`) — không còn alias sai; usage còn lại của "plugin implementation version" đã được làm rõ trỏ đúng tầng.

### Checklist
- Ch9 v2.8 · §9.1→§9.10 liên tục · **0 tham chiếu §9.x gãy** · grep xác nhận 0 alias `Definition/Package` · Decision evidence bắt buộc exact-artifact resolution, không chỉ Plugin Version.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 8 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 9 v2.7 (ChatGPT review round 6: **1 Blocker · 2 Major · 0 Minor · 0 Suggestion mới**)

### Note — checklist v2.6 "0 wording cũ còn sót" đã không chính xác
Checklist v2.6 tuyên bố "0 wording cũ còn sót" nhưng chỉ kiểm 3 cụm từ cụ thể (peer-authority OR · single-implementation · zero-impact) — không kiểm alias `Plugin Definition / Package` vẫn còn nguyên trong bảng §9.3 sau khi §9.1 đã tách 4 tầng. Đây là lỗi phạm vi kiểm tra (checklist hẹp hơn khẳng định), không phải sai fact về các mục đã kiểm. Ghi nhận để vòng sau kiểm rộng hơn: sau mỗi thay đổi thuật ngữ ở §9.1, phải grep toàn file cho alias cũ, không chỉ raw diff.

### Fixed — Blocker: `module-registry` và event log cùng có nguy cơ sở hữu Strategy Instance runtime identity
- v2.6 viết independently-operated Strategy Instance "có `module-registry` entry cho runtime component" — mâu thuẫn trực tiếp với §9.8 (runtime lifecycle facts: created/activated/retired → authoritative event log; registry không phải runtime truth) và với Chapter 7 Locked (registry sở hữu module identity/taxonomy, không sở hữu deployment/instance fact). Kịch bản vỡ: instance retire → không rõ registry entry bị xóa/đổi hay giữ nguyên trong khi event log đã nói retired; scale thêm instance → phải sửa architecture registry cho một operational action, phá §9.10.
- **Sửa:** registry chỉ sở hữu **registered module type/definition**, không bao giờ sở hữu instance fact — dù hosted hay independently operated. Instance không tự tạo `module-registry` entry chỉ vì có deployment/scale riêng. Chỉ khi kiến trúc tạo ra một **module type mới** với published responsibility riêng (không chỉ thêm instance của type đã có) mới cần entry mới, và đó là architecture change thuộc diện ADR Required. `strategy_instance_id` luôn khác `module_id`; identity/lifecycle của instance luôn authoritative trong event log, không phụ thuộc operational boundary.

### Fixed — Major
- **§9.3 vẫn gộp `Plugin Definition / Package` sau khi §9.1 đã tách 4 tầng:** xóa alias, bảng ba-identity giờ chỉ dùng **Plugin Definition** (trỏ về 4 tầng ở §9.1); ghi rõ Package/Build Artifact và Plugin Runtime không thuộc bảng ba-identity domain/runtime này. Sửa luôn câu "Một Strategy Plugin (Plugin Version) phục vụ nhiều Strategy Instance" → "Một Plugin Version của một Plugin Definition có thể phục vụ nhiều Strategy Instance" — không dùng "Strategy Plugin" như alias cho Plugin Version.
- **§9.3 mở đầu "Vì Strategy Instance nằm ngoài `module-registry`" mâu thuẫn với §9.1 mới:** đổi thành "Strategy Instance identity không được lấy từ `module-registry`" — khớp mô hình module-type-vs-instance vừa khóa ở Blocker trên, không còn nói instance "nằm trong/ngoài" registry một cách mơ hồ.

### Checklist (mở rộng phạm vi kiểm tra sau lỗi ở v2.6)
- Ch9 v2.7 · §9.1→§9.10 liên tục · **0 tham chiếu §9.x gãy** · grep toàn file xác nhận 0 alias `Plugin Definition / Package` · 0 câu "nằm ngoài `module-registry`" · 0 exception clause cũ về independently-operated instance tự tạo registry entry · registry ↔ event log không còn competing authority cho instance fact.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 7 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 9 v2.6 (ChatGPT review round 5, actual: **2 Blocker · 4 Major · 1 Minor · 0 Suggestion mới**)

### Correction — entry v2.5 bên dưới ghi sai severity
Entry gốc cho v2.5 (giữ nguyên bên dưới, không xóa để tránh mất lịch sử) ghi **"0 Blocker · 0 Major · 1 Minor"** và note "ChatGPT khuyến nghị Approve". Đây là **sai lệch với review thật** của ChatGPT round 5, vốn là **Revision Requested** với đúng **2 Blocker · 4 Major · 1 Minor · 0 Suggestion mới**. Round 5 xác nhận 6 concern outstanding từ v2.4 vẫn chưa đóng; v2.5 chỉ xử lý phần precondition của promotion (đúng như entry gốc mô tả), KHÔNG xử lý 6 concern còn lại. Không tự kết luận "đã sạch" khi chưa đối chiếu đủ nguyên văn bảng severity.

### Fixed — Blocker
- **`decision-dependency contract` là peer authority của Input Contract (§9.5):** chữ "hoặc" giữa Input Contract và decision-dependency contract tạo hai authority ngang hàng — `decision_context_cursor` chỉ pin Input Contract, nên dependency contract nằm ngoài trở thành **hidden input** không có root path bắt buộc khi replay, bất kể có immutable hay không. **Sửa:** decision-dependency contract giờ là **subordinate immutable artifact** phải được Input Contract **exact-pin**; không tự mở rộng input scope; đổi reference bắt buộc bump Input Contract version; xóa hoàn toàn cấu trúc OR. Nếu cần nhiều peer input authority thật sự, phải qua ADR sửa canonical cursor — Chapter 9 không tự tạo bằng prose.
- **Promotion `decision-relevant` chưa có authoritative activation boundary:** v2.5 mới có precondition verify (4 điều kiện visibility) nhưng không định nghĩa promotion có hiệu lực từ đâu — có thể rơi vào half-promoted/mixed-version state theo cả hai chiều (Plugin Contract đã promote nhưng Input Contract/permission/runtime chưa theo kịp, hoặc ngược lại). **Sửa:** khóa invariant **atomic activation boundary** — một **validated compatibility set** (Plugin Contract version · Input Contract version · published contract refs · permission grant version · capability/compatibility result · runtime deployment version) phải đồng bộ tại boundary. Trước boundary: cấm dùng cho authoritative Decision. Sau boundary: mọi Decision phải pin đúng promoted snapshot. Partial/mixed-version activation → integrity violation, fail-safe I-6. Cơ chế fencing cụ thể defer Phase 1; atomic semantic khóa ngay ở Chapter 9.

### Fixed — Major
- **Strategy Instance bị loại tuyệt đối khỏi Module Taxonomy (§9.1):** chỉ đúng với hosted instance. Độc lập operated instance (process/pod riêng, deploy/restart/scale riêng, published contract riêng) thỏa định nghĩa module của Ch7 §7.0. **Sửa:** tách bảng thành Strategy Instance (hosted) = KHÔNG thuộc taxonomy · Strategy Instance (independently operated) = CÓ, có `module-registry` entry cho runtime component, `strategy_instance_id ≠ module_id`. Nguyên tắc: classification phụ thuộc operational boundary thật, không phụ thuộc domain identity class.
- **Plugin Definition / Package vẫn gộp logical + artifact identity (§9.1, §9.3):** không rõ registry đăng ký logical plugin hay binary; Decision evidence không rõ pin semantic version hay content hash; promote/rollback không rõ tác động layer nào. **Sửa:** tách 4 tầng — Plugin Definition (logical identity) ≠ Plugin Version (immutable release) ≠ Package/Build Artifact (immutable bytes + content hash) ≠ Plugin Runtime (deployment/replica). `module-registry.yaml` chỉ đăng ký Plugin Definition; Decision evidence pin Plugin Version.
- **Strategy Definition bị khóa vào một Strategy Plugin (§9.3):** yếu hơn Chapter 3 Locked, vốn cho phép authoritative/shadow/experimental/migration implementation song song. **Sửa:** một Strategy Definition có thể có nhiều implementation/Plugin Version; đúng một implementation authoritative trong mỗi execution/parity scope; shadow/experimental/migration không sinh authoritative Decision trước parity validation + promotion. "Canonical" = authority status trong scope, không phải cardinality.
- **Version independence bị hiểu thành zero downstream impact (§9.7):** "cập nhật một plugin không ảnh hưởng plugin khác" sai — plugin update có thể ảnh hưởng consumer qua contract/semantic/capability/permission/freshness/dependency/resource contention. **Sửa:** "independent versioning ≠ zero downstream impact"; impact đánh giá bằng compatibility/capability/dependency rules của Chapter 10.

### Fixed — Minor
- **§9.4 câu mở "chịu toàn bộ ràng buộc" vẫn đọc được thành bảng exhaustive** dù đã có câu "CẦN chưa ĐỦ" ở đoạn sau. Đổi câu mở thành: bảng tóm tắt các ràng buộc trực tiếp quan trọng nhất, không thay thế toàn bộ Chapter 8 và ADR-010.

### Checklist
- Ch9 v2.6 · §9.1→§9.10 liên tục · **0 tham chiếu §9.x gãy** · 0 wording cũ còn sót (peer-authority OR · single-implementation · zero-impact) · CHANGELOG v2.5 đã đính chính severity sai.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 6 xác nhận, và chờ Product Owner Approve/Lock.

## [Unreleased] — Chapter 9 v2.5 (ChatGPT review round 5: **0 Blocker · 0 Major · 1 Minor** — ⚠️ **entry này ghi sai, xem đính chính ở entry v2.6 phía trên**)

### Fixed — Minor
- **"Verify lại toàn bộ §9.5" mơ hồ về điều kiện cụ thể của promote:** liệt kê rõ 4 điều kiện bắt buộc trước khi promote một plugin thành decision-relevant có hiệu lực — cursor/snapshot-bounded · không đọc ambient state · pin projection version/schema/config · evidence đủ cho Replay (I-5).

### Note
- ChatGPT khuyến nghị **Approve** Chapter 9 sau vòng này. *(⚠️ Sai lệch với review thật — xem đính chính ở entry v2.6.)*

## [Unreleased] — Chapter 9 v2.4 (ChatGPT review round 4: **1 Blocker · 2 Major**)

### Fixed — Blocker: lỗ hổng reclassification ngầm do chính câu Claude thêm ở v2.3
- v2.3 viết *"phân loại theo **đường dữ liệu thực tế**, không theo ý định ban đầu"* — nghe hợp lý nhưng biến decision-relevance thành thuộc tính **suy ra lúc runtime**. Hệ quả: cùng một plugin, cùng một version, cùng một output sẽ **đổi ràng buộc theo hành vi của consumer** — evidence requirement thay đổi hồi tố, không audit được, và một consumer có thể **lặng lẽ kéo plugin chưa đủ điều kiện vào Decision Pipeline** rồi tuyên bố "giờ nó decision-relevant".
- **Sửa:** decision-relevance là **thuộc tính CONTRACT được khai báo** (`Decision participation`, §9.6), không suy runtime. **CẤM** dùng output của plugin chưa khai báo decision-relevant làm Decision input → integrity violation, fail-safe I-6, **không tự động nâng cấp**. Muốn tái sử dụng phải **promote qua contract change** (versioned, verify lại §9.5, ADR Required nếu đổi pipeline topology). **CẤM silent reclassification**. Làm rõ cách hiểu đúng: "đường dữ liệu thực tế" dùng để **phát hiện vi phạm**, KHÔNG phải để **tự động hợp thức hóa**.
- Thêm dòng tương ứng vào Forbidden patterns.

### Fixed — Major
- **Một dòng trong Forbidden patterns không có runtime enforcement:** "Bắt mở ADR cho mọi activate/pause instance" là lỗi **quy trình/governance**, không phải hành vi runtime — không cơ chế kỹ thuật nào phát hiện được. Để chung bảng làm loãng chuẩn "mọi dòng phải thi hành được" mà chính v2.3 vừa thiết lập. Tách thành bảng riêng **"Anti-pattern thuộc phạm vi GOVERNANCE"** với cột phát hiện = governance/process review.
- **"Instance identity không được tái sử dụng" chưa thi hành được:** thiếu (a) **uniqueness scope** — Ch6 §6.1 (Locked) cấm mặc định global, phải khai báo tường minh (global/per-Account/per-Strategy-Definition); nếu hẹp hơn global thì reference qua boundary phải qualified; (b) **retention/resolvability horizon** — Ch8 §8.1.1 yêu cầu persistently resolvable trong horizon platform cam kết, hết horizon phải có explicit retention/archive policy. Không có hai thứ này thì "không tái dùng" không kiểm chứng được sau vài năm.

### Checklist (7 mục)
- Ch9 v2.4 · decision-relevance là contract property · cấm silent reclassification · bảng governance tách riêng · instance identity có scope + horizon · **0 tham chiếu §9.x gãy** · bảng runtime không còn dòng governance.

## [Unreleased] — Chapter 9 v2.3 (ChatGPT review round 3: **1 Blocker · 2 Major · 1 Minor**)

### Fixed — Blocker: §9.4 mất ràng buộc visibility sau khi tách §9.5
- Vòng trước Claude **nâng decision-time visibility thành §9.5 độc lập** nhưng **không để lại liên kết** trong §9.4. Kết quả: bảng §9.4 liệt kê 6 ràng buộc và tự xưng là "toàn bộ ràng buộc đã Locked ở Chapter 8 + ADR-010", trong khi thiếu đúng ràng buộc quyết định — implementation đọc riêng §9.4 sẽ kết luận Decision Advisor chỉ cần schema đúng. Sửa: thêm dòng **Decision-time visibility (§9.5, bắt buộc)** vào bảng + câu chốt **"bảng trên là điều kiện CẦN, chưa ĐỦ"** + đưa "không có ngoại lệ cho AI module" về đúng chỗ.
- *Lớp lỗi:* tách một mục ra khỏi mục khác mà không kiểm mục gốc còn tự đủ không — cùng họ với các lỗi propagation đã ghi nhận.

### Fixed — Major
- **Instance lifecycle transition chưa bảo vệ Decision evidence:** §9.3 nói state transition là authoritative event, §9.8 nói lifecycle facts thuộc event log — nhưng không nói pause/stop/retire **không được** hủy/vô hiệu hóa evidence của Decision đã tính. Thêm ràng buộc 5: Decision đã tính vẫn tái dựng đầy đủ với đúng instance + plugin version + config (I-1) · **instance identity không được tái sử dụng** sau retire ([Ch6 §6.1](constitution/06-identity-model.md)) · nếu retire/stop chặn một Decision in-flight thì áp **cùng nguyên tắc ADR-010 §2.6**: ghi immutable preservation/rejection fact đủ evidence, **không xóa/ghi đè** Decision gốc, **không** cấp execution eligibility.
- **Forbidden patterns thiếu enforcement/verification ownership:** bảng liệt kê pattern + invariant bị vi phạm nhưng không nói **ai phát hiện, ai chặn** → là checklist review, không phải rule thi hành được (đúng bài học I-7: bypass không nhất thiết xuất hiện dưới dạng import code). Thêm cột **"Phát hiện / chặn bởi"** cho cả 9 dòng, **không tạo authority mới** — mỗi dòng trỏ về cơ chế đã tồn tại (I-7 Verification · Risk Gateway · Grant layer `granted ⊆ declared` · I-11 access-control audit · self-contained replay test · registry review · event log). Ghi rõ: pattern không có cột này chỉ là *khuyến nghị*.

### Fixed — Minor
- **§9.5 heading và body lệch phạm vi:** heading nói "MỌI plugin sinh authoritative output", body nói "decision-relevant path" → không rõ reporting/notification plugin có phải cursor-bound không. Thống nhất: áp cho plugin **trong decision-relevant path**; ghi rõ **ngoài phạm vi** (reporting/notification thuần túy, observability projection) — **nhưng** nếu output về sau được dùng làm input cho Decision thì plugin đó **trở thành** decision-relevant và phải tuân đầy đủ; phân loại theo **đường dữ liệu thực tế**, không theo ý định ban đầu.

### Checklist (7 mục)
- Ch9 v2.3 · §9.4 có dòng visibility · §9.4 nói rõ "CẦN chưa ĐỦ" · lifecycle không hủy evidence · forbidden patterns có cột enforcement · §9.5 có mục "ngoài phạm vi" · **0 tham chiếu §9.x gãy**.

## [Unreleased] — Chapter 9 v2.2 (ChatGPT review round 2: **1 Blocker · 2 Major · 1 Minor · 1 Suggestion**)

### Fixed — Blocker: mâu thuẫn nội tại về phạm vi Module Taxonomy
- §9.1 khẳng định plugin là runtime application component → có taxonomy type + `module-registry` entry; §9.3 lại khẳng định Strategy Instance KHÔNG phải module. Nhưng theo [Ch7 §7.0](constitution/07-module-taxonomy.md) (Locked), Strategy Instance **cũng** có runtime responsibility và published boundary → hai câu không thể cùng đúng nếu đọc §7.0 theo nghĩa rộng.
- **Sửa bằng cách làm rõ, KHÔNG định nghĩa lại Ch7:** Ch7 §7.0 viết *"**deployable** service, process, hoặc in-process component **được vận hành độc lập**"*. Strategy Instance chạy bên trong Strategy Engine **không được vận hành độc lập** → nằm ngoài phạm vi taxonomy. Thêm bảng: **Plugin Definition/Package** (deployable/executable unit) = CÓ taxonomy type + registry entry · **Strategy Instance** (runtime configuration bound vào deployable unit) = KHÔNG. Ghi rõ điều kiện escalate: *nếu reviewer đánh giá đây là redefinition chứ không phải clarification thì bắt buộc mở ADR sửa Ch7 — Chapter 9 không được tự làm.*

### Fixed — Major
- **Strategy Instance nằm ngoài registry nhưng chưa có identity/state authority:** không có nó thì I-1 và ADR-010 không tái dựng được Decision. Thêm 4 ràng buộc: instance identity **ổn định qua restart/redeploy** · đổi plugin version/config phải tạo **binding hoặc instance version mới** (cấm mutate ngầm identity đang chạy) · Decision evidence phải resolve chính xác `strategy_instance` + `configuration version` + `plugin implementation version` (ba thứ ADR-010 đã tách riêng) · state transition (created/activated/paused/stopped/retired) là **authoritative event**, không suy từ registry hay config file.
- **Permission boundary chỉ là declaration, chưa có enforcement/verification authority:** khai báo mà không nói ai cấp, ai chặn, ai chứng minh thì đó là mô tả, không phải ranh giới an toàn. Thêm phân tầng 4 lớp: **Declaration** (Plugin Contract) · **Grant** (deployment/authorization config, versioned — plugin **không tự cấp quyền cho mình**) · **Enforcement runtime** (Risk Gateway với execution intent I-4 · Exchange Adapter/Signing Service với credential I-11 · contract/API authorization với query & command) · **Verification** (đúng bộ kiểm I-7 đã khóa). Ràng buộc: **`granted ⊆ declared`**; vượt quyền = integrity violation → fail-safe I-6. Khóa tuyệt đối: **plugin KHÔNG bao giờ được cấp quyền dùng exchange credential trực tiếp** (I-11, không ngoại lệ).

### Fixed — Minor
- **Decision-time visibility đặt sai chỗ:** nằm trong §9.4 "Decision Advisor" nhưng phải áp cho **mọi plugin sinh authoritative output** trong decision-relevant path (Strategy Plugin · Feature/Signal · Risk-context · plugin sinh input cho Decision) — vì I-3 chống look-ahead ở **mọi** compute path, không riêng bước cuối. Nâng thành **§9.5 độc lập**.

### Added — Suggestion
- **§9.9 Forbidden patterns** — bảng 9 anti-pattern đối chiếu trực tiếp với invariant bị vi phạm (gọi Exchange API → I-4 · đọc storage module khác → I-7 · đọc "current state" không cursor-bound → I-2/I-3/I-5 · cấp credential cho plugin → I-11 · registry entry cho mỗi instance → §9.1/§9.3 · mutate ngầm version đang chạy → §9.3 · suy runtime state từ registry → I-12 · ADR cho mọi activate/pause → §9.10 · nâng strategy philosophy thành invariant → Ch2).

### Checklist
- Ch9 v2.2 · §9.1→§9.10 liên tục · fence 2 (chẵn) · **0 tham chiếu §9.x gãy** · phạm vi taxonomy làm rõ kèm điều kiện escalate ADR · runtime identity 4 ràng buộc · permission 4 tầng + `granted ⊆ declared` · decision-time visibility là mục độc lập · forbidden patterns 9 dòng.

## [Unreleased] — Chapter 9 v2.1 (ChatGPT review round 1: **2 Blocker · 2 Major · 1 Suggestion**)

### Fixed — Blocker 1: "Strategy = Plugin" đồng nhất 3 identity khác nhau
- ADR-010 (Approved) đã khóa evidence của Decision gồm **strategy/model version** *và* **strategy instance** *và* **configuration version** như ba thứ riêng — nhưng Chapter 9 gộp tất cả thành "strategy là plugin". Hệ quả: `BTC-15m-conservative`, `BTC-1h-aggressive`, `ETH-15m-paper` cùng dùng `ride-strategy-negation v2.1` nhưng khác tham số sẽ thành **3 module riêng, 3 registry entry, 3 plugin version** — architecture registry phình theo runtime instance, mất khả năng trả lời *"hai instance có dùng cùng implementation không?"*. Tách §9.3: **Plugin Definition/Package** (architecture, `module-registry`) ≠ **Strategy Definition** (domain semantics, Domain Contract) ≠ **Strategy Instance** (runtime, có identity/params/Input Contract/config/lifecycle riêng). Khóa: một plugin phục vụ **nhiều** instance; **Strategy Instance KHÔNG tạo `module-registry` entry mới**.

### Fixed — Blocker 2: query/read contract chưa bị Decision-time visibility ràng buộc
- Công thức mấu chốt: **`Published contract compliance ≠ Decision-time visibility compliance`**. Plugin tuân I-7 hoàn hảo vẫn phá I-2/I-3/I-5 nếu query trả về "current state": cursor pin frontier 1000 → gọi `getCurrentExposure()` → projection đã ở 1010 → Decision attach cursor 1000 nhưng **đã đọc state từ tương lai**. Schema hợp lệ, invariant vỡ. Thêm §9.4: Decision Advisor **cấm đọc ambient/current mutable state**; mọi dependency phải (1) khai báo trong Input Contract/immutable decision-dependency contract · (2) resolve tại hoặc trước `decision_context_cursor` · (3) **pin projection version/schema/config** khi đọc derived state · (4) có evidence đủ để Replay tái tạo đúng snapshot (I-5). Query không chứng minh được knowledge boundary → **cấm dùng tạo authoritative Decision**; projection cho Decision phải trả về source frontier + version + freshness, **cấm lấy "latest" ngầm**.

### Fixed — Major
- **Lifecycle authority chưa tách khỏi architecture registry:** §9.6 cũ gộp "đăng ký, kích hoạt, gỡ bỏ" thành một, ngầm biến `module-registry.yaml` thành nguồn runtime truth — trái I-12 (runtime facts → event log). Tách 4 tầng authority: module identity/taxonomy → `module-registry.yaml` · installable version + content identity → artifact reference (thỏa Referenced Authoritative Artifact rules §8.1.1 nếu bị event/cursor tham chiếu) · **runtime lifecycle facts → authoritative event log** · Strategy Instance state → Strategy Domain Contract.
- **ADR gate quá rộng, chặn vận hành:** "thay đổi ảnh hưởng Decision Pipeline → ADR Required" + "Strategy Plugin mặc định tham gia Decision Pipeline" ⟹ **bật/tắt một strategy instance phải mở ADR** — không vận hành được. §9.8 tách: ADR Required cho architecture/contract change (plugin type/capability mới · published contract · dependency graph · pipeline topology · authority model · lifecycle semantics); **KHÔNG** cho operational action (tạo instance từ plugin đã approved · activate/pause/stop · promote/rollback theo policy đã approved · kill-switch disable · uninstall version không còn reference). Ghi rõ **không đóng ngầm OQ-002** (Strategy Lifecycle Gate vẫn Open, thuộc Quality Gates).

### Added — Suggestion
- **§9.5 Plugin Contract** — 6 nhóm khai báo tối thiểu (Identity · Contract surface · Permission boundary · Decision participation · Lifecycle class · Required capabilities). Không có chúng thì các kiểm tra I-7 Verification đã khóa (network ACL · authorization scope · event schema compatibility · command authorization · capability declaration) **không thực hiện được**. Chapter 9 sở hữu *sự tồn tại + ý nghĩa*; Chapter 10 sở hữu *thuật toán compatibility*.

### Checklist (8 mục)
- Ch9 v2.1 · fence 2 (chẵn) · §9.1→§9.8 liên tục · ba identity tách rõ · query cursor-bounded · runtime facts không lấy từ module-registry · ADR không áp runtime op · OQ-002 không bị đóng ngầm.

## [Unreleased] — Chapter 9 (Plugin Model) v2.0 — Claude tự review

### Fixed — mâu thuẫn trực tiếp với chapter đã Locked
- **"AI Module mặc định là consumer thuần túy của Event Bus" lặp lại wording I-7 ĐÃ BỊ SỬA:** I-7 được siết ở Chapter 7 review từ "mọi module mới mặc định là consumer của Event Bus" → "module mở rộng không được mặc định trở thành thành phần nội bộ của Decision Pipeline; plugin chỉ tương tác qua published contracts". Lý do siết: **không phải plugin nào cũng cần là event consumer** — một plugin chỉ cần query/read contract là hợp lệ. Chapter 9 vẫn mang model cũ. Sửa: phát biểu theo **published contract**, không theo consumer role.
- **Dùng "Event Bus" như authority, trái Chapter 8 §8.1 (Locked):** Chapter 8 khóa transport/broker KHÔNG phải source of truth (authority ở durable append-only event log). Mô tả plugin "consume Event Bus" là mô tả theo **transport** thay vì theo **contract**. Đã sửa.

### Fixed — khoảng trống thẩm quyền
- **Quan hệ Plugin ↔ Module Taxonomy chưa xác định:** Chapter 7 §7.0 định nghĩa taxonomy áp cho "runtime application component" — plugin đúng là loại đó, nhưng Chapter 9 không nói plugin có primary type hay đăng ký ở đâu. Chốt §9.1: plugin **thuộc phạm vi taxonomy**, có primary type (Strategy Plugin điển hình = Compute Engine), đăng ký trong **`module-registry.yaml`** cùng mọi module khác. **KHÔNG tạo plugin registry riêng** — sẽ có 2 nguồn cho cùng sự thật "component nào tồn tại và thuộc loại gì" (I-12).
- **`strategy.json` hardcode artifact vào Constitution:** lặp lại đúng lớp lỗi đã sửa ở I-2 (field list), I-13 (state machine), ADR-008 (ngôn ngữ). Sửa: Constitution giữ nguyên tắc (metadata gồm philosophy/tham số/version), **format và tên file thuộc Domain Contract/module-registry**; chọn format cụ thể là ADR Required nếu ảnh hưởng nhiều module.
- **Versioning chồng lấn Chapter 10:** Chapter 9 phát biểu quy tắc versioning trong khi Chapter 10 sở hữu SemVer/`schemaVersion`/capability/Capability Matrix. §9.5 chỉ tuyên bố *tính độc lập*, trỏ chi tiết sang Chapter 10. Kèm cảnh báo **tránh vòng dependency**: Chapter 10 khai `depends_on: [09-plugin-model]` nên Chapter 9 không được tham chiếu ngược vào chi tiết Ch10.

### Added
- **§9.4 Decision Advisor** — nối plugin với toàn bộ ràng buộc Chapter 8 + ADR-010 vừa Locked: `event_class: decision` · `decision_time` (effective) + `effective_time` prohibited · `decision_context_cursor` đủ 5 field · relational invariants · Append-and-Revalidate khi có registry transition · I-4 (mọi intent qua Risk Gateway). Khóa rõ: **không có ngoại lệ cho AI module** — dùng ML không đổi bất kỳ ràng buộc nào; I-1 vẫn đòi model/config version trong evidence.
- **§9.6 Plugin lifecycle** — thay đổi version/trạng thái plugin đang tham gia Decision Pipeline **không được làm mất evidence của Decision đã tính** (I-1). Protocol cụ thể (drain, activation boundary, in-flight handling) → Phase 1 design spec.
- Frontmatter: thêm dependency `08-event-model` (Chapter 9 giờ tham chiếu trực tiếp Decision event requirements).

## [Unreleased] — Sửa lỗi MANIFEST phát hiện khi re-orientation

### Fixed
- **OQ-005/OQ-006: chữ "RESOLVED" nằm SAI CỘT.** Lần cập nhật milestone trước dùng regex thay nội dung, khiến "RESOLVED" rơi vào cột **Chủ đề** trong khi cột **Trạng thái** vẫn là . Đọc bảng sẽ thấy hai OQ này vẫn Open dù ADR đã Approved. Phát hiện khi Product Owner yêu cầu re-orientation từ MANIFEST — đúng giá trị của việc đọc lại từ nguồn thay vì tin trí nhớ. Đã tách đúng cột.
- **Decision Log còn text stale:** ADR-009/ADR-010 status đã  nhưng phần tóm tắt vẫn ghi "ADR chờ review + accept". Đã sửa thành "Approved 2026-07-18, resolves OQ-00x".
- *Lớp lỗi lặp lại:* regex/replace hàng loạt trên bảng Markdown mà không verify theo cột — cùng họ với các lỗi verify đã ghi nhận trước đó.

## [Milestone] — 2026-07-18 — 🔒 Chapter 8 (Event Model) LOCKED · ADR-009 & ADR-010 APPROVED

Product Owner thực hiện **atomic transition** theo [Chapter 11 §metadata contract](constitution/11-adr-process.md), đúng thứ tự dependency gate:

**1. ADR-009 — Ordering Mechanism → `Approved`**
`status: Draft → Approved` · `addresses: [OQ-005] → []` · `resolves: [] → [OQ-005]` · `approved_by/at` set · **OQ-005 → `Resolved`**.

**2. ADR-010 — Decision Effective-Time Model + Append-and-Revalidate → `Approved`** (sau ADR-009, thỏa dependency gate §7)
`status: Draft → Approved` · `addresses: [OQ-006] → []` · `resolves: [] → [OQ-006]` · `approved_by/at` set · **OQ-006 → `Resolved`**.
*Xác minh gate:* hash ADR-009 không đổi từ vòng 31 (`03fe53cf`), nên ADR-010 ở vòng 32-33 đã được review đối chiếu **đúng snapshot đang được accept** — không cần re-review sau accept.

**3. Chapter 8 → `Locked`** — đủ cả 6 điều kiện lock gate:
1. ✅ ADR-009 Approved · 2. ✅ ADR-010 Approved theo dependency gate · 3. ✅ OQ-005/006 → Resolved · 4. ✅ §8.4.1 Append-and-Revalidate (PO quyết) · 5. ✅ Scoped Policy + canonical Audit Stream (PO quyết) · 6. ✅ Consolidation review hoàn tất.

### Quy mô công việc
Chapter 8 là chapter nặng nhất dự án: **33 vòng review** (so với 3-6 vòng của Chapter 0-7). Các model đã khóa: event log authority (không phải transport) · event envelope + cardinality + relational invariants · `P_global`/`P_run` · per-stream contiguous sequence · explicit causation (semantic thuộc Ch6) · Input Contract cross-mode (exact registry pin, `causal_closure_policy`, `frontier_policy`) · Stream Registry + Genesis Registry + protected Lifecycle/Audit streams · canonical Replay Cursor + `lifecycle_frontier` · Decision Effective-Time Model + `decision_context_cursor` · Append-and-Revalidate + Scoped Preservation Policy · revalidation evidence chain + 3 execution boundary.

### Deferred sang Phase 1 (ADR-009 per-capability gate)
watermark/committed frontier/barrier · multi-stream completeness · late-arrival protocol · buffer sizing/overflow · coordinator/checkpoint · topological merge + cycle-detection implementation · writer handoff/retirement/registry activation protocol · storage/archive/retention/recovery.

**Đã Locked tới nay:** Chapter 0, 1, 2, 3, 4, 5, 6, 7, **8** + ADR-005 → ADR-010.

**Next Milestone:** Chapter 9 — Plugin Model.

## [Unreleased] — Vòng 33: Ch8 v4.8 · ADR-010 (**0 Blocker · 1 Major hẹp**)

### Fixed — Major: preservation fact ép `risk_policy_version` trước khi Risk từng xảy ra
- Vòng trước Claude thêm `risk policy version` vào evidence **bắt buộc** của preservation fact. Nhưng nhánh preservation có thể **kết thúc trước bất kỳ Risk evaluation nào**: Decision tính xong → target stream retire/ineligible → ghi preservation fact → **không có execution eligibility** → không nhất thiết qua Risk Gateway. Ép field này tạo hai kết quả đều sai: (1) gán một risk policy **chưa từng được evaluate** → **evidence giả**; (2) không có policy nên **không ghi được** preservation fact → path thất bại đúng lúc cần bảo toàn evidence.
- **Sửa — tách 2 nhóm evidence với cardinality riêng:**

| Nhóm | Cardinality | Nội dung |
|---|---|---|
| Decision computation | **Required** | semantic Decision output · original cursor · strategy/model version + instance · configuration version · code/build version · mọi policy/reference **thực sự được Decision computation tiêu thụ** |
| Risk evaluation (`risk_policy_ref`) | **Conditional** | chỉ khi Risk evaluation **đã thực sự xảy ra** hoặc policy **thực sự là input** của Decision computation |

- Khóa thêm: **CẤM gán risk policy chưa từng evaluate chỉ để thỏa schema**; Risk Action về sau **tự sở hữu** policy/version nó áp dụng (I-4 — Risk Gateway nằm sau Decision, trước Execution). Đúng tinh thần I-1: trace phải chứa risk policy **đã áp dụng**, không đòi mọi event mang một policy chưa được áp dụng.
- Propagate đồng bộ Chapter 8 §8.4.1 + ADR-010 §2.6.

### Trạng thái sau vòng này
- **ADR-009: `technically ready for Product Owner decision`** (ChatGPT xác nhận, vẫn `Draft` — quyền quyết định thuộc Product Owner).
- ADR-010: Major hẹp duy nhất đã xử lý.
- ChatGPT ghi rõ vòng kế chỉ cần kiểm propagation của evidence ownership + regression liên quan; **không có lý do mở lại** ordering, cursor, lifecycle hay causation model.

### Checklist (5 mục)
- Ch8 v4.8 · fence 68 (chẵn) · `risk_policy_ref` = Conditional trong bảng Ch8 · "CẤM gán" hiện diện ở cả Ch8 và ADR-010 · ADR-010 tách rõ 2 nhóm evidence.

## [Unreleased] — Vòng 32: Ch8 v4.7 · ADR-010 (**1 Blocker · 2 Major · 1 Suggestion**)

### Fixed — Blocker: `dependency_authority` có hai schema shape trong cùng Chapter
- §8.2.3 vẫn hiển thị **object** `dependency_authority: {event_contract_ref: {...}}` trong khi prose kế tiếp và §8.3.4 + ADR-009 đều dùng **scalar enum** `per_effect_event_contract` → validator có thể hợp lệ hóa hai cấu trúc hoàn toàn khác nhau. Đúng lớp lỗi "một concept, nhiều schema shape" đã gặp nhiều lần. Xóa object shape, chuẩn hóa scalar + thêm **cardinality tường minh**: `mode: full` → `dependency_authority` **PROHIBITED**; `mode: declared-state-dependencies` → **REQUIRED**, giá trị duy nhất hiện hỗ trợ `per_effect_event_contract`.

### Fixed — Major
- **Merge target vẫn có thể bị hiểu là `P_global`:** câu "topological order trên **hợp của hai partial order này**" chính là cách vừa định nghĩa `P_global = P_stream ∪ P_causation` → implementation có thể quay lại sort toàn `P_global` gồm cả external vertex, trái model mới. Sửa dứt khoát: **merge order trên `P_run`**; `P_global` chỉ là authority để kiểm causal integrity, phát hiện cycle, và suy quan hệ bắc cầu phải bảo toàn trong `P_run`. Đồng thời **hợp nhất alias**: `P_authoritative` (tên cũ) ≡ `P_global` — giữ hai tên cho cùng concept là nguồn tái phát mơ hồ "merge target nào mới là authority".
- **Execution-boundary validity ở Chapter 8 YẾU HƠN ADR-010:** Chapter 8 chỉ yêu cầu Risk Approval còn valid tại thời điểm **emit intent**; ADR-010 yêu cầu tới **trước external side effect**. Kịch bản hỏng: Risk check pass ở frontier 900 → emit intent → registry transition ở 901 → Execution Engine gửi lệnh ra sàn ở 902 dưới authorization **đã stale**. Propagate rule mạnh vào Chapter 8: eligibility **KHÔNG được đóng băng tại intent creation**; authorization chain phải valid tại **cả 3 boundary** (Risk Approval · Execution Intent · **ngay trước external side effect**); transition ở bất kỳ khoảng nào → blocked lại. Cơ chế (atomic check/fencing token/transaction) → Phase 1; **boundary semantic** khóa tại Chapter 8.

### Added — Suggestion: preservation fact phải đủ evidence tái dựng Decision đã tính
- Scoped Preservation Policy trước đó chỉ bắt buộc cursor + lý do + boundary — nhưng mục tiêu là chứng minh *"một Decision đã được tính"*, trong khi **I-1** yêu cầu tái dựng được cả model/strategy version, configuration, risk policy version. Thêm conformance requirement cho dedicated Event Contract: preservation fact phải **chứa hoặc resolve được** immutable evidence đủ tái dựng semantic Decision output. Nếu không, preservation path thành **"audit stub" rỗng nội dung**. Propagate cả Chapter 8 và ADR-010.

### Note — trạng thái hai ADR
- Lần đầu ChatGPT đánh giá **cả ADR-009 và ADR-010 là "technically near-ready"** — không còn Blocker độc lập trong bản thân hai ADR; chỉ chờ Chapter 8 dùng **cùng schema + cùng merge target + cùng execution-boundary invariant**. Sau vòng này cả ba đã đồng bộ.
- ChatGPT xác nhận `Option A/Option B` còn lại (phần contiguous sequence) có subject ngay trong câu, không tạo cross-reference mơ hồ → không đạt stop rule, không tính finding.

### Checklist (7 mục)
- Ch8 v4.7 · fence 68 (chẵn) · **0 object shape `dependency_authority`** · merge target = `P_run` · `P_authoritative` chỉ còn dạng alias khai báo · 3 execution boundary hiện diện · preservation evidence I-1 ở cả Ch8 và ADR-010.

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
