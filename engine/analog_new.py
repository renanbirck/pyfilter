#!/usr/bin/python3

from math import pi
from scipy import signal
from filter import Filter
import custom


class AnalogFilter(Filter):

   def compute_parameters(self):
        self._compute_parameters()

   def design(self):
        self._design() # It computes Z, P, K for numerical stability.
        self.B, self.A = signal.zpk2tf(self.Z, self.P, self.K)

   def _compute_parameters(self):
        raise ValueError("Please override me with your own _compute_parameters function!")

   def _design(self):
        raise ValueError("Please override me with your own _design function!")

class ButterworthFilter(AnalogFilter):
    target = None
    def _compute_parameters(self):
        if self.target == 'passband':
            self.N, self.Wn = signal.buttord(self.filter_parameters['passband_frequency'],
                                             self.filter_parameters['stopband_frequency'],
                                             self.filter_parameters['passband_attenuation'],
                                             self.filter_parameters['stopband_attenuation'],
                                             analog=True)
        elif self.target == 'stopband':
            self.N, self.Wn = custom.custom_buttord(self.filter_parameters['passband_frequency'],
                                             self.filter_parameters['stopband_frequency'],
                                             self.filter_parameters['passband_attenuation'],
                                             self.filter_parameters['stopband_attenuation'],
                                             analog=True)

        else:
            raise ValueError("Butterworth filters must match or the passband\
                              or the stopband.")


    def _design(self):
        self.Z, self.P, self.K = signal.butter(self.N, self.Wn,
                                               self.filter_kind, analog=True,
                                               output='zpk')

class BesselFilter(AnalogFilter):
    # Since the Bessel filter approximates the Butterworth filter, the calculation
    # can be done similarly.
    target = None
    def _compute_parameters(self):
        if self.target == 'passband':
            self.N, self.Wn = signal.buttord(self.filter_parameters['passband_frequency'],
                                             self.filter_parameters['stopband_frequency'],
                                             self.filter_parameters['passband_attenuation'],
                                             self.filter_parameters['stopband_attenuation'],
                                             analog=True)
        elif self.target == 'stopband':
            self.N, self.Wn = custom.custom_buttord(self.filter_parameters['passband_frequency'],
                                             self.filter_parameters['stopband_frequency'],
                                             self.filter_parameters['passband_attenuation'],
                                             self.filter_parameters['stopband_attenuation'],
                                             analog=True)

        else:
            raise ValueError("Butterworth filters must match or the passband\
                              or the stopband.")

    def _design(self):
        self.Z, self.P, self.K = signal.bessel(self.N, self.Wn,
                                               self.filter_kind, analog=True,
                                               output='zpk')

class ChebyshevIFilter(AnalogFilter):
    ripple = None
    def _compute_parameters(self):
        self.N, self.Wn = signal.cheb1ord(self.filter_parameters['passband_frequency'],
                                          self.filter_parameters['stopband_frequency'],
                                          self.filter_parameters['passband_attenuation'],
                                          self.filter_parameters['stopband_attenuation'],
                                          analog=True)
    def _design(self):
        if not self.ripple and 'ripple' in self.filter_parameters:
            self.ripple = self.filter_parameters['ripple']
        elif not self.ripple and 'ripple' not in self.filter_parameters:
            raise ValueError("Needs a ripple value.")

        self.Z, self.P, self.K = signal.cheby1(self.N, self.ripple, self.Wn,
                                               self.filter_kind, analog=True,
                                               output='zpk')

class ChebyshevIIFilter(AnalogFilter):
    stopband_attenuation = None
    def _compute_parameters(self):

        self.N, self.Wn = signal.cheb2ord(self.filter_parameters['passband_frequency'],
                self.filter_parameters['stopband_frequency'],
                self.filter_parameters['passband_attenuation'],
                self.filter_parameters['stopband_attenuation'], analog=True)
    def _design(self):
        if not self.stopband_attenuation:
            self.stopband_attenuation = self.filter_parameters['stopband_attenuation']

        self.Z, self.P, self.K = signal.cheby2(self.N, self.stopband_attenuation,
                                               self.Wn,
                                               self.filter_kind,
                                               analog=True, output='zpk')

class EllipticFilter(AnalogFilter):
    ripple = None
    stopband_attenuation = None

    def _compute_parameters(self):
        if not self.stopband_attenuation:
            self.stopband_attenuation = self.filter_parameters['stopband_attenuation']
        if not self.ripple:
            self.ripple = self.filter_parameters['ripple']
        self.N, self.Wn = signal.ellipord(self.filter_parameters['passband_frequency'],
                                          self.filter_parameters['stopband_frequency'],
                                          self.ripple,
                                          self.stopband_attenuation, analog=True)


    def _design(self):
        if not self.stopband_attenuation:
            self.stopband_attenuation = self.filter_parameters['stopband_attenuation']

        if not self.ripple:
            self.ripple = self.filter_parameters['ripple']

        self.Z, self.P, self.K = signal.ellip(self.N, self.ripple,
                                              self.stopband_attenuation,
                                              self.Wn, self.filter_kind, analog=True,
                                              output='zpk')
