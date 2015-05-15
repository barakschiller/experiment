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
        escaped_entity_name = str(entity_name).replace('-', '--').replace(':', '-')
        return 'experiment:{}:entity:{}'.format(experiment_name, escaped_entity_name)
