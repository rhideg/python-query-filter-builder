import pandas as pd
from query_filter_builder.pandas_filters import convert_to_pandas_query

df = pd.DataFrame({
    "A": range(10),
    "B": range(10, 0, -1),
    "C": [ch for ch in "abcde" * 2]
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
print(convert_to_pandas_query(filter))

print_df = df.query(convert_to_pandas_query(filter))
assert print_df.equals(expected_df)

# print_df = df.query("A.astype('str').str.contains('1')")
print(print_df)
