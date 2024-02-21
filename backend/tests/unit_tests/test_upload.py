from server.api.upload import _guess_mimetype
from tests.unit_tests.fixtures import get_sample_paths


async def test_mimetype_guessing() -> None:
    """Verify mimetype guessing for all fixtures."""
    name_to_mime = {}
    for file in sorted(get_sample_paths()):
        data = file.read_bytes()
        name_to_mime[file.name] = _guess_mimetype(data)

    assert {
        "sample.docx": (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ),
        "sample.epub": "application/epub+zip",
        "sample.html": "text/html",
        "sample.odt": "application/vnd.oasis.opendocument.text",
        "sample.pdf": "application/pdf",
        "sample.rtf": "text/rtf",
        "sample.txt": "text/plain",
    } == name_to_mime
