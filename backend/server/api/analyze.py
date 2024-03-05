from typing import Any, Dict, List, TypedDict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from langchain_core.load import load
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from db.models import QueryAnalysisExample, QueryAnalyzer, get_session
from server.query_analysis import QueryAnalysisRequest, QueryAnalysisResponse
from server.query_analysis import query_analyzer as query_analyzer_runnable

router = APIRouter(
    prefix="/analyze",
    tags=["analyze"],
    responses={404: {"description": "Not found"}},
)


class AnalyzeRequest(TypedDict):
    """A request to create an example."""

    query_analyzer_id: Annotated[UUID, "The extractor ID that this is an example for."]
    messages: Annotated[List[Any], "The input portion of the example."]


def _cast_example_to_dict(example: QueryAnalysisExample) -> Dict[str, Any]:
    """Cast example record to dictionary."""
    return {
        "messages": load(example.content),
        "output": example.output,
    }


def get_examples_from_query_analyzer(
    query_analyzer: QueryAnalyzer,
) -> List[Dict[str, Any]]:
    """Get examples from an query_analyzer."""
    return [_cast_example_to_dict(example) for example in query_analyzer.examples]


@router.post("", response_model=QueryAnalysisResponse)
async def analyze_using_existing_analyzer(
    request: AnalyzeRequest,
    *,
    session: Session = Depends(get_session),
) -> QueryAnalysisResponse:
    """Endpoint that is used with an existing extractor."""
    analyzer = (
        session.query(QueryAnalyzer)
        .filter(QueryAnalyzer.uuid == request["query_analyzer_id"])
        .scalar()
    )
    if analyzer is None:
        raise HTTPException(status_code=404, detail="Analyzer not found.")
    examples = get_examples_from_query_analyzer(analyzer)
    request = QueryAnalysisRequest(
        messages=load(request["messages"]),
        schema=analyzer.schema,
        instructions=analyzer.instructions,
        examples=examples,
    )
    return await query_analyzer_runnable.ainvoke(request)
