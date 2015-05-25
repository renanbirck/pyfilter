#!/usr/bin/python3

import scipy as sp, numpy as np, sympy as sym, sympy.solvers as solvers


def vec_to_polynomial(vec, poly_var='s'):
    """ Converts a vector to its polynomial representation.
    E.g. [1, 2, 3] -> s**2 + 2*s + 3"""

    s = sym.var(poly_var)
    powers = [s ** n for n in list(reversed(range(len(vec))))]
    expr_pow = [vec_val * vec_pow for (vec_val, vec_pow) in zip(vec, powers)]
    return sum(expr_pow)


def ba_to_polynomial(num, den, poly_var='s'):
    """ Like vec_to_polynomial, only for
    transfer functions with num/den. """
    return vec_to_polynomial(num, poly_var) / vec_to_polynomial(den, poly_var)
