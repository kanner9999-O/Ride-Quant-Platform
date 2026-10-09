# M3 Context Closure Derivation — 001

```
status: Draft (reasoning-heavy derivation artifact, not an authority artifact)
version: "0.2"
owner: Product Owner
generated_at: "2026-10-09"
role: M3 Context Closure Executor
```

Purpose: derive, from existing repository authority only, the actual remaining M3
("Context Projection / context-aggregator") completion boundary — per
`docs/project/milestone.md` §3's own explicit statement that this has not yet been
derived. This artifact does NOT amend `docs/project/milestone.md` — it is evidence for a
separate, later Review A / Product Owner decision that persists its conclusion into the
milestone register.

**v0.2 bounded correction (2026-10-09)** — fresh ChatGPT Review A on v0.1 returned
`REVISION_REQUIRED — 0 Blocker / 4 Major / 0 Minor`, Risk R2:
`CONTEXT-CLOSURE-A-MAJ-01` (the Context output stream identity/writer authority is a
genuine ADR-required Event Model decision — v0.1 wrongly treated it as a mechanical
"decide and mint" step and wrongly concluded `architecture escalation: NONE`),
`CONTEXT-CLOSURE-A-MAJ-02` (v0.1 claimed all twelve Published upstream artifacts carry
`causal_state_dependency_declaration`; Feature v1.0's pair do not, and ADR-048 is
non-retroactive — fail-closed for that pair as per-effect authority, not a defect),
`CONTEXT-CLOSURE-A-MAJ-03` (v0.1 wrongly described both future Context output Event
Contracts as classifying a uniform "seven causation_refs"; `context.md` §3/§4 defines two
different, variable-cardinality shapes), `CONTEXT-CLOSURE-A-MAJ-04` (v0.1's Quality-Gate
item recreated the false per-module approval-gate model `milestone.md` §3.1 already
removed). All four addressed below; not self-closed by the correction executor.

## 1. Derived M3 acceptance condition

M3 ("Context Projection / context-aggregator") is DONE when all of the following hold,
simultaneously, for `context_type: market_context` (`docs/domain/context.md` v0.4):

1. A governed decision (ADR) pins Context's own output logical stream identity and
   writer authority, and the resulting Stream Registry transition is Approved (§5 —
   genuine architecture escalation, not a mechanical step).
2. The Context-scoped Input Contract (`context-market-input/v1.0`) is Published as an
   immutable snapshot (Approved ADR-041 discipline).
3. Context's own output Event Contracts (`market-context-snapshot`,
   `market-context-fact-invalidated`) are authored and Published against (1)'s stream
   identity, each carrying an Approved-ADR-048-conformant
   `causal_state_dependency_declaration` — classifying each contract's OWN actual
   causation_refs role/category coverage (§3 — NOT a uniform seven-ref shape for both
   contracts; the two differ, per `context.md` §3/§4).
4. `context-aggregator`'s runtime binds the existing deterministic aggregation core
   (`python/context-aggregator/`, unaffected by this WP) to a real Chapter 8 §8.2 envelope
   — genuine `event_id`/`stream_ref`/`producer_ref`/`sequence`/`causation_refs` — and
   performs the four-stream frontier capture, causal-closure execution, and
   `computation_cursor` construction this Input Contract's own protocol specifies.
5. The invalidation/replacement lineage runtime behavior (`context.md` §4/§12, Case A/
   Case B, `COVERS_CONTEXT`) is implemented and tested against the Domain Contract's own
   worked examples.
6. `context-aggregator` has a resolved authoritative quality tier (`module-registry.yaml`,
   Chapter 13 §13.4 tier-resolution chain — currently absent, see §6) and the Chapter-13
   Quality Gate applicable to that tier has produced its PASS/evidence record. This is
   NOT a standalone per-module approval gate (`milestone.md` §3.1 already removed that
   model for M3) — it is ordinary Quality-Gate evidence feeding the single Phase-3
   Approval Gate, same as every other module.

This condition is **not invented** by this transaction: every element above is already
named, as an open item, by `context.md` §21 ("Ngoài phạm vi") or by
`python/context-aggregator/README.md`'s own "What this slice does not implement" list.
This derivation only assembles those already-named items into one ordered acceptance
condition and classifies each against current repository state (§4 below).

