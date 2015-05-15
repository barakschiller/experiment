from api.services import escape_name


class AssignmentService(object):
    def __init__(self, storage):
        self.storage = storage

    def assign(self, experiment, entity):
        """
        Query the variant to be used for the given entity
        :type experiment: experiment.core.experiment.Experiment
        """
        existing_assignment = self.storage.get(self._key(experiment.name, entity))

        if existing_assignment is not None:
            return existing_assignment

        assignment = experiment.assign(entity)

        self.storage.store(self._key(experiment.name, entity), assignment)
        return assignment

    def manual_assign(self, experiment, entity, variant_name):
        """
        Manually set a variant for an entity
        :type experiment: experiment.core.experiment.Experiment
        """
        if variant_name not in experiment.variant_names:
            raise ValueError("Invalid variant")

        if self.storage.get(self._key(experiment.name, entity)) is None:
            self.storage.store(self._key(experiment.name, entity), variant_name)
        else:
            self.storage.update(self._key(experiment.name, entity), variant_name)
        return variant_name


    @staticmethod
    def _key(experiment_name, entity_name):
        return 'experiment:{}:entity:{}'.format(escape_name(experiment_name), escape_name(entity_name))
