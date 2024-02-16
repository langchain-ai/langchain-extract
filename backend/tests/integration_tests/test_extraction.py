"""Makes it easy to run an integration tests using a real chat model."""
from contextlib import asynccontextmanager
from typing import Optional

import httpx
from fastapi import FastAPI
from httpx import AsyncClient

from server.main import app


@asynccontextmanager
async def get_async_test_client(
    server: FastAPI, *, path: Optional[str] = None, raise_app_exceptions: bool = True
) -> AsyncClient:
    """Get an async client."""
    url = "http://localhost:9999"
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
    async with get_async_test_client(app) as client:
        result = await client.post(
            "/extract_from_text", json={"text": "hello", "schema": {}}
        )
        assert result.status_code == 200, result.text
