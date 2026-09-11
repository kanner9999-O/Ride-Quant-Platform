---
id: feature-engine-evid07-property-based-mechanism-candidate-001
title: "Feature Engine — `P3-FEATURE-QG-EVID-07` Python Property-Based Testing Mechanism — CANDIDATE"
candidate_version: "0.1"
status: CANDIDATE — NOT EFFECTIVE — PENDING REVIEW A
performed_at: "2026-09-11"
repository_head_at_authoring: "310a83e22c868611028e5804c524fb5a4e9f57da"
---

# Feature Engine — `P3-FEATURE-QG-EVID-07` Python Property-Based Testing Mechanism — CANDIDATE 001

> **Status banner:** `CANDIDATE / NOT EFFECTIVE — PENDING REVIEW A`. This is a **design / mechanism-selection transaction only** — vai trò: `Feature Engine EVID-07 Property-Based Mechanism Candidate Author`. It selects and proposes a mechanism; it does **not** install any dependency, does **not** edit `pyproject.toml`/`requirements-dev.lock.txt`, does **not** modify any Feature Engine production or test file, does **not** measure anything, and does **not** close `P3-FEATURE-QG-EVID-07`. Executor does not self-approve — closure/approval belongs to Review A (ADR-042: `Executor → Review A → Risk Classification → Product Owner Decision`), never asserted here.

## 0. Baseline / boundary verification (fresh, this transaction — not assumed)

```text
Repository HEAD (verified via `git rev-parse HEAD`, this transaction):
  310a83e22c868611028e5804c524fb5a4e9f57da — matches the expected fresh-start
  boundary exactly; `git status --porcelain=v1 -- python/ docs/` clean
  (only the pre-existing untracked docs/.DS_Store, unrelated).

Governing review-gate model (verified against docs/MANIFEST.md frontmatter
  banner, this transaction): ADR-042 v0.5 Approved, ACTIVE since
  2026-09-10T15:51+07:00 — Executor → Review A (mandatory) → Risk
  Classification (R0/R1/R2) → Product Owner Decision → Execution. Review A
  is mandatory; a second (cross-check) review is optional and, per
  docs/adr/ADR-042.md, recommended only for R2 — never automatically
  required. The obsolete mandatory-two-review "Review A/B" workflow the
  task instructed NOT to rely on (docs/adr/ADR-031.md, Mode A/Mode B) is
  Superseded (MANIFEST, ADR-042 activation) and is not used anywhere in
  this candidate.

Current pyproject.toml (python/feature-engine/pyproject.toml, read fresh,
  this transaction): `requires-python = ">=3.13"`; `dependencies = []`
  (production has zero runtime dependencies, unchanged); `[project.
  optional-dependencies].dev` = ruff==0.16.4, mypy==2.3.1, pytest==9.1.1,
  coverage==7.16.0, mutmut==3.7.0 — exact-pinned (`==`), no property-based
  library present. `requirements-dev.lock.txt` (head, read fresh):
  ast_serialize, click, coverage, iniconfig, libcst, librt, linkify-it-py,
  markdown-it-py, mdit-py-plugins, mdurl, mutmut, mypy, mypy_extensions,
  packaging, pathspec, platformdirs, pluggy, Pygments, pytest, PyYAML-ft,
  rich, ruff, setproctitle, textual, typing_extensions — zero
  hypothesis/sortedcontainers/any other property-based library entry.
  Installed venv: Python 3.13.6 (verified `python --version`, existing
  `python/feature-engine/.venv`).
```

## 1. Current factual gap (re-verified fresh, not assumed from the old remediation plan)

