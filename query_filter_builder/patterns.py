import re

def is_list_pattern(val):
    return isinstance(val, list)


def is_like_pattern(val):
    return isinstance(val, str) and val[0] == '~'


def is_compare_pattern(val):
    compare_pattern = r'^([<>]=?[^<>=]+){1,2}$'
    return re.fullmatch(compare_pattern, str(val)) is not None
