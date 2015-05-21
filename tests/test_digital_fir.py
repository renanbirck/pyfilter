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

    sample_rate = 2000
    taps = 10
    freqs = [0, 300, 600]
    gains = [0, 1, 1]
    window = 'boxcar'

    def test_get_filter_type(self):

        taps = 3
        fir = digital.FIRFilter(self.sample_rate, taps,
                                self.freqs, self.gains,
                                self.window, antisymmetric=False)
        self.assertEqual(fir.get_filter_type(), 1)

        fir.taps = 4
        self.assertEqual(fir.get_filter_type(), 2)

        fir.taps = 5
        fir.antisymmetric = True

        self.assertEqual(fir.get_filter_type(), 3)

        fir.taps = 6
        self.assertEqual(fir.get_filter_type(), 4)

    def test_firwin2_type1(self):
        fir = digital.FIRFilter(self.sample_rate, 9,
                                self.freqs, self.gains,
                                self.window)
        fir.design()
        target_B_coefs = [-0.05120328, -0.02293234, -0.22677772,
                          0.03562499,  0.64778646, 0.03562499,
                          -0.22677772, -0.02293234, -0.05120328]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(fir.B[idx], coef, places=3)


    def test_firwin2_type2(self):
        fir = digital.FIRFilter(self.sample_rate, self.taps,
                                self.freqs, self.gains,
                                self.window)
        fir.design()
        target_B_coefs = [-0.03241918, -0.0366439, -0.093414,
                          -0.23450071,  0.44703339, 0.44703339,
                          -0.23450071, -0.093414, -0.0366439,
                          -0.03241918]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(fir.B[idx], coef, places=3)



if __name__ == '__main__':
    unittest.main()