`MarketContextCurrentView` runtime (`context.md` §5/§13) is **not** included as a hard M3
acceptance item: nothing in `milestone.md`, `m3-execution-control-plane.yaml`, or
`context.md` itself states that a queryable current-view materialization (as opposed to
the append-only snapshot/invalidation record stream) is required for M3 to be DONE — only
that its *policy schema* (`current_view_selection_policy`) be defined, which it already is
(`context.md` §6). If Review A disagrees, this is the smallest item to re-scope, not a
reason to add new items elsewhere.

## 2. A — Already-complete prerequisites

- 10 current-target upstream Event Contract version-artifacts (Candle v1.0 ×2, Structure
  v1.0 ×4, Regime v1.0 ×2, Feature v1.1 ×2) are `status: Published`, each carrying an
  Approved-ADR-048-conformant `causal_state_dependency_declaration` (fresh-verified this
  transaction).
- Feature's two contract_ids additionally have a historical `v1.0` pair, also
  `status: Published`, co-existing (expected under ADR-039's versioning model — historical
  events keep citing whichever version was current when produced) but NOT carrying the
  declaration — they predate ADR-048's 2026-10-05 approval, which applies prospectively
  only (ADR-048, "Non-retroactivity and existing Published Event Contracts"). This is not
  a defect in either artifact; it is a permanent, by-design fail-closed carve-out for any
  causal-closure step that would need to classify a causation_ref carried by a v1.0-pinned
  Feature event (§3/§7 below).
- `docs/architecture/stream-registry.yaml` is `status: Approved`, `registry_version:
  v1.0`; its immutable `docs/architecture/stream-registry-versions/v1.0.yaml` snapshot
  exists; all four streams `context-market-input.yaml` includes are `status: active`.
- `docs/domain/context.md` v0.4 is PO-accepted as the governed basis for Context work
  (`CONTEXT-DOMAIN-V04-PO-ACCEPTANCE-001`); ADR-046 (Approved) supplies `computation_cursor`
  / temporal-supersession semantics on top of it.
- `docs/architecture/input-contracts/context-market-input.yaml`'s semantic body (merge
  policy, frontier policy, causal-closure policy, four-stream cut-capture protocol) is
  sound and requires no semantic change — only the readiness narrative needed correcting
  (§3 below, done in this same transaction).
- `python/context-aggregator/`'s deterministic aggregation core is implemented, tested
  (76/76 passing, fresh-run this transaction), and carries `REVIEW A VALIDATED — CLEAN`
  per `milestone.md` §4a. It correctly uses "eligible cursor-bounded ... candidate"
  terminology throughout, never "authoritative" (§5 below).
- The Chapter-7-vs-`context.md` authoritative/Projection terminology tension (see §5) is
  an already-adjudicated, Product-Owner-acknowledged **non-blocking carried-forward open
  gap** — not a new architecture question for this WP to raise.

## 3. B — Remaining Context contract/publication work

- Publish `context-market-input/v1.0` (this file, now v0.5, Draft) — requires Review A
  and a Product Owner decision; creation of the immutable
  `docs/architecture/input-contract-versions/context-market-input/v1.0.yaml` snapshot is
  explicitly reserved for that publication transaction (ADR-041), not performed here.
