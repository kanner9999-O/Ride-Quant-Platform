---
id: context-aggregator-quality-tier-derivation-001
title: "Context Aggregator — Chapter 13 Quality-Tier Classification Derivation"
kind: analysis
version: "0.1"
status: Draft
owner: Product Owner
generated_at: "2026-10-09"
---

# Context Aggregator — Chapter 13 Quality-Tier Classification Derivation

> **What this artifact does NOT do.** It does **not** edit `module-registry.yaml`. It does **not**
> assign `context-aggregator`'s `quality_tier` as authoritative. It does **not** run or claim any
> Chapter 13 Quality Gate result. It does **not** create an ADR (fresh ADR Scope analysis below
> finds none required). It does **not** create a module/phase approval gate. It does **not** modify
> `python/context-aggregator/**` or any other implementation. It produces exactly one thing: a
> **candidate** tier classification, with full reasoning, rejected alternatives, and the exact
> decision surface, for **Review A and then Product Owner decision**.

## §0. Boundary and fresh-verification record

- **Reviewed boundary (HEAD):** `0dbd9f44fd9fa85dbf1ccba984608380273dbade` — fetched from
  `origin/main` and verified via `git rev-parse HEAD` in an isolated worktree before any read,
  matching the expected main boundary supplied with this task exactly.
- **Branch:** `workstream/m3-context-aggregator-quality-tier`, created fresh from `origin/main`
  at the boundary above — no prior Draft/correction history (e.g. ADR-050) pulled in.
- **Fresh-read artifacts and their exact blob identity at this boundary** (`git ls-tree HEAD`):

  | Artifact | Blob |
  |---|---|
  | `docs/constitution/13-quality-gates.md` | `acf4ab75eda1ea0613250ce3159669ea727e28ec` |
  | `docs/constitution/07-module-taxonomy.md` | `173d76542c91692ba49cb3ba49b444f9fa939590` |
  | `docs/constitution/11-adr-process.md` | `38364f9f9448ae0da563a868db172256d3f5b229` |
  | `docs/adr/ADR-045.md` | `ac13ece16ff644d0d88ddf982d83bfb0e8d5ad16` |
  | `docs/architecture/module-registry.yaml` | `8535f92efeb76ffb226791d201dc0b3fb71f06c0` |
  | `docs/domain/context.md` | `d7b2c07b82984958e52ede0d536cc443ade22577` |
  | `docs/architecture/engine/feature-context-architecture.md` | `0c08cd3518fd5d0aa97ba9d052c6bca587eb2162` |
  | `python/context-aggregator/README.md` (+ `src/`, `tests/`) | `f706a782e1659d670de426cc34d1813c7b536ad1` |
  | `docs/governance/lean-ride-operating-model-v1-candidate.md` | `7c33d891d4d304f73c14e89ccd4362b9edd9f094` |

- **Ground truth confirmed, independently, at this boundary** — `context-aggregator`'s current
  `module-registry.yaml` entry (lines 803–820):

  ```yaml
  module_id: context-aggregator
  module_type: projection
  owns_authoritative_state: false
  consumes: [event]
  emits: [event, query]
  depends_on: [market-data-ingestion, structure-engine, raw-regime-engine, feature-engine]
  forbidden_dependencies: []
  security_classification: none
  status: candidate
  # quality_tier field: ABSENT
  ```

  `quality_tier` is genuinely absent — not `null`, not an empty object. Per the registry's own
  field reference (`module-registry.yaml` lines 651–664, this boundary): *"Absence of this field
  on a module means its tier is UNRESOLVED (Chapter 13 §13.4 point 4, fail-closed) — absence is
  not 'no tier'/'Tier 3 default,' it is 'not yet classified.'"* This derivation treats that absence
  as fully open — it does **not** infer a default, and does not treat the absence itself as
  evidence for any particular tier.

## §1. Tier-resolution authority path (Chapter 13 §13.4)

Chapter 7 §7.0/§7.1 defines "module" exhaustively as one of three runtime-application types
(`compute_engine` | `projection` | `runtime_service`); `context-aggregator` is registered as
`module_type: projection` in `module-registry.yaml`. It is therefore unambiguously a **runtime
module** for Chapter 13 §13.4's tier-resolution chain, and resolves via **branch 1**:

> "Runtime module → resolve tier từ `module-registry.yaml`, Chapter 7 §7.5."

