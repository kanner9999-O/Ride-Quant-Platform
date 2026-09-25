from __future__ import annotations

import dataclasses
from datetime import timedelta
from decimal import Decimal

import pytest
from conftest import BASE, make_candle, make_feature, make_regime, make_structure, ref

from context_aggregator import (
    ContextAggregatorError,
    DuplicateFactReferenceError,
    FeatureType,
    RegimeDimension,
    StructureFactKind,
    StructureOrientation,
)
from context_aggregator.selection import select_candle, select_feature, select_regime, select_structure

# --- Phase 1 step 1: identity/scope match -----------------------------------


def test_scope_mismatch_rejection_structure() -> None:
    wrong_instrument = make_structure(effective_minute=60, instrument_id="ETH-USD")
    winner = select_structure(
        [wrong_instrument],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=60),
        required_definition_version="struct-v1",
    )
    assert winner is None


# --- Phase 1 step 1: required definition-version pin ------------------------


def test_upstream_definition_mismatch_rejection() -> None:
    wrong_version = make_structure(definition_version="struct-v2")
    winner = select_structure(
        [wrong_version],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=60),
        required_definition_version="struct-v1",
    )
    assert winner is None


# --- Phase 1 step 3: effective-time cutoff (no look-ahead) -------------------


def test_effective_time_look_ahead_rejection() -> None:
    too_late = make_structure(effective_minute=61)
    winner = select_structure(
        [too_late],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=60),
        required_definition_version="struct-v1",
    )
    assert winner is None


def test_effective_time_exactly_at_cutoff_is_inclusive() -> None:
    exactly_at_cutoff = make_structure(effective_minute=60)
    winner = select_structure(
        [exactly_at_cutoff],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=60),
        required_definition_version="struct-v1",
    )
    assert winner is exactly_at_cutoff


# --- Phase 1 step 4 + Phase 2: Structure "Required verdict" (context.md §8) --


def test_structure_required_verdict_invalidated_never_beats_valid_older() -> None:
    """context.md §8's own worked example: Structure A (recorded R10, valid)
    vs Structure B (recorded R20, invalidated at R30) — cursor R40. A MUST
    win even though B has a later recorded_time, because B never survives
    Phase 1 (it is excluded before Phase 2 ever sees it)."""
    a = make_structure("structure-a", effective_minute=10, recorded=10, orientation=StructureOrientation.BULLISH)
    b = make_structure("structure-b", effective_minute=20, recorded=20, orientation=StructureOrientation.BEARISH)
    winner = select_structure(
        [a, b],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=40),
        required_definition_version="struct-v1",
        invalidated_refs=frozenset({b.ref}),
    )
    assert winner is a


def test_structure_recomputed_survives_even_if_invalidation_would_target_it() -> None:
    """StructureRecomputed is never a valid target of StructureFactInvalidated
    (structure.md §5) — this core must not apply the invalidation exclusion
    to it regardless of what invalidated_refs contains."""
    recomputed = make_structure(
        "structure-recomputed-1", effective_minute=10, recorded=10, kind=StructureFactKind.STRUCTURE_RECOMPUTED
    )
    winner = select_structure(
        [recomputed],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=60),
        required_definition_version="struct-v1",
        invalidated_refs=frozenset({recomputed.ref}),
    )
    assert winner is recomputed


def test_structure_phase2_picks_max_recorded_time() -> None:
    older = make_structure("structure-older", effective_minute=10, recorded=10)
    newer = make_structure("structure-newer", effective_minute=20, recorded=20)
    winner = select_structure(
        [older, newer],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=60),
        required_definition_version="struct-v1",
    )
    assert winner is newer


# --- Phase 2: Regime/Feature lineage-head selection --------------------------


