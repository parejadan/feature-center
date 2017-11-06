import pytest
from random import random
from feature.model import ProductTypes, ClientFeatureRequest
from feature.model.logic import update_peer_priority


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
    rank_space = 11
    ranks = [r for r in range(rank_space)]
    random_promotee = round(random() * rank_space)  # choose a random rookie to promote
    random_rank = round(random() * rank_space)  # choose a random rank to promote to
    cadets = [ClientFeatureRequest(id=r, priority_id=r) for r in ranks]  # create peers
    # assign the random promotee it's new rank
    promotee = ClientFeatureRequest(id=random_promotee, priority_id=random_rank)
    # demote or promote peers to accommodate change
    update_peer_priority(cadets, promotee, random_promotee)
    # validate we always have unique ranks
    new_ranks_stats = [c.priority_id for c in cadets]
    assert len(ranks) == len(new_ranks_stats)


