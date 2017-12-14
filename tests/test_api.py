import json

import pytest

from pilotwire_controller import __version__ as project_version
from pilotwire_controller import api


@pytest.fixture
def client():
    api.app.testing = True
    return api.app.test_client()


class TestModesEndpoint:

    ENDPOINT = '/pilotwire'

    def test_modes_get(self, client):
        api.controller.modes = 'ACHE'
        rv = client.get(self.ENDPOINT)
        assert json.loads(rv.data) == {
            'modes': 'ACHE',
            'version': project_version,
        }

    def test_modes_put_with_empty_data(self, client):
        rv = client.put(self.ENDPOINT, data={})
        assert rv.status_code == 400
        assert json.loads(rv.data) == {
            'modes': ["Missing data for required field."]
        }

    def test_modes_put_with_too_short_data(self, client):
        rv = client.put(self.ENDPOINT, data={'modes': ''})
        assert rv.status_code == 400
        assert json.loads(rv.data) == {
            'modes': ["Must have at least one character."]
        }

    def test_modes_put_with_too_long_data(self, client):
        rv = client.put(self.ENDPOINT, data={'modes': 'CEHAC'})
        assert rv.status_code == 400
        assert json.loads(rv.data) == {
            'modes': ["Must have at most four characters."]
        }

    def test_modes_put_with_invalid_modes(self, client):
        rv = client.put(self.ENDPOINT, data={'modes': '+-*/'})
        assert rv.status_code == 400
        assert json.loads(rv.data) == {
            'modes': ["Each mode must be one of 'C', 'E', 'H', 'A'."]
        }

    def test_modes_put_good(self, client, good_modes_str):
        rv = client.put(self.ENDPOINT, data={'modes': good_modes_str})
        assert rv.status_code == 200
        assert rv.data == (
            b"Modes set on pilotwire controller: %b" %
            '{:C<4}'.format(good_modes_str).encode('utf8')
        )
