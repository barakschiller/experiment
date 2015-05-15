class AssignmentService(object):
    def __init__(self, storage):
        self.storage = storage

    def assign(self, experiment, entity):
        existing_assignment = self.storage.get(self.key(experiment.name, entity))

        if existing_assignment is not None:
            return existing_assignment

        assignment = experiment.assign(entity)

        self.storage.store(self.key(experiment.name, entity), assignment)
        return assignment

    @staticmethod
    def key(experiment_name, entity_name):
        return 'experiment:{}:entity:{}'.format(experiment_name, entity_name)
