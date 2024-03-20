"""Endpoints for managing definition of examples.."""
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Cookie, Depends, HTTPException
from sqlalchemy.orm import Session
from typing_extensions import Annotated, TypedDict

from db.models import Example, get_session, validate_extractor_owner

router = APIRouter(
    prefix="/examples",
    tags=["example definitions"],
    responses={404: {"description": "Not found"}},
)


class CreateExample(TypedDict):
    """A request to create an example."""

    extractor_id: Annotated[UUID, "The extractor ID that this is an example for."]
    content: Annotated[str, "The input portion of the example."]
    output: Annotated[
        List[Any], "JSON object that is expected to be extracted from the content."
    ]


class CreateExampleResponse(TypedDict):
    """Response for creating an example."""

    uuid: UUID


@router.post("")
def create(
    create_request: CreateExample,
    *,
    session: Session = Depends(get_session),
    owner_id: UUID = Cookie(...),
) -> CreateExampleResponse:
    """Endpoint to create an example."""
    if not validate_extractor_owner(session, create_request["extractor_id"], owner_id):
        raise HTTPException(status_code=404, detail="Extractor not found for owner.")

    instance = Example(
        extractor_id=create_request["extractor_id"],
        content=create_request["content"],
        output=create_request["output"],
    )
    session.add(instance)
    session.commit()
    return {"uuid": instance.uuid}


@router.get("")
def list(
    extractor_id: UUID,
    *,
    limit: int = 10,
    offset: int = 0,
    session=Depends(get_session),
    owner_id: UUID = Cookie(...),
) -> List[Any]:
    """Endpoint to get all examples."""
    if not validate_extractor_owner(session, extractor_id, owner_id):
        raise HTTPException(status_code=404, detail="Extractor not found for owner.")
    return (
        session.query(Example)
        .filter(Example.extractor_id == extractor_id)
        .order_by(Example.uuid)
        .limit(limit)
        .offset(offset)
        .all()
    )


@router.delete("/{uuid}")
def delete(
    uuid: UUID, *, session: Session = Depends(get_session), owner_id: UUID = Cookie(...)
) -> None:
    """Endpoint to delete an example."""
    extractor_id = session.query(Example).filter_by(uuid=str(uuid)).first().extractor_id
    if not validate_extractor_owner(session, extractor_id, owner_id):
        raise HTTPException(status_code=404, detail="Extractor not found for owner.")
    session.query(Example).filter_by(uuid=str(uuid)).delete()
    session.commit()