This is the exact same branch every prior tier pin in this registry resolved through
(`market-reference-service`, `market-data-ingestion`, `structure-engine`, `raw-regime-engine`,
`feature-engine` — all five explicitly cite this same branch-1 path in their own registry
history). **No §13.4.1/§13.4.2 canonical-authority machinery is needed or invoked here** — that
machinery exists for standalone or owned *executable artifacts without a canonical owning
module*; `context-aggregator` already has a canonical owning module (itself), per the same
precedent reasoning already recorded for `feature-engine`'s own pin.

Chapter 13's own §13.4 "initial assignment" table does **not** name a "Projection" or "Context
Aggregation" row directly — it names Risk Gateway/Execution Engine/Position Ledger (Tier 0),
Strategy/Feature/Structure/Regime Engine (Tier 1), API layer/Data Ingestion (Tier 2), Frontend
(Tier 3). Per §13.4's own text, that column is "the current mapping for already-known modules, not
a competing authority with the registry" — so the absence of a named row is expected and does not
make the module "unclassifiable"; it means the classification must be **derived** from Chapter
7 §7.4/§7.5 criteria and the module's actual registered role, which is exactly this artifact's
purpose.

## §2. What `context-aggregator` actually is and does

- **Registry-declared role:** "CQRS read-model tổng hợp Structure+Regime+Feature+market state cho
  Strategy tiêu thụ" (`module-registry.yaml` line 808) — a Type 2 Projection (Chapter 7 §7.4):
  non-authoritative, deterministic, rebuildable from the authoritative event log, forbidden from
  ever originating an authoritative domain fact/decision/state transition.
- **Upstream dependency set:** `market-data-ingestion`, `structure-engine`, `raw-regime-engine`,
  `feature-engine` — i.e., it fans in from *every* analytical layer in the platform, directly
  (ADR-014's "Context snapshot aggregation" is a distinct fan-in operation from "Feature
  computation fan-in", not routed through Feature Engine as an intermediary;
  `feature-context-architecture.md` §3).
- **Downstream consumer:** per `feature-context-architecture.md` §3's data-flow diagram,
  `context-aggregator`'s output (`MarketContextSnapshot`/`MarketContextFactInvalidated` events,
  `GetCurrentContext`/`GetContextHistory` queries) feeds directly and *only* into
  **Strategy/Decision Engine** — it is the single convergence point between the analytical layer
  (Structure/Regime/Feature) and the decision layer.
- **What it explicitly never contains** (`context.md` §3 invariants; enforced structurally by
  `python/context-aggregator/tests/test_aggregation.py::test_context_values_has_no_strategy_
  decision_risk_execution_fields`): signal strength, setup quality, bias, buy/sell/hold,
  entry/stop/target, position size, strategy ID, account state. It copies upstream values
  verbatim (`context.md` §3: "Context KHÔNG tự tính toán lại, KHÔNG diễn giải thêm ý nghĩa") — it
  does not re-derive Structure/Regime/Feature semantics.
- **Implementation status today** (`python/context-aggregator/README.md`, this boundary): a
  deterministic aggregation core only — no runtime/event-log integration, no Input/Event Contract
  publication, no Strategy/Decision integration, **"No Quality Tier / Quality-Gate PASS —
  `context-aggregator`'s `quality_tier` remains unresolved after this transaction; no formal
  Chapter 13 Quality Gate result is claimed here."** This confirms the `ABSENT` field is not an
  oversight — it is a known, carried-forward open item, consistent with this derivation's premise.

## §3. Chapter 7 §7.4's controlling criticality rule for projections

Chapter 7 §7.4 (Locked) states the exact rule this derivation turns on:

> "**Criticality (nhất quán I-6 Fail-Safe by Scope):** projection **không critical** được phép
> degrade có kiểm soát mà không dừng toàn platform. **NHƯNG derived ≠ luôn non-critical** — một
> projection được dùng làm dependency của decision/risk/execution (ví dụ exposure read-model mà
> Risk Gateway đọc, order-state projection dùng reconcile) phải **khai báo criticality và failure
> policy tường minh**; khi tính đúng đắn hoặc độ freshness của nó không xác định, consumer phải
> fail-safe theo I-6. Điều này không biến projection thành authoritative source."

