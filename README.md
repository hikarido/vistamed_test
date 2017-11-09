

# vistamed_test
## Тестовое задание для Vistamed

Задача ваполнена в ООП стиле. Программа подключается к mysql и забирает данные по следующему запросу в класс Table, который унаследован от QTableWidget:
```select 
	C.firstName,
	C.lastName,
	C.patrName,
	C.sex,
	C.birthDate,
	CP.serial,
	CP.number,
	CP.endDate,
	CD.serial,
	CD.number,
	CD.date 

from Client C 
left join 
	ClientPolicy CP on C.id = CP.client_id 
left join 
	ClientDocument CD on CD.client_id = C.id;
```

получается таблицу вида: 
![selected Table](https://yadi.sk/i/8pzQ3NbX3PYNKY)
## Классы 
* класса SettingsWindow содержит поля для ввыода настроек
* Класс Table выполняет поиск в таблице по флагу QtCore.Qt.MatchContains и тексту из ViewerWidget.search_line, подсвечивает строки с вхождениями. Поиск выполняется по нажатию кнопки Search
* Класс ViewerWidget унаследованный от QtGui.QWidget отображает все графические компоненты программы и управляет их сигналами
## Кнопки
* Кнопка Reload забирает данные из полей класса SettingsWindow и передает их Table для перезагрузки таблицы
* Кнопка Quit завершает работу программы
* Кнопка Settings вызывает окно настроек, при нажатии кнопки ОК, программа актоматически делаетпопытку считать данные из БД
## Сообщения об ошибках:
* Connection data is incorrect - программа не смогла подключиться к базе данных
* Can't make correct query to mysql - программе не удалось выполнить запрос к базу данных





        

