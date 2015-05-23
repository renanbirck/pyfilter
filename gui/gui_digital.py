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
BAND_MESSAGE = """ For the bandpass and bandstop cases,
                give 2 frequencies separated by space,
                like: 1 10, otherwise give one frequency."""


class StartQT4(QtGui.QMainWindow):
    common = None
    config_dict = {}

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

        for FIR_mode_widget in [self.ui.radioButton_Parks,
                                self.ui.radioButton_Window]:
            QtCore.QObject.connect(FIR_mode_widget,
                                   QtCore.SIGNAL("clicked()"),
                                   self.FIR_setup)

        for designParametersWidget in [self.ui.radioButton_NWn,
                                       self.ui.radioButton_AttSpecs]:
            QtCore.QObject.connect(designParametersWidget,
                                   QtCore.SIGNAL("clicked()"),
                                   self.configure_boxes_for_design_parameters)

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

        QtCore.QObject.connect(self.ui.pushButton_addItem,
                               QtCore.SIGNAL("clicked()"),
                               self.add_fir_param)
        QtCore.QObject.connect(self.ui.pushButton_removeItem,
                               QtCore.SIGNAL("clicked()"),
                               self.delete_fir_param)
        QtCore.QObject.connect(self.ui.pushButton_Design,
                               QtCore.SIGNAL("clicked()"),
                               self.design_filter)

        self.pick_widgets_for_filter_type()
        self.populate_window_list()
        self.FIR_setup()
        self.configure_boxes_for_design_parameters()

    def FIR_setup(self):
        self.ui.tableWidget_FIR.setColumnCount(2)
        if self.ui.radioButton_Parks.isChecked():
            self.ui.tableWidget_FIR.setHorizontalHeaderLabels(["Band", "Gain"])
            self.ui.comboBox_Window.setEnabled(False)
        elif self.ui.radioButton_Window.isChecked():
            self.ui.tableWidget_FIR.setHorizontalHeaderLabels(["Freq", "Gain"])
            self.ui.comboBox_Window.setEnabled(True)
        else:
            pass


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
            self.ui.stackedWidget_filterSpecs.setCurrentIndex(0)
            self.ui.groupBox_Filter_Type.show()
            self.ui.groupBox_paramCalc.show()
            self.config_dict['filter_IR'] = "IIR"
        elif self.ui.radioButton_FIR.isChecked():
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.stackedWidget_filterSpecs.setCurrentIndex(1)
            self.ui.groupBox_Filter_Type.hide()
            self.ui.groupBox_paramCalc.hide()
            self.config_dict['filter_IR'] = "FIR"
        else:  # Should not happen...
            pass

    def add_fir_param(self):
        rows = self.ui.tableWidget_FIR.rowCount()
        self.ui.tableWidget_FIR.setRowCount(rows + 1)

    def delete_fir_param(self):
        picked = self.ui.tableWidget_FIR.currentRow()
        rows = self.ui.tableWidget_FIR.rowCount()
        print("picked ", picked)
        self.ui.tableWidget_FIR.removeRow(picked)

    def configure_boxes_for_design_parameters(self):

        if self.config_dict['filter_IR'] == 'FIR':
            return

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
            self.ui.plainTextEdit_opt2.setToolTip("The natural frequency(ies). \n" + BAND_MESSAGE)

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

            self.ui.plainTextEdit_opt1.setToolTip("The passband frequency(ies), in hertz. " + BAND_MESSAGE)
            self.ui.plainTextEdit_opt2.setToolTip("The stop frequency(ies), in hertz." + BAND_MESSAGE)
            self.ui.plainTextEdit_opt3.setToolTip("The attenuation at passband, in dB.")
            self.ui.plainTextEdit_opt4.setToolTip("The attenuation at stopband, in dB.")
            self.config_dict['mode'] = "specs"

        else:
            raise ValueError("Somehow we chose something that can't be chosen!")

    def get_filter_TF(self):
        """ This function gets the appropriate filter transfer-fucntion from
            the chosen options and configures the other radio buttons
            and controls accordingly. """

        if self.config_dict['filter_IR'] == 'FIR':
            return

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
            if self.config_dict['filter_IR'] == 'IIR':
                self.validate_IIR()
                self.build_IIR_struct()
            elif self.config_dict['filter_IR'] == 'FIR':
                self.validate_FIR()
                self.build_FIR_struct()
            self.actually_design_filter()
            self.report()
            self.plot()
        except Exception as went_wrong:
            critical(self, 'Error', str(went_wrong))
            print("Internal error happened! Please report the traceback to the developer.")
            print("The traceback is: ")
            print("---------------------------")
            print(traceback.format_exc())
            print("---------------------------")
            return


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()

    sys.exit(app.exec_())
