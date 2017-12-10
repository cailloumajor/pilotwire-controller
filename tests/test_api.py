import json

import pytest

from pilotwire_controller import api


class TestingController:

    MODES = ''

    @property
    def modes(self):
        return self.MODES

    @modes.setter
    def modes(self, modes_str):
        self.MODES = modes_str


@pytest.fixture
def patch_controller(monkeypatch):
    monkeypatch.setattr(__name__ + '.api.controller', TestingController())


@pytest.fixture
def client():
    api.app.testing = True
    return api.app.test_client()


@pytest.mark.usefixtures('patch_controller')
class TestModesEndpoint:

    def test_modes_get(self, client):
        TestingController.MODES = 'ABCD'
        rv = client.get('/modes')
        assert json.loads(rv.data) == {'modes': 'ABCD'}

    def test_modes_put_with_empty_data(self, client):
        rv = client.put('/modes', data={})
        assert rv.status_code == 400
        assert json.loads(rv.data) == {
            'modes': ["Missing data for required field."]
        }

    def test_modes_put_with_too_short_data(self, client):
        rv = client.put('/modes', data={'modes': ''})
        assert rv.status_code == 400
        assert json.loads(rv.data) == {
            'modes': ["Must have at least one character."]
        }

    def test_modes_put_with_too_long_data(self, client):
        rv = client.put('/modes', data={'modes': 'CEHAC'})
        assert rv.status_code == 400
        assert json.loads(rv.data) == {
            'modes': ["Must have at most four characters."]
        }

    def test_modes_put_with_invalid_modes(self, client):
        rv = client.put('/modes', data={'modes': '+-*/'})
        assert rv.status_code == 400
        assert json.loads(rv.data) == {
            'modes': ["Each mode must be one of 'C', 'E', 'H', 'A'."]
        }

    def test_modes_put_good(self, client, good_modes_str):
        rv = client.put('/modes', data={'modes': good_modes_str})
        assert rv.status_code == 200
        assert rv.data == (
            b"Modes set on pilotwire controller: %b" %
            good_modes_str.encode('utf8')
        )
