"""Endpoints for working with shared resources."""
from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from db.models import Extractor, SharedExtractors, get_session

router = APIRouter(
    prefix="/s",
    tags=["extractor definitions"],
    responses={404: {"description": "Not found"}},
)


class SharedExtractorResponse(BaseModel):
    """Response for sharing an extractor."""

    # UUID should not be included in the response since it is not a public identifier!
    name: str
    description: str
    # schema is a reserved keyword by pydantic
    schema_: Dict[str, Any] = Field(..., alias="schema")
    instruction: str


@router.get("/{uuid}")
def get(
    uuid: UUID,
    *,
    session: Session = Depends(get_session),
) -> SharedExtractorResponse:
    """Get a shared extractor."""
    extractor = (
        session.query(Extractor)
        .join(SharedExtractors, Extractor.uuid == SharedExtractors.extractor_id)
        .filter(SharedExtractors.share_token == uuid)
        .first()
    )

    if not extractor:
        raise HTTPException(status_code=404, detail="Extractor not found.")

    return SharedExtractorResponse(
        name=extractor.name,
        description=extractor.description,
        schema=extractor.schema,
        instruction=extractor.instruction,
    )
