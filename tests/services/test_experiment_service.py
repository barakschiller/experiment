from nose.tools import assert_in
from api.services.experiment_service import ExperimentService
from core.experiment import Experiment
from storage.dict import DictStorage


class TestExperimentService(object):
    def test_stored_experiment_is_added_to_list(self):
        EXPERIMENT_NAME = 'any-experiment'

        service = ExperimentService(storage=DictStorage())
        experiment = Experiment(EXPERIMENT_NAME, [])

        service.store(experiment)

        assert_in(EXPERIMENT_NAME, service.list())


