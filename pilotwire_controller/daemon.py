# -*- coding: utf-8 -*-

import argparse
import logging
import sys

from .server import PilotwireServer
from .zeroconf import ServiceDiscoveryServer


DEFAULT_OPTIONS = {
    'debug': False,
    'port': 8888,
    'controller_type': 'piface',
}


def _init_logging(debug):
    lvl = 'DEBUG' if debug else 'INFO'
    for logger_name in ('stevedore', 'zeroconf'):
        logger = logging.getLogger(logger_name)
        logger.setLevel(lvl)
        handler = logging.StreamHandler()
        handler.setLevel(lvl)
        logger.addHandler(handler)


def run(**kwargs):
    import atexit

    options = DEFAULT_OPTIONS.copy()
    options.update(kwargs)
    if __name__ == '__main__':
        from . import zeroconf
        zeroconf.NAME = 'Test'
        options['controller_type'] = 'test'

    _init_logging(options['debug'])

    server = PilotwireServer(
        options['port'], options['debug'], options['controller_type']
    )
    zeroconf = ServiceDiscoveryServer(options['port'])

    atexit.register(server.stop)
    atexit.register(zeroconf.stop)

    zeroconf.start()
    server.start()


def parse_args(args):
    parser = argparse.ArgumentParser(description="Pilotwire controller server")
    parser.add_argument('-d', dest='debug', action='store_true',
                        help="output debugging messages")
    parser.add_argument('-p', dest='port', default=8888, type=int,
                        help="port number on which listen")
    return parser.parse_args(args)


def main():
    run(**vars(parse_args(sys.argv[1:])))


if __name__ == '__main__':
    main()
