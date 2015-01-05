#!/usr/bin/python3

import unittest
from ..engine import calculation

class TestCalculation(unittest.TestCase):
    """ Unit tests of the calculation engine.
        The calculation engine provides an abstraction layer
        for all the algorithms involved. """

    self.Calculation = calculation()

    def setUp(self):
        pass

    def test_get_computation_types(self):
        filters = self.Calculation.get_filter_types()
        self.assertEquals(filters, ["bandpass", "highpass",
                                    "lowpass", "notch",
                                    "allpass"])
