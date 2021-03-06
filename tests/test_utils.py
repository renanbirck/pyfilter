#!/usr/bin/python3
# coding: utf-8

# pyfilter: a Python program for filter synthesis
# (c) 2015 Renan Birck <renan.ee.ufsm@gmail.com>

""" This module is a testbench for the Utils library, that has some
    routines used elsewhere in the code. """

import unittest
import sys
import subprocess

sys.path.append('../engine')
sys.path.append('..')

from engine import utils

class TestUtils(unittest.TestCase):
    """ The testbench for routines under the utils.py code. """

    def test_generate_polynomial(self):
        coefs = [1, 2, 3, 4]
        variable = 's'
        result = utils.generate_polynomial(coefs, variable)
        self.assertEqual(result, "s^3 + 2s^2 + 3s + 4")

        coefs = [1, 0, 1]
        result = utils.generate_polynomial(coefs, variable)
        self.assertEqual(result, "s^2 + 1")

        coefs = [2.5, 0, -1.5]
        result = utils.generate_polynomial(coefs, variable)
        self.assertEqual(result, "2.5s^2 - 1.5")

        coefs = [-3.5, -1.5, 1]
        result = utils.generate_polynomial(coefs, variable)
        self.assertEqual(result, "-3.5s^2 - 1.5s + 1")

        coefs = [3, 1, 0]
        result = utils.generate_polynomial(coefs, variable)
        self.assertEqual(result, "3s^2 + s")

    def test_generate_latex_for_polynomial(self):
        num = [1, 2, 3]
        den = [4, 5, 6]
        variable = 's'

        result = utils.generate_latex_for_polynomial(num, den, variable)
        self.assertEqual(result, "\\frac{s^2 + 2s + 3}{4s^2 + 5s + 6}")

        # Test handling of zero and floating point.
        num = [1, -1, 1.5]
        den = [4, 0, 1]

        result = utils.generate_latex_for_polynomial(num, den, variable)
        self.assertEqual(result, "\\frac{s^2 - s + 1.5}{4s^2 + 1}")

        # Test unequal sizes of parameters

        num = [1]
        den = [2, 3, 5]

        result = utils.generate_latex_for_polynomial(num, den, variable)
        self.assertEqual(result, "\\frac{1}{2s^2 + 3s + 5}")

        # Test case of exponential > 10

        num = [0] * 11
        den = [2]
        num[0] = 1

        result = utils.generate_latex_for_polynomial(num, den, variable)
        self.assertEqual(result, "\\frac{s^{10}}{2}")

        num = [0] * 12
        den = [2]
        num[0] = 1
        num[1] = 10

        result = utils.generate_latex_for_polynomial(num, den, variable)
        self.assertEqual(result, "\\frac{s^{11} + 10s^{10}}{2}")

    def test_generate_HTML_table(self):
        """ This tries generating table HTML for given columns. """
        column_names = ['', 'A', 'B']
        column_data = [[1, 2, 3, 4],
                       [5, 6, 7, 8],
                       [9, 0, 1, 2]]

        generated_HTML_file_name = utils.generate_HTML(column_names,
                                                       column_data)

        # Use Lynx to parse the HTML, rather than doing with other library.

        parsed_output_generated = subprocess.check_output(["lynx",
                                                           "-dump",
                                                           generated_HTML_file_name])
        parsed_output_reference = subprocess.check_output(["lynx",
                                                           "-dump",
                                                           "table_reference.html"])
        self.assertEqual(parsed_output_generated, parsed_output_reference)

    def test_generate_HTML_report(self):
        html = utils.HTMLReport()
        html.put_text("this is text")
        html.put_newline()
        html.put_polynomial([1, 2, 3], [4, 5, 6], variable='s')
        column_names = ['', 'A', 'B']
        column_data = [[1, 2, 3, 4],
                       [5, 6, 7, 8],
                       [9, 0, 1, 2]]
        html.put_table(column_names, column_data)
        html.write()

        file_name = html.output.name

        parsed_output_generated = subprocess.check_output(["lynx",
                                                           "-dump",
                                                           file_name])

        parsed_output_reference = subprocess.check_output(["lynx",
                                                           "-dump",
                                                           "report_reference.html"])

        self.assertEqual(parsed_output_generated, parsed_output_reference)

if __name__ == '__main__':
    unittest.main()
