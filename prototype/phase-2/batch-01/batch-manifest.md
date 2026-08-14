---
id: phase-2-batch-01-manifest
title: "Phase 2 Prototype — Batch 01 — Batch Manifest"
version: "1.3"
status: Candidate
owner: Product Owner
created_at: "2026-08-13"
---

# Phase 2 Prototype — Batch 01 — Batch Manifest

**Vai trò của tài liệu này:** batch-level evidence record cho Batch 01, đúng `phase-2-rules.md` `P2-PROTOTYPE-001` (review theo batch/milestone, KHÔNG per-screen governance cycle riêng). Batch 01 đã qua đầy đủ Review A + Independent Review B trên v1.2 — verdict `READY_FOR_NEXT_PHASE2_BATCH` — **NHƯNG lifecycle VẪN `CANDIDATE`** (`READY_FOR_NEXT_PHASE2_BATCH` LÀ completed-review verdict, KHÔNG PHẢI lifecycle status; Product Owner CHƯA issue một lifecycle-promotion transaction riêng).

**v1.3 — deterministic bookkeeping reconciliation (2026-08-14), vai trò: `Phase 2 Prototype Review-State Bookkeeping Reconciliation Executor`, đúng `G-TXN-003`.** KHÔNG PHẢI lifecycle transition, KHÔNG PHẢI prototype semantic correction — reconcile review-state/current-progress bookkeeping tại §1/§16 để khớp với governed review history ĐÃ hoàn tất (bounded Review A re-review trên v1.2: CLEAN; Independent Review B trên v1.2: `P2-B01-B-MAJ-01` CLOSED, `P2-B01-A-MIN-01` CLOSED, Blocker/Major/Minor mới = 0/0/0, verdict `READY_FOR_NEXT_PHASE2_BATCH`) — history này trước đây CHƯA được ghi nhận vào tài liệu này, khiến §1/§16 stale ("chờ Review A + Independent Review B," "last independently verified 2/17, 2/21"). KHÔNG sửa nội dung semantic/artifact evidence (§2–§15 giữ nguyên byte-for-byte ngoại trừ mục này); KHÔNG sửa `index.html`/`app.js`/`styles.css` (blob KHÔNG đổi); KHÔNG sửa `traceability.md` (KHÔNG chứa current-state review-progress claim nào mâu thuẫn, verify trực tiếp — giữ byte-identical). `README.md` sửa tối thiểu (câu "not yet reviewed or approved" mâu thuẫn trực tiếp với review COMPLETE — sửa thành "reviewed, verdict READY_FOR_NEXT_PHASE2_BATCH, nhưng lifecycle vẫn candidate, chưa approved"). Lifecycle VẪN `CANDIDATE` — `READY_FOR_NEXT_PHASE2_BATCH` là verdict review, KHÔNG phải Approved/Accepted/Complete.

**v1.1 — bounded correction (2026-08-13), đóng `P2-B01-A-MAJ-01`/`P2-B01-A-MIN-01`.** (1) `P2-B01-A-MAJ-01`: authority/workflow label trong `app.js` conflate authority CLASS (vd "authoritative (recorded fact, read-only)") với authority STATUS của chính prototype datum (mock fixture) — sửa thành hai badge tách biệt: "Authority class: [...]" (giữ nguyên UX affordance) + "Prototype datum: Illustrative / non-authoritative" (badge mới, `.prototype-datum-label`) tại cả ba vị trí (SCR-001 normal-content, VIEW-001 list, VIEW-002 tất cả ba outcome). (2) `P2-B01-A-MIN-01`: 21-UC coverage accounting mơ hồ giữa "substantive" và "referenced qua shell/nav/handoff" — thêm taxonomy A (Substantive)/B (Partial-referenced)/C (Deferred) tường minh tại `traceability.md` §0/§1, đầy đủ 21 UC classify; §4 dưới đây cập nhật đồng bộ. Progress 3/21 KHÔNG đổi (vẫn CHỈ đếm hạng mục A) — chỉ accounting logic được làm rõ, KHÔNG inflate. **KHÔNG đổi:** batch semantic scope, SCR-001/VIEW-001/VIEW-002, NAV/FLOW/STATE scope, static HTML/CSS/vanilla-JS medium, mock/static data policy, QA tooling, I-11 audit result, I-12 source authority, Trigger B/C/D/E boundary, LIVE Unauthorized, 3/17 surface progress.

