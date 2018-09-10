# pylint: disable=protected-access
import pytest

from pilotwire_controller.piface import PiFaceController


@pytest.mark.parametrize(
    "output,modes", [(0, "CCCC"), (0b10011100, "CEHA"), (0b100000000, "CCCC")]
)
def test_piface_modes_getter(output, modes):
    controller = PiFaceController()
    controller._piface.output_port.value = output
    assert controller.modes == modes


@pytest.mark.parametrize(
    "modes,output", [("", 0), ("CEHA", 0b10011100), ("____", 0), ("EEEEE", 0b11111111)]
)
def test_piface_modes_setter(modes, output):
    controller = PiFaceController()
    controller.modes = modes
    assert controller._piface.output_port.value == output
