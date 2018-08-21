# pylint: disable=redefined-outer-name
import pytest
import rpyc

from pilotwire_controller.server import PilotwireControllerService


@pytest.fixture
def rpyc_service():
    conn = rpyc.connect_thread(
        remote_service=PilotwireControllerService,
        remote_config={"allow_public_attrs": True, "allow_setattr": True},
    )
    yield conn.root
    conn.close()


def test_get_modes(rpyc_service):
    modes = "ACEH"
    assert rpyc_service.get_modes() != modes
    rpyc_service.controller.modes = modes
    assert rpyc_service.get_modes() == modes


def test_set_modes(rpyc_service):
    modes = "HECA"
    assert rpyc_service.controller.modes != modes
    rpyc_service.set_modes(modes)
    assert rpyc_service.controller.modes == modes
