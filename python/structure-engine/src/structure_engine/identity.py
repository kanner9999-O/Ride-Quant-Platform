"""Deterministic opaque subject identity.

swing.md §17 and structure.md §16 both explicitly leave the concrete subject-id
algorithm out of the Domain Contract's scope, requiring only that it be opaque,
stable, and deterministic from the declared qualifying-scope fields (Chapter 6
§6.1/§6.8). This module pins one such algorithm for structure-engine's own
authoritative subjects — a module-local implementation detail, not a Domain
Contract or cross-module semantic.
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