This is a direct, named carve-out: being a Type-2 Projection does **not** default a module to
"non-critical" when that projection is a declared dependency of the decision pipeline.
`context-aggregator` is exactly this case — its sole declared consumer is Strategy/Decision
(§2 above), and its own domain contract (`context.md`) makes clear its entire purpose is to be
the aggregated input to that decision layer. The rule does **not** make Context an authoritative
source (it stays Type 2, `owns_authoritative_state: false`) — but it does mean Context cannot be
waved through to the lowest-rigor tier merely because it is "just a projection."

## §4. Candidate tier — recommendation and rejected alternatives

| Tier | Verdict | Reasoning |
|---|---|---|
| **Tier 0 — Critical** | **Rejected** | Reserved for Risk Gateway / Execution Engine / Position Ledger — modules with an authoritative execution, custody, or risk-control side effect, whose failure causes direct, irreversible platform/financial harm (the Chapter-13-mandated Chaos Test trigger presumes exactly this). `context-aggregator` owns no such side effect: it is `owns_authoritative_state: false`, Type 2 Projection, structurally forbidden (Chapter 7 §7.4) from ever originating an authoritative domain decision or state transition. |
| **Tier 3 — UI** | **Rejected** | Not a frontend/UI artifact; plainly out of scope for this row. |
| **Tier 2 — Supporting** (same tier as its own upstream `market-data-ingestion`/`market-reference-service`) | **Rejected** | Tier 2's two named precedent members are the **raw-observation / reference-data boundary** — the foundational layer that each independent analytical engine (Structure, Regime, Feature) subsequently re-derives and re-verifies before anything reaches Decision. `context-aggregator` has no equivalent downstream re-verification step: it sits **directly** between the analytical layer and Strategy/Decision, so an aggregation defect here propagates straight into the decision input with no further independent engine positioned to catch it first. Treating it as Tier 2 would also contradict Chapter 7 §7.4's explicit instruction (§3 above) that a decision-dependency projection may **not** default to the non-critical/Supporting treatment that would otherwise apply to "just a projection." |
| **Tier 1 — Core Logic** | **Recommended candidate** | (1) Chapter 13's own Tier 1 row names exactly the three modules that are `context-aggregator`'s entire upstream dependency set — `Structure Engine`, `Regime Engine` (`raw-regime-engine`), `Feature Engine` — all three already Product-Owner-approved at Tier 1 in this same registry. `context-aggregator` is the module that converges all three of these Tier-1 outputs (plus Candle) into the single artifact Strategy/Decision actually consumes — it does not sit outside this group's criticality, it sits at its exact convergence point. (2) Chapter 13 §13.12-C ties the mandatory **Parity Test** to Tier 1 precisely because of "decision-pipeline responsibility" — and `context-aggregator`'s *only* declared consumer is the decision pipeline (§2). (3) Chapter 7 §7.4's named exception for decision-dependency projections (§3) independently points the same direction without relying on the Tier 1 table's engine-name list alone. |

## §5. Does downstream Strategy/Decision use raise criticality?

**Yes — this is the primary driver of the recommendation**, not a secondary consideration. Two
independent, already-Locked authorities converge on it: Chapter 7 §7.4's explicit
projection-as-decision-dependency carve-out (§3), and Chapter 13 §13.12-C's explicit tying of the
Parity Test trigger to "decision-pipeline responsibility" at Tier 1. Nothing in this derivation
invents a new criterion — both are read directly off already-approved Constitution text.

## §6. Does Projection / rebuildability lower criticality?

**No — not for the coverage-tier/test-rigor question.** Rebuildability (Chapter 7 §7.4's "phải
deterministic và rebuild được từ authoritative source", consistent with I-12) is a **recovery**
property: it means that *after* a fault is detected, the read-model can always be reconstructed
from the authoritative log. It is not a **prevention** property — it says nothing about whether a
logic defect in the aggregation code would be caught *before* a bad snapshot reaches Strategy/
Decision. Coverage floor and the Parity Test exist precisely to catch that class of defect pre-
publication; rebuildability does not substitute for either. Chapter 7 §7.4 makes this explicit by
naming "derived ≠ always non-critical" as the controlling rule rather than letting rebuildability
settle the question on its own. Rebuildability is relevant to a *different* axis — fail-safe/
recovery behavior (§7 below) — not to the coverage-tier selection itself.

## §7. Fail-safe implications

Two distinct, non-overlapping obligations apply, neither of which this transaction discharges:

1. **Universal invariant-conformance (§13.12-A, tier-independent):** Chapter 13 §13.5's
   Invariant Conformance Gate table lists I-6 "Fail-Safe by Scope" as applicable to
   "Engine/Projection/Runtime Service" — `context-aggregator` falls under this regardless of
   which coverage tier it is ultimately pinned to, because §13.12-A applies to every artifact
   in scope independent of tier. This derivation does not evaluate or claim that gate; it only
   notes it is in scope.
2. **Chapter 7 §7.4's consumer-side fail-safe duty:** when Context's correctness or freshness is
   undetermined, its **consumer** (Strategy/Decision) — not Context itself — must fail-safe per
   I-6. This is an obligation on the Strategy/Decision architecture, not something this
   module-registry tier derivation resolves; it is flagged here as an open item for whichever
   artifact elaborates Strategy/Decision's own architecture (Package 1.3-C, out of scope for
   Package 1.3-B / this task).

