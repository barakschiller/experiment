from enum import Enum
from collections import namedtuple
import hashlib

Variant = namedtuple('Variant',['name','allocation'])

class DraftExperiment(object):
	def __init__(self, name, variants):
		self.name = name
		self.variants = variants[:]
	
	def build(self):
		return Experiment(self.name, self.variants)

	def __eq__(self, other):
		return self.name == other.name and self.variants == other.variants 



class Experiment(object):
	def __init__(self, name, variants):
		self.name = name
		self.salt = self.name
		self.variants = variants[:]
		self.mod = sum([variant.allocation for variant in self.variants])
	
	def assign(self, entity):
		hash = hashlib.md5("{}-{}".format(self.salt, entity)).hexdigest()
		entity_allocation = int(hash[:15], 16) % self.mod
		
	 	cum_sum = 0
		for variant in self.variants:
			cum_sum += variant.allocation
			if entity_allocation < cum_sum:
				return variant.name

	def complete(self, variant_name):
		if variant_name not in (variant.name for variant in self.variants):
			raise ValueError('Variant "{}" not defined in experiment'.format(variant_name))

		return CompletedExperiment(self.name, variant_name)


class CompletedExperiment(object):
	def __init__(self, name, variant_name):
		self.name = name
		self.variant_name = variant_name

	def assign(self, _):
		return self.variant_name