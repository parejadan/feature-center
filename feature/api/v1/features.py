from flask import Blueprint, request
from feature.model import ClientFeatureRequest
from feature.model.qbridge import basic_select, basic_insert


feature_api = Blueprint('features', __name__, template_folder='templates')


@feature_api.route('/')
def index():
    return basic_select(ClientFeatureRequest)


@feature_api.route('/get<feature_id>')
def get_by_id(feature_id):
    return basic_select(ClientFeatureRequest, feature_id)


@feature_api.route('/create', methods=['POST'])
def create():
    try:
        payload = request.get_json(force=True)
        if 'info' in payload:

            request_feature = ClientFeatureRequest(**payload['info'])
            basic_insert(request_feature)
            request_feature.insert_relations(payload)

    except Exception as ex:
        print('something happened creating feature relation', ex)
