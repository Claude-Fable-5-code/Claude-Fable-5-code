"""Usage, plan, and task-unit contracts.

Contracts only: no billing runtime, no payment integration, and no settlement
side effects. These models preserve the estimate -> reserve -> settle lifecycle.
"""

from __future__ import annotations

from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class UsageContractModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class TaskComplexity(StrEnum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


class UsageReservationStatus(StrEnum):
    ESTIMATED = "estimated"
    RESERVED = "reserved"
    SETTLED = "settled"
    REFUNDED = "refunded"
    FAILED = "failed"


class EntitlementKey(StrEnum):
    AGENT_MODE = "agent_mode"
    IMAGE_GENERATION = "image_generation"
    GITHUB_READ = "github_read"
    GITHUB_WRITE = "github_write"
    MAX_MODELS = "max_models"


class TaskUnitCost(UsageContractModel):
    complexity: TaskComplexity
    units: int = Field(ge=1)


class PlanRef(UsageContractModel):
    plan_id: str = Field(min_length=1)
    display_name: str
    task_unit_limit: int | None = Field(default=None, ge=0)
    entitlements: set[EntitlementKey] = Field(default_factory=set)


class UsageEstimate(UsageContractModel):
    tenant_id: UUID
    complexity: TaskComplexity
    estimated_units: int = Field(ge=1)
    modality_costs: dict[str, int] = Field(default_factory=dict)
    cost_snapshot: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class UsageReservation(UsageContractModel):
    reservation_id: UUID
    tenant_id: UUID
    execution_id: UUID
    units_reserved: int = Field(ge=1)
    status: UsageReservationStatus = UsageReservationStatus.RESERVED
    cost_snapshot: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class UsageSettlement(UsageContractModel):
    reservation_id: UUID
    execution_id: UUID
    units_reserved: int = Field(ge=1)
    units_settled: int = Field(ge=0)
    status: UsageReservationStatus

    @model_validator(mode="after")
    def settled_units_cannot_exceed_reserved(self) -> "UsageSettlement":
        if self.units_settled > self.units_reserved:
            raise ValueError("units_settled cannot exceed units_reserved")
        if self.status not in {
            UsageReservationStatus.SETTLED,
            UsageReservationStatus.REFUNDED,
            UsageReservationStatus.FAILED,
        }:
            raise ValueError("settlement status must be settled/refunded/failed")
        return self
