import pytest

from pilotwire_controller.piface import PiFaceController


def test_all_off_called(piface_mock):
    piface_mock.reset_mock()
    controller = PiFaceController()
    controller._piface.output_port.all_off.assert_called_once()


@pytest.mark.parametrize('output,modes', [
    (0, 'CCCC'),
    (0b10011100, 'CEHA'),
    (0b100000000, 'CCCC'),
])
def test_piface_modes_getter(output, modes):
    controller = PiFaceController()
    controller._piface.output_port.value = output
    assert controller.modes == modes


@pytest.mark.parametrize('modes,output', [
    ('', 0),
    ('CEHA', 0b10011100),
    ('____', 0)
])
def test_piface_modes_setter(modes, output):
    controller = PiFaceController()
    controller.modes = modes
    assert controller._piface.output_port.value == output
