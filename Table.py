# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 11:31:56 2017

@author: takava
"""
from PyQt4 import QtGui, QtCore
from PyQt4.QtSql import QSqlDatabase, QSqlQuery

class Table(QtGui.QTableWidget):
    '''
    Загружает данные из базы данных и выводит их в таблицу
    реализует сортировку по столбцам
    '''
    def __init__(self, parent=None):
        QtGui.QTableWidget.__init__(self, parent)        
        
        self.headers = u"ФИО;Возрост;Пол;Полис;Паспорт".split(";")
        self.header_len = len(self.headers);
        self.load_data(default = True) 
        self.setHorizontalHeaderLabels(self.headers)                            
                  
    def load_data(self, default = True, settings = dict()):
        if default:
            db = QSqlDatabase.addDatabase('QMYSQL');
            db.setHostName('localhost');
            db.setDatabaseName('vistamed_test');
            db.setUserName('root');
            db.setPassword('hero123001');
        else:
            db = QSqlDatabase.addDatabase('QMYSQL');
            db.setHostName(settings['Host Name']);
            db.setDatabaseName(settings['DataBase name']);
            db.setUserName(settings['User Name']);
            db.setPassword(settings['Password']);
        
        ok = db.open();
        if(ok):
            print('Connected')
        else:
            print('can\'t to connect to data base')
            raise Exception('Connection data incorrect')
            
        while(self.rowCount() > 0):
            self.removeRow(0)
        
        query_client = QSqlQuery('select C.firstName, C.lastName, C.patrName, C.sex, C.birthDate, CP.serial, CP.number, CP.endDate, CD.serial, CD.number, CD.date from Client C left\
                                join ClientPolicy CP on C.id = CP.client_id left join ClientDocument CD on CD.client_id = C.id;')
        
        
        if(query_client.exec_() == False):
            raise Exception('Can\'t make correct query to mysql')
        
        
        self.setColumnCount(len(self.headers))
        self.setRowCount(query_client.size()) 

        current_year = QtCore.QDate().currentDate().year()     
                
        index = 0
        while(query_client.next()):
            
            full_name = ' '.join([query_client.value(0), query_client.value(1), query_client.value(2)])

            age_birth_date = ' age, '.join([str(current_year - query_client.value(4).year()), \
            query_client.value(4).toString()])

            sex = u'мужской'
            if query_client.value(3) == 2:
                sex = u'женский'
            
            if isinstance(query_client.value(8), QtCore.QPyNullVariant):
                self.setItem(index,4, QtGui.QTableWidgetItem(u'Отсутствует'))
            else:    
                passport_data = ' '.join([str(query_client.value(8)), str(query_client.value(9)),\
                query_client.value(10).toString()])
                self.setItem(index,4, QtGui.QTableWidgetItem(passport_data))                            
            
            self.setItem(index,0,QtGui.QTableWidgetItem(full_name))
            self.setItem(index,1,QtGui.QTableWidgetItem(age_birth_date))
            self.setItem(index,2,QtGui.QTableWidgetItem(sex))

            if(isinstance(query_client.value(5), QtCore.QPyNullVariant)):
                self.setItem(index,3, QtGui.QTableWidgetItem(u'Отсутствует'))
            else:    
                policy_data = ' '.join([query_client.value(5), query_client.value(6), \
                query_client.value(7).toString()])
                self.setItem(index,3, QtGui.QTableWidgetItem(policy_data))
        
            index += 1
            
        db.close()
        
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    
    table = Table()
    table.show()
    
    sys.exit(app.exec_())