import json
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from jsonschema import Draft202012Validator, exceptions
from langchain.chains.openai_functions import create_openai_fn_runnable
from langchain.text_splitter import TokenTextSplitter
from langchain_core.runnables import chain
from langchain_openai.chat_models import ChatOpenAI
from langserve import CustomUserType
from pydantic import BaseModel, Field, validator

from db.models import Extractor
from extraction.utils import (
    FewShotExample,
    convert_json_schema_to_openai_schema,
    get_examples_from_extractor,
    make_prompt_template,
)
from server.settings import CHUNK_SIZE, MODEL_NAME
from server.validators import validate_json_schema


class ExtractRequest(CustomUserType):
    """Request body for the extract endpoint."""

    text: str = Field(..., description="The text to extract from.")
    json_schema: Dict[str, Any] = Field(
        ...,
        description="JSON schema that describes what content should be extracted "
        "from the text.",
        alias="schema",
    )
    instructions: Optional[str] = Field(
        None, description="Supplemental system instructions."
    )
    examples: Optional[List[FewShotExample]] = Field(
        None, description="Few shot examples."
    )

    @validator("json_schema")
    def validate_schema(cls, v: Any) -> Dict[str, Any]:
        """Validate the schema."""
        validate_json_schema(v)
        return v


ExtractedType = Any


class InternalExtraction(BaseModel):
    """An extraction result."""

    extracted: ExtractedType


class ExtractResponse(BaseModel):
    """Response body for the extract endpoint."""

    extracted: List[ExtractedType]


def _deduplicate_extract_results(
    responses: List[InternalExtraction],
) -> ExtractResponse:
    unique_extracted = []
    seen = set()
    for response in responses:
        serialized = json.dumps(response.extracted, sort_keys=True)
        if serialized not in seen:
            seen.add(serialized)
            unique_extracted.append(response.extracted)

    return ExtractResponse(extracted=unique_extracted)


model = ChatOpenAI(model=MODEL_NAME, temperature=0)


async def extract_entire_document(
    content: str, extractor: Extractor, multi: bool = True,
) -> ExtractResponse:
    """Extract from entire document."""
    json_schema = extractor.schema
    examples = get_examples_from_extractor(extractor)
    text_splitter = TokenTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=20,
        model_name=MODEL_NAME,
    )
    texts = text_splitter.split_text(content)
    extraction_requests = [
        ExtractRequest(
            text=text,
            schema=json_schema,
            instructions=extractor.instruction,  # TODO: consistent naming
            examples=examples,
        )
        for text in texts
    ]
    results = await extraction_runnable.abatch(
        extraction_requests, {'max_concurrency': 1}
    )
    return _deduplicate_extract_results(results)


@chain
async def extraction_runnable(extraction_request: ExtractRequest) -> InternalExtraction:
    """An end point to extract content from a given text object.

    Used for powering an extraction playground.
    """
    schema = extraction_request.json_schema
    name = schema.get("title", "")
    try:
        Draft202012Validator.check_schema(schema)
    except exceptions.ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Invalid schema: {e.message}")

    prompt = make_prompt_template(
        extraction_request.instructions, extraction_request.examples, name
    )
    openai_function = convert_json_schema_to_openai_schema(schema)
    runnable = create_openai_fn_runnable(
        functions=[openai_function], llm=model, prompt=prompt
    )
    extracted_content = runnable.ainvoke({"text": extraction_request.text})

    return InternalExtraction(
        extracted=extracted_content,
    )
