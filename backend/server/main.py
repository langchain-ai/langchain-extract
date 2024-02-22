"""Entry point into the server."""
from typing import Literal
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from langserve import add_routes
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing_extensions import Annotated, TypedDict

from db.models import Extractor, get_session
from extraction.utils import get_examples_from_extractor
from server.api import examples, extractors
from server.extraction_runnable import (
    ExtractRequest,
    ExtractResponse,
    extraction_runnable,
)
from server.retrieval import extract_from_content

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


class ExtractFromFileRequest(BaseModel):
    extractor_id: UUID = Field(..., description="The extractor ID to use.")
    text: str = Field(..., description="The text to extract from.")
    mode: Literal["entire_document", "retrieval"] = Field(
        "entire_document", description="The mode of extraction."
    )


@app.post("/extract", response_model=ExtractResponse, tags=["extraction"])
async def extract_using_existing_extractor(
    extract_request: ExtractFromFileRequest,
    *,
    session: Session = Depends(get_session),
) -> ExtractResponse:
    """Endpoint that is used with an existing extractor.

    This endpoint will be expanded to support upload of binary files as well as
    text files.
    """
    extractor = (
        session.query(Extractor)
        .filter(Extractor.uuid == extract_request.extractor_id)
        .scalar()
    )
    if extractor is None:
        raise HTTPException(status_code=404, detail="Extractor not found.")

    mode = extract_request.mode
    if mode == "entire_document":
        json_schema = extractor.schema
        examples = get_examples_from_extractor(extractor)
        extraction_request = ExtractRequest(
            text=extract_request.text,
            schema=json_schema,
            instructions=extractor.instruction,  # TODO: consistent naming
            examples=examples,
        )
        return await extraction_runnable.ainvoke(extraction_request)
    elif mode == "retrieval":
        return await extract_from_content(
            extract_request.text, extractor, text_splitter_kwargs=None
        )
    else:
        raise ValueError(
            f"Invalid mode {mode}. Expected one of 'entire_document', " "'retrieval'."
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
