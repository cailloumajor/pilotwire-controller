import sys
from unittest.mock import Mock

import pytest


mock = Mock()
sys.modules['pifacedigitalio'] = mock


@pytest.fixture
def piface_mock():
    return mock
