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

        cheby2.sample_rate = 20000
        cheby2.N = 2
        cheby2.Wn = [100, 200]
        cheby2.stopband_attenuation = 80
        cheby2.filter_kind = 'bandpass'
        cheby2.design()

        target_B_coefs = [100.017928631756e-006, -399.479724271789e-006,
                          598.923980729970e-006, -399.479724271789e-006,
                          100.017928631756e-006]
        target_A_coefs = [1.00000000000000e+000, -3.99542476423799e+000,
                          5.99022652135467e+000, -3.99416972119781e+000,
                          999.371858580165e-003]
        for idx, coef in enumerate(target_B_coefs):
             self.assertAlmostEqual(cheby2.B[idx],
                                    coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
             self.assertAlmostEqual(cheby2.A[idx],
                                    coef, places=4)

        cheby2.sample_rate = 20000
        cheby2.N = 2
        cheby2.Wn = [100, 200]
        cheby2.stopband_attenuation = 80
        cheby2.filter_kind = 'bandstop'
        cheby2.design()

        target_B_coefs = [262.861754223389e-003, -1.05027977124056e+000,
                          1.57483705794453e+000, -1.05027977124056e+000,
                          262.861754223389e-003]
        target_A_coefs = [1.00000000000000e+000, -1.87519417681152e+000,
                          926.289867090544e-003, -225.365365669609e-003,
                          174.270699300762e-003]

        for idx, coef in enumerate(target_B_coefs):
             self.assertAlmostEqual(cheby2.B[idx],
                                    coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
             self.assertAlmostEqual(cheby2.A[idx],
                                    coef, places=4)


    def test_ellip_N_Wn(self):
        ellip = digital.EllipticalFilter()
        ellip.sample_rate = 20000
        ellip.N = 2
        ellip.Wn = 200
        ellip.ripple = 1
        ellip.stopband_attenuation = 80
        ellip.filter_kind = 'lowpass'
        ellip.design()

        target_B_coefs = [1.03370433556178e-003, 1.68115343291991e-003, 1.03370433556178e-003]
        target_A_coefs = [1.00000000000000e+000, -1.92917321288040e+000, 933.379168738236e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(ellip.B[idx],
                                    coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
             self.assertAlmostEqual(ellip.A[idx],
                                    coef, places=4)

        ellip.sample_rate = 50000
        ellip.N = 2
        ellip.Wn = 200
        ellip.ripple = 1
        ellip.stopband_attenuation = 80
        ellip.filter_kind = 'highpass'
        ellip.design()

        target_B_coefs = [880.113561737520e-003, -1.76022706689550e+000, 880.113561737520e-003]
        target_A_coefs = [1.00000000000000e+000, -1.97472438687787e+000, 975.290182242553e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(ellip.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(ellip.A[idx],
                                   coef, places=4)

        ellip.sample_rate = 50000
        ellip.N = 2
        ellip.Wn = [100, 200]
        ellip.ripple = 1
        ellip.stopband_attenuation = 80
        ellip.filter_kind = 'bandpass'
        ellip.design()
        target_B_coefs = [137.838348358635e-006, -397.180205908006e-006,
                          518.683725004420e-006, -397.180205908006e-006,
                          137.838348358635e-006]
        target_A_coefs = [1.00000000000000e+000, -3.98549876240398e+000,
                          5.95730308332100e+000, -3.95810535489672e+000,
                          986.301133036477e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(ellip.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(ellip.A[idx],
                                   coef, places=4)

        ellip.sample_rate = 50000
        ellip.N = 2
        ellip.Wn = [100, 200]
        ellip.ripple = 1
        ellip.stopband_attenuation = 80
        ellip.filter_kind = 'bandstop'
        ellip.design()

        target_B_coefs = [885.678969784819e-003, -3.54215642900254e+000,
                          5.31295500677686e+000, -3.54215642900255e+000,
                          885.678969784823e-003]
        target_A_coefs = [1.00000000000000e+000, -3.98679546270721e+000,
                          5.96116240643601e+000, -3.96193430002317e+000,
                          987.567455415066e-003]
        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(ellip.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(ellip.A[idx],
                                   coef, places=4)


    def test_compute_cheb1_lp(self):
        parameters = {'passband_frequency': 10,
                      'stopband_frequency': 100,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        cheby1 = digital.ChebyshevIFilter(parameters)
        cheby1.sample_rate = 500
        cheby1.compute_parameters()

        self.assertEqual(cheby1.N, 4)
        self.assertAlmostEqual(cheby1.Wn, 0.04)
        cheby1.ripple = 1

        cheby1.design()
        target_B_coefs = [3.61092006543050e-006, 14.4436802617220e-006,
                          21.6655203925830e-006, 14.4436802617220e-006,
                          3.61092006543050e-006]
        target_A_coefs = [1.00000000000000e+000, -3.86484928162257e+000,
                          5.61832412411045e+000, -3.64058272249581e+000,
                          887.172704311142e-003]

        for idx, coef in enumerate(target_B_coefs):
             self.assertAlmostEqual(cheby1.B[idx],
                                    coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
             self.assertAlmostEqual(cheby1.A[idx],
                                    coef, places=4)

    def test_compute_cheb1_hp(self):
        parameters = {'passband_frequency': 100,
                      'stopband_frequency': 10,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        cheby1 = digital.ChebyshevIFilter(parameters)
        cheby1.sample_rate = 500
        cheby1.compute_parameters()

        self.assertEqual(cheby1.N, 4)
        self.assertAlmostEqual(cheby1.Wn, 0.4)
        cheby1.ripple = 1
        cheby1.design()

        target_B_coefs = [0.110321442810114, -0.441285771240457,
                          0.661928656860685, -0.441285771240457,
                          0.110321442810114]
        target_A_coefs = [1.00000000000000e+000, -150.986050190449e-003,
                          804.174213117362e-003, 161.810537814229e-003,
                          187.173390317085e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby1.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby1.A[idx],
                                   coef, places=4)

    def test_compute_cheb1_bp(self):
        parameters = {'passband_frequency': [1, 2],
                      'stopband_frequency': [0.1, 5],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        cheby1 = digital.ChebyshevIFilter(parameters)
        cheby1.ripple = 1
        cheby1.sample_rate = 50
        cheby1.compute_parameters()

        self.assertEqual(cheby1.N, 5)
        self.assertAlmostEqual(cheby1.Wn[0], 0.04)
        self.assertAlmostEqual(cheby1.Wn[1], 0.08)
        cheby1.design()

        target_B_coefs = [113.590739945972e-009, 0.00000000000000e+000,
                          -567.953699729860e-009, 0.00000000000000e+000,
                          1.13590739945972e-006, 0.00000000000000e+000,
                          -1.13590739945972e-006, 0.00000000000000e+000,
                          567.953699729860e-009]
        target_A_coefs = [1.00000000000000e+000, -9.70734068372584e+000,
                          42.5757352105897e+000, -111.100142776047e+000,
                          191.012009578846e+000, -226.083311697567e+000,
                          186.565335560800e+000, -105.987935461550e+000,
                          39.6714495427978e+000]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby1.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby1.A[idx],
                                   coef, places=4)

    def test_compute_cheb1_bs(self):
        parameters = {'passband_frequency': [10, 70],
                      'stopband_frequency': [20, 60],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        cheby1 = digital.ChebyshevIFilter(parameters)
        cheby1.ripple = 1
        cheby1.sample_rate = 500
        cheby1.compute_parameters()
        self.assertEqual(cheby1.N, 13)
        self.assertAlmostEqual(cheby1.Wn[0], 0.04)
        self.assertAlmostEqual(cheby1.Wn[1], 0.28)
        cheby1.design()

        target_B_coefs = [8.74608886e-03, -2.14321035e-01, 2.53764887e+00,
                          -1.93252385e+01, 1.06295284e+02, -4.49552843e+02,
                          1.51961565e+03, -4.21310899e+03, 9.75526990e+03,
                          -1.91101874e+04, 3.19684412e+04, -4.59684673e+04,
                          5.70662222e+04, -6.13150691e+04, 5.70662222e+04,
                          -4.59684673e+04, 3.19684412e+04, -1.91101874e+04,
                          9.75526990e+03, -4.21310899e+03, 1.51961565e+03,
                          -4.49552843e+02, 1.06295284e+02, -1.93252385e+01,
                          2.53764887e+00, -2.14321035e-01, 8.74608886e-03]

        target_A_coefs = [1.00000000e+00, -1.60685557e+01, 1.24950495e+02,
                          -6.26706028e+02, 2.27918097e+03, -6.40332860e+03,
                          1.44540254e+04, -2.69088299e+04, 4.20737837e+04,
                          -5.59585058e+04, 6.38544401e+04, -6.28218874e+04,
                          5.33222598e+04, -3.88186873e+04, 2.37827848e+04,
                          -1.16198786e+04, 3.71545958e+03, 2.82229442e+02,
                          -1.59246199e+03, 1.51008040e+03, -9.76631282e+02,
                          4.86536598e+02, -1.89706382e+02, 5.65717590e+01,
                          -1.21903894e+01, 1.69279910e+00, -1.13719952e-01]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby1.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby1.A[idx],
                                   coef, places=4)

    def test_compute_butter_lp(self):
        parameters = {'passband_frequency': 10,
                      'stopband_frequency': 100,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        butter = digital.ButterworthFilter(parameters)
        butter.sample_rate = 500

        butter.target = 'stopband'
        butter.compute_parameters()
        butter.design()
        self.assertEqual(butter.N, 5)
        self.assertAlmostEqual(butter.Wn, 72.9848327762502e-003)

        target_B_coefs = [13.9554935029984e-006, 69.7774675149920e-006,
                          139.554935029984e-006, 139.554935029984e-006,
                          69.7774675149920e-006, 13.9554935029984e-006]

        target_A_coefs = [1.00000000000000e+000, -4.25847314441103e+000,
                          7.30143280938040e+000, -6.29570509456441e+000,
                          2.72839589436988e+000, -475.203888982748e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(butter.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(butter.A[idx],
                                   coef, places=4)

        butter.target = 'passband'
        butter.compute_parameters()
        self.assertEqual(butter.N, 5)
        self.assertAlmostEqual(butter.Wn, 0.045768368162850868)
        butter.design()

        target_B_coefs = [1.53470825990307e-006, 7.67354129951534e-006,
                          15.3470825990307e-006, 15.3470825990307e-006,
                          7.67354129951534e-006, 1.53470825990307e-006]
        target_A_coefs = [1.00000000000000e+000, -4.53481633767399e+000,
                          8.24563188183775e+000, -7.51327290057926e+000,
                          3.43014167292325e+000, -627.635205843430e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(butter.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(butter.A[idx],
                                   coef, places=4)


    def test_compute_butter_hp(self):
        parameters = {'passband_frequency': 100,
                      'stopband_frequency': 10,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        butter = digital.ButterworthFilter(parameters)
        butter.sample_rate = 500

        butter.target = 'stopband'
        butter.compute_parameters()
        self.assertEqual(butter.N, 5)
        self.assertAlmostEqual(butter.Wn, 240.570345569637e-003)
        butter.design()

        target_B_coefs = [283.489972641606e-003, -1.41744986320803e+000,
                          2.83489972641606e+000, -2.83489972641606e+000,
                          1.41744986320803e+000, -283.489972641606e-003]

        target_A_coefs = [1.00000000000000e+000, -2.56870920176411e+000,
                          2.98322539177564e+000, -1.84206031464644e+000,
                          597.325460739181e-003, -80.3587556060112e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(butter.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(butter.A[idx],
                                   coef, places=4)

        butter.target = 'passband'
        butter.compute_parameters()
        butter.design()
        self.assertEqual(butter.N, 5)
        self.assertAlmostEqual(butter.Wn, 0.36004326343144744)

        target_B_coefs = [140.242720840311e-003, -701.213604201556e-003,
                          1.40242720840311e+000, -1.40242720840311e+000,
                          701.213604201556e-003, -140.242720840311e-003]
        target_A_coefs = [1.00000000000000e+000, -1.38023900721199e+000,
                          1.30312415600401e+000, -613.035772803709e-003,
                          171.908821314534e-003, -19.4593095557128e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(butter.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(butter.A[idx],
                                   coef, places=4)

    def test_compute_butter_bp(self):
        parameters = {'passband_frequency': [1, 2],
                      'stopband_frequency': [0.1, 5],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        butter = digital.ButterworthFilter(parameters)
        butter.sample_rate = 50

        butter.target = 'stopband'
        butter.compute_parameters()
        butter.design()
        self.assertEqual(butter.N, 7)
        self.assertAlmostEqual(butter.Wn[0], 36.5880780276322e-003)
        self.assertAlmostEqual(butter.Wn[1], 87.3893423777441e-003)
        target_B_coefs = [14.3375327927349e-009, 0.00000000000000e+000,
                          -100.362729549144e-009, 0.00000000000000e+000,
                          301.088188647432e-009, 0.00000000000000e+000,
                          -501.813647745721e-009, 0.00000000000000e+000,
                          501.813647745721e-009, 0.00000000000000e+000,
                          -301.088188647432e-009, 0.00000000000000e+000,
                          100.362729549144e-009, 0.00000000000000e+000,
                          -14.3375327927349e-009]
        target_A_coefs = [1.00000000000000e+000, -13.0734060396007e+000,
                          79.5641515407404e+000, -298.774051509031e+000,
                          773.370588276682e+000, -1.45973447099227e+003,
                          2.07187696283509e+003, -2.24645044945352e+003,
                          1.86977093042128e+003, -1.18884359044868e+003,
                          568.419441368658e+000, -198.180399595484e+000,
                          47.6299635654552e+000, -7.06329781991096e+000,
                          487.627850612888e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(butter.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(butter.A[idx],
                                   coef, places=4)


        butter.target = 'passband'
        butter.compute_parameters()
        butter.design()
        self.assertEqual(butter.N, 7)
        self.assertAlmostEqual(butter.Wn[0], 0.038675590426020465)
        self.assertAlmostEqual(butter.Wn[1], 0.082716323618103132)

        target_B_coefs = [5.21183518025846e-009, 0.00000000000000e+000,
                          -36.4828462618092e-009, 0.00000000000000e+000,
                          109.448538785428e-009, 0.00000000000000e+000,
                          -182.414231309046e-009, 0.00000000000000e+000,
                          182.414231309046e-009, 0.00000000000000e+000,
                          -109.448538785428e-009, 0.00000000000000e+000,
                          36.4828462618092e-009, 0.00000000000000e+000,
                          -5.21183518025846e-009]
        target_A_coefs = [1.00000000000000e+00,  -1.31673106824993e+01,
                          8.07078725006832e+01,  -3.05219413464552e+02,
                          7.95623289716231e+02,  -1.51224871120647e+03,
                          2.16133044191775e+03,  -2.35960723130886e+03,
                          1.97739925345442e+03,  -1.26581693976280e+03,
                          6.09301525711200e+02,  -2.13854323618345e+02,
                          5.17378511442546e+01,  -7.72295169986461e+00,
                          5.36647298877683e-01]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(butter.B[idx],
                                   coef, places=2)


        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(butter.A[idx],
                                   coef, places=1)


    def test_compute_butter_bs(self):

        parameters = {'passband_frequency': [1, 7],
                      'stopband_frequency': [2, 6],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 5}

        butter = digital.ButterworthFilter(parameters)
        butter.sample_rate = 50
        butter.target = 'stopband'
        butter.compute_parameters()
        butter.design()

        self.assertEqual(butter.N, 4)
        self.assertAlmostEqual(butter.Wn[0], 0.076018239965718007)
        self.assertAlmostEqual(butter.Wn[1], 0.25143968885666007)

        target_B_coefs = [481.405830693621e-003, -3.48435290477535e+000,
                          11.3828585629904e+000, -21.8614321972257e+000,
                          26.9636758517415e+000, -21.8614321972257e+000,
                          11.3828585629904e+000, -3.48435290477535e+000,
                          481.405830693621e-003]
        target_A_coefs = [1.00000000000000e+000, -5.94212484129793e+000,
                          15.9489891635285e+000, -25.2696110239082e+000,
                          25.8589005881025e+000, -17.5022117616133e+000,
                          7.65255384709579e+000, -1.97762257668612e+000,
                          231.761039886462e-003]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(butter.B[idx],
                                   coef, places=2)


        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(butter.A[idx],
                                   coef, places=1)

    def test_compute_cheb2_lp(self):
        parameters = {'passband_frequency': 10,
                      'stopband_frequency': 100,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        cheby2 = digital.ChebyshevIIFilter(parameters)
        cheby2.sample_rate = 500
        cheby2.stopband_attenuation = 80
        cheby2.compute_parameters()

        self.assertEqual(cheby2.N, 4)
        self.assertAlmostEqual(cheby2.Wn, 0.26663100739645568)
        cheby2.design()

        target_B_coefs = [ 0.0002386 , -0.00022575,  0.00038794, -0.00022575,  0.0002386 ]
        target_A_coefs = [ 1.        , -3.61074947,  4.90624573, -2.97224795,  0.67716533]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby2.B[idx],
                                   coef, places=2)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby2.A[idx],
                                   coef, places=1)

    def test_compute_cheb2_hp(self):
        parameters = {'passband_frequency': 100,
                      'stopband_frequency': 10,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        cheby2 = digital.ChebyshevIIFilter(parameters)
        cheby2.sample_rate = 500
        cheby2.stopband_attenuation = 80
        cheby2.compute_parameters()

        self.assertEqual(cheby2.N, 4)
        self.assertEqual(cheby2.Wn, 0.065141234256020891)
        cheby2.design()

        target_B_coefs = [ 0.22057452, -0.87306839,  1.30503626, -0.87306839,  0.22057452]
        target_A_coefs = [ 1.        , -1.18443635,  0.93923523, -0.31907741,  0.04957309]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby2.B[idx],
                                   coef, places=2)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby2.A[idx],
                                   coef, places=1)

    def test_compute_cheb2_bp(self):
        parameters = {'passband_frequency': [1, 2],
                      'stopband_frequency': [0.1, 5],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        cheby2 = digital.ChebyshevIIFilter(parameters)
        cheby2.sample_rate = 50
        cheby2.compute_parameters()
        cheby2.design()

        self.assertEqual(cheby2.N, 5)
        self.assertListEqual(list(cheby2.Wn), [ 0.017210851459767147, 0.181989819725220547])

        target_B_coefs = [ 0.000135712, -0.000940014,  0.002824547, -0.004612154,
                           0.003832163,  0.         , -0.003832163,  0.004612154,
                           -0.002824547,  0.000940014, -0.000135712]

        target_A_coefs = [   1.         ,   -9.38111324 ,   39.753041358, -100.203106884,
                          166.376914952, -190.14129197 ,  151.469644676,  -83.051931955,
                            29.997294982,   -6.444965683,    0.62551379]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby2.B[idx],
                                   coef, places=2)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby2.A[idx],
                                   coef, places=1)


    def test_compute_cheb2_bs(self):
        parameters = {'passband_frequency': [1, 7],
                      'stopband_frequency': [2, 6],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 5}

        cheby2 = digital.ChebyshevIIFilter(parameters)
        cheby2.sample_rate = 50
        cheby2.compute_parameters()
        cheby2.design()

        self.assertEqual(cheby2.N, 3)
        self.assertAlmostEqual(cheby2.Wn[0], 0.074014128)
        self.assertAlmostEqual(cheby2.Wn[1], 0.257595349)

        target_B_coefs = [  0.793616223,  -4.130260046,   9.497020267, -12.315603367,
                            9.497020267,  -4.130260046,   0.793616223]
        target_A_coefs = [  1.         ,  -4.812806141,  10.21498456 , -12.238622803,
                            8.736512745,  -3.524694514,   0.629775676]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby2.B[idx],
                                   coef, places=2)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby2.A[idx],
                                   coef, places=1)

    def test_compute_elliptical_lp(self):
        parameters = {'passband_frequency': 10,
                      'stopband_frequency': 100,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        ellip = digital.EllipticalFilter(parameters)
        ellip.sample_rate = 500
        ellip.ripple = 1
        ellip.stopband_attenuation = 80
        ellip.compute_parameters()

        self.assertEqual(ellip.N, 3)
        self.assertAlmostEqual(ellip.Wn, 0.04)

        ellip.design()

        target_B_coefs = [ 0.00030465 ,  0.000155439,  0.000155439,  0.00030465 ]
        target_A_coefs = [ 1.         , -2.864462665,  2.74868316 , -0.883300318]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(ellip.B[idx],
                                   coef, places=2)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(ellip.A[idx],
                                   coef, places=1)

    def test_compute_elliptical_hp(self):
        parameters = {'passband_frequency': 100,
                      'stopband_frequency': 10,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        ellip = digital.EllipticalFilter(parameters)
        ellip.sample_rate = 500
        ellip.ripple = 1
        ellip.stopband_attenuation = 80
        ellip.compute_parameters()

        self.assertEqual(ellip.N, 3)
        self.assertAlmostEqual(ellip.Wn, 0.4)
        ellip.design()
        target_B_coefs = [ 0.215250183, -0.642794874,  0.642794874, -0.215250183]
        target_A_coefs = [ 1.         , -0.307552733,  0.525670317,  0.117132936]


        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(ellip.B[idx],
                                   coef, places=2)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(ellip.A[idx],
                                   coef, places=1)

    def test_compute_elliptical_bp(self):

        parameters = {'passband_frequency': [1, 2],
                      'stopband_frequency': [0.1, 5],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        ellip = digital.EllipticalFilter(parameters)
        ellip.sample_rate = 50
        ellip.ripple = 1
        ellip.stopband_attenuation = 80
        ellip.compute_parameters()
        self.assertEqual(ellip.N, 4)
        self.assertAlmostEqual(ellip.Wn[0], 0.04)
        self.assertAlmostEqual(ellip.Wn[1], 0.08)
        ellip.design()
        target_B_coefs = [ 0.000149968, -0.000945145,  0.002744802,
                           -0.004872166, 0.005845081, -0.004872166,
                           0.002744802, -0.000945145,  0.000149968]

        target_A_coefs = [ 1.         ,  -7.740894095, 26.351978106,
                          -51.526073594, 63.290406212, -50.008340755,
                          24.822582584,  -7.077002512, 0.887344983]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(ellip.B[idx],
                                   coef, places=2)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(ellip.A[idx],
                                   coef, places=1)

    def test_compute_elliptical_bs(self):
        parameters = {'passband_frequency': [1, 7],
                      'stopband_frequency': [2, 6],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 5}
        ellip = digital.EllipticalFilter(parameters)
        ellip.sample_rate = 50
        ellip.ripple = 1
        ellip.stopband_attenuation = 80
        ellip.compute_parameters()
        ellip.design()

        self.assertEqual(ellip.N, 2)
        self.assertAlmostEqual(ellip.Wn[0], 0.0674131)
        self.assertAlmostEqual(ellip.Wn[1], 0.27999758)
        target_B_coefs = [ 0.612746909, -2.217463339,  3.231677071,
                           -2.217463339,  0.612746909]
        target_A_coefs = [ 1.         , -2.917691877,  3.475927094,
                           -2.058377701,  0.525100898]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(ellip.B[idx],
                                   coef, places=2)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(ellip.A[idx],
                                   coef, places=1)


if __name__ == '__main__':
    unittest.main()

