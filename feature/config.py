import json
from feature.model import db


class ConfigManager:
    def __init__(self, file='config.json'):
        """load application configurations from json - alternative to env variables"""
        _config_cache = self._get_config(file)
        self._user = _config_cache['user']
        self._password = _config_cache['password']
        self._host = _config_cache['host']
        self._port = _config_cache['port']
        self._db = _config_cache['db']
        self._database_uri = _config_cache['SQLALCHEMY_DATABASE_URI']
        self._track_modifications = _config_cache['SQLALCHEMY_TRACK_MODIFICATIONS']
        self.app_host, self.app_port = _config_cache['app_host'], _config_cache['app_port']
        self.REGRESSION_TEST_URL = '{}:{}'.format(self.app_host, self.app_port)
        self.REGRESSION_DRIVER = _config_cache['REGRESSION_DRIVER']
        

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

    @staticmethod
    def init_db(_app):
        db.init_app(_app)
