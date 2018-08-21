import sys
import types
from unittest.mock import Mock


module_name = "pifacedigitalio"
mocked = types.ModuleType(module_name)
sys.modules[module_name] = mocked
fakepfd = Mock(name=module_name + ".PiFaceDigital")
fakepfd.return_value.output_port.value = 0
mocked.PiFaceDigital = fakepfd
