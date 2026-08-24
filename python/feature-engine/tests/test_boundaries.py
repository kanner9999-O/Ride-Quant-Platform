from __future__ import annotations

import pathlib
import re

import feature_engine

# --- 20. Static/import boundary ------------------------------------------------

_PROHIBITED_IMPORT_MODULES = (
    "structure_engine",
    "raw_regime_engine",
    "strategy",
    "decision",
    "risk",
    "execution",
    "context_aggregator",
)


def test_no_prohibited_module_imports() -> None:
    package_dir = pathlib.Path(feature_engine.__file__).parent
    for module in _PROHIBITED_IMPORT_MODULES:
        pattern = re.compile(rf"^\s*(import|from)\s+{re.escape(module)}\b", re.MULTILINE)
        for path in package_dir.rglob("*.py"):
            content = path.read_text()
            assert not pattern.search(content), f"{path} imports prohibited module {module!r}"


def test_no_wall_clock_domain_decisions() -> None:
    package_dir = pathlib.Path(feature_engine.__file__).parent
    pattern = re.compile(r"datetime\.now\(|time\.time\(")
    for path in package_dir.rglob("*.py"):
        content = path.read_text()
        assert not pattern.search(content), f"{path} uses wall-clock time for a domain decision"


def test_no_prohibited_structure_semantics_defined_or_imported() -> None:
    """These terms may legitimately appear in prose (docstrings explaining
    what this module does NOT consume, e.g. candle.py/regime_passthrough.py)
    but must never be *defined* (class/def) or *imported* as an actual
    symbol anywhere in this package.
    """
    package_dir = pathlib.Path(feature_engine.__file__).parent
    prohibited_terms = (
        "BreakOfStructureDetected",
        "ChangeOfCharacterDetected",
        "StructureFactInvalidated",
        "StructureRecomputed",
        "StructureCurrentView",
        "SwingCandidateDetected",
        "SwingCurrentView",
        "CandleObserved",
        "CandleCurrentView",
        "RegimeCurrentView",
    )
    for term in prohibited_terms:
        definition_pattern = re.compile(rf"^\s*(class|def)\s+{re.escape(term)}\b", re.MULTILINE)
        import_pattern = re.compile(rf"^\s*(import|from)\s+.*\b{re.escape(term)}\b", re.MULTILINE)
        for path in package_dir.rglob("*.py"):
            content = path.read_text()
            assert not definition_pattern.search(content), f"{path} defines prohibited type {term!r}"
            assert not import_pattern.search(content), f"{path} imports prohibited type {term!r}"
    for term in prohibited_terms:
        assert not hasattr(feature_engine, term), f"feature_engine exports prohibited symbol {term!r}"


# --- 12. Prohibited input: BOS/CHoCH / Structure events cannot be Feature input


def test_feature_engine_defines_no_structure_event_types() -> None:
    assert not hasattr(feature_engine, "BreakOfStructureDetected")
    assert not hasattr(feature_engine, "ChangeOfCharacterDetected")
    assert not hasattr(feature_engine, "StructureFactInvalidated")
    assert not hasattr(feature_engine, "StructureRecomputed")
