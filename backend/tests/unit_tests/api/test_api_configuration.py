from tests.db import get_async_client


async def test_configuration_api() -> None:
    """Test the configuration API."""
    async with get_async_client() as client:
        response = await client.get("/configuration")
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, dict)
        assert sorted(result) == [
            "accepted_mimetypes",
            "available_models",
            "max_file_size_mb",
        ]
        models = result["available_models"]
        assert all(isinstance(model_name, str) for model_name in models)
        assert "gpt-3.5-turbo" in models
        assert len(models) >= 2
