"""Endpoint for listing available chat models for extraction."""
from typing import List

from fastapi import APIRouter
from typing_extensions import Annotated, TypedDict

from extraction.parsing import MAX_FILE_SIZE_MB, SUPPORTED_MIMETYPES
from server.models import SUPPORTED_MODELS

router = APIRouter(
    prefix="/configuration",
    tags=["Configuration"],
    responses={404: {"description": "Not found"}},
)


class ConfigurationResponse(TypedDict):
    """Response for configuration."""

    available_models: Annotated[List[str], "List of available models for extraction."]
    supported_mimetypes: Annotated[List[str], "List of supported mimetypes."]
    max_file_size_mb: Annotated[int, "Maximum file size in MB."]


@router.get("")
def get() -> ConfigurationResponse:
    """Endpoint to show server configuration."""
    return {
        "available_models": sorted(SUPPORTED_MODELS),
        "supported_mimetypes": SUPPORTED_MIMETYPES,
        "max_file_size_mb": MAX_FILE_SIZE_MB,
    }
