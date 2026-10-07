---
id: feature-output-compatibility-policy-triage-001
title: "Feature Output Event Contract — Format-Specific Reader/Schema Policy Architecture Triage"
kind: analysis
version: "0.1"
status: Draft
owner: Product Owner
generated_at: "2026-10-07"
---

# FEATURE-OUTPUT-COMPATIBILITY-POLICY-TRIAGE-001

Bounded architecture-triage artifact, produced under the M3 Feature Future Dependency Authority
workstream. Does NOT create ADR-050 or any other ADR. Does NOT modify Feature v1.0 Published
artifacts, Feature v1.1 Draft candidates, `ADR-038`/`ADR-039`/`ADR-048`, or any Structure/Regime/
Context file. Does NOT choose a new architecture policy. Does NOT perform Review A. Does NOT merge
`main`.

## 0. Boundary and fresh-verification record

Starting boundary: `main == origin/main == 35535aac9f09f1c8ca8ad83495887860bcef578e`, fresh-fetched
and confirmed before this transaction; working tree clean of in-progress change (only pre-existing
untracked `.DS_Store`/`CLAUDE.md` noise present). Executed on isolated branch
`workstream/m3-feature-future-dependency-authority-triage`.

Fresh-read in full this transaction: `docs/adr/ADR-038.md` (Approved v0.1); `docs/adr/ADR-039.md`
(Approved v0.1); `docs/adr/ADR-037.md` (Approved v0.1, header + Compatibility/versioning section);
`docs/constitution/10-compatibility-capability-contract.md` (Locked v2.7) §10.1–§10.5, §10.7, §10.9;
`docs/governance/execution-rules.md` §G-ADR; `docs/constitution/00-governance.md` §4b;
`docs/project/feature-causal-state-dependency-version-impact-001.md` v0.1 (the artifact whose
conclusion Review A did not accept); `docs/domain/feature.md` v0.6 (compatibility-relevant
sections, §3/§4 header prose); both Published Feature v1.0 Event Contracts (blob
`9e1da0ac1e72403a780ff16e0d06ed68354da623` for `feature-computed`, `7015fa4c09b0fa6993c1324858719ebca76d260d`
for `feature-fact-invalidated` — confirmed identical to the version-impact artifact's own recorded
blobs, no drift); both Draft Feature v1.1 candidates (confirmed `causal_state_dependency_declaration`
is placed as a top-level sibling field, before `payload_shape`, in `feature-computed/v1.1.yaml` —
spot-verified by direct grep, not merely trusted from the prior artifact's own claim).

Repository-wide fresh search performed (not inherited from memory) for ANY existing
format-specific reader/schema compatibility policy applicable to Feature Output Event Contracts:
searched every `.md`/`.yaml`/`.yml` under `docs/` for `JSON Schema`, `Avro`, `Protobuf`, `.proto`,
`unknown field`, `additionalProperties`, `tolerant reader`, `reader policy`, `deserializ` (full
command and result set in §2 below).

## 1. Question

Does an already-authoritative Feature-output reader/schema policy exist that closes the
prerequisite `ADR-038`/`ADR-037` both explicitly named (a format-specific — JSON Schema/Avro/
Protobuf-or-equivalent — reader policy for the Feature Output Event Contracts, deferred by Chapter
10 §10.3.1 to "Domain Contract/Phase 1" authority, not yet authored anywhere)?

## 2. Search performed and result

```text
grep -rniI "json schema|avro|protobuf|\.proto\b|unknown field|unknown-field|additionalProperties|
  additional_properties|strict schema|tolerant reader|forward compat.*reader|reader policy|
  deserializ" docs/ --include="*.md" --include="*.yaml" --include="*.yml" -l
```

Matched files inspected individually, with result:

| File | Relevant content | Is this an authoritative reader/format policy for Feature Output Event Contracts? |
|---|---|---|
| `docs/adr/ADR-037.md` | States explicitly: backward compatibility "depends entirely on that old consumer's own reader/format policy (permissive... versus strict...) — a controlling policy §10.3.1 itself defers to... which does not currently exist for these Event Contracts." | NO — confirms absence, does not supply it |
| `docs/adr/ADR-038.md` | Same absence, named as a downstream Domain Contract/Phase-1 prerequisite (Consequences item 0) | NO — confirms absence, does not supply it |
| `docs/constitution/10-compatibility-capability-contract.md` §10.3.1 | "Quy tắc theo từng format cụ thể (JSON Schema, Avro, Protobuf...) thuộc Domain Contract/Phase 1 — Constitution chỉ khóa semantic trên." | NO — Constitution explicitly defers this to a lower authority tier it does not itself supply |
| `docs/architecture/api-architecture.md` §8 | "Format-specific rule-set (JSON Schema/OpenAPI/GraphQL/protobuf...) KHÔNG author — deferred tới khi một concrete schema artifact..." | NO — a DIFFERENT subsystem (Package 1.4 command/query API surface, not Event Contracts), and explicitly not authored there either |
| `docs/engineering/config.md` | Lists "config schema technology (JSON Schema, protobuf...)" under its own explicit out-of-scope/deferred list | NO — unrelated subsystem (runtime config), explicitly deferred |
| `docs/engineering/coding-standard.md`, `docs/engineering/testing.md` | Incidental mentions of generated protobuf/gRPC stubs and JSON-schema-based test assertions, no policy declaration | NO — not a reader/format policy for Feature Output Event Contracts |
| `docs/domain/feature.md` | No reader/format policy; §3/§4 header prose applies §10.3.1's own format-independent "required-no-fallback→breaking" rule to `computation_dependency_content_evidence` specifically (a *payload_shape* field), explicitly stating that classification does NOT need a reader/format policy because it is forced regardless of reader strictness | Confirms the one case that IS already decidable without the policy (see §4 below) — NOT itself the missing policy |
| `docs/adr/ADR-022.md`, `docs/adr/ADR-047.md`, `docs/MANIFEST.md`, `docs/CHANGELOG.md`, `docs/domain/account.md`, `docs/domain/instrument.md`, `docs/project/milestone.md`, `docs/project/context-upstream-state-dependency-derivation-001.md` | Incidental/unrelated matches (different ADRs' own schema-unrelated prose, bookkeeping mentions) | NO |

Implementation code checked for completeness (NOT treated as authority per this task's own
instruction — no governance artifact anywhere cites `python/feature-engine/src/feature_engine/contracts.py`
as an authoritative reader/format policy; it is plain Python `dataclass` domain objects with no
declared unknown-field-tolerance or wire-serialization discipline, and is not elevated to policy
status by any ADR, Domain Contract, or Constitution chapter).

**Result: no match found anywhere in the repository that constitutes an authoritative,
format-specific (JSON Schema/Avro/Protobuf-or-equivalent) reader/schema compatibility policy for
the Feature Output Event Contracts.**

## 3. Answer to Question 1

**NO.** No already-authoritative Feature-output reader/schema policy exists. `ADR-038`'s own named
prerequisite (Consequences item 0) remains unresolved, exactly as `ADR-038` and `ADR-037` both
state in their own text, independently reconfirmed by this fresh, repository-wide search — not
merely re-asserted from memory.

## 4. What IS already resolved — narrow, does not reach this delta

For completeness, and to avoid overstating the gap: `feature.md` v0.6's own text (line 43,
fresh-read) already correctly classifies a DIFFERENT delta — `ADR-037`'s `computation_dependency_content_evidence`,
a *payload_shape* field — as `BREAKING`, explicitly without waiting for the reader/format policy,
because §10.3.1's own minimal classification rule ("thêm element **required** không có fallback →
breaking") is forced regardless of reader strictness: old data simply lacks the value, so no reader
implementation — permissive or strict — can satisfy a required-field read against it. This
format-independent case is already closed and is NOT reopened by this triage.

`causal_state_dependency_declaration` is categorically different from that already-closed case: it
is not a `payload_shape` element at all (confirmed by direct inspection of both Draft v1.1
candidates, §0) — it is a top-level Event-Contract-artifact field, per `ADR-048`'s own framing,
sibling to `event_class`/`allowed_streams`/`merge_constraints`. The forced, format-independent
"required-no-fallback" rule that closed the `computation_dependency_content_evidence` case does not
mechanically transfer to this one, because this field is never missing-or-present *in any event
instance's own data* — it never appears there at all, in either version. Whether that fact is
itself sufficient to resolve the question is precisely the missing decision surface below — this
triage does not assume it is.

## 5. Precise missing decision surface

Two distinct, nested questions, neither answered by any existing authority found in §2:

**(a) The pre-existing, platform-wide gap `ADR-038`/`ADR-037` already named:** no format-specific
(JSON Schema/Avro/Protobuf-or-equivalent) reader/schema compatibility policy exists for the Feature
Output Event Contracts' own payload data — i.e., whether an old reader of `feature-computed`/
`feature-fact-invalidated` event *instances* tolerates an unrecognized field it does not look for,
versus validating against a closed/strict field set. This governs every future `payload_shape`
delta's backward-compatibility evaluation, not only this one.

**(b) A narrower, logically-prior question this specific `ADR-048` delta newly raises, not
previously named by any existing ADR:** does `ADR-038`'s own backward-only commitment — explicitly
scoped by its own text to "dữ liệu" (DATA a consumer reads/validates) — even extend to a top-level
Event-Contract-*artifact* field that is never serialized into any event instance's own payload
bytes, or is such a field categorically outside that commitment's scope entirely (in the same sense
that a change to `event_class`/`allowed_streams`/`merge_constraints` — also artifact-level, also
never payload data — has never been treated as a "breaking data change" anywhere in this
repository's history, though no existing text states this exemption explicitly either)? No
Constitution chapter, Approved ADR, or Domain Contract answers (b) one way or the other. Resolving
(b) in the "exempt" direction would narrowly unblock this specific delta's classification without
first requiring the full, platform-wide policy (a). Resolving (b) in the "not exempt" direction
would mean (a) remains the controlling, larger prerequisite exactly as `ADR-038` already states.

**Concrete fact sharpening (b)'s stakes, fresh-confirmed this transaction, not previously recorded
in the version-impact artifact accurately:** `docs/architecture/input-contracts/context-market-input.yaml`
(the real, already-registered consumer `context-aggregator`'s own Input Contract, Draft) already
declares `causal_closure_policy: {mode: declared-state-dependencies, dependency_authority:
per_effect_event_contract}` over `included_streams` that explicitly include
`feature-engine-feature`. This directly contradicts the version-impact artifact's own §3.3 claim
that `causal_state_dependency_declaration` is "a consumption mode no currently-registered consumer
of Feature's events uses" — `context-aggregator`'s own Draft Input Contract already structurally
commits to exactly that mode, for exactly Feature's stream. Per Chapter 8 §8.2.3's own
`declared-state-dependencies` mode requirement (fresh-cited, not re-derived here), that Input
Contract cannot be satisfied/validated for the `feature-engine-feature` stream until a Feature
Event Contract version actually carries `causal_state_dependency_declaration` — this is a genuine
operational dependency on the field's eventual existence, not an inert, nobody-reads-it addition.
This does not by itself answer (b) — it raises the cost of leaving (b) unresolved and is reported
here as a correction to the prior artifact's own factual claim, not as this triage's own resolution
of the architecture question.

## 6. Affected modules/contracts

- `feature-engine` — producer of `feature-computed`/`feature-fact-invalidated` (both `contract_id`s
  affected identically).
- `context-aggregator` — sole registered consumer (`docs/domain/context-map.yaml`, `ADR-038`'s own
  finding, independently reconfirmed); its own Draft Input Contract's `declared-state-dependencies`
  mode is the concrete, already-registered dependency sharpening question (b) above.
- Platform-wide, not Feature-specific in its eventual resolution scope: every current Candle/
  Structure/Regime Event Contract (all currently `status: Draft`, never yet Published) will face
  the identical (a)/(b) question the first time any of them needs a post-publication `ADR-048`
  delta — Feature is simply the first `contract_id` pair already `Published` and therefore the
  first to encounter it concretely. Resolving (a) and/or (b) here sets platform-wide precedent, not
  a Feature-local one.

## 7. ADR Scope classification (Chapter 0 §4b / `G-ADR`)

```text
G-ADR-004 inflation/scope self-check:
1. Existing authority/alignment resolves this without a new decision? NO -- confirmed by the
   repository-wide search in §2: no format-specific reader/schema policy exists anywhere; ADR-037/
   ADR-038 both independently and explicitly name this exact prerequisite as absent; Chapter 10
   §10.3.1 explicitly defers it to a lower authority tier (Domain Contract/Phase 1) neither
   Constitution nor any current Approved ADR occupies.
2. Genuine architecture decision, not cheaply reversible? YES for both (a) and (b). (a) governs
   backward/forward compatibility classification for every future Feature Output Event Contract
   payload delta -- a wrong choice, once consumers build against an assumed tolerance behavior,
   requires migrating every such consumer to correct. (b) fixes an interpretive rule for every
   future Event-Contract-artifact-level metadata field (ADR-048-style) across every current and
   future Event Contract platform-wide -- equally hard to reverse once a validator/producer
   implementation is built against either reading.
3. Chapter 0 §4b trigger fires independently? YES -- "thay đổi Event Schema" (this is squarely a
   compatibility-classification-policy question for an Event Schema axis, Chapter 8 §8.2.5/Chapter
   10 §10.3) and ">1 module" (feature-engine producer, context-aggregator consumer confirmed above;
   platform-wide for Candle/Structure/Regime's own future identical situations) both fire,
   independently of each other.
4. Authored merely to "complete" ADR-037/ADR-038's own prior open item (G-ADR-003)? NOT SOLELY --
   ADR-038 itself already named prerequisite (a) as separate, later, governed work, which alone
   would not justify a new ADR under G-ADR-003's own rule against ADR-chaining. However, items 1-3
   above each independently and freshly confirm a live, currently-blocking decision gap (Review A's
   own rejection of the premature version-impact conclusion is the concrete trigger event), and
   question (b) was never named by ADR-037/ADR-038 at all -- it is a new question this ADR-048
   delta itself raises, not inherited from either ADR's own unfinished business.
Result: ADR_REQUIRED -- confirmed by genuine §4b triggers (Event Schema change, >1-module impact),
  not by "repeated correction" or any other ADR-045 Risk-Classification-only criterion (that
  distinction itself follows the corrected discipline ADR-049 v0.2 established on this same branch
  of work: Risk Classification criteria are never cited as independent ADR Scope triggers).
```

## 8. Risk classification (`ADR-045`)

```text
class: R2
reason: >
  Authority/source-of-truth semantics (ADR-045's own R2 criterion) -- this decision fixes how
  compatibility/breaking-change classification applies to an entire category of future Event
  Contract deltas (governance-metadata-only additions outside payload_shape), a platform-wide
  source-of-truth question, not a single-artifact judgment call. Cross-module contract/dependency
  change with significant blast radius (feature-engine/context-aggregator today; every future
  Candle/Structure/Regime Event Contract's own identical future situation). Review A finding
  conflicting authority/evidence or unresolved ambiguity -- an explicit ADR-045 R2 trigger -- is
  exactly what happened here: Review A did not accept the prior bounded analysis's own concrete
  compatibility conclusion precisely because this authority gap remains open. Difficult/expensive
  to reverse once a Feature v1.1 (or any later Event Contract) is Published and real consumers
  advance their bindings under an assumed, ungoverned classification.
```

Per `ADR-045`, R2 is never delegated and never automatically cross-checked —
`RECOMMEND OPTIONAL INDEPENDENT CROSS-CHECK`, Product-Owner-only routing. This triage does not
perform that optional cross-check and does not record a Product Owner decision — both out of scope
for this transaction.

## 9. Smallest next governed action

A bounded ADR candidate (new ADR identity, NOT selected, NOT authored, NOT numbered by this
transaction) should resolve question **(b) first**, as the narrower, logically-prior question:
does an Event-Contract-artifact-level declarative field addition outside `payload_shape` — never
serialized into any event instance's own payload bytes — engage `ADR-038`'s own "dữ liệu"-scoped
backward-only commitment at all, or is it categorically outside that commitment's scope (consistent
with how `event_class`/`allowed_streams`/`merge_constraints` changes have implicitly been treated
throughout this repository's history, though never yet tested)?

- If (b) resolves **"exempt"**: the Feature `v1.1` candidates' compatibility classification is
  narrowly unblocked without needing the full platform-wide reader/format policy (a) first; (a)
  remains separately, later governed work exactly as `ADR-038` already scoped it, for the next
  `payload_shape`-touching delta.
- If (b) resolves **"not exempt"**: question (a) — establishing the actual Domain-Contract/Phase-1
  format-specific reader/schema policy `ADR-038`/`ADR-037` both already named — becomes the
  controlling, larger prerequisite, and must be resolved before any concrete backward-compatibility
  conclusion for this delta (or any future `causal_state_dependency_declaration` addition to an
  already-Published Event Contract) can be honestly stated.

This triage does not select between these two outcomes — doing so would be choosing a new
architecture policy, outside this transaction's own scope and explicitly forbidden by the governing
task.

## 10. Forbidden-scope confirmation

- `docs/architecture/event-contracts/feature-computed/v1.0.yaml`,
  `docs/architecture/event-contracts/feature-fact-invalidated/v1.0.yaml` — unmodified, blobs
  reconfirmed identical to those recorded in the version-impact artifact (§0).
- `docs/architecture/event-contracts/feature-computed/v1.1.yaml`,
  `docs/architecture/event-contracts/feature-fact-invalidated/v1.1.yaml` — unmodified (read-only
  inspection, §0).
- `docs/adr/ADR-038.md`, `docs/adr/ADR-039.md`, `docs/adr/ADR-048.md` — unmodified.
- No ADR authored, no ADR number selected or reserved.
- No Structure/Regime/Context file touched.
- No governance (Constitution, Global Execution Rules, Phase rules, Lean Ride Operating Model) file
  touched.
- No Review A performed.
- `main` not merged, not advanced, not modified.

## 11. Terminal state

**`ARCHITECTURE_ESCALATION`**

- Exact question: see §1/§5 (questions (a) and, newly, (b)).
- Exact conflicting/missing authorities: `ADR-038`/`ADR-037` (name prerequisite (a), do not supply
  it); Chapter 10 §10.3.1 (defers (a) to an authority tier it does not itself occupy); no existing
  ADR/Constitution/Domain Contract addresses (b) at all.
- Affected artifacts/modules: see §6 (`feature-engine`, `context-aggregator`, and platform-wide
  precedent for Candle/Structure/Regime's own future identical situations).
- Reversible local option(s): none that resolve the classification question itself without
  deciding (b) or (a) — the only fully reversible local action is what this triage already took:
  leaving both Feature v1.1 candidates `status: Draft`, unpublished, with no compatibility
  conclusion asserted, pending the governed decision this escalation requests.
- Why existing authority cannot decide it: confirmed by exhaustive fresh repository search (§2) —
  no format-specific reader/schema policy exists anywhere, and no existing text resolves the
  narrower artifact-level-field-scope question (b) this specific `ADR-048` delta newly raises.
