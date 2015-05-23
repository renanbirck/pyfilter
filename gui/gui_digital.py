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

from engine import digital
from engine import utils
from math import pi
from numpy import log10, abs, angle, unwrap

import gui_common
import canvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
BAND_MESSAGE = """ For the bandpass and bandstop cases,
                give 2 frequencies separated by space,
                like: 1 10, otherwise give one frequency."""


class StartQT4(QtGui.QMainWindow):
    common = None
    config_dict = {}
    filter_data = {}
    file_names = []

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
        QtCore.QObject.connect(self.ui.pushButton_WriteToFile,
                               QtCore.SIGNAL("clicked()"),
                               self.write_plots_to_file)
        QtCore.QObject.connect(self.ui.tabWidget,
                               QtCore.SIGNAL("tabCloseRequested(int)"),
                               self.destroy_tab)

        self.pick_widgets_for_filter_type()
        self.populate_window_list()
        self.FIR_setup()
        self.configure_boxes_for_design_parameters()
        self.get_filter_TF()
        self.get_filter_type()


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
            self.validate_common()
            if self.config_dict['filter_IR'] == 'IIR':
                self.validate_IIR()
                self.build_IIR_struct()
                self.actually_design_IIR_filter()
            elif self.config_dict['filter_IR'] == 'FIR':
                self.validate_FIR()
                self.build_FIR_struct()
                self.actually_design_FIR_filter()

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

    def validate_common(self):
        """ Validate the inputs that are used
            for both FIR and IIR filter designs. """
        try:
            sample_rate = float(self.ui.textEdit_SampleRate.toPlainText())
            if sample_rate <= 0:
                raise ValueError("must be positive")
        except:
            raise ValueError("Sample rate must be positive.")

        self.config_dict['sample_rate'] = sample_rate

    def validate_IIR(self):
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

    def validate_FIR(self):
        raise NotImplementedError("validate_FIR not made yet.")

    def build_IIR_struct(self):
        config = {}
        def build_struct_common():
            if self.config_dict['filter_TF'] == "butterworth":
                self.filter_design = digital.ButterworthFilter()
            elif self.config_dict['filter_TF'] == "chebyshev_1":
                self.filter_design = digital.ChebyshevIFilter()
            elif self.config_dict['filter_TF'] == "chebyshev_2":
                self.filter_design = digital.ChebyshevIIFilter()
            elif self.config_dict['filter_TF'] == "bessel":
                self.filter_design = digital.BesselFilter()
            elif self.config_dict['filter_TF'] == "elliptical":
                self.filter_design = digital.EllipticFilter()
            else:  # Should never happen, but... you never know.
                raise ValueError("Unknown filter type requested!!")
            self.filter_design.sample_rate = 2*pi*self.config_dict['sample_rate']

        def build_struct_n_wn():
            """ Builds the data structure for filter given the N, Wn. """
            self.filter_design.N = self.filter_data['N']
            self.filter_design.Wn = self.filter_data['Wn']
            self.filter_design.filter_kind = self.config_dict['filter_type']
            if hasattr(self.filter_design, "ripple"):
                self.filter_design.ripple = self.filter_data['ripple']
            if hasattr(self.filter_design, "stopband_attenuation"):
                self.filter_design.stopband_attenuation = self.filter_data['stopband_attenuation']

        def build_struct_specs():
            """ Builds the data structure for filter given the specifications. """

            if 'band' in self.config_dict['filter_type']:
                config['passband_frequency'] = list(map(float, self.filter_data['passband_frequency']))
                config['stopband_frequency'] = list(map(float, self.filter_data['stopband_frequency']))
            else:
                config['passband_frequency'] = float(self.filter_data['passband_frequency'])
                config['stopband_frequency'] = float(self.filter_data['stopband_frequency'])

            if self.config_dict['filter_type'] == "highpass": # The object model requires this.
                config['passband_frequency'] = float(self.filter_data['stopband_frequency'])
                config['stopband_frequency'] = float(self.filter_data['passband_frequency'])

            config['passband_attenuation'] = float(self.filter_data['passband_attenuation'])
            config['stopband_attenuation'] = float(self.filter_data['stopband_attenuation'])

            if hasattr(self.filter_design, "ripple"):
                self.filter_design.ripple = self.filter_data['ripple']
            if hasattr(self.filter_design, "stopband_attenuation"):
                self.filter_design.stopband_attenuation = float(self.filter_data['stopband_attenuation'])
            if hasattr(self.filter_design, "target"):
                if self.ui.radioButton_matchPB.isChecked():
                    self.filter_design.target = 'passband'
                elif self.ui.radioButton_matchSB.isChecked():
                    self.filter_design.target = 'stopband'
                else:
                    raise NotImplementedError("WHAT? Target is not passband or stopband?")

            self.filter_design.set_parameters(config)
            self.filter_design.compute_parameters()

            print("You asked for", self.config_dict['filter_type'],
                  " you got ", self.filter_design.filter_kind)
            if self.config_dict['filter_type'] != self.filter_design.filter_kind:
                print("You didn't get what you asked for. This means a bug. Report.")
                raise SystemError("Filter asked is not filter got!")

        build_struct_common()
        if self.config_dict['mode'] == "N_WN":
            build_struct_n_wn()
        elif self.config_dict['mode'] == "specs":
            build_struct_specs()

    def actually_design_IIR_filter(self):
        """ Where the actual design happens. """
        print("-------------------------")
        print("Begin design.")
        self.filter_design.design()
        print("Design finished.")
        print("Z: ", self.filter_design.Z)
        print("P: ", self.filter_design.P)
        print("K: ", self.filter_design.K)
        print("B: ", self.filter_design.B)
        print("A: ", self.filter_design.A)
        print("-------------------------")

    def report(self):
        self.ui.pushButton_saveToFile.setEnabled(True)
        html = utils.HTMLReport()
        html.put_text("<body bgcolor=\"white\">")
        html.put_text("Transfer function: ")
        html.put_newline()
        html.put_polynomial(self.filter_design.B,
                            self.filter_design.A,
                            variable='s')

        html.put_text("Coefficients:")

        len_B = len(self.filter_design.B)
        len_A = len(self.filter_design.A)
        pad_len = abs(len_B - len_A)

        padded_B = [0] * pad_len
        print("need to pad with ", pad_len)

        for element in self.filter_design.B:
            padded_B.append(element)

        print("after padding, B became ", padded_B)

        len_order = max(len_B, len_A)
        coeffs = list(reversed(range(0, len_order+1)))
        coeffs = list(map(lambda x: x-1, coeffs))

        # Keep track of the file names we've used for the reports,
        # then at the end of the program we can delete 'em.
        self.file_names.append(html.output.name)
        url = QtCore.QUrl(html.output.name)

        columns = ['', 'B (num)', 'A (den)']
        data = [coeffs,
                padded_B,
                self.filter_design.A]
        html.put_newline()
        html.put_table(columns, data)
        html.put_text("</body>")
        html.write(close=True)
        self.ui.tfOutputHTML.load(url)

    def plot(self):
        self.filter_design.compute_frequencies(N=1000)
        #self.ui.graphicsView.hide()
        #self.ui.graphicsView_2.hide()
        #self.ui.tab_plot.hide()

        # Build the tab used for plotting.
        sample_rate = 2*pi*self.config_dict['sample_rate']

        plot_tab = QtGui.QWidget()
        plot_tab_layout = QtGui.QVBoxLayout()
        plot_tab_splitter = QtGui.QSplitter()
        plot_tab_splitter.setOrientation(QtCore.Qt.Vertical)
        plot_tab.setLayout(plot_tab_layout)

        self.ui.tabWidget.addTab(plot_tab, "Frequency Response")

        plot_tab_layout.addWidget(plot_tab_splitter)

        self.ui.magnitudePlotWidget = canvas.StaticPlot(plot_tab_splitter, width=9,
                                                        height=6, dpi=80)

        nyquist = self.config_dict['sample_rate']
        W_Hz = nyquist*(self.filter_design.W / pi)
        self.ui.magnitudePlotWidget.compute_initial_figure(W_Hz,
                                                           20 * log10(abs(self.filter_design.H)),
                                                           mode="logx")
        self.ui.magnitudePlotWidget.set_label("Frequency (Hz)", "Gain (dB)")

        if isinstance(self.filter_design.Wn, float):
            self.ui.magnitudePlotWidget.add_line('x', self.filter_design.Wn / (2*pi))
        else:
            for value in self.filter_design.Wn:
                self.ui.magnitudePlotWidget.add_line('x', value / (2*pi))

        self.ui.magnitudeGraphToolbar = NavigationToolbar(self.ui.magnitudePlotWidget,
                                                          self)
        plot_tab_splitter.addWidget(self.ui.magnitudeGraphToolbar)

        self.ui.phasePlotWidget = canvas.StaticPlot(plot_tab_splitter, width=9,
                                                    height=6, dpi=80)
        self.ui.phasePlotWidget.compute_initial_figure(W_Hz,
                                                       unwrap(angle(self.filter_design.H)) * 180/pi,
                                                       mode="logx")
        self.ui.phasePlotWidget.set_label("Frequency (Hz)", "Phase (°)")
        self.ui.phaseGraphToolbar = NavigationToolbar(self.ui.phasePlotWidget,
                                                      self)
        plot_tab_splitter.addWidget(self.ui.phaseGraphToolbar)

    def write_plots_to_file(self):
        save_dialog = QtGui.QFileDialog()
        file_name_to_save = save_dialog.getSaveFileName(self, "Save plots...", "",
                                                        "Images (*.png *.jpg *.svg)")
        if file_name_to_save:
            self.ui.magnitudePlotWidget.dump(file_name_to_save)

    def build_FIR_struct(self):
        raise NotImplementedError("build_FIR_struct not made yet.")

    def destroy_tab(self, tab_id):
        if tab_id == 0:
            return # The results tab shall not close.
        self.ui.tabWidget.removeTab(tab_id)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()

    sys.exit(app.exec_())
