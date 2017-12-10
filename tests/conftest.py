import random
import sys
from unittest.mock import Mock

import pytest


mock = Mock()
sys.modules['pifacedigitalio'] = mock


def pytest_generate_tests(metafunc):
    if 'good_modes_str' in metafunc.fixturenames:
        random.seed()
        modes_strings = [
            ''.join(random.choices(['A', 'C', 'E', 'H'], k=k))
            for k in range(1, 5)
        ]
        metafunc.parametrize('good_modes_str', modes_strings)


@pytest.fixture
def piface_mock():
    return mock
