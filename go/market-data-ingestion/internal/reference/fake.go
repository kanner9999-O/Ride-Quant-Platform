package reference

import (
	"context"
	"fmt"
	"time"
)

// Fake is a test double for Provider. It is NOT a reference implementation
// of market-reference-service: its session model is always-open (24/7,
// UTC-aligned), which is a deliberate test simplification, not a real
// trading-calendar/session resolution (candle.md §14 requires deriving
// window boundaries from the venue's actual calendar/session — that
// mechanism does not exist yet, see this module's README).
type Fake struct {
	// Identities maps "rawVenueID/rawInstrumentSymbol" -> canonical Identity.
	Identities map[string]Identity
	// TimeframeDurations maps a timeframe string (e.g. "1m", "5m", "1h") to
	// its window duration, used to align t into a [Start, End) bucket.
	TimeframeDurations map[string]time.Duration
}

// NewFake builds a Fake with a small default identity/timeframe set
// sufficient for tests and the demo wiring in cmd/marketdataingestion.
func NewFake() *Fake {
	return &Fake{
		Identities: map[string]Identity{
			"binance-spot/BTCUSDT": {InstrumentID: "BTC-USDT", VenueID: "binance-spot"},
			"binance-spot/ETHUSDT": {InstrumentID: "ETH-USDT", VenueID: "binance-spot"},
		},
		TimeframeDurations: map[string]time.Duration{
			"1m": time.Minute,
			"5m": 5 * time.Minute,
			"1h": time.Hour,
		},
	}
}

// ResolveIdentity implements Provider.
func (f *Fake) ResolveIdentity(_ context.Context, rawVenueID, rawInstrumentSymbol string) (Identity, error) {
	id, ok := f.Identities[rawVenueID+"/"+rawInstrumentSymbol]
	if !ok {
		return Identity{}, fmt.Errorf("%w: %s/%s", ErrUnknownReference, rawVenueID, rawInstrumentSymbol)
	}
	return id, nil
}

// WindowFor implements Provider using an always-open, UTC-epoch-aligned
// session — see the Fake doc comment for why this is not a real
// calendar/session implementation.
func (f *Fake) WindowFor(_ context.Context, _, _, timeframe string, t time.Time) (WindowBoundary, error) {
	dur, ok := f.TimeframeDurations[timeframe]
	if !ok {
		return WindowBoundary{}, fmt.Errorf("reference: fake has no configured duration for timeframe %q", timeframe)
	}
	utc := t.UTC()
	bucketStart := utc.Truncate(dur)
	return WindowBoundary{Start: bucketStart, End: bucketStart.Add(dur)}, nil
}
