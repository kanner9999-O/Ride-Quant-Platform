package candle

import (
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/decimal"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/envelope"
)

// Event types (candle.md §2 event_types — PAST_TENSE_UPPER_SNAKE per
// Chapter 3 §3.2).
const (
	EventTypeObserved        = "CANDLE_OBSERVED"
	EventTypeClosed          = "CANDLE_CLOSED"
	EventTypeCorrected       = "CANDLE_CORRECTED"
	EventTypeDataGapObserved = "CANDLE_DATA_GAP_OBSERVED"
)

// Contract concept IDs (candle.md §0: "canonical contract concept ID —
// đúng giá trị id: khai báo trong từng khối YAML"). Used as
// envelope.ContractRef.ContractID.
const (
	ContractIDObserved        = "candle-observed"
	ContractIDClosed          = "candle-closed"
	ContractIDCorrected       = "candle-corrected"
	ContractIDDataGapObserved = "candle-data-gap-observed"
)

// contractVersion pins the candle.md document version this implementation
// was built against. candle.md does not (yet) version each event concept
// independently — using the document version as ContractVersion is an
// implementation-level mapping made at this build transaction, not an
// architecture decision: candle.md is Draft/unapproved, so this pin must be
// revisited if/when candle.md is Approved and per-event contract
// versioning is established.
const contractVersion = "0.4"

// payloadSchemaVersion is this package's payload schema_version (Chapter 8
// §8.2.5) — independent of contractVersion.
const payloadSchemaVersion = 1

// DataQuality is CandleClosed's payload.data_quality (candle.md §4).
type DataQuality string

const (
	DataQualityComplete           DataQuality = "complete"
	DataQualityCompleteZeroVolume DataQuality = "complete_zero_volume"
)

// GapReason is CandleDataGapObserved's payload.reason (candle.md §6).
type GapReason string

const (
	GapReasonSourceUnavailable      GapReason = "source_unavailable"
	GapReasonDelayedBeyondThreshold GapReason = "delayed_beyond_threshold"
	GapReasonUnknown                GapReason = "unknown"
)

// OHLCV is the OHLCV payload shared by Observed/Closed/Corrected
// (candle.md §3-§5).
type OHLCV struct {
	Open   decimal.Decimal
	High   decimal.Decimal
	Low    decimal.Decimal
	Close  decimal.Decimal
	Volume decimal.Decimal
}

// ObservedPayload is CandleObserved's payload (candle.md §3).
type ObservedPayload struct {
	OHLCV
}

// ClosedPayload is CandleClosed's payload (candle.md §4).
type ClosedPayload struct {
	OHLCV
	DataQuality DataQuality
}

// CorrectedPayload is CandleCorrected's payload (candle.md §5).
type CorrectedPayload struct {
	OHLCV
	CorrectionReason string // optional
}

// DataGapPayload is CandleDataGapObserved's payload (candle.md §6).
// It deliberately carries no OHLC fields (candle.md §6 invariant).
type DataGapPayload struct {
	Reason GapReason
}

func subjectRef(s Scope) envelope.SubjectRef {
	return envelope.SubjectRef{
		ContextID:   "market-data-observation",
		SubjectKind: "entity",
		SubjectType: "Candle",
		SubjectID:   s.SubjectID(),
		Scope: map[string]string{
			"instrument_id": s.InstrumentID,
			"venue_id":      s.VenueID,
			"timeframe":     s.Timeframe,
			"window_start":  s.WindowStart.UTC().Format(time.RFC3339Nano),
			"window_end":    s.WindowEnd.UTC().Format(time.RFC3339Nano),
		},
	}
}

func effectiveTime(s Scope) *envelope.EffectiveTime {
	return &envelope.EffectiveTime{WindowStart: s.WindowStart, WindowEnd: s.WindowEnd}
}

// marketTime returns window_start as market_time, per candle.md §8:
// "market_time = window_start khi có". venueProvided indicates whether the
// venue actually supplied a market timestamp for this observation — when
// false, envelope.market_time is left nil per Chapter 5 §5.2 ("không tạo
// market_time giả").
func marketTime(s Scope, venueProvided bool) *time.Time {
	if !venueProvided {
		return nil
	}
	t := s.WindowStart
	return &t
}

func baseDraft(eventID, eventType, contractID string, s Scope, recordedTime time.Time, venueProvidedMarketTime bool, sourceIdentity *envelope.SourceIdentity) envelope.Draft {
	return envelope.Draft{
		EventID:   eventID,
		EventType: eventType,
		EventContractRef: envelope.ContractRef{
			ContractID:      contractID,
			ContractVersion: contractVersion,
		},
		SchemaVersion:    payloadSchemaVersion,
		RecordedTime:     recordedTime,
		SubjectRef:       subjectRef(s),
		CausationRefs:    []envelope.EventRecordRef{}, // root event (candle.md §2/§3/§4/§6)
		RelatedEventRefs: []envelope.EventRecordRef{},
		EffectiveTime:    effectiveTime(s),
		MarketTime:       marketTime(s, venueProvidedMarketTime),
		SourceIdentity:   sourceIdentity,
	}
}

// NewObservedDraft builds the envelope.Draft for a CandleObserved event.
// causation_refs is [] (root event, candle.md §3).
func NewObservedDraft(eventID string, s Scope, recordedTime time.Time, venueProvidedMarketTime bool, sourceIdentity *envelope.SourceIdentity) envelope.Draft {
	return baseDraft(eventID, EventTypeObserved, ContractIDObserved, s, recordedTime, venueProvidedMarketTime, sourceIdentity)
}

// NewClosedDraft builds the envelope.Draft for a CandleClosed event.
// causation_refs is [] (root event, candle.md §4 — a second non-identical
// closed fact for the same subject must go through CandleCorrected instead,
// see internal/precedence).
func NewClosedDraft(eventID string, s Scope, recordedTime time.Time, venueProvidedMarketTime bool, sourceIdentity *envelope.SourceIdentity) envelope.Draft {
	return baseDraft(eventID, EventTypeClosed, ContractIDClosed, s, recordedTime, venueProvidedMarketTime, sourceIdentity)
}

// NewCorrectedDraft builds the envelope.Draft for a CandleCorrected event.
// causation_refs MUST be non-empty and point to the fact being corrected
// (candle.md §5 invariant) — enforced by the caller supplying correcting.
func NewCorrectedDraft(eventID string, s Scope, recordedTime time.Time, venueProvidedMarketTime bool, sourceIdentity *envelope.SourceIdentity, correcting envelope.EventRecordRef) envelope.Draft {
	d := baseDraft(eventID, EventTypeCorrected, ContractIDCorrected, s, recordedTime, venueProvidedMarketTime, sourceIdentity)
	d.CausationRefs = []envelope.EventRecordRef{correcting}
	return d
}

// NewDataGapDraft builds the envelope.Draft for a CandleDataGapObserved
// event. causation_refs is [] (root event, candle.md §6).
func NewDataGapDraft(eventID string, s Scope, recordedTime time.Time, sourceIdentity *envelope.SourceIdentity) envelope.Draft {
	return baseDraft(eventID, EventTypeDataGapObserved, ContractIDDataGapObserved, s, recordedTime, false, sourceIdentity)
}
