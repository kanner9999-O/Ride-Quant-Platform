package fact

import "testing"

func TestResolveNoFactsYet(t *testing.T) {
	out := Resolve(ResolveInput{InitialStatus: "REGISTERED", IsValidTransition: instrumentTransitions, EffectiveCursor: t0(100), KnowledgeCursor: t0(100)})
	if out.ViewState != ViewPendingCorrection || out.PendingClass != PendingCorrectionNone {
		t.Fatalf("got %+v, want no-facts-yet zero result", out)
	}
}

func TestResolveValidWithMetadataAndStatus(t *testing.T) {
	in := ResolveInput{
		RegistrationFacts: []LineageFact{{Ref: ref("r1"), RecordedTime: t0(0)}},
		MetadataBase:      map[string]string{"display_name": "Base"},
		MetadataPatches: []MetadataPatch{
			{LineageFact: LineageFact{Ref: ref("m1"), RecordedTime: t0(1)}, EffectiveTime: t0(5), ChangedFields: map[string]string{"display_name": "Patched"}},
		},
		StatusChanges: []StatusChange{
			{LineageFact: LineageFact{Ref: ref("s1"), RecordedTime: t0(1)}, EffectiveTime: t0(2), NewStatus: "ACTIVE"},
		},
		InitialStatus:     "REGISTERED",
		IsValidTransition: instrumentTransitions,
		EffectiveCursor:   t0(10),
		KnowledgeCursor:   t0(10),
	}
	out := Resolve(in)
	if out.ViewState != ViewValid {
		t.Fatalf("got ViewState=%v, want ViewValid", out.ViewState)
	}
	if out.RegistrationHead != ref("r1") {
		t.Fatalf("got RegistrationHead=%v, want r1", out.RegistrationHead)
	}
	if out.Fields["display_name"] != "Patched" {
		t.Fatalf("got display_name=%q, want Patched", out.Fields["display_name"])
	}
	if out.CurrentStatus != "ACTIVE" {
		t.Fatalf("got CurrentStatus=%q, want ACTIVE", out.CurrentStatus)
	}
}

func TestResolveRegistrationPendingShortCircuits(t *testing.T) {
	in := ResolveInput{
		RegistrationFacts:         []LineageFact{{Ref: ref("r1"), RecordedTime: t0(0)}},
		RegistrationInvalidations: []Invalidation{{Ref: ref("i1"), RecordedTime: t0(1), InvalidatedRef: ref("r1"), CorrectionClass: CorrectionClassScopeError}},
		InitialStatus:             "REGISTERED",
		IsValidTransition:         instrumentTransitions,
		EffectiveCursor:           t0(10),
		KnowledgeCursor:           t0(10),
	}
	out := Resolve(in)
	if out.ViewState != ViewPendingCorrection || out.PendingClass != TerminalScopeInvalidation {
		t.Fatalf("got %+v, want PENDING_CORRECTION/TerminalScopeInvalidation", out)
	}
}
