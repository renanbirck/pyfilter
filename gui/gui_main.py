#!/usr/bin/env python3
# coding: utf-8

# pyfilter: a filter synthesis tool written in the Python language.
# (c) 2015 Renan Birck <renan.ee.ufsm@gmail.com>

# This is the main file for the GUI.

import sys
from PyQt4 import QtCore, QtGui
from pyfilter_main_window import Ui_MainWindow

class StartQT4(QtGui.QMainWindow):

    BAND_MESSAGE = """ For the bandpass and bandstop cases,
    give 2 frequencies separated by space,
    like: 1 10, otherwise give one frequency."""

    config_dict = {}  # The dictionary of configuration
                      # used by the validation routines.

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
                                   self.get_filter_TF)

        for typeWidget in [self.ui.radioButton_AP,
                           self.ui.radioButton_BP,
                           self.ui.radioButton_BS,
                           self.ui.radioButton_HP,
                           self.ui.radioButton_LP]:
            QtCore.QObject.connect(typeWidget,
                                   QtCore.SIGNAL("clicked()"),
                                   self.get_filter_type)

        for designParametersWidget in [self.ui.radioButton_NWn,
                                       self.ui.radioButton_AttSpecs]:
            QtCore.QObject.connect(designParametersWidget,
                                   QtCore.SIGNAL("clicked()"),
                                   self.configure_boxes_for_design_parameters)

        QtCore.QObject.connect(self.ui.pushButton_Design,
                               QtCore.SIGNAL("clicked()"),
                               self.design_filter)

        # Initial preparations
        self.configure_boxes_for_design_parameters()
        self.get_filter_TF()
        self.get_filter_type()

        # Populate the color boxes

        color_names = ['Red', 'Green', 'Blue', 'Yellow', 'Black']
        color_internal_names = ['red', 'green', 'blue', 'yellow', 'black']

        color_pairs = zip(color_names, color_internal_names)

    def set_status(self, message):
        self.statusBar.showMessage(message)

    def menuAbout(self):
        message_box = QtGui.QMessageBox.information(self,
                                                    'About PyFilter...',
                                                    'PyFilter 0.1 (c) 2015 Renan Birck.')
        print("Hello World")

    def configure_boxes_for_design_parameters(self):
        """ This function configure the text boxes for the chosen design parameters.
        """
        if self.ui.radioButton_NWn.isChecked():
            self.ui.label_opt1.setText("N: ")
            self.ui.label_opt2.setText("Wn: ")
            self.ui.label_opt3.hide()
            self.ui.label_opt4.hide()
            self.ui.plainTextEdit_opt1.setEnabled(True)
            self.ui.plainTextEdit_opt2.setEnabled(True)
            self.ui.plainTextEdit_opt3.hide()
            self.ui.plainTextEdit_opt4.hide()

            self.ui.plainTextEdit_opt1.setToolTip("The order. "
                                                  "It must be an integer bigger than zero.")
            self.ui.plainTextEdit_opt2.setToolTip("The natural frequency(ies). \n" + self.BAND_MESSAGE)

            self.config_dict['mode'] = "N_WN"
        elif self.ui.radioButton_AttSpecs.isChecked():
            self.ui.label_opt1.setText("Fpass (Hz): ")
            self.ui.label_opt2.setText("Fstop (Hz): ")
            self.ui.label_opt3.setText("Rpass (dB): ")
            self.ui.label_opt4.setText("Rstop (dB): ")
            self.ui.label_opt3.show()
            self.ui.label_opt4.show()
            self.ui.plainTextEdit_opt3.show()
            self.ui.plainTextEdit_opt4.show()

            self.ui.plainTextEdit_opt1.setToolTip("The passband frequency(ies), in hertz. " + self.BAND_MESSAGE)
            self.ui.plainTextEdit_opt2.setToolTip("The stop frequency(ies), in hertz." + self.BAND_MESSAGE)
            self.ui.plainTextEdit_opt3.setToolTip("The attenuation at passband, in dB.")
            self.ui.plainTextEdit_opt4.setToolTip("The attenuation at stopband, in dB.")
            self.config_dict['mode'] = "specs"

        else:
            raise ValueError("Somehow we chose something that can't be chosen!")

    def get_filter_TF(self):
        """ This function gets the appropriate filter transfer-fucntion from
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

        self.config_dict['filter_TF'] = choice
        self.setup_widgets(choice)

    def get_filter_type(self):
        """ This function gets the appropriate filter type from the chosen
            options and configures the other radio buttons
            and controls accordingly. """

        choice = None
        if self.ui.radioButton_LP.isChecked():
            choice = "lowpass"
        elif self.ui.radioButton_HP.isChecked():
            choice = "highpass"
        elif self.ui.radioButton_BP.isChecked():
            choice = "bandpass"
        elif self.ui.radioButton_BS.isChecked():
            choice = "bandstop"
        elif self.ui.radioButton_AP.isChecked():
            choice = "allpass"
        self.config_dict['filter_type'] = choice
        print("picked filter type {}".format(self.config_dict['filter_type']))

    def setup_widgets(self, choice):
        if choice == "butterworth":
            # Butterworth filter needs to have the choice between match the
            # passband or the stopband.
            self.ui.radioButton_matchPB.setEnabled(True)
            self.ui.radioButton_matchSB.setEnabled(True)
        else:
            self.ui.radioButton_matchPB.setEnabled(False)
            self.ui.radioButton_matchSB.setEnabled(False)

        if choice == "cheby1":
            # Chebyshev type-1 filter needs to have the option to
            # configure the ripple.
            self.ui.label_pbRipple.setEnabled(True)
            self.ui.plainTextEdit_pbRipple.setEnabled(True)
        else:
            self.ui.label_pbRipple.setEnabled(False)
            self.ui.plainTextEdit_pbRipple.setEnabled(False)

    def design_filter(self):
        """ This function designs the filter. """
        # Parameter validation
        if self.config_dict['mode'] == "N_WN":
            # In N, Wn mode: N must be integer > 0
            # Wn must be either 1 or 2 numbers > 0

            try:
                temp_N = int(self.ui.plainTextEdit_opt1.toPlainText())
                if temp_N <= 0:
                    raise ValueError("Order must be bigger than 0!")
            except:
                QtGui.QMessageBox.critical(self,
                                           'Parameter error',
                                           'The filter order must be integer '
                                           'and bigger than zero. Please fix.')
                return

            # Wn must be either 1 or 2 parameters.
            self.config_dict['Wn'] = self.ui.plainTextEdit_opt2.toPlainText().split()
            try:
                self.config_dict['Wn'] = list(map(float, self.config_dict['Wn']))
                if not 1 <= len(self.config_dict['Wn']) <= 2:
                    raise ValueError("Need 1 or 2 values for frequency!")
            except ValueError:
                QtGui.QMessageBox.critical(self,
                                           'Parameter error',
                                           'You need to give either 1 or 2 values '
                                           'for the Wn parameter.')
                return

            # If filter is LP or HP, Wn must be 1 parameter.
            # If filter is BP or BS, Wn must be 2 parameters in rising order.

            if self.config_dict['filter_type'] in ['bandpass', 'bandstop']:
                num_elements = 2
            else:
                num_elements = 1

            if len(self.config_dict['Wn']) != num_elements:
                QtGui.QMessageBox.critical(self,
                                           'Parameter error',
                                           'This filter type needs {} parameters for Wn'.format(num_elements))
                return

            print(self.config_dict['Wn'])

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()

    sys.exit(app.exec_())
