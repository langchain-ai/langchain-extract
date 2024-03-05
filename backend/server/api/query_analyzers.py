"""Endpoints for managing definition of query analyzers."""
from typing import Any, Dict, List, Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session

from db.models import QueryAnalyzer, get_session
from server.validators import validate_json_schema

router = APIRouter(
    prefix="/query_analyzers",
    tags=["query analyzer definitions"],
    responses={404: {"description": "Not found"}},
)


class CreateQueryAnalyzerRequest(BaseModel):
    """A request to create an query analyzer."""

    name: str = Field(default="", description="The name of the query_analyzer.")

    description: str = Field(
        default="", description="Short description of the query_analyzer."
    )
    json_schema: Union[Dict[str, Any], List[Dict[str, Any]]] = Field(
        ..., description="The schema(s) to use for analysis.", alias="schema"
    )
    instructions: str = Field(
        ..., description="The instruction to use for query analysis."
    )

    @validator("json_schema")
    def validate_schema(cls, v: Any) -> Dict[str, Any]:
        """Validate the schema."""
        to_validate = v if isinstance(v, List) else [v]
        for v_ in to_validate:
            validate_json_schema(v_)
        return v


class CreateQueryAnalyzerResponse(BaseModel):
    """Response for creating an query analyzer."""

    uuid: UUID


@router.post("")
def create(
    create_request: CreateQueryAnalyzerRequest,
    *,
    session: Session = Depends(get_session),
) -> CreateQueryAnalyzerResponse:
    """Endpoint to create an query analyzer."""
    instance = QueryAnalyzer(
        name=create_request.name,
        schema=create_request.json_schema,
        description=create_request.description,
        instructions=create_request.instructions,
    )
    session.add(instance)
    session.commit()
    return CreateQueryAnalyzerResponse(uuid=instance.uuid)


@router.get("/{uuid}")
def get(uuid: UUID, *, session: Session = Depends(get_session)) -> Dict[str, Any]:
    """Endpoint to get an query analyzer."""
    query_analyzer = (
        session.query(QueryAnalyzer).filter(QueryAnalyzer.uuid == str(uuid)).scalar()
    )
    if query_analyzer is None:
        raise HTTPException(status_code=404, detail="Query analyzer not found.")
    return {
        "uuid": query_analyzer.uuid,
        "name": query_analyzer.name,
        "description": query_analyzer.description,
        "schema": query_analyzer.schema,
        "instructions": query_analyzer.instructions,
    }


@router.get("")
def list(
    *,
    limit: int = 10,
    offset: int = 0,
    session=Depends(get_session),
) -> List[Any]:
    """Endpoint to get all query analyzers."""
    return session.query(QueryAnalyzer).limit(limit).offset(offset).all()


@router.delete("/{uuid}")
def delete(uuid: UUID, *, session: Session = Depends(get_session)) -> None:
    """Endpoint to delete an query analyzer."""
    session.query(QueryAnalyzer).filter(QueryAnalyzer.uuid == str(uuid)).delete()
    session.commit()
