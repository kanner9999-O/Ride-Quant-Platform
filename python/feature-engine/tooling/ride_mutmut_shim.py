"""Ride-owned, FEATURE-ENGINE-ONLY compatibility shim for mutmut 3.7.0.

Implements the compatibility design approved in Testing Convention v0.16
(reviewed semantic boundary 773bd9851fe6aa5023740d07db55b5337c9362d4). Fixes
`P3-PY-MUT-BASELINE-B-MAJ-01` (`MUTMUT_3_7_INTERNAL_DEFECT`): mutmut's own
forced-fail sanity phase aborts the entire run with a fatal
`BadTestExecutionCommandsException` when its injected sentinel exception
surfaces via a conftest.py ImportError (pytest exit code 4) rather than a
normal test failure (exit code 1) -- which is exactly what happens here,
because `tests/conftest.py` legitimately calls a mutation-instrumented
function at module import time.

Detection is call-site-authenticated by Python code-object identity, never by
text, exception name, or filename/function-name-only matching:

1. At import time, the exact code object of mutmut's own nested `trampoline`
   function (wrap_in_trampoline -> mutmut_mutated -> trampoline, in
   mutmut/mutation/trampoline.py) is derived and pinned from the currently
   installed mutmut 3.7.0 package.
2. Fail closed: if that code object cannot be resolved, the pin is `None` and
   the marker below can never be set True by any caller -- behavior falls
   back unconditionally to stock, unmodified mutmut.
3. A subclass of mutmut's own `MutmutProgrammaticFailException` is rebound
   into `mutmut.mutation.trampoline`'s own module namespace, so the real
   trampoline code constructs the subclass. The subclass's `__init__`
   authenticates its immediate caller frame by code-object identity (`is`)
   against the pinned trampoline code object, setting an invocation-local
   marker ONLY when that identity check passes.
4. `PytestRunner.execute_pytest` is patched: a pytest exit code of 4 is
   treated as a successful forced-fail verification ONLY when
   `MUTANT_UNDER_TEST == "fail"` AND the marker was set during that exact
   invocation. Every other exit-code-4 case is fatal, byte-for-byte identical
   to unmodified mutmut 3.7.0 -- including direct construction of the
   rebound exception from conftest/plugin/test/arbitrary helper code, which
   never authenticates because its caller frame is never the pinned
   trampoline code object.

This module never modifies, forks, or redistributes any mutmut file -- it
operates entirely via runtime monkeypatching against the officially installed
PyPI package. Scope is FEATURE-ENGINE-ONLY: nothing here is imported by, or
affects, any other module in this repository.
"""

from __future__ import annotations

import os
import sys
from typing import Any

import mutmut.mutation.trampoline as _trampoline_module
from mutmut import Config
from mutmut.__main__ import BadTestExecutionCommandsException, PytestRunner
from mutmut.__main__ import MutmutProgrammaticFailException as _OriginalSentinel


def resolve_pinned_trampoline_code_object() -> Any | None:
    """Derive the exact, stable code object of mutmut's own nested
    `trampoline` function from the currently-installed mutmut package.
    Returns `None` (fail-closed) if the expected structure is not found."""
    try:
        wrap_code = _trampoline_module.wrap_in_trampoline.__code__
        mutmut_mutated_code = None
        for const in wrap_code.co_consts:
            if getattr(const, "co_name", None) == "mutmut_mutated":
                mutmut_mutated_code = const
                break
        if mutmut_mutated_code is None:
            return None
        expected_filename_suffix = os.path.join("mutation", "trampoline.py")
        for const in mutmut_mutated_code.co_consts:
            if getattr(const, "co_name", None) == "trampoline" and getattr(
                const, "co_filename", ""
            ).endswith(expected_filename_suffix):
                return const
        return None
    except Exception:
        return None


_PINNED_TRAMPOLINE_CODE = resolve_pinned_trampoline_code_object()

_invocation_marker: dict[str, bool] = {"sentinel_constructed": False}


class StructuralForcedFailSentinel(_OriginalSentinel):
    """Subclass of mutmut's own sentinel exception. Sets the invocation-local
    marker ONLY when constructed with the pinned, real mutmut trampoline code
    object as its immediate caller frame -- authenticating the call site by
    Python code-object identity, never by exception type/name/text alone."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if _PINNED_TRAMPOLINE_CODE is None:
            return  # fail closed: identity could never be resolved
        caller_frame = sys._getframe(1)
        if caller_frame is not None and caller_frame.f_code is _PINNED_TRAMPOLINE_CODE:
            _invocation_marker["sentinel_constructed"] = True


_original_trampoline_exception_binding = _trampoline_module.MutmutProgrammaticFailException
_original_execute_pytest = PytestRunner.execute_pytest


def _patched_execute_pytest(self: PytestRunner, params: list[str], **kwargs: Any) -> int:
    import pytest

    full_params = ["--rootdir=.", "--tb=native"] + params + self._pytest_add_cli_args
    if Config.get().debug:
        full_params = ["-vv"] + full_params
        print("python -m pytest ", " ".join(f'"{p}"' for p in full_params))

    _invocation_marker["sentinel_constructed"] = False
    try:
        exit_code = int(pytest.main(full_params, **kwargs))
    finally:
        sentinel_constructed_this_invocation = _invocation_marker["sentinel_constructed"]
        _invocation_marker["sentinel_constructed"] = False

    if Config.get().debug:
        print("    exit code", exit_code)

    if exit_code == 4:
        mutant_under_test = os.environ.get("MUTANT_UNDER_TEST", "")
        if mutant_under_test == "fail" and sentinel_constructed_this_invocation:
            print(
                "    [ride-shim] pytest exit 4 authenticated as mutmut's own real, "
                "pinned nested trampoline code object constructing its forced-fail "
                "sentinel during this exact invocation -- treating as a SUCCESSFUL "
                "forced-fail verification."
            )
            return 1
        raise BadTestExecutionCommandsException(params)
    return exit_code


def install_shim() -> None:
    """Activate the compatibility shim: rebind mutmut's trampoline-module
    sentinel to the call-site-authenticated subclass and monkeypatch
    PytestRunner.execute_pytest. Idempotent."""
    _trampoline_module.MutmutProgrammaticFailException = StructuralForcedFailSentinel
    PytestRunner.execute_pytest = _patched_execute_pytest


def uninstall_shim() -> None:
    """Restore stock, unmodified mutmut 3.7.0 behavior."""
    _trampoline_module.MutmutProgrammaticFailException = _original_trampoline_exception_binding
    PytestRunner.execute_pytest = _original_execute_pytest


def main() -> None:
    """Entrypoint: install the shim, then invoke mutmut's own real CLI
    unchanged (`from mutmut.__main__ import cli; cli()`). Governed Feature
    Engine mutmut measurement transactions invoke this instead of the bare
    `mutmut` command; no other invocation path in this repository changes."""
    install_shim()
    from mutmut.__main__ import cli

    cli()


if __name__ == "__main__":
    main()
