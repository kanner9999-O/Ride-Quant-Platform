package precedence

import (
	"testing"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/candle"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/decimal"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/envelope"
)

func payload(close string) candle.ClosedPayload {
	return candle.ClosedPayload{
		OHLCV: candle.OHLCV{
			Open:   decimal.MustFromString("100"),
			High:   decimal.MustFromString("110"),
			Low:    decimal.MustFromString("90"),
			Close:  decimal.MustFromString(close),
			Volume: decimal.MustFromString("5"),
		},
		DataQuality: candle.DataQualityComplete,
	}
}

func nativeID(value string) Identity {
	return NativeIdentity(envelope.SourceIdentity{VenueID: "binance-spot", InstrumentID: "BTC-USDT", Type: "kline_update_id", Value: value})
}

func TestResolveUnresolvedIdentityFailsClosed(t *testing.T) {
	fact := SourceFact{Payload: payload("105")} // zero-value Identity
	got := Resolve(fact, nil)
	if got.Outcome != OutcomeFailClosed || got.FailReason != FailReasonUnresolvedIdentity {
		t.Fatalf("Resolve() = %+v, want FailClosed/UnresolvedIdentity", got)
	}
	// Must fail-closed even when a prior fact exists.
	existing := &ProcessedFact{Identity: nativeID("1"), Payload: payload("105")}
	got2 := Resolve(fact, existing)
	if got2.Outcome != OutcomeFailClosed || got2.FailReason != FailReasonUnresolvedIdentity {
		t.Fatalf("Resolve() with existing = %+v, want FailClosed/UnresolvedIdentity", got2)
	}
}

func TestResolveFirstCloseForSubject(t *testing.T) {
	fact := SourceFact{Identity: nativeID("1"), Payload: payload("105")}
	got := Resolve(fact, nil)
	if got.Outcome != OutcomeEmitFirstClosed {
		t.Fatalf("Resolve() = %+v, want EmitFirstClosed", got)
	}
}

func TestResolveStep3DuplicateIdenticalPayload(t *testing.T) {
	existing := &ProcessedFact{Identity: nativeID("1"), Payload: payload("105")}
	fact := SourceFact{Identity: nativeID("1"), Payload: payload("105")} // same identity, same payload
	got := Resolve(fact, existing)
	if got.Outcome != OutcomeDuplicateZeroEffect {
		t.Fatalf("Resolve() = %+v, want DuplicateZeroEffect", got)
	}
}

func TestResolveStep3ProvenanceIntegrityViolation(t *testing.T) {
	existing := &ProcessedFact{Identity: nativeID("1"), Payload: payload("105")}
	fact := SourceFact{Identity: nativeID("1"), Payload: payload("999")} // same identity, DIFFERENT payload
	got := Resolve(fact, existing)
	if got.Outcome != OutcomeFailClosed || got.FailReason != FailReasonProvenanceIntegrityViolation {
		t.Fatalf("Resolve() = %+v, want FailClosed/ProvenanceIntegrityViolation", got)
	}
}

func TestResolveStep4EmitsCorrected(t *testing.T) {
	authRef := envelope.EventRecordRef{StreamID: "binance-candle", Sequence: 7, EventID: "evt-original"}
	existing := &ProcessedFact{Identity: nativeID("1"), Payload: payload("105"), AuthoritativeRef: authRef}
	fact := SourceFact{Identity: nativeID("2"), Payload: payload("106")} // different identity, changed payload
	got := Resolve(fact, existing)
	if got.Outcome != OutcomeEmitCorrected {
		t.Fatalf("Resolve() = %+v, want EmitCorrected", got)
	}
	if got.CorrectingRef != authRef {
		t.Fatalf("CorrectingRef = %+v, want %+v (must point to currently-authoritative fact)", got.CorrectingRef, authRef)
	}
}

func TestResolveStep4NeverProducesSecondClosed(t *testing.T) {
	// Regression guard: a changed, differently-identified fact must ALWAYS
	// resolve to EmitCorrected, never to any "second closed" outcome —
	// there is no such outcome in this API by construction, but assert the
	// specific branch explicitly.
	existing := &ProcessedFact{Identity: nativeID("1"), Payload: payload("105")}
	fact := SourceFact{Identity: nativeID("2"), Payload: payload("999")}
	got := Resolve(fact, existing)
	if got.Outcome == OutcomeEmitFirstClosed {
		t.Fatalf("a changed fact for a subject with an existing authoritative fact must never be treated as a first close")
	}
	if got.Outcome != OutcomeEmitCorrected {
		t.Fatalf("Resolve() = %+v, want EmitCorrected", got)
	}
}

func TestResolveStep5DeclaredEquivalenceIsDuplicate(t *testing.T) {
	existing := &ProcessedFact{Identity: nativeID("1"), Payload: payload("105")}
	fact := SourceFact{Identity: nativeID("2"), Payload: payload("105"), EquivalenceDeclared: true} // different identity, same payload
	got := Resolve(fact, existing)
	if got.Outcome != OutcomeDuplicateZeroEffect {
		t.Fatalf("Resolve() = %+v, want DuplicateZeroEffect", got)
	}
}

func TestResolveStep5UndeclaredEquivalenceFailsClosed(t *testing.T) {
	existing := &ProcessedFact{Identity: nativeID("1"), Payload: payload("105")}
	fact := SourceFact{Identity: nativeID("2"), Payload: payload("105"), EquivalenceDeclared: false}
	got := Resolve(fact, existing)
	if got.Outcome != OutcomeFailClosed || got.FailReason != FailReasonEquivalenceUndeclared {
		t.Fatalf("Resolve() = %+v, want FailClosed/EquivalenceUndeclared", got)
	}
}

func TestIdentityEqualAndZero(t *testing.T) {
	var zero Identity
	if !zero.IsZero() {
		t.Fatalf("zero-value Identity.IsZero() = false")
	}
	a := nativeID("1")
	if a.IsZero() {
		t.Fatalf("resolved Identity.IsZero() = true")
	}
	b := nativeID("1")
	if !a.Equal(b) {
		t.Fatalf("expected identical native identities to be Equal")
	}
	c := nativeID("2")
	if a.Equal(c) {
		t.Fatalf("expected different native identities to not be Equal")
	}
	f1 := FallbackIdentity("x")
	f2 := FallbackIdentity("x")
	if !f1.Equal(f2) {
		t.Fatalf("expected identical fallback identities to be Equal")
	}
	if a.Equal(f1) {
		t.Fatalf("native and fallback identities with unrelated values must not collide")
	}
}