**v1.2 — bounded correction (2026-08-13), Independent Review B trên v1.1: `P2-B01-A-MAJ-01` CLOSED, `P2-B01-A-MIN-01` REOPENED, `P2-B01-B-MAJ-01` (mới) — đóng CẢ HAI tại transaction này.** `P2-B01-B-MAJ-01`: `#range-select` (SCR-001's authorized "chọn thời điểm/khoảng thời gian" action) tồn tại trong `index.html` NHƯNG `app.js` KHÔNG đọc/listen nó — đổi range KHÔNG làm evidence hiển thị thay đổi, "Candle (latest)" label sai bất kể range nào chọn. Sửa: thêm `state.selectedRange` + `MOCK_RANGE_EVIDENCE` (ba fixture tách biệt: Latest/Last 4h/Last 1d, mỗi cái khác nhau tường minh ở candle/swing/structure/regime/feature) + change listener trên `#range-select` + `renderScr001()` nay bind theo `state.selectedRange` + candle label động (`range.candleLabel`) thay "Candle (latest)" cố định + QA reset khôi phục default range + missing-evidence message nay trích dẫn đúng range đã chọn. `P2-B01-A-MIN-01` REOPENED: `batch-manifest.md` §8/§15 VẪN dùng wording "18 of 21 UC deferred" — collapse sai B+C thành một "deferred" bucket, mâu thuẫn taxonomy §4 đã establish. Sửa: §8/§15 nay tách tường minh B (7, partial/referenced)/C (11, deferred) — KHÔNG dùng "deferred" cho tổng 18 nữa. §16 (Batch lifecycle) cập nhật đồng bộ để phản ánh chính xác review history đầy đủ VÀ phân biệt tường minh "candidate contribution" (3/17, 3/21 — CHƯA verified) khỏi "last independently verified" (2/17, 2/21 — theo Independent Review B's v1.1 finding). **KHÔNG đổi:** batch semantic scope, SCR-001/VIEW-001/VIEW-002 substantive spec, VIEW-001/VIEW-002 behavior, commit-gate semantics, authority-label correction từ v1.1, medium, mock/static data only, QA tooling, I-11/I-12 boundary, Trigger B/C/D/E boundary, LIVE Unauthorized. KHÔNG surface/screen mới nào thêm.

## 1. Batch identity

```text
Batch:              Phase 2 — Batch 01 (Lifecycle entry + Research foundation)
Phase:               Phase 2 — Product Prototype (AUTHORIZED TO BEGIN)
Authoritative DoD:   docs/phase-dod/phase-2-dod.md v0.3, status Approved,
                     post-acceptance blob de399900a93c7ec7ee64577093513de1643ebb33
Status:              CANDIDATE — Review A + Independent Review B COMPLETE trên v1.2, verdict
                     READY_FOR_NEXT_PHASE2_BATCH (batch-level, P2-PROTOTYPE-001). Lifecycle VẪN
                     CANDIDATE — verdict review KHÔNG PHẢI lifecycle promotion.
Created:             2026-08-13
```

## 2. Semantic scope

```text
Target semantic slice: Lifecycle entry (WS-001 shell) + Research foundation (SCR-001) + the
  immediately required commit-gate binding/verification interactions (VIEW-001, VIEW-002) —
  established directly from ux-blueprint.md §4 "Thứ tự entry của Research" and §8 FLOW-001's
  initial segment (WS-001 → NAV-001 → SCR-001 → commit gate → VIEW-001 → VIEW-002).
Batch-selection rule application: only elements that (1) are part of the authoritative
  lifecycle-entry/Research slice, (2) the slice cannot be navigated/understood coherently
  without, (3) are an explicit prerequisite/binding view/handoff/gate/state for that slice, or
  (4) are reusable global shell/navigation required by every screen in this batch, were
  included. Replay/Backtest/Paper/Review/Improve substantive screens were explicitly excluded —
  see traceability.md §3.
```

