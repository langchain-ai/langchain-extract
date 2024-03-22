"""Endpoint for listing available chat models for extraction."""
from typing import List

from fastapi import APIRouter
from typing_extensions import TypedDict

from extraction.parsing import MAX_CHUNK_COUNT, MAX_FILE_SIZE_MB, SUPPORTED_MIMETYPES
from server.models import SUPPORTED_MODELS

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


@router.get("")
def get() -> ConfigurationResponse:
    """Endpoint to show server configuration."""
    return {
        "available_models": sorted(SUPPORTED_MODELS),
        "accepted_mimetypes": SUPPORTED_MIMETYPES,
        "max_file_size_mb": MAX_FILE_SIZE_MB,
        "max_chunk_count": MAX_CHUNK_COUNT,
    }
