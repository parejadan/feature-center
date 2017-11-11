from flask import Blueprint
from feature.model.transaction import Transaction
from feature.model import Client

client_api = Blueprint('clients', __name__, template_folder='templates')


@client_api.route('/')
def index():
    """Returns overall available clients"""
    # todo: lazy load data
    try:
        return Transaction.basic_select(Client, order_key='id')
    except Exception as ex:
        print("issue encountered while getting client data", ex)