- Author Context's own output Event Contracts (`market-context-snapshot`,
  `market-context-fact-invalidated`) — do not exist yet (`context.md` §21). Each must
  carry its own ADR-048 `causal_state_dependency_declaration`, but the two contracts do
  NOT share one uniform shape — fresh-read `context.md` §3/§4 this transaction:
  - `MarketContextSnapshot`'s `causation_refs` is never empty, but its content differs by
    case: **original computation** — exactly `context_cutoff_source_ref` plus all six role
    fact refs (seven elements); **correction replacement** — the current (possibly
    updated) role refs **plus** the `MarketContextFactInvalidated` event being superseded
    (`context.md` lines ~156). A single fixed "seven causation_refs" shape does not cover
    the replacement case.
  - `MarketContextFactInvalidated`'s `causation_refs` = exactly one `invalidated_fact_ref`
    **plus** a minimal-complete direct-cause set (one or more refs each) for every role in
    `affected_upstream_roles`, unioned/deduped into one flat array (`context.md` §4,
    ADR-046 Decision item 7) — cardinality is genuinely variable, not seven, not fixed.
  - Which individual roles/refs are `STATE_DEPENDENCY` vs `EXTERNAL_NON_STATE_CAUSE` is
    **not decided by this derivation** — this WP is a closure derivation, not the output
    Event Contract authoring WP, and no existing authority uniquely determines those
    classifications by analogy alone (e.g. the candle-cutoff-ref classification is NOT
    hard-coded here merely because Regime's own `candle_evidence_ref` role happens to be
    `EXTERNAL_NON_STATE_CAUSE` — Context's own apply-time test has not been derived).
- Context's own output stream identity/writer authority — **genuine architecture
  escalation, not a mechanical registry edit** (§5 below). Not decided, not minted, and
  `stream-registry.yaml` not touched by this derivation.
- Per the terminology discipline Package 1.3-B already established for itself (§5 below),
  whoever authors these Event Contracts should follow the same "eligible cursor-bounded
  ... projection record" / record-integrity framing `feature-context-architecture.md`
  §5.2 and the `python/context-aggregator/README.md` already use, rather than reproducing
  `context.md` §2's own unmodified "authoritative event record" wording verbatim into a
  new artifact — this is a wording-discipline note for that future work, not a decision
  this WP makes on context.md's behalf.

## 4. C — Remaining runtime/implementation work

- `context-aggregator` runtime: four-stream frontier/cut-capture (the protocol
  `context-market-input.yaml` specifies), causal-closure fixed-point execution,
  `computation_cursor` construction, binding the existing deterministic core's result to
  a real Chapter 8 envelope, output publication path.
- Invalidation/replacement lineage runtime (`context.md` §4/§12 Case A/Case B,
  `COVERS_CONTEXT` evaluation) — the deterministic core's `selection.py` already resolves
  lineage over a *supplied* candidate/invalidation set; it does not yet compute that set
  from a live stream.
- `context_definition_version` concrete registry/storage mechanism — `context.md` §22
  and `feature-context-architecture.md` §13 both already defer this as a cross-cutting,
  not-yet-elaborated Phase-1/Phase-3 concern shared with Swing/Structure/Regime/Feature;
  M3 does not need to solve it uniquely for Context.
- `MarketContextCurrentView` runtime, if Review A disagrees with §1's scoping above.

## 5. D — Architecture/authority questions

Two distinct questions were examined under this heading. **D1** (terminology tension) is
resolved, non-blocking. **D2** (output stream identity) is a genuine, authority-undecided
architecture decision — the corrected overall WP terminal (§10).

### D1 — Chapter-7-§7.4-vs-`context.md` "authoritative event record" tension (RESOLVED, non-blocking)

**This is NOT a new unresolved architecture question raised by this WP — it is an
already-adjudicated, explicitly carried-forward, non-blocking open gap, confirmed by
three independent, mutually-consistent existing authorities:**

1. `docs/architecture/module-registry.yaml`'s own `context-aggregator` entry (`notes`
   field) already distinguishes "immutable-record-integrity" from
   "authoritative-domain-ownership" and names
   `docs/architecture/engine/feature-context-architecture.md` as the artifact that draws
   this boundary.
2. `feature-context-architecture.md` §13 ("Open Domain và architecture gaps") states the
   tension explicitly, records that it was **partially addressed** at v0.2 (renaming its
   own self-description of Context's record from "authoritative MarketContextSnapshot" to
   "eligible cursor-bounded MarketContextSnapshot projection record" — separating
   record-integrity, which Context genuinely has, from authoritative domain-state
   ownership, which it does not), and records a **Product Owner consolidation decision**
   (2026-08-04) that approved Package 1.3-B "with the context.md authority-terminology
   tension preserved as an explicit non-blocking open gap" — i.e., a Product Owner has
   already ruled this does not block progress and declined to pick a new Context
   authority model.
3. `python/context-aggregator/README.md` independently states the same conclusion for the
   deterministic core: it is called an "eligible cursor-bounded Context aggregation
   candidate," never "authoritative," and the README names the gap as "preserved here
   unresolved, not decided by this slice" — consistent with, not contradicting, (1)/(2).

The part that genuinely remains open is narrower than the full tension: `context.md` §2's
own Domain Contract text still uses the "authoritative event record" envelope framing for
`MarketContextSnapshot`/`MarketContextFactInvalidated`, and no transaction to date
(Package 1.3-B, ADR-046, this WP) has corrected that specific wording — each has
explicitly declined to, on the grounds that rewriting `context.md`'s own normative text
is its own separate, governed Domain Contract transaction, not a side effect of
unrelated work. This is a **bounded, carried-forward wording-discipline item**, already
on record, not a blocker for M3 and not something this WP resolves or needs to resolve:
Context's future output Event Contracts can and should use the same
record-integrity-not-authoritative-ownership framing Package 1.3-B and the Python core
already adopted (§3 above), independent of whether `context.md` §2's own prose is ever
updated to match.

