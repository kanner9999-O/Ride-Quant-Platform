package candle

import (
	"testing"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/envelope"
)

func TestNewObservedDraftIsRootEvent(t *testing.T) {
	s := mkScope()
	now := time.Now().UTC()
	d := NewObservedDraft("evt-1", s, now, true, nil)

	if d.EventType != EventTypeObserved {
		t.Errorf("EventType = %q, want %q", d.EventType, EventTypeObserved)
	}
	if len(d.CausationRefs) != 0 {
		t.Errorf("root event CausationRefs must be empty, got %v", d.CausationRefs)
	}
	if d.CausationRefs == nil {
		t.Errorf("root event CausationRefs must be [] not nil (candle.md §2: 'root event có thể rỗng ([]), không absent')")
	}
	if d.EffectiveTime == nil || !d.EffectiveTime.WindowStart.Equal(s.WindowStart) || !d.EffectiveTime.WindowEnd.Equal(s.WindowEnd) {
		t.Errorf("EffectiveTime = %+v, want window [%v, %v)", d.EffectiveTime, s.WindowStart, s.WindowEnd)
	}
	if d.MarketTime == nil || !d.MarketTime.Equal(s.WindowStart) {
		t.Errorf("MarketTime = %v, want %v (candle.md §8: market_time = window_start)", d.MarketTime, s.WindowStart)
	}
	if d.SubjectRef.SubjectID != s.SubjectID() {
		t.Errorf("SubjectRef.SubjectID = %q, want %q", d.SubjectRef.SubjectID, s.SubjectID())
	}
	if d.SubjectRef.Scope["instrument_id"] != s.InstrumentID {
		t.Errorf("SubjectRef.Scope[instrument_id] = %q, want %q", d.SubjectRef.Scope["instrument_id"], s.InstrumentID)
	}
}

func TestMarketTimeNilWhenVenueDidNotProvide(t *testing.T) {
	s := mkScope()
	d := NewClosedDraft("evt-2", s, time.Now().UTC(), false, nil)
	if d.MarketTime != nil {
		t.Errorf("MarketTime = %v, want nil when venue did not provide it (Chapter 5 §5.2: no fabricated market_time)", d.MarketTime)
	}
}

func TestNewCorrectedDraftRequiresNonEmptyCausation(t *testing.T) {
	s := mkScope()
	ref := envelope.EventRecordRef{StreamID: "binance-candle", Sequence: 42, EventID: "evt-original"}
	d := NewCorrectedDraft("evt-3", s, time.Now().UTC(), true, nil, ref)

	if len(d.CausationRefs) != 1 || d.CausationRefs[0] != ref {
		t.Errorf("CausationRefs = %v, want exactly [%v] (candle.md §5: correction must point to fact being corrected)", d.CausationRefs, ref)
	}
	if d.EventType != EventTypeCorrected {
		t.Errorf("EventType = %q, want %q", d.EventType, EventTypeCorrected)
	}
}

func TestNewDataGapDraftIsRootEvent(t *testing.T) {
	s := mkScope()
	d := NewDataGapDraft("evt-4", s, time.Now().UTC(), nil)
	if len(d.CausationRefs) != 0 {
		t.Errorf("CandleDataGapObserved must be a root event, got CausationRefs=%v", d.CausationRefs)
	}
	if d.EventType != EventTypeDataGapObserved {
		t.Errorf("EventType = %q, want %q", d.EventType, EventTypeDataGapObserved)
	}
}

func TestContractRefPinsCorrectConceptID(t *testing.T) {
	s := mkScope()
	now := time.Now().UTC()
	cases := []struct {
		draft  envelope.Draft
		wantID string
	}{
		{NewObservedDraft("e", s, now, false, nil), ContractIDObserved},
		{NewClosedDraft("e", s, now, false, nil), ContractIDClosed},
		{NewCorrectedDraft("e", s, now, false, nil, envelope.EventRecordRef{}), ContractIDCorrected},
		{NewDataGapDraft("e", s, now, nil), ContractIDDataGapObserved},
	}
	for _, tc := range cases {
		if tc.draft.EventContractRef.ContractID != tc.wantID {
			t.Errorf("ContractID = %q, want %q", tc.draft.EventContractRef.ContractID, tc.wantID)
		}
	}
}
