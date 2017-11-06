import feature
from waitress import serve


serve(feature.app, host='0.0.0.0', port=8080)
# feature.app.run()
