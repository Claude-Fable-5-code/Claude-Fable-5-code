"""/v1/execute API contract models.

Initial MVP contracts for task submission and response envelopes. These models
preserve the public API direction in final_docs_v3/10_API_CONTRACTS.md while
remaining independent from runtime implementation.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from .domain import ExecutionStatus
from .errors import ErrorResponse


class ContractModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class ExecutionMode(StrEnum):
    AUTO = "auto"
    DIRECT = "direct"
    AGENT = "agent"


class ModelPolicyType(StrEnum):
    AUTO = "auto"
    TIER = "tier"
    EXPLICIT_MODEL = "explicit_model"
    EXPLICIT_MODELS = "explicit_models"
    AGENT_NODE_MAPPING = "agent_node_mapping"


class ExecutionStrategy(StrEnum):
    AUTO = "auto"
    SINGLE = "single"
    PARALLEL = "parallel"
    PIPELINE = "pipeline"
    DEBATE = "debate"
    REVIEW_JUDGE = "review_judge"
    MAP_REDUCE = "map_reduce"
    AGENT = "agent"
    HYBRID = "hybrid"


class OutputFormat(StrEnum):
    MARKDOWN = "markdown"
    JSON = "json"
    TEXT = "text"


class ModelPolicy(ContractModel):
    type: ModelPolicyType = ModelPolicyType.AUTO
    tier: str | None = None
    model_id: str | None = None
    models: list[dict[str, str | None]] = Field(default_factory=list)
    selection_strategy: str | None = None
    allow_fallback: bool = True
    fallback_scope: str | None = None


class ExecutionPolicy(ContractModel):
    strategy: ExecutionStrategy = ExecutionStrategy.AUTO
    async_execution: bool = Field(default=False, alias="async")
    stream: bool = False
    max_cost_units: int | None = Field(default=None, ge=1)
    approval_required_for_tools: bool = True


class ToolPolicy(ContractModel):
    allowed: list[str] = Field(default_factory=list)
    denied: list[str] = Field(default_factory=list)
    approval_mode: str = "before_write"


class ExecuteContext(ContractModel):
    attachments: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    language: str | None = None


class OutputPolicy(ContractModel):
    format: OutputFormat = OutputFormat.MARKDOWN
    language: str | None = None
    schema_: dict[str, Any] | None = Field(default=None, alias="schema")


class ExecuteRequest(ContractModel):
    ask: str = Field(min_length=1)
    mode: ExecutionMode = ExecutionMode.AUTO
    conversation_id: UUID | None = None
    project_id: UUID | None = None
    role: dict[str, str] | None = None
    model_policy: ModelPolicy = Field(default_factory=ModelPolicy)
    execution_policy: ExecutionPolicy = Field(default_factory=ExecutionPolicy)
    tools: ToolPolicy = Field(default_factory=ToolPolicy)
    context: ExecuteContext = Field(default_factory=ExecuteContext)
    output: OutputPolicy = Field(default_factory=OutputPolicy)
    webhook_url: HttpUrl | None = None


class UsageSummary(ContractModel):
    units_reserved: int | None = None
    units_settled: int | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class EvaluationSummary(ContractModel):
    visible: bool = False
    level: str | None = None
    summary: str | None = None


class ExecuteResult(ContractModel):
    type: str = "message"
    content: str | dict[str, Any]
    format: OutputFormat = OutputFormat.MARKDOWN
    artifacts: list[dict[str, Any]] = Field(default_factory=list)


class ExecuteResponse(ContractModel):
    execution_id: UUID
    status: ExecutionStatus
    result: ExecuteResult | None = None
    usage: UsageSummary | None = None
    evaluation: EvaluationSummary | None = None
    error: ErrorResponse | None = None
