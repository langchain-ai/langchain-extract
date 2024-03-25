from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Sequence

from fastapi import HTTPException
from jsonschema import Draft202012Validator, exceptions
from langchain.text_splitter import TokenTextSplitter
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import chain
from langserve import CustomUserType
from pydantic import BaseModel, Field, validator
from typing_extensions import TypedDict

from db.models import Example, Extractor
from extraction.utils import update_json_schema
from server import settings
from server.models import DEFAULT_MODEL, get_chunk_size, get_model
from server.validators import validate_json_schema


class ExtractionExample(BaseModel):
    """An example extraction.

    This example consists of a text and the expected output of the extraction.
    """

    text: str = Field(..., description="The input text")
    output: List[Dict[str, Any]] = Field(
        ..., description="The expected output of the example. A list of objects."
    )


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
    examples: Optional[List[ExtractionExample]] = Field(
        None, description="Examples of extractions."
    )
    model_name: Optional[str] = Field("gpt-3.5-turbo", description="Chat model to use.")

    @validator("json_schema")
    def validate_schema(cls, v: Any) -> Dict[str, Any]:
        """Validate the schema."""
        validate_json_schema(v)
        return v


class ExtractResponse(TypedDict, total=False):
    """Response body for the extract endpoint."""

    data: List[Any]
    # content to long will be set to true if the content is too long
    # and had to be truncated
    content_too_long: Optional[bool]


def _cast_example_to_dict(example: Example) -> Dict[str, Any]:
    """Cast example record to dictionary."""
    return {
        "text": example.content,
        "output": example.output,
    }


def _make_prompt_template(
    instructions: Optional[str],
    examples: Optional[Sequence[ExtractionExample]],
    function_name: str,
) -> ChatPromptTemplate:
    """Make a system message from instructions and examples."""
    prefix = (
        "You are a top-tier algorithm for extracting information from text. "
        "Only extract information that is relevant to the provided text. "
        "If no information is relevant, use the schema and output "
        "an empty list where appropriate."
    )
    if instructions:
        system_message = ("system", f"{prefix}\n\n{instructions}")
    else:
        system_message = ("system", prefix)
    prompt_components = [system_message]
    if examples is not None:
        few_shot_prompt = []
        for example in examples:
            # TODO: We'll need to refactor this at some point to
            # support other encoding strategies. The function calling logic here
            # has some hard-coded assumptions (e.g., name of parameters like `data`).
            function_call = {
                "arguments": json.dumps(
                    {
                        "data": example.output,
                    }
                ),
                "name": function_name,
            }
            few_shot_prompt.extend(
                [
                    HumanMessage(content=example.text),
                    AIMessage(
                        content="", additional_kwargs={"function_call": function_call}
                    ),
                ]
            )
        prompt_components.extend(few_shot_prompt)

    prompt_components.append(
        (
            "human",
            "I need to extract information from "
            "the following text: ```\n{text}\n```\n",
        ),
    )
    return ChatPromptTemplate.from_messages(prompt_components)


# PUBLIC API


def deduplicate(
    extract_responses: Sequence[ExtractResponse],
) -> ExtractResponse:
    """Deduplicate the results.

    The deduplication is done by comparing the serialized JSON of each of the results
    and only keeping the unique ones.
    """
    unique_extracted = []
    seen = set()
    for response in extract_responses:
        for data_item in response["data"]:
            # Serialize the data item for comparison purposes
            serialized = json.dumps(data_item, sort_keys=True)
            if serialized not in seen:
                seen.add(serialized)
                unique_extracted.append(data_item)

    return {
        "data": unique_extracted,
    }


def get_examples_from_extractor(extractor: Extractor) -> List[Dict[str, Any]]:
    """Get examples from an extractor."""
    return [_cast_example_to_dict(example) for example in extractor.examples]


@chain
async def extraction_runnable(extraction_request: ExtractRequest) -> ExtractResponse:
    """An end point to extract content from a given text object."""
    # TODO: Add validation for model context window size
    schema = update_json_schema(extraction_request.json_schema)
    try:
        Draft202012Validator.check_schema(schema)
    except exceptions.ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Invalid schema: {e.message}")

    prompt = _make_prompt_template(
        extraction_request.instructions,
        extraction_request.examples,
        schema["title"],
    )
    model = get_model(extraction_request.model_name)
    # N.B. method must be consistent with examples in _make_prompt_template
    runnable = (prompt | model.with_structured_output(schema=schema)).with_config(
        {"run_name": "extraction"}
    )

    return await runnable.ainvoke({"text": extraction_request.text})


async def extract_entire_document(
    content: str,
    extractor: Extractor,
    model_name: str,
) -> ExtractResponse:
    """Extract from entire document."""

    json_schema = extractor.schema
    examples = get_examples_from_extractor(extractor)
    text_splitter = TokenTextSplitter(
        chunk_size=get_chunk_size(model_name),
        chunk_overlap=20,
        model_name=DEFAULT_MODEL,
    )
    texts = text_splitter.split_text(content)
    extraction_requests = [
        ExtractRequest(
            text=text,
            schema=json_schema,
            instructions=extractor.instruction,  # TODO: consistent naming
            examples=examples,
            model_name=model_name,
        )
        for text in texts
    ]

    # Limit the number of chunks to process
    if len(extraction_requests) > settings.MAX_CHUNKS and settings.MAX_CHUNKS > 0:
        content_too_long = True
        extraction_requests = extraction_requests[: settings.MAX_CHUNKS]
    else:
        content_too_long = False

    # Run extractions which may potentially yield duplicate results
    extract_responses: List[ExtractResponse] = await extraction_runnable.abatch(
        extraction_requests, {"max_concurrency": settings.MAX_CONCURRENCY}
    )
    # Deduplicate the results
    return {
        "data": deduplicate(extract_responses)["data"],
        "content_too_long": content_too_long,
    }
