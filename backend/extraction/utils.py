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
    schema: dict, *, name: str = "", description: str = "", rm_titles: bool = True
) -> dict:
    """Convert JSON schema to a corresponding OpenAI function call."""
    schema = dereference_refs(schema)
    schema.pop("definitions", None)
    title = schema.pop("title", "")
    default_description = schema.pop("description", "")
    return {
        "name": name or title,
        "description": description or default_description,
        "parameters": _rm_titles(schema) if rm_titles else schema,
    }
