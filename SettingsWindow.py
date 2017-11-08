# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 18:20:02 2017

@author: takava
"""

from PyQt4 import QtCore, QtGui, uic

class SettingsWindow(QtGui.QDialog):
    
    new_data_already_signal = QtCore.pyqtSignal(name = 'new_data_already')
    
    def __init__(self, parent= None):
        QtGui.QDialog.__init__(self)
        uic.loadUi("/home/takava/Forge/vistamed_test/dialog.ui", self)
        self.setWindowTitle("Settings")
        self.set_signals()
        
    def set_signals(self):
        self.end_dialog.clicked.connect(self.close_dialog)
        
    def close_dialog(self):
        self.new_data_already_signal.emit()
        self.hide()
        
    def get_settings(self):
        data = dict()
        for i in range(0, self.gridLayout.rowCount()):
            key = self.gridLayout.itemAtPosition(i, 0).widget().text()            
            value = self.gridLayout.itemAtPosition(i, 1).widget().text();
            data[key] = value
        return data
        
        
if __name__ == '__main__':
    print('ok')
    import sys
    app = QtGui.QApplication(sys.argv)
    
    dialog = SettingsWindow()
    dialog.show()
    
    sys.exit(app.exec_())