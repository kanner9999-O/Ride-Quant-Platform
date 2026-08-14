---
id: phase-2-batch-06-traceability
title: "Phase 2 Prototype — Batch 06 — Traceability Artifact"
version: "1.0"
status: Candidate
owner: Product Owner
created_at: "2026-08-14"
---

# Phase 2 Prototype — Batch 06 — Traceability Artifact

**Vai trò của tài liệu này:** đây LÀ I-12 (Single Source of Truth) conformance evidence cho Batch
06, per `docs/phase-dod/phase-2-dod.md` §2's applicable Trigger A / I-12 requirement — mọi phần tử
prototype trong batch này PHẢI trace được TRỰC TIẾP về đúng một hoặc nhiều `SCR-XXX`/`VIEW-XXX`/
`NAV-XXX`/`STATE-XXX` đã `Consolidated Stable` trong [`docs/product/ux-blueprint.md`](../../../docs/product/ux-blueprint.md),
VÀ về đúng `UC-XXX` đã `Consolidated Stable` trong [`docs/product/use-case-workflow.md`](../../../docs/product/use-case-workflow.md),
VÀ về đúng `PR-XXX`/Domain Contract field đã tồn tại. Prototype LÀ derived representation — KHÔNG
một UC/PR/domain concept nào originate tại đây. Áp dụng ĐÚNG taxonomy A/B/C đã establish tại
`../batch-01/traceability.md` §0, kế thừa nguyên vẹn qua Batch 02-05.

## 0. UC accounting taxonomy (kế thừa nguyên vẹn từ Batch 01-05, KHÔNG redefine)

```text
A. SUBSTANTIVELY COVERED — Batch tự author ĐỦ representation (screen/view + required context +
   primary/blocked states + exit behavior đúng ux-blueprint.md/use-case-workflow.md spec) để tính
   vào 21-UC completion numerator (phase-2-dod.md §3).
B. PARTIAL / REFERENCED — UC xuất hiện qua global shell context, nav-button existence, handoff
   affordance, hay deferred-placeholder destination — KHÔNG đủ để tính vào numerator.
C. DEFERRED / NOT YET REPRESENTED — KHÔNG một element nào trong batch tham chiếu UC đó.
```

## 1. Batch-06-authored substantive contribution (distinct từ cumulative ledger, §2 dưới)

```text
Batch-06-authored substantive UC (NEW tại batch này, 3, CANDIDATE — CHƯA independently verified):
  UC-019 (SCR-010 — Strategy Definition Version Creation)
  UC-020 (SCR-011 — Strategy Version Comparison)
  UC-021 (VIEW-005 — Old-Version Evidence Access)

VIEW-006 substantively represents the UC-019→UC-002 handoff (registration, distinct from
  selection/pinning) — its own traceability rows below cite BOTH UC-019 (upstream) and UC-002
  (downstream, ALREADY independently verified since Batch 01). VIEW-006 does NOT create new
  Batch-06 substantive UC progress for UC-002 — UC-002 is NOT double-counted (it was already A
  before this batch and remains A for the SAME reason, Batch 01's own VIEW-001, untouched).

UC-019 was previously hạng B (referenced only via NAV-006's nav-button-existence citation, Batch
  01-05) — nay promote lên A vì SCR-010 tự author đủ representation (existing Definition +
  old-version evidence shown, real editable creation control, distinct new version identity
  produced, old version provably unmutated, exact handoff to VIEW-006) đúng `ux-blueprint.md`
  §7.6 SCR-010 spec VÀ `use-case-workflow.md` UC-019 Main flow.
UC-020 previously hạng B — nay promote lên A vì SCR-011 tự author đủ representation
  (required-context gate, real Instance+mode selection per side, Backtest-vs-Backtest/
  PAPER-vs-PAPER/cross-mode all materially reachable, missing-outcome-per-Instance behavior,
  old-version route to VIEW-005, no unified outcome/score) đúng `ux-blueprint.md` §7.6 SCR-011
  spec VÀ `use-case-workflow.md` UC-020 Main flow.
UC-021 previously hạng B — nay promote lên A vì VIEW-005 tự author đủ representation
  (old-version identity always visible, independent per-family resolution, STATE-025/STATE-026
  both materially reachable, missing-family disclosure with reason, no fabrication) đúng
  `ux-blueprint.md` §7.6 VIEW-005 spec VÀ `use-case-workflow.md` UC-021 Main flow +
  Alternate/failure.

Batch-01/02/03/04/05-verified substantive UC (KHÔNG re-authored, KHÔNG double-counted, VẪN A):
  UC-001..UC-018.
```

