"""Code to test API endpoints."""
import tempfile
from unittest.mock import patch
from uuid import UUID, uuid4

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import FakeEmbeddings
from langchain_core.runnables import RunnableLambda

from tests.db import get_async_client


def mock_extraction_runnable(*args, **kwargs):
    """Mock the extraction_runnable function."""
    extract_request = args[0]
    return {
        "data": [
            extract_request.text[:10],
        ]
    }


def mock_text_splitter(*args, **kwargs):
    return CharacterTextSplitter()


def mock_embeddings(*args, **kwargs):
    return FakeEmbeddings(size=10)


@patch(
    "server.extraction_runnable.extraction_runnable",
    new=RunnableLambda(mock_extraction_runnable),
)
@patch(
    "server.retrieval.extraction_runnable",
    new=RunnableLambda(mock_extraction_runnable),
)
@patch("server.extraction_runnable.TokenTextSplitter", mock_text_splitter)
@patch("server.retrieval.OpenAIEmbeddings", mock_embeddings)
async def test_extract_from_file() -> None:
    """Test extract from file API."""
    async with get_async_client() as client:
        owner_id = str(uuid4())
        cookies = {"owner_id": owner_id}
        # Test with invalid extractor
        extractor_id = UUID(int=1027)  # 1027 is a good number.
        response = await client.post(
            "/extract",
            data={
                "extractor_id": str(extractor_id),
                "text": "Test Content",
            },
            cookies=cookies,
        )
        assert response.status_code == 404, response.text

        # First create an extractor
        create_request = {
            "name": "Test Name",
            "description": "Test Description",
            "schema": {"type": "object"},
            "instruction": "Test Instruction",
        }
        response = await client.post(
            "/extractors", json=create_request, cookies=cookies
        )
        assert response.status_code == 200, response.text
        # Get the extractor id
        extractor_id = response.json()["uuid"]

        # Run an extraction.
        # We'll use multi-form data here.
        response = await client.post(
            "/extract",
            data={
                "extractor_id": extractor_id,
                "text": "Test Content",
                "mode": "entire_document",
            },
            cookies={"owner_id": owner_id},
        )
        assert response.status_code == 200
        assert response.json() == {"data": ["Test Conte"]}

        # Vary chat model
        response = await client.post(
            "/extract",
            data={
                "extractor_id": extractor_id,
                "text": "Test Content",
                "mode": "entire_document",
                "model_name": "gpt-3.5-turbo",
            },
            cookies={"owner_id": owner_id},
        )
        assert response.status_code == 200
        assert response.json() == {"data": ["Test Conte"]}

        # Test retrieval
        response = await client.post(
            "/extract",
            data={
                "extractor_id": extractor_id,
                "text": "Test Content",
                "mode": "retrieval",
            },
            cookies={"owner_id": owner_id},
        )
        assert response.status_code == 200
        assert response.json() == {"data": ["Test Conte"]}

        # We'll use multi-form data here.
        # Create a named temporary file
        with tempfile.NamedTemporaryFile(mode="w+t", delete=False) as f:
            f.write("This is a named temporary file.")
            f.seek(0)
            f.flush()
            response = await client.post(
                "/extract",
                data={
                    "extractor_id": extractor_id,
                    "mode": "entire_document",
                },
                files={"file": f},
                cookies={"owner_id": owner_id},
            )

        assert response.status_code == 200, response.text
        assert response.json() == {"data": ["This is a "]}

        # Test file size constraint
        with patch("extraction.parsing._get_file_size_in_mb", return_value=20):
            with tempfile.NamedTemporaryFile(mode="w+t", delete=False) as f:
                f.write("This is a named temporary file.")
                f.seek(0)
                f.flush()
                response = await client.post(
                    "/extract",
                    data={
                        "extractor_id": extractor_id,
                        "mode": "entire_document",
                    },
                    files={"file": f},
                    cookies={"owner_id": owner_id},
                )
            assert response.status_code == 413

        # Test page number constraint
        with patch("extraction.parsing._get_pdf_page_count", return_value=100), patch(
            "extraction.parsing._guess_mimetype", return_value="application/pdf"
        ), tempfile.NamedTemporaryFile(mode="w+t", delete=False) as f:
            f.write("This is a named temporary file.")
            f.seek(0)
            f.flush()

            response = await client.post(
                "/extract",
                data={
                    "extractor_id": extractor_id,
                    "mode": "entire_document",
                },
                files={"file": f.name},
                cookies={"owner_id": owner_id},
            )

            assert response.status_code == 413
