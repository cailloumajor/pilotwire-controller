# -*- coding: utf-8 -*-


ZONES = [1, 2, 3, 4]


class BaseController(object):

    modes_out = {
        'C': '00',
        'E': '11',
        'H': '01',
        'A': '10',
    }

    @property
    def modes_dict(self):
        output_integer = self.output_value
        rev_modes_out = {v: k for k, v in self.modes_out.items()}
        def get_bit_pair(integer, position):
            """Get a bit pair string from an integer,
            given the pair position.
            """
            shift = (position - 1) * 2
            integer_bitpair = (integer & (0b11 << shift)) >> shift
            return '{:02b}'.format(integer_bitpair)
        return {
            str(z): rev_modes_out.get(get_bit_pair(output_integer, z))
            for z in ZONES
        }

    @modes_dict.setter
    def modes_dict(self, dct):
        zones_modes = [(z, dct.get(str(z), 'C')) for z in ZONES]
        zones_int = [
            int(self.modes_out.get(m, '00'), 2) << ((n - 1) * 2)
            for n, m in zones_modes
        ]
        self.output_value = sum(zones_int)

    def getModes(self):
        return self.modes_dict

    def setModes(self, modes_dict):
        if not isinstance(modes_dict, dict):
            raise TypeError("setModes: bad argument type (dict expected)")
        self.modes_dict = modes_dict
        return self.modes_dict

    def test(self):
        return True
