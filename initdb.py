from sys import exit
from flask import Flask
from feature.config import ConfigManager
from feature.model import db, ProductTypes, Client


def load_data_file(file):
    try:
        return [f for f in open(file).read().split('\n') if len(f) > 0]
    except Exception as ex:
        print('we encountered an issue reading {}'.format(file), ex)


def add_data_to_sess(obj, obj_keys, obj_vals, sess, val_split=None):
    """flexible wrapper for adding data to db session (does not perform commits \
       obj: Model object we want obj_vals (actual data) to get initialized with
       obj_keys: should be read from datafile whee obj_vals comes from
       sess: db (warning do not pass db.session
       val_split: if obj_keys is not a list, then leave blank"""
    try:
        if val_split is None:  # setting model 'obj' with one key only for all records
            for val in obj_vals:
                dct = {obj_keys: val}
                rec = obj(**dct)
                sess.session.add(rec)
        else:  # for every record, define dct object where obj keys are set with respective val
            for val in obj_vals:
                dct = {}
                tokens = val.split(val_split)
                # only initialize model 'obj' with the data we have
                token_len, itr = len(tokens), 0
                while itr < token_len:
                    dct[obj_keys[itr]] = tokens[itr]
                    itr += 1
                rec = obj(**dct)
                sess.session.add(rec)
    except Exception as ex:
        print('issue encountered adding data to db session', ex)


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
    db.drop_all()  # make sure we're recreating everything
    print('>> dropped tables for clean setup')
    db.create_all()
    print('>> created database tables')
    # add data to session
    add_data_to_sess(ProductTypes,
                     'product_code',  # should be the same as properties in ProductTypes model
                     product_data, db)
    print('>> setup product data')
    add_data_to_sess(Client,
                     ['name', 'email', 'phone_number', 'product_id'],
                     client_data, db, ',')
    print('>> setup client data')
    # commit data to database
    db.session.commit()
    print('>> committing session')
    exit()
    print('>> database setup complete!')
