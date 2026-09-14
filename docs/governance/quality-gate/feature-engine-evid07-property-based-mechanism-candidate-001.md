---
id: feature-engine-evid07-property-based-mechanism-candidate-001
title: "Feature Engine — `P3-FEATURE-QG-EVID-07` Python Property-Based Testing Mechanism — CANDIDATE"
candidate_version: "0.2"
status: "CANDIDATE — NOT EFFECTIVE — BOUNDED CORRECTION 001 (P3-FEATURE-QG-EVID07-A-MAJ-01/-02/-03/-04/-05 REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW)"
performed_at: "2026-09-11"
repository_head_at_authoring: "310a83e22c868611028e5804c524fb5a4e9f57da"
bounded_correction_001:
  applied_at_repository_head: "cd9d2684b0a315cde1bd429f3d4b0b07f8fe96d5"
  corrected_candidate_blob_before_correction: "f3bdb9ff82e3e88456792c4e06da48688a5bd6b4"
  reviewer_findings_addressed:
    - id: P3-FEATURE-QG-EVID07-A-MAJ-01
      status: "REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW"
    - id: P3-FEATURE-QG-EVID07-A-MAJ-02
      status: "REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW"
    - id: P3-FEATURE-QG-EVID07-A-MAJ-03
      status: "REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW"
    - id: P3-FEATURE-QG-EVID07-A-MAJ-04
      status: "REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW"
    - id: P3-FEATURE-QG-EVID07-A-MAJ-05
      status: "REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW"
---

# Feature Engine — `P3-FEATURE-QG-EVID-07` Python Property-Based Testing Mechanism — CANDIDATE 001

> **Bounded correction 001 (this transaction)** — vai trò: `Feature Engine EVID-07 Property-Based Mechanism Candidate Bounded Correction Executor`. Remediates five Review A findings against candidate v0.1 (reviewed blob `f3bdb9ff82e3e88456792c4e06da48688a5bd6b4`, boundary `cd9d2684b0a315cde1bd429f3d4b0b07f8fe96d5`): `-MAJ-01` (ADR Scope misclassification — corrected `ADR_NOT_REQUIRED` → `ADR_OPTIONAL — ADR NOT AUTHORED`, and removed the "carve-out" mischaracterization of Chapter 3 §3.2/Chapter 13 §13.14); `-MAJ-02` (approval-authority misstatement — removed every claim that Review A approves or closes this candidate; corrected to `Executor → Review A + Risk Classification → Product Owner Decision → Execution`, Product Owner sole approval authority); `-MAJ-03` (competing tooling SSOT — this file is now QG-scoped rationale only; the actual mechanism/tool decision is canonicalized into `docs/engineering/testing.md` v0.17 candidate section, added in this same bounded transaction as one coherent semantic decision, not a second unrelated one); `-MAJ-04` (Hypothesis reproducibility contract — corrected after re-reading hypothesis 6.168.0's actual source this transaction: removed the false claim that every ordinary falsifying example prints a reusable seed; distinguished deterministic CI generation (`derandomize`) from failure-artifact persistence (`print_blob`/`@reproduce_failure`, version-locked, temporary) from durable regression capture (`@example`)); `-MAJ-05` (I-13 concurrent-transition applicability — replaced grep-only reasoning with the authoritative basis: Chapter 8 §8.3's Locked single-writer-authority + atomic-sequence-assignment contract, which structurally prevents competing transitions from independently reaching any stream's append point, Feature Engine's included). None of the five findings is self-closed here — closure is Review A's own determination on re-review, per Chapter 0 §3.
>
> `P3-FEATURE-QG-EVID07-A-MAJ-01: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID07-A-MAJ-02: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID07-A-MAJ-03: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID07-A-MAJ-04: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID07-A-MAJ-05: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`

