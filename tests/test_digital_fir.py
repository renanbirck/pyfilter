#!/usr/bin/python3
# coding: utf-8
# pyfilter: a Python program for filter synthesis and analysis.
# (c) 2015 Renan Birck <renan.ee.ufsm@gmail.com>

""" This module is a testbench for the DigitalFilter class. """
import unittest
import sys

sys.path.append('../engine')
sys.path.append('..')

from engine import digital

class TestFIR(unittest.TestCase):

    sample_rate = 20000

    def test_FIR1(self):
        fir = digital.FIRFilter()
        fir.sample_rate = self.sample_rate
        fir.N = 3
        fir.Wn = 500
        fir.mode = 1  # numtaps, cutoff -> filter
        fir.design()
        target_B_coefs = [0.0467086576553336, 0.453291342344666,
                          0.453291342344666, 0.0467086576553336]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(fir.B[idx], coef, places=4)

    pass

if __name__ == '__main__':
    unittest.main()