def test_regime_lineage_head_never_falls_back_to_superseded_survivor() -> None:
    original = make_regime("regime-original", start=0, end=60, recorded=61)
    replacement = make_regime(
        "regime-replacement", start=0, end=60, recorded=90, supersedes=original.ref, stream_id="stream-regime"
    )
    winner = select_regime(
        [original, replacement],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=90),
        dimension=RegimeDimension.VOLATILITY,
        required_definition_version="regime-vol-v1",
    )
    assert winner is replacement


def test_feature_lineage_head_never_falls_back_to_superseded_survivor() -> None:
    original = make_feature("feature-original", start=0, end=60, recorded=61, value=Decimal("1.0"))
    replacement = make_feature(
        "feature-replacement",
        start=0,
        end=60,
        recorded=90,
        value=Decimal("2.0"),
        supersedes=original.ref,
        stream_id="stream-feature",
    )
    winner = select_feature(
        [original, replacement],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=90),
        feature_type=FeatureType.VOLATILITY_METRIC,
        required_definition_version="feat-vol-v1",
    )
    assert winner is replacement
    assert winner.value == Decimal("2.0")


def test_regime_dimension_discriminant_excludes_wrong_dimension() -> None:
    wrong_dimension = make_regime(
        "regime-wrong-dim", dimension=RegimeDimension.DIRECTIONAL_PERSISTENCE, definition_version="regime-vol-v1"
    )
    winner = select_regime(
        [wrong_dimension],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=90),
        dimension=RegimeDimension.VOLATILITY,
        required_definition_version="regime-vol-v1",
    )
    assert winner is None


def test_feature_type_discriminant_excludes_wrong_type() -> None:
    wrong_type = make_feature("feature-wrong-type", feature_type=FeatureType.DISTANCE_TO_LAST_CONFIRMED_SWING)
    winner = select_feature(
        [wrong_type],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=90),
        feature_type=FeatureType.VOLATILITY_METRIC,
        required_definition_version="feat-vol-v1",
    )
    assert winner is None


# --- Superseded Regime/Feature resurrection prevention (CONTEXT-CORE-A-MAJ-02) --


def test_regime_invalidated_replacement_with_no_further_replacement_yields_none() -> None:
    """Case 1: A original, B supersedes A, B invalidated, no C visible yet.
    A must NEVER be returned merely because B (its only successor) is now
    invalidated — the role resolves missing/pending (context.md §9)."""
    a = make_regime("regime-a", start=0, end=60, recorded=10, stream_id="stream-regime")
    b = make_regime("regime-b", start=0, end=60, recorded=20, supersedes=a.ref, stream_id="stream-regime")
    winner = select_regime(
        [a, b],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=90),
        dimension=RegimeDimension.VOLATILITY,
        required_definition_version="regime-vol-v1",
        invalidated_refs=frozenset({b.ref}),
    )
    assert winner is None


def test_regime_chain_resolves_to_valid_current_head_c() -> None:
    """Case 2: A original, B supersedes A, B invalidated, C supersedes B and
    is eligible/current -> C must win."""
    a = make_regime("regime-a", start=0, end=60, recorded=10, stream_id="stream-regime")
    b = make_regime("regime-b", start=0, end=60, recorded=20, supersedes=a.ref, stream_id="stream-regime")
    c = make_regime("regime-c", start=0, end=60, recorded=30, supersedes=b.ref, stream_id="stream-regime")
    winner = select_regime(
        [a, b, c],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=90),
        dimension=RegimeDimension.VOLATILITY,
        required_definition_version="regime-vol-v1",
        invalidated_refs=frozenset({b.ref}),
    )
    assert winner is c


def test_regime_a_remains_superseded_even_though_b_is_filtered_by_invalidation() -> None:
    """Case 3: even though B is excluded from the eligible/current-valid
    output (invalidated), A must still be recognized as historically
    superseded by B and never resurface — same fixture as Case 1, asserted
    from the lineage-superseded-set angle rather than just the end result."""
    a = make_regime("regime-a", start=0, end=60, recorded=10, stream_id="stream-regime")
    b = make_regime("regime-b", start=0, end=60, recorded=20, supersedes=a.ref, stream_id="stream-regime")
    winner = select_regime(
        [a, b],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=90),
        dimension=RegimeDimension.VOLATILITY,
        required_definition_version="regime-vol-v1",
        invalidated_refs=frozenset({b.ref}),
    )
    assert winner is not a
    assert winner is None


