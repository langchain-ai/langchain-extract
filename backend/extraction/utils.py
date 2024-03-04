"""Adapters to convert between different formats."""
from __future__ import annotations

from typing import Union

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


def convert_json_schema_to_openai_schema(
    schema: Union[dict, list],
    *,
    rm_titles: bool = True,
    multi: bool = True,
) -> dict:
    """Convert JSON schema to a corresponding OpenAI function call."""
    if not multi:
        raise NotImplementedError("Only multi is supported for now.")
    # Wrap the schema in an object called "Root" with a property called: "data"
    # which will be a json array of the original schema.
    if isinstance(schema, dict):
        schema_ = dereference_refs(schema)
    else:
        schema_ = {"anyOf": [dereference_refs(s) for s in schema]}
    params = {
        "type": "object",
        "properties": {
            "data": {
                "type": "array",
                "items": schema_,
            },
        },
        "required": ["data"],
    }

    return {
        "name": "query_analyzer",
        "description": "Generate optimized queries matching the given schema.",
        "parameters": _rm_titles(params) if rm_titles else params,
    }
