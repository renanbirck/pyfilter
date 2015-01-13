#!/usr/bin/python3
# coding: utf-8

from filter import Filter
from math import pi

hz_to_rad = lambda x: 2 * pi * x

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

    def __init__(self, **kwargs):

        # Build the dispatcher table for computation of
        # filter parameters.

        # Load the initial conditions given in the kwargs.
        pass

    def configure_filter(self, settings):
        """ This configures the filter and
            determinates its type from the specifications. """
        Wp = hz_to_rad(settings['passband_frequency'])
        Ws = hz_to_rad(settings['stopband_frequency'])

        print("Wp = {} Hz, Ws = {} Hz".format(Wp, Ws))
        if Wp < Ws:
            self.filter_type = 'lowpass'
        elif Wp > Ws:
            self.filter_type = 'highpass'

        pass

    def compute_order(self):
        """ This function computes the order of the filter
            for the specific parameters. """
        pass

