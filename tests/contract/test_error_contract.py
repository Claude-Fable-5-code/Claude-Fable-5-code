import pytest
from pydantic import ValidationError

from core.contracts import ErrorCode, ErrorDetail, ErrorResponse, ErrorSeverity


def test_error_response_schema_exports_public_error_shape():
    schema = ErrorResponse.model_json_schema()

    assert schema["type"] == "object"
    assert set(schema["required"]) >= {"code", "message", "retryable"}
    assert "details" in schema["properties"]


def test_capability_denied_helper_is_safe_and_non_retryable():
    error = ErrorResponse.capability_denied(
        "Tool is not allowed", trace_id="trace-1", capability="github.pr.merge"
    )

    assert error.code == ErrorCode.CAPABILITY_DENIED
    assert error.retryable is False
    assert error.severity == ErrorSeverity.ERROR
    assert error.details == [ErrorDetail(field="capability", reason="github.pr.merge")]


def test_error_response_rejects_unknown_fields_and_codes():
    with pytest.raises(ValidationError):
        ErrorResponse(
            code="not_a_code",
            message="bad",
            retryable=False,
        )

    with pytest.raises(ValidationError):
        ErrorResponse(
            code=ErrorCode.INTERNAL_ERROR,
            message="bad",
            retryable=True,
            secret="must not be accepted",  # type: ignore[call-arg]
        )
