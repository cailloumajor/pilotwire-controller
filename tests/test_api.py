import json

import pytest

from pilotwire_controller import __version__ as project_version
from pilotwire_controller import api


@pytest.fixture
def client():
    api.app.testing = True
    return api.app.test_client()


class TestPilotwireEndpoint:

    ENDPOINT = '/pilotwire'

    def test_modes_get(self, client):
        api.controller.modes = 'ACHE'
        rv = client.get(self.ENDPOINT)
        assert rv.status_code == 200
        assert 'application/json' in rv.content_type
        assert json.loads(rv.data) == {
            'modes': 'ACHE',
            'version': project_version,
        }

    @pytest.mark.parametrize('req_data,resp_data', [
        (
            {},
            {'errors': {'modes': ["Missing data for required field."]}}
        ),
        (
            {'modes': ''},
            {'errors': {'modes': ["Must have at least one character."]}}
        ),
        (
            {'modes': 'CEHAC'},
            {'errors': {'modes': ["Must have at most four characters."]}}
        ),
        (
            {'modes': '+-*/'},
            {'errors': {
                'modes': ["Each mode must be one of 'C', 'E', 'H', 'A'."]
            }}
        ),
    ])
    def test_modes_put_error(self, client, req_data, resp_data):
        rv = client.put(self.ENDPOINT, data=req_data)
        assert rv.status_code == 400
        assert 'application/json' in rv.content_type
        assert json.loads(rv.data) == resp_data

    def test_modes_put_good(self, client, good_modes_str):
        rv = client.put(self.ENDPOINT, data={'modes': good_modes_str})
        assert rv.status_code == 200
        assert 'application/json' in rv.content_type
        assert json.loads(rv.data) == {
            'message': "Modes successfully set on pilotwire controller.",
            'modes': '{:C<4}'.format(good_modes_str)
        }
