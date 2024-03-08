"""Module to handle the suggest API endpoint.

This is logic that leverages LLMs to suggest an extractor for a given task.
"""
from typing import Optional

from fastapi import APIRouter
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from server.settings import get_model

router = APIRouter(
    prefix="/suggest",
    tags=["Suggest an extractor"],
    responses={404: {"description": "Not found"}},
)


model = get_model()


class SuggestExtractor(BaseModel):
    """A request to create an extractor."""

    description: str = Field(
        default="",
        description=(
            "Short description of what  information the extractor is extracting."
        ),
    )
    jsonSchema: Optional[str] = Field(
        default=None,
        description=(
            "Existing JSON Schema that describes the entity / "
            "information that should be extracted."
        ),
    )


class ExtractorDefinition(BaseModel):
    """Define an information extractor to be used in an information extraction system."""

    name: str = Field(..., description="A human readable name for this extractor")
    json_schema: str = Field(
        ...,
        description=(
            "JSON Schema that describes the entity / information that should be extracted "
            "This schema is specified in JSON Schema format. "
        ),
    )
    description: str = Field(
        ...,
        description=(
            "Description of what information will be extracted by this extractor."
        ),
    )


SUGGEST_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are are an expert ontologist and have been asked to help a user define an information extractor."
            "The user will describe an entity, a topic or a piece of information that they would like to extract from text. "
            "Based on the user input, you are to provide a schema and description for the extractor. "
            "The schema should be a JSON Schema that describes the entity or information to be extracted. "
            "information to be extracted. "
            "Make sure to include title and description for all the attributes in the schema."
            "The JSON Schema should describe a top level object. The object MUST have a title and description."
            "Unless otherwise stated all entity properties in the schema should be considered optional.",
        ),
        ("human", "{input}"),
    ]
)

suggestion_chain = SUGGEST_PROMPT | model.with_structured_output(
    schema=ExtractorDefinition
)

UPDATE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are are an expert ontologist and have been asked to help a user define an information extractor."
            "The existing extractor schema is provided.\n"
            "```\n{json_schema}\n```\n"
            "The user will describe a desired modification to the schema (e.g., adding a new field, changing a field type, etc.)."
            "Your goal is to provide a new schema that incorporates the user's desired modification."
            "The user may also request a completely new schema, in which case you should provide a new schema based on the user's input, and "
            "ignore the existing schema."
            "The JSON Schema should describe a top level object. The object MUST have a title and description."
            "Unless otherwise stated all entity properties in the schema should be considered optional.",
        ),
        ("human", "{input}")
    ]
)

UPDATE_CHAIN = UPDATE_PROMPT | model.with_structured_output(schema=ExtractorDefinition)


# PUBLIC API


@router.post("")
async def suggest(request: SuggestExtractor) -> ExtractorDefinition:
    """Endpoint to create an extractor."""
    if len(request.jsonSchema) > 10:
        print(f"Using update chain with {request.jsonSchema}")
        return await UPDATE_CHAIN.ainvoke(
            {"input": request.description, "json_schema": request.jsonSchema}
        )
    return await suggestion_chain.ainvoke({"input": request.description})
