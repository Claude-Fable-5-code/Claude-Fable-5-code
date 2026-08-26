import json

from core.contracts import CONTRACT_MODELS, ExecuteRequest, export_contract_schemas, write_contract_schemas


def test_export_contract_schemas_is_deterministic_and_complete():
    schemas = export_contract_schemas()

    assert list(schemas) == sorted(schemas)
    assert set(CONTRACT_MODELS) <= set(schemas)
    assert schemas["ExecuteRequest"] == ExecuteRequest.model_json_schema()
    assert schemas["ExecuteResponse"]["type"] == "object"


def test_write_contract_schemas_writes_json_files(tmp_path):
    written = write_contract_schemas(tmp_path)

    assert written
    names = {path.name for path in written}
    assert "ExecuteRequest.schema.json" in names
    assert "ErrorResponse.schema.json" in names

    loaded = json.loads((tmp_path / "ExecuteRequest.schema.json").read_text(encoding="utf-8"))
    assert "ask" in loaded["required"]
