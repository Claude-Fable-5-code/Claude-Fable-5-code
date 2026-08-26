"""Conversation, message, and memory contracts.

Memory is scoped, evidence-bearing, and not training data by default.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MemoryContractModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class ConversationStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class MemoryScope(StrEnum):
    GLOBAL = "global"
    TENANT = "tenant"
    WORKSPACE = "workspace"
    PROJECT = "project"
    CONVERSATION = "conversation"
    USER = "user"
    ROLE = "role"


class SensitivityLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    SECRET = "secret"


class ConversationRecord(MemoryContractModel):
    conversation_id: UUID
    tenant_id: UUID
    user_id: UUID
    project_id: UUID | None = None
    title: str | None = None
    status: ConversationStatus = ConversationStatus.ACTIVE


class MessageRecord(MemoryContractModel):
    message_id: UUID
    conversation_id: UUID
    tenant_id: UUID
    role: MessageRole
    content: str | dict[str, Any]
    attachments: list[dict[str, Any]] = Field(default_factory=list)
    created_at_unix_ms: int | None = Field(default=None, ge=0)


class MemoryItem(MemoryContractModel):
    memory_id: UUID
    tenant_id: UUID
    scope: MemoryScope
    key: str = Field(min_length=1)
    value: dict[str, Any]
    source: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_count: int = Field(ge=1)
    sensitivity: SensitivityLevel = SensitivityLevel.LOW
    training_eligible: bool = False

    @model_validator(mode="after")
    def secret_memory_cannot_be_training_eligible(self) -> "MemoryItem":
        if self.sensitivity == SensitivityLevel.SECRET and self.training_eligible:
            raise ValueError("secret memory cannot be training eligible")
        return self


class ContextBlock(MemoryContractModel):
    type: str = Field(min_length=1)
    content: str
    source_ref: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
