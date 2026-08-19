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
// Fake DOES honor the ADR-032 §B.3 two-axis contract for ALL THREE
// reference lookups Provider exposes — identity, window, precision-
// adjacent duration — for the purpose of this module's own tests:
// corrections/revisions can be registered with an explicit effective_time
// and recorded_time via ReviseIdentity/ReviseDuration, and every Provider
// method resolves strictly as the deterministic intersection of "facts
// effective at effectiveInstant" AND "facts visible at knowledgeCursor" —
// a correction recorded after knowledgeCursor is invisible regardless of
// effectiveInstant, and effectiveInstant alone never controls visibility.
// This lets this module's own tests exercise the same look-ahead
// discipline go/market-reference-service/internal/query's own tests
// exercise against the real implementation, without this module depending
// on that module's package (Go internal/ visibility prevents that import
// anyway).
//
// P3-DL-A-MAJ-01 correction: identity resolution previously ignored both
// axes (a bare static map) — Identities below is now only the BASE
// mapping in effect "from the beginning of time"; ReviseIdentity registers
// bitemporal corrections/revisions on top of it, mirroring ReviseDuration.
type Fake struct {
	// Identities is the base "rawVenueID/rawInstrumentSymbol" -> canonical
	// Identity mapping in effect before any revision.
	Identities map[string]Identity
	// identityRevisions is an unordered log of identity corrections/
	// revisions per raw reference key; resolved at query time by the
	// two-axis cursor pair (see resolveIdentity).
	identityRevisions map[string][]identityRevision

	// baseDurations is the timeframe -> duration mapping in effect before
	// any correction (i.e. as of the beginning of time).
	baseDurations map[string]time.Duration
	// revisions is an unordered log of corrections per timeframe; resolved
	// at query time by the two-axis cursor pair (see resolveDuration).
	revisions map[string][]durationRevision
}

type identityRevision struct {
	identity      Identity
	effectiveTime time.Time
	recordedTime  time.Time
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
		identityRevisions: make(map[string][]identityRevision),
		baseDurations: map[string]time.Duration{
			"1m": time.Minute,
			"5m": 5 * time.Minute,
			"1h": time.Hour,
		},
		revisions: make(map[string][]durationRevision),
	}
}

// ReviseIdentity registers a corrected/revised identity mapping for
// (rawVenueID, rawInstrumentSymbol), effective from effectiveTime onward,
// visible only to queries whose knowledgeCursor is at or after
// recordedTime (ADR-032 §B.3) — for tests exercising the identity
// bitemporal look-ahead guard (P3-DL-A-MAJ-01).
func (f *Fake) ReviseIdentity(rawVenueID, rawInstrumentSymbol string, newIdentity Identity, effectiveTime, recordedTime time.Time) {
	key := rawVenueID + "/" + rawInstrumentSymbol
	f.identityRevisions[key] = append(f.identityRevisions[key], identityRevision{identity: newIdentity, effectiveTime: effectiveTime, recordedTime: recordedTime})
}

func (f *Fake) resolveIdentity(rawVenueID, rawInstrumentSymbol string, effectiveInstant, knowledgeCursor time.Time) (Identity, bool) {
	key := rawVenueID + "/" + rawInstrumentSymbol
	id, ok := f.Identities[key]

	revs := append([]identityRevision(nil), f.identityRevisions[key]...)
	sort.Slice(revs, func(i, j int) bool { return revs[i].effectiveTime.Before(revs[j].effectiveTime) })
	for _, rev := range revs {
		if rev.effectiveTime.After(effectiveInstant) {
			continue
		}
		if rev.recordedTime.After(knowledgeCursor) {
			continue
		}
		id = rev.identity
		ok = true
	}
	return id, ok
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

// ResolveIdentity implements Provider — resolved as the deterministic
// intersection of effectiveInstant and knowledgeCursor (P3-DL-A-MAJ-01;
// ADR-032 §B.3), the same two-axis discipline WindowFor already honors.
func (f *Fake) ResolveIdentity(_ context.Context, rawVenueID, rawInstrumentSymbol string, effectiveInstant, knowledgeCursor time.Time) (Identity, error) {
	id, ok := f.resolveIdentity(rawVenueID, rawInstrumentSymbol, effectiveInstant, knowledgeCursor)
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
