from operator import itemgetter
from typing import Any, Dict, List, Optional

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from langchain_openai import OpenAIEmbeddings

from db.models import Extractor
from extraction.utils import get_examples_from_extractor
from server.extraction_runnable import (
    ExtractRequest,
    ExtractResponse,
    extraction_runnable,
)


def _get_top_doc_content(docs: List[Document]) -> str:
    if docs:
        return docs[0].page_content
    else:
        return ""


def _make_extract_request(input_dict: Dict[str, Any]) -> ExtractRequest:
    return ExtractRequest(**input_dict)


async def extract_from_content(
    content: str,
    extractor: Extractor,
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
            "text": itemgetter("query") | retriever | _get_top_doc_content,
            "schema": itemgetter("schema"),
            "instructions": lambda x: x.get("instructions"),
            "examples": lambda x: x.get("examples"),
        }
        | RunnableLambda(_make_extract_request)
        | extraction_runnable
    )
    schema = extractor.schema
    examples = get_examples_from_extractor(extractor)
    description = extractor.description  # TODO: improve this
    return await runnable.ainvoke(
        {
            "query": description,
            "schema": schema,
            "examples": examples,
            "instructions": extractor.instruction,
        }
    )
