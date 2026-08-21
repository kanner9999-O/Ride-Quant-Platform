"""Deterministic opaque subject identity.

regime.md §19 explicitly defers the concrete `regime_subject_id` algorithm to
implementation, requiring only that it be opaque, stable, and deterministic
from the declared five-field qualifying scope (Chapter 6 §6.1/§6.8). This
module pins one such algorithm for raw-regime-engine's own authoritative
subjects — a module-local implementation detail, not a Domain Contract or
cross-module semantic. Duplicated (not imported) from structure-engine's own
`identity.py`, deliberately — the two modules are structurally independent
(ADR-014) and must not share code across a forbidden-dependency boundary,
mirroring the existing precedent of market-reference-service's own
independent copy of a Go decimal package originally duplicated from
market-data-ingestion.
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
