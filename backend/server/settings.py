from __future__ import annotations

import os

from sqlalchemy.engine import URL


def get_postgres_url() -> URL:
    if "INSTANCE_UNIX_SOCKET" in os.environ:
        return URL.create(
            drivername="postgresql",
            username=os.environ.get("PG_USER", "langchain"),
            password=os.environ.get("PG_PASSWORD", "langchain"),
            host=os.environ.get("PG_HOST", "localhost"),
            database=os.environ.get("PG_DATABASE", "langchain"),
            query={
                "unix_socket": os.environ["INSTANCE_UNIX_SOCKET"],
            },
        )

    url = URL.create(
        drivername="postgresql",
        username=os.environ.get("PG_USER", "langchain"),
        password=os.environ.get("PG_PASSWORD", "langchain"),
        host=os.environ.get("PG_HOST", "localhost"),
        database=os.environ.get("PG_DATABASE", "langchain"),
        port=5432,
    )
    return url
