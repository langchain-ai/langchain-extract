import pytest

from server.validators import validate_json_schema


def test_validate_json_schema() -> None:
    """Test validate_json_schema."""
    # TODO: Validate more extensively to make sure that it actually validates
    # the schema as expected.
    with pytest.raises(Exception):
        validate_json_schema({"type": "meow"})

    with pytest.raises(Exception):
        validate_json_schema({"type": "str"})

    validate_json_schema({"type": "string"})
