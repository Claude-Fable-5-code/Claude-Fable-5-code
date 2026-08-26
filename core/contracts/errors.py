"""Unified error contract.

Matches the public API direction in final_docs_v3/10_API_CONTRACTS.md:
errors are structured, retry-aware, traceable, and safe to expose.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ErrorCode(StrEnum):
    VALIDATION_ERROR = "validation_error"
    UNAUTHENTICATED = "unauthenticated"
    UNAUTHORIZED = "unauthorized"
    ENTITLEMENT_EXCEEDED = "entitlement_exceeded"
    CAPABILITY_DENIED = "capability_denied"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    MODEL_UNAVAILABLE = "model_unavailable"
    TOOL_APPROVAL_REQUIRED = "tool_approval_required"
    RATE_LIMITED = "rate_limited"
    EXECUTION_FAILED = "execution_failed"
    INTERNAL_ERROR = "internal_error"


class ErrorSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorDetail(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    field: str | None = None
    reason: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    code: ErrorCode
    message: str
    retryable: bool
    severity: ErrorSeverity = ErrorSeverity.ERROR
    trace_id: str | None = None
    details: list[ErrorDetail] = Field(default_factory=list)

    @classmethod
    def capability_denied(
        cls,
        message: str,
        *,
        trace_id: str | None = None,
        capability: str | None = None,
    ) -> "ErrorResponse":
        details = []
        if capability:
            details.append(ErrorDetail(field="capability", reason=capability))
        return cls(
            code=ErrorCode.CAPABILITY_DENIED,
            message=message,
            retryable=False,
            trace_id=trace_id,
            details=details,
        )
