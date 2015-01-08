#!/usr/bin/python3
# coding: utf-8


class Filter:
    """ Generic class for a filter. This is not called directly,
        but rather, the AnalogFilter and DigitalFilter classes
        inherit from us. """

    _order = 0
    types = None
    topologies = None
    classes = None
    implementations = None
    transfer_function = None

    def __init__(self):
        pass

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, new_order):
        if new_order < 0 or not isinstance(new_order, int):
            raise ValueError("Order must be an integer > 0")
        self._order = new_order

    def synthesize(self):
        """ Synthesize the filter from the given configuration.
            Here it will fail because this class is inherited
            and other classes override this method. """
        raise NotImplementedError("Please override this with your \
                                   own implementation of synthesize")
