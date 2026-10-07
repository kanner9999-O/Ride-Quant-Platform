# M3 Workstream — Feature Future Dependency Authority

Project orchestration packet only. NOT governance authority, NOT an ADR, NOT a
Product Owner decision. Subordinate to Constitution / Approved ADR / Domain
Contract authority at all times — this packet bounds scope, it does not grant it.

## Identity

```text
workstream_id:   m3-feature-future-dependency-authority
parent_milestone: M3 — Context Projection / context-aggregator
planning_head:   197100785fb786278816b5b694dc9d380d9c1b8b
owner/executor:  AI Technical Architect (Claude or ChatGPT) — bounded WP Executor,
                 per Lean Ride Operating Model v1.1 §3
state:           NOT_STARTED
```

## Objective

Determine, as one coherent bounded analysis, whether `feature-computed`/
`feature-fact-invalidated` (both `status: Published`, `v1.0`) require a new
version to carry Approved `ADR-048`'s `causal_state_dependency_declaration` field,
and if so, what Chapter 10 §10.4 Compatibility Result classification that delta
would receive — not a sequence of per-field micro-transactions. This workstream is
independent of Structure/Regime's own Event Contract content (see rejected
dependency assumption in the control plane) — it is self-contained to Feature's own
already-Published artifacts and existing classification evidence.

## Authority closure set

Fresh-read in full before any semantic conclusion:

- `docs/domain/feature.md` v0.6 — the complete Domain Contract, not only the sections a prior Candle/Structure precedent happened to use.
- `docs/architecture/event-contracts/feature-computed/v1.0.yaml` and `docs/architecture/event-contracts/feature-fact-invalidated/v1.0.yaml` — the current Published artifacts, read in full (including whatever state-dependency representation they currently carry, if any).
- `docs/adr/ADR-048.md` (Approved, v0.3) — canonical `causal_state_dependency_declaration` grammar.
- `docs/adr/ADR-038.md` (Approved) — "Feature Output Event Contract Compatibility Commitment"; the existing governing decision for these two `contract_id`s' compatibility posture — do not assume ADR-047 (which does not enumerate Feature) applies instead.
- `docs/adr/ADR-039.md` (Approved) — Event Contract self-containment model.
- `docs/constitution/10-compatibility-capability-contract.md` §10.3 (version compatibility), §10.4 (Compatibility Result — immutable artifact, not a one-off check), §10.7 (downstream impact assessment).
- `docs/project/context-upstream-state-dependency-derivation-001.md` v0.5 §2.1/§2.2 — existing classification evidence for `FEATURE_COMPUTED`/`FEATURE_FACT_INVALIDATED`'s causation categories (already derived; this workstream does not re-derive classification, only representation/version consequence).
- `docs/architecture/context-map.yaml` — confirm Feature's own registered consumers (not Structure's or Regime's).

Do not fresh-read unrelated history (Candle's/Structure's/Regime's own authoring or correction rounds) merely for completeness — Feature's own Domain Contract, its two Published artifacts, and its own governing ADR (`ADR-038`) are the controlling sources.

## Semantic Closure stage

Before any conclusion, derive this matrix (minimum rows below; add rows if full-section reading surfaces more):

| semantic topic | authoritative source | resolved? | unresolved decision? | implementation consequence |
|---|---|---|---|---|
| Feature's own causation-ref classification (STATE_DEPENDENCY vs EXTERNAL_NON_STATE_CAUSE) | derivation v0.5 §2.1/§2.2 | resolved | no | reuse as-is; do not re-derive |
| Whether a Published v1.0 Event Contract may gain `causal_state_dependency_declaration` without a version bump | `ADR-039` self-containment model + Chapter 10 §10.3 version-compatibility rules | to be determined during fresh-read | likely yes a version question — confirm against §10.3's own text, do not assume | determines whether this is a vNext authoring task or a zero-version-impact clarification |
| Compatibility Result classification of that delta (additive field vs. breaking) | Chapter 10 §10.4 | to be determined during fresh-read | unknown until read | determines whether `ADR-038`'s existing `backward_only`-style commitment (confirm exact value, do not assume it matches ADR-047's Candle/Structure/Regime value) already covers this delta or requires a fresh Compatibility Result artifact |
| Whether Feature consumes any Structure/Regime event type directly (would create a true cross-lane dependency this packet does not currently assume) | `context-map.yaml`, `feature.md` fan-in rules | to be re-verified fresh, not inherited from a prior session's conclusion | no, pending fresh verification | if fresh verification finds a genuine direct consumption edge, this changes the control plane's "no true dependency" conclusion — escalate rather than silently proceeding on the old assumption |

## Existing findings / debt

None opened against `feature-computed`/`feature-fact-invalidated` specifically in
this session's history. Carry forward only the fact that these two artifacts are
`status: Published` and therefore immutable as currently written (`ADR-039`
self-containment + Chapter 11 §11.3 immutability-after-publication precedent) — any
change is necessarily a NEW version, never an in-place edit.

## Implementation scope

After semantic closure, this lane MAY:

- Produce the bounded analysis artifact (version-impact + Compatibility Result classification conclusion) as a new file under `docs/project/`.
- IF the analysis concludes a new version is warranted: author a Draft (not Published) `feature-computed`/`feature-fact-invalidated` vNext Event Contract candidate, `status: Draft`, carrying the ADR-048 declaration — never editing the existing Published `v1.0` files in place.

## Explicit forbidden scope

- No governance amendment (Constitution, Global Execution Rules, Phase-3 rules, Lean Ride Operating Model).
- No mutation of `structure`, `regime`, or any other workstream's files.
- No in-place edit of the Published `feature-computed/v1.0.yaml` or `feature-fact-invalidated/v1.0.yaml` files.
- No mutation of `feature.md` itself (Domain Contract) or `ADR-038`.
- No Product Owner decision fabrication.
- No spontaneous ADR authoring.
- No publication of any new version unless separately authorized by current authority.

## Escalation contract

Terminate with exactly `ARCHITECTURE_ESCALATION` only when a genuinely unresolved
semantic/authority decision is found that existing authority cannot decide — report:

- exact question;
- exact conflicting/missing authorities;
- affected artifacts/modules;
- reversible local option(s), if any;
- why existing authority cannot decide it.

Do not author an ADR as part of the escalation report. In particular, if fresh
verification finds Feature genuinely consumes a Structure or Regime event type
directly (contradicting this packet's own "no true dependency" assumption), report
that as an escalation finding about the control plane's dependency graph, not as a
reason to silently create a new cross-lane dependency without recording it.

## Completion contract

Report exactly one of: `WORKSTREAM_COMPLETE`, `ARCHITECTURE_ESCALATION`, or
`BLOCKED_BY_EXTERNAL_DEPENDENCY`. No Review A request is made until one coherent
analysis conclusion (plus any warranted Draft candidate) exists.
