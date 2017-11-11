import json


def update_feature_and_peers(updated_feature, feature_space):
    """updated_feature.id & updated_feature.priority_id is expected to be numeric"""
    try:
        cur_priority = update_feature_data(feature_space, updated_feature)
        update_peer_priority(feature_space, updated_feature, cur_priority)
    except Exception as ex:
        print('exception encountered updating feature : ', ex)


def update_feature_data(feature_space, updated_feature_date):
    """updates feature data in feature_space set with updated_feature_data
       returns: None if the updated_feature_date.id does not exists in feature_space,
       otherwise returns previous priority value for feature being updated"""
    for feature in feature_space:
        if feature.id == updated_feature_date.id:
            previous_priority = feature.priority_id
            feature.title, feature.description = updated_feature_date.title, updated_feature_date.description
            feature.priority_id = updated_feature_date.priority_id
            feature.product_id = updated_feature_date.product_id
            feature.date_target = updated_feature_date.date_target
            return previous_priority
    return None


def update_peer_priority(feature_space, updated_feature, cur_priority):
    """determine feature being updated rank got demoted
       updated_feature: feature that was updated - priority_id is expected to already be updated
       cur_rank: previous priority of updated_feature before it was changed"""
    if cur_priority < updated_feature.priority_id:
        promote_peer_priority(feature_space, updated_feature, cur_priority)  # promote peers
    elif cur_priority > updated_feature.priority_id:
        demote_peer_priority(feature_space, updated_feature, cur_priority)  # demote peers


def promote_peer_priority(feature_space, updated_feature, cur_rank):
    """PROMOTES every one else between your old to new demoted rank
       updated_feature: feature that was updated - priority_id is expected to already be updated
       cur_rank: previous priority of updated_feature before it was changed"""
    for feature in feature_space:
        if feature.id != updated_feature.id:
            # feature's rank is lower (n being the lowest)
            if feature.priority_id > cur_rank:
                # feature's rank is higher (0 being the highest)
                if feature.priority_id <= int(updated_feature.priority_id):
                    feature.priority_id -= 1  # we promote you a rank higher


def demote_peer_priority(feature_space, updated_feature, cur_rank):
    """DEMOTES every one else from your current to new promoted rank
       updated_feature: feature that was updated - priority_id is expected to already be updated
       cur_rank: previous priority of updated_feature before it was changed"""
    for feature in feature_space:
        if feature.id != updated_feature.id:
            # feature's rank is higher (0 being highest)
            if feature.priority_id < cur_rank:
                # feature's rank is lower(n being the lowest)
                if feature.priority_id >= int(updated_feature.priority_id):
                    feature.priority_id += 1


def to_dict(obj):
    """converts feature.model obj (or obj set) set to serialized dict version"""
    if type(obj) in [type([]), type(())]:
        return [o.to_dict() for o in obj]
    elif not(obj is None) and hasattr(obj, 'to_dict'):
        return obj.to_dict()
    else:
        return []


def to_json_dump(obj, cast=True, seprtrs=(',', ':')):
    """serializes feature.model obj or list of objects to json string"""
    try:
        if cast:
            payload = to_dict(obj)
        else:
            payload = obj
        return json.dumps(payload, separators=seprtrs)
    except Exception as ex:
        print('exception encountered serializing object', ex)
