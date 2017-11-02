import json
from flask import Blueprint
from feature.model import Client

client_api = Blueprint('client_api', __name__, template_folder='templates')


@client_api.route('/')
def index():
    query = Client.query.order_by('id').all()
    client_list = [client.to_dict() for client in query]
    return json.dumps(client_list, separators=(',', ':'))


@client_api.route('/get<client_id>')
def get_by_id(client_id):
    query = Client.query.get(client_id)
    return json.dumps(query.to_dict(), separators=(',', ':'))


