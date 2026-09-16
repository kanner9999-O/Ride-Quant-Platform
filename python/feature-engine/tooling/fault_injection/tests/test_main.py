"""Dedicated, bounded tests for `tooling.fault_injection.__main__`'s
population-size-generic rollup (`_rollup`) — proves it makes no fixed-count
assumption (e.g. the historical hardcoded "five methods"), against synthetic
`FaultEvidenceRecord`s, not a live fault run.
"""

from __future__ import annotations

from tooling.fault_injection.__main__ import _rollup
from tooling.fault_injection.harness import FaultEvidenceRecord, Verdict


def _record(fault_id: str, method: str, verdict: Verdict) -> FaultEvidenceRecord:
    return FaultEvidenceRecord(
        fault_id=fault_id,
        method=method,
        source_file="src/feature_engine/irrelevant.py",
        fault_class="irrelevant",
        pinned_repository_head="deadbeef",
        old_string="irrelevant",
        new_string="irrelevant",
        verdict=verdict,
        verdict_detail="synthetic",
        isolation_path="/irrelevant",
    )


def test_rollup_handles_nine_methods_generically_when_all_qualify() -> None:
    records = [_record(f"FI-M{i}-01", f"module.Method{i}", Verdict.DETECTED) for i in range(9)]

    rollup = _rollup(records)

    assert rollup["target_method_count"] == 9
    assert rollup["fault_count"] == 9
    assert rollup["all_target_methods_have_detected_fault"] is True
    assert all(rollup["method_has_at_least_one_detected_fault"].values())
    assert "five_of_five_completion_criterion_supported" not in rollup


def test_rollup_reports_false_when_one_of_nine_methods_has_no_detected_fault() -> None:
    records = [_record(f"FI-M{i}-01", f"module.Method{i}", Verdict.DETECTED) for i in range(8)]
    records.append(_record("FI-M8-01", "module.Method8", Verdict.SURVIVED))

    rollup = _rollup(records)

    assert rollup["target_method_count"] == 9
    assert rollup["all_target_methods_have_detected_fault"] is False
    assert rollup["method_has_at_least_one_detected_fault"]["module.Method8"] is False


def test_rollup_a_method_with_multiple_faults_qualifies_on_at_least_one_detected() -> None:
    records = [
        _record("FI-M0-01", "module.Method0", Verdict.SURVIVED),
        _record("FI-M0-02", "module.Method0", Verdict.DETECTED),
    ]

    rollup = _rollup(records)

    assert rollup["target_method_count"] == 1
    assert rollup["fault_count"] == 2
    assert rollup["all_target_methods_have_detected_fault"] is True


def test_rollup_empty_population_does_not_claim_all_methods_qualify() -> None:
    rollup = _rollup([])

    assert rollup["target_method_count"] == 0
    assert rollup["all_target_methods_have_detected_fault"] is False
