"""Entry point into the server."""
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from jsonschema import Draft202012Validator, exceptions
from langchain.chains.openai_functions import create_openai_fn_runnable
from langchain_core.runnables import chain
from langchain_openai.chat_models import ChatOpenAI
from langserve import CustomUserType, add_routes
from pydantic import BaseModel, Field, validator

from extraction.utils import (
    FewShotExample,
    convert_json_schema_to_openai_schema,
    make_prompt_template,
)
from server.api import examples, extractors
from server.validators import validate_json_schema

app = FastAPI(
    title="Extraction Powered by LangChain",
    description="An extraction service powered by LangChain.",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "extraction",
            "description": "Operations related to extracting content from text.",
        }
    ],
)

# Include API endpoints for extractor definitions
app.include_router(extractors.router)
app.include_router(examples.router)


class ExtractRequest(CustomUserType):
    """Request body for the extract endpoint."""

    text: str = Field(..., description="The text to extract from.")
    json_schema: Dict[str, Any] = Field(
        ...,
        description="JSON schema that describes what content should be extracted "
        "from the text.",
        alias="schema",
    )
    instructions: Optional[str] = Field(
        None, description="Supplemental system instructions."
    )
    examples: Optional[List[FewShotExample]] = Field(
        None, description="Few shot examples."
    )

    @validator("json_schema")
    def validate_schema(cls, v: Any) -> Dict[str, Any]:
        """Validate the schema."""
        validate_json_schema(v)
        return v


class ExtractResponse(BaseModel):
    """Response body for the extract endpoint."""

    extracted: Any


model = ChatOpenAI(temperature=0)


@chain
def extraction_runnable(extraction_request: ExtractRequest) -> ExtractResponse:
    """An end point to extract content from a given text object."""
    schema = extraction_request.json_schema
    name = schema.get("title", "")
    try:
        Draft202012Validator.check_schema(schema)
    except exceptions.ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Invalid schema: {e.message}")

    prompt = make_prompt_template(
        extraction_request.instructions, extraction_request.examples, name
    )
    openai_function = convert_json_schema_to_openai_schema(schema)
    runnable = create_openai_fn_runnable(
        functions=[openai_function], llm=model, prompt=prompt
    )
    extracted_content = runnable.invoke({"text": extraction_request.text})

    return ExtractResponse(
        extracted=extracted_content,
    )


add_routes(
    app,
    extraction_runnable,
    path="/extract_text",
    enabled_endpoints=["invoke", "playground", "stream_log"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
