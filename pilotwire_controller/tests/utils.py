# -*- coding: utf-8 -*-

from ..controller.base import BaseController


class TestingController(BaseController):

    def __init__(self):
        self._out = 0

    @property
    def output_value(self):
        return self._out

    @output_value.setter
    def output_value(self, val):
        self._out = val
