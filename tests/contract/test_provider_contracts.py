from uuid import uuid4

import pytest
from pydantic import ValidationError

from core.contracts import (
    AccountLifecycleState,
    CapabilityId,
    CredentialOwnerType,
    CredentialRef,
    Modality,
    ModelRef,
    ProviderAccountRef,
    ProviderHealthStatus,
    ProviderModelBinding,
    ProviderRef,
    ProviderStatus,
    export_contract_schemas,
)


def test_model_provider_account_are_distinct_contracts():
    provider = ProviderRef(
        provider_id="provider_x",
        display_name="Provider X",
        status=ProviderStatus.ACTIVE,
        capabilities={CapabilityId.TEXT_GENERATION},
        modalities={Modality.TEXT},
    )
    model = ModelRef(
        model_id="model_y",
        display_name="Model Y",
        capabilities={CapabilityId.TEXT_GENERATION},
        modalities={Modality.TEXT},
    )
    credential = CredentialRef(
        credential_id=uuid4(),
        owner_type=CredentialOwnerType.PLATFORM,
        provider_id=provider.provider_id,
        credential_ref="secret://provider-x/account-1",
    )
    account = ProviderAccountRef(
        account_id=uuid4(),
        provider_id=provider.provider_id,
        credential_id=credential.credential_id,
        owner_type=CredentialOwnerType.PLATFORM,
        lifecycle_state=AccountLifecycleState.READY,
        health_state=ProviderHealthStatus.HEALTHY,
    )

    assert provider.provider_id != model.model_id
    assert account.provider_id == provider.provider_id
    assert account.credential_id == credential.credential_id


def test_provider_model_binding_declares_provider_specific_model_name():
    binding = ProviderModelBinding(
        provider_id="provider_x",
        model_id="logical_model_y",
        provider_model_name="provider-y-internal-name",
        capabilities={CapabilityId.REASONING, CapabilityId.CODING},
        availability=ProviderHealthStatus.HEALTHY,
    )

    assert binding.model_id != binding.provider_model_name
    assert CapabilityId.CODING in binding.capabilities


def test_template_provider_is_non_functional_and_excluded_by_contract_flag():
    template = ProviderRef(
        provider_id="template_image_provider",
        display_name="Template Image Provider",
        status=ProviderStatus.TEMPLATE_DISABLED,
        capabilities={CapabilityId.IMAGE_GENERATION},
        modalities={Modality.IMAGE},
        is_template=True,
        is_functional=False,
    )

    assert template.is_template is True
    assert template.is_functional is False
    assert template.status == ProviderStatus.TEMPLATE_DISABLED


def test_provider_contracts_reject_unknown_fields_and_export_schema():
    with pytest.raises(ValidationError):
        ProviderRef(
            provider_id="p",
            display_name="P",
            status=ProviderStatus.ACTIVE,
            unsupported=True,  # type: ignore[call-arg]
        )

    schemas = export_contract_schemas()
    assert "ProviderRef" in schemas
    assert "ProviderModelBinding" in schemas
    assert "CredentialRef" in schemas
