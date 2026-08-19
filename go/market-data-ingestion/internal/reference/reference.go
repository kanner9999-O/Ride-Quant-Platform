// Package reference defines market-data-ingestion's dependency port onto
// market-reference-service (module-registry.yaml: market-data-ingestion
// depends_on: [market-reference-service]).
//
// market-reference-service is now implemented (go/market-reference-service/,
// under Approved ADR-032 v0.2) — market-data-ingestion still depends only
// on this interface, not on market-reference-service's package directly
// (Go's internal/ visibility rules prevent that cross-module import
// anyway, and doing so would create a compile-time coupling this module's
// dependency-graph entry never authorized). The Fake in this package
// remains a test double, exercised by this module's own tests; a real
// client wiring Provider to market-reference-service's
// internal/query.Service is a deployment-topology concern for a future
// transaction (ADR-032 §B.3 point 3 defers transport, and neither module's
// build has stood up any real transport yet).
//
// Two-axis bitemporal contract (ADR-032 v0.2 §B.3, aligned in this
// transaction — closes the "Known implementation gap" ADR-032 itself
// flagged): every method below takes BOTH required axes as separate,
// mandatory parameters — an effective-applicability instant/window and a
// knowledgeCursor (recorded_time / Replay Cursor) visibility boundary —
// never a single ambiguous temporal parameter. Callers pass
// RawFact.RecordedTime as the knowledge cursor (see ingest/service.go):
// this ingestion pipeline's own processing/recording point is the correct
// "what did we know as of when we processed this fact" boundary,
// consistent with I-3/I-5 no-look-ahead applied to the ingestion pipeline
// itself, not just to the Candle events it produces.
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
// venue-specific observation into canonical Candle event form. Every
// method takes the ADR-032 §B.3 two-axis bitemporal query contract
// explicitly.
type Provider interface {
	// ResolveIdentity maps a venue-specific raw instrument/venue reference
	// to the canonical instrument_id/venue_id used throughout Candle
	// events, as visible at knowledgeCursor (ADR-032 §B.3.b — recorded_time
	// / Replay Cursor boundary). Returns ErrUnknownReference if
	// market-reference-service does not recognize the reference as of that
	// cursor.
	ResolveIdentity(ctx context.Context, rawVenueID, rawInstrumentSymbol string, knowledgeCursor time.Time) (Identity, error)

	// WindowFor resolves the [window_start, window_end) boundary that
	// effectiveInstant falls into, for instrument/venue/timeframe, per the
	// venue's trading calendar/session (candle.md §14: window boundaries
	// "phải suy ra từ trading calendar/session của Venue, KHÔNG
	// hardcode"), as visible at knowledgeCursor (ADR-032 §B.3.b). The
	// result MUST be the deterministic intersection of both axes —
	// effectiveInstant alone must never control what session/calendar
	// definition is used; a session-calendar correction recorded after
	// knowledgeCursor must not be visible to this call, regardless of
	// effectiveInstant (ADR-032 §B.3: "corrections recorded later MUST NOT
	// leak into earlier Replay"). Returns ErrSessionClosed when the
	// session is validly closed at effectiveInstant.
	WindowFor(ctx context.Context, instrumentID, venueID, timeframe string, effectiveInstant, knowledgeCursor time.Time) (WindowBoundary, error)
}
