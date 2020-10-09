import json
from .exceptions import InvalidFilterError


def convert_from_json(filter_obj):
    try:
        return json.loads(filter_obj)
    except json.JSONDecodeError as err:
        message = "could not parse filter object from JSON"
        raise InvalidFilterError(message) from err    


def validate_filter_obj(filter_obj, is_json=False, valid_cols=None):
    if is_json:
        filter_obj = convert_from_json(filter_obj)

    join = filter_obj.get("join")
    if join is not None and join not in ("AND", "OR"):
        raise InvalidFilterError("join must be one of ('AND', 'OR')")
    
    filters = filter_obj.get("filters")
    if filters is None:
        return
    
    for filter in filters:
        is_nested = filter.get("filters") is not None
        if is_nested:
            validate_filter_obj(filter, valid_cols=valid_cols)
            continue

        col = filter.get("col")
        if col is None:
            raise InvalidFilterError("col required")
        if valid_cols is not None and not col in valid_cols:
            raise InvalidFilterError(f"invalid value for 'col': {col}")

        negate = filter.get("negate")
        if negate is not None and not isinstance(negate, bool):
            raise InvalidFilterError(f"invalid value for 'negate': {negate}")

        val = filter.get("value")
        if val is None or not isinstance(val, (list, str, int, float)):
            raise InvalidFilterError("'value' is required")

    return True
