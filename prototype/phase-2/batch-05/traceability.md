---
id: phase-2-batch-05-traceability
title: "Phase 2 Prototype — Batch 05 — Traceability Artifact"
version: "1.2"
status: Candidate
owner: Product Owner
created_at: "2026-08-14"
---

# Phase 2 Prototype — Batch 05 — Traceability Artifact

**v1.2 — deterministic bookkeeping reconciliation (2026-08-14), vai trò: `Phase 2 Prototype
Batch 05 Review-State Reconciliation Executor`, đúng `G-TXN-003`.** KHÔNG PHẢI lifecycle
transition, KHÔNG PHẢI prototype semantic correction. §2's tiêu đề VÀ kết luận vẫn nói "candidate
tại transaction này ... KHÔNG claim independently verified" — mâu thuẫn trực tiếp với governed
review history ĐÃ hoàn tất từ v1.1 (final bounded Review A v1.1: hai finding tất cả CLOSED,
0/0/0, CLEAN; final Independent Review B v1.1: cùng hai finding CLOSED, 0/0/0, verdict
`READY_FOR_NEXT_PHASE2_BATCH`). Sửa: §2's tiêu đề + kết luận + surface-progress câu viết lại để
phản ánh 18/21 UC + 13/17 surface ĐÃ independently verified. KHÔNG đổi §0/§1/§3/§4/§5 (A/B/C
partition, element-level map, reconciliation statement, four Review invariant verification KHÔNG
đổi — VẪN A=18/B=3/C=0/tổng=21).

**v1.1 — bounded correction (2026-08-14), Review A trên v1.0: `P2-B05-A-MAJ-01` (Major) +
`P2-B05-A-MIN-01` (Minor) — đóng CẢ HAI tại transaction này.** `P2-B05-A-MAJ-01`: SCR-009's
correction-visible branch (`C-100`) chỉ disclose invalidation đã xảy ra (`invalidation_reason`/
`invalidated_fact_ref`/recorded_time) — KHÔNG hiển thị later replacement value (`PD-101`/`LONG`)
hay explicit old→new difference, khiến UC-017 KHÔNG thỏa mãn được nếu KHÔNG đi tiếp tới VIEW-004.
Sửa: thêm một panel MỚI, riêng biệt ("Later-correction comparison") — hiển thị historical cursor,
fact gốc (`PD-100`/`NO_ACTION`, KHÔNG đổi), invalidation đầy đủ, later replacement (`PD-101`/
`LONG`, `supersedes_fact_ref=PD-100`, recorded_time), VÀ một comparison-result row tường minh
(`NO_ACTION → LONG`) gắn nhãn non-authoritative — TÁCH BIỆT khỏi các row authoritative phía trên.
Historical panel gốc (ReplayState(C-100)/recorded-at-cursor) VẪN KHÔNG đổi (no repaint) — panel
mới thuần túy additive, dùng LẠI CHÍNH XÁC `MOCK_DECISION_CORRECTION` object đã share với
VIEW-004 (KHÔNG duplicate fixture). `P2-B05-A-MIN-01`: SCR-008's exit button "Compare this
trace's cursor in Historical State Comparison" ngụ ý sai rằng cursor của lineage đang chọn được
carry forward sang SCR-009 — trong khi `LINEAGE_FILLS` KHÔNG mang mapped Replay Cursor nào, VÀ
SCR-009 tự chọn cursor độc lập. Sửa: đổi tên thành "Open Historical State Comparison (SCR-009)"
+ thêm disclosure tường minh "the historical comparison target (Replay Cursor) is selected
independently on SCR-009." KHÔNG đổi A/B/C partition, KHÔNG surface mới, KHÔNG claim independently
verified. Xem `app.js`'s own v1.1 inline comments cho code-level chi tiết.

