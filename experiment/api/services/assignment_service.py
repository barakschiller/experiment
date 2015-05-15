from api.services import escape_name

class AssignmentService(object):
    def __init__(self, storage):
        self.storage = storage

    def assign(self, experiment, entity):
        """
        :type experiment: experiment.core.experiment.Experiment
        :param entity: the entity for which a variant is requested (int or string)
        """
        existing_assignment = self.storage.get(self._key(experiment.name, entity))

        if existing_assignment is not None:
            return existing_assignment

        assignment = experiment.assign(entity)

        self.storage.store(self._key(experiment.name, entity), assignment)
        return assignment

    @staticmethod
    def _key(experiment_name, entity_name):
        return 'experiment:{}:entity:{}'.format(escape_name(experiment_name), escape_name(entity_name))
