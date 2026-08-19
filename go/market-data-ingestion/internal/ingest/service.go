// Package ingest orchestrates market-data-ingestion's core pipeline:
// resolve venue-neutral identity + window via reference.Provider, apply
// candle.md §11's precedence algorithm to closed-or-correction facts, and
// publish the resulting canonical Candle events via publish.EventPublisher.
//
// This package never talks to a real venue: callers (a future venue
// adapter, or this transaction's demo/tests) supply already venue-adapter-
// normalized RawFact values. Building a real venue adapter is explicitly
// out of scope for this transaction (LIVE exchange connectivity is
// forbidden) — see this module's README.
package ingest

import (
	"context"
	"errors"
	"fmt"
	"sync"

	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/candle"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/envelope"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/precedence"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/publish"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/reference"
)

// ErrSessionClosed is returned when the venue's session is validly closed
// at the fact's instant (candle.md §12 case one — out of candle.md's own
// scope, see reference.ErrSessionClosed).
var ErrSessionClosed = reference.ErrSessionClosed

// RawFact is a venue-adapter-normalized observation: already venue-neutral
// (no raw exchange-specific fields, candle.md §13/§14), but not yet
// resolved to canonical instrument/venue identity or window boundaries.
type RawFact struct {
	EventID              string // caller-assigned; event_id is required on every event record (Chapter 6 §6.2)
	RawVenueID           string
	RawInstrumentSymbol  string
	Timeframe            string
	Instant              time.Time // any instant within the window this fact describes
	RecordedTime         time.Time
	OHLCV                candle.OHLCV
	NativeSourceIdentity *envelope.SourceIdentity
	// FallbackIdentityValue is used only when NativeSourceIdentity is nil
	// and the adapter has a declared deterministic fallback (candle.md §11
	// Step 1, option 2). Empty means no fallback is available.
	FallbackIdentityValue string
	// EquivalenceDeclared feeds candle.md §11 Step 5 — see
	// precedence.SourceFact.EquivalenceDeclared.
	EquivalenceDeclared bool
}

// RawClosedFact is a RawFact plus the CandleClosed-specific data_quality
// decision, which the caller must have already resolved (e.g. via the gap
// package's complete_zero_volume gate) — ingest.Service does not make that
// decision itself.
type RawClosedFact struct {
	RawFact
	DataQuality candle.DataQuality
}

// Result is the outcome of ingesting a closed-or-correction fact.
type Result struct {
	Outcome precedence.Outcome
	// Ref is the published event's record reference — valid only when
	// Outcome is OutcomeEmitFirstClosed or OutcomeEmitCorrected.
	Ref envelope.EventRecordRef
}

// Service wires reference.Provider + publish.EventPublisher into the
// candle.md pipeline.
type Service struct {
	Reference reference.Provider
	Publisher publish.EventPublisher

	mu sync.Mutex
	// lastFact indexes the last processed authoritative fact per subject
	// (candle_subject_id), used as precedence.Resolve's `existing`
	// argument. This is a local read index, not a second source of truth:
	// it is populated only from this Service's own successful publishes.
	// A real (non-single-process) implementation must rebuild this by
	// querying the authoritative event log (I-12), not by holding
	// independent mutable state — flagged in this module's README as a
	// gap this in-memory index does not solve.
	lastFact map[string]precedence.ProcessedFact
}

// NewService builds a Service.
func NewService(ref reference.Provider, pub publish.EventPublisher) *Service {
	return &Service{
		Reference: ref,
		Publisher: pub,
		lastFact:  make(map[string]precedence.ProcessedFact),
	}
}

// resolveScope resolves identity/window through the reference.Provider
// two-axis contract (ADR-032 §B.3): raw.Instant is the effective-
// applicability input, raw.RecordedTime is the knowledge-visibility
// boundary — this ingestion pipeline's own processing/recording point is
// the correct "what did we know as of when we processed this fact"
// cursor, consistent with I-3/I-5 no-look-ahead applied to the pipeline
// itself, not just to the Candle events it produces.
func (s *Service) resolveScope(ctx context.Context, raw RawFact) (candle.Scope, error) {
	id, err := s.Reference.ResolveIdentity(ctx, raw.RawVenueID, raw.RawInstrumentSymbol, raw.RecordedTime)
	if err != nil {
		return candle.Scope{}, fmt.Errorf("ingest: resolve identity: %w", err)
	}
	window, err := s.Reference.WindowFor(ctx, id.InstrumentID, id.VenueID, raw.Timeframe, raw.Instant, raw.RecordedTime)
	if err != nil {
		if errors.Is(err, reference.ErrSessionClosed) {
			return candle.Scope{}, ErrSessionClosed
		}
		return candle.Scope{}, fmt.Errorf("ingest: resolve window: %w", err)
	}
	return candle.Scope{
		InstrumentID: id.InstrumentID,
		VenueID:      id.VenueID,
		Timeframe:    raw.Timeframe,
		WindowStart:  window.Start,
		WindowEnd:    window.End,
	}, nil
}

