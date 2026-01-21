"""Add example middleware to enable langsmith tracing on selected endpoints.

This enables langsmith tracing on selected endpoints, showing how to add
tags and metadata to the traces.
"""
from urllib.parse import urlparse

from langchain_core.tracers.context import tracing_v2_enabled
from langsmith import trace
from starlette.requests import Request


async def add_langsmith_tracing(request: Request, call_next):
    """Add langsmith middleware"""
    with tracing_v2_enabled():
        parsed_url = urlparse(str(request.url))
        if parsed_url.path not in {"/suggest", "/extract", "/extract/shared"}:
            # Skip tracing for all other endpoints
            return await call_next(request)

        method = request.method

        with trace(
            name=parsed_url.path,
            tags=[method],
            metadata={
                "__useragent": request.headers.get("user-agent"),
            },
        ):
            response = await call_next(request)
    return response
