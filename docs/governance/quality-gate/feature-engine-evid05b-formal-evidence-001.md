---
id: feature-engine-evid05b-formal-evidence-001
title: "Feature Engine — Formal Chapter 13 §13.9 Quality-Gate Evidence — `P3-FEATURE-QG-EVID-05(b)`"
artifact_version: "1.0"
status: RECORDED — CLOSED — PASS
performed_at: "2026-09-11"
subject_head: "8a89f31a44731ec2f56a26f49bcdbc7c6ebb69c4"
---

# Feature Engine — Formal `P3-FEATURE-QG-EVID-05(b)` Quality-Gate Evidence Transaction

**Bounded formal Quality-Gate evidence transaction — vai trò: `Feature Engine EVID-05(b) Quality-Gate Evidence Recording Executor`.** Records Review A's already-completed validation of the two implementation transactions remediating `P3-FEATURE-EVID05B-IMPL-A-MAJ-01`/`-MAJ-02`/`-MAJ-03` (commits `2b25b8e9deda954b6a4a4e2684c12a466bf60f47` and `8a89f31a44731ec2f56a26f49bcdbc7c6ebb69c4`), substantiates that recorded determination with a fresh, independently-run test evidence set at the exact reviewed boundary, and — **only because both the recorded Review A disposition and this transaction's own fresh reproduction agree** — closes `P3-FEATURE-QG-EVID-05(b): CLOSED — PASS` per Chapter 13 §13.8/§13.9. Does **not** modify `src/feature_engine/**`, `tests/**`, any ADR, `feature.md`, or any canonical `v1.0` snapshot artifact. Does **not** infer or change the overall Feature Engine Chapter 13 Quality Gate, Feature module approval, the Phase 3 Approval Gate, or LIVE authorization — all remain exactly as recorded before this transaction (see §6).

## 1. Subject / source boundary (Chapter 13 §13.9 — subject identity + version/artifact/config)

```text
Repository HEAD (subject boundary, exact, non-mutable):
  8a89f31a44731ec2f56a26f49bcdbc7c6ebb69c4
  (branch review/feature-evid05b-formal-evidence-001; identical to the two
  implementation commits below plus their full ancestor chain — no
  intervening commit, no drift).

Parent chain evaluated (both implementation commits in scope):
  2b25b8e9deda954b6a4a4e2684c12a466bf60f47 -- "feature-engine: EVID-05(b)
    implementation correction (MAJ-01 + MAJ-02)"
  8a89f31a44731ec2f56a26f49bcdbc7c6ebb69c4 -- "feature-engine: EVID-05(b)
    MAJ-03 correction -- restore profile <-> contract-lineage binding in
    historical resolver" (HEAD)

Working tree at evaluation time: clean against HEAD for python/ and docs/
  (git status --porcelain=v1 -- python/ docs/ returns only pre-existing
  untracked docs/.DS_Store, unrelated to this subject and not part of any
  tracked artifact).

Exact subject files (blob identity, HEAD):
  python/feature-engine/src/feature_engine/authority_resolver.py:
    e4fe5038a5da2db0134fa9d77fa4fdf0c800a3e9
  python/feature-engine/src/feature_engine/contracts.py:
    e0ea0572d8ac16bdb602942970573d1ab59144fc
  python/feature-engine/src/feature_engine/output_contract_resolver.py:
    f703d91a609b6de5835e509e95004545e3c0c38e
  python/feature-engine/src/feature_engine/__init__.py:
    4d9eaac00f8e56cd6f45b1632e83ebde9c005c1b
  python/feature-engine/tests/test_historical_authority_resolver.py:
    0d00dadfbd656f9d0bee2481646e090b17c135d3
  python/feature-engine/tests/test_replay_preparation.py:
    0ffcc15bff583ad4e4cf0e888bbe32cc5b2a5681
  python/feature-engine/tests/test_replay_isolation.py:
    bb92d3bcb8f5d94564af62a401e1ab449a1890ea
  python/feature-engine/tests/test_evidence.py:
    42faadf66334da9e7c4bcbf766df7118cbfd183f
  python/feature-engine/tests/test_authority_resolver.py:
    386ae3c17e69738bb3a28a25663aebe0a635a83b (byte-identical to the copy
    already pinned in MANIFEST's ADR-041 bootstrap record -- unchanged by
    either implementation commit)
  python/feature-engine/tests/test_contracts.py:
    3a4a910a15b306db2935c5971f788dcbae1798fe

Referenced immutable Authoritative Artifacts consumed (unchanged, already
  Published/pinned by the ADR-041 canonical v1.0 bootstrap transaction --
  not re-verified here, only cited by exact identity):
  docs/architecture/stream-registry-versions/v1.0.yaml: blob
    4d67a8c3008231406f2038394fba6a7e98075bf4
  docs/architecture/input-contract-versions/feature-candle-input/v1.0.yaml:
    blob 8325dde1262530cfce0e110674d1b9444545c019
  docs/architecture/input-contract-versions/feature-regime-input/v1.0.yaml:
    blob fcb3e033e0aa9fb7756b152d17000f5a585b6d55
  docs/architecture/input-contract-versions/feature-swing-distance-input/
    v1.0.yaml: blob e3764d4f19a3f1d5e52b763d8383effa96ae986a
```