def test_feature_invalidated_replacement_with_no_further_replacement_yields_none() -> None:
    a = make_feature("feature-a", start=0, end=60, recorded=10, value=Decimal("1.0"), stream_id="stream-feature")
    b = make_feature(
        "feature-b",
        start=0,
        end=60,
        recorded=20,
        value=Decimal("2.0"),
        supersedes=a.ref,
        stream_id="stream-feature",
    )
    winner = select_feature(
        [a, b],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=90),
        feature_type=FeatureType.VOLATILITY_METRIC,
        required_definition_version="feat-vol-v1",
        invalidated_refs=frozenset({b.ref}),
    )
    assert winner is None


def test_feature_chain_resolves_to_valid_current_head_c() -> None:
    a = make_feature("feature-a", start=0, end=60, recorded=10, value=Decimal("1.0"), stream_id="stream-feature")
    b = make_feature(
        "feature-b",
        start=0,
        end=60,
        recorded=20,
        value=Decimal("2.0"),
        supersedes=a.ref,
        stream_id="stream-feature",
    )
    c = make_feature(
        "feature-c",
        start=0,
        end=60,
        recorded=30,
        value=Decimal("3.0"),
        supersedes=b.ref,
        stream_id="stream-feature",
    )
    winner = select_feature(
        [a, b, c],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=90),
        feature_type=FeatureType.VOLATILITY_METRIC,
        required_definition_version="feat-vol-v1",
        invalidated_refs=frozenset({b.ref}),
    )
    assert winner is c
    assert winner.value == Decimal("3.0")


def test_feature_a_remains_superseded_even_though_b_is_filtered_by_invalidation() -> None:
    a = make_feature("feature-a", start=0, end=60, recorded=10, value=Decimal("1.0"), stream_id="stream-feature")
    b = make_feature(
        "feature-b",
        start=0,
        end=60,
        recorded=20,
        value=Decimal("2.0"),
        supersedes=a.ref,
        stream_id="stream-feature",
    )
    winner = select_feature(
        [a, b],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=90),
        feature_type=FeatureType.VOLATILITY_METRIC,
        required_definition_version="feat-vol-v1",
        invalidated_refs=frozenset({b.ref}),
    )
    assert winner is not a
    assert winner is None


def test_regime_malformed_lineage_self_supersession_fails_closed() -> None:
    original = make_regime("regime-self", start=0, end=60, recorded=10, stream_id="stream-regime")
    self_superseding = dataclasses.replace(original, supersedes_ref=original.ref)
    with pytest.raises(ContextAggregatorError):
        select_regime(
            [self_superseding],
            instrument_id="BTC-USD",
            venue_id="binance",
            timeframe="1h",
            context_cutoff=BASE + timedelta(minutes=90),
            dimension=RegimeDimension.VOLATILITY,
            required_definition_version="regime-vol-v1",
        )


def test_regime_malformed_lineage_fork_fails_closed() -> None:
    a = make_regime("regime-a", start=0, end=60, recorded=10, stream_id="stream-regime")
    b1 = make_regime("regime-b1", start=0, end=60, recorded=20, supersedes=a.ref, stream_id="stream-regime")
    b2 = make_regime("regime-b2", start=0, end=60, recorded=21, supersedes=a.ref, stream_id="stream-regime")
    with pytest.raises(ContextAggregatorError):
        select_regime(
            [a, b1, b2],
            instrument_id="BTC-USD",
            venue_id="binance",
            timeframe="1h",
            context_cutoff=BASE + timedelta(minutes=90),
            dimension=RegimeDimension.VOLATILITY,
            required_definition_version="regime-vol-v1",
        )