**D1 conclusion: no escalation.** Chapter 7 §7.4's prohibition on a Projection emitting an
authoritative domain fact is satisfied by construction once Context's future output
Event Contracts are framed, as Package 1.3-B's own precedent requires, as
record-integrity-guaranteeing projection records rather than authoritative domain facts —
this is an implementation/wording discipline for category B's future work, not an open
decision surface.

### D2 — Context output stream identity/writer authority (ARCHITECTURE ESCALATION — ADR_REQUIRED)

**v0.1 of this derivation incorrectly treated this as a mechanical "decide and mint"
step. Fresh-read this transaction, it is a genuine Event Model change under existing,
already-Approved authority — not a new rule invented by this WP:**

- Chapter 8 §8.3.1 (Locked): *"Tạo/xóa/tách stream, hoặc đổi writer authority, là thay
  đổi Event Model → ADR Required, kèm bump `registry_version`"* — creating, deleting, or
  splitting a stream, or changing writer authority, is an Event Model change requiring an
  ADR and a `registry_version` bump. §8.3.1 also vests stream identity/topology/writer
  authority **solely** in `docs/architecture/stream-registry.yaml` (I-12: one concept, one
  authoritative source) — an Event Contract may only *reference* a stream via
  `allowed_streams`, never define one.
- `docs/architecture/stream-registry.yaml` (status: Approved, `registry_version: v1.0`,
  fresh-read this transaction) contains exactly seven streams: the five analytical
  streams ADR-036 established (`market-data-ingestion-candle`, `structure-engine-swing`,
  `structure-engine-structure`, `raw-regime-engine-regime`, `feature-engine-feature`) plus
  the two protected control-plane streams (`platform-lifecycle`, `platform-audit`). **No
  Context output stream exists.**
- `docs/adr/ADR-036.md` (Approved) — the ADR that established this Genesis topology —
  scopes itself explicitly to "the currently-implemented Phase-3 core analytical chain"
  (`Market Data Ingestion → Structure/Swing → Raw Regime → Feature`). It does not mention,
  and was not asked to decide, `context-aggregator`'s own output. No later Approved ADR or
  registry transition has added one.
- `docs/architecture/module-registry.yaml`'s current `context-aggregator` entry declares
  `emits: [event, query]` but carries no `writer_authority`/`stream_ref` assignment on any
  stream (that assignment lives in `stream-registry.yaml`, not `module-registry.yaml`,
  per the authority split Chapter 8 §8.3.1 itself draws) — confirming no stream-level
  authority has been granted to this module yet, consistent with no stream existing for
  it to write to.

**Why existing authority cannot decide this on its own:** Chapter 8/ADR-036 both correctly
identify *that* a new stream + writer-authority decision is required; neither one *makes*
that decision for Context, because ADR-036 was scoped to a different (already-implemented
at the time) chain and explicitly did not extend itself to cover future writers. There is
no default rule anywhere in the Constitution for what a Projection's own output stream
should be named, scoped, or partitioned by — Chapter 8 §8.3.1's own alternatives analysis
(ADR-036 §Alternatives) rejected scope-partitioned streams (per-instrument/venue/timeframe)
for the analytical chain on combinatorial-growth grounds; whether that same reasoning
applies identically to a Projection's output, or whether Context's own five-field subject
scope (`context.md` §1) changes the calculus, is not pre-decided anywhere.

**Smallest viable decision surface** (this derivation does not answer it — stating it
precisely so the escalation is actionable, not vague):

> What post-Genesis logical output stream identity (or identities) and writer authority
> shall carry Context projection output records (`MarketContextSnapshot`,
> `MarketContextFactInvalidated`), and what `stream-registry.yaml` transition
> (new `registry_version`, `effective_from` activation on `platform-lifecycle`, per Chapter
> 8 §8.3.1/§8.3.5) does that require?

**Explicitly NOT part of this decision surface** (do not broaden): message broker/queue
technology, storage engine, deployment topology, or any other runtime infrastructure
choice — those are Chapter 0 §4b-excluded implementation concerns, not Event Model
decisions, and Chapter 8's own authority split keeps them out of `stream-registry.yaml`
entirely.

**Smallest viable alternatives** (illustrative only, not a recommendation — Review A/the
eventual ADR author decides):
1. One stream per writer module per fact family, following ADR-036's own chosen pattern
   exactly — a single `context-projection-context` (or similarly named) stream for both
   Context output event types, writer authority `context-aggregator`.