## 2. Applicable criteria / policy authority (exact versions applied)

```text
Constitution I-5 (Decision-Time Observable Dependency), 02-platform-
  invariants.md v3.1, Locked -- Verification: Replay execution reads only
  already-saved events + materialized/immutable artifacts; checksum of
  every referenced artifact must be checked, not merely materialized.
Chapter 13 (Quality Gates) v1.7, Locked -- §13.5 invariant-conformance
  gate (I-5 row); §13.8 fail-closed semantics; §13.9 evidence contract
  (this transaction's own governing format); §13.12(A) universal
  applicability (invariant conformance applies to every in-scope
  artifact regardless of tier -- no tier-resolution provenance required
  for this gate, since I-5 conformance is not coverage/tier-triggered).
Chapter 8 (Event Model) v4.8, Locked -- §8.1.1 rule 5 (verifiable content
  identity), §8.5/§8.5.1 (canonical Replay Cursor, unaffected/untouched
  by this evidence).
ADR-035 (Approved v0.2) -- computation_cursor canonical shape, unaffected.
ADR-037 (Approved v0.1, approved_at 2026-09-08T13:44+07:00) --
  Feature Computation Dependency Content Identity Evidence: the
  computation_dependency_content_evidence sibling payload field, Option 2
  architecture.
ADR-038 (Approved v0.1) -- Feature Output Event Contract Compatibility
  Commitment (backward_only), governs the BREAKING classification of the
  v0.6 payload delta.
ADR-039 (Approved v0.1, approved_at 2026-09-09T10:58+07:00) -- Canonical
  Event Contract Version-Artifact Authority and Resolution Mechanism.
ADR-040 (Approved v0.1, approved_at 2026-09-09T13:49+07:00) -- Platform-
  wide Retention/Archive Policy Semantics for Referenced Authoritative
  Artifacts.
ADR-041 (Approved v0.1, approved_at 2026-09-09T21:19+07:00; canonical
  v1.0 bootstrap atomically published 2026-09-11T10:48:31+07:00) --
  Canonical Exact-Version Resolution for Input Contracts and Stream
  Registry -- the authority the historical resolver (MAJ-02 fix) reads.
docs/domain/feature.md v0.6 (Draft) §3/§4/§8b -- the domain-contract
  payload/invariant definitions the implementation conforms to (verified
  fresh against current file content in §4 below, not assumed from
  memory).
```

## 3. Evaluator / authority (Chapter 13 §13.9 — evaluator/authority đã đánh giá)

```text
Review A: ChatGPT (AI Technical Architect, per docs/team/team.yaml) --
  the actual, sole Review A principal for this transaction. Distinct
  from the implementation Executor (Claude, Co-Authored-By on both
  reviewed commits 2b25b8e/8a89f31) -- no self-review.
Review A result, as recorded by the Product Owner as input to this
  transaction:
    Technical closure condition: SATISFIED
    Blocker 0 / Major 0 / Minor 0
    Verdict: CLEAN
    Risk Classification: R1 (bounded semantic / normal implementation
      risk -- ADR-042 §"R1" definition: "bounded bug fix; bounded
      semantic correction; internal algorithm change that does not
      alter external contract/authority" -- matches exactly: MAJ-01/
      MAJ-02/MAJ-03 are internal authority_resolver.py/
      output_contract_resolver.py/contracts.py corrections, no
      event-schema/payload-shape change, no new ADR, no canonical-
      snapshot edit).
    Cross-check: NO CROSS-CHECK (ADR-042 R1 default -- Review A alone
      is sufficient; not escalated to R2 by Review A or Product Owner).
    Recommendation: record P3-FEATURE-QG-EVID-05(b): CLOSED — PASS.
Per Chapter 13 §13.1, Quality Gate evidence is distinct from Product
  Owner Approval Gate consumption (§13.1's own "Quality Gate ≠ Approval
  Gate" formula) -- recording this evaluator determination as QG
  evidence does not itself constitute, and does not require, a
  Product Owner Approval Gate decision; it supplies input evidence for
  a future Chapter 12 §12.2(5) gate, consistent with the identical
  precedent already established for P3-FEATURE-QG-EVID-03 ("CLOSED --
  PASS -- REVIEW A VALIDATED", recorded 2026-09-08 as a bookkeeping
  transaction, no separate Product Owner decision line).
This Executor transaction independently reproduces (§5 below) the
  technical substance Review A validated -- Review A's own recorded
  disposition is accepted as input per instruction, not re-derived, but
  is not accepted uncritically: it is cross-checked here against a
  fresh, independent test run at the identical boundary before being
  recorded as PASS (fail-closed discipline, §13.8 -- had the fresh run
  disagreed with Review A's disposition, this transaction would have
  stopped fail-closed per §5's own instruction and reported the defect,
  not recorded PASS).
```