| UC | Classification | Evidence / reason |
|---|---|---|
| UC-019 | **A — Substantive** (Batch 06, promoted từ B, CANDIDATE) | SCR-010 fully authored: existing Strategy Definition (`sd-fam-001`) + old version (`sdv-v1.0`, full seven-field content) shown as required context; real, non-inert creation control (editable `thesis`/`supported_scope`, other fields fixed-illustrative-but-real) that materially produces a brand-new `strategy_definition_version_id` (`sdv-v1.1`, `sdv-v1.2`, ... via `buildNewVersion()`, append-only counter — never overwrites); old version's own panel re-reads the SAME unmutated `VERSION_FIXTURES["sdv-v1.0"]` object after creation, proving no in-place mutation; exact created version handed to VIEW-006 via `latestCreatedVersion()` (no unrelated fixture) — matches `ux-blueprint.md` §7.6 SCR-010 spec + `use-case-workflow.md` UC-019 Main flow steps 1-3. |
| UC-020 | **A — Substantive** (Batch 06, promoted từ B, CANDIDATE) | SCR-011 fully authored: STATE-002-canonical required-context gate (ux-blueprint.md §11 explicitly lists SCR-011 in STATE-002's own row — no disclaimer needed, unlike Batch 05's SCR-008/009 situation), real per-side Instance+mode selection materially reaching all three scenarios (same mode both sides = Backtest-vs-Backtest or PAPER-vs-PAPER; different modes = cross-mode), each side rendered from `EVIDENCE[instanceId][mode]` independently (never merged), missing-outcome renders empty for exactly one side without failing the other, RETIRED Instance's evidence links to VIEW-005 with identity preserved, `authority-label-recomputation` "Read-only / non-authoritative comparison presentation" badge distinct from each family's own authority label, zero score/ranking/normalization function anywhere — matches `ux-blueprint.md` §7.6 SCR-011 spec + `use-case-workflow.md` UC-020 Main flow steps 1-5. |
| UC-021 | **A — Substantive** (Batch 06, promoted từ B, CANDIDATE) | VIEW-005 fully authored: old version identity (`sdv-v0.9`) always rendered first, unconditionally; mode selector (Backtest/PAPER/Both) resolves each family independently via `renderView005Families()`; STATE-025 (complete) and STATE-026 (PAPER Fill/Position unavailable, Backtest remains available) both materially reachable via the SAME QA flag `state.oldVersionPaperFillAvailable` that SCR-011 also reads (single source of truth, no drift between screens); missing-family panel discloses reason, marks the rest "incomplete," never hides/fabricates; explicit `<div>` states the missing part does NOT mean the entire old-version history is unavailable — matches `ux-blueprint.md` §7.6 VIEW-005 spec + `use-case-workflow.md` UC-021 Main flow + Alternate/failure. |
| UC-001..UC-018 | **A — Substantive** (Batch 01-05, giữ nguyên) | Fully authored + independently verified tại Batch 01-05 (mỗi batch tự nó qua đầy đủ Review A + Independent Review B, verdict `READY_FOR_NEXT_PHASE2_BATCH`). Batch 06 CHỈ link tới Research/Replay/Backtest/Paper/Review (real nav link) — KHÔNG re-author, NHƯNG cumulative classification VẪN A. UC-002 specifically: VIEW-006's handoff cites it as the downstream consumer, but Batch 06 does NOT re-author VIEW-001 — UC-002's own A classification remains sourced ENTIRELY from Batch 01, not double-counted here. |

## 2. Cumulative Phase-2 UC ledger (Batch 01-05 verified + Batch 06 candidate)

```text
Trước Batch 06 (Batch 01-05, ĐÃ independently verified — xem ../batch-05/traceability.md §2):
  A = {001,002,003,004,005,006,007,008,009,010,011,012,013,014,015,016,017,018}   (18)
  B = {019,020,021}                                                                (3)
  C = {}                                                                           (0)

Batch 06 di chuyển UC-019,020,021 từ B → A (SCR-010/SCR-011/VIEW-005 tự author đủ
  representation; VIEW-006 represents the UC-019→UC-002 handoff, UC-002 not re-counted).

Sau Batch 06 (CANDIDATE — CHƯA independently verified cho phần Batch 06):
  A = {001,002,003,004,005,006,007,008,009,010,011,012,013,014,015,016,017,018,019,020,021}   (21)
  B = {}                                                                                        (0)
  C = {}                                                                                        (0)
```

