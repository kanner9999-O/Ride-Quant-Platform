package decimal

import "testing"

func TestNewFromString(t *testing.T) {
	cases := []struct {
		name    string
		input   string
		want    string
		wantErr bool
	}{
		{name: "integer", input: "100", want: "100"},
		{name: "simple decimal", input: "65432.10", want: "65432.10"},
		{name: "negative", input: "-0.001", want: "-0.001"},
		{name: "explicit positive", input: "+42", want: "42"},
		{name: "leading dot", input: ".5", want: "0.5"},
		{name: "empty", input: "", wantErr: true},
		{name: "trailing dot", input: "5.", wantErr: true},
		{name: "not digits", input: "12a.3", wantErr: true},
		{name: "float classic trap", input: "0.1", want: "0.1"},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			got, err := NewFromString(tc.input)
			if tc.wantErr {
				if err == nil {
					t.Fatalf("NewFromString(%q) = %v, want error", tc.input, got)
				}
				return
			}
			if err != nil {
				t.Fatalf("NewFromString(%q) unexpected error: %v", tc.input, err)
			}
			if got.String() != tc.want {
				t.Errorf("NewFromString(%q).String() = %q, want %q", tc.input, got.String(), tc.want)
			}
		})
	}
}

func TestAddNoFloatRoundTrip(t *testing.T) {
	// The classic float trap: 0.1 + 0.2 != 0.3 in float64.
	a := MustFromString("0.1")
	b := MustFromString("0.2")
	got := a.Add(b)
	want := MustFromString("0.3")
	if !got.Equal(want) {
		t.Fatalf("0.1 + 0.2 = %s, want %s", got.String(), want.String())
	}
	if got.String() != "0.3" {
		t.Fatalf("0.1 + 0.2 String() = %q, want %q", got.String(), "0.3")
	}
}

func TestSub(t *testing.T) {
	a := MustFromString("10.5")
	b := MustFromString("3.25")
	got := a.Sub(b)
	if got.String() != "7.25" {
		t.Fatalf("10.5 - 3.25 = %s, want 7.25", got.String())
	}
}

func TestCmpAndEqual(t *testing.T) {
	a := MustFromString("1.50")
	b := MustFromString("1.5")
	if !a.Equal(b) {
		t.Fatalf("expected 1.50 == 1.5")
	}
	if a.Cmp(b) != 0 {
		t.Fatalf("expected Cmp(1.50, 1.5) == 0")
	}
	c := MustFromString("1.51")
	if a.Cmp(c) >= 0 {
		t.Fatalf("expected 1.50 < 1.51")
	}
	if c.Cmp(a) <= 0 {
		t.Fatalf("expected 1.51 > 1.50")
	}
}

func TestIsZeroAndSign(t *testing.T) {
	if !Zero.IsZero() {
		t.Fatalf("Zero.IsZero() = false")
	}
	if MustFromString("0.00").Sign() != 0 {
		t.Fatalf("expected sign 0 for 0.00")
	}
	if MustFromString("-5").Sign() != -1 {
		t.Fatalf("expected sign -1 for -5")
	}
	if MustFromString("5").Sign() != 1 {
		t.Fatalf("expected sign 1 for 5")
	}
}

func TestMarshalUnmarshalText(t *testing.T) {
	d := MustFromString("42.1234")
	text, err := d.MarshalText()
	if err != nil {
		t.Fatalf("MarshalText error: %v", err)
	}
	if string(text) != "42.1234" {
		t.Fatalf("MarshalText() = %q, want %q", text, "42.1234")
	}
	var round Decimal
	if err := round.UnmarshalText(text); err != nil {
		t.Fatalf("UnmarshalText error: %v", err)
	}
	if !round.Equal(d) {
		t.Fatalf("round-trip mismatch: got %s, want %s", round.String(), d.String())
	}
}
