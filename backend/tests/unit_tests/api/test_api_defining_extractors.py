"""Code to test API endpoints."""
import uuid

from tests.db import get_async_client


async def test_extractors_api() -> None:
    """This will test a few of the extractors API endpoints."""
    # First verify that the database is empty
    async with get_async_client() as client:
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

        # Verify that we can create an extractor, including other properties
        owner_id = str(uuid.uuid4())
        create_request = {
            "name": "my extractor",
            "owner_id": owner_id,
            "description": "Test Description",
            "schema": {"type": "object"},
            "instruction": "Test Instruction",
        }
        response = await client.post("/extractors", json=create_request)
        extractor_uuid = response.json()["uuid"]
        assert response.status_code == 200
        response = await client.get(f"/extractors/{extractor_uuid}")
        assert extractor_uuid == response.json()["uuid"]
        assert owner_id == response.json()["owner_id"]


async def test_sharing_extractor() -> None:
    """Test sharing an extractor."""
    async with get_async_client() as client:
        response = await client.get("/extractors")
        assert response.status_code == 200
        assert response.json() == []
        # Verify that we can create an extractor
        create_request = {
            "name": "Test Name",
            "description": "Test Description",
            "schema": {"type": "object"},
            "instruction": "Test Instruction",
        }
        response = await client.post("/extractors", json=create_request)
        assert response.status_code == 200

        uuid = response.json()["uuid"]

        # Verify that the extractor was created
        response = await client.post(f"/extractors/{uuid}/share")
        assert response.status_code == 200
        assert "share_uuid" in response.json()
        share_uuid = response.json()["share_uuid"]

        # Test idempotency
        response = await client.post(f"/extractors/{uuid}/share")
        assert response.status_code == 200
        assert "share_uuid" in response.json()
        assert response.json()["share_uuid"] == share_uuid

        # Check that we can retrieve the shared extractor
        response = await client.get(f"/s/{share_uuid}")
        assert response.status_code == 200
        keys = sorted(response.json())
        assert keys == ["description", "instruction", "name", "schema"]

        assert response.json() == {
            "description": "Test Description",
            "instruction": "Test Instruction",
            "name": "Test Name",
            "schema": {"type": "object"},
        }
