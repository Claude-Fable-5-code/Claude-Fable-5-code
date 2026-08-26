"""Schema export helpers for public contract models."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypeAlias

from pydantic import BaseModel

from .domain import ActorRef, ConversationRef, ExecutionRef, ProjectRef, TenantRef, UserRef
from .errors import ErrorResponse
from .execute import ExecuteRequest, ExecuteResponse
from .memory import ContextBlock, ConversationRecord, MemoryItem, MessageRecord
from .usage import PlanRef, TaskUnitCost, UsageEstimate, UsageReservation, UsageSettlement
from .providers import (
    CredentialRef,
    ModelRef,
    ProviderAccountRef,
    ProviderHealth,
    ProviderModelBinding,
    ProviderRef,
)

ContractModel: TypeAlias = type[BaseModel]

CONTRACT_MODELS: dict[str, ContractModel] = {
    "ActorRef": ActorRef,
    "ConversationRef": ConversationRef,
    "ErrorResponse": ErrorResponse,
    "ExecuteRequest": ExecuteRequest,
    "ExecuteResponse": ExecuteResponse,
    "ExecutionRef": ExecutionRef,
    "CredentialRef": CredentialRef,
    "ContextBlock": ContextBlock,
    "ConversationRecord": ConversationRecord,
    "MemoryItem": MemoryItem,
    "MessageRecord": MessageRecord,
    "ModelRef": ModelRef,
    "ProviderAccountRef": ProviderAccountRef,
    "ProviderHealth": ProviderHealth,
    "ProviderModelBinding": ProviderModelBinding,
    "ProviderRef": ProviderRef,
    "ProjectRef": ProjectRef,
    "PlanRef": PlanRef,
    "TaskUnitCost": TaskUnitCost,
    "UsageEstimate": UsageEstimate,
    "UsageReservation": UsageReservation,
    "UsageSettlement": UsageSettlement,
    "TenantRef": TenantRef,
    "UserRef": UserRef,
}


def export_contract_schemas() -> dict[str, dict]:
    """Return deterministic JSON-schema dictionaries for public contracts."""

    return {name: CONTRACT_MODELS[name].model_json_schema() for name in sorted(CONTRACT_MODELS)}


def write_contract_schemas(output_dir: str | Path) -> list[Path]:
    """Write one JSON Schema file per public contract model.

    This is helper tooling only; generated artifacts are not required for runtime.
    """

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for name, schema in export_contract_schemas().items():
        path = destination / f"{name}.schema.json"
        path.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written.append(path)
    return written
