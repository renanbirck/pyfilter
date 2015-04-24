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

class TestDigital(unittest.TestCase):

    filter_under_test = None
    sample_rate = 20000

    def test_butterworth_N_Wn(self):
        butterworth = digital.ButterworthFilter()
        butterworth.sample_rate = self.sample_rate

        butterworth.N = 2
        butterworth.Wn = 100
        butterworth.filter_kind = "lowpass"
        butterworth.design()

        target_B_coefs = [241.359049041961e-006, 482.718098083923e-006, 241.359049041961e-006]
        target_A_coefs = [1.00000000000000e+000, -1.95557824031504e+000, 956.543676511203e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(butterworth.B[idx],
                                   coef, places=4)

        for idx,coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(butterworth.A[idx],
                                   coef, places=4)

        butterworth.N = 2
        butterworth.Wn = 100
        butterworth.filter_kind = "highpass"
        butterworth.design()

        target_B_coefs = [978.030479206560e-003,
                          -1.95606095841312e+000,
                          978.030479206560e-003]
        target_A_coefs = [1, -1.95557824031504e+000, 956.543676511203e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(butterworth.B[idx],
                                   coef, places=4)

        for idx,coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(butterworth.A[idx],
                                   coef, places=4)

        butterworth.N = 2
        butterworth.Wn = [100, 200]
        butterworth.filter_kind = "bandpass"
        butterworth.design()

        target_B_coefs = [241.359049192824e-006, 0, -482.718098385647e-006,
                          0, 241.359049192824e-006]

        target_A_coefs = [1, -3.95167456215460e+000, 5.85998238324547e+000,
                          -3.86484768746649e+000,  956.543676511207e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(butterworth.B[idx],
                                   coef, places=4)

        for idx,coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(butterworth.A[idx],
                                   coef, places=4)

        butterworth.N = 2
        butterworth.Wn = [100, 200]
        butterworth.filter_kind = "bandstop"
        butterworth.design()

        target_B_coefs = [978.030479148820e-003, -3.90826112457980e+000,
                          5.86046510099756e+000, -3.90826112457980e+000,
                          978.030479148819e-003]
        target_A_coefs = [1.00000000000000e+000, -3.95167456215460e+000,
                          5.85998238324547e+000, -3.86484768746648e+000,
                          956.543676511206e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(butterworth.B[idx],
                                   coef, places=4)

        for idx,coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(butterworth.A[idx],
                                   coef, places=4)


    def test_bessel_N_Wn(self):
        pass

    def test_cheby1_N_Wn(self):
        pass

    def test_cheby2_N_Wn(self):
        pass

    def test_ellip_N_Wn(self):
        pass


if __name__ == '__main__':
    unittest.main()

