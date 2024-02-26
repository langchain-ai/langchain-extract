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


def convert_json_schema_to_openai_schema(
    schema: dict,
    *,
    rm_titles: bool = True,
    multi: bool = True,
) -> dict:
    """Convert JSON schema to a corresponding OpenAI function call."""
    if multi:
        # Wrap the schema in an object called "Root" with a property called: "data"
        # which will be a json array of the original schema.
        schema_ = {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": schema,
                },
            },
            "required": ["data"],
        }
    else:
        raise NotImplementedError("Only multi is supported for now.")

    schema_ = dereference_refs(schema_)
    schema_.pop("definitions", None)

    return {
        "name": "extractor",
        "description": "Extract information matching the given schema.",
        "parameters": _rm_titles(schema_) if rm_titles else schema_,
    }
