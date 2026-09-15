---
id: feature-engine-evid07-property-based-mechanism-candidate-001
title: "Feature Engine — `P3-FEATURE-QG-EVID-07` Python Property-Based Testing Mechanism — CANDIDATE"
candidate_version: "0.5"
status: "EVIDENCE PRODUCED — PENDING REVIEW A VALIDATION — CORRECTION-CHAIN ROOT-CAUSE CONSOLIDATION + STABILIZATION 001 (P3-FEATURE-QG-EVID07-A-MAJ-01/-02/-03/-04/-05 CLOSED — REVIEW A VALIDATED; -MAJ-06/-07/-08/-MIN-01 REMEDIATED — PENDING REVIEW A RE-REVIEW; formal I-13 property evidence produced against commit e901f1857b1049ebc0bb4bdfd7a047e40e1174ed)"
performed_at: "2026-09-11"
repository_head_at_authoring: "310a83e22c868611028e5804c524fb5a4e9f57da"
stabilization_001:
  role: "Feature Engine EVID-07 Root-Cause Consolidation + Stabilization Executor"
  applied_at_repository_head_a2: "e901f1857b1049ebc0bb4bdfd7a047e40e1174ed"
  a2_parent: "86470d105f0608f0708be7c694a6f331486edf09"
  corrected_candidate_blob_before_correction: "42aee062841d5f389ec213a056d374b717a1a4de"
  superseded_evidence_attempt: "27bd472efeab9a9538bde62ccfeca5c0a1ce48c9 (Commit A, superseded -- see §13 root-cause record)"
  review_a_result_addressed:
    disposition: "REVISION_REQUIRED — 0 Blocker / 3 Major / 1 Minor"
    risk: "R1"
    findings:
      - id: P3-FEATURE-QG-EVID07-A-MAJ-01
        status: "CLOSED — REVIEW A VALIDATED"
      - id: P3-FEATURE-QG-EVID07-A-MAJ-02
        status: "CLOSED — REVIEW A VALIDATED"
      - id: P3-FEATURE-QG-EVID07-A-MAJ-03
        status: "CLOSED — REVIEW A VALIDATED"
      - id: P3-FEATURE-QG-EVID07-A-MAJ-04
        status: "CLOSED — REVIEW A VALIDATED"
      - id: P3-FEATURE-QG-EVID07-A-MAJ-05
        status: "CLOSED — REVIEW A VALIDATED"
      - id: P3-FEATURE-QG-EVID07-A-MAJ-06
        status: "REMEDIATED — PENDING REVIEW A RE-REVIEW"
      - id: P3-FEATURE-QG-EVID07-A-MAJ-07
        status: "REMEDIATED — PENDING REVIEW A RE-REVIEW"
      - id: P3-FEATURE-QG-EVID07-A-MAJ-08
        status: "REMEDIATED — PENDING REVIEW A RE-REVIEW"
      - id: P3-FEATURE-QG-EVID07-A-MIN-01
        status: "REMEDIATED — PENDING REVIEW A RE-REVIEW"
  r0_factual_correction:
    subject: "Testing Convention v0.17 Product Owner decision date"
    was: "2026-09-14"
    corrected_to: "2026-09-15"
    decision_text: "unchanged and valid"
bounded_correction_003:
  applied_at_repository_head: "27bd472efeab9a9538bde62ccfeca5c0a1ce48c9"
  corrected_candidate_blob_before_correction: "bf347512d649ee9d6284851a7e10a95fd3e3df51"
  reviewer_findings_addressed:
    - id: P3-FEATURE-QG-EVID07-A-MAJ-01
      status: "CLOSED — REVIEW A VALIDATED"
    - id: P3-FEATURE-QG-EVID07-A-MAJ-02
      status: "CLOSED — REVIEW A VALIDATED"
    - id: P3-FEATURE-QG-EVID07-A-MAJ-03
      status: "CLOSED — REVIEW A VALIDATED"
    - id: P3-FEATURE-QG-EVID07-A-MAJ-04
      status: "CLOSED — REVIEW A VALIDATED"
    - id: P3-FEATURE-QG-EVID07-A-MAJ-05
      status: "REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW"
bounded_correction_001:
  applied_at_repository_head: "cd9d2684b0a315cde1bd429f3d4b0b07f8fe96d5"
  corrected_candidate_blob_before_correction: "f3bdb9ff82e3e88456792c4e06da48688a5bd6b4"
  reviewer_findings_addressed:
    - id: P3-FEATURE-QG-EVID07-A-MAJ-01
      status: "CLOSED — REVIEW A VALIDATED"
    - id: P3-FEATURE-QG-EVID07-A-MAJ-02
      status: "CLOSED — REVIEW A VALIDATED"
    - id: P3-FEATURE-QG-EVID07-A-MAJ-03
      status: "CLOSED — REVIEW A VALIDATED"
    - id: P3-FEATURE-QG-EVID07-A-MAJ-04
      status: "REOPENED — CORRECTION REQUIRED (residual contradiction found on re-review)"
    - id: P3-FEATURE-QG-EVID07-A-MAJ-05
      status: "REOPENED — CORRECTION REQUIRED (prior remediation insufficient)"
bounded_correction_002:
  applied_at_repository_head: "c8e5d2e9ab5e9bf5e8000004c58d1005f7ccc287"
  corrected_candidate_blob_before_correction: "f83911161783fc85d596ffd80ec143f3e446888a"
  reviewer_findings_addressed:
    - id: P3-FEATURE-QG-EVID07-A-MAJ-04
      status: "REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW"
    - id: P3-FEATURE-QG-EVID07-A-MAJ-05
      status: "REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW"
---

# Feature Engine — `P3-FEATURE-QG-EVID-07` Python Property-Based Testing Mechanism — CANDIDATE 001

