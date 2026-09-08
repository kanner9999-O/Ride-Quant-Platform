# Feature Engine — `P3-FEATURE-QG-EVID-05(b)` Persisted Content-Identity Design Candidate 001

> **Bounded correction — `P3-FEATURE-QG-EVID05B-A-MAJ-01`**, addressed/remediated pending Review A re-review (not self-closed by this correction transaction): the original candidate omitted a genuine fourth alternative — a durable run/replay-manifest content-identity binding — even though Chapter 8 §8.1.1/§8.3.1 explicitly permit content identity to live off-event. **Corrected:** Option 4 added and independently assessed (§2); the prior recommendation's implicit claim that content hashes must be copied onto every Feature fact is corrected (§2.1); the recommended architecture changes from Option 2 to Option 4 (§3); Chapter 0 §4b is rerun against the corrected recommendation, independently of the discarded Option 2 (§4), yielding `ADR_OPTIONAL` rather than the prior `ADR_REQUIRED`. **No change to:** the finding this candidate addresses (`P3-FEATURE-QG-EVID-05(b)`), `EVID-05(a)`'s `SATISFIED` disposition, ADR-035 (still not edited/superseded/reopened), or the `DESIGN ONLY` transaction kind — no ADR authored, no production/schema/test implementation, `EVID-05` still not closed.
>
> `P3-FEATURE-QG-EVID05B-A-MAJ-01: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`

