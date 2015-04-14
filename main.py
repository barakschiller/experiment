from experiment.api.app import app
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
app.run(debug=True, host='0.0.0.0')