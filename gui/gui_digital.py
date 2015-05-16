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
        QtCore.QObject.connect(self.ui.actionAbout,
                               QtCore.SIGNAL("triggered()"),
                               common.menuAbout)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()

    sys.exit(app.exec_())
