#!/usr/bin/python3

import unittest, sys, os

# I don't really like this, but doesn't know any way
sys.path.append('../engine')
sys.path.append('..')

from engine import calculation

class TestCalculation(unittest.TestCase):
    """ Unit tests of the calculation engine.
        The calculation engine provides an abstraction layer
        for all the algorithms involved. """

    self.Calculation = calculation()

    def setUp(self):
        pass

    def test_get_computation_types(self):
        filters = self.Calculation.get_filter_types()
        topologies = self.Calculation.get_topologies()
        self.assertEquals(filters, ["bandpass", "highpass",
                                    "lowpass", "notch",
                                    "allpass"])

        self.assertEquals(filters)

    def test_compute_filters(self):

