import pandas as pd
from query_filter_builder.pandas.pandas_filters import convert_to_pandas_query

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
        },
        {
            "col": "col5",
            "value": 42
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
    query_str = convert_to_pandas_query(simple_obj)
    expected_query_str = "(col1 == 'asd' and col2.astype('str').str.contains('asd', case=False) and "\
                         + "(col3 < 42 and col3 >= 40) and col4 in [1, 2, 3]"\
                         + " and col5 == '42')"
    assert query_str == expected_query_str


def test_nested_convert():
    query_str = convert_to_pandas_query(nested_obj)
    expected_query_str = "(col1 == 'asd' and col2.astype('str').str.contains('asd', case=False)"\
                         + " and col3 in [1, 2, 3] and (col4 < 5 and col4 >= 3.2)"\
                         + " and (not col5 == 'negate this value'"\
                         + " or col6.astype('str').str.contains('something like this', case=False)))"
    assert query_str == expected_query_str


def test_filter_works():
    df = pd.DataFrame({
        "A": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "B": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        "C": ["a", "b", "c", "d", "e", "a", "b", "c", "d", "e"]
    })

    filter = {"filters": [
        {"col": "A", "value": ">=0<5"},
        {"col": "C", "value": ['a', 'b', 'c', 'd']},
        {"col": "C", "value": "d", "negate": True},
        {
            "join": "OR",
            "filters": [
            {"col": "B", "value": 10},
            {"col": "B", "value": "~9"},
            {"col": "C", "value": "'C"}
        ]}
    ]}

    expected_df = pd.DataFrame({
        "A": [0, 1],
        "B": [10, 9],
        "C": ["a", "b"]
    })

    result_df = df.query(convert_to_pandas_query(filter))
    assert expected_df.equals(result_df)
