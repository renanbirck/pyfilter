#!/usr/bin/python3
# coding: utf-8
# pyfilter: a Python program for filter synthesis and analysis.
# (c) 2015 Renan Birck <renan.ee.ufsm@gmail.com>

""" This module is a testbench for the AnalogFilter class. """
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

if __name__ == '__main__':
        unittest.main()
