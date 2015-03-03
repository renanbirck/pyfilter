#!/usr/bin/env python3
# coding: utf-8

# pyfilter: a filter synthesis tool written in the Python language.
# (c) 2015 Renan Birck <renan.ee.ufsm@gmail.com>

# This is the main file for the GUI.

import sys
from PyQt4 import QtCore, QtGui
from pyfilter_main_window import Ui_MainWindow

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Enable the Status Bar.
        self.statusBar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.set_status("blá blá blá")

        # Callbacks
        QtCore.QObject.connect(self.ui.actionAbout,
                               QtCore.SIGNAL("triggered()"),
                               self.menuAbout)

        for topologyWidget in [self.ui.radioButton_Bessel,
                               self.ui.radioButton_Butterworth,
                               self.ui.radioButton_Cheby1,
                               self.ui.radioButton_Cheby2,
                               self.ui.radioButton_Elliptical]:

            QtCore.QObject.connect(topologyWidget,
                                   QtCore.SIGNAL("clicked()"),
                                   self.get_filter_kind)

    def set_status(self, message):
        self.statusBar.showMessage(message);

    def menuAbout(self):
        message_box = QtGui.QMessageBox.information(self,
                                                    'About PyFilter...',
                                                    'PyFilter 0.1 (c) 2015 Renan Birck.')
        print("Hello World")

    def get_filter_kind(self):
        """ This function gets the appropriate filter type from
            the chosen options and configures the other radio buttons
            and controls accordingly. """

        choice = None

        if self.ui.radioButton_Bessel.isChecked():
            print("pick Bessel")
            choice = "bessel"
        elif self.ui.radioButton_Butterworth.isChecked():
            print("pick Butterworth")
            choice = "butterworth"
        elif self.ui.radioButton_Cheby1.isChecked():
            print("pick Cheby1")
            choice = "cheby1"
        elif self.ui.radioButton_Cheby2.isChecked():
            print("pick Cheby2")
            choice = "cheby2"
        elif self.ui.radioButton_Elliptical.isChecked():
            print("pick elliptical")
            choice = "elliptical"

        self.setup_widgets(choice)

    def setup_widgets(self, choice):
        if choice == "butterworth":
            self.ui.radioButton_matchPB.setEnabled(True)
            self.ui.radioButton_matchSB.setEnabled(True)
        else:
            self.ui.radioButton_matchPB.setEnabled(False)
            self.ui.radioButton_matchSB.setEnabled(False)

        if choice == "cheby1":
            self.ui.label_pbRipple.setEnabled(True)
            self.ui.plainTextEdit_pbRipple.setEnabled(True)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()

    sys.exit(app.exec_())
