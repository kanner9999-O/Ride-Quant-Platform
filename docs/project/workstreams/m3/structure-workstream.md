# M3 Workstream — Structure

Project orchestration packet only. NOT governance authority, NOT an ADR, NOT a
Product Owner decision. Subordinate to Constitution / Approved ADR / Domain
Contract authority at all times — this packet bounds scope, it does not grant it.

## Identity

```text
workstream_id:   m3-structure
parent_milestone: M3 — Context Projection / context-aggregator
planning_head:   197100785fb786278816b5b694dc9d380d9c1b8b
owner/executor:  AI Technical Architect (Claude or ChatGPT) — bounded WP Executor,
                 per Lean Ride Operating Model v1.1 §3
state:           IN_PROGRESS (MAJ-04/05/06 independently actionable; MAJ-03
                 PENDING_ARCHITECTURE_DISPOSITION — see §Existing findings /
                 debt and §Completion contract; terminal state cannot be
                 WORKSTREAM_COMPLETE while MAJ-03 is unresolved)
```

## Objective

Bring all four Structure Event Contract Draft candidates
(`break-of-structure-detected`, `change-of-character-detected`,
`structure-fact-invalidated`, `structure-recomputed`) to one coherent,
self-contained integration candidate that resolves every currently-open Review A
finding this workstream has authority to resolve, ready for a single batched
Review A request — not a sequence of per-finding micro-transactions.

## Authority closure set

Fresh-read in full (not only the sections a prior finding named) before any
semantic conclusion:

- `docs/domain/structure.md` v0.4 — the complete Domain Contract, not only §5/§6a/§10.
- `docs/adr/ADR-048.md` (Approved, v0.3) — canonical `causal_state_dependency_declaration` grammar.
- `docs/adr/ADR-049.md` (Draft, v0.1, **PARKED — not authoritative until Product Owner decides**) — read for context on STRUCT-EC-A-MAJ-03 only; its conclusions may not be applied as if approved.
- `docs/adr/ADR-039.md` (Approved) — Event Contract self-containment model.
- `docs/adr/ADR-047.md` (Approved) — `backward_only` compatibility commitment, all four Structure `contract_id`s.
- `docs/constitution/08-event-model.md` §8.2.3, §8.3.4, §8.5/§8.5.1/§8.5.2/§8.5.3 — causal closure, merge constraints, canonical Replay Cursor.
- `docs/project/context-upstream-state-dependency-derivation-001.md` v0.5 §2.3–§2.6 — classification evidence.
- `docs/project/event-contract-causal-dependency-representation-001.md` v0.5 §H — flagged stale `STRUCTURE_FACT_INVALIDATED` mapping (do not treat as current).
- The four current files under `docs/architecture/event-contracts/{break-of-structure-detected,change-of-character-detected,structure-fact-invalidated,structure-recomputed}/v1.0.yaml`.
- `docs/architecture/context-map.yaml` — confirms `context-aggregator` as sole registered consumer.

