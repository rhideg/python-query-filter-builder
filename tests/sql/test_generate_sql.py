from query_filter_builder.sql import generate_sql

FILTER_OBJ = {
    "col1": "<5>=6"
}


def test_generate_with_list_params():
    expected_sql = "((col1 < %s AND col1 >= %s))"
    expected_params = ["5", "6"]
    result_sql, result_params = generate_sql(FILTER_OBJ)
    assert expected_sql == result_sql
    assert expected_params == result_params


def test_generate_with_dict_params():
    expected_sql = "((col1 < %(col1)s AND col1 >= %(col1_)s))"
    expected_params = {"col1": "5", "col1_": "6"}
    result_sql, result_params = generate_sql(FILTER_OBJ, dict_params=True)
    assert expected_sql == result_sql
    assert expected_params == result_params
