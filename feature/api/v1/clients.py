from flask import Blueprint
from feature.model.logic import basic_select
from feature.model import Client

client_api = Blueprint('clients', __name__, template_folder='templates')


@client_api.route('/')
def index():
    try:
        return basic_select(Client)
    except Exception as ex:
        print("issue encountered while getting client data", ex)


@client_api.route('/get<client_id>')
def get_by_id(client_id):
    return basic_select(Client, client_id)
