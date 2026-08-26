"""Core domain contract types.

These are intentionally small initial contracts for MVP Phase 1. They capture
stable identities and execution status shared by later API, routing, provider,
and audit contracts without importing implementation modules.
"""

from __future__ import annotations

from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class FrozenContract(BaseModel):
    """Base class for immutable public contract objects."""

    model_config = ConfigDict(frozen=True, extra="forbid")


class TenantType(StrEnum):
    PERSONAL = "personal"
    ORGANIZATION = "organization"


class ExecutionStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TenantRef(FrozenContract):
    tenant_id: UUID = Field(description="Tenant identifier that scopes all owned data.")
    tenant_type: TenantType = Field(default=TenantType.PERSONAL)


class UserRef(FrozenContract):
    user_id: UUID
    tenant_id: UUID
    email: str | None = Field(default=None, description="Optional user email; not trusted as auth.")


class ProjectRef(FrozenContract):
    project_id: UUID
    tenant_id: UUID
    workspace_id: UUID | None = None


class ConversationRef(FrozenContract):
    conversation_id: UUID
    tenant_id: UUID
    project_id: UUID | None = None


class ExecutionRef(FrozenContract):
    execution_id: UUID
    tenant_id: UUID
    status: ExecutionStatus


class ActorRef(FrozenContract):
    """Actor identity passed to authorization and audit contracts."""

    actor_type: str = Field(pattern="^(user|system|service)$")
    actor_id: UUID | None = None
    tenant_id: UUID | None = None
