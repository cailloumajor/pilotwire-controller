# -*- coding: utf-8 -*-

from unittest.mock import patch, PropertyMock

import pytest

from pilotwire_controller.controller import testing, piface


@pytest.fixture
def testing_controller():
    return testing.TestingController()

@pytest.yield_fixture
def piface_fixture():
    class Fixture:
        def __init__(self, controller, output_port):
            self.controller = controller
            self.output_port = output_port
    patcher = patch(
        '{}.pifacedigitalio.PiFaceDigital'.format(
            piface.PiFaceController.__module__))
    patcher.start()
    controller = piface.PiFaceController()
    mock_out_value = PropertyMock()
    type(controller._piface.output_port).value = mock_out_value
    yield Fixture(controller, mock_out_value)
    patcher.stop()


class TestBaseController:

    def test_base_mode_dict_getter(self, testing_controller, output, modes):
        testing_controller._out = output
        assert testing_controller.modes_dict == modes

    def test_base_mode_dict_setter(self, testing_controller, modes, output):
        testing_controller.modes_dict = modes
        assert testing_controller._out == output


class TestPiFaceController:

    def test_piface_all_off_called(self, piface_fixture):
        all_off = piface_fixture.controller._piface.output_port.all_off
        all_off.assert_called_once_with()

    def test_piface_mode_dict_getter(self, piface_fixture, output, modes):
        piface_fixture.output_port.return_value = output
        assert piface_fixture.controller.modes_dict == modes

    def test_piface_mode_dict_setter(self, piface_fixture, modes, output):
        piface_fixture.controller.modes_dict = modes
        piface_fixture.output_port.assert_called_with(output)
