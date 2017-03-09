# -*- coding: utf-8 -*-

from xmlrpc.server import SimpleXMLRPCServer

from .controller.piface import PiFaceController as Controller


class XMLRPCMethods:

    def __init__(self, controller):
        self.controller = controller

    def getModes(self):
        return self.controller.modes_dict

    def setModes(self, modes_dict):
        self.controller.modes_dict = modes_dict
        return self.controller.modes_dict

    def test(self):
        # pylint: disable=no-self-use
        return True


class PilotwireServer:

    def __init__(self, port, debug):
        self.xmlrpc_server = SimpleXMLRPCServer(('', port), logRequests=debug)
        self.controller = Controller()
        self.xmlrpc_server.register_instance(XMLRPCMethods(self.controller))

    def start(self):
        self.xmlrpc_server.serve_forever()

    def stop(self):
        self.xmlrpc_server.shutdown()
        self.xmlrpc_server.server_close()
