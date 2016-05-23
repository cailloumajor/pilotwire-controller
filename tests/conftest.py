# -*- coding: utf-8 -*-

import pytest


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
