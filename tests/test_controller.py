# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch, PropertyMock

from .utils import TestingController, output_to_modes, modes_to_output
from ..controller.piface import PiFaceController


class TestBaseController(TestCase):

    def setUp(self):
        self.controller = TestingController()

    def test_base_mode_dict_getter(self):
        for i, d in output_to_modes:
            self.controller._out = i
            self.assertEqual(self.controller.modes_dict, d)

    def test_base_mode_dict_setter(self):
        for d, i in modes_to_output:
            self.controller.modes_dict = d
            self.assertEqual(self.controller._out, i)


class TestPiFaceController(TestCase):

    def setUp(self):
        patcher = patch(
            '{}.pifacedigitalio.PiFaceDigital'.format(
                PiFaceController.__module__))
        patcher.start()
        self.addCleanup(patcher.stop)
        self.controller = PiFaceController()
        self.mock_out_value = PropertyMock()
        type(self.controller._piface.output_port).value = self.mock_out_value

    def test_piface_all_off_called(self):
        all_off = self.controller._piface.output_port.all_off
        all_off.assert_called_once_with()

    def test_piface_mode_dict_getter(self):
        for i, d in output_to_modes:
            self.mock_out_value.return_value = i
            self.assertEqual(self.controller.modes_dict, d)

    def test_piface_mode_dict_setter(self):
        for d, i in modes_to_output:
            self.controller.modes_dict = d
            self.mock_out_value.assert_called_with(i)
