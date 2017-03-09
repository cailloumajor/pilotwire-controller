# -*- coding: utf-8 -*-
# pylint: disable=protected-access, redefined-outer-name, unused-argument

from threading import Thread
from xmlrpc.client import ServerProxy

import pytest

from pilotwire_controller.server import PilotwireServer


pytestmark = pytest.mark.usefixtures('test_controller')


@pytest.yield_fixture
def server():
    srv = PilotwireServer(0, False)
    thread = Thread(target=srv.start)
    thread.start()
    yield srv
    srv.stop()
    thread.join()


@pytest.fixture
def client(server):
    _, port = server.xmlrpc_server.socket.getsockname()
    return ServerProxy('http://localhost:{}'.format(port))


def test_server_set_modes(server, client, modes, output):
    client.setModes(modes)
    assert server.controller._out == output


def test_server_get_modes(server, client, output, modes):
    server.controller._out = output
    assert client.getModes() == modes


def test_server_test(server, client):
    assert client.test() is True
