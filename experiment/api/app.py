import flask
from flask import request, jsonify
import logging

_log = logging.getLogger('experiment.app')

from experiment.storage import json_ser

from experiment.api.services.experiment_service import ExperimentService
from experiment.api.services.assignment_service import AssignmentService
from experiment.storage import ItemAlreadyExistsException

app = flask.Flask(__name__)

@app.route('/experiment', methods=['POST'])
def create_experiment():
    draft = json_ser.draft_from_json(request.data)

    ExperimentService.create().store(draft)
    return jsonify(status='Successfuly created')

@app.route('/experiment/<name>', methods=['GET'])
def get_experiment(name):
    experiment = ExperimentService.create().get(name)
    return jsonify(json_ser.experiment_to_dict(experiment))


@app.route('/experiment/<name>', methods=['POST'])
def update_experiment(name):
    experiment = ExperimentService.create().update(name, json_ser.variants_from_json(request.data))
    return jsonify(json_ser.experiment_to_dict(experiment))

@app.route('/experiment/<name>/start')
def start_experiment(name):
    ExperimentService.create().start(name)
    _log.info('Started experiment {} from draft'.format(name))
    return jsonify(status='Experiment started')


@app.route('/experiment', methods=['GET'])
def get_all_experiments():
    experiments = ExperimentService.create().list()
    return jsonify(experiments=experiments)

@app.route('/experiment/<name>/assign/<entity_id>', methods=['GET'])
def experiment_assign_entity(name, entity_id):
    experiment = ExperimentService.create().get(name)
    assignment = AssignmentService.create().assign(experiment, entity_id)
    _log.info('Experiment {}, assigned <{}> to <{}>'.format(experiment.name, entity_id, assignment))
    return jsonify(entity_id=entity_id, assignment=assignment)

@app.errorhandler(ItemAlreadyExistsException)
def handle_item_already_exists(error):
    return ('Item with the same name already exists', 400)