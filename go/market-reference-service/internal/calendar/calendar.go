// Package calendar implements the session/calendar window-resolution
// mechanism venue.md §8 and instrument.md §22 require but explicitly do
// not define concretely (venue.md §17: "cơ chế resolve cụ thể... calendar/
// timezone/reference service, Phase 1"). ADR-032 §B.3 assigns this
// concrete mechanism to market-reference-service's own build transaction
// — this package is that transaction's implementation-level choice, not a
// new domain-semantic decision.
//
// ADR-007 explicitly forbids hardcoding a single universal session model
// ("KHÔNG được giả định... 24/7 trading... một session per day"). This
// package therefore does not hardcode a universal calendar: Calendar is an
// interface, and each Venue's session_calendar_ref (an opaque reference,
// venue.md §8) resolves to a concrete Calendar implementation via a
// Resolver the caller supplies. Only one concrete implementation exists in
// this transaction — Continuous (24/7), matching ADR-007's current actual
// deployment scope ("nội bộ/crypto trước") and the same assumption
// market-data-ingestion's Batch 01 Fake already used. A traditional
// exchange-hours Calendar (open/close/holidays) is a natural future
// extension via this same interface, requiring no architecture change —
// it is not built here because nothing in this transaction's scope
// exercises it.
package calendar

import "time"

// Window is a resolved [Start, End) session/candle window.
type Window struct {
	Start time.Time
	End   time.Time
}

// Calendar resolves the window a given instant falls into, for some
// timeframe granularity.
type Calendar interface {
	// WindowFor returns the [Start, End) window instant t falls into for
	// the given timeframe (e.g. "1m", "5m", "1h"). ok is false if the
	// calendar has no defined window for t (e.g. outside a bounded
	// session) — candle.md §12 case one ("Venue/session hợp lệ đóng"),
	// which this package does not interpret further; the caller decides
	// what "session closed" means for its own purpose.
	WindowFor(t time.Time, timeframe string) (Window, bool)
}

// Continuous is a 24/7, UTC-epoch-aligned Calendar — a deliberate test/
// initial-deployment simplification (see package doc), not a claim that
// all venues are always open (ADR-007).
type Continuous struct {
	TimeframeDurations map[string]time.Duration
}

// NewContinuous builds a Continuous calendar with a small default
// timeframe set.
func NewContinuous() Continuous {
	return Continuous{
		TimeframeDurations: map[string]time.Duration{
			"1m": time.Minute,
			"5m": 5 * time.Minute,
			"1h": time.Hour,
		},
	}
}

// WindowFor implements Calendar.
func (c Continuous) WindowFor(t time.Time, timeframe string) (Window, bool) {
	dur, ok := c.TimeframeDurations[timeframe]
	if !ok {
		return Window{}, false
	}
	start := t.UTC().Truncate(dur)
	return Window{Start: start, End: start.Add(dur)}, true
}

// Resolver maps an opaque session_calendar_ref (venue.md §8) to a concrete
// Calendar. Only Continuous is registered by default (see package doc).
type Resolver struct {
	byRef map[string]Calendar
}

// NewResolver builds a Resolver with the given ref -> Calendar bindings.
func NewResolver(bindings map[string]Calendar) *Resolver {
	return &Resolver{byRef: bindings}
}

// Resolve looks up the Calendar for a session_calendar_ref.
func (r *Resolver) Resolve(sessionCalendarRef string) (Calendar, bool) {
	c, ok := r.byRef[sessionCalendarRef]
	return c, ok
}
