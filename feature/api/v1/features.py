from flask import Blueprint, request
from feature.model import FeatureInfo, ClientFeatureRequest
from feature.model.qbridge import basic_select


feature_api = Blueprint('features', __name__, template_folder='templates')


@feature_api.route('/')
def index():
    return basic_select(FeatureInfo)


@feature_api.route('/get<feature_id>')
def get_by_id(feature_id):
    return basic_select(FeatureInfo, feature_id)


@feature_api.route('/create', methods=['POST'])
def create():
    info_fields = ['title', 'description', 'date_target']
    request_fields = ['client_id', 'priority_id', 'product_id']
    info_params, request_params = {}, {}

    # pull feature information from post
    for field in info_fields:
        if field in request.form[field]:
            info_params[field] = request.form[field]
    # pull request details from post
    for field in request_fields:
        if field in request.form[field]:
            request_params[field] = request.form[field]
    print(request_params)
    print(info_params)
    # feature_info = FeatureInfo(**info_params)
    # submit feature information and retrieve feature.id
    # update request_params
    # request_info = ClientFeatureRequest(**request_params)
    # submit request data to db
