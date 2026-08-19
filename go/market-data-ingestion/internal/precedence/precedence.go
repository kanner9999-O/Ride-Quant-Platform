// Package precedence implements the candle.md §11 5-step duplicate/
// correction/fail-closed precedence algorithm applied when ingestion
// receives a closed-or-correction source fact for a Logical Candle
// Subject.
//
// candle.md §11 itself only specifies the algorithm from Step 1 (identity
// resolution) onward, comparing an incoming fact against facts "already
// processed" / "currently in effect" for the subject. It does not
// separately spell out the case where no fact has been processed yet for
// the subject — there is nothing to duplicate, corrupt, or correct against,
// so this package treats that case as the subject's first authoritative
// close (OutcomeEmitFirstClosed). This is an implementation-level
// completion of the algorithm, not a deviation from it: Steps 3-5 all
// presuppose a prior processed fact to compare against, and none of the
// five steps describes what happens on the very first close.
package precedence

import (
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/candle"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/envelope"
)

// Identity is an opaque, resolved idempotency identity (candle.md §11 Step
// 1) — either the native envelope.SourceIdentity or a fallback identity
// declared explicitly by a source/adapter contract. The algorithm only
// ever compares identities for equality; it never inspects internal
// structure (Chapter 6 §6.8 opaque-ID discipline). The zero value means
// "unresolved" (Step 2).
type Identity struct {
	handle string
}

// NativeIdentity wraps a native envelope.SourceIdentity (candle.md §11 Step
// 1, option 1).
func NativeIdentity(si envelope.SourceIdentity) Identity {
	return Identity{handle: "native:" + si.VenueID + "\x1f" + si.InstrumentID + "\x1f" + si.Type + "\x1f" + si.Value}
}

// FallbackIdentity wraps an identity value already computed by a
// source/adapter contract's declared, deterministic, versioned fallback
// mechanism (candle.md §11 Step 1, option 2). This package does not invent
// fallback algorithms — the caller (ingestion adapter) owns that
// declaration and must ensure it is deterministic and parity-preserving
// across execution modes.
func FallbackIdentity(value string) Identity {
	return Identity{handle: "fallback:" + value}
}

// Equal reports whether two identities are the same.
func (i Identity) Equal(other Identity) bool { return i.handle == other.handle }

// IsZero reports whether the identity is unresolved.
func (i Identity) IsZero() bool { return i.handle == "" }

// SourceFact is an incoming closed-or-correction source fact for a Logical
// Candle Subject (candle.md §11).
type SourceFact struct {
	// Identity is the Step-1-resolved idempotency identity. The zero value
	// means identity resolution failed (neither native source_identity nor
	// a declared fallback was available) — Step 2 applies.
	Identity Identity
	Payload  candle.ClosedPayload
	// EquivalenceDeclared reports whether the source contract explicitly
	// declares equivalence semantics for this fact family (candle.md §11
	// Step 5's "source contract khai báo TƯỜNG MINH equivalence semantics"
	// branch). Never inferred by this package.
	EquivalenceDeclared bool
}

// ProcessedFact is the fact currently authoritative (in effect) for a
// subject, from a prior successful resolution.
type ProcessedFact struct {
	Identity Identity
	Payload  candle.ClosedPayload
	// AuthoritativeRef is the event record currently authoritative for the
	// subject — the correction causation_refs target if this fact must be
	// superseded (candle.md §5 invariant: causation_refs points to the
	// fact "ĐANG authoritative hiện tại").
	AuthoritativeRef envelope.EventRecordRef
}

// Outcome is the precedence algorithm's result.
type Outcome int

const (
	// OutcomeEmitFirstClosed: no prior processed fact for this subject —
	// emit the subject's first CandleClosed. See package doc.
	OutcomeEmitFirstClosed Outcome = iota
	// OutcomeDuplicateZeroEffect: Step 3 (identical payload, same identity)
	// or Step 5 (declared-equivalent payload, different identity).
	OutcomeDuplicateZeroEffect
	// OutcomeEmitCorrected: Step 4 — emit CandleCorrected, causation_refs
	// pointing at Decision.CorrectingRef.
	OutcomeEmitCorrected
	// OutcomeFailClosed: Step 2, Step 3's integrity-violation branch, or
	// Step 5's undeclared-equivalence branch — quarantine, no event
	// appended.
	OutcomeFailClosed
)

// FailReason distinguishes the three distinct fail-closed branches
// (candle.md §11 Steps 2/3/5) — all fail-closed, but for different reasons
// worth preserving for observability/quarantine handling.
type FailReason int

const (
	FailReasonNone FailReason = iota
	// FailReasonUnresolvedIdentity: Step 2 — neither native nor fallback
	// identity resolved.
	FailReasonUnresolvedIdentity
	// FailReasonProvenanceIntegrityViolation: Step 3 — same identity,
	// different payload. "Thiếu provenance KHÔNG phải bằng chứng cho
	// correction."
	FailReasonProvenanceIntegrityViolation
	// FailReasonEquivalenceUndeclared: Step 5 — different identity, same
	// payload, but no declared equivalence semantics.
	FailReasonEquivalenceUndeclared
)

// Decision is the precedence algorithm's output for one SourceFact.
type Decision struct {
	Outcome    Outcome
	FailReason FailReason // valid only when Outcome == OutcomeFailClosed
	// CorrectingRef is the causation_refs target for a CandleCorrected —
	// valid only when Outcome == OutcomeEmitCorrected.
	CorrectingRef envelope.EventRecordRef
}

// Resolve applies the candle.md §11 5-step precedence algorithm.
// existing is nil when no fact has been processed yet for the subject.
func Resolve(fact SourceFact, existing *ProcessedFact) Decision {
	// Step 1/2 — identity resolution.
	if fact.Identity.IsZero() {
		return Decision{Outcome: OutcomeFailClosed, FailReason: FailReasonUnresolvedIdentity}
	}

	if existing == nil {
		return Decision{Outcome: OutcomeEmitFirstClosed}
	}

	if fact.Identity.Equal(existing.Identity) {
		// Step 3 — same identity.
		if payloadEqual(fact.Payload, existing.Payload) {
			return Decision{Outcome: OutcomeDuplicateZeroEffect}
		}
		return Decision{Outcome: OutcomeFailClosed, FailReason: FailReasonProvenanceIntegrityViolation}
	}

	// Identity differs from the currently authoritative fact.
	if !payloadEqual(fact.Payload, existing.Payload) {
		// Step 4 — authoritative value changed: always a correction, never
		// a second CandleClosed.
		return Decision{Outcome: OutcomeEmitCorrected, CorrectingRef: existing.AuthoritativeRef}
	}

	// Step 5 — different identity, same payload.
	if fact.EquivalenceDeclared {
		return Decision{Outcome: OutcomeDuplicateZeroEffect}
	}
	return Decision{Outcome: OutcomeFailClosed, FailReason: FailReasonEquivalenceUndeclared}
}

func payloadEqual(a, b candle.ClosedPayload) bool {
	return a.Open.Equal(b.Open) &&
		a.High.Equal(b.High) &&
		a.Low.Equal(b.Low) &&
		a.Close.Equal(b.Close) &&
		a.Volume.Equal(b.Volume) &&
		a.DataQuality == b.DataQuality
}
