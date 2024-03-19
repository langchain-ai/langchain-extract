from __future__ import annotations

import os

from sqlalchemy.engine import URL


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
