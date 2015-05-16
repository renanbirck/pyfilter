#!/usr/bin/env python3
# coding: utf-8

# Common files for both analog and digital GUIs.
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox

critical = QMessageBox.critical
information = QMessageBox.information
warning = QMessageBox.information
question = QMessageBox.question


class common_tools():
    parent = None

    def __init__(self, parent):
        if not parent:
            raise TypeError("I need a QMainWindow as my parent.")
        self.parent = parent

    def set_status_bar(self, text):
        """ Sets the status bar to text. """
        self.parent.statusBar = QtGui.QStatusBar(self.parent)
        self.parent.setStatusBar(self.parent.statusBar)
        self.parent.statusBar.showMessage(text)

    def menuAbout(self):
        information(parent, 'About PyFilter...',
                    'PyFilter 0.1 (c) 2015 Renan Birck.')