## 3. Included IDs

```text
SCR:    SCR-001 (Market Analysis Workspace)
VIEW:   VIEW-001 (Strategy Instance Selector), VIEW-002 (Research Verification Result)
NAV:    NAV-001 (Research — fully represented); NAV-002..NAV-006 (destination-existence/
        read-only-navigation-affordance only, per UX-P-5 — substantive screens NOT authored)
FLOW:   FLOW-001 (initial segment only, up to and including the commit gate); FLOW-002
        (Strategy Instance selection/pin)
STATE:  STATE-001 (loading), STATE-003 (invalid Instrument/Venue), STATE-004 (missing Strategy
        Instance), STATE-005 (missing historical evidence), STATE-022 (verification PASSED),
        STATE-023 (verification FAILED), STATE-024 (verification INDETERMINATE), STATE-027
        (Live unauthorized, global static label)
WS:     WS-001 (Ride Workspace Shell — bounded subset per ux-blueprint.md §5 table: Account
        context, Instrument/Venue context, Strategy Instance context, Live Unauthorized label)
```

## 4. Covered UC IDs — substantive accounting (đóng `P2-B01-A-MIN-01`, xem `traceability.md` §0/§1 cho taxonomy đầy đủ)

```text
Taxonomy (traceability.md §0): A = Substantively covered (counts toward 21-UC numerator);
  B = Partial/referenced (appears via shell/nav/handoff, does NOT count); C = Deferred/not yet
  represented.

A — Substantively covered (3 of 21, = the 21-UC completion progress number):
  UC-001  Research / Market Analysis observation — SCR-001
  UC-002  Strategy Instance selection/pin — VIEW-001, FLOW-002
  UC-003  Research Verification — VIEW-002

B — Partial/referenced (7 of 21, do NOT count toward the numerator):
  UC-004, UC-006 (Replay/Backtest nav-button + handoff-affordance existence only)
  UC-011, UC-015 (WS-001 shell context / STATE-027 global label source-spec justification only)
  UC-019, UC-020, UC-021 (NAV-006 nav-button existence only)

C — Deferred/not yet represented (11 of 21):
  UC-005, UC-007, UC-008, UC-009, UC-010, UC-012, UC-013, UC-014, UC-016, UC-017, UC-018

21-UC substantive completion progress: 3/21 (A only — B is explicitly excluded from the
  numerator, per the taxonomy above).
```

## 5. Covered PR IDs (5 of 34)

```text
PR-001, PR-003, PR-015, PR-016, PR-017
```

## 6. Prototype artifact identities

```text
prototype/phase-2/batch-01/index.html         blob e519162bd3407dc176f265e1799cadc883246769 (unchanged since v1.0)
prototype/phase-2/batch-01/styles.css          blob 89c34c0d7f500950987dfb4cdd440f14cc7661ab (unchanged since v1.1)
prototype/phase-2/batch-01/app.js              blob 5e1a7237d034afffb28a268c1b828b2dc86ccf32 (v1.2, was 1aadeb01387beb6fb3379535cf82c57d41af0281)
prototype/phase-2/batch-01/traceability.md     blob 764936474af8ff6b5cb8f1672f2855bac5c47759 (v1.2, was 46466e2e99937311ef3e7f7124eccc9388c5aefe)
```

## 7. Authority sources consumed (reference only, none modified)

```text
docs/product/ux-blueprint.md       (Package 0.3-C, Consolidated Stable) §2-§11, §17
docs/product/use-case-workflow.md  (Package 0.3-B, Consolidated Stable) §3, §4, §7 (via
                                    ux-blueprint.md's inherited mapping — not re-read for
                                    semantics not already surfaced in ux-blueprint.md)
docs/product/product-requirement.md (Package 0.3-A, Consolidated Stable) PR-001/003/015/016/017
docs/domain/instrument.md, venue.md, candle.md, swing.md, structure.md, regime.md, feature.md,
  context.md, strategy.md, decision.md (vocabulary reference only — no schema/field authored)
```

