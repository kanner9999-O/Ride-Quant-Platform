// Package decimal implements a lossless, arbitrary-precision decimal type.
//
// Constitution I-9 (Numerical Precision) requires that financial values
// (price, quantity, volume) never round-trip through float64 at any step,
// including deserialization. This package parses decimal values directly
// from their lossless string representation into a scaled-integer form
// (unscaled *big.Int, scale int) and never converts through float64.
package decimal

import (
	"fmt"
	"math/big"
	"strings"
)

// Decimal is an immutable arbitrary-precision decimal number, represented
// as unscaled * 10^(-scale). It is never backed by float32/float64.
type Decimal struct {
	unscaled *big.Int
	scale    int32
}

// Zero is the additive identity.
var Zero = Decimal{unscaled: big.NewInt(0), scale: 0}

// NewFromString parses a decimal literal (e.g. "65432.10", "-0.001", "100")
// directly from its digit string — no float conversion at any step.
func NewFromString(s string) (Decimal, error) {
	orig := s
	neg := false
	if strings.HasPrefix(s, "-") {
		neg = true
		s = s[1:]
	} else if strings.HasPrefix(s, "+") {
		s = s[1:]
	}
	if s == "" {
		return Decimal{}, fmt.Errorf("decimal: empty value in %q", orig)
	}

	intPart, fracPart, hasFrac := strings.Cut(s, ".")
	if intPart == "" {
		intPart = "0"
	}
	if !isDigits(intPart) || (hasFrac && !isDigits(fracPart)) || (hasFrac && fracPart == "") {
		return Decimal{}, fmt.Errorf("decimal: invalid literal %q", orig)
	}

	digits := intPart + fracPart
	unscaled, ok := new(big.Int).SetString(digits, 10)
	if !ok {
		return Decimal{}, fmt.Errorf("decimal: invalid literal %q", orig)
	}
	if neg {
		unscaled.Neg(unscaled)
	}

	return Decimal{unscaled: unscaled, scale: int32(len(fracPart))}, nil
}

// MustFromString is NewFromString, panicking on error. Intended for
// literals fixed at compile time (tests, constants) — never for parsing
// externally supplied/untrusted data.
func MustFromString(s string) Decimal {
	d, err := NewFromString(s)
	if err != nil {
		panic(err)
	}
	return d
}

func isDigits(s string) bool {
	for _, r := range s {
		if r < '0' || r > '9' {
			return false
		}
	}
	return true
}

func (d Decimal) rescale(scale int32) Decimal {
	if d.scale == scale {
		return d
	}
	diff := scale - d.scale
	factor := new(big.Int).Exp(big.NewInt(10), big.NewInt(int64(absInt32(diff))), nil)
	u := new(big.Int)
	if diff > 0 {
		u.Mul(d.unscaled, factor)
	} else {
		u.Quo(d.unscaled, factor)
	}
	return Decimal{unscaled: u, scale: scale}
}

func absInt32(v int32) int32 {
	if v < 0 {
		return -v
	}
	return v
}

func maxScale(a, b Decimal) int32 {
	if a.scale > b.scale {
		return a.scale
	}
	return b.scale
}

// Add returns d + other.
func (d Decimal) Add(other Decimal) Decimal {
	scale := maxScale(d, other)
	a, b := d.rescale(scale), other.rescale(scale)
	return Decimal{unscaled: new(big.Int).Add(a.unscaled, b.unscaled), scale: scale}
}

// Sub returns d - other.
func (d Decimal) Sub(other Decimal) Decimal {
	scale := maxScale(d, other)
	a, b := d.rescale(scale), other.rescale(scale)
	return Decimal{unscaled: new(big.Int).Sub(a.unscaled, b.unscaled), scale: scale}
}

// Cmp returns -1, 0, or 1 as d is less than, equal to, or greater than other.
func (d Decimal) Cmp(other Decimal) int {
	scale := maxScale(d, other)
	a, b := d.rescale(scale), other.rescale(scale)
	return a.unscaled.Cmp(b.unscaled)
}

// Equal reports whether d and other represent the same numeric value,
// regardless of trailing-zero scale differences (e.g. "1.50" == "1.5").
func (d Decimal) Equal(other Decimal) bool {
	return d.Cmp(other) == 0
}

// IsZero reports whether d represents the value zero.
func (d Decimal) IsZero() bool {
	return d.unscaled.Sign() == 0
}

// Sign returns -1, 0, or 1 for negative, zero, or positive d.
func (d Decimal) Sign() int {
	return d.unscaled.Sign()
}

// String renders the canonical lossless decimal representation.
func (d Decimal) String() string {
	if d.scale <= 0 {
		return d.rescale(0).unscaled.String()
	}
	neg := d.unscaled.Sign() < 0
	digits := new(big.Int).Abs(d.unscaled).String()
	for int32(len(digits)) <= d.scale {
		digits = "0" + digits
	}
	cut := int32(len(digits)) - d.scale
	intPart, fracPart := digits[:cut], digits[cut:]
	out := intPart + "." + fracPart
	if neg {
		out = "-" + out
	}
	return out
}

// MarshalText implements encoding.TextMarshaler using the lossless decimal
// string form — never float64 — so JSON/text encoding never round-trips
// through float (I-9).
func (d Decimal) MarshalText() ([]byte, error) {
	return []byte(d.String()), nil
}

// UnmarshalText implements encoding.TextUnmarshaler, parsing directly from
// the decimal string form — never float64.
func (d *Decimal) UnmarshalText(text []byte) error {
	parsed, err := NewFromString(string(text))
	if err != nil {
		return err
	}
	*d = parsed
	return nil
}
