import json

import pytest

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
        }

    def test_modes_put_missing_data_error(self, client):
        rv = client.put(self.ENDPOINT, data={})
        assert rv.status_code == 400
        assert 'application/json' in rv.content_type
        modes_errors = json.loads(rv.data)['errors']['modes']
        assert len(modes_errors) == 1
        assert modes_errors[0] == "Missing data for required field."

    @pytest.mark.parametrize('req_modes', ['', '-', 'CEHAC'])
    def test_modes_put_regexp_error(self, client, req_modes):
        rv = client.put(self.ENDPOINT, data={'modes': req_modes})
        assert rv.status_code == 400
        assert 'application/json' in rv.content_type
        modes_errors = json.loads(rv.data)['errors']['modes']
        assert len(modes_errors) == 1
        assert modes_errors[0] == ''.join([
            "Modes string must match '[ACEH]{1,4}' regular expression, ",
            f"received {req_modes!r}"
        ])

    @pytest.mark.parametrize('req_modes', [
        'C', 'E', 'H', 'A', 'EC', 'AH', 'HCE', 'AAA', 'HECA'
    ])
    def test_modes_put_ok(self, client, req_modes):
        rv = client.put(self.ENDPOINT, data={'modes': req_modes})
        assert rv.status_code == 200
        assert 'application/json' in rv.content_type
        assert json.loads(rv.data) == {
            'message': "Modes successfully set on pilotwire controller.",
            'modes': '{:C<4}'.format(req_modes)
        }
