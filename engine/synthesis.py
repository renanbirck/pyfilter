#!/usr/bin/python3

# The circuit synthesis routines.
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

# Building blocks that we implement.
def rc_lowpass(s, R, C):
    return 1/(1/(R*C)+s)

def rc_highpass(s, R, C):
    return (s)/(1/(R*C) + s)

def sk_lowpass(s, R1, R2, C1, C2):
    return 1/(R1*R2*C1*C2 * s**2 + C2 * (R1 + R2) * s + 1)

def sk_highpass(s, R1, R2, C1, C2):
    raise NotImplementedError

def mfb_lowpass(s, R1, R3, R4, C2, C5):
    raise NotImplementedError

def mfb_highpass(s, C1, C3, C4, R2, R5):
    raise NotImplementedError

def mfb_bandpass(s, R1, R2, C3, C4, R5):
    raise NotImplementedError

def khn_lp(s, R1, R2, R3, R4, R5, R6, C1, C2):
    raise NotImplementedError

def khn_hp(s, R1, R2, R3, R4, R5, R6, C1, C2):
    raise NotImplementedError

def khn_bp(s, R1, R2, R3, R4, R5, R6, C1, C2):
    raise NotImplementedError

def synthesize(polynomial, filter_implementation, filter_type, parameters):
    """ Implements the filter given by polynomial,
        with the filter_implementation and filter_type given.
        Assumptions:

        - Low-pass and high-pass filters set the resistor and find the capacitor.
        - Sallen-key LP filter sets R1 = R2 = Rr and C1 and C2 can vary.
    """
    s = sym.var('s')
    if filter_implementation == '1' and filter_type == 'lp':
        C = sym.var('C')
        targets = [C]
        R = parameters['R']
        tf = rc_lowpass(s, R, C)

    elif filter_implementation == '1' and filter_type == 'hp':
        C = sym.var('C')
        targets = [C]
        R = parameters['R']
        tf = rc_highpass(s, R, C)

    elif filter_implementation == 'sk' and filter_type == 'lp':
        C1, C2, s = sym.var('C1 C2 s')
        targets = [C1, C2] # The values we want to find
        Rr = parameters['Rr']
        tf = sk_lowpass(s, Rr, Rr, C1, C2)

    return solvers.solve_undetermined_coeffs(tf - polynomial, targets, 's')

    raise NotImplementedError
