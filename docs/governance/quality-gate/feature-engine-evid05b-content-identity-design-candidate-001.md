# Feature Engine — `P3-FEATURE-QG-EVID-05(b)` Persisted Content-Identity Design Candidate 001

```yaml
status: CANDIDATE / NOT EFFECTIVE — ADR_REQUIRED, STOPPED AT DESIGN/SCOPE PER INSTRUCTION
artifact_id: feature-engine-evid05b-content-identity-design-candidate-001
created_for: >
  Designing (not implementing, not authoring the ADR) one governed
  architecture for P3-FEATURE-QG-EVID-05(b) — I-5 persisted content-identity
  evidence for the Input Contract / Stream Registry artifacts a Feature
  computation used, closing the structural-unverifiability gap
  feature-engine-chapter13-remediation-plan-001.md's EVID-05 row and §2
  correction 2 already named.
transaction_kind: DESIGN ONLY
production_changed: false
tests_changed: false
schema_changed: false
adr_035_edited: false
evid_05_closed: false
repository_head_at_authoring: c220b62a097aa036413865ff0222c5c136f6f05f
```

## 0. Preserved lifecycle state (unchanged by this candidate)

```text
P3-FEATURE-QG-EVID-03:        CLOSED — PASS — REVIEW A VALIDATED (unaffected).
P3-FEATURE-QG-EVID-05(a):     SATISFIED — Review A validated (unaffected).
P3-FEATURE-QG-EVID-05 overall: OPEN / blocking — unchanged, NOT closed by
                               this candidate (part (b) is designed here,
                               not implemented or approved).
P3-FEATURE-QG-EVID-04/-06/-07/-08: OPEN / blocking (unaffected).
Overall Feature Engine Chapter 13 Quality Gate: FAIL — evidence (unaffected).
ADR-035: Approved, NOT edited in place, NOT superseded, NOT reopened.
Feature module approval: NOT APPROVED. Phase 3 Approval Gate: NOT OPENED.
LIVE: NOT_AUTHORIZED.
```

## 1. Authority resolved (independently, this transaction)

- **Constitution I-5** (`02-platform-invariants.md`): Replay execution reads only already-saved events + materialized/immutable artifacts; a checksum-bearing, content-addressed reference is the sanctioned mechanism for large/external dependencies; *"Coi content-addressed reference là đủ để đảm bảo offline"* is explicitly named a **prohibited** shortcut — materialization alone is not proof; the checksum must actually be checked.
- **Chapter 8 §8.1.1** (`08-event-model.md`), rule 5, *Verifiable content identity*: **"Bắt buộc là verifiability, không phải một field cụ thể; identity có thể nằm ở run manifest thay vì lặp trên mọi event."** — Chapter 8 itself does not mandate that content identity live inline on every event; a resolvable-elsewhere identity satisfies the rule. §8.3.1 repeats the identical pattern for the Stream Registry specifically ("checksum không cần lặp trong mọi event, nhưng event hoặc run manifest phải truy được tới content identity bất biến"). This is the controlling authority for the option analysis below.
- **Chapter 8 §8.5/§8.5.1** (canonical `replay_cursor`): a **closed**, five-field cardinality table (`recorded_time`, `input_contract_ref {contract_id, contract_version}`, `stream_registry_version`, `lifecycle_frontier`, `stream_positions`) — content identity is not one of the five fields, and §8.5.1's own table is the validator authority for what a cursor must/only carries.
- **ADR-035** (Approved v0.2): `computation_cursor`'s value is the canonical §8.5 Replay Cursor **verbatim** — "not a second, Feature-local, near-equivalent schema" (Alternative 2, rejected). Required on every `FeatureComputed`/`FeatureFactInvalidated`, original and replacement alike, captured independently at each fact's own evaluation. ADR-035's own "Fail-closed consequence" paragraph already anticipated today's exact gap: *"a `computation_cursor` value cannot genuinely satisfy §8.1.1's five conditions... until the referenced Stream Registry/Input Contract artifacts are genuinely persistently resolvable"* — and explicitly scoped closing that gap out to follow-on work, never claiming to close it itself.
- **`feature-engine-chapter13-remediation-plan-001.md`**, EVID-05 row + §2 correction 2: confirms by direct code reading (not assumption) that `VerifiedInputContractAuthority` DOES compute `input_contract_content_id`/`stream_registry_content_id`, but they are "not threaded into the persisted, replay-relevant cursor" — precisely the gap this candidate designs a closure for.
- **Current `feature.md`** (domain contract, §3/§4): zero mention of `content_id`/`checksum`/"content identity" anywhere — confirms the domain contract itself has not yet anticipated this evidence at all; any closure requires a domain-contract amendment regardless of which architecture is chosen.
- **Current `VerifiedInputContractAuthority`** (`contracts.py`): frozen dataclass, no public constructor (Review-A round-5), fields include `input_contract_content_id: str` and `stream_registry_content_id: str` — both SHA-256 hex digests of the real artifact bytes, computed exactly once in `authority_resolver.resolve_input_contract_authority_from_repository`, at Replay-preparation/construction time, never recomputed by any runtime handler (confirmed independently in the EVID-05(a) transaction).
- **Current `ComputationCursor`** (`contracts.py`): exactly the five §8.5.1 fields, nothing more — confirmed byte-for-byte matching ADR-035's schema, no Feature-local additions exist today.