## §8. ADR Scope Rule — `G-ADR-004` self-check

| Check | Finding |
|---|---|
| 1. Does existing authority resolve this without a new decision? | Yes — Chapter 13 §13.4 branch 1 + Chapter 7 §7.4/§7.5 criteria, already Locked, are sufficient to derive a candidate; no new rule is being invented. |
| 2. Is it a genuine, hard-to-reverse architecture decision? | No — a `quality_tier` pin is revisable (every prior pin in this registry remained open to future correction via its own version/`package_lifecycle` mechanism); it changes no dependency edge, no module type, no contract. |
| 3. Does a Chapter 0 §4b trigger fire independently? | No. Not a Platform Invariant/Event Schema change. Not a Module Taxonomy/dependency-graph change (`module_type`/`depends_on` untouched). Not a governance/approval-process change. Not a decision affecting >1 module or hard to reverse — this is the **identical** reasoning already recorded verbatim for `market-reference-service`'s own v1.1→v1.2 tier pin: "neither the '>1 module' nor 'khó đảo ngược' clause triggers for one module's own tier field." Not an amendment to a Locked ADR. |
| 4. Was it authored merely to "complete" a prior ADR's open item (forbidden, `G-ADR-003`)? | No — this is a direct response to a fresh, explicitly-scoped Product Owner task, not manufactured to close an ADR's residual item. |

**Conclusion: `ADR_NOT_REQUIRED`** — identical disposition to all five prior tier-pin transactions
in this exact registry (`market-reference-service`, `market-data-ingestion`, `structure-engine`,
`raw-regime-engine`, `feature-engine`), for the same reasons.

## §9. Risk Classification (ADR-045, current authority — Review A mandatory, R2 cross-check optional, Product Owner is decision authority)

> **Explicit note on historical process:** several of this registry's prior tier-pin
> transactions cite a now-retired **mandatory Review B** step. That process is **superseded**.
> This derivation uses only the current model: **Review A mandatory → Risk Classification
> (R0/R1/R2) → routing**, with R2 cross-check optional/advisory/never mandatory, and Product
> Owner as sole decision/approval authority (ADR-045, Approved, supersedes ADR-042). No
> retired Review-B requirement is carried forward here.

**Risk Classification candidate: R1 — Bounded semantic / normal implementation risk.**

Reasoning against ADR-045's self-contained definitions: this is a classification decision that
(a) applies an already-Locked rule (Chapter 13 §13.4 tier table + Chapter 7 §7.4 criteria) to one
bounded, individually-verifiable module case; (b) introduces no new Platform Invariant, Event
Schema, authority/source-of-truth semantic, identity/lifecycle/replay/versioning semantic, or
cross-module contract/dependency change (no `depends_on`/`module_type`/`forbidden_dependencies`
edge is touched); (c) is reversible with a blast radius bounded to `context-aggregator`'s own
coverage floor and tier-triggered test requirement. None of R2's enumerated triggers (Platform
Invariant/Event Schema change; authority/source-of-truth semantics; cross-module contract/
dependency change with significant blast radius; destructive/irreversible transition; Review-A
confidence materially low; repeated same-artifact correction; etc.) materially applies.

**However — this does *not* make the decision Delegated-Technical-Resolution-eligible under
ADR-045's D1–D12 predicate, independent of the R1 finding.** D10(a) fails: *"a governing artifact
explicitly reserves this decision class to Product Owner."* `module-registry.yaml`'s own field
reference (§0 above, lines 651–664 at this boundary) defines `quality_tier` as valid **only**
"once a module's Chapter 13 §13.4 criticality classification has been **Product-Owner-approved**"
— this is the field's own schema-level reservation, not an inference. It is additionally
corroborated by unbroken precedent: all five prior `quality_tier` pins in this exact registry were
recorded as explicit Product Owner decisions, none as a Delegated Technical Resolution.

