# -*- coding: utf-8 -*-

import argparse
import logging

from .server import PilotwireServer
from .zeroconf import ServiceDiscoveryServer


def _init_logging(debug):
    lvl = 'DEBUG' if debug else 'INFO'
    for logger_name in ('stevedore', 'zeroconf'):
        logger = logging.getLogger(logger_name)
        logger.setLevel(lvl)
        handler = logging.StreamHandler()
        handler.setLevel(lvl)
        logger.addHandler(handler)


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Pilotwire controller server")
    parser.add_argument('-d', dest='debug', action='store_true',
                        help="output debugging messages")
    parser.add_argument('-p', dest='port', default=8888, type=int,
                        help="port number on which listen")
    return parser.parse_args(args)


def main():
    import atexit

    args = parse_args()

    _init_logging(args.debug)

    server = PilotwireServer(args.port, args.debug, 'piface')
    zeroconf = ServiceDiscoveryServer(args.port)

    atexit.register(server.stop)
    atexit.register(zeroconf.stop)

    zeroconf.start()
    server.start()


if __name__ == '__main__':
    main()
