from experiment.storage import json_ser
from api.services import escape_name


class ExperimentService(object):
    ADMIN_KEY = 'admin:all_experiments'

    def __init__(self, storage):
        self.storage = storage

    def list(self):
        result = self.storage.get(self.ADMIN_KEY)
        if result is None:
            return []
        else:
            return result

    def store(self, experiment):
        self.storage.store(
            key=self._key(experiment.name),
            dict_value=json_ser.experiment_to_dict(experiment))

        experiment_list = self.list()
        if len(experiment_list) == 0:
            self.storage.store(self.ADMIN_KEY, [experiment.name])
        else:
            experiment_list.append(experiment.name)
            self.storage.update(self.ADMIN_KEY, experiment_list)

    def get(self, experiment_name):
        return json_ser.experiment_from_dict(self.storage.get(self._key(experiment_name)))

    def update(self, experiment_name, variants):
        experiment = self.get(experiment_name)
        experiment.update_variants(variants)
        self.storage.update(self._key(experiment.name), dict_value=json_ser.experiment_to_dict(experiment))
        return experiment

    def start(self, experiment_name):
        experiment = self.get(experiment_name)
        experiment.start()
        self.storage.update(self._key(experiment.name), dict_value=json_ser.experiment_to_dict(experiment))
        return experiment

    @staticmethod
    def _key(experiment_name):
        return '{}:{}'.format('experiment', escape_name(experiment_name))