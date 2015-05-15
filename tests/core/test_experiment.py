from nose.tools import assert_equals, assert_greater, assert_raises, assert_in
from collections import Counter

from experiment.core.experiment import Experiment, Variant


class TestExperiment(object):
    VARIANT1 = 'any1'
    VARIANT2 = 'any2'
    VARIANT_NOT_IN_EXPERIMENT = 'not-in-exp'

    @staticmethod
    def build_two_variant_experiment():
        return Experiment.create_draft(
            name='test',
            variants=[
                Variant(TestExperiment.VARIANT1, 50),
                Variant(TestExperiment.VARIANT2, 50)
                ]).start()

    @staticmethod
    def generate_assignments(experiment, count=100):
        return Counter([experiment.assign(entity) for entity in xrange(count)])

    def test_one_variant_is_always_assigned(self):
        VARIANT = 'any'

        e = Experiment.create_draft(
            name='test',
            variants=[
                Variant(VARIANT, 100)
                ]).start()

        assert_equals(self.generate_assignments(e)[VARIANT], 100)


    def test_multiple_variants_are_roughly_equal(self):
        e = self.build_two_variant_experiment()

        assignments = self.generate_assignments(e)

        assert_greater(assignments[self.VARIANT1], 30)
        assert_greater(assignments[self.VARIANT2], 30)

    def test_completed_experiment_always_assigns_one_value(self):
        e = self.build_two_variant_experiment().complete(self.VARIANT1)
        assert_equals(self.generate_assignments(e)[self.VARIANT1], 100)

    def test_fail_to_finalize_experiment_to_non_existing_variant(self):
        with assert_raises(ValueError):
            self.build_two_variant_experiment().complete(self.VARIANT_NOT_IN_EXPERIMENT)

    def test_fail_to_update_completed_experiment(self):
        VARIANT = 'any'
        e = Experiment.create_draft(
            name='test',
            variants=[
                Variant(VARIANT, 100)
            ]).start()
        e.complete(VARIANT)
        with assert_raises(ValueError):
            e.update_variants([])

    def test_cannot_add_variant_to_running_test(self):
        EXISTING_VARIANT = Variant('existing', 100)
        ADDED_VARIANT = Variant('added', 100)
        e = Experiment.create_draft(
            name='test',
            variants=[EXISTING_VARIANT]).start()

        with assert_raises(ValueError):
            e.update_variants([EXISTING_VARIANT, ADDED_VARIANT])

    def can_change_allocation_for_running_test(self):
        INITIAL_VARIANT = Variant('var', 100)
        CHANGED_VARIANT = Variant('var', 50)

        e = Experiment.create_draft(
            name='test',
            variants=[INITIAL_VARIANT]).start()

        e.update_variants([CHANGED_VARIANT])

        assert_in(CHANGED_VARIANT, e.variants)
