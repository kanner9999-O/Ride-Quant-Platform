"""The isolated-checkout fault-injection harness itself.

Implements the exact sequence approved in `feature-engine-mutation-
surface-completeness-design-001.md` §2.1/§2.1a, for one fault at a time:

    create isolation -> verify identities -> clean control -> apply one
    fault -> prove activation -> evidence run -> classify verdict ->
    destroy isolation.

The canonical checkout (the git working tree this module itself lives in)
is never entered, read for mutation purposes, or written to — every fault
is applied inside its own disposable `git worktree` checkout, created
fresh and destroyed unconditionally regardless of verdict.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from tooling.fault_injection.faults import FaultSpec

_FEATURE_ENGINE_RELPATH = "python/feature-engine"
_TEST_COMMAND_ARGS = ("tests/", "-q", "-rA", "--tb=line", "--no-header")
_TEST_COMMAND_DISPLAY = "pytest tests/ -q"
_SUBPROCESS_TIMEOUT_SECONDS = 300


class Verdict(StrEnum):
    CONTROL_FAILED = "CONTROL_FAILED"
    INJECTION_FAILED = "INJECTION_FAILED"
    TEST_INFRA_ERROR = "TEST_INFRA_ERROR"
    SURVIVED = "SURVIVED"
    DETECTED = "DETECTED"


QUALIFYING_VERDICTS = frozenset({Verdict.DETECTED, Verdict.SURVIVED})


class PatchNotUniqueError(Exception):
    """`old_string` was not found exactly once in the target file."""


class IsolationError(Exception):
    """Isolated checkout creation, identity verification, or destruction failed."""


@dataclass(frozen=True, slots=True)
class TestRunResult:
    exit_code: int
    passed_node_ids: frozenset[str]
    failed_node_ids: frozenset[str]
    raw_output: str
    timed_out: bool = False


@dataclass(slots=True)
class FaultEvidenceRecord:
    fault_id: str
    method: str
    source_file: str
    fault_class: str
    pinned_repository_head: str
    old_string: str
    new_string: str
    verdict: Verdict
    verdict_detail: str
    isolation_path: str
    isolation_head_verified: str | None = None
    isolation_src_tree_verified: str | None = None
    isolation_tests_tree_verified: str | None = None
    isolation_tooling_tree_verified: str | None = None
    expected_src_tree: str | None = None
    expected_tests_tree: str | None = None
    expected_tooling_tree: str | None = None
    control_test_command: str = _TEST_COMMAND_DISPLAY
    control_test_command_actual: str = ""
    control_result: str = ""
    control_exit_code: int | None = None
    control_passed_node_id_count: int | None = None
    activation_new_string_unique_and_located: bool = False
    activation_expected_patched_file_sha256: str | None = None
    activation_observed_patched_file_sha256: str | None = None
    activation_diff_files_changed: int | None = None
    activation_diff_hunks_in_target_file: int | None = None
    activation_diff_single_hunk_single_file_confirmed: bool = False
    evidence_test_command: str = _TEST_COMMAND_DISPLAY
    evidence_test_command_actual: str = ""
    evidence_exit_code: int | None = None
    detecting_test_node_ids: list[str] = field(default_factory=list)
    isolation_destroyed_confirmed: bool = False
    canonical_checkout_never_touched_confirmed: bool = False


def _git(args: list[str], *, cwd: Path, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def _canonical_repo_status_snapshot(repo_root: Path) -> str:
    """A cheap, sufficient fingerprint of the canonical checkout's own
    working-tree state — used as a before/after defense-in-depth check
    that this harness never left the canonical tree modified. `git
    worktree add`/`remove` only touch `.git/worktrees/` administrative
    metadata, never tracked working-tree files, so this is expected to be
    byte-identical across a fault's entire isolate/inject/destroy cycle.
    """
    status = _git(["status", "--porcelain"], cwd=repo_root)
    diff = _git(["diff"], cwd=repo_root)
    return f"status={status.stdout!r}\ndiff={diff.stdout!r}"


def _parse_pytest_rA_output(output: str) -> tuple[frozenset[str], frozenset[str]]:
    """Parses `pytest -rA`'s short-summary lines (`PASSED <node_id>`,
    `FAILED <node_id> - <reason>`) into exact node-ID sets — no reliance on
    any reconstructed/derived node-ID format, only pytest's own literal
    output.
    """
    passed: set[str] = set()
    failed: set[str] = set()
    for line in output.splitlines():
        if line.startswith("PASSED "):
            passed.add(line[len("PASSED ") :].strip())
        elif line.startswith("FAILED "):
            rest = line[len("FAILED ") :]
            node_id = rest.split(" - ", 1)[0].strip()
            failed.add(node_id)
    return frozenset(passed), frozenset(failed)


def apply_patch(content: str, fault: FaultSpec) -> str:
    """Applies `fault`'s exact patch to `content`. Fails closed
    (`PatchNotUniqueError`) unless `old_string` occurs exactly once."""
    count = content.count(fault.old_string)
    if count != 1:
        raise PatchNotUniqueError(
            f"{fault.fault_id}: expected exactly one occurrence of old_string in {fault.source_file!r}, found {count}"
        )
    return content.replace(fault.old_string, fault.new_string, 1)


def classify_verdict(
    *,
    evidence_exit_code: int,
    control_passed_node_ids: frozenset[str],
    evidence_failed_node_ids: frozenset[str],
) -> tuple[Verdict, list[str]]:
    """Pure verdict classification given an already-clean-passing control
    and a successfully-activated fault. `evidence_exit_code` outside
    {0, 1} means pytest itself did not complete an ordinary collect-and-run
    cycle (collection error, interpreter crash, interrupted, usage error)
    -- `TEST_INFRA_ERROR`, never coerced into `DETECTED`/`SURVIVED`.
    """
    if evidence_exit_code not in (0, 1):
        return Verdict.TEST_INFRA_ERROR, []
    newly_failed = sorted(control_passed_node_ids & evidence_failed_node_ids)
    if newly_failed:
        return Verdict.DETECTED, newly_failed
    return Verdict.SURVIVED, []


def _run_governed_suite(*, feature_engine_dir: Path, src_dir: Path, python_executable: str) -> TestRunResult:
    # PYTHONDONTWRITEBYTECODE is essential, not cosmetic: without it, the
    # control run can write a `.pyc` cache keyed on the pre-patch source's
    # mtime/size, and a same-second patch (near-certain given how fast this
    # sequence runs) can be indistinguishable to Python's own cache
    # invalidation -- silently reusing STALE, pre-fault bytecode during the
    # evidence run and masking a real fault as a false `SURVIVED`.
    env = {"PATH": "/usr/bin:/bin", "PYTHONPATH": str(src_dir), "PYTHONDONTWRITEBYTECODE": "1"}
    try:
        result = subprocess.run(
            [python_executable, "-m", "pytest", *_TEST_COMMAND_ARGS],
            cwd=str(feature_engine_dir),
            env=env,
            capture_output=True,
            text=True,
            timeout=_SUBPROCESS_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout.decode() if exc.stdout else "")
        stderr = exc.stderr if isinstance(exc.stderr, str) else (exc.stderr.decode() if exc.stderr else "")
        raw = stdout + stderr
        return TestRunResult(
            exit_code=-1, passed_node_ids=frozenset(), failed_node_ids=frozenset(), raw_output=raw, timed_out=True
        )
    output = result.stdout + result.stderr
    passed, failed = _parse_pytest_rA_output(output)
    return TestRunResult(exit_code=result.returncode, passed_node_ids=passed, failed_node_ids=failed, raw_output=output)


def _create_isolation(repo_root: Path, isolation_path: Path, pinned_sha: str) -> None:
    isolation_path.parent.mkdir(parents=True, exist_ok=True)
    result = _git(["worktree", "add", "--detach", str(isolation_path), pinned_sha], cwd=repo_root, timeout=120)
    if result.returncode != 0:
        raise IsolationError(f"git worktree add failed: {result.stderr.strip()}")


def _destroy_isolation(repo_root: Path, isolation_path: Path) -> bool:
    result = _git(["worktree", "remove", "--force", str(isolation_path)], cwd=repo_root, timeout=60)
    if result.returncode != 0 and isolation_path.exists():
        shutil.rmtree(isolation_path, ignore_errors=True)
        prune = _git(["worktree", "prune"], cwd=repo_root, timeout=60)
        return prune.returncode == 0 and not isolation_path.exists()
    return result.returncode == 0 and not isolation_path.exists()


def _tree_hash(cwd: Path, ref: str, relpath: str) -> str | None:
    result = _git(["rev-parse", f"{ref}:{relpath}"], cwd=cwd)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def run_fault(
    fault: FaultSpec,
    *,
    repo_root: Path,
    pinned_sha: str,
    work_root: Path,
    python_executable: str,
) -> FaultEvidenceRecord:
    """Runs the full isolate -> verify -> control -> inject -> activate ->
    evidence -> classify -> destroy sequence for exactly one fault, and
    returns its evidence record. Never raises for an ordinary fail-closed
    outcome (`CONTROL_FAILED`/`INJECTION_FAILED`/`TEST_INFRA_ERROR`) --
    those are recorded as verdicts, not exceptions.
    """
    canonical_snapshot_before = _canonical_repo_status_snapshot(repo_root)
    isolation_path = work_root / f"{fault.fault_id.lower()}-{uuid.uuid4().hex[:8]}"
    record = FaultEvidenceRecord(
        fault_id=fault.fault_id,
        method=fault.method,
        source_file=fault.source_file,
        fault_class=fault.fault_class,
        pinned_repository_head=pinned_sha,
        old_string=fault.old_string,
        new_string=fault.new_string,
        verdict=Verdict.INJECTION_FAILED,
        verdict_detail="not yet run",
        isolation_path=str(isolation_path),
    )

    expected_src_tree = _tree_hash(repo_root, pinned_sha, f"{_FEATURE_ENGINE_RELPATH}/src")
    expected_tests_tree = _tree_hash(repo_root, pinned_sha, f"{_FEATURE_ENGINE_RELPATH}/tests")
    expected_tooling_tree = _tree_hash(repo_root, pinned_sha, f"{_FEATURE_ENGINE_RELPATH}/tooling")
    record.expected_src_tree = expected_src_tree
    record.expected_tests_tree = expected_tests_tree
    record.expected_tooling_tree = expected_tooling_tree

    # Before any isolation exists, nothing has been created or could have
    # touched the canonical checkout — both "destroyed" and "never touched"
    # are trivially true unless/until an isolation is actually created
    # below, at which point the `finally` block re-derives them for real.
    record.isolation_destroyed_confirmed = True
    record.canonical_checkout_never_touched_confirmed = True

    pinned_source_relpath = f"{_FEATURE_ENGINE_RELPATH}/{fault.source_file}"
    pinned_show = _git(["show", f"{pinned_sha}:{pinned_source_relpath}"], cwd=repo_root)
    if pinned_show.returncode != 0:
        record.verdict = Verdict.INJECTION_FAILED
        record.verdict_detail = f"could not read pinned source at boundary: {pinned_show.stderr.strip()}"
        return record
    try:
        expected_patched_content = apply_patch(pinned_show.stdout, fault)
    except PatchNotUniqueError as exc:
        record.verdict = Verdict.INJECTION_FAILED
        record.verdict_detail = f"SOURCE DRIFT (pinned boundary): {exc}"
        return record
    record.activation_expected_patched_file_sha256 = hashlib.sha256(
        expected_patched_content.encode("utf-8")
    ).hexdigest()

    try:
        _create_isolation(repo_root, isolation_path, pinned_sha)
    except IsolationError as exc:
        record.verdict = Verdict.INJECTION_FAILED
        record.verdict_detail = f"ISOLATION IDENTITY MISMATCH (creation failed): {exc}"
        return record

    try:
        # Step 2: verify exact identities inside the isolation.
        head = _git(["rev-parse", "HEAD"], cwd=isolation_path).stdout.strip()
        record.isolation_head_verified = head
        src_tree = _tree_hash(isolation_path, "HEAD", "python/feature-engine/src")
        tests_tree = _tree_hash(isolation_path, "HEAD", "python/feature-engine/tests")
        tooling_tree = _tree_hash(isolation_path, "HEAD", "python/feature-engine/tooling")
        record.isolation_src_tree_verified = src_tree
        record.isolation_tests_tree_verified = tests_tree
        record.isolation_tooling_tree_verified = tooling_tree
        status = _git(["status", "--porcelain"], cwd=isolation_path).stdout.strip()
        diff_clean = _git(["diff", "--quiet"], cwd=isolation_path).returncode == 0
        identity_ok = (
            head == pinned_sha
            and src_tree == expected_src_tree
            and tests_tree == expected_tests_tree
            and tooling_tree == expected_tooling_tree
            and status == ""
            and diff_clean
        )
        if not identity_ok:
            record.verdict = Verdict.INJECTION_FAILED
            record.verdict_detail = (
                "ISOLATION IDENTITY MISMATCH: "
                f"head_match={head == pinned_sha} src_match={src_tree == expected_src_tree} "
                f"tests_match={tests_tree == expected_tests_tree} "
                f"tooling_match={tooling_tree == expected_tooling_tree} "
                f"pristine={status == '' and diff_clean}"
            )
            return record

        feature_engine_dir = isolation_path / _FEATURE_ENGINE_RELPATH
        src_dir = feature_engine_dir / "src"

        # Step 3: clean control, before injecting anything.
        control = _run_governed_suite(
            feature_engine_dir=feature_engine_dir, src_dir=src_dir, python_executable=python_executable
        )
        record.control_test_command_actual = f"{python_executable} -m pytest " + " ".join(_TEST_COMMAND_ARGS)
        record.control_exit_code = control.exit_code
        record.control_passed_node_id_count = len(control.passed_node_ids)
        if control.timed_out or control.exit_code != 0 or len(control.failed_node_ids) > 0:
            record.control_result = "FAIL"
            record.verdict = Verdict.CONTROL_FAILED
            record.verdict_detail = (
                f"clean control did not pass in full: exit_code={control.exit_code}, "
                f"failed={sorted(control.failed_node_ids)}, timed_out={control.timed_out}"
            )
            return record
        record.control_result = "PASS"

        # Step 4: apply exactly one fault, inside the isolation's own file only.
        target_file = feature_engine_dir / fault.source_file
        original_content = target_file.read_text()
        try:
            patched_content = apply_patch(original_content, fault)
        except PatchNotUniqueError as exc:
            record.verdict = Verdict.INJECTION_FAILED
            record.verdict_detail = f"SOURCE DRIFT (isolation copy): {exc}"
            return record
        target_file.write_text(patched_content)
        record.activation_new_string_unique_and_located = patched_content.count(fault.new_string) >= 1

        # Step 5: prove activation.
        observed_content = target_file.read_text()
        observed_hash = hashlib.sha256(observed_content.encode("utf-8")).hexdigest()
        record.activation_observed_patched_file_sha256 = observed_hash
        hash_match = observed_hash == record.activation_expected_patched_file_sha256

        numstat = _git(["diff", "--numstat"], cwd=isolation_path).stdout.strip()
        files_changed = len([line for line in numstat.splitlines() if line.strip()])
        record.activation_diff_files_changed = files_changed
        file_diff = _git(["diff", "-U0", "--", fault.source_file], cwd=feature_engine_dir).stdout
        hunks = len([line for line in file_diff.splitlines() if line.startswith("@@")])
        record.activation_diff_hunks_in_target_file = hunks

        scope_ok = files_changed == 1 and hunks == 1
        record.activation_diff_single_hunk_single_file_confirmed = scope_ok

        if not (record.activation_new_string_unique_and_located and hash_match and scope_ok):
            record.verdict = Verdict.INJECTION_FAILED
            record.verdict_detail = (
                f"ACTIVATION MISMATCH: new_string_located={record.activation_new_string_unique_and_located}, "
                f"hash_match={hash_match}, files_changed={files_changed}, hunks={hunks}"
            )
            return record

        # Step 6: run the evidence suite, inside the same isolation.
        evidence = _run_governed_suite(
            feature_engine_dir=feature_engine_dir, src_dir=src_dir, python_executable=python_executable
        )
        record.evidence_test_command_actual = f"{python_executable} -m pytest " + " ".join(_TEST_COMMAND_ARGS)
        record.evidence_exit_code = evidence.exit_code

        if evidence.timed_out:
            record.verdict = Verdict.TEST_INFRA_ERROR
            record.verdict_detail = "evidence run timed out"
            return record

        # Step 7: classify verdict.
        verdict, detecting = classify_verdict(
            evidence_exit_code=evidence.exit_code,
            control_passed_node_ids=control.passed_node_ids,
            evidence_failed_node_ids=evidence.failed_node_ids,
        )
        record.verdict = verdict
        record.detecting_test_node_ids = detecting
        if verdict is Verdict.TEST_INFRA_ERROR:
            record.verdict_detail = (
                f"evidence run did not complete an ordinary pass/fail cycle: exit_code={evidence.exit_code}"
            )
        elif verdict is Verdict.DETECTED:
            record.verdict_detail = f"{len(detecting)} node ID(s) passed control and failed under the activated fault"
        else:
            record.verdict_detail = "every node ID that passed control also passed under the activated fault"
        return record
    finally:
        destroyed = _destroy_isolation(repo_root, isolation_path)
        record.isolation_destroyed_confirmed = destroyed
        canonical_snapshot_after = _canonical_repo_status_snapshot(repo_root)
        record.canonical_checkout_never_touched_confirmed = canonical_snapshot_after == canonical_snapshot_before
        if not record.canonical_checkout_never_touched_confirmed:
            # Fail closed at the loudest possible volume: this must never
            # happen (the canonical tree is never written to by this
            # harness), but if it ever does, do not silently continue.
            raise IsolationError(
                f"{fault.fault_id}: canonical checkout state changed during this fault's run — "
                "refusing to continue silently"
            )
