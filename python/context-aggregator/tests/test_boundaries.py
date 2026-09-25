"""Structural boundary tests that scan this package's own source tree —
these enforce constraints the type system and unit tests cannot: no import
of another module's implementation package, no wall-clock domain decision,
no runtime network/filesystem dependency in the deterministic core.
"""

from __future__ import annotations

import ast
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parent.parent / "src" / "context_aggregator"

PROHIBITED_IMPORT_PREFIXES = (
    "feature_engine",
    "structure_engine",
    "raw_regime_engine",
)

PROHIBITED_WALL_CLOCK_CALLS = {
    ("datetime", "now"),
    ("datetime", "utcnow"),
    ("time", "time"),
    ("time", "monotonic"),
}

PROHIBITED_IO_MODULES = {
    "socket",
    "requests",
    "urllib",
    "http",
    "aiohttp",
    "sqlite3",
    "subprocess",
}


def _all_source_files() -> list[Path]:
    return sorted(SRC_ROOT.rglob("*.py"))


def test_package_has_source_files() -> None:
    assert _all_source_files(), "expected context_aggregator source files to exist"


def test_no_imports_of_producer_implementation_packages() -> None:
    for path in _all_source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(PROHIBITED_IMPORT_PREFIXES), (
                        f"{path}: prohibited import {alias.name!r}"
                    )
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                assert not module.startswith(PROHIBITED_IMPORT_PREFIXES), f"{path}: prohibited import from {module!r}"


def test_no_wall_clock_domain_decision() -> None:
    for path in _all_source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                attr = node.func.attr
                owner = node.func.value
                owner_name = owner.id if isinstance(owner, ast.Name) else None
                if owner_name is not None and (owner_name, attr) in PROHIBITED_WALL_CLOCK_CALLS:
                    raise AssertionError(f"{path}: prohibited wall-clock call {owner_name}.{attr}()")


def test_no_runtime_network_or_filesystem_dependency() -> None:
    for path in _all_source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [(node.module or "").split(".")[0]]
            for name in names:
                assert name not in PROHIBITED_IO_MODULES, f"{path}: prohibited I/O import {name!r}"

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
                raise AssertionError(f"{path}: prohibited filesystem call open()")


def test_no_float_round_trip_of_decimal_values() -> None:
    """Section H: numerical Context values must be preserved losslessly
    (`Decimal`, never a float round-trip). No source file may call
    `float(...)`."""
    for path in _all_source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "float":
                raise AssertionError(f"{path}: prohibited float() conversion")
