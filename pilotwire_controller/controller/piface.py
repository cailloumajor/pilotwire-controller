# -*- coding: utf-8 -*-

import pifacedigitalio  # pylint: disable=import-error

from .base import BaseController


class PiFaceController(BaseController):

    def __init__(self):
        self._piface = pifacedigitalio.PiFaceDigital()
        self._piface.output_port.all_off()

    @property
    def output_value(self):
        return self._piface.output_port.value

    @output_value.setter
    def output_value(self, outval):
        self._piface.output_port.value = outval
