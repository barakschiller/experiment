import json

from experiment.core.experiment import Variant, DraftExperiment


def experiment_draft_from_json(content):
	content = json.loads(content)
	name = content['name']
	variants = []
	for v in content['variants']:
		variants.append(Variant(v['name'], v['allocation']))
	return DraftExperiment(name=name, variants=variants)

def experiment_draft_to_dict(draft):
	return dict(
			name=draft.name,
			variants=[
				dict(name=var.name, allocation=var.allocation) for var in draft.variants
				]
		)