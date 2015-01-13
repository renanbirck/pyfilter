#!/usr/bin/python3
# coding: utf-8

import unittest
import sys
import random

sys.path.append('../engine')
sys.path.append('..')

from engine import filter

class TestFilterClass(unittest.TestCase):
    """ The testbench for the Filter class.
        Because other classes inherit from us, we only test
        some basic features.

        Because filter calculation, parameters etc... depend
        on whether the filter is analog or digital, the functions here
        will just raise an error. """

    test_filter = None

    def setUp(self):
        self.test_filter = filter.Filter()

    def test_synth_filter(self):
        """ This test tries to synthesize a filter.
            Because this class is abstract, it should fail. """
        with self.assertRaises(NotImplementedError):
            self.test_filter.synthesize()

    def test_get_topologies(self):
        """ No topologies are known here. """
        self.assertEqual(self.test_filter.topologies, None)

    def test_get_transfer_function(self):
        """ This tries to get a transfer function that doesn't
            exist. """
        self.assertEqual(self.test_filter.transfer_function, None)
    def test_invalid_order(self):
        """ Tries to set the filter to an invalid order. """
        with self.assertRaises(ValueError):
            self.test_filter.order = -1
            self.test_filter.order = 3.1415
            self.test_filter.order = "blah"

    def test_valid_order(self):
        for _ in range(1, 100):
            random_order = random.randint(1, 1000)
            self.test_filter.order = random_order
            self.assertEqual(self.test_filter.order, random_order)

    def test_compute_order(self):
        with self.assertRaises(NotImplementedError):
            self.test_filter.compute_order()

if __name__ == '__main__':
    unittest.main()
