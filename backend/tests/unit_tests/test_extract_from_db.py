"""Code to test API endpoints."""
from uuid import UUID

from tests.db import get_async_client


async def test_extract_from_file() -> None:
    """Test extract from file API."""
    async with get_async_client() as client:
        # Test with invalid extractor
        extractor_id = UUID(int=1027)  # 1027 is a good number.
        response = await client.post(
            "/extract", json={"extractor_id": str(extractor_id), "text": "Test Content"}
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

        # Let's verify that there are no examples
        response = await client.post(
            "/extract", json={"extractor_id": extractor_id, "text": "Test Content"}
        )
        assert response.status_code == 200
        assert response.json() == {"extracted": "placeholder"}
