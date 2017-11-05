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


def promote_peer_priority(query, updated_feature, cur_rank):
    """Promote every one else between your old to new demoted rank"""
    for feature in query:
        if feature.id != updated_feature.id:
            # feature's rank is lower (n being the lowest)
            if feature.priority_id > cur_rank:
                # feature's rank is higher (0 being the highest)
                if feature.priority_id <= int(updated_feature.priority_id):
                    feature.priority_id -= 1  # we promote you a rank higher


def demote_peer_priority(query, updated_feature, cur_rank):
    """demote every one else from your current to new promoted rank"""
    for feature in query:
        if feature.id != updated_feature.id:
            # feature's rank is higher (0 being highest)
            if feature.priority_id < cur_rank:
                # feature's rank is lower(n being the lowest)
                if feature.priority_id >= int(updated_feature.priority_id):
                    feature.priority_id += 1


def update_features_request(updated_feature, query):
    try:
        cur_priority = -1
        for feature in query:
            if feature.id == int(updated_feature.id):  # update all the information for supplied priority
                cur_priority = int(feature.priority_id)
                feature.title, feature.description = updated_feature.title, updated_feature.description
                feature.priority_id = int(updated_feature.priority_id)
                feature.product_id = int(updated_feature.product_id)
                feature.date_target = updated_feature.date_target
        # determine feature being updated rank got demoted
        if cur_priority < int(updated_feature.priority_id):
            promote_peer_priority(query, updated_feature, cur_priority)  # promote peers
        elif cur_priority > int(updated_feature.priority_id):
            demote_peer_priority(query, updated_feature, cur_priority)  # demote peers
        db.session.commit()
        return True
    except Exception as ex:
        print('exception encountered commiting transaction: ', ex)
        return False


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
