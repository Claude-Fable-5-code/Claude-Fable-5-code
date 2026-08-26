from uuid import uuid4

import pytest
from pydantic import ValidationError

from core.contracts import ActorRef, ExecutionRef, ExecutionStatus, TenantRef, TenantType, UserRef


def test_tenant_ref_is_immutable_and_schema_exportable():
    tenant = TenantRef(tenant_id=uuid4(), tenant_type=TenantType.PERSONAL)
    schema = TenantRef.model_json_schema()

    assert schema["type"] == "object"
    assert "tenant_id" in schema["properties"]
    with pytest.raises(ValidationError):
        TenantRef(tenant_id=tenant.tenant_id, unexpected=True)  # type: ignore[call-arg]


def test_user_and_execution_refs_keep_tenant_scope():
    tenant_id = uuid4()
    user = UserRef(user_id=uuid4(), tenant_id=tenant_id, email="user@example.com")
    execution = ExecutionRef(
        execution_id=uuid4(), tenant_id=tenant_id, status=ExecutionStatus.QUEUED
    )

    assert user.tenant_id == execution.tenant_id
    assert execution.status == ExecutionStatus.QUEUED


def test_actor_ref_rejects_unknown_actor_type():
    with pytest.raises(ValidationError):
        ActorRef(actor_type="provider", actor_id=uuid4(), tenant_id=uuid4())
