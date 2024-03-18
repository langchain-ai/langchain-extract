"""Endpoint for listing available chat models for extraction."""
from typing import List, get_args

from fastapi import APIRouter

from server.settings import ModelNameLiteral

router = APIRouter(
    prefix="/chat_models",
    tags=["Available chat models"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def list_chat_models() -> List[str]:
    """Endpoint to get all chat models."""
    return list(get_args(ModelNameLiteral))
