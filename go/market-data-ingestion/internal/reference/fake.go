package reference

import (
	"context"
	"fmt"
	"sort"
	"time"
)

// Fake is a test double for Provider. It is NOT a reference implementation
// of market-reference-service (a real implementation now exists at
// go/market-reference-service/): its session model is always-open (24/7,
// UTC-aligned), a deliberate test simplification, not a real trading-
// calendar/session resolution.
//
// Fake DOES honor the ADR-032 §B.3 two-axis contract for the purpose of
// this module's own tests: timeframe-duration "corrections" can be
// registered with an explicit recorded_time via ReviseDuration, and
// WindowFor/ResolveIdentity resolve strictly as of the supplied
// knowledgeCursor — a correction recorded after knowledgeCursor is
// invisible to that call, regardless of effectiveInstant. This lets
// service_test.go exercise the same look-ahead discipline
// go/market-reference-service/internal/query's own tests exercise against
// the real implementation, without this module depending on that module's
// package (Go internal/ visibility prevents that import anyway).
type Fake struct {
	// Identities maps "rawVenueID/rawInstrumentSymbol" -> canonical Identity.
	Identities map[string]Identity
	// baseDurations is the timeframe -> duration mapping in effect before
	// any correction (i.e. as of the beginning of time).
	baseDurations map[string]time.Duration
	// revisions is an unordered log of corrections per timeframe; resolved
	// at query time by knowledgeCursor (see resolveDuration).
	revisions map[string][]durationRevision
}

type durationRevision struct {
	recordedTime time.Time
	duration     time.Duration
}

// NewFake builds a Fake with a small default identity/timeframe set
// sufficient for tests and the demo wiring in cmd/marketdataingestion.
func NewFake() *Fake {
	return &Fake{
		Identities: map[string]Identity{
			"binance-spot/BTCUSDT": {InstrumentID: "BTC-USDT", VenueID: "binance-spot"},
			"binance-spot/ETHUSDT": {InstrumentID: "ETH-USDT", VenueID: "binance-spot"},
		},
		baseDurations: map[string]time.Duration{
			"1m": time.Minute,
			"5m": 5 * time.Minute,
			"1h": time.Hour,
		},
		revisions: make(map[string][]durationRevision),
	}
}

// ReviseDuration registers a correction to timeframe's window duration,
// visible only to queries whose knowledgeCursor is at or after
// recordedTime (ADR-032 §B.3.b) — for tests exercising bitemporal
// look-ahead behavior.
func (f *Fake) ReviseDuration(timeframe string, newDuration time.Duration, recordedTime time.Time) {
	f.revisions[timeframe] = append(f.revisions[timeframe], durationRevision{recordedTime: recordedTime, duration: newDuration})
}

func (f *Fake) resolveDuration(timeframe string, knowledgeCursor time.Time) (time.Duration, bool) {
	d, ok := f.baseDurations[timeframe]
	revs := append([]durationRevision(nil), f.revisions[timeframe]...)
	sort.Slice(revs, func(i, j int) bool { return revs[i].recordedTime.Before(revs[j].recordedTime) })
	for _, rev := range revs {
		if !rev.recordedTime.After(knowledgeCursor) {
			d = rev.duration
			ok = true
		}
	}
	return d, ok
}

// ResolveIdentity implements Provider. The Fake's identity index is static
// (not itself bitemporally corrected) — knowledgeCursor is accepted for
// interface conformance but does not affect resolution, a documented
// simplification consistent with go/market-reference-service's own README
// ("A real symbol-to-listing index... not built here").
func (f *Fake) ResolveIdentity(_ context.Context, rawVenueID, rawInstrumentSymbol string, _ time.Time) (Identity, error) {
	id, ok := f.Identities[rawVenueID+"/"+rawInstrumentSymbol]
	if !ok {
		return Identity{}, fmt.Errorf("%w: %s/%s", ErrUnknownReference, rawVenueID, rawInstrumentSymbol)
	}
	return id, nil
}

// WindowFor implements Provider using an always-open, UTC-epoch-aligned
// session (see Fake doc) — but DOES honor knowledgeCursor for timeframe-
// duration corrections registered via ReviseDuration.
func (f *Fake) WindowFor(_ context.Context, _, _, timeframe string, effectiveInstant, knowledgeCursor time.Time) (WindowBoundary, error) {
	dur, ok := f.resolveDuration(timeframe, knowledgeCursor)
	if !ok {
		return WindowBoundary{}, fmt.Errorf("reference: fake has no configured duration for timeframe %q as of knowledge cursor %v", timeframe, knowledgeCursor)
	}
	utc := effectiveInstant.UTC()
	bucketStart := utc.Truncate(dur)
	return WindowBoundary{Start: bucketStart, End: bucketStart.Add(dur)}, nil
}
