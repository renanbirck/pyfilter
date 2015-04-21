#!/usr/bin/python3

# Canvas for plotting.

import gui_main
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from PyQt4 import QtCore, QtGui

class Canvas(FigureCanvas):
    """ Canvas for drawing plots. """

    def __init__(self, parent=None, width=5, height=4, dpi=96):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.axes.autoscale(True, 'both')

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

    def set_label(self, x=None, y=None):
        """ Sets the label of the axes.
        If 'None', it doesn't change. """

        if x:
            self.axes.set_xlabel(x)
        if y:
            self.axes.set_ylabel(y)

    def add_line(self, axis, value):
        """ Add a line at axis and value. """

        if axis == 'x':
            self.axes.axvline(value)
        elif axis == 'y':
            self.axes.axhline(value)
        else:
            raise ValueError("Axis must be one of X or Y.")

class StaticPlot(Canvas):
    """ A very simple plotting canvas,
    that display a static plot. """
    def compute_initial_figure(self, x, y, mode="normal"):

        dispatchers = {'normal': self.axes.plot,
                       'logx': self.axes.semilogx,
                       'logy': self.axes.semilogy,
                       'loglog': self.axes.loglog}
        choice = dispatchers[mode]

        choice(x, y)
        self.axes.autoscale_view()
        self.axes.set_xlim(left=min(x) - 1, right=max(x) + 1)
        self.axes.set_ylim(bottom=min(y) - 1, top=max(y) + 3)
