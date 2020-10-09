import pytest
from query_filter_builder.exceptions import InvalidFilterError
from query_filter_builder.utils import convert_from_json


def test_convert_from_json():
    test_json = """
    {
        "join": "AND",
        "filters": [
             {"col": "col1", "value": "asd"},
             {"col": "col2", "value": [1, 2, 3], "negate": true}
        ]
    }
    """
    expected_dict = {
        "join": "AND",
        "filters": [
            {"col": "col1", "value": "asd"},
            {"col": "col2", "value": [1, 2, 3], "negate": True}
        ]
    }
    assert convert_from_json(test_json) == expected_dict

    invalid_json = """
    {
        "filters": [
            {"col": "asd", "value": asd}
        ]
    }
    """
    with pytest.raises(InvalidFilterError):
        convert_from_json(invalid_json)
