from server.extraction_runnable import ExtractResponse, _deduplicate


async def test_deduplication_different_resutls() -> None:
    """Test deduplication of extraction results."""
    result = _deduplicate(
        [
            {"data": [{"name": "Chester", "age": 42}]},
            {"data": [{"name": "Jane", "age": 42}]},
        ]
    )
    expected = ExtractResponse(
        data=[
            {"name": "Chester", "age": 42},
            {"name": "Jane", "age": 42},
        ]
    )
    assert expected == result

    result = _deduplicate(
        [
            {
                "data": [
                    {"field_1": 1, "field_2": "a"},
                    {"field_1": 2, "field_2": "b"},
                ]
            },
            {
                "data": [
                    {"field_1": 1, "field_2": "a"},
                    {"field_1": 2, "field_2": "c"},
                ]
            },
        ]
    )

    expected = ExtractResponse(
        data=[
            {"field_1": 1, "field_2": "a"},
            {"field_1": 2, "field_2": "b"},
            {"field_1": 2, "field_2": "c"},
        ]
    )
    assert expected == result

    # Test with data being a list of strings
    result = _deduplicate([{"data": ["1", "2"]}, {"data": ["1", "3"]}])
    expected = ExtractResponse(data=["1", "2", "3"])
    assert expected == result

    # Test with data being a mix of integer and string
    result = _deduplicate([{"data": [1, "2"]}, {"data": ["1", "3"]}])
    expected = ExtractResponse(data=[1, "2", "1", "3"])
    assert expected == result
