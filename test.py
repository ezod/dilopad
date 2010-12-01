#!/usr/bin/env python

"""\
Unit tests for Dilopad.

@author: Aaron Mavrinac
@contact: mavrinac@gmail.com
@license: GPL-3
"""

import unittest

from dilo.boolean import BooleanExpression
from dilo.device import Circuit
from dilo.devices.gates import NOTGate, ANDGate, ORGate, NANDGate, NORGate, XNORGate


class TestExamples(unittest.TestCase):
    def setUp(self):
        pass

    def test_boolean(self):
        result = []
        F = BooleanExpression("((A' + B) * C + C' * D)'")
        for a in [False, True]:
            for b in [False, True]:
                for c in [False, True]:
                    for d in [False, True]:
                        result.append(F.evaluate({'A': a, 'B': b, 'C': c, 'D': d}))
        self.assertEqual(result, [True, False, False, False, True, False, False, False, True, False, True, True, True, False, False, False])

    def test_combinational(self):
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

    def test_combinational_boolean(self):
        C = Circuit()
        C.add('one', XNORGate())
        C.add('two', NOTGate())
        C.add('three', ANDGate())
        C.add('four', ANDGate())
        C.add('five', ANDGate())
        C.add('six', NANDGate())
        C.add('seven', ORGate())
        C.add('eight', ANDGate())
        C.add('nine', NOTGate())
        C.add('ten', ORGate())
        C.add('eleven', ORGate())
        C.connect('one', 'q', 'three', 'a')
        C.connect('two', 'q', 'four', 'a')
        C.connect('three', 'q', 'seven', 'a')
        C.connect('four', 'q', 'seven', 'b')
        C.connect('four', 'q', 'eight', 'a')
        C.connect('five', 'q', 'ten', 'a')
        C.connect('six', 'q', 'ten', 'b')
        C.connect('eight', 'q', 'eleven', 'a')
        C.connect('nine', 'q', 'eleven', 'b')
        C.connect('eleven', 'q', 'five', 'a')
        F = BooleanExpression("y' * z + w * x * y + w' * x' * y")
        G = BooleanExpression("x' + y' * z")
        H = BooleanExpression("w * x' + y' + z'")
        for w in [False, True]:
            for x in [False, True]:
                for y in [False, True]:
                    for z in [False, True]:
                        C.set_input('one.a', w)
                        C.set_input('five.b', w)
                        C.set_input('one.b', x)
                        C.set_input('eight.b', x)
                        C.set_input('nine.a', x)
                        C.set_input('three.b', y)
                        C.set_input('two.a', y)
                        C.set_input('six.a', y)
                        C.set_input('four.b', z)
                        C.set_input('six.b', z)
                        values = {'w': w, 'x': x, 'y': y, 'z': z}
                        self.assertEqual(C.get_output('seven.q'), F.evaluate(values))
                        self.assertEqual(C.get_output('eleven.q'), G.evaluate(values))
                        self.assertEqual(C.get_output('ten.q'), H.evaluate(values))

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
