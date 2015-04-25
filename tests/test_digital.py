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


    def test_cheby1_N_Wn(self):
        cheby1 = digital.ChebyshevIFilter()
        cheby1.sample_rate = 20000
        cheby1.N = 2
        cheby1.Wn = 200
        cheby1.ripple = 1
        cheby1.filter_kind = 'lowpass'
        cheby1.design()
        target_B_coefs = [937.091145651502e-006, 1.87418229130300e-003, 937.091145651502e-006]
        target_A_coefs = [1, -1.92916981735421e+000, 933.375551589350e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby1.B[idx],
                                   coef, places=4)

        for idx,coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby1.A[idx],
                                   coef, places=4)

        cheby1.N = 2
        cheby1.Wn = 200
        cheby1.ripple = 1
        cheby1.filter_kind = 'highpass'
        cheby1.design()
        target_B_coefs = [863.459699559376e-003, -1.72691939911875e+000, 863.459699559376e-003]
        target_A_coefs = [1, -1.93589973368970e+000, 939.371136116897e-003]
        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby1.B[idx],
                                   coef, places=4)

        for idx,coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby1.A[idx],
                                   coef, places=4)

        cheby1.N = 2
        cheby1.Wn = [100, 200]
        cheby1.ripple = 1
        cheby1.filter_kind = 'bandpass'
        cheby1.design()
        target_B_coefs = [238.315522985134e-006, 0.00000000000000e+000, -476.631045970269e-006,
                          0, 238.315522985134e-006]
        target_A_coefs = [1, -3.96112196901397e+000, 5.88841922559771e+000, -3.89339798541959e+000,
                          966.104557493301e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby1.B[idx],
                                   coef, places=4)

        for idx,coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby1.A[idx],
                                   coef, places=4)

        cheby1.N = 2
        cheby1.Wn = [100, 200]
        cheby1.ripple = 1
        cheby1.filter_kind = 'bandstop'
        cheby1.design()
        target_B_coefs = [877.332031334516e-003, -3.50586484216467e+000, 5.25706903950268e+000,
                           -3.50586484216467e+000, 877.332031334515e-003]
        target_A_coefs = [1, -3.96440852225006e+000, 5.89808779705332e+000,
                          -3.90288157794408e+000, 969.206138023026e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby1.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby1.A[idx],
                                   coef, places=4)



    def test_cheby2_N_Wn(self):
        cheby2 = digital.ChebyshevIIFilter()
        cheby2.sample_rate = 20000
        cheby2.N = 2
        cheby2.Wn = 200
        cheby2.stopband_attenuation = 80
        cheby2.filter_kind = 'lowpass'
        cheby2.design()

        target_B_coefs = [100.134568295967e-006, -199.479544843547e-006, 100.134568295967e-006]
        target_A_coefs = [1.00000000000000e+000, -1.99874301238154e+000, 998.743801973285e-003]
        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby2.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby2.A[idx],
                                   coef, places=4)

        cheby2.sample_rate = 20000
        cheby2.N = 2
        cheby2.Wn = 200
        cheby2.stopband_attenuation = 80
        cheby2.filter_kind = 'highpass'
        cheby2.design()
        target_B_coefs = [110.180226995036e-003, -220.142931172479e-003, 110.180226995036e-003]
        target_A_coefs = [1.00000000000000e+000, 867.362395388384e-003, 307.865780550935e-003]
        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby2.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby2.A[idx],
                                   coef, places=4)


    def test_ellip_N_Wn(self):
        pass


if __name__ == '__main__':
    unittest.main()

