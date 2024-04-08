# -*- coding: utf-8 -*-
import os
import zipfile
from distutils.dir_util import copy_tree
from working_temp import MainWindow as MainChart

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QPushButton
import pydicom.encoders.gdcm
import pydicom.encoders.pylibjpeg
import pydicom.encoders
import scipy.special
import scipy.special._cdflib


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button = QPushButton(MainWindow)
        self.button.setGeometry(QtCore.QRect(0, 0, 800, 109))
        self.button.clicked.connect(self.file_browser)
        # MainWindow.setCentralWidget(self.button)
        # file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        # MainWindow.set(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 100, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.button_ok = QPushButton(MainWindow)
        self.button_ok.setGeometry(QtCore.QRect(0, 110, 800, 109))
        self.button_ok.clicked.connect(self.open_chart)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button.setText(_translate("MainWindow", "Выбрать файл"))
        self.button_ok.setText(_translate("MainWindow", "Открыть график"))


    def open_chart(self):
        w = MainChart(self.path)
        w.exec()

    def file_browser(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.show()
        if dialog.exec_():
            self.files_container = dialog.selectedFiles()[0]
            self.copy_files(self.files_container)

    def copy_files(self, file):
        dir_name = './data_stor'
        if 'data_stor' not in os.listdir('./'):
            os.mkdir(dir_name)
        print(file)
        dir_name_inside = file.split('/')[-1]
        path = os.path.join(dir_name, dir_name_inside)
        if dir_name_inside not in os.listdir(dir_name):
            os.mkdir(path)
        self.path = path
        copy_tree(file, path)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
