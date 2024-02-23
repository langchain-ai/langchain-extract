"""Convert binary input to blobs and parse them using the appropriate parser."""
from __future__ import annotations

from typing import BinaryIO, List

from langchain.document_loaders.parsers import BS4HTMLParser, PDFMinerParser
from langchain.document_loaders.parsers.generic import MimeTypeBasedParser
from langchain.document_loaders.parsers.txt import TextParser
from langchain_community.document_loaders import Blob
from langchain_core.documents import Document

HANDLERS = {
    "application/pdf": PDFMinerParser(),
    "text/plain": TextParser(),
    "text/html": BS4HTMLParser(),
    # Disable for now as they rely on unstructured and there's some install
    # issue with unstructured.
    # from langchain.document_loaders.parsers.msword import MsWordParser
    # "application/msword": MsWordParser(),
    # "application/vnd.openxmlformats-officedocument.wordprocessingml.document": (
    #     MsWordParser()
    # ),
}

SUPPORTED_MIMETYPES = sorted(HANDLERS.keys())


def _guess_mimetype(file_bytes: bytes) -> str:
    """Guess the mime-type of a file."""
    try:
        import magic
    except ImportError as e:
        raise ImportError(
            "magic package not found, please install it with `pip install python-magic`"
        ) from e

    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(file_bytes)
    return mime_type


# PUBLIC API

MIMETYPE_BASED_PARSER = MimeTypeBasedParser(
    handlers=HANDLERS,
    fallback_parser=None,
)


def convert_binary_input_to_blob(data: BinaryIO) -> Blob:
    """Convert ingestion input to blob."""
    file_data = data.read()
    mimetype = _guess_mimetype(file_data)
    file_name = data.name
    return Blob.from_data(
        data=file_data,
        path=file_name,
        mime_type=mimetype,
    )


def parse_binary_input(data: BinaryIO) -> List[Document]:
    """Parse binary input."""
    blob = convert_binary_input_to_blob(data)
    return MIMETYPE_BASED_PARSER.parse(blob)
