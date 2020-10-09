from query_filter_builder import v0_to_v01

def test_v0_to_v1():
    v0_object = {
        "col1": "asd",
        "col2": "~asd",
        "col3": [1, 2, 3],
        "col4": "<5>=3.2"
    }
    correct_v1_object = {
        "version": 0.1,
        "filters": [
            {
                "col": "col1",
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
            }
        ]
    }
    test_v1_object = v0_to_v01(v0_object)
    assert test_v1_object == correct_v1_object
