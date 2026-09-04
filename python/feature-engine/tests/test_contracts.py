from __future__ import annotations

import pytest

from feature_engine import (
    FEATURE_COMPUTED_CONTRACT_ID,
    FEATURE_FACT_INVALIDATED_CONTRACT_ID,
    EventContractRef,
    UnresolvedOutputContractAuthorityError,
    resolve_output_contract_refs,
)

# P3-PY-MUT-STEP9-A field-completeness remediation (EVID-03,
# constructed_object_field_not_independently_asserted): `resolve_output_
# contract_refs` is the single place every computation engine resolves its
# own outbound `(FeatureComputed, FeatureFactInvalidated)` `event_contract_
# ref`s -- every existing test file only ever imports the two contract-ID
# constants to build its OWN expected refs by hand, never calling this
# function directly and asserting its actual return value. This is a direct
# unit test of the function itself.


def test_resolve_output_contract_refs_returns_genuine_pinned_identities() -> None:
    computed_ref, invalidated_ref = resolve_output_contract_refs("fv1")
    assert computed_ref == EventContractRef(FEATURE_COMPUTED_CONTRACT_ID, "fv1")
    assert invalidated_ref == EventContractRef(FEATURE_FACT_INVALIDATED_CONTRACT_ID, "fv1")
    assert computed_ref.contract_id == FEATURE_COMPUTED_CONTRACT_ID
    assert computed_ref.contract_version == "fv1"
    assert invalidated_ref.contract_id == FEATURE_FACT_INVALIDATED_CONTRACT_ID
    assert invalidated_ref.contract_version == "fv1"


def test_resolve_output_contract_refs_different_version_produces_different_refs() -> None:
    computed_v1, invalidated_v1 = resolve_output_contract_refs("fv1")
    computed_v2, invalidated_v2 = resolve_output_contract_refs("fv2")
    assert computed_v1 != computed_v2
    assert invalidated_v1 != invalidated_v2
    assert computed_v1.contract_id == computed_v2.contract_id
    assert invalidated_v1.contract_id == invalidated_v2.contract_id


def test_resolve_output_contract_refs_empty_version_fails_closed() -> None:
    with pytest.raises(UnresolvedOutputContractAuthorityError):
        resolve_output_contract_refs("")
