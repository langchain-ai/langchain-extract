"""Makes it easy to run an integration tests using a real chat model."""
from contextlib import asynccontextmanager
from typing import Optional

import httpx
from fastapi import FastAPI
from httpx import AsyncClient
from langchain_core.pydantic_v1 import BaseModel

from server.main import app


@asynccontextmanager
async def get_async_test_client(
    server: FastAPI, *, path: Optional[str] = None, raise_app_exceptions: bool = True
) -> AsyncClient:
    """Get an async client."""
    url = "http://localhost:9999/"
    if path:
        url += path
    transport = httpx.ASGITransport(
        app=server,
        raise_app_exceptions=raise_app_exceptions,
    )
    async_client = AsyncClient(app=server, base_url=url, transport=transport)
    try:
        yield async_client
    finally:
        await async_client.aclose()


async def test_extraction_api() -> None:
    """Test the extraction API endpoint."""

    class Person(BaseModel):
        age: Optional[int]
        name: Optional[str]
        alias: Optional[str]

    async with get_async_test_client(app) as client:
        text = """
        My name is Chester. I am young. I love cats. I have two cats. My age
        is the number of cats I have to the power of 5. (Approximately.)
        I also have a friend. His name is Neo. He is older than me. He is
        also a cat lover. He has 3 cats. He is 25 years old.
        """
        result = await client.post(
            "/extract_text/invoke",
            json={"input": {"text": text, "schema": Person.schema()}},
        )
        assert result.status_code == 200, result.text
        response_data = result.json()
        assert response_data == {}
        assert isinstance(response_data["output"]["data"], list)

        # Test with instructions
        result = await client.post(
            "/extract_text/invoke",
            json={
                "input": {
                    "text": text,
                    "schema": Person.schema(),
                    "instructions": "Very important: Chester's alias is Neo.",
                }
            },
        )
        response_data = result.json()
        assert result.status_code == 200, result.text

        # Test with few shot examples
        examples = [
            {
                "text": "My name is Grung. I am 100.",
                "output": [Person(age=100, name="######").dict()],
            },
        ]
        result = await client.post(
            "/extract_text/invoke",
            json={
                "input": {
                    "text": text,
                    "schema": Person(),
                    "instructions": "Redact all names using the characters `######`",
                    "examples": examples,
                }
            },
        )
        assert result.status_code == 200, result.text
