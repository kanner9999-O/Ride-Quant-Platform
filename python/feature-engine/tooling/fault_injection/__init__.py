"""Feature-Engine-scoped supplemental deterministic fault-injection harness.

Implements the mechanism approved in Testing Convention v0.16 §5c path (ii)
and `docs/governance/mutation-baseline-evidence/feature-engine-mutation-
surface-completeness-design-001.md` §2.1/§2.1a/§2.1b (APPROVED — DESIGN
EFFECTIVE) — supplemental Condition-3 evidence for the 5 high-materiality
methods mutmut 3.7.0 structurally excludes from Feature Engine's mutation
surface (decorated-class limitation, `P3-PY-MUT-A-MAJ-02`).

Scope: FEATURE-ENGINE-ONLY. Never invokes mutmut, never touches `mutants/`
or `.mutmut-cache`, never changes the raw 1531-mutant denominator or any
Condition-1 score. Every fault runs inside its own disposable, isolated
`git worktree` checkout pinned to the exact governed boundary — the
canonical working tree is never entered or written to.
"""

from __future__ import annotations
