import pifacedigitalio


BINARY_MODE = {
    'C': '00',
    'E': '11',
    'H': '01',
    'A': '10',
}
MODE_BINARY = {v: k for k, v in BINARY_MODE.items()}


class PiFaceController:

    def __init__(self):
        self._piface = pifacedigitalio.PiFaceDigital()
        self._piface.output_port.all_off()

    @property
    def modes(self):
        """
        Get or set modes as a 4-character string.
        """
        out_port = self._piface.output_port.value
        bitpairs = [(out_port & (0b11 << r)) >> r for r in range(0, 8, 2)]
        binaries = ['{:02b}'.format(b) for b in bitpairs]
        modes = [MODE_BINARY[b] for b in binaries]
        return ''.join(modes)

    @modes.setter
    def modes(self, modes_str):
        binaries = [BINARY_MODE.get(m, '00') for m in modes_str]
        bitpairs = [int(b, 2) for b in binaries]
        out_port = sum([v << (i * 2) for i, v in enumerate(bitpairs)])
        self._piface.output_port.value = out_port
