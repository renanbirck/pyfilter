#!/usr/bin/python3
# coding: utf-8

import unittest, sys

sys.path.append('../engine')
sys.path.append('..')

from engine import analog

class TestAnalog(unittest.TestCase):
    """ The testbench for the AnalogFilter class. """

    def setUp(self):
        filter_under_test = analog.AnalogFilter()

    def test_get_topologies(self):
        """ This test, gets all the known topologies
            for the analog filter. """
        pass

    def test_configure_filter(self):
        """ This test tries to load some invalid parameters
            into the filter object, to check whether the
            handling works. """
        pass

    def test_get_transfer_function(self):
        """ This test validates the transfer function and the
            pretty-printing routines. """
        pass

    def test_synth_filter(self):
        """ This test tries to synthesize a filter.
            New tests could be added for different topologies. """
        pass

    def test_fail_to_synth_filter(self):
        """ This test tries to synthesize a filter with
            invalid/meaningless settings."""
        pass

if __name__ == '__main__':
    unittest.main()
