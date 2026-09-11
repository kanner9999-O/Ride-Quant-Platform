from __future__ import annotations

from pathlib import Path

import pytest
from conftest import FEATURE_OUTPUT_CONTRACT_VERSION, OUTPUT_EVENT_CONTRACT_AUTHORITY

from feature_engine import EventContractRef
from feature_engine.contracts import VerifiedOutputEventContractAuthority
from feature_engine.errors import (
    OutputEventContractIdentityMismatchError,
    OutputEventContractNotPublishedError,
    OutputEventContractUnresolvableError,
)
from feature_engine.output_contract_resolver import (
    FilesystemOutputEventContractAuthorityResolver,
    StaticOutputEventContractAuthorityProvider,
    _find_repo_root,
    resolve_output_event_contract_authority_from_repository,
)

_COMPUTED_RELPATH = "docs/architecture/event-contracts/feature-computed/v1.0.yaml"
_INVALIDATED_RELPATH = "docs/architecture/event-contracts/feature-fact-invalidated/v1.0.yaml"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _artifact_yaml(*, contract_id: str, contract_version: str, status: str) -> str:
    return f"""# TEST FIXTURE ONLY -- not a real Event Contract version-artifact.
contract_id: {contract_id}
contract_version: {contract_version}
status: {status}

event_type: {contract_id.upper().replace("-", "_")}
event_class: derived_fact
allowed_streams:
  - stream_id: feature-engine-feature
merge_constraints:
  prerequisite_policy: causation_must_resolve_before_apply
"""


def _write_fake_repo(
    tmp_path: Path,
    *,
    computed_status: str = "Published",
    invalidated_status: str = "Published",
    computed_contract_id: str = "feature-computed",
    computed_contract_version: str = "v1.0",
    invalidated_contract_id: str = "feature-fact-invalidated",
    invalidated_contract_version: str = "v1.0",
) -> Path:
    """A minimal, TEMPORARY, fabricated repository tree mirroring just
    enough of the real Event Contract version-artifact YAML shape for the
    resolver's line scanner to parse — never touches the actual
    authoritative docs.
    """
    _write(tmp_path / "docs" / "MARKER.md", "marker file, only used to anchor repo-root discovery")
    _write(
        tmp_path / _COMPUTED_RELPATH,
        _artifact_yaml(
            contract_id=computed_contract_id, contract_version=computed_contract_version, status=computed_status
        ),
    )
    _write(
        tmp_path / _INVALIDATED_RELPATH,
        _artifact_yaml(
            contract_id=invalidated_contract_id,
            contract_version=invalidated_contract_version,
            status=invalidated_status,
        ),
    )
    return tmp_path


# --- Positive resolution: the real, current repository artifacts -----------


def test_real_output_authority_resolves_successfully() -> None:
    resolved = resolve_output_event_contract_authority_from_repository("v1.0", "v1.0")
    assert isinstance(resolved, VerifiedOutputEventContractAuthority)
    assert resolved.computed_contract_ref == EventContractRef("feature-computed", "v1.0")
    assert resolved.invalidated_contract_ref == EventContractRef("feature-fact-invalidated", "v1.0")


def test_conftest_authority_matches_direct_resolution() -> None:
    """Sanity control: `conftest.OUTPUT_EVENT_CONTRACT_AUTHORITY` — used by
    every engine construction across this suite — is exactly what direct
    resolution returns, never a hand-substituted stand-in.
    """
    direct = resolve_output_event_contract_authority_from_repository(
        FEATURE_OUTPUT_CONTRACT_VERSION, FEATURE_OUTPUT_CONTRACT_VERSION
    )
    assert OUTPUT_EVENT_CONTRACT_AUTHORITY == direct


# --- P3-FEATURE-EVID05B-IMPL-A-MAJ-01 remediation: independent lineages ----


def test_independently_pinned_different_versions_resolve_successfully(tmp_path: Path) -> None:
    """`feature-computed` and `feature-fact-invalidated` are NOT required to
    share a version — a repository where each lineage is Published at a
    genuinely different exact version (different canonical PATH, not merely
    different embedded content at the same path) resolves successfully,
    with each resolved ref carrying its own lineage's own version.
    """
    _write(tmp_path / "docs" / "MARKER.md", "marker file, only used to anchor repo-root discovery")
    _write(
        tmp_path / "docs/architecture/event-contracts/feature-computed/v1.0.yaml",
        _artifact_yaml(contract_id="feature-computed", contract_version="v1.0", status="Published"),
    )
    _write(
        tmp_path / "docs/architecture/event-contracts/feature-fact-invalidated/v2.0.yaml",
        _artifact_yaml(contract_id="feature-fact-invalidated", contract_version="v2.0", status="Published"),
    )
    resolved = resolve_output_event_contract_authority_from_repository("v1.0", "v2.0", repo_root=tmp_path)
    assert resolved.computed_contract_ref == EventContractRef("feature-computed", "v1.0")
    assert resolved.invalidated_contract_ref == EventContractRef("feature-fact-invalidated", "v2.0")