```text
Partition validation (mechanical):
  |A| = 21, |B| = 0, |C| = 0.  21 + 0 + 0 = 21.  Đúng.
  A ∩ B: {001..021} ∩ {} = ∅.  Đúng (trivial).
  A ∩ C: {001..021} ∩ {} = ∅.  Đúng (trivial).
  B ∩ C: {} ∩ {} = ∅.  Đúng (trivial).
  A ∪ B ∪ C = {001..021} — liệt kê tuần tự xác nhận KHÔNG thiếu UC nào: 001..021 (A, 21 liên
    tiếp) — 21 UC, mỗi UC xuất hiện ĐÚNG MỘT LẦN.

21-UC substantive completion progress: 21/21 (A only) — CANDIDATE tại transaction này (Batch 06's
  own Review A + Independent Review B CHƯA thực hiện — chỉ authoring transaction, KHÔNG claim
  independently verified). Last independently verified: 18/21 (UC-001..018, Batch 01-05 baseline,
  mỗi batch đã qua đầy đủ Review A + Independent Review B).

IMPORTANT: candidate 21/21 UC (và candidate 17/17 surface, §ngay dưới) tại thời điểm authoring
  KHÔNG establish Phase-2 substantive completion — completion đòi hỏi Batch 06's own Review A +
  Independent Review B COMPLETE trước, VÀ tách biệt hoàn toàn khỏi Quality Gate/Gate 3/
  P2-RETRO-001/Phase 3/LIVE authorization, KHÔNG một trong số đó được transaction này chạm tới.
```

Surface progress (17-surface set, `SCR-001`–`SCR-011`/`VIEW-001`–`VIEW-006`, `phase-2-dod.md` §3
criterion 3a): trước Batch 06 = 13/17 (Batch 01-05). Batch 06 thêm `SCR-010`, `VIEW-006`,
`SCR-011`, `VIEW-005` (+4) → candidate 17/17 (full 17-surface set represented). CANDIDATE, KHÔNG
independently verified.

## 3. Element-level traceability map

**Ghi chú:** SCR-010 trace RIÊNG BIỆT theo bảy khía cạnh yêu cầu (existing Definition identity,
old version identity, creation action, new immutable version identity, old/new separation,
handoff to VIEW-006, optional Research handoff). VIEW-006 trace RIÊNG BIỆT theo tám khía cạnh yêu
cầu (required new-version context, registration ready, registration unavailable, registration
action, new Strategy Instance identity, exact Instance→new-Version binding, handoff to VIEW-001,
distinction from selection/pinning). SCR-011 trace RIÊNG BIỆT theo bảy khía cạnh yêu cầu
(Instance/version selection, Backtest-vs-Backtest, PAPER-vs-PAPER, cross-mode, per-column
mode/authority labels, missing-outcome per-Instance behavior, old-version route to VIEW-005, no
unified outcome/scoring). VIEW-005 trace RIÊNG BIỆT theo chín khía cạnh yêu cầu (old-version
identity always visible, mode selector, Backtest family, PAPER family, both-families separation,
STATE-025, STATE-026, missing-family/type disclosure, return to SCR-011) — KHÔNG một hàng gộp nào
cho UC-019/UC-020/UC-021.

### SCR-010 — Strategy Definition Version Creation (UC-019)

