# M3 Context Closure Derivation — 001

```
status: Draft (reasoning-heavy derivation artifact, not an authority artifact)
version: "0.1"
owner: Product Owner
generated_at: "2026-10-08"
role: M3 Context Closure Executor
```

Purpose: derive, from existing repository authority only, the actual remaining M3
("Context Projection / context-aggregator") completion boundary — per
`docs/project/milestone.md` §3's own explicit statement that this has not yet been
derived. This artifact does NOT amend `docs/project/milestone.md` — it is evidence for a
separate, later Review A / Product Owner decision that persists its conclusion into the
milestone register.

## 1. Derived M3 acceptance condition

M3 ("Context Projection / context-aggregator") is DONE when all of the following hold,
simultaneously, for `context_type: market_context` (`docs/domain/context.md` v0.4):

1. The Context-scoped Input Contract (`context-market-input/v1.0`) is Published as an
   immutable snapshot (Approved ADR-041 discipline).
2. Context's own output Event Contracts (`market-context-snapshot`,
   `market-context-fact-invalidated`) are authored and Published, each carrying an
   Approved-ADR-048-conformant `causal_state_dependency_declaration` classifying
   Context's own seven causation_refs.
3. `context-aggregator`'s runtime binds the existing deterministic aggregation core
   (`python/context-aggregator/`, unaffected by this WP) to a real Chapter 8 §8.2 envelope
   — genuine `event_id`/`stream_ref`/`producer_ref`/`sequence`/`causation_refs` — and
   performs the four-stream frontier capture, causal-closure execution, and
   `computation_cursor` construction this Input Contract's own protocol specifies.
4. The invalidation/replacement lineage runtime behavior (`context.md` §4/§12, Case A/
   Case B, `COVERS_CONTEXT`) is implemented and tested against the Domain Contract's own
   worked examples.
5. Quality-Gate evidence sufficient for `context-aggregator` to leave `status: candidate`
   in `module-registry.yaml` exists (tests, Review A, Product Owner decision on the
   runtime slice) — the exact Quality Tier/Gate mechanism is not invented by this
   derivation; it is whatever Chapter 13 already requires for a Type-2 Projection.

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

- All ten upstream Event Contracts (Candle ×2, Structure ×4, Regime ×2, Feature ×2) are
  `status: Published`, each carrying an Approved-ADR-048-conformant
  `causal_state_dependency_declaration` (fresh-verified this transaction).
- Feature's two contract_ids have since advanced to `v1.1` (also Published); both `v1.0`
  and `v1.1` coexist as Published, which is expected under ADR-039's versioning model —
  historical events keep citing whichever version was current when they were produced.
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

- Publish `context-market-input/v1.0` (this file, now v0.4, Draft) — requires Review A
  and a Product Owner decision; creation of the immutable
  `docs/architecture/input-contract-versions/context-market-input/v1.0.yaml` snapshot is
  explicitly reserved for that publication transaction (ADR-041), not performed here.
- Author Context's own output Event Contracts (`market-context-snapshot`,
  `market-context-fact-invalidated`) — do not exist yet (`context.md` §21). Each must
  carry its own ADR-048 `causal_state_dependency_declaration` classifying Context's seven
  causation_refs (candle cutoff ref as EXTERNAL_NON_STATE_CAUSE by the same reasoning
  Regime's own `candle_evidence_ref` role uses; the Structure/Regime/Feature role refs
  need their own classification — not decided by this WP).
- Decide and mint Context's own output stream identity and register it in
  `stream-registry.yaml` (a registry transition, not a Genesis edit — Chapter 8 §8.3.1).
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

**The Chapter-7-§7.4-vs-`context.md` "authoritative event record" tension is NOT a new
unresolved architecture question raised by this WP — it is an already-adjudicated,
explicitly carried-forward, non-blocking open gap, confirmed by three independent,
mutually-consistent existing authorities:**

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

**Conclusion: architecture escalation NONE.** No genuine, authority-undecided
contradiction blocks M3 closure. Chapter 7 §7.4's prohibition on a Projection emitting an
authoritative domain fact is satisfied by construction once Context's future output
Event Contracts are framed, as Package 1.3-B's own precedent requires, as
record-integrity-guaranteeing projection records rather than authoritative domain facts —
this is an implementation/wording discipline for category B's future work, not an open
decision surface.

