from nose.tools import assert_equal, assert_not_equal

from api.services.assignment_service import AssignmentService
from core.experiment import Experiment, Variant
from storage.dict import DictStorage


class TestAssignmentService(object):

    def test_when_variants_are_changed_existing_assignments_stay_the_same(self):
        START = 'var1'
        AFTER_UPDATE = 'var2'
        ANY_ENTITY = 1

        experiment = Experiment.create_draft(
            name='test',
            variants=[
                Variant(START, 100),
                Variant(AFTER_UPDATE, 0)
            ]).start()

        service = AssignmentService(storage=DictStorage())

        assert_equal(service.assign(experiment, ANY_ENTITY), START)

        experiment.update_variants([
            Variant(START, 0),
            Variant(AFTER_UPDATE, 100)
        ])

        assert_equal(service.assign(experiment, ANY_ENTITY), START)

    def test_entity_name_escaped(self):
        experiment = Experiment.create_draft(
            name='test',
            variants=[
                Variant('anyvar', 100),
            ]).start()

        storage = DictStorage()
        service = AssignmentService(storage=storage)

        service.assign(experiment, 'name-with-colon:')
        assert_not_equal(':', storage.list()[0][-1])






