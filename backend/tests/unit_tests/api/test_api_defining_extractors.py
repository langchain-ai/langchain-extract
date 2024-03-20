"""Code to test API endpoints."""
import uuid

from tests.db import get_async_client


async def test_extractors_api() -> None:
    """This will test a few of the extractors API endpoints."""
    # First verify that the database is empty
    async with get_async_client() as client:
        owner_id = str(uuid.uuid4())
        cookies = {"owner_id": owner_id}
        response = await client.get("/extractors", cookies=cookies)
        assert response.status_code == 200
        assert response.json() == []

        # Verify that we can create an extractor
        create_request = {
            "description": "Test Description",
            "schema": {"type": "object"},
            "instruction": "Test Instruction",
        }
        response = await client.post(
            "/extractors", json=create_request, cookies=cookies
        )
        assert response.status_code == 200

        # Verify that the extractor was created
        response = await client.get("/extractors", cookies=cookies)
        assert response.status_code == 200
        get_response = response.json()
        assert len(get_response) == 1

        # Check cookies
        bad_cookies = {"owner_id": str(uuid.uuid4())}
        bad_response = await client.get("/extractors", cookies=bad_cookies)
        assert bad_response.status_code == 200
        assert len(bad_response.json()) == 0

        # Check we need cookie to delete
        uuid_str = get_response[0]["uuid"]
        _ = uuid.UUID(uuid_str)  # assert valid uuid
        bad_response = await client.delete(
            f"/extractors/{uuid_str}", cookies=bad_cookies
        )
        # Check extractor was not deleted
        response = await client.get("/extractors", cookies=cookies)
        assert len(response.json()) == 1

        # Verify that we can delete an extractor
        _ = uuid.UUID(uuid_str)  # assert valid uuid
        response = await client.delete(f"/extractors/{uuid_str}", cookies=cookies)
        assert response.status_code == 200

        get_response = await client.get("/extractors", cookies=cookies)
        assert get_response.status_code == 200
        assert get_response.json() == []

        # Verify that we can create an extractor
        create_request = {
            "description": "Test Description",
            "schema": {"type": "object"},
            "instruction": "Test Instruction",
        }
        response = await client.post(
            "/extractors", json=create_request, cookies=cookies
        )
        assert response.status_code == 200

        # Verify that the extractor was created
        response = await client.get("/extractors", cookies=cookies)
        assert response.status_code == 200
        assert len(response.json()) == 1

        # Verify that we can delete an extractor
        get_response = response.json()
        uuid_str = get_response[0]["uuid"]
        _ = uuid.UUID(uuid_str)  # assert valid uuid
        response = await client.delete(f"/extractors/{uuid_str}", cookies=cookies)
        assert response.status_code == 200

        get_response = await client.get("/extractors", cookies=cookies)
        assert get_response.status_code == 200
        assert get_response.json() == []

        # Verify that we can create an extractor, including other properties
        owner_id = str(uuid.uuid4())
        create_request = {
            "name": "my extractor",
            "description": "Test Description",
            "schema": {"type": "object"},
            "instruction": "Test Instruction",
        }
        response = await client.post(
            "/extractors", json=create_request, cookies=cookies
        )
        extractor_uuid = response.json()["uuid"]
        assert response.status_code == 200
        response = await client.get(f"/extractors/{extractor_uuid}", cookies=cookies)
        response_data = response.json()
        assert extractor_uuid == response_data["uuid"]
        assert "my extractor" == response_data["name"]
        assert "owner_id" not in response_data


async def test_sharing_extractor() -> None:
    """Test sharing an extractor."""
    async with get_async_client() as client:
        owner_id = str(uuid.uuid4())
        cookies = {"owner_id": owner_id}
        response = await client.get("/extractors", cookies=cookies)
        assert response.status_code == 200
        assert response.json() == []
        # Verify that we can create an extractor
        create_request = {
            "name": "Test Name",
            "description": "Test Description",
            "schema": {"type": "object"},
            "instruction": "Test Instruction",
        }
        response = await client.post(
            "/extractors", json=create_request, cookies=cookies
        )
        assert response.status_code == 200

        uuid_str = response.json()["uuid"]

        # Generate a share uuid
        response = await client.post(f"/extractors/{uuid_str}/share", cookies=cookies)
        assert response.status_code == 200
        assert "share_uuid" in response.json()
        share_uuid = response.json()["share_uuid"]

        # Test idempotency
        response = await client.post(f"/extractors/{uuid_str}/share", cookies=cookies)
        assert response.status_code == 200
        assert "share_uuid" in response.json()
        assert response.json()["share_uuid"] == share_uuid

        # Check cookies
        bad_cookies = {"owner_id": str(uuid.uuid4())}
        response = await client.post(
            f"/extractors/{uuid_str}/share", cookies=bad_cookies
        )
        assert response.status_code == 404

        # Check that we can retrieve the shared extractor
        response = await client.get(f"/shared/extractors/{share_uuid}")
        assert response.status_code == 200
        keys = sorted(response.json())
        assert keys == ["description", "instruction", "name", "schema"]

        assert response.json() == {
            "description": "Test Description",
            "instruction": "Test Instruction",
            "name": "Test Name",
            "schema": {"type": "object"},
        }