# --- Structure effective-time interval (CONTEXT-CORE-A-MAJ-03) --------------


def test_structure_tie_break_uses_interval_start_when_end_and_recorded_time_tie() -> None:
    """Two Structure facts tied on recorded_time (Phase-2 primary criterion)
    and tied on effective_time.window_end -- the interval START must decide
    (criterion 2, DESC) rather than collapsing both facts to one scalar."""
    later_start = make_structure(
        "structure-later-start", start=30, end=60, recorded=10, stream_id="stream-structure"
    )
    earlier_start = make_structure(
        "structure-earlier-start", start=0, end=60, recorded=10, stream_id="stream-structure"
    )
    winner = select_structure(
        [earlier_start, later_start],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=60),
        required_definition_version="struct-v1",
    )
    assert winner is later_start  # window_start DESC picks the later start


def test_structure_cutoff_checks_window_end_not_start_or_recorded_time() -> None:
    """A Structure fact whose window_start is well before the cutoff but
    whose window_end exceeds it must be rejected (no look-ahead); one whose
    window_start exceeds a hypothetical earlier cutoff but window_end does
    not exceed the real cutoff must be accepted."""
    spans_the_cutoff = make_structure("structure-spans-cutoff", start=0, end=61, recorded=5)
    winner = select_structure(
        [spans_the_cutoff],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=60),
        required_definition_version="struct-v1",
    )
    assert winner is None  # window_end (61) > cutoff (60) -> rejected regardless of window_start/recorded_time

    starts_late_ends_on_time = make_structure(
        "structure-starts-late", start=59, end=60, recorded=5
    )
    winner2 = select_structure(
        [starts_late_ends_on_time],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=60),
        required_definition_version="struct-v1",
    )
    assert winner2 is starts_late_ends_on_time  # window_end (60) <= cutoff (60) -> accepted


def test_structure_no_cross_stream_sequence_comparison_with_distinct_intervals() -> None:
    same_time = 61
    a = make_structure(
        "structure-a", start=10, end=70, recorded=same_time, stream_id="stream-x", sequence=999
    )
    b = make_structure(
        "structure-b", start=10, end=70, recorded=same_time, stream_id="stream-a", sequence=1
    )
    winner = select_structure(
        [a, b],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=70),
        required_definition_version="struct-v1",
    )
    assert winner is b  # "stream-a" < "stream-x" lexically, decides before sequence ever matters


# --- Total-order tie-break: cross-stream sequence is never a global order ---


def test_cross_stream_sequence_never_used_as_global_order() -> None:
    """Fact A is in stream `stream-x` with a HIGH raw sequence; fact B is in
    stream `stream-a` (lexically earlier) with a LOW raw sequence. Both tie
    on every earlier criterion. Naive cross-stream sequence comparison would
    wrongly rank by raw sequence; the correct tie-break instead ranks by
    `stream_id` ASC (criterion 4) before `sequence` is ever considered."""
    same_time = 61
    a = make_structure(
        "structure-a", effective_minute=60, recorded=same_time, stream_id="stream-x", sequence=999
    )
    b = make_structure(
        "structure-b", effective_minute=60, recorded=same_time, stream_id="stream-a", sequence=1
    )
    winner = select_structure(
        [a, b],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=60),
        required_definition_version="struct-v1",
    )
    assert winner is b  # "stream-a" < "stream-x" lexically, decides before sequence ever matters


def test_sequence_only_compared_within_same_stream_identity() -> None:
    same_time = 61
    later_seq = make_structure(
        "structure-later-seq", effective_minute=60, recorded=same_time, stream_id="s", sequence=5
    )
    earlier_seq = make_structure(
        "structure-earlier-seq", effective_minute=60, recorded=same_time, stream_id="s", sequence=2
    )
    winner = select_structure(
        [later_seq, earlier_seq],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=60),
        required_definition_version="struct-v1",
    )
    assert winner is earlier_seq  # same stream identity -> sequence ASC decides


