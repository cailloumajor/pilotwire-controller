# -*- coding: utf-8 -*-

import pprint
import sys
from unittest.mock import Mock

sys.modules['pifacedigitalio'] = Mock()
from pilotwire_controller import daemon  # noqa


class FakeServer:

    def __init__(self, *args, **kwargs):
        fargs = pprint.pformat(args)
        fkwargs = pprint.pformat(kwargs)
        self._print("instanciated with args {} and kwargs {}".format(
            fargs, fkwargs))

    def _print(self, text):
        _text = self.__class__.__name__ + ": " + text
        print(_text)

    def start(self):
        self._print('started')

    def stop(self):
        self._print('stopped')


class FakePilotwireServer(FakeServer):
    pass


class FakeServiceDiscoveryServer(FakeServer):
    pass


if __name__ == '__main__':
    daemon.PilotwireServer = FakePilotwireServer
    daemon.ServiceDiscoveryServer = FakeServiceDiscoveryServer
    daemon.main()
