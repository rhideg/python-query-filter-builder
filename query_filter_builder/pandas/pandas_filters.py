import re
from ..patterns import is_compare_pattern, is_like_pattern, is_list_pattern


def _get_list_filter(key: str, val: list, negate: bool) -> (str, list):
    prefix = "not " if negate else ""
    filter_str = f"{prefix}{key} in {str(val)}"
    return filter_str


def _get_like_filter(key: str, val: str, negate: bool) -> (str, list):
    prefix = "not " if negate else ""
    val = str(val).replace("'", "\\'")
    filter_str =\
        f"{prefix}{key}.astype('str').str.contains('{val[1:]}', case=False)"
    return filter_str


def _get_compare_filter(key: str, val: str, negate: bool) -> (str, list):
    prefix = "not " if negate else ""
    filters = []
    compare_types = re.findall(r'[<>]=?', val)
    compare_values = re.split(r'[<>]=?', val)[1:]
    for i, _ in enumerate(compare_types):
        filters.append(
            f"{key} {compare_types[i]} {compare_values[i]}")
    filter_str = f"{prefix}({' and '.join(filters)})"
    return filter_str


def _get_equal_filter(key:str, val: str, negate: bool) -> (str, list):
    prefix = "not " if negate else ""
    val = str(val).replace("'", "\\'")
    filter_str = f"{prefix}{key} == '{val}'"
    return filter_str


def convert_to_pandas_query(filter_obj) -> str:
    filters = filter_obj.get("filters")
    join_type = {"AND": "and", "OR": "or"}\
                .get(filter_obj.get("join")) or "and"
    filters_sqls = []

    for filter in filters:
        if filter.get("filters") is not None:
            filter_str = convert_to_pandas_query(filter)
            filters_sqls.append(filter_str)
            continue

        col_name = filter["col"]
        val = filter["value"]
        negate = filter.get("negate") or False
        if is_list_pattern(val):
            if len(val) == 0:
                continue
            filter_str = _get_list_filter(col_name, val, negate)
            filters_sqls.append(filter_str)

        elif is_like_pattern(val):
            filter_str = _get_like_filter(col_name, val, negate)
            filters_sqls.append(filter_str)

        elif is_compare_pattern(val):
            filter_str = _get_compare_filter(col_name, val, negate)
            filters_sqls.append(filter_str)

        else:
            filter_str = _get_equal_filter(col_name, val, negate)
            filters_sqls.append(filter_str)

    return "(" + f" {join_type} ".join(filters_sqls) + ")"
