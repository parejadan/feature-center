from flask import Blueprint, request
from feature.model import ClientFeatureRequest
from feature.model.logic import to_dict, to_json_dump, basic_insert


feature_api = Blueprint('features', __name__, template_folder='templates')
PRIORITY_REQUEST_LIMIT = 10
_priority_list = [p+1 for p in range(PRIORITY_REQUEST_LIMIT)]


@feature_api.route('/')  # get all features (should be lazy loading)
def index():
    try:
        query = ClientFeatureRequest.query.order_by('id').all()
        return to_json_dump(query)
    except Exception as ex:
        print('trouble fetching overall requested features', ex)


@feature_api.route('/getClientRequests/<client_id>')
def get_client_requests(client_id):
    """Returns a client's existing feature requests and available requests for further submissions"""
    try:
        query = ClientFeatureRequest.query.filter(ClientFeatureRequest.client_id == client_id).all()
        feature_requests = to_dict(query)
        used_requests = [r['priority_id'] for r in feature_requests]
        payload = {
            'available_requests': [r for r in _priority_list if r not in used_requests],
            'existing_requests': feature_requests}

        return to_json_dump(payload, False)

    except Exception as ex:
        print('issue while supplying client requests', ex)


@feature_api.route('/create', methods=['POST'])
def create():
    try:
        payload = request.get_json(force=True)
        request_feature = ClientFeatureRequest(**payload)
        basic_insert(request_feature)

    except Exception as ex:
        print('something happened creating feature relation', ex)
