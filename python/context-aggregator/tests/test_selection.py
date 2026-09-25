from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

import pytest
from conftest import BASE, make_candle, make_feature, make_regime, make_structure

from context_aggregator import (
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
    winner = select_candle(
        [original, corrected],
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
    )
    assert winner is corrected


def test_candle_no_candidates_yields_missing() -> None:
    winner = select_candle([], instrument_id="BTC-USD", venue_id="binance", timeframe="1h")
    assert winner is None
