from sys import exit
from flask import Flask
from feature.config import ConfigManager
from feature.model import db, PriorityTypes, ProductTypes, Client


def load_data_file(file):
    try:
        return [f for f in open(file).read().split('\n') if len(f) > 0]
    except Exception as ex:
        print('we encountered an issue reading {}'.format(file), ex)


app, env_config = Flask(__name__), ConfigManager()
env_config.apply_config(app)
env_config.init_db(app)

with app.app_context():
    # load sample data
    priority_data = load_data_file('data/priority.csv')
    product_data = load_data_file('data/product.csv')
    client_data = load_data_file('data/client.csv')
    print('\n\n>> loaded sample data..')
    # create databases
    db.drop_all() # make sure we're recreating everything
    db.create_all()
    print('>> created database tables')
    # add data to session
    for tok in priority_data:
        rec = PriorityTypes(priority_name=tok)
        db.session.add(rec)
    for tok in product_data:
        rec = ProductTypes(product_code=tok)
        db.session.add(rec)
    for tok in client_data:
        nam, mail, phnum, prodcode = tok.split(',')
        rec = Client(name=nam, email=mail, phone_number=phnum)
        # product = ProductTypes(product_code=prodcode)
        # rec.product_relation.append(product)
        db.session.add(rec)
    # commit data to database
    db.session.commit()
    exit()