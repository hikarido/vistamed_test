# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from ViewerWidget import Viewer
import sys

class MainWindow(QtGui.QApplication):
    def __init__(self):
        QtGui.QApplication.__init__(self, sys.argv)
        
        self.make_gui()        
        
        sys.exit(self.exec_())
        
    def make_gui(self):
        self.window = Viewer()
        self.window.setWindowTitle("VistaMed test applocation")
        self.window.setGeometry(QtCore.QRect(100, 100, 900, 600))
        self.window.show()


if __name__ == '__main__':
    print('ok')
    app = MainWindow()