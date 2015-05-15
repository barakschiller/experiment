import json

from experiment.core.experiment import Variant, Experiment, State


def draft_from_json(content):
    experiment = experiment_from_json(content)
    experiment.state = State.DRAFT
    experiment.override = None
    return experiment


def experiment_from_json(content):
    return experiment_from_dict(json.loads(content))


def experiment_from_dict(content):
    name = content['name']
    variants = variants_from_dict(content)

    if 'state' in content:
        state = State[content['state']]
    else:
        state = State.DRAFT

    if 'override' in content:
        override = content['override']
    else:
        override = None

    return Experiment(name=name, variants=variants, state=state, override=override)


def variants_from_json(content):
    return variants_from_dict(json.loads(content))


def variants_from_dict(content):
    variants = []
    for v in content['variants']:
        variants.append(Variant(v['name'], v['allocation']))
    return variants


def experiment_to_dict(experiment):
    return dict(
            name=experiment.name,
            variants=[
                dict(name=var.name, allocation=var.allocation) for var in experiment.variants
                ],
            state=experiment.state.name,
            override=experiment.override
        )
