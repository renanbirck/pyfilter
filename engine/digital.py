#!/usr/bin/python3
# coding: utf-8

from math import pi
from scipy import signal
from filter import Filter
import custom

hz_to_rad = lambda x: 2 * pi * float(x)

class IIRFilter(Filter):

    sample_rate = None
    filter_type = None

    def compute_parameters(self):
        self._compute_parameters()

    def design(self):
        self._design() # It computes Z, P, K for numerical stability.
        self.B, self.A = signal.zpk2tf(self.Z, self.P, self.K)

    def _compute_parameters(self):
        raise ValueError("Please override me with your own _compute_parameters function!")

    def _design(self):
        self.normalize_Wn()

        raise ValueError("Please override me with your own _design function!")

    def normalize_Wn(self):
        if self.Wn > self.sample_rate:
            raise ValueError("Frequency must be smaller than sample rate.")
        self.Wn = self.Wn / (self.sample_rate/2)

# MATLAB-ish filter design classes.
class ButterworthFilter(IIRFilter):
    target = None
    filter_type = 'butter'

    def _design(self):
        self.normalize_Wn()
        self.Z, self.P, self.K = signal.butter(self.N, self.Wn,
                                               self.filter_kind, analog=False,
                                               output='zpk')

class ChebyshevIFilter(IIRFilter):
    pass

class ChebyshevIIFilter(IIRFilter):
    pass

class EllipticalFilter(IIRFilter):
    pass

class BesselFilter(IIRFilter):
    pass