## 8. Known deferred surfaces / non-substantive UC (not a gap — explicit batch boundary, đóng REOPENED `P2-B01-A-MIN-01`)

```text
14 of 17 SCR/VIEW surfaces deferred: SCR-002..SCR-011, VIEW-003..VIEW-006. Represented in this
  batch ONLY as a read-only nav-bar affordance leading to a labelled "Deferred — not included in
  Batch 01" placeholder (#screen-deferred) — no substantive screen/view content authored for any
  of them, per batch-selection rule.

18 of 21 UC NOT substantively covered (traceability.md §0/§1 taxonomy — NOT collapsed to a single
  "deferred" bucket):
  B — Partial/referenced (7): UC-004, UC-006, UC-011, UC-015, UC-019, UC-020, UC-021 — appear only
    via shell/nav-button-existence/handoff-affordance elements, traced to the exact source-spec
    fragment each element actually represents (traceability.md §1).
  C — Deferred/not yet represented (11): UC-005, UC-007, UC-008, UC-009, UC-010, UC-012, UC-013,
    UC-014, UC-016, UC-017, UC-018 — zero reference anywhere in Batch 01.
  Neither B nor C counts toward the 3/21 substantive-completion numerator (§4 above) — that
  distinction is exactly what this correction makes explicit.
```

## 9. I-11 — Secrets & Custody Isolation — bounded Phase-2 Access-control audit

```text
Authoritative Verification (Chapter 2 §I-11, NOT redefined here): Access-control audit.
Bounded Phase-2 interpretation (phase-2-dod.md §2/§4):
  (1) No credential-use capability established:      CONFIRMED — no code path in app.js/index.html
                                                       uses, stores, or transmits a credential.
  (2) No credential access-control surface required
      or introduced:                                  CONFIRMED — no login/auth UI, no session
                                                       token, no permission gate exists.
  (3) No backend/custody/signing integration exists:   CONFIRMED — static files only, no network
                                                       call, no fetch/XHR/WebSocket in app.js.
  (4) No real secret/credential used or required:      CONFIRMED — MOCK_INSTRUMENTS/
                                                       MOCK_STRATEGY_INSTANCES are hardcoded
                                                       illustrative values, not real Account/
                                                       exchange data.
Result: AUDIT PASS.
```

## 10. I-11 — secret-pattern scan (supporting evidence only, NOT a substitute for the audit)

```text
Command: grep -niE "api[_-]?key|secret|password|private[_-]?key|token|credential|apikey|
  auth[_-]?header|bearer" prototype/phase-2/batch-01/*.html *.css *.js
Result: one match, app.js:5 — inside a comment explicitly disclaiming credentials ("no real
  credentials, no authoritative financial data"). No actual credential-like value found.
```

## 11. I-12 — Single Source of Truth — traceability/reconciliation result

```text
Full element-by-element mapping: prototype/phase-2/batch-01/traceability.md.
Result: PASS — every prototype element traces to an existing SCR/VIEW/NAV/FLOW/STATE +
  UC + PR + exact ux-blueprint.md section. Zero new UC/PR/domain concept originated in this
  batch (verified directly, traceability.md §2).
```

## 12. Trigger B/C/D/E boundary confirmation (phase-2-dod.md §2/§4)

```text
No authoritative executable implementation:  CONFIRMED — static HTML/CSS/vanilla JS, mock data
                                              only, not wired to any production build/deploy
                                              path, no module-registry.yaml entry created.
No registered runtime module:                 CONFIRMED.
No authoritative financial data:              CONFIRMED — all Candle/Swing/Structure/Regime/
                                              Feature/Market Context values are hardcoded and
                                              labelled "illustrative."
No real backend:                              CONFIRMED — no fetch/XHR/WebSocket call anywhere
                                              in app.js (verified directly, grep clean).
No production/operational deployment:         CONFIRMED — files exist only under prototype/,
                                              no deployment config/pipeline touches them.
No published API/database/event contract:     CONFIRMED — no schema file, no contract
                                              definition authored.
No migration:                                 CONFIRMED — not applicable, no migration artifact.
Result: boundary preserved. Trigger B/C/D/E conclusions from phase-2-dod.md §2 (NOT APPLICABLE,
  conditional) remain valid for this batch — no re-resolution triggered.
```

