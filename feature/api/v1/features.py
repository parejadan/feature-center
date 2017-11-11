from flask import Blueprint, request, Response
from feature.model import ClientFeatureRequest
from feature.model.logic import to_dict, to_json_dump, update_feature_and_peers
from feature.model.transaction import Transaction


feature_api = Blueprint('features', __name__, template_folder='templates')
PRIORITY_REQUEST_LIMIT = 5
_priority_list = [p+1 for p in range(PRIORITY_REQUEST_LIMIT)]
_transInterface = Transaction()


@feature_api.route('/')
def index():
    """Returns all features"""
    # todo lazy load data for UI (receive index)
    try:
        query = ClientFeatureRequest.query.order_by('priority_id').all()
        return to_json_dump(query)
    except Exception as ex:
        print('exception encountered pulling all existing feature requests: ', ex)


@feature_api.route('/getClientRequests/<client_id>')
def get_client_requests(client_id):
    """Returns a client's existing feature requests and available requests for further submissions"""
    try:
        query = ClientFeatureRequest.query.filter(ClientFeatureRequest.client_id == client_id) \
            .order_by('priority_id').all()
        feature_requests = to_dict(query)
        used_requests = [r['priority_id'] for r in feature_requests]
        payload = {
            'available_requests': [r for r in _priority_list if r not in used_requests],
            'existing_requests': feature_requests}

        return to_json_dump(payload, False)

    except Exception as ex:
        print('exception encountered pulling client requests: ', ex)


@feature_api.route('/getOverallPriorities')
def get_priority_set():
    """Returns generic available priorities for any client"""
    try:
        return to_json_dump(_priority_list, False)
    except Exception as ex:
        print('exception encountered returning generic priority set', ex)


@feature_api.route('/create', methods=['POST'])
def create():
    """creates a client feature request"""
    try:
        payload = request.get_json(force=True)
        request_feature = ClientFeatureRequest(**payload)
        return execute_trans_for_response(request_feature, _transInterface.INSERT)
    except Exception as ex:
        print('exception encountered creating a client request: ', ex)
        return Response(status=500)


@feature_api.route('/update', methods=['POST'])
def update():
    """Update a client's feature request information"""
    try:
        payload = request.get_json(force=True)
        updated_feature = ClientFeatureRequest(**payload)
        query = ClientFeatureRequest.query.filter(ClientFeatureRequest.client_id == updated_feature.client_id) \
            .order_by('priority_id').all()
        # cast once for numerical comparison of IDs
        updated_feature.id, updated_feature.priority_id = int(updated_feature.id), int(updated_feature.priority_id)
        update_feature_and_peers(updated_feature, query)

        return execute_trans_for_response(query, _transInterface.UPDATE)
    except Exception as ex:
        print('exception encountered updating client feature request: ', ex)
        return Response(status=500)


@feature_api.route('/delete', methods=['POST'])
def delete():
    """Delete a client's feature request information"""
    try:
        payload = request.get_json(force=True)
        delete_feature = ClientFeatureRequest(**payload)
        query = _transInterface.basic_select(ClientFeatureRequest, _id=delete_feature.id)

        return execute_trans_for_response(query, _transInterface.DELETE)
    except Exception as ex:
        print('exception encountered deleting client request:', ex)
        return Response(status=500)


def execute_trans_for_response(query, t_type):
    """Assures API response for CRUD request matches transaction result"""
    if _transInterface.commit(query, t_type):
        return Response(status=200)
    else:
        return Response(status=500)