```text
Constitution I-13 (docs/constitution/02-platform-invariants.md v3.1,
  Locked) Verification clause requires: "Property-based test trên
  transition graph authoritative" as one of five required evidence
  categories (the other four: illegal-transition test, strictly-terminal/
  correction test, concurrent transition test, Replay state
  reconstruction test).
Chapter 13 (docs/constitution/13-quality-gates.md v1.7, Locked) §13.6
  lists "Property-based" as a required test category "khi áp dụng" for
  numerical/state-machine boundaries (I-9, I-13) — not discretionary once
  the boundary class applies (confirmed independently by the exact same
  reading already applied to market-reference-service's own I-13 finding,
  `P3-MR-QG-A-MAJ-01`, docs/MANIFEST.md).
Fresh grep across python/feature-engine/{src,tests}/ for `hypothesis`,
  `import hypothesis`, `@given`, `RuleBasedStateMachine`: zero hits.
  Fresh grep across the same tree for any other Python property-based
  library import (`pyfuzz`, `schemathesis`, `crosshair`): zero hits.
  No property-based testing framework is installed, pinned, approved, or
  in use anywhere in this repository's Python code today (Go's own
  `market-reference-service` uses native Go 1.18+ fuzzing plus hand-rolled
  `math/rand`-seeded generators — a Go-toolchain-specific mechanism with
  no Python equivalent capability built into CPython's stdlib; see §3
  Alternative A for why this precedent does not transfer as "zero-
  dependency" for Python).
Existing Feature Engine state-transition tests (tests/test_current_view.py,
  tests/test_regime_passthrough.py, tests/test_swing_distance.py) are all
  example-based (fixed input → fixed expected output/exception) — real,
  valid, passing evidence of correctness, but not the specific
  "Property-based" category Chapter 13 §13.6 names, exactly the same
  distinction already recorded for the Go finding (`P3-MR-QG-A-MAJ-01`):
  existing deterministic tests are not invalidated or discarded, they
  simply do not by themselves satisfy this category's requirement.
Conclusion: `P3-FEATURE-QG-EVID-07` gap is confirmed real and unchanged —
  NEEDS_GOVERNED_DESIGN_OR_MECHANISM, exactly as
  feature-engine-chapter13-remediation-plan-001.md's own EVID-07 row
  found (re-verified here directly against current repository state, not
  imported uncritically).
```

## 2. Feature transition surfaces `EVID-07` will exercise (authoritative, verified against current source)

Two authoritative transition graphs are in scope, both owned by `docs/domain/feature.md` per I-13's own "state machine authoritative của entity đó tại `/docs/domain/`" requirement — Constitution does not redefine either, only requires evidence against them.

```text
Surface 1 — Per-window correction lineage (feature.md §9, rules 1/4/5/6/9):
  Entity: the FeatureComputed lineage for one exact
  (feature_subject_id, effective_window) pair.
  States (existence lifecycle, feature.md line 81/91): notional
  UNCOMPUTED -> COMPUTED (self-transition for every subsequent
  FeatureComputed on the SAME subject/window pair — the state machine
  encodes "has this pair ever been computed," not the current value).
  Legal transitions: an original FeatureComputed (supersedes_fact_ref
  absent, feature.md line 161) establishes the lineage; a replacement
  FeatureComputed (supersedes_fact_ref present) is legal only when it
  names the lineage's CURRENT head, that head has never itself been
  superseded (no fork, rule 6), does not skip an intermediate invalidated
  member (rule 4/5), and has already received exactly one visible
  FeatureFactInvalidated.
  Illegal transitions (must be rejected): a second original for an
  already-computed pair; a replacement naming a stale/non-head fact
  (fork); a replacement arriving before its own invalidation is visible;
  a second invalidation of an already-invalidated fact.
  Real implementation under test (verified via source read, this
  transaction — not from memory):
    src/feature_engine/current_view.py — FeatureCurrentView.
      on_feature_computed / on_feature_invalidated, raising the real
      FeatureLineageError for exactly the four illegal cases above (lines
      92, 102, 107, 117, 122).
    src/feature_engine/regime_passthrough.py — RegimePassthroughFeature
      Engine._WindowLineage / _emit_original / _emit_invalidation /
      _emit_replacement, raising the same real FeatureLineageError class
      (lines 239, 265).
    src/feature_engine/swing_distance.py — SwingDistanceFeatureEngine.
      _WindowLineage / _recompute / _invalidate_and_replace /
      _emit_replacement_only / _invalidate_and_reattempt /
      _reevaluate_all_windows / _preempt_settled_window (these are the
      exact functions already independently identified as the highest
      mutation-density hotspots in
      feature-engine-mutation-baseline-001-analysis.md §1.6 — direct
      cross-confirmation that this surface is genuinely load-bearing, not
      an arbitrarily chosen one).

Surface 2 — FeatureCurrentView projection derivation (feature.md §11):
  Entity: the derived view_state for one (feature_subject_id,
  effective_window) target window.
  States: no-row (before any fact) -> VALID | PENDING_CORRECTION — exactly
  two post-existence states, no third value (feature.md line 269, 287).
  Legal transitions: VALID when the target window's lineage head has no
  visible invalidation; PENDING_CORRECTION when the head has a visible
  invalidation but no visible replacement yet; transition back to VALID
  only once the replacement becomes visible.
  Illegal/prohibited outcomes (must never occur): falling back to an
  older window than the true target window (feature.md line 608); falling
  back to a fact that has itself been invalidated; reporting a third
  view_state value.
  Real implementation under test: src/feature_engine/current_view.py —
  FeatureViewResult (line 39, VALID/PENDING_CORRECTION only, all four
  value fields simultaneously None iff PENDING_CORRECTION), _view_ordering_
  key (line 57, target-window/lineage-head resolution).

Not a separate surface (scoped out, avoiding an invented third graph):
  the "eligible_swing_selection_superseded" invalidation-cause distinction
  (feature.md, "Winner supersession" section) is a documented VARIANT
  within Surface 1's own replacement/invalidation transitions (a different
  invalidation_cause value on the same FeatureFactInvalidated transition),
  not a structurally distinct state machine — it is exercised as an
  additional legal-transition case under Surface 1, not a third surface.
```

