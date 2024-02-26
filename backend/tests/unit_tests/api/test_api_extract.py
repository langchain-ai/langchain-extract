"""Code to test API endpoints."""
import tempfile
from unittest.mock import patch
from uuid import UUID

from langchain.text_splitter import CharacterTextSplitter
from langchain_core.runnables import RunnableLambda

from tests.db import get_async_client


def mock_extraction_runnable(*args, **kwargs):
    """Mock the extraction_runnable function."""
    extract_request = args[0]
    return {
        "data": [
            extract_request.text[:10],
        ]
    }


def mock_text_splitter(*args, **kwargs):
    return CharacterTextSplitter()


@patch(
    "server.extraction_runnable.extraction_runnable",
    new=RunnableLambda(mock_extraction_runnable),
)
@patch("server.extraction_runnable.TokenTextSplitter", mock_text_splitter)
async def test_extract_from_file() -> None:
    """Test extract from file API."""
    async with get_async_client() as client:
        # Test with invalid extractor
        extractor_id = UUID(int=1027)  # 1027 is a good number.
        response = await client.post(
            "/extract",
            data={
                "extractor_id": str(extractor_id),
                "text": "Test Content",
            },
        )
        assert response.status_code == 404, response.text

        # First create an extractor
        create_request = {
            "description": "Test Description",
            "schema": {"type": "object"},
            "instruction": "Test Instruction",
        }
        response = await client.post("/extractors", json=create_request)
        assert response.status_code == 200, response.text
        # Get the extractor id
        extractor_id = response.json()

        # Run an extraction.
        # We'll use multi-form data here.
        response = await client.post(
            "/extract",
            data={
                "extractor_id": extractor_id,
                "text": "Test Content",
                "mode": "entire_document",
            },
        )
        assert response.status_code == 200
        assert response.json() == {"data": ["Test Conte"]}

        # We'll use multi-form data here.
        # Create a named temporary file
        with tempfile.NamedTemporaryFile(mode="w+t", delete=False) as f:
            f.write("This is a named temporary file.")
            f.seek(0)
            f.flush()
            response = await client.post(
                "/extract",
                data={
                    "extractor_id": extractor_id,
                    "mode": "entire_document",
                },
                files={"file": f},
            )

        assert response.status_code == 200, response.text
        assert response.json() == {"data": ["This is a "]}
