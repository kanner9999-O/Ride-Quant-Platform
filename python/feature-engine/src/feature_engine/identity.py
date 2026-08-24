"""Deterministic opaque subject identity.

feature.md §19 explicitly defers the concrete `feature_subject_id` algorithm
to implementation, requiring only that it be opaque, stable, and
deterministic from the declared five-field qualifying scope (Chapter 6
§6.1/§6.8). This module pins one such algorithm for feature-engine's own
authoritative subjects — a module-local implementation detail, not a Domain
Contract or cross-module semantic. Duplicated (not imported) from
structure-engine/raw-regime-engine's own `identity.py` — each Python module
is independently built/deployed (Chapter 3 §3.1); feature-engine is
*permitted* to depend on structure-engine/raw-regime-engine's *event
contracts* (module-registry.yaml `depends_on`), which is a different concern
from importing their Python packages as code dependencies.
"""

from __future__ import annotations

import hashlib


def deterministic_id(*parts: object) -> str:
    """SHA-256 hex digest over the pipe-joined string form of ``parts``.

    Same parts always produce the same id (deterministic); different parts
    always produce a different id with overwhelming probability (stable,
    collision-resistant). Callers must never parse the result (Chapter 6
    §6.8) — it is opaque by construction.
    """
    joined = "|".join(str(part) for part in parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()
