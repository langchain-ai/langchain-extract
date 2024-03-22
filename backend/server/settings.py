from __future__ import annotations

import os

from sqlalchemy.engine import URL


def get_postgres_url() -> URL:
    if "INSTANCE_UNIX_SOCKET" in os.environ:
        return URL.create(
            drivername="postgresql+psycopg2",
            username=os.environ.get("PG_USER", "langchain"),
            password=os.environ.get("PG_PASSWORD", "langchain"),
            database=os.environ.get("PG_DATABASE", "langchain"),
            query={
                "host": os.environ["INSTANCE_UNIX_SOCKET"],
            },
        )

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ.get("PG_USER", "langchain"),
        password=os.environ.get("PG_PASSWORD", "langchain"),
        host=os.environ.get("PG_HOST", "localhost"),
        database=os.environ.get("PG_DATABASE", "langchain"),
        port=5432,
    )
    return url


# Max concurrency used for extracting content from documents.
# A long document is broken into smaller chunks this controls
# how many chunks are processed concurrently.
MAX_CONCURRENCY = int(os.environ.get("MAX_CONCURRENCY", 1))

# Max number of chunks to process per documents
# When a long document is split into chunks, this controls
# how many of those chunks will be processed.
# Set to 0 or negative to disable the max chunks limit.
MAX_CHUNKS = int(os.environ.get("MAX_CHUNKS", -1))
