# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyfilter_plot_config_widget.ui'
#
# Created: Sat Feb 28 18:25:00 2015
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

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(400, 300)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.checkBox = QtGui.QCheckBox(self.dockWidgetContents)
        self.checkBox.setGeometry(QtCore.QRect(10, 20, 89, 21))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox_2 = QtGui.QCheckBox(self.dockWidgetContents)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 40, 89, 21))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.checkBox_3 = QtGui.QCheckBox(self.dockWidgetContents)
        self.checkBox_3.setGeometry(QtCore.QRect(10, 80, 89, 21))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.checkBox_4 = QtGui.QCheckBox(self.dockWidgetContents)
        self.checkBox_4.setGeometry(QtCore.QRect(10, 100, 131, 21))
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setGeometry(QtCore.QRect(20, 130, 101, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setGeometry(QtCore.QRect(34, 168, 81, 10))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.comboBox = QtGui.QComboBox(self.dockWidgetContents)
        self.comboBox.setGeometry(QtCore.QRect(100, 130, 161, 25))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox_2 = QtGui.QComboBox(self.dockWidgetContents)
        self.comboBox_2.setGeometry(QtCore.QRect(100, 160, 161, 25))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.dockWidgetContents)
        self.doubleSpinBox.setGeometry(QtCore.QRect(130, 10, 101, 25))
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.dockWidgetContents)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(280, 10, 101, 25))
        self.doubleSpinBox_2.setObjectName(_fromUtf8("doubleSpinBox_2"))
        self.doubleSpinBox_3 = QtGui.QDoubleSpinBox(self.dockWidgetContents)
        self.doubleSpinBox_3.setGeometry(QtCore.QRect(130, 40, 101, 25))
        self.doubleSpinBox_3.setObjectName(_fromUtf8("doubleSpinBox_3"))
        self.doubleSpinBox_4 = QtGui.QDoubleSpinBox(self.dockWidgetContents)
        self.doubleSpinBox_4.setGeometry(QtCore.QRect(280, 40, 101, 25))
        self.doubleSpinBox_4.setObjectName(_fromUtf8("doubleSpinBox_4"))
        self.pushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton.setGeometry(QtCore.QRect(110, 220, 141, 26))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "Plot options", None))
        self.checkBox.setText(_translate("DockWidget", "X grid", None))
        self.checkBox_2.setText(_translate("DockWidget", "Y grid", None))
        self.checkBox_3.setText(_translate("DockWidget", "X log scale", None))
        self.checkBox_4.setText(_translate("DockWidget", "Y log scale (dB)", None))
        self.label.setText(_translate("DockWidget", "Frontal color:", None))
        self.label_2.setText(_translate("DockWidget", "Back color:", None))
        self.pushButton.setText(_translate("DockWidget", "Redraw graph", None))