## 3. Candidate alternatives (compared against current Ride authority, not popularity)

```text
Alternative A — Hand-rolled stdlib generators (Go precedent, mirrored)
  Mechanism: Python's stdlib `random` module, explicitly seeded, fixed
  trial-count loops asserting against the real state machines — the exact
  pattern already used for market-reference-service's I-13 evidence
  (docs/MANIFEST.md, TestFoldStatusPropertySequentialOracleMatchesReal
  Validator etc., 150-300 trials/machine, zero third-party dependency).
  For: genuinely zero new dependency (matches this repository's own
    established Go precedent exactly); no new license/supply-chain
    surface; total control over generation logic.
  Against (the reason the Go precedent does NOT transfer cleanly): Go's
    own mechanism relied on TWO stdlib/toolchain capabilities Python's
    stdlib does not have an equivalent of — (1) `math/rand` is
    deterministically seedable AND the Go team additionally used Go
    1.18+'s BUILT-IN native fuzzer (`testing.F`, part of the `go test`
    toolchain itself, not a third-party library) for the
    panic/crash-class properties; Python's stdlib `random` is seedable but
    CPython ships no built-in fuzzing/shrinking engine at all. Building an
    equivalent (generation strategies for the Feature domain's own
    composite types — EventRecordRef, EvaluationFrontier, ComputationCursor
    — PLUS a shrinking algorithm to reduce a failing generated case to a
    minimal reproducible counterexample PLUS a seed/reproduction
    convention) from raw `random` calls means re-implementing, in Feature
    Engine's own test suite, a materially worse subset of what a mature
    library already provides and already tests itself. This is a real,
    ongoing maintenance/correctness liability the Go module did not incur,
    because Go's toolchain absorbed it for free — Python's did not.
  Verdict: rejected as the sole mechanism — the zero-dependency property
    that made this the right choice for Go does not hold for Python
    without materially higher build/maintenance cost; see §4 for why
    "minimum mechanism" does not mean "minimum dependency count" once the
    stdlib capability gap is this large.

Alternative B — `hypothesis` (PyPI, HypothesisWorks)
  Purpose-built Python property-based/fuzz testing library, pytest-
  integrated (Framework :: Pytest classifier, verified), with a dedicated
  `hypothesis.stateful.RuleBasedStateMachine` API specifically for
  rule/state-machine/transition-sequence verification — the closest
  existing match to I-13's own "transition graph authoritative" wording
  of any candidate assessed. Verified directly this transaction (`pip
  download --no-deps`, scratch dir outside the repository, NOT installed
  into python/feature-engine — see §7 for the exact non-installation
  scope discipline):
    latest version: 6.168.0 (verified via `pip index versions hypothesis`,
      this transaction, not from memory).
    Development Status :: 5 - Production/Stable (verified from wheel
      METADATA, this transaction).
    License-Expression: MPL-2.0 (Mozilla Public License 2.0 — OSI-
      approved, file-level weak copyleft; verified from wheel METADATA).
    Requires-Python: >=3.10 (compatible with this project's own
      requires-python = ">=3.13" and the installed 3.13.6, verified).
    Mandatory runtime Requires-Dist on Python >=3.11 (this project's
      floor): exactly ONE — `sortedcontainers>=2.1.0,<3.0.0`. (The only
      other unconditional entry, `exceptiongroup>=1.0.0`, is marked
      `python_full_version < '3.11'` and does not apply at >=3.13.)
      `sortedcontainers` itself verified this transaction (`pip download`,
      scratch dir): version 2.4.0, License: Apache 2.0, zero further
      Requires-Dist of its own (pure-Python, leaf dependency). Total
      mandatory dependency footprint of adopting hypothesis on this
      project's Python floor: exactly one small, pure-Python, permissively
      licensed leaf package — a materially lean footprint, comparable to
      or smaller than `mutmut` (already approved, pulls in
      ast_serialize/libcst/librt/textual/rich per the current lock file).
    `RuleBasedStateMachine`/`@given`/`@example`/`@seed`/`assume` cover
      exactly the evidence categories §6 below requires: generated legal
      transition sequences, illegal-transition rejection (via `assume`/
      explicit negative rules or plain `@given` + `pytest.raises`),
      deterministic shrinking to a minimal failing example, and a printed,
      directly-reusable reproduction seed.
  Against: one new dependency (see above — small, but non-zero); a
    learning-curve cost for anyone unfamiliar with the library (mitigated
    by `RuleBasedStateMachine` being a close conceptual match to this
    repository's own already-declared "state machine authoritative"
    vocabulary, and by the pytest integration requiring no separate
    runner).
  Verdict: candidate for selection, §4.

Alternative C — `schemathesis` / `crosshair` / other niche PBT-adjacent
  tools
  `schemathesis` is API-schema/contract fuzzing (OpenAPI/GraphQL-focused)
    — wrong problem shape, Feature Engine exposes no such schema surface;
    not evaluated further.
  `crosshair` is symbolic execution / SMT-based verification, not
    generative property-based testing — a fundamentally heavier mechanism
    (requires an SMT solver, materially larger footprint and learning
    curve) solving a related but distinct problem (proof-oriented, not
    generate-and-shrink). Notably, `crosshair-tool` appears only as an
    OPTIONAL extra of hypothesis itself (`extra == 'crosshair'`,
    verified from hypothesis's own METADATA, §above) — confirming it is
    not a competing baseline mechanism but an optional add-on to the
    already-selected Alternative B, not pulled in by a bare `hypothesis`
    install.
  `pytest-quickcheck` — verified via `pip index versions pytest-
    quickcheck`: latest is a pre-1.0, sparsely maintained wrapper with a
    materially smaller feature set than hypothesis (no stateful-machine
    API, no shrinking database) and no distinct capability hypothesis
    lacks; rejected as strictly dominated by Alternative B for this exact
    use case, not evaluated further to avoid unnecessary landscape churn
    for a dominated option.
  Verdict: none of these is competitive with Alternative B for I-13's
    specific transition-graph/illegal-transition/shrinking requirements;
    not adopted, not added merely because they exist.
```

