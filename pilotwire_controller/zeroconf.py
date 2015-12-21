# -*- coding: utf-8 -*-

import socket

from zeroconf import Zeroconf, ServiceInfo


NAME = "Pilotwire Controller"
SRV_TYPE = '_xml-rpc._tcp.local.'

srv_fqname = '.'.join((NAME, SRV_TYPE))


class ServiceDiscoveryServer:

    def __init__(self, port):
        hostname = socket.gethostname()
        addr = socket.gethostbyname(hostname)
        addr = socket.inet_aton(addr)
        self.zeroconf = Zeroconf()
        self.info = ServiceInfo(
            SRV_TYPE, srv_fqname, addr, port, 0, 0,
            {}, '{}.local.'.format(hostname)
        )

    def start(self):
        self.zeroconf.register_service(self.info)

    def stop(self):
        self.zeroconf.unregister_service(self.info)
        self.zeroconf.close()