## 13. LIVE boundary

```text
Live representation:  static "Unauthorized" badge (STATE-027) in the global context bar, always
                       visible, no action/link/button anywhere leads toward a Live path.
OQ-002:                NOT resolved, NOT touched by this batch.
Result: LIVE remains NOT AUTHORIZED.
```

## 14. Domain/architecture boundary

```text
No new domain entity, no new state machine, no architecture change, no backend contract choice,
  no API/event/database schema, no reinterpretation of Decision/Risk/Execution semantics —
  verified directly: docs/domain/, docs/architecture/, docs/constitution/ untouched by this
  transaction (see CHANGELOG.md forbidden-scope verification).
No missing-authoritative-decision gap was encountered that required stopping an interaction —
  all included elements (SCR-001, VIEW-001, VIEW-002) had complete authoritative UX Blueprint
  specification.
```

## 15. Unresolved gaps

```text
None within this batch's scope. 14/17 surfaces not yet authored and 18/21 UC not substantively
  covered (7 partial/referenced + 11 deferred, §8) remain for later batches — this is the
  expected, planned state of a first milestone, not an unresolved defect.
```

## 16. Batch lifecycle / review state

```text
Status:            CANDIDATE — v1.2 artifact candidate, review COMPLETE, NOT self-approved
                    (READY_FOR_NEXT_PHASE2_BATCH verdict ≠ lifecycle approval).

Review history (chronological, KHÔNG rewrite):
  Review A (v1.0):              P2-B01-A-MAJ-01, P2-B01-A-MIN-01 found, REVISION_REQUIRED.
  v1.1 bounded correction:       both CLOSED.
  Bounded Review A re-review
    (v1.1):                      CLEAN.
  Independent Review B (v1.1):   P2-B01-A-MAJ-01 CLOSED; P2-B01-A-MIN-01 REOPENED; new
                                 P2-B01-B-MAJ-01 found; verdict REVISION_REQUIRED.
  v1.2 bounded correction:       đóng P2-B01-B-MAJ-01 (range-select binding) VÀ REOPENED
                                 P2-B01-A-MIN-01 (§8 taxonomy wording).
  Bounded Review A re-review
    (v1.2, FINAL):                CLEAN.
  Independent Review B (v1.2,
    FINAL):                       P2-B01-B-MAJ-01 CLOSED; P2-B01-A-MIN-01 CLOSED; new
                                 Blocker/Major/Minor = 0/0/0; verdict
                                 READY_FOR_NEXT_PHASE2_BATCH.

CURRENT TRUTH (v1.3 bookkeeping reconciliation, 2026-08-14 — đóng gap "chờ bounded re-review"
  trước đây, đúng G-TXN-003):
  Review verdict:                 READY_FOR_NEXT_PHASE2_BATCH (final, v1.2 artifact candidate —
                                 KHÔNG PHẢI Approved/Accepted/Complete lifecycle transition).
  Verified contribution:          3/17 surfaces (SCR-001, VIEW-001, VIEW-002); 3/21 substantive
                                 UC (UC-001, UC-002, UC-003).
  Batch lifecycle:                CANDIDATE (unchanged — Product Owner CHƯA issue lifecycle-
                                 promotion transaction riêng cho Batch 01).
  Further Batch-01 correction/
    re-review pending:            NONE — review COMPLETE trên v1.2, KHÔNG bounded re-review nào
                                 chờ xử lý.

Next step:          Không applicable cho riêng Batch 01 — Phase 2 đã tiếp tục sang Batch 02/03
                     dựa trên contribution đã verified này (P2-PROTOTYPE-001).
```