2. Two streams (one per output event type) — rejected-by-precedent unless Context's own
   semantics give a reason ADR-036's four analytical writers didn't have; ADR-036 chose
   one-stream-per-writer-per-fact-family specifically to avoid this split.
3. Defer the ADR until Context's runtime work begins, and treat Input Contract/Event
   Contract authoring (category B's other items) as not strictly blocked by it — Review A
   should confirm whether authoring the output Event Contracts can proceed with an
   `allowed_streams` placeholder pending the ADR, or whether the ADR must land first; this
   derivation does not decide that ordering question either.

## 6. E — Quality-Gate / lifecycle work required before M3 DONE

**v0.2 correction (`CONTEXT-CLOSURE-A-MAJ-04`):** v0.1 said Quality-Gate evidence must be
"sufficient for `context-aggregator` to leave `status: candidate`," tied to a Product
Owner "runtime slice approval." That recreates exactly the false per-module
approval-gate model `milestone.md` §3.1 already removed from this project
(`RIDE-CRITICAL-PATH-CORRECTION-001`): *"Chapter 13 §13.1 is explicit: `Quality Gate pass
≠ Product Owner approval`... Quality Gate never approves, locks, or decides phase
transition... a single phase-level [Approval] Gate... not a per-module gate."* Corrected:

- `context-aggregator` currently has **no resolved authoritative quality tier**.
  `module-registry.yaml`'s entry carries no `quality_tier` field, and Chapter 13 §13.4's
  own "initial assignment" table (Tier 0: Risk Gateway/Execution Engine/Position Ledger;
  Tier 1: Strategy/Feature/Structure/Regime Engine; Tier 2: API layer/Data Ingestion;
  Tier 3: Frontend) does not list `context-aggregator` or any Context/Projection module
  either. Per Chapter 13 §13.4's own tier-resolution chain item 4: *"tier không resolve
  được → undefined tier applicability → fail-closed → eligibility incomplete."* This is a
  **remaining governed prerequisite** — tier resolution is explicitly reserved to
  `module-registry.yaml`/Chapter 7 §7.5 authority (§13.4 item 1), not invented here, and
  not something this derivation assigns a value to.
- Once a tier resolves, the applicable Chapter-13 Quality Gate (coverage floor + the
  tier's additional requirement, e.g. Parity Test for Tier 1) must be evaluated and
  produce PASS/evidence — ordinary Quality-Gate evidence, not a standalone approval.
- Review A + Product Owner decision on `context-market-input/v1.0` publication (category
  B, item 1) — a publication decision under ADR-041, not a module-approval gate.
- Review A + Product Owner decision on Context's output Event Contracts once authored
  (category B) — likewise a publication decision, not a module-approval gate.
- The quality-tier resolution and Quality Gate evidence above feed the single Phase-3
  Approval Gate (Chapter 12 §12.2) when M3's work reaches that boundary — they do not
  themselves constitute or trigger a module-registry `status` transition; no fresh
  authority found by this derivation requires one, so none is included in §1's acceptance
  condition beyond "a resolved tier and the applicable Gate's evidence exist."
- `milestone.md` §3's own acceptance-condition field update — explicitly NOT done by this
  WP; requires its own Review A on §1's derived condition first.

## 7. Context Input Contract publication-readiness conclusion

`docs/architecture/input-contracts/context-market-input.yaml` (now v0.5, Draft, this
transaction) is **semantically ready, factually readiness-corrected, still correctly
Draft/unpublished**:

- Semantic body (merge_policy, frontier_policy, causal_closure_policy, four-stream
  cut-capture protocol): unchanged, sound, no defect found.
- Readiness narrative: corrected across two rounds this WP (v0.3 → v0.4
  `CONTEXT-IC-CLOSURE-001`, then v0.4 → v0.5 `CONTEXT-IC-CLOSURE-002`) — the stale
  "Candle/Structure/Regime Event Contract authority absent/unresolved" conclusion is
  replaced with a fresh-verified, precisely-scoped conclusion: resolved for the **10
  current-target** version-artifacts (Candle v1.0 ×2, Structure v1.0 ×4, Regime v1.0 ×2,
  Feature v1.1 ×2); permanently fail-closed, by ADR-048's own non-retroactivity design,
  for the 2 historical, co-existing `feature-computed`/`feature-fact-invalidated` v1.0
  artifacts if a causal-closure step ever needs to classify one of their causation_refs.
  Zero semantic/policy value changed across either correction round.
- Remaining blockers to actual publication (unchanged by this correction): the immutable
  `v1.0` snapshot does not yet exist (reserved for the publication transaction, ADR-041);
  this candidate has not yet had its own Review A / Product Owner decision.
- Overall Context-authoritative-publication fail-closed conclusion is unchanged — but the
  *reason* has narrowed from "upstream Event Contract authority absent" to "Context's own
  output Event Contract/stream/runtime not yet authored" (category B/C above) **plus** the
  narrow, permanent historical-Feature-v1.0 fail-closed carve-out just stated. This
  Input Contract's own publication readiness is **not** blocked by the D2 output-stream
  escalation (§5) — that escalation concerns Context's OUTPUT stream, not the four
  UPSTREAM streams this Input Contract reads from — but the overall M3 output path remains
  blocked on it regardless.

## 8. Remaining M3 work graph (dependency ordering)

```
0. ADR: decide Context output stream identity + writer authority;    [no dependency —
   Stream Registry transition (registry_version bump, §5 D2)           smallest, most
                                                                         independent next step]
1. Review A + PO decision: publish context-market-input/v1.0          [no dependency —
                                                                         independent of (0)]
2. Author Context output Event Contracts (market-context-snapshot,     [depends on: (0) Approved,
   market-context-fact-invalidated), each with its own actual           for allowed_streams; NOT
   causation-ref-category ADR-048 declaration (§3 — not a uniform       on (1)]
   seven-ref shape), targeting (0)'s stream identity
3. context-aggregator runtime: envelope binding, frontier capture,     [depends on: (1) published,
   causal-closure execution, computation_cursor construction            (2) published, for the
                                                                         envelope/stream it writes to]
4. Invalidation/replacement lineage runtime (Case A/Case B,            [depends on: (3)]
   COVERS_CONTEXT)
5. Resolve context-aggregator's authoritative quality tier             [no dependency — may run
   (module-registry.yaml, Chapter 13 §13.4); evaluate the applicable    in parallel with (0)-(4);
   Quality Gate once resolved                                           PO-reserved classification]
