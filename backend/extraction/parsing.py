"""Convert binary input to blobs and parse them using the appropriate parser."""
from __future__ import annotations

import io
from typing import BinaryIO, List

from fastapi import HTTPException
from langchain.document_loaders.parsers import BS4HTMLParser, PDFMinerParser
from langchain.document_loaders.parsers.generic import MimeTypeBasedParser
from langchain.document_loaders.parsers.txt import TextParser
from langchain_community.document_loaders import Blob
from langchain_core.documents import Document
from pdfminer.pdfpage import PDFPage

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

MAX_FILE_SIZE = 10  # in MB
MAX_PAGES = 20  # for PDFs


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


def _get_pdf_page_count(file_bytes: bytes) -> int:
    """Get the number of pages in a PDF file."""
    file_stream = io.BytesIO(file_bytes)
    pages = PDFPage.get_pages(file_stream)
    return sum(1 for _ in pages)


# PUBLIC API

MIMETYPE_BASED_PARSER = MimeTypeBasedParser(
    handlers=HANDLERS,
    fallback_parser=None,
)


def convert_binary_input_to_blob(data: BinaryIO) -> Blob:
    """Convert ingestion input to blob."""
    file_size_in_mb = _get_file_size_in_mb(data)

    if file_size_in_mb > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds the maximum limit of {MAX_FILE_SIZE} MB.",
        )

    file_data = data.read()
    mimetype = _guess_mimetype(file_data)
    file_name = data.name

    if mimetype == "application/pdf":
        number_of_pages = _get_pdf_page_count(file_data)
        if number_of_pages > MAX_PAGES:
            raise HTTPException(
                status_code=413,
                detail=(
                    f"PDF has too many pages: {number_of_pages}, "
                    f"exceeding the maximum of {MAX_PAGES}."
                ),
            )

    return Blob.from_data(
        data=file_data,
        path=file_name,
        mime_type=mimetype,
    )


def parse_binary_input(data: BinaryIO) -> List[Document]:
    """Parse binary input."""
    blob = convert_binary_input_to_blob(data)
    return MIMETYPE_BASED_PARSER.parse(blob)
