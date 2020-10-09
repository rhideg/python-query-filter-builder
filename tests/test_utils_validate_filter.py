import pytest
from query_filter_builder.exceptions import InvalidFilterError
from query_filter_builder.utils import validate_filter_obj

def test_validate_basic_filter():
    valid_filter = {
        "filters": [
            {"col": "col1", "value": "~asd"},
            {"col": "col2", "value": [1, 2, 3]}
        ]
    }

    assert validate_filter_obj(valid_filter) == True


VALID_NESTED_FILTER = {
    "version": 0.1,
    "join": "AND",
    "filters": [
        {
            "join": "OR",
            "filters": [
                {"col": "col1", "value": "this", "negate": True},
                {"col": "col2", "value": "~like that"},
            ]
        },
        {
            "join": "OR",
            "filters": [
                {"col": "col3", "value": "dsa"},
                {"col": "col4", "value": "~like asd"},
                {"filters": [{"col": "col5", "value": "double nested"}]}
            ]
        }
    ]
}


def test_validate_nested_filter():
    assert validate_filter_obj(VALID_NESTED_FILTER) == True

    valid_cols = ["col1", "col2", "col3", "col4", "col5"]
    assert validate_filter_obj(VALID_NESTED_FILTER, valid_cols=valid_cols)


def test_valudate_invalid_cols():
    valid_cols = ["col1", "col2", "col3", "col4"]
    with pytest.raises(InvalidFilterError):
        validate_filter_obj(VALID_NESTED_FILTER, valid_cols=valid_cols)


def test_validate_joins():
    invalid_join_filter = {
        "join": "asd",
        "filters": []
    }
    with pytest.raises(InvalidFilterError):
        validate_filter_obj(invalid_join_filter)


def test_validate_negate():
    invalid_negate_filter = {
        "filters": [
            {"col": "col1", "value": "asd", "negate": "asd"}
        ]
    }
    with pytest.raises(InvalidFilterError):
        validate_filter_obj(invalid_negate_filter)


def test_validate_missing_value():
    missing_value_filter = {
        "filters": [
            {"col": "col1"},
            {"col": "col2", "value": "asd"}
        ]
    }
    with pytest.raises(InvalidFilterError):
        validate_filter_obj(missing_value_filter)


def test_invalid_value():
    invalid_value_filter = {
        "filters": [
            {"col": "col1", "value": {"oh shit": "a nested object!"}}
        ]
    }
    with pytest.raises(InvalidFilterError):
        validate_filter_obj(invalid_value_filter)


def test_converts_from_json():
    filter_in_json = '{"filters":[{"col":"col1","value":"asd"}]}'
    assert validate_filter_obj(filter_in_json, is_json=True) == True
