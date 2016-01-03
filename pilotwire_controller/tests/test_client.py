# -*- coding: utf-8 -*-

from multiprocessing import Process
from types import MethodType
from unittest import TestCase

from ..client import ControllerProxy, PilotwireModesInconsistent
from .. import daemon


class ControllerProxyTestCase(TestCase):

    def stop_server(self):
        self.server_process.terminate()
        self.server_process.join()

    def setUp(self):
        self.server_process = Process(
            target=daemon.run, kwargs=dict(controller_type='test')
        )
        self.server_process.start()
        self.client = ControllerProxy(500)

    def tearDown(self):
        del self.client
        self.stop_server()


class TestControllerProxyProperties(ControllerProxyTestCase):

    def test_modes_getter(self):
        expected = {'1':'C', '2':'C', '3':'C', '4':'C'}
        self.assertEqual(self.client.modes, expected)

    def test_modes_setter(self):
        expected = {'1':'C', '2':'E', '3':'H', '4':'A'}
        self.client.modes = {'2':'E', '3':'H', '4':'A'}
        self.assertEqual(self.client.modes, expected)

    def test_modes_set_error(self):
        self.assertRaises(
            PilotwireModesInconsistent,
            setattr, self.client, 'modes', {'1':'Z'})
        self.assertRaises(
            PilotwireModesInconsistent,
            setattr, self.client, 'modes', {'Z':'C'})


class TestControllerProxyMethods(ControllerProxyTestCase):

    def test_test_method(self):
        self.assertIs(self.client.test(), True)

    def test_service_not_found_status(self):
        self.stop_server()
        self.assertEqual(self.client.check_status(), 'service_not_found')

    def test_connection_error_status(self):
        self.client.test()
        self.stop_server()
        self.assertEqual(self.client.check_status(), 'connection_error')

    def test_xml_rpc_error_status(self):
        self.client.test = MethodType(
            lambda s: s._xmlrpc_client.zest(), self.client)
        self.assertEqual(self.client.check_status(), 'xml-rpc_error')

    def test_unknown_error_status(self):
        self.client.test = None
        self.assertEqual(self.client.check_status(), 'unknown_error')

    def test_unknown_status(self):
        self.client.test = MethodType(lambda s: False, self.client)
        self.assertEqual(self.client.check_status(), 'unknown_status')

    def test_active_status(self):
        self.assertEqual(self.client.check_status(), 'active')
