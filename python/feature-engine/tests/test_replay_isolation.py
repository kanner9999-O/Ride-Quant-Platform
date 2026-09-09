"""`P3-FEATURE-QG-EVID-05(a)` — I-5 Decision-Time Observable Dependency,
self-contained replay execution (Constitution `02-platform-invariants.md`
I-5; `feature-engine-chapter13-remediation-plan-001.md` §1/§2 row `EVID-05`).

I-5 requires two strictly separated phases: *Replay preparation* (external
resolution -- reading Input Contract/Stream Registry authority off the
repository filesystem -- is allowed) and *Replay execution* (must depend
only on already-materialized, persisted/cached state; never touches an
external source again).

Every computation engine here already resolves its own
`VerifiedInputContractAuthority` exactly once, at construction time, through
an injected `InputContractAuthorityProvider` (`contracts.py`), and caches it
as `self._resolved_input_contract` -- `authority_resolver.py` is the ONLY
module anywhere in `src/feature_engine/` that performs filesystem I/O, and
nothing in this package performs network I/O at all. This module proves
that design genuinely satisfies I-5(a): after construction, real filesystem
and network primitives are cut fail-closed, the cut is proven to guard the
actual reachable boundary (not a vacuous mock nobody calls), and real
public runtime handlers across all three "consumes cached authority"/
"pure projection" classes -- `SwingDistanceFeatureEngine`,
`RegimePassthroughFeatureEngine`, `FeatureCurrentView` -- still produce
correct events end-to-end using only that already-materialized state.

Does NOT address `EVID-05(b)` (persisted content-identity checksum in
`ComputationCursor`) -- out of scope for this transaction.
"""

from __future__ import annotations

import builtins
import socket
from datetime import timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
from conftest import (
    OUTPUT_EVENT_CONTRACT_AUTHORITY,
    REGIME_INPUT_CONTRACT,
    SWING_DISTANCE_INPUT_CONTRACT,
    FixedDeltaTimeSource,
    authorized_candle_contract_refs,
    authorized_swing_contract_refs,
    candle_at,
    current_result,
    feature_scope,
    frontier_at,
    make_distance_definition,
    make_regime_definition,
    only_computed,
    only_invalidated,
    regime_classified_at,
    regime_invalidated_at,
    swing_confirmed_at,
)

from feature_engine import (
    FeatureCurrentView,
    RegimePassthroughFeatureEngine,
    SequenceAllocator,
    StaticInputContractAuthorityProvider,
    StaticOutputEventContractAuthorityProvider,
    SwingDistanceFeatureEngine,
    resolve_input_contract_authority_from_repository,
)


class ExternalAccessCutError(AssertionError):
    """Raised by every guard `_install_external_access_cut` installs. If
    this ever surfaces from inside a runtime handler call (rather than from
    this module's own direct probes), that handler illegally touched the
    filesystem or network during what I-5 designates Replay execution.
    """


def _install_external_access_cut(monkeypatch: pytest.MonkeyPatch) -> None:
    """Cuts the actual, reachable filesystem/network primitives -- not a
    substitute for `authority_resolver.py`'s own call sites, which would be
    provable vacuously (nothing calls them post-construction regardless of
    whether this guard exists). `Path.read_bytes`/`Path.read_text` and
    `builtins.open` are exactly what `authority_resolver.py` itself uses to
    read the Input Contract/Stream Registry YAML files; `socket.socket.
    connect`/`socket.create_connection` are the two standard-library entry
    points any future network access would have to go through.
    """

    def _blocked_read_bytes(self: Path, *args: Any, **kwargs: Any) -> bytes:
        raise ExternalAccessCutError(f"blocked filesystem read via Path.read_bytes({self!r})")

    def _blocked_read_text(self: Path, *args: Any, **kwargs: Any) -> str:
        raise ExternalAccessCutError(f"blocked filesystem read via Path.read_text({self!r})")

    def _blocked_open(*args: Any, **kwargs: Any) -> Any:
        raise ExternalAccessCutError(f"blocked filesystem access via open(args={args!r})")

    def _blocked_socket_connect(self: socket.socket, *args: Any, **kwargs: Any) -> Any:
        raise ExternalAccessCutError(f"blocked network access via socket.connect(args={args!r})")

    def _blocked_create_connection(*args: Any, **kwargs: Any) -> Any:
        raise ExternalAccessCutError(f"blocked network access via socket.create_connection(args={args!r})")

    monkeypatch.setattr(Path, "read_bytes", _blocked_read_bytes)
    monkeypatch.setattr(Path, "read_text", _blocked_read_text)
    monkeypatch.setattr(builtins, "open", _blocked_open)
    monkeypatch.setattr(socket.socket, "connect", _blocked_socket_connect)
    monkeypatch.setattr(socket, "create_connection", _blocked_create_connection)


def test_external_access_cut_guards_the_real_reachable_boundary(monkeypatch: pytest.MonkeyPatch) -> None:
    """Proves the cut installed below is itself active against the actual
    primitives a runtime handler could reach -- including the real,
    production `resolve_input_contract_authority_from_repository` call
    path itself, not merely a mock nobody calls."""
    _install_external_access_cut(monkeypatch)

    with pytest.raises(ExternalAccessCutError):
        Path(__file__).read_bytes()

    with pytest.raises(ExternalAccessCutError):
        Path(__file__).read_text()

    with pytest.raises(ExternalAccessCutError):
        open(__file__)

    with pytest.raises(ExternalAccessCutError):
        socket.create_connection(("127.0.0.1", 9), timeout=0.01)

    with pytest.raises(ExternalAccessCutError):
        probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            probe.connect(("127.0.0.1", 9))
        finally:
            probe.close()

    # The real production authority-resolution path (the only filesystem-
    # touching code anywhere in src/feature_engine/) is itself unusable
    # while the cut is active -- confirms the guard sits on the actual
    # boundary this design relies on, not an adjacent substitute.
    with pytest.raises(ExternalAccessCutError):
        resolve_input_contract_authority_from_repository("regime")


