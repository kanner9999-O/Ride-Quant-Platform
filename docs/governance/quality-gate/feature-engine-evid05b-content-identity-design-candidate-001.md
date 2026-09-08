# Feature Engine — `P3-FEATURE-QG-EVID-05(b)` Persisted Content-Identity Design Candidate 001

> **Bounded correction 002 — `P3-FEATURE-QG-EVID05B-A-MAJ-02`**, addressed/remediated pending Review A re-review (not self-closed by this correction transaction). Records **`P3-FEATURE-QG-EVID05B-A-MAJ-01: CLOSED — BOUNDED REVIEW A RE-REVIEW`** (correction 001's Option-4 addition and per-fact-duplication correction were validated). **New finding this transaction remediates:** correction 001 wrongly assumed Chapter 8's permitted "run manifest" pattern automatically means governance `docs/MANIFEST.md`, and wrongly classified assigning `MANIFEST.md` a new runtime content-identity-mapping responsibility as an ordinary row extension / "no new mechanism." **Corrected:** Option 4 is split into **4A** (a genuinely new dedicated run/replay content-identity manifest — no such mechanism is claimed to exist) and **4B** (extending governance `MANIFEST.md`'s authority, now honestly assessed as assigning it a NEW authoritative responsibility, not bookkeeping) — both fully re-assessed against Chapter 0/I-12 and the direct **ADR-022** precedent (§1, §2); the recommendation reverts from Option 4 back to **Option 2**, based on current repository authority rather than hypothetical future infrastructure (§3); Chapter 0 §4b is rerun against Option 2 independently, yielding **`ADR_REQUIRED`** (Event Schema) again — not inherited from correction 001's `ADR_OPTIONAL` (§4). **No change to:** the finding this candidate addresses (`P3-FEATURE-QG-EVID-05(b)`), `EVID-05(a)`'s `SATISFIED` disposition, ADR-035 (still not edited/superseded/reopened), or the `DESIGN ONLY` transaction kind — no ADR authored, no production/schema/test implementation, `EVID-05` still not closed.
>
> `P3-FEATURE-QG-EVID05B-A-MAJ-01: CLOSED — BOUNDED REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID05B-A-MAJ-02: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`

```yaml
status: CANDIDATE / NOT EFFECTIVE — ADR_REQUIRED (reverted to Option 2), PENDING BOUNDED REVIEW A RE-REVIEW
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
      status: "CLOSED — BOUNDED REVIEW A RE-REVIEW"
bounded_correction_002:
  applied_at_repository_head: eb9d6eab37f7c21f309fea7ada6691e5ad22d90a
  corrected_candidate_blob_before_correction: 9b1aab7ce0d89d3615e89bd206a881ffce49e2af
  reviewer_findings_addressed:
    - id: P3-FEATURE-QG-EVID05B-A-MAJ-02
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
- **Repository precedent for run-manifest/off-event content-identity evidence (correction 001):** independently inspected. `raw_regime_engine.regime.RegimeDefinition.content_identity()` computes a deterministic SHA-256 fingerprint over the definition's full canonical content, and its own docstring states it is *"suitable as external run-manifest evidence"* — but the SAME docstring explicitly disclaims inventing any registry/storage/lifecycle authority: *"This module invents no definition registry/storage/lifecycle authority — that remains deferred by regime.md §19/§20."* This is a hash-producing **capability**, not an implemented manifest artifact. A repository-wide search for `run_manifest`/`replay_manifest` found zero authoritative schema anywhere (no Constitution chapter, Domain Contract, or ADR defines a "Run Manifest"/"Replay Manifest" artifact type, its versioning, or its resolution mechanism) — **no platform run-manifest schema is claimed to exist**, consistent with the instruction not to assume one.
- **What `docs/MANIFEST.md` is currently authoritative for (corrected, `P3-FEATURE-QG-EVID05B-A-MAJ-02`):** Chapter 0 §5b/§7 and I-12 define `MANIFEST.md`'s current scope precisely: the Decision Log; current document version/status (the "Documentation Manifest (Lockfile)"); ADR lifecycle state and reverse `superseded_by` supersession mapping; current OQ status. **Nowhere does Chapter 0 define `MANIFEST.md` as an authoritative RUNTIME mapping** from an Input Contract/Stream Registry logical version to an immutable content identity, consumed by a running process (Replay preparation) to make a fail-closed verification decision. Correction 001's characterization of this as "an existing, already-governed mechanism... reuses existing infrastructure" **conflated** MANIFEST's actual documentation-governance scope with a materially different, new kind of authority (a runtime dependency-verification source) — the correction here does not restate that conflation as settled.
- **ADR-022** (Approved v0.3, `Package 1.4 Published-Contract Compatibility Commitment and Policy Root`) — **direct, on-point precedent**, independently inspected. ADR-022 itself decided to designate `docs/MANIFEST.md` as canonical authority for a NEW role (Package 1.4 policy-root identity/version AND applicability/activation, Chapter 10 §10.4.3 mục 3/4) — and this designation was made through a **full governed ADR** (Product Owner `APPROVE`), not an ordinary editorial/bookkeeping transaction; ADR-022's own scope classification recorded `ADR REQUIRED` for exactly this kind of MANIFEST-authority assignment. Critically, ADR-022 §5.2 **explicitly limits its own designation to "Phase 1 architecture-only scope (KHÔNG runtime activation event nào tồn tại)"** and states in so many words: *"ADR này KHÔNG tự động carry-forward MANIFEST LÀM runtime activation authority vượt quá Phase 1 architecture-only scope"* (this ADR does not carry forward MANIFEST as a runtime activation authority beyond Phase-1-architecture-only scope) — reserving any RUNTIME extension of MANIFEST's authority for "một ADR successor... riêng" (a separate successor ADR). This is direct, existing repository precedent **against** treating a MANIFEST-as-runtime-authority extension (Option 4B, below) as small or already-settled; it confirms both that such an assignment requires an ADR, and that this specific repository has already, deliberately, declined to make the runtime-scoped version of it so far.
- **Git history as audit evidence, not authoritative mapping (`P3-FEATURE-QG-EVID05B-A-MAJ-02`):** git commit history is durable and inspectable, but I-12/Chapter 0 do not anywhere designate "the git history of `docs/architecture/*.yaml`" as itself an authoritative content-identity mapping a runtime process may rely on for a fail-closed decision — it is audit evidence a human or tool *could* inspect after the fact, not a resolvable, pinned, versioned authority a computation can query the way it queries `VerifiedInputContractAuthority`.

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
| Verdict | **Recommended (reaffirmed, §3)** — its checksum-copying cost and `ADR_REQUIRED` (Event Schema) are real, but bounded and well-precedented (ADR-034/035 both already went through this exact class of change cleanly); §2's re-assessment of Options 4A/4B (below) shows neither is demonstrably smaller once their own governance costs are honestly accounted for, per the recompare in §3 |

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

### Option 4A — a genuinely new, dedicated run/replay content-identity manifest (reworked — `P3-FEATURE-QG-EVID05B-A-MAJ-02` remediation)

A brand-new authoritative artifact class, purpose-built for this exact function: a durable, structured (not prose) evidence artifact binding each exact `{contract_id, contract_version}`/`registry_version` to its content identity, satisfying Chapter 8 §8.1.1's five conditions on its own terms — **no such mechanism currently exists anywhere in this repository; none is claimed to exist.**

| Criterion | Assessment |
|---|---|
| I-5 compliance | Achievable in principle — this is the "purpose-built manifest" §8.1.1 rule 5 gestures at, if actually built |
| Immutable/versioned identity | Would have to be designed from scratch: its own artifact-versioning scheme, its own immutable-once-referenced rule, its own non-reused-identifier rule — none of this exists today |
| Exact mapping cursor-ref → content hash | Designable, but is new design work, not reuse of anything existing |
| Persistently resolvable through replay/audit horizon | Requires its own retention/archive policy to be authored (§8.1.1 rule 4) — no such policy exists for any hypothetical artifact of this kind today |
| Manifest identity itself pinned/unambiguous for the run | Requires solving a **self-reference problem**: the manifest artifact is itself a Referenced Authoritative Artifact under §8.1.1, so it needs its own version identity that a fact/run can pin — a design question with no existing answer |
| Fail-closed missing/mismatch | Achievable, structurally identical to Option 2/4B's own check |
| Retention/lifecycle authority | Undetermined — no module or chapter currently owns "replay-manifest lifecycle"; this is a genuine new ownership question, not an extension of an existing owner |
| No process-local/unpinned-commit reliance | Achievable *if* designed correctly, but is not automatic — a naive implementation could easily degrade into "read whatever the current file looks like", the same trap Option 3 (rejected) fell into |
| New authoritative-artifact/mechanism impact | **New class, in full** — an entirely new kind of artifact, ownership, versioning, and resolution mechanism, with no existing repository precedent to reuse |
| Chapter-8/ADR-035 compatibility | No conflict with ADR-035/§8.5, but only because it is a wholly separate concept — this is not evidence of small scope, only of non-overlap |
| Cross-module blast radius | Nominally scopeable to Feature Engine alone today, but designing a brand-new artifact CLASS is inherently the kind of decision Chapter 0 §4b treats as architecturally significant regardless of current consumer count |
| Verdict | **Rejected as minimum-scope** — genuinely I-5-compliant if built correctly, but requires inventing an entire new authoritative-artifact class, ownership model, versioning scheme, and self-reference resolution from nothing; larger design footprint than Option 2, not smaller |

### Option 4B — extend governance `docs/MANIFEST.md`'s authority (reworked, honestly — `P3-FEATURE-QG-EVID05B-A-MAJ-02` remediation)

Treated here, correctly, as assigning `MANIFEST.md` a **new authoritative responsibility** — a runtime dependency-verification source Replay preparation depends on — not as an ordinary row/bookkeeping extension.

| Criterion | Assessment |
|---|---|
| Chapter-0/I-12 authority impact | **Real and non-trivial.** MANIFEST's current Chapter 0 §5b/§7 scope is Decision Log + document version/status + ADR lifecycle/supersession + OQ state — a documentation lockfile. Making a RUNNING PROCESS depend on it for a fail-closed verification decision is a materially new authority role, not a natural reading of its current scope |
| Must MANIFEST entries become immutable per artifact-version key | **Yes, and this conflicts with MANIFEST's own current editorial discipline.** Every other MANIFEST.md row is routinely edited/replaced in place as a document's version bumps (demonstrated repeatedly across this very repository's transaction history — "Blob X → Blob Y" is the normal pattern). A row that must instead become permanently immutable once referenced (§8.1.1 rule 2) — while every surrounding row in the same file keeps its current mutable-in-place discipline — is an inconsistent, currently-undefined split within one document, not something already true of MANIFEST.md today |
| How old bindings remain authoritative after later MANIFEST edits | **Undefined today.** MANIFEST.md tracks CURRENT state per document (its own banner: "tổ hợp version+status chính xác... tại một thời điểm"), not a durable, append-only ledger of every historical version's own content identity kept forever. A fact computed under Input Contract v3 must be able to look up v3's binding forever, even after MANIFEST's own row for that artifact has moved on to v5 — MANIFEST's current structure does not obviously support this without a redesign of how that row behaves, which is design work, not "add two rows" |
| Whether a fact/run needs to pin a MANIFEST identity | **Yes, and this is a new requirement.** Since MANIFEST.md itself changes over time, a replay-verification lookup needs to know as-of-which-MANIFEST-commit it is querying to be unambiguous — MANIFEST.md has no existing per-entry frozen identity the way an Approved ADR file does |
| Runtime → governance-artifact dependency | **A new, awkward coupling.** Feature Engine's runtime replay-verification code would need to parse a large, prose-heavy, human-authored governance document (this very file's own neighbor) to extract a machine-checkable binding — architecturally weaker than reading the already-structured YAML artifacts Option 2 already reads today |
| Precedent — ADR-022 | **Direct and unfavorable to "ordinary extension."** ADR-022 assigned `MANIFEST.md` canonical authority for a comparable NEW role (Package 1.4 policy-root identity/version + activation) only through a full governed ADR (`ADR REQUIRED`, Product Owner `APPROVE`) — and explicitly scoped that designation to "Phase 1 architecture-only," refusing to extend MANIFEST into runtime-activation authority, reserving that for a future, separate ADR (§1 above). Option 4B is precisely the runtime extension ADR-022 itself declined to make |
| New authoritative-artifact/mechanism impact | **New authoritative ROLE, even without a new artifact class** — per ADR-022's own precedent, this is not "no new mechanism"; it is a new authority assignment of the same kind ADR-022 needed a full ADR for |
| Cross-module blast radius | None today in terms of other modules' code, but the AUTHORITY-BOUNDARY change itself (documentation ledger becoming a trusted runtime input) is the kind of decision Chapter 0 treats as significant independent of current consumer count (see ADR-022 precedent) |
| Verdict | **Rejected as minimum-scope** — not ordinary bookkeeping; carries its own real governance cost (an ADR, by direct precedent) plus unresolved structural gaps (row immutability, historical-binding retention, MANIFEST-identity pinning) Option 2 does not have at all |

**Recompare, §2.1 correction preserved:** Chapter 8 §8.1.1 rule 5 genuinely does not require content identity to live on every event — that correction from bounded correction 001 stands. What correction 001 got wrong was assuming an off-event realization was automatically *cheaper* under CURRENT repository authority. Once 4A's from-scratch-mechanism cost and 4B's ADR-022-precedented authority cost are honestly priced in, neither is smaller than Option 2's single, well-precedented Event Schema change (§3).

### 2.1 Correction — content hashes are NOT necessarily copied onto every Feature fact (correction 001, preserved)

Chapter 8 §8.1.1 rule 5 is explicit: *"Bắt buộc là verifiability, không phải một field cụ thể"* — verifiability is required, not any specific field, and identity "có thể nằm ở run manifest thay vì lặp trên mọi event" (may live in a run manifest instead of repeating on every event). This remains true and is not retracted by correction 002. What correction 002 corrects is the separate, further claim that an off-event realization is therefore the smaller-scope choice under this repository's CURRENT authority — see the recompare above and §3.

## 3. Recommended minimum-scope architecture (reverted — Option 2)

**This reverts correction 001's recommendation (Option 4) back to Option 2**, per `P3-FEATURE-QG-EVID05B-A-MAJ-02`: under CURRENT repository authority (not hypothetical future infrastructure), neither 4A nor 4B is demonstrably smaller-scope than Option 2 once their own governance costs are honestly priced in (§2) — 4A requires inventing an entire new authoritative-artifact class from nothing; 4B requires an ADR by direct ADR-022 precedent, plus carries unresolved structural gaps (row immutability, historical-binding retention, MANIFEST-identity pinning) that ADR-022 itself never had to solve because it stayed Phase-1-architecture-only and explicitly declined the runtime extension. Option 2's cost, by contrast, is a single, already-precedented, already-bounded Event Schema change (ADR-034/035 both went through it cleanly).

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
- **Version/name equality alone is insufficient** — `computation_cursor.input_contract_ref`/`stream_registry_version` already carry version/name; this field adds the missing content proof, so a version string silently repointed at different bytes (a §8.1.1 rule-2 violation) becomes detectable instead of structurally unverifiable.
- **Replay preparation resolves + verifies** — re-resolves `{contract_id, contract_version}`/`stream_registry_version` named by the fact's own `computation_cursor`, recomputes both content IDs from the current real bytes, and compares against `computation_dependency_content_evidence`; identical mechanism to what `authority_resolver.py` already does, plus one new comparison step.
- **Mismatch/missing artifact fails closed before execution** — a comparison failure (or unresolvable artifact) is a Replay-preparation failure; Replay execution never starts, consistent with I-5's Verification text and unaffected by the EVID-05(a) transaction's existing self-contained-execution proof.
- **Replay execution performs no external resolution** — unaffected; the new evidence is read from the already-persisted fact / already-materialized authority, exactly like `computation_cursor` itself is read today.
- **Original and replacement facts each preserve their own evidence** — required on both `FeatureComputed` and `FeatureFactInvalidated`, captured independently at each fact's own evaluation, mirroring `computation_cursor`'s own existing "never inherited/copied from the fact it supersedes" discipline.
- **No process-local pointer qualifies** — both values are content hashes of durable, versioned artifact bytes carried on the durable event log itself (Chapter 8 §8.1, I-12's own authoritative source for runtime facts) — not object identity/memory references, and not dependent on any new, as-yet-unauthorized authority (unlike 4A/4B).

**Cross-module impact:** none. Chapter 8's canonical `replay_cursor` (§8.5), ADR-035's decision content, Structure/Raw-Regime/other Compute Engines, `docs/MANIFEST.md`'s current authority, and any future Decision/Strategy/Risk/Execution module are all unaffected and unreferenced by this candidate.

**Event/schema impact:** one new required field on `FeatureComputed`/`FeatureFactInvalidated` (`feature.md` §3/§4) — the same class and scale of change ADR-035 itself made for `computation_cursor`, and ADR-034 made for `invalidation_cause`.

**Note on §2.1's correction (preserved, not retracted):** Chapter 8 §8.1.1 rule 5 genuinely does not *require* this per-event duplication — an off-event manifest binding would also be compliant *if* one existed under settled, adequate authority. Option 2 is recommended here not because it is the only compliant shape, but because it is the only one of the three assessed options that requires no new authority, no new artifact class, and no ADR precedent-defying assumption to actually build today.

### 3.1 Not recommended, retained for completeness — Options 4A/4B

Should a future transaction find that a dedicated replay-manifest mechanism (4A) or a governed MANIFEST-authority extension (4B, likely via its own ADR, following the ADR-022 pattern directly) becomes independently worth building — e.g. because a second consumer of Input Contract/Stream Registry content identity emerges, changing the "one ledger entry per version, reused platform-wide" economics — either remains available as a superseding design. Neither is adopted here: see §2's 4A/4B tables for the full, corrected assessment.

## 4. Fresh Chapter 0 §4b ADR-scope run (rerun against the reverted recommendation, Option 2 — independent, not inherited from correction 001's Option 4)

| Trigger checked | Result |
|---|---|
| Event Schema change | **YES** — a new required payload field on `FeatureComputed`/`FeatureFactInvalidated` (`feature.md` §3/§4) is precisely "thay đổi Event Schema", the identical trigger ADR-034 (`invalidation_cause`) and ADR-035 (`computation_cursor`) both cited for themselves |
| Modification/extension of Approved ADR-035 semantics | **NO** — `computation_cursor`'s shape, meaning, and the canonical §8.5 reuse are untouched; the new field is a sibling on the *event*, not a change to the *cursor* |
| Canonical Chapter-8 Replay Cursor ownership | **NO conflict** — Option 2 does not touch §8.5's closed five-field table or any other `replay_cursor` consumer |
| Governance/Approval-process or MANIFEST-authority change | **NO** — Option 2 does not touch `docs/MANIFEST.md`'s scope or authority at all, so the ADR-022 precedent's own trigger (assigning MANIFEST a new role) simply does not apply here |
| >1 module / platform-wide effect | **NO** — confirmed no cross-module blast radius (§3); this is a Feature-only Event Schema addition |
| New authoritative-artifact/mechanism | **NO** — no new artifact class, no new manifest, no new ownership question (unlike both 4A and 4B) |

**Result: `ADR_REQUIRED`** — solely on the independently-sufficient Event Schema trigger (disjunctive reading, same precedent ADR-034/035 already established). This is **not inherited** from correction 001's now-superseded `ADR_OPTIONAL` conclusion for Option 4 — it is freshly rerun against Option 2 on its own terms, arriving back at the same result the original candidate (before correction 001) first found: adding required payload structure to an authoritative Feature event has no non-ADR path, per the same reasoning ADR-035's own "Scope classification" already recorded for itself. (For completeness, had 4A or 4B instead been recommended, each independently reaches `ADR_REQUIRED` too — 4A via a new-authoritative-artifact-class decision, 4B via the direct ADR-022 precedent for assigning MANIFEST a new authoritative role — so no path among the three options assessed avoids an ADR under current authority; §3's choice of Option 2 is about which `ADR_REQUIRED` path costs least, not about avoiding the ADR trigger altogether.)

**Per instruction: STOPPING at this design/scope candidate.** No ADR is authored in this transaction. No `feature.md` amendment, no `contracts.py`/schema implementation, no test authored, no `MANIFEST.md` change of any kind. `EVID-05` remains OPEN; `EVID-05(b)` remains unresolved pending a future, separate ADR-authoring transaction that would formally decide Option 2 (or a superior option, should one later be demonstrated).

## 5. Not performed by this candidate (explicit)

```text
No ADR authored. No feature.md amendment. No contracts.py/event-schema
change. No MANIFEST.md scope-extension or edit of any kind (no rows
added for stream-registry.yaml/Input Contract YAMLs — this correction
does not perform even the Option-4B mechanism it evaluated and
rejected). No test authored or modified. No mutation run. No formal
Chapter-13 evaluation. ADR-035 not edited, not superseded, not
reopened. ADR-022 not edited, not superseded, not reopened (read-only
precedent citation). EVID-05 not closed; EVID-05(a)'s SATISFIED
disposition is unaffected and unrevisited.
P3-FEATURE-QG-EVID05B-A-MAJ-01: recorded CLOSED — BOUNDED REVIEW A
  RE-REVIEW.
P3-FEATURE-QG-EVID05B-A-MAJ-02: recorded REMEDIATED here but NOT
  self-closed — closure is a Review A re-review determination.
```