| Prototype element (file:selector) | UX Blueprint / Domain ID | UC | PR | Authoritative source section |
|---|---|---|---|---|
| `app.js` `renderScr010()` "Existing Strategy Definition + current version" `.evidence-group-upstream` block | SCR-010 "Required context" — một Strategy Definition (identity) đã tồn tại | UC-019 | PR-031 | `ux-blueprint.md` §7.6 SCR-010 "Required context"; `use-case-workflow.md` UC-019 Preconditions |
| `app.js` `VERSION_FIXTURES["sdv-v1.0"]` fields (`strategy_definition_version_id`/`strategy_definition_id`/`thesis`/`supported_scope`/`required_input_contracts`/`decision_rule_ref`/`explanation_contract_ref`/`downstream_output_capability`) | Old `strategy_definition_version_id` — exact seven-field schema, KHÔNG hơn | UC-019 | PR-031 | `strategy.md` §1 `StrategyDefinitionVersionRegistered` schema (exactly these seven fields) |
| `index.html`/`app.js` `#scr010-thesis`/`#scr010-scope` editable fields + `#btn-create-version` | SCR-010 "Available user actions" — Tạo Strategy Definition Version mới; material interaction requirement | UC-019 | PR-031 | `ux-blueprint.md` §7.6 SCR-010 "Available user actions"; task requirement "the creation control must not be inert" |
| `app.js` `buildNewVersion()` (new `strategy_definition_version_id` = `sdv-v1.` + counter, append-only, `VERSION_FIXTURES` never mutated) | SCR-010 "System-owned actions" — Gán version identity mới, tách biệt version cũ (append-only) | UC-019 | PR-031 | `ux-blueprint.md` §7.6 SCR-010 "System-owned actions"; `strategy.md` §1 invariants (opaque, immutable, no same-ID replacement) |
| `app.js` `renderScr010Result()` "New Strategy Definition Version created" panel, incl. explicit "Old version ... is UNCHANGED" hint re-reading the same unmutated fixture | SCR-010 "Observable outcome" — Version mới tạo thành công, độc lập version cũ (INV-1) | UC-019 | PR-031 | `use-case-workflow.md` UC-019 "Observable outcome"; task INV-1 |
| `app.js` `#btn-scr010-to-view006` | SCR-010 "Exit points" — VIEW-006 | UC-019 | PR-031 | `ux-blueprint.md` §7.6 SCR-010 "Exit points" |
| `app.js` `#btn-scr010-to-scr011` | SCR-010 "Exit points" — SCR-011 (so sánh version, khi áp dụng) | UC-019 | PR-031 | `ux-blueprint.md` §7.6 SCR-010 "Exit points" |
| `index.html` real link to `../batch-01/index.html` ("Open Research (SCR-001) read-only, optional") | SCR-010 "Exit points" — SCR-001 (quan sát read-only tuỳ chọn, KHÔNG cần pin) | UC-019 | PR-031 | `ux-blueprint.md` §7.6 SCR-010 "Exit points"; task "Improve → Research loop-back" |
| `index.html` `.label-row` authority labels ("Represented authority class: authoritative Strategy registration") | SCR-010 "Authority labels" | UC-019 | PR-031 | `ux-blueprint.md` §7.6 SCR-010 "Authority labels" |
| Absence of "Empty/unavailable/blocked" branch anywhere in `renderScr010()` | SCR-010 "Empty/unavailable/blocked states: KHÔNG áp dụng tại tầng UX" | UC-019 | PR-031 | `ux-blueprint.md` §7.6 SCR-010 "Empty/unavailable/blocked states" |

### VIEW-006 — Strategy Instance Creation/Binding (UC-019 handoff, UC-002 downstream)

