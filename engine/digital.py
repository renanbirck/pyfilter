#!/usr/bin/python3
# coding: utf-8

from math import pi
from scipy import signal
from filter import Filter
import custom

hz_to_rad = lambda x: 2 * pi * float(x)
rad_to_hz = lambda x: float(x)/(2 * pi)

class IIRFilter(Filter):

    sample_rate = None
    filter_type = None
    already_normalized_Wn = False

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
        if isinstance(self.Wn, float) or isinstance(self.Wn, int):
            return self.Wn / (self.sample_rate/2)
        return list(map(lambda x: x/(self.sample_rate/2), self.Wn))

    def normalized_pb_sb(self):
        def sample_to_hz(x):
            return rad_to_hz(x/(self.sample_rate/2))

        if isinstance(self.filter_parameters['passband_frequency'], list):
            normalized_pb = list(map(sample_to_hz, self.filter_parameters['passband_frequency']))
            normalized_sb = list(map(sample_to_hz, self.filter_parameters['stopband_frequency']))
        else:
            normalized_pb = sample_to_hz(self.filter_parameters['passband_frequency'])
            normalized_sb = sample_to_hz(self.filter_parameters['stopband_frequency'])

        return normalized_pb, normalized_sb

# MATLAB-ish filter design classes.
class ButterworthFilter(IIRFilter):
    target = None

    def _compute_parameters(self):
        normalized_pb, normalized_sb = self.normalized_pb_sb()
        self.already_normalized_Wn = True
        if self.target == 'passband':
            self.N, self.Wn = signal.buttord(normalized_pb, normalized_sb,
                                             self.filter_parameters['passband_attenuation'],
                                             self.filter_parameters['stopband_attenuation'],
                                             analog=False)
        elif self.target == 'stopband': # Match stopband (like MATLAB)
            self.N, self.Wn = custom.custom_buttord(normalized_pb, normalized_sb,
                                             self.filter_parameters['passband_attenuation'],
                                             self.filter_parameters['stopband_attenuation'],
                                             analog=False)

        else:
            raise ValueError("Butterworth filters must match or the passband\
                              or the stopband.")


    def _design(self):
        if self.already_normalized_Wn:
            self.Z, self.P, self.K = signal.butter(self.N, self.Wn,
                                                   self.filter_kind, analog=False,
                                                   output='zpk')
        else:
            self.Z, self.P, self.K = signal.butter(self.N, self.normalize_Wn(),
                                                   self.filter_kind, analog=False,
                                                   output='zpk')


class ChebyshevIFilter(IIRFilter):
    ripple = None

    def _compute_parameters(self):
        normalized_pb, normalized_sb = self.normalized_pb_sb()
        self.N, self.Wn = signal.cheb1ord(normalized_pb, normalized_sb,
                                          self.filter_parameters['passband_attenuation'],
                                          self.filter_parameters['stopband_attenuation'],
                                          analog=False)
        if self.filter_kind == "bandstop": # For some reason it fails.
            self.Wn = normalized_pb

        self.already_normalized_Wn = True

    def _design(self):
        if not self.ripple and 'ripple' in self.filter_parameters:
            self.ripple = self.filter_parameters['ripple']
        elif not self.ripple and 'ripple' not in self.filter_parameters:
            raise ValueError("Needs a ripple value.")

        if self.already_normalized_Wn:
            self.Z, self.P, self.K = signal.cheby1(self.N, self.ripple, self.Wn,
                                                   self.filter_kind, analog=False,
                                                   output='zpk')
        else:
            self.Z, self.P, self.K = signal.cheby1(self.N, self.ripple, self.normalize_Wn(),
                                                   self.filter_kind, analog=False,
                                                   output='zpk')


class ChebyshevIIFilter(IIRFilter):
    stopband_attenuation = None

    def _compute_parameters(self):
        normalized_pb, normalized_sb = self.normalized_pb_sb()
        self.N, self.Wn = signal.cheb2ord(normalized_pb, normalized_sb,
                                          self.filter_parameters['passband_attenuation'],
                                          self.filter_parameters['stopband_attenuation'])
        self.already_normalized_Wn = True

    def _design(self):
        if not self.stopband_attenuation and 'stopband_attenuation' in self.filter_parameters:
            self.stopband_attenuation = self.filter_parameters['stopband_attenuation']
        elif not self.stopband_attenuation and 'stopband_attenuation' not in self.filter_parameters:
            raise ValueError("Needs a stopband_attenuation value.")

        if self.already_normalized_Wn:
            self.Z, self.P, self.K = signal.cheby2(self.N, self.stopband_attenuation, self.Wn,
                                                   self.filter_kind, analog=False,
                                                   output='zpk')
        else:
            self.Z, self.P, self.K = signal.cheby2(self.N, self.stopband_attenuation, self.normalize_Wn(),
                                                   self.filter_kind, analog=False,
                                                   output='zpk')


class EllipticalFilter(IIRFilter):
    stopband_attenuation = None
    ripple = None

    def _design(self):
        if not self.stopband_attenuation:
            self.stopband_attenuation = self.filter_parameters['stopband_attenuation']

        if not self.ripple:
            self.ripple = self.filter_parameters['ripple']

        self.Z, self.P, self.K = signal.ellip(self.N, self.ripple,
                                              self.stopband_attenuation,
                                              self.normalize_Wn(),
                                              self.filter_kind, analog=False,
                                              output='zpk')
    pass

class BesselFilter(IIRFilter):

    def _design(self):
        self.Z, self.P, self.K = signal.bessel(self.N, self.normalize_Wn(),
                                               self.filter_kind, analog=False,
                                               output='zpk')
