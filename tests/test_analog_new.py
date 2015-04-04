#!/usr/bin/python3
# coding: utf-8
# pyfilter: a Python program for filter synthesis and analysis.
# (c) 2015 Renan Birck <renan.ee.ufsm@gmail.com>

""" This module is a testbench for the new AnalogFilter class,
    which is done in a much more OO way. """

import unittest
import sys
from math import pi

sys.path.append('../engine')
sys.path.append('..')

from engine import analog_new as analog

class TestAnalog(unittest.TestCase):
    filter_under_test = None

    def setUp(self):
        self.filter_under_test = analog.AnalogFilter()

    def test_pass_initial_parameters(self):
        """ Try passing initial parameters and convert all the
            frequencies to Hz. """
        parameters = {'passband_frequency': 1,
                      'stopband_frequency': 10,
                      'passband_attenuation': 0,
                      'stopband_attenuation': 80,
                      'ripple': 0.01}

        temp_filter = analog.AnalogFilter(parameters)
        self.assertEqual(temp_filter.filter_parameters['passband_frequency'], 2 * pi * 1)
        self.assertEqual(temp_filter.filter_parameters['stopband_frequency'], 2 * pi * 10)
        self.assertEqual(temp_filter.filter_parameters['passband_attenuation'], 0)
        self.assertEqual(temp_filter.filter_parameters['stopband_attenuation'], 80)
        self.assertEqual(temp_filter.filter_parameters['ripple'], 0.01)

    def test_get_filter_kind(self):
        """ This checks that we can find the filter type from the parameters. """
        parameters = {'passband_frequency': 1,
                      'stopband_frequency': 10,
                      'passband_attenuation': 0,
                      'stopband_attenuation': 80,
                      'ripple': 0.01}
        self.filter_under_test.set_parameters(parameters)
        self.assertEqual(self.filter_under_test.filter_kind, "lowpass")

        parameters = {'passband_frequency': 10,
                      'stopband_frequency': 1,
                      'passband_attenuation': 0,
                      'stopband_attenuation': 80,
                      'ripple': 0.01}

        self.filter_under_test.set_parameters(parameters)
        self.assertEqual(self.filter_under_test.filter_kind, "highpass")

        parameters['passband_frequency'] = [2, 5]
        parameters['stopband_frequency'] = [1, 6]

        self.filter_under_test.set_parameters(parameters)
        self.assertEqual(self.filter_under_test.filter_kind, "bandpass")

        parameters['passband_frequency'] = [1, 6]
        parameters['stopband_frequency'] = [2, 5]

        self.filter_under_test.set_parameters(parameters)
        self.assertEqual(self.filter_under_test.filter_kind, "bandstop")

        # Meaningless combination should fail.

        parameters['passband_frequency'] = [6, 1]
        parameters['stopband_frequency'] = [6, 6]

        with self.assertRaises(ValueError):
            self.filter_under_test.set_parameters(parameters)

        # Try giving invalid parameters.

        with self.assertRaises(ValueError):
            for invalid in [-1, "this is invalid!", '1']:
                parameters['passband_frequency'] = invalid
                self.filter_under_test.set_parameters(parameters)

    # Those try synthesizing directly from N, Wn.

    def test_butterworth_N_Wn(self):
        butterworth = analog.ButterworthFilter()
        butterworth.N = 2
        butterworth.Wn = 100 # 100 rad/s
        butterworth.filter_kind = "lowpass"
        butterworth.design()

        self.assertEqual(list(butterworth.Z), [])
        self.assertListEqual(list(butterworth.P), [-70.710678118654755+70.710678118654741j,
                                                   -70.710678118654755-70.710678118654741j])
        self.assertEqual(butterworth.K, 10000)
        self.assertListEqual(list(butterworth.B), [10000])
        self.assertAlmostEqual(butterworth.A[0], 1)
        self.assertAlmostEqual(butterworth.A[1], 141.42135623730951)
        self.assertAlmostEqual(butterworth.A[2], 10000)

        ### Highpass test
        butterworth.filter_kind = "highpass"
        butterworth.design()
        self.assertListEqual(list(butterworth.Z), [0, 0])
        self.assertListEqual(list(butterworth.P), [-70.71067811865476-70.71067811865474j,
                                                   -70.71067811865476+70.71067811865474j])
        self.assertEqual(butterworth.K, 1)
        self.assertListEqual(list(butterworth.B), [1, 0, 0])
        self.assertAlmostEqual(butterworth.A[0], 1)
        self.assertAlmostEqual(butterworth.A[1], 141.42135623730951)
        self.assertAlmostEqual(butterworth.A[2], 10000)

        ### Bandpass test
        butterworth.N = 1
        butterworth.Wn = [100, 200]
        butterworth.filter_kind = "bandpass"
        butterworth.design()
        self.assertEqual(butterworth.Z, 0)
        self.assertAlmostEqual(butterworth.P[0], -50 - 132.28756555323j)
        self.assertAlmostEqual(butterworth.P[1], -50 + 132.28756555323j)
        self.assertAlmostEqual(butterworth.K, 100)
        self.assertAlmostEqual(butterworth.B[0], 100)
        self.assertAlmostEqual(butterworth.B[1], 0)
        self.assertAlmostEqual(butterworth.A[0], 1)
        self.assertAlmostEqual(butterworth.A[1], 100)
        self.assertAlmostEqual(butterworth.A[2], 20000)

        ### Bandstop test
        butterworth.N = 1
        butterworth.Wn = [100, 200]
        butterworth.filter_kind = "bandstop"
        butterworth.design()
        self.assertAlmostEqual(butterworth.Z[0], +141.42135623731j)
        self.assertAlmostEqual(butterworth.Z[1], -141.42135623731j)
        self.assertAlmostEqual(butterworth.P[0], -50 + 132.28756555323j)
        self.assertAlmostEqual(butterworth.P[1], -50 - 132.28756555323j)
        self.assertAlmostEqual(butterworth.K, 1)
        self.assertAlmostEqual(butterworth.B[0], 1)
        self.assertAlmostEqual(butterworth.B[1], 0)
        self.assertAlmostEqual(butterworth.B[2], 20000)
        self.assertAlmostEqual(butterworth.A[0], 1)
        self.assertAlmostEqual(butterworth.A[1], 100)
        self.assertAlmostEqual(butterworth.A[2], 20000)

    def test_bessel_N_Wn(self):
        bessel = analog.BesselFilter()
        bessel.N = 2
        bessel.Wn = 100 # 100 rad/s
        bessel.filter_kind = "lowpass"
        bessel.design()
        self.assertEqual(list(bessel.Z), [])
        self.assertAlmostEqual(bessel.P[0], -86.60254038+50j)
        self.assertAlmostEqual(bessel.P[1], -86.60254038-50j)
        self.assertAlmostEqual(bessel.K, 10000)
        self.assertAlmostEqual(bessel.B[0], 10000)
        self.assertAlmostEqual(bessel.A[0], 1)
        self.assertAlmostEqual(bessel.A[1], 173.20508075688772)
        self.assertAlmostEqual(bessel.A[2], 1.00000000e+04)

        bessel.filter_kind = "highpass"
        bessel.design()

        self.assertEqual(list(bessel.Z), [0, 0])
        self.assertAlmostEqual(bessel.P[0], -86.60254038-50j)
        self.assertAlmostEqual(bessel.P[1], -86.60254038+50j)
        self.assertAlmostEqual(bessel.K, 1)
        self.assertAlmostEqual(bessel.B[0], 1)
        self.assertAlmostEqual(bessel.A[0], 1)
        self.assertAlmostEqual(bessel.A[1], 173.20508075688772)
        self.assertAlmostEqual(bessel.A[2], 1.00000000e+04)

        bessel.N = 1
        bessel.Wn = [100, 200]
        bessel.filter_kind = "bandpass"
        bessel.design()

        self.assertEqual(list(bessel.Z), [0])
        self.assertAlmostEqual(bessel.P[0], -50.-132.28756555j)
        self.assertAlmostEqual(bessel.P[1], -50.+132.28756555j)
        self.assertAlmostEqual(bessel.K, 100)
        self.assertAlmostEqual(bessel.B[0], 100)
        self.assertAlmostEqual(bessel.B[1], 0)
        self.assertAlmostEqual(bessel.A[0], 1)
        self.assertAlmostEqual(bessel.A[1], 100)
        self.assertAlmostEqual(bessel.A[2], 20000)

        bessel.N = 1
        bessel.Wn = [100, 200]
        bessel.filter_kind = "bandstop"
        bessel.design()

        self.assertAlmostEqual(bessel.Z[0], 0.+141.42135624j)
        self.assertAlmostEqual(bessel.Z[1], 0.-141.42135624j)
        self.assertAlmostEqual(bessel.P[0], -50.-132.28756555j)
        self.assertAlmostEqual(bessel.P[1], -50.+132.28756555j)
        self.assertAlmostEqual(bessel.K, 1)
        self.assertAlmostEqual(bessel.B[0], 1)
        self.assertAlmostEqual(bessel.B[1], 0)
        self.assertAlmostEqual(bessel.B[2], 20000)
        self.assertAlmostEqual(bessel.A[0], 1)
        self.assertAlmostEqual(bessel.A[1], 100)
        self.assertAlmostEqual(bessel.A[2], 20000)

    def test_cheby1_N_Wn(self):

        cheby1 = analog.ChebyshevIFilter()
        cheby1.N = 2
        cheby1.Wn = 100 # 100 rad/s
        cheby1.ripple = 0.01
        cheby1.filter_kind = "lowpass"
        cheby1.design()

        self.assertAlmostEqual(list(cheby1.Z), [])
        self.assertAlmostEqual(cheby1.P[0], -222.776405361899 + 233.729174015502j)
        self.assertAlmostEqual(cheby1.P[1], -222.776405361899 - 233.729174015502j)
        self.assertAlmostEqual(cheby1.K, 104138.690430759)
        self.assertAlmostEqual(cheby1.B[0], 104138.690430759)
        self.assertAlmostEqual(cheby1.A[0], 1)
        self.assertAlmostEqual(cheby1.A[1], 445.552810723798)
        self.assertAlmostEqual(cheby1.A[2], 104258.653571938)

        cheby1.N = 2
        cheby1.Wn = 100 # 100 rad/s
        cheby1.ripple = 1
        cheby1.filter_kind = "highpass"
        cheby1.design()

        self.assertEqual(list(cheby1.Z), [0, 0])
        self.assertAlmostEqual(cheby1.P[0], -49.7834034127213 - 81.190039788561j)
        self.assertAlmostEqual(cheby1.P[1], -49.7834034127213 + 81.190039788561j)
        self.assertAlmostEqual(cheby1.K, 0.891250938133745)
        self.assertAlmostEqual(cheby1.B[0], 0.891250938133745)
        self.assertAlmostEqual(cheby1.A[0], 1)
        self.assertAlmostEqual(cheby1.A[1], 99.5668068254425)
        self.assertAlmostEqual(cheby1.A[2], 9070.20981622186)

        cheby1.N = 1
        cheby1.Wn = [100, 200]
        cheby1.ripple = 0.01
        cheby1.filter_kind = "bandpass"
        cheby1.design()

        self.assertEqual(cheby1.Z[0], 0)
        self.assertAlmostEqual(cheby1.P[0], -9.64726444521389)
        self.assertAlmostEqual(cheby1.P[1], -2073.12654416996)
        self.assertAlmostEqual(cheby1.K, 2082.77380861517)
        self.assertAlmostEqual(cheby1.B[0], 2082.77380861517)
        self.assertAlmostEqual(cheby1.B[1], 0)
        self.assertAlmostEqual(cheby1.A[0], 1)
        self.assertAlmostEqual(cheby1.A[1], 2082.77380861517)
        self.assertAlmostEqual(cheby1.A[2], 20000)

        cheby1.filter_kind = "bandstop"
        cheby1.design()
        self.assertAlmostEqual(cheby1.Z[0], 141.42135623731j)
        self.assertAlmostEqual(cheby1.Z[1], -141.42135623731j)
        self.assertAlmostEqual(cheby1.P[0], -2.40064474563586 +      141.400979150801j)
        self.assertAlmostEqual(cheby1.P[1], -2.40064474563586 -      141.400979150801j)
        self.assertAlmostEqual(cheby1.K, 1)

        self.assertAlmostEqual(cheby1.B[0], 1)
        self.assertAlmostEqual(cheby1.B[1], 0)
        self.assertAlmostEqual(cheby1.B[2], 20000)
        self.assertAlmostEqual(cheby1.A[0], 1)
        self.assertAlmostEqual(cheby1.A[1], 4.80128949127172)
        self.assertAlmostEqual(cheby1.A[2], 20000)



if __name__ == '__main__':
        unittest.main()
