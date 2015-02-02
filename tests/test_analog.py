#!/usr/bin/python3
# coding: utf-8

import unittest
import sys

sys.path.append('../engine')
sys.path.append('..')

from engine import analog


class TestAnalog(unittest.TestCase):
    """ The testbench for the AnalogFilter class. """

    filter_under_test = None

    def setUp(self):
        self.filter_under_test = analog.AnalogFilter()

    def test_get_types(self):
        """ This test, gets all the known types
            of analog filter. """

        self.assertEqual(self.filter_under_test.types,
                         ['allpass', 'bandpass',
                          'bandstop', 'highpass',
                          'lowpass'])

    def test_get_classes(self):
        self.assertEqual(self.filter_under_test.classes,
                         ['butterworth', 'chebyshev',
                          'elliptical', 'bessel'])

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

    def test_fail_to_synth_filter(self):
        """ This test tries to synthesize a filter with
            invalid/meaningless settings."""
        raise NotImplementedError

    def test_compute_parameters(self):
        """ This test tries to compute the parameters (Wn and order, e.g.)
            of a filter. Because (I assume) SciPy and MATLAB already have
            those methods tested, this is more of a sanity check. """

        # Configure the filter

        parameters = {'passband_frequency': 10,
                      'stopband_frequency': 100,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        self.filter_under_test.filter_class = 'butterworth'

        # the MATLAB command line for this would be
        # [N, Wn] = buttord(Wp, Ws, Rp, Rs, 's')

        # Compute a low-pass filter
        self.filter_under_test.configure_filter(parameters)
        self.filter_under_test.compute_parameters(target='passband')
        self.assertEqual(self.filter_under_test.N, 5)
        self.assertEqual(self.filter_under_test.Wn, 71.92210683023319)

        self.filter_under_test.compute_parameters(target='stopband')
        self.assertEqual(self.filter_under_test.N, 5)
        self.assertAlmostEqual(self.filter_under_test.Wn, 99.5817763027)

        # Compute a high-pass filter

        parameters = {'passband_frequency': 100,
                      'stopband_frequency': 10,
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}

        self.filter_under_test.configure_filter(parameters)

        self.filter_under_test.compute_parameters(target='passband')
        self.assertEqual(self.filter_under_test.N, 5)
        self.assertAlmostEqual(self.filter_under_test.Wn, 548.90518846372663)

        self.filter_under_test.compute_parameters(target='stopband')
        self.assertEqual(self.filter_under_test.N, 5)
        self.assertAlmostEqual(self.filter_under_test.Wn, 396.442191233058)

        # Compute a bandpass filter
        parameters = {'passband_frequency': [1, 2],
                      'stopband_frequency': [0.1, 5],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        self.filter_under_test.configure_filter(parameters)

        self.filter_under_test.compute_parameters(target='passband')
        self.assertEqual(self.filter_under_test.filter_type, 'bandpass')
        self.assertEqual(self.filter_under_test.N, 7)
        self.assertAlmostEqual(self.filter_under_test.Wn[0], 6.07569169)
        self.assertAlmostEqual(self.filter_under_test.Wn[1], 12.99553026)

        self.filter_under_test.compute_parameters(target='stopband')
        self.assertEqual(self.filter_under_test.filter_type, 'bandpass')
        self.assertEqual(self.filter_under_test.N, 7)
        self.assertAlmostEqual(self.filter_under_test.Wn[0], 5.81782828643783)
        self.assertAlmostEqual(self.filter_under_test.Wn[1], 13.5715307020618)

        # Compute a band-stop filter

        parameters = {'passband_frequency': [1, 7],
                      'stopband_frequency': [2, 6],
                      'passband_attenuation': 1,
                      'stopband_attenuation': 80}
        self.filter_under_test.configure_filter(parameters)
        self.filter_under_test.compute_parameters(target='passband')
        self.assertEqual(self.filter_under_test.filter_type, 'bandstop')
        self.assertEqual(self.filter_under_test.N, 36)
        self.assertAlmostEqual(self.filter_under_test.Wn[0], 10.89374879)
        self.assertAlmostEqual(self.filter_under_test.Wn[1], 43.48740788)

        self.filter_under_test.compute_parameters(target='stopband')
        self.assertEqual(self.filter_under_test.N, 36)
        self.assertAlmostEqual(self.filter_under_test.Wn[0], 10.920538677969954)
        self.assertAlmostEqual(self.filter_under_test.Wn[1], 43.380726095525773)


if __name__ == '__main__':
    unittest.main()
