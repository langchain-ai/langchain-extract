from typing import List

import pytest
from langchain.pydantic_v1 import BaseModel, Field

from extraction.utils import (
    convert_json_schema_to_openai_schema,
)
from server.extraction_runnable import FewShotExample, _make_prompt_template


def test_convert_json_schema_to_openai_schema() -> None:
    """Test converting a JSON schema to an OpenAI schema."""

    class Person(BaseModel):
        name: str = Field(..., description="The name of the person.")
        age: int = Field(..., description="The age of the person.")

    schema = Person.schema()

    assert schema == {
        "properties": {
            "age": {
                "description": "The age of the person.",
                "title": "Age",
                "type": "integer",
            },
            "name": {
                "description": "The name of the person.",
                "title": "Name",
                "type": "string",
            },
        },
        "required": ["name", "age"],
        "title": "Person",
        "type": "object",
    }

    openai_schema = convert_json_schema_to_openai_schema(schema)
    assert openai_schema == {
        "description": "Extract information matching the given schema.",
        "name": "extractor",
        "parameters": {
            "properties": {
                "data": {
                    "items": {
                        "properties": {
                            "age": {
                                "description": "The age of the person.",
                                "type": "integer",
                            },
                            "name": {
                                "description": "The name of the person.",
                                "type": "string",
                            },
                        },
                        "required": ["name", "age"],
                        "type": "object",
                    },
                    "type": "array",
                }
            },
            "required": ["data"],
            "type": "object",
        },
    }


def test_make_prompt_template() -> None:
    """Test making a system message from instructions and examples."""
    instructions = "Test instructions."
    examples = [
        FewShotExample(
            text="Test text.",
            output=[
                {"name": "Test Name", "age": 0},
                {"name": "Test Name 2", "age": 1},
            ],
        )
    ]
    prefix = (
        "You are a top-tier algorithm for extracting information from text. "
        "Only extract information that is relevant to the provided text. "
        "If no information is relevant, use the schema and output "
        "an empty list where appropriate."
    )
    prompt = _make_prompt_template(instructions, examples, "name")
    messages = prompt.messages
    assert 4 == len(messages)
    system = messages[0].prompt.template
    assert system.startswith(prefix)
    assert system.endswith(instructions)

    example_input = messages[1]
    assert example_input.content == "Test text."
    example_output = messages[2]
    assert "function_call" in example_output.additional_kwargs
    assert example_output.additional_kwargs["function_call"]["name"] == "name"

    prompt = _make_prompt_template(instructions, None, "name")
    assert 2 == len(prompt.messages)

    prompt = _make_prompt_template(None, examples, "name")
    assert 4 == len(prompt.messages)
