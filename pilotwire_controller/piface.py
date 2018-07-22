import pifacedigitalio  # pylint: disable=import-error


DIBIT_FOR_MODE = {"C": 0b00, "E": 0b11, "H": 0b01, "A": 0b10}
MODE_FOR_DIBIT = {v: k for k, v in DIBIT_FOR_MODE.items()}


class PiFaceController:
    def __init__(self):
        self._piface = pifacedigitalio.PiFaceDigital()

    @property
    def modes(self):
        """
        Get or set modes as a 4-character string.
        """
        out_port = self._piface.output_port.value
        dibits = [(out_port & (0b11 << r)) >> r for r in range(0, 8, 2)]
        modes = [MODE_FOR_DIBIT[b] for b in dibits]
        return "".join(modes)

    @modes.setter
    def modes(self, modes_str):
        dibits = [DIBIT_FOR_MODE.get(m, 0b00) for m in modes_str]
        out_port = sum(v << (i * 2) for i, v in enumerate(dibits))
        self._piface.output_port.value = out_port
