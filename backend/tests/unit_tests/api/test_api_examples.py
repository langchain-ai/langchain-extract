"""Code to test API endpoints."""
import uuid

from tests.db import get_async_client


async def _list_extractors() -> list:
    async with get_async_client() as client:
        response = await client.get("/extractors")
        assert response.status_code == 200
        return response.json()


async def test_examples_api() -> None:
    """Runs through a set of API calls to test the examples API."""
    async with get_async_client() as client:
        # First create an extractor
        user_id = str(uuid.uuid4())
        headers = {"x-key": user_id}
        create_request = {
            "description": "Test Description",
            "name": "Test Name",
            "schema": {"type": "object"},
            "instruction": "Test Instruction",
        }
        response = await client.post(
            "/extractors", json=create_request, headers=headers
        )
        assert response.status_code == 200
        # Get the extractor id
        extractor_id = response.json()["uuid"]

        # Let's verify that there are no examples
        response = await client.get(
            "/examples?extractor_id=" + extractor_id, headers=headers
        )
        assert response.status_code == 200
        assert response.json() == []

        # Now let's create an example
        create_request = {
            "extractor_id": extractor_id,
            "content": "Test Content",
            "output": [
                {
                    "age": 100,
                    "name": "Grung",
                }
            ],
        }
        response = await client.post("/examples", json=create_request, headers=headers)
        assert response.status_code == 200
        example_id = response.json()["uuid"]

        # Check headers
        bad_headers = {"x-key": str(uuid.uuid4())}
        response = await client.post(
            "/examples", json=create_request, headers=bad_headers
        )
        assert response.status_code == 404

        # Verify that the example was created
        response = await client.get(
            "/examples?extractor_id=" + extractor_id, headers=headers
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

        keys = ["content", "extractor_id", "output", "uuid"]
        projected_response = {
            key: record[key] for key in keys for record in response.json()
        }
        assert projected_response == {
            "content": "Test Content",
            "extractor_id": extractor_id,
            "output": [
                {
                    "age": 100,
                    "name": "Grung",
                }
            ],
            "uuid": example_id,
        }

        # Check headers
        response = await client.get(
            "/examples?extractor_id=" + extractor_id, headers=bad_headers
        )
        assert response.status_code == 404

        # Check we need cookie to delete
        response = await client.delete(f"/examples/{example_id}", headers=bad_headers)
        assert response.status_code == 404

        # Verify that we can delete an example
        response = await client.delete(f"/examples/{example_id}", headers=headers)
        assert response.status_code == 200

        # Verify that the example was deleted
        response = await client.get(
            "/examples?extractor_id=" + extractor_id, headers=headers
        )
        assert response.status_code == 200
        assert response.json() == []
