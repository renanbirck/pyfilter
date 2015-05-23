#!/usr/bin/env python3
# coding: utf-8

# pyfilter: a filter synthesis tool written in the Python language.
# (c) 2015 Renan Birck <renan.ee.ufsm@gmail.com>

# This is the main file for the GUI.


import sys
import traceback
import os
from PyQt4 import QtCore, QtGui
from pyfilter_main_digital import Ui_MainWindow
from PyQt4.QtGui import QMessageBox
from shutil import copyfile

# Aliases and other useful functions
critical = QMessageBox.critical
information = QMessageBox.information
warning = QMessageBox.information
question = QMessageBox.question

sys.path.append('../engine')
sys.path.append('..')

from engine import analog_new as analog
from engine import utils
from math import pi
from numpy import log10, abs, angle

import gui_common
import canvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar

class StartQT4(QtGui.QMainWindow):
    common = None

    def __init__(self, parent=None):

        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        common = gui_common.common_tools(self)
        common.set_status_bar("Olá mundo!")

        # Callbacks
        about = lambda: information(self, 'About PyFilter...',
                                    'PyFilter 0.1 (c) 2015 Renan Birck.')

        QtCore.QObject.connect(self.ui.actionAbout,
                               QtCore.SIGNAL("triggered()"),
                               about)

        for filter_type_widget in [self.ui.radioButton_IIR,
                                   self.ui.radioButton_FIR]:
            QtCore.QObject.connect(filter_type_widget,
                                   QtCore.SIGNAL("clicked()"),
                                   self.pick_widgets_for_filter_type)
        self.populate_window_list()

    def populate_window_list(self):
        # Format of tuples is:
        # 1. visible name
        # 2. internal name
        # 3. number of parameters
        # 4-end. parameter names

        window_types = [('Rectangular', 'boxcar', 0, ''),
                        ('Triangular', 'triang', 0, ''),
                        ('Hamming', 'hamming', 0, ''),
                        ('Hann', 'hann', 0, ''),
                        ('Kaiser', 'kaiser', 1, 'beta')]

        for window_name, window_internal, num_parameters, parameter_name in window_types:
            self.ui.comboBox_Window.addItem(window_name)

    def pick_widgets_for_filter_type(self):
        if self.ui.radioButton_IIR.isChecked():
            self.ui.stackedWidget.setCurrentIndex(0)
        elif self.ui.radioButton_FIR.isChecked():
            self.ui.stackedWidget.setCurrentIndex(1)
        else:  # Should not happen...
            pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()

    sys.exit(app.exec_())
