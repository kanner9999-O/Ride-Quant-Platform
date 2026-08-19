package gap

import (
	"testing"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/candle"
)

func fullAssertion() ZeroVolumeAssertion {
	return ZeroVolumeAssertion{
		SourceConfirmedZeroVolumeClose:   true,
		ProducerRefResolved:              true,
		ContractAllowsZeroVolume:         true,
		SourceIdentityPresentIfRetryable: true,
		InferredFromSilenceOnly:          false,
	}
}

func TestResolveClosedDataQualityAllConditionsMet(t *testing.T) {
	quality, ok := ResolveClosedDataQuality(fullAssertion())
	if !ok {
		t.Fatalf("expected ok=true when all five conditions hold")
	}
	if quality != candle.DataQualityCompleteZeroVolume {
		t.Errorf("quality = %q, want %q", quality, candle.DataQualityCompleteZeroVolume)
	}
}

func TestResolveClosedDataQualityMissingAnyConditionFails(t *testing.T) {
	base := fullAssertion()
	mutate := []func(*ZeroVolumeAssertion){
		func(a *ZeroVolumeAssertion) { a.SourceConfirmedZeroVolumeClose = false },
		func(a *ZeroVolumeAssertion) { a.ProducerRefResolved = false },
		func(a *ZeroVolumeAssertion) { a.ContractAllowsZeroVolume = false },
		func(a *ZeroVolumeAssertion) { a.SourceIdentityPresentIfRetryable = false },
		func(a *ZeroVolumeAssertion) { a.InferredFromSilenceOnly = true },
	}
	for i, m := range mutate {
		a := base
		m(&a)
		_, ok := ResolveClosedDataQuality(a)
		if ok {
			t.Errorf("mutation %d: expected ok=false when a required condition is unmet, assertion=%+v", i, a)
		}
	}
}

func TestResolveClosedDataQualitySilenceInferenceAloneIsInsufficient(t *testing.T) {
	// candle.md §12 condition 5: silence alone must never be sufficient,
	// even if the other four conditions somehow appear satisfied.
	a := fullAssertion()
	a.InferredFromSilenceOnly = true
	_, ok := ResolveClosedDataQuality(a)
	if ok {
		t.Fatalf("expected ok=false when InferredFromSilenceOnly=true regardless of other conditions")
	}
}

func TestResolveGapReasonSourceUnavailable(t *testing.T) {
	got := ResolveGapReason(true, nil, 0)
	if got != candle.GapReasonSourceUnavailable {
		t.Errorf("got %q, want %q", got, candle.GapReasonSourceUnavailable)
	}
}

func TestResolveGapReasonDelayedBeyondThreshold(t *testing.T) {
	eval := &DelayEvaluator{Threshold: 5 * time.Second}
	got := ResolveGapReason(false, eval, 10*time.Second)
	if got != candle.GapReasonDelayedBeyondThreshold {
		t.Errorf("got %q, want %q", got, candle.GapReasonDelayedBeyondThreshold)
	}
}

func TestResolveGapReasonWithinThresholdIsUnknown(t *testing.T) {
	eval := &DelayEvaluator{Threshold: 5 * time.Second}
	got := ResolveGapReason(false, eval, 1*time.Second)
	if got != candle.GapReasonUnknown {
		t.Errorf("got %q, want %q", got, candle.GapReasonUnknown)
	}
}

func TestResolveGapReasonNoEvaluatorConfiguredIsUnknown(t *testing.T) {
	got := ResolveGapReason(false, nil, 100*time.Second)
	if got != candle.GapReasonUnknown {
		t.Errorf("got %q, want %q — must not guess a threshold when none is configured", got, candle.GapReasonUnknown)
	}
}
