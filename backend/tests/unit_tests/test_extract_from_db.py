"""Code to test API endpoints."""
from unittest.mock import patch
from uuid import UUID

from langchain_core.runnables import RunnableLambda

from tests.db import get_async_client


def mock_extraction_runnable(*args, **kwargs):
    """Mock the extraction_runnable function."""
    return {"extracted": "placeholder"}


@patch("server.main.extraction_runnable", new=RunnableLambda(mock_extraction_runnable))
async def test_extract_from_file() -> None:
    """Test extract from file API."""
    async with get_async_client() as client:
        # Test with invalid extractor
        extractor_id = UUID(int=1027)  # 1027 is a good number.
        response = await client.post(
            "/extract",
            json={
                "extractor_id": str(extractor_id),
                "text": "Test Content",
            },
        )
        assert response.status_code == 404

        # First create an extractor
        create_request = {
            "description": "Test Description",
            "schema": {"type": "object"},
            "instruction": "Test Instruction",
        }
        response = await client.post("/extractors", json=create_request)
        assert response.status_code == 200
        # Get the extractor id
        extractor_id = response.json()

        # Extract
        response = await client.post(
            "/extract",
            json={
                "extractor_id": extractor_id,
                "text": "Test Content",
                "mode": "entire_document",
            },
        )
        assert response.status_code == 200
        assert response.json() == {"extracted": "placeholder"}
