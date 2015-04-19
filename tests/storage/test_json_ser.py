from nose.tools import assert_equals
import json


from experiment.storage.json_ser import experiment_from_json, experiment_to_dict
from experiment.core.experiment import Variant, Experiment

def test_json_serde():
	draft = Experiment.create_draft('exp', [Variant('var1', 50), Variant('var2', 50)])
	json_value = json.dumps(experiment_to_dict(draft))
	assert_equals(draft, experiment_from_json(json_value))