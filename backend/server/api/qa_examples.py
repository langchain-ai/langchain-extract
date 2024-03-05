"""Endpoints for managing definition of examples.."""
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing_extensions import Annotated, TypedDict

from db.models import QueryAnalysisExample, get_session

router = APIRouter(
    prefix="/qa_examples",
    tags=["example definitions"],
    responses={404: {"description": "Not found"}},
)


class CreateExample(TypedDict):
    """A request to create an example."""

    query_analyzer_id: Annotated[UUID, "The extractor ID that this is an example for."]
    content: Annotated[List[Any], "The input portion of the example."]
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
) -> CreateExampleResponse:
    """Endpoint to create an example."""
    instance = QueryAnalysisExample(
        query_analyzer_id=create_request["query_analyzer_id"],
        content=create_request["content"],
        output=create_request["output"],
    )
    session.add(instance)
    session.commit()
    return {"uuid": instance.uuid}


@router.get("")
def list(
    query_analyzer_id: UUID,
    *,
    limit: int = 10,
    offset: int = 0,
    session=Depends(get_session),
) -> List[Any]:
    """Endpoint to get all examples."""
    return (
        session.query(QueryAnalysisExample)
        .filter(QueryAnalysisExample.query_analyzer_id == query_analyzer_id)
        .order_by(QueryAnalysisExample.uuid)
        .limit(limit)
        .offset(offset)
        .all()
    )


@router.delete("/{uuid}")
def delete(uuid: UUID, *, session: Session = Depends(get_session)) -> None:
    """Endpoint to delete an example."""
    session.query(QueryAnalysisExample).filter(
        QueryAnalysisExample.uuid == str(uuid)
    ).delete()
    session.commit()
