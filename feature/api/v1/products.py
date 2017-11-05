from flask import Blueprint
from feature.model import ProductTypes
from feature.model.logic import basic_select

product_api = Blueprint('products', __name__, template_folder='templates')


@product_api.route('/')
def index():
    """Returns overall available products"""
    # todo: lazy load data
    try:
        return basic_select(ProductTypes)
    except Exception as ex:
        print('exception encountered pulling existing products: ', ex)
