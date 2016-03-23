# -*- coding: utf-8 -*-

from threading import Thread
from unittest import TestCase
from xmlrpc.client import ServerProxy

from .utils import modes_to_output, output_to_modes
from ..server import PilotwireServer


class TestPilotwireServer(TestCase):

    def setUp(self):
        self.server = PilotwireServer(0, False, 'test')
        addr, port = self.server.xmlrpc_server.socket.getsockname()
        self.server_thread = Thread(target=self.server.start)
        self.client = ServerProxy('http://localhost:{}'.format(port))
        self.server_thread.start()

    def tearDown(self):
        self.server.stop()
        self.server_thread.join()

    def test_server_set_modes(self):
        for d, i in modes_to_output:
            self.client.setModes(d)
            self.assertEqual(self.server.controller._out, i)

    def test_server_get_modes(self):
        for i, d in output_to_modes:
            self.server.controller._out = i
            self.assertEqual(self.client.getModes(), d)
