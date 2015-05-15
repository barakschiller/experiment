from experiment.storage import json_ser


class ExperimentService(object):
    ADMIN_KEY = 'admin:all_experiments'

    def __init__(self, storage):
        self.storage = storage

    def list(self):
        return self.storage.get(self.ADMIN_KEY)

    def store(self, experiment):
        if experiment.name.find(':') >= 0:
            raise ValueError('Experiment name cannot contain a colon')

        self.storage.store(
            key=self.key(experiment.name),
            dict_value=json_ser.experiment_to_dict(experiment))

        experiment_list = self.list()
        if experiment_list is None:
            self.storage.store(self.ADMIN_KEY, [experiment.name])
        else:
            experiment_list.append(experiment.name)
            self.storage.update(self.ADMIN_KEY, experiment_list)

    def get(self, experiment_name):
        return json_ser.experiment_from_dict(self.storage.get(self.key(experiment_name)))

    def update(self, experiment_name, variants):
        experiment = self.get(experiment_name)
        experiment.update_variants(variants)
        self.storage.update(self.key(experiment.name), dict_value=json_ser.experiment_to_dict(experiment))
        return experiment

    def start(self, experiment_name):
        experiment = self.get(experiment_name)
        experiment.start()
        self.storage.update(self.key(experiment.name), dict_value=json_ser.experiment_to_dict(experiment))
        return experiment

    @staticmethod
    def key(experiment_name):
        return '{}:{}'.format('experiment', experiment_name)