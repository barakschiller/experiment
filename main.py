from experiment.api.dispatcher import experiment_app
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
experiment_app.run(debug=True, host='0.0.0.0')