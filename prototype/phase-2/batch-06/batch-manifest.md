---
id: phase-2-batch-06-manifest
title: "Phase 2 Prototype — Batch 06 — Batch Manifest"
version: "1.0"
status: Candidate
owner: Product Owner
created_at: "2026-08-14"
---

# Phase 2 Prototype — Batch 06 — Batch Manifest

**Vai trò của tài liệu này:** batch-level evidence record cho Batch 06, đúng `phase-2-rules.md`
`P2-PROTOTYPE-001` (review theo batch/milestone, KHÔNG per-screen governance cycle riêng). Đây LÀ
transaction AUTHORING đầu tiên cho Batch 06 — the final planned Phase-2 Product Prototype
milestone — Review A/Independent Review B **CHƯA thực hiện**. Lifecycle `CANDIDATE`, chưa
self-approved, chưa review.

## 1. Batch identity

```text
Batch:              Phase 2 — Batch 06 (Improve / new strategy version / instance registration /
                     version comparison / old-version evidence access)
Phase:               Phase 2 — Product Prototype (AUTHORIZED TO BEGIN)
Authoritative DoD:   docs/phase-dod/phase-2-dod.md v0.3, status Approved,
                     post-acceptance blob de399900a93c7ec7ee64577093513de1643ebb33
Status:              CANDIDATE — authoring transaction, Review A + Independent Review B CHƯA thực
                     hiện. KHÔNG READY_FOR_NEXT_PHASE2_BATCH verdict tại transaction này.
Created:             2026-08-14
Starting HEAD:       30c405bbb95010a8130d102a0c03a9aadfa1e29f (verified via git rev-parse HEAD
                     trước khi tạo file, đúng G-VERIFY-001)
Depends on (real,
  read-only link,
  KHÔNG modified):    prototype/phase-2/batch-01/ .. batch-05/ — mỗi batch CANDIDATE, review
                     COMPLETE, verdict READY_FOR_NEXT_PHASE2_BATCH, untouched by this
                     transaction. Verified: git status --porcelain=v1 -uall trên toàn bộ
                     prototype/phase-2/batch-01/ .. batch-05/ returned empty (zero diff).
```

## 2. Semantic scope

```text
Target semantic slice: Improve — new Strategy Definition Version creation + Strategy Instance
  registration/binding + version comparison + old-version evidence access (NAV-006 + SCR-010 +
  VIEW-006 + SCR-011 + VIEW-005) — resolved directly from ux-blueprint.md §5a NAV-006, §7.6
  (SCR-010/VIEW-006/SCR-011/VIEW-005 detailed spec), §11 STATE-002/025/026 rows,
  use-case-workflow.md UC-019–UC-021 detailed block, docs/domain/strategy.md.
Batch-selection rule application: NAV-006 + SCR-010 + VIEW-006 + SCR-011 + VIEW-005 authored as
  ONE coherent Improve milestone (P2-PROTOTYPE-001, batch/milestone review, KHÔNG per-screen
  cycle riêng) — the final planned Phase-2 Product Prototype milestone, closing the 17-surface/
  21-UC candidate set. Explicit instruction not to expand into Phase-3 implementation, Gate-3
  work, or LIVE.
Six non-negotiable Improve invariants verified (traceability.md §5): INV-1 new version = new
  immutable identity, INV-2 no invented Strategy Definition schema, INV-3 VIEW-006 registration
  ≠ VIEW-001 selection/pinning, INV-4 comparison keeps evidence families separate, INV-5
  old-version evidence stays accessible, INV-6 registration vs inspection actions distinct.
```

## 3. Included IDs

```text
SCR:    SCR-010 (Strategy Definition Version Creation), SCR-011 (Strategy Version Comparison)
VIEW:   VIEW-006 (Strategy Instance Creation/Binding), VIEW-005 (Old-Version Evidence Access)
NAV:    NAV-006 (Improve — fully represented, incl. required-context-is-action-specific
        behavior per ux-blueprint.md §5a); NAV-001/002/003/004/005 (real links to Batch 01-05,
        not re-authored)
FLOW:   (no new FLOW-XXX authored — UC-019/020/021 sit within FLOW-001's existing scope per
        use-case-workflow.md)
STATE:  STATE-002 (empty, canonical row explicitly lists SCR-011 — no disclaimer needed),
        STATE-025 (old-version evidence complete, VIEW-005), STATE-026 (old-version evidence
        partially unavailable, VIEW-005)
```

