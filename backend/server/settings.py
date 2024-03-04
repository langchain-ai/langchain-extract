from __future__ import annotations

import os

from langchain_openai import ChatOpenAI
from sqlalchemy.engine import URL

MODEL_NAME = "gpt-3.5-turbo-0125"
CHUNK_SIZE = int(4_096 * 0.8)
# Max concurrency for the model.
MAX_CONCURRENCY = 1


def get_postgres_url() -> URL:
    url = URL.create(
        drivername="postgresql",
        username="langchain",
        password="langchain",
        host=os.environ.get("PG_HOST", "localhost"),
        database="langchain",
        port=5432,
    )
    return url


def get_model() -> ChatOpenAI:
    """Get the model."""
    return ChatOpenAI(model=MODEL_NAME, temperature=0)
