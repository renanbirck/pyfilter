#!/usr/bin/python3

from math import pi
from scipy import signal
import custom


def hz_to_rad(x):
    """ Converts X Hz to radians/second. """
    if isinstance(x, list):
        return list(map(hz_to_rad, x))
    return 2 * pi * x

class AnalogFilter():

    filter_parameters = {}
    filter_kind = None
    #ripple = None
    # Those are common to all types of filter
    N = None
    Wn = None
    B, A = None, None # Filter in B/A mode
    Z, P, K = None, None, None # Filter in ZPK mode

    def __init__(self, parameters=None):
        if parameters:
            self.set_parameters(parameters)

    def set_parameters(self, parameters):
        """ Configures the parameters and does some validation on them. """
        self.filter_parameters = parameters

        # Convert from Hz to rad/s
        self.filter_parameters['passband_frequency'] = hz_to_rad(self.filter_parameters['passband_frequency'])
        self.filter_parameters['stopband_frequency'] = hz_to_rad(self.filter_parameters['stopband_frequency'])

        self.refresh_filter_kind()

    def refresh_filter_kind(self):
        """ From the parameters given, it finds the filter type. """
        def filter_kind(pb0, pb1, sb0, sb1):
            if pb1 == None and sb1 == None:
                if pb0 < sb0:
                    return "lowpass"
                elif pb0 > sb0:
                    return "highpass"
                else:
                    return "allpass"
            else:
                if pb0 > sb0 and pb1 < sb1:
                    return "bandpass"
                elif pb0 < sb0 and pb1 > sb1:
                    return "bandstop"
                else:
                    raise ValueError("Meaningless filter.")

        if isinstance(self.filter_parameters['passband_frequency'], list):
            pb0, pb1 = self.filter_parameters['passband_frequency'][:]
            sb0, sb1 = self.filter_parameters['stopband_frequency'][:]
            if pb0 <= 0 or pb1 <= 0 or sb0 <= 0 or sb1 <= 0:
                raise ValueError("All values should be positive!")

            self.filter_kind = filter_kind(pb0, pb1, sb0, sb1)
        elif isinstance(self.filter_parameters['passband_frequency'], float):
            pb = self.filter_parameters['passband_frequency']
            sb = self.filter_parameters['stopband_frequency']
            if pb <= 0 or sb <= 0:
                raise ValueError("All values should be positive!")
            self.filter_kind = filter_kind(pb, None, sb, None)

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
