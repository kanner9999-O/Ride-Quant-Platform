// Package reference defines market-data-ingestion's dependency port onto
// market-reference-service (module-registry.yaml: market-data-ingestion
// depends_on: [market-reference-service]).
//
// market-reference-service is NOT implemented in this transaction — see
// this module's README for why (its implementation language does not
// cleanly resolve under ADR-008, and its own Domain Contracts
// (instrument.md/venue.md) are still Draft with the concrete
// calendar/session/precision resolution mechanism explicitly deferred).
// market-data-ingestion therefore depends only on this interface. The Fake
// in this package is a test double, not a reference implementation of
// market-reference-service.
package reference

import (
	"context"
	"errors"
	"time"
)

// ErrSessionClosed is returned by WindowFor when the venue's trading
// session is validly closed at the requested instant. candle.md §12 case
// one ("Venue/session hợp lệ đóng") is explicitly out of candle.md's own
// scope — this module treats it as a signal to skip window resolution
// entirely, not as a gap (candle.md §12: "Candle không tự suy session
// state từ việc vắng mặt candle").
var ErrSessionClosed = errors.New("reference: venue session validly closed at requested instant")

// ErrUnknownReference is returned by ResolveIdentity when the venue-
// specific raw reference is not recognized.
var ErrUnknownReference = errors.New("reference: venue-specific reference not recognized")

// Identity is the canonical instrument/venue identity resolved from a
// venue-specific raw reference (candle.md §14 venue neutrality).
type Identity struct {
	InstrumentID string
	VenueID      string
}

// WindowBoundary is a resolved [Start, End) candle window.
type WindowBoundary struct {
	Start time.Time
	End   time.Time
}

// Provider is the identity + calendar/session resolution market-data-
// ingestion needs from market-reference-service before it may normalize a
// venue-specific observation into canonical Candle event form.
type Provider interface {
	// ResolveIdentity maps a venue-specific raw instrument/venue reference
	// to the canonical instrument_id/venue_id used throughout Candle
	// events. Returns ErrUnknownReference if market-reference-service does
	// not recognize the reference.
	ResolveIdentity(ctx context.Context, rawVenueID, rawInstrumentSymbol string) (Identity, error)

	// WindowFor resolves the [window_start, window_end) boundary that
	// instant t falls into, for instrument/venue/timeframe, per the
	// venue's trading calendar/session (candle.md §14: window boundaries
	// "phải suy ra từ trading calendar/session của Venue, KHÔNG
	// hardcode"). Returns ErrSessionClosed when the session is validly
	// closed at t.
	WindowFor(ctx context.Context, instrumentID, venueID, timeframe string, t time.Time) (WindowBoundary, error)
}
