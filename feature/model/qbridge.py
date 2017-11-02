import json


def basic_select(table, id=None):
    if id is None:
        query = table.query.order_by('id').all()
        return to_json_dump(query)
    else:
        query = table.query.get(id)
        return to_json_dump(query)


def to_json_dump(obj, seprtrs=(',', ':')):
    if len(obj) > 1:
        dict_list = [o.to_dict() for o in obj]
        return json.dump(dict_list, separators=seprtrs)
    else:
        return json.dump(obj.to_dict(), separators=seprtrs)