## 2. Options evaluated

### Option 1 — Extend the canonical Chapter-8 `replay_cursor` itself with artifact content identities

| Criterion | Assessment |
|---|---|
| I-5 compliance | Would satisfy it, but by over-reach |
| Fail-closed before execution | Achievable |
| Event-schema impact | **Platform-wide** — every event carrying any `replay_cursor`-shaped value (`decision_context_cursor` per §8.4, any future Decision/Strategy/Risk/Execution consumer) inherits the new fields, whether or not that consumer's own artifacts even have a content-identity story yet |
| Chapter-8/ADR-035 compatibility | Technically "compatible" (ADR-035 says "verbatim", so it would inherit automatically) but requires reopening **Locked** Chapter 8 §8.5's own closed cardinality table — a chapter-level amendment, not a Feature-scoped decision |
| Cross-module blast radius | **>1 module, platform-wide** — squarely Chapter 0 §4b's ">1 module" ADR trigger on its own, independent of the Event-Schema trigger |
| Backward compatibility | Every existing/future `replay_cursor` consumer must be revisited |
| Competing-cursor risk | None (correctly reuses one shape) but the *scope* of the change is not Feature's to make |
| Checksum source | Same `authority_resolver.py` values, but now generalized to an artifact taxonomy Feature does not own |
| Verdict | **Rejected** — correct mechanism, wrong owner/scope. Chapter 8 is Locked and centrally owned (I-12); a Feature-scoped remediation cannot unilaterally decide this for every current and future consumer. Not minimum-scope. |

### Option 2 — Keep canonical Replay Cursor unchanged; persist content-identity evidence adjacent to it, directly on `FeatureComputed`/`FeatureFactInvalidated`

| Criterion | Assessment |
|---|---|
| I-5 compliance | Directly satisfies §8.1.1 rule 5's own sanctioned pattern (identity travels with the artifact-referencing record) |
| Fail-closed before execution | Replay preparation re-resolves the exact `{contract_id, contract_version}`/`stream_registry_version` `computation_cursor` names, recomputes `input_contract_content_id`/`stream_registry_content_id` from the real current artifact bytes (identical mechanism `authority_resolver.py` already implements), and compares against the fact's own persisted evidence — mismatch or missing artifact fails closed **before** Replay execution starts |
| Event-schema impact | **Feature-scoped only** — one new required sibling payload field on `FeatureComputed`/`FeatureFactInvalidated` (`feature.md` §3/§4), exactly the same class of change ADR-035 itself made for `computation_cursor` |
| Chapter-8/ADR-035 compatibility | `computation_cursor`'s own shape is untouched — the new field is a sibling, never nested inside/merged into it; ADR-035's Alternative-2 rejection (no Feature-local near-copy *cursor*) does not apply, since this is not an ordering/visibility concept at all, it is artifact-identity evidence |
| Cross-module blast radius | **None** — Chapter 8, Decision, Structure, Regime all unaffected; no other module's event schema or dependency graph changes |
| Backward compatibility | Same posture ADR-035 itself already established: Feature Engine has zero production events today (Phase 3, pre-production) — a new required field is a forward schema-versioning decision (Chapter 10), not a live migration |
| Competing-cursor risk | None — structurally and namespace-separate from `computation_cursor`; records "which artifacts were used", not "what ordering position was reached" |
| Checksum source | Verbatim reuse of `VerifiedInputContractAuthority.input_contract_content_id`/`.stream_registry_content_id` — no new hashing mechanism invented |
| Verdict | **Recommended** — smallest blast radius that genuinely satisfies every required invariant; reuses existing, already-computed authority values; touches only artifacts Feature already owns (its own event payload) |

