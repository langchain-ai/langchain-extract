"""Code to test API endpoints."""
import uuid

from tests.db import get_async_client


async def test_extractors_api() -> None:
    """This will test a few of the extractors API endpoints."""
    # First verify that the database is empty
    with get_async_client() as client:
        response = await client.get("/extractors")
        assert response.status_code == 200
        assert response.json() == []

        # Verify that we can create an extractor
        create_request = {
            "description": "Test Description",
            "schema": {"type": "object"},
            "instruction": "Test Instruction",
        }
        response = await client.post("/extractors", json=create_request)
        assert response.status_code == 200

        # Verify that the extractor was created
        response = await client.get("/extractors")
        assert response.status_code == 200
        assert len(response.json()) == 1

        # Verify that we can delete an extractor
        get_response = response.json()
        uuid_str = get_response[0]["uuid"]
        _ = uuid.UUID(uuid_str)  # assert valid uuid
        response = await client.delete(f"/extractors/{uuid_str}")
        assert response.status_code == 200

        get_response = await client.get("/extractors")
        assert get_response.status_code == 200
        assert get_response.json() == []

        # Verify that we can create an extractor
        create_request = {
            "description": "Test Description",
            "schema": {"type": "object"},
            "instruction": "Test Instruction",
        }
        response = await client.post("/extractors", json=create_request)
        assert response.status_code == 200

        # Verify that the extractor was created
        response = await client.get("/extractors")
        assert response.status_code == 200
        assert len(response.json()) == 1

        # Verify that we can delete an extractor
        get_response = response.json()
        uuid_str = get_response[0]["uuid"]
        _ = uuid.UUID(uuid_str)  # assert valid uuid
        response = await client.delete(f"/extractors/{uuid_str}")
        assert response.status_code == 200

        get_response = await client.get("/extractors")
        assert get_response.status_code == 200
        assert get_response.json() == []

        # Verify that we can create an extractor
        create_request = {
            "description": "Test Description",
            "schema": {"type": "object"},
            "instruction": "Test Instruction",
        }
        response = await client.post("/extractors", json=create_request)
        assert response.status_code == 200
