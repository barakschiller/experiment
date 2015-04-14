import flask
from flask import request, jsonify
import logging

_log = logging.getLogger('experiment.app')

from experiment.storage.json_ser import experiment_draft_from_json, experiment_draft_to_dict
from experiment.storage import database

app = flask.Flask(__name__)


@app.route('/draft', methods=['GET'])
def get_all_drafts():
	return jsonify(draft_ids=database.drafts.get_all_ids())


@app.route('/draft', methods=['POST'])
def create_draft():
	draft = experiment_draft_from_json(request.data)
	draft_id = database.drafts.store(draft)
	return jsonify(draft_id=draft_id)


@app.route('/draft/<int:draft_id>')
def get_draft(draft_id):
	return jsonify(experiment_draft_to_dict(database.drafts.get(draft_id)))


@app.route('/draft/<int:draft_id>/start')
def start_experiment(draft_id):
	draft = database.drafts.get(draft_id)
	experiment = draft.build()
	experiment_id = database.experiments.store(experiment)
	database.drafts.delete(draft_id)
	_log.info('Built experiment {} from draft {}'.format(experiment_id, draft_id))
	return jsonify(experiment_id=experiment_id)


@app.route('/experiment', methods=['GET'])
def get_all_experiments():
	return jsonify(experiment_ids=database.experiments.get_all_ids())


@app.route('/experiment/<int:experiment_id>/assign/<int:entity_id>', methods=['GET'])
def experiment_assign_entity(experiment_id, entity_id):
	experiment = database.experiments.get(experiment_id)
	assignment = experiment.assign(entity_id)
	_log.info('Experiment {}, assigned <{}> to <{}>'.format(experiment.name, entity_id, assignment))
	return jsonify(entity_id=entity_id, assignment=assignment)