## 4. Selected recommendation

```text
Selected mechanism: `hypothesis` (Alternative B), used specifically via
  `hypothesis.stateful.RuleBasedStateMachine` for the transition-graph/
  sequence-constraint/illegal-transition evidence (§6), and plain `@given`
  strategies for the narrower correction/invalidation/replay-
  reconstruction properties that do not require full stateful-machine
  modeling.

Why this is the MINIMUM mechanism, not merely the popular one: the
  actual capability gap is not "does Python have `random`" (it does) but
  "does anything in this repository's current reach provide deterministic
  generation + shrinking + a transition-sequence-aware testing model for
  Python, the way Go's own toolchain already provided natively for
  market-reference-service." Nothing does. Building that capability by
  hand (Alternative A) is not actually smaller in real engineering cost
  than adopting a single, Production/Stable, MPL-2.0, one-dependency
  library purpose-built for exactly this — it is larger, because Feature
  Engine's own test suite would then own and maintain a materially worse
  reimplementation of shrinking/generation logic hypothesis already
  provides, tests, and maintains upstream. This mirrors the same standard
  this repository already applied when it accepted `mutmut` (also a
  third-party PyPI dependency with a non-trivial transitive footprint) as
  the Python test-effectiveness mechanism rather than hand-rolling mutant
  generation — see docs/engineering/testing.md's own "Python test-
  effectiveness mechanism — APPROVED" section and §8 below.
```

## 5. Deterministic / reproducibility contract (proposed — not yet enforced by any committed config)

