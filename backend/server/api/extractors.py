"""Endpoints for managing definition of extractors.

"""
from typing import Any, Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session

from db.models import Extractor, get_session
from server.validators import validate_json_schema

router = APIRouter(
    prefix="/extractors",
    tags=["extractors"],
    responses={404: {"description": "Not found"}},
)


class CreateExtractor(BaseModel):
    """A request to create an extractor."""

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


@router.post("")
def create_extractor(
    create_request: CreateExtractor, *, session: Session = Depends(get_session)
) -> str:
    """Endpoint to create an extractor."""
    instance = Extractor(
        schema=create_request.json_schema, description=create_request.description
    )
    session.add(instance)
    session.commit()
    return instance.uuid


@router.get("")
def list_extractors(
    *,
    limit: int = 10,
    offset: int = 0,
    session=Depends(get_session),
) -> List[Any]:
    """Endpoint to get all extractors."""
    return session.query(Extractor).limit(limit).offset(offset).all()


@router.delete("{uuid}")
def delete_extractor(uuid: UUID, *, session: Session = Depends(get_session)) -> None:
    """Endpoint to delete an extractor."""
    session.query(Extractor).filter(Extractor.uuid == str(uuid)).delete()
    session.commit()
