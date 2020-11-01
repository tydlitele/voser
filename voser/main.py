from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
import sys
import gui

app = QApplication(sys.argv)

window = gui.MainWindow()
window.show()
app.exec_()