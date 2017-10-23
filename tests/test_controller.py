# pylint: disable=protected-access, redefined-outer-name, unused-argument
# pylint: disable=no-self-use

from unittest.mock import patch, PropertyMock

import pytest

from pilotwire_controller import piface


@pytest.yield_fixture
def piface_fixture():
    patcher = patch(
        '{}.pifacedigitalio.PiFaceDigital'.format(
            piface.PiFaceController.__module__))
    patcher.start()
    controller = piface.PiFaceController()
    mock_out_value = PropertyMock()
    type(controller._piface.output_port).value = mock_out_value
    yield {'controller': controller, 'output_port': mock_out_value}
    patcher.stop()


class TestPiFaceController:

    def test_piface_all_off_called(self, piface_fixture):
        all_off = piface_fixture['controller']._piface.output_port.all_off
        all_off.assert_called_once_with()

    @pytest.mark.parametrize('output,modes', [
        (0, 'CCCC'),
        (0b10011100, 'CEHA'),
        (0b100000000, 'CCCC'),
    ])
    def test_piface_modes_getter(self, piface_fixture, output, modes):
        piface_fixture['output_port'].return_value = output
        assert piface_fixture['controller'].modes == modes

    @pytest.mark.parametrize('modes,output', [
        ('', 0),
        ('CEHA', 0b10011100),
    ])
    def test_piface_modes_setter(self, piface_fixture, modes, output):
        piface_fixture['controller'].modes = modes
        piface_fixture['output_port'].assert_called_with(output)
