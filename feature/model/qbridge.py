import json


def basic_select(table, id=None):
    if id is None:
        query = table.query.order_by('id').all()
        return to_json_dump(query)
    else:
        query = table.query.get(id)
        return to_json_dump(query)


def to_json_dump(obj, seprtrs=(',', ':')):
    try:
        obj_len = len(obj)
        if obj_len > 1:
            dict_list = [o.to_dict() for o in obj]
            return json.dumps(dict_list, separators=seprtrs)
        elif obj_len == 1:
            return json.dumps(obj.to_dict(), separators=seprtrs)
        else:
            return json.dumps([], separators=seprtrs)
    except Exception as ex:
        # todo improve logging
        print('something happened', ex)