def test_replay_execution_is_self_contained_after_construction(
    monkeypatch: pytest.MonkeyPatch, allocator: SequenceAllocator, time_source: FixedDeltaTimeSource
) -> None:
    """EVID-05(a): construct real engines/projections using ALREADY-
    materialized authority (`SWING_DISTANCE_INPUT_CONTRACT`/`REGIME_INPUT_
    CONTRACT` were resolved once, from the real repository, at conftest
    module-import time -- this test's own Replay-preparation-equivalent
    boundary), THEN cut filesystem/network fail-closed, THEN exercise real
    public runtime handlers end-to-end and assert genuinely correct event
    production -- proving no handler needs, or silently performs, any
    further external resolution during what I-5 designates Replay
    execution.
    """
    swing_definition = make_distance_definition()
    swing_scope = feature_scope("distance_to_last_confirmed_swing", version=swing_definition.feature_definition_version)
    swing_engine = SwingDistanceFeatureEngine(
        swing_scope,
        swing_definition,
        allocator,
        time_source,
        output_event_contract_authority_provider=StaticOutputEventContractAuthorityProvider(
            OUTPUT_EVENT_CONTRACT_AUTHORITY
        ),
        authorized_candle_contract_refs=authorized_candle_contract_refs(),
        authorized_swing_contract_refs=authorized_swing_contract_refs(),
        input_contract_authority_provider=StaticInputContractAuthorityProvider(SWING_DISTANCE_INPUT_CONTRACT),
    )

    regime_definition = make_regime_definition(regime_dimension_version="rgd-1")
    regime_scope = feature_scope("volatility_metric", version=regime_definition.feature_definition_version)
    regime_engine = RegimePassthroughFeatureEngine(
        regime_scope,
        regime_definition,
        allocator,
        time_source,
        output_event_contract_authority_provider=StaticOutputEventContractAuthorityProvider(
            OUTPUT_EVENT_CONTRACT_AUTHORITY
        ),
        input_contract_authority_provider=StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT),
    )

    swing_view = FeatureCurrentView(swing_scope)
    regime_view = FeatureCurrentView(regime_scope)

    # --- construction/materialization complete -- cut external access now ---
    _install_external_access_cut(monkeypatch)

    # Swing-distance path: confirm a swing, then a covering candle, exactly
    # as the ordinary (non-replay-isolation) test_swing_distance.py suite
    # does -- same production authority flow, not a substitute path.
    swing = swing_confirmed_at(allocator, pivot_index=8, swing_id="s1", pivot_price="100")
    swing_engine.on_swing_confirmed(swing, cursor=frontier_at(swing.recorded_time))
    reference_candle = candle_at(allocator, 10, high="110", low="90", close="105")
    swing_events = swing_engine.on_candle(reference_candle, cursor=frontier_at(reference_candle.recorded_time))
    assert len(swing_events) == 1
    swing_computed = only_computed(swing_events[0])
    assert swing_computed.value == Decimal("5.00")  # 105 - 100

    swing_view.on_feature_computed(swing_computed)
    assert current_result(swing_view).value == Decimal("5.00")

    # Regime pass-through path: original computation, then a correction
    # (invalidate + implicit replacement window), exercising both
    # `on_regime_classified` and `on_regime_invalidated`.
    regime_original_fact = regime_classified_at(
        allocator, 0, computed_metric="1.5", regime_dimension="volatility", regime_definition_version="rgd-1"
    )
    regime_original = only_computed(
        regime_engine.on_regime_classified(
            regime_original_fact,
            cursor=frontier_at(regime_original_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT),
        )[0]
    )
    assert regime_original.value == Decimal("1.50")

    regime_view.on_feature_computed(regime_original)
    assert current_result(regime_view).value == Decimal("1.50")

    regime_invalidation_fact = regime_invalidated_at(
        allocator,
        invalidated_fact_ref=regime_original_fact.ref,
        recorded_time=regime_original.recorded_time + timedelta(minutes=5),
    )
    regime_invalidation = only_invalidated(
        regime_engine.on_regime_invalidated(
            regime_invalidation_fact,
            cursor=frontier_at(regime_invalidation_fact.recorded_time, resolved_input_contract=REGIME_INPUT_CONTRACT),
        )[0]
    )
    assert regime_invalidation.invalidated_fact_ref == regime_original.ref

    regime_view.on_feature_invalidated(regime_invalidation)
    pending = regime_view.current()
    assert pending is not None
    assert pending.view_state == "PENDING_CORRECTION"

    # Final proof this design is genuinely cache-only, not merely "happened
    # not to call" an external source: every handler above executed to
    # completion, with real, correct results, while Path.read_bytes/
    # read_text, builtins.open, and both socket entry points were all
    # actively raising -- if any handler had performed, or silently
    # attempted, filesystem/network access, this test would have failed
    # with `ExternalAccessCutError` surfacing from inside that call instead
    # of reaching these assertions.