```text
Seed / reproduction: hypothesis generates from an internal PRNG seeded
  per-test-per-run by default; on a failing example it prints the
  "Falsifying example" AND an explicit reproduction instruction
  ("You can reproduce this example by temporarily adding @seed(<N>) to
  this test"). Proposal: every CI/local failure report MUST be captured
  verbatim (the printed seed + minimal example), matching this
  repository's own Chapter 13 §13.10 flaky-test discipline (no silent
  retry-until-green) — the failing seed becomes part of the defect
  record, exactly like a fixed example-based test's failing input would.

Shrinking: built into hypothesis, deterministic given the same seed —
  every failing generated example is automatically reduced to a
  locally-minimal reproducible counterexample before being reported. No
  additional configuration required; proposal records this as REQUIRED
  behavior (not merely default), i.e. a future install/pin transaction
  MUST NOT disable shrinking (`phases` setting) for the required EVID-07
  properties.

Generated-input bounds: proposal — two named `hypothesis.settings`
  profiles (registered via `settings.register_profile`, standard
  hypothesis pattern), mirroring this repository's own dev/CI split
  already used elsewhere (e.g. mutmut's own separate dev/measurement
  invocation discipline):
    "dev" profile — interactive default, local `.hypothesis` example
      database enabled (developer convenience, faster iteration on
      previously-failing examples), `max_examples` at hypothesis's own
      library default.
    "ci" profile — `derandomize=True` (forces a fully deterministic,
      bytecode-derived seed so the SAME examples are generated on every
      run, not merely reproducible via a logged seed after the fact),
      `database=None` (no local-machine-dependent state persisted/read —
      avoids non-hermetic behavior differences between machines/CI
      workers), explicit `max_examples` bound (proposal: 200 per property,
      the same order of magnitude as the Go precedent's 150-300
      trials/machine — exact number to be finalized at the install/pin
      transaction against real measured runtime, not fixed here as a
      Constitution-adjacent numeric commitment).
  Rationale for NOT committing the `.hypothesis` example database to the
  repository: it is a local cache of previously-failing inputs, not a
  reproducibility mechanism this repository's own I-12/SSOT discipline
  would want to treat as authoritative — the PRINTED seed on failure is
  the authoritative, portable reproduction artifact, consistent with how
  this repository's own mutmut/coverage evidence transactions already
  favor explicit, re-runnable commands over opaque local caches.

Flaky-test handling: hypothesis has built-in `Flaky` exception detection
  — if replaying an already-found failing example produces a DIFFERENT
  result than the original run, hypothesis raises `Flaky` distinctly
  rather than silently reporting pass or fail. Proposal: a `Flaky` result
  on an EVID-07 property is treated exactly as Chapter 13 §13.10 already
  requires for any nondeterministic test — quarantine with an explicit
  MANIFEST/backlog follow-up, NEVER retried-until-green to mask it. This
  is a strictly stronger detection signal than the repository's existing
  flaky-test tooling has for ordinary example-based tests (§12 of this
  same testing.md), since hypothesis proves non-reproducibility on the
  SAME generated input rather than relying on incidental re-runs.

CI/local reproducibility: identical `hypothesis==<pinned>` version in
  both environments (single exact pin, no version range, matching this
  project's existing `==`-only convention for every other dev dependency)
  is REQUIRED — hypothesis's own shrinking/generation algorithm is not
  guaranteed stable across its own versions (documented upstream
  behavior: new hypothesis releases may change which examples are
  generated/shrunk-to). Version pinning is therefore not merely this
  repository's house style here — it is a correctness precondition for
  reproducibility, to be re-verified at install time per §7.

Version pinning: proposal — add `hypothesis==6.168.0` (exact, matching
  the version verified live in this transaction, §3) to `[project.
  optional-dependencies].dev` in pyproject.toml, and its resolved
  transitive closure (`hypothesis==6.168.0`, `sortedcontainers==2.4.0`)
  to `requirements-dev.lock.txt` — NOT executed in this transaction (§7,
  §9). The exact version MUST be re-verified (not merely copied from this
  document) at the actual install/pin transaction, per this repository's
  own G-VERIFY-001 discipline — the PyPI candidate landscape can advance
  between candidate-authoring and install time, exactly the same
  discipline testing.md's own coverage.py/mutmut installation-time
  verification contracts already require (§7 below).
```

## 6. Valid-evidence definitions (Chapter 13 §13.6, scoped to Surfaces 1–2, §2 above)

