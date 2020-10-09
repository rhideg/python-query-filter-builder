from query_filter_builder.sql.sql_filter_dict_params import convert_to_sql_with_dict_params

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
    sql, params = convert_to_sql_with_dict_params(simple_obj, ":key")
    expected_sql_str = "(col1 = :col1 AND col2 ILIKE :col2 AND (col3 < :col3 AND col3 >= :col3_) AND col4 IN :col4)"
    expected_sql_params = {
        "col1": "asd",
        "col2": "%asd%",
        "col3": "42",
        "col3_": "40",
        "col4": (1, 2, 3)
    }
    assert sql == expected_sql_str
    assert params == expected_sql_params


def test_nested_convert():
    sql, params = convert_to_sql_with_dict_params(nested_obj, ":key")
    expected_sql = "(col1 = :col1 AND col2 ILIKE :col2 AND col3 IN :col3 AND (col4 < :col4 AND col4 >= :col4_) AND (NOT col5 = :col5 OR col6 ILIKE :col6))"
    expected_params = {
        "col1": "asd",
        "col2": "%asd%",
        "col3": (1, 2, 3),
        "col4": "5",
        "col4_": "3.2",
        "col5": "negate this value",
        "col6": "%something like this%"
    }
    print("**")
    print(sql)
    print(expected_sql)
    assert sql == expected_sql
    assert params == expected_params
