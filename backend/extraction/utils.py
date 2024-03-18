"""Adapters to convert between different formats."""
from __future__ import annotations

from langchain_core.utils.json_schema import dereference_refs


def _rm_titles(kv: dict) -> dict:
    """Remove titles from a dictionary."""
    new_kv = {}
    for k, v in kv.items():
        if k == "title":
            continue
        elif isinstance(v, dict):
            new_kv[k] = _rm_titles(v)
        else:
            new_kv[k] = v
    return new_kv


# PUBLIC API


def update_json_schema(
    schema: dict,
    *,
    multi: bool = True,
) -> dict:
    """Add missing fields to JSON schema and add support for multiple records."""
    if multi:
        # Wrap the schema in an object called "Root" with a property called: "data"
        # which will be a json array of the original schema.
        schema_ = {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": dereference_refs(schema),
                },
            },
            "required": ["data"],
        }
    else:
        raise NotImplementedError("Only multi is supported for now.")

    schema_["title"] = "extractor"
    schema_["description"] = "Extract information matching the given schema."
    return schema_
