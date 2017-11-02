from flask import Blueprint
from feature.model import ProductTypes
from feature.model.qbridge import basic_select

product_api = Blueprint('products', __name__, template_folder='templates')


@product_api.route('/')
def index():
    return basic_select(ProductTypes)