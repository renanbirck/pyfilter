#!/usr/bin/python3
# coding: utf-8

import unittest, sys

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
        """ This test tries to load some invalid parameters
            into the filter object, to check whether the
            handling works. """
        raise NotImplementedError

    def test_get_transfer_function(self):
        """ This test validates the transfer function and the
            pretty-printing routines. """
        raise NotImplementedError

    def test_synth_filter(self):
        """ This test tries to synthesize a filter.
            New tests could be added for different topologies. """
        raise NotImplementedError

    def test_fail_to_synth_filter(self):
        """ This test tries to synthesize a filter with
            invalid/meaningless settings."""
        raise NotImplementedError

if __name__ == '__main__':
    unittest.main()
