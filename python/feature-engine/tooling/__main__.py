"""Entrypoint for `python -m tooling <mutmut-args>` (e.g. `python -m tooling run`).
Delegates to `ride_mutmut_shim.main()`, which installs the compatibility shim
before invoking mutmut's own unmodified CLI."""

from tooling.ride_mutmut_shim import main

if __name__ == "__main__":
    main()
