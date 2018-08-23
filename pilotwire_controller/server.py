import fire
import rpyc

from pilotwire_controller.piface import PiFaceController


# pylint: disable=attribute-defined-outside-init
class PilotwireControllerService(rpyc.Service):
    def on_connect(self, conn):
        self.controller = PiFaceController()
        print()

    def exposed_get_modes(self):
        return self.controller.modes

    def exposed_set_modes(self, modes):
        self.controller.modes = modes


def main(**kwargs):
    server = rpyc.ThreadedServer(PilotwireControllerService(), **kwargs)
    server.start()


if __name__ == "__main__":
    fire.Fire(main)
