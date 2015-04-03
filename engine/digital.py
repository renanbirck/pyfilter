#!/usr/bin/python3
# coding: utf-8

from math import pi
from scipy import signal
import custom

hz_to_rad = lambda x: 2 * pi * float(x)

class DigitalFilter(object):
    """ Class of a general digital filter. """

    sample_rate = 0

    def __init__(self, sample_rate):
        if sample_rate <= 0:
            raise ValueError("Sampling rate must be greater than zero!")
        self.sample_rate = sample_rate


class ButterworthFilter(DigitalFilter):
    pass

class ChebyshevIFilter(DigitalFilter):
    pass

class ChebyshevIIFilter(DigitalFilter):
    pass

class EllipticalFilter(DigitalFilter):
    pass

class BesselFilter(DigitalFilter):
    pass
