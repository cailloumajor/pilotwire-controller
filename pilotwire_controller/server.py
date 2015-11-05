#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pifacedigitalio
from xmlrpc.server import SimpleXMLRPCServer

from . import BaseController


XMLRPC_PORT = 8888


class Controller(BaseController):

    def __init__(self):
        self._piface = pifacedigitalio.PiFaceDigital()
        self._piface.output_port.all_off()

    @property
    def output_value(self):
        return self._piface.output_port.value

    @output_value.setter
    def output_value(self, val):
        self._piface.output_port.value = val


def main():
    server = SimpleXMLRPCServer(('', XMLRPC_PORT))
    server.register_instance(Controller())
    server.serve_forever()


if __name__ == '__main__':
    sys.exit(main())