## 4. Covered UC IDs — substantive accounting (A/B/C taxonomy, kế thừa từ `../batch-01/traceability.md` §0, recomputed đầy đủ tại `traceability.md` §2)

```text
Batch-06-authored substantive (A, +3 mới, CANDIDATE — CHƯA independently verified): UC-019
  (SCR-010), UC-020 (SCR-011), UC-021 (VIEW-005). VIEW-006 represents the UC-019→UC-002 handoff
  (registration, distinct from selection/pinning) — UC-002 is NOT double-counted (already A since
  Batch 01, for the same reason, untouched here).

Candidate cumulative A (21 of 21): UC-001..UC-018 (Batch 01-05, ĐÃ independently verified) +
  UC-019, UC-020, UC-021 (Batch 06, CANDIDATE — CHƯA independently verified, Review A +
  Independent Review B CHƯA thực hiện).

Candidate cumulative B (0 of 21, giảm từ 3 vì UC-019/020/021 promote lên A):
  (rỗng).

Candidate cumulative C (0 of 21, không đổi):
  (rỗng).

Partition validation: |A|=21, |B|=0, |C|=0, tổng=21. A∩B=A∩C=B∩C=∅ (verify mechanically, xem
  traceability.md §2). Union = {UC-001..UC-021}, mỗi UC đúng một lần — KHÔNG thiếu, KHÔNG dư.

21-UC substantive completion progress: 21/21 (A only) — CANDIDATE (Batch 06's own Review A +
  Independent Review B CHƯA thực hiện tại transaction này). Last independently verified: 18/21
  (UC-001..018, Batch 01-05 baseline, mỗi batch đã qua đầy đủ Review A + Independent Review B).

IMPORTANT: candidate 21/21 UC + candidate 17/17 surface (§8 dưới) tại thời điểm authoring KHÔNG
  establish Phase-2 substantive completion (§16 dưới) — completion đòi hỏi Batch 06's own Review
  A + Independent Review B COMPLETE trước, VÀ tách biệt hoàn toàn khỏi Quality Gate/Gate 3/
  P2-RETRO-001/Phase 3/LIVE authorization.
```

## 5. Covered PR IDs (Batch 06 mới)

```text
PR-031 (SCR-010, UC-019; VIEW-006 handoff)
PR-001, PR-016 (VIEW-006, UC-002 downstream reference)
PR-031, PR-032 (SCR-011, UC-020)
PR-032 (VIEW-005, UC-021)
```

## 6. Prototype artifact identities

```text
prototype/phase-2/batch-06/index.html         blob 3f081111c260e64618689490363bfdb6255bdc23 (CURRENT — v1.0)
prototype/phase-2/batch-06/app.js              blob b37967b62457595f7ac6cfb5fba692b6d255e9f2 (CURRENT — v1.0)
prototype/phase-2/batch-06/styles.css          blob 5114548728ad678c16f862e79b09b71798d8df69 (CURRENT — v1.0)
prototype/phase-2/batch-06/traceability.md     blob d8f1e360f2f726061049af0accfab7ecdb4971ff (CURRENT — v1.0)
prototype/phase-2/batch-06/batch-manifest.md   (this file — CURRENT, v1.0)
prototype/phase-2/batch-06/README.md           (CURRENT, v1.0)
```

## 7. Authority sources consumed (reference only, none modified)

```text
docs/product/ux-blueprint.md          (Package 0.3-C, Consolidated Stable) §5a NAV-006, §7.6
                                       SCR-010/VIEW-006/SCR-011/VIEW-005, §11 STATE-002/025/026
docs/product/use-case-workflow.md     (Package 0.3-B, Consolidated Stable) UC-019, UC-020,
                                       UC-021 detailed block
docs/domain/strategy.md               §1 StrategyDefinitionVersionRegistered (seven-field
                                       schema, immutable, invalidate-only-no-replacement), §5/§6
                                       StrategyInstanceRegistered (four independent evidence
                                       axes + Account + instrument_selection_ref), §5
                                       state_machine (UNSEEN/ACTIVE/PAUSED/RETIRED)
docs/domain/decision.md               vocabulary reference only (Backtest/PAPER Decision
                                       evidence-source, not redefined)
docs/domain/risk.md                   vocabulary reference only (RiskEvaluation evidence-source)
docs/domain/trade-intent.md           vocabulary reference only (Trade Intent, PAPER family)
docs/domain/execution-intent.md       vocabulary reference only (Execution Intent, PAPER family)
docs/domain/order.md                  vocabulary reference only (Order, PAPER family)
docs/domain/execution-result.md       vocabulary reference only (ExecutionResult, PAPER family)
docs/domain/fill.md                   vocabulary reference only (Fill, PAPER family)
docs/domain/position.md               vocabulary reference only (Position, PAPER family)
docs/product/product-requirement.md   (Package 0.3-A, Consolidated Stable) PR-001/016/031/032
ADR-013                               referenced only as strategy.md itself references it (four
                                       independent evidence axes architecture) — not re-inspected
                                       independently beyond strategy.md's own citations
```