```yaml
status: CANDIDATE / NOT EFFECTIVE — ADR_OPTIONAL (corrected), PENDING BOUNDED REVIEW A RE-REVIEW
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
bounded_correction_001:
  applied_at_repository_head: ef63daf5a302ad8b174fe95d44249e5defc613ac
  corrected_candidate_blob_before_correction: 33a1ea6ddb95b6b744d33b490ce35a76c13405ae
  reviewer_findings_addressed:
    - id: P3-FEATURE-QG-EVID05B-A-MAJ-01
      status: "REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW"
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
- **Repository precedent for run-manifest/off-event content-identity evidence (bounded correction — `P3-FEATURE-QG-EVID05B-A-MAJ-01`):** independently inspected. `raw_regime_engine.regime.RegimeDefinition.content_identity()` computes a deterministic SHA-256 fingerprint over the definition's full canonical content, and its own docstring states it is *"suitable as external run-manifest evidence"* — but the SAME docstring explicitly disclaims inventing any registry/storage/lifecycle authority: *"This module invents no definition registry/storage/lifecycle authority — that remains deferred by regime.md §19/§20."* This is a hash-producing **capability**, not an implemented manifest artifact. A repository-wide search for `run_manifest`/`replay_manifest` found zero authoritative schema anywhere (no Constitution chapter, Domain Contract, or ADR defines a "Run Manifest"/"Replay Manifest" artifact type, its versioning, or its resolution mechanism) — **no platform run-manifest schema is claimed to exist**, consistent with the instruction not to assume one. The closest EXISTING, already-authoritative, already-governed mechanism performing this general class of function (durably binding an artifact's identifier to a verifiable content identity, git-tracked, versioned via its own `manifest_version`, updated in lockstep with every tracked document's edit per its own stated rule: *"Mỗi khi một file trong `/docs` đổi version/status, Manifest phải cập nhật cùng lúc, nếu không bị coi là stale"*) is `docs/MANIFEST.md` itself (Chapter 0 §5b/§7, I-12) — but it does **not** currently track `docs/architecture/stream-registry.yaml` or the Feature-scoped Input Contract YAMLs at all (confirmed: no dedicated ledger row exists for either today). Using it for this purpose is a genuine **scope extension** of an existing governed ledger, not the invention of a brand-new authoritative-artifact class — this distinction is load-bearing for the ADR-scope rerun in §4.

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
| Verdict | **Valid, but superseded as the primary recommendation by Option 4 (§2.1, §3)** — genuinely authority-compliant and still the preserved fallback (§3.1), but not minimum-scope once Option 4's off-event binding is considered: it duplicates the same checksum onto every fact and independently triggers `ADR_REQUIRED` (Event Schema), neither of which Option 4 requires |

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

### Option 4 — durable run/replay-manifest content-identity binding (added — `P3-FEATURE-QG-EVID05B-A-MAJ-01` remediation)

`computation_cursor.input_contract_ref`/`stream_registry_version` (unchanged, already required by ADR-035) are used as the lookup **key** into a durable, versioned, git-tracked ledger — `docs/MANIFEST.md`, its scope extended with rows for `docs/architecture/stream-registry.yaml` and each Feature-scoped Input Contract YAML — that binds each exact `{contract_id, contract_version}`/`registry_version` to the `input_contract_content_id`/`stream_registry_content_id` recorded **at the time that version was authored/approved** (same discipline MANIFEST.md's own governing rule already requires of every other tracked document today). No field is added to any Feature event or to `ComputationCursor`.

**Required flow:** event/cursor reference (`computation_cursor.input_contract_ref`/`stream_registry_version`, already present) → look up that exact key's binding in the manifest ledger → materialize the current Input Contract/Stream Registry artifact (same `authority_resolver.py` mechanism) → recompute its SHA-256 → compare against the manifest-bound value → mismatch or missing ledger entry/artifact fails closed → **only then** does Replay execution start.

| Criterion | Assessment |
|---|---|
| I-5 compliance | Directly implements §8.1.1 rule 5's own sanctioned pattern verbatim — "identity có thể nằm ở run manifest thay vì lặp trên mọi event" — this is that exact mechanism, not an analogy to it |
| Historical comparison-point integrity | Requires a **process discipline**, not an automatic code path: whoever authors/approves a new Input Contract/Stream Registry version must record its content identity in the ledger as part of that same transaction (identical in kind to MANIFEST.md's own existing rule for every other tracked document — not a new class of trust, an extension of an existing one) |
| How event references reach the checksum | Via the fact's own **unchanged** `computation_cursor.input_contract_ref`/`stream_registry_version` — no new field needed, since those keys already uniquely determine the ledger entry |
| Audit/replay reproducibility | Full — the ledger entry, like every other MANIFEST.md row, is git-tracked and reconstructable at any historical commit |
| Duplicate evidence volume | **One entry per distinct artifact *version*** (bounded by how many Input Contract/Stream Registry versions are ever authored — small), not one per fact — orders of magnitude smaller than Option 2's one-per-fact duplication, because §8.1.1 rule 2 makes the artifact immutable once referenced, so one verified binding per version is valid for every fact that ever cites it |
| Event-schema impact | **None** — `FeatureComputed`/`FeatureFactInvalidated`/`ComputationCursor` are untouched |
| New authoritative-artifact/mechanism impact | **None new** — extends `MANIFEST.md`'s existing, already-governed scope (Chapter 0 §5b/§7, I-12) to two more file paths it doesn't track today; does not invent a new artifact class (unlike the rejected "new provenance artifact" idea below) |
| Ownership / I-12 | `MANIFEST.md` is already the single authoritative source for "version/status hiện tại của tài liệu" (I-12, §5b) — Input Contract/Stream Registry YAMLs already live under `docs/architecture/`, structurally the same document class MANIFEST.md already tracks elsewhere |
| Cross-module blast radius | **None today** — Structure/Raw-Regime Engines do not consume `InputContractAuthorityProvider`/these artifacts at all (independently confirmed: no `InputContract`/`StreamRegistry` runtime reference in either engine's `src/`); only Feature Engine resolves them via content-hash-bearing authority today, so extending the ledger for these two specific artifact paths changes no other module's behavior |
| Backward compatibility / migration | None needed — adds ledger rows for existing files; no event ever needs to change shape, historically or going forward |
| Implementation complexity | Trades per-event schema/serialization work for ledger-maintenance discipline; benefits from (future, not this transaction) a lightweight verification check that MANIFEST.md's recorded content identity for each tracked Input Contract/Stream Registry version still matches that file's actual bytes |
| Failure semantics | Identical fail-closed posture to Option 2 — mismatch/missing ledger entry/artifact is a Replay-preparation failure, Replay execution never starts |
| Verdict | **Recommended** (see §3) — smaller footprint than Option 2 on every impact dimension (no Event Schema change, no new artifact class, smallest duplicate-evidence volume), fully authority-compliant, with the honest trade-off that its historical-integrity guarantee depends on a maintained ledger-update discipline rather than an automatic code path |

**No option superior to Option 4 was identified.** A fifth "invent a brand-new authoritative artifact/event type carrying content-identity provenance" (distinct from extending the existing `MANIFEST.md` ledger) mirrors ADR-035's own Alternative 3 (a separate referenced provenance artifact), rejected there for the same reason it would fail here: it adds an entire new authoritative-artifact class, causation hop, and stream/registry surface for information an already-existing, already-governed ledger can carry (Chapter 8 §8.4 made the identical choice for `decision_context_cursor` — embed/reuse, don't create a referenced side-channel; §8.1.1 rule 5 makes the identical choice here — reuse an off-event manifest, don't invent a new one).

### 2.1 Correction — content hashes are NOT necessarily copied onto every Feature fact

The original candidate's recommendation (Option 2) stated its checksum fields as if per-event persistence were the only compliant path. That overstated the requirement. Chapter 8 §8.1.1 rule 5 is explicit: *"Bắt buộc là verifiability, không phải một field cụ thể"* — verifiability is required, not any specific field, and identity "có thể nằm ở run manifest thay vì lặp trên mọi event" (may live in a run manifest instead of repeating on every event). Option 2 remains one valid, authority-compliant realization of that verifiability requirement (per-event, self-contained, automatic) — but it is not the only one, and Option 4 satisfies the identical invariant list (§3) while keeping the checksum off the event entirely. Any prior wording implying necessity of per-fact duplication is corrected here.

## 3. Recommended minimum-scope architecture (corrected — Option 4)

**This corrects the prior recommendation (Option 2).** Based on authority — specifically Chapter 8 §8.1.1 rule 5's explicit sanction of an off-event binding — Option 4 is the smaller-footprint, equally I-5-compliant architecture: no Event Schema change, no new authoritative-artifact class, no `ComputationCursor`/`FeatureComputed`/`FeatureFactInvalidated` change of any kind.

**Mechanism:** extend `docs/MANIFEST.md`'s existing, already-governed document ledger (Chapter 0 §5b/§7, I-12) with rows for `docs/architecture/stream-registry.yaml` and each Feature-scoped Input Contract YAML, each row recording that artifact version's content identity (SHA-256 of its real bytes) at the point that version is authored/approved — mechanically identical to how MANIFEST.md already records a content-identity blob for every other tracked document on every edit (already demonstrated dozens of times in this repository's own history, including every transaction in this candidate's own lineage).

```text
Replay preparation:
  1. read fact.computation_cursor.input_contract_ref / .stream_registry_version
     (unchanged, already required by ADR-035)
  2. look up MANIFEST.md's ledger entry for that exact {contract_id,
     contract_version} / registry_version key
  3. materialize the current Input Contract / Stream Registry artifact
     (authority_resolver.py, unchanged mechanism)
  4. recompute its SHA-256 over the real current bytes
  5. compare against the ledger-bound value
  6. mismatch OR missing ledger entry OR missing artifact -> FAIL CLOSED,
     Replay execution never starts
