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

        elliptic.N = 1
        elliptic.Wn = [100, 200]
        elliptic.filter_kind = "bandpass"
        elliptic.design()
        self.assertAlmostEqual(elliptic.Z[0], 0)
        self.assertAlmostEqual(elliptic.P[0], -9.64726445+0j)
        self.assertAlmostEqual(elliptic.P[1], -2073.12654417+0.j)
        self.assertAlmostEqual(elliptic.K, 2082.7738086151749)
        self.assertAlmostEqual(elliptic.B[0],  2082.7738086151749)
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
        self.assertAlmostEqual(cheby1.Wn[0],  6.28318530717959)
        self.assertAlmostEqual(cheby1.Wn[1],  12.5663706143592)
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
                         770023239.70909572, 0, 6079859439822.2012,
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




if __name__ == '__main__':
        unittest.main()
