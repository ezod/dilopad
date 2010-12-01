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
from dilo.truth import binary_combinations


class TestExamples(unittest.TestCase):
    def setUp(self):
        pass

    def test_boolean(self):
        result = []
        F = BooleanExpression("((A' + B) * C + C' * D)'")
        for values in binary_combinations(['A', 'B', 'C', 'D']):
            result.append(F.evaluate(values))
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
        C.label_inputs('x', ['one.a', 'three.a'])
        C.label_inputs('y', ['two.b'])
        C.label_inputs('z', ['three.b'])
        C.label_output('F', 'five.q')
        for values in binary_combinations(C.inputs):
            C.apply_inputs(values)
            result.append(C.get_output('F'))
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
        C.label_inputs('w', ['one.a', 'five.b'])
        C.label_inputs('x', ['one.b', 'eight.b', 'nine.a'])
        C.label_inputs('y', ['three.b', 'two.a', 'six.a'])
        C.label_inputs('z', ['four.b', 'six.b'])
        C.label_output('F', 'seven.q')
        C.label_output('G', 'eleven.q')
        C.label_output('H', 'ten.q')
        F = BooleanExpression("y' * z + w * x * y + w' * x' * y")
        G = BooleanExpression("x' + y' * z")
        H = BooleanExpression("w * x' + y' + z'")
        for values in binary_combinations(C.inputs):
            C.apply_inputs(values)
            self.assertEqual(C.get_output('F'), F.evaluate(values))
            self.assertEqual(C.get_output('G'), G.evaluate(values))
            self.assertEqual(C.get_output('H'), H.evaluate(values))

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
