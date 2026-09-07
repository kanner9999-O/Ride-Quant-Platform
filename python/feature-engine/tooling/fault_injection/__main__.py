"""Entrypoint: `python -m tooling.fault_injection --boundary <sha> --output <path>`.

Runs the full approved 10-fault population (`faults.APPROVED_FAULTS`)
against the exact pinned repository boundary, one isolated `git worktree`
checkout per fault, and writes one JSON evidence artifact (schema per
`feature-engine-mutation-surface-completeness-design-001.md` §2.1b,
extended per this implementation transaction's own bounded corrections).

This script performs no repository-state mutation of its own beyond
disposable, per-fault `git worktree` checkouts under `--work-root` — the
canonical checkout is verified untouched after every fault.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

from tooling.fault_injection.faults import APPROVED_FAULTS
from tooling.fault_injection.harness import FaultEvidenceRecord, Verdict, run_fault


def _repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=str(Path(__file__).resolve().parent),
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(result.stdout.strip())


def _record_to_json(record: FaultEvidenceRecord) -> dict[str, object]:
    data = asdict(record)
    data["verdict"] = record.verdict.value
    return data


def _rollup(records: list[FaultEvidenceRecord]) -> dict[str, object]:
    by_method: dict[str, list[str]] = {}
    verdict_by_fault_id = {r.fault_id: r.verdict for r in records}
    for r in records:
        by_method.setdefault(r.method, []).append(r.fault_id)
    method_qualifies = {
        method: any(verdict_by_fault_id[fid] is Verdict.DETECTED for fid in fault_ids)
        for method, fault_ids in by_method.items()
    }
    return {
        "methods": by_method,
        "method_has_at_least_one_detected_fault": method_qualifies,
        "five_of_five_completion_criterion_supported": len(method_qualifies) == 5 and all(method_qualifies.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--boundary", required=True, help="Pinned repository boundary SHA to run evidence against")
    parser.add_argument("--output", required=True, type=Path, help="Path to write the JSON evidence artifact")
    parser.add_argument("--work-root", required=True, type=Path, help="Disposable directory for isolated checkouts")
    parser.add_argument(
        "--python-executable", required=True, help="Interpreter used to run the governed suite inside each isolation"
    )
    args = parser.parse_args()

    repo_root = _repo_root()
    args.work_root.mkdir(parents=True, exist_ok=True)

    records: list[FaultEvidenceRecord] = []
    for fault in APPROVED_FAULTS:
        print(f"[fault-injection] running {fault.fault_id} ({fault.method}) ...", file=sys.stderr)
        record = run_fault(
            fault,
            repo_root=repo_root,
            pinned_sha=args.boundary,
            work_root=args.work_root,
            python_executable=args.python_executable,
        )
        records.append(record)
        print(f"[fault-injection] {fault.fault_id}: {record.verdict.value} — {record.verdict_detail}", file=sys.stderr)

    artifact = {
        "pinned_repository_head": args.boundary,
        "fault_count": len(records),
        "faults": [_record_to_json(r) for r in records],
        "rollup": _rollup(records),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    print(f"[fault-injection] wrote evidence artifact to {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
