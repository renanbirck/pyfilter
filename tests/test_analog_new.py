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
        self.assertAlmostEqual(bessel.B[1], 0)
        self.assertAlmostEqual(bessel.B[2], 0)
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

    def test_cheby2_N_Wn(self):
        cheby2 = analog.ChebyshevIIFilter()
        cheby2.N = 2
        cheby2.Wn = 100 # 100 rad/s
        cheby2.stopband_attenuation = 40
        cheby2.filter_kind = "lowpass"
        cheby2.design()

        self.assertAlmostEqual(cheby2.Z[0], -141.42135623731j)
        self.assertAlmostEqual(cheby2.Z[1], 141.42135623731j)
        self.assertAlmostEqual(cheby2.P[0], -9.9498743710662 -      10.0498756211209j)
        self.assertAlmostEqual(cheby2.P[1], -9.9498743710662 +      10.0498756211209j)
        self.assertAlmostEqual(cheby2.K, 0.01)

        self.assertAlmostEqual(cheby2.B[0], 0.01)
        self.assertAlmostEqual(cheby2.B[1], 0)
        self.assertAlmostEqual(cheby2.B[2], 200)
        self.assertAlmostEqual(cheby2.A[0], 1)
        self.assertAlmostEqual(cheby2.A[1], 19.8997487421324)
        self.assertAlmostEqual(cheby2.A[2], 200)

        cheby2.filter_kind = "highpass"
        cheby2.design()
        self.assertAlmostEqual(cheby2.Z[0], 70.7106781186545j, places=6)
        self.assertAlmostEqual(cheby2.Z[1], -70.7106781186545j, places=6)
        self.assertAlmostEqual(cheby2.P[0], -497.49371855331 + 502.493781056045j,
                               places=6)
        self.assertAlmostEqual(cheby2.P[1], -497.49371855331 - 502.493781056045j,
                               places=6)
        self.assertAlmostEqual(cheby2.K, 1)
        self.assertAlmostEqual(cheby2.B[0], 1)
        self.assertAlmostEqual(cheby2.B[1], 0)
        self.assertAlmostEqual(cheby2.B[2], 5000)
        self.assertAlmostEqual(cheby2.A[0], 1)
        self.assertAlmostEqual(cheby2.A[1], 994.98743710662)
        self.assertAlmostEqual(cheby2.A[2], 500000)

        cheby2.N = 1
        cheby2.Wn = [100, 200]
        cheby2.stopband_attenuation = 30
        cheby2.filter_kind = "bandpass"
        cheby2.design()
        self.assertAlmostEqual(cheby2.Z[0], 0)
        self.assertAlmostEqual(cheby2.P[0], -1.58192999292083 -      141.412508278078j)
        self.assertAlmostEqual(cheby2.P[1], -1.58192999292083 +      141.412508278078j)
        self.assertAlmostEqual(cheby2.K, 3.16385998584166)

        self.assertAlmostEqual(cheby2.B[0], 3.16385998584166)
        self.assertAlmostEqual(cheby2.A[0], 1)
        self.assertAlmostEqual(cheby2.A[1], 3.16385998584167)
        self.assertAlmostEqual(cheby2.A[2], 20000)

        cheby2.filter_kind = "bandstop"
        cheby2.design()
        self.assertAlmostEqual(cheby2.Z[0], +141.42135623731j)
        self.assertAlmostEqual(cheby2.Z[1], -141.42135623731j)
        self.assertAlmostEqual(cheby2.P[0], -6.34043905819145)
        self.assertAlmostEqual(cheby2.P[1], -3154.35568679763)
        self.assertAlmostEqual(cheby2.K, 1)

        self.assertAlmostEqual(cheby2.B[0], 1)
        self.assertAlmostEqual(cheby2.B[1], 0)
        self.assertAlmostEqual(cheby2.B[2], 20000)
        self.assertAlmostEqual(cheby2.A[0], 1)
        self.assertAlmostEqual(cheby2.A[1], 3160.69612585582)
        self.assertAlmostEqual(cheby2.A[2], 20000)

    def test_elliptic_N_Wn(self):
        elliptic = analog.EllipticFilter()
        elliptic.N = 2
        elliptic.Wn = 100 # 100 rad/s
        elliptic.ripple = 0.01
        elliptic.stopband_attenuation = 40
        elliptic.filter_kind = "lowpass"
        elliptic.design()

        self.assertAlmostEqual(elliptic.Z[0], 3219.4126544993424j)
        self.assertAlmostEqual(elliptic.Z[1], -3219.4126544993424j)
        self.assertAlmostEqual(elliptic.P[0], -221.64707884-234.89695898j)
        self.assertAlmostEqual(elliptic.P[1], -221.64707884+234.89695898j)
        self.assertAlmostEqual(elliptic.K, 0.010051889531786585)
        self.assertAlmostEqual(elliptic.B[0], 0.010051889531786585)
        self.assertAlmostEqual(elliptic.B[1], 0)
        self.assertAlmostEqual(elliptic.B[2], 104183.99356636693)
        self.assertAlmostEqual(elliptic.A[0], 1)
        self.assertAlmostEqual(elliptic.A[1], 443.29415767889253)
        self.assertAlmostEqual(elliptic.A[2], 104304.00889474427)

        elliptic.filter_kind = "highpass"
        elliptic.design()
        self.assertAlmostEqual(elliptic.Z[0], -3.1061566419652165j)
        self.assertAlmostEqual(elliptic.Z[1], 3.1061566419652165j)
        self.assertAlmostEqual(elliptic.P[0], -21.250101620074428+22.520415223362118j)
        self.assertAlmostEqual(elliptic.P[1], -21.250101620074428-22.520415223362118j)
        self.assertAlmostEqual(elliptic.K, 0.99884936993650497)
        self.assertAlmostEqual(elliptic.B[0], 0.99884936993650497)
        self.assertAlmostEqual(elliptic.B[1], 0)
        self.assertAlmostEqual(elliptic.B[2], 9.6371075649932063)
        self.assertAlmostEqual(elliptic.A[0], 1)
        self.assertAlmostEqual(elliptic.A[1], 42.50020324)
        self.assertAlmostEqual(elliptic.A[2], 958.73592069)

        elliptic.N = 1
        elliptic.Wn = [100, 200]
        elliptic.filter_kind = "bandpass"
        elliptic.design()
        self.assertAlmostEqual(elliptic.Z[0], 0)
        self.assertAlmostEqual(elliptic.P[0], -9.64726445+0j)
        self.assertAlmostEqual(elliptic.P[1], -2073.12654417+0.j)
        self.assertAlmostEqual(elliptic.K, 2082.7738086151749)
        self.assertAlmostEqual(elliptic.B[0], 2082.7738086151749)
        self.assertAlmostEqual(elliptic.B[1], 0)
        self.assertAlmostEqual(elliptic.A[0], 1)
        self.assertAlmostEqual(elliptic.A[1], 2082.7738086151749)
        self.assertAlmostEqual(elliptic.A[2], 20000)

        elliptic.filter_kind = "bandstop"
        elliptic.design()
        self.assertListEqual(list(elliptic.Z), [141.42135623730951j,
                                            -141.42135623730951j])
        self.assertListEqual(list(elliptic.P), [(-2.4006447456358564-141.40097915080096j),
                                                (-2.4006447456358564+141.40097915080096j)])
        self.assertAlmostEqual(elliptic.K, 1)
        self.assertListEqual(list(elliptic.B), [1.0, 0.0, 20000.0])
        self.assertListEqual(list(elliptic.A), [1.0, 4.8012894912717128, 20000.0])


    def test_compute_cheb1_lp(self):
        parameters = {'passband_frequency': 10,
                      'stopband_frequency': 100,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        cheby1 = analog.ChebyshevIFilter(parameters)
        cheby1.compute_parameters()

        self.assertEqual(cheby1.N, 4)
        self.assertAlmostEqual(cheby1.Wn, 62.8318530717959)

        cheby1.ripple = 1
        cheby1.design()

        self.assertAlmostEqual(cheby1.B[0], 3828618.98570601)
        self.assertAlmostEqual(cheby1.A[0], 1)
        self.assertAlmostEqual(cheby1.A[1], 59.8669045905151)
        self.assertAlmostEqual(cheby1.A[2], 5739.86489306066)
        self.assertAlmostEqual(cheby1.A[3], 184206.894005592)
        self.assertAlmostEqual(cheby1.A[4], 4295781.15645301)

    def test_compute_cheb1_hp(self):

        parameters = {'passband_frequency': 100,
                      'stopband_frequency': 10,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        cheby1 = analog.ChebyshevIFilter(parameters)
        cheby1.ripple = 1
        cheby1.compute_parameters()
        cheby1.design()

        self.assertEqual(cheby1.N, 4)
        self.assertAlmostEqual(cheby1.Wn, 628.318530717959)

        self.assertAlmostEqual(cheby1.B[0], 0.891250938133746)
        self.assertAlmostEqual(cheby1.A[0], 1)
        self.assertAlmostEqual(cheby1.A[1], 1692.86945081694)
        self.assertAlmostEqual(cheby1.A[2], 2082471.15587304)
        self.assertAlmostEqual(cheby1.A[3], 857479735.09746361)
        self.assertAlmostEqual(cheby1.A[4], 565453371958.94922)


    def test_compute_cheb1_bp(self):

        # Band-pass filter calculation
        parameters = {'passband_frequency': [1, 2],
                      'stopband_frequency': [0.1, 5],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        cheby1 = analog.ChebyshevIFilter(parameters)
        cheby1.ripple = 1
        cheby1.compute_parameters()
        cheby1.design()

        self.assertEqual(cheby1.N, 5)
        self.assertAlmostEqual(cheby1.Wn[0], 6.28318530717959)
        self.assertAlmostEqual(cheby1.Wn[1], 12.5663706143592)
        self.assertAlmostEqual(cheby1.B[0], 1202.79612788877)
        self.assertAlmostEqual(cheby1.A[0], 1)
        self.assertAlmostEqual(cheby1.A[1], 5.88621448427819)
        self.assertAlmostEqual(cheby1.A[2], 461.455958526484)
        self.assertAlmostEqual(cheby1.A[3], 2100.72662205608)
        self.assertAlmostEqual(cheby1.A[4], 79039.1859533964)
        self.assertAlmostEqual(cheby1.A[5], 259544.784834649)
        self.assertAlmostEqual(cheby1.A[6], 6240683.98035329)
        self.assertAlmostEqual(cheby1.A[7], 13096311.7289864)
        self.assertAlmostEqual(cheby1.A[8], 227143051.1812073)
        self.assertAlmostEqual(cheby1.A[9], 228767861.56059638)
        self.assertAlmostEqual(cheby1.A[10],
                               3068659219.6962843)

    def test_compute_cheb1_bs(self):
        # Band-stop filter calculation
        parameters = {'passband_frequency': [1, 7],
                      'stopband_frequency': [2, 6],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        cheby1 = analog.ChebyshevIFilter(parameters)
        cheby1.ripple = 1
        cheby1.compute_parameters()
        cheby1.design()

        self.assertEqual(cheby1.N, 14)
        self.assertAlmostEqual(cheby1.Wn[0],
                               10.771173962426296)
        self.assertAlmostEqual(cheby1.Wn[1],
                               43.982292294453401)

        self.assertAlmostEqual(cheby1.B[0], 0.891250938133753)
        self.assertAlmostEqual(cheby1.B[2], 5911.10857094055)
        self.assertAlmostEqual(cheby1.B[4], 18202171.142328978)
        self.assertAlmostEqual(cheby1.B[6], 34492453326.155769)
        self.assertAlmostEqual(cheby1.B[8], 44936338221315.367)
        self.assertAlmostEqual(cheby1.B[10],
                               42576364561914056.0)
        self.assertAlmostEqual(cheby1.B[12],
                               3.0255249276953297e+19)
        self.assertAlmostEqual(cheby1.B[14],
                               1.6380742485482297e+22)
        self.assertAlmostEqual(cheby1.B[16],
                               6.7901995359355942e+24)
        self.assertAlmostEqual(cheby1.B[18],
                               2.1445302571983762e+27)
        self.assertAlmostEqual(cheby1.B[20],
                               5.079758701897002e+29)
        self.assertAlmostEqual(cheby1.B[22],
                               8.7508711592342312e+31)
        self.assertAlmostEqual(cheby1.B[24],
                               1.0364114418785841e+34)
        self.assertAlmostEqual(cheby1.B[26],
                               7.5537001784783249e+35)
        self.assertAlmostEqual(cheby1.B[28],
                               2.5560692027246954e+37)

    def test_compute_cheb2_lp(self):
        parameters = {'passband_frequency': 10,
                      'stopband_frequency': 100,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        cheby2 = analog.ChebyshevIIFilter(parameters)
        cheby2.stopband_attenuation = 80

        cheby2.compute_parameters()
        cheby2.design()

        self.assertEqual(cheby2.N, 4)
        self.assertAlmostEqual(cheby2.Wn, 444.575606682405)

        target_B_coefs = [9.999999e-5, 0, 158.117976045623,
                          0, 31251617.9359552]
        target_A_coefs = [1, 194.810986902063, 18975.6761206756,
                          1084508.31036336, 31251617.9359552]
        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby2.B[idx],
                                   coef, places=4)
            self.assertAlmostEqual(cheby2.A[idx],
                                   target_A_coefs[idx], places=4)

    def test_compute_cheb2_hp(self):
        parameters = {'passband_frequency': 100,
                      'stopband_frequency': 10,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        cheby2 = analog.ChebyshevIIFilter(parameters)
        cheby2.stopband_attenuation = 80

        cheby2.compute_parameters()
        cheby2.design()
        self.assertEqual(cheby2.N, 4)
        self.assertAlmostEqual(cheby2.Wn, 88.8002333258017)
        target_B_coefs = [1, 2.6640245834111e-13, 7885.48143871698,
                          2.15641845491182e-08, 7772602.19003515]
        target_A_coefs = [1, 1369.99857286308,
                          946333.526262156, 383548377.904685,
                          77726021900.434341]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby2.B[idx],
                                   coef, places=4)
            self.assertAlmostEqual(cheby2.A[idx],
                                   target_A_coefs[idx], places=4)

    def test_compute_cheb2_bp(self):
        parameters = {'passband_frequency': [1, 2],
                      'stopband_frequency': [0.1, 5],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        cheby2 = analog.ChebyshevIIFilter(parameters)

        cheby2.compute_parameters()
        cheby2.design()
        self.assertEqual(cheby2.N, 5)
        self.assertAlmostEqual(cheby2.Wn[0], 2.70854152973696)
        self.assertAlmostEqual(cheby2.Wn[1], 29.1510520853571)

        target_B_coefs = [0.0132212553439163, 0, 41.1531774495097, 0,
                          27017.7489051283, 0, 256556.390945137,
                          0, 513844.393583164]
        target_A_coefs = [1, 23.4435180976834, 669.583359040983,
                          9398.53292546406, 136432.286369784, 1212538.46889098,
                          10772261.5520472, 58592163.1566463, 329589865.256886,
                          911132871.047911, 3068659219.6963]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby2.B[idx],
                                   coef, places=4)

        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby2.A[idx],
                                   coef, places=4)

    def test_compute_cheb2_bs(self):
        parameters = {'passband_frequency': [1, 50],
                      'stopband_frequency': [10, 20],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        cheby2 = analog.ChebyshevIIFilter(parameters)

        cheby2.compute_parameters()
        cheby2.design()

        self.assertEqual(cheby2.N, 5)
        self.assertAlmostEqual(cheby2.Wn[0],
                               60.9231519986727, places=3)
        self.assertAlmostEqual(cheby2.Wn[1],
                               129.600700160979, places=3)
        cheby2.design()
        target_B_coefs = [1, 0, 45374.174385258048, 0,
                         770023239.70909572, 0,
                         6079859439822.2012,
                         0, 22334583333229276.0, 0,
                         3.068658299488802e+19]
        target_A_coefs = [1.00000000e+00, 790.06228468972586, 357473.38122983265,
                         104519632.7445026, 20482841787.389153, 2506892093515.71,
                         161726026661856.78, 6515943167761986.0, 1.7595954374175722e+17,
                         3.070578153267778e+18, 3.0686582994888024e+19]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(cheby2.B[idx],
                                   coef, places=2)
        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(cheby2.A[idx],
                                   coef, places=2)

    def test_compute_butter_lp(self):
        parameters = {'passband_frequency': 10,
                      'stopband_frequency': 100,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        butter = analog.ButterworthFilter(parameters)
        butter.target = 'passband'
        butter.compute_parameters()
        butter.design()
        self.assertEqual(butter.N, 5)
        self.assertEqual(butter.Wn, 71.92210683023319)
        self.assertAlmostEqual(butter.B[0], 1924473804.6221437)
        self.assertAlmostEqual(butter.A[0], 1.00000000e+00)
        self.assertAlmostEqual(butter.A[1], 232.744826787636)
        self.assertAlmostEqual(butter.A[2], 27085.0771982035)
        self.assertAlmostEqual(butter.A[3], 1948015.8157543)
        self.assertAlmostEqual(butter.A[4], 86589900.200991)
        self.assertAlmostEqual(butter.A[5], 1924473804.6221435)

        butter.target = 'stopband'
        butter.compute_parameters()
        butter.design()
        self.assertEqual(butter.N, 5)
        self.assertAlmostEqual(butter.Wn, 99.5817763027)
        self.assertAlmostEqual(butter.B[0], 9792629962.0921497)
        self.assertAlmostEqual(butter.A[0], 1)
        self.assertAlmostEqual(butter.A[1], 322.253397435715)
        self.assertAlmostEqual(butter.A[2], 51923.626079522102)
        self.assertAlmostEqual(butter.A[3], 5170646.9170805747)
        self.assertAlmostEqual(butter.A[4], 318227063.34817803, places=3)
        self.assertAlmostEqual(butter.A[5], 9792629962.0921497)

    def test_compute_butter_hp(self):
        parameters = {'passband_frequency': 100,
                      'stopband_frequency': 10,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        butter = analog.ButterworthFilter(parameters)
        butter.target = 'passband'
        butter.compute_parameters()
        butter.design()
        self.assertEqual(butter.N, 5)
        self.assertAlmostEqual(butter.Wn, 548.90518846372663)
        self.assertAlmostEqual(butter.B[0], 1)
        self.assertAlmostEqual(butter.A[0], 1)
        self.assertAlmostEqual(butter.A[1], 1776.29450307095)
        self.assertAlmostEqual(butter.A[2], 1577611.08082004)
        self.assertAlmostEqual(butter.A[3], 865958907.6399883, places=3)
        self.assertAlmostEqual(butter.A[4], 293769686363.14844)
        self.assertAlmostEqual(butter.A[5], 49829517234887.664)


        butter.target = 'stopband'
        butter.compute_parameters()
        butter.design()
        self.assertEqual(butter.N, 5)
        self.assertAlmostEqual(butter.Wn, 396.442191233058)
        self.assertAlmostEqual(butter.B[0], 1)
        self.assertAlmostEqual(butter.A[0], 1)
        self.assertAlmostEqual(butter.A[1], 1282.91387997915)
        self.assertAlmostEqual(butter.A[2], 822934.011721574)
        self.assertAlmostEqual(butter.A[3], 326245762.84711146)
        self.assertAlmostEqual(butter.A[4], 79935023616.862686, places=3)
        self.assertAlmostEqual(butter.A[5], 9792629864165.8633)

    def test_compute_butter_bp(self):
        parameters = {'passband_frequency': [1, 2],
                      'stopband_frequency': [0.1, 5],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        butter = analog.ButterworthFilter(parameters)
        butter.target = 'passband'
        butter.compute_parameters()
        butter.design()
        self.assertEqual(butter.filter_kind, 'bandpass')
        self.assertEqual(butter.N, 7)
        self.assertAlmostEqual(butter.Wn[0], 6.07569169)
        self.assertAlmostEqual(butter.Wn[1], 12.99553026)

        self.assertAlmostEqual(butter.B[0], 759751.80527519668)
        self.assertAlmostEqual(butter.A[0], 1)
        self.assertAlmostEqual(butter.A[1], 31.0974722556149)
        self.assertAlmostEqual(butter.A[2], 1036.224236482155)
        self.assertAlmostEqual(butter.A[3], 19567.149028043725)
        self.assertAlmostEqual(butter.A[4], 355263.81277219893)
        self.assertAlmostEqual(butter.A[5], 4595251.7849443173)
        self.assertAlmostEqual(butter.A[6], 55790492.859455325)
        self.assertAlmostEqual(butter.A[7], 513056794.27105772)
        self.assertAlmostEqual(butter.A[8], 4405040750.916997)
        self.assertAlmostEqual(butter.A[9], 28647635164.403412)
        self.assertAlmostEqual(butter.A[10],
                               174871956719.38678)
        self.assertAlmostEqual(butter.A[11],
                               760477697837.74438)
        self.assertAlmostEqual(butter.A[12],
                               3179819056953.7114)
        self.assertAlmostEqual(butter.A[13],
                               7534656938190.1543)
        self.assertAlmostEqual(butter.A[14],
                               19130579538158.508)

        butter.target = 'stopband'
        butter.compute_parameters()
        butter.design()
        self.assertEqual(butter.N, 7)
        self.assertAlmostEqual(butter.Wn[0], 5.81782828643783)
        self.assertAlmostEqual(butter.Wn[1], 13.5715307020618)

        butter.design()

        self.assertAlmostEqual(butter.B[0], 1684860.320277143)
        self.assertAlmostEqual(butter.A[0], 1)
        self.assertAlmostEqual(butter.A[1], 34.844822362404)
        self.assertAlmostEqual(butter.A[2], 1159.77866919475)
        self.assertAlmostEqual(butter.A[3], 23309.4127006002)
        self.assertAlmostEqual(butter.A[4], 423324.337255822)
        self.assertAlmostEqual(butter.A[5], 5689681.03696918)
        self.assertAlmostEqual(butter.A[6], 68543839.369195938)
        self.assertAlmostEqual(butter.A[7], 643836464.42606068)
        self.assertAlmostEqual(butter.A[8], 5412004629.6462231)
        self.assertAlmostEqual(butter.A[9], 35470506117.4123, places=4)
        self.assertAlmostEqual(butter.A[10],
                               208373474926.16934, places=4)
        self.assertAlmostEqual(butter.A[11],
                               905920861700.2373, places=4)
        self.assertAlmostEqual(butter.A[12],
                               3558965506031.5576)
        self.assertAlmostEqual(butter.A[13],
                               8442608469993.4551)
        self.assertAlmostEqual(butter.A[14],
                               19130579538158.492)

    def test_compute_butter_bs(self):
        parameters = {'passband_frequency': [1, 25],
                      'stopband_frequency': [2, 15],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 40}
        butter = analog.ButterworthFilter(parameters)
        butter.target = 'passband'
        butter.compute_parameters()
        butter.design()
        self.assertEqual(butter.N, 9)
        self.assertAlmostEqual(butter.Wn[0], 8.0681551)
        self.assertAlmostEqual(butter.Wn[1], 146.79336908)
        target_B_coefs = [1, 0, 10659.165019231212, 0, 50496799.514312126,
                          0, 139547260472.68924, 0, 247909546226676.62,
                          0, 2.9361208478586816e+17, 0, 2.3182664173133981e+20,
                          0, 1.176704014318369e+23, 0, 3.484078407614217e+25,
                          0, 4.5848600847778207e+27]
        target_A_coefs = [1, 798.886667535808, 329769.118807736,
                          90767049.233665258,
                          18246055317.574032, 2779764493559.9531,
                          323737622832967.38,
                          28439472756901700.0, 1.81600865109824e+18,
                          7.8893059749655937e+19, 2.1507928764897349e+21,
                          3.9891732058277975e+22, 5.3781783783668297e+23,
                          5.4692869382179792e+24, 4.2517955086597096e+25,
                          2.5050262147266549e+26, 1.0778906831551871e+27,
                          3.0926486540565985e+27, 4.5848600847778174e+27]

        for pos, B in enumerate(target_B_coefs):
            self.assertAlmostEqual(butter.B[pos], B, places=1)
            self.assertAlmostEqual(butter.A[pos],
                                   target_A_coefs[pos], places=1)

    def test_compute_ellip_lp(self):
        parameters = {'passband_frequency': 10,
                      'stopband_frequency': 100,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        ellip = analog.EllipticFilter(parameters)
        ellip.ripple = 1
        ellip.compute_parameters()
        ellip.design()
        self.assertEqual(ellip.N, 4)
        self.assertAlmostEqual(ellip.Wn, 62.8318530717959)

        target_B_coefs = [9.99947e-5, 0, 55.7382135386156, 0, 3938804.2931307442]
        target_A_coefs = [1, 59.7697622129101, 5762.1982895999772,
                          185887.21463406115, 4419411.104776497]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(ellip.B[idx],
                                   coef, places=2)
        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(ellip.A[idx],
                                   coef, places=2)

    def test_compute_ellip_hp(self):
        parameters = {'passband_frequency': 100,
                      'stopband_frequency': 10,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        ellip = analog.EllipticFilter(parameters)
        ellip.ripple = 1
        ellip.compute_parameters()
        ellip.design()
        self.assertEqual(ellip.N, 4)
        self.assertAlmostEqual(ellip.Wn, 200 * pi)

        target_B_coefs = [8.91250938e-01, 0, 1.96559946e+04, 0, 5.496064040835e+07]
        target_A_coefs = [1.00000000e+00, 1.66052284e+03, 2.03209155e+06,
                          832134764.96873713, 549635207615.95068]

        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(ellip.B[idx],
                                   coef, places=2)
        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(ellip.A[idx],
                                   coef, places=2)

    def test_compute_ellip_bp(self):
        parameters = {'passband_frequency': [1, 2],
                      'stopband_frequency': [0.1, 5],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        ellip = analog.EllipticFilter(parameters)
        ellip.ripple = 1
        ellip.compute_parameters()
        ellip.design()

        self.assertEqual(ellip.N, 4)
        self.assertAlmostEqual(ellip.Wn[0],
                               6.28318530717959, places=7)
        self.assertAlmostEqual(ellip.Wn[1],
                               12.5663706143592, places=7)

        target_B_coefs = [9.99947595183175e-05, 0, 0.588946412352835,
                          0, 485.636345934744, 0, 3671.59900370003,
                          0, 3886.29859721522]
        target_A_coefs = [1,
                          5.97693947945851,
                          373.449322877403,
                          1601.64788735756,
                          46946.3306687963,
                          126461.048015471,
                          2328150.987,
                          2942036.496778,
                          38865023.0418]
        for idx, coef in enumerate(target_B_coefs):
            self.assertAlmostEqual(ellip.B[idx],
                                   coef, places=2)
        for idx, coef in enumerate(target_A_coefs):
            self.assertAlmostEqual(ellip.A[idx],
                                   coef, places=2)


if __name__ == '__main__':
        unittest.main()
