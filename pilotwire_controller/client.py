# -*- coding: utf-8 -*-

import socket

from xmlrpc.client import ServerProxy, Fault as XMLRPCFault

from cached_property import cached_property

from .zeroconf import ServiceDiscoveryClient, ZeroconfServiceNotFound


class PilotwireModesInconsistent(Exception):
    pass


class ControllerProxy:

    def __init__(self, zeroconf_timeout=None):
        self.zeroconf_timeout = zeroconf_timeout

    @cached_property
    def _xmlrpc_client(self):
        zeroconf_service = ServiceDiscoveryClient(self.zeroconf_timeout)
        return ServerProxy(
            'http://{s.address}:{s.port}/'.format(s=zeroconf_service)
        )

    @property
    def modes(self):
        return self._xmlrpc_client.getModes()

    @modes.setter
    def modes(self, modes_dict):
        response = self._xmlrpc_client.setModes(modes_dict)
        if not all(item in response.items() for item in modes_dict.items()):
            raise PilotwireModesInconsistent(
                "Modes on controller not reflecting requested modes"
            )

    def test(self):
        return self._xmlrpc_client.test()

    def check_status(self):
        # pylint: disable=broad-except
        socket.setdefaulttimeout(3)

        try:
            result = self.test()
        except ZeroconfServiceNotFound:
            return 'service_not_found'
        except ConnectionError:
            return 'connection_error'
        except XMLRPCFault:
            return 'xml-rpc_error'
        except Exception:
            return 'unknown_error'
        else:
            if result is True:
                return 'active'
            else:
                return 'unknown_status'
        finally:
            socket.setdefaulttimeout(None)
