# -*- coding: utf-8 -*-

from socket import gethostname, gethostbyname
from unittest import TestCase

from ..zeroconf import (ServiceDiscoveryClient,
                        ServiceDiscoveryServer,
                        ZeroconfServiceNotFound)

class TestZeroconfDiscovery(TestCase):

    SRV_PORT = 8889

    @classmethod
    def setUpClass(cls):
        cls.client = ServiceDiscoveryClient(500)

    def test_service_not_found(self):
        self.assertRaises(
            ZeroconfServiceNotFound, getattr, self.client, 'address')
        self.assertRaises(
            ZeroconfServiceNotFound, getattr, self.client, 'port')

    def test_service_properties(self):
        address = gethostbyname(gethostname())
        server = ServiceDiscoveryServer(self.SRV_PORT)
        server.start()
        self.assertEqual(self.client.address, address)
        self.assertEqual(self.client.port, str(self.SRV_PORT))
        server.stop()
