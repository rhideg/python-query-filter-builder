# query-filter-builder

#### filter object types:

##### v0.0

```
{
    "col1": "asd",
    "col2": "~asd",
    "col3": [1, 2, 3],
    "col4": "<5>=3.2"
}
```

* sql string: `(col1 = %s AND col2 ILIKE %s AND col3 IN %s AND (col4 < %s AND col4 >= %s))` 
* params: `["asd", "%asd%", (1, 2, 3), "5", "3.2"]`

##### v0.1
```
{
    "version": 0.1,
    "join": "AND",    # AND, OR (default: AND)
    "filters": [
        {
            "col": "col1",
            "negate": False,    # True, False (default: False)
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
```

###### built sql string with params:

* sql string: `"(col1 = %s AND col2 ILIKE %s AND col3 IN %s AND (col4 < %s AND col4 >= %s) AND (NOT col5 = %s OR col6 ILIKE %s))"` 
* params: `["asd", "%asd%", (1, 2, 3), "5", "3.2", "negate this value", "%something like this%"]`


### update local package:
`python setup.py sdist upload -r local`
