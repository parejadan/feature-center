from flask import Flask, render_template
from feature.model import db, Client, ClientFeatureRequest

# todo- horrible, horrible setup. Please change this to config value
SQLALCHEMY_DATABASE_URI = 'postgresql://parejadan:a1s2r3j4f5k6@localhost:5432/feature_center'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

# default initialize databases to test environment setup
# todo- change this as optional based on config settings
with app.app_context():
    db.create_all()