## 8. Known deferred surfaces / non-substantive UC (not a gap — Phase-2 candidate set now closed)

```text
0 of 17 surfaces not yet substantively covered — Batch 06 completes the full 17-surface set
  (SCR-001–SCR-011, VIEW-001–VIEW-006) as a CANDIDATE (NOT independently verified) contribution.
  This is the final planned Phase-2 Product Prototype milestone under P2-PROTOTYPE-001.

0 of 21 UC NOT substantively covered (candidate) — traceability.md §2 — B=0, C=0 (candidate).
  Batch 06's own +3 (UC-019/020/021) remain CHƯA independently verified until this batch's own
  Review A + Independent Review B complete.
```

## 9. I-11 — Secrets & Custody Isolation — bounded Phase-2 Access-control audit

```text
Authoritative Verification (Chapter 2 §I-11, NOT redefined here): Access-control audit.
Bounded Phase-2 interpretation (phase-2-dod.md §2/§4, same as Batch 01-05):
  (1) No credential-use capability established:      CONFIRMED — no code path in app.js/
                                                       index.html uses, stores, or transmits a
                                                       credential.
  (2) No credential input surface required
      or introduced:                                  CONFIRMED — no login/auth UI, no session
                                                       token, no permission gate, no credential-
                                                       shaped <input> element anywhere (only
                                                       thesis/supported_scope illustrative text
                                                       fields, verified directly).
  (3) No signing key / custody / backend integration
      exists:                                          CONFIRMED — static files only, no
                                                       fetch/XHR/WebSocket/axios/.ajax in app.js.
  (4) No real secret/credential used or required:      CONFIRMED — VERSION_FIXTURES/
                                                       INSTANCE_FIXTURES/EVIDENCE are hardcoded
                                                       illustrative values.
Result: AUDIT PASS.
```

## 10. I-11 — secret-pattern scan (supporting evidence only, NOT a substitute for the audit)

```text
Command: grep -niE "api[_-]?key|secret|password|private[_-]?key|token|credential|apikey|
  auth[_-]?header|bearer" prototype/phase-2/batch-06/*.html *.css *.js
Result: one match, app.js:6 — inside the file-header comment explicitly disclaiming
  credentials/signing/custody/network calls. No actual credential-like value found. Same clean
  pattern as Batch 01-05.
```

## 11. I-12 — Single Source of Truth — traceability/reconciliation result

```text
Full element-by-element mapping: prototype/phase-2/batch-06/traceability.md §3 (separately per
  SCR-010/VIEW-006/SCR-011/VIEW-005, no merged rows).
Result: PASS — every prototype element traces to an existing NAV/SCR/VIEW/STATE + UC + PR + exact
  ux-blueprint.md/use-case-workflow.md/strategy.md section. Zero new UC/PR/domain concept
  originated (verified directly, traceability.md §4) — no Strategy Definition aggregate beyond
  family identity, no mutable "latest" object, no version graph, no approval workflow, no
  optimizer/DSL, no auto-ranking/scoring, no unified Backtest/PAPER outcome, no unified
  old-version evidence object.
```

## 12. Trigger B/C/D/E boundary confirmation (phase-2-dod.md §2/§4 — re-confirmed, not re-resolved)

```text
No authoritative executable implementation:  CONFIRMED — static HTML/CSS/vanilla JS, mock data
                                              only, no module-registry.yaml entry, no Strategy
                                              management service/engine implemented (every
                                              version/instance/evidence value is a hardcoded or
                                              counter-generated deterministic fixture).
No registered runtime module/tier:            CONFIRMED.
Representation vs. authority (Trigger D):     Prototype REPRESENTS authoritative-class Strategy
                                              registration (authority=authoritative Strategy
                                              registration labels on SCR-010/VIEW-006; mixed
                                              non-PAPER simulated / authoritative PAPER labels on
                                              SCR-011/VIEW-005) but every actual value remains
                                              mock/static/counter-generated — no authoritative
                                              financial computation, no custody/security
                                              implementation, no production operational path.
No real backend:                              CONFIRMED — grep for fetch/XHR/WebSocket/axios/
                                              .ajax across app.js/index.html returned no match.
No production/operational deployment:         CONFIRMED — files exist only under prototype/,
                                              no deployment config/pipeline touches them.
No published API/database/event contract,
  no new Domain Contract, no migration:        CONFIRMED — no schema file, no contract
                                              definition authored; no new Strategy Instance
                                              schema, no new registration API/event/schema.
Result: boundary preserved. Trigger B/C/D/E conclusions from phase-2-dod.md §2 remain valid for
  this batch — no re-resolution triggered.
```

