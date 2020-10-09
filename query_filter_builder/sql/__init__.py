import json
from ..utils import convert_from_json, validate_filter_obj
from ..version_converts import v0_to_v01
from .sql_filters import convert_to_sql_with_params
from .sql_filter_dict_params import convert_to_sql_with_dict_params

# TODO update function docstring
# TODO add basic column validation ( [A-Za-z0-9_] )

def generate_sql(
    filter_obj, *,
    validate:bool=True,
    valid_cols: list=None,
    list_param_str: str="%s",
    dict_params: bool=False,
    dict_param_str: str="%(key)s",
) -> (str, list or dict):
    """ Creates an sql string and a list of params from a filter_object.
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
    
    if dict_params:
        return convert_to_sql_with_dict_params(filter_obj, dict_param_str)
    else:
        return convert_to_sql_with_params(filter_obj, list_param_str)
