#!/usr/bin/python3

class AnalogFilter():

    filter_parameters = None
    filter_kind = None
    # Those are common to all types of filter
    N = None
    Wn = None
    B, A = None, None # Filter in B/A mode
    Z, P, K = None, None, None # Filter in ZPK mode

    def __init__(self, parameters):
        self.filter_parameters = parameters

    def set_parameters(self, parameters):
        self.filter_parameters = parameters
        self.compute_parameters()

    def compute_parameters(self):
        self._compute_parameters()

    def design(self):
        self._design()

    def _design(self):
        raise ValueError("Please override me with your own _design function!")

    def _compute_parameters(self):
        raise ValueError("Please override me with your own _compute_parameters function!")