### Option 3 — Extend/redefine the Input Contract / Stream Registry reference mechanism so content identity is carried by the referenced artifact's own identity

| Criterion | Assessment |
|---|---|
| I-5 compliance | Superficially attractive (matches §8.1.1 rule 5's "or equivalent" framing most literally) |
| Fail-closed before execution | **Does not actually solve the problem.** Artifact-level content identity is already fully computable today — `authority_resolver.py` already hashes the artifact's *current* bytes on every resolution. What is missing is not "can content identity be computed", it is "was THIS EXACT content identity, as it stood at ORIGINAL computation time, durably recorded so a later replay can compare against it." Redefining the artifact's own identity mechanism does not create that historical comparison point — it would still need an Option-2-shaped persisted record layered on top, making this strictly more work for no closure benefit |
| Event-schema impact | None directly, but... |
| Chapter-8/ADR-035 compatibility | Input Contract/Stream Registry are Chapter-8-owned artifact **classes** (§8.1.1's own named taxonomy) — redefining how their identity/versioning works is not Feature's artifact to redefine at all |
| Cross-module blast radius | **>1 module, platform-wide** — every current/future consumer of these two artifact classes (Structure, Regime, any future Decision/Strategy consumer) is affected |
| Backward compatibility | Any existing `{contract_id, contract_version}`/`registry_version` reference semantics platform-wide would need re-evaluation |
| Competing-cursor risk | N/A |
| Checksum source | Same underlying bytes, but now via a mechanism Feature does not own |
| Verdict | **Rejected** — larger blast radius than Option 1 in ownership terms (touches artifacts Feature doesn't own) while not even closing the actual gap (no historical comparison point without also doing Option 2's work) |

**No better authority-compliant option was identified beyond these three** — a fourth "invent a new authoritative artifact/event type carrying content-identity provenance" mirrors ADR-035's own Alternative 3 (a separate referenced provenance artifact), rejected there for the same reason it would fail here: it adds an entire new authoritative-artifact class, causation hop, and stream/registry surface for information that fits directly on the fact that already needs it (Chapter 8 §8.4 made the identical choice for `decision_context_cursor` — embed, don't create a referenced side-channel).

## 3. Recommended minimum-scope architecture (Option 2)

A new, **required**, sibling payload field on `FeatureComputed`/`FeatureFactInvalidated` — never inside `ComputationCursor`, never replacing or duplicating any of its five canonical fields:

```yaml
# sibling to computation_cursor, NOT part of it — a distinct concept
# (artifact content-identity evidence, not ordering/visibility)
computation_dependency_content_evidence:
  input_contract_content_id:    # verbatim = VerifiedInputContractAuthority.input_contract_content_id
                                 #   SHA-256 of the exact Input Contract artifact bytes
                                 #   resolved for computation_cursor.input_contract_ref
  stream_registry_content_id:   # verbatim = VerifiedInputContractAuthority.stream_registry_content_id
                                 #   SHA-256 of the exact Stream Registry artifact bytes
                                 #   resolved for computation_cursor.stream_registry_version
```

**Invariants satisfied:**

- **Content identity from exact immutable bytes** — both values are the same SHA-256-of-real-artifact-bytes `authority_resolver.py` already computes today; no new hashing mechanism, no invented algorithm.
- **Binds the exact artifacts used** — persisted verbatim from the same `VerifiedInputContractAuthority` instance the computation engine resolved and cached for *this exact* fact's evaluation; not a global/shared value, not recomputed after the fact.
- **Version/name equality alone is insufficient** — `computation_cursor.input_contract_ref`/`stream_registry_version` already carry version/name; this field adds the missing content proof, so a version string that was silently repointed at different bytes (a §8.1.1 rule-2 violation) becomes detectable instead of structurally unverifiable.
- **Replay preparation resolves + verifies** — re-resolves `{contract_id, contract_version}`/`stream_registry_version` named by the fact's own `computation_cursor`, recomputes both content IDs from the current real bytes, and compares against `computation_dependency_content_evidence`; identical mechanism to what `authority_resolver.py` already does, plus one new comparison step.
- **Mismatch/missing artifact fails closed before execution** — a comparison failure (or unresolvable artifact) is a Replay-preparation failure; Replay execution never starts, consistent with I-5's Verification text and unaffected by the EVID-05(a) transaction's existing self-contained-execution proof (the new check happens strictly *before* the network/filesystem cut EVID-05(a) already proves, never during execution).
- **Replay execution performs no external resolution** — unaffected; the new evidence is read from the already-persisted fact / already-materialized authority, exactly like `computation_cursor` itself is read today.
- **Original and replacement facts each preserve their own evidence** — required on both `FeatureComputed` and `FeatureFactInvalidated`, captured independently at each fact's own evaluation, mirroring `computation_cursor`'s own existing "never inherited/copied from the fact it supersedes" discipline (ADR-035, `contracts.py` docstrings).
- **No process-local pointer qualifies** — both values are content hashes of durable, versioned artifact bytes, not object identity/memory references; identical durability class to `computation_cursor`'s own fields.

**Cross-module impact:** none. Chapter 8's canonical `replay_cursor` (§8.5), ADR-035's decision content, Structure/Raw-Regime/other Compute Engines, and any future Decision/Strategy/Risk/Execution module are all unaffected and unreferenced by this candidate.

**Event/schema impact:** one new required field on `FeatureComputed`/`FeatureFactInvalidated` (`feature.md` §3/§4) — the same class and scale of change ADR-035 itself made for `computation_cursor`, and ADR-034 made for `invalidation_cause`.

## 4. Fresh Chapter 0 §4b ADR-scope run

| Trigger checked | Result |
|---|---|
| Event Schema change | **YES** — a new required payload field on `FeatureComputed`/`FeatureFactInvalidated` (`feature.md` §3/§4) is precisely "thay đổi Event Schema", the identical trigger ADR-034 (`invalidation_cause`) and ADR-035 (`computation_cursor`) both cited for themselves |
| Modification/extension of Approved ADR-035 semantics | **NO** — `computation_cursor`'s shape, meaning, and the canonical §8.5 reuse are untouched; the new field is a sibling on the *event*, not a change to the *cursor* |
| Canonical Chapter-8 Replay Cursor ownership | **NO conflict** — Option 2 was chosen specifically because it does not touch §8.5's closed five-field table or any other `replay_cursor` consumer (this is exactly why Options 1/3 were rejected) |
| >1 module / platform-wide effect | **NO** — confirmed no cross-module blast radius (§3 above); this is a Feature-only Event Schema addition |

**Result: `ADR_REQUIRED`** — solely on the independently-sufficient Event Schema trigger (disjunctive reading, same precedent ADR-034/035 already established), even though this candidate's chosen architecture deliberately avoids every other possible trigger (no ADR-035 edit, no Chapter-8 ownership conflict, no >1-module effect). Adding required payload structure to an authoritative Feature event has no non-ADR path, per the same reasoning ADR-035 §"Scope classification" already recorded for itself.

**Per instruction: STOPPING at this design/scope candidate.** No ADR is authored in this transaction. No `feature.md` amendment, no `contracts.py`/schema implementation, no test authored. `EVID-05` remains OPEN; `EVID-05(b)` remains unresolved pending a future, separate ADR-authoring transaction that would formally decide this (or a superior) architecture.

## 5. Not performed by this candidate (explicit)

```text
No ADR authored. No feature.md amendment. No contracts.py/event-schema
change. No test authored or modified. No mutation run. No formal
Chapter-13 evaluation. ADR-035 not edited, not superseded, not reopened.
EVID-05 not closed; EVID-05(a)'s SATISFIED disposition is unaffected and
unrevisited.
```
