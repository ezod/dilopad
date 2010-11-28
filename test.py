#!/usr/bin/env python

"""\
Unit tests for Dilopad.

@author: Aaron Mavrinac
@contact: mavrinac@gmail.com
@license: GPL-3
"""

import unittest

from dilo.device import Circuit
from dilo.devices.gates import NOTGate, ANDGate, ORGate, NORGate


class TestExamples(unittest.TestCase):
    def setUp(self):
        pass

    def test_combinational_simple(self):
        result = []
        C = Circuit()
        C.add('one', NOTGate())
        C.add('two', ANDGate())
        C.add('three', ORGate())
        C.add('four', NOTGate())
        C.add('five', ORGate())
        C.connect('one', 'q', 'two', 'a')
        C.connect('two', 'q', 'five', 'a')
        C.connect('three', 'q', 'four', 'a')
        C.connect('four', 'q', 'five', 'b')
        for x in [False, True]:
            for y in [False, True]:
                for z in [False, True]:
                    C.set_input('one.a', x)
                    C.set_input('three.a', x)
                    C.set_input('two.b', y)
                    C.set_input('three.b', z)
                    result.append(C.get_output('five.q'))
        self.assertEqual(result, [True, False, True, True] + [False] * 4)

    def test_latch_sr_nor(self):
        result = []
        L = Circuit()
        L.add('r', NORGate())
        L.add('s', NORGate())
        L.connect('r', 'q', 's', 'a')
        L.connect('s', 'q', 'r', 'b')
        for i in range(2):
            for inputid in ['s.b', 'r.a']:
                for value in [True, False]:
                    L.set_input(inputid, value)
                    result.append(L.get_output('r.q'))
        self.assertEqual(result, [True, True, False, False] * 2)


if __name__ == '__main__':
    unittest.main()
