import sys

from PyQt5 import QtWidgets

from working_temp import MainWindow

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
# w.resize(640, 480)
w.show()

sys.exit(app.exec_())