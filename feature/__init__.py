import json
from flask import Flask, render_template
from feature.model import db, Client, ClientFeatureRequest


class ConfigManager:
    def __init__(self, file='config.json'):
        """load application configurations from json - alternative to env variables"""
        self._config_cache = self._get_config(file)
        self._user = self._config_cache['user']
        self._password = self._config_cache['password']
        self._host = self._config_cache['host']
        self._port = self._config_cache['port']
        self._db = self._config_cache['db']
        self._database_uri = self._config_cache['SQLALCHEMY_DATABASE_URI']
        self._track_modifications = self._config_cache['SQLALCHEMY_TRACK_MODIFICATIONS']
        self.setup_database = self._config_cache['SETUP_DATABASE']

    @staticmethod
    def _get_config(file):
        try:
            with open(file) as json_data_file:
                return json.load(json_data_file)
        except IOError as ex:
            raise IOError("config file was not setup correctly: {}".format(ex))

    def _get_database_uri(self):
        database_uri = self._database_uri.format(self._user, self._password, self._host, self._port, self._db)
        # print(database_uri)
        return database_uri

    def apply_config(self, _app):
        _app.config['SQLALCHEMY_DATABASE_URI'] = self._get_database_uri()
        _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = self._track_modifications

    def app_run(self, _app):
        db.init_app(app)
        # build database if environment config has it set
        if self.setup_database:
            with app.app_context():
                db.create_all()


app, env_config = Flask(__name__), ConfigManager()
env_config.apply_config(app)  # load configuration settings from json file
env_config.app_run(app)


@app.route('/')
def index():
    return render_template('index.html')

# if __name__ == "__main__":
#    app.run()
