from flask import Blueprint
from feature.model.qbridge import basic_select
from feature.model import Client

client_api = Blueprint('clients', __name__, template_folder='templates')



@client_api.route('/')
def index():
	return basic_select(Client)


@client_api.route('/get<client_id>')
def get_by_id(client_id):
	return basic_select(Client, client_id)
