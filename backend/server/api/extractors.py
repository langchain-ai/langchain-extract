"""Endpoints for managing definition of extractors."""
from typing import Any, Dict, List
from uuid import UUID, uuid4

from fastapi import APIRouter, Cookie, Depends, HTTPException
from pydantic import BaseModel, Field, validator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.models import Extractor, SharedExtractors, get_session
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

    uuid: UUID = Field(..., description="The UUID of the created extractor.")


class ShareExtractorRequest(BaseModel):
    """Response for sharing an extractor."""

    uuid: UUID = Field(..., description="The UUID of the extractor to share.")


class ShareExtractorResponse(BaseModel):
    """Response for sharing an extractor."""

    share_uuid: UUID = Field(..., description="The UUID for the shared extractor.")


@router.post("/{uuid}/share", response_model=ShareExtractorResponse)
def share(
    uuid: UUID,
    *,
    session: Session = Depends(get_session),
) -> ShareExtractorResponse:
    """Endpoint to share an extractor.

    Look up a shared extractor by UUID and return the share UUID if it exists.
    If not shared, create a new shared extractor entry and return the new share UUID.

    Args:
        uuid: The UUID of the extractor to share.
        session: The database session.

    Returns:
        The UUID for the shared extractor.
    """
    # Check if the extractor is already shared
    shared_extractor = (
        session.query(SharedExtractors)
        .filter(SharedExtractors.extractor_id == uuid)
        .scalar()
    )

    if shared_extractor:
        # The extractor is already shared, return the existing share_uuid
        return ShareExtractorResponse(share_uuid=shared_extractor.share_token)

    # If not shared, create a new shared extractor entry
    new_shared_extractor = SharedExtractors(
        extractor_id=uuid,
        # This will automatically generate a new UUID for share_token
        share_token=uuid4(),
    )

    session.add(new_shared_extractor)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Failed to share the extractor.")

    # Return the new share_uuid
    return ShareExtractorResponse(share_uuid=new_shared_extractor.share_token)


@router.post("")
def create(
    create_request: CreateExtractor,
    *,
    session: Session = Depends(get_session),
    owner_id: UUID = Cookie(...),
) -> CreateExtractorResponse:
    """Endpoint to create an extractor."""

    instance = Extractor(
        name=create_request.name,
        owner_id=owner_id,
        schema=create_request.json_schema,
        description=create_request.description,
        instruction=create_request.instruction,
    )
    session.add(instance)
    session.commit()
    return CreateExtractorResponse(uuid=instance.uuid)


@router.get("/{uuid}")
def get(uuid: UUID, *, session: Session = Depends(get_session)) -> Dict[str, Any]:
    """Endpoint to get an extractor."""
    extractor = session.query(Extractor).filter(Extractor.uuid == str(uuid)).scalar()
    if extractor is None:
        raise HTTPException(status_code=404, detail="Extractor not found.")
    return {
        "uuid": extractor.uuid,
        "name": extractor.name,
        "description": extractor.description,
        "schema": extractor.schema,
        "instruction": extractor.instruction,
    }


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