| Prototype element (file:selector) | UX Blueprint / Domain ID | UC | PR | Authoritative source section |
|---|---|---|---|---|
| `app.js` `renderView006()` `!target` branch — "Registration unavailable" (four-part fallback: stop, disclose reason, preserve `sd-fam-001` identity, no authoritative action; no new STATE-XXX invented) | VIEW-006 "Empty/unavailable/blocked states" — registration unavailable khi thiếu danh tính Strategy Definition Version mới | UC-019 | PR-031 | `ux-blueprint.md` §7.6 VIEW-006 "Empty/unavailable/blocked states" |
| `app.js` `latestCreatedVersion()` used as `target`, "registration ready" branch (no `existingInstance` yet) | VIEW-006 "Primary states" — registration ready | UC-019 | PR-031 | `ux-blueprint.md` §7.6 VIEW-006 "Primary states" |
| `index.html`/`app.js` `#btn-register-instance` | VIEW-006 "Available user actions" — Tạo/đăng ký Strategy Instance cho Version này | UC-019 | PR-001, PR-016 | `ux-blueprint.md` §7.6 VIEW-006 "Available user actions" |
| `app.js` `registerInstance()` (new `strategy_instance_id` = `inst-b-` + counter, distinct from `inst-a`/`inst-old-001`, `INSTANCE_FIXTURES` never mutated) | VIEW-006 "System-owned actions" — Đăng ký một Strategy Instance identity RIÊNG BIỆT | UC-019 | PR-031, PR-001 | `ux-blueprint.md` §7.6 VIEW-006 "System-owned actions"; `strategy.md` §6 `StrategyInstanceRegistered` schema |
| `app.js` `renderView006()` `existingInstance` branch — "Registration completed" panel (Strategy Definition identity + new Version identity + new Instance identity + explicit binding row `instanceId + " → " + versionRef`) | VIEW-006 "Information displayed" — sau khi đăng ký thành công, danh tính Instance đã đăng ký + liên kết tường minh | UC-019 | PR-031, PR-001, PR-016 | `ux-blueprint.md` §7.6 VIEW-006 "Information displayed"; "Registration result" (task) |
| `app.js` explicit "Distinct from the pre-existing Instance inst-a" hint | Old/new Strategy Instance identities remain distinct — KHÔNG silently reuse old Instance | UC-019 | PR-031 | task "Old and new Strategy Instance identities must remain distinct" |
| `index.html`/`app.js` real link `../batch-01/index.html` labelled "Instance is now available to select/pin through VIEW-001 →" (exact required wording) | VIEW-006 "Exit points" — VIEW-001 (chọn/pin Instance vừa đăng ký) | UC-019, UC-002 | PR-031, PR-001, PR-016 | `ux-blueprint.md` §7.6 VIEW-006 "Exit points"; task "Wording must be exact" |
| Explicit hint "This is NOT a claim that the Instance is now pinned — no Replay pin, Backtest pin, or Paper pin is created here" + absence of any pin-setting code anywhere in `app.js` (grep clean) | VIEW-006 distinct from VIEW-001 selection/pinning (INV-3) | UC-019 | PR-016 | `ux-blueprint.md` §7.6 VIEW-006 Purpose ("KHÔNG phải chính bản thân UC-002"); task INV-3 |
| `index.html` `.label-row` authority labels (same convention as SCR-010) | VIEW-006 "Authority labels" | UC-019 | PR-031 | `ux-blueprint.md` §7.6 VIEW-006 "Authority labels" |

### SCR-011 — Strategy Version Comparison (UC-020)

