#!/usr/bin/env python3
# coding: utf-8

# pyfilter: a filter synthesis tool written in the Python language.
# (c) 2015 Renan Birck <renan.ee.ufsm@gmail.com>

# This is the main file for the GUI.

import sys, traceback
from PyQt4 import QtCore, QtGui
from pyfilter_main_window import Ui_MainWindow
from PyQt4.QtGui import QMessageBox

# Aliases and other useful functions
critical = QMessageBox.critical
information = QMessageBox.information
warning = QMessageBox.information
question = QMessageBox.question
plural = lambda n: 's' if n > 1 else ''

sys.path.append('../engine')
sys.path.append('..')

from engine import analog_new as analog
from math import pi


class StartQT4(QtGui.QMainWindow):

    BAND_MESSAGE = """ For the bandpass and bandstop cases,
    give 2 frequencies separated by space,
    like: 1 10, otherwise give one frequency."""

    config_dict = {}  # The dictionary of configuration
                      # used by the validation routines.
    filter_data = {}

    N = 0
    Wn = None
    ripple = 0
    passband_frequency = None
    stopband_frequency = None
    passband_attenuation = 0
    stopband_attenuation = 0

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
        information(self, 'About PyFilter...',
                    'PyFilter 0.1 (c) 2015 Renan Birck.')

    def configure_boxes_for_design_parameters(self):
        """ This function configure the text boxes
        for the chosen design parameters. """
        if self.ui.radioButton_NWn.isChecked():
            self.ui.label_opt1.setText("N: ")
            self.ui.label_opt2.setText("Freq. (Hz): ")
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
            self.ui.label_opt3.setText("Apass (dB): ")
            self.ui.label_opt4.setText("Astop (dB): ")
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
            print("pick chebyshev_1")
            choice = "chebyshev_1"
        elif self.ui.radioButton_Cheby2.isChecked():
            print("pick chebyshev_2")
            choice = "chebyshev_2"
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
            warning(self, '', 'The allpass is not made yet.')
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

        if choice == "chebyshev_1":
            # Chebyshev type-1 filter needs to have the option to
            # configure the ripple in both modes.
            self.ui.label_pbRipple.setEnabled(True)
            self.ui.label_pbRipple.setText("Passband\n ripple (dB): ")
            self.ui.plainTextEdit_pbRipple.setEnabled(True)

        elif choice == "elliptical":
            # The elliptical needs to have the both options.
            self.ui.label_pbRipple.setEnabled(True)
            self.ui.plainTextEdit_pbRipple.setEnabled(True)

        else:  # Bessel, Butterworth
            self.ui.label_pbRipple.setEnabled(False)
            self.ui.plainTextEdit_pbRipple.setEnabled(False)

        if self.config_dict['mode'] == "N_WN":
            if choice in ['chebyshev_2', 'elliptical']:
                self.ui.label_opt4.setEnabled(True)
                self.ui.label_opt4.setText("Astop (dB):")
                self.ui.label_opt4.show()
                self.ui.plainTextEdit_opt4.show()
            else:
                self.ui.label_opt4.hide()
                self.ui.plainTextEdit_opt4.hide()


    def design_filter(self):
        try:
            self.validate_inputs()
            self.build_struct()
            self.actually_design_filter()
        except Exception as went_wrong:
            critical(self, 'Error', str(went_wrong))
            print("Internal error happened! Please report the traceback to the developer.")
            print("The traceback is: ")
            print("---------------------------")
            print(traceback.format_exc())
            print("---------------------------")
            return

    def validate_inputs(self):

        def validate_common():
            if self.config_dict['filter_TF'] in ['bessel', 'butterworth']:
                return # not needed to enter here

            if self.config_dict['filter_TF'] in ['elliptical', 'chebyshev_2']:
                # Needs stopband attenuation
                stopband_attenuation = self.ui.plainTextEdit_opt4.toPlainText()
                try:
                    stopband_attenuation = float(stopband_attenuation)
                    if stopband_attenuation <= 0:
                        raise ValueError("must be positive")
                except:
                    raise ValueError("Stopband attenuation must be positive.")
                self.filter_data['stopband_attenuation'] = stopband_attenuation
                print(">> Stopband attenuation (dB): ", stopband_attenuation)

            if self.config_dict['filter_TF'] in ['elliptical', 'chebyshev_1']:
                ripple = self.ui.plainTextEdit_pbRipple.toPlainText()
                try:
                    ripple = float(ripple)
                    if ripple <= 0:
                        raise ValueError("must be positive")
                except:
                    raise ValueError("Ripple must be positive.")
                self.filter_data['ripple'] = ripple
                print(">> Ripple (dB): ", ripple)

        def validate_n_wn():
            N = self.ui.plainTextEdit_opt1.toPlainText()
            try:
                N = int(N)
                if N <= 0 or N > 500:
                    raise ValueError("out of range")
            except:
                raise ValueError("Filter order must be between 0 and 500.")
            pass
            self.filter_data['N'] = N
            print(">> N: ", self.filter_data['N'])

            # Validate Wn
            Wn = self.ui.plainTextEdit_opt2.toPlainText()
            if 'band' in self.config_dict['filter_type']:
                try:
                    Wn = Wn.split(' ')[0:2]
                    Wn = [2 * pi * float(Wn[0]), 2 * pi * float(Wn[1])]
                except:
                    raise ValueError("Needs two parameters for Wn.")
            else:
                try:
                    Wn = Wn.split(' ')[0]
                    Wn = 2 * pi * float(Wn)
                    if Wn <= 0:
                        raise ValueError("Wn must be positive.")
                except:
                    raise ValueError("Wn must be a positive number.")
            self.filter_data['Wn'] = Wn

            print(">> Wn: ", self.filter_data['Wn'])

        def validate_specs():
            Wp = self.ui.plainTextEdit_opt1.toPlainText()
            Ws = self.ui.plainTextEdit_opt2.toPlainText()
            Rp = self.ui.plainTextEdit_opt3.toPlainText()
            Rs = self.ui.plainTextEdit_opt4.toPlainText()

            if 'band' in self.config_dict['filter_type']:
                try:
                    print(Wp, Ws)
                    Wp = Wp.split(' ')
                    Ws = Ws.split(' ')
                    Wp = [float(Wp[0]), float(Wp[1])]
                    Ws = [float(Ws[0]), float(Ws[1])]
                    if Wp[0] <= 0 or Ws[0] <= 0 or Wp[1] <= 0 or Ws[1] <= 0:
                        raise ValueError("must be positive.")
                except:
                    raise ValueError("Both Wp and Ws need 2 positive parameters.")
            else:
                try:
                    Wp = float(Wp)
                    Ws = float(Ws)
                    if Wp <= 0 or Ws <= 0:
                        raise ValueError("must be positive.")
                except:
                    raise ValueError("Both Wp and Ws must be positive.")

            # Validate according to filter type chosen.

            if 'band' in self.config_dict['filter_type']:
                pb0, pb1, sb0, sb1 = Wp[0], Wp[1], Ws[0], Ws[1]
                if self.config_dict['filter_type'] == 'bandpass':
                    if not (pb0 > sb0 and pb1 < sb1):
                        raise ValueError("The bandpass filter needs that the passband "
                                         "be inside the stopband.")
                elif self.config_dict['filter_type'] == 'bandstop':
                    if not (pb0 < sb0 and pb1 > sb1):
                        raise ValueError("The bandstop filter needs that the stopband "
                                         "be inside the passband.")
            self.filter_data['passband_frequency'] = Wp
            self.filter_data['stopband_frequency'] = Ws
            self.filter_data['passband_attenuation'] = Rp
            self.filter_data['stopband_attenuation'] = Rs

        validate_common()
        if self.config_dict['mode'] == "N_WN":
            validate_n_wn()
        elif self.config_dict['mode'] == "specs":
            validate_specs()

    def build_struct(self):
        raise NotImplementedError("build_struct() not implemented yet.")

    def actually_design_filter(self):
        raise NotImplementedError("actually_design_filter() not implemented yet.")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()

    sys.exit(app.exec_())
