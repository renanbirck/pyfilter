#!/usr/bin/python3
# coding: utf-8
# pyfilter: a Python program for filter synthesis and analysis.
# (c) 2015 Renan Birck <renan.ee.ufsm@gmail.com>

import unittest
import sys
from math import pi
import sympy as sym

sys.path.append('../engine')
sys.path.append('..')

from engine import synthesis

class TestSynthesis(unittest.TestCase):
    def setUp(self):
        pass

    def test_vec_to_poly(self):
        vec = [1, 2, 3, 4]
        poly = synthesis.vec_to_polynomial(vec, 's')
        s = sym.var('s')
        self.assertEqual(poly, s**3 + 2*s**2 + 3*s + 4)

        vec = [1, 0, 1]
        poly = synthesis.vec_to_polynomial(vec, 's')
        self.assertEqual(poly, s**2 + 1)

        vec = [-1, 0, 1]
        poly = synthesis.vec_to_polynomial(vec, 'x')
        x = sym.var('x')
        self.assertEqual(poly, -x**2 + 1)


if __name__ == '__main__':
    unittest.main()
