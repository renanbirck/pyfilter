#!/usr/bin/python3

# Canvas for plotting.

import gui_main
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt4 import QtCore, QtGui

class Canvas(FigureCanvas):
    """ Canvas for drawing plots. """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class StaticPlot(Canvas):
    """ A very simple plotting canvas,
    that display a static plot. """
    def compute_initial_figure(self, x, y):
        self.axes.plot(x, y)
