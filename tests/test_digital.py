#!/usr/bin/python3
# coding: utf-8
# pyfilter: a Python program for filter synthesis and analysis.
# (c) 2015 Renan Birck <renan.ee.ufsm@gmail.com>

""" This module is a testbench for the DigitalFilter class. """
import unittest
import sys

sys.path.append('../engine')
sys.path.append('..')

from engine import digital

class TestDigital(unittest.Testcase):

    filter_under_test = None
    sample_rate = 20000

    def setUp(self):
        """ Instance the filter. """
        self.filter_under_test = digital.DigitalFilter(sample_rate=self.sample_rate)
        self.assertEqual(self.filter_under_test.sample_rate, sample_rate)

    def test_construct_filters(self):
        """ Try constructing some filters. """
        butterworth = digital.ButterworthFilter(sample_rate=self.sample_rate)
        cheby1 = digital.ChebyshevIFilter(sample_rate=self.sample_rate)
        cheby2 = digital.ChebyshevIIFilter(sample_rate=self.sample_rate)
        elliptical = digital.EllipticalFilter(sample_rate=self.sample_rate)
        bessel = digital.BesselFilter(sample_rate=self.sample_rate)

        self.assertIsInstance(butterworth, digital.ButterworthFilter)
        self.assertIsInstance(cheby1, digital.ChebyshevIFilter)
        self.assertIsInstance(cheby2, digital.ChebyshevIIFilter)
        self.assertIsInstance(elliptical, digital.EllipticalFilter)
        self.assertIsInstance(bessel, digital.BesselFilter)


