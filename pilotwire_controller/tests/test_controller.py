# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch, PropertyMock

from ..controller.base import BaseController
from ..controller.piface import PiFaceController


output_to_modes = (
    (0,           {'1':'C', '2':'C', '3':'C', '4':'C'}),
    (0b10011100 , {'1':'C', '2':'E', '3':'H', '4':'A'}),
    (0b100000000, {'1':'C', '2':'C', '3':'C', '4':'C'}),
)

modes_to_output = (
    ({}, 0),
    ({'1':'C', '2':'E', '3':'H', '4':'A'}, 0b10011100),
    ({'4':'E', 'X':'Z'}, 0b11000000),
)


class TestingController(BaseController):

    def __init__(self):
        self._out = 0

    @property
    def output_value(self):
        return self._out

    @output_value.setter
    def output_value(self, val):
        self._out = val


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
