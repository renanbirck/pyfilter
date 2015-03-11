#!/usr/bin/python3
# coding: utf-8

# pyfilter: a Python program for filter synthesis
# (c) 2015 Renan Birck <renan.ee.ufsm@gmail.com>

""" This module has some useful routines used during the code. """

def generate_latex_for_polynomial(num,
                                  den,
                                  variable):
    """ Generate the LaTeX code for a polynomial.
        Currently is supported:
        - Powers
        - Fractions (\\frac) """

    # Build the numerator string

    def build_string(values):
        string = ''
        tuples = list(reversed(list(enumerate(reversed(values))))) # kill me now
    # Special case for the first element:
        (first_degree, first_value) = tuples[0]

        if len(values) == 1:
            return str(values[0])

        if first_value != 0:
            if first_value < 0:
                string = string + '-'
            if first_value != 1:
                string = string + str(first_value)
            string = string + variable + '^'
        if first_degree >= 10:
            string = string + '{' + str(first_degree) + '}'
        else:
            string = string + str(first_degree)

        for (order, value) in tuples[1:]:
            if value == 0:
                continue
            elif value < 0:
                string = string + ' - '
            else:
                string = string + ' + '
            if not (value == 1 or value == -1) and order != 0:
                string = string + str(value)

            if order == 1:
                string = string + variable
            elif order >= 10:
                string = string + variable + '^{' + str(order) + '}'
            elif order == 0:
                string = string + str(value)
            elif order != 0:
                string = string + variable + '^' + str(order)

        return string

    num_string = build_string(num)
    den_string = build_string(den)
    return "\\frac{" + num_string + "}{" + den_string + "}"
