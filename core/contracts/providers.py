"""Provider, model, account, and capability contracts.

These contracts preserve the critical separation:
Model != Provider != Account != Credential.
Providers are capability-driven and implement only declared operations.
"""

from __future__ import annotations

from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProviderContractModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class Modality(StrEnum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    CODE = "code"
    FILE = "file"


class CapabilityId(StrEnum):
    TEXT_GENERATION = "text_generation"
    REASONING = "reasoning"
    CODING = "coding"
    VISION_INPUT = "vision_input"
    IMAGE_GENERATION = "image_generation"
    AUDIO_STT = "audio_stt"
    AUDIO_TTS = "audio_tts"
    EMBEDDINGS = "embeddings"
    RERANK = "rerank"
    MODERATION = "moderation"
    FILE_UPLOAD = "file_upload"
    STREAMING = "streaming"
    PROVIDER_AGENT = "provider_agent"


class ProviderStatus(StrEnum):
    ACTIVE = "active"
    DISABLED = "disabled"
    MAINTENANCE = "maintenance"
    TEMPLATE_DISABLED = "template_disabled"


class ProviderHealthStatus(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    SUSPENDED = "suspended"
    UNKNOWN = "unknown"


class AccountLifecycleState(StrEnum):
    PENDING = "pending"
    READY = "ready"
    IN_USE = "in_use"
    COOLDOWN = "cooldown"
    REFRESH_REQUIRED = "refresh_required"
    AUTH_EXPIRED = "auth_expired"
    RATE_LIMITED = "rate_limited"
    VERIFICATION_REQUIRED = "verification_required"
    INVALID = "invalid"
    DISABLED = "disabled"


class CredentialOwnerType(StrEnum):
    PLATFORM = "platform"
    TENANT = "tenant"
    USER = "user"


class ProviderRef(ProviderContractModel):
    provider_id: str = Field(min_length=1)
    display_name: str
    status: ProviderStatus
    capabilities: set[CapabilityId] = Field(default_factory=set)
    modalities: set[Modality] = Field(default_factory=set)
    is_template: bool = False
    is_functional: bool = True


class ModelRef(ProviderContractModel):
    model_id: str = Field(min_length=1)
    display_name: str
    tier: str | None = None
    capabilities: set[CapabilityId] = Field(default_factory=set)
    modalities: set[Modality] = Field(default_factory=set)


class ProviderModelBinding(ProviderContractModel):
    provider_id: str
    model_id: str
    provider_model_name: str
    capabilities: set[CapabilityId] = Field(default_factory=set)
    availability: ProviderHealthStatus = ProviderHealthStatus.UNKNOWN


class CredentialRef(ProviderContractModel):
    credential_id: UUID
    owner_type: CredentialOwnerType
    owner_id: UUID | None = None
    provider_id: str
    credential_ref: str = Field(min_length=1, description="Opaque secret-manager reference.")


class ProviderAccountRef(ProviderContractModel):
    account_id: UUID
    provider_id: str
    credential_id: UUID
    owner_type: CredentialOwnerType
    lifecycle_state: AccountLifecycleState
    health_state: ProviderHealthStatus = ProviderHealthStatus.UNKNOWN


class ProviderHealth(ProviderContractModel):
    provider_id: str
    status: ProviderHealthStatus
    message: str | None = None
    checked_at_unix_ms: int | None = Field(default=None, ge=0)
