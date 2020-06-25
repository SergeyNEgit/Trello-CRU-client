Trello-CRU-client 

SkillFactory D1.10 HW Trello console CRU (Create-Read-Update) client

Важно! 
Требуется установить пакет работы с datetime:  
  pip install python-dateutil
или убрать форматирование даты: 
... dup.parse(task['dateLastActivity']).strftime("%d.%m.%Y %H:%M:%S")

Данные авторизации в Trello:  
  {'key': "414d13a43ea879c2f26c593e26a2fd3d", 'token': "36dfb3c022ef0c912bbcf7b895531a1dfd735efe66f93c6f51f910396fc1a841"}  

Доска https://trello.com/b/Fx11R3X9/created-with-trelloapi:
  {'id': '5ed3993eb091f30d88e84582', 'name': 'Created with TrelloApi'}

Методы Trello-CRU-client:

python D1-10-HW-trello-CRU-client.py list column_name 
- создание колонки column_name

python D1-10-HW-trello-CRU-client.py [read] 
- список задач по колонкам, с указанием id задачи 

python D1-10-HW-trello-CRU-client.py create task_name column_name 
- создание задачи task_name в колонке column_name 

python D1-10-HW-trello-CRU-client.py move task_name column_name 
- перемещение задачи task_name в колонку column_name
