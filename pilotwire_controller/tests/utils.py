# -*- coding: utf-8 -*-

from ..controller.base import BaseController


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