# --- Duplicate/conflicting evidence fails closed -----------------------------


def test_duplicate_conflicting_candidate_fails_closed() -> None:
    a = make_structure("structure-dup", effective_minute=10, orientation=StructureOrientation.BULLISH)
    conflicting = make_structure("structure-dup", effective_minute=20, orientation=StructureOrientation.BEARISH)
    with pytest.raises(DuplicateFactReferenceError):
        select_structure(
            [a, conflicting],
            instrument_id="BTC-USD",
            venue_id="binance",
            timeframe="1h",
            context_cutoff=BASE + timedelta(minutes=60),
            required_definition_version="struct-v1",
        )


def test_duplicate_identical_redelivery_is_harmless() -> None:
    a = make_structure("structure-redelivered", effective_minute=10)
    identical_redelivery = make_structure("structure-redelivered", effective_minute=10)
    winner = select_structure(
        [a, identical_redelivery],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_cutoff=BASE + timedelta(minutes=60),
        required_definition_version="struct-v1",
    )
    assert winner is not None


# --- Candle lineage resolution (Phase 1 step 4) ------------------------------


def test_candle_correction_lineage_only_current_head_survives() -> None:
    original = make_candle("candle-original", start=0, end=60)
    corrected = make_candle("candle-corrected", start=0, end=60, recorded=90, supersedes=original.ref)
    # Caller names the (now-superseded) original ref as the computation point
    # it observed; the core must still resolve to the CURRENT lineage head.
    winner = select_candle(
        [original, corrected],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        target_computation_point_ref=original.ref,
    )
    assert winner is corrected


def test_candle_no_candidates_yields_missing() -> None:
    winner = select_candle(
        [],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        target_computation_point_ref=ref("candle-nonexistent"),
    )
    assert winner is None


# --- Candle computation-point binding (CONTEXT-CORE-A-MAJ-01) ---------------


def test_candle_computation_point_binding_w1_correction_not_hijacked_by_later_w2() -> None:
    """context.md §6/§7.0/§11: each authoritative Candle fact defines exactly
    ONE Context computation point. A later window (W2) visible in the same
    candidate set must NEVER win merely because its effective boundary is
    newer — the caller explicitly names W1's corrected fact as the target."""
    w1_original = make_candle("candle-w1-original", start=0, end=60, recorded=61, stream_id="stream-candle")
    w2 = make_candle("candle-w2", start=60, end=120, recorded=121, stream_id="stream-candle")
    w1_corrected = make_candle(
        "candle-w1-corrected",
        start=0,
        end=60,
        recorded=200,
        supersedes=w1_original.ref,
        stream_id="stream-candle",
    )
    winner = select_candle(
        [w1_original, w2, w1_corrected],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        target_computation_point_ref=w1_corrected.ref,
    )
    assert winner is w1_corrected
    assert winner.effective_window.window_start == w1_original.effective_window.window_start
    assert winner.effective_window.window_end == w1_original.effective_window.window_end


def test_candle_computation_point_binding_normal_w2_computation() -> None:
    """A normal, independent request for W2's own computation point still
    resolves correctly and is unaffected by W1's presence in the same set."""
    w1 = make_candle("candle-w1", start=0, end=60, recorded=61, stream_id="stream-candle")
    w2 = make_candle("candle-w2", start=60, end=120, recorded=121, stream_id="stream-candle")
    winner = select_candle(
        [w1, w2],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        target_computation_point_ref=w2.ref,
    )
    assert winner is w2


def test_candle_computation_point_ref_not_found_fails_closed() -> None:
    w1 = make_candle("candle-w1", start=0, end=60)
    winner = select_candle(
        [w1],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        target_computation_point_ref=ref("candle-never-supplied"),
    )
    assert winner is None
