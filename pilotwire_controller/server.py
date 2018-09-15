import logging

import rpyc
from cached_property import threaded_cached_property

from pilotwire_controller.piface import PiFaceController


# pylint: disable=attribute-defined-outside-init
class PilotwireControllerService(rpyc.Service):
    @threaded_cached_property
    def controller(self):
        return PiFaceController()

    def exposed_get_modes(self):
        return self.controller.modes

    def exposed_set_modes(self, modes):
        self.controller.modes = modes


def main(**kwargs):
    logging.basicConfig(level=logging.DEBUG)
    server = rpyc.ThreadedServer(PilotwireControllerService(), **kwargs)
    server.start()
