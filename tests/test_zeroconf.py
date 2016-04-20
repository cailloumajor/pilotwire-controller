# -*- coding: utf-8 -*-
# pylint: disable=protected-access, redefined-outer-name, unused-argument

import netifaces
import pytest

from pilotwire_controller.zeroconf import (ServiceDiscoveryClient,
                                           ServiceDiscoveryServer,
                                           ZeroconfServiceNotFound)


SRV_PORT = 8889


@pytest.fixture
def client():
    return ServiceDiscoveryClient(300)

@pytest.yield_fixture
def server():
    srv = ServiceDiscoveryServer(SRV_PORT)
    srv.start()
    yield srv
    srv.stop()

@pytest.fixture
def address():
    inet = netifaces.AF_INET
    def_gw = netifaces.gateways()['default'][inet][1]
    return netifaces.ifaddresses(def_gw)[inet][0]['addr']


def test_service_not_found_getting_address(client):
    with pytest.raises(ZeroconfServiceNotFound):
        getattr(client, 'address')

def test_service_not_found_getting_port(client):
    with pytest.raises(ZeroconfServiceNotFound):
        getattr(client, 'port')

def test_service_properties(server, client, address):
    assert client.address == address
    assert client.port, str(SRV_PORT)
