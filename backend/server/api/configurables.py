"""Endpoint for listing available chat models for extraction."""
from typing import List

from fastapi import APIRouter
from typing_extensions import TypedDict

from extraction.parsing import MAX_FILE_SIZE_MB, SUPPORTED_MIMETYPES
from server.models import SUPPORTED_MODELS
from server.settings import MAX_CHUNKS, MAX_CONCURRENCY

router = APIRouter(
    prefix="/configuration",
    tags=["Configuration"],
    responses={404: {"description": "Not found"}},
)


class ConfigurationResponse(TypedDict):
    """Response for configuration."""

    available_models: List[str]
    accepted_mimetypes: List[str]
    max_file_size_mb: int
    max_concurrency: int
    max_chunks: int
    models: List[dict]


@router.get("")
def get() -> ConfigurationResponse:
    """Endpoint to show server configuration."""
    return {
        "available_models": sorted(SUPPORTED_MODELS),  # Deprecate
        "models": [
            {
                "name": model,
                "description": data["description"],
            }
            for model, data in SUPPORTED_MODELS.items()
        ],
        "accepted_mimetypes": SUPPORTED_MIMETYPES,
        "max_file_size_mb": MAX_FILE_SIZE_MB,
        "max_concurrency": MAX_CONCURRENCY,
        "max_chunks": MAX_CHUNKS,
    }
