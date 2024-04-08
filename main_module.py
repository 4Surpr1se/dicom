import copy
import json
import os
import re
import sys
import datetime
import matplotlib
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint
from PyQt5.QtWidgets import QScrollArea, QTabWidget, QGridLayout, QLabel, QPushButton, QTableWidget
from matplotlib.text import Annotation
from mpldatacursor import datacursor


matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.child = MplCanvas(self, width=5, height=4, dpi=100)
        self.child.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        self.child.setStyleSheet("background-color:red;border-radius:15px;")
        self.child.resize(100, 100)
        self.anim = QPropertyAnimation(self.child, b"pos")
        # self.anim.setEndValue(QPoint(400, 400))
        # self.anim.setDuration(1500)
        self.anim.start()
        self.setCentralWidget(self.child)

        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()

