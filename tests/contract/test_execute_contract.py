from uuid import uuid4

import pytest
from pydantic import ValidationError

from core.contracts import (
    ErrorCode,
    ErrorResponse,
    ExecuteRequest,
    ExecuteResponse,
    ExecuteResult,
    ExecutionMode,
    ExecutionStatus,
    ModelPolicyType,
)


def test_execute_request_defaults_and_schema_export():
    request = ExecuteRequest(ask="Review this code", mode=ExecutionMode.AGENT)
    schema = ExecuteRequest.model_json_schema()

    assert request.model_policy.type == ModelPolicyType.AUTO
    assert request.execution_policy.approval_required_for_tools is True
    assert schema["type"] == "object"
    assert "ask" in schema["required"]
    assert "model_policy" in schema["properties"]


def test_execute_request_rejects_empty_ask_and_unknown_fields():
    with pytest.raises(ValidationError):
        ExecuteRequest(ask="")

    with pytest.raises(ValidationError):
        ExecuteRequest(ask="hello", hidden="field")  # type: ignore[call-arg]


def test_execute_response_supports_success_and_error_envelopes():
    execution_id = uuid4()
    success = ExecuteResponse(
        execution_id=execution_id,
        status=ExecutionStatus.SUCCEEDED,
        result=ExecuteResult(content="done"),
    )
    failure = ExecuteResponse(
        execution_id=execution_id,
        status=ExecutionStatus.FAILED,
        error=ErrorResponse(
            code=ErrorCode.EXECUTION_FAILED,
            message="failed",
            retryable=False,
        ),
    )

    assert success.result is not None
    assert failure.error is not None
    assert ExecuteResponse.model_json_schema()["type"] == "object"
