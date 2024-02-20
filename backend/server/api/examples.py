"""Endpoints for managing definition of examples.."""
from typing import Annotated, Any, List
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing_extensions import TypedDict

from db.models import Example, get_session

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
        str, "JSON object that is expected to be extracted from the content."
    ]


@router.post("")
def create(
    create_request: CreateExample,
    *,
    session: Session = Depends(get_session),
) -> UUID:
    """Endpoint to create an example."""
    instance = Example(
        extractor_id=create_request["extractor_id"],
        content=create_request["content"],
        output=create_request["output"],
    )
    session.add(instance)
    session.commit()
    return instance.uuid


@router.get("")
def list(
    extractor_id: UUID,
    *,
    limit: int = 10,
    offset: int = 0,
    session=Depends(get_session),
) -> List[Any]:
    """Endpoint to get all examples."""
    return (
        session.query(Example)
        .filter(Example.extractor_id == extractor_id)
        .limit(limit)
        .offset(offset)
        .all()
    )


@router.delete("/{uuid}")
def delete(uuid: UUID, *, session: Session = Depends(get_session)) -> None:
    """Endpoint to delete an example."""
    session.query(Example).filter(Example.uuid == str(uuid)).delete()
    session.commit()
