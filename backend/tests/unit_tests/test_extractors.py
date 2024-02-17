from unittest.mock import Mock

from fastapi.testclient import TestClient


def test_create_extractor(client: TestClient, mock_db_session: Mock):
    create_request = {
        "description": "Test Description",
        "schema": {"type": "object"},
        "instruction": "Test Instruction",
    }
    response = client.post("/extractors", json=create_request)
    assert response.status_code == 200
    assert len(mock_db_session.add.call_args_list) == 1
    assert len(mock_db_session.commit.call_args_list) == 1


def test_list_extractors(client: TestClient, mock_db_session: Mock):
    extractor_data = [{"description": "Test", "uuid": "1"}]
    response = client.get("/extractors")
    assert response.status_code == 200
    assert response.json() == extractor_data


def test_delete_extractor(client: TestClient, mock_db_session: Mock):
    response = client.delete("/extractors/1")
    assert response.status_code == 200
    assert (
        len(
            mock_db_session.query.return_value.filter_by.return_value.delete.call_args_list
        )
        == 1
    )
    assert len(mock_db_session.commit.call_args_list) == 1
