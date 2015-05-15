import flask
from flask import request, jsonify
import logging
from storage.dict import DictStorage
from storage.postgres import PostgresStorage

_log = logging.getLogger('experiment.dispatcher')

from experiment.storage import json_ser

from experiment.api.services.experiment_service import ExperimentService
from experiment.api.services.assignment_service import AssignmentService
from experiment.storage import ItemAlreadyExistsException

experiment_app = flask.Flask(__name__)

@experiment_app.before_first_request
def initialise_storage():
    is_testing = experiment_app.config.get('TESTING', False)
    if not is_testing:
        experiment_app.config['EXPERIMENT_STORAGE'] = PostgresStorage("host='localhost' dbname='experiment' user='postgres'")
        experiment_app.config['ASSIGNMENT_STORAGE'] = PostgresStorage("host='localhost' dbname='experiment' user='postgres'")
    else:
        experiment_app.config['EXPERIMENT_STORAGE'] = DictStorage()
        experiment_app.config['ASSIGNMENT_STORAGE'] = DictStorage()


@experiment_app.route('/experiment', methods=['POST'])
def create_experiment():
    draft = json_ser.draft_from_json(request.data)

    _experiment_service().store(draft)
    return jsonify(status='Successfully created')

@experiment_app.route('/experiment/<name>', methods=['GET'])
def get_experiment(name):
    experiment = _experiment_service().get(name)
    return jsonify(json_ser.experiment_to_dict(experiment))


@experiment_app.route('/experiment/<name>', methods=['POST'])
def update_experiment(name):
    experiment = _experiment_service().update(name, json_ser.variants_from_json(request.data))
    return jsonify(json_ser.experiment_to_dict(experiment))

@experiment_app.route('/experiment/<name>/start')
def start_experiment(name):
    _experiment_service().start(name)
    _log.info('Started experiment {} from draft'.format(name))
    return jsonify(status='Experiment started')


@experiment_app.route('/experiment', methods=['GET'])
def get_all_experiments():
    experiments = _experiment_service().list()
    return jsonify(experiments=experiments)

@experiment_app.route('/experiment/<name>/assign/<entity_id>', methods=['GET'])
def experiment_assign_entity(name, entity_id):
    experiment = _experiment_service().get(name)
    assignment = _assignment_service().assign(experiment, entity_id)
    _log.info('Experiment {}, assigned <{}> to <{}>'.format(experiment.name, entity_id, assignment))
    return jsonify(entity_id=entity_id, assignment=assignment)

@experiment_app.errorhandler(ItemAlreadyExistsException)
def handle_item_already_exists(_):
    return 'Item with the same name already exists', 400

def _experiment_service():
    return ExperimentService(experiment_app.config['EXPERIMENT_STORAGE'])

def _assignment_service():
    return AssignmentService(experiment_app.config['ASSIGNMENT_STORAGE'])

