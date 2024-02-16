"""Entry point into the server."""
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from jsonschema import Draft202012Validator, exceptions
from langchain.chains.openai_functions import create_openai_fn_runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import chain
from langchain_openai.chat_models import ChatOpenAI
from langserve import add_routes
from pydantic import BaseModel, Field

from extraction.utils import convert_json_schema_to_openai_schema

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


class ExtractRequest(BaseModel):
    """Request body for the extract endpoint."""

    text: str = Field(..., description="The text to extract from.")
    json_schema: Dict[str, Any] = Field(
        ...,
        description="JSON schema that describes what content should be extracted "
        "from the text.",
        alias="schema",
    )


class ExtractResponse(BaseModel):
    """Response body for the extract endpoint."""

    extracted: Any


# class CreateExtractor(BaseModel):
#     """Request body for the create_extractor endpoint."""
#
#     schema: Dict[str, Any] = Field(..., description="The schema to use for extraction.")
#     instruction: str = Field(..., description="The instruction to use for extraction.")
#

model = ChatOpenAI(temperature=0)


@chain
def extraction_runnable(extraction_request: ExtractRequest) -> ExtractResponse:
    schema = extraction_request["json_schema"]
    try:
        Draft202012Validator.check_schema(schema)
    except exceptions.ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Invalid schema: {e.message}")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a top-tier algorithm for extracting information from text. "
                "Only extract information that is relevant to the provided text. "
                "If no information is relevant, use the schema and output "
                "an empty list where appropriate.",
            ),
            (
                "human",
                "I need to extract information from the following text: ```\n{text}\n```\n",
            ),
        ]
    )

    openai_function = convert_json_schema_to_openai_schema(schema)
    runnable = create_openai_fn_runnable(
        functions=[openai_function], llm=model, prompt=prompt
    )
    extracted_content = runnable.invoke({"text": extraction_request["text"]})
    return ExtractResponse(
        extracted=extracted_content,
    )


add_routes(
    app,
    extraction_runnable,
    path="/extract_runnable",
    enabled_endpoints=["invoke", "playground", "stream_log"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
