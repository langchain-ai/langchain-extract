from typing import List

from langchain.pydantic_v1 import BaseModel, Field

from extraction.utils import (
    FewShotExample,
    convert_json_schema_to_openai_schema,
    make_system_message,
)


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
        "description": "",
        "name": "Person",
        "parameters": {
            "properties": {
                "age": {"description": "The age of the person.", "type": "integer"},
                "name": {"description": "The name of the " "person.", "type": "string"},
            },
            "required": ["name", "age"],
            "type": "object",
        },
    }

    class People(BaseModel):
        """A list of people with names and ages."""

        people: List[Person] = Field(..., description="A list of people.")

    assert convert_json_schema_to_openai_schema(People.schema()) == {
        "description": "A list of people with names and ages.",
        "name": "People",
        "parameters": {
            "properties": {
                "people": {
                    "description": "A list of people.",
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
            "required": ["people"],
            "type": "object",
        },
    }


def test_make_system_message() -> None:
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
    system_message = make_system_message(instructions, examples)
    examples_str = (
        '\{{"text": "Test text.", '
        '"output": [\{{"name": "Test Name", "age": 0\}}, '
        '\{{"name": "Test Name 2", "age": 1\}}]\}}'
    )
    assert f"{prefix}\n\nTest instructions.\n\n{examples_str}" == system_message

    system_message = make_system_message(None, None)
    assert prefix == system_message

    system_message = make_system_message(instructions, None)
    assert f"{prefix}\n\nTest instructions." == system_message

    system_message = make_system_message(None, examples)
    assert f"{prefix}\n\n{examples_str}" == system_message

    examples = [FewShotExample(text="Test text.", output=[])]
    system_message = make_system_message(None, examples)
    examples_str = '\\{{"text": "Test text.", "output": []\\}}'
    assert f"{prefix}\n\n{examples_str}" == system_message
