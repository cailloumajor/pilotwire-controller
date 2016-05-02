# -*- coding: utf-8 -*-
# pylint: disable=protected-access, redefined-outer-name, unused-argument

import subprocess
import textwrap

import pytest

from pilotwire_controller import daemon


FAKED_DAEMON_OUTPUT = textwrap.dedent(
    """\
    FakePilotwireServer: instanciated with args {} and kwargs {}
    FakeServiceDiscoveryServer: instanciated with args {} and kwargs {}
    FakeServiceDiscoveryServer: started
    FakePilotwireServer: started
    FakeServiceDiscoveryServer: stopped
    FakePilotwireServer: stopped
    """)


@pytest.mark.parametrize('args,expected', [
    ([], False),
    (['-d'], True),
])
def test_debug_argument(args, expected):
    parser = daemon.parse_args(args)
    assert parser.debug == expected


@pytest.mark.parametrize('args,expected', [
    ([], 8888),
    (['-p', '1234'], 1234),
    (['-p', 'str'], SystemExit),
])
def test_port_argument(args, expected):
    if isinstance(expected, type) and issubclass(expected, BaseException):
        with pytest.raises(expected):
            parser = daemon.parse_args(args)
    else:
        parser = daemon.parse_args(args)
        assert parser.port == expected


@pytest.mark.parametrize('args,output', [
    ([], ("(8888, False, 'piface')", '{}', "(8888,)", '{}')),
    (['-d'], ("(8888, True, 'piface')", '{}', "(8888,)", '{}')),
    (['-p', '1234'], ("(1234, False, 'piface')", '{}', "(1234,)", '{}')),
    (['-d', '-p', '5678'], ("(5678, True, 'piface')", '{}', "(5678,)", '{}')),
])
def test_faked_daemon(args, output):
    cmd = ['python', 'tests/faked_daemon_stub.py']
    cmd.extend(args)
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True)
    return_code = process.wait(timeout=1)
    out, err = process.communicate()
    assert return_code == 0
    assert err is None
    assert out == FAKED_DAEMON_OUTPUT.format(*output)