**Therefore: Risk R1, but routed to Product Owner Decision regardless of R-tier, under D10(a).**
This is a narrower and more precise basis than simply classifying the case R2 to force PO
routing — it keeps the Risk Classification honest while still reaching the correct (and, per
precedent, only-ever-used) routing for this exact decision class.

## §10. Candidate tier — summary for Review A

```text
Candidate module_id:         context-aggregator
Candidate tier:               Tier 1 — Core Logic
Coverage floor (derives from
  Chapter 13 §13.4 table,
  not duplicated/re-pinned):  >= 90% line AND >= 90% branch, independently
Tier-triggered requirement:   Mandatory Parity Test (Chapter 13 §13.4 table;
                               §13.12-C, "decision-pipeline responsibility")
                               — NOT Chaos Test (Tier 0-only)
ADR Scope:                    ADR_NOT_REQUIRED
Risk Classification:          R1
Delegation eligibility:       NOT delegated — D10(a) fails (field-level and
                               precedent Product-Owner reservation); routes to
                               Product Owner Decision regardless of R-tier
Quality Gate claimed:         NONE — no coverage/Parity/invariant-conformance
                               evidence is run, measured, or asserted by this
                               transaction
```

## §11. Exact Product Owner decision surface

This transaction asks the Product Owner, after Review A, to choose exactly one of:

1. **APPROVE CONTEXT-AGGREGATOR TIER 1 — CORE LOGIC** — accepts the candidate above as
   authoritative; a follow-up mechanical transaction then records it into
   `module-registry.yaml` (§12).
2. **Reject / request a different tier** — e.g., if the Product Owner judges the Tier-2
   reasoning (§4) more applicable than reasoned here, or wants a different coverage/requirement
   outcome; a correction round would follow the same pattern as prior tier-pin corrections in
   this registry (e.g. `market-data-ingestion`'s own Major-finding correction cycle).
3. **Request further analysis** — e.g., if the Product Owner wants the Strategy/Decision-side
   fail-safe obligation (§7, item 2) resolved first, or wants an explicit criticality/failure-
   policy statement authored into `context.md`/`feature-context-architecture.md` before pinning
   the tier.

No tier is asserted as authoritative by this transaction; §10's candidate is a recommendation
only.

## §12. Mechanical repository changes required AFTER approval (NOT performed by this transaction)

Once the Product Owner issues a decision under §11(1), a **separate, later** transaction would:

1. Add exactly one field to the `context-aggregator` entry in `module-registry.yaml`:
   ```yaml
   quality_tier: { tier: "Tier 1 — Core Logic", approved_by: "Product Owner", approved_at: "<exact PO decision timestamp>" }
   ```
   — no coverage floor or extra-requirement value duplicated into the registry (both derive from
   Chapter 13 §13.4's own Locked table for the pinned tier name, per the registry's own
   field-reference convention already used for every prior pin).
2. Bump `module-registry.yaml`'s `version` (currently `"1.7"` at this boundary) — a genuine
   semantic field addition, not a mechanical/wording-only change, following the exact precedent
   already established for every prior `quality_tier` addition in this file.
3. Revert `package_lifecycle` from `Consolidated Stable` (current value at this boundary) to
   `candidate` — same precedent as every prior semantic amendment to this file — pending a future
   Review A + reconsolidation transaction.
4. Add a banner entry at the top of `module-registry.yaml` documenting the transaction, following
   this file's own established convention.
5. **Not** touch `python/context-aggregator/**`, any Domain Contract, any ADR, Chapter 13, or any
   other module's fields.
6. **Not** run or claim any Chapter 13 Quality Gate result — pinning the tier makes the coverage
   floor *applicable*; it does not make it *evaluated*.

None of the above is performed by this transaction.

## §13. Review A / Risk Classification / Concerns / Risks noted

| Reviewer | Role | Boundary reviewed | Findings | Risk | Verdict |
|---|---|---|---|---|---|
| — | AI Technical Architect | `0dbd9f44fd9fa85dbf1ccba984608380273dbade` | Not yet reviewed | — | — |

## §14. Product Owner decision

**PENDING.**

---

**Terminal state of this transaction: `QUALITY_TIER_CANDIDATE_READY_FOR_REVIEW_A`.**
