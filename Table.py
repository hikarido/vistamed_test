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
            
        query_client = QSqlQuery('select firstName, lastName, patrName, sex, birthDate from Client where deleted = 0;')
        query_client_passport = QSqlQuery('select serial, number, date from ClientDocument where client_id in (select id from Client where deleted = 0);')
        query_client_policy = QSqlQuery('select serial, number, endDate from ClientPolicy where client_id in (select Client.id from Client where Client.deleted = 0);')
        
        valid = (query_client.exec_(), query_client_passport.exec_(), query_client_policy.exec_())        
        
        if(False in valid):
            report = zip(['query_client', 'query_client_passport', 'query_client_policy'], valid)
            msg = str(report)
            raise Exception('Can\'t make correct query to mysql' + msg)
        
        
        self.setColumnCount(len(self.headers))
        self.setRowCount(query_client.size()) 

        current_year = QtCore.QDate().currentDate().year()     
                
        index = 0
        while(query_client.next() and query_client_passport.next()):
            
            full_name = ' '.join([query_client.value(0), query_client.value(1), query_client.value(2)])

            age_birth_date = ' age, '.join([str(current_year - query_client.value(4).year()), query_client.value(4).toString()])

            sex = u'мужской'
            if query_client.value(3) == 2:
                sex = u'женский'
                
            passport_data = ' '.join([query_client_passport.value(0), query_client_passport.value(1), query_client_passport.value(2).toString()])
            policy_data = 'Not exist'
                
            self.setItem(index,0,QtGui.QTableWidgetItem(full_name))
            self.setItem(index,1,QtGui.QTableWidgetItem(age_birth_date))
            self.setItem(index,2,QtGui.QTableWidgetItem(sex))

            if(query_client_policy.next()):
                policy_data = ' '.join([query_client_policy.value(0), query_client_policy.value(1), query_client_policy.value(2).toString()])
                self.setItem(index,3, QtGui.QTableWidgetItem(policy_data))
            
            self.setItem(index,4, QtGui.QTableWidgetItem(passport_data))
            
#            self.setItem(index,3,QtGui.QTableWidgetItem(str(current_year - query.value(3).year())))
            index += 1
            
        
        
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    
    table = Table()
    table.show()
    
    sys.exit(app.exec_())