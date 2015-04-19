#!/usr/bin/python3
# coding: utf-8


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
    B, A = None, None # Filter in B/A mode
    Z, P, K = None, None, None # Filter in ZPK mode


    def __init__(self):
        pass