def test_invalidated_lineage_failure_is_independent_of_computed_success(tmp_path: Path) -> None:
    """`feature-computed` resolving successfully must never mask or
    substitute for an independently-pinned `feature-fact-invalidated`
    version that does not exist.
    """
    repo = _write_fake_repo(tmp_path, computed_contract_version="v1.0", invalidated_contract_version="v1.0")
    with pytest.raises(OutputEventContractUnresolvableError):
        resolve_output_event_contract_authority_from_repository("v1.0", "v9.0", repo_root=repo)


def test_computed_lineage_failure_is_independent_of_invalidated_success(tmp_path: Path) -> None:
    """The reverse of the above: `feature-fact-invalidated` resolving
    successfully must never mask an independently-pinned `feature-computed`
    version that does not exist.
    """
    repo = _write_fake_repo(tmp_path, computed_contract_version="v1.0", invalidated_contract_version="v1.0")
    with pytest.raises(OutputEventContractUnresolvableError):
        resolve_output_event_contract_authority_from_repository("v9.0", "v1.0", repo_root=repo)


def test_no_implicit_version_substitution_between_lineages(tmp_path: Path) -> None:
    """Both lineages having a Published artifact available at the SAME
    version (`v1.0`) must never cause one lineage's requested, different
    version to be silently substituted with the other's — each resolved ref
    carries exactly the version it was independently asked to resolve.
    """
    repo = _write_fake_repo(tmp_path, computed_contract_version="v1.0", invalidated_contract_version="v1.0")
    _write(
        repo / "docs/architecture/event-contracts/feature-computed/v2.0.yaml",
        _artifact_yaml(contract_id="feature-computed", contract_version="v2.0", status="Published"),
    )
    resolved = resolve_output_event_contract_authority_from_repository("v2.0", "v1.0", repo_root=repo)
    assert resolved.computed_contract_ref == EventContractRef("feature-computed", "v2.0")
    assert resolved.invalidated_contract_ref == EventContractRef("feature-fact-invalidated", "v1.0")


# --- Canonical path resolution (ADR-039) ------------------------------------


def test_resolution_uses_exact_canonical_path_no_alias(tmp_path: Path) -> None:
    """Only the exact `docs/architecture/event-contracts/<contract_id>/
    <contract_version>.yaml` path is ever read — a differently-named file,
    even with identical content, is never found.
    """
    repo = _write_fake_repo(tmp_path)
    (repo / _COMPUTED_RELPATH).rename(repo / "docs/architecture/event-contracts/feature-computed/v1.0.yml")
    with pytest.raises(OutputEventContractUnresolvableError):
        resolve_output_event_contract_authority_from_repository("v1.0", "v1.0", repo_root=repo)


def test_missing_computed_artifact_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_repo(tmp_path)
    (repo / _COMPUTED_RELPATH).unlink()
    with pytest.raises(OutputEventContractUnresolvableError):
        resolve_output_event_contract_authority_from_repository("v1.0", "v1.0", repo_root=repo)


def test_missing_invalidated_artifact_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_repo(tmp_path)
    (repo / _INVALIDATED_RELPATH).unlink()
    with pytest.raises(OutputEventContractUnresolvableError):
        resolve_output_event_contract_authority_from_repository("v1.0", "v1.0", repo_root=repo)


def test_nonexistent_contract_version_fails_closed(tmp_path: Path) -> None:
    """A `contract_version` with no artifact at its own canonical path
    (e.g. an unpublished future version) fails closed — never falls back
    to the nearest existing version.
    """
    repo = _write_fake_repo(tmp_path)
    with pytest.raises(OutputEventContractUnresolvableError):
        resolve_output_event_contract_authority_from_repository("v2.0", "v2.0", repo_root=repo)


# --- status: Published requirement (ADR-039/ADR-040) ------------------------


