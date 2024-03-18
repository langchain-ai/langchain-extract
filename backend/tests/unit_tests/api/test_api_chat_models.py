from tests.db import get_async_client


async def test_chat_models_api() -> None:
    async with get_async_client() as client:
        response = await client.get("/chat_models")
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)
        assert all(isinstance(model_name, str) for model_name in result)
        assert "gpt-3.5-turbo" in result
        assert len(result) >= 2
