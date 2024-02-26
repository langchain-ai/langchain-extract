"""Endpoints for managing definition of extractors."""
from typing import Any, Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session

from db.models import Extractor, get_session
from server.validators import validate_json_schema

router = APIRouter(
    prefix="/extractors",
    tags=["extractor definitions"],
    responses={404: {"description": "Not found"}},
)


class CreateExtractor(BaseModel):
    """A request to create an extractor."""

    name: str = Field(default="", description="The name of the extractor.")

    description: str = Field(
        default="", description="Short description of the extractor."
    )
    json_schema: Dict[str, Any] = Field(
        ..., description="The schema to use for extraction.", alias="schema"
    )
    instruction: str = Field(..., description="The instruction to use for extraction.")

    @validator("json_schema")
    def validate_schema(cls, v: Any) -> Dict[str, Any]:
        """Validate the schema."""
        validate_json_schema(v)
        return v


class CreateExtractorResponse(BaseModel):
    """Response for creating an extractor."""

    uuid: UUID


@router.post("")
def create(
    create_request: CreateExtractor, *, session: Session = Depends(get_session)
) -> CreateExtractorResponse:
    """Endpoint to create an extractor."""
    instance = Extractor(
        name=create_request.name,
        schema=create_request.json_schema,
        description=create_request.description,
        instruction=create_request.instruction,
    )
    session.add(instance)
    session.commit()
    return CreateExtractorResponse(uuid=instance.uuid)


@router.get("")
def list(
    *,
    limit: int = 10,
    offset: int = 0,
    session=Depends(get_session),
) -> List[Any]:
    """Endpoint to get all extractors."""
    return session.query(Extractor).limit(limit).offset(offset).all()


@router.delete("/{uuid}")
def delete(uuid: UUID, *, session: Session = Depends(get_session)) -> None:
    """Endpoint to delete an extractor."""
    session.query(Extractor).filter(Extractor.uuid == str(uuid)).delete()
    session.commit()