```text
Legal transitions: a `RuleBasedStateMachine`-driven test that generates
  sequences of ORIGINAL-then-zero-or-more-REPLACEMENT operations against
  a real engine instance (RegimePassthroughFeatureEngine or
  SwingDistanceFeatureEngine, real, never a re-implementation of their
  rules — same discipline the Go precedent already established, "against
  the real, authoritative fold engine") and asserts, after every
  operation, that FeatureCurrentView's real on_feature_computed/
  on_feature_invalidated projection (Surface 2) matches the expected
  VALID/PENDING_CORRECTION state and lineage head — i.e. legal-transition
  evidence and Surface-2 projection evidence are exercised TOGETHER by
  the same generated sequences, not as two unrelated test suites.

Illegal-transition rejection: generated sequences that deliberately
  violate feature.md §9's four rules (fork: two replacements naming the
  same head; skip-ahead: a replacement naming a non-head/stale fact; a
  replacement before its invalidation is visible; double-invalidation)
  must be rejected by the REAL FeatureLineageError raise sites already
  verified in §2 — property asserts the specific exception type is
  raised, not merely "some exception," matching this repository's own
  existing example-based tests' own precision (e.g.
  test_foreign_scope_*_rejected already assert specific exception types
  per feature-engine-chapter13-remediation-plan-001.md §2).

Sequence/order constraints: order-independence-style properties (mirrored
  from the Go precedent's own TestFoldStatusPropertyOrderIndependence) —
  for facts whose relative arrival order should not matter to the final
  legal state (interleaved candle vs. swing-confirmation delivery,
  interleaved regime facts across independent windows), shuffled
  application orders must converge to the identical final projection;
  for facts whose order legally MUST matter (a replacement is illegal
  before its own invalidation is visible), the same generator must assert
  the REJECTION triggers precisely when order is violated — sequence
  constraints are evidence for both "order-independent where it should
  be" and "order-dependent, and enforced, where it must be," not treated
  as a single blanket property.

Correction/invalidation/replacement lifecycle: property-based coverage of
  feature.md §9's full lineage lifecycle end-to-end (original -> N
  corrections, N generated/bounded, not fixed at one correction the way
  today's example-based tests are) — asserting each lineage member's own
  independently-pinned `computation_dependency_content_evidence`/
  `computation_cursor` is never inherited/copied from a prior member
  (ADR-037's own discipline, EVID-05(b), already CLOSED — PASS; this
  candidate does not reopen or modify that evidence, it adds an
  orthogonal generative check that the SAME already-verified invariant
  continues to hold under generated sequences, not just the fixed
  examples EVID-05(b)'s own tests use).

Replay reconstruction consistency: for a generated lineage sequence,
  rebuilding FeatureCurrentView from the persisted event sequence via
  replay (already-existing self-contained-replay discipline, EVID-05(a),
  SATISFIED, unaffected/unrevisited by this candidate) must produce the
  IDENTICAL final view_state/lineage-head as the original, non-replayed,
  live application of the same sequence — a property-based generalization
  of feature.md §11/§"Cursor-correct pending correction" over MANY
  generated sequences rather than the fixed scenarios EVID-05(a)'s
  existing tests already cover.

Concurrent/interleaved transitions — applicability determined, not
  assumed: a fresh grep across src/feature_engine/*.py for `concurren`,
  `expected_version`, `optimistic`, `threading`, `asyncio`, `Lock(` this
  transaction returned ZERO hits. Feature Engine's real handlers
  (on_candle/on_swing_confirmed/on_swing_invalidated/on_regime_classified/
  on_regime_invalidated) are synchronous, single-threaded consumers of an
  already-ordered event stream at a single computation cursor — there is
  no concurrent-writer/version-conflict contract exposed at this module's
  boundary today. I-13's "concurrent transition attempt... resolve
  deterministic bằng version/concurrency contract" clause is therefore
  genuinely NOT APPLICABLE at the Feature Engine module boundary as
  currently implemented (this is an ownership/architecture fact, not a
  gap this candidate is deferring) — true multi-writer concurrency, if it
  ever exists for Feature facts, is owned by Chapter 8's stream/sequence
  model and Event Bus/log write-path, outside src/feature_engine/**.
  This is NOT the same as "interleaved," which genuinely IS applicable
  and is covered above (sequence/order constraints) — interleaved
  ARRIVAL ORDER of already-serialized facts at one cursor is real and
  testable; concurrent WRITERS are not present in this module. Per §13.8
  fail-closed discipline, this is an explicit, verified "not applicable"
  determination (backed by the grep command above), not a silent skip.
```

## 7. Installation-time verification contract (REQUIRED for any future install/pin transaction — mirrors testing.md's own coverage.py/mutmut contracts; fail-closed if any item does not resolve)

```text
- exact package identity: `hypothesis` on PyPI (not a same-named package
  on a different index);
- exact pinned version, re-verified live (the candidate landscape can
  move between this authoring transaction and install time — `pip index
  versions hypothesis` or equivalent, not copied from §3/§5 above);
- exact pinned transitive closure, re-verified live: `sortedcontainers`
  (and, only if Python drops below 3.11 by then, `exceptiongroup` —
  re-check this project's own `requires-python` has not changed);
- content identity at install (`pip download --no-deps`, sha256/wheel
  hash cross-check, same discipline already used in this very candidate's
  own §3 verification);
- Python 3.13(+) compatibility re-verified at the actual interpreter/
  version installed at that time, not assumed unchanged from this
  candidate;
- current `pytest` version compatibility (hypothesis's own pytest plugin
  entry point) re-verified against whatever `pytest` version the lock
  file carries at install time (may have moved past `9.1.1`);
- `RuleBasedStateMachine`/`@given`/`@example`/`@seed`/`assume`/`settings`/
  `settings.register_profile` API surface re-verified stable at the
  pinned version (hypothesis is Production/Stable but still ships minor
  API evolution between releases — re-read the actual installed
  version's own changelog/docs, not this candidate's description);
- shrinking/database default behavior re-verified unchanged (confirm the
  "ci" profile settings proposed in §5 still map to the same parameter
  names/semantics at the version actually installed);
- `Flaky` exception class/import path re-verified unchanged;
- reproducibility in a clean environment (fresh venv, `pip install
  --no-deps -r requirements-dev.lock.txt`, `pip check` -> "No broken
  requirements found") — identical discipline to every other QG evidence
  transaction in this repository;
- no unsupported Python 3.13+ construct in Feature Engine's current
  source that hypothesis's strategy-generation code cannot model (re-scan
  at install time, current source may have changed since this candidate).
  Any item above that does not resolve at install time -> fail-closed,
  hypothesis is NOT accepted as EVID-07 evidence machinery until resolved
  (Chapter 13 §13.8).
```

## 8. ADR Scope Rule — fresh run (Chapter 0 §4b, independent of the old remediation plan's language)

```text
Trigger checked                              | Result
-----------------------------------------------|-------
Platform Invariant addition/edit               | NO — I-13's text is
                                                  unchanged; this candidate
                                                  proposes EVIDENCE for an
                                                  already-Locked invariant,
                                                  not a new/edited one.
Event Schema change                            | NO — no event/payload
                                                  field is added, changed,
                                                  or proposed; this is a
                                                  dev/test-only dependency.
Module Taxonomy / dependency-graph change      | NO — no new module, no
                                                  module-registry.yaml
                                                  edit; hypothesis is a
                                                  dev-time TEST dependency
                                                  of the existing
                                                  feature-engine module,
                                                  not a new runtime module
                                                  or a change to production
                                                  `dependencies = []`.
Governance/Approval-process change             | NO — does not touch
                                                  Chapter 0/11/12/ADR-042.
>1 module or hard-to-reverse effect            | NO — scoped to
                                                  python/feature-engine
                                                  only (this repository's
                                                  own established
                                                  "FEATURE-ENGINE-ONLY"
                                                  scoping pattern, e.g. the
                                                  mutmut threshold); a
                                                  dev/test dependency is
                                                  trivially reversible
                                                  (remove from
                                                  pyproject.toml/lock,
                                                  delete the tests that use
                                                  it) — same reversibility
                                                  class as ruff/mypy/
                                                  pytest/coverage/mutmut,
                                                  none of which required an
                                                  ADR.
Edit/supersede a Locked ADR                    | NO — no ADR file touched.

Carve-out authority directly on point (Chapter 3 §3.2 line 44 + Chapter
  13 §13.3/§13.14, both Locked, verified fresh): Testing Convention
  ("chỉ quy định style/tooling... coverage/tier requirement đã có đầy đủ
  ở Chapter 13, không định nghĩa lại") and Chapter 13 §13.3/§13.14
  ("không khóa tool/vendor cụ thể... defer Engineering Foundation") both
  ALREADY pre-authorize tool/vendor selection within Testing Convention's
  own governed candidate -> Review A/B (now Review A + Risk
  Classification) -> Product Owner approval workflow — this is exactly
  the SAME "pattern (b)" already used, independently, for THREE prior
  Testing Convention tool selections in this repository: `coverage.py`
  (Python line+branch coverage, APPROVED via Testing Convention v0.7,
  ADR_NOT_REQUIRED), `mutmut` (Python test-effectiveness, APPROVED via
  Testing Convention v0.12, same disposition), and `gobco` (Go branch
  coverage, CANDIDATE, same disposition) — none of the three required an
  ADR, all three used this exact carve-out reasoning, verified directly
  against docs/engineering/testing.md this transaction, not assumed.

Result: `ADR_NOT_REQUIRED`.
  This is NOT inherited from feature-engine-chapter13-remediation-plan-
  001.md (which only described a workflow SEQUENCE mirroring mutmut's own
  precedent, without itself asserting a scope-rule classification) — it
  is freshly re-derived here, directly against Chapter 0 §4b's table and
  the two Locked carve-out clauses, and cross-checked against three
  independent same-repository precedents reaching the identical
  disposition for the identical class of decision (dev/test tooling
  selection, single-module scope, pre-authorized by Chapter 13 §13.14).
  This candidate authors NO ADR file.
```

## 9. Not performed at this transaction (explicit)

```text
No `pip install hypothesis` (or any package) into python/feature-engine's
  committed environment — all verification in §3/§5/§7 used a SCRATCH
  directory strictly outside the repository (deleted-safe, never
  committed, never touching python/feature-engine/.venv's installed
  package set beyond the pre-existing dev dependencies already present
  before this transaction).
No edit to pyproject.toml or requirements-dev.lock.txt.
No production or test file under python/feature-engine/{src,tests}
  created, edited, or deleted (verified `git diff --quiet -- python/`
  before and after, this transaction).
No property-based test authored.
No `P3-FEATURE-QG-EVID-07` PASS/FAIL/CLOSED disposition recorded — it
  remains exactly `NEEDS_GOVERNED_DESIGN_OR_MECHANISM` /
  `FAIL — evidence`, unchanged.
No reopening, re-litigation, or modification of `P3-FEATURE-QG-EVID-05(a)`
  or `P3-FEATURE-QG-EVID-05(b)` — both verified byte-unchanged in
  docs/MANIFEST.md/docs/CHANGELOG.md/docs/governance/quality-gate/ (this
  candidate only ADDS one new file); both remain CLOSED — PASS / SATISFIED
  exactly as recorded at HEAD 310a83e22c868611028e5804c524fb5a4e9f57da.
Overall Feature Engine Chapter 13 Quality Gate: UNCHANGED, `FAIL —
  evidence` (EVID-04/-06/-07/-08 remain OPEN/blocking; this candidate does
  not touch EVID-04/-06/-08 at all).
Feature module approval: NOT APPROVED (unaffected). Phase 3 Approval
  Gate: NOT opened (unaffected). LIVE: NOT_AUTHORIZED (unaffected).
No Product Owner Approval Gate decision performed or implied — per
  Chapter 13 §13.1 (Quality Gate evidence ≠ Approval Gate consumption)
  AND because this transaction does not even reach the Quality Gate
  evidence stage yet (mechanism not yet selected/approved).
No mutmut/coverage.py/gobco candidate or approval history touched —
  verified byte-unchanged.
```

## 10. Self-consistency check (performed before commit)

```text
- §2's cited source identifiers (FeatureLineageError, FeatureCurrentView.
  on_feature_computed/on_feature_invalidated, RegimePassthroughFeature
  Engine._emit_original/_emit_invalidation/_emit_replacement,
  SwingDistanceFeatureEngine._recompute/_invalidate_and_replace/
  _emit_replacement_only/_invalidate_and_reattempt/_reevaluate_all_
  windows/_preempt_settled_window) were verified via direct `grep -n`
  against current src/feature_engine/*.py this transaction, not recalled
  from memory — line numbers cited match the grep output captured this
  transaction.
- §3/§5/§7's hypothesis/sortedcontainers version, license, Requires-
  Python, and Requires-Dist claims were verified via `pip index versions`
  and `pip download --no-deps` into a scratch directory outside the
  repository this transaction, not from training-data memory.
- §6's "concurrent transition" not-applicable determination is backed by
  an explicit, reproducible grep command (zero hits) rather than an
  unverified assertion.
- §8's ADR-scope conclusion was cross-checked against three independent,
  same-repository precedents (coverage.py, mutmut, gobco) reaching the
  identical disposition for the identical decision class, not asserted on
  Chapter 0 §4b's table alone.
- No numeric Chapter 13 threshold is duplicated into this candidate (no
  such threshold exists for the Property-based category — §13.6 states
  the category is required "khi áp dụng," not a percentage — so the
  EF-TEST-A-MIN-01/P3-PY-COV-A-MIN-01 SSOT-duplication defect class does
  not apply here; confirmed by direct reading of §13.6, not assumed).
- Internally coherent: no section of this candidate asserts EVID-07 is
  closed, asserts a dependency was installed, or asserts a Product Owner
  decision occurred — cross-checked against §9's own explicit negative
  list.
```

## 11. Next governed step (not performed by this transaction)

```text
1. Review A (ChatGPT, per docs/team/team.yaml) reviews this candidate:
   mechanism selection soundness, Surface 1/2 completeness, §6 evidence-
   category sufficiency, §8's ADR-scope conclusion, and Risk
   Classification (R0/R1/R2, per ADR-042) for the CANDIDATE itself.
2. If Review A finds defects: a bounded correction transaction remediates
   them (same pattern as every prior Testing Convention candidate in this
   repository) — not self-closed by the correction author.
3. Once Review A is CLEAN: Product Owner decision on the candidate
   (mechanism selection only — still no installation).
4. A SEPARATE, later, install/pinning transaction executes §7's full
   installation-time verification contract, actually adds `hypothesis`/
   `sortedcontainers` to pyproject.toml and requirements-dev.lock.txt, and
   installs into python/feature-engine's environment.
5. A SEPARATE, later, test-authoring transaction writes the actual
   property-based tests against Surfaces 1–2 (§2/§6).
6. A SEPARATE, later, formal Chapter 13 §13.9 evidence transaction (same
   pattern as feature-engine-evid05b-formal-evidence-001.md) records
   fresh measurement and, only if it genuinely passes, closes
   `P3-FEATURE-QG-EVID-07`.
   None of steps 1-6 is performed by this transaction.
```