> **Status banner:** `CANDIDATE / NOT EFFECTIVE — BOUNDED CORRECTION 001 PENDING REVIEW A RE-REVIEW`. This remains a **QG-scoped analysis/rationale transaction only** — vai trò: `Feature Engine EVID-07 Property-Based Mechanism Candidate Author`. It does **not** install any dependency, does **not** edit `pyproject.toml`/`requirements-dev.lock.txt`, does **not** modify any Feature Engine production or test file, does **not** measure anything, and does **not** close `P3-FEATURE-QG-EVID-07`. Per `-MAJ-03`'s remediation (below), this file does **not** itself canonicalize the mechanism/tool decision — that decision is canonicalized in `docs/engineering/testing.md`'s own "Python property-based testing mechanism — CANDIDATE" subsection (v0.17, added this same transaction), through its own governed candidate lifecycle. Per `-MAJ-02`'s remediation, the governance path is `Executor → Review A + Risk Classification → Product Owner Decision → Execution` (Chapter 0 §3, ADR-042): Review A determines technical disposition/eligibility and may close Review A findings on re-review, but Review A does **not** approve — Product Owner is the sole approval authority, and no Product Owner decision is recorded or implied anywhere in this file.

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

## 3. Candidate alternatives (QG-scoped rationale — `-MAJ-03`: analysis feeding the Testing Convention decision, not itself a competing tooling SSOT)

> **`-MAJ-03` framing note:** the comparison below is this file's own QG-scoped contribution — it explains WHY a property-based mechanism is needed and what I-13/Surfaces 1–2 (§2 above) require of one. It does **not** itself constitute the canonical tool-selection decision. That decision is canonicalized in `docs/engineering/testing.md`'s own "Python property-based testing mechanism — CANDIDATE" subsection (v0.17, added in this same bounded-correction transaction), through Testing Convention's own governed candidate lifecycle (Review A + Risk Classification → Product Owner decision), exactly as `docs/constitution/03-engineering-principles.md` §3.2 establishes Testing Convention as the authority responsible for testing style/tooling decisions.

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
  Verdict: rejected as the RECOMMENDED mechanism — but NOT rejected as
    constitutionally non-compliant. Stated explicitly, per the task's own
    required framing: I-13 requires property-based evidence against the
    authoritative transition graph; I-13 does NOT require shrinking, does
    NOT require Hypothesis by name, and does NOT require any third-party
    framework. A deterministic, stdlib-seeded `random`-based generator
    (Alternative A) is technically CAPABLE of satisfying Chapter 13
    §13.6's property-based category, exactly as it already did for
    market-reference-service's own I-13 evidence — IF its generated
    coverage of Surfaces 1-2 (§2) is genuinely sufficient. The rejection
    here is an ENGINEERING-COST judgment (§4), not a compliance judgment
    — the zero-dependency property that made Alternative A the right
    choice for Go does not, by itself, make it the cheaper or better
    choice for Python once the real cost of hand-building shrinking/
    generation/reproduction machinery is honestly priced in; see §4.

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

## 4. Recommendation feeding the Testing Convention decision (`-MAJ-03`: not a self-standing selection)

> This section states what this QG-scoped analysis RECOMMENDS for canonicalization — it is input to, not a substitute for, the Testing Convention candidate at `docs/engineering/testing.md`'s own "Python property-based testing mechanism — CANDIDATE" subsection (v0.17), which is where the actual mechanism decision lives, is reviewed, and is approved or not.

```text
Recommended for canonicalization: `hypothesis` (Alternative B), used specifically via
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
  effectiveness mechanism — APPROVED" section, and this file's own §8
  below for the ADR-scope treatment of a materially significant
  testing-tool decision.
```

## 5. Deterministic / reproducibility contract (`-MAJ-04` corrected — re-verified against hypothesis 6.168.0's actual installed source this transaction, not from memory; proposed, not yet enforced by any committed config)

