import feature
from waitress import serve


serve(feature.app, host=feature.env_config.app_host, port=feature.env_config.app_port)
