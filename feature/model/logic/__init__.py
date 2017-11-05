import json
from feature.model import db


def basic_select(table, id=None):
    try:
        if id is None:
            query = table.query.order_by('id').all()
            return to_json_dump(query)
        else:
            query = table.query.get(id)
            return to_json_dump(query)
    except Exception as ex:
        print('exception encountered pulling records for {]:'.format(table), ex)


def basic_insert(trans):
    try:
        db.session.add(trans)
        db.session.commit()
    except Exception as ex:
        print('exception encountered executing transaction', ex)


def to_dict(obj):
    obj_len = len(obj)
    if obj_len > 1:
        return [o.to_dict() for o in obj]
    elif obj_len == 1:
        return [obj[0].to_dict()]
    else:
        return []


def to_json_dump(obj, cast=True, seprtrs=(',', ':')):
    try:
        if cast:
            payload = to_dict(obj)
        else:
            payload = obj
        return json.dumps(payload, separators=seprtrs)
    except Exception as ex:
        print('exception encountered serializing object', ex)