```text
`-MAJ-04` correction notice: v0.1 of this candidate asserted that "on a
  failing example [hypothesis] prints... an explicit reproduction
  instruction (@seed(<N>))" as if this happened for every ordinary
  falsifying example. This is FALSE and is retracted. Verified directly
  against the installed 6.168.0 wheel's own source
  (hypothesis/core.py's `seed()` docstring, extracted this transaction):
  "Hypothesis will only print the seed which would reproduce a failure
  IF A TEST FAILS IN AN UNEXPECTED WAY, for instance inside Hypothesis
  internals" — i.e. seed-printing is reserved for internal-error-class
  failures, NOT ordinary property falsification. The corrected contract
  below distinguishes the five separate mechanisms the task named, each
  independently re-verified against hypothesis 6.168.0's real source
  this transaction (files under a scratch `pip download --no-deps`
  extraction, outside the repository, per §9's own non-installation
  discipline):

Deterministic CI generation — `settings.derandomize` (verified,
  hypothesis/_settings.py): "If True, seed Hypothesis' random number
  generator using a HASH OF THE TEST FUNCTION, so that every run will
  test the same set of test cases until you update Hypothesis, Python,
  or the test function." Default `False`; default `True` when Hypothesis
  detects it is running on CI. This is a GENERATION policy only — it
  controls WHICH cases get generated on a given run, deterministically
  across repeated runs of the identical code — it is NOT itself a
  failure-artifact persistence or cross-environment reproduction
  mechanism (a `derandomize=True` run that fails still needs one of the
  three mechanisms below to hand a specific failing case to a developer
  on a different machine/environment).

Shrinking / minimized falsifying example: built into hypothesis,
  deterministic within a single run/replay — every failing generated
  example is automatically reduced to a locally-minimal reproducible
  counterexample before being reported, unconditionally (no additional
  configuration required to enable it). Proposal records shrinking as
  REQUIRED behavior for the EVID-07 properties, i.e. a future install/
  pin transaction MUST NOT disable it via the `phases` setting.

Example database — `settings.database` (verified, hypothesis/_settings.py):
  an `ExampleDatabase` instance; if unset, defaults to a
  `DirectoryBasedExampleDatabase` under `.hypothesis/examples` in the
  current working directory (falls back to an in-memory database if that
  location is unusable); stores failing cases and replays them FIRST on
  subsequent runs before generating new random ones. `None` disables
  storage entirely. This is a LOCAL, machine-scoped convenience cache,
  not a portable/authoritative reproduction artifact — see the
  non-committal rationale below (unchanged from v0.1).

Explicit regression examples — `@example(...)` (verified,
  hypothesis/core.py `class example`): "Add an explicit input to a
  Hypothesis test, which Hypothesis will always try before generating
  random inputs... can also be used to easily reproduce a failure. For
  instance, if Hypothesis reports that `f(n=[0, math.nan])` fails, you
  can add `@example(n=[0, math.nan])` to your test to quickly reproduce
  that failure." Explicit examples run in `Phase.explicit`, do NOT
  shrink, and do not count toward `max_examples`. Proposal: once a
  generated failure is diagnosed as a genuine defect (not a test-quality
  issue), the specific failing input SHOULD be promoted to a permanent
  `@example(...)` on the relevant test — this is the durable,
  portable, version-independent regression-test mechanism, and is the
  form EVID-07's own regression corpus should converge toward over time,
  rather than depending indefinitely on an opaque temporary blob.

Version-specific cross-environment failure reproduction — `print_blob`/
  `@reproduce_failure` (verified, hypothesis/_settings.py +
  hypothesis/core.py): `settings.print_blob` — "If set to True,
  Hypothesis will print code for failing test cases that can be used
  with `@reproduce_failure` to reproduce the failing test case." Default
  `False`; default `True` when running on CI. `reproduce_failure(version:
  str, blob: bytes)` — "Run the test case corresponding to the binary
  `blob` in order to reproduce a failure... A test decorated with
  `@reproduce_failure` always runs exactly one test case... Hypothesis
  will print an `@reproduce_failure` decorator if `settings.print_blob`
  is True." CRITICALLY, verified directly from the docstring: "no
  compatibility guarantees are made across Hypothesis versions, and
  `@reproduce_failure` will error if used on a different Hypothesis
  version than it was created for" — a printed blob is tied to the
  EXACT hypothesis version that produced it, and the docstring itself
  states it "is not intended to be a permanent addition to your test
  suite," only a temporary tool for reproducing one specific failure
  before either fixing the defect or promoting the case to `@example`.
  Proposal (the explicit mechanism the task requires): CI runs with
  `print_blob` at its CI-default `True` (or explicitly forced `True` in
  the "ci" settings profile, §below, regardless of environment
  auto-detection) so that any CI failure's terminal output already
  contains a ready-to-paste `@reproduce_failure(version, blob)` snippet;
  that snippet is captured VERBATIM into the defect record (matching
  Chapter 13 §13.10's flaky-test discipline of not silently retrying)
  and is the mechanism used to reproduce the exact failing case locally
  — NOT a printed `@seed(...)` line, which (per the correction above)
  ordinary property failures do not produce.

Generated-input bounds: proposal — two named `hypothesis.settings`
  profiles (registered via `settings.register_profile`, standard
  hypothesis pattern), mirroring this repository's own dev/CI split
  already used elsewhere (e.g. mutmut's own separate dev/measurement
  invocation discipline):
    "dev" profile — interactive default, local `.hypothesis` example
      database enabled (developer convenience, faster iteration on
      previously-failing examples), `max_examples` at hypothesis's own
      library default.
    "ci" profile — `derandomize=True` (deterministic case GENERATION
      across repeated runs, per the correction above — a generation
      policy, not a failure-persistence mechanism on its own),
      `print_blob=True` (explicit, not merely relying on CI
      auto-detection — the cross-environment failure-reproduction
      mechanism, per the correction above), `database=None` (no
      local-machine-dependent state persisted/read — avoids non-hermetic
      behavior differences between machines/CI workers; reproduction
      instead flows through the printed `@reproduce_failure` blob),
      explicit `max_examples` bound (proposal: 200 per property, the same
      order of magnitude as the Go precedent's 150-300 trials/machine —
      exact number to be finalized at the install/pin transaction against
      real measured runtime, not fixed here as a Constitution-adjacent
      numeric commitment).
  Rationale for NOT committing the `.hypothesis` example database to the
  repository: it is a local cache of previously-failing inputs, not a
  reproducibility mechanism this repository's own I-12/SSOT discipline
  would want to treat as authoritative — the PRINTED `@reproduce_failure`
  blob (`-MAJ-04`, above) is the authoritative, portable, per-failure
  reproduction artifact, and a promoted `@example(...)` is the
  authoritative, durable, version-independent one; consistent with how
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

Concurrent transitions — `-MAJ-05` corrected disposition: **A. NOT_APPLICABLE**
  at the Feature Engine module boundary, on AUTHORITATIVE-CONTRACT
  grounds (not on the absence-of-implementation-primitives reasoning v0.1
  wrongly relied on as its sole basis).

  I-13's own clause is semantic, not implementation-detail: "concurrent/
  competing transition attempts on the same entity must resolve
  deterministically under the authoritative version/concurrency
  contract" — the question is whether such competing attempts can reach
  Feature Engine's own state-machine boundary AT ALL, not whether
  Feature Engine's own source file happens to import a lock primitive.

  Authoritative basis, freshly resolved this transaction against Chapter
  8 (docs/constitution/08-event-model.md v4.8, Locked) §8.3 (verified
  directly, this transaction, not from memory):
    "Một stream là một ordered log partition có đúng MỘT writer
    authority cấp phát sequence" (line 222) — EVERY stream, including
    whatever stream(s) carry FeatureComputed/FeatureFactInvalidated, has
    EXACTLY one writer authority resolvable at any point in time.
    "Mỗi stream chỉ có 1 writer authority (điều kiện để sequence
    contiguous)" (line 299) — restated as a structural precondition,
    not a recommendation.
    Writer-authority handoff invariant (lines 348-356): "Không có
    khoảng thời gian nào hai writer cùng authoritative" (rule 5 — never
    a window where two writers are simultaneously authoritative), sequence
    assigned ATOMICALLY at append time (line 363 — "reserve-then-crash sẽ
    tạo lỗ hổng vĩnh viễn" is explicitly rejected), and handoff failure
    must itself be fail-safe (I-6).
  Consequence for Feature Engine specifically: because every stream
  (Chapter 8-owned, platform-wide, Locked) structurally cannot have two
  independently-authoritative writers appending conflicting events at
  the same time, two competing/conflicting FeatureComputed/
  FeatureFactInvalidated transitions for the SAME (feature_subject_id,
  effective_window) lineage head CANNOT be independently, concurrently
  appended to the authoritative event log in the first place — the
  "version/concurrency contract" I-13 requires is Chapter 8's own
  single-writer-authority + atomic-sequence-assignment contract,
  ALREADY resolved and Locked, and it operates one level up the stack,
  at the event-log append boundary, BEFORE any event ever reaches
  Feature Engine's own `on_feature_computed`/`on_feature_invalidated`
  handlers. Feature Engine's handlers only ever apply an already-
  serialized, single-writer-produced sequence — there is no "competing
  transition attempt" for them to resolve, because Chapter 8 has already
  made that outcome structurally impossible upstream. This is an
  architecture/ownership fact about where the guarantee lives (Chapter
  8, universally, for every stream), not a gap this candidate is
  deferring or a claim invented from an absence of code.
  Corroborating (not sole) evidence: a fresh grep across
  src/feature_engine/*.py for `concurren`, `expected_version`,
  `optimistic`, `threading`, `asyncio`, `Lock(` this transaction returned
  ZERO hits — CONSISTENT with (not proof of) the architectural
  determination above: Feature Engine's own implementation correctly
  contains no concurrency-conflict-resolution code of its own, because it
  correctly does not own that responsibility.

  Explicitly NOT the same question as "interleaved," which remains
  genuinely APPLICABLE and is covered above (sequence/order constraints,
  §6 "Sequence/order constraints") — interleaved ARRIVAL ORDER of
  already-serialized, single-writer-produced facts at one computation
  cursor is real and testable (e.g. candle vs. swing-confirmation
  delivery order); that is a property about ORDER of an already-
  guaranteed-serial stream, not about resolving a genuine WRITE conflict,
  which Chapter 8 has already ruled out. Per §13.8 fail-closed
  discipline, this is an explicit, contract-backed "not applicable"
  determination (Chapter 8 §8.3, cited above), not a silent skip and not
  a grep-only claim.
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

## 8. ADR Scope Rule — `-MAJ-01` corrected, fresh run (Chapter 0 §4b, this transaction's own boundary, not copied from v0.1 or from the task's own hint)

```text
`-MAJ-01` correction notice: v0.1 of this candidate framed
  Chapter 3 §3.2 and Chapter 13 §13.3/§13.14 as a "carve-out" exempting
  tool/vendor selection from Chapter 0 §4b entirely, and concluded
  `ADR_NOT_REQUIRED` on that basis. This framing is WRONG and is
  retracted. Directly on point, verified fresh this transaction against
  docs/engineering/testing.md's own "Python Mutation Compatibility
  Candidate" v0.15 correction (`P3-PY-MUT-COMPAT-A-MAJ-02`): that exact
  correction already established, for this same repository, that
  "Chapter 3 §3.2 establishes Testing Convention as the AUTHORITY for
  testing style/tooling decisions -- it does NOT exempt those decisions
  from Chapter 0 §4b's own ADR Scope Rule" -- Testing Convention decides
  WITHIN §4b's framework, never outside it. That same correction also
  explicitly preserved the ORIGINAL coverage.py/gobco/mutmut mechanism-
  SELECTION decisions as "settled, unchallenged, and out of scope" at
  their own `ADR_NOT_REQUIRED` disposition -- it did not blanket-
  reclassify every testing-tool decision to `ADR_OPTIONAL`. The task's
  own hinted disposition (`ADR_OPTIONAL — ADR NOT AUTHORED`) is
  therefore NOT copied blindly here -- it is independently re-derived
  below, on hypothesis's own actual characteristics, against the SAME
  corrected criteria testing.md's own v0.15 correction used.

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
Production/event/API/domain contract change    | NONE — no event schema,
                                                  no domain concept, no
                                                  published contract
                                                  touched.
Dependency graph/invariant/governance-process  | NONE beyond the single
  change                                         new dev-only PyPI leaf
                                                  dependency itself (§7).
Cross-module authority                         | NONE — explicitly,
                                                  contractually FEATURE-
                                                  ENGINE-ONLY, same
                                                  scoping discipline as
                                                  the mutmut compatibility
                                                  candidate's own
                                                  corrected classification.
Reversible                                     | YES — single-step
                                                  removal (delete the
                                                  pyproject.toml/lock
                                                  entries and the tests
                                                  that use it).
Edit/supersede a Locked ADR                    | NO — no ADR file touched.
Materially significant internal testing-tool   | YES, independently
  decision (the criterion that actually decides    assessed on
  ADR Optional vs. Not Required, per testing.md's   hypothesis's OWN
  own v0.15 correction, not inherited)             characteristics
                                                  (reasoning below) — this
                                                  is the one dimension
                                                  where hypothesis differs
                                                  materially from
                                                  coverage.py/mutmut/
                                                  gobco's own original
                                                  selections.

Why "materially significant," specifically (not by label-copying the
  mutmut compat-shim outcome, but by the SAME underlying criterion
  testing.md's own v0.15 correction used — does the decision change how
  test EXECUTION itself behaves, versus merely instrumenting/observing
  the existing deterministic suite):
  coverage.py instruments already-existing, already-deterministic
    example-based tests to measure which lines/branches executed -- it
    does not change what a test DOES or generate new test cases.
  mutmut's own original selection runs the EXISTING test suite,
    unmodified, against synthetically mutated production code -- again,
    it does not change how Feature Engine's own tests generate or
    execute cases; the mutmut COMPATIBILITY SHIM (correctly ADR_OPTIONAL)
    was significant specifically because it changed HOW an already-
    approved mechanism's own sanity-check phase behaves internally.
  hypothesis is categorically different in kind: adopting it introduces
    RANDOMIZED-BUT-SEEDED, GENERATED test-case execution into Feature
    Engine's own test suite for the first time -- test cases that did
    not exist as fixed examples before, a new `RuleBasedStateMachine`/
    `@given` execution model, a new Flaky-detection failure category
    (§5) that does not exist for any current example-based test, and a
    dev/CI settings-profile split (§5) governing how MANY and WHICH
    cases actually run. This changes what "running Feature Engine's test
    suite" DOES, not merely what it measures or what it runs against --
    the same class of "substantive change to tooling behavior" testing.md's
    own v0.15 correction identified as crossing from Not-Required into
    Optional-but-significant territory, independently re-derived here
    for hypothesis's own actual properties rather than copied from that
    prior finding's conclusion.

Result: `ADR_OPTIONAL — ADR NOT AUTHORED`.
  Materially significant (reasoning above) + one module only + no
  contract change + reversible + no cross-module authority maps DIRECTLY
  to Chapter 0 §4b's "ADR Optional: thay đổi nội bộ một module không đổi
  contract nhưng ảnh hưởng đáng kể" category -- not to "ADR Not
  Required" (typo/formatting/no-behavior-change refactor) and not to
  "ADR Required" (no Platform Invariant/Event Schema/Module Taxonomy/
  Governance-process/>1-module/Locked-ADR trigger fires, per the table
  above). This candidate deliberately chooses ADR NOT AUTHORED, available
  specifically BECAUSE the classification is Optional (not because
  Optional exempts consideration) -- exactly the same deliberate-choice
  structure testing.md's own v0.15 correction recorded for the mutmut
  compatibility candidate. This is NOT inherited from v0.1's
  `ADR_NOT_REQUIRED`, NOT copied blindly from the task's own hinted
  disposition, and NOT a blanket reclassification of coverage.py/gobco/
  mutmut's own original, already-settled `ADR_NOT_REQUIRED` selections
  (unchallenged, out of scope for this correction, same non-
  retroactivity discipline testing.md's own v0.15 correction applied to
  itself). A future installation/pinning transaction, or any proposal to
  extend this mechanism beyond feature-engine, MUST independently re-run
  Chapter 0 §4b at its own boundary and MAY reach a different conclusion.
  This candidate authors NO ADR file at this transaction.
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
No Product Owner Approval Gate decision performed or implied, and NONE
  invented for this bounded correction either — per Chapter 13 §13.1
  (Quality Gate evidence ≠ Approval Gate consumption) AND because,
  per `-MAJ-02`, only Product Owner may approve, and no Product Owner
  decision has occurred on this candidate or on the testing.md v0.17
  "Python property-based testing mechanism — CANDIDATE" subsection it
  now references (added this same transaction).
No mutmut/coverage.py/gobco candidate or approval history touched —
  verified byte-unchanged (this correction only ADDS one new subsection
  to docs/engineering/testing.md (v0.17) — it does not edit any
  existing section's content).
No self-closure of `P3-FEATURE-QG-EVID07-A-MAJ-01` through `-MAJ-05` —
  all five recorded `REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`
  (frontmatter, banner), never `CLOSED`, per `-MAJ-02`'s own corrected
  governance path (Review A determines disposition on re-review; this
  Executor transaction does not).
```

## 10. Self-consistency check (performed before commit)

```text
- §2's cited source identifiers (unchanged by this correction, re-
  confirmed still present in current source, this transaction) were
  originally verified via direct `grep -n` against src/feature_engine/*.py
  and remain accurate — not touched by this correction.
- §3/§5/§7's hypothesis/sortedcontainers version, license, Requires-
  Python/Dist claims (unchanged, still 6.168.0/2.4.0 — the candidate
  landscape did not need re-checking for this bounded correction, since
  no install/pin is proposed to execute at this boundary) remain as
  originally verified via `pip index versions`/`pip download --no-deps`.
- `-MAJ-04`'s corrected §5 API claims (print_blob, reproduce_failure,
  derandomize, database, @example, Flaky) were verified this transaction
  directly against hypothesis 6.168.0's own extracted wheel source
  (hypothesis/core.py, hypothesis/_settings.py, hypothesis/errors.py) —
  not from memory, and not merely restated from the task's own prompt
  text.
- `-MAJ-05`'s corrected §6 concurrent-transition disposition is backed by
  a direct reading of Chapter 8 §8.3 (docs/constitution/08-event-model.md,
  Locked, single-writer-authority + atomic-sequence-assignment
  invariants, lines 222/299/348-363, this transaction) — grep is now
  cited only as corroborating, not as the architectural proof.
- `-MAJ-01`'s corrected §8 ADR-scope conclusion was cross-checked
  directly against docs/engineering/testing.md's own v0.15 correction
  text (`P3-PY-MUT-COMPAT-A-MAJ-02`) this transaction, applying its
  corrected CRITERION (does the decision change test-execution behavior,
  not merely instrument/observe it) to hypothesis's own characteristics
  — not copied from that finding's own label, and not copied from the
  task's own hinted disposition without independent re-derivation.
- `-MAJ-03`'s SSOT correction is internally consistent: §3/§4 of this
  file now explicitly frame themselves as QG-scoped input to, not a
  substitute for, the testing.md v0.17 candidate subsection (added this
  same transaction) — verified by re-reading both files together before
  commit.
- No numeric Chapter 13 threshold is duplicated into this candidate (no
  such threshold exists for the Property-based category — §13.6 states
  the category is required "khi áp dụng," not a percentage).
- Internally coherent: no section of this candidate asserts EVID-07 is
  closed, asserts a dependency was installed, asserts a Product Owner
  decision occurred, or asserts Review A itself approves anything —
  cross-checked against §9's own explicit negative list and against
  `-MAJ-02`'s corrected banner.
```

## 11. Next governed step (not performed by this transaction) — `-MAJ-02`/`-MAJ-03` corrected governance path

```text
1. Bounded Review A re-review of this correction (this transaction):
   determines whether `-MAJ-01` through `-MAJ-05` are genuinely
   remediated (CLOSED) or require further correction. Review A
   determines technical disposition/eligibility only — it does not
   approve this candidate or the testing.md v0.17 candidate subsection,
   per Chapter 0 §3.
2. If Review A finds the corrections insufficient: a further bounded
   correction transaction remediates the residual — not self-closed by
   the correction author, same discipline as this transaction.
3. Once Review A closes all five findings CLEAN: Risk Classification
   (R0/R1/R2, per ADR-042) is recorded for the testing.md candidate
   decision specifically (the actual mechanism/tool decision, per
   `-MAJ-03` — not for this QG-scoped file, which makes no decision of
   its own to classify).
4. Product Owner decision on the testing.md candidate (mechanism
   selection only — still no installation) — the SOLE approval authority,
   per `-MAJ-02`; not Review A, not this Executor.
5. ONLY AFTER the mechanism becomes effective in testing.md (Approved):
   a SEPARATE, later, install/pinning transaction executes testing.md's
   own installation-time verification contract (§7 of this file feeds
   that contract's content but does not itself authorize installation),
   actually adds `hypothesis`/`sortedcontainers` to pyproject.toml and
   requirements-dev.lock.txt, and installs into python/feature-engine's
   environment.
6. A SEPARATE, later, test-authoring transaction writes the actual
   property-based tests against Surfaces 1–2 (§2/§6).
7. A SEPARATE, later, formal Chapter 13 §13.9 evidence transaction (same
   pattern as feature-engine-evid05b-formal-evidence-001.md) records
   fresh measurement and, only if it genuinely passes, closes
   `P3-FEATURE-QG-EVID-07`.
   None of steps 1-7 is performed by this transaction.
```
