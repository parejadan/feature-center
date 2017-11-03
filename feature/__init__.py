from flask import Flask, render_template
from feature.config import ConfigManager

# from v1.clients import client_api
# from v1.features import feature_api
from feature.api.v1.clients import client_api
from feature.api.v1.features import feature_api
from feature.api.v1.priorities import priority_api
from feature.api.v1.products import product_api


app, env_config = Flask(__name__), ConfigManager()
env_config.apply_config(app)  # load configuration settings from json file
env_config.init_db(app)


@app.route('/')
def index():
    return render_template('index.html')


app.register_blueprint(client_api, url_prefix='/api/v1/clients')
app.register_blueprint(feature_api, url_prefix='/api/v1/features')
app.register_blueprint(priority_api, url_prefix='/api/v1/priorities')
app.register_blueprint(product_api, url_prefix='/api/v1/products')
