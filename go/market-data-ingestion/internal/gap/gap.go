// Package gap implements candle.md §12's missing-data handling: the strict
// five-condition provenance gate for CandleClosed.payload.data_quality =
// complete_zero_volume, and the CandleDataGapObserved reason mapping for
// the "missing/delayed/unavailable" case.
//
// candle.md §12 distinguishes three cases. This package only decides
// between the last two — session-open-no-trade (complete_zero_volume) and
// missing/delayed/unavailable (gap) — because the first case (valid
// session close) is explicitly out of candle.md's scope, answered by the
// Venue/session authority in the instrument-venue-reference context, whose
// Domain Contract has not been authored yet (see the market-reference-
// service deferral note in this module's README). Whether a given window
// even needs this package's evaluation at all — i.e. whether the session
// was open — is a decision this module cannot make on its own until that
// authority exists.
//
// This package never synthesizes OHLC values for a missing window: there
// is no function anywhere in this package (or the rest of this module)
// that fabricates open/high/low/close/volume from absence of data — that
// prohibition (candle.md §12, "Cấm tự tổng hợp OHLC giả") is enforced by
// this design, not by a runtime check.
package gap

import (
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/candle"
)

// ZeroVolumeAssertion carries the evidence needed to evaluate candle.md
// §12's five mandatory provenance conditions for
// data_quality: complete_zero_volume. Missing any one condition means the
// window MUST be treated as the gap case instead (candle.md §12: "thiếu
// bất kỳ điều kiện nào thì KHÔNG hợp lệ, phải xử lý như case thứ ba").
type ZeroVolumeAssertion struct {
	// SourceConfirmedZeroVolumeClose is condition 1: the authoritative
	// source/producer explicitly confirmed a completed zero-volume candle
	// — never inferred from silence.
	SourceConfirmedZeroVolumeClose bool
	// ProducerRefResolved is condition 2: envelope.producer_ref resolves
	// to the producer that made the confirmation in condition 1.
	ProducerRefResolved bool
	// ContractAllowsZeroVolume is condition 3: envelope.event_contract_ref
	// resolves to an Event Contract that permits the complete_zero_volume
	// semantic (not every CandleClosed Event Contract allows it).
	ContractAllowsZeroVolume bool
	// SourceIdentityPresentIfRetryable is condition 4: source_identity is
	// present whenever the source is capable of retry/redelivery.
	SourceIdentityPresentIfRetryable bool
	// InferredFromSilenceOnly is condition 5's violation flag: true means
	// the adapter would be inferring complete_zero_volume purely from the
	// absence of trade/message activity, which candle.md §12 explicitly
	// forbids as sufficient evidence. Must be false for the assertion to
	// satisfy the gate.
	InferredFromSilenceOnly bool
}

// Satisfied reports whether all five candle.md §12 provenance conditions
// hold.
func (a ZeroVolumeAssertion) Satisfied() bool {
	return a.SourceConfirmedZeroVolumeClose &&
		a.ProducerRefResolved &&
		a.ContractAllowsZeroVolume &&
		a.SourceIdentityPresentIfRetryable &&
		!a.InferredFromSilenceOnly
}

// ResolveClosedDataQuality applies the candle.md §12 gate. When the
// assertion is not fully satisfied, ok is false — the caller MUST NOT
// synthesize a CandleClosed for this window and must instead treat it as
// the gap case (candle.md §12 case three).
func ResolveClosedDataQuality(assertion ZeroVolumeAssertion) (quality candle.DataQuality, ok bool) {
	if assertion.Satisfied() {
		return candle.DataQualityCompleteZeroVolume, true
	}
	return "", false
}

// DelayEvaluator decides whether an observed data delay exceeds the
// configured threshold. The threshold VALUE itself is explicitly deferred
// by candle.md §17 ("ngưỡng delayed_beyond_threshold") to Engineering
// Foundation/Phase 1 — it is supplied here as external configuration
// (config.md §1: externally-supplied operational setting), never
// hardcoded.
type DelayEvaluator struct {
	Threshold time.Duration
}

// IsDelayedBeyondThreshold reports whether observedDelay exceeds the
// configured threshold.
func (e DelayEvaluator) IsDelayedBeyondThreshold(observedDelay time.Duration) bool {
	return observedDelay > e.Threshold
}

// ResolveGapReason maps ingestion-observed conditions to the candle.md §6
// GapReason enum for CandleDataGapObserved. delayEvaluator may be nil when
// no threshold has been configured, in which case a non-unavailable delay
// resolves to GapReasonUnknown rather than guessing at a threshold.
func ResolveGapReason(sourceUnavailable bool, delayEvaluator *DelayEvaluator, observedDelay time.Duration) candle.GapReason {
	if sourceUnavailable {
		return candle.GapReasonSourceUnavailable
	}
	if delayEvaluator != nil && delayEvaluator.IsDelayedBeyondThreshold(observedDelay) {
		return candle.GapReasonDelayedBeyondThreshold
	}
	return candle.GapReasonUnknown
}
