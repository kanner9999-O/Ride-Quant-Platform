# M3 Workstream — Regime

Project orchestration packet only. NOT governance authority, NOT an ADR, NOT a
Product Owner decision. Subordinate to Constitution / Approved ADR / Domain
Contract authority at all times — this packet bounds scope, it does not grant it.

## Identity

```text
workstream_id:   m3-regime
parent_milestone: M3 — Context Projection / context-aggregator
planning_head:   197100785fb786278816b5b694dc9d380d9c1b8b
owner/executor:  AI Technical Architect (Claude or ChatGPT) — bounded WP Executor,
                 per Lean Ride Operating Model v1.1 §3
state:           NOT_STARTED
```

## Objective

Author Draft v1.0 Event Contract candidates for `regime-classified` and
`regime-fact-invalidated` against Approved `ADR-048`'s canonical grammar,
self-contained per `ADR-039`, as one coherent deliverable — not a sequence of
per-contract micro-transactions. This is the first authoring pass; it mirrors the
precedent already established for Candle and Structure, applied fresh to Regime's
own Domain Contract rather than copied from either precedent's specific content.

## Authority closure set

Fresh-read in full before any semantic conclusion:

- `docs/domain/regime.md` v0.2 — the complete Domain Contract (four concepts: Logical Regime Subject, `RegimeClassified`, `RegimeFactInvalidated`, `RegimeCurrentView`), not only the sections a Candle/Structure precedent happened to use.
- `docs/adr/ADR-048.md` (Approved, v0.3) — canonical `causal_state_dependency_declaration` grammar; apply fresh, do not assume Structure's or Candle's specific role shapes transfer unexamined.
- `docs/adr/ADR-039.md` (Approved) — Event Contract self-containment model.
- `docs/adr/ADR-047.md` (Approved) — confirm `backward_only` compatibility commitment for `regime-classified`/`regime-fact-invalidated` specifically (per-`contract_id` table, not inherited from the Candle/Structure rows).
- `docs/constitution/08-event-model.md` §8.2.3, §8.3.4, §8.5 — same canonical envelope/causal-closure/replay-cursor authority Structure/Candle already apply, not redefined here.
- `docs/project/context-upstream-state-dependency-derivation-001.md` v0.5 §2.7/§2.8 — existing classification evidence for `REGIME_CLASSIFIED`/`REGIME_FACT_INVALIDATED`'s causation categories.
- `docs/architecture/stream-registry.yaml` (Approved) — confirm the `raw-regime-engine-regime` stream identity.
- `docs/architecture/module-registry.yaml` — confirm `raw-regime-engine`'s registered producer identity.
- `docs/architecture/context-map.yaml` — confirm registered consumers of both Regime `contract_id`s (prior derivation found 2 modules each; re-verify fresh, do not inherit the count unchecked).

Do not fresh-read unrelated history (Candle's own correction rounds, Structure's own findings) merely for completeness — Regime's Domain Contract and its own classification evidence are the controlling sources; Candle/Structure are precedent for GRAMMAR APPLICATION STYLE only, never for Regime's own semantic content.

## Semantic Closure stage

Before any mutation, derive this matrix (minimum rows below; add rows if full-section reading surfaces more):

| semantic topic | authoritative source | resolved? | unresolved decision? | implementation consequence |
|---|---|---|---|---|
| `RegimeClassified` causation-ref shape (candle evidence set) | `regime.md` §8a (canonical Candle evidence normalization, closes `IRB-B2-MAJ-01`) | resolved | no | `causal_state_dependency_declaration` role(s) must reflect the set semantics (not an array-order dependency) |
| `RegimeFactInvalidated` envelope binding | `regime.md` §2/§4 (closes `IRB-B2-MAJ-02` — `subject_ref`/`effective_time` inherited, never independently declared) | resolved | no | invalidation role's `apply_time_requirement` must state identity-only resolution, consistent with Structure/Candle precedent's own wording style |
| Current View ambiguity before first fact | `regime.md` §5/§11 (closes `RA-B2-MIN-01`/`IRB-B2-MIN-03`) | resolved | no | no causal-dependency consequence — `RegimeCurrentView` is a non-authoritative projection, out of this workstream's Event Contract scope unless the task later requires it |
| self-containment of any producer-side ranking/tie-break logic | `regime.md` (full document) | to be determined during fresh-read | unknown until read | if any winner-selection-style rule exists analogous to Structure's §6a, inline the rule itself, not only its outcome (per the STRUCT-EC-A-MAJ-05 lesson — do not repeat that omission here) |

## Existing findings / debt

None — this is a first authoring pass, no prior Review A exists for these two `contract_id`s. Do not import Structure's or Candle's specific finding IDs as if they applied here; derive fresh.

## Implementation scope

After semantic closure, this lane MAY:

- Author `docs/architecture/event-contracts/regime-classified/v1.0.yaml` and `docs/architecture/event-contracts/regime-fact-invalidated/v1.0.yaml` as new `status: Draft` files, `contract_version: v1.0`, `reviewers: []`, `approved_by: null`, `approved_at: null`.
- Declare `causal_state_dependency_declaration` per ADR-048's canonical grammar, using the derivation v0.5 §2.7/§2.8 classification evidence.
- Declare `compatibility_commitment: backward_only` per Approved ADR-047's Regime rows.

## Explicit forbidden scope

- No governance amendment (Constitution, Global Execution Rules, Phase-3 rules, Lean Ride Operating Model).
- No mutation of `structure`, `feature_future_dependency_authority`, or any other workstream's files.
- No mutation of `regime.md` itself (Domain Contract) — apply it, do not redefine it.
- No Product Owner decision fabrication.
- No spontaneous ADR authoring.
- No publication (`status` stays `Draft`) unless separately authorized by current authority.

## Escalation contract

Terminate with exactly `ARCHITECTURE_ESCALATION` only when a genuinely unresolved semantic/authority decision is found that existing authority cannot decide — report:

- exact question;
- exact conflicting/missing authorities;
- affected artifacts/modules;
- reversible local option(s), if any;
- why existing authority cannot decide it.

Do not author an ADR as part of the escalation report.

## Completion contract

Report exactly one of: `WORKSTREAM_COMPLETE`, `ARCHITECTURE_ESCALATION`, or
`BLOCKED_BY_EXTERNAL_DEPENDENCY`. No Review A request is made until both Draft
candidates form one coherent integration candidate.
