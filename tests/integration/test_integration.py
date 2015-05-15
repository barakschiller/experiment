from experiment.api import app
import json
import logging

from nose.tools import assert_not_equal, assert_equal

logging.basicConfig()

class TestIntegration(object):
    EXPERIMENT_NAME = 'somename'
    DRAFT_WITH_ONE_VARIANT = json.dumps(dict(
                name=EXPERIMENT_NAME,
                variants = [
                    dict(name='var1', allocation=100)
                ]
            ))

    def setup(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_build_experiment_and_assign(self):

        get_json(self.app.post('/experiment', data=self.DRAFT_WITH_ONE_VARIANT))
        get_json(self.app.get('/experiment/{}/start'.format(self.EXPERIMENT_NAME)))
        response = get_json(self.app.get('/experiment/{}/assign/1'.format(self.EXPERIMENT_NAME)))
        assert_equal(response['assignment'], 'var1')

    def test_fail_to_create_drafts_with_the_same_name(self):
        self.app.post('/experiment', data=self.DRAFT_WITH_ONE_VARIANT)
        assert_equal(self.app.post('/experiment', data=self.DRAFT_WITH_ONE_VARIANT).status_code, 400)


def get_json(response):
    assert_equal(response.status_code, 200)
    return json.loads(response.data)