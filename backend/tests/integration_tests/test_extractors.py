import uuid

from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from db.models import Base, get_session
from server.main import app

url = URL.create(
    drivername="postgresql",
    username="test_user",
    password="test_pwd",
    host="localhost",
    database="test",
    port=5433,
)

engine = create_engine(url)
TestingSession = sessionmaker(bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_session():
    try:
        session = TestingSession()
        yield session
    finally:
        session.close()


app.dependency_overrides[get_session] = override_get_session

client = AsyncClient(app=app, base_url="http://test")


async def _list_extractors(client: AsyncClient) -> list:
    response = await client.get("/extractors")
    assert response.status_code == 200
    return response.json()


async def test_create_extractor():
    create_request = {
        "description": "Test Description",
        "schema": {"type": "object"},
        "instruction": "Test Instruction",
    }
    response = await client.post("/extractors", json=create_request)
    assert response.status_code == 200


async def test_list_extractors():
    extractor_data = [
        {
            "description": "Test Description",
            "schema": {"type": "object"},
            "instruction": "Test Instruction",
        },
    ]
    get_response = await _list_extractors(client)
    subset_fields = ["description", "schema", "instruction"]
    response_subset = [
        {key: record[key] for key in subset_fields} for record in get_response
    ]
    assert response_subset == extractor_data


async def test_delete_extractor():
    # Get record uuid
    get_response = await _list_extractors(client)
    assert len(get_response) == 1
    uuid_str = get_response[0]["uuid"]
    _ = uuid.UUID(uuid_str)  # assert valid uuid
    response = await client.delete(f"/extractors/{uuid_str}")
    assert response.status_code == 200

    get_response = await _list_extractors(client)
    assert get_response == []
