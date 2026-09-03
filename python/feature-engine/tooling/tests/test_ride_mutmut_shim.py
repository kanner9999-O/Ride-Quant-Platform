"""Dedicated tests for the FEATURE-ENGINE-ONLY mutmut compatibility shim
(Testing Convention v0.16). Not part of `tests/` -- deliberately outside the
governed Feature Engine mutation-testing suite (`testpaths = ["tests"]`,
`[tool.mutmut] pytest_add_cli_args_test_selection = ["tests/"]`), since this
validates tooling infrastructure, not Feature Engine business logic. Run
directly via `pytest tooling/tests/`.
"""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest

from tooling import ride_mutmut_shim as shim


@pytest.fixture(autouse=True)
def _isolate_shim_state() -> Iterator[None]:
    """Ensure the shim is uninstalled before and after every test, and that
    MUTANT_UNDER_TEST / the invocation marker never leak across tests."""
    shim.uninstall_shim()
    shim._invocation_marker["sentinel_constructed"] = False
    original_env = os.environ.get("MUTANT_UNDER_TEST")
    try:
        yield
    finally:
        shim.uninstall_shim()
        shim._invocation_marker["sentinel_constructed"] = False
        if original_env is None:
            os.environ.pop("MUTANT_UNDER_TEST", None)
        else:
            os.environ["MUTANT_UNDER_TEST"] = original_env


def test_pin_resolves_against_installed_mutmut() -> None:
    """The exact trampoline code object must be resolvable against the
    actually-installed mutmut 3.7.0 package (fail-closed path not
    exercised here since resolution is expected to succeed)."""
    code_obj = shim.resolve_pinned_trampoline_code_object()
    assert code_obj is not None
    assert code_obj.co_name == "trampoline"
    assert code_obj.co_filename.endswith(os.path.join("mutation", "trampoline.py"))
    # Module-level pin must be the SAME object (compiled once, stable identity).
    assert shim._PINNED_TRAMPOLINE_CODE is code_obj


def test_genuine_trampoline_path_is_authenticated() -> None:
    """Calling the REAL mutmut trampoline (via its own wrap_in_trampoline)
    with MUTANT_UNDER_TEST='fail' must construct the sentinel via the pinned
    code object as caller, setting the marker True."""
    import mutmut.mutation.trampoline as trampoline_module

    shim.install_shim()

    def _mutmut_orig() -> str:
        return "orig"

    wrapped = trampoline_module.wrap_in_trampoline({"_mutmut_orig": _mutmut_orig})(_mutmut_orig)

    os.environ["MUTANT_UNDER_TEST"] = "fail"
    assert shim._invocation_marker["sentinel_constructed"] is False
    with pytest.raises(shim.StructuralForcedFailSentinel):
        wrapped()
    assert shim._invocation_marker["sentinel_constructed"] is True


def test_direct_spoof_construction_is_rejected() -> None:
    """Constructing the rebound sentinel directly from test/plugin/conftest
    code (never through the real trampoline) must NOT set the marker, even
    with MUTANT_UNDER_TEST='fail' active."""
    shim.install_shim()
    os.environ["MUTANT_UNDER_TEST"] = "fail"

    decoy = shim.StructuralForcedFailSentinel("decoy, not from trampoline")

    assert isinstance(decoy, Exception)
    assert shim._invocation_marker["sentinel_constructed"] is False


def test_uninstall_restores_stock_mutmut_bindings() -> None:
    """After uninstall_shim(), mutmut's own original exception binding and
    execute_pytest method must be restored exactly."""
    import mutmut.mutation.trampoline as trampoline_module
    from mutmut.__main__ import MutmutProgrammaticFailException, PytestRunner

    shim.install_shim()
    assert trampoline_module.MutmutProgrammaticFailException is shim.StructuralForcedFailSentinel
    assert PytestRunner.execute_pytest is shim._patched_execute_pytest

    shim.uninstall_shim()
    assert trampoline_module.MutmutProgrammaticFailException is MutmutProgrammaticFailException
    assert PytestRunner.execute_pytest is shim._original_execute_pytest


def test_normal_pytest_exit_codes_pass_through_unaffected(tmp_path: object) -> None:
    """A non-4 exit code (e.g. a normal passing suite) must be returned
    unmodified by the patched execute_pytest, with the shim installed."""
    import tempfile

    shim.install_shim()
    os.environ["MUTANT_UNDER_TEST"] = ""

    from mutmut.__main__ import PytestRunner

    runner = PytestRunner.__new__(PytestRunner)
    runner._pytest_add_cli_args = []

    tmpdir = tempfile.mkdtemp(prefix="ride_shim_normal_exit_")
    test_file = os.path.join(tmpdir, "test_ok.py")
    with open(test_file, "w") as f:
        f.write("def test_ok():\n    assert True\n")

    real_cwd = os.getcwd()
    os.chdir(tmpdir)
    try:
        exit_code = runner.execute_pytest(["test_ok.py"])
    finally:
        os.chdir(real_cwd)

    assert exit_code == 0
