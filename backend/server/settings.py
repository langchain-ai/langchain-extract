from sqlalchemy.engine import URL

MODEL_NAME = "gpt-3.5-turbo"
CHUNK_SIZE = int(4_096 * 0.8)


def get_postgres_url():
    url = URL.create(
        drivername="postgresql",
        username="langchain",
        password="langchain",
        host="localhost",
        database="langchain",
        port=5432,
    )
    return url
