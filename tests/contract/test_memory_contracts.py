from uuid import uuid4

import pytest
from pydantic import ValidationError

from core.contracts import (
    ConversationRecord,
    MemoryItem,
    MemoryScope,
    MessageRecord,
    MessageRole,
    SensitivityLevel,
    export_contract_schemas,
)


def test_conversation_and_message_are_tenant_scoped():
    tenant_id = uuid4()
    conversation = ConversationRecord(
        conversation_id=uuid4(),
        tenant_id=tenant_id,
        user_id=uuid4(),
        title="Support chat",
    )
    message = MessageRecord(
        message_id=uuid4(),
        conversation_id=conversation.conversation_id,
        tenant_id=tenant_id,
        role=MessageRole.USER,
        content="hello",
    )

    assert conversation.tenant_id == message.tenant_id
    assert message.role == MessageRole.USER


def test_memory_is_not_training_data_by_default_and_requires_evidence():
    memory = MemoryItem(
        memory_id=uuid4(),
        tenant_id=uuid4(),
        scope=MemoryScope.USER,
        key="preferred_language",
        value={"language": "ar"},
        source="conversation",
        confidence=0.9,
        evidence_count=2,
    )

    assert memory.training_eligible is False
    assert memory.evidence_count == 2
    assert "MemoryItem" in export_contract_schemas()


def test_secret_memory_cannot_be_training_eligible():
    with pytest.raises(ValidationError):
        MemoryItem(
            memory_id=uuid4(),
            tenant_id=uuid4(),
            scope=MemoryScope.USER,
            key="api_key",
            value={"secret": "redacted"},
            source="manual",
            confidence=1.0,
            evidence_count=1,
            sensitivity=SensitivityLevel.SECRET,
            training_eligible=True,
        )


def test_memory_contracts_reject_unknown_fields():
    with pytest.raises(ValidationError):
        MessageRecord(
            message_id=uuid4(),
            conversation_id=uuid4(),
            tenant_id=uuid4(),
            role=MessageRole.SYSTEM,
            content="x",
            extra="not allowed",  # type: ignore[call-arg]
        )
