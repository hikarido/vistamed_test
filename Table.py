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
    реализует сортировку по столбцам, поиск и подстветку найденных элементов
    '''
    def __init__(self, parent=None):
        QtGui.QTableWidget.__init__(self, parent)        
        
        self.headers = u"ФИО;Возрост;Пол;Полис;Паспорт".split(";")
        self.header_len = len(self.headers);
        self.load_data(default = True) 
        self.setHorizontalHeaderLabels(self.headers)
        self.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

        for i in range(0, self.columnCount()):
            self.horizontalHeader().setResizeMode(i, QtGui.QHeaderView.Stretch)
                            
                  
                 
    def load_data(self, default = True, settings = dict()):
        '''
            Загружает данные из БД по параметрам из settings полученным из окна настроек @see SettingsWindow
            или использует параметры по умолчанию
        '''
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
        
        try:
            if(ok):
                print('Connected')
            else:
                print('Connection data is incorrect')
                raise Exception()
        except Exception:
            db.close()
            QSqlDatabase.removeDatabase("qt_sql_default_connection");
            return
        
        while(self.rowCount() > 0):
            self.removeRow(0)
        
        '''
            Один запрос на все данные 
            - ФИО
            - дата рождения + возраст
            - пол
            - информация о действующем полисе ОМС при наличии
            - информация о действующем документе (паспорт, свидетельство о рождении и т.д.)
        '''
        query_client = QSqlQuery('select C.firstName, C.lastName, C.patrName, C.sex, C.birthDate, CP.serial, CP.number, CP.endDate, CD.serial, CD.number, CD.date from Client C left\
                                join ClientPolicy CP on C.id = CP.client_id left join ClientDocument CD on CD.client_id = C.id;')
        
        try:
            if(query_client.exec_() == False):
                raise Exception()
        except Exception:
            print('Can\'t make correct query to mysql')
            db.close()            
            QSqlDatabase.removeDatabase("qt_sql_default_connectiont");
            return
        
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
        QSqlDatabase.removeDatabase("vistamed_test");

    def present_search(self, text):
        '''
            производит поиск по text метдом QtCore.Qt.MatchContains
            снимает предыдущее выделение
            ищит вхождения
            подствечивает строки таблицы по вхождениям
        '''
        self.clearSelection()
#        filter_exp = QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive)
        print(text)
        iteams = self.findItems(text, QtCore.Qt.MatchContains)
        selected = []
        print(iteams)
        for i in iteams:
            if i.row() in selected:
                continue
            self.selectRow(i.row());
            selected.append(i.row())
    

        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    
    table = Table()
    table.show()
    
    sys.exit(app.exec_())