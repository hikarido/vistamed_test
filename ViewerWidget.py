# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 10:55:06 2017

@author: takava
"""

# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import Table

class Viewer(QtGui.QWidget):
    '''
        Агрегирует все графические компоненты приложения
        и управляет их сигналами
    '''

    open_settings_signal = QtCore.pyqtSignal(name = 'open_settings')
    reload_database_signal = QtCore.pyqtSignal(name = 'reload_database')
    close_application_signal = QtCore.pyqtSignal(name = 'close_application')
    
    def __init__(self):
        QtGui.QWidget.__init__(self, parent = None)
        self.make_viewer()   
        self.set_signals()
        
    def make_viewer(self):
        '''
            Размещает графические компоненты приложения
        '''
    
        self.settingsBox = QtGui.QComboBox()
        self.settingsBox.addItem('Settings')
        self.settingsBox.addItem('Reload')
        self.settingsBox.addItem('Quit')
        
        self.table = Table.Table()
        self.search_line = QtGui.QLineEdit()
        self.search_lina_label = QtGui.QLabel('Search')
        self.btn_search = QtGui.QPushButton('Search')
        
        self.table.setSortingEnabled(True)
        self.vLayout = QtGui.QVBoxLayout()
        self.vLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.vLayout.addWidget(self.settingsBox)
        self.vLayout.addWidget(self.table)
        self.vLayout.addWidget(self.search_lina_label)
        self.vLayout.addWidget(self.search_line) 
        self.vLayout.addWidget(self.btn_search)
        self.setLayout(self.vLayout)
        self.setWindowFlags((QtCore.Qt.WindowFlags() | \
        QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowMaximizeButtonHint) &\
        ~QtCore.Qt.WindowCloseButtonHint)
        
    def set_signals(self):
        self.settingsBox.activated.connect(self.signal_listener)
        self.btn_search.clicked.connect(self.make_search)
                
        
    def signal_listener(self, name):
        if(name == 0):
            self.open_settings_signal.emit()
        elif name == 1:
            self.reload_database_signal.emit()
        else:
            self.close_application_signal.emit()
            
    def make_search(self): 
        self.table.present_search(self.search_line.text())
        
 
            
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = Viewer()
    window.setWindowTitle("VistaMed test applocation")
    window.setGeometry(QtCore.QRect(100, 100, 800, 600))
    window.show()
    
    sys.exit(app.exec_())

