#!/usr/bin/python3
# coding: utf-8

# pyfilter: a Python program for filter synthesis
# (c) 2015 Renan Birck <renan.ee.ufsm@gmail.com>

""" This module has some useful routines used during the code. """
import tempfile # Used to build the HTML output
from numpy.polynomial import Polynomial

def generate_polynomial(coefs, variable='x'):
    """ Generates a polynomial from the given coefficients. """
    power = len(coefs) - 1
    polynomial = ''

    first = coefs[0]
    coefs = coefs[1:]

    if first == 1:
        polynomial = variable + "^" + str(power)
    else:
        polynomial = str(first) + variable + "^" + str(power)

    power = power - 1

    for term in coefs:
        if term == 0:
            power = power - 1
            continue

        if term == 1 and power != 0:
            operator_term = " + "
            value_term = ''
        elif term == -1 and power != 0:
            operator_term = " - "
            value_term = ''
        elif term < 0:
            operator_term = " - "
            value_term = str(abs(term))
        elif term > 0:
            operator_term = " + "
            value_term = str(term)

        else:
            continue

        if power == 1:
            power_term = variable
        elif power == 0:
            power_term = ''
        else:
            power_term = variable + '^' + str(power)

        polynomial = polynomial + operator_term + value_term + power_term

        power = power - 1

    return polynomial

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
        # First I need a list of values in descending order.
        # Then I need to enumerate them to create the (degree, value) vector,
        # and finally I need this in descending order.
        # TODO: use generators properly.

        tuples = list(reversed(list(enumerate(reversed(values)))))
        # Special case for the first element:
        (first_degree, first_value) = tuples[0]

        if len(values) == 1: # Handle the special case first
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
            # Correctly add the +/-.
            if value == 0:
                continue
            elif value < 0:
                string = string + ' - '
            else:
                string = string + ' + '
            if not (value == 1 or value == -1) and order != 0:
                string = string + str(value)

            # And the variable and power.
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

def generate_HTML(column_names, column_data):
    transpose = lambda l: [list(i) for i in zip(*l)]
    temp = tempfile.NamedTemporaryFile(prefix='pyfilter',
                                       suffix='.html',
                                       delete=False)

    print("My temporary file is ", temp.name)
    transposed_names = transpose(column_names)
    transposed_data = transpose(column_data)
    html_code = ''

    html_code += '<table border=\"1\">\n'
    html_code += '<tr>\n'

    for line in column_names:
        html_code += "<td>{}</td>\n".format(line)
    html_code += '</tr>\n'

    for line in transposed_data:
        html_code += '<tr>\n'
        for value in line:
            html_code += '<td>{}</td>\n'.format(value)
        html_code += '</tr>\n'

    temp.write(bytes(html_code, 'UTF-8'))

    temp.close()
    return temp.name
