from query_filter_builder.sql.sql_filters import convert_to_sql_with_params

simple_obj = {
    "version": 0.1,
    "filters": [
        {
            "col": "col1",
            "value": "asd",
        },
        {
            "col": "col2",
            "value": "~asd",
        },
        {
            "col": "col3",
            "value": "<42>=40"
        },
        {
            "col": "col4",
            "value": [1, 2, 3]
        }
    ]
}

nested_obj = {
    "version": 0.1,
    "join": "AND",
    "filters": [
        {
            "col": "col1",
            "negate": False,
            "value": "asd"
        },
        {
            "col": "col2",
            "value": "~asd",
        },
        {
            "col": "col3",
            "value": [1, 2, 3]
        },
        {
            "col": "col4",
            "value": "<5>=3.2"
        },
        {
            "join": "OR",
            "filters": [
                {
                    "col": "col5",
                    "negate": True,
                    "value": "negate this value"
                },
                {
                    "col": "col6",
                    "value": "~something like this"
                }
            ]
        }
    ]
}

def test_simple_convert():
    sql, params = convert_to_sql_with_params(simple_obj)
    correct_sql_str = "(col1 = %s AND col2 ILIKE %s AND (col3 < %s AND col3 >= %s) AND col4 IN %s)"
    correct_sql_params = ["asd", "%asd%", "42", "40", (1, 2, 3)]
    assert sql == correct_sql_str
    assert params == correct_sql_params


def test_nested_convert():
    sql, params = convert_to_sql_with_params(nested_obj)
    expected_sql = "(col1 = %s AND col2 ILIKE %s AND col3 IN %s AND (col4 < %s AND col4 >= %s) AND (NOT col5 = %s OR col6 ILIKE %s))"
    expected_params = ["asd", "%asd%", (1, 2, 3), "5", "3.2", "negate this value", "%something like this%"]
    assert sql == expected_sql
    assert params == expected_params


def test_custom_param_str():
    sql, params = convert_to_sql_with_params(simple_obj, "?")
    correct_sql_str = "(col1 = ? AND col2 ILIKE ? AND (col3 < ? AND col3 >= ?) AND col4 IN ?)"
    correct_sql_params = ["asd", "%asd%", "42", "40", (1, 2, 3)]
    assert sql == correct_sql_str
    assert params == correct_sql_params