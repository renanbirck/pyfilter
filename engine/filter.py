#!/usr/bin/python3
# coding: utf-8

from math import pi
from scipy import signal

class Filter:
    """ Generic class for a filter. This is not called directly,
        but rather, the AnalogFilter and DigitalFilter classes
        inherit from us. """

    filter_parameters = {}
    filter_kind = None
    #ripple = None
    # Those are common to all types of filter
    N = None
    Wn = None
    B, A = None, None  # Filter in B/A mode
    Z, P, K = None, None, None  # Filter in ZPK mode
    W, H = None, None  # Filter's frequencies and values.
    def hz_to_rad(self, x):
        """ Converts X Hz to radians/second. """
        if isinstance(x, list):
            return list(map(self.hz_to_rad, x))
        return 2 * pi * x



    def __init__(self, parameters=None):
        if parameters:
            self.set_parameters(parameters)

    def set_parameters(self, parameters):
        """ Configures the parameters and does some validation on them. """
        self.filter_parameters = parameters

        # Convert from Hz to rad/s
        self.filter_parameters['passband_frequency'] = self.hz_to_rad(self.filter_parameters['passband_frequency'])
        self.filter_parameters['stopband_frequency'] = self.hz_to_rad(self.filter_parameters['stopband_frequency'])

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

    def compute_frequencies(self, N=None):
        self.W, self.H = signal.freqs(self.B, self.A, N)
