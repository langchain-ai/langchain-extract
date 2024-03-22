"""Convert binary input to blobs and parse them using the appropriate parser."""
from __future__ import annotations

from typing import BinaryIO, List

from fastapi import HTTPException
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

MAX_FILE_SIZE_MB = 10  # in MB


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


def _get_file_size_in_mb(data: BinaryIO) -> float:
    """Get file size in MB."""
    data.seek(0, 2)  # Move the cursor to the end of the file
    file_size = data.tell()
    file_size_in_mb = file_size / (1024 * 1024)
    data.seek(0)
    return file_size_in_mb


# PUBLIC API

MIMETYPE_BASED_PARSER = MimeTypeBasedParser(
    handlers=HANDLERS,
    fallback_parser=None,
)


def convert_binary_input_to_blob(data: BinaryIO) -> Blob:
    """Convert ingestion input to blob."""
    file_size_in_mb = _get_file_size_in_mb(data)

    if file_size_in_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds the maximum limit of {MAX_FILE_SIZE_MB} MB.",
        )

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
