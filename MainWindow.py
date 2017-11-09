# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from ViewerWidget import Viewer
from SettingsWindow import SettingsWindow
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
        self.settings_window = SettingsWindow()
        self.window.show()
        
    def set_signals(self):
        self.window.open_settings_signal.connect(self.open_settings)
        self.window.reload_database_signal.connect(self.reload_database)
        self.window.close_application_signal.connect(self.close_application)
        self.settings_window.new_data_already_signal.connect(self.new_data_already)
        
    def new_data_already(self):
        self.window.table.load_data(default = False, settings = self.settings_window.get_settings())        
        
    def open_settings(self):
        self.settings_window.show()
        
    def reload_database(self):
        new_data = self.settings_window.get_settings()
        if str() in new_data.values():
            print('Empty settings. New settings not installed.')
        else:        
            self.window.table.load_data(default = False, settings = new_data)
        
    def close_application(self):
        self.quit()


if __name__ == '__main__':
    print('ok')
    app = MainWindow()