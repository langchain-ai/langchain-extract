"""Adapters to convert between different formats."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.utils.json_schema import dereference_refs
from pydantic import BaseModel, Field


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
class FewShotExample(BaseModel):
    text: str = Field(..., description="The input text")
    output: Dict[str, Any] = Field(..., description="Desired output records.")


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


def make_prompt_template(
    instructions: Optional[str], examples: Optional[List[FewShotExample]]
) -> ChatPromptTemplate:
    """Make a system message from instructions and examples."""
    prefix = (
        "You are a top-tier algorithm for extracting information from text. "
        "Only extract information that is relevant to the provided text. "
        "If no information is relevant, use the schema and output "
        "an empty list where appropriate."
    )
    if instructions:
        system_message = ("system", f"{prefix}\n\n{instructions}")
    else:
        system_message = ("system", prefix)
    prompt_components = [system_message]
    if examples is not None:
        few_shot_prompt = []
        for example in examples:
            few_shot_prompt.extend(
                [
                    HumanMessage(content=example.text),
                    AIMessage(
                        content="", additional_kwargs={"function_call": example.output}
                    ),
                ]
            )
        prompt_components.extend(few_shot_prompt)

    prompt_components.append(
        (
            "human",
            "I need to extract information from "
            "the following text: ```\n{text}\n```\n",
        ),
    )
    return ChatPromptTemplate.from_messages(prompt_components)
