# -*- coding: utf-8 -*-
# pylint: disable=protected-access, redefined-outer-name, unused-argument
# pylint: disable=no-self-use

from multiprocessing import Process
from types import MethodType

import pytest

from pilotwire_controller.client import ControllerProxy, \
    PilotwireModesInconsistent
from pilotwire_controller import daemon


class Server:

    def __init__(self):
        self.process = Process(
            target=daemon.run, kwargs=dict(controller_type='test'))

    def start(self):
        self.process.start()

    def stop(self):
        self.process.terminate()
        self.process.join()


@pytest.yield_fixture
def server():
    srv = Server()
    srv.start()
    yield srv
    srv.stop()


@pytest.yield_fixture
def client(server):
    cln = ControllerProxy(500)
    yield cln
    del cln


class TestControllerProxyProperties:

    def test_modes_getter(self, client):
        expected = {'1':'C', '2':'C', '3':'C', '4':'C'}
        assert client.modes == expected

    def test_modes_setter(self, client):
        expected = {'1':'C', '2':'E', '3':'H', '4':'A'}
        client.modes = {'2':'E', '3':'H', '4':'A'}
        assert client.modes == expected

    def test_modes_set_error_bad_mode(self, client):
        with pytest.raises(PilotwireModesInconsistent):
            client.modes = {'1':'Z'}

    def test_modes_set_error_bad_zone(self, client):
        with pytest.raises(PilotwireModesInconsistent):
            client.modes = {'Z':'C'}


class TestControllerProxyMethods:

    def test_test_method(self, client):
        assert client.test() is True

    def test_service_not_found_status(self, client, server):
        server.stop()
        assert client.check_status() == 'service_not_found'

    def test_connection_error_status(self, client, server):
        client.test()
        server.stop()
        assert client.check_status() == 'connection_error'

    def test_xml_rpc_error_status(self, client):
        client.test = MethodType(lambda s: s._xmlrpc_client.zest(), client)
        assert client.check_status() == 'xml-rpc_error'

    def test_unknown_error_status(self, client):
        client.test = None
        assert client.check_status() == 'unknown_error'

    def test_unknown_status(self, client):
        client.test = MethodType(lambda s: False, client)
        assert client.check_status() == 'unknown_status'

    def test_active_status(self, client):
        assert client.check_status() == 'active'
