"""Endpoint for listing available chat models for extraction."""
from typing import Any, Dict

from fastapi import APIRouter

from server.models import SUPPORTED_MODELS

router = APIRouter(
    prefix="/configurables",
    tags=["Available chat models"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def get_configurables() -> Dict[str, Any]:
    """Endpoint to get all chat models."""
    return {
        "models": list(SUPPORTED_MODELS.keys()),
    }