## 6. E — Quality-Gate / lifecycle work required before M3 DONE

- Review A + Product Owner decision on `context-market-input/v1.0` publication (category
  B, item 1).
- Review A + Product Owner decision on Context's output Event Contracts once authored
  (category B).
- Whatever Quality Tier / Quality-Gate evidence Chapter 13 requires for a Type-2
  Projection to leave `module-registry.yaml`'s `status: candidate` (category C's last
  item) — not newly invented here; this derivation does not create a new gate.
- `milestone.md` §3's own acceptance-condition field update — explicitly NOT done by this
  WP; requires its own Review A on §1's derived condition first.

## 7. Context Input Contract publication-readiness conclusion

`docs/architecture/input-contracts/context-market-input.yaml` (now v0.4, Draft, this
transaction) is **semantically ready, factually readiness-corrected, still correctly
Draft/unpublished**:

- Semantic body (merge_policy, frontier_policy, causal_closure_policy, four-stream
  cut-capture protocol): unchanged, sound, no defect found.
- Readiness narrative: corrected in this transaction (v0.3 → v0.4,
  `CONTEXT-IC-CLOSURE-001`) — the stale "Candle/Structure/Regime Event Contract authority
  absent/unresolved" and "state-dependency classification unresolved" conclusions are
  replaced with a fresh-verified "resolved" conclusion, now that all twelve relevant
  upstream Event Contract artifacts are Published with ADR-048 declarations. Zero
  semantic/policy value changed.
- Remaining blockers to actual publication (unchanged by this correction): the immutable
  `v1.0` snapshot does not yet exist (reserved for the publication transaction, ADR-041);
  this candidate has not yet had its own Review A / Product Owner decision.
- Overall Context-authoritative-publication fail-closed conclusion is unchanged — but the
  *reason* has narrowed from "upstream Event Contract authority absent" to "Context's own
  output Event Contract / runtime not yet authored" (category B/C above).

## 8. Remaining M3 work graph (dependency ordering)

```
1. Review A + PO decision: publish context-market-input/v1.0          [no dependency]
2. Author Context output Event Contracts (market-context-snapshot,     [depends on: context.md's
   market-context-fact-invalidated), each with ADR-048 declaration      existing §3/§4 payload
   and Context output stream identity registered in stream-registry     shapes — already fixed;
                                                                         no new dependency on (1)]
3. context-aggregator runtime: envelope binding, frontier capture,     [depends on: (1) published,
   causal-closure execution, computation_cursor construction            (2) published, for the
                                                                         envelope/stream it writes to]
4. Invalidation/replacement lineage runtime (Case A/Case B,            [depends on: (3)]
   COVERS_CONTEXT)
5. Quality-Gate evidence; module-registry status: candidate -> next    [depends on: (3), (4)]
6. milestone.md §3 acceptance-condition persisted (separate Review A   [depends on: this
   on this derivation's §1, not performed by this WP)                   derivation's own Review A]
```

## 9. Recommended next bounded implementation WP(s)

1. **Context Input Contract publication WP** — Review A on this v0.4 candidate, Product
   Owner decision, atomic publication (create the immutable `v1.0` snapshot per ADR-041).
   Smallest, most independent next step; no new authority needed.
2. **Context output Event Contract authoring WP** — author `market-context-snapshot`/
   `market-context-fact-invalidated` Event Contracts against `context.md` §3/§4's already
   -fixed payload shapes, each with an ADR-048 declaration, plus the output stream
   registry addition. Should explicitly carry forward the record-integrity-not-
   authoritative-ownership terminology discipline (§5 above).
3. **context-aggregator runtime integration WP** — bind the existing, unmodified
   deterministic core to a real envelope/frontier/publication path. Depends on (1) and (2)
   being Published.

Each should remain its own bounded WP, consistent with this WP's own instruction not to
micro-split *this* closure analysis — the analysis is one coherent artifact; the
*implementation* that follows from it is naturally several separate, bounded WPs.
