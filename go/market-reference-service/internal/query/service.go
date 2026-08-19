// Package query implements market-reference-service's query boundary: the
// concrete two-axis bitemporal contract ADR-032 §B.3 requires. Every
// method here takes both required axes as separate, independent
// parameters — an effective-applicability instant and a knowledge
// (recorded_time) cursor — and resolves the deterministic intersection of
// "facts effective for the requested applicability" and "facts visible at
// the supplied knowledge boundary" (instrument.md §20's own selection
// algorithm, which ADR-032 §B.3 cites as already establishing this exact
// two-axis discipline).
package query

import (
	"errors"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/calendar"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/decimal"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/fact"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/instrument"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/listing"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/venue"
)

// ErrUnknownReference is returned when a venue-specific raw reference is
// not recognized.
var ErrUnknownReference = errors.New("query: venue-specific reference not recognized")

// ErrNoCalendarBinding is returned when a listing's session_calendar_ref
// does not resolve to a registered calendar.Calendar.
var ErrNoCalendarBinding = errors.New("query: session_calendar_ref has no registered calendar binding")

// ErrWindowNotResolved is returned when the resolved calendar has no
// defined window for the requested instant/timeframe (candle.md §12 case
// one — this package does not interpret that further; see
// go/market-data-ingestion's reference.ErrSessionClosed on the consumer
// side).
var ErrWindowNotResolved = errors.New("query: calendar has no window for the requested instant/timeframe")

// Identity is the canonical instrument/venue identity resolved from a
// venue-specific raw reference.
type Identity struct {
	InstrumentID string
	VenueID      string
}

// symbolBinding is a known (raw venue-specific reference) -> (canonical
// listing scope) association. See Service doc: this is a static index, a
// documented simplification (see README known-gaps) — a full
// implementation would resolve this through TradableListing's own
// bitemporal venue_symbol history, not a single current mapping.
type symbolBinding struct {
	rawVenueID, rawSymbol string
}

// Service is market-reference-service's query boundary — the concrete
// implementation market-data-ingestion's aligned internal/reference.Provider
// calls against.
type Service struct {
	Instruments *instrument.Registry
	Venues      *venue.Registry
	Listings    *listing.Registry
	Calendars   *calendar.Resolver

	bySymbol map[symbolBinding]listing.Scope
}

// NewService builds a Service.
func NewService(instruments *instrument.Registry, venues *venue.Registry, listings *listing.Registry, calendars *calendar.Resolver) *Service {
	return &Service{
		Instruments: instruments,
		Venues:      venues,
		Listings:    listings,
		Calendars:   calendars,
		bySymbol:    make(map[symbolBinding]listing.Scope),
	}
}

// RegisterSymbolBinding records that a venue-specific raw reference
// identifies the given listing scope. See Service/symbolBinding doc for
// the simplification this represents.
func (s *Service) RegisterSymbolBinding(rawVenueID, rawSymbol string, scope listing.Scope) {
	s.bySymbol[symbolBinding{rawVenueID, rawSymbol}] = scope
}

// ResolveIdentity maps a venue-specific raw reference to canonical
// instrument_id/venue_id.
func (s *Service) ResolveIdentity(rawVenueID, rawSymbol string) (Identity, error) {
	scope, ok := s.bySymbol[symbolBinding{rawVenueID, rawSymbol}]
	if !ok {
		return Identity{}, ErrUnknownReference
	}
	return Identity{InstrumentID: scope.InstrumentID, VenueID: scope.VenueID}, nil
}

// ResolveWindow resolves the [Start, End) window instant t falls into for
// (instrumentID, venueID, timeframe), per the venue's trading calendar/
// session — the two-axis bitemporal query ADR-032 §B.3 mandates:
//   - effectiveApplicability = t (the effective instant the window must
//     cover);
//   - knowledgeCursor = the Replay-Cursor/recorded_time boundary limiting
//     which TradableListing facts (including corrections) are visible.
//
// The resolved SessionCalendarRef is read from the TradableListing bound
// to (instrumentID, venueID) at this exact cursor pair — never from
// current/live state (ADR-032 §B.3: "current wall clock/current live
// state MUST NOT answer bounded historical queries").
func (s *Service) ResolveWindow(instrumentID, venueID, timeframe string, t, knowledgeCursor time.Time) (calendar.Window, error) {
	scope, ok := s.findListingScope(instrumentID, venueID)
	if !ok {
		return calendar.Window{}, ErrUnknownReference
	}
	view := s.Listings.ResolveView(scope.ListingID, t, knowledgeCursor)
	if view.SessionCalendarRef == "" {
		return calendar.Window{}, ErrUnknownReference
	}
	cal, ok := s.Calendars.Resolve(view.SessionCalendarRef)
	if !ok {
		return calendar.Window{}, ErrNoCalendarBinding
	}
	window, ok := cal.WindowFor(t, timeframe)
	if !ok {
		return calendar.Window{}, ErrWindowNotResolved
	}
	return window, nil
}

// Precision is the resolved tick/lot metadata for a listing at a given
// two-axis bitemporal cursor pair.
type Precision struct {
	PriceIncrement    decimal.Decimal
	QuantityIncrement decimal.Decimal
	MinQuantity       *decimal.Decimal
	MinNotional       *decimal.Decimal
}

// ResolvePrecision resolves (instrumentID, venueID)'s precision/tick/lot
// metadata at the two-axis bitemporal cursor pair (effective instant +
// knowledge cursor) — same look-ahead discipline as ResolveWindow.
func (s *Service) ResolvePrecision(instrumentID, venueID string, effectiveInstant, knowledgeCursor time.Time) (Precision, error) {
	scope, ok := s.findListingScope(instrumentID, venueID)
	if !ok {
		return Precision{}, ErrUnknownReference
	}
	view := s.Listings.ResolveView(scope.ListingID, effectiveInstant, knowledgeCursor)
	if view.ViewState != fact.ViewValid {
		return Precision{}, ErrUnknownReference
	}
	return Precision{
		PriceIncrement:    view.PriceIncrement,
		QuantityIncrement: view.QuantityIncrement,
		MinQuantity:       view.MinQuantity,
		MinNotional:       view.MinNotional,
	}, nil
}

func (s *Service) findListingScope(instrumentID, venueID string) (listing.Scope, bool) {
	for _, scope := range s.bySymbol {
		if scope.InstrumentID == instrumentID && scope.VenueID == venueID {
			return scope, true
		}
	}
	return listing.Scope{}, false
}
