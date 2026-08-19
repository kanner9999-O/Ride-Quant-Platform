// Package candle implements the Logical Candle Subject (candle.md §1):
// identity, qualifying scope, and state machine.
package candle

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"time"
)

// State is the Logical Candle Subject state machine (candle.md §1).
// UNSEEN is notional — no event asserts it, it is simply "before any event
// exists for this subject" (candle.md §1, "UNSEEN là notional initial
// state").
type State int

const (
	StateUnseen State = iota
	StateProvisional
	StateClosed
)

func (s State) String() string {
	switch s {
	case StateUnseen:
		return "UNSEEN"
	case StateProvisional:
		return "PROVISIONAL"
	case StateClosed:
		return "CLOSED"
	default:
		return "UNKNOWN"
	}
}

// CanTransition reports whether `from -> to` is a declared transition
// (candle.md §1 state_machine.transitions). terminal_states is empty:
// CLOSED never leaves CLOSED to go back to PROVISIONAL, but it accepts a
// CLOSED -> CLOSED self-transition on CandleCorrected.
func CanTransition(from, to State) bool {
	switch {
	case from == StateUnseen && to == StateProvisional: // caused_by CandleObserved
		return true
	case from == StateUnseen && to == StateClosed: // caused_by CandleClosed (historical/closed-only ingestion)
		return true
	case from == StateProvisional && to == StateProvisional: // caused_by CandleObserved
		return true
	case from == StateProvisional && to == StateClosed: // caused_by CandleClosed
		return true
	case from == StateClosed && to == StateClosed: // caused_by CandleCorrected (self-transition, NOT terminal)
		return true
	default:
		return false
	}
}

// Scope is the Logical Candle Subject's qualifying scope: exactly the five
// fields candle.md §1 declares. Two scopes are the same logical subject iff
// all five fields are equal.
type Scope struct {
	InstrumentID string
	VenueID      string
	Timeframe    string
	WindowStart  time.Time
	WindowEnd    time.Time
}

// SubjectID computes the opaque, stable candle_subject_id deterministically
// from the five-field scope (candle.md §1 invariants). candle.md §17
// explicitly defers the concrete algorithm to implementation — this SHA-256
// content-hash construction is that implementation-level decision, made at
// this build transaction. It is not architecture: any deterministic,
// stable, opaque function of the five fields satisfies the domain contract,
// and domain logic elsewhere is forbidden from parsing this value
// (Chapter 6 §6.8) — no downstream code may depend on the hash choice.
//
// Timestamps are canonicalized to UTC RFC3339Nano before hashing so the
// same logical window always produces the same ID regardless of the
// timezone the caller happened to construct it in (required for I-2
// Decision Parity across execution modes).
func (s Scope) SubjectID() string {
	canonical := fmt.Sprintf("%s\x1f%s\x1f%s\x1f%s\x1f%s",
		s.InstrumentID,
		s.VenueID,
		s.Timeframe,
		s.WindowStart.UTC().Format(time.RFC3339Nano),
		s.WindowEnd.UTC().Format(time.RFC3339Nano),
	)
	sum := sha256.Sum256([]byte(canonical))
	return "cnd_" + hex.EncodeToString(sum[:])
}

// Equal reports whether two scopes identify the same logical subject.
func (s Scope) Equal(other Scope) bool {
	return s.SubjectID() == other.SubjectID()
}