**Vai trò của tài liệu này:** đây LÀ I-12 (Single Source of Truth) conformance evidence cho Batch
05, per `docs/phase-dod/phase-2-dod.md` §2's applicable Trigger A / I-12 requirement — mọi phần tử
prototype trong batch này PHẢI trace được TRỰC TIẾP về đúng một hoặc nhiều `SCR-XXX`/`NAV-XXX`/
`STATE-XXX` đã `Consolidated Stable` trong [`docs/product/ux-blueprint.md`](../../../docs/product/ux-blueprint.md),
VÀ về đúng `UC-XXX` đã `Consolidated Stable` trong [`docs/product/use-case-workflow.md`](../../../docs/product/use-case-workflow.md),
VÀ về đúng `PR-XXX`/Domain Contract field đã tồn tại. Prototype LÀ derived representation — KHÔNG
một UC/PR/domain concept nào originate tại đây. Áp dụng ĐÚNG taxonomy A/B/C đã establish tại
`../batch-01/traceability.md` §0, kế thừa nguyên vẹn qua Batch 02/03/04.

## 0. UC accounting taxonomy (kế thừa nguyên vẹn từ Batch 01/02/03/04, KHÔNG redefine)

```text
A. SUBSTANTIVELY COVERED — Batch tự author ĐỦ representation (screen/view + required context +
   primary/blocked states + exit behavior đúng ux-blueprint.md/use-case-workflow.md spec) để tính
   vào 21-UC completion numerator (phase-2-dod.md §3).
B. PARTIAL / REFERENCED — UC xuất hiện qua global shell context, nav-button existence, handoff
   affordance, hay deferred-placeholder destination — KHÔNG đủ để tính vào numerator.
C. DEFERRED / NOT YET REPRESENTED — KHÔNG một element nào trong batch tham chiếu UC đó.
```

## 1. Batch-05-authored substantive contribution (distinct từ cumulative ledger, §2 dưới)

```text
Batch-05-authored substantive UC (NEW tại batch này, 3):
  UC-016 (SCR-008 — Decision → Position Lineage Trace: causation trace + Decision explainability,
    tách biệt tường minh)
  UC-017 (SCR-009 — Historical State Comparison: ReplayState(C) reconstructed vs. recorded state,
    No conflict / correction-visible-after-cursor)
  UC-018 (VIEW-004 — Correction Inspection: original fact + invalidation + replacement, luôn cả
    hai trạng thái, KHÔNG repaint)

UC-016 was previously hạng B (referenced only via NAV-005's nav-button-existence citation, Batch
  01-04) — nay promote lên A vì SCR-008 tự author đủ representation (required-context gate, real
  Fill-selection control, đầy đủ bảy mắt xích causation Fill→ExecutionResult→Order→Execution
  Intent→RiskEvaluation→Trade Intent→Decision KHÔNG thiếu, Decision explainability evidence tách
  biệt tường minh khỏi causation trace) đúng `ux-blueprint.md` §7.5 SCR-008 spec VÀ
  `use-case-workflow.md` UC-016 detailed block.
UC-017 previously hạng B — nay promote lên A vì SCR-009 tự author đủ representation
  (required-context gate, real cursor-selection control, cả hai outcome "No conflict" VÀ
  "correction visible after historical cursor" materially reachable, historical value KHÔNG BAO
  GIỜ bị repaint) đúng `ux-blueprint.md` §7.5 SCR-009 spec VÀ `use-case-workflow.md` UC-017
  detailed block.
UC-018 previously hạng B — nay promote lên A vì VIEW-004 tự author đủ representation (fact gốc
  VẪN resolvable + fact replacement + `supersedes_fact_ref` link tường minh, CẢ HAI trạng thái
  LUÔN hiển thị đồng thời, KHÔNG một nhánh nào chỉ show giá trị "đã sửa") đúng `ux-blueprint.md`
  §7.5 VIEW-004 spec VÀ `use-case-workflow.md` UC-018 detailed block.

Batch-01/02/03/04-verified substantive UC (KHÔNG re-authored, KHÔNG double-counted, VẪN A):
  UC-001..UC-015.
```

