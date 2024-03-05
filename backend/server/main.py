"""Entry point into the server."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes

from server.api import (
    analyze,
    examples,
    extract,
    extractors,
    qa_examples,
    query_analyzers,
)
from server.extraction_runnable import (
    ExtractRequest,
    ExtractResponse,
    extraction_runnable,
)
from server.query_analysis import (
    QueryAnalysisRequest,
    QueryAnalysisResponse,
    query_analyzer,
)

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


origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ready")
def ready():
    return "ok"


# Include API endpoints for extractor definitions
app.include_router(extractors.router)
app.include_router(examples.router)
app.include_router(extract.router)

add_routes(
    app,
    extraction_runnable.with_types(
        input_type=ExtractRequest, output_type=ExtractResponse
    ),
    path="/extract_text",
    enabled_endpoints=["invoke", "batch"],
)


# Include API endpoints for extractor definitions
app.include_router(query_analyzers.router)
app.include_router(qa_examples.router)
app.include_router(analyze.router)

add_routes(
    app,
    query_analyzer.with_types(
        input_type=QueryAnalysisRequest, output_type=QueryAnalysisResponse
    ),
    path="/query_analysis",
    enabled_endpoints=["invoke", "batch"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
