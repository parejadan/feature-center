from flask import Blueprint
from feature.model import PriorityTypes
from feature.model.qbridge import basic_select


priority_api = Blueprint('priorities', __name__, template_folder='templates')


@priority_api.route('/')
def index():
    return basic_select(PriorityTypes)
