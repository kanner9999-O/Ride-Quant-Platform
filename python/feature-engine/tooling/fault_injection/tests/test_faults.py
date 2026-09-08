"""Validates that every entry in `faults.APPROVED_FAULTS` satisfies the
activation uniqueness contract (`feature-engine-mutation-surface-
completeness-design-001.md` §2.1a) against this repository's own real,
current source files -- not a synthetic fixture.

This is the direct MAJ-01 regression guard: FI-OHLCV-FIELD-01 and
FI-OHLCV-FIELD-02 both had an `old_string` that was unique before patch but
a `new_string` that collided with an already-present, unrelated occurrence
after patch -- a `count(new_string) >= 1` check waved this through as
"located" even though it wasn't unique. `apply_patch` + a strict
`== 1` check is the approved contract; this test proves the approved
population actually meets it, for every fault, not just the two OHLCV
ones.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tooling.fault_injection.faults import APPROVED_FAULTS, FaultSpec
from tooling.fault_injection.harness import apply_patch

_FEATURE_ENGINE_ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.parametrize("fault", APPROVED_FAULTS, ids=lambda f: f.fault_id)
def test_approved_fault_new_string_uniquely_located_after_patch(fault: FaultSpec) -> None:
    source_path = _FEATURE_ENGINE_ROOT / fault.source_file
    content = source_path.read_text()

    assert content.count(fault.old_string) == 1, (
        f"{fault.fault_id}: old_string is not unique in the current {fault.source_file}"
    )

    patched = apply_patch(content, fault)

    assert patched.count(fault.new_string) == 1, (
        f"{fault.fault_id}: new_string is not uniquely located after patch -- "
        "this fault would false-to-label as activated under a `>= 1` check "
        "(the exact MAJ-01 regression); the approved uniqueness contract requires `== 1`"
    )
