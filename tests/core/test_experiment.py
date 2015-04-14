from nose.tools import assert_equals, assert_greater, assert_raises
from collections import Counter

from experiment.core import experiment


class TestExperiment(object):
	VARIANT1 = 'any1'
	VARIANT2 = 'any2'
	VARIANT_NOT_IN_EXPERIMENT = 'not-in-exp'

	@staticmethod
	def build_two_variant_experiment():
		return experiment.DraftExperiment(
			name='test',
			variants = [
				experiment.Variant(TestExperiment.VARIANT1,50),
				experiment.Variant(TestExperiment.VARIANT2,50)
			]).build()  
	
	@staticmethod
	def generate_assignments(experiment, count=100):
		return Counter([experiment.assign(entity) for entity in xrange(count)])

	def test_one_variant_is_always_assigned(self):
		VARIANT = 'any'
		
		e = experiment.DraftExperiment(
			name='test',
			variants = [
				experiment.Variant(VARIANT,100)
			]).build()  
		
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