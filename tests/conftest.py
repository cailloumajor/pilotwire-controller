# -*- coding: utf-8 -*-

import sys
from unittest.mock import Mock

import pytest

from pilotwire_controller.controller.base import BaseController


sys.modules['pifacedigitalio'] = Mock()


OUTPUT_TO_MODES = [
    (0, {'1': 'C', '2': 'C', '3': 'C', '4': 'C'}),
    (0b10011100, {'1': 'C', '2': 'E', '3': 'H', '4': 'A'}),
    (0b100000000, {'1': 'C', '2': 'C', '3': 'C', '4': 'C'}),
]

MODES_TO_OUTPUT = [
    ({}, 0),
    ({'1': 'C', '2': 'E', '3': 'H', '4': 'A'}, 0b10011100),
    ({'4': 'E', 'X': 'Z'}, 0b11000000),
]


def pytest_generate_tests(metafunc):
    fixtures_str = ','.join(metafunc.fixturenames)
    if 'output,modes' in fixtures_str:
        metafunc.parametrize(['output', 'modes'], OUTPUT_TO_MODES)
    if 'modes,output' in fixtures_str:
        metafunc.parametrize(['modes', 'output'], MODES_TO_OUTPUT)


@pytest.fixture
def patch_zeroconf_name(monkeypatch):
    monkeypatch.setattr('pilotwire_controller.zeroconf.NAME', 'Test')


class TestingController(BaseController):

    def __init__(self):
        self._out = 0

    @property
    def output_value(self):
        return self._out

    @output_value.setter
    def output_value(self, val):
        self._out = val


@pytest.fixture
def test_controller(monkeypatch):
    monkeypatch.setattr(
        'pilotwire_controller.server.Controller',
        TestingController
    )
    return TestingController()
