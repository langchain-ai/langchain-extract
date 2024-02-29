from typing import Any, Dict

from fastapi import HTTPException
from jsonschema import exceptions
from jsonschema.validators import Draft202012Validator


def validate_json_schema(schema: Dict[str, Any]) -> None:
    """Validate a JSON schema."""
    try:
        Draft202012Validator.check_schema(schema)
    except exceptions.ValidationError as e:
        raise HTTPException(
            status_code=422, detail=f"Not a valid JSON schema: {e.message}"
        )