Replay execution:
  reads only the already-verified, already-materialized
  VerifiedInputContractAuthority -- unaffected by, and strictly after,
  step 6 above; the EVID-05(a)-proven network/filesystem cut is untouched
```

**Invariants satisfied:**

- **Content identity from exact immutable bytes** — the same SHA-256-of-real-artifact-bytes `authority_resolver.py` already computes today; no new hashing mechanism, no invented algorithm.
- **Binds the exact artifacts used** — the ledger key (`{contract_id, contract_version}`/`registry_version`) is exactly what `computation_cursor` already carries on every fact; per §8.1.1 rule 2 (immutable once referenced), one verified binding per version is valid for every fact that ever cites that version — no ambiguity about which artifact a given fact used.
- **Version/name equality alone is insufficient** — the ledger entry adds the missing content proof beyond the version string alone, so a version silently repointed at different bytes (a rule-2 violation) becomes detectable instead of structurally unverifiable.
- **Replay preparation resolves + verifies; mismatch/missing artifact fails closed before execution** — see flow above.
- **Replay execution performs no external resolution** — unaffected; the ledger lookup and artifact re-resolution both happen during Replay preparation, never during execution.
- **Original and replacement facts each preserve their own computation-time dependency evidence** — unaffected: both already carry their own independently-captured `computation_cursor.input_contract_ref`/`stream_registry_version` (ADR-035, unchanged); that is precisely what already identifies which artifacts governed each fact's own computation — no new field is needed to preserve this, since the artifact's own immutability (rule 2) makes the content identity a property of the *version*, not of the individual fact.
- **No process-local pointer qualifies** — the ledger is a durable, git-tracked, versioned file (`MANIFEST.md`), not an in-memory/process-local map; explicitly the class of durable evidence the invariant requires.

**Honest trade-off (surfaced, not hidden):** Option 2's per-event field is bound automatically, by the same code path that already resolves the authority object — it cannot be forgotten. Option 4's ledger binding depends on a maintained process discipline (an Input Contract/Stream Registry version-authoring transaction must also record its content identity in the ledger) — the same discipline MANIFEST.md already requires platform-wide for every other tracked document, not a new class of risk, but a real one worth naming for Review A.

**Cross-module impact:** none today — confirmed no other module resolves these artifacts via a content-hash-bearing authority object (§1).

**Event/schema impact:** none — `FeatureComputed`, `FeatureFactInvalidated`, and `ComputationCursor` are all unchanged.

### 3.1 Preserved fallback — Option 2's architecture (not recommended, retained for completeness)

Should Review A find extending `MANIFEST.md`'s scope to Chapter-8-owned Referenced Authoritative Artifacts unsuitable, Option 2 remains a fully valid, authority-compliant fallback: a new required sibling payload field, `computation_dependency_content_evidence: {input_contract_content_id, stream_registry_content_id}`, on `FeatureComputed`/`FeatureFactInvalidated` (never inside `ComputationCursor`), sourced verbatim from `VerifiedInputContractAuthority`'s existing fields, required on both original and replacement facts independently — full assessment in §2's Option 2 table. Its own ADR-scope result is unchanged from the original candidate: `ADR_REQUIRED` (Event Schema trigger) — see §4.

## 4. Fresh Chapter 0 §4b ADR-scope run (rerun against the corrected recommendation, Option 4 — independent, not inherited from Option 2)

| Trigger checked | Result |
|---|---|
| Event Schema change | **NO** — Option 4 adds no field anywhere on `FeatureComputed`, `FeatureFactInvalidated`, or `ComputationCursor`; the ledger key is `computation_cursor.input_contract_ref`/`stream_registry_version`, already required, unchanged |
| Platform Invariant addition/change | **NO** — I-5's own text is unchanged; this designs one compliant *verification mechanism* for it, it does not add or amend an invariant |
| Module Taxonomy / dependency-graph change | **NO** — no new module, no new dependency edge; `MANIFEST.md` is documentation governance, not a runtime module |
| Governance/Approval process change | **NO** — adding tracked-document rows to `MANIFEST.md` is the ordinary, routine editorial mechanism that document already uses for every other artifact it tracks (demonstrated repeatedly in this repository's own history); it does not alter Chapter 0's approval-gate process itself |
| Modification/supersession of a Locked/Approved ADR | **NO** — ADR-035 is untouched; no ADR is edited, superseded, or reopened |
| >1 module / platform-wide effect | **NO** — independently confirmed (§1, §2 Option 4 row) that no module besides Feature Engine currently resolves Input Contract/Stream Registry artifacts via a content-hash-bearing authority object; extending the ledger for these two specific artifact paths changes no other module's behavior today |
| Hard-to-reverse decision | **NO** — ledger rows are additive and can be extended/corrected the same way every other MANIFEST.md entry already is, without touching any event, code, or ADR |

**Result: `ADR_OPTIONAL`.** No hard Chapter 0 §4b trigger fires — this is deliberately why Option 4 was preferred over Option 2 (whose own, still-valid, unchanged assessment remains `ADR_REQUIRED` on the Event Schema trigger alone, per §3.1/§4's prior run). `ADR_OPTIONAL` (not `ADR_NOT_REQUIRED`) is judged appropriate rather than automatic, because this decision establishes a new fail-closed verification mechanism specifically relied upon as I-5 compliance evidence — "ảnh hưởng đáng kể" in Chapter 0 §4b's own middle-row sense, even though it alters no contract, schema, or Locked artifact. A governed reviewer (Review A / Product Owner) may reasonably choose to formalize this via a lightweight ADR for the benefit of future consumers of the same artifact classes, but it is not mandatory before implementation, unlike Option 2.

**Per instruction: STOPPING at this design/scope candidate regardless of the corrected `ADR_OPTIONAL` result.** No ADR is authored in this transaction. No `MANIFEST.md` scope-extension, `feature.md` amendment, `contracts.py`/schema implementation, or test is performed. `EVID-05` remains OPEN; `EVID-05(b)` remains unresolved pending a governed decision on whether to proceed directly to implementation (permitted under `ADR_OPTIONAL`, but not performed here) or to author an optional ADR first.

## 5. Not performed by this candidate (explicit)

```text
No ADR authored. No feature.md amendment. No contracts.py/event-schema
change. No MANIFEST.md scope-extension (no rows added for stream-
registry.yaml/Input Contract YAMLs). No test authored or modified. No
mutation run. No formal Chapter-13 evaluation. ADR-035 not edited, not
superseded, not reopened. EVID-05 not closed; EVID-05(a)'s SATISFIED
disposition is unaffected and unrevisited. P3-FEATURE-QG-EVID05B-A-MAJ-01
recorded REMEDIATED here but NOT self-closed — closure is a Review A
re-review determination.
```
