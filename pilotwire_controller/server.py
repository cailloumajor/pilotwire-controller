# -*- coding: utf-8 -*-

import sys
import argparse
from xmlrpc.server import SimpleXMLRPCServer

from stevedore import driver


class XMLRPCMethods:

    def __init__(self, controller):
        self.controller = controller

    def getModes(self):
        return self.controller.modes_dict

    def setModes(self, modes_dict):
        self.controller.modes_dict = modes_dict
        return self.controller.modes_dict

    def test(self):
        return True


class PilotwireServer:

    def __init__(self, port, debug, controller_name):
        self.xmlrpc_server = SimpleXMLRPCServer(('', port), logRequests=debug)
        self.controller = driver.DriverManager(
            namespace='pilotwire.controller',
            name=controller_name,
            invoke_on_load=True,
            verify_requirements=True,
        )
        self.xmlrpc_server.register_instance(XMLRPCMethods(self.controller))

    def start(self):
        self.xmlrpc_server.serve_forever()

    def stop(self):
        self.xmlrpc_server.shutdown()
        self.xmlrpc_server.server_close()


def main():
    parser = argparse.ArgumentParser("Pilotwire controller server")
    parser.add_argument('-d', dest='debug', action='store_true',
                        help="output debugging messages (eg. XML-RPC requests)")
    parser.add_argument('-p', dest='port', default=8888, type=int,
                        help="port number on which listen")
    args = parser.parse_args()
    server = PilotwireServer(args.port, args.debug, 'piface')
    sys.exit(server.start())
