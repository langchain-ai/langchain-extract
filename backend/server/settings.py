from sqlalchemy.engine import URL


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