## 13. Six Improve invariants (batch-specific critical boundary)

```text
Full verification: prototype/phase-2/batch-06/traceability.md §5.
Summary: INV-1 (new immutable identity) — buildNewVersion() append-only, old fixture never
  mutated. INV-2 (no invented schema) — exactly strategy.md §1's seven fields, no DSL/compiler/
  version graph/approval workflow. INV-3 (not VIEW-001) — no pin flag anywhere, exact required
  handoff wording, real link only. INV-4 (families separate) — two independent render functions,
  zero score/rank/normalize function. INV-5 (old-version accessible) — identity always first,
  independent per-family resolution, incomplete marking never hides available evidence. INV-6
  (registration vs inspection) — exactly two creation functions, all SCR-011/VIEW-005 render
  functions read-only.
```

## 14. LIVE boundary

```text
Live representation: static "Unauthorized" badge (STATE-027 convention, same as Batch 01-05)
  in the global context bar, always visible. No action/link/button anywhere leads toward a Live
  path. OQ-002 not touched, not resolved.
```

## 15. Domain/architecture boundary

```text
No new domain entity, no new state machine, no architecture change, no backend contract choice,
  no API/event/database schema, no reinterpretation of Strategy Definition Version/Strategy
  Instance semantics — verified directly: docs/domain/, docs/architecture/, docs/constitution/
  untouched by this transaction. No Strategy management service/engine invented — every SCR-010/
  VIEW-006/SCR-011/VIEW-005 value is a hardcoded or counter-generated deterministic fixture
  (buildNewVersion()/registerInstance() helpers), never computed from real business logic. No
  Strategy Definition aggregate beyond family identity (strategy_definition_id remains a plain
  scope field, never a registered subject of its own), no mutable "latest strategy" object, no
  version graph, no approval workflow, no optimizer, no strategy DSL/compiler, no auto-ranking/
  scoring, no unified Backtest/PAPER outcome, no unified old-version evidence object, no new
  retention/archive semantics, no evidence SLA, no PaperSession, no new Strategy Instance schema,
  no new registration API/event/schema.
```

## 16. Unresolved gaps

```text
None within this batch's scope. This batch completes the candidate 17-surface/21-UC set — but
  Phase-2 substantive completion (phase-2-dod.md §3) remains NOT ESTABLISHED: Batch 06 still
  requires its own governed Review A + Independent Review B before its +4 surfaces/+3 UC count as
  independently verified, and Phase-2 completion additionally requires Quality Gate/Gate 3
  evidence entirely separate from per-batch review, none of which this transaction performs or
  claims.
```

## 17. Batch lifecycle / review state

```text
Status:            CANDIDATE — v1.0 authoring transaction. Review A + Independent Review B CHƯA
                    thực hiện. KHÔNG self-approved, KHÔNG READY_FOR_NEXT_PHASE2_BATCH verdict.

Review history (chronological, KHÔNG rewrite):
  (none yet — this is the initial authoring transaction)

CURRENT TRUTH (v1.0, authoring transaction, 2026-08-14):
  Review verdict:                 NONE — chưa qua Review A.
  Candidate Batch-06 contribution: +4/17 surfaces (SCR-010, VIEW-006, SCR-011, VIEW-005); +3/21
                                 candidate substantive UC (UC-019, UC-020, UC-021) — CHƯA
                                 independently verified.
  Candidate cumulative (Batch
    01+02+03+04+05+06):            17/17 surfaces; 21/21 candidate substantive UC.
  Last independently verified
    (Batch 01-05 baseline):        13/17 surfaces; 18/21 UC.
  Remaining:                      0/17 surfaces; 0/21 UC not substantive (candidate set closed;
                                 independent verification of Batch 06's own contribution still
                                 pending).
  Batch lifecycle:                CANDIDATE.
  Next governed step:              Review A on this v1.0 artifact (not authored by this
                                 transaction — per instruction, this executor does not author
                                 the next-task prompt).
```
