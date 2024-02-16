from typing import List

from langchain.pydantic_v1 import BaseModel, Field

from extraction.utils import convert_json_schema_to_openai_schema


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
