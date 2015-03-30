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

from engine import analog
from math import pi


class StartQT4(QtGui.QMainWindow):

    BAND_MESSAGE = """ For the bandpass and bandstop cases,
    give 2 frequencies separated by space,
    like: 1 10, otherwise give one frequency."""

    config_dict = {}  # The dictionary of configuration
                      # used by the validation routines.

    analog_filter = analog.AnalogFilter()
    N = 0
    Wn = 0

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
            # configure the ripple.
            self.ui.label_pbRipple.setEnabled(True)
            self.ui.label_pbRipple.setText("Passband\n ripple (dB): ")
            self.ui.plainTextEdit_pbRipple.setEnabled(True)
        elif choice == "chebyshev_2":
            self.ui.label_pbRipple.setEnabled(False)
            self.ui.label_sbAtt.setEnabled(True)
            self.ui.plainTextEdit_pbRipple.setEnabled(False)
            self.ui.plainTextEdit_sbAtt.setEnabled(True)
        elif choice == "elliptical":
            self.ui.label_pbRipple.setEnabled(True)
            self.ui.label_sbAtt.setEnabled(True)
            self.ui.plainTextEdit_pbRipple.setEnabled(True)
            self.ui.plainTextEdit_sbAtt.setEnabled(True)
        else:  # Bessel, Butterworth
            self.ui.label_pbRipple.setEnabled(False)
            self.ui.plainTextEdit_pbRipple.setEnabled(False)
            self.ui.label_sbAtt.setEnabled(False)
            self.ui.plainTextEdit_sbAtt.setEnabled(False)

    def design_filter(self):
        try:
            self.validate_inputs()
            self.build_struct()
            self.actually_design_filter()
        except ValueError as val:
            critical(self, 'Error', str(val))
            print(traceback.format_exc())
            return

    def validate_inputs(self):
        print("Filter type is ", self.config_dict['filter_type'])
        print("Filter TF is ", self.config_dict['filter_TF'])
        Fpass = 0
        Fstop = 0

        if self.config_dict['filter_TF'] == 'butterworth':
            if self.ui.radioButton_matchPB.isChecked():
                self.config_dict['target'] = 'passband'
            elif self.ui.radioButton_matchSB.isChecked():
                self.config_dict['target'] = 'stopband'
            else:
                raise ValueError("WHAT? This is impossible.")

        if self.config_dict['filter_TF'] == 'elliptical':
            print("aqui")
            try:
                ripple = float(self.ui.plainTextEdit_pbRipple.toPlainText())
                attenuation = float(self.ui.plainTextEdit_sbAtt.toPlainText())
                if ripple <= 0 or attenuation <= 0:
                    raise ValueError("Bad value.")
                self.config_dict['ripple'] = ripple
                self.config_dict['attenuation'] = attenuation
            except:
                raise ValueError(""" For the elliptical filter,
                the ripple and the attenuation must
                be positive and not zero. """)

        if self.config_dict['filter_TF'] == 'chebyshev_1':
            try:
                ripple = float(self.ui.plainTextEdit_pbRipple.toPlainText())
                if ripple <= 0:
                    raise ValueError("Bad value.")
                self.config_dict['ripple'] = ripple
            except:
                raise ValueError("""For the Chebyshev type1 and
                the elliptical filters,
                the ripple must be positive and not zero. """)

        if self.config_dict['filter_TF'] == 'chebyshev_2':
            try:
                attenuation = float(self.ui.plainTextEdit_sbAtt.toPlainText())
                if attenuation <= 0:
                    raise ValueError("Bad value.")
                self.config_dict['attenuation'] = attenuation
            except:
                raise ValueError("""For the Chebyshev type2 and
                the elliptical filters,
                the stopband attenuation must be positive and not zero. """)

        if 'band' in self.config_dict['filter_type']:
            num_elements = 2  # bandstop, bandpass
        else:
            num_elements = 1

        if self.config_dict['mode'] == "N_WN":
            try:
                N = int(self.ui.plainTextEdit_opt1.toPlainText())
                if N <= 0:
                    raise ValueError("N must be integer >= 0.")
            except:
                raise ValueError("N must be integer >= 0.")

            self.N = N

            try:
                Wn = list(map(float, self.ui.plainTextEdit_opt2.toPlainText().split(' ')))
                if len(Wn) != num_elements:
                    raise ValueError("Wrong number of elements.")
            except:
                raise ValueError("Wn must be {} number{}.".format(num_elements, plural(num_elements)))

            if num_elements == 1:
                self.Wn = Wn[0]
            else:
                self.Wn = Wn

            print(">> N = {}, Wn = {}".format(self.N, self.Wn))

        elif self.config_dict['mode'] == "specs":
            try:
                Fpass = list(map(float, self.ui.plainTextEdit_opt1.toPlainText().split(' ')))
                Fstop = list(map(float, self.ui.plainTextEdit_opt2.toPlainText().split(' ')))
                if len(Fstop) != num_elements or len(Fpass) != num_elements:
                    raise ValueError("Wrong number of elements.")
            except:
                raise ValueError("Fpass and Fstop must be {} number{}.".format(num_elements,
                                                                               plural(num_elements)))

            # After converting the inputs to numbers, validation them

            if num_elements == 1:
                Fpass = Fpass[0]
                Fstop = Fstop[0]
                if Fpass <= 0 or Fstop <= 0:
                    raise ValueError("Both frequencies must be positive.")
            else:
                if Fpass[0] <= 0 or Fstop[0] <= 0 or Fpass[1] <= 0 or Fstop[1] <= 0:
                    raise ValueError("All frequencies must be positive.")

            # Special case for the bandpass and bandstop-filters.

            if num_elements == 2:
                pb0, pb1 = Fpass[0], Fpass[1]
                sb0, sb1 = Fstop[0], Fstop[1]

                if not ((pb0 > sb0 and pb1 < sb1)
                        or (pb0 < sb0 and pb1 > sb1)):
                    raise ValueError("""Parameters for bandpass/bandstop \
                                     are invalid. """)
            try:
                Apass = float(self.ui.plainTextEdit_opt3.toPlainText())
                Astop = float(self.ui.plainTextEdit_opt4.toPlainText())
                if Apass < 0 or Astop < 0:
                    raise ValueError("not positive")
            except:
                raise ValueError("Both attenuations should be positive number.")

            self.config_dict['passband_frequency'] = Fpass
            self.config_dict['stopband_frequency'] = Fstop
            self.config_dict['passband_attenuation'] = Apass
            self.config_dict['stopband_attenuation'] = Astop

    def build_struct(self):
        # Build the filter structure.

        if self.config_dict['mode'] == "N_WN":  # Direct (doesn't need any configurations)
            self.analog_filter.filter_class = self.config_dict['filter_TF']
            self.analog_filter.filter_type = self.config_dict['filter_type']
            self.analog_filter.N = self.N
            if isinstance(self.Wn, list):
                self.analog_filter.Wn = list(map(lambda x: 2 * pi * x, self.Wn))
            else:
                self.analog_filter.Wn = 2 * pi * self.Wn
            return  # We're done here, now go on to design filter.
        else:
            filter_configs = {}
            filter_configs['passband_frequency'] = self.config_dict['passband_frequency']
            filter_configs['stopband_frequency'] = self.config_dict['stopband_frequency']
            filter_configs['passband_attenuation'] = self.config_dict['passband_attenuation']
            filter_configs['stopband_attenuation'] = self.config_dict['stopband_attenuation']

            # scipy.signal functions want PB and SB swapped in the highpass case.

            if self.analog_filter.filter_type == 'highpass':
                pb = filter_configs['passband_frequency']
                sb = filter_configs['stopband_frequency']
                filter_configs['passband_frequency'] = sb
                filter_configs['stopband_frequency'] = pb

            self.analog_filter.configure_filter(filter_configs)
            if self.config_dict['filter_type'] == 'butterworth':
                self.analog_filter.compute_parameters(target=self.config_dict['target'])
            else:
                self.analog_filter.compute_parameters()

    def actually_design_filter(self):
        print(self.analog_filter.N)
        print(self.analog_filter.Wn)
        print("The filter type is", self.analog_filter.filter_type)
        print("The filter TF is", self.analog_filter.filter_class)

        print("Begin filter design")
        if self.analog_filter.filter_class == 'chebyshev_1':
            self.analog_filter.design(ripple=self.config_dict['ripple'])
        elif self.analog_filter.filter_class == 'chebyshev_2':
            self.analog_filter.stopband_attenuation = float(self.config_dict['attenuation'])
            self.analog_filter.design()
        elif self.analog_filter.filter_class == 'elliptical':
            self.analog_filter.passband_attenuation = float(self.config_dict['ripple'])
            self.analog_filter.stopband_attenuation = float(self.config_dict['attenuation'])
            print("Rp = ", self.analog_filter.passband_attenuation, self.config_dict['ripple'])
            print("Rs = ", self.analog_filter.stopband_attenuation, self.config_dict['attenuation'])
            self.analog_filter.design()
        else:  # Bessel, Butterworth
            self.analog_filter.design()
        print("Filter design finished.")

        print("The order is ", self.analog_filter.N, ".")
        print("The natural freq is ", self.analog_filter.Wn, ".")
        print("B = ", self.analog_filter.B)
        print("A = ", self.analog_filter.A)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()

    sys.exit(app.exec_())
