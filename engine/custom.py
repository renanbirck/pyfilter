#!/usr/bin/python3
# coding: utf-8

# This file implements modified functions for filter computation, in order to
# make the implementation compatible with MATLAB.

# It was done after it was found that SciPy and MATLAB do those computation
# with different goals: MATLAB tries to optimize to match the stopband edge,
# while SciPy tries to optimize to match the passband edge.
