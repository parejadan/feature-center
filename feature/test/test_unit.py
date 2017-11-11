import pytest
from random import random
from feature.model import ProductTypes, ClientFeatureRequest
from feature.model.logic import update_feature_and_peers


def test_full_safe_serialize_serialize():
    properties = {'product_code': 'telecommunication'}
    definition = ProductTypes(**properties)
    definition.to_dict()


def test_client_feature_request_bad_date_serialize():
    properties = {'date_target': 'cat-date-birthday'}
    with pytest.raises(Exception):
        definition = ClientFeatureRequest(**properties)
        definition.to_dict()


def test_peer_priority_update():
    # generate random set of FeatureRequests where client's option is to only to update ranks
    rank_space = 11
    rank_set = [r+1 for r in range(rank_space)]
    cadets = [ClientFeatureRequest(id=r, priority_id=r) for r in rank_set]

    # choose a random item to promote or demote in priority
    random_promotee = round(random() * rank_space) + 1
    random_rank = round(random() * rank_space) + 1
    promotee = ClientFeatureRequest(id=random_promotee, priority_id=random_rank)  # assign random item's new priority

    print('Item chosen for test: id-{}, rnk-{}'.format(promotee.id, promotee.priority_id))
    print('Original Roster: \n', ''.join(['\tid: {}, rnk: {}\n|'.format(c.id, c.priority_id) for c in cadets]))
    update_feature_and_peers(promotee, cadets)
    print('New Roster: \n', ''.join(['\tid: {}, rnk: {}\n|'.format(c.id, c.priority_id) for c in cadets]))

    # validate we always have unique ranks
    new_ranks_stats = set([c.priority_id for c in cadets])  # set only returns unique tokens from list
    assert len(rank_set) == len(new_ranks_stats)


