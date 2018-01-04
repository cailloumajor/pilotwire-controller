import random
import sys
import types
from unittest.mock import Mock

module_name = 'pifacedigitalio'
mocked = types.ModuleType(module_name)
sys.modules[module_name] = mocked
mocked.PiFaceDigital = Mock(name=module_name+'.PiFaceDigital')


def pytest_generate_tests(metafunc):
    if 'good_modes_str' in metafunc.fixturenames:
        random.seed()
        modes_strings = [
            ''.join(random.choices(['A', 'C', 'E', 'H'], k=k))
            for k in range(1, 5)
        ]
        metafunc.parametrize('good_modes_str', modes_strings)
