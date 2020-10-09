import re
from ..patterns import is_compare_pattern, is_like_pattern, is_list_pattern


def _get_list_filter(key: str, val: list, negate: bool,
                     param_str) -> (str, list):
    prefix = "NOT " if negate else ""
    filter_str = f"{prefix}{key} IN {param_str}"
    filter_param = tuple(val)
    return filter_str, [filter_param]


def _get_like_filter(key: str, val: str, negate: bool,
                     param_str) -> (str, list):
    prefix = "NOT " if negate else ""
    filter_str = f"{prefix}{key} ILIKE {param_str}"
    filter_param = f"%{val[1:]}%"
    return filter_str, [filter_param]


def _get_compare_filter(key: str, val: str, negate: bool,
                        param_str) -> (str, list):
    prefix = "NOT " if negate else ""
    filters = []
    filter_params = []
    compare_types = re.findall(r'[<>]=?', val)
    compare_values = re.split(r'[<>]=?', val)[1:]
    for i, _ in enumerate(compare_types):
        filters.append(
            f"{key} {compare_types[i]} {param_str}")
        filter_params.append(compare_values[i])
    filter_str = f"{prefix}({' AND '.join(filters)})"
    return filter_str, filter_params


def _get_equal_filter(key:str, val: str, negate: bool,
                      param_str) -> (str, list):
    prefix = "NOT " if negate else ""
    filter_str = f"{prefix}{key} = {param_str}"
    filter_param = val
    return filter_str, [filter_param]


def convert_to_sql_with_params(filter_obj, param_str="%s") -> (str, list):
    filters = filter_obj.get("filters")
    join_type = filter_obj.get("join") or "AND"
    filters_sqls = []
    filter_params = []

    for filter in filters:
        if filter.get("filters") is not None:
            filter_str, filter_param = convert_to_sql_with_params(filter)
            filters_sqls.append(filter_str)
            filter_params.extend(filter_param)
            continue

        col_name = filter["col"]
        val = filter["value"]
        negate = filter.get("negate") or False
        if is_list_pattern(val):
            if len(val) == 0:
                continue
            filter_str, filter_param =\
                _get_list_filter(col_name, val, negate, param_str)
            filters_sqls.append(filter_str)
            filter_params.append(*filter_param)

        elif is_like_pattern(val):
            filter_str, filter_param =\
                 _get_like_filter(col_name, val, negate, param_str)
            filters_sqls.append(filter_str)
            filter_params.extend(filter_param)

        elif is_compare_pattern(val):
            filter_str, filter_param =\
                _get_compare_filter(col_name, val, negate, param_str)
            filters_sqls.append(filter_str)
            filter_params.extend(filter_param)

        else:
            filter_str, filter_param =\
                _get_equal_filter(col_name, val, negate, param_str)
            filters_sqls.append(filter_str)
            filter_params.extend(filter_param)

    return "(" + f" {join_type} ".join(filters_sqls) + ")", filter_params
