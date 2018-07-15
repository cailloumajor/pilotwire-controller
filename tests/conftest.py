import sys
import types
from unittest.mock import Mock


module_name = "pifacedigitalio"
mocked = types.ModuleType(module_name)
sys.modules[module_name] = mocked
mocked.PiFaceDigital = Mock(name=module_name + ".PiFaceDigital")