def test_draft_computed_artifact_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_repo(tmp_path, computed_status="Draft")
    with pytest.raises(OutputEventContractNotPublishedError):
        resolve_output_event_contract_authority_from_repository("v1.0", "v1.0", repo_root=repo)


def test_draft_invalidated_artifact_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_repo(tmp_path, invalidated_status="Draft")
    with pytest.raises(OutputEventContractNotPublishedError):
        resolve_output_event_contract_authority_from_repository("v1.0", "v1.0", repo_root=repo)


def test_matching_published_artifacts_resolve_successfully(tmp_path: Path) -> None:
    """Sanity control: the SAME fixture-generation path, with no deliberate
    defect, resolves cleanly — proving the failure tests above fail for the
    SPECIFIC reason under test, not fixture malformation.
    """
    repo = _write_fake_repo(tmp_path)
    resolved = resolve_output_event_contract_authority_from_repository("v1.0", "v1.0", repo_root=repo)
    assert resolved.computed_contract_ref == EventContractRef("feature-computed", "v1.0")
    assert resolved.invalidated_contract_ref == EventContractRef("feature-fact-invalidated", "v1.0")


# --- Self-identity consistency (artifact content vs. its own canonical path)


def test_computed_artifact_wrong_contract_id_inside_content_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_repo(tmp_path, computed_contract_id="not-feature-computed")
    with pytest.raises(OutputEventContractIdentityMismatchError):
        resolve_output_event_contract_authority_from_repository("v1.0", "v1.0", repo_root=repo)


def test_computed_artifact_wrong_contract_version_inside_content_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_repo(tmp_path, computed_contract_version="v2.0")
    with pytest.raises(OutputEventContractIdentityMismatchError):
        resolve_output_event_contract_authority_from_repository("v1.0", "v1.0", repo_root=repo)


# --- Malformed artifact content ---------------------------------------------


def test_missing_contract_id_field_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_repo(tmp_path)
    path = repo / _COMPUTED_RELPATH
    path.write_text(path.read_text().replace("contract_id: feature-computed\n", ""))
    with pytest.raises(OutputEventContractUnresolvableError, match="did not resolve a complete"):
        resolve_output_event_contract_authority_from_repository("v1.0", "v1.0", repo_root=repo)


def test_missing_status_field_fails_closed(tmp_path: Path) -> None:
    repo = _write_fake_repo(tmp_path)
    path = repo / _COMPUTED_RELPATH
    path.write_text(path.read_text().replace("status: Published\n", ""))
    with pytest.raises(OutputEventContractUnresolvableError, match="did not resolve a complete"):
        resolve_output_event_contract_authority_from_repository("v1.0", "v1.0", repo_root=repo)


# --- P3-FEATURE-QG-COV-01-style residual: `_find_repo_root` --------------


def test_find_repo_root_raises_when_no_docs_ancestor_exists(tmp_path: Path) -> None:
    start = tmp_path / "definitely" / "not" / "a" / "repository" / "checkout"
    with pytest.raises(OutputEventContractUnresolvableError) as excinfo:
        _find_repo_root(start)
    message = str(excinfo.value)
    assert message.startswith(f"could not locate repository root (no {'docs'!r} directory found above {start!r}) — ")
    assert message.endswith("outbound Event Contract authority cannot be resolved from the filesystem")


# --- Provider wrappers -------------------------------------------------------


def test_filesystem_resolver_delegates_to_module_function(tmp_path: Path) -> None:
    repo = _write_fake_repo(tmp_path)
    resolver = FilesystemOutputEventContractAuthorityResolver(
        computed_contract_version="v1.0", invalidated_contract_version="v1.0", repo_root=repo
    )
    resolved = resolver.resolve()
    direct = resolve_output_event_contract_authority_from_repository("v1.0", "v1.0", repo_root=repo)
    assert resolved == direct


def test_static_provider_returns_wrapped_authority() -> None:
    provider = StaticOutputEventContractAuthorityProvider(OUTPUT_EVENT_CONTRACT_AUTHORITY)
    assert provider.resolve() is OUTPUT_EVENT_CONTRACT_AUTHORITY


# --- No public constructor for VerifiedOutputEventContractAuthority ---------


def test_verified_output_authority_has_no_public_constructor() -> None:
    with pytest.raises(TypeError):
        VerifiedOutputEventContractAuthority(
            computed_contract_ref=EventContractRef("feature-computed", "v1.0"),
            invalidated_contract_ref=EventContractRef("feature-fact-invalidated", "v1.0"),
        )
