# Re-add
# from httpx import AsyncClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.pool import StaticPool
#
# from db.models import Base, get_session
# from server.main import app
#
# SQLALCHEMY_DATABASE_URL = "sqlite://"
#
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False},
#     poolclass=StaticPool,
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# Base.metadata.create_all(bind=engine)
#
#
# def override_get_session():
#     try:
#         session = TestingSessionLocal()
#         yield session
#     finally:
#         session.close()
#
#
# app.dependency_overrides[get_session] = override_get_session
#
# client = AsyncClient(app=app, base_url="http://test")
#
# # def test_create_extractor():
# #     create_request = {
# #         "description": "Test Description",
# #         "schema": {"type": "object"},
# #         "instruction": "Test Instruction",
# #     }
# #     response = client.post("/extractors", json=create_request)
# #     assert response.status_code == 200
# #     assert len(mock_db_session.add.call_args_list) == 1
# #     assert len(mock_db_session.commit.call_args_list) == 1
# #
#
#
# async def test_list_extractors():
#     # extractor_data = [{"description": "Test", "uuid": "1"}]
#     response = await client.get("/extractors")
#     assert response.status_code == 200
#     assert response.json() == extractor_data
#
#
# # def test_delete_extractor(client: TestClient, mock_db_session: Mock):
# #     response = client.delete("/extractors/1")
# #     assert response.status_code == 200
# #     assert (
# #         len(
# #             mock_db_session.query.return_value.filter_by.return_value.delete.call_args_list
# #         )
# #         == 1
# #     )
# #     assert len(mock_db_session.commit.call_args_list) == 1
