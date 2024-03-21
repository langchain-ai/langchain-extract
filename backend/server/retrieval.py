from operator import itemgetter
from typing import Any, Dict, List, Optional

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableLambda
from langchain_openai import OpenAIEmbeddings

from db.models import Extractor
from server.extraction_runnable import (
    ExtractRequest,
    ExtractResponse,
    deduplicate,
    extraction_runnable,
    get_examples_from_extractor,
)


def _make_extract_requests(input_dict: Dict[str, Any]) -> List[ExtractRequest]:
    docs = input_dict.pop("text")
    return [ExtractRequest(text=doc.page_content, **input_dict) for doc in docs]


async def extract_from_content(
    content: str,
    extractor: Extractor,
    model_name: str,
    *,
    text_splitter_kwargs: Optional[Dict[str, Any]] = None,
) -> ExtractResponse:
    """Extract from potentially long-form content."""
    if text_splitter_kwargs is None:
        text_splitter_kwargs = {
            "separator": "\n\n",
            "chunk_size": 1000,
            "chunk_overlap": 50,
        }
    text_splitter = CharacterTextSplitter(**text_splitter_kwargs)
    docs = text_splitter.create_documents([content])
    doc_contents = [doc.page_content for doc in docs]

    vectorstore = FAISS.from_texts(doc_contents, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()

    runnable = (
        {
            "text": itemgetter("query") | retriever,
            "schema": itemgetter("schema"),
            "instructions": lambda x: x.get("instructions"),
            "examples": lambda x: x.get("examples"),
            "model_name": lambda x: x.get("model_name"),
        }
        | RunnableLambda(_make_extract_requests)
        | extraction_runnable.abatch
    )
    schema = extractor.schema
    examples = get_examples_from_extractor(extractor)
    description = extractor.description  # TODO: improve this
    result = await runnable.ainvoke(
        {
            "query": description,
            "schema": schema,
            "examples": examples,
            "instructions": extractor.instruction,
            "model_name": model_name,
        }
    )
    return deduplicate(result)
