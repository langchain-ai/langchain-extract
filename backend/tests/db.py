"""Utility code that sets up a test database and client for tests."""
import os
from contextlib import asynccontextmanager
from typing import Generator

# We'll need to fix the handling of env variables for testing purposes
# This is fine for now.
os.environ["OPENAI_API_KEY"] = "placeholder"

from httpx import AsyncClient
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base, get_session
from server.main import app

url = URL.create(
    drivername="postgresql",
    username="langchain",
    password="langchain",
    host="localhost",
    database="langchain_test",
    port=5432,
)
engine = create_engine(url)
TestingSession = sessionmaker(bind=engine)


def override_get_session() -> Generator[TestingSession, None, None]:
    """Override the get_session dependency with a test session.

    This fixture also re-creats the database before each test and drops it after to
    ensure a clean slate for each test.
    """
    try:
        session = TestingSession()
        yield session
    finally:
        session.close()


app.dependency_overrides[get_session] = override_get_session


@asynccontextmanager
async def get_async_client() -> AsyncClient:
    """Get an async client."""
    # Clear the database before each test
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    async_client = AsyncClient(app=app, base_url="http://test")
    try:
        yield async_client
    finally:
        await async_client.aclose()
