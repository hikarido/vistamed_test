# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from ViewerWidget import Viewer
import sys

class MainWindow(QtGui.QApplication):
    def __init__(self):
        QtGui.QApplication.__init__(self, sys.argv)
        
        self.make_gui() 
        self.set_signals()
        
        sys.exit(self.exec_())
        
    def make_gui(self):
        self.window = Viewer()
        self.window.setWindowTitle("VistaMed test applocation")
        self.window.setGeometry(QtCore.QRect(100, 100, 900, 600))
        self.window.show()
        
    def set_signals(self):
        self.window.open_settings_signal.connect(self.open_settings)
        self.window.reload_database_signal.connect(self.reload_database)
        self.window.close_application_signal.connect(self.close_application)
        
    def open_settings(self):
        print('open settings')
        
    def reload_database(self):
        print('reload data base')
        
    def close_application(self):
        self.quit()
        print('close application')


if __name__ == '__main__':
    print('ok')
    app = MainWindow()