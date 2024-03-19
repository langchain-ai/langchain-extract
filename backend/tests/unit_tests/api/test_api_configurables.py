from tests.db import get_async_client


async def test_configurables_api() -> None:
    async with get_async_client() as client:
        response = await client.get("/configurables")
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, dict)

        assert "models" in result
        models = result["models"]
        assert all(isinstance(model_name, str) for model_name in models)
        assert "gpt-3.5-turbo" in models
        assert len(models) >= 2