func resolveFactIdentity(raw RawFact) precedence.Identity {
	if raw.NativeSourceIdentity != nil {
		return precedence.NativeIdentity(*raw.NativeSourceIdentity)
	}
	if raw.FallbackIdentityValue != "" {
		return precedence.FallbackIdentity(raw.FallbackIdentityValue)
	}
	return precedence.Identity{} // unresolved — precedence.Resolve fails closed (candle.md §11 Step 2)
}

// ObserveProvisional resolves identity+window and publishes a
// CandleObserved event. No precedence algorithm applies to provisional
// observations (candle.md §11 only governs closed-or-correction facts) —
// every provisional observation is appended as-is (candle.md §9).
func (s *Service) ObserveProvisional(ctx context.Context, raw RawFact) (envelope.EventRecordRef, error) {
	scope, err := s.resolveScope(ctx, raw)
	if err != nil {
		return envelope.EventRecordRef{}, err
	}
	draft := candle.NewObservedDraft(raw.EventID, scope, raw.RecordedTime, true, raw.NativeSourceIdentity)
	payload := candle.ObservedPayload{OHLCV: raw.OHLCV}
	return s.Publisher.Publish(ctx, draft, payload)
}

// IngestClosedFact applies the candle.md §11 5-step precedence algorithm to
// an incoming closed-or-correction source fact and publishes the correct
// event: CandleClosed for a subject's first authoritative close, or
// CandleCorrected per Step 4. Duplicate (Steps 3/5) and fail-closed
// (Steps 2/3/5) outcomes publish nothing.
func (s *Service) IngestClosedFact(ctx context.Context, raw RawClosedFact) (Result, error) {
	scope, err := s.resolveScope(ctx, raw.RawFact)
	if err != nil {
		return Result{}, err
	}

	payload := candle.ClosedPayload{OHLCV: raw.OHLCV, DataQuality: raw.DataQuality}
	fact := precedence.SourceFact{
		Identity:            resolveFactIdentity(raw.RawFact),
		Payload:             payload,
		EquivalenceDeclared: raw.EquivalenceDeclared,
	}

	subjectID := scope.SubjectID()

	s.mu.Lock()
	existing, hasExisting := s.lastFact[subjectID]
	s.mu.Unlock()

	var existingPtr *precedence.ProcessedFact
	if hasExisting {
		existingPtr = &existing
	}

	decision := precedence.Resolve(fact, existingPtr)

	switch decision.Outcome {
	case precedence.OutcomeEmitFirstClosed:
		draft := candle.NewClosedDraft(raw.EventID, scope, raw.RecordedTime, true, raw.NativeSourceIdentity)
		ref, err := s.Publisher.Publish(ctx, draft, payload)
		if err != nil {
			return Result{}, err
		}
		s.recordProcessed(subjectID, fact, ref)
		return Result{Outcome: decision.Outcome, Ref: ref}, nil

	case precedence.OutcomeEmitCorrected:
		draft := candle.NewCorrectedDraft(raw.EventID, scope, raw.RecordedTime, true, raw.NativeSourceIdentity, decision.CorrectingRef)
		correctedPayload := candle.CorrectedPayload{OHLCV: raw.OHLCV}
		ref, err := s.Publisher.Publish(ctx, draft, correctedPayload)
		if err != nil {
			return Result{}, err
		}
		s.recordProcessed(subjectID, fact, ref)
		return Result{Outcome: decision.Outcome, Ref: ref}, nil

	case precedence.OutcomeDuplicateZeroEffect, precedence.OutcomeFailClosed:
		return Result{Outcome: decision.Outcome}, nil

	default:
		return Result{}, fmt.Errorf("ingest: unhandled precedence outcome %v", decision.Outcome)
	}
}

func (s *Service) recordProcessed(subjectID string, fact precedence.SourceFact, ref envelope.EventRecordRef) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.lastFact[subjectID] = precedence.ProcessedFact{
		Identity:         fact.Identity,
		Payload:          fact.Payload,
		AuthoritativeRef: ref,
	}
}

// ReportDataGap publishes a CandleDataGapObserved signal for a window
// ingestion could not resolve (candle.md §12 case three). scope must
// already be resolved by the caller (typically via resolveScope through a
// prior failed IngestClosedFact/ObserveProvisional call, or directly known).
func (s *Service) ReportDataGap(ctx context.Context, eventID string, scope candle.Scope, recordedTime time.Time, reason candle.GapReason) (envelope.EventRecordRef, error) {
	draft := candle.NewDataGapDraft(eventID, scope, recordedTime, nil)
	payload := candle.DataGapPayload{Reason: reason}
	return s.Publisher.Publish(ctx, draft, payload)
}
