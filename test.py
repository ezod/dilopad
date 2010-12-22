#!/usr/bin/env python

"""\
Unit tests for Dilopad.

@author: Aaron Mavrinac
@contact: mavrinac@gmail.com
@license: GPL-3
"""

import unittest

from dilo.boolean import *
from dilo.device import *
from dilo.truth import *
from dilo.devices.basic import *
from dilo.devices.gates import *


class TestCircuit(unittest.TestCase):
    def setUp(self):
        self.C = Circuit()
        self.C.add('one', Inverter())
        self.C.add('two', ANDGate())
        self.C.add('three', ORGate())
        self.C.add('four', Inverter())
        self.C.add('five', ORGate())
        self.C.connect('one', 'q', 'two', 'a')
        self.C.connect('two', 'q', 'five', 'a')
        self.C.connect('three', 'q', 'four', 'a')
        self.C.connect('four', 'q', 'five', 'b')
        self.C.label_inputs('x', ['one.a', 'three.a'])
        self.C.label_inputs('y', ['two.b'])
        self.C.label_inputs('z', ['three.b'])
        self.C.label_output('F', 'five.q')

    def test_function(self):
        result = []
        for values in binary_combinations(self.C.inputs):
            self.C.apply_inputs(values)
            result.append(self.C.get_output('F'))
        self.assertEqual(result, [True, False, True, True] + [False] * 4)
    
    def test_remove(self):
        self.assertTrue(('two', 'a') in self.C._connections)
        self.assertEqual(self.C.inputs, ['x', 'y', 'z'])
        self.assertEqual(self.C.outputs, ['F'])
        self.C.remove('one')
        self.assertFalse(('two', 'a') in self.C._connections)
        self.assertEqual(self.C.inputs, ['x', 'y', 'z'])
        self.C.remove('three')
        self.assertEqual(self.C.inputs, ['y'])
        self.C.remove('five')
        self.assertEqual(self.C.outputs, ['four.q', 'two.q'])


class TestTruth(unittest.TestCase):
    def setUp(self):
        pass

    def test_binary_combinations(self):
        C = binary_combinations(['x', 'y'])
        for x in [False, True]:
            for y in [False, True]:
                self.assertEqual(next(C), {'x': x, 'y': y})


class TestExamples(unittest.TestCase):
    def setUp(self):
        pass

    def test_boolean(self):
        result = []
        F = BooleanExpression("((A' + B) * C + C' * D)'")
        for values in binary_combinations(['A', 'B', 'C', 'D']):
            result.append(F.evaluate(values))
        self.assertEqual(result, [True, False, False, False, True, False, False, False, True, False, True, True, True, False, False, False])

    def test_combinational_boolean(self):
        C = Circuit()
        C.add('one', XNORGate())
        C.add('two', Inverter())
        C.add('three', ANDGate())
        C.add('four', ANDGate())
        C.add('five', ANDGate())
        C.add('six', NANDGate())
        C.add('seven', ORGate())
        C.add('eight', ANDGate())
        C.add('nine', Inverter())
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
