from __future__ import annotations

import os

from sqlalchemy import create_engine

from sqlalchemy.engine import URL


def get_postgres_url() -> URL:
    return os.environ.get("PG_URL")




# Max concurrency used for extracting content from documents.
# A long document is broken into smaller chunks this controls
# how many chunks are processed concurrently.
MAX_CONCURRENCY = int(os.environ.get("MAX_CONCURRENCY", 1))

# Max number of chunks to process per documents
# When a long document is split into chunks, this controls
# how many of those chunks will be processed.
# Set to 0 or negative to disable the max chunks limit.
MAX_CHUNKS = int(os.environ.get("MAX_CHUNKS", -1))