6. milestone.md §3 acceptance-condition persisted (separate Review A   [depends on: this
   on this derivation's §1, not performed by this WP)                   derivation's own Review A]
```

## 9. Recommended next bounded implementation WP(s)

0. **Context output stream ADR** — the smallest, most independent, and now highest-
   priority next step (§5 D2): decide Context's output logical stream identity and
   writer authority, author the ADR, run it through Review A/Independent Review B/Product
   Owner decision, then the mechanical `stream-registry.yaml` registry-version transition
   and `module-registry.yaml` alignment (ADR-023/ADR-036 precedent: mechanical
   transcription, no new decision at that step). Blocks category B's output Event
   Contract authoring (item 2 below), not Input Contract publication (item 1).
1. **Context Input Contract publication WP** — Review A on this v0.5 candidate, Product
   Owner decision, atomic publication (create the immutable `v1.0` snapshot per ADR-041).
   Independent of (0); no new authority needed.
2. **Context output Event Contract authoring WP** — author `market-context-snapshot`/
   `market-context-fact-invalidated` Event Contracts against `context.md` §3/§4's already
   -fixed payload shapes (two different causation_refs shapes, §3 above — not a uniform
   seven-ref declaration), each with its own ADR-048 declaration, targeting (0)'s now-
   Approved stream identity. Should explicitly carry forward the record-integrity-not-
   authoritative-ownership terminology discipline (§5 D1 above). Depends on (0).
3. **context-aggregator runtime integration WP** — bind the existing, unmodified
   deterministic core to a real envelope/frontier/publication path. Depends on (1) and (2)
   being Published.
4. **context-aggregator quality-tier resolution** — a Product-Owner-reserved
   classification (§6), not invented here; may proceed independently/in parallel with
   (0)-(3).

Each should remain its own bounded WP, consistent with this WP's own instruction not to
micro-split *this* closure analysis — the analysis is one coherent artifact; the
*implementation* that follows from it is naturally several separate, bounded WPs.

## 10. Overall WP terminal

`ARCHITECTURE_ESCALATION` — D2 (§5) is a genuine, authority-undecided, ADR-required
Event Model decision (Context's own output stream identity/writer authority) that
existing repository authority (Chapter 8 §8.3.1, ADR-036) identifies as required but does
not itself resolve. D1 (the terminology tension) remains correctly resolved/non-blocking
and does not itself independently trigger escalation; D2 alone does. No ADR is authored,
no stream is minted, and `stream-registry.yaml`/`module-registry.yaml` are not touched by
this derivation or by this correction.
