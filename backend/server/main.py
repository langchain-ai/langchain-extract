"""Entry point into the app."""
from typing import Any, Dict

from fastapi import FastAPI
from langchain.chains.openai_functions import create_openai_fn_runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from pydantic import BaseModel, Field

app = FastAPI()


class ExtractRequest(BaseModel):
    """Request body for the extract endpoint."""

    text: str = Field(..., description="The text to extract from.")
    schema: Dict[str, Any] = Field(
        ...,
        description="JSON schema that describes what content should be extracted "
                    "from the text."
    )


class ExtractResponse(BaseModel):
    """Response body for the extract endpoint."""

    raw_output: str
    extracted: Any


class CreateExtractor(BaseModel):
    """Request body for the create_extractor endpoint."""
    schema: Dict[str, Any] = Field(..., description="The schema to use for extraction.")
    instruction: str = Field(..., description="The instruction to use for extraction.")


model = ChatOpenAI()


@app.post("/extract_from_text")
def extract(extract_request: ExtractRequest) -> ExtractResponse:
    """An end point to extract content from a given text object."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a top-tier algorithm for extracting information from text. "
                   "Only extract information that is relevant to the provided text. "
                   "If no information is relevant, use the schema and output "
                   "an empty list where appropriate."),
        ("human", "I need to extract information from the following text: ```\n{text}\n```\n"),
    ])

    runnable = create_openai_fn_runnable(
        functions=[extract_request.schema], llm=model, prompt=prompt
    )
    extracted_content = runnable.invoke({"text": extract_request.text})
    return ExtractResponse(
        extracted=extracted_content,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