## 4. Fresh conformance verification against `feature.md` v0.6 (independent, not assumed)

Directly re-read `docs/domain/feature.md` (current HEAD content, not memory) confirms the implementation subject matches the domain contract this gate is evaluated against:

```text
§3/§4 require computation_dependency_content_evidence present on EVERY
  FeatureComputed/FeatureFactInvalidated (original and replacement/
  invalidation alike), containing input_contract_content_id/
  stream_registry_content_id copied verbatim from the SAME
  VerifiedInputContractAuthority instance the computation engine
  resolved/cached for that exact fact, corresponding exactly to that
  fact's own computation_cursor.input_contract_ref/
  computation_cursor.stream_registry_version -- confirmed present in
  tests/test_evidence.py (10/10 passed, §5) and in the Replay-
  preparation contract text (feature.md line 47): resolve the artifact
  computation_cursor references -> recompute content ID from real
  current bytes -> compare against persisted evidence -> fail closed
  before Replay execution on any of: missing artifact, malformed
  evidence, reference mismatch, content-ID mismatch -- confirmed
  exercised by tests/test_replay_preparation.py (14/14 passed, §5).
```

## 5. Fresh test evidence (independent local pytest run — this transaction, NOT GitHub CI)

**Explicit correction per instruction:** at the Review A boundary (`8a89f31a44731ec2f56a26f49bcdbc7c6ebb69c4`) there are no GitHub commit statuses or workflow runs attached to this repository — no CI exists for this project today. Any prior "305 passed" figure reported by an implementation-transaction executor is **not** GitHub CI evidence and is not cited as such here. The numbers below are a **fresh, independently-executed local run performed by this Executor transaction**, at this exact boundary, in a reinstalled editable virtualenv — not a reproduction of a cached/remembered number.

```text
Environment: existing python/feature-engine/.venv (Python 3.13.6),
  `pip install -e . --no-deps` reinstalled fresh against HEAD
  8a89f31a44731ec2f56a26f49bcdbc7c6ebb69c4 before running. pytest 9.1.1.
  Command: pytest <path> -v, run separately per required category, plus
  one full-suite run -- all from python/feature-engine/, this
  transaction, this session.

Required category 1 -- evidence emission/binding
  (tests/test_evidence.py): 10 passed, 0 failed.
  Covers: computation_dependency_content_evidence copied verbatim from
  the cached VerifiedInputContractAuthority instance for both Regime and
  Swing-Distance engines; original vs. invalidation/replacement facts
  each persist independently (no inheritance); conflict/cardinality
  fail-closed cases for normalized input-fact evidence.

Required category 2 -- historical authority resolver
  (tests/test_historical_authority_resolver.py): 34 passed, 0 failed.
  Covers: real Published v1.0 snapshot resolution (matches current
  active content ID); missing-snapshot fail-closed (Input Contract and
  Stream Registry, separately); no silent fallback to a different
  existing version; malformed version-token fail-closed (8 cases,
  including path-traversal payloads `../../../etc/passwd`,
  `v1.0/../../x`); malformed contract-id fail-closed (4 cases);
  wrong-content-inside-snapshot fail-closed (contract_id, contract_
  version, registry_version each independently); relational mismatch
  between pinned snapshots fail-closed; included-stream absent from
  pinned registry fail-closed; missing contract_id/registry_version
  field fail-closed; and the MAJ-03 fix specifically --
  test_regime_profile_rejects_swing_distance_contract_lineage,
  test_distance_profile_rejects_regime_contract_lineage,
  test_unknown_profile_fails_closed_even_with_a_genuinely_valid_snapshot,
  test_profile_binding_checked_before_any_filesystem_access -- all
  passed, directly substantiating the MAJ-03 remediation (profile <->
  contract-lineage binding checked before any filesystem access, fails
  closed for both cross-profile substitution and unknown profiles).

Required category 3 -- Replay preparation fail-closed
  (tests/test_replay_preparation.py): 14 passed, 0 failed.
  Covers: genuine-fact success path; missing artifact fail-closed;
  malformed snapshot fail-closed; snapshot correctly used when no
  current file exists / current file changed / current file removed
  (proving genuine snapshot-only resolution, not mutable-current
  fallback); a Regime fact forged onto a Swing-Distance snapshot fails
  closed (cross-profile forgery, MAJ-03-adjacent); malformed/missing
  evidence fail-closed; cursor naming a nonexistent contract/registry
  version fails closed; input_contract_content_id/
  stream_registry_content_id mismatch each independently fail closed.

Required category 4 -- Replay isolation regression
  (tests/test_replay_isolation.py): 2 passed, 0 failed.
  Covers: the EVID-05(a)-established external-access cut still actively
  intercepts filesystem/network access and the real production
  authority-resolution call path; Replay execution remains genuinely
  self-contained after construction for both engines -- confirms MAJ-01/
  MAJ-02/MAJ-03's implementation changes (all inside authority
  resolution / Replay *preparation*) introduced no regression into
  Replay *execution*'s self-containment, preserving EVID-05(a)'s
  disposition unrevisited.

Full feature-engine suite regression (tests/): 305 passed, 0 failed,
  0 skipped, 0 errors, in 0.26s (60 of these 305 are the four required
  categories above; the remaining 245 cover swing-distance/regime-
  passthrough/current-view/contracts/authority-resolver/output-contract-
  resolver -- confirming no cross-cutting regression from either
  reviewed commit).
```

