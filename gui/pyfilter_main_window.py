# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyfilter_main_window.ui'
#
# Created: Thu Mar 19 20:54:38 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(1121, 806)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tabWidget = QtGui.QTabWidget(self.splitter)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_TF = QtGui.QWidget()
        self.tab_TF.setObjectName(_fromUtf8("tab_TF"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab_TF)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tfOutputHTML = QtWebKit.QWebView(self.tab_TF)
        self.tfOutputHTML.setUrl(QtCore.QUrl(_fromUtf8("file:///mnt/dados/Insync/Insync (e-mail pessoal)/Arquivos/Sources/pyfilter_TCC/gui/data/result_template.html")))
        self.tfOutputHTML.setObjectName(_fromUtf8("tfOutputHTML"))
        self.verticalLayout_2.addWidget(self.tfOutputHTML)
        self.tabWidget.addTab(self.tab_TF, _fromUtf8(""))
        self.tab_plot = QtGui.QWidget()
        self.tab_plot.setObjectName(_fromUtf8("tab_plot"))
        self.gridLayout = QtGui.QGridLayout(self.tab_plot)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter_2 = QtGui.QSplitter(self.tab_plot)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.graphicsView = QtGui.QGraphicsView(self.splitter_2)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.graphicsView_2 = QtGui.QGraphicsView(self.splitter_2)
        self.graphicsView_2.setObjectName(_fromUtf8("graphicsView_2"))
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_plot, _fromUtf8(""))
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1121, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.configurationsDock = QtGui.QDockWidget(MainWindow)
        self.configurationsDock.setMinimumSize(QtCore.QSize(380, 41))
        self.configurationsDock.setObjectName(_fromUtf8("configurationsDock"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.pushButton_Design = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_Design.setGeometry(QtCore.QRect(20, 360, 85, 26))
        self.pushButton_Design.setObjectName(_fromUtf8("pushButton_Design"))
        self.groupBox_FilterSpecs = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox_FilterSpecs.setGeometry(QtCore.QRect(160, 70, 221, 171))
        self.groupBox_FilterSpecs.setObjectName(_fromUtf8("groupBox_FilterSpecs"))
        self.label_opt1 = QtGui.QLabel(self.groupBox_FilterSpecs)
        self.label_opt1.setGeometry(QtCore.QRect(0, 20, 71, 20))
        self.label_opt1.setObjectName(_fromUtf8("label_opt1"))
        self.label_opt2 = QtGui.QLabel(self.groupBox_FilterSpecs)
        self.label_opt2.setGeometry(QtCore.QRect(0, 60, 71, 20))
        self.label_opt2.setObjectName(_fromUtf8("label_opt2"))
        self.plainTextEdit_opt1 = QtGui.QPlainTextEdit(self.groupBox_FilterSpecs)
        self.plainTextEdit_opt1.setGeometry(QtCore.QRect(90, 20, 121, 31))
        self.plainTextEdit_opt1.setTabChangesFocus(True)
        self.plainTextEdit_opt1.setObjectName(_fromUtf8("plainTextEdit_opt1"))
        self.plainTextEdit_opt2 = QtGui.QPlainTextEdit(self.groupBox_FilterSpecs)
        self.plainTextEdit_opt2.setGeometry(QtCore.QRect(90, 60, 121, 31))
        self.plainTextEdit_opt2.setTabChangesFocus(True)
        self.plainTextEdit_opt2.setObjectName(_fromUtf8("plainTextEdit_opt2"))
        self.label_opt3 = QtGui.QLabel(self.groupBox_FilterSpecs)
        self.label_opt3.setGeometry(QtCore.QRect(0, 90, 81, 41))
        self.label_opt3.setObjectName(_fromUtf8("label_opt3"))
        self.plainTextEdit_opt3 = QtGui.QPlainTextEdit(self.groupBox_FilterSpecs)
        self.plainTextEdit_opt3.setGeometry(QtCore.QRect(90, 100, 121, 31))
        self.plainTextEdit_opt3.setTabChangesFocus(True)
        self.plainTextEdit_opt3.setObjectName(_fromUtf8("plainTextEdit_opt3"))
        self.label_opt4 = QtGui.QLabel(self.groupBox_FilterSpecs)
        self.label_opt4.setGeometry(QtCore.QRect(0, 140, 71, 20))
        self.label_opt4.setObjectName(_fromUtf8("label_opt4"))
        self.plainTextEdit_opt4 = QtGui.QPlainTextEdit(self.groupBox_FilterSpecs)
        self.plainTextEdit_opt4.setGeometry(QtCore.QRect(90, 140, 121, 31))
        self.plainTextEdit_opt4.setTabChangesFocus(True)
        self.plainTextEdit_opt4.setObjectName(_fromUtf8("plainTextEdit_opt4"))
        self.groupBox_Filter_Type = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox_Filter_Type.setGeometry(QtCore.QRect(10, 210, 171, 131))
        self.groupBox_Filter_Type.setObjectName(_fromUtf8("groupBox_Filter_Type"))
        self.radioButton_LP = QtGui.QRadioButton(self.groupBox_Filter_Type)
        self.radioButton_LP.setGeometry(QtCore.QRect(0, 20, 104, 21))
        self.radioButton_LP.setChecked(True)
        self.radioButton_LP.setObjectName(_fromUtf8("radioButton_LP"))
        self.radioButton_HP = QtGui.QRadioButton(self.groupBox_Filter_Type)
        self.radioButton_HP.setGeometry(QtCore.QRect(0, 40, 104, 21))
        self.radioButton_HP.setObjectName(_fromUtf8("radioButton_HP"))
        self.radioButton_BP = QtGui.QRadioButton(self.groupBox_Filter_Type)
        self.radioButton_BP.setGeometry(QtCore.QRect(0, 60, 104, 21))
        self.radioButton_BP.setObjectName(_fromUtf8("radioButton_BP"))
        self.radioButton_BS = QtGui.QRadioButton(self.groupBox_Filter_Type)
        self.radioButton_BS.setGeometry(QtCore.QRect(0, 80, 104, 21))
        self.radioButton_BS.setObjectName(_fromUtf8("radioButton_BS"))
        self.radioButton_AP = QtGui.QRadioButton(self.groupBox_Filter_Type)
        self.radioButton_AP.setGeometry(QtCore.QRect(0, 100, 104, 21))
        self.radioButton_AP.setObjectName(_fromUtf8("radioButton_AP"))
        self.groupBox_Filter_Top = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox_Filter_Top.setGeometry(QtCore.QRect(10, 70, 191, 121))
        self.groupBox_Filter_Top.setObjectName(_fromUtf8("groupBox_Filter_Top"))
        self.radioButton_Butterworth = QtGui.QRadioButton(self.groupBox_Filter_Top)
        self.radioButton_Butterworth.setGeometry(QtCore.QRect(0, 40, 104, 21))
        self.radioButton_Butterworth.setObjectName(_fromUtf8("radioButton_Butterworth"))
        self.radioButton_Cheby1 = QtGui.QRadioButton(self.groupBox_Filter_Top)
        self.radioButton_Cheby1.setGeometry(QtCore.QRect(0, 60, 131, 21))
        self.radioButton_Cheby1.setObjectName(_fromUtf8("radioButton_Cheby1"))
        self.radioButton_Cheby2 = QtGui.QRadioButton(self.groupBox_Filter_Top)
        self.radioButton_Cheby2.setGeometry(QtCore.QRect(0, 80, 131, 21))
        self.radioButton_Cheby2.setObjectName(_fromUtf8("radioButton_Cheby2"))
        self.radioButton_Elliptical = QtGui.QRadioButton(self.groupBox_Filter_Top)
        self.radioButton_Elliptical.setGeometry(QtCore.QRect(0, 100, 104, 21))
        self.radioButton_Elliptical.setObjectName(_fromUtf8("radioButton_Elliptical"))
        self.radioButton_Bessel = QtGui.QRadioButton(self.groupBox_Filter_Top)
        self.radioButton_Bessel.setGeometry(QtCore.QRect(0, 20, 104, 21))
        self.radioButton_Bessel.setChecked(True)
        self.radioButton_Bessel.setObjectName(_fromUtf8("radioButton_Bessel"))
        self.groupBox_AD = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox_AD.setGeometry(QtCore.QRect(10, 0, 120, 80))
        self.groupBox_AD.setObjectName(_fromUtf8("groupBox_AD"))
        self.radioButton_Analog = QtGui.QRadioButton(self.groupBox_AD)
        self.radioButton_Analog.setGeometry(QtCore.QRect(0, 20, 104, 21))
        self.radioButton_Analog.setChecked(True)
        self.radioButton_Analog.setObjectName(_fromUtf8("radioButton_Analog"))
        self.radioButton_Digital = QtGui.QRadioButton(self.groupBox_AD)
        self.radioButton_Digital.setGeometry(QtCore.QRect(0, 40, 104, 21))
        self.radioButton_Digital.setObjectName(_fromUtf8("radioButton_Digital"))
        self.groupBox_Options = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox_Options.setGeometry(QtCore.QRect(155, 250, 181, 101))
        self.groupBox_Options.setObjectName(_fromUtf8("groupBox_Options"))
        self.radioButton_matchPB = QtGui.QRadioButton(self.groupBox_Options)
        self.radioButton_matchPB.setEnabled(False)
        self.radioButton_matchPB.setGeometry(QtCore.QRect(0, 20, 171, 21))
        self.radioButton_matchPB.setObjectName(_fromUtf8("radioButton_matchPB"))
        self.radioButton_matchSB = QtGui.QRadioButton(self.groupBox_Options)
        self.radioButton_matchSB.setEnabled(False)
        self.radioButton_matchSB.setGeometry(QtCore.QRect(0, 40, 141, 21))
        self.radioButton_matchSB.setObjectName(_fromUtf8("radioButton_matchSB"))
        self.label_pbRipple = QtGui.QLabel(self.groupBox_Options)
        self.label_pbRipple.setEnabled(False)
        self.label_pbRipple.setGeometry(QtCore.QRect(0, 60, 111, 31))
        self.label_pbRipple.setObjectName(_fromUtf8("label_pbRipple"))
        self.plainTextEdit_pbRipple = QtGui.QPlainTextEdit(self.groupBox_Options)
        self.plainTextEdit_pbRipple.setEnabled(False)
        self.plainTextEdit_pbRipple.setGeometry(QtCore.QRect(100, 60, 81, 31))
        self.plainTextEdit_pbRipple.setTabChangesFocus(True)
        self.plainTextEdit_pbRipple.setObjectName(_fromUtf8("plainTextEdit_pbRipple"))
        self.groupBox_paramCalc = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox_paramCalc.setGeometry(QtCore.QRect(155, 0, 211, 71))
        self.groupBox_paramCalc.setObjectName(_fromUtf8("groupBox_paramCalc"))
        self.radioButton_NWn = QtGui.QRadioButton(self.groupBox_paramCalc)
        self.radioButton_NWn.setGeometry(QtCore.QRect(0, 20, 104, 21))
        self.radioButton_NWn.setChecked(True)
        self.radioButton_NWn.setObjectName(_fromUtf8("radioButton_NWn"))
        self.radioButton_AttSpecs = QtGui.QRadioButton(self.groupBox_paramCalc)
        self.radioButton_AttSpecs.setGeometry(QtCore.QRect(0, 40, 171, 21))
        self.radioButton_AttSpecs.setObjectName(_fromUtf8("radioButton_AttSpecs"))
        self.configurationsDock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.configurationsDock)
        self.dockWidget_PlotOptions = QtGui.QDockWidget(MainWindow)
        self.dockWidget_PlotOptions.setObjectName(_fromUtf8("dockWidget_PlotOptions"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.label_2 = QtGui.QLabel(self.dockWidgetContents_2)
        self.label_2.setGeometry(QtCore.QRect(24, 138, 81, 10))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label = QtGui.QLabel(self.dockWidgetContents_2)
        self.label.setGeometry(QtCore.QRect(10, 100, 101, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.doubleSpinBox_Ymax = QtGui.QDoubleSpinBox(self.dockWidgetContents_2)
        self.doubleSpinBox_Ymax.setGeometry(QtCore.QRect(260, 50, 101, 25))
        self.doubleSpinBox_Ymax.setObjectName(_fromUtf8("doubleSpinBox_Ymax"))
        self.checkBox_Ydb = QtGui.QCheckBox(self.dockWidgetContents_2)
        self.checkBox_Ydb.setGeometry(QtCore.QRect(90, 50, 51, 21))
        self.checkBox_Ydb.setObjectName(_fromUtf8("checkBox_Ydb"))
        self.doubleSpinBox_Xmin = QtGui.QDoubleSpinBox(self.dockWidgetContents_2)
        self.doubleSpinBox_Xmin.setGeometry(QtCore.QRect(150, 20, 101, 25))
        self.doubleSpinBox_Xmin.setObjectName(_fromUtf8("doubleSpinBox_Xmin"))
        self.comboBox_backColor = QtGui.QComboBox(self.dockWidgetContents_2)
        self.comboBox_backColor.setGeometry(QtCore.QRect(90, 130, 161, 25))
        self.comboBox_backColor.setObjectName(_fromUtf8("comboBox_backColor"))
        self.doubleSpinBox_Ymin = QtGui.QDoubleSpinBox(self.dockWidgetContents_2)
        self.doubleSpinBox_Ymin.setGeometry(QtCore.QRect(150, 50, 101, 25))
        self.doubleSpinBox_Ymin.setObjectName(_fromUtf8("doubleSpinBox_Ymin"))
        self.checkBox_Xlog = QtGui.QCheckBox(self.dockWidgetContents_2)
        self.checkBox_Xlog.setGeometry(QtCore.QRect(90, 20, 51, 21))
        self.checkBox_Xlog.setObjectName(_fromUtf8("checkBox_Xlog"))
        self.doubleSpinBox_Xmax = QtGui.QDoubleSpinBox(self.dockWidgetContents_2)
        self.doubleSpinBox_Xmax.setGeometry(QtCore.QRect(260, 20, 101, 25))
        self.doubleSpinBox_Xmax.setObjectName(_fromUtf8("doubleSpinBox_Xmax"))
        self.label_4 = QtGui.QLabel(self.dockWidgetContents_2)
        self.label_4.setGeometry(QtCore.QRect(11, 51, 16, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.checkBox_Ygrid = QtGui.QCheckBox(self.dockWidgetContents_2)
        self.checkBox_Ygrid.setGeometry(QtCore.QRect(30, 50, 61, 21))
        self.checkBox_Ygrid.setObjectName(_fromUtf8("checkBox_Ygrid"))
        self.checkBox_Xgrid = QtGui.QCheckBox(self.dockWidgetContents_2)
        self.checkBox_Xgrid.setGeometry(QtCore.QRect(30, 20, 61, 21))
        self.checkBox_Xgrid.setObjectName(_fromUtf8("checkBox_Xgrid"))
        self.comboBox_frontColor = QtGui.QComboBox(self.dockWidgetContents_2)
        self.comboBox_frontColor.setGeometry(QtCore.QRect(90, 100, 161, 25))
        self.comboBox_frontColor.setObjectName(_fromUtf8("comboBox_frontColor"))
        self.label_3 = QtGui.QLabel(self.dockWidgetContents_2)
        self.label_3.setGeometry(QtCore.QRect(10, 16, 16, 30))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.pushButton_4 = QtGui.QPushButton(self.dockWidgetContents_2)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 180, 141, 26))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton = QtGui.QPushButton(self.dockWidgetContents_2)
        self.pushButton.setGeometry(QtCore.QRect(170, 180, 141, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.dockWidget_PlotOptions.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_PlotOptions)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionExport_plots = QtGui.QAction(MainWindow)
        self.actionExport_plots.setObjectName(_fromUtf8("actionExport_plots"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExport_plots)
        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.radioButton_Analog, self.radioButton_Digital)
        MainWindow.setTabOrder(self.radioButton_Digital, self.radioButton_NWn)
        MainWindow.setTabOrder(self.radioButton_NWn, self.radioButton_AttSpecs)
        MainWindow.setTabOrder(self.radioButton_AttSpecs, self.radioButton_Bessel)
        MainWindow.setTabOrder(self.radioButton_Bessel, self.radioButton_Butterworth)
        MainWindow.setTabOrder(self.radioButton_Butterworth, self.radioButton_Cheby1)
        MainWindow.setTabOrder(self.radioButton_Cheby1, self.radioButton_Cheby2)
        MainWindow.setTabOrder(self.radioButton_Cheby2, self.radioButton_Elliptical)
        MainWindow.setTabOrder(self.radioButton_Elliptical, self.radioButton_LP)
        MainWindow.setTabOrder(self.radioButton_LP, self.radioButton_HP)
        MainWindow.setTabOrder(self.radioButton_HP, self.radioButton_BP)
        MainWindow.setTabOrder(self.radioButton_BP, self.radioButton_BS)
        MainWindow.setTabOrder(self.radioButton_BS, self.radioButton_AP)
        MainWindow.setTabOrder(self.radioButton_AP, self.plainTextEdit_opt1)
        MainWindow.setTabOrder(self.plainTextEdit_opt1, self.plainTextEdit_opt2)
        MainWindow.setTabOrder(self.plainTextEdit_opt2, self.plainTextEdit_opt3)
        MainWindow.setTabOrder(self.plainTextEdit_opt3, self.plainTextEdit_opt4)
        MainWindow.setTabOrder(self.plainTextEdit_opt4, self.radioButton_matchPB)
        MainWindow.setTabOrder(self.radioButton_matchPB, self.radioButton_matchSB)
        MainWindow.setTabOrder(self.radioButton_matchSB, self.plainTextEdit_pbRipple)
        MainWindow.setTabOrder(self.plainTextEdit_pbRipple, self.pushButton_Design)
        MainWindow.setTabOrder(self.pushButton_Design, self.checkBox_Xgrid)
        MainWindow.setTabOrder(self.checkBox_Xgrid, self.checkBox_Xlog)
        MainWindow.setTabOrder(self.checkBox_Xlog, self.doubleSpinBox_Xmin)
        MainWindow.setTabOrder(self.doubleSpinBox_Xmin, self.doubleSpinBox_Xmax)
        MainWindow.setTabOrder(self.doubleSpinBox_Xmax, self.checkBox_Ygrid)
        MainWindow.setTabOrder(self.checkBox_Ygrid, self.checkBox_Ydb)
        MainWindow.setTabOrder(self.checkBox_Ydb, self.doubleSpinBox_Ymin)
        MainWindow.setTabOrder(self.doubleSpinBox_Ymin, self.doubleSpinBox_Ymax)
        MainWindow.setTabOrder(self.doubleSpinBox_Ymax, self.comboBox_frontColor)
        MainWindow.setTabOrder(self.comboBox_frontColor, self.comboBox_backColor)
        MainWindow.setTabOrder(self.comboBox_backColor, self.pushButton_4)
        MainWindow.setTabOrder(self.pushButton_4, self.pushButton)
        MainWindow.setTabOrder(self.pushButton, self.tfOutputHTML)
        MainWindow.setTabOrder(self.tfOutputHTML, self.tabWidget)
        MainWindow.setTabOrder(self.tabWidget, self.graphicsView)
        MainWindow.setTabOrder(self.graphicsView, self.graphicsView_2)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "PyFilter", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_TF), _translate("MainWindow", "Transfer Function", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_plot), _translate("MainWindow", "Frequency Response", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuOptions.setTitle(_translate("MainWindow", "Options", None))
        self.menuAbout.setTitle(_translate("MainWindow", "About", None))
        self.configurationsDock.setWindowTitle(_translate("MainWindow", "Filter options", None))
        self.pushButton_Design.setText(_translate("MainWindow", "Design", None))
        self.groupBox_FilterSpecs.setTitle(_translate("MainWindow", "Filter specs", None))
        self.label_opt1.setText(_translate("MainWindow", "Opt1:", None))
        self.label_opt2.setText(_translate("MainWindow", "Opt2:", None))
        self.label_opt3.setText(_translate("MainWindow", "Opt3:", None))
        self.plainTextEdit_opt3.setToolTip(_translate("MainWindow", "For band-pass and band-stop filters, input 2 parameters, like \'1 2\'.", None))
        self.label_opt4.setText(_translate("MainWindow", "Opt4:", None))
        self.plainTextEdit_opt4.setToolTip(_translate("MainWindow", "For band-pass and band-stop filters, input 2 parameters, like \'1 2\'.", None))
        self.groupBox_Filter_Type.setTitle(_translate("MainWindow", "Filter type", None))
        self.radioButton_LP.setText(_translate("MainWindow", "Low-pass", None))
        self.radioButton_HP.setText(_translate("MainWindow", "High-pass", None))
        self.radioButton_BP.setText(_translate("MainWindow", "Band-pass", None))
        self.radioButton_BS.setText(_translate("MainWindow", "Band-stop", None))
        self.radioButton_AP.setText(_translate("MainWindow", "All-pass", None))
        self.groupBox_Filter_Top.setTitle(_translate("MainWindow", "Filter topology", None))
        self.radioButton_Butterworth.setText(_translate("MainWindow", "Butterworth", None))
        self.radioButton_Cheby1.setText(_translate("MainWindow", "Chebyshev Type1", None))
        self.radioButton_Cheby2.setText(_translate("MainWindow", "Chebyshev Type2", None))
        self.radioButton_Elliptical.setText(_translate("MainWindow", "Elliptical", None))
        self.radioButton_Bessel.setText(_translate("MainWindow", "Bessel", None))
        self.groupBox_AD.setTitle(_translate("MainWindow", "Analog or digital?", None))
        self.radioButton_Analog.setText(_translate("MainWindow", "Analog", None))
        self.radioButton_Digital.setText(_translate("MainWindow", "Digital", None))
        self.groupBox_Options.setTitle(_translate("MainWindow", "Options", None))
        self.radioButton_matchPB.setText(_translate("MainWindow", "Match passband", None))
        self.radioButton_matchSB.setText(_translate("MainWindow", "Match stopband", None))
        self.label_pbRipple.setText(_translate("MainWindow", "Passband ripple \n"
" (dB)", None))
        self.groupBox_paramCalc.setTitle(_translate("MainWindow", "Parameter calculation...", None))
        self.radioButton_NWn.setText(_translate("MainWindow", "From N, Wn", None))
        self.radioButton_AttSpecs.setText(_translate("MainWindow", "From attenuation specs", None))
        self.dockWidget_PlotOptions.setWindowTitle(_translate("MainWindow", "Plot options", None))
        self.label_2.setText(_translate("MainWindow", "Back color:", None))
        self.label.setText(_translate("MainWindow", "Frontal color:", None))
        self.checkBox_Ydb.setText(_translate("MainWindow", "dB", None))
        self.checkBox_Xlog.setText(_translate("MainWindow", "Log", None))
        self.label_4.setText(_translate("MainWindow", "Y:", None))
        self.checkBox_Ygrid.setText(_translate("MainWindow", "Grid", None))
        self.checkBox_Xgrid.setText(_translate("MainWindow", "Grid", None))
        self.label_3.setText(_translate("MainWindow", "X:", None))
        self.pushButton_4.setText(_translate("MainWindow", "Redraw graph", None))
        self.pushButton.setText(_translate("MainWindow", "Write to File", None))
        self.actionOpen.setText(_translate("MainWindow", "Open...", None))
        self.actionSave.setText(_translate("MainWindow", "Save...", None))
        self.actionExport_plots.setText(_translate("MainWindow", "Export plots...", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionAbout.setText(_translate("MainWindow", "About this program...", None))

from PyQt4 import QtWebKit
