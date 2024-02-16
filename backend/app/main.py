"""Entry point into the app."""
from typing import Dict, Any

from fastapi import FastAPI
from langchain_openai.chat_models import ChatOpenAI
from pydantic import BaseModel, Field

app = FastAPI()

class ExtractRequest(BaseModel):
    """Request body for the extract endpoint."""
    text: str = Field(..., description="The text to extract from.")
    schema: Dict[str, Any] = Field(..., description="The schema to use for extraction.")

class ExtractResponse(BaseModel):
    """Response body for the extract endpoint."""
    raw_output: str
    extracted: Dict[str, Any]


model = ChatOpenAI()

@app.post("/extract_from_text")
def extract(extract_request: ExtractRequest) -> ExtractResponse:
    """An end point to extract content from a given text object."""
    return {
        "raw_output": "output from the model",
        "extracted": {"extracted": "content"}
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