## 6. Result

```text
P3-FEATURE-EVID05B-IMPL-A-MAJ-01: CLOSED — REVIEW A VALIDATED.
P3-FEATURE-EVID05B-IMPL-A-MAJ-02: CLOSED — REVIEW A VALIDATED.
P3-FEATURE-EVID05B-IMPL-A-MAJ-03: CLOSED — REVIEW A VALIDATED.

P3-FEATURE-QG-EVID-05(b): CLOSED — PASS.
  Basis: Review A CLEAN (Blocker 0/Major 0/Minor 0, R1, NO CROSS-CHECK)
  + this transaction's own fresh, independent reproduction of the exact
  same technical substance (§5), both agreeing, at the exact reviewed
  boundary 8a89f31a44731ec2f56a26f49bcdbc7c6ebb69c4. No FAIL — evidence
  or FAIL — criteria condition (§13.8) present: subject/criteria/
  evaluator/boundary/input-identity all pinned (§13.9), measurement
  reproducible (this transaction reproduced it fresh, not reused a
  stale number).

P3-FEATURE-QG-EVID-05(a): SATISFIED (unaffected, unrevisited -- §5's
  Replay-isolation regression run confirms it still holds, not that it
  was re-litigated).
P3-FEATURE-QG-EVID-05 overall: CLOSED — both part (a) and part (b) now
  SATISFIED/CLOSED — PASS.
```

## 7. Not performed / preserved unchanged (explicit)

```text
No src/feature_engine/**, tests/**, tooling/**, pyproject.toml, or
  requirements-dev.lock.txt change -- this transaction is evidence-
  recording only, verified via `git diff --quiet` against HEAD before
  and after.
No ADR authored, edited, or superseded. ADR-035/037/038/039/040/041 all
  verified byte-unchanged.
No docs/domain/feature.md edit -- read-only re-verification (§4).
No canonical v1.0 snapshot artifact edited (Referenced Authoritative
  Artifacts, immutable per ADR-041 -- not touched).
P3-FEATURE-QG-EVID-01/-02/-03/-04/-06/-07/-08: unaffected, unchanged by
  this transaction -- EVID-03 remains CLOSED — PASS — REVIEW A VALIDATED
  (2026-09-08, unrevisited); EVID-04/06/07/08 remain OPEN / blocking
  exactly as recorded in feature-engine-chapter13-remediation-plan-001.md.
Overall Feature Engine Chapter 13 Quality Gate: FAIL — evidence
  (unaffected -- EVID-04/06/07/08 remain open; closing EVID-05 overall
  does not close the overall gate, which requires ALL eight findings
  resolved).
Feature module approval: NOT APPROVED (unaffected).
Phase 3 Approval Gate: NOT OPENED (unaffected).
LIVE: NOT_AUTHORIZED (unaffected).
No Product Owner Approval Gate decision performed or implied by this
  transaction (§3 -- Quality Gate evidence ≠ Approval Gate consumption,
  Chapter 13 §13.1).
```

**Next governed step (not performed by this transaction):** a future Chapter 12 §12.2(5) Approval-Gate transaction may consume this evidence together with EVID-01/-02/-03 once EVID-04/-06/-07/-08 are also resolved — none of those four is addressed here, and EVID-04/-08 remain externally blocked on the (not-yet-built) Decision Engine/Risk Gateway/Execution Engine per `feature-engine-chapter13-remediation-plan-001.md` §1/§6.
