from enum import Enum
from collections import namedtuple
import hashlib
import logging

_log = logging.getLogger('experiment.core')

Variant = namedtuple('Variant', ['name', 'allocation'])
State = Enum('State', 'DRAFT RUNNING COMPLETED')


class Experiment(object):
    def __init__(self, name, variants, state=State.DRAFT, override=None):
        self.name = name
        self.state = state
        self.override = override
        self._internal_update_variants(variants)

    def __eq__(self, other):
        return self.name == other.name and \
               self.salt == other.salt and \
               self.variants == other.variants and \
               self.state == other.state and \
               self.override == other.override

    @classmethod
    def create_draft(cls, name, variants):
        return cls(name, variants, State.DRAFT)

    def assign(self, entity):
        if self.state == State.DRAFT:
            raise ValueError('Experiment is still a draft')
        if self.override is not None:
            return self.override

        hashed_user = hashlib.md5("{}-{}".format(self.salt, entity)).hexdigest()
        entity_allocation = int(hashed_user[:15], 16) % self.mod

        cum_sum = 0
        for variant in self.variants:
            cum_sum += variant.allocation
            if entity_allocation < cum_sum:
                return variant.name

    def start(self):
        if self.state != State.DRAFT:
            raise ValueError('Experiment already started')
        self.state = State.RUNNING
        _log.info('Experiment <{}> started'.format(self.name))
        return self

    def complete(self, variant_name):
        if self.state != State.RUNNING:
            raise ValueError('Experiment not started')

        if variant_name not in (variant.name for variant in self.variants):
            raise ValueError('Variant "{}" not defined in experiment'.format(variant_name))
        self.override = variant_name
        self.state = State.COMPLETED
        return self

    def update_variants(self, variants):
        if self.state == State.COMPLETED:
            raise ValueError('Cannot update a completed experiment')
        if self.state == State.RUNNING and _names(self.variants) != _names(variants):
            raise ValueError('Cannot add or remove variants from a running experiment')
        self._internal_update_variants(variants)

    def _internal_update_variants(self, variants):
        self.variants = variants[:]
        self.mod = sum([variant.allocation for variant in self.variants])
        self.salt = self.name


def _names(variants):
    return set([var.name for var in variants])