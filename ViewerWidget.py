# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 10:55:06 2017

@author: takava
"""

# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import Table

class Viewer(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self, parent = None)
        self.make_viewer()   
        self.set_signals()
        
    def make_viewer(self):
        
        self.btnQuit = QtGui.QPushButton('Quit')
        self.table = Table.Table()
        
        self.vLayout = QtGui.QVBoxLayout()
        self.vLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.vLayout.addWidget(self.table)
        self.vLayout.addWidget(self.btnQuit)
        self.setLayout(self.vLayout)
        
    def set_signals(self):
        self.connect(self.btnQuit, QtCore.SIGNAL('clicked()'), QtGui.qApp.quit)           
       
 
            
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = Viewer()
    window.setWindowTitle("VistaMed test applocation")
    window.setGeometry(QtCore.QRect(100, 100, 800, 600))
    window.show()
    
    sys.exit(app.exec_())

