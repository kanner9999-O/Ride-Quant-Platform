// Package query implements market-reference-service's query boundary: the
// concrete two-axis bitemporal contract ADR-032 §B.3 requires. Every
// method here — including identity resolution (closes P3-DL-A-MAJ-01,
// which found identity resolution alone still went through a current/
// static mapping) — takes both required axes as separate, independent
// parameters: an effective-applicability instant and a knowledge
// (recorded_time) cursor — and resolves the deterministic intersection of
// "facts effective for the requested applicability" and "facts visible at
// the supplied knowledge boundary" (instrument.md §20's own selection
// algorithm, which ADR-032 §B.3 cites as already establishing this exact
// two-axis discipline).
//
// Identity resolution (P3-DL-A-MAJ-01 correction): no new Domain Contract
// semantics were needed to fix this — instrument.md §12 already makes
// TradableListing.venue_symbol a forward-looking, bitemporally-revisable
// field (whitelist patchable via TradableListingMetadataRevised), and
// venue.md §1 already makes Venue.venue_identity_ref an opaque external
// reference. Resolving a raw (venue, symbol) pair to canonical identity is
// therefore just reverse-scanning the ALREADY-MODELED bitemporal fold
// (listing.ResolveView/venue's own registration facts) for a match at the
// requested cursor pair, instead of maintaining a separate, non-bitemporal
// side index. rawVenueID is treated as the Venue's venue_identity_ref by
// convention — venue.md §1 leaves the concrete string format of
// venue_identity_ref to "registration authority bên ngoài" (deferred),
// so this is an implementation-level interpretation, not an invented
// domain rule.
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

// ErrUnknownReference is returned when a venue-specific raw reference does
// not resolve at the requested two-axis cursor pair.
var ErrUnknownReference = errors.New("query: venue-specific reference not recognized at the requested cursor")

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

// Service is market-reference-service's query boundary — the concrete
// implementation market-data-ingestion's aligned internal/reference.Provider
// calls against.
type Service struct {
	Instruments *instrument.Registry
	Venues      *venue.Registry
	Listings    *listing.Registry
	Calendars   *calendar.Resolver
}

// NewService builds a Service.
func NewService(instruments *instrument.Registry, venues *venue.Registry, listings *listing.Registry, calendars *calendar.Resolver) *Service {
	return &Service{
		Instruments: instruments,
		Venues:      venues,
		Listings:    listings,
		Calendars:   calendars,
	}
}

// ResolveIdentity maps a venue-specific raw reference to canonical
// instrument_id/venue_id, at the two-axis bitemporal cursor pair ADR-032
// §B.3 requires — the deterministic intersection of facts effective at
// effectiveInstant AND visible at knowledgeCursor. effectiveInstant alone
// never controls the result; a venue_symbol correction/revision recorded
// after knowledgeCursor is invisible regardless of effectiveInstant.
func (s *Service) ResolveIdentity(rawVenueID, rawSymbol string, effectiveInstant, knowledgeCursor time.Time) (Identity, error) {
	venueID, ok := s.resolveVenueID(rawVenueID, effectiveInstant, knowledgeCursor)
	if !ok {
		return Identity{}, ErrUnknownReference
	}
	scope, ok := s.resolveListingByVenueSymbol(venueID, rawSymbol, effectiveInstant, knowledgeCursor)
	if !ok {
		return Identity{}, ErrUnknownReference
	}
	return Identity{InstrumentID: scope.InstrumentID, VenueID: scope.VenueID}, nil
}

// resolveVenueID reverse-scans VenueRegistered facts for one whose
// venue_identity_ref matches rawVenueID, visible at knowledgeCursor and
// effective at effectiveInstant. A Venue's identity/scope is immutable
// once registered (venue.md §1) — the only temporal question is whether
// the registration itself is known/effective yet at this cursor pair, not
// whether the identity_ref value itself has since "changed" (it never
// does; a SCOPE_ERROR correction registers a wholly new venue_id under a
// different identity_ref instead, venue.md §11/§19).
func (s *Service) resolveVenueID(rawVenueID string, effectiveInstant, knowledgeCursor time.Time) (string, bool) {
	for _, rec := range s.Venues.Store.AllRecords() {
		p, ok := rec.Payload.(venue.RegisteredPayload)
		if !ok {
			continue
		}
		if p.Scope.VenueIdentityRef != rawVenueID {
			continue
		}
		if rec.Envelope.RecordedTime.After(knowledgeCursor) {
			continue
		}
		if rec.Envelope.EffectiveTime.After(effectiveInstant) {
			continue
		}
		return p.VenueID, true
	}
	return "", false
}

// resolveListingByVenueSymbol reverse-scans TradableListingCreated facts
// under venueID, resolving each candidate listing's Current View (Steps
// 1-3, listing.ResolveView) at the exact (effectiveInstant,
// knowledgeCursor) cursor pair, and matches on the resulting
// bitemporally-correct venue_symbol — never on the symbol value the
// listing was CREATED with (which a later TradableListingMetadataRevised,
// instrument.md §12, may have superseded going forward, or a correction
// may have superseded historically).
func (s *Service) resolveListingByVenueSymbol(venueID, rawSymbol string, effectiveInstant, knowledgeCursor time.Time) (listing.Scope, bool) {
	seen := make(map[string]bool)
	for _, rec := range s.Listings.Store.AllRecords() {
		p, ok := rec.Payload.(listing.CreatedPayload)
		if !ok {
			continue
		}
		if p.Scope.VenueID != venueID || seen[p.Scope.ListingID] {
			continue
		}
		seen[p.Scope.ListingID] = true

		view := s.Listings.ResolveView(p.Scope.ListingID, effectiveInstant, knowledgeCursor)
		if view.ViewState != fact.ViewValid {
			continue
		}
		if view.VenueSymbol == rawSymbol {
			return listing.Scope{InstrumentID: p.Scope.InstrumentID, VenueID: venueID, ListingID: p.Scope.ListingID}, true
		}
	}
	return listing.Scope{}, false
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
	scope, ok := s.findListingScope(instrumentID, venueID, t, knowledgeCursor)
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
	scope, ok := s.findListingScope(instrumentID, venueID, effectiveInstant, knowledgeCursor)
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

// findListingScope resolves the TradableListing valid for (instrumentID,
// venueID) at the two-axis cursor pair — scanning all listings ever
// created for that pair (a relist after delisting is a wholly new
// listing_id, instrument.md §10 invariant) and returning whichever one
// resolves to a VALID Current View at this exact cursor pair, so
// historical queries against an earlier (now-delisted) listing and
// current queries against its replacement both resolve correctly.
func (s *Service) findListingScope(instrumentID, venueID string, effectiveInstant, knowledgeCursor time.Time) (listing.Scope, bool) {
	seen := make(map[string]bool)
	for _, rec := range s.Listings.Store.AllRecords() {
		p, ok := rec.Payload.(listing.CreatedPayload)
		if !ok {
			continue
		}
		if p.Scope.InstrumentID != instrumentID || p.Scope.VenueID != venueID || seen[p.Scope.ListingID] {
			continue
		}
		seen[p.Scope.ListingID] = true

		view := s.Listings.ResolveView(p.Scope.ListingID, effectiveInstant, knowledgeCursor)
		if view.ViewState == fact.ViewValid {
			return listing.Scope{InstrumentID: instrumentID, VenueID: venueID, ListingID: p.Scope.ListingID}, true
		}
	}
	return listing.Scope{}, false
}
