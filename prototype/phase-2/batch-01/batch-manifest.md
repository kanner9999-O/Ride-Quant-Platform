---
id: phase-2-batch-01-manifest
title: "Phase 2 Prototype — Batch 01 — Batch Manifest"
version: "1.1"
status: Candidate
owner: Product Owner
created_at: "2026-08-13"
---

# Phase 2 Prototype — Batch 01 — Batch Manifest

**Vai trò của tài liệu này:** batch-level evidence record cho Batch 01, đúng `phase-2-rules.md` `P2-PROTOTYPE-001` (review theo batch/milestone, KHÔNG per-screen governance cycle riêng). Batch 01 LÀ candidate/in-review — **KHÔNG self-approved** (chờ Review A + Independent Review B theo batch, đúng `P2-PROTOTYPE-001`).

**v1.1 — bounded correction (2026-08-13), đóng `P2-B01-A-MAJ-01`/`P2-B01-A-MIN-01`.** (1) `P2-B01-A-MAJ-01`: authority/workflow label trong `app.js` conflate authority CLASS (vd "authoritative (recorded fact, read-only)") với authority STATUS của chính prototype datum (mock fixture) — sửa thành hai badge tách biệt: "Authority class: [...]" (giữ nguyên UX affordance) + "Prototype datum: Illustrative / non-authoritative" (badge mới, `.prototype-datum-label`) tại cả ba vị trí (SCR-001 normal-content, VIEW-001 list, VIEW-002 tất cả ba outcome). (2) `P2-B01-A-MIN-01`: 21-UC coverage accounting mơ hồ giữa "substantive" và "referenced qua shell/nav/handoff" — thêm taxonomy A (Substantive)/B (Partial-referenced)/C (Deferred) tường minh tại `traceability.md` §0/§1, đầy đủ 21 UC classify; §4 dưới đây cập nhật đồng bộ. Progress 3/21 KHÔNG đổi (vẫn CHỈ đếm hạng mục A) — chỉ accounting logic được làm rõ, KHÔNG inflate. **KHÔNG đổi:** batch semantic scope, SCR-001/VIEW-001/VIEW-002, NAV/FLOW/STATE scope, static HTML/CSS/vanilla-JS medium, mock/static data policy, QA tooling, I-11 audit result, I-12 source authority, Trigger B/C/D/E boundary, LIVE Unauthorized, 3/17 surface progress.

## 1. Batch identity

```text
Batch:              Phase 2 — Batch 01 (Lifecycle entry + Research foundation)
Phase:               Phase 2 — Product Prototype (AUTHORIZED TO BEGIN)
Authoritative DoD:   docs/phase-dod/phase-2-dod.md v0.3, status Approved,
                     post-acceptance blob de399900a93c7ec7ee64577093513de1643ebb33
Status:              CANDIDATE — chờ Review A + Independent Review B (batch-level,
                     P2-PROTOTYPE-001)
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
prototype/phase-2/batch-01/index.html         blob e519162bd3407dc176f265e1799cadc883246769 (unchanged, v1.0/v1.1)
prototype/phase-2/batch-01/styles.css          blob 89c34c0d7f500950987dfb4cdd440f14cc7661ab (v1.1, was cdd6dbb1b2364dc288616f083f7247b7bb0cb146)
prototype/phase-2/batch-01/app.js              blob 1aadeb01387beb6fb3379535cf82c57d41af0281 (v1.1, was cfae4327486c48c2eb9f20988d94441797fadfac)
prototype/phase-2/batch-01/traceability.md     blob 46466e2e99937311ef3e7f7124eccc9388c5aefe (v1.1, was 1f98aa71fc05b670bd40759f12d448f04ef5879c)
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

## 8. Known deferred surfaces (not a gap — explicit batch boundary)

```text
14 of 17 SCR/VIEW surfaces deferred: SCR-002..SCR-011, VIEW-003..VIEW-006.
18 of 21 UC deferred: UC-004..UC-021.
Represented in this batch ONLY as a read-only nav-bar affordance leading to a labelled
  "Deferred — not included in Batch 01" placeholder (#screen-deferred) — no substantive
  screen/view content authored for any of them, per batch-selection rule.
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
None within this batch's scope. 14/17 surfaces and 18/21 UC remain for later batches (§8) — this
  is the expected, planned state of a first milestone, not an unresolved defect.
```

## 16. Batch lifecycle / review state

```text
Status:            CANDIDATE — authored, NOT self-approved.
Review A:           NOT YET PERFORMED (batch-level, P2-PROTOTYPE-001).
Independent
  Review B:          NOT YET PERFORMED.
Next step:          Batch-level Review A + Independent Review B on this coherent milestone —
                     a separate governed transaction, per this transaction's own scope
                     (authoring only).
```