Do not fresh-read unrelated history (Candle's own correction rounds, Regime, Feature) merely for completeness — out of this workstream's scope.

## Semantic Closure stage

Before any mutation, derive this matrix (minimum rows below; add rows if full-section reading surfaces more):

| semantic topic | authoritative source | resolved? | unresolved decision? | implementation consequence |
|---|---|---|---|---|
| BOS/CHoCH winner-selection rule (8-criteria total order) | `structure.md` §6a | content resolved, representation not yet inlined | no | inline the deterministic rule itself (not just its outcome) into both BOS/CHoCH Event Contracts |
| `structure-recomputed.input_cursor_ref` shape | Chapter 8 §8.5.1 | resolved | no | use canonical `type: replay_cursor`, full §8.5.1 field set + §8.5.2 relational invariants; note the still-missing Structure-scoped Input Contract as an operational prerequisite, not a representation gap |
| `structure-recomputed` cascade membership/completion algorithm | `structure.md` §10 | content resolved, representation not yet inlined | no | inline cascade root / dependency-forward descendant membership / direct-vs-chained relation / completion / causation-set completeness / exactly-one-recompute-per-cascade |
| `StructureFactInvalidated` multi-cause representation | `structure.md` §5 + §10; `ADR-049` (Draft, not approved, self-proposed ADR_REQUIRED/R2 — not yet Review-A-validated) | **PENDING_ARCHITECTURE_DISPOSITION** | yes — which disposition route applies (ADR-049 approval, alignment/correction under existing authority, or another governed route) is itself undecided | do not mutate `structure-fact-invalidated/v1.0.yaml` for this finding; do not assume any specific route; resolve independently under Chapter 0 §4b / G-ADR-001/004 / Review A triage |

## Existing findings / debt

Carry forward, do not treat prior reviewer conclusions as ground truth — re-derive from the closure set above:

- `STRUCT-EC-A-MAJ-01`/`02` — `CLOSED — REVIEW A VALIDATED`. No further action.
- `STRUCT-EC-A-MAJ-03` — REOPENED; analyzed (not decided) by `ADR-049` (Draft, v0.1, self-proposed ADR_REQUIRED/R2, not yet Review-A-validated, not approved). Status: **PENDING_ARCHITECTURE_DISPOSITION** — this workstream does not pre-decide whether the eventual resolution is ADR-049 approval, an alignment/correction resolvable under existing authority without a new ADR, or another governed route; that determination happens independently under Chapter 0 §4b / G-ADR-001/004 / Review A triage. **BLOCKED for this workstream** — do not implement a representation change in `structure-fact-invalidated/v1.0.yaml` ahead of that determination; CORR-001's own prior "exactly-one-direct-cause" fix is itself acknowledged incorrect and must not be reinstated or defended.
- `STRUCT-EC-A-MAJ-04` — disposition reversed from CORR-001's own STOP: Chapter 8 §8.5.1 already mechanically determines the cursor shape; actionable now.
- `STRUCT-EC-A-MAJ-05` (new) — BOS/CHoCH still externalize §6a's 8-criteria total order; actionable now.
- `STRUCT-EC-A-MAJ-06` (new) — `structure-recomputed` still externalizes §10's cascade algorithm; actionable now.

## Implementation scope

After semantic closure, this lane MAY:

- Correct `break-of-structure-detected/v1.0.yaml` and `change-of-character-detected/v1.0.yaml` to inline the §6a winner-selection rule (MAJ-05).
- Correct `structure-recomputed/v1.0.yaml`'s `input_cursor_ref` to the canonical `type: replay_cursor` shape (MAJ-04) and inline the §10 cascade algorithm (MAJ-06).
- Update each corrected file's own provenance/header annotations and `causal_state_dependency_declaration` only as mechanically required by the above (no new role/selector invented beyond what ADR-048's existing grammar already supports).
- Leave `structure-fact-invalidated/v1.0.yaml` untouched pending STRUCT-EC-A-MAJ-03's PENDING_ARCHITECTURE_DISPOSITION resolution — not pre-assigned to ADR-049 approval specifically.

## Explicit forbidden scope

- No governance amendment (Constitution, Global Execution Rules, Phase-3 rules, Lean Ride Operating Model).
- No mutation of `regime`, `feature_future_dependency_authority`, or any other workstream's files.
- No Product Owner decision fabrication.
- No spontaneous ADR authoring — if a genuine new architecture gap surfaces beyond what `ADR-049` already scopes, escalate (see below), do not author an ADR here.
- No mutation of `ADR-049.md` or any Approved ADR.
- No publication of any Structure Event Contract (`status` stays `Draft`) unless separately authorized by current authority.

## Escalation contract

Terminate with exactly `ARCHITECTURE_ESCALATION` only when a genuinely unresolved semantic/authority decision is found that existing authority cannot decide — report:

- exact question;
- exact conflicting/missing authorities;
- affected artifacts/modules;
- reversible local option(s), if any;
- why existing authority cannot decide it.

Do not author an ADR as part of the escalation report.

## Completion contract

This lane MAY execute every independently resolvable finding (MAJ-04/05/06) now,
inside this same lane — that work is never blocked by MAJ-03.

Report exactly one of:

- `WORKSTREAM_COMPLETE` — ONLY once the full four-contract Structure integration
  candidate is coherent, i.e. MAJ-03 is ALSO resolved (under whatever disposition
  route Chapter 0 §4b / Review A triage determines) in addition to MAJ-04/05/06.
  **Never** report this while MAJ-03 remains `PENDING_ARCHITECTURE_DISPOSITION` —
  even if MAJ-04/05/06 are fully resolved.
- `BLOCKED_BY_EXTERNAL_DEPENDENCY` — the correct terminal state when MAJ-04/05/06
  are resolved but MAJ-03 is the only remaining open item. This is not a failure
  state for the lane's own executed work; it accurately reports that one required
  finding for the four-contract candidate still awaits an architecture disposition
  this lane has no authority to resolve or predict.
- `ARCHITECTURE_ESCALATION` — if a genuinely new unresolved semantic/authority
  question (beyond MAJ-03, already tracked above) is found.

A single batched Structure Review A request is made only once the full
four-contract integration candidate (MAJ-03 included) is coherent — never
requested for a partial 3-of-4 subset by default — unless an existing
higher-authority rule explicitly requires a narrower review boundary for a
specific finding or artifact (in which case that narrower boundary controls, per
Lean Ride Operating Model v1.1 §1's own "Batched Review A (default, not an
override)" clause).
