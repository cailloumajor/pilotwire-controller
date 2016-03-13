# -*- coding: utf-8 -*-

import socket

from cached_property import cached_property_with_ttl
from zeroconf import Zeroconf, ServiceInfo


NAME = "Pilotwire Controller"
SRV_TYPE = '_xml-rpc._tcp.local.'

SRV_FQNAME = '.'.join((NAME, SRV_TYPE))


class ZeroconfServiceNotFound(Exception):
    pass


class ServiceDiscoveryServer:

    def __init__(self, port):
        hostname = socket.gethostname()
        addr = socket.gethostbyname(hostname)
        addr = socket.inet_aton(addr)
        self.zeroconf = Zeroconf()
        self.info = ServiceInfo(
            SRV_TYPE, SRV_FQNAME, addr, port, 0, 0,
            {}, '{}.local.'.format(hostname)
        )

    def start(self):
        self.zeroconf.register_service(self.info)

    def stop(self):
        self.zeroconf.unregister_service(self.info)
        self.zeroconf.close()


class ServiceDiscoveryClient:

    def __init__(self, service_timeout=None):
        self.zeroconf = Zeroconf()
        self.service_args = [SRV_TYPE, SRV_FQNAME]
        if service_timeout:
            self.service_args.append(service_timeout)

    @cached_property_with_ttl(ttl=1.0)
    def info(self):
        service_info = self.zeroconf.get_service_info(*self.service_args)
        if not service_info:
            raise ZeroconfServiceNotFound(
                "Pilotwire Controller Zeroconf service not found"
            )
        return service_info

    @property
    def address(self):
        return socket.inet_ntoa(self.info.address)

    @property
    def port(self):
        return str(self.info.port)