> **CORRECTION-CHAIN ROOT-CAUSE CONSOLIDATION + STABILIZATION 001 (this transaction)** — vai trò: `Feature Engine EVID-07 Root-Cause Consolidation + Stabilization Executor`. Correction 003 did not stabilize: bounded Review A re-review found `-MAJ-01`/`-02`/`-03`/`-04`/`-05` **CLOSED — REVIEW A VALIDATED**, but surfaced three NEW Major findings (`-MAJ-06`/`-07`/`-08`) and one new Minor (`-MIN-01`) on the formal evidence itself — disposition **`REVISION_REQUIRED — 0 Blocker / 3 Major / 1 Minor`**, Risk `R1`. Per instruction, this is **not** a normal `bounded correction 004` — it is ONE consolidated root-cause-consolidation + stabilization transaction: root causes recorded below (§13), exact defects corrected, formal evidence rerun against a fresh exact executable commit (**Commit A2**, `e901f1857b1049ebc0bb4bdfd7a047e40e1174ed`, parent `86470d105f0608f0708be7c694a6f331486edf09`), corrected evidence recorded in this SAME following docs-only commit (**Commit B2**). The previously-recorded formal evidence result (against Commit A, `27bd472efeab9a9538bde62ccfeca5c0a1ce48c9`) is **superseded** — §12 below is replaced wholesale with A2's own exact evidence, not merged/appended alongside the stale result. An additional R0 factual defect is folded into this same transaction (per instruction, not a separate transaction): the Testing Convention v0.17 Product Owner decision date was recorded as `2026-09-14`; the actual decision in the governing conversation occurred on `2026-09-15` — corrected in `docs/engineering/testing.md` (Commit A2) and reconciled here/in MANIFEST/CHANGELOG (Commit B2); the decision text itself is unchanged and valid. No new ADR, no Review B, no new Product Owner decision, no production `src/feature_engine/**` change, no dependency version change — same discipline as every prior transaction in this chain.
>
> `P3-FEATURE-QG-EVID07-A-MAJ-01: CLOSED — REVIEW A VALIDATED`
> `P3-FEATURE-QG-EVID07-A-MAJ-02: CLOSED — REVIEW A VALIDATED`
> `P3-FEATURE-QG-EVID07-A-MAJ-03: CLOSED — REVIEW A VALIDATED`
> `P3-FEATURE-QG-EVID07-A-MAJ-04: CLOSED — REVIEW A VALIDATED`
> `P3-FEATURE-QG-EVID07-A-MAJ-05: CLOSED — REVIEW A VALIDATED`
> `P3-FEATURE-QG-EVID07-A-MAJ-06: REMEDIATED — PENDING REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID07-A-MAJ-07: REMEDIATED — PENDING REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID07-A-MAJ-08: REMEDIATED — PENDING REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID07-A-MIN-01: REMEDIATED — PENDING REVIEW A RE-REVIEW`
>
> `P3-FEATURE-QG-EVID-07: EVIDENCE PRODUCED — PENDING REVIEW A VALIDATION` (unchanged label — none of the four new findings is self-closed, and this transaction does not self-close its own evidence finding; closure remains Review A's own determination, per Chapter 0 §3).

> **Bounded correction 003 (this transaction) + formal evidence record** — vai trò: `Feature Engine EVID-07 Integrated Execution Executor`. Records, as already-completed governance input to this integrated transaction (not re-run, not re-litigated here): (1) Product Owner decision (verbatim) — **"APPROVE Testing Convention v0.17 — Python property-based testing mechanism: Hypothesis — ADR_OPTIONAL, ADR NOT AUTHORED."** — decision date `2026-09-14`, recorded in full in `docs/engineering/testing.md`'s own v0.17 approval banner (reviewed boundary `81605fd1ca099eae48b937ced3c775e271dee2e2`, reviewed blob `708744f0464720cb14ceafbe75bb422200a57820`, Review A CLEAN 0 Blocker / 0 Major / 0 Minor, Risk Classification R1, no Independent Review B required at R1); (2) ADR-043 implementation Review A's own CLEAN 0/0/0 final disposition (reviewed boundary `81605fd1ca099eae48b937ced3c775e271dee2e2`), recorded in full in `python/feature-engine/README.md`; (3) Review A's re-review disposition on bounded correction 002 (mechanically recorded per the established convention this file already uses for correction 002 itself — no separate transcript file, consistent with the incoming task input): `-MAJ-01`/`-MAJ-02`/`-MAJ-03` remain **CLOSED — REVIEW A VALIDATED** (not re-litigated, not reopened absent a fresh direct contradiction, none found); `-MAJ-04` (Hypothesis reproducibility contract, §5) is now **CLOSED — REVIEW A VALIDATED**; `-MAJ-05` (concurrent/competing-transition applicability, §6) was found on re-review to still rest on a rationale that has since become stale now that ADR-043's actual per-subject ownership runtime is implemented and Review-A-validated — remediated again in this transaction (below), **not** closed by this transaction.
>
> Same integrated transaction (Commit `27bd472efeab9a9538bde62ccfeca5c0a1ce48c9`, this file's own boundary): `hypothesis==6.168.0` / `sortedcontainers==2.4.0` installed and pinned (`python/feature-engine/pyproject.toml` `[project.optional-dependencies].dev`; `requirements-dev.lock.txt`), formal I-13 property-based evidence authored (`python/feature-engine/tests/test_i13_properties.py`, 18 tests across all 6 property categories §6 requires), and formal evidence recorded against the exact pushed boundary — full record in §12 below. This corrects/supersedes §9's now-stale "Not performed" claims about installation/authoring/testing.md-editing (those were true when §9 was written, prior to this transaction; §9 itself is left textually unedited, as historical record, with a pointer notice added) and supersedes §6's `-MAJ-05` "one instance per Feature subject" rationale with the current, Review-A-validated ADR-043 authority stack (§6 correction notice, below).
>
> `P3-FEATURE-QG-EVID07-A-MAJ-01: CLOSED — REVIEW A VALIDATED`
> `P3-FEATURE-QG-EVID07-A-MAJ-02: CLOSED — REVIEW A VALIDATED`
> `P3-FEATURE-QG-EVID07-A-MAJ-03: CLOSED — REVIEW A VALIDATED`
> `P3-FEATURE-QG-EVID07-A-MAJ-04: CLOSED — REVIEW A VALIDATED`
> `P3-FEATURE-QG-EVID07-A-MAJ-05: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`
>
> `P3-FEATURE-QG-EVID-07: EVIDENCE PRODUCED — PENDING REVIEW A VALIDATION` (not `CLOSED`, not `FINAL PASS` — this transaction does not self-close its own evidence finding; that determination is Review A's own, per Chapter 0 §3, same governance path `-MAJ-02` already established for this file).

> **Bounded correction 002 (this transaction)** — vai trò: `Feature Engine EVID-07 Property-Based Mechanism Candidate Bounded Correction Executor`. Records Review A's re-review disposition on bounded correction 001 (reviewed blob `f83911161783fc85d596ffd80ec143f3e446888a`, boundary `c8e5d2e9ab5e9bf5e8000004c58d1005f7ccc287` — mechanically recorded per the established convention throughout this repository's Review A dispositions, no separate transcript file, consistent with the incoming task input): `-MAJ-01`/`-MAJ-02`/`-MAJ-03` **CLOSED — REVIEW A VALIDATED** (not re-litigated in this transaction; not reopened absent a fresh direct contradiction, and none was found on fresh re-read). `-MAJ-04`/`-MAJ-05` remained **OPEN — CORRECTION REQUIRED**, remediated here: `-MAJ-04` (a surviving contradictory sentence in §3 Alternative B — "a printed, directly-reusable reproduction seed" — was missed by correction 001's own fix to §5; found via a full-file search for every `seed`/`reproduce_failure`/`print_blob`/`derandomize` occurrence, per instruction, not just the one sentence Review A cited; corrected to match §5's own accurate contract). `-MAJ-05` (the prior `NOT_APPLICABLE` disposition inferred "single writer authority → competing transitions structurally impossible," which conflates Chapter 8 §8.3's STREAM-level writer-authority/append-ordering guarantee with a DOMAIN-level version/concurrency contract I-13 actually requires; re-derived from `feature.md` §9 rule 6 (no fork — an existing Domain Contract semantic, not invented) plus the actual Feature Engine implementation's own verified, pre-emission fail-closed rejection of conflicting transitions — disposition corrected to **APPLICABLE**, satisfied by the SAME evidence category already scoped for Surface 1's illegal-transition/fork case, explicitly distinguished from interleaving). Neither finding is self-closed here — closure is Review A's own determination on re-review, per Chapter 0 §3.
>
> `P3-FEATURE-QG-EVID07-A-MAJ-01: CLOSED — REVIEW A VALIDATED`
> `P3-FEATURE-QG-EVID07-A-MAJ-02: CLOSED — REVIEW A VALIDATED`
> `P3-FEATURE-QG-EVID07-A-MAJ-03: CLOSED — REVIEW A VALIDATED`
> `P3-FEATURE-QG-EVID07-A-MAJ-04: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID07-A-MAJ-05: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`

> **Bounded correction 001** — vai trò: `Feature Engine EVID-07 Property-Based Mechanism Candidate Bounded Correction Executor`. Remediates five Review A findings against candidate v0.1 (reviewed blob `f3bdb9ff82e3e88456792c4e06da48688a5bd6b4`, boundary `cd9d2684b0a315cde1bd429f3d4b0b07f8fe96d5`): `-MAJ-01` (ADR Scope misclassification — corrected `ADR_NOT_REQUIRED` → `ADR_OPTIONAL — ADR NOT AUTHORED`, and removed the "carve-out" mischaracterization of Chapter 3 §3.2/Chapter 13 §13.14); `-MAJ-02` (approval-authority misstatement — removed every claim that Review A approves or closes this candidate; corrected to `Executor → Review A + Risk Classification → Product Owner Decision → Execution`, Product Owner sole approval authority); `-MAJ-03` (competing tooling SSOT — this file is now QG-scoped rationale only; the actual mechanism/tool decision is canonicalized into `docs/engineering/testing.md` v0.17 candidate section, added in this same bounded transaction as one coherent semantic decision, not a second unrelated one); `-MAJ-04` (Hypothesis reproducibility contract — corrected after re-reading hypothesis 6.168.0's actual source this transaction: removed the false claim that every ordinary falsifying example prints a reusable seed; distinguished deterministic CI generation (`derandomize`) from failure-artifact persistence (`print_blob`/`@reproduce_failure`, version-locked, temporary) from durable regression capture (`@example`)); `-MAJ-05` (I-13 concurrent-transition applicability — replaced grep-only reasoning with the authoritative basis: Chapter 8 §8.3's Locked single-writer-authority + atomic-sequence-assignment contract, which structurally prevents competing transitions from independently reaching any stream's append point, Feature Engine's included). None of the five findings is self-closed here — closure is Review A's own determination on re-review, per Chapter 0 §3.
>
> `P3-FEATURE-QG-EVID07-A-MAJ-01: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID07-A-MAJ-02: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID07-A-MAJ-03: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID07-A-MAJ-04: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`
> `P3-FEATURE-QG-EVID07-A-MAJ-05: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW`

> **Status banner (superseded by bounded correction 003 — historical, left unedited for the record):** `CANDIDATE / NOT EFFECTIVE — BOUNDED CORRECTION 002 PENDING REVIEW A RE-REVIEW (MAJ-04/-05 ONLY)`. This remains a **QG-scoped analysis/rationale transaction only** — vai trò: `Feature Engine EVID-07 Property-Based Mechanism Candidate Author`. It does **not** install any dependency, does **not** edit `pyproject.toml`/`requirements-dev.lock.txt`, does **not** modify any Feature Engine production or test file, does **not** measure anything, and does **not** close `P3-FEATURE-QG-EVID-07`. Per `-MAJ-03`'s remediation (below), this file does **not** itself canonicalize the mechanism/tool decision — that decision is canonicalized in `docs/engineering/testing.md`'s own "Python property-based testing mechanism — CANDIDATE" subsection (v0.17, added this same transaction), through its own governed candidate lifecycle. Per `-MAJ-02`'s remediation, the governance path is `Executor → Review A + Risk Classification → Product Owner Decision → Execution` (Chapter 0 §3, ADR-042): Review A determines technical disposition/eligibility and may close Review A findings on re-review, but Review A does **not** approve — Product Owner is the sole approval authority, and no Product Owner decision is recorded or implied anywhere in this file.
>
> **Status banner (superseded by stabilization 001 — historical, left unedited for the record):** `EVIDENCE PRODUCED — PENDING REVIEW A VALIDATION — CANDIDATE v0.4`. This transaction is no longer QG-scoped-rationale-only: the Testing Convention v0.17 mechanism (Hypothesis) received its Product Owner decision on `2026-09-14` (recorded in `testing.md`), was installed/pinned into `python/feature-engine/pyproject.toml` and `requirements-dev.lock.txt`, and formal I-13 property-based evidence was authored (`tests/test_i13_properties.py`) and run against the exact committed boundary `27bd472efeab9a9538bde62ccfeca5c0a1ce48c9` — full record in §12. `P3-FEATURE-QG-EVID-07` is recorded **`EVIDENCE PRODUCED — PENDING REVIEW A VALIDATION`**, explicitly not `CLOSED` and not `FINAL PASS` — closure remains Review A's own determination, per Chapter 0 §3 and this file's own `-MAJ-02` governance path (unchanged). The Feature Engine module remains **NOT APPROVED**; LIVE remains **NOT_AUTHORIZED**.
>
> **Current status banner (stabilization 001, this transaction):** `EVIDENCE PRODUCED — PENDING REVIEW A VALIDATION — CANDIDATE v0.5`. The `27bd472e...` evidence above is **superseded** — Review A found it `REVISION_REQUIRED` (`-MAJ-06`/`-07`/`-08`/`-MIN-01`). Root causes recorded in §13; defects corrected against Commit A2 `e901f1857b1049ebc0bb4bdfd7a047e40e1174ed`; formal evidence rerun and recorded fresh in §12 (wholesale replacement, not an appendix to the stale result). Testing Convention v0.17's Product Owner decision date is now correctly recorded as `2026-09-15` (R0 correction, §13 RC-5; decision text unchanged). `P3-FEATURE-QG-EVID-07` remains **`EVIDENCE PRODUCED — PENDING REVIEW A VALIDATION`** — not `CLOSED`, not `FINAL PASS`. The Feature Engine module remains **NOT APPROVED**; LIVE remains **NOT_AUTHORIZED**.

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
      deterministic shrinking to a minimal failing example within a run,
      and — `-MAJ-04` correction, this transaction: NOT an automatically-
      printed reproduction seed for ordinary falsifying examples (that
      claim was false and is retracted here as well as in §5) — an
      explicit, version-locked cross-environment reproduction blob
      (`settings.print_blob` + `@reproduce_failure(version, blob)`, both
      re-verified against hypothesis 6.168.0's own installed source in
      §5, correction 001) for reproducing a specific failing case, plus
      `@example(...)` for promoting a diagnosed failure to a durable,
      version-independent regression check. See §5 for the full,
      corrected reproducibility contract — this sentence is intentionally
      kept consistent with it, not a separate restatement.
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

`-MAJ-05` bounded correction 003 notice: correction 002's disposition
  below (retained unedited, as historical record) grounded APPLICABLE
  in an "architectural precondition" that was, at that time, HONESTLY
  DISCLOSED as implementation-level only — pinned solely in
  `regime_passthrough.py`/`swing_distance.py`'s own class docstrings
  ("One instance per Feature subject"), not yet a Domain-Contract- or
  Constitution-level guarantee, and not yet backed by any dedicated
  runtime authority. That precondition has since been SUPERSEDED, not by
  a documentation change, but by an actual, Review-A-validated
  implementation: **ADR-043** (Approved) — the per-`feature_subject_id`
  authoritative ownership architecture — is now implemented
  (`src/feature_engine/ownership.py`: `AuthoritativeSubjectOwner`,
  `SubjectOwnershipAuthority`, `FencedFeatureCommitter`,
  `AuthoritativeLineageHistoryProvider`, `p_run_sort`), and its
  implementation Review A closed CLEAN — 0 Blocker / 0 Major / 0 Minor
  (`ADR043-IMPL-A-MAJ-01..07` all `CLOSED — REVIEW A VALIDATED`,
  boundary `81605fd1ca099eae48b937ced3c775e271dee2e2`; full record in
  `python/feature-engine/README.md`). The current, authoritative basis
  for `-MAJ-05`'s APPLICABLE disposition and its satisfying evidence is
  therefore the STACK, not the docstring alone: (1) Chapter 8 §8.3
  single-writer/atomic-sequence stream-level ordering (unchanged,
  necessary but not sufficient, as correction 002 already correctly
  established); (2) `feature.md` §9 rule 6 (no fork) as the
  Domain-Contract-owned domain-level semantic (unchanged, still the
  actual authority for the rule itself); (3) **ADR-043's runtime**
  as the concrete, Review-A-validated MECHANISM that makes rule 6
  enforceable per-subject across ownership handoffs — not merely within
  one long-lived in-process engine instance — via
  `SubjectOwnershipAuthority.acquire`/`revoke` fencing,
  `FencedFeatureCommitter` generation-checked commits
  (`StaleOwnershipGenerationError` on a stale/fenced attempt), and
  canonical-history catch-up (`AuthoritativeLineageHistoryProvider`) that
  reconstructs a fresh owner's lineage before it may act; (4) the
  formal I-13 property evidence itself (§12 below,
  `tests/test_i13_properties.py`), which exercises the actual
  implementation boundary directly — not a re-statement of the rule,
  direct generated evidence that it holds. `SubjectOwnershipAuthority`,
  `FencedFeatureCommitter`, and `AuthoritativeLineageHistoryProvider`
  remain test-doubled in this evidence (in-memory; §12 documents this
  explicitly) — no concrete production-durable distributed-storage
  fencing/history adapter is implemented or claimed by this correction;
  that remains explicitly out of scope, same discipline as every prior
  transaction in this chain. The Chapter 8 §8.3 stream-level guarantee
  remains relevant but, as correction 002 already established, is not
  by itself sufficient — it is the ADR-043 runtime, now implemented and
  validated, that supplies the missing per-subject coordination/fencing
  contract; `feature.md`'s no-fork rule remains the domain semantic
  authority throughout, unedited, uninvented.

Concurrent/competing transitions — `-MAJ-05` corrected disposition
  (correction 002, retained unedited as historical record — superseded
  by the notice above, not by editing the text below):
  **B. APPLICABLE**, satisfied by the SAME evidence category already
  scoped above as "Illegal-transition rejection" (specifically its
  `fork` case) — NOT a separate concurrency-testing mechanism, and NOT
  literal threaded/concurrent execution. This replaces v0.1/correction
  001's `NOT_APPLICABLE` disposition, which is retracted: that disposition
  inferred "single writer authority → competing transitions structurally
  impossible" from Chapter 8 §8.3 alone. On fresh re-read, §8.3
  establishes STREAM-level guarantees only — exactly one writer authority
  per stream, atomic sequence assignment, no dual-authoritative window
  (docs/constitution/08-event-model.md v4.8, Locked, lines 222/299/
  348-363, re-verified this transaction). That guarantees ORDERING and
  APPEND-MECHANICS integrity (no gaps, no duplicate sequence numbers, no
  two writers). It says nothing about, and does not by itself validate,
  a payload's DOMAIN-LEVEL cross-reference (`supersedes_fact_ref`
  targeting the true current lineage head) — Event Contract governs
  event-to-stream eligibility and payload schema (§8.3.1), not cross-fact
  referential integrity across a lineage, and neither authority checks
  whether a given `FeatureComputed.supersedes_fact_ref` is genuinely the
  CURRENT head at append time. Chapter 8 alone therefore does not prove
  I-13's requirement; the prior inference conflated "the log can't be
  corrupted by two writers" with "two conflicting successor candidates
  can never be independently constructed for the same head," which is a
  distinct, domain-level claim Chapter 8 does not make.

  Re-derived, this transaction, from EXISTING Feature-specific authority
  (no new contract invented):

  1. `feature.md` §9 rule 6 (already cited in §2 above, Surface 1) is
     ITSELF the Domain-Contract-owned version/concurrency semantic I-13's
     guarantee #1 requires ("Mỗi entity type phải có state machine
     authoritative... được sở hữu bởi Domain Contract"): "fact CHƯA từng
     là supersedes_fact_ref của bất kỳ FeatureComputed nào khác" — a
     replacement may target a given head EXACTLY ONCE; a second attempt
     to supersede the SAME head is, by this rule's own text, a fork and
     is prohibited. This is precisely I-13's own required guarantee #4
     restated in domain terms: "không được tạo ra hai transition xung
     đột từ cùng một authoritative state/version."
  2. The rule is not merely declaratory — it is actively ENFORCED, before
     emission, by the real implementation (verified via direct source
     read, this transaction, not from memory):
       `src/feature_engine/regime_passthrough.py` — both class-level
       docstrings state, verbatim: **"One instance per Feature
       subject."** `RegimePassthroughFeatureEngine.on_regime_classified`
       validates an incoming upstream fact against this engine's own
       authoritative in-memory `self._lineage[key]` state and raises the
       real `FeatureLineageError` — "received a new RegimeClassified for
       window ... whose current lineage head is not pending correction —
       a replacement must be preceded by RegimeFactInvalidated" — BEFORE
       any `FeatureComputed`/`FeatureFactInvalidated` is constructed or
       returned (i.e. before append), not after the fact.
       `src/feature_engine/swing_distance.py` — identical docstring
       guarantee ("One instance per Feature subject"). Its
       `on_swing_invalidated` validates an incoming upstream fact against
       `self._latest_confirmation(...)`/`self._swing_invalidations` and
       raises `InvalidSwingEligibilityInputError` — "which is not the
       current non-invalidated revision tracked by this engine" — again
       BEFORE any state mutation or emission (the method's own docstring:
       "a rejected frontier leaves the targeted revision's non-invalidated
       state untouched"). Its own `_emit_replacement_only`/
       `_invalidate_and_replace` construct `supersedes_fact_ref=existing.
       head_fact.ref` directly from this SAME authoritative internal
       state — never from an externally-asserted value — so a forked
       successor cannot be constructed by this engine even in principle.
  3. Combined, these establish the actual Feature-specific "version/
     concurrency contract": exactly ONE authoritative computation
     instance exists per Feature subject (an architectural guarantee
     currently pinned in the implementation's own class docstrings, not
     yet restated in `feature.md` itself — noted honestly, not hidden;
     see the scope note below), and that instance validates every
     externally-asserted transition against its own authoritative,
     sequentially-updated internal lineage state, failing closed BEFORE
     emission whenever the asserted predecessor is not genuinely the
     current head. This is exactly the shape of "resolve deterministically
     by comparing against the authoritative current head/version, reject
     the loser" that I-13 and the task's own example both describe — it
     is a real, enforced, pre-append mechanism, not a downstream
     projection catching an already-appended defect (§6's own "Do not
     assume a projection rejecting an already-appended invalid event is
     sufficient" instruction is honored: `FeatureCurrentView`'s
     `FeatureLineageError` raises, cited under Surface 1 above, are a
     SEPARATE, additional check on the read side; the ENGINE-level checks
     identified here are the primary, pre-append enforcement point).

  Required evidence (this is the concrete competing-transition property,
  conceptually per the task's own formulation): generate two candidate
  successor facts that both target the SAME current lineage head (i.e.
  both would set `supersedes_fact_ref` to the identical `head_fact.ref`)
  — for `RegimePassthroughFeatureEngine`, this means delivering a second
  `RegimeClassifiedFact` for a window whose lineage head is not (or is no
  longer) pending correction; apply the first legally, then attempt the
  second against the SAME pre-attempt head. Assert DETERMINISTICALLY:
  the first attempt is accepted and becomes the new authoritative current
  head; the second attempt — now stale relative to the (already-advanced)
  head — is rejected via the real `FeatureLineageError` (fail-closed), and
  the lineage never contains two facts both claiming the same
  `supersedes_fact_ref`. This is a DETERMINISTIC, SEQUENTIALLY-GENERATED
  scenario (apply attempt 1, then attempt 2, against a shared starting
  head) — not literal multi-threaded execution, consistent with the task's
  own guidance ("Do NOT invent threaded testing merely because the word
  'concurrent' appears... If the contract resolves concurrency by
  serialization/current-head comparison, generated conflicting/
  interleaved histories may be the correct verification mechanism").

  Explicitly distinguished from interleaving (a DIFFERENT test category,
  per the task's own instruction — they are not the same): "Sequence/order
  constraints" above covers ARRIVAL ORDER of facts that do NOT conflict
  with each other (e.g. candle vs. swing-confirmation delivery order,
  regime facts across independent windows) — shuffling their arrival order
  must not change the final legal result. The competing-transition property
  here covers two candidates that DO conflict (both claim the same
  predecessor) — the correct, required outcome is NOT "both apply in some
  order" but "exactly one is ever accepted, the other fails closed." A
  property/test conflating these two categories would be incorrect.

  Honest scope note (not a contract invention, a disclosure): "One
  instance per Feature subject" is currently established only in the
  implementation's own class docstrings (`regime_passthrough.py`,
  `swing_distance.py`), not restated as an explicit guarantee in
  `feature.md` itself. This is sufficient authority for THIS candidate's
  own purpose — I-13 requires evidence against "state machine
  authoritative... sở hữu bởi Domain Contract," and `feature.md` §9 rule 6
  IS that Domain-Contract-owned semantic (point 1, above); the
  single-instance architecture is the (currently implementation-level,
  not yet Domain-Contract-pinned) MECHANISM that makes rule 6 actually
  enforceable, exactly as I-13's own "Constitution không tự áp đặt...
  đó là quyết định của từng Domain Contract" principle allows enforcement
  detail to live in implementation. This is NOT the FAIL-CLOSED/STOP
  condition the task describes (that would apply if NO existing authority
  defined the semantic rule at all) — the semantic rule already exists
  and is already enforced; only its ARCHITECTURAL PRECONDITION
  (single-instance-per-subject) is presently undocumented at the Domain
  Contract level. No edit to `feature.md` is made or proposed by this
  QG-scoped correction — documenting that precondition in `feature.md`,
  if ever warranted, is a separate, future Domain Contract decision, out
  of scope here.
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

> **Bounded correction 003 notice:** the "Not performed" list below is
> historical — it was true of the transaction that authored §9
> (candidate v0.1/boundary `310a83e22c868611028e5804c524fb5a4e9f57da`)
> and is left textually unedited as the record of what THAT transaction
> did and did not do. It is now **superseded** for the repository's
> CURRENT state: as of this bounded correction 003 (Commit
> `27bd472efeab9a9538bde62ccfeca5c0a1ce48c9`), `hypothesis==6.168.0`/
> `sortedcontainers==2.4.0` ARE installed and pinned
> (`pyproject.toml`/`requirements-dev.lock.txt`), `docs/engineering/
> testing.md` HAS been edited (mechanical v0.17 approval-lifecycle
> recording only — see `testing.md`'s own approval banner),
> `python/feature-engine/tests/test_i13_properties.py` HAS been
> authored, and `P3-FEATURE-QG-EVID-07` now carries the disposition
> `EVIDENCE PRODUCED — PENDING REVIEW A VALIDATION` (still not `CLOSED`,
> still not `FINAL PASS`) — full record in §12 below. The
> `P3-FEATURE-QG-EVID-05(a)`/`-05(b)` and mutmut/coverage.py/gobco
> non-interference claims below remain accurate and unchanged by this
> correction (verified fresh this transaction: `git diff --quiet --
> docs/governance/quality-gate/feature-engine-evid05*` and equivalent
> for mutmut/coverage candidate files — none touched).

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
No self-closure of `P3-FEATURE-QG-EVID07-A-MAJ-04`/`-MAJ-05` — both
  recorded `REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW` (frontmatter,
  banner), never `CLOSED`, per `-MAJ-02`'s own corrected governance path
  (Review A determines disposition on re-review; this Executor
  transaction does not). `-MAJ-01`/`-MAJ-02`/`-MAJ-03` are recorded
  `CLOSED — REVIEW A VALIDATED` per the incoming, mechanically-recorded
  Review A re-review disposition (frontmatter `bounded_correction_002`,
  banner) — not re-derived or re-litigated by this transaction, and not
  reopened absent a fresh direct contradiction (none found).
No edit to `docs/engineering/testing.md` — verified byte-unchanged, blob
  `708744f0464720cb14ceafbe75bb422200a57820` (`git diff --quiet --
  docs/engineering/testing.md`), same as before this transaction. The
  `-MAJ-05` correction is grounded in `feature.md` §9 rule 6 (already
  cited, unedited) and the existing Feature Engine implementation
  (unedited) — no new contract text was required or added anywhere.
```

## 10. Self-consistency check (performed before commit)

```text
- §2's cited source identifiers, and the additional identifiers this
  correction newly cites (`RegimePassthroughFeatureEngine`/
  `SwingDistanceFeatureEngine`'s "One instance per Feature subject"
  docstrings; `InvalidSwingEligibilityInputError`; the `on_swing_
  invalidated`/`on_regime_classified` pre-emission validation logic) were
  verified via direct source read against current
  src/feature_engine/{regime_passthrough,swing_distance}.py this
  transaction, not recalled from memory.
- `-MAJ-04`: the entire QG candidate file was searched for every
  occurrence of `seed`, `@seed`, `reproduction seed`, `reusable seed`,
  `reproduce_failure`, `print_blob`, `derandomize` (this transaction) —
  the one surviving contradictory sentence (§3 Alternative B) was found
  and corrected to match §5's own accurate contract; every other
  occurrence was re-read and confirmed already consistent (Alternative
  A's stdlib-seeding discussion is unrelated to hypothesis's own API and
  was left unchanged; §5/§7's content, corrected in bounded correction
  001, is unchanged and remains accurate).
- `-MAJ-05`: the corrected disposition does not repeat "single writer
  authority → competing transitions structurally impossible." It is
  grounded in `feature.md` §9 rule 6 (Domain-Contract-owned semantic,
  already cited in §2, unedited by this correction) plus direct,
  this-transaction verification that the real implementation enforces it
  BEFORE emission (`FeatureLineageError` in `regime_passthrough.py`,
  `InvalidSwingEligibilityInputError` in `swing_distance.py`, both
  checked prior to any state mutation per their own docstrings/code) —
  not a downstream-projection-only claim, and not a grep-only claim.
  Interleaving and competing-transition semantics are kept explicitly
  distinct (§6, two separate paragraphs with an explicit "explicitly
  distinguished" cross-reference).
- No contract was invented: `feature.md` was read, not edited; the
  "one instance per Feature subject" precondition is disclosed as
  implementation-level, not claimed as a Domain-Contract-level guarantee
  — an honest scope note, not a fabricated authority.
- `docs/engineering/testing.md` verified byte-unchanged this transaction
  (`git diff --quiet`), blob `708744f0464720cb14ceafbe75bb422200a57820` —
  no scope-expansion into the canonical tool decision was needed to
  remediate `-MAJ-04`/`-MAJ-05`.
- No numeric Chapter 13 threshold is duplicated into this candidate.
- Internally coherent: no section of this candidate asserts EVID-07 is
  closed, asserts a dependency was installed, asserts a Product Owner
  decision occurred, or asserts Review A itself approves anything.
```

## 11. Next governed step (not performed by this transaction) — `-MAJ-02`/`-MAJ-03` corrected governance path

> **Bounded correction 003 notice:** steps 1–6 below (the list was
> authored at correction 002's boundary) have since occurred, largely as
> already-completed governance input to this integrated transaction (not
> re-run here — recorded verbatim in the banner at the top of this
> file) plus this transaction's own execution work: step 1 (Review A
> re-review of correction 002) occurred — `-MAJ-04` closed, `-MAJ-05`
> found to need further remediation (this correction). Step 3
> (Risk Classification, R1) and step 4 (Product Owner decision,
> `2026-09-14`, verbatim in the banner above) occurred on the
> testing.md v0.17 candidate. Step 5 (install/pin) and step 6
> (test-authoring) were executed in this SAME transaction (Commit
> `27bd472efeab9a9538bde62ccfeca5c0a1ce48c9`), per the task's own
> integrated-transaction shape. Step 7 (formal evidence) is THIS
> correction 003 itself — §12 below — and, per its own instruction,
> does **not** self-close `P3-FEATURE-QG-EVID-07`. The list below is
> left textually unedited as the historical record of correction 002's
> own view of the remaining path; the ACTUAL next governed step, as of
> this transaction, is: **bounded Review A of EVID-07 correction 003 +
> formal evidence at Commit `27bd472efeab9a9538bde62ccfeca5c0a1ce48c9`**
> — scoped to (a) the corrected `-MAJ-05` rationale (§6 notice), (b) the
> formal evidence record's own validity and completeness (§12), and (c)
> whether `P3-FEATURE-QG-EVID-07` should close. Not performed by this
> transaction.

```text
1. Bounded Review A re-review of THIS correction (correction 002),
   scoped to `-MAJ-04`/`-MAJ-05` ONLY (`-MAJ-01`/`-MAJ-02`/`-MAJ-03`
   already CLOSED — REVIEW A VALIDATED, not reopened, not re-reviewed):
   determines whether the two are genuinely remediated (CLOSED) or
   require further correction. Review A determines technical
   disposition/eligibility only — it does not approve this candidate or
   the testing.md v0.17 candidate subsection, per Chapter 0 §3. Per the
   task's own instruction, R2 (the incoming classification) does not
   automatically require a second review/cross-check — only the Product
   Owner may choose one, and none is requested or performed here.
2. If Review A finds the corrections insufficient: a further bounded
   correction transaction remediates the residual — not self-closed by
   the correction author, same discipline as this transaction.
3. Once Review A closes both remaining findings CLEAN: Risk
   Classification (R0/R1/R2, per ADR-042) is recorded for the testing.md
   candidate decision specifically (the actual mechanism/tool decision,
   per `-MAJ-03` — not for this QG-scoped file, which makes no decision
   of its own to classify).
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
   property-based tests against Surfaces 1–2 (§2/§6), including the
   competing-transition property now defined under `-MAJ-05`'s
   corrected disposition.
7. A SEPARATE, later, formal Chapter 13 §13.9 evidence transaction (same
   pattern as feature-engine-evid05b-formal-evidence-001.md) records
   fresh measurement and, only if it genuinely passes, closes
   `P3-FEATURE-QG-EVID-07`.
   None of steps 1-7 is performed by this transaction.
```

## 12. Formal evidence record (stabilization 001, this transaction — WHOLESALE REPLACEMENT of the superseded correction-003 evidence below)

> The formal evidence record previously recorded here (tested boundary `27bd472efeab9a9538bde62ccfeca5c0a1ce48c9`) is **superseded** — Review A found it `REVISION_REQUIRED` (`-MAJ-06`/`-07`/`-08`/`-MIN-01`, root causes at §13). This section is replaced wholesale with the corrected evidence obtained against **Commit A2**, not appended alongside the stale result.

```text
Tested boundary (exact, pushed, verified `main == origin/main` before AND
  after this run): e901f1857b1049ebc0bb4bdfd7a047e40e1174ed ("Commit A2",
  parent: 86470d105f0608f0708be7c694a6f331486edf09 — the correction-003
  docs-only boundary). Superseded prior evidence boundary (historical,
  no longer qualifying): 27bd472efeab9a9538bde62ccfeca5c0a1ce48c9.
Commit A2 contents (exactly): docs/engineering/testing.md,
  python/feature-engine/README.md (tiny wording correction only, same
  approval-date reference), python/feature-engine/tests/
  test_i13_properties.py. No production `src/feature_engine/**` file
  touched, no dependency-version file touched (verified `git diff
  --stat 86470d1.. e901f185 -- python/feature-engine/src
  python/feature-engine/pyproject.toml
  python/feature-engine/requirements-dev.lock.txt` empty).

Package identity and provenance (`-MAJ-08` corrected — re-downloaded
  fresh this transaction into a NEW scratch directory OUTSIDE the
  repository, not copied from the superseded record above; captured
  DIRECTLY from the downloaded filename, not manually transcribed):
  hypothesis, version 6.168.0, for this exact Python 3.13/macOS ARM64
    qualifying environment: `pip download --no-deps --no-cache-dir`
    selected exactly ONE coherent artifact —
    `hypothesis-6.168.0-cp313-cp313-macosx_11_0_arm64.whl`, size 784558
    bytes, SHA-256 `92cff497b92e2285ff6a94193fdee04aba483a4115d501c1f9a
    570bd103fcd20` — verified byte-identical against PyPI's own JSON API
    declared digest for this exact filename
    (`https://pypi.org/pypi/hypothesis/6.168.0/json`). `-MAJ-08`'s root
    cause (§13 RC-3): the prior evidence record's own §3/§5 prose
    additionally described this artifact once as
    `hypothesis-6.168.0-py3-none-any.whl` — a UNIVERSAL-wheel filename
    that does not exist for this package/version at all (PyPI's file
    index for `hypothesis==6.168.0` lists ONLY CPython-version- and
    platform-tagged wheels, e.g. `cp313-cp313-macosx_11_0_arm64`,
    `cp313-cp313-manylinux_2_17_x86_64`, etc. — Hypothesis is NOT
    distributed as a universal `py3-none-any` wheel; verified directly
    against the live PyPI file listing, this transaction). The record
    now names exactly ONE artifact identity, consistently, everywhere:
    `hypothesis-6.168.0-cp313-cp313-macosx_11_0_arm64.whl` / 784558
    bytes / SHA-256 `92cff497...03fcd20`.
  sortedcontainers, version 2.4.0: `sortedcontainers-2.4.0-py2.py3-
    none-any.whl` (this one genuinely IS a universal wheel — pure-Python,
    consistent with its own PyPI file listing), size 29575 bytes,
    SHA-256 `a163dcaede0f1c021485e957a39245190e74249897e2ae4b2aa38595db
    237ee0` — verified byte-identical against PyPI's own JSON API
    declared digest.
  Development Status :: 5 - Production/Stable; License-Expression:
    MPL-2.0; Requires-Python: >=3.10; Requires-Dist (unconditional at
    Python >=3.11): sortedcontainers>=2.1.0,<3.0.0 — all re-confirmed
    unchanged from the wheel METADATA of the newly-downloaded artifact
    this transaction.
  Package versions unchanged (`hypothesis==6.168.0`,
    `sortedcontainers==2.4.0` remain exactly the approved v0.17
    candidate's own versions — no STOP condition was triggered; the
    version identity was never in question, only the recorded artifact
    FILENAME/hash-pairing prose).
  Required API surface re-confirmed importable at 6.168.0: `hypothesis.
    given`, `hypothesis.example`, `hypothesis.settings`, `hypothesis.
    reproduce_failure`, `hypothesis.stateful.RuleBasedStateMachine`,
    `hypothesis.stateful.rule`, `hypothesis.stateful.invariant`,
    `hypothesis.stateful.precondition`.

Interpreter / tool identities (this transaction, exact venv used for the
  qualifying run — python/feature-engine/.venv, matching the committed
  lock discipline, unchanged from the superseded record):
  Python 3.13.6
  pytest 9.1.1
  hypothesis 6.168.0
  sortedcontainers 2.4.0
  Clean-environment re-verification (SEPARATE, fresh venv strictly
    outside the repository, built from `pip install -r
    requirements-dev.lock.txt` + `pip install -e .` reading the
    COMMITTED lock file): `pip check` -> "No broken requirements found."
  Production dependency surface confirmed unchanged: `[project]
    dependencies = []` in pyproject.toml.

Hypothesis execution profiles (`-MIN-01` corrected —
  tests/test_i13_properties.py, module level):
  "ci": derandomize=True, print_blob=True, database=None,
    max_examples=200, suppress_health_check=[HealthCheck.too_slow] —
    UNCHANGED, exactly the approved formal-evidence semantics.
  "dev": `settings.register_profile("dev")` with NO `max_examples`
    override (corrected — previously `max_examples=25`, a locally-tuned
    value that diverged from the approved mechanism's own "library
    default" semantics, §13 RC-4) — now uses Hypothesis's own unmodified
    library default. Verified PROGRAMMATICALLY, not merely by omission:
    `test_dev_profile_uses_hypothesis_library_default_max_examples`
    asserts `settings.get_profile("dev").max_examples ==
    settings.get_profile("default").max_examples` — this test itself
    passed in both formal runs below.
  Loaded via `settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE",
    "dev"))` — formal evidence commands below explicitly set
    `HYPOTHESIS_PROFILE=ci`, never relying on environment
    auto-detection. No change to formal "ci" evidence semantics from
    this correction.
  `TestRegimeLegalTransitionMachine.settings` overrides
    `stateful_step_count=12` on top of the loaded "ci" profile's other
    values — unchanged.

Formal property evidence command (executed TWICE against exact Commit
  A2, per instruction — no retry-until-green, both runs required to
  pass independently):
  `HYPOTHESIS_PROFILE=ci pytest -q tests/test_i13_properties.py
  --hypothesis-show-statistics`
  Run 1 result: 20 passed in 1.98s.
  Run 2 result: 20 passed in 2.15s.
  (20, not 18: `-MAJ-07`'s correction replaced one mismodeled property
  with two correctly-distinguished properties, net +1, and `-MIN-01`'s
  correction added one dedicated verification test, net +1 — 18 - 1 + 2
  + 1 = 20.)
  Both runs produced statistically identical Hypothesis statistics per
    test (identical pass/generate/invalid counts per test; the only
    textual difference between the two runs' raw output was non-semantic
    generate-phase timing noise and Python object memory-address/hash
    noise in printed debug repr strings — confirmed via `diff` after
    filtering those lines; zero difference in any pass/fail/invalid
    count). No `Flaky` result occurred on either run
    (`grep -i flaky` on both raw outputs: no match). Per-test statistics
    (both runs identical on pass/fail/invalid counts):
    TestRegimeLegalTransitionMachine: 200 passing, 0 failing, 237
      invalid (Hypothesis's own `RuleStrategy` filter-retry accounting
      for the bounded, narrowing precondition set as
      `generation_count` advances — not a failure).
    test_second_original_against_non_invalidated_lineage_fails_closed,
      test_double_invalidation_fails_closed,
      test_stale_nonexistent_lineage_successor_invalidation_fails_closed,
      test_fork_attempt_second_successor_of_same_prior_head_fails_closed,
      test_foreign_scope_fails_closed,
      test_p_run_sort_tie_break_matches_stream_id_then_sequence_for_
      unrelated_events,
      test_adr043_successor_generation_fences_stale_predecessor_and_
      sees_canonical_state,
      test_adr043_different_subjects_remain_fully_independent: each 200
      passing, 0 failing, 0 invalid.
    test_swing_revision_skip_fails_closed: 21 passing, 0 failing, 21
      invalid (`assume(swing_definition_version == "swd-1")` filters the
      other sampled value — expected, not a failure).
    test_p_run_sort_permutation_invariant_preserves_hard_constraints:
      200 passing, 0 failing, 22 invalid.
    test_p_run_sort_identical_duplicate_ref_dedups_deterministically,
      test_p_run_sort_conflicting_duplicate_ref_fails_closed_both_orders:
      each 100 passing, 0 failing, 0 invalid.
    test_p_run_sort_cycle_fails_closed: 3 passing, 0 failing, 0 invalid
      (bounded `st.integers(min_value=2, max_value=4)` domain).
    test_p_run_sort_never_waits_for_a_future_unrelated_event (`-MAJ-07`
      corrected Case 2): 200 passing, 0 failing, 20 invalid.
    test_p_run_sort_never_waits_for_an_already_applied_out_of_set_cause
      (`-MAJ-07` corrected distinct counterpart, not Hypothesis-decorated
      — exercises a real `AuthoritativeSubjectOwner` commit): 1/1
      passed, deterministic.
    test_adr043_two_racing_successor_acquisitions_only_the_later_one_wins:
      1 passing (fixed `st.just(None)` case, by construction), 0
      failing.
    test_regime_catch_up_reconstruction_matches_reference_history
      (`-MAJ-06` corrected live-vs-replay oracle): 200 passing, 0
      failing, 31 invalid.
    test_swing_catch_up_reconstructs_non_selected_swing_evidence: 16
      passing (bounded by `assume(swing_a_pivot != swing_b_pivot)` over
      a small integer domain), 0 failing.
    test_dev_profile_uses_hypothesis_library_default_max_examples
      (`-MIN-01` corrected, not Hypothesis-decorated): 1/1 passed,
      deterministic.
  No property test discovered a production defect. No production
    source file was modified in this transaction. No weakening of any
    assertion was performed to make a property pass. `.hypothesis/` was
    never committed (auto-`.gitignore`d by Hypothesis; confirmed via
    `git status --porcelain=v1 --ignored=matching -- .hypothesis`
    showing `!!` markers both before and after this run).

Full regression command and result (exact Commit A2, "ci" profile):
  `HYPOTHESIS_PROFILE=ci pytest -q` -> 388 passed in 2.45s (368
  pre-existing tests, unchanged, + 20 I-13 property/verification tests
  — zero regressions in any pre-existing test).

Static analysis commands and results (exact Commit A2):
  `ruff check src tests` -> 2 findings, BOTH pre-existing and unrelated
    (E501 line-too-long, `src/feature_engine/authority_resolver.py:465`
    and `:528` — unchanged from every prior transaction in this chain;
    NOT introduced, NOT fixed, by this transaction). Ruff is therefore
    NOT claimed "clean" — it is claimed "2 pre-existing, unrelated
    findings, unchanged."
  `mypy src tests` -> "Success: no issues found in 34 source files."

Evidence-category mapping — the 5 required I-13 evidence categories
  (Constitution 02-platform-invariants.md I-13 Verification clause),
  mapped to exact committed test identifiers in
  `python/feature-engine/tests/test_i13_properties.py` at Commit A2
  `e901f1857b1049ebc0bb4bdfd7a047e40e1174ed` (sufficient for an
  independent reviewer to re-run each by name, e.g.
  `HYPOTHESIS_PROFILE=ci pytest -q tests/test_i13_properties.py::<name>
  --hypothesis-show-statistics`):

  1. Property-based test on the authoritative transition graph:
     - `TestRegimeLegalTransitionMachine` (built on
       `RegimeLegalTransitionMachine(RuleBasedStateMachine)`, rules
       `submit_original`/`invalidate_current`/`submit_replacement`,
       `stateful_step_count=12`) — generates sequences of legal
       Surface-1/Surface-2 transitions against the REAL
       `RegimePassthroughFeatureEngine` and `FeatureCurrentView`,
       asserting lineage-head correctness, `view.current()`
       VALID/PENDING_CORRECTION correctness, `supersedes_fact_ref`
       chain integrity, and strictly increasing `recorded_time` after
       every step.
     - `test_p_run_sort_permutation_invariant_preserves_hard_constraints`,
       `test_p_run_sort_tie_break_matches_stream_id_then_sequence_for_
       unrelated_events`, `test_p_run_sort_identical_duplicate_ref_
       dedups_deterministically`,
       `test_p_run_sort_conflicting_duplicate_ref_fails_closed_both_
       orders`, `test_p_run_sort_cycle_fails_closed`,
       `test_p_run_sort_never_waits_for_a_future_unrelated_event`
       (`-MAJ-07` corrected Case 2),
       `test_p_run_sort_never_waits_for_an_already_applied_out_of_set_
       cause` (`-MAJ-07` corrected distinct counterpart) —
       generated-order-independence evidence for the real `p_run_sort`
       (Chapter 8 §8.3.4 P_stream ∪ P_causation) underlying the same
       transition graph's application order.

  2. Illegal-transition rejection:
     `test_second_original_against_non_invalidated_lineage_fails_closed`,
     `test_double_invalidation_fails_closed`,
     `test_stale_nonexistent_lineage_successor_invalidation_fails_closed`,
     `test_fork_attempt_second_successor_of_same_prior_head_fails_closed`,
     `test_swing_revision_skip_fails_closed`,
     `test_foreign_scope_fails_closed` — each asserts the SPECIFIC real
     exception type (`FeatureLineageError`,
     `InvalidSwingEligibilityInputError`, `ForeignScopeError`) is raised
     and that engine/lineage state is unchanged after rejection.

  3. Correction / strictly-governed lifecycle:
     `TestRegimeLegalTransitionMachine` (same class as category 1,
     different assertion angle) — bounded, generated
     ORIGINAL -> N x (INVALIDATE -> REPLACEMENT) lifecycles
     (`generation_count < 6` precondition), asserting every lineage
     member's own `computation_cursor`/
     `computation_dependency_content_evidence` is independently pinned
     (never inherited from a prior member) across the full generated
     history, not merely a single fixed correction as the pre-existing
     example-based tests cover.

  4. Competing / concurrent transition behavior:
     `test_adr043_successor_generation_fences_stale_predecessor_and_
     sees_canonical_state`, `test_adr043_two_racing_successor_
     acquisitions_only_the_later_one_wins`,
     `test_adr043_different_subjects_remain_fully_independent` —
     exercise the REAL `AuthoritativeSubjectOwner`/`p_run_sort` against
     test-doubled `SubjectOwnershipAuthority`/`FencedFeatureCommitter`/
     `AuthoritativeLineageHistoryProvider` (external boundaries, no
     production-durable adapter implemented or claimed), asserting a
     stale/fenced generation is rejected via the real
     `StaleOwnershipGenerationError`, exactly one of two racing
     acquisitions wins, and different `feature_subject_id` subjects
     remain fully independent.

  5. Replay / catch-up reconstruction:
     `test_regime_catch_up_reconstruction_matches_reference_history`
     (`-MAJ-06` corrected: a REAL `reference_live_view` `FeatureCurrentView`
     is updated CONTEMPORANEOUSLY with reference generation — immediately
     after every emitted event/batch — and `reference_live_result` is
     captured only once generation completes; the replay side
     (`replay_view`) is a SEPARATE `FeatureCurrentView` rebuilt
     AFTERWARD purely from the persisted `canonical_events` obtained via
     catch-up; the two sides never share a construction path),
     `test_swing_catch_up_reconstructs_non_selected_swing_evidence` —
     for generated reference lineages (bounded original/invalidation/
     replacement chains, including mid-invalidation-pending endings), a
     FRESH engine + fresh owner catching up via
     `AuthoritativeLineageHistoryProvider` and a
     `RaisingRecordedTimeSource` (proving no live clock is consulted)
     reconstructs an IDENTICAL lineage/head/`FeatureCurrentView` state
     to the LIVE reference, with zero new ref allocation
     (`fresh_allocator._sequences == {}`).

Real-vs-test-double boundary discipline (unchanged from §6/README):
  `RegimePassthroughFeatureEngine`, `SwingDistanceFeatureEngine`,
  `FeatureCurrentView`, `AuthoritativeSubjectOwner`, `p_run_sort`, and
  real `PreparedTransition` reconciliation are exercised as REAL
  production code throughout. `SubjectOwnershipAuthority`,
  `FencedFeatureCommitter`, and `AuthoritativeLineageHistoryProvider`
  are test-doubled (in-memory) ONLY — external-boundary interfaces with
  no production-durable distributed adapter implemented in this
  repository. This evidence does NOT claim, and must not be read as
  claiming, that a concrete production distributed fencing/history
  storage adapter exists — it does not, and none is added by this
  transaction.

Overall qualifying-run result: SUCCESS. No STOP condition (HEAD drift,
  package-fact contradiction, install failure, `pip check` failure,
  production defect discovery, `Flaky` result, qualifying-evidence
  failure, necessary-production-change, unpinnable provenance) was
  triggered at any point in this transaction.
```

`P3-FEATURE-QG-EVID-07: EVIDENCE PRODUCED — PENDING REVIEW A VALIDATION` (final disposition recorded by this transaction — not `CLOSED`, not `FINAL PASS`; closure remains Review A's own determination on review of stabilization 001, per Chapter 0 §3).

## 13. Root-cause consolidation (stabilization 001, this transaction)

Review A's `REVISION_REQUIRED` disposition on bounded correction 003 (§ banner above) surfaced a pattern, not four unrelated defects — recorded here so the SAME class of defect is less likely to recur in a future transaction, per instruction ("do not introduce another governance workflow around it" — this is a record, not a new process).

```text
RC-1 — test prose drift from reviewed semantics (caused -MAJ-07).
  Some evidence tests were implemented from abbreviated task prose
  instead of validating the exact reviewed semantic distinction between
  (a) a future, unrelated event (no P_stream/P_causation relationship
  at all) and (b) an already-applied, out-of-set causal predecessor (a
  genuine causation edge to an event that already resolved outside the
  current apply set). `test_p_run_sort_never_waits_for_a_cause_outside_
  the_apply_set` collapsed both into one property that actually only
  modeled (b) while being narrated/labeled as (a) ("hypothetical event
  outside its own certified apply set"). Corrected (§12 category 1):
  split into `test_p_run_sort_never_waits_for_a_future_unrelated_event`
  (models (a) — the comparison identity is never placed in any
  envelope's `causation_refs`) and
  `test_p_run_sort_never_waits_for_an_already_applied_out_of_set_cause`
  (models (b) — "already applied" demonstrated via a real
  `AuthoritativeSubjectOwner` commit, not merely asserted in prose).

RC-2 — oracle construction reused persisted history on both sides
  (caused -MAJ-06).
  `test_regime_catch_up_reconstruction_matches_reference_history`'s
  "reference" side and its replay side were BOTH folded, after the
  fact, from the identical `canonical_events` list — a replay-vs-replay
  comparison, not a live-vs-replay one; it could not actually detect a
  defect where catch-up/replay silently diverges from genuine live
  behavior, because both sides used the same input by construction.
  Corrected (§12 category 5): the reference side is now a REAL
  `FeatureCurrentView` (`reference_live_view`) updated CONTEMPORANEOUSLY
  with reference generation, immediately after each engine emission;
  the replay side (`replay_view`) remains a separate reconstruction from
  persisted `canonical_events`, built afterward. The two sides are now
  structurally independent.

RC-3 — package provenance was manually transcribed from mixed artifact
  identities (caused -MAJ-08).
  The evidence record's own §3/§5 prose named the Hypothesis wheel once
  as `hypothesis-6.168.0-py3-none-any.whl` (a universal-wheel filename)
  while the ACTUAL artifact downloaded/hashed/used throughout was the
  platform-specific `hypothesis-6.168.0-cp313-cp313-macosx_11_0_arm64.
  whl` — an internally contradictory record naming two different files
  for what must be one coherent artifact identity. Root mechanism:
  Hypothesis does not in fact ship a universal wheel for this version at
  all (confirmed against PyPI's live file listing, this transaction) —
  the `py3-none-any` mention was a transcription error, not a real
  alternate artifact. Corrected (§12): the record now names exactly ONE
  Hypothesis artifact — filename, byte size, and SHA-256 all captured
  directly from a freshly re-downloaded file this transaction, not
  copied from prior prose.

RC-4 — non-formal profile tuning escaped the approved mechanism (caused
  -MIN-01).
  `settings.register_profile("dev", max_examples=25)` introduced a
  locally-tuned bound, although the approved Testing Convention v0.17
  semantics (§5 of this file) specify the `dev` profile as ordinary
  local Hypothesis behavior — i.e. the library's own default
  `max_examples`, not a project-chosen number. Corrected (§12): the
  override was removed; `dev` now inherits Hypothesis's own unmodified
  default, verified programmatically (`test_dev_profile_uses_hypothesis_
  library_default_max_examples`), not merely by the absence of a kwarg.

RC-5 — lifecycle date was copied from an incorrect task assumption (R0
  factual bookkeeping only, not a Review A finding).
  The Testing Convention v0.17 Product Owner decision itself, and its
  exact text, were always correct and valid — but the recorded decision
  DATE was transcribed as `2026-09-14` when the actual Product Owner
  decision, in the governing conversation, occurred on `2026-09-15`.
  Corrected in `docs/engineering/testing.md` (Commit A2: frontmatter
  `approved_at`/`last_review`, the approval banner's decision-date line,
  and the mechanical lifecycle-change sentence) and reconciled here/in
  MANIFEST/CHANGELOG (Commit B2). This is R0 bookkeeping, not a
  Review A finding, and does not alter approval authority, decision
  content, Review A's own CLEAN 0/0/0 disposition, or Risk R1.

This consolidation is the correction-chain's response to the
  `REVISION_REQUIRED` disposition — it does not introduce a new ADR, a
  new Review B, a new Product Owner decision, or a standalone Risk
  Classification transaction; per instruction, it is folded entirely
  into this one stabilization transaction.
```
