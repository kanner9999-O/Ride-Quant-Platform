"""`feature_engine.identity.deterministic_id` — module-local opaque subject
identity algorithm (feature.md §19 defers the concrete algorithm to
implementation; this module pins one, duplicated not imported from
structure-engine/raw-regime-engine's own `identity.py`; see the module's own
docstring). No dedicated test file previously existed — `deterministic_id`
was exercised only indirectly via `candle.py`'s `CandleScope.subject_id` and
`contracts.py`'s own call site.
"""

from __future__ import annotations

from feature_engine.identity import deterministic_id


def test_same_parts_produce_the_same_id() -> None:
    assert deterministic_id("a", "b", "c") == deterministic_id("a", "b", "c")


def test_different_single_part_produces_a_different_id() -> None:
    assert deterministic_id("a") != deterministic_id("b")


def test_boundary_shift_between_adjacent_parts_produces_a_different_id() -> None:
    """Wave-5 (Condition-1B): `deterministic_id`'s own docstring claims
    "different parts always produce a different id... (stable,
    collision-resistant)". That collision-resistance is only meaningful if
    the join preserves EXACT part boundaries — a naive separator-free (or
    ambiguously-separated) join would let a suffix of one part "leak" into
    the next part's prefix and produce a genuine collision. No existing
    test (direct or indirect, via `CandleScope.subject_id`'s parametrized
    single-field-difference tests) constructs this specific boundary-shift
    scenario, since changing exactly one field's value while holding the
    rest fixed changes the joined string under ANY separator choice, never
    isolating the separator's own role. This test isolates it directly:
    moving the shared substring "b" from the end of the first part to the
    start of the second part must NOT collide.
    """
    assert deterministic_id("ab", "c") != deterministic_id("a", "bc")


def test_boundary_shift_holds_for_three_part_identities() -> None:
    """Same boundary-shift property, exercised with the multi-part shape
    `CandleScope.subject_id` actually uses (six parts) reduced to a
    minimal three-part case sharing the same collision-resistance
    obligation."""
    assert deterministic_id("a", "bc", "d") != deterministic_id("a", "b", "cd")


def test_join_uses_the_exact_documented_pipe_separator() -> None:
    """Wave-5 (Condition-1B): `deterministic_id`'s own docstring commits to
    a SPECIFIC, stable algorithm ("same parts always produce the same
    id"); this pins the exact SHA-256 digest of the pipe-joined
    (`"|"`-separated) two- and three-part forms, so that a change to the
    separator character(s) itself — which would silently and permanently
    change every multi-part id this module has ever produced, a real,
    high-impact behavioral regression the "same parts -> same id"
    property alone cannot detect — is caught. This is a determinism/
    stability pin on the documented algorithm, not on any implementation
    detail: any change to the join separator is exactly the kind of
    silent algorithm drift this pin exists to catch.
    """
    assert deterministic_id("a", "b") == "0eab8a0a3380abf4c7d1fb0b43b66aafbb64a4b953e4eb2dccca579461912d0c"
    assert deterministic_id("a", "b", "c") == "a52dd81bfd5e4e66d96b9f598382f6cbf8c5c3897654e6ae9055e03620fcf38e"
