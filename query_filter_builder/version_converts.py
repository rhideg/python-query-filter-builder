
def v0_to_v01(v0_object):
    filters = []
    v1_object = {
        "version": 0.1,
        "filters": filters
    }
    for key, val in v0_object.items():
        filters.append({
            "col": key,
            "value": val
        })
    return v1_object
