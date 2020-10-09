from ..utils import convert_from_json, validate_filter_obj
from ..exceptions import InvalidFilterError
from .pandas_filters import convert_to_pandas_query
from ..version_converts import v0_to_v01

def generate_query_str(
    filter_obj, *,
    validate:bool=True,
    valid_cols: list=None
) -> (str):
    """ Creates pandas query string from a filter_object.
    Raises InvalidFilter error if validate is true
    or filter_obj is an invalid JSON string.

    params:
    filter_obj -- can be a dict or JSON string,
                  can use v0.0 or v0.1 type filter_object,
                  can omit {"filters": ..} and just pass the list
    validate   -- runs a validation before trying to create the sql,
                  raises InvalidFilterError if filter_obj is invalid
    valid_cols -- if passed and validation is True,
                  checks if cols in filter_obj match cols in valid_cols
    """
    if isinstance(filter_obj, str):
        convert_from_json(filter_obj)

    if isinstance(filter_obj, list):
        filter_obj = {
            "filters": filter_obj
        }

    if filter_obj.get("filters") is None:
        filter_obj = v0_to_v01(filter_obj)

    if validate:
        validate_filter_obj(filter_obj, valid_cols=valid_cols)
    
    return convert_to_pandas_query(filter_obj)
