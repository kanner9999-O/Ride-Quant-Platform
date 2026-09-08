"""Dedicated, bounded tests for the fault-injection harness itself
(`tooling.fault_injection`). Not part of `tests/` — deliberately outside
the governed Feature Engine mutation-testing suite, since this validates
harness infrastructure, not Feature Engine business logic. Run directly
via `pytest tooling/fault_injection/tests/`.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import tooling.fault_injection.harness as harness_module
from tooling.fault_injection.faults import FaultSpec
from tooling.fault_injection.harness import (
    QUALIFYING_VERDICTS,
    PatchNotUniqueError,
    Verdict,
    _parse_pytest_rA_output,
    apply_patch,
    classify_verdict,
    run_fault,
)

# --- apply_patch: pure patch-application logic ------------------------------


def _fault(old_string: str = "return a + b", new_string: str = "return a - b") -> FaultSpec:
    return FaultSpec(
        fault_id="FI-TEST-01",
        method="mypkg.add",
        source_file="src/mypkg/__init__.py",
        fault_class="sign_flip",
        old_string=old_string,
        new_string=new_string,
    )


def test_apply_patch_replaces_unique_match() -> None:
    content = "def add(a, b):\n    return a + b\n"
    patched = apply_patch(content, _fault())
    assert patched == "def add(a, b):\n    return a - b\n"


def test_apply_patch_raises_when_old_string_absent() -> None:
    content = "def add(a, b):\n    return a * b\n"
    with pytest.raises(PatchNotUniqueError):
        apply_patch(content, _fault())


def test_apply_patch_raises_when_old_string_not_unique() -> None:
    content = "return a + b\nreturn a + b\n"
    with pytest.raises(PatchNotUniqueError):
        apply_patch(content, _fault())


# --- _parse_pytest_rA_output: node-ID extraction from pytest's own output --


def test_parse_pytest_rA_output_extracts_passed_and_failed_node_ids() -> None:
    output = (
        ".F.\n"
        "=========================== short test summary info ===========================\n"
        "PASSED tests/test_x.py::test_one\n"
        "FAILED tests/test_x.py::test_two - AssertionError: assert False\n"
        "PASSED tests/test_x.py::test_three\n"
        "1 failed, 2 passed in 0.01s\n"
    )
    passed, failed = _parse_pytest_rA_output(output)
    assert passed == frozenset({"tests/test_x.py::test_one", "tests/test_x.py::test_three"})
    assert failed == frozenset({"tests/test_x.py::test_two"})


# --- classify_verdict: pure verdict classification --------------------------


def test_classify_verdict_detected_when_a_control_passed_test_now_fails() -> None:
    verdict, detecting = classify_verdict(
        evidence_exit_code=1,
        control_passed_node_ids=frozenset({"tests/test_x.py::test_one", "tests/test_x.py::test_two"}),
        evidence_failed_node_ids=frozenset({"tests/test_x.py::test_one"}),
    )
    assert verdict is Verdict.DETECTED
    assert detecting == ["tests/test_x.py::test_one"]


def test_classify_verdict_survived_when_no_control_passed_test_fails() -> None:
    verdict, detecting = classify_verdict(
        evidence_exit_code=0,
        control_passed_node_ids=frozenset({"tests/test_x.py::test_one"}),
        evidence_failed_node_ids=frozenset(),
    )
    assert verdict is Verdict.SURVIVED
    assert detecting == []


def test_classify_verdict_test_infra_error_on_non_ordinary_exit_code() -> None:
    verdict, detecting = classify_verdict(
        evidence_exit_code=2,
        control_passed_node_ids=frozenset({"tests/test_x.py::test_one"}),
        evidence_failed_node_ids=frozenset(),
    )
    assert verdict is Verdict.TEST_INFRA_ERROR
    assert detecting == []


# --- run_fault: full isolate/verify/control/inject/evidence/destroy cycle,
# against a throwaway, hermetic git fixture repo (never the real Feature
# Engine canonical checkout) ------------------------------------------------


def _git(args: list[str], *, cwd: Path) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), check=True, capture_output=True, text=True)


def _head_sha(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(repo_root), capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def _build_fixture_repo(tmp_path: Path) -> tuple[Path, str]:
    """A minimal, throwaway git repository mirroring just enough of
    `python/feature-engine/{src,tests,tooling}`'s own shape for `run_fault`
    to operate on — a trivial `mypkg.add` function and one test that
    covers it. Returns (repo_root, pinned_sha).
    """
    repo_root = tmp_path / "fixture-repo"
    fe = repo_root / "python" / "feature-engine"
    (fe / "src" / "mypkg").mkdir(parents=True)
    (fe / "tests").mkdir(parents=True)
    (fe / "tooling").mkdir(parents=True)
    (fe / "src" / "mypkg" / "__init__.py").write_text("def add(a, b):\n    return a + b\n")
    (fe / "tests" / "test_add.py").write_text(
        "from mypkg import add\n\n\ndef test_add() -> None:\n    assert add(1, 2) == 3\n"
    )
    (fe / "tooling" / "__init__.py").write_text("")

    _git(["init", "-q", "-b", "main"], cwd=repo_root)
    _git(["config", "user.email", "fixture@example.invalid"], cwd=repo_root)
    _git(["config", "user.name", "fixture"], cwd=repo_root)
    _git(["add", "-A"], cwd=repo_root)
    _git(["commit", "-q", "-m", "fixture repo"], cwd=repo_root)
    return repo_root, _head_sha(repo_root)


def test_run_fault_detected_when_covering_test_catches_the_fault(tmp_path: Path) -> None:
    repo_root, pinned_sha = _build_fixture_repo(tmp_path)
    work_root = tmp_path / "isolations"
    fault = _fault(old_string="return a + b", new_string="return a - b")

    record = run_fault(
        fault,
        repo_root=repo_root,
        pinned_sha=pinned_sha,
        work_root=work_root,
        python_executable=sys.executable,
    )

    assert record.verdict is Verdict.DETECTED
    assert record.detecting_test_node_ids == ["tests/test_add.py::test_add"]
    assert record.control_result == "PASS"
    assert record.activation_diff_single_hunk_single_file_confirmed is True
    assert record.isolation_destroyed_confirmed is True
    assert record.canonical_checkout_never_touched_confirmed is True
    assert not Path(record.isolation_path).exists()


def test_run_fault_survived_when_no_test_covers_the_faulted_branch(tmp_path: Path) -> None:
    repo_root, pinned_sha = _build_fixture_repo(tmp_path)
    work_root = tmp_path / "isolations"
    # `add` is never called with digits/rounding-sensitive edge cases here --
    # patch an unrelated, uncovered no-op line instead, so no existing test
    # can possibly observe the change.
    fe = repo_root / "python" / "feature-engine"
    (fe / "src" / "mypkg" / "__init__.py").write_text(
        "def add(a, b):\n    return a + b\n\n\ndef unused() -> int:\n    return 1\n"
    )
    _git(["add", "-A"], cwd=repo_root)
    _git(["commit", "-q", "-m", "add uncovered function"], cwd=repo_root)
    pinned_sha = _head_sha(repo_root)

    fault = _fault(old_string="return 1", new_string="return 2")
    record = run_fault(
        fault,
        repo_root=repo_root,
        pinned_sha=pinned_sha,
        work_root=work_root,
        python_executable=sys.executable,
    )

    assert record.verdict is Verdict.SURVIVED
    assert record.detecting_test_node_ids == []
    assert record.isolation_destroyed_confirmed is True
    assert record.canonical_checkout_never_touched_confirmed is True


def test_run_fault_injection_failed_when_old_string_absent(tmp_path: Path) -> None:
    repo_root, pinned_sha = _build_fixture_repo(tmp_path)
    work_root = tmp_path / "isolations"
    fault = _fault(old_string="this string does not exist in the source", new_string="irrelevant")

    record = run_fault(
        fault,
        repo_root=repo_root,
        pinned_sha=pinned_sha,
        work_root=work_root,
        python_executable=sys.executable,
    )

    assert record.verdict is Verdict.INJECTION_FAILED
    assert "SOURCE DRIFT" in record.verdict_detail
    assert record.canonical_checkout_never_touched_confirmed is True


# --- MAJ-01 remediation: a unique-before-patch `old_string` whose
# `new_string` is NOT uniquely located after patch (because it already
# occurs elsewhere, unrelated to the fault) must not be able to satisfy
# activation -- this is exactly the FI-OHLCV-FIELD-01/02 regression Review A
# found (a bare `count(new_string) >= 1` check was true-but-meaningless for
# both, since their replacement return statements already existed
# elsewhere). ------------------------------------------------------------


def test_run_fault_injection_failed_when_new_string_not_unique_after_patch(tmp_path: Path) -> None:
    repo_root, pinned_sha = _build_fixture_repo(tmp_path)
    work_root = tmp_path / "isolations"
    fe = repo_root / "python" / "feature-engine"
    # `old_string` ("return a + b") is unique here, but the fault's
    # `new_string` ("return a - b") already exists verbatim in an unrelated,
    # untouched function -- exactly the shape that a `>= 1` check would
    # wrongly wave through as "located".
    (fe / "src" / "mypkg" / "__init__.py").write_text(
        "def add(a, b):\n    return a + b\n\n\ndef already_present() -> int:\n    return a - b\n"
    )
    _git(["add", "-A"], cwd=repo_root)
    _git(["commit", "-q", "-m", "add pre-existing new_string collision"], cwd=repo_root)
    pinned_sha = _head_sha(repo_root)

    fault = _fault(old_string="return a + b", new_string="return a - b")
    record = run_fault(
        fault,
        repo_root=repo_root,
        pinned_sha=pinned_sha,
        work_root=work_root,
        python_executable=sys.executable,
    )

    assert record.verdict is Verdict.INJECTION_FAILED
    assert record.verdict not in QUALIFYING_VERDICTS
    assert record.activation_new_string_unique_and_located is False
    assert "new_string_located=False" in record.verdict_detail
    assert record.canonical_checkout_never_touched_confirmed is True


# --- MAJ-02 remediation: cleanup must fail closed ---------------------------


def test_run_fault_cleanup_failure_forces_test_infra_error_not_a_qualifying_verdict(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root, pinned_sha = _build_fixture_repo(tmp_path)
    work_root = tmp_path / "isolations"
    fault = _fault(old_string="return a + b", new_string="return a - b")

    real_destroy = harness_module._destroy_isolation

    def _destroy_then_report_unconfirmed(repo_root: Path, isolation_path: Path) -> bool:
        # Actually clean up the disposable worktree (so this test doesn't
        # litter tmp_path with orphaned `git worktree` state), but report
        # destruction as unconfirmed -- this is the only thing `run_fault`
        # is meant to be able to observe.
        real_destroy(repo_root, isolation_path)
        return False

    monkeypatch.setattr(harness_module, "_destroy_isolation", _destroy_then_report_unconfirmed)

    record = run_fault(
        fault,
        repo_root=repo_root,
        pinned_sha=pinned_sha,
        work_root=work_root,
        python_executable=sys.executable,
    )

    # Absent the MAJ-02 fix, this fault's covering test makes it DETECTED --
    # cleanup failure must override that, never let it stand.
    assert record.verdict is Verdict.TEST_INFRA_ERROR
    assert record.verdict not in QUALIFYING_VERDICTS
    assert record.isolation_destroyed_confirmed is False
    assert "isolation destruction could not be confirmed" in record.verdict_detail
    assert "DETECTED" in record.verdict_detail
