#!/usr/bin/python3
# coding: utf-8

from filter import Filter
from math import pi

hz_to_rad = lambda x: 2 * pi * float(x)

class AnalogFilter(Filter):
    """ Class of a generic analog filter. """

    filter_type = None
    filter_class = None
    filter_parameters = None

    types = ['allpass', 'bandpass', 'bandstop', 'highpass', 'lowpass']
    classes = ['butterworth', 'chebyshev', 'elliptical', 'bessel']

    class_dispatcher = None

    passband_frequency = None
    passband_attenuation = None
    stopband_frequency = None
    stopband_attenuation = None

    # Internal only: passband and stopband frequency(ies) converted
    # to rad/s.

    Wp = None
    Ws = None
    def __init__(self, **kwargs):

        # Build the dispatcher table for computation of
        # filter parameters.

        # Load the initial conditions given in the kwargs.
        pass

    def configure_filter(self, settings):
        """ This configures the filter and
            determinates its type from the specifications. """

        def convert_to_Hz(x):
            if isinstance(x, list):
                return list(map(convert_to_Hz, x))
            else:
                if x < 0:
                    raise ValueError("Parameter must be positive.")
                return hz_to_rad(x)

        # Validate the filter and its parameters.

        pb_is_list = isinstance(settings['passband_frequency'], list)
        sb_is_list = isinstance(settings['stopband_frequency'], list)

        if not type(settings['passband_frequency']) == type(settings['stopband_frequency']):
            raise ValueError("The two parameters must be of the same type (number or list)")

        if pb_is_list and sb_is_list:
            (pb0, pb1) = settings['passband_frequency']
            (sb0, sb1) = settings['stopband_frequency']

            if pb0 > sb0 and pb1 < sb1:
                self.Wp = convert_to_Hz(settings['passband_frequency'])
                self.Ws = convert_to_Hz(settings['stopband_frequency'])
                self.filter_type = 'bandpass'
            elif pb0 < sb0 and pb1 > sb1:
                self.Wp = convert_to_Hz(settings['passband_frequency'])
                self.Ws = convert_to_Hz(settings['stopband_frequency'])
                self.filter_type = 'bandstop'
            else:
                raise ValueError("Meaningless filter.")
        else:
            pb = settings['passband_frequency']
            sb = settings['stopband_frequency']

            self.Wp = convert_to_Hz(pb)
            self.Ws = convert_to_Hz(sb)

            print("Wp = {}, Ws = {}", self.Wp, self.Ws)

            if self.Wp < self.Ws:
                self.filter_type = 'lowpass'
            elif self.Wp > self.Ws:
                self.filter_type = 'highpass'
            elif self.Wp == self.Ws:
                self.filter_type = 'allpass'




    def compute_order(self):
        """ This function computes the order of the filter
            for the specific parameters. """
        pass

