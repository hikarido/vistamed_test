# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 18:20:02 2017

@author: takava
"""

from PyQt4 import QtCore, QtGui, uic

class SettingsWindow(QtGui.QDialog):
    '''
        всплывающее окно настроек приложения
        Настройки:
        - имя хоста 
        - идентификатор БД mysql
        - имя пользователя mysql
        - пароль пользователя mysql
        сигнал new_data_already_signal возбуждается при закрытии окна
    '''

    new_data_already_signal = QtCore.pyqtSignal(name = 'new_data_already')
    
    def __init__(self, parent= None):
        QtGui.QDialog.__init__(self)
        uic.loadUi("dialog.ui", self)
        self.setWindowTitle("Settings")
        self.setWindowFlags((QtCore.Qt.WindowFlags() | QtCore.Qt.CustomizeWindowHint) & ~QtCore.Qt.WindowCloseButtonHint)
        self.set_signals()
        
    def set_signals(self):
        self.end_dialog.clicked.connect(self.close_dialog)
        
    def close_dialog(self):
        self.new_data_already_signal.emit()
        self.hide()
        
    def get_settings(self):
        '''
            возвращает словарь с новыми настройками
        '''
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