| UC | Classification | Evidence / reason |
|---|---|---|
| UC-016 | **A — Substantive** (Batch 05, promoted từ B) | SCR-008 fully authored: STATE-002-labelled required-context gate (§3 below, disclaimer re: STATE-002's own narrower canonical scope), real Fill-selection control (`FILL-RV-A-001` LONG / `FILL-RV-B-001` SHORT, two genuinely distinct already-recorded lineages — never one mutated into the other) that materially updates the displayed trace, exactly the seven-link chain UC-016 itself names (Fill→ExecutionResult→Order→Execution Intent→RiskEvaluation→Trade Intent→Decision, no extra/invented nodes, none missing), Decision explainability group (outcome/Strategy Instance/Strategy Definition Version/recorded input snapshot/recorded evaluation evidence) rendered as a SEPARATE evidence group from the causation trace, resolved directly from the recorded fixture (no re-derivation) — matches `ux-blueprint.md` §7.5 SCR-008 spec + `use-case-workflow.md` UC-016 Main flow. |
| UC-017 | **A — Substantive** (Batch 05, promoted từ B; v1.1 đóng `P2-B05-A-MAJ-01`) | SCR-009 fully authored: STATE-002-labelled required-context gate, real cursor-selection control (`C-200` / `C-100`, two genuinely distinct already-run Replay Cursors), "ReplayState(C) reconstructed now" panel structurally identical to "state recorded/originally displayed at that cursor" panel (deterministic no-look-ahead fold, replay-event.md §2 — proves no-drift by construction, not by coincidence), correction-check panel materially reaching BOTH outcomes ("No conflict" for `C-200`; "Correction visible after historical cursor" for `C-100`). **v1.1:** the `C-100` branch now ALSO renders a dedicated "Later-correction comparison" panel showing the original historical fact (`PD-100`/`NO_ACTION`, unchanged), the full invalidation record, the later replacement (`PD-101`/`LONG`, `supersedes_fact_ref=PD-100`), and an explicit `NO_ACTION → LONG` comparison-result row — the historical panels above remain byte-for-byte unchanged (no repaint). Authority labels split explicitly: `authority-label-authoritative` for original/invalidation/replacement rows, `authority-label-recomputation` (non-authoritative) for the comparison-result row only — matches `ux-blueprint.md` §7.5 SCR-009 spec + `use-case-workflow.md` UC-017 Main flow + `replay-event.md` §2 no-look-ahead invariant. |
| UC-018 | **A — Substantive** (Batch 05, promoted từ B) | VIEW-004 fully authored: original fact panel (`PD-100`, still resolvable, explicitly labelled append-only) AND invalidation+replacement panel (`DecisionFactInvalidated` — `invalidated_fact_ref`/`invalidation_reason`; replacement `DecisionRecorded` `PD-101` — `supersedes_fact_ref` pointing DIRECTLY at `PD-100`, same `decision_context_cursor`) rendered SIMULTANEOUSLY, unconditionally, no empty/blocked branch (matches ux-blueprint.md's explicit "KHÔNG áp dụng — hiển thị luôn cả hai trạng thái là hành vi bắt buộc"), explicit `supersedes_fact_ref` binding called out in its own hint row, plus an explicit scope note disclosing that RiskEvaluation/Fill share this direct pattern while ExecutionResult's is materially different and PaperExecutionObservation/Position have none — matches `ux-blueprint.md` §7.5 VIEW-004 spec + `use-case-workflow.md` UC-018 Main flow + `decision.md` §6/§11. |
| UC-001..UC-015 | **A — Substantive** (Batch 01/02/03/04, giữ nguyên) | Fully authored + independently verified tại Batch 01/02/03/04 (mỗi batch tự nó qua đầy đủ Review A + Independent Review B, verdict `READY_FOR_NEXT_PHASE2_BATCH`). Batch 05 CHỈ link tới Research/Replay/Backtest/Paper (real nav link) — KHÔNG re-author, NHƯNG cumulative classification VẪN A (một UC KHÔNG thể vừa A vừa B/C). |

## 2. Cumulative Phase-2 UC ledger (Batch 01+02+03+04 verified + Batch 05 candidate)

```text
Trước Batch 05 (Batch 01+02+03+04, ĐÃ independently verified — xem ../batch-04/traceability.md §2):
  A = {001,002,003,004,005,006,007,008,009,010,011,012,013,014,015}   (15)
  B = {016,017,018,019,020,021}                                        (6)
  C = {}                                                                (0)

Batch 05 di chuyển UC-016,017,018 từ B → A (SCR-008/SCR-009/VIEW-004 tự author đủ representation).

Sau Batch 05:
  A = {001,002,003,004,005,006,007,008,009,010,011,012,013,014,015,016,017,018}   (18)
  B = {019,020,021}                                                                (3)
  C = {}                                                                           (0)
```

```text
Partition validation (mechanical):
  |A| = 18, |B| = 3, |C| = 0.  18 + 3 + 0 = 21.  Đúng.
  A ∩ B: {001..018} ∩ {019,020,021} = ∅.  Đúng.
  A ∩ C: {001..018} ∩ {} = ∅.  Đúng (trivial).
  B ∩ C: {019,020,021} ∩ {} = ∅.  Đúng (trivial).
  A ∪ B ∪ C = {001..021} — liệt kê tuần tự xác nhận KHÔNG thiếu UC nào: 001..018 (A, 18 liên
    tiếp) 019(B) 020(B) 021(B) — 21 UC, mỗi UC xuất hiện ĐÚNG MỘT LẦN.

21-UC substantive completion progress: 18/21 (A only) — ĐÃ independently verified (v1.2
  bookkeeping reconciliation, 2026-08-14 — final bounded Review A v1.1 CLEAN (hai finding
  CLOSED) + final Independent Review B v1.1 verdict READY_FOR_NEXT_PHASE2_BATCH, 0/0/0). Lifecycle
  VẪN CANDIDATE (verdict review ≠ lifecycle promotion). Historical (TRƯỚC Batch 05's own review
  hoàn tất): last independently verified 15/21 (UC-001..015, Batch 01+02+03+04 baseline).
```

Surface progress (17-surface set, `SCR-001`–`SCR-011`/`VIEW-001`–`VIEW-006`, `phase-2-dod.md` §3
criterion 3a): trước Batch 05 = 10/17 (Batch 01+02+03+04). Batch 05 thêm `SCR-008`, `SCR-009`,
`VIEW-004` (+3) → 13/17, ĐÃ independently verified (v1.2 bookkeeping reconciliation). Remaining:
`SCR-010`, `SCR-011`, `VIEW-005`, `VIEW-006` (4/17).

## 3. Element-level traceability map

**Ghi chú:** SCR-008 trace RIÊNG BIỆT theo năm khía cạnh yêu cầu (required-context gate, Fill
selection control, causation trace bảy mắt xích, Decision explainability group, exit to SCR-009).
SCR-009 trace RIÊNG BIỆT theo sáu khía cạnh yêu cầu (required-context gate, cursor selection
control, ReplayState(C) reconstructed panel, recorded-state-at-cursor panel, No-conflict outcome,
correction-visible-after-cursor outcome + exit to VIEW-004). VIEW-004 trace RIÊNG BIỆT theo bốn
khía cạnh yêu cầu (original-fact panel, invalidation+replacement panel với `supersedes_fact_ref`
link, correction-pattern scope note, exit back to SCR-008/SCR-009) — KHÔNG một hàng gộp nào cho
UC-016..UC-018.

| Prototype element (file:selector) | UX Blueprint / Domain ID | UC | PR | Authoritative source section |
|---|---|---|---|---|
| `index.html` `#shell`/`#context-bar` (bounded subset, reused convention) | WS-001 | UC-016, UC-017, UC-018 | PR-002 | `ux-blueprint.md` §5 "WS-001" table (same authority as Batch 01-04, re-derived independently in this batch's own files) |
| `index.html` `[data-nav="NAV-001"]`/`[NAV-002]`/`[NAV-003]`/`[NAV-004]` (real links to Batch 01/02/03/04) | NAV-001, NAV-002, NAV-003, NAV-004 | UC-001, UC-002 (precondition), UC-004, UC-006, UC-011 | PR-003, PR-015, PR-017, PR-001, PR-016, PR-008, PR-018, PR-020, PR-021, PR-022, PR-023, PR-006, PR-007, PR-024 | `ux-blueprint.md` §5a NAV-001/002/003/004; genuine navigation to already-authored Batch 01-04 screens, NOT a new representation |
| `index.html` `[data-nav="NAV-005"]` (Review, active), `[data-target="screen-review"]` | NAV-005 | UC-016, UC-017, UC-018 | PR-028, PR-029, PR-011, PR-030 | `ux-blueprint.md` §5a "NAV-005 — Review": Destination SCR-008/SCR-009/VIEW-004; "Khả dụng từ global nav bar tại mọi stage" |
| `index.html` `[data-nav="NAV-006"]` → `#screen-deferred` | NAV-006 (destination existence only) | see NAV-006's own §5a traceability | — | `ux-blueprint.md` §5a; §3 UX-P-5 (read-only inspection navigation always available) |
| `app.js` `state.reviewEvidence.fillContributionExists = false` / `renderScr008()` required-context branch | NAV-005 "Required context" ("một Fill/Position contribution ... phải tồn tại. KHÔNG evidence review nào bị bịa đặt khi thiếu") — labelled "STATE-002" per NAV-005's own text ("destination hiển thị STATE-002 (empty)"), **distinct from STATE-002's own narrower canonical catalogue row** (`ux-blueprint.md` §11: v0.5 explicitly narrows STATE-002 to SCR-004/SCR-005/SCR-007/SCR-011, explicitly excluding SCR-008/SCR-009 as "unfilled-form/không-genuinely-empty") — same "cited at NAV level, distinct from catalogue applicability" convention already established for STATE-004's citation at NAV-002/003/004 in earlier batches | UC-016 (alternate/failure) | PR-028 | `ux-blueprint.md` §5a NAV-005 "Available navigation behavior"; §11 STATE-002 row + its rationale note |
| `index.html` `[data-fill-select="FILL-RV-A-001"]`/`[FILL-RV-B-001"]` / `app.js` `state.scr008Selection` | SCR-008 "Available user actions" — "chọn một Fill để trace" (UC-016 Main flow bước 1) | UC-016 | PR-028 | `ux-blueprint.md` §7.5 SCR-008 "Available user actions"; `use-case-workflow.md` UC-016 Main flow bước 1 |
| `app.js` `LINEAGE_FILLS` / `renderScr008Trace()` `.evidence-group-downstream` chain-list (Fill→ExecutionResult→Order→Execution Intent→RiskEvaluation→Trade Intent→Decision, đúng bảy mắt xích, KHÔNG thiếu KHÔNG thừa) | SCR-008 "Information displayed" — causation trace ngược | UC-016 | PR-028, PR-004, PR-005 | `ux-blueprint.md` §7.5 SCR-008 "Information displayed"; `use-case-workflow.md` UC-016 Main flow bước 2 |
| `app.js` `renderScr008Trace()` `.evidence-group-upstream` Decision explainability block (outcome badge, Decision identity, Strategy Instance, Strategy Definition Version, Configuration, recorded input snapshot, recorded evaluation evidence — resolved TRỰC TIẾP từ `LINEAGE_FILLS[...].decision`, KHÔNG suy diễn/tính lại) | SCR-008 "Information displayed" — Decision explainability evidence, TÁCH BIỆT khỏi downstream lineage | UC-016 | PR-004, PR-005 | `ux-blueprint.md` §7.5 SCR-008 "Information displayed"; `use-case-workflow.md` UC-016 Main flow bước 3 |
| `index.html` `#btn-scr008-to-scr009` (v1.1, đóng `P2-B05-A-MIN-01` — renamed "Compare this trace's cursor..." → "Open Historical State Comparison (SCR-009)" + explicit disclosure "the historical comparison target (Replay Cursor) is selected independently on SCR-009," since `LINEAGE_FILLS` carries no mapped Replay Cursor and no cursor is actually carried forward) | SCR-008 "Exit points" — SCR-009 | UC-016 | PR-028, PR-029 | `ux-blueprint.md` §7.5 SCR-008 "Exit points" |
| `app.js` `state.reviewEvidence.replayCursorRunExists = false` / `renderScr009()` required-context branch | NAV-005 "Required context" ("một Replay Cursor đã chạy tại SCR-002 ... phải tồn tại") — same STATE-002-at-NAV-level convention as SCR-008's row above | UC-017 (alternate/failure) | PR-029 | `ux-blueprint.md` §5a NAV-005 "Available navigation behavior"; §11 STATE-002 row |
| `index.html` `[data-cursor-select="C-200"]`/`["C-100"]` / `app.js` `state.scr009Selection` | SCR-009 "Required context"/entry — cursor chosen from those already run at SCR-002 | UC-017 | PR-029 | `ux-blueprint.md` §7.5 SCR-009 "Entry points"/"Required context"; `use-case-workflow.md` UC-017 Main flow bước 1 |
| `app.js` `REPLAY_CURSORS` / `renderScr009Comparison()` "ReplayState(C) — reconstructed now" panel | SCR-009 "Information displayed" — ReplayState(C) hiện tại | UC-017 | PR-029 | `use-case-workflow.md` UC-017 Main flow bước 1; `replay-event.md` §1/§2 `ReplayStateProjection` (`decision_lineage` fold TẠI `replay_cursor`) |
| `app.js` `renderScr009Comparison()` "State recorded / originally displayed at cursor" panel (structurally identical object to the reconstructed panel above) | SCR-009 "Information displayed" — so sánh với state đã từng hiển thị/ghi nhận tại đúng cursor đó | UC-017 | PR-029 | `use-case-workflow.md` UC-017 Main flow bước 2; `replay-event.md` §2 "No-look-ahead xuyên suốt" (deterministic fold guarantees identity, not coincidence) |
| `app.js` `renderScr009Comparison()` `!c.hasCorrectionAfterCursor` branch ("No conflict" panel, `authority-label-recomputation`) | SCR-009 "Primary states" — "No conflict"; comparison result non-authoritative | UC-017 | PR-029 | `ux-blueprint.md` §7.5 SCR-009 "Primary states"/"Authority labels"; `use-case-workflow.md` UC-017 Main flow bước 3 |
| `app.js` `renderScr009Comparison()` `c.hasCorrectionAfterCursor` branch, first panel ("Correction visible after historical cursor" — historical panel above left unchanged, correction recorded_time explicitly compared against the cursor's own recorded_time) | SCR-009 "Empty/blocked" — correction visible sau historical cursor | UC-017 (alternate/failure) | PR-029 | `ux-blueprint.md` §7.5 SCR-009 "Empty/blocked states"; `use-case-workflow.md` UC-017 "Alternate/failure §8 'correction visible after historical cursor'" |
| `app.js` `renderScr009Comparison()` `c.hasCorrectionAfterCursor` branch, second panel — "Later-correction comparison" (v1.1, MỚI, đóng `P2-B05-A-MAJ-01`: `orig`/`inv`/`repl` rows resolved directly from `MOCK_DECISION_CORRECTION`, plus an explicit `orig.outcome + " → " + repl.outcome` comparison-result row) + `#btn-scr009-to-view004` | UC-017 "explicit difference kèm theo fact correction liên quan" (Main flow bước 3) + hand-off to VIEW-004 using the same identity | UC-017, UC-018 (hand-off) | PR-029, PR-011, PR-030 | `use-case-workflow.md` UC-017 Main flow bước 3 ("hiển thị khác biệt tường minh kèm fact correction liên quan"); `ux-blueprint.md` §7.5 SCR-009 "Exit points" (VIEW-004 nếu correction phát hiện) |
| `app.js` `MOCK_DECISION_CORRECTION` shared by reference between `renderScr009Comparison()`'s "Later-correction comparison" panel and `renderView004()` (SAME `PD-100`/`PD-101`/invalidation object identity, no re-fixture) | SCR-009→VIEW-004 cross-screen coherence — hand-off uses the SAME correction identity | UC-017, UC-018 | PR-029, PR-011, PR-030 | Task requirement: "SCR-009's correction-detection hand-off to VIEW-004 must use the SAME correction identity" |
| `app.js` `renderView004()` `.evidence-group-upstream` "Original fact" panel (`PD-100`, explicitly labelled "still resolvable, append-only") | VIEW-004 "Information displayed" — fact gốc vẫn resolvable | UC-018 | PR-011, PR-030 | `ux-blueprint.md` §7.5 VIEW-004 "Information displayed"; `use-case-workflow.md` UC-018 Main flow bước 2; `decision.md` (`DecisionRecorded` immutable, append-only) |
| `app.js` `renderView004()` `.evidence-group-downstream` "Invalidation + replacement fact" panel (`DecisionFactInvalidated`: `invalidated_fact_ref`/`invalidation_reason`; replacement `DecisionRecorded` `PD-101`: `supersedes_fact_ref` explicit hint row) | VIEW-004 "Information displayed" — fact replacement + liên kết tường minh `supersedes_fact_ref` | UC-018 | PR-011, PR-030 | `ux-blueprint.md` §7.5 VIEW-004 "Information displayed"; `use-case-workflow.md` UC-018 Main flow bước 2; `decision.md` §6 `DecisionFactInvalidated` schema (`invalidated_fact_ref`/`invalidation_reason`), §11/DecisionRecorded `supersedes_fact_ref` (direct-predecessor-fact-targeting) |
| `app.js` `renderView004()` unconditional dual-panel render (no `if`/empty branch — both panels always present in the returned HTML) | VIEW-004 "System-owned actions" — hiển thị CẢ HAI trạng thái, hành vi bắt buộc, không nhánh lỗi; "Empty/blocked: KHÔNG áp dụng" | UC-018 | PR-011, PR-030 | `ux-blueprint.md` §7.5 VIEW-004 "System-owned actions"/"Empty/blocked states" |
| `app.js` `renderView004()` trailing scope-note `.hint` (RiskEvaluation/Fill share the direct pattern; ExecutionResult's is materially different; PaperExecutionObservation/Position have none) | Task boundary — "do not invent a generic universal correction schema... use exact vocabulary of whichever entity is chosen" | UC-018 | PR-011, PR-030 | `risk.md` (direct `supersedes_fact_ref` + `RiskEvaluationFactInvalidated`); `fill.md` (same pattern, §25); `execution-result.md` §2/§5/§11 (`ExecutionResultComputation` CORRECTION three-way linkage; PaperExecutionObservation has no correction lineage of its own); `position.md` §1 (derived projection, no correction lineage) |
| `app.js` `#btn-view004-to-scr009`/`#btn-view004-to-scr008` | VIEW-004 "Exit points" — trở lại SCR-008/SCR-009 | UC-018 | PR-011, PR-030 | `ux-blueprint.md` §7.5 VIEW-004 "Exit points" |
| `index.html` `.label-row` `.mode-label`("Review")/`.authority-label-authoritative`/`.authority-label-recomputation`/`.prototype-datum-label` | SCR-008/SCR-009/VIEW-004 "Authority labels" | UC-016, UC-017, UC-018 | PR-028, PR-029, PR-011, PR-030 | `ux-blueprint.md` §7.5 SCR-008/SCR-009/VIEW-004 "Authority labels" |
| Absence of any "apply correction"/"accept replacement"/"save reconstructed state"/create/overwrite/invalidate/promote action anywhere in Batch 05 | NAV-005 "Read-only inspection behavior" — KHÔNG authoritative action nào tồn tại tại Review (INV-1) | UC-016, UC-017, UC-018 | PR-028, PR-029, PR-011, PR-030 | `ux-blueprint.md` §5a NAV-005 "Read-only inspection behavior"; §7.5 SCR-008/SCR-009/VIEW-004 (all read-only per §7.5 header) |
| Absence of any Position correction fact anywhere in Batch 05 | Task boundary — "do not invent Position correction facts" | UC-018 | PR-011, PR-030 | `position.md` §1 (`kind: read_model`, derived projection, explicitly NOT an authoritative fact — cannot have correction lineage) |
| `#screen-deferred` panel (Improve) | (Batch-scoping placeholder — a prototype-batch concept, not a UX Blueprint state) | — | — | N/A — same convention as Batch 01-04, intentionally represents ONLY "not included in this batch" |
| `#qa-panel`/`#qa-body` (QA state switcher) | (Prototype tooling — explicitly NOT part of authoritative UX) | — | — | N/A — exists only to let the Scenario-family-D required-context-missing states be inspected without a real event log/Replay engine |

## 4. Reconciliation statement (I-12 Verification)

```text
Mọi hàng ở §3 trên trace được, đối chiếu trực tiếp, về đúng một section cụ thể trong
  docs/product/ux-blueprint.md (Package 0.3-C, Consolidated Stable), docs/product/use-case-
  workflow.md (Package 0.3-B, Consolidated Stable), hoặc Domain Contract tương ứng
  (decision.md/trade-intent.md/risk.md/execution-intent.md/order.md/execution-result.md/
  fill.md/position.md/replay-event.md) — đây LÀ "rebuild hoặc đối chiếu hoàn toàn từ authoritative
  source" per I-12's Verification (Chapter 2 §I-12).
KHÔNG một NAV-XXX/SCR-XXX/VIEW-XXX/STATE-XXX/UC-XXX/PR-XXX ID nào xuất hiện trong Batch 05 mà
  KHÔNG có hàng tương ứng ở §3.
KHÔNG một UC/PR/domain concept mới nào originate trong Batch 05 — verify trực tiếp: prototype/
  phase-2/batch-05/*.{html,css,js} KHÔNG tạo entity/event/state-machine mới (mọi identity là
  hardcoded illustrative string, KHÔNG API/database/event contract), KHÔNG tạo "generic universal
  correction schema" (VIEW-004 dùng ĐÚNG decision.md §6/§11 vocabulary, KHÔNG một field tên chung
  chung áp cho mọi entity), KHÔNG tạo Position correction fact, KHÔNG implement snapshot-storage
  mechanism, KHÔNG authoritative action nào (grep clean: KHÔNG create/overwrite/correct/
  invalidate/promote function trên bất kỳ MOCK_* fixture).
§2's cumulative UC ledger LÀ completion accounting (Chapter 12/phase-2-dod.md §3 purpose) —
  TÁCH BIỆT khỏi §3's element-to-authority traceability map (I-12 purpose). Mọi UC cited tại §3
  đều resolve nhất quán vào ĐÚNG MỘT hạng mục tại §2's partition — verify trực tiếp, KHÔNG UC nào
  tại §3 rơi ngoài {A, B} đã định nghĩa tại §2 (C rỗng sau Batch 05).
```

## 5. Four non-negotiable Review invariants — verified explicitly

```text
INV-1 (read-only): verified — grep across index.html/app.js confirms no create/overwrite/correct/
  invalidate/promote action, no "apply correction"/"accept replacement"/"save reconstructed state"
  control anywhere. Every render function only reads MOCK_ACCOUNT_CONTEXT/MOCK_STRATEGY_CONTEXT/
  LINEAGE_FILLS/MOCK_DECISION_CORRECTION/REPLAY_CURSORS and writes only to `state.*` (prototype-
  local UI selection state — which Fill/cursor/tab is displayed, and the two Family-D QA toggles),
  never mutating a MOCK_* fixture's own fields.

INV-2 (downstream lineage vs. Decision explainability distinct): verified — SCR-008's
  `.evidence-group-downstream` (causation trace) and `.evidence-group-upstream` (Decision
  explainability) are two visually-distinct blocks (separate border-left color/class,
  `evidence-group-label` heading each), never merged into one list; the Decision explainability
  block resolves directly from `LINEAGE_FILLS[...].decision`'s recorded fields (outcome, Strategy
  Instance, Strategy Definition Version, recorded input snapshot, recorded evaluation evidence) —
  no recomputation/re-derivation function touches it.

INV-3 (historical comparison never repaints history): verified — `renderScr009Comparison()`'s
  "ReplayState(C) reconstructed" and "state recorded at that cursor" panels render from the SAME
  `c.decision` object (no separate "current view" vs. "historical view" divergence is possible by
  construction). When a correction exists after the cursor (`C-100`), the historical panel's
  values are NOT altered — the correction is disclosed in a THIRD and FOURTH, separate panel
  ("Correction visible after historical cursor" intro, then v1.1's "Later-correction comparison"
  detail panel, closes `P2-B05-A-MAJ-01`), matching replay-event.md §2's no-look-ahead guarantee
  (`fact.recorded_time ≤ C.recorded_time` for every ReplayState(C) component) and the task's
  explicit INV-3 wording ("show the historical state as it was, show the later correction
  separately, never silently replace historical values"). The v1.1 detail panel now ALSO shows
  the explicit old→new difference (`orig.outcome → repl.outcome`) UC-017 requires, still without
  touching the two historical panels above (verified: neither panel's HTML-building code changed
  in v1.1 — only new panels were appended). The comparison-result row carries the
  `authority-label-recomputation` (non-authoritative) label; the original/invalidation/replacement
  rows above it carry `authority-label-authoritative`, distinct and explicit per row-group.

INV-4 (correction inspection preserves original + correction lineage): verified —
  `renderView004()` unconditionally renders BOTH the original-fact panel (`PD-100`, labelled
  "still resolvable, append-only") AND the invalidation+replacement panel (`DecisionFactInvalidated`
  + replacement `DecisionRecorded PD-101`) in every code path — there is no `if` branch that shows
  only one. The `supersedes_fact_ref` binding (`PD-101` → `PD-100`) is rendered as its own explicit
  hint row, not implied. No branch anywhere shows only the "corrected value" with its origin
  hidden.
```
