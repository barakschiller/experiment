from experiment import storage
from experiment.storage.dict import DictStorage
from experiment.storage.postgres import PostgresStorage
from experiment.storage import json_ser

storage = DictStorage()
#storage = PostgresStorage("host='localhost' dbname='experiment' user='postgres'")

class ExperimentService(object):
	ADMIN_KEY = 'admin:all_experiments'

	def __init__(self, storage):
		self.storage = storage

	def list(self):
		return storage.get(self.ADMIN_KEY)

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
		return json_ser.experiment_from_dict(storage.get(self.key(experiment_name)))

	def update(self, experiment_name, variants):
		experiment = self.get(experiment_name)
		experiment.update_variants(variants)
		storage.update(self.key(experiment.name), dict_value=json_ser.experiment_to_dict(experiment))
		return experiment

	def start(self, experiment_name):
		experiment = self.get(experiment_name)
		experiment.start()
		storage.update(self.key(experiment.name), dict_value=json_ser.experiment_to_dict(experiment))
		return experiment

	@staticmethod
	def key(experiment_name):
		return '{}:{}'.format('experiment', experiment_name)

	@classmethod
	def create(cls):
		return cls(storage)