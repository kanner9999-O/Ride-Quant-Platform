from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from context_aggregator import (
    CandleFact,
    ContextDefinition,
    ContextSubjectScope,
    DirectionalPersistenceRegimeClass,
    EffectiveWindow,
    EventRecordRef,
    FeatureFact,
    FeatureType,
    RegimeDimension,
    RegimeFact,
    StructureFact,
    StructureFactKind,
    StructureOrientation,
    VolatilityRegimeClass,
)

BASE = datetime(2026, 1, 1, 0, 0, 0)


def ref(
    event_id: str, *, stream_id: str = "stream-a", registry_version: str = "v1.0", sequence: int = 1
) -> EventRecordRef:
    return EventRecordRef(
        stream_id=stream_id, registry_version=registry_version, sequence=sequence, event_id=event_id
    )


def window(start_minute: int, end_minute: int) -> EffectiveWindow:
    return EffectiveWindow(
        window_start=BASE + timedelta(minutes=start_minute),
        window_end=BASE + timedelta(minutes=end_minute),
    )


@pytest.fixture
def scope() -> ContextSubjectScope:
    return ContextSubjectScope(
        instrument_id="BTC-USD",
        venue_id="binance",
        timeframe="1h",
        context_definition_version="ctxdef-v1",
    )


@pytest.fixture
def definition() -> ContextDefinition:
    return ContextDefinition(
        context_definition_id="ctxdef",
        context_definition_version="ctxdef-v1",
        required_structure_definition_version="struct-v1",
        required_volatility_regime_definition_version="regime-vol-v1",
        required_directional_persistence_regime_definition_version="regime-dp-v1",
        required_volatility_metric_feature_definition_version="feat-vol-v1",
        required_directional_persistence_metric_feature_definition_version="feat-dp-v1",
        required_distance_to_last_confirmed_swing_feature_definition_version="feat-dist-v1",
    )


def make_candle(
    event_id: str = "candle-1",
    *,
    start: int = 0,
    end: int = 60,
    recorded: int = 61,
    supersedes: EventRecordRef | None = None,
    instrument_id: str = "BTC-USD",
    venue_id: str = "binance",
    timeframe: str = "1h",
    stream_id: str = "stream-candle",
    sequence: int = 1,
) -> CandleFact:
    return CandleFact(
        ref=ref(event_id, stream_id=stream_id, sequence=sequence),
        recorded_time=BASE + timedelta(minutes=recorded),
        instrument_id=instrument_id,
        venue_id=venue_id,
        timeframe=timeframe,
        effective_window=window(start, end),
        supersedes_ref=supersedes,
    )


def make_structure(
    event_id: str = "structure-1",
    *,
    effective_minute: int = 60,
    recorded: int = 61,
    kind: StructureFactKind = StructureFactKind.BREAK_OF_STRUCTURE_DETECTED,
    orientation: StructureOrientation = StructureOrientation.BULLISH,
    definition_version: str = "struct-v1",
    instrument_id: str = "BTC-USD",
    venue_id: str = "binance",
    timeframe: str = "1h",
    stream_id: str = "stream-structure",
    sequence: int = 1,
) -> StructureFact:
    return StructureFact(
        ref=ref(event_id, stream_id=stream_id, sequence=sequence),
        recorded_time=BASE + timedelta(minutes=recorded),
        instrument_id=instrument_id,
        venue_id=venue_id,
        timeframe=timeframe,
        effective_time=BASE + timedelta(minutes=effective_minute),
        definition_version=definition_version,
        kind=kind,
        orientation=orientation,
    )


def make_regime(
    event_id: str = "regime-1",
    *,
    start: int = 0,
    end: int = 60,
    recorded: int = 61,
    dimension: RegimeDimension = RegimeDimension.VOLATILITY,
    regime_class: VolatilityRegimeClass | DirectionalPersistenceRegimeClass = VolatilityRegimeClass.NORMAL,
    definition_version: str = "regime-vol-v1",
    supersedes: EventRecordRef | None = None,
    instrument_id: str = "BTC-USD",
    venue_id: str = "binance",
    timeframe: str = "1h",
    stream_id: str = "stream-regime",
    sequence: int = 1,
) -> RegimeFact:
    return RegimeFact(
        ref=ref(event_id, stream_id=stream_id, sequence=sequence),
        recorded_time=BASE + timedelta(minutes=recorded),
        instrument_id=instrument_id,
        venue_id=venue_id,
        timeframe=timeframe,
        analysis_window=window(start, end),
        definition_version=definition_version,
        regime_dimension=dimension,
        regime_class=regime_class,
        supersedes_ref=supersedes,
    )


def make_feature(
    event_id: str = "feature-1",
    *,
    start: int = 0,
    end: int = 60,
    recorded: int = 61,
    feature_type: FeatureType = FeatureType.VOLATILITY_METRIC,
    value: Decimal = Decimal("1.5"),
    definition_version: str = "feat-vol-v1",
    supersedes: EventRecordRef | None = None,
    instrument_id: str = "BTC-USD",
    venue_id: str = "binance",
    timeframe: str = "1h",
    stream_id: str = "stream-feature",
    sequence: int = 1,
) -> FeatureFact:
    return FeatureFact(
        ref=ref(event_id, stream_id=stream_id, sequence=sequence),
        recorded_time=BASE + timedelta(minutes=recorded),
        instrument_id=instrument_id,
        venue_id=venue_id,
        timeframe=timeframe,
        effective_window=window(start, end),
        definition_version=definition_version,
        feature_type=feature_type,
        value=value,
        supersedes_ref=supersedes,
    )


def full_valid_kwargs(scope: ContextSubjectScope, definition: ContextDefinition) -> dict[str, object]:
    """A minimal, complete, valid seven-role candidate set that
    `aggregate_context_candidate` accepts and resolves to a full candidate."""
    return dict(
        scope=scope,
        definition=definition,
        candle_candidates=[make_candle()],
        structure_candidates=[make_structure()],
        volatility_regime_candidates=[
            make_regime(
                "regime-vol-1",
                dimension=RegimeDimension.VOLATILITY,
                regime_class=VolatilityRegimeClass.NORMAL,
                definition_version="regime-vol-v1",
                stream_id="stream-regime-vol",
            )
        ],
        directional_persistence_regime_candidates=[
            make_regime(
                "regime-dp-1",
                dimension=RegimeDimension.DIRECTIONAL_PERSISTENCE,
                regime_class=DirectionalPersistenceRegimeClass.DIRECTIONAL,
                definition_version="regime-dp-v1",
                stream_id="stream-regime-dp",
            )
        ],
        volatility_metric_candidates=[
            make_feature(
                "feat-vol-1",
                feature_type=FeatureType.VOLATILITY_METRIC,
                value=Decimal("1.23456789012345"),
                definition_version="feat-vol-v1",
                stream_id="stream-feat-vol",
            )
        ],
        directional_persistence_metric_candidates=[
            make_feature(
                "feat-dp-1",
                feature_type=FeatureType.DIRECTIONAL_PERSISTENCE_METRIC,
                value=Decimal("0.42"),
                definition_version="feat-dp-v1",
                stream_id="stream-feat-dp",
            )
        ],
        distance_to_last_confirmed_swing_candidates=[
            make_feature(
                "feat-dist-1",
                feature_type=FeatureType.DISTANCE_TO_LAST_CONFIRMED_SWING,
                value=Decimal("3.14159265358979"),
                definition_version="feat-dist-v1",
                stream_id="stream-feat-dist",
            )
        ],
    )
