#!/usr/bin/python3
# coding: utf-8
# pyfilter: a Python program for filter synthesis and analysis.
# (c) 2015 Renan Birck <renan.ee.ufsm@gmail.com>

""" This module is a testbench for the AnalogFilter class. """
import unittest
import sys

sys.path.append('../engine')
sys.path.append('..')

from engine import analog


class TestAnalog(unittest.TestCase):
    """ The testbench for the AnalogFilter class. """

    filter_under_test = None

    def setUp(self):
        """ This tries to construct a filter with
            parameters given in the arguments of the
            object instantiation. """
        self.filter_under_test = analog.AnalogFilter()

    def test_get_types(self):
        """ This test, gets all the known types
            of analog filter. """

        self.assertEqual(self.filter_under_test.types,
                         ['allpass', 'bandpass',
                          'bandstop', 'highpass',
                          'lowpass'])

    def test_get_classes(self):
        """ Finds the classes of supported filters. """
        self.assertEqual(self.filter_under_test.classes,
                         ['butterworth', 'chebyshev_1', 'chebyshev_2',
                          'elliptical', 'bessel'])

    def test_pass_initial_arguments(self):
        """ Tests passing parameters as arguments. """
        parameters = {'passband_frequency': 10,
                      'stopband_frequency': 100,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        temp_filter = analog.AnalogFilter(parameters,
                                          filter_class='butterworth')

        self.assertEqual(temp_filter.filter_class, 'butterworth')
        temp_filter.compute_parameters(target='passband')
        self.assertEqual(temp_filter.N, 5)
        self.assertEqual(temp_filter.Wn, 71.92210683023319)

    def test_configure_filter(self):
        """ This test tries configuring the filter with some
            example values, to check if the type of filter is determined
            correctly.
            The parameters are in Hertz, NOT in rad/s! """

        parameters = {'passband_frequency': 1,
                      'stopband_frequency': 10,
                      'passband_attenuation': 0,
                      'stopband_attenuation': 80}

        # Wp < Ws, low-pass filter
        self.filter_under_test.configure_filter(parameters)
        self.assertEqual(self.filter_under_test.filter_type, 'lowpass')

        # Wp > Ws, high-pass filter
        parameters['passband_frequency'] = 20
        parameters['stopband_frequency'] = 10
        self.filter_under_test.configure_filter(parameters)
        self.assertEqual(self.filter_under_test.filter_type, 'highpass')

        # Wp and Ws are lists where Wp[0]>Ws[0] and Wp[1]<Ws[1],
        # band-pass filter
        parameters['passband_frequency'] = [2, 5]
        parameters['stopband_frequency'] = [1, 6]
        self.filter_under_test.configure_filter(parameters)
        self.assertEqual(self.filter_under_test.filter_type, 'bandpass')

        # Wp and Ws are lists where Wp[0]<Ws[0] and Wp[1]>Ws[1],
        # band-stop filter
        parameters['passband_frequency'] = [1, 6]
        parameters['stopband_frequency'] = [2, 5]
        self.filter_under_test.configure_filter(parameters)
        self.assertEqual(self.filter_under_test.filter_type, 'bandstop')

        # Other combinations don't make sense.
        parameters['passband_frequency'] = [6, 1]
        parameters['stopband_frequency'] = [6, 6]
        with self.assertRaises(ValueError):
            self.filter_under_test.configure_filter(parameters)

        # Wp = Ws, all-pass filter
        parameters['passband_frequency'] = 1
        parameters['stopband_frequency'] = 1
        self.filter_under_test.configure_filter(parameters)
        self.assertEqual(self.filter_under_test.filter_type, 'allpass')

        # Invalid parameters
        with self.assertRaises(ValueError):
            for invalid in [-1, "invalid", '1']:
                parameters['passband_frequency'] = invalid
                self.filter_under_test.configure_filter(parameters)

    def test_get_transfer_function(self):
        """ This test validates the transfer function calculation. """
        raise NotImplementedError

    def test_compute_cheb1_lp_filter(self):
        """ This test tries to compute the parameters of a Chebyshev type1
            low-pass filter. """

        # Low-pass filter calculation
        parameters = {'passband_frequency': 10,
                      'stopband_frequency': 100,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        self.filter_under_test.filter_class = 'chebyshev_1'
        self.filter_under_test.configure_filter(parameters)
        self.filter_under_test.compute_parameters(target='passband')

        self.assertEqual(self.filter_under_test.N, 4)
        self.assertAlmostEqual(self.filter_under_test.Wn, 62.8318530717959)

        self.filter_under_test.design(ripple=1)
        self.assertAlmostEqual(self.filter_under_test.B[0], 3828618.98570601)
        self.assertAlmostEqual(self.filter_under_test.A[0], 1)
        self.assertAlmostEqual(self.filter_under_test.A[1], 59.8669045905151)
        self.assertAlmostEqual(self.filter_under_test.A[2], 5739.86489306066)
        self.assertAlmostEqual(self.filter_under_test.A[3], 184206.894005592)
        self.assertAlmostEqual(self.filter_under_test.A[4], 4295781.15645301)

    def test_compute_cheb1_hp_filter(self):
        """ This test tries to compute the parameters of a Chebyshev type1
            high-pass filter. """

       # High-pass filter calculation
        parameters = {'passband_frequency': 100,
                      'stopband_frequency': 10,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        self.filter_under_test.filter_class = 'chebyshev_1'
        self.filter_under_test.configure_filter(parameters)
        self.filter_under_test.compute_parameters(target='passband')

        self.assertEqual(self.filter_under_test.N, 4)
        self.assertAlmostEqual(self.filter_under_test.Wn, 628.318530717959)

        self.filter_under_test.design(ripple=1)
        self.assertAlmostEqual(self.filter_under_test.B[0], 0.891250938133746)
        self.assertAlmostEqual(self.filter_under_test.A[0], 1)
        self.assertAlmostEqual(self.filter_under_test.A[1], 1692.86945081694)
        self.assertAlmostEqual(self.filter_under_test.A[2], 2082471.15587304)
        self.assertAlmostEqual(self.filter_under_test.A[3], 857479735.09746361)
        self.assertAlmostEqual(self.filter_under_test.A[4], 565453371958.94922)

    def test_compute_cheb1_bp_filter(self):
        """ This test tries to compute the parameters of a Chebyshev type1
            band-pass filter. """

        # Band-pass filter calculation
        parameters = {'passband_frequency': [1, 2],
                      'stopband_frequency': [0.1, 5],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        self.filter_under_test.filter_class = 'chebyshev_1'
        self.filter_under_test.configure_filter(parameters)
        self.filter_under_test.compute_parameters(target='passband')
        self.assertEqual(self.filter_under_test.N, 5)
        self.assertAlmostEqual(self.filter_under_test.Wn[0], 6.28318530717959)
        self.assertAlmostEqual(self.filter_under_test.Wn[1], 12.5663706143592)

        self.filter_under_test.design(ripple=1)
        self.assertAlmostEqual(self.filter_under_test.B[0], 1202.79612788877)
        self.assertAlmostEqual(self.filter_under_test.A[0], 1)
        self.assertAlmostEqual(self.filter_under_test.A[1], 5.88621448427819)
        self.assertAlmostEqual(self.filter_under_test.A[2], 461.455958526484)
        self.assertAlmostEqual(self.filter_under_test.A[3], 2100.72662205608)
        self.assertAlmostEqual(self.filter_under_test.A[4], 79039.1859533964)
        self.assertAlmostEqual(self.filter_under_test.A[5], 259544.784834649)
        self.assertAlmostEqual(self.filter_under_test.A[6], 6240683.98035329)
        self.assertAlmostEqual(self.filter_under_test.A[7], 13096311.7289864)
        self.assertAlmostEqual(self.filter_under_test.A[8], 227143051.1812073)
        self.assertAlmostEqual(self.filter_under_test.A[9], 228767861.56059638)
        self.assertAlmostEqual(self.filter_under_test.A[10],
                               3068659219.6962843)

    def test_compute_cheb1_bs_filter(self):
        """ This test tries to compute the parameters of a Chebyshev type1
            band-stop filter. """

        # Band-stop filter calculation
        parameters = {'passband_frequency': [1, 7],
                      'stopband_frequency': [2, 6],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        self.filter_under_test.filter_class = 'chebyshev_1'
        self.filter_under_test.configure_filter(parameters)
        self.filter_under_test.compute_parameters(target='passband')
        self.assertEqual(self.filter_under_test.N, 14)
        self.assertAlmostEqual(self.filter_under_test.Wn[0],
                               10.771173962426296)
        self.assertAlmostEqual(self.filter_under_test.Wn[1],
                               43.982292294453401)

        self.filter_under_test.design(ripple=1)
        self.assertAlmostEqual(self.filter_under_test.B[0], 0.891250938133753)
        self.assertAlmostEqual(self.filter_under_test.B[2], 5911.10857094055)
        self.assertAlmostEqual(self.filter_under_test.B[4], 18202171.142328978)
        self.assertAlmostEqual(self.filter_under_test.B[6], 34492453326.155769)
        self.assertAlmostEqual(self.filter_under_test.B[8], 44936338221315.367)
        self.assertAlmostEqual(self.filter_under_test.B[10],
                               42576364561914056.0)
        self.assertAlmostEqual(self.filter_under_test.B[12],
                               3.0255249276953297e+19)
        self.assertAlmostEqual(self.filter_under_test.B[14],
                               1.6380742485482297e+22)
        self.assertAlmostEqual(self.filter_under_test.B[16],
                               6.7901995359355942e+24)
        self.assertAlmostEqual(self.filter_under_test.B[18],
                               2.1445302571983762e+27)
        self.assertAlmostEqual(self.filter_under_test.B[20],
                               5.079758701897002e+29)
        self.assertAlmostEqual(self.filter_under_test.B[22],
                               8.7508711592342312e+31)
        self.assertAlmostEqual(self.filter_under_test.B[24],
                               1.0364114418785841e+34)
        self.assertAlmostEqual(self.filter_under_test.B[26],
                               7.5537001784783249e+35)
        self.assertAlmostEqual(self.filter_under_test.B[28],
                               2.5560692027246954e+37)

    def test_compute_cheb2_lp_filter(self):
        """ This test tries to compute the parameters of a Chebyshev type2
            low-pass filter. """
        parameters = {'passband_frequency': 10,
                      'stopband_frequency': 100,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        self.filter_under_test.filter_class = 'chebyshev_2'
        self.filter_under_test.configure_filter(parameters)
        self.filter_under_test.compute_parameters(target='passband')

        self.assertEqual(self.filter_under_test.N, 4)
        self.assertAlmostEqual(self.filter_under_test.Wn, 444.575606682405)

    def test_compute_cheb2_hp_filter(self):
        """ This test tries to compute the parameters of a Chebyshev type2
            high-pass filter. """
        parameters = {'passband_frequency': 100,
                      'stopband_frequency': 10,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        self.filter_under_test.filter_class = 'chebyshev_2'
        self.filter_under_test.configure_filter(parameters)
        self.filter_under_test.compute_parameters(target='passband')

        self.assertEqual(self.filter_under_test.N, 4)
        self.assertAlmostEqual(self.filter_under_test.Wn, 88.8002333258017)

    def test_compute_cheb2_bp_filter(self):
        """ This test tries to compute the parameters of a Chebyshev type2
            band-pass filter. """

        # Band-pass filter calculation
        parameters = {'passband_frequency': [1, 2],
                      'stopband_frequency': [0.1, 5],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        self.filter_under_test.filter_class = 'chebyshev_2'
        self.filter_under_test.configure_filter(parameters)
        self.filter_under_test.compute_parameters(target='passband')
        self.assertEqual(self.filter_under_test.N, 5)
        self.assertAlmostEqual(self.filter_under_test.Wn[0], 2.70854152973696)
        self.assertAlmostEqual(self.filter_under_test.Wn[1], 29.1510520853571)

    def test_compute_cheb2_bs_filter(self):
        """ This test tries to compute the parameters of a Chebyshev type2
            band-stop filter. """
        parameters = {'passband_frequency': [1, 7],
                      'stopband_frequency': [2, 6],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        self.filter_under_test.filter_class = 'chebyshev_2'
        self.filter_under_test.configure_filter(parameters)
        self.filter_under_test.compute_parameters(target='passband')
        self.assertEqual(self.filter_under_test.N, 14)
        self.assertAlmostEqual(self.filter_under_test.Wn[0],
                               12.460281968697171)
        self.assertAlmostEqual(self.filter_under_test.Wn[1],
                               38.020080344889088)

    def test_compute_butter_lp_filter(self):
        """ This test tries to compute the parameters of a Butterworth
            low-pass filter. """

        # Configure the filter

        parameters = {'passband_frequency': 10,
                      'stopband_frequency': 100,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        self.filter_under_test.filter_class = 'butterworth'

        self.filter_under_test.configure_filter(parameters)
        self.filter_under_test.compute_parameters(target='passband')
        self.assertEqual(self.filter_under_test.N, 5)
        self.assertEqual(self.filter_under_test.Wn, 71.92210683023319)

        self.filter_under_test.design()
        self.assertAlmostEqual(self.filter_under_test.B[0], 1924473804.6221437)
        self.assertAlmostEqual(self.filter_under_test.A[0], 1.00000000e+00)
        self.assertAlmostEqual(self.filter_under_test.A[1], 232.744826787636)
        self.assertAlmostEqual(self.filter_under_test.A[2], 27085.0771982035)
        self.assertAlmostEqual(self.filter_under_test.A[3], 1948015.8157543)
        self.assertAlmostEqual(self.filter_under_test.A[4], 86589900.200991)
        self.assertAlmostEqual(self.filter_under_test.A[5], 1924473804.6221435)

        self.filter_under_test.compute_parameters(target='stopband')
        self.assertEqual(self.filter_under_test.N, 5)
        self.assertAlmostEqual(self.filter_under_test.Wn, 99.5817763027)
        self.filter_under_test.design()

        self.assertAlmostEqual(self.filter_under_test.B[0], 9792629962.0921497)
        self.assertAlmostEqual(self.filter_under_test.A[0], 1)
        self.assertAlmostEqual(self.filter_under_test.A[1], 322.253397435715)
        self.assertAlmostEqual(self.filter_under_test.A[2], 51923.626079522102)
        self.assertAlmostEqual(self.filter_under_test.A[3], 5170646.9170805747)
        self.assertAlmostEqual(self.filter_under_test.A[4], 318227063.34817797)
        self.assertAlmostEqual(self.filter_under_test.A[5], 9792629962.0921497)

    def test_compute_butter_hp_filter(self):
        """ This test tries to compute the parameters of a Butterworth
            high-pass filter. """

        # Compute a high-pass filter

        parameters = {'passband_frequency': 100,
                      'stopband_frequency': 10,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        self.filter_under_test.filter_class = 'butterworth'
        self.filter_under_test.configure_filter(parameters)

        self.filter_under_test.compute_parameters(target='passband')
        self.assertEqual(self.filter_under_test.N, 5)
        self.assertAlmostEqual(self.filter_under_test.Wn, 548.90518846372663)

        self.filter_under_test.design()
        self.assertAlmostEqual(self.filter_under_test.B[0], 1)
        self.assertAlmostEqual(self.filter_under_test.A[0], 1)
        self.assertAlmostEqual(self.filter_under_test.A[1], 1776.29450307095)
        self.assertAlmostEqual(self.filter_under_test.A[2], 1577611.08082004)
        self.assertAlmostEqual(self.filter_under_test.A[3], 865958907.63998842)
        self.assertAlmostEqual(self.filter_under_test.A[4], 293769686363.14844)
        self.assertAlmostEqual(self.filter_under_test.A[5], 49829517234887.664)

        self.filter_under_test.compute_parameters(target='stopband')
        self.assertEqual(self.filter_under_test.N, 5)
        self.assertAlmostEqual(self.filter_under_test.Wn, 396.442191233058)

        self.filter_under_test.design()
        self.assertAlmostEqual(self.filter_under_test.B[0], 1)
        self.assertAlmostEqual(self.filter_under_test.A[0], 1)
        self.assertAlmostEqual(self.filter_under_test.A[1], 1282.91387997915)
        self.assertAlmostEqual(self.filter_under_test.A[2], 822934.011721574)
        self.assertAlmostEqual(self.filter_under_test.A[3], 326245762.84711146)
        self.assertAlmostEqual(self.filter_under_test.A[4], 79935023616.862701)
        self.assertAlmostEqual(self.filter_under_test.A[5], 9792629864165.8633)

    def test_compute_butter_bp_filter(self):
        """ This test tries to compute the parameters of a Butterworth
            band-pass filter. """

        # Compute a bandpass filter
        parameters = {'passband_frequency': [1, 2],
                      'stopband_frequency': [0.1, 5],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        self.filter_under_test.configure_filter(parameters)

        self.filter_under_test.filter_class = 'butterworth'
        self.filter_under_test.compute_parameters(target='passband')
        self.assertEqual(self.filter_under_test.filter_type, 'bandpass')
        self.assertEqual(self.filter_under_test.N, 7)
        self.assertAlmostEqual(self.filter_under_test.Wn[0], 6.07569169)
        self.assertAlmostEqual(self.filter_under_test.Wn[1], 12.99553026)

        self.filter_under_test.design()

        self.assertAlmostEqual(self.filter_under_test.B[0], 759751.80527519668)
        self.assertAlmostEqual(self.filter_under_test.A[0], 1)
        self.assertAlmostEqual(self.filter_under_test.A[1], 31.0974722556149)
        self.assertAlmostEqual(self.filter_under_test.A[2], 1036.224236482155)
        self.assertAlmostEqual(self.filter_under_test.A[3], 19567.149028043725)
        self.assertAlmostEqual(self.filter_under_test.A[4], 355263.81277219893)
        self.assertAlmostEqual(self.filter_under_test.A[5], 4595251.7849443173)
        self.assertAlmostEqual(self.filter_under_test.A[6], 55790492.859455325)
        self.assertAlmostEqual(self.filter_under_test.A[7], 513056794.27105772)
        self.assertAlmostEqual(self.filter_under_test.A[8], 4405040750.9169989)
        self.assertAlmostEqual(self.filter_under_test.A[9], 28647635164.403412)
        self.assertAlmostEqual(self.filter_under_test.A[10],
                               174871956719.38678)
        self.assertAlmostEqual(self.filter_under_test.A[11],
                               760477697837.74438)
        self.assertAlmostEqual(self.filter_under_test.A[12],
                               3179819056953.7124)
        self.assertAlmostEqual(self.filter_under_test.A[13],
                               7534656938190.1572)
        self.assertAlmostEqual(self.filter_under_test.A[14],
                               19130579538158.508)

        self.filter_under_test.compute_parameters(target='stopband')
        self.assertEqual(self.filter_under_test.filter_type, 'bandpass')
        self.assertEqual(self.filter_under_test.N, 7)
        self.assertAlmostEqual(self.filter_under_test.Wn[0], 5.81782828643783)
        self.assertAlmostEqual(self.filter_under_test.Wn[1], 13.5715307020618)

        self.filter_under_test.design()

        self.assertAlmostEqual(self.filter_under_test.B[0], 1684860.320277143)
        self.assertAlmostEqual(self.filter_under_test.A[0], 1)
        self.assertAlmostEqual(self.filter_under_test.A[1], 34.844822362404)
        self.assertAlmostEqual(self.filter_under_test.A[2], 1159.77866919475)
        self.assertAlmostEqual(self.filter_under_test.A[3], 23309.4127006002)
        self.assertAlmostEqual(self.filter_under_test.A[4], 423324.337255822)
        self.assertAlmostEqual(self.filter_under_test.A[5], 5689681.03696918)
        self.assertAlmostEqual(self.filter_under_test.A[6], 68543839.369195938)
        self.assertAlmostEqual(self.filter_under_test.A[7], 643836464.42606068)
        self.assertAlmostEqual(self.filter_under_test.A[8], 5412004629.6462231)
        self.assertAlmostEqual(self.filter_under_test.A[9], 35470506117.412323)
        self.assertAlmostEqual(self.filter_under_test.A[10],
                               208373474926.16937)
        self.assertAlmostEqual(self.filter_under_test.A[11],
                               905920861700.23743)
        self.assertAlmostEqual(self.filter_under_test.A[12],
                               3558965506031.5586)
        self.assertAlmostEqual(self.filter_under_test.A[13],
                               8442608469993.46)
        self.assertAlmostEqual(self.filter_under_test.A[14],
                               19130579538158.492)

    def test_compute_butter_bs_filter(self):
        """ This test tries to compute the parameters of a Butterworth
            band-stop filter. """

        parameters = {'passband_frequency': [1, 7],
                      'stopband_frequency': [2, 6],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        self.filter_under_test.filter_class = 'butterworth'
        self.filter_under_test.configure_filter(parameters)
        self.filter_under_test.compute_parameters(target='passband')
        self.assertEqual(self.filter_under_test.filter_type, 'bandstop')
        self.assertEqual(self.filter_under_test.N, 36)
        self.assertAlmostEqual(self.filter_under_test.Wn[0], 10.89374879)
        self.assertAlmostEqual(self.filter_under_test.Wn[1], 43.48740788)

        self.filter_under_test.compute_parameters(target='stopband')
        self.assertEqual(self.filter_under_test.N, 36)
        self.assertAlmostEqual(self.filter_under_test.Wn[0],
                               10.920538677969954)
        self.assertAlmostEqual(self.filter_under_test.Wn[1],
                               43.380726095525773)
        raise NotImplementedError("Bandstop test not implemented")

if __name__ == '__main__':
    unittest.main()