| Prototype element (file:selector) | UX Blueprint / Domain ID | UC | PR | Authoritative source section |
|---|---|---|---|---|
| `app.js` `state.scr011EvidenceExists` / `renderScr011()` `count < 2` branch — STATE-002 | STATE-002 empty (canonical row, ux-blueprint.md §11 explicitly lists SCR-011 — "dưới hai Strategy Instance đã đăng ký để so sánh"; unlike Batch 05's SCR-008/009, NO disclaimer needed — this is genuine canonical membership) | UC-020 (alternate/failure) | PR-021, PR-034 | `ux-blueprint.md` §11 STATE-002 row (SCR-011 explicitly listed) |
| `index.html`/`app.js` `#scr011-inst-A`/`#scr011-mode-A`/`#scr011-inst-B`/`#scr011-mode-B` (independent per-side Instance+mode selection) | SCR-011 "Available user actions" — Chọn Strategy Instance cần so sánh; chọn mode so sánh | UC-020 | PR-031, PR-032 | `ux-blueprint.md` §7.6 SCR-011 "Available user actions"; `use-case-workflow.md` UC-020 Main flow bước 1 |
| `app.js` `renderComparisonSide()` when both sides select mode=`backtest` (Scenario A) | SCR-011 "Information displayed" — Backtest vs Backtest, non-PAPER authority, tách biệt hoàn toàn | UC-020 | PR-031, PR-032 | `use-case-workflow.md` UC-020 Main flow bước 2 |
| `app.js` `renderComparisonSide()` when both sides select mode=`paper` (Scenario B) | SCR-011 "Information displayed" — PAPER vs PAPER, authoritative, tách biệt hoàn toàn | UC-020 | PR-031, PR-032 | `use-case-workflow.md` UC-020 Main flow bước 3 |
| `app.js` `renderComparisonSide()` when sides select different modes (Scenario C, cross-mode) | SCR-011 "Information displayed" — cross-mode side-by-side, mỗi bên gắn nhãn mode/authority/evidence-type/Instance identity/Version identity | UC-020 | PR-031, PR-032 | `use-case-workflow.md` UC-020 Main flow bước 4 |
| `app.js` `renderBacktestFamilyHtml()`/`renderPaperFamilyHtml()` (two fully separate functions, never called together into one merged object) + `index.html` `.label-row` per-column `authority-label-recomputation`("non-PAPER simulated")/`authority-label-authoritative`("authoritative PAPER") | SCR-011 "Authority labels" — gắn nhãn RIÊNG cho từng cột/panel, authority KHÔNG BAO GIỜ trộn lẫn | UC-020 | PR-031, PR-032 | `ux-blueprint.md` §7.6 SCR-011 "Authority labels" |
| `app.js` `renderComparisonSide()` `!famObj` branch — "No outcome yet" (renders for exactly one side, `EVIDENCE` lookup miss for newly-registered Instances) | SCR-011 "Alternate/failure" — Một Strategy Instance chưa có outcome nào → hiển thị rỗng cho Instance đó, KHÔNG lỗi cho toàn bộ so sánh | UC-020 (alternate/failure) | PR-031, PR-032 | `use-case-workflow.md` UC-020 "Alternate/failure" |
| `app.js` `inst.status === "RETIRED"` branch, `#btn-scr011-to-view005-A`/`-B` | SCR-011 "Exit points" — VIEW-005 (nếu version cũ không active) | UC-020 | PR-031, PR-032 | `ux-blueprint.md` §7.6 SCR-011 "Exit points"; `use-case-workflow.md` UC-020 Main flow bước 5 |
| `index.html` `.label-row` top-level `authority-label-recomputation` "Read-only / non-authoritative comparison presentation" | SCR-011 comparison-result authority label (task requirement, distinct from each family's own label) | UC-020 | PR-031, PR-032 | task "Authority labels" section; `use-case-workflow.md` UC-020 "Evidence produced: KHÔNG" |
| Absence of any score/ranking/normalization function anywhere in `app.js` (grep clean for "score"/"rank"/"normalize") | SCR-011 "System-owned actions" — KHÔNG unified outcome card, KHÔNG single normalized score, KHÔNG common execution result, KHÔNG automatic ranking | UC-020 | PR-031, PR-032 | `ux-blueprint.md` §7.6 SCR-011 "System-owned actions"; `use-case-workflow.md` UC-020 "Out-of-scope boundary" |

### VIEW-005 — Old-Version Evidence Access (UC-021)

| Prototype element (file:selector) | UX Blueprint / Domain ID | UC | PR | Authoritative source section |
|---|---|---|---|---|
| `app.js` `renderView005()` first `el5(...)` row (`oldVersion.strategyDefinitionVersionId`), rendered unconditionally before any mode selection | VIEW-005 "Information displayed" — Danh tính version (LUÔN hiển thị) | UC-021 | PR-032 | `ux-blueprint.md` §7.6 VIEW-005 "Information displayed"; `use-case-workflow.md` UC-021 Main flow bước 1 |
| `index.html`/`app.js` `#view005-mode-selector` `[data-mode="backtest"/"paper"/"both"]` | VIEW-005 "Available user actions" — Chọn mode cần resolve | UC-021 | PR-032 | `ux-blueprint.md` §7.6 VIEW-005 "Available user actions" |
| `app.js` `renderView005Families()` backtest branch (`famData.backtest`, non-PAPER) | VIEW-005 "Information displayed" — Backtest evidence family khi áp dụng | UC-021 | PR-032 | `use-case-workflow.md` UC-021 Main flow bước 2 |
| `app.js` `renderView005Families()` paper branch (`famData.paper`, authoritative) | VIEW-005 "Information displayed" — PAPER evidence family khi áp dụng | UC-021 | PR-032 | `use-case-workflow.md` UC-021 Main flow bước 3 |
| `app.js` `renderView005Families()` "both" branch — two separate `.evidence-group` blocks, never merged | VIEW-005 "Information displayed" — HAI HỌ HIỂN THỊ TÁCH BIỆT hoàn toàn | UC-021 | PR-032 | `use-case-workflow.md` UC-021 Main flow bước 4 |
| `app.js` `state.oldVersionPaperFillAvailable = true` / `renderView005Families()` overall-state panel — STATE-025 | STATE-025 old-version evidence complete | UC-021 | PR-032 | `ux-blueprint.md` §11 STATE-025 row |
| `app.js` `state.oldVersionPaperFillAvailable = false` / `renderPaperFamilyHtml()` "Fill / Position — incomplete" panel + overall-state STATE-026 panel (Backtest remains available, PAPER Fill/Position unavailable — coherent single fixture, reason disclosed, explicit "does NOT mean entire history unavailable" statement) | STATE-026 old-version evidence partially unavailable | UC-021 (alternate/failure) | PR-032 | `ux-blueprint.md` §11 STATE-026 row; `use-case-workflow.md` UC-021 "Alternate/failure" (all nine sub-requirements: stop only affected part, identity/mode/authority visible, available evidence visible+marked incomplete, missing family identified, reason disclosed, no fabrication, no silent omission, no false completeness claim, no "entire history unavailable" implication) |
| `app.js` `#btn-view005-to-scr011` | VIEW-005 "Exit points" — Trở lại SCR-011 với evidence resolved | UC-021 | PR-032 | `ux-blueprint.md` §7.6 VIEW-005 "Exit points" |
| `app.js` `state.view005EntryNote` set by SCR-011's `#btn-scr011-to-view005-*` (same `inst-old-001`/`sdv-v0.9` identity, no unrelated fixture) + `state.oldVersionPaperFillAvailable` shared flag (SCR-011 and VIEW-005 both read it) | SCR-011↔VIEW-005 identity continuity — SAME old Strategy Definition Version identity; resolved/partial evidence stays associated with that version on return | UC-020, UC-021 | PR-031, PR-032 | task "SCR-011 ↔ VIEW-005 identity continuity" |

### Shared / NAV-006

| Prototype element (file:selector) | UX Blueprint / Domain ID | UC | PR | Authoritative source section |
|---|---|---|---|---|
| `index.html` `#shell`/`#context-bar` (bounded subset, reused convention) | WS-001 | UC-019, UC-020, UC-021 | PR-002 | `ux-blueprint.md` §5 "WS-001" table (same authority as Batch 01-05, re-derived independently in this batch's own files) |
| `index.html` `[data-nav="NAV-001"]`..`[NAV-005]` (real links to Batch 01-05) | NAV-001..NAV-005 | UC-001, UC-002 (precondition), UC-004, UC-006, UC-011, UC-016, UC-017, UC-018 | (inherited, see each batch's own traceability) | genuine navigation to already-authored Batch 01-05 screens, NOT a new representation |
| `index.html` `[data-nav="NAV-006"]` (Improve, active), `[data-target="screen-improve"]` | NAV-006 | UC-019, UC-002 (VIEW-006 handoff), UC-020, UC-021 | PR-031, PR-001, PR-016, PR-032 | `ux-blueprint.md` §5a "NAV-006 — Improve" |
| `app.js` `showScreen("screen-improve")` always reachable regardless of any downstream precondition | NAV-006 "Required context is action-specific, not a navigation blocker" | UC-019, UC-020, UC-021 | PR-031, PR-032 | `ux-blueprint.md` §5a NAV-006 "Available navigation behavior" |
| Absence of any organization/strategy-administration control anywhere in `index.html`/`app.js` | NAV-006 "Out-of-scope boundary" — KHÔNG organization/strategy-administration behavior | UC-019, UC-020, UC-021 | PR-031, PR-032 | `ux-blueprint.md` §5a NAV-006 "Out-of-scope boundary" |
| `#qa-panel`/`#qa-body` (QA state switcher) | (Prototype tooling — explicitly NOT part of authoritative UX) | — | — | N/A — exists only to let STATE-002/STATE-025/STATE-026 be inspected without a real event log/Strategy engine |

## 4. Reconciliation statement (I-12 Verification)

```text
Mọi hàng ở §3 trên trace được, đối chiếu trực tiếp, về đúng một section cụ thể trong
  docs/product/ux-blueprint.md (Package 0.3-C, Consolidated Stable), docs/product/use-case-
  workflow.md (Package 0.3-B, Consolidated Stable), hoặc docs/domain/strategy.md — đây LÀ "rebuild
  hoặc đối chiếu hoàn toàn từ authoritative source" per I-12's Verification (Chapter 2 §I-12).
KHÔNG một NAV-XXX/SCR-XXX/VIEW-XXX/STATE-XXX/UC-XXX/PR-XXX ID nào xuất hiện trong Batch 06 mà
  KHÔNG có hàng tương ứng ở §3.
KHÔNG một UC/PR/domain concept mới nào originate trong Batch 06 — verify trực tiếp: prototype/
  phase-2/batch-06/*.{html,css,js} KHÔNG tạo entity/event/state-machine mới (mọi identity là
  hardcoded/counter-generated illustrative string, KHÔNG API/database/event contract), KHÔNG
  invent Strategy Definition field beyond strategy.md §1's exact seven, KHÔNG mutable "latest
  strategy" object (VERSION_FIXTURES/INSTANCE_FIXTURES never mutated in place — grep clean for
  any assignment into their own keys), KHÔNG version graph/approval workflow/strategy DSL/
  optimizer/scoring function, KHÔNG unified Backtest/PAPER outcome object.
§2's cumulative UC ledger LÀ completion accounting (Chapter 12/phase-2-dod.md §3 purpose) —
  TÁCH BIỆT khỏi §3's element-to-authority traceability map (I-12 purpose). Mọi UC cited tại §3
  đều resolve nhất quán vào ĐÚNG MỘT hạng mục tại §2's partition — verify trực tiếp, KHÔNG UC nào
  tại §3 rơi ngoài {A} đã định nghĩa tại §2 (B/C rỗng, candidate, sau Batch 06).
```

## 5. Six non-negotiable Improve invariants — verified explicitly

```text
INV-1 (new version = new immutable identity): verified — buildNewVersion() only ever pushes a
  brand-new object with a counter-generated strategy_definition_version_id into
  state.createdVersions; VERSION_FIXTURES["sdv-v1.0"] is never assigned to, only read (grep clean
  for "VERSION_FIXTURES[" on the left-hand side of an assignment). renderScr010Result() re-reads
  the SAME old-version object after creation and displays it unchanged, proving no in-place
  mutation. The new version's strategy_definition_id equals STRATEGY_DEFINITION_ID — same family,
  distinct version id.

INV-2 (no invented Strategy Definition schema): verified — every field in VERSION_FIXTURES and
  buildNewVersion()'s new object is exactly one of strategy.md §1's seven
  StrategyDefinitionVersionRegistered payload fields (strategy_definition_version_id,
  strategy_definition_id, thesis, supported_scope, required_input_contracts, decision_rule_ref,
  explanation_contract_ref, downstream_output_capability) — no DSL, compiler, rule language,
  validation taxonomy, version graph, or approval workflow field exists anywhere.

INV-3 (VIEW-006 registration is not VIEW-001 selection/pinning): verified — registerInstance()
  only sets strategy.md §6 StrategyInstanceRegistered-shaped fields (never a "pinnedForReplay"/
  "pinnedForBacktest"/"pinnedForPaper" flag, grep clean); the handoff link text is the exact
  required wording "Instance is now available to select/pin through VIEW-001," a real link to
  ../batch-01/index.html (no re-authoring of VIEW-001's own substance); an explicit hint states
  this is NOT a claim of pinning.

INV-4 (version comparison keeps evidence families separate): verified — renderBacktestFamilyHtml()
  and renderPaperFamilyHtml() are two entirely separate functions, never called into a shared
  merged structure; each comparison side resolves EVIDENCE[instanceId][mode] independently; no
  score/rank/normalize function exists anywhere in app.js (grep clean); cross-mode rendering shows
  each side's own mode/authority/Instance-identity/Version-identity label, never a single unified
  card.

INV-5 (old-version evidence remains accessible): verified — renderView005() renders the old
  version's identity as the FIRST element, unconditionally, before any mode selection or family
  resolution; STATE-026's "incomplete" panel never removes the version identity, mode, or
  authority labels from view; the Backtest family remains fully visible even when the PAPER
  family's Fill/Position is unavailable (and vice versa is structurally possible via the same
  independent-resolution code path).

INV-6 (registration vs inspection actions): verified — buildNewVersion()/registerInstance() are
  the ONLY two functions in app.js that create a new prototype-local record; every SCR-011/
  VIEW-005 render function (renderScr011/renderComparisonSide/renderView005/
  renderView005Families) only reads VERSION_FIXTURES/INSTANCE_FIXTURES/EVIDENCE/state.* and never
  calls buildNewVersion()/registerInstance() or writes a new record.
```